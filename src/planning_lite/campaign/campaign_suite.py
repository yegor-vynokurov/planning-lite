from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping

from .campaign import (
    CampaignError,
    JournalEvent,
    append_campaign_event,
    inspect_campaign,
    load_campaign_journal,
    load_campaign_manifest,
)



PROMOTION_VERDICT_STATUSES = frozenset({"promote-for-fixture", "promote-routing-policy"})
_REQUIRED_EVIDENCE_FILES = (
    "suite-plan.json",
    "suite-state.json",
    "suite-result.json",
    "suite-aggregation.json",
    "suite-report.json",
    "suite-verdict.json",
)


class CampaignSuiteError(CampaignError):
    """Raised when a suite cannot be linked to a campaign without ambiguity."""


@dataclass(frozen=True)
class CampaignSuiteBinding:
    campaign_root: Path
    hypothesis_id: str
    candidate_id: str
    attempt_id: str | None = None
    summary: str | None = None

    def resolved_attempt_id(self, suite_id: str) -> str:
        value = self.attempt_id or suite_id
        return _nonempty(value, "campaign attempt_id")

    def validate(self) -> None:
        _nonempty(str(self.campaign_root), "campaign_root")
        _nonempty(self.hypothesis_id, "campaign hypothesis_id")
        _nonempty(self.candidate_id, "campaign candidate_id")
        if self.attempt_id is not None:
            _nonempty(self.attempt_id, "campaign attempt_id")
        if self.summary is not None:
            _nonempty(self.summary, "campaign summary")


def start_campaign_suite_attempt(
    binding: CampaignSuiteBinding,
    *,
    suite_id: str,
    eval_id: str,
    source_commit: str,
    suite_root: Path,
    plan_sha256: str,
):
    """Idempotently register hypothesis, candidate, and one suite-level attempt.

    A campaign attempt represents one complete balanced suite, not one internal
    arm run. The existing suite runner remains the owner of its nine-run state.
    """

    binding.validate()
    campaign_root = binding.campaign_root.resolve()
    suite_root = suite_root.resolve()
    attempt_id = binding.resolved_attempt_id(suite_id)
    identity = _suite_identity(
        suite_id=suite_id,
        eval_id=eval_id,
        source_commit=source_commit,
        suite_root=suite_root,
        plan_sha256=plan_sha256,
    )

    manifest = load_campaign_manifest(campaign_root)
    events = load_campaign_journal(campaign_root, manifest=manifest)

    hypothesis = _find_event(events, "hypothesis_registered", "hypothesis_id", binding.hypothesis_id)
    if hypothesis is None:
        append_campaign_event(
            campaign_root=campaign_root,
            event_type="hypothesis_registered",
            payload={
                "hypothesis_id": binding.hypothesis_id,
                "summary": binding.summary or f"Evaluate {binding.candidate_id} with {eval_id}.",
                "adapter": "balanced-suite-v1",
            },
        )
        events = load_campaign_journal(campaign_root, manifest=manifest)

    candidate = _find_event(events, "candidate_registered", "candidate_id", binding.candidate_id)
    if candidate is None:
        append_campaign_event(
            campaign_root=campaign_root,
            event_type="candidate_registered",
            payload={
                "candidate_id": binding.candidate_id,
                "hypothesis_id": binding.hypothesis_id,
                "summary": binding.summary or f"Suite candidate {binding.candidate_id}.",
                "adapter": "balanced-suite-v1",
            },
        )
        events = load_campaign_journal(campaign_root, manifest=manifest)
    else:
        observed_hypothesis = candidate.payload.get("hypothesis_id")
        if observed_hypothesis != binding.hypothesis_id:
            raise CampaignSuiteError(
                f"Candidate {binding.candidate_id!r} is already bound to hypothesis "
                f"{observed_hypothesis!r}, not {binding.hypothesis_id!r}"
            )

    completed = _find_event(events, "attempt_completed", "attempt_id", attempt_id)
    if completed is not None:
        _verify_attempt_identity(completed, binding.candidate_id, identity)
        _verify_recorded_evidence(completed, suite_root)
        return inspect_campaign(campaign_root)

    started = _find_event(events, "attempt_started", "attempt_id", attempt_id)
    if started is not None:
        _verify_attempt_identity(started, binding.candidate_id, identity)
        return inspect_campaign(campaign_root)

    return append_campaign_event(
        campaign_root=campaign_root,
        event_type="attempt_started",
        payload={
            "candidate_id": binding.candidate_id,
            "attempt_id": attempt_id,
            "suite": identity,
            "adapter": "balanced-suite-v1",
        },
    )


def complete_campaign_suite_attempt(
    binding: CampaignSuiteBinding,
    result: "SuiteExecutionResult",
):
    """Record a terminal balanced suite as one campaign attempt.

    Incomplete suites remain as ``attempt_started`` so ``run-suite --resume`` can
    continue them. Candidate keep/reject decisions remain explicit review actions.
    """

    binding.validate()
    campaign_root = binding.campaign_root.resolve()
    suite_root = Path(result.suite_root).resolve()
    attempt_id = binding.resolved_attempt_id(result.suite_id)
    manifest = load_campaign_manifest(campaign_root)
    events = load_campaign_journal(campaign_root, manifest=manifest)

    completed = _find_event(events, "attempt_completed", "attempt_id", attempt_id)
    if completed is not None:
        _verify_attempt_identity(
            completed,
            binding.candidate_id,
            _suite_identity_from_artifacts(result, suite_root),
        )
        _verify_recorded_evidence(completed, suite_root)
        return inspect_campaign(campaign_root)

    started = _find_event(events, "attempt_started", "attempt_id", attempt_id)
    if started is None:
        raise CampaignSuiteError(
            f"Campaign attempt {attempt_id!r} was not started before suite completion"
        )
    _verify_attempt_identity(
        started,
        binding.candidate_id,
        _suite_identity_from_artifacts(result, suite_root),
    )

    if not result.all_runs_executed:
        return inspect_campaign(campaign_root)

    evidence = _collect_suite_evidence(suite_root)
    metrics = _collect_suite_metrics(suite_root)
    verdict = _read_json_object(suite_root / "suite-verdict.json", "suite verdict")
    verdict_status = _nonempty(verdict.get("status"), "suite verdict status")
    recommended_arm = verdict.get("recommended_arm")
    if recommended_arm is not None and not isinstance(recommended_arm, str):
        raise CampaignSuiteError("suite verdict recommended_arm must be a string or null")

    hard_gate_passed = result.error_runs == 0
    improved = verdict_status in PROMOTION_VERDICT_STATUSES
    suite_payload = {
        **_suite_identity_from_artifacts(result, suite_root),
        "suite_status": result.status,
        "total_runs": result.total_runs,
        "terminal_runs": result.terminal_runs,
        "passed_runs": result.passed_runs,
        "failed_runs": result.failed_runs,
        "error_runs": result.error_runs,
        "verdict_status": verdict_status,
        "recommended_arm": recommended_arm,
        "evidence_sha256": evidence,
    }
    return append_campaign_event(
        campaign_root=campaign_root,
        event_type="attempt_completed",
        payload={
            "candidate_id": binding.candidate_id,
            "attempt_id": attempt_id,
            "hard_gate_passed": hard_gate_passed,
            "improved": improved,
            "metrics": metrics,
            "suite": suite_payload,
            "adapter": "balanced-suite-v1",
        },
    )


def _suite_identity(
    *,
    suite_id: str,
    eval_id: str,
    source_commit: str,
    suite_root: Path,
    plan_sha256: str,
) -> dict[str, str]:
    return {
        "suite_id": _nonempty(suite_id, "suite_id"),
        "eval_id": _nonempty(eval_id, "eval_id"),
        "source_commit": _nonempty(source_commit, "source_commit"),
        "suite_root": str(suite_root.resolve()),
        "plan_sha256": _nonempty(plan_sha256, "plan_sha256"),
    }


def _suite_identity_from_artifacts(
    result: "SuiteExecutionResult",
    suite_root: Path,
) -> dict[str, str]:
    plan = _read_json_object(suite_root / "suite-plan.json", "suite plan")
    return _suite_identity(
        suite_id=result.suite_id,
        eval_id=result.eval_id,
        source_commit=_nonempty(plan.get("source_commit"), "suite plan source_commit"),
        suite_root=suite_root,
        plan_sha256=_nonempty(plan.get("plan_sha256"), "suite plan plan_sha256"),
    )


def _collect_suite_metrics(suite_root: Path) -> dict[str, int | float]:
    state = _read_json_object(suite_root / "suite-state.json", "suite state")
    runs = state.get("runs")
    if not isinstance(runs, list) or not runs:
        raise CampaignSuiteError("suite state must contain at least one run")

    total_tokens = 0
    for index, run in enumerate(runs, start=1):
        if not isinstance(run, Mapping):
            raise CampaignSuiteError(f"suite state run {index} must be an object")
        metrics_path_value = run.get("metrics_path")
        if not isinstance(metrics_path_value, str) or not metrics_path_value:
            record_dir = run.get("record_dir")
            if isinstance(record_dir, str) and record_dir:
                metrics_path_value = str(Path(record_dir) / "metrics.json")
            else:
                raise CampaignSuiteError(f"suite run {index} has no metrics path")
        metrics = _read_json_object(Path(metrics_path_value), f"suite run {index} metrics")
        tokens = metrics.get("tokens")
        value = tokens.get("total_tokens") if isinstance(tokens, Mapping) else None
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise CampaignSuiteError(
                f"suite run {index} total_tokens must be a non-negative integer"
            )
        total_tokens += value

    started = _parse_timestamp(state.get("started_at_utc"), "suite started_at_utc")
    completed = _parse_timestamp(state.get("completed_at_utc"), "suite completed_at_utc")
    duration = (completed - started).total_seconds()
    if duration < 0:
        raise CampaignSuiteError("suite completed_at_utc precedes started_at_utc")
    return {
        "total_tokens": total_tokens,
        "duration_seconds": round(duration, 6),
    }


def _collect_suite_evidence(suite_root: Path) -> dict[str, str]:
    evidence: dict[str, str] = {}
    for name in _REQUIRED_EVIDENCE_FILES:
        path = suite_root / name
        if not path.is_file():
            raise CampaignSuiteError(f"Required suite evidence was not found: {path}")
        evidence[name] = _sha256_file(path)
    return evidence


def _verify_attempt_identity(
    event: JournalEvent,
    candidate_id: str,
    expected_suite: Mapping[str, str],
) -> None:
    if event.payload.get("candidate_id") != candidate_id:
        raise CampaignSuiteError(
            f"Attempt {event.payload.get('attempt_id')!r} belongs to a different candidate"
        )
    observed = event.payload.get("suite")
    if not isinstance(observed, Mapping):
        raise CampaignSuiteError("Campaign suite event is missing suite identity")
    for field, expected in expected_suite.items():
        if observed.get(field) != expected:
            raise CampaignSuiteError(
                f"Campaign suite identity mismatch for {field}: "
                f"expected {expected!r}, got {observed.get(field)!r}"
            )


def _verify_recorded_evidence(event: JournalEvent, suite_root: Path) -> None:
    suite = event.payload.get("suite")
    if not isinstance(suite, Mapping):
        raise CampaignSuiteError("Completed campaign attempt is missing suite payload")
    recorded = suite.get("evidence_sha256")
    if recorded is None:
        # attempt_started events intentionally have no terminal evidence yet.
        return
    if not isinstance(recorded, Mapping):
        raise CampaignSuiteError("Completed campaign attempt evidence_sha256 must be an object")
    for name, expected in recorded.items():
        if not isinstance(name, str) or not isinstance(expected, str):
            raise CampaignSuiteError("Completed campaign attempt evidence hashes are invalid")
        path = suite_root / name
        if not path.is_file():
            raise CampaignSuiteError(f"Recorded suite evidence was not found: {path}")
        observed = _sha256_file(path)
        if observed != expected:
            raise CampaignSuiteError(
                f"Recorded suite evidence hash mismatch for {name}: "
                f"expected {expected}, got {observed}"
            )


def _find_event(
    events: tuple[JournalEvent, ...],
    event_type: str,
    field: str,
    value: str,
) -> JournalEvent | None:
    matches = [
        event
        for event in events
        if event.event_type == event_type and event.payload.get(field) == value
    ]
    if len(matches) > 1:
        raise CampaignSuiteError(
            f"Campaign journal contains duplicate {event_type} events for {field}={value!r}"
        )
    return matches[0] if matches else None


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CampaignSuiteError(f"{label} was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CampaignSuiteError(f"{label} is invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise CampaignSuiteError(f"{label} root must be an object: {path}")
    return payload


def _parse_timestamp(value: Any, label: str) -> datetime:
    if not isinstance(value, str) or not value:
        raise CampaignSuiteError(f"{label} must be a non-empty timestamp")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        return datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise CampaignSuiteError(f"{label} is not a valid ISO-8601 timestamp") from exc


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _nonempty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CampaignSuiteError(f"{label} must be a non-empty string")
    return value.strip()
