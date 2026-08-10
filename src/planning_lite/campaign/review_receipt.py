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
    ResumeCapsule,
    append_campaign_event,
    inspect_campaign,
    load_campaign_journal,
    load_campaign_manifest,
)
from .candidate_review import (
    CANDIDATE_REVIEW_GATE_VERSION,
    CANDIDATE_REVIEW_SCHEMA_VERSION,
)


REVIEW_RECEIPT_SCHEMA_VERSION = 1
REVIEW_RECEIPT_VERSION = "review-receipt-v1"
HANDOFF_CAPSULE_SCHEMA_VERSION = 1
HANDOFF_CAPSULE_VERSION = "independent-review-handoff-v1"
REVIEW_DECISIONS = frozenset({"keep", "reject", "continue"})
DECISION_OPERATIONAL_MEANING = {
    "keep": "keep-for-independent-review",
    "reject": "reject-candidate",
    "continue": "collect-or-reconcile-evidence",
}
DECISION_NEXT_ACTION = {
    "keep": "await_independent_review",
    "reject": "record_candidate_rejected",
    "continue": "start_next_independent_attempt",
}
DECISION_PERMITTED_FOLLOW_UP_EVENTS = {
    "keep": (
        "candidate_kept",
        "candidate_rejected",
        "candidate_quarantined",
        "campaign_stopped",
    ),
    "reject": (
        "candidate_rejected",
        "candidate_quarantined",
        "campaign_stopped",
    ),
    "continue": (
        "attempt_started",
        "candidate_quarantined",
        "campaign_stopped",
    ),
}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")


class ReviewReceiptError(CampaignError):
    """Raised when review receipt or handoff state cannot be recorded safely."""


@dataclass(frozen=True)
class ReviewHandoffCapsule:
    schema_version: int
    capsule_version: str
    campaign_id: str
    manifest_sha256: str
    candidate_id: str
    hypothesis_id: str
    frozen_parent: dict[str, str | None]
    source_review_path: str
    source_review_sha256: str
    source_journal_head_sha256: str
    decision: str
    operational_meaning: str
    promotion_status: str
    required_attempts: int
    observed_attempts: int
    independent_attempts: int
    reason_codes: tuple[str, ...]
    attempts: tuple[dict[str, Any], ...]
    next_action: str
    required_role: str
    permitted_follow_up_events: tuple[str, ...]
    restrictions: tuple[str, ...]
    handoff_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("handoff_sha256", None)
        payload["reason_codes"] = list(self.reason_codes)
        payload["attempts"] = [dict(item) for item in self.attempts]
        payload["permitted_follow_up_events"] = list(self.permitted_follow_up_events)
        payload["restrictions"] = list(self.restrictions)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned_dict(), "handoff_sha256": self.handoff_sha256}


@dataclass(frozen=True)
class ReviewReceipt:
    schema_version: int
    receipt_version: str
    campaign_id: str
    manifest_sha256: str
    candidate_id: str
    hypothesis_id: str
    decision: str
    operational_meaning: str
    promotion_status: str
    review_path: str
    review_sha256: str
    review_journal_head_sha256: str
    handoff_path: str
    handoff_sha256: str
    candidate_reviewed_event_sequence: int
    candidate_reviewed_event_sha256: str
    journal_head_sha256_after_receipt: str
    next_action: str
    receipt_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("receipt_sha256", None)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned_dict(), "receipt_sha256": self.receipt_sha256}


@dataclass(frozen=True)
class ReviewReceiptResult:
    status: str
    receipt_path: Path
    handoff_path: Path
    receipt: ReviewReceipt
    handoff: ReviewHandoffCapsule
    resume_capsule: ResumeCapsule
    journal_appended: bool


def record_candidate_review_receipt(
    campaign_root: Path,
    *,
    review_path: Path | None = None,
    receipt_path: Path | None = None,
    handoff_path: Path | None = None,
) -> ReviewReceiptResult:
    """Verify a deterministic candidate review and record one append-only receipt.

    The command never promotes a candidate. A ``keep`` review becomes only an
    ``await_independent_review`` handoff. Repeating the operation with the same
    verified artifacts is idempotent and never appends a second journal event.
    """

    root = campaign_root.resolve()
    manifest = load_campaign_manifest(root)
    events = load_campaign_journal(root, manifest=manifest)
    resolved_review_path = (review_path or root / "candidate-review.json").resolve()
    review = _load_and_verify_review(resolved_review_path)
    resolved_receipt_path = (
        receipt_path
        or root / "review-receipts" / f"{review['review_sha256']}.json"
    ).resolve()
    resolved_handoff_path = (
        handoff_path
        or root / "review-handoffs" / f"{review['review_sha256']}.json"
    ).resolve()
    _validate_review_binding(review, manifest=manifest, events=events)

    handoff = _build_handoff(
        review=review,
        review_path=resolved_review_path,
        manifest=manifest,
    )

    existing_event = _matching_receipt_event(events, review)
    journal_appended = False
    if existing_event is None:
        _write_self_hashed_artifact(
            resolved_handoff_path,
            handoff.to_dict(),
            hash_field="handoff_sha256",
            label="Review handoff capsule",
        )
        if events[-1].event_sha256 != review["journal_head_sha256"]:
            raise ReviewReceiptError(
                "Candidate review is stale: its journal head does not match the current campaign head"
            )
        if events[-1].event_type != "attempt_completed":
            raise ReviewReceiptError(
                "Candidate review receipt requires attempt_completed as the current journal event"
            )
        event_payload = {
            "candidate_id": review["candidate_id"],
            "hypothesis_id": review["hypothesis_id"],
            "decision": review["decision"],
            "operational_meaning": review["operational_meaning"],
            "promotion_status": "not_requested",
            "review_path": str(resolved_review_path),
            "review_sha256": review["review_sha256"],
            "review_journal_head_sha256": review["journal_head_sha256"],
            "handoff_path": str(resolved_handoff_path),
            "handoff_sha256": handoff.handoff_sha256,
            "receipt_path": str(resolved_receipt_path),
            "next_action": DECISION_NEXT_ACTION[review["decision"]],
        }
        append_campaign_event(
            campaign_root=root,
            event_type="candidate_reviewed",
            payload=event_payload,
        )
        events = load_campaign_journal(root, manifest=manifest)
        existing_event = events[-1]
        journal_appended = True
    else:
        _validate_existing_receipt_event(
            existing_event,
            review=review,
            review_path=resolved_review_path,
            handoff=handoff,
            handoff_path=resolved_handoff_path,
            receipt_path=resolved_receipt_path,
        )
        _write_self_hashed_artifact(
            resolved_handoff_path,
            handoff.to_dict(),
            hash_field="handoff_sha256",
            label="Review handoff capsule",
        )

    if existing_event is None:  # pragma: no cover - defensive boundary
        raise ReviewReceiptError("Candidate review receipt event was not found after append")

    capsule = inspect_campaign(root, write_capsule=True)
    receipt = _build_receipt(
        review=review,
        review_path=resolved_review_path,
        handoff=handoff,
        handoff_path=resolved_handoff_path,
        event=existing_event,
        capsule=capsule,
    )
    _write_self_hashed_artifact(
        resolved_receipt_path,
        receipt.to_dict(),
        hash_field="receipt_sha256",
        label="Review receipt",
    )
    return ReviewReceiptResult(
        status="recorded" if journal_appended else "already-recorded",
        receipt_path=resolved_receipt_path,
        handoff_path=resolved_handoff_path,
        receipt=receipt,
        handoff=handoff,
        resume_capsule=capsule,
        journal_appended=journal_appended,
    )


def load_review_receipt(path: Path) -> ReviewReceipt:
    payload = _read_json_object(path, "review receipt")
    _verify_self_hash(payload, "receipt_sha256", "Review receipt")
    if payload.get("schema_version") != REVIEW_RECEIPT_SCHEMA_VERSION:
        raise ReviewReceiptError(
            f"Unsupported review receipt schema: {payload.get('schema_version')!r}"
        )
    if payload.get("receipt_version") != REVIEW_RECEIPT_VERSION:
        raise ReviewReceiptError(
            f"Unsupported review receipt version: {payload.get('receipt_version')!r}"
        )
    return ReviewReceipt(
        schema_version=REVIEW_RECEIPT_SCHEMA_VERSION,
        receipt_version=REVIEW_RECEIPT_VERSION,
        campaign_id=_required_string(payload.get("campaign_id"), "receipt.campaign_id"),
        manifest_sha256=_required_sha(payload.get("manifest_sha256"), "receipt.manifest_sha256"),
        candidate_id=_required_string(payload.get("candidate_id"), "receipt.candidate_id"),
        hypothesis_id=_required_string(payload.get("hypothesis_id"), "receipt.hypothesis_id"),
        decision=_required_decision(payload.get("decision")),
        operational_meaning=_required_string(payload.get("operational_meaning"), "receipt.operational_meaning"),
        promotion_status=_required_string(payload.get("promotion_status"), "receipt.promotion_status"),
        review_path=_required_string(payload.get("review_path"), "receipt.review_path"),
        review_sha256=_required_sha(payload.get("review_sha256"), "receipt.review_sha256"),
        review_journal_head_sha256=_required_sha(
            payload.get("review_journal_head_sha256"),
            "receipt.review_journal_head_sha256",
        ),
        handoff_path=_required_string(payload.get("handoff_path"), "receipt.handoff_path"),
        handoff_sha256=_required_sha(payload.get("handoff_sha256"), "receipt.handoff_sha256"),
        candidate_reviewed_event_sequence=_positive_int(
            payload.get("candidate_reviewed_event_sequence"),
            "receipt.candidate_reviewed_event_sequence",
        ),
        candidate_reviewed_event_sha256=_required_sha(
            payload.get("candidate_reviewed_event_sha256"),
            "receipt.candidate_reviewed_event_sha256",
        ),
        journal_head_sha256_after_receipt=_required_sha(
            payload.get("journal_head_sha256_after_receipt"),
            "receipt.journal_head_sha256_after_receipt",
        ),
        next_action=_required_string(payload.get("next_action"), "receipt.next_action"),
        receipt_sha256=_required_sha(payload.get("receipt_sha256"), "receipt.receipt_sha256"),
    )


def load_review_handoff(path: Path) -> ReviewHandoffCapsule:
    payload = _read_json_object(path, "review handoff capsule")
    _verify_self_hash(payload, "handoff_sha256", "Review handoff capsule")
    if payload.get("schema_version") != HANDOFF_CAPSULE_SCHEMA_VERSION:
        raise ReviewReceiptError(
            f"Unsupported handoff capsule schema: {payload.get('schema_version')!r}"
        )
    if payload.get("capsule_version") != HANDOFF_CAPSULE_VERSION:
        raise ReviewReceiptError(
            f"Unsupported handoff capsule version: {payload.get('capsule_version')!r}"
        )
    decision = _required_decision(payload.get("decision"))
    return ReviewHandoffCapsule(
        schema_version=HANDOFF_CAPSULE_SCHEMA_VERSION,
        capsule_version=HANDOFF_CAPSULE_VERSION,
        campaign_id=_required_string(payload.get("campaign_id"), "handoff.campaign_id"),
        manifest_sha256=_required_sha(payload.get("manifest_sha256"), "handoff.manifest_sha256"),
        candidate_id=_required_string(payload.get("candidate_id"), "handoff.candidate_id"),
        hypothesis_id=_required_string(payload.get("hypothesis_id"), "handoff.hypothesis_id"),
        frozen_parent=dict(_object(payload.get("frozen_parent"), "handoff.frozen_parent")),
        source_review_path=_required_string(payload.get("source_review_path"), "handoff.source_review_path"),
        source_review_sha256=_required_sha(payload.get("source_review_sha256"), "handoff.source_review_sha256"),
        source_journal_head_sha256=_required_sha(
            payload.get("source_journal_head_sha256"),
            "handoff.source_journal_head_sha256",
        ),
        decision=decision,
        operational_meaning=_required_string(payload.get("operational_meaning"), "handoff.operational_meaning"),
        promotion_status=_required_string(payload.get("promotion_status"), "handoff.promotion_status"),
        required_attempts=_nonnegative_int(payload.get("required_attempts"), "handoff.required_attempts"),
        observed_attempts=_nonnegative_int(payload.get("observed_attempts"), "handoff.observed_attempts"),
        independent_attempts=_nonnegative_int(payload.get("independent_attempts"), "handoff.independent_attempts"),
        reason_codes=tuple(_string_list(payload.get("reason_codes"), "handoff.reason_codes")),
        attempts=tuple(dict(item) for item in _object_list(payload.get("attempts"), "handoff.attempts")),
        next_action=_required_string(payload.get("next_action"), "handoff.next_action"),
        required_role=_required_string(payload.get("required_role"), "handoff.required_role"),
        permitted_follow_up_events=tuple(
            _string_list(payload.get("permitted_follow_up_events"), "handoff.permitted_follow_up_events")
        ),
        restrictions=tuple(_string_list(payload.get("restrictions"), "handoff.restrictions")),
        handoff_sha256=_required_sha(payload.get("handoff_sha256"), "handoff.handoff_sha256"),
    )


def _load_and_verify_review(path: Path) -> dict[str, Any]:
    payload = _read_json_object(path, "candidate review")
    _verify_self_hash(payload, "review_sha256", "Candidate review")
    if payload.get("schema_version") != CANDIDATE_REVIEW_SCHEMA_VERSION:
        raise ReviewReceiptError(
            f"Unsupported candidate review schema: {payload.get('schema_version')!r}"
        )
    if payload.get("gate_version") != CANDIDATE_REVIEW_GATE_VERSION:
        raise ReviewReceiptError(
            f"Unsupported candidate review gate: {payload.get('gate_version')!r}"
        )
    decision = _required_decision(payload.get("decision"))
    operational_meaning = _required_string(
        payload.get("operational_meaning"), "review.operational_meaning"
    )
    if operational_meaning != DECISION_OPERATIONAL_MEANING[decision]:
        raise ReviewReceiptError(
            "Candidate review operational_meaning does not match its decision"
        )
    if payload.get("promotion_status") != "not_requested":
        raise ReviewReceiptError(
            "Candidate review must preserve promotion_status='not_requested'"
        )
    normalized = dict(payload)
    normalized["campaign_id"] = _required_string(payload.get("campaign_id"), "review.campaign_id")
    normalized["manifest_sha256"] = _required_sha(payload.get("manifest_sha256"), "review.manifest_sha256")
    normalized["journal_head_sha256"] = _required_sha(
        payload.get("journal_head_sha256"), "review.journal_head_sha256"
    )
    normalized["candidate_id"] = _required_string(payload.get("candidate_id"), "review.candidate_id")
    normalized["hypothesis_id"] = _required_string(payload.get("hypothesis_id"), "review.hypothesis_id")
    normalized["decision"] = decision
    normalized["operational_meaning"] = operational_meaning
    normalized["required_attempts"] = _nonnegative_int(payload.get("required_attempts"), "review.required_attempts")
    normalized["observed_attempts"] = _nonnegative_int(payload.get("observed_attempts"), "review.observed_attempts")
    normalized["independent_attempts"] = _nonnegative_int(
        payload.get("independent_attempts"), "review.independent_attempts"
    )
    normalized["reason_codes"] = _string_list(payload.get("reason_codes"), "review.reason_codes")
    normalized["attempts"] = _object_list(payload.get("attempts"), "review.attempts")
    normalized["review_sha256"] = _required_sha(payload.get("review_sha256"), "review.review_sha256")
    return normalized


def _validate_review_binding(review: Mapping[str, Any], *, manifest, events: tuple[JournalEvent, ...]) -> None:
    if review["campaign_id"] != manifest.campaign_id:
        raise ReviewReceiptError("Candidate review campaign_id does not match campaign manifest")
    if review["manifest_sha256"] != manifest.manifest_sha256:
        raise ReviewReceiptError("Candidate review manifest hash does not match campaign manifest")
    candidate_id = review["candidate_id"]
    hypothesis_id = review["hypothesis_id"]
    registrations = [
        event
        for event in events
        if event.event_type == "candidate_registered"
        and event.payload.get("candidate_id") == candidate_id
    ]
    if len(registrations) != 1:
        raise ReviewReceiptError(
            f"Candidate review references an unregistered or ambiguous candidate: {candidate_id!r}"
        )
    if registrations[0].payload.get("hypothesis_id") != hypothesis_id:
        raise ReviewReceiptError("Candidate review hypothesis_id does not match candidate registration")
    if not any(event.event_sha256 == review["journal_head_sha256"] for event in events):
        raise ReviewReceiptError("Candidate review journal head is not present in the campaign journal")


def _build_handoff(*, review: Mapping[str, Any], review_path: Path, manifest) -> ReviewHandoffCapsule:
    decision = review["decision"]
    unsigned = {
        "schema_version": HANDOFF_CAPSULE_SCHEMA_VERSION,
        "capsule_version": HANDOFF_CAPSULE_VERSION,
        "campaign_id": manifest.campaign_id,
        "manifest_sha256": manifest.manifest_sha256,
        "candidate_id": review["candidate_id"],
        "hypothesis_id": review["hypothesis_id"],
        "frozen_parent": asdict(manifest.frozen_parent),
        "source_review_path": str(review_path),
        "source_review_sha256": review["review_sha256"],
        "source_journal_head_sha256": review["journal_head_sha256"],
        "decision": decision,
        "operational_meaning": review["operational_meaning"],
        "promotion_status": "not_requested",
        "required_attempts": review["required_attempts"],
        "observed_attempts": review["observed_attempts"],
        "independent_attempts": review["independent_attempts"],
        "reason_codes": list(review["reason_codes"]),
        "attempts": [dict(item) for item in review["attempts"]],
        "next_action": DECISION_NEXT_ACTION[decision],
        "required_role": (
            "independent_reviewer" if decision == "keep" else "campaign_operator"
        ),
        "permitted_follow_up_events": list(DECISION_PERMITTED_FOLLOW_UP_EVENTS[decision]),
        "restrictions": [
            "promotion_not_authorized",
            "central_planning_lite_mutation_not_authorized",
            "verify_review_and_handoff_sha256_before_action",
            "preserve_append_only_campaign_journal",
        ],
    }
    return ReviewHandoffCapsule(
        **{
            **unsigned,
            "reason_codes": tuple(unsigned["reason_codes"]),
            "attempts": tuple(unsigned["attempts"]),
            "permitted_follow_up_events": tuple(unsigned["permitted_follow_up_events"]),
            "restrictions": tuple(unsigned["restrictions"]),
            "handoff_sha256": _sha256_json(unsigned),
        }
    )


def _build_receipt(
    *,
    review: Mapping[str, Any],
    review_path: Path,
    handoff: ReviewHandoffCapsule,
    handoff_path: Path,
    event: JournalEvent,
    capsule: ResumeCapsule,
) -> ReviewReceipt:
    unsigned = {
        "schema_version": REVIEW_RECEIPT_SCHEMA_VERSION,
        "receipt_version": REVIEW_RECEIPT_VERSION,
        "campaign_id": review["campaign_id"],
        "manifest_sha256": review["manifest_sha256"],
        "candidate_id": review["candidate_id"],
        "hypothesis_id": review["hypothesis_id"],
        "decision": review["decision"],
        "operational_meaning": review["operational_meaning"],
        "promotion_status": "not_requested",
        "review_path": str(review_path),
        "review_sha256": review["review_sha256"],
        "review_journal_head_sha256": review["journal_head_sha256"],
        "handoff_path": str(handoff_path),
        "handoff_sha256": handoff.handoff_sha256,
        "candidate_reviewed_event_sequence": event.sequence,
        "candidate_reviewed_event_sha256": event.event_sha256,
        "journal_head_sha256_after_receipt": event.event_sha256,
        "next_action": _required_string(event.payload.get("next_action"), "candidate_reviewed.next_action"),
    }
    return ReviewReceipt(**{**unsigned, "receipt_sha256": _sha256_json(unsigned)})


def _matching_receipt_event(
    events: tuple[JournalEvent, ...], review: Mapping[str, Any]
) -> JournalEvent | None:
    matching = [
        event
        for event in events
        if event.event_type == "candidate_reviewed"
        and event.payload.get("candidate_id") == review["candidate_id"]
        and event.payload.get("review_sha256") == review["review_sha256"]
    ]
    if not matching:
        return None
    if len(matching) == 1:
        return matching[0]
    raise ReviewReceiptError(
        "Candidate has duplicate candidate_reviewed events for one review artifact"
    )


def _validate_existing_receipt_event(
    event: JournalEvent,
    *,
    review: Mapping[str, Any],
    review_path: Path,
    handoff: ReviewHandoffCapsule,
    handoff_path: Path,
    receipt_path: Path,
) -> None:
    expected = {
        "candidate_id": review["candidate_id"],
        "hypothesis_id": review["hypothesis_id"],
        "decision": review["decision"],
        "operational_meaning": review["operational_meaning"],
        "promotion_status": "not_requested",
        "review_path": str(review_path),
        "review_sha256": review["review_sha256"],
        "review_journal_head_sha256": review["journal_head_sha256"],
        "handoff_path": str(handoff_path),
        "handoff_sha256": handoff.handoff_sha256,
        "receipt_path": str(receipt_path),
        "next_action": DECISION_NEXT_ACTION[review["decision"]],
    }
    if event.payload != expected:
        raise ReviewReceiptError(
            "Existing candidate_reviewed event does not match the verified review receipt binding"
        )


def _write_self_hashed_artifact(
    path: Path,
    payload: Mapping[str, Any],
    *,
    hash_field: str,
    label: str,
) -> None:
    target = path.resolve()
    _verify_self_hash(payload, hash_field, label)
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if target.exists():
        existing = target.read_text(encoding="utf-8")
        if existing == text:
            return
        raise ReviewReceiptError(f"{label} already exists with different content: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = target.with_name(f".{target.name}.tmp")
    temporary.write_text(text, encoding="utf-8", newline="")
    temporary.replace(target)


def _verify_self_hash(payload: Mapping[str, Any], hash_field: str, label: str) -> None:
    supplied = _required_sha(payload.get(hash_field), f"{label}.{hash_field}")
    unsigned = dict(payload)
    unsigned.pop(hash_field, None)
    calculated = _sha256_json(unsigned)
    if supplied != calculated:
        raise ReviewReceiptError(
            f"{label} SHA-256 mismatch: expected self-hash {supplied}, calculated {calculated}"
        )


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReviewReceiptError(f"{label.capitalize()} was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReviewReceiptError(f"{label.capitalize()} is invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ReviewReceiptError(f"{label.capitalize()} root must be an object: {path}")
    return payload


def _required_decision(value: Any) -> str:
    decision = _required_string(value, "decision")
    if decision not in REVIEW_DECISIONS:
        raise ReviewReceiptError(f"Unsupported review decision: {decision!r}")
    return decision


def _required_sha(value: Any, label: str) -> str:
    text = _required_string(value, label).lower()
    if not SHA256_RE.fullmatch(text):
        raise ReviewReceiptError(f"{label} must be a SHA-256 digest")
    return text


def _required_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReviewReceiptError(f"{label} must be a non-empty string")
    return value.strip()


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise ReviewReceiptError(f"{label} must be a positive integer")
    return value


def _nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ReviewReceiptError(f"{label} must be a non-negative integer")
    return value


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ReviewReceiptError(f"{label} must be an object")
    return dict(value)


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item.strip() for item in value
    ):
        raise ReviewReceiptError(f"{label} must be an array of non-empty strings")
    return [item.strip() for item in value]


def _object_list(value: Any, label: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ReviewReceiptError(f"{label} must be an array of objects")
    return [dict(item) for item in value]


def _sha256_json(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()
