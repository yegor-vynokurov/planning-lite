"""Bounded, read-only resume context for an installed Planning Lite project.

The command in this module is deliberately a projection of existing project
state.  It does not create a memory store, scan history, or write the target.
"""

from __future__ import annotations

from hashlib import sha256
import json
import os
from pathlib import Path
import re
import stat
from typing import Any, Iterable, Mapping

from .workspace import (
    WorkspaceError,
    _guard_product_read,
    _product_git_context,
    load_effective_policy,
)


class ContextError(ValueError):
    """A malformed or unsafe bounded context request."""


DEFAULT_MAX_ARTIFACTS = 3
MAX_EXPANSIONS = 5
MAX_TOTAL_ARTIFACTS = 8
CURRENT_STATE_MAX_CHARS = 8192
CURRENT_STATE_MAX_BULLETS = 12
ACTIVE_CONTEXT_MAX_CHARS = 16384
ACTIVE_CONTEXT_MAX_FIELDS = 12
SECTION_MAX_CHARS = 4096

_ACTIVE_FIELDS = (
    "Change",
    "Change status",
    "Lifecycle stage",
    "Stage status",
    "Current task",
    "Last verified checkpoint",
    "Next gate",
    "Next permitted action",
    "Implementation authorized",
    "Active context packet",
)
_REQUIRED_ACTIVE_FIELDS = ("Lifecycle stage", "Implementation authorized", "Next permitted action")
_HANDOFF_KEYS = {
    "schema_version",
    "project_id",
    "change_id",
    "active_context_path",
    "changed_paths",
    "lifecycle_stage",
    "stage_status",
    "implementation_authorized",
    "verification",
    "open_blocker",
    "accepted_dispositions",
    "next_permitted_action",
    "artifact_refs",
    "source_revision",
}
_EXCLUDED = (
    ("completed changes", "not loaded by default"),
    ("full ledgers", "not loaded by default"),
    ("archives", "not loaded by default"),
    ("raw logs", "not loaded by default"),
    ("historical proposals", "not loaded by default"),
)


def _clean(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    text = re.sub(r"^`(.*)`$", r"\1", text)
    if text.lower() in {"none", "null", "n/a", "na", "-"}:
        return None
    return text


def _bool(value: object) -> bool | None:
    value = _clean(value)
    if value is None:
        return None
    if value.lower() in {"yes", "true", "authorized", "allowed"}:
        return True
    if value.lower() in {"no", "false", "not authorized", "denied"}:
        return False
    raise ContextError(f"Implementation authorized has an invalid value: {value!r}")


def _parse_bullets(text: str, *, limit: int | None = None) -> dict[str, str]:
    result: dict[str, str] = {}
    count = 0
    for line in text.splitlines():
        match = re.match(r"^\s*-\s*([^:]+):\s*(.*?)\s*$", line)
        if not match:
            continue
        key, value = match.groups()
        key = key.strip()
        if key not in result:
            result[key] = value
            count += 1
            if limit is not None and count >= limit:
                break
    return result


def _read(path: Path) -> bytes:
    try:
        return path.read_bytes()
    except OSError as exc:
        raise ContextError(f"Cannot read owner artifact: {path}") from exc


def _relative(root: Path, path: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def _has_reparse_component(root: Path, path: Path) -> bool:
    """Reject symlink/junction components before a file is selected."""

    try:
        relative = path.absolute().relative_to(root.absolute())
    except ValueError:
        return True
    current = root
    for component in relative.parts:
        current = current / component
        try:
            info = current.lstat()
        except OSError:
            continue
        if stat.S_ISLNK(info.st_mode):
            return True
        if getattr(info, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
            return True
    return False


def _safe_path(root: Path, candidate: str | Path, forbidden: list[str]) -> tuple[Path, str]:
    raw = str(candidate).replace("\\", "/")
    if isinstance(candidate, Path) and candidate.is_absolute():
        inspected = candidate
        path = candidate.resolve()
        raw = _relative(root, path)
    else:
        if not raw or raw.startswith("/") or re.match(r"^[A-Za-z]:", raw):
            raise ContextError("Selector must be a repository-relative path")
        if any(token in raw for token in ("*", "?", "[", "]")):
            raise ContextError("Glob and pattern selectors are not allowed")
        pieces = Path(raw).parts
        if ".." in pieces:
            raise ContextError("Selector may not traverse parent directories")
        inspected = root / Path(raw)
        path = inspected.resolve()
    try:
        relative = _relative(root, path)
    except ValueError as exc:
        raise ContextError("Selector escapes the product root") from exc
    if relative == ".git" or relative.startswith(".git/"):
        raise ContextError(".git is not an eligible context source")
    if _has_reparse_component(root, inspected):
        raise ContextError(f"Symlink/reparse selectors are not allowed: {relative}")
    try:
        path = _guard_product_read(root, path, forbidden)
    except WorkspaceError as exc:
        raise ContextError(str(exc)) from exc
    return path, relative


def _sha(path: Path) -> str:
    return sha256(_read(path)).hexdigest()


def _source(path: Path, relative: str, *, role: str, reason: str, section: str | None = None) -> dict[str, Any]:
    data = _read(path)
    return {
        "path": relative,
        "sha256": sha256(data).hexdigest(),
        "role": role,
        "storage_class": classify_storage(relative),
        "reason": reason,
        "section": section,
    }


def classify_storage(path: str) -> str:
    """Classify only known path roles; content similarity is never used."""
    normalized = path.replace("\\", "/")
    if normalized.startswith("./"):
        normalized = normalized[2:]
    if normalized in {".planning/ACTIVE.md", ".planning/project/CURRENT_STATE.md"} or normalized.startswith(".planning/changes/active/"):
        return "TRACKED_CANONICAL"
    if normalized.startswith("recommendations/inbox/"):
        return "LOCAL_OPERATIONAL"
    if normalized.startswith(".planning/changes/completed/") or normalized.startswith(".planning/decisions/") or "ledger" in Path(normalized).name.lower() or normalized.endswith("review.md"):
        return "TRACKED_EVIDENCE_HISTORY"
    return "RECONSTRUCTABLE"


def validate_handoff(payload: object, *, current: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Validate the exact in-memory HandoffV1 contract and return a copy."""
    if not isinstance(payload, dict):
        raise ContextError("HandoffV1 must be a JSON object")
    unknown = set(payload) - _HANDOFF_KEYS
    missing = _HANDOFF_KEYS - set(payload)
    if unknown:
        raise ContextError(f"HandoffV1 has unknown keys: {sorted(unknown)}")
    if missing:
        raise ContextError(f"HandoffV1 is missing keys: {sorted(missing)}")
    if payload["schema_version"] != 1:
        raise ContextError("HandoffV1 schema_version must be 1")
    if not isinstance(payload["project_id"], (str, type(None))):
        raise ContextError("HandoffV1 project_id must be a string or null")
    if not isinstance(payload["change_id"], (str, type(None))):
        raise ContextError("HandoffV1 change_id must be a string or null")
    if not isinstance(payload["active_context_path"], (str, type(None))):
        raise ContextError("HandoffV1 active_context_path must be a string or null")
    paths = payload["changed_paths"]
    if not isinstance(paths, list) or len(paths) > 64:
        raise ContextError("HandoffV1 changed_paths must contain at most 64 non-empty strings")
    normalized_paths = [_normalize_handoff_path(item, "changed_paths") for item in paths]
    if not isinstance(payload["lifecycle_stage"], str) or not isinstance(payload["stage_status"], str):
        raise ContextError("HandoffV1 lifecycle fields must be strings")
    if not isinstance(payload["implementation_authorized"], bool):
        raise ContextError("HandoffV1 implementation_authorized must be boolean")
    if not isinstance(payload["next_permitted_action"], str):
        raise ContextError("HandoffV1 next_permitted_action must be a string")
    if not isinstance(payload["open_blocker"], (str, type(None))):
        raise ContextError("HandoffV1 open_blocker must be a string or null")
    verification = payload["verification"]
    if not isinstance(verification, list) or len(verification) > 32:
        raise ContextError("HandoffV1 verification must contain at most 32 entries")
    for item in verification:
        if not isinstance(item, dict) or set(item) != {"command", "outcome", "evidence_pointer"}:
            raise ContextError("HandoffV1 verification entries have an exact schema")
        if not isinstance(item["command"], str) or not isinstance(item["outcome"], str) or not isinstance(item["evidence_pointer"], (str, type(None))):
            raise ContextError("HandoffV1 verification values have an exact schema")
    dispositions = payload["accepted_dispositions"]
    if not isinstance(dispositions, list) or len(dispositions) > 16:
        raise ContextError("HandoffV1 accepted_dispositions must contain at most 16 entries")
    for item in dispositions:
        if not isinstance(item, dict) or set(item) != {"id", "disposition", "artifact_pointer"}:
            raise ContextError("HandoffV1 disposition entries have an exact schema")
        if not isinstance(item["id"], str) or not isinstance(item["disposition"], str) or not isinstance(item["artifact_pointer"], (str, type(None))):
            raise ContextError("HandoffV1 disposition values have an exact schema")
    refs = payload["artifact_refs"]
    if not isinstance(refs, list) or len(refs) > 16:
        raise ContextError("HandoffV1 artifact_refs must contain at most 16 entries")
    for item in refs:
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            raise ContextError("HandoffV1 artifact_refs entries have an exact schema")
        if not isinstance(item["sha256"], str) or not re.fullmatch(r"[0-9a-fA-F]{64}", item["sha256"]):
            raise ContextError("HandoffV1 artifact_refs values must be strings")
    source = payload["source_revision"]
    if not isinstance(source, dict) or set(source) != {"head", "state"}:
        raise ContextError("HandoffV1 source_revision has an exact schema")
    if not isinstance(source["head"], (str, type(None))) or not isinstance(source["state"], str):
        raise ContextError("HandoffV1 source_revision values are invalid")
    if current:
        if payload["project_id"] != current.get("project_id"):
            raise ContextError("HandoffV1 project identity conflicts with current authority")
        if payload["change_id"] != current.get("active_change"):
            raise ContextError("HandoffV1 active Change conflicts with current authority")
        if bool(payload["implementation_authorized"]) != bool(current.get("implementation_authorized")):
            raise ContextError("HandoffV1 cannot elevate or revoke current authorization")
    normalized = json.loads(json.dumps(payload, sort_keys=True))
    normalized["active_context_path"] = (
        None
        if normalized["active_context_path"] is None
        else _normalize_handoff_path(normalized["active_context_path"], "active_context_path")
    )
    normalized["changed_paths"] = normalized_paths
    normalized["artifact_refs"] = [
        {**item, "path": _normalize_handoff_path(item["path"], "artifact_refs.path")}
        for item in normalized["artifact_refs"]
    ]
    return normalized


def _active_state(text: str) -> tuple[dict[str, Any], str | None]:
    fields = _parse_bullets(text)
    for required in _REQUIRED_ACTIVE_FIELDS:
        if required not in fields:
            raise ContextError("MISSING_REQUIRED_CURRENT_STATE")
    state: dict[str, Any] = {key.lower().replace(" ", "_"): _clean(fields.get(key)) for key in _ACTIVE_FIELDS}
    state["implementation_authorized"] = _bool(fields.get("Implementation authorized"))
    blocker_match = re.search(r"(?ms)^##\s+Blocking decision\s*\n(.*?)(?=^##\s+|\Z)", text)
    blocker_text = blocker_match.group(1) if blocker_match else ""
    blocker_fields = _parse_bullets(blocker_text, limit=1)
    blocker_value = next(iter(blocker_fields.values()), None)
    if blocker_value is None:
        raw_bullet = re.search(r"(?m)^\s*-\s+(.+?)\s*$", blocker_text)
        blocker_value = raw_bullet.group(1) if raw_bullet else None
    state["open_blocker"] = _clean(blocker_value)
    return state, _clean(fields.get("Active context packet"))


def _current_state(text: str) -> dict[str, Any]:
    preamble = re.split(r"(?m)^##\s+", text, maxsplit=1)[0]
    if len(preamble) > CURRENT_STATE_MAX_CHARS:
        preamble = preamble[:CURRENT_STATE_MAX_CHARS]
    return {
        key.lower().replace(" ", "_"): _clean(value)
        for key, value in _parse_bullets(preamble, limit=CURRENT_STATE_MAX_BULLETS).items()
    }


def _context_fields(text: str) -> dict[str, str]:
    fields = _parse_bullets(text, limit=ACTIVE_CONTEXT_MAX_FIELDS)
    if sum(len(k) + len(v) for k, v in fields.items()) > ACTIVE_CONTEXT_MAX_CHARS:
        raise ContextError("ACTIVE_CONTEXT_TOO_LARGE")
    return fields


def _heading_section(text: str, heading: str) -> str:
    wanted = heading.strip()
    if not wanted or any(char in wanted for char in "\r\n#"):
        raise ContextError("Heading selector must be exact")
    pattern = re.compile(r"(?m)^(#{1,6})\s+(.+?)\s*$")
    matches = list(pattern.finditer(text))
    selected = next((m for m in matches if m.group(2).strip() == wanted), None)
    if selected is None:
        raise ContextError(f"Heading not found: {wanted}")
    level = len(selected.group(1))
    end = len(text)
    for match in matches:
        if match.start() > selected.start() and len(match.group(1)) <= level:
            end = match.start()
            break
    content = text[selected.end():end].lstrip("\r\n")
    return content


def _include_spec(spec: str) -> tuple[str, str | None]:
    if "#" in spec:
        path, heading = spec.split("#", 1)
        if not path or not heading:
            raise ContextError("--include requires PATH or PATH#HEADING")
        return path, heading
    return spec, None


def _normalize_handoff_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContextError(f"HandoffV1 {label} must be a non-empty relative path")
    normalized = value.strip().replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise ContextError(f"HandoffV1 {label} must be repository-relative")
    if ".." in Path(normalized).parts or normalized == ".git" or normalized.startswith(".git/"):
        raise ContextError(f"HandoffV1 {label} is outside the eligible root")
    return normalized


_STATUS_RANK = {
    "CURRENT": 0,
    "STALE": 1,
    "SUPERSEDED": 2,
    "MISSING_OWNER_ARTIFACT": 3,
}


def _promote_status(current: str, candidate: str) -> str:
    return candidate if _STATUS_RANK[candidate] > _STATUS_RANK[current] else current


def build_resume_context(
    target: str | Path,
    *,
    include: Iterable[str] = (),
    handoff: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic bounded resume view without writing anything."""
    root = Path(target).expanduser().resolve()
    try:
        effective = load_effective_policy(root)
        policy = effective["project_policy"]
        forbidden = policy.get("forbidden_read_paths", [])
        planning = (root / policy.get("planning_root", ".planning")).resolve()
        _guard_product_read(root, planning, forbidden)
    except (WorkspaceError, KeyError) as exc:
        raise ContextError(str(exc)) from exc
    if not isinstance(forbidden, list):
        raise ContextError("project_policy.forbidden_read_paths must be a list")

    project_id = policy.get("project_id") or root.name
    active_path, active_relative = _safe_path(root, planning / "ACTIVE.md", forbidden)
    active_exists = active_path.is_file()
    sources: list[dict[str, Any]] = []
    active: dict[str, Any] = {}
    context_pointer: str | None = None
    status = "CURRENT"
    if not active_exists:
        status = "MISSING_OWNER_ARTIFACT"
    else:
        active_text = _read(active_path).decode("utf-8")
        try:
            active, context_pointer = _active_state(active_text)
        except UnicodeDecodeError as exc:
            raise ContextError("ACTIVE.md is not UTF-8") from exc
        sources.append(_source(active_path, active_relative, role="active_state", reason="authority identity and exact pointers"))

    current_path, current_relative = _safe_path(root, planning / "project" / "CURRENT_STATE.md", forbidden)
    current_data: dict[str, Any] = {}
    if current_path.is_file():
        try:
            current_data = _current_state(_read(current_path).decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise ContextError("CURRENT_STATE.md is not UTF-8") from exc
        sources.append(_source(current_path, current_relative, role="current_state", reason="ACTIVE compact current state"))
    else:
        status = "MISSING_OWNER_ARTIFACT"

    active_change = active.get("change")
    context_path: Path | None = None
    context_relative: str | None = None
    if active_change and context_pointer:
        context_raw = context_pointer
        if context_raw.startswith(".planning/"):
            context_path, context_relative = _safe_path(root, context_raw, forbidden)
        else:
            context_path, context_relative = _safe_path(root, planning / context_raw, forbidden)
        if context_path.is_file():
            try:
                context_data = _context_fields(_read(context_path).decode("utf-8"))
            except UnicodeDecodeError as exc:
                raise ContextError("active context packet is not UTF-8") from exc
            sources.append(_source(context_path, context_relative, role="active_context", reason="active context packet fields"))
        else:
            status = "MISSING_OWNER_ARTIFACT"

    requested = list(include)
    if len(requested) > MAX_EXPANSIONS:
        raise ContextError("At most five explicit expansions are allowed")
    if len(sources) + len(requested) > MAX_TOTAL_ARTIFACTS:
        raise ContextError("Total selected artifacts may not exceed eight")
    selected_sections = 0
    selected_chars = 0
    expansion_results: list[dict[str, Any]] = []
    for source in sources:
        source_path, _ = _safe_path(root, source["path"], forbidden)
        source_text = _read(source_path).decode("utf-8")
        selected_chars += len(
            _heading_section(source_text, source["section"])
            if source["section"]
            else source_text
        )
    for spec in requested:
        raw_path, heading = _include_spec(spec)
        if raw_path.replace("\\", "/").startswith("recommendations/inbox/"):
            raise ContextError("recommendations/inbox is local operational input and cannot be selected")
        path, relative = _safe_path(root, raw_path, forbidden)
        if not (
            relative.startswith(".planning/project/")
            or relative.startswith(".planning/changes/active/")
            or relative.startswith(".planning/changes/completed/")
            or relative.startswith(".planning/decisions/")
        ):
            raise ContextError("Explicit expansions must target an eligible Planning Lite artifact")
        if not path.is_file():
            status = "MISSING_OWNER_ARTIFACT"
            continue
        data = _read(path).decode("utf-8")
        if heading is not None:
            section = _heading_section(data, heading)
            if len(section) > SECTION_MAX_CHARS:
                expansion_results.append(
                    {
                        "status": "EXPANSION_TOO_LARGE",
                        "path": relative,
                        "section": heading,
                        "limit_chars": SECTION_MAX_CHARS,
                    }
                )
                continue
            selected_sections += 1
        sources.append(_source(path, relative, role="explicit_expansion", reason="explicit exact lineage expansion", section=heading))
        selected_chars += len(data if heading is None else _heading_section(data, heading))

    git = _product_git_context(root, forbidden)
    head = git.get("head")
    if git.get("available") and not head:
        head = "UNBORN"
    branch_probe = None
    if git.get("available"):
        from .workspace import product_git

        branch_result = product_git(root, "symbolic-ref", "--short", "-q", "HEAD")
        branch_probe = branch_result.stdout.strip() if branch_result.returncode == 0 else "DETACHED"
    git_identity = {
        "head": head,
        "branch": branch_probe,
        "clean": git.get("clean"),
        "state": "UNAVAILABLE" if not git.get("available") else ("UNBORN" if head == "UNBORN" else "AVAILABLE"),
    }
    current_tuple = (
        active.get("change"),
        active.get("lifecycle_stage"),
        active.get("stage_status"),
        active.get("implementation_authorized"),
        active.get("next_permitted_action"),
        context_relative,
    )
    bootstrap = {
        "project_id": project_id,
        "active_change": active.get("change"),
        "last_completed_or_next_pointer": active.get("last_verified_checkpoint"),
        "lifecycle_stage": active.get("lifecycle_stage"),
        "stage_status": active.get("stage_status"),
        "implementation_authorized": active.get("implementation_authorized"),
        "open_blocker": active.get("open_blocker"),
        "next_permitted_action": active.get("next_permitted_action"),
        "active_context_path": context_relative,
        "source_revision": head,
    }
    normalized_handoff = None
    if handoff is not None:
        normalized_handoff = validate_handoff(handoff, current={**bootstrap, "project_id": project_id})
        if (
            normalized_handoff["active_context_path"] != bootstrap["active_context_path"]
            or
            normalized_handoff["lifecycle_stage"] != bootstrap["lifecycle_stage"]
            or normalized_handoff["stage_status"] != bootstrap["stage_status"]
            or normalized_handoff["next_permitted_action"] != bootstrap["next_permitted_action"]
            or normalized_handoff["open_blocker"] != bootstrap["open_blocker"]
        ):
            status = _promote_status(status, "SUPERSEDED")
        refs = normalized_handoff["artifact_refs"]
        for ref in refs:
            path, relative = _safe_path(root, ref["path"], forbidden)
            if not path.is_file():
                status = _promote_status(status, "MISSING_OWNER_ARTIFACT")
            elif _sha(path) != ref["sha256"]:
                status = _promote_status(status, "STALE")
        if normalized_handoff["source_revision"]["head"] not in {None, head}:
            status = _promote_status(status, "STALE")
    trace = {
        "selected": sources,
        "excluded_by_default": [{"category": category, "reason": reason} for category, reason in _EXCLUDED],
        "selected_artifact_count": len(sources),
        "selected_section_count": selected_sections,
        "selected_character_count": selected_chars,
        "explicit_expansion_count": len(requested),
        "bounds": {
            "default_artifacts": DEFAULT_MAX_ARTIFACTS,
            "explicit_expansions": MAX_EXPANSIONS,
            "total_artifacts": MAX_TOTAL_ARTIFACTS,
            "current_state_chars": CURRENT_STATE_MAX_CHARS,
            "active_context_chars": ACTIVE_CONTEXT_MAX_CHARS,
            "section_chars": SECTION_MAX_CHARS,
        },
    }
    return {
        "schema_version": 1,
        "status": status,
        "project_identity": {"project_id": project_id, "root": str(root)},
        "git_identity": git_identity,
        "current_state": {**current_data, "active_tuple": current_tuple},
        "bootstrap": bootstrap,
        "selected_sources": sources,
        "handoff": normalized_handoff,
        "expansion_results": expansion_results,
        "context_trace": trace,
    }


validate_resume_context = build_resume_context
resume_context = build_resume_context


__all__ = [
    "ContextError",
    "build_resume_context",
    "classify_storage",
    "resume_context",
    "validate_handoff",
    "validate_resume_context",
]
