from __future__ import annotations

from pathlib import Path
import subprocess

import pytest
import yaml

import planning_lite.workspace as workspace
from planning_lite.workspace import (
    WorkspaceError,
    control_git,
    control_init,
    inspect_project,
    product_git,
    register_project,
)


def _git(root: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(root), *args], check=True, capture_output=True, text=True)
    return result.stdout.strip()


def _fixture(tmp_path: Path) -> Path:
    root = tmp_path / "product"
    planning = root / ".planning"
    (planning / "framework").mkdir(parents=True)
    (planning / "control").mkdir()
    (planning / "project").mkdir()
    (planning / "framework" / "OWNERSHIP.yml").write_text(
        "schema_version: 1\nmanaged:\n- .planning/control/**\n- .planning/framework/**\nproject_owned:\n- .planning/project/**\n- .planning/CONFIG.yml\ninstaller_metadata:\n- .copier-answers.planning-lite.yml\n",
        encoding="utf-8",
    )
    (planning / "CONFIG.yml").write_text("{}\n", encoding="utf-8")
    (planning / "project" / "notes.md").write_text("keep\n", encoding="utf-8")
    (root / ".gitignore").write_text(".planning/\n", encoding="utf-8")
    (root / "README.md").write_text("product\n", encoding="utf-8")
    _git(root, "init", "-b", "main")
    _git(root, "config", "user.email", "planning-lite@example.invalid")
    _git(root, "config", "user.name", "Planning Lite")
    _git(root, "add", ".gitignore", "README.md")
    _git(root, "commit", "-m", "fixture")
    return root


def test_split_control_init_is_external_and_idempotent(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    home = tmp_path / "home"
    before = _git(root, "rev-parse", "HEAD")
    result = control_init(root, project_id="demo", home=home)
    assert Path(result["git_dir"]).is_dir()
    gitfile = root / ".planning" / ".git"
    assert gitfile.is_file()
    gitfile_target = gitfile.read_text(encoding="utf-8").split(":", 1)[1].strip()
    assert Path(result["git_dir"]).resolve() == Path(gitfile_target).resolve()
    assert _git(root, "rev-parse", "HEAD") == before
    assert ".planning/" in _git(root, "check-ignore", ".planning/")
    content = (root / ".planning" / ".gitignore").read_text(encoding="utf-8")
    assert "control/**" in content
    assert ".git" not in content
    assert (root / ".planning" / "CONFIG.yml").read_text(encoding="utf-8")
    control_status = control_git(root / ".planning", result["git_dir"], "status", "--porcelain")
    assert control_status.returncode == 0
    repeat = control_init(root, project_id="demo", home=home)
    assert repeat["already_initialized"] is True


def test_control_init_requires_outer_ignore(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    (root / ".gitignore").write_text("", encoding="utf-8")
    with pytest.raises(WorkspaceError, match="must already ignore"):
        control_init(root, project_id="demo", home=tmp_path / "home")


def test_control_init_rejects_external_dir_inside_product(tmp_path: Path) -> None:
    root = _fixture(tmp_path)
    with pytest.raises(WorkspaceError, match="outside"):
        control_init(root, project_id="demo", home=tmp_path / "home", git_dir=root / "bad.git")


def test_inspect_reports_independent_product_and_control_git(tmp_path: Path) -> None:
    root = _fixture(tmp_path / "single")
    home = tmp_path / "home"
    register_project(root, project_id="single", mode="single-repo", status="paused", home=home)
    single = inspect_project(root, home=home)
    assert single["product_git"]["available"] is True
    assert single["product_git"]["clean"] is True
    assert single["control_git"]["configured"] is False

    split_root = _fixture(tmp_path / "split")
    control_init(split_root, project_id="split", home=home)
    register_project(split_root, project_id="split", mode="split-control", status="paused", home=home)
    (split_root / "README.md").write_text("product changed\n", encoding="utf-8")
    (split_root / ".planning/project/notes.md").write_text("control changed\n", encoding="utf-8")
    split = inspect_project(split_root, home=home)
    assert split["product_git"]["clean"] is False
    assert split["control_git"]["configured"] is True
    assert split["control_git"]["available"] is True
    assert split["control_git"]["clean"] is False
    assert split["control_git"]["head"] is None


def test_forbidden_paths_disable_product_and_control_git_status(
    tmp_path: Path, monkeypatch
) -> None:
    root = _fixture(tmp_path)
    home = tmp_path / "home"
    control_init(root, project_id="demo", home=home)
    register_project(root, project_id="demo", mode="split-control", status="paused", home=home)
    config_path = root / ".planning/CONFIG.yml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    config["project_policy"]["forbidden_read_paths"] = [".planning/project/**"]
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")

    product_calls: list[tuple[str, ...]] = []
    control_calls: list[tuple[str, ...]] = []
    original_product_git = workspace.product_git
    original_control_git = workspace.control_git

    def guarded_product_git(project_root, *args: str):  # type: ignore[no-untyped-def]
        product_calls.append(args)
        if args and args[0] == "status":
            raise AssertionError("forbidden policy must prevent product git status")
        return original_product_git(project_root, *args)

    def guarded_control_git(planning_root, git_dir, *args: str):  # type: ignore[no-untyped-def]
        control_calls.append(args)
        if args and args[0] == "status":
            raise AssertionError("forbidden policy must prevent control git status")
        return original_control_git(planning_root, git_dir, *args)

    monkeypatch.setattr(workspace, "product_git", guarded_product_git)
    monkeypatch.setattr(workspace, "control_git", guarded_control_git)
    result = inspect_project(root, home=home)
    assert result["product_git"]["clean"] is None
    assert result["product_git"]["status_reason"] == "forbidden_read_paths_prevent_full_status"
    assert result["control_git"]["clean"] is None
    assert result["control_git"]["status_reason"] == "forbidden_read_paths_prevent_full_status"
    assert not any(args and args[0] == "status" for args in product_calls)
    assert not any(args and args[0] == "status" for args in control_calls)
