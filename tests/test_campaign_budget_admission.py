from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from planning_lite.campaign.campaign import (
    AttemptBudgetReservation,
    CampaignError,
    append_campaign_event,
    initialize_campaign,
    load_campaign_journal,
    load_manifest_template,
    prepare_attempt_budget_admission,
)


class CampaignBudgetAdmissionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.frozen = self.root / "frozen.txt"
        self.frozen.write_text("frozen\n", encoding="utf-8")
        self.frozen_sha = hashlib.sha256(self.frozen.read_bytes()).hexdigest()

    def tearDown(self):
        self.temp.cleanup()

    def _campaign(self, *, strict: bool, max_tokens: int = 1000, max_wall: float = 120.0) -> Path:
        payload = {
            "schema_version": 1,
            "campaign_id": f"budget-admission-{'strict' if strict else 'legacy'}",
            "purpose": "Test attempt budget admission semantics.",
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
                    "sha256": self.frozen_sha,
                }
            ],
            "mutable_scope": ["src/planning_lite/campaign/**"],
            "off_limits": ["template/**"],
            "budget": {
                "max_candidates": 1,
                "max_attempts_per_candidate": 3,
                "max_total_attempts": 3,
                "max_total_tokens": max_tokens,
                "max_wall_clock_seconds": max_wall,
            },
            "stop_policy": {
                "stop_on_hard_gate_failure": True,
                "stop_after_accepted_candidate": True,
                "max_consecutive_non_improving": 3,
            },
        }
        if strict:
            payload["attempt_budget_admission"] = {"required": True}
        manifest_path = self.root / f"manifest-{'strict' if strict else 'legacy'}.json"
        manifest_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        campaign = self.root / f"campaign-{'strict' if strict else 'legacy'}"
        initialize_campaign(
            campaign_root=campaign,
            manifest=load_manifest_template(manifest_path),
            inputs_root=self.root,
        )
        append_campaign_event(
            campaign_root=campaign,
            event_type="hypothesis_registered",
            payload={"hypothesis_id": "H-001"},
        )
        append_campaign_event(
            campaign_root=campaign,
            event_type="candidate_registered",
            payload={"candidate_id": "C-001", "hypothesis_id": "H-001"},
        )
        return campaign

    def test_strict_manifest_requires_budget_admission(self):
        campaign = self._campaign(strict=True)
        with self.assertRaisesRegex(CampaignError, "requires an exact budget_admission"):
            append_campaign_event(
                campaign_root=campaign,
                event_type="attempt_started",
                payload={"candidate_id": "C-001", "attempt_id": "A-001"},
            )
        self.assertEqual(len(load_campaign_journal(campaign)), 3)

    def test_legacy_manifest_remains_backward_compatible(self):
        campaign = self._campaign(strict=False)
        capsule = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_started",
            payload={"candidate_id": "C-001", "attempt_id": "A-001"},
        )
        self.assertEqual(capsule.attempts_started, 1)
        self.assertEqual(capsule.next_action, "recover_or_complete_attempt")

    def test_admission_is_bound_to_remaining_budget_and_journal_head(self):
        campaign = self._campaign(strict=True)
        admission = prepare_attempt_budget_admission(
            campaign_root=campaign,
            candidate_id="C-001",
            attempt_id="A-001",
            reservation=AttemptBudgetReservation(
                total_tokens=600,
                wall_clock_seconds=60.0,
                basis="historical-upper-bound-v1",
            ),
        )
        before = load_campaign_journal(campaign)
        self.assertEqual(admission["journal_head_sha256"], before[-1].event_sha256)
        self.assertEqual(admission["remaining_before"]["total_tokens"], 1000)
        capsule = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "budget_admission": admission,
            },
        )
        self.assertEqual(capsule.attempts_started, 1)
        self.assertEqual(capsule.remaining_budget["tokens"], 400)
        self.assertEqual(capsule.remaining_budget["wall_clock_seconds"], 60.0)

    def test_admission_rejects_token_reservation_above_remaining(self):
        campaign = self._campaign(strict=True)
        with self.assertRaisesRegex(CampaignError, "need=1001, remaining=1000"):
            prepare_attempt_budget_admission(
                campaign_root=campaign,
                candidate_id="C-001",
                attempt_id="A-001",
                reservation=AttemptBudgetReservation(
                    total_tokens=1001,
                    wall_clock_seconds=60.0,
                    basis="too-large",
                ),
            )
        self.assertEqual(len(load_campaign_journal(campaign)), 3)

    def test_admission_rejects_wall_clock_reservation_above_remaining(self):
        campaign = self._campaign(strict=True)
        with self.assertRaisesRegex(CampaignError, "wall-clock reservation exceeds"):
            prepare_attempt_budget_admission(
                campaign_root=campaign,
                candidate_id="C-001",
                attempt_id="A-001",
                reservation=AttemptBudgetReservation(
                    total_tokens=600,
                    wall_clock_seconds=121.0,
                    basis="too-long",
                ),
            )

    def test_tampered_admission_fails_closed(self):
        campaign = self._campaign(strict=True)
        admission = prepare_attempt_budget_admission(
            campaign_root=campaign,
            candidate_id="C-001",
            attempt_id="A-001",
            reservation=AttemptBudgetReservation(
                total_tokens=600,
                wall_clock_seconds=60.0,
                basis="tamper-test",
            ),
        )
        admission["reservation"]["total_tokens"] = 599
        with self.assertRaisesRegex(CampaignError, "identity does not match"):
            append_campaign_event(
                campaign_root=campaign,
                event_type="attempt_started",
                payload={
                    "candidate_id": "C-001",
                    "attempt_id": "A-001",
                    "budget_admission": admission,
                },
            )

    def test_completion_releases_unused_open_reservation(self):
        campaign = self._campaign(strict=True, max_tokens=1000)
        admission = prepare_attempt_budget_admission(
            campaign_root=campaign,
            candidate_id="C-001",
            attempt_id="A-001",
            reservation=AttemptBudgetReservation(
                total_tokens=900,
                wall_clock_seconds=60.0,
                basis="release-test",
            ),
        )
        started = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "budget_admission": admission,
            },
        )
        self.assertEqual(started.remaining_budget["tokens"], 100)
        completed = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "hard_gate_passed": True,
                "improved": True,
                "metrics": {"total_tokens": 500, "duration_seconds": 30.0},
            },
        )
        self.assertEqual(completed.remaining_budget["tokens"], 500)
        self.assertEqual(completed.remaining_budget["wall_clock_seconds"], 90.0)
        self.assertEqual(completed.campaign_status, "running")

    def test_truthful_completion_can_exceed_reservation_and_then_requires_stop(self):
        campaign = self._campaign(strict=True, max_tokens=1000)
        admission = prepare_attempt_budget_admission(
            campaign_root=campaign,
            candidate_id="C-001",
            attempt_id="A-001",
            reservation=AttemptBudgetReservation(
                total_tokens=900,
                wall_clock_seconds=60.0,
                basis="bounded-estimate-v1",
            ),
        )
        append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_started",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "budget_admission": admission,
            },
        )
        capsule = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "hard_gate_passed": True,
                "improved": True,
                "metrics": {"total_tokens": 1100, "duration_seconds": 61.0},
            },
        )
        self.assertEqual(capsule.attempts_completed, 1)
        self.assertEqual(capsule.total_tokens, 1100)
        self.assertEqual(capsule.remaining_budget["tokens"], 0)
        self.assertEqual(capsule.campaign_status, "stop-required")
        self.assertIn("token_budget_overrun", capsule.stop_reasons)
        self.assertEqual(capsule.next_action, "record_campaign_stopped")


if __name__ == "__main__":
    unittest.main()
