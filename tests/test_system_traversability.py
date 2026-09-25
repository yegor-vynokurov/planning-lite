from __future__ import annotations

import importlib.util
import hashlib
import json
import re
from dataclasses import asdict
from pathlib import Path

import pytest

from planning_lite.attempt_evaluation import (
    AttemptRecordV1,
    CandidateIdentityV1,
    IdentityRefV1,
    ObservedResultV1,
    TechnicalEvaluationV1,
    VerifierEvidenceV1,
    allocate_attempt_ordinal,
    evaluate_technical,
)
from planning_lite.execution_guidance import OperationGuidanceV1, select_operation_guidance
from planning_lite.attempt_runtime import (
    AdmissibilityOutcome,
    LookupOutcome,
    attempt_store_path,
    check_activation_admissibility,
    claim_attempt,
    lookup_attempt,
)
from planning_lite.authorization import issue_preparation_authorization, issue_recovery_authorization
from planning_lite.cli import main
from planning_lite.telemetry import validate_receipt
from planning_lite.traversability import (
    APPLICABILITY_VALUES,
    CHECK_DISPOSITIONS,
    GAP_CLASSES,
    JOURNEY_STATES,
    PLACEHOLDER_VALUES,
    CriticalJourneyProjectionV1,
    JourneySmokeResultV1,
    SeamObservationV1,
    TraversabilityError,
    check_critical_journey_smoke,
    check_system_traversability,
)


def _seam(
    ref: str,
    *,
    status: str = "PASS",
    reason: str | None = None,
    reachable: bool = True,
    activated: bool = True,
    identity_continuous: bool = True,
    contract_compatible: bool = True,
    gap_class: str | None = None,
    activation_qualifier: bool = False,
) -> SeamObservationV1:
    return SeamObservationV1(
        seam_ref=ref,
        producer_ref=f"producer:{ref}",
        consumer_ref=f"consumer:{ref}",
        status=status,
        causal_reason=reason,
        reachable=reachable,
        activated=activated,
        identity_continuous=identity_continuous,
        contract_compatible=contract_compatible,
        gap_class=gap_class,
        activation_qualifier=activation_qualifier,
    )


def _journey(
    *seams: SeamObservationV1,
    journey_id: str = "J-001",
    current_state: str = "DEFINED",
    placeholder_policy: str = "NONE",
    real_behavior_present: bool = True,
    traversal_probe_admissible: bool = True,
    evidence_admissible: bool = True,
    observation_block: str = "NONE",
    applicability: str = "REQUIRED",
) -> CriticalJourneyProjectionV1:
    return CriticalJourneyProjectionV1(
        journey_id=journey_id,
        applicability=applicability,
        current_state=current_state,
        ordered_seams=seams,
        placeholder_policy=placeholder_policy,
        real_behavior_present=real_behavior_present,
        traversal_probe_admissible=traversal_probe_admissible,
        evidence_admissible=evidence_admissible,
        observation_block=observation_block,
    )


_CARRIER_FIELDS = (
    "journey_id",
    "applicability",
    "applicability_reason",
    "target_refs",
    "roadmap_refs",
    "entry_ref",
    "ordered_nodes",
    "ordered_seams",
    "runtime_lifetime_owner_ref",
    "identity_continuity_ref",
    "placeholder_policy",
    "terminal_semantics",
    "evidence_channel_ref",
    "current_state",
    "gap_refs",
    "last_observation_ref",
)

_JOURNEY_STATES = {
    "NOT_DEFINED",
    "DEFINED",
    "WIRED_FAIL",
    "WIRED_TRAVERSABLE",
    "PASSING",
}


def _parse_carrier_records(text: str) -> tuple[str, ...]:
    assert text.splitlines()[0] == "# Critical Journeys"
    visible = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    remainder = visible.split("# Critical Journeys", 1)[1].strip()
    if not remainder or remainder == "No CriticalJourney records are declared yet.":
        return ()

    def tick_value(value: str) -> str:
        tick = chr(96)
        assert value.startswith(tick) and value.endswith(tick)
        assert len(value) > 2
        return value[1:-1]

    def refs(value: str) -> tuple[str, ...]:
        if value == "[]":
            return ()
        assert value.startswith("[") and value.endswith("]")
        items = tuple(item.strip() for item in value[1:-1].split(","))
        assert items
        names = tuple(tick_value(item) for item in items)
        assert names == tuple(sorted(names))
        assert len(names) == len(set(names))
        return names

    def ordered(value: str) -> tuple[str, ...]:
        if value == "[]":
            return ()
        tick = chr(96)
        assert value.startswith("[") and value.endswith("]")
        parts = tuple(part.strip() for part in value[1:-1].split(","))
        entries = tuple(part.split(":" + tick, 1) for part in parts)
        assert all(len(entry) == 2 for entry in entries)
        assert tuple(int(entry[0]) for entry in entries) == tuple(
            range(1, len(entries) + 1)
        )
        assert all(entry[1].endswith(tick) and len(entry[1]) > 1 for entry in entries)
        return tuple(entry[1][:-1] for entry in entries)

    journey_ids: list[str] = []
    for record in remainder.split(chr(10) + chr(10)):
        lines = record.splitlines()
        assert lines and lines[0].startswith("## Journey: ")
        journey_id = lines[0][len("## Journey: ") :].strip()
        assert journey_id
        assert all(line.startswith("- ") for line in lines[1:])
        pairs = [line[2:].split(": ", 1) for line in lines[1:]]
        assert all(len(pair) == 2 for pair in pairs)
        fields = tuple(pair[0] for pair in pairs)
        assert fields == _CARRIER_FIELDS
        values = dict(pairs)

        assert tick_value(values["journey_id"]) == journey_id
        assert values["applicability"] in {"REQUIRED", "NOT_APPLICABLE"}
        assert tick_value(values["applicability_reason"])
        refs(values["target_refs"])
        refs(values["roadmap_refs"])
        ordered(values["ordered_nodes"])
        ordered(values["ordered_seams"])
        refs(values["gap_refs"])

        for field in (
            "entry_ref",
            "runtime_lifetime_owner_ref",
            "identity_continuity_ref",
            "evidence_channel_ref",
        ):
            assert values[field] == "NONE_DECLARED" or tick_value(values[field])
        assert values["placeholder_policy"] in {"NONE", "NOT_IMPLEMENTED", "FIXTURE_ONLY"}
        assert tick_value(values["terminal_semantics"])
        assert values["current_state"] in _JOURNEY_STATES | {"NONE"}
        if values["applicability"] == "NOT_APPLICABLE":
            assert values["current_state"] == "NONE"
        else:
            assert values["current_state"] in _JOURNEY_STATES
        assert values["last_observation_ref"] == "NONE" or tick_value(
            values["last_observation_ref"]
        )
        journey_ids.append(journey_id)

    assert journey_ids == sorted(journey_ids)
    assert len(journey_ids) == len(set(journey_ids))
    return tuple(journey_ids)


def _valid_carrier_fixture() -> str:
    nl = chr(10)
    tick = chr(96)
    return nl.join(
        (
            "# Critical Journeys",
            "",
            "## Journey: J-001",
            f"- journey_id: {tick}J-001{tick}",
            "- applicability: REQUIRED",
            f"- applicability_reason: {tick}material flow{tick}",
            f"- target_refs: [{tick}T-001{tick}]",
            f"- roadmap_refs: [{tick}R-001{tick}]",
            f"- entry_ref: {tick}entry{tick}",
            f"- ordered_nodes: [1:{tick}node-a{tick}, 2:{tick}node-b{tick}]",
            f"- ordered_seams: [1:{tick}seam-a{tick}]",
            f"- runtime_lifetime_owner_ref: {tick}owner{tick}",
            f"- identity_continuity_ref: {tick}identity{tick}",
            "- placeholder_policy: NONE",
            f"- terminal_semantics: {tick}terminal{tick}",
            f"- evidence_channel_ref: {tick}evidence{tick}",
            "- current_state: DEFINED",
            "- gap_refs: []",
            "- last_observation_ref: NONE",
            "",
            "## Journey: J-002",
            f"- journey_id: {tick}J-002{tick}",
            "- applicability: REQUIRED",
            f"- applicability_reason: {tick}second material flow{tick}",
            f"- target_refs: [{tick}T-002{tick}]",
            f"- roadmap_refs: [{tick}R-002{tick}]",
            "- entry_ref: NONE_DECLARED",
            "- ordered_nodes: []",
            "- ordered_seams: []",
            "- runtime_lifetime_owner_ref: NONE_DECLARED",
            "- identity_continuity_ref: NONE_DECLARED",
            "- placeholder_policy: FIXTURE_ONLY",
            f"- terminal_semantics: {tick}fixture terminal{tick}",
            f"- evidence_channel_ref: {tick}evidence-2{tick}",
            "- current_state: PASSING",
            f"- gap_refs: [{tick}G-002{tick}]",
            f"- last_observation_ref: {tick}OBS-002{tick}",
        )
    ) + nl


def test_carrier_serialization_cardinality_and_copy_contract() -> None:
    paths = (
        Path("template/.planning/project/CRITICAL_JOURNEYS.md"),
        Path("template/.planning/templates/project/CRITICAL_JOURNEYS.md"),
    )
    contents = tuple(path.read_text(encoding="utf-8") for path in paths)
    assert contents[0] == contents[1]
    assert _parse_carrier_records(contents[0]) == ()

    valid = _valid_carrier_fixture()
    assert _parse_carrier_records(valid) == ("J-001", "J-002")
    with pytest.raises(AssertionError):
        _parse_carrier_records(valid.replace("## Journey: J-002", "## Journey: J-001"))
    with pytest.raises(AssertionError):
        _parse_carrier_records(valid.replace("- gap_refs:", "- extra_refs:"))
    with pytest.raises(AssertionError):
        _parse_carrier_records(valid.replace("current_state: PASSING", "current_state: UNKNOWN"))
    tick = chr(96)
    with pytest.raises(AssertionError):
        _parse_carrier_records(
            valid.replace(
                "target_refs: [" + tick + "T-002" + tick + "]",
                "target_refs: [" + tick + "T-003" + tick + ", " + tick + "T-002" + tick + "]",
            )
        )


def test_contract_constants_and_carrier_projection_are_bounded() -> None:
    assert JOURNEY_STATES == (
        "NOT_DEFINED",
        "DEFINED",
        "WIRED_FAIL",
        "WIRED_TRAVERSABLE",
        "PASSING",
    )
    assert GAP_CLASSES == (
        "IMPLEMENTATION_GAP",
        "WIRING_GAP",
        "ORCHESTRATION_GAP",
        "EVIDENCE_GAP",
    )
    assert APPLICABILITY_VALUES == ("REQUIRED", "NOT_APPLICABLE")
    assert PLACEHOLDER_VALUES == ("NONE", "NOT_IMPLEMENTED", "FIXTURE_ONLY")
    assert CHECK_DISPOSITIONS == (
        "PASS",
        "WIRED_FAIL",
        "BLOCKED_BY_ENVIRONMENT",
        "BLOCKED_BY_MISSING_PROBE",
        "NOT_APPLICABLE",
    )
    for relative in (
        "template/.planning/project/CRITICAL_JOURNEYS.md",
        "template/.planning/templates/project/CRITICAL_JOURNEYS.md",
    ):
        text = Path(relative).read_text(encoding="utf-8")
        assert text.startswith("# Critical Journeys\n")
        assert "- journey_id:" in text
        assert "- ordered_seams:" in text
        assert "- current_state:" in text


def test_not_applicable_is_separate_from_required_journey_state() -> None:
    result = check_critical_journey_smoke(
        _journey(
            _seam("s1"),
            applicability="NOT_APPLICABLE",
            current_state="NONE",
        )
    )
    assert result.applicability == "NOT_APPLICABLE"
    assert result.check_disposition == "NOT_APPLICABLE"
    assert result.observed_traversability_state is None
    assert result.first_broken_seam is None
    assert result.gap_class is None
    assert result.seams[0].disposition == "UNOBSERVED"


@pytest.mark.parametrize(
    ("seam", "expected_gap"),
    [
        (_seam("impl", status="FAIL", gap_class="IMPLEMENTATION_GAP"), "IMPLEMENTATION_GAP"),
        (_seam("wire", status="FAIL", reachable=False), "WIRING_GAP"),
        (_seam("orch", status="FAIL", identity_continuous=False), "ORCHESTRATION_GAP"),
    ],
)
def test_first_broken_seam_preserves_causal_class_and_downstream_boundary(
    seam: SeamObservationV1,
    expected_gap: str,
) -> None:
    result = check_critical_journey_smoke(_journey(_seam("before"), seam, _seam("after")))
    assert result.observed_traversability_state == "WIRED_FAIL"
    assert result.first_broken_seam == seam.seam_ref
    assert result.gap_class == expected_gap
    assert [item.disposition for item in result.seams] == [
        "PASS",
        "FAIL",
        "DOWNSTREAM_UNREACHABLE",
    ]
    assert result.seams[1].causal_reason


def test_activation_is_only_a_wiring_gap_qualifier() -> None:
    seam = _seam(
        "activation",
        status="FAIL",
        activated=False,
        gap_class="WIRING_GAP",
        activation_qualifier=True,
    )
    result = check_critical_journey_smoke(_journey(seam))
    assert result.gap_class == "WIRING_GAP"
    assert result.activation_qualifier is True
    with pytest.raises(TraversabilityError):
        _seam(
            "bad-activation",
            status="FAIL",
            identity_continuous=False,
            gap_class="ORCHESTRATION_GAP",
            activation_qualifier=True,
        )


def test_placeholder_is_traversable_but_never_passing() -> None:
    placeholder = check_critical_journey_smoke(
        _journey(
            _seam("s1"),
            placeholder_policy="NOT_IMPLEMENTED",
            real_behavior_present=False,
        )
    )
    assert placeholder.observed_traversability_state == "WIRED_TRAVERSABLE"
    assert placeholder.check_disposition == "PASS"

    with pytest.raises(TraversabilityError):
        _journey(
            _seam("s1"),
            placeholder_policy="FIXTURE_ONLY",
            real_behavior_present=True,
        )

    passing = check_critical_journey_smoke(
        _journey(_seam("s1"), real_behavior_present=True, evidence_admissible=True)
    )
    assert passing.observed_traversability_state == "PASSING"
    assert passing.check_disposition == "PASS"


def test_environment_and_missing_probe_do_not_promote_or_regress_state() -> None:
    environment = check_critical_journey_smoke(
        _journey(
            _seam("s1"),
            current_state="PASSING",
            observation_block="BLOCKED_BY_ENVIRONMENT",
        )
    )
    assert environment.observed_traversability_state == "PASSING"
    assert environment.check_disposition == "BLOCKED_BY_ENVIRONMENT"
    assert environment.gap_class is None

    missing_probe = check_critical_journey_smoke(
        _journey(
            _seam("s1"),
            current_state="PASSING",
            evidence_admissible=False,
        )
    )
    assert missing_probe.observed_traversability_state == "PASSING"
    assert missing_probe.check_disposition == "BLOCKED_BY_MISSING_PROBE"
    assert missing_probe.gap_class == "EVIDENCE_GAP"


def test_causal_failure_precedes_environment_and_probe_blocks() -> None:
    result = check_critical_journey_smoke(
        _journey(
            _seam("broken", status="FAIL", reachable=False),
            observation_block="BLOCKED_BY_MISSING_PROBE",
            evidence_admissible=False,
        )
    )
    assert result.check_disposition == "WIRED_FAIL"
    assert result.first_broken_seam == "broken"
    assert result.gap_class == "WIRING_GAP"


def test_causal_gap_survives_environment_and_probe_dispositions() -> None:
    implementation = check_critical_journey_smoke(
        _journey(
            _seam("s1"),
            current_state="PASSING",
            real_behavior_present=False,
            observation_block="BLOCKED_BY_ENVIRONMENT",
        )
    )
    assert implementation.observed_traversability_state == "WIRED_FAIL"
    assert implementation.gap_class == "IMPLEMENTATION_GAP"
    assert implementation.check_disposition == "WIRED_FAIL"

    orchestration = check_critical_journey_smoke(
        _journey(
            _seam("s1", status="FAIL", identity_continuous=False),
            observation_block="BLOCKED_BY_ENVIRONMENT",
        )
    )
    assert orchestration.gap_class == "ORCHESTRATION_GAP"
    assert orchestration.check_disposition == "WIRED_FAIL"

    wiring = check_critical_journey_smoke(
        _journey(
            _seam("s1", status="FAIL", reachable=False),
            observation_block="BLOCKED_BY_MISSING_PROBE",
        )
    )
    assert wiring.gap_class == "WIRING_GAP"
    assert wiring.check_disposition == "WIRED_FAIL"


@pytest.mark.parametrize(
    "seam",
    (
        _seam(
            "orchestration-wiring",
            status="FAIL",
            identity_continuous=False,
            gap_class="WIRING_GAP",
        ),
        _seam(
            "wiring-orchestration",
            status="FAIL",
            reachable=False,
            gap_class="ORCHESTRATION_GAP",
        ),
        _seam(
            "orchestration-implementation",
            status="FAIL",
            identity_continuous=False,
            gap_class="IMPLEMENTATION_GAP",
        ),
    ),
)
def test_supplied_gap_class_cannot_override_causal_precedence(
    seam: SeamObservationV1,
) -> None:
    with pytest.raises(TraversabilityError, match="canonical causal precedence"):
        check_critical_journey_smoke(_journey(seam))


def test_passing_journey_can_regress_without_false_promotion() -> None:
    passing = check_critical_journey_smoke(
        _journey(_seam("s1"), current_state="PASSING")
    )
    assert passing.observed_traversability_state == "PASSING"
    assert passing.check_disposition == "PASS"

    regression = check_critical_journey_smoke(
        _journey(
            _seam("s1", status="FAIL", reachable=False),
            current_state="PASSING",
        )
    )
    assert regression.observed_traversability_state == "WIRED_FAIL"
    assert regression.check_disposition == "WIRED_FAIL"

    placeholder = check_critical_journey_smoke(
        _journey(
            _seam("s1"),
            current_state="PASSING",
            placeholder_policy="FIXTURE_ONLY",
            real_behavior_present=False,
        )
    )
    assert placeholder.observed_traversability_state == "WIRED_TRAVERSABLE"
    assert placeholder.check_disposition == "PASS"

    evidence_block = check_critical_journey_smoke(
        _journey(
            _seam("s1"),
            current_state="PASSING",
            evidence_admissible=False,
        )
    )
    assert evidence_block.observed_traversability_state == "PASSING"
    assert evidence_block.check_disposition == "BLOCKED_BY_MISSING_PROBE"


def test_local_capability_pass_does_not_hide_system_journey_regression() -> None:
    local_pass = check_critical_journey_smoke(
        _journey(_seam("local"), journey_id="CAPABILITY_LOCAL")
    )
    system_regression = check_critical_journey_smoke(
        _journey(
            _seam("system", status="FAIL", reachable=False),
            journey_id="SYSTEM_CRITICAL",
        )
    )
    aggregate = check_system_traversability((local_pass, system_regression))
    assert local_pass.check_disposition == "PASS"
    assert system_regression.check_disposition == "WIRED_FAIL"
    assert aggregate.check_disposition == "WIRED_FAIL"


def test_change_bypass_requires_surface_check_and_evidence_reason() -> None:
    controls = "\n".join(
        Path(path).read_text(encoding="utf-8")
        for path in (
            "template/.planning/control/CHANGE_DEFINITION.md",
            "template/.planning/control/CHANGE_PLANNING.md",
            "template/.planning/control/CHANGE_READINESS.md",
        )
    )
    for required_field in (
        "AFFECTED_CRITICAL_JOURNEYS",
        "EXPECTED_JOURNEY_STATE_DELTA",
        "SYSTEM_PROOF_REQUIRED",
        "SYSTEM_PROOF_NOT_APPLICABLE_REASON",
        "AFFECTED_JOURNEY_SURFACE_CHECK",
    ):
        assert required_field in controls
    assert "unaffected journey requires an evidence-backed bypass" in controls
    assert (
        "Missing carrier data or an unbound applicability choice is an architecture STOP"
        in controls
    )
    bare_not_applicable = {"AFFECTED_CRITICAL_JOURNEYS": "NONE"}
    assert not {
        "SYSTEM_PROOF_NOT_APPLICABLE_REASON",
        "AFFECTED_JOURNEY_SURFACE_CHECK",
    }.issubset(bare_not_applicable)


def test_bypass_contract_has_direct_positive_and_negative_proofs() -> None:
    def has_evidence_backed_reason(reason: str) -> bool:
        evidence_ref, separator, inspection = reason.partition(
            " | affected-surface inspection: "
        )
        return (
            bool(separator)
            and evidence_ref.startswith("EV-")
            and bool(evidence_ref[3:].strip())
            and bool(inspection.strip())
        )

    def permits_system_proof_na(block: dict[str, str]) -> bool:
        reason = block.get("SYSTEM_PROOF_NOT_APPLICABLE_REASON", "")
        return (
            block.get("AFFECTED_CRITICAL_JOURNEYS") == "NONE"
            and block.get("AFFECTED_JOURNEY_SURFACE_CHECK") == "PASS"
            and has_evidence_backed_reason(reason)
        )

    positive = {
        "AFFECTED_CRITICAL_JOURNEYS": "NONE",
        "AFFECTED_JOURNEY_SURFACE_CHECK": "PASS",
        "SYSTEM_PROOF_NOT_APPLICABLE_REASON": (
            "EV-UNRELATED-001 | affected-surface inspection: no entry, node, seam, "
            "activation, operation identity, runtime lifetime, placeholder, terminal, "
            "evidence/probe, or journey-state authority surface is modified or "
            "semantically affected"
        ),
    }
    assert permits_system_proof_na(positive)

    # A: NONE without a passing affected-surface check is not a bypass.
    assert not permits_system_proof_na(
        {"AFFECTED_CRITICAL_JOURNEYS": "NONE"}
    )

    # B: PASS without an evidence-backed N/A basis is not a bypass.
    assert not permits_system_proof_na(
        {
            "AFFECTED_CRITICAL_JOURNEYS": "NONE",
            "AFFECTED_JOURNEY_SURFACE_CHECK": "FAIL",
            "SYSTEM_PROOF_NOT_APPLICABLE_REASON": "no affected journey surface",
        }
    )

    # C: arbitrary non-empty text must not satisfy the bypass.
    assert not permits_system_proof_na(
        {
            "AFFECTED_CRITICAL_JOURNEYS": "NONE",
            "AFFECTED_JOURNEY_SURFACE_CHECK": "PASS",
            "SYSTEM_PROOF_NOT_APPLICABLE_REASON": "just because",
        }
    )

    # D: a reason without the canonical evidence reference/inspection basis fails.
    assert not permits_system_proof_na(
        {
            "AFFECTED_CRITICAL_JOURNEYS": "NONE",
            "AFFECTED_JOURNEY_SURFACE_CHECK": "PASS",
            "SYSTEM_PROOF_NOT_APPLICABLE_REASON": (
                "NOT-EVIDENCE-001 | affected-surface inspection: no affected journey"
            ),
        }
    )
    assert not permits_system_proof_na(
        {
            "AFFECTED_CRITICAL_JOURNEYS": "NONE",
            "AFFECTED_JOURNEY_SURFACE_CHECK": "PASS",
            "SYSTEM_PROOF_NOT_APPLICABLE_REASON": "EV-UNRELATED-001",
        }
    )

    # E: an affected journey cannot declare NONE and bypass system proof.
    assert not permits_system_proof_na(
        {
            "AFFECTED_CRITICAL_JOURNEYS": "J-001",
            "AFFECTED_JOURNEY_SURFACE_CHECK": "PASS",
            "SYSTEM_PROOF_NOT_APPLICABLE_REASON": (
                "EV-UNRELATED-001 | affected-surface inspection: no affected journey"
            ),
        }
    )


def test_aggregate_precedence_and_no_mutation() -> None:
    passing = check_critical_journey_smoke(_journey(_seam("pass")))
    blocked = check_critical_journey_smoke(
        _journey(
            _seam("blocked"),
            journey_id="J-002",
            observation_block="BLOCKED_BY_ENVIRONMENT",
        )
    )
    failing = check_critical_journey_smoke(
        _journey(
            _seam("fail", status="FAIL", identity_continuous=False),
            journey_id="J-003",
        )
    )
    before = asdict(failing)
    aggregate = check_system_traversability((passing, blocked, failing))
    assert aggregate.check_disposition == "WIRED_FAIL"
    assert aggregate.required_journey_ids == ("J-001", "J-002", "J-003")
    assert asdict(failing) == before


def test_aggregate_empty_required_set_is_not_applicable() -> None:
    result = check_system_traversability(
        (
            check_critical_journey_smoke(
                _journey(_seam("na"), applicability="NOT_APPLICABLE", current_state="NONE")
            ),
        )
    )
    assert result.check_disposition == "NOT_APPLICABLE"
    assert result.required_journey_ids == ()


def test_self_hosted_governed_operation_pre_correction() -> None:
    """Preserve the honest pre-correction red at the first absent seam."""
    resume = {
        "schema_version": 1,
        "status": "CURRENT",
        "git_identity": {"head": "a" * 40, "branch": "main"},
        "bootstrap": {
            "project_id": "fixture",
            "active_change": "CHG-PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-001",
            "lifecycle_stage": "Implementation",
            "stage_status": "In progress",
            "implementation_authorized": True,
            "open_blocker": None,
            "next_permitted_action": "EXECUTE_AUTHORIZED_TASK",
            "active_context_path": ".planning/changes/active/fixture/context.md",
            "source_revision": "a" * 40,
        },
        "selected_sources": [],
    }
    guidance: OperationGuidanceV1 = select_operation_guidance(resume)
    assert guidance["outcome"] == "MATCHED"
    assert guidance["operation"]["operation_id"] == "EXECUTE_CHANGE_TASK"

    ordinal = allocate_attempt_ordinal(
        (),
        change_id="CHG-PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-001",
        task_or_operation_id="T-05",
    )
    attempt = AttemptRecordV1(
        attempt_id="CHG-PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-001/T-05/A1",
        change_id="CHG-PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-001",
        task_or_operation_id="T-05",
        attempt_ordinal=ordinal,
        authorization_ref="OWNER_AUTHORIZATION_PL_SYSTEM_TRAVERSABILITY_IMPLEMENTATION",
        acceptance_contract_ref="AC-06",
        candidate_identity=CandidateIdentityV1(kind="GIT_COMMIT", head="a" * 40),
        baseline_refs=(IdentityRefV1(ref="HEAD", identity="a" * 40),),
        operation_guidance_ref="EXECUTE_AUTHORIZED_TASK",
    )
    assert attempt.attempt_ordinal == 1

    resume_module_path = Path("scripts/maintainer_resume.py").resolve()
    spec = importlib.util.spec_from_file_location("maintainer_resume_fixture", resume_module_path)
    assert spec is not None and spec.loader is not None
    resume_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(resume_module)
    assert resume_module.CURRENT_REL == "docs/design/project-spine/CURRENT.md"
    assert "next_permitted_action" in resume_module.REQUIRED_KEYS
    parsed = resume_module.parse_resume_block(
        "<!-- PLANNING_LITE_RESUME_CONTRACT_V1:BEGIN -->\n"
        + "\n".join(
            f"{key}: {'NO' if key == 'implementation_authorized' else 'fixture'}"
            for key in resume_module.REQUIRED_KEYS
        )
        + "\n<!-- PLANNING_LITE_RESUME_CONTRACT_V1:END -->"
    )
    assert parsed["next_permitted_action"] == "fixture"
    live_resume = resume_module.load_resume(Path.cwd())
    assert live_resume["resume_authority"] == resume_module.CURRENT_REL
    assert isinstance(live_resume["next_permitted_action"], str)
    assert live_resume["next_permitted_action"]

    # Bind the real downstream contract identities without fabricating any
    # receipt, result, evidence, technical evaluation, or next-gate continuity.
    assert callable(validate_receipt)
    assert ObservedResultV1 is not None
    assert VerifierEvidenceV1 is not None
    assert TechnicalEvaluationV1 is not None
    assert callable(evaluate_technical)

    result = check_critical_journey_smoke(
        _journey(
            _seam(
                "OperationGuidance -> Governed Operation Lifecycle",
                status="FAIL",
                identity_continuous=False,
                reason="NO_LEGITIMATE_RUNTIME_LIFETIME_OWNER",
                gap_class="ORCHESTRATION_GAP",
            ),
            _seam("Governed Operation Lifecycle -> Execution"),
            _seam("Execution -> validated RunReceipt"),
            _seam("validated RunReceipt -> PL08 Result/Evidence"),
            _seam("PL08 Result/Evidence -> authoritative Next Gate"),
        )
    )
    assert result.observed_traversability_state == "WIRED_FAIL"
    assert result.first_broken_seam == "OperationGuidance -> Governed Operation Lifecycle"
    assert result.gap_class == "ORCHESTRATION_GAP"
    assert result.seams[0].causal_reason == "NO_LEGITIMATE_RUNTIME_LIFETIME_OWNER"
    assert [item.disposition for item in result.seams[1:]] == [
        "DOWNSTREAM_UNREACHABLE",
        "DOWNSTREAM_UNREACHABLE",
        "DOWNSTREAM_UNREACHABLE",
        "DOWNSTREAM_UNREACHABLE",
    ]


def test_validator_has_no_authority_or_filesystem_surface() -> None:
    import planning_lite.traversability as module

    source = Path(module.__file__).read_text(encoding="utf-8")
    assert "Path(" not in source
    assert "open(" not in source
    assert "subprocess" not in source
    assert "CURRENT.md" not in source
    assert not hasattr(module, "write_project_state")
    assert not hasattr(module, "authorize")
    for forbidden in (
        "registry",
        "scheduler",
        "database",
        "event_store",
        "append-only",
        "persist",
    ):
        assert forbidden not in source.lower()
    carrier_paths = (
        Path("template/.planning/project/CRITICAL_JOURNEYS.md"),
        Path("template/.planning/templates/project/CRITICAL_JOURNEYS.md"),
    )
    before = tuple(path.read_bytes() for path in carrier_paths)
    result = check_critical_journey_smoke(_journey(_seam("pure")))
    assert result.check_disposition == "PASS"
    assert tuple(path.read_bytes() for path in carrier_paths) == before
    for authority_field in (
        "write_project_state",
        "next_gate",
        "route",
        "runtime_lifetime_owner",
    ):
        assert not hasattr(result, authority_field)
    for path in carrier_paths:
        carrier_text = path.read_text(encoding="utf-8").lower()
        assert "registry" not in carrier_text
        assert "event store" not in carrier_text


def test_attempt_access_seam_is_wired_traversable(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    change_id = "CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001"
    task_id = "T-08"
    head = "a" * 40
    authorization = issue_preparation_authorization(tmp_path, change_id, task_id, "OWNER-DECISION")
    payload = tmp_path / "preparation.json"
    payload.write_text(
        json.dumps(
            {
                "change_id": change_id,
                "task_or_operation_id": task_id,
                "authorization_ref": authorization,
                "acceptance_contract_ref": "AC-22",
                "candidate_identity": {"kind": "GIT_COMMIT", "head": head, "dirty_manifest": []},
                "baseline_refs": [{"ref": "HEAD", "identity": head}],
            }
        ),
        encoding="utf-8",
    )
    assert main(["attempt-prepare", str(tmp_path), "--input", str(payload)]) == 0
    attempt_id = capsys.readouterr().out.strip()
    assert lookup_attempt(tmp_path, attempt_id).outcome is LookupOutcome.FOUND
    assert check_activation_admissibility(tmp_path, attempt_id).outcome is AdmissibilityOutcome.ADMISSIBLE
    assert claim_attempt(tmp_path, attempt_id).runtime_state == "IN_FLIGHT"
    recovery = issue_recovery_authorization(tmp_path, attempt_id, "OWNER-RECOVERY")
    assert main(
        [
            "attempt-resolve-interrupted",
            str(tmp_path),
            attempt_id,
            "--authorization-ref",
            recovery,
        ]
    ) == 0
    capsys.readouterr()
    assert json.loads(attempt_store_path(tmp_path).read_text(encoding="utf-8"))["attempts"][0]["runtime_state"] == "TERMINAL"

    projection = check_critical_journey_smoke(
        _journey(
            _seam("Attempt Runtime Access"),
            _seam(
                "Governed Executor Callable Binding",
                status="FAIL",
                reachable=False,
                reason="GOVERNED_EXECUTOR_CALLABLE_BINDING / WIRING_GAP",
                gap_class="WIRING_GAP",
            ),
        )
    )
    assert projection.seams[0].disposition == "PASS"
    assert projection.first_broken_seam == "Governed Executor Callable Binding"
    assert projection.gap_class == "WIRING_GAP"


def test_decoy_authority_sources_cannot_authorize_attempts(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    payload = tmp_path / "decoy.json"
    payload.write_text(
        json.dumps(
            {
                "change_id": "CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001",
                "task_or_operation_id": "T-08",
                "authorization_ref": "authz_" + "0" * 32,
                "acceptance_contract_ref": "AC-22",
                "candidate_identity": {"kind": "GIT_COMMIT", "head": "a" * 40, "dirty_manifest": []},
                "baseline_refs": [{"ref": "HEAD", "identity": "a" * 40}],
                "decoy_source": ".local/CURRENT.md",
            }
        ),
        encoding="utf-8",
    )
    assert main(["attempt-prepare", str(tmp_path), "--input", str(payload)]) == 2
    capsys.readouterr()
    assert not attempt_store_path(tmp_path).exists()


def test_real_self_hosted_execute_entrypoint_reaches_lifecycle() -> None:
    parser = main.__globals__["build_parser"]()
    actions = next(action for action in parser._actions if getattr(action, "dest", None) == "command")
    assert "execute" in actions.choices
    assert "status" in actions.choices


def test_system_traversability_preserves_closed_boundaries() -> None:
    executor = Path(__file__).parents[1] / "src" / "planning_lite" / "governed_executor.py"
    lifecycle = Path(__file__).parents[1] / "src" / "planning_lite" / "operation_lifecycle.py"
    executor_text = executor.read_text(encoding="utf-8")
    lifecycle_text = lifecycle.read_text(encoding="utf-8")
    assert "collect_governed_receipt" not in executor_text
    assert "terminalize_attempt" not in executor_text
    assert "select_operation_guidance" not in lifecycle_text
    assert "next_gate" not in lifecycle_text


def test_template_checksum_matches_authorized_surface() -> None:
    root = Path(__file__).parents[1]
    adapter = root / "template" / ".planning" / "adapters" / "codex" / "README.md"
    checksum = root / "template" / ".planning" / "framework" / "SHA256SUMS.txt"
    expected = next(line.split()[0] for line in checksum.read_text(encoding="utf-8").splitlines() if line.endswith(".planning/adapters/codex/README.md"))
    assert hashlib.sha256(adapter.read_bytes().replace(b"\r\n", b"\n")).hexdigest() == expected


def test_downstream_executor_remains_next_break() -> None:
    result = check_critical_journey_smoke(
        _journey(
            _seam("Attempt Runtime Access"),
            _seam(
                "Governed Executor Callable Binding",
                status="FAIL",
                reachable=False,
                gap_class="WIRING_GAP",
            ),
        )
    )
    assert result.first_broken_seam == "Governed Executor Callable Binding"
    assert result.gap_class == "WIRING_GAP"
    assert result.observed_traversability_state == "WIRED_FAIL"


def test_false_done_shortcuts_are_rejected(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main(
        [
            "attempt-resolve-interrupted",
            str(tmp_path),
            "CHG/T/A1",
            "--authorization-ref",
            "authz_" + "0" * 32,
        ]
    ) == 2
    capsys.readouterr()
    assert not attempt_store_path(tmp_path).exists()
