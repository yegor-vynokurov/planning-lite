from __future__ import annotations

import argparse
import subprocess
import tomllib
from datetime import date
from importlib.metadata import version as distribution_version
from pathlib import Path

import pytest
from packaging.version import Version

import planning_lite
from planning_lite.cli import (
    PlanningLiteError,
    _next_release_version,
    _render_released_changelog,
    _validate_release_lockfile,
    command_release,
)


def test_runtime_version_matches_distribution_metadata() -> None:
    assert planning_lite.__version__ == distribution_version("planning-lite")


def test_pyproject_uses_vcs_as_single_version_source() -> None:
    root = Path(__file__).resolve().parents[1]
    with (root / "pyproject.toml").open("rb") as handle:
        pyproject = tomllib.load(handle)

    project = pyproject["project"]
    assert "version" not in project
    assert "version" in project["dynamic"]
    assert pyproject["tool"]["hatch"]["version"]["source"] == "vcs"
    assert "hatch-vcs>=0.5" in pyproject["build-system"]["requires"]


def test_template_has_no_hardcoded_framework_version() -> None:
    root = Path(__file__).resolve().parents[1]
    assert not (root / "template/.planning/VERSION").exists()

    ownership = (root / "template/.planning/framework/OWNERSHIP.yml").read_text(
        encoding="utf-8"
    )
    assert ".planning/VERSION" not in ownership


def test_next_release_version_supports_bumps_and_explicit_versions() -> None:
    current = Version("3.4.5")
    assert _next_release_version(current, "patch") == Version("3.4.6")
    assert _next_release_version(current, "minor") == Version("3.5.0")
    assert _next_release_version(current, "major") == Version("4.0.0")
    assert _next_release_version(current, "v3.6.0") == Version("3.6.0")


@pytest.mark.parametrize("requested", ["3.4.5", "3.4.4", "3.5.0rc1", "3.5"])
def test_next_release_version_rejects_invalid_release_targets(requested: str) -> None:
    with pytest.raises(PlanningLiteError):
        _next_release_version(Version("3.4.5"), requested)


def test_changelog_finalization_preserves_unreleased_heading() -> None:
    original = """# Changelog

## Unreleased

- Add release automation.

## 3.0.0

- Initial release.
"""
    rendered = _render_released_changelog(
        original,
        Version("3.0.1"),
        released_on=date(2026, 7, 11),
    )

    assert rendered.startswith("# Changelog\n\n## Unreleased\n\n## 3.0.1 - 2026-07-11")
    assert "- Add release automation." in rendered
    assert "## 3.0.0" in rendered


def test_release_lock_check_requires_lockfile(tmp_path: Path) -> None:
    with pytest.raises(PlanningLiteError):
        _validate_release_lockfile(tmp_path)


def test_release_lock_check_rejects_environment_specific_index(tmp_path: Path) -> None:
    (tmp_path / "uv.lock").write_text(
        "https://packages.applied-caas-gateway1.internal.api.openai.org/simple",
        encoding="utf-8",
    )
    with pytest.raises(PlanningLiteError):
        _validate_release_lockfile(tmp_path)


def test_release_dry_run_uses_latest_tag_without_mutating_repo(tmp_path: Path) -> None:
    (tmp_path / "template").mkdir()
    (tmp_path / "copier.yml").write_text("_subdirectory: template\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## Unreleased\n\n- Prepared release.\n\n## 3.0.0\n\n- Initial.\n",
        encoding="utf-8",
    )
    (tmp_path / "uv.lock").write_text("version = 1\n", encoding="utf-8")

    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Planning Lite Tests"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "tag", "v3.0.0"], cwd=tmp_path, check=True)

    args = argparse.Namespace(
        target=str(tmp_path),
        branch="main",
        allow_other_branch=False,
        version="patch",
        dry_run=True,
        skip_tests=False,
        message=None,
    )
    before = (tmp_path / "CHANGELOG.md").read_text(encoding="utf-8")
    assert command_release(args) == 0
    assert (tmp_path / "CHANGELOG.md").read_text(encoding="utf-8") == before
    tags = subprocess.run(
        ["git", "tag", "--list"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert tags == ["v3.0.0"]


def test_release_creates_release_commit_and_annotated_tag_when_checks_are_skipped(
    tmp_path: Path,
) -> None:
    (tmp_path / "template").mkdir()
    (tmp_path / "copier.yml").write_text("_subdirectory: template\n", encoding="utf-8")
    (tmp_path / "CHANGELOG.md").write_text(
        "# Changelog\n\n## Unreleased\n\n- Prepared release.\n\n## 3.0.0\n\n- Initial.\n",
        encoding="utf-8",
    )
    (tmp_path / "uv.lock").write_text("version = 1\n", encoding="utf-8")

    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Planning Lite Tests"],
        cwd=tmp_path,
        check=True,
    )
    subprocess.run(["git", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(["git", "commit", "-m", "Initial"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(["git", "tag", "v3.0.0"], cwd=tmp_path, check=True)

    args = argparse.Namespace(
        target=str(tmp_path),
        branch="main",
        allow_other_branch=False,
        version="patch",
        dry_run=False,
        skip_tests=True,
        message=None,
    )
    assert command_release(args) == 0

    changelog = (tmp_path / "CHANGELOG.md").read_text(encoding="utf-8")
    assert "## 3.0.1 - " in changelog
    assert "- Prepared release." in changelog
    tags = subprocess.run(
        ["git", "tag", "--list"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    assert tags == ["v3.0.0", "v3.0.1"]
    tag_type = subprocess.run(
        ["git", "cat-file", "-t", "v3.0.1"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    assert tag_type == "tag"
