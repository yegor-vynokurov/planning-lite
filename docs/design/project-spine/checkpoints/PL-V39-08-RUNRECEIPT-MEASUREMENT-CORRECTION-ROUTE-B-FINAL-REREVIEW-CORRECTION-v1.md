# Route B Final Rereview Corrections

Transition: `FIX_CHANGE_3_ROUTE_B_FINAL_REREVIEW_FINDINGS_R5R_01_R5R_02`
Change: `CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001`
Date: `2026-09-30`

## Owner decision and entry synchronization

`OWNER_DECISION`: `AUTHORIZE_AND_EXECUTE_FINAL_REREVIEW_CORRECTIONS`

The fresh strict `SYNC_CAPSULE_V1` contained exactly the twelve specified fields, with canonical UTF-8 JSON, sorted keys, compact separators, and one terminal LF. Derived `semantic_projection` and `sync_state_id` fields were excluded from the hashed object.

`SYNC_RECONCILIATION`: `PASS`
`ACTUAL_REPOSITORY_STATE_DRIFT`: `NO`
`ENTRY_HEAD`: `19217522f3dac695602a8534d7ddb8f9bbee5858`
`ENTRY_INDEX_EMPTY`: `YES`
`ENTRY_AUTHORITY_STATE_ID`: `08d6ddc4b18c6052e7aa485bb3cc8b3fee37f30b350b0f2a6d712ae5a4831edd`
`ENTRY_CANDIDATE_STATE_ID`: `ba432e66f650955997c2559720a757f0e5defafef45a3f72604752ba0f4508d2`
`ENTRY_UNRELATED_DIRT_STATE_ID`: `2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a`
`ENTRY_SYNC_STATE_ID`: `e14627761cc5ac72b6ae72f6ed8c8dc35fec90fb60113f50c9d41b0d94037984`
`ENTRY_DIRTY_PATH_COUNTS`: `76 (authority 56 / candidate 8 / unrelated 12)`
`ENTRY_ACTIVE_CHANGE`: `CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001`
`ENTRY_NEXT_GATE`: `OWNER_REREVIEW_CHANGE_3_ROUTE_B_T01_T05_CORRECTED_CANDIDATE`

All substantive entry fields matched the authorized baseline. The prior sync digest bookkeeping issue was already adjudicated; the fresh entry digest above matched the prior strict exit digest, so no synchronization gate was created.

## R5R-01: unknown installed ref

`R5R_01_STATUS`: `CORRECTED`

Work Window OPEN continues to resolve the target's `.copier-answers.planning-lite.yml` in `_commit`, then `_vcs_ref` order. With Route B's strict option, trimmed case-insensitive `unknown` is skipped as unusable, allowing a usable `_vcs_ref`; if no usable ref remains, OPEN fails before source inspection and telemetry append. Both Work Window registration and observation validation reject `unknown` after trimming and case folding.

The shared legacy RunReceipt collector retains its prior default resolution behavior. A deterministic compatibility test verifies that a legacy RunReceipt can still be collected with `_commit: UnKnOwN`; this behavior does not confer Work Window authority.

## R5R-02: minimum current envelope shapes

`R5R_02_STATUS`: `CORRECTED`

Stable known records now fail closed as `UNAVAILABLE / USAGE_RECORD_INVALID` with empty quantities when their current payload shape is incomplete. `session_meta` requires a usable `id` or `session_id`, and contradictory usable aliases fail closed. `turn_context` requires usable `turn_id` and `model` or `model_id`, retains the existing model/model_id conflict check, and contributes present session identity to membership consistency. `response_item` requires the evidenced `assistant_message` discriminator and leaves content opaque. No accepted repository fixture establishes a safe current shape for `compacted`, `inter_agent_communication_metadata`, or `world_state`; these families fail closed.

The source scanner continues to validate full JSON structure, reject duplicate keys, and avoid semantic inspection, persistence, attribution, or error echo of content/body text. Existing `event_msg` discriminator allowlisting, usage aggregation, duplicate-response handling, optional metrics, arithmetic checks, and transient partial-tail behavior remain covered by the focused suite.

## Acceptance and changed paths

`ORIGINAL_ACCEPTANCE`: `20 / 20`
`PRIOR_CORRECTIVE_ACCEPTANCE`: `22 / 22`
`NEW_REREVIEW_ACCEPTANCE_COUNT`: `20`
`NEW_REREVIEW_ACCEPTANCE_PASS`: `20`
`NEW_REREVIEW_ACCEPTANCE_FAIL`: `0`
`FOCUSED_TEST_COMMAND`: `uv run --frozen pytest tests/test_run_receipts.py tests/test_codex_run_receipt_capture.py tests/test_codex_work_window.py tests/test_cli.py -q`
`FOCUSED_TEST_RESULT`: `PASS (exit code 0)`
`RUNRECEIPT_BACKWARD_COMPATIBILITY`: `PASS`
`AUTHORIZED_SURFACE_VIOLATION`: `NO`
`MATERIAL_FINDING_COUNT_AFTER_FIX`: `0 observed by deterministic acceptance; independent final rereview pending`
`FIRST_BROKEN_SEAM`: `Unknown installed-ref sentinels could be registered as Work Window provenance, and empty/incomplete allowlisted non-usage payloads could accompany valid usage and still claim a complete direct total.`

Product paths changed:

- `src/planning_lite/telemetry.py`
- `src/planning_lite/codex_work_window.py`

Test paths changed:

- `tests/test_codex_work_window.py`
- `tests/test_run_receipts.py`

The two previously authorized product paths and the two test paths above contain the complete correction surface. `cli.py`, `test_cli.py`, the capture product, capture regression test, workspace modules, Definition, Plan, and Roadmap were not changed by this transition.

## Result and preserved gates

`RESULT`: `FINAL_CORRECTED_CANDIDATE_PREPARED`
`INDEPENDENT_FINAL_REREVIEW_REQUIRED`: `YES`
`ADDITIONAL_IMPLEMENTATION_MUTATION_AUTHORIZED`: `NO`
`T06_FIELD_PROOF_AUTHORIZED`: `NO`
`T00_REEXECUTION_AUTHORIZED`: `NO`
`REAL_WORK_WINDOW_PERFORMED`: `NO`
`09_G_STARTED`: `NO`
`STAGE`: `NO`
`COMMIT`: `NO`
`PUSH`: `NO`
`RELEASE`: `NO`

Definition amendment v6, Plan amendment v5, Formal Readiness, original implementation and corrective authorizations/executions, prior corrected-candidate receipt, independent implementation review, seam review, Roadmap, external archive manifest, and unrelated dirt remain unchanged. This candidate is ready for the final independent rereview only.

## Next single gate

`OWNER_FINAL_REREVIEW_CHANGE_3_ROUTE_B_T01_T05_CANDIDATE`
