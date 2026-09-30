"""Validation and append-only collection of RunReceipt v1 and v2."""

from __future__ import annotations

from copy import deepcopy
from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import threading
from typing import Any, Callable, Mapping, TypedDict

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
TOP_LEVEL_KEYS_V1 = TOP_LEVEL_KEYS
TOP_LEVEL_KEYS_V2 = TOP_LEVEL_KEYS_V1 | {"attempt_id", "execution_invocation_id"}
SCHEMA_TOP_LEVEL_KEYS = {1: TOP_LEVEL_KEYS_V1, 2: TOP_LEVEL_KEYS_V2}
TOKEN_KEYS = {"input", "output", "cached", "reasoning", "total", "source"}
READ_KEYS = {"planning", "non_planning", "source"}
WORK_WINDOW_REGISTRATION = "work_window_registration"
RESOURCE_OBSERVATION = "resource_observation"
WORK_WINDOW_MEMBERSHIP_RULE = "DEDICATED_EXPLICIT_SOURCE_SEGMENT_V1"
CONFIGURATION_REF_ROLE = "DECLARED_IMMUTABLE_COMPARISON_ARM_REFERENCE / NOT AUTOMATICALLY PROVIDER-VERIFIED"
WORK_WINDOW_REGISTRATION_KEYS = {
    "record_type", "schema_version", "window_id", "project_id", "project_root",
    "configuration_ref", "planning_lite_ref", "configuration_ref_role", "provider", "model", "membership_rule", "source_ref",
    "source_identity", "start_offset_bytes", "prefix_anchor", "registered_at_utc",
    "registration_state",
}
RESOURCE_OBSERVATION_KEYS = {
    "record_type", "schema_version", "observation_id", "project_id", "scope",
    "configuration_ref", "planning_lite_ref", "configuration_ref_role", "provider", "model", "measurement_method",
    "native_quantity_semantics", "source", "quantities", "source_completeness",
    "metric_completeness", "limitations", "unavailable_reason", "finalized_at_utc",
}
RESOURCE_METRICS = {
    "input_tokens", "cached_input_tokens", "output_tokens",
    "reasoning_output_tokens", "total_tokens",
}
RESOURCE_QUALITIES = {"DIRECT", "BOUNDED"}
RESOURCE_CLAIM_KINDS = {
    "COMPLETE_SCOPE_TOTAL", "EXACT_OBSERVED_SUBSET", "PROVEN_LOWER_BOUND",
    "OTHER_PRECISELY_DEFINED_NONCOMPLETE_CLAIM",
}
UNAVAILABLE_REASONS = {
    "SOURCE_NOT_FOUND", "SOURCE_IDENTITY_MISMATCH", "SOURCE_REPLACED_OR_TRUNCATED",
    "SOURCE_READ_UNSTABLE", "MEMBERSHIP_BINDING_MISMATCH",
    "CONFIGURATION_BINDING_MISMATCH", "USAGE_RECORD_INVALID",
    "DUPLICATE_USAGE_CONFLICT", "REQUIRED_USAGE_MISSING",
    "AGGREGATE_RECONCILIATION_FAILED",
}
_LOCKS: dict[Path, threading.Lock] = {}
_LOCKS_GUARD = threading.Lock()


class WorkWindowRegistrationV1(TypedDict):
    record_type: str
    schema_version: int
    window_id: str
    project_id: str
    project_root: str
    configuration_ref: str
    planning_lite_ref: str
    configuration_ref_role: str
    provider: str
    model: str | None
    membership_rule: str
    source_ref: str
    source_identity: dict[str, Any]
    start_offset_bytes: int
    prefix_anchor: dict[str, Any]
    registered_at_utc: str
    registration_state: str


class ResourceObservationV1(TypedDict):
    record_type: str
    schema_version: int
    observation_id: str
    project_id: str
    scope: dict[str, Any]
    configuration_ref: str
    planning_lite_ref: str
    configuration_ref_role: str
    provider: str
    model: str | None
    measurement_method: str
    native_quantity_semantics: str
    source: dict[str, Any]
    quantities: dict[str, Any]
    source_completeness: str
    metric_completeness: dict[str, str]
    limitations: list[str]
    unavailable_reason: str | None
    finalized_at_utc: str


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


def _validate_receipt_record(
    value: Mapping[str, Any],
    *,
    registered_project_id: str,
) -> dict[str, Any]:
    """Validate stored-record structure without current-ref authority."""

    if not isinstance(value, Mapping):
        raise ReceiptError("RunReceipt must be a JSON object")
    data = deepcopy(dict(value))
    schema_version = data.get("schema_version")
    if isinstance(schema_version, bool) or not isinstance(schema_version, int) or schema_version not in SCHEMA_TOP_LEVEL_KEYS:
        raise ReceiptError("Unsupported RunReceipt schema_version")
    expected_keys = SCHEMA_TOP_LEVEL_KEYS[schema_version]
    if set(data) != expected_keys:
        missing = sorted(expected_keys - set(data))
        extra = sorted(set(data) - expected_keys)
        raise ReceiptError(f"RunReceipt shape mismatch; missing={missing}, extra={extra}")
    _nullable_string(data["receipt_id"], "receipt_id")
    if data["receipt_id"] is None:
        raise ReceiptError("receipt_id is required")
    _validate_timestamp(data["occurred_at_utc"])
    if data["project_id"] != registered_project_id:
        raise ReceiptError("receipt project_id does not match registered target")
    if not isinstance(data["planning_lite_ref"], str) or not data["planning_lite_ref"].strip():
        raise ReceiptError("planning_lite_ref must be a non-empty string")
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
    if schema_version == 2:
        for field in ("attempt_id", "execution_invocation_id"):
            if not isinstance(data[field], str) or not data[field].strip():
                raise ReceiptError(f"{field} must be a non-empty string")
    return data


def validate_configuration_ref(value: object) -> str:
    """Validate one immutable caller-declared comparison-arm reference."""

    if not isinstance(value, str) or not value or value != value.strip() or any(ch.isspace() for ch in value):
        raise ReceiptError("configuration_ref must be a non-empty immutable reference without whitespace")
    if value.startswith("sha256:"):
        digest = value.removeprefix("sha256:")
        if len(digest) == 64 and all(ch in "0123456789abcdef" for ch in digest):
            return value
        raise ReceiptError("configuration_ref sha256 form must contain 64 lowercase hexadecimal characters")
    separator = "@" if "@" in value else ":" if ":" in value else None
    if separator is None:
        raise ReceiptError("configuration_ref must be a versioned external reference or sha256 fingerprint")
    name, version = value.split(separator, 1)
    if not name or not version or not any(ch.isdigit() for ch in version) and not version.lower().startswith("v"):
        raise ReceiptError("configuration_ref external reference must include a version")
    return value


def _validate_source_identity(value: object, *, source_ref: str) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != {"path", "device", "file_id"}:
        raise ReceiptError("source_identity must contain exactly path, device, and file_id")
    path = value["path"]
    if not isinstance(path, str) or not path or path != source_ref or not Path(path).is_absolute():
        raise ReceiptError("source_identity.path must match the absolute source_ref")
    for field in ("device", "file_id"):
        number = value[field]
        if not isinstance(number, int) or isinstance(number, bool) or number < 0:
            raise ReceiptError(f"source_identity.{field} must be a non-negative integer")
    if value["file_id"] == 0:
        raise ReceiptError("source_identity.file_id must identify a stable file")
    return deepcopy(dict(value))


def _validate_prefix_anchor(value: object, *, start_offset_bytes: int) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != {
        "start_offset_bytes", "end_offset_bytes", "sha256"
    }:
        raise ReceiptError("prefix_anchor must contain exactly start_offset_bytes, end_offset_bytes, and sha256")
    start = value["start_offset_bytes"]
    end = value["end_offset_bytes"]
    if any(not isinstance(item, int) or isinstance(item, bool) for item in (start, end)):
        raise ReceiptError("prefix_anchor offsets must be integers")
    if start != max(0, start_offset_bytes - 64) or end != start_offset_bytes or end < start:
        raise ReceiptError("prefix_anchor offsets do not bind the registered start boundary")
    digest = value["sha256"]
    if not isinstance(digest, str) or len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
        raise ReceiptError("prefix_anchor.sha256 must be a lowercase SHA256 digest")
    return deepcopy(dict(value))


def _validate_work_window_planning_lite_ref(value: object) -> None:
    if (
        not isinstance(value, str)
        or not value.strip()
        or value.strip().casefold() == "unknown"
    ):
        raise ReceiptError("planning_lite_ref must be a known installed project ref")


def _validate_work_window_registration(
    value: Mapping[str, Any], *, registered_project_id: str
) -> dict[str, Any]:
    data = deepcopy(dict(value))
    if set(data) != WORK_WINDOW_REGISTRATION_KEYS:
        raise ReceiptError("WorkWindowRegistrationV1 shape mismatch")
    if data["record_type"] != WORK_WINDOW_REGISTRATION or type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ReceiptError("Unsupported WorkWindowRegistrationV1 discriminator")
    for field in ("window_id", "project_id", "project_root", "provider", "membership_rule", "source_ref"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ReceiptError(f"{field} must be a non-empty string")
    if data["project_id"] != registered_project_id:
        raise ReceiptError("registration project_id does not match registered target")
    if not Path(data["project_root"]).is_absolute():
        raise ReceiptError("project_root must be absolute")
    validate_configuration_ref(data["configuration_ref"])
    _validate_work_window_planning_lite_ref(data["planning_lite_ref"])
    if data["configuration_ref_role"] != CONFIGURATION_REF_ROLE:
        raise ReceiptError("configuration_ref_role must state declared, not provider-verified authority")
    if data["provider"] != "codex" or data["membership_rule"] != WORK_WINDOW_MEMBERSHIP_RULE:
        raise ReceiptError("Unsupported Work Window provider or membership_rule")
    if data["model"] is not None and (not isinstance(data["model"], str) or not data["model"].strip()):
        raise ReceiptError("model must be a non-empty string or null")
    if not Path(data["source_ref"]).is_absolute():
        raise ReceiptError("source_ref must be an absolute path")
    data["source_identity"] = _validate_source_identity(data["source_identity"], source_ref=data["source_ref"])
    start = data["start_offset_bytes"]
    if not isinstance(start, int) or isinstance(start, bool) or start < 0:
        raise ReceiptError("start_offset_bytes must be a non-negative integer")
    data["prefix_anchor"] = _validate_prefix_anchor(data["prefix_anchor"], start_offset_bytes=start)
    _validate_timestamp(data["registered_at_utc"])
    if data["registration_state"] != "OPEN":
        raise ReceiptError("registration_state must be OPEN")
    return data


def _validate_resource_observation(
    value: Mapping[str, Any], *, registered_project_id: str
) -> dict[str, Any]:
    data = deepcopy(dict(value))
    if set(data) != RESOURCE_OBSERVATION_KEYS:
        raise ReceiptError("ResourceObservationV1 shape mismatch")
    if data["record_type"] != RESOURCE_OBSERVATION or type(data["schema_version"]) is not int or data["schema_version"] != 1:
        raise ReceiptError("Unsupported ResourceObservationV1 discriminator")
    for field in ("observation_id", "project_id", "provider", "measurement_method", "native_quantity_semantics"):
        if not isinstance(data[field], str) or not data[field].strip():
            raise ReceiptError(f"{field} must be a non-empty string")
    if data["project_id"] != registered_project_id:
        raise ReceiptError("observation project_id does not match registered target")
    validate_configuration_ref(data["configuration_ref"])
    _validate_work_window_planning_lite_ref(data["planning_lite_ref"])
    if data["configuration_ref_role"] != CONFIGURATION_REF_ROLE:
        raise ReceiptError("configuration_ref_role must state declared, not provider-verified authority")
    if data["model"] is not None and (not isinstance(data["model"], str) or not data["model"].strip()):
        raise ReceiptError("model must be a non-empty string or null")

    scope = data["scope"]
    if not isinstance(scope, Mapping) or set(scope) != {"kind", "id", "start_offset_bytes", "end_offset_bytes"}:
        raise ReceiptError("scope must contain exactly kind, id, start_offset_bytes, and end_offset_bytes")
    if scope["kind"] != "WORK_WINDOW" or not isinstance(scope["id"], str) or not scope["id"].strip():
        raise ReceiptError("ResourceObservationV1 scope must identify one WORK_WINDOW")
    start = scope["start_offset_bytes"]
    end = scope["end_offset_bytes"]
    if not isinstance(start, int) or isinstance(start, bool) or start < 0:
        raise ReceiptError("scope.start_offset_bytes must be a non-negative integer")
    if end is not None and (not isinstance(end, int) or isinstance(end, bool) or end < 0):
        raise ReceiptError("scope.end_offset_bytes must be null or a non-negative integer")

    source = data["source"]
    source_keys = {
        "source_ref", "membership_rule", "source_identity", "prefix_anchor", "segment_sha256",
        "unique_response_count", "response_identity_sha256", "thread_id",
    }
    if not isinstance(source, Mapping) or set(source) != source_keys:
        raise ReceiptError("source provenance shape mismatch")
    source_ref = source["source_ref"]
    if not isinstance(source_ref, str) or not Path(source_ref).is_absolute():
        raise ReceiptError("source.source_ref must be an absolute path")
    if source["membership_rule"] != WORK_WINDOW_MEMBERSHIP_RULE:
        raise ReceiptError("Unsupported source membership rule")
    source["source_identity"] = _validate_source_identity(source["source_identity"], source_ref=source_ref)
    source["prefix_anchor"] = _validate_prefix_anchor(source["prefix_anchor"], start_offset_bytes=start)
    segment_digest = source["segment_sha256"]
    if segment_digest is not None and (
        not isinstance(segment_digest, str) or len(segment_digest) != 64
        or any(ch not in "0123456789abcdef" for ch in segment_digest)
    ):
        raise ReceiptError("source.segment_sha256 must be null or a lowercase SHA256 digest")
    count = source["unique_response_count"]
    if not isinstance(count, int) or isinstance(count, bool) or count < 0:
        raise ReceiptError("unique_response_count must be a non-negative integer")
    response_digest = source["response_identity_sha256"]
    if not isinstance(response_digest, str) or len(response_digest) != 64 or any(ch not in "0123456789abcdef" for ch in response_digest):
        raise ReceiptError("response_identity_sha256 must be a lowercase SHA256 digest")
    if source["thread_id"] is not None and (not isinstance(source["thread_id"], str) or not source["thread_id"].strip()):
        raise ReceiptError("source.thread_id must be a non-empty string or null")

    metrics = data["metric_completeness"]
    if not isinstance(metrics, Mapping) or set(metrics) != RESOURCE_METRICS:
        raise ReceiptError("metric_completeness must describe exactly the supported native metrics")
    if any(
        not isinstance(state, str)
        or state not in {"COMPLETE", "ABSENT", "PARTIAL", "UNKNOWN", "UNAVAILABLE"}
        for state in metrics.values()
    ):
        raise ReceiptError("metric_completeness contains an unsupported state")
    if not isinstance(data["quantities"], Mapping) or set(data["quantities"]) - RESOURCE_METRICS:
        raise ReceiptError("quantities contains an unsupported native metric")
    source_completeness = data["source_completeness"]
    if not isinstance(source_completeness, str) or source_completeness not in {
        "COMPLETE", "PARTIAL", "UNKNOWN", "UNAVAILABLE"
    }:
        raise ReceiptError("source_completeness is invalid")
    for metric, quantity in data["quantities"].items():
        if not isinstance(quantity, Mapping) or set(quantity) != {"value", "quality", "numeric_claim_kind"}:
            raise ReceiptError(f"quantity {metric} must contain value, quality, and numeric_claim_kind")
        number = quantity["value"]
        if not isinstance(number, int) or isinstance(number, bool) or number < 0:
            raise ReceiptError(f"quantity {metric}.value must be a non-negative integer")
        if not isinstance(quantity["quality"], str) or quantity["quality"] not in RESOURCE_QUALITIES:
            raise ReceiptError(f"quantity {metric}.quality is invalid")
        if not isinstance(quantity["numeric_claim_kind"], str) or quantity["numeric_claim_kind"] not in RESOURCE_CLAIM_KINDS:
            raise ReceiptError(f"quantity {metric}.numeric_claim_kind is invalid")
        if quantity["quality"] == "DIRECT":
            if quantity["numeric_claim_kind"] != "COMPLETE_SCOPE_TOTAL":
                raise ReceiptError("DIRECT quantities must claim COMPLETE_SCOPE_TOTAL")
            if source_completeness != "COMPLETE" or metrics[metric] != "COMPLETE":
                raise ReceiptError("DIRECT COMPLETE_SCOPE_TOTAL requires complete source and metric coverage")
        elif quantity["numeric_claim_kind"] == "COMPLETE_SCOPE_TOTAL":
            raise ReceiptError("BOUNDED quantities cannot claim COMPLETE_SCOPE_TOTAL")
        elif metrics[metric] in {"ABSENT", "UNAVAILABLE"}:
            raise ReceiptError(f"BOUNDED quantity {metric} must have observed metric coverage")
    if not isinstance(data["limitations"], list) or any(not isinstance(item, str) or not item.strip() for item in data["limitations"]):
        raise ReceiptError("limitations must be a list of non-empty strings")
    reason = data["unavailable_reason"]
    if reason is None:
        if end is None or end < start:
            raise ReceiptError("available observations require an end offset at/after the start")
        if not data["quantities"] or source_completeness == "UNAVAILABLE":
            raise ReceiptError("available observations require at least one numeric quantity")
        if any(state == "UNAVAILABLE" for state in metrics.values()):
            raise ReceiptError("available observation metrics cannot be marked UNAVAILABLE")
        if end is None or source["segment_sha256"] is None:
            raise ReceiptError("available observations require a bounded end offset and segment digest")
    else:
        if not isinstance(reason, str) or reason not in UNAVAILABLE_REASONS:
            raise ReceiptError("unavailable_reason is not in the stable vocabulary")
        if end is not None and end < start and reason != "SOURCE_REPLACED_OR_TRUNCATED":
            raise ReceiptError("only a truncation failure may report an end before the registered start")
        if data["quantities"] or source_completeness != "UNAVAILABLE" or any(state != "UNAVAILABLE" for state in metrics.values()):
            raise ReceiptError("UNAVAILABLE observations cannot contain numeric claims")
        if end is None and source["segment_sha256"] is not None:
            raise ReceiptError("unavailable observation without an end boundary cannot claim a segment digest")
    _validate_timestamp(data["finalized_at_utc"])
    return data


def validate_telemetry_record(
    value: Mapping[str, Any], *, registered_project_id: str
) -> dict[str, Any]:
    """Dispatch one untagged RunReceipt or a known typed sibling strictly."""

    if not isinstance(value, Mapping):
        raise ReceiptError("Telemetry record must be a JSON object")
    if "record_type" not in value:
        return _validate_receipt_record(value, registered_project_id=registered_project_id)
    record_type = value.get("record_type")
    if record_type == WORK_WINDOW_REGISTRATION:
        return _validate_work_window_registration(value, registered_project_id=registered_project_id)
    if record_type == RESOURCE_OBSERVATION:
        return _validate_resource_observation(value, registered_project_id=registered_project_id)
    raise ReceiptError(f"Unknown tagged telemetry record_type: {record_type!r}")


def validate_receipt(
    value: Mapping[str, Any],
    *,
    registered_project_id: str,
    planning_lite_ref: str,
) -> dict[str, Any]:
    """Validate a receipt and return a detached current-authority mapping."""

    data = _validate_receipt_record(value, registered_project_id=registered_project_id)
    if data["planning_lite_ref"] != planning_lite_ref:
        raise ReceiptError("planning_lite_ref is collector-owned and does not match answers")
    return data


def canonical_bytes(receipt: Mapping[str, Any]) -> bytes:
    return json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _load_answers_ref(path: Path, *, reject_unknown: bool = False) -> str:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ReceiptError(f"Cannot read Copier answers {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise ReceiptError(f"Invalid Copier answers mapping: {path}")
    for key in ("_commit", "_vcs_ref"):
        value = data.get(key)
        if isinstance(value, str) and value.strip():
            resolved = value.strip()
            if reject_unknown and resolved.casefold() == "unknown":
                continue
            return resolved
    raise ReceiptError("Copier answers has no usable installed ref")


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ReceiptError(f"Telemetry JSON contains duplicate key: {key}")
        result[key] = value
    return result


def _scan_telemetry_stream(
    path: Path, *, registered_project_id: str
) -> dict[str, dict[str, tuple[dict[str, Any], bytes]]]:
    """Validate one mixed stream while keeping identity namespaces separate."""

    result: dict[str, dict[str, tuple[dict[str, Any], bytes]]] = {
        "run_receipts": {},
        "work_window_registrations": {},
        "resource_observations": {},
    }
    if not path.exists():
        return result
    raw = path.read_bytes()
    if raw and not raw.endswith(b"\n"):
        raise ReceiptError("Telemetry stream ends with a partial line")
    if not raw:
        return result
    observations_by_window: dict[str, str] = {}
    for line in raw.split(b"\n")[:-1]:
        if not line.strip():
            raise ReceiptError("Telemetry stream contains an empty line")
        try:
            previous = json.loads(line, object_pairs_hook=_unique_json_object)
        except (json.JSONDecodeError, ReceiptError) as exc:
            raise ReceiptError("Telemetry stream contains invalid JSON") from exc
        if not isinstance(previous, dict):
            raise ReceiptError("Telemetry stream contains a non-object record")
        validated = validate_telemetry_record(previous, registered_project_id=registered_project_id)
        if "record_type" not in validated:
            family = "run_receipts"
            identity = validated["receipt_id"]
        elif validated["record_type"] == WORK_WINDOW_REGISTRATION:
            family = "work_window_registrations"
            identity = validated["window_id"]
            if line != canonical_bytes(validated):
                raise ReceiptError("Persisted WorkWindowRegistrationV1 is not canonical JSON")
        else:
            family = "resource_observations"
            identity = validated["observation_id"]
            if line != canonical_bytes(validated):
                raise ReceiptError("Persisted ResourceObservationV1 is not canonical JSON")
            window_id = validated["scope"]["id"]
            if window_id not in result["work_window_registrations"]:
                raise ReceiptError("ResourceObservationV1 was appended before its prospective registration")
            if window_id in observations_by_window:
                raise ReceiptError("Telemetry stream contains more than one final observation for a window")
            observations_by_window[window_id] = identity
        if identity in result[family]:
            raise ReceiptError(f"Telemetry stream contains a duplicate {family} identity")
        result[family][identity] = (validated, line)

    registrations = result["work_window_registrations"]
    for observation, _line in result["resource_observations"].values():
        scope = observation["scope"]
        registration_row = registrations.get(scope["id"])
        if registration_row is None:
            raise ReceiptError("ResourceObservationV1 has no persisted WorkWindowRegistrationV1")
        registration = registration_row[0]
        source = observation["source"]
        if (
            observation["project_id"] != registration["project_id"]
            or observation["configuration_ref"] != registration["configuration_ref"]
            or observation["planning_lite_ref"] != registration["planning_lite_ref"]
            or observation["configuration_ref_role"] != registration["configuration_ref_role"]
            or observation["provider"] != registration["provider"]
            or (registration["model"] is not None and observation["model"] != registration["model"])
            or scope["start_offset_bytes"] != registration["start_offset_bytes"]
            or source["source_ref"] != registration["source_ref"]
            or source["source_identity"] != registration["source_identity"]
            or source["membership_rule"] != registration["membership_rule"]
            or source["prefix_anchor"] != registration["prefix_anchor"]
        ):
            raise ReceiptError("ResourceObservationV1 conflicts with its prospective registration")
    return result


def scan_telemetry_records(
    receipt_path: str | Path, *, registered_project_id: str
) -> dict[str, dict[str, dict[str, Any]]]:
    """Read all validated record families; receipt-facing callers may filter receipts."""

    path = Path(receipt_path).expanduser().resolve()
    with _serialized_receipt(path):
        scanned = _scan_telemetry_stream(path, registered_project_id=registered_project_id)
    return {
        family: {identity: deepcopy(record) for identity, (record, _line) in records.items()}
        for family, records in scanned.items()
    }


def _scan_existing_records(
    path: Path,
    *,
    registered_project_id: str,
) -> dict[str, tuple[dict[str, Any], bytes]]:
    """Read the existing receipt namespace from the strict mixed stream."""

    return _scan_telemetry_stream(path, registered_project_id=registered_project_id)["run_receipts"]


def _append_validated_receipt(
    validated: dict[str, Any],
    *,
    receipt_path: str | Path,
    registered_project_id: str,
) -> bool:
    """Append a structurally and current-authority validated receipt."""

    path = Path(receipt_path).expanduser().resolve()
    payload = canonical_bytes(validated)
    with _serialized_receipt(path):
        existing = _scan_existing_records(path, registered_project_id=registered_project_id)
        previous = existing.get(validated["receipt_id"])
        if previous is not None:
            if previous[1] == payload:
                return False
            raise ReceiptError("Conflicting reuse of receipt_id")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("ab") as handle:
            handle.write(payload + b"\n")
            handle.flush()
            try:
                os.fsync(handle.fileno())
            except OSError:
                pass
    return True


def _work_window_intent(value: Mapping[str, Any]) -> dict[str, Any]:
    keys = {
        "window_id", "project_id", "project_root", "configuration_ref", "planning_lite_ref", "provider",
        "model", "membership_rule", "source_ref",
    }
    if not isinstance(value, Mapping) or set(value) != keys:
        raise ReceiptError("Work Window intent shape mismatch")
    intent = deepcopy(dict(value))
    for field in ("window_id", "project_id", "project_root", "provider", "membership_rule", "source_ref"):
        if not isinstance(intent[field], str) or not intent[field].strip():
            raise ReceiptError(f"{field} must be a non-empty string")
    if not Path(intent["project_root"]).is_absolute() or not Path(intent["source_ref"]).is_absolute():
        raise ReceiptError("project_root and source_ref must be absolute paths")
    validate_configuration_ref(intent["configuration_ref"])
    if not isinstance(intent["planning_lite_ref"], str) or not intent["planning_lite_ref"].strip():
        raise ReceiptError("planning_lite_ref must be a non-empty installed project ref")
    if intent["provider"] != "codex" or intent["membership_rule"] != WORK_WINDOW_MEMBERSHIP_RULE:
        raise ReceiptError("Unsupported Work Window provider or membership rule")
    if intent["model"] is not None and (not isinstance(intent["model"], str) or not intent["model"].strip()):
        raise ReceiptError("model must be a non-empty string or null")
    return intent


def _registration_matches_intent(
    registration: Mapping[str, Any], intent: Mapping[str, Any]
) -> bool:
    return all(registration[key] == value for key, value in intent.items())


def persist_work_window_registration(
    intent: Mapping[str, Any],
    *,
    receipt_path: str | Path,
    registered_project_id: str,
    registration_factory: Callable[[], Mapping[str, Any]],
) -> dict[str, Any]:
    """Create or replay a prospective registration under the stream lock."""

    checked_intent = _work_window_intent(intent)
    if checked_intent["project_id"] != registered_project_id:
        raise ReceiptError("Work Window intent project_id does not match registered target")
    path = Path(receipt_path).expanduser().resolve()
    def persist(candidate: Mapping[str, Any] | None) -> dict[str, Any]:
        with _serialized_receipt(path):
            stream = _scan_telemetry_stream(path, registered_project_id=registered_project_id)
            prior = stream["work_window_registrations"].get(checked_intent["window_id"])
            if prior is not None:
                if not _registration_matches_intent(prior[0], checked_intent):
                    raise ReceiptError("Conflicting reuse of window_id")
                return deepcopy(prior[0])
            candidate_value = registration_factory() if candidate is None else candidate
            if not isinstance(candidate_value, Mapping):
                raise ReceiptError("registration_factory must return a mapping")
            validated = _validate_work_window_registration(
                candidate_value, registered_project_id=registered_project_id
            )
            if not _registration_matches_intent(validated, checked_intent):
                raise ReceiptError("Generated registration does not match the explicit intent")
            payload = canonical_bytes(validated)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("ab") as handle:
                handle.write(payload + b"\n")
                handle.flush()
                try:
                    os.fsync(handle.fileno())
                except OSError:
                    pass
            readback = _scan_telemetry_stream(path, registered_project_id=registered_project_id)
            stored = readback["work_window_registrations"].get(checked_intent["window_id"])
            if stored is None or stored[1] != payload:
                raise ReceiptError("Persisted WorkWindowRegistrationV1 canonical readback mismatch")
            return deepcopy(stored[0])

    # A failed first open must not create telemetry state just to acquire a lock.
    # If a stream already exists, inspect/replay under its process-safe lock before
    # touching the explicitly supplied source.
    if not path.exists():
        candidate = registration_factory()
        return persist(candidate)
    return persist(None)


def read_work_window_registration(
    window_id: str, *, receipt_path: str | Path, registered_project_id: str
) -> dict[str, Any]:
    path = Path(receipt_path).expanduser().resolve()
    with _serialized_receipt(path):
        stream = _scan_telemetry_stream(path, registered_project_id=registered_project_id)
        stored = stream["work_window_registrations"].get(window_id)
        if stored is None:
            raise ReceiptError(f"Work Window registration not found: {window_id}")
        return deepcopy(stored[0])


def read_resource_observation_for_window(
    window_id: str, *, receipt_path: str | Path, registered_project_id: str
) -> dict[str, Any] | None:
    path = Path(receipt_path).expanduser().resolve()
    with _serialized_receipt(path):
        stream = _scan_telemetry_stream(path, registered_project_id=registered_project_id)
        for record, _line in stream["resource_observations"].values():
            if record["scope"]["id"] == window_id:
                return deepcopy(record)
        return None


def append_resource_observation(
    observation: Mapping[str, Any], *, receipt_path: str | Path, registered_project_id: str
) -> dict[str, Any]:
    """Persist one terminal observation, serializing replay through readback."""

    validated = _validate_resource_observation(
        observation, registered_project_id=registered_project_id
    )
    path = Path(receipt_path).expanduser().resolve()
    payload = canonical_bytes(validated)
    window_id = validated["scope"]["id"]
    with _serialized_receipt(path):
        stream = _scan_telemetry_stream(path, registered_project_id=registered_project_id)
        registration = stream["work_window_registrations"].get(window_id)
        if registration is None:
            raise ReceiptError("Cannot finalize an unregistered Work Window")
        registered = registration[0]
        source = validated["source"]
        if (
            validated["project_id"] != registered["project_id"]
            or validated["configuration_ref"] != registered["configuration_ref"]
            or validated["planning_lite_ref"] != registered["planning_lite_ref"]
            or validated["configuration_ref_role"] != registered["configuration_ref_role"]
            or validated["provider"] != registered["provider"]
            or (registered["model"] is not None and validated["model"] != registered["model"])
            or validated["scope"]["start_offset_bytes"] != registered["start_offset_bytes"]
            or source["source_ref"] != registered["source_ref"]
            or source["source_identity"] != registered["source_identity"]
            or source["membership_rule"] != registered["membership_rule"]
            or source["prefix_anchor"] != registered["prefix_anchor"]
        ):
            raise ReceiptError("ResourceObservationV1 registration binding mismatch")
        existing = next(
            (row for row in stream["resource_observations"].values() if row[0]["scope"]["id"] == window_id),
            None,
        )
        if existing is not None:
            prior_semantics = deepcopy(existing[0])
            candidate_semantics = deepcopy(validated)
            prior_semantics.pop("finalized_at_utc", None)
            candidate_semantics.pop("finalized_at_utc", None)
            if canonical_bytes(prior_semantics) != canonical_bytes(candidate_semantics):
                raise ReceiptError("WINDOW_ALREADY_FINALIZED_CONFLICT")
            return deepcopy(existing[0])
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("ab") as handle:
            handle.write(payload + b"\n")
            handle.flush()
            try:
                os.fsync(handle.fileno())
            except OSError:
                pass
        readback = _scan_telemetry_stream(path, registered_project_id=registered_project_id)
        stored = readback["resource_observations"].get(validated["observation_id"])
        if stored is None or stored[1] != payload:
            raise ReceiptError("Persisted ResourceObservationV1 canonical readback mismatch")
        return deepcopy(stored[0])


def _read_receipt_by_id(
    receipt_id: str,
    *,
    receipt_path: str | Path,
    registered_project_id: str,
    expected_payload: bytes,
) -> dict[str, Any]:
    """Return the exact persisted receipt whose bytes match the expectation."""

    path = Path(receipt_path).expanduser().resolve()
    with _serialized_receipt(path):
        existing = _scan_existing_records(path, registered_project_id=registered_project_id)
        matching = existing.get(receipt_id)
        if matching is None:
            raise ReceiptError("Persisted receipt_id was not found")
        if matching[1] != expected_payload:
            raise ReceiptError("Persisted receipt bytes do not match expected payload")
        return deepcopy(matching[0])


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
    if isinstance(receipt, Mapping) and receipt.get("schema_version") == 2:
        raise ReceiptError("RunReceipt v2 requires collect_governed_receipt")
    validated = validate_receipt(
        receipt,
        registered_project_id=registered_project_id,
        planning_lite_ref=planning_lite_ref,
    )
    return _append_validated_receipt(
        validated,
        receipt_path=receipt_path,
        registered_project_id=registered_project_id,
    )


def collect_governed_receipt(
    receipt: Mapping[str, Any],
    *,
    project_root: str | Path,
    receipt_path: str | Path,
    registered_project_id: str,
    attempt_id: str,
    execution_invocation_id: str,
    enabled: bool,
) -> dict[str, Any]:
    """Collect a v2 receipt with caller-supplied governed identity context."""

    if not enabled:
        raise ReceiptError("Telemetry is disabled for this project; no receipt was written")
    if not isinstance(receipt, Mapping) or receipt.get("schema_version") != 2:
        raise ReceiptError("collect_governed_receipt requires RunReceipt schema_version 2")
    for value, field in ((attempt_id, "attempt_id"), (execution_invocation_id, "execution_invocation_id")):
        if not isinstance(value, str) or not value.strip():
            raise ReceiptError(f"{field} authority context must be a non-empty string")
    data = dict(receipt)
    data["planning_lite_ref"] = _load_answers_ref(Path(project_root).resolve() / ".copier-answers.planning-lite.yml")
    data["attempt_id"] = attempt_id
    data["execution_invocation_id"] = execution_invocation_id
    validated = validate_receipt(
        data,
        registered_project_id=registered_project_id,
        planning_lite_ref=data["planning_lite_ref"],
    )
    payload = canonical_bytes(validated)
    _append_validated_receipt(
        validated,
        receipt_path=receipt_path,
        registered_project_id=registered_project_id,
    )
    return _read_receipt_by_id(
        validated["receipt_id"],
        receipt_path=receipt_path,
        registered_project_id=registered_project_id,
        expected_payload=payload,
    )


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
    if raw.get("schema_version") == 2:
        raise ReceiptError("RunReceipt v2 requires collect_governed_receipt")
    raw["planning_lite_ref"] = _load_answers_ref(Path(project_root).resolve() / ".copier-answers.planning-lite.yml")
    return append_receipt(
        raw,
        receipt_path=receipt_path,
        registered_project_id=registered_project_id,
        planning_lite_ref=raw["planning_lite_ref"],
        enabled=enabled,
    )
