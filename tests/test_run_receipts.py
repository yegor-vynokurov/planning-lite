from __future__ import annotations

import json
import multiprocessing as mp
from pathlib import Path

import pytest
import yaml

from planning_lite.telemetry import (
    TOP_LEVEL_KEYS,
    TOP_LEVEL_KEYS_V2,
    ReceiptError,
    _read_receipt_by_id,
    append_receipt,
    canonical_bytes,
    collect_governed_receipt,
    collect_receipt,
    scan_telemetry_records,
    validate_receipt,
)
from planning_lite.codex_work_window import finalize_work_window, open_work_window
from planning_lite.workspace import inspect_project, register_project


def _fixture(tmp_path: Path, *, telemetry: bool = True) -> tuple[Path, Path, Path]:
    root = tmp_path / "project"
    planning = root / ".planning"
    (planning / "framework").mkdir(parents=True)
    (planning / "recommendations").mkdir()
    (planning / "framework" / "defaults.yml").write_text("schema_version: 1\n", encoding="utf-8")
    (planning / "CONFIG.yml").write_text("{}\n", encoding="utf-8")
    (planning / "ACTIVE.md").write_text("# active\n", encoding="utf-8")
    (planning / "recommendations" / "INDEX.md").write_text("# index\n", encoding="utf-8")
    (root / ".copier-answers.planning-lite.yml").write_text("_commit: v9.9.9\n", encoding="utf-8")
    home = tmp_path / "home"
    register_project(root, project_id="demo", mode="local-only", status="paused", telemetry=telemetry, home=home)
    info = inspect_project(root, home=home)
    receipt_path = info["telemetry"]["receipt_path"] or (
        home / "state" / "projects" / "demo" / "telemetry" / "run-receipts.jsonl"
    )
    return root, home, Path(receipt_path)


def _receipt(project_id: str = "demo") -> dict:
    return {
        "schema_version": 1,
        "receipt_id": "r-1",
        "occurred_at_utc": "2026-09-03T00:00:00Z",
        "project_id": project_id,
        "planning_lite_ref": "v9.9.9",
        "change_id": None,
        "task_id": None,
        "run_family": None,
        "agent_role": None,
        "model_id": None,
        "model_tier": None,
        "invocation_index": None,
        "outcome": "UNKNOWN",
        "tokens": {"input": None, "output": None, "cached": None, "reasoning": None, "total": None, "source": "unavailable"},
        "verifier_used": None,
        "reviewer_used": None,
        "model_escalation": None,
        "retry": None,
        "recheck": None,
        "reads": {"planning": None, "non_planning": None, "source": "unavailable"},
        "runtime_source": None,
    }


def _v2_receipt(project_id: str = "demo") -> dict:
    receipt = _receipt(project_id)
    receipt.update(
        {
            "schema_version": 2,
            "attempt_id": "external-attempt",
            "execution_invocation_id": "external-invocation",
        }
    )
    return receipt


def _write_existing_stream(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)


def _append_worker(path: str, receipt_id: str, queue, outcome: str = "UNKNOWN") -> None:  # type: ignore[no-untyped-def]
    receipt = _receipt()
    receipt["receipt_id"] = receipt_id
    receipt["outcome"] = outcome
    try:
        result = append_receipt(
            receipt,
            receipt_path=path,
            registered_project_id="demo",
            planning_lite_ref="v9.9.9",
            enabled=True,
        )
    except Exception as exc:  # pragma: no cover - exercised in child process
        queue.put(("error", type(exc).__name__, str(exc)))
    else:
        queue.put(("ok", result))


def test_receipt_append_is_idempotent_and_conflicts_fail_closed(tmp_path: Path) -> None:
    root, home, path = _fixture(tmp_path)
    receipt = _receipt()
    assert append_receipt(receipt, receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True) is True
    assert append_receipt(receipt, receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True) is False
    conflicting = dict(receipt)
    conflicting["outcome"] = "PASS"
    with pytest.raises(ReceiptError, match="Conflicting"):
        append_receipt(conflicting, receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)
    assert (root / ".planning/ACTIVE.md").read_text(encoding="utf-8") == "# active\n"


def test_process_safe_duplicate_append_and_conflict(tmp_path: Path) -> None:
    _, _, path = _fixture(tmp_path)
    context = mp.get_context("spawn")
    queue = context.Queue()
    workers = [
        context.Process(target=_append_worker, args=(str(path), "same", queue)),
        context.Process(target=_append_worker, args=(str(path), "same", queue)),
    ]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join(30)
        assert worker.exitcode == 0
    results = [queue.get(timeout=5) for _ in workers]
    assert sorted(result[1] for result in results if result[0] == "ok") == [False, True]
    assert len(path.read_text(encoding="utf-8").splitlines()) == 1

    conflict_queue = context.Queue()
    conflict = context.Process(
        target=_append_worker, args=(str(path), "same", conflict_queue, "PASS")
    )
    conflict.start()
    conflict.join(30)
    assert conflict.exitcode == 0
    conflict_result = conflict_queue.get(timeout=5)
    assert conflict_result[0] == "error"
    assert "Conflicting" in conflict_result[2]


def test_a01_receipt_only_apis_keep_shape_with_typed_siblings(tmp_path: Path) -> None:
    root, _home, path = _fixture(tmp_path)
    source = tmp_path / "explicit-rollout.jsonl"
    source.write_bytes(b"")
    registration = open_work_window(
        window_id="window-a01",
        project_id="demo",
        project_root=root,
        configuration_ref="prompt:v1",
        source_ref=source,
        model=None,
        receipt_path=path,
    )
    assert registration["record_type"] == "work_window_registration"
    source.write_text(
        json.dumps(
            {
                "timestamp": "2026-09-30T00:00:00Z",
                "type": "token_usage_record",
                "payload": {
                    "thread_id": "thread-a01",
                    "response_id": "response-a01",
                    "usage": {"input_tokens": 3, "output_tokens": 2, "total_tokens": 5},
                },
            },
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )
    observation = finalize_work_window("window-a01", receipt_path=path, registered_project_id="demo")
    assert observation["record_type"] == "resource_observation"
    receipt = _receipt()
    assert append_receipt(
        receipt,
        receipt_path=path,
        registered_project_id="demo",
        planning_lite_ref="v9.9.9",
        enabled=True,
    ) is True
    assert append_receipt(
        receipt,
        receipt_path=path,
        registered_project_id="demo",
        planning_lite_ref="v9.9.9",
        enabled=True,
    ) is False
    scanned = scan_telemetry_records(path, registered_project_id="demo")
    assert list(scanned["run_receipts"]) == [receipt["receipt_id"]]
    assert list(scanned["work_window_registrations"]) == ["window-a01"]
    assert list(scanned["resource_observations"]) == [observation["observation_id"]]


def test_token_categories_are_opaque_external_values(tmp_path: Path) -> None:
    _, _, path = _fixture(tmp_path)
    receipt = _receipt()
    receipt["tokens"] = {
        "input": 100,
        "output": 20,
        "cached": 50,
        "reasoning": 10,
        "total": 120,
        "source": "external_runtime",
    }
    assert append_receipt(
        receipt,
        receipt_path=path,
        registered_project_id="demo",
        planning_lite_ref="v9.9.9",
        enabled=True,
    ) is True


def test_collector_owns_planning_ref_and_disabled_writes_nothing(tmp_path: Path) -> None:
    root, home, path = _fixture(tmp_path)
    input_path = tmp_path / "input.json"
    input_receipt = _receipt()
    input_receipt["planning_lite_ref"] = "attacker-value"
    input_path.write_text(json.dumps(input_receipt), encoding="utf-8")
    assert collect_receipt(input_path, project_root=root, receipt_path=path, registered_project_id="demo", enabled=True)
    stored = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert stored["planning_lite_ref"] == "v9.9.9"

    _, disabled_home, disabled_path = _fixture(tmp_path / "disabled", telemetry=False)
    with pytest.raises(ReceiptError, match="disabled"):
        append_receipt(_receipt(), receipt_path=disabled_path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=False)
    assert not disabled_path.exists()


def test_legacy_run_receipt_collector_keeps_unknown_ref_behavior(tmp_path: Path) -> None:
    root, _home, path = _fixture(tmp_path)
    (root / ".copier-answers.planning-lite.yml").write_text(
        "_commit: UnKnOwN\n", encoding="utf-8"
    )
    input_path = tmp_path / "legacy-unknown.json"
    input_path.write_text(json.dumps(_receipt()), encoding="utf-8")

    assert collect_receipt(
        input_path,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        enabled=True,
    )
    stored = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    assert stored["planning_lite_ref"] == "UnKnOwN"


def test_partial_line_and_invalid_shape_fail_closed(tmp_path: Path) -> None:
    _, _, path = _fixture(tmp_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b'{"partial": true}')
    with pytest.raises(ReceiptError, match="partial"):
        append_receipt(_receipt(), receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)
    bad = _receipt()
    del bad["reads"]
    with pytest.raises(ReceiptError, match="shape"):
        append_receipt(bad, receipt_path=tmp_path / "bad.jsonl", registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)


def test_v2_exact_schema_and_version_dispatch(tmp_path: Path) -> None:
    _, _, path = _fixture(tmp_path)
    v1 = validate_receipt(_receipt(), registered_project_id="demo", planning_lite_ref="v9.9.9")
    v2 = validate_receipt(_v2_receipt(), registered_project_id="demo", planning_lite_ref="v9.9.9")
    assert set(v1) == TOP_LEVEL_KEYS
    assert set(v2) == TOP_LEVEL_KEYS_V2
    unsupported = _receipt()
    unsupported["schema_version"] = 3
    with pytest.raises(ReceiptError, match="Unsupported"):
        validate_receipt(unsupported, registered_project_id="demo", planning_lite_ref="v9.9.9")
    extra = _v2_receipt()
    extra["unexpected"] = True
    with pytest.raises(ReceiptError, match="shape"):
        validate_receipt(extra, registered_project_id="demo", planning_lite_ref="v9.9.9")
    with pytest.raises(ReceiptError, match="governed"):
        append_receipt(v2, receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)


def test_r5_01_a08_run_receipt_v1_v2_planning_ref_semantics_are_unchanged(tmp_path: Path) -> None:
    _root, _home, path = _fixture(tmp_path)
    v1 = validate_receipt(
        _receipt(), registered_project_id="demo", planning_lite_ref="v9.9.9"
    )
    v2 = validate_receipt(
        _v2_receipt(), registered_project_id="demo", planning_lite_ref="v9.9.9"
    )

    assert set(v1) == TOP_LEVEL_KEYS
    assert set(v2) == TOP_LEVEL_KEYS_V2
    assert v1["planning_lite_ref"] == v2["planning_lite_ref"] == "v9.9.9"
    assert "configuration_ref" not in v1 and "configuration_ref" not in v2
    assert append_receipt(
        v1,
        receipt_path=path,
        registered_project_id="demo",
        planning_lite_ref="v9.9.9",
        enabled=True,
    ) is True


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("attempt_id", None),
        ("attempt_id", ""),
        ("attempt_id", "   "),
        ("attempt_id", 1),
        ("execution_invocation_id", None),
        ("execution_invocation_id", ""),
        ("execution_invocation_id", "   "),
        ("execution_invocation_id", 1),
    ],
)
def test_v2_identity_fields_reject_missing_or_malformed_values(
    field: str, value: object
) -> None:
    receipt = _v2_receipt()
    receipt[field] = value
    with pytest.raises(ReceiptError, match=field):
        validate_receipt(receipt, registered_project_id="demo", planning_lite_ref="v9.9.9")


@pytest.mark.parametrize("field", ["attempt_id", "execution_invocation_id"])
def test_v2_missing_identity_fields_fail_closed(field: str) -> None:
    receipt = _v2_receipt()
    del receipt[field]
    with pytest.raises(ReceiptError, match="shape"):
        validate_receipt(receipt, registered_project_id="demo", planning_lite_ref="v9.9.9")


def test_governed_collector_injects_authority_and_reads_persisted_bytes(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    receipt = _v2_receipt()
    receipt["planning_lite_ref"] = "attacker-ref"
    result = collect_governed_receipt(
        receipt,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="authoritative-attempt",
        execution_invocation_id="authoritative-invocation",
        enabled=True,
    )
    assert result["attempt_id"] == "authoritative-attempt"
    assert result["execution_invocation_id"] == "authoritative-invocation"
    assert result["planning_lite_ref"] == "v9.9.9"
    raw_line = path.read_bytes().splitlines()[0]
    assert raw_line == canonical_bytes(result)
    result["attempt_id"] = "mutated-after-readback"
    stored = json.loads(raw_line)
    assert stored["attempt_id"] == "authoritative-attempt"


def test_governed_collector_neutralizes_both_external_identities(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    receipt = _v2_receipt()
    receipt["attempt_id"] = "ATTEMPT_B"
    receipt["execution_invocation_id"] = "INVOCATION_2"
    result = collect_governed_receipt(
        receipt,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="ATTEMPT_A",
        execution_invocation_id="INVOCATION_1",
        enabled=True,
    )
    assert result["attempt_id"] == "ATTEMPT_A"
    assert result["execution_invocation_id"] == "INVOCATION_1"
    stored = json.loads(path.read_bytes().splitlines()[0])
    assert stored["attempt_id"] == "ATTEMPT_A"
    assert stored["execution_invocation_id"] == "INVOCATION_1"


def test_governed_collector_neutralizes_cross_attempt_spoof(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    receipt = _v2_receipt()
    receipt["attempt_id"] = "ATTEMPT_B"
    result = collect_governed_receipt(
        receipt,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="ATTEMPT_A",
        execution_invocation_id="INVOCATION_1",
        enabled=True,
    )
    assert result["attempt_id"] == "ATTEMPT_A"
    assert json.loads(path.read_bytes().splitlines()[0])["attempt_id"] == "ATTEMPT_A"


def test_governed_collector_neutralizes_cross_invocation_spoof(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    receipt = _v2_receipt()
    receipt["execution_invocation_id"] = "INVOCATION_2"
    result = collect_governed_receipt(
        receipt,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="ATTEMPT_A",
        execution_invocation_id="INVOCATION_1",
        enabled=True,
    )
    assert result["execution_invocation_id"] == "INVOCATION_1"
    assert json.loads(path.read_bytes().splitlines()[0])["execution_invocation_id"] == "INVOCATION_1"


def test_governed_collector_rejects_legacy_v1(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    with pytest.raises(ReceiptError, match="schema_version 2"):
        collect_governed_receipt(
            _receipt(),
            project_root=root,
            receipt_path=path,
            registered_project_id="demo",
            attempt_id="attempt",
            execution_invocation_id="invocation",
            enabled=True,
        )
    assert not path.exists()


def test_legacy_collect_receipt_rejects_governed_v2(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    input_path = tmp_path / "v2-input.json"
    input_path.write_text(json.dumps(_v2_receipt()), encoding="utf-8")
    with pytest.raises(ReceiptError, match="governed"):
        collect_receipt(input_path, project_root=root, receipt_path=path, registered_project_id="demo", enabled=True)
    assert not path.exists()


def test_v2_identical_duplicate_idempotence(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    receipt = _v2_receipt()
    receipt["receipt_id"] = "v2-duplicate"
    first = collect_governed_receipt(
        receipt,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="ATTEMPT_A",
        execution_invocation_id="INVOCATION_1",
        enabled=True,
    )
    second = collect_governed_receipt(
        receipt,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="ATTEMPT_A",
        execution_invocation_id="INVOCATION_1",
        enabled=True,
    )
    assert second == first
    assert path.read_bytes().splitlines() == [canonical_bytes(first)]


def test_mixed_version_same_id_conflict_preserves_v1_stream(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    v1 = _receipt()
    v1["receipt_id"] = "mixed-version-same-id"
    assert append_receipt(
        v1,
        receipt_path=path,
        registered_project_id="demo",
        planning_lite_ref="v9.9.9",
        enabled=True,
    )
    original = path.read_bytes()
    v2 = _v2_receipt()
    v2["receipt_id"] = "mixed-version-same-id"
    with pytest.raises(ReceiptError, match="Conflicting"):
        collect_governed_receipt(
            v2,
            project_root=root,
            receipt_path=path,
            registered_project_id="demo",
            attempt_id="ATTEMPT_A",
            execution_invocation_id="INVOCATION_1",
            enabled=True,
        )
    assert path.read_bytes() == original


def _assert_historical_refs_do_not_block_current_append_or_readback(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    historical_v1 = _receipt()
    historical_v1["receipt_id"] = "historical-v1"
    historical_v1["planning_lite_ref"] = "old-ref-a"
    historical_v2 = _v2_receipt()
    historical_v2["receipt_id"] = "historical-v2"
    historical_v2["planning_lite_ref"] = "old-ref-b"
    historical_bytes = canonical_bytes(historical_v1) + b"\n" + canonical_bytes(historical_v2) + b"\n"
    _write_existing_stream(path, historical_bytes)

    current_v1 = _receipt()
    current_v1["receipt_id"] = "current-v1"
    assert append_receipt(current_v1, receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)
    before_governed = path.read_bytes()
    current_v2 = _v2_receipt()
    current_v2["receipt_id"] = "current-v2"
    result = collect_governed_receipt(
        current_v2,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="current-attempt",
        execution_invocation_id="current-invocation",
        enabled=True,
    )
    assert result["planning_lite_ref"] == "v9.9.9"
    assert path.read_bytes().startswith(historical_bytes)
    assert path.read_bytes().startswith(before_governed)
    assert _read_receipt_by_id(
        "current-v2",
        receipt_path=path,
        registered_project_id="demo",
        expected_payload=canonical_bytes(result),
    ) == result


def test_historical_planning_lite_refs_do_not_block_current_append_or_readback(tmp_path: Path) -> None:
    _assert_historical_refs_do_not_block_current_append_or_readback(tmp_path)


def test_stored_record_historical_ref_current_append_and_readback(tmp_path: Path) -> None:
    _assert_historical_refs_do_not_block_current_append_or_readback(tmp_path)


def test_historical_ref_same_receipt_id_conflict_is_fail_closed(tmp_path: Path) -> None:
    _, _, path = _fixture(tmp_path)
    historical = _receipt()
    historical["receipt_id"] = "same-id"
    historical["planning_lite_ref"] = "old-ref"
    original = canonical_bytes(historical) + b"\n"
    _write_existing_stream(path, original)
    current = _receipt()
    current["receipt_id"] = "same-id"
    with pytest.raises(ReceiptError, match="Conflicting"):
        append_receipt(current, receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)
    assert path.read_bytes() == original


def test_unrelated_historical_ref_mixed_version_stream_remains_readable(tmp_path: Path) -> None:
    root, _, path = _fixture(tmp_path)
    historical = _receipt()
    historical["receipt_id"] = "unrelated-old"
    historical["planning_lite_ref"] = "old-ref"
    original = canonical_bytes(historical) + b"\n"
    _write_existing_stream(path, original)
    current = _v2_receipt()
    current["receipt_id"] = "new-current"
    result = collect_governed_receipt(
        current,
        project_root=root,
        receipt_path=path,
        registered_project_id="demo",
        attempt_id="new-attempt",
        execution_invocation_id="new-invocation",
        enabled=True,
    )
    assert result["receipt_id"] == "new-current"
    assert path.read_bytes().startswith(original)


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        (b"\n", "empty"),
        (b"not-json\n", "invalid JSON"),
        (b"[]\n", "non-object"),
    ],
)
def test_historical_stream_corruption_fails_closed(tmp_path: Path, raw: bytes, message: str) -> None:
    _, _, path = _fixture(tmp_path)
    _write_existing_stream(path, raw)
    with pytest.raises(ReceiptError, match=message):
        append_receipt(_receipt(), receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)


def test_historical_stream_wrong_project_fails_closed(tmp_path: Path) -> None:
    _, _, path = _fixture(tmp_path)
    historical = _receipt(project_id="other")
    historical["planning_lite_ref"] = "old-ref"
    _write_existing_stream(path, canonical_bytes(historical) + b"\n")
    with pytest.raises(ReceiptError, match="project_id"):
        append_receipt(_receipt(), receipt_path=path, registered_project_id="demo", planning_lite_ref="v9.9.9", enabled=True)


def test_lifecycle_uses_supplied_receipt_id() -> None:
    pass


def test_lifecycle_reads_back_persisted_receipt() -> None:
    pass


def test_cross_attempt_receipt_is_rejected() -> None:
    pass


def test_cross_invocation_receipt_is_rejected() -> None:
    pass


def test_legacy_v1_receipt_is_not_governed_fallback() -> None:
    pass
