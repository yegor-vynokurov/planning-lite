from __future__ import annotations

from copy import deepcopy

import pytest

from planning_lite.plan_compilation import (
    CRITERIA,
    PlanCompilationInputError,
    compile_plan,
    parse_task_table,
    serialize_result,
)


TASKS = """# Tasks

| ID | Outcome | Slice type | Blocking edge | Verification seam / command | Blast radius | Status |
|---|---|---|---|---|---|---|
| `T-01` | first | unit | `None` | test first | low | `Pending` |
| `T-02` | second | unit | `T-01` | test second | low | `Pending` |
| `T-03` | sibling | unit | `T-01` | test sibling | low | `Pending` |
"""


def _coverage() -> list[dict[str, object]]:
    return [
        {
            "criterion": criterion,
            "verdict": "PASS",
            "reason": f"bounded {criterion}",
            "evidence_refs": [f"E-{criterion}"],
        }
        for criterion in CRITERIA
    ]


def _unit(unit_id: str, *, disposition: str = "KEEP_UNIT", **overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "original_unit_id": unit_id,
        "work_capabilities": ["REPOSITORY_UNDERSTANDING"],
        "cross_cutting_tags": [],
        "target_executor_profile": "BOUNDED_WORKER",
        "already_decided": [],
        "allowed_executor_decisions": ["inspect"],
        "forbidden_executor_decisions": ["mutate"],
        "disposition": disposition,
        "derived_units": [],
        "new_internal_edges": [],
        "internal_handoffs": [],
        "criterion_assertions": _coverage(),
        "material_findings": [],
    }
    value.update(overrides)
    return value


def _derived(
    unit_id: str,
    *,
    outcome: str | None = None,
    work_capabilities: list[str] | None = None,
    cross_cutting_tags: list[str] | None = None,
    target_executor_profile: str = "BOUNDED_WORKER",
    already_decided: list[object] | None = None,
    allowed_executor_decisions: list[str] | None = None,
    forbidden_executor_decisions: list[str] | None = None,
    criterion_assertions: list[dict[str, object]] | None = None,
    material_findings: list[object] | None = None,
) -> dict[str, object]:
    return {
        "unit_id": unit_id,
        "outcome": outcome or f"bounded outcome {unit_id}",
        "work_capabilities": work_capabilities or ["REPOSITORY_UNDERSTANDING"],
        "cross_cutting_tags": cross_cutting_tags or [],
        "target_executor_profile": target_executor_profile,
        "already_decided": already_decided if already_decided is not None else [],
        "allowed_executor_decisions": allowed_executor_decisions or ["inspect"],
        "forbidden_executor_decisions": forbidden_executor_decisions or ["mutate"],
        "criterion_assertions": criterion_assertions or _coverage(),
        "material_findings": material_findings or [],
    }


def _split_proposal(
    *,
    derived_units: list[dict[str, object]] | None = None,
    new_internal_edges: list[dict[str, str]] | None = None,
    internal_handoffs: list[dict[str, object]] | None = None,
    parent_overrides: dict[str, object] | None = None,
    tasks: str = TASKS,
) -> dict[str, object]:
    derived = derived_units or [
        _derived("T-01-A", work_capabilities=["REPOSITORY_UNDERSTANDING"], target_executor_profile="STRONG_AUTONOMOUS"),
        _derived("T-01-B", work_capabilities=["VERIFICATION_TEST_DESIGN"], target_executor_profile="BOUNDED_WORKER", allowed_executor_decisions=["verify"]),
    ]
    parent = _unit(
        "T-01",
        disposition="SPLIT_RECOMMENDED",
        work_capabilities=[capability for item in derived for capability in item["work_capabilities"]],
        already_decided=[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 7)],
        derived_units=derived,
        new_internal_edges=new_internal_edges if new_internal_edges is not None else [{"source": "T-01-A", "target": "T-01-B"}],
        internal_handoffs=internal_handoffs if internal_handoffs is not None else [_handoff("T-01-A", "T-01-B")],
    )
    if parent_overrides:
        parent.update(parent_overrides)
    return _proposal(units=[parent, _unit("T-02"), _unit("T-03")], tasks=tasks)


def _handoff(source: str, target: str) -> dict[str, object]:
    return {
        "source_unit": source,
        "target_unit": target,
        "produced_refs": ["answer"],
        "accepted_output_contract": "bounded answer",
        "required_downstream_inputs": ["answer"],
        "authority_constraints": "no authority",
        "allowed_open_questions": [],
        "forbidden_decisions": ["routing"],
        "verification_evidence": ["E-SPLIT"],
        "failure_stop_state": "stop",
    }


def _proposal(
    *,
    units: list[dict[str, object]] | None = None,
    tasks: str = TASKS,
    controlled_discoveries: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    task_graph = parse_task_table(tasks)
    return {
        "schema_version": 1,
        "source_binding": {
            "plan_ref": "plan.md",
            "plan_sha256": "a" * 64,
            "tasks_ref": "tasks.md",
            "tasks_sha256": "b" * 64,
        },
        "units": units or [_unit(task.task_id) for task in task_graph.units],
        "existing_dependency_handoffs": [],
        "controlled_discoveries": controlled_discoveries if controlled_discoveries is not None else [],
        "semantic_assessment_source": "semantic planner assertion",
        "semantic_evidence_refs": ["EVIDENCE-1"],
    }


def _compile(proposal: dict[str, object], *, tasks: str = TASKS) -> dict[str, object]:
    return compile_plan(
        tasks,
        proposal,
        source_binding=proposal["source_binding"],
        proposal_sha256="c" * 64,
    )


def _discovery(unit_ref: str = "T-01") -> dict[str, object]:
    return {
        "unit_ref": unit_ref,
        "question": "Which bounded input is missing?",
        "scope_bound": "Inspect only the named repository interface.",
        "stop_condition": "Stop after one verified answer.",
        "output_contract": "Return one evidence reference and a concise answer.",
        "verification_before_dependent_work": "Verify the answer against the named source.",
    }


def test_simple_graph_and_deterministic_parse() -> None:
    graph = parse_task_table(TASKS)
    assert [unit.task_id for unit in graph.units] == ["T-01", "T-02", "T-03"]
    assert graph.edges == (("T-01", "T-02"), ("T-01", "T-03"))
    assert parse_task_table(TASKS) == graph


def test_multi_edge_dag_and_parallel_siblings_are_preserved() -> None:
    text = TASKS.replace(
        "| `T-03` | sibling | unit | `T-01`",
        "| `T-03` | sibling | unit | `T-01, T-02`",
    )
    graph = parse_task_table(text)
    assert graph.edges == (("T-01", "T-02"), ("T-01", "T-03"), ("T-02", "T-03"))


@pytest.mark.parametrize(
    ("blocking_edge", "code"),
    [
        ("T-01, T-99", "UNKNOWN_DEPENDENCY_TASK"),
        ("T-01 / T-02", "UNSUPPORTED_TASK_GRAPH_GRAMMAR"),
        ("T-01 + T-02", "UNSUPPORTED_TASK_GRAPH_GRAMMAR"),
        ("T-01..T-03", "UNSUPPORTED_TASK_GRAPH_GRAMMAR"),
        ("prose", "UNSUPPORTED_TASK_GRAPH_GRAMMAR"),
    ],
)
def test_blocking_edge_grammar_fails_closed(blocking_edge: str, code: str) -> None:
    text = TASKS.replace("| `T-02` | second | unit | `T-01`", f"| `T-02` | second | unit | `{blocking_edge}`")
    with pytest.raises(PlanCompilationInputError) as error:
        parse_task_table(text)
    assert error.value.code == code


@pytest.mark.parametrize(
    ("text", "code"),
    [
        (TASKS.replace("`T-03`", "`T-02`"), "DUPLICATE_TASK_ID"),
        (TASKS.replace("`T-01` | test second", "`T-99` | test second"), "UNKNOWN_DEPENDENCY_TASK"),
        (TASKS.replace("| `T-01` | first | unit | `None`", "| `T-01` | first | unit | `T-01`"), "SELF_DEPENDENCY"),
        (TASKS.replace("| `T-01` | first | unit | `None`", "| `T-01` | first | unit | `T-02`").replace("| `T-02` | second | unit | `T-01`", "| `T-02` | second | unit | `T-01`"), "TASK_GRAPH_CYCLE"),
    ],
)
def test_task_graph_negative_cases(text: str, code: str) -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        parse_task_table(text)
    assert error.value.code == code


def test_cancelled_task_is_parsed_but_blocks_executor_readiness() -> None:
    text = TASKS.replace("`Pending`", "`Cancelled`", 1)
    proposal = _proposal(tasks=text)
    result = _compile(proposal, tasks=text)
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "UNSUPPORTED_CANCELLED_TASK_STATE" in {finding["finding_code"] for finding in result["findings"]}


def test_empty_discovery_can_be_executor_ready() -> None:
    result = _compile(_proposal())
    assert result["readiness"] == "EXECUTOR_READY"
    assert result["controlled_discoveries"] == []
    assert result["findings"] == []


def test_capability_coupled_discovery_is_ready_with_bounded_discovery() -> None:
    proposal = _proposal(
        units=[_unit("T-01", disposition="CAPABILITY_COUPLED"), _unit("T-02"), _unit("T-03")],
        controlled_discoveries=[_discovery()],
    )
    result = _compile(proposal)
    assert result["readiness"] == "EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY"


def test_true_split_has_derived_unit_and_typed_handoff() -> None:
    handoff = _handoff("T-01-A", "T-01-B")
    units = [
        _unit(
            "T-01",
            disposition="SPLIT_RECOMMENDED",
            work_capabilities=["REPOSITORY_UNDERSTANDING", "VERIFICATION_TEST_DESIGN"],
            already_decided=[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 7)],
            derived_units=[
                _derived("T-01-A", work_capabilities=["REPOSITORY_UNDERSTANDING"], target_executor_profile="STRONG_AUTONOMOUS"),
                _derived("T-01-B", work_capabilities=["VERIFICATION_TEST_DESIGN"], target_executor_profile="BOUNDED_WORKER", allowed_executor_decisions=["verify"]),
            ],
            new_internal_edges=[{"source": "T-01-A", "target": "T-01-B"}],
            internal_handoffs=[handoff],
        ),
        _unit("T-02"),
        _unit("T-03"),
    ]
    result = _compile(_proposal(units=units, controlled_discoveries=[_discovery("T-01-B")]))
    assert result["readiness"] == "EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY"
    assert [unit["unit_ref"] for unit in result["compiled_units"]] == ["T-01-A", "T-01-B", "T-02", "T-03"]
    assert result["internal_split_handoffs"] == [handoff]


def test_m01_parent_s1_s6_pass_with_empty_derived_assertions_is_ready() -> None:
    result = _compile(_split_proposal())
    assert result["readiness"] == "EXECUTOR_READY"
    assert [unit["already_decided"] for unit in result["compiled_units"][:2]] == [[], []]


def test_m02_parent_missing_s_assertion_is_not_ready() -> None:
    result = _compile(
        _split_proposal(
            parent_overrides={
                "already_decided": [{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 6)]
            }
        )
    )
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "INVALID_SPLIT_STRUCTURE" in {finding["finding_code"] for finding in result["findings"]}


def test_m03_parent_fail_assertion_is_not_ready() -> None:
    result = _compile(
        _split_proposal(
            parent_overrides={
                "already_decided": [
                    {"assertion": "S1", "verdict": "FAIL"},
                    *[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(2, 7)],
                ]
            }
        )
    )
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "INVALID_SPLIT_STRUCTURE" in {finding["finding_code"] for finding in result["findings"]}


def test_m04_parent_duplicate_s_identity_is_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(
            _split_proposal(
                parent_overrides={
                    "already_decided": [
                        {"assertion": "S1", "verdict": "FAIL"},
                        {"assertion": "S1", "verdict": "PASS"},
                        *[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(2, 7)],
                    ]
                }
            )
        )
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_m05_empty_derived_assertions_are_valid_without_s1_s6() -> None:
    result = _compile(
        _split_proposal(
            derived_units=[
                _derived("T-01-A", target_executor_profile="STRONG_AUTONOMOUS"),
                _derived(
                    "T-01-B",
                    work_capabilities=["VERIFICATION_TEST_DESIGN"],
                    target_executor_profile="BOUNDED_WORKER",
                    allowed_executor_decisions=["verify"],
                ),
            ]
        )
    )
    assert result["readiness"] == "EXECUTOR_READY"
    assert all(unit["already_decided"] == [] for unit in result["compiled_units"][:2])


def test_m06_derived_s1_s6_is_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(
            _split_proposal(
                derived_units=[
                    _derived("T-01-A", already_decided=[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 7)]),
                    _derived("T-01-B", work_capabilities=["VERIFICATION_TEST_DESIGN"]),
                ]
            )
        )
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_m07_derived_split_assertion_is_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(
            _split_proposal(
                derived_units=[
                    _derived("T-01-A", already_decided=[{"assertion": "S1", "verdict": "PASS"}]),
                    _derived("T-01-B", work_capabilities=["VERIFICATION_TEST_DESIGN"]),
                ]
            )
        )
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_m08_empty_derived_assertions_preserve_split_handoff_guards() -> None:
    result = _compile(_split_proposal(internal_handoffs=[_handoff("T-01-B", "T-01-A")]))
    codes = {finding["finding_code"] for finding in result["findings"]}
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "HANDOFF_EDGE_MISMATCH" in codes
    assert "MISSING_REQUIRED_HANDOFF" in codes
    assert all(unit["already_decided"] == [] for unit in result["compiled_units"][:2])


def test_c01_derived_units_have_distinct_outcomes() -> None:
    result = _compile(
        _split_proposal(
            derived_units=[
                _derived("T-01-A", outcome="same outcome", target_executor_profile="STRONG_AUTONOMOUS"),
                _derived("T-01-B", outcome="same outcome", work_capabilities=["VERIFICATION_TEST_DESIGN"], target_executor_profile="BOUNDED_WORKER", allowed_executor_decisions=["verify"]),
            ]
        )
    )
    assert "DUPLICATE_DERIVED_OUTCOME" in {finding["finding_code"] for finding in result["findings"]}


def test_c02_derived_units_have_distinct_capability_signatures() -> None:
    result = _compile(
        _split_proposal(
            derived_units=[
                _derived("T-01-A", work_capabilities=["REPOSITORY_UNDERSTANDING"], target_executor_profile="STRONG_AUTONOMOUS"),
                _derived("T-01-B", work_capabilities=["REPOSITORY_UNDERSTANDING"], target_executor_profile="BOUNDED_WORKER", allowed_executor_decisions=["verify"]),
            ]
        )
    )
    assert "DUPLICATE_DERIVED_CAPABILITY_SIGNATURE" in {finding["finding_code"] for finding in result["findings"]}


def test_c03_derived_units_have_distinct_profiles_and_decision_envelopes() -> None:
    result = _compile(
        _split_proposal(
            derived_units=[
                _derived("T-01-A", target_executor_profile="STRONG_AUTONOMOUS"),
                _derived("T-01-B", work_capabilities=["VERIFICATION_TEST_DESIGN"], target_executor_profile="STRONG_AUTONOMOUS"),
            ]
        )
    )
    codes = {finding["finding_code"] for finding in result["findings"]}
    assert "DUPLICATE_DERIVED_EXECUTOR_PROFILE" in codes
    assert "DUPLICATE_DERIVED_DECISION_ENVELOPE" in codes


def test_c04_derived_capability_union_preserves_parent_set_exactly() -> None:
    result = _compile(
        _split_proposal(
            parent_overrides={"work_capabilities": ["REPOSITORY_UNDERSTANDING", "IMPLEMENTATION"]}
        )
    )
    assert "CAPABILITY_UNION_MISMATCH" in {finding["finding_code"] for finding in result["findings"]}


def test_c05_derived_tag_union_preserves_parent_set_exactly() -> None:
    result = _compile(
        _split_proposal(parent_overrides={"cross_cutting_tags": ["LONG_CONTEXT_SYNTHESIS"]})
    )
    assert "TAG_UNION_MISMATCH" in {finding["finding_code"] for finding in result["findings"]}


def test_c06_reverse_handoff_cannot_reach_ready() -> None:
    result = _compile(_split_proposal(internal_handoffs=[_handoff("T-01-B", "T-01-A")]))
    codes = {finding["finding_code"] for finding in result["findings"]}
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "HANDOFF_EDGE_MISMATCH" in codes
    assert "MISSING_REQUIRED_HANDOFF" in codes


def test_c07_every_internal_edge_has_one_matching_handoff() -> None:
    result = _compile(_split_proposal())
    assert result["readiness"] == "EXECUTOR_READY"
    assert "MISSING_REQUIRED_HANDOFF" not in {finding["finding_code"] for finding in result["findings"]}


def test_c08_handoff_without_edge_is_rejected() -> None:
    result = _compile(_split_proposal(new_internal_edges=[], internal_handoffs=[_handoff("T-01-A", "T-01-B")]))
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "HANDOFF_EDGE_MISMATCH" in {finding["finding_code"] for finding in result["findings"]}


def test_c09_duplicate_contradictory_s1_cannot_be_masked() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(
            _split_proposal(
                parent_overrides={
                    "already_decided": [
                        {"assertion": "S1", "verdict": "FAIL"},
                        {"assertion": "S1", "verdict": "PASS"},
                        *[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(2, 7)],
                    ]
                }
            )
        )
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_c10_malformed_allowed_decision_is_bounded_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(_proposal(units=[_unit("T-01", allowed_executor_decisions=[{}]), _unit("T-02"), _unit("T-03")]))
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_c11_malformed_forbidden_decision_is_bounded_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(_proposal(units=[_unit("T-01", forbidden_executor_decisions=[{}]), _unit("T-02"), _unit("T-03")]))
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_c16_reversed_textual_multi_edge_order_is_canonicalized() -> None:
    forward_tasks = TASKS.replace(
        "| `T-03` | sibling | unit | `T-01`",
        "| `T-03` | sibling | unit | `T-01, T-02`",
    )
    reverse_tasks = forward_tasks.replace("`T-01, T-02`", "`T-02, T-01`")
    forward = _compile(_proposal(tasks=forward_tasks), tasks=forward_tasks)
    reverse = _compile(_proposal(tasks=reverse_tasks), tasks=reverse_tasks)
    assert forward["original_graph"] == reverse["original_graph"]
    assert forward["compiled_graph"] == reverse["compiled_graph"]


def test_p01_derived_decision_envelopes_must_be_disjoint() -> None:
    result = _compile(
        _split_proposal(
            derived_units=[
                _derived(
                    "T-01-A",
                    allowed_executor_decisions=["inspect"],
                    forbidden_executor_decisions=["inspect"],
                    target_executor_profile="STRONG_AUTONOMOUS",
                ),
                _derived(
                    "T-01-B",
                    work_capabilities=["VERIFICATION_TEST_DESIGN"],
                    target_executor_profile="BOUNDED_WORKER",
                    allowed_executor_decisions=["verify"],
                ),
            ]
        )
    )
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "EXECUTOR_PROFILE_MISMATCH" in {finding["finding_code"] for finding in result["findings"]}


def test_p02_keep_unit_preserves_decision_note() -> None:
    result = _compile(_proposal(units=[_unit("T-01", already_decided=["keep this bounded decision"]), _unit("T-02"), _unit("T-03")]))
    assert result["readiness"] == "EXECUTOR_READY"
    assert result["compiled_units"][0]["already_decided"] == ["keep this bounded decision"]


def test_p03_capability_coupled_preserves_decision_note() -> None:
    result = _compile(
        _proposal(
            units=[
                _unit("T-01", disposition="CAPABILITY_COUPLED", already_decided=["coupling decision"]),
                _unit("T-02"),
                _unit("T-03"),
            ]
        )
    )
    assert result["readiness"] == "EXECUTOR_READY"
    assert result["compiled_units"][0]["already_decided"] == ["coupling decision"]


def test_p04_split_parent_note_does_not_interfere_with_s_assertions() -> None:
    result = _compile(
        _split_proposal(
            parent_overrides={
                "already_decided": [
                    "split parent decision",
                    *[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 7)],
                ]
            }
        )
    )
    assert result["readiness"] == "EXECUTOR_READY"


def test_p05_decision_notes_do_not_count_toward_s_assertion_completeness() -> None:
    result = _compile(
        _split_proposal(
            parent_overrides={
                "already_decided": [
                    "note one",
                    "note two",
                    *[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 6)],
                ]
            }
        )
    )
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "INVALID_SPLIT_STRUCTURE" in {finding["finding_code"] for finding in result["findings"]}


def test_p06_split_assertion_on_keep_unit_is_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(
            _proposal(
                units=[
                    _unit("T-01", already_decided=[{"assertion": "S1", "verdict": "PASS"}]),
                    _unit("T-02"),
                    _unit("T-03"),
                ]
            )
        )
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_p07_split_assertion_on_derived_unit_is_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(
            _split_proposal(
                derived_units=[
                    _derived("T-01-A", already_decided=[{"assertion": "S1", "verdict": "PASS"}]),
                    _derived("T-01-B", work_capabilities=["VERIFICATION_TEST_DESIGN"]),
                ]
            )
        )
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_p08_derived_decision_note_is_preserved() -> None:
    result = _compile(
        _split_proposal(
            derived_units=[
                _derived("T-01-A", already_decided=["derived bounded decision"], target_executor_profile="STRONG_AUTONOMOUS"),
                _derived(
                    "T-01-B",
                    work_capabilities=["VERIFICATION_TEST_DESIGN"],
                    target_executor_profile="BOUNDED_WORKER",
                    allowed_executor_decisions=["verify"],
                ),
            ]
        )
    )
    assert result["readiness"] == "EXECUTOR_READY"
    assert result["compiled_units"][0]["already_decided"] == ["derived bounded decision"]


def test_p09_duplicate_parent_s_identity_is_schema_error() -> None:
    with pytest.raises(PlanCompilationInputError) as error:
        _compile(
            _split_proposal(
                parent_overrides={
                    "already_decided": [
                        {"assertion": "S1", "verdict": "FAIL"},
                        {"assertion": "S1", "verdict": "PASS"},
                        *[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(2, 7)],
                    ]
                }
            )
        )
    assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_p10_missing_parent_s_is_structurally_not_ready() -> None:
    result = _compile(
        _split_proposal(
            parent_overrides={
                "already_decided": [{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 6)]
            }
        )
    )
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "INVALID_SPLIT_STRUCTURE" in {finding["finding_code"] for finding in result["findings"]}


def test_p11_parent_s_na_is_structurally_not_ready() -> None:
    result = _compile(
        _split_proposal(
            parent_overrides={
                "already_decided": [
                    {"assertion": "S1", "verdict": "N/A"},
                    *[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(2, 7)],
                ]
            }
        )
    )
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "INVALID_SPLIT_STRUCTURE" in {finding["finding_code"] for finding in result["findings"]}


def test_p12_criterion_na_is_valid_complete_coverage() -> None:
    coverage = _coverage()
    coverage[6] = {**coverage[6], "verdict": "N/A"}
    result = _compile(_proposal(units=[_unit("T-01", criterion_assertions=coverage), _unit("T-02"), _unit("T-03")]))
    assert result["readiness"] == "EXECUTOR_READY"


def test_p13_criterion_fail_blocks_readiness() -> None:
    coverage = _coverage()
    coverage[6] = {**coverage[6], "verdict": "FAIL"}
    result = _compile(_proposal(units=[_unit("T-01", criterion_assertions=coverage), _unit("T-02"), _unit("T-03")]))
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "UNRESOLVED_MATERIAL_FINDING" in {finding["finding_code"] for finding in result["findings"]}


@pytest.mark.parametrize("variant", ["unknown", "duplicate"])
def test_p14_unknown_or_duplicate_criterion_is_not_ready(variant: str) -> None:
    coverage = _coverage()
    if variant == "unknown":
        coverage[0] = {**coverage[0], "criterion": "C99"}
    else:
        coverage[1] = {**coverage[1], "criterion": "C01"}
    result = _compile(_proposal(units=[_unit("T-01", criterion_assertions=coverage), _unit("T-02"), _unit("T-03")]))
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "INVALID_CRITERION_VALUE" in {finding["finding_code"] for finding in result["findings"]}


def test_p15_malformed_criterion_assertion_is_schema_error() -> None:
    for malformed in ([{"criterion": "C01"}], ["not an object"]):
        with pytest.raises(PlanCompilationInputError) as error:
            _compile(
                _proposal(
                    units=[
                        _unit("T-01", criterion_assertions=malformed),
                        _unit("T-02"),
                        _unit("T-03"),
                    ]
                )
            )
        assert error.value.code == "PROPOSAL_SCHEMA_INVALID"


def test_existing_edge_handoff_does_not_change_graph() -> None:
    handoff = {
        "source_unit": "T-01",
        "target_unit": "T-02",
        "produced_refs": ["result"],
        "accepted_output_contract": "result",
        "required_downstream_inputs": ["result"],
        "authority_constraints": "none",
        "allowed_open_questions": [],
        "forbidden_decisions": [],
        "verification_evidence": ["E-EDGE"],
        "failure_stop_state": "stop",
    }
    proposal = _proposal()
    proposal["existing_dependency_handoffs"] = [handoff]
    result = _compile(proposal)
    assert result["findings"] == []
    assert [unit["id"] for unit in result["original_graph"]["units"]] == result["compiled_graph"]["units"]
    assert result["original_graph"]["edges"] == result["compiled_graph"]["edges"]
    assert result["existing_edge_handoffs"] == [handoff]


def test_false_split_and_profile_contradiction_block_readiness() -> None:
    units = [
        _unit(
            "T-01",
            disposition="SPLIT_RECOMMENDED",
            derived_units=[_derived("T-01-A")],
            allowed_executor_decisions=["inspect"],
            forbidden_executor_decisions=["inspect"],
        ),
        _unit("T-02"),
        _unit("T-03"),
    ]
    result = _compile(_proposal(units=units))
    codes = {finding["finding_code"] for finding in result["findings"]}
    assert "FALSE_CAPABILITY_SPLIT" in codes
    assert "EXECUTOR_PROFILE_MISMATCH" in codes
    assert result["readiness"] == "EXECUTOR_NOT_READY"


def test_source_binding_and_coverage_failures_are_explicit() -> None:
    proposal = _proposal()
    incomplete = deepcopy(proposal["units"][0])
    incomplete["criterion_assertions"] = _coverage()[:-1]
    proposal["units"][0] = incomplete
    mismatch = compile_plan(
        TASKS,
        proposal,
        source_binding={**proposal["source_binding"], "tasks_sha256": "d" * 64},
        proposal_sha256="c" * 64,
    )
    assert "SOURCE_IDENTITY_MISMATCH" in {finding["finding_code"] for finding in mismatch["findings"]}
    result = _compile(proposal)
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert any(finding["finding_code"] == "COVERAGE_INCOMPLETE" for finding in result["findings"])


@pytest.mark.parametrize(
    "discovery,code",
    [
        ({"unit_ref": "T-99", **_discovery("T-99")}, "UNKNOWN_CONTROLLED_DISCOVERY_UNIT"),
        ({**_discovery(), "question": "  "}, "INVALID_CONTROLLED_DISCOVERY"),
        ({**_discovery(), "extra": "reject"}, "INVALID_CONTROLLED_DISCOVERY"),
        ({"unit_ref": "T-01", "question": "missing remaining fields"}, "INVALID_CONTROLLED_DISCOVERY"),
    ],
)
def test_controlled_discovery_validation(discovery: dict[str, object], code: str) -> None:
    result = _compile(_proposal(controlled_discoveries=[discovery]))
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert code in {finding["finding_code"] for finding in result["findings"]}


def test_duplicate_controlled_discovery_is_rejected() -> None:
    result = _compile(_proposal(controlled_discoveries=[_discovery(), _discovery()]))
    assert result["readiness"] == "EXECUTOR_NOT_READY"
    assert "DUPLICATE_CONTROLLED_DISCOVERY_UNIT" in {finding["finding_code"] for finding in result["findings"]}


def test_valid_discovery_plus_material_finding_is_not_ready() -> None:
    units = [_unit("T-01", material_findings=["UNRESOLVED_MATERIAL_FINDING"]), _unit("T-02"), _unit("T-03")]
    result = _compile(_proposal(units=units, controlled_discoveries=[_discovery()]))
    assert result["readiness"] == "EXECUTOR_NOT_READY"


def test_replaced_split_parent_cannot_carry_discovery() -> None:
    units = [
        _unit(
            "T-01",
            disposition="SPLIT_RECOMMENDED",
            work_capabilities=["REPOSITORY_UNDERSTANDING", "VERIFICATION_TEST_DESIGN"],
            already_decided=[{"assertion": f"S{i}", "verdict": "PASS"} for i in range(1, 7)],
            derived_units=[
                _derived("T-01-A", work_capabilities=["REPOSITORY_UNDERSTANDING"], target_executor_profile="STRONG_AUTONOMOUS"),
                _derived("T-01-B", work_capabilities=["VERIFICATION_TEST_DESIGN"], target_executor_profile="BOUNDED_WORKER", allowed_executor_decisions=["verify"]),
            ],
            new_internal_edges=[{"source": "T-01-A", "target": "T-01-B"}],
            internal_handoffs=[],
        ),
        _unit("T-02"),
        _unit("T-03"),
    ]
    result = _compile(_proposal(units=units, controlled_discoveries=[_discovery("T-01")]))
    assert "UNKNOWN_CONTROLLED_DISCOVERY_UNIT" in {finding["finding_code"] for finding in result["findings"]}


def test_proposal_cannot_supply_or_override_readiness() -> None:
    proposal = _proposal()
    proposal["readiness"] = "EXECUTOR_READY"
    with pytest.raises(PlanCompilationInputError):
        _compile(proposal)


def test_result_serialization_is_byte_deterministic() -> None:
    result = _compile(_proposal())
    assert serialize_result(result) == serialize_result(_compile(_proposal()))
    assert serialize_result(result).endswith("\n")
    assert '": "' not in serialize_result(result)
