"""Pattern-B coordinator for one bounded governed operation.

The lifecycle owns ordering only.  Attempt Runtime owns occurrence/state,
Telemetry owns receipt validation/storage/readback, and PL08 owns evaluation.
There is no lifecycle store, queue, worker, retry, callback, or next-gate
authority here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .attempt_evaluation import (
    AcceptanceContractV1,
    EvidenceSupersessionV1,
    FindingV1,
    FindingApplicabilityV1,
    CandidateIdentityV1,
    DirtyPathEntryV1,
    EvidenceApplicabilityV1,
    ObservedResultV1,
    IdentityRefV1,
    VerifierContractV1,
    VerifierEvidenceV1,
    evaluate_technical,
)
from .attempt_runtime import (
    AdmissibilityOutcome,
    AttemptRuntimeError,
    LookupOutcome,
    check_activation_admissibility,
    claim_attempt,
    lookup_attempt,
    terminalize_attempt,
)
from .governed_executor import (
    GovernedExecutionCompletionV1,
    GovernedExecutionEnvelopeV1,
    GovernedExecutionResultV1,
    GovernedExecutorError,
    invoke_governed_operation,
    prepare_governed_operation,
)
from .telemetry import ReceiptError, collect_governed_receipt
from .workspace import WorkspaceError, inspect_project


class OperationLifecycleError(RuntimeError):
    """The lifecycle stopped at its first broken governed seam."""


OperationGuidanceV1 = Mapping[str, Any]


def _attribute(value: object, name: str, default: object = None) -> object:
    try:
        return object.__getattribute__(value, name)
    except AttributeError:
        return default


@dataclass(frozen=True, slots=True)
class GovernedLifecycleResultV1:
    """Detached result of one lifecycle call, with no authority fields."""

    disposition: str
    attempt_id: str
    first_broken_seam: str | None = None
    reason_code: str | None = None
    guidance: OperationGuidanceV1 | None = None
    envelope: GovernedExecutionEnvelopeV1 | None = None
    execution: GovernedExecutionResultV1 | None = None
    receipt: dict[str, Any] | None = None
    observed_result: ObservedResultV1 | None = None
    technical_evaluation: Any = None
    terminal_attempt: Any = None
    downstream: dict[str, Any] | None = None

    @property
    def completed(self) -> bool:
        return self.disposition == "COMPLETED_WITH_FACTS"

    def to_mapping(self) -> dict[str, Any]:
        def detached(value: object) -> object:
            if value is None:
                return None
            method = _attribute(value, "to_mapping")
            if callable(method):
                return method()
            if isinstance(value, Mapping):
                return dict(value)
            return value

        return {
            "disposition": self.disposition,
            "attempt_id": self.attempt_id,
            "first_broken_seam": self.first_broken_seam,
            "reason_code": self.reason_code,
            "guidance": detached(self.guidance),
            "envelope": detached(self.envelope),
            "execution": detached(self.execution),
            "receipt": dict(self.receipt) if self.receipt is not None else None,
            "observed_result": detached(self.observed_result),
            "technical_evaluation": detached(self.technical_evaluation),
            "terminal_attempt": detached(self.terminal_attempt),
            "downstream": dict(self.downstream) if self.downstream is not None else None,
        }


def _stopped(
    attempt_id: str,
    seam: str,
    reason: str,
    *,
    guidance: OperationGuidanceV1 | None = None,
    envelope: GovernedExecutionEnvelopeV1 | None = None,
    execution: GovernedExecutionResultV1 | None = None,
    receipt: dict[str, Any] | None = None,
) -> GovernedLifecycleResultV1:
    return GovernedLifecycleResultV1(
        disposition="STOPPED_FAIL_CLOSED",
        attempt_id=attempt_id,
        first_broken_seam=seam,
        reason_code=reason,
        guidance=guidance,
        envelope=envelope,
        execution=execution,
        receipt=receipt,
    )


def _typed_completion(value: object) -> GovernedExecutionCompletionV1 | None:
    if isinstance(value, GovernedExecutionCompletionV1):
        source = {name: object.__getattribute__(value, name) for name in GovernedExecutionCompletionV1.__dataclass_fields__}
    elif isinstance(value, Mapping):
        source = dict(value)
    else:
        return None
    try:
        source["acceptance_contract"] = _acceptance_contract(source.get("acceptance_contract"))
        source["verifier_contracts"] = tuple(
            _verifier_contract(item) for item in source.get("verifier_contracts", ())
        )
        source["verifier_evidence"] = tuple(
            _verifier_evidence(item) for item in source.get("verifier_evidence", ())
        )
        source["findings"] = tuple(_finding(item) for item in source.get("findings", ()))
        source["supersession"] = tuple(_supersession(item) for item in source.get("supersession", ()))
        fields = {field.name for field in GovernedExecutionCompletionV1.__dataclass_fields__.values()}
        return GovernedExecutionCompletionV1(**{key: source[key] for key in fields if key in source})
    except (TypeError, ValueError, GovernedExecutorError):
        return None


def _identity_ref(value: object) -> IdentityRefV1:
    if isinstance(value, IdentityRefV1):
        return value
    if isinstance(value, Mapping):
        return IdentityRefV1(ref=value.get("ref"), identity=value.get("identity"))
    raise ValueError("identity reference is invalid")


def _candidate(value: object) -> CandidateIdentityV1:
    if isinstance(value, CandidateIdentityV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("candidate identity is invalid")
    dirty: list[DirtyPathEntryV1] = []
    for item in value.get("dirty_manifest", ()):
        if isinstance(item, DirtyPathEntryV1):
            dirty.append(item)
            continue
        if not isinstance(item, Mapping):
            raise ValueError("dirty candidate entry is invalid")
        identity = item.get("content_identity", {})
        if not isinstance(identity, Mapping):
            raise ValueError("dirty candidate identity is invalid")
        dirty.append(
            DirtyPathEntryV1(
                path=item.get("path"),
                change_kind=item.get("change_kind"),
                before=identity.get("before"),
                after=identity.get("after"),
                source_path=item.get("source_path"),
            )
        )
    return CandidateIdentityV1(kind=value.get("kind"), head=value.get("head"), dirty_manifest=tuple(dirty))


def _verifier_contract(value: object) -> VerifierContractV1:
    if isinstance(value, VerifierContractV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("verifier contract is invalid")
    return VerifierContractV1(
        acceptance_contract_ref=value.get("acceptance_contract_ref"),
        contract_id=value.get("contract_id"),
        contract_version_or_ref=value.get("contract_version_or_ref"),
        required=value.get("required"),
        evidence_class=value.get("evidence_class"),
        predicate=value.get("predicate"),
        required_evidence_refs=tuple(value.get("required_evidence_refs", ())),
        failure_semantics=value.get("failure_semantics"),
    )


def _acceptance_contract(value: object) -> AcceptanceContractV1 | None:
    if value is None or isinstance(value, AcceptanceContractV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("acceptance contract is invalid")
    return AcceptanceContractV1(
        value.get("acceptance_contract_ref"),
        tuple(_verifier_contract(item) for item in value.get("verifier_contracts", ())),
    )


def _evidence_applicability(value: object) -> EvidenceApplicabilityV1:
    if isinstance(value, EvidenceApplicabilityV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("evidence applicability is invalid")
    return EvidenceApplicabilityV1(
        attempt_id=value.get("attempt_id"),
        candidate_identity=_candidate(value.get("candidate_identity")),
        acceptance_contract_ref=value.get("acceptance_contract_ref"),
        verifier_contract_ref=value.get("verifier_contract_ref"),
        verifier_contract_version_or_ref=value.get("verifier_contract_version_or_ref"),
        evaluation_scope_ref=value.get("evaluation_scope_ref"),
        finding_refs=tuple(value.get("finding_refs", ())),
        input_baseline_refs=tuple(_identity_ref(item) for item in value.get("input_baseline_refs", ())),
    )


def _verifier_evidence(value: object) -> VerifierEvidenceV1:
    if isinstance(value, VerifierEvidenceV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("verifier evidence is invalid")
    return VerifierEvidenceV1(
        evidence_id=value.get("evidence_id"),
        attempt_id=value.get("attempt_id"),
        candidate_identity=_candidate(value.get("candidate_identity")),
        verifier_contract_ref=value.get("verifier_contract_ref"),
        verifier_contract_version_or_ref=value.get("verifier_contract_version_or_ref"),
        outcome=value.get("outcome"),
        evidence_refs=tuple(value.get("evidence_refs", ())),
        applicability=_evidence_applicability(value.get("applicability")),
        claim_refs=tuple(value.get("claim_refs", ())),
    )


def _finding(value: object) -> FindingV1:
    if isinstance(value, FindingV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("finding is invalid")
    raw_applicability = value.get("applicability")
    applicability = raw_applicability
    if isinstance(raw_applicability, Mapping):
        applicability = FindingApplicabilityV1(
            attempt_id=raw_applicability.get("attempt_id"),
            candidate_identity=_candidate(raw_applicability.get("candidate_identity")),
            acceptance_contract_ref=raw_applicability.get("acceptance_contract_ref"),
            evaluation_scope_ref=raw_applicability.get("evaluation_scope_ref"),
            input_baseline_refs=tuple(_identity_ref(item) for item in raw_applicability.get("input_baseline_refs", ())),
        )
    return FindingV1(
        finding_id=value.get("finding_id"),
        statement=value.get("statement"),
        severity=value.get("severity"),
        responsibility_domains=tuple(value.get("responsibility_domains", ())),
        acceptance_impact=value.get("acceptance_impact"),
        disposition=value.get("disposition"),
        evidence_refs=tuple(value.get("evidence_refs", ())),
        owner_adjudication_ref=value.get("owner_adjudication_ref"),
        applicability=applicability,
    )


def _supersession(value: object) -> EvidenceSupersessionV1:
    if isinstance(value, EvidenceSupersessionV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("supersession is invalid")
    return EvidenceSupersessionV1(
        prior_evidence_ref=value.get("prior_evidence_ref"),
        successor_evidence_ref=value.get("successor_evidence_ref"),
        current_acceptance_scope_ref=value.get("current_acceptance_scope_ref"),
        rechecked_claim_refs=tuple(value.get("rechecked_claim_refs", ())),
        reason=value.get("reason"),
    )


def _evaluation_carriers_valid(completion: GovernedExecutionCompletionV1) -> bool:
    """Check the live typed carrier boundary before irreversible terminalization."""

    return (
        isinstance(completion.acceptance_contract, AcceptanceContractV1)
        and isinstance(completion.evaluation_scope_ref, str)
        and bool(completion.evaluation_scope_ref)
        and all(isinstance(item, VerifierContractV1) for item in completion.verifier_contracts)
        and all(isinstance(item, VerifierEvidenceV1) for item in completion.verifier_evidence)
        and all(isinstance(item, FindingV1) for item in completion.findings)
        and all(isinstance(item, EvidenceSupersessionV1) for item in completion.supersession)
    )


def _receipt_context(
    target: Path,
    *,
    registered_project_id: str | None,
    receipt_path: str | Path | None,
    home: str | Path | None,
) -> tuple[str, Path, bool]:
    if registered_project_id is not None and receipt_path is not None:
        return registered_project_id, Path(receipt_path).expanduser().resolve(), True
    info = inspect_project(target, home=home)
    entry = info.get("entry", info)
    project_id = registered_project_id or entry.get("project_id")
    telemetry = entry.get("telemetry") if isinstance(entry, Mapping) else None
    path = receipt_path or (telemetry.get("receipt_path") if isinstance(telemetry, Mapping) else None)
    enabled = bool(telemetry.get("enabled")) if isinstance(telemetry, Mapping) else False
    if not isinstance(project_id, str) or not project_id or path is None:
        raise WorkspaceError("registered telemetry receipt context is unavailable")
    return project_id, Path(path).expanduser().resolve(), enabled


def execute_governed_operation(
    target: str | Path,
    attempt_id: str,
    *,
    guidance: OperationGuidanceV1 | Mapping[str, Any] | None = None,
    bounded_payload: object = None,
    completion: GovernedExecutionCompletionV1 | Mapping[str, Any] | None = None,
    receipt: Mapping[str, Any] | None = None,
    receipt_path: str | Path | None = None,
    registered_project_id: str | None = None,
    home: str | Path | None = None,
    telemetry_enabled: bool | None = None,
    payload_schema_ref: str = "payload.v1",
    authority_refs: Sequence[str] | None = None,
    guidance_ref: str | None = None,
) -> GovernedLifecycleResultV1:
    """Run the exact lookup→claim→execute→receipt→terminal→PL08 order."""

    root = Path(target).expanduser().resolve()
    lookup = lookup_attempt(root, attempt_id)
    if lookup.outcome is not LookupOutcome.FOUND or lookup.attempt is None:
        return _stopped(attempt_id, "AUTHORITATIVE_ATTEMPT_LOOKUP", lookup.outcome.value)
    admissibility = check_activation_admissibility(root, attempt_id)
    if admissibility.outcome is not AdmissibilityOutcome.ADMISSIBLE:
        return _stopped(attempt_id, "ATTEMPT_ADMISSIBILITY", admissibility.outcome.value)
    try:
        claimed = claim_attempt(root, attempt_id)
    except AttemptRuntimeError as exc:
        return _stopped(attempt_id, "ATTEMPT_CLAIM", type(exc).__name__)
    attempt = claimed.attempt

    selected_guidance: OperationGuidanceV1 | None
    if guidance is None:
        return _stopped(attempt_id, "OPERATION_GUIDANCE", "GUIDANCE_REQUIRED")
    selected_guidance = guidance  # exact supplied PL07 projection; no reselection
    if not isinstance(selected_guidance, Mapping) or selected_guidance.get("outcome") != "MATCHED":
        return _stopped(attempt_id, "OPERATION_GUIDANCE", "GUIDANCE_NOT_MATCHED")

    execution = invoke_governed_operation(
        attempt,
        selected_guidance,
        bounded_payload,
        completion,
        payload_schema_ref,
        authority_refs,
        guidance_ref,
    )
    envelope: GovernedExecutionEnvelopeV1 | None = None
    if execution.envelope_digest is not None:
        try:
            envelope = prepare_governed_operation(
                attempt,
                selected_guidance,
                bounded_payload,
                payload_schema_ref,
                authority_refs,
                guidance_ref,
            )
        except GovernedExecutorError:
            envelope = None
    if not execution.accepted or execution.completion is None:
        return _stopped(
            attempt_id,
            "GOVERNED_EXECUTOR_COMPLETION",
            execution.failure_category or "EXECUTION_REJECTED",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    typed = _typed_completion(execution.completion)
    if typed is None or not _evaluation_carriers_valid(typed):
        return _stopped(
            attempt_id,
            "TYPED_EVALUATION_CARRIERS",
            "INVALID_CONTRACT_OR_FIXTURE",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    if receipt is None:
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_COLLECTION",
            "RECEIPT_MISSING",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    if receipt.get("receipt_id") != typed.receipt_id if typed.receipt_id is not None else False:
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_IDENTITY",
            "RECEIPT_ID_MISMATCH",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    try:
        project_id, path, registered_enabled = _receipt_context(
            root,
            registered_project_id=registered_project_id,
            receipt_path=receipt_path,
            home=home,
        )
        enabled = registered_enabled if telemetry_enabled is None else telemetry_enabled
        persisted = collect_governed_receipt(
            receipt,
            project_root=root,
            receipt_path=path,
            registered_project_id=project_id,
            attempt_id=attempt.attempt_id,
            execution_invocation_id=execution.execution_invocation_id or "",
            enabled=enabled,
        )
    except (ReceiptError, WorkspaceError, OSError, ValueError) as exc:
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_COLLECTION",
            type(exc).__name__,
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    if (
        persisted.get("schema_version") != 2
        or persisted.get("receipt_id") != receipt.get("receipt_id")
        or persisted.get("attempt_id") != attempt.attempt_id
        or persisted.get("execution_invocation_id") != execution.execution_invocation_id
        or typed.receipt_id is not None and persisted.get("receipt_id") != typed.receipt_id
    ):
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_IDENTITY",
            "IDENTITY_TRIANGLE_MISMATCH",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
            receipt=persisted,
        )

    observed = ObservedResultV1(
        result_id=typed.result_id,
        attempt_id=attempt.attempt_id,
        execution_status=typed.execution_status,
        changed_paths=typed.changed_paths,
        fact_refs=typed.fact_refs,
        artifact_refs=typed.artifact_refs,
    )
    try:
        terminal = terminalize_attempt(root, attempt.attempt_id, observed)
    except AttemptRuntimeError as exc:
        return _stopped(
            attempt_id,
            "ATTEMPT_TERMINALIZATION",
            type(exc).__name__,
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
            receipt=persisted,
        )
    technical = evaluate_technical(
        attempt=attempt,
        contracts=typed.verifier_contracts,
        evidence=typed.verifier_evidence,
        findings=typed.findings,
        acceptance_contract_ref=attempt.acceptance_contract_ref,
        evaluation_scope_ref=typed.evaluation_scope_ref,
        acceptance_contract=typed.acceptance_contract,
        supersession=typed.supersession,
        evaluation_id=typed.evaluation_id,
        evaluation_run=typed.evaluation_run,
        candidate_quality=typed.candidate_quality,
    )
    return GovernedLifecycleResultV1(
        disposition="COMPLETED_WITH_FACTS",
        attempt_id=attempt.attempt_id,
        guidance=selected_guidance,
        envelope=envelope,
        execution=execution,
        receipt=dict(persisted),
        observed_result=observed,
        technical_evaluation=technical,
        terminal_attempt=terminal,
        downstream={"status_projection": "AVAILABLE"},
    )


run_governed_operation = execute_governed_operation
execute_operation_lifecycle = execute_governed_operation


__all__ = [
    "GovernedLifecycleResultV1",
    "OperationLifecycleError",
    "execute_governed_operation",
    "execute_operation_lifecycle",
    "run_governed_operation",
]
