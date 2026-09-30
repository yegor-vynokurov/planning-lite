# PL-V39-08 RunReceipt Measurement Correction — Option C Owner Decision

schema_version: 1
transition: OWNER_DECISION_CHANGE_3_BOUNDARY_PROVENANCE_AND_CAPTURE_HANDOFF_DISPOSITION
owner_decision_source: EXPLICIT_HUMAN_OWNER
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
owner_decision: SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT
decision_date: 2026-09-28

## Decision fields

```text
OWNER_DECISION:
SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT

BOUNDARY_DELTA_REMOVED:
NO

RESPONSE_AGGREGATE_SELECTED_AS_PREFERRED_CODEX_METHOD:
YES

DIRECT_OPENAI_API_REQUIRED:
NO

NEW_CODEX_INSTRUMENTATION_REQUIRED_FOR_ROOT_USAGE:
NO

ATTEMPT_TO_TURN_BINDING_REMAINS_TO_BE_DESIGNED:
YES

WHOLE_AGENT_TREE_REQUIRED_FOR_ROOT_MEASUREMENT:
NO

DEFINITION_AMENDMENT_REQUIRED:
YES

PLAN_AMENDMENT_REQUIRED_AFTER_DEFINITION_ACCEPTANCE:
YES

IMPLEMENTATION_AUTHORIZED:
NO

09_G_STARTED:
NO
```

The owner rejects further pursuit of a new cumulative before/after host-counter
handoff as the preferred Change 3 path and selects a material Definition
Amendment route based on locally persisted Codex per-response token usage
records. This decision authorizes preparation of exactly one Definition
Amendment candidate for owner review. It does not accept exact Amendment text,
activate amended semantics, prepare a Plan Amendment, authorize implementation,
or start 09-G.

## Accepted local evidence

The four external read-only artifacts were present and their SHA256 values were
verified at entry and exit. They remain outside the repository write surface.

| Artifact | SHA256 |
|---|---|
| `D:\documents\planning-lite-sync\CHANGE_3_CODEX_TOKEN_USAGE_RECORD_LOCAL_PROBE_V1.md` | `9cf4d33c90f0a8522c4cc45ba9ade246c82ee1dba5297f0b559cc26cd8139427` |
| `D:\documents\planning-lite-sync\CHANGE_3_CODEX_TOKEN_USAGE_RECORD_LOCAL_PROBE_V1.json` | `f935042e962d3d5fa0707e51091f3757c37dd9121d1ed1830ce856e4a80cb934` |
| `D:\documents\planning-lite-sync\CHANGE_3_PLANNING_LITE_ATTEMPT_TO_CODEX_TURN_MAPPING_PROBE_V1.md` | `ac77d7c175e92ec8ce6ba834b5e920062fd80ca4a1db2fc42fa183c6dad6b0b3` |
| `D:\documents\planning-lite-sync\CHANGE_3_PLANNING_LITE_ATTEMPT_TO_CODEX_TURN_MAPPING_PROBE_V1.json` | `8c235bfb9bb95d8ff1182a330ec25eb77ccfb41658b32e68482dd9f950440246` |

Accepted conclusions:

1. Actual Codex VS Code/sidebar sessions persist structured per-response
   `token_usage_record` telemetry locally; direct OpenAI API calls are not
   required for this local usage ledger.
2. Records expose structured `thread_id`, `turn_id`, `session_id`,
   `root_turn_id`, `response_id`, and numeric usage fields.
3. Unique per-response records can be deterministically aggregated for a root
   turn without cumulative before/after subtraction. One completed observed
   turn had 11 unique responses and totals of input `547702`, cached input
   `468224`, uncached input `79478`, output `56429`, reasoning output `25178`,
   and total `604131`; the result exactly matched final `turn_token_usage`.
4. `CODEX_THREAD_ID` was present in the sidebar environment and matched the
   rollout thread identity. Current turn identity was available through
   structured task/turn metadata without parsing prompt bodies.
5. Existing Change 3 receipt/measurement structures carry host session and
   host turn identity; RunReceipt schema v2 permits `attempt_id`.
6. The missing root-only seam is the exact authoritative Planning Lite Attempt
   to `(thread_id, turn_id)` join. Its existence is not proven by the current
   capture path.
7. Whole-agent-tree attribution is `PARTIAL`. It is not a prerequisite for a
   separately proven root-only measurement.
8. If multiple Attempts share a Codex turn and response ownership cannot be
   separated deterministically, per-Attempt measurement must fail closed; the
   turn aggregate must not be divided or guessed.

## Definition Amendment disposition

Exactly one candidate was prepared:

```text
path: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v1.md
sha256: ec31d84aa97b1aecf2b8763e3423221d10072ac85a8799eed5700b81aeee7335
status: CANDIDATE / OWNER_REVIEW_REQUIRED
```

The candidate proposes `SOURCE-BOUND OPERATION-LOCAL MEASUREMENT` with
versioned `RESPONSE_AGGREGATE` as the preferred Codex method when its safe scope
and exact Attempt binding are proven, and `BOUNDARY_DELTA` as a preserved
fallback. Existing v1 delta fields keep their prior meaning. R-01
`SAFE_BOUNDARY_PROVENANCE_NOT_BOUND` and R-02
`M13_CAPTURE_TO_GOVERNED_HANDOFF_NOT_PROVEN` remain open against the
boundary-delta-only candidate; neither is closed by this decision. Their
possible supersession for a response-aggregate path remains for owner review.

The approved predecessor Definition remains immutable historical authority.
No Plan Amendment is prepared. After Definition Amendment acceptance, a Plan
Amendment is required before implementation of amended semantics. The current
corrective candidate remains `PRESERVE / DO NOT COMMIT` at state ID
`37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555`.

## State and write-boundary record

```text
entry_head: 19217522f3dac695602a8534d7ddb8f9bbee5858
exit_head: 19217522f3dac695602a8534d7ddb8f9bbee5858
entry_authority_state_id: 565ab23ded027f85b3ecb84e327a4a02728e90b631aa5cc9e6fd30679c9ce16f
exit_authority_state_id: ca23d96a0c8c8d4db43c0abe458fc88eb30e20679a70c4a9afcebf6f346b744b
authority_state_id_semantics: SHA256 of exact CURRENT.md bytes
entry_candidate_state_id: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
exit_candidate_state_id: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
entry_unrelated_dirt_state_id: 8637ad6c46d5b5e738f1de72256f9c2e78bd53b7ab3de76f55ebf3af089d51fc
exit_unrelated_dirt_state_id: 8637ad6c46d5b5e738f1de72256f9c2e78bd53b7ab3de76f55ebf3af089d51fc
unrelated_dirt_state_id_semantics: SHA256 of sorted git porcelain path/status and file SHA256 rows, excluding the three authorized paths
entry_sync_state_id: 62fef00f78bc1d9d1ff0dcde41661b4249514d47a924ef406e9d41eed363ad08
exit_sync_state_id: 62fef00f78bc1d9d1ff0dcde41661b4249514d47a924ef406e9d41eed363ad08
sync_state_id_semantics: SHA256 of the ordered four evidence artifact names and SHA256 values recorded above
entry_index_empty: YES
exit_index_empty: YES
source_changed: NO / entry bytes preserved
tests_changed: NO / entry bytes preserved
roadmap_changed: NO
corrective_candidate_changed: NO
prior_definition_changed: NO
prior_plan_changed: NO
prior_review_checkpoints_changed: NO
unrelated_dirt_unchanged: YES
stage: NOT PERFORMED
commit: NOT PERFORMED
push: NOT PERFORMED
```

The repository write surface for this transition was limited to `CURRENT.md`,
this owner-decision checkpoint, and the single Definition Amendment candidate.
The `PLANNING_LITE_RESUME_CONTRACT_V1` key schema was preserved. The approved
predecessor Definition, original Plan, existing review checkpoints, corrective
candidate, source, tests, Roadmap, and unrelated dirt remain unchanged.

## Current authority and next gate

`CURRENT.md` now projects Option C and the pending Amendment review. The
Amendment is not approved or active; the original approved Definition remains
historical authority; implementation is not authorized; and the existing Plan
requires a downstream Amendment only after acceptance of the Definition
Amendment.

The only next gate is:

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_DEFINITION_AMENDMENT
```

