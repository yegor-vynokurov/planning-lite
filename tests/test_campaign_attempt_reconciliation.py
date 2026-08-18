from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from planning_lite.campaign.attempt_reconciliation import (
    AttemptEvidenceReconciliationError,
    reconcile_completed_attempt_suite_evidence,
)
from planning_lite.campaign.campaign import (
    append_campaign_event,
    initialize_campaign,
    inspect_campaign,
    load_campaign_journal,
    load_manifest_template,
)
from planning_lite.campaign.candidate_review import review_campaign_candidate


class CampaignAttemptReconciliationTests(unittest.TestCase):
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
                    "campaign_id": "reconciliation-test",
                    "purpose": "Test append-only historical suite reconciliation.",
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
                        "max_total_tokens": 1000000,
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
            payload={"hypothesis_id": "H-001", "summary": "hypothesis"},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_registered",
            payload={"hypothesis_id": "H-001", "candidate_id": "C-001", "summary": "candidate"},
        )

    def tearDown(self):
        self.temp.cleanup()

    def _suite(self, name: str, seed: int) -> Path:
        root = self.root / "suites" / name
        root.mkdir(parents=True)
        plan = {
            "schema_version": 1,
            "suite_id": name,
            "eval_id": "lifecycle-status",
            "source_commit": "e5c30acd325bc6a5b28a94c404349c53cb47a674",
            "plan_sha256": f"{seed:x}".rjust(64, "0"),
        }
        state = {
            "schema_version": 1,
            "suite_id": name,
            "eval_id": "lifecycle-status",
            "status": "completed",
            "runs": [{"run_id": f"{name}-{i}", "status": "passed"} for i in range(9)],
        }
        verdict = {"status": "promote-for-fixture", "recommended_arm": "snapshot"}
        for filename, value in {
            "suite-plan.json": plan,
            "suite-state.json": state,
            "suite-result.json": {"status": "completed"},
            "suite-aggregation.json": {"arms": {}},
            "suite-report.json": {"status": "completed"},
            "suite-verdict.json": verdict,
        }.items():
            (root / filename).write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
        return root

    @staticmethod
    def _start_suite_payload(suite: Path) -> dict[str, str]:
        plan = json.loads((suite / "suite-plan.json").read_text(encoding="utf-8"))
        return {
            "suite_id": plan["suite_id"],
            "eval_id": plan["eval_id"],
            "source_commit": plan["source_commit"],
            "suite_root": str(suite.resolve()),
            "plan_sha256": plan["plan_sha256"],
        }

    def _legacy_attempt_and_review(self) -> tuple[object, Path]:
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={"candidate_id": "C-001", "attempt_id": "A-001"},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "hard_gate_passed": True,
                "improved": True,
                "metrics": {"total_tokens": 100, "duration_seconds": 1.0},
            },
        )
        events = load_campaign_journal(self.campaign_root)
        completion = events[-1]
        proposal = review_campaign_candidate(self.campaign_root, candidate_id="C-001")
        self.assertEqual(proposal.independent_attempts, 0)
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_reviewed",
            payload={
                "candidate_id": "C-001",
                "hypothesis_id": "H-001",
                "decision": "continue",
                "operational_meaning": "collect-or-reconcile-evidence",
                "promotion_status": "not_requested",
                "next_action": "start_next_independent_attempt",
                "review_path": str(self.root / "review.json"),
                "review_sha256": proposal.review_sha256,
                "review_journal_head_sha256": completion.event_sha256,
                "handoff_path": str(self.root / "handoff.json"),
                "handoff_sha256": "a" * 64,
                "receipt_path": str(self.root / "receipt.json"),
            },
        )
        return completion, self._suite("suite-a01", 1)

    def test_reconciliation_is_append_only_and_preserves_accounting(self):
        completion, suite = self._legacy_attempt_and_review()
        before = inspect_campaign(self.campaign_root, write_capsule=False)
        result = reconcile_completed_attempt_suite_evidence(
            campaign_root=self.campaign_root,
            candidate_id="C-001",
            attempt_id="A-001",
            suite_root=suite,
            expected_source_event_sha256=completion.event_sha256,
        )
        events = load_campaign_journal(self.campaign_root)
        self.assertEqual(events[-1].event_type, "attempt_evidence_reconciled")
        self.assertEqual(events[-1].payload["source_attempt_completed_event_sha256"], completion.event_sha256)
        self.assertEqual(result.attempts_started, before.attempts_started)
        self.assertEqual(result.attempts_completed, before.attempts_completed)
        self.assertEqual(result.total_tokens, before.total_tokens)
        self.assertEqual(result.wall_clock_seconds, before.wall_clock_seconds)
        self.assertEqual(result.next_action, "start_next_independent_attempt")
        proposal = review_campaign_candidate(self.campaign_root, candidate_id="C-001")
        self.assertEqual(proposal.observed_attempts, 1)
        self.assertEqual(proposal.independent_attempts, 1)
        self.assertEqual(proposal.attempts[0].suite_id, "suite-a01")
        self.assertEqual(len(proposal.attempts[0].evidence_sha256), 6)

    def test_reconciliation_matches_historical_start_suite_identity_when_present(self):
        suite = self._suite("suite-a01-start-bound", 7)
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "suite": self._start_suite_payload(suite),
            },
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001", "attempt_id": "A-001",
                "hard_gate_passed": True, "improved": True,
                "metrics": {"total_tokens": 100, "duration_seconds": 1.0},
            },
        )
        completion = load_campaign_journal(self.campaign_root)[-1]
        proposal = review_campaign_candidate(self.campaign_root, candidate_id="C-001")
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_reviewed",
            payload={
                "candidate_id": "C-001", "hypothesis_id": "H-001",
                "decision": "continue", "operational_meaning": "collect-or-reconcile-evidence",
                "promotion_status": "not_requested", "next_action": "start_next_independent_attempt",
                "review_path": str(self.root / "review-start-bound.json"),
                "review_sha256": proposal.review_sha256,
                "review_journal_head_sha256": completion.event_sha256,
                "handoff_path": str(self.root / "handoff-start-bound.json"),
                "handoff_sha256": "a" * 64,
                "receipt_path": str(self.root / "receipt-start-bound.json"),
            },
        )
        result = reconcile_completed_attempt_suite_evidence(
            campaign_root=self.campaign_root,
            candidate_id="C-001", attempt_id="A-001", suite_root=suite,
            expected_source_event_sha256=completion.event_sha256,
        )
        self.assertEqual(result.last_event_type, "attempt_evidence_reconciled")
        reconciled = load_campaign_journal(self.campaign_root)[-1]
        self.assertEqual(reconciled.payload["suite"]["plan_sha256"], "7".rjust(64, "0"))

    def test_reconciliation_rejects_suite_identity_drift_from_historical_start(self):
        suite = self._suite("suite-a01-start-drift", 8)
        start_suite = self._start_suite_payload(suite)
        start_suite["plan_sha256"] = "9".rjust(64, "0")
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={"candidate_id": "C-001", "attempt_id": "A-001", "suite": start_suite},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001", "attempt_id": "A-001",
                "hard_gate_passed": True, "improved": True,
                "metrics": {"total_tokens": 100, "duration_seconds": 1.0},
            },
        )
        completion = load_campaign_journal(self.campaign_root)[-1]
        proposal = review_campaign_candidate(self.campaign_root, candidate_id="C-001")
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_reviewed",
            payload={
                "candidate_id": "C-001", "hypothesis_id": "H-001",
                "decision": "continue", "operational_meaning": "collect-or-reconcile-evidence",
                "promotion_status": "not_requested", "next_action": "start_next_independent_attempt",
                "review_path": str(self.root / "review-start-drift.json"),
                "review_sha256": proposal.review_sha256,
                "review_journal_head_sha256": completion.event_sha256,
                "handoff_path": str(self.root / "handoff-start-drift.json"),
                "handoff_sha256": "a" * 64,
                "receipt_path": str(self.root / "receipt-start-drift.json"),
            },
        )
        with self.assertRaisesRegex(AttemptEvidenceReconciliationError, "plan_sha256.*attempt_started"):
            reconcile_completed_attempt_suite_evidence(
                campaign_root=self.campaign_root,
                candidate_id="C-001", attempt_id="A-001", suite_root=suite,
                expected_source_event_sha256=completion.event_sha256,
            )

    def test_reconciliation_rejects_native_suite_completion(self):
        suite = self._suite("suite-native", 2)
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={"candidate_id": "C-001", "attempt_id": "A-001", "suite": {
                "suite_id": "suite-native", "eval_id": "lifecycle-status",
                "source_commit": "e5c30acd325bc6a5b28a94c404349c53cb47a674",
                "suite_root": str(suite), "plan_sha256": "2".rjust(64, "0")}},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001", "attempt_id": "A-001",
                "hard_gate_passed": True, "improved": True,
                "metrics": {"total_tokens": 100, "duration_seconds": 1.0},
                "suite": {"suite_id": "suite-native"},
            },
        )
        with self.assertRaisesRegex(AttemptEvidenceReconciliationError, "already has native"):
            reconcile_completed_attempt_suite_evidence(
                campaign_root=self.campaign_root,
                candidate_id="C-001", attempt_id="A-001", suite_root=suite,
            )

    def test_reconciliation_is_idempotent_for_exact_same_evidence(self):
        completion, suite = self._legacy_attempt_and_review()
        first = reconcile_completed_attempt_suite_evidence(
            campaign_root=self.campaign_root, candidate_id="C-001", attempt_id="A-001",
            suite_root=suite, expected_source_event_sha256=completion.event_sha256,
        )
        count = len(load_campaign_journal(self.campaign_root))
        second = reconcile_completed_attempt_suite_evidence(
            campaign_root=self.campaign_root, candidate_id="C-001", attempt_id="A-001",
            suite_root=suite, expected_source_event_sha256=completion.event_sha256,
        )
        self.assertEqual(len(load_campaign_journal(self.campaign_root)), count)
        self.assertEqual(first.journal_head_sha256, second.journal_head_sha256)

    def test_reconciled_a01_plus_native_a02_yields_two_independent_attempts(self):
        completion, suite1 = self._legacy_attempt_and_review()
        reconcile_completed_attempt_suite_evidence(
            campaign_root=self.campaign_root, candidate_id="C-001", attempt_id="A-001",
            suite_root=suite1, expected_source_event_sha256=completion.event_sha256,
        )
        suite2 = self._suite("suite-a02", 2)
        evidence2 = {name: hashlib.sha256((suite2 / name).read_bytes()).hexdigest() for name in (
            "suite-plan.json", "suite-state.json", "suite-result.json",
            "suite-aggregation.json", "suite-report.json", "suite-verdict.json",
        )}
        append_campaign_event(
            campaign_root=self.campaign_root, event_type="attempt_started",
            payload={"candidate_id":"C-001","attempt_id":"A-002","suite":{
                "suite_id":"suite-a02","eval_id":"lifecycle-status",
                "source_commit":"e5c30acd325bc6a5b28a94c404349c53cb47a674",
                "suite_root":str(suite2),"plan_sha256":"2".rjust(64,"0")}},
        )
        append_campaign_event(
            campaign_root=self.campaign_root, event_type="attempt_completed",
            payload={"candidate_id":"C-001","attempt_id":"A-002","hard_gate_passed":True,"improved":True,
                "metrics":{"total_tokens":200,"duration_seconds":2.0},
                "suite":{"suite_id":"suite-a02","eval_id":"lifecycle-status",
                    "source_commit":"e5c30acd325bc6a5b28a94c404349c53cb47a674",
                    "suite_root":str(suite2),"plan_sha256":"2".rjust(64,"0"),
                    "suite_status":"completed","total_runs":9,"terminal_runs":9,"passed_runs":9,"failed_runs":0,"error_runs":0,
                    "verdict_status":"promote-for-fixture","recommended_arm":"snapshot","evidence_sha256":evidence2}},
        )
        proposal = review_campaign_candidate(self.campaign_root, candidate_id="C-001")
        self.assertEqual(proposal.observed_attempts, 2)
        self.assertEqual(proposal.independent_attempts, 2)
        self.assertIn("completed_attempts=2/3", proposal.reason_codes)
        self.assertEqual({x.suite_id for x in proposal.attempts}, {"suite-a01", "suite-a02"})


if __name__ == "__main__":
    unittest.main()
