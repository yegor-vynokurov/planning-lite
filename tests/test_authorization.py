from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest

import planning_lite.authorization as authorization
from planning_lite.authorization import (
    AuthorizationAction,
    AuthorizationError,
    AuthorizationRecordV1,
    PreparationScopeV1,
    RecoveryScopeV1,
    ResolutionOutcome,
    decode_authorization_record,
    encode_authorization_record,
    issue_preparation_authorization,
    issue_recovery_authorization,
    resolve_authorization,
)


def _target(root: Path) -> Path:
    defaults = root / ".planning/framework/defaults.yml"
    defaults.parent.mkdir(parents=True)
    defaults.write_text(
        "schema_version: 1\n"
        "project_policy:\n"
        "  schema_version: 1\n"
        "  planning_root: .planning\n"
        "  agents_root: .agents\n"
        "  forbidden_read_paths: []\n"
        "  secret_storage: prohibited\n",
        encoding="utf-8",
    )
    (root / ".planning/CONFIG.yml").write_text("{}\n", encoding="utf-8")
    return root


def test_preparation_record_is_exact_canonical_and_resolves(tmp_path: Path) -> None:
    target = _target(tmp_path / "consumer")
    reference = issue_preparation_authorization(
        target, "CHG-PL-V39-09", "TASK-01", "PLAN-APPROVAL-REF"
    )
    assert reference.startswith("authz_") and len(reference) == 38
    store = authorization.authorization_store_path(target)
    raw = (store / f"{reference}.json").read_bytes()
    expected = (
        "{\"action_type\":\"OWNER_AUTHORIZED_ATTEMPT_PREPARATION\","
        f"\"authorization_ref\":\"{reference}\","
        "\"decision_authority_class\":\"EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY\","
        "\"decision_outcome\":\"AUTHORIZED\","
        "\"decision_provenance_ref\":\"PLAN-APPROVAL-REF\","
        "\"schema_version\":1,"
        "\"scope\":{\"change_id\":\"CHG-PL-V39-09\",\"task_or_operation_id\":\"TASK-01\"}}\n"
    ).encode()
    assert raw == expected
    result = resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("CHG-PL-V39-09", "TASK-01"),
    )
    assert result.outcome is ResolutionOutcome.AUTHORIZED
    assert result.record is not None
    assert encode_authorization_record(result.record) == raw


def test_recovery_negative_scope_and_wrong_action_or_scope(tmp_path: Path) -> None:
    target = _target(tmp_path / "consumer")
    reference = issue_recovery_authorization(target, "ATTEMPT-01", "LIFECYCLE-REF")
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("CHANGE", "TASK"),
    ).outcome is ResolutionOutcome.WRONG_ACTION
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1("OTHER"),
    ).outcome is ResolutionOutcome.WRONG_SCOPE
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1("ATTEMPT-01"),
    ).outcome is ResolutionOutcome.AUTHORIZED


@pytest.mark.parametrize(
    "raw",
    [
        b'{"action_type":"OWNER_AUTHORIZED_ATTEMPT_PREPARATION","authorization_ref":"authz_00000000000000000000000000000000","authorization_ref":"authz_00000000000000000000000000000000","decision_authority_class":"EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY","decision_outcome":"AUTHORIZED","decision_provenance_ref":"P","schema_version":1,"scope":{"change_id":"C","task_or_operation_id":"T"}}\n',
        b'{"action_type":"OWNER_AUTHORIZED_ATTEMPT_PREPARATION","authorization_ref":"authz_00000000000000000000000000000000","decision_authority_class":"EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY","decision_outcome":"AUTHORIZED","decision_provenance_ref":"P","schema_version":1,"scope":{"change_id":"C","change_id":"C","task_or_operation_id":"T"}}\n',
        b'{"action_type":"OWNER_AUTHORIZED_ATTEMPT_PREPARATION","authorization_ref":"authz_00000000000000000000000000000000","decision_authority_class":"EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY","decision_outcome":"AUTHORIZED","decision_provenance_ref":"P","schema_version":1,"scope":{"change_id":"C","task_or_operation_id":"T"}}',
    ],
)
def test_codec_rejects_duplicate_or_noncanonical_bytes(raw: bytes) -> None:
    with pytest.raises(AuthorizationError):
        decode_authorization_record(raw)


@pytest.mark.parametrize("value", [" C", "C ", "", "C\nD", "C\rD"])
def test_preparation_negative_identifiers_are_not_trimmed_or_normalized(
    tmp_path: Path, value: str
) -> None:
    target = _target(tmp_path / "consumer")
    with pytest.raises(AuthorizationError):
        issue_preparation_authorization(target, value, "TASK", "PROVENANCE")


@pytest.mark.parametrize(
    ("change_id", "task_id", "provenance"),
    [
        ("ChG-Case", "Task.Mixed", "Proof/α"),
        ("Δ-change::v2", "task/compound[1]", "Owner.Ref/β"),
    ],
)
def test_accepted_identifiers_are_preserved_exactly(
    tmp_path: Path, change_id: str, task_id: str, provenance: str
) -> None:
    target = _target(tmp_path / "consumer")
    reference = issue_preparation_authorization(target, change_id, task_id, provenance)
    raw = (authorization.authorization_store_path(target) / f"{reference}.json").read_bytes()
    record = decode_authorization_record(raw)
    assert record.scope == PreparationScopeV1(change_id, task_id)
    assert record.decision_provenance_ref == provenance
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(change_id, task_id),
    ).outcome is ResolutionOutcome.AUTHORIZED


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("change_id", ""),
        ("change_id", " CHANGE"),
        ("task_or_operation_id", "TASK "),
        ("task_or_operation_id", "TASK\nID"),
        ("decision_provenance_ref", "PROOF\rID"),
    ],
)
def test_malformed_preparation_identifier_rejects_without_writing(
    tmp_path: Path, field: str, value: str
) -> None:
    target = _target(tmp_path / "consumer")
    values = {
        "change_id": "CHANGE",
        "task_or_operation_id": "TASK",
        "decision_provenance_ref": "PROVENANCE",
    }
    values[field] = value
    with pytest.raises(AuthorizationError):
        issue_preparation_authorization(
            target,
            values["change_id"],
            values["task_or_operation_id"],
            values["decision_provenance_ref"],
        )
    store = authorization.authorization_store_path(target)
    assert not list(store.glob("*.json"))
    assert not list(store.glob("*.tmp"))


def test_preparation_wrong_change_and_wrong_task_are_separate_exact_scope_failures(
    tmp_path: Path,
) -> None:
    target = _target(tmp_path / "consumer")
    reference = issue_preparation_authorization(target, "CHANGE", "TASK", "PROVENANCE")
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("OTHER-CHANGE", "TASK"),
    ).outcome is ResolutionOutcome.WRONG_SCOPE
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("CHANGE", "OTHER-TASK"),
    ).outcome is ResolutionOutcome.WRONG_SCOPE


def test_preparation_negative_invalid_reference_not_found_and_resolver_is_read_only(
    tmp_path: Path,
) -> None:
    target = _target(tmp_path / "consumer")
    before = sorted(p.relative_to(target).as_posix() for p in target.rglob("*"))
    invalid = resolve_authorization(
        target, "not-an-authorization", AuthorizationAction.RECOVERY, RecoveryScopeV1("A")
    )
    assert invalid.outcome is ResolutionOutcome.INVALID_REFERENCE
    missing = resolve_authorization(
        target,
        "authz_00000000000000000000000000000000",
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1("A"),
    )
    assert missing.outcome is ResolutionOutcome.NOT_FOUND
    after = sorted(p.relative_to(target).as_posix() for p in target.rglob("*"))
    assert before == after


def test_corrupt_or_filename_conflict_fails_closed(tmp_path: Path) -> None:
    target = _target(tmp_path / "consumer")
    store = authorization.authorization_store_path(target)
    store.mkdir(parents=True)
    reference = "authz_" + "c" * 32
    (store / "not-the-reference.json").write_bytes(
        (
            "{\"action_type\":\"OWNER_AUTHORIZED_ATTEMPT_PREPARATION\","
            f"\"authorization_ref\":\"{reference}\","
            "\"decision_authority_class\":\"EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY\","
            "\"decision_outcome\":\"AUTHORIZED\",\"decision_provenance_ref\":\"P\","
            "\"schema_version\":1,\"scope\":{\"change_id\":\"C\",\"task_or_operation_id\":\"T\"}}\n"
        ).encode()
    )
    result = resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("C", "T"),
    )
    assert result.outcome is ResolutionOutcome.CORRUPT_CONFLICT


def test_ref_collision_exhaustion_does_not_overwrite_or_leave_partial(tmp_path: Path, monkeypatch) -> None:
    target = _target(tmp_path / "consumer")
    fixed = "authz_" + "a" * 32
    store = authorization.authorization_store_path(target)
    store.mkdir(parents=True)
    final = store / f"{fixed}.json"
    original = b"existing-bytes\n"
    final.write_bytes(original)
    monkeypatch.setattr(authorization, "_allocate_authorization_ref", lambda: fixed)
    with pytest.raises(AuthorizationError, match="AUTHORIZATION_REF_ALLOCATION_EXHAUSTED"):
        issue_recovery_authorization(target, "A", "P")
    assert final.read_bytes() == original
    assert not list(store.glob("*.tmp"))


def test_eight_process_cli_issuances_are_unique_complete_and_immutable(tmp_path: Path) -> None:
    target = _target(tmp_path / "consumer")
    command = (
        "from planning_lite.cli import main; import sys; "
        "raise SystemExit(main(sys.argv[1:]))"
    )
    argv = [
        sys.executable,
        "-c",
        command,
        "authorize-preparation",
        str(target),
        "--change-id",
        "CHANGE-PROCESS",
        "--task-or-operation-id",
        "TASK-PROCESS",
        "--decision-provenance-ref",
        "PROCESS-PROOF",
    ]

    def issue_in_independent_process() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            argv,
            cwd=Path(__file__).resolve().parents[1],
            check=False,
            capture_output=True,
            text=True,
        )

    with ThreadPoolExecutor(max_workers=8) as pool:
        completed = list(pool.map(lambda _: issue_in_independent_process(), range(8)))
    assert all(
        result.returncode == 0 for result in completed
    ), [(result.returncode, result.stdout, result.stderr) for result in completed]
    references = [result.stdout.strip() for result in completed]
    assert len(set(references)) == 8
    store = authorization.authorization_store_path(target)
    records = sorted(store.glob("*.json"))
    assert len(records) == 8
    assert {path.stem for path in records} == set(references)
    before_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in records}
    for path in records:
        decoded = decode_authorization_record(path.read_bytes())
        assert decoded.authorization_ref == path.stem
        assert resolve_authorization(
            target,
            path.stem,
            AuthorizationAction.PREPARATION,
            PreparationScopeV1("CHANGE-PROCESS", "TASK-PROCESS"),
        ).outcome is ResolutionOutcome.AUTHORIZED
    after_hashes = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in records}
    assert after_hashes == before_hashes
    assert not list(store.glob("*.tmp"))


@pytest.mark.parametrize(
    "decoy_relative",
    [
        ".planning/project/CURRENT.md",
        ".planning/ACTIVE.md",
        ".local/work/experiments/authorization.json",
        "AUTHORIZATION.md",
        ".planning/project/evidence/AUTHORIZATION_RECEIPT.json",
        ".planning/project/attempts/ATTEMPT-1.json",
    ],
)
def test_decoy_authority_sources_cannot_issue_or_resolve(
    tmp_path: Path, decoy_relative: str
) -> None:
    target = _target(tmp_path / "consumer")
    record = AuthorizationRecordV1(
        1,
        "authz_" + "d" * 32,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("CHANGE-DECOY", "TASK-DECOY"),
        authorization.PREPARATION_AUTHORITY,
        "AUTHORIZED",
        "DECOY-PROVENANCE",
    )
    decoy = target / decoy_relative
    decoy.parent.mkdir(parents=True, exist_ok=True)
    decoy.write_bytes(authorization.encode_authorization_record(record))
    result = resolve_authorization(
        target,
        record.authorization_ref,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1("CHANGE-DECOY", "TASK-DECOY"),
    )
    assert result.outcome is ResolutionOutcome.NOT_FOUND
    assert not list(authorization.authorization_store_path(target).glob("*.json"))


def test_encode_rejects_scope_action_mismatch() -> None:
    record = authorization.AuthorizationRecordV1(
        1,
        "authz_" + "b" * 32,
        AuthorizationAction.PREPARATION,
        RecoveryScopeV1("A"),
        authorization.PREPARATION_AUTHORITY,
        "AUTHORIZED",
        "P",
    )
    with pytest.raises(AuthorizationError):
        encode_authorization_record(record)
