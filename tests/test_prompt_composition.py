from __future__ import annotations

import hashlib
import json
from pathlib import Path
import shutil
import subprocess
from dataclasses import fields

import pytest

from planning_lite.attempt_evaluation import (
    AttemptEvaluationError,
    AttemptRecordV1,
    CandidateIdentityV1,
    ContextResidencyClass,
    FindingV1,
    IdentityRefV1,
    PromptComponentRefV1,
    PromptCompositionComparisonV1,
    PromptCompositionRefV1,
    RecommendationEvidenceV1,
    compare_prompt_compositions,
    derive_promptops_finding,
    derive_recommendation_evidence,
    derive_stable_prefix_identity,
)


def component(
    ref: str,
    order: int,
    *,
    identity: str | None = None,
    role: str = "CONTEXT",
    residency: str | ContextResidencyClass = ContextResidencyClass.CHANGE_STABLE,
) -> PromptComponentRefV1:
    return PromptComponentRefV1(
        ref,
        identity or f"hash-{ref}",
        role,
        residency,
        order,
    )


def composition(*components: PromptComponentRefV1, version: str | None = None, adapter: str | None = None) -> PromptCompositionRefV1:
    return PromptCompositionRefV1.from_components(
        components,
        prompt_version_ref=version,
        agent_adapter_ref=adapter,
    )


def direct_comparison_copy(base: PromptCompositionComparisonV1, **changes: object) -> PromptCompositionComparisonV1:
    values = {field.name: changes.get(field.name, getattr(base, field.name)) for field in fields(PromptCompositionComparisonV1)}
    return PromptCompositionComparisonV1(**values)


def test_residency_vocabulary_and_reserved_dynamic_roles_are_fail_closed() -> None:
    assert {item.value for item in ContextResidencyClass} == {
        "FRAMEWORK_STATIC",
        "ENVIRONMENT_STABLE",
        "CHANGE_STABLE",
        "RUN_DYNAMIC",
        "ON_DEMAND",
    }
    with pytest.raises(AttemptEvaluationError):
        component("auth", 0, role="OWNER_AUTHORIZATION", residency="CHANGE_STABLE")
    assert component("auth", 0, role="OWNER_AUTHORIZATION", residency="RUN_DYNAMIC").residency_class == "RUN_DYNAMIC"


def test_component_order_must_be_contiguous_and_already_canonical() -> None:
    with pytest.raises(AttemptEvaluationError):
        composition(component("b", 1), component("a", 0))
    with pytest.raises(AttemptEvaluationError):
        composition(component("a", 0), component("a", 1))


def test_full_and_stable_prefix_identities_are_deterministic_with_unicode_and_nulls() -> None:
    first = composition(
        component("юнит", 0, identity="значение"),
        component("run", 1, role="TASK_RESULT", residency="RUN_DYNAMIC"),
    )
    second = composition(
        component("юнит", 0, identity="значение"),
        component("run", 1, role="TASK_RESULT", residency="RUN_DYNAMIC"),
    )
    assert first.composition_identity == second.composition_identity
    assert first.stable_prefix_identity == second.stable_prefix_identity
    assert first.prompt_version_ref is None
    assert first.agent_adapter_ref is None
    assert first.to_mapping()["prompt_version_ref"] is None
    assert first.to_mapping()["agent_adapter_ref"] is None
    assert first.composition_identity == first.composition_identity.lower()


def test_stable_prefix_is_longest_leading_stable_run() -> None:
    before_dynamic = composition(
        component("framework", 0, residency="FRAMEWORK_STATIC"),
        component("run", 1, role="GIT_HEAD", residency="RUN_DYNAMIC"),
        component("late", 2, residency="CHANGE_STABLE"),
    )
    after_dynamic = composition(
        component("framework", 0, residency="FRAMEWORK_STATIC"),
        component("run", 1, role="GIT_HEAD", identity="another-head", residency="RUN_DYNAMIC"),
        component("late", 2, residency="CHANGE_STABLE"),
    )
    assert before_dynamic.stable_prefix_components == (before_dynamic.components[0],)
    assert before_dynamic.stable_prefix_identity == after_dynamic.stable_prefix_identity
    assert before_dynamic.composition_identity != after_dynamic.composition_identity


@pytest.mark.parametrize("role", [
    "OWNER_AUTHORIZATION",
    "IMPLEMENTATION_AUTHORIZATION",
    "GIT_MUTATION_AUTHORIZATION",
    "NEXT_PERMITTED_ACTION",
    "BLOCKER",
    "TASK_RESULT",
    "GIT_HEAD",
    "GIT_STATUS",
    "RUNTIME_EVIDENCE",
])
def test_every_reserved_run_dynamic_role_is_excluded_from_stable_prefix(role: str) -> None:
    left = composition(
        component("stable", 0, residency="CHANGE_STABLE"),
        component("dynamic", 1, role=role, identity="one", residency="RUN_DYNAMIC"),
    )
    right = composition(
        component("stable", 0, residency="CHANGE_STABLE"),
        component("dynamic", 1, role=role, identity="two", residency="RUN_DYNAMIC"),
    )
    assert left.stable_prefix_identity == right.stable_prefix_identity


def test_on_demand_ends_prefix_and_is_not_fabricated_when_absent() -> None:
    present = composition(
        component("stable", 0),
        component("optional", 1, residency="ON_DEMAND"),
    )
    absent = composition(component("stable", 0))
    assert present.stable_prefix_components == (present.components[0],)
    assert absent.stable_prefix_components == (absent.components[0],)
    assert present.stable_prefix_identity == absent.stable_prefix_identity


def test_prompt_version_and_adapter_are_full_identity_only_metadata() -> None:
    base = composition(component("stable", 0))
    changed = composition(component("stable", 0), version="prompt-v2", adapter="adapter-v1")
    assert base.stable_prefix_identity == changed.stable_prefix_identity
    assert base.composition_identity != changed.composition_identity


def test_same_stable_components_different_dynamic_tail_reuse_prefix() -> None:
    left = composition(component("stable", 0), component("tail", 1, role="TASK_RESULT", residency="RUN_DYNAMIC"))
    right = composition(component("stable", 0), component("tail", 1, identity="new", role="TASK_RESULT", residency="RUN_DYNAMIC"))
    result = compare_prompt_compositions(left, right)
    assert result.stable_prefix_reused
    assert not result.stable_prefix_changed
    assert result.identity_changed_component_refs == ("tail",)
    assert result.composition_changed_between_attempts
    assert result.unexpected_component_churn


def test_comparison_public_carrier_rejects_contradictory_relational_flags() -> None:
    left = composition(component("stable", 0))
    right = composition(component("stable", 0, identity="changed"))
    valid = compare_prompt_compositions(left, right)
    assert isinstance(valid, PromptCompositionComparisonV1)
    assert valid.stable_prefix_reused is False
    assert valid.stable_prefix_changed is True
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, stable_prefix_reused=True, stable_prefix_changed=True)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, stable_prefix_reused=False, stable_prefix_changed=False)


def test_comparison_public_carrier_rejects_other_derived_flag_mismatches() -> None:
    left = composition(component("stable", 0))
    right = composition(component("stable", 0, identity="changed"))
    valid = compare_prompt_compositions(left, right)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, composition_changed_between_attempts=False)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, component_order_stable=False)


def test_comparison_public_carrier_rejects_impossible_same_identity_deltas() -> None:
    base = composition(component("stable", 0))
    valid = compare_prompt_compositions(base, base)
    for changes in (
        {"prompt_version_changed": True},
        {"added_component_refs": ("ghost",)},
        {"left_stable_prefix_identity": "prefix-other"},
    ):
        with pytest.raises(AttemptEvaluationError):
            direct_comparison_copy(valid, **changes)


def test_comparison_public_carrier_rejects_incoherent_stable_prefix_relations() -> None:
    base = composition(component("stable", 0))
    changed_prefix = composition(component("stable", 0, identity="changed"))
    valid = compare_prompt_compositions(base, changed_prefix)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, stable_prefix_reused=True, stable_prefix_changed=False)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, stable_prefix_changed=True, left_stable_prefix_identity=valid.right_stable_prefix_identity)


def test_comparison_public_carrier_rejects_cross_delta_membership_conflicts() -> None:
    left = composition(component("stable", 0))
    right = composition(component("stable", 0, identity="changed"))
    valid = compare_prompt_compositions(left, right)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, added_component_refs=("x",), removed_component_refs=("x",))
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, added_component_refs=("x",), identity_changed_component_refs=("stable", "x"))
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, removed_component_refs=("x",), identity_changed_component_refs=("stable", "x"))


def test_comparison_public_carrier_rejects_churn_aggregate_mismatch() -> None:
    left = composition(component("stable", 0))
    right = composition(component("stable", 0, identity="changed"))
    valid = compare_prompt_compositions(left, right)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, unexpected_component_churn=False)
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(valid, identity_changed_component_refs=(), unexpected_component_churn=True)


def test_comparison_public_carrier_accepts_coherent_membership_and_common_deltas() -> None:
    left = composition(component("a", 0), component("b", 1))
    added = composition(component("a", 0), component("b", 1), component("c", 2))
    removed = composition(component("a", 0))
    changed = composition(component("a", 0, identity="changed"), component("b", 1))
    assert compare_prompt_compositions(left, added).added_component_refs == ("c",)
    assert compare_prompt_compositions(left, removed).removed_component_refs == ("b",)
    assert compare_prompt_compositions(left, changed).identity_changed_component_refs == ("a",)


def test_comparison_covers_each_identity_bearing_field_with_the_existing_delta_carrier() -> None:
    base = composition(component("x", 0, identity="one"), component("y", 1, identity="two"))
    hash_changed = composition(component("x", 0, identity="changed"), component("y", 1, identity="two"))
    role_changed = composition(
        PromptComponentRefV1("x", "hash-x", "SYSTEM", ContextResidencyClass.CHANGE_STABLE, 0),
        component("y", 1, identity="two"),
    )
    residency_changed = composition(
        component("x", 0, identity="one", residency=ContextResidencyClass.ENVIRONMENT_STABLE),
        component("y", 1, identity="two"),
    )
    moved = composition(component("y", 0, identity="two"), component("x", 1, identity="one"))
    added = composition(component("x", 0, identity="one"), component("y", 1, identity="two"), component("z", 2))
    removed = composition(component("x", 0, identity="one"))
    assert compare_prompt_compositions(base, hash_changed).identity_changed_component_refs == ("x",)
    assert compare_prompt_compositions(base, role_changed).identity_changed_component_refs == ("x",)
    assert compare_prompt_compositions(base, residency_changed).residency_changed_component_refs == ("x",)
    assert compare_prompt_compositions(base, moved).moved_component_refs == ("x", "y")
    assert compare_prompt_compositions(base, added).added_component_refs == ("z",)
    assert compare_prompt_compositions(base, removed).removed_component_refs == ("y",)


def test_comparison_requires_full_identity_explainability_and_preserves_valid_top_level_deltas() -> None:
    base = composition(component("stable", 0))
    versioned = composition(component("stable", 0), version="v2")
    adapted = composition(component("stable", 0), adapter="adapter-v2")
    version_result = compare_prompt_compositions(base, versioned)
    adapter_result = compare_prompt_compositions(base, adapted)
    assert version_result.prompt_version_changed
    assert not version_result.unexpected_component_churn
    assert adapter_result.agent_adapter_changed
    assert not adapter_result.unexpected_component_churn
    with pytest.raises(AttemptEvaluationError):
        direct_comparison_copy(
            version_result,
            prompt_version_changed=False,
            left_composition_identity="a" * 64,
            right_composition_identity="b" * 64,
        )


def test_role_change_with_other_common_deltas_remains_coherent() -> None:
    left = composition(
        PromptComponentRefV1("x", "hash-x", "CONTEXT", ContextResidencyClass.ENVIRONMENT_STABLE, 0),
        component("y", 1, identity="hash-y"),
    )
    right = composition(
        component("y", 0, identity="hash-y"),
        PromptComponentRefV1("x", "hash-x", "SYSTEM", ContextResidencyClass.CHANGE_STABLE, 1),
    )
    result = compare_prompt_compositions(left, right)
    assert result.identity_changed_component_refs == ("x",)
    assert result.residency_changed_component_refs == ("x",)
    assert result.moved_component_refs == ("x", "y")
    assert result.unexpected_component_churn


def test_changed_stable_component_changes_prefix() -> None:
    left = composition(component("stable", 0, identity="one"))
    right = composition(component("stable", 0, identity="two"))
    result = compare_prompt_compositions(left, right)
    assert result.stable_prefix_changed
    assert result.identity_changed_component_refs == ("stable",)


def test_comparison_reports_add_remove_move_residency_and_version_facts() -> None:
    left = composition(
        component("a", 0),
        component("b", 1, residency="ENVIRONMENT_STABLE"),
        version="v1",
    )
    right = composition(
        component("b", 0, residency="CHANGE_STABLE"),
        component("c", 1),
        version="v2",
    )
    result = compare_prompt_compositions(left, right)
    assert result.added_component_refs == ("c",)
    assert result.removed_component_refs == ("a",)
    assert result.moved_component_refs == ("b",)
    assert result.residency_changed_component_refs == ("b",)
    assert result.prompt_version_changed
    assert not result.component_order_stable


def test_dynamic_before_stable_boundary_is_explicitly_observable() -> None:
    left = composition(
        component("dynamic", 0, role="RUNTIME_EVIDENCE", residency="RUN_DYNAMIC"),
        component("stable", 1),
    )
    result = compare_prompt_compositions(left, left)
    assert result.dynamic_component_before_stable_boundary
    assert result.unexpected_component_churn


def test_promptops_finding_uses_existing_nonblocking_domain_and_noop_when_clean() -> None:
    clean = composition(component("stable", 0))
    assert derive_promptops_finding(compare_prompt_compositions(clean, clean)) is None
    changed = composition(component("stable", 0, identity="new"))
    comparison = compare_prompt_compositions(clean, changed, evidence_refs=("EV-COMP",))
    finding = derive_promptops_finding(comparison)
    assert isinstance(finding, FindingV1)
    assert finding.responsibility_domains == ("VERIFICATION_TEST_COVERAGE",)
    assert finding.acceptance_impact == "NON_BLOCKING"
    assert finding.disposition == "OPEN"
    assert finding.owner_adjudication_ref is None


def test_recommendation_contract_has_exact_noop_and_eligible_outcomes() -> None:
    clean = composition(component("stable", 0))
    clean_result = compare_prompt_compositions(clean, clean)
    noop = derive_recommendation_evidence(clean_result)
    assert noop.outcome == "NO_RECOMMENDATION"
    assert noop.non_authoritative is True
    changed = composition(component("stable", 0, identity="new"))
    result = compare_prompt_compositions(clean, changed, evidence_refs=("EV-COMP",), finding_refs=("F-1",))
    finding = derive_promptops_finding(result, evidence_refs=("EV-COMP",), finding_id="F-1")
    recommendation = derive_recommendation_evidence(
        result,
        (finding,) if finding is not None else (),
    )
    assert recommendation.outcome == "RECOMMENDATION"
    assert recommendation.recommendation_kind == "STABLE_CARRIER_REUSE"
    assert recommendation.non_authoritative is True
    assert recommendation.owner_adjudication_ref is None


def test_blocking_finding_prevents_recommendation_promotion() -> None:
    clean = composition(component("stable", 0))
    changed = composition(component("stable", 0, identity="new"))
    result = compare_prompt_compositions(clean, changed, evidence_refs=("EV",), finding_refs=("F",))
    blocking = FindingV1("F", "blocking", "MATERIAL", ("CONTRACT",), "BLOCKING", "OPEN", ("EV",))
    output = derive_recommendation_evidence(result, (blocking,))
    assert output.outcome == "NO_RECOMMENDATION"


def test_orphan_and_mismatched_finding_refs_cannot_produce_recommendation() -> None:
    clean = composition(component("stable", 0))
    changed = composition(component("stable", 0, identity="new"))
    orphan = compare_prompt_compositions(clean, changed, evidence_refs=("EV",), finding_refs=("F-ORPHAN",))
    assert derive_recommendation_evidence(orphan, ()).outcome == "NO_RECOMMENDATION"
    mismatched = compare_prompt_compositions(clean, changed, evidence_refs=("EV",), finding_refs=("F-1",))
    different_finding = FindingV1("F-2", "different", "NON_MATERIAL", ("CONTRACT",), "NON_BLOCKING", "OPEN", ("EV",))
    assert derive_recommendation_evidence(mismatched, (different_finding,)).outcome == "NO_RECOMMENDATION"


def test_mismatched_finding_evidence_refs_cannot_produce_recommendation() -> None:
    clean = composition(component("stable", 0))
    changed = composition(component("stable", 0, identity="new"))
    comparison = compare_prompt_compositions(clean, changed, evidence_refs=("EV",), finding_refs=("F-1",))
    finding = FindingV1("F-1", "mismatch", "NON_MATERIAL", ("CONTRACT",), "NON_BLOCKING", "OPEN", ("OTHER",))
    assert derive_recommendation_evidence(comparison, (finding,)).outcome == "NO_RECOMMENDATION"


def test_valid_finding_and_evidence_provenance_preserves_eligible_recommendation() -> None:
    clean = composition(component("stable", 0))
    changed = composition(component("stable", 0, identity="new"))
    comparison = compare_prompt_compositions(clean, changed, evidence_refs=("EV",), finding_refs=("F-1",))
    finding = FindingV1("F-1", "valid", "NON_MATERIAL", ("CONTRACT",), "NON_BLOCKING", "OPEN", ("EV",))
    result = derive_recommendation_evidence(comparison, (finding,))
    assert result.outcome == "RECOMMENDATION"
    assert result.finding_refs == ("F-1",)
    assert result.evidence_refs == ("EV",)


def test_explicit_evidence_override_cannot_replace_comparison_provenance() -> None:
    clean = composition(component("stable", 0))
    changed = composition(component("stable", 0, identity="new"))
    comparison = compare_prompt_compositions(clean, changed, evidence_refs=("EV-COMPARISON",), finding_refs=("F-1",))
    finding = FindingV1("F-1", "valid", "NON_MATERIAL", ("CONTRACT",), "NON_BLOCKING", "OPEN", ("EV-OVERRIDE",))
    result = derive_recommendation_evidence(comparison, (finding,), evidence_refs=("EV-OVERRIDE",))
    assert result.outcome == "NO_RECOMMENDATION"


def test_empty_comparison_evidence_cannot_be_backfilled_by_finding_or_caller() -> None:
    clean = composition(component("stable", 0))
    changed = composition(component("stable", 0, identity="new"))
    comparison = compare_prompt_compositions(clean, changed, finding_refs=("F-1",))
    finding = FindingV1("F-1", "supplied only", "NON_MATERIAL", ("CONTRACT",), "NON_BLOCKING", "OPEN", ("EV-SUPPLIED",))
    result = derive_recommendation_evidence(comparison, (finding,), evidence_refs=("EV-SUPPLIED",))
    assert result.outcome == "NO_RECOMMENDATION"


def _attempt(attempt_ordinal: int, composition_ref: str, *, parent: str | None = None) -> AttemptRecordV1:
    return AttemptRecordV1(
        f"CHG-PL-V39-08/T-10/A{attempt_ordinal}",
        "CHG-PL-V39-08",
        "T-10",
        attempt_ordinal,
        f"OWNER-AUTH-08C-{attempt_ordinal}",
        "AC-PL-V39-08-T10",
        CandidateIdentityV1("GIT_COMMIT", "a" * 40),
        (IdentityRefV1("plan", "ca9309f2575636ea7ca08801a30b68e273d30912"),),
        prompt_composition_ref=composition_ref,
        parent_attempt_ref=parent,
    )


def test_composition_refs_are_evidence_not_attempt_or_authority() -> None:
    ref = composition(component("stable", 0))
    assert ref.composition_identity != "CHG-1/T-07/A1"
    assert not hasattr(ref, "authorization_ref")
    assert not hasattr(ref, "provider_cache_key")


def test_disposable_recommendation_fixture_does_not_mutate_source(tmp_path: Path) -> None:
    source = tmp_path / "source.md"
    source.write_text("stable source\n", encoding="utf-8")
    before = source.read_bytes()
    left = composition(component("stable", 0))
    right = composition(component("stable", 0, identity="changed"))
    comparison = compare_prompt_compositions(left, right, evidence_refs=("EV",), finding_refs=("F",))
    finding = derive_promptops_finding(comparison, finding_id="F", evidence_refs=("EV",))
    result = derive_recommendation_evidence(comparison, (finding,) if finding else ())
    assert result.outcome == "RECOMMENDATION"
    assert source.read_bytes() == before


def _git_status(root: Path) -> str:
    return subprocess.check_output(
        ["git", "-C", str(root), "status", "--short", "--untracked-files=all"],
        text=True,
    )


def _init_disposable_repo(root: Path) -> Path:
    subprocess.run(["git", "init", "-q", str(root)], check=True, capture_output=True)
    source = root / "source.md"
    source.write_text("stable source\n", encoding="utf-8")
    return source


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_disposable_recommendation_inbox_proof_covers_eligible_noop_and_cleanup(tmp_path: Path) -> None:
    eligible_root = tmp_path / "eligible-workspace"
    eligible_root.mkdir()
    source = _init_disposable_repo(eligible_root)
    source_hash_before = _sha256(source)
    status_before = _git_status(eligible_root)
    assert "source.md" in status_before

    left = composition(component("stable", 0))
    right = composition(component("stable", 0, identity="changed"))
    attempt_a = _attempt(1, left.composition_identity)
    attempt_b = _attempt(2, right.composition_identity, parent=attempt_a.attempt_id)
    assert isinstance(attempt_a, AttemptRecordV1)
    assert isinstance(attempt_b, AttemptRecordV1)
    assert attempt_a.prompt_composition_ref == left.composition_identity
    assert attempt_b.prompt_composition_ref == right.composition_identity
    comparison = compare_prompt_compositions(left, right, evidence_refs=("EV-T10",), finding_refs=("F-T10",))
    finding = FindingV1("F-T10", "eligible", "NON_MATERIAL", ("CONTRACT",), "NON_BLOCKING", "OPEN", ("EV-T10",))
    result = derive_recommendation_evidence(comparison, (finding,))
    assert result.outcome == "RECOMMENDATION"
    candidate = eligible_root / ".planning" / "recommendations" / "inbox" / "REC-08C-T10.md"
    candidate.parent.mkdir(parents=True)
    candidate.write_text(
        "\n".join(
            (
                f"Source Attempt references: {attempt_a.attempt_id}, {attempt_b.attempt_id}",
                f"Source PromptComposition / comparison reference: {comparison.right_composition_identity}",
                "Source Finding references: F-T10",
                "Source evidence references: EV-T10",
                f"Recommendation evidence outcome: {result.outcome}",
                "Recommendation authority: NON_AUTHORITATIVE",
                "Owner decision: PENDING",
            )
        )
        + "\n",
        encoding="utf-8",
    )
    status_after = _git_status(eligible_root)
    assert "REC-08C-T10.md" in status_after
    assert _sha256(source) == source_hash_before
    assert "NON_AUTHORITATIVE" in candidate.read_text(encoding="utf-8")
    assert "Owner decision: PENDING" in candidate.read_text(encoding="utf-8")
    candidate_path = candidate.relative_to(eligible_root).as_posix()
    candidate_hash = _sha256(candidate)

    noop_root = tmp_path / "noop-workspace"
    noop_root.mkdir()
    noop_source = _init_disposable_repo(noop_root)
    noop_hash_before = _sha256(noop_source)
    noop_status_before = _git_status(noop_root)
    noop_left = composition(component("stable", 0))
    noop_attempt_a = _attempt(1, noop_left.composition_identity)
    noop_attempt_b = _attempt(2, noop_left.composition_identity, parent=noop_attempt_a.attempt_id)
    assert noop_attempt_a.prompt_composition_ref == noop_left.composition_identity
    assert noop_attempt_b.prompt_composition_ref == noop_left.composition_identity
    noop_comparison = compare_prompt_compositions(noop_left, noop_left)
    noop_result = derive_recommendation_evidence(noop_comparison, ())
    assert noop_result.outcome == "NO_RECOMMENDATION"
    noop_candidate = noop_root / ".planning" / "recommendations" / "inbox" / "REC-08C-T10.md"
    assert not noop_candidate.exists()
    assert _git_status(noop_root) == noop_status_before
    assert _sha256(noop_source) == noop_hash_before

    shutil.rmtree(eligible_root)
    shutil.rmtree(noop_root)
    assert not eligible_root.exists()
    assert not noop_root.exists()
    assert candidate_path == ".planning/recommendations/inbox/REC-08C-T10.md"
    assert len(candidate_hash) == 64


def test_recommendation_template_preserves_complete_provenance_and_owner_gate() -> None:
    template = (Path(__file__).parents[1] / "template/.planning/recommendations/TEMPLATE.md").read_text(encoding="utf-8")
    required = (
        "Source Attempt / candidate reference:",
        "Source PromptComposition / comparison reference:",
        "Source Finding references:",
        "Source evidence references:",
        "Recommendation authority: `NON_AUTHORITATIVE`",
        "Owner decision: `OWNER DECISION REQUIRED / PENDING`",
    )
    assert all(field in template for field in required)


def test_recommendation_provenance_mapping_is_serializable() -> None:
    clean = composition(component("stable", 0))
    changed = composition(component("stable", 0, identity="new"))
    comparison = compare_prompt_compositions(clean, changed, evidence_refs=("EV",), finding_refs=("F-1",))
    finding = FindingV1("F-1", "valid", "NON_MATERIAL", ("CONTRACT",), "NON_BLOCKING", "OPEN", ("EV",))
    result = derive_recommendation_evidence(comparison, (finding,))
    payload = {
        "attempt_ref": "CHG-PL-V39-08/T-10/A1",
        "comparison_ref": comparison.right_composition_identity,
        "finding_refs": list(result.finding_refs),
        "evidence_refs": list(result.evidence_refs),
        "outcome": result.outcome,
    }
    assert json.loads(json.dumps(payload, sort_keys=True)) == payload


def test_recommendation_record_rejects_authority_elevation() -> None:
    with pytest.raises(AttemptEvaluationError):
        RecommendationEvidenceV1(
            "RECOMMENDATION",
            "x",
            "STABLE_CARRIER_REUSE",
            "statement",
            ("EV",),
            ("F",),
            "target",
            False,
        )
