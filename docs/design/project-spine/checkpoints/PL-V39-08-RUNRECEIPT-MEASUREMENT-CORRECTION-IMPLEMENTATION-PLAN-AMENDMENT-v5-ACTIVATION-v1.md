# PL-V39-08 RunReceipt Measurement Correction - Implementation Plan Amendment v5 Activation v1

Transition: OWNER_ACCEPT_AND_ACTIVATE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_IMPLEMENTATION_PLAN_AMENDMENT_V5
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Owner decision source: EXPLICIT_HUMAN_OWNER
Owner decision: ACCEPT_AND_ACTIVATE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_IMPLEMENTATION_PLAN_AMENDMENT_V5
Decision date: 2026-09-29

## Entry state and reviewed authority

HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
ENTRY_AUTHORITY_STATE_ID: 7d9cd3007804f2f8422d7ef5cdb66fa4210ccacd00af3dde42ac8ca677548a80
ENTRY_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
ENTRY_SYNC_STATE_ID: 5c805b58dde2edcec0e563ec717374fdc83080f7e18bb05bf275a9ba8e28c034
ENTRY_INDEX_EMPTY: YES

Active Definition: PREDECESSOR + AMENDMENT V2 + AMENDMENT V6
Definition Amendment v6 SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74
Definition v6 activation SHA256: 94967e652ac0640a9465caa5af15b14f57438b1f4f71063489ecd5eb68b11dd6
Reviewed Plan candidate: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5.md
Plan Amendment v5 SHA256: b68ecd94456c9d00fcbca6524ee8063165fa95889e16f834a0416105fd2454db
Independent Plan review: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5-REVIEW-v1.md
Independent Plan review SHA256: 39284d1c68badc650ad168d4d76f154cdca1dfb04fa25fd7db733c859d195649
Independent review verdict: REVIEW_PASS / 0 MATERIAL FINDINGS

## Owner acceptance and activation

PLAN_AMENDMENT_V5: APPROVED_BY_OWNER / ACTIVE
ACTIVE_EFFECTIVE_DEFINITION: PREDECESSOR + AMENDMENT V2 + AMENDMENT V6
ACTIVE_EFFECTIVE_PLAN: PREDECESSOR + PLAN AMENDMENT V4 + PLAN AMENDMENT V5
Plan Amendment v5 supplies the active Route B implementation plan. Plan v4 is preserved unchanged as its predecessor authority, except where Plan v5 explicitly supersedes it for Route B.

ROUTE_B_VERTICAL_SLICE: WORK_WINDOW / ONE_DEDICATED_PROVIDER_SOURCE_SEGMENT
INITIAL_PROVIDER_ADAPTER: CODEX_LOCAL_ROLLOUT
EXACT_ATTEMPT_BRIDGE_REQUIRED: NO
MULTI_SOURCE_WORK_WINDOW: OUT_OF_SCOPE_FOR_FIRST_SLICE
AUTOMATIC_COLLECTION: NO

The accepted first-slice lifecycle explicitly opens a Work Window; prospectively registers the window identity, immutable configuration_ref, exact dedicated Codex source segment, source identity, and start boundary; performs measured provider work; explicitly finalizes; captures the exact end boundary; reads the stable bounded segment; aggregates structured token_usage_record.usage; persists a provider-neutral Resource Observation; and returns canonical persisted readback.

For supported exact quantities, the target result is WORK_WINDOW / DIRECT / COMPLETE_SCOPE_TOTAL. If a truthful complete result is not yet possible because the source is unstable, finalization returns REQUEST_NOT_YET_FINALIZABLE; a proven terminal source state may produce UNAVAILABLE. A BOUNDED producer is not required in the first implementation slice.

CONFIGURATION_REF_ROLE: DECLARED_IMMUTABLE_COMPARISON_ARM_REFERENCE / NOT AUTOMATICALLY PROVIDER-VERIFIED
A caller-supplied configuration_ref is not provider-verified runtime evidence unless independent evidence later proves that stronger claim.

## Accepted implementation surfaces and tasks

ACTIVE_PRODUCT_WRITE_SURFACE_COUNT: 4
- src/planning_lite/telemetry.py
- scripts/capture_codex_run_receipts.py
- src/planning_lite/codex_work_window.py
- src/planning_lite/cli.py

ACTIVE_TEST_WRITE_SURFACE_COUNT: 4
- tests/test_run_receipts.py
- tests/test_codex_run_receipt_capture.py
- tests/test_codex_work_window.py
- tests/test_cli.py

TASK_COUNT: 6
T-01: provider-neutral carrier and validator
T-02: typed persistence/readback and legacy capture compatibility
T-03: Codex dedicated-source-segment adapter
T-04: explicit work-window open/finalize CLI
T-05: focused deterministic acceptance
T-06: separately authorized real bounded field proof
ACCEPTANCE_CASE_COUNT: 20

## Preserved candidate and later gates

PRESERVED_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
PRESERVED_CANDIDATE_DISPOSITION: UNRESOLVED
PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION_REQUIRED: YES
PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION_COMPLETED: NO
CANDIDATE_DISPOSITION_AUTHORIZED_BY_THIS_TRANSITION: NO
FORMAL_READINESS_BLOCKED_PENDING_CANDIDATE_DISPOSITION: YES

The preserved candidate overlaps exactly these four accepted Route B paths:
- src/planning_lite/telemetry.py
- scripts/capture_codex_run_receipts.py
- tests/test_codex_run_receipt_capture.py
- tests/test_run_receipts.py

Its exact disposition remains a separate human-owner gate. This activation does not reset, stash, clean, revert, delete, adopt, merge, or otherwise adjudicate the candidate, and its worktree bytes are not treated as the canonical Route B baseline.

FORMAL_READINESS_FOR_ROUTE_B: NOT PERFORMED
FORMAL_READINESS_AUTHORIZED: NO
IMPLEMENTATION_AUTHORIZED: NO
T01_T05_EXECUTION_AUTHORIZED: NO
T06_FIELD_PROOF_AUTHORIZED: NO
FIELD_PROOF_AUTHORIZED: NO
T00: EXECUTED / ACCEPTED / CONSUMED / STOP_WITH_PROVEN_SEAM
T00_REEXECUTION_AUTHORIZED: NO
Q1-Q4: PRESERVED NOT_PROVEN EVIDENCE
No T00 seam is declared repaired.
PL_V39_09_G_STARTED: NO
PL_V39_09_G_SEMANTICS_REPLACED: NO

NEXT_SINGLE_GATE: OWNER_DECISION_CHANGE_3_ROUTE_B_PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION

This checkpoint records Plan acceptance and activation only. It does not adjudicate the candidate, perform Formal Readiness, authorize implementation or field proof, execute T-01 through T-06, modify product source/tests or Roadmap, rerun T00, start 09-G, or stage, commit, push, or release.

## Write and validation boundary

The only authorized repository paths for this transition are:

1. docs/design/project-spine/CURRENT.md
2. docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5-ACTIVATION-v1.md

Plan v5, its review, active Definition v6 and its review/activation, Plan v4, the preserved candidate, source, tests, Roadmap, and unrelated dirt remain unchanged. The index remains empty.

