from __future__ import annotations

from pathlib import Path

from planning_lite.cli import _iter_required_paths


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (_root() / relative).read_text(encoding="utf-8")


def test_gap_map_has_matching_pristine_copy_and_existing_ownership_boundary() -> None:
    root = _root()
    project = _read("template/.planning/project/GAP_MAP.md")
    pristine = _read("template/.planning/templates/project/GAP_MAP.md")

    assert project == pristine
    assert "CURRENT_BASELINE" in project
    assert "explicit user acceptance" in project.lower()
    assert "Change does not close a Gap automatically" in project
    assert ".planning/project/**" in _read("template/.planning/framework/OWNERSHIP.yml")


def test_current_capability_assessment_is_a_snapshot_not_a_project_truth_file() -> None:
    root = _root()
    workflow = _read("template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md")
    template = _read("template/.planning/assessments/CURRENT_CAPABILITY_ASSESSMENT_TEMPLATE.md")

    assert "PW-DIR-004" in workflow
    assert ".planning/assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md" in workflow
    assert not (root / "template/.planning/assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md").exists()
    assert "Formal-Gap derivation readiness" in template
    assert "Canonical assessment statuses: `DRAFT`, `CURRENT`" in template
    assert "Coverage" in template
    assert "EvidenceConfidence" in template


def test_current_capability_assessment_keeps_coverage_and_confidence_independent() -> None:
    workflow = _read("template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md")

    for value in ("SATISFIED", "PARTIAL", "NOT_SATISFIED", "UNCERTAIN"):
        assert value in workflow
    for value in ("HIGH", "MEDIUM", "LOW"):
        assert value in workflow
    assert "Coverage != EvidenceConfidence" in workflow
    assert "satisfied target properties" in workflow
    assert "missing target properties" in workflow
    assert "evidence limitations" in workflow
    assert "evidence limitation alone is not recorded as a missing Target property" in workflow


def test_formal_assessment_requires_accepted_target_and_capability_baseline() -> None:
    workflow = _read("template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md")

    assert "TARGET_STATE status = ACCEPTED" in workflow
    assert "CAPABILITY_MODEL status = CURRENT_BASELINE" in workflow
    assert "explicit acceptance evidence" in workflow
    assert "TARGET_STATE_SIGNAL" in workflow
    assert "`CURRENT` assessment status" in workflow
    assert "do not derive or imply formal Gaps" in workflow


def test_gap_derivation_is_causal_and_does_not_turn_uncertainty_into_gap() -> None:
    workflow = _read("template/.planning/control/CAUSAL_GAP_DERIVATION.md")

    assert "PW-DIR-005" in workflow
    assert "causal missing condition" in workflow
    assert "evidence limitation != automatic Gap" in workflow
    assert "do not mint a Gap" in workflow
    assert "Causal compression" in workflow
    assert "PRIMARY" in workflow
    assert "DEPENDENT" in workflow
    assert "SATISFIED" in workflow


def test_gap_identity_closure_and_human_authority_are_preserved() -> None:
    workflow = _read("template/.planning/control/CAUSAL_GAP_DERIVATION.md")

    assert "Change completion != Gap closure" in workflow
    assert "Gap identity remains distinct from RoadmapOutcome and Change identity" in workflow
    assert "outcome-oriented" in workflow
    assert "CURRENT_BASELINE" in workflow
    assert "explicit user authority" in workflow
    assert "Individual newly derived Gaps start `OPEN`" in workflow


def test_pl_v38_02_workflows_are_routed_as_separate_turns() -> None:
    root_router = _read("template/.planning/control/ROOT_ROUTER.md")
    mode_router = _read("template/.planning/control/MODE_ROUTER.md")
    workflow = _read("template/.planning/WORKFLOW.md")
    prompt = _read("template/.planning/prompts/02-refine-project-goal-and-completion-criteria.md")

    for name in ("CURRENT_CAPABILITY_ASSESSMENT.md", "CAUSAL_GAP_DERIVATION.md"):
        assert name in root_router
        assert name in mode_router
        assert name in workflow
        assert name in prompt
    assert "one mode and one authoritative workflow per turn" in prompt
    assert "Stop after the evidence snapshot/readiness verdict" in prompt
    assert "Stop after the `DRAFT` Gap Map" in prompt


def test_pl_v38_02_defers_recommendation_and_roadmap_history() -> None:
    assessment = _read("template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md")
    gap = _read("template/.planning/control/CAUSAL_GAP_DERIVATION.md")

    assert "Do not load broad recommendation history" in assessment
    assert "Do not load broad recommendation, decision, old Roadmap" in gap
    assert "Historical reconciliation belongs to PL-V38-03" in gap
    assert "Do not rank Gaps" in gap
    assert "create a Change" in gap


def test_context_policy_has_assessment_and_gap_profiles() -> None:
    context = _read("template/.planning/control/CONTEXT_POLICY.md")

    assert "### Current Capability Assessment" in context
    assert "### Causal Gap derivation" in context
    assert "capability by capability" in context
    assert "assessment as the primary evidence boundary" in context
    assert "Do not rescan the repository" in context


def test_doctor_requires_gap_map_but_not_runtime_assessment_snapshot() -> None:
    required = set(_iter_required_paths())

    assert ".planning/project/GAP_MAP.md" in required
    assert ".planning/assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md" not in required
