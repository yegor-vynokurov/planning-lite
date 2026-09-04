from __future__ import annotations

from dataclasses import dataclass
from fnmatch import fnmatchcase
import hashlib
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from typing import Iterable, Literal

import yaml

ANSWERS_FILE = ".copier-answers.planning-lite.yml"
OWNERSHIP_FILE = ".planning/framework/OWNERSHIP.yml"
TOPOLOGY_METADATA = {".planning/.git", ".planning/.gitignore"}

OwnershipClass = Literal["managed", "project_owned", "installer_metadata", "unknown"]
Action = Literal[
    "ADD_MANAGED",
    "UPDATE_MANAGED",
    "REMOVE_MANAGED",
    "ADD_PROJECT",
    "KEEP_PROJECT",
    "UPDATE_METADATA",
    "KEEP_METADATA",
    "UNCHANGED_MANAGED",
]


@dataclass(frozen=True)
class OwnershipPolicy:
    managed: tuple[str, ...]
    project_owned: tuple[str, ...]
    installer_metadata: tuple[str, ...]


@dataclass(frozen=True)
class Mutation:
    action: Action
    path: str


@dataclass(frozen=True)
class LocalUpdatePlan:
    mutations: tuple[Mutation, ...]

    def changed(self) -> tuple[Mutation, ...]:
        return tuple(
            item
            for item in self.mutations
            if item.action
            not in {"KEEP_PROJECT", "KEEP_METADATA", "UNCHANGED_MANAGED"}
        )

    def count(self, action: Action) -> int:
        return sum(1 for item in self.mutations if item.action == action)


class LocalUpdateError(RuntimeError):
    """Fail-closed local-only update planning/apply failure."""


def _normalize(path: str | Path) -> str:
    normalized = str(path).replace("\\", "/")
    while normalized.startswith("./"):
        normalized = normalized[2:]
    return normalized


def _pattern_specificity(pattern: str) -> tuple[int, int, int]:
    """Prefer exact paths, then fewer wildcards, then longer patterns."""
    wildcard_count = pattern.count("*") + pattern.count("?") + pattern.count("[")
    exact = 1 if wildcard_count == 0 else 0
    return (exact, -wildcard_count, len(pattern))


def _best_match(path: str, patterns: Iterable[str]) -> str | None:
    matches = [pattern for pattern in patterns if fnmatchcase(path, pattern)]
    if not matches:
        return None
    return max(matches, key=_pattern_specificity)


def load_ownership_policy(root: Path) -> OwnershipPolicy:
    path = root / OWNERSHIP_FILE
    if not path.exists():
        raise LocalUpdateError(f"Ownership manifest not found: {path}")
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise LocalUpdateError(f"Cannot parse ownership manifest {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise LocalUpdateError(f"Ownership manifest is not a mapping: {path}")

    values: dict[str, tuple[str, ...]] = {}
    for key in ("managed", "project_owned", "installer_metadata"):
        raw = data.get(key)
        if not isinstance(raw, list) or not all(isinstance(item, str) for item in raw):
            raise LocalUpdateError(f"Ownership manifest field `{key}` must be a list of paths")
        values[key] = tuple(raw)
    return OwnershipPolicy(**values)


def classify_path(path: str, policy: OwnershipPolicy) -> OwnershipClass:
    normalized = _normalize(path)
    matches = {
        "managed": _best_match(normalized, policy.managed),
        "project_owned": _best_match(normalized, policy.project_owned),
        "installer_metadata": _best_match(normalized, policy.installer_metadata),
    }
    present = {key: value for key, value in matches.items() if value is not None}
    if not present:
        return "unknown"
    if len(present) == 1:
        return next(iter(present))  # type: ignore[return-value]

    # Installer metadata is always installer-owned when explicitly listed.
    if present.get("installer_metadata") is not None:
        return "installer_metadata"

    # Exact framework files beat broad project-owned globs. This allows a
    # reserved TEMPLATE.md to live inside an otherwise project-owned runtime dir.
    managed = present.get("managed")
    project = present.get("project_owned")
    if managed is not None and project is not None:
        if _pattern_specificity(managed) > _pattern_specificity(project):
            return "managed"
        if _pattern_specificity(project) > _pattern_specificity(managed):
            return "project_owned"

    raise LocalUpdateError(
        f"Ambiguous ownership for `{normalized}`: "
        + ", ".join(f"{key}={value}" for key, value in sorted(present.items()))
    )


def _forbidden_read(root: Path, relative: str, patterns: Iterable[str]) -> bool:
    relative = _normalize(relative)
    absolute = _normalize(root / relative)
    for raw in patterns:
        pattern = _normalize(raw).rstrip("/")
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


def _is_link_or_reparse(path: Path) -> bool:
    """Detect links and Windows reparse directories without new dependencies."""

    try:
        if path.is_symlink():
            return True
        isjunction = getattr(os.path, "isjunction", None)
        if callable(isjunction) and isjunction(path):
            return True
        if os.name == "nt":
            return bool(getattr(path.lstat(), "st_reparse_tag", 0))
    except (OSError, RuntimeError) as exc:
        raise LocalUpdateError(f"Cannot inspect symlink/reparse path: {path}") from exc
    return False


def _check_link_containment(root: Path, path: Path, relative: str) -> bool:
    if not _is_link_or_reparse(path):
        return False
    try:
        path.resolve().relative_to(root)
    except (OSError, RuntimeError, ValueError) as exc:
        raise LocalUpdateError(f"Symlink/reparse path escapes update root: {relative}") from exc
    return True


def iter_files(root: Path, *, forbidden_read_paths: Iterable[str] = ()) -> dict[str, Path]:
    """Walk bounded files, pruning Git metadata before entering it."""

    root = root.resolve()
    patterns = tuple(forbidden_read_paths)
    files: dict[str, Path] = {}
    for current, dirnames, filenames in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        kept_dirs: list[str] = []
        for name in sorted(dirnames):
            child = current_path / name
            relative = child.relative_to(root).as_posix()
            is_link_or_reparse = _check_link_containment(root, child, relative)
            if name == ".git":
                continue
            if is_link_or_reparse:
                # Do not follow symlink/reparse directories, even when they
                # resolve inside the root; bounded scans remain deterministic.
                continue
            if _forbidden_read(root, relative, patterns):
                raise LocalUpdateError(f"Forbidden read path intersects scan: {relative}")
            kept_dirs.append(name)
        dirnames[:] = kept_dirs
        for name in sorted(filenames):
            path = current_path / name
            relative = path.relative_to(root).as_posix()
            parts = relative.split("/")
            if ".git" in parts or relative in TOPOLOGY_METADATA:
                continue
            if _forbidden_read(root, relative, patterns):
                raise LocalUpdateError(f"Forbidden read path intersects scan: {relative}")
            if _check_link_containment(root, path, relative):
                # Do not read link/reparse files through an alternate path.
                continue
            if path.is_file():
                files[relative] = path
    return files


def _same_bytes(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    return hashlib.sha256(left.read_bytes()).digest() == hashlib.sha256(right.read_bytes()).digest()


def _same_installer_metadata(left: Path, right: Path) -> bool:
    """Treat equivalent Copier answers formatting/path separators as unchanged."""

    if _same_bytes(left, right):
        return True
    try:
        old = yaml.safe_load(left.read_text(encoding="utf-8"))
        new = yaml.safe_load(right.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError):
        return False
    if not isinstance(old, dict) or not isinstance(new, dict):
        return False
    for data in (old, new):
        source = data.get("_src_path")
        if isinstance(source, str):
            data["_src_path"] = source.replace("\\", "/")
    # Copier materializes a dirty local source through an ephemeral commit;
    # its pseudo-ref changes on every render even when the rendered bytes do
    # not.  Do not turn that non-semantic identity churn into UPDATE_METADATA.
    if old == new:
        return True
    old_ref = old.get("_commit")
    new_ref = new.get("_commit")
    source = old.get("_src_path")
    if (
        isinstance(source, str)
        and isinstance(old_ref, str)
        and isinstance(new_ref, str)
        and re.search(r"-[0-9]+-g[0-9a-f]+$", old_ref)
        and re.search(r"-[0-9]+-g[0-9a-f]+$", new_ref)
        and _local_source_is_dirty(source)
    ):
        old["_commit"] = new["_commit"]
    return old == new


def _local_source_is_dirty(source: str) -> bool:
    parsed = Path(source).expanduser()
    if not parsed.is_dir() or not (parsed / ".git").exists():
        return False
    result = subprocess.run(
        ["git", "-C", str(parsed), "status", "--porcelain"],
        check=False,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0 and bool(result.stdout.strip())


def _classify_candidate(
    candidate_files: dict[str, Path],
    policy: OwnershipPolicy,
) -> dict[str, OwnershipClass]:
    classified: dict[str, OwnershipClass] = {}
    unknown: list[str] = []
    for relative in sorted(candidate_files):
        ownership = classify_path(relative, policy)
        classified[relative] = ownership
        if ownership == "unknown":
            unknown.append(relative)
    if unknown:
        raise LocalUpdateError(
            "Candidate template contains unclassified files; update stopped:\n"
            + "\n".join(f"- {path}" for path in unknown)
        )
    return classified


def build_local_update_plan(
    target: Path, candidate: Path, *, forbidden_read_paths: Iterable[str] = ()
) -> LocalUpdatePlan:
    target = target.resolve()
    candidate = candidate.resolve()
    patterns = tuple(forbidden_read_paths)
    for root in (target, candidate):
        if _forbidden_read(root, OWNERSHIP_FILE, patterns):
            raise LocalUpdateError(f"Forbidden read path intersects scan: {OWNERSHIP_FILE}")
    old_policy = load_ownership_policy(target)
    new_policy = load_ownership_policy(candidate)
    target_files = iter_files(target, forbidden_read_paths=patterns)
    candidate_files = iter_files(candidate, forbidden_read_paths=patterns)
    candidate_classes = _classify_candidate(candidate_files, new_policy)

    mutations: list[Mutation] = []

    # Candidate-driven writes/preservation.
    for relative in sorted(candidate_files):
        ownership = candidate_classes[relative]
        source = candidate_files[relative]
        destination = target / relative
        exists = destination.is_file()

        if ownership == "managed":
            if exists:
                old_class = classify_path(relative, old_policy)
                if old_class == "project_owned":
                    raise LocalUpdateError(
                        f"Unsafe ownership transition for `{relative}`: "
                        "project_owned -> managed. Reconcile ownership explicitly before updating."
                    )
                if old_class == "unknown" and not _same_bytes(destination, source):
                    raise LocalUpdateError(
                        f"Unsafe ownership transition for `{relative}`: unknown -> managed with "
                        "different bytes. Reconcile ownership explicitly before updating."
                    )
            if not exists:
                mutations.append(Mutation("ADD_MANAGED", relative))
            elif _same_bytes(destination, source):
                mutations.append(Mutation("UNCHANGED_MANAGED", relative))
            else:
                mutations.append(Mutation("UPDATE_MANAGED", relative))
        elif ownership == "project_owned":
            mutations.append(Mutation("KEEP_PROJECT" if exists else "ADD_PROJECT", relative))
        elif ownership == "installer_metadata":
            if exists and _same_installer_metadata(destination, source):
                mutations.append(Mutation("KEEP_METADATA", relative))
            else:
                mutations.append(Mutation("UPDATE_METADATA", relative))
        else:  # pragma: no cover - guarded above
            raise LocalUpdateError(f"Unknown candidate ownership: {relative}")

    # Files that were managed by the previous framework and intentionally no
    # longer exist in the new candidate may be removed. Unknown/project-owned
    # extras are never deleted by this updater.
    candidate_paths = set(candidate_files)
    for relative, path in sorted(target_files.items()):
        if relative in candidate_paths:
            continue
        old_class = classify_path(relative, old_policy)
        if old_class != "managed":
            continue
        new_class = classify_path(relative, new_policy)
        if new_class == "project_owned":
            continue
        if path.is_file():
            mutations.append(Mutation("REMOVE_MANAGED", relative))

    mutations.sort(key=lambda item: (item.path, item.action))
    return LocalUpdatePlan(tuple(mutations))


def _project_owned_hashes(
    target: Path, policy: OwnershipPolicy, *, forbidden_read_paths: Iterable[str] = ()
) -> dict[str, str]:
    result: dict[str, str] = {}
    for relative, path in iter_files(target, forbidden_read_paths=forbidden_read_paths).items():
        if classify_path(relative, policy) == "project_owned":
            result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def _verify_applied_plan(target: Path, candidate: Path, plan: LocalUpdatePlan) -> None:
    for mutation in plan.mutations:
        destination = target / mutation.path
        source = candidate / mutation.path
        if mutation.action in {"ADD_MANAGED", "UPDATE_MANAGED", "UPDATE_METADATA", "ADD_PROJECT"}:
            if not destination.is_file() or not _same_bytes(destination, source):
                raise LocalUpdateError(f"Post-apply verification failed for {mutation.path}")
        elif mutation.action == "REMOVE_MANAGED" and destination.exists():
            raise LocalUpdateError(f"Removed managed path still exists: {mutation.path}")


def apply_local_update_plan(
    target: Path,
    candidate: Path,
    plan: LocalUpdatePlan,
    *,
    forbidden_read_paths: Iterable[str] = (),
) -> None:
    target = target.resolve()
    candidate = candidate.resolve()
    patterns = tuple(forbidden_read_paths)
    for root in (target, candidate):
        if _forbidden_read(root, OWNERSHIP_FILE, patterns):
            raise LocalUpdateError(f"Forbidden read path intersects scan: {OWNERSHIP_FILE}")
    new_policy = load_ownership_policy(candidate)
    before_project = _project_owned_hashes(
        target, new_policy, forbidden_read_paths=patterns
    )
    changed = plan.changed()

    with tempfile.TemporaryDirectory(prefix="planning-lite-local-update-backup-") as temporary:
        backup = Path(temporary)
        existed: set[str] = set()
        touched: set[str] = set()
        try:
            for mutation in changed:
                destination = target / mutation.path
                source = candidate / mutation.path
                touched.add(mutation.path)
                if destination.is_file():
                    existed.add(mutation.path)
                    backup_path = backup / mutation.path
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(destination, backup_path)

                if mutation.action == "REMOVE_MANAGED":
                    if destination.exists():
                        destination.unlink()
                    continue

                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, destination)

            _verify_applied_plan(target, candidate, plan)
            after_project = _project_owned_hashes(
                target, new_policy, forbidden_read_paths=patterns
            )
            for relative, digest in before_project.items():
                if after_project.get(relative) != digest:
                    raise LocalUpdateError(
                        f"Project-owned file changed during local-only update: {relative}"
                    )
        except Exception as exc:
            # Roll back every planned mutation before surfacing the failure.
            for relative in sorted(touched, reverse=True):
                destination = target / relative
                backup_path = backup / relative
                if relative in existed:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_path, destination)
                elif destination.exists():
                    destination.unlink()
            if isinstance(exc, LocalUpdateError):
                raise
            raise LocalUpdateError(f"Local-only update failed and was rolled back: {exc}") from exc


def format_local_update_plan(plan: LocalUpdatePlan) -> str:
    visible = [item for item in plan.mutations if item.action != "UNCHANGED_MANAGED"]
    lines = ["Planning Lite local-only update plan:"]
    for item in visible:
        lines.append(f"{item.action:<18} {item.path}")
    lines.append("")
    lines.append("Summary:")
    for action in (
        "ADD_MANAGED",
        "UPDATE_MANAGED",
        "REMOVE_MANAGED",
        "ADD_PROJECT",
        "KEEP_PROJECT",
        "UPDATE_METADATA",
        "KEEP_METADATA",
        "UNCHANGED_MANAGED",
    ):
        lines.append(f"  {action:<18} {plan.count(action)}")
    return "\n".join(lines)
