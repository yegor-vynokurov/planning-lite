from __future__ import annotations

from pathlib import Path


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (_root() / relative).read_text(encoding="utf-8")


def test_pw_dir_007_exists_and_requires_current_spine_and_reconciliation() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")

    assert "PW-DIR-007" in workflow
    assert "Mode:** Planning" in workflow
    assert "TARGET_STATE.md` status = `ACCEPTED`" in workflow
    assert "CAPABILITY_MODEL.md` status = `CURRENT_BASELINE`" in workflow
    assert "CURRENT_CAPABILITY_ASSESSMENT.md` status = `CURRENT`" in workflow
    assert "GAP_MAP.md` status = `CURRENT_BASELINE`" in workflow
    assert "DIRECTION_HISTORY_RECONCILIATION.md` status = `CURRENT`" in workflow
    assert "READY_FOR_ROADMAP_SYNTHESIS" in workflow


def test_roadmap_synthesis_uses_reconciliation_as_history_boundary() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")
    context = _read("template/.planning/control/CONTEXT_POLICY.md")

    assert "reconciliation snapshot as the normal history boundary" in workflow
    assert "Do not reopen broad recommendations" in workflow
    assert "historical Roadmap order != current priority" in workflow
    assert "### Roadmap synthesis + qualitative prioritization" in context
    assert "Historical sequence position is not priority evidence" in context


def test_roadmap_outcomes_are_distinct_from_gaps_and_changes() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")
    roadmap = _read("template/.planning/project/ROADMAP.md")

    for text in (
        "RoadmapOutcome identity != Gap identity != Change identity",
        "one RoadmapOutcome -> several Gap refs is allowed",
        "Gap closure checks remain independent",
        "RoadmapOutcome completion does not automatically close a Gap",
    ):
        assert text in workflow
    assert "RoadmapOutcome != Gap != Change" in roadmap
    assert "Change completion != RoadmapOutcome completion" in roadmap


def test_gap_bundling_requires_one_natural_outcome_not_convenience() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")

    assert "Natural Gap bundling" in workflow
    assert "one natural result, evidence chain, public boundary, or decision boundary" in workflow
    assert "Do **not** bundle merely because Gaps are adjacent" in workflow


def test_prioritization_compares_credible_alternatives_without_fake_precision() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")
    assessment = _read("template/.planning/assessments/ROADMAP_SYNTHESIS_TEMPLATE.md")

    assert "strongest credible alternatives" in workflow
    assert "Do not use a weighted score or fake numeric precision" in workflow
    for criterion in (
        "TARGET_CRITICALITY",
        "GAP_LEVERAGE",
        "DEPENDENCY_LEVERAGE",
        "EVIDENCE_READINESS",
        "BOUNDEDNESS",
        "UNCERTAINTY",
        "PREMATURE_FREEZE_RISK",
    ):
        assert criterion in workflow
        assert criterion in assessment
    assert "Do not total or weight" in assessment


def test_sequence_is_partial_order_not_forced_total_order() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")
    assessment = _read("template/.planning/assessments/ROADMAP_SYNTHESIS_TEMPLATE.md")

    for label in ("NOW", "NEXT", "LATER", "FINAL_GATE", "DEFERRED"):
        assert f"`{label}`" in workflow
        assert f"`{label}`" in assessment
    assert "exactly one preferred open outcome" in workflow
    assert "Do not impose an order among `LATER` outcomes" in workflow
    assert "Do not invent an order among `LATER` outcomes" in assessment


def test_research_heavy_outcomes_can_be_protocol_first_without_forcing_adoption() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")

    assert "protocol-first" in workflow.lower()
    assert "study_complete != production_integrated" in workflow
    assert "synthetic recovery != independent validation" in workflow
    assert "study validity != model result != production disposition" in workflow
    assert "negative or non-adoption result may satisfy" in workflow
    assert "Do not force protocol-first onto routine engineering outcomes" in workflow


def test_roadmap_synthesis_is_snapshot_until_explicit_acceptance() -> None:
    root = _root()
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")
    assessment = _read("template/.planning/assessments/ROADMAP_SYNTHESIS_TEMPLATE.md")

    assert ".planning/assessments/current/ROADMAP_SYNTHESIS.md" in workflow
    assert not (root / "template/.planning/assessments/current/ROADMAP_SYNTHESIS.md").exists()
    assert "assessment status = `DRAFT`" in workflow
    assert "canonical `project/ROADMAP.md` remains unchanged" in workflow
    assert "Only explicit user acceptance authorizes canonical Roadmap mutation" in workflow
    assert "READY_FOR_DIRECTION_ACCEPTANCE / BLOCKED" in assessment


def test_project_roadmap_has_pristine_copy_and_human_baseline_authority() -> None:
    project = _read("template/.planning/project/ROADMAP.md")
    pristine = _read("template/.planning/templates/project/ROADMAP.md")

    assert project == pristine
    assert "CURRENT_BASELINE" in project
    assert "explicit user acceptance" in project
    assert "Current preferred outcome" in project
    assert "Direct Gap refs" in project
    assert "Likely delivery shape" in project


def test_roadmap_acceptance_stops_before_change_definition() -> None:
    workflow = _read("template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md")
    prompt = _read("template/.planning/prompts/02-refine-project-goal-and-completion-criteria.md")

    assert "do not create or activate a Change" in workflow
    assert "Do not continue into `CHANGE_DEFINITION` in the same turn" in workflow
    assert "Do not continue into Change definition in that turn" in prompt


def test_change_definition_consumes_exact_roadmap_gap_and_recommendation_lineage() -> None:
    definition = _read("template/.planning/control/CHANGE_DEFINITION.md")
    proposal = _read("template/.planning/changes/templates/proposal.md")

    assert "Source Roadmap outcome" in proposal
    assert "Roadmap outcome contribution" in proposal
    assert "Source gaps" in proposal
    assert "Source recommendation units" in proposal
    assert "accepted `NOW` outcome" in definition
    assert "partial contribution" in definition
    assert "Change completion != RoadmapOutcome completion" in definition
    assert "Change completion != Gap closure" in definition


def test_change_closure_does_not_auto_complete_roadmap_or_gap() -> None:
    closure = _read("template/.planning/control/CHANGE_CLOSURE.md")
    review = _read("template/.planning/changes/templates/review.md")

    assert "Roadmap / Gap contribution" in closure
    assert "Change completion != RoadmapOutcome completion" in closure
    assert "Change completion != Gap closure" in closure
    assert "does not automatically complete a Roadmap outcome or close a Gap" in review


def test_pw_dir_007_is_routed_and_documented_as_one_turn_operation() -> None:
    root_router = _read("template/.planning/control/ROOT_ROUTER.md")
    mode_router = _read("template/.planning/control/MODE_ROUTER.md")
    workflow_index = _read("template/.planning/WORKFLOW.md")
    prompt = _read("template/.planning/prompts/02-refine-project-goal-and-completion-criteria.md")
    change_prompt = _read("template/.planning/prompts/04-create-approved-change.md")

    name = "ROADMAP_SYNTHESIS_PRIORITIZATION.md"
    assert name in root_router
    assert name in mode_router
    assert name in workflow_index
    assert name in prompt
    assert "one mode and one authoritative workflow per turn" in prompt
    assert "CURRENT_BASELINE` Roadmap" in change_prompt


def test_roadmap_state_ownership_separates_synthesis_evidence_from_canonical_priority() -> None:
    ownership = _read("template/.planning/control/STATE_OWNERSHIP.md")
    state_model = _read("template/.planning/docs/STATE_MODEL.md")
    assessments = _read("template/.planning/assessments/README.md")

    assert "assessments/current/ROADMAP_SYNTHESIS.md" in ownership
    assert "project/ROADMAP.md" in ownership
    assert "not canonical until explicit acceptance" in ownership
    assert "Only an explicitly accepted `project/ROADMAP.md`" in state_model
    assert "ROADMAP_SYNTHESIS_TEMPLATE.md" in assessments


def test_project_state_refresh_cannot_silently_reprioritize_roadmap() -> None:
    refresh = _read("template/.planning/control/PROJECT_STATE_REFRESH.md")

    assert "`ROADMAP.md` is not an ordinary factual refresh target" in refresh
    assert "must not reprioritize outcomes" in refresh
    assert "must not" in refresh and "change the `NOW` outcome" in refresh
    assert "ROADMAP_SYNTHESIS_PRIORITIZATION.md" in refresh
    assert "explicit user acceptance" in refresh
