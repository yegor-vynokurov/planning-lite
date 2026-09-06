from __future__ import annotations

from pathlib import Path
import json

import yaml
import pytest

from planning_lite import cli
from planning_lite.cli import BRIDGE_START, _ensure_agents_bridge, build_parser, main


def test_bridge_is_appended_once(tmp_path: Path) -> None:
    agents = tmp_path / "AGENTS.md"
    agents.write_text("# Existing\n\nKeep local rules.\n", encoding="utf-8")

    assert _ensure_agents_bridge(tmp_path) == "appended"
    assert _ensure_agents_bridge(tmp_path) == "already-present"

    content = agents.read_text(encoding="utf-8")
    assert content.count(BRIDGE_START) == 1
    assert "Keep local rules." in content


def test_check_command_sets_dry_run() -> None:
    parser = build_parser()
    args = parser.parse_args(["check", "."])
    assert args.dry_run is True


def test_ownership_manifest_has_distinct_classes() -> None:
    root = Path(__file__).resolve().parents[1]
    ownership = yaml.safe_load(
        (root / "template/.planning/framework/OWNERSHIP.yml").read_text(encoding="utf-8")
    )

    assert ".planning/control/**" in ownership["managed"]
    assert ".planning/project/**" in ownership["project_owned"]
    assert ".copier-answers.planning-lite.yml" in ownership["installer_metadata"]


def test_release_command_accepts_short_bump() -> None:
    parser = build_parser()
    args = parser.parse_args(["release", "patch", "--dry-run"])
    assert args.version == "patch"
    assert args.dry_run is True


def test_resume_command_accepts_bounded_inputs() -> None:
    parser = build_parser()
    args = parser.parse_args(
        ["resume", "consumer", "--include", ".planning/ACTIVE.md", "--handoff", "handoff.json", "--json"]
    )
    assert args.command == "resume"
    assert args.include == [".planning/ACTIVE.md"]
    assert args.handoff == "handoff.json"
    assert args.json is True
    assert args.guidance is False


def _resume_snapshot(*, action: str = "RUN_FORMAL_READINESS") -> dict:
    return {
        "schema_version": 1,
        "status": "CURRENT",
        "git_identity": {"head": "abc123", "branch": "main"},
        "bootstrap": {
            "project_id": "fixture",
            "active_change": "CHG-1",
            "lifecycle_stage": "Readiness",
            "stage_status": "In progress",
            "implementation_authorized": False,
            "open_blocker": None,
            "next_permitted_action": action,
            "active_context_path": ".planning/changes/active/CHG-1/context.md",
            "source_revision": "abc123",
        },
        "selected_sources": [
            {"path": ".planning/ACTIVE.md", "sha256": "a" * 64},
        ],
    }


def test_resume_guidance_builds_one_snapshot_and_is_read_only(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    snapshot = _resume_snapshot()
    calls = 0

    def fake_build(*args, **kwargs):
        nonlocal calls
        calls += 1
        return snapshot

    monkeypatch.setattr(cli, "build_resume_context", fake_build)
    before = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    assert main(["resume", str(tmp_path), "--guidance", "--json"]) == 0
    after = sorted(path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*"))
    payload = json.loads(capsys.readouterr().out)
    assert calls == 1
    assert payload["resume"] == snapshot
    assert payload["guidance"]["outcome"] == "MATCHED"
    assert before == after


def test_resume_guidance_returns_structured_nonmatch_exit_three(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        cli, "build_resume_context", lambda *args, **kwargs: _resume_snapshot(action="UNKNOWN")
    )
    assert main(["resume", ".", "--guidance", "--json"]) == 3
    payload = json.loads(capsys.readouterr().out)
    assert payload["guidance"]["outcome"] == "NO_APPLICABLE_OPERATION"


def test_plain_resume_remains_without_guidance_wrapper(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    snapshot = _resume_snapshot()
    monkeypatch.setattr(cli, "build_resume_context", lambda *args, **kwargs: snapshot)
    assert main(["resume", ".", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload == snapshot
