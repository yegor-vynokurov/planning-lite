"""Bounded, read-only resume context for an installed Planning Lite project.

The command in this module is deliberately a projection of existing project
state.  It does not create a memory store, scan history, or write the target.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import stat
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from .workspace import (
    WorkspaceError,
    _guard_product_read,
    _product_git_context,
    load_effective_policy,
)


def _compact_unavailable(reason: str) -> dict[str, str]:
    return {"status": "DISPLAY_UNAVAILABLE", "reason": reason}


def build_compact_status(
    target: str | Path,
    *,
    attempt_id: str | None = None,
    include: Iterable[str] = (),
) -> dict[str, Any]:
    """Project exactly six read-only owner-language status fields.

    This is a projection over existing resume and Attempt Runtime producers.
    It does not choose an action, create a receipt, or persist status.
    """

    root = Path(target).expanduser().resolve()
    try:
        resume = build_resume_context(root, include=include)
        project = resume["project_identity"]
        bootstrap = resume["bootstrap"]
        where_we_are = {
            "status": resume["status"],
            "project_id": project["project_id"],
            "active_change": bootstrap["active_change"],
            "lifecycle_stage": bootstrap["lifecycle_stage"],
            "stage_status": bootstrap["stage_status"],
        }
        where_we_are_ok = all(value is not None for value in where_we_are.values())
    except (ContextError, KeyError, TypeError):
        resume = None
        bootstrap = None
        where_we_are = _compact_unavailable("RESUME_SOURCE_UNAVAILABLE")
        where_we_are_ok = False

    what_is_done: object = _compact_unavailable("ATTEMPT_RUNTIME_UNAVAILABLE")
    what_is_current: object = _compact_unavailable("ATTEMPT_RUNTIME_UNAVAILABLE")
    state: object = _compact_unavailable("STATUS_SOURCE_UNAVAILABLE")
    try:
        from .attempt_runtime import load_attempt_store, lookup_attempt, check_activation_admissibility

        store = load_attempt_store(root)
        terminal_rows = [row for row in store.attempts if row.runtime_state == "TERMINAL"]
        if len(terminal_rows) == 1 and terminal_rows[0].observed_result is not None:
            row = terminal_rows[0]
            observed = row.observed_result
            what_is_done = {
                "runtime_state": row.runtime_state,
                "attempt_id": row.attempt.attempt_id,
                "result_id": observed.result_id,
                "execution_status": observed.execution_status,
                "fact_refs": list(observed.fact_refs),
                "artifact_refs": list(observed.artifact_refs),
                "verifier_contract_refs": [list(ref) for ref in row.attempt.verifier_contract_refs],
            }
        if attempt_id is not None:
            current_lookup = lookup_attempt(root, attempt_id)
            current_admissibility = check_activation_admissibility(root, attempt_id)
            if current_lookup.attempt is not None and bootstrap is not None:
                current = current_lookup.attempt
                what_is_current = {
                    "status": resume["status"],
                    "active_change": bootstrap["active_change"],
                    "lifecycle_stage": bootstrap["lifecycle_stage"],
                    "stage_status": bootstrap["stage_status"],
                    "active_context_path": bootstrap["active_context_path"],
                    "runtime_state": current_admissibility.envelope.runtime_state
                    if current_admissibility.envelope is not None
                    else "DISPLAY_UNAVAILABLE",
                    "task_or_operation_id": current.task_or_operation_id,
                    "operation_guidance_ref": current.operation_guidance_ref,
                    "execution_invocation_id": "DISPLAY_UNAVAILABLE",
                }
        if bootstrap is not None:
            state = {
                "status": resume["status"],
                "implementation_authorized": bootstrap["implementation_authorized"],
                "runtime_state": (
                    current_admissibility.envelope.runtime_state
                    if attempt_id is not None and current_admissibility.envelope is not None
                    else "DISPLAY_UNAVAILABLE"
                ),
            }
    except Exception:
        # A compact status must mark an unavailable owner source, never invent
        # a terminal or invocation fact from partial data.
        pass

    resources: object = _compact_unavailable("OBSERVED_CONTEXT_UNAVAILABLE")
    try:
        observed_context = build_observed_resume_context(root, include=include)
        observation = OperationDepthObservationV1.from_produced_context(observed_context)
        resources = observation.to_dict()
    except Exception:
        pass

    return {
        "where_we_are": where_we_are if where_we_are_ok else _compact_unavailable("RESUME_SOURCE_UNAVAILABLE"),
        "what_is_done": what_is_done,
        "what_is_current": what_is_current,
        "what_next": (
            bootstrap["next_permitted_action"]
            if isinstance(bootstrap, Mapping) and isinstance(bootstrap.get("next_permitted_action"), str)
            else "DISPLAY_UNAVAILABLE"
        ),
        "resources": resources,
        "state": state,
    }


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

_DEPTH_RAW_KEYS = frozenset(
    {
        "body",
        "content",
        "prompt",
        "response",
        "transcript",
        "tool_payload",
        "tool_body",
        "reasoning",
        "hidden_reasoning",
    }
)
_DEPTH_REASON_CODES = frozenset(
    {
        "INVALID_START_CONTEXT",
        "NO_APPROVED_SEAM",
        "STALE_SOURCE",
        "SUPERSEDED_SOURCE",
        "MISSING_SOURCE",
        "FORBIDDEN_SOURCE",
        "EXPANSION_TOO_LARGE",
    }
)
_DEPTH_COMPLETENESS_RANK = {"COMPLETE": 0, "PARTIAL": 1, "UNAVAILABLE": 2}
_DEPTH_SOURCE_KEYS = frozenset({"path", "sha256", "role", "storage_class", "reason", "section"})
_DEPTH_RESUME_KEYS = frozenset(
    {
        "schema_version",
        "status",
        "project_identity",
        "git_identity",
        "current_state",
        "bootstrap",
        "selected_sources",
        "handoff",
        "expansion_results",
        "context_trace",
    }
)
_DEPTH_TRACE_KEYS = frozenset(
    {
        "selected",
        "excluded_by_default",
        "selected_artifact_count",
        "selected_section_count",
        "selected_character_count",
        "explicit_expansion_count",
        "bounds",
    }
)
_DEPTH_GIT_KEYS = frozenset({"head", "branch", "clean", "state"})
_DEPTH_PROJECT_KEYS = frozenset({"project_id", "root"})
_DEPTH_BOOTSTRAP_KEYS = frozenset(
    {
        "project_id",
        "active_change",
        "last_completed_or_next_pointer",
        "lifecycle_stage",
        "stage_status",
        "implementation_authorized",
        "open_blocker",
        "next_permitted_action",
        "active_context_path",
        "source_revision",
    }
)
_DEPTH_BOUNDS = {
    "default_artifacts": DEFAULT_MAX_ARTIFACTS,
    "explicit_expansions": MAX_EXPANSIONS,
    "total_artifacts": MAX_TOTAL_ARTIFACTS,
    "current_state_chars": CURRENT_STATE_MAX_CHARS,
    "active_context_chars": ACTIVE_CONTEXT_MAX_CHARS,
    "section_chars": SECTION_MAX_CHARS,
}
_DEPTH_SOURCE_REASONS = {
    "active_state": "authority identity and exact pointers",
    "current_state": "ACTIVE compact current state",
    "active_context": "active context packet fields",
    "explicit_expansion": "explicit exact lineage expansion",
}
_DEPTH_EVENT_KEYS = frozenset(
    {
        "sequence_index",
        "source_ref",
        "role",
        "storage_class",
        "reason_family",
        "section",
        "source_revision",
        "freshness",
        "bounded_volume",
        "repeated_or_reopened",
        "completeness",
    }
)
_DEPTH_START_KEYS = frozenset(
    {
        "context_trace_ref",
        "source_revision",
        "freshness",
        "selected_sources",
        "selected_artifact_count",
        "selected_section_count",
        "selected_character_count",
        "explicit_expansion_count",
        "bounds",
    }
)
_PRODUCER_CAPABILITY = object()

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


def _build_resume_context_mapping(
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


def _depth_assert_no_raw(value: Any, *, location: str = "resume_context") -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            normalized = key.lower().replace("-", "_").replace(" ", "_") if isinstance(key, str) else ""
            if normalized in _DEPTH_RAW_KEYS:
                raise ContextError(f"OperationDepthObservationV1 rejects raw field: {location}.{key}")
            _depth_assert_no_raw(nested, location=f"{location}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _depth_assert_no_raw(nested, location=f"{location}[{index}]")


def _depth_assert_json_metadata(value: Any, *, location: str = "resume_context") -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if not isinstance(key, str):
                raise ContextError(f"{location} metadata keys must be strings")
            _depth_assert_json_metadata(nested, location=f"{location}.{key}")
    elif isinstance(value, (list, tuple)):
        for index, nested in enumerate(value):
            _depth_assert_json_metadata(nested, location=f"{location}[{index}]")
    elif value is not None and not isinstance(value, (str, int, bool)):
        raise ContextError(f"{location} contains unsupported mutable or non-JSON metadata")


def _depth_freeze(value: Any) -> Any:
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ContextError("OperationDepthObservationV1 metadata keys must be strings")
        return MappingProxyType({key: _depth_freeze(item) for key, item in value.items()})
    if isinstance(value, (list, tuple)):
        return tuple(_depth_freeze(item) for item in value)
    if value is None or isinstance(value, (str, int, bool)):
        return value
    raise ContextError("OperationDepthObservationV1 rejects mutable or non-JSON metadata")


def _depth_thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _depth_thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_depth_thaw(item) for item in value]
    return value


def _depth_operation_ref(value: object) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip() or any(char in value for char in "\r\n"):
        raise ContextError("operation_ref must be a non-empty single-line string or null")
    return value.strip()


def _depth_path(value: object, *, label: str = "source path") -> str:
    if not isinstance(value, str) or not value.strip():
        raise ContextError(f"{label} must be a non-empty repository-relative path")
    normalized = value.strip().replace("\\", "/")
    if normalized.startswith("/") or re.match(r"^[A-Za-z]:", normalized):
        raise ContextError(f"{label} must be repository-relative")
    if any(token in normalized for token in ("*", "?", "[", "]")):
        raise ContextError(f"{label} may not contain glob or pattern syntax")
    parts = normalized.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ContextError(f"{label} must be normalized")
    if normalized == ".git" or normalized.startswith(".git/"):
        raise ContextError(f"{label} escapes the eligible root")
    return normalized


def _depth_sha(value: object, *, allow_null: bool = False) -> str | None:
    if value is None and allow_null:
        return None
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", value):
        raise ContextError("source sha256 must be a 64-character hexadecimal string")
    return value.lower()


def _depth_is_expansion_path(path: str) -> bool:
    return path.startswith(
        (
            ".planning/project/",
            ".planning/changes/active/",
            ".planning/changes/completed/",
            ".planning/decisions/",
        )
    )


def _depth_source(value: object) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != _DEPTH_SOURCE_KEYS:
        raise ContextError("OperationDepthObservationV1 source metadata has an exact schema")
    section = value["section"]
    if not isinstance(section, (str, type(None))):
        raise ContextError("source section must be a string or null")
    if isinstance(section, str) and (
        not section or len(section) > SECTION_MAX_CHARS or any(char in section for char in "\r\n#")
    ):
        raise ContextError("source section must be a bounded exact heading")
    fields = {
        "path": _depth_path(value["path"]),
        "sha256": _depth_sha(value["sha256"]),
        "role": value["role"],
        "storage_class": value["storage_class"],
        "reason": value["reason"],
        "section": section,
    }
    if any(not isinstance(fields[key], str) for key in ("role", "storage_class", "reason")):
        raise ContextError("source role, storage_class, and reason must be strings")
    role = fields["role"]
    if role not in _DEPTH_SOURCE_REASONS or fields["reason"] != _DEPTH_SOURCE_REASONS[role]:
        raise ContextError("source role and reason must match the finite PL06 producer schema")
    if fields["storage_class"] != classify_storage(fields["path"]):
        raise ContextError("source storage_class must match the existing PL06 classifier")
    if role != "explicit_expansion" and section is not None:
        raise ContextError("only an explicit expansion may carry a section")
    if role == "explicit_expansion" and not _depth_is_expansion_path(fields["path"]):
        raise ContextError("explicit expansion source is outside the eligible PL06 paths")
    return fields


def _depth_source_ref(value: object) -> dict[str, Any] | None:
    if value is None:
        return None
    if not isinstance(value, Mapping) or set(value) != {"path", "sha256"}:
        raise ContextError("source_ref must contain exactly path and sha256")
    return {"path": _depth_path(value["path"]), "sha256": _depth_sha(value["sha256"])}


def _depth_count(value: object) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return None
    return value


def _depth_required_count(value: object, *, label: str) -> int:
    count = _depth_count(value)
    if count is None:
        raise ContextError(f"{label} must be a non-negative integer")
    return count


def _depth_exact_keys(value: object, expected: frozenset[str], *, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping) or set(value) != expected:
        raise ContextError(f"{label} has an exact schema")
    return value


def _depth_revision(value: object) -> dict[str, Any] | None:
    if not isinstance(value, Mapping) or set(value) not in ({"head", "state"}, _DEPTH_GIT_KEYS):
        return None
    head = value.get("head")
    state = value.get("state")
    if not isinstance(head, (str, type(None))) or not isinstance(state, str):
        return None
    if state not in {"AVAILABLE", "UNBORN", "UNAVAILABLE"}:
        return None
    return {"head": head, "state": state}


def _depth_validate_resume_shape(resume_context: Mapping[str, Any], *, require_complete: bool = False) -> None:
    unknown = set(resume_context) - _DEPTH_RESUME_KEYS
    if unknown:
        raise ContextError(f"ResumeContext has unknown keys: {sorted(unknown)}")
    if require_complete:
        missing = _DEPTH_RESUME_KEYS - set(resume_context)
        if missing:
            raise ContextError(f"ResumeContext is missing producer keys: {sorted(missing)}")
    if "schema_version" in resume_context and resume_context["schema_version"] != 1:
        raise ContextError("ResumeContext schema_version must be 1")
    status = resume_context.get("status")
    if status is not None and status not in _STATUS_RANK:
        raise ContextError("ResumeContext status is invalid")

    project_identity = resume_context.get("project_identity")
    if project_identity is not None:
        project = _depth_exact_keys(project_identity, _DEPTH_PROJECT_KEYS, label="project_identity")
        if any(not isinstance(project[key], str) or not project[key] for key in _DEPTH_PROJECT_KEYS):
            raise ContextError("project_identity values must be non-empty strings")

    git_identity = resume_context.get("git_identity")
    if git_identity is not None and (
        set(git_identity) != _DEPTH_GIT_KEYS or _depth_revision(git_identity) is None
    ):
        raise ContextError("git_identity has an exact schema")

    bootstrap = resume_context.get("bootstrap")
    if bootstrap is not None:
        boot = _depth_exact_keys(bootstrap, _DEPTH_BOOTSTRAP_KEYS, label="bootstrap")
        if any(not isinstance(boot[key], (str, type(None))) for key in _DEPTH_BOOTSTRAP_KEYS - {"implementation_authorized"}):
            raise ContextError("bootstrap metadata must use strings or null")
        if not isinstance(boot["implementation_authorized"], (bool, type(None))):
            raise ContextError("bootstrap implementation_authorized must be boolean or null")
        if project_identity is not None and boot["project_id"] != project_identity["project_id"]:
            raise ContextError("bootstrap project_id must match project_identity")
        if git_identity is not None and boot["source_revision"] != git_identity["head"]:
            raise ContextError("bootstrap source_revision must match git_identity")

    current_state = resume_context.get("current_state")
    if current_state is not None:
        if not isinstance(current_state, Mapping):
            raise ContextError("current_state must be a mapping")
        active_tuple = current_state.get("active_tuple")
        if not isinstance(active_tuple, (list, tuple)) or len(active_tuple) != 6:
            raise ContextError("current_state.active_tuple must contain six bounded values")
        if any(not isinstance(item, (str, bool, type(None))) for item in active_tuple):
            raise ContextError("current_state.active_tuple contains invalid metadata")
        for key, value in current_state.items():
            if not isinstance(key, str) or (key != "active_tuple" and not isinstance(value, (str, type(None)))):
                raise ContextError("current_state contains invalid metadata")

    handoff = resume_context.get("handoff")
    if handoff is not None:
        validate_handoff(handoff)

    normalized_sources: list[dict[str, Any]] | None = None
    sources = resume_context.get("selected_sources")
    if sources is not None:
        if not isinstance(sources, (list, tuple)) or len(sources) > MAX_TOTAL_ARTIFACTS:
            raise ContextError(f"ResumeContext selected_sources must contain at most {MAX_TOTAL_ARTIFACTS} items")
        normalized_sources = [_depth_source(source) for source in sources]

    normalized_results: list[dict[str, Any]] | None = None
    results = resume_context.get("expansion_results")
    if results is not None:
        if not isinstance(results, (list, tuple)) or len(results) > MAX_EXPANSIONS:
            raise ContextError("ResumeContext expansion_results must be bounded")
        normalized_results = []
        for result in results:
            if not isinstance(result, Mapping) or set(result) != {"status", "path", "section", "limit_chars"}:
                raise ContextError("ResumeContext expansion_results has an exact schema")
            if result["status"] != "EXPANSION_TOO_LARGE":
                raise ContextError("ResumeContext expansion_results has an unsupported status")
            path = _depth_path(result["path"])
            section = result["section"]
            if not isinstance(section, str) or not section or len(section) > SECTION_MAX_CHARS or any(char in section for char in "\r\n#"):
                raise ContextError("Expansion result section is invalid")
            if _depth_required_count(result["limit_chars"], label="expansion result limit_chars") != SECTION_MAX_CHARS:
                raise ContextError("Expansion result limit must match the existing PL06 bound")
            if not _depth_is_expansion_path(path):
                raise ContextError("Expansion result is outside eligible PL06 paths")
            normalized_results.append({"status": result["status"], "path": path, "section": section, "limit_chars": SECTION_MAX_CHARS})

    trace = resume_context.get("context_trace")
    if trace is not None:
        bounded_trace = _depth_exact_keys(trace, _DEPTH_TRACE_KEYS, label="ContextTrace")
        selected = bounded_trace["selected"]
        if not isinstance(selected, (list, tuple)) or len(selected) > MAX_TOTAL_ARTIFACTS:
            raise ContextError("ContextTrace selected sources exceed the PL06 artifact bound")
        trace_sources = [_depth_source(source) for source in selected]
        if normalized_sources is not None and trace_sources != normalized_sources:
            raise ContextError("ContextTrace selected sources must match ResumeContext selected_sources")
        if bounded_trace["excluded_by_default"] != [{"category": category, "reason": reason} for category, reason in _EXCLUDED]:
            raise ContextError("ContextTrace excluded_by_default must match the PL06 producer")
        counts = {key: _depth_required_count(bounded_trace[key], label=f"ContextTrace.{key}") for key in (
            "selected_artifact_count", "selected_section_count", "selected_character_count", "explicit_expansion_count"
        )}
        if counts["selected_artifact_count"] != len(trace_sources):
            raise ContextError("ContextTrace selected_artifact_count disagrees with selected sources")
        if counts["selected_section_count"] != sum(source["section"] is not None for source in trace_sources):
            raise ContextError("ContextTrace selected_section_count disagrees with selected sources")
        if counts["explicit_expansion_count"] > MAX_EXPANSIONS:
            raise ContextError("ContextTrace explicit_expansion_count exceeds the PL06 bound")
        if any(sum(source["role"] == role for source in trace_sources) > 1 for role in ("active_state", "current_state", "active_context")):
            raise ContextError("ContextTrace contains duplicate default source roles")
        bounds = _depth_exact_keys(bounded_trace["bounds"], frozenset(_DEPTH_BOUNDS), label="ContextTrace.bounds")
        if dict(bounds) != _DEPTH_BOUNDS:
            raise ContextError("ContextTrace bounds must match the existing PL06 limits")
        if len(trace_sources) + len(normalized_results or ()) > MAX_TOTAL_ARTIFACTS:
            raise ContextError("ResumeContext artifacts and results exceed the PL06 total bound")
        if status == "CURRENT":
            expansion_count = sum(source["role"] == "explicit_expansion" for source in trace_sources) + len(normalized_results or ())
            if counts["explicit_expansion_count"] != expansion_count:
                raise ContextError("ContextTrace expansion count disagrees with selected sources")


def _depth_start_projection(resume_context: Mapping[str, Any]) -> dict[str, Any]:
    status = resume_context.get("status")
    if status != "CURRENT":
        reason = {
            "STALE": "STALE_SOURCE",
            "SUPERSEDED": "SUPERSEDED_SOURCE",
            "MISSING_OWNER_ARTIFACT": "MISSING_SOURCE",
        }.get(status, "INVALID_START_CONTEXT")
        return {
            "context_trace_ref": None,
            "source_revision": None,
            "freshness": "UNAVAILABLE",
            "selected_sources": [],
            "selected_artifact_count": None,
            "selected_section_count": None,
            "selected_character_count": None,
            "explicit_expansion_count": None,
            "bounds": None,
            "unavailable_reason": reason,
        }
    trace = resume_context.get("context_trace")
    revision = _depth_revision(resume_context.get("git_identity"))
    if not isinstance(trace, Mapping) or revision is None:
        raise ContextError("CURRENT ResumeContext lacks producer trace or revision")
    selected = trace["selected"]
    sources = [_depth_source(item) for item in selected]
    if trace["explicit_expansion_count"] != 0 or any(source["role"] == "explicit_expansion" for source in sources):
        raise ContextError("Operation start must not contain an explicit expansion")
    if resume_context.get("expansion_results") not in ([], ()):
        raise ContextError("Operation start must not contain expansion results")
    return {
        "context_trace_ref": None,
        "source_revision": revision,
        "freshness": "CURRENT",
        "selected_sources": sources,
        "selected_artifact_count": _depth_required_count(trace["selected_artifact_count"], label="start selected_artifact_count"),
        "selected_section_count": _depth_required_count(trace["selected_section_count"], label="start selected_section_count"),
        "selected_character_count": _depth_required_count(trace["selected_character_count"], label="start selected_character_count"),
        "explicit_expansion_count": 0,
        "bounds": dict(trace["bounds"]),
    }


def _depth_next_sequence(current: tuple[Mapping[str, Any], ...], supplied: object) -> int:
    expected = len(current) + 1
    if len(current) >= MAX_EXPANSIONS:
        raise ContextError(f"OperationDepthObservationV1 allows at most {MAX_EXPANSIONS} expansion events")
    if supplied is None:
        return expected
    if isinstance(supplied, bool) or not isinstance(supplied, int) or supplied != expected:
        raise ContextError(f"sequence_index must be the next one-based contiguous value ({expected})")
    return supplied


def _depth_identity(event: Mapping[str, Any]) -> tuple[object, object, object] | None:
    source_ref = event.get("source_ref")
    if not isinstance(source_ref, Mapping):
        return None
    return source_ref.get("path"), source_ref.get("sha256"), event.get("section")


def _depth_event(value: Mapping[str, Any], *, expected_sequence: int) -> dict[str, Any]:
    if set(value) != _DEPTH_EVENT_KEYS or value["sequence_index"] != expected_sequence:
        raise ContextError("OperationDepthObservationV1 event has an invalid schema or sequence")
    completeness = value["completeness"]
    if completeness not in _DEPTH_COMPLETENESS_RANK:
        raise ContextError("OperationDepthObservationV1 event completeness is invalid")
    source_ref = _depth_source_ref(value["source_ref"])
    revision = value["source_revision"]
    if revision is not None:
        revision = _depth_revision(revision)
        if revision is None:
            raise ContextError("OperationDepthObservationV1 event revision is invalid")
    section = value["section"]
    if not isinstance(section, (str, type(None))) or (isinstance(section, str) and (not section or len(section) > SECTION_MAX_CHARS)):
        raise ContextError("OperationDepthObservationV1 event section is invalid")
    bounded_volume = value["bounded_volume"]
    if bounded_volume is not None:
        bounded_volume = _depth_required_count(bounded_volume, label="event bounded_volume")
    normalized = dict(value, source_ref=source_ref, source_revision=revision, bounded_volume=bounded_volume)
    if completeness == "COMPLETE":
        if source_ref is None or value["role"] != "explicit_expansion" or value["storage_class"] != classify_storage(source_ref["path"]):
            raise ContextError("Complete expansion event is not producer-derived")
        if value["reason_family"] != _DEPTH_SOURCE_REASONS["explicit_expansion"] or revision is None or value["freshness"] != "CURRENT":
            raise ContextError("Complete expansion event is not producer-derived")
        if value["repeated_or_reopened"] not in {"YES", "NO"}:
            raise ContextError("Complete expansion repeat status is invalid")
    elif completeness == "PARTIAL":
        if source_ref is not None or value["role"] != "explicit_expansion" or value["reason_family"] != "EXPANSION_TOO_LARGE":
            raise ContextError("Partial expansion event is not producer-derived")
        if not isinstance(section, str) or revision is None or value["freshness"] != "CURRENT" or value["repeated_or_reopened"] != "UNAVAILABLE":
            raise ContextError("Partial expansion event is not producer-derived")
    else:
        if value["role"] is not None or value["storage_class"] is not None or value["reason_family"] not in _DEPTH_REASON_CODES:
            raise ContextError("Unavailable expansion event contains unsupported metadata")
        if section is not None or revision is not None or bounded_volume is not None or value["freshness"] != "UNAVAILABLE" or value["repeated_or_reopened"] != "UNAVAILABLE":
            raise ContextError("Unavailable expansion event contains unsupported metadata")
    return normalized


@dataclass(frozen=True, slots=True, init=False)
class ProducedResumeContextV1:
    """Factory-only producer-bound wrapper around bounded ResumeContext metadata."""

    _payload: Mapping[str, Any]

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise ContextError("ProducedResumeContextV1 has no public constructor")

    @classmethod
    def _from_product(cls, payload: Mapping[str, Any], capability: object) -> "ProducedResumeContextV1":
        if capability is not _PRODUCER_CAPABILITY:
            raise ContextError("ProducedResumeContextV1 is producer-controlled")
        if type(payload) is not dict:
            raise ContextError("ProducedResumeContextV1 requires the exact producer result")
        _depth_assert_no_raw(payload)
        _depth_assert_json_metadata(payload)
        _depth_validate_resume_shape(payload, require_complete=True)
        instance = object.__new__(cls)
        object.__setattr__(instance, "_payload", _depth_freeze(payload))
        return instance

    def to_dict(self) -> dict[str, Any]:
        return _depth_thaw(self._payload)


def _build_resume_context_product(
    target: str | Path,
    *,
    include: Iterable[str] = (),
    handoff: Mapping[str, Any] | None = None,
) -> ProducedResumeContextV1:
    payload = _build_resume_context_mapping(target, include=include, handoff=handoff)
    return ProducedResumeContextV1._from_product(payload, _PRODUCER_CAPABILITY)


def build_resume_context(
    target: str | Path,
    *,
    include: Iterable[str] = (),
    handoff: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    return _build_resume_context_product(target, include=include, handoff=handoff).to_dict()


def build_observed_resume_context(
    target: str | Path,
    *,
    include: Iterable[str] = (),
    handoff: Mapping[str, Any] | None = None,
) -> ProducedResumeContextV1:
    return _build_resume_context_product(target, include=include, handoff=handoff)


@dataclass(frozen=True, slots=True, init=False)
class OperationDepthObservationV1:
    """Immutable, bounded observation over producer-bound context products."""

    operation_ref: str | None
    start: Mapping[str, Any]
    expansions: tuple[Mapping[str, Any], ...] = ()
    overall_completeness: str = "COMPLETE"
    unavailable_reasons: tuple[str, ...] = ()

    def __init__(self, *args: object, **kwargs: object) -> None:
        raise ContextError("OperationDepthObservationV1 must be created through from_produced_context")

    @classmethod
    def _create(
        cls,
        *,
        operation_ref: str | None,
        start: Mapping[str, Any],
        expansions: tuple[Mapping[str, Any], ...] = (),
    ) -> "OperationDepthObservationV1":
        normalized_ref = _depth_operation_ref(operation_ref)
        _depth_assert_no_raw(start, location="start")
        _depth_assert_json_metadata(start, location="start")
        if set(start) != _DEPTH_START_KEYS | ({"unavailable_reason"} if start.get("freshness") == "UNAVAILABLE" else set()):
            raise ContextError("OperationDepthObservationV1 start has an exact schema")
        if start["freshness"] == "UNAVAILABLE":
            if start["unavailable_reason"] not in _DEPTH_REASON_CODES or start["selected_sources"] not in ([], ()):
                raise ContextError("Unavailable operation start contains invalid metadata")
            if any(start[key] is not None for key in ("source_revision", "selected_artifact_count", "selected_section_count", "selected_character_count", "explicit_expansion_count", "bounds")):
                raise ContextError("Unavailable operation start may not retain source metadata")
        else:
            if start["freshness"] != "CURRENT" or _depth_revision(start["source_revision"]) is None:
                raise ContextError("Complete operation start is not producer-derived")
            sources = [_depth_source(source) for source in start["selected_sources"]]
            if start["selected_artifact_count"] != len(sources) or start["selected_section_count"] != sum(source["section"] is not None for source in sources):
                raise ContextError("Operation start counts disagree with retained sources")
            if start["explicit_expansion_count"] != 0 or dict(start["bounds"]) != _DEPTH_BOUNDS:
                raise ContextError("Operation start bounds are invalid")
        if not isinstance(expansions, tuple) or len(expansions) > MAX_EXPANSIONS:
            raise ContextError(f"OperationDepthObservationV1 allows at most {MAX_EXPANSIONS} expansion events")
        normalized_events = []
        for sequence, event in enumerate(expansions, start=1):
            _depth_assert_no_raw(event, location="expansion")
            _depth_assert_json_metadata(event, location="expansion")
            normalized_events.append(_depth_event(event, expected_sequence=sequence))
        overall = "UNAVAILABLE" if start["freshness"] == "UNAVAILABLE" else "COMPLETE"
        reasons = []
        if start.get("unavailable_reason"):
            reasons.append(start["unavailable_reason"])
        for event in normalized_events:
            if _DEPTH_COMPLETENESS_RANK[event["completeness"]] > _DEPTH_COMPLETENESS_RANK[overall]:
                overall = event["completeness"]
            if event["completeness"] != "COMPLETE" and event["reason_family"] not in reasons:
                reasons.append(event["reason_family"])
        instance = object.__new__(cls)
        object.__setattr__(instance, "operation_ref", normalized_ref)
        object.__setattr__(instance, "start", _depth_freeze(start))
        object.__setattr__(instance, "expansions", tuple(_depth_freeze(event) for event in normalized_events))
        object.__setattr__(instance, "overall_completeness", overall)
        object.__setattr__(instance, "unavailable_reasons", tuple(reasons))
        return instance

    @classmethod
    def from_produced_context(cls, produced_context: ProducedResumeContextV1, operation_ref: str | None = None) -> "OperationDepthObservationV1":
        if type(produced_context) is not ProducedResumeContextV1:
            raise ContextError("from_produced_context requires an exact ProducedResumeContextV1")
        return cls._create(operation_ref=operation_ref, start=_depth_start_projection(produced_context.to_dict()))

    @classmethod
    def from_resume_context(cls, resume_context: Mapping[str, Any], operation_ref: str | None = None) -> "OperationDepthObservationV1":
        raise ContextError("mapping-based observation provenance is disabled; use from_produced_context")

    def _append_event(self, event: Mapping[str, Any], *, sequence_index: object = None) -> "OperationDepthObservationV1":
        sequence = _depth_next_sequence(self.expansions, sequence_index)
        normalized = dict(event)
        normalized["sequence_index"] = sequence
        return type(self)._create(operation_ref=self.operation_ref, start=self.start, expansions=(*self.expansions, normalized))

    def record_expansion(self, produced_context: ProducedResumeContextV1, sequence_index: int | None = None) -> "OperationDepthObservationV1":
        if type(produced_context) is not ProducedResumeContextV1:
            raise ContextError("record_expansion requires an exact ProducedResumeContextV1")
        _depth_next_sequence(self.expansions, sequence_index)
        context = produced_context.to_dict()
        _depth_validate_resume_shape(context, require_complete=True)
        status = context["status"]
        stale_reason = {"STALE": "STALE_SOURCE", "SUPERSEDED": "SUPERSEDED_SOURCE", "MISSING_OWNER_ARTIFACT": "MISSING_SOURCE"}.get(status)
        if stale_reason:
            return self.record_unavailable(stale_reason, sequence_index=sequence_index)
        if status != "CURRENT":
            raise ContextError("Expansion context has no current owner status")
        trace = context["context_trace"]
        revision = _depth_revision(context["git_identity"])
        selected = [_depth_source(item) for item in trace["selected"]]
        explicit = [item for item in selected if item["role"] == "explicit_expansion"]
        baseline = [item for item in selected if item["role"] != "explicit_expansion"]
        results = context["expansion_results"]
        if trace["explicit_expansion_count"] != 1 or len(explicit) + len(results) != 1:
            raise ContextError("Expansion observation requires exactly one explicit expansion result")
        if self.start["freshness"] != "CURRENT" or baseline != _depth_thaw(self.start["selected_sources"]):
            raise ContextError("Expansion context default sources do not match the operation start")
        if revision != _depth_thaw(self.start["source_revision"]):
            raise ContextError("Expansion context revision does not match the operation start")
        bounded_volume = _depth_required_count(trace["selected_character_count"], label="expansion bounded volume")
        if explicit:
            source = explicit[0]
            identity = (source["path"], source["sha256"], source["section"])
            event = {
                "source_ref": {"path": source["path"], "sha256": source["sha256"]},
                "role": source["role"],
                "storage_class": source["storage_class"],
                "reason_family": source["reason"],
                "section": source["section"],
                "source_revision": revision,
                "freshness": status,
                "bounded_volume": bounded_volume,
                "repeated_or_reopened": "YES" if any(_depth_identity(previous) == identity for previous in self.expansions) else "NO",
                "completeness": "COMPLETE",
            }
            return self._append_event(event, sequence_index=sequence_index)
        result = results[0]
        if result["status"] != "EXPANSION_TOO_LARGE":
            raise ContextError("Expansion result has an unsupported bounded status")
        event = {
            "source_ref": None,
            "role": "explicit_expansion",
            "storage_class": classify_storage(_depth_path(result["path"])),
            "reason_family": "EXPANSION_TOO_LARGE",
            "section": result["section"],
            "source_revision": revision,
            "freshness": status,
            "bounded_volume": bounded_volume,
            "repeated_or_reopened": "UNAVAILABLE",
            "completeness": "PARTIAL",
        }
        return self._append_event(event, sequence_index=sequence_index)

    def record_unavailable(self, reason_code: str, sequence_index: int | None = None, source_ref: Mapping[str, Any] | None = None) -> "OperationDepthObservationV1":
        if reason_code not in _DEPTH_REASON_CODES:
            raise ContextError(f"Unsupported observation unavailable reason: {reason_code!r}")
        _depth_next_sequence(self.expansions, sequence_index)
        normalized_ref = _depth_source_ref(source_ref)
        if normalized_ref is not None:
            known = {(source["path"], source["sha256"]) for source in self.start.get("selected_sources", ())}
            known.update(
                (event_ref["path"], event_ref["sha256"])
                for event in self.expansions
                if isinstance((event_ref := event.get("source_ref")), Mapping)
            )
            if (normalized_ref["path"], normalized_ref["sha256"]) not in known:
                raise ContextError("record_unavailable source_ref must already be bound to this observation")
        return self._append_event(
            {
                "source_ref": normalized_ref,
                "role": None,
                "storage_class": None,
                "reason_family": reason_code,
                "section": None,
                "source_revision": None,
                "freshness": "UNAVAILABLE",
                "bounded_volume": None,
                "repeated_or_reopened": "UNAVAILABLE",
                "completeness": "UNAVAILABLE",
            },
            sequence_index=sequence_index,
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "operation_ref": self.operation_ref,
            "start": _depth_thaw(self.start),
            "expansions": [_depth_thaw(event) for event in self.expansions],
            "overall_completeness": self.overall_completeness,
            "unavailable_reasons": list(self.unavailable_reasons),
        }


validate_resume_context = build_resume_context
resume_context = build_resume_context


__all__ = [
    "ContextError",
    "OperationDepthObservationV1",
    "ProducedResumeContextV1",
    "build_compact_status",
    "build_observed_resume_context",
    "build_resume_context",
    "classify_storage",
    "resume_context",
    "validate_handoff",
    "validate_resume_context",
]
