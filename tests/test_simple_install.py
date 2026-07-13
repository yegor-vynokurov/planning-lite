from __future__ import annotations

from pathlib import Path

import pytest

import planning_lite.cli as cli


def test_install_parser_uses_current_directory_and_codex() -> None:
    args = cli.build_parser().parse_args(["install"])

    assert args.target == "."
    assert args.agent == "codex"
    assert args.func is cli.command_install


def test_simple_install_does_not_require_git(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    commands: list[list[str]] = []

    def fake_run(command: list[str], *, cwd: Path | None = None) -> int:
        commands.append(command)
        return 0

    monkeypatch.setattr(cli, "_run", fake_run)
    monkeypatch.setattr(
        cli,
        "_discover_template_source",
        lambda explicit: "https://example.invalid/planning-lite",
    )

    args = cli.build_parser().parse_args(["install", str(tmp_path)])

    assert cli.command_install(args) == 0
    assert (tmp_path / "AGENTS.md").exists()
    assert cli.BRIDGE_START in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert len(commands) == 1
    command = commands[0]
    assert command[:4] == [cli.sys.executable, "-m", "copier", "copy"]
    assert "--quiet" in command
    assert "--defaults" in command
    assert "project_name=" + tmp_path.name in command
    assert "agent_adapter=codex" in command
    assert command[-2:] == ["https://example.invalid/planning-lite", str(tmp_path.resolve())]


def test_simple_install_refuses_a_second_install(tmp_path: Path) -> None:
    (tmp_path / cli.ANSWERS_FILE).write_text("_src_path: example\n", encoding="utf-8")
    args = cli.build_parser().parse_args(["install", str(tmp_path)])

    with pytest.raises(cli.PlanningLiteError, match="already appears to be installed"):
        cli.command_install(args)
