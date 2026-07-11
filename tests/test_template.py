from __future__ import annotations

from pathlib import Path


def test_root_agents_is_small_bridge() -> None:
    root = Path(__file__).resolve().parents[1]
    content = (root / "template/AGENTS.md").read_text(encoding="utf-8")
    assert ".planning/control/ROOT_ROUTER.md" in content
    assert len(content.splitlines()) < 25


def test_project_config_does_not_copy_defaults() -> None:
    root = Path(__file__).resolve().parents[1]
    config = (root / "template/.planning/CONFIG.yml").read_text(encoding="utf-8")
    defaults = (root / "template/.planning/framework/defaults.yml").read_text(encoding="utf-8")
    assert config.strip().endswith("{}")
    assert "quick_fix:" in defaults


def test_no_unexpected_template_suffixes() -> None:
    root = Path(__file__).resolve().parents[1] / "template"
    allowed = {
        root / ".copier-answers.planning-lite.yml.jinja",
        root / ".planning/AGENT_PROFILE.yml.jinja",
    }
    found = set(root.rglob("*.jinja"))
    assert found == allowed
