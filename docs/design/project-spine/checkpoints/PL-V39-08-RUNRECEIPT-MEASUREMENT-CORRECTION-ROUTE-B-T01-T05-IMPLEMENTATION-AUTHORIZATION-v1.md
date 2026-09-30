# Route B T-01..T-05 Implementation Authorization v1

Transition: OWNER_AUTHORIZE_CHANGE_3_ROUTE_B_IMPLEMENTATION_T01_T05  
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001  
Decision date: 2026-09-29

## Owner decision

OWNER_DECISION_SOURCE: EXPLICIT_HUMAN_OWNER  
OWNER_DECISION: AUTHORIZE_CHANGE_3_ROUTE_B_IMPLEMENTATION_T01_T05  
AUTHORIZATION_EFFECT: IMPLEMENTATION AUTHORITY ONLY / NO TASK EXECUTED

## Strict entry synchronization

SYNC_PREFLIGHT: PASS  
ENTRY_CAPSULE: strict 12-field SYNC_CAPSULE_V1; UTF-8 JSON, sorted keys, compact separators, one final LF; `semantic_projection` and `sync_state_id` excluded from hashed bytes.  
ENTRY_HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858  
ENTRY_AUTHORITY_STATE_ID: 03422f0468677e2b406642ca87d87b2c82cbba203fafce4d2c4754599d25a3a6  
ENTRY_CANDIDATE_STATE_ID: 44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a  
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a  
ENTRY_SYNC_STATE_ID: 6a5e7ec63ce8055221a36a22783e1a0225c2ca261c14dc9e867c68eef1a94f46  
ENTRY_INDEX_EMPTY: YES  
ENTRY_DIRTY_PATH_COUNT: 65 (authority 53 / candidate 0 / unrelated 12)

## Active authority and readiness

ACTIVE_EFFECTIVE_DEFINITION: PREDECESSOR + AMENDMENT V2 + AMENDMENT V6  
DEFINITION_AMENDMENT_V6_PATH: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v6.md  
DEFINITION_AMENDMENT_V6_SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74  
ACTIVE_EFFECTIVE_PLAN: PREDECESSOR PLAN + PLAN AMENDMENT V4 + PLAN AMENDMENT V5  
PLAN_AMENDMENT_V5_PATH: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5.md  
PLAN_AMENDMENT_V5_SHA256: b68ecd94456c9d00fcbca6524ee8063165fa95889e16f834a0416105fd2454db  
PLAN_AMENDMENT_V5_ACTIVATION_PATH: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5-ACTIVATION-v1.md  
PLAN_AMENDMENT_V5_ACTIVATION_SHA256: 3a7c4f47222252aaa83ae99b49e519628109730d88eecee0dfe67362d34127e2

FORMAL_READINESS: READY  
MATERIAL_BLOCKER_COUNT: 0  
FIRST_BROKEN_SEAM: NONE  
FORMAL_READINESS_CHECKPOINT: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-ROUTE-B-FORMAL-READINESS-VERDICT-v1.md  
FORMAL_READINESS_CHECKPOINT_SHA256: 120cb05eba9be1d0409b68a8961d1f782b8fc0575461c0e6a14a8ad5aafd9e4e  
BASELINE_TEST_RESULT: 90 PASSED / 0 FAILED / PREVIOUS READINESS EVIDENCE
ROUTE_B_BASELINE_ISOLATED: YES  
CANONICAL_IMPLEMENTATION_BASELINE: HEAD 19217522f3dac695602a8534d7ddb8f9bbee5858  
HISTORICAL_CANDIDATE: ARCHIVED / NOT LIVE  
HISTORICAL_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555  
LIVE_CANDIDATE_PATH_COUNT: 0  
CANDIDATE_CONTAMINATION_REMAINING: NO  
DISPOSITION_CHECKPOINT_SHA256: ed9919a02123a65d4bdb06fc7a9be598616c7c7a757471e7ac90630dca58c7cc  
ARCHIVE_MANIFEST_SHA256: 96fcef0094cb0fb41a73f6d40d49f323f55f1c20ba2a79ce73ec4d9be79f1aff  

## Bounded implementation authority granted

T01_T05_EXECUTION_AUTHORIZED: YES  
T06_FIELD_PROOF_AUTHORIZED: NO  
IMPLEMENTATION_EXECUTED: NO  
FIELD_PROOF_EXECUTED: NO  
T00_REEXECUTION_AUTHORIZED: NO  
09_G_STARTED: NO  
EXACT_ATTEMPT_BRIDGE_REQUIRED: NO

AUTHORIZED_TASKS:
- T-01: Provider-neutral carrier and validator.
- T-02: Typed persistence/readback and legacy capture compatibility.
- T-03: Codex dedicated-source-segment adapter.
- T-04: Explicit work-window open/finalize CLI.
- T-05: Focused deterministic acceptance.

AUTHORIZED_PRODUCT_PATH_COUNT: 4
AUTHORIZED_PRODUCT_PATHS:
- `src/planning_lite/telemetry.py`
- `scripts/capture_codex_run_receipts.py`
- `src/planning_lite/codex_work_window.py`
- `src/planning_lite/cli.py`
AUTHORIZED_TEST_PATH_COUNT: 4
AUTHORIZED_TEST_PATHS:
- `tests/test_run_receipts.py`
- `tests/test_codex_run_receipt_capture.py`
- `tests/test_codex_work_window.py`
- `tests/test_cli.py`

M14: ARCHIVED / OPTIONAL T05 REINTRODUCTION  
M14_T05_REINTRODUCTION_ALLOWED: YES / OPTIONAL LEGACY-COMPATIBILITY TEST ONLY IN `tests/test_run_receipts.py`  
ATTEMPT_BRIDGE: NOT REQUIRED  
T06_REAL_CODEX_FIELD_PROOF: NOT AUTHORIZED  
REAL_MEASURED_WORK_WINDOW_DURING_T01_T05: NOT AUTHORIZED  
NEXT_SINGLE_GATE: RUN_CHANGE_3_ROUTE_B_IMPLEMENTATION_T01_T05

## Preserved constraints and stop conditions

The authorized slice is one explicitly opened/finalized WORK_WINDOW bound to one dedicated provider source segment, with the initial adapter CODEX_LOCAL_ROLLOUT. The supported success shape is `WORK_WINDOW + DIRECT + COMPLETE_SCOPE_TOTAL`; allowed non-success outcomes are `REQUEST_NOT_YET_FINALIZABLE` and `UNAVAILABLE` under the active Definition and Plan. A BOUNDED producer is not required in this first slice.

Preserve RunReceipt v1/v2 meaning and public receipt-only behavior; do not migrate or backfill history, reinterpret legacy deltas, attribute an Attempt, use timestamp-only membership, select semantic prompt/body sources, guess the latest/nearest source, call the direct OpenAI API, add a daemon/scheduler or automatic collection/lifecycle, support multi-source windows, normalize tokens across providers, make efficiency judgments, start 09-G, or perform T-06 field proof. `configuration_ref` remains `DECLARED_IMMUTABLE_COMPARISON_ARM_REFERENCE / NOT AUTOMATICALLY PROVIDER-VERIFIED`.

Stop and seek a separate owner gate if execution requires a product or test path outside the four authorized paths, breaks RunReceipt compatibility, requires Attempt/operation-lifecycle integration or a second store, materially conflicts with the accepted Codex source contract or Definition v6/Plan v5, redefines `configuration_ref` authority, or requires live-provider evidence to complete T-01..T-05. Do not restore any other archived candidate hunk.

T00 remains preserved / consumed with no reexecution. The candidate disposition remains completed. No Roadmap change is authorized.

STAGE: NO  
COMMIT: NO  
PUSH: NO  
RELEASE: NO
