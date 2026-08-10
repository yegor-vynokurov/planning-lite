from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from dataclasses import dataclass

@dataclass(frozen=True)
class SuiteExecutionResult:
    schema_version: int
    suite_id: str
    eval_id: str
    status: str
    suite_root: str
    plan_path: str
    state_path: str
    result_path: str | None
    aggregation_path: str | None
    report_path: str | None
    runs_csv_path: str | None
    arm_summary_csv_path: str | None
    pairwise_csv_path: str | None
    verdict_path: str | None
    total_runs: int
    terminal_runs: int
    passed_runs: int
    failed_runs: int
    error_runs: int
    resolved_runs: int
    safe_deferral_runs: int
    all_runs_executed: bool
    all_passed: bool
    run_order: tuple[str, ...]


from planning_lite.campaign.campaign import (
    CampaignError,
    initialize_campaign,
    inspect_campaign,
    load_campaign_journal,
    load_manifest_template,
)
from planning_lite.campaign.campaign_suite import (
    CampaignSuiteBinding,
    CampaignSuiteError,
    complete_campaign_suite_attempt,
    start_campaign_suite_attempt,
)


class CampaignSuiteAdapterTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        frozen = self.root / "frozen.txt"
        frozen.write_text("frozen\n", encoding="utf-8")
        frozen_sha = hashlib.sha256(frozen.read_bytes()).hexdigest()
        manifest_path = self.root / "manifest.json"
        manifest_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "campaign_id": "suite-adapter-test",
                    "purpose": "Test deterministic suite-to-campaign journaling.",
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
                            "sha256": frozen_sha,
                        }
                    ],
                    "mutable_scope": ["src/planning_lite/campaign/**"],
                    "off_limits": ["template/**"],
                    "budget": {
                        "max_candidates": 2,
                        "max_attempts_per_candidate": 3,
                        "max_total_attempts": 6,
                        "max_total_tokens": 10000,
                        "max_wall_clock_seconds": 1000,
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
        self.suite_root = self.root / "suites" / "suite-001"
        self.suite_root.mkdir(parents=True)
        self.binding = CampaignSuiteBinding(
            campaign_root=self.campaign_root,
            hypothesis_id="H-001",
            candidate_id="C-001",
            attempt_id="A-001",
            summary="Adapter candidate",
        )
        self.plan_sha = "a" * 64
        self._write_terminal_suite()

    def tearDown(self):
        self.temp.cleanup()

    def _write_json(self, path: Path, payload: object) -> None:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def _write_terminal_suite(self) -> None:
        metrics_paths = []
        runs = []
        for index, tokens in enumerate((100, 110, 120), start=1):
            record = self.suite_root / "runs" / f"run-{index}"
            record.mkdir(parents=True)
            metrics = record / "metrics.json"
            self._write_json(metrics, {"tokens": {"total_tokens": tokens}})
            metrics_paths.append(metrics)
            runs.append(
                {
                    "run_id": f"run-{index}",
                    "execution_run_id": f"run-{index}",
                    "metrics_path": str(metrics),
                    "record_dir": str(record),
                    "status": "passed",
                }
            )
        self._write_json(
            self.suite_root / "suite-plan.json",
            {
                "suite_id": "suite-001",
                "eval_id": "lifecycle-status",
                "source_commit": "abc123",
                "plan_sha256": self.plan_sha,
            },
        )
        self._write_json(
            self.suite_root / "suite-state.json",
            {
                "suite_id": "suite-001",
                "status": "completed",
                "started_at_utc": "2026-08-06T09:00:00Z",
                "completed_at_utc": "2026-08-06T09:00:12.5Z",
                "runs": runs,
            },
        )
        self._write_json(self.suite_root / "suite-result.json", {"status": "completed"})
        self._write_json(self.suite_root / "suite-aggregation.json", {"complete": True})
        self._write_json(self.suite_root / "suite-report.json", {"complete": True})
        self._write_json(
            self.suite_root / "suite-verdict.json",
            {"status": "promote-for-fixture", "recommended_arm": "snapshot"},
        )

    def _result(self, *, terminal: bool = True) -> SuiteExecutionResult:
        return SuiteExecutionResult(
            schema_version=1,
            suite_id="suite-001",
            eval_id="lifecycle-status",
            status="completed" if terminal else "incomplete",
            suite_root=str(self.suite_root),
            plan_path=str(self.suite_root / "suite-plan.json"),
            state_path=str(self.suite_root / "suite-state.json"),
            result_path=str(self.suite_root / "suite-result.json") if terminal else None,
            aggregation_path=str(self.suite_root / "suite-aggregation.json") if terminal else None,
            report_path=str(self.suite_root / "suite-report.md") if terminal else None,
            runs_csv_path=None,
            arm_summary_csv_path=None,
            pairwise_csv_path=None,
            verdict_path=str(self.suite_root / "suite-verdict.json") if terminal else None,
            total_runs=3,
            terminal_runs=3 if terminal else 1,
            passed_runs=3 if terminal else 1,
            failed_runs=0,
            error_runs=0,
            resolved_runs=3 if terminal else 1,
            safe_deferral_runs=0,
            all_runs_executed=terminal,
            all_passed=terminal,
            run_order=("run-1", "run-2", "run-3"),
        )

    def _start(self):
        return start_campaign_suite_attempt(
            self.binding,
            suite_id="suite-001",
            eval_id="lifecycle-status",
            source_commit="abc123",
            suite_root=self.suite_root,
            plan_sha256=self.plan_sha,
        )

    def test_suite_attempt_is_journaled_once_and_uses_aggregate_cost(self):
        started = self._start()
        self.assertEqual(started.next_action, "recover_or_complete_attempt")
        completed = complete_campaign_suite_attempt(self.binding, self._result())
        self.assertEqual(completed.next_action, "review_candidate")
        self.assertEqual(completed.attempts_started, 1)
        self.assertEqual(completed.attempts_completed, 1)
        self.assertEqual(completed.total_tokens, 330)
        self.assertEqual(completed.wall_clock_seconds, 12.5)

        events = load_campaign_journal(self.campaign_root)
        self.assertEqual(
            [event.event_type for event in events],
            [
                "campaign_initialized",
                "hypothesis_registered",
                "candidate_registered",
                "attempt_started",
                "attempt_completed",
            ],
        )
        payload = events[-1].payload
        self.assertTrue(payload["hard_gate_passed"])
        self.assertTrue(payload["improved"])
        self.assertEqual(payload["suite"]["verdict_status"], "promote-for-fixture")
        self.assertEqual(len(payload["suite"]["evidence_sha256"]), 6)

        # Repeating both hooks is safe after a terminal suite.
        self._start()
        complete_campaign_suite_attempt(self.binding, self._result())
        self.assertEqual(len(load_campaign_journal(self.campaign_root)), 5)

    def test_incomplete_suite_leaves_attempt_open_for_suite_resume(self):
        self._start()
        capsule = complete_campaign_suite_attempt(self.binding, self._result(terminal=False))
        self.assertEqual(capsule.next_action, "recover_or_complete_attempt")
        self.assertEqual(capsule.attempts_completed, 0)
        self.assertEqual(len(load_campaign_journal(self.campaign_root)), 4)

    def test_completed_attempt_detects_suite_evidence_tampering(self):
        self._start()
        complete_campaign_suite_attempt(self.binding, self._result())
        verdict = self.suite_root / "suite-verdict.json"
        verdict.write_text('{"status":"retain-baseline"}\n', encoding="utf-8")
        with self.assertRaisesRegex(CampaignSuiteError, "evidence hash mismatch"):
            self._start()

    def test_attempt_identity_mismatch_fails_closed(self):
        self._start()
        other = CampaignSuiteBinding(
            campaign_root=self.campaign_root,
            hypothesis_id="H-001",
            candidate_id="C-001",
            attempt_id="A-001",
        )
        with self.assertRaisesRegex(CampaignSuiteError, "identity mismatch"):
            start_campaign_suite_attempt(
                other,
                suite_id="suite-other",
                eval_id="lifecycle-status",
                source_commit="abc123",
                suite_root=self.root / "other-suite",
                plan_sha256="b" * 64,
            )

    def test_binding_validates_as_standalone_adapter_contract(self):
        binding = CampaignSuiteBinding(
            campaign_root=self.campaign_root,
            hypothesis_id="H-001",
            candidate_id="C-001",
        )
        binding.validate()
        self.assertEqual(binding.resolved_attempt_id("suite-001"), "suite-001")

    def test_binding_rejects_missing_hypothesis(self):
        binding = CampaignSuiteBinding(
            campaign_root=self.campaign_root,
            hypothesis_id="",
            candidate_id="C-001",
        )
        with self.assertRaisesRegex(CampaignSuiteError, "hypothesis_id"):
            binding.validate()


if __name__ == "__main__":
    unittest.main()
