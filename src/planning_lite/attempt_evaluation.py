"""Pure, contract-only governed Attempt and technical-evaluation records.

This module deliberately owns no persistence, filesystem/Git access, authority,
workflow, registry, or provider behavior. Callers supply the ledger-scoped
lineage and already-observed evidence; the functions validate and reconcile
those bounded facts.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
import hashlib
import json
import re
from typing import Any


SCHEMA_VERSION = 1
SHA256_RE = re.compile(r"[0-9a-f]{64}\Z")
GIT_SHA_RE = re.compile(r"[0-9a-f]{40}\Z")
CHANGE_KINDS = frozenset({"ADD", "MODIFY", "DELETE", "RENAME", "TYPE_CHANGE"})
SEVERITIES = frozenset({"MATERIAL", "NON_MATERIAL"})
RESPONSIBILITY_DOMAINS = frozenset(
    {
        "IMPLEMENTATION",
        "VERIFICATION_TEST_COVERAGE",
        "CONTRACT",
        "AUTHORITY",
        "FIXTURE_HARNESS",
        "ENVIRONMENT",
        "SCOPE_PROVENANCE",
    }
)
ACCEPTANCE_IMPACTS = frozenset({"BLOCKING", "NON_BLOCKING"})
DISPOSITIONS = frozenset({"OPEN", "REMEDIATION_REQUIRED", "DEFERRED", "CLOSED"})
EXECUTION_STATUSES = frozenset({"COMPLETED", "FAILED", "INTERRUPTED", "INVALID"})
VERIFIER_OUTCOMES = frozenset({"PASS", "FAIL", "INVALID", "NOT_RUN"})
EVALUATION_OUTCOMES = frozenset({"NOT_EVALUATED", "NOT_SATISFIED", "INDETERMINATE", "SATISFIED"})
ABSENT = "ABSENT"


class AttemptEvaluationError(ValueError):
    """A supplied contract or evidence value is invalid."""


def canonical_json_bytes(value: object) -> bytes:
    """Return the project-compatible deterministic UTF-8 JSON byte form."""

    try:
        encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    except (TypeError, ValueError) as exc:
        raise AttemptEvaluationError("value is not canonically JSON serializable") from exc
    return encoded.encode("utf-8")


def _nonempty(value: object, field: str, *, forbid_edges: bool = True) -> str:
    if not isinstance(value, str) or not value:
        raise AttemptEvaluationError(f"{field} must be a non-empty string")
    if forbid_edges and (value != value.strip() or "\r" in value or "\n" in value):
        raise AttemptEvaluationError(f"{field} has forbidden surrounding whitespace or newline")
    return value


def _sha(value: object, field: str) -> str:
    text = _nonempty(value, field)
    if not SHA256_RE.fullmatch(text):
        raise AttemptEvaluationError(f"{field} must be a lowercase SHA-256")
    return text


def _git_sha(value: object, field: str) -> str:
    text = _nonempty(value, field)
    if not GIT_SHA_RE.fullmatch(text):
        raise AttemptEvaluationError(f"{field} must be a lowercase Git SHA")
    return text


def _path(value: object, field: str) -> str:
    text = _nonempty(value, field).replace("\\", "/")
    if re.match(r"^[A-Za-z]:", text) or text.startswith("/") or any(part in {"", ".", ".."} for part in text.split("/")):
        raise AttemptEvaluationError(f"{field} must be a normalized repository-relative path")
    return text


def _tuple_strings(value: object, field: str, *, unique: bool = True) -> tuple[str, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise AttemptEvaluationError(f"{field} must be a sequence of strings")
    result = tuple(_nonempty(item, f"{field}[]") for item in value)
    if unique and len(set(result)) != len(result):
        raise AttemptEvaluationError(f"{field} must not contain duplicates")
    return result


VerifierContractIdentity = tuple[str, str]


def _verifier_identity(value: object, field: str) -> VerifierContractIdentity:
    """Validate one lossless ``(contract_id, contract_version_or_ref)`` pair."""

    if isinstance(value, Mapping):
        if set(value) != {"contract_id", "contract_version_or_ref"}:
            raise AttemptEvaluationError(f"{field} must carry both verifier identity components")
        raw = (value.get("contract_id"), value.get("contract_version_or_ref"))
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        if len(value) != 2:
            raise AttemptEvaluationError(f"{field} must carry both verifier identity components")
        raw = (value[0], value[1])
    else:
        raise AttemptEvaluationError(f"{field} must carry both verifier identity components")
    return (
        _nonempty(raw[0], f"{field}.contract_id"),
        _nonempty(raw[1], f"{field}.contract_version_or_ref"),
    )


def _tuple_verifier_identities(value: object, field: str) -> tuple[VerifierContractIdentity, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise AttemptEvaluationError(f"{field} must be a sequence of composite verifier identities")
    result = tuple(_verifier_identity(item, f"{field}[]") for item in value)
    if len(set(result)) != len(result):
        raise AttemptEvaluationError(f"{field} must not contain duplicate composite identities")
    return result


def _verifier_identity_mapping(value: VerifierContractIdentity) -> dict[str, str]:
    return {"contract_id": value[0], "contract_version_or_ref": value[1]}


def _mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise AttemptEvaluationError(f"{field} must be an object")
    return value


@dataclass(frozen=True, slots=True)
class DirtyPathEntryV1:
    path: str
    change_kind: str
    before: str
    after: str
    source_path: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "path", _path(self.path, "path"))
        if self.change_kind not in CHANGE_KINDS:
            raise AttemptEvaluationError("change_kind is not supported")
        if self.change_kind == "RENAME":
            if self.source_path is None:
                raise AttemptEvaluationError("RENAME requires source_path")
            object.__setattr__(self, "source_path", _path(self.source_path, "source_path"))
            if self.source_path == self.path:
                raise AttemptEvaluationError("RENAME source and destination must differ")
        elif self.source_path is not None:
            raise AttemptEvaluationError("source_path is allowed only for RENAME")
        for field_name in ("before", "after"):
            value = getattr(self, field_name)
            if value != ABSENT:
                value = _sha(value, field_name)
                object.__setattr__(self, field_name, value)
        if self.change_kind == "ADD" and (self.before != ABSENT or self.after == ABSENT):
            raise AttemptEvaluationError("ADD must use ABSENT before and a digest after identity")
        if self.change_kind == "DELETE" and (self.before == ABSENT or self.after != ABSENT):
            raise AttemptEvaluationError("DELETE must use a digest before and ABSENT after identity")
        if self.change_kind in {"MODIFY", "RENAME", "TYPE_CHANGE"} and ABSENT in {self.before, self.after}:
            raise AttemptEvaluationError(f"{self.change_kind} must use digest identities on both sides")

    @property
    def content_identity(self) -> dict[str, str]:
        return {"before": self.before, "after": self.after}

    def to_mapping(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "change_kind": self.change_kind,
            "content_identity": self.content_identity,
            "source_path": self.source_path,
        }


@dataclass(frozen=True, slots=True)
class CandidateIdentityV1:
    kind: str
    head: str
    dirty_manifest: tuple[DirtyPathEntryV1, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in {"GIT_COMMIT", "DIRTY_SCOPE"}:
            raise AttemptEvaluationError("candidate kind is invalid")
        object.__setattr__(self, "head", _git_sha(self.head, "candidate.head"))
        manifest = tuple(self.dirty_manifest)
        if any(not isinstance(item, DirtyPathEntryV1) for item in manifest):
            raise AttemptEvaluationError("dirty_manifest contains an invalid entry")
        if self.kind == "GIT_COMMIT" and manifest:
            raise AttemptEvaluationError("GIT_COMMIT cannot contain dirty_manifest")
        keys = [(item.path, item.source_path or "") for item in manifest]
        if keys != sorted(keys) or len({item.path for item in manifest}) != len(manifest):
            raise AttemptEvaluationError("dirty_manifest is not canonically ordered")
        rename_sources = tuple(item.source_path for item in manifest if item.change_kind == "RENAME")
        if len(set(rename_sources)) != len(rename_sources):
            raise AttemptEvaluationError("a rename source may participate at most once")
        non_rename_paths = {item.path for item in manifest if item.change_kind != "RENAME"}
        if any(source in non_rename_paths for source in rename_sources):
            raise AttemptEvaluationError("rename source collides with another path transition")
        object.__setattr__(self, "dirty_manifest", manifest)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "head": self.head,
            "dirty_manifest": [item.to_mapping() for item in self.dirty_manifest],
        }


@dataclass(frozen=True, slots=True)
class IdentityRefV1:
    ref: str
    identity: str | None = None

    def __post_init__(self) -> None:
        object.__setattr__(self, "ref", _nonempty(self.ref, "identity.ref"))
        if self.identity is not None:
            object.__setattr__(self, "identity", _nonempty(self.identity, "identity.identity"))

    def to_mapping(self) -> dict[str, str | None]:
        return {"ref": self.ref, "identity": self.identity}


@dataclass(frozen=True, slots=True)
class AttemptRecordV1:
    attempt_id: str
    change_id: str
    task_or_operation_id: str
    attempt_ordinal: int
    authorization_ref: str
    acceptance_contract_ref: str
    candidate_identity: CandidateIdentityV1
    baseline_refs: tuple[IdentityRefV1, ...]
    operation_guidance_ref: str | None = None
    prompt_composition_ref: str | None = None
    parent_attempt_ref: str | None = None
    addresses_finding_refs: tuple[str, ...] = ()
    observed_result_ref: str | None = None
    verifier_contract_refs: tuple[VerifierContractIdentity, ...] = ()

    def __post_init__(self) -> None:
        change_id = _nonempty(self.change_id, "change_id")
        task_id = _nonempty(self.task_or_operation_id, "task_or_operation_id")
        object.__setattr__(self, "change_id", change_id)
        object.__setattr__(self, "task_or_operation_id", task_id)
        if not isinstance(self.attempt_ordinal, int) or isinstance(self.attempt_ordinal, bool) or self.attempt_ordinal < 1:
            raise AttemptEvaluationError("attempt_ordinal must be a positive integer")
        expected = f"{change_id}/{task_id}/A{self.attempt_ordinal}"
        if self.attempt_id != expected:
            raise AttemptEvaluationError("attempt_id does not match Change/task/ordinal")
        object.__setattr__(self, "authorization_ref", _nonempty(self.authorization_ref, "authorization_ref"))
        object.__setattr__(self, "acceptance_contract_ref", _nonempty(self.acceptance_contract_ref, "acceptance_contract_ref"))
        if not isinstance(self.candidate_identity, CandidateIdentityV1):
            raise AttemptEvaluationError("candidate_identity is invalid")
        refs = tuple(self.baseline_refs)
        if not refs or any(not isinstance(ref, IdentityRefV1) for ref in refs):
            raise AttemptEvaluationError("baseline_refs must contain IdentityRefV1 values")
        object.__setattr__(self, "baseline_refs", refs)
        for field_name in ("operation_guidance_ref", "prompt_composition_ref", "parent_attempt_ref", "observed_result_ref"):
            value = getattr(self, field_name)
            if value is not None:
                object.__setattr__(self, field_name, _nonempty(value, field_name))
        object.__setattr__(self, "addresses_finding_refs", _tuple_strings(self.addresses_finding_refs, "addresses_finding_refs"))
        raw_verifier_refs = tuple(self.verifier_contract_refs)
        try:
            verifier_refs = _tuple_verifier_identities(raw_verifier_refs, "verifier_contract_refs")
        except AttemptEvaluationError as exc:
            # Preserve a structurally malformed fixture so the evaluator can
            # return the contract-level NOT_EVALUATED boundary deterministically.
            if "duplicate composite identities" in str(exc):
                raise
            if any(not isinstance(item, (str, bytes, Mapping, Sequence)) for item in raw_verifier_refs):
                raise
            verifier_refs = raw_verifier_refs  # type: ignore[assignment]
        object.__setattr__(self, "verifier_contract_refs", verifier_refs)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "attempt_id": self.attempt_id,
            "change_id": self.change_id,
            "task_or_operation_id": self.task_or_operation_id,
            "attempt_ordinal": self.attempt_ordinal,
            "authorization_ref": self.authorization_ref,
            "acceptance_contract_ref": self.acceptance_contract_ref,
            "operation_guidance_ref": self.operation_guidance_ref,
            "candidate_identity": self.candidate_identity.to_mapping(),
            "baseline_refs": [ref.to_mapping() for ref in self.baseline_refs],
            "prompt_composition_ref": self.prompt_composition_ref,
            "parent_attempt_ref": self.parent_attempt_ref,
            "addresses_finding_refs": list(self.addresses_finding_refs),
            "observed_result_ref": self.observed_result_ref,
            "verifier_contract_refs": [
                _verifier_identity_mapping(item) if isinstance(item, tuple) and len(item) == 2 else item
                for item in self.verifier_contract_refs
            ],
        }


def _lineage_item(value: AttemptRecordV1 | Mapping[str, Any]) -> tuple[str, str, int]:
    if isinstance(value, AttemptRecordV1):
        return value.change_id, value.task_or_operation_id, value.attempt_ordinal
    data = _mapping(value, "attempt lineage item")
    change_id = _nonempty(data.get("change_id"), "lineage.change_id")
    task_id = _nonempty(data.get("task_or_operation_id"), "lineage.task_or_operation_id")
    ordinal = data.get("attempt_ordinal")
    if not isinstance(ordinal, int) or isinstance(ordinal, bool) or ordinal < 1:
        raise AttemptEvaluationError("lineage.attempt_ordinal must be positive")
    attempt_id = data.get("attempt_id")
    if attempt_id != f"{change_id}/{task_id}/A{ordinal}":
        raise AttemptEvaluationError("lineage attempt_id is inconsistent")
    return change_id, task_id, ordinal


def allocate_attempt_ordinal(
    lineage: Sequence[AttemptRecordV1 | Mapping[str, Any]],
    *,
    change_id: str,
    task_or_operation_id: str,
) -> int:
    """Allocate the next ordinal from a complete ledger-scoped lineage."""

    change_id = _nonempty(change_id, "change_id")
    task_or_operation_id = _nonempty(task_or_operation_id, "task_or_operation_id")
    rows = [_lineage_item(item) for item in lineage]
    ordinals: list[int] = []
    for row_change, row_task, ordinal in rows:
        if row_change != change_id or row_task != task_or_operation_id:
            raise AttemptEvaluationError("lineage belongs to another Change/task")
        ordinals.append(ordinal)
    expected = list(range(1, len(ordinals) + 1))
    if sorted(ordinals) != expected or len(set(ordinals)) != len(ordinals):
        raise AttemptEvaluationError("Attempt lineage must be contiguous and non-reused")
    return len(ordinals) + 1


validate_attempt_lineage = allocate_attempt_ordinal


def validate_corrective_attempt(
    attempt: AttemptRecordV1,
    *,
    parent: AttemptRecordV1,
    prior_lineage: Sequence[AttemptRecordV1],
    prior_findings: Sequence[FindingV1],
) -> AttemptRecordV1:
    """Validate one corrective Attempt against explicit prior Finding carriers."""

    if not isinstance(attempt, AttemptRecordV1) or not isinstance(parent, AttemptRecordV1):
        raise AttemptEvaluationError("corrective Attempt and parent must be AttemptRecordV1")
    lineage = tuple(prior_lineage)
    if any(not isinstance(item, AttemptRecordV1) for item in lineage):
        raise AttemptEvaluationError("prior lineage contains an invalid Attempt")
    if parent not in lineage:
        raise AttemptEvaluationError("parent Attempt is absent from supplied lineage")
    if attempt.parent_attempt_ref != parent.attempt_id:
        raise AttemptEvaluationError("corrective Attempt parent reference does not match parent")
    if (attempt.change_id, attempt.task_or_operation_id) != (parent.change_id, parent.task_or_operation_id):
        raise AttemptEvaluationError("corrective Attempt crosses Change/task lineage")
    expected = allocate_attempt_ordinal(
        lineage,
        change_id=parent.change_id,
        task_or_operation_id=parent.task_or_operation_id,
    )
    lineage_by_id = {item.attempt_id: item for item in lineage}
    for item in lineage:
        if item.parent_attempt_ref is None:
            continue
        lineage_parent = lineage_by_id.get(item.parent_attempt_ref)
        if lineage_parent is None or lineage_parent.attempt_ordinal >= item.attempt_ordinal:
            raise AttemptEvaluationError("prior Attempt lineage has an invalid parent link")
    prior_authorizations = {item.authorization_ref for item in lineage}
    if len(prior_authorizations) != len(lineage):
        raise AttemptEvaluationError("prior Attempt lineage reuses authorization provenance")
    if attempt.authorization_ref in prior_authorizations:
        raise AttemptEvaluationError("corrective Attempt requires a previously unused authorization provenance")
    findings = tuple(prior_findings)
    if any(not isinstance(item, FindingV1) for item in findings):
        raise AttemptEvaluationError("prior Findings contain an invalid carrier")
    finding_ids = tuple(item.finding_id for item in findings)
    if len(set(finding_ids)) != len(finding_ids):
        raise AttemptEvaluationError("prior Finding identities must be unique")
    for item in findings:
        applicability = item.applicability
        if applicability is None:
            raise AttemptEvaluationError("prior Finding applicability is required")
        source_attempt = lineage_by_id.get(applicability.attempt_id)
        if source_attempt is None:
            raise AttemptEvaluationError("prior Finding belongs to a foreign Attempt")
        if (
            applicability.candidate_identity != source_attempt.candidate_identity
            or not _same_baselines(applicability.input_baseline_refs, source_attempt.baseline_refs)
            or applicability.acceptance_contract_ref != source_attempt.acceptance_contract_ref
        ):
            raise AttemptEvaluationError("prior Finding provenance does not match its Attempt")
    permitted = set(finding_ids)
    addressed = set(attempt.addresses_finding_refs)
    if not addressed or not addressed.issubset(permitted):
        raise AttemptEvaluationError("corrective Attempt addresses a foreign or missing Finding")
    if attempt.attempt_ordinal != expected:
        raise AttemptEvaluationError("corrective Attempt does not use the next lineage ordinal")
    return attempt


@dataclass(frozen=True, slots=True)
class ObservedResultV1:
    result_id: str
    attempt_id: str
    execution_status: str
    changed_paths: tuple[str, ...] = ()
    fact_refs: tuple[str, ...] = ()
    artifact_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "result_id", _nonempty(self.result_id, "result_id"))
        object.__setattr__(self, "attempt_id", _nonempty(self.attempt_id, "attempt_id"))
        if self.execution_status not in EXECUTION_STATUSES:
            raise AttemptEvaluationError("execution_status is invalid")
        changed_paths = tuple(_path(p, "changed_paths[]") for p in self.changed_paths)
        if len(set(changed_paths)) != len(changed_paths):
            raise AttemptEvaluationError("changed_paths must not contain duplicates")
        object.__setattr__(self, "changed_paths", changed_paths)
        object.__setattr__(self, "fact_refs", _tuple_strings(self.fact_refs, "fact_refs"))
        object.__setattr__(self, "artifact_refs", _tuple_strings(self.artifact_refs, "artifact_refs"))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "result_id": self.result_id,
            "attempt_id": self.attempt_id,
            "execution_status": self.execution_status,
            "changed_paths": list(self.changed_paths),
            "fact_refs": list(self.fact_refs),
            "artifact_refs": list(self.artifact_refs),
        }


@dataclass(frozen=True, slots=True)
class VerifierContractV1:
    acceptance_contract_ref: str
    contract_id: str
    contract_version_or_ref: str
    required: bool
    evidence_class: str
    predicate: str
    required_evidence_refs: tuple[str, ...] = ()
    failure_semantics: str = ""

    def __post_init__(self) -> None:
        for name in ("acceptance_contract_ref", "contract_id", "contract_version_or_ref", "evidence_class", "predicate", "failure_semantics"):
            object.__setattr__(self, name, _nonempty(getattr(self, name), name))
        if not isinstance(self.required, bool):
            raise AttemptEvaluationError("required must be boolean")
        object.__setattr__(self, "required_evidence_refs", _tuple_strings(self.required_evidence_refs, "required_evidence_refs"))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "acceptance_contract_ref": self.acceptance_contract_ref,
            "contract_id": self.contract_id,
            "contract_version_or_ref": self.contract_version_or_ref,
            "required": self.required,
            "evidence_class": self.evidence_class,
            "predicate": self.predicate,
            "required_evidence_refs": list(self.required_evidence_refs),
            "failure_semantics": self.failure_semantics,
        }


@dataclass(frozen=True, slots=True)
class AcceptanceContractV1:
    """Immutable, evaluator-supplied carrier for the complete verifier set."""

    acceptance_contract_ref: str
    verifier_contracts: tuple[VerifierContractV1, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "acceptance_contract_ref", _nonempty(self.acceptance_contract_ref, "acceptance_contract_ref"))
        values = tuple(self.verifier_contracts)
        if not values or any(not isinstance(item, VerifierContractV1) for item in values):
            raise AttemptEvaluationError("acceptance contract requires a complete verifier set")
        if any(item.acceptance_contract_ref != self.acceptance_contract_ref for item in values):
            raise AttemptEvaluationError("verifier contract is bound to another acceptance contract")
        identities = [(item.contract_id, item.contract_version_or_ref) for item in values]
        if len(set(identities)) != len(identities):
            raise AttemptEvaluationError("acceptance contract verifier identities must be unique")
        object.__setattr__(self, "verifier_contracts", values)

    @property
    def required_contracts(self) -> tuple[VerifierContractV1, ...]:
        return tuple(item for item in self.verifier_contracts if item.required)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "acceptance_contract_ref": self.acceptance_contract_ref,
            "verifier_contracts": [item.to_mapping() for item in self.verifier_contracts],
        }


@dataclass(frozen=True, slots=True)
class EvidenceApplicabilityV1:
    attempt_id: str
    candidate_identity: CandidateIdentityV1
    acceptance_contract_ref: str
    verifier_contract_ref: str
    verifier_contract_version_or_ref: str
    evaluation_scope_ref: str
    finding_refs: tuple[str, ...] = ()
    input_baseline_refs: tuple[IdentityRefV1, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "attempt_id", _nonempty(self.attempt_id, "applicability.attempt_id"))
        if not isinstance(self.candidate_identity, CandidateIdentityV1):
            raise AttemptEvaluationError("applicability.candidate_identity is invalid")
        object.__setattr__(self, "acceptance_contract_ref", _nonempty(self.acceptance_contract_ref, "applicability.acceptance_contract_ref"))
        object.__setattr__(self, "verifier_contract_ref", _nonempty(self.verifier_contract_ref, "applicability.verifier_contract_ref"))
        object.__setattr__(self, "verifier_contract_version_or_ref", _nonempty(self.verifier_contract_version_or_ref, "applicability.verifier_contract_version_or_ref"))
        object.__setattr__(self, "evaluation_scope_ref", _nonempty(self.evaluation_scope_ref, "applicability.evaluation_scope_ref"))
        object.__setattr__(self, "finding_refs", _tuple_strings(self.finding_refs, "applicability.finding_refs"))
        refs = tuple(self.input_baseline_refs)
        if any(not isinstance(ref, IdentityRefV1) for ref in refs):
            raise AttemptEvaluationError("input_baseline_refs is invalid")
        object.__setattr__(self, "input_baseline_refs", refs)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "candidate_identity": self.candidate_identity.to_mapping(),
            "acceptance_contract_ref": self.acceptance_contract_ref,
            "verifier_contract_ref": self.verifier_contract_ref,
            "verifier_contract_version_or_ref": self.verifier_contract_version_or_ref,
            "evaluation_scope_ref": self.evaluation_scope_ref,
            "finding_refs": list(self.finding_refs),
            "input_baseline_refs": [ref.to_mapping() for ref in self.input_baseline_refs],
        }


@dataclass(frozen=True, slots=True)
class FindingApplicabilityV1:
    attempt_id: str
    candidate_identity: CandidateIdentityV1
    acceptance_contract_ref: str
    evaluation_scope_ref: str
    input_baseline_refs: tuple[IdentityRefV1, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "attempt_id", _nonempty(self.attempt_id, "finding_applicability.attempt_id"))
        if not isinstance(self.candidate_identity, CandidateIdentityV1):
            raise AttemptEvaluationError("finding_applicability.candidate_identity is invalid")
        object.__setattr__(self, "acceptance_contract_ref", _nonempty(self.acceptance_contract_ref, "finding_applicability.acceptance_contract_ref"))
        object.__setattr__(self, "evaluation_scope_ref", _nonempty(self.evaluation_scope_ref, "finding_applicability.evaluation_scope_ref"))
        refs = tuple(self.input_baseline_refs)
        if not refs or any(not isinstance(ref, IdentityRefV1) for ref in refs):
            raise AttemptEvaluationError("finding_applicability.input_baseline_refs is invalid")
        object.__setattr__(self, "input_baseline_refs", refs)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "attempt_id": self.attempt_id,
            "candidate_identity": self.candidate_identity.to_mapping(),
            "acceptance_contract_ref": self.acceptance_contract_ref,
            "evaluation_scope_ref": self.evaluation_scope_ref,
            "input_baseline_refs": [ref.to_mapping() for ref in self.input_baseline_refs],
        }


@dataclass(frozen=True, slots=True)
class VerifierEvidenceV1:
    evidence_id: str
    attempt_id: str
    candidate_identity: CandidateIdentityV1
    verifier_contract_ref: str
    verifier_contract_version_or_ref: str
    outcome: str
    evidence_refs: tuple[str, ...]
    applicability: EvidenceApplicabilityV1
    claim_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        object.__setattr__(self, "evidence_id", _nonempty(self.evidence_id, "evidence_id"))
        object.__setattr__(self, "attempt_id", _nonempty(self.attempt_id, "attempt_id"))
        if not isinstance(self.candidate_identity, CandidateIdentityV1):
            raise AttemptEvaluationError("evidence.candidate_identity is invalid")
        object.__setattr__(self, "verifier_contract_ref", _nonempty(self.verifier_contract_ref, "verifier_contract_ref"))
        object.__setattr__(self, "verifier_contract_version_or_ref", _nonempty(self.verifier_contract_version_or_ref, "verifier_contract_version_or_ref"))
        if self.outcome not in VERIFIER_OUTCOMES:
            raise AttemptEvaluationError("verifier evidence outcome is invalid")
        object.__setattr__(self, "evidence_refs", _tuple_strings(self.evidence_refs, "evidence_refs"))
        object.__setattr__(self, "claim_refs", _tuple_strings(self.claim_refs, "claim_refs"))
        if not isinstance(self.applicability, EvidenceApplicabilityV1):
            raise AttemptEvaluationError("evidence applicability is invalid")
        if (
            self.applicability.attempt_id != self.attempt_id
            or self.applicability.candidate_identity != self.candidate_identity
            or self.applicability.verifier_contract_ref != self.verifier_contract_ref
            or self.applicability.verifier_contract_version_or_ref != self.verifier_contract_version_or_ref
        ):
            raise AttemptEvaluationError("evidence and applicability identity mismatch")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "attempt_id": self.attempt_id,
            "candidate_identity": self.candidate_identity.to_mapping(),
            "verifier_contract_ref": self.verifier_contract_ref,
            "verifier_contract_version_or_ref": self.verifier_contract_version_or_ref,
            "outcome": self.outcome,
            "evidence_refs": list(self.evidence_refs),
            "claim_refs": list(self.claim_refs),
            "applicability": self.applicability.to_mapping(),
        }


@dataclass(frozen=True, slots=True)
class EvidenceSupersessionV1:
    prior_evidence_ref: str
    successor_evidence_ref: str
    current_acceptance_scope_ref: str
    rechecked_claim_refs: tuple[str, ...]
    reason: str

    def __post_init__(self) -> None:
        for name in ("prior_evidence_ref", "successor_evidence_ref", "current_acceptance_scope_ref", "reason"):
            object.__setattr__(self, name, _nonempty(getattr(self, name), name))
        if self.prior_evidence_ref == self.successor_evidence_ref:
            raise AttemptEvaluationError("supersession cannot point to itself")
        object.__setattr__(self, "rechecked_claim_refs", _tuple_strings(self.rechecked_claim_refs, "rechecked_claim_refs"))
        if not self.rechecked_claim_refs:
            raise AttemptEvaluationError("supersession requires explicit rechecked claims")

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "prior_evidence_ref": self.prior_evidence_ref,
            "successor_evidence_ref": self.successor_evidence_ref,
            "current_acceptance_scope_ref": self.current_acceptance_scope_ref,
            "rechecked_claim_refs": list(self.rechecked_claim_refs),
            "reason": self.reason,
        }


@dataclass(frozen=True, slots=True)
class FindingV1:
    finding_id: str
    statement: str
    severity: str
    responsibility_domains: tuple[str, ...]
    acceptance_impact: str
    disposition: str
    evidence_refs: tuple[str, ...]
    owner_adjudication_ref: str | None = None
    applicability: FindingApplicabilityV1 | None = None

    def __post_init__(self) -> None:
        for name in ("finding_id", "statement"):
            object.__setattr__(self, name, _nonempty(getattr(self, name), name))
        if self.severity not in SEVERITIES:
            raise AttemptEvaluationError("finding severity is invalid")
        domains = _tuple_strings(self.responsibility_domains, "responsibility_domains")
        if not domains or any(domain not in RESPONSIBILITY_DOMAINS for domain in domains):
            raise AttemptEvaluationError("finding responsibility_domains are invalid")
        object.__setattr__(self, "responsibility_domains", domains)
        if self.acceptance_impact not in ACCEPTANCE_IMPACTS:
            raise AttemptEvaluationError("finding acceptance_impact is invalid")
        if self.disposition not in DISPOSITIONS:
            raise AttemptEvaluationError("finding disposition is invalid")
        object.__setattr__(self, "evidence_refs", _tuple_strings(self.evidence_refs, "finding.evidence_refs"))
        if not self.evidence_refs:
            raise AttemptEvaluationError("finding requires evidence_refs")
        if self.disposition in {"DEFERRED", "CLOSED", "REMEDIATION_REQUIRED"} and self.owner_adjudication_ref is None:
            raise AttemptEvaluationError("owner-governed disposition requires owner_adjudication_ref")
        if self.owner_adjudication_ref is not None:
            object.__setattr__(self, "owner_adjudication_ref", _nonempty(self.owner_adjudication_ref, "owner_adjudication_ref"))
        if self.applicability is not None and not isinstance(self.applicability, FindingApplicabilityV1):
            raise AttemptEvaluationError("finding applicability is invalid")
        if self.disposition == "DEFERRED" and self.acceptance_impact != "NON_BLOCKING":
            raise AttemptEvaluationError("DEFERRED finding must be NON_BLOCKING")

    @property
    def unresolved(self) -> bool:
        return self.disposition in {"OPEN", "REMEDIATION_REQUIRED"}

    @property
    def blocks_acceptance(self) -> bool:
        return self.acceptance_impact == "BLOCKING" and self.unresolved

    def to_mapping(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "statement": self.statement,
            "severity": self.severity,
            "responsibility_domains": list(self.responsibility_domains),
            "acceptance_impact": self.acceptance_impact,
            "disposition": self.disposition,
            "owner_adjudication_ref": self.owner_adjudication_ref,
            "evidence_refs": list(self.evidence_refs),
            "applicability": None if self.applicability is None else self.applicability.to_mapping(),
        }


@dataclass(frozen=True, slots=True)
class TechnicalEvaluationV1:
    evaluation_id: str
    attempt_id: str
    candidate_identity: CandidateIdentityV1 | None
    acceptance_contract_ref: str
    declared_verifier_contract_refs: tuple[VerifierContractIdentity, ...]
    required_verifier_contract_refs: tuple[VerifierContractIdentity, ...]
    outcome: str
    evidence_complete: bool
    required_evidence_refs: tuple[str, ...]
    applicable_finding_refs: tuple[str, ...]
    reason_codes: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "evaluation_id", _nonempty(self.evaluation_id, "evaluation_id"))
        object.__setattr__(self, "attempt_id", _nonempty(self.attempt_id, "attempt_id"))
        if not isinstance(self.candidate_identity, CandidateIdentityV1) and not (
            self.candidate_identity is None and self.outcome == "NOT_EVALUATED"
        ):
            raise AttemptEvaluationError("evaluation candidate_identity is invalid")
        object.__setattr__(self, "acceptance_contract_ref", _nonempty(self.acceptance_contract_ref, "acceptance_contract_ref"))
        declared_refs = _tuple_verifier_identities(self.declared_verifier_contract_refs, "declared_verifier_contract_refs")
        required_refs = _tuple_verifier_identities(self.required_verifier_contract_refs, "required_verifier_contract_refs")
        if not set(required_refs).issubset(set(declared_refs)):
            raise AttemptEvaluationError("required verifier identities must be a subset of declared verifier identities")
        if self.outcome not in EVALUATION_OUTCOMES:
            raise AttemptEvaluationError("evaluation outcome is invalid")
        if self.outcome == "SATISFIED" and not declared_refs:
            raise AttemptEvaluationError("SATISFIED evaluation requires a declared verifier carrier")
        object.__setattr__(self, "declared_verifier_contract_refs", declared_refs)
        object.__setattr__(self, "required_verifier_contract_refs", required_refs)
        if not isinstance(self.evidence_complete, bool):
            raise AttemptEvaluationError("evidence_complete must be boolean")
        object.__setattr__(self, "required_evidence_refs", _tuple_strings(self.required_evidence_refs, "required_evidence_refs"))
        object.__setattr__(self, "applicable_finding_refs", _tuple_strings(self.applicable_finding_refs, "applicable_finding_refs"))
        object.__setattr__(self, "reason_codes", _tuple_strings(self.reason_codes, "reason_codes"))

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "evaluation_id": self.evaluation_id,
            "attempt_id": self.attempt_id,
            "candidate_identity": None if self.candidate_identity is None else self.candidate_identity.to_mapping(),
            "acceptance_contract_ref": self.acceptance_contract_ref,
            "declared_verifier_contract_refs": [_verifier_identity_mapping(item) for item in self.declared_verifier_contract_refs],
            "required_verifier_contract_refs": [_verifier_identity_mapping(item) for item in self.required_verifier_contract_refs],
            "outcome": self.outcome,
            "evidence_complete": self.evidence_complete,
            "required_evidence_refs": list(self.required_evidence_refs),
            "applicable_finding_refs": list(self.applicable_finding_refs),
            "reason_codes": list(self.reason_codes),
        }


def validate_verifier_set(
    attempt: AttemptRecordV1,
    contracts: Sequence[VerifierContractV1],
    *,
    acceptance_contract_ref: str,
    acceptance_contract: AcceptanceContractV1 | None = None,
) -> tuple[VerifierContractV1, ...]:
    """Validate an independently supplied, complete approved contract set."""

    if not isinstance(attempt, AttemptRecordV1):
        raise AttemptEvaluationError("attempt is invalid")
    acceptance_contract_ref = _nonempty(acceptance_contract_ref, "acceptance_contract_ref")
    if not isinstance(acceptance_contract, AcceptanceContractV1):
        raise AttemptEvaluationError("independent acceptance contract carrier is required")
    if (
        acceptance_contract.acceptance_contract_ref != acceptance_contract_ref
        or attempt.acceptance_contract_ref != acceptance_contract_ref
    ):
        raise AttemptEvaluationError("acceptance contract reference does not match Attempt")
    values = tuple(contracts)
    if not values or any(not isinstance(item, VerifierContractV1) for item in values):
        raise AttemptEvaluationError("complete verifier contract carrier is required")
    carrier = acceptance_contract.verifier_contracts
    carrier_keys = tuple((item.contract_id, item.contract_version_or_ref) for item in carrier)
    supplied_keys = tuple((item.contract_id, item.contract_version_or_ref) for item in values)
    if len(set(supplied_keys)) != len(supplied_keys) or set(supplied_keys) != set(carrier_keys):
        raise AttemptEvaluationError("supplied verifier contracts do not match the complete acceptance carrier")
    authoritative_declared_refs = tuple((item.contract_id, item.contract_version_or_ref) for item in carrier)
    attempt_ids = _tuple_verifier_identities(attempt.verifier_contract_refs, "attempt.verifier_contract_refs")
    if len(set(attempt_ids)) != len(attempt_ids) or set(attempt_ids) != set(authoritative_declared_refs):
        raise AttemptEvaluationError("Attempt verifier contract refs must exactly match the declared acceptance set")
    return carrier


def _same_candidate(left: CandidateIdentityV1, right: CandidateIdentityV1) -> bool:
    return left.to_mapping() == right.to_mapping()


def _same_baselines(left: Sequence[IdentityRefV1], right: Sequence[IdentityRefV1]) -> bool:
    return tuple(ref.to_mapping() for ref in left) == tuple(ref.to_mapping() for ref in right)


def _contract_key(contract_id: str, version_or_ref: str) -> tuple[str, str]:
    return contract_id, version_or_ref


def _evidence_claims(item: VerifierEvidenceV1) -> tuple[str, ...]:
    return item.claim_refs or item.evidence_refs


def _effective_evidence(
    evidence: Sequence[VerifierEvidenceV1],
    supersession: Sequence[EvidenceSupersessionV1],
    *,
    evaluation_scope_ref: str,
) -> tuple[tuple[VerifierEvidenceV1, ...], frozenset[str]]:
    values = tuple(evidence)
    if len({item.evidence_id for item in values}) != len(values):
        raise AttemptEvaluationError("evidence_id values must be unique")
    by_id = {item.evidence_id: item for item in values}
    relations = tuple(supersession)
    graph: dict[str, set[str]] = {item.evidence_id: set() for item in values}
    superseded_claims: dict[str, set[str]] = {item.evidence_id: set() for item in values}
    relation_keys: set[tuple[str, str, str, tuple[str, ...]]] = set()

    for relation in relations:
        if not isinstance(relation, EvidenceSupersessionV1):
            raise AttemptEvaluationError("supersession relation is invalid")
        if relation.current_acceptance_scope_ref != evaluation_scope_ref:
            continue
        prior = by_id.get(relation.prior_evidence_ref)
        successor = by_id.get(relation.successor_evidence_ref)
        if prior is None or successor is None:
            raise AttemptEvaluationError("supersession references unknown evidence")
        if (
            prior.attempt_id != successor.attempt_id
            or not _same_candidate(prior.candidate_identity, successor.candidate_identity)
            or prior.applicability.acceptance_contract_ref != successor.applicability.acceptance_contract_ref
            or prior.applicability.evaluation_scope_ref != successor.applicability.evaluation_scope_ref
            or not _same_baselines(prior.applicability.input_baseline_refs, successor.applicability.input_baseline_refs)
            or _contract_key(prior.verifier_contract_ref, prior.verifier_contract_version_or_ref)
            != _contract_key(successor.verifier_contract_ref, successor.verifier_contract_version_or_ref)
        ):
            raise AttemptEvaluationError("supersession evidence lineage is incompatible")
        if successor.outcome not in {"PASS", "FAIL"}:
            raise AttemptEvaluationError("supersession successor must be a completed verifier result")
        claims = tuple(relation.rechecked_claim_refs)
        prior_claims = set(_evidence_claims(prior))
        successor_claims = set(_evidence_claims(successor))
        if not claims or not set(claims).issubset(prior_claims) or not set(claims).issubset(successor_claims):
            raise AttemptEvaluationError("supersession claims are not explicitly rechecked")
        relation_key = (
            relation.prior_evidence_ref,
            relation.successor_evidence_ref,
            relation.current_acceptance_scope_ref,
            claims,
        )
        if relation_key in relation_keys:
            raise AttemptEvaluationError("supersession relation is duplicated")
        relation_keys.add(relation_key)
        overlap = superseded_claims[relation.prior_evidence_ref].intersection(claims)
        if overlap:
            raise AttemptEvaluationError("one evidence claim cannot have multiple superseders")
        superseded_claims[relation.prior_evidence_ref].update(claims)
        graph[relation.prior_evidence_ref].add(relation.successor_evidence_ref)

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            raise AttemptEvaluationError("supersession relation creates a cycle")
        if node in visited:
            return
        visiting.add(node)
        for successor in sorted(graph[node]):
            visit(successor)
        visiting.remove(node)
        visited.add(node)

    for evidence_id in sorted(graph):
        visit(evidence_id)

    current: list[VerifierEvidenceV1] = []
    for evidence_id in sorted(by_id):
        item = by_id[evidence_id]
        remaining = tuple(claim for claim in _evidence_claims(item) if claim not in superseded_claims[evidence_id])
        if remaining:
            current.append(replace(item, claim_refs=remaining))
    targets = frozenset(target for successors in graph.values() for target in successors)
    return tuple(current), targets


def _evidence_meets_contract(item: VerifierEvidenceV1, contract: VerifierContractV1) -> bool:
    required = set(contract.required_evidence_refs)
    return required.issubset(item.evidence_refs)


def _not_evaluated(
    *,
    evaluation_id: object,
    attempt: object,
    acceptance_contract_ref: object,
    reason_code: str,
) -> TechnicalEvaluationV1:
    """Build a stable fail-closed result even when identity fields are invalid."""

    try:
        safe_evaluation_id = _nonempty(evaluation_id, "evaluation_id")
    except AttemptEvaluationError:
        safe_evaluation_id = "INVALID_EVALUATION"
    try:
        safe_acceptance_ref = _nonempty(acceptance_contract_ref, "acceptance_contract_ref")
    except AttemptEvaluationError:
        safe_acceptance_ref = "INVALID_ACCEPTANCE_CONTRACT"
    if isinstance(attempt, AttemptRecordV1):
        attempt_id = attempt.attempt_id
        candidate = attempt.candidate_identity
    else:
        attempt_id = "INVALID_ATTEMPT"
        candidate = None
    return TechnicalEvaluationV1(
        safe_evaluation_id,
        attempt_id,
        candidate,
        safe_acceptance_ref,
        (),
        (),
        "NOT_EVALUATED",
        False,
        (),
        (),
        (reason_code,),
    )


def _validate_evaluation_fixture(
    attempt: object,
    contracts: object,
    evidence: object,
    findings: object,
    supersession: object,
    *,
    acceptance_contract_ref: object,
    evaluation_scope_ref: object,
    acceptance_contract: object,
    evaluation_id: object,
    evaluation_run: object,
    candidate_quality: object,
) -> tuple[
    str,
    str,
    tuple[VerifierContractV1, ...],
    tuple[VerifierEvidenceV1, ...],
    tuple[FindingV1, ...],
    tuple[EvidenceSupersessionV1, ...],
]:
    """Validate the bounded structural fixture before evidence aggregation."""

    _nonempty(evaluation_id, "evaluation_id")
    acceptance_ref = _nonempty(acceptance_contract_ref, "acceptance_contract_ref")
    scope_ref = _nonempty(evaluation_scope_ref, "evaluation_scope_ref")
    if not isinstance(evaluation_run, bool) or not isinstance(candidate_quality, bool):
        raise AttemptEvaluationError("evaluation state flags must be boolean")
    if not isinstance(attempt, AttemptRecordV1):
        raise AttemptEvaluationError("attempt is invalid")
    contract_values = tuple(contracts)  # type: ignore[arg-type]
    contract_values = validate_verifier_set(
        attempt,
        contract_values,
        acceptance_contract_ref=acceptance_ref,
        acceptance_contract=acceptance_contract if isinstance(acceptance_contract, AcceptanceContractV1) else None,
    )
    evidence_values = tuple(evidence)  # type: ignore[arg-type]
    if any(not isinstance(item, VerifierEvidenceV1) for item in evidence_values):
        raise AttemptEvaluationError("verifier evidence is invalid")
    if len({item.evidence_id for item in evidence_values}) != len(evidence_values):
        raise AttemptEvaluationError("evidence_id values must be unique")
    finding_values = tuple(findings)  # type: ignore[arg-type]
    if any(not isinstance(item, FindingV1) for item in finding_values):
        raise AttemptEvaluationError("finding carrier is invalid")
    if any(item.applicability is None for item in finding_values):
        raise AttemptEvaluationError("finding applicability is required")
    if len({item.finding_id for item in finding_values}) != len(finding_values):
        raise AttemptEvaluationError("finding identities must be unique")
    supersession_values = tuple(supersession)  # type: ignore[arg-type]
    if any(not isinstance(item, EvidenceSupersessionV1) for item in supersession_values):
        raise AttemptEvaluationError("supersession relation is invalid")
    return (
        acceptance_ref,
        scope_ref,
        contract_values,
        evidence_values,
        finding_values,
        supersession_values,
    )


def evaluate_technical(
    attempt: AttemptRecordV1,
    contracts: Sequence[VerifierContractV1],
    evidence: Sequence[VerifierEvidenceV1],
    findings: Sequence[FindingV1] = (),
    *,
    acceptance_contract_ref: str,
    evaluation_scope_ref: str,
    acceptance_contract: AcceptanceContractV1 | None = None,
    supersession: Sequence[EvidenceSupersessionV1] = (),
    evaluation_id: str = "EVALUATION-1",
    evaluation_run: bool = True,
    candidate_quality: bool = True,
) -> TechnicalEvaluationV1:
    """Return the derived evaluation using the frozen four-state precedence."""

    try:
        (
            acceptance_ref,
            scope_ref,
            contracts_tuple,
            evidence_values,
            finding_values,
            supersession_values,
        ) = _validate_evaluation_fixture(
            attempt,
            contracts,
            evidence,
            findings,
            supersession,
            acceptance_contract_ref=acceptance_contract_ref,
            evaluation_scope_ref=evaluation_scope_ref,
            acceptance_contract=acceptance_contract,
            evaluation_id=evaluation_id,
            evaluation_run=evaluation_run,
            candidate_quality=candidate_quality,
        )
        if not evaluation_run or not candidate_quality:
            return _not_evaluated(
                evaluation_id=evaluation_id,
                attempt=attempt,
                acceptance_contract_ref=acceptance_ref,
                reason_code="NOT_EVALUATED",
            )
        applicable_evidence: list[VerifierEvidenceV1] = []
        contract_keys = {_contract_key(item.contract_id, item.contract_version_or_ref) for item in contracts_tuple}
        for item in evidence_values:
            app = item.applicability
            item_key = _contract_key(item.verifier_contract_ref, item.verifier_contract_version_or_ref)
            if (
                item_key in contract_keys
                and item.attempt_id == attempt.attempt_id
                and _same_candidate(item.candidate_identity, attempt.candidate_identity)
                and _same_candidate(app.candidate_identity, attempt.candidate_identity)
                and app.acceptance_contract_ref == acceptance_ref
                and app.evaluation_scope_ref == scope_ref
                and _same_baselines(app.input_baseline_refs, attempt.baseline_refs)
            ):
                applicable_evidence.append(item)
        effective, supersession_targets = _effective_evidence(
            applicable_evidence,
            supersession_values,
            evaluation_scope_ref=scope_ref,
        )
    except (AttemptEvaluationError, TypeError):
        return _not_evaluated(
            evaluation_id=evaluation_id,
            attempt=attempt,
            acceptance_contract_ref=acceptance_contract_ref,
            reason_code="INVALID_CONTRACT_OR_FIXTURE",
        )

    required = tuple((item.contract_id, item.contract_version_or_ref) for item in contracts_tuple if item.required)
    applicable_findings = tuple(
        item for item in finding_values
        if item.applicability is not None
        and item.applicability.attempt_id == attempt.attempt_id
        and _same_candidate(item.applicability.candidate_identity, attempt.candidate_identity)
        and item.applicability.acceptance_contract_ref == acceptance_ref
        and item.applicability.evaluation_scope_ref == scope_ref
        and _same_baselines(item.applicability.input_baseline_refs, attempt.baseline_refs)
    )
    non_applicable_finding_ids = tuple(
        item.finding_id for item in finding_values if item not in applicable_findings
    )
    blocking = tuple(item for item in applicable_findings if item.blocks_acceptance)
    current_by_contract: dict[tuple[str, str], list[VerifierEvidenceV1]] = {
        _contract_key(item.contract_id, item.contract_version_or_ref): [] for item in contracts_tuple
    }
    for item in effective:
        key = _contract_key(item.verifier_contract_ref, item.verifier_contract_version_or_ref)
        if key in current_by_contract:
            current_by_contract[key].append(item)
    fail_contracts: list[VerifierContractIdentity] = []
    missing_contracts: list[VerifierContractIdentity] = []
    evidence_refs: list[str] = []
    evidence_ref_set: set[str] = set()
    conflict = False
    for contract in (item for item in contracts_tuple if item.required):
        contract_identity = (contract.contract_id, contract.contract_version_or_ref)
        current = sorted(
            current_by_contract[_contract_key(contract.contract_id, contract.contract_version_or_ref)],
            key=lambda item: item.evidence_id,
        )
        if not current:
            missing_contracts.append(contract_identity)
            continue
        combined_refs: list[str] = []
        combined_ref_set: set[str] = set()
        for item in current:
            for ref in item.evidence_refs:
                if ref not in combined_ref_set:
                    combined_ref_set.add(ref)
                    combined_refs.append(ref)
        contract_evidence_complete = set(contract.required_evidence_refs).issubset(combined_ref_set)
        claim_sets = [set(_evidence_claims(item)) for item in current]
        claims_overlap = any(
            left.intersection(right)
            for index, left in enumerate(claim_sets)
            for right in claim_sets[index + 1:]
        )
        explicit_claim_partition = (
            len(current) == 1
            or (
                all(item.evidence_id in supersession_targets for item in current)
                and not claims_overlap
            )
        )
        if not contract_evidence_complete:
            missing_contracts.append(contract_identity)
        for ref in combined_refs:
            if ref not in evidence_ref_set:
                evidence_ref_set.add(ref)
                evidence_refs.append(ref)
        if any(item.outcome == "FAIL" for item in current) and contract_evidence_complete:
            fail_contracts.append(contract_identity)
        elif any(item.outcome != "PASS" for item in current):
            if contract_identity not in missing_contracts:
                missing_contracts.append(contract_identity)
        if not explicit_claim_partition:
            conflict = True
            if contract_identity not in missing_contracts:
                missing_contracts.append(contract_identity)
        elif all(item.outcome == "PASS" for item in current) and not contract_evidence_complete:
            if contract_identity not in missing_contracts:
                missing_contracts.append(contract_identity)
    reason_codes: list[str] = []
    if fail_contracts or blocking:
        outcome = "NOT_SATISFIED"
        reason_codes.extend(f"REQUIRED_FAIL:{item[0]}|{item[1]}" for item in fail_contracts)
        reason_codes.extend(f"BLOCKING_FINDING:{item.finding_id}" for item in blocking)
    elif missing_contracts or conflict:
        outcome = "INDETERMINATE"
        reason_codes.extend(f"REQUIRED_EVIDENCE_MISSING:{item[0]}|{item[1]}" for item in missing_contracts)
        if conflict:
            reason_codes.append("CONFLICTING_CURRENT_EVIDENCE")
    else:
        outcome = "SATISFIED"
        reason_codes.append("ALL_REQUIRED_PASS")
    reason_codes.extend(f"NON_APPLICABLE_FINDING:{finding_id}" for finding_id in non_applicable_finding_ids)
    return TechnicalEvaluationV1(
        evaluation_id,
        attempt.attempt_id,
        attempt.candidate_identity,
        acceptance_ref,
        tuple((item.contract_id, item.contract_version_or_ref) for item in contracts_tuple),
        required,
        outcome,
        not missing_contracts and not conflict,
        tuple(evidence_refs),
        tuple(item.finding_id for item in applicable_findings),
        tuple(reason_codes),
    )


def sha256_identity(value: object) -> str:
    """Hash a canonical JSON-compatible bounded identity."""

    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


__all__ = [
    "ABSENT",
    "ACCEPTANCE_IMPACTS",
    "AcceptanceContractV1",
    "AttemptEvaluationError",
    "AttemptRecordV1",
    "CandidateIdentityV1",
    "DirtyPathEntryV1",
    "EvidenceApplicabilityV1",
    "EvidenceSupersessionV1",
    "FindingApplicabilityV1",
    "FindingV1",
    "IdentityRefV1",
    "ObservedResultV1",
    "RESPONSIBILITY_DOMAINS",
    "TechnicalEvaluationV1",
    "VerifierContractV1",
    "VerifierContractIdentity",
    "VerifierEvidenceV1",
    "allocate_attempt_ordinal",
    "canonical_json_bytes",
    "evaluate_technical",
    "sha256_identity",
    "validate_attempt_lineage",
    "validate_corrective_attempt",
    "validate_verifier_set",
]
