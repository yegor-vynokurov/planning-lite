from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from planning_lite.campaign.campaign import (
    CampaignError,
    append_campaign_event,
    initialize_campaign,
    inspect_campaign,
    load_campaign_journal,
    load_manifest_template,
)
from planning_lite.campaign.candidate_review import (
    review_campaign_candidate,
    write_candidate_review,
)
from planning_lite.campaign.review_receipt import (
    ReviewReceiptError,
    load_review_handoff,
    load_review_receipt,
    record_candidate_review_receipt,
)


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "planning_lite_campaign.py"


class ReviewReceiptAndHandoffTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        frozen = self.root / "frozen.txt"
        frozen.write_text("frozen\n", encoding="utf-8")
        manifest_path = self.root / "manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "campaign_id": "review-receipt-test",
                    "purpose": "Test review receipt and handoff capsule.",
                    "frozen_parent": {
                        "repository": "planning-lite",
                        "commit": "bd8c4224ca0fb708ebe3c6dd000491f2f03da4fe",
                        "tag": "v4.2.0",
                    },
                    "frozen_inputs": [
                        {
                            "input_id": "fixture",
                            "role": "verification",
                            "path": "frozen.txt",
                            "sha256": hashlib.sha256(frozen.read_bytes()).hexdigest(),
                        }
                    ],
                    "mutable_scope": ["src/planning_lite/campaign/**"],
                    "off_limits": ["template/**"],
                    "budget": {
                        "max_candidates": 2,
                        "max_attempts_per_candidate": 3,
                        "max_total_attempts": 6,
                        "max_total_tokens": 100000,
                        "max_wall_clock_seconds": 10000,
                    },
                    "stop_policy": {
                        "stop_on_hard_gate_failure": True,
                        "stop_after_accepted_candidate": True,
                        "max_consecutive_non_improving": 3,
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        self.campaign_root = self.root / "campaign"
        initialize_campaign(
            campaign_root=self.campaign_root,
            manifest=load_manifest_template(manifest_path),
            inputs_root=self.root,
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="hypothesis_registered",
            payload={"hypothesis_id": "H-001", "summary": "Receipt hypothesis"},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_registered",
            payload={
                "hypothesis_id": "H-001",
                "candidate_id": "C-001",
                "summary": "Receipt candidate",
            },
        )

    def tearDown(self):
        self.temp.cleanup()

    def _attempt(
        self,
        index: int,
        *,
        verdict_status: str = "promote-for-fixture",
        recommended_arm: str | None = "snapshot",
        hard_gate_passed: bool = True,
    ) -> None:
        attempt_id = f"A-{index:03d}"
        suite_id = f"suite-{index:03d}"
        suite_root = str((self.root / "suites" / suite_id).resolve())
        plan_sha = hashlib.sha256(f"plan:{index}".encode()).hexdigest()
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "suite": {
                    "suite_id": suite_id,
                    "suite_root": suite_root,
                    "eval_id": "lifecycle-status",
                    "source_commit": "abc123",
                    "plan_sha256": plan_sha,
                },
            },
        )
        evidence = {
            name: hashlib.sha256(f"{index}:{name}".encode()).hexdigest()
            for name in (
                "suite-plan.json",
                "suite-state.json",
                "suite-result.json",
                "suite-aggregation.json",
                "suite-report.json",
                "suite-verdict.json",
            )
        }
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "hard_gate_passed": hard_gate_passed,
                "improved": verdict_status in {"promote-for-fixture", "promote-routing-policy"},
                "metrics": {"total_tokens": 100 + index, "duration_seconds": 1.0},
                "suite": {
                    "suite_id": suite_id,
                    "suite_root": suite_root,
                    "eval_id": "lifecycle-status",
                    "source_commit": "abc123",
                    "plan_sha256": plan_sha,
                    "verdict_status": verdict_status,
                    "recommended_arm": recommended_arm,
                    "evidence_sha256": evidence,
                },
            },
        )

    def _write_review(self) -> Path:
        path = self.campaign_root / "candidate-review.json"
        write_candidate_review(path, review_campaign_candidate(self.campaign_root))
        return path

    def test_keep_receipt_appends_once_and_waits_for_independent_review(self):
        for index in range(1, 4):
            self._attempt(index)
        review_path = self._write_review()
        before_count = len(load_campaign_journal(self.campaign_root))
        result = record_candidate_review_receipt(self.campaign_root, review_path=review_path)
        after = load_campaign_journal(self.campaign_root)

        self.assertTrue(result.journal_appended)
        self.assertEqual(result.status, "recorded")
        self.assertEqual(len(after), before_count + 1)
        self.assertEqual(after[-1].event_type, "candidate_reviewed")
        self.assertEqual(after[-1].payload["decision"], "keep")
        self.assertEqual(result.resume_capsule.next_action, "await_independent_review")
        self.assertEqual(result.receipt.promotion_status, "not_requested")
        self.assertEqual(result.handoff.required_role, "independent_reviewer")
        self.assertIn("promotion_not_authorized", result.handoff.restrictions)
        self.assertEqual(load_review_receipt(result.receipt_path), result.receipt)
        self.assertEqual(load_review_handoff(result.handoff_path), result.handoff)

    def test_receipt_replay_is_idempotent_and_does_not_change_journal(self):
        for index in range(1, 4):
            self._attempt(index)
        self._write_review()
        first = record_candidate_review_receipt(self.campaign_root)
        journal_before = (self.campaign_root / "campaign-journal.jsonl").read_bytes()
        receipt_before = first.receipt_path.read_bytes()
        handoff_before = first.handoff_path.read_bytes()

        second = record_candidate_review_receipt(self.campaign_root)
        self.assertFalse(second.journal_appended)
        self.assertEqual(second.status, "already-recorded")
        self.assertEqual(journal_before, (self.campaign_root / "campaign-journal.jsonl").read_bytes())
        self.assertEqual(receipt_before, second.receipt_path.read_bytes())
        self.assertEqual(handoff_before, second.handoff_path.read_bytes())
        self.assertEqual(first.receipt.receipt_sha256, second.receipt.receipt_sha256)

    def test_keep_receipt_does_not_authorize_candidate_kept_implicitly(self):
        for index in range(1, 4):
            self._attempt(index)
        self._write_review()
        record_candidate_review_receipt(self.campaign_root)
        events = load_campaign_journal(self.campaign_root)
        self.assertNotIn("candidate_kept", {event.event_type for event in events})
        self.assertEqual(inspect_campaign(self.campaign_root).next_action, "await_independent_review")

    def test_reject_receipt_allows_explicit_candidate_rejected_before_stop(self):
        self._attempt(
            1,
            verdict_status="reject-candidates",
            recommended_arm=None,
            hard_gate_passed=False,
        )
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "reject")
        write_candidate_review(self.campaign_root / "candidate-review.json", proposal)
        result = record_candidate_review_receipt(self.campaign_root)
        self.assertEqual(result.resume_capsule.next_action, "record_candidate_rejected")

        capsule = append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_rejected",
            payload={"candidate_id": "C-001", "reason": "review receipt reject"},
        )
        self.assertEqual(capsule.next_action, "record_campaign_stopped")

    def test_continue_receipt_routes_to_next_independent_attempt(self):
        self._attempt(1)
        self._attempt(2)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        write_candidate_review(self.campaign_root / "candidate-review.json", proposal)
        result = record_candidate_review_receipt(self.campaign_root)
        self.assertEqual(result.resume_capsule.next_action, "start_next_independent_attempt")
        self.assertIn("attempt_started", result.handoff.permitted_follow_up_events)

        capsule = append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-003",
                "suite": {
                    "suite_id": "suite-003",
                    "suite_root": str(self.root / "suites" / "suite-003"),
                    "eval_id": "lifecycle-status",
                    "source_commit": "abc123",
                    "plan_sha256": hashlib.sha256(b"plan:3").hexdigest(),
                },
            },
        )
        self.assertEqual(capsule.next_action, "recover_or_complete_attempt")

    def test_continue_can_be_reviewed_again_after_new_completed_attempt(self):
        self._attempt(1)
        self._attempt(2)
        first_proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(first_proposal.decision, "continue")
        review_path = self.campaign_root / "candidate-review.json"
        write_candidate_review(review_path, first_proposal)
        first_receipt = record_candidate_review_receipt(self.campaign_root)

        with self.assertRaisesRegex(Exception, "already has a review receipt"):
            review_campaign_candidate(self.campaign_root)

        attempt_id = "A-003"
        suite_id = "suite-003"
        plan_sha = hashlib.sha256(b"plan:3").hexdigest()
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "suite": {
                    "suite_id": suite_id,
                    "suite_root": str(self.root / "suites" / suite_id),
                    "eval_id": "lifecycle-status",
                    "source_commit": "abc123",
                    "plan_sha256": plan_sha,
                },
            },
        )
        evidence = {
            name: hashlib.sha256(f"3:{name}".encode()).hexdigest()
            for name in (
                "suite-plan.json",
                "suite-state.json",
                "suite-result.json",
                "suite-aggregation.json",
                "suite-report.json",
                "suite-verdict.json",
            )
        }
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "hard_gate_passed": True,
                "improved": True,
                "metrics": {"total_tokens": 103, "duration_seconds": 1.0},
                "suite": {
                    "suite_id": suite_id,
                    "suite_root": str(self.root / "suites" / suite_id),
                    "eval_id": "lifecycle-status",
                    "source_commit": "abc123",
                    "plan_sha256": plan_sha,
                    "verdict_status": "promote-for-fixture",
                    "recommended_arm": "snapshot",
                    "evidence_sha256": evidence,
                },
            },
        )
        second_proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(second_proposal.decision, "keep")
        write_candidate_review(review_path, second_proposal, replace=True)
        second_receipt = record_candidate_review_receipt(self.campaign_root)
        self.assertNotEqual(
            first_receipt.receipt.receipt_sha256,
            second_receipt.receipt.receipt_sha256,
        )
        self.assertNotEqual(first_receipt.receipt_path, second_receipt.receipt_path)
        self.assertEqual(inspect_campaign(self.campaign_root).next_action, "await_independent_review")

    def test_stale_review_is_rejected(self):
        self._attempt(1)
        self._attempt(2)
        review_path = self._write_review()
        self._attempt(3)
        with self.assertRaisesRegex(ReviewReceiptError, "stale"):
            record_candidate_review_receipt(self.campaign_root, review_path=review_path)

    def test_tampered_review_self_hash_is_rejected(self):
        for index in range(1, 4):
            self._attempt(index)
        review_path = self._write_review()
        payload = json.loads(review_path.read_text(encoding="utf-8"))
        payload["summary"] = "tampered"
        review_path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(ReviewReceiptError, "SHA-256 mismatch"):
            record_candidate_review_receipt(self.campaign_root)

    def test_tampered_handoff_or_receipt_fails_closed_on_replay(self):
        for index in range(1, 4):
            self._attempt(index)
        self._write_review()
        result = record_candidate_review_receipt(self.campaign_root)

        handoff_payload = json.loads(result.handoff_path.read_text(encoding="utf-8"))
        handoff_payload["required_role"] = "intruder"
        result.handoff_path.write_text(json.dumps(handoff_payload), encoding="utf-8")
        with self.assertRaisesRegex(ReviewReceiptError, "different content"):
            record_candidate_review_receipt(self.campaign_root)

        result.handoff_path.write_text(
            json.dumps(result.handoff.to_dict(), sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )
        receipt_payload = json.loads(result.receipt_path.read_text(encoding="utf-8"))
        receipt_payload["next_action"] = "promote"
        result.receipt_path.write_text(json.dumps(receipt_payload), encoding="utf-8")
        with self.assertRaisesRegex(ReviewReceiptError, "different content"):
            record_candidate_review_receipt(self.campaign_root)

    def test_generic_campaign_record_cannot_forge_candidate_reviewed(self):
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "campaign-record",
                "--campaign-root",
                str(self.campaign_root),
                "--event-type",
                "candidate_reviewed",
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid choice", result.stderr)

    def test_cli_receipt_does_not_require_eval_fixture(self):
        for index in range(1, 4):
            self._attempt(index)
        self._write_review()
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "campaign-review-receipt",
                "--campaign-root",
                str(self.campaign_root),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "recorded")
        self.assertTrue(payload["journal_appended"])
        self.assertEqual(payload["decision"], "keep")
        self.assertEqual(payload["promotion_status"], "not_requested")
        self.assertEqual(payload["next_action"], "await_independent_review")

    def test_invalid_decision_follow_up_fails_closed(self):
        self._attempt(1)
        self._attempt(2)
        self._write_review()
        record_candidate_review_receipt(self.campaign_root)
        with self.assertRaisesRegex(CampaignError, "does not permit"):
            append_campaign_event(
                campaign_root=self.campaign_root,
                event_type="candidate_rejected",
                payload={"candidate_id": "C-001", "reason": "not allowed after continue"},
            )


if __name__ == "__main__":
    unittest.main()
