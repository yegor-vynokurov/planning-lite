from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLANNING = ROOT / "template/.planning"

BR = PLANNING / "assessments/BROWNFIELD_RECOVERY_TEMPLATE.md"
OL = PLANNING / "assessments/OUTCOME_LADDER_TEMPLATE.md"
DI = PLANNING / "control/DIRECTION_INVENTORY.md"
TE = PLANNING / "control/TARGET_STATE_EXPLORER.md"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")


def collapsed(path: Path) -> str:
    return re.sub(r"\s+", " ", read(path)).strip()


def test_s1_existing_accepted_direction_bypasses_brownfield_archaeology():
    recovery = collapsed(BR)
    inventory = collapsed(DI)
    assert "REUSE_CURRENT_ACCEPTED_DIRECTION" in recovery
    assert "REUSE_CURRENT_ACCEPTED_DIRECTION" in inventory
    assert "Historical recovery is not required merely because older artifacts exist." in inventory
    assert "BR-STOP-01" in inventory
    assert "sufficient current accepted authority exists" in inventory


def test_s2_recoverable_direction_remains_provisional_and_only_grounds_provisional_ladder():
    recovery = collapsed(BR)
    ladder = collapsed(OL)
    inventory = collapsed(DI)
    explorer = collapsed(TE)
    assert "RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL" in recovery
    assert "RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL" in inventory
    assert "Recovery alone must never promote this candidate to accepted Target intent." in inventory
    assert "RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL → provisional ladder" in ladder
    assert "If the grounding direction is provisional, the ladder is provisional." in explorer
    assert "ladder generation → cannot accept Target or authorize work" in ladder


def test_s3_material_authority_conflict_stops_and_is_not_silently_merged():
    recovery = collapsed(BR)
    inventory = collapsed(DI)
    assert "BLOCKED_DIRECTION_CONFLICT" in recovery
    assert "BR-STOP-03" in recovery
    assert "BR-STOP-03" in inventory
    assert "Do not silently merge conflicting authorities." in recovery
    assert "Do not silently normalize competing authorities." in inventory
    assert "surface the conflict and route to clarification/user decision" in inventory


def test_s4_large_irrelevant_history_does_not_force_repository_archaeology():
    recovery = collapsed(BR)
    inventory = collapsed(DI)
    assert "Do not load full project history by default." in recovery
    assert "Read only history/provenance that can materially affect current direction shaping." in inventory
    assert "History volume, file age, or minor unrelated drift do not by themselves invalidate" in recovery
    assert "BR-STOP-02" in inventory


def test_s5_outcome_ladder_rejects_task_shaped_levels():
    ladder = collapsed(OL)
    explorer = collapsed(TE)
    assert "What observable project outcome is true at this level?" in explorer
    assert "What should we implement next?" in explorer
    assert "Reject or reframe task lists" in explorer
    for task in ("implement API", "add tests", "write docs"):
        assert task in ladder
    assert "They are not ladder levels." in ladder
    assert "Minimum useful stopping level" in ladder


def test_s1_s5_do_not_pull_later_shaping_into_pl_v39_05_b():
    explorer = re.sub(r"\s+", " ", read(TE))
    for deferred in (
        "Adaptive Engagement",
        "Strategy Portfolio",
        "Target Skeleton",
        "Executable Target Contract",
    ):
        assert deferred in explorer
    assert "remain later work" in explorer
