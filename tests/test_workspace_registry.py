from __future__ import annotations

from pathlib import Path
import subprocess

import pytest
import yaml

import planning_lite.workspace as workspace
from planning_lite.cli import PlanningLiteError, build_parser, command_register
from planning_lite.workspace import (
    WorkspaceError,
    inspect_project,
    load_effective_policy,
    load_registry,
    register_project,
    resolve_home,
    save_registry,
    update_project_policy,
)


def _consumer(root: Path, *, config: dict | None = None) -> Path:
    planning = root / ".planning"
    (planning / "framework").mkdir(parents=True)
    (planning / "recommendations").mkdir()
    (planning / "framework" / "defaults.yml").write_text(
        "schema_version: 1\nmode:\n  default: auto\n", encoding="utf-8"
    )
    (planning / "ACTIVE.md").write_text("# Active\n", encoding="utf-8")
    (planning / "recommendations" / "INDEX.md").write_text("# Index\n", encoding="utf-8")
    (root / ".copier-answers.planning-lite.yml").write_text(
        "_commit: v1.2.3\n", encoding="utf-8"
    )
    (planning / "CONFIG.yml").write_text(
        yaml.safe_dump(config or {}, sort_keys=False), encoding="utf-8"
    )
    return root


def test_home_precedence(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    explicit = tmp_path / "explicit"
    env = tmp_path / "env"
    monkeypatch.setenv("PLANNING_LITE_HOME", str(env))
    assert resolve_home(explicit) == explicit.resolve()
    assert resolve_home() == env.resolve()
    monkeypatch.delenv("PLANNING_LITE_HOME")
    assert resolve_home() == (Path.home() / ".config" / "planning-lite").resolve()


def test_effective_policy_merges_defaults_and_config(tmp_path: Path) -> None:
    root = _consumer(tmp_path, config={"project_policy": {"project_id": "demo", "telemetry": {"enabled": True}}})
    policy = load_effective_policy(root)["project_policy"]
    assert policy["project_id"] == "demo"
    assert policy["telemetry"]["enabled"] is True
    assert policy["planning_root"] == ".planning"
    assert policy["secret_storage"] == "prohibited"


def test_managed_policy_default_is_runtime_authority(tmp_path: Path) -> None:
    root = _consumer(tmp_path)
    (root / ".planning/framework/defaults.yml").write_text(
        "schema_version: 1\n"
        "project_policy:\n"
        "  schema_version: 1\n"
        "  language: managed-fixture-value\n"
        "  telemetry:\n"
        "    enabled: true\n",
        encoding="utf-8",
    )
    policy = load_effective_policy(root)["project_policy"]
    assert policy["language"] == "managed-fixture-value"
    assert policy["telemetry"]["enabled"] is True


def test_managed_policy_null_or_scalar_fails_closed(tmp_path: Path) -> None:
    for value in ("null", "invalid-scalar"):
        root = _consumer(tmp_path / value)
        (root / ".planning/framework/defaults.yml").write_text(
            f"schema_version: 1\nproject_policy: {value}\n", encoding="utf-8"
        )
        with pytest.raises(WorkspaceError, match="defaults.project_policy must be a mapping"):
            load_effective_policy(root)


def test_legacy_policy_fallback_is_used_only_when_key_is_absent(tmp_path: Path) -> None:
    root = _consumer(tmp_path)
    policy = load_effective_policy(root)["project_policy"]
    assert policy["planning_root"] == ".planning"
    assert policy["project_id"] is None


def test_update_project_policy_validates_against_managed_defaults(tmp_path: Path) -> None:
    root = _consumer(tmp_path)
    (root / ".planning/framework/defaults.yml").write_text(
        "schema_version: 1\n"
        "project_policy:\n"
        "  schema_version: 1\n"
        "  planning_root: managed-planning\n"
        "  agents_root: managed-agents\n"
        "  language: managed-fixture-value\n",
        encoding="utf-8",
    )
    updated = update_project_policy(root, project_id="managed-id")
    assert updated["project_id"] == "managed-id"
    effective = load_effective_policy(root)["project_policy"]
    assert effective["planning_root"] == "managed-planning"
    assert effective["language"] == "managed-fixture-value"


def test_policy_rejects_escape_and_overlap(tmp_path: Path) -> None:
    root = _consumer(tmp_path / "escape", config={"project_policy": {"planning_root": "../outside"}})
    with pytest.raises(WorkspaceError, match="escapes"):
        load_effective_policy(root)
    root = _consumer(tmp_path / "overlap", config={"project_policy": {"agents_root": ".planning/agents"}})
    with pytest.raises(WorkspaceError, match="overlap"):
        load_effective_policy(root)


def test_registration_is_idempotent_and_conflicts_fail_closed(tmp_path: Path) -> None:
    root = _consumer(tmp_path)
    home = tmp_path / "home"
    first = register_project(root, mode="local-only", status="paused", home=home, project_id="demo")
    second = register_project(root, mode="local-only", status="paused", home=home, project_id="demo")
    assert first == second
    assert load_registry(home)["projects"][0]["project_id"] == "demo"
    with pytest.raises(WorkspaceError, match="Conflicting"):
        register_project(root, mode="single-repo", status="active", home=home, project_id="demo")


def test_registry_rejects_duplicate_roots(tmp_path: Path) -> None:
    home = tmp_path / "home"
    root = tmp_path / "project"
    home.mkdir(parents=True)
    (home / "projects.yml").write_text(
        yaml.safe_dump(
            {
                "schema_version": 1,
                "projects": [
                    {"project_id": "one", "project_root": str(root), "project_status": "paused", "control_history": {"mode": "local-only", "git_dir": None}},
                    {"project_id": "two", "project_root": str(root), "project_status": "paused", "control_history": {"mode": "local-only", "git_dir": None}},
                ],
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    with pytest.raises(WorkspaceError, match="duplicate project_root"):
        load_registry(home)


def test_legacy_null_mode_is_accepted(tmp_path: Path) -> None:
    root = _consumer(tmp_path, config={"project_policy": {"project_id": None, "control_history_mode": None}})
    policy = load_effective_policy(root)["project_policy"]
    assert policy["project_id"] is None
    assert policy["control_history_mode"] is None


def test_forbidden_inspection_path_fails_closed(tmp_path: Path) -> None:
    root = _consumer(
        tmp_path,
        config={"project_policy": {"forbidden_read_paths": [".planning/ACTIVE.md"]}},
    )
    home = tmp_path / "home"
    register_project(root, mode="local-only", status="paused", home=home, project_id="demo")
    with pytest.raises(WorkspaceError, match="Forbidden read path"):
        inspect_project(root, home=home)


def test_forbidden_paths_disable_product_git_status(tmp_path: Path, monkeypatch) -> None:
    root = _consumer(
        tmp_path,
        config={"project_policy": {"forbidden_read_paths": [".private/**"]}},
    )
    (root / ".private").mkdir()
    (root / ".private/secret.txt").write_text("secret\n", encoding="utf-8")
    (root / ".git").mkdir()
    home = tmp_path / "home"
    register_project(root, mode="single-repo", status="paused", home=home, project_id="demo")
    calls: list[tuple[str, ...]] = []

    def guarded_product_git(project_root, *args: str):  # type: ignore[no-untyped-def]
        calls.append(args)
        if args and args[0] == "status":
            raise AssertionError("forbidden policy must prevent unrestricted git status")
        if args == ("rev-parse", "--git-dir"):
            return subprocess.CompletedProcess(args, 0, ".git\n", "")
        if args == ("rev-parse", "HEAD"):
            return subprocess.CompletedProcess(args, 0, "head\n", "")
        return subprocess.CompletedProcess(args, 0, "", "")

    monkeypatch.setattr(workspace, "product_git", guarded_product_git)
    result = inspect_project(root, home=home)
    assert result["product_git"]["available"] is True
    assert result["product_git"]["head"] == "head"
    assert result["product_git"]["clean"] is None
    assert result["product_git"]["status_reason"] == "forbidden_read_paths_prevent_full_status"
    assert not any(args and args[0] == "status" for args in calls)


def test_inspection_continues_for_unrelated_allowed_paths(tmp_path: Path) -> None:
    root = _consumer(
        tmp_path,
        config={"project_policy": {"forbidden_read_paths": [".planning/private/**"]}},
    )
    home = tmp_path / "home"
    register_project(root, mode="local-only", status="paused", home=home, project_id="demo")
    result = inspect_project(root, home=home)
    assert result["lifecycle_exists"] is True
    assert result["control_git"]["configured"] is False


def test_register_dry_run_and_apply_share_conflict_validation(tmp_path: Path) -> None:
    root = _consumer(tmp_path / "existing")
    home = tmp_path / "home"
    register_project(root, mode="local-only", status="paused", home=home, project_id="demo")
    config_before = (root / ".planning/CONFIG.yml").read_bytes()
    registry_before = (home / "projects.yml").read_bytes()
    for extra in ([], ["--dry-run"]):
        args = build_parser().parse_args(
            [
                "register",
                str(root),
                "--project-id",
                "demo",
                "--mode",
                "single-repo",
                "--status",
                "active",
                "--home",
                str(home),
                *extra,
            ]
        )
        with pytest.raises(PlanningLiteError, match="Conflicting"):
            command_register(args)
        assert (root / ".planning/CONFIG.yml").read_bytes() == config_before
        assert (home / "projects.yml").read_bytes() == registry_before


def test_register_dry_run_and_apply_require_split_topology(tmp_path: Path) -> None:
    root = _consumer(tmp_path / "split")
    home = tmp_path / "home"
    config_before = (root / ".planning/CONFIG.yml").read_bytes()
    for extra in ([], ["--dry-run"]):
        args = build_parser().parse_args(
            [
                "register",
                str(root),
                "--project-id",
                "split",
                "--mode",
                "split-control",
                "--status",
                "paused",
                "--home",
                str(home),
                *extra,
            ]
        )
        with pytest.raises(PlanningLiteError, match="control-init"):
            command_register(args)
        assert (root / ".planning/CONFIG.yml").read_bytes() == config_before
        assert not (home / "projects.yml").exists()
