from __future__ import annotations

import copy
from dataclasses import replace
import json

import pytest

from planning_lite.execution_guidance import (
    CAPABILITY_IDS,
    PRODUCTION_BINDINGS,
    _select_operation_guidance,
    select_operation_guidance,
    serialize_guidance,
)


def _resume(
    *,
    action: str = "RUN_FORMAL_READINESS",
    lifecycle: str = "Readiness",
    stage_status: str = "In progress",
    authorized: bool = False,
    blocker: str | None = None,
) -> dict:
    return {
        "schema_version": 1,
        "status": "CURRENT",
        "git_identity": {"head": "abc123", "branch": "main"},
        "bootstrap": {
            "project_id": "fixture",
            "active_change": "CHG-1",
            "lifecycle_stage": lifecycle,
            "stage_status": stage_status,
            "implementation_authorized": authorized,
            "open_blocker": blocker,
            "next_permitted_action": action,
            "active_context_path": ".planning/changes/active/CHG-1/context.md",
            "source_revision": "abc123",
        },
        "selected_sources": [
            {"path": ".planning/ACTIVE.md", "sha256": "a" * 64},
            {
                "path": ".planning/changes/active/CHG-1/context.md",
                "sha256": "b" * 64,
            },
        ],
    }


def test_production_candidate_set_is_finite_exact_and_duplicate_free() -> None:
    assert len(PRODUCTION_BINDINGS) == 3
    assert len({item.action_id for item in PRODUCTION_BINDINGS}) == 3
    assert [item.action_id for item in PRODUCTION_BINDINGS] == [
        "RUN_FORMAL_READINESS",
        "EXECUTE_AUTHORIZED_TASK",
        "EXECUTE_AUTHORIZED_CONTRACT_TASK",
    ]


def test_readiness_matches_without_implementation_authorization() -> None:
    result = select_operation_guidance(_resume())
    assert result["outcome"] == "MATCHED"
    assert result["reason_code"] == "EXACT_OPERATION_BINDING"
    assert result["operation"] == {
        "operation_id": "FORMAL_READINESS_AUDIT",
        "operation_class": "FORMAL_READINESS_AUDIT",
        "route_id": "FORMAL_READINESS_V1",
    }
    assert result["authority"]["predicate_result"] == "AUTHORIZED_FOR_THIS_OPERATION"
    assert result["guidance"]["skill_ref"] == ".planning/skills/planning-audit/SKILL.md"


def test_implementation_requires_authorization_but_preserves_route_identity() -> None:
    result = select_operation_guidance(
        _resume(
            action="EXECUTE_AUTHORIZED_TASK",
            lifecycle="Implementation",
            authorized=False,
        )
    )
    assert result["outcome"] == "NOT_AUTHORIZED"
    assert result["reason_code"] == "IMPLEMENTATION_NOT_AUTHORIZED"
    assert result["operation"]["route_id"] == "CHANGE_EXECUTION_V1"
    assert result["guidance"] is None


def test_authorized_implementation_has_bounded_capabilities_not_git_authority() -> None:
    result = select_operation_guidance(
        _resume(
            action="EXECUTE_AUTHORIZED_TASK",
            lifecycle="Implementation",
            authorized=True,
        )
    )
    assert result["outcome"] == "MATCHED"
    capabilities = {item["capability_id"]: item for item in result["capabilities"]}
    assert list(capabilities) == list(CAPABILITY_IDS)
    assert capabilities["PRODUCT_WRITE"]["state"] == "ALLOWED"
    assert capabilities["GIT_STAGE"]["state"] == "REQUIRES_SEPARATE_AUTHORIZATION"
    assert capabilities["GIT_COMMIT"]["state"] == "REQUIRES_SEPARATE_AUTHORIZATION"


def test_contract_route_projects_contract_closure_and_zero_discipline_is_explicit() -> None:
    ordinary = select_operation_guidance(
        _resume(action="EXECUTE_AUTHORIZED_TASK", lifecycle="Execution", authorized=True)
    )
    contract = select_operation_guidance(
        _resume(
            action="EXECUTE_AUTHORIZED_CONTRACT_TASK",
            lifecycle="Execution",
            authorized=True,
        )
    )
    assert ordinary["guidance"]["discipline_refs"] == []
    assert contract["guidance"]["discipline_refs"] == [
        ".planning/disciplines/CONTRACT_CLOSURE.md"
    ]


@pytest.mark.parametrize(
    "action",
    [
        "RUN_PL_V39_07_FORMAL_READINESS",
        "run_formal_readiness",
        "RUN_FORMAL_READINESS_ALIAS",
        "UNKNOWN_ACTION",
    ],
)
def test_nearest_wrong_actions_do_not_alias(action: str) -> None:
    result = select_operation_guidance(_resume(action=action))
    assert result["outcome"] == "NO_APPLICABLE_OPERATION"
    assert result["reason_code"] == "UNMAPPED_OPERATION"


def test_wrong_lifecycle_is_route_prerequisite_failure() -> None:
    result = select_operation_guidance(_resume(lifecycle="Execution"))
    assert result["outcome"] == "NOT_AUTHORIZED"
    assert result["reason_code"] == "ROUTE_PREREQUISITE_NOT_MET"


def test_open_blocker_rejects_implementation_but_readiness_can_audit_it() -> None:
    readiness = select_operation_guidance(_resume(blocker="owner decision required"))
    implementation = select_operation_guidance(
        _resume(
            action="EXECUTE_AUTHORIZED_TASK",
            lifecycle="Implementation",
            authorized=True,
            blocker="owner decision required",
        )
    )
    assert readiness["outcome"] == "MATCHED"
    assert implementation["outcome"] == "NOT_AUTHORIZED"
    assert implementation["reason_code"] == "OPEN_BLOCKER"


def test_invalid_context_precedes_action_selection() -> None:
    result = select_operation_guidance({"schema_version": 1, "status": "STALE"})
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "RESUME_NOT_CURRENT"

    missing_change = _resume()
    del missing_change["bootstrap"]["active_change"]
    assert select_operation_guidance(missing_change)["reason_code"] == "MISSING_ACTIVE_CHANGE"

    missing_context = _resume()
    del missing_context["bootstrap"]["active_context_path"]
    assert select_operation_guidance(missing_context)["reason_code"] == "MISSING_ACTIVE_CONTEXT"


def test_candidate_integrity_and_ambiguity_are_deterministic() -> None:
    context = _resume()
    assert _select_operation_guidance(context, candidates=())["reason_code"] == "UNMAPPED_OPERATION"
    duplicate = (PRODUCTION_BINDINGS[0], PRODUCTION_BINDINGS[0])
    assert _select_operation_guidance(context, candidates=duplicate)["reason_code"] == "INVALID_CANDIDATE_SET"
    too_many = PRODUCTION_BINDINGS + (PRODUCTION_BINDINGS[0],) * 6
    assert _select_operation_guidance(context, candidates=too_many)["reason_code"] == "INVALID_CANDIDATE_SET"
    # Two structurally valid exact entries are needed; duplicate identity is an
    # integrity error, so use the bounded private ambiguity variant.
    ambiguous = (
        PRODUCTION_BINDINGS[0],
        replace(PRODUCTION_BINDINGS[0], route_id="FORMAL_READINESS_V1#AMBIGUOUS_TEST"),
    )
    result = _select_operation_guidance(context, candidates=ambiguous)
    assert result["outcome"] == "AMBIGUOUS_OPERATION"
    assert result["reason_code"] == "MULTIPLE_EXACT_BINDINGS"

    malformed = (replace(PRODUCTION_BINDINGS[0], capabilities=()),)
    malformed_result = _select_operation_guidance(context, candidates=malformed)
    assert malformed_result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert malformed_result["reason_code"] == "INVALID_CAPABILITY_CONTRACT"


@pytest.mark.parametrize(
    "candidate",
    [
        replace(PRODUCTION_BINDINGS[0], route_id="UNDECLARED_ROUTE"),
        replace(PRODUCTION_BINDINGS[0], skill_ref=""),
    ],
)
def test_malformed_binding_fails_before_route_matching(candidate) -> None:
    result = _select_operation_guidance(_resume(), candidates=(candidate,))
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CANDIDATE_SET"


def test_invalid_candidate_precedes_unmapped_action() -> None:
    malformed = replace(PRODUCTION_BINDINGS[0], procedure_ref="")
    result = _select_operation_guidance(
        _resume(action="UNKNOWN_ACTION"), candidates=(malformed,)
    )
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CANDIDATE_SET"


def test_readiness_rejects_implementation_capability_matrix() -> None:
    malformed = replace(
        PRODUCTION_BINDINGS[0], capabilities=PRODUCTION_BINDINGS[1].capabilities
    )
    result = _select_operation_guidance(_resume(), candidates=(malformed,))
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CAPABILITY_CONTRACT"
    assert result["capabilities"] == []


def test_implementation_rejects_contradictory_capability_state() -> None:
    capabilities = list(PRODUCTION_BINDINGS[1].capabilities)
    capabilities[2] = replace(capabilities[2], state="FORBIDDEN")
    malformed = replace(PRODUCTION_BINDINGS[1], capabilities=tuple(capabilities))
    result = _select_operation_guidance(
        _resume(action="EXECUTE_AUTHORIZED_TASK", lifecycle="Implementation", authorized=True),
        candidates=(malformed,),
    )
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CAPABILITY_CONTRACT"


def test_implementation_authorization_precedes_bad_capability_matrix() -> None:
    capabilities = list(PRODUCTION_BINDINGS[1].capabilities)
    capabilities[2] = replace(capabilities[2], state="FORBIDDEN")
    malformed = replace(PRODUCTION_BINDINGS[1], capabilities=tuple(capabilities))
    result = _select_operation_guidance(
        _resume(action="EXECUTE_AUTHORIZED_TASK", lifecycle="Implementation", authorized=False),
        candidates=(malformed,),
    )
    assert result["outcome"] == "NOT_AUTHORIZED"
    assert result["reason_code"] == "IMPLEMENTATION_NOT_AUTHORIZED"


def test_all_production_capability_matrices_remain_exact() -> None:
    readiness = select_operation_guidance(_resume())
    ordinary = select_operation_guidance(
        _resume(action="EXECUTE_AUTHORIZED_TASK", lifecycle="Implementation", authorized=True)
    )
    contract = select_operation_guidance(
        _resume(
            action="EXECUTE_AUTHORIZED_CONTRACT_TASK",
            lifecycle="Implementation",
            authorized=True,
        )
    )
    assert readiness["capabilities"][2]["state"] == "FORBIDDEN"
    assert ordinary["capabilities"][2]["state"] == "ALLOWED"
    assert contract["capabilities"] == ordinary["capabilities"]


@pytest.mark.parametrize(
    "field,value",
    [
        ("route_id", []),
        ("skill_ref", 123),
        ("predicate_id", None),
        ("operation_class", {}),
        ("policy_refs", ("valid-ref", 123)),
        ("discipline_refs", {"invalid": "container"}),
    ],
)
def test_malformed_candidate_types_fail_closed(field: str, value: object) -> None:
    candidate = replace(PRODUCTION_BINDINGS[0], **{field: value})
    result = _select_operation_guidance(_resume(), candidates=(candidate,))
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CANDIDATE_SET"


@pytest.mark.parametrize(
    "field,value",
    [("implementation_required", 0), ("implementation_required", "true")],
)
def test_implementation_required_requires_exact_bool(field: str, value: object) -> None:
    candidate = replace(PRODUCTION_BINDINGS[0], **{field: value})
    result = _select_operation_guidance(_resume(), candidates=(candidate,))
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CANDIDATE_SET"


@pytest.mark.parametrize("value", [1, []])
def test_readiness_route_requires_exact_bool(value: object) -> None:
    candidate = replace(PRODUCTION_BINDINGS[0], readiness_route=value)
    result = _select_operation_guidance(_resume(), candidates=(candidate,))
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CANDIDATE_SET"


def test_malformed_type_precedes_unmapped_action() -> None:
    candidate = replace(PRODUCTION_BINDINGS[0], route_id=[])
    result = _select_operation_guidance(
        _resume(action="UNKNOWN_ACTION"), candidates=(candidate,)
    )
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == "INVALID_CANDIDATE_SET"


def test_result_is_stable_and_prior_result_cannot_authorize() -> None:
    context = _resume(
        action="EXECUTE_AUTHORIZED_TASK", lifecycle="Implementation", authorized=False
    )
    first = select_operation_guidance(context)
    second = select_operation_guidance(copy.deepcopy(context))
    assert serialize_guidance(first) == serialize_guidance(second)
    assert json.loads(serialize_guidance(first)) == first
    context["guidance"] = first
    assert select_operation_guidance(context)["outcome"] == "NOT_AUTHORIZED"


def test_result_arrays_and_guidance_are_contract_complete() -> None:
    result = select_operation_guidance(_resume())
    guidance = result["guidance"]
    assert set(guidance) == {
        "procedure_ref",
        "mode_ref",
        "skill_ref",
        "policy_refs",
        "discipline_refs",
        "task_binding_refs",
        "precondition_refs",
        "scope_refs",
        "verification_refs",
        "result_contract_refs",
        "evidence_refs",
        "stop_condition_refs",
        "escalation_ref",
        "next_gate_ref",
        "next_gate_owner_ref",
    }
    assert set(result) == {
        "schema_version",
        "outcome",
        "reason_code",
        "operation",
        "authority",
        "capabilities",
        "guidance",
        "provenance",
    }


@pytest.mark.parametrize(
    "payload,reason",
    [
        (None, "INVALID_RESUME_CONTEXT"),
        ({}, "INVALID_RESUME_CONTEXT"),
        ({"schema_version": 2, "status": "CURRENT"}, "INVALID_RESUME_CONTEXT"),
    ],
)
def test_malformed_contexts_fail_closed(payload: object, reason: str) -> None:
    result = select_operation_guidance(payload)  # type: ignore[arg-type]
    assert result["outcome"] == "MISSING_OR_UNUSABLE_CONTEXT"
    assert result["reason_code"] == reason
