"""Bounded, host-neutral execution contracts for one governed operation.

This module deliberately has no knowledge of Attempt Runtime, Operation
Guidance selection, telemetry, or PL08.  It validates the immutable inputs
already selected by the lifecycle and returns one typed result.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import math
import re
import unicodedata
from typing import Any


SCHEMA_VERSION = 1
CONTRACT_VERSION = "GovernedExecutionEnvelopeV1"
INVOCATION_DOMAIN = b"planning-lite:governed-operation-execution-envelope:v1"
EXECUTION_STATUSES = frozenset({"COMPLETED", "FAILED", "INTERRUPTED", "INVALID"})
FAILURE_CATEGORIES = frozenset(
    {
        "EXECUTOR_UNAVAILABLE",
        "INVOCATION_REJECTED",
        "HOST_INVOCATION_FAILED",
        "EXECUTION_FAILED",
        "EXECUTION_INTERRUPTED",
        "INVALID_EXECUTION_RESULT",
        "ATTEMPT_IDENTITY_MISMATCH",
        "RECEIPT_MISSING",
        "RECEIPT_INVALID",
        "RECEIPT_ATTEMPT_ASSOCIATION_MISMATCH",
    }
)
_SHA256 = re.compile(r"[0-9A-F]{64}\Z")


class GovernedExecutorError(ValueError):
    """Fail-closed validation error for one bounded execution call."""


@dataclass(frozen=True, slots=True)
class EvidenceContentInputV1:
    """Transient exact-ref evidence bytes returned with a governed completion.

    This value carries no caller, digest, path, or authority facts. Lifecycle
    accepts it only as invocation-associated Class-B content and publishes it
    through the existing dependency-admission owner. It is never persisted or
    hashed into the execution envelope.
    """

    evidence_ref: str
    exact_raw_bytes: bytes

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_ref", _nonempty(self.evidence_ref, "evidence_ref"))
        if type(self.exact_raw_bytes) is not bytes:
            raise GovernedExecutorError("exact_raw_bytes must be exact bytes")


@dataclass(frozen=True, slots=True)
class GovernedExecutionDependencyInputV1:
    """Transient non-authoritative exact bytes for a legally claimed T-02.

    Lifecycle creates this two-field value only after the T-02 D11 claim and
    fresh current requirement/admission/route joins. It remains outside the
    persisted envelope, bounded payload, and envelope digest; the executor
    validates shape and passes the same bytes to host execution.
    """

    required_input_logical_ref: str
    exact_raw_bytes: bytes

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "required_input_logical_ref",
            _nonempty(self.required_input_logical_ref, "required_input_logical_ref"),
        )
        if type(self.exact_raw_bytes) is not bytes:
            raise GovernedExecutorError("exact_raw_bytes must be exact bytes")


def _attribute(value: object, name: str, default: object = None) -> object:
    try:
        return object.__getattribute__(value, name)
    except AttributeError:
        return default


def _nonempty(value: object, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or "\n" in value or "\r" in value:
        raise GovernedExecutorError(f"{field} must be a non-empty scalar string")
    return unicodedata.normalize("NFC", value)


def _sha256(value: object, field: str) -> str:
    text = _nonempty(value, field)
    if not _SHA256.fullmatch(text):
        raise GovernedExecutorError(f"{field} must be an uppercase SHA-256")
    return text


def _normal(value: object) -> object:
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, bool) or value is None or isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise GovernedExecutorError("canonical JSON rejects non-finite floats")
        raise GovernedExecutorError("canonical JSON rejects floats")
    if isinstance(value, Mapping):
        result: dict[str, object] = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise GovernedExecutorError("canonical JSON object keys must be strings")
            normalized_key = unicodedata.normalize("NFC", key)
            if normalized_key in result:
                raise GovernedExecutorError("canonical JSON contains duplicate object members")
            result[normalized_key] = _normal(item)
        return result
    if isinstance(value, (list, tuple)):
        return [_normal(item) for item in value]
    raise GovernedExecutorError("value is not canonically JSON serializable")


def canonical_json(value: object) -> str:
    """Return the lifecycle's exact canonical UTF-8 JSON text."""

    try:
        normalized = _normal(value)
        return json.dumps(
            normalized,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise GovernedExecutorError("value is not canonically JSON serializable") from exc


def canonical_digest(value: object) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest().upper()


def _tuple_strings(value: object, field: str) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise GovernedExecutorError(f"{field} must be an ordered string sequence")
    result = tuple(_nonempty(item, f"{field}[]") for item in value)
    if len(set(result)) != len(result):
        raise GovernedExecutorError(f"{field} must not contain duplicates")
    return result


def _to_mapping(value: object, field: str) -> dict[str, Any]:
    if isinstance(value, Mapping):
        return dict(value)
    method = _attribute(value, "to_mapping")
    if callable(method):
        result = method()
        if isinstance(result, Mapping):
            return dict(result)
    raise GovernedExecutorError(f"{field} must be a typed mapping carrier")


def _guidance_digest(guidance: Mapping[str, Any]) -> str:
    return canonical_digest(guidance)


def _guidance_ref(attempt: object, guidance: Mapping[str, Any], explicit: str | None) -> str:
    if explicit is not None:
        return _nonempty(explicit, "guidance_ref")
    attempt_ref = _attribute(attempt, "operation_guidance_ref")
    if isinstance(attempt_ref, str) and attempt_ref:
        return attempt_ref
    provenance = guidance.get("provenance")
    if isinstance(provenance, Mapping) and isinstance(provenance.get("selection_reason"), str):
        return provenance["selection_reason"]
    raise GovernedExecutorError("guidance_ref is not bound to the Attempt")


def _attempt_identity(attempt: object) -> tuple[str, str]:
    attempt_id = _nonempty(_attribute(attempt, "attempt_id"), "attempt.attempt_id")
    task_id = _nonempty(_attribute(attempt, "task_or_operation_id"), "attempt.task_or_operation_id")
    return attempt_id, task_id


@dataclass(frozen=True, slots=True)
class GovernedExecutionEnvelopeV1:
    """The exact ten-field canonical preparation envelope."""

    schema_version: int
    contract_version: str
    attempt_id: str
    operation_id: str
    task_or_operation_id: str
    guidance_ref: str
    guidance_digest: str
    authority_refs: tuple[str, ...]
    bounded_payload_digest: str
    payload_schema_ref: str

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise GovernedExecutorError("unsupported envelope schema_version")
        if self.contract_version != CONTRACT_VERSION:
            raise GovernedExecutorError("unsupported envelope contract_version")
        for name in ("attempt_id", "operation_id", "task_or_operation_id", "guidance_ref", "payload_schema_ref"):
            object.__setattr__(self, name, _nonempty(_attribute(self, name), name))
        for name in ("guidance_digest", "bounded_payload_digest"):
            object.__setattr__(self, name, _sha256(_attribute(self, name), name))
        object.__setattr__(self, "authority_refs", _tuple_strings(self.authority_refs, "authority_refs"))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "contract_version": self.contract_version,
            "attempt_id": self.attempt_id,
            "operation_id": self.operation_id,
            "task_or_operation_id": self.task_or_operation_id,
            "guidance_ref": self.guidance_ref,
            "guidance_digest": self.guidance_digest,
            "authority_refs": list(self.authority_refs),
            "bounded_payload_digest": self.bounded_payload_digest,
            "payload_schema_ref": self.payload_schema_ref,
        }

    @property
    def canonical_projection(self) -> str:
        return canonical_json(self.to_mapping())

    @property
    def envelope_digest(self) -> str:
        return hashlib.sha256(self.canonical_projection.encode("utf-8")).hexdigest().upper()

    @property
    def execution_invocation_id(self) -> str:
        return hashlib.sha256(INVOCATION_DOMAIN + b"\0" + self.canonical_projection.encode("utf-8")).hexdigest().upper()


@dataclass(frozen=True, slots=True)
class GovernedExecutionCompletionV1:
    """Typed facts and transient output bytes returned by one occurrence.

    ``artifact_output_bytes`` is the actual producer output associated with
    this exact completion. ``evidence_content_inputs`` carries only exact
    evidence refs and raw bytes. Lifecycle joins both to the completed source
    Attempt and PL08 refs before publication. They remain transient and are
    excluded from the unchanged persisted envelope and digest domain.
    """

    attempt_id: str
    execution_invocation_id: str
    envelope_digest: str
    operation_id: str
    task_or_operation_id: str
    result_id: str
    execution_status: str
    changed_paths: tuple[str, ...] = ()
    fact_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    acceptance_contract_ref: str = ""
    acceptance_contract: object | None = None
    verifier_contracts: tuple[object, ...] = ()
    verifier_evidence: tuple[object, ...] = ()
    findings: tuple[object, ...] = ()
    evaluation_scope_ref: str = ""
    supersession: tuple[object, ...] = ()
    evaluation_id: str = "EVALUATION-1"
    evaluation_run: bool = True
    candidate_quality: bool = True
    receipt_id: str | None = None
    artifact_output_bytes: bytes | None = None
    evidence_content_inputs: tuple[EvidenceContentInputV1, ...] = ()

    def __post_init__(self) -> None:
        for name in ("attempt_id", "execution_invocation_id", "envelope_digest", "operation_id", "task_or_operation_id", "result_id"):
            object.__setattr__(self, name, _nonempty(_attribute(self, name), name))
        object.__setattr__(self, "envelope_digest", _sha256(self.envelope_digest, "envelope_digest"))
        if self.execution_status not in EXECUTION_STATUSES:
            raise GovernedExecutorError("execution_status is unsupported")
        object.__setattr__(self, "changed_paths", _tuple_strings(self.changed_paths, "changed_paths"))
        object.__setattr__(self, "fact_refs", _tuple_strings(self.fact_refs, "fact_refs"))
        object.__setattr__(self, "artifact_refs", _tuple_strings(self.artifact_refs, "artifact_refs"))
        object.__setattr__(self, "verifier_contracts", tuple(self.verifier_contracts))
        object.__setattr__(self, "verifier_evidence", tuple(self.verifier_evidence))
        object.__setattr__(self, "findings", tuple(self.findings))
        object.__setattr__(self, "supersession", tuple(self.supersession))
        if self.artifact_output_bytes is not None and type(self.artifact_output_bytes) is not bytes:
            raise GovernedExecutorError("artifact_output_bytes must be exact bytes or None")
        evidence_inputs = tuple(self.evidence_content_inputs)
        if any(type(item) is not EvidenceContentInputV1 for item in evidence_inputs):
            raise GovernedExecutorError("evidence_content_inputs must contain exact EvidenceContentInputV1 values")
        object.__setattr__(self, "evidence_content_inputs", evidence_inputs)
        if self.receipt_id is not None:
            object.__setattr__(self, "receipt_id", _nonempty(self.receipt_id, "receipt_id"))
        if not isinstance(self.evaluation_run, bool) or not isinstance(self.candidate_quality, bool):
            raise GovernedExecutorError("evaluation_run and candidate_quality must be bool")


@dataclass(frozen=True, slots=True)
class GovernedExecutionResultV1:
    """One bounded result; it never carries storage or runtime state."""

    attempt_id: str
    execution_invocation_id: str | None
    accepted: bool
    outcome: str
    failure_category: str | None = None
    result_id: str | None = None
    execution_status: str | None = None
    operation_id: str | None = None
    task_or_operation_id: str | None = None
    envelope_digest: str | None = None
    changed_paths: tuple[str, ...] = ()
    fact_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()
    receipt_id: str | None = None
    completion: GovernedExecutionCompletionV1 | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "attempt_id", _nonempty(self.attempt_id, "attempt_id"))
        if self.execution_invocation_id is not None:
            object.__setattr__(self, "execution_invocation_id", _sha256(self.execution_invocation_id, "execution_invocation_id"))
        if not isinstance(self.accepted, bool):
            raise GovernedExecutorError("accepted must be bool")
        object.__setattr__(self, "outcome", _nonempty(self.outcome, "outcome"))
        if self.failure_category is not None and self.failure_category not in FAILURE_CATEGORIES:
            raise GovernedExecutorError("failure_category is unsupported")
        if self.result_id is not None:
            object.__setattr__(self, "result_id", _nonempty(self.result_id, "result_id"))
        if self.execution_status is not None and self.execution_status not in EXECUTION_STATUSES:
            raise GovernedExecutorError("execution_status is unsupported")
        for name in ("operation_id", "task_or_operation_id"):
            value = _attribute(self, name)
            if value is not None:
                object.__setattr__(self, name, _nonempty(value, name))
        if self.envelope_digest is not None:
            object.__setattr__(self, "envelope_digest", _sha256(self.envelope_digest, "envelope_digest"))
        object.__setattr__(self, "changed_paths", _tuple_strings(self.changed_paths, "changed_paths"))
        object.__setattr__(self, "fact_refs", _tuple_strings(self.fact_refs, "fact_refs"))
        object.__setattr__(self, "artifact_refs", _tuple_strings(self.artifact_refs, "artifact_refs"))
        if self.receipt_id is not None:
            object.__setattr__(self, "receipt_id", _nonempty(self.receipt_id, "receipt_id"))


def _authority_refs(guidance: Mapping[str, Any], explicit: Sequence[str] | None) -> tuple[str, ...]:
    if explicit is not None:
        return _tuple_strings(explicit, "authority_refs")
    authority = guidance.get("authority")
    if not isinstance(authority, Mapping):
        raise GovernedExecutorError("matched guidance lacks authority")
    raw = authority.get("authority_refs")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise GovernedExecutorError("guidance authority_refs are invalid")
    refs: list[str] = []
    for item in raw:
        if isinstance(item, Mapping):
            refs.append(_nonempty(item.get("path"), "authority_refs[].path"))
        else:
            refs.append(_nonempty(item, "authority_refs[]"))
    return _tuple_strings(refs, "authority_refs")


def prepare_governed_operation(
    attempt: object,
    guidance: Mapping[str, Any],
    bounded_payload: object,
    payload_schema_ref: str = "payload.v1",
    authority_refs: Sequence[str] | None = None,
    guidance_ref: str | None = None,
) -> GovernedExecutionEnvelopeV1:
    """Construct one immutable envelope from already-selected live inputs."""

    if not isinstance(guidance, Mapping):
        raise GovernedExecutorError("guidance must be a mapping")
    if guidance.get("outcome") != "MATCHED":
        raise GovernedExecutorError("guidance is not a matched operation")
    operation = guidance.get("operation")
    if not isinstance(operation, Mapping):
        raise GovernedExecutorError("matched guidance lacks operation")
    operation_id = _nonempty(operation.get("operation_id"), "operation.operation_id")
    attempt_id, task_id = _attempt_identity(attempt)
    attempt_guidance_ref = _attribute(attempt, "operation_guidance_ref")
    resolved_guidance_ref = _guidance_ref(attempt, guidance, guidance_ref)
    if isinstance(attempt_guidance_ref, str) and attempt_guidance_ref and resolved_guidance_ref != attempt_guidance_ref:
        raise GovernedExecutorError("guidance does not preserve Attempt operation_guidance_ref")
    if not isinstance(bounded_payload, (Mapping, list, tuple, str, int, bool)) and bounded_payload is not None:
        raise GovernedExecutorError("bounded_payload is not a bounded JSON value")
    return GovernedExecutionEnvelopeV1(
        schema_version=SCHEMA_VERSION,
        contract_version=CONTRACT_VERSION,
        attempt_id=attempt_id,
        operation_id=operation_id,
        task_or_operation_id=task_id,
        guidance_ref=resolved_guidance_ref,
        guidance_digest=_guidance_digest(guidance),
        authority_refs=_authority_refs(guidance, authority_refs),
        bounded_payload_digest=canonical_digest(bounded_payload),
        payload_schema_ref=_nonempty(payload_schema_ref, "payload_schema_ref"),
    )


def _completion_from_mapping(value: Mapping[str, Any]) -> GovernedExecutionCompletionV1:
    fields = {field.name for field in GovernedExecutionCompletionV1.__dataclass_fields__.values()}
    if set(value) - fields:
        raise GovernedExecutorError("completion mapping contains unsupported fields")
    raw_inputs = value.get("evidence_content_inputs", ())
    if not isinstance(raw_inputs, (tuple, list)):
        raise GovernedExecutorError("evidence_content_inputs must be an ordered array")
    typed_inputs: list[EvidenceContentInputV1] = []
    for item in raw_inputs:
        if type(item) is EvidenceContentInputV1:
            typed_inputs.append(item)
        elif isinstance(item, Mapping) and set(item) == {"evidence_ref", "exact_raw_bytes"}:
            typed_inputs.append(EvidenceContentInputV1(item["evidence_ref"], item["exact_raw_bytes"]))
        else:
            raise GovernedExecutorError("EvidenceContentInputV1 mapping has an incorrect type or key set")
    values = {key: value[key] for key in fields if key in value and key != "evidence_content_inputs"}
    values["evidence_content_inputs"] = tuple(typed_inputs)
    return GovernedExecutionCompletionV1(**values)


def validate_governed_completion(
    envelope: GovernedExecutionEnvelopeV1,
    completion: GovernedExecutionCompletionV1 | Mapping[str, Any],
) -> GovernedExecutionResultV1:
    """Validate one completion against the exact envelope identity."""

    try:
        typed = completion if isinstance(completion, GovernedExecutionCompletionV1) else _completion_from_mapping(completion)
    except (TypeError, GovernedExecutorError) as exc:
        return GovernedExecutionResultV1(
            attempt_id=envelope.attempt_id,
            execution_invocation_id=envelope.execution_invocation_id,
            accepted=False,
            outcome="REJECTED",
            failure_category="INVALID_EXECUTION_RESULT",
        )
    if typed.attempt_id != envelope.attempt_id or typed.execution_invocation_id != envelope.execution_invocation_id:
        return GovernedExecutionResultV1(
            attempt_id=envelope.attempt_id,
            execution_invocation_id=envelope.execution_invocation_id,
            accepted=False,
            outcome="REJECTED",
            failure_category="ATTEMPT_IDENTITY_MISMATCH",
        )
    if typed.envelope_digest != envelope.envelope_digest or typed.operation_id != envelope.operation_id or typed.task_or_operation_id != envelope.task_or_operation_id:
        return GovernedExecutionResultV1(
            attempt_id=envelope.attempt_id,
            execution_invocation_id=envelope.execution_invocation_id,
            accepted=False,
            outcome="REJECTED",
            failure_category="ATTEMPT_IDENTITY_MISMATCH",
        )
    return GovernedExecutionResultV1(
        attempt_id=typed.attempt_id,
        execution_invocation_id=typed.execution_invocation_id,
        accepted=True,
        outcome=typed.execution_status,
        result_id=typed.result_id,
        execution_status=typed.execution_status,
        operation_id=typed.operation_id,
        task_or_operation_id=typed.task_or_operation_id,
        envelope_digest=typed.envelope_digest,
        changed_paths=typed.changed_paths,
        fact_refs=typed.fact_refs,
        artifact_refs=typed.artifact_refs,
        receipt_id=typed.receipt_id,
        completion=typed,
    )


def invoke_governed_operation(
    attempt: object,
    guidance: Mapping[str, Any],
    bounded_payload: object,
    completion: GovernedExecutionCompletionV1 | Mapping[str, Any] | None = None,
    payload_schema_ref: str = "payload.v1",
    authority_refs: Sequence[str] | None = None,
    guidance_ref: str | None = None,
    *,
    dependency_input: GovernedExecutionDependencyInputV1 | None = None,
) -> GovernedExecutionResultV1:
    """Perform one synchronous bounded invocation with optional transient input.

    The current host supplies ``completion`` as already-observed typed facts.
    The optional dependency input is exact typed transient data supplied after
    the caller-owned claim/join boundary, does not alter the execution
    envelope, and is supported only for T-02. This owner checks shape only; it
    does not resolve governance, routes, storage, or authority. There is
    intentionally no callback, worker, retry, receipt, or persistence fallback.
    """

    if dependency_input is not None:
        if type(dependency_input) is not GovernedExecutionDependencyInputV1:
            raise GovernedExecutorError(
                "dependency_input must be exact GovernedExecutionDependencyInputV1 or None"
            )
        if _attribute(attempt, "task_or_operation_id") != "T-02":
            raise GovernedExecutorError("dependency_input is supported only for T-02")

    try:
        envelope = prepare_governed_operation(
            attempt,
            guidance,
            bounded_payload,
            payload_schema_ref,
            authority_refs,
            guidance_ref,
        )
    except GovernedExecutorError:
        attempt_id = _attribute(attempt, "attempt_id", "UNKNOWN")
        return GovernedExecutionResultV1(
            attempt_id=attempt_id if isinstance(attempt_id, str) and attempt_id else "UNKNOWN",
            execution_invocation_id=None,
            accepted=False,
            outcome="REJECTED",
            failure_category="INVOCATION_REJECTED",
        )
    if completion is None:
        return GovernedExecutionResultV1(
            attempt_id=envelope.attempt_id,
            execution_invocation_id=envelope.execution_invocation_id,
            accepted=False,
            outcome="REJECTED",
            failure_category="EXECUTOR_UNAVAILABLE",
            operation_id=envelope.operation_id,
            task_or_operation_id=envelope.task_or_operation_id,
            envelope_digest=envelope.envelope_digest,
        )
    return validate_governed_completion(envelope, completion)


__all__ = [
    "CONTRACT_VERSION",
    "EXECUTION_STATUSES",
    "FAILURE_CATEGORIES",
    "EvidenceContentInputV1",
    "GovernedExecutionCompletionV1",
    "GovernedExecutionDependencyInputV1",
    "GovernedExecutionEnvelopeV1",
    "GovernedExecutionResultV1",
    "GovernedExecutorError",
    "canonical_digest",
    "canonical_json",
    "invoke_governed_operation",
    "prepare_governed_operation",
    "validate_governed_completion",
]
