# PL-V39-08 RunReceipt Measurement Correction - Option C Sync Correction v2

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: HISTORICAL_OPTION_C_SYNC_ENTRY_EXIT_INTERPRETATION_CORRECTION
transition_source: AUTHORIZED_GOVERNANCE_CORRECTION
transition_date: 2026-09-29
supersedes: HISTORICAL_ENTRY_EXIT_INTERPRETATION_ONLY

## Scope and preserved authority

This v2 clarification does not edit the Option C owner-decision checkpoint or
Sync Correction v1. Sync Correction v1 remains valid for the reconciled
CURRENT / POST-OPTION-C canonical state recorded there. Its canonical IDs are
for that post-transition state only and must not be read as proof that the
historical Option C transition entry and exit canonical IDs were identical.

The semantic Option C owner decision
`SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT` remains valid. The
accepted external evidence bindings remain valid. This clarification does not
change the accepted definition semantics, candidate state, authorization, or
current post-Option-C reconciliation.

## Historical entry / exit distinction

The earlier Option C transition evidence records these byte-presence facts:

```text
HISTORICAL_ENTRY_CURRENT_SHA256:
565ab23ded027f85b3ecb84e327a4a02728e90b631aa5cc9e6fd30679c9ce16f

HISTORICAL_EXIT_CURRENT_SHA256:
ca23d96a0c8c8d4db43c0abe458fc88eb30e20679a70c4a9afcebf6f346b744b

OPTION_C_OWNER_DECISION_CHECKPOINT:
ABSENT AT ENTRY / PRESENT AT EXIT

DEFINITION_AMENDMENT_V1:
ABSENT AT ENTRY / PRESENT AT EXIT

HISTORICAL_OPTION_C_ENTRY_CANONICAL_STATE_ID:
NOT_RECONSTRUCTED / NOT_REQUIRED_FOR_CURRENT_STATE_SAFETY
```

The entry and exit `CURRENT.md` byte hashes differ, and the two governance
checkpoints above were added during that transition. A canonical historical
entry AUTHORITY_STATE_ID or SYNC_STATE_ID is not asserted because the complete
historical entry capsule is not being reconstructed. Sync Correction v1's
mapping of both historical `entry_*` and `exit_*` fields to the post-Option-C
canonical values must not be interpreted as reconstructing the entry state.

## Verified post-Option-C state

These values are the reconciled CURRENT / POST-OPTION-C canonical state from
Sync Correction v1 and its verified capsule/report. They do not stand in for
unreconstructed historical entry IDs.

```text
POST_OPTION_C_AUTHORITY_STATE_ID:
fd6fc9ddaffa8f1d826fdf35b2db5d291a77d0f4ffb02d74a65266959df6360c

POST_OPTION_C_CANDIDATE_STATE_ID:
37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555

POST_OPTION_C_UNRELATED_DIRT_STATE_ID:
2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a

POST_OPTION_C_SYNC_STATE_ID:
9046338e712a1120aae9f47f60fbd2905078c0cc2c6b760eaf4a474ff7ed23d4
```

The v1 correction's post-state capsule and report remain unchanged:

| Artifact | Path | SHA256 |
|---|---|---|
| Sync Correction v1 | `docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-OPTION-C-SYNC-CORRECTION-v1.md` | `bc1220c4a8e4847c582a780311e4cf5591377e48d699ae5f4a88ba354743f939` |
| Canonical capsule | `D:/documents/planning-lite-sync/PL-SYNC-CAPSULE-after-change3-option-c-owner-decision-canonical-v1.json` | `8ac9247c0a16a72dc81b7a4d31976a1f756b8d6f025c996579850cb9fbff8307` |
| Reconciliation report | `D:/documents/planning-lite-sync/CHANGE_3_OPTION_C_TRANSITION_SYNC_RECONCILIATION_V1.md` | `d405cb33ac5aba3756f93fe86f6ae7451e2b6dde15bfc674378f22ffd65fd04e` |

## Accepted bounded byte-change proof

The preserved reconciliation report proves that the historical Option C
materialization changed exactly these three repository paths:

```text
docs/design/project-spine/CURRENT.md
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-OPTION-C-OWNER-DECISION-v1.md
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v1.md
```

The owner-decision checkpoint and v1 Amendment were absent at entry and
present at exit. The entry and exit hashes of all 30 pre-existing dirty paths
outside those authorized paths match. The six-file corrective candidate,
source, tests, prior Definition, prior Plan, prior review checkpoints,
Roadmap, and unrelated dirt remained unchanged. The unrelated partition had
no actual byte drift. This v2 note accepts that bounded byte-change proof; it
does not recalculate or invent historical entry partition IDs.

```text
OPTION_C_SEMANTIC_DECISION:
SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT / VALID AND UNCHANGED

HISTORICAL_OWNER_DECISION_FILE:
UNCHANGED

HISTORICAL_SYNC_CORRECTION_V1:
UNCHANGED

IMPLEMENTATION_AUTHORIZED:
NO
09_G_STARTED:
NO
```

The next permitted gate remains
`OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V1`.
