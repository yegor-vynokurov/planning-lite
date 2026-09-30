# Change 3 Route B T-06 Poker Registration and Field Proof

schema_version: 1
transition: AUTHORIZE_POKER_PROJECT_POLICY_REGISTRATION_DELTA_AND_EXECUTE_CHANGE_3_ROUTE_B_T06
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
date: 2026-09-30

## Owner decision and entry

```text
OWNER_DECISION: AUTHORIZE_POKER_PROJECT_POLICY_REGISTRATION_DELTA_AND_EXECUTE_T06
PLAN_AMENDMENT_REQUIRED: NO
OWNER_FINAL_REVIEW: PASS / 0 MATERIAL FINDINGS
ENTRY_HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
ENTRY_AUTHORITY_STATE_ID: 89c7a8ca755cf3e721281c3f98a297dd4f854ac8c7d47c0c8a09b0a3cad69733
ENTRY_CANDIDATE_STATE_ID: 21dfac584a924db6650e46a0b361e08b9c028d7dd2b78f5f763952f62c6651e0
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
ENTRY_SYNC_STATE_ID: d8b7becffcb40211ab98e6845996b984fbfbd1e9c6dc9a8acb94982b33bbc446
INDEX_EMPTY_AT_ENTRY: YES
```

## Bounded target registration

```text
TARGET: D:\documents\poker
TARGET_CLASS: EXISTING_REAL_PLANNING_LITE_CONSUMER
HOME: D:\documents\planning-lite\.local
PROJECT_ID: planning-lite-t06-poker
AUTHORIZED_TARGET_WRITE: .planning/CONFIG.yml
CONFIG_CHANGE_CLASS: REGISTRATION_PROJECT_POLICY_ONLY
REGISTRATION_DRY_RUN: PASS / EXACT TWO PATHS
REGISTRATION_EXECUTED: YES
```

The dry run planned exactly the authorized consumer configuration and Planning
Lite home registry paths. Registration selected `local-only` because the
existing effective project policy had no configured control-history mode.
Registration used status `paused` and enabled telemetry.

```text
CONFIG_PRE_SHA256: 7c0a92d51fe364b52bced7ef2ac127e5a80f792235584a6660f90320775ef770
CONFIG_POST_SHA256: b428aa664f276d06351573814a9ccee3137aaa94701687db38ebe4ee06335edd
CONFIG_PRE_SEMANTICS: {}
CONFIG_POST_SEMANTICS:
  project_policy.project_id: planning-lite-t06-poker
  project_policy.control_history_mode: local-only
  project_policy.telemetry.enabled: true
CONFIG_SEMANTIC_DELTA: ONLY THE THREE AUTHORIZED PROJECT_POLICY VALUES ABOVE
ALL_OTHER_CONFIG_SEMANTICS_PRESERVED: YES
COPIER_ANSWERS_PRE_SHA256: 2c462fa5698b4154c160f642ff5988cf9ce9af4d4795cb5e0b786d229916c2e0
COPIER_ANSWERS_POST_SHA256: 2c462fa5698b4154c160f642ff5988cf9ce9af4d4795cb5e0b786d229916c2e0
COPIER_ANSWERS_CHANGED: NO
POKER_STATUS_PRE_COUNT: 17
POKER_STATUS_POST_COUNT: 17
POKER_STATUS_PRE_SHA256: 6f7436e77553775b2117e1cce36f74e286012b49de9b9299435fcb7812a2ad5f
POKER_STATUS_POST_SHA256: 6f7436e77553775b2117e1cce36f74e286012b49de9b9299435fcb7812a2ad5f
POKER_PREEXISTING_DIRT_PRESERVED: YES
UNAUTHORIZED_POKER_PATH_CHANGED: NO
```

Existing Planning Lite inspect readback:

```text
PROJECT_ID: planning-lite-t06-poker
PROJECT_ROOT: D:\documents\poker
CONTROL_HISTORY_MODE: local-only
PROJECT_STATUS: paused
TELEMETRY_ENABLED: YES
RECEIPT_PATH: D:\documents\planning-lite\.local\state\projects\planning-lite-t06-poker\telemetry\run-receipts.jsonl
INSTALLED_PLANNING_LITE_REF: v4.3.0-45-gc9deee6
```

## Current session source binding and Work Window

The runtime `CODEX_SESSION_ID` and `CODEX_THREAD_ID` both matched
`01a0e8ae-a956-7c13-ad6e-b123d9f5aed5`. Structured `session_meta.payload.id`
matching found exactly one rollout file among 243 scanned:

```text
SOURCE_SESSION_BINDING: PASS / UNIQUE STRUCTURED MATCH
SOURCE_REF: C:\Users\yegor\.codex\sessions\2026\09\28\rollout-2026-09-28T18-42-35-01a0e8ae-a956-7c13-ad6e-b123d9f5aed5.jsonl
WINDOW_ID: CHANGE_3_ROUTE_B_T06_FIELD_PROOF_V1
CONFIGURATION_REF: field-proof:v1
PROVIDER: codex
REGISTRATION_STATE: OPEN
MEMBERSHIP_RULE: DEDICATED_EXPLICIT_SOURCE_SEGMENT_V1
PLANNING_LITE_REF: v4.3.0-45-gc9deee6
START_OFFSET_BYTES: 33965963
```

The canonical persisted WorkWindowRegistration matched the CLI OPEN result;
exactly one registration exists for the window. A bounded read-only continuation
reread the existing FRR-01 checkpoint. The source interval was complete through
the finalized end offset and contained six complete structured
`token_usage_record` rows after OPEN.

## T-06 result

```text
T06_EXECUTED: YES / OPENED AND FINALIZED
T06_RESULT: FAIL_CLOSED_REAL_SOURCE_SEAM
RECORD_TYPE: resource_observation
SCOPE_KIND: WORK_WINDOW
SCOPE_ID: CHANGE_3_ROUTE_B_T06_FIELD_PROOF_V1
END_OFFSET_BYTES: 34076473
SEGMENT_SHA256: 361dce95ac0b65a80ba44d3d72fd5b28a051cc63a5d800a159d801df4f22afa3
SOURCE_COMPLETENESS: UNAVAILABLE
UNAVAILABLE_REASON: USAGE_RECORD_INVALID
RESOURCE_OBSERVATION_ID: work-window-observation-v1:20fea75d362d0005f9053af568be8aecb21d12f60839c97a98900250d1b256aa
UNIQUE_RESPONSE_COUNT: 0
RESPONSE_IDENTITY_SHA256: 4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945
MEASURED_NATIVE_QUANTITIES: NONE
METRIC_COMPLETENESS: ALL UNAVAILABLE
```

The provider source did not yield an eligible usage set. No Attempt attribution,
efficiency judgment, or numeric claim is made. Product source and tests were not
changed.

## Persistence, replay, and privacy

```text
CANONICAL_READBACK: PASS / EQUAL TO FIRST FINALIZE RESULT
FINALIZE_REPLAY: PASS / EXACT PERSISTED RESOURCE OBSERVATION RETURNED
REPLAY_TELEMETRY_BYTES_UNCHANGED: YES
POST_REPLAY_TELEMETRY_SHA256: 9a65fb85fd80708a2ce6360cf8331d3a7ad4b7c6abb20caed7128cd5fd11c5b7
WINDOW_REGISTRATION_COUNT: 1
WINDOW_OBSERVATION_COUNT: 1
PRIVACY_BODY_PERSISTENCE: NONE OBSERVED
```

The persisted observation contains structural source metadata and an unavailable
reason only. It contains no prompt, reasoning text, assistant body, or tool body.
The `reasoning_output_tokens` label in metric-completeness metadata is a metric
name; its value is `UNAVAILABLE` and it contains no reasoning content.

## Repository and write boundaries

```text
POKER_CHANGED_ONLY_BY_AUTHORIZED_CONFIG_DELTA: YES
PLANNING_LITE_PRODUCT_SOURCE_CHANGED: NO
PLANNING_LITE_TESTS_CHANGED: NO
DEFINITION_CHANGED: NO
PLAN_CHANGED: NO
ROADMAP_CHANGED: NO
T00_REEXECUTED: NO
09_G_STARTED: NO
STAGE: NO
COMMIT: NO
PUSH: NO
```

No success projection was applied to `CURRENT.md` because T-06 ended in a
terminal fail-closed observation. The registered target and terminal
observation remain in the Planning Lite home as evidence.
