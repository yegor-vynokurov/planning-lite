from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "scripts/maintainer_resume.py"
CURRENT = ROOT / "docs/design/project-spine/CURRENT.md"
LEGACY = ROOT / "docs/design/project-spine/PL-V38-CURRENT.md"
IA = ROOT / "docs/design/project-spine/INFORMATION-ARCHITECTURE-v1.md"
README = ROOT / "README.md"
OPERATOR = ROOT / "docs/OPERATOR_WORKFLOW.ru.md"

def load_helper():
    spec = importlib.util.spec_from_file_location("maintainer_resume", HELPER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module

def run(cmd, cwd: Path):
    return subprocess.run(
        cmd, cwd=str(cwd), text=True, capture_output=True,
        encoding="utf-8", errors="replace"
    )

def block(**overrides):
    values = {
        "repository_role": "CENTRAL_SOURCE",
        "resume_authority": "docs/design/project-spine/CURRENT.md",
        "current_roadmap": "docs/design/project-spine/roadmap/ROADMAP.md",
        "active_change": "CHG-TEST-001",
        "lifecycle_gate": "TEST",
        "implementation_authorized": "NO",
        "blockers": "NONE",
        "next_permitted_action": "test_next_action",
        "last_transition_receipt": "NONE",
        "state_as_of": "2026-08-25",
    }
    values.update(overrides)
    return "\n".join(
        ["<!-- PLANNING_LITE_RESUME_CONTRACT_V1:BEGIN -->"]
        + [f"{k}: {v}" for k, v in values.items()]
        + ["<!-- PLANNING_LITE_RESUME_CONTRACT_V1:END -->"]
    )

def make_fixture(tmp_path: Path, *, git: bool = True, name: str = "arbitrary-central"):
    root = tmp_path / name
    (root / "scripts").mkdir(parents=True)
    (root / "docs/design/project-spine/roadmap").mkdir(parents=True)
    shutil.copy2(HELPER, root / "scripts/maintainer_resume.py")
    (root / "docs/design/project-spine/CURRENT.md").write_text(
        "# Current\n\n" + block() + "\n", encoding="utf-8"
    )
    (root / "docs/design/project-spine/roadmap/ROADMAP.md").write_text(
        "# Roadmap\n", encoding="utf-8"
    )
    (root / "pyproject.toml").write_text(
        "[project]\nname='fixture'\nversion='0.0.0'\n", encoding="utf-8"
    )
    (root / "copier.yml").write_text("_subdirectory: template\n", encoding="utf-8")
    (root / "template").mkdir()
    if git:
        assert run(["git", "init", "-b", "main"], root).returncode == 0
        assert run(["git", "config", "user.email", "resume-test@example.invalid"], root).returncode == 0
        assert run(["git", "config", "user.name", "Resume Test"], root).returncode == 0
        assert run(["git", "add", "."], root).returncode == 0
        assert run(["git", "commit", "-m", "fixture"], root).returncode == 0
    return root

def test_helper_succeeds_in_valid_arbitrarily_named_checkout(tmp_path):
    root = make_fixture(tmp_path, git=True, name="not-called-planning-lite")
    p = run([sys.executable, "scripts/maintainer_resume.py"], root)
    assert p.returncode == 0, p.stderr
    assert "Planning Lite CENTRAL SOURCE RESUME" in p.stdout
    assert str(root.resolve()) in p.stdout
    assert "active Change:" in p.stdout
    assert "CHG-TEST-001" in p.stdout
    assert "working tree:\n  CLEAN" in p.stdout

def test_non_git_snapshot_fails_closed_even_with_central_markers(tmp_path):
    root = make_fixture(tmp_path, git=False, name="planning-lite")
    p = run([sys.executable, "scripts/maintainer_resume.py"], root)
    assert p.returncode != 0
    assert "NOT A VERIFIED CENTRAL GIT CHECKOUT" in p.stderr

def test_parse_requires_exactly_one_block():
    m = load_helper()
    with pytest.raises(m.ResumeError):
        m.parse_resume_block("# none")
    with pytest.raises(m.ResumeError):
        m.parse_resume_block(block() + "\n" + block())

def test_parse_rejects_malformed_duplicate_missing_and_extra_keys():
    m = load_helper()
    with pytest.raises(m.ResumeError):
        m.parse_resume_block(block().replace("blockers: NONE", "blockers NONE"))
    with pytest.raises(m.ResumeError):
        m.parse_resume_block(block().replace("blockers: NONE", "blockers: NONE\nblockers: AGAIN"))
    with pytest.raises(m.ResumeError):
        m.parse_resume_block(block().replace("blockers: NONE\n", ""))
    with pytest.raises(m.ResumeError):
        m.parse_resume_block(block().replace("blockers: NONE", "blockers: NONE\nsurprise: value"))

def test_parse_requires_yes_no_authorization():
    m = load_helper()
    with pytest.raises(m.ResumeError):
        m.parse_resume_block(block(implementation_authorized="MAYBE"))

def test_load_resume_requires_exact_canonical_paths_and_no_escape(tmp_path):
    m = load_helper()
    root = make_fixture(tmp_path, git=False)
    current = root / "docs/design/project-spine/CURRENT.md"
    current.write_text("# Current\n\n" + block(resume_authority="README.md") + "\n", encoding="utf-8")
    with pytest.raises(m.ResumeError):
        m.load_resume(root)
    current.write_text("# Current\n\n" + block(current_roadmap="../../outside.md") + "\n", encoding="utf-8")
    with pytest.raises(m.ResumeError):
        m.load_resume(root)

def test_non_none_transition_receipt_must_exist(tmp_path):
    m = load_helper()
    root = make_fixture(tmp_path, git=False)
    current = root / "docs/design/project-spine/CURRENT.md"
    current.write_text(
        "# Current\n\n" + block(last_transition_receipt="docs/missing.md") + "\n",
        encoding="utf-8",
    )
    with pytest.raises(m.ResumeError):
        m.load_resume(root)

def test_legacy_current_self_disqualifies():
    text = LEGACY.read_text(encoding="utf-8-sig")
    assert "LEGACY CHECKPOINT / NOT CURRENT RESUME AUTHORITY" in text
    assert "docs/design/project-spine/CURRENT.md" in text

def test_information_architecture_encodes_precedence_and_lab_boundary():
    text = IA.read_text(encoding="utf-8-sig")
    for item in [
        "Authority precedence",
        "live Git checkout identity",
        "docs/design/project-spine/CURRENT.md",
        "docs/design/project-spine/roadmap/ROADMAP.md",
        ".planning-lab/**",
        "must not silently override",
    ]:
        assert item in text

def test_root_and_operator_docs_explain_central_resume_boundary():
    readme = README.read_text(encoding="utf-8-sig")
    operator = OPERATOR.read_text(encoding="utf-8-sig")
    for item in [
        "central source repository",
        "scripts/maintainer_resume.py",
        "docs/design/project-spine/CURRENT.md",
        "planning-lite doctor .",
    ]:
        assert item in readme
    assert "Resume / New Chat / New Maintainer" in operator
    assert "scripts/maintainer_resume.py" in operator
    assert "resume safety" in operator
    assert "implementation readiness" in operator

def test_helper_is_read_only_on_actual_checkout():
    before = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], ROOT)
    assert before.returncode == 0
    p = run([sys.executable, str(HELPER)], ROOT)
    assert p.returncode == 0, p.stderr
    after = run(["git", "status", "--porcelain=v1", "--untracked-files=all"], ROOT)
    assert after.returncode == 0
    assert after.stdout == before.stdout

def test_dirty_checkout_is_reported_but_resume_succeeds(tmp_path):
    root = make_fixture(tmp_path, git=True)
    (root / "dirty.txt").write_text("dirty\n", encoding="utf-8")
    p = run([sys.executable, "scripts/maintainer_resume.py"], root)
    assert p.returncode == 0, p.stderr
    assert "working tree:\n  DIRTY(" in p.stdout

def test_current_contains_complete_semantic_resume_state():
    m = load_helper()
    data = m.parse_resume_block(CURRENT.read_text(encoding="utf-8-sig"))
    assert tuple(data.keys()) == m.REQUIRED_KEYS
    assert data["repository_role"] == "CENTRAL_SOURCE"
    assert data["resume_authority"] == m.CURRENT_REL
    assert data["current_roadmap"] == m.ROADMAP_REL

def test_no_duplicate_mutable_central_state_store():
    forbidden = [
        ROOT / "CENTRAL_STATE.yml",
        ROOT / "CENTRAL_STATE.json",
        ROOT / "PROJECT_STATE.json",
        ROOT / "docs/design/project-spine/CURRENT2.md",
        ROOT / "docs/design/project-spine/MASTER_ROADMAP.md",
        ROOT / "docs/design/project-spine/META_ROADMAP.md",
    ]
    assert not any(p.exists() for p in forbidden)
