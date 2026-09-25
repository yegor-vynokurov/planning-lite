from __future__ import annotations

import hashlib
import os
import re
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from .execution_guidance import OperationGuidanceV1


class ProjectSpineHandoffError(RuntimeError):
    """The authoritative Project Spine handoff failed closed."""


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
_SNAPSHOT_FIELDS = (
    "Change",
    "Lifecycle stage",
    "Stage status",
    "Next gate",
    "Next permitted action",
    "Implementation authorized",
    "Active context packet",
)
_PROTECTED_FIELDS = tuple(field for field in _ACTIVE_FIELDS if field != "Last verified checkpoint")
_BULLET_RE = re.compile(
    r"(?m)^[ \t]*-[ \t]*(?P<key>[^:\r\n]+):(?P<value>[^\r\n]*)(?P<newline>\r\n|\n|\r|$)"
)
_ACTIVE_HEADING_RE = re.compile(r"(?m)^##[ \t]+Active change[ \t]*(?:\r\n|\n|\r|$)")
_BLOCKING_HEADING_RE = re.compile(r"(?m)^##[ \t]+Blocking decision[ \t]*(?:\r\n|\n|\r|$)")
_NEXT_SECTION_RE = re.compile(r"(?m)^#{1,2}[ \t]+")
_CHECKPOINT_LINE_RE = re.compile(
    r"(?m)^[ \t]*-[ \t]*Last verified checkpoint:[^\r\n]*(?:\r\n|\n|\r|$)"
)
_TRUE_VALUES = frozenset({"yes", "true", "authorized", "allowed"})
_FALSE_VALUES = frozenset({"no", "false", "not authorized", "denied"})


@dataclass(frozen=True, slots=True)
class ProjectSpineSnapshotV1:
    active_change: str
    lifecycle_stage: str
    stage_status: str
    next_gate: str
    next_permitted_action: str
    implementation_authorized: bool
    active_context_path: str
    active_sha256: str

    def __post_init__(self) -> None:
        for name in (
            "active_change",
            "lifecycle_stage",
            "stage_status",
            "next_gate",
            "next_permitted_action",
            "active_context_path",
        ):
            _nonempty_text(getattr(self, name), name)
        if not isinstance(self.implementation_authorized, bool):
            raise ProjectSpineHandoffError("implementation_authorized must be bool")
        if not isinstance(self.active_sha256, str) or not re.fullmatch(
            r"[0-9A-F]{64}", self.active_sha256
        ):
            raise ProjectSpineHandoffError("active_sha256 must be uppercase SHA-256")


@dataclass(frozen=True, slots=True)
class PostEvaluationCheckpointV1:
    attempt_id: str
    result_id: str
    evaluation_id: str
    evaluation_outcome: str
    evaluation_reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in (
            "attempt_id",
            "result_id",
            "evaluation_id",
            "evaluation_outcome",
        ):
            _nonempty_text(getattr(self, name), name)
        if type(self.evaluation_reason_codes) is not tuple:
            raise ProjectSpineHandoffError("evaluation_reason_codes must be tuple")
        for index, value in enumerate(self.evaluation_reason_codes):
            _nonempty_text(value, f"evaluation_reason_codes[{index}]")


@dataclass(frozen=True, slots=True)
class _ParsedActive:
    values: dict[str, object]
    blocking_section: str | None
    checkpoint_span: tuple[int, int]


def _nonempty_text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProjectSpineHandoffError(f"{name} must be non-empty")
    if "\r" in value or "\n" in value:
        raise ProjectSpineHandoffError(f"{name} must not contain CR or LF")
    return value


def _clean(value: str) -> str | None:
    text = value.strip()
    if len(text) >= 2 and text.startswith(chr(96)) and text.endswith(chr(96)):
        text = text[1:-1].strip()
    if text.lower() in {"", "none", "null", "n/a", "na", "-"}:
        return None
    return text


def _boolean(value: str, name: str) -> bool:
    cleaned = _clean(value)
    if cleaned is None:
        raise ProjectSpineHandoffError(f"{name} is missing")
    lowered = cleaned.lower()
    if lowered in _TRUE_VALUES:
        return True
    if lowered in _FALSE_VALUES:
        return False
    raise ProjectSpineHandoffError(f"{name} has an invalid value")


def _active_bounds(text: str) -> tuple[int, int]:
    matches = list(_ACTIVE_HEADING_RE.finditer(text))
    if len(matches) != 1:
        raise ProjectSpineHandoffError("Active change section is missing or ambiguous")
    start = matches[0].end()
    next_heading = _NEXT_SECTION_RE.search(text, start)
    return start, next_heading.start() if next_heading is not None else len(text)


def _blocking_section(text: str) -> str | None:
    matches = list(_BLOCKING_HEADING_RE.finditer(text))
    if len(matches) > 1:
        raise ProjectSpineHandoffError("Blocking decision section is ambiguous")
    if not matches:
        return None
    start = matches[0].end()
    next_heading = _NEXT_SECTION_RE.search(text, start)
    end = next_heading.start() if next_heading is not None else len(text)
    return text[start:end]


def _parse_active(text: str) -> _ParsedActive:
    active_start, active_end = _active_bounds(text)
    active_text = text[active_start:active_end]
    occurrences: dict[str, list[re.Match[str]]] = {}
    for match in _BULLET_RE.finditer(active_text):
        key = match.group("key").strip()
        if key in _ACTIVE_FIELDS:
            occurrences.setdefault(key, []).append(match)
    for field in _ACTIVE_FIELDS:
        if len(occurrences.get(field, ())) != 1:
            raise ProjectSpineHandoffError(
                f"Active field is missing or duplicated: {field}"
            )

    values: dict[str, object] = {}
    for field in _ACTIVE_FIELDS:
        match = occurrences[field][0]
        raw_value = match.group("value")
        if field == "Implementation authorized":
            values[field] = _boolean(raw_value, field)
        else:
            cleaned = _clean(raw_value)
            if cleaned is None:
                raise ProjectSpineHandoffError(f"{field} is missing or empty")
            values[field] = cleaned

    checkpoint_match = _CHECKPOINT_LINE_RE.search(active_text)
    if checkpoint_match is None:
        raise ProjectSpineHandoffError("Last verified checkpoint field is missing")
    if _CHECKPOINT_LINE_RE.search(active_text, checkpoint_match.end()) is not None:
        raise ProjectSpineHandoffError("Last verified checkpoint field is duplicated")

    return _ParsedActive(
        values=values,
        blocking_section=_blocking_section(text),
        checkpoint_span=(
            active_start + checkpoint_match.start(),
            active_start + checkpoint_match.end(),
        ),
    )


def _active_path(target_root: str | Path) -> Path:
    root = Path(target_root).expanduser().resolve()
    return root / ".planning" / "ACTIVE.md"


def _read_parsed_active(target_root: str | Path) -> tuple[Path, bytes, str, _ParsedActive]:
    path = _active_path(target_root)
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise ProjectSpineHandoffError(f"Cannot read authoritative ACTIVE.md: {path}") from exc
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ProjectSpineHandoffError("ACTIVE.md must be valid UTF-8") from exc
    return path, raw, text, _parse_active(text)


def _snapshot_from(parsed: _ParsedActive, raw: bytes) -> ProjectSpineSnapshotV1:
    values = parsed.values
    digest = hashlib.sha256(raw).hexdigest().upper()
    return ProjectSpineSnapshotV1(
        active_change=values["Change"],  # type: ignore[arg-type]
        lifecycle_stage=values["Lifecycle stage"],  # type: ignore[arg-type]
        stage_status=values["Stage status"],  # type: ignore[arg-type]
        next_gate=values["Next gate"],  # type: ignore[arg-type]
        next_permitted_action=values["Next permitted action"],  # type: ignore[arg-type]
        implementation_authorized=values["Implementation authorized"],  # type: ignore[arg-type]
        active_context_path=values["Active context packet"],  # type: ignore[arg-type]
        active_sha256=digest,
    )


def _snapshot_values(snapshot: ProjectSpineSnapshotV1) -> tuple[object, ...]:
    return (
        snapshot.active_change,
        snapshot.lifecycle_stage,
        snapshot.stage_status,
        snapshot.next_gate,
        snapshot.next_permitted_action,
        snapshot.implementation_authorized,
        snapshot.active_context_path,
    )


def _parsed_snapshot_values(parsed: _ParsedActive) -> tuple[object, ...]:
    values = parsed.values
    return tuple(values[field] for field in _SNAPSHOT_FIELDS)


def _protected_values(parsed: _ParsedActive) -> tuple[object, ...]:
    return tuple(parsed.values[field] for field in _PROTECTED_FIELDS) + (
        parsed.blocking_section,
    )


def _validate_guidance(operation_guidance: OperationGuidanceV1) -> None:
    if not isinstance(operation_guidance, Mapping):
        raise ProjectSpineHandoffError("OperationGuidanceV1 is not a mapping")
    if operation_guidance.get("outcome") != "MATCHED":
        raise ProjectSpineHandoffError("OperationGuidance outcome is not MATCHED")
    authority = operation_guidance.get("authority")
    if not isinstance(authority, Mapping) or authority.get("predicate_result") != "AUTHORIZED_FOR_THIS_OPERATION":
        raise ProjectSpineHandoffError("OperationGuidance predicate is not authorized")
    capabilities = operation_guidance.get("capabilities")
    if not isinstance(capabilities, (list, tuple)):
        raise ProjectSpineHandoffError("OperationGuidance capabilities are missing")
    if not any(
        isinstance(item, Mapping)
        and item.get("capability_id") == "GOVERNANCE_WRITE"
        and item.get("state") == "ALLOWED"
        for item in capabilities
    ):
        raise ProjectSpineHandoffError("GOVERNANCE_WRITE is not ALLOWED")
    guidance = operation_guidance.get("guidance")
    if not isinstance(guidance, Mapping):
        raise ProjectSpineHandoffError("OperationGuidance guidance is missing")
    if guidance.get("next_gate_owner_ref") != "change-owner":
        raise ProjectSpineHandoffError("next_gate_owner_ref is not change-owner")
    if guidance.get("next_gate_ref") != ".planning/ACTIVE.md#Active change":
        raise ProjectSpineHandoffError("next_gate_ref is not authoritative ACTIVE")


def _checkpoint_line(checkpoint: PostEvaluationCheckpointV1) -> str:
    reasons = ",".join(checkpoint.evaluation_reason_codes) or "NONE"
    value = (
        f"POST_PL08 attempt={checkpoint.attempt_id} result={checkpoint.result_id} "
        f"evaluation={checkpoint.evaluation_id} outcome={checkpoint.evaluation_outcome} "
        f"reasons={reasons}"
    )
    return "- Last verified checkpoint: " + chr(96) + value + chr(96)


def capture_project_spine_snapshot(target_root: str | Path) -> ProjectSpineSnapshotV1:
    """Capture the authoritative ACTIVE state without writing it."""

    _, raw, _, parsed = _read_parsed_active(target_root)
    return _snapshot_from(parsed, raw)


def record_post_evaluation_checkpoint(
    target_root: str | Path,
    *,
    pre_execution_snapshot: ProjectSpineSnapshotV1,
    checkpoint: PostEvaluationCheckpointV1,
    operation_guidance: OperationGuidanceV1,
) -> ProjectSpineSnapshotV1:
    """Atomically record one post-PL08 checkpoint under an owner-state guard."""

    if not isinstance(pre_execution_snapshot, ProjectSpineSnapshotV1):
        raise ProjectSpineHandoffError("pre_execution_snapshot has an invalid type")
    if not isinstance(checkpoint, PostEvaluationCheckpointV1):
        raise ProjectSpineHandoffError("checkpoint has an invalid type")
    _validate_guidance(operation_guidance)

    path, raw, text, parsed = _read_parsed_active(target_root)
    digest = hashlib.sha256(raw).hexdigest().upper()
    if digest != pre_execution_snapshot.active_sha256:
        raise ProjectSpineHandoffError("ACTIVE.md changed during execution")
    if _parsed_snapshot_values(parsed) != _snapshot_values(pre_execution_snapshot):
        raise ProjectSpineHandoffError("protected Project Spine snapshot changed")

    start, end = parsed.checkpoint_span
    line_text = text[start:end]
    newline_match = re.search(r"\r\n|\n|\r$", line_text)
    newline = newline_match.group(0) if newline_match is not None else ""
    replacement = _checkpoint_line(checkpoint) + newline
    new_text = text[:start] + replacement + text[end:]
    new_raw = new_text.encode("utf-8")

    temporary: str | None = None
    try:
        fd, temporary = tempfile.mkstemp(
            prefix=f".{path.name}.",
            suffix=".tmp",
            dir=str(path.parent),
        )
        with os.fdopen(fd, "wb") as handle:
            handle.write(new_raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    except (OSError, UnicodeError) as exc:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass
        raise ProjectSpineHandoffError("atomic Project Spine checkpoint failed") from exc

    try:
        _, reread_raw, _, reread = _read_parsed_active(target_root)
        reread_snapshot = _snapshot_from(reread, reread_raw)
        if _protected_values(reread) != _protected_values(parsed):
            raise ProjectSpineHandoffError("protected Project Spine state changed after write")
        if _snapshot_values(reread_snapshot) != _snapshot_values(pre_execution_snapshot):
            raise ProjectSpineHandoffError("authoritative Project Spine readback changed")
        return reread_snapshot
    except ProjectSpineHandoffError:
        raise
    except (OSError, UnicodeError, ValueError) as exc:
        raise ProjectSpineHandoffError("authoritative Project Spine readback failed") from exc


__all__ = [
    "ProjectSpineHandoffError",
    "ProjectSpineSnapshotV1",
    "PostEvaluationCheckpointV1",
    "capture_project_spine_snapshot",
    "record_post_evaluation_checkpoint",
]
