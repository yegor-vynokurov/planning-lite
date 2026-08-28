from __future__ import annotations

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "template/.planning"

SURVEY = PLANNING / "assessments/PROJECT_SURVEY_TEMPLATE.md"
ASSESSMENT = PLANNING / "control/CURRENT_CAPABILITY_ASSESSMENT.md"
TARGET = PLANNING / "control/TARGET_BASELINE_CALIBRATION.md"
ASSESSMENTS_README = PLANNING / "assessments/README.md"
ROOT_ROUTER = PLANNING / "control/ROOT_ROUTER.md"
MODE_ROUTER = PLANNING / "control/MODE_ROUTER.md"
MANIFEST = PLANNING / "docs/MANIFEST_V4.md"
SHA_RECEIPTS = PLANNING / "framework/SHA256SUMS.txt"
BROWNFIELD_RECOVERY = PLANNING / "assessments/BROWNFIELD_RECOVERY_TEMPLATE.md"
OUTCOME_LADDER = PLANNING / "assessments/OUTCOME_LADDER_TEMPLATE.md"
DIRECTION_INVENTORY = PLANNING / "control/DIRECTION_INVENTORY.md"
TARGET_EXPLORER = PLANNING / "control/TARGET_STATE_EXPLORER.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def collapsed(path: Path) -> str:
    return re.sub(r"\s+", " ", read(path)).strip()


def canonical_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def manifest_paths() -> tuple[set[str], int]:
    text = read(MANIFEST)
    paths = set(re.findall(r"^- `([^`]+)`$", text, flags=re.MULTILINE))
    m = re.search(r"Files:\s*\*\*(\d+)\*\*\.", text)
    assert m is not None
    return paths, int(m.group(1))


def sha_receipts() -> dict[str, str]:
    out: dict[str, str] = {}
    for line in read(SHA_RECEIPTS).splitlines():
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        assert re.fullmatch(r"[0-9a-f]{64}", digest)
        assert rel not in out
        out[rel] = digest
    return out


def actual_template_paths() -> set[str]:
    return {
        ".planning/" + p.relative_to(PLANNING).as_posix()
        for p in PLANNING.rglob("*")
        if p.is_file()
    }


def test_project_survey_has_bounded_minimum_schema():
    text = read(SURVEY)
    required = {
        "# Project Survey",
        "## Evidence notation",
        "## System boundaries",
        "## Components / modules",
        "## Datastores / durable state",
        "## External integrations",
        "## Main execution paths",
        "## Build / test / run commands",
        "## Important conventions and source evidence",
        "## Material constraints",
        "## Relevant debt",
        "## Reusable assets",
        "## Unknown / not yet observed",
        "## Freshness / reuse decision",
    }
    for marker in required:
        assert marker in text

    for field in ("Reflects revision", "Survey scope", "Evidence sources"):
        assert field in text


def test_project_survey_is_evidence_not_project_truth_authority():
    text = collapsed(SURVEY)
    assert "SURVEY = AS-IS EVIDENCE" in text
    assert "TARGET = TO-BE ACCEPTED INTENT" in text

    for owner in (
        "CURRENT_STATE",
        "CURRENT_CAPABILITY_ASSESSMENT",
        "CAPABILITY_MODEL",
        "GAP_MAP",
        "TARGET_STATE",
        "ROADMAP",
    ):
        assert owner in text

    assert "does not own or replace" in text


def test_project_survey_uses_observed_inferred_unknown_without_inventing_intent():
    text = collapsed(SURVEY)
    for label in ("OBSERVED", "INFERRED", "UNKNOWN"):
        assert label in text
    assert "Do not convert observed implementation into claims about historical intent." in text


def test_current_capability_assessment_invokes_survey_only_on_three_part_trigger():
    text = collapsed(ASSESSMENT)

    a = "material brownfield/current-state work"
    b = "the assessment depends on repository/runtime structure"
    c = "existing current evidence is not sufficiently bounded/fresh"

    assert a in text
    assert b in text
    assert c in text

    trigger = re.search(
        re.escape(a) + r".{0,120}\bAND\b.{0,120}" +
        re.escape(b) + r".{0,120}\bAND\b.{0,120}" +
        re.escape(c),
        text,
    )
    assert trigger is not None


def test_routine_or_small_work_can_bypass_project_survey():
    text = collapsed(ASSESSMENT)
    assert "Routine or small work may bypass Project Survey." in text


def test_survey_freshness_is_material_and_scope_bounded():
    assessment = collapsed(ASSESSMENT)
    survey = collapsed(SURVEY)

    for text in (assessment, survey):
        assert "material repository/runtime drift" in text
        assert "surveyed scope" in text
        assert "Unrelated minor drift" in text

    for field in ("Reflects revision", "Survey scope", "Evidence sources"):
        assert field in assessment
        assert field in survey


def test_assessments_readme_documents_managed_vs_project_owned_split():
    text = collapsed(ASSESSMENTS_README)
    assert ".planning/assessments/PROJECT_SURVEY_TEMPLATE.md" in text
    assert ".planning/assessments/current/PROJECT_SURVEY.md" in text
    assert "managed" in text
    assert "project-owned" in text
    assert "must be preserved by update behavior" in text


def test_target_calibration_contains_bounded_determinacy_test():
    text = collapsed(TARGET)
    assert "Bounded Clarification Sweep" in text
    assert (
        "Can two reasonable implementers build materially different things "
        "while both satisfying the text?"
    ) in text
    assert "material ambiguity" in text


def test_clarification_preserves_question_owner_classes():
    text = read(TARGET)
    for owner in (
        "TARGET_BOUNDARY_QUESTION",
        "CAPABILITY_DESIGN_QUESTION",
        "RESEARCH_QUESTION",
    ):
        assert owner in text


def test_only_target_boundary_questions_hold_provisional_target_eligibility_open():
    text = collapsed(TARGET)
    assert (
        "Only `TARGET_BOUNDARY_QUESTION` blocks eligibility for "
        "`PROVISIONAL_TARGET_BASELINE`."
    ) in text
    assert (
        "`CAPABILITY_DESIGN_QUESTION` and `RESEARCH_QUESTION` do not hold Target "
        "eligibility open merely because downstream resolution is incomplete."
    ) in text


def test_clarification_has_bounded_stop_rule():
    text = collapsed(TARGET)
    assert "Clarification stops when every material Target-boundary ambiguity is either:" in text
    assert "RESOLVED or represented by an explicit TARGET_BOUNDARY_QUESTION" in text
    assert (
        "Do not continue clarification merely because downstream capability design "
        "or research remains unresolved."
    ) in text


def test_target_status_model_is_not_expanded():
    text = read(TARGET)
    assert "Canonical statuses:" in text
    tail = text.split("Canonical statuses:", 1)[1]
    parts = tail.split("```")
    assert len(parts) >= 3
    status_block = parts[1]

    for required in ("DRAFT", "PROVISIONAL_TARGET_BASELINE", "ACCEPTED"):
        assert required in status_block

    for forbidden in ("CONVERGED", "TARGET_CONVERGED", "SHAPING_READY"):
        assert forbidden not in status_block

    collapsed_target = collapsed(TARGET)
    assert re.search(
        r"(?:\*\*)?Target convergence(?:\*\*)?\s+means\s+eligibility\s+for\s+"
        r"`PROVISIONAL_TARGET_BASELINE`",
        collapsed_target,
    )


def test_glossary_remains_conditional_and_no_second_project_lexicon_is_created():
    text = collapsed(TARGET)
    assert ".planning/project/GLOSSARY.md" in text
    assert "only when meaningful term drift exists" in text
    assert re.search(
        r"do\s+not\s+create\s+a\s+second\s+Project\s+Lexicon",
        text,
        flags=re.IGNORECASE,
    )


def test_no_generic_research_execution_workflow_is_claimed():
    text = collapsed(TARGET)
    assert (
        "`RESEARCH_QUESTION` classification and preservation do not imply that a "
        "generic governed research execution workflow exists in this stage."
    ) in text


def test_project_shaping_foundation_does_not_add_router_entry_points():
    routers = collapsed(ROOT_ROUTER) + " " + collapsed(MODE_ROUTER)

    for forbidden in (
        "PROJECT_SURVEY_TEMPLATE.md",
        "Bounded Clarification Sweep",
        "SHAPING_READY",
        "TARGET_CONVERGED",
    ):
        assert forbidden not in routers


def test_manifest_and_sha_receipts_cover_the_current_template_tree():
    actual = actual_template_paths()
    listed, header_count = manifest_paths()
    receipts = sha_receipts()

    assert listed == actual
    assert header_count == len(actual)
    assert set(receipts) == actual - {".planning/framework/SHA256SUMS.txt"}

    for rel, expected in receipts.items():
        assert canonical_sha(ROOT / "template" / rel) == expected


def test_project_survey_is_registered_in_manifest_and_receipts():
    listed, _ = manifest_paths()
    receipts = sha_receipts()

    rel = ".planning/assessments/PROJECT_SURVEY_TEMPLATE.md"
    assert rel in listed
    assert rel in receipts
    assert canonical_sha(SURVEY) == receipts[rel]

def test_pl_v39_05_b_brownfield_recovery_contract():
    r=collapsed(BROWNFIELD_RECOVERY); i=collapsed(DIRECTION_INVENTORY)
    for x in ("REUSE_CURRENT_ACCEPTED_DIRECTION","RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL","BLOCKED_DIRECTION_CONFLICT","INSUFFICIENT_DIRECTION_EVIDENCE"):
        assert x in r
    for x in ("BR-STOP-01","BR-STOP-02","BR-STOP-03","BR-STOP-04"):
        assert x in r and x in i
    assert "Recovery alone must never promote this candidate to accepted Target intent." in i
    assert "Historical recovery is not required merely because older artifacts exist." in i
    assert "Do not silently merge conflicting authorities." in r

def test_pl_v39_05_b_outcome_ladder_contract():
    l=collapsed(OUTCOME_LADDER); e=collapsed(TARGET_EXPLORER)
    assert "The ladder never has greater authority than its grounding direction." in l
    assert "If the grounding direction is provisional, the ladder is provisional." in e
    assert "What observable project outcome is true at this level?" in e
    assert "What should we implement next?" in e
    for x in ("implement API","add tests","write docs"): assert x in l
    assert "They are not ladder levels." in l
    assert "Minimum useful stopping level" in l

def test_pl_v39_05_b_later_shaping_remains_deferred():
    e=re.sub(r"\s+"," ",collapsed(TARGET_EXPLORER))
    for x in ("Adaptive Engagement","Strategy Portfolio","Target Skeleton","Executable Target Contract"):
        assert x in e

def test_pl_v39_05_b_docs_and_integrity_registration():
    d=collapsed(ASSESSMENTS_README)
    listed,_=manifest_paths(); receipts=sha_receipts()
    for rel,path in (
        (".planning/assessments/BROWNFIELD_RECOVERY_TEMPLATE.md",BROWNFIELD_RECOVERY),
        (".planning/assessments/OUTCOME_LADDER_TEMPLATE.md",OUTCOME_LADDER),
    ):
        assert rel in d and rel in listed and rel in receipts
        assert canonical_sha(path)==receipts[rel]
    for rel in (".planning/assessments/current/BROWNFIELD_RECOVERY.md",".planning/assessments/current/OUTCOME_LADDER.md"):
        assert rel in d
    assert "must be preserved by update behavior" in d
