from __future__ import annotations

from pathlib import Path

import yaml

from planning_lite.cli import _iter_required_paths


def _root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_direction_project_artifacts_have_matching_pristine_copies() -> None:
    root = _root()
    for name in ("TARGET_STATE.md", "CAPABILITY_MODEL.md"):
        project = (root / f"template/.planning/project/{name}").read_text(encoding="utf-8")
        pristine = (root / f"template/.planning/templates/project/{name}").read_text(
            encoding="utf-8"
        )
        assert project == pristine


def test_direction_artifacts_follow_existing_ownership_boundary() -> None:
    root = _root()
    ownership = yaml.safe_load(
        (root / "template/.planning/framework/OWNERSHIP.yml").read_text(encoding="utf-8")
    )

    assert ".planning/project/**" in ownership["project_owned"]
    assert ".planning/templates/**" in ownership["managed"]
    assert ".planning/control/**" in ownership["managed"]

    copier = yaml.safe_load((root / "copier.yml").read_text(encoding="utf-8"))
    assert ".planning/project/**" in copier["_skip_if_exists"]


def test_direction_workflows_are_routed_and_versioned() -> None:
    root = _root()
    router = (root / "template/.planning/control/ROOT_ROUTER.md").read_text(encoding="utf-8")
    modes = (root / "template/.planning/control/MODE_ROUTER.md").read_text(encoding="utf-8")
    workflow = (root / "template/.planning/WORKFLOW.md").read_text(encoding="utf-8")
    prompt = (
        root / "template/.planning/prompts/02-refine-project-goal-and-completion-criteria.md"
    ).read_text(encoding="utf-8")

    expected = {
        "DIRECTION_INVENTORY.md": "PW-DIR-001",
        "TARGET_STATE_EXPLORER.md": "PW-DIR-002",
        "TARGET_BASELINE_CALIBRATION.md": "PW-DIR-003",
    }
    for name, workflow_id in expected.items():
        content = (root / f"template/.planning/control/{name}").read_text(encoding="utf-8")
        assert workflow_id in content
        assert name in router or name in prompt
        assert name in workflow

    assert "DIRECTION_INVENTORY.md" in modes
    assert "TARGET_STATE_EXPLORER.md" in modes
    assert "TARGET_BASELINE_CALIBRATION.md" in modes


def test_direction_foundation_preserves_human_target_authority() -> None:
    root = _root()
    explorer = (
        root / "template/.planning/control/TARGET_STATE_EXPLORER.md"
    ).read_text(encoding="utf-8")
    calibration = (
        root / "template/.planning/control/TARGET_BASELINE_CALIBRATION.md"
    ).read_text(encoding="utf-8")
    target = (root / "template/.planning/project/TARGET_STATE.md").read_text(encoding="utf-8")

    assert "PROVISIONAL_TARGET_BASELINE" in calibration
    assert "ACCEPTED" in calibration
    assert "explicit user" in calibration.lower()
    assert "TARGET_STATE_SIGNAL" in calibration
    assert "CURRENT_BASELINE" in calibration
    assert "explicit user acceptance" in calibration.lower()
    assert "DRAFT" in explorer
    assert "TARGET_BOUNDARY_QUESTION" in target
    assert "CAPABILITY_DESIGN_QUESTION" in target
    assert "RESEARCH_QUESTION" in target


def test_direction_inventory_has_fail_closed_consistency_gate() -> None:
    root = _root()
    inventory = (
        root / "template/.planning/control/DIRECTION_INVENTORY.md"
    ).read_text(encoding="utf-8")

    assert "Current-State Consistency Gate" in inventory
    assert "PASS" in inventory
    assert "FAIL" in inventory
    assert "UNCERTAIN" in inventory
    assert "git clean" in inventory.lower()
    assert "stop before Target exploration" in inventory


def test_capability_model_is_not_current_state_or_gap_map() -> None:
    root = _root()
    capability = (root / "template/.planning/project/CAPABILITY_MODEL.md").read_text(
        encoding="utf-8"
    )

    assert "not tasks" in capability.lower()
    assert "SATISFIED" in capability
    assert "PARTIAL" in capability
    assert "do not record" in capability.lower()
    assert not (root / "template/.planning/project/GAP_MAP.md").exists()
    assert not (root / "template/.planning/control/CAUSAL_GAP_DERIVATION.md").exists()


def test_doctor_requires_first_class_direction_project_files() -> None:
    required = set(_iter_required_paths())
    assert ".planning/project/TARGET_STATE.md" in required
    assert ".planning/project/CAPABILITY_MODEL.md" in required


def test_context_policy_has_direction_stage_profiles() -> None:
    root = _root()
    context = (root / "template/.planning/control/CONTEXT_POLICY.md").read_text(
        encoding="utf-8"
    )

    assert "Direction-stage context profiles" in context
    assert "Direction inventory" in context
    assert "Target-State exploration" in context
    assert "Target baseline calibration" in context
    assert "do not authorize a Context Compiler" in context


def test_planning_manifest_and_sha_receipt_match_template_tree() -> None:
    import hashlib
    import re

    root = _root() / "template/.planning"
    manifest_path = root / "docs/MANIFEST_V4.md"
    sha_path = root / "framework/SHA256SUMS.txt"

    actual = {
        ".planning/" + path.relative_to(root).as_posix()
        for path in root.rglob("*")
        if path.is_file()
    }

    manifest = manifest_path.read_text(encoding="utf-8")
    listed = set(re.findall(r"^- `([^`]+)`$", manifest, flags=re.MULTILINE))
    assert listed == actual
    assert f"Files: **{len(actual)}**." in manifest

    receipts: dict[str, str] = {}
    for line in sha_path.read_text(encoding="utf-8").splitlines():
        digest, path = line.split("  ", 1)
        receipts[path] = digest

    expected_receipt_paths = actual - {".planning/framework/SHA256SUMS.txt"}
    assert set(receipts) == expected_receipt_paths
    for relative, digest in receipts.items():
        path = root.parent / relative
        # The receipt represents canonical repository text. Git may materialize
        # text files with CRLF on Windows, so line-ending conversion must not
        # turn an otherwise identical template checkout into an integrity failure.
        canonical_bytes = path.read_bytes().replace(b"\r\n", b"\n")
        assert hashlib.sha256(canonical_bytes).hexdigest() == digest
