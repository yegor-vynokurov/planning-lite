from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import subprocess

import pytest
import yaml

import planning_lite.cli as cli
from planning_lite.local_update import (
    ANSWERS_FILE,
    LocalUpdateError,
    apply_local_update_plan,
    build_local_update_plan,
    classify_path,
    iter_files,
    load_ownership_policy,
)


ROOT = Path(__file__).resolve().parents[1]
V42_COMMIT = "bd8c422"


def _run(*args: str, cwd: Path) -> str:
    completed = subprocess.run(args, cwd=cwd, check=True, capture_output=True, text=True)
    return completed.stdout.strip()


def _init_local_only_repo(target: Path) -> None:
    target.mkdir(parents=True, exist_ok=True)
    _run("git", "init", cwd=target)
    _run("git", "config", "user.email", "planning-lite@example.invalid", cwd=target)
    _run("git", "config", "user.name", "Planning Lite Test", cwd=target)
    (target / ".gitignore").write_text(".planning\n.agents\n", encoding="utf-8")
    (target / ANSWERS_FILE).write_text(
        "_commit: v4.2.0\n"
        "_src_path: https://example.invalid/planning-lite\n"
        "agent_adapter: codex\n"
        "project_name: fixture\n",
        encoding="utf-8",
    )
    (target / "README.md").write_text("# target\n", encoding="utf-8")
    if not (target / "AGENTS.md").exists():
        (target / "AGENTS.md").write_text("LOCAL AGENTS\n", encoding="utf-8")
    _run("git", "add", ".gitignore", ANSWERS_FILE, "README.md", "AGENTS.md", cwd=target)
    _run("git", "commit", "-m", "fixture", cwd=target)


def _write_policy(root: Path) -> None:
    path = root / ".planning/framework/OWNERSHIP.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "schema_version: 1\n"
        "managed:\n"
        "- .agents/skills/**\n"
        "- .planning/control/**\n"
        "- .planning/framework/**\n"
        "project_owned:\n"
        "- AGENTS.md\n"
        "- .planning/project/**\n"
        "installer_metadata:\n"
        "- .copier-answers.planning-lite.yml\n",
        encoding="utf-8",
    )


def _write_minimal_target(target: Path) -> None:
    _write_policy(target)
    (target / ".planning/control").mkdir(parents=True, exist_ok=True)
    (target / ".planning/control/KEEP.md").write_text("old managed\n", encoding="utf-8")
    (target / ".planning/control/REMOVE.md").write_text("removed upstream\n", encoding="utf-8")
    (target / ".planning/project").mkdir(parents=True, exist_ok=True)
    (target / ".planning/project/CURRENT_STATE.md").write_text("USER STATE\n", encoding="utf-8")
    (target / ".agents/skills/demo").mkdir(parents=True, exist_ok=True)
    (target / ".agents/skills/demo/SKILL.md").write_text("old skill\n", encoding="utf-8")
    (target / "AGENTS.md").write_text("LOCAL AGENTS\n", encoding="utf-8")


def _write_minimal_candidate(candidate: Path) -> None:
    _write_policy(candidate)
    (candidate / ".planning/control").mkdir(parents=True, exist_ok=True)
    (candidate / ".planning/control/KEEP.md").write_text("new managed\n", encoding="utf-8")
    (candidate / ".planning/control/NEW.md").write_text("new file\n", encoding="utf-8")
    (candidate / ".planning/project").mkdir(parents=True, exist_ok=True)
    (candidate / ".planning/project/CURRENT_STATE.md").write_text("PRISTINE STATE\n", encoding="utf-8")
    (candidate / ".planning/project/TARGET_STATE.md").write_text("NEW PROJECT DEFAULT\n", encoding="utf-8")
    (candidate / ".agents/skills/demo").mkdir(parents=True, exist_ok=True)
    (candidate / ".agents/skills/demo/SKILL.md").write_text("new skill\n", encoding="utf-8")
    (candidate / "AGENTS.md").write_text("PRISTINE AGENTS\n", encoding="utf-8")
    (candidate / ANSWERS_FILE).write_text(
        "_commit: candidate\n_src_path: local\nagent_adapter: codex\nproject_name: fixture\n",
        encoding="utf-8",
    )


class _CandidateHandle:
    def __init__(self, path: Path) -> None:
        self.name = str(path)

    def cleanup(self) -> None:
        return None


def _render_git_template(commit: str, destination: Path, *, installed_ref: str) -> None:
    files = _run("git", "ls-tree", "-r", "--name-only", commit, "template", cwd=ROOT).splitlines()
    for listed in files:
        relative = listed.removeprefix("template/")
        if relative == ".copier-answers.planning-lite.yml.jinja":
            output = destination / ANSWERS_FILE
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                "# Changes here will be overwritten by Copier; NEVER EDIT MANUALLY\n"
                f"_commit: {installed_ref}\n"
                "_src_path: https://github.com/yegor-vynokurov/planning-lite\n"
                "agent_adapter: codex\n"
                "project_name: poker-fixture\n",
                encoding="utf-8",
            )
            continue
        if relative == ".planning/AGENT_PROFILE.yml.jinja":
            output = destination / ".planning/AGENT_PROFILE.yml"
            data = subprocess.check_output(
                ["git", "show", f"{commit}:{listed}"], cwd=ROOT
            ).decode("utf-8").replace("{{ agent }}", "codex")
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(data, encoding="utf-8")
            continue
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(subprocess.check_output(["git", "show", f"{commit}:{listed}"], cwd=ROOT))


def _render_working_template(destination: Path, *, installed_ref: str) -> None:
    for source in (ROOT / "template").rglob("*"):
        if not source.is_file():
            continue
        relative = source.relative_to(ROOT / "template").as_posix()
        if relative == ".copier-answers.planning-lite.yml.jinja":
            output = destination / ANSWERS_FILE
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(
                "# Changes here will be overwritten by Copier; NEVER EDIT MANUALLY\n"
                f"_commit: {installed_ref}\n"
                "_src_path: https://github.com/yegor-vynokurov/planning-lite\n"
                "agent_adapter: codex\n"
                "project_name: poker-fixture\n",
                encoding="utf-8",
            )
            continue
        if relative == ".planning/AGENT_PROFILE.yml.jinja":
            output = destination / ".planning/AGENT_PROFILE.yml"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(source.read_text(encoding="utf-8").replace("{{ agent }}", "codex"), encoding="utf-8")
            continue
        output = destination / relative
        output.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, output)


def test_current_template_is_fully_classified_for_local_only_update() -> None:
    policy = load_ownership_policy(ROOT / "template")
    unknown = [
        relative
        for relative in iter_files(ROOT / "template")
        if not relative.endswith(".jinja") and classify_path(relative, policy) == "unknown"
    ]
    # Rendered Jinja destinations are also part of the ownership contract.
    assert classify_path(ANSWERS_FILE, policy) == "installer_metadata"
    assert classify_path(".planning/AGENT_PROFILE.yml", policy) == "project_owned"
    assert unknown == []
    assert classify_path(".planning/drift/reviews/TEMPLATE.md", policy) == "managed"


def test_local_only_plan_preserves_project_owned_and_removes_only_old_managed(tmp_path: Path) -> None:
    target = tmp_path / "target"
    candidate = tmp_path / "candidate"
    target.mkdir()
    candidate.mkdir()
    (target / ANSWERS_FILE).write_text("_commit: old\n", encoding="utf-8")
    _write_minimal_target(target)
    _write_minimal_candidate(candidate)

    before_state = (target / ".planning/project/CURRENT_STATE.md").read_bytes()
    before_agents = (target / "AGENTS.md").read_bytes()
    plan = build_local_update_plan(target, candidate)

    actions = {(item.action, item.path) for item in plan.mutations}
    assert ("UPDATE_MANAGED", ".planning/control/KEEP.md") in actions
    assert ("REMOVE_MANAGED", ".planning/control/REMOVE.md") in actions
    assert ("ADD_MANAGED", ".planning/control/NEW.md") in actions
    assert ("KEEP_PROJECT", ".planning/project/CURRENT_STATE.md") in actions
    assert ("ADD_PROJECT", ".planning/project/TARGET_STATE.md") in actions
    assert ("UPDATE_METADATA", ANSWERS_FILE) in actions

    apply_local_update_plan(target, candidate, plan)

    assert (target / ".planning/project/CURRENT_STATE.md").read_bytes() == before_state
    assert (target / "AGENTS.md").read_bytes() == before_agents
    assert not (target / ".planning/control/REMOVE.md").exists()
    assert (target / ".planning/control/KEEP.md").read_text(encoding="utf-8") == "new managed\n"
    assert (target / ".planning/control/NEW.md").exists()
    assert (target / ".planning/project/TARGET_STATE.md").exists()


def test_ordinary_update_fails_closed_for_ignored_managed_tree(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "repo"
    _init_local_only_repo(target)
    _write_minimal_target(target)

    called = False

    def _unexpected_run(*args, **kwargs):  # type: ignore[no-untyped-def]
        nonlocal called
        called = True
        return 0

    monkeypatch.setattr(cli, "_run", _unexpected_run)
    args = cli.build_parser().parse_args(["update", str(target), "--vcs-ref", "candidate"])
    with pytest.raises(cli.PlanningLiteError, match="Ordinary Copier update is blocked"):
        cli.command_update(args)
    assert called is False


def test_check_auto_previews_local_only_without_writing(tmp_path: Path, monkeypatch, capsys) -> None:
    target = tmp_path / "repo"
    candidate = tmp_path / "candidate"
    _init_local_only_repo(target)
    _write_minimal_target(target)
    candidate.mkdir()
    _write_minimal_candidate(candidate)
    before = (target / ".planning/control/KEEP.md").read_bytes()

    monkeypatch.setattr(
        cli,
        "_render_local_update_candidate",
        lambda **kwargs: _CandidateHandle(candidate),
    )
    args = cli.build_parser().parse_args(["check", str(target), "--vcs-ref", "candidate"])
    assert cli.command_update(args) == 0
    output = capsys.readouterr().out
    assert "Detected local-only Planning Lite managed roots" in output
    assert "UPDATE_MANAGED" in output
    assert "REMOVE_MANAGED" in output
    assert "KEEP_PROJECT" in output
    assert "Dry run: no files were written." in output
    assert (target / ".planning/control/KEEP.md").read_bytes() == before


def test_local_only_update_applies_candidate_and_is_idempotent(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "repo"
    candidate = tmp_path / "candidate"
    _init_local_only_repo(target)
    _write_minimal_target(target)
    candidate.mkdir()
    _write_minimal_candidate(candidate)
    before_state = (target / ".planning/project/CURRENT_STATE.md").read_bytes()

    monkeypatch.setattr(
        cli,
        "_render_local_update_candidate",
        lambda **kwargs: _CandidateHandle(candidate),
    )
    args = cli.build_parser().parse_args(
        ["update", str(target), "--vcs-ref", "candidate", "--local-only"]
    )
    assert cli.command_update(args) == 0
    assert (target / ".planning/project/CURRENT_STATE.md").read_bytes() == before_state
    assert (target / ".planning/control/NEW.md").exists()

    second = build_local_update_plan(target, candidate)
    assert second.changed() == ()


def test_v42_local_only_fixture_updates_to_current_without_destructive_removals(tmp_path: Path) -> None:
    target = tmp_path / "v42-consumer"
    candidate = tmp_path / "current-candidate"
    target.mkdir()
    candidate.mkdir()
    _render_git_template(V42_COMMIT, target, installed_ref="v4.2.0")
    _render_working_template(candidate, installed_ref="current-test")

    # Simulate real consumer-owned state rather than pristine defaults.
    project_sentinels = {
        ".planning/project/CURRENT_STATE.md": b"POKER CURRENT STATE\n",
        ".planning/project/ROADMAP.md": b"POKER ROADMAP\n",
        ".planning/recommendations/INDEX.md": b"POKER RECOMMENDATION INDEX\n",
        ".planning/ACTIVE.md": b"POKER ACTIVE\n",
    }
    for relative, content in project_sentinels.items():
        path = target / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)

    before_hashes = {
        relative: hashlib.sha256((target / relative).read_bytes()).hexdigest()
        for relative in project_sentinels
    }
    plan = build_local_update_plan(target, candidate)

    # No managed file was intentionally deleted between v4.2.0 and this candidate.
    assert [item.path for item in plan.mutations if item.action == "REMOVE_MANAGED"] == []
    apply_local_update_plan(target, candidate, plan)

    for relative, digest in before_hashes.items():
        assert hashlib.sha256((target / relative).read_bytes()).hexdigest() == digest

    # Representative v4.2 managed files must survive, while new Direction files appear.
    assert (target / ".planning/control/CHANGE_PLANNING.md").is_file()
    assert (target / ".planning/framework/defaults.yml").is_file()
    assert (target / ".agents/skills/planning-plan/SKILL.md").is_file()
    assert (target / ".planning/control/DIRECTION_INVENTORY.md").is_file()
    assert (target / ".planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md").is_file()
    assert yaml.safe_load((target / ANSWERS_FILE).read_text(encoding="utf-8"))["_commit"] == "current-test"

    second = build_local_update_plan(target, candidate)
    assert second.changed() == ()


def test_candidate_unknown_path_fails_closed(tmp_path: Path) -> None:
    target = tmp_path / "target"
    candidate = tmp_path / "candidate"
    target.mkdir()
    candidate.mkdir()
    (target / ANSWERS_FILE).write_text("_commit: old\n", encoding="utf-8")
    _write_minimal_target(target)
    _write_minimal_candidate(candidate)
    (candidate / ".planning/unclassified.txt").write_text("unknown\n", encoding="utf-8")

    with pytest.raises(LocalUpdateError, match="unclassified"):
        build_local_update_plan(target, candidate)


def test_local_update_never_scans_nested_git_metadata(tmp_path: Path) -> None:
    target = tmp_path / "target"
    candidate = tmp_path / "candidate"
    target.mkdir()
    candidate.mkdir()
    (target / ANSWERS_FILE).write_text("_commit: old\n", encoding="utf-8")
    _write_minimal_target(target)
    _write_minimal_candidate(candidate)
    (target / ".planning/.git").mkdir(parents=True)
    (target / ".planning/.git/objects").mkdir()
    (target / ".planning/.git/objects/secret").write_text("metadata\n", encoding="utf-8")
    (candidate / ".planning/.git").mkdir(parents=True)
    (candidate / ".planning/.git/config").write_text("metadata\n", encoding="utf-8")

    plan = build_local_update_plan(target, candidate)
    assert all(".git/" not in item.path for item in plan.mutations)


def test_local_update_prunes_nested_git_before_scandir(tmp_path: Path, monkeypatch) -> None:
    root = tmp_path / "root"
    (root / ".planning/.git/objects").mkdir(parents=True)
    (root / ".planning/.git/objects/secret").write_text("must not be read\n", encoding="utf-8")
    (root / ".planning/allowed.txt").write_text("allowed\n", encoding="utf-8")
    original_scandir = os.scandir

    def guarded_scandir(path):  # type: ignore[no-untyped-def]
        if Path(path).name == ".git":
            raise AssertionError("iter_files descended into nested .git")
        return original_scandir(path)

    monkeypatch.setattr(os, "scandir", guarded_scandir)
    files = iter_files(root)
    assert ".planning/allowed.txt" in files
    assert all(".git" not in path for path in files)


@pytest.mark.skipif(os.name != "nt", reason="Windows junction discriminator")
def test_local_update_prunes_windows_junction_and_rejects_escape(tmp_path: Path) -> None:
    isjunction = getattr(os.path, "isjunction", None)
    if not callable(isjunction):
        pytest.skip("runtime cannot detect Windows junctions")

    root = tmp_path / "root"
    root.mkdir()
    (root / "normal").mkdir()
    (root / "normal/allowed.txt").write_text("allowed\n", encoding="utf-8")
    junction_target = root / "junction-target"
    junction_target.mkdir()
    (junction_target / "secret.txt").write_text("must not be read\n", encoding="utf-8")
    junction = root / "junction"
    created = subprocess.run(
        ["cmd.exe", "/c", "mklink", "/J", str(junction), str(junction_target)],
        check=False,
        capture_output=True,
        text=True,
    )
    if created.returncode != 0 or not isjunction(junction):
        if isjunction(junction):
            subprocess.run(
                ["cmd.exe", "/c", "rmdir", str(junction)],
                check=False,
                capture_output=True,
                text=True,
            )
        pytest.skip("host cannot create/detect a Windows junction")

    escaping = root / "escaping"
    try:
        files = iter_files(root)
        assert "normal/allowed.txt" in files
        assert not any(path.startswith("junction/") for path in files)

        outside = tmp_path / "outside"
        outside.mkdir()
        (outside / "secret.txt").write_text("outside\n", encoding="utf-8")
        escaped = subprocess.run(
            ["cmd.exe", "/c", "mklink", "/J", str(escaping), str(outside)],
            check=False,
            capture_output=True,
            text=True,
        )
        if escaped.returncode != 0 or not isjunction(escaping):
            pytest.skip("host cannot create a second Windows junction")
        with pytest.raises(LocalUpdateError, match="escapes update root"):
            iter_files(root)
    finally:
        for link in (escaping, junction):
            if isjunction(link):
                subprocess.run(
                    ["cmd.exe", "/c", "rmdir", str(link)],
                    check=False,
                    capture_output=True,
                    text=True,
                )


def test_local_update_forbidden_scan_fails_closed(tmp_path: Path) -> None:
    target = tmp_path / "target"
    candidate = tmp_path / "candidate"
    target.mkdir()
    candidate.mkdir()
    (target / ANSWERS_FILE).write_text("_commit: old\n", encoding="utf-8")
    _write_minimal_target(target)
    _write_minimal_candidate(candidate)
    (target / ".planning/private").mkdir(parents=True)
    (target / ".planning/private/secret.txt").write_text("secret\n", encoding="utf-8")
    with pytest.raises(LocalUpdateError, match="Forbidden read path"):
        build_local_update_plan(
            target, candidate, forbidden_read_paths=[".planning/private/**"]
        )
    allowed = build_local_update_plan(
        target, candidate, forbidden_read_paths=[".planning/other/**"]
    )
    assert allowed.mutations


def test_explicit_update_source_is_passed_to_local_candidate(tmp_path: Path, monkeypatch) -> None:
    target = tmp_path / "repo"
    candidate = tmp_path / "candidate"
    _init_local_only_repo(target)
    _write_minimal_target(target)
    candidate.mkdir()
    _write_minimal_candidate(candidate)
    selected: dict[str, object] = {}

    def render(**kwargs):  # type: ignore[no-untyped-def]
        selected.update(kwargs)
        return _CandidateHandle(candidate)

    monkeypatch.setattr(cli, "_render_local_update_candidate", render)
    args = cli.build_parser().parse_args(
        ["check", str(target), "--template-source", str(ROOT)]
    )
    assert cli.command_update(args) == 0
    assert selected["template_source"] == str(ROOT)


def test_project_owned_to_managed_transition_fails_closed(tmp_path: Path) -> None:
    target = tmp_path / "target"
    candidate = tmp_path / "candidate"
    target.mkdir()
    candidate.mkdir()
    (target / ANSWERS_FILE).write_text("_commit: old\n", encoding="utf-8")
    old_policy = target / ".planning/framework/OWNERSHIP.yml"
    old_policy.parent.mkdir(parents=True, exist_ok=True)
    old_policy.write_text(
        "schema_version: 1\nmanaged:\n- .planning/framework/**\n"
        "project_owned:\n- .planning/control/**\n"
        "installer_metadata:\n- .copier-answers.planning-lite.yml\n",
        encoding="utf-8",
    )
    (target / ".planning/control").mkdir(parents=True, exist_ok=True)
    (target / ".planning/control/CUSTOM.md").write_text("user-owned\n", encoding="utf-8")

    _write_minimal_candidate(candidate)
    (candidate / ".planning/control/CUSTOM.md").write_text("framework-owned\n", encoding="utf-8")

    with pytest.raises(LocalUpdateError, match="project_owned -> managed"):
        build_local_update_plan(target, candidate)


def test_apply_rolls_back_when_post_apply_verification_fails(
    tmp_path: Path, monkeypatch
) -> None:
    import planning_lite.local_update as local_update

    target = tmp_path / "target"
    candidate = tmp_path / "candidate"
    target.mkdir()
    candidate.mkdir()
    (target / ANSWERS_FILE).write_text("_commit: old\n", encoding="utf-8")
    _write_minimal_target(target)
    _write_minimal_candidate(candidate)
    before = {path: file.read_bytes() for path, file in iter_files(target).items()}
    plan = build_local_update_plan(target, candidate)

    monkeypatch.setattr(
        local_update,
        "_verify_applied_plan",
        lambda *args, **kwargs: (_ for _ in ()).throw(LocalUpdateError("forced verification failure")),
    )
    with pytest.raises(LocalUpdateError, match="forced verification failure"):
        apply_local_update_plan(target, candidate, plan)

    after = {path: file.read_bytes() for path, file in iter_files(target).items()}
    assert after == before
