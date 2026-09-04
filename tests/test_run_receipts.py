from __future__ import annotations

import json
import multiprocessing as mp
from pathlib import Path

import pytest
import yaml

from planning_lite.telemetry import ReceiptError, append_receipt, collect_receipt
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
    receipt_path = info["telemetry"]["receipt_path"] or (home / "telemetry/demo/run-receipts.jsonl")
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
