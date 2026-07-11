from __future__ import annotations

from pathlib import Path

import planning_lite.cli as cli


def _isolate_source_discovery(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.delenv(cli.CONFIG_ENV, raising=False)
    monkeypatch.setattr(cli, "CONFIG_PATH", tmp_path / "user-config" / "config.toml")


def test_default_template_source_is_the_official_repository(
    monkeypatch,
    tmp_path: Path,
) -> None:
    _isolate_source_discovery(monkeypatch, tmp_path)
    target = tmp_path / "ordinary-project"
    target.mkdir()
    monkeypatch.chdir(target)

    assert cli._discover_template_source(None) == (
        "https://github.com/yegor-vynokurov/planning-lite"
    )


def test_explicit_source_overrides_every_other_source(monkeypatch, tmp_path: Path) -> None:
    _isolate_source_discovery(monkeypatch, tmp_path)
    monkeypatch.setenv(cli.CONFIG_ENV, "https://example.invalid/from-env")
    cli.CONFIG_PATH.parent.mkdir(parents=True)
    cli.CONFIG_PATH.write_text(
        'template_source = "https://example.invalid/from-config"\n',
        encoding="utf-8",
    )

    assert cli._discover_template_source("D:/local/template") == "D:/local/template"


def test_environment_source_overrides_user_configuration(
    monkeypatch,
    tmp_path: Path,
) -> None:
    _isolate_source_discovery(monkeypatch, tmp_path)
    cli.CONFIG_PATH.parent.mkdir(parents=True)
    cli.CONFIG_PATH.write_text(
        'template_source = "https://example.invalid/from-config"\n',
        encoding="utf-8",
    )
    monkeypatch.setenv(cli.CONFIG_ENV, "https://example.invalid/from-env")

    assert cli._discover_template_source(None) == "https://example.invalid/from-env"


def test_local_central_repository_overrides_user_configuration(
    monkeypatch,
    tmp_path: Path,
) -> None:
    _isolate_source_discovery(monkeypatch, tmp_path)
    cli.CONFIG_PATH.parent.mkdir(parents=True)
    cli.CONFIG_PATH.write_text(
        'template_source = "https://example.invalid/from-config"\n',
        encoding="utf-8",
    )
    (tmp_path / "copier.yml").write_text("_subdirectory: template\n", encoding="utf-8")
    (tmp_path / "template").mkdir()
    nested = tmp_path / "nested"
    nested.mkdir()
    monkeypatch.chdir(nested)

    assert cli._discover_template_source(None) == str(tmp_path.resolve())


def test_configured_source_overrides_the_official_default(
    monkeypatch,
    tmp_path: Path,
) -> None:
    _isolate_source_discovery(monkeypatch, tmp_path)
    cli.CONFIG_PATH.parent.mkdir(parents=True)
    cli.CONFIG_PATH.write_text(
        'template_source = "https://example.invalid/from-config"\n',
        encoding="utf-8",
    )
    target = tmp_path / "ordinary-project"
    target.mkdir()
    monkeypatch.chdir(target)

    assert cli._discover_template_source(None) == "https://example.invalid/from-config"
