from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from planning_lite.authorization import (
    AuthorizationAction,
    PreparationScopeV1,
    RecoveryScopeV1,
    ResolutionOutcome,
    resolve_authorization,
)
from planning_lite.cli import main


def _target(root: Path) -> Path:
    framework = root / ".planning/framework"
    framework.mkdir(parents=True)
    (framework / "defaults.yml").write_text(
        "schema_version: 1\n"
        "project_policy:\n"
        "  schema_version: 1\n"
        "  planning_root: managed-planning\n"
        "  agents_root: managed-agents\n"
        "  forbidden_read_paths: []\n"
        "  secret_storage: prohibited\n",
        encoding="utf-8",
    )
    (root / "managed-planning/CONFIG.yml").parent.mkdir(parents=True, exist_ok=True)
    (root / "managed-planning/CONFIG.yml").write_text("{}\n", encoding="utf-8")
    return root


def test_preparation_positive_and_recovery_traversability_for_custom_planning_root(
    tmp_path: Path, capsys
) -> None:
    target = _target(tmp_path / "consumer")
    assert main(
        [
            "authorize-preparation",
            str(target),
            "--change-id",
            "CHG-1",
            "--task-or-operation-id",
            "TASK-1",
            "--decision-provenance-ref",
            "PROV-1",
        ]
    ) == 0
    preparation_ref = capsys.readouterr().out.strip()
    assert preparation_ref.startswith("authz_")
    preparation = resolve_authorization(
        target,
        preparation_ref,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("CHG-1", "TASK-1"),
    )
    assert preparation.outcome is ResolutionOutcome.AUTHORIZED

    assert main(
        [
            "authorize-recovery",
            str(target),
            "--attempt-id",
            "ATTEMPT-1",
            "--decision-provenance-ref",
            "PROV-2",
        ]
    ) == 0
    recovery_ref = capsys.readouterr().out.strip()
    recovery = resolve_authorization(
        target,
        recovery_ref,
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1("ATTEMPT-1"),
    )
    assert recovery.outcome is ResolutionOutcome.AUTHORIZED
    assert (target / "managed-planning/project/authorizations").is_dir()


def test_cli_authorization_arguments_are_required() -> None:
    from planning_lite.cli import build_parser

    parser = build_parser()
    for argv in (
        ["authorize-preparation", "target", "--change-id", "C"],
        ["authorize-recovery", "target", "--attempt-id", "A"],
    ):
        try:
            parser.parse_args(argv)
        except SystemExit as exc:
            assert exc.code == 2
        else:  # pragma: no cover
            raise AssertionError("missing provenance was accepted")


@pytest.mark.parametrize("action", ["preparation", "recovery"])
def test_independent_closure_single_use_contract(action: str, tmp_path: Path, capsys) -> None:
    target = _target(tmp_path / "consumer")
    if action == "preparation":
        argv = [
            "authorize-preparation",
            str(target),
            "--change-id",
            "CHG-CLOSURE",
            "--task-or-operation-id",
            "TASK-CLOSURE",
            "--decision-provenance-ref",
            "PROV-CLOSURE",
        ]
        expected_action = AuthorizationAction.PREPARATION
        expected_scope = PreparationScopeV1("CHG-CLOSURE", "TASK-CLOSURE")
    else:
        argv = [
            "authorize-recovery",
            str(target),
            "--attempt-id",
            "ATTEMPT-CLOSURE",
            "--decision-provenance-ref",
            "PROV-CLOSURE",
        ]
        expected_action = AuthorizationAction.RECOVERY
        expected_scope = RecoveryScopeV1("ATTEMPT-CLOSURE")
    assert main(argv) == 0
    reference = capsys.readouterr().out.strip()
    record_path = target / "managed-planning/project/authorizations" / f"{reference}.json"
    before_hash = hashlib.sha256(record_path.read_bytes()).hexdigest()
    used: set[str] = set()

    def consumer_admits(*, commit: bool) -> bool:
        resolved = resolve_authorization(target, reference, expected_action, expected_scope)
        if resolved.outcome is not ResolutionOutcome.AUTHORIZED or reference in used:
            return False
        if commit:
            used.add(reference)
        return True

    assert consumer_admits(commit=False) is True
    assert used == set()
    assert consumer_admits(commit=False) is True
    assert consumer_admits(commit=True) is True
    assert consumer_admits(commit=True) is False
    assert resolve_authorization(
        target, reference, expected_action, expected_scope
    ).outcome is ResolutionOutcome.AUTHORIZED
    assert hashlib.sha256(record_path.read_bytes()).hexdigest() == before_hash
