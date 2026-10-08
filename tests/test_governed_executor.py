from __future__ import annotations

import ast
from pathlib import Path

import pytest

from planning_lite.attempt_evaluation import AttemptRecordV1, CandidateIdentityV1, IdentityRefV1
from planning_lite.execution_guidance import select_operation_guidance
from planning_lite.governed_executor import (
    EvidenceContentInputV1,
    GovernedExecutionCompletionV1,
    GovernedExecutionDependencyInputV1,
    GovernedExecutionEnvelopeV1,
    GovernedExecutorError,
    canonical_digest,
    invoke_governed_operation,
    prepare_governed_operation,
    validate_governed_completion,
)


def _attempt(guidance_ref: str = "GUIDANCE-1") -> AttemptRecordV1:
    return AttemptRecordV1(
        attempt_id="CHG-TEST-001/T-01/A1",
        change_id="CHG-TEST-001",
        task_or_operation_id="T-01",
        attempt_ordinal=1,
        authorization_ref="OWNER-AUTHORIZATION-1",
        acceptance_contract_ref="AC-1",
        candidate_identity=CandidateIdentityV1(kind="GIT_COMMIT", head="a" * 40),
        baseline_refs=(IdentityRefV1(ref="HEAD", identity="a" * 40),),
        operation_guidance_ref=guidance_ref,
    )


def _guidance() -> dict[str, object]:
    context = {
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
            {
                "path": ".planning/control/APPROVAL_GATES.md",
                "sha256": "ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789ABCDEF0123456789",
            }
        ],
    }
    return select_operation_guidance(context)

def test_envelope_identity_vector() -> None:
    envelope = GovernedExecutionEnvelopeV1(
        1,
        "GovernedExecutionEnvelopeV1",
        "CHG-TEST-001/T-01/A1",
        "OP-TEST",
        "T-01",
        "GUIDANCE-1",
        "0" * 63 + "1",
        ("AUTH-A", "AUTH-B"),
        "0" * 63 + "2",
        "payload.v1",
    )
    assert envelope.envelope_digest == "D2E8370C6024A14E2864DEA05AB02CA0E08678497F4E33370BC3CF35657FA829"
    assert envelope.execution_invocation_id == "A7DE0328ADF1DEC38496F8A9B3740B91672D7ACAC49662FFD7803229E820A1D1"


def test_complete_guidance_digest_vector() -> None:
    guidance = _guidance()
    assert guidance["outcome"] == "MATCHED"
    assert guidance["reason_code"] == "EXACT_OPERATION_BINDING"
    assert guidance["authority"]["predicate_result"] == "AUTHORIZED_FOR_THIS_OPERATION"  # type: ignore[index]
    assert canonical_digest(guidance).lower() == "f36d5fba7d210b60eb278a8dc8b8509daeafa2143fba89e4fc3fe5588b5fa4fe"
    envelope = prepare_governed_operation(_attempt("EXECUTE_AUTHORIZED_TASK"), guidance, {"task": "T-01"})
    assert envelope.guidance_digest == canonical_digest(guidance)


def test_executor_negative_identity_matrix() -> None:
    envelope = prepare_governed_operation(_attempt(), _guidance(), {"bounded": True})
    completion = GovernedExecutionCompletionV1(
        attempt_id="CHG-TEST-001/T-99/A1",
        execution_invocation_id=envelope.execution_invocation_id,
        envelope_digest=envelope.envelope_digest,
        operation_id=envelope.operation_id,
        task_or_operation_id=envelope.task_or_operation_id,
        result_id="RESULT-1",
        execution_status="COMPLETED",
    )
    result = validate_governed_completion(envelope, completion)
    assert not result.accepted
    assert result.failure_category == "ATTEMPT_IDENTITY_MISMATCH"


def test_executor_has_no_forbidden_owner_calls() -> None:
    tree = ast.parse((Path(__file__).parents[1] / "src/planning_lite" / "governed_executor.py").read_text(encoding="utf-8"))
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom)
        for alias in node.names
    }
    assert not imported.intersection({"attempt_runtime", "execution_guidance", "telemetry", "operation_lifecycle", "attempt_evaluation"})


def test_executor_projects_typed_result() -> None:
    envelope = prepare_governed_operation(_attempt(), _guidance(), {"bounded": True})
    completion = GovernedExecutionCompletionV1(
        attempt_id=envelope.attempt_id,
        execution_invocation_id=envelope.execution_invocation_id,
        envelope_digest=envelope.envelope_digest,
        operation_id=envelope.operation_id,
        task_or_operation_id=envelope.task_or_operation_id,
        result_id="RESULT-1",
        execution_status="COMPLETED",
        changed_paths=("src/example.py",),
        fact_refs=("FACT-1",),
        artifact_refs=("ARTIFACT-1",),
    )
    result = validate_governed_completion(envelope, completion)
    assert result.accepted
    assert result.attempt_id == envelope.attempt_id
    assert result.execution_invocation_id == envelope.execution_invocation_id
    assert result.result_id == "RESULT-1"
    assert not {"receipt_path", "runtime_store", "next_gate"}.intersection(result.__dataclass_fields__)


def test_transient_dependency_input_stays_outside_envelope_and_is_t02_only() -> None:
    attempt = AttemptRecordV1(
        attempt_id="CHG-TEST-001/T-02/A1",
        change_id="CHG-TEST-001",
        task_or_operation_id="T-02",
        attempt_ordinal=1,
        authorization_ref="OWNER-AUTHORIZATION-2",
        acceptance_contract_ref="AC-1",
        candidate_identity=CandidateIdentityV1(kind="GIT_COMMIT", head="a" * 40),
        baseline_refs=(IdentityRefV1(ref="HEAD", identity="a" * 40),),
        operation_guidance_ref="GUIDANCE-1",
    )
    guidance = _guidance()
    envelope = prepare_governed_operation(attempt, guidance, {"task": "T-02"})
    value = GovernedExecutionDependencyInputV1("artifact:build", b"producer\x00bytes")
    assert set(value.__dataclass_fields__) == {"required_input_logical_ref", "exact_raw_bytes"}
    assert type(value.exact_raw_bytes) is bytes
    assert prepare_governed_operation(attempt, guidance, {"task": "T-02"}) == envelope
    assert len(envelope.__dataclass_fields__) == 10

    completion = GovernedExecutionCompletionV1(
        attempt_id=envelope.attempt_id,
        execution_invocation_id=envelope.execution_invocation_id,
        envelope_digest=envelope.envelope_digest,
        operation_id=envelope.operation_id,
        task_or_operation_id="T-02",
        result_id="RESULT-T02",
        execution_status="COMPLETED",
    )
    result = invoke_governed_operation(
        attempt, guidance, {"task": "T-02"}, completion, dependency_input=value
    )
    assert result.accepted
    assert result.completion is completion
    with pytest.raises(GovernedExecutorError, match="exact bytes"):
        GovernedExecutionDependencyInputV1("artifact:build", bytearray(b"bad"))  # type: ignore[arg-type]
    with pytest.raises(GovernedExecutorError, match="only for T-02"):
        invoke_governed_operation(_attempt(), _guidance(), None, dependency_input=value)


def test_transient_completion_bytes_have_exact_shapes_and_do_not_change_envelope() -> None:
    envelope = prepare_governed_operation(_attempt(), _guidance(), {"task": "T-01"})
    raw = b"actual artifact bytes"
    evidence = EvidenceContentInputV1("evidence:external", b"exact Class-B bytes")
    assert set(evidence.__dataclass_fields__) == {"evidence_ref", "exact_raw_bytes"}
    completion = GovernedExecutionCompletionV1(
        attempt_id=envelope.attempt_id,
        execution_invocation_id=envelope.execution_invocation_id,
        envelope_digest=envelope.envelope_digest,
        operation_id=envelope.operation_id,
        task_or_operation_id="T-01",
        result_id="RESULT-T01",
        execution_status="COMPLETED",
        artifact_output_bytes=raw,
        evidence_content_inputs=(evidence,),
    )
    projected = validate_governed_completion(envelope, completion)
    assert projected.accepted
    assert projected.completion is completion
    assert completion.artifact_output_bytes is raw
    assert completion.evidence_content_inputs == (evidence,)
    with pytest.raises(GovernedExecutorError, match="unsupported fields"):
        from planning_lite.governed_executor import _completion_from_mapping

        mapping = {
            name: getattr(completion, name)
            for name in GovernedExecutionCompletionV1.__dataclass_fields__
        }
        _completion_from_mapping({**mapping, "caller_identity": "not allowed"})
