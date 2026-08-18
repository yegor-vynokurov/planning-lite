from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .campaign import (
    CampaignError,
    append_campaign_event,
    inspect_campaign,
    load_campaign_journal,
    load_campaign_manifest,
)

REQUIRED_SUITE_EVIDENCE_FILES = (
    "suite-plan.json",
    "suite-state.json",
    "suite-result.json",
    "suite-aggregation.json",
    "suite-report.json",
    "suite-verdict.json",
)
TERMINAL_RUN_STATUSES = frozenset({"passed", "failed", "error"})


class AttemptEvidenceReconciliationError(CampaignError):
    """Raised when historical suite evidence cannot be reconciled safely."""


def reconcile_completed_attempt_suite_evidence(
    *,
    campaign_root: Path,
    candidate_id: str,
    attempt_id: str,
    suite_root: Path,
    expected_source_event_sha256: str | None = None,
):
    """Append native suite provenance for a legacy completed attempt.

    This is append-only. It never rewrites the historical ``attempt_completed``
    event and never changes attempt counters or accounting. The reconciliation is
    permitted only when the historical completion has no native ``suite`` block.
    """

    root = campaign_root.resolve()
    suite = suite_root.resolve()
    manifest = load_campaign_manifest(root)
    events = load_campaign_journal(root, manifest=manifest)

    completions = [
        event
        for event in events
        if event.event_type == "attempt_completed"
        and event.payload.get("candidate_id") == candidate_id
        and event.payload.get("attempt_id") == attempt_id
    ]
    if len(completions) != 1:
        raise AttemptEvidenceReconciliationError(
            f"Expected exactly one historical completion for {attempt_id!r}, got {len(completions)}"
        )
    source = completions[0]
    if source.payload.get("suite") is not None:
        raise AttemptEvidenceReconciliationError(
            f"Attempt {attempt_id!r} already has native suite provenance"
        )
    if expected_source_event_sha256 is not None and source.event_sha256 != expected_source_event_sha256:
        raise AttemptEvidenceReconciliationError(
            "Historical completion event SHA does not match the expected binding"
        )

    suite_payload = build_reconciled_suite_payload(suite)

    starts = [
        event
        for event in events
        if event.event_type == "attempt_started"
        and event.payload.get("candidate_id") == candidate_id
        and event.payload.get("attempt_id") == attempt_id
    ]
    if len(starts) != 1:
        raise AttemptEvidenceReconciliationError(
            f"Expected exactly one historical start for {attempt_id!r}, got {len(starts)}"
        )
    start_suite = starts[0].payload.get("suite")
    if start_suite is not None:
        if not isinstance(start_suite, Mapping):
            raise AttemptEvidenceReconciliationError(
                f"Historical start suite provenance for {attempt_id!r} must be an object"
            )
        for key in ("suite_id", "eval_id", "source_commit", "suite_root", "plan_sha256"):
            if start_suite.get(key) != suite_payload.get(key):
                raise AttemptEvidenceReconciliationError(
                    f"Reconciled suite {key} does not match historical attempt_started provenance"
                )

    payload = {
        "candidate_id": candidate_id,
        "attempt_id": attempt_id,
        "source_attempt_completed_sequence": source.sequence,
        "source_attempt_completed_event_sha256": source.event_sha256,
        "suite": suite_payload,
        "adapter": "balanced-suite-reconciliation-v1",
        "reason": "historical_suite_projection_reconciliation",
        "next_action": "start_next_independent_attempt",
    }

    existing = [
        event
        for event in events
        if event.event_type == "attempt_evidence_reconciled"
        and event.payload.get("candidate_id") == candidate_id
        and event.payload.get("attempt_id") == attempt_id
    ]
    if existing:
        if len(existing) != 1 or existing[0].payload != payload:
            raise AttemptEvidenceReconciliationError(
                f"Attempt {attempt_id!r} already has different reconciled suite evidence"
            )
        return inspect_campaign(root)

    return append_campaign_event(
        campaign_root=root,
        event_type="attempt_evidence_reconciled",
        payload=payload,
    )


def build_reconciled_suite_payload(suite_root: Path) -> dict[str, Any]:
    root = suite_root.resolve()
    if not root.is_dir():
        raise AttemptEvidenceReconciliationError(f"Suite root was not found: {root}")

    plan = _read_json(root / "suite-plan.json", "suite plan")
    state = _read_json(root / "suite-state.json", "suite state")
    verdict = _read_json(root / "suite-verdict.json", "suite verdict")

    suite_id = _required_string(plan.get("suite_id"), "suite-plan.suite_id")
    eval_id = _required_string(plan.get("eval_id"), "suite-plan.eval_id")
    source_commit = _required_string(plan.get("source_commit"), "suite-plan.source_commit")
    plan_sha256 = _required_string(plan.get("plan_sha256"), "suite-plan.plan_sha256")
    if len(plan_sha256) != 64:
        raise AttemptEvidenceReconciliationError("suite-plan.plan_sha256 must be a SHA-256")

    state_suite_id = state.get("suite_id")
    if state_suite_id is not None and state_suite_id != suite_id:
        raise AttemptEvidenceReconciliationError("suite state suite_id does not match suite plan")
    state_eval_id = state.get("eval_id")
    if state_eval_id is not None and state_eval_id != eval_id:
        raise AttemptEvidenceReconciliationError("suite state eval_id does not match suite plan")

    suite_status = _required_string(state.get("status"), "suite-state.status")
    runs = state.get("runs")
    if not isinstance(runs, list) or not runs:
        raise AttemptEvidenceReconciliationError("suite-state.runs must be a non-empty list")
    statuses: list[str] = []
    for index, run in enumerate(runs, start=1):
        if not isinstance(run, Mapping):
            raise AttemptEvidenceReconciliationError(f"suite-state run {index} must be an object")
        statuses.append(_required_string(run.get("status"), f"suite-state.runs[{index}].status"))

    counts = {name: statuses.count(name) for name in TERMINAL_RUN_STATUSES}
    terminal_runs = sum(counts.values())
    total_runs = len(statuses)
    if terminal_runs != total_runs:
        raise AttemptEvidenceReconciliationError(
            f"Historical suite is not terminal: {terminal_runs}/{total_runs} terminal runs"
        )

    verdict_status = _required_string(verdict.get("status"), "suite-verdict.status")
    recommended_arm = verdict.get("recommended_arm")
    if recommended_arm is not None and (not isinstance(recommended_arm, str) or not recommended_arm.strip()):
        raise AttemptEvidenceReconciliationError(
            "suite-verdict.recommended_arm must be a non-empty string or null"
        )

    evidence = {}
    for name in REQUIRED_SUITE_EVIDENCE_FILES:
        path = root / name
        if not path.is_file():
            raise AttemptEvidenceReconciliationError(f"Required suite evidence was not found: {path}")
        evidence[name] = _sha256_file(path)

    return {
        "suite_id": suite_id,
        "eval_id": eval_id,
        "source_commit": source_commit,
        "suite_root": str(root),
        "plan_sha256": plan_sha256,
        "suite_status": suite_status,
        "total_runs": total_runs,
        "terminal_runs": terminal_runs,
        "passed_runs": counts["passed"],
        "failed_runs": counts["failed"],
        "error_runs": counts["error"],
        "verdict_status": verdict_status,
        "recommended_arm": recommended_arm,
        "evidence_sha256": evidence,
    }


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as exc:
        raise AttemptEvidenceReconciliationError(f"Required {label} was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise AttemptEvidenceReconciliationError(f"Invalid {label}: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise AttemptEvidenceReconciliationError(f"{label} root must be an object: {path}")
    return value


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise AttemptEvidenceReconciliationError(f"{label} must be a non-empty string")
    return value.strip()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()
