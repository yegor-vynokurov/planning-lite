from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from planning_lite.campaign.campaign import (
    append_campaign_event,
    initialize_campaign,
    load_manifest_template,
)
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "planning_lite_campaign.py"


from planning_lite.campaign.candidate_review import (
    CandidateReviewError,
    review_campaign_candidate,
    write_candidate_review,
)


class CandidateReviewGateTests(unittest.TestCase):
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
                    "campaign_id": "candidate-review-test",
                    "purpose": "Test deterministic candidate review proposals.",
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
            payload={"hypothesis_id": "H-001", "summary": "Review gate hypothesis"},
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_registered",
            payload={
                "hypothesis_id": "H-001",
                "candidate_id": "C-001",
                "summary": "Review gate candidate",
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
        suite_id: str | None = None,
        suite_root: str | None = None,
        eval_id: str = "lifecycle-status",
        source_commit: str = "abc123",
        include_evidence: bool = True,
        improved_override: bool | None = None,
        evidence_seed: int | None = None,
    ) -> None:
        attempt_id = f"A-{index:03d}"
        resolved_suite_id = suite_id or f"suite-{index:03d}"
        resolved_suite_root = suite_root or str(self.root / "suites" / resolved_suite_id)
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "suite": {
                    "suite_id": resolved_suite_id,
                    "suite_root": resolved_suite_root,
                    "eval_id": eval_id,
                    "source_commit": source_commit,
                    "plan_sha256": f"{index:x}".rjust(64, "0"),
                },
            },
        )
        evidence = (
            {
                name: hashlib.sha256(
                    f"{evidence_seed if evidence_seed is not None else index}:{name}".encode("utf-8")
                ).hexdigest()
                for name in (
                    "suite-plan.json",
                    "suite-state.json",
                    "suite-result.json",
                    "suite-aggregation.json",
                    "suite-report.json",
                    "suite-verdict.json",
                )
            }
            if include_evidence
            else {}
        )
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": attempt_id,
                "hard_gate_passed": hard_gate_passed,
                "improved": (
                    improved_override
                    if improved_override is not None
                    else verdict_status
                    in {"promote-for-fixture", "promote-routing-policy"}
                ),
                "metrics": {"total_tokens": 100 + index, "duration_seconds": 1.0},
                "suite": {
                    "suite_id": resolved_suite_id,
                    "suite_root": resolved_suite_root,
                    "eval_id": eval_id,
                    "source_commit": source_commit,
                    "plan_sha256": f"{index:x}".rjust(64, "0"),
                    "verdict_status": verdict_status,
                    "recommended_arm": recommended_arm,
                    "evidence_sha256": evidence,
                },
            },
        )

    def test_three_consistent_positive_attempts_propose_keep_for_review(self):
        for index in range(1, 4):
            self._attempt(index)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "keep")
        self.assertEqual(proposal.operational_meaning, "keep-for-independent-review")
        self.assertEqual(proposal.promotion_status, "not_requested")
        self.assertEqual(proposal.observed_attempts, 3)
        self.assertEqual(proposal.independent_attempts, 3)
        self.assertIn("keep_is_not_promotion", proposal.reason_codes)
        self.assertRegex(proposal.review_sha256, r"^[0-9a-f]{64}$")

    def test_two_attempts_propose_continue(self):
        self._attempt(1)
        self._attempt(2)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        self.assertIn("completed_attempts=2/3", proposal.reason_codes)

    def test_any_hard_gate_failure_proposes_reject_immediately(self):
        self._attempt(1, hard_gate_passed=False, verdict_status="reject-candidates", recommended_arm=None)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "reject")
        self.assertIn("hard_gate_failure", proposal.reason_codes)

    def test_three_conclusive_negative_attempts_propose_reject(self):
        for index in range(1, 4):
            self._attempt(index, verdict_status="retain-baseline", recommended_arm="raw-docs")
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "reject")
        self.assertIn("three_conclusive_negative_verdicts", proposal.reason_codes)

    def test_mixed_positive_and_negative_attempts_propose_continue(self):
        self._attempt(1)
        self._attempt(2, verdict_status="retain-baseline", recommended_arm="raw-docs")
        self._attempt(3)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        self.assertIn("positive_negative_verdict_conflict", proposal.reason_codes)

    def test_inconsistent_positive_recommended_arm_proposes_continue(self):
        self._attempt(1, recommended_arm="snapshot")
        self._attempt(2, recommended_arm="snapshot-skill")
        self._attempt(3, recommended_arm="snapshot")
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        self.assertIn("recommended_arm_inconsistent", proposal.reason_codes)

    def test_duplicate_suite_identity_is_not_independent(self):
        duplicate_root = str(self.root / "suites" / "duplicate")
        self._attempt(1, suite_id="duplicate", suite_root=duplicate_root)
        self._attempt(2, suite_id="duplicate", suite_root=duplicate_root)
        self._attempt(3)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        self.assertLess(proposal.independent_attempts, 3)
        self.assertIn("duplicate_suite_id", proposal.reason_codes)
        self.assertIn("duplicate_suite_root", proposal.reason_codes)

    def test_copied_evidence_is_not_an_independent_attempt(self):
        self._attempt(1, evidence_seed=1)
        self._attempt(2, evidence_seed=1)
        self._attempt(3, evidence_seed=3)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        self.assertIn("duplicate_evidence_fingerprint", proposal.reason_codes)

    def test_missing_sealed_evidence_proposes_continue(self):
        self._attempt(1)
        self._attempt(2, include_evidence=False)
        self._attempt(3)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        self.assertTrue(any("missing_evidence" in item for item in proposal.reason_codes))

    def test_improved_flag_must_match_suite_verdict(self):
        self._attempt(1)
        self._attempt(2, improved_override=False)
        self._attempt(3)
        proposal = review_campaign_candidate(self.campaign_root)
        self.assertEqual(proposal.decision, "continue")
        self.assertTrue(
            any("improved_flag_verdict_mismatch" in item for item in proposal.reason_codes)
        )

    def test_review_artifact_is_deterministic_and_replace_guarded(self):
        for index in range(1, 4):
            self._attempt(index)
        proposal = review_campaign_candidate(self.campaign_root)
        output = self.root / "candidate-review.json"
        write_candidate_review(output, proposal)
        before = output.read_bytes()
        write_candidate_review(output, proposal)
        self.assertEqual(before, output.read_bytes())

        payload = json.loads(output.read_text(encoding="utf-8"))
        payload["summary"] = "tampered"
        output.write_text(json.dumps(payload), encoding="utf-8")
        with self.assertRaisesRegex(CandidateReviewError, "different content"):
            write_candidate_review(output, proposal)
        write_candidate_review(output, proposal, replace=True)
        self.assertEqual(json.loads(output.read_text(encoding="utf-8"))["review_sha256"], proposal.review_sha256)

    def test_already_decided_candidate_cannot_be_reviewed_again(self):
        self._attempt(1)
        append_campaign_event(
            campaign_root=self.campaign_root,
            event_type="candidate_rejected",
            payload={"candidate_id": "C-001", "reason": "manual review"},
        )
        with self.assertRaisesRegex(CandidateReviewError, "already has terminal review"):
            review_campaign_candidate(self.campaign_root, candidate_id="C-001")

    def test_cli_review_does_not_require_eval_fixture_and_writes_artifact(self):
        for index in range(1, 4):
            self._attempt(index)
        output = self.root / "cli-review.json"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "campaign-review",
                "--campaign-root",
                str(self.campaign_root),
                "--output",
                str(output),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
        payload = json.loads(result.stdout)
        self.assertEqual(payload["status"], "reviewed")
        self.assertEqual(payload["decision"], "keep")
        self.assertEqual(payload["promotion_status"], "not_requested")
        self.assertTrue(output.is_file())


if __name__ == "__main__":
    unittest.main()
