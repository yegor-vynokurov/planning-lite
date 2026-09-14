from __future__ import annotations

import re
from pathlib import Path

import pathspec
import yaml


ROOT = Path(__file__).resolve().parents[1]
TPL = ROOT / "template/.planning"

UNIT_STATES = {
    "IMPLEMENTED",
    "STILL_OPEN",
    "CARRIED_FORWARD",
    "FUTURE_SEED",
    "DEFERRED",
    "REJECTED",
    "SUPERSEDED",
    "NEEDS_REFRAME",
    "UNCERTAIN",
}

PARENT_STATES = {
    "OPEN",
    "COMPLETED",
    "PARTIALLY_REALIZED",
    "CLOSED_WITH_CARRYFORWARD",
    "DEFERRED",
    "SUPERSEDED",
    "REJECTED",
    "UNANCHORED",
    "NEEDS_REFRAME",
    "UNCERTAIN",
}

DISCOVERY_MANAGED = {
    ".planning/discoveries/README.md",
    ".planning/discoveries/TEMPLATE.md",
}
DISCOVERY_PROJECT = {
    ".planning/discoveries/INDEX.md",
    ".planning/discoveries/items/**",
}


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _yaml(rel: str):
    return yaml.safe_load(_read(rel))


def _code_block_after(text: str, heading: str) -> set[str]:
    pos = text.index(heading)
    tail = text[pos:]
    match = re.search(r"```text\s*\n(.*?)\n```", tail, flags=re.DOTALL)
    assert match, heading
    return {line.strip() for line in match.group(1).splitlines() if line.strip()}


def _marker_block(text: str, marker: str) -> str:
    begin = f"<!-- {marker}:BEGIN -->"
    end = f"<!-- {marker}:END -->"
    assert text.count(begin) == 1
    assert text.count(end) == 1
    return text.split(begin, 1)[1].split(end, 1)[0]


def test_discovery_exists_and_has_no_executable_authority() -> None:
    lifecycle_path = TPL / "control/DISCOVERY_LIFECYCLE.md"
    assert lifecycle_path.is_file()
    lifecycle = lifecycle_path.read_text(encoding="utf-8")
    assert {"OPEN", "RESOLVED", "SUPERSEDED"} <= set(re.findall(r"\b[A-Z_]+\b", lifecycle))
    assert "There is no `ABSORBED` Discovery status." in lifecycle
    assert "Discovery status != Recommendation status" in lifecycle
    assert "Discovery status != implementation authority" in lifecycle
    assert "A Discovery MUST NOT by itself:" in lifecycle
    assert "authorize implementation;" in lifecycle
    assert "create or approve a Change;" in lifecycle


def test_discovery_ownership_is_exact() -> None:
    ownership = _yaml("template/.planning/framework/OWNERSHIP.yml")
    managed = set(ownership["managed"])
    project = set(ownership["project_owned"])

    assert {x for x in managed if x.startswith(".planning/discoveries/")} == DISCOVERY_MANAGED
    assert {x for x in project if x.startswith(".planning/discoveries/")} == DISCOVERY_PROJECT
    assert not (DISCOVERY_MANAGED & DISCOVERY_PROJECT)


def test_copier_preserves_discovery_project_owned_state() -> None:
    copier = _yaml("copier.yml")
    skip = set(copier["_skip_if_exists"])
    discovery_skip = {x for x in skip if x.startswith(".planning/discoveries/")}
    assert discovery_skip == DISCOVERY_PROJECT


def test_template_tree_is_fully_classified_for_local_only_update() -> None:
    ownership = _yaml("template/.planning/framework/OWNERSHIP.yml")
    managed_spec = pathspec.PathSpec.from_lines("gitwildmatch", ownership["managed"])
    project_spec = pathspec.PathSpec.from_lines("gitwildmatch", ownership["project_owned"])

    unknown: list[str] = []
    overlap: list[str] = []

    for path in sorted(TPL.rglob("*")):
        if not path.is_file():
            continue
        rendered = ".planning/" + path.relative_to(TPL).as_posix()
        if rendered.endswith(".jinja"):
            rendered = rendered[:-len(".jinja")]

        is_managed = managed_spec.match_file(rendered)
        is_project = project_spec.match_file(rendered)

        if not is_managed and not is_project:
            unknown.append(rendered)
        if is_managed and is_project:
            overlap.append(rendered)

    assert unknown == []
    # Legacy ownership may contain pre-existing intentional overlap. The FCP
    # invariant is narrower: every template file must be classified, and the
    # seven new FCP template files must not introduce new ownership overlap.
    fcp_added = {
        ".planning/control/DISCOVERY_LIFECYCLE.md",
        ".planning/control/RECOMMENDATION_ABSORPTION.md",
        ".planning/disciplines/CONTRACT_CLOSURE.md",
        ".planning/discoveries/README.md",
        ".planning/discoveries/INDEX.md",
        ".planning/discoveries/TEMPLATE.md",
        ".planning/discoveries/items/.gitkeep",
    }
    assert sorted(set(overlap) & fcp_added) == []


def test_recommendation_unit_vocabulary_is_canonical_and_exact() -> None:
    absorption = _read("template/.planning/control/RECOMMENDATION_ABSORPTION.md")
    states = _code_block_after(
        absorption,
        "## Canonical RecommendationUnit reconciliation states",
    )
    assert states == UNIT_STATES

    lifecycle = _read("template/.planning/control/RECOMMENDATION_LIFECYCLE.md")
    for state in UNIT_STATES:
        assert state in lifecycle


def test_parent_recommendation_state_is_separate() -> None:
    absorption = _read("template/.planning/control/RECOMMENDATION_ABSORPTION.md")
    parent = _code_block_after(
        absorption,
        "### 5. Derive parent reconciliation state separately",
    )
    assert parent == PARENT_STATES
    assert "Recommendation lifecycle Status" in absorption
    assert "RecommendationUnit reconciliation state" in absorption
    assert "parent Recommendation reconciliation state" in absorption


def test_recommendation_residue_is_exhaustive_and_ambiguity_blocks() -> None:
    absorption = _read("template/.planning/control/RECOMMENDATION_ABSORPTION.md")
    assert "all in-scope durable Recommendation units are accounted for" in absorption
    assert "### Material placement ambiguity" in absorption
    block = absorption.split("### Material placement ambiguity", 1)[1]
    assert "BLOCK" in block
    assert "Do not guess." in block
    assert "create a Roadmap item;" in absorption
    assert "create or approve a Change;" in absorption
    assert "authorize implementation;" in absorption


def test_readiness_is_exhaustive_and_preserves_independent_work() -> None:
    readiness = _marker_block(
        _read("template/.planning/control/CHANGE_READINESS.md"),
        "PL_FCP_EXHAUSTIVE_READINESS_V1",
    )
    n = _norm(readiness)
    assert _norm("Do not stop after the first independent blocker.") in n
    assert _norm("complete known in-scope blocker set") in n
    assert _norm("independent legal work") in n
    assert _norm("Two independent blockers must both be reportable in the same Readiness pass.") in n
    assert _norm("Readiness PASS != Execution authorization") in n


def test_contract_closure_is_conditional_and_simple_leaf_can_be_na() -> None:
    closure = _read("template/.planning/disciplines/CONTRACT_CLOSURE.md")
    for dimension in ("SHAPE", "SEMANTICS", "ENCODING", "OWNERSHIP"):
        assert dimension in closure
    assert {"CLOSED", "BLOCKED", "N/A"} <= set(re.findall(r"\b(?:CLOSED|BLOCKED|N/A)\b", closure))
    assert "simple leaf task may legitimately record all heavyweight closure dimensions" in closure
    assert "Materiality / Simplicity challenge" in closure
    assert "If a simpler bounded repair closes the approved contract, prefer it." in closure
    assert "Determinacy is conditional." in closure


def test_readiness_template_records_multiple_blockers_and_conditional_closure() -> None:
    template = _marker_block(
        _read("template/.planning/changes/templates/readiness.md"),
        "PL_FCP_READINESS_RECORD_V1",
    )
    assert "Independent blocker ledger" in template
    assert "independent legal work still allowed" in template
    assert "CLOSED | BLOCKED | N/A" in template
    assert "simple leaf Change" in template
    assert "NOT IMPLIED BY READINESS" in template


def test_execution_semantic_choice_guard_blocks_material_invention() -> None:
    execution = _marker_block(
        _read("template/.planning/control/CHANGE_EXECUTION.md"),
        "PL_FCP_EXECUTION_CONTROL_V1",
    )
    for dimension in (
        "science",
        "evidence",
        "identity",
        "persistence",
        "authorization",
        "cross-task ownership",
        "downstream interface semantics",
    ):
        assert dimension in execution
    assert "stop only the dependent slice" in execution
    assert "Do not guess" in execution


def test_blocker_locality_preserves_independent_legal_work() -> None:
    execution = _marker_block(
        _read("template/.planning/control/CHANGE_EXECUTION.md"),
        "PL_FCP_EXECUTION_CONTROL_V1",
    )
    assert "A blocker stops only the work that depends on it" in execution
    assert "independent work still allowed" in execution
    assert "An independently closed task remains permitted" in execution
    assert "shared contract" in execution


def test_context_exposes_exact_execution_envelope_fields() -> None:
    context = _marker_block(
        _read("template/.planning/changes/templates/context.md"),
        "PL_FCP_EXECUTION_CONTEXT_V1",
    )
    fields = {
        "Authorized task(s)",
        "Allowed write surface",
        "Relevant read-only surface",
        "Forbidden/downstream surface",
        "Tool/network constraints when material",
        "Owned responsibility",
        "Next permitted action",
    }
    seen = {
        line.split(":", 1)[0].lstrip("- ").strip()
        for line in context.splitlines()
        if line.startswith("- ") and ":" in line
    }
    assert fields <= seen


def test_context_exposes_exact_six_structured_blocker_fields() -> None:
    context = _marker_block(
        _read("template/.planning/changes/templates/context.md"),
        "PL_FCP_EXECUTION_CONTEXT_V1",
    )
    blocker = context.split("## Structured blocked outcome", 1)[1]
    fields = {
        "failure_class",
        "evidence",
        "blocked_slice",
        "independent_work_still_allowed",
        "missing_decision_owner",
        "next_permitted_action",
    }
    seen = {
        line.split(":", 1)[0].lstrip("- ").strip()
        for line in blocker.splitlines()
        if line.startswith("- ") and ":" in line
    }
    assert seen == fields


def test_closed_world_positive_and_nearest_wrong_semantics_are_shared() -> None:
    closure = _read("template/.planning/disciplines/CONTRACT_CLOSURE.md")
    execution = _read("template/.planning/control/CHANGE_EXECUTION.md")
    for token in ("canonical-positive", "nearest-wrong"):
        assert token in closure
        assert token in execution


def test_pilot_protocols_are_not_universal_modes_skills_or_stages() -> None:
    forbidden_names = ("converge", "independent-task-closure", "task-closure-review")
    universal_paths = [
        p.relative_to(TPL).as_posix().lower()
        for base in (TPL / "modes", TPL / "skills")
        if base.exists()
        for p in base.rglob("*")
        if p.is_file()
    ]
    for path in universal_paths:
        assert not any(token in path for token in forbidden_names)

    router = _read("template/.planning/control/ROOT_ROUTER.md")
    assert "Independent Task Closure Review" not in router
    assert not re.search(r"\bCONVERGE\b", router)


def test_existing_lifecycle_authority_remains_distinct() -> None:
    readiness = _read("template/.planning/control/CHANGE_READINESS.md")
    execution = _read("template/.planning/control/CHANGE_EXECUTION.md")
    absorption = _read("template/.planning/control/RECOMMENDATION_ABSORPTION.md")

    assert "Readiness PASS != Execution authorization" in readiness
    assert "Use in Execution mode only after Gate D is satisfied." in execution
    assert "Absorption MUST NOT automatically:" in absorption
    assert "authorize implementation;" in absorption


def test_deterministic_operation_guidance_ownership_and_gate_contract() -> None:
    planning = _read("template/.planning/control/CHANGE_PLANNING.md")
    readiness = _read("template/.planning/control/CHANGE_READINESS.md")
    execution = _read("template/.planning/control/CHANGE_EXECUTION.md")
    checkpoint = _read("template/.planning/control/SESSION_CHECKPOINT.md")
    gates = _read("template/.planning/control/APPROVAL_GATES.md")
    ownership = _read("template/.planning/control/STATE_OWNERSHIP.md")

    assert "RUN_FORMAL_READINESS" in planning
    assert "RUN_FORMAL_READINESS" in readiness
    assert "FORMAL_READINESS_V1" in readiness
    assert "EXECUTE_AUTHORIZED_TASK" in execution
    assert "EXECUTE_AUTHORIZED_CONTRACT_TASK" in execution
    assert "GIT_STAGE" in checkpoint and "GIT_COMMIT" in checkpoint
    assert "PRODUCT_WRITE" in gates and "live-consumer" in gates
    assert "derived, non-persistent" in ownership

    canonical = [
        "planning-audit",
        "planning-checkpoint",
        "planning-dialogue",
        "planning-plan",
        "planning-execute",
        "planning-git-review",
        "planning-quick-fix",
        "planning-recover",
    ]
    assert len(canonical) == 8
    for skill in canonical[:4]:
        assert "planning" in _read(f"template/.planning/skills/{skill}/SKILL.md").lower()
        assert "canonical" in _read(f"template/.agents/skills/{skill}/SKILL.md").lower()
    assert not (TPL / "skills" / "operation-guidance").exists()
    assert "registry" not in planning.lower()


def test_field_control_pack_does_not_introduce_deferred_runtime_scope() -> None:
    governed = "\n".join(
        _read(rel)
        for rel in (
            "template/.planning/control/DISCOVERY_LIFECYCLE.md",
            "template/.planning/control/RECOMMENDATION_ABSORPTION.md",
            "template/.planning/disciplines/CONTRACT_CLOSURE.md",
            "template/.planning/control/CHANGE_READINESS.md",
            "template/.planning/control/CHANGE_EXECUTION.md",
            "template/.planning/changes/templates/context.md",
        )
    )

    assert ".planning/campaign" not in governed
    assert "planning-lite-campaign" not in governed
    assert "generic Eval Core" not in governed
    assert "automatic Execution Pattern" not in governed

    assert not (ROOT / "src/planning_lite/field_control_pack.py").exists()
    assert not (TPL / "modes/field-control-pack.md").exists()
    assert not (TPL / "skills/field-control-pack").exists()


def test_execution_routing_is_managed_and_single_source() -> None:
    routing_path = TPL / "control/EXECUTION_ROUTING.md"
    assert routing_path.is_file()
    routing = routing_path.read_text(encoding="utf-8")
    for capability in (
        "DETERMINISTIC_OR_TOOL_PREFERRED",
        "BOUNDED_MODEL_CAPABLE",
        "STRONG_JUDGMENT_REQUIRED",
    ):
        assert capability in routing
    for required in (
        "authority/envelope",
        "strongest material requirement",
        "deterministic subwork",
        "Result Contract",
        "mission",
        "source/scope boundary",
        "questions",
        "required evidence",
        "output contract",
        "escalation rule",
        "child/model result is evidence, not owner acceptance",
        "stronger-than-default",
        "nested delegation",
    ):
        assert required in routing
    assert routing.count("DETERMINISTIC_OR_TOOL_PREFERRED") == 1
    assert not (TPL / "control/EXECUTION_ROUTING.yml").exists()


def test_root_router_conditionally_activates_execution_routing_without_duplication() -> None:
    router = _read("template/.planning/control/ROOT_ROUTER.md")
    assert "EXECUTION_ROUTING.md" in router
    assert ".planning/AGENT_PROFILE.yml" in router
    assert "active adapter" in router
    activation = router.lower()
    assert activation.count("execution_routing.md") == 1
    assert "DETERMINISTIC_OR_TOOL_PREFERRED" not in router
    assert "GPT-5.6 Luna" not in router
    assert "Result Contract fields" not in router
    assert "nested delegation" not in router.lower()


def test_codex_adapter_owns_fail_closed_model_binding_and_result_contract() -> None:
    adapter = _read("template/.planning/adapters/codex/README.md")
    for required in (
        "GPT-5.6 Sol / High",
        "GPT-5.6 Luna / Extra High",
        "REQUESTED_BINDING",
        "CONFIRMED_BINDING",
        "MODEL_SELF_REPORT",
        "never sufficient binding evidence",
        "current-turn execution",
        "post-turn mismatch",
        "BOUNDED_MODEL_CAPABLE",
        "does not self-authorize",
        "exact scope",
        "required evidence",
        "STOP conditions",
        "revision/hash binding",
        "next gate",
        "cannot widen scope",
        "cannot grant owner acceptance",
        "stronger-model escalation remains STOP",
        "nested delegation",
        "mission",
        "source/scope boundary",
        "questions",
        "output contract",
        "escalation rule",
    ):
        assert required in adapter
    assert "model self-report" in adapter.lower()
    assert "owner acceptance" in adapter.lower()


def test_execution_routing_manifest_and_canonical_lf_integrity() -> None:
    manifest = _read("template/.planning/docs/MANIFEST_V4.md")
    assert ".planning/control/EXECUTION_ROUTING.md" in manifest
    assert manifest.startswith("# Planning Lite 4.x template `.planning` manifest\n")

    checksum_path = TPL / "framework/SHA256SUMS.txt"
    checksums = checksum_path.read_text(encoding="utf-8")
    assert ".planning/control/EXECUTION_ROUTING.md" in checksums
    assert "  .planning/control/EXECUTION_ROUTING.md\n" in checksums
    for line in checksums.splitlines():
        if line.endswith("  .planning/control/EXECUTION_ROUTING.md"):
            assert re.fullmatch(r"[0-9a-f]{64}  \.planning/control/EXECUTION_ROUTING\.md", line)
            break
    else:
        raise AssertionError("missing canonical checksum entry")

    assert "EXECUTION_ROUTING.md" not in _read("template/.planning/framework/OWNERSHIP.yml")
