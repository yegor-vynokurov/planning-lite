"""Authoritative PL09 Attempt Runtime persistence and access boundary.

This module owns the target-local Attempt Runtime store, its one policy-resolved
V2 mutation lock, and every proof-control/admission state transition. Under
that lock it orders deterministic cancellation tombstones, first proof CURRENT
installation, exact owner invalidation, and the shared A/B admission
materializer. Blob publication alone never grants CURRENT; invalidation is
monotonic; cancellation before CURRENT creates no synthetic control, while
cancellation afterward preserves the head and attaches only its tombstone
pointer. Every store write uses atomic replacement and strict canonical
readback before releasing the lock.

Runtime re-resolves governance, Attempt and Preparation rows, owner
Authorization, the sole Workspace artifact route, and exact raw artifact bytes
inside the critical section. It delegates immutable proof/tombstone carriers
and pure admission construction to ``dependency_admission``. It does not issue
Authorization, rerun PL08, execute work, add a second lock/store, change V1
claim/terminal/Recovery behavior, or integrate the future T-07 producer. The
exported ``claim_attempt`` is the dependent V2 gate: own Preparation remains
authority, persisted admission is eligibility only, every decisive join is
fresh under the existing V2 lock, and failure never repairs evidence. A
successful claim is not revoked by later proof invalidation. Independent V2
and legacy Attempt operations retain their existing behavior.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, replace
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from typing import Any, BinaryIO

from .attempt_evaluation import (
    AttemptEvaluationError,
    AttemptRecordV1,
    CandidateIdentityV1,
    DirtyPathEntryV1,
    IdentityRefV1,
    ObservedResultV1,
    VerifierContractIdentity,
    allocate_attempt_ordinal,
    canonical_json_bytes,
)
from .authorization import (
    AuthorizationRecordV2,
    AuthorizationAction,
    DependencyProofInvalidationScopeV1,
    PreparationScopeV1,
    PreparationScopeV2,
    RecoveryScopeV1,
    ResolutionOutcome as AuthorizationResolutionOutcome,
    resolve_authorization,
)
from .dependency_admission import (
    CancellationCarrierError,
    CancellationTombstoneV1,
    DependencyAdmissionError,
    DependencyProofCarrierError,
    DependencyProofError,
    DependencyAcceptanceProofV1,
    DependencyResolution,
    build_dependency_admission,
    validate_dependency_admission,
    cancellation_tombstone_ref,
    publish_dependency_acceptance_proof_blob,
    _publish_cancellation_tombstone_locked,
    resolve_dependency_acceptance_proof_blob,
    resolve_cancellation_tombstone,
    resolve_dependency,
)
from .workspace import WorkspaceError, load_effective_policy, resolve_dependency_artifact_output_route


SCHEMA_VERSION = 1
RUNTIME_STATES = frozenset({"ACTIVATABLE", "IN_FLIGHT", "TERMINAL"})
TERMINAL_STATUSES = frozenset({"COMPLETED", "FAILED", "INTERRUPTED", "INVALID"})
ATTEMPT_ID_PATTERN = re.compile(r"[^/\s]+/[^/\s]+/A[1-9][0-9]*\Z")
AUTHORIZATION_REF_PATTERN = re.compile(r"authz_[0-9a-f]{32}\Z")

STORE_KEYS = frozenset({"schema_version", "attempts"})
V2_STORE_KEYS = STORE_KEYS
ENVELOPE_KEYS = frozenset(
    {"attempt", "runtime_state", "observed_result", "recovery_authorization_ref"}
)
V2_ENVELOPE_KEYS = frozenset(
    {"attempt", "runtime_state", "observed_result", "recovery_authorization_ref", "dependency_edge_control"}
)
ATTEMPT_KEYS = frozenset(
    {
        "schema_version",
        "attempt_id",
        "change_id",
        "task_or_operation_id",
        "attempt_ordinal",
        "authorization_ref",
        "acceptance_contract_ref",
        "operation_guidance_ref",
        "candidate_identity",
        "baseline_refs",
        "prompt_composition_ref",
        "parent_attempt_ref",
        "addresses_finding_refs",
        "observed_result_ref",
        "verifier_contract_refs",
    }
)
V2_ATTEMPT_KEYS = ATTEMPT_KEYS | frozenset({"preparation_binding", "dependency_admission"})
PREPARATION_BINDING_KEYS = frozenset(
    {
        "authorization_ref",
        "plan_ref",
        "tasks_ref",
        "approved_plan_digest",
        "dependency_semantic_digest",
        "requirement_id",
        "dependency_classification",
        "expected_attempt_id",
    }
)
DEPENDENCY_EDGE_CONTROL_KEYS = frozenset(
    {
        "schema_version",
        "change_id",
        "source_task_or_operation_id",
        "source_attempt_id",
        "successor_task_or_operation_id",
        "successor_attempt_id",
        "dependency_semantic_digest",
        "proof_head",
        "cancellation_tombstone_ref",
    }
)
PROOF_HEAD_KEYS = frozenset(
    {"schema_version", "state", "proof_id", "proof_digest", "invalidation_authorization_ref"}
)
DEPENDENCY_ADMISSION_KEYS = frozenset(
    {
        "schema_version",
        "admission_id",
        "requirement_id",
        "change_id",
        "source_task_or_operation_id",
        "source_attempt_id",
        "successor_task_or_operation_id",
        "successor_attempt_id",
        "dependency_semantic_digest",
        "observed_result_id",
        "acceptance_proof_id",
        "acceptance_proof_digest",
        "technical_evaluation_id",
        "technical_evaluation_outcome",
        "acceptance_contract_ref",
        "acceptance_contract_digest",
        "evaluation_scope_ref",
        "required_verifier_contract_refs",
        "artifact_logical_ref",
        "artifact_digest",
        "required_successor_input_logical_ref",
        "eligible_outcome",
    }
)
OBSERVED_RESULT_KEYS = frozenset(
    {
        "schema_version",
        "result_id",
        "attempt_id",
        "execution_status",
        "changed_paths",
        "fact_refs",
        "artifact_refs",
    }
)

ReplacementHook = Callable[[str], None]


class AttemptRuntimeError(ValueError):
    """Fail-closed runtime, codec, authorization, or storage error."""


class AttemptStoreCorruptError(AttemptRuntimeError):
    """The authoritative store cannot be decoded as one valid document."""


class AttemptNotFoundError(AttemptRuntimeError):
    """An exact Attempt or required authoritative store was not found."""


class AttemptStateError(AttemptRuntimeError):
    """A requested state transition is not admissible for the exact Attempt."""


class AttemptAuthorizationError(AttemptRuntimeError):
    """The supplied authorization is not applicable to the requested action."""


class CancellationOutcome(str, Enum):
    """Transient result of the one locked fixed-edge cancellation observation."""

    CLEAR = "CLEAR"
    BLOCKED = "BLOCKED"


@dataclass(frozen=True)
class CancellationObservationV1:
    """Resolver-backed cancellation result; this is not persisted runtime state."""

    change_id: str
    requested_task_id: str
    observed_status: str
    outcome: CancellationOutcome
    tombstone_ref: str | None


class LookupOutcome(str, Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    INVALID_ID = "INVALID_ID"
    CORRUPT_CONFLICT = "CORRUPT_CONFLICT"


class AdmissibilityOutcome(str, Enum):
    ADMISSIBLE = "ADMISSIBLE"
    INVALID_ID = "INVALID_ID"
    NOT_FOUND = "NOT_FOUND"
    CORRUPT_CONFLICT = "CORRUPT_CONFLICT"
    INVALID_RECORD = "INVALID_RECORD"
    IN_FLIGHT = "IN_FLIGHT"
    TERMINAL = "TERMINAL"


class DependencyAdmissionOutcome(str, Enum):
    """The eight transient outcomes of the one shared A/B admission transition."""

    MATERIALIZED = "MATERIALIZED"
    ALREADY_MATERIALIZED = "ALREADY_MATERIALIZED"
    DEFERRED_SUCCESSOR_NOT_PREPARED = "DEFERRED_SUCCESSOR_NOT_PREPARED"
    DEFERRED_PREDECESSOR_PROOF_NOT_CURRENT = "DEFERRED_PREDECESSOR_PROOF_NOT_CURRENT"
    BLOCKED_PROOF_INVALIDATED = "BLOCKED_PROOF_INVALIDATED"
    BLOCKED_CANCELLATION = "BLOCKED_CANCELLATION"
    BLOCKED_STALE_DEPENDENCY = "BLOCKED_STALE_DEPENDENCY"
    BLOCK_CONFLICTING_ADMISSION = "BLOCK_CONFLICTING_ADMISSION"


@dataclass(frozen=True, slots=True)
class DependencyAdmissionMaterializationResultV1:
    """Transient exact A/B outcome; persisted Attempt state remains authoritative.

    Success returns the exact T-02/A1 and complete admission ID. The two
    deferred outcomes have Definition-v10's distinct nullable-ID shapes;
    blocked outcomes carry the exact successor ID when one exists and no
    admission ID. This value is never itself authority or durable state.
    """

    trigger: str
    outcome: DependencyAdmissionOutcome
    attempt_id: str | None
    admission_id: str | None
    schema_version: int = 1

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int or self.schema_version != 1 or self.trigger not in {"A", "B"}:
            raise AttemptRuntimeError("admission materialization result identity is invalid")
        if not isinstance(self.outcome, DependencyAdmissionOutcome):
            raise AttemptRuntimeError("admission materialization outcome is unsupported")
        if self.outcome is DependencyAdmissionOutcome.DEFERRED_SUCCESSOR_NOT_PREPARED:
            if self.attempt_id is not None or self.admission_id is not None:
                raise AttemptRuntimeError("missing-successor result requires null IDs")
        elif self.outcome is DependencyAdmissionOutcome.MATERIALIZED or self.outcome is DependencyAdmissionOutcome.ALREADY_MATERIALIZED:
            if self.attempt_id is None or self.admission_id is None:
                raise AttemptRuntimeError("successful admission result requires both exact IDs")
        else:
            if self.attempt_id is None or self.admission_id is not None:
                raise AttemptRuntimeError("deferred or blocked result requires successor ID and null admission ID")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "trigger": self.trigger,
            "outcome": self.outcome.value,
            "attempt_id": self.attempt_id,
            "admission_id": self.admission_id,
        }


@dataclass(frozen=True, slots=True)
class AttemptEnvelopeV1:
    """One persisted Attempt, its runtime state, and its terminal fact.

    ``attempt`` carries immutable materialization provenance.  A terminal
    transition adds the exact same-Attempt ``observed_result`` and updates the
    record's terminal-fact reference; recovery additionally persists the exact
    owner authorization reference beside that fact.
    """

    attempt: AttemptRecordV1
    runtime_state: str
    observed_result: ObservedResultV1 | None = None
    recovery_authorization_ref: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.attempt, AttemptRecordV1):
            raise AttemptRuntimeError("attempt envelope requires AttemptRecordV1")
        if self.runtime_state not in RUNTIME_STATES:
            raise AttemptRuntimeError("runtime_state is unsupported")
        if self.runtime_state == "TERMINAL":
            if not isinstance(self.observed_result, ObservedResultV1):
                raise AttemptRuntimeError("TERMINAL requires an ObservedResultV1")
            if self.observed_result.attempt_id != self.attempt.attempt_id:
                raise AttemptRuntimeError("terminal result belongs to another Attempt")
            if self.observed_result.execution_status not in TERMINAL_STATUSES:
                raise AttemptRuntimeError("terminal result status is unsupported")
            if self.attempt.observed_result_ref != self.observed_result.result_id:
                raise AttemptRuntimeError("terminal result reference is inconsistent")
        else:
            if self.observed_result is not None:
                raise AttemptRuntimeError("non-terminal Attempt cannot carry a result")
            if self.attempt.observed_result_ref is not None:
                raise AttemptRuntimeError("non-terminal Attempt cannot reference a result")
            if self.recovery_authorization_ref is not None:
                raise AttemptRuntimeError("non-terminal Attempt cannot carry recovery authority")
        if self.recovery_authorization_ref is not None and not AUTHORIZATION_REF_PATTERN.fullmatch(
            self.recovery_authorization_ref
        ):
            raise AttemptRuntimeError("recovery_authorization_ref is malformed")

    @property
    def attempt_id(self) -> str:
        return self.attempt.attempt_id

    @property
    def authorization_ref(self) -> str:
        return self.attempt.authorization_ref

    def to_mapping(self) -> dict[str, Any]:
        return {
            "attempt": self.attempt.to_mapping(),
            "runtime_state": self.runtime_state,
            "observed_result": self.observed_result.to_mapping() if self.observed_result else None,
            "recovery_authorization_ref": self.recovery_authorization_ref,
        }


@dataclass(frozen=True, slots=True)
class AttemptStoreV1:
    """The unchanged legacy V1 Attempt document, retained beside its V2 successor."""

    attempts: tuple[AttemptEnvelopeV1, ...] = ()
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise AttemptRuntimeError("unsupported Attempt Runtime schema_version")
        rows = tuple(self.attempts)
        if any(not isinstance(item, AttemptEnvelopeV1) for item in rows):
            raise AttemptRuntimeError("Attempt store contains an invalid envelope")
        ids = [item.attempt_id for item in rows]
        if len(set(ids)) != len(ids):
            raise AttemptStoreCorruptError("Attempt store contains duplicate Attempt identities")
        if ids != sorted(ids):
            raise AttemptStoreCorruptError("Attempt store records are not canonically ordered")
        object.__setattr__(self, "attempts", rows)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "attempts": [item.to_mapping() for item in self.attempts],
        }

    def by_id(self, attempt_id: str) -> AttemptEnvelopeV1 | None:
        return next((item for item in self.attempts if item.attempt_id == attempt_id), None)


@dataclass(frozen=True, slots=True)
class PreparationBindingV2:
    """The exact eight-field Preparation authority copied from immutable V2 Authorization.

    Runtime constructs this only from a resolved ``PreparationScopeV2``; no
    payload field can supply or replace its governance refs, digests,
    classification, or exact dependent Attempt identity.
    """

    authorization_ref: str
    plan_ref: str
    tasks_ref: str
    approved_plan_digest: str
    dependency_semantic_digest: str
    requirement_id: str
    dependency_classification: str
    expected_attempt_id: str | None

    def to_mapping(self) -> dict[str, Any]:
        return {
            "authorization_ref": self.authorization_ref,
            "plan_ref": self.plan_ref,
            "tasks_ref": self.tasks_ref,
            "approved_plan_digest": self.approved_plan_digest,
            "dependency_semantic_digest": self.dependency_semantic_digest,
            "requirement_id": self.requirement_id,
            "dependency_classification": self.dependency_classification,
            "expected_attempt_id": self.expected_attempt_id,
        }


@dataclass(frozen=True, slots=True)
class AttemptRecordV2:
    """Exact 17-key Attempt identity, retaining the V1 field meanings.

    The immutable Preparation binding is resolver-derived and remains attached
    for the record's lifetime. Exact dependent T-02/A1 may receive one complete
    immutable DependencyAdmissionV2 under Runtime's shared mutation lock;
    V1 and independent records never receive admission or edge control.
    """

    attempt_id: str
    change_id: str
    task_or_operation_id: str
    attempt_ordinal: int
    authorization_ref: str
    acceptance_contract_ref: str
    candidate_identity: CandidateIdentityV1
    baseline_refs: tuple[IdentityRefV1, ...]
    preparation_binding: PreparationBindingV2
    operation_guidance_ref: str | None = None
    prompt_composition_ref: str | None = None
    parent_attempt_ref: str | None = None
    addresses_finding_refs: tuple[str, ...] = ()
    observed_result_ref: str | None = None
    verifier_contract_refs: tuple[VerifierContractIdentity, ...] = ()
    dependency_admission: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.preparation_binding, PreparationBindingV2):
            raise AttemptRuntimeError("V2 Attempt requires PreparationBindingV2")
        if self.authorization_ref != self.preparation_binding.authorization_ref:
            raise AttemptRuntimeError("V2 Attempt authorization and Preparation binding differ")
        # Reuse the established V1 identity and nested PL08 contracts without
        # changing or re-encoding any persisted V1 record.
        self.as_v1()
        if (
            not re.fullmatch(r"[^/\s]+", self.change_id)
            or not re.fullmatch(r"[^/\s]+", self.task_or_operation_id)
            or not ATTEMPT_ID_PATTERN.fullmatch(self.attempt_id)
        ):
            raise AttemptRuntimeError("V2 Attempt IDs do not satisfy the exact identity grammar")
        binding = self.preparation_binding
        if binding.dependency_classification == "DEPENDENCY_EDGE_MEMBER":
            if (
                self.task_or_operation_id not in {"T-01", "T-02"}
                or self.attempt_ordinal != 1
                or self.parent_attempt_ref is not None
                or binding.expected_attempt_id != self.attempt_id
            ):
                raise AttemptRuntimeError("dependent V2 Attempt must be exact edge A1 with null parent")
        elif binding.dependency_classification == "NOT_APPLICABLE":
            if self.task_or_operation_id in {"T-01", "T-02"} or binding.expected_attempt_id is not None:
                raise AttemptRuntimeError("independent V2 Attempt has invalid edge identity")
        else:
            raise AttemptRuntimeError("V2 Preparation classification is unsupported")
        if self.dependency_admission is not None:
            validated_admission = _dependency_admission_from_mapping(self.dependency_admission, self)
            object.__setattr__(self, "dependency_admission", _freeze_json(validated_admission))

    def as_v1(self) -> AttemptRecordV1:
        """Return an ephemeral common-field view for the established PL08 contract."""
        try:
            return AttemptRecordV1(
                self.attempt_id,
                self.change_id,
                self.task_or_operation_id,
                self.attempt_ordinal,
                self.authorization_ref,
                self.acceptance_contract_ref,
                self.candidate_identity,
                self.baseline_refs,
                self.operation_guidance_ref,
                self.prompt_composition_ref,
                self.parent_attempt_ref,
                self.addresses_finding_refs,
                self.observed_result_ref,
                self.verifier_contract_refs,
            )
        except (AttemptEvaluationError, TypeError) as exc:
            raise AttemptRuntimeError("V2 Attempt common fields are invalid") from exc

    def to_mapping(self) -> dict[str, Any]:
        mapping = self.as_v1().to_mapping()
        mapping["schema_version"] = 2
        mapping["preparation_binding"] = self.preparation_binding.to_mapping()
        mapping["dependency_admission"] = _json_tree(self.dependency_admission)
        return mapping


@dataclass(frozen=True, slots=True)
class AttemptEnvelopeV2:
    """V2 Attempt lifecycle state and exact optional post-proof edge schema."""

    attempt: AttemptRecordV2
    runtime_state: str
    observed_result: ObservedResultV1 | None = None
    recovery_authorization_ref: str | None = None
    dependency_edge_control: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.attempt, AttemptRecordV2):
            raise AttemptRuntimeError("V2 envelope requires AttemptRecordV2")
        if not isinstance(self.runtime_state, str) or self.runtime_state not in RUNTIME_STATES:
            raise AttemptRuntimeError("runtime_state is unsupported")
        if self.runtime_state == "TERMINAL":
            if not isinstance(self.observed_result, ObservedResultV1):
                raise AttemptRuntimeError("TERMINAL requires an ObservedResultV1")
            if self.observed_result.attempt_id != self.attempt.attempt_id:
                raise AttemptRuntimeError("terminal result belongs to another Attempt")
            if self.observed_result.execution_status not in TERMINAL_STATUSES:
                raise AttemptRuntimeError("terminal result status is unsupported")
            if self.attempt.observed_result_ref != self.observed_result.result_id:
                raise AttemptRuntimeError("terminal result reference is inconsistent")
            if self.recovery_authorization_ref is not None and self.observed_result.execution_status != "INTERRUPTED":
                raise AttemptRuntimeError("Recovery authority may accompany only an INTERRUPTED V2 result")
        elif self.observed_result is not None or self.attempt.observed_result_ref is not None:
            raise AttemptRuntimeError("non-terminal V2 Attempt cannot carry a result")
        if self.runtime_state != "TERMINAL" and self.recovery_authorization_ref is not None:
            raise AttemptRuntimeError("non-terminal V2 Attempt cannot carry recovery authority")
        if self.recovery_authorization_ref is not None and not AUTHORIZATION_REF_PATTERN.fullmatch(
            self.recovery_authorization_ref
        ):
            raise AttemptRuntimeError("recovery_authorization_ref is malformed")
        if self.dependency_edge_control is not None:
            control = _dependency_edge_control_from_mapping(self.dependency_edge_control, self.attempt)
            object.__setattr__(self, "dependency_edge_control", _freeze_json(control))

    @property
    def attempt_id(self) -> str:
        return self.attempt.attempt_id

    @property
    def authorization_ref(self) -> str:
        return self.attempt.authorization_ref

    def to_mapping(self) -> dict[str, Any]:
        return {
            "attempt": self.attempt.to_mapping(),
            "runtime_state": self.runtime_state,
            "observed_result": self.observed_result.to_mapping() if self.observed_result else None,
            "recovery_authorization_ref": self.recovery_authorization_ref,
            "dependency_edge_control": _json_tree(self.dependency_edge_control),
        }


@dataclass(frozen=True, slots=True)
class AttemptStoreV2:
    """Canonical side-by-side V2 store; V1 bytes remain independently owned."""

    attempts: tuple[AttemptEnvelopeV2, ...] = ()
    schema_version: int = 2

    def __post_init__(self) -> None:
        if type(self.schema_version) is not int or self.schema_version != 2:
            raise AttemptRuntimeError("unsupported AttemptStoreV2 schema_version")
        rows = tuple(self.attempts)
        if any(not isinstance(item, AttemptEnvelopeV2) for item in rows):
            raise AttemptRuntimeError("V2 Attempt store contains an invalid envelope")
        ids = [item.attempt_id for item in rows]
        refs = [item.authorization_ref for item in rows]
        if len(set(ids)) != len(ids) or len(set(refs)) != len(refs):
            raise AttemptStoreCorruptError("V2 Attempt store contains duplicate identity or authorization")
        if ids != sorted(ids):
            raise AttemptStoreCorruptError("V2 Attempt store records are not canonically ordered")
        object.__setattr__(self, "attempts", rows)

    def to_mapping(self) -> dict[str, Any]:
        return {"schema_version": 2, "attempts": [item.to_mapping() for item in self.attempts]}

    def by_id(self, attempt_id: str) -> AttemptEnvelopeV2 | None:
        return next((item for item in self.attempts if item.attempt_id == attempt_id), None)


@dataclass(frozen=True, slots=True)
class AttemptLookupResultV1:
    """Stable exact-lookup result shape carrying either native V1 or V2 rows."""

    outcome: LookupOutcome
    envelope: AttemptEnvelopeV1 | AttemptEnvelopeV2 | None = None

    @property
    def attempt(self) -> AttemptRecordV1 | AttemptRecordV2 | None:
        return self.envelope.attempt if self.envelope else None

    @property
    def runtime_state(self) -> str | None:
        return self.envelope.runtime_state if self.envelope else None

    def to_mapping(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome.value,
            "attempt": self.envelope.to_mapping() if self.envelope else None,
        }


@dataclass(frozen=True, slots=True)
class AttemptAdmissibilityResultV1:
    """Pure state predicate result for one exact Attempt identity."""

    outcome: AdmissibilityOutcome
    envelope: AttemptEnvelopeV1 | AttemptEnvelopeV2 | None = None

    @property
    def admissible(self) -> bool:
        return self.outcome is AdmissibilityOutcome.ADMISSIBLE

    def to_mapping(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome.value,
            "attempt": self.envelope.to_mapping() if self.envelope else None,
        }


@dataclass(frozen=True, slots=True)
class MutationEvidenceV1:
    """Non-authoritative evidence returned after a verified store mutation."""

    store_path: str
    store_sha256: str
    attempt_id: str
    runtime_state: str

    def to_mapping(self) -> dict[str, str]:
        return {
            "store_path": self.store_path,
            "store_sha256": self.store_sha256,
            "attempt_id": self.attempt_id,
            "runtime_state": self.runtime_state,
        }


@dataclass(frozen=True, slots=True)
class _FrozenJsonObject(Mapping[str, Any]):
    """Small immutable JSON object used for typed inert future V2 subrecords."""

    _entries: tuple[tuple[str, Any], ...]

    def __getitem__(self, key: str) -> Any:
        for item_key, value in self._entries:
            if item_key == key:
                return value
        raise KeyError(key)

    def __iter__(self):
        return (key for key, _ in self._entries)

    def __len__(self) -> int:
        return len(self._entries)


def _freeze_json(value: Any) -> Any:
    if isinstance(value, Mapping):
        return _FrozenJsonObject(tuple((key, _freeze_json(item)) for key, item in value.items()))
    if isinstance(value, (list, tuple)):
        return tuple(_freeze_json(item) for item in value)
    return value


def _json_tree(value: Any) -> Any:
    """Return ordinary JSON containers for canonical encoding of immutable values."""
    if isinstance(value, Mapping):
        return {key: _json_tree(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_tree(item) for item in value]
    return value


_THREAD_LOCKS: dict[Path, threading.RLock] = {}
_THREAD_LOCKS_GUARD = threading.Lock()


def _thread_lock_for(path: Path) -> threading.RLock:
    key = path.resolve()
    with _THREAD_LOCKS_GUARD:
        return _THREAD_LOCKS.setdefault(key, threading.RLock())


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        return canonical_json_bytes(value) + b"\n"
    except AttemptEvaluationError as exc:
        raise AttemptRuntimeError("Attempt Runtime value is not canonical JSON") from exc


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AttemptStoreCorruptError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _strict_json(raw: bytes) -> Mapping[str, Any]:
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise AttemptStoreCorruptError("authoritative store must end with exactly one LF")
    try:
        text = raw[:-1].decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                AttemptStoreCorruptError(f"non-finite JSON constant: {value}")
            ),
        )
    except AttemptStoreCorruptError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise AttemptStoreCorruptError("authoritative store is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("authoritative store must be a JSON object")
    return value


def _keys(value: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    if set(value) != expected:
        raise AttemptStoreCorruptError(f"{label} has an unexpected key set")


def _version(value: Mapping[str, Any], label: str) -> None:
    if value.get("schema_version") != SCHEMA_VERSION:
        raise AttemptStoreCorruptError(f"{label} has an unsupported schema_version")


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or "\r" in value or "\n" in value:
        raise AttemptStoreCorruptError(f"{label} must be a non-empty stripped string")
    return value


def _optional_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def _dirty_path_from_mapping(value: object) -> DirtyPathEntryV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("dirty manifest entry must be an object")
    _keys(value, frozenset({"path", "change_kind", "content_identity", "source_path"}), "dirty manifest entry")
    identity = value.get("content_identity")
    if not isinstance(identity, Mapping):
        raise AttemptStoreCorruptError("dirty path content_identity must be an object")
    _keys(identity, frozenset({"before", "after"}), "dirty path content_identity")
    try:
        return DirtyPathEntryV1(
            value["path"],
            value["change_kind"],
            identity["before"],
            identity["after"],
            value["source_path"],
        )
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("dirty manifest entry is invalid") from exc


def _candidate_from_mapping(value: object) -> CandidateIdentityV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("candidate_identity must be an object")
    _keys(value, frozenset({"kind", "head", "dirty_manifest"}), "candidate_identity")
    manifest = value.get("dirty_manifest")
    if not isinstance(manifest, list):
        raise AttemptStoreCorruptError("candidate dirty_manifest must be a list")
    try:
        return CandidateIdentityV1(value["kind"], value["head"], tuple(_dirty_path_from_mapping(item) for item in manifest))
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("candidate_identity is invalid") from exc


def _identity_ref_from_mapping(value: object) -> IdentityRefV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("baseline reference must be an object")
    if set(value) != {"ref", "identity"}:
        raise AttemptStoreCorruptError("baseline reference has an unexpected key set")
    try:
        return IdentityRefV1(value["ref"], value["identity"])
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("baseline reference is invalid") from exc


def _attempt_from_mapping(value: object, *, require_authorization_pattern: bool = True) -> AttemptRecordV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("attempt must be an object")
    _keys(value, ATTEMPT_KEYS, "attempt")
    _version(value, "attempt")
    baseline = value.get("baseline_refs")
    findings = value.get("addresses_finding_refs")
    verifier_refs = value.get("verifier_contract_refs")
    if not isinstance(baseline, list) or not isinstance(findings, list) or not isinstance(verifier_refs, list):
        raise AttemptStoreCorruptError("attempt sequence fields are invalid")
    raw_verifier: list[VerifierContractIdentity] = []
    for item in verifier_refs:
        if not isinstance(item, Mapping) or set(item) != {"contract_id", "contract_version_or_ref"}:
            raise AttemptStoreCorruptError("verifier contract identity is invalid")
        raw_verifier.append((_text(item["contract_id"], "contract_id"), _text(item["contract_version_or_ref"], "contract_version_or_ref")))
    authorization_ref = value.get("authorization_ref")
    if require_authorization_pattern and (
        not isinstance(authorization_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(authorization_ref)
    ):
        raise AttemptStoreCorruptError("attempt authorization_ref is malformed")
    try:
        return AttemptRecordV1(
            value["attempt_id"],
            value["change_id"],
            value["task_or_operation_id"],
            value["attempt_ordinal"],
            authorization_ref,
            value["acceptance_contract_ref"],
            _candidate_from_mapping(value["candidate_identity"]),
            tuple(_identity_ref_from_mapping(item) for item in baseline),
            value["operation_guidance_ref"],
            value["prompt_composition_ref"],
            value["parent_attempt_ref"],
            tuple(findings),
            value["observed_result_ref"],
            tuple(raw_verifier),
        )
    except (AttemptEvaluationError, TypeError, KeyError) as exc:
        raise AttemptStoreCorruptError("attempt record is invalid") from exc


def _observed_result_from_mapping(value: object) -> ObservedResultV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("observed_result must be an object")
    _keys(value, OBSERVED_RESULT_KEYS, "observed_result")
    _version(value, "observed_result")
    changed = value.get("changed_paths")
    facts = value.get("fact_refs")
    artifacts = value.get("artifact_refs")
    if not isinstance(changed, list) or not isinstance(facts, list) or not isinstance(artifacts, list):
        raise AttemptStoreCorruptError("observed result sequence fields are invalid")
    try:
        return ObservedResultV1(
            value["result_id"],
            value["attempt_id"],
            value["execution_status"],
            tuple(changed),
            tuple(facts),
            tuple(artifacts),
        )
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("observed result is invalid") from exc


def _v2_int(value: object, label: str, *, expected: int | None = None) -> int:
    if type(value) is not int or (expected is not None and value != expected):
        raise AttemptStoreCorruptError(f"{label} must be integer {expected}" if expected is not None else f"{label} must be an integer")
    return value


def _digest(value: object, label: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise AttemptStoreCorruptError(f"{label} must be a lowercase SHA-256 digest")
    return value


def _binding_from_mapping(value: object) -> PreparationBindingV2:
    """Decode the exact immutable eight-field Authorization projection."""
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("preparation_binding must be an object")
    _keys(value, PREPARATION_BINDING_KEYS, "PreparationBindingV2")
    auth_ref = value["authorization_ref"]
    if not isinstance(auth_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(auth_ref):
        raise AttemptStoreCorruptError("PreparationBindingV2 authorization_ref is malformed")
    plan_ref = _text(value["plan_ref"], "plan_ref")
    tasks_ref = _text(value["tasks_ref"], "tasks_ref")
    approved_digest = _digest(value["approved_plan_digest"], "approved_plan_digest")
    dependency_digest = _digest(value["dependency_semantic_digest"], "dependency_semantic_digest")
    requirement = value["requirement_id"]
    if not isinstance(requirement, str) or not re.fullmatch(r"dreq_[0-9a-f]{64}", requirement):
        raise AttemptStoreCorruptError("PreparationBindingV2 requirement_id is malformed")
    classification = value["dependency_classification"]
    if not isinstance(classification, str) or classification not in {"DEPENDENCY_EDGE_MEMBER", "NOT_APPLICABLE"}:
        raise AttemptStoreCorruptError("PreparationBindingV2 classification is unsupported")
    expected = value["expected_attempt_id"]
    if expected is not None:
        if not isinstance(expected, str) or not ATTEMPT_ID_PATTERN.fullmatch(expected):
            raise AttemptStoreCorruptError("PreparationBindingV2 expected_attempt_id is malformed")
    return PreparationBindingV2(
        auth_ref,
        plan_ref,
        tasks_ref,
        approved_digest,
        dependency_digest,
        requirement,
        classification,
        expected,
    )


def _observed_result_v2_from_mapping(value: object) -> ObservedResultV1:
    """Decode the existing exact V1 result schema with strict V2 integer rules."""
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("V2 observed_result must be an object")
    _v2_int(value.get("schema_version"), "ObservedResultV1.schema_version", expected=1)
    return _observed_result_from_mapping(value)


def _proof_head_from_mapping(value: object) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("proof_head must be an object")
    _keys(value, PROOF_HEAD_KEYS, "proof_head")
    _v2_int(value["schema_version"], "proof_head.schema_version", expected=1)
    state = value["state"]
    proof_id = value["proof_id"]
    proof_digest = _digest(value["proof_digest"], "proof_head.proof_digest")
    invalidation_ref = value["invalidation_authorization_ref"]
    if not isinstance(state, str) or state not in {"CURRENT", "INVALIDATED"}:
        raise AttemptStoreCorruptError("proof_head state is unsupported")
    if proof_id != f"dproof_{proof_digest}":
        raise AttemptStoreCorruptError("proof_head identity is inconsistent")
    if state == "CURRENT" and invalidation_ref is not None:
        raise AttemptStoreCorruptError("CURRENT proof_head cannot carry invalidation authority")
    if state == "INVALIDATED" and (
        not isinstance(invalidation_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(invalidation_ref)
    ):
        raise AttemptStoreCorruptError("INVALIDATED proof_head requires exact invalidation authority")
    return dict(value)


def _dependency_edge_control_from_mapping(
    value: object, attempt: AttemptRecordV2
) -> Mapping[str, Any]:
    """Validate inert post-proof control shape without creating or advancing it."""
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("dependency_edge_control must be an object")
    _keys(value, DEPENDENCY_EDGE_CONTROL_KEYS, "DependencyEdgeControlV1")
    _v2_int(value["schema_version"], "DependencyEdgeControlV1.schema_version", expected=1)
    expected_source = f"{attempt.change_id}/T-01/A1"
    expected_successor = f"{attempt.change_id}/T-02/A1"
    if (
        value["change_id"] != attempt.change_id
        or value["source_task_or_operation_id"] != "T-01"
        or value["source_attempt_id"] != expected_source
        or value["successor_task_or_operation_id"] != "T-02"
        or value["successor_attempt_id"] != expected_successor
        or attempt.task_or_operation_id != "T-01"
        or attempt.attempt_id != expected_source
        or value["dependency_semantic_digest"] != attempt.preparation_binding.dependency_semantic_digest
    ):
        raise AttemptStoreCorruptError("DependencyEdgeControlV1 identity is inconsistent")
    cancellation_ref = value["cancellation_tombstone_ref"]
    if cancellation_ref is not None and (
        not isinstance(cancellation_ref, str) or not re.fullmatch(r"cancellation:[0-9a-f]{64}", cancellation_ref)
    ):
        raise AttemptStoreCorruptError("cancellation_tombstone_ref is malformed")
    proof_head = _proof_head_from_mapping(value["proof_head"])
    return {**dict(value), "proof_head": dict(proof_head)}


def _dependency_admission_from_mapping(
    value: object, attempt: AttemptRecordV2
) -> Mapping[str, Any]:
    """Validate the exact 22-key payload; only T-05 attaches it to dependent T-02/A1."""
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("dependency_admission must be an object")
    _keys(value, DEPENDENCY_ADMISSION_KEYS, "DependencyAdmissionV2")
    _v2_int(value["schema_version"], "DependencyAdmissionV2.schema_version", expected=2)
    semantic = dict(value)
    admission_id = semantic.pop("admission_id")
    if not isinstance(admission_id, str) or not re.fullmatch(r"dadm_[0-9a-f]{64}", admission_id):
        raise AttemptStoreCorruptError("DependencyAdmissionV2 admission_id is malformed")
    if admission_id != "dadm_" + hashlib.sha256(_canonical_v2_json(_json_tree(semantic))).hexdigest():
        raise AttemptStoreCorruptError("DependencyAdmissionV2 content identity is inconsistent")
    strings = DEPENDENCY_ADMISSION_KEYS - {"schema_version", "admission_id", "required_verifier_contract_refs"}
    for key in strings:
        _text(value[key], f"DependencyAdmissionV2.{key}")
    if value["schema_version"] != 2 or value["eligible_outcome"] != "ELIGIBLE_FOR_CLAIM_CHECK":
        raise AttemptStoreCorruptError("DependencyAdmissionV2 version or outcome is unsupported")
    verifier_refs = value["required_verifier_contract_refs"]
    if not isinstance(verifier_refs, (list, tuple)) or not verifier_refs:
        raise AttemptStoreCorruptError("DependencyAdmissionV2 verifier refs are invalid")
    parsed_verifiers: list[tuple[str, str]] = []
    for item in verifier_refs:
        if not isinstance(item, Mapping) or set(item) != {"contract_id", "contract_version_or_ref"}:
            raise AttemptStoreCorruptError("DependencyAdmissionV2 verifier identity is invalid")
        parsed_verifiers.append(
            (
                _text(item["contract_id"], "DependencyAdmissionV2.contract_id"),
                _text(item["contract_version_or_ref"], "DependencyAdmissionV2.contract_version_or_ref"),
            )
        )
    if len(set(parsed_verifiers)) != len(parsed_verifiers):
        raise AttemptStoreCorruptError("DependencyAdmissionV2 verifier identities are duplicated")
    if value["technical_evaluation_outcome"] != "SATISFIED":
        raise AttemptStoreCorruptError("DependencyAdmissionV2 technical outcome must be SATISFIED")
    if not re.fullmatch(r"dreq_[0-9a-f]{64}", value["requirement_id"]):
        raise AttemptStoreCorruptError("DependencyAdmissionV2 requirement_id is malformed")
    proof_digest = _digest(value["acceptance_proof_digest"], "DependencyAdmissionV2.acceptance_proof_digest")
    if value["acceptance_proof_id"] != f"dproof_{proof_digest}":
        raise AttemptStoreCorruptError("DependencyAdmissionV2 proof identity is inconsistent")
    for digest_field in ("dependency_semantic_digest", "acceptance_contract_digest", "artifact_digest"):
        _digest(value[digest_field], f"DependencyAdmissionV2.{digest_field}")
    for identity_field in ("source_attempt_id", "successor_attempt_id"):
        if not isinstance(value[identity_field], str) or not ATTEMPT_ID_PATTERN.fullmatch(value[identity_field]):
            raise AttemptStoreCorruptError(f"DependencyAdmissionV2.{identity_field} is malformed")
    if (
        value["change_id"] != attempt.change_id
        or attempt.task_or_operation_id != "T-02"
        or attempt.attempt_ordinal != 1
        or attempt.parent_attempt_ref is not None
        or value["source_task_or_operation_id"] != "T-01"
        or value["source_attempt_id"] != f"{attempt.change_id}/T-01/A1"
        or value["successor_task_or_operation_id"] != "T-02"
        or value["successor_attempt_id"] != attempt.attempt_id
        or value["requirement_id"] != attempt.preparation_binding.requirement_id
        or value["dependency_semantic_digest"] != attempt.preparation_binding.dependency_semantic_digest
        or attempt.preparation_binding.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
    ):
        raise AttemptStoreCorruptError("DependencyAdmissionV2 successor join is inconsistent")
    return dict(value)


def _attempt_v2_from_mapping(value: object) -> AttemptRecordV2:
    """Decode exact V2 Attempt keys while reusing the established V1 field rules."""
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("V2 attempt must be an object")
    _keys(value, V2_ATTEMPT_KEYS, "AttemptRecordV2")
    _v2_int(value["schema_version"], "AttemptRecordV2.schema_version", expected=2)
    legacy_mapping = {key: item for key, item in value.items() if key in ATTEMPT_KEYS}
    legacy_mapping["schema_version"] = 1
    base = _attempt_from_mapping(legacy_mapping)
    binding = _binding_from_mapping(value["preparation_binding"])
    try:
        return AttemptRecordV2(
            base.attempt_id,
            base.change_id,
            base.task_or_operation_id,
            base.attempt_ordinal,
            base.authorization_ref,
            base.acceptance_contract_ref,
            base.candidate_identity,
            base.baseline_refs,
            binding,
            base.operation_guidance_ref,
            base.prompt_composition_ref,
            base.parent_attempt_ref,
            base.addresses_finding_refs,
            base.observed_result_ref,
            base.verifier_contract_refs,
            value["dependency_admission"],
        )
    except AttemptRuntimeError as exc:
        raise AttemptStoreCorruptError("AttemptRecordV2 is inconsistent") from exc


def _envelope_v2_from_mapping(value: object) -> AttemptEnvelopeV2:
    """Validate the exact five-key envelope and its state/result/control joins."""
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("V2 Attempt envelope must be an object")
    _keys(value, V2_ENVELOPE_KEYS, "AttemptEnvelopeV2")
    attempt = _attempt_v2_from_mapping(value["attempt"])
    raw_result = value["observed_result"]
    result = None if raw_result is None else _observed_result_v2_from_mapping(raw_result)
    recovery_ref = value["recovery_authorization_ref"]
    if recovery_ref is not None and (
        not isinstance(recovery_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(recovery_ref)
    ):
        raise AttemptStoreCorruptError("V2 recovery authorization reference is malformed")
    control = value["dependency_edge_control"]
    if control is not None:
        control = _dependency_edge_control_from_mapping(control, attempt)
    try:
        return AttemptEnvelopeV2(attempt, value["runtime_state"], result, recovery_ref, control)
    except AttemptRuntimeError as exc:
        raise AttemptStoreCorruptError("V2 Attempt envelope is inconsistent") from exc


def _store_v2_from_mapping(value: object) -> AttemptStoreV2:
    """Decode the two-key V2 store, including sorted rows and unique refs."""
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("AttemptStoreV2 must be an object")
    _keys(value, V2_STORE_KEYS, "AttemptStoreV2")
    _v2_int(value["schema_version"], "AttemptStoreV2.schema_version", expected=2)
    raw_attempts = value["attempts"]
    if not isinstance(raw_attempts, list):
        raise AttemptStoreCorruptError("AttemptStoreV2 attempts must be a list")
    try:
        return AttemptStoreV2(tuple(_envelope_v2_from_mapping(item) for item in raw_attempts))
    except AttemptStoreCorruptError:
        raise
    except AttemptRuntimeError as exc:
        raise AttemptStoreCorruptError("AttemptStoreV2 is inconsistent") from exc


def _canonical_v2_json(value: Mapping[str, Any]) -> bytes:
    """Serialize new V2 mappings with the strict Definition-v7 JSON policy."""
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            allow_nan=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise AttemptRuntimeError("V2 Attempt Runtime value is not canonical JSON") from exc


def _strict_v2_json(raw: bytes) -> Mapping[str, Any]:
    """Parse V2 UTF-8/no-BOM bytes through duplicate-aware strict JSON loading."""
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AttemptStoreCorruptError("V2 Attempt store must not contain a UTF-8 BOM")
    return _strict_json(raw)


def _envelope_from_mapping(value: object) -> AttemptEnvelopeV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("Attempt envelope must be an object")
    _keys(value, ENVELOPE_KEYS, "Attempt envelope")
    attempt = _attempt_from_mapping(value["attempt"])
    raw_result = value["observed_result"]
    result = None if raw_result is None else _observed_result_from_mapping(raw_result)
    recovery_ref = value["recovery_authorization_ref"]
    if recovery_ref is not None and (
        not isinstance(recovery_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(recovery_ref)
    ):
        raise AttemptStoreCorruptError("recovery authorization reference is malformed")
    try:
        return AttemptEnvelopeV1(attempt, value["runtime_state"], result, recovery_ref)
    except AttemptRuntimeError as exc:
        raise AttemptStoreCorruptError("Attempt envelope is inconsistent") from exc


def _store_from_mapping(value: object) -> AttemptStoreV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("Attempt store must be an object")
    _keys(value, STORE_KEYS, "Attempt store")
    _version(value, "Attempt store")
    raw_attempts = value.get("attempts")
    if not isinstance(raw_attempts, list):
        raise AttemptStoreCorruptError("Attempt store attempts must be a list")
    try:
        return AttemptStoreV1(tuple(_envelope_from_mapping(item) for item in raw_attempts))
    except AttemptStoreCorruptError:
        raise
    except AttemptRuntimeError as exc:
        raise AttemptStoreCorruptError("Attempt store is inconsistent") from exc


def encode_attempt_store(store: AttemptStoreV1 | Mapping[str, Any]) -> bytes:
    """Strictly canonical-encode one complete Attempt Runtime document."""

    candidate = store if isinstance(store, AttemptStoreV1) else _store_from_mapping(store)
    raw = _canonical_bytes(candidate.to_mapping())
    # Re-decode the exact bytes so public encoding never produces an invalid
    # authoritative document, even when a future contract field is added.
    decoded = decode_attempt_store(raw)
    if decoded.to_mapping() != candidate.to_mapping():
        raise AttemptRuntimeError("Attempt store canonical round-trip changed the document")
    return raw


def decode_attempt_store(raw: bytes | bytearray | str | os.PathLike[str] | Path) -> AttemptStoreV1:
    """Strictly decode canonical store bytes, rejecting duplicates and drift."""

    if isinstance(raw, (str, os.PathLike, Path)):
        try:
            raw_bytes = Path(raw).read_bytes()
        except OSError as exc:
            raise AttemptStoreCorruptError("cannot read Attempt Runtime store") from exc
    elif isinstance(raw, (bytes, bytearray)):
        raw_bytes = bytes(raw)
    else:
        raise AttemptStoreCorruptError("Attempt Runtime input must be bytes or a path")
    value = _strict_json(raw_bytes)
    store = _store_from_mapping(value)
    if _canonical_bytes(store.to_mapping()) != raw_bytes:
        raise AttemptStoreCorruptError("Attempt Runtime store is not canonical")
    return store


def encode_attempt_store_v2(store: AttemptStoreV2 | Mapping[str, Any]) -> bytes:
    """Encode one complete V2 store using its independent strict canonical codec."""
    candidate = store if isinstance(store, AttemptStoreV2) else _store_v2_from_mapping(store)
    raw = _canonical_v2_json(candidate.to_mapping()) + b"\n"
    if decode_attempt_store_v2(raw).to_mapping() != candidate.to_mapping():
        raise AttemptRuntimeError("AttemptStoreV2 canonical round-trip changed the document")
    return raw


def decode_attempt_store_v2(raw: bytes | bytearray | str | os.PathLike[str] | Path) -> AttemptStoreV2:
    """Strictly decode V2 bytes; reject BOM, duplicate keys, schema drift and noncanonical JSON."""
    if isinstance(raw, (str, os.PathLike, Path)):
        try:
            raw_bytes = Path(raw).read_bytes()
        except OSError as exc:
            raise AttemptStoreCorruptError("cannot read AttemptStoreV2") from exc
    elif isinstance(raw, (bytes, bytearray)):
        raw_bytes = bytes(raw)
    else:
        raise AttemptStoreCorruptError("AttemptStoreV2 input must be bytes or a path")
    value = _strict_v2_json(raw_bytes)
    store = _store_v2_from_mapping(value)
    if _canonical_v2_json(store.to_mapping()) + b"\n" != raw_bytes:
        raise AttemptStoreCorruptError("AttemptStoreV2 bytes are not canonical")
    return store


def attempt_store_path(target: str | os.PathLike[str] | Path) -> Path:
    """Resolve the one target-local store through effective project policy."""

    product_root = Path(target).expanduser().resolve()
    try:
        effective = load_effective_policy(product_root)
        policy = effective["project_policy"]
        planning_root = policy["planning_root"]
        if not isinstance(planning_root, str) or not planning_root:
            raise WorkspaceError("effective planning_root is invalid")
        path = (product_root / planning_root / "changes" / "active" / ".planning-lite" / "attempt-runtime.json").resolve()
        if not path.is_relative_to(product_root):
            raise WorkspaceError("Attempt Runtime store escapes product root")
        return path
    except (WorkspaceError, KeyError, TypeError) as exc:
        raise AttemptRuntimeError("cannot resolve effective Attempt Runtime store path") from exc


runtime_store_path = attempt_store_path


def attempt_store_v2_path(target: str | os.PathLike[str] | Path) -> Path:
    """Resolve side-by-side V2 persistence under the effective project policy.

    The path is the ``attempt-runtime-v2.json`` sibling of V1 and defines the
    existing path-keyed lock identity for every V2 Runtime mutation. Resolution
    is read-only; lookup never creates either store.
    """
    return attempt_store_path(target).with_name("attempt-runtime-v2.json")


def _lock_path(store: Path) -> Path:
    return store.with_name(f"{store.name}.lock")


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


@contextmanager
def _store_lock(store: Path, *, create: bool):
    """Hold the in-process and OS lock for the full mutation sequence.

    The sidecar is intentionally not a runtime state or a second store.  Its
    OS lock is held through replacement and reread so a process loss leaves
    the durable state exactly where the completed atomic replacement left it.
    """

    parent = store.parent
    if create:
        parent.mkdir(parents=True, exist_ok=True)
    elif not parent.is_dir():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    lock_path = _lock_path(store)
    with _thread_lock_for(store):
        handle: BinaryIO | None = None
        acquired = False
        try:
            handle = lock_path.open("a+b")
            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            acquired = True
            yield
        except (ImportError, OSError) as exc:
            if not acquired:
                raise AttemptRuntimeError(f"cannot acquire Attempt Runtime lock: {lock_path}") from exc
            raise AttemptRuntimeError("Attempt Runtime lock or mutation failed") from exc
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


def _observe_dependency_cancellation_locked(
    target: str | os.PathLike[str] | Path,
    change_id: str,
    task_id: str,
    v2_store: Path,
) -> CancellationObservationV1:
    """Re-resolve status and immutable cancellation while the V2 lock is held.

    Governance is the only source of task status. A pre-existing edge
    tombstone remains terminal after status edits; the first exact Cancelled
    observation publishes and strictly rereads one shared edge object before
    returning. If a CURRENT/INVALIDATED control already exists, it attaches
    only that exact tombstone ref under the same lock. Before a control exists
    it never creates an AttemptStore, Authorization, source Attempt, proof
    head, control record, or admission.
    """
    try:
        # The existing T-01 resolver owns the consumer-root governance route.
        # Keep the Runtime lock identity selected separately by effective
        # policy, then re-read its canonical active governance inside the lock.
        product_root = Path(target).expanduser().resolve()
        requested = resolve_dependency(product_root, task_id)
        if requested.change_id != change_id:
            raise AttemptRuntimeError("requested Change does not match the active governed Change")
        carrier_root = v2_store.parent
        if task_id not in {"T-01", "T-02"}:
            if requested.task_status == "Cancelled":
                raise AttemptRuntimeError("cancelled independent task cannot receive Preparation")
            return CancellationObservationV1(
                requested.change_id,
                task_id,
                requested.task_status,
                CancellationOutcome.CLEAR,
                None,
            )

        source = resolve_dependency(product_root, "T-01")
        successor = resolve_dependency(product_root, "T-02")
        tombstone = CancellationTombstoneV1(requested.change_id)
        existing = resolve_cancellation_tombstone(carrier_root, tombstone)
        if existing is not None:
            ref, _ = existing
            _persist_cancellation_pointer_locked(target, v2_store, requested.change_id, ref)
            return CancellationObservationV1(
                requested.change_id,
                task_id,
                "Cancelled" if "Cancelled" in {source.task_status, successor.task_status} else requested.task_status,
                CancellationOutcome.BLOCKED,
                ref,
            )
        if "Cancelled" in {source.task_status, successor.task_status}:
            published_ref, _ = _publish_cancellation_tombstone_locked(
                carrier_root,
                tombstone,
            )
            verified = resolve_cancellation_tombstone(carrier_root, tombstone)
            if verified is None or verified[0] != published_ref or verified[1] != tombstone:
                raise AttemptRuntimeError("cancellation tombstone failed strict durable reread")
            _persist_cancellation_pointer_locked(target, v2_store, requested.change_id, verified[0])
            return CancellationObservationV1(
                requested.change_id,
                task_id,
                "Cancelled",
                CancellationOutcome.BLOCKED,
                verified[0],
            )
        return CancellationObservationV1(
            requested.change_id,
            task_id,
            requested.task_status,
            CancellationOutcome.CLEAR,
            None,
        )
    except (DependencyAdmissionError, CancellationCarrierError) as exc:
        raise AttemptRuntimeError(f"dependency cancellation observation failed closed: {exc}") from exc


def observe_dependency_cancellation(
    target: str | os.PathLike[str] | Path,
    change_id: str,
    task_id: str,
) -> CancellationObservationV1:
    """Observe governed Preparation applicability under Runtime's V2 mutation lock.

    ``change_id`` and ``task_id`` are request identities only. The active
    Change, applicability, approved/reconciled Plan facts, and live status are
    re-derived inside this boundary. Exact T-01/T-02 cancellation shares the
    fixed-edge tombstone; an independent task remains outside that edge and
    does not invent a cancellation ref. The same V2 sibling lock is reserved
    for later mutations and is created before any V2 JSON store or source row.
    No unlocked tombstone writer is exposed. The transient result is clear
    with no ref or blocked with the exact immutable, strictly reread edge ref.
    """
    if not isinstance(change_id, str) or not change_id or change_id != change_id.strip():
        raise AttemptRuntimeError("cancellation observation requires an exact Change ID")
    if not isinstance(task_id, str) or not task_id or task_id != task_id.strip():
        raise AttemptRuntimeError("cancellation observation requires an exact task ID")
    store = attempt_store_v2_path(target)
    try:
        with _store_lock(store, create=True):
            return _observe_dependency_cancellation_locked(target, change_id, task_id, store)
    except AttemptRuntimeError:
        raise
    except OSError as exc:
        raise AttemptRuntimeError("cannot acquire or complete V2 cancellation mutation boundary") from exc


def _run_hook(hook: ReplacementHook | None, phase: str) -> None:
    if hook is not None:
        hook(phase)


def _safe_replace(
    store: Path,
    proposed: AttemptStoreV1 | AttemptStoreV2,
    *,
    attempt_id: str | None = None,
    hook: ReplacementHook | None = None,
) -> MutationEvidenceV1:
    """Atomically replace and strictly reread one complete V1 or V2 Runtime store.

    The caller holds that store's existing path-keyed Runtime lock. Encoding
    and decoding dispatch by schema while the same staging, fsync, atomic
    replacement, exact-byte reread, and fault-hook sequence protects both
    stores; V1 uses its unchanged codec and V2 uses its strict no-BOM codec.
    """

    is_v2 = isinstance(proposed, AttemptStoreV2)
    encode = encode_attempt_store_v2 if is_v2 else encode_attempt_store
    decode = decode_attempt_store_v2 if is_v2 else decode_attempt_store
    raw = encode(proposed)
    temporary: Path | None = None
    try:
        _run_hook(hook, "prepare")
        prefix = ".attempt-runtime-v2-" if is_v2 else ".attempt-runtime-"
        with tempfile.NamedTemporaryFile(mode="wb", dir=store.parent, prefix=prefix, suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        _run_hook(hook, "validate")
        validated = decode(raw)
        if validated.to_mapping() != proposed.to_mapping():
            raise AttemptRuntimeError("prepared Attempt Runtime bytes changed during validation")
        _run_hook(hook, "replace")
        os.replace(temporary, store)
        temporary = None
        _fsync_directory(store.parent)
        _run_hook(hook, "verify")
        verified_raw = store.read_bytes()
        verified = decode(verified_raw)
        if verified.to_mapping() != proposed.to_mapping() or verified_raw != raw:
            raise AttemptRuntimeError("verified Attempt Runtime bytes do not match the intended document")
        digest = hashlib.sha256(verified_raw).hexdigest()
        _run_hook(hook, "hash")
        changed = proposed.by_id(attempt_id) if attempt_id is not None else (proposed.attempts[-1] if proposed.attempts else None)
        if changed is None:
            raise AttemptRuntimeError("Attempt Runtime mutation has no resulting Attempt")
        return MutationEvidenceV1(str(store), digest, changed.attempt_id, changed.runtime_state)
    except AttemptRuntimeError:
        raise
    except (OSError, ValueError, TypeError) as exc:
        raise AttemptRuntimeError("Attempt Runtime safe replacement failed") from exc
    except Exception as exc:
        raise AttemptRuntimeError("Attempt Runtime safe replacement failed") from exc
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


def _persist_cancellation_pointer_locked(
    target: Path, store: Path, change_id: str, tombstone_ref: str
) -> None:
    """Attach only the immutable cancellation pointer when proof control exists.

    Caller holds Runtime's exact V2 mutation lock. Before proof CURRENT this
    is a no-op, preserving tombstone-only cancellation and avoiding synthetic
    control/head state. After CURRENT it atomically changes only the control's
    pointer; it preserves CURRENT/INVALIDATED and any existing admission.
    """
    if not store.exists():
        return
    current_v1, current_v2 = _read_authoritative_stores(target)
    source_id = f"{change_id}/T-01/A1"
    source = current_v2.by_id(source_id)
    if source is None or source.dependency_edge_control is None:
        return
    control = dict(source.dependency_edge_control)
    existing_ref = control["cancellation_tombstone_ref"]
    if existing_ref is not None and existing_ref != tombstone_ref:
        raise AttemptStoreCorruptError("source control contains a conflicting cancellation pointer")
    if existing_ref == tombstone_ref:
        return
    control["cancellation_tombstone_ref"] = tombstone_ref
    updated_source = replace(source, dependency_edge_control=control)
    proposed = AttemptStoreV2(
        tuple(sorted((updated_source if row.attempt_id == source_id else row for row in current_v2.attempts), key=lambda row: row.attempt_id))
    )
    _safe_replace(store, proposed, attempt_id=source_id)
    verified_v1, verified_v2 = _read_authoritative_stores(target)
    verified = verified_v2.by_id(source_id)
    if verified_v1 != current_v1 or verified is None or verified.dependency_edge_control is None:
        raise AttemptRuntimeError("cancellation pointer failed strict Runtime readback")
    if verified.dependency_edge_control["cancellation_tombstone_ref"] != tombstone_ref:
        raise AttemptRuntimeError("cancellation pointer readback differs from its tombstone")


def _exact_source_id(change_id: str) -> str:
    return f"{change_id}/T-01/A1"


def _exact_successor_id(change_id: str) -> str:
    return f"{change_id}/T-02/A1"


def _proof_mapping(proof: DependencyAcceptanceProofV1) -> dict[str, Any]:
    return proof.to_mapping()


def _resolve_current_requirement_locked(target: Path, change_id: str) -> tuple[Any, Any, Mapping[str, Any]]:
    """Re-resolve both edge statuses and the sole current dependent requirement.

    Caller holds the authoritative V2 lock. This is a fresh resolver call,
    never a cached pre-lock governance object; T-01 supplies current status and
    T-02 supplies the canonical fixed-edge requirement.
    """
    try:
        source = resolve_dependency(target, "T-01")
        successor = resolve_dependency(target, "T-02")
    except DependencyAdmissionError as exc:
        raise AttemptRuntimeError("current dependency governance cannot be resolved") from exc
    if source.change_id != change_id or successor.change_id != change_id:
        raise AttemptRuntimeError("active Change changed during locked dependency transition")
    requirement = successor.requirement
    if (
        successor.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
        or requirement.get("dependency_classification") != "DEPENDENCY_EDGE_MEMBER"
        or requirement.get("source_attempt_id") != _exact_source_id(change_id)
        or requirement.get("successor_attempt_id") != _exact_successor_id(change_id)
    ):
        raise AttemptRuntimeError("current requirement does not bind exact T-01/A1 -> T-02/A1")
    return source, successor, requirement


def _artifact_digest_inside_lock(target: Path, requirement: Mapping[str, Any]) -> str:
    """Use Workspace's sole route, then hash its exact current raw bytes."""
    try:
        route = resolve_dependency_artifact_output_route(target)
        if route.key.requirement_id != requirement.get("requirement_id"):
            raise AttemptRuntimeError("artifact route was derived from another current requirement")
        raw = route.path.read_bytes()
    except AttemptRuntimeError:
        raise
    except (WorkspaceError, OSError, AttributeError, TypeError) as exc:
        raise AttemptRuntimeError("current canonical artifact route or raw bytes are unavailable") from exc
    return hashlib.sha256(raw).hexdigest()


def _verify_source_proof_joins(
    source: AttemptEnvelopeV2,
    proof: DependencyAcceptanceProofV1,
    requirement: Mapping[str, Any],
    artifact_digest: str,
) -> None:
    """Require the exact terminal Attempt/result and full captured proof joins."""
    mapping = _proof_mapping(proof)
    if (
        source.attempt_id != _exact_source_id(source.attempt.change_id)
        or source.attempt.task_or_operation_id != "T-01"
        or source.attempt.attempt_ordinal != 1
        or source.attempt.parent_attempt_ref is not None
        or source.runtime_state != "TERMINAL"
        or source.observed_result is None
        or source.observed_result.execution_status != "COMPLETED"
        or source.attempt.observed_result_ref != source.observed_result.result_id
    ):
        raise AttemptRuntimeError("source Attempt is not exact completed T-01/A1")
    if (
        mapping["change_id"] != source.attempt.change_id
        or mapping["source_attempt_id"] != source.attempt_id
        or mapping["dependency_semantic_digest"] != requirement.get("dependency_semantic_digest")
        or source.attempt.preparation_binding.dependency_semantic_digest != requirement.get("dependency_semantic_digest")
    ):
        raise AttemptRuntimeError("proof, source Attempt, and current dependency digest differ")
    try:
        captured_result = mapping["observed_result"]
        captured_value = captured_result["value"]
        if captured_value != source.observed_result.to_mapping():
            raise AttemptRuntimeError("captured ObservedResult content differs from exact Runtime result")
        input_value = mapping["attempt_evaluation_input"]
        expected_candidate = source.attempt.candidate_identity.to_mapping()
        expected_baselines = [item.to_mapping() for item in source.attempt.baseline_refs]
        expected_verifiers = [
            {"contract_id": item[0], "contract_version_or_ref": item[1]}
            for item in source.attempt.verifier_contract_refs
        ]
        if (
            input_value["attempt_id"] != source.attempt_id
            or input_value["candidate_identity"] != expected_candidate
            or input_value["baseline_refs"] != expected_baselines
            or input_value["acceptance_contract_ref"] != source.attempt.acceptance_contract_ref
            or input_value["verifier_contract_refs"] != expected_verifiers
            or mapping["acceptance_contract_ref"] != source.attempt.acceptance_contract_ref
            or mapping["artifact_logical_ref"] != requirement.get("produced_artifact_logical_ref")
            or mapping["artifact_digest"] != artifact_digest
        ):
            raise AttemptRuntimeError("captured proof does not join exact Attempt, contract, or artifact bytes")
    except (KeyError, TypeError) as exc:
        raise AttemptRuntimeError("proof is missing an exact source-result join") from exc


def _locked_cancellation_ref(
    target: Path, store: Path, change_id: str, control: Mapping[str, Any] | None
) -> str | None:
    """Observe live cancellation and verify any persisted pointer/tombstone pair."""
    try:
        observation = _observe_dependency_cancellation_locked(target, change_id, "T-02", store)
    except AttemptRuntimeError:
        raise
    if observation.outcome is CancellationOutcome.BLOCKED:
        return observation.tombstone_ref
    if control is not None and control.get("cancellation_tombstone_ref") is not None:
        pointer = control["cancellation_tombstone_ref"]
        resolved = resolve_cancellation_tombstone(store.parent, CancellationTombstoneV1(change_id))
        if resolved is None or resolved[0] != pointer:
            raise AttemptStoreCorruptError("control cancellation pointer does not resolve to its exact tombstone")
        return pointer
    return None


@dataclass(frozen=True, slots=True)
class _DependentClaimEvidence:
    """Named snapshot of the exact independent facts required by D11."""

    source_governance: DependencyResolution
    successor_governance: DependencyResolution
    requirement: Mapping[str, Any]
    source: AttemptEnvelopeV2
    successor: AttemptEnvelopeV2
    proof: DependencyAcceptanceProofV1
    artifact_digest: str
    admission: Mapping[str, Any]


@dataclass(frozen=True, slots=True)
class _SourceEdgeClaimEvidence:
    """Fresh own-authority and edge/cancellation facts for source T-01/A1."""

    source_governance: DependencyResolution
    successor_governance: DependencyResolution
    requirement: Mapping[str, Any]
    source: AttemptEnvelopeV2


def _source_edge_claim_evidence_locked(
    target: Path,
    store: Path,
    current_v2: AttemptStoreV2,
    attempt_id: str,
    *,
    original_source: AttemptEnvelopeV2 | None = None,
) -> _SourceEdgeClaimEvidence:
    """Validate only T-01's own Preparation and the current fixed edge.

    This source claim shares the Runtime V2 lock with T-02, re-resolves the
    exact edge requirement, its own immutable Preparation, live status and the
    durable cancellation owner. It deliberately reads no proof, admission,
    artifact route/bytes, PL08 result, or successor-eligibility state.
    """
    if attempt_store_v2_path(target).resolve() != store.resolve():
        raise AttemptStateError("source claim lock no longer names the policy-resolved V2 store")
    source = current_v2.by_id(attempt_id)
    if source is None or source.runtime_state != "ACTIVATABLE":
        raise AttemptStateError("exact dependent source is not ACTIVATABLE")
    change_id = source.attempt.change_id
    source_id = _exact_source_id(change_id)
    if (
        attempt_id != source_id
        or source.attempt_id != source_id
        or source.attempt.task_or_operation_id != "T-01"
        or source.attempt.attempt_ordinal != 1
        or source.attempt.parent_attempt_ref is not None
        or source.attempt.preparation_binding.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
    ):
        raise AttemptStateError("source edge-member claim is limited to exact T-01/A1")
    if original_source is not None and source != original_source:
        raise AttemptStateError("T-01/A1 changed during the final locked reread")

    source_governance, successor_governance, requirement = _resolve_current_requirement_locked(
        target, change_id
    )
    if (
        source_governance.task_id != "T-01"
        or source_governance.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
        or successor_governance.task_id != "T-02"
        or requirement.get("change_id") != change_id
        or requirement.get("source_attempt_id") != source_id
        or requirement.get("successor_attempt_id") != _exact_successor_id(change_id)
    ):
        raise AttemptStateError("current governance does not describe the exact source dependency edge")
    expected_scope = _preparation_scope_from_binding(source.attempt)
    binding = source.attempt.preparation_binding
    if (
        binding.authorization_ref != source.authorization_ref
        or expected_scope.change_id != change_id
        or expected_scope.task_or_operation_id != "T-01"
        or expected_scope.plan_ref != source_governance.plan_ref
        or expected_scope.tasks_ref != source_governance.tasks_ref
        or expected_scope.dependency_semantic_digest != requirement["dependency_semantic_digest"]
        or expected_scope.requirement_id != requirement["requirement_id"]
        or expected_scope.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
        or expected_scope.expected_attempt_id != source_id
    ):
        raise AttemptAuthorizationError("T-01 Preparation binding does not exactly join current governance")
    _auth_or_raise(target, source.authorization_ref, AuthorizationAction.PREPARATION, expected_scope)

    cancellation_ref = _locked_cancellation_ref(
        target, store, change_id, source.dependency_edge_control
    )
    if cancellation_ref is not None or "Cancelled" in {
        source_governance.task_status,
        successor_governance.task_status,
    }:
        raise AttemptStateError("current cancellation status, tombstone, or pointer blocks source claim")
    return _SourceEdgeClaimEvidence(
        source_governance,
        successor_governance,
        dict(requirement),
        source,
    )


def _dependent_claim_artifact_digest_locked(
    target: Path, store: Path, requirement: Mapping[str, Any]
) -> str:
    """Re-derive Workspace's sole route and hash its exact bytes under claim lock."""
    try:
        route = resolve_dependency_artifact_output_route(target)
        expected_key = {
            "schema_version": 1,
            "change_id": requirement["change_id"],
            "source_task_or_operation_id": "T-01",
            "source_attempt_id": requirement["source_attempt_id"],
            "requirement_id": requirement["requirement_id"],
            "dependency_semantic_digest": requirement["dependency_semantic_digest"],
            "accepted_output_contract_ref": requirement["accepted_output_contract_ref"],
            "artifact_logical_ref": requirement["produced_artifact_logical_ref"],
        }
        expected_store = (
            route.effective_planning_root
            / "changes"
            / "active"
            / ".planning-lite"
            / "attempt-runtime-v2.json"
        ).resolve()
        if (
            route.key.to_mapping() != expected_key
            or route.product_root.resolve() != target.resolve()
            or expected_store != store.resolve()
        ):
            raise AttemptRuntimeError("canonical Workspace route does not join the locked current requirement")
        raw = route.path.read_bytes()
    except AttemptRuntimeError:
        raise
    except (DependencyAdmissionError, WorkspaceError, OSError, AttributeError, KeyError, TypeError) as exc:
        raise AttemptRuntimeError("canonical artifact route or exact raw bytes are unavailable") from exc
    return hashlib.sha256(raw).hexdigest()


def _dependent_claim_evidence_locked(
    target: Path,
    store: Path,
    current_v2: AttemptStoreV2,
    attempt_id: str,
    *,
    original_successor: AttemptEnvelopeV2 | None = None,
    original_source: AttemptEnvelopeV2 | None = None,
) -> _DependentClaimEvidence:
    """Evaluate all dependent claim joins from fresh canonical facts under one V2 lock.

    The successor's own current Preparation is execution authority. The
    existing admission is eligibility only. Every invocation re-resolves
    governance, cancellation, proof CURRENT/blob, Workspace route/raw bytes,
    and the complete admission; it never materializes or repairs evidence.
    """
    if attempt_store_v2_path(target).resolve() != store.resolve():
        raise AttemptStateError("claim lock no longer names the policy-resolved V2 store")
    successor = current_v2.by_id(attempt_id)
    if successor is None or successor.runtime_state != "ACTIVATABLE":
        raise AttemptStateError("exact dependent successor is not ACTIVATABLE")
    if (
        successor.attempt_id != _exact_successor_id(successor.attempt.change_id)
        or successor.attempt.task_or_operation_id != "T-02"
        or successor.attempt.attempt_ordinal != 1
        or successor.attempt.parent_attempt_ref is not None
        or successor.attempt.preparation_binding.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
    ):
        raise AttemptStateError("dependent claim is limited to exact T-02/A1")
    if original_successor is not None and successor != original_successor:
        raise AttemptStateError("T-02/A1 changed during the final locked reread")

    change_id = successor.attempt.change_id
    source_id = _exact_source_id(change_id)
    source = current_v2.by_id(source_id)
    if source is None:
        raise AttemptStateError("exact T-01/A1 source Attempt is absent")
    if original_source is not None and source != original_source:
        raise AttemptStateError("T-01/A1 proof control changed during the final locked reread")
    source_governance, successor_governance, requirement = _resolve_current_requirement_locked(target, change_id)
    if (
        successor_governance.task_id != "T-02"
        or successor_governance.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
        or requirement.get("change_id") != change_id
        or requirement.get("source_attempt_id") != source_id
        or requirement.get("successor_attempt_id") != attempt_id
    ):
        raise AttemptStateError("current governance does not describe exact dependent T-02/A1")

    binding = successor.attempt.preparation_binding
    expected_scope = PreparationScopeV2(
        change_id,
        "T-02",
        successor_governance.plan_ref,
        successor_governance.tasks_ref,
        successor_governance.approved_plan_digest,
        requirement["dependency_semantic_digest"],
        requirement["requirement_id"],
        "DEPENDENCY_EDGE_MEMBER",
        attempt_id,
    )
    if (
        binding.authorization_ref != successor.authorization_ref
        or _preparation_scope_from_binding(successor.attempt) != expected_scope
    ):
        raise AttemptAuthorizationError("T-02 Preparation binding does not exactly join current governance")
    _auth_or_raise(target, successor.authorization_ref, AuthorizationAction.PREPARATION, expected_scope)

    cancellation_ref = _locked_cancellation_ref(
        target, store, change_id, source.dependency_edge_control
    )
    if cancellation_ref is not None or "Cancelled" in {
        source_governance.task_status,
        successor_governance.task_status,
    }:
        raise AttemptStateError("current cancellation status, tombstone, or pointer blocks dependent claim")

    if (
        source.attempt.task_or_operation_id != "T-01"
        or source.attempt.attempt_ordinal != 1
        or source.attempt.parent_attempt_ref is not None
        or source.runtime_state != "TERMINAL"
    ):
        raise AttemptStateError("source is not exact terminal T-01/A1")
    control = source.dependency_edge_control
    if control is None:
        raise AttemptStateError("T-01/A1 has no canonical proof control head")
    head = control["proof_head"]
    if (
        head["state"] != "CURRENT"
        or control["change_id"] != change_id
        or control["source_attempt_id"] != source_id
        or control["successor_attempt_id"] != attempt_id
        or control["dependency_semantic_digest"] != requirement["dependency_semantic_digest"]
    ):
        raise AttemptStateError("exact T-01/A1 proof head is missing, conflicting, or INVALIDATED")
    proof = _proof_blob_locked(store, head["proof_id"])
    if proof.proof_id != head["proof_id"] or proof.proof_digest != head["proof_digest"]:
        raise AttemptStoreCorruptError("CURRENT proof head differs from its immutable proof blob")
    proof = DependencyAcceptanceProofV1.from_mapping(
        proof.to_mapping(), current_requirement=requirement
    )
    artifact_digest = _dependent_claim_artifact_digest_locked(target, store, requirement)
    _verify_source_proof_joins(source, proof, requirement, artifact_digest)

    admission = successor.attempt.dependency_admission
    if admission is None:
        raise AttemptStateError("complete persisted DependencyAdmissionV2 is required for claim")
    validate_dependency_admission(
        admission,
        proof,
        requirement,
        artifact_digest=artifact_digest,
    )
    return _DependentClaimEvidence(
        source_governance=source_governance,
        successor_governance=successor_governance,
        requirement=dict(requirement),
        source=source,
        successor=successor,
        proof=proof,
        artifact_digest=artifact_digest,
        admission=admission,
    )


def _proof_blob_locked(store: Path, proof_id: str) -> DependencyAcceptanceProofV1:
    try:
        proof = resolve_dependency_acceptance_proof_blob(store.parent, proof_id)
    except DependencyProofCarrierError as exc:
        raise AttemptStoreCorruptError("durable dependency proof carrier is corrupt") from exc
    if proof is None:
        raise AttemptStoreCorruptError("Runtime proof head has no durable proof blob")
    return proof


def publish_dependency_acceptance_proof(
    target: str | os.PathLike[str] | Path,
    proof: DependencyAcceptanceProofV1,
    *,
    fault_hook: ReplacementHook | None = None,
) -> DependencyAdmissionMaterializationResultV1:
    """Publish immutable proof bytes, then install first CURRENT under one lock.

    The blob is durably written and strictly reread before lock acquisition but
    remains inert until the exact T-01/A1 control head is atomically installed.
    Under the existing policy-resolved V2 lock Runtime executes all D6.3
    governance/status/tombstone/Attempt/result/route-byte rereads, rejects any
    prior or invalidated head, installs CURRENT once, verifies canonical
    readback, then invokes Trigger A through the shared materializer before
    unlocking. A pre-CURRENT cancellation leaves only the approved tombstone.
    This API does not rerun PL08, replace proof, or change V1 behavior.
    """
    if not isinstance(proof, DependencyAcceptanceProofV1):
        raise AttemptRuntimeError("DependencyAcceptanceProofV1 is required")
    product_root = Path(target).expanduser().resolve()
    store = attempt_store_v2_path(product_root)
    try:
        proof_id, durable = publish_dependency_acceptance_proof_blob(store.parent, proof)
    except (DependencyProofCarrierError, DependencyProofError) as exc:
        raise AttemptRuntimeError("immutable dependency proof publication failed closed") from exc
    if proof_id != proof.proof_id or durable.to_mapping() != proof.to_mapping():
        raise AttemptRuntimeError("durable proof readback differs from the submitted exact proof")
    try:
        with _store_lock(store, create=False):
            current_v1, current_v2 = _read_authoritative_stores(product_root)
            source_id = _exact_source_id(proof.to_mapping()["change_id"])
            source = current_v2.by_id(source_id)
            if source is None:
                raise AttemptNotFoundError("exact T-01/A1 source Attempt is absent")
            source_governance, successor_governance, requirement = _resolve_current_requirement_locked(
                product_root, source.attempt.change_id
            )
            fresh_proof = DependencyAcceptanceProofV1.from_mapping(
                durable.to_mapping(), current_requirement=requirement
            )
            cancellation = _locked_cancellation_ref(product_root, store, source.attempt.change_id, source.dependency_edge_control)
            if cancellation is not None:
                raise AttemptStateError("cancellation won before proof CURRENT installation")
            # Re-read both status records after the accepted shared cancellation
            # owner: status and tombstone are distinct checks in D6.3.
            if "Cancelled" in {source_governance.task_status, successor_governance.task_status}:
                raise AttemptStateError("current T-01/T-02 status blocks proof CURRENT installation")
            tombstone = resolve_cancellation_tombstone(store.parent, CancellationTombstoneV1(source.attempt.change_id))
            if tombstone is not None:
                raise AttemptStateError("deterministic cancellation tombstone blocks proof CURRENT installation")
            control = source.dependency_edge_control
            if control is not None:
                head = control["proof_head"]
                if head["state"] == "INVALIDATED":
                    raise AttemptStateError("INVALIDATED proof state cannot be restored")
                raise AttemptStateError("T-01/A1 already has a proof head; replacement is forbidden")
            artifact_digest = _artifact_digest_inside_lock(product_root, requirement)
            _verify_source_proof_joins(source, fresh_proof, requirement, artifact_digest)
            new_control = {
                "schema_version": 1,
                "change_id": source.attempt.change_id,
                "source_task_or_operation_id": "T-01",
                "source_attempt_id": source_id,
                "successor_task_or_operation_id": "T-02",
                "successor_attempt_id": _exact_successor_id(source.attempt.change_id),
                "dependency_semantic_digest": requirement["dependency_semantic_digest"],
                "proof_head": {
                    "schema_version": 1,
                    "state": "CURRENT",
                    "proof_id": fresh_proof.proof_id,
                    "proof_digest": fresh_proof.proof_digest,
                    "invalidation_authorization_ref": None,
                },
                "cancellation_tombstone_ref": None,
            }
            installed = replace(source, dependency_edge_control=new_control)
            proposed = AttemptStoreV2(
                tuple(sorted((installed if row.attempt_id == source_id else row for row in current_v2.attempts), key=lambda row: row.attempt_id))
            )
            _safe_replace(store, proposed, attempt_id=source_id, hook=fault_hook)
            verified_v1, verified_v2 = _read_authoritative_stores(product_root)
            verified = verified_v2.by_id(source_id)
            if (
                verified_v1 != current_v1
                or verified is None
                or _canonical_v2_json(_json_tree(verified.dependency_edge_control))
                != _canonical_v2_json(_json_tree(installed.dependency_edge_control))
            ):
                raise AttemptRuntimeError("proof CURRENT failed exact canonical Runtime readback")
            verified_proof = _proof_blob_locked(store, fresh_proof.proof_id)
            _, _, verified_requirement = _resolve_current_requirement_locked(product_root, source.attempt.change_id)
            verified_artifact_digest = _artifact_digest_inside_lock(product_root, verified_requirement)
            _verify_source_proof_joins(verified, verified_proof, verified_requirement, verified_artifact_digest)
            return materialize_dependency_admission_if_ready(
                product_root, trigger="A", _locked_store=store, fault_hook=fault_hook
            )
    except AttemptRuntimeError:
        raise
    except (DependencyAdmissionError, DependencyProofCarrierError, DependencyProofError, WorkspaceError, OSError) as exc:
        raise AttemptRuntimeError("proof CURRENT transition failed closed") from exc


def invalidate_dependency_proof(
    target: str | os.PathLike[str] | Path,
    authorization_ref: str,
    *,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV2:
    """Use exact owner Authorization to make one locked CURRENT->INVALIDATED transition.

    Runtime reopens the immutable Authorization and its exact ADR provenance
    at use time while holding the same V2 lock as cancellation and admission.
    Caller assertions cannot authorize the change. Only proof_head changes;
    cancellation pointer and any already-attached admission remain untouched.
    INVALIDATED is terminal and can never be restored to CURRENT.
    """
    if not isinstance(authorization_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(authorization_ref):
        raise AttemptAuthorizationError("exact invalidation Authorization ref is required")
    product_root = Path(target).expanduser().resolve()
    store = attempt_store_v2_path(product_root)
    try:
        with _store_lock(store, create=False):
            current_v1, current_v2 = _read_authoritative_stores(product_root)
            source_id = None
            for row in current_v2.attempts:
                if row.attempt.task_or_operation_id == "T-01" and row.attempt.attempt_ordinal == 1:
                    if source_id is not None:
                        raise AttemptStoreCorruptError("multiple T-01 source rows exist")
                    source_id = row.attempt_id
            if source_id is None:
                raise AttemptNotFoundError("exact T-01/A1 source Attempt is absent")
            source = current_v2.by_id(source_id)
            assert source is not None
            control = source.dependency_edge_control
            if control is None or control["proof_head"]["state"] != "CURRENT":
                raise AttemptStateError("only exact CURRENT proof state can be invalidated")
            head = control["proof_head"]
            proof = _proof_blob_locked(store, head["proof_id"])
            if proof.proof_digest != head["proof_digest"] or proof.to_mapping()["change_id"] != source.attempt.change_id:
                raise AttemptStoreCorruptError("invalidation proof identity differs from exact source head")
            _, _, requirement = _resolve_current_requirement_locked(product_root, source.attempt.change_id)
            proof = DependencyAcceptanceProofV1.from_mapping(proof.to_mapping(), current_requirement=requirement)
            scope = DependencyProofInvalidationScopeV1(
                source.attempt.change_id,
                source_id,
                _exact_successor_id(source.attempt.change_id),
                proof.proof_id,
            )
            authorization = resolve_authorization(
                product_root,
                authorization_ref,
                AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
                scope,
            )
            if authorization.outcome is AuthorizationResolutionOutcome.CORRUPT_CONFLICT:
                raise AttemptStoreCorruptError("invalidation Authorization or ADR provenance is corrupt")
            if authorization.outcome is not AuthorizationResolutionOutcome.AUTHORIZED or authorization.record is None:
                raise AttemptAuthorizationError(f"invalidation Authorization rejected: {authorization.outcome.value}")
            invalidated_control = dict(control)
            invalidated_control["proof_head"] = {
                "schema_version": 1,
                "state": "INVALIDATED",
                "proof_id": proof.proof_id,
                "proof_digest": proof.proof_digest,
                "invalidation_authorization_ref": authorization.record.authorization_ref,
            }
            updated = replace(source, dependency_edge_control=invalidated_control)
            proposed = AttemptStoreV2(
                tuple(sorted((updated if row.attempt_id == source_id else row for row in current_v2.attempts), key=lambda row: row.attempt_id))
            )
            _safe_replace(store, proposed, attempt_id=source_id, hook=fault_hook)
            verified_v1, verified_v2 = _read_authoritative_stores(product_root)
            verified = verified_v2.by_id(source_id)
            if (
                verified_v1 != current_v1
                or verified is None
                or _canonical_v2_json(_json_tree(verified.dependency_edge_control))
                != _canonical_v2_json(_json_tree(updated.dependency_edge_control))
            ):
                raise AttemptRuntimeError("proof invalidation failed exact canonical Runtime readback")
            _proof_blob_locked(store, proof.proof_id)
            return verified
    except AttemptRuntimeError:
        raise
    except (DependencyAdmissionError, DependencyProofCarrierError, DependencyProofError, WorkspaceError, OSError) as exc:
        raise AttemptRuntimeError("owner proof invalidation failed closed") from exc


def materialize_dependency_admission_if_ready(
    target: str | os.PathLike[str] | Path,
    *,
    trigger: str,
    _locked_store: Path | None = None,
    fault_hook: ReplacementHook | None = None,
) -> DependencyAdmissionMaterializationResultV1:
    """Run the one serialized A/B transition and attach one complete admission.

    ``trigger`` is only A (immediately after proof CURRENT) or B (immediately
    after exact T-02/A1 Preparation materialization). Internal callers pass
    the already-held policy-resolved V2 store lock identity; an external
    focused invocation acquires that same lock once. The transition rereads
    both Attempts, current Preparation use-state, proof/control/tombstone,
    current requirement and the sole Workspace route/raw bytes. It returns
    only Definition-v10's eight outcomes. Runtime constructs the complete
    admission from the dependency owner and atomically mutates only T-02/A1;
    identical content is idempotent, conflicting content is never rewritten.
    This is not a claim-time or background trigger, and it does not alter V1.
    """
    if trigger not in {"A", "B"}:
        raise AttemptRuntimeError("dependency admission accepts only exact Trigger A or B")
    product_root = Path(target).expanduser().resolve()
    store = attempt_store_v2_path(product_root)
    if _locked_store is None:
        try:
            with _store_lock(store, create=False):
                return materialize_dependency_admission_if_ready(
                    product_root, trigger=trigger, _locked_store=store, fault_hook=fault_hook
                )
        except AttemptRuntimeError:
            raise
        except OSError as exc:
            raise AttemptRuntimeError("cannot acquire admission Runtime lock") from exc
    if Path(_locked_store).resolve() != store.resolve():
        raise AttemptRuntimeError("admission transition was given a non-authoritative lock identity")

    current_v1, current_v2 = _read_authoritative_stores(product_root)
    try:
        current_governance = resolve_dependency(product_root, "T-02")
    except DependencyAdmissionError as exc:
        raise AttemptRuntimeError("current dependent requirement cannot be resolved") from exc
    change_id = current_governance.change_id
    source_id = _exact_source_id(change_id)
    successor_id = _exact_successor_id(change_id)
    source = current_v2.by_id(source_id)
    successor = current_v2.by_id(successor_id)
    if successor is None:
        if trigger == "A":
            return DependencyAdmissionMaterializationResultV1(
                trigger, DependencyAdmissionOutcome.DEFERRED_SUCCESSOR_NOT_PREPARED, None, None
            )
        raise AttemptNotFoundError("Trigger B requires exact T-02/A1 materialized from Preparation")
    if (
        successor.attempt_id != successor_id
        or successor.attempt.task_or_operation_id != "T-02"
        or successor.attempt.attempt_ordinal != 1
        or successor.attempt.parent_attempt_ref is not None
    ):
        raise AttemptStoreCorruptError("successor row is not exact T-02/A1")
    if source is not None and (
        source.attempt_id != source_id
        or source.attempt.task_or_operation_id != "T-01"
        or source.attempt.attempt_ordinal != 1
        or source.attempt.parent_attempt_ref is not None
    ):
        raise AttemptStoreCorruptError("source row is not exact T-01/A1")
    if successor.runtime_state != "ACTIVATABLE":
        return DependencyAdmissionMaterializationResultV1(
            trigger, DependencyAdmissionOutcome.BLOCKED_STALE_DEPENDENCY, successor_id, None
        )

    try:
        _, _, requirement = _resolve_current_requirement_locked(product_root, change_id)
    except AttemptRuntimeError:
        return DependencyAdmissionMaterializationResultV1(
            trigger, DependencyAdmissionOutcome.BLOCKED_STALE_DEPENDENCY, successor_id, None
        )
    binding = successor.attempt.preparation_binding
    if (
        binding.dependency_classification != "DEPENDENCY_EDGE_MEMBER"
        or binding.expected_attempt_id != successor_id
        or binding.requirement_id != requirement.get("requirement_id")
        or binding.dependency_semantic_digest != requirement.get("dependency_semantic_digest")
        or binding.plan_ref != current_governance.plan_ref
        or binding.tasks_ref != current_governance.tasks_ref
    ):
        return DependencyAdmissionMaterializationResultV1(
            trigger, DependencyAdmissionOutcome.BLOCKED_STALE_DEPENDENCY, successor_id, None
        )
    preparation_use = resolve_authorization(
        product_root,
        successor.authorization_ref,
        AuthorizationAction.PREPARATION,
        _preparation_scope_from_binding(successor.attempt),
    )
    if preparation_use.outcome is AuthorizationResolutionOutcome.CORRUPT_CONFLICT:
        raise AttemptStoreCorruptError("successor Preparation Authorization is corrupt")
    if preparation_use.outcome is not AuthorizationResolutionOutcome.AUTHORIZED or preparation_use.record is None:
        return DependencyAdmissionMaterializationResultV1(
            trigger, DependencyAdmissionOutcome.BLOCKED_STALE_DEPENDENCY, successor_id, None
        )

    if source is None or source.dependency_edge_control is None:
        if trigger == "B":
            return DependencyAdmissionMaterializationResultV1(
                trigger, DependencyAdmissionOutcome.DEFERRED_PREDECESSOR_PROOF_NOT_CURRENT, successor_id, None
            )
        raise AttemptNotFoundError("Trigger A requires the exact installed T-01/A1 proof head")
    control = source.dependency_edge_control
    head = control["proof_head"]
    proof = _proof_blob_locked(store, head["proof_id"])
    if head["proof_digest"] != proof.proof_digest:
        raise AttemptStoreCorruptError("source proof head and immutable proof digest differ")

    existing = successor.attempt.dependency_admission
    if existing is None:
        # D10 gives already-attached immutable state first priority. Otherwise
        # currentness and cancellation outcomes precede artifact freshness so
        # a stale route cannot mask the exact owner block that won the lock.
        if head["state"] == "INVALIDATED":
            invalidation_scope = DependencyProofInvalidationScopeV1(
                change_id, source_id, successor_id, proof.proof_id
            )
            invalidation = resolve_authorization(
                product_root,
                head["invalidation_authorization_ref"],
                AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
                invalidation_scope,
            )
            if invalidation.outcome is AuthorizationResolutionOutcome.CORRUPT_CONFLICT:
                raise AttemptStoreCorruptError("persisted invalidation Authorization/ADR is corrupt")
            if invalidation.outcome is not AuthorizationResolutionOutcome.AUTHORIZED:
                raise AttemptStoreCorruptError("INVALIDATED head lacks currently valid exact owner provenance")
            return DependencyAdmissionMaterializationResultV1(
                trigger, DependencyAdmissionOutcome.BLOCKED_PROOF_INVALIDATED, successor_id, None
            )
        if head["state"] != "CURRENT" or head["proof_id"] != proof.proof_id:
            if trigger == "B":
                return DependencyAdmissionMaterializationResultV1(
                    trigger, DependencyAdmissionOutcome.DEFERRED_PREDECESSOR_PROOF_NOT_CURRENT, successor_id, None
                )
            raise AttemptStateError("Trigger A no longer observes its exact CURRENT proof head")
        cancellation = _locked_cancellation_ref(product_root, store, change_id, control)
        if cancellation is not None:
            return DependencyAdmissionMaterializationResultV1(
                trigger, DependencyAdmissionOutcome.BLOCKED_CANCELLATION, successor_id, None
            )
        if "Cancelled" in {current_governance.task_status, resolve_dependency(product_root, "T-01").task_status}:
            return DependencyAdmissionMaterializationResultV1(
                trigger, DependencyAdmissionOutcome.BLOCKED_CANCELLATION, successor_id, None
            )

    try:
        proof = DependencyAcceptanceProofV1.from_mapping(
            proof.to_mapping(), current_requirement=requirement
        )
        artifact_digest = _artifact_digest_inside_lock(product_root, requirement)
        _verify_source_proof_joins(source, proof, requirement, artifact_digest)
        admission = build_dependency_admission(proof, requirement, artifact_digest=artifact_digest)
    except (AttemptRuntimeError, DependencyProofError, DependencyAdmissionError):
        return DependencyAdmissionMaterializationResultV1(
            trigger, DependencyAdmissionOutcome.BLOCKED_STALE_DEPENDENCY, successor_id, None
        )

    if existing is not None:
        if _json_tree(existing) == admission:
            return DependencyAdmissionMaterializationResultV1(
                trigger, DependencyAdmissionOutcome.ALREADY_MATERIALIZED, successor_id, admission["admission_id"]
            )
        return DependencyAdmissionMaterializationResultV1(
            trigger, DependencyAdmissionOutcome.BLOCK_CONFLICTING_ADMISSION, successor_id, None
        )

    updated_attempt = replace(successor.attempt, dependency_admission=admission)
    updated_successor = replace(successor, attempt=updated_attempt)
    proposed = AttemptStoreV2(
        tuple(sorted((updated_successor if row.attempt_id == successor_id else row for row in current_v2.attempts), key=lambda row: row.attempt_id))
    )
    _safe_replace(store, proposed, attempt_id=successor_id, hook=fault_hook)
    verified_v1, verified_v2 = _read_authoritative_stores(product_root)
    verified = verified_v2.by_id(successor_id)
    verified_source = verified_v2.by_id(source_id)
    if (
        verified_v1 != current_v1
        or verified is None
        or verified_source is None
        or _json_tree(verified.attempt.dependency_admission) != admission
        or _canonical_v2_json(_json_tree(verified_source.dependency_edge_control))
        != _canonical_v2_json(_json_tree(source.dependency_edge_control))
    ):
        raise AttemptRuntimeError("complete admission failed strict same-lock Runtime readback")
    # Re-resolve requirement, route and bytes after replacement and before
    # unlocking; a concurrent filesystem edit cannot turn stale pre-write
    # evidence into successful attachment.
    try:
        _, _, final_requirement = _resolve_current_requirement_locked(product_root, change_id)
        final_artifact_digest = _artifact_digest_inside_lock(product_root, final_requirement)
        final_proof = _proof_blob_locked(store, proof.proof_id)
        _verify_source_proof_joins(verified_source, final_proof, final_requirement, final_artifact_digest)
        expected = build_dependency_admission(final_proof, final_requirement, artifact_digest=final_artifact_digest)
    except (AttemptRuntimeError, DependencyProofError, DependencyAdmissionError) as exc:
        raise AttemptRuntimeError("post-attachment joins changed before lock release") from exc
    if expected != admission:
        raise AttemptRuntimeError("post-attachment semantic admission identity changed before lock release")
    return DependencyAdmissionMaterializationResultV1(
        trigger, DependencyAdmissionOutcome.MATERIALIZED, successor_id, admission["admission_id"]
    )


def _read_store_v2(store: Path) -> AttemptStoreV2:
    if not store.exists():
        raise AttemptNotFoundError("AttemptStoreV2 is absent")
    try:
        raw = store.read_bytes()
    except OSError as exc:
        raise AttemptStoreCorruptError("cannot read AttemptStoreV2") from exc
    return decode_attempt_store_v2(raw)


def _read_store_v2_or_empty(store: Path) -> AttemptStoreV2:
    return _read_store_v2(store) if store.exists() else AttemptStoreV2()


def _read_authoritative_stores(
    target: str | os.PathLike[str] | Path,
) -> tuple[AttemptStoreV1, AttemptStoreV2]:
    """Read both no-migration stores and reject cross-store identity reuse."""
    v1_path = attempt_store_path(target)
    v2_path = attempt_store_v2_path(target)
    v1 = _read_store(v1_path) if v1_path.exists() else AttemptStoreV1()
    v2 = _read_store_v2(v2_path) if v2_path.exists() else AttemptStoreV2()
    ids_v1 = [row.attempt_id for row in v1.attempts]
    ids_v2 = [row.attempt_id for row in v2.attempts]
    refs_v1 = [row.authorization_ref for row in v1.attempts]
    refs_v2 = [row.authorization_ref for row in v2.attempts]
    if (
        set(ids_v1) & set(ids_v2)
        or set(refs_v1) & set(refs_v2)
        or len(set(refs_v1)) != len(refs_v1)
        or len(set(refs_v2)) != len(refs_v2)
    ):
        raise AttemptStoreCorruptError("V1/V2 Attempt stores contain a duplicate identity or Authorization ref")
    return v1, v2


def _read_store(store: Path) -> AttemptStoreV1:
    if not store.exists():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    try:
        raw = store.read_bytes()
    except OSError as exc:
        raise AttemptStoreCorruptError("cannot read Attempt Runtime store") from exc
    return decode_attempt_store(raw)


def _read_store_or_empty(store: Path) -> AttemptStoreV1:
    if not store.exists():
        return AttemptStoreV1()
    return _read_store(store)


def _exact_id(attempt_id: object) -> str:
    if not isinstance(attempt_id, str) or not ATTEMPT_ID_PATTERN.fullmatch(attempt_id):
        raise AttemptRuntimeError("INVALID_ID")
    return attempt_id


def _auth_or_raise(target: Path, authorization_ref: str, action: AuthorizationAction, scope: object) -> None:
    result = resolve_authorization(target, authorization_ref, action, scope)  # type: ignore[arg-type]
    if result.outcome is not AuthorizationResolutionOutcome.AUTHORIZED or result.record is None:
        raise AttemptAuthorizationError(f"authorization rejected: {result.outcome.value}")
    if result.record.decision_outcome != "AUTHORIZED":
        raise AttemptAuthorizationError("authorization decision is not AUTHORIZED")


def _resolved_preparation_scope_v2(
    target: Path, authorization_ref: str, change_id: str, task_id: str
) -> PreparationScopeV2:
    """Resolve current immutable V2 Preparation scope through Authorization.

    The V1-shaped Change/task pair is only the request selector accepted by
    the existing Authorization API. Runtime takes all persisted binding
    fields from the returned V2 record, resolves that exact scope again, and
    rejects any mismatch or V1 authority; payload values never form a binding.
    """
    request = PreparationScopeV1(change_id, task_id)
    candidate = resolve_authorization(target, authorization_ref, AuthorizationAction.PREPARATION, request)
    record = candidate.record
    if not isinstance(record, AuthorizationRecordV2) or not isinstance(record.scope, PreparationScopeV2):
        raise AttemptAuthorizationError("new Attempt materialization requires immutable V2 Preparation authority")
    if (record.scope.change_id, record.scope.task_or_operation_id) != (change_id, task_id):
        raise AttemptAuthorizationError("Preparation request does not match immutable V2 scope")
    resolved = resolve_authorization(
        target,
        authorization_ref,
        AuthorizationAction.PREPARATION,
        record.scope,
    )
    if (
        resolved.outcome is not AuthorizationResolutionOutcome.AUTHORIZED
        or resolved.record != record
        or record.decision_outcome != "AUTHORIZED"
    ):
        raise AttemptAuthorizationError(f"authorization rejected: {resolved.outcome.value}")
    return record.scope


def _payload_mapping(preparation: Mapping[str, Any] | bytes | str | os.PathLike[str] | Path | None) -> dict[str, Any]:
    if preparation is None:
        return {}
    if isinstance(preparation, Mapping):
        return dict(preparation)
    if isinstance(preparation, (str, os.PathLike, Path)):
        try:
            raw = Path(preparation).read_bytes()
        except OSError as exc:
            raise AttemptRuntimeError("cannot read preparation input") from exc
    elif isinstance(preparation, bytes):
        raw = preparation
    else:
        raise AttemptRuntimeError("preparation input must be a mapping, JSON bytes, or a path")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise AttemptRuntimeError("preparation input is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise AttemptRuntimeError("preparation input must be a JSON object")
    return dict(value)


def _merge_preparation_fields(
    preparation: Mapping[str, Any] | bytes | str | os.PathLike[str] | Path | None,
    overrides: Mapping[str, Any],
) -> dict[str, Any]:
    data = _payload_mapping(preparation)
    nested = data.get("attempt") or data.get("attempt_record")
    if nested is not None:
        if not isinstance(nested, Mapping):
            raise AttemptRuntimeError("preparation attempt payload must be an object")
        merged = dict(nested)
        merged.update({key: value for key, value in data.items() if key not in {"attempt", "attempt_record"}})
        data = merged
    for key, value in overrides.items():
        if value is not None:
            data[key] = value
    return data


def _candidate_from_payload(value: object) -> CandidateIdentityV1:
    return _candidate_from_mapping(value)


def _baseline_from_payload(value: object) -> tuple[IdentityRefV1, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
        raise AttemptRuntimeError("baseline_refs must be a non-empty list")
    try:
        return tuple(_identity_ref_from_mapping(item) for item in value)
    except AttemptStoreCorruptError as exc:
        raise AttemptRuntimeError("baseline_refs are invalid") from exc


def _build_attempt(
    data: Mapping[str, Any],
    *,
    ordinal: int,
    existing: Sequence[AttemptEnvelopeV1],
) -> AttemptRecordV1:
    required = ("change_id", "task_or_operation_id", "authorization_ref", "acceptance_contract_ref", "candidate_identity", "baseline_refs")
    missing = [key for key in required if key not in data]
    if missing:
        raise AttemptRuntimeError(f"preparation input is missing: {', '.join(missing)}")
    change_id = _text(data["change_id"], "change_id")
    task_id = _text(data["task_or_operation_id"], "task_or_operation_id")
    auth_ref = data["authorization_ref"]
    if not isinstance(auth_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(auth_ref):
        raise AttemptRuntimeError("authorization_ref is malformed")
    candidate = _candidate_from_payload(data["candidate_identity"])
    baseline = _baseline_from_payload(data["baseline_refs"])
    findings = data.get("addresses_finding_refs", [])
    verifier_values = data.get("verifier_contract_refs", [])
    if not isinstance(findings, Sequence) or isinstance(findings, (str, bytes)):
        raise AttemptRuntimeError("addresses_finding_refs must be a list")
    if not isinstance(verifier_values, Sequence) or isinstance(verifier_values, (str, bytes)):
        raise AttemptRuntimeError("verifier_contract_refs must be a list")
    verifier_contracts: list[VerifierContractIdentity] = []
    for item in verifier_values:
        if not isinstance(item, Mapping) or set(item) != {"contract_id", "contract_version_or_ref"}:
            raise AttemptRuntimeError("verifier_contract_refs contains an invalid identity")
        verifier_contracts.append(
            (_text(item["contract_id"], "contract_id"), _text(item["contract_version_or_ref"], "contract_version_or_ref"))
        )
    try:
        attempt = AttemptRecordV1(
            f"{change_id}/{task_id}/A{ordinal}",
            change_id,
            task_id,
            ordinal,
            auth_ref,
            _text(data["acceptance_contract_ref"], "acceptance_contract_ref"),
            candidate,
            baseline,
            _optional_text(data.get("operation_guidance_ref"), "operation_guidance_ref"),
            _optional_text(data.get("prompt_composition_ref"), "prompt_composition_ref"),
            _optional_text(data.get("parent_attempt_ref"), "parent_attempt_ref"),
            tuple(findings),
            None,
            tuple(verifier_contracts),
        )
    except (AttemptEvaluationError, TypeError, KeyError) as exc:
        raise AttemptRuntimeError("preparation Attempt input is invalid") from exc
    parent_id = attempt.parent_attempt_ref
    if parent_id is not None:
        parent = next((row.attempt for row in existing if row.attempt_id == parent_id), None)
        if parent is None or (parent.change_id, parent.task_or_operation_id) != (change_id, task_id):
            raise AttemptRuntimeError("parent Attempt is absent or crosses Change/task scope")
    return attempt


def _build_attempt_v2(
    data: Mapping[str, Any],
    *,
    scope: PreparationScopeV2,
    authorization_ref: str,
    ordinal: int,
    existing: Sequence[AttemptEnvelopeV1 | AttemptEnvelopeV2],
) -> AttemptRecordV2:
    """Build the V2 record from resolver-owned scope plus ordinary Attempt facts."""
    authoritative = {
        **dict(data),
        "change_id": scope.change_id,
        "task_or_operation_id": scope.task_or_operation_id,
        "authorization_ref": authorization_ref,
    }
    if scope.dependency_classification == "DEPENDENCY_EDGE_MEMBER":
        if authoritative.get("parent_attempt_ref") is not None:
            raise AttemptRuntimeError("fixed dependency edge Attempt cannot have a parent")
        ordinal = 1
    v1_rows: list[AttemptEnvelopeV1] = []
    for row in existing:
        attempt = row.attempt.as_v1() if isinstance(row.attempt, AttemptRecordV2) else row.attempt
        v1_rows.append(
            AttemptEnvelopeV1(
                attempt,
                row.runtime_state,
                row.observed_result,
                row.recovery_authorization_ref,
            )
        )
    base = _build_attempt(authoritative, ordinal=ordinal, existing=v1_rows)
    binding = PreparationBindingV2(
        authorization_ref,
        scope.plan_ref,
        scope.tasks_ref,
        scope.approved_plan_digest,
        scope.dependency_semantic_digest,
        scope.requirement_id,
        scope.dependency_classification,
        scope.expected_attempt_id,
    )
    return AttemptRecordV2(
        base.attempt_id,
        base.change_id,
        base.task_or_operation_id,
        base.attempt_ordinal,
        base.authorization_ref,
        base.acceptance_contract_ref,
        base.candidate_identity,
        base.baseline_refs,
        binding,
        base.operation_guidance_ref,
        base.prompt_composition_ref,
        base.parent_attempt_ref,
        base.addresses_finding_refs,
        base.observed_result_ref,
        base.verifier_contract_refs,
        None,
    )


def prepare_attempt(
    target: str | os.PathLike[str] | Path,
    preparation: Mapping[str, Any] | bytes | str | os.PathLike[str] | Path | None = None,
    *,
    authorization_ref: str | None = None,
    change_id: str | None = None,
    task_or_operation_id: str | None = None,
    acceptance_contract_ref: str | None = None,
    candidate_identity: Mapping[str, Any] | None = None,
    baseline_refs: Sequence[Mapping[str, Any]] | None = None,
    operation_guidance_ref: str | None = None,
    prompt_composition_ref: str | None = None,
    parent_attempt_ref: str | None = None,
    addresses_finding_refs: Sequence[str] | None = None,
    verifier_contract_refs: Sequence[Mapping[str, str]] | None = None,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV2:
    """Materialize one V2 ``ACTIVATABLE`` Attempt from current immutable Preparation.

    Authorization supplies Change/task identity and all eight binding fields;
    payload values supply only ordinary Attempt facts. A1 edge identity,
    cross-store ID/ref uniqueness, single-use, and publication are checked
    under the existing V2 path lock. For exact dependent T-02/A1, the same
    critical section immediately invokes Trigger B through the shared
    materializer after strict Preparation readback, then returns the final
    reread row without nested lock acquisition. V1 stores are read-only here
    and never migrated or rewritten.
    """

    overrides = {
        "authorization_ref": authorization_ref,
        "change_id": change_id,
        "task_or_operation_id": task_or_operation_id,
        "acceptance_contract_ref": acceptance_contract_ref,
        "candidate_identity": candidate_identity,
        "baseline_refs": baseline_refs,
        "operation_guidance_ref": operation_guidance_ref,
        "prompt_composition_ref": prompt_composition_ref,
        "parent_attempt_ref": parent_attempt_ref,
        "addresses_finding_refs": addresses_finding_refs,
        "verifier_contract_refs": verifier_contract_refs,
    }
    data = _merge_preparation_fields(preparation, overrides)
    required = ("authorization_ref", "change_id", "task_or_operation_id")
    if any(key not in data for key in required):
        raise AttemptRuntimeError("preparation input lacks authorization and exact Change/task scope")
    change = _text(data["change_id"], "change_id")
    task = _text(data["task_or_operation_id"], "task_or_operation_id")
    auth_ref = data["authorization_ref"]
    if not isinstance(auth_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(auth_ref):
        raise AttemptRuntimeError("authorization_ref is malformed")
    product_root = Path(target).expanduser().resolve()
    scope = _resolved_preparation_scope_v2(product_root, auth_ref, change, task)
    if (change, task) != (scope.change_id, scope.task_or_operation_id):
        raise AttemptAuthorizationError("payload Change/task differs from resolved Preparation authority")
    store = attempt_store_v2_path(product_root)
    with _store_lock(store, create=True):
        current_v1, current_v2 = _read_authoritative_stores(product_root)
        all_rows: tuple[AttemptEnvelopeV1 | AttemptEnvelopeV2, ...] = (*current_v1.attempts, *current_v2.attempts)
        if any(row.authorization_ref == auth_ref for row in all_rows):
            raise AttemptAuthorizationError("preparation authorization has already materialized an Attempt")
        lineage = sorted(
            (
                row.attempt.as_v1() if isinstance(row.attempt, AttemptRecordV2) else row.attempt
                for row in all_rows
                if row.attempt.change_id == change and row.attempt.task_or_operation_id == task
            ),
            key=lambda row: row.attempt_ordinal,
        )
        if scope.dependency_classification == "DEPENDENCY_EDGE_MEMBER":
            expected_id = f"{change}/{task}/A1"
            if scope.expected_attempt_id != expected_id or lineage or any(row.attempt_id == expected_id for row in all_rows):
                raise AttemptAuthorizationError("fixed dependency edge A1 is already occupied or mismatched")
            ordinal = 1
        else:
            try:
                ordinal = allocate_attempt_ordinal(lineage, change_id=change, task_or_operation_id=task)
            except AttemptEvaluationError as exc:
                raise AttemptRuntimeError("authoritative Attempt lineage is invalid") from exc
        attempt = _build_attempt_v2(
            data,
            scope=scope,
            authorization_ref=auth_ref,
            ordinal=ordinal,
            existing=all_rows,
        )
        if any(row.attempt_id == attempt.attempt_id for row in all_rows) or any(
            row.authorization_ref == attempt.authorization_ref for row in all_rows
        ):
            raise AttemptAuthorizationError("materialized Attempt ID or Authorization ref is already occupied")
        envelope = AttemptEnvelopeV2(attempt, "ACTIVATABLE")
        proposed = AttemptStoreV2(tuple(sorted((*current_v2.attempts, envelope), key=lambda row: row.attempt_id)))
        _safe_replace(store, proposed, attempt_id=attempt.attempt_id, hook=fault_hook)
        verified_v1, verified_v2 = _read_authoritative_stores(product_root)
        verified = verified_v2.by_id(attempt.attempt_id)
        if verified is None or verified.runtime_state != "ACTIVATABLE" or verified_v1 != current_v1:
            raise AttemptRuntimeError("materialized V2 Attempt failed authoritative verification")
        if task == "T-02" and scope.dependency_classification == "DEPENDENCY_EDGE_MEMBER":
            # Trigger B is part of exact T-02/A1 materialization and reuses
            # this already-held V2 lock; it never calls the public lock wrapper.
            materialize_dependency_admission_if_ready(
                product_root, trigger="B", _locked_store=store, fault_hook=fault_hook
            )
            verified_v1, verified_v2 = _read_authoritative_stores(product_root)
            verified = verified_v2.by_id(attempt.attempt_id)
            if verified is None or verified_v1 != current_v1:
                raise AttemptRuntimeError("Trigger B changed the exact materialized Attempt identity")
        return verified


materialize_attempt = prepare_attempt


def lookup_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
) -> AttemptLookupResultV1:
    """Resolve one exact identity across both stores without creating or promoting state.

    Either store being malformed, or an identity/authorization duplicated
    across V1 and V2, is reported as ``CORRUPT_CONFLICT``. A valid exact row is
    returned in its native envelope type; absence from both stores is
    ``NOT_FOUND``.
    """

    if not isinstance(attempt_id, str) or not ATTEMPT_ID_PATTERN.fullmatch(attempt_id):
        return AttemptLookupResultV1(LookupOutcome.INVALID_ID)
    try:
        v1, v2 = _read_authoritative_stores(target)
    except AttemptRuntimeError:
        return AttemptLookupResultV1(LookupOutcome.CORRUPT_CONFLICT)
    record = v1.by_id(attempt_id)
    v2_record = v2.by_id(attempt_id)
    if record is not None and v2_record is not None:
        return AttemptLookupResultV1(LookupOutcome.CORRUPT_CONFLICT)
    record = record or v2_record
    return AttemptLookupResultV1(
        LookupOutcome.FOUND if record is not None else LookupOutcome.NOT_FOUND,
        record,
    )


def exact_lookup(target: str | os.PathLike[str] | Path, attempt_id: str) -> AttemptLookupResultV1:
    """Alias for the exact lookup application seam."""

    return lookup_attempt(target, attempt_id)


def check_activation_admissibility(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
) -> AttemptAdmissibilityResultV1:
    """Report native-store state without substituting for either edge claim gate.

    This is read-only across both stores. Independent V2 and compatible V1
    rows retain the simple state result. Exact dependent T-01/A1 is admissible
    for its separate source claim, whose locked path validates own Preparation,
    current edge and cancellation. Exact T-02/A1 becomes a lifecycle candidate
    only after a complete admission is attached; the ensuing claim still runs
    every D11 predicate. This projection grants no authority itself.
    """

    if not isinstance(attempt_id, str) or not ATTEMPT_ID_PATTERN.fullmatch(attempt_id):
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.INVALID_ID)
    try:
        v1, v2 = _read_authoritative_stores(target)
    except AttemptRuntimeError:
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.CORRUPT_CONFLICT)
    envelope_v1 = v1.by_id(attempt_id)
    envelope_v2 = v2.by_id(attempt_id)
    if envelope_v1 is not None and envelope_v2 is not None:
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.CORRUPT_CONFLICT)
    envelope = envelope_v1 or envelope_v2
    if envelope is None:
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.NOT_FOUND)
    if isinstance(envelope, AttemptEnvelopeV2) and envelope.attempt.preparation_binding.dependency_classification != "NOT_APPLICABLE":
        source = envelope.attempt
        if (
            source.task_or_operation_id == "T-01"
            and source.attempt_id == _exact_source_id(source.change_id)
            and source.attempt_ordinal == 1
            and source.parent_attempt_ref is None
            and source.preparation_binding.expected_attempt_id == source.attempt_id
            and envelope.runtime_state == "ACTIVATABLE"
        ):
            return AttemptAdmissibilityResultV1(AdmissibilityOutcome.ADMISSIBLE, envelope)
        if (
            source.task_or_operation_id == "T-02"
            and source.attempt_id == _exact_successor_id(source.change_id)
            and source.attempt_ordinal == 1
            and source.parent_attempt_ref is None
            and source.preparation_binding.expected_attempt_id == source.attempt_id
            and source.dependency_admission is not None
            and envelope.runtime_state == "ACTIVATABLE"
        ):
            # Admission only permits Lifecycle to reach the existing claim
            # owner; it is not trusted here as a substitute for D11.
            return AttemptAdmissibilityResultV1(AdmissibilityOutcome.ADMISSIBLE, envelope)
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.INVALID_RECORD, envelope)
    if envelope.runtime_state == "ACTIVATABLE":
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.ADMISSIBLE, envelope)
    if envelope.runtime_state == "IN_FLIGHT":
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.IN_FLIGHT, envelope)
    return AttemptAdmissibilityResultV1(AdmissibilityOutcome.TERMINAL, envelope)


def _required_store_for_mutation(target: str | os.PathLike[str] | Path) -> tuple[Path, AttemptStoreV1]:
    store = attempt_store_path(target)
    if not store.exists():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    return store, _read_store(store)


def _mutation_row(
    target: Path, attempt_id: str
) -> tuple[Path, AttemptEnvelopeV1 | AttemptEnvelopeV2]:
    """Select the native store for one exact row; the mutation rereads under its lock."""
    try:
        v1, v2 = _read_authoritative_stores(target)
    except AttemptRuntimeError:
        raise
    row_v1 = v1.by_id(attempt_id)
    row_v2 = v2.by_id(attempt_id)
    if row_v1 is not None and row_v2 is not None:
        raise AttemptStoreCorruptError("Attempt identity occurs in both Runtime stores")
    if row_v2 is not None:
        return attempt_store_v2_path(target), row_v2
    if row_v1 is not None:
        return attempt_store_path(target), row_v1
    raise AttemptNotFoundError("Attempt is not found")


def _preparation_scope_from_binding(attempt: AttemptRecordV2) -> PreparationScopeV2:
    """Reconstruct only the exact resolver scope needed for independent revalidation."""
    binding = attempt.preparation_binding
    return PreparationScopeV2(
        attempt.change_id,
        attempt.task_or_operation_id,
        binding.plan_ref,
        binding.tasks_ref,
        binding.approved_plan_digest,
        binding.dependency_semantic_digest,
        binding.requirement_id,
        binding.dependency_classification,
        binding.expected_attempt_id,
    )


def claim_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
    *,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1 | AttemptEnvelopeV2:
    """Perform the exported, non-bypassable claim gate under the native lock.

    A dependent V2 claim keeps one policy-resolved Runtime lock while it
    re-resolves its own Preparation authority, current governance and
    cancellation facts, exact persisted admission, CURRENT proof/blob, and
    Workspace route/raw bytes, then repeats the decisive reads immediately
    before atomic ACTIVATABLE-to-IN_FLIGHT replacement and strict readback.
    Admission is eligibility, never authority; this path fails closed and
    never repairs/materializes evidence or invokes an executor. A successful
    claim is not revoked by later proof invalidation and terminalization or
    Recovery performs no second admission check. Independent V2 and V1 rows
    retain their existing separate claim semantics.
    """

    _exact_id(attempt_id)
    product_root = Path(target).expanduser().resolve()
    store, selected = _mutation_row(product_root, attempt_id)
    with _store_lock(store, create=False):
        current_v1, current_v2 = _read_authoritative_stores(product_root)
        current = current_v2 if store == attempt_store_v2_path(product_root) else current_v1
        row = current.by_id(attempt_id)
        if row is None:
            raise AttemptNotFoundError("Attempt is not found")
        if type(row) is not type(selected):
            raise AttemptStoreCorruptError("Attempt changed native store before claim")
        if row.runtime_state != "ACTIVATABLE":
            raise AttemptStateError(f"Attempt cannot be claimed from {row.runtime_state}")
        if isinstance(row, AttemptEnvelopeV2):
            classification = row.attempt.preparation_binding.dependency_classification
            if classification == "DEPENDENCY_EDGE_MEMBER":
                try:
                    if row.attempt.task_or_operation_id == "T-01":
                        first_source = _source_edge_claim_evidence_locked(
                            product_root, store, current_v2, attempt_id
                        )
                        # The source edge claim repeats its own authority,
                        # current edge, cancellation, and Attempt rereads
                        # immediately before the atomic transition. It does
                        # not route through the successor's D11 evidence gate.
                        final_v1, final_v2 = _read_authoritative_stores(product_root)
                        if final_v1 != current_v1:
                            raise AttemptStoreCorruptError("V1 Runtime changed during source edge claim")
                        final_evidence = _source_edge_claim_evidence_locked(
                            product_root,
                            store,
                            final_v2,
                            attempt_id,
                            original_source=row,
                        )
                        if final_evidence != first_source:
                            raise AttemptStateError("source edge evidence changed before final claim write")
                        claimed = replace(final_evidence.source, runtime_state="IN_FLIGHT")
                        proposed = AttemptStoreV2(
                            tuple(
                                sorted(
                                    (claimed if item.attempt_id == attempt_id else item for item in final_v2.attempts),
                                    key=lambda item: item.attempt_id,
                                )
                            )
                        )
                        _safe_replace(store, proposed, attempt_id=attempt_id, hook=fault_hook)
                        verified_v1, verified_v2 = _read_authoritative_stores(product_root)
                        verified = verified_v2.by_id(attempt_id)
                        if (
                            verified_v1 != current_v1
                            or verified_v2 != proposed
                            or verified != claimed
                            or verified.runtime_state != "IN_FLIGHT"
                        ):
                            raise AttemptRuntimeError("source edge claim failed exact canonical Runtime readback")
                        return verified
                    if row.attempt.task_or_operation_id != "T-02":
                        raise AttemptStateError("dependent claim endpoint is unsupported")
                    first_evidence = _dependent_claim_evidence_locked(
                        product_root, store, current_v2, attempt_id
                    )
                    # D11-6 rereads both canonical stores and repeats every
                    # governance/authority/proof/route/admission join just
                    # before the one atomic state transition.
                    final_v1, final_v2 = _read_authoritative_stores(product_root)
                    if final_v1 != current_v1:
                        raise AttemptStoreCorruptError("V1 Runtime changed during dependent claim")
                    final_row = final_v2.by_id(attempt_id)
                    if final_row != row:
                        raise AttemptStateError("T-02/A1 changed before final dependent claim write")
                    final_evidence = _dependent_claim_evidence_locked(
                        product_root,
                        store,
                        final_v2,
                        attempt_id,
                        original_successor=row,
                        original_source=first_evidence.source,
                    )
                    if final_evidence != first_evidence:
                        raise AttemptStateError("dependent claim evidence changed before final write")
                    claimed = replace(final_row, runtime_state="IN_FLIGHT")
                    proposed = AttemptStoreV2(
                        tuple(
                            sorted(
                                (claimed if item.attempt_id == attempt_id else item for item in final_v2.attempts),
                                key=lambda item: item.attempt_id,
                            )
                        )
                    )
                    _safe_replace(store, proposed, attempt_id=attempt_id, hook=fault_hook)
                    verified_v1, verified_v2 = _read_authoritative_stores(product_root)
                    verified = verified_v2.by_id(attempt_id)
                    if verified_v1 != current_v1 or verified_v2 != proposed or verified != claimed:
                        raise AttemptRuntimeError("dependent claim failed exact canonical Runtime readback")
                    return verified
                except AttemptRuntimeError:
                    raise
                except (
                    DependencyAdmissionError,
                    DependencyProofCarrierError,
                    DependencyProofError,
                    WorkspaceError,
                    OSError,
                    KeyError,
                    TypeError,
                    ValueError,
                ) as exc:
                    raise AttemptRuntimeError("dependent T-06 claim failed closed") from exc
            if classification != "NOT_APPLICABLE":
                raise AttemptStateError("V2 Preparation classification is unsupported")
            scope = _preparation_scope_from_binding(row.attempt)
        else:
            scope = PreparationScopeV1(row.attempt.change_id, row.attempt.task_or_operation_id)
        _auth_or_raise(product_root, row.authorization_ref, AuthorizationAction.PREPARATION, scope)
        claimed = replace(row, runtime_state="IN_FLIGHT")
        if isinstance(current, AttemptStoreV2):
            proposed: AttemptStoreV1 | AttemptStoreV2 = AttemptStoreV2(
                tuple(sorted((claimed if item.attempt_id == attempt_id else item for item in current.attempts), key=lambda item: item.attempt_id))
            )
        else:
            proposed = AttemptStoreV1(
                tuple(sorted((claimed if item.attempt_id == attempt_id else item for item in current.attempts), key=lambda item: item.attempt_id))
            )
        _safe_replace(store, proposed, attempt_id=attempt_id, hook=fault_hook)
        verified_v1, verified_v2 = _read_authoritative_stores(product_root)
        verified = verified_v2.by_id(attempt_id) if isinstance(proposed, AttemptStoreV2) else verified_v1.by_id(attempt_id)
        if verified is None or verified.runtime_state != "IN_FLIGHT":
            raise AttemptRuntimeError("claimed Attempt failed authoritative verification")
        return verified


def _result_from_input(
    value: ObservedResultV1 | Mapping[str, Any], *, strict_v2: bool = False
) -> ObservedResultV1:
    """Parse a terminal result under native V1 rules or strict V2 integer rules."""
    if isinstance(value, ObservedResultV1):
        return value
    return _observed_result_v2_from_mapping(value) if strict_v2 else _observed_result_from_mapping(value)


def terminalize_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
    observed_result: ObservedResultV1 | Mapping[str, Any],
    *,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1 | AttemptEnvelopeV2:
    """Persist one normal irreversible same-Attempt terminal fact.

    Normal terminalization accepts all supported executor statuses and always
    persists null recovery provenance.  In particular, ``INTERRUPTED``
    describes what happened during execution; it is not owner recovery
    authority.  Explicit owner recovery is available only through
    ``resolve_interrupted_attempt``.

    Only ``IN_FLIGHT`` can terminalize in either native store. This performs
    an authoritative prepare, validate, replace, verify, and hash-preserving
    write under that store's existing Runtime lock; there is no reset, retry,
    rollback, lease, or automatic repair after process loss.
    """

    # INTERRUPTED execution status != owner recovery authority.
    return _terminalize_attempt(
        Path(target).expanduser().resolve(),
        attempt_id,
        observed_result,
        terminal_authorization_ref=None,
        fault_hook=fault_hook,
    )


def _terminalize_attempt(
    target: Path,
    attempt_id: str,
    observed_result: ObservedResultV1 | Mapping[str, Any],
    *,
    terminal_authorization_ref: str | None,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1 | AttemptEnvelopeV2:
    """Persist terminal facts after provenance has been selected internally.

    ``terminal_authorization_ref`` may be non-null only for the private owner
    recovery caller, after exact CLOSED Authorization resolution.  Keeping
    this capability out of the public normal-terminalization signature makes
    fabricated recovery provenance fail closed at the public contract.
    """

    _exact_id(attempt_id)
    if terminal_authorization_ref is not None and not AUTHORIZATION_REF_PATTERN.fullmatch(terminal_authorization_ref):
        raise AttemptAuthorizationError("recovery authorization reference is malformed")
    store, selected = _mutation_row(target, attempt_id)
    result = _result_from_input(observed_result, strict_v2=isinstance(selected, AttemptEnvelopeV2))
    if result.attempt_id != attempt_id or result.execution_status not in TERMINAL_STATUSES:
        raise AttemptStateError("terminal fact is wrong-Attempt or unsupported")
    with _store_lock(store, create=False):
        current_v1, current_v2 = _read_authoritative_stores(target)
        current = current_v2 if store == attempt_store_v2_path(target) else current_v1
        row = current.by_id(attempt_id)
        if row is None:
            raise AttemptNotFoundError("Attempt is not found")
        if type(row) is not type(selected):
            raise AttemptStoreCorruptError("Attempt changed native store before terminalization")
        if row.runtime_state != "IN_FLIGHT":
            raise AttemptStateError(f"Attempt cannot terminalize from {row.runtime_state}")
        all_rows = (*current_v1.attempts, *current_v2.attempts)
        if any(item.observed_result and item.observed_result.result_id == result.result_id for item in all_rows):
            raise AttemptStateError("terminal result identity is already persisted")
        updated_attempt = replace(row.attempt, observed_result_ref=result.result_id)
        if isinstance(row, AttemptEnvelopeV2):
            terminal: AttemptEnvelopeV1 | AttemptEnvelopeV2 = AttemptEnvelopeV2(
                updated_attempt,
                "TERMINAL",
                result,
                terminal_authorization_ref,
                row.dependency_edge_control,
            )
            proposed = AttemptStoreV2(
                tuple(sorted((terminal if item.attempt_id == attempt_id else item for item in current.attempts), key=lambda item: item.attempt_id))
            )
        else:
            terminal = AttemptEnvelopeV1(updated_attempt, "TERMINAL", result, terminal_authorization_ref)
            proposed = AttemptStoreV1(
                tuple(sorted((terminal if item.attempt_id == attempt_id else item for item in current.attempts), key=lambda item: item.attempt_id))
            )
        _safe_replace(store, proposed, attempt_id=attempt_id, hook=fault_hook)
        verified_v1, verified_v2 = _read_authoritative_stores(target)
        verified = verified_v2.by_id(attempt_id) if isinstance(proposed, AttemptStoreV2) else verified_v1.by_id(attempt_id)
        if verified is None or verified.runtime_state != "TERMINAL":
            raise AttemptRuntimeError("terminal Attempt failed authoritative verification")
        return verified


def resolve_interrupted_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
    authorization_ref: str,
    *,
    result_id: str | None = None,
    fact_refs: Sequence[str] = (),
    artifact_refs: Sequence[str] = (),
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1 | AttemptEnvelopeV2:
    """Resolve one exact in-flight Attempt through owner recovery authority.

    The existing V1 Recovery Authorization capability remains Plan-independent
    and must authorize the exact Attempt ID before the private terminalization
    helper may persist its provenance on either V1 or V2. It grants no
    preparation or dependent-claim authority.
    """

    _exact_id(attempt_id)
    if not isinstance(authorization_ref, str):
        raise AttemptAuthorizationError("recovery authorization reference is malformed")
    product_root = Path(target).expanduser().resolve()
    _auth_or_raise(
        product_root,
        authorization_ref,
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1(attempt_id),
    )
    return _terminalize_with_recovery(
        product_root,
        attempt_id,
        authorization_ref,
        result_id=result_id,
        fact_refs=fact_refs,
        artifact_refs=artifact_refs,
        fault_hook=fault_hook,
    )


def _terminalize_with_recovery(
    target: Path,
    attempt_id: str,
    authorization_ref: str,
    *,
    result_id: str | None,
    fact_refs: Sequence[str],
    artifact_refs: Sequence[str],
    fault_hook: ReplacementHook | None,
) -> AttemptEnvelopeV1 | AttemptEnvelopeV2:
    result = ObservedResultV1(
        result_id or f"recovery:{attempt_id}",
        attempt_id,
        "INTERRUPTED",
        (),
        tuple(fact_refs),
        tuple(artifact_refs),
    )
    return _terminalize_attempt(
        target,
        attempt_id,
        result,
        terminal_authorization_ref=authorization_ref,
        fault_hook=fault_hook,
    )


recover_interrupted_attempt = resolve_interrupted_attempt


def load_attempt_store(target: str | os.PathLike[str] | Path) -> AttemptStoreV1:
    """Read the authoritative store without creating or mutating it."""

    return _read_store(attempt_store_path(target))


def store_sha256(target: str | os.PathLike[str] | Path) -> str:
    """Return evidence hash of the verified canonical store bytes."""

    path = attempt_store_path(target)
    raw = path.read_bytes()
    decode_attempt_store(raw)
    return hashlib.sha256(raw).hexdigest()


__all__ = [
    "AdmissibilityOutcome",
    "AttemptAdmissibilityResultV1",
    "AttemptAuthorizationError",
    "AttemptEnvelopeV1",
    "AttemptEnvelopeV2",
    "AttemptLookupResultV1",
    "AttemptNotFoundError",
    "AttemptRuntimeError",
    "AttemptStateError",
    "AttemptStoreCorruptError",
    "AttemptStoreV1",
    "AttemptStoreV2",
    "AttemptRecordV2",
    "PreparationBindingV2",
    "LookupOutcome",
    "MutationEvidenceV1",
    "RUNTIME_STATES",
    "TERMINAL_STATUSES",
    "attempt_store_path",
    "attempt_store_v2_path",
    "check_activation_admissibility",
    "claim_attempt",
    "decode_attempt_store",
    "decode_attempt_store_v2",
    "encode_attempt_store",
    "encode_attempt_store_v2",
    "exact_lookup",
    "load_attempt_store",
    "lookup_attempt",
    "materialize_attempt",
    "prepare_attempt",
    "recover_interrupted_attempt",
    "resolve_interrupted_attempt",
    "runtime_store_path",
    "store_sha256",
    "terminalize_attempt",
]
