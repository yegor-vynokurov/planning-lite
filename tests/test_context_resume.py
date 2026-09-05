from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from planning_lite.context import ContextError, build_resume_context, classify_storage, validate_handoff
from planning_lite.cli import main


def _project(tmp_path: Path, *, active_change: str | None = "CHG-1", unborn: bool = False) -> Path:
    root = tmp_path / "consumer"
    planning = root / ".planning"
    (planning / "framework").mkdir(parents=True)
    (planning / "project").mkdir()
    (planning / "changes" / "active" / "CHG-1").mkdir(parents=True)
    (planning / "framework" / "defaults.yml").write_text(
        "schema_version: 1\nproject_policy:\n  schema_version: 1\n  project_id: fixture\n  planning_root: .planning\n  agents_root: .agents\n  forbidden_read_paths: []\n  secret_storage: prohibited\n",
        encoding="utf-8",
    )
    change = f"`{active_change}`" if active_change else "`None`"
    context = "`.planning/changes/active/CHG-1/context.md`" if active_change else "`None`"
    (planning / "ACTIVE.md").write_text(
        "# Active state\n\n## Active change\n\n"
        f"- Change: {change}\n- Change status: `Active`\n"
        "- Lifecycle stage: `Implementation`\n- Stage status: `Ready`\n"
        "- Current task: `T-01`\n- Last verified checkpoint: `checkpoint.md`\n"
        "- Next gate: `Central Candidate Review Gate`\n"
        "- Next permitted action: `Run T-01`\n"
        "- Implementation authorized: `No`\n"
        f"- Active context packet: {context}\n\n"
        "## Blocking decision\n\n- `None`\n",
        encoding="utf-8",
    )
    (planning / "project" / "CURRENT_STATE.md").write_text(
        "- Project: `Fixture`\n- Direction: `Bounded`\n\n## Current capability\n\nold history\n",
        encoding="utf-8",
    )
    if active_change:
        (planning / "changes" / "active" / "CHG-1" / "context.md").write_text(
            "# Active context packet\n\n- Approved outcome: `bounded resume`\n"
            "- Next permitted action: `Run T-01`\n",
            encoding="utf-8",
        )
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    if not unborn:
        subprocess.run(["git", "-C", str(root), "add", "."], check=True)
        subprocess.run(
            ["git", "-C", str(root), "-c", "user.name=Fixture", "-c", "user.email=fixture@example.test", "commit", "-qm", "fixture"],
            check=True,
        )
    return root


def test_default_resume_is_bounded_and_deterministic(tmp_path: Path) -> None:
    root = _project(tmp_path)
    first = build_resume_context(root)
    second = build_resume_context(root)
    assert first == second
    assert first["status"] == "CURRENT"
    assert first["bootstrap"]["active_change"] == "CHG-1"
    assert first["context_trace"]["selected_artifact_count"] == 3
    assert first["context_trace"]["explicit_expansion_count"] == 0


def test_no_change_and_unborn_are_valid(tmp_path: Path) -> None:
    root = _project(tmp_path, active_change=None, unborn=True)
    result = build_resume_context(root)
    assert result["status"] == "CURRENT"
    assert result["bootstrap"]["active_change"] is None
    assert result["bootstrap"]["open_blocker"] is None
    assert result["git_identity"]["head"] == "UNBORN"


def test_current_state_preamble_does_not_load_history(tmp_path: Path) -> None:
    root = _project(tmp_path)
    result = build_resume_context(root)
    current = result["current_state"]
    assert current["project"] == "Fixture"
    assert "old history" not in json.dumps(current)


def test_explicit_heading_is_exact_and_bounded(tmp_path: Path) -> None:
    root = _project(tmp_path)
    path = root / ".planning" / "changes" / "active" / "CHG-1" / "plan.md"
    path.write_text("# Plan\n\n## Exact\nselected\n\n## Other\nhidden\n", encoding="utf-8")
    result = build_resume_context(root, include=[".planning/changes/active/CHG-1/plan.md#Exact"])
    selected = result["selected_sources"][-1]
    assert selected["section"] == "Exact"
    with pytest.raises(ContextError):
        build_resume_context(root, include=[".planning/changes/active/CHG-1/plan.md#exact"])


def test_trace_is_fixed_and_history_is_not_scanned(tmp_path: Path) -> None:
    root = _project(tmp_path)
    history = root / ".planning" / "changes" / "completed"
    history.mkdir(parents=True)
    (history / "ancient.md").write_text("do not load", encoding="utf-8")
    result = build_resume_context(root)
    selected_paths = {item["path"] for item in result["context_trace"]["selected"]}
    assert ".planning/changes/completed/ancient.md" not in selected_paths
    assert [item["category"] for item in result["context_trace"]["excluded_by_default"]] == [
        "completed changes",
        "full ledgers",
        "archives",
        "raw logs",
        "historical proposals",
    ]


def test_oversize_expansion_fails_closed(tmp_path: Path) -> None:
    root = _project(tmp_path)
    path = root / ".planning" / "changes" / "active" / "CHG-1" / "large.md"
    path.write_text("# Large\n" + ("x" * 5000), encoding="utf-8")
    result = build_resume_context(root, include=[".planning/changes/active/CHG-1/large.md#Large"])
    assert result["status"] == "CURRENT"
    assert result["expansion_results"] == [
        {
            "status": "EXPANSION_TOO_LARGE",
            "path": ".planning/changes/active/CHG-1/large.md",
            "section": "Large",
            "limit_chars": 4096,
        }
    ]
    assert result["context_trace"]["selected_artifact_count"] == 3
    assert "x" * 5000 not in json.dumps(result["selected_sources"])


def test_bounds_reject_glob_and_too_many_expansions(tmp_path: Path) -> None:
    root = _project(tmp_path)
    with pytest.raises(ContextError):
        build_resume_context(root, include=[".planning/changes/active/CHG-1/*.md"])
    with pytest.raises(ContextError):
        build_resume_context(root, include=[".planning/ACTIVE.md"] * 6)


def test_forbidden_and_inbox_are_not_selectable(tmp_path: Path) -> None:
    root = _project(tmp_path)
    (root / "recommendations" / "inbox").mkdir(parents=True)
    (root / "recommendations" / "inbox" / "raw.md").write_text("raw", encoding="utf-8")
    with pytest.raises(ContextError):
        build_resume_context(root, include=["recommendations/inbox/raw.md"])
    with pytest.raises(ContextError):
        build_resume_context(root, include=[".git/config"])


def test_outside_root_and_parent_escape_are_rejected(tmp_path: Path) -> None:
    root = _project(tmp_path)
    outside = tmp_path / "outside.md"
    outside.write_text("secret", encoding="utf-8")
    with pytest.raises(ContextError):
        build_resume_context(root, include=["../outside.md"])
    with pytest.raises(ContextError):
        build_resume_context(root, include=[str(outside)])


def test_effective_forbidden_read_paths_are_enforced(tmp_path: Path) -> None:
    root = _project(tmp_path)
    defaults = root / ".planning" / "framework" / "defaults.yml"
    defaults.write_text(
        defaults.read_text(encoding="utf-8") + "  forbidden_read_paths:\n  - .planning/changes/active/**\n",
        encoding="utf-8",
    )
    with pytest.raises(ContextError):
        build_resume_context(root)


def test_symlink_component_is_rejected_when_supported(tmp_path: Path) -> None:
    root = _project(tmp_path)
    target = root / "outside.md"
    target.write_text("outside", encoding="utf-8")
    link = root / ".planning" / "project" / "link.md"
    try:
        link.symlink_to(target)
    except (OSError, NotImplementedError):
        pytest.skip("symlink creation is unavailable on this runner")
    with pytest.raises(ContextError):
        build_resume_context(root, include=[".planning/project/link.md"])


def test_handoff_exact_schema_and_current_authority(tmp_path: Path) -> None:
    root = _project(tmp_path)
    current = build_resume_context(root)
    handoff = {
        "schema_version": 1,
        "project_id": "fixture",
        "change_id": "CHG-1",
        "active_context_path": ".planning/changes/active/CHG-1/context.md",
        "changed_paths": [],
        "lifecycle_stage": "Implementation",
        "stage_status": "Ready",
        "implementation_authorized": False,
        "verification": [],
        "open_blocker": None,
        "accepted_dispositions": [],
        "next_permitted_action": "Run T-01",
        "artifact_refs": [],
        "source_revision": {"head": current["git_identity"]["head"], "state": "AVAILABLE"},
    }
    assert validate_handoff(handoff, current=current["bootstrap"])["project_id"] == "fixture"
    with pytest.raises(ContextError):
        validate_handoff({**handoff, "raw_body": "forbidden"})
    with pytest.raises(ContextError):
        validate_handoff({**handoff, "implementation_authorized": True}, current=current["bootstrap"])


def test_freshness_reports_stale_artifact(tmp_path: Path) -> None:
    root = _project(tmp_path)
    source = root / ".planning" / "project" / "CURRENT_STATE.md"
    import hashlib

    old_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    handoff = {
        "schema_version": 1,
        "project_id": "fixture",
        "change_id": "CHG-1",
        "active_context_path": ".planning/changes/active/CHG-1/context.md",
        "changed_paths": [],
        "lifecycle_stage": "Implementation",
        "stage_status": "Ready",
        "implementation_authorized": False,
        "verification": [],
        "open_blocker": None,
        "accepted_dispositions": [],
        "next_permitted_action": "Run T-01",
        "artifact_refs": [{"path": ".planning/project/CURRENT_STATE.md", "sha256": old_hash}],
        "source_revision": {"head": None, "state": "AVAILABLE"},
    }
    source.write_text(source.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
    assert build_resume_context(root, handoff=handoff)["status"] == "STALE"


def test_freshness_reports_superseded_active_tuple_and_missing_owner(tmp_path: Path) -> None:
    root = _project(tmp_path)
    current = build_resume_context(root)
    base = {
        "schema_version": 1,
        "project_id": "fixture",
        "change_id": "CHG-1",
        "active_context_path": ".planning/changes/active/CHG-1/context.md",
        "changed_paths": [],
        "lifecycle_stage": "Implementation",
        "stage_status": "Ready",
        "implementation_authorized": False,
        "verification": [],
        "open_blocker": None,
        "accepted_dispositions": [],
        "next_permitted_action": "Run T-01",
        "artifact_refs": [],
        "source_revision": {"head": current["git_identity"]["head"], "state": "AVAILABLE"},
    }
    assert build_resume_context(root, handoff={**base, "stage_status": "Superseded"})["status"] == "SUPERSEDED"
    missing = {**base, "artifact_refs": [{"path": ".planning/project/missing.md", "sha256": "0" * 64}]}
    assert build_resume_context(root, handoff=missing)["status"] == "MISSING_OWNER_ARTIFACT"


def test_freshness_reports_active_context_pointer_superseded(tmp_path: Path) -> None:
    root = _project(tmp_path)
    current = build_resume_context(root)
    handoff = {
        "schema_version": 1,
        "project_id": "fixture",
        "change_id": "CHG-1",
        "active_context_path": ".planning/changes/active/CHG-1/old-context.md",
        "changed_paths": [],
        "lifecycle_stage": "Implementation",
        "stage_status": "Ready",
        "implementation_authorized": False,
        "verification": [],
        "open_blocker": None,
        "accepted_dispositions": [],
        "next_permitted_action": "Run T-01",
        "artifact_refs": [],
        "source_revision": {"head": current["git_identity"]["head"], "state": "AVAILABLE"},
    }
    assert build_resume_context(root, handoff=handoff)["status"] == "SUPERSEDED"


def test_freshness_reports_null_pointer_mismatch_superseded(tmp_path: Path) -> None:
    root = _project(tmp_path)
    current = build_resume_context(root)
    handoff = {
        "schema_version": 1,
        "project_id": "fixture",
        "change_id": "CHG-1",
        "active_context_path": None,
        "changed_paths": [],
        "lifecycle_stage": "Implementation",
        "stage_status": "Ready",
        "implementation_authorized": False,
        "verification": [],
        "open_blocker": None,
        "accepted_dispositions": [],
        "next_permitted_action": "Run T-01",
        "artifact_refs": [],
        "source_revision": {"head": current["git_identity"]["head"], "state": "AVAILABLE"},
    }
    assert build_resume_context(root, handoff=handoff)["status"] == "SUPERSEDED"


def test_matching_null_context_pointers_remain_current(tmp_path: Path) -> None:
    root = _project(tmp_path, active_change=None, unborn=True)
    current = build_resume_context(root)
    handoff = {
        "schema_version": 1,
        "project_id": "fixture",
        "change_id": None,
        "active_context_path": None,
        "changed_paths": [],
        "lifecycle_stage": "Implementation",
        "stage_status": "Ready",
        "implementation_authorized": False,
        "verification": [],
        "open_blocker": None,
        "accepted_dispositions": [],
        "next_permitted_action": "Run T-01",
        "artifact_refs": [],
        "source_revision": {"head": current["git_identity"]["head"], "state": "UNBORN"},
    }
    assert build_resume_context(root, handoff=handoff)["status"] == "CURRENT"


def test_superseded_precedes_stale(tmp_path: Path) -> None:
    root = _project(tmp_path)
    source = root / ".planning" / "project" / "CURRENT_STATE.md"
    import hashlib

    old_hash = hashlib.sha256(source.read_bytes()).hexdigest()
    current = build_resume_context(root)
    handoff = {
        "schema_version": 1,
        "project_id": "fixture",
        "change_id": "CHG-1",
        "active_context_path": None,
        "changed_paths": [],
        "lifecycle_stage": "Implementation",
        "stage_status": "Ready",
        "implementation_authorized": False,
        "verification": [],
        "open_blocker": None,
        "accepted_dispositions": [],
        "next_permitted_action": "Run T-01",
        "artifact_refs": [{"path": ".planning/project/CURRENT_STATE.md", "sha256": old_hash}],
        "source_revision": {"head": current["git_identity"]["head"], "state": "AVAILABLE"},
    }
    source.write_text(source.read_text(encoding="utf-8") + "\nchanged\n", encoding="utf-8")
    assert build_resume_context(root, handoff=handoff)["status"] == "SUPERSEDED"


def test_classification_is_fixed_and_not_content_based() -> None:
    assert classify_storage("recommendations/inbox/raw.md") == "LOCAL_OPERATIONAL"
    assert classify_storage(".planning/changes/completed/old.md") == "TRACKED_EVIDENCE_HISTORY"
    assert classify_storage(".planning/ACTIVE.md") == "TRACKED_CANONICAL"


def test_cli_resume_json_is_read_only(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _project(tmp_path)
    before = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    assert main(["resume", str(root), "--json"]) == 0
    output = json.loads(capsys.readouterr().out)
    after = sorted(path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file())
    assert output["schema_version"] == 1
    assert before == after
