from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping

from .campaign import (
    CampaignError,
    CampaignManifest,
    JournalEvent,
    load_campaign_journal,
    load_campaign_manifest,
)
from .campaign_suite import PROMOTION_VERDICT_STATUSES


CANDIDATE_REVIEW_SCHEMA_VERSION = 1
CANDIDATE_REVIEW_GATE_VERSION = "candidate-review-gate-v1"
REQUIRED_INDEPENDENT_ATTEMPTS = 3
NEGATIVE_VERDICT_STATUSES = frozenset({"retain-baseline", "reject-candidates"})
UNCERTAIN_VERDICT_STATUSES = frozenset({"continue-experiment", "inconclusive"})
KNOWN_VERDICT_STATUSES = (
    PROMOTION_VERDICT_STATUSES
    | NEGATIVE_VERDICT_STATUSES
    | UNCERTAIN_VERDICT_STATUSES
)
REQUIRED_SUITE_EVIDENCE_FILES = frozenset(
    {
        "suite-plan.json",
        "suite-state.json",
        "suite-result.json",
        "suite-aggregation.json",
        "suite-report.json",
        "suite-verdict.json",
    }
)
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class CandidateReviewError(CampaignError):
    """Raised when a deterministic candidate review cannot be constructed safely."""


@dataclass(frozen=True)
class CandidateAttemptReview:
    sequence: int
    event_sha256: str
    attempt_id: str
    suite_id: str | None
    suite_root: str | None
    eval_id: str | None
    source_commit: str | None
    plan_sha256: str | None
    verdict_status: str | None
    recommended_arm: str | None
    hard_gate_passed: bool
    improved: bool
    evidence_sha256: dict[str, str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CandidateReviewProposal:
    schema_version: int
    gate_version: str
    campaign_id: str
    manifest_sha256: str
    journal_head_sha256: str
    candidate_id: str
    hypothesis_id: str
    required_attempts: int
    observed_attempts: int
    independent_attempts: int
    decision: str
    operational_meaning: str
    promotion_status: str
    summary: str
    reason_codes: tuple[str, ...]
    attempts: tuple[CandidateAttemptReview, ...]
    review_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("review_sha256", None)
        payload["reason_codes"] = list(self.reason_codes)
        payload["attempts"] = [item.to_dict() for item in self.attempts]
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned_dict(), "review_sha256": self.review_sha256}


def review_campaign_candidate(
    campaign_root: Path,
    *,
    candidate_id: str | None = None,
) -> CandidateReviewProposal:
    """Build a deterministic keep/reject/continue proposal from sealed suite evidence.

    This function never appends campaign events and never promotes a candidate.
    ``keep`` means only ``keep-for-independent-review``.
    """

    root = campaign_root.resolve()
    manifest = load_campaign_manifest(root)
    events = load_campaign_journal(root, manifest=manifest)
    resolved_candidate = candidate_id or _current_candidate_id(events)
    if not resolved_candidate:
        raise CandidateReviewError("Campaign has no candidate to review")

    candidate_event = _candidate_registration(events, resolved_candidate)
    if candidate_event is None:
        raise CandidateReviewError(
            f"Candidate {resolved_candidate!r} is not registered in the campaign journal"
        )
    hypothesis_id = _required_string(
        candidate_event.payload.get("hypothesis_id"),
        "candidate_registered.hypothesis_id",
    )

    terminal_decision = _candidate_terminal_decision(events, resolved_candidate)
    if terminal_decision is not None:
        raise CandidateReviewError(
            f"Candidate {resolved_candidate!r} already has terminal review event "
            f"{terminal_decision.event_type!r}"
        )

    latest_receipt = next(
        (
            event
            for event in reversed(events)
            if event.event_type == "candidate_reviewed"
            and event.payload.get("candidate_id") == resolved_candidate
        ),
        None,
    )
    latest_completion = next(
        (
            event
            for event in reversed(events)
            if event.event_type == "attempt_completed"
            and event.payload.get("candidate_id") == resolved_candidate
        ),
        None,
    )
    if latest_receipt is not None and (
        latest_completion is None or latest_receipt.sequence > latest_completion.sequence
    ):
        raise CandidateReviewError(
            f"Candidate {resolved_candidate!r} already has a review receipt for current evidence"
        )

    completed = tuple(
        _attempt_from_event(event)
        for event in events
        if event.event_type == "attempt_completed"
        and event.payload.get("candidate_id") == resolved_candidate
    )
    started_ids = {
        _required_string(event.payload.get("attempt_id"), "attempt_started.attempt_id")
        for event in events
        if event.event_type == "attempt_started"
        and event.payload.get("candidate_id") == resolved_candidate
    }
    completed_ids = {item.attempt_id for item in completed}
    open_attempt_ids = tuple(sorted(started_ids - completed_ids))

    decision, summary, reason_codes, independent_attempts = _decide(
        manifest=manifest,
        attempts=completed,
        open_attempt_ids=open_attempt_ids,
    )
    unsigned = {
        "schema_version": CANDIDATE_REVIEW_SCHEMA_VERSION,
        "gate_version": CANDIDATE_REVIEW_GATE_VERSION,
        "campaign_id": manifest.campaign_id,
        "manifest_sha256": manifest.manifest_sha256,
        "journal_head_sha256": events[-1].event_sha256,
        "candidate_id": resolved_candidate,
        "hypothesis_id": hypothesis_id,
        "required_attempts": REQUIRED_INDEPENDENT_ATTEMPTS,
        "observed_attempts": len(completed),
        "independent_attempts": independent_attempts,
        "decision": decision,
        "operational_meaning": (
            "keep-for-independent-review"
            if decision == "keep"
            else "reject-candidate"
            if decision == "reject"
            else "collect-or-reconcile-evidence"
        ),
        "promotion_status": "not_requested",
        "summary": summary,
        "reason_codes": list(reason_codes),
        "attempts": [item.to_dict() for item in completed],
    }
    review_sha256 = _sha256_json(unsigned)
    return CandidateReviewProposal(
        **{
            **unsigned,
            "reason_codes": tuple(reason_codes),
            "attempts": completed,
            "review_sha256": review_sha256,
        }
    )


def write_candidate_review(
    path: Path,
    proposal: CandidateReviewProposal,
    *,
    replace: bool = False,
) -> Path:
    """Atomically write a deterministic review artifact.

    Re-writing the exact same artifact is idempotent. A different artifact requires
    explicit ``replace=True`` because its journal-head binding changed.
    """

    target = path.resolve()
    text = json.dumps(
        proposal.to_dict(),
        ensure_ascii=False,
        sort_keys=True,
        indent=2,
    ) + "\n"
    if target.exists():
        existing = target.read_text(encoding="utf-8")
        if existing == text:
            return target
        if not replace:
            raise CandidateReviewError(
                f"Candidate review artifact already exists with different content: {target}"
            )
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    temporary.write_text(text, encoding="utf-8", newline="")
    temporary.replace(target)
    return target


def _decide(
    *,
    manifest: CampaignManifest,
    attempts: tuple[CandidateAttemptReview, ...],
    open_attempt_ids: tuple[str, ...],
) -> tuple[str, str, tuple[str, ...], int]:
    reasons: list[str] = []

    if manifest.budget.max_attempts_per_candidate < REQUIRED_INDEPENDENT_ATTEMPTS:
        reasons.append("campaign_budget_below_three_attempts")

    if open_attempt_ids:
        reasons.extend(f"attempt_open={attempt_id}" for attempt_id in open_attempt_ids)

    if any(not item.hard_gate_passed for item in attempts):
        reasons.append("hard_gate_failure")
        return (
            "reject",
            "At least one completed suite failed a hard gate; the candidate is not eligible for keep-for-review.",
            tuple(dict.fromkeys(reasons)),
            _independent_attempt_count(attempts),
        )

    independent_count, independence_reasons = _independence(attempts)
    reasons.extend(independence_reasons)

    if len(attempts) < REQUIRED_INDEPENDENT_ATTEMPTS:
        reasons.append(
            f"completed_attempts={len(attempts)}/{REQUIRED_INDEPENDENT_ATTEMPTS}"
        )
        return (
            "continue",
            "Fewer than three completed independent suite attempts are available.",
            tuple(dict.fromkeys(reasons)),
            independent_count,
        )

    selected = attempts[-REQUIRED_INDEPENDENT_ATTEMPTS:]
    evidence_reasons = _evidence_completeness_reasons(selected)
    if evidence_reasons:
        reasons.extend(evidence_reasons)
        return (
            "continue",
            "Completed attempts are missing sealed suite identity or evidence hashes.",
            tuple(dict.fromkeys(reasons)),
            independent_count,
        )

    if independent_count < REQUIRED_INDEPENDENT_ATTEMPTS:
        reasons.append(
            f"independent_attempts={independent_count}/{REQUIRED_INDEPENDENT_ATTEMPTS}"
        )
        return (
            "continue",
            "Three completed records exist, but they do not establish three independent suite attempts.",
            tuple(dict.fromkeys(reasons)),
            independent_count,
        )

    eval_ids = {item.eval_id for item in selected}
    source_commits = {item.source_commit for item in selected}
    if len(eval_ids) != 1:
        reasons.append("eval_id_inconsistent")
    if len(source_commits) != 1:
        reasons.append("source_commit_inconsistent")
    if reasons:
        return (
            "continue",
            "The three attempts do not evaluate one stable candidate under one pinned suite context.",
            tuple(dict.fromkeys(reasons)),
            independent_count,
        )

    statuses = tuple(item.verdict_status for item in selected)
    unknown = tuple(sorted({item for item in statuses if item not in KNOWN_VERDICT_STATUSES}))
    if unknown:
        reasons.extend(f"unsupported_verdict_status={item}" for item in unknown)
        return (
            "continue",
            "At least one suite verdict is not recognized by the fixed review gate.",
            tuple(dict.fromkeys(reasons)),
            independent_count,
        )

    if all(status in NEGATIVE_VERDICT_STATUSES for status in statuses):
        reasons.append("three_conclusive_negative_verdicts")
        return (
            "reject",
            "All three independent suites produced conclusive non-promotion verdicts.",
            tuple(dict.fromkeys(reasons)),
            independent_count,
        )

    if all(status in PROMOTION_VERDICT_STATUSES for status in statuses):
        status_set = set(statuses)
        recommended_arms = {item.recommended_arm for item in selected}
        if None in recommended_arms:
            reasons.append("positive_verdict_missing_recommended_arm")
        if len(status_set) != 1:
            reasons.append("positive_verdict_status_inconsistent")
        if len(recommended_arms) != 1:
            reasons.append("recommended_arm_inconsistent")
        if reasons:
            return (
                "continue",
                "Positive suite results are not mutually consistent enough for keep-for-review.",
                tuple(dict.fromkeys(reasons)),
                independent_count,
            )
        reasons.extend(
            (
                "three_independent_attempts",
                "all_hard_gates_passed",
                "three_consistent_positive_verdicts",
                f"recommended_arm={selected[0].recommended_arm}",
                "keep_is_not_promotion",
            )
        )
        return (
            "keep",
            "Three independent suites passed hard gates and produced the same positive fixture-scoped recommendation. Keep the candidate only for a later independent review gate.",
            tuple(dict.fromkeys(reasons)),
            independent_count,
        )

    if any(status in UNCERTAIN_VERDICT_STATUSES for status in statuses):
        reasons.append("uncertain_suite_verdict_present")
    if any(status in PROMOTION_VERDICT_STATUSES for status in statuses) and any(
        status in NEGATIVE_VERDICT_STATUSES for status in statuses
    ):
        reasons.append("positive_negative_verdict_conflict")
    if not reasons:
        reasons.append("verdicts_not_unanimous")
    return (
        "continue",
        "The three attempts are complete, but their verdicts do not support a unanimous keep or reject proposal.",
        tuple(dict.fromkeys(reasons)),
        independent_count,
    )


def _independence(
    attempts: tuple[CandidateAttemptReview, ...],
) -> tuple[int, tuple[str, ...]]:
    reasons: list[str] = []
    suite_ids = [item.suite_id for item in attempts if item.suite_id]
    suite_roots = [item.suite_root for item in attempts if item.suite_root]
    evidence_fingerprints = [
        _evidence_fingerprint(item.evidence_sha256)
        for item in attempts
        if item.evidence_sha256
    ]
    if len(suite_ids) != len(set(suite_ids)):
        reasons.append("duplicate_suite_id")
    if len(suite_roots) != len(set(suite_roots)):
        reasons.append("duplicate_suite_root")
    if len(evidence_fingerprints) != len(set(evidence_fingerprints)):
        reasons.append("duplicate_evidence_fingerprint")
    independent_count = min(
        len(set(suite_ids)),
        len(set(suite_roots)),
        len(set(evidence_fingerprints)),
        len(attempts),
    )
    return independent_count, tuple(reasons)


def _evidence_fingerprint(evidence_sha256: Mapping[str, str]) -> str:
    return _sha256_json(dict(sorted(evidence_sha256.items())))


def _independent_attempt_count(attempts: tuple[CandidateAttemptReview, ...]) -> int:
    return _independence(attempts)[0]


def _evidence_completeness_reasons(
    attempts: Iterable[CandidateAttemptReview],
) -> tuple[str, ...]:
    reasons: list[str] = []
    for item in attempts:
        prefix = f"attempt={item.attempt_id}"
        for name, value in (
            ("suite_id", item.suite_id),
            ("suite_root", item.suite_root),
            ("eval_id", item.eval_id),
            ("source_commit", item.source_commit),
            ("plan_sha256", item.plan_sha256),
            ("verdict_status", item.verdict_status),
        ):
            if not value:
                reasons.append(f"{prefix}:missing_{name}")
        if item.plan_sha256 and not SHA256_RE.fullmatch(item.plan_sha256):
            reasons.append(f"{prefix}:invalid_plan_sha256")
        if item.verdict_status in KNOWN_VERDICT_STATUSES:
            expected_improved = item.verdict_status in PROMOTION_VERDICT_STATUSES
            if item.improved != expected_improved:
                reasons.append(f"{prefix}:improved_flag_verdict_mismatch")
        observed_files = set(item.evidence_sha256)
        missing = REQUIRED_SUITE_EVIDENCE_FILES - observed_files
        if missing:
            reasons.extend(f"{prefix}:missing_evidence={name}" for name in sorted(missing))
        for name, digest in sorted(item.evidence_sha256.items()):
            if not SHA256_RE.fullmatch(digest):
                reasons.append(f"{prefix}:invalid_evidence_sha256={name}")
    return tuple(reasons)


def _attempt_from_event(event: JournalEvent) -> CandidateAttemptReview:
    suite = event.payload.get("suite")
    suite_payload = suite if isinstance(suite, Mapping) else {}
    evidence = suite_payload.get("evidence_sha256")
    evidence_payload = evidence if isinstance(evidence, Mapping) else {}
    normalized_evidence = {
        str(name): str(digest).lower()
        for name, digest in evidence_payload.items()
        if isinstance(name, str) and isinstance(digest, str)
    }
    verdict_status = _optional_string(suite_payload.get("verdict_status"))
    recommended_arm = _optional_string(suite_payload.get("recommended_arm"))
    hard_gate = event.payload.get("hard_gate_passed")
    improved = event.payload.get("improved")
    if not isinstance(hard_gate, bool) or not isinstance(improved, bool):
        raise CandidateReviewError(
            f"attempt_completed event {event.sequence} has invalid gate booleans"
        )
    return CandidateAttemptReview(
        sequence=event.sequence,
        event_sha256=event.event_sha256,
        attempt_id=_required_string(event.payload.get("attempt_id"), "attempt_id"),
        suite_id=_optional_string(suite_payload.get("suite_id")),
        suite_root=_optional_string(suite_payload.get("suite_root")),
        eval_id=_optional_string(suite_payload.get("eval_id")),
        source_commit=_optional_string(suite_payload.get("source_commit")),
        plan_sha256=_optional_string(suite_payload.get("plan_sha256")),
        verdict_status=verdict_status,
        recommended_arm=recommended_arm,
        hard_gate_passed=hard_gate,
        improved=improved,
        evidence_sha256=normalized_evidence,
    )


def _current_candidate_id(events: tuple[JournalEvent, ...]) -> str | None:
    for event in reversed(events):
        candidate_id = _optional_string(event.payload.get("candidate_id"))
        if candidate_id:
            return candidate_id
    return None


def _candidate_registration(
    events: tuple[JournalEvent, ...], candidate_id: str
) -> JournalEvent | None:
    for event in events:
        if (
            event.event_type == "candidate_registered"
            and event.payload.get("candidate_id") == candidate_id
        ):
            return event
    return None


def _candidate_terminal_decision(
    events: tuple[JournalEvent, ...], candidate_id: str
) -> JournalEvent | None:
    for event in reversed(events):
        if (
            event.event_type
            in {"candidate_kept", "candidate_rejected", "candidate_quarantined"}
            and event.payload.get("candidate_id") == candidate_id
        ):
            return event
    return None


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CandidateReviewError(f"{label} must be a non-empty string")
    return value.strip()


def _optional_string(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def _sha256_json(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
