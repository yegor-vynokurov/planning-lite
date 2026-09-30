# Change 3 Route B FRR-01 Task-Started Compatibility Fix

Transition: `FIX_CHANGE_3_ROUTE_B_FRR_01_KNOWN_TASK_STARTED_EVENT_OMITTED`
Change: `CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001`
Date: `2026-09-30`

## Owner decision

```text
OWNER_DECISION: AUTHORIZE_AND_EXECUTE_FRR_01_FIX
FRR_01_STATUS: CORRECTED
```

The correction accepts the evidenced `task_started` event only when
`payload.type` is `task_started` and `payload.turn_id` is a non-empty string.
The event remains structural control data: it is not a usage source, does not
create Attempt attribution, does not restrict a Work Window to one turn, does
not participate in timestamp membership, and does not change token aggregation.
Malformed `task_started` shapes produce terminal
`UNAVAILABLE / USAGE_RECORD_INVALID` with empty quantities.

## First broken seam

`codex_work_window._read_bounded` rejected an otherwise valid native usage
segment because its fail-closed `event_msg` allowlist omitted the evidenced
`task_started` discriminator before a valid `token_usage_record` and
`task_complete` event.

## Changed paths and acceptance

```text
PRODUCT_PATHS_CHANGED:
- src/planning_lite/codex_work_window.py

TEST_PATHS_CHANGED:
- tests/test_codex_work_window.py

FOCUSED_TEST_COMMAND:
uv run --frozen pytest tests/test_run_receipts.py tests/test_codex_run_receipt_capture.py tests/test_codex_work_window.py tests/test_cli.py -q
FOCUSED_TEST_RESULT: PASS (exit code 0)
FRR_01_ACCEPTANCE: 4 / 4 cases passed
RUNRECEIPT_BACKWARD_COMPATIBILITY: PASS
MATERIAL_FINDING_COUNT_AFTER_FIX: 0 expected; final independent confirmation pending
FINAL_INDEPENDENT_CONFIRMATION_REQUIRED: YES
```

The acceptance covers a valid `task_started` + native usage + `task_complete`
segment producing `COMPLETE` direct `COMPLETE_SCOPE_TOTAL` quantities, and
missing, empty, and non-string `turn_id` values failing closed with empty
quantities. The full established focused suite also retained the existing
event fail-closed and R5/R5R coverage.

## Preserved boundaries

```text
T06_FIELD_PROOF_AUTHORIZED: NO
REAL_WORK_WINDOW_PERFORMED: NO
T00_REEXECUTED: NO
09_G_STARTED: NO
DEFINITION_CHANGED: NO
PLAN_CHANGED: NO
ROADMAP_CHANGED: NO
STAGE: NO
COMMIT: NO
PUSH: NO
RELEASE: NO
```

R5-01, R5-02, R5R-01, and R5R-02 remain closed. The implementation candidate
is prepared for final independent confirmation; this receipt does not authorize
T-06 or any further implementation mutation.

## Next single gate

`OWNER_FINAL_CONFIRM_CHANGE_3_ROUTE_B_T01_T05_CANDIDATE`
