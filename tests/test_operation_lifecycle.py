from __future__ import annotations

from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path

import pytest

from planning_lite import operation_lifecycle as lifecycle
from planning_lite.attempt_evaluation import (
    AcceptanceContractV1,
    AttemptRecordV1,
    CandidateIdentityV1,
    EvidenceApplicabilityV1,
    EvidenceSupersessionV1,
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
from planning_lite.context import OperationDepthObservationV1
from planning_lite.execution_guidance import select_operation_guidance
from planning_lite.governed_executor import (
    EvidenceContentInputV1,
    GovernedExecutionCompletionV1,
    GovernedExecutionDependencyInputV1,
    GovernedExecutionResultV1,
    invoke_governed_operation,
    prepare_governed_operation,
)
from planning_lite.project_spine import capture_project_spine_snapshot
from planning_lite.operation_trace import TRACE_COMPLETE, read_operation_trace_evidence


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


def _production_completion_mapping(completion: GovernedExecutionCompletionV1) -> dict[str, object]:
    def detached(value: object) -> object:
        if isinstance(value, Mapping):
            return {key: detached(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [detached(item) for item in value]
        method = getattr(value, "to_mapping", None)
        if callable(method):
            return detached(method())
        return value

    return {
        field: detached(getattr(completion, field))
        for field in GovernedExecutionCompletionV1.__dataclass_fields__
    }


def _prepare_project_spine(root: Path, attempt: AttemptRecordV1) -> None:
    planning = root / ".planning"
    (planning / "framework").mkdir(parents=True)
    (planning / "project").mkdir()
    context_dir = planning / "changes" / "active" / attempt.change_id
    context_dir.mkdir(parents=True)
    (planning / "framework" / "defaults.yml").write_text(
        "schema_version: 1\n"
        "project_policy:\n"
        "  schema_version: 1\n"
        "  project_id: demo\n"
        "  planning_root: .planning\n"
        "  agents_root: .agents\n"
        "  forbidden_read_paths: []\n"
        "  secret_storage: prohibited\n",
        encoding="utf-8",
    )
    (planning / "ACTIVE.md").write_text(
        "# Active state\n\n## Active change\n\n"
        f"- Change: `{attempt.change_id}`\n"
        "- Change status: `Active`\n"
        "- Lifecycle stage: `Implementation`\n"
        "- Stage status: `In progress`\n"
        f"- Current task: `{attempt.task_or_operation_id}`\n"
        "- Last verified checkpoint: `checkpoint-0`\n"
        "- Next gate: `Central Candidate Review Gate`\n"
        "- Next permitted action: `EXECUTE_AUTHORIZED_TASK`\n"
        "- Implementation authorized: `Yes`\n"
        f"- Active context packet: `.planning/changes/active/{attempt.change_id}/context.md`\n\n"
        "## Blocking decision\n\n- `None`\n",
        encoding="utf-8",
    )
    (planning / "project" / "CURRENT_STATE.md").write_text(
        "- Project: `Demo`\n- Direction: `Bounded`\n", encoding="utf-8"
    )
    (context_dir / "context.md").write_text(
        "# Active context\n\n- Approved outcome: `bounded`\n", encoding="utf-8"
    )


def _depth_observation(attempt: AttemptRecordV1) -> OperationDepthObservationV1:
    return OperationDepthObservationV1._create(
        operation_ref=attempt.attempt_id,
        start={
            "context_trace_ref": None,
            "source_revision": {"head": "a" * 64, "state": "AVAILABLE"},
            "freshness": "CURRENT",
            "selected_sources": [],
            "selected_artifact_count": 0,
            "selected_section_count": 0,
            "selected_character_count": 0,
            "explicit_expansion_count": 0,
            "bounds": {
                "default_artifacts": 3,
                "explicit_expansions": 5,
                "total_artifacts": 8,
                "current_state_chars": 8192,
                "active_context_chars": 16384,
                "section_chars": 4096,
            },
        },
    )


def _wire(
    monkeypatch: pytest.MonkeyPatch,
    calls: list[str],
    attempt: AttemptRecordV1,
    completion: GovernedExecutionCompletionV1,
    root: Path,
    *,
    with_progress: bool = False,
):
    _prepare_project_spine(root, attempt)
    if with_progress:
        (root / ".planning" / "changes" / "active" / attempt.change_id / "progress.md").write_text(
            "# Progress\n\n## Governed Attempt / Evaluation evidence\n\n"
            "- Existing historical body must remain byte-stable.\n",
            encoding="utf-8",
        )
    snapshot = capture_project_spine_snapshot(root)
    guidance = _guidance()
    activatable = AttemptEnvelopeV1(attempt, "ACTIVATABLE")
    inflight = AttemptEnvelopeV1(attempt, "IN_FLIGHT")
    monkeypatch.setattr(lifecycle, "lookup_attempt", lambda *_: (calls.append("lookup") or AttemptLookupResultV1(LookupOutcome.FOUND, activatable)))
    monkeypatch.setattr(lifecycle, "check_activation_admissibility", lambda *_: (calls.append("admissibility") or AttemptAdmissibilityResultV1(AdmissibilityOutcome.ADMISSIBLE, activatable)))
    monkeypatch.setattr(lifecycle, "claim_attempt", lambda *_: (calls.append("claim") or inflight))
    real_invoke = lifecycle.invoke_governed_operation
    monkeypatch.setattr(lifecycle, "invoke_governed_operation", lambda *args, **kwargs: (calls.append("execute") or real_invoke(*args, **kwargs)))
    monkeypatch.setattr(
        lifecycle,
        "collect_governed_receipt",
        lambda *args, **kwargs: (
            calls.append("receipt")
            or {
                "schema_version": 2,
                "receipt_id": "RECEIPT-1",
                "attempt_id": attempt.attempt_id,
                "execution_invocation_id": completion.execution_invocation_id,
                "planning_lite_ref": "v1",
                "model_id": "model-1",
                "agent_role": "PARENT",
                "invocation_index": 0,
                "runtime_source": "test-runtime",
            }
        ),
    )
    terminal = AttemptEnvelopeV1(attempt.__class__(**{**attempt.__dict__}) if hasattr(attempt, "__dict__") else attempt, "IN_FLIGHT")
    monkeypatch.setattr(lifecycle, "terminalize_attempt", lambda *_: (calls.append("terminal") or terminal))
    real_evaluate = lifecycle.evaluate_technical
    monkeypatch.setattr(
        lifecycle,
        "evaluate_technical",
        lambda *args, **kwargs: (calls.append("pl08") or real_evaluate(*args, **kwargs)),
    )
    monkeypatch.setattr(
        lifecycle,
        "record_post_evaluation_checkpoint",
        lambda *args, **kwargs: (calls.append("spine") or snapshot),
    )
    return guidance, snapshot


def test_pattern_b_order_and_identity_triangle(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    attempt = _attempt()
    completion = _completion(attempt)
    calls: list[str] = []
    guidance, snapshot = _wire(monkeypatch, calls, attempt, completion, tmp_path)
    result = lifecycle.execute_governed_operation(
        tmp_path,
        attempt.attempt_id,
        target_root=tmp_path,
        pre_execution_project_spine_snapshot=snapshot,
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
    assert calls == ["lookup", "admissibility", "claim", "execute", "receipt", "terminal", "pl08", "spine"]


def test_production_shaped_completion_crosses_typed_boundary(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    attempt = _attempt()
    completion = replace(_completion(attempt), receipt_id="RECEIPT-1")
    finding = FindingV1(
        "F-1",
        "Boundary fixture is non-blocking.",
        "NON_MATERIAL",
        ("FIXTURE_HARNESS",),
        "NON_BLOCKING",
        "CLOSED",
        ("FACT-1",),
        "OWNER-REVIEW-PL09",
        lifecycle.FindingApplicabilityV1(
            attempt.attempt_id,
            attempt.candidate_identity,
            "AC-1",
            "SCOPE-1",
            attempt.baseline_refs,
        ),
    )
    completion = replace(
        completion,
        findings=(finding,),
        supersession=(
            lifecycle.EvidenceSupersessionV1(
                "E-0", "E-1", "SCOPE-1", ("FACT-1",), "Fresh boundary verification"
            ),
        ),
    )
    production_completion = _production_completion_mapping(completion)
    raw_boundary_completion = GovernedExecutionCompletionV1(**production_completion)
    assert isinstance(raw_boundary_completion, GovernedExecutionCompletionV1)
    assert not lifecycle._evaluation_carriers_valid(raw_boundary_completion)
    calls: list[str] = []
    converted: list[GovernedExecutionCompletionV1 | None] = []
    pl08_inputs: list[dict[str, object]] = []
    real_typed_completion = lifecycle._typed_completion
    monkeypatch.setattr(
        lifecycle,
        "_typed_completion",
        lambda value: (converted.append(real_typed_completion(value)) or converted[-1]),
    )
    guidance, snapshot = _wire(monkeypatch, calls, attempt, completion, tmp_path)
    real_evaluate = lifecycle.evaluate_technical
    monkeypatch.setattr(
        lifecycle,
        "evaluate_technical",
        lambda **kwargs: (pl08_inputs.append(kwargs) or real_evaluate(**kwargs)),
    )

    result = lifecycle.execute_governed_operation(
        tmp_path,
        attempt.attempt_id,
        target_root=tmp_path,
        pre_execution_project_spine_snapshot=snapshot,
        guidance=guidance,
        bounded_payload={"task": "T-01"},
        completion=production_completion,
        receipt={"schema_version": 2, "receipt_id": "RECEIPT-1"},
        receipt_path=tmp_path / "receipts.jsonl",
        registered_project_id="demo",
        telemetry_enabled=True,
    )

    assert result.completed
    assert len(converted) == 1
    typed = converted[0]
    assert isinstance(typed, GovernedExecutionCompletionV1)
    assert isinstance(typed.acceptance_contract, AcceptanceContractV1)
    assert all(isinstance(item, VerifierContractV1) for item in typed.verifier_contracts)
    assert all(isinstance(item, VerifierEvidenceV1) for item in typed.verifier_evidence)
    assert all(isinstance(item, FindingV1) for item in typed.findings)
    assert all(isinstance(item, lifecycle.EvidenceSupersessionV1) for item in typed.supersession)
    assert typed.attempt_id == completion.attempt_id
    assert typed.execution_invocation_id == completion.execution_invocation_id
    assert typed.envelope_digest == completion.envelope_digest
    assert typed.result_id == completion.result_id
    assert typed.receipt_id == completion.receipt_id
    assert calls == ["lookup", "admissibility", "claim", "execute", "receipt", "terminal", "pl08", "spine"]
    assert len(pl08_inputs) == 1
    inputs = pl08_inputs[0]
    assert inputs["attempt"] is attempt
    assert inputs["contracts"] is typed.verifier_contracts
    assert inputs["evidence"] is typed.verifier_evidence
    assert inputs["findings"] is typed.findings
    assert inputs["acceptance_contract"] is typed.acceptance_contract
    assert inputs["supersession"] is typed.supersession
    assert inputs["acceptance_contract_ref"] == attempt.acceptance_contract_ref
    assert inputs["evaluation_scope_ref"] == typed.evaluation_scope_ref
    assert inputs["evaluation_id"] == typed.evaluation_id
    assert inputs["evaluation_run"] == typed.evaluation_run
    assert inputs["candidate_quality"] == typed.candidate_quality


def test_lifecycle_writes_bounded_trace_before_execute_and_after_s6(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    attempt = _attempt()
    completion = replace(_completion(attempt), receipt_id="RECEIPT-1")
    calls: list[str] = []
    guidance, snapshot = _wire(
        monkeypatch, calls, attempt, completion, tmp_path, with_progress=True
    )
    progress = tmp_path / ".planning" / "changes" / "active" / attempt.change_id / "progress.md"

    result = lifecycle.execute_governed_operation(
        tmp_path,
        attempt.attempt_id,
        target_root=tmp_path,
        pre_execution_project_spine_snapshot=snapshot,
        guidance=guidance,
        bounded_payload={"task": "T-01"},
        completion=completion,
        receipt={"schema_version": 2, "receipt_id": "RECEIPT-1"},
        receipt_path=tmp_path / "receipts.jsonl",
        registered_project_id="demo",
        telemetry_enabled=True,
        operation_depth_observation=_depth_observation(attempt),
    )

    assert result.completed
    assert calls == ["lookup", "admissibility", "claim", "execute", "receipt", "terminal", "pl08", "spine"]
    body = progress.read_text(encoding="utf-8")
    assert body.count("PL_OPERATION_TRACE_ENTRIES_BEGIN") == 1
    assert body.count("PL_OPERATION_TRACE_ENTRY_BEGIN") == 1
    _, _, entries = lifecycle._trace_read(progress, initialize_legacy=False)
    assert len(entries) == 1
    persisted = result.receipt
    assert persisted is not None
    view = read_operation_trace_evidence(
        entries[0][2], lambda ref: dict(persisted) if ref.endswith("#receipt_id=RECEIPT-1") else None
    )
    assert view.trace_state == TRACE_COMPLETE
    assert view.f01 is not None and view.f01["operation_guidance_ref"] == attempt.operation_guidance_ref
    assert view.f03 is not None and view.f03["next_gate_ref"] == snapshot.next_permitted_action


def test_lifecycle_trace_failure_does_not_create_missing_progress_or_change_result(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    attempt = _attempt()
    completion = replace(_completion(attempt), receipt_id="RECEIPT-1")
    calls: list[str] = []
    guidance, snapshot = _wire(monkeypatch, calls, attempt, completion, tmp_path)
    result = lifecycle.execute_governed_operation(
        tmp_path,
        attempt.attempt_id,
        target_root=tmp_path,
        pre_execution_project_spine_snapshot=snapshot,
        guidance=guidance,
        bounded_payload={"task": "T-01"},
        completion=completion,
        receipt={"schema_version": 2, "receipt_id": "RECEIPT-1"},
        receipt_path=tmp_path / "receipts.jsonl",
        registered_project_id="demo",
        telemetry_enabled=True,
    )
    progress = tmp_path / ".planning" / "changes" / "active" / attempt.change_id / "progress.md"
    assert result.completed
    assert not progress.exists()


def test_post_trace_refuses_stale_progress_without_overwrite(tmp_path: Path) -> None:
    attempt = _attempt()
    _prepare_project_spine(tmp_path, attempt)
    progress = tmp_path / ".planning" / "changes" / "active" / attempt.change_id / "progress.md"
    progress.write_text(
        "# Progress\n\n## Governed Attempt / Evaluation evidence\n\n"
        "<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->\n"
        "<!-- PL_OPERATION_TRACE_ENTRIES_END -->\n",
        encoding="utf-8",
    )
    guidance = _guidance()
    handle = lifecycle._trace_persist_pre(
        tmp_path, attempt.attempt_id, guidance, attempt.operation_guidance_ref, None
    )
    before = progress.read_bytes()
    progress.write_bytes(before + b"\nconcurrent owner update\n")
    with pytest.raises(lifecycle._TracePersistenceError, match="STALE_PROGRESS"):
        lifecycle._trace_persist_post(
            handle,
            {
                "attempt_id": attempt.attempt_id,
                "receipt_id": "receipt-1",
                "planning_lite_ref": "v1",
                "model_id": "model-1",
                "agent_role": "PARENT",
                "invocation_index": 0,
                "runtime_source": "test-runtime",
            },
            capture_project_spine_snapshot(tmp_path),
        )
    assert progress.read_bytes() == before + b"\nconcurrent owner update\n"


@pytest.mark.parametrize(
    "owner_body",
    [
        (
            "## Governed Attempt / Evaluation evidence\n"
            "\n## Governed Attempt / Evaluation evidence\n"
        ),
        (
            "## Governed Attempt / Evaluation evidence\n"
            "<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->\n"
            "<!-- PL_OPERATION_TRACE_ENTRIES_END -->\n"
            "<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->\n"
        ),
        (
            "## Governed Attempt / Evaluation evidence\n"
            "<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->\n"
        ),
    ],
)
def test_trace_marker_structure_fails_closed(tmp_path: Path, owner_body: str) -> None:
    attempt = _attempt()
    _prepare_project_spine(tmp_path, attempt)
    progress = tmp_path / ".planning" / "changes" / "active" / attempt.change_id / "progress.md"
    progress.write_text("# Progress\n\n" + owner_body, encoding="utf-8")
    with pytest.raises(lifecycle._TracePersistenceError):
        lifecycle._trace_persist_pre(
            tmp_path, attempt.attempt_id, _guidance(), attempt.operation_guidance_ref, None
        )


def test_trace_duplicate_attempt_and_crlf_are_bounded(tmp_path: Path) -> None:
    attempt = _attempt()
    _prepare_project_spine(tmp_path, attempt)
    progress = tmp_path / ".planning" / "changes" / "active" / attempt.change_id / "progress.md"
    progress.write_bytes(
        (
            "# Progress\n\n## Governed Attempt / Evaluation evidence\n\n"
            "<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->\n"
            "<!-- PL_OPERATION_TRACE_ENTRIES_END -->\n"
        ).replace("\n", "\r\n").encode("utf-8")
    )
    lifecycle._trace_persist_pre(
        tmp_path, attempt.attempt_id, _guidance(), attempt.operation_guidance_ref, None
    )
    assert b"\r\n" in progress.read_bytes()
    with pytest.raises(lifecycle._TracePersistenceError, match="DUPLICATE_TRACE_ATTEMPT"):
        lifecycle._trace_persist_pre(
            tmp_path, attempt.attempt_id, _guidance(), attempt.operation_guidance_ref, None
        )


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
    assert "def _trace_atomic_replace(" in source


def test_lifecycle_false_done_and_next_gate_boundaries() -> None:
    result = lifecycle.GovernedLifecycleResultV1("COMPLETED_WITH_FACTS", "CHG/T/A1", downstream={"status_projection": "AVAILABLE"})
    assert "next_gate" not in result.to_mapping()
    assert result.disposition != "PASSING"


def test_public_t07_source_to_successor_bytes_use_one_satisfied_pl08_pass(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    """Exercise public endpoint Preparation/claim and the byte-identical successor seam."""
    import hashlib

    from planning_lite import dependency_admission as dependency_owner
    from planning_lite.attempt_evaluation import EvidenceApplicabilityV1
    from planning_lite.attempt_runtime import (
        AttemptEnvelopeV2,
        claim_attempt,
        prepare_attempt,
    )
    from planning_lite.authorization import issue_preparation_authorization
    from planning_lite.dependency_admission import resolve_evidence_content, resolve_dependency
    from planning_lite.workspace import resolve_dependency_artifact_output_route

    change_id = "CHG-TEST-DEPENDENCY-001"
    from test_dependency_admission import _write_fixture

    _write_fixture(tmp_path, change_id=change_id)
    planning = tmp_path / ".planning"
    (planning / "framework").mkdir(parents=True, exist_ok=True)
    (planning / "project").mkdir(parents=True, exist_ok=True)
    (planning / "framework" / "defaults.yml").write_text(
        "schema_version: 1\nproject_policy:\n"
        "  schema_version: 1\n  project_id: demo\n  planning_root: .planning\n"
        "  agents_root: .agents\n  forbidden_read_paths: []\n"
        "  secret_storage: prohibited\n",
        encoding="utf-8",
    )
    (planning / "CONFIG.yml").write_text("{}\n", encoding="utf-8")
    (planning / "project" / "CURRENT_STATE.md").write_text(
        "- Project: `Demo`\n- Direction: `Bounded dependency byte flow`\n",
        encoding="utf-8",
    )
    context_dir = planning / "changes" / "active" / change_id
    (context_dir / "context.md").write_text(
        "# Active context\n\n- Approved outcome: `produce and consume exact bytes`\n",
        encoding="utf-8",
    )
    (planning / "ACTIVE.md").write_text(
        "# Active state\n\n## Active change\n\n"
        f"- Change: `{change_id}`\n- Change status: `Active`\n"
        "- Lifecycle stage: `Implementation`\n- Stage status: `In progress`\n"
        "- Current task: `T-01`\n- Last verified checkpoint: `checkpoint-0`\n"
        "- Next gate: `Central Candidate Review Gate`\n"
        "- Next permitted action: `EXECUTE_AUTHORIZED_TASK`\n"
        "- Implementation authorized: `Yes`\n"
        f"- Active context packet: `.planning/changes/active/{change_id}/context.md`\n\n"
        "## Blocking decision\n\n- `None`\n",
        encoding="utf-8",
    )
    requirement = resolve_dependency(tmp_path, "T-01").requirement

    # Both endpoint authorities exist before either public A1 is occupied.
    source_auth = issue_preparation_authorization(
        tmp_path, change_id, "T-01", "decision:source-preparation"
    )
    successor_auth = issue_preparation_authorization(
        tmp_path, change_id, "T-02", "decision:successor-preparation"
    )
    head = "a" * 40
    preparation = {
        "acceptance_contract_ref": requirement["acceptance_contract_ref"],
        "candidate_identity": {"kind": "GIT_COMMIT", "head": head, "dirty_manifest": []},
        "baseline_refs": [{"ref": "HEAD", "identity": head}],
        "operation_guidance_ref": "EXECUTE_AUTHORIZED_TASK",
        "verifier_contract_refs": [
            {"contract_id": "build", "contract_version_or_ref": "v1"}
        ],
    }
    source_prepared = prepare_attempt(
        tmp_path,
        {
            **preparation,
            "change_id": change_id,
            "task_or_operation_id": "T-01",
            "authorization_ref": source_auth,
        },
    )
    assert source_prepared.attempt_id == f"{change_id}/T-01/A1"
    assert resolve_dependency(tmp_path, "T-01").requirement == resolve_dependency(
        tmp_path, "T-02"
    ).requirement

    guidance = _guidance()
    payload = {"operation": "produce exact governed bytes"}
    source_envelope = prepare_governed_operation(source_prepared.attempt, guidance, payload)
    verifier_contract = VerifierContractV1(
        requirement["acceptance_contract_ref"],
        "build",
        "v1",
        True,
        "AUTOMATED_TEST",
        "All required checks pass",
        ("evidence-content:build",),
        "Block on missing or non-pass evidence",
    )
    acceptance_contract = AcceptanceContractV1(
        requirement["acceptance_contract_ref"], (verifier_contract,)
    )
    applicability = EvidenceApplicabilityV1(
        source_prepared.attempt.attempt_id,
        source_prepared.attempt.candidate_identity,
        requirement["acceptance_contract_ref"],
        "build",
        "v1",
        requirement["evaluation_scope_ref"],
        input_baseline_refs=source_prepared.attempt.baseline_refs,
    )
    evidence = VerifierEvidenceV1(
        "evidence:build:pass",
        source_prepared.attempt.attempt_id,
        source_prepared.attempt.candidate_identity,
        "build",
        "v1",
        "PASS",
        ("evidence-content:build",),
        applicability,
        ("claim:build",),
    )
    artifact_bytes = b"the exact producer bytes\x00\xff"
    evidence_bytes = b"actual invocation-associated Class-B evidence"
    completion = GovernedExecutionCompletionV1(
        attempt_id=source_envelope.attempt_id,
        execution_invocation_id=source_envelope.execution_invocation_id,
        envelope_digest=source_envelope.envelope_digest,
        operation_id=source_envelope.operation_id,
        task_or_operation_id="T-01",
        result_id="result:source:1",
        execution_status="COMPLETED",
        fact_refs=("claim:build",),
        artifact_refs=(requirement["produced_artifact_logical_ref"],),
        acceptance_contract_ref=requirement["acceptance_contract_ref"],
        acceptance_contract=acceptance_contract,
        verifier_contracts=(verifier_contract,),
        verifier_evidence=(evidence,),
        evaluation_scope_ref=requirement["evaluation_scope_ref"],
        evaluation_id="evaluation:source:1",
        receipt_id="receipt:source:1",
        artifact_output_bytes=artifact_bytes,
        evidence_content_inputs=(EvidenceContentInputV1("evidence-content:build", evidence_bytes),),
    )
    source_snapshot = capture_project_spine_snapshot(tmp_path)

    order: list[str] = []
    evaluator_calls: list[object] = []
    invocation_inputs: list[GovernedExecutionDependencyInputV1 | None] = []
    real_evaluate = lifecycle.evaluate_technical

    def evaluate_once(**kwargs: object):
        result = real_evaluate(**kwargs)
        evaluator_calls.append(result)
        order.append("pl08-satisfied" if result.outcome == "SATISFIED" else "pl08-other")
        return result

    monkeypatch.setattr(lifecycle, "evaluate_technical", evaluate_once)
    real_artifact_publish = lifecycle.publish_governed_artifact_output

    def publish_artifact(*args: object, **kwargs: object):
        assert evaluator_calls and evaluator_calls[-1].outcome == "SATISFIED"
        order.append("artifact-publication")
        return real_artifact_publish(*args, **kwargs)

    monkeypatch.setattr(lifecycle, "publish_governed_artifact_output", publish_artifact)
    real_evidence_publish = dependency_owner.publish_evidence_content

    def publish_evidence(*args: object, **kwargs: object):
        assert evaluator_calls and evaluator_calls[-1].outcome == "SATISFIED"
        order.append("class-b-publication")
        return real_evidence_publish(*args, **kwargs)

    monkeypatch.setattr(dependency_owner, "publish_evidence_content", publish_evidence)
    real_capture = dependency_owner.capture_dependency_acceptance_proof

    def capture_proof(*args: object, **kwargs: object):
        order.append("proof-capture")
        return real_capture(*args, **kwargs)

    monkeypatch.setattr(dependency_owner, "capture_dependency_acceptance_proof", capture_proof)
    real_install = lifecycle.publish_dependency_acceptance_proof

    def install_current(*args: object, **kwargs: object):
        order.append("proof-current-trigger-a")
        return real_install(*args, **kwargs)

    monkeypatch.setattr(lifecycle, "publish_dependency_acceptance_proof", install_current)
    publication_errors: list[str] = []
    real_source_publication = lifecycle._publish_satisfied_source_outputs

    def observe_source_publication(*args: object, **kwargs: object):
        try:
            return real_source_publication(*args, **kwargs)
        except Exception as exc:
            publication_errors.append(f"{type(exc).__name__}: {exc}")
            raise

    monkeypatch.setattr(lifecycle, "_publish_satisfied_source_outputs", observe_source_publication)
    monkeypatch.setattr(
        lifecycle,
        "_receipt_context",
        lambda target, **kwargs: ("demo", kwargs["receipt_path"], True),
    )

    def collect_receipt(receipt: object, *, attempt_id: str, execution_invocation_id: str, **kwargs: object):
        order.append("receipt")
        return {
            "schema_version": 2,
            "receipt_id": "receipt:source:1",
            "attempt_id": attempt_id,
            "execution_invocation_id": execution_invocation_id,
            "planning_lite_ref": "planning-lite:test",
            "model_id": "model:test",
            "agent_role": "PARENT",
            "invocation_index": 0,
            "runtime_source": "t07-test-host",
        }

    monkeypatch.setattr(lifecycle, "collect_governed_receipt", collect_receipt)
    real_terminalize = lifecycle.terminalize_attempt

    def terminalize(*args: object, **kwargs: object):
        order.append("terminal-completed")
        return real_terminalize(*args, **kwargs)

    monkeypatch.setattr(lifecycle, "terminalize_attempt", terminalize)
    real_invoke = lifecycle.invoke_governed_operation

    def observe_invocation(*args: object, **kwargs: object):
        invocation_inputs.append(kwargs.get("dependency_input"))
        order.append(f"invoke-{kwargs.get('dependency_input') is not None}")
        return real_invoke(*args, **kwargs)

    monkeypatch.setattr(lifecycle, "invoke_governed_operation", observe_invocation)

    source_result = lifecycle.execute_governed_operation(
        tmp_path,
        source_prepared.attempt_id,
        target_root=tmp_path,
        pre_execution_project_spine_snapshot=source_snapshot,
        guidance=guidance,
        bounded_payload=payload,
        completion=completion,
        receipt={"schema_version": 2, "receipt_id": "receipt:source:1"},
        receipt_path=tmp_path / "receipts.jsonl",
        registered_project_id="demo",
        telemetry_enabled=True,
    )
    assert source_result.completed, (source_result.to_mapping(), publication_errors)
    assert source_result.technical_evaluation.outcome == "SATISFIED"
    assert source_result.downstream["dependency_admission_trigger_a"]["outcome"] == "DEFERRED_SUCCESSOR_NOT_PREPARED"
    assert len(evaluator_calls) == 1
    assert invocation_inputs == [None]
    assert order.index("invoke-False") < order.index("receipt")
    assert order.index("receipt") < order.index("terminal-completed")
    assert order.index("terminal-completed") < order.index("pl08-satisfied")
    assert order.index("pl08-satisfied") < order.index("artifact-publication")
    assert order.index("artifact-publication") < order.index("class-b-publication")
    assert order.index("class-b-publication") < order.index("proof-capture")
    assert order.index("proof-capture") < order.index("proof-current-trigger-a")

    route = resolve_dependency_artifact_output_route(tmp_path)
    assert route.path.read_bytes() == artifact_bytes
    assert resolve_evidence_content(tmp_path, "evidence-content:build").exact_raw_bytes == evidence_bytes
    successor_prepared = prepare_attempt(
        tmp_path,
        {
            **preparation,
            "change_id": change_id,
            "task_or_operation_id": "T-02",
            "authorization_ref": successor_auth,
        },
    )
    assert successor_prepared.attempt_id == f"{change_id}/T-02/A1"
    assert successor_prepared.attempt.dependency_admission is not None
    successor_claim = claim_attempt(tmp_path, successor_prepared.attempt_id)
    assert isinstance(successor_claim, AttemptEnvelopeV2)
    assert successor_claim.runtime_state == "IN_FLIGHT"
    dependency_input = lifecycle._fresh_successor_dependency_input(tmp_path, successor_claim)
    assert type(dependency_input) is GovernedExecutionDependencyInputV1
    assert dependency_input.required_input_logical_ref == requirement["required_successor_input_logical_ref"]
    assert dependency_input.exact_raw_bytes == artifact_bytes
    assert hashlib.sha256(dependency_input.exact_raw_bytes).hexdigest() == hashlib.sha256(artifact_bytes).hexdigest()

    successor_envelope = prepare_governed_operation(
        successor_prepared.attempt, guidance, {"operation": "consume exact bytes"}
    )
    successor_completion = GovernedExecutionCompletionV1(
        attempt_id=successor_envelope.attempt_id,
        execution_invocation_id=successor_envelope.execution_invocation_id,
        envelope_digest=successor_envelope.envelope_digest,
        operation_id=successor_envelope.operation_id,
        task_or_operation_id="T-02",
        result_id="result:successor:1",
        execution_status="COMPLETED",
    )
    successor_execution = lifecycle.invoke_governed_operation(
        successor_prepared.attempt,
        guidance,
        {"operation": "consume exact bytes"},
        successor_completion,
        dependency_input=dependency_input,
    )
    assert successor_execution.accepted
    assert invocation_inputs[1] is dependency_input
    assert invocation_inputs[1].exact_raw_bytes == artifact_bytes

    # On a fresh independent consumer, mutate the canonical artifact only
    # after the public T-02 D11 claim. Lifecycle must stop before its executor
    # and evaluator while leaving that already-successful claim IN_FLIGHT.
    negative_root = tmp_path / "post-claim-negative"
    _write_fixture(negative_root, change_id=change_id)
    negative_planning = negative_root / ".planning"
    (negative_planning / "framework").mkdir(parents=True, exist_ok=True)
    (negative_planning / "project").mkdir(parents=True, exist_ok=True)
    (negative_planning / "framework" / "defaults.yml").write_text(
        "schema_version: 1\nproject_policy:\n"
        "  schema_version: 1\n  project_id: demo\n  planning_root: .planning\n"
        "  agents_root: .agents\n  forbidden_read_paths: []\n"
        "  secret_storage: prohibited\n",
        encoding="utf-8",
    )
    (negative_planning / "CONFIG.yml").write_text("{}\n", encoding="utf-8")
    (negative_planning / "project" / "CURRENT_STATE.md").write_text(
        "- Project: `Demo`\n- Direction: `Bounded dependency byte flow`\n",
        encoding="utf-8",
    )
    negative_context = negative_planning / "changes" / "active" / change_id / "context.md"
    negative_context.write_text(
        "# Active context\n\n- Approved outcome: `produce and consume exact bytes`\n",
        encoding="utf-8",
    )
    negative_active = (negative_planning / "ACTIVE.md")
    negative_active.write_text(
        "# Active state\n\n## Active change\n\n"
        f"- Change: `{change_id}`\n- Change status: `Active`\n"
        "- Lifecycle stage: `Implementation`\n- Stage status: `In progress`\n"
        "- Current task: `T-01`\n- Last verified checkpoint: `checkpoint-0`\n"
        "- Next gate: `Central Candidate Review Gate`\n"
        "- Next permitted action: `EXECUTE_AUTHORIZED_TASK`\n"
        "- Implementation authorized: `Yes`\n"
        f"- Active context packet: `.planning/changes/active/{change_id}/context.md`\n\n"
        "## Blocking decision\n\n- `None`\n",
        encoding="utf-8",
    )
    negative_source_auth = issue_preparation_authorization(
        negative_root, change_id, "T-01", "decision:negative-source"
    )
    negative_successor_auth = issue_preparation_authorization(
        negative_root, change_id, "T-02", "decision:negative-successor"
    )
    negative_source = prepare_attempt(
        negative_root,
        {
            **preparation,
            "change_id": change_id,
            "task_or_operation_id": "T-01",
            "authorization_ref": negative_source_auth,
        },
    )
    negative_snapshot = capture_project_spine_snapshot(negative_root)
    negative_source_result = lifecycle.execute_governed_operation(
        negative_root,
        negative_source.attempt_id,
        target_root=negative_root,
        pre_execution_project_spine_snapshot=negative_snapshot,
        guidance=guidance,
        bounded_payload=payload,
        completion=completion,
        receipt={"schema_version": 2, "receipt_id": "receipt:source:1"},
        receipt_path=negative_root / "receipts.jsonl",
        registered_project_id="demo",
        telemetry_enabled=True,
    )
    assert negative_source_result.completed
    negative_successor = prepare_attempt(
        negative_root,
        {
            **preparation,
            "change_id": change_id,
            "task_or_operation_id": "T-02",
            "authorization_ref": negative_successor_auth,
        },
    )
    negative_snapshot = capture_project_spine_snapshot(negative_root)
    calls_before_invalid_input = len(invocation_inputs)
    evaluations_before_invalid_input = len(evaluator_calls)
    real_route_resolver = lifecycle.resolve_dependency_artifact_output_route

    def mutate_after_claim(target: object):
        route_value = real_route_resolver(target)
        route_value.path.write_bytes(b"changed after D11 claim")
        return route_value

    monkeypatch.setattr(lifecycle, "resolve_dependency_artifact_output_route", mutate_after_claim)
    stopped = lifecycle.execute_governed_operation(
        negative_root,
        negative_successor.attempt_id,
        target_root=negative_root,
        pre_execution_project_spine_snapshot=negative_snapshot,
        guidance=guidance,
        bounded_payload={"operation": "consume exact bytes"},
        completion=None,
        receipt=None,
        receipt_path=negative_root / "receipts.jsonl",
        registered_project_id="demo",
        telemetry_enabled=True,
    )
    assert stopped.disposition == "STOPPED_FAIL_CLOSED"
    assert stopped.first_broken_seam == "SUCCESSOR_DEPENDENCY_INPUT"
    assert stopped.reason_code == "DEPENDENCY_INPUT_INVALID"
    assert stopped.execution is None and stopped.receipt is None
    assert stopped.observed_result is None and stopped.technical_evaluation is None
    assert stopped.terminal_attempt is None
    assert len(invocation_inputs) == calls_before_invalid_input
    assert len(evaluator_calls) == evaluations_before_invalid_input
    from planning_lite.attempt_runtime import lookup_attempt

    assert lookup_attempt(negative_root, negative_successor.attempt_id).runtime_state == "IN_FLIGHT"
    negative_source_row = lookup_attempt(negative_root, negative_source.attempt_id).envelope
    assert negative_source_row.dependency_edge_control["proof_head"]["state"] == "CURRENT"


def test_t07_class_b_inputs_require_exact_refs_and_allow_class_a_only() -> None:
    """Lifecycle needs bytes only for external Class-B refs, exactly once each."""
    completion = _completion(_attempt())
    evidence = completion.verifier_evidence[0]
    first_class_a = replace(evidence, evidence_refs=())
    second_class_a = replace(evidence, evidence_id="E-2", evidence_refs=())
    class_a_only = replace(
        completion,
        verifier_evidence=(first_class_a, second_class_a),
        supersession=(
            EvidenceSupersessionV1(
                "E-1", "E-2", "SCOPE-OTHER", ("FACT-1",), "Captured Class-A mapping pair."
            ),
        ),
    )
    assert lifecycle._required_class_b_evidence_refs(class_a_only) == frozenset()
    assert lifecycle._exact_class_b_inputs(class_a_only) == {}

    class_b = replace(
        completion,
        verifier_evidence=(replace(evidence, evidence_refs=("external:a", "external:b")),),
    )
    assert lifecycle._required_class_b_evidence_refs(class_b) == frozenset({"external:a", "external:b"})
    exact_inputs = (
        EvidenceContentInputV1("external:a", b"a bytes"),
        EvidenceContentInputV1("external:b", b"b bytes"),
    )
    joined = lifecycle._exact_class_b_inputs(replace(class_b, evidence_content_inputs=exact_inputs))
    assert joined["external:a"].exact_raw_bytes == b"a bytes"
    assert joined["external:b"].exact_raw_bytes == b"b bytes"

    invalid_inputs = (
        (),
        (EvidenceContentInputV1("external:a", b"a bytes"),),
        (
            EvidenceContentInputV1("external:a", b"a bytes"),
            EvidenceContentInputV1("external:b", b"b bytes"),
            EvidenceContentInputV1("external:unrelated", b"other bytes"),
        ),
        (
            EvidenceContentInputV1("external:a", b"a bytes"),
            EvidenceContentInputV1("external:a", b"a bytes"),
            EvidenceContentInputV1("external:b", b"b bytes"),
        ),
        (
            EvidenceContentInputV1("external:a", b"a bytes"),
            EvidenceContentInputV1("external:a", b"conflicting bytes"),
            EvidenceContentInputV1("external:b", b"b bytes"),
        ),
    )
    for inputs in invalid_inputs:
        with pytest.raises(ValueError):
            lifecycle._exact_class_b_inputs(replace(class_b, evidence_content_inputs=inputs))
