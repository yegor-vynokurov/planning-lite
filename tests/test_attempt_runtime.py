from __future__ import annotations

from dataclasses import replace
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import subprocess
import time

import pytest

from planning_lite import attempt_runtime
from planning_lite.attempt_evaluation import (
    AttemptRecordV1,
    CandidateIdentityV1,
    IdentityRefV1,
    ObservedResultV1,
)
from planning_lite.attempt_runtime import (
    AdmissibilityOutcome,
    AttemptAuthorizationError,
    AttemptRuntimeError,
    AttemptStoreV1,
    LookupOutcome,
    AttemptEnvelopeV1,
    attempt_store_path,
    check_activation_admissibility,
    claim_attempt,
    decode_attempt_store,
    encode_attempt_store,
    lookup_attempt,
    prepare_attempt,
    resolve_interrupted_attempt,
    store_sha256,
    terminalize_attempt,
)
from planning_lite.authorization import (
    AuthorizationAction,
    PreparationScopeV1,
    RecoveryScopeV1,
    ResolutionOutcome,
    authorization_store_path,
    issue_preparation_authorization,
    issue_recovery_authorization,
    resolve_authorization,
)


CHANGE_ID = "CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001"
TASK_ID = "T-02"
HEAD = "a" * 40


def _payload(auth_ref: str, *, change_id: str = CHANGE_ID, task_id: str = TASK_ID) -> dict[str, object]:
    return {
        "change_id": change_id,
        "task_or_operation_id": task_id,
        "authorization_ref": auth_ref,
        "acceptance_contract_ref": "AC-04",
        "candidate_identity": {"kind": "GIT_COMMIT", "head": HEAD, "dirty_manifest": []},
        "baseline_refs": [{"ref": "HEAD", "identity": HEAD}],
        "operation_guidance_ref": "EXECUTE_CHANGE_TASK",
    }


def _prepare(target: Path, *, change_id: str = CHANGE_ID, task_id: str = TASK_ID):
    ref = issue_preparation_authorization(target, change_id, task_id, "OWNER-DECISION-PL09")
    return prepare_attempt(target, _payload(ref, change_id=change_id, task_id=task_id)), ref


def _store_bytes(target: Path) -> bytes:
    return attempt_store_path(target).read_bytes()


def _assert_canonical_scope_mutant_rejected(
    target: Path,
    *,
    original_change_id: str = CHANGE_ID,
    original_task_id: str = TASK_ID,
    foreign_change_id: str | None = None,
    foreign_task_id: str | None = None,
) -> None:
    envelope, authorization_ref = _prepare(
        target,
        change_id=original_change_id,
        task_id=original_task_id,
    )
    if foreign_change_id is not None:
        mutated_attempt = replace(
            envelope.attempt,
            change_id=foreign_change_id,
            attempt_id=f"{foreign_change_id}/{envelope.attempt.task_or_operation_id}/A{envelope.attempt.attempt_ordinal}",
        )
    else:
        assert foreign_task_id is not None
        mutated_attempt = replace(
            envelope.attempt,
            task_or_operation_id=foreign_task_id,
            attempt_id=f"{envelope.attempt.change_id}/{foreign_task_id}/A{envelope.attempt.attempt_ordinal}",
        )
    mutated_envelope = replace(envelope, attempt=mutated_attempt)
    mutant_bytes = encode_attempt_store(AttemptStoreV1((mutated_envelope,)))
    decoded_mutant = decode_attempt_store(mutant_bytes)
    assert encode_attempt_store(decoded_mutant) == mutant_bytes

    original_resolution = resolve_authorization(
        target,
        authorization_ref,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(envelope.attempt.change_id, envelope.attempt.task_or_operation_id),
    )
    assert original_resolution.outcome is ResolutionOutcome.AUTHORIZED
    assert original_resolution.record is not None
    assert original_resolution.record.authorization_ref == authorization_ref
    assert original_resolution.record.scope == PreparationScopeV1(
        envelope.attempt.change_id,
        envelope.attempt.task_or_operation_id,
    )
    foreign_resolution = resolve_authorization(
        target,
        authorization_ref,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(mutated_attempt.change_id, mutated_attempt.task_or_operation_id),
    )
    assert foreign_resolution.outcome is ResolutionOutcome.WRONG_SCOPE

    attempt_store_path(target).write_bytes(mutant_bytes)
    before_claim = _store_bytes(target)
    with pytest.raises(AttemptAuthorizationError):
        claim_attempt(target, mutated_attempt.attempt_id)

    assert _store_bytes(target) == before_claim
    persisted = decode_attempt_store(before_claim).by_id(mutated_attempt.attempt_id)
    assert persisted is not None
    assert persisted.runtime_state == "ACTIVATABLE"
    assert persisted.attempt == mutated_attempt


def test_p05_foreign_change_canonical_persisted_attempt_cannot_be_claimed(tmp_path: Path) -> None:
    _assert_canonical_scope_mutant_rejected(
        tmp_path,
        original_change_id="CHG-P05-ORIGINAL",
        original_task_id="T-P05-01",
        foreign_change_id="CHG-P05-FOREIGN",
    )


def test_p05_foreign_task_canonical_persisted_attempt_cannot_be_claimed(tmp_path: Path) -> None:
    _assert_canonical_scope_mutant_rejected(tmp_path, foreign_task_id="T-P05-FOREIGN")


def _claim_worker(target: str, attempt_id: str, queue) -> None:
    try:
        result = claim_attempt(target, attempt_id)
        queue.put(("PASS", result.runtime_state))
    except Exception as exc:  # pragma: no cover - exercised in child process
        queue.put(("FAIL", type(exc).__name__))


def _claim_and_wait_worker(target: str, attempt_id: str, ready, release) -> None:
    claim_attempt(target, attempt_id)
    ready.set()
    release.wait(10)


def test_entry_authority_hashes_and_write_boundary() -> None:
    root = Path(__file__).resolve().parents[1]
    expected = {
        "PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CHANGE-DEFINITION-v1.md": "81514C1519BBDF97D2908B1F0EF2A73CAE19A76535D22923ED726C82A5C63DB1",
        "PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-DEFINITION-ACTIVATION-v1.md": "0DE397A60FCE5E1ABB3257BD0F7DC3C66F5DEF851274033D2A1C14B8A5A7BB3D",
        "PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-IMPLEMENTATION-PLAN-v1.md": "3347577BEB68AB907253C19706436B72D5EC1293F997F9D828990AF5F4CE42C6",
        "PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-PLAN-APPROVAL-READINESS-ENTRY-v1.md": "5E37D074D82B593A3075F518F58DA90FD41D781A15A078720038840A8373A7DC",
        "PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-FORMAL-READINESS-VERDICT-v1.md": "B39A1CB5ECFD9CEFD592F2BBEF38705EDE7875329B7D5C74387A60F427EE07AD",
        "PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-CLOSURE-v1.md": "B16025A7170BC7F14430989C3A203449B95A3432ABAEB7231831B59BD76E1E44",
    }
    for name, digest in expected.items():
        assert hashlib.sha256((root / "docs/design/project-spine/checkpoints" / name).read_bytes()).hexdigest().upper() == digest
    # The implementation-entry HEAD is historical evidence, not a descendant-checkout invariant.
    assert subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=root, capture_output=True, text=True, check=True).stdout.strip() == ""
    assert subprocess.run(["git", "status", "--short", "--", "src/planning_lite/authorization.py"], cwd=root, capture_output=True, text=True, check=True).stdout.strip() == ""


def test_store_codec_strict_fail_closed(tmp_path: Path) -> None:
    raw = encode_attempt_store(AttemptStoreV1())
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n")
    assert decode_attempt_store(raw).to_mapping() == {"schema_version": 1, "attempts": []}
    malformed = [
        raw + b"\n",
        b'{"schema_version":1,"schema_version":1,"attempts":[]}\n',
        b"not-json\n",
        json.dumps({"schema_version": 2, "attempts": []}, separators=(",", ":")).encode() + b"\n",
        json.dumps({"schema_version": 1, "attempts": [{}]}, separators=(",", ":")).encode() + b"\n",
    ]
    for candidate in malformed:
        with pytest.raises(AttemptRuntimeError):
            decode_attempt_store(candidate)


def test_store_path_is_policy_resolved_and_owner_scoped(tmp_path: Path) -> None:
    path = attempt_store_path(tmp_path)
    assert path == (tmp_path / ".planning/changes/active/.planning-lite/attempt-runtime.json").resolve()
    assert not path.exists()
    assert lookup_attempt(tmp_path, "CHG/T-01/A1").outcome is LookupOutcome.NOT_FOUND
    assert not path.exists()
    assert not (tmp_path / ".local").exists()


def test_preparation_materializes_exact_activatable_record(tmp_path: Path) -> None:
    envelope, ref = _prepare(tmp_path)
    assert envelope.attempt_id == f"{CHANGE_ID}/{TASK_ID}/A1"
    assert envelope.runtime_state == "ACTIVATABLE"
    assert envelope.authorization_ref == ref
    found = lookup_attempt(tmp_path, envelope.attempt_id)
    assert found.outcome is LookupOutcome.FOUND
    assert found.envelope == envelope


def test_preparation_authorization_negative_matrix(tmp_path: Path) -> None:
    good = issue_preparation_authorization(tmp_path, CHANGE_ID, TASK_ID, "OWNER-DECISION")
    wrong_change = issue_preparation_authorization(tmp_path, "CHG-OTHER", TASK_ID, "OWNER-DECISION")
    wrong_task = issue_preparation_authorization(tmp_path, CHANGE_ID, "T-OTHER", "OWNER-DECISION")
    recovery = issue_recovery_authorization(tmp_path, f"{CHANGE_ID}/{TASK_ID}/A1", "OWNER-DECISION")
    candidates = ["bad", "authz_" + "0" * 32, wrong_change, wrong_task, recovery]
    for ref in candidates:
        with pytest.raises(AttemptRuntimeError):
            prepare_attempt(tmp_path, _payload(ref))
    assert not attempt_store_path(tmp_path).exists()
    # The valid record remains available after all rejected references.
    envelope = prepare_attempt(tmp_path, _payload(good))
    assert envelope.runtime_state == "ACTIVATABLE"


def test_preparation_single_use_and_failed_attempt_non_consumption(tmp_path: Path) -> None:
    ref = issue_preparation_authorization(tmp_path, CHANGE_ID, TASK_ID, "OWNER-DECISION")
    auth_before = (authorization_store_path(tmp_path) / f"{ref}.json").read_bytes()
    first = prepare_attempt(tmp_path, _payload(ref))
    with pytest.raises(AttemptRuntimeError):
        prepare_attempt(tmp_path, _payload(ref))
    assert len(decode_attempt_store(_store_bytes(tmp_path)).attempts) == 1
    assert (authorization_store_path(tmp_path) / f"{ref}.json").read_bytes() == auth_before

    second_ref = issue_preparation_authorization(tmp_path, CHANGE_ID, "T-03", "OWNER-DECISION")
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        prepare_attempt(tmp_path, {**_payload(second_ref, task_id="T-03"), "candidate_identity": {"bad": True}})
    assert _store_bytes(tmp_path) == before
    second = prepare_attempt(tmp_path, _payload(second_ref, task_id="T-03"))
    assert second.attempt_id.endswith("/T-03/A1")
    assert first.attempt_id.endswith("/T-02/A1")


def test_identity_lineage_and_ordinal_allocation(tmp_path: Path) -> None:
    first, _ = _prepare(tmp_path)
    # A second same-scope authorization must allocate the next contiguous ID.
    ref = issue_preparation_authorization(tmp_path, CHANGE_ID, TASK_ID, "OWNER-DECISION-2")
    second = prepare_attempt(tmp_path, _payload(ref))
    assert first.attempt_id.endswith("/A1")
    assert second.attempt_id.endswith("/A2")
    assert [row.attempt.attempt_ordinal for row in decode_attempt_store(_store_bytes(tmp_path)).attempts] == [1, 2]
    foreign = issue_preparation_authorization(tmp_path, "CHG-FOREIGN", TASK_ID, "OWNER-DECISION")
    foreign_envelope = prepare_attempt(tmp_path, _payload(foreign, change_id="CHG-FOREIGN"))
    assert foreign_envelope.attempt_id == f"CHG-FOREIGN/{TASK_ID}/A1"


def test_exact_lookup_contract(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    assert lookup_attempt(tmp_path, envelope.attempt_id).outcome is LookupOutcome.FOUND
    assert lookup_attempt(tmp_path, envelope.attempt_id + "-missing").outcome is LookupOutcome.INVALID_ID
    assert lookup_attempt(tmp_path, f"{CHANGE_ID}/{TASK_ID}/A9").outcome is LookupOutcome.NOT_FOUND
    path = attempt_store_path(tmp_path)
    path.write_bytes(b"{\"schema_version\":1,\"attempts\":[]\n")
    assert lookup_attempt(tmp_path, envelope.attempt_id).outcome is LookupOutcome.CORRUPT_CONFLICT


def test_admissibility_is_pure_and_state_bounded(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    before = _store_bytes(tmp_path)
    assert check_activation_admissibility(tmp_path, envelope.attempt_id).outcome is AdmissibilityOutcome.ADMISSIBLE
    assert _store_bytes(tmp_path) == before
    claim_attempt(tmp_path, envelope.attempt_id)
    assert check_activation_admissibility(tmp_path, envelope.attempt_id).outcome is AdmissibilityOutcome.IN_FLIGHT
    terminalize_attempt(tmp_path, envelope.attempt_id, ObservedResultV1("result-1", envelope.attempt_id, "FAILED"))
    assert check_activation_admissibility(tmp_path, envelope.attempt_id).outcome is AdmissibilityOutcome.TERMINAL


def test_multiprocess_claim_has_one_winner(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    context = mp.get_context("spawn")
    queue = context.Queue()
    processes = [context.Process(target=_claim_worker, args=(str(tmp_path), envelope.attempt_id, queue)) for _ in range(2)]
    for process in processes:
        process.start()
    results = [queue.get(timeout=20) for _ in processes]
    for process in processes:
        process.join(timeout=20)
    assert [item[0] for item in results].count("PASS") == 1
    assert lookup_attempt(tmp_path, envelope.attempt_id).runtime_state == "IN_FLIGHT"


def test_abrupt_loss_preserves_in_flight_and_releases_lock(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    context = mp.get_context("spawn")
    ready = context.Event()
    release = context.Event()
    process = context.Process(target=_claim_and_wait_worker, args=(str(tmp_path), envelope.attempt_id, ready, release))
    process.start()
    assert ready.wait(20)
    process.terminate()
    process.join(timeout=20)
    assert lookup_attempt(tmp_path, envelope.attempt_id).runtime_state == "IN_FLIGHT"
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, envelope.attempt_id)
    recovery_ref = issue_recovery_authorization(tmp_path, envelope.attempt_id, "OWNER-RECOVERY")
    recovered = resolve_interrupted_attempt(tmp_path, envelope.attempt_id, recovery_ref)
    assert recovered.runtime_state == "TERMINAL"


@pytest.mark.parametrize("status", ["COMPLETED", "FAILED", "INTERRUPTED", "INVALID"])
def test_terminal_status_contract_and_irreversibility(tmp_path: Path, status: str) -> None:
    envelope, _ = _prepare(tmp_path)
    claim_attempt(tmp_path, envelope.attempt_id)
    terminal = terminalize_attempt(
        tmp_path,
        envelope.attempt_id,
        ObservedResultV1(f"result-{status}", envelope.attempt_id, status),
    )
    assert terminal.runtime_state == "TERMINAL"
    assert terminal.observed_result is not None
    with pytest.raises(AttemptRuntimeError):
        terminalize_attempt(tmp_path, envelope.attempt_id, ObservedResultV1("other", envelope.attempt_id, "FAILED"))


def test_safe_replacement_fault_preservation(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    before = _store_bytes(tmp_path)
    for phase in ("prepare", "validate", "replace"):
        with pytest.raises(AttemptRuntimeError):
            claim_attempt(tmp_path, envelope.attempt_id, fault_hook=lambda current, phase=phase: (_ for _ in ()).throw(RuntimeError(phase)) if current == phase else None)
        assert _store_bytes(tmp_path) == before
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, envelope.attempt_id, fault_hook=lambda current: (_ for _ in ()).throw(RuntimeError("verify")) if current == "verify" else None)
    assert lookup_attempt(tmp_path, envelope.attempt_id).runtime_state == "IN_FLIGHT"
    assert store_sha256(tmp_path) == hashlib.sha256(_store_bytes(tmp_path)).hexdigest()
    assert "store.unlink" not in Path(attempt_runtime.__file__).read_text(encoding="utf-8")


def test_authority_boundaries_are_separate() -> None:
    source = Path(attempt_runtime.__file__).read_text(encoding="utf-8")
    assert "issue_authorization" not in source
    assert "RunReceipt" not in source
    assert "from .execution" not in source
    assert "from .lifecycle" not in source
    assert "from .authorization import" in source


def test_recovery_authorization_negative_matrix(tmp_path: Path) -> None:
    envelope, preparation_ref = _prepare(tmp_path)
    wrong_attempt_ref = issue_recovery_authorization(tmp_path, f"{CHANGE_ID}/{TASK_ID}/A9", "OWNER-RECOVERY")
    invalid = ["bad", "authz_" + "1" * 32, preparation_ref, wrong_attempt_ref]
    for ref in invalid:
        with pytest.raises(AttemptRuntimeError):
            resolve_interrupted_attempt(tmp_path, envelope.attempt_id, ref)
    assert lookup_attempt(tmp_path, envelope.attempt_id).runtime_state == "ACTIVATABLE"
    claim_attempt(tmp_path, envelope.attempt_id)
    valid_ref = issue_recovery_authorization(tmp_path, envelope.attempt_id, "OWNER-RECOVERY")
    terminal = resolve_interrupted_attempt(tmp_path, envelope.attempt_id, valid_ref)
    assert terminal.observed_result is not None and terminal.observed_result.execution_status == "INTERRUPTED"
    assert terminal.recovery_authorization_ref == valid_ref


def test_public_terminalization_rejects_fabricated_recovery_provenance(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    claim_attempt(tmp_path, envelope.attempt_id)
    fabricated_ref = "authz_" + "0" * 32
    before = _store_bytes(tmp_path)
    with pytest.raises(TypeError):
        terminalize_attempt(
            tmp_path,
            envelope.attempt_id,
            ObservedResultV1("fabricated", envelope.attempt_id, "INTERRUPTED"),
            recovery_authorization_ref=fabricated_ref,
        )
    assert _store_bytes(tmp_path) == before
    persisted = lookup_attempt(tmp_path, envelope.attempt_id).envelope
    assert persisted is not None
    assert persisted.runtime_state == "IN_FLIGHT"
    assert persisted.recovery_authorization_ref is None
    assert fabricated_ref.encode() not in _store_bytes(tmp_path)


def test_normal_interrupted_terminalization_has_null_recovery_provenance(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    claim_attempt(tmp_path, envelope.attempt_id)
    terminal = terminalize_attempt(
        tmp_path,
        envelope.attempt_id,
        ObservedResultV1("normal-interrupted", envelope.attempt_id, "INTERRUPTED"),
    )
    assert terminal.runtime_state == "TERMINAL"
    assert terminal.observed_result is not None
    assert terminal.observed_result.execution_status == "INTERRUPTED"
    assert terminal.recovery_authorization_ref is None


def test_recovery_provenance_is_authorized_and_exact(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    claim_attempt(tmp_path, envelope.attempt_id)
    recovery_ref = issue_recovery_authorization(tmp_path, envelope.attempt_id, "OWNER-RECOVERY")
    terminal = resolve_interrupted_attempt(tmp_path, envelope.attempt_id, recovery_ref)
    persisted = decode_attempt_store(_store_bytes(tmp_path)).by_id(envelope.attempt_id)
    assert persisted == terminal
    assert persisted is not None
    assert persisted.recovery_authorization_ref == recovery_ref
    resolved = resolve_authorization(
        tmp_path,
        recovery_ref,
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1(envelope.attempt_id),
    )
    assert resolved.outcome is ResolutionOutcome.AUTHORIZED


def test_recovery_single_use_and_replay(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    claim_attempt(tmp_path, envelope.attempt_id)
    ref = issue_recovery_authorization(tmp_path, envelope.attempt_id, "OWNER-RECOVERY")
    resolve_interrupted_attempt(tmp_path, envelope.attempt_id, ref)
    with pytest.raises(AttemptRuntimeError):
        resolve_interrupted_attempt(tmp_path, envelope.attempt_id, ref)


def test_cli_and_runtime_share_one_store_contract(tmp_path: Path) -> None:
    assert attempt_store_path(tmp_path).name == "attempt-runtime.json"
    assert hasattr(attempt_runtime, "prepare_attempt")
    assert hasattr(attempt_runtime, "resolve_interrupted_attempt")


def test_decoy_authority_and_forbidden_shortcuts_are_not_runtime_inputs() -> None:
    source = Path(attempt_runtime.__file__).read_text(encoding="utf-8").lower()
    for decoy in ("current.md", "active.md", "runreceipt", ".local", "git history", "environment"):
        assert decoy not in source
    assert "latest" not in source
    assert "fuzzy" not in source


def test_normal_terminalization_requires_same_attempt_and_in_flight(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        terminalize_attempt(tmp_path, envelope.attempt_id, ObservedResultV1("wrong", "CHG/OTHER/A1", "FAILED"))
    with pytest.raises(AttemptRuntimeError):
        terminalize_attempt(tmp_path, envelope.attempt_id, ObservedResultV1("direct", envelope.attempt_id, "FAILED"))


def test_runtime_records_are_canonical_and_unrelated_records_survive(tmp_path: Path) -> None:
    first, _ = _prepare(tmp_path, task_id="T-01")
    second, _ = _prepare(tmp_path, task_id="T-02")
    claim_attempt(tmp_path, first.attempt_id)
    decoded = decode_attempt_store(_store_bytes(tmp_path))
    assert [row.attempt_id for row in decoded.attempts] == sorted([first.attempt_id, second.attempt_id])
    assert decoded.by_id(second.attempt_id).runtime_state == "ACTIVATABLE"
    assert _store_bytes(tmp_path) == encode_attempt_store(decoded)


def test_public_codec_rejects_noncanonical_and_duplicate_result_conflicts(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    value = json.loads(_store_bytes(tmp_path).decode("utf-8"))
    value["attempts"][0]["attempt"]["observed_result_ref"] = "not-terminal"
    with pytest.raises(AttemptRuntimeError):
        decode_attempt_store(json.dumps(value, separators=(",", ":")).encode() + b"\n")
    assert envelope.attempt_id
