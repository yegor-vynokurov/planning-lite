from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from planning_lite.project_spine import (
    PostEvaluationCheckpointV1,
    ProjectSpineHandoffError,
    ProjectSpineSnapshotV1,
    capture_project_spine_snapshot,
    record_post_evaluation_checkpoint,
)


TICK = chr(96)


def _active_text(*, newline: str = "\n", checkpoint: str = "checkpoint-0") -> str:
    return newline.join(
        (
            "# Active state",
            "",
            "## Active change",
            "",
            f"- Change: {TICK}CHG-TEST-001{TICK}",
            f"- Change status: {TICK}Active{TICK}",
            f"- Lifecycle stage: {TICK}Implementation{TICK}",
            f"- Stage status: {TICK}Ready{TICK}",
            f"- Current task: {TICK}T-01{TICK}",
            f"- Last verified checkpoint: {TICK}{checkpoint}{TICK}",
            f"- Next gate: {TICK}Central Candidate Review Gate{TICK}",
            f"- Next permitted action: {TICK}Run T-01{TICK}",
            f"- Implementation authorized: {TICK}No{TICK}",
            f"- Active context packet: {TICK}.planning/changes/active/CHG-TEST-001/context.md{TICK}",
            "",
            "## Blocking decision",
            "",
            f"- {TICK}None{TICK}",
            "",
        )
    )


def _root(tmp_path: Path, *, newline: str = "\n", checkpoint: str = "checkpoint-0") -> Path:
    planning = tmp_path / ".planning"
    planning.mkdir()
    (planning / "ACTIVE.md").write_bytes(
        _active_text(newline=newline, checkpoint=checkpoint).encode("utf-8")
    )
    return tmp_path


def _guidance(
    *,
    capability_state: str = "ALLOWED",
    owner: str = "change-owner",
    ref: str = ".planning/ACTIVE.md#Active change",
) -> dict[str, object]:
    return {
        "outcome": "MATCHED",
        "authority": {"predicate_result": "AUTHORIZED_FOR_THIS_OPERATION"},
        "capabilities": [
            {"capability_id": "GOVERNANCE_WRITE", "state": capability_state}
        ],
        "guidance": {
            "next_gate_owner_ref": owner,
            "next_gate_ref": ref,
        },
    }


def _checkpoint(*, reasons: tuple[str, ...] = ("ALL_REQUIRED_PASS",)) -> PostEvaluationCheckpointV1:
    return PostEvaluationCheckpointV1(
        attempt_id="CHG-TEST-001/T-01/A1",
        result_id="RESULT-1",
        evaluation_id="EVALUATION-1",
        evaluation_outcome="SATISFIED",
        evaluation_reason_codes=reasons,
    )


def test_snapshot_reads_exact_authority_and_raw_sha(tmp_path: Path) -> None:
    root = _root(tmp_path)
    snapshot = capture_project_spine_snapshot(root)
    raw = (root / ".planning/ACTIVE.md").read_bytes()

    assert snapshot.active_change == "CHG-TEST-001"
    assert snapshot.lifecycle_stage == "Implementation"
    assert snapshot.stage_status == "Ready"
    assert snapshot.next_gate == "Central Candidate Review Gate"
    assert snapshot.next_permitted_action == "Run T-01"
    assert snapshot.implementation_authorized is False
    assert snapshot.active_context_path == ".planning/changes/active/CHG-TEST-001/context.md"
    assert snapshot.active_sha256 == hashlib.sha256(raw).hexdigest().upper()


def test_checkpoint_changes_only_one_field_and_preserves_lf_bytes(tmp_path: Path) -> None:
    root = _root(tmp_path)
    before = (root / ".planning/ACTIVE.md").read_bytes()
    snapshot = capture_project_spine_snapshot(root)

    after_snapshot = record_post_evaluation_checkpoint(
        root,
        pre_execution_snapshot=snapshot,
        checkpoint=_checkpoint(reasons=("FIRST", "SECOND")),
        operation_guidance=_guidance(),
    )
    after = (root / ".planning/ACTIVE.md").read_bytes()
    expected_line = (
        "- Last verified checkpoint: " + TICK + "POST_PL08 attempt=CHG-TEST-001/T-01/A1 "
        "result=RESULT-1 evaluation=EVALUATION-1 outcome=SATISFIED "
        "reasons=FIRST,SECOND" + TICK
    ).encode()
    assert expected_line in after
    assert after.count(b"\n") == before.count(b"\n")
    assert after_snapshot.active_sha256 == hashlib.sha256(after).hexdigest().upper()
    assert after_snapshot.next_gate == snapshot.next_gate
    assert after_snapshot.next_permitted_action == snapshot.next_permitted_action
    assert after_snapshot.lifecycle_stage == snapshot.lifecycle_stage
    assert after_snapshot.implementation_authorized == snapshot.implementation_authorized
    assert after != before


def test_checkpoint_preserves_crlf_and_empty_reasons(tmp_path: Path) -> None:
    root = _root(tmp_path, newline="\r\n")
    snapshot = capture_project_spine_snapshot(root)
    record_post_evaluation_checkpoint(
        root,
        pre_execution_snapshot=snapshot,
        checkpoint=_checkpoint(reasons=()),
        operation_guidance=_guidance(),
    )
    raw = (root / ".planning/ACTIVE.md").read_bytes()
    assert (b"reasons=NONE" + TICK.encode()) in raw
    assert b"\r\n" in raw
    assert b"\n" not in raw.replace(b"\r\n", b"")


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"capability_state": "FORBIDDEN"}, "GOVERNANCE_WRITE"),
        ({"owner": "lifecycle"}, "next_gate_owner_ref"),
        ({"ref": ".planning/other.md"}, "next_gate_ref"),
    ],
)
def test_checkpoint_authorization_is_fail_closed(
    tmp_path: Path, kwargs: dict[str, str], message: str
) -> None:
    root = _root(tmp_path)
    snapshot = capture_project_spine_snapshot(root)
    before = (root / ".planning/ACTIVE.md").read_bytes()
    with pytest.raises(ProjectSpineHandoffError, match=message):
        record_post_evaluation_checkpoint(
            root,
            pre_execution_snapshot=snapshot,
            checkpoint=_checkpoint(),
            operation_guidance=_guidance(**kwargs),
        )
    assert (root / ".planning/ACTIVE.md").read_bytes() == before


def test_stale_sha_and_changed_owner_state_fail_before_write(tmp_path: Path) -> None:
    root = _root(tmp_path)
    snapshot = capture_project_spine_snapshot(root)
    active = root / ".planning/ACTIVE.md"
    active.write_bytes(active.read_bytes().replace(b"Next gate: " + TICK.encode() + b"Central", b"Next gate: " + TICK.encode() + b"Changed"))
    before = active.read_bytes()
    with pytest.raises(ProjectSpineHandoffError):
        record_post_evaluation_checkpoint(
            root,
            pre_execution_snapshot=snapshot,
            checkpoint=_checkpoint(),
            operation_guidance=_guidance(),
        )
    assert active.read_bytes() == before


@pytest.mark.parametrize(
    "mutation",
    [
        lambda text: text.replace(
            "- Last verified checkpoint: " + TICK + "checkpoint-0" + TICK, ""
        ),
        lambda text: text.replace(
            "- Last verified checkpoint: " + TICK + "checkpoint-0" + TICK,
            "- Last verified checkpoint: " + TICK + "checkpoint-0" + TICK
            + "\n- Last verified checkpoint: " + TICK + "duplicate" + TICK,
        ),
        lambda text: text.replace(
            "- Next gate: " + TICK + "Central Candidate Review Gate" + TICK, ""
        ),
        lambda text: text.replace("## Active change", "## Active change\n## Active change"),
    ],
)
def test_malformed_or_ambiguous_active_fails_closed(tmp_path: Path, mutation) -> None:
    root = _root(tmp_path)
    active = root / ".planning/ACTIVE.md"
    active.write_text(mutation(active.read_text(encoding="utf-8")), encoding="utf-8")
    with pytest.raises(ProjectSpineHandoffError):
        capture_project_spine_snapshot(root)


@pytest.mark.parametrize(
    "checkpoint",
    [
        {"evaluation_reason_codes": ["NOT_A_TUPLE"]},
        {"attempt_id": ""},
        {"result_id": "bad\nline"},
        {"evaluation_reason_codes": ("",)},
    ],
)
def test_invalid_checkpoint_carrier_fails_closed(checkpoint: dict[str, object]) -> None:
    values: dict[str, object] = {
        "attempt_id": "A",
        "result_id": "R",
        "evaluation_id": "E",
        "evaluation_outcome": "SATISFIED",
        "evaluation_reason_codes": ("PASS",),
    }
    values.update(checkpoint)
    with pytest.raises(ProjectSpineHandoffError):
        PostEvaluationCheckpointV1(**values)


def test_snapshot_carrier_rejects_invalid_hash() -> None:
    with pytest.raises(ProjectSpineHandoffError):
        ProjectSpineSnapshotV1(
            "C",
            "Implementation",
            "Ready",
            "Gate",
            "Action",
            False,
            ".planning/context.md",
            "not-a-sha",
        )
