"""Validation and append-only collection of externally supplied RunReceipt v1."""

from __future__ import annotations

from copy import deepcopy
from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import threading
from typing import Any, Mapping

import yaml


class ReceiptError(RuntimeError):
    """Fail-closed receipt validation/storage error."""


OUTCOMES = {"PASS", "FAIL", "BLOCKED", "CANCELLED", "UNKNOWN"}
SOURCES = {"external_runtime", "operator", "unavailable"}
TOP_LEVEL_KEYS = {
    "schema_version", "receipt_id", "occurred_at_utc", "project_id",
    "planning_lite_ref", "change_id", "task_id", "run_family", "agent_role",
    "model_id", "model_tier", "invocation_index", "outcome", "tokens",
    "verifier_used", "reviewer_used", "model_escalation", "retry", "recheck",
    "reads", "runtime_source",
}
TOKEN_KEYS = {"input", "output", "cached", "reasoning", "total", "source"}
READ_KEYS = {"planning", "non_planning", "source"}
_LOCKS: dict[Path, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()


def _lock_for(path: Path) -> threading.Lock:
    with _LOCKS_GUARD:
        return _LOCKS.setdefault(path.resolve(), threading.Lock())


@contextmanager
def _process_lock(path: Path):
    """Serialize writers from separate processes with a small sidecar lock."""

    lock_path = path.with_name(f".{path.name}.lock")
    handle = None
    acquired = False
    try:
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        handle = lock_path.open("a+b")
        if os.name == "nt":
            import msvcrt

            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            acquired = True
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            acquired = True
        yield
    except (ImportError, OSError) as exc:
        if not acquired:
            raise ReceiptError(f"Cannot acquire receipt process lock: {lock_path}") from exc
        raise
    finally:
        if handle is not None:
            try:
                if acquired:
                    if os.name == "nt":
                        import msvcrt

                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            finally:
                handle.close()


@contextmanager
def _serialized_receipt(path: Path):
    with _lock_for(path):
        with _process_lock(path):
            yield


def _nullable_string(value: object, field: str) -> None:
    if value is not None and (not isinstance(value, str) or not value.strip()):
        raise ReceiptError(f"{field} must be a non-empty string or null")


def _nullable_nonnegative_int(value: object, field: str) -> None:
    if value is not None and (not isinstance(value, int) or isinstance(value, bool) or value < 0):
        raise ReceiptError(f"{field} must be a non-negative integer or null")


def _validate_timestamp(value: object) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ReceiptError("occurred_at_utc must be a non-empty ISO-8601 string")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ReceiptError("occurred_at_utc must be an ISO-8601 timestamp") from exc


def validate_receipt(
    value: Mapping[str, Any],
    *,
    registered_project_id: str,
    planning_lite_ref: str,
) -> dict[str, Any]:
    """Validate a receipt and return a detached canonical mapping."""

    if not isinstance(value, Mapping):
        raise ReceiptError("RunReceipt must be a JSON object")
    data = deepcopy(dict(value))
    if set(data) != TOP_LEVEL_KEYS:
        missing = sorted(TOP_LEVEL_KEYS - set(data))
        extra = sorted(set(data) - TOP_LEVEL_KEYS)
        raise ReceiptError(f"RunReceipt shape mismatch; missing={missing}, extra={extra}")
    if data["schema_version"] != 1:
        raise ReceiptError("Unsupported RunReceipt schema_version")
    _nullable_string(data["receipt_id"], "receipt_id")
    if data["receipt_id"] is None:
        raise ReceiptError("receipt_id is required")
    _validate_timestamp(data["occurred_at_utc"])
    if data["project_id"] != registered_project_id:
        raise ReceiptError("receipt project_id does not match registered target")
    if data["planning_lite_ref"] != planning_lite_ref:
        raise ReceiptError("planning_lite_ref is collector-owned and does not match answers")
    for field in ("change_id", "task_id", "run_family", "agent_role", "model_id", "model_tier", "runtime_source"):
        _nullable_string(data[field], field)
    _nullable_nonnegative_int(data["invocation_index"], "invocation_index")
    if data["outcome"] not in OUTCOMES:
        raise ReceiptError(f"Unsupported receipt outcome: {data['outcome']!r}")
    tokens = data["tokens"]
    if not isinstance(tokens, Mapping) or set(tokens) != TOKEN_KEYS:
        raise ReceiptError("tokens must contain exactly the v1 fields")
    for field in ("input", "output", "cached", "reasoning", "total"):
        _nullable_nonnegative_int(tokens[field], f"tokens.{field}")
    if tokens["source"] not in SOURCES:
        raise ReceiptError("tokens.source is invalid")
    reads = data["reads"]
    if not isinstance(reads, Mapping) or set(reads) != READ_KEYS:
        raise ReceiptError("reads must contain exactly the v1 fields")
    for field in ("planning", "non_planning"):
        _nullable_nonnegative_int(reads[field], f"reads.{field}")
    if reads["source"] not in SOURCES:
        raise ReceiptError("reads.source is invalid")
    for field in ("verifier_used", "reviewer_used", "model_escalation", "retry", "recheck"):
        if data[field] is not None and not isinstance(data[field], bool):
            raise ReceiptError(f"{field} must be boolean or null")
    return data


def canonical_bytes(receipt: Mapping[str, Any]) -> bytes:
    return json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _load_answers_ref(path: Path) -> str:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReceiptError(f"Cannot read Copier answers {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ReceiptError(f"Invalid Copier answers mapping: {path}")
    value = data.get("_commit") or data.get("_vcs_ref")
    if not isinstance(value, str) or not value.strip():
        raise ReceiptError("Copier answers has no usable installed ref")
    return value.strip()


def append_receipt(
    receipt: Mapping[str, Any],
    *,
    receipt_path: str | Path,
    registered_project_id: str,
    planning_lite_ref: str,
    enabled: bool,
) -> bool:
    """Validate and append one receipt. Return False for an identical duplicate."""

    if not enabled:
        raise ReceiptError("Telemetry is disabled for this project; no receipt was written")
    validated = validate_receipt(
        receipt,
        registered_project_id=registered_project_id,
        planning_lite_ref=planning_lite_ref,
    )
    path = Path(receipt_path).expanduser().resolve()
    payload = canonical_bytes(validated)
    with _serialized_receipt(path):
        if path.exists():
            raw = path.read_bytes()
            if raw and not raw.endswith(b"\n"):
                raise ReceiptError("Receipt stream ends with a partial line")
            for line in raw.splitlines():
                if not line.strip():
                    raise ReceiptError("Receipt stream contains an empty line")
                try:
                    previous = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise ReceiptError("Receipt stream contains invalid JSON") from exc
                if not isinstance(previous, dict):
                    raise ReceiptError("Receipt stream contains a non-object record")
                if previous.get("receipt_id") == validated["receipt_id"]:
                    if line == payload:
                        return False
                    raise ReceiptError("Conflicting reuse of receipt_id")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("ab") as handle:
            handle.write(payload + b"\n")
            handle.flush()
            try:
                import os

                os.fsync(handle.fileno())
            except OSError:
                pass
    return True


def collect_receipt(
    input_path: str | Path,
    *,
    project_root: str | Path,
    receipt_path: str | Path,
    registered_project_id: str,
    enabled: bool,
) -> bool:
    """Read external JSON, inject the answers-derived ref, and append it."""

    if not enabled:
        raise ReceiptError("Telemetry is disabled for this project; no receipt was written")
    source = Path(input_path).expanduser().resolve()
    try:
        raw = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReceiptError(f"Cannot read receipt input {source}: {exc}") from exc
    if not isinstance(raw, dict):
        raise ReceiptError("Receipt input must be a JSON object")
    raw["planning_lite_ref"] = _load_answers_ref(Path(project_root).resolve() / ".copier-answers.planning-lite.yml")
    return append_receipt(
        raw,
        receipt_path=receipt_path,
        registered_project_id=registered_project_id,
        planning_lite_ref=raw["planning_lite_ref"],
        enabled=enabled,
    )
