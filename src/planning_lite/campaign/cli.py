from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from planning_lite import __version__

from .campaign import (
    EVENT_TYPES,
    CampaignError,
    append_campaign_event,
    initialize_campaign,
    inspect_campaign,
    load_manifest_template,
)
from .candidate_review import CandidateReviewError, review_campaign_candidate, write_candidate_review
from .review_receipt import ReviewReceiptError, record_candidate_review_receipt
from .independent_review import IndependentReviewError, record_independent_review_decision
from .campaign_completion import CampaignCompletionError, record_campaign_completion


def emit(payload: object) -> None:
    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def _failure_class(exc: Exception) -> str:
    mapping = (
        (CampaignCompletionError, "campaign_completion_error"),
        (IndependentReviewError, "independent_review_error"),
        (ReviewReceiptError, "review_receipt_error"),
        (CandidateReviewError, "candidate_review_error"),
        (CampaignError, "campaign_error"),
    )
    for error_type, label in mapping:
        if isinstance(exc, error_type):
            return label
    return "campaign_error"


def _failure_next_action(exc: Exception) -> str:
    mapping = (
        (CampaignCompletionError, "inspect_completion_seal_release_handoff_or_decision_chain"),
        (IndependentReviewError, "inspect_independent_review_chain_or_decision_artifact"),
        (ReviewReceiptError, "inspect_review_receipt_handoff_or_campaign_journal"),
        (CandidateReviewError, "inspect_candidate_attempts_suite_evidence_or_review_artifact"),
        (CampaignError, "inspect_campaign_manifest_journal_or_frozen_inputs"),
    )
    for error_type, action in mapping:
        if isinstance(exc, error_type):
            return action
    return "inspect_campaign_inputs"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="planning-lite-campaign",
        description=(
            "Planning Lite bounded Experiment Campaign Core. This tool records and "
            "seals experiment evidence; it does not authorize release promotion."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    campaign_init = sub.add_parser("campaign-init")
    campaign_init.add_argument("--manifest", required=True)
    campaign_init.add_argument("--campaign-root", required=True)
    campaign_init.add_argument("--inputs-root", default=None)
    campaign_init.add_argument("--skip-input-verification", action="store_true")

    campaign_record = sub.add_parser("campaign-record")
    campaign_record.add_argument("--campaign-root", required=True)
    campaign_record.add_argument(
        "--event-type",
        required=True,
        choices=tuple(
            item
            for item in EVENT_TYPES
            if item not in {
                "campaign_initialized",
                "candidate_reviewed",
                "candidate_kept",
                "candidate_rejected",
                "candidate_quarantined",
                "campaign_completed",
            }
        ),
    )
    campaign_record.add_argument("--payload-json", default="{}")

    campaign_status = sub.add_parser("campaign-status")
    campaign_status.add_argument("--campaign-root", required=True)

    campaign_review = sub.add_parser("campaign-review")
    campaign_review.add_argument("--campaign-root", required=True)
    campaign_review.add_argument("--candidate-id", default=None)
    campaign_review.add_argument("--output", default=None)
    campaign_review.add_argument("--replace", action="store_true")

    review_receipt = sub.add_parser("campaign-review-receipt")
    review_receipt.add_argument("--campaign-root", required=True)
    review_receipt.add_argument("--review", default=None)
    review_receipt.add_argument("--receipt-output", default=None)
    review_receipt.add_argument("--handoff-output", default=None)

    independent_review = sub.add_parser("campaign-independent-review")
    independent_review.add_argument("--campaign-root", required=True)
    independent_review.add_argument(
        "--decision",
        required=True,
        choices=("candidate_kept", "candidate_rejected", "candidate_quarantined"),
    )
    independent_review.add_argument("--reviewer-id", required=True)
    independent_review.add_argument("--attestation", required=True)
    independent_review.add_argument("--output", default=None)

    campaign_complete = sub.add_parser("campaign-complete")
    campaign_complete.add_argument("--campaign-root", required=True)
    campaign_complete.add_argument("--seal-output", default=None)
    campaign_complete.add_argument("--release-handoff-output", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "campaign-init":
            manifest = load_manifest_template(Path(args.manifest))
            capsule = initialize_campaign(
                campaign_root=Path(args.campaign_root),
                manifest=manifest,
                verify_inputs=not args.skip_input_verification,
                inputs_root=Path(args.inputs_root) if args.inputs_root else None,
            )
            emit({"status": "initialized", "campaign_root": str(Path(args.campaign_root).resolve()), "resume_capsule": capsule.to_dict()})
            return 0

        if args.command == "campaign-record":
            try:
                payload = json.loads(args.payload_json)
            except json.JSONDecodeError as exc:
                raise CampaignError("--payload-json must be valid JSON") from exc
            if not isinstance(payload, dict):
                raise CampaignError("--payload-json root must be an object")
            capsule = append_campaign_event(
                campaign_root=Path(args.campaign_root),
                event_type=args.event_type,
                payload=payload,
            )
            emit({"status": "recorded", "campaign_root": str(Path(args.campaign_root).resolve()), "resume_capsule": capsule.to_dict()})
            return 0

        if args.command == "campaign-status":
            capsule = inspect_campaign(Path(args.campaign_root), write_capsule=True)
            emit({"status": "valid", "campaign_root": str(Path(args.campaign_root).resolve()), "resume_capsule": capsule.to_dict()})
            return 0

        if args.command == "campaign-review":
            campaign_root = Path(args.campaign_root).resolve()
            proposal = review_campaign_candidate(campaign_root, candidate_id=args.candidate_id)
            output = Path(args.output).resolve() if args.output else campaign_root / "candidate-review.json"
            write_candidate_review(output, proposal, replace=args.replace)
            emit({"status": "reviewed", "campaign_root": str(campaign_root), "review_path": str(output), "decision": proposal.decision, "promotion_status": proposal.promotion_status, "review": proposal.to_dict()})
            return 0

        if args.command == "campaign-review-receipt":
            campaign_root = Path(args.campaign_root).resolve()
            result = record_candidate_review_receipt(
                campaign_root,
                review_path=Path(args.review) if args.review else None,
                receipt_path=Path(args.receipt_output) if args.receipt_output else None,
                handoff_path=Path(args.handoff_output) if args.handoff_output else None,
            )
            emit({"status": result.status, "campaign_root": str(campaign_root), "journal_appended": result.journal_appended, "receipt_path": str(result.receipt_path), "handoff_path": str(result.handoff_path), "decision": result.receipt.decision, "promotion_status": result.receipt.promotion_status, "next_action": result.resume_capsule.next_action, "receipt": result.receipt.to_dict(), "handoff": result.handoff.to_dict(), "resume_capsule": result.resume_capsule.to_dict()})
            return 0

        if args.command == "campaign-independent-review":
            campaign_root = Path(args.campaign_root).resolve()
            result = record_independent_review_decision(
                campaign_root,
                decision=args.decision,
                reviewer_id=args.reviewer_id,
                attestation=args.attestation,
                decision_path=Path(args.output) if args.output else None,
            )
            emit({"status": result.status, "campaign_root": str(campaign_root), "journal_appended": result.journal_appended, "decision": result.decision.decision, "promotion_status": result.decision.promotion_status, "decision_path": str(result.decision_path), "decision_sha256": result.decision.decision_sha256, "decision_event_sequence": result.decision_event.sequence, "decision_event_sha256": result.decision_event.event_sha256, "next_action": result.next_action, "decision_artifact": result.decision.to_dict()})
            return 0

        if args.command == "campaign-complete":
            campaign_root = Path(args.campaign_root).resolve()
            result = record_campaign_completion(
                campaign_root,
                seal_path=Path(args.seal_output) if args.seal_output else None,
                release_handoff_path=Path(args.release_handoff_output) if args.release_handoff_output else None,
            )
            emit({"status": result.status, "campaign_root": str(campaign_root), "journal_appended": result.journal_appended, "completion_seal_path": str(result.seal_path), "completion_seal_sha256": result.seal.completion_seal_sha256, "release_handoff_path": str(result.release_handoff_path), "release_handoff_sha256": result.release_handoff.release_handoff_sha256, "campaign_complete": result.resume_capsule.campaign_status == "completed", "candidate_accepted": result.seal.accepted_candidate, "release_status": result.release_handoff.release_status, "central_planning_lite_mutated": result.release_handoff.central_planning_lite_mutated, "completion_event_sequence": result.completion_event.sequence, "completion_event_sha256": result.completion_event.event_sha256, "next_release_action": result.release_handoff.next_action, "completion_seal": result.seal.to_dict(), "release_handoff": result.release_handoff.to_dict(), "resume_capsule": result.resume_capsule.to_dict()})
            return 0
    except CampaignError as exc:
        emit({"status": "invalid", "failure_class": _failure_class(exc), "message": str(exc), "next_action": _failure_next_action(exc)})
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
