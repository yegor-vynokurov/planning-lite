from __future__ import annotations

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


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "planning_lite_campaign.py"


class CampaignCoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.input = self.root / "frozen.txt"
        self.input.write_text("frozen\n", encoding="utf-8")
        import hashlib

        self.input_sha = hashlib.sha256(self.input.read_bytes()).hexdigest()
        self.manifest_path = self.root / "manifest.json"
        self.manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "campaign_id": "chg-e1-test",
                    "purpose": "Prove deterministic campaign state.",
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
                            "sha256": self.input_sha,
                        }
                    ],
                    "mutable_scope": ["src/planning_lite/campaign/campaign.py"],
                    "off_limits": ["template/**", "evals/**"],
                    "budget": {
                        "max_candidates": 2,
                        "max_attempts_per_candidate": 2,
                        "max_total_attempts": 3,
                        "max_total_tokens": 1000,
                        "max_wall_clock_seconds": 120.0,
                    },
                    "stop_policy": {
                        "stop_on_hard_gate_failure": True,
                        "stop_after_accepted_candidate": True,
                        "max_consecutive_non_improving": 2,
                    },
                },
                indent=2,
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.temp.cleanup()

    def _init(self) -> Path:
        campaign = self.root / "campaign"
        manifest = load_manifest_template(self.manifest_path)
        capsule = initialize_campaign(
            campaign_root=campaign,
            manifest=manifest,
            inputs_root=self.root,
        )
        self.assertEqual(capsule.next_action, "register_hypothesis")
        return campaign

    def _register_candidate(
        self,
        campaign: Path,
        *,
        hypothesis_id: str = "H-001",
        candidate_id: str = "C-001",
        register_hypothesis: bool = True,
    ) -> None:
        if register_hypothesis:
            append_campaign_event(
                campaign_root=campaign,
                event_type="hypothesis_registered",
                payload={"hypothesis_id": hypothesis_id},
            )
        append_campaign_event(
            campaign_root=campaign,
            event_type="candidate_registered",
            payload={
                "candidate_id": candidate_id,
                "hypothesis_id": hypothesis_id,
            },
        )

    def _complete_attempt(
        self,
        campaign: Path,
        *,
        candidate_id: str = "C-001",
        attempt_id: str = "A-001",
        hard_gate_passed: bool = True,
        improved: bool = True,
    ) -> None:
        append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_started",
            payload={"candidate_id": candidate_id, "attempt_id": attempt_id},
        )
        append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_completed",
            payload={
                "candidate_id": candidate_id,
                "attempt_id": attempt_id,
                "hard_gate_passed": hard_gate_passed,
                "improved": improved,
                "metrics": {},
            },
        )

    def test_initialization_pins_manifest_and_creates_hash_linked_journal(self):
        campaign = self._init()
        manifest = json.loads((campaign / "campaign-manifest.json").read_text())
        self.assertEqual(len(manifest["manifest_sha256"]), 64)
        events = load_campaign_journal(campaign)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0].event_type, "campaign_initialized")
        self.assertIsNone(events[0].previous_event_sha256)
        capsule = inspect_campaign(campaign)
        self.assertEqual(capsule.journal_head_sha256, events[0].event_sha256)

    def test_attempt_events_update_budget_and_resume_action(self):
        campaign = self._init()
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
        started = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_started",
            payload={"candidate_id": "C-001", "attempt_id": "A-001"},
        )
        self.assertEqual(started.next_action, "recover_or_complete_attempt")
        completed = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "hard_gate_passed": True,
                "improved": True,
                "metrics": {"total_tokens": 250, "duration_seconds": 12.5},
            },
        )
        self.assertEqual(completed.attempts_started, 1)
        self.assertEqual(completed.attempts_completed, 1)
        self.assertEqual(completed.total_tokens, 250)
        self.assertEqual(completed.remaining_budget["total_attempts"], 2)
        self.assertEqual(completed.remaining_budget["tokens"], 750)
        self.assertEqual(completed.next_action, "review_candidate")

    def test_hard_gate_failure_requires_explicit_stop_record(self):
        campaign = self._init()
        self._register_candidate(campaign)
        append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_started",
            payload={"candidate_id": "C-001", "attempt_id": "A-001"},
        )
        capsule = append_campaign_event(
            campaign_root=campaign,
            event_type="attempt_completed",
            payload={
                "candidate_id": "C-001",
                "attempt_id": "A-001",
                "hard_gate_passed": False,
                "improved": False,
                "metrics": {},
            },
        )
        self.assertEqual(capsule.campaign_status, "stop-required")
        self.assertIn("hard_gate_failure", capsule.stop_reasons)
        self.assertEqual(capsule.next_action, "record_campaign_stopped")

    def test_candidate_budget_does_not_block_the_last_allowed_candidate(self):
        campaign = self._init()
        self._register_candidate(campaign)
        self._complete_attempt(campaign, improved=False)
        append_campaign_event(
            campaign_root=campaign,
            event_type="candidate_rejected",
            payload={"candidate_id": "C-001"},
        )
        capsule = append_campaign_event(
            campaign_root=campaign,
            event_type="candidate_registered",
            payload={"candidate_id": "C-002", "hypothesis_id": "H-001"},
        )
        self.assertEqual(capsule.remaining_budget["candidates"], 0)
        self.assertEqual(capsule.campaign_status, "running")
        self.assertEqual(capsule.next_action, "start_attempt")

    def test_kept_candidate_requires_terminal_completion_event(self):
        campaign = self._init()
        self._register_candidate(campaign)
        self._complete_attempt(campaign)
        capsule = append_campaign_event(
            campaign_root=campaign,
            event_type="candidate_kept",
            payload={"candidate_id": "C-001"},
        )
        self.assertEqual(capsule.campaign_status, "stop-required")
        self.assertEqual(capsule.next_action, "record_campaign_completed")
        terminal = append_campaign_event(
            campaign_root=campaign,
            event_type="campaign_completed",
            payload={"reason": "accepted_candidate"},
        )
        self.assertEqual(terminal.campaign_status, "completed")
        self.assertEqual(terminal.next_action, "none")

    def test_invalid_event_order_and_unknown_hypothesis_fail_closed(self):
        campaign = self._init()
        with self.assertRaisesRegex(CampaignError, "Invalid campaign transition"):
            append_campaign_event(
                campaign_root=campaign,
                event_type="attempt_started",
                payload={"candidate_id": "C-001", "attempt_id": "A-001"},
            )
        append_campaign_event(
            campaign_root=campaign,
            event_type="hypothesis_registered",
            payload={"hypothesis_id": "H-001"},
        )
        with self.assertRaisesRegex(CampaignError, "unknown hypothesis_id"):
            append_campaign_event(
                campaign_root=campaign,
                event_type="candidate_registered",
                payload={"candidate_id": "C-001", "hypothesis_id": "H-404"},
            )

    def test_manifest_or_journal_tampering_fails_closed(self):
        campaign = self._init()
        journal = campaign / "campaign-journal.jsonl"
        payload = json.loads(journal.read_text().splitlines()[0])
        payload["payload"]["purpose"] = "tampered"
        journal.write_text(json.dumps(payload) + "\n", encoding="utf-8")
        with self.assertRaisesRegex(CampaignError, "hash mismatch"):
            inspect_campaign(campaign)

    def test_frozen_input_hash_mismatch_blocks_initialization(self):
        manifest = load_manifest_template(self.manifest_path)
        self.input.write_text("changed\n", encoding="utf-8")
        with self.assertRaisesRegex(CampaignError, "hash mismatch"):
            initialize_campaign(
                campaign_root=self.root / "blocked",
                manifest=manifest,
                inputs_root=self.root,
            )

    def test_cli_campaign_commands_do_not_require_eval_fixture_loading(self):
        campaign = self.root / "cli-campaign"
        init = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "campaign-init",
                "--manifest",
                str(self.manifest_path),
                "--campaign-root",
                str(campaign),
                "--inputs-root",
                str(self.root),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(init.returncode, 0, init.stderr or init.stdout)
        self.assertEqual(json.loads(init.stdout)["status"], "initialized")
        status = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "campaign-status",
                "--campaign-root",
                str(campaign),
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        self.assertEqual(status.returncode, 0, status.stderr or status.stdout)
        self.assertEqual(json.loads(status.stdout)["status"], "valid")


if __name__ == "__main__":
    unittest.main()
