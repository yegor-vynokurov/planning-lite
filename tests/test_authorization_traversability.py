from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from planning_lite.authorization import (
    AuthorizationAction,
    AuthorizationRecordV2,
    PreparationScopeV2,
    RecoveryScopeV1,
    ResolutionOutcome,
    decode_authorization_record,
    resolve_authorization,
)
from planning_lite.dependency_admission import resolve_dependency
from planning_lite.cli import main
from test_authorization import _governed_target


def _target(root: Path, *, change_id: str | None = None) -> Path:
    """Select managed-planning for canonical governance and owner stores."""
    if change_id is not None:
        return _governed_target(
            root,
            change_id=change_id,
            task_ids=("T-03",),
            planning_root="managed-planning",
        )
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
    """Prove resolver, Preparation, and Recovery traversal under managed-planning.

    Bootstrap CONFIG remains in product ``.planning``. The complete canonical
    Change and ACTIVE pointer live below the selected effective root; the
    resulting Preparation refs remain product-root-relative, while Recovery
    retains its Plan-independent V1 path.
    """
    target = _target(
        tmp_path / "consumer",
        change_id="CHG-1",
    )
    assert main(
        [
            "authorize-preparation",
            str(target),
            "--change-id",
            "CHG-1",
            "--task-or-operation-id",
            "T-03",
            "--decision-provenance-ref",
            "PROV-1",
        ]
    ) == 0
    preparation_ref = capsys.readouterr().out.strip()
    assert preparation_ref.startswith("authz_")
    preparation_record = decode_authorization_record(
        (target / "managed-planning/project/authorizations" / f"{preparation_ref}.json").read_bytes()
    )
    assert isinstance(preparation_record, AuthorizationRecordV2)
    current = resolve_dependency(target, "T-03")
    assert current.plan_ref == "managed-planning/changes/active/CHG-1/plan.md"
    assert current.tasks_ref == "managed-planning/changes/active/CHG-1/tasks.md"
    assert preparation_record.scope == PreparationScopeV2(
        "CHG-1",
        "T-03",
        current.plan_ref,
        current.tasks_ref,
        current.approved_plan_digest,
        current.dependency_semantic_digest,
        current.requirement["requirement_id"],
        "NOT_APPLICABLE",
        None,
    )
    preparation = resolve_authorization(
        target,
        preparation_ref,
        AuthorizationAction.PREPARATION,
        preparation_record.scope,
    )
    assert preparation.outcome is ResolutionOutcome.AUTHORIZED
    from planning_lite.attempt_runtime import attempt_store_v2_path

    v2_store = attempt_store_v2_path(target)
    assert v2_store == target / "managed-planning/changes/active/.planning-lite/attempt-runtime-v2.json"
    assert (v2_store.parent / f"{v2_store.name}.lock").is_file()
    assert not v2_store.exists()
    assert not (v2_store.parent / "dependency-admission/cancellations").exists()

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
    """Keep V2 single-use semantics; custom-root Preparation shares the D2 path mismatch above."""
    target = _target(
        tmp_path / "consumer",
        change_id="CHG-CLOSURE" if action == "preparation" else None,
    )
    if action == "preparation":
        argv = [
            "authorize-preparation",
            str(target),
            "--change-id",
            "CHG-CLOSURE",
            "--task-or-operation-id",
            "T-03",
            "--decision-provenance-ref",
            "PROV-CLOSURE",
        ]
        expected_action = AuthorizationAction.PREPARATION
        expected_scope = None
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
    if action == "preparation":
        record = decode_authorization_record(record_path.read_bytes())
        assert isinstance(record, AuthorizationRecordV2)
        current = resolve_dependency(target, "T-03")
        expected_scope = PreparationScopeV2(
            "CHG-CLOSURE",
            "T-03",
            current.plan_ref,
            current.tasks_ref,
            current.approved_plan_digest,
            current.dependency_semantic_digest,
            current.requirement["requirement_id"],
            "NOT_APPLICABLE",
            None,
        )
        assert record.scope == expected_scope
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
