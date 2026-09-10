"""Workspace, project-policy, and topology registry primitives.

The module deliberately keeps the registry limited to locators and topology
metadata.  Project documents, lifecycle state, and telemetry records remain in
their owning repositories/files.
"""

from __future__ import annotations

from copy import deepcopy
from fnmatch import fnmatchcase
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any, Mapping

import yaml

from .local_update import load_ownership_policy


HOME_ENV = "PLANNING_LITE_HOME"
CENTRAL_ROOT_ENV = "PLANNING_LITE_CENTRAL_ROOT"
LOCAL_ROOT_NAME = ".local"
REGISTRY_FILENAME = "projects.yml"
LOCAL_ROUTE_RELATIVE: dict[str, Path] = {
    "config": Path("."),
    "registry": Path("registry"),
    "consumer_state": Path("state") / "projects",
    "roadmap_inbox": Path("inbox") / "roadmaps",
    "recommendation_inbox": Path("inbox") / "recommendations",
    "compiled_prompts": Path("work") / "compiled-prompts",
    "experiments": Path("work") / "experiments",
    "cache": Path("cache"),
}
ANSWERS_FILENAME = ".copier-answers.planning-lite.yml"
LEGACY_POLICY_FALLBACK: dict[str, Any] = {
    # Only used when a legacy consumer has no managed project_policy block.
    # Current consumers receive the complete policy from framework/defaults.yml.
    "schema_version": 1,
    "project_id": None,
    "planning_root": ".planning",
    "agents_root": ".agents",
    "control_history_mode": None,
    "secret_storage": "prohibited",
    "forbidden_read_paths": [],
    "telemetry": {"enabled": False},
}
ALLOWED_MODES = {"single-repo", "split-control", "local-only"}
ALLOWED_PROJECT_STATUSES = {"active", "paused", "archived"}
ALLOWED_SOURCE_TYPES = {"external_runtime", "operator", "unavailable"}


class WorkspaceError(RuntimeError):
    """Fail-closed workspace or registry operation."""


def central_repository_root(explicit: str | Path | None = None) -> Path:
    """Resolve the central source repository without inventing a user-home path.

    An explicit root or ``PLANNING_LITE_CENTRAL_ROOT`` is authoritative.  When
    running from the central source checkout, the package location provides a
    deterministic relative route.  Installed consumers must supply an
    explicit root because their package directory is not a central repository.
    """

    raw = explicit
    if raw is None:
        environment = os.environ.get(CENTRAL_ROOT_ENV)
        if environment and environment.strip():
            raw = environment.strip()
    if raw is not None and str(raw).strip():
        candidate = Path(raw).expanduser().resolve()
    else:
        candidate = Path(__file__).resolve().parents[2]
    if not (candidate / "copier.yml").is_file() or not (candidate / "template").is_dir():
        raise WorkspaceError(
            "ARTIFACT_ROUTING_UNRESOLVED: central Planning Lite repository root "
            "is unavailable; set PLANNING_LITE_CENTRAL_ROOT or pass an explicit home"
        )
    return candidate


def local_operational_root(explicit_central_root: str | Path | None = None) -> Path:
    """Return the central repository-local operational root."""

    return central_repository_root(explicit_central_root) / LOCAL_ROOT_NAME


def local_route(route: str, home: str | Path | None = None) -> Path:
    """Resolve one of the canonical local operational routes.

    Route names are deliberately closed.  An unknown route fails closed rather
    than allowing a caller to invent a second persistent data location.
    """

    relative = LOCAL_ROUTE_RELATIVE.get(route)
    if relative is None:
        raise WorkspaceError(f"ARTIFACT_ROUTING_UNRESOLVED: unknown local route: {route}")
    return resolve_home(home) / relative


def _forbidden_product_path(
    product_root: Path, path: str | Path, patterns: list[str] | tuple[str, ...]
) -> bool:
    root = product_root.resolve()
    candidate = Path(path).expanduser().resolve()
    try:
        relative = candidate.relative_to(root).as_posix()
    except ValueError:
        return False
    absolute = candidate.as_posix()
    for raw in patterns:
        pattern = str(raw).replace("\\", "/").strip().rstrip("/")
        if pattern.startswith("./"):
            pattern = pattern[2:]
        if not pattern:
            continue
        candidates = [pattern]
        if pattern.endswith("/**"):
            candidates.append(pattern[:-3].rstrip("/"))
        if (
            any(fnmatchcase(relative, candidate) for candidate in candidates)
            or any(fnmatchcase(absolute, candidate) for candidate in candidates)
            or any(
                relative == candidate or relative.startswith(candidate + "/")
                for candidate in candidates
            )
            or any(
                absolute == candidate or absolute.startswith(candidate + "/")
                for candidate in candidates
            )
        ):
            return True
    return False


def _guard_product_read(
    product_root: Path,
    path: str | Path,
    forbidden_read_paths: list[str] | tuple[str, ...],
) -> Path:
    root = product_root.resolve()
    candidate = Path(path).expanduser().resolve()
    try:
        relative = candidate.relative_to(root).as_posix()
    except ValueError as exc:
        raise WorkspaceError(f"Inspection path escapes product root: {candidate}") from exc
    if _forbidden_product_path(root, candidate, forbidden_read_paths):
        raise WorkspaceError(f"Forbidden read path: {relative}")
    return candidate


def _product_git_context(
    product_root: Path, forbidden_read_paths: list[str] | tuple[str, ...]
) -> dict[str, Any]:
    _guard_product_read(product_root, product_root / ".git", forbidden_read_paths)
    configured = (product_root / ".git").exists()
    probe = product_git(product_root, "rev-parse", "--git-dir")
    if probe.returncode != 0:
        return {
            "configured": configured,
            "available": False,
            "head": None,
            "clean": None,
            "status_reason": "git_unavailable",
        }
    if forbidden_read_paths:
        head = product_git(product_root, "rev-parse", "HEAD")
        return {
            "configured": True,
            "available": True,
            "head": head.stdout.strip() if head.returncode == 0 else None,
            "clean": None,
            "status_reason": "forbidden_read_paths_prevent_full_status",
        }
    status = product_git(product_root, "status", "--porcelain")
    head = product_git(product_root, "rev-parse", "HEAD")
    return {
        "configured": True,
        "available": True,
        "head": head.stdout.strip() if head.returncode == 0 else None,
        "clean": not status.stdout.strip() if status.returncode == 0 else None,
        "status_reason": None if status.returncode == 0 else "git_status_unavailable",
    }


def _control_git_context(
    product_root: Path,
    planning_root: Path,
    forbidden_read_paths: list[str] | tuple[str, ...],
) -> dict[str, Any]:
    marker = _guard_product_read(product_root, planning_root / ".git", forbidden_read_paths)
    configured = marker.exists()
    if not configured:
        return {
            "configured": False,
            "available": False,
            "git_dir": None,
            "head": None,
            "clean": None,
            "status_reason": "control_git_not_configured",
        }
    try:
        git_dir = resolve_control_git_dir(planning_root)
    except WorkspaceError as exc:
        return {
            "configured": True,
            "available": False,
            "git_dir": None,
            "head": None,
            "clean": None,
            "error": str(exc),
            "status_reason": "control_git_unavailable",
        }
    if git_dir is None:
        return {
            "configured": True,
            "available": False,
            "git_dir": None,
            "head": None,
            "clean": None,
            "status_reason": "control_git_unavailable",
        }
    probe = control_git(planning_root, git_dir, "rev-parse", "--git-dir")
    head = control_git(planning_root, git_dir, "rev-parse", "HEAD")
    if forbidden_read_paths:
        return {
            "configured": True,
            "available": probe.returncode == 0,
            "git_dir": str(git_dir),
            "head": head.stdout.strip() if head.returncode == 0 else None,
            "clean": None,
            "status_reason": "forbidden_read_paths_prevent_full_status",
        }
    status = control_git(planning_root, git_dir, "status", "--porcelain")
    return {
        "configured": True,
        "available": probe.returncode == 0,
        "git_dir": str(git_dir),
        "head": head.stdout.strip() if head.returncode == 0 else None,
        "clean": not status.stdout.strip() if status.returncode == 0 else None,
        "status_reason": None if status.returncode == 0 else "git_status_unavailable",
    }


def product_git(project_root: str | Path, *args: str) -> subprocess.CompletedProcess[str]:
    """Run a Git command against the explicit product repository."""

    root = Path(project_root).expanduser().resolve()
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def control_git(
    planning_root: str | Path, git_dir: str | Path, *args: str
) -> subprocess.CompletedProcess[str]:
    """Run a Git command against an explicit external control repository."""

    planning = Path(planning_root).expanduser().resolve()
    metadata = Path(git_dir).expanduser().resolve()
    return subprocess.run(
        ["git", "--git-dir", str(metadata), "--work-tree", str(planning), *args],
        check=False,
        capture_output=True,
        text=True,
    )


def _gitfile_target(planning_root: Path) -> Path | None:
    marker = planning_root / ".git"
    if not marker.is_file():
        return None
    try:
        first = marker.read_text(encoding="utf-8").strip().splitlines()[0]
    except (OSError, IndexError):
        return None
    if not first.lower().startswith("gitdir:"):
        return None
    raw = first.split(":", 1)[1].strip()
    return (marker.parent / raw).resolve()


def resolve_control_git_dir(planning_root: str | Path) -> Path | None:
    """Return the external control Git directory from a valid gitfile."""

    planning = Path(planning_root).expanduser().resolve()
    marker = planning / ".git"
    if not marker.exists():
        return None
    target = _gitfile_target(planning)
    if target is None or target.is_relative_to(planning) or target.is_relative_to(planning.parent):
        raise WorkspaceError(".planning/.git is not a valid external Git gitfile")
    if not target.exists() or not target.is_dir():
        raise WorkspaceError(f"External control Git directory is unavailable: {target}")
    if control_git(planning, target, "rev-parse", "--git-dir").returncode != 0:
        raise WorkspaceError(f"External control Git directory is not a repository: {target}")
    return target


def _outer_ignores_planning(product_root: Path) -> bool:
    planning_root = product_root / ".planning"
    probes = [
        ".planning",
        ".planning/",
        ".planning/.planning-lite-control-init-probe",
        ".planning/project/.planning-lite-control-init-probe",
    ]
    try:
        for child in sorted(planning_root.iterdir(), key=lambda path: path.name):
            if child.name != ".git":
                probes.append(f".planning/{child.name}/.planning-lite-control-init-probe")
    except OSError:
        return False
    for relative in probes:
        result = product_git(product_root, "check-ignore", "-q", "--", relative)
        if result.returncode != 0:
            return False
    return True


def _safe_project_id(project_id: str) -> str:
    if not isinstance(project_id, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", project_id):
        raise WorkspaceError("project_id must contain only letters, digits, '.', '_' or '-'")
    return project_id


def _control_gitignore(planning_root: Path) -> str:
    policy = load_ownership_policy(planning_root.parent)
    managed: set[str] = set()
    for pattern in policy.managed:
        normalized = pattern.replace("\\", "/")
        if normalized == ".planning" or normalized == ".planning/":
            continue
        if normalized.startswith(".planning/"):
            normalized = normalized[len(".planning/") :]
        if normalized and not normalized.startswith(".git"):
            managed.add(normalized)
    lines = [
        "# Generated by Planning Lite control-init; managed/reproducible paths only.",
        "# Project-owned paths remain visible to the control repository.",
    ]
    lines.extend(sorted(managed))
    return "\n".join(lines) + "\n"


def plan_control_init(
    target: str | Path,
    *,
    project_id: str,
    home: str | Path | None = None,
    git_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Validate split-control prerequisites and return the proposed topology."""

    product_root = Path(target).expanduser().resolve()
    if not product_root.is_dir():
        raise WorkspaceError(f"Product root does not exist: {product_root}")
    planning_root = (product_root / ".planning").resolve()
    if not planning_root.is_dir():
        raise WorkspaceError(f"Planning root does not exist: {planning_root}")
    if product_git(product_root, "rev-parse", "--show-toplevel").returncode != 0:
        raise WorkspaceError(f"Product root is not a Git repository: {product_root}")
    if not _outer_ignores_planning(product_root):
        raise WorkspaceError("Outer product Git must already ignore .planning completely before control-init")
    safe_id = _safe_project_id(project_id)
    home_root = resolve_home(home)
    metadata = (
        Path(git_dir).expanduser()
        if git_dir
        else local_route("consumer_state", home_root) / safe_id / "control" / f"{safe_id}.git"
    ).resolve()
    if metadata == product_root or metadata.is_relative_to(product_root) or metadata.is_relative_to(planning_root):
        raise WorkspaceError("External control git directory must be outside product and Planning roots")
    existing = planning_root / ".git"
    existing_target = _gitfile_target(planning_root)
    if existing.exists() and existing_target != metadata:
        raise WorkspaceError(".planning/.git already exists but does not match requested external Git directory")
    if existing_target == metadata and metadata.is_dir() and control_git(
        planning_root, metadata, "rev-parse", "--git-dir"
    ).returncode != 0:
        raise WorkspaceError(f"External control Git directory is not a repository: {metadata}")
    return {
        "project_id": safe_id,
        "product_root": product_root,
        "planning_root": planning_root,
        "home": home_root,
        "git_dir": metadata,
        "gitfile": existing,
        "gitignore": planning_root / ".gitignore",
        "gitignore_content": _control_gitignore(planning_root),
        "already_initialized": existing_target == metadata and metadata.is_dir(),
    }


def control_init(
    target: str | Path,
    *,
    project_id: str,
    home: str | Path | None = None,
    git_dir: str | Path | None = None,
) -> dict[str, Any]:
    """Create external split-control metadata without staging or committing."""

    proposal = plan_control_init(target, project_id=project_id, home=home, git_dir=git_dir)
    planning_root: Path = proposal["planning_root"]
    metadata: Path = proposal["git_dir"]
    if not proposal["already_initialized"]:
        metadata.parent.mkdir(parents=True, exist_ok=True)
        command = subprocess.run(
            ["git", "init", "--separate-git-dir", str(metadata), str(planning_root)],
            check=False,
            capture_output=True,
            text=True,
        )
        if command.returncode != 0:
            raise WorkspaceError(command.stderr.strip() or "Cannot initialize external control Git")
    expected_gitignore = proposal["gitignore_content"]
    gitignore_path: Path = proposal["gitignore"]
    if not gitignore_path.exists() or gitignore_path.read_text(encoding="utf-8") != expected_gitignore:
        gitignore_path.write_text(expected_gitignore, encoding="utf-8", newline="\n")
    update_project_policy(
        proposal["product_root"],
        project_id=proposal["project_id"],
        control_history_mode="split-control",
    )
    return proposal


def resolve_home(explicit: str | Path | None = None) -> Path:
    """Resolve the Planning Lite operational home using explicit routes only.

    Explicit ``--home`` and ``PLANNING_LITE_HOME`` remain supported for
    disposable/isolated runs.  The implicit route is the central repository's
    ``.local`` directory; there is no user-profile fallback.
    """

    if explicit is not None and str(explicit).strip():
        return Path(explicit).expanduser().resolve()
    environment = os.environ.get(HOME_ENV)
    if environment and environment.strip():
        return Path(environment.strip()).expanduser().resolve()
    return local_operational_root()


def _mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise WorkspaceError(f"{label} must be a mapping")
    return value


def _deep_merge(base: Mapping[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = deepcopy(dict(base))
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = deepcopy(value)
    return result


def _read_yaml(path: Path, label: str) -> object:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)
    except (OSError, yaml.YAMLError) as exc:
        raise WorkspaceError(f"Cannot read {label} {path}: {exc}") from exc


def _write_yaml_atomic(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = yaml.safe_dump(value, sort_keys=False, allow_unicode=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent)
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
        try:
            directory_fd = os.open(path.parent, os.O_DIRECTORY)
        except (AttributeError, OSError):
            directory_fd = None
        if directory_fd is not None:
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
    finally:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass


def _relative_root(product_root: Path, value: object, field: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        raise WorkspaceError(f"project_policy.{field} must be a non-empty path")
    raw = Path(value)
    if raw.is_absolute():
        raise WorkspaceError(f"project_policy.{field} must be repository-relative")
    resolved = (product_root / raw).resolve()
    try:
        resolved.relative_to(product_root.resolve())
    except ValueError as exc:
        raise WorkspaceError(f"project_policy.{field} escapes the product root") from exc
    return resolved


def validate_project_policy(policy: Mapping[str, Any], product_root: Path) -> dict[str, Any]:
    """Validate and normalize the namespaced effective policy."""

    data = _mapping(policy, "project_policy")
    schema = data.get("schema_version", 1)
    if schema != 1:
        raise WorkspaceError(f"Unsupported project_policy schema_version: {schema!r}")
    mode = data.get("control_history_mode")
    if mode is not None and mode not in ALLOWED_MODES:
        raise WorkspaceError(
            "project_policy.control_history_mode must be single-repo, split-control, "
            "local-only, or null"
        )
    if data.get("secret_storage", "prohibited") != "prohibited":
        raise WorkspaceError("project_policy.secret_storage must be prohibited")
    forbidden = data.get("forbidden_read_paths", [])
    if not isinstance(forbidden, list) or not all(isinstance(item, str) for item in forbidden):
        raise WorkspaceError("project_policy.forbidden_read_paths must be a list of strings")
    planning_root = _relative_root(product_root, data.get("planning_root", ".planning"), "planning_root")
    agents_root = _relative_root(product_root, data.get("agents_root", ".agents"), "agents_root")
    if planning_root == agents_root or planning_root.is_relative_to(agents_root) or agents_root.is_relative_to(planning_root):
        raise WorkspaceError("project_policy.planning_root and agents_root may not overlap")
    project_id = data.get("project_id")
    if project_id is not None:
        if not isinstance(project_id, str) or not project_id.strip():
            raise WorkspaceError("project_policy.project_id must be a non-empty string or null")
        _safe_project_id(project_id.strip())
    normalized = dict(data)
    normalized["planning_root"] = planning_root.relative_to(product_root).as_posix()
    normalized["agents_root"] = agents_root.relative_to(product_root).as_posix()
    if project_id is not None:
        normalized["project_id"] = project_id.strip()
    return normalized


def _load_managed_defaults(product_root: Path) -> dict[str, Any]:
    """Load defaults and apply compatibility only when the key is absent."""

    defaults_path = product_root / ".planning" / "framework" / "defaults.yml"
    defaults_raw: object = {}
    if defaults_path.exists():
        defaults_raw = _read_yaml(defaults_path, "defaults")
    defaults = _mapping(defaults_raw or {}, "defaults")
    if "project_policy" not in defaults:
        defaults = deepcopy(defaults)
        defaults["project_policy"] = deepcopy(LEGACY_POLICY_FALLBACK)
    elif not isinstance(defaults["project_policy"], Mapping):
        raise WorkspaceError("defaults.project_policy must be a mapping")
    return defaults


def load_effective_policy(target: str | Path) -> dict[str, Any]:
    """Merge managed defaults and project-owned CONFIG.yml."""

    product_root = Path(target).expanduser().resolve()
    config_path = product_root / ".planning" / "CONFIG.yml"
    defaults = _load_managed_defaults(product_root)
    overrides_raw: object = {}
    if config_path.exists():
        overrides_raw = _read_yaml(config_path, "project configuration")
    overrides = _mapping(overrides_raw or {}, "project configuration")
    # Managed defaults are the sole authority for current project-policy
    # defaults. The small fallback is used only when the managed key is absent.
    merged = defaults
    merged = _deep_merge(merged, overrides)
    policy = validate_project_policy(_mapping(merged.get("project_policy"), "project_policy"), product_root)
    merged["project_policy"] = policy
    return merged


def update_project_policy(
    target: str | Path,
    *,
    project_id: str | None = None,
    control_history_mode: str | None = None,
    telemetry_enabled: bool | None = None,
) -> dict[str, Any]:
    """Atomically update only explicit project_policy overrides in CONFIG.yml."""

    product_root = Path(target).expanduser().resolve()
    config_path = product_root / ".planning" / "CONFIG.yml"
    existing_raw = _read_yaml(config_path, "project configuration") if config_path.exists() else {}
    config = _mapping(existing_raw or {}, "project configuration")
    if "project_policy" in config and not isinstance(config["project_policy"], Mapping):
        raise WorkspaceError("project_policy must be a mapping")
    policy = _mapping(config.get("project_policy") or {}, "project_policy")
    updated = deepcopy(policy)
    if project_id is not None:
        if not project_id.strip():
            raise WorkspaceError("project_id cannot be empty")
        updated["project_id"] = _safe_project_id(project_id.strip())
    if control_history_mode is not None:
        if control_history_mode not in ALLOWED_MODES:
            raise WorkspaceError(f"Unsupported control history mode: {control_history_mode}")
        updated["control_history_mode"] = control_history_mode
    if telemetry_enabled is not None:
        updated["telemetry"] = {"enabled": bool(telemetry_enabled)}
    candidate_config = deepcopy(config)
    candidate_config["project_policy"] = updated
    candidate = _deep_merge(_load_managed_defaults(product_root), candidate_config)
    validate_project_policy(_mapping(candidate.get("project_policy"), "project_policy"), product_root)
    if policy != updated or "project_policy" not in config:
        config["project_policy"] = updated
        _write_yaml_atomic(config_path, config)
    return updated


def registry_path(home: str | Path | None = None) -> Path:
    return local_route("registry", home) / REGISTRY_FILENAME


def _validate_registry_shape(data: object, *, home: Path) -> dict[str, Any]:
    mapping = _mapping(data, "project registry")
    if mapping.get("schema_version") != 1:
        raise WorkspaceError(f"Unsupported projects.yml schema_version: {mapping.get('schema_version')!r}")
    projects = mapping.get("projects")
    if not isinstance(projects, list):
        raise WorkspaceError("projects.yml projects must be a list")
    normalized: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    seen_roots: set[Path] = set()
    control_dirs: list[Path] = []
    for raw in projects:
        item = _mapping(raw, "project registry entry")
        project_id = item.get("project_id")
        root_raw = item.get("project_root")
        if not isinstance(project_id, str) or not project_id.strip():
            raise WorkspaceError("registry project_id must be a non-empty string")
        project_id = _safe_project_id(project_id.strip())
        if project_id in seen_ids:
            raise WorkspaceError(f"duplicate project_id in registry: {project_id}")
        if not isinstance(root_raw, str) or not root_raw.strip():
            raise WorkspaceError(f"registry project_root missing for {project_id}")
        root = Path(root_raw).expanduser().resolve()
        if root in seen_roots:
            raise WorkspaceError(f"duplicate project_root in registry: {root}")
        status = item.get("project_status")
        if status not in ALLOWED_PROJECT_STATUSES:
            raise WorkspaceError(f"invalid project_status for {project_id}: {status!r}")
        planning = Path(str(item.get("planning_root", root / ".planning"))).expanduser().resolve()
        agents = Path(str(item.get("agents_root", root / ".agents"))).expanduser().resolve()
        if not planning.is_relative_to(root) or not agents.is_relative_to(root):
            raise WorkspaceError(f"registry roots escape product root for {project_id}")
        control = item.get("control_history") or {}
        control = _mapping(control, "control_history")
        mode = control.get("mode")
        if mode not in ALLOWED_MODES:
            raise WorkspaceError(f"invalid control history mode for {project_id}: {mode!r}")
        git_dir_raw = control.get("git_dir")
        if mode == "split-control":
            if not isinstance(git_dir_raw, str) or not git_dir_raw.strip():
                raise WorkspaceError(f"split-control entry lacks control git_dir: {project_id}")
            git_dir = Path(git_dir_raw).expanduser().resolve()
            if git_dir.is_relative_to(root) or git_dir.is_relative_to(planning):
                raise WorkspaceError(f"control git_dir overlaps product/planning root: {project_id}")
            if any(git_dir == other or git_dir.is_relative_to(other) or other.is_relative_to(git_dir) for other in control_dirs):
                raise WorkspaceError(f"control git_dir overlaps another registered project: {project_id}")
            control_dirs.append(git_dir)
            control["git_dir"] = str(git_dir)
        else:
            control = {"mode": mode, "git_dir": None}
        item = deepcopy(item)
        item.update({"project_id": project_id, "project_root": str(root), "planning_root": str(planning), "agents_root": str(agents), "project_status": status, "control_history": control})
        seen_ids.add(project_id)
        seen_roots.add(root)
        normalized.append(item)
    product_roots = [Path(item["project_root"]).resolve() for item in normalized]
    for item in normalized:
        control = item["control_history"]
        git_dir_raw = control.get("git_dir")
        if control.get("mode") != "split-control" or not isinstance(git_dir_raw, str):
            continue
        git_dir = Path(git_dir_raw).resolve()
        if any(
            git_dir.is_relative_to(other_root) or other_root.is_relative_to(git_dir)
            for other_root in product_roots
        ):
            raise WorkspaceError(
                f"control git_dir overlaps a registered product root: {item['project_id']}"
            )
    return {"schema_version": 1, "projects": normalized}


def load_registry(home: str | Path | None = None) -> dict[str, Any]:
    path = registry_path(home)
    if not path.exists():
        return {"schema_version": 1, "projects": []}
    data = _read_yaml(path, "project registry")
    return _validate_registry_shape(data, home=resolve_home(home))


def save_registry(home: str | Path | None, data: Mapping[str, Any]) -> None:
    home_path = resolve_home(home)
    normalized = _validate_registry_shape(data, home=home_path)
    _write_yaml_atomic(registry_path(home_path), normalized)


def _source_path(root: Path, relative: str) -> str:
    return str((root / relative).resolve())


def _find_project(registry: Mapping[str, Any], project_id: str) -> dict[str, Any] | None:
    for item in registry["projects"]:
        if item["project_id"] == project_id:
            return item
    return None


def plan_registration(
    target: str | Path,
    *,
    mode: str,
    status: str,
    home: str | Path | None = None,
    project_id: str | None = None,
    telemetry: bool = False,
) -> dict[str, Any]:
    """Validate registration completely without writing config or registry."""

    if mode not in ALLOWED_MODES:
        raise WorkspaceError(f"Unsupported control history mode: {mode}")
    if status not in ALLOWED_PROJECT_STATUSES:
        raise WorkspaceError(f"Unsupported project status: {status}")
    root = Path(target).expanduser().resolve()
    if not root.is_dir():
        raise WorkspaceError(f"Product root does not exist: {root}")
    effective = load_effective_policy(root)
    policy = effective["project_policy"]
    resolved_id = project_id or policy.get("project_id") or root.name
    if not isinstance(resolved_id, str) or not resolved_id.strip():
        raise WorkspaceError("project_id is required for registration")
    resolved_id = _safe_project_id(resolved_id.strip())
    planning_root = _relative_root(root, policy.get("planning_root", ".planning"), "planning_root")
    agents_root = _relative_root(root, policy.get("agents_root", ".agents"), "agents_root")
    home_path = resolve_home(home)
    git_dir: Path | None = None
    if mode == "split-control":
        git_dir = resolve_control_git_dir(planning_root)
        if git_dir is None:
            raise WorkspaceError("register --mode split-control requires control-init first")
    entry: dict[str, Any] = {
        "project_id": resolved_id,
        "project_root": str(root),
        "planning_root": str(planning_root),
        "agents_root": str(agents_root),
        "control_history": {"mode": mode, "git_dir": str(git_dir) if git_dir else None},
        "project_status": status,
        "installed_ref_source": _source_path(root, ANSWERS_FILENAME),
        "lifecycle_source": str(planning_root / "ACTIVE.md"),
        "recommendation_index_source": str(planning_root / "recommendations" / "INDEX.md"),
        "telemetry": {
            "enabled": bool(telemetry),
            "receipt_path": (
                str(local_route("consumer_state", home_path) / resolved_id / "telemetry" / "run-receipts.jsonl")
                if telemetry
                else None
            ),
        },
    }
    registry = load_registry(home_path)
    existing = _find_project(registry, resolved_id)
    if existing is not None:
        candidate = deepcopy(existing)
        candidate.update(entry)
        if candidate != existing:
            raise WorkspaceError(f"Conflicting registration already exists: {resolved_id}")
        return {
            "entry": existing,
            "registry": registry,
            "already_registered": True,
            "config_path": root / ".planning" / "CONFIG.yml",
            "registry_path": registry_path(home_path),
        }
    for other in registry["projects"]:
        other_root = Path(other["project_root"]).resolve()
        if other_root == root or root.is_relative_to(other_root) or other_root.is_relative_to(root):
            raise WorkspaceError(f"Product root already registered as {other['project_id']}")
    # Validate the complete candidate before mutating project config. This keeps
    # cross-project topology conflicts write-free as well as ID/root conflicts.
    candidate_registry = deepcopy(registry)
    candidate_registry["projects"].append(entry)
    _validate_registry_shape(candidate_registry, home=home_path)
    return {
        "entry": entry,
        "registry": candidate_registry,
        "already_registered": False,
        "config_path": root / ".planning" / "CONFIG.yml",
        "registry_path": registry_path(home_path),
    }


def register_project(
    target: str | Path,
    *,
    mode: str,
    status: str,
    home: str | Path | None = None,
    project_id: str | None = None,
    telemetry: bool = False,
) -> dict[str, Any]:
    """Enroll one product repository and persist only locator metadata."""

    plan = plan_registration(
        target,
        mode=mode,
        status=status,
        home=home,
        project_id=project_id,
        telemetry=telemetry,
    )
    if plan["already_registered"]:
        return plan["entry"]
    entry = plan["entry"]
    # Persist project-owned overrides only after every registry conflict and
    # topology prerequisite has passed, so a rejected repeat is write-free.
    root = Path(target).expanduser().resolve()
    update_project_policy(
        root,
        project_id=entry["project_id"],
        control_history_mode=entry["control_history"]["mode"],
        telemetry_enabled=telemetry,
    )
    save_registry(home, plan["registry"])
    return entry


def inspect_project(target: str | Path, *, home: str | Path | None = None) -> dict[str, Any]:
    root = Path(target).expanduser().resolve()
    registry = load_registry(home)
    entry = next((item for item in registry["projects"] if Path(item["project_root"]).resolve() == root), None)
    if entry is None:
        raise WorkspaceError(f"Project is not registered: {root}")
    result = deepcopy(entry)
    policy = load_effective_policy(root)["project_policy"]
    forbidden = policy.get("forbidden_read_paths", [])
    if not isinstance(forbidden, list) or not all(isinstance(item, str) for item in forbidden):
        raise WorkspaceError("project_policy.forbidden_read_paths must be a list of strings")
    answers = root / ANSWERS_FILENAME
    installed_ref = None
    _guard_product_read(root, answers, forbidden)
    if answers.is_file():
        raw = _read_yaml(answers, "Copier answers")
        if isinstance(raw, dict):
            value = raw.get("_commit") or raw.get("_vcs_ref")
            if isinstance(value, str) and value.strip():
                installed_ref = value.strip()
    result["installed_ref"] = installed_ref
    lifecycle = _guard_product_read(root, entry["lifecycle_source"], forbidden)
    recommendation_index = _guard_product_read(
        root, entry["recommendation_index_source"], forbidden
    )
    result["lifecycle_exists"] = lifecycle.is_file()
    result["recommendation_index_exists"] = recommendation_index.is_file()
    result["product_git"] = _product_git_context(root, tuple(forbidden))
    planning_root = Path(entry["planning_root"]).resolve()
    result["control_git"] = _control_git_context(root, planning_root, tuple(forbidden))
    return result


def registry_json(data: Mapping[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True, ensure_ascii=False)
