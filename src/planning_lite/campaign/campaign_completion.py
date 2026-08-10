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
from .independent_review import (
    IndependentReviewDecision,
    load_independent_review_decision,
)
from .review_receipt import load_review_handoff, load_review_receipt


COMPLETION_SCHEMA_VERSION = 1
COMPLETION_SEAL_VERSION = "campaign-completion-seal-v1"
RELEASE_HANDOFF_VERSION = "release-handoff-v1"
RELEASE_ROLE = "release_reviewer"
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


class CampaignCompletionError(CampaignError):
    """Raised when an accepted campaign cannot be sealed safely for release handoff."""


@dataclass(frozen=True)
class ReleaseHandoffCapsule:
    schema_version: int
    capsule_version: str
    campaign_id: str
    manifest_sha256: str
    candidate_id: str
    hypothesis_id: str
    frozen_parent: dict[str, str | None]
    independent_decision_path: str
    independent_decision_sha256: str
    independent_decision_event_sequence: int
    independent_decision_event_sha256: str
    reviewer_id: str
    accepted_candidate: bool
    verified_attempts: int
    verified_evidence_files: int
    evidence_bundle_sha256: str
    completion_reason: str
    release_status: str
    central_planning_lite_mutated: bool
    next_action: str
    required_role: str
    permitted_follow_up_actions: tuple[str, ...]
    restrictions: tuple[str, ...]
    release_handoff_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("release_handoff_sha256", None)
        payload["permitted_follow_up_actions"] = list(self.permitted_follow_up_actions)
        payload["restrictions"] = list(self.restrictions)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.unsigned_dict(),
            "release_handoff_sha256": self.release_handoff_sha256,
        }


@dataclass(frozen=True)
class CampaignCompletionSeal:
    schema_version: int
    seal_version: str
    campaign_id: str
    manifest_sha256: str
    candidate_id: str
    hypothesis_id: str
    frozen_parent: dict[str, str | None]
    independent_decision_path: str
    independent_decision_sha256: str
    independent_decision_event_sequence: int
    independent_decision_event_sha256: str
    journal_head_sha256_before_completion: str
    completion_reason: str
    accepted_candidate: bool
    expected_terminal_event: str
    attempts_started: int
    attempts_completed: int
    total_tokens: int
    wall_clock_seconds: float
    remaining_budget: dict[str, int | float | None]
    verified_attempts: int
    verified_evidence_files: int
    evidence_bundle_sha256: str
    release_handoff_path: str
    release_handoff_sha256: str
    release_status: str
    central_planning_lite_mutated: bool
    restrictions: tuple[str, ...]
    completion_seal_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("completion_seal_sha256", None)
        payload["restrictions"] = list(self.restrictions)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.unsigned_dict(),
            "completion_seal_sha256": self.completion_seal_sha256,
        }


@dataclass(frozen=True)
class CampaignCompletionResult:
    status: str
    seal_path: Path
    seal: CampaignCompletionSeal
    release_handoff_path: Path
    release_handoff: ReleaseHandoffCapsule
    journal_appended: bool
    completion_event: JournalEvent
    resume_capsule: Any


def record_campaign_completion(
    campaign_root: Path,
    *,
    seal_path: Path | None = None,
    release_handoff_path: Path | None = None,
) -> CampaignCompletionResult:
    """Seal one accepted campaign and append its terminal campaign_completed event.

    This operation closes the experiment only. It never promotes a release and never
    mutates central Planning Lite. The release handoff is an immutable capsule for a
    later, separate release gate.
    """

    root = campaign_root.resolve()
    manifest = load_campaign_manifest(root)
    events = load_campaign_journal(root, manifest=manifest)
    last = events[-1]

    if last.event_type == "campaign_completed":
        return _replay_existing_completion(
            root,
            manifest=manifest,
            events=events,
            completion_event=last,
            seal_path=seal_path,
            release_handoff_path=release_handoff_path,
        )

    if last.event_type != "candidate_kept":
        raise CampaignCompletionError(
            "Campaign completion requires candidate_kept to be the current journal head"
        )
    if last.payload.get("reason") != "independent_review_decision":
        raise CampaignCompletionError(
            "campaign completion requires candidate_kept from the Independent Review Decision Gate"
        )
    if last.payload.get("promotion_status") != "not_requested":
        raise CampaignCompletionError("Accepted candidate unexpectedly authorizes promotion")

    decision_path = Path(
        _required_string(
            last.payload.get("decision_artifact_path"),
            "candidate_kept.decision_artifact_path",
        )
    ).resolve()
    try:
        decision = load_independent_review_decision(decision_path)
        verified_files, evidence_bundle_sha256 = _verify_independent_decision_chain(
            manifest=manifest,
            events=events,
            decision_event=last,
            decision_path=decision_path,
            decision=decision,
        )
    except CampaignCompletionError:
        raise
    except CampaignError as exc:
        raise CampaignCompletionError(
            f"Accepted candidate decision chain failed completion verification: {exc}"
        ) from exc

    capsule_before = inspect_campaign(root, write_capsule=False)
    resolved_release_handoff_path = (
        release_handoff_path
        or root / "release-handoffs" / f"{last.event_sha256}.json"
    ).resolve()
    resolved_seal_path = (
        seal_path
        or root / "completion-seals" / f"{last.event_sha256}.json"
    ).resolve()

    release_handoff = _build_release_handoff(
        manifest=manifest,
        decision_event=last,
        decision_path=decision_path,
        decision=decision,
        verified_evidence_files=verified_files,
        evidence_bundle_sha256=evidence_bundle_sha256,
    )
    _write_self_hashed_artifact(
        resolved_release_handoff_path,
        release_handoff.to_dict(),
        hash_field="release_handoff_sha256",
        label="Release handoff capsule",
    )

    seal = _build_completion_seal(
        manifest=manifest,
        decision_event=last,
        decision_path=decision_path,
        decision=decision,
        capsule_before=capsule_before,
        release_handoff_path=resolved_release_handoff_path,
        release_handoff=release_handoff,
        verified_evidence_files=verified_files,
        evidence_bundle_sha256=evidence_bundle_sha256,
    )
    _write_self_hashed_artifact(
        resolved_seal_path,
        seal.to_dict(),
        hash_field="completion_seal_sha256",
        label="Campaign completion seal",
    )

    append_campaign_event(
        campaign_root=root,
        event_type="campaign_completed",
        payload={
            "candidate_id": decision.candidate_id,
            "hypothesis_id": decision.hypothesis_id,
            "reason": "campaign_completion_seal",
            "source_decision_artifact_path": str(decision_path),
            "source_decision_sha256": decision.decision_sha256,
            "source_decision_event_sha256": last.event_sha256,
            "completion_seal_path": str(resolved_seal_path),
            "completion_seal_sha256": seal.completion_seal_sha256,
            "release_handoff_path": str(resolved_release_handoff_path),
            "release_handoff_sha256": release_handoff.release_handoff_sha256,
            "release_status": "not_requested",
            "central_planning_lite_mutated": False,
        },
    )
    events_after = load_campaign_journal(root, manifest=manifest)
    completion_event = events_after[-1]
    resume = inspect_campaign(root, write_capsule=True)
    return CampaignCompletionResult(
        status="recorded",
        seal_path=resolved_seal_path,
        seal=seal,
        release_handoff_path=resolved_release_handoff_path,
        release_handoff=release_handoff,
        journal_appended=True,
        completion_event=completion_event,
        resume_capsule=resume,
    )


def load_campaign_completion_seal(path: Path) -> CampaignCompletionSeal:
    payload = _load_self_hashed_json(
        path,
        hash_field="completion_seal_sha256",
        label="Campaign completion seal",
    )
    if payload.get("schema_version") != COMPLETION_SCHEMA_VERSION:
        raise CampaignCompletionError(
            f"Unsupported campaign completion schema: {payload.get('schema_version')!r}"
        )
    if payload.get("seal_version") != COMPLETION_SEAL_VERSION:
        raise CampaignCompletionError(
            f"Unsupported campaign completion seal: {payload.get('seal_version')!r}"
        )
    restrictions = _string_list(payload.get("restrictions"), "completion.restrictions")
    return CampaignCompletionSeal(
        schema_version=COMPLETION_SCHEMA_VERSION,
        seal_version=COMPLETION_SEAL_VERSION,
        campaign_id=_required_string(payload.get("campaign_id"), "completion.campaign_id"),
        manifest_sha256=_required_sha(payload.get("manifest_sha256"), "completion.manifest_sha256"),
        candidate_id=_required_string(payload.get("candidate_id"), "completion.candidate_id"),
        hypothesis_id=_required_string(payload.get("hypothesis_id"), "completion.hypothesis_id"),
        frozen_parent=dict(_object(payload.get("frozen_parent"), "completion.frozen_parent")),
        independent_decision_path=_required_string(
            payload.get("independent_decision_path"), "completion.independent_decision_path"
        ),
        independent_decision_sha256=_required_sha(
            payload.get("independent_decision_sha256"), "completion.independent_decision_sha256"
        ),
        independent_decision_event_sequence=_positive_int(
            payload.get("independent_decision_event_sequence"),
            "completion.independent_decision_event_sequence",
        ),
        independent_decision_event_sha256=_required_sha(
            payload.get("independent_decision_event_sha256"),
            "completion.independent_decision_event_sha256",
        ),
        journal_head_sha256_before_completion=_required_sha(
            payload.get("journal_head_sha256_before_completion"),
            "completion.journal_head_sha256_before_completion",
        ),
        completion_reason=_required_string(payload.get("completion_reason"), "completion.completion_reason"),
        accepted_candidate=_required_bool(payload.get("accepted_candidate"), "completion.accepted_candidate"),
        expected_terminal_event=_required_string(
            payload.get("expected_terminal_event"), "completion.expected_terminal_event"
        ),
        attempts_started=_nonnegative_int(payload.get("attempts_started"), "completion.attempts_started"),
        attempts_completed=_nonnegative_int(
            payload.get("attempts_completed"), "completion.attempts_completed"
        ),
        total_tokens=_nonnegative_int(payload.get("total_tokens"), "completion.total_tokens"),
        wall_clock_seconds=_nonnegative_number(
            payload.get("wall_clock_seconds"), "completion.wall_clock_seconds"
        ),
        remaining_budget=dict(_object(payload.get("remaining_budget"), "completion.remaining_budget")),
        verified_attempts=_positive_int(payload.get("verified_attempts"), "completion.verified_attempts"),
        verified_evidence_files=_positive_int(
            payload.get("verified_evidence_files"), "completion.verified_evidence_files"
        ),
        evidence_bundle_sha256=_required_sha(
            payload.get("evidence_bundle_sha256"), "completion.evidence_bundle_sha256"
        ),
        release_handoff_path=_required_string(
            payload.get("release_handoff_path"), "completion.release_handoff_path"
        ),
        release_handoff_sha256=_required_sha(
            payload.get("release_handoff_sha256"), "completion.release_handoff_sha256"
        ),
        release_status=_required_string(payload.get("release_status"), "completion.release_status"),
        central_planning_lite_mutated=_required_bool(
            payload.get("central_planning_lite_mutated"),
            "completion.central_planning_lite_mutated",
        ),
        restrictions=tuple(restrictions),
        completion_seal_sha256=_required_sha(
            payload.get("completion_seal_sha256"), "completion.completion_seal_sha256"
        ),
    )


def load_release_handoff(path: Path) -> ReleaseHandoffCapsule:
    payload = _load_self_hashed_json(
        path,
        hash_field="release_handoff_sha256",
        label="Release handoff capsule",
    )
    if payload.get("schema_version") != COMPLETION_SCHEMA_VERSION:
        raise CampaignCompletionError(
            f"Unsupported release handoff schema: {payload.get('schema_version')!r}"
        )
    if payload.get("capsule_version") != RELEASE_HANDOFF_VERSION:
        raise CampaignCompletionError(
            f"Unsupported release handoff version: {payload.get('capsule_version')!r}"
        )
    actions = _string_list(
        payload.get("permitted_follow_up_actions"), "release_handoff.permitted_follow_up_actions"
    )
    restrictions = _string_list(payload.get("restrictions"), "release_handoff.restrictions")
    return ReleaseHandoffCapsule(
        schema_version=COMPLETION_SCHEMA_VERSION,
        capsule_version=RELEASE_HANDOFF_VERSION,
        campaign_id=_required_string(payload.get("campaign_id"), "release_handoff.campaign_id"),
        manifest_sha256=_required_sha(
            payload.get("manifest_sha256"), "release_handoff.manifest_sha256"
        ),
        candidate_id=_required_string(payload.get("candidate_id"), "release_handoff.candidate_id"),
        hypothesis_id=_required_string(payload.get("hypothesis_id"), "release_handoff.hypothesis_id"),
        frozen_parent=dict(_object(payload.get("frozen_parent"), "release_handoff.frozen_parent")),
        independent_decision_path=_required_string(
            payload.get("independent_decision_path"), "release_handoff.independent_decision_path"
        ),
        independent_decision_sha256=_required_sha(
            payload.get("independent_decision_sha256"), "release_handoff.independent_decision_sha256"
        ),
        independent_decision_event_sequence=_positive_int(
            payload.get("independent_decision_event_sequence"),
            "release_handoff.independent_decision_event_sequence",
        ),
        independent_decision_event_sha256=_required_sha(
            payload.get("independent_decision_event_sha256"),
            "release_handoff.independent_decision_event_sha256",
        ),
        reviewer_id=_required_string(payload.get("reviewer_id"), "release_handoff.reviewer_id"),
        accepted_candidate=_required_bool(
            payload.get("accepted_candidate"), "release_handoff.accepted_candidate"
        ),
        verified_attempts=_positive_int(
            payload.get("verified_attempts"), "release_handoff.verified_attempts"
        ),
        verified_evidence_files=_positive_int(
            payload.get("verified_evidence_files"), "release_handoff.verified_evidence_files"
        ),
        evidence_bundle_sha256=_required_sha(
            payload.get("evidence_bundle_sha256"), "release_handoff.evidence_bundle_sha256"
        ),
        completion_reason=_required_string(
            payload.get("completion_reason"), "release_handoff.completion_reason"
        ),
        release_status=_required_string(payload.get("release_status"), "release_handoff.release_status"),
        central_planning_lite_mutated=_required_bool(
            payload.get("central_planning_lite_mutated"),
            "release_handoff.central_planning_lite_mutated",
        ),
        next_action=_required_string(payload.get("next_action"), "release_handoff.next_action"),
        required_role=_required_string(payload.get("required_role"), "release_handoff.required_role"),
        permitted_follow_up_actions=tuple(actions),
        restrictions=tuple(restrictions),
        release_handoff_sha256=_required_sha(
            payload.get("release_handoff_sha256"), "release_handoff.release_handoff_sha256"
        ),
    )


def _verify_independent_decision_chain(
    *,
    manifest,
    events: tuple[JournalEvent, ...],
    decision_event: JournalEvent,
    decision_path: Path,
    decision: IndependentReviewDecision,
) -> tuple[int, str]:
    if decision.decision != "candidate_kept":
        raise CampaignCompletionError("Only candidate_kept may complete an accepted campaign")
    if decision.promotion_status != "not_requested":
        raise CampaignCompletionError("Independent decision unexpectedly authorizes promotion")
    if decision.manifest_sha256 != manifest.manifest_sha256:
        raise CampaignCompletionError("Independent decision manifest hash does not match campaign")
    if decision.frozen_parent != asdict(manifest.frozen_parent):
        raise CampaignCompletionError("Independent decision frozen parent does not match campaign")
    if decision_event.payload.get("candidate_id") != decision.candidate_id:
        raise CampaignCompletionError("candidate_kept candidate does not match decision artifact")
    if decision_event.payload.get("hypothesis_id") != decision.hypothesis_id:
        raise CampaignCompletionError("candidate_kept hypothesis does not match decision artifact")
    if Path(
        _required_string(
            decision_event.payload.get("decision_artifact_path"),
            "candidate_kept.decision_artifact_path",
        )
    ).resolve() != decision_path:
        raise CampaignCompletionError("candidate_kept decision path does not match decision artifact")
    if decision_event.payload.get("decision_sha256") != decision.decision_sha256:
        raise CampaignCompletionError("candidate_kept decision SHA-256 does not match decision artifact")
    if decision_event.payload.get("reviewer_id") != decision.reviewer_id:
        raise CampaignCompletionError("candidate_kept reviewer does not match decision artifact")
    if decision_event.payload.get("source_candidate_reviewed_event_sha256") != decision.candidate_reviewed_event_sha256:
        raise CampaignCompletionError("candidate_kept source review event does not match decision artifact")

    for restriction in (
        "promotion_not_authorized",
        "central_planning_lite_mutation_not_authorized",
        "release_gate_not_executed",
        "preserve_append_only_campaign_journal",
    ):
        if restriction not in decision.restrictions:
            raise CampaignCompletionError(
                f"Independent decision omitted required restriction {restriction!r}"
            )

    review = _load_self_hashed_json(
        Path(decision.review_path).resolve(),
        hash_field="review_sha256",
        label="Candidate review",
    )
    receipt = load_review_receipt(Path(decision.receipt_path).resolve())
    handoff = load_review_handoff(Path(decision.handoff_path).resolve())
    if review.get("review_sha256") != decision.review_sha256:
        raise CampaignCompletionError("Decision review SHA-256 binding is stale")
    if receipt.receipt_sha256 != decision.receipt_sha256:
        raise CampaignCompletionError("Decision receipt SHA-256 binding is stale")
    if handoff.handoff_sha256 != decision.handoff_sha256:
        raise CampaignCompletionError("Decision handoff SHA-256 binding is stale")
    if receipt.candidate_id != decision.candidate_id or handoff.candidate_id != decision.candidate_id:
        raise CampaignCompletionError("Review chain candidate differs from independent decision")
    if receipt.hypothesis_id != decision.hypothesis_id or handoff.hypothesis_id != decision.hypothesis_id:
        raise CampaignCompletionError("Review chain hypothesis differs from independent decision")
    if handoff.frozen_parent != asdict(manifest.frozen_parent):
        raise CampaignCompletionError("Review handoff frozen parent no longer matches campaign")
    if receipt.promotion_status != "not_requested" or handoff.promotion_status != "not_requested":
        raise CampaignCompletionError("Review chain unexpectedly authorizes promotion")

    reviewed_event = next(
        (
            event
            for event in events
            if event.sequence == decision.candidate_reviewed_event_sequence
            and event.event_sha256 == decision.candidate_reviewed_event_sha256
        ),
        None,
    )
    if reviewed_event is None or reviewed_event.event_type != "candidate_reviewed":
        raise CampaignCompletionError("Independent decision source candidate_reviewed event is missing")

    attempts = handoff.attempts
    if len(attempts) != decision.verified_attempts or decision.verified_attempts < 3:
        raise CampaignCompletionError("Independent decision does not bind three verified attempts")
    event_by_hash = {event.event_sha256: event for event in events}
    evidence_bundle: list[dict[str, Any]] = []
    verified_files = 0
    for attempt in attempts:
        event_sha = _required_sha(
            attempt.get("event_sha256"), "release_verification.attempt.event_sha256"
        )
        event = event_by_hash.get(event_sha)
        if event is None or event.event_type != "attempt_completed":
            raise CampaignCompletionError("Release verification attempt is missing from campaign journal")
        suite_root = Path(
            _required_string(attempt.get("suite_root"), "release_verification.attempt.suite_root")
        ).resolve()
        evidence = _object(
            attempt.get("evidence_sha256"), "release_verification.attempt.evidence_sha256"
        )
        if set(evidence) != REQUIRED_EVIDENCE_FILES:
            raise CampaignCompletionError(
                "Release verification attempt does not seal the six required evidence files"
            )
        normalized_evidence: dict[str, str] = {}
        for name in sorted(REQUIRED_EVIDENCE_FILES):
            expected = _required_sha(
                evidence.get(name), f"release_verification.attempt.evidence_sha256.{name}"
            )
            path = (suite_root / name).resolve()
            try:
                path.relative_to(suite_root)
            except ValueError as exc:  # pragma: no cover - defensive
                raise CampaignCompletionError("Evidence path escapes suite root") from exc
            if not path.is_file():
                raise CampaignCompletionError(f"Release verification evidence is missing: {path}")
            observed = _sha256_file(path)
            if observed != expected:
                raise CampaignCompletionError(
                    f"Release verification evidence SHA-256 mismatch for {path}: "
                    f"expected {expected}, observed {observed}"
                )
            normalized_evidence[name] = expected
            verified_files += 1
        evidence_bundle.append(
            {
                "attempt_id": _required_string(
                    attempt.get("attempt_id"), "release_verification.attempt.attempt_id"
                ),
                "event_sha256": event_sha,
                "evidence_sha256": normalized_evidence,
            }
        )
    if verified_files != decision.verified_evidence_files:
        raise CampaignCompletionError(
            "Fresh evidence verification count differs from independent decision artifact"
        )
    return verified_files, _sha256_json({"attempts": evidence_bundle})


def _build_release_handoff(
    *,
    manifest,
    decision_event: JournalEvent,
    decision_path: Path,
    decision: IndependentReviewDecision,
    verified_evidence_files: int,
    evidence_bundle_sha256: str,
) -> ReleaseHandoffCapsule:
    unsigned = {
        "schema_version": COMPLETION_SCHEMA_VERSION,
        "capsule_version": RELEASE_HANDOFF_VERSION,
        "campaign_id": manifest.campaign_id,
        "manifest_sha256": manifest.manifest_sha256,
        "candidate_id": decision.candidate_id,
        "hypothesis_id": decision.hypothesis_id,
        "frozen_parent": asdict(manifest.frozen_parent),
        "independent_decision_path": str(decision_path),
        "independent_decision_sha256": decision.decision_sha256,
        "independent_decision_event_sequence": decision_event.sequence,
        "independent_decision_event_sha256": decision_event.event_sha256,
        "reviewer_id": decision.reviewer_id,
        "accepted_candidate": True,
        "verified_attempts": decision.verified_attempts,
        "verified_evidence_files": verified_evidence_files,
        "evidence_bundle_sha256": evidence_bundle_sha256,
        "completion_reason": "accepted_candidate",
        "release_status": "not_requested",
        "central_planning_lite_mutated": False,
        "next_action": "await_release_gate",
        "required_role": RELEASE_ROLE,
        "permitted_follow_up_actions": (
            "verify_release_handoff",
            "prepare_release_candidate",
            "reject_release",
            "quarantine_release",
        ),
        "restrictions": (
            "promotion_not_authorized",
            "central_planning_lite_mutation_not_authorized",
            "release_gate_not_executed",
            "verify_campaign_completed_event_and_artifact_hashes_before_release_action",
            "preserve_append_only_campaign_journal",
        ),
    }
    digest_payload = dict(unsigned)
    digest_payload["permitted_follow_up_actions"] = list(unsigned["permitted_follow_up_actions"])
    digest_payload["restrictions"] = list(unsigned["restrictions"])
    return ReleaseHandoffCapsule(
        **{**unsigned, "release_handoff_sha256": _sha256_json(digest_payload)}
    )


def _build_completion_seal(
    *,
    manifest,
    decision_event: JournalEvent,
    decision_path: Path,
    decision: IndependentReviewDecision,
    capsule_before,
    release_handoff_path: Path,
    release_handoff: ReleaseHandoffCapsule,
    verified_evidence_files: int,
    evidence_bundle_sha256: str,
) -> CampaignCompletionSeal:
    unsigned = {
        "schema_version": COMPLETION_SCHEMA_VERSION,
        "seal_version": COMPLETION_SEAL_VERSION,
        "campaign_id": manifest.campaign_id,
        "manifest_sha256": manifest.manifest_sha256,
        "candidate_id": decision.candidate_id,
        "hypothesis_id": decision.hypothesis_id,
        "frozen_parent": asdict(manifest.frozen_parent),
        "independent_decision_path": str(decision_path),
        "independent_decision_sha256": decision.decision_sha256,
        "independent_decision_event_sequence": decision_event.sequence,
        "independent_decision_event_sha256": decision_event.event_sha256,
        "journal_head_sha256_before_completion": decision_event.event_sha256,
        "completion_reason": "accepted_candidate",
        "accepted_candidate": True,
        "expected_terminal_event": "campaign_completed",
        "attempts_started": capsule_before.attempts_started,
        "attempts_completed": capsule_before.attempts_completed,
        "total_tokens": capsule_before.total_tokens,
        "wall_clock_seconds": capsule_before.wall_clock_seconds,
        "remaining_budget": dict(capsule_before.remaining_budget),
        "verified_attempts": decision.verified_attempts,
        "verified_evidence_files": verified_evidence_files,
        "evidence_bundle_sha256": evidence_bundle_sha256,
        "release_handoff_path": str(release_handoff_path),
        "release_handoff_sha256": release_handoff.release_handoff_sha256,
        "release_status": "not_requested",
        "central_planning_lite_mutated": False,
        "restrictions": (
            "campaign_completion_is_not_release_promotion",
            "promotion_not_authorized",
            "central_planning_lite_mutation_not_authorized",
            "release_gate_not_executed",
            "preserve_append_only_campaign_journal",
        ),
    }
    digest_payload = dict(unsigned)
    digest_payload["restrictions"] = list(unsigned["restrictions"])
    return CampaignCompletionSeal(
        **{**unsigned, "completion_seal_sha256": _sha256_json(digest_payload)}
    )


def _replay_existing_completion(
    root: Path,
    *,
    manifest,
    events: tuple[JournalEvent, ...],
    completion_event: JournalEvent,
    seal_path: Path | None,
    release_handoff_path: Path | None,
) -> CampaignCompletionResult:
    payload = completion_event.payload
    if payload.get("reason") != "campaign_completion_seal":
        raise CampaignCompletionError("Existing campaign_completed event is not an E1.6 completion seal")
    existing_seal_path = Path(
        _required_string(payload.get("completion_seal_path"), "campaign_completed.completion_seal_path")
    ).resolve()
    existing_handoff_path = Path(
        _required_string(payload.get("release_handoff_path"), "campaign_completed.release_handoff_path")
    ).resolve()
    if seal_path is not None and seal_path.resolve() != existing_seal_path:
        raise CampaignCompletionError("Requested completion seal output differs from existing seal")
    if release_handoff_path is not None and release_handoff_path.resolve() != existing_handoff_path:
        raise CampaignCompletionError("Requested release handoff output differs from existing handoff")
    seal = load_campaign_completion_seal(existing_seal_path)
    handoff = load_release_handoff(existing_handoff_path)
    if payload.get("completion_seal_sha256") != seal.completion_seal_sha256:
        raise CampaignCompletionError("Existing completion seal hash differs from campaign journal")
    if payload.get("release_handoff_sha256") != handoff.release_handoff_sha256:
        raise CampaignCompletionError("Existing release handoff hash differs from campaign journal")
    if payload.get("source_decision_sha256") != seal.independent_decision_sha256:
        raise CampaignCompletionError("Existing completion seal decision binding differs from journal")
    if payload.get("source_decision_event_sha256") != seal.independent_decision_event_sha256:
        raise CampaignCompletionError("Existing completion seal source event differs from journal")
    if seal.release_handoff_sha256 != handoff.release_handoff_sha256:
        raise CampaignCompletionError("Completion seal release handoff binding differs")
    if handoff.release_status != "not_requested" or seal.release_status != "not_requested":
        raise CampaignCompletionError("Existing completion artifacts unexpectedly authorize release")
    if handoff.central_planning_lite_mutated or seal.central_planning_lite_mutated:
        raise CampaignCompletionError("Existing completion artifacts claim central mutation")

    decision_event = next(
        (
            event
            for event in events
            if event.event_sha256 == seal.independent_decision_event_sha256
            and event.sequence == seal.independent_decision_event_sequence
        ),
        None,
    )
    if decision_event is None or decision_event.event_type != "candidate_kept":
        raise CampaignCompletionError("Completion seal source candidate_kept event is missing")
    decision_path = Path(seal.independent_decision_path).resolve()
    try:
        decision = load_independent_review_decision(decision_path)
        verified_files, evidence_bundle_sha256 = _verify_independent_decision_chain(
            manifest=manifest,
            events=events[:-1],
            decision_event=decision_event,
            decision_path=decision_path,
            decision=decision,
        )
    except CampaignCompletionError:
        raise
    except CampaignError as exc:
        raise CampaignCompletionError(
            f"Existing completion decision chain failed verification: {exc}"
        ) from exc
    if verified_files != seal.verified_evidence_files or verified_files != handoff.verified_evidence_files:
        raise CampaignCompletionError("Completion artifact verified evidence count is stale")
    if evidence_bundle_sha256 != seal.evidence_bundle_sha256 or evidence_bundle_sha256 != handoff.evidence_bundle_sha256:
        raise CampaignCompletionError("Completion artifact evidence bundle binding is stale")

    resume = inspect_campaign(root, write_capsule=True)
    return CampaignCompletionResult(
        status="already-recorded",
        seal_path=existing_seal_path,
        seal=seal,
        release_handoff_path=existing_handoff_path,
        release_handoff=handoff,
        journal_appended=False,
        completion_event=completion_event,
        resume_capsule=resume,
    )


def _write_self_hashed_artifact(
    path: Path,
    payload: Mapping[str, Any],
    *,
    hash_field: str,
    label: str,
) -> None:
    _verify_self_hash(payload, hash_field=hash_field, label=label)
    target = path.resolve()
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if target.exists():
        if target.read_text(encoding="utf-8") == text:
            return
        raise CampaignCompletionError(f"{label} already exists with different content: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    temp = target.with_name(f".{target.name}.tmp")
    temp.write_text(text, encoding="utf-8", newline="")
    temp.replace(target)


def _load_self_hashed_json(
    path: Path,
    *,
    hash_field: str,
    label: str,
) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CampaignCompletionError(f"{label} was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CampaignCompletionError(f"{label} is invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise CampaignCompletionError(f"{label} root must be an object: {path}")
    _verify_self_hash(payload, hash_field=hash_field, label=label)
    return payload


def _verify_self_hash(payload: Mapping[str, Any], *, hash_field: str, label: str) -> None:
    supplied = _required_sha(payload.get(hash_field), f"{label}.{hash_field}")
    unsigned = dict(payload)
    unsigned.pop(hash_field, None)
    calculated = _sha256_json(unsigned)
    if supplied != calculated:
        raise CampaignCompletionError(
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
        raise CampaignCompletionError(f"{label} must be a non-empty string")
    return value.strip()


def _required_sha(value: Any, label: str) -> str:
    text = _required_string(value, label).lower()
    if not SHA256_RE.fullmatch(text):
        raise CampaignCompletionError(f"{label} must be a SHA-256 digest")
    return text


def _positive_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CampaignCompletionError(f"{label} must be a positive integer")
    return value


def _nonnegative_int(value: Any, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CampaignCompletionError(f"{label} must be a non-negative integer")
    return value


def _nonnegative_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
        raise CampaignCompletionError(f"{label} must be a non-negative number")
    return float(value)


def _required_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise CampaignCompletionError(f"{label} must be boolean")
    return value


def _object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CampaignCompletionError(f"{label} must be an object")
    return dict(value)


def _string_list(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise CampaignCompletionError(f"{label} must be a list of non-empty strings")
    return list(value)
