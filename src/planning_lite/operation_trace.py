"""Pure semantic evidence construction for one governed operation attempt.

The trace is deliberately a derived view.  It does not select a route, own an
attempt, read a receipt stream, or decide a Project Spine gate.  The lifecycle
passes already-authoritative values to this module and owns any bounded
persistence transport around it.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
import re
from typing import Any, TypedDict


TRACE_COMPLETE = "TRACE_COMPLETE"
TRACE_PARTIAL = "TRACE_PARTIAL"
TRACE_UNAVAILABLE = "TRACE_UNAVAILABLE"

F01_FIELDS = (
    "operation_guidance_ref",
    "expected_route_operation_id",
    "expected_route_operation_class",
    "expected_route_id",
    "expected_route_outcome",
    "expected_route_reason_code",
    "expected_route_source_revision",
    "expected_route_authority_refs",
    "expected_route_selection_reason",
)
F02_FIELDS = (
    "actual_executor_receipt_ref",
    "actual_executor_receipt_id",
    "actual_executor_planning_lite_ref",
)
F03_FIELDS = (
    "next_gate_ref",
    "next_gate_source_ref",
    "next_gate_source_sha256",
)
DURING_FIELDS = (
    "during_operation_ref",
    "during_completeness",
    "during_expansion_count",
)

_ATTEMPT_ID = re.compile(r"[^/\s]+/[^/\s]+/A[1-9][0-9]*\Z")
_SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")
_ACTIVE_NEXT_GATE_SOURCE = ".planning/ACTIVE.md#Active change/Next permitted action"
_RECEIPT_CORE = ("receipt_id", "model_id", "agent_role", "invocation_index", "runtime_source")
_BASE_EVIDENCE_FIELDS = frozenset(
    {
        "authorization_ref",
        "candidate_source_identity",
        "observed_result_ref",
        "declared_verifier_contract_identities",
        "required_verifier_contract_identities",
        "technical_evaluation",
        "finding_refs",
        "prompt_composition_provenance_ref",
        "prompt_component_refs",
        "prompt_composition_identity",
        "stable_prefix_identity",
        "composition_comparison_evidence_refs",
        "recommendation_evidence_ref",
        "recommendation_outcome",
        "recommendation_authority",
        "evidence_status",
    }
)


class OperationTraceEvidenceEntry(TypedDict, total=False):
    """The small JSON-like mapping persisted inside a progress entry."""

    attempt_id: str
    operation_guidance_ref: str
    expected_route_operation_id: str
    expected_route_operation_class: str
    expected_route_id: str
    expected_route_outcome: str
    expected_route_reason_code: str
    expected_route_source_revision: str
    expected_route_authority_refs: list[dict[str, str]]
    expected_route_selection_reason: str
    during_operation_ref: str
    during_completeness: str
    during_expansion_count: int
    actual_executor_receipt_ref: str
    actual_executor_receipt_id: str
    actual_executor_planning_lite_ref: str
    next_gate_ref: str
    next_gate_source_ref: str
    next_gate_source_sha256: str


class OperationTraceError(ValueError):
    """A deterministic trace contract or trusted-relation failure."""

    def __init__(self, reason_code: str, message: str | None = None) -> None:
        self.reason_code = reason_code
        super().__init__(message or reason_code)


def _require_attempt(value: object, *, reason: str = "INVALID_ATTEMPT_ID") -> str:
    if not isinstance(value, str) or _ATTEMPT_ID.fullmatch(value) is None:
        raise OperationTraceError(reason, "AttemptRecordV1.attempt_id is invalid")
    return value


def _require_text(value: object, reason: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise OperationTraceError(reason)
    return value


def _require_ref(value: object, reason: str) -> str:
    text = _require_text(value, reason)
    if "\n" in text or "\r" in text:
        raise OperationTraceError(reason)
    return text


def _copy_entry(entry: Mapping[str, Any] | None, attempt_id: str) -> dict[str, Any]:
    if entry is None:
        return {"attempt_id": attempt_id}
    if not isinstance(entry, Mapping):
        raise OperationTraceError("INVALID_TRACE_ENTRY")
    result = deepcopy(dict(entry))
    existing_id = result.get("attempt_id")
    if existing_id != attempt_id:
        raise OperationTraceError("CROSS_ATTEMPT_TRACE")
    result["attempt_id"] = attempt_id
    return result


def _reject_duplicate(entry: Mapping[str, Any], fields: Sequence[str]) -> None:
    if any(field in entry for field in fields):
        raise OperationTraceError("DUPLICATE_TRACE_COMPONENT")


def _authority_refs(value: object) -> list[dict[str, str]]:
    if not isinstance(value, (list, tuple)):
        raise OperationTraceError("INVALID_ROUTE_AUTHORITY_REFS")
    refs: list[dict[str, str]] = []
    for item in value:
        if not isinstance(item, Mapping):
            raise OperationTraceError("INVALID_ROUTE_AUTHORITY_REFS")
        path = _require_ref(item.get("path"), "INVALID_ROUTE_AUTHORITY_REFS")
        digest = _require_ref(item.get("sha256"), "INVALID_ROUTE_AUTHORITY_REFS")
        refs.append({"path": path, "sha256": digest})
    return refs


def _guidance_fields(guidance: Mapping[str, Any]) -> dict[str, Any]:
    operation = guidance.get("operation")
    provenance = guidance.get("provenance")
    if not isinstance(operation, Mapping) or not isinstance(provenance, Mapping):
        raise OperationTraceError("INCOMPLETE_EXPECTED_ROUTE")
    result: dict[str, Any] = {
        "expected_route_operation_id": _require_ref(operation.get("operation_id"), "INCOMPLETE_EXPECTED_ROUTE"),
        "expected_route_operation_class": _require_ref(operation.get("operation_class"), "INCOMPLETE_EXPECTED_ROUTE"),
        "expected_route_id": _require_ref(operation.get("route_id"), "INCOMPLETE_EXPECTED_ROUTE"),
        "expected_route_outcome": _require_ref(guidance.get("outcome"), "INCOMPLETE_EXPECTED_ROUTE"),
        "expected_route_reason_code": _require_ref(guidance.get("reason_code"), "INCOMPLETE_EXPECTED_ROUTE"),
        "expected_route_source_revision": _require_ref(
            provenance.get("source_revision"), "INCOMPLETE_EXPECTED_ROUTE"
        ),
        "expected_route_authority_refs": _authority_refs(provenance.get("authority_refs")),
        "expected_route_selection_reason": _require_ref(
            provenance.get("selection_reason"), "INCOMPLETE_EXPECTED_ROUTE"
        ),
    }
    return result


def write_expected_route_evidence(
    attempt_id: str,
    operation_guidance_ref: str,
    guidance: Mapping[str, Any],
    existing_entry: Mapping[str, Any] | None = None,
) -> OperationTraceEvidenceEntry:
    """Add the exact already-selected PL07 route projection to an Attempt."""

    attempt = _require_attempt(attempt_id)
    entry = _copy_entry(existing_entry, attempt)
    _reject_duplicate(entry, F01_FIELDS)
    if not isinstance(guidance, Mapping):
        raise OperationTraceError("INCOMPLETE_EXPECTED_ROUTE")
    result: dict[str, Any] = {"attempt_id": attempt}
    result["operation_guidance_ref"] = _require_ref(operation_guidance_ref, "INCOMPLETE_EXPECTED_ROUTE")
    result.update(_guidance_fields(guidance))
    for key, value in entry.items():
        if key != "attempt_id":
            result[key] = value
    return result  # type: ignore[return-value]


def bind_attempt_run_receipt(
    attempt_id: str,
    receipt_ref: str | None = None,
    validated_receipt: Mapping[str, Any] | None = None,
    existing_entry: Mapping[str, Any] | None = None,
    *,
    actual_executor_receipt_ref: str | None = None,
    receipt_id: str | None = None,
    planning_lite_ref: str | None = None,
) -> OperationTraceEvidenceEntry:
    """Add a receipt locator and exact collector-owned identity to an Attempt."""

    attempt = _require_attempt(attempt_id)
    entry = _copy_entry(existing_entry, attempt)
    _reject_duplicate(entry, F02_FIELDS)
    ref = actual_executor_receipt_ref if actual_executor_receipt_ref is not None else receipt_ref
    ref = _require_ref(ref, "INCOMPLETE_EXECUTOR_RECEIPT")
    if not isinstance(validated_receipt, Mapping):
        raise OperationTraceError("INCOMPLETE_EXECUTOR_RECEIPT")
    persisted_attempt = validated_receipt.get("attempt_id")
    if persisted_attempt != attempt:
        raise OperationTraceError("CROSS_ATTEMPT_RECEIPT")
    actual_id = validated_receipt.get("receipt_id") if receipt_id is None else receipt_id
    actual_ref = validated_receipt.get("planning_lite_ref") if planning_lite_ref is None else planning_lite_ref
    actual_id = _require_ref(actual_id, "INCOMPLETE_EXECUTOR_RECEIPT")
    actual_ref = _require_ref(actual_ref, "INCOMPLETE_EXECUTOR_RECEIPT")
    if receipt_id is not None and validated_receipt.get("receipt_id") != receipt_id:
        raise OperationTraceError("RECEIPT_IDENTITY_MISMATCH")
    if planning_lite_ref is not None and validated_receipt.get("planning_lite_ref") != planning_lite_ref:
        raise OperationTraceError("RECEIPT_IDENTITY_MISMATCH")
    for field in _RECEIPT_CORE:
        value = validated_receipt.get(field)
        if field == "invocation_index":
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise OperationTraceError("INCOMPLETE_EXECUTOR_RECEIPT")
        elif value is None or (isinstance(value, str) and not value.strip()):
            raise OperationTraceError("INCOMPLETE_EXECUTOR_RECEIPT")
    result = dict(entry)
    result.update(
        {
            "actual_executor_receipt_ref": ref,
            "actual_executor_receipt_id": actual_id,
            "actual_executor_planning_lite_ref": actual_ref,
        }
    )
    return result  # type: ignore[return-value]


def write_historical_next_gate_evidence(
    attempt_id: str,
    next_gate_ref: str,
    next_gate_source_ref: str = _ACTIVE_NEXT_GATE_SOURCE,
    next_gate_source_sha256: str | None = None,
    existing_entry: Mapping[str, Any] | None = None,
) -> OperationTraceEvidenceEntry:
    """Add the post-S6 historical next action returned by Project Spine."""

    attempt = _require_attempt(attempt_id)
    entry = _copy_entry(existing_entry, attempt)
    _reject_duplicate(entry, F03_FIELDS)
    source = _require_ref(next_gate_source_ref, "INVALID_NEXT_GATE_SOURCE")
    if source != _ACTIVE_NEXT_GATE_SOURCE:
        raise OperationTraceError("INVALID_NEXT_GATE_SOURCE")
    digest = _require_ref(next_gate_source_sha256, "INVALID_NEXT_GATE_SOURCE_SHA256").lower()
    if _SHA256.fullmatch(digest) is None:
        raise OperationTraceError("INVALID_NEXT_GATE_SOURCE_SHA256")
    result = dict(entry)
    result.update(
        {
            "next_gate_ref": _require_ref(next_gate_ref, "MISSING_HISTORICAL_NEXT_GATE"),
            "next_gate_source_ref": source,
            "next_gate_source_sha256": digest,
        }
    )
    return result  # type: ignore[return-value]


def _write_during(
    attempt_id: str,
    observation: object,
    existing_entry: Mapping[str, Any],
) -> dict[str, Any]:
    from .context import OperationDepthObservationV1

    if type(observation) is not OperationDepthObservationV1:
        raise OperationTraceError("INVALID_DURING_OBSERVATION")
    if observation.operation_ref != attempt_id:
        raise OperationTraceError("CROSS_ATTEMPT_DURING")
    completeness = _require_text(observation.overall_completeness, "INVALID_DURING_OBSERVATION")
    if completeness not in {"COMPLETE", "PARTIAL", "UNAVAILABLE"}:
        raise OperationTraceError("INVALID_DURING_OBSERVATION")
    expansions = observation.expansions
    if not isinstance(expansions, tuple) or not all(isinstance(item, Mapping) for item in expansions):
        raise OperationTraceError("INVALID_DURING_OBSERVATION")
    result = dict(existing_entry)
    _reject_duplicate(result, DURING_FIELDS)
    result.update(
        {
            "during_operation_ref": attempt_id,
            "during_completeness": completeness,
            "during_expansion_count": len(expansions),
        }
    )
    return result


def record_governed_attempt_evidence(
    phase: str,
    attempt_id: str,
    existing_entry: Mapping[str, Any] | None = None,
    *,
    operation_guidance_ref: str | None = None,
    guidance: Mapping[str, Any] | None = None,
    receipt_ref: str | None = None,
    validated_receipt: Mapping[str, Any] | None = None,
    next_gate_ref: str | None = None,
    next_gate_source_ref: str = _ACTIVE_NEXT_GATE_SOURCE,
    next_gate_source_sha256: str | None = None,
    operation_depth_observation: object | None = None,
) -> OperationTraceEvidenceEntry:
    """Dispatch the pure PRE/POST additive trace construction phases."""

    normalized_phase = _require_text(phase, "INVALID_TRACE_PHASE").upper()
    attempt = _require_attempt(attempt_id)
    if normalized_phase == "PRE":
        if operation_guidance_ref is None or guidance is None:
            raise OperationTraceError("INCOMPLETE_EXPECTED_ROUTE")
        result: Mapping[str, Any] = write_expected_route_evidence(
            attempt, operation_guidance_ref, guidance, existing_entry
        )
        if operation_depth_observation is not None:
            result = _write_during(attempt, operation_depth_observation, result)
        return dict(result)  # type: ignore[return-value]
    if normalized_phase != "POST":
        raise OperationTraceError("INVALID_TRACE_PHASE")
    if existing_entry is None:
        raise OperationTraceError("MISSING_PRE_TRACE")
    entry = _copy_entry(existing_entry, attempt)
    if any(field not in entry for field in F01_FIELDS):
        raise OperationTraceError("MISSING_EXPECTED_ROUTE")
    if receipt_ref is None or validated_receipt is None:
        raise OperationTraceError("INCOMPLETE_EXECUTOR_RECEIPT")
    result = bind_attempt_run_receipt(attempt, receipt_ref, validated_receipt, entry)
    result = write_historical_next_gate_evidence(
        attempt,
        _require_ref(next_gate_ref, "MISSING_HISTORICAL_NEXT_GATE"),
        next_gate_source_ref,
        next_gate_source_sha256,
        result,
    )
    if operation_depth_observation is not None and not any(field in result for field in DURING_FIELDS):
        result = _write_during(attempt, operation_depth_observation, result)
    return result  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class OperationTraceView:
    """Detached, non-authoritative classification of persisted trace evidence."""

    attempt_id: str | None
    trace_state: str
    f01: Mapping[str, Any] | None = None
    during: Mapping[str, Any] | None = None
    f02: Mapping[str, Any] | None = None
    f03: Mapping[str, Any] | None = None
    reason_codes: tuple[str, ...] = ()

    @property
    def completeness(self) -> str:
        return self.trace_state

    @property
    def state(self) -> str:
        return self.trace_state

    def to_mapping(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "trace_state": self.trace_state,
            "f01": deepcopy(dict(self.f01)) if self.f01 is not None else None,
            "during": deepcopy(dict(self.during)) if self.during is not None else None,
            "f02": deepcopy(dict(self.f02)) if self.f02 is not None else None,
            "f03": deepcopy(dict(self.f03)) if self.f03 is not None else None,
            "reason_codes": list(self.reason_codes),
        }


def _component(entry: Mapping[str, Any], fields: Sequence[str]) -> dict[str, Any] | None:
    if not any(field in entry for field in fields):
        return None
    if any(field not in entry for field in fields):
        return None
    return {field: deepcopy(entry[field]) for field in fields}


def _valid_receipt_core(receipt: Mapping[str, Any], attempt_id: str, component: Mapping[str, Any]) -> None:
    if receipt.get("attempt_id") != attempt_id:
        raise OperationTraceError("CROSS_ATTEMPT_RECEIPT")
    if receipt.get("receipt_id") != component.get("actual_executor_receipt_id"):
        raise OperationTraceError("RECEIPT_IDENTITY_MISMATCH")
    if receipt.get("planning_lite_ref") != component.get("actual_executor_planning_lite_ref"):
        raise OperationTraceError("RECEIPT_IDENTITY_MISMATCH")
    for field in _RECEIPT_CORE:
        value = receipt.get(field)
        if field == "invocation_index":
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise OperationTraceError("INCOMPLETE_EXECUTOR_RECEIPT")
        elif not isinstance(value, str) or not value.strip():
            raise OperationTraceError("INCOMPLETE_EXECUTOR_RECEIPT")


def _validate_f01(entry: Mapping[str, Any], component: Mapping[str, Any]) -> None:
    for field in F01_FIELDS:
        if field not in component:
            raise OperationTraceError("INCOMPLETE_EXPECTED_ROUTE")
    for field in F01_FIELDS[:7] + (F01_FIELDS[8],):
        _require_ref(component[field], "INVALID_EXPECTED_ROUTE")
    _require_ref(component["expected_route_source_revision"], "INVALID_EXPECTED_ROUTE")
    _authority_refs(component["expected_route_authority_refs"])


def _validate_during(entry: Mapping[str, Any], attempt_id: str) -> tuple[dict[str, Any] | None, bool, str | None]:
    component = _component(entry, DURING_FIELDS)
    if component is None:
        return None, False, "MISSING_DURING_OBSERVATION"
    if component["during_operation_ref"] != attempt_id:
        raise OperationTraceError("CROSS_ATTEMPT_DURING")
    completeness = component["during_completeness"]
    if completeness not in {"COMPLETE", "PARTIAL", "UNAVAILABLE"}:
        raise OperationTraceError("INVALID_DURING_OBSERVATION")
    if type(component["during_expansion_count"]) is not int or component["during_expansion_count"] < 0:
        raise OperationTraceError("INVALID_DURING_OBSERVATION")
    return component, completeness == "COMPLETE", None if completeness == "COMPLETE" else "DURING_NOT_COMPLETE"


def read_operation_trace_evidence(
    entry: Mapping[str, Any],
    receipt_lookup: Callable[[str], Mapping[str, Any] | None],
) -> OperationTraceView:
    """Validate one persisted entry using only its exact receipt locator."""

    if not isinstance(entry, Mapping) or not callable(receipt_lookup):
        raise OperationTraceError("INVALID_TRACE_READBACK")
    unknown = set(entry) - (set(F01_FIELDS) | set(F02_FIELDS) | set(F03_FIELDS) | set(DURING_FIELDS) | _BASE_EVIDENCE_FIELDS | {"attempt_id"})
    if unknown:
        raise OperationTraceError("UNKNOWN_TRACE_FIELD")
    attempt_id = _require_attempt(entry.get("attempt_id"))
    f01 = _component(entry, F01_FIELDS)
    f02 = _component(entry, F02_FIELDS)
    f03 = _component(entry, F03_FIELDS)
    reasons: list[str] = []
    if f01 is None:
        reasons.append("MISSING_EXPECTED_ROUTE")
    else:
        _validate_f01(entry, f01)
    during, during_complete, during_reason = _validate_during(entry, attempt_id)
    if during_reason is not None:
        reasons.append(during_reason)

    receipt: Mapping[str, Any] | None = None
    if f02 is None:
        reasons.append("MISSING_EXECUTOR_RECEIPT")
    else:
        ref = _require_ref(f02["actual_executor_receipt_ref"], "INVALID_EXECUTOR_RECEIPT_REF")
        receipt = receipt_lookup(ref)
        if receipt is None:
            reasons.append("RECEIPT_NOT_FOUND")
        else:
            _valid_receipt_core(receipt, attempt_id, f02)
    if f03 is None:
        reasons.append("MISSING_HISTORICAL_NEXT_GATE")
    else:
        _require_ref(f03["next_gate_ref"], "INVALID_HISTORICAL_NEXT_GATE")
        if f03["next_gate_source_ref"] != _ACTIVE_NEXT_GATE_SOURCE:
            raise OperationTraceError("INVALID_NEXT_GATE_SOURCE")
        digest = _require_ref(f03["next_gate_source_sha256"], "INVALID_NEXT_GATE_SOURCE_SHA256")
        if _SHA256.fullmatch(digest) is None or digest != digest.lower():
            raise OperationTraceError("INVALID_NEXT_GATE_SOURCE_SHA256")

    if f01 is None or f02 is None or f03 is None or during is None or not during_complete or receipt is None:
        return OperationTraceView(
            attempt_id,
            TRACE_PARTIAL,
            f01=f01,
            during=during,
            f02=f02,
            f03=f03,
            reason_codes=tuple(dict.fromkeys(reasons)),
        )
    return OperationTraceView(
        attempt_id,
        TRACE_COMPLETE,
        f01=f01,
        during=during,
        f02=f02,
        f03=f03,
        reason_codes=(),
    )


__all__ = [
    "DURING_FIELDS",
    "F01_FIELDS",
    "F02_FIELDS",
    "F03_FIELDS",
    "OperationTraceError",
    "OperationTraceEvidenceEntry",
    "OperationTraceView",
    "TRACE_COMPLETE",
    "TRACE_PARTIAL",
    "TRACE_UNAVAILABLE",
    "bind_attempt_run_receipt",
    "read_operation_trace_evidence",
    "record_governed_attempt_evidence",
    "write_expected_route_evidence",
    "write_historical_next_gate_evidence",
]
