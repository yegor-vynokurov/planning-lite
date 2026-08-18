from __future__ import annotations

from pathlib import Path


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (_root() / relative).read_text(encoding="utf-8")


def test_pw_dir_006_exists_and_stops_before_roadmap_synthesis() -> None:
    workflow = _read("template/.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md")

    assert "PW-DIR-006" in workflow
    assert "Mode:** Planning" in workflow
    assert "broad recommendation and historical Roadmap reads are intentionally allowed" in workflow
    assert "Historical Roadmap order is prior intent" in workflow
    assert "Do not continue into PL-V38-04" in workflow
    assert "do not rank Gaps" in workflow.lower() or "Do not rank Gaps" in workflow
    assert "create a Change" in workflow


def test_semantic_units_have_stable_ids_states_and_lineage() -> None:
    workflow = _read("template/.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md")
    lifecycle = _read("template/.planning/control/RECOMMENDATION_LIFECYCLE.md")

    assert "REC-NNNN/U1" in workflow
    assert "Never renumber" in workflow
    for state in (
        "IMPLEMENTED",
        "STILL_OPEN",
        "CARRIED_FORWARD",
        "FUTURE_SEED",
        "DEFERRED",
        "REJECTED",
        "SUPERSEDED",
        "NEEDS_REFRAME",
        "UNCERTAIN",
    ):
        assert state in workflow
        assert state in lifecycle
    for lineage in (
        "GAP_ANCHORED",
        "TARGET_STATE_SIGNAL",
        "LOCAL_TACTIC",
        "OPTIONAL_FUTURE",
        "OUTSIDE_BOUNDED_TARGET",
        "UNANCHORED",
    ):
        assert lineage in workflow
        assert lineage in lifecycle


def test_recommendation_lifecycle_separates_status_from_reconciliation_state() -> None:
    lifecycle = _read("template/.planning/control/RECOMMENDATION_LIFECYCLE.md")

    assert "Keep lifecycle `Status` separate from semantic reconciliation" in lifecycle
    assert "Reconciliation review" in lifecycle
    assert "NOT_RECONCILED" in lifecycle
    assert "DRAFT" in lifecycle
    assert "CURRENT" in lifecycle
    for state in (
        "OPEN",
        "COMPLETED",
        "PARTIALLY_REALIZED",
        "CLOSED_WITH_CARRYFORWARD",
        "UNANCHORED",
        "NEEDS_REFRAME",
        "UNCERTAIN",
    ):
        assert state in lifecycle
    assert "does not silently change lifecycle `Status`" in lifecycle


def test_residue_invariant_and_change_completion_boundary_are_explicit() -> None:
    workflow = _read("template/.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md")
    lifecycle = _read("template/.planning/control/RECOMMENDATION_LIFECYCLE.md")
    closure = _read("template/.planning/control/CHANGE_CLOSURE.md")

    invariant = "all original recommendation semantic units are accounted for"
    assert invariant in workflow
    assert invariant in lifecycle
    assert "Change completion != Recommendation completion" in workflow
    assert "Change completion != Recommendation completion" in closure
    assert "leave unrelated units untouched" in closure


def test_change_definition_and_proposal_support_exact_recommendation_units() -> None:
    definition = _read("template/.planning/control/CHANGE_DEFINITION.md")
    proposal = _read("template/.planning/changes/templates/proposal.md")

    assert "Source recommendation units" in definition
    assert "Source recommendation units" in proposal
    assert "rather than implying whole-parent coverage" in definition


def test_reconciliation_assessment_is_runtime_snapshot_not_installed_current_truth() -> None:
    root = _root()
    template = _read("template/.planning/assessments/DIRECTION_HISTORY_RECONCILIATION_TEMPLATE.md")
    workflow = _read("template/.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md")

    assert "DRAFT / CURRENT" in template
    assert "READY_FOR_ROADMAP_SYNTHESIS / BLOCKED" in template
    assert ".planning/assessments/current/DIRECTION_HISTORY_RECONCILIATION.md" in workflow
    assert not (root / "template/.planning/assessments/current/DIRECTION_HISTORY_RECONCILIATION.md").exists()
    assert "explicit user acceptance" in workflow


def test_historical_roadmap_dispositions_do_not_imply_priority() -> None:
    workflow = _read("template/.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md")
    template = _read("template/.planning/assessments/DIRECTION_HISTORY_RECONCILIATION_TEMPLATE.md")

    for disposition in (
        "KEEP",
        "REFRAME",
        "SPLIT",
        "MERGE_CANDIDATE",
        "DEFER",
        "COMPLETE",
        "RETIRE_FROM_BOUNDED_TARGET",
        "UNCERTAIN",
    ):
        assert disposition in workflow
        assert disposition in template
    assert "Historical order is not current priority" in template
    assert "does not select or prioritize" in workflow


def test_reconciliation_runs_orphan_overlap_and_future_seed_checks() -> None:
    workflow = _read("template/.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md")
    template = _read("template/.planning/assessments/DIRECTION_HISTORY_RECONCILIATION_TEMPLATE.md")

    assert "apparently completed/converted recommendations with unresolved semantic units" in workflow
    assert "current Gaps with no direct recommendation lineage" in workflow
    assert "current Gaps with no meaningful historical Roadmap coverage" in workflow
    assert "overlapping/duplicate semantic units" in workflow
    assert "Future-seed register" in template
    assert "no implementation date or priority" in template


def test_reconciliation_is_routed_as_separate_direction_turn() -> None:
    root_router = _read("template/.planning/control/ROOT_ROUTER.md")
    mode_router = _read("template/.planning/control/MODE_ROUTER.md")
    workflow = _read("template/.planning/WORKFLOW.md")
    prompt = _read("template/.planning/prompts/02-refine-project-goal-and-completion-criteria.md")
    context = _read("template/.planning/control/CONTEXT_POLICY.md")

    name = "RECOMMENDATION_HISTORY_RECONCILIATION.md"
    assert name in root_router
    assert name in mode_router
    assert name in workflow
    assert name in prompt
    assert "Stop after the `DRAFT` reconciliation assessment" in prompt
    assert "### Recommendation + historical Roadmap reconciliation" in context
    assert "first direction stage where broad recommendation/Roadmap history is justified" in context


def test_recommendation_template_supports_units_without_invalidating_legacy_capture() -> None:
    template = _read("template/.planning/recommendations/TEMPLATE.md")
    lifecycle = _read("template/.planning/control/RECOMMENDATION_LIFECYCLE.md")
    capture_prompt = _read("template/.planning/prompts/03-capture-or-triage-recommendations.md")

    assert "## Semantic units" in template
    assert "## Residue accounting" in template
    assert "| Change | Unit(s) | Coverage" in template
    assert "legacy/simple form" in lifecycle
    assert "Existing `REC-NNNN/Ux` IDs are stable" in capture_prompt
    assert "Do not run broad Project Spine historical reconciliation" in capture_prompt


def test_reconciliation_snapshot_ownership_is_explicit() -> None:
    state = _read("template/.planning/control/STATE_OWNERSHIP.md")
    model = _read("template/.planning/docs/STATE_MODEL.md")
    assessments = _read("template/.planning/assessments/README.md")

    assert "DIRECTION_HISTORY_RECONCILIATION.md" in state
    assert "not current Roadmap priority" in state
    assert "DIRECTION_HISTORY_RECONCILIATION.md" in model
    assert "DIRECTION_HISTORY_RECONCILIATION_TEMPLATE.md" in assessments
