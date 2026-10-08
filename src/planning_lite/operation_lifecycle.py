"""Pattern-B coordinator for one bounded governed operation.

The lifecycle owns ordering only.  Attempt Runtime owns occurrence/state,
Telemetry owns receipt validation/storage/readback, and PL08 owns evaluation.
There is no lifecycle store, queue, worker, retry, callback, or next-gate
authority here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile
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
from .context import OperationDepthObservationV1, build_compact_status
from .attempt_runtime import (
    AdmissibilityOutcome,
    AttemptEnvelopeV2,
    AttemptRecordV2,
    AttemptRuntimeError,
    LookupOutcome,
    attempt_store_v2_path,
    check_activation_admissibility,
    claim_attempt,
    lookup_attempt,
    publish_dependency_acceptance_proof,
    terminalize_attempt,
)
from .governed_executor import (
    EvidenceContentInputV1,
    GovernedExecutionCompletionV1,
    GovernedExecutionDependencyInputV1,
    GovernedExecutionEnvelopeV1,
    GovernedExecutionResultV1,
    GovernedExecutorError,
    invoke_governed_operation,
    prepare_governed_operation,
)
from .project_spine import (
    PostEvaluationCheckpointV1,
    ProjectSpineHandoffError,
    ProjectSpineSnapshotV1,
    capture_project_spine_snapshot,
    record_post_evaluation_checkpoint,
)
from .operation_trace import (
    OperationTraceError,
    OperationTraceView,
    read_operation_trace_evidence,
    record_governed_attempt_evidence,
)
from .telemetry import ReceiptError, collect_governed_receipt
from .workspace import (
    WorkspaceError,
    inspect_project,
    publish_governed_artifact_output,
    resolve_dependency_artifact_output_route,
)


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
    observed_result: ObservedResultV1 | None = None,
    technical_evaluation: Any = None,
    terminal_attempt: Any = None,
    downstream: dict[str, Any] | None = None,
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
        observed_result=observed_result,
        technical_evaluation=technical_evaluation,
        terminal_attempt=terminal_attempt,
        downstream=downstream,
    )


def _typed_completion(value: object) -> GovernedExecutionCompletionV1 | None:
    if isinstance(value, GovernedExecutionCompletionV1):
        source = {name: object.__getattribute__(value, name) for name in GovernedExecutionCompletionV1.__dataclass_fields__}
    elif isinstance(value, Mapping):
        source = dict(value)
    else:
        return None
    try:
        evidence_inputs: list[EvidenceContentInputV1] = []
        raw_evidence_inputs = source.get("evidence_content_inputs", ())
        if not isinstance(raw_evidence_inputs, (tuple, list)):
            return None
        for item in raw_evidence_inputs:
            if type(item) is EvidenceContentInputV1:
                evidence_inputs.append(item)
            elif isinstance(item, Mapping) and set(item) == {"evidence_ref", "exact_raw_bytes"}:
                evidence_inputs.append(EvidenceContentInputV1(item["evidence_ref"], item["exact_raw_bytes"]))
            else:
                return None
        source["evidence_content_inputs"] = tuple(evidence_inputs)
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


def _is_dependent_endpoint(attempt: object, task_id: str) -> bool:
    binding = _attribute(attempt, "preparation_binding")
    return (
        _attribute(attempt, "task_or_operation_id") == task_id
        and _attribute(binding, "dependency_classification") == "DEPENDENCY_EDGE_MEMBER"
    )


def _source_attempt_evaluation_input(attempt: object, completion: GovernedExecutionCompletionV1) -> dict[str, Any]:
    """Derive the exact PL08 input snapshot from the claimed source Attempt and call."""
    candidate = _attribute(attempt, "candidate_identity")
    baselines = _attribute(attempt, "baseline_refs")
    verifier_refs = _attribute(attempt, "verifier_contract_refs")
    if not callable(_attribute(candidate, "to_mapping")) or not isinstance(baselines, (tuple, list)):
        raise ValueError("source Attempt lacks its complete PL08 identity inputs")
    if not isinstance(verifier_refs, (tuple, list)):
        raise ValueError("source Attempt lacks its verifier identity inputs")
    normalized_refs: list[dict[str, str]] = []
    for item in verifier_refs:
        if isinstance(item, Mapping):
            contract_id = item.get("contract_id")
            contract_version = item.get("contract_version_or_ref")
        elif isinstance(item, (tuple, list)) and len(item) == 2:
            contract_id, contract_version = item
        else:
            contract_id = _attribute(item, "contract_id")
            contract_version = _attribute(item, "contract_version_or_ref")
        if not isinstance(contract_id, str) or not isinstance(contract_version, str):
            raise ValueError("source verifier identity is malformed")
        normalized_refs.append(
            {"contract_id": contract_id, "contract_version_or_ref": contract_version}
        )
    return {
        "attempt_id": _attribute(attempt, "attempt_id"),
        "candidate_identity": candidate.to_mapping(),
        "baseline_refs": [value.to_mapping() for value in baselines],
        "acceptance_contract_ref": _attribute(attempt, "acceptance_contract_ref"),
        "verifier_contract_refs": normalized_refs,
        "evaluation_id": completion.evaluation_id,
        "evaluation_scope_ref": completion.evaluation_scope_ref,
        "evaluation_run": completion.evaluation_run,
        "candidate_quality": completion.candidate_quality,
    }


def _required_class_b_evidence_refs(
    completion: GovernedExecutionCompletionV1,
) -> frozenset[str]:
    """Derive exact Class-B refs using the proof owner's Class-A overlap rule.

    Verifier/Finding external refs are Class B even when they also occur in a
    captured verifier mapping. Supersession endpoints are Class A only when
    their exact ref is a captured VerifierEvidence ID; all other endpoints
    require durable external content. Class-A-only values need no byte input.
    """
    evidence_ids = {item.evidence_id for item in completion.verifier_evidence}
    class_b_refs = {
        ref for item in completion.verifier_evidence for ref in item.evidence_refs
    } | {ref for item in completion.findings for ref in item.evidence_refs}
    for item in completion.supersession:
        for ref in (item.prior_evidence_ref, item.successor_evidence_ref):
            if ref not in evidence_ids:
                class_b_refs.add(ref)
    return frozenset(class_b_refs)


def _exact_class_b_inputs(
    completion: GovernedExecutionCompletionV1,
) -> dict[str, EvidenceContentInputV1]:
    """Require exactly one transient input per actual Class-B ref occurrence set."""
    required_refs = _required_class_b_evidence_refs(completion)
    by_ref: dict[str, EvidenceContentInputV1] = {}
    for evidence_input in completion.evidence_content_inputs:
        if type(evidence_input) is not EvidenceContentInputV1:
            raise ValueError("completion contains a non-exact EvidenceContentInputV1")
        if evidence_input.evidence_ref in by_ref:
            raise ValueError("completion contains duplicate Class-B evidence inputs")
        by_ref[evidence_input.evidence_ref] = evidence_input
    if set(by_ref) != required_refs:
        raise ValueError("completion Class-B evidence inputs are missing or unrelated")
    return by_ref


def _publish_satisfied_source_outputs(
    target: Path,
    attempt: object,
    observed: ObservedResultV1,
    completion: GovernedExecutionCompletionV1,
    technical: Any,
) -> dict[str, Any]:
    """Publish only identity-joined T-01 completion bytes after PL08 SATISFIED.

    Lifecycle is the sole producer-provenance integration owner: the typed
    completion has already joined the invocation envelope, and this boundary
    then requires exact T-01/A1, SATISFIED PL08, its governed artifact ref and
    exactly one Class-B byte input per invocation-associated external ref.
    Workspace publishes artifact bytes first; dependency_admission publishes
    the same call's Class-B bytes; only their verified rereads feed proof
    capture and Runtime's locked CURRENT/Trigger A transition. Failure never
    republishes, reruns the producer, or bypasses either owner.
    """
    from .dependency_admission import (
        capture_dependency_acceptance_proof,
        publish_evidence_content,
        resolve_dependency,
    )

    if not isinstance(attempt, AttemptRecordV2):
        raise ValueError("T-07 producer publication requires exact V2 T-01/A1")
    if (
        attempt.attempt_id != f"{attempt.change_id}/T-01/A1"
        or attempt.task_or_operation_id != "T-01"
        or not _is_dependent_endpoint(attempt, "T-01")
        or technical.outcome != "SATISFIED"
    ):
        raise ValueError("T-07 producer publication requires satisfied dependent T-01/A1")
    requirement_resolution = resolve_dependency(target, "T-01")
    requirement = requirement_resolution.requirement
    artifact_ref = requirement.get("produced_artifact_logical_ref")
    if (
        requirement_resolution.change_id != attempt.change_id
        or requirement.get("source_attempt_id") != attempt.attempt_id
        or not isinstance(artifact_ref, str)
        or artifact_ref not in observed.artifact_refs
        or type(completion.artifact_output_bytes) is not bytes
    ):
        raise ValueError("actual completion bytes do not join the current source artifact requirement")

    # Match the proof owner's exact Class-A/Class-B classification. A verifier
    # or Finding external evidence ref is always Class B; supersession endpoints
    # without a captured VerifierEvidence ID are Class B as well.
    by_ref = _exact_class_b_inputs(completion)
    class_b_refs = _required_class_b_evidence_refs(completion)

    artifact_digest = publish_governed_artifact_output(target, completion.artifact_output_bytes)
    for evidence_ref in sorted(class_b_refs):
        published = publish_evidence_content(
            target, evidence_ref, by_ref[evidence_ref].exact_raw_bytes
        )
        if (
            published.evidence_ref != evidence_ref
            or published.content_digest != hashlib.sha256(by_ref[evidence_ref].exact_raw_bytes).hexdigest()
        ):
            raise ValueError("published Class-B evidence failed exact digest/ref readback")

    evaluation_input = _source_attempt_evaluation_input(attempt, completion)
    proof = capture_dependency_acceptance_proof(
        target,
        observed_result=observed,
        attempt_evaluation_input=evaluation_input,
        acceptance_contract=completion.acceptance_contract,
        verifier_evidence_inputs=completion.verifier_evidence,
        evidence_supersession_inputs=completion.supersession,
        finding_inputs=completion.findings,
        technical_evaluation=technical,
    )
    proof_mapping = proof.to_mapping()
    if proof_mapping["artifact_digest"] != artifact_digest or proof_mapping["artifact_logical_ref"] != artifact_ref:
        raise ValueError("captured proof does not join the exact published producer bytes")
    transition = publish_dependency_acceptance_proof(target, proof)
    return {
        "artifact_digest": artifact_digest,
        "artifact_logical_ref": artifact_ref,
        "evidence_content_refs": sorted(class_b_refs),
        "proof_id": proof.proof_id,
        "proof_digest": proof.proof_digest,
        "trigger_a": transition.to_mapping(),
    }


def _read_current_artifact_bytes(route: Any) -> bytes:
    """Read one freshly derived regular artifact route and reject target swaps."""
    info = route.path.lstat()
    if stat.S_ISLNK(info.st_mode) or not stat.S_ISREG(info.st_mode):
        raise ValueError("canonical artifact target is missing, symlinked, or non-regular")
    raw = route.path.read_bytes()
    after = route.path.lstat()
    if (
        stat.S_ISLNK(after.st_mode)
        or not stat.S_ISREG(after.st_mode)
        or (info.st_dev, info.st_ino) != (after.st_dev, after.st_ino)
    ):
        raise ValueError("canonical artifact target changed during exact read")
    return raw


def _fresh_successor_dependency_input(
    target: Path, claimed: AttemptEnvelopeV2
) -> GovernedExecutionDependencyInputV1:
    """Rejoin CURRENT proof, immutable admission and fresh exact route after D11.

    This is the one post-claim byte boundary. It consumes no caller-provided
    ref, path, digest, or bytes; any failed current join stops before executor,
    receipt, terminalization, or PL08 and leaves the successful claim IN_FLIGHT
    without rollback, revocation, or producer rerun.
    """
    from .dependency_admission import (
        DependencyAcceptanceProofV1,
        resolve_dependency,
        resolve_dependency_acceptance_proof_blob,
        validate_dependency_admission,
    )

    if (
        type(claimed) is not AttemptEnvelopeV2
        or claimed.runtime_state != "IN_FLIGHT"
        or not _is_dependent_endpoint(claimed.attempt, "T-02")
    ):
        raise ValueError("successor dependency input requires the exact successful T-02 claim")
    fresh_lookup = lookup_attempt(target, claimed.attempt_id)
    fresh_envelope = fresh_lookup.envelope
    if (
        fresh_lookup.outcome is not LookupOutcome.FOUND
        or type(fresh_envelope) is not AttemptEnvelopeV2
        or fresh_envelope.runtime_state != "IN_FLIGHT"
        or fresh_envelope.attempt != claimed.attempt
    ):
        raise ValueError("T-02 claim changed before successor input resolution")
    successor = fresh_envelope
    source_id = f"{successor.attempt.change_id}/T-01/A1"
    source_lookup = lookup_attempt(target, source_id)
    source_envelope = source_lookup.envelope
    if (
        source_lookup.outcome is not LookupOutcome.FOUND
        or type(source_envelope) is not AttemptEnvelopeV2
        or source_envelope.runtime_state != "TERMINAL"
        or source_envelope.attempt.task_or_operation_id != "T-01"
    ):
        raise ValueError("exact terminal T-01/A1 source is missing after T-02 claim")
    control = source_envelope.dependency_edge_control
    if not isinstance(control, Mapping):
        raise ValueError("T-01/A1 has no CURRENT dependency proof control")
    head = control.get("proof_head")
    if not isinstance(head, Mapping) or head.get("state") != "CURRENT":
        raise ValueError("T-01/A1 proof head is not CURRENT")

    resolution = resolve_dependency(target, "T-02")
    requirement = resolution.requirement
    binding = successor.attempt.preparation_binding
    if (
        resolution.change_id != successor.attempt.change_id
        or requirement.get("source_attempt_id") != source_id
        or requirement.get("successor_attempt_id") != successor.attempt_id
        or binding.requirement_id != requirement.get("requirement_id")
        or binding.dependency_semantic_digest != requirement.get("dependency_semantic_digest")
    ):
        raise ValueError("current T-02 requirement does not join its immutable Preparation binding")

    proof_id = head.get("proof_id")
    proof_digest = head.get("proof_digest")
    if not isinstance(proof_id, str) or not isinstance(proof_digest, str):
        raise ValueError("CURRENT proof head identity is malformed")
    proof = resolve_dependency_acceptance_proof_blob(
        attempt_store_v2_path(target).parent, proof_id
    )
    if proof is None or proof.proof_digest != proof_digest:
        raise ValueError("CURRENT proof blob is missing or differs from its locked head")
    proof = DependencyAcceptanceProofV1.from_mapping(
        proof.to_mapping(), current_requirement=requirement
    )

    route = resolve_dependency_artifact_output_route(target)
    if (
        route.key.change_id != successor.attempt.change_id
        or route.key.source_attempt_id != source_id
        or route.key.requirement_id != requirement.get("requirement_id")
        or route.key.dependency_semantic_digest != requirement.get("dependency_semantic_digest")
        or route.key.artifact_logical_ref != requirement.get("produced_artifact_logical_ref")
    ):
        raise ValueError("fresh Workspace route does not join the current requirement")
    raw = _read_current_artifact_bytes(route)
    artifact_digest = hashlib.sha256(raw).hexdigest()
    admission = successor.attempt.dependency_admission
    if admission is None:
        raise ValueError("complete immutable DependencyAdmissionV2 is missing")
    validate_dependency_admission(
        admission, proof, requirement, artifact_digest=artifact_digest
    )
    required_input_ref = requirement.get("required_successor_input_logical_ref")
    if (
        not isinstance(required_input_ref, str)
        or not required_input_ref
        or admission.get("required_successor_input_logical_ref") != required_input_ref
        or admission.get("artifact_logical_ref") != route.key.artifact_logical_ref
        or admission.get("artifact_digest") != artifact_digest
    ):
        raise ValueError("immutable admission does not transfer the exact current artifact bytes")
    current_route = resolve_dependency_artifact_output_route(target)
    current_requirement = resolve_dependency(target, "T-02").requirement
    if (
        current_route.key != route.key
        or current_route.path != route.path
        or current_requirement != requirement
        or _read_current_artifact_bytes(current_route) != raw
    ):
        raise ValueError("requirement, Workspace route, or raw artifact bytes changed during successor join")
    return GovernedExecutionDependencyInputV1(required_input_ref, raw)


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


class _TracePersistenceError(RuntimeError):
    """A non-authoritative progress trace transport failure."""


_TRACE_OWNER_HEADING = "## Governed Attempt / Evaluation evidence"
_TRACE_CONTAINER_BEGIN = "<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->"
_TRACE_CONTAINER_END = "<!-- PL_OPERATION_TRACE_ENTRIES_END -->"
_TRACE_ENTRY_BEGIN = "<!-- PL_OPERATION_TRACE_ENTRY_BEGIN -->"
_TRACE_ENTRY_END = "<!-- PL_OPERATION_TRACE_ENTRY_END -->"
_TRACE_OWNER_RE = re.compile(r"(?m)^## Governed Attempt / Evaluation evidence[ \t]*(?:\r?\n|\Z)")
_TRACE_H2_RE = re.compile(r"(?m)^##(?!#)[ \t]+")
_TRACE_ENTRY_FIELDS = {
    "operation_guidance_ref",
    "expected_route_operation_id",
    "expected_route_operation_class",
    "expected_route_id",
    "expected_route_outcome",
    "expected_route_reason_code",
    "expected_route_source_revision",
    "expected_route_authority_refs",
    "expected_route_selection_reason",
    "during_operation_ref",
    "during_completeness",
    "during_expansion_count",
    "actual_executor_receipt_ref",
    "actual_executor_receipt_id",
    "actual_executor_planning_lite_ref",
    "next_" + "gate_ref",
    "next_" + "gate_source_ref",
    "next_" + "gate_source_sha256",
}


@dataclass(frozen=True, slots=True)
class _PreTraceHandle:
    path: Path
    raw_sha256: str
    attempt_id: str


def _trace_newline(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    if "\n" in text:
        return "\n"
    return "\n"


def _trace_progress_path(target_root: str | Path) -> Path:
    root = Path(target_root).expanduser().resolve()
    snapshot = capture_project_spine_snapshot(root)
    context_ref = snapshot.active_context_path.replace("\\", "/")
    expected = (".planning", "changes", "active", snapshot.active_change, "context.md")
    if tuple(context_ref.split("/")) != expected:
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD")
    context_path = root.joinpath(*expected)
    if not context_path.is_file():
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD")
    try:
        context_path.resolve().relative_to(root)
    except ValueError as exc:
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD") from exc
    progress_path = context_path.with_name("progress.md").resolve()
    try:
        progress_path.relative_to(root)
    except ValueError as exc:
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD") from exc
    if not progress_path.is_file():
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD")
    return progress_path


def _trace_owner_span(text: str) -> tuple[int, int]:
    owners = list(_TRACE_OWNER_RE.finditer(text))
    if len(owners) != 1:
        raise _TracePersistenceError("INVALID_TRACE_OWNER_SECTION")
    owner = owners[0]
    next_heading = _TRACE_H2_RE.search(text, owner.end())
    return owner.start(), next_heading.start() if next_heading is not None else len(text)


def _trace_initialize_container(text: str, section_end: int) -> str:
    section = text[:section_end]
    if section.count(_TRACE_CONTAINER_BEGIN) or section.count(_TRACE_CONTAINER_END):
        return text
    newline = _trace_newline(section)
    insertion = f"{_TRACE_CONTAINER_BEGIN}{newline}{_TRACE_CONTAINER_END}"
    if not section.endswith(("\r\n", "\n")):
        insertion = newline + insertion
    insertion += newline
    return text[:section_end] + insertion + text[section_end:]


def _trace_container_span(text: str) -> tuple[int, int, int, int]:
    section_start, section_end = _trace_owner_span(text)
    section = text[section_start:section_end]
    begins = [match.start() + section_start for match in re.finditer(re.escape(_TRACE_CONTAINER_BEGIN), section)]
    ends = [match.start() + section_start for match in re.finditer(re.escape(_TRACE_CONTAINER_END), section)]
    if len(begins) != 1 or len(ends) != 1 or begins[0] > ends[0]:
        raise _TracePersistenceError("MALFORMED_TRACE_CONTAINER")
    container_begin_end = begins[0] + len(_TRACE_CONTAINER_BEGIN)
    if _TRACE_CONTAINER_BEGIN in text[container_begin_end:ends[0]] or _TRACE_CONTAINER_END in text[container_begin_end:ends[0]]:
        raise _TracePersistenceError("MALFORMED_TRACE_CONTAINER")
    for marker in (_TRACE_ENTRY_BEGIN, _TRACE_ENTRY_END):
        if marker in text[section_start:begins[0]] or marker in text[ends[0] + len(_TRACE_CONTAINER_END):section_end]:
            raise _TracePersistenceError("MALFORMED_TRACE_MARKERS")
    return begins[0], container_begin_end, ends[0], ends[0] + len(_TRACE_CONTAINER_END)


def _trace_entries(text: str) -> list[tuple[int, int, dict[str, Any]]]:
    begin, begin_end, end, _ = _trace_container_span(text)
    content = text[begin_end:end]
    markers = list(re.finditer(re.escape(_TRACE_ENTRY_BEGIN) + "|" + re.escape(_TRACE_ENTRY_END), content))
    if len(markers) % 2:
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY_MARKERS")
    entries: list[tuple[int, int, dict[str, Any]]] = []
    for index in range(0, len(markers), 2):
        opening, closing = markers[index], markers[index + 1]
        if opening.group(0) != _TRACE_ENTRY_BEGIN or closing.group(0) != _TRACE_ENTRY_END:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY_MARKERS")
        raw_start = begin_end + opening.start()
        raw_end = begin_end + closing.end()
        body = content[opening.end():closing.start()]
        entry = _trace_parse_entry(body)
        entries.append((raw_start, raw_end, entry))
    attempt_ids = [entry.get("attempt_id") for _, _, entry in entries]
    if len(attempt_ids) != len(set(attempt_ids)):
        raise _TracePersistenceError("DUPLICATE_TRACE_ATTEMPT")
    return entries


def _trace_parse_entry(body: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    attempt_count = 0
    attempt_pattern = re.compile(r"^[ \t]*- Attempt ref: `([^`\r\n]+)`[ \t]*(?:\r)?$", re.MULTILINE)
    for match in attempt_pattern.finditer(body):
        attempt_count += 1
        result["attempt_id"] = match.group(1)
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("- Attempt ref:"):
            continue
        field_match = re.fullmatch(r"- ([a-z][a-z0-9_]*)[ \t]*:[ \t]*(.*)", stripped)
        if field_match is None:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
        key, raw_value = field_match.groups()
        if key not in _TRACE_ENTRY_FIELDS or key in result:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
        try:
            result[key] = json.loads(raw_value)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY") from exc
    if attempt_count != 1 or "attempt_id" not in result:
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
    return result


def _trace_format_entry(entry: Mapping[str, Any], newline: str) -> str:
    attempt_id = entry.get("attempt_id")
    if not isinstance(attempt_id, str) or not attempt_id:
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
    lines = [f"{_TRACE_ENTRY_BEGIN}", f"- Attempt ref: `{attempt_id}`"]
    order = (
        "operation_guidance_ref",
        "expected_route_operation_id",
        "expected_route_operation_class",
        "expected_route_id",
        "expected_route_outcome",
        "expected_route_reason_code",
        "expected_route_source_revision",
        "expected_route_authority_refs",
        "expected_route_selection_reason",
        "during_operation_ref",
        "during_completeness",
        "during_expansion_count",
        "actual_executor_receipt_ref",
        "actual_executor_receipt_id",
        "actual_executor_planning_lite_ref",
        "next_" + "gate_ref",
        "next_" + "gate_source_ref",
        "next_" + "gate_source_sha256",
    )
    for key in order:
        if key in entry:
            try:
                value = json.dumps(entry[key], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            except (TypeError, ValueError) as exc:
                raise _TracePersistenceError("MALFORMED_TRACE_ENTRY") from exc
            lines.append(f"- {key}: {value}")
    if set(entry) - ({"attempt_id"} | _TRACE_ENTRY_FIELDS):
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
    lines.append(_TRACE_ENTRY_END)
    return newline.join(lines)


def _trace_replace_entry(text: str, entry: Mapping[str, Any], *, existing: tuple[int, int, dict[str, Any]] | None) -> str:
    newline = _trace_newline(text)
    serialized = _trace_format_entry(entry, newline)
    if existing is not None:
        start, end, _ = existing
        return text[:start] + serialized + text[end:]
    _, _, container_end, _ = _trace_container_span(text)
    prefix = text[:container_end]
    if not prefix.endswith(("\r\n", "\n")):
        prefix += newline
    return prefix + serialized + newline + text[container_end:]


def _trace_read(path: Path, *, initialize_legacy: bool) -> tuple[bytes, str, list[tuple[int, int, dict[str, Any]]]]:
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        section_start, section_end = _trace_owner_span(text)
        section = text[section_start:section_end]
        if section.count(_TRACE_CONTAINER_BEGIN) == 0 and section.count(_TRACE_CONTAINER_END) == 0:
            if not initialize_legacy:
                raise _TracePersistenceError("MISSING_TRACE_CONTAINER")
            text = _trace_initialize_container(text, section_end)
        elif section.count(_TRACE_CONTAINER_BEGIN) != 1 or section.count(_TRACE_CONTAINER_END) != 1:
            raise _TracePersistenceError("MALFORMED_TRACE_CONTAINER")
        entries = _trace_entries(text)
        return raw, text, entries
    except _TracePersistenceError:
        raise
    except (OSError, UnicodeError) as exc:
        raise _TracePersistenceError("TRACE_PROGRESS_READ_FAILED") from exc


def _trace_atomic_replace(path: Path, raw: bytes) -> None:
    temporary: str | None = None
    try:
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    except OSError as exc:
        raise _TracePersistenceError("TRACE_PROGRESS_ATOMIC_WRITE_FAILED") from exc
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass


def _trace_persist_pre(
    target_root: str | Path,
    attempt_id: str,
    guidance: OperationGuidanceV1,
    operation_guidance_ref: str | None,
    operation_depth_observation: OperationDepthObservationV1 | None,
) -> _PreTraceHandle:
    path = _trace_progress_path(target_root)
    raw, text, entries = _trace_read(path, initialize_legacy=True)
    existing = next((item for item in entries if item[2].get("attempt_id") == attempt_id), None)
    if existing is not None:
        raise _TracePersistenceError("DUPLICATE_TRACE_ATTEMPT")
    entry = record_governed_attempt_evidence(
        "PRE",
        attempt_id,
        operation_guidance_ref=operation_guidance_ref,
        guidance=guidance,
        operation_depth_observation=operation_depth_observation,
    )
    new_text = _trace_replace_entry(text, entry, existing=None)
    new_raw = new_text.encode("utf-8")
    _trace_atomic_replace(path, new_raw)
    try:
        reread = path.read_bytes()
        _, reread_text, reread_entries = _trace_read(path, initialize_legacy=False)
    except (OSError, UnicodeError, _TracePersistenceError) as exc:
        raise _TracePersistenceError("TRACE_PROGRESS_READBACK_FAILED") from exc
    matching = [item for item in reread_entries if item[2].get("attempt_id") == attempt_id]
    if len(matching) != 1 or matching[0][2] != dict(entry):
        raise _TracePersistenceError("TRACE_PRE_READBACK_MISMATCH")
    _ = reread_text
    return _PreTraceHandle(path, hashlib.sha256(reread).hexdigest(), attempt_id)


def _trace_persist_post(
    handle: _PreTraceHandle,
    persisted_receipt: Mapping[str, Any],
    post_spine_snapshot: ProjectSpineSnapshotV1,
) -> OperationTraceView:
    current_raw = handle.path.read_bytes()
    if hashlib.sha256(current_raw).hexdigest() != handle.raw_sha256:
        raise _TracePersistenceError("STALE_PROGRESS")
    _, text, entries = _trace_read(handle.path, initialize_legacy=False)
    matching = [item for item in entries if item[2].get("attempt_id") == handle.attempt_id]
    if len(matching) != 1:
        raise _TracePersistenceError("MISSING_PRE_TRACE")
    receipt_id = persisted_receipt.get("receipt_id")
    if not isinstance(receipt_id, str) or not receipt_id:
        raise _TracePersistenceError("INCOMPLETE_EXECUTOR_RECEIPT")
    receipt_ref = f"{handle.path.as_posix()}#receipt_id={receipt_id}"
    entry = record_governed_attempt_evidence(
        "POST",
        handle.attempt_id,
        matching[0][2],
        receipt_ref=receipt_ref,
        validated_receipt=persisted_receipt,
        **{
            "next_" + "gate_ref": post_spine_snapshot.next_permitted_action,
            "next_" + "gate_source_ref": ".planning/ACTIVE.md#Active change/Next permitted action",
            "next_" + "gate_source_sha256": post_spine_snapshot.active_sha256.lower(),
        },
    )
    new_text = _trace_replace_entry(text, entry, existing=matching[0])
    _trace_atomic_replace(handle.path, new_text.encode("utf-8"))
    _, reread_text, reread_entries = _trace_read(handle.path, initialize_legacy=False)
    _ = reread_text
    final = [item[2] for item in reread_entries if item[2].get("attempt_id") == handle.attempt_id]
    if len(final) != 1 or final[0] != dict(entry):
        raise _TracePersistenceError("TRACE_POST_READBACK_MISMATCH")
    expected_ref = receipt_ref
    return read_operation_trace_evidence(
        final[0], lambda ref: dict(persisted_receipt) if ref == expected_ref else None
    )


def execute_governed_operation(
    target: str | Path,
    attempt_id: str,
    *,
    target_root: str | Path,
    pre_execution_project_spine_snapshot: ProjectSpineSnapshotV1,
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
    operation_depth_observation: OperationDepthObservationV1 | None = None,
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

    dependency_input: GovernedExecutionDependencyInputV1 | None = None
    if _is_dependent_endpoint(attempt, "T-02"):
        try:
            dependency_input = _fresh_successor_dependency_input(root, claimed)
        except Exception:
            # The D11 claim is already a durable fact. This exact existing
            # stopped result shape exposes the post-claim byte boundary while
            # leaving the Attempt IN_FLIGHT and invoking neither executor nor
            # PL08; no rollback, revocation, or producer retry follows.
            return _stopped(
                attempt_id,
                "SUCCESSOR_DEPENDENCY_INPUT",
                "DEPENDENCY_INPUT_INVALID",
            )

    selected_guidance: OperationGuidanceV1 | None
    if guidance is None:
        return _stopped(attempt_id, "OPERATION_GUIDANCE", "GUIDANCE_REQUIRED")
    selected_guidance = guidance  # exact supplied PL07 projection; no reselection
    if not isinstance(selected_guidance, Mapping) or selected_guidance.get("outcome") != "MATCHED":
        return _stopped(attempt_id, "OPERATION_GUIDANCE", "GUIDANCE_NOT_MATCHED")

    pre_trace: _PreTraceHandle | None = None
    try:
        pre_trace = _trace_persist_pre(
            target_root,
            attempt.attempt_id,
            selected_guidance,
            attempt.operation_guidance_ref,
            operation_depth_observation,
        )
    except Exception:
        # Progress evidence is derived and non-authoritative.  Its absence or
        # failure must not alter the governed execution decision.
        pre_trace = None

    execution = invoke_governed_operation(
        attempt,
        selected_guidance,
        bounded_payload,
        completion,
        payload_schema_ref,
        authority_refs,
        guidance_ref,
        dependency_input=dependency_input,
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
    evaluation_attempt = attempt.as_v1() if isinstance(attempt, AttemptRecordV2) else attempt
    technical = evaluate_technical(
        attempt=evaluation_attempt,
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
    source_publication: dict[str, Any] | None = None
    if _is_dependent_endpoint(attempt, "T-01") and technical.outcome == "SATISFIED":
        try:
            source_publication = _publish_satisfied_source_outputs(
                root, attempt, observed, typed, technical
            )
        except Exception as exc:
            return _stopped(
                attempt_id,
                "T-07_SOURCE_OUTPUT_PUBLICATION",
                type(exc).__name__,
                guidance=selected_guidance,
                envelope=envelope,
                execution=execution,
                receipt=persisted,
                observed_result=observed,
                technical_evaluation=technical,
                terminal_attempt=terminal,
            )
    checkpoint = PostEvaluationCheckpointV1(
        attempt_id=attempt.attempt_id,
        result_id=observed.result_id,
        evaluation_id=technical.evaluation_id,
        evaluation_outcome=technical.outcome,
        evaluation_reason_codes=technical.reason_codes,
    )
    post_spine_snapshot: ProjectSpineSnapshotV1
    try:
        post_spine_snapshot = record_post_evaluation_checkpoint(
            target_root,
            pre_execution_snapshot=pre_execution_project_spine_snapshot,
            checkpoint=checkpoint,
            operation_guidance=selected_guidance,
        )
        downstream = build_compact_status(target_root, attempt_id=attempt.attempt_id)
        if downstream.get("what_next") != pre_execution_project_spine_snapshot.next_permitted_action:
            raise ProjectSpineHandoffError("post-PL08 compact status is not authoritative")
        if source_publication is not None:
            downstream = {
                **downstream,
                "dependency_admission_trigger_a": source_publication["trigger_a"],
                "dependency_proof_id": source_publication["proof_id"],
                "producer_artifact_digest": source_publication["artifact_digest"],
            }
    except (ProjectSpineHandoffError, OSError, ValueError, KeyError, TypeError) as exc:
        return _stopped(
            attempt_id,
            "PL08 Result/Evidence -> authoritative Next Gate",
            "PROJECT_SPINE_HANDOFF",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
            receipt=persisted,
            observed_result=observed,
            technical_evaluation=technical,
            terminal_attempt=terminal,
        )
    if pre_trace is not None:
        try:
            _trace_persist_post(pre_trace, persisted, post_spine_snapshot)
        except Exception:
            # A stale or malformed trace cannot roll back facts already owned
            # by receipt, Attempt Runtime, PL08, or Project Spine.
            pass
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
        downstream=downstream,
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
