from __future__ import annotations

from collections.abc import Mapping

import pytest

from planning_lite.operation_trace import (
    OperationTraceError,
    TRACE_COMPLETE,
    TRACE_PARTIAL,
    bind_attempt_run_receipt,
    read_operation_trace_evidence,
    record_governed_attempt_evidence,
)
from planning_lite.context import OperationDepthObservationV1


ATTEMPT = "CHG-TRACE/T-01/A1"
OTHER_ATTEMPT = "CHG-TRACE/T-02/A1"


def _guidance() -> dict[str, object]:
    return {
        "outcome": "MATCHED",
        "reason_code": "EXACT_OPERATION_BINDING",
        "operation": {
            "operation_id": "EXECUTE_CHANGE_TASK",
            "operation_class": "EXECUTE_CHANGE_TASK",
            "route_id": "CHANGE_EXECUTION_V1",
        },
        "provenance": {
            "source_revision": "a" * 64,
            "authority_refs": [{"path": ".planning/ACTIVE.md", "sha256": "b" * 64}],
            "selection_reason": "EXACT_OPERATION_BINDING:EXECUTE_AUTHORIZED_TASK",
        },
    }


def _receipt(attempt_id: str = ATTEMPT) -> dict[str, object]:
    return {
        "schema_version": 2,
        "receipt_id": "receipt-1",
        "attempt_id": attempt_id,
        "planning_lite_ref": "v1",
        "model_id": "model-1",
        "agent_role": "PARENT",
        "invocation_index": 0,
        "runtime_source": "test-runtime",
    }


def _observation() -> OperationDepthObservationV1:
    return OperationDepthObservationV1._create(
        operation_ref=ATTEMPT,
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


def _post_entry(*, attempt_id: str = ATTEMPT, with_during: bool = True) -> dict[str, object]:
    entry = record_governed_attempt_evidence(
        "PRE",
        attempt_id,
        operation_guidance_ref="EXECUTE_AUTHORIZED_TASK",
        guidance=_guidance(),
        operation_depth_observation=_observation() if with_during and attempt_id == ATTEMPT else None,
    )
    return record_governed_attempt_evidence(
        "POST",
        attempt_id,
        entry,
        receipt_ref="C:/receipts.jsonl#receipt_id=receipt-1",
        validated_receipt=_receipt(attempt_id),
        next_gate_ref="OWNER_REVIEW_CHANGE2_IMPLEMENTATION",
        next_gate_source_sha256="c" * 64,
    )


def test_f01_is_exact_and_does_not_select_a_route() -> None:
    entry = record_governed_attempt_evidence(
        "PRE",
        ATTEMPT,
        operation_guidance_ref="EXECUTE_AUTHORIZED_TASK",
        guidance=_guidance(),
    )
    assert entry["expected_route_id"] == "CHANGE_EXECUTION_V1"
    assert entry["expected_route_source_revision"] == "a" * 64
    assert "select_operation_guidance" not in repr(entry)


def test_f01_rejects_cross_attempt_and_missing_guidance_fields() -> None:
    with pytest.raises(OperationTraceError):
        record_governed_attempt_evidence(
            "PRE",
            ATTEMPT,
            {"attempt_id": OTHER_ATTEMPT},
            operation_guidance_ref="EXECUTE_AUTHORIZED_TASK",
            guidance=_guidance(),
        )
    malformed = dict(_guidance())
    malformed["operation"] = {"operation_id": "only"}
    with pytest.raises(OperationTraceError):
        record_governed_attempt_evidence(
            "PRE", ATTEMPT, operation_guidance_ref="EXECUTE_AUTHORIZED_TASK", guidance=malformed
        )


def test_f02_uses_one_exact_receipt_lookup_and_rejects_wrong_attempt() -> None:
    pre = record_governed_attempt_evidence(
        "PRE", ATTEMPT, operation_guidance_ref="EXECUTE_AUTHORIZED_TASK", guidance=_guidance()
    )
    post = record_governed_attempt_evidence(
        "POST",
        ATTEMPT,
        pre,
        receipt_ref="C:/receipts.jsonl#receipt_id=receipt-1",
        validated_receipt=_receipt(),
        next_gate_ref="NEXT",
        next_gate_source_sha256="c" * 64,
    )
    looked_up: list[str] = []
    view = read_operation_trace_evidence(post, lambda ref: (looked_up.append(ref) or _receipt()))
    assert view.trace_state == TRACE_PARTIAL
    assert looked_up == ["C:/receipts.jsonl#receipt_id=receipt-1"]
    with pytest.raises(OperationTraceError):
        bind_attempt_run_receipt(
            ATTEMPT,
            "exact",
            _receipt(OTHER_ATTEMPT),
        )


def test_f03_is_historical_and_never_infers_next_action() -> None:
    entry = _post_entry(with_during=False)
    assert entry["next_gate_ref"] == "OWNER_REVIEW_CHANGE2_IMPLEMENTATION"
    assert entry["next_gate_source_ref"] == ".planning/ACTIVE.md#Active change/Next permitted action"
    assert entry["next_gate_source_sha256"] == "c" * 64
    missing = dict(entry)
    del missing["next_gate_ref"]
    view = read_operation_trace_evidence(missing, lambda _: _receipt())
    assert view.trace_state == TRACE_PARTIAL


def test_complete_trace_requires_during_and_all_same_attempt_components() -> None:
    entry = _post_entry()
    view = read_operation_trace_evidence(entry, lambda ref: _receipt())
    assert view.trace_state == TRACE_COMPLETE
    assert view.attempt_id == ATTEMPT
    assert view.reason_codes == ()
    no_during = _post_entry(with_during=False)
    assert read_operation_trace_evidence(no_during, lambda ref: _receipt()).trace_state == TRACE_PARTIAL
    cross = dict(entry)
    cross["during_operation_ref"] = OTHER_ATTEMPT
    with pytest.raises(OperationTraceError):
        read_operation_trace_evidence(cross, lambda ref: _receipt())


def test_old_entry_is_partial_and_raw_content_is_not_accepted() -> None:
    old = {"attempt_id": ATTEMPT, "operation_guidance_ref": "legacy"}
    view = read_operation_trace_evidence(old, lambda ref: _receipt())
    assert view.trace_state == TRACE_PARTIAL
    with pytest.raises(OperationTraceError):
        record_governed_attempt_evidence(
            "PRE", ATTEMPT, operation_guidance_ref="EXECUTE\nraw", guidance=_guidance()
        )


def test_complete_view_is_detached_and_has_no_authority_fields() -> None:
    entry = _post_entry()
    view = read_operation_trace_evidence(entry, lambda ref: _receipt())
    detached = view.to_mapping()
    assert detached["attempt_id"] == ATTEMPT
    assert "next_gate_owner" not in detached
    assert isinstance(detached["f01"], Mapping)


def test_two_attempt_skeletons_never_copy_or_latest_win() -> None:
    b1_pre = record_governed_attempt_evidence(
        "PRE",
        ATTEMPT,
        operation_guidance_ref="EXECUTE_AUTHORIZED_TASK",
        guidance=_guidance(),
        operation_depth_observation=_observation(),
    )
    b1_pre["finding_refs"] = ["F-B1-BLOCKED"]
    b1 = bind_attempt_run_receipt(
        ATTEMPT,
        "C:/receipts.jsonl#receipt_id=receipt-1",
        _receipt(),
        b1_pre,
    )
    b1_view = read_operation_trace_evidence(b1, lambda ref: _receipt())
    assert b1_view.trace_state == TRACE_PARTIAL
    assert b1_view.f03 is None

    b2 = _post_entry(attempt_id=OTHER_ATTEMPT, with_during=False)
    b2_view = read_operation_trace_evidence(b2, lambda ref: _receipt(OTHER_ATTEMPT))
    assert b2_view.attempt_id == OTHER_ATTEMPT
    assert b2["attempt_id"] != b1["attempt_id"]
    assert "finding_refs" not in b2
