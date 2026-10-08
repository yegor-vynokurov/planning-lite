from __future__ import annotations

from dataclasses import replace
import hashlib
import json
import multiprocessing as mp
from pathlib import Path
import subprocess
import threading
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

import pytest

from planning_lite import attempt_runtime
from planning_lite import authorization as authorization_owner
from planning_lite.attempt_evaluation import (
    AttemptRecordV1,
    CandidateIdentityV1,
    IdentityRefV1,
    ObservedResultV1,
)
from planning_lite.attempt_runtime import (
    AdmissibilityOutcome,
    AttemptEnvelopeV2,
    AttemptRecordV2,
    AttemptAuthorizationError,
    AttemptRuntimeError,
    AttemptStateError,
    AttemptStoreV2,
    AttemptStoreV1,
    PreparationBindingV2,
    DependencyAdmissionOutcome,
    LookupOutcome,
    AttemptEnvelopeV1,
    attempt_store_path,
    check_activation_admissibility,
    claim_attempt,
    decode_attempt_store,
    encode_attempt_store,
    lookup_attempt,
    prepare_attempt,
    publish_dependency_acceptance_proof,
    materialize_dependency_admission_if_ready,
    invalidate_dependency_proof,
    resolve_interrupted_attempt,
    terminalize_attempt,
)
from planning_lite.authorization import (
    AuthorizationAction,
    AuthorizationRecordV1,
    DependencyProofInvalidationScopeV1,
    PreparationScopeV1,
    PreparationScopeV2,
    RecoveryScopeV1,
    ResolutionOutcome,
    authorization_store_path,
    decode_authorization_record,
    encode_authorization_record,
    issue_preparation_authorization,
    issue_recovery_authorization,
    resolve_authorization,
)
from planning_lite.dependency_admission import (
    CancellationCarrierError,
    CancellationTombstoneV1,
    DependencyProofCarrierError,
    cancellation_tombstone_path,
    cancellation_tombstone_ref,
    encode_cancellation_tombstone,
    resolve_dependency,
)
from planning_lite.attempt_runtime import attempt_store_v2_path, decode_attempt_store_v2, encode_attempt_store_v2

from test_dependency_admission import _task_rows as _dependency_task_rows
from test_dependency_admission import _write_fixture as _write_dependency_fixture
from test_dependency_admission import _capture_proof as _capture_dependency_proof


CHANGE_ID = "CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001"
TASK_ID = "T-03"
HEAD = "a" * 40
T05_CHANGE_ID = "CHG-TEST-DEPENDENCY-001"


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
    _ensure_runtime_governance(target, change_id=change_id)
    ref = issue_preparation_authorization(target, change_id, task_id, "OWNER-DECISION-PL09")
    return prepare_attempt(target, _payload(ref, change_id=change_id, task_id=task_id)), ref


def _ensure_runtime_governance(target: Path, *, change_id: str = CHANGE_ID) -> None:
    """Install the real resolver fixture once for this isolated Runtime target."""
    active = target / ".planning/ACTIVE.md"
    if active.exists():
        if f"- Change: `{change_id}`" not in active.read_text(encoding="utf-8"):
            raise AssertionError("Runtime fixture target already has another active Change")
        return
    _write_dependency_fixture(target, change_id=change_id)


def _store_bytes(target: Path) -> bytes:
    return attempt_store_v2_path(target).read_bytes()


def _seed_t05_source_attempt(target: Path, proof: object) -> AttemptEnvelopeV2:
    """Seed the exact completed producer row consumed by the T-05 owner tests."""
    proof_mapping = proof.to_mapping()
    requirement = resolve_dependency(target, "T-02").requirement
    source_id = f"{T05_CHANGE_ID}/T-01/A1"
    prep = PreparationBindingV2(
        "authz_" + "f" * 32,
        requirement["plan_ref"],
        requirement["tasks_ref"],
        resolve_dependency(target, "T-02").approved_plan_digest,
        requirement["dependency_semantic_digest"],
        requirement["requirement_id"],
        "DEPENDENCY_EDGE_MEMBER",
        source_id,
    )
    evaluation_input = proof_mapping["attempt_evaluation_input"]
    candidate_mapping = evaluation_input["candidate_identity"]
    candidate = CandidateIdentityV1(candidate_mapping["kind"], candidate_mapping["head"], ())
    baselines = tuple(IdentityRefV1(row["ref"], row["identity"]) for row in evaluation_input["baseline_refs"])
    verifiers = tuple(
        (row["contract_id"], row["contract_version_or_ref"])
        for row in evaluation_input["verifier_contract_refs"]
    )
    attempt = AttemptRecordV2(
        source_id,
        T05_CHANGE_ID,
        "T-01",
        1,
        prep.authorization_ref,
        proof_mapping["acceptance_contract_ref"],
        candidate,
        baselines,
        prep,
        verifier_contract_refs=verifiers,
    )
    result_mapping = proof_mapping["observed_result"]["value"]
    result = ObservedResultV1(
        result_mapping["result_id"],
        result_mapping["attempt_id"],
        result_mapping["execution_status"],
        tuple(result_mapping["changed_paths"]),
        tuple(result_mapping["fact_refs"]),
        tuple(result_mapping["artifact_refs"]),
    )
    attempt = replace(attempt, observed_result_ref=result.result_id)
    envelope = AttemptEnvelopeV2(attempt, "TERMINAL", result)
    store = attempt_store_v2_path(target)
    existing = decode_attempt_store_v2(store.read_bytes()) if store.exists() else AttemptStoreV2()
    store.write_bytes(encode_attempt_store_v2(AttemptStoreV2(tuple(sorted((*existing.attempts, envelope), key=lambda row: row.attempt_id)))))
    return envelope


def _t05_prepare_target(target: Path, *, prepare_successor: bool) -> tuple[object, str | None]:
    _write_dependency_fixture(target, change_id=T05_CHANGE_ID)
    auth_ref = issue_preparation_authorization(target, T05_CHANGE_ID, "T-02", "OWNER-DECISION-T05")
    if prepare_successor:
        prepare_attempt(target, _payload(auth_ref, change_id=T05_CHANGE_ID, task_id="T-02"))
    proof = _capture_dependency_proof(target)
    _seed_t05_source_attempt(target, proof)
    return proof, auth_ref


def _legacy_v1_envelope(
    *,
    change_id: str = "CHG-LEGACY-ATTEMPT-001",
    task_id: str = "T-03",
    authorization_ref: str = "authz_" + "f" * 32,
) -> AttemptEnvelopeV1:
    """Construct a genuine exact V1 row for read, conflict, and byte-preservation probes."""
    attempt = AttemptRecordV1(
        f"{change_id}/{task_id}/A1",
        change_id,
        task_id,
        1,
        authorization_ref,
        "AC-LEGACY",
        CandidateIdentityV1("GIT_COMMIT", HEAD, ()),
        (IdentityRefV1("HEAD", HEAD),),
    )
    return AttemptEnvelopeV1(attempt, "ACTIVATABLE")


def _copy_mapping(value: dict[str, object]) -> dict[str, object]:
    return json.loads(json.dumps(value))


def _cancellation_target(target: Path, *, cancelled_task: str | None) -> None:
    rows = _dependency_task_rows()
    if cancelled_task is not None:
        next(row for row in rows if row["id"] == cancelled_task)["status"] = "Cancelled"
    _write_dependency_fixture(target, task_rows=rows)


def _set_t05_task_status(target: Path, task_id: str, status: str) -> None:
    task_file = target / ".planning/changes/active" / T05_CHANGE_ID / "tasks.md"
    lines = task_file.read_text(encoding="utf-8").splitlines()
    prefix = f"| `{task_id}` |"
    indices = [index for index, line in enumerate(lines) if line.startswith(prefix)]
    assert len(indices) == 1
    row = lines[indices[0]]
    if "| `Pending` |" in row:
        lines[indices[0]] = row.replace("| `Pending` |", f"| `{status}` |", 1)
    elif "| `Cancelled` |" in row:
        lines[indices[0]] = row.replace("| `Cancelled` |", f"| `{status}` |", 1)
    else:
        raise AssertionError("fixture task status is not an expected exact value")
    task_file.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def _cancellation_artifacts(target: Path, change_id: str = "CHG-TEST-DEPENDENCY-001"):
    v1_store = attempt_store_path(target)
    v2_store = attempt_runtime.attempt_store_v2_path(target)
    auth_store = authorization_store_path(target)
    record = CancellationTombstoneV1(change_id)
    carrier_path = cancellation_tombstone_path(v2_store.parent, record)
    return v1_store, v2_store, auth_store, carrier_path


@pytest.mark.parametrize("cancelled_task", ["T-01", "T-02"])
def test_public_cancellation_observation_publishes_one_edge_tombstone_without_store(
    tmp_path: Path, cancelled_task: str
) -> None:
    change_id = "CHG-TEST-DEPENDENCY-001"
    _cancellation_target(tmp_path, cancelled_task=cancelled_task)
    v1_store, v2_store, auth_store, carrier_path = _cancellation_artifacts(tmp_path, change_id)

    first = attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, cancelled_task)
    other_task = "T-02" if cancelled_task == "T-01" else "T-01"
    second = attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, other_task)

    assert first.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    assert second.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    assert first.tombstone_ref == second.tombstone_ref == cancellation_tombstone_ref(CancellationTombstoneV1(change_id))
    assert first.observed_status == "Cancelled"
    assert carrier_path.read_bytes() == encode_cancellation_tombstone(CancellationTombstoneV1(change_id))
    assert (v2_store.parent / f"{v2_store.name}.lock").is_file()
    assert not v1_store.exists()
    assert not v2_store.exists()
    assert not auth_store.exists()
    assert sorted(path.name for path in carrier_path.parent.glob("*.json")) == [carrier_path.name]


def test_public_cancellation_observation_clear_then_status_edit_cannot_revive_edge(tmp_path: Path) -> None:
    change_id = "CHG-TEST-DEPENDENCY-001"
    _cancellation_target(tmp_path, cancelled_task=None)
    v1_store, v2_store, auth_store, carrier_path = _cancellation_artifacts(tmp_path, change_id)

    clear = attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, "T-02")
    assert clear.outcome is attempt_runtime.CancellationOutcome.CLEAR
    assert clear.tombstone_ref is None
    assert not carrier_path.exists()
    assert not v1_store.exists()
    assert not v2_store.exists()
    assert not auth_store.exists()

    task_file = tmp_path / ".planning" / "changes" / "active" / change_id / "tasks.md"
    task_file.write_text(
        task_file.read_text(encoding="utf-8").replace("| `T-01` | Produce governed artifact | `Tracer bullet` | `None` | focused producer test | source task | `Pending` |", "| `T-01` | Produce governed artifact | `Tracer bullet` | `None` | focused producer test | source task | `Cancelled` |"),
        encoding="utf-8",
        newline="\n",
    )
    before_digest = resolve_dependency(tmp_path, "T-02").dependency_semantic_digest
    blocked = attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, "T-01")
    assert blocked.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    assert blocked.tombstone_ref == cancellation_tombstone_ref(CancellationTombstoneV1(change_id))
    task_file.write_text(
        task_file.read_text(encoding="utf-8").replace("| `T-01` | Produce governed artifact | `Tracer bullet` | `None` | focused producer test | source task | `Cancelled` |", "| `T-01` | Produce governed artifact | `Tracer bullet` | `None` | focused producer test | source task | `Pending` |"),
        encoding="utf-8",
        newline="\n",
    )
    later = attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, "T-02")
    assert resolve_dependency(tmp_path, "T-02").dependency_semantic_digest == before_digest
    assert later.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    assert later.observed_status == "Pending"
    assert later.tombstone_ref == blocked.tombstone_ref
    assert not v1_store.exists()
    assert not v2_store.exists()
    assert not auth_store.exists()


def test_public_cancellation_observations_serialize_real_lock_contention(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    change_id = "CHG-TEST-DEPENDENCY-001"
    _cancellation_target(tmp_path, cancelled_task="T-01")
    v1_store, v2_store, auth_store, carrier_path = _cancellation_artifacts(tmp_path, change_id)
    first_published = threading.Event()
    release_first = threading.Event()
    second_contended = threading.Event()
    original_publish = attempt_runtime._publish_cancellation_tombstone_locked
    original_thread_lock_for = attempt_runtime._thread_lock_for
    shared_thread_lock = original_thread_lock_for(v2_store)

    def gate_first_publish(carrier_root: Path, record: CancellationTombstoneV1):
        result = original_publish(carrier_root, record)
        first_published.set()
        if not release_first.wait(10):
            raise AssertionError("test did not release first locked cancellation observation")
        return result

    @contextmanager
    def tracked_thread_lock(store: Path):
        if store != v2_store:
            raise AssertionError("cancellation observation used a different lock identity")
        if threading.current_thread().name == "cancel-second":
            if not shared_thread_lock.acquire(blocking=False):
                second_contended.set()
                shared_thread_lock.acquire()
            else:
                shared_thread_lock.release()
                shared_thread_lock.acquire()
        else:
            shared_thread_lock.acquire()
        try:
            yield
        finally:
            shared_thread_lock.release()

    monkeypatch.setattr(attempt_runtime, "_publish_cancellation_tombstone_locked", gate_first_publish)
    monkeypatch.setattr(attempt_runtime, "_thread_lock_for", lambda store: tracked_thread_lock(store))

    with ThreadPoolExecutor(max_workers=2, thread_name_prefix="cancel") as pool:
        first_future = pool.submit(attempt_runtime.observe_dependency_cancellation, tmp_path, change_id, "T-01")
        assert first_published.wait(10)

        def observe_as_second_contender():
            threading.current_thread().name = "cancel-second"
            return attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, "T-02")

        second_future = pool.submit(observe_as_second_contender)
        assert second_contended.wait(10)
        release_first.set()
        first = first_future.result(timeout=10)
        second = second_future.result(timeout=10)

    assert first.outcome is second.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    assert first.tombstone_ref == second.tombstone_ref == cancellation_tombstone_ref(CancellationTombstoneV1(change_id))
    assert carrier_path.read_bytes() == encode_cancellation_tombstone(CancellationTombstoneV1(change_id))
    assert sorted(path.name for path in carrier_path.parent.glob("*.json")) == [carrier_path.name]
    assert not v1_store.exists()
    assert not v2_store.exists()
    assert not auth_store.exists()


def test_public_cancellation_observation_fails_closed_on_publication_reread_and_conflict(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    change_id = "CHG-TEST-DEPENDENCY-001"
    _cancellation_target(tmp_path, cancelled_task="T-02")
    v1_store, v2_store, auth_store, carrier_path = _cancellation_artifacts(tmp_path, change_id)
    original_publish = attempt_runtime._publish_cancellation_tombstone_locked
    original_resolve = attempt_runtime.resolve_cancellation_tombstone

    def failed_publish(carrier_root: Path, record: CancellationTombstoneV1):
        raise CancellationCarrierError("injected publication failure")

    monkeypatch.setattr(attempt_runtime, "_publish_cancellation_tombstone_locked", failed_publish)
    with pytest.raises(AttemptRuntimeError):
        attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, "T-02")
    assert not carrier_path.exists()
    assert not v1_store.exists() and not v2_store.exists() and not auth_store.exists()

    monkeypatch.setattr(attempt_runtime, "_publish_cancellation_tombstone_locked", original_publish)
    reads = 0

    def failed_post_publish_reread(carrier_root: Path, record: CancellationTombstoneV1):
        nonlocal reads
        reads += 1
        if reads == 1:
            return None
        if reads == 2:
            raise CancellationCarrierError("injected durable reread failure")
        return original_resolve(carrier_root, record)

    monkeypatch.setattr(attempt_runtime, "resolve_cancellation_tombstone", failed_post_publish_reread)
    with pytest.raises(AttemptRuntimeError):
        attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, "T-02")
    assert carrier_path.read_bytes() == encode_cancellation_tombstone(CancellationTombstoneV1(change_id))
    assert not v1_store.exists() and not v2_store.exists() and not auth_store.exists()

    monkeypatch.setattr(attempt_runtime, "resolve_cancellation_tombstone", original_resolve)
    carrier_path.write_bytes(b"conflicting bytes that must stay immutable\n")
    with pytest.raises(AttemptRuntimeError):
        attempt_runtime.observe_dependency_cancellation(tmp_path, change_id, "T-01")
    assert carrier_path.read_bytes() == b"conflicting bytes that must stay immutable\n"
    assert not v1_store.exists() and not v2_store.exists() and not auth_store.exists()


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
    mutant_bytes = encode_attempt_store_v2(attempt_runtime.AttemptStoreV2((mutated_envelope,)))
    decoded_mutant = decode_attempt_store_v2(mutant_bytes)
    assert encode_attempt_store_v2(decoded_mutant) == mutant_bytes

    binding = envelope.attempt.preparation_binding
    original_scope = PreparationScopeV2(
        envelope.attempt.change_id,
        envelope.attempt.task_or_operation_id,
        binding.plan_ref,
        binding.tasks_ref,
        binding.approved_plan_digest,
        binding.dependency_semantic_digest,
        binding.requirement_id,
        binding.dependency_classification,
        binding.expected_attempt_id,
    )

    original_resolution = resolve_authorization(
        target,
        authorization_ref,
        AuthorizationAction.PREPARATION,
        original_scope,
    )
    assert original_resolution.outcome is ResolutionOutcome.AUTHORIZED
    assert original_resolution.record is not None
    assert original_resolution.record.authorization_ref == authorization_ref
    assert original_resolution.record.scope == original_scope
    foreign_resolution = resolve_authorization(
        target,
        authorization_ref,
        AuthorizationAction.PREPARATION,
        replace(
            original_scope,
            change_id=mutated_attempt.change_id,
            task_or_operation_id=mutated_attempt.task_or_operation_id,
        ),
    )
    assert foreign_resolution.outcome is ResolutionOutcome.WRONG_SCOPE

    attempt_store_v2_path(target).write_bytes(mutant_bytes)
    before_claim = _store_bytes(target)
    with pytest.raises(AttemptAuthorizationError):
        claim_attempt(target, mutated_attempt.attempt_id)

    assert _store_bytes(target) == before_claim
    persisted = decode_attempt_store_v2(before_claim).by_id(mutated_attempt.attempt_id)
    assert persisted is not None
    assert persisted.runtime_state == "ACTIVATABLE"
    assert persisted.attempt == mutated_attempt


def test_p05_foreign_change_canonical_persisted_attempt_cannot_be_claimed(tmp_path: Path) -> None:
    _assert_canonical_scope_mutant_rejected(
        tmp_path,
        original_change_id="CHG-P05-ORIGINAL",
        original_task_id="T-03",
        foreign_change_id="CHG-P05-FOREIGN",
    )


def test_p05_foreign_task_canonical_persisted_attempt_cannot_be_claimed(tmp_path: Path) -> None:
    _assert_canonical_scope_mutant_rejected(
        tmp_path,
        original_task_id="T-03",
        foreign_task_id="T-04",
    )


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


_T07_EXECUTION_RESULT = (
    "docs/design/project-spine/checkpoints/"
    "PL-V39-09G-DEPENDENCY-ADMISSION-T07-EXECUTION-RESULT-v1.md"
)
_T07_EXECUTION_OWNER_ADJUDICATION = (
    "docs/design/project-spine/checkpoints/"
    "PL-V39-09G-DEPENDENCY-ADMISSION-T07-EXECUTION-OWNER-ADJUDICATION-v1.md"
)
_T07_FINAL_OWNER_ACCEPTANCE = (
    "docs/design/project-spine/checkpoints/"
    "PL-V39-09G-DEPENDENCY-ADMISSION-T07-FINAL-OWNER-ACCEPTANCE-v1.md"
)
_T07_PRODUCT_TEST_PATHS = frozenset(
    {
        "src/planning_lite/attempt_runtime.py",
        "src/planning_lite/authorization.py",
        "src/planning_lite/dependency_admission.py",
        "src/planning_lite/governed_executor.py",
        "src/planning_lite/operation_lifecycle.py",
        "src/planning_lite/workspace.py",
        "tests/test_attempt_runtime.py",
        "tests/test_authorization.py",
        "tests/test_dependency_admission.py",
        "tests/test_governed_executor.py",
        "tests/test_operation_lifecycle.py",
        "tests/test_workspace_registry.py",
    }
)
_T07_GOVERNANCE_PATHS = frozenset(
    {
        "docs/design/project-spine/CURRENT.md",
        _T07_EXECUTION_RESULT,
    }
)


def _read_exact_markdown_table(text: str, header: str, width: int) -> list[tuple[str, ...]]:
    lines = text.splitlines()
    header_index = next(index for index, line in enumerate(lines) if line.strip() == header)
    rows: list[tuple[str, ...]] = []
    for line in lines[header_index + 2 :]:
        if not line.strip().startswith("|"):
            break
        row = tuple(cell.strip().strip("`") for cell in line.strip().strip("|").split("|"))
        assert len(row) == width
        rows.append(row)
    return rows


def _read_exact_text_field(text: str, field: str) -> str:
    prefix = f"{field}: "
    values = [line.removeprefix(prefix) for line in text.splitlines() if line.startswith(prefix)]
    assert len(values) == 1
    return values[0]


def _assert_exact_historical_write_boundary(
    observed_paths: set[str], authorized_paths: set[str]
) -> None:
    unauthorized = observed_paths - authorized_paths
    assert not unauthorized, f"unauthorized historical paths: {sorted(unauthorized)}"
    missing = authorized_paths - observed_paths
    assert not missing, f"missing historical paths: {sorted(missing)}"


def _committed_evidence_bytes(root: Path, relative_path: str) -> bytes:
    """Read an evidence artifact from HEAD's Git blob, independent of checkout EOL."""
    blob = subprocess.run(
        ["git", "rev-parse", "--verify", f"HEAD:{relative_path}"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return subprocess.run(
        ["git", "cat-file", "blob", blob],
        cwd=root,
        capture_output=True,
        check=True,
    ).stdout


def _assert_committed_evidence_sha256(
    root: Path, relative_path: str, expected_sha256: str
) -> bytes:
    """Fail closed when committed historical evidence differs from its accepted digest."""
    evidence = _committed_evidence_bytes(root, relative_path)
    actual_sha256 = hashlib.sha256(evidence).hexdigest()
    assert actual_sha256 == expected_sha256.lower(), (
        f"committed evidence SHA-256 mismatch for {relative_path}: {actual_sha256}"
    )
    return evidence


def _t07_historical_path_hash_facts(root: Path) -> dict[str, tuple[str | None, str | None]]:
    result_raw = _committed_evidence_bytes(root, _T07_EXECUTION_RESULT)
    first_adjudication_raw = _committed_evidence_bytes(
        root, _T07_EXECUTION_OWNER_ADJUDICATION
    )
    acceptance_raw = _committed_evidence_bytes(root, _T07_FINAL_OWNER_ACCEPTANCE)
    result_sha256 = hashlib.sha256(result_raw).hexdigest()
    first_adjudication_sha256 = hashlib.sha256(first_adjudication_raw).hexdigest()
    acceptance_sha256 = hashlib.sha256(acceptance_raw).hexdigest()
    assert result_sha256 == "49ae76475801852707a86458c4b3d028a95fb7ceaf77e4d740a964f47ab1f01b"
    assert first_adjudication_sha256 == "8934793d2639d76d83edc812b6e867d808723f195e408520ad6d4d0ebb44c79b"
    assert acceptance_sha256 == "59d542fd4e5d3e7cc218c9bf058a78c5a5ffb746df11c5ac139ecb4b60d4bbec"

    result_text = result_raw.decode("utf-8")
    first_adjudication_text = first_adjudication_raw.decode("utf-8")
    acceptance_text = acceptance_raw.decode("utf-8")
    assert _read_exact_text_field(result_text, "unrelated_entry_dirty_bytes_changed") == "0"
    assert (
        _read_exact_text_field(first_adjudication_text, "T07_execution_result_raw_sha256_before_adjudication")
        == result_sha256
    )
    assert (
        f"PL-V39-09G-DEPENDENCY-ADMISSION-T07-EXECUTION-OWNER-ADJUDICATION-v1.md` / raw SHA-256 `"
        f"{first_adjudication_sha256}`"
    ) in acceptance_text
    assert (
        f"PL-V39-09G-DEPENDENCY-ADMISSION-T07-EXECUTION-RESULT-v1.md` / raw SHA-256 `"
        f"{result_sha256}`"
    ) in acceptance_text

    entry_exit_rows = _read_exact_markdown_table(
        result_text,
        "| Authorized path | Entry raw SHA-256 | Result raw SHA-256 |",
        3,
    )
    accepted_rows = _read_exact_markdown_table(
        acceptance_text,
        "| Exact T-07 candidate path | Recomputed raw SHA-256 | Match |",
        3,
    )
    assert len(entry_exit_rows) == 12
    assert len(accepted_rows) == 12
    assert {row[0] for row in entry_exit_rows} == _T07_PRODUCT_TEST_PATHS
    assert {row[0] for row in accepted_rows} == _T07_PRODUCT_TEST_PATHS
    accepted_hashes = {path: digest for path, digest, match in accepted_rows if match == "PASS"}
    assert len(accepted_hashes) == 12

    facts: dict[str, tuple[str | None, str | None]] = {}
    for path, before_sha256, after_sha256 in entry_exit_rows:
        assert len(before_sha256) == 64 and len(after_sha256) == 64
        assert accepted_hashes[path] == after_sha256
        facts[path] = (before_sha256, after_sha256)

    current_path = "docs/design/project-spine/CURRENT.md"
    current_before = _read_exact_text_field(result_text, "entry_CURRENT_sha256")
    current_after = _read_exact_text_field(
        first_adjudication_text, "CURRENT_at_adjudication_entry_raw_sha256"
    )
    assert len(current_before) == 64 and len(current_after) == 64
    facts[current_path] = (current_before, current_after)
    facts[_T07_EXECUTION_RESULT] = (None, result_sha256)
    assert set(facts) == _T07_PRODUCT_TEST_PATHS | _T07_GOVERNANCE_PATHS
    return facts


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
        _assert_committed_evidence_sha256(
            root,
            f"docs/design/project-spine/checkpoints/{name}",
            digest,
        )
    t07_result_path = root / _T07_EXECUTION_RESULT
    t07_acceptance_path = root / _T07_FINAL_OWNER_ACCEPTANCE
    if t07_result_path.is_file() or t07_acceptance_path.is_file():
        assert t07_result_path.is_file() and t07_acceptance_path.is_file()
        t07_facts = _t07_historical_path_hash_facts(root)
        _assert_exact_historical_write_boundary(
            set(t07_facts), _T07_PRODUCT_TEST_PATHS | _T07_GOVERNANCE_PATHS
        )
        assert subprocess.run(
            ["git", "diff", "--cached", "--name-only"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip() == ""
        return

    # Compare the actual execution delta with the newest captured gate entry
    # state; prior accepted governance files are not mistaken for T-06 edits.
    t06_scratch = root / ".local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T06_EXECUTION"
    t06_manifest_path = t06_scratch / "entry-manifest.json"
    t05_scratch = root / ".local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T05_EXECUTION"
    t05_manifest_path = t05_scratch / "entry-manifest.json"
    t03_scratch = root / ".local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T03_EXECUTION"
    manifest_path = (
        t06_manifest_path
        if t06_manifest_path.is_file()
        else t05_manifest_path if t05_manifest_path.is_file() else t03_scratch / "entry-manifest.json"
    )
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        baseline = manifest.get("file_hashes", manifest.get("all_nonignored_files", {}))
        if not baseline and "tracked_nonignored_entry_manifest" in manifest:
            baseline = {
                item["path"]: item["sha256"]
                for item in manifest["tracked_nonignored_entry_manifest"]
                if item.get("kind") == "file"
            }
        changed = {
            name
            for name, digest in baseline.items()
            if not (root / name).is_file() or hashlib.sha256((root / name).read_bytes()).hexdigest() != digest
        }
        untracked = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        changed.update(name for name in untracked if name not in baseline)
        if manifest_path == t06_manifest_path:
            allowed = {
                "src/planning_lite/attempt_runtime.py",
                "src/planning_lite/dependency_admission.py",
                "tests/test_attempt_runtime.py",
                "tests/test_dependency_admission.py",
                "docs/design/project-spine/CURRENT.md",
                "docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-T06-EXECUTION-RESULT-v1.md",
            }
        elif manifest_path == t05_manifest_path:
            allowed = {
                "src/planning_lite/attempt_runtime.py",
                "src/planning_lite/dependency_admission.py",
                "tests/test_attempt_runtime.py",
                "tests/test_dependency_admission.py",
                "docs/design/project-spine/CURRENT.md",
                "docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-T05-EXECUTION-RESULT-v1.md",
            }
        else:
            allowed = {
                "src/planning_lite/attempt_runtime.py",
                "tests/test_attempt_runtime.py",
                "tests/test_system_traversability.py",
                "tests/test_cli.py",
                "docs/design/project-spine/CURRENT.md",
                "docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-T03-EXECUTION-RESULT-v1.md",
            }
        assert changed <= allowed
        assert set(baseline) >= {
            "src/planning_lite/authorization.py",
            "src/planning_lite/dependency_admission.py",
            "src/planning_lite/cli.py",
            "src/planning_lite/operation_lifecycle.py",
        }
        protected_paths = (
            "src/planning_lite/authorization.py",
            "src/planning_lite/dependency_admission.py",
            "src/planning_lite/cli.py",
            "src/planning_lite/operation_lifecycle.py",
            "src/planning_lite/governed_executor.py",
            "src/planning_lite/attempt_evaluation.py",
            "src/planning_lite/workspace.py",
        )
        if manifest_path in {t05_manifest_path, t06_manifest_path}:
            protected_paths = tuple(path for path in protected_paths if path != "src/planning_lite/dependency_admission.py")
        for protected in protected_paths:
            assert hashlib.sha256((root / protected).read_bytes()).hexdigest() == baseline[protected]
        if manifest_path == t05_manifest_path:
            refs = subprocess.run(
                ["git", "show-ref"], cwd=root, capture_output=True, check=True
            ).stdout
            assert hashlib.sha256(refs).hexdigest() == manifest["refs_sha256"]
        elif manifest_path == t06_manifest_path:
            refs = subprocess.run(["git", "show-ref"], cwd=root, capture_output=True, check=True).stdout
            assert hashlib.sha256(refs).hexdigest() == manifest["refs_sha256_raw_show_ref"]
        else:
            refs = subprocess.run(
                ["git", "for-each-ref", "--format=%(refname) %(objectname)"],
                cwd=root,
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()
            assert hashlib.sha256(refs.encode()).hexdigest() == manifest["refs_sha256"]
        recorded_index_sha = manifest.get(
            "raw_index_sha256", manifest.get("index_sha256", manifest.get("index_sha256_raw"))
        )
        if recorded_index_sha is not None:
            entry_index_sha = recorded_index_sha
        assert hashlib.sha256((root / ".git/index").read_bytes()).hexdigest() == entry_index_sha
    else:
        # A clean checkout has no execution manifest; its current unstaged
        # delta still must remain within the same explicit T-03 surface.
        changed = subprocess.run(
            ["git", "diff", "--name-only", "HEAD"],
            cwd=root,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.splitlines()
        assert set(changed) <= {
            "src/planning_lite/attempt_runtime.py",
            "tests/test_attempt_runtime.py",
            "tests/test_system_traversability.py",
            "tests/test_cli.py",
            "docs/design/project-spine/CURRENT.md",
        }
    assert subprocess.run(["git", "diff", "--cached", "--name-only"], cwd=root, capture_output=True, text=True, check=True).stdout.strip() == ""


def test_committed_evidence_digest_ignores_checkout_eol_and_rejects_mutation(
    tmp_path: Path,
) -> None:
    """Pin Git source bytes across CRLF checkouts and reject a changed evidence blob."""
    root = tmp_path / "evidence-source"
    root.mkdir()
    subprocess.run(["git", "init"], cwd=root, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "planning-lite-test@example.invalid"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Planning Lite Test"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "core.autocrlf", "false"],
        cwd=root,
        check=True,
        capture_output=True,
    )

    relative_path = "evidence.md"
    evidence_path = root / relative_path
    accepted_bytes = b"# accepted evidence\n\nimmutable source bytes\n"
    evidence_path.write_bytes(accepted_bytes)
    subprocess.run(["git", "add", relative_path], cwd=root, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "accepted evidence"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    expected_sha256 = hashlib.sha256(accepted_bytes).hexdigest()

    crlf_checkout = accepted_bytes.replace(b"\n", b"\r\n")
    evidence_path.write_bytes(crlf_checkout)
    assert hashlib.sha256(evidence_path.read_bytes()).hexdigest() != expected_sha256
    assert _assert_committed_evidence_sha256(root, relative_path, expected_sha256) == accepted_bytes

    mutated_bytes = b"# changed evidence\n\nnot the accepted source\n"
    evidence_path.write_bytes(mutated_bytes)
    subprocess.run(["git", "add", relative_path], cwd=root, check=True, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "mutated evidence"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    with pytest.raises(AssertionError, match="committed evidence SHA-256 mismatch"):
        _assert_committed_evidence_sha256(root, relative_path, expected_sha256)


def test_t07_historical_write_boundary_rejects_unauthorized_path() -> None:
    root = Path(__file__).resolve().parents[1]
    facts = _t07_historical_path_hash_facts(root)
    with pytest.raises(AssertionError):
        _assert_exact_historical_write_boundary(
            set(facts) | {"tests/test_unauthorized_historical_path.py"}, set(facts)
        )


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


def test_attempt_store_v2_golden_bytes_and_exact_nested_schemas(tmp_path: Path) -> None:
    """Pin exact V2 keys, resolver binding copy, null joins and canonical wire bytes."""
    _ensure_runtime_governance(tmp_path)
    reference = issue_preparation_authorization(tmp_path, CHANGE_ID, TASK_ID, "OWNER-DECISION")
    envelope = prepare_attempt(
        tmp_path,
        {**_payload(reference), "operation_guidance_ref": "guidance:café"},
    )
    raw = _store_bytes(tmp_path)
    decoded = decode_attempt_store_v2(raw)
    mapping = decoded.to_mapping()
    stored = decoded.by_id(envelope.attempt_id)
    assert stored is not None
    assert set(mapping) == {"schema_version", "attempts"}
    assert mapping["schema_version"] == 2
    assert set(mapping["attempts"][0]) == {
        "attempt",
        "runtime_state",
        "observed_result",
        "recovery_authorization_ref",
        "dependency_edge_control",
    }
    attempt = mapping["attempts"][0]["attempt"]
    assert set(attempt) == {
        "schema_version",
        "attempt_id",
        "change_id",
        "task_or_operation_id",
        "attempt_ordinal",
        "authorization_ref",
        "acceptance_contract_ref",
        "operation_guidance_ref",
        "candidate_identity",
        "baseline_refs",
        "prompt_composition_ref",
        "parent_attempt_ref",
        "addresses_finding_refs",
        "observed_result_ref",
        "verifier_contract_refs",
        "preparation_binding",
        "dependency_admission",
    }
    binding = attempt["preparation_binding"]
    assert set(binding) == {
        "authorization_ref",
        "plan_ref",
        "tasks_ref",
        "approved_plan_digest",
        "dependency_semantic_digest",
        "requirement_id",
        "dependency_classification",
        "expected_attempt_id",
    }
    assert len(attempt) == 17 and len(binding) == 8
    assert binding["authorization_ref"] == reference == stored.authorization_ref
    candidate_scope = resolve_authorization(
        tmp_path,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(CHANGE_ID, TASK_ID),
    ).record.scope
    assert resolve_authorization(
        tmp_path,
        reference,
        AuthorizationAction.PREPARATION,
        candidate_scope,
    ).outcome is ResolutionOutcome.AUTHORIZED
    assert binding == {
        "authorization_ref": reference,
        "plan_ref": candidate_scope.plan_ref,
        "tasks_ref": candidate_scope.tasks_ref,
        "approved_plan_digest": candidate_scope.approved_plan_digest,
        "dependency_semantic_digest": candidate_scope.dependency_semantic_digest,
        "requirement_id": candidate_scope.requirement_id,
        "dependency_classification": candidate_scope.dependency_classification,
        "expected_attempt_id": candidate_scope.expected_attempt_id,
    }
    assert binding["dependency_classification"] == "NOT_APPLICABLE"
    assert binding["expected_attempt_id"] is None
    assert attempt["dependency_admission"] is None
    assert mapping["attempts"][0]["dependency_edge_control"] is None
    assert mapping["attempts"][0]["observed_result"] is None
    assert mapping["attempts"][0]["recovery_authorization_ref"] is None
    assert mapping["attempts"][0]["runtime_state"] == "ACTIVATABLE"
    expected_wire = json.dumps(
        mapping,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8") + b"\n"
    assert raw == expected_wire
    assert "café".encode("utf-8") in raw and b"caf\\u00e9" not in raw
    assert raw.endswith(b"\n") and not raw.endswith(b"\n\n") and not raw.startswith(b"\xef\xbb\xbf")


def test_attempt_store_v2_strict_codec_rejects_schema_and_canonical_mutants(tmp_path: Path) -> None:
    """Reject exact-schema, primitive-type, duplicate-member, and byte-canonicality mutants."""
    envelope, _ = _prepare(tmp_path)
    raw = _store_bytes(tmp_path)
    mapping = json.loads(raw.decode("utf-8"))

    mutants: list[dict[str, object]] = []
    for location, key in (
        (mapping, "attempts"),
        (mapping["attempts"][0], "dependency_edge_control"),
        (mapping["attempts"][0]["attempt"], "preparation_binding"),
        (mapping["attempts"][0]["attempt"]["preparation_binding"], "plan_ref"),
    ):
        missing = _copy_mapping(mapping)
        target = missing
        if location is not mapping:
            if key == "dependency_edge_control":
                target = missing["attempts"][0]
            elif key == "preparation_binding":
                target = missing["attempts"][0]["attempt"]
            else:
                target = missing["attempts"][0]["attempt"]["preparation_binding"]
        target.pop(key)
        mutants.append(missing)
    extra = _copy_mapping(mapping)
    extra["unexpected"] = None
    mutants.append(extra)
    extra_binding = _copy_mapping(mapping)
    extra_binding["attempts"][0]["attempt"]["preparation_binding"]["caller_choice"] = "ignored?"
    mutants.append(extra_binding)
    bool_store = _copy_mapping(mapping)
    bool_store["schema_version"] = True
    mutants.append(bool_store)
    bool_attempt = _copy_mapping(mapping)
    bool_attempt["attempts"][0]["attempt"]["schema_version"] = True
    mutants.append(bool_attempt)
    bool_ordinal = _copy_mapping(mapping)
    bool_ordinal["attempts"][0]["attempt"]["attempt_ordinal"] = True
    mutants.append(bool_ordinal)
    bad_digest = _copy_mapping(mapping)
    bad_digest["attempts"][0]["attempt"]["preparation_binding"]["approved_plan_digest"] = "A" * 64
    mutants.append(bad_digest)
    bad_ref = _copy_mapping(mapping)
    bad_ref["attempts"][0]["attempt"]["authorization_ref"] = "authz_" + "A" * 32
    mutants.append(bad_ref)
    bad_identity = _copy_mapping(mapping)
    bad_identity["attempts"][0]["attempt"]["attempt_id"] = "bad/A1"
    mutants.append(bad_identity)
    partial_admission = _copy_mapping(mapping)
    partial_admission["attempts"][0]["attempt"]["dependency_admission"] = {
        "schema_version": 2,
        "admission_id": "dadm_" + "0" * 64,
    }
    mutants.append(partial_admission)
    for mutant in mutants:
        with pytest.raises(AttemptRuntimeError):
            encode_attempt_store_v2(mutant)

    duplicate = raw.replace(b'"attempt_id":', b'"attempt_id":"duplicate","attempt_id":', 1)
    reordered = _copy_mapping(mapping)
    attempt_mapping = reordered["attempts"][0]["attempt"]
    moved = attempt_mapping.pop("attempt_id")
    attempt_mapping["attempt_id"] = moved
    noncanonical_order = json.dumps(reordered, ensure_ascii=False, separators=(",", ":")).encode("utf-8") + b"\n"
    malformed = (
        raw[:-1],
        raw + b"\n",
        b"\xef\xbb\xbf" + raw,
        b"\xff" + raw,
        duplicate,
        noncanonical_order,
        json.dumps(mapping, ensure_ascii=False, sort_keys=True).encode("utf-8") + b"\n",
        raw.replace(b'"runtime_state":"ACTIVATABLE"', b'"runtime_state":NaN'),
    )
    for candidate in malformed:
        with pytest.raises(AttemptRuntimeError):
            decode_attempt_store_v2(candidate)
    with pytest.raises(AttemptRuntimeError):
        attempt_runtime._canonical_v2_json({"not_finite": float("nan")})
    assert lookup_attempt(tmp_path, envelope.attempt_id).outcome is LookupOutcome.FOUND


def test_v2_sorted_unique_rows_and_cross_store_conflicts_fail_closed(tmp_path: Path) -> None:
    """Enforce sorted V2 identity/ref uniqueness and corrupt cross-store joins without mutation."""
    first, first_ref = _prepare(tmp_path, task_id="T-03")
    second_ref = issue_preparation_authorization(tmp_path, CHANGE_ID, "T-04", "OWNER-DECISION-2")
    second = prepare_attempt(tmp_path, _payload(second_ref, task_id="T-04"))
    store = decode_attempt_store_v2(_store_bytes(tmp_path))
    assert [row.attempt_id for row in store.attempts] == sorted([first.attempt_id, second.attempt_id])
    with pytest.raises(AttemptRuntimeError):
        attempt_runtime.AttemptStoreV2((store.attempts[0], store.attempts[0]))

    unsorted = store.to_mapping()
    unsorted["attempts"].reverse()
    with pytest.raises(AttemptRuntimeError):
        encode_attempt_store_v2(unsorted)

    duplicate_binding = replace(store.attempts[1].attempt.preparation_binding, authorization_ref=first_ref)
    duplicate_ref = replace(
        store.attempts[1].attempt,
        authorization_ref=first_ref,
        preparation_binding=duplicate_binding,
    )
    duplicate_envelope = replace(store.attempts[1], attempt=duplicate_ref)
    with pytest.raises(AttemptRuntimeError):
        attempt_runtime.AttemptStoreV2((store.attempts[0], duplicate_envelope))

    v1_same_id = _legacy_v1_envelope(
        change_id=first.attempt.change_id,
        task_id=first.attempt.task_or_operation_id,
        authorization_ref="authz_" + "e" * 32,
    )
    v1_path = attempt_store_path(tmp_path)
    v1_bytes = encode_attempt_store(AttemptStoreV1((v1_same_id,)))
    v1_path.parent.mkdir(parents=True, exist_ok=True)
    v1_path.write_bytes(v1_bytes)
    assert lookup_attempt(tmp_path, first.attempt_id).outcome is LookupOutcome.CORRUPT_CONFLICT
    assert v1_path.read_bytes() == v1_bytes

    cross_ref = _legacy_v1_envelope(
        change_id="CHG-LEGACY-DIFFERENT-ID",
        task_id="T-04",
        authorization_ref=first_ref,
    )
    cross_ref_bytes = encode_attempt_store(AttemptStoreV1((cross_ref,)))
    v1_path.write_bytes(cross_ref_bytes)
    assert lookup_attempt(tmp_path, first.attempt_id).outcome is LookupOutcome.CORRUPT_CONFLICT
    assert v1_path.read_bytes() == cross_ref_bytes


def test_v1_bytes_remain_identical_when_v2_is_added_and_id_conflict_blocks_publication(tmp_path: Path) -> None:
    """Preserve a real V1 document byte-for-byte and reject a cross-store A1 collision before V2 write."""
    _ensure_runtime_governance(tmp_path)
    legacy = _legacy_v1_envelope()
    v1_path = attempt_store_path(tmp_path)
    v1_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_bytes = encode_attempt_store(AttemptStoreV1((legacy,)))
    v1_path.write_bytes(legacy_bytes)
    reference = issue_preparation_authorization(tmp_path, CHANGE_ID, "T-03", "OWNER-DECISION")
    new = prepare_attempt(tmp_path, _payload(reference, task_id="T-03"))
    assert decode_attempt_store(legacy_bytes).by_id(legacy.attempt_id) == legacy
    assert v1_path.read_bytes() == legacy_bytes
    assert lookup_attempt(tmp_path, legacy.attempt_id).outcome is LookupOutcome.FOUND
    assert lookup_attempt(tmp_path, new.attempt_id).outcome is LookupOutcome.FOUND
    claim_attempt(tmp_path, new.attempt_id)
    terminalize_attempt(tmp_path, new.attempt_id, ObservedResultV1("v2-result", new.attempt_id, "COMPLETED"))
    assert v1_path.read_bytes() == legacy_bytes

    conflict_target = tmp_path / "conflict"
    _ensure_runtime_governance(conflict_target)
    conflict_ref = issue_preparation_authorization(conflict_target, CHANGE_ID, "T-02", "OWNER-DECISION")
    occupying = _legacy_v1_envelope(change_id=CHANGE_ID, task_id="T-02")
    conflict_v1 = attempt_store_path(conflict_target)
    conflict_v1.parent.mkdir(parents=True, exist_ok=True)
    conflict_bytes = encode_attempt_store(AttemptStoreV1((occupying,)))
    conflict_v1.write_bytes(conflict_bytes)
    with pytest.raises(AttemptAuthorizationError):
        prepare_attempt(conflict_target, _payload(conflict_ref, task_id="T-02"))
    assert conflict_v1.read_bytes() == conflict_bytes
    assert not attempt_store_v2_path(conflict_target).exists()


def test_edge_materialization_is_exact_a1_and_dependent_claim_stays_blocked(tmp_path: Path) -> None:
    """Copy T-02/A1 authority exactly, reject caller bindings, and keep claim owned by T-06."""
    _ensure_runtime_governance(tmp_path)
    reference = issue_preparation_authorization(tmp_path, CHANGE_ID, "T-02", "OWNER-DECISION-T02")
    payload = _payload(reference, task_id="T-02")
    payload["preparation_binding"] = {"dependency_classification": "NOT_APPLICABLE"}
    payload["dependency_admission"] = {"eligible_outcome": "ELIGIBLE_FOR_CLAIM_CHECK"}
    payload["attempt_id"] = f"{CHANGE_ID}/T-02/A7"
    envelope = prepare_attempt(tmp_path, payload)
    assert envelope.attempt_id == f"{CHANGE_ID}/T-02/A1"
    assert envelope.attempt.attempt_ordinal == 1
    assert envelope.attempt.parent_attempt_ref is None
    binding = envelope.attempt.preparation_binding
    assert binding.dependency_classification == "DEPENDENCY_EDGE_MEMBER"
    assert binding.expected_attempt_id == envelope.attempt_id
    assert envelope.attempt.dependency_admission is None
    assert envelope.dependency_edge_control is None
    before = _store_bytes(tmp_path)
    assert check_activation_admissibility(tmp_path, envelope.attempt_id).outcome is AdmissibilityOutcome.INVALID_RECORD
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, envelope.attempt_id)
    assert _store_bytes(tmp_path) == before
    with pytest.raises(AttemptRuntimeError):
        prepare_attempt(tmp_path, {**_payload(reference, task_id="T-02"), "parent_attempt_ref": "parent"})
    with pytest.raises(AttemptRuntimeError):
        prepare_attempt(tmp_path, _payload(reference, change_id="CHG-CALLER-SPOOF", task_id="T-02"))

    a2_mapping = json.loads(before.decode("utf-8"))
    a2_record = a2_mapping["attempts"][0]["attempt"]
    a2_record["attempt_ordinal"] = 2
    a2_record["attempt_id"] = f"{CHANGE_ID}/T-02/A2"
    with pytest.raises(AttemptRuntimeError):
        encode_attempt_store_v2(a2_mapping)
    incomplete_admission = json.loads(before.decode("utf-8"))
    incomplete_admission["attempts"][0]["attempt"]["dependency_admission"] = {
        "admission_id": "dadm_" + "0" * 64,
        "schema_version": 2,
    }
    with pytest.raises(AttemptRuntimeError):
        encode_attempt_store_v2(incomplete_admission)


def test_source_edge_member_claim_uses_own_authority_without_successor_evidence(
    tmp_path: Path,
) -> None:
    """Public T-01 claim needs its own current Preparation, not T-02 D11 facts."""
    _ensure_runtime_governance(tmp_path, change_id=T05_CHANGE_ID)
    source_auth = issue_preparation_authorization(
        tmp_path, T05_CHANGE_ID, "T-01", "OWNER-DECISION-T07-SOURCE"
    )
    successor_auth = issue_preparation_authorization(
        tmp_path, T05_CHANGE_ID, "T-02", "OWNER-DECISION-T07-SIBLING"
    )
    source = prepare_attempt(
        tmp_path, _payload(source_auth, change_id=T05_CHANGE_ID, task_id="T-01")
    )
    assert source.attempt_id == f"{T05_CHANGE_ID}/T-01/A1"
    assert source.attempt.dependency_admission is None
    assert source.dependency_edge_control is None

    claimed = claim_attempt(tmp_path, source.attempt_id)
    assert isinstance(claimed, AttemptEnvelopeV2)
    assert claimed.runtime_state == "IN_FLIGHT"
    assert claimed.authorization_ref == source_auth
    assert claimed.attempt.preparation_binding.expected_attempt_id == source.attempt_id
    assert claimed.attempt.dependency_admission is None
    assert claimed.dependency_edge_control is None
    # The pre-issued sibling remains present and unused; source claim did not
    # need proof, admission, route bytes, or PL08 evidence.
    sibling_record = decode_authorization_record(
        (authorization_store_path(tmp_path) / f"{successor_auth}.json").read_bytes()
    )
    assert resolve_authorization(
        tmp_path,
        successor_auth,
        AuthorizationAction.PREPARATION,
        sibling_record.scope,
    ).outcome is ResolutionOutcome.AUTHORIZED
    route = attempt_runtime.resolve_dependency_artifact_output_route(tmp_path)
    assert not route.path.exists()


def test_source_edge_member_claim_rejects_sibling_t02_authority(tmp_path: Path) -> None:
    """A stored T-01 row cannot switch to the pre-issued T-02 scope."""
    _ensure_runtime_governance(tmp_path, change_id=T05_CHANGE_ID)
    source_auth = issue_preparation_authorization(
        tmp_path, T05_CHANGE_ID, "T-01", "OWNER-DECISION-T07-SOURCE"
    )
    successor_auth = issue_preparation_authorization(
        tmp_path, T05_CHANGE_ID, "T-02", "OWNER-DECISION-T07-SIBLING"
    )
    source = prepare_attempt(
        tmp_path, _payload(source_auth, change_id=T05_CHANGE_ID, task_id="T-01")
    )
    path = attempt_store_v2_path(tmp_path)
    before = decode_attempt_store_v2(path.read_bytes())
    row = before.by_id(source.attempt_id)
    assert row is not None
    forged_attempt = replace(
        row.attempt,
        authorization_ref=successor_auth,
        preparation_binding=replace(row.attempt.preparation_binding, authorization_ref=successor_auth),
    )
    forged = replace(row, attempt=forged_attempt)
    path.write_bytes(encode_attempt_store_v2(AttemptStoreV2((forged,))))
    forged_bytes = path.read_bytes()
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, source.attempt_id)
    assert path.read_bytes() == forged_bytes


def test_legacy_v1_dependent_attempt_without_binding_stays_unclaimable(tmp_path: Path) -> None:
    """Keep genuine V1 bytes readable while requiring live independent applicability to claim."""
    _ensure_runtime_governance(tmp_path)
    reference = "authz_" + "d" * 32
    legacy_authorization = AuthorizationRecordV1(
        1,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(CHANGE_ID, "T-02"),
        authorization_owner.PREPARATION_AUTHORITY,
        "AUTHORIZED",
        "OWNER-LEGACY-PREPARATION",
    )
    auth_store = authorization_store_path(tmp_path)
    auth_store.mkdir(parents=True, exist_ok=True)
    (auth_store / f"{reference}.json").write_bytes(encode_authorization_record(legacy_authorization))
    legacy = _legacy_v1_envelope(change_id=CHANGE_ID, task_id="T-02", authorization_ref=reference)
    raw = encode_attempt_store(AttemptStoreV1((legacy,)))
    v1_path = attempt_store_path(tmp_path)
    v1_path.parent.mkdir(parents=True, exist_ok=True)
    v1_path.write_bytes(raw)
    assert lookup_attempt(tmp_path, legacy.attempt_id).outcome is LookupOutcome.FOUND
    assert lookup_attempt(tmp_path, legacy.attempt_id).attempt.to_mapping().get("preparation_binding") is None
    with pytest.raises(AttemptAuthorizationError):
        claim_attempt(tmp_path, legacy.attempt_id)
    assert v1_path.read_bytes() == raw
    assert not attempt_store_v2_path(tmp_path).exists()


def test_v2_lookup_is_read_only_and_reports_corrupt_or_duplicate_stores(tmp_path: Path) -> None:
    """Lookup dispatches exact V1/V2 rows without creating either store or masking corruption."""
    missing_id = "CHG-NOT-HERE/T-03/A1"
    assert lookup_attempt(tmp_path, missing_id).outcome is LookupOutcome.NOT_FOUND
    assert not attempt_store_path(tmp_path).exists()
    assert not attempt_store_v2_path(tmp_path).exists()
    assert not (tmp_path / ".local").exists()

    v1 = _legacy_v1_envelope()
    v1_path = attempt_store_path(tmp_path)
    v1_path.parent.mkdir(parents=True, exist_ok=True)
    v1_raw = encode_attempt_store(AttemptStoreV1((v1,)))
    v1_path.write_bytes(v1_raw)
    assert lookup_attempt(tmp_path, v1.attempt_id).outcome is LookupOutcome.FOUND
    assert v1_path.read_bytes() == v1_raw

    v2_target = tmp_path / "v2"
    row, _ = _prepare(v2_target)
    v2_store = attempt_store_v2_path(v2_target)
    v2_bytes = v2_store.read_bytes()
    assert lookup_attempt(v2_target, row.attempt_id).outcome is LookupOutcome.FOUND
    assert v2_store.read_bytes() == v2_bytes
    v2_store.write_bytes(b"corrupt V2\n")
    assert lookup_attempt(v2_target, row.attempt_id).outcome is LookupOutcome.CORRUPT_CONFLICT


def test_v2_post_write_reread_is_authoritative_and_failed_pre_replace_keeps_bytes(tmp_path: Path) -> None:
    """Exercise V2 pre-commit preservation and strict authoritative reread under the shared seam."""
    envelope, _ = _prepare(tmp_path)
    before = _store_bytes(tmp_path)
    for phase in ("prepare", "validate", "replace"):
        with pytest.raises(AttemptRuntimeError):
            claim_attempt(
                tmp_path,
                envelope.attempt_id,
                fault_hook=lambda current, phase=phase: (_ for _ in ()).throw(RuntimeError(phase)) if current == phase else None,
            )
        assert _store_bytes(tmp_path) == before

    path = attempt_store_v2_path(tmp_path)

    def corrupt_after_replace(phase: str) -> None:
        if phase == "verify":
            path.write_bytes(b"not the intended canonical document\n")

    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, envelope.attempt_id, fault_hook=corrupt_after_replace)
    assert lookup_attempt(tmp_path, envelope.attempt_id).outcome is LookupOutcome.CORRUPT_CONFLICT


def test_v2_terminal_result_mapping_uses_strict_integer_schema(tmp_path: Path) -> None:
    """Reject bool-as-version in a newly persisted V2 terminal result without changing state."""
    envelope, _ = _prepare(tmp_path)
    claim_attempt(tmp_path, envelope.attempt_id)
    before = _store_bytes(tmp_path)
    invalid = ObservedResultV1("strict-result", envelope.attempt_id, "FAILED").to_mapping()
    invalid["schema_version"] = True
    with pytest.raises(AttemptRuntimeError):
        terminalize_attempt(tmp_path, envelope.attempt_id, invalid)
    assert _store_bytes(tmp_path) == before
    valid = ObservedResultV1("strict-result", envelope.attempt_id, "FAILED").to_mapping()
    terminal = terminalize_attempt(tmp_path, envelope.attempt_id, valid)
    assert terminal.runtime_state == "TERMINAL"
    assert terminal.observed_result == ObservedResultV1("strict-result", envelope.attempt_id, "FAILED")


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
    _ensure_runtime_governance(tmp_path)
    good = issue_preparation_authorization(tmp_path, CHANGE_ID, TASK_ID, "OWNER-DECISION")
    wrong_task = issue_preparation_authorization(tmp_path, CHANGE_ID, "T-04", "OWNER-DECISION")
    recovery = issue_recovery_authorization(tmp_path, f"{CHANGE_ID}/{TASK_ID}/A1", "OWNER-DECISION")
    candidates = ["bad", "authz_" + "0" * 32, wrong_task, recovery]
    for ref in candidates:
        with pytest.raises(AttemptRuntimeError):
            prepare_attempt(tmp_path, _payload(ref))
    assert not attempt_store_path(tmp_path).exists()
    # The valid record remains available after all rejected references.
    envelope = prepare_attempt(tmp_path, _payload(good))
    assert envelope.runtime_state == "ACTIVATABLE"


def test_preparation_single_use_and_failed_attempt_non_consumption(tmp_path: Path) -> None:
    _ensure_runtime_governance(tmp_path)
    ref = issue_preparation_authorization(tmp_path, CHANGE_ID, TASK_ID, "OWNER-DECISION")
    auth_before = (authorization_store_path(tmp_path) / f"{ref}.json").read_bytes()
    first = prepare_attempt(tmp_path, _payload(ref))
    with pytest.raises(AttemptRuntimeError):
        prepare_attempt(tmp_path, _payload(ref))
    assert len(decode_attempt_store_v2(_store_bytes(tmp_path)).attempts) == 1
    assert (authorization_store_path(tmp_path) / f"{ref}.json").read_bytes() == auth_before

    second_ref = issue_preparation_authorization(tmp_path, CHANGE_ID, "T-04", "OWNER-DECISION")
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        prepare_attempt(tmp_path, {**_payload(second_ref, task_id="T-04"), "candidate_identity": {"bad": True}})
    assert _store_bytes(tmp_path) == before
    second = prepare_attempt(tmp_path, _payload(second_ref, task_id="T-04"))
    assert second.attempt_id.endswith("/T-04/A1")
    assert first.attempt_id.endswith(f"/{TASK_ID}/A1")


def test_identity_lineage_and_ordinal_allocation(tmp_path: Path) -> None:
    first, _ = _prepare(tmp_path)
    # A second same-scope authorization must allocate the next contiguous ID.
    ref = issue_preparation_authorization(tmp_path, CHANGE_ID, TASK_ID, "OWNER-DECISION-2")
    second = prepare_attempt(tmp_path, _payload(ref))
    assert first.attempt_id.endswith("/A1")
    assert second.attempt_id.endswith("/A2")
    assert [row.attempt.attempt_ordinal for row in decode_attempt_store_v2(_store_bytes(tmp_path)).attempts] == [1, 2]
    foreign_target = tmp_path / "foreign"
    _ensure_runtime_governance(foreign_target, change_id="CHG-FOREIGN")
    foreign = issue_preparation_authorization(foreign_target, "CHG-FOREIGN", TASK_ID, "OWNER-DECISION")
    foreign_envelope = prepare_attempt(foreign_target, _payload(foreign, change_id="CHG-FOREIGN"))
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
    assert hashlib.sha256(_store_bytes(tmp_path)).hexdigest() == hashlib.sha256(attempt_store_v2_path(tmp_path).read_bytes()).hexdigest()
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
    persisted = decode_attempt_store_v2(_store_bytes(tmp_path)).by_id(envelope.attempt_id)
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
    assert attempt_store_v2_path(tmp_path).name == "attempt-runtime-v2.json"
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
    first, _ = _prepare(tmp_path, task_id="T-03")
    second, _ = _prepare(tmp_path, task_id="T-04")
    claim_attempt(tmp_path, first.attempt_id)
    decoded = decode_attempt_store_v2(_store_bytes(tmp_path))
    assert [row.attempt_id for row in decoded.attempts] == sorted([first.attempt_id, second.attempt_id])
    assert decoded.by_id(second.attempt_id).runtime_state == "ACTIVATABLE"
    assert _store_bytes(tmp_path) == encode_attempt_store_v2(decoded)


def test_public_codec_rejects_noncanonical_and_duplicate_result_conflicts(tmp_path: Path) -> None:
    envelope, _ = _prepare(tmp_path)
    value = json.loads(_store_bytes(tmp_path).decode("utf-8"))
    value["attempts"][0]["attempt"]["observed_result_ref"] = "not-terminal"
    with pytest.raises(AttemptRuntimeError):
        decode_attempt_store_v2(json.dumps(value, separators=(",", ":")).encode() + b"\n")
    assert envelope.attempt_id


def _issue_t05_invalidation_authorization(target: Path, proof: object) -> tuple[str, Path, bytes]:
    mapping = proof.to_mapping()
    decision_id = "ADR-0042"
    decision_path = target / ".planning/decisions/ADR-0042-invalidate-dependency-proof.md"
    decision_path.parent.mkdir(parents=True, exist_ok=True)
    block = {
        "schema_version": 1,
        "decision_id": decision_id,
        "decision_kind": "DEPENDENCY_PROOF_INVALIDATION",
        "decision_status": "APPROVED",
        "change_id": T05_CHANGE_ID,
        "source_attempt_id": f"{T05_CHANGE_ID}/T-01/A1",
        "successor_attempt_id": f"{T05_CHANGE_ID}/T-02/A1",
        "proof_id": mapping["proof_id"],
        "decision_outcome": "INVALIDATE_EXACT_DEPENDENCY_PROOF",
    }
    block_json = json.dumps(block, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":"))
    raw = (
        f"# {decision_id}: Invalidate exact dependency proof\n\n"
        "- Status: `Accepted`\n\n"
        "```dependency-proof-invalidation-decision-v1\n"
        f"{block_json}\n```\n"
    ).encode("utf-8")
    decision_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    provenance = f"decision:.planning/decisions/{decision_path.name}@sha256:{digest}"
    scope = DependencyProofInvalidationScopeV1(
        T05_CHANGE_ID,
        f"{T05_CHANGE_ID}/T-01/A1",
        f"{T05_CHANGE_ID}/T-02/A1",
        mapping["proof_id"],
    )
    reference = authorization_owner.issue_authorization(
        target,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
        provenance,
    )
    return reference, decision_path, raw


def test_t05_two_triggers_converge_under_one_v2_lock_and_admission_is_idempotent(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    first = tmp_path / "trigger-a"
    first.mkdir()
    proof_a, _ = _t05_prepare_target(first, prepare_successor=True)
    real_lock = attempt_runtime._store_lock
    lock_calls = 0

    @contextmanager
    def counted_lock(store: Path, *, create: bool):
        nonlocal lock_calls
        lock_calls += 1
        with real_lock(store, create=create):
            yield

    monkeypatch.setattr(attempt_runtime, "_store_lock", counted_lock)
    result_a = publish_dependency_acceptance_proof(first, proof_a)
    assert lock_calls == 1
    assert result_a.outcome is DependencyAdmissionOutcome.MATERIALIZED
    stored_a = decode_attempt_store_v2(_store_bytes(first))
    admission_a = stored_a.by_id(f"{T05_CHANGE_ID}/T-02/A1").attempt.dependency_admission
    assert admission_a is not None and len(admission_a) == 22
    assert admission_a["admission_id"] == result_a.admission_id
    again = materialize_dependency_admission_if_ready(first, trigger="A")
    assert again.outcome is DependencyAdmissionOutcome.ALREADY_MATERIALIZED
    assert again.admission_id == result_a.admission_id

    second = tmp_path / "trigger-b"
    second.mkdir()
    proof_b, auth_b = _t05_prepare_target(second, prepare_successor=False)
    deferred = publish_dependency_acceptance_proof(second, proof_b)
    assert deferred.outcome is DependencyAdmissionOutcome.DEFERRED_SUCCESSOR_NOT_PREPARED
    assert deferred.to_mapping()["attempt_id"] is None and deferred.admission_id is None
    materialized = prepare_attempt(second, _payload(auth_b, change_id=T05_CHANGE_ID, task_id="T-02"))
    assert materialized.attempt.dependency_admission is not None
    assert materialized.attempt.dependency_admission["admission_id"] == result_a.admission_id


def test_t05_existing_current_head_cannot_be_reinstalled_or_replaced(tmp_path: Path) -> None:
    identical = tmp_path / "identical-current"
    identical.mkdir()
    proof, _ = _t05_prepare_target(identical, prepare_successor=True)
    installed = publish_dependency_acceptance_proof(identical, proof)
    assert installed.outcome is DependencyAdmissionOutcome.MATERIALIZED
    before = _store_bytes(identical)
    # V10 permits only NO_CURRENT_PROOF_HEAD -> CURRENT, so even the same
    # immutable proof cannot reinstall or rewrite an already-current head.
    with pytest.raises(AttemptStateError):
        publish_dependency_acceptance_proof(identical, proof)
    assert _store_bytes(identical) == before

    conflict = tmp_path / "conflicting-current"
    conflict.mkdir()
    conflict_proof, _ = _t05_prepare_target(conflict, prepare_successor=True)
    store = attempt_store_v2_path(conflict)
    current = decode_attempt_store_v2(_store_bytes(conflict))
    source_id = f"{T05_CHANGE_ID}/T-01/A1"
    source = current.by_id(source_id)
    assert source is not None
    requirement = resolve_dependency(conflict, "T-02").requirement
    conflicting_digest = "a" * 64
    control = {
        "schema_version": 1,
        "change_id": T05_CHANGE_ID,
        "source_task_or_operation_id": "T-01",
        "source_attempt_id": source_id,
        "successor_task_or_operation_id": "T-02",
        "successor_attempt_id": f"{T05_CHANGE_ID}/T-02/A1",
        "dependency_semantic_digest": requirement["dependency_semantic_digest"],
        "proof_head": {
            "schema_version": 1,
            "state": "CURRENT",
            "proof_id": f"dproof_{conflicting_digest}",
            "proof_digest": conflicting_digest,
            "invalidation_authorization_ref": None,
        },
        "cancellation_tombstone_ref": None,
    }
    conflict_source = replace(source, dependency_edge_control=control)
    seeded = AttemptStoreV2(tuple(sorted(
        (conflict_source if row.attempt_id == source_id else row for row in current.attempts),
        key=lambda row: row.attempt_id,
    )))
    with attempt_runtime._store_lock(store, create=False):
        attempt_runtime._safe_replace(store, seeded, attempt_id=source_id)
    before_conflict = _store_bytes(conflict)
    with pytest.raises(AttemptStateError):
        publish_dependency_acceptance_proof(conflict, conflict_proof)
    assert _store_bytes(conflict) == before_conflict


def test_t05_cancellation_before_proof_leaves_only_tombstone_and_inert_blob(tmp_path: Path) -> None:
    proof, _ = _t05_prepare_target(tmp_path, prepare_successor=True)
    _set_t05_task_status(tmp_path, "T-01", "Cancelled")
    with pytest.raises(AttemptStateError):
        publish_dependency_acceptance_proof(tmp_path, proof)
    store = attempt_store_v2_path(tmp_path)
    decoded = decode_attempt_store_v2(store.read_bytes())
    source = decoded.by_id(f"{T05_CHANGE_ID}/T-01/A1")
    successor = decoded.by_id(f"{T05_CHANGE_ID}/T-02/A1")
    assert source is not None and source.dependency_edge_control is None
    assert successor is not None and successor.attempt.dependency_admission is None
    proof_blob = store.parent / "dependency-admission" / "proofs" / f"{proof.proof_digest}.json"
    tombstone = cancellation_tombstone_path(store.parent, CancellationTombstoneV1(T05_CHANGE_ID))
    assert proof_blob.is_file() and tombstone.is_file()


def test_t05_cancellation_after_current_preserves_head_and_existing_admission(tmp_path: Path) -> None:
    proof, _ = _t05_prepare_target(tmp_path, prepare_successor=True)
    installed = publish_dependency_acceptance_proof(tmp_path, proof)
    assert installed.outcome is DependencyAdmissionOutcome.MATERIALIZED
    before = decode_attempt_store_v2(_store_bytes(tmp_path)).by_id(f"{T05_CHANGE_ID}/T-02/A1")
    assert before is not None
    admission_before = before.attempt.dependency_admission
    _set_t05_task_status(tmp_path, "T-02", "Cancelled")
    observation = attempt_runtime.observe_dependency_cancellation(tmp_path, T05_CHANGE_ID, "T-02")
    assert observation.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    after_store = decode_attempt_store_v2(_store_bytes(tmp_path))
    source = after_store.by_id(f"{T05_CHANGE_ID}/T-01/A1")
    successor = after_store.by_id(f"{T05_CHANGE_ID}/T-02/A1")
    assert source is not None and source.dependency_edge_control is not None
    assert source.dependency_edge_control["proof_head"]["state"] == "CURRENT"
    assert source.dependency_edge_control["cancellation_tombstone_ref"] == observation.tombstone_ref
    assert successor is not None and successor.attempt.dependency_admission == admission_before


def test_t05_invalidation_rechecks_exact_adr_and_blocks_trigger_b(tmp_path: Path) -> None:
    proof, auth = _t05_prepare_target(tmp_path, prepare_successor=False)
    deferred = publish_dependency_acceptance_proof(tmp_path, proof)
    assert deferred.outcome is DependencyAdmissionOutcome.DEFERRED_SUCCESSOR_NOT_PREPARED
    invalidation_ref, decision_path, decision_bytes = _issue_t05_invalidation_authorization(tmp_path, proof)
    before = _store_bytes(tmp_path)
    with pytest.raises(TypeError):
        invalidate_dependency_proof(tmp_path, invalidation_ref, caller_assertion=True)  # type: ignore[call-arg]
    assert _store_bytes(tmp_path) == before

    decision_path.write_bytes(decision_bytes + b" ")
    with pytest.raises(AttemptRuntimeError):
        invalidate_dependency_proof(tmp_path, invalidation_ref)
    assert _store_bytes(tmp_path) == before
    decision_path.write_bytes(decision_bytes)
    invalidated = invalidate_dependency_proof(tmp_path, invalidation_ref)
    assert invalidated.dependency_edge_control["proof_head"]["state"] == "INVALIDATED"
    assert invalidated.dependency_edge_control["proof_head"]["invalidation_authorization_ref"] == invalidation_ref
    attempt_runtime.resolve_dependency_artifact_output_route(tmp_path).path.write_bytes(
        b"artifact changed after owner invalidation"
    )

    successor = prepare_attempt(tmp_path, _payload(auth, change_id=T05_CHANGE_ID, task_id="T-02"))
    assert successor.attempt.dependency_admission is None
    blocked = materialize_dependency_admission_if_ready(tmp_path, trigger="B")
    assert blocked.outcome is DependencyAdmissionOutcome.BLOCKED_PROOF_INVALIDATED
    assert blocked.attempt_id == f"{T05_CHANGE_ID}/T-02/A1" and blocked.admission_id is None
    store_after_invalidation = _store_bytes(tmp_path)
    with pytest.raises(AttemptStateError):
        publish_dependency_acceptance_proof(tmp_path, proof)
    assert _store_bytes(tmp_path) == store_after_invalidation


def test_t05_malformed_tombstone_and_pre_replace_fault_leave_current_absent(
    tmp_path: Path,
) -> None:
    malformed = tmp_path / "malformed-tombstone"
    malformed.mkdir()
    malformed_proof, _ = _t05_prepare_target(malformed, prepare_successor=True)
    malformed_store = attempt_store_v2_path(malformed)
    malformed_record = CancellationTombstoneV1(T05_CHANGE_ID)
    malformed_path = cancellation_tombstone_path(malformed_store.parent, malformed_record)
    malformed_path.parent.mkdir(parents=True, exist_ok=True)
    malformed_path.write_bytes(b"conflicting tombstone bytes\n")
    malformed_before = _store_bytes(malformed)
    with pytest.raises(AttemptRuntimeError):
        publish_dependency_acceptance_proof(malformed, malformed_proof)
    assert _store_bytes(malformed) == malformed_before
    malformed_source = decode_attempt_store_v2(malformed_before).by_id(f"{T05_CHANGE_ID}/T-01/A1")
    assert malformed_source is not None and malformed_source.dependency_edge_control is None

    faulted = tmp_path / "pre-replace-fault"
    faulted.mkdir()
    fault_proof, _ = _t05_prepare_target(faulted, prepare_successor=True)
    fault_store = attempt_store_v2_path(faulted)
    fault_before = _store_bytes(faulted)

    def fail_before_replace(phase: str) -> None:
        if phase == "replace":
            raise RuntimeError("injected T-05 pre-replace failure")

    with pytest.raises(AttemptRuntimeError):
        publish_dependency_acceptance_proof(faulted, fault_proof, fault_hook=fail_before_replace)
    assert _store_bytes(faulted) == fault_before
    fault_source = decode_attempt_store_v2(fault_before).by_id(f"{T05_CHANGE_ID}/T-01/A1")
    assert fault_source is not None and fault_source.dependency_edge_control is None
    fault_blob = fault_store.parent / "dependency-admission" / "proofs" / f"{fault_proof.proof_digest}.json"
    assert fault_blob.is_file()


@pytest.mark.parametrize("mutant", ["source_state", "source_result"])
def test_t05_proof_current_rejects_source_state_and_result_mismatches(
    tmp_path: Path, mutant: str
) -> None:
    target = tmp_path / mutant
    target.mkdir()
    proof, _ = _t05_prepare_target(target, prepare_successor=True)
    store = attempt_store_v2_path(target)
    before = decode_attempt_store_v2(_store_bytes(target))
    source_id = f"{T05_CHANGE_ID}/T-01/A1"
    source = before.by_id(source_id)
    assert source is not None and source.observed_result is not None
    if mutant == "source_state":
        changed_source = replace(
            source,
            observed_result=replace(source.observed_result, execution_status="FAILED"),
        )
    else:
        changed_source = replace(
            source,
            observed_result=replace(source.observed_result, fact_refs=(*source.observed_result.fact_refs, "changed-proof-result")),
        )
    changed = AttemptStoreV2(tuple(sorted(
        (changed_source if row.attempt_id == source_id else row for row in before.attempts),
        key=lambda row: row.attempt_id,
    )))
    store.write_bytes(encode_attempt_store_v2(changed))
    changed_bytes = _store_bytes(target)
    with pytest.raises(AttemptRuntimeError):
        publish_dependency_acceptance_proof(target, proof)
    assert _store_bytes(target) == changed_bytes
    persisted = decode_attempt_store_v2(changed_bytes).by_id(source_id)
    assert persisted is not None and persisted.dependency_edge_control is None


def test_t05_deferred_stale_cancellation_and_conflicting_admission_outcomes(tmp_path: Path) -> None:
    assert {item.value for item in DependencyAdmissionOutcome} == {
        "MATERIALIZED", "ALREADY_MATERIALIZED", "DEFERRED_SUCCESSOR_NOT_PREPARED",
        "DEFERRED_PREDECESSOR_PROOF_NOT_CURRENT", "BLOCKED_PROOF_INVALIDATED",
        "BLOCKED_CANCELLATION", "BLOCKED_STALE_DEPENDENCY", "BLOCK_CONFLICTING_ADMISSION",
    }

    missing_successor = tmp_path / "missing-successor"
    missing_successor.mkdir()
    proof, _ = _t05_prepare_target(missing_successor, prepare_successor=False)
    assert publish_dependency_acceptance_proof(missing_successor, proof).outcome is DependencyAdmissionOutcome.DEFERRED_SUCCESSOR_NOT_PREPARED
    # A T-02 Preparation created before source proof remains deferred on B.
    waiting = tmp_path / "waiting-successor"
    waiting.mkdir()
    _write_dependency_fixture(waiting, change_id=T05_CHANGE_ID)
    waiting_auth = issue_preparation_authorization(waiting, T05_CHANGE_ID, "T-02", "OWNER-DECISION-T05")
    prepare_attempt(waiting, _payload(waiting_auth, change_id=T05_CHANGE_ID, task_id="T-02"))
    deferred = materialize_dependency_admission_if_ready(waiting, trigger="B")
    assert deferred.outcome is DependencyAdmissionOutcome.DEFERRED_PREDECESSOR_PROOF_NOT_CURRENT
    assert deferred.attempt_id == f"{T05_CHANGE_ID}/T-02/A1" and deferred.admission_id is None

    stale = tmp_path / "stale-binding"
    stale.mkdir()
    _write_dependency_fixture(stale, change_id=T05_CHANGE_ID)
    stale_auth = issue_preparation_authorization(stale, T05_CHANGE_ID, "T-02", "OWNER-DECISION-T05")
    prepare_attempt(stale, _payload(stale_auth, change_id=T05_CHANGE_ID, task_id="T-02"))
    store = attempt_store_v2_path(stale)
    mapping = json.loads(store.read_bytes())
    mapping["attempts"][0]["attempt"]["preparation_binding"]["dependency_semantic_digest"] = "0" * 64
    store.write_bytes(encode_attempt_store_v2(mapping))
    stale_result = materialize_dependency_admission_if_ready(stale, trigger="B")
    assert stale_result.outcome is DependencyAdmissionOutcome.BLOCKED_STALE_DEPENDENCY
    assert stale_result.admission_id is None

    cancelled = tmp_path / "cancelled-edge"
    cancelled.mkdir()
    cancel_proof, cancel_auth = _t05_prepare_target(cancelled, prepare_successor=False)
    assert publish_dependency_acceptance_proof(cancelled, cancel_proof).outcome is DependencyAdmissionOutcome.DEFERRED_SUCCESSOR_NOT_PREPARED
    _set_t05_task_status(cancelled, "T-02", "Cancelled")
    prepared = prepare_attempt(cancelled, _payload(cancel_auth, change_id=T05_CHANGE_ID, task_id="T-02"))
    assert prepared.attempt.dependency_admission is None
    before_block = _store_bytes(cancelled)
    attempt_runtime.resolve_dependency_artifact_output_route(cancelled).path.write_bytes(
        b"artifact changed after cancellation"
    )
    cancellation = materialize_dependency_admission_if_ready(cancelled, trigger="B")
    assert cancellation.outcome is DependencyAdmissionOutcome.BLOCKED_CANCELLATION
    assert cancellation.attempt_id == f"{T05_CHANGE_ID}/T-02/A1" and cancellation.admission_id is None
    assert _store_bytes(cancelled) == before_block

    conflict_root = tmp_path / "conflict"
    conflict_root.mkdir()
    conflict_proof, _ = _t05_prepare_target(conflict_root, prepare_successor=True)
    materialized = publish_dependency_acceptance_proof(conflict_root, conflict_proof)
    assert materialized.outcome is DependencyAdmissionOutcome.MATERIALIZED
    conflict_mapping = json.loads(_store_bytes(conflict_root))
    successor = next(row for row in conflict_mapping["attempts"] if row["attempt"]["task_or_operation_id"] == "T-02")
    conflicting = successor["attempt"]["dependency_admission"]
    conflicting["artifact_digest"] = "f" * 64
    semantic = dict(conflicting)
    semantic.pop("admission_id")
    conflicting["admission_id"] = "dadm_" + hashlib.sha256(
        json.dumps(semantic, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    conflict_bytes = encode_attempt_store_v2(conflict_mapping)
    attempt_store_v2_path(conflict_root).write_bytes(conflict_bytes)
    conflict_result = materialize_dependency_admission_if_ready(conflict_root, trigger="A")
    assert conflict_result.outcome is DependencyAdmissionOutcome.BLOCK_CONFLICTING_ADMISSION
    assert conflict_result.admission_id is None
    assert _store_bytes(conflict_root) == conflict_bytes


def test_t05_cancellation_vs_current_uses_real_lock_and_event_ordering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof, _ = _t05_prepare_target(tmp_path, prepare_successor=True)
    _set_t05_task_status(tmp_path, "T-01", "Cancelled")
    store = attempt_store_v2_path(tmp_path)
    tombstone_published = threading.Event()
    proof_waiting_for_lock = threading.Event()
    release_cancellation = threading.Event()
    original_publish = attempt_runtime._publish_cancellation_tombstone_locked
    original_thread_lock_for = attempt_runtime._thread_lock_for
    shared_lock = original_thread_lock_for(store)

    def hold_after_tombstone(carrier_root: Path, record: CancellationTombstoneV1):
        result = original_publish(carrier_root, record)
        tombstone_published.set()
        if not release_cancellation.wait(10):
            raise AssertionError("test did not release cancellation-first V2 lock")
        return result

    @contextmanager
    def observe_real_contention(lock_store: Path):
        if threading.current_thread().name == "t05-proof-after-cancel":
            proof_waiting_for_lock.set()
        with shared_lock:
            yield

    monkeypatch.setattr(attempt_runtime, "_publish_cancellation_tombstone_locked", hold_after_tombstone)
    monkeypatch.setattr(attempt_runtime, "_thread_lock_for", lambda _store: observe_real_contention(_store))
    with ThreadPoolExecutor(max_workers=2) as pool:
        def cancel_first():
            threading.current_thread().name = "t05-cancel-first"
            return attempt_runtime.observe_dependency_cancellation(tmp_path, T05_CHANGE_ID, "T-01")

        def publish_after_cancel():
            threading.current_thread().name = "t05-proof-after-cancel"
            return publish_dependency_acceptance_proof(tmp_path, proof)

        cancel_future = pool.submit(cancel_first)
        assert tombstone_published.wait(10)
        proof_future = pool.submit(publish_after_cancel)
        assert proof_waiting_for_lock.wait(10)
        release_cancellation.set()
        cancellation = cancel_future.result(timeout=10)
        with pytest.raises(AttemptStateError):
            proof_future.result(timeout=10)

    assert cancellation.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    decoded = decode_attempt_store_v2(_store_bytes(tmp_path))
    source = decoded.by_id(f"{T05_CHANGE_ID}/T-01/A1")
    successor = decoded.by_id(f"{T05_CHANGE_ID}/T-02/A1")
    assert source is not None and source.dependency_edge_control is None
    assert successor is not None and successor.attempt.dependency_admission is None
    proof_blob = store.parent / "dependency-admission" / "proofs" / f"{proof.proof_digest}.json"
    tombstone = cancellation_tombstone_path(store.parent, CancellationTombstoneV1(T05_CHANGE_ID))
    assert proof_blob.is_file() and tombstone.is_file()


def test_t05_current_vs_cancellation_keeps_current_and_admission_with_real_contention(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof, _ = _t05_prepare_target(tmp_path, prepare_successor=True)
    store = attempt_store_v2_path(tmp_path)
    admission_written = threading.Event()
    cancellation_waiting_for_lock = threading.Event()
    release_admission = threading.Event()
    original_thread_lock_for = attempt_runtime._thread_lock_for
    shared_lock = original_thread_lock_for(store)
    hash_calls = 0

    @contextmanager
    def observe_real_contention(lock_store: Path):
        if threading.current_thread().name == "t05-cancel-after-current":
            cancellation_waiting_for_lock.set()
        with shared_lock:
            yield

    def gate_admission_write(phase: str) -> None:
        nonlocal hash_calls
        if phase == "hash":
            hash_calls += 1
            if hash_calls == 2:
                admission_written.set()
                if not release_admission.wait(10):
                    raise AssertionError("test did not release admission-first V2 lock")

    monkeypatch.setattr(attempt_runtime, "_thread_lock_for", lambda _store: observe_real_contention(_store))
    with ThreadPoolExecutor(max_workers=2) as pool:
        def publish_first():
            threading.current_thread().name = "t05-proof-first"
            return publish_dependency_acceptance_proof(tmp_path, proof, fault_hook=gate_admission_write)

        def cancel_after_current():
            threading.current_thread().name = "t05-cancel-after-current"
            return attempt_runtime.observe_dependency_cancellation(tmp_path, T05_CHANGE_ID, "T-02")

        proof_future = pool.submit(publish_first)
        assert admission_written.wait(10)
        cancellation_future = pool.submit(cancel_after_current)
        assert cancellation_waiting_for_lock.wait(10)
        _set_t05_task_status(tmp_path, "T-02", "Cancelled")
        release_admission.set()
        proof_result = proof_future.result(timeout=10)
        cancellation = cancellation_future.result(timeout=10)

    assert proof_result.outcome is DependencyAdmissionOutcome.MATERIALIZED
    assert cancellation.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    decoded = decode_attempt_store_v2(_store_bytes(tmp_path))
    source = decoded.by_id(f"{T05_CHANGE_ID}/T-01/A1")
    successor = decoded.by_id(f"{T05_CHANGE_ID}/T-02/A1")
    assert source is not None and source.dependency_edge_control is not None
    assert source.dependency_edge_control["proof_head"]["state"] == "CURRENT"
    assert source.dependency_edge_control["cancellation_tombstone_ref"] == cancellation.tombstone_ref
    assert successor is not None and successor.attempt.dependency_admission is not None
    assert successor.attempt.dependency_admission["admission_id"] == proof_result.admission_id


def test_t05_invalidation_first_wins_real_lock_before_trigger_b(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof, successor_auth = _t05_prepare_target(tmp_path, prepare_successor=False)
    assert publish_dependency_acceptance_proof(tmp_path, proof).outcome is DependencyAdmissionOutcome.DEFERRED_SUCCESSOR_NOT_PREPARED
    invalidation_ref, _, _ = _issue_t05_invalidation_authorization(tmp_path, proof)
    store = attempt_store_v2_path(tmp_path)
    invalidation_written = threading.Event()
    preparation_waiting_for_lock = threading.Event()
    release_invalidation = threading.Event()
    original_thread_lock_for = attempt_runtime._thread_lock_for
    shared_lock = original_thread_lock_for(store)

    @contextmanager
    def observe_real_contention(lock_store: Path):
        if threading.current_thread().name == "t05-prepare-after-invalidation":
            preparation_waiting_for_lock.set()
        with shared_lock:
            yield

    def gate_invalidation_write(phase: str) -> None:
        if phase == "hash":
            invalidation_written.set()
            if not release_invalidation.wait(10):
                raise AssertionError("test did not release invalidation-first V2 lock")

    monkeypatch.setattr(attempt_runtime, "_thread_lock_for", lambda _store: observe_real_contention(_store))
    with ThreadPoolExecutor(max_workers=2) as pool:
        def invalidate_first():
            threading.current_thread().name = "t05-invalidation-first"
            return invalidate_dependency_proof(tmp_path, invalidation_ref, fault_hook=gate_invalidation_write)

        def prepare_after_invalidation():
            threading.current_thread().name = "t05-prepare-after-invalidation"
            return prepare_attempt(tmp_path, _payload(successor_auth, change_id=T05_CHANGE_ID, task_id="T-02"))

        invalidation_future = pool.submit(invalidate_first)
        assert invalidation_written.wait(10)
        preparation_future = pool.submit(prepare_after_invalidation)
        assert preparation_waiting_for_lock.wait(10)
        release_invalidation.set()
        invalidated = invalidation_future.result(timeout=10)
        successor = preparation_future.result(timeout=10)

    assert invalidated.dependency_edge_control["proof_head"]["state"] == "INVALIDATED"
    assert successor.attempt.dependency_admission is None
    source = decode_attempt_store_v2(_store_bytes(tmp_path)).by_id(f"{T05_CHANGE_ID}/T-01/A1")
    assert source is not None and source.dependency_edge_control["proof_head"]["state"] == "INVALIDATED"


def test_t05_admission_first_wins_real_lock_and_invalidation_preserves_object(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof, _ = _t05_prepare_target(tmp_path, prepare_successor=True)
    from planning_lite.dependency_admission import publish_dependency_acceptance_proof_blob

    store = attempt_store_v2_path(tmp_path)
    publish_dependency_acceptance_proof_blob(store.parent, proof)
    # Install only the exact test fixture CURRENT head so the two already-
    # authorized Runtime transitions can contend without Trigger A winning first.
    with attempt_runtime._store_lock(store, create=False):
        current = decode_attempt_store_v2(store.read_bytes())
        source_id = f"{T05_CHANGE_ID}/T-01/A1"
        source = current.by_id(source_id)
        assert source is not None
        control = {
            "schema_version": 1,
            "change_id": T05_CHANGE_ID,
            "source_task_or_operation_id": "T-01",
            "source_attempt_id": source_id,
            "successor_task_or_operation_id": "T-02",
            "successor_attempt_id": f"{T05_CHANGE_ID}/T-02/A1",
            "dependency_semantic_digest": resolve_dependency(tmp_path, "T-02").requirement["dependency_semantic_digest"],
            "proof_head": {
                "schema_version": 1,
                "state": "CURRENT",
                "proof_id": proof.proof_id,
                "proof_digest": proof.proof_digest,
                "invalidation_authorization_ref": None,
            },
            "cancellation_tombstone_ref": None,
        }
        seeded = replace(source, dependency_edge_control=control)
        attempt_runtime._safe_replace(
            store,
            AttemptStoreV2(tuple(sorted((seeded if row.attempt_id == source_id else row for row in current.attempts), key=lambda row: row.attempt_id))),
            attempt_id=source_id,
        )
    invalidation_ref, _, _ = _issue_t05_invalidation_authorization(tmp_path, proof)
    admission_written = threading.Event()
    invalidation_waiting_for_lock = threading.Event()
    release_admission = threading.Event()
    original_thread_lock_for = attempt_runtime._thread_lock_for
    shared_lock = original_thread_lock_for(store)

    @contextmanager
    def observe_real_contention(lock_store: Path):
        if threading.current_thread().name == "t05-invalidate-after-admission":
            invalidation_waiting_for_lock.set()
        with shared_lock:
            yield

    def gate_admission_write(phase: str) -> None:
        if phase == "hash":
            admission_written.set()
            if not release_admission.wait(10):
                raise AssertionError("test did not release admission-first V2 lock")

    monkeypatch.setattr(attempt_runtime, "_thread_lock_for", lambda _store: observe_real_contention(_store))
    with ThreadPoolExecutor(max_workers=2) as pool:
        def materialize_first():
            threading.current_thread().name = "t05-admission-first"
            return materialize_dependency_admission_if_ready(
                tmp_path, trigger="A", fault_hook=gate_admission_write
            )

        def invalidate_after_admission():
            threading.current_thread().name = "t05-invalidate-after-admission"
            return invalidate_dependency_proof(tmp_path, invalidation_ref)

        materialization_future = pool.submit(materialize_first)
        assert admission_written.wait(10)
        invalidation_future = pool.submit(invalidate_after_admission)
        assert invalidation_waiting_for_lock.wait(10)
        release_admission.set()
        materialized = materialization_future.result(timeout=10)
        invalidated = invalidation_future.result(timeout=10)

    assert materialized.outcome is DependencyAdmissionOutcome.MATERIALIZED
    assert invalidated.dependency_edge_control["proof_head"]["state"] == "INVALIDATED"
    decoded = decode_attempt_store_v2(_store_bytes(tmp_path))
    successor = decoded.by_id(f"{T05_CHANGE_ID}/T-02/A1")
    assert successor is not None and successor.attempt.dependency_admission is not None
    assert successor.attempt.dependency_admission["admission_id"] == materialized.admission_id


def test_t05_workspace_route_is_reresolved_under_lock_and_raw_artifact_bytes_are_authoritative(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof, _ = _t05_prepare_target(tmp_path, prepare_successor=True)
    original_lock = attempt_runtime._store_lock
    original_route = attempt_runtime.resolve_dependency_artifact_output_route
    lock_held = False
    route_calls = 0

    @contextmanager
    def tracked_lock(store: Path, *, create: bool):
        nonlocal lock_held
        with original_lock(store, create=create):
            lock_held = True
            try:
                yield
            finally:
                lock_held = False

    def tracked_route(root: Path):
        nonlocal route_calls
        assert lock_held, "T-05 route resolver ran outside the actual V2 mutation lock"
        route_calls += 1
        return original_route(root)

    monkeypatch.setattr(attempt_runtime, "_store_lock", tracked_lock)
    monkeypatch.setattr(attempt_runtime, "resolve_dependency_artifact_output_route", tracked_route)
    result = publish_dependency_acceptance_proof(tmp_path, proof)
    assert result.outcome is DependencyAdmissionOutcome.MATERIALIZED
    assert route_calls >= 2

    changed_root = tmp_path / "changed-artifact"
    changed_root.mkdir()
    changed_proof, _ = _t05_prepare_target(changed_root, prepare_successor=True)
    route = original_route(changed_root)
    route.path.write_bytes(b"changed after T-04 proof capture")
    with pytest.raises(AttemptRuntimeError):
        publish_dependency_acceptance_proof(changed_root, changed_proof)
    source = decode_attempt_store_v2(_store_bytes(changed_root)).by_id(f"{T05_CHANGE_ID}/T-01/A1")
    assert source is not None and source.dependency_edge_control is None


def _ready_t06_target(target: Path) -> tuple[object, str]:
    proof, authorization_ref = _t05_prepare_target(target, prepare_successor=True)
    result = publish_dependency_acceptance_proof(target, proof)
    assert result.outcome is DependencyAdmissionOutcome.MATERIALIZED
    return proof, authorization_ref


def _rewrite_t06_store(target: Path, mapping: dict[str, object]) -> bytes:
    raw = encode_attempt_store_v2(mapping)
    attempt_store_v2_path(target).write_bytes(raw)
    return raw


def test_t06_exported_claim_attempt_is_exact_direct_gate_and_post_write_readback(tmp_path: Path) -> None:
    _ready_t06_target(tmp_path)
    before = decode_attempt_store_v2(_store_bytes(tmp_path))
    successor_id = f"{T05_CHANGE_ID}/T-02/A1"
    successor_before = before.by_id(successor_id)
    assert successor_before is not None
    assert successor_before.runtime_state == "ACTIVATABLE"
    assert successor_before.attempt.dependency_admission is not None

    claimed = claim_attempt(tmp_path, successor_id)
    persisted = decode_attempt_store_v2(_store_bytes(tmp_path))
    verified = persisted.by_id(successor_id)
    assert claimed == verified
    assert verified is not None and verified.runtime_state == "IN_FLIGHT"
    assert verified.attempt == successor_before.attempt
    assert persisted.by_id(f"{T05_CHANGE_ID}/T-01/A1") == before.by_id(f"{T05_CHANGE_ID}/T-01/A1")
    after_first_claim = _store_bytes(tmp_path)
    with pytest.raises(AttemptStateError):
        claim_attempt(tmp_path, successor_id)
    assert _store_bytes(tmp_path) == after_first_claim


@pytest.mark.parametrize("mutant", ["missing", "forged_artifact_digest", "extra_key"])
def test_t06_malformed_or_nonjoining_embedded_admission_blocks_without_repair(
    tmp_path: Path, mutant: str
) -> None:
    _ready_t06_target(tmp_path)
    mapping = json.loads(_store_bytes(tmp_path).decode("utf-8"))
    successor = next(row for row in mapping["attempts"] if row["attempt"]["attempt_id"] == f"{T05_CHANGE_ID}/T-02/A1")
    admission = successor["attempt"]["dependency_admission"]
    if mutant == "missing":
        successor["attempt"]["dependency_admission"] = None
        _rewrite_t06_store(tmp_path, mapping)
    elif mutant == "forged_artifact_digest":
        admission["artifact_digest"] = "f" * 64
        semantic = dict(admission)
        semantic.pop("admission_id")
        admission["admission_id"] = "dadm_" + hashlib.sha256(
            json.dumps(semantic, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        _rewrite_t06_store(tmp_path, mapping)
    else:
        admission["unapproved"] = True
        attempt_store_v2_path(tmp_path).write_bytes(
            json.dumps(mapping, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8") + b"\n"
        )
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before
    if mutant == "extra_key":
        decoded_mapping = json.loads(before.decode("utf-8"))
        state = next(
            row["runtime_state"]
            for row in decoded_mapping["attempts"]
            if row["attempt"]["attempt_id"] == f"{T05_CHANGE_ID}/T-02/A1"
        )
    else:
        state = decode_attempt_store_v2(before).by_id(f"{T05_CHANGE_ID}/T-02/A1").runtime_state
    assert state == "ACTIVATABLE"


def test_t06_missing_current_head_blocks_even_when_the_immutable_blob_exists(tmp_path: Path) -> None:
    proof, _ = _ready_t06_target(tmp_path)
    mapping = json.loads(_store_bytes(tmp_path).decode("utf-8"))
    source = next(row for row in mapping["attempts"] if row["attempt"]["attempt_id"] == f"{T05_CHANGE_ID}/T-01/A1")
    source["dependency_edge_control"] = None
    before = _rewrite_t06_store(tmp_path, mapping)
    proof_blob = attempt_store_v2_path(tmp_path).parent / "dependency-admission" / "proofs" / f"{proof.proof_digest}.json"
    assert proof_blob.is_file()
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before


def test_t06_invalidated_current_head_blocks_without_rewriting_attempts(tmp_path: Path) -> None:
    proof, _ = _ready_t06_target(tmp_path)
    invalidation_ref, _, _ = _issue_t05_invalidation_authorization(tmp_path, proof)
    invalidated = invalidate_dependency_proof(tmp_path, invalidation_ref)
    assert invalidated.dependency_edge_control["proof_head"]["state"] == "INVALIDATED"
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptStateError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before


@pytest.mark.parametrize(
    ("field", "replacement"),
    [
        ("acceptance_proof_id", "dproof_" + "0" * 64),
        ("acceptance_proof_digest", "0" * 64),
        ("artifact_logical_ref", "artifact:forged"),
        ("required_successor_input_logical_ref", "artifact:forged-input"),
    ],
)
def test_t06_rehashed_admission_join_mutants_block_without_repair(
    tmp_path: Path, field: str, replacement: str
) -> None:
    _ready_t06_target(tmp_path)
    mapping = json.loads(_store_bytes(tmp_path).decode("utf-8"))
    successor = next(row for row in mapping["attempts"] if row["attempt"]["attempt_id"] == f"{T05_CHANGE_ID}/T-02/A1")
    admission = successor["attempt"]["dependency_admission"]
    admission[field] = replacement
    if field == "acceptance_proof_id":
        admission["acceptance_proof_digest"] = "0" * 64
    elif field == "acceptance_proof_digest":
        admission["acceptance_proof_id"] = "dproof_" + replacement
    semantic = dict(admission)
    semantic.pop("admission_id")
    admission["admission_id"] = "dadm_" + hashlib.sha256(
        json.dumps(semantic, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    _rewrite_t06_store(tmp_path, mapping)
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before


@pytest.mark.parametrize("binding_mutant", ["tasks_ref", "dependency_semantic_digest"])
def test_t06_stale_preparation_binding_blocks(
    tmp_path: Path, binding_mutant: str
) -> None:
    _ready_t06_target(tmp_path)
    mapping = json.loads(_store_bytes(tmp_path).decode("utf-8"))
    successor = next(row for row in mapping["attempts"] if row["attempt"]["attempt_id"] == f"{T05_CHANGE_ID}/T-02/A1")
    if binding_mutant == "tasks_ref":
        successor["attempt"]["preparation_binding"]["tasks_ref"] = ".planning/changes/active/forged/tasks.md"
    else:
        forged_digest = "0" * 64
        successor["attempt"]["preparation_binding"]["dependency_semantic_digest"] = forged_digest
        admission = successor["attempt"]["dependency_admission"]
        admission["dependency_semantic_digest"] = forged_digest
        semantic = dict(admission)
        semantic.pop("admission_id")
        admission["admission_id"] = "dadm_" + hashlib.sha256(
            json.dumps(semantic, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
    before = _rewrite_t06_store(tmp_path, mapping)
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before


def test_t06_missing_proof_blob_blocks(tmp_path: Path) -> None:
    proof, _ = _ready_t06_target(tmp_path)
    from planning_lite.dependency_admission import dependency_acceptance_proof_path

    proof_path = dependency_acceptance_proof_path(attempt_store_v2_path(tmp_path).parent, proof)
    proof_path.unlink()
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before


def test_t06_persisted_cancellation_tombstone_and_pointer_remain_blocking_after_status_edit(tmp_path: Path) -> None:
    _ready_t06_target(tmp_path)
    _set_t05_task_status(tmp_path, "T-02", "Cancelled")
    observed = attempt_runtime.observe_dependency_cancellation(tmp_path, T05_CHANGE_ID, "T-02")
    assert observed.outcome is attempt_runtime.CancellationOutcome.BLOCKED
    _set_t05_task_status(tmp_path, "T-02", "Pending")
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before
    source = decode_attempt_store_v2(before).by_id(f"{T05_CHANGE_ID}/T-01/A1")
    assert source is not None and source.dependency_edge_control is not None
    assert source.dependency_edge_control["cancellation_tombstone_ref"] == observed.tombstone_ref


def test_t06_current_classification_change_blocks_stale_dependent_binding(tmp_path: Path) -> None:
    _ready_t06_target(tmp_path)
    tasks_file = tmp_path / ".planning/changes/active" / T05_CHANGE_ID / "tasks.md"
    lines = tasks_file.read_text(encoding="utf-8").splitlines()
    index = next(i for i, line in enumerate(lines) if line.startswith("| `T-02` |"))
    assert "| `T-01` |" in lines[index]
    lines[index] = lines[index].replace("| `T-01` |", "| `None` |", 1)
    tasks_file.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before


def test_t06_genuine_v1_independent_claim_terminalization_and_recovery_remain_compatible(tmp_path: Path) -> None:
    def seed_legacy_independent(root: Path, suffix: str) -> AttemptEnvelopeV1:
        _ensure_runtime_governance(root)
        reference = "authz_" + suffix * 32
        legacy_authorization = AuthorizationRecordV1(
            1,
            reference,
            AuthorizationAction.PREPARATION,
            PreparationScopeV1(CHANGE_ID, "T-03"),
            authorization_owner.PREPARATION_AUTHORITY,
            "AUTHORIZED",
            f"OWNER-LEGACY-{suffix}",
        )
        auth_store = authorization_store_path(root)
        auth_store.mkdir(parents=True, exist_ok=True)
        (auth_store / f"{reference}.json").write_bytes(encode_authorization_record(legacy_authorization))
        legacy = _legacy_v1_envelope(change_id=CHANGE_ID, task_id="T-03", authorization_ref=reference)
        store = attempt_store_path(root)
        store.parent.mkdir(parents=True, exist_ok=True)
        store.write_bytes(encode_attempt_store(AttemptStoreV1((legacy,))))
        return legacy

    terminal_target = tmp_path / "legacy-terminal"
    terminal_target.mkdir()
    terminal_attempt = seed_legacy_independent(terminal_target, "b")
    assert claim_attempt(terminal_target, terminal_attempt.attempt_id).runtime_state == "IN_FLIGHT"
    terminal = terminalize_attempt(
        terminal_target,
        terminal_attempt.attempt_id,
        ObservedResultV1("legacy-v1-completed", terminal_attempt.attempt_id, "COMPLETED"),
    )
    assert terminal.runtime_state == "TERMINAL"
    assert terminal.observed_result == ObservedResultV1("legacy-v1-completed", terminal_attempt.attempt_id, "COMPLETED")

    recovery_target = tmp_path / "legacy-recovery"
    recovery_target.mkdir()
    recovery_attempt = seed_legacy_independent(recovery_target, "c")
    assert claim_attempt(recovery_target, recovery_attempt.attempt_id).runtime_state == "IN_FLIGHT"
    recovery_ref = issue_recovery_authorization(recovery_target, recovery_attempt.attempt_id, "OWNER-LEGACY-RECOVERY")
    recovered = resolve_interrupted_attempt(recovery_target, recovery_attempt.attempt_id, recovery_ref)
    assert recovered.runtime_state == "TERMINAL"
    assert recovered.recovery_authorization_ref == recovery_ref
    assert recovered.observed_result is not None and recovered.observed_result.execution_status == "INTERRUPTED"


def test_t06_own_preparation_authorization_and_raw_artifact_bytes_are_required(tmp_path: Path) -> None:
    proof, authorization_ref = _ready_t06_target(tmp_path)
    authorization_file = authorization_store_path(tmp_path) / f"{authorization_ref}.json"
    authorization_file.unlink()
    before = _store_bytes(tmp_path)
    with pytest.raises(AttemptAuthorizationError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(tmp_path) == before

    # Restore the exact immutable record from the fixture's original reference
    # is intentionally impossible here; use a fresh independent target for the
    # canonical-route byte mismatch probe.
    changed = tmp_path / "changed-artifact"
    changed.mkdir()
    _ready_t06_target(changed)
    route = attempt_runtime.resolve_dependency_artifact_output_route(changed)
    route.path.write_bytes(b"stale bytes after T-05 admission")
    store_before = _store_bytes(changed)
    with pytest.raises(AttemptRuntimeError):
        claim_attempt(changed, f"{T05_CHANGE_ID}/T-02/A1")
    assert _store_bytes(changed) == store_before


def test_t06_route_and_raw_bytes_are_reresolved_inside_the_claim_lock(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _ready_t06_target(tmp_path)
    route = attempt_runtime.resolve_dependency_artifact_output_route(tmp_path)
    real_lock = attempt_runtime._store_lock
    real_resolver = attempt_runtime.resolve_dependency_artifact_output_route
    real_read_bytes = Path.read_bytes
    lock_held = False
    lock_calls = 0
    route_calls = 0
    artifact_reads = 0

    @contextmanager
    def tracked_lock(store: Path, *, create: bool):
        nonlocal lock_held, lock_calls
        lock_calls += 1
        with real_lock(store, create=create):
            lock_held = True
            try:
                yield
            finally:
                lock_held = False

    def tracked_resolver(root: Path):
        nonlocal route_calls
        assert lock_held
        route_calls += 1
        return real_resolver(root)

    def tracked_read_bytes(path: Path) -> bytes:
        nonlocal artifact_reads
        if path == route.path:
            assert lock_held
            artifact_reads += 1
        return real_read_bytes(path)

    monkeypatch.setattr(attempt_runtime, "_store_lock", tracked_lock)
    monkeypatch.setattr(attempt_runtime, "resolve_dependency_artifact_output_route", tracked_resolver)
    monkeypatch.setattr(Path, "read_bytes", tracked_read_bytes)
    claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    assert route_calls == 2
    assert artifact_reads == 2
    assert lock_calls == 1


def test_t06_live_cancellation_blocks_and_only_uses_the_existing_cancellation_side_effect(tmp_path: Path) -> None:
    _ready_t06_target(tmp_path)
    _set_t05_task_status(tmp_path, "T-02", "Cancelled")
    with pytest.raises(AttemptStateError):
        claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")
    store = decode_attempt_store_v2(_store_bytes(tmp_path))
    source = store.by_id(f"{T05_CHANGE_ID}/T-01/A1")
    successor = store.by_id(f"{T05_CHANGE_ID}/T-02/A1")
    assert successor is not None and successor.runtime_state == "ACTIVATABLE"
    assert source is not None and source.dependency_edge_control is not None
    assert source.dependency_edge_control["cancellation_tombstone_ref"] == cancellation_tombstone_ref(
        CancellationTombstoneV1(T05_CHANGE_ID)
    )


def test_t06_multiprocess_claim_has_exactly_one_winner(tmp_path: Path) -> None:
    _ready_t06_target(tmp_path)
    attempt_id = f"{T05_CHANGE_ID}/T-02/A1"
    context = mp.get_context("spawn")
    queue = context.Queue()
    processes = [context.Process(target=_claim_worker, args=(str(tmp_path), attempt_id, queue)) for _ in range(2)]
    for process in processes:
        process.start()
    results = [queue.get(timeout=30) for _ in processes]
    for process in processes:
        process.join(timeout=30)
    assert all(process.exitcode == 0 for process in processes)
    assert [result[0] for result in results].count("PASS") == 1
    assert [result[0] for result in results].count("FAIL") == 1
    assert lookup_attempt(tmp_path, attempt_id).runtime_state == "IN_FLIGHT"


def test_t06_invalidation_first_serializes_before_claim_and_keeps_successor_activatable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof, _ = _ready_t06_target(tmp_path)
    invalidation_ref, _, _ = _issue_t05_invalidation_authorization(tmp_path, proof)
    store = attempt_store_v2_path(tmp_path)
    invalidation_written = threading.Event()
    claim_waiting = threading.Event()
    release_invalidation = threading.Event()
    shared_lock = attempt_runtime._thread_lock_for(store)

    @contextmanager
    def track_contention(_store: Path):
        if threading.current_thread().name == "t06-claim-after-invalidation":
            claim_waiting.set()
        with shared_lock:
            yield

    def hold_invalidation(phase: str) -> None:
        if phase == "hash":
            invalidation_written.set()
            assert release_invalidation.wait(20)

    monkeypatch.setattr(attempt_runtime, "_thread_lock_for", lambda _store: track_contention(_store))
    with ThreadPoolExecutor(max_workers=2) as pool:
        invalidation = pool.submit(invalidate_dependency_proof, tmp_path, invalidation_ref, fault_hook=hold_invalidation)

        def claim_after():
            threading.current_thread().name = "t06-claim-after-invalidation"
            return claim_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1")

        assert invalidation_written.wait(15)
        claim = pool.submit(claim_after)
        assert claim_waiting.wait(15)
        release_invalidation.set()
        invalidation.result(timeout=20)
        with pytest.raises(AttemptStateError):
            claim.result(timeout=20)
    assert lookup_attempt(tmp_path, f"{T05_CHANGE_ID}/T-02/A1").runtime_state == "ACTIVATABLE"


def test_t06_claim_first_survives_later_invalidation_terminalization_and_recovery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    proof, _ = _ready_t06_target(tmp_path)
    invalidation_ref, _, _ = _issue_t05_invalidation_authorization(tmp_path, proof)
    store = attempt_store_v2_path(tmp_path)
    claim_written = threading.Event()
    invalidation_waiting = threading.Event()
    release_claim = threading.Event()
    shared_lock = attempt_runtime._thread_lock_for(store)

    @contextmanager
    def track_contention(_store: Path):
        if threading.current_thread().name == "t06-invalidate-after-claim":
            invalidation_waiting.set()
        with shared_lock:
            yield

    def hold_claim(phase: str) -> None:
        if phase == "hash":
            claim_written.set()
            assert release_claim.wait(20)

    monkeypatch.setattr(attempt_runtime, "_thread_lock_for", lambda _store: track_contention(_store))
    attempt_id = f"{T05_CHANGE_ID}/T-02/A1"
    with ThreadPoolExecutor(max_workers=2) as pool:
        claim = pool.submit(claim_attempt, tmp_path, attempt_id, fault_hook=hold_claim)

        def invalidate_after():
            threading.current_thread().name = "t06-invalidate-after-claim"
            return invalidate_dependency_proof(tmp_path, invalidation_ref)

        assert claim_written.wait(15)
        invalidation = pool.submit(invalidate_after)
        assert invalidation_waiting.wait(15)
        release_claim.set()
        assert claim.result(timeout=20).runtime_state == "IN_FLIGHT"
        assert invalidation.result(timeout=20).dependency_edge_control["proof_head"]["state"] == "INVALIDATED"

    terminal = terminalize_attempt(tmp_path, attempt_id, ObservedResultV1("t06-completed", attempt_id, "COMPLETED"))
    assert terminal.runtime_state == "TERMINAL"

    recovery_target = tmp_path / "recovery-after-invalidation"
    recovery_target.mkdir()
    recovery_proof, _ = _ready_t06_target(recovery_target)
    recovery_attempt_id = f"{T05_CHANGE_ID}/T-02/A1"
    claim_attempt(recovery_target, recovery_attempt_id)
    recovery_invalidation_ref, _, _ = _issue_t05_invalidation_authorization(recovery_target, recovery_proof)
    invalidate_dependency_proof(recovery_target, recovery_invalidation_ref)
    recovery_ref = issue_recovery_authorization(recovery_target, recovery_attempt_id, "OWNER-T06-RECOVERY")
    recovered = resolve_interrupted_attempt(recovery_target, recovery_attempt_id, recovery_ref)
    assert recovered.runtime_state == "TERMINAL"
    assert recovered.recovery_authorization_ref == recovery_ref
    assert recovered.observed_result is not None and recovered.observed_result.execution_status == "INTERRUPTED"
