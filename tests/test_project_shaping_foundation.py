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
