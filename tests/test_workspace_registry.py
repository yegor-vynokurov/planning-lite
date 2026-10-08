from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess

import pytest
import yaml

import planning_lite.workspace as workspace
from planning_lite.cli import PlanningLiteError, _registration_preview, build_parser, command_register
from planning_lite.workspace import (
    CanonicalArtifactOutputRouteKeyV1,
    DependencyArtifactOutputRouteV1,
    WorkspaceError,
    inspect_project,
    load_effective_policy,
    load_registry,
    plan_registration,
    register_project,
    resolve_home,
    registry_path,
    save_registry,
    local_operational_root,
    local_route,
    resolve_dependency_artifact_output_route,
    publish_governed_artifact_output,
    update_project_policy,
)


def _governed_route_root(tmp_path: Path, planning_root: str = ".planning") -> Path:
    # Reuse the existing complete governance fixture so route tests exercise
    # the canonical dependency resolver rather than a test-only route source.
    from test_dependency_admission import _write_fixture

    root = tmp_path / "route-consumer"
    _write_fixture(root, planning_root=planning_root)
    if planning_root != ".planning":
        config = root / ".planning" / "CONFIG.yml"
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(f"project_policy:\n  planning_root: {planning_root}\n", encoding="utf-8", newline="\n")
    return root


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
    assert resolve_home() == local_operational_root()
    assert resolve_home() != (Path.home() / ".config" / "planning-lite").resolve()


def test_central_local_routes_are_deterministic_and_fail_closed(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    assert registry_path() == local_operational_root() / "registry" / "projects.yml"
    assert local_route("roadmap_inbox") == local_operational_root() / "inbox" / "roadmaps"
    assert local_route("recommendation_inbox") == local_operational_root() / "inbox" / "recommendations"
    assert local_route("compiled_prompts") == local_operational_root() / "work" / "compiled-prompts"
    assert local_route("experiments") == local_operational_root() / "work" / "experiments"
    assert local_route("cache") == local_operational_root() / "cache"
    with pytest.raises(WorkspaceError, match="ARTIFACT_ROUTING_UNRESOLVED"):
        local_route("invented-route")
    monkeypatch.setenv("PLANNING_LITE_CENTRAL_ROOT", str(tmp_path / "missing-central"))
    with pytest.raises(WorkspaceError, match="ARTIFACT_ROUTING_UNRESOLVED"):
        resolve_home()


def test_central_local_state_does_not_relocate_consumer_planning(tmp_path: Path) -> None:
    root = _consumer(tmp_path / "consumer")
    plan = plan_registration(root, mode="local-only", status="paused", home=tmp_path / "home")
    assert plan["config_path"] == root / ".planning" / "CONFIG.yml"
    assert Path(plan["registry_path"]).is_relative_to(tmp_path / "home" / "registry")
    assert (root / ".planning").is_dir()


def test_registration_preview_reports_operational_root_for_explicit_home(tmp_path: Path) -> None:
    root = _consumer(tmp_path / "consumer")
    home = tmp_path / "home"
    args = build_parser().parse_args(
        [
            "register",
            str(root),
            "--mode",
            "local-only",
            "--status",
            "paused",
            "--home",
            str(home),
            "--dry-run",
        ]
    )
    preview = _registration_preview(args)
    resolved_home = home.resolve()
    assert preview["home"] == str(resolved_home)
    assert preview["registry_path"] == str(resolved_home / "registry" / "projects.yml")


def test_registration_preview_reports_default_central_local_root(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _consumer(tmp_path / "consumer")
    monkeypatch.delenv("PLANNING_LITE_HOME", raising=False)
    args = build_parser().parse_args(
        [
            "register",
            str(root),
            "--mode",
            "local-only",
            "--status",
            "paused",
            "--dry-run",
        ]
    )
    preview = _registration_preview(args)
    expected_home = local_operational_root()
    assert preview["home"] == str(expected_home)
    assert preview["registry_path"] == str(expected_home / "registry" / "projects.yml")


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
    (home / "registry" / "projects.yml").parent.mkdir(parents=True)
    (home / "registry" / "projects.yml").write_text(
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
    registry_before = (home / "registry" / "projects.yml").read_bytes()
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
        assert (home / "registry" / "projects.yml").read_bytes() == registry_before


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
        assert not (home / "registry" / "projects.yml").exists()


@pytest.mark.parametrize("planning_root", [".planning", "managed-planning", "managed[1]-planning"])
def test_dependency_artifact_route_has_exact_key_digest_and_effective_root(
    tmp_path: Path, planning_root: str
) -> None:
    root = _governed_route_root(tmp_path, planning_root)
    route = resolve_dependency_artifact_output_route(root)

    assert isinstance(route, DependencyArtifactOutputRouteV1)
    assert isinstance(route.key, CanonicalArtifactOutputRouteKeyV1)
    mapping = route.key.to_mapping()
    assert set(mapping) == {
        "schema_version", "change_id", "source_task_or_operation_id", "source_attempt_id",
        "requirement_id", "dependency_semantic_digest", "accepted_output_contract_ref",
        "artifact_logical_ref",
    }
    assert mapping["schema_version"] == 1 and type(mapping["schema_version"]) is int
    assert mapping["source_task_or_operation_id"] == "T-01"
    assert mapping["source_attempt_id"] == f'{mapping["change_id"]}/T-01/A1'
    assert mapping["artifact_logical_ref"] == "artifact:build"
    assert route.artifact_route_digest == hashlib.sha256(
        json.dumps(mapping, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False).encode("utf-8")
    ).hexdigest()
    assert route.effective_planning_root == root / planning_root
    assert route.path == (
        root / planning_root / "changes" / "active" / ".planning-lite"
        / "artifact-output-v1" / f"{route.artifact_route_digest}.bin"
    )
    assert route.path.is_relative_to(route.effective_planning_root)
    assert route.path.is_relative_to(root)
    assert not route.path.exists()  # derivation is valid before T-07 publication
    with pytest.raises(WorkspaceError, match="integer 1"):
        CanonicalArtifactOutputRouteKeyV1(
            mapping["change_id"], mapping["source_attempt_id"], mapping["requirement_id"],
            mapping["dependency_semantic_digest"], mapping["accepted_output_contract_ref"],
            mapping["artifact_logical_ref"], schema_version=True,
        )


def test_dependency_artifact_route_rejects_caller_selected_authority(tmp_path: Path) -> None:
    root = _governed_route_root(tmp_path)
    with pytest.raises(TypeError):
        resolve_dependency_artifact_output_route(root, path=tmp_path / "substitute")  # type: ignore[call-arg]
    with pytest.raises(TypeError):
        resolve_dependency_artifact_output_route(root, requirement={})  # type: ignore[call-arg]


def test_dependency_artifact_route_never_falls_back_from_custom_root(tmp_path: Path) -> None:
    from test_dependency_admission import _write_fixture

    root = _governed_route_root(tmp_path, "managed-planning")
    _write_fixture(root, planning_root=".planning", change_id="CHG-DEFAULT-DECOY-002")
    (root / "managed-planning" / "ACTIVE.md").unlink()
    with pytest.raises(WorkspaceError, match="current dependent requirement"):
        resolve_dependency_artifact_output_route(root)


def test_dependency_artifact_route_fails_closed_for_symlink_and_nonregular_terminal(
    tmp_path: Path,
) -> None:
    root = _governed_route_root(tmp_path)
    route = resolve_dependency_artifact_output_route(root)
    route.path.parent.parent.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside-artifacts"
    outside.mkdir()
    try:
        route.path.parent.symlink_to(outside, target_is_directory=True)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"directory symlinks are unavailable: {exc}")
    with pytest.raises(WorkspaceError, match="symlink"):
        resolve_dependency_artifact_output_route(root)

    route.path.parent.unlink()
    route.path.parent.mkdir()
    route.path.mkdir()
    with pytest.raises(WorkspaceError, match="terminal object"):
        resolve_dependency_artifact_output_route(root)


def test_governed_artifact_publisher_is_contained_immutable_and_byte_verified(
    tmp_path: Path,
) -> None:
    root = _governed_route_root(tmp_path)
    route = resolve_dependency_artifact_output_route(root)
    payload = b"exact producer bytes\x00\xff"
    expected_digest = hashlib.sha256(payload).hexdigest()

    assert publish_governed_artifact_output(root, payload) == expected_digest
    assert route.path.read_bytes() == payload
    assert publish_governed_artifact_output(root, payload) == expected_digest
    assert route.path.read_bytes() == payload
    with pytest.raises(WorkspaceError, match="conflicting immutable bytes"):
        publish_governed_artifact_output(root, b"different producer bytes")
    assert route.path.read_bytes() == payload


def test_governed_artifact_publisher_rejects_unsafe_parent_and_final_target(
    tmp_path: Path,
) -> None:
    blocked = _governed_route_root(tmp_path / "blocked")
    blocked_route = resolve_dependency_artifact_output_route(blocked)
    blocked_route.path.parent.parent.mkdir(parents=True, exist_ok=True)
    blocked_route.path.parent.write_bytes(b"not a directory")
    with pytest.raises(WorkspaceError):
        publish_governed_artifact_output(blocked, b"payload")

    nonregular = _governed_route_root(tmp_path / "nonregular")
    nonregular_route = resolve_dependency_artifact_output_route(nonregular)
    nonregular_route.path.parent.mkdir(parents=True, exist_ok=True)
    nonregular_route.path.mkdir()
    with pytest.raises(WorkspaceError, match="terminal object"):
        publish_governed_artifact_output(nonregular, b"payload")


def test_governed_artifact_publisher_rejects_symlink_final_target(tmp_path: Path) -> None:
    root = _governed_route_root(tmp_path / "symlink-final")
    route = resolve_dependency_artifact_output_route(root)
    route.path.parent.mkdir(parents=True, exist_ok=True)
    outside = tmp_path / "outside-payload.bin"
    outside.write_bytes(b"outside bytes stay unchanged")
    try:
        route.path.symlink_to(outside)
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"file symlinks are unavailable: {exc}")

    with pytest.raises(WorkspaceError):
        publish_governed_artifact_output(root, b"governed payload")
    assert outside.read_bytes() == b"outside bytes stay unchanged"
