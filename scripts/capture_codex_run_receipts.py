"""Capture explicitly bound Codex rollout metadata as RunReceipt v1 records.

This is a central-maintainer command, deliberately separate from the
``planning-lite`` CLI.  It accepts exact operation and host bindings, reads
only structured rollout metadata, and delegates receipt validation,
canonicalization, and append ownership to :mod:`planning_lite.telemetry`.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Iterable, Mapping

from planning_lite.telemetry import (
    ReceiptError,
    append_receipt,
    canonical_bytes,
    scan_telemetry_records,
    validate_receipt,
)


PROJECT_ID = "planning-lite-central"
RUNTIME_SOURCE = "codex_rollout_jsonl_v1"
RECEIPT_ID_SCHEMA = "planning-lite-codex-receipt-id-v1"
RECEIPT_ID_PREFIX = "codex-run-v1:"
HEX_SHA_RE = re.compile(r"^[0-9a-f]{40}$")
CONTENT_TOP_LEVEL_TYPES = {
    "compacted",
    "response_item",
    "inter_agent_communication_metadata",
    "world_state",
}
SUPPORTED_TOP_LEVEL_TYPES = {"session_meta", "turn_context", "event_msg", "token_usage_record"} | CONTENT_TOP_LEVEL_TYPES
TOKEN_EVENT_TYPES = {"token_count"}
COMPLETION_EVENT_TYPES = {"task_complete"}


class CaptureError(ReceiptError):
    """Fail-closed capture error with a stable class in CLI diagnostics."""


@dataclass(frozen=True)
class Binding:
    repo_root: Path
    expected_head: str
    project_id: str
    change_id: str | None
    task_id: str
    run_family: str
    outcome: str
    parent_rollout: Path
    parent_session_id: str
    parent_turn_id: str
    children: tuple["ChildBinding", ...]

    @property
    def receipt_path(self) -> Path:
        root = self.repo_root.expanduser().resolve()
        return (
            root
            / ".local"
            / "state"
            / "projects"
            / PROJECT_ID
            / "telemetry"
            / "run-receipts.jsonl"
        )


@dataclass(frozen=True)
class ChildBinding:
    rollout: Path
    session_id: str
    turn_id: str
    invocation_index: int


@dataclass(frozen=True)
class InvocationFacts:
    session_id: str
    turn_id: str
    model_id: str
    reasoning_effort: str | None
    terminal_timestamp: str
    tokens: Mapping[str, int]
    parent_session_id: str | None
    parent_turn_id: str | None


@dataclass(frozen=True)
class ExistingRecord:
    receipt: dict[str, Any]
    payload: bytes


def _failure(failure_class: str, path: Path | None = None, ordinal: int | None = None, detail: str = "") -> CaptureError:
    location = ""
    if path is not None:
        location = f" file={path}"
    if ordinal is not None:
        location += f" record={ordinal}"
    suffix = f": {detail}" if detail else ""
    return CaptureError(f"{failure_class}{location}{suffix}")


def _skip_ws(raw: str, index: int) -> int:
    while index < len(raw) and raw[index] in " \t\r\n":
        index += 1
    return index


def _scan_string(raw: str, index: int) -> tuple[str, int]:
    """Decode one JSON string only; never decode an enclosing content value."""

    if index >= len(raw) or raw[index] != '"':
        raise ValueError("expected JSON string")
    decoder = json.JSONDecoder()
    value, end = decoder.raw_decode(raw, index)
    if not isinstance(value, str):
        raise ValueError("expected JSON string")
    return value, end


def _skip_string(raw: str, index: int) -> int:
    if index >= len(raw) or raw[index] != '"':
        raise ValueError("expected string")
    index += 1
    escaped = False
    while index < len(raw):
        char = raw[index]
        if escaped:
            escaped = False
        elif char == "\\":
            escaped = True
        elif char == '"':
            return index + 1
        index += 1
    raise ValueError("unterminated string")


def _skip_value(raw: str, index: int) -> int:
    """Skip a JSON value without materializing it (privacy boundary)."""

    index = _skip_ws(raw, index)
    if index >= len(raw):
        raise ValueError("missing value")
    if raw[index] == '"':
        return _skip_string(raw, index)
    if raw[index] in "[{":
        opening = raw[index]
        closing = "]" if opening == "[" else "}"
        depth = 0
        in_string = False
        escaped = False
        for position in range(index, len(raw)):
            char = raw[position]
            if in_string:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    in_string = False
                continue
            if char == '"':
                in_string = True
            elif char == opening:
                depth += 1
            elif char == closing:
                depth -= 1
                if depth == 0:
                    return position + 1
        raise ValueError("unterminated composite value")
    position = index
    while position < len(raw) and raw[position] not in ",}] \t\r\n":
        position += 1
    if position == index:
        raise ValueError("invalid value")
    return position


def _object_field_start(raw: str, object_start: int, field: str) -> int | None:
    """Return the value start for a direct object field, without decoding others."""

    index = _skip_ws(raw, object_start)
    if index >= len(raw) or raw[index] != "{":
        raise ValueError("expected object")
    index += 1
    while True:
        index = _skip_ws(raw, index)
        if index >= len(raw):
            raise ValueError("unterminated object")
        if raw[index] == "}":
            return None
        key, index = _scan_string(raw, index)
        index = _skip_ws(raw, index)
        if index >= len(raw) or raw[index] != ":":
            raise ValueError("missing object colon")
        index = _skip_ws(raw, index + 1)
        value_start = index
        value_end = _skip_value(raw, value_start)
        if key == field:
            return value_start
        index = _skip_ws(raw, value_end)
        if index >= len(raw):
            raise ValueError("unterminated object")
        if raw[index] == "}":
            return None
        if raw[index] != ",":
            raise ValueError("missing object comma")
        index += 1


def _raw_top_level_type(raw: str) -> str:
    index = _skip_ws(raw, 0)
    if index >= len(raw) or raw[index] != "{":
        raise ValueError("expected top-level object")
    index += 1
    while True:
        index = _skip_ws(raw, index)
        if index >= len(raw) or raw[index] == "}":
            raise ValueError("missing top-level type discriminator")
        key, index = _scan_string(raw, index)
        index = _skip_ws(raw, index)
        if index >= len(raw) or raw[index] != ":":
            raise ValueError("missing object colon")
        value_start = _skip_ws(raw, index + 1)
        if key == "payload":
            raise ValueError("payload precedes top-level discriminator")
        if key == "type":
            value, _ = _scan_string(raw, value_start)
            return value
        index = _skip_ws(raw, _skip_value(raw, value_start))
        if index >= len(raw) or raw[index] != ",":
            raise ValueError("missing object comma before discriminator")
        index += 1


def _raw_payload_type(raw: str) -> str | None:
    payload_start = _object_field_start(raw, 0, "payload")
    if payload_start is None:
        return None
    index = _skip_ws(raw, payload_start)
    if index >= len(raw) or raw[index] != "{":
        raise ValueError("payload is not an object")
    index = _skip_ws(raw, index + 1)
    if index >= len(raw) or raw[index] == "}":
        return None
    key, index = _scan_string(raw, index)
    index = _skip_ws(raw, index)
    if index >= len(raw) or raw[index] != ":":
        raise ValueError("missing payload colon")
    if key != "type":
        raise ValueError("payload discriminator is not first")
    value, _ = _scan_string(raw, _skip_ws(raw, index + 1))
    return value


def _raw_string_field(raw: str, object_start: int, field: str) -> str | None:
    value_start = _object_field_start(raw, object_start, field)
    if value_start is None:
        return None
    value, _ = _scan_string(raw, value_start)
    return value


def _safe_metadata_json(raw: str, path: Path, ordinal: int) -> dict[str, Any]:
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise _failure("INVALID_METADATA_JSON", path, ordinal, "metadata record is not valid JSON") from exc
    if not isinstance(value, dict):
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "metadata record is not an object")
    return value


def _metadata_prefix_fields(
    raw: str,
    path: Path,
    ordinal: int,
    *,
    wanted: set[str],
    content_boundaries: set[str],
) -> dict[str, str | None]:
    """Read allowlisted scalar payload fields without decoding content tails."""

    try:
        payload_start = _object_field_start(raw, 0, "payload")
        if payload_start is None:
            raise ValueError("missing payload")
        index = _skip_ws(raw, payload_start)
        if index >= len(raw) or raw[index] != "{":
            raise ValueError("payload is not an object")
        index += 1
        values: dict[str, str | None] = {}
        while True:
            index = _skip_ws(raw, index)
            if index >= len(raw):
                raise ValueError("unterminated payload")
            if raw[index] == "}":
                return values
            key, index = _scan_string(raw, index)
            index = _skip_ws(raw, index)
            if index >= len(raw) or raw[index] != ":":
                raise ValueError("missing payload colon")
            value_start = _skip_ws(raw, index + 1)
            if key in content_boundaries:
                return values
            value_end = _skip_value(raw, value_start)
            if key in wanted:
                if raw.startswith("null", value_start):
                    values[key] = None
                else:
                    value, decoded_end = _scan_string(raw, value_start)
                    if decoded_end != value_end:
                        raise ValueError("bound field is not a string or null")
                    values[key] = value
            index = _skip_ws(raw, value_end)
            if index >= len(raw):
                raise ValueError("unterminated payload")
            if raw[index] == "}":
                return values
            if raw[index] != ",":
                raise ValueError("missing payload comma")
            index += 1
    except ValueError as exc:
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "safe metadata prefix is unavailable") from exc


def _safe_session_metadata(raw: str, path: Path, ordinal: int) -> dict[str, Any]:
    fields = _metadata_prefix_fields(
        raw,
        path,
        ordinal,
        wanted={"id", "session_id", "parent_thread_id", "parent_session_id"},
        content_boundaries={"base_instructions", "developer_instructions", "user_instructions", "dynamic_tools"},
    )
    try:
        timestamp = _raw_string_field(raw, 0, "timestamp")
    except ValueError as exc:
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "session timestamp is unavailable") from exc
    return {"timestamp": timestamp, "payload": fields}


def _safe_turn_metadata(raw: str, path: Path, ordinal: int) -> dict[str, Any]:
    fields = _metadata_prefix_fields(
        raw,
        path,
        ordinal,
        wanted={
            "turn_id",
            "model",
            "model_id",
            "effort",
            "reasoning_effort",
            "root_turn_id",
            "parent_turn_id",
            "session_id",
            "parent_session_id",
        },
        content_boundaries={"summary"},
    )
    try:
        timestamp = _raw_string_field(raw, 0, "timestamp")
    except ValueError as exc:
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "turn timestamp is unavailable") from exc
    return {"timestamp": timestamp, "payload": fields}


def _safe_completion_metadata(raw: str, path: Path, ordinal: int, event_type: str) -> dict[str, Any]:
    """Retain only completion metadata before the opaque message body."""

    try:
        timestamp = _raw_string_field(raw, 0, "timestamp")
        payload_start = _object_field_start(raw, 0, "payload")
        turn_id = None if payload_start is None else _raw_string_field(raw, payload_start, "turn_id")
    except ValueError as exc:
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "completion metadata is unavailable") from exc
    return {"timestamp": timestamp, "payload": {"type": event_type, "turn_id": turn_id}}


def _metadata_event_type(raw: str, path: Path, ordinal: int) -> str | None:
    try:
        return _raw_payload_type(raw)
    except ValueError as exc:
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "event discriminator is unavailable") from exc


def _record_type_and_metadata(raw: str, path: Path, ordinal: int) -> tuple[str, dict[str, Any] | None, str | None]:
    """Classify a raw line; only allowlisted metadata records are decoded."""

    try:
        record_type = _raw_top_level_type(raw)
    except ValueError as exc:
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "top-level discriminator is unavailable") from exc
    if record_type not in SUPPORTED_TOP_LEVEL_TYPES:
        raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "unsupported top-level discriminator")
    if record_type in CONTENT_TOP_LEVEL_TYPES:
        return record_type, None, None
    if record_type == "token_usage_record":
        # The current host shape is a content-adjacent accounting envelope.
        # The authoritative cumulative counter remains event_msg/token_count.
        return record_type, None, None
    if record_type == "session_meta":
        return record_type, _safe_session_metadata(raw, path, ordinal), None
    if record_type == "turn_context":
        return record_type, _safe_turn_metadata(raw, path, ordinal), None
    if record_type == "event_msg":
        event_type = _metadata_event_type(raw, path, ordinal)
        if event_type not in TOKEN_EVENT_TYPES | COMPLETION_EVENT_TYPES:
            # event_msg is a known host envelope.  Unknown/content event
            # payloads remain opaque and are never JSON-decoded.
            return record_type, None, event_type
        if event_type in COMPLETION_EVENT_TYPES:
            return record_type, _safe_completion_metadata(raw, path, ordinal, event_type), event_type
        return record_type, _safe_metadata_json(raw, path, ordinal), event_type
    return record_type, _safe_metadata_json(raw, path, ordinal), None


def _read_rollout(path: Path) -> list[tuple[int, str, dict[str, Any] | None, str | None]]:
    try:
        handle = path.open("r", encoding="utf-8")
    except OSError as exc:
        raise _failure("ROLLOUT_READ_FAILED", path, detail="cannot read rollout") from exc
    rows: list[tuple[int, str, dict[str, Any] | None, str | None]] = []
    with handle:
        for ordinal, line in enumerate(handle, start=1):
            raw = line.rstrip("\r\n")
            if not raw.strip():
                raise _failure("UNSUPPORTED_HOST_RECORD_SHAPE", path, ordinal, "blank record")
            record_type, metadata, nested_type = _record_type_and_metadata(raw, path, ordinal)
            rows.append((ordinal, record_type, metadata, nested_type))
    return rows


def _text(value: Any, field: str, path: Path, ordinal: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _failure("IDENTITY_AMBIGUITY", path, ordinal, f"{field} must be a non-empty string")
    return value


def _optional_text(value: Any, field: str, path: Path, ordinal: int) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise _failure("IDENTITY_AMBIGUITY", path, ordinal, f"{field} must be a string or null")
    return value


def _timestamp(value: Any, path: Path, ordinal: int) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _failure("INVALID_TIMESTAMP", path, ordinal, "timestamp must be aware ISO-8601")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise _failure("INVALID_TIMESTAMP", path, ordinal, "timestamp must be aware ISO-8601") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise _failure("INVALID_TIMESTAMP", path, ordinal, "timestamp must be timezone-aware")
    utc = parsed.astimezone(timezone.utc)
    return utc.strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def _usage(info: Any, path: Path, ordinal: int) -> Mapping[str, Any]:
    if not isinstance(info, Mapping):
        raise _failure("INVALID_TOKEN_RECORD", path, ordinal, "token usage info must be an object")
    usage = info.get("total_token_usage", info.get("token_usage"))
    if not isinstance(usage, Mapping):
        raise _failure("INVALID_TOKEN_RECORD", path, ordinal, "total_token_usage must be an object")
    aliases = {
        "input": "input_tokens",
        "output": "output_tokens",
        "cached": "cached_input_tokens",
        "reasoning": "reasoning_output_tokens",
        "total": "total_tokens",
    }
    values: dict[str, int] = {}
    for target, source in aliases.items():
        value = usage.get(source)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise _failure("INVALID_TOKEN_RECORD", path, ordinal, f"{source} must be a non-negative integer")
        values[target] = value
    if values["cached"] > values["input"]:
        raise _failure("INVALID_TOKEN_RECORD", path, ordinal, "cached input exceeds input")
    return values


def _field(mapping: Mapping[str, Any], *names: str) -> Any:
    for name in names:
        if name in mapping:
            return mapping[name]
    return None


def _extract_session(meta: Mapping[str, Any], path: Path, ordinal: int) -> tuple[str, str | None]:
    payload = meta.get("payload")
    if not isinstance(payload, Mapping):
        raise _failure("IDENTITY_AMBIGUITY", path, ordinal, "session_meta payload must be an object")
    # ``id`` is the rollout/thread identity.  In a spawned host session the
    # legacy ``session_id`` field can refer to the root/parent session.
    session_id = _field(payload, "id", "session_id")
    return _text(session_id, "session_id", path, ordinal), _optional_text(
        _field(payload, "parent_thread_id", "parent_session_id"), "parent_thread_id", path, ordinal
    )


def _extract_turn(meta: Mapping[str, Any], path: Path, ordinal: int) -> tuple[str, str, str | None, str | None, str | None, str | None]:
    payload = meta.get("payload")
    if not isinstance(payload, Mapping):
        raise _failure("IDENTITY_AMBIGUITY", path, ordinal, "turn_context payload must be an object")
    turn_id = _text(payload.get("turn_id"), "turn_id", path, ordinal)
    model = _text(_field(payload, "model", "model_id"), "model", path, ordinal)
    effort = _optional_text(_field(payload, "reasoning_effort", "effort"), "reasoning_effort", path, ordinal)
    root_turn = _optional_text(_field(payload, "root_turn_id", "parent_turn_id"), "root_turn_id", path, ordinal)
    session_id = _optional_text(payload.get("session_id"), "session_id", path, ordinal)
    parent_session = _optional_text(payload.get("parent_session_id"), "parent_session_id", path, ordinal)
    return turn_id, model, effort, root_turn, session_id, parent_session


def parse_rollout(
    path: str | Path,
    *,
    expected_session_id: str,
    expected_turn_id: str,
    expected_parent_session_id: str | None = None,
    expected_parent_turn_id: str | None = None,
    require_direct_parent: bool = False,
) -> InvocationFacts:
    """Parse exactly one bound invocation from a metadata-only rollout."""

    rollout = Path(path).expanduser().resolve()
    rows = _read_rollout(rollout)
    session_matches: list[tuple[str, str | None, int]] = []
    turn_matches: list[tuple[str, str, str | None, str | None, str | None, str | None, int, str]] = []
    current_turn: str | None = None
    counters: list[tuple[int, str, Mapping[str, int]]] = []
    completions: list[tuple[int, str | None, str]] = []
    seen_after_completion = False
    for ordinal, record_type, metadata, nested_type in rows:
        if record_type == "session_meta" and metadata is not None:
            session_id, parent_session = _extract_session(metadata, rollout, ordinal)
            if session_id == expected_session_id:
                session_matches.append((session_id, parent_session, ordinal))
        elif record_type == "turn_context" and metadata is not None:
            turn_id, model, effort, root_turn, session_id, parent_session = _extract_turn(metadata, rollout, ordinal)
            current_turn = turn_id
            if turn_id == expected_turn_id:
                timestamp = _timestamp(metadata.get("timestamp"), rollout, ordinal)
                turn_matches.append((turn_id, model, effort, root_turn, session_id, parent_session, ordinal, timestamp))
        elif record_type == "event_msg" and metadata is not None and nested_type in TOKEN_EVENT_TYPES | COMPLETION_EVENT_TYPES:
            payload = metadata.get("payload")
            if not isinstance(payload, Mapping):
                raise _failure("INVALID_METADATA_JSON", rollout, ordinal, "event payload must be an object")
            event_turn = _optional_text(payload.get("turn_id"), "turn_id", rollout, ordinal)
            if nested_type in TOKEN_EVENT_TYPES:
                if event_turn is not None and event_turn != expected_turn_id:
                    continue
                if event_turn is None and current_turn != expected_turn_id:
                    continue
                if seen_after_completion:
                    raise _failure("COUNTER_AFTER_COMPLETION", rollout, ordinal)
                info = payload.get("info")
                counters.append((ordinal, _timestamp(metadata.get("timestamp"), rollout, ordinal), _usage(info, rollout, ordinal)))
            elif (event_turn is None and current_turn == expected_turn_id) or event_turn == expected_turn_id:
                if completions:
                    raise _failure("MULTIPLE_COMPLETIONS", rollout, ordinal)
                completions.append((ordinal, event_turn, _timestamp(metadata.get("timestamp"), rollout, ordinal)))
                seen_after_completion = True
    semantic_sessions = {
        (session_id, parent_session)
        for session_id, parent_session, _ in session_matches
    }
    if len(semantic_sessions) != 1:
        raise _failure("IDENTITY_AMBIGUITY", rollout, detail="expected exactly one matching session identity")
    semantic_turns = {
        (turn_id, model, effort, root_turn, session_id, parent_session)
        for turn_id, model, effort, root_turn, session_id, parent_session, _, _ in turn_matches
    }
    if len(semantic_turns) != 1:
        raise _failure("IDENTITY_AMBIGUITY", rollout, detail="expected exactly one matching turn identity")
    if len(completions) != 1:
        raise _failure("MISSING_COMPLETION" if not completions else "MULTIPLE_COMPLETIONS", rollout)
    if not counters:
        raise _failure("MISSING_FINAL_COUNTER", rollout)
    turn_id, model, effort, root_turn, turn_session, turn_parent_session, _, _ = turn_matches[0]
    session_id, session_parent, _ = session_matches[0]
    if turn_session is not None and turn_session != session_id:
        raise _failure("IDENTITY_AMBIGUITY", rollout, detail="turn/session identity conflict")
    parent_session = session_parent or turn_parent_session
    parent_turn = root_turn
    if require_direct_parent:
        linked_session = parent_session == expected_parent_session_id
        linked_turn = parent_turn == expected_parent_turn_id
        if not (linked_session or linked_turn):
            raise _failure("UNLINKED_CHILD", rollout)
        if parent_session is not None and parent_session != expected_parent_session_id:
            raise _failure("UNLINKED_CHILD", rollout)
        if parent_turn is not None and parent_turn != expected_parent_turn_id:
            raise _failure("UNLINKED_CHILD", rollout)
    _, terminal_timestamp, terminal_tokens = counters[-1]
    if any(counter_ordinal > completions[0][0] for counter_ordinal, _, _ in counters):
        raise _failure("COUNTER_AFTER_COMPLETION", rollout)
    return InvocationFacts(
        session_id=session_id,
        turn_id=turn_id,
        model_id=model,
        reasoning_effort=effort,
        terminal_timestamp=terminal_timestamp,
        tokens=terminal_tokens,
        parent_session_id=parent_session,
        parent_turn_id=parent_turn,
    )


def receipt_identity(
    *,
    agent_role: str,
    change_id: str | None,
    host_session_id: str,
    host_turn_id: str,
    invocation_index: int,
    planning_lite_ref: str,
    project_id: str,
    run_family: str,
    task_id: str,
) -> dict[str, Any]:
    return {
        "agent_role": agent_role,
        "change_id": change_id,
        "host_session_id": host_session_id,
        "host_turn_id": host_turn_id,
        "invocation_index": invocation_index,
        "planning_lite_ref": planning_lite_ref,
        "project_id": project_id,
        "run_family": run_family,
        "schema": RECEIPT_ID_SCHEMA,
        "task_id": task_id,
    }


def make_receipt_id(**kwargs: Any) -> str:
    raw = json.dumps(receipt_identity(**kwargs), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return RECEIPT_ID_PREFIX + hashlib.sha256(raw).hexdigest()


def _make_receipt(binding: Binding, facts: InvocationFacts, *, role: str, invocation_index: int) -> dict[str, Any]:
    receipt = {
        "schema_version": 1,
        "receipt_id": make_receipt_id(
            agent_role=role,
            change_id=binding.change_id,
            host_session_id=facts.session_id,
            host_turn_id=facts.turn_id,
            invocation_index=invocation_index,
            planning_lite_ref=binding.expected_head,
            project_id=binding.project_id,
            run_family=binding.run_family,
            task_id=binding.task_id,
        ),
        "occurred_at_utc": facts.terminal_timestamp,
        "project_id": binding.project_id,
        "planning_lite_ref": binding.expected_head,
        "change_id": binding.change_id,
        "task_id": binding.task_id,
        "run_family": binding.run_family,
        "agent_role": role,
        "model_id": facts.model_id,
        "model_tier": None,
        "invocation_index": invocation_index,
        "outcome": binding.outcome,
        "tokens": {
            "input": facts.tokens["input"],
            "output": facts.tokens["output"],
            "cached": facts.tokens["cached"],
            "reasoning": facts.tokens["reasoning"],
            "total": facts.tokens["total"],
            "source": "external_runtime",
        },
        "verifier_used": None,
        "reviewer_used": None,
        "model_escalation": None,
        "retry": None,
        "recheck": None,
        "reads": {"planning": None, "non_planning": None, "source": "unavailable"},
        "runtime_source": RUNTIME_SOURCE,
    }
    try:
        return validate_receipt(
            receipt,
            registered_project_id=binding.project_id,
            planning_lite_ref=binding.expected_head,
        )
    except ReceiptError as exc:
        raise CaptureError(f"INVALID_RUNRECEIPT_MAPPING: {exc}") from exc


def _verify_repository(repo_root: Path, expected_head: str) -> Path:
    if not HEX_SHA_RE.fullmatch(expected_head):
        raise _failure("HEAD_MISMATCH", detail="expected HEAD must be a lowercase 40-character SHA")
    resolved = repo_root.expanduser().resolve()
    try:
        top = subprocess.run(
            ["git", "-C", str(resolved), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        actual_root = Path(top).resolve()
        actual_head = subprocess.run(
            ["git", "-C", str(resolved), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise _failure("HEAD_MISMATCH", detail="repo-root is not a readable Git repository") from exc
    if actual_root != resolved or actual_head != expected_head:
        raise _failure("HEAD_MISMATCH", detail="repo root or HEAD does not match explicit binding")
    return resolved


def _parse_index(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise CaptureError("INVALID_BINDING: invocation index must be a non-negative integer") from exc
    if parsed < 0:
        raise CaptureError("INVALID_BINDING: invocation index must be a non-negative integer")
    return parsed


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--project-id", required=True)
    change = parser.add_mutually_exclusive_group(required=True)
    change.add_argument("--change-id")
    change.add_argument("--null-change-id", action="store_true")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--run-family", required=True)
    parser.add_argument("--outcome", required=True, choices=("PASS", "FAIL", "BLOCKED", "CANCELLED", "UNKNOWN"))
    parser.add_argument("--parent-rollout", required=True)
    parser.add_argument("--parent-session-id", required=True)
    parser.add_argument("--parent-turn-id", required=True)
    parser.add_argument("--child", action="append", nargs=4, metavar=("ROLLOUT", "SESSION_ID", "TURN_ID", "INDEX"))
    return parser


def parse_args(argv: Iterable[str] | None = None) -> Binding:
    args = _parser().parse_args(list(argv) if argv is not None else None)
    if args.project_id != PROJECT_ID:
        raise _failure("PROJECT_ID_MISMATCH", detail=f"project_id must be {PROJECT_ID}")
    if not args.task_id.strip() or not args.run_family.strip() or not args.parent_session_id.strip() or not args.parent_turn_id.strip():
        raise _failure("INVALID_BINDING", detail="task, run, parent session, and parent turn are required")
    child_args = args.child or []
    children: list[ChildBinding] = []
    indices: set[int] = set()
    for values in child_args:
        rollout, session_id, turn_id, index_value = values
        index = _parse_index(index_value)
        if index in indices:
            raise _failure("DUPLICATE_CHILD_INDEX", detail=f"invocation_index={index}")
        indices.add(index)
        children.append(ChildBinding(Path(rollout), session_id, turn_id, index))
    return Binding(
        repo_root=Path(args.repo_root),
        expected_head=args.expected_head,
        project_id=args.project_id,
        change_id=None if args.null_change_id else args.change_id,
        task_id=args.task_id,
        run_family=args.run_family,
        outcome=args.outcome,
        parent_rollout=Path(args.parent_rollout),
        parent_session_id=args.parent_session_id,
        parent_turn_id=args.parent_turn_id,
        children=tuple(children),
    )


def _read_existing(path: Path, binding: Binding) -> dict[str, ExistingRecord]:
    try:
        families = scan_telemetry_records(path, registered_project_id=binding.project_id)
    except OSError as exc:
        raise _failure("RECEIPT_STREAM_READ_FAILED", path=path) from exc
    except ReceiptError as exc:
        raise _failure("RECEIPT_STREAM_INVALID", path=path, detail="invalid telemetry record") from exc
    records: dict[str, ExistingRecord] = {}
    for validated in families["run_receipts"].values():
        try:
            stored_ref = validated.get("planning_lite_ref")
            if not isinstance(stored_ref, str) or not stored_ref.strip():
                raise ReceiptError("planning_lite_ref must be a non-empty stored string")
            validated = validate_receipt(
                validated,
                registered_project_id=binding.project_id,
                planning_lite_ref=stored_ref,
            )
        except ReceiptError as exc:
            raise _failure("RECEIPT_STREAM_INVALID", path=path, detail="invalid RunReceipt") from exc
        receipt_id = validated["receipt_id"]
        if receipt_id in records:
            raise _failure("RECEIPT_STREAM_INVALID", path=path, detail="duplicate receipt_id")
        records[receipt_id] = ExistingRecord(validated, canonical_bytes(validated))
    return records


def capture(binding: Binding) -> dict[str, Any]:
    """Capture the explicit operation and return the structured summary."""

    # This guard intentionally precedes rollout reads and receipt-directory
    # creation.  A stale root cannot inspect metadata or leave state behind.
    root = _verify_repository(binding.repo_root, binding.expected_head)
    parent_path = binding.parent_rollout.expanduser().resolve()
    parent = parse_rollout(parent_path, expected_session_id=binding.parent_session_id, expected_turn_id=binding.parent_turn_id)
    candidates: list[tuple[str, int, Path, InvocationFacts, dict[str, Any]]] = []
    parent_receipt = _make_receipt(binding, parent, role="PARENT", invocation_index=0)
    candidates.append(("PARENT", 0, parent_path, parent, parent_receipt))
    for child in binding.children:
        child_path = child.rollout.expanduser().resolve()
        child_facts = parse_rollout(
            child_path,
            expected_session_id=child.session_id,
            expected_turn_id=child.turn_id,
            expected_parent_session_id=binding.parent_session_id,
            expected_parent_turn_id=binding.parent_turn_id,
            require_direct_parent=True,
        )
        child_receipt = _make_receipt(binding, child_facts, role="CHILD", invocation_index=child.invocation_index)
        candidates.append(("CHILD", child.invocation_index, child_path, child_facts, child_receipt))
    ids = [record[4]["receipt_id"] for record in candidates]
    if len(set(ids)) != len(ids):
        raise _failure("DUPLICATE_RECEIPT_ID", detail="candidate receipt IDs are not unique")

    existing = _read_existing(binding.receipt_path, binding)
    operation_keys = {"project_id": binding.project_id, "planning_lite_ref": binding.expected_head, "change_id": binding.change_id, "task_id": binding.task_id, "run_family": binding.run_family}
    operation_records = [record for record in existing.values() if all(record.receipt.get(key) == value for key, value in operation_keys.items())]
    if len(operation_records) > len(candidates):
        raise _failure("RECEIPT_COUNT_MISMATCH", detail="existing operation has too many receipts")
    candidate_ids = set(ids)
    if any(record.receipt["receipt_id"] not in candidate_ids for record in operation_records):
        raise _failure("RECEIPT_COUNT_MISMATCH", detail="existing operation contains an alien receipt ID")

    results: list[dict[str, Any]] = []
    missing: list[dict[str, Any]] = []
    for role, index, rollout_path, facts, receipt in candidates:
        payload = canonical_bytes(receipt)
        previous = existing.get(receipt["receipt_id"])
        if previous is None:
            result = "APPENDED"
            missing.append(receipt)
        elif previous.payload == payload:
            result = "IDENTICAL_EXISTING"
        else:
            raise _failure("CONFLICTING_RECEIPT_ID", detail=receipt["receipt_id"])
        results.append(
            {
                "agent_role": role,
                "invocation_index": index,
                "receipt_id": receipt["receipt_id"],
                "session_id": facts.session_id,
                "turn_id": facts.turn_id,
                "rollout_path": str(rollout_path),
                "model_id": facts.model_id,
                "reasoning_effort": facts.reasoning_effort,
                "append_result": result,
            }
        )
    # Every candidate has been parsed, mapped, validated, canonicalized, and
    # compared with the existing stream before the first append.
    for receipt in missing:
        append_receipt(
            receipt,
            receipt_path=binding.receipt_path,
            registered_project_id=binding.project_id,
            planning_lite_ref=binding.expected_head,
            enabled=True,
        )
    read_back = _read_existing(binding.receipt_path, binding)
    for receipt in [candidate[4] for candidate in candidates]:
        stored = read_back.get(receipt["receipt_id"])
        if stored is None or stored.payload != canonical_bytes(receipt):
            raise _failure("READ_BACK_MISMATCH", path=binding.receipt_path)
    operation_count = sum(
        1
        for record in read_back.values()
        if all(record.receipt.get(key) == value for key, value in operation_keys.items())
    )
    if operation_count != len(candidates):
        raise _failure("RECEIPT_COUNT_MISMATCH", path=binding.receipt_path, detail=f"expected={len(candidates)} actual={operation_count}")
    return {
        "status": "PASS",
        "project_id": binding.project_id,
        "planning_lite_ref": binding.expected_head,
        "change_id": binding.change_id,
        "task_id": binding.task_id,
        "run_family": binding.run_family,
        "outcome": binding.outcome,
        "receipt_path": str(binding.receipt_path),
        "expected_receipt_count": len(candidates),
        "verified_receipt_count": operation_count,
        "records": results,
    }


def main(argv: Iterable[str] | None = None) -> int:
    try:
        binding = parse_args(argv)
        summary = capture(binding)
    except (CaptureError, ReceiptError) as exc:
        print(f"CAPTURE_FAILURE: {exc}", file=sys.stderr)
        return 1
    except (OSError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"CAPTURE_FAILURE: INVALID_BINDING: {type(exc).__name__}", file=sys.stderr)
        return 1
    print(json.dumps(summary, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
