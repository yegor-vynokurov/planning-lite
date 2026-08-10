from __future__ import annotations

import hashlib
import json
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
from planning_lite.campaign.cli import build_parser
from planning_lite.campaign.independent_review import (
    IndependentReviewError,
    load_independent_review_decision,
    record_independent_review_decision,
)
from planning_lite.campaign.review_receipt import record_candidate_review_receipt


class IndependentReviewDecisionGateTests(unittest.TestCase):
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
                    "campaign_id": "independent-review-test",
                    "purpose": "Test independent review decision gate.",
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
            payload={"hypothesis_id": "H-001", "summary": "Independent review hypothesis"},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_registered",
            payload={
                "hypothesis_id": "H-001",
                "candidate_id": "C-001",
                "summary": "Independent review candidate",
            },
        )
        for index in range(1, 4):
            self._attempt(index)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "keep")
        write_candidate_review(self.campaign_root / "candidate-review.json", proposal)
        self.receipt = record_candidate_review_receipt(self.campaign_root)
        self.assertEqual(self.receipt.resume_capsule.next_action, "await_independent_review")

    def tearDown(self):
        self.temp.cleanup()

    def _attempt(self, index: int) -> None:
        attempt_id = f"A-{index:03d}"
        suite_id = f"suite-{index:03d}"
        suite_root = self.root / "suites" / suite_id
        suite_root.mkdir(parents=True, exist_ok=True)
        critical = (
            "suite-plan.json",
            "suite-state.json",
            "suite-result.json",
            "suite-aggregation.json",
            "suite-report.json",
            "suite-verdict.json",
        )
        for name in critical:
            (suite_root / name).write_text(
                json.dumps({"suite_id": suite_id, "artifact": name, "index": index}, sort_keys=True) + "\n",
                encoding="utf-8",
            )
        evidence = {
            name: hashlib.sha256((suite_root / name).read_bytes()).hexdigest()
            for name in critical
        }
        identity = {
            "suite_id": suite_id,
            "suite_root": str(suite_root.resolve()),
            "eval_id": "lifecycle-status",
            "source_commit": "abc123",
            "plan_sha256": evidence["suite-plan.json"],
        }
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "suite": identity,
            },
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "hard_gate_passed": True,
                "improved": True,
                "metrics": {"total_tokens": 100 + index, "duration_seconds": 1.0},
                "suite": {
                    **identity,
                    "verdict_status": "promote-for-fixture",
                    "recommended_arm": "snapshot",
                    "evidence_sha256": evidence,
                },
            },
        )

    def _record(self, decision: str = "candidate_kept"):
        return record_independent_review_decision(
            self.campaign_root,
            decision=decision,
            reviewer_id="reviewer-001",
            attestation="I independently verified the sealed artifact chain and evidence hashes.",
        )

    def test_candidate_kept_appends_explicit_decision_without_promotion(self):
        before = len(load_campaign_journal(self.campaign_root))
        result = self._record("candidate_kept")
        after = load_campaign_journal(self.campaign_root)
        self.assertEqual(result.status, "recorded")
        self.assertTrue(result.journal_appended)
        self.assertEqual(len(after), before + 1)
        self.assertEqual(after[-1].event_type, "candidate_kept")
        self.assertEqual(result.decision.promotion_status, "not_requested")
        self.assertIn("release_gate_not_executed", result.decision.restrictions)
        self.assertEqual(result.next_action, "record_campaign_completed")
        self.assertEqual(load_independent_review_decision(result.decision_path), result.decision)

    def test_candidate_rejected_is_an_explicit_independent_decision(self):
        result = self._record("candidate_rejected")
        self.assertEqual(result.decision_event.event_type, "candidate_rejected")
        self.assertEqual(result.next_action, "register_candidate")
        self.assertEqual(result.decision.promotion_status, "not_requested")

    def test_candidate_quarantined_is_an_explicit_independent_decision(self):
        result = self._record("candidate_quarantined")
        self.assertEqual(result.decision_event.event_type, "candidate_quarantined")
        self.assertEqual(result.next_action, "register_candidate")

    def test_replay_is_idempotent(self):
        first = self._record()
        journal = (self.campaign_root / "campaign-journal.jsonl").read_bytes()
        artifact = first.decision_path.read_bytes()
        second = self._record()
        self.assertEqual(second.status, "already-recorded")
        self.assertFalse(second.journal_appended)
        self.assertEqual(journal, (self.campaign_root / "campaign-journal.jsonl").read_bytes())
        self.assertEqual(artifact, second.decision_path.read_bytes())
        self.assertEqual(first.decision.decision_sha256, second.decision.decision_sha256)

    def test_replay_with_different_reviewer_fails_closed(self):
        self._record()
        with self.assertRaises(IndependentReviewError):
            record_independent_review_decision(
                self.campaign_root,
                decision="candidate_kept",
                reviewer_id="reviewer-002",
                attestation="I independently verified the sealed artifact chain and evidence hashes.",
            )

    def test_replay_with_different_decision_fails_closed(self):
        self._record("candidate_kept")
        with self.assertRaises(IndependentReviewError):
            self._record("candidate_rejected")

    def test_tampered_suite_evidence_fails_closed(self):
        handoff = self.receipt.handoff
        suite_root = Path(handoff.attempts[0]["suite_root"])
        (suite_root / "suite-report.json").write_text("tampered\n", encoding="utf-8")
        with self.assertRaises(IndependentReviewError):
            self._record()

    def test_tampered_receipt_fails_closed(self):
        payload = json.loads(self.receipt.receipt_path.read_text(encoding="utf-8"))
        payload["reviewer_note"] = "tampered"
        self.receipt.receipt_path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(Exception):
            self._record()

    def test_tampered_handoff_fails_closed(self):
        payload = json.loads(self.receipt.handoff_path.read_text(encoding="utf-8"))
        payload["frozen_parent"]["commit"] = "deadbeef"
        self.receipt.handoff_path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(Exception):
            self._record()

    def test_tampered_review_fails_closed(self):
        review_path = self.campaign_root / "candidate-review.json"
        payload = json.loads(review_path.read_text(encoding="utf-8"))
        payload["summary"] = "tampered"
        review_path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(IndependentReviewError):
            self._record()

    def test_non_keep_receipt_is_not_an_independent_review_handoff(self):
        # Build a separate reject campaign because the fixture in setUp already has a keep receipt.
        root = self.root / "reject-case"
        root.mkdir()
        frozen = root / "frozen.txt"
        frozen.write_text("frozen\n", encoding="utf-8")
        manifest_path = root / "manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "campaign_id": "reject-review-test",
                    "purpose": "reject path",
                    "frozen_parent": {"repository": "planning-lite", "commit": "abc", "tag": "v"},
                    "frozen_inputs": [{"input_id": "f", "role": "verification", "path": "frozen.txt", "sha256": hashlib.sha256(frozen.read_bytes()).hexdigest()}],
                    "mutable_scope": ["src/**"],
                    "off_limits": ["template/**"],
                    "budget": {"max_candidates": 2, "max_attempts_per_candidate": 3, "max_total_attempts": 6, "max_total_tokens": 10000, "max_wall_clock_seconds": 1000},
                    "stop_policy": {"stop_on_hard_gate_failure": False, "stop_after_accepted_candidate": True, "max_consecutive_non_improving": 3},
                }
            ),
            encoding="utf-8",
        )
        campaign = root / "campaign"
        initialize_campaign(campaign_root=campaign, manifest=load_manifest_template(manifest_path), inputs_root=root)
        append_campaign_event(campaign_root=campaign, event_type="hypothesis_registered", payload={"hypothesis_id": "H"})
        append_campaign_event(campaign_root=campaign, event_type="candidate_registered", payload={"hypothesis_id": "H", "candidate_id": "C"})
        suite_root = root / "suite"
        suite_root.mkdir()
        critical = ("suite-plan.json", "suite-state.json", "suite-result.json", "suite-aggregation.json", "suite-report.json", "suite-verdict.json")
        for name in critical:
            (suite_root / name).write_text(name, encoding="utf-8")
        evidence = {name: hashlib.sha256((suite_root / name).read_bytes()).hexdigest() for name in critical}
        identity = {"suite_id": "s", "suite_root": str(suite_root.resolve()), "eval_id": "lifecycle-status", "source_commit": "abc", "plan_sha256": evidence["suite-plan.json"]}
        append_campaign_event(campaign_root=campaign, event_type="attempt_started", payload={"candidate_id": "C", "attempt_id": "A", "suite": identity})
        append_campaign_event(campaign_root=campaign, event_type="attempt_completed", payload={"candidate_id": "C", "attempt_id": "A", "hard_gate_passed": True, "improved": False, "metrics": {}, "suite": {**identity, "verdict_status": "retain-baseline", "recommended_arm": None, "evidence_sha256": evidence}})
        proposal = review_campaign_candidate(campaign)
        self.assertEqual(proposal.decision, "continue")
        write_candidate_review(campaign / "candidate-review.json", proposal)
        receipt = record_candidate_review_receipt(campaign)
        self.assertNotEqual(receipt.resume_capsule.next_action, "await_independent_review")
        with self.assertRaises(IndependentReviewError):
            record_independent_review_decision(campaign, decision="candidate_quarantined", reviewer_id="r", attestation="checked")

    def test_direct_keep_follow_up_without_gate_fails_closed(self):
        with self.assertRaises(CampaignError):
            append_campaign_event(
                campaign_root=self.campaign_root,
                event_type="candidate_kept",
                payload={"candidate_id": "C-001", "reason": "manual-bypass"},
            )

    def test_generic_campaign_record_parser_excludes_independent_decisions(self):
        parser = build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(
                [
                    "campaign-record",
                    "--campaign-root",
                    str(self.campaign_root),
                    "--event-type",
                    "candidate_kept",
                ]
            )

    def test_decision_artifact_binds_reviewer_and_all_evidence(self):
        result = self._record()
        artifact = result.decision
        self.assertEqual(artifact.reviewer_role, "independent_reviewer")
        self.assertEqual(artifact.verified_attempts, 3)
        self.assertEqual(artifact.verified_evidence_files, 18)
        self.assertEqual(artifact.frozen_parent["commit"], "bd8c4224ca0fb708ebe3c6dd000491f2f03da4fe")
        self.assertEqual(artifact.candidate_reviewed_event_sha256, self.receipt.receipt.candidate_reviewed_event_sha256)


if __name__ == "__main__":
    unittest.main()
