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
from planning_lite.campaign.campaign_completion import (
    CampaignCompletionError,
    load_campaign_completion_seal,
    load_release_handoff,
    record_campaign_completion,
)
from planning_lite.campaign.candidate_review import review_campaign_candidate, write_candidate_review
from planning_lite.campaign.cli import build_parser, main
from planning_lite.campaign.independent_review import record_independent_review_decision
from planning_lite.campaign.review_receipt import record_candidate_review_receipt


class CampaignCompletionSealTests(unittest.TestCase):
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
                    "campaign_id": "campaign-completion-test",
                    "purpose": "Test campaign completion seal and release handoff.",
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
            payload={"hypothesis_id": "H-001", "summary": "Completion hypothesis"},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_registered",
            payload={
                "hypothesis_id": "H-001",
                "candidate_id": "C-001",
                "summary": "Completion candidate",
            },
        )
        for index in range(1, 4):
            self._attempt(index)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "keep")
        write_candidate_review(self.campaign_root / "candidate-review.json", proposal)
        self.receipt = record_candidate_review_receipt(self.campaign_root)
        self.independent = record_independent_review_decision(
            self.campaign_root,
            decision="candidate_kept",
            reviewer_id="reviewer-001",
            attestation="I independently verified the sealed artifact chain and evidence hashes.",
        )
        self.assertEqual(self.independent.next_action, "record_campaign_completed")

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
                json.dumps({"suite_id": suite_id, "artifact": name, "index": index}, sort_keys=True)
                + "\n",
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
            payload={"candidate_id": "C-001", "attempt_id": attempt_id, "suite": identity},
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

    def _complete(self):
        return record_campaign_completion(self.campaign_root)

    def test_completion_appends_terminal_event_without_release(self):
        before = len(load_campaign_journal(self.campaign_root))
        result = self._complete()
        events = load_campaign_journal(self.campaign_root)
        self.assertEqual(result.status, "recorded")
        self.assertTrue(result.journal_appended)
        self.assertEqual(len(events), before + 1)
        self.assertEqual(events[-1].event_type, "campaign_completed")
        self.assertEqual(result.resume_capsule.campaign_status, "completed")
        self.assertEqual(result.resume_capsule.next_action, "none")
        self.assertEqual(result.release_handoff.release_status, "not_requested")
        self.assertFalse(result.release_handoff.central_planning_lite_mutated)
        self.assertIn("release_gate_not_executed", result.release_handoff.restrictions)

    def test_completion_seal_binds_budget_decision_and_release_handoff(self):
        result = self._complete()
        seal = load_campaign_completion_seal(result.seal_path)
        handoff = load_release_handoff(result.release_handoff_path)
        self.assertEqual(seal.independent_decision_sha256, self.independent.decision.decision_sha256)
        self.assertEqual(seal.independent_decision_event_sha256, self.independent.decision_event.event_sha256)
        self.assertEqual(seal.verified_attempts, 3)
        self.assertEqual(seal.verified_evidence_files, 18)
        self.assertEqual(seal.attempts_started, 3)
        self.assertEqual(seal.attempts_completed, 3)
        self.assertEqual(seal.release_handoff_sha256, handoff.release_handoff_sha256)
        self.assertEqual(seal.evidence_bundle_sha256, handoff.evidence_bundle_sha256)
        self.assertEqual(seal.expected_terminal_event, "campaign_completed")

    def test_release_handoff_is_bounded_and_requires_later_release_gate(self):
        result = self._complete()
        handoff = result.release_handoff
        self.assertTrue(handoff.accepted_candidate)
        self.assertEqual(handoff.next_action, "await_release_gate")
        self.assertEqual(handoff.required_role, "release_reviewer")
        self.assertIn("verify_release_handoff", handoff.permitted_follow_up_actions)
        self.assertIn("promotion_not_authorized", handoff.restrictions)
        self.assertIn("central_planning_lite_mutation_not_authorized", handoff.restrictions)

    def test_replay_is_idempotent(self):
        first = self._complete()
        journal = (self.campaign_root / "campaign-journal.jsonl").read_bytes()
        seal = first.seal_path.read_bytes()
        handoff = first.release_handoff_path.read_bytes()
        second = self._complete()
        self.assertEqual(second.status, "already-recorded")
        self.assertFalse(second.journal_appended)
        self.assertEqual(journal, (self.campaign_root / "campaign-journal.jsonl").read_bytes())
        self.assertEqual(seal, second.seal_path.read_bytes())
        self.assertEqual(handoff, second.release_handoff_path.read_bytes())
        self.assertEqual(first.seal.completion_seal_sha256, second.seal.completion_seal_sha256)
        self.assertEqual(
            first.release_handoff.release_handoff_sha256,
            second.release_handoff.release_handoff_sha256,
        )

    def test_tampered_decision_fails_closed_before_completion(self):
        payload = json.loads(self.independent.decision_path.read_text(encoding="utf-8"))
        payload["attestation"] = "tampered"
        self.independent.decision_path.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaises(CampaignCompletionError):
            self._complete()

    def test_tampered_suite_evidence_fails_closed_before_completion(self):
        suite_root = Path(self.receipt.handoff.attempts[0]["suite_root"])
        (suite_root / "suite-report.json").write_text("tampered\n", encoding="utf-8")
        with self.assertRaises(CampaignCompletionError):
            self._complete()

    def test_tampered_review_receipt_or_handoff_fails_closed(self):
        for path in (
            self.campaign_root / "candidate-review.json",
            self.receipt.receipt_path,
            self.receipt.handoff_path,
        ):
            original = path.read_bytes()
            payload = json.loads(original.decode("utf-8"))
            payload["tamper"] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(Exception):
                self._complete()
            path.write_bytes(original)

    def test_tampered_completion_artifacts_fail_closed_on_replay(self):
        result = self._complete()
        for path in (result.seal_path, result.release_handoff_path):
            original = path.read_bytes()
            payload = json.loads(original.decode("utf-8"))
            payload["tamper"] = True
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(CampaignCompletionError):
                self._complete()
            path.write_bytes(original)

    def test_cli_campaign_complete_does_not_require_eval_fixture(self):
        code = main([
            "campaign-complete",
            "--campaign-root",
            str(self.campaign_root),
        ])
        self.assertEqual(code, 0)
        capsule = inspect_campaign(self.campaign_root)
        self.assertEqual(capsule.campaign_status, "completed")

    def test_generic_campaign_record_parser_excludes_campaign_completed(self):
        parser = build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(
                [
                    "campaign-record",
                    "--campaign-root",
                    str(self.campaign_root),
                    "--event-type",
                    "campaign_completed",
                ]
            )

    def test_direct_campaign_completed_bypass_fails_closed(self):
        with self.assertRaises(CampaignError):
            append_campaign_event(
                campaign_root=self.campaign_root,
                event_type="campaign_completed",
                payload={"candidate_id": "C-001", "reason": "manual-bypass"},
            )

    def test_replay_with_different_output_paths_fails_closed(self):
        self._complete()
        with self.assertRaises(CampaignCompletionError):
            record_campaign_completion(
                self.campaign_root,
                seal_path=self.root / "different-seal.json",
            )
        with self.assertRaises(CampaignCompletionError):
            record_campaign_completion(
                self.campaign_root,
                release_handoff_path=self.root / "different-handoff.json",
            )

    def test_campaign_status_is_terminal_after_completion(self):
        self._complete()
        capsule = inspect_campaign(self.campaign_root)
        self.assertEqual(capsule.last_event_type, "campaign_completed")
        self.assertEqual(capsule.campaign_status, "completed")
        self.assertIn("campaign_completed", capsule.stop_reasons)
        self.assertIn("accepted_candidate", capsule.stop_reasons)
        self.assertEqual(capsule.next_action, "none")


if __name__ == "__main__":
    unittest.main()
