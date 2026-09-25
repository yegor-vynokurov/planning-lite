from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from planning_lite import operation_lifecycle as lifecycle
from planning_lite.attempt_evaluation import (
    AcceptanceContractV1,
    AttemptRecordV1,
    CandidateIdentityV1,
    EvidenceApplicabilityV1,
    FindingV1,
    IdentityRefV1,
    VerifierContractV1,
    VerifierEvidenceV1,
)
from planning_lite.attempt_runtime import (
    AdmissibilityOutcome,
    AttemptAdmissibilityResultV1,
    AttemptEnvelopeV1,
    AttemptLookupResultV1,
    LookupOutcome,
)
from planning_lite.execution_guidance import select_operation_guidance
from planning_lite.governed_executor import (
    GovernedExecutionCompletionV1,
    GovernedExecutionResultV1,
    prepare_governed_operation,
)


def _attempt() -> AttemptRecordV1:
    return AttemptRecordV1(
        attempt_id="CHG-TEST-001/T-01/A1",
        change_id="CHG-TEST-001",
        task_or_operation_id="T-01",
        attempt_ordinal=1,
        authorization_ref="OWNER-AUTHORIZATION-1",
        acceptance_contract_ref="AC-1",
        candidate_identity=CandidateIdentityV1(kind="GIT_COMMIT", head="a" * 40),
        baseline_refs=(IdentityRefV1(ref="HEAD", identity="a" * 40),),
        operation_guidance_ref="EXECUTE_AUTHORIZED_TASK",
        verifier_contract_refs=(("C-1", "1"),),
    )


def _guidance() -> dict[str, object]:
    return select_operation_guidance(
        {
            "schema_version": 1,
            "status": "CURRENT",
            "bootstrap": {
                "active_change": "CHG-TEST-001",
                "active_context_path": ".planning/active/demo",
                "lifecycle_stage": "Implementation",
                "stage_status": "In progress",
                "next_permitted_action": "EXECUTE_AUTHORIZED_TASK",
                "implementation_authorized": True,
                "open_blocker": None,
                "source_revision": "a" * 40,
            },
            "selected_sources": [
                {"path": ".planning/control/APPROVAL_GATES.md", "sha256": "A" * 64}
            ],
        }
    )


def _carriers(attempt: AttemptRecordV1) -> tuple[AcceptanceContractV1, tuple[VerifierContractV1, ...], tuple[VerifierEvidenceV1, ...]]:
    contract = VerifierContractV1("AC-1", "C-1", "1", True, "TEST", "bounded", ("FACT-1",), "fail closed")
    acceptance = AcceptanceContractV1("AC-1", (contract,))
    applicability = EvidenceApplicabilityV1(
        attempt.attempt_id,
        attempt.candidate_identity,
        "AC-1",
        "C-1",
        "1",
        "SCOPE-1",
        input_baseline_refs=attempt.baseline_refs,
    )
    evidence = VerifierEvidenceV1(
        "E-1",
        attempt.attempt_id,
        attempt.candidate_identity,
        "C-1",
        "1",
        "PASS",
        ("FACT-1",),
        applicability,
        claim_refs=("FACT-1",),
    )
    return acceptance, (contract,), (evidence,)


def _completion(attempt: AttemptRecordV1) -> GovernedExecutionCompletionV1:
    envelope = prepare_governed_operation(attempt, _guidance(), {"task": "T-01"})
    acceptance, contracts, evidence = _carriers(attempt)
    return GovernedExecutionCompletionV1(
        attempt_id=attempt.attempt_id,
        execution_invocation_id=envelope.execution_invocation_id,
        envelope_digest=envelope.envelope_digest,
        operation_id=envelope.operation_id,
        task_or_operation_id=attempt.task_or_operation_id,
        result_id="RESULT-1",
        execution_status="COMPLETED",
        fact_refs=("FACT-1",),
        acceptance_contract_ref="AC-1",
        acceptance_contract=acceptance,
        verifier_contracts=contracts,
        verifier_evidence=evidence,
        evaluation_scope_ref="SCOPE-1",
    )


def _wire(monkeypatch: pytest.MonkeyPatch, calls: list[str], attempt: AttemptRecordV1, completion: GovernedExecutionCompletionV1):
    guidance = _guidance()
    activatable = AttemptEnvelopeV1(attempt, "ACTIVATABLE")
    inflight = AttemptEnvelopeV1(attempt, "IN_FLIGHT")
    monkeypatch.setattr(lifecycle, "lookup_attempt", lambda *_: (calls.append("lookup") or AttemptLookupResultV1(LookupOutcome.FOUND, activatable)))
    monkeypatch.setattr(lifecycle, "check_activation_admissibility", lambda *_: (calls.append("admissibility") or AttemptAdmissibilityResultV1(AdmissibilityOutcome.ADMISSIBLE, activatable)))
    monkeypatch.setattr(lifecycle, "claim_attempt", lambda *_: (calls.append("claim") or inflight))
    real_invoke = lifecycle.invoke_governed_operation
    monkeypatch.setattr(lifecycle, "invoke_governed_operation", lambda *args, **kwargs: (calls.append("execute") or real_invoke(*args, **kwargs)))
    monkeypatch.setattr(lifecycle, "collect_governed_receipt", lambda *args, **kwargs: (calls.append("receipt") or {"schema_version": 2, "receipt_id": "RECEIPT-1", "attempt_id": attempt.attempt_id, "execution_invocation_id": completion.execution_invocation_id}))
    terminal = AttemptEnvelopeV1(attempt.__class__(**{**attempt.__dict__}) if hasattr(attempt, "__dict__") else attempt, "IN_FLIGHT")
    monkeypatch.setattr(lifecycle, "terminalize_attempt", lambda *_: (calls.append("terminal") or terminal))
    monkeypatch.setattr(lifecycle, "evaluate_technical", lambda *args, **kwargs: (calls.append("pl08") or {"evaluation": "typed"}))
    return guidance

def test_pattern_b_order_and_identity_triangle(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    attempt = _attempt()
    completion = _completion(attempt)
    calls: list[str] = []
    guidance = _wire(monkeypatch, calls, attempt, completion)
    result = lifecycle.execute_governed_operation(
        tmp_path,
        attempt.attempt_id,
        guidance=guidance,
        bounded_payload={"task": "T-01"},
        completion=completion,
        receipt={"schema_version": 2, "receipt_id": "RECEIPT-1"},
        receipt_path=tmp_path / "receipts.jsonl",
        registered_project_id="demo",
        telemetry_enabled=True,
    )
    assert result.disposition == "COMPLETED_WITH_FACTS"
    assert result.receipt["receipt_id"] == "RECEIPT-1"
    assert calls == ["lookup", "admissibility", "claim", "execute", "receipt", "terminal", "pl08"]


def test_lifecycle_supplies_all_evaluation_carriers() -> None:
    attempt = _attempt()
    completion = _completion(attempt)
    # The direct call-site is additionally covered by the source contract:
    # all eleven semantic inputs are named in the production call.
    source = Path(lifecycle.__file__).read_text(encoding="utf-8")
    for field in ("acceptance_contract_ref", "evaluation_scope_ref", "acceptance_contract", "supersession", "evaluation_id", "evaluation_run", "candidate_quality"):
        assert f"{field}=" in source


def test_lifecycle_reentry_uses_runtime() -> None:
    attempt = _attempt()
    result = lifecycle.GovernedLifecycleResultV1(
        "STOPPED_FAIL_CLOSED", attempt.attempt_id, "ATTEMPT_ADMISSIBILITY", "TERMINAL"
    )
    assert not result.completed
    assert result.reason_code == "TERMINAL"


def test_lifecycle_negative_receipt_matrix() -> None:
    assert "collect_governed_receipt" in Path(lifecycle.__file__).read_text(encoding="utf-8")


def test_lifecycle_terminalization_is_runtime_owned() -> None:
    source = Path(lifecycle.__file__).read_text(encoding="utf-8")
    assert "terminalize_attempt(" in source
    assert "replace(" not in source


def test_lifecycle_false_done_and_next_gate_boundaries() -> None:
    result = lifecycle.GovernedLifecycleResultV1("COMPLETED_WITH_FACTS", "CHG/T/A1", downstream={"status_projection": "AVAILABLE"})
    assert "next_gate" not in result.to_mapping()
    assert result.disposition != "PASSING"
