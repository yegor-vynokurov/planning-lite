"""Explicit, byte-bounded Codex source-segment adapter for Work Windows."""

from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping

from .telemetry import (
    CONFIGURATION_REF_ROLE,
    RESOURCE_METRICS,
    WORK_WINDOW_MEMBERSHIP_RULE,
    ReceiptError,
    append_resource_observation,
    canonical_bytes,
    _load_answers_ref,
    persist_work_window_registration,
    read_resource_observation_for_window,
    read_work_window_registration,
    validate_configuration_ref,
)


PREFIX_ANCHOR_BYTES = 64
CODEX_RECORD_TYPES = {
    "session_meta", "turn_context", "event_msg", "token_usage_record",
    "compacted", "response_item", "inter_agent_communication_metadata", "world_state",
}
CODEX_EVENT_TYPES = {
    "token_count", "task_started", "task_complete", "user_message", "assistant_message",
    "function_call", "reasoning", "agent_message",
}
CODEX_RESPONSE_ITEM_TYPES = {
    "assistant_message", "reasoning", "custom_tool_call", "message",
    "custom_tool_call_output",
}
USAGE_KEYS = RESOURCE_METRICS | {"cache_write_input_tokens"}


class WorkWindowError(ReceiptError):
    """Bounded source or membership failure."""


class _PendingRead(WorkWindowError):
    pass


class _TerminalSource(WorkWindowError):
    def __init__(self, reason: str, *, end_offset: int | None = None):
        self.reason = reason
        self.end_offset = end_offset
        super().__init__(reason)


class _StableSegmentFailure(WorkWindowError):
    """A stable bounded segment was read, but its envelope/usage was invalid."""

    def __init__(self, reason: str, *, end_offset: int, segment_digest: str):
        self.reason = reason
        self.end_offset = end_offset
        self.segment_digest = segment_digest
        super().__init__(reason)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _file_identity(handle: Any, path: Path) -> dict[str, Any]:
    try:
        opened = os.fstat(handle.fileno())
        linked = path.stat()
    except OSError as exc:
        raise _PendingRead("SOURCE_READ_UNSTABLE") from exc
    opened_identity = (int(opened.st_dev), int(opened.st_ino))
    linked_identity = (int(linked.st_dev), int(linked.st_ino))
    if opened_identity != linked_identity:
        raise _TerminalSource("SOURCE_IDENTITY_MISMATCH", end_offset=int(opened.st_size))
    if opened_identity[1] == 0:
        raise _TerminalSource("SOURCE_IDENTITY_MISMATCH", end_offset=int(opened.st_size))
    return {"path": str(path), "device": opened_identity[0], "file_id": opened_identity[1]}


def _anchor_at(handle: Any, start_offset: int) -> dict[str, Any]:
    anchor_start = max(0, start_offset - PREFIX_ANCHOR_BYTES)
    handle.seek(anchor_start)
    value = handle.read(start_offset - anchor_start)
    if len(value) != start_offset - anchor_start:
        raise _PendingRead("SOURCE_READ_UNSTABLE")
    return {
        "start_offset_bytes": anchor_start,
        "end_offset_bytes": start_offset,
        "sha256": _sha(value),
    }


def _build_registration(intent: Mapping[str, Any]) -> dict[str, Any]:
    path = Path(str(intent["source_ref"])).expanduser()
    try:
        resolved = path.resolve(strict=True)
        if not resolved.is_file():
            raise FileNotFoundError(str(resolved))
        with resolved.open("rb") as handle:
            identity = _file_identity(handle, resolved)
            handle.seek(0, os.SEEK_END)
            start = handle.tell()
            if start:
                handle.seek(start - 1)
                if handle.read(1) != b"\n":
                    raise WorkWindowError("SOURCE_READ_UNSTABLE: source EOF is not a complete LF JSONL boundary")
            anchor = _anchor_at(handle, start)
            after = _file_identity(handle, resolved)
            if after != identity or os.fstat(handle.fileno()).st_size < start:
                raise WorkWindowError("SOURCE_READ_UNSTABLE")
    except FileNotFoundError as exc:
        raise WorkWindowError("SOURCE_NOT_FOUND") from exc
    except PermissionError as exc:
        raise WorkWindowError("SOURCE_NOT_FOUND") from exc
    return {
        "record_type": "work_window_registration",
        "schema_version": 1,
        "window_id": intent["window_id"],
        "project_id": intent["project_id"],
        "project_root": intent["project_root"],
        "configuration_ref": intent["configuration_ref"],
        "planning_lite_ref": intent["planning_lite_ref"],
        "configuration_ref_role": CONFIGURATION_REF_ROLE,
        "provider": "codex",
        "model": intent["model"],
        "membership_rule": WORK_WINDOW_MEMBERSHIP_RULE,
        "source_ref": str(resolved),
        "source_identity": identity,
        "start_offset_bytes": start,
        "prefix_anchor": anchor,
        "registered_at_utc": _now(),
        "registration_state": "OPEN",
    }


def open_work_window(
    *,
    window_id: str,
    project_id: str,
    project_root: str | Path,
    configuration_ref: str,
    source_ref: str | Path,
    model: str | None,
    receipt_path: str | Path,
) -> dict[str, Any]:
    """Persist an explicit registration, returning the immutable first readback."""

    config_ref = validate_configuration_ref(configuration_ref)
    resolved_project_root = Path(project_root).expanduser().resolve()
    # Resolve the target's installed ref before resolving or inspecting the
    # source path, and before the persistence layer can append registration.
    planning_lite_ref = _load_answers_ref(
        resolved_project_root / ".copier-answers.planning-lite.yml",
        reject_unknown=True,
    )
    source = str(Path(source_ref).expanduser().resolve())
    intent = {
        "window_id": window_id,
        "project_id": project_id,
        "project_root": str(resolved_project_root),
        "configuration_ref": config_ref,
        "planning_lite_ref": planning_lite_ref,
        "provider": "codex",
        "model": model,
        "membership_rule": WORK_WINDOW_MEMBERSHIP_RULE,
        "source_ref": source,
    }
    return persist_work_window_registration(
        intent,
        receipt_path=receipt_path,
        registered_project_id=project_id,
        registration_factory=lambda: _build_registration(intent),
    )


def _skip_string(raw: str, index: int) -> int:
    if index >= len(raw) or raw[index] != '"':
        raise ValueError("expected JSON string")
    index += 1
    while index < len(raw):
        char = raw[index]
        if char == '"':
            return index + 1
        if ord(char) < 0x20:
            raise ValueError("control character in JSON string")
        if char == "\\":
            index += 1
            if index >= len(raw):
                break
            if raw[index] == "u":
                digits = raw[index + 1 : index + 5]
                if len(digits) != 4 or any(c not in "0123456789abcdefABCDEF" for c in digits):
                    raise ValueError("invalid JSON unicode escape")
                index += 4
            elif raw[index] not in '"\\/bfnrt':
                raise ValueError("invalid JSON escape")
        index += 1
    raise ValueError("unterminated JSON string")


def _skip_value(raw: str, index: int) -> int:
    return _scan_json_value(raw, index)


def _scan_number(raw: str, index: int) -> int:
    start = index
    if index < len(raw) and raw[index] == "-":
        index += 1
    if index >= len(raw):
        raise ValueError("incomplete JSON number")
    if raw[index] == "0":
        index += 1
        if index < len(raw) and raw[index] in "0123456789":
            raise ValueError("leading zero in JSON number")
    elif "1" <= raw[index] <= "9":
        index += 1
        while index < len(raw) and raw[index] in "0123456789":
            index += 1
    else:
        raise ValueError("invalid JSON number")
    if index < len(raw) and raw[index] == ".":
        index += 1
        fraction_start = index
        while index < len(raw) and raw[index] in "0123456789":
            index += 1
        if index == fraction_start:
            raise ValueError("incomplete JSON fraction")
    if index < len(raw) and raw[index] in "eE":
        index += 1
        if index < len(raw) and raw[index] in "+-":
            index += 1
        exponent_start = index
        while index < len(raw) and raw[index] in "0123456789":
            index += 1
        if index == exponent_start:
            raise ValueError("incomplete JSON exponent")
    if index == start:
        raise ValueError("invalid JSON number")
    return index


def _scan_json_value(raw: str, index: int) -> int:
    while index < len(raw) and raw[index] in " \t\r\n":
        index += 1
    if index >= len(raw):
        raise ValueError("missing JSON value")
    if raw[index] == '"':
        return _skip_string(raw, index)
    if raw[index] == "{":
        seen: set[str] = set()
        index += 1
        index = _skip_ws(raw, index)
        if index < len(raw) and raw[index] == "}":
            return index + 1
        while True:
            key, index = _scan_string(raw, index)
            if key in seen:
                raise ValueError("duplicate JSON object key")
            seen.add(key)
            index = _skip_ws(raw, index)
            if index >= len(raw) or raw[index] != ":":
                raise ValueError("missing JSON object colon")
            index = _scan_json_value(raw, index + 1)
            index = _skip_ws(raw, index)
            if index < len(raw) and raw[index] == "}":
                return index + 1
            if index >= len(raw) or raw[index] != ",":
                raise ValueError("missing JSON object comma")
            index = _skip_ws(raw, index + 1)
            if index >= len(raw) or raw[index] == "}":
                raise ValueError("trailing JSON object comma")
    if raw[index] == "[":
        index = _skip_ws(raw, index + 1)
        if index < len(raw) and raw[index] == "]":
            return index + 1
        while True:
            index = _scan_json_value(raw, index)
            index = _skip_ws(raw, index)
            if index < len(raw) and raw[index] == "]":
                return index + 1
            if index >= len(raw) or raw[index] != ",":
                raise ValueError("missing JSON array comma")
            index = _skip_ws(raw, index + 1)
            if index >= len(raw) or raw[index] == "]":
                raise ValueError("trailing JSON array comma")
    for literal in ("true", "false", "null"):
        if raw.startswith(literal, index):
            return index + len(literal)
    if raw[index] == "-" or raw[index].isdigit():
        return _scan_number(raw, index)
    raise ValueError("invalid JSON value")


def _skip_ws(raw: str, index: int) -> int:
    while index < len(raw) and raw[index] in " \t\r\n":
        index += 1
    return index


def _scan_string(raw: str, index: int) -> tuple[str, int]:
    decoder = json.JSONDecoder()
    value, end = decoder.raw_decode(raw, index)
    if not isinstance(value, str):
        raise ValueError("expected JSON string")
    return value, end


def _object_field_start(raw: str, object_start: int, wanted: str) -> int | None:
    index = _skip_ws(raw, object_start)
    if index >= len(raw) or raw[index] != "{":
        raise ValueError("expected JSON object")
    index += 1
    found: int | None = None
    while True:
        index = _skip_ws(raw, index)
        if index >= len(raw):
            raise ValueError("unterminated JSON object")
        if raw[index] == "}":
            return found
        key, index = _scan_string(raw, index)
        index = _skip_ws(raw, index)
        if index >= len(raw) or raw[index] != ":":
            raise ValueError("missing JSON object colon")
        value_start = _skip_ws(raw, index + 1)
        if key == wanted:
            if found is not None:
                raise ValueError(f"duplicate JSON field: {wanted}")
            found = value_start
        index = _skip_ws(raw, _skip_value(raw, value_start))
        if index >= len(raw):
            raise ValueError("unterminated JSON object")
        if raw[index] == "}":
            return found
        if raw[index] != ",":
            raise ValueError("missing JSON object comma")
        index += 1
        next_index = _skip_ws(raw, index)
        if next_index >= len(raw) or raw[next_index] == "}":
            raise ValueError("trailing JSON object comma")
        index = next_index


def _top_level_type(raw: str) -> str:
    return _validate_source_envelope(raw)[0]


def _validate_source_envelope(raw: str) -> tuple[str, int]:
    index = _skip_ws(raw, 0)
    if index >= len(raw) or raw[index] != "{":
        raise ValueError("top-level JSON row is not an object")
    index += 1
    record_type: str | None = None
    timestamp: str | None = None
    payload_start: int | None = None
    keys: set[str] = set()
    while True:
        index = _skip_ws(raw, index)
        if index >= len(raw):
            raise ValueError("unterminated top-level JSON object")
        if raw[index] == "}":
            index += 1
            break
        key, index = _scan_string(raw, index)
        if key in keys:
            raise ValueError(f"duplicate top-level JSON field: {key}")
        if key not in {"timestamp", "type", "payload", "metadata"}:
            raise ValueError("unknown top-level envelope field")
        keys.add(key)
        index = _skip_ws(raw, index)
        if index >= len(raw) or raw[index] != ":":
            raise ValueError("missing top-level colon")
        value_start = _skip_ws(raw, index + 1)
        if key == "type":
            record_type, end = _scan_string(raw, value_start)
            if not record_type.strip():
                raise ValueError("empty type discriminator")
            index = end
        elif key == "timestamp":
            timestamp, index = _scan_string(raw, value_start)
            if not timestamp.strip():
                raise ValueError("empty timestamp")
        elif key == "payload":
            if value_start >= len(raw) or raw[value_start] != "{":
                raise ValueError("payload must be a JSON object")
            payload_start = value_start
            index = _scan_json_value(raw, value_start)
        elif key == "metadata":
            if value_start >= len(raw) or raw[value_start] != "{":
                raise ValueError("metadata must be a JSON object")
            index = _scan_json_value(raw, value_start)
        else:
            raise ValueError("unsupported top-level envelope field")
        index = _skip_ws(raw, index)
        if index < len(raw) and raw[index] == ",":
            index += 1
            next_index = _skip_ws(raw, index)
            if next_index >= len(raw) or raw[next_index] == "}":
                raise ValueError("trailing top-level JSON comma")
            index = next_index
            continue
        if index < len(raw) and raw[index] == "}":
            index += 1
            break
        raise ValueError("invalid top-level JSON object")
    if _skip_ws(raw, index) != len(raw):
        raise ValueError("trailing content after top-level JSON object")
    if not {"timestamp", "type", "payload"} <= keys or record_type is None or timestamp is None or payload_start is None:
        raise ValueError("incomplete current Codex envelope")
    try:
        parsed_timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError("invalid Codex envelope timestamp") from exc
    if parsed_timestamp.tzinfo is None or parsed_timestamp.utcoffset() is None:
        raise ValueError("Codex envelope timestamp must be timezone-aware")
    if _skip_ws(raw, index) != len(raw):
        raise ValueError("trailing content after top-level JSON object")
    return record_type, payload_start


def _payload_strings(raw: str, names: set[str]) -> dict[str, str | None]:
    payload = _object_field_start(raw, 0, "payload")
    if payload is None:
        raise ValueError("missing payload")
    result: dict[str, str | None] = {}
    for name in names:
        start = _object_field_start(raw, payload, name)
        if start is None:
            continue
        if raw.startswith("null", start):
            end = _skip_ws(raw, start + 4)
            if end >= len(raw) or raw[end] not in ",}":
                raise ValueError(f"{name} must be null or a string")
            result[name] = None
            continue
        value, end = _scan_string(raw, start)
        if _skip_ws(raw, end) < len(raw) and raw[_skip_ws(raw, end)] not in ",}":
            raise ValueError(f"{name} must be a string or null")
        result[name] = value
    return result


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def _parse_usage_line(raw: str) -> dict[str, Any]:
    record_type, _payload_start = _validate_source_envelope(raw)
    if record_type != "token_usage_record":
        raise WorkWindowError("USAGE_RECORD_INVALID")
    try:
        record = json.loads(raw, object_pairs_hook=_unique_object)
    except (json.JSONDecodeError, ValueError, RecursionError) as exc:
        raise WorkWindowError("USAGE_RECORD_INVALID") from exc
    if not isinstance(record, dict) or set(record) != {"timestamp", "type", "payload"}:
        raise WorkWindowError("USAGE_RECORD_INVALID")
    payload = record.get("payload")
    allowed_payload = {
        "thread_id", "turn_id", "session_id", "response_id", "usage",
        "turn_token_usage", "thread_token_usage", "root_turn_id", "model", "model_id",
    }
    if not isinstance(payload, dict) or set(payload) - allowed_payload:
        raise WorkWindowError("USAGE_RECORD_INVALID")
    thread_id = payload.get("thread_id")
    response_id = payload.get("response_id")
    session_id = payload.get("session_id")
    if not isinstance(thread_id, str) or not thread_id.strip() or not isinstance(response_id, str) or not response_id.strip():
        raise WorkWindowError("USAGE_RECORD_INVALID")
    if session_id is not None and (not isinstance(session_id, str) or not session_id.strip()):
        raise WorkWindowError("USAGE_RECORD_INVALID")
    model = payload.get("model") if payload.get("model") is not None else payload.get("model_id")
    if model is not None and (not isinstance(model, str) or not model.strip()):
        raise WorkWindowError("USAGE_RECORD_INVALID")
    if payload.get("model") is not None and payload.get("model_id") is not None and payload["model"] != payload["model_id"]:
        raise WorkWindowError("CONFIGURATION_BINDING_MISMATCH")
    usage = payload.get("usage")
    if not isinstance(usage, dict) or set(usage) - USAGE_KEYS:
        raise WorkWindowError("USAGE_RECORD_INVALID")
    checked_usage: dict[str, int] = {}
    for name, value in usage.items():
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise WorkWindowError("USAGE_RECORD_INVALID")
        checked_usage[name] = value
    if checked_usage.get("cache_write_input_tokens", 0) != 0:
        raise WorkWindowError("USAGE_RECORD_INVALID")
    metrics = {name: checked_usage[name] for name in RESOURCE_METRICS if name in checked_usage}
    return {
        "thread_id": thread_id,
        "session_id": session_id,
        "response_id": response_id,
        "model": model,
        "usage": metrics,
    }


def _read_bounded(
    handle: Any, *, start_offset: int, end_offset: int, parse: bool
) -> tuple[str, list[dict[str, Any]], str | None]:
    handle.seek(start_offset)
    remaining = end_offset - start_offset
    digest = hashlib.sha256()
    rows: list[dict[str, Any]] = []
    failure: str | None = None
    while remaining:
        line = handle.readline(remaining)
        if not line:
            raise _PendingRead("SOURCE_READ_UNSTABLE")
        digest.update(line)
        remaining -= len(line)
        if not line.endswith(b"\n"):
            raise _PendingRead("SOURCE_READ_UNSTABLE")
        if not parse or failure is not None:
            continue
        content = line[:-1]
        if content.endswith(b"\r"):
            content = content[:-1]
        try:
            raw = content.decode("utf-8")
            record_type = _top_level_type(raw)
            if record_type not in CODEX_RECORD_TYPES:
                raise WorkWindowError("USAGE_RECORD_INVALID")
            if record_type == "event_msg":
                event_type = _payload_strings(raw, {"type"}).get("type")
                if not isinstance(event_type, str) or not event_type.strip() or event_type not in CODEX_EVENT_TYPES:
                    raise WorkWindowError("USAGE_RECORD_INVALID")
                if event_type == "task_started":
                    turn_id = _payload_strings(raw, {"turn_id"}).get("turn_id")
                    if not isinstance(turn_id, str) or not turn_id.strip():
                        raise WorkWindowError("USAGE_RECORD_INVALID")
            if record_type == "token_usage_record":
                rows.append(_parse_usage_line(raw))
            elif record_type == "session_meta":
                fields = _payload_strings(raw, {"id", "session_id"})
                identities = [
                    value
                    for value in (fields.get("id"), fields.get("session_id"))
                    if isinstance(value, str) and value.strip()
                ]
                if not identities or len(set(identities)) != 1:
                    raise WorkWindowError("USAGE_RECORD_INVALID")
                rows.append({"record_type": record_type, "identity_value": identities[0]})
            elif record_type == "turn_context":
                fields = _payload_strings(raw, {"session_id", "turn_id", "model", "model_id"})
                if (
                    fields.get("model") is not None
                    and fields.get("model_id") is not None
                    and fields["model"] != fields["model_id"]
                ):
                    raise WorkWindowError("CONFIGURATION_BINDING_MISMATCH")
                model = fields.get("model") if fields.get("model") is not None else fields.get("model_id")
                turn_id = fields.get("turn_id")
                session_id = fields.get("session_id")
                if (
                    not isinstance(model, str) or not model.strip()
                    or not isinstance(turn_id, str) or not turn_id.strip()
                    or (session_id is not None and (not isinstance(session_id, str) or not session_id.strip()))
                ):
                    raise WorkWindowError("USAGE_RECORD_INVALID")
                rows.append({"record_type": record_type, "identity_value": model, "session_id": session_id})
            elif record_type == "response_item":
                item_type = _payload_strings(raw, {"type"}).get("type")
                if not isinstance(item_type, str) or item_type not in CODEX_RESPONSE_ITEM_TYPES:
                    raise WorkWindowError("USAGE_RECORD_INVALID")
            elif record_type in {"compacted", "inter_agent_communication_metadata", "world_state"}:
                # No accepted repository fixture establishes a safe current
                # payload discriminator for these families. Fail closed.
                raise WorkWindowError("USAGE_RECORD_INVALID")
        except WorkWindowError as exc:
            failure = str(exc).split(":", 1)[0]
        except (UnicodeDecodeError, ValueError, TypeError, RecursionError) as exc:
            del exc
            failure = "USAGE_RECORD_INVALID"
    if remaining != 0:
        raise _PendingRead("SOURCE_READ_UNSTABLE")
    return digest.hexdigest(), rows, failure


def _read_identity_and_anchor(handle: Any, path: Path, registration: Mapping[str, Any]) -> None:
    identity = _file_identity(handle, path)
    if identity != registration["source_identity"]:
        raise _TerminalSource("SOURCE_IDENTITY_MISMATCH", end_offset=os.fstat(handle.fileno()).st_size)
    if os.fstat(handle.fileno()).st_size < registration["start_offset_bytes"]:
        raise _TerminalSource("SOURCE_REPLACED_OR_TRUNCATED", end_offset=os.fstat(handle.fileno()).st_size)
    anchor = _anchor_at(handle, registration["start_offset_bytes"])
    if anchor != registration["prefix_anchor"]:
        raise _TerminalSource("SOURCE_REPLACED_OR_TRUNCATED", end_offset=os.fstat(handle.fileno()).st_size)


def _response_digest(identities: list[tuple[str, str]]) -> str:
    canonical = json.dumps(identities, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return _sha(canonical)


def _unavailable_observation(
    registration: Mapping[str, Any],
    *,
    reason: str,
    end_offset: int | None,
    segment_digest: str | None = None,
    response_count: int = 0,
    response_digest: str | None = None,
    thread_id: str | None = None,
    model: str | None = None,
) -> dict[str, Any]:
    window_id = registration["window_id"]
    return {
        "record_type": "resource_observation",
        "schema_version": 1,
        "observation_id": "work-window-observation-v1:" + _sha(window_id.encode("utf-8")),
        "project_id": registration["project_id"],
        "scope": {
            "kind": "WORK_WINDOW", "id": window_id,
            "start_offset_bytes": registration["start_offset_bytes"],
            "end_offset_bytes": end_offset,
        },
        "configuration_ref": registration["configuration_ref"],
        "planning_lite_ref": registration["planning_lite_ref"],
        "configuration_ref_role": CONFIGURATION_REF_ROLE,
        "provider": registration["provider"],
        "model": model if model is not None else registration["model"],
        "measurement_method": "CODEX_LOCAL_ROLLOUT_BOUNDED_JSONL_SEGMENT_V1",
        "native_quantity_semantics": "CODEX_TOKEN_USAGE_RECORD_USAGE_V1",
        "source": {
            "source_ref": registration["source_ref"],
            "membership_rule": registration["membership_rule"],
            "source_identity": registration["source_identity"],
            "prefix_anchor": registration["prefix_anchor"],
            "segment_sha256": segment_digest,
            "unique_response_count": response_count,
            "response_identity_sha256": response_digest or _response_digest([]),
            "thread_id": thread_id,
        },
        "quantities": {},
        "source_completeness": "UNAVAILABLE",
        "metric_completeness": {metric: "UNAVAILABLE" for metric in sorted(RESOURCE_METRICS)},
        "limitations": ["No numeric claim is made."],
        "unavailable_reason": reason,
        "finalized_at_utc": _now(),
    }


def _aggregate(
    registration: Mapping[str, Any], rows: list[dict[str, Any]]
) -> tuple[dict[str, int], dict[str, str], str, str | None, int, str | None]:
    usage_rows = [row for row in rows if "usage" in row]
    context_models = {row["identity_value"] for row in rows if row.get("record_type") == "turn_context"}
    context_sessions = {
        row["identity_value"] for row in rows if row.get("record_type") == "session_meta"
    } | {
        row["session_id"]
        for row in rows
        if row.get("record_type") == "turn_context" and row.get("session_id") is not None
    }
    response_rows: dict[tuple[str, str], dict[str, Any]] = {}
    session_ids: set[str] = set(context_sessions)
    models: set[str] = set(context_models)
    threads: set[str] = set()
    for row in usage_rows:
        key = (row["thread_id"], row["response_id"])
        threads.add(row["thread_id"])
        if row["session_id"] is not None:
            session_ids.add(row["session_id"])
        if row["model"] is not None:
            models.add(row["model"])
        previous = response_rows.get(key)
        if previous is not None:
            if previous["usage"] != row["usage"] or previous["model"] != row["model"]:
                raise WorkWindowError("DUPLICATE_USAGE_CONFLICT")
            continue
        response_rows[key] = row
    if len(threads) > 1 or len(session_ids) > 1:
        raise WorkWindowError("MEMBERSHIP_BINDING_MISMATCH")
    if len(models) > 1:
        raise WorkWindowError("CONFIGURATION_BINDING_MISMATCH")
    model = next(iter(models), registration["model"])
    if registration["model"] is not None and model is not None and registration["model"] != model:
        raise WorkWindowError("CONFIGURATION_BINDING_MISMATCH")
    if not response_rows:
        raise WorkWindowError("REQUIRED_USAGE_MISSING")
    for row in response_rows.values():
        usage = row["usage"]
        if "cached_input_tokens" in usage and "input_tokens" in usage and usage["cached_input_tokens"] > usage["input_tokens"]:
            raise WorkWindowError("AGGREGATE_RECONCILIATION_FAILED")
        if {"input_tokens", "output_tokens", "total_tokens"} <= set(usage) and usage["total_tokens"] != usage["input_tokens"] + usage["output_tokens"]:
            raise WorkWindowError("AGGREGATE_RECONCILIATION_FAILED")
        if "reasoning_output_tokens" in usage and "output_tokens" in usage and usage["reasoning_output_tokens"] > usage["output_tokens"]:
            raise WorkWindowError("AGGREGATE_RECONCILIATION_FAILED")
    unique_rows = list(response_rows.values())
    metrics: dict[str, int] = {}
    completeness: dict[str, str] = {}
    for metric in sorted(RESOURCE_METRICS):
        present = [row["usage"][metric] for row in unique_rows if metric in row["usage"]]
        if len(present) == len(unique_rows):
            metrics[metric] = sum(present)
            completeness[metric] = "COMPLETE"
        elif present:
            completeness[metric] = "PARTIAL"
        else:
            completeness[metric] = "ABSENT"
    if not metrics:
        raise WorkWindowError("REQUIRED_USAGE_MISSING")
    identities = sorted(response_rows)
    thread_id = next(iter(threads)) if threads else None
    return metrics, completeness, model if isinstance(model, str) else None, thread_id, len(identities), _response_digest(identities)


def _final_observation(
    registration: Mapping[str, Any],
    *,
    end_offset: int,
    segment_digest: str,
    rows: list[dict[str, Any]],
) -> dict[str, Any]:
    metrics, completeness, model, thread_id, response_count, response_digest = _aggregate(registration, rows)
    absent = sorted(metric for metric, state in completeness.items() if state != "COMPLETE")
    return {
        "record_type": "resource_observation",
        "schema_version": 1,
        "observation_id": "work-window-observation-v1:" + _sha(registration["window_id"].encode("utf-8")),
        "project_id": registration["project_id"],
        "scope": {
            "kind": "WORK_WINDOW", "id": registration["window_id"],
            "start_offset_bytes": registration["start_offset_bytes"],
            "end_offset_bytes": end_offset,
        },
        "configuration_ref": registration["configuration_ref"],
        "planning_lite_ref": registration["planning_lite_ref"],
        "configuration_ref_role": CONFIGURATION_REF_ROLE,
        "provider": registration["provider"],
        "model": model if model is not None else registration["model"],
        "measurement_method": "CODEX_LOCAL_ROLLOUT_BOUNDED_JSONL_SEGMENT_V1",
        "native_quantity_semantics": "CODEX_TOKEN_USAGE_RECORD_USAGE_V1",
        "source": {
            "source_ref": registration["source_ref"],
            "membership_rule": registration["membership_rule"],
            "source_identity": registration["source_identity"],
            "prefix_anchor": registration["prefix_anchor"],
            "segment_sha256": segment_digest,
            "unique_response_count": response_count,
            "response_identity_sha256": response_digest,
            "thread_id": thread_id,
        },
        "quantities": {
            metric: {
                "value": value,
                "quality": "DIRECT",
                "numeric_claim_kind": "COMPLETE_SCOPE_TOTAL",
            }
            for metric, value in sorted(metrics.items())
        },
        "source_completeness": "COMPLETE",
        "metric_completeness": completeness,
        "limitations": ["Optional or partially present provider-native metrics are not reported as totals: " + ", ".join(absent)] if absent else [],
        "unavailable_reason": None,
        "finalized_at_utc": _now(),
    }


def _capture_segment(registration: Mapping[str, Any]) -> tuple[str, int, list[dict[str, Any]]]:
    path = Path(registration["source_ref"])
    try:
        handle = path.open("rb")
    except FileNotFoundError as exc:
        raise _TerminalSource("SOURCE_NOT_FOUND") from exc
    except OSError as exc:
        raise _PendingRead("SOURCE_READ_UNSTABLE") from exc
    with handle:
        _read_identity_and_anchor(handle, path, registration)
        handle.seek(0, os.SEEK_END)
        end_offset = handle.tell()
        start = registration["start_offset_bytes"]
        if end_offset < start:
            raise _TerminalSource("SOURCE_REPLACED_OR_TRUNCATED", end_offset=end_offset)
        if end_offset:
            handle.seek(end_offset - 1)
            if handle.read(1) != b"\n":
                raise _PendingRead("SOURCE_READ_UNSTABLE")
        if end_offset == start:
            return _sha(b""), end_offset, []
        for attempt in range(2):
            try:
                _read_identity_and_anchor(handle, path, registration)
                if os.fstat(handle.fileno()).st_size < end_offset:
                    raise _TerminalSource("SOURCE_REPLACED_OR_TRUNCATED", end_offset=end_offset)
                first_digest, rows, parse_failure = _read_bounded(
                    handle, start_offset=start, end_offset=end_offset, parse=True
                )
                second_digest, _ignored, _failure = _read_bounded(
                    handle, start_offset=start, end_offset=end_offset, parse=False
                )
                _read_identity_and_anchor(handle, path, registration)
                if os.fstat(handle.fileno()).st_size < end_offset:
                    raise _TerminalSource("SOURCE_REPLACED_OR_TRUNCATED", end_offset=end_offset)
                if first_digest == second_digest:
                    if parse_failure:
                        raise _StableSegmentFailure(
                            parse_failure, end_offset=end_offset, segment_digest=first_digest
                        )
                    return first_digest, end_offset, rows
            except _TerminalSource:
                raise
            except _PendingRead:
                if attempt == 1:
                    raise
                continue
            except WorkWindowError:
                raise
            except OSError as exc:
                if os.fstat(handle.fileno()).st_size < end_offset:
                    raise _TerminalSource("SOURCE_REPLACED_OR_TRUNCATED", end_offset=end_offset) from exc
            if attempt == 1:
                raise _PendingRead("SOURCE_READ_UNSTABLE")
        raise _PendingRead("SOURCE_READ_UNSTABLE")


def finalize_work_window(
    window_id: str, *, receipt_path: str | Path, registered_project_id: str
) -> dict[str, Any]:
    """Finalize exactly one previously registered byte interval."""

    prior = read_resource_observation_for_window(
        window_id, receipt_path=receipt_path, registered_project_id=registered_project_id
    )
    if prior is not None:
        return prior
    registration = read_work_window_registration(
        window_id, receipt_path=receipt_path, registered_project_id=registered_project_id
    )
    try:
        segment_digest, end_offset, rows = _capture_segment(registration)
        if end_offset == registration["start_offset_bytes"]:
            observation = _unavailable_observation(
                registration, reason="REQUIRED_USAGE_MISSING", end_offset=end_offset,
                segment_digest=segment_digest,
            )
        else:
            try:
                observation = _final_observation(
                    registration, end_offset=end_offset, segment_digest=segment_digest, rows=rows
                )
            except WorkWindowError as exc:
                observation = _unavailable_observation(
                    registration, reason=str(exc).split(":", 1)[0], end_offset=end_offset,
                    segment_digest=segment_digest,
                )
    except _PendingRead as exc:
        return {"status": "REQUEST_NOT_YET_FINALIZABLE", "reason": str(exc).split(":", 1)[0], "window_id": window_id}
    except _TerminalSource as exc:
        observation = _unavailable_observation(
            registration, reason=exc.reason, end_offset=exc.end_offset,
        )
    except _StableSegmentFailure as exc:
        observation = _unavailable_observation(
            registration, reason=exc.reason, end_offset=exc.end_offset,
            segment_digest=exc.segment_digest,
        )
    except WorkWindowError as exc:
        reason = str(exc).split(":", 1)[0]
        if reason not in {
            "SOURCE_NOT_FOUND", "SOURCE_IDENTITY_MISMATCH", "SOURCE_REPLACED_OR_TRUNCATED",
            "SOURCE_READ_UNSTABLE", "MEMBERSHIP_BINDING_MISMATCH", "CONFIGURATION_BINDING_MISMATCH",
            "USAGE_RECORD_INVALID", "DUPLICATE_USAGE_CONFLICT", "REQUIRED_USAGE_MISSING",
            "AGGREGATE_RECONCILIATION_FAILED",
        }:
            reason = "USAGE_RECORD_INVALID"
        observation = _unavailable_observation(registration, reason=reason, end_offset=None)
    return append_resource_observation(
        observation, receipt_path=receipt_path, registered_project_id=registered_project_id
    )
