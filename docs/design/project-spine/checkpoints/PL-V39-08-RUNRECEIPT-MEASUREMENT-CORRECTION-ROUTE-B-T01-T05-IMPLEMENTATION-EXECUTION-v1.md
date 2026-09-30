# PL-V39-08 Route B T-01..T-05 Implementation Execution v1

Transition: RUN_CHANGE_3_ROUTE_B_IMPLEMENTATION_T01_T05
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Execution date: 2026-09-30

## Entry synchronization and authority

```text
SYNC_PREFLIGHT: PASS
ENTRY_HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
ENTRY_AUTHORITY_STATE_ID: 2fd06d1c4e0e73773c4eee329a9bc098d8b0b875d94150f8ef1c22caa321e24e
ENTRY_CANDIDATE_STATE_ID: 44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
ENTRY_SYNC_STATE_ID: 7f98aa9fec31e6f8f0419162206f201caaee9caf64d1d11083a1e07d9bc9dbde
ENTRY_INDEX_EMPTY: YES
ENTRY_DIRTY_PATH_COUNT: 66 (authority 54 / candidate 0 / unrelated 12)
LIVE_CANDIDATE_PATH_COUNT: 0
ROUTE_B_BASELINE_ISOLATED: YES
CANDIDATE_CONTAMINATION_REMAINING: NO
IMPLEMENTATION_AUTHORITY: VALID / 2ce7ca510631182c705286d92f3ab344dbc3daefe43aea3af2a3371593593b9c
ACTIVE_DEFINITION_V6_SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74
ACTIVE_PLAN_V5_SHA256: b68ecd94456c9d00fcbca6524ee8063165fa95889e16f834a0416105fd2454db
FORMAL_READINESS_VERDICT_SHA256: 120cb05eba9be1d0409b68a8961d1f782b8fc0575461c0e6a14a8ad5aafd9e4e
PRE_IMPLEMENTATION_DISPOSITION_SHA256: ed9919a02123a65d4bdb06fc7a9be598616c7c7a757471e7ac90630dca58c7cc
ARCHIVE_MANIFEST_SHA256: 96fcef0094cb0fb41a73f6d40d49f323f55f1c20ba2a79ce73ec4d9be79f1aff
```

The strict entry capsule used the exact twelve `SYNC_CAPSULE_V1` fields,
UTF-8, sorted keys, compact separators, and one final LF; its hash excluded
`semantic_projection` and `sync_state_id`. The six archived candidate paths
matched canonical HEAD before implementation. No T00 rerun or Roadmap mutation
occurred.

## Task execution

```text
TASK_STATUS_T01: COMPLETE
TASK_STATUS_T02: COMPLETE
TASK_STATUS_T03: COMPLETE
TASK_STATUS_T04: COMPLETE
TASK_STATUS_T05: COMPLETE
T06_FIELD_PROOF_EXECUTED: NO
```

T-01 adds strict `WorkWindowRegistrationV1` and `ResourceObservationV1`
dispatch and validation. Legacy untagged RunReceipt v1/v2 shapes and meanings
remain unchanged. `DIRECT` quantities require a complete source and metric
and `COMPLETE_SCOPE_TOTAL`; valid `BOUNDED` claims cannot assert a complete
scope total. Unavailable observations carry no numeric quantities.

T-02 persists registration and final observation siblings in the existing
receipt JSONL stream. The existing per-path thread and process lock protects
scan, identity/replay decision, append, and canonical readback. Capture scans
and validates typed siblings while returning and producing RunReceipts only.

T-03 adds the explicit Codex source adapter. It records `st_dev` and `st_ino`
from `os.fstat` on the open handle and cross-checks them with `Path.stat`.
The prefix anchor is SHA256 over the last at most 64 raw bytes before the
registered start offset. Finalization captures one EOF bound, enforces an LF
record boundary, verifies path/handle identity and anchor, reads exactly
`[start_offset_bytes, end_offset_bytes)` twice, and compares segment digests.
One immediate bounded retry is allowed for transient read instability. Stable
malformed segments retain their digest and end bound in the unavailable row;
integrity failures do not claim a trusted segment digest.

Only allowlisted envelope metadata and `token_usage_record.usage` are used.
Rows deduplicate by `(thread_id, response_id)`, reject conflicting duplicates,
preserve a deterministic response identity digest, validate provider-native
integer quantities and accepted arithmetic, and never infer zeros for absent
metrics. No Attempt bridge, API usage, efficiency result, cross-provider
normalization, or 09-G output was added.

T-04 adds explicit `work-window open` and `work-window finalize` CLI commands.
Both require an inspected registered project and enabled telemetry before
calling the adapter; open also validates the immutable configuration
reference before source inspection. Finalize uses the persisted source
registration and returns persisted canonical readback.

T-05 provides synthetic acceptance coverage only. No live provider source or
real measured Work Window was opened.

## Identity and compatibility choices

```text
CARRIER_CHOICE: Versioned typed sibling records in the existing receipt JSONL stream
REGISTRATION_IDENTITY_CHOICE: window_id in a namespace separate from receipt_id
OBSERVATION_IDENTITY_CHOICE: work-window-observation-v1:<SHA256(window_id UTF-8)>
SOURCE_IDENTITY_MECHANISM: (st_dev, st_ino) from open handle, cross-checked against the resolved path
PREFIX_ANCHOR_MECHANISM: SHA256 of [max(0,start-64), start) raw bytes
STABLE_READ_MECHANISM: Fixed EOF bound; two exact bounded reads and SHA256 comparison; one immediate bounded retry
M14_REINTRODUCED: NO
M14_REASON: Existing A-01 receipt-only compatibility coverage is adequate; no archived Attempt-bound hunk was restored.
```

Registration replay compares the immutable caller intent and returns the first
persisted registration, preserving its original start boundary. Observation
replay returns the persisted row; a conflicting terminal result for the same
window fails with `WINDOW_ALREADY_FINALIZED_CONFLICT`.

## Acceptance coverage

```text
ACCEPTANCE_CASE_COUNT: 20
ACCEPTANCE_CASES_PASS: 20
```

| Case | Deterministic coverage |
|---|---|
| A-01 | `test_a01_receipt_only_apis_keep_shape_with_typed_siblings` and the existing receipt append/replay/readback tests |
| A-02 | `test_a02_typed_dispatch_is_strict_and_namespaces_are_separate`; capture sibling test |
| A-03 | `test_a03_registration_survives_fresh_scan_and_readback` |
| A-04 | `test_a04_exact_open_replays_after_growth_and_conflicting_intent_fails` |
| A-05 | `test_a05_timestamp_or_pre_registration_content_does_not_create_membership` |
| A-06 | `test_a06_source_identity_truncation_and_anchor_conflicts_fail_closed` (replacement, truncation, anchor variants) |
| A-07 | `test_a07_partial_tail_and_unstable_reads_are_not_finalized` |
| A-08 | `test_a08_exact_segment_aggregates_structured_usage_and_ignores_content_payloads` |
| A-09 | `test_a09_identical_response_duplicates_count_once_and_conflicts_are_unavailable` |
| A-10 | `test_a10_absent_optional_metrics_are_not_fabricated_as_zero` |
| A-11 | `test_a11_complete_supported_metrics_are_direct_scope_totals` |
| A-12 | `test_a12_observation_needs_no_attempt_bridge` |
| A-13 | `test_a13_identical_terminal_replay_returns_exact_persisted_bytes` |
| A-14 | `test_a14_conflicting_terminal_replay_has_stable_conflict` |
| A-15 | `test_a15_canonical_readback_matches_the_persisted_semantic_record` |
| A-16 | `test_a16_preopen_bytes_and_growth_after_captured_end_are_excluded` |
| A-17 | `test_a17_result_stays_provider_native_and_has_no_comparison_output` |
| A-18 | `test_a18_terminal_bad_usage_is_one_unavailable_nonzero_claim_free_observation`; `test_a18_missing_usage_is_unavailable_not_measured_zero` |
| A-19 | `test_a19_concurrent_open_finalize_and_receipt_writes_keep_unique_rows` plus existing process-safe RunReceipt append coverage |
| A-20 | `test_a20_work_window_commands_check_registration_before_source_access` |

```text
FOCUSED_TEST_COMMAND: uv run --frozen pytest tests/test_run_receipts.py tests/test_codex_run_receipt_capture.py tests/test_codex_work_window.py tests/test_cli.py
FOCUSED_TEST_RESULT: PASS / 117 passed / 0 failed
RUNRECEIPT_BACKWARD_COMPATIBILITY: PASS
```

## Changed surfaces and disposition

```text
PRODUCT_PATH_COUNT_CHANGED: 4
PRODUCT_PATHS_CHANGED:
- src/planning_lite/telemetry.py
- scripts/capture_codex_run_receipts.py
- src/planning_lite/codex_work_window.py
- src/planning_lite/cli.py

TEST_PATH_COUNT_CHANGED: 4
TEST_PATHS_CHANGED:
- tests/test_run_receipts.py
- tests/test_codex_run_receipt_capture.py
- tests/test_codex_work_window.py
- tests/test_cli.py

AUTHORIZED_SURFACE_VIOLATION: NO
MATERIAL_IMPLEMENTATION_FINDING_COUNT: 0
FIRST_BROKEN_SEAM: NONE
IMPLEMENTATION_RESULT: CANDIDATE_PREPARED
IMPLEMENTATION_REVIEW_REQUIRED: YES
IMPLEMENTATION_AUTHORIZED_FOR_ADDITIONAL_MUTATION: NO
FIELD_PROOF_AUTHORIZED: NO
09_G_STARTED: NO
T00_REEXECUTION_AUTHORIZED: NO
STAGE: NO
COMMIT: NO
PUSH: NO
```

Only the listed four product and four test paths were changed for this
implementation. Governance bookkeeping is limited to this execution
checkpoint and `docs/design/project-spine/CURRENT.md`. Review is the next
permitted gate; T-06 remains unauthorized and unexecuted.
