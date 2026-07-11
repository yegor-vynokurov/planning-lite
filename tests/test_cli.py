from __future__ import annotations

from pathlib import Path

import yaml

from planning_lite.cli import BRIDGE_START, _ensure_agents_bridge, build_parser


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
