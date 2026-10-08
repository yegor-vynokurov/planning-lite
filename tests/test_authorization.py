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
    AuthorizationRecordV2,
    DependencyProofInvalidationScopeV1,
    PreparationScopeV1,
    PreparationScopeV2,
    RecoveryScopeV1,
    ResolutionOutcome,
    decode_authorization_record,
    encode_authorization_record,
    issue_authorization,
    issue_preparation_authorization,
    issue_recovery_authorization,
    resolve_authorization,
)
from planning_lite.dependency_admission import (
    CancellationCarrierError,
    CancellationTombstoneV1,
    resolve_dependency,
)
from planning_lite.plan_compilation import canonical_json


POSITIVE_CHANGE_ID = "CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001"
POSITIVE_TASK_ID = "T-08"


def _target(root: Path, *, planning_root: str = ".planning") -> Path:
    defaults = root / ".planning/framework/defaults.yml"
    defaults.parent.mkdir(parents=True)
    defaults.write_text(
        "schema_version: 1\n"
        "project_policy:\n"
        "  schema_version: 1\n"
        f"  planning_root: {planning_root}\n"
        "  agents_root: .agents\n"
        "  forbidden_read_paths: []\n"
        "  secret_storage: prohibited\n",
        encoding="utf-8",
    )
    (root / ".planning/CONFIG.yml").write_text("{}\n", encoding="utf-8")
    selected_config = root / planning_root / "CONFIG.yml"
    selected_config.parent.mkdir(parents=True, exist_ok=True)
    selected_config.write_text("{}\n", encoding="utf-8")
    return root


def _governed_target(
    root: Path,
    *,
    change_id: str = POSITIVE_CHANGE_ID,
    task_ids: tuple[str, ...] = (POSITIVE_TASK_ID,),
    planning_root: str = ".planning",
    cancelled_task: str | None = None,
) -> Path:
    """Build exact approved governance below the effective planning root.

    The fixed T-01/T-02 edge is retained, each positive task is explicitly
    present and independent, and the existing dependency fixture writer
    derives approval digests/reconciliation bytes from managed templates.
    ``planning_root`` selects canonical ACTIVE/Change governance and product-
    root-relative refs as well as the existing Authorization and Attempt
    storage locations; bootstrap defaults and CONFIG discovery remain in
    product ``.planning``.
    """
    target = _target(root, planning_root=planning_root)
    import test_dependency_admission as dependency_fixture

    rows = dependency_fixture._task_rows()
    rows = rows[:2]
    for index, task_id in enumerate(task_ids):
        base = dependency_fixture._task_rows()[2 + min(index, 1)].copy()
        base["id"] = task_id
        base["edge"] = "None"
        base["status"] = "Pending"
        rows.append(base)
    if cancelled_task is not None:
        next(row for row in rows if row["id"] == cancelled_task)["status"] = "Cancelled"
    dependency_fixture._write_fixture(
        target,
        change_id=change_id,
        planning_root=planning_root,
        task_rows=rows,
    )
    return target


def test_preparation_record_is_exact_canonical_and_resolves(tmp_path: Path) -> None:
    target = _governed_target(tmp_path / "consumer")
    reference = issue_preparation_authorization(
        target, POSITIVE_CHANGE_ID, POSITIVE_TASK_ID, "PLAN-APPROVAL-REF"
    )
    assert reference.startswith("authz_") and len(reference) == 38
    store = authorization.authorization_store_path(target)
    raw = (store / f"{reference}.json").read_bytes()
    current = resolve_dependency(target, POSITIVE_TASK_ID)
    expected_scope = PreparationScopeV2(
        POSITIVE_CHANGE_ID,
        POSITIVE_TASK_ID,
        current.plan_ref,
        current.tasks_ref,
        current.approved_plan_digest,
        current.dependency_semantic_digest,
        current.requirement["requirement_id"],
        "NOT_APPLICABLE",
        None,
    )
    expected = {
        "schema_version": 2,
        "authorization_ref": reference,
        "action_type": AuthorizationAction.PREPARATION.value,
        "scope": authorization._scope_mapping(expected_scope),
        "decision_authority_class": authorization.PREPARATION_AUTHORITY,
        "decision_outcome": "AUTHORIZED",
        "decision_provenance_ref": "PLAN-APPROVAL-REF",
    }
    assert raw == (canonical_json(expected) + "\n").encode("utf-8")
    assert isinstance(decode_authorization_record(raw), AuthorizationRecordV2)
    duplicate = raw.replace(
        b'"expected_attempt_id":null',
        b'"expected_attempt_id":null,"expected_attempt_id":null',
    )
    with pytest.raises(AuthorizationError):
        decode_authorization_record(duplicate)
    for field_change in (
        {"schema_version": True},
        {"extra": "forbidden"},
    ):
        mutant = json.loads(raw)
        mutant.update(field_change)
        with pytest.raises(AuthorizationError):
            decode_authorization_record((canonical_json(mutant) + "\n").encode("utf-8"))
    wrong_attempt = json.loads(raw)
    wrong_attempt["scope"]["expected_attempt_id"] = f"{POSITIVE_CHANGE_ID}/T-08/A1"
    with pytest.raises(AuthorizationError):
        decode_authorization_record((canonical_json(wrong_attempt) + "\n").encode("utf-8"))
    result = resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        expected_scope,
    )
    assert result.outcome is ResolutionOutcome.AUTHORIZED
    assert isinstance(result.record, AuthorizationRecordV2)
    assert result.record.scope == expected_scope
    assert encode_authorization_record(result.record) == raw
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(POSITIVE_CHANGE_ID, POSITIVE_TASK_ID),
    ).outcome is ResolutionOutcome.WRONG_SCOPE


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


def test_genuine_v1_preparation_read_is_independent_only_and_never_synthesized(tmp_path: Path) -> None:
    target = _governed_target(tmp_path / "consumer")
    store = authorization.authorization_store_path(target)
    store.mkdir(parents=True)
    independent_ref = "authz_" + "1" * 32
    independent_bytes = (
        "{\"action_type\":\"OWNER_AUTHORIZED_ATTEMPT_PREPARATION\","
        f"\"authorization_ref\":\"{independent_ref}\","
        "\"decision_authority_class\":\"EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY\","
        "\"decision_outcome\":\"AUTHORIZED\","
        "\"decision_provenance_ref\":\"legacy-owner-decision\","
        "\"schema_version\":1,"
        f"\"scope\":{{\"change_id\":\"{POSITIVE_CHANGE_ID}\","
        f"\"task_or_operation_id\":\"{POSITIVE_TASK_ID}\"}}}}\n"
    ).encode("utf-8")
    (store / f"{independent_ref}.json").write_bytes(independent_bytes)
    read = decode_authorization_record(independent_bytes)
    assert isinstance(read, AuthorizationRecordV1)
    assert resolve_authorization(
        target,
        independent_ref,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(POSITIVE_CHANGE_ID, POSITIVE_TASK_ID),
    ).outcome is ResolutionOutcome.AUTHORIZED

    dependent_ref = "authz_" + "2" * 32
    dependent_bytes = (
        "{\"action_type\":\"OWNER_AUTHORIZED_ATTEMPT_PREPARATION\","
        f"\"authorization_ref\":\"{dependent_ref}\","
        "\"decision_authority_class\":\"EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY\","
        "\"decision_outcome\":\"AUTHORIZED\","
        "\"decision_provenance_ref\":\"legacy-owner-decision\","
        "\"schema_version\":1,"
        f"\"scope\":{{\"change_id\":\"{POSITIVE_CHANGE_ID}\","
        "\"task_or_operation_id\":\"T-02\"}}\n"
    ).encode("utf-8")
    (store / f"{dependent_ref}.json").write_bytes(dependent_bytes)
    assert resolve_authorization(
        target,
        dependent_ref,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(POSITIVE_CHANGE_ID, "T-02"),
    ).outcome is ResolutionOutcome.WRONG_SCOPE
    assert (store / f"{independent_ref}.json").read_bytes() == independent_bytes
    assert (store / f"{dependent_ref}.json").read_bytes() == dependent_bytes


def test_no_plan_and_caller_constructed_v2_scope_publish_nothing(tmp_path: Path) -> None:
    planless = _target(tmp_path / "planless")
    with pytest.raises(AuthorizationError):
        issue_preparation_authorization(planless, POSITIVE_CHANGE_ID, POSITIVE_TASK_ID, "OWNER")
    assert not authorization.authorization_store_path(planless).exists()

    target = _governed_target(tmp_path / "governed")
    current = resolve_dependency(target, POSITIVE_TASK_ID)
    supplied = PreparationScopeV2(
        POSITIVE_CHANGE_ID,
        POSITIVE_TASK_ID,
        current.plan_ref,
        current.tasks_ref,
        current.approved_plan_digest,
        current.dependency_semantic_digest,
        current.requirement["requirement_id"],
        "NOT_APPLICABLE",
        None,
    )
    with pytest.raises(AuthorizationError):
        issue_authorization(
            target,
            AuthorizationAction.PREPARATION,
            supplied,
            "OWNER",
        )
    with pytest.raises(AuthorizationError):
        issue_authorization(
            target,
            AuthorizationAction.PREPARATION,
            {"change_id": POSITIVE_CHANGE_ID, "task_or_operation_id": POSITIVE_TASK_ID},  # type: ignore[arg-type]
            "OWNER",
        )
    assert not authorization.authorization_store_path(target).exists()


def test_generic_and_wrapper_ingress_publish_same_resolver_owned_v2_shape(tmp_path: Path) -> None:
    target = _governed_target(tmp_path / "consumer")
    generic = issue_authorization(
        target,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(POSITIVE_CHANGE_ID, POSITIVE_TASK_ID),
        "generic-owner-decision",
    )
    wrapped = issue_preparation_authorization(
        target,
        POSITIVE_CHANGE_ID,
        POSITIVE_TASK_ID,
        "wrapper-owner-decision",
    )
    for reference in (generic, wrapped):
        record = decode_authorization_record(
            (authorization.authorization_store_path(target) / f"{reference}.json").read_bytes()
        )
        assert isinstance(record, AuthorizationRecordV2)
        expected = resolve_dependency(target, POSITIVE_TASK_ID)
        assert record.scope == PreparationScopeV2(
            expected.change_id,
            expected.task_id,
            expected.plan_ref,
            expected.tasks_ref,
            expected.approved_plan_digest,
            expected.dependency_semantic_digest,
            expected.requirement["requirement_id"],
            expected.dependency_classification,
            None,
        )
    recovery = issue_recovery_authorization(target, f"{POSITIVE_CHANGE_ID}/T-08/A1", "lifecycle-owner")
    recovery_record = decode_authorization_record(
        (authorization.authorization_store_path(target) / f"{recovery}.json").read_bytes()
    )
    assert isinstance(recovery_record, AuthorizationRecordV1)
    assert resolve_authorization(
        target,
        recovery,
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1(f"{POSITIVE_CHANGE_ID}/T-08/A1"),
    ).outcome is ResolutionOutcome.AUTHORIZED


def test_dependent_preparation_binds_exact_first_attempt_identity(tmp_path: Path) -> None:
    target = _governed_target(tmp_path / "consumer", task_ids=("T-08",))
    reference = issue_preparation_authorization(
        target, POSITIVE_CHANGE_ID, "T-02", "owner-decision:prepare-T02-A1"
    )
    record = decode_authorization_record(
        (authorization.authorization_store_path(target) / f"{reference}.json").read_bytes()
    )
    assert isinstance(record, AuthorizationRecordV2)
    assert record.scope.dependency_classification == "DEPENDENCY_EDGE_MEMBER"
    assert record.scope.expected_attempt_id == f"{POSITIVE_CHANGE_ID}/T-02/A1"
    assert record.scope.task_or_operation_id == "T-02"
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        record.scope,
    ).outcome is ResolutionOutcome.AUTHORIZED


@pytest.mark.parametrize("occupied_task_id", ["T-01", "T-02"])
@pytest.mark.parametrize("requested_task_id", ["T-01", "T-02"])
def test_dependent_preparation_refuses_occupied_edge_a1_before_publication(
    tmp_path: Path, occupied_task_id: str, requested_task_id: str
) -> None:
    """Runtime-owned exact lookup blocks each occupied edge A1 without publishing."""
    from planning_lite.attempt_evaluation import AttemptRecordV1, CandidateIdentityV1, IdentityRefV1
    from planning_lite.attempt_runtime import (
        AttemptEnvelopeV1,
        AttemptStoreV1,
        LookupOutcome,
        attempt_store_path,
        encode_attempt_store,
        lookup_attempt,
    )

    target = _governed_target(tmp_path / occupied_task_id, task_ids=("T-03",))
    occupied_id = f"{POSITIVE_CHANGE_ID}/{occupied_task_id}/A1"
    head = "b" * 40
    occupied = AttemptRecordV1(
        occupied_id,
        POSITIVE_CHANGE_ID,
        occupied_task_id,
        1,
        "authz_" + "a" * 32,
        "AC-OCCUPIED",
        CandidateIdentityV1("GIT_COMMIT", head),
        (IdentityRefV1("HEAD", head),),
    )
    runtime_path = attempt_store_path(target)
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    runtime_before = encode_attempt_store(
        AttemptStoreV1((AttemptEnvelopeV1(occupied, "ACTIVATABLE"),))
    )
    runtime_path.write_bytes(runtime_before)
    assert lookup_attempt(target, occupied_id).outcome is LookupOutcome.FOUND

    authorization_store = authorization.authorization_store_path(target)
    assert not authorization_store.exists()
    with pytest.raises(AuthorizationError, match="unoccupied exact A1"):
        issue_preparation_authorization(
            target,
            POSITIVE_CHANGE_ID,
            requested_task_id,
            "owner-decision:occupied-edge-a1",
        )

    assert runtime_path.read_bytes() == runtime_before
    assert not authorization_store.exists()
    assert lookup_attempt(target, occupied_id).outcome is LookupOutcome.FOUND


def test_both_endpoint_authorizations_are_preissued_and_sibling_remains_usable(
    tmp_path: Path,
) -> None:
    """Issuance checks dual-A1 absence once; use rechecks the sibling's own A1."""
    from planning_lite.attempt_runtime import AttemptAuthorizationError, prepare_attempt

    target = _governed_target(tmp_path / "consumer", task_ids=("T-03",))
    source_auth = issue_preparation_authorization(
        target, POSITIVE_CHANGE_ID, "T-01", "owner-decision:prepare-T01-A1"
    )
    successor_auth = issue_preparation_authorization(
        target, POSITIVE_CHANGE_ID, "T-02", "owner-decision:prepare-T02-A1"
    )
    source_resolution = resolve_dependency(target, "T-01")
    successor_resolution = resolve_dependency(target, "T-02")
    assert source_resolution.requirement == successor_resolution.requirement

    def payload(task_id: str, auth_ref: str) -> dict[str, object]:
        return {
            "change_id": POSITIVE_CHANGE_ID,
            "task_or_operation_id": task_id,
            "authorization_ref": auth_ref,
            "acceptance_contract_ref": source_resolution.requirement["acceptance_contract_ref"],
            "candidate_identity": {"kind": "GIT_COMMIT", "head": "b" * 40, "dirty_manifest": []},
            "baseline_refs": [{"ref": "HEAD", "identity": "b" * 40}],
            "operation_guidance_ref": "EXECUTE_AUTHORIZED_TASK",
        }

    source = prepare_attempt(target, payload("T-01", source_auth))
    assert source.attempt_id == f"{POSITIVE_CHANGE_ID}/T-01/A1"
    # Trigger B defers because the source proof is not CURRENT; the pre-issued
    # sibling remains valid because its own exact A1 is still free.
    successor = prepare_attempt(target, payload("T-02", successor_auth))
    assert successor.attempt_id == f"{POSITIVE_CHANGE_ID}/T-02/A1"

    with pytest.raises(AuthorizationError, match="unoccupied exact A1"):
        issue_preparation_authorization(
            target, POSITIVE_CHANGE_ID, "T-01", "owner-decision:late-T01"
        )
    with pytest.raises(AttemptAuthorizationError):
        prepare_attempt(target, payload("T-01", successor_auth))


def test_dependent_preparation_fails_closed_on_corrupt_attempt_occupancy_store(tmp_path: Path) -> None:
    """A corrupt authoritative Runtime store prevents dependent issuance unchanged."""
    from planning_lite.attempt_runtime import attempt_store_path

    target = _governed_target(tmp_path / "corrupt-runtime", task_ids=("T-03",))
    runtime_path = attempt_store_path(target)
    runtime_path.parent.mkdir(parents=True, exist_ok=True)
    corrupt = b"not an authoritative Attempt Runtime document\n"
    runtime_path.write_bytes(corrupt)
    authorization_store = authorization.authorization_store_path(target)

    with pytest.raises(AuthorizationError, match="Runtime returned CORRUPT_CONFLICT"):
        issue_preparation_authorization(
            target,
            POSITIVE_CHANGE_ID,
            "T-02",
            "owner-decision:corrupt-edge-a1-state",
        )

    assert runtime_path.read_bytes() == corrupt
    assert not authorization_store.exists()


def test_preparation_ingress_observes_source_cancellation_before_any_authorization(tmp_path: Path) -> None:
    target = _governed_target(
        tmp_path / "consumer",
        task_ids=("T-03",),
        cancelled_task="T-01",
    )
    store = authorization.authorization_store_path(target)
    with pytest.raises(AuthorizationError):
        issue_preparation_authorization(target, POSITIVE_CHANGE_ID, "T-02", "owner-decision")
    assert not store.exists()
    from planning_lite.attempt_runtime import attempt_store_v2_path

    v2_store = attempt_store_v2_path(target)
    assert not v2_store.exists()
    tombstones = list((v2_store.parent / "dependency-admission" / "cancellations").glob("*.json"))
    assert len(tombstones) == 1
    task_file = target / ".planning" / "changes" / "active" / POSITIVE_CHANGE_ID / "tasks.md"
    task_file.write_text(
        task_file.read_text(encoding="utf-8").replace(
            "| `T-01` | Produce governed artifact | `Tracer bullet` | `None` | focused producer test | source task | `Cancelled` |",
            "| `T-01` | Produce governed artifact | `Tracer bullet` | `None` | focused producer test | source task | `Pending` |",
        ),
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(AuthorizationError):
        issue_preparation_authorization(target, POSITIVE_CHANGE_ID, "T-02", "owner-decision")
    assert not store.exists()
    assert len(list((v2_store.parent / "dependency-admission" / "cancellations").glob("*.json"))) == 1


@pytest.mark.parametrize("failure", ["publication", "durable reread"])
def test_preparation_runtime_carrier_failure_publishes_no_authorization(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, failure: str
) -> None:
    import planning_lite.attempt_runtime as runtime

    target = _governed_target(
        tmp_path / "consumer",
        task_ids=("T-03",),
        cancelled_task="T-02",
    )
    original_resolve = runtime.resolve_cancellation_tombstone
    if failure == "publication":
        def fail_publish(carrier_root: Path, record: CancellationTombstoneV1):
            raise CancellationCarrierError("injected publication failure")

        monkeypatch.setattr(runtime, "_publish_cancellation_tombstone_locked", fail_publish)
    else:
        reads = 0

        def fail_durable_reread(carrier_root: Path, record: CancellationTombstoneV1):
            nonlocal reads
            reads += 1
            if reads == 1:
                return None
            if reads == 2:
                raise CancellationCarrierError("injected durable reread failure")
            return original_resolve(carrier_root, record)

        monkeypatch.setattr(runtime, "resolve_cancellation_tombstone", fail_durable_reread)

    with pytest.raises(AuthorizationError):
        issue_preparation_authorization(target, POSITIVE_CHANGE_ID, "T-02", "owner-decision")
    store = authorization.authorization_store_path(target)
    assert not store.exists()
    v2_store = runtime.attempt_store_v2_path(target)
    assert not v2_store.exists()
    tombstones = list((v2_store.parent / "dependency-admission" / "cancellations").glob("*.json"))
    assert (len(tombstones) == 0) is (failure == "publication")
    if failure == "durable reread":
        assert tombstones


def _write_invalidation_decision(
    target: Path,
    scope: DependencyProofInvalidationScopeV1,
    *,
    decision_id: str = "ADR-0042",
    status: str = "Accepted",
    rationale: str = "The owner reviewed contradictory evidence for the exact proof.",
    block_overrides: dict[str, object] | None = None,
    duplicate_block: bool = False,
    duplicate_status: bool = False,
) -> tuple[Path, str]:
    slug = "invalidate-t01-proof"
    path = target / ".planning" / "decisions" / f"{decision_id}-{slug}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    block: dict[str, object] = {
        "schema_version": 1,
        "decision_id": decision_id,
        "decision_kind": "DEPENDENCY_PROOF_INVALIDATION",
        "decision_status": "APPROVED",
        "change_id": scope.change_id,
        "source_attempt_id": scope.source_attempt_id,
        "successor_attempt_id": scope.successor_attempt_id,
        "proof_id": scope.proof_id,
        "decision_outcome": "INVALIDATE_EXACT_DEPENDENCY_PROOF",
    }
    if block_overrides:
        block.update(block_overrides)
    body = json.dumps(block, sort_keys=True, ensure_ascii=False, indent=2)
    typed_block = f"```dependency-proof-invalidation-decision-v1\n{body}\n```"
    duplicate_status_text = "\n- Status: `Rejected`\n" if duplicate_status else ""
    content = (
        f"# {decision_id}: Invalidate T-01 dependency proof\n\n"
        f"- Status: `{status}`\n"
        "- Date: 2026-10-03\n"
        "- Deciders: Project owner\n\n"
        "## Context\n\n"
        f"{rationale}\n\n"
        "## Decision\n\n"
        f"{typed_block}\n"
        f"{typed_block + chr(10) if duplicate_block else ''}"
        "\n## Consequences\n\nThe exact proof may be invalidated once.\n"
        + duplicate_status_text
    )
    raw = content.encode("utf-8")
    path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    provenance = f"decision:.planning/decisions/{path.name}@sha256:{digest}"
    return path, provenance


def _invalidation_scope(change_id: str = POSITIVE_CHANGE_ID) -> DependencyProofInvalidationScopeV1:
    return DependencyProofInvalidationScopeV1(
        change_id,
        f"{change_id}/T-01/A1",
        f"{change_id}/T-02/A1",
        "dproof_" + "a" * 64,
    )


def test_decision_provenance_issues_exact_v2_and_rereads_same_item_on_use(tmp_path: Path) -> None:
    target = _governed_target(tmp_path / "consumer")
    scope = _invalidation_scope()
    decision_path, provenance = _write_invalidation_decision(target, scope)
    reference = issue_authorization(
        target,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
        provenance,
    )
    record_path = authorization.authorization_store_path(target) / f"{reference}.json"
    before = record_path.read_bytes()
    record = decode_authorization_record(before)
    assert isinstance(record, AuthorizationRecordV2)
    assert record.scope == scope
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
    ).outcome is ResolutionOutcome.AUTHORIZED

    decision_path.write_text(
        decision_path.read_text(encoding="utf-8").replace(
            "contradictory evidence", "different rationale"
        ),
        encoding="utf-8",
        newline="\n",
    )
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
    ).outcome is ResolutionOutcome.CORRUPT_CONFLICT
    assert record_path.read_bytes() == before


@pytest.mark.parametrize(
    "mutation",
    [
        "free-form provenance",
        "wrong digest",
        "wrong proof tuple",
        "wrong ordinary status",
        "duplicate status",
        "duplicate typed block",
        "wrong decision path",
        "UTF-8 BOM",
        "bare carriage return",
        "duplicate ADR ordinal",
    ],
)
def test_fake_invalidation_provenance_fails_before_authorization_publication(
    tmp_path: Path, mutation: str
) -> None:
    target = _governed_target(tmp_path / "consumer")
    scope = _invalidation_scope()
    overrides = {"proof_id": "dproof_" + "b" * 64} if mutation == "wrong proof tuple" else None
    status = "Draft" if mutation == "wrong ordinary status" else "Accepted"
    path, provenance = _write_invalidation_decision(
        target,
        scope,
        status=status,
        block_overrides=overrides,
        duplicate_block=mutation == "duplicate typed block",
        duplicate_status=mutation == "duplicate status",
    )
    if mutation == "free-form provenance":
        provenance = "owner-decision:plausible-but-not-an-ADR"
    elif mutation == "wrong digest":
        provenance = provenance[:-1] + ("0" if provenance[-1] != "0" else "1")
    elif mutation == "wrong decision path":
        provenance = provenance.replace(".planning/decisions/ADR-0042", ".planning/decisions/INDEX")
    elif mutation == "UTF-8 BOM":
        path.write_bytes(b"\xef\xbb\xbf" + path.read_bytes())
    elif mutation == "bare carriage return":
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r", 1))
    elif mutation == "duplicate ADR ordinal":
        duplicate = path.with_name("ADR-0042-second-invalidation.md")
        duplicate.write_bytes(path.read_bytes())

    with pytest.raises(AuthorizationError):
        issue_authorization(
            target,
            AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
            scope,
            provenance,
        )
    assert not authorization.authorization_store_path(target).exists()


def test_invalidation_authorization_does_not_follow_a_moved_decision_item(tmp_path: Path) -> None:
    target = _governed_target(tmp_path / "consumer")
    scope = _invalidation_scope()
    decision_path, provenance = _write_invalidation_decision(target, scope)
    reference = issue_authorization(
        target,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
        provenance,
    )
    moved = decision_path.with_name("ADR-0042-moved-proof.md")
    decision_path.rename(moved)
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
    ).outcome is ResolutionOutcome.CORRUPT_CONFLICT
    assert moved.is_file()


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate block",
        "duplicate status",
        "wrong tuple",
        "BOM",
        "bare CR",
        "duplicate ADR ordinal",
        "digest-changing rationale",
    ],
)
def test_invalidation_authorization_rejects_nearest_wrong_use_time_item(
    tmp_path: Path, mutation: str
) -> None:
    target = _governed_target(tmp_path / "consumer")
    scope = _invalidation_scope()
    decision_path, provenance = _write_invalidation_decision(target, scope)
    reference = issue_authorization(
        target,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
        provenance,
    )
    record_path = authorization.authorization_store_path(target) / f"{reference}.json"
    record_before = record_path.read_bytes()

    if mutation in {"duplicate block", "duplicate status", "wrong tuple"}:
        _write_invalidation_decision(
            target,
            scope,
            duplicate_block=mutation == "duplicate block",
            duplicate_status=mutation == "duplicate status",
            block_overrides=(
                {"proof_id": "dproof_" + "b" * 64}
                if mutation == "wrong tuple"
                else None
            ),
        )
    elif mutation == "BOM":
        decision_path.write_bytes(b"\xef\xbb\xbf" + decision_path.read_bytes())
    elif mutation == "bare CR":
        decision_path.write_bytes(decision_path.read_bytes().replace(b"\n", b"\r", 1))
    elif mutation == "duplicate ADR ordinal":
        decision_path.with_name("ADR-0042-second-invalidation.md").write_bytes(decision_path.read_bytes())
    else:
        decision_path.write_text(
            decision_path.read_text(encoding="utf-8").replace("contradictory evidence", "rationale changed"),
            encoding="utf-8",
            newline="\n",
        )

    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION,
        scope,
    ).outcome is ResolutionOutcome.CORRUPT_CONFLICT
    assert record_path.read_bytes() == record_before


@pytest.mark.parametrize("value", [" C", "C ", "", "C\nD", "C\rD"])
def test_preparation_negative_identifiers_are_not_trimmed_or_normalized(
    tmp_path: Path, value: str
) -> None:
    target = _target(tmp_path / "consumer")
    with pytest.raises(AuthorizationError):
        issue_preparation_authorization(target, value, "TASK", "PROVENANCE")


def test_v2_record_preserves_unicode_decision_provenance_exactly(tmp_path: Path) -> None:
    target = _governed_target(tmp_path / "consumer")
    reference = issue_preparation_authorization(
        target, POSITIVE_CHANGE_ID, POSITIVE_TASK_ID, "Owner.Ref/β"
    )
    raw = (authorization.authorization_store_path(target) / f"{reference}.json").read_bytes()
    record = decode_authorization_record(raw)
    assert isinstance(record, AuthorizationRecordV2)
    assert record.scope.task_or_operation_id == POSITIVE_TASK_ID
    assert record.decision_provenance_ref == "Owner.Ref/β"
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        record.scope,
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
    target = _governed_target(tmp_path / "consumer")
    reference = issue_preparation_authorization(
        target, POSITIVE_CHANGE_ID, POSITIVE_TASK_ID, "PROVENANCE"
    )
    record = decode_authorization_record(
        (authorization.authorization_store_path(target) / f"{reference}.json").read_bytes()
    )
    assert isinstance(record, AuthorizationRecordV2)
    scope = record.scope
    wrong_change = PreparationScopeV2(
        "CHG-OTHER",
        scope.task_or_operation_id,
        scope.plan_ref,
        scope.tasks_ref,
        scope.approved_plan_digest,
        scope.dependency_semantic_digest,
        scope.requirement_id,
        scope.dependency_classification,
        None,
    )
    wrong_task = PreparationScopeV2(
        scope.change_id,
        "T-09",
        scope.plan_ref,
        scope.tasks_ref,
        scope.approved_plan_digest,
        scope.dependency_semantic_digest,
        scope.requirement_id,
        scope.dependency_classification,
        None,
    )
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        wrong_change,
    ).outcome is ResolutionOutcome.WRONG_SCOPE
    assert resolve_authorization(
        target,
        reference,
        AuthorizationAction.PREPARATION,
        wrong_task,
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
    target = _governed_target(
        tmp_path / "consumer",
        change_id=POSITIVE_CHANGE_ID,
        task_ids=("T-04", "T-05"),
    )
    # Prime only the shared parent so this packet isolates cross-process
    # immutable Authorization allocation; T-02A separately proves first lock
    # creation while both Attempt JSON stores are absent.
    from planning_lite.attempt_runtime import attempt_store_v2_path

    attempt_store_v2_path(target).parent.mkdir(parents=True, exist_ok=True)
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
        POSITIVE_CHANGE_ID,
        "--task-or-operation-id",
        "T-04",
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
        assert isinstance(decoded, AuthorizationRecordV2)
        assert resolve_authorization(
            target,
            path.stem,
            AuthorizationAction.PREPARATION,
            decoded.scope,
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
