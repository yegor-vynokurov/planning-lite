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
