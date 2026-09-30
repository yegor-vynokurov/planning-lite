# Route B T-06 real-source compatibility correction v1

```text
OWNER_DECISION: ACCEPT_T06_REAL_SOURCE_EVIDENCE_AND_AUTHORIZE_NARROW_COMPATIBILITY_FIX
FINDING_ID: T06-RS-01_CURRENT_CODEX_NON_USAGE_COMPATIBILITY_SURFACE_INCOMPLETE
PRIMARY_SEAM_CLASS: EVIDENCED_CURRENT_CODEX_SHAPE_OMITTED
PLAN_AMENDMENT_REQUIRED: NO
DEFINITION_AMENDMENT_REQUIRED: NO

ENTRY_HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
ENTRY_AUTHORITY_STATE_ID: 36d18fb4eac4157a4a4625310af510dff35ac55a1f7cde5189c5b7b24de12d06
ENTRY_CANDIDATE_STATE_ID: 21dfac584a924db6650e46a0b361e08b9c028d7dd2b78f5f763952f62c6651e0
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
ENTRY_SYNC_STATE_ID: c3c3381c0a5308b86eae046c0b50a3ac5afbd6df4f6931d8982aa7fc83eef3da

METADATA_ROW_COUNT: 6
METADATA_JSON_KINDS: OBJECT
METADATA_KIND_CONSISTENT: YES
METADATA_TOP_LEVEL_KEY_SET: [metadata, payload, timestamp, type] / SAME ON ALL SIX

PRODUCT_PATHS_CHANGED: src/planning_lite/codex_work_window.py
TEST_PATHS_CHANGED: tests/test_codex_work_window.py
REAL_SHAPES_ADDED:
- response_item/reasoning
- response_item/custom_tool_call
- response_item/message
- response_item/custom_tool_call_output
- event_msg/agent_message
- optional envelope metadata with object structural kind
TOKEN_USAGE_CONTRACT_CHANGED: NO

FROZEN_SEGMENT_SHA256: 361dce95ac0b65a80ba44d3d72fd5b28a051cc63a5d800a159d801df4f22afa3
FROZEN_SEGMENT_REPLAY: PASS / READ-ONLY EXACT INTERVAL
FROZEN_SEGMENT_TOTAL_ROWS: 44
FROZEN_SEGMENT_VALID_USAGE_ROWS: 6
FROZEN_SEGMENT_REJECTED_ROWS: 0
FROZEN_SEGMENT_UNIQUE_RESPONSE_COUNT: 6
FROZEN_SEGMENT_AGGREGATION: PASS
FROZEN_SEGMENT_ARITHMETIC_RECONCILIATION: PASS
NO_TELEMETRY_WRITTEN: YES
T06_V1_HISTORICAL_EVIDENCE: PRESERVED / NOT RE-FINALIZED

FOCUSED_TEST_COMMAND: uv run --frozen pytest tests/test_run_receipts.py tests/test_codex_run_receipt_capture.py tests/test_codex_work_window.py tests/test_cli.py
FOCUSED_TEST_RESULT: PASS / 176 PASSED
RUNRECEIPT_BACKWARD_COMPATIBILITY: PASS / 1 PASSED
R5_R5R_FRR_REGRESSION: PASS / INCLUDED IN FOCUSED SUITE
GIT_DIFF_CHECK: PASS
STRICT_RESUME_VALIDATOR: PASS
OPEN_MATERIAL_FINDINGS_AFTER_CORRECTION: 0

CURRENT_CHANGED: YES
ROADMAP_CHANGED: NO
UNRELATED_DIRT_UNCHANGED: YES
INDEPENDENT_REREVIEW_REQUIRED: YES
T06_V2_AUTHORIZED: NO
09_G_STARTED: NO
STAGE: NO
COMMIT: NO
PUSH: NO
```

## Scope and result

The parser now recognizes only the observed non-usage discriminators and the
optional top-level `metadata` field when it has JSON object kind. The existing
structural scanner validates and skips that object without extracting its
values. Unknown top-level fields, unsupported metadata kinds, and unknown event
or response-item discriminators remain fail-closed. No usage parsing,
aggregation, membership, attribution, or numeric-completeness rule changed.

The exact frozen T-06 V1 interval now parses with no rejected rows. Its six
usage rows continue to pass the unchanged usage parser and aggregate to six
unique responses with complete supported metrics. This replay is diagnostic
only; the historical V1 `UNAVAILABLE / USAGE_RECORD_INVALID` observation is
preserved, no live Work Window was opened, and T-06 V2 remains unauthorized
pending independent review.
