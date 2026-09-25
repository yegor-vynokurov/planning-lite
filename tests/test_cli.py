from __future__ import annotations

from pathlib import Path
import hashlib
import json

import yaml
import pytest

from planning_lite import cli
from planning_lite.cli import BRIDGE_START, _ensure_agents_bridge, build_parser, main
from planning_lite.governed_executor import GovernedExecutionResultV1
from planning_lite.operation_lifecycle import GovernedLifecycleResultV1
from planning_lite.attempt_runtime import attempt_store_path, claim_attempt, lookup_attempt
from planning_lite.authorization import (
    authorization_store_path,
    issue_preparation_authorization,
    issue_recovery_authorization,
)


_ATTEMPT_CHANGE = "CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001"
_ATTEMPT_TASK = "T-04"
_ATTEMPT_HEAD = "a" * 40


def _attempt_payload(reference: str, *, task_id: str = _ATTEMPT_TASK) -> dict[str, object]:
    return {
        "change_id": _ATTEMPT_CHANGE,
        "task_or_operation_id": task_id,
        "authorization_ref": reference,
        "acceptance_contract_ref": "AC-04",
        "candidate_identity": {"kind": "GIT_COMMIT", "head": _ATTEMPT_HEAD, "dirty_manifest": []},
        "baseline_refs": [{"ref": "HEAD", "identity": _ATTEMPT_HEAD}],
    }


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


def test_authorize_issuers_have_explicit_required_contract() -> None:
    parser = build_parser()
    preparation = parser.parse_args(
        [
            "authorize-preparation",
            "consumer",
            "--change-id",
            "CHG-1",
            "--task-or-operation-id",
            "TASK-1",
            "--decision-provenance-ref",
            "PROV-1",
        ]
    )
    assert preparation.command == "authorize-preparation"
    assert preparation.target == "consumer"
    assert preparation.change_id == "CHG-1"
    assert preparation.task_or_operation_id == "TASK-1"
    assert preparation.decision_provenance_ref == "PROV-1"

    recovery = parser.parse_args(
        [
            "authorize-recovery",
            "consumer",
            "--attempt-id",
            "ATTEMPT-1",
            "--decision-provenance-ref",
            "PROV-2",
        ]
    )
    assert recovery.command == "authorize-recovery"
    assert recovery.attempt_id == "ATTEMPT-1"
    assert not hasattr(recovery, "change_id")


def test_attempt_prepare_uses_production_runtime_adapter(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    reference = issue_preparation_authorization(tmp_path, _ATTEMPT_CHANGE, _ATTEMPT_TASK, "OWNER-DECISION")
    payload_path = tmp_path / "preparation.json"
    payload_path.write_text(json.dumps(_attempt_payload(reference)), encoding="utf-8")
    authorization_before = next(authorization_store_path(tmp_path).glob(f"{reference}.json")).read_bytes()

    assert main(["attempt-prepare", str(tmp_path), "--input", str(payload_path)]) == 0
    attempt_id = capsys.readouterr().out.strip()
    assert attempt_id == f"{_ATTEMPT_CHANGE}/{_ATTEMPT_TASK}/A1"
    found = lookup_attempt(tmp_path, attempt_id)
    assert found.outcome.value == "FOUND"
    assert found.runtime_state == "ACTIVATABLE"
    assert found.attempt.authorization_ref == reference
    assert next(authorization_store_path(tmp_path).glob(f"{reference}.json")).read_bytes() == authorization_before


def test_cli_preparation_authorization_negative_matrix(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    wrong_scope = issue_preparation_authorization(tmp_path, _ATTEMPT_CHANGE, "T-WRONG", "OWNER-DECISION")
    payload_path = tmp_path / "preparation.json"
    for reference in ("malformed", "authz_" + "0" * 32, wrong_scope):
        payload_path.write_text(json.dumps(_attempt_payload(reference)), encoding="utf-8")
        assert main(["attempt-prepare", str(tmp_path), "--input", str(payload_path)]) == 2
        capsys.readouterr()
    assert not attempt_store_path(tmp_path).exists()


def test_attempt_commands_are_thin_adapters(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    called: list[Path] = []

    class Result:
        attempt_id = "CHG/T/A1"
        runtime_state = "ACTIVATABLE"
        observed_result = None

    def fake_prepare(target, preparation):
        called.append(Path(target))
        return Result()

    monkeypatch.setattr(cli, "prepare_attempt", fake_prepare)
    payload = tmp_path / "input.json"
    payload.write_text("{}", encoding="utf-8")
    assert main(["attempt-prepare", str(tmp_path), "--input", str(payload)]) == 0
    assert capsys.readouterr().out.strip() == "CHG/T/A1"
    assert called == [tmp_path.resolve()]
    source = Path(cli.__file__).read_text(encoding="utf-8")
    assert "resolve_authorization(" not in source
    assert "os.replace" not in source


def test_attempt_runtime_reuses_closed_authorization_boundary() -> None:
    root = Path(__file__).resolve().parents[1]
    authorization = root / "src/planning_lite/authorization.py"
    digest_before = hashlib.sha256(authorization.read_bytes()).hexdigest()
    source = Path(cli.__file__).read_text(encoding="utf-8")
    assert "from .attempt_runtime import" in source
    assert hashlib.sha256(authorization.read_bytes()).hexdigest() == digest_before


def test_clean_target_production_preparation_materialization(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    reference = issue_preparation_authorization(tmp_path, _ATTEMPT_CHANGE, _ATTEMPT_TASK, "OWNER-DECISION")
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps(_attempt_payload(reference)), encoding="utf-8")
    assert main(["attempt-prepare", str(tmp_path), "--input", str(payload), "--json"]) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["attempt_id"].endswith("/A1")
    assert json.loads(attempt_store_path(tmp_path).read_text(encoding="utf-8"))["attempts"][0]["runtime_state"] == "ACTIVATABLE"


def test_clean_target_production_interrupted_recovery(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    preparation = issue_preparation_authorization(tmp_path, _ATTEMPT_CHANGE, _ATTEMPT_TASK, "OWNER-DECISION")
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps(_attempt_payload(preparation)), encoding="utf-8")
    assert main(["attempt-prepare", str(tmp_path), "--input", str(payload)]) == 0
    attempt_id = capsys.readouterr().out.strip()
    claim_attempt(tmp_path, attempt_id)
    recovery = issue_recovery_authorization(tmp_path, attempt_id, "OWNER-RECOVERY")
    assert main(
        [
            "attempt-resolve-interrupted",
            str(tmp_path),
            "--attempt-id",
            attempt_id,
            "--authorization-ref",
            recovery,
            "--json",
        ]
    ) == 0
    result = json.loads(capsys.readouterr().out)
    assert result == {"attempt_id": attempt_id, "execution_status": "INTERRUPTED", "runtime_state": "TERMINAL"}


def test_cli_recovery_authorization_negative_matrix(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    preparation = issue_preparation_authorization(tmp_path, _ATTEMPT_CHANGE, _ATTEMPT_TASK, "OWNER-DECISION")
    payload = tmp_path / "payload.json"
    payload.write_text(json.dumps(_attempt_payload(preparation)), encoding="utf-8")
    assert main(["attempt-prepare", str(tmp_path), "--input", str(payload)]) == 0
    attempt_id = capsys.readouterr().out.strip()
    claim_attempt(tmp_path, attempt_id)
    other = issue_recovery_authorization(tmp_path, f"{_ATTEMPT_CHANGE}/{_ATTEMPT_TASK}/A9", "OWNER-RECOVERY")
    for reference in ("malformed", "authz_" + "0" * 32, preparation, other):
        assert main(
            [
                "attempt-resolve-interrupted",
                str(tmp_path),
                attempt_id,
                "--authorization-ref",
                reference,
            ]
        ) == 2
        capsys.readouterr()
    assert lookup_attempt(tmp_path, attempt_id).runtime_state == "IN_FLIGHT"


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


def test_execute_prepare_complete_route(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    def fake_execute(*args, **kwargs):
        assert args[1] == "CHG/T/A1"
        return GovernedLifecycleResultV1("COMPLETED_WITH_FACTS", "CHG/T/A1")

    monkeypatch = pytest.MonkeyPatch()
    try:
        monkeypatch.setattr(cli, "execute_governed_operation", fake_execute)
        input_path = tmp_path / "execute.json"
        input_path.write_text('{"attempt_id":"CHG/T/A1","payload":{}}', encoding="utf-8")
        assert main(["execute", str(tmp_path), "--input", str(input_path), "--json"]) == 0
        assert json.loads(capsys.readouterr().out)["disposition"] == "COMPLETED_WITH_FACTS"
    finally:
        monkeypatch.undo()


def test_execute_renders_typed_result_when_receipt_is_incomplete(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    execution = GovernedExecutionResultV1(
        attempt_id="CHG/T/A1",
        execution_invocation_id="A" * 64,
        accepted=True,
        outcome="COMPLETED",
        result_id="RESULT-1",
        execution_status="COMPLETED",
        changed_paths=("artifact.txt",),
        fact_refs=("FACT-1",),
        artifact_refs=("artifact.txt",),
    )
    stopped = GovernedLifecycleResultV1(
        disposition="STOPPED_FAIL_CLOSED",
        attempt_id="CHG/T/A1",
        first_broken_seam="GOVERNED_RECEIPT_COLLECTION",
        reason_code="RECEIPT_MISSING",
        execution=execution,
    )
    monkeypatch.setattr(cli, "execute_governed_operation", lambda *args, **kwargs: stopped)
    input_path = tmp_path / "execute.json"
    input_path.write_text(
        '{"attempt_id":"CHG/T/A1","guidance":{"outcome":"MATCHED"}}',
        encoding="utf-8",
    )

    assert main(["execute", str(tmp_path), "--input", str(input_path), "--json"]) == 2

    payload = json.loads(capsys.readouterr().out)
    assert payload["disposition"] == "STOPPED_FAIL_CLOSED"
    assert payload["reason_code"] == "RECEIPT_MISSING"
    assert payload["execution"] == {
        "accepted": True,
        "artifact_refs": ["artifact.txt"],
        "attempt_id": "CHG/T/A1",
        "changed_paths": ["artifact.txt"],
        "completion": None,
        "envelope_digest": None,
        "execution_invocation_id": "A" * 64,
        "execution_status": "COMPLETED",
        "fact_refs": ["FACT-1"],
        "failure_category": None,
        "operation_id": None,
        "outcome": "COMPLETED",
        "receipt_id": None,
        "result_id": "RESULT-1",
        "task_or_operation_id": None,
    }
    assert payload["receipt"] is None
    assert payload["observed_result"] is None
    assert payload["technical_evaluation"] is None
    assert payload["terminal_attempt"] is None
    assert payload["downstream"] is None


def test_finish_requires_typed_current_cycle(tmp_path: Path) -> None:
    input_path = tmp_path / "finish.json"
    input_path.write_text('{"action":"FINISH"}', encoding="utf-8")
    assert main(["finish", str(tmp_path), "--input", str(input_path)]) == 2


def test_status_route_is_read_only(tmp_path: Path) -> None:
    before = (tmp_path / "marker").write_text("keep", encoding="utf-8")
    original = (tmp_path / "marker").read_bytes()
    monkeypatch = pytest.MonkeyPatch()
    try:
        monkeypatch.setattr(cli, "build_compact_status", lambda *args, **kwargs: {
            "where_we_are": {}, "what_is_done": {}, "what_is_current": {},
            "what_next": "EXECUTE_AUTHORIZED_TASK", "resources": {}, "state": {},
        })
        assert main(["status", str(tmp_path), "--json"]) == 0
    finally:
        monkeypatch.undo()
    assert (tmp_path / "marker").read_bytes() == original
