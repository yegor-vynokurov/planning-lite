"""Acceptance scaffold for the bounded Codex RunReceipt capture seam.

The rollout records in this file intentionally use the production host shape:
the top-level discriminator is available before a payload is considered, and
metadata needed for binding is kept separate from content-bearing records.
The fixture is generated in ``tmp_path`` so the test never depends on a
checked-in rollout or on the host's private history.

Slice A-01 deliberately has one passing fixture-contract node and two RED
nodes.  The latter stop at ``CAPTURE_CAPABILITY_MISSING`` until the capture
script is present.  Once it exists, those same nodes execute the real CLI and
become the walking-skeleton and preflight acceptance tests.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import runpy
import subprocess
import sys
from typing import Any, Callable, Iterable

import pytest

from planning_lite.codex_work_window import finalize_work_window, open_work_window


PROJECT_ID = "planning-lite-central"
CHANGE_ID = "CHG-PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-001"
TASK_ID = "A-04"
RUN_FAMILY = "bootstrap-slice-a-capture"
CONTENT_SENTINEL = "DO_NOT_READ_OR_HASH_CONTENT_SENTINEL_9f3a"
SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "capture_codex_run_receipts.py"

PARENT_SESSION = "session-parent-001"
PARENT_TURN = "turn-parent-001"
CHILD_SESSION = "session-child-001"
CHILD_TURN = "turn-child-001"


@dataclass(frozen=True)
class RolloutFixture:
    """Paths and exact binding facts for one disposable operation."""

    root: Path
    parent_rollout: Path
    child_rollout: Path
    expected_head: str
    parent_session_id: str = PARENT_SESSION
    parent_turn_id: str = PARENT_TURN
    child_session_id: str = CHILD_SESSION
    child_turn_id: str = CHILD_TURN

    @property
    def receipt_path(self) -> Path:
        return (
            self.root
            / ".local"
            / "state"
            / "projects"
            / PROJECT_ID
            / "telemetry"
            / "run-receipts.jsonl"
        )


@dataclass(frozen=True)
class CaptureResult:
    """A subprocess result with output retained for structured assertions."""

    returncode: int
    stdout: str
    stderr: str


def _iso(second: int) -> str:
    return f"2026-09-14T10:00:{second:02d}.123456+00:00"


def _record(record_type: str, timestamp: str, payload: dict[str, Any]) -> dict[str, Any]:
    """Build a host record with discriminator-before-payload key order."""

    # Retained Codex rollouts currently order these as timestamp, type,
    # payload.  The contract requires the discriminator before the payload,
    # not that it be the first object key.
    return {"timestamp": timestamp, "type": record_type, "payload": payload}


def _session_records(
    *,
    session_id: str,
    turn_id: str,
    model: str,
    effort: str,
    parent_session_id: str | None,
    parent_turn_id: str | None,
    input_tokens: int,
    output_tokens: int,
    cached_input_tokens: int,
    reasoning_output_tokens: int,
    total_tokens: int,
    content_prefix: str,
) -> list[dict[str, Any]]:
    """Return a realistic Codex rollout segment for one invocation.

    The intermediate counter makes the terminal-counter rule observable: the
    adapter must choose the last cumulative counter before completion rather
    than the first or a counter after completion.
    """

    return [
        _record(
            "session_meta",
            _iso(1),
            {
                "id": session_id,
                "session_id": session_id,
                "parent_session_id": parent_session_id,
                "parent_thread_id": parent_session_id,
            },
        ),
        _record(
            "turn_context",
            _iso(2),
            {
                "session_id": session_id,
                "turn_id": turn_id,
                "model": model,
                "effort": effort,
                "root_turn_id": parent_turn_id,
            },
        ),
        # Content records are present to prove that attribution does not need
        # prompt, assistant, tool-payload, or reasoning bodies.
        _record(
            "event_msg",
            _iso(3),
            {"type": "user_message", "message": f"{content_prefix}:{CONTENT_SENTINEL}"},
        ),
        _record(
            "response_item",
            _iso(4),
            {"type": "assistant_message", "content": f"{content_prefix}:{CONTENT_SENTINEL}"},
        ),
        _record(
            "event_msg",
            _iso(5),
            {"type": "function_call", "arguments": f"{content_prefix}:{CONTENT_SENTINEL}"},
        ),
        _record(
            "event_msg",
            _iso(6),
            {"type": "reasoning", "text": f"{content_prefix}:{CONTENT_SENTINEL}"},
        ),
        _record(
            "event_msg",
            _iso(7),
            {
                "type": "token_count",
                "turn_id": turn_id,
                "info": {
                    "total_token_usage": {
                        "input_tokens": max(input_tokens - 10, 0),
                        "cached_input_tokens": cached_input_tokens,
                        "output_tokens": max(output_tokens - 2, 0),
                        "reasoning_output_tokens": max(reasoning_output_tokens - 1, 0),
                        "total_tokens": max(total_tokens - 12, 0),
                    }
                },
            },
        ),
        _record(
            "event_msg",
            _iso(8),
            {
                "type": "token_count",
                "turn_id": turn_id,
                "info": {
                    "total_token_usage": {
                        "input_tokens": input_tokens,
                        "cached_input_tokens": cached_input_tokens,
                        "output_tokens": output_tokens,
                        "reasoning_output_tokens": reasoning_output_tokens,
                        "total_tokens": total_tokens,
                    }
                },
            },
        ),
        _record("event_msg", _iso(9), {"type": "task_complete", "turn_id": turn_id}),
    ]


def _write_jsonl(path: Path, records: Iterable[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(record, ensure_ascii=False, separators=(",", ":")) + "\n" for record in records),
        encoding="utf-8",
    )


def _git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        check=check,
        capture_output=True,
        text=True,
    )


def _make_fixture(tmp_path: Path) -> RolloutFixture:
    """Create a clean Git root and two explicitly bindable rollout files."""

    root = tmp_path / "central-repository"
    root.mkdir()
    (root / "fixture.txt").write_text("production-equivalent\n", encoding="utf-8")
    _git(root, "init", "--initial-branch", "main")
    _git(root, "add", "fixture.txt")
    subprocess.run(
        [
            "git",
            "-C",
            str(root),
            "-c",
            "user.name=Planning Lite Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-m",
            "fixture",
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    expected_head = _git(root, "rev-parse", "HEAD").stdout.strip()
    assert len(expected_head) == 40 and all(char in "0123456789abcdef" for char in expected_head)
    assert Path(_git(root, "rev-parse", "--show-toplevel").stdout.strip()).resolve() == root.resolve()

    parent_rollout = root / "rollouts" / "parent.jsonl"
    child_rollout = root / "rollouts" / "child.jsonl"
    parent_rollout.parent.mkdir()
    _write_jsonl(
        parent_rollout,
        _session_records(
            session_id=PARENT_SESSION,
            turn_id=PARENT_TURN,
            model="gpt-5.6-sol",
            effort="high",
            parent_session_id=None,
            parent_turn_id=None,
            input_tokens=120,
            output_tokens=30,
            cached_input_tokens=40,
            reasoning_output_tokens=10,
            total_tokens=150,
            content_prefix="parent",
        ),
    )
    _write_jsonl(
        child_rollout,
        _session_records(
            session_id=CHILD_SESSION,
            turn_id=CHILD_TURN,
            model="gpt-5.6-luna",
            effort="extra_high",
            parent_session_id=PARENT_SESSION,
            parent_turn_id=PARENT_TURN,
            input_tokens=80,
            output_tokens=20,
            cached_input_tokens=12,
            reasoning_output_tokens=8,
            total_tokens=100,
            content_prefix="child",
        ),
    )
    return RolloutFixture(
        root=root,
        parent_rollout=parent_rollout,
        child_rollout=child_rollout,
        expected_head=expected_head,
    )


def _records(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _variant(path: Path, name: str, mutate: Callable[[list[dict[str, Any]]], None]) -> Path:
    target = path.with_name(f"{path.stem}-{name}.jsonl")
    records = _records(path)
    mutate(records)
    _write_jsonl(target, records)
    return target


def _assert_capture_failure(result: CaptureResult, failure_class: str) -> None:
    assert result.returncode != 0
    assert result.stdout == ""
    assert failure_class in result.stderr
    assert CONTENT_SENTINEL not in result.stderr


def _metadata_projection(path: Path) -> list[tuple[str, str | None]]:
    """Classify by discriminator without looking inside content records."""

    content_types = {"user_message", "assistant_message", "function_call", "reasoning"}
    projection: list[tuple[str, str | None]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        # Reading the top-level discriminator is the only operation performed
        # before deciding whether a payload is metadata or content.
        raw = json.loads(line)
        record_type = raw["type"]
        if record_type == "session_meta":
            projection.append((record_type, raw["payload"]["id"]))
        elif record_type == "turn_context":
            projection.append((record_type, raw["payload"]["turn_id"]))
        elif record_type == "event_msg" and raw.get("payload", {}).get("type") == "token_count":
            projection.append((record_type, "token_count"))
        elif record_type == "event_msg" and raw.get("payload", {}).get("type") == "task_complete":
            projection.append((record_type, "task_complete"))
        elif record_type in {"event_msg", "response_item"}:
            # The payload is deliberately opaque.  Keep only the top-level
            # record class; content text never enters the projection.
            projection.append((record_type, None))
        else:  # pragma: no cover - the fixture contract catches this first.
            raise AssertionError(f"unexpected host record type: {record_type}")
    return projection


def _identity_bytes(
    *,
    agent_role: str,
    change_id: str | None,
    session_id: str,
    turn_id: str,
    invocation_index: int,
    planning_lite_ref: str,
    project_id: str,
    run_family: str,
    task_id: str,
) -> bytes:
    identity = {
        "agent_role": agent_role,
        "change_id": change_id,
        "host_session_id": session_id,
        "host_turn_id": turn_id,
        "invocation_index": invocation_index,
        "planning_lite_ref": planning_lite_ref,
        "project_id": project_id,
        "run_family": run_family,
        "schema": "planning-lite-codex-receipt-id-v1",
        "task_id": task_id,
    }
    return json.dumps(identity, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _receipt_id(**kwargs: Any) -> str:
    return "codex-run-v1:" + hashlib.sha256(_identity_bytes(**kwargs)).hexdigest()


def _discriminator_cases(fixture: RolloutFixture) -> dict[str, Callable[[], Any]]:
    """Name every approved GREEN discriminator without requiring the adapter.

    A-01 uses these builders in the fixture self-check.  A-02/A-03 can invoke
    the same cases against the real capture command without adding permanent
    rollout data or changing the RED seam.
    """

    def _copy_with(path: Path, mutate: Callable[[list[dict[str, Any]]], None]) -> Path:
        target = path.with_name(path.stem + "-variant.jsonl")
        records = _records(path)
        mutate(records)
        _write_jsonl(target, records)
        return target

    return {
        "exact_parent_and_ordered_child_binding": lambda: [
            fixture.parent_rollout,
            fixture.child_rollout,
        ],
        "direct_child_parent_linkage": lambda: (
            _records(fixture.child_rollout)[1]["payload"]["root_turn_id"] == fixture.parent_turn_id
        ),
        "no_latest_newest_timestamp_fuzzy_title_content_attribution": lambda: _metadata_projection(
            fixture.parent_rollout
        ),
        "parent_child_role_model_tier_and_effort": lambda: (
            _records(fixture.parent_rollout)[1]["payload"]["model"],
            _records(fixture.child_rollout)[1]["payload"]["model"],
            _records(fixture.parent_rollout)[1]["payload"]["effort"],
            _records(fixture.child_rollout)[1]["payload"]["effort"],
        ),
        "exact_field_token_read_and_runtime_mapping": lambda: (
            _records(fixture.parent_rollout)[7]["payload"]["info"]["total_token_usage"],
            "external_runtime",
            "codex_rollout_jsonl_v1",
        ),
        "frozen_receipt_id_vector": lambda: _receipt_id(
            agent_role="CHILD",
            change_id=CHANGE_ID,
            session_id="session-child-001",
            turn_id="turn-child-001",
            invocation_index=1,
            planning_lite_ref="748fbe70dd6f3d5a6d7242df41ace2d573c40d55",
            project_id=PROJECT_ID,
            run_family="bootstrap-slice-b-review",
            task_id="B-04",
        ),
        "token_model_outcome_and_path_exclusion_from_id": lambda: _receipt_id(
            agent_role="PARENT",
            change_id=CHANGE_ID,
            session_id=fixture.parent_session_id,
            turn_id=fixture.parent_turn_id,
            invocation_index=0,
            planning_lite_ref=fixture.expected_head,
            project_id=PROJECT_ID,
            run_family=RUN_FAMILY,
            task_id=TASK_ID,
        ),
        "identical_replay_conflict_and_interrupted_prefix_completion": lambda: fixture.receipt_path,
        "full_preflight_and_invalid_one_of_n_zero_write": lambda: _copy_with(
            fixture.child_rollout,
            lambda records: records.__setitem__(
                8,
                _record("event_msg", _iso(9), {"type": "task_complete", "turn_id": "wrong-turn"}),
            ),
        ),
        "unsupported_host_shape": lambda: _copy_with(
            fixture.parent_rollout,
            lambda records: records.append(_record("unsupported_host_record", _iso(10), {})),
        ),
        "missing_conflicting_or_multiple_identity": lambda: _copy_with(
            fixture.parent_rollout,
            lambda records: records.__setitem__(
                0,
                _record("session_meta", _iso(1), {"id": "different-session", "model": "gpt-5.6-sol"}),
            ),
        ),
        "missing_final_counter": lambda: _copy_with(
            fixture.child_rollout,
            lambda records: records.__setitem__(
                slice(6, 8),
                [],
            ),
        ),
        "invalid_token_type_or_range": lambda: _copy_with(
            fixture.parent_rollout,
            lambda records: records[7]["payload"]["info"]["total_token_usage"].update(
                {"input_tokens": True}
            ),
        ),
        "unlinked_child": lambda: _copy_with(
            fixture.child_rollout,
            lambda records: records[1]["payload"].update({"root_turn_id": "unlinked-turn"}),
        ),
        "duplicate_child_index": lambda: (0, 1),
        "head_mismatch": lambda: "0" * 40,
        "expected_receipt_count": lambda: 2,
        "privacy_no_content_decode_persist_hash_echo_or_attribution": lambda: CONTENT_SENTINEL,
    }


def _assert_fixture_contract(fixture: RolloutFixture) -> None:
    """Validate the production-equivalent fixture before any RED marker."""

    parent = _records(fixture.parent_rollout)
    child = _records(fixture.child_rollout)
    assert parent and child
    assert all(list(record).index("type") < list(record).index("payload") for record in [*parent, *child])
    assert parent[0]["type"] == child[0]["type"] == "session_meta"
    assert parent[0]["payload"]["id"] == fixture.parent_session_id
    assert child[0]["payload"]["id"] == fixture.child_session_id
    assert parent[1]["payload"]["turn_id"] == fixture.parent_turn_id
    assert child[1]["payload"]["turn_id"] == fixture.child_turn_id
    assert child[0]["payload"]["parent_thread_id"] == fixture.parent_session_id
    assert child[1]["payload"]["root_turn_id"] == fixture.parent_turn_id
    assert parent[1]["payload"]["model"] == "gpt-5.6-sol"
    assert child[1]["payload"]["model"] == "gpt-5.6-luna"
    assert parent[1]["payload"]["effort"] == "high"
    assert child[1]["payload"]["effort"] == "extra_high"

    for stream, expected_turn, expected_total in (
        (parent, fixture.parent_turn_id, 150),
        (child, fixture.child_turn_id, 100),
    ):
        counters = [record for record in stream if record.get("payload", {}).get("type") == "token_count"]
        completions = [record for record in stream if record.get("payload", {}).get("type") == "task_complete"]
        assert len(counters) == 2
        assert len(completions) == 1
        assert counters[-1]["payload"]["turn_id"] == expected_turn
        assert counters[-1]["payload"]["info"]["total_token_usage"]["total_tokens"] == expected_total
        assert stream.index(counters[-1]) < stream.index(completions[0])
        assert counters[-1]["timestamp"] == _iso(8)
        parsed_timestamp = datetime.fromisoformat(counters[-1]["timestamp"])
        assert parsed_timestamp.tzinfo is not None
        assert parsed_timestamp.astimezone(timezone.utc).isoformat().endswith("+00:00")

    raw = fixture.parent_rollout.read_text(encoding="utf-8") + fixture.child_rollout.read_text(encoding="utf-8")
    assert raw.count(CONTENT_SENTINEL) == 8
    projection = _metadata_projection(fixture.parent_rollout)
    assert projection[0:2] == [("session_meta", fixture.parent_session_id), ("turn_context", fixture.parent_turn_id)]
    assert all(CONTENT_SENTINEL not in json.dumps(item) for item in projection)

    expected_id = "codex-run-v1:8a5db46c63972343069db409940828848164a22cfaf297126c072e8bc8795283"
    assert (
        _receipt_id(
            agent_role="CHILD",
            change_id=CHANGE_ID,
            session_id="session-child-001",
            turn_id="turn-child-001",
            invocation_index=1,
            planning_lite_ref="748fbe70dd6f3d5a6d7242df41ace2d573c40d55",
            project_id=PROJECT_ID,
            run_family="bootstrap-slice-b-review",
            task_id="B-04",
        )
        == expected_id
    )
    cases = _discriminator_cases(fixture)
    assert set(cases) == {
        "exact_parent_and_ordered_child_binding",
        "direct_child_parent_linkage",
        "no_latest_newest_timestamp_fuzzy_title_content_attribution",
        "parent_child_role_model_tier_and_effort",
        "exact_field_token_read_and_runtime_mapping",
        "frozen_receipt_id_vector",
        "token_model_outcome_and_path_exclusion_from_id",
        "identical_replay_conflict_and_interrupted_prefix_completion",
        "full_preflight_and_invalid_one_of_n_zero_write",
        "unsupported_host_shape",
        "missing_conflicting_or_multiple_identity",
        "missing_final_counter",
        "invalid_token_type_or_range",
        "unlinked_child",
        "duplicate_child_index",
        "head_mismatch",
        "expected_receipt_count",
        "privacy_no_content_decode_persist_hash_echo_or_attribution",
    }
    # Exercise every approved case builder so malformed scaffold cases cannot
    # be hidden behind a merely declarative list.
    built_cases = {name: builder() for name, builder in cases.items()}
    assert built_cases["frozen_receipt_id_vector"] == expected_id
    assert built_cases["expected_receipt_count"] == 2
    assert built_cases["head_mismatch"] == "0" * 40
    assert built_cases["privacy_no_content_decode_persist_hash_echo_or_attribution"] == CONTENT_SENTINEL


def _capture_command(
    fixture: RolloutFixture,
    *,
    child_rollout: Path | None = None,
    child_session_id: str | None = None,
    child_turn_id: str | None = None,
    child_index: int = 1,
    expected_head: str | None = None,
    project_id: str = PROJECT_ID,
    task_id: str = TASK_ID,
    run_family: str = RUN_FAMILY,
    change_id: str | None = CHANGE_ID,
    null_change_id: bool = False,
    include_child: bool = True,
    extra_children: list[tuple[Path, str, str, int]] | None = None,
) -> CaptureResult:
    """Invoke the eventual production command with no implicit selection."""

    if not SCRIPT_PATH.exists():
        pytest.fail("CAPTURE_CAPABILITY_MISSING")
    child = child_rollout or fixture.child_rollout
    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--repo-root",
        str(fixture.root),
        "--expected-head",
        expected_head or fixture.expected_head,
        "--project-id",
        project_id,
    ]
    if null_change_id:
        command.append("--null-change-id")
    elif change_id is not None:
        command.extend(["--change-id", change_id])
    command.extend(
        [
        "--task-id",
        task_id,
        "--run-family",
        run_family,
        "--outcome",
        "PASS",
        "--parent-rollout",
        str(fixture.parent_rollout),
        "--parent-session-id",
        fixture.parent_session_id,
        "--parent-turn-id",
        fixture.parent_turn_id,
        ]
    )
    if include_child:
        command.extend(
            [
                "--child",
                str(child),
                child_session_id or fixture.child_session_id,
                child_turn_id or fixture.child_turn_id,
                str(child_index),
            ]
        )
    for rollout, session_id, turn_id, index in extra_children or []:
        command.extend(["--child", str(rollout), session_id, turn_id, str(index)])
    completed = subprocess.run(command, capture_output=True, text=True)
    return CaptureResult(completed.returncode, completed.stdout, completed.stderr)


def test_production_equivalent_rollout_fixture_contract_is_valid(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    _assert_fixture_contract(fixture)


def test_capture_walking_skeleton_maps_persists_and_reads_parent_and_child(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    _assert_fixture_contract(fixture)
    first = _capture_command(fixture)
    assert first.returncode == 0, first.stderr
    assert CONTENT_SENTINEL not in first.stdout
    assert CONTENT_SENTINEL not in first.stderr
    summary = json.loads(first.stdout)
    assert summary["status"] == "PASS"
    assert summary["expected_receipt_count"] == summary["verified_receipt_count"] == 2
    assert [record["agent_role"] for record in summary["records"]] == ["PARENT", "CHILD"]
    assert [record["append_result"] for record in summary["records"]] == ["APPENDED", "APPENDED"]
    assert fixture.receipt_path.exists()
    receipts = [json.loads(line) for line in fixture.receipt_path.read_text(encoding="utf-8").splitlines()]
    assert len(receipts) == 2
    assert [receipt["agent_role"] for receipt in receipts] == ["PARENT", "CHILD"]
    assert receipts[0]["tokens"]["total"] == 150
    assert receipts[1]["tokens"]["total"] == 100
    assert receipts[0]["model_tier"] is None
    assert receipts[1]["model_tier"] is None
    assert all(receipt["runtime_source"] == "codex_rollout_jsonl_v1" for receipt in receipts)
    assert all(CONTENT_SENTINEL not in line for line in fixture.receipt_path.read_text(encoding="utf-8").splitlines())
    second = _capture_command(fixture)
    assert second.returncode == 0, second.stderr
    replay = json.loads(second.stdout)
    assert [record["append_result"] for record in replay["records"]] == [
        "IDENTICAL_EXISTING",
        "IDENTICAL_EXISTING",
    ]
    assert len(fixture.receipt_path.read_text(encoding="utf-8").splitlines()) == 2


def test_capture_preserves_parent_then_command_line_child_order(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    second_child = fixture.root / "rollouts" / "child-second.jsonl"
    second_records = _records(fixture.child_rollout)
    second_records[0]["payload"].update(
        {"id": "session-child-002", "session_id": "session-child-002"}
    )
    second_records[1]["payload"].update(
        {"turn_id": "turn-child-002", "root_turn_id": fixture.parent_turn_id, "session_id": "session-child-002"}
    )
    for record in second_records:
        payload = record.get("payload", {})
        if payload.get("type") in {"token_count", "task_complete"}:
            payload["turn_id"] = "turn-child-002"
    _write_jsonl(second_child, second_records)
    result = _capture_command(
        fixture,
        extra_children=[(second_child, "session-child-002", "turn-child-002", 2)],
    )
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["expected_receipt_count"] == summary["verified_receipt_count"] == 3
    assert [(record["agent_role"], record["invocation_index"]) for record in summary["records"]] == [
        ("PARENT", 0),
        ("CHILD", 1),
        ("CHILD", 2),
    ]
    receipts = [json.loads(line) for line in fixture.receipt_path.read_text(encoding="utf-8").splitlines()]
    assert [(receipt["agent_role"], receipt["invocation_index"]) for receipt in receipts] == [
        ("PARENT", 0),
        ("CHILD", 1),
        ("CHILD", 2),
    ]


def test_capture_preflight_rejects_one_invalid_candidate_without_writing(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    _assert_fixture_contract(fixture)
    invalid_child = fixture.child_rollout.with_name("child-invalid.jsonl")
    invalid_records = _records(fixture.child_rollout)
    invalid_records[8] = _record("event_msg", _iso(9), {"type": "task_complete", "turn_id": "wrong-turn"})
    _write_jsonl(invalid_child, invalid_records)
    result = _capture_command(fixture, child_rollout=invalid_child)
    assert result.returncode != 0
    assert "CAPTURE_CAPABILITY_MISSING" not in result.stderr
    assert not fixture.receipt_path.exists()


def test_capture_rejects_unsupported_host_shape_before_writing(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    unsupported = _variant(
        fixture.parent_rollout,
        "unsupported",
        lambda records: records.append(_record("unsupported_host_record", _iso(10), {})),
    )
    fixture = RolloutFixture(
        fixture.root,
        unsupported,
        fixture.child_rollout,
        fixture.expected_head,
    )
    result = _capture_command(fixture)
    _assert_capture_failure(result, "UNSUPPORTED_HOST_RECORD_SHAPE")
    assert not fixture.receipt_path.exists()


def test_capture_rejects_identity_ambiguity_and_multiple_matches(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    duplicate_session = _variant(
        fixture.parent_rollout,
        "duplicate-session",
        lambda records: records.append(
            {
                **records[0],
                "payload": {**records[0]["payload"], "parent_thread_id": "conflicting-parent"},
            }
        ),
    )
    duplicate_turn = _variant(
        fixture.parent_rollout,
        "duplicate-turn",
        lambda records: records.insert(
            2,
            {
                **records[1],
                "payload": {**records[1]["payload"], "model": "conflicting-model"},
            },
        ),
    )
    duplicate_session_fixture = RolloutFixture(
        fixture.root,
        duplicate_session,
        fixture.child_rollout,
        fixture.expected_head,
    )
    duplicate_turn_fixture = RolloutFixture(
        fixture.root,
        duplicate_turn,
        fixture.child_rollout,
        fixture.expected_head,
    )
    _assert_capture_failure(_capture_command(duplicate_session_fixture), "IDENTITY_AMBIGUITY")
    _assert_capture_failure(_capture_command(duplicate_turn_fixture), "IDENTITY_AMBIGUITY")

    missing_session = _variant(
        fixture.parent_rollout,
        "missing-session",
        lambda records: records[0]["payload"].update({"id": "other", "session_id": "other"}),
    )
    conflicting_turn_session = _variant(
        fixture.parent_rollout,
        "conflicting-turn-session",
        lambda records: records[1]["payload"].update({"session_id": "other-session"}),
    )
    missing_fixture = RolloutFixture(fixture.root, missing_session, fixture.child_rollout, fixture.expected_head)
    conflicting_fixture = RolloutFixture(
        fixture.root,
        conflicting_turn_session,
        fixture.child_rollout,
        fixture.expected_head,
    )
    _assert_capture_failure(_capture_command(missing_fixture), "IDENTITY_AMBIGUITY")
    _assert_capture_failure(_capture_command(conflicting_fixture), "IDENTITY_AMBIGUITY")
    assert not fixture.receipt_path.exists()


def test_capture_accepts_repeated_identical_turn_context_and_opaque_current_host_records(
    tmp_path: Path,
) -> None:
    fixture = _make_fixture(tmp_path)
    records = _records(fixture.parent_rollout)
    records.insert(2, records[1])
    records.insert(
        3,
        _record(
            "token_usage_record",
            _iso(2),
            {
                "response_id": "opaque",
                "root_turn_id": fixture.parent_turn_id,
                "session_id": fixture.parent_session_id,
                "thread_id": fixture.parent_session_id,
                "turn_id": fixture.parent_turn_id,
                "usage": {"content_adjacent": CONTENT_SENTINEL},
            },
        ),
    )
    _write_jsonl(fixture.parent_rollout, records)
    result = _capture_command(fixture)
    assert result.returncode == 0, result.stderr
    assert CONTENT_SENTINEL not in result.stdout
    assert json.loads(result.stdout)["verified_receipt_count"] == 2


def test_capture_never_decodes_known_content_payloads(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    raw = fixture.parent_rollout.read_text(encoding="utf-8")
    # An invalid JSON escape lives only inside known content bodies.  Capture
    # can still bind metadata because those bodies are classified then opaque.
    raw = raw.replace(CONTENT_SENTINEL, r"OPAQUE_INVALID_ESCAPE\q")
    fixture.parent_rollout.write_text(raw, encoding="utf-8")
    result = _capture_command(fixture)
    assert result.returncode == 0, result.stderr
    assert "OPAQUE_INVALID_ESCAPE" not in result.stdout
    assert "OPAQUE_INVALID_ESCAPE" not in result.stderr


@pytest.mark.parametrize(
    ("name", "mutate", "failure_class"),
    [
        (
            "missing-counter",
            lambda records: records.__setitem__(
                slice(6, 8),
                [],
            ),
            "MISSING_FINAL_COUNTER",
        ),
        (
            "missing-completion",
            lambda records: records.__setitem__(
                slice(8, 9),
                [],
            ),
            "MISSING_COMPLETION",
        ),
        (
            "counter-after-completion",
            lambda records: records.append(records[7]),
            "COUNTER_AFTER_COMPLETION",
        ),
        (
            "counter-before-completion-order",
            lambda records: records.__setitem__(
                slice(6, 9),
                [records[8], records[7]],
            ),
            "COUNTER_AFTER_COMPLETION",
        ),
        (
            "invalid-token-type",
            lambda records: records[7]["payload"]["info"]["total_token_usage"].update({"input_tokens": True}),
            "INVALID_TOKEN_RECORD",
        ),
        (
            "invalid-token-range",
            lambda records: records[7]["payload"]["info"]["total_token_usage"].update({"input_tokens": -1}),
            "INVALID_TOKEN_RECORD",
        ),
    ],
)
def test_capture_rejects_counter_completion_and_token_discriminators(
    tmp_path: Path,
    name: str,
    mutate: Callable[[list[dict[str, Any]]], None],
    failure_class: str,
) -> None:
    fixture = _make_fixture(tmp_path)
    invalid_parent = _variant(fixture.parent_rollout, name, mutate)
    invalid_fixture = RolloutFixture(fixture.root, invalid_parent, fixture.child_rollout, fixture.expected_head)
    _assert_capture_failure(_capture_command(invalid_fixture), failure_class)
    assert not fixture.receipt_path.exists()


def test_capture_rejects_unlinked_child_and_duplicate_invocation_index(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    unlinked_child = _variant(
        fixture.child_rollout,
        "unlinked",
        lambda records: records[1]["payload"].update({"root_turn_id": "unlinked-turn"}),
    )
    unlinked_fixture = RolloutFixture(fixture.root, fixture.parent_rollout, unlinked_child, fixture.expected_head)
    _assert_capture_failure(_capture_command(unlinked_fixture), "UNLINKED_CHILD")

    duplicate = _capture_command(
        fixture,
        extra_children=[(fixture.child_rollout, fixture.child_session_id, fixture.child_turn_id, 1)],
    )
    _assert_capture_failure(duplicate, "DUPLICATE_CHILD_INDEX")
    assert not fixture.receipt_path.exists()


def test_capture_guards_head_project_and_explicit_change_binding(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    _assert_capture_failure(_capture_command(fixture, expected_head="0" * 40), "HEAD_MISMATCH")
    _assert_capture_failure(_capture_command(fixture, project_id="wrong-project"), "PROJECT_ID_MISMATCH")
    missing_change = _capture_command(fixture, change_id=None)
    assert missing_change.returncode != 0
    assert "change-id" in missing_change.stderr
    assert not fixture.receipt_path.exists()

    null_change = _capture_command(fixture, null_change_id=True)
    assert null_change.returncode == 0, null_change.stderr
    summary = json.loads(null_change.stdout)
    assert summary["change_id"] is None
    stored = [json.loads(line) for line in fixture.receipt_path.read_text(encoding="utf-8").splitlines()]
    assert all(receipt["change_id"] is None for receipt in stored)


def test_capture_receipt_identity_freezes_inputs_and_excludes_observation_fields() -> None:
    namespace = runpy.run_path(str(SCRIPT_PATH))
    make_receipt_id = namespace["make_receipt_id"]
    receipt_identity = namespace["receipt_identity"]

    kwargs = {
        "agent_role": "CHILD",
        "change_id": CHANGE_ID,
        "host_session_id": "session-child-001",
        "host_turn_id": "turn-child-001",
        "invocation_index": 1,
        "planning_lite_ref": "748fbe70dd6f3d5a6d7242df41ace2d573c40d55",
        "project_id": PROJECT_ID,
        "run_family": "bootstrap-slice-b-review",
        "task_id": "B-04",
    }
    expected = "codex-run-v1:8a5db46c63972343069db409940828848164a22cfaf297126c072e8bc8795283"
    assert make_receipt_id(**kwargs) == expected
    assert json.dumps(receipt_identity(**kwargs), sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    assert make_receipt_id(**{**kwargs, "host_session_id": "s-ü"}) != make_receipt_id(**kwargs)
    assert make_receipt_id(**{**kwargs, "change_id": None}) != make_receipt_id(**kwargs)
    assert make_receipt_id(**{**kwargs, "invocation_index": 0}) != make_receipt_id(**kwargs)
    # Rollout path, timestamp, token, model, effort, outcome, and retry state
    # are deliberately absent from the frozen identity input.
    assert set(receipt_identity(**kwargs)) == {
        "agent_role",
        "change_id",
        "host_session_id",
        "host_turn_id",
        "invocation_index",
        "planning_lite_ref",
        "project_id",
        "run_family",
        "schema",
        "task_id",
    }


def test_capture_replay_conflict_and_interrupted_prefix_completion(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    prefix = _capture_command(fixture, include_child=False)
    assert prefix.returncode == 0, prefix.stderr
    assert json.loads(prefix.stdout)["verified_receipt_count"] == 1
    completed = _capture_command(fixture)
    assert completed.returncode == 0, completed.stderr
    records = json.loads(completed.stdout)["records"]
    assert [record["append_result"] for record in records] == ["IDENTICAL_EXISTING", "APPENDED"]

    stored = [json.loads(line) for line in fixture.receipt_path.read_text(encoding="utf-8").splitlines()]
    stored[0]["outcome"] = "FAIL"
    fixture.receipt_path.write_text(
        "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in stored),
        encoding="utf-8",
    )
    conflict = _capture_command(fixture)
    _assert_capture_failure(conflict, "CONFLICTING_RECEIPT_ID")
    assert len(fixture.receipt_path.read_text(encoding="utf-8").splitlines()) == 2


def test_capture_uses_only_explicit_rollout_bindings_not_latest_or_content(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    decoy = fixture.root / "rollouts" / "newest-decoy.jsonl"
    decoy.write_text(
        json.dumps(
            {
                "timestamp": "2099-01-01T00:00:00Z",
                "type": "session_meta",
                "payload": {
                    "id": "wrong-session",
                    "session_id": "wrong-session",
                    "prompt": CONTENT_SENTINEL,
                },
            }
        )
        + "\n",
        encoding="utf-8",
    )
    result = _capture_command(fixture)
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert [record["session_id"] for record in summary["records"]] == [PARENT_SESSION, CHILD_SESSION]
    assert CONTENT_SENTINEL not in result.stdout


def test_capture_rejects_existing_operation_count_mismatch(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    first = _capture_command(fixture)
    assert first.returncode == 0, first.stderr
    records = [json.loads(line) for line in fixture.receipt_path.read_text(encoding="utf-8").splitlines()]
    extra = dict(records[0])
    extra["receipt_id"] = "manual-extra-receipt"
    fixture.receipt_path.write_text(
        "".join(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n" for record in [*records, extra]),
        encoding="utf-8",
    )
    result = _capture_command(fixture)
    _assert_capture_failure(result, "RECEIPT_COUNT_MISMATCH")
    assert len(fixture.receipt_path.read_text(encoding="utf-8").splitlines()) == 3


def test_br_a_01_alien_same_operation_receipt_is_zero_write_preappend(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    prefix = _capture_command(fixture, include_child=False)
    assert prefix.returncode == 0, prefix.stderr

    existing = _records(fixture.receipt_path)
    assert len(existing) == 1
    # The record remains structurally valid, but its opaque ID is not one of
    # the two IDs declared by the candidate operation.
    existing[0]["receipt_id"] = "codex-run-v1:alien-same-operation-receipt"
    _write_jsonl(fixture.receipt_path, existing)
    before_count = len(_records(fixture.receipt_path))

    result = _capture_command(fixture)
    _assert_capture_failure(result, "RECEIPT_COUNT_MISMATCH")

    after_count = len(_records(fixture.receipt_path))
    assert after_count - before_count == 0, "NEW_RECEIPTS_WRITTEN must be 0"


def test_br_a_02_new_head_operation_appends_preserving_historical_receipts(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    h1 = fixture.expected_head
    first = _capture_command(fixture)
    assert first.returncode == 0, first.stderr
    assert len(_records(fixture.receipt_path)) == 2

    (fixture.root / "fixture.txt").write_text("production-equivalent-h2\n", encoding="utf-8")
    _git(fixture.root, "add", "fixture.txt")
    _git(
        fixture.root,
        "-c",
        "user.name=Planning Lite Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-m",
        "fixture-h2",
    )
    h2 = _git(fixture.root, "rev-parse", "HEAD").stdout.strip()
    assert h2 != h1

    second = _capture_command(
        fixture,
        expected_head=h2,
        task_id="A-05",
        run_family="bootstrap-slice-a-h2-append",
    )
    assert second.returncode == 0, second.stderr

    receipts = _records(fixture.receipt_path)
    assert len(receipts) == 4
    assert [receipt["planning_lite_ref"] for receipt in receipts] == [h1, h1, h2, h2]
    assert [receipt["run_family"] for receipt in receipts] == [
        RUN_FAMILY,
        RUN_FAMILY,
        "bootstrap-slice-a-h2-append",
        "bootstrap-slice-a-h2-append",
    ]


def test_capture_a02_skips_validated_typed_siblings_and_returns_receipts_only(tmp_path: Path) -> None:
    fixture = _make_fixture(tmp_path)
    (fixture.root / ".copier-answers.planning-lite.yml").write_text(
        "_commit: v1.0.0\n", encoding="utf-8"
    )
    source = tmp_path / "dedicated-window.jsonl"
    source.write_bytes(b"")
    open_work_window(
        window_id="capture-window",
        project_id=PROJECT_ID,
        project_root=fixture.root,
        configuration_ref="comparison:v1",
        source_ref=source,
        model=None,
        receipt_path=fixture.receipt_path,
    )
    source.write_text(
        json.dumps(
            {
                "timestamp": _iso(10),
                "type": "token_usage_record",
                "payload": {
                    "thread_id": "window-thread",
                    "response_id": "window-response",
                    "usage": {"input_tokens": 4, "output_tokens": 1, "total_tokens": 5},
                },
            },
            separators=(",", ":"),
        )
        + "\n",
        encoding="utf-8",
    )
    finalize_work_window(
        "capture-window", receipt_path=fixture.receipt_path, registered_project_id=PROJECT_ID
    )
    result = _capture_command(fixture)
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["verified_receipt_count"] == 2
    rows = [json.loads(line) for line in fixture.receipt_path.read_text(encoding="utf-8").splitlines()]
    assert [row.get("record_type") for row in rows] == [
        "work_window_registration", "resource_observation", None, None
    ]
    assert len(summary["records"]) == 2
