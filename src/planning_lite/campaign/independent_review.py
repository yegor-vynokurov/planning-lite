from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass
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
from .review_receipt import (
    ReviewReceipt,
    ReviewHandoffCapsule,
    load_review_handoff,
    load_review_receipt,
)


INDEPENDENT_REVIEW_SCHEMA_VERSION = 1
INDEPENDENT_REVIEW_GATE_VERSION = "independent-review-decision-gate-v1"
INDEPENDENT_REVIEW_ROLE = "independent_reviewer"
INDEPENDENT_DECISIONS = frozenset(
    {"candidate_kept", "candidate_rejected", "candidate_quarantined"}
)
REQUIRED_EVIDENCE_FILES = frozenset(
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


class IndependentReviewError(CampaignError):
    """Raised when independent review cannot be bound safely to sealed evidence."""


@dataclass(frozen=True)
class IndependentReviewDecision:
    schema_version: int
    gate_version: str
    campaign_id: str
    manifest_sha256: str
    candidate_id: str
    hypothesis_id: str
    reviewer_id: str
    reviewer_role: str
    attestation: str
    decision: str
    promotion_status: str
    frozen_parent: dict[str, str | None]
    review_path: str
    review_sha256: str
    receipt_path: str
    receipt_sha256: str
    handoff_path: str
    handoff_sha256: str
    candidate_reviewed_event_sequence: int
    candidate_reviewed_event_sha256: str
    journal_head_sha256_before_decision: str
    verified_attempts: int
    verified_evidence_files: int
    restrictions: tuple[str, ...]
    decision_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("decision_sha256", None)
        payload["restrictions"] = list(self.restrictions)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned_dict(), "decision_sha256": self.decision_sha256}


@dataclass(frozen=True)
class IndependentReviewResult:
    status: str
    decision_path: Path
    decision: IndependentReviewDecision
    journal_appended: bool
    decision_event: JournalEvent
    next_action: str


def record_independent_review_decision(
    campaign_root: Path,
    *,
    decision: str,
    reviewer_id: str,
    attestation: str,
    decision_path: Path | None = None,
) -> IndependentReviewResult:
    """Verify the E1.4 handoff chain and append one explicit candidate decision.

    This gate never performs release promotion or mutates central Planning Lite.
    ``candidate_kept`` means only that the candidate was accepted by the
    independent review gate and is eligible for a later release/promotion gate.
    """

    root = campaign_root.resolve()
    manifest = load_campaign_manifest(root)
    events = load_campaign_journal(root, manifest=manifest)
    reviewer_id = _required_string(reviewer_id, "reviewer_id")
    attestation = _required_string(attestation, "attestation")
    if decision not in INDEPENDENT_DECISIONS:
        raise IndependentReviewError(
            "Independent review decision must be candidate_kept, "
            "candidate_rejected, or candidate_quarantined"
        )

    reviewed_event = _latest_candidate_reviewed(events)
    if reviewed_event is None:
        existing = _latest_independent_decision_event(events)
        if existing is not None:
            return _replay_existing_decision(
                root,
                manifest=manifest,
                events=events,
                existing_event=existing,
                decision=decision,
                reviewer_id=reviewer_id,
                attestation=attestation,
                decision_path=decision_path,
            )
        raise IndependentReviewError("Campaign has no candidate_reviewed handoff to review")

    if events[-1].event_sha256 != reviewed_event.event_sha256:
        existing = _decision_event_after(events, reviewed_event)
        if existing is not None:
            return _replay_existing_decision(
                root,
                manifest=manifest,
                events=events,
                existing_event=existing,
                decision=decision,
                reviewer_id=reviewer_id,
                attestation=attestation,
                decision_path=decision_path,
            )
        raise IndependentReviewError(
            "Independent review requires candidate_reviewed to be the current journal head"
        )

    if reviewed_event.payload.get("decision") != "keep":
        raise IndependentReviewError(
            "Independent review decision gate accepts only a keep-for-independent-review handoff"
        )
    if reviewed_event.payload.get("next_action") != "await_independent_review":
        raise IndependentReviewError(
            "candidate_reviewed event is not waiting for independent review"
        )
    if reviewed_event.payload.get("promotion_status") != "not_requested":
        raise IndependentReviewError("candidate_reviewed unexpectedly authorizes promotion")

    receipt_path = Path(
        _required_string(reviewed_event.payload.get("receipt_path"), "candidate_reviewed.receipt_path")
    ).resolve()
    handoff_path = Path(
        _required_string(reviewed_event.payload.get("handoff_path"), "candidate_reviewed.handoff_path")
    ).resolve()
    review_path = Path(
        _required_string(reviewed_event.payload.get("review_path"), "candidate_reviewed.review_path")
    ).resolve()
    receipt = load_review_receipt(receipt_path)
    handoff = load_review_handoff(handoff_path)
    review = _load_self_hashed_json(review_path, "review_sha256", "Candidate review")

    verified_evidence_files = _verify_chain(
        manifest=manifest,
        events=events,
        reviewed_event=reviewed_event,
        review=review,
        review_path=review_path,
        receipt=receipt,
        receipt_path=receipt_path,
        handoff=handoff,
        handoff_path=handoff_path,
    )

    resolved_decision_path = (
        decision_path
        or root / "independent-review-decisions" / f"{reviewed_event.event_sha256}.json"
    ).resolve()
    artifact = _build_decision(
        manifest=manifest,
        reviewed_event=reviewed_event,
        review_path=review_path,
        review=review,
        receipt_path=receipt_path,
        receipt=receipt,
        handoff_path=handoff_path,
        handoff=handoff,
        reviewer_id=reviewer_id,
        attestation=attestation,
        decision=decision,
        verified_evidence_files=verified_evidence_files,
    )
    _write_self_hashed_artifact(resolved_decision_path, artifact.to_dict())

    payload = {
        "candidate_id": handoff.candidate_id,
        "hypothesis_id": handoff.hypothesis_id,
        "reason": "independent_review_decision",
        "reviewer_id": reviewer_id,
        "reviewer_role": INDEPENDENT_REVIEW_ROLE,
        "decision_artifact_path": str(resolved_decision_path),
        "decision_sha256": artifact.decision_sha256,
        "source_candidate_reviewed_event_sha256": reviewed_event.event_sha256,
        "promotion_status": "not_requested",
    }
    append_campaign_event(
        campaign_root=root,
        event_type=decision,
        payload=payload,
    )
    events_after = load_campaign_journal(root, manifest=manifest)
    decision_event = events_after[-1]
    capsule = inspect_campaign(root, write_capsule=True)
    return IndependentReviewResult(
        status="recorded",
        decision_path=resolved_decision_path,
        decision=artifact,
        journal_appended=True,
        decision_event=decision_event,
        next_action=capsule.next_action,
    )


def load_independent_review_decision(path: Path) -> IndependentReviewDecision:
    payload = _load_self_hashed_json(path, "decision_sha256", "Independent review decision")
    if payload.get("schema_version") != INDEPENDENT_REVIEW_SCHEMA_VERSION:
        raise IndependentReviewError(
            f"Unsupported independent review schema: {payload.get('schema_version')!r}"
        )
    if payload.get("gate_version") != INDEPENDENT_REVIEW_GATE_VERSION:
        raise IndependentReviewError(
            f"Unsupported independent review gate: {payload.get('gate_version')!r}"
        )
    decision = _required_string(payload.get("decision"), "decision.decision")
    if decision not in INDEPENDENT_DECISIONS:
        raise IndependentReviewError(f"Unsupported independent review decision: {decision!r}")
    restrictions = payload.get("restrictions")
    if not isinstance(restrictions, list) or not all(
        isinstance(item, str) and item for item in restrictions
    ):
        raise IndependentReviewError("decision.restrictions must be a list of strings")
    return IndependentReviewDecision(
        schema_version=INDEPENDENT_REVIEW_SCHEMA_VERSION,
        gate_version=INDEPENDENT_REVIEW_GATE_VERSION,
        campaign_id=_required_string(payload.get("campaign_id"), "decision.campaign_id"),
        manifest_sha256=_required_sha(payload.get("manifest_sha256"), "decision.manifest_sha256"),
        candidate_id=_required_string(payload.get("candidate_id"), "decision.candidate_id"),
        hypothesis_id=_required_string(payload.get("hypothesis_id"), "decision.hypothesis_id"),
        reviewer_id=_required_string(payload.get("reviewer_id"), "decision.reviewer_id"),
        reviewer_role=_required_string(payload.get("reviewer_role"), "decision.reviewer_role"),
        attestation=_required_string(payload.get("attestation"), "decision.attestation"),
        decision=decision,
        promotion_status=_required_string(payload.get("promotion_status"), "decision.promotion_status"),
        frozen_parent=dict(_object(payload.get("frozen_parent"), "decision.frozen_parent")),
        review_path=_required_string(payload.get("review_path"), "decision.review_path"),
        review_sha256=_required_sha(payload.get("review_sha256"), "decision.review_sha256"),
        receipt_path=_required_string(payload.get("receipt_path"), "decision.receipt_path"),
        receipt_sha256=_required_sha(payload.get("receipt_sha256"), "decision.receipt_sha256"),
        handoff_path=_required_string(payload.get("handoff_path"), "decision.handoff_path"),
        handoff_sha256=_required_sha(payload.get("handoff_sha256"), "decision.handoff_sha256"),
        candidate_reviewed_event_sequence=_positive_int(
            payload.get("candidate_reviewed_event_sequence"),
            "decision.candidate_reviewed_event_sequence",
        ),
        candidate_reviewed_event_sha256=_required_sha(
            payload.get("candidate_reviewed_event_sha256"),
            "decision.candidate_reviewed_event_sha256",
        ),
        journal_head_sha256_before_decision=_required_sha(
            payload.get("journal_head_sha256_before_decision"),
            "decision.journal_head_sha256_before_decision",
        ),
        verified_attempts=_positive_int(payload.get("verified_attempts"), "decision.verified_attempts"),
        verified_evidence_files=_positive_int(
            payload.get("verified_evidence_files"), "decision.verified_evidence_files"
        ),
        restrictions=tuple(restrictions),
        decision_sha256=_required_sha(payload.get("decision_sha256"), "decision.decision_sha256"),
    )


def _verify_chain(
    *,
    manifest,
    events: tuple[JournalEvent, ...],
    reviewed_event: JournalEvent,
    review: Mapping[str, Any],
    review_path: Path,
    receipt: ReviewReceipt,
    receipt_path: Path,
    handoff: ReviewHandoffCapsule,
    handoff_path: Path,
) -> int:
    expected_parent = asdict(manifest.frozen_parent)
    if handoff.frozen_parent != expected_parent:
        raise IndependentReviewError("Handoff frozen_parent does not match campaign manifest")
    if handoff.campaign_id != manifest.campaign_id or receipt.campaign_id != manifest.campaign_id:
        raise IndependentReviewError("Receipt or handoff campaign_id does not match manifest")
    if handoff.manifest_sha256 != manifest.manifest_sha256 or receipt.manifest_sha256 != manifest.manifest_sha256:
        raise IndependentReviewError("Receipt or handoff manifest hash does not match campaign manifest")
    if review.get("manifest_sha256") != manifest.manifest_sha256:
        raise IndependentReviewError("Candidate review manifest hash does not match campaign manifest")
    if review.get("campaign_id") != manifest.campaign_id:
        raise IndependentReviewError("Candidate review campaign_id does not match campaign manifest")

    review_sha = _required_sha(review.get("review_sha256"), "review.review_sha256")
    if receipt.review_sha256 != review_sha or handoff.source_review_sha256 != review_sha:
        raise IndependentReviewError("Review SHA-256 binding differs across review, receipt, and handoff")
    if Path(receipt.review_path).resolve() != review_path or Path(handoff.source_review_path).resolve() != review_path:
        raise IndependentReviewError("Review path binding differs across receipt or handoff")
    if receipt.handoff_sha256 != handoff.handoff_sha256:
        raise IndependentReviewError("Receipt handoff SHA-256 does not match handoff capsule")
    if Path(receipt.handoff_path).resolve() != handoff_path:
        raise IndependentReviewError("Receipt handoff path does not match handoff capsule")
    if receipt.candidate_reviewed_event_sha256 != reviewed_event.event_sha256:
        raise IndependentReviewError("Receipt candidate_reviewed event hash does not match journal")
    if receipt.candidate_reviewed_event_sequence != reviewed_event.sequence:
        raise IndependentReviewError("Receipt candidate_reviewed sequence does not match journal")
    if receipt.journal_head_sha256_after_receipt != reviewed_event.event_sha256:
        raise IndependentReviewError("Receipt journal head does not match candidate_reviewed event")
    if handoff.source_journal_head_sha256 != receipt.review_journal_head_sha256:
        raise IndependentReviewError("Handoff source journal head does not match receipt review head")
    if reviewed_event.payload.get("review_sha256") != review_sha:
        raise IndependentReviewError("candidate_reviewed event review hash does not match review")
    if reviewed_event.payload.get("handoff_sha256") != handoff.handoff_sha256:
        raise IndependentReviewError("candidate_reviewed event handoff hash does not match handoff")
    if Path(str(reviewed_event.payload.get("receipt_path"))).resolve() != receipt_path:
        raise IndependentReviewError("candidate_reviewed event receipt path does not match receipt")
    if Path(str(reviewed_event.payload.get("handoff_path"))).resolve() != handoff_path:
        raise IndependentReviewError("candidate_reviewed event handoff path does not match handoff")
    if handoff.decision != "keep" or receipt.decision != "keep" or review.get("decision") != "keep":
        raise IndependentReviewError("Independent review requires a keep review chain")
    if handoff.operational_meaning != "keep-for-independent-review":
        raise IndependentReviewError("Handoff operational meaning is not keep-for-independent-review")
    if handoff.promotion_status != "not_requested" or receipt.promotion_status != "not_requested":
        raise IndependentReviewError("Review chain unexpectedly authorizes promotion")
    if handoff.required_role != INDEPENDENT_REVIEW_ROLE:
        raise IndependentReviewError("Handoff does not require independent_reviewer role")
    if handoff.next_action != "await_independent_review" or receipt.next_action != "await_independent_review":
        raise IndependentReviewError("Review chain is not waiting for independent review")
    for required in ("candidate_kept", "candidate_rejected", "candidate_quarantined"):
        if required not in handoff.permitted_follow_up_events:
            raise IndependentReviewError(f"Handoff does not permit {required}")
    for restriction in (
        "promotion_not_authorized",
        "central_planning_lite_mutation_not_authorized",
        "verify_review_and_handoff_sha256_before_action",
        "preserve_append_only_campaign_journal",
    ):
        if restriction not in handoff.restrictions:
            raise IndependentReviewError(f"Handoff omitted required restriction {restriction!r}")

    attempts = handoff.attempts
    if len(attempts) != handoff.independent_attempts or handoff.independent_attempts < 3:
        raise IndependentReviewError("Handoff does not contain three independent attempts")
    total_files = 0
    event_by_hash = {event.event_sha256: event for event in events}
    for attempt in attempts:
        event_sha = _required_sha(attempt.get("event_sha256"), "handoff.attempt.event_sha256")
        event = event_by_hash.get(event_sha)
        if event is None or event.event_type != "attempt_completed":
            raise IndependentReviewError("Handoff attempt event is missing from campaign journal")
        if event.payload.get("candidate_id") != handoff.candidate_id:
            raise IndependentReviewError("Handoff attempt candidate does not match reviewed candidate")
        if event.payload.get("attempt_id") != attempt.get("attempt_id"):
            raise IndependentReviewError("Handoff attempt_id does not match campaign journal")
        suite_root = Path(_required_string(attempt.get("suite_root"), "handoff.attempt.suite_root")).resolve()
        evidence = _object(attempt.get("evidence_sha256"), "handoff.attempt.evidence_sha256")
        if set(evidence) != REQUIRED_EVIDENCE_FILES:
            raise IndependentReviewError("Handoff attempt does not seal the six required evidence files")
        for name in sorted(REQUIRED_EVIDENCE_FILES):
            expected = _required_sha(evidence.get(name), f"handoff.attempt.evidence_sha256.{name}")
            path = (suite_root / name).resolve()
            try:
                path.relative_to(suite_root)
            except ValueError as exc:  # pragma: no cover - defensive
                raise IndependentReviewError("Evidence path escapes suite root") from exc
            if not path.is_file():
                raise IndependentReviewError(f"Independent review evidence file is missing: {path}")
            observed = _sha256_file(path)
            if observed != expected:
                raise IndependentReviewError(
                    f"Independent review evidence SHA-256 mismatch for {path}: expected {expected}, observed {observed}"
                )
            total_files += 1
    return total_files


def _build_decision(
    *,
    manifest,
    reviewed_event: JournalEvent,
    review_path: Path,
    review: Mapping[str, Any],
    receipt_path: Path,
    receipt: ReviewReceipt,
    handoff_path: Path,
    handoff: ReviewHandoffCapsule,
    reviewer_id: str,
    attestation: str,
    decision: str,
    verified_evidence_files: int,
) -> IndependentReviewDecision:
    unsigned = {
        "schema_version": INDEPENDENT_REVIEW_SCHEMA_VERSION,
        "gate_version": INDEPENDENT_REVIEW_GATE_VERSION,
        "campaign_id": manifest.campaign_id,
        "manifest_sha256": manifest.manifest_sha256,
        "candidate_id": handoff.candidate_id,
        "hypothesis_id": handoff.hypothesis_id,
        "reviewer_id": reviewer_id,
        "reviewer_role": INDEPENDENT_REVIEW_ROLE,
        "attestation": attestation,
        "decision": decision,
        "promotion_status": "not_requested",
        "frozen_parent": asdict(manifest.frozen_parent),
        "review_path": str(review_path),
        "review_sha256": _required_sha(review.get("review_sha256"), "review.review_sha256"),
        "receipt_path": str(receipt_path),
        "receipt_sha256": receipt.receipt_sha256,
        "handoff_path": str(handoff_path),
        "handoff_sha256": handoff.handoff_sha256,
        "candidate_reviewed_event_sequence": reviewed_event.sequence,
        "candidate_reviewed_event_sha256": reviewed_event.event_sha256,
        "journal_head_sha256_before_decision": reviewed_event.event_sha256,
        "verified_attempts": handoff.independent_attempts,
        "verified_evidence_files": verified_evidence_files,
        "restrictions": (
            "promotion_not_authorized",
            "central_planning_lite_mutation_not_authorized",
            "release_gate_not_executed",
            "preserve_append_only_campaign_journal",
        ),
    }
    payload = dict(unsigned)
    payload["restrictions"] = list(unsigned["restrictions"])
    digest = _sha256_json(payload)
    return IndependentReviewDecision(**{**unsigned, "decision_sha256": digest})


def _replay_existing_decision(
    root: Path,
    *,
    manifest,
    events: tuple[JournalEvent, ...],
    existing_event: JournalEvent,
    decision: str,
    reviewer_id: str,
    attestation: str,
    decision_path: Path | None,
) -> IndependentReviewResult:
    if existing_event.event_type != decision:
        raise IndependentReviewError(
            f"Candidate already has independent decision {existing_event.event_type!r}, not {decision!r}"
        )
    payload = existing_event.payload
    if payload.get("reviewer_id") != reviewer_id or payload.get("reviewer_role") != INDEPENDENT_REVIEW_ROLE:
        raise IndependentReviewError("Existing independent decision reviewer binding differs")
    artifact_path = Path(
        _required_string(payload.get("decision_artifact_path"), "decision_event.decision_artifact_path")
    ).resolve()
    if decision_path is not None and decision_path.resolve() != artifact_path:
        raise IndependentReviewError("Requested decision output differs from existing decision artifact")
    artifact = load_independent_review_decision(artifact_path)
    if artifact.attestation != attestation:
        raise IndependentReviewError("Existing independent decision attestation differs")
    if payload.get("decision_sha256") != artifact.decision_sha256:
        raise IndependentReviewError("Existing independent decision artifact hash differs from journal")
    if artifact.manifest_sha256 != manifest.manifest_sha256:
        raise IndependentReviewError("Existing independent decision manifest hash differs")
    capsule = inspect_campaign(root, write_capsule=True)
    return IndependentReviewResult(
        status="already-recorded",
        decision_path=artifact_path,
        decision=artifact,
        journal_appended=False,
        decision_event=existing_event,
        next_action=capsule.next_action,
    )


def _latest_candidate_reviewed(events: tuple[JournalEvent, ...]) -> JournalEvent | None:
    for event in reversed(events):
        if event.event_type == "candidate_reviewed":
            return event
    return None


def _latest_independent_decision_event(events: tuple[JournalEvent, ...]) -> JournalEvent | None:
    for event in reversed(events):
        if event.event_type in INDEPENDENT_DECISIONS and event.payload.get("reason") == "independent_review_decision":
            return event
    return None


def _decision_event_after(
    events: tuple[JournalEvent, ...], reviewed_event: JournalEvent
) -> JournalEvent | None:
    for event in events:
        if event.sequence <= reviewed_event.sequence:
            continue
        if event.event_type in INDEPENDENT_DECISIONS and event.payload.get(
            "source_candidate_reviewed_event_sha256"
        ) == reviewed_event.event_sha256:
            return event
    return None


def _write_self_hashed_artifact(path: Path, payload: Mapping[str, Any]) -> None:
    _verify_self_hash(payload, "decision_sha256", "Independent review decision")
    target = path.resolve()
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if target.exists():
        if target.read_text(encoding="utf-8") == text:
            return
        raise IndependentReviewError(
            f"Independent review decision already exists with different content: {target}"
        )
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.tmp")
    temp.write_text(text, encoding="utf-8", newline="")
    temp.replace(target)


def _load_self_hashed_json(path: Path, hash_field: str, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise IndependentReviewError(f"{label} was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise IndependentReviewError(f"{label} is invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise IndependentReviewError(f"{label} root must be an object: {path}")
    _verify_self_hash(payload, hash_field, label)
    return payload


def _verify_self_hash(payload: Mapping[str, Any], hash_field: str, label: str) -> None:
    supplied = _required_sha(payload.get(hash_field), f"{label}.{hash_field}")
    unsigned = dict(payload)
    unsigned.pop(hash_field, None)
    calculated = _sha256_json(unsigned)
    if supplied != calculated:
        raise IndependentReviewError(
            f"{label} SHA-256 mismatch: expected self-hash {supplied}, calculated {calculated}"
        )


def _sha256_json(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise IndependentReviewError(f"{label} must be a non-empty string")
    return value.strip()


def _required_sha(value: Any, label: str) -> str:
    text = _required_string(value, label).lower()
    if not SHA256_RE.fullmatch(text):
        raise IndependentReviewError(f"{label} must be a SHA-256 digest")
    return text


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise IndependentReviewError(f"{label} must be a positive integer")
    return value


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise IndependentReviewError(f"{label} must be an object")
    return dict(value)
