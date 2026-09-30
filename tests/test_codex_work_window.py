from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path

import pytest

import planning_lite.codex_work_window as work_window
from planning_lite.codex_work_window import finalize_work_window, open_work_window
from planning_lite.telemetry import (
    ReceiptError,
    append_receipt,
    append_resource_observation,
    canonical_bytes,
    read_resource_observation_for_window,
    read_work_window_registration,
    scan_telemetry_records,
    validate_telemetry_record,
)


PROJECT_ID = "window-test"
CONFIGURATION_REF = "prompt:v1"
_NO_METADATA = object()


def _usage(
    response_id: str = "response-1",
    *,
    thread_id: str = "thread-1",
    session_id: str | None = None,
    model: str | None = None,
    usage: dict[str, object] | None = None,
) -> bytes:
    payload = {
        "thread_id": thread_id,
        "session_id": session_id,
        "response_id": response_id,
        "usage": usage
        if usage is not None
        else {"input_tokens": 10, "output_tokens": 5, "total_tokens": 15},
    }
    if model is not None:
        payload["model"] = model
    return (
        json.dumps(
            {
                "timestamp": "2026-09-30T01:02:03Z",
                "type": "token_usage_record",
                "payload": payload,
            },
            separators=(",", ":"),
        ).encode("utf-8")
        + b"\n"
    )


def _open(tmp_path: Path, *, window_id: str = "window-1", prefix: bytes = b"") -> tuple[Path, Path, dict]:
    tmp_path.mkdir(parents=True, exist_ok=True)
    (tmp_path / ".copier-answers.planning-lite.yml").write_text(
        "_commit: v1.0.0\n", encoding="utf-8"
    )
    source = tmp_path / "explicit-rollout.jsonl"
    stream = tmp_path / "run-receipts.jsonl"
    source.write_bytes(prefix)
    registration = open_work_window(
        window_id=window_id,
        project_id=PROJECT_ID,
        project_root=tmp_path,
        configuration_ref=CONFIGURATION_REF,
        source_ref=source,
        model=None,
        receipt_path=stream,
    )
    return source, stream, registration


def _receipt(receipt_id: str) -> dict:
    return {
        "schema_version": 1,
        "receipt_id": receipt_id,
        "occurred_at_utc": "2026-09-30T00:00:00Z",
        "project_id": PROJECT_ID,
        "planning_lite_ref": "v1.0.0",
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


def _finish(source: Path, stream: Path, window_id: str = "window-1") -> dict:
    return finalize_work_window(window_id, receipt_path=stream, registered_project_id=PROJECT_ID)


def test_a02_typed_dispatch_is_strict_and_namespaces_are_separate(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path, window_id="same-id")
    source.write_bytes(_usage())
    observation = _finish(source, stream, "same-id")
    # A syntactically valid bounded quantity proves the carrier can represent a
    # non-complete observed subset without relabeling it as a scope total.
    bounded = json.loads(json.dumps(observation))
    bounded["source_completeness"] = "PARTIAL"
    bounded["quantities"] = {"input_tokens": bounded["quantities"]["input_tokens"]}
    bounded["metric_completeness"]["input_tokens"] = "PARTIAL"
    bounded["quantities"]["input_tokens"] = {
        "value": 10,
        "quality": "BOUNDED",
        "numeric_claim_kind": "EXACT_OBSERVED_SUBSET",
    }
    assert validate_telemetry_record(bounded, registered_project_id=PROJECT_ID)["record_type"] == "resource_observation"
    assert validate_telemetry_record(registration, registered_project_id=PROJECT_ID)["record_type"] == "work_window_registration"

    receipt = _receipt("same-id")
    append_receipt(receipt, receipt_path=stream, registered_project_id=PROJECT_ID, planning_lite_ref="v1.0.0", enabled=True)
    scanned = scan_telemetry_records(stream, registered_project_id=PROJECT_ID)
    assert "same-id" in scanned["run_receipts"]
    assert "same-id" in scanned["work_window_registrations"]
    assert len(scanned["resource_observations"]) == 1

    with pytest.raises(ReceiptError, match="Unknown tagged"):
        validate_telemetry_record({"record_type": "future", "schema_version": 1}, registered_project_id=PROJECT_ID)
    malformed = json.loads(json.dumps(registration))
    malformed["start_offset_bytes"] = True
    with pytest.raises(ReceiptError):
        validate_telemetry_record(malformed, registered_project_id=PROJECT_ID)


def test_a03_registration_survives_fresh_scan_and_readback(tmp_path: Path) -> None:
    _source, stream, registration = _open(tmp_path)
    assert read_work_window_registration("window-1", receipt_path=stream, registered_project_id=PROJECT_ID) == registration
    assert scan_telemetry_records(stream, registered_project_id=PROJECT_ID)["work_window_registrations"]["window-1"] == registration


def test_a04_exact_open_replays_after_growth_and_conflicting_intent_fails(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path)
    source.write_bytes(_usage())
    replay = open_work_window(
        window_id="window-1", project_id=PROJECT_ID, project_root=tmp_path,
        configuration_ref=CONFIGURATION_REF, source_ref=source, model=None, receipt_path=stream,
    )
    assert replay == registration
    with pytest.raises(ReceiptError, match="Conflicting reuse of window_id"):
        open_work_window(
            window_id="window-1", project_id=PROJECT_ID, project_root=tmp_path,
            configuration_ref="prompt:v2", source_ref=source, model=None, receipt_path=stream,
        )


def test_a05_timestamp_or_pre_registration_content_does_not_create_membership(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, prefix=_usage("before-window"))
    result = _finish(source, stream)
    assert result["unavailable_reason"] == "REQUIRED_USAGE_MISSING"
    assert result["source"]["unique_response_count"] == 0
    assert result["quantities"] == {}


@pytest.mark.parametrize("mutation, expected", [
    ("replacement", "SOURCE_IDENTITY_MISMATCH"),
    ("truncation", "SOURCE_REPLACED_OR_TRUNCATED"),
    ("anchor", "SOURCE_REPLACED_OR_TRUNCATED"),
])
def test_a06_source_identity_truncation_and_anchor_conflicts_fail_closed(
    tmp_path: Path, mutation: str, expected: str
) -> None:
    source, stream, _ = _open(
        tmp_path,
        prefix=b'{"timestamp":"2026-09-30T01:02:03Z","type":"session_meta","payload":{"id":"before"}}\n',
    )
    if mutation == "replacement":
        replacement = tmp_path / "replacement.jsonl"
        replacement.write_bytes(source.read_bytes() + _usage())
        os.replace(replacement, source)
    elif mutation == "truncation":
        source.write_bytes(b"")
    else:
        changed = bytearray(source.read_bytes())
        changed[-2] = ord("X")
        source.write_bytes(changed)
        source.write_bytes(source.read_bytes() + _usage())
    result = _finish(source, stream)
    assert result["unavailable_reason"] == expected
    assert result["quantities"] == {}
    assert result["scope"]["end_offset_bytes"] == len(source.read_bytes())
    assert result["source"]["segment_sha256"] is None


def test_a07_partial_tail_and_unstable_reads_are_not_finalized(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source, stream, _ = _open(tmp_path)
    row = _usage().rstrip(b"\n")
    source.write_bytes(row)
    pending = _finish(source, stream)
    assert pending["status"] == "REQUEST_NOT_YET_FINALIZABLE"
    assert read_resource_observation_for_window("window-1", receipt_path=stream, registered_project_id=PROJECT_ID) is None
    with source.open("ab") as handle:
        handle.write(b"\n")
    assert _finish(source, stream)["unavailable_reason"] is None

    other_source, other_stream, _ = _open(tmp_path / "other", window_id="window-unstable")
    other_source.write_bytes(_usage())
    calls = 0

    def unstable(*_args: object, **_kwargs: object) -> tuple[str, list[dict], str | None]:
        nonlocal calls
        calls += 1
        raise work_window._PendingRead("SOURCE_READ_UNSTABLE")

    monkeypatch.setattr(work_window, "_read_bounded", unstable)
    pending_again = finalize_work_window("window-unstable", receipt_path=other_stream, registered_project_id=PROJECT_ID)
    assert pending_again["status"] == "REQUEST_NOT_YET_FINALIZABLE"
    assert calls == 2
    assert read_resource_observation_for_window("window-unstable", receipt_path=other_stream, registered_project_id=PROJECT_ID) is None


def test_a08_exact_segment_aggregates_structured_usage_and_ignores_content_payloads(tmp_path: Path) -> None:
    source, stream, _ = _open(
        tmp_path,
        prefix=b'{"timestamp":"2026-09-30T01:02:03Z","type":"session_meta","payload":{"id":"old"}}\n',
    )
    source.write_bytes(source.read_bytes() + b'{"timestamp":"2026-09-30T01:02:03Z","type":"response_item","payload":{"type":"assistant_message","text":"SENTINEL"}}\n')
    source.write_bytes(source.read_bytes() + b'{"timestamp":"2026-09-30T01:02:03Z","type":"event_msg","payload":{"type":"token_count","info":{"total_token_count":999}}}\n')
    source.write_bytes(source.read_bytes() + _usage("r1", usage={"input_tokens": 4, "output_tokens": 2, "total_tokens": 6}))
    source.write_bytes(source.read_bytes() + _usage("r2", usage={"input_tokens": 6, "output_tokens": 3, "total_tokens": 9}))
    result = _finish(source, stream)
    assert result["quantities"]["input_tokens"]["value"] == 10
    assert result["quantities"]["output_tokens"]["value"] == 5
    assert result["quantities"]["total_tokens"]["value"] == 15
    assert "SENTINEL" not in json.dumps(result)


def test_a09_identical_response_duplicates_count_once_and_conflicts_are_unavailable(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    row = _usage("same")
    source.write_bytes(row + row)
    result = _finish(source, stream)
    assert result["source"]["unique_response_count"] == 1
    assert result["quantities"]["total_tokens"]["value"] == 15

    source2, stream2, _ = _open(tmp_path / "conflict", window_id="conflict")
    source2.write_bytes(row + _usage("same", usage={"input_tokens": 11, "output_tokens": 5, "total_tokens": 16}))
    conflict = finalize_work_window("conflict", receipt_path=stream2, registered_project_id=PROJECT_ID)
    assert conflict["unavailable_reason"] == "DUPLICATE_USAGE_CONFLICT"
    assert conflict["quantities"] == {}


def test_a10_absent_optional_metrics_are_not_fabricated_as_zero(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage(usage={"input_tokens": 0, "output_tokens": 2, "total_tokens": 2}))
    result = _finish(source, stream)
    assert result["quantities"]["input_tokens"]["value"] == 0
    for metric in ("cached_input_tokens", "reasoning_output_tokens"):
        assert metric not in result["quantities"]
        assert result["metric_completeness"][metric] == "ABSENT"


def test_a11_complete_supported_metrics_are_direct_scope_totals(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage(usage={
        "input_tokens": 10, "cached_input_tokens": 2, "output_tokens": 7,
        "reasoning_output_tokens": 3, "total_tokens": 17,
    }))
    result = _finish(source, stream)
    assert set(result["quantities"]) == {
        "input_tokens", "cached_input_tokens", "output_tokens", "reasoning_output_tokens", "total_tokens",
    }
    assert all(q["quality"] == "DIRECT" and q["numeric_claim_kind"] == "COMPLETE_SCOPE_TOTAL" for q in result["quantities"].values())


def test_a12_observation_needs_no_attempt_bridge(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage())
    result = _finish(source, stream)
    assert not any("attempt" in key.lower() or "turn_to_attempt" in key.lower() for key in result)
    assert result["scope"]["kind"] == "WORK_WINDOW"


def test_a13_identical_terminal_replay_returns_exact_persisted_bytes(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage())
    first = _finish(source, stream)
    before = stream.read_bytes()
    second = _finish(source, stream)
    assert second == first
    assert stream.read_bytes() == before
    assert len(scan_telemetry_records(stream, registered_project_id=PROJECT_ID)["resource_observations"]) == 1


def test_a14_conflicting_terminal_replay_has_stable_conflict(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage())
    result = _finish(source, stream)
    conflict = json.loads(json.dumps(result))
    conflict["quantities"]["input_tokens"]["value"] += 1
    with pytest.raises(ReceiptError, match="WINDOW_ALREADY_FINALIZED_CONFLICT"):
        append_resource_observation(conflict, receipt_path=stream, registered_project_id=PROJECT_ID)


def test_a15_canonical_readback_matches_the_persisted_semantic_record(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage())
    result = _finish(source, stream)
    row = next(line for line in stream.read_bytes().splitlines() if b"resource_observation" in line)
    assert row == canonical_bytes(result)
    assert json.loads(row) == result


def test_a16_preopen_bytes_and_growth_after_captured_end_are_excluded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    source, stream, _ = _open(tmp_path, prefix=_usage("pre-open"))
    source.write_bytes(source.read_bytes() + _usage("included"))
    original = work_window._read_bounded
    appended = False

    def grow_after_end(handle: object, *, start_offset: int, end_offset: int, parse: bool):
        nonlocal appended
        if not appended:
            appended = True
            with source.open("ab") as output:
                output.write(_usage("after-end"))
        return original(handle, start_offset=start_offset, end_offset=end_offset, parse=parse)  # type: ignore[arg-type]

    monkeypatch.setattr(work_window, "_read_bounded", grow_after_end)
    result = _finish(source, stream)
    assert result["source"]["unique_response_count"] == 1
    assert result["source"]["thread_id"] == "thread-1"
    assert result["scope"]["start_offset_bytes"] == len(_usage("pre-open"))
    assert result["scope"]["end_offset_bytes"] == len(_usage("pre-open")) + len(_usage("included"))


def test_a17_result_stays_provider_native_and_has_no_comparison_output(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage())
    result = _finish(source, stream)
    serialized = json.dumps(result).lower()
    assert result["provider"] == "codex"
    assert result["native_quantity_semantics"] == "CODEX_TOKEN_USAGE_RECORD_USAGE_V1"
    assert not any(word in serialized for word in ("efficiency", "winner", "normalized", "api_call", "09-g"))


@pytest.mark.parametrize("usage, expected", [
    ({"input_tokens": True, "output_tokens": 1, "total_tokens": 2}, "USAGE_RECORD_INVALID"),
    ({"input_tokens": 2, "output_tokens": 1, "total_tokens": 9}, "AGGREGATE_RECONCILIATION_FAILED"),
    ({"input_tokens": 2, "output_tokens": 1, "total_tokens": 3, "cache_write_input_tokens": 1}, "USAGE_RECORD_INVALID"),
])
def test_a18_terminal_bad_usage_is_one_unavailable_nonzero_claim_free_observation(
    tmp_path: Path, usage: dict[str, object], expected: str
) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(_usage(usage=usage))
    result = _finish(source, stream)
    assert result["unavailable_reason"] == expected
    assert result["quantities"] == {}
    assert result["scope"]["end_offset_bytes"] == len(source.read_bytes())
    assert result["source"]["segment_sha256"] is not None
    assert len(scan_telemetry_records(stream, registered_project_id=PROJECT_ID)["resource_observations"]) == 1


def test_a18_missing_usage_is_unavailable_not_measured_zero(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path)
    source.write_bytes(
        b'{"timestamp":"2026-09-30T01:02:03Z","type":"response_item","payload":{"type":"assistant_message","text":"not usage"}}\n'
    )
    result = _finish(source, stream)
    assert result["unavailable_reason"] == "REQUIRED_USAGE_MISSING"
    assert result["quantities"] == {}
    assert result["source"]["segment_sha256"] is not None


def test_a19_concurrent_open_finalize_and_receipt_writes_keep_unique_rows(tmp_path: Path) -> None:
    source = tmp_path / "rollout.jsonl"
    stream = tmp_path / "run-receipts.jsonl"
    (tmp_path / ".copier-answers.planning-lite.yml").write_text(
        "_commit: v1.0.0\n", encoding="utf-8"
    )
    source.write_bytes(b"")

    def open_same() -> dict:
        return open_work_window(
            window_id="concurrent", project_id=PROJECT_ID, project_root=tmp_path,
            configuration_ref=CONFIGURATION_REF, source_ref=source, model=None, receipt_path=stream,
        )

    with ThreadPoolExecutor(max_workers=4) as pool:
        registrations = list(pool.map(lambda _index: open_same(), range(4)))
    assert all(row == registrations[0] for row in registrations)
    source.write_bytes(_usage())

    def finalize() -> dict:
        return finalize_work_window("concurrent", receipt_path=stream, registered_project_id=PROJECT_ID)

    def append_run_receipt() -> bool:
        return append_receipt(
            _receipt("receipt-concurrent"), receipt_path=stream,
            registered_project_id=PROJECT_ID, planning_lite_ref="v1.0.0", enabled=True,
        )

    with ThreadPoolExecutor(max_workers=4) as pool:
        futures = [pool.submit(finalize), pool.submit(finalize), pool.submit(append_run_receipt)]
        observations = [futures[0].result(), futures[1].result()]
        receipt_results = futures[2].result()
    assert observations[0] == observations[1]
    assert receipt_results is True
    scanned = scan_telemetry_records(stream, registered_project_id=PROJECT_ID)
    assert len(scanned["work_window_registrations"]) == 1
    assert len(scanned["resource_observations"]) == 1
    assert len(scanned["run_receipts"]) == 1


def test_r5_01_a01_commit_ref_is_persisted_separately_from_configuration_ref(tmp_path: Path) -> None:
    _source, _stream, registration = _open(tmp_path, window_id="r5-01-a01")

    assert registration["planning_lite_ref"] == "v1.0.0"
    assert registration["configuration_ref"] == CONFIGURATION_REF
    assert registration["planning_lite_ref"] != registration["configuration_ref"]


def test_r5_01_a02_vcs_ref_is_used_when_commit_is_absent_or_unusable(tmp_path: Path) -> None:
    source = tmp_path / "source.jsonl"
    source.write_bytes(b"")
    answers = tmp_path / ".copier-answers.planning-lite.yml"
    stream = tmp_path / "receipts.jsonl"

    answers.write_text("_vcs_ref: release-2\n", encoding="utf-8")
    from_absent_commit = open_work_window(
        window_id="r5-01-a02a",
        project_id=PROJECT_ID,
        project_root=tmp_path,
        configuration_ref=CONFIGURATION_REF,
        source_ref=source,
        model=None,
        receipt_path=stream,
    )
    assert from_absent_commit["planning_lite_ref"] == "release-2"

    answers.write_text("_commit: '   '\n_vcs_ref: release-3\n", encoding="utf-8")
    from_unusable_commit = open_work_window(
        window_id="r5-01-a02b",
        project_id=PROJECT_ID,
        project_root=tmp_path,
        configuration_ref=CONFIGURATION_REF,
        source_ref=source,
        model=None,
        receipt_path=stream,
    )
    assert from_unusable_commit["planning_lite_ref"] == "release-3"


def test_r5_01_a03_observation_copies_the_registered_ref(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path, window_id="r5-01-a03")
    source.write_bytes(_usage())

    observation = _finish(source, stream, "r5-01-a03")

    assert observation["planning_lite_ref"] == registration["planning_lite_ref"]


def test_r5_01_a04_finalize_keeps_ref_registered_before_installation_update(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path, window_id="r5-01-a04")
    (tmp_path / ".copier-answers.planning-lite.yml").write_text(
        "_commit: v2.0.0\n", encoding="utf-8"
    )
    source.write_bytes(_usage())

    observation = _finish(source, stream, "r5-01-a04")

    assert registration["planning_lite_ref"] == "v1.0.0"
    assert observation["planning_lite_ref"] == "v1.0.0"


def test_r5_01_a05_same_ref_open_replay_is_idempotent_and_keeps_start(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path, window_id="r5-01-a05")
    source.write_bytes(_usage())

    replay = open_work_window(
        window_id="r5-01-a05",
        project_id=PROJECT_ID,
        project_root=tmp_path,
        configuration_ref=CONFIGURATION_REF,
        source_ref=source,
        model=None,
        receipt_path=stream,
    )

    assert replay == registration
    assert replay["start_offset_bytes"] == 0


def test_r5_01_a06_changed_ref_conflicts_and_preserves_first_registration(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path, window_id="r5-01-a06")
    source.write_bytes(_usage())
    (tmp_path / ".copier-answers.planning-lite.yml").write_text(
        "_commit: v2.0.0\n", encoding="utf-8"
    )

    with pytest.raises(ReceiptError, match="Conflicting reuse of window_id"):
        open_work_window(
            window_id="r5-01-a06",
            project_id=PROJECT_ID,
            project_root=tmp_path,
            configuration_ref=CONFIGURATION_REF,
            source_ref=source,
            model=None,
            receipt_path=stream,
        )

    stored = read_work_window_registration(
        "r5-01-a06", receipt_path=stream, registered_project_id=PROJECT_ID
    )
    assert stored["planning_lite_ref"] == "v1.0.0"
    assert stored["start_offset_bytes"] == registration["start_offset_bytes"] == 0


def test_r5_01_a07_bad_install_ref_fails_before_source_access_or_telemetry(tmp_path: Path) -> None:
    scenarios = (("missing", None), ("unusable", "_commit: '  '\n_vcs_ref: ''\n"))
    for name, answers_content in scenarios:
        root = tmp_path / name
        root.mkdir()
        answers = root / ".copier-answers.planning-lite.yml"
        if answers_content is not None:
            answers.write_text(answers_content, encoding="utf-8")
        source = root / "does-not-exist-poison-source.jsonl"
        stream = root / "telemetry" / "receipts.jsonl"

        with pytest.raises(ReceiptError, match="Copier answers|installed ref"):
            open_work_window(
                window_id=f"r5-01-a07-{name}",
                project_id=PROJECT_ID,
                project_root=root,
                configuration_ref=CONFIGURATION_REF,
                source_ref=source,
                model=None,
                receipt_path=stream,
            )

        assert not source.exists()
        assert not stream.exists()


def test_r5_01_a09_typed_validators_require_well_formed_planning_ref(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path, window_id="r5-01-a09")
    source.write_bytes(_usage())
    observation = _finish(source, stream, "r5-01-a09")

    for record in (registration, observation):
        missing = dict(record)
        del missing["planning_lite_ref"]
        with pytest.raises(ReceiptError, match="shape mismatch"):
            validate_telemetry_record(missing, registered_project_id=PROJECT_ID)
        malformed = dict(record)
        malformed["planning_lite_ref"] = "  "
        with pytest.raises(ReceiptError, match="planning_lite_ref"):
            validate_telemetry_record(malformed, registered_project_id=PROJECT_ID)


def test_r5_01_a10_observation_ref_must_match_persisted_registration(tmp_path: Path) -> None:
    source, stream, registration = _open(tmp_path, window_id="r5-01-a10")
    source.write_bytes(_usage())
    observation = _finish(source, stream, "r5-01-a10")
    conflicting = dict(observation)
    conflicting["planning_lite_ref"] = "different-installed-ref"

    with pytest.raises(ReceiptError, match="registration binding mismatch"):
        append_resource_observation(
            conflicting, receipt_path=stream, registered_project_id=PROJECT_ID
        )

    stored = read_resource_observation_for_window(
        "r5-01-a10", receipt_path=stream, registered_project_id=PROJECT_ID
    )
    assert stored is not None
    assert stored["planning_lite_ref"] == registration["planning_lite_ref"]


def _opaque_line(record_type: str, payload: str) -> bytes:
    return (
        '{"timestamp":"2026-09-30T01:02:03Z","type":'
        + json.dumps(record_type)
        + ',"payload":'
        + payload
        + "}\n"
    ).encode("utf-8")


def _envelope_line(
    record_type: str,
    payload: dict[str, object],
    *,
    metadata: object = _NO_METADATA,
    extra_top_level: dict[str, object] | None = None,
) -> bytes:
    record: dict[str, object] = {
        "timestamp": "2026-09-30T01:02:03Z",
        "type": record_type,
        "payload": payload,
    }
    if metadata is not _NO_METADATA:
        record["metadata"] = metadata
    if extra_top_level:
        record.update(extra_top_level)
    return json.dumps(record, separators=(",", ":")).encode("utf-8") + b"\n"


def test_r5_02_a01_incomplete_response_item_cannot_support_direct_usage(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a01")
    source.write_bytes(b'{"type":"response_item"}\n' + _usage())

    result = _finish(source, stream, "r5-02-a01")

    assert result["source_completeness"] == "UNAVAILABLE"
    assert result["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert result["quantities"] == {}
    assert len(scan_telemetry_records(stream, registered_project_id=PROJECT_ID)["resource_observations"]) == 1


def test_r5_02_a02_invalid_json_scalar_is_not_opaque_skipped(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a02")
    source.write_bytes(_opaque_line("response_item", '{"body":not_json}') + _usage())

    result = _finish(source, stream, "r5-02-a02")

    assert result["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert result["quantities"] == {}


def test_r5_02_a03_unknown_top_level_type_fails_closed(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a03")
    source.write_bytes(_opaque_line("future_record", "{}") + _usage())

    result = _finish(source, stream, "r5-02-a03")

    assert result["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert result["quantities"] == {}


def test_r5_02_a04_unknown_event_discriminator_fails_closed(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a04")
    source.write_bytes(_opaque_line("event_msg", '{"type":"future_event","body":"opaque"}') + _usage())

    result = _finish(source, stream, "r5-02-a04")

    assert result["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert result["quantities"] == {}


def test_r5_02_a05_known_opaque_event_is_accepted_without_body_use(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a05")
    secret = "EVENT_BODY_MUST_STAY_OPAQUE_517"
    source.write_bytes(
        _opaque_line("event_msg", json.dumps({"type": "user_message", "message": secret}))
        + _usage()
    )

    result = _finish(source, stream, "r5-02-a05")

    assert result["source_completeness"] == "COMPLETE"
    assert result["quantities"]["total_tokens"]["value"] == 15
    assert secret not in json.dumps(result)


def test_r5_02_a06_known_opaque_top_level_envelope_is_accepted(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a06")
    secret = "TOP_LEVEL_BODY_MUST_STAY_OPAQUE_528"
    payload = json.dumps({"type": "assistant_message", "content": [{"text": secret}]})
    source.write_bytes(_opaque_line("response_item", payload) + _usage())

    result = _finish(source, stream, "r5-02-a06")

    assert result["source_completeness"] == "COMPLETE"
    assert result["quantities"]["total_tokens"]["value"] == 15
    assert secret not in json.dumps(result)


def test_r5_02_a07_duplicate_structural_keys_fail_closed(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a07")
    duplicate = (
        b'{"timestamp":"2026-09-30T01:02:03Z","type":"response_item",'
        b'"payload":{"body":"one","body":"two"}}\n'
    )
    source.write_bytes(duplicate + _usage())

    result = _finish(source, stream, "r5-02-a07")

    assert result["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert result["quantities"] == {}


def test_r5_02_a08_usage_record_aggregation_is_unchanged(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a08")
    source.write_bytes(
        _usage("r5-a", usage={"input_tokens": 4, "output_tokens": 2, "total_tokens": 6})
        + _usage("r5-b", usage={"input_tokens": 6, "output_tokens": 3, "total_tokens": 9})
    )

    result = _finish(source, stream, "r5-02-a08")

    assert result["source"]["unique_response_count"] == 2
    assert result["quantities"]["input_tokens"]["value"] == 10
    assert result["quantities"]["output_tokens"]["value"] == 5
    assert result["quantities"]["total_tokens"]["value"] == 15


def test_r5_02_a09_duplicate_response_semantics_are_unchanged(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a09-same")
    row = _usage("duplicate")
    source.write_bytes(row + row)
    identical = _finish(source, stream, "r5-02-a09-same")
    assert identical["source"]["unique_response_count"] == 1
    assert identical["quantities"]["total_tokens"]["value"] == 15

    source2, stream2, _ = _open(tmp_path / "conflict", window_id="r5-02-a09-conflict")
    source2.write_bytes(
        row + _usage("duplicate", usage={"input_tokens": 11, "output_tokens": 5, "total_tokens": 16})
    )
    conflict = _finish(source2, stream2, "r5-02-a09-conflict")
    assert conflict["unavailable_reason"] == "DUPLICATE_USAGE_CONFLICT"
    assert conflict["quantities"] == {}


def test_r5_02_a10_optional_metrics_and_arithmetic_reconciliation_are_unchanged(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a10-optional")
    source.write_bytes(_usage(usage={"input_tokens": 2, "output_tokens": 1, "total_tokens": 3}))
    optional = _finish(source, stream, "r5-02-a10-optional")
    assert "cached_input_tokens" not in optional["quantities"]
    assert optional["metric_completeness"]["cached_input_tokens"] == "ABSENT"

    source2, stream2, _ = _open(tmp_path / "arithmetic", window_id="r5-02-a10-arithmetic")
    source2.write_bytes(_usage(usage={"input_tokens": 2, "output_tokens": 1, "total_tokens": 9}))
    mismatch = _finish(source2, stream2, "r5-02-a10-arithmetic")
    assert mismatch["unavailable_reason"] == "AGGREGATE_RECONCILIATION_FAILED"
    assert mismatch["quantities"] == {}


def test_r5_02_a11_partial_tail_remains_pending_without_observation(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a11")
    source.write_bytes(_usage().rstrip(b"\n"))

    result = _finish(source, stream, "r5-02-a11")

    assert result["status"] == "REQUEST_NOT_YET_FINALIZABLE"
    assert read_resource_observation_for_window(
        "r5-02-a11", receipt_path=stream, registered_project_id=PROJECT_ID
    ) is None
    assert len(stream.read_bytes().splitlines()) == 1


def test_r5_02_a12_stable_malformed_envelope_is_terminal_and_persisted_once(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5-02-a12")
    source.write_bytes(_opaque_line("response_item", '{"text":}') + _usage())

    first = _finish(source, stream, "r5-02-a12")
    second = _finish(source, stream, "r5-02-a12")

    assert first["source_completeness"] == "UNAVAILABLE"
    assert first["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert first["quantities"] == {}
    assert second == first
    assert len(scan_telemetry_records(stream, registered_project_id=PROJECT_ID)["resource_observations"]) == 1
    assert len(stream.read_bytes().splitlines()) == 2


@pytest.mark.parametrize(
    "answers",
    [
        "_commit: unknown\n",
        "_vcs_ref: ' UNKNOWN '\n",
    ],
    ids=["unknown-commit", "unknown-vcs-ref"],
)
def test_r5r_01_a01_unknown_installed_ref_fails_before_source_or_telemetry(
    tmp_path: Path, answers: str
) -> None:
    root = tmp_path / "target"
    root.mkdir()
    (root / ".copier-answers.planning-lite.yml").write_text(answers, encoding="utf-8")
    source = root / "source-must-not-be-inspected.jsonl"
    stream = root / "telemetry" / "receipts.jsonl"

    with pytest.raises(ReceiptError, match="usable installed ref"):
        open_work_window(
            window_id="r5r-01-a01",
            project_id=PROJECT_ID,
            project_root=root,
            configuration_ref=CONFIGURATION_REF,
            source_ref=source,
            model=None,
            receipt_path=stream,
        )

    assert not source.exists()
    assert not stream.exists()


@pytest.mark.parametrize("commit", ["UNKNOWN", " UnKnOwN ", "unknown"], ids=["upper", "trimmed-mixed", "lower"])
def test_r5r_01_a02_unknown_commit_falls_back_and_never_persists_unknown(
    tmp_path: Path, commit: str
) -> None:
    answers = tmp_path / ".copier-answers.planning-lite.yml"
    answers.write_text(f"_commit: '{commit}'\n_vcs_ref: release-4\n", encoding="utf-8")
    source = tmp_path / "source.jsonl"
    source.write_bytes(b"")
    stream = tmp_path / "receipts.jsonl"

    registration = open_work_window(
        window_id=f"r5r-01-a02-{commit.strip().casefold()}",
        project_id=PROJECT_ID,
        project_root=tmp_path,
        configuration_ref=CONFIGURATION_REF,
        source_ref=source,
        model=None,
        receipt_path=stream,
    )
    assert registration["planning_lite_ref"] == "release-4"
    source.write_bytes(_usage())
    observation = _finish(source, stream, registration["window_id"])

    assert observation["planning_lite_ref"] == "release-4"
    persisted = [json.loads(line) for line in stream.read_text(encoding="utf-8").splitlines()]
    assert all(record["planning_lite_ref"].casefold() != "unknown" for record in persisted)
    for record in (registration, observation):
        malformed = dict(record)
        malformed["planning_lite_ref"] = "UnKnOwN"
        with pytest.raises(ReceiptError, match="known installed project ref"):
            validate_telemetry_record(malformed, registered_project_id=PROJECT_ID)


@pytest.mark.parametrize("record_type", ["session_meta", "turn_context", "response_item"])
def test_r5r_02_a01_empty_known_payload_shell_fails_closed(
    tmp_path: Path, record_type: str
) -> None:
    source, stream, _ = _open(tmp_path, window_id=f"r5r-02-empty-{record_type}")
    source.write_bytes(_opaque_line(record_type, "{}") + _usage())

    observation = _finish(source, stream, f"r5r-02-empty-{record_type}")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}


def test_r5r_02_a02_current_session_meta_is_accepted_and_binds_usage(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5r-02-session-meta")
    session_id = "current-session-02"
    meta = {"id": session_id, "session_id": session_id, "parent_thread_id": "opaque-parent"}
    source.write_bytes(_opaque_line("session_meta", json.dumps(meta)) + _usage(session_id=session_id))

    observation = _finish(source, stream, "r5r-02-session-meta")

    assert observation["source_completeness"] == "COMPLETE"
    assert observation["unavailable_reason"] is None
    assert observation["quantities"]["total_tokens"]["value"] == 15


def test_r5r_02_a03_current_turn_context_is_accepted_and_binds_model_and_session(
    tmp_path: Path,
) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5r-02-turn-context")
    context = {
        "session_id": "current-session-03",
        "turn_id": "current-turn-03",
        "model": "gpt-5.6-sol",
        "effort": "medium",
        "root_turn_id": "root-turn-03",
    }
    source.write_bytes(
        _opaque_line("turn_context", json.dumps(context))
        + _usage(session_id="current-session-03", model="gpt-5.6-sol")
    )

    observation = _finish(source, stream, "r5r-02-turn-context")

    assert observation["source_completeness"] == "COMPLETE"
    assert observation["model"] == "gpt-5.6-sol"
    assert observation["quantities"]["total_tokens"]["value"] == 15


@pytest.mark.parametrize(
    ("context_session", "context_model", "usage_session", "usage_model", "reason"),
    [
        ("other-session", "gpt-5.6-sol", "current-session", "gpt-5.6-sol", "MEMBERSHIP_BINDING_MISMATCH"),
        ("current-session", "other-model", "current-session", "gpt-5.6-sol", "CONFIGURATION_BINDING_MISMATCH"),
    ],
    ids=["session-conflict", "model-conflict"],
)
def test_r5r_02_a04_turn_context_conflicts_fail_closed(
    tmp_path: Path,
    context_session: str,
    context_model: str,
    usage_session: str,
    usage_model: str,
    reason: str,
) -> None:
    source, stream, _ = _open(tmp_path, window_id=f"r5r-02-context-{reason}")
    context = {
        "session_id": context_session,
        "turn_id": "current-turn-04",
        "model": context_model,
    }
    source.write_bytes(
        _opaque_line("turn_context", json.dumps(context))
        + _usage(session_id=usage_session, model=usage_model)
    )

    observation = _finish(source, stream, f"r5r-02-context-{reason}")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == reason
    assert observation["quantities"] == {}


def test_r5r_02_a05_current_response_item_discriminator_keeps_body_opaque(
    tmp_path: Path,
) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5r-02-response-item")
    secret = "RESPONSE_BODY_STAYS_OPAQUE_R5R"
    payload = {"type": "assistant_message", "content": [{"text": secret}]}
    source.write_bytes(_opaque_line("response_item", json.dumps(payload)) + _usage())

    observation = _finish(source, stream, "r5r-02-response-item")

    assert observation["source_completeness"] == "COMPLETE"
    assert observation["quantities"]["total_tokens"]["value"] == 15
    assert secret not in json.dumps(observation)
    assert secret.encode() not in stream.read_bytes()


@pytest.mark.parametrize("item_type", ["reasoning", "custom_tool_call", "message"])
def test_t06_rs01_evidenced_response_items_are_known_non_usage(
    tmp_path: Path, item_type: str
) -> None:
    source, stream, _ = _open(tmp_path, window_id=f"t06-rs01-{item_type}")
    source.write_bytes(
        _opaque_line("response_item", json.dumps({"type": item_type})) + _usage()
    )

    observation = _finish(source, stream, f"t06-rs01-{item_type}")

    assert observation["source_completeness"] == "COMPLETE"
    assert observation["unavailable_reason"] is None
    assert observation["source"]["unique_response_count"] == 1
    assert observation["quantities"]["total_tokens"]["quality"] == "DIRECT"
    assert observation["quantities"]["total_tokens"]["numeric_claim_kind"] == "COMPLETE_SCOPE_TOTAL"


def test_t06_rs01_custom_tool_call_output_accepts_object_metadata(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="t06-rs01-object-metadata")
    source.write_bytes(
        _envelope_line(
            "response_item",
            {"type": "custom_tool_call_output"},
            metadata={"opaque_marker": "not interpreted"},
        )
        + _usage()
    )

    observation = _finish(source, stream, "t06-rs01-object-metadata")

    assert observation["source_completeness"] == "COMPLETE"
    assert observation["source"]["unique_response_count"] == 1


@pytest.mark.parametrize(
    "metadata",
    [None, [], "unsupported", 7, True],
    ids=["null", "array", "string", "number", "boolean"],
)
def test_t06_rs01_metadata_requires_evidenced_object_kind(
    tmp_path: Path, metadata: object
) -> None:
    source, stream, _ = _open(tmp_path, window_id="t06-rs01-bad-metadata")
    source.write_bytes(
        _envelope_line(
            "response_item", {"type": "custom_tool_call_output"}, metadata=metadata
        )
        + _usage()
    )

    observation = _finish(source, stream, "t06-rs01-bad-metadata")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}


def test_t06_rs01_unknown_top_level_field_remains_fail_closed(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="t06-rs01-extra-envelope-field")
    source.write_bytes(
        _envelope_line(
            "response_item",
            {"type": "custom_tool_call_output"},
            metadata={},
            extra_top_level={"unrecognized": True},
        )
        + _usage()
    )

    observation = _finish(source, stream, "t06-rs01-extra-envelope-field")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}


def test_t06_rs01_unknown_response_item_discriminator_remains_fail_closed(
    tmp_path: Path,
) -> None:
    source, stream, _ = _open(tmp_path, window_id="t06-rs01-unknown-response-item")
    source.write_bytes(
        _opaque_line("response_item", json.dumps({"type": "future_item"})) + _usage()
    )

    observation = _finish(source, stream, "t06-rs01-unknown-response-item")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}


def test_t06_rs01_agent_message_is_known_non_usage_and_unknown_event_stays_rejected(
    tmp_path: Path,
) -> None:
    source, stream, _ = _open(tmp_path, window_id="t06-rs01-agent-message")
    source.write_bytes(
        _opaque_line("event_msg", json.dumps({"type": "agent_message"})) + _usage()
    )

    accepted = _finish(source, stream, "t06-rs01-agent-message")

    assert accepted["source_completeness"] == "COMPLETE"
    assert accepted["source"]["unique_response_count"] == 1

    source2, stream2, _ = _open(tmp_path / "unknown", window_id="t06-rs01-unknown-event")
    source2.write_bytes(
        _opaque_line("event_msg", json.dumps({"type": "future_event"})) + _usage()
    )

    rejected = _finish(source2, stream2, "t06-rs01-unknown-event")

    assert rejected["source_completeness"] == "UNAVAILABLE"
    assert rejected["unavailable_reason"] == "USAGE_RECORD_INVALID"


def test_t06_rs01_synthetic_real_shapes_remain_opaque_and_aggregate_direct_totals(
    tmp_path: Path,
) -> None:
    source, stream, _ = _open(tmp_path, window_id="t06-rs01-synthetic-segment")
    sentinel = "T06_RS01_PRIVATE_BODY_SENTINEL"
    rows = [
        _opaque_line(
            "response_item",
            json.dumps({"type": "reasoning", "content": [{"text": sentinel}]}),
        ),
        _opaque_line(
            "response_item",
            json.dumps({"type": "custom_tool_call", "input": {"value": sentinel}}),
        ),
        _opaque_line(
            "response_item",
            json.dumps({"type": "message", "content": [{"text": sentinel}]}),
        ),
        _envelope_line(
            "response_item",
            {"type": "custom_tool_call_output", "output": {"value": sentinel}},
            metadata={"opaque": {"value": sentinel}},
        ),
        _opaque_line(
            "event_msg",
            json.dumps({"type": "agent_message", "message": sentinel}),
        ),
    ]
    rows.extend(_usage(f"synthetic-{index}") for index in range(6))
    source.write_bytes(b"".join(rows))

    observation = _finish(source, stream, "t06-rs01-synthetic-segment")

    assert observation["source_completeness"] == "COMPLETE"
    assert observation["source"]["unique_response_count"] == 6
    assert observation["scope"]["kind"] == "WORK_WINDOW"
    assert all(
        quantity["quality"] == "DIRECT"
        and quantity["numeric_claim_kind"] == "COMPLETE_SCOPE_TOTAL"
        for quantity in observation["quantities"].values()
    )
    assert sentinel not in json.dumps(observation)
    assert sentinel.encode("utf-8") not in stream.read_bytes()


def test_r5r_02_a06_contradictory_session_meta_identities_fail_closed(tmp_path: Path) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5r-02-session-conflict")
    meta = {"id": "session-a", "session_id": "session-b"}
    source.write_bytes(_opaque_line("session_meta", json.dumps(meta)) + _usage(session_id="session-a"))

    observation = _finish(source, stream, "r5r-02-session-conflict")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}


@pytest.mark.parametrize(
    "record_type",
    ["compacted", "inter_agent_communication_metadata", "world_state"],
)
def test_r5r_02_a07_unproven_opaque_families_fail_closed(
    tmp_path: Path, record_type: str
) -> None:
    source, stream, _ = _open(tmp_path, window_id=f"r5r-02-unproven-{record_type}")
    source.write_bytes(_opaque_line(record_type, "{}") + _usage())

    observation = _finish(source, stream, f"r5r-02-unproven-{record_type}")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}


@pytest.mark.parametrize(
    "payload",
    [
        {"model": "gpt-5.6-sol"},
        {"turn_id": "current-turn"},
    ],
    ids=["missing-turn-id", "missing-model"],
)
def test_r5r_02_a08_incomplete_turn_context_carriers_fail_closed(
    tmp_path: Path, payload: dict[str, str]
) -> None:
    source, stream, _ = _open(tmp_path, window_id="r5r-02-incomplete-context")
    source.write_bytes(_opaque_line("turn_context", json.dumps(payload)) + _usage())

    observation = _finish(source, stream, "r5r-02-incomplete-context")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}


def test_frr_01_task_started_with_turn_id_allows_direct_complete_scope_usage(
    tmp_path: Path,
) -> None:
    source, stream, _ = _open(tmp_path, window_id="frr-01-task-started")
    source.write_bytes(
        _opaque_line(
            "event_msg",
            json.dumps({"type": "task_started", "turn_id": "turn-frr-01"}),
        )
        + _usage()
        + _opaque_line("event_msg", json.dumps({"type": "task_complete"}))
    )

    observation = _finish(source, stream, "frr-01-task-started")

    assert observation["source_completeness"] == "COMPLETE"
    assert observation["unavailable_reason"] is None
    assert observation["quantities"]["total_tokens"]["value"] == 15
    assert all(
        quantity["quality"] == "DIRECT"
        and quantity["numeric_claim_kind"] == "COMPLETE_SCOPE_TOTAL"
        for quantity in observation["quantities"].values()
    )
    assert observation["scope"]["kind"] == "WORK_WINDOW"
    assert not any(
        "attempt" in key.lower() or "turn_to_attempt" in key.lower()
        for key in observation
    )


@pytest.mark.parametrize(
    "payload",
    [
        {"type": "task_started"},
        {"type": "task_started", "turn_id": ""},
        {"type": "task_started", "turn_id": 42},
    ],
    ids=["missing-turn-id", "empty-turn-id", "non-string-turn-id"],
)
def test_frr_01_malformed_task_started_fails_closed_without_quantities(
    tmp_path: Path, payload: dict[str, object]
) -> None:
    source, stream, _ = _open(tmp_path, window_id="frr-01-malformed-task-started")
    source.write_bytes(
        _opaque_line("event_msg", json.dumps(payload))
        + _usage()
        + _opaque_line("event_msg", json.dumps({"type": "task_complete"}))
    )

    observation = _finish(source, stream, "frr-01-malformed-task-started")

    assert observation["source_completeness"] == "UNAVAILABLE"
    assert observation["unavailable_reason"] == "USAGE_RECORD_INVALID"
    assert observation["quantities"] == {}
