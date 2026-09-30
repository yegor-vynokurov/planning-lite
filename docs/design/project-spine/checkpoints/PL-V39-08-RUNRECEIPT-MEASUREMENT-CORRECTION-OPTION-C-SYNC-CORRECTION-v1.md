# PL-V39-08 RunReceipt Measurement Correction - Option C Sync Correction

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: CANONICAL_OPTION_C_SYNC_PARTITION_AND_STATE_ID_CORRECTION
transition_source: AUTHORIZED_GOVERNANCE_CORRECTION
transition_date: 2026-09-28
supersedes: OPTION_C_OWNER_DECISION_CHECKPOINT_STATE_ID_AND_PARTITION_BOOKKEEPING_ONLY

## Scope and preserved decision

This checkpoint supersedes only the repository state-ID and partition
bookkeeping recorded in
`PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-OPTION-C-OWNER-DECISION-v1.md`.
That historical file is not edited. Its entry SHA256 is
`2563bdeba4d3e185a5f89a2d9a54d6697b61b83d1867800b03f921b411765c4d`. The semantic owner decision
`SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT` remains valid and
unchanged. The four accepted external evidence artifact bindings and their
recorded hashes remain valid and unchanged. This correction does not approve the
Definition Amendment v1 or v2, authorize a Plan Amendment or implementation,
change the Option C semantic direction, or modify the corrective candidate.

## Canonical entry state and reconciliation

```text
HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
INDEX_EMPTY: YES
AUTHORITY_STATE_ID: fd6fc9ddaffa8f1d826fdf35b2db5d291a77d0f4ffb02d74a65266959df6360c
CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
UNRELATED_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
SYNC_STATE_ID: 9046338e712a1120aae9f47f60fbd2905078c0cc2c6b760eaf4a474ff7ed23d4
SYNC_RECONCILIATION: PASS
```

Canonical read-only reconciliation artifacts, stored outside the repository:

| Artifact | Path | SHA256 |
|---|---|---|
| Sync capsule | `D:\documents\planning-lite-sync\PL-SYNC-CAPSULE-after-change3-option-c-owner-decision-canonical-v1.json` | `8ac9247c0a16a72dc81b7a4d31976a1f756b8d6f025c996579850cb9fbff8307` |
| Reconciliation report | `D:\documents\planning-lite-sync\CHANGE_3_OPTION_C_TRANSITION_SYNC_RECONCILIATION_V1.md` | `d405cb33ac5aba3756f93fe86f6ae7451e2b6dde15bfc674378f22ffd65fd04e` |

The IDs above are the canonical partition IDs from that capsule and its verified
report. The owner-decision checkpoint's previously recorded bookkeeping is
superseded as follows:

| Historical field | Historical value | Canonical value |
|---|---|---|
| `entry_authority_state_id` | `565ab23ded027f85b3ecb84e327a4a02728e90b631aa5cc9e6fd30679c9ce16f` | `fd6fc9ddaffa8f1d826fdf35b2db5d291a77d0f4ffb02d74a65266959df6360c` |
| `exit_authority_state_id` | `ca23d96a0c8c8d4db43c0abe458fc88eb30e20679a70c4a9afcebf6f346b744b` | `fd6fc9ddaffa8f1d826fdf35b2db5d291a77d0f4ffb02d74a65266959df6360c` |
| `entry_unrelated_dirt_state_id` / `exit_unrelated_dirt_state_id` | `8637ad6c46d5b5e738f1de72256f9c2e78bd53b7ab3de76f55ebf3af089d51fc` | `2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a` |
| `entry_sync_state_id` / `exit_sync_state_id` | `62fef00f78bc1d9d1ff0dcde41661b4249514d47a924ef406e9d41eed363ad08` | `9046338e712a1120aae9f47f60fbd2905078c0cc2c6b760eaf4a474ff7ed23d4` |

The old authority value was a hash of `CURRENT.md` bytes; the old sync value
hashed the four evidence artifact names and hashes; and the old unrelated value
used a different local dirt projection. Those semantics do not identify the
canonical partitions. The canonical authority partition contains 15 paths, the
corrective candidate partition contains six implementation files, and the
unrelated partition contains 12 paths. Their state IDs are the canonical IDs
above.

## Drift adjudication

```text
ACTUAL_UNRELATED_BYTE_DRIFT: NO
CORRECTIVE_CANDIDATE_DRIFT: NO
SOURCE_DRIFT: NO
TEST_DRIFT: NO
ROADMAP_DRIFT: NO
INDEX_DRIFT: NO
```

The corrective candidate state remains
`37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555`. The
accepted external evidence files remain byte-identical to the hashes recorded
in the owner-decision checkpoint. No source, test, Roadmap, candidate, prior
Definition, prior Plan, or historical owner-decision checkpoint bytes were
changed by the reconciliation or this correction. This checkpoint changes only
the current governance record of the canonical partition/state-ID semantics.

## Write boundary and next gate

```text
AUTHORIZED_REPOSITORY_PATHS:
- docs/design/project-spine/CURRENT.md
- docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-RESPONSE-AGGREGATE-DEFINITION-AMENDMENT-REVIEW-v1.md
- docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-OPTION-C-SYNC-CORRECTION-v1.md
- docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v2.md
IMPLEMENTATION_AUTHORIZED: NO
PLAN_AMENDMENT_PREPARED: NO
09_G_STARTED: NO
STAGE: NOT PERFORMED
COMMIT: NOT PERFORMED
PUSH: NOT PERFORMED
```

The next permitted gate remains
`OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_DEFINITION_AMENDMENT_V2`.
