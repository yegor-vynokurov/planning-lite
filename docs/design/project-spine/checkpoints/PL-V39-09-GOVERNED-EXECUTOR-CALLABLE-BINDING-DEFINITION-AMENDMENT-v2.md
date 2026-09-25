# PL-V39-09 Governed Executor Callable Binding - Definition Amendment v2

Status: `PROPOSED_FOR_OWNER_REVIEW`

## 1. Amendment Identity

```text
AMENDMENT_ID: PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-002
CHANGE_ID: CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001
CLASSIFICATION: MINOR DEPENDENT DEFINITION AMENDMENT
PREPARATION_GATE: OWNER_AUTHORIZATION_PL09_RUNRECEIPT_V2_DEPENDENT_EXECUTOR_LIFECYCLE_DEFINITION_AMENDMENT_PREPARATION
APPROVAL: NO
ACTIVATION: NO
IMPLEMENTATION_AUTHORIZATION: NO
FORMAL_READINESS: NOT_RUN
```

This is an additive proposed amendment. It is not an approval, Activation,
Implementation Plan, implementation authorization, or closure record.

## 2. Bound Effective Predecessor Authority

| Authority | Path | SHA-256 |
| --- | --- | --- |
| predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md` | `127F19F505527B622BF3F45D6AA83D432B8F5BE93BD5856CE516C4CEE34BE332` |
| approved Amendment v1 | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v1.md` | `AC012052CCCE524FD9770EEEF94D87181C320ABE0D863C2DC930928740F9B886` |
| Amendment v1 Activation | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v1.md` | `59797EFD9F2FDDA8E7A1B4A478F7985A8E43C66956F5BFBD3420F0F7531511D4` |
| shaping authority | `.local/work/experiments/PL09_RUNRECEIPT_V2_DEPENDENT_EXECUTOR_LIFECYCLE_DEFINITION_AMENDMENT_SHAPING.md` | `A626164475296704EB1E81B5FC9E80EB6CA9CE83E63D3043CFCB6980F94C7371` |
| approved RunReceipt prerequisite | `docs/design/project-spine/checkpoints/PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-CHANGE-DEFINITION-v1.md` | `9B55A79681B9C3151BD698B6ED60BC7BDA87A5C263E562C7918CD7A5D81CB71D` |
| RunReceipt prerequisite Activation | `docs/design/project-spine/checkpoints/PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-DEFINITION-ACTIVATION-v1.md` | `210A5D7F6C61353B559C6D207796EB4AABF44AE760A18ABF07343813A93E8969` |

The effective authority before this proposed amendment is:

```text
PREDECESSOR_DEFINITION
+
APPROVED_EXECUTOR_AMENDMENT_V1
=
EFFECTIVE_EXECUTOR_DEFINITION_BEFORE_V2
```

After separate owner approval and Activation, this proposed record would be
added to that effective authority. Unchanged predecessor and Amendment v1
clauses remain effective.

## 3. Bound RunReceipt v2 Prerequisite

The canonical owner of the dependent receipt contract is the approved and
active RunReceipt prerequisite Change:

```text
PREREQUISITE_CHANGE: CHG-PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-001
PREREQUISITE_DEFINITION: APPROVED / ACTIVE
PREREQUISITE_IMPLEMENTATION: NOT_YET_AUTHORIZED
RUNRECEIPT_SCHEMA_DECISION: V2
V2_REQUIRED_FIELDS: attempt_id; execution_invocation_id
GOVERNED_OPERATION_ACCEPTS_LEGACY_UNBOUND_RECEIPT: NO
GOVERNED_IDENTITY_EXTERNAL_INPUT_TRUSTED: NO
NEW_PERSISTENCE: NO
```

This amendment references the prerequisite for the v2 schema, identity
injection, validation, append, and exact readback rules. It does not duplicate
the full RunReceipt v2 Definition and does not claim its implementation exists.

## 4. Reason for Amendment

The effective Executor Definition already establishes the canonical envelope,
deterministic invocation identity, and typed completion result. Its remaining
v1 receipt wording treats same-invocation receipt association as sufficient and
states that the RunReceipt schema is unchanged. The active prerequisite now
provides the narrower durable evidence contract required across Pattern-B
reentrant boundaries.

This Amendment v2 therefore makes the result identity explicit and binds the
downstream Lifecycle receipt context without moving receipt collection or
storage into the Executor.

## 5. Exact Semantic Delta

The proposed amendment adds only these dependent semantics:

```text
EXECUTOR_ROLE: TYPED_EXECUTION_CONTRACT
EXECUTOR_RESULT_IDENTITY_FIELDS: attempt_id; execution_invocation_id
RUNRECEIPT_REQUIRED_BEFORE_EXECUTOR_BINDING_RESULT: NO
RECEIPT_MISSING_AT_EXECUTOR_RESULT_STAGE: NOT_AN_EXECUTOR_RESULT_FAILURE
EXECUTOR_OWNS_RUNRECEIPT_COLLECTION: NO
EXECUTOR_OWNS_RUNRECEIPT_STORAGE: NO
EXECUTOR_OWNS_RECEIPT_IDENTITY_INJECTION: NO
```

The normative sequence is:

```text
GovernedExecutionEnvelopeV1
-> validate_governed_completion(...)
-> GovernedExecutionResultV1(attempt_id, execution_invocation_id)
-> Lifecycle-controlled governed receipt collection
-> RunReceipt v2
```

`GovernedExecutionResultV1.attempt_id` is the exact Attempt identity associated
with the validated execution. `GovernedExecutionResultV1.execution_invocation_id`
is the exact deterministic identity associated with the validated canonical
envelope. No `receipt_id` is required merely to produce the Executor result.

## 6. Preserved Semantics

```text
EXECUTION_INVOCATION_ID:
DOMAIN-SEPARATED SHA-256 OF VERSIONED CANONICAL GovernedExecutionEnvelopeV1
DETERMINISTIC: YES
CONTENT_BOUND: YES
RECOMPUTABLE: YES
PERSISTED_BY_EXECUTOR: NO
IS_SECOND_ATTEMPT_IDENTITY: NO
NEW_EXECUTOR_PERSISTENCE: NO
PATTERN_A: REJECTED
PATTERN_B: SELECTED
SIDEBAR_CALLBACK_REQUIRED: NO
NORMAL_OWNER_UX_REQUIRES_HOOKS: NO
EXECUTOR_BINDING_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: NO
```

The Executor remains responsible for canonical envelope construction,
preparation validation, completion validation, invocation identity, and the
typed result. It does not invoke the sidebar, sequence cross-turn work, claim
or terminalize Attempts, evaluate PL08, or select a next gate.

## 7. Authority Boundary

| Concern | Authority | Executor responsibility |
| --- | --- | --- |
| Attempt occurrence and state | Attempt Runtime | consume exact Attempt identity; never claim or terminalize |
| envelope and invocation identity | Executor | construct, validate, and recompute |
| typed completion result | Executor | return exact identity-bearing result |
| cross-turn sequencing | Governed Operation Lifecycle | outside Executor |
| RunReceipt v1/v2 validation and storage | `src/planning_lite/telemetry.py` | no transfer |
| governed receipt coordination | Lifecycle | downstream of Executor result |
| evaluation | PL08 | no transfer |
| next gate | Project Spine / owner | no transfer |
| sidebar execution | Sidebar agent | external execution operator |

```text
AUTHORITY_TRANSFER: NONE
```

## 8. AC Delta

Exactly three additive Amendment v2 acceptance criteria are proposed:

```text
AC-E2-01 DETERMINISTIC_RECEIPT_BINDING_ANCHOR:
The exact recomputable execution_invocation_id derived from the versioned
canonical GovernedExecutionEnvelopeV1 is the Executor-side anchor for later
RunReceipt v2 binding; it is not randomly generated or guessed.

AC-E2-02 EXACT_RESULT_IDENTITY:
GovernedExecutionResultV1 exposes the exact attempt_id and
execution_invocation_id associated with the validated Attempt and envelope.

AC-E2-03 DOWNSTREAM_RECEIPT_BOUNDARY:
Executor completion produces the typed result before receipt collection and
does not collect, persist, inject, or store RunReceipt v2 evidence.
```

```text
EXECUTOR_AMENDMENT_AC_DELTA_COUNT: 3
```

Unaffected predecessor and Amendment v1 acceptance criteria are not duplicated.

## 9. CC Delta

Exactly three additive Amendment v2 closure criteria are proposed:

```text
CC-E2-01 RESULT_IDENTITY_PROOF:
Integrated completion proof shows exact result attempt_id and recomputed
execution_invocation_id for the canonical envelope.

CC-E2-02 IDENTITY_MISMATCH_FAILURE:
Negative proof rejects cross-Attempt, envelope, invocation, and result-identity
substitution before any downstream receipt context is accepted.

CC-E2-03 NO_EXECUTOR_RECEIPT_AUTHORITY:
Static and integration proof shows no Executor receipt collection, receipt
identity injection, receipt persistence, or independent Executor closure.
Executor closure still requires integrated Executor plus Lifecycle proof.
```

```text
EXECUTOR_AMENDMENT_CC_DELTA_COUNT: 3
EXECUTOR_BINDING_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: NO
RUNRECEIPT_IDENTITY_CHANGE_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: YES
```

The last line concerns the separate prerequisite Change only; it does not make
the Executor independently closable.

## 10. No-False-Done Conditions

The proposed amendment is not satisfied by:

- a random, guessed, or non-recomputable invocation identity;
- a result that omits either exact identity field;
- a receipt being required before the Executor result exists;
- receipt collection or persistence moved into the Executor;
- an isolated helper without integrated Lifecycle evidence continuity;
- a schema constant, manually authored receipt, or unit-only identity proof;
- independent Executor closure before integrated Lifecycle implementation.

## 11. Downstream Dependency

The coordinated Lifecycle Amendment v2 consumes this result contract:

```text
GovernedExecutionResultV1(attempt_id, execution_invocation_id)
-> Lifecycle authoritative Attempt and envelope verification
-> telemetry-owned RunReceipt v2 collection context
```

```text
LIFECYCLE_AMENDMENT_V2:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v2.md
CHANGE_MERGE_REQUIRED: NO
DEPENDENCY_GOVERNANCE_ORDER: B
```

The RunReceipt identity prerequisite may close independently before Lifecycle
implementation, but dependent Definition approval and Activation must precede
prerequisite Implementation Planning.

## 12. Explicit Non-Goals

This amendment does not include:

- telemetry schema or collector implementation;
- RunReceipt collection or persistence;
- Attempt Runtime mutation;
- Lifecycle implementation or Plan correction;
- owner UX, status, routing, or completion-intent changes;
- PL08 implementation or evaluation changes;
- Change 2 or Change 3;
- hooks, callbacks, sidebar invocation, or private IPC;
- source, test, template, script, CURRENT.md, or Roadmap mutation.

## 13. Activation / Approval Boundary

```text
STATUS: PROPOSED_FOR_OWNER_REVIEW
APPROVAL: NO
ACTIVATION: NO
IMPLEMENTATION_AUTHORIZATION: NO
FORMAL_READINESS: NOT_RUN
EXECUTOR_AMENDMENT_V2_ACTIVATION_CREATED: NO
CURRENT_MUTATION: NO
ROADMAP_MUTATION: NO
SOURCE_MUTATIONS: 0
TEST_MUTATIONS: 0
```

Approval and Activation require a later clean independent review of both
proposed Amendment v2 artifacts followed by the separate owner gate. No
Activation record is created here.

## 14. Next Gate

```text
NEXT_SINGLE_GATE: FRESH_INDEPENDENT_REVIEW_PL09_RUNRECEIPT_V2_DEPENDENT_EXECUTOR_LIFECYCLE_DEFINITION_AMENDMENTS
REVIEWER: GPT-5.6 Luna / Extra High
```

The next gate is read-only and must review both proposed amendments together.

## Terminal Receipt

```text
PL09_RUNRECEIPT_V2_DEPENDENT_EXECUTOR_LIFECYCLE_DEFINITION_AMENDMENT_PREPARATION

OVERALL: PASS_RUNRECEIPT_V2_DEPENDENT_PROPOSED_AMENDMENTS_PREPARED
REASONER: GPT-5.6_LUNA_EXTRA_HIGH
SHAPING_SHA256: A626164475296704EB1E81B5FC9E80EB6CA9CE83E63D3043CFCB6980F94C7371
AMENDMENT_SHA256: COMPUTED_AFTER_FINAL_WRITE_AND_REPORTED_IN_TERMINAL_RECEIPT
AMENDMENT_STATUS: PROPOSED_FOR_OWNER_REVIEW
EXECUTOR_AMENDMENT_REMAINS_MINOR: YES
LIFECYCLE_AMENDMENT_REMAINS_MINOR: YES
SHAPING_TO_EXECUTOR_AMENDMENT_FIDELITY: PASS
EXECUTOR_RESULT_IDENTITY_FIELDS: attempt_id; execution_invocation_id
RUNRECEIPT_REQUIRED_BEFORE_EXECUTOR_BINDING_RESULT: NO
EXECUTOR_OWNS_RUNRECEIPT_COLLECTION: NO
EXECUTOR_OWNS_RUNRECEIPT_STORAGE: NO
GOVERNED_OPERATION_ACCEPTS_LEGACY_UNBOUND_RECEIPT: NO
GOVERNED_IDENTITY_EXTERNAL_INPUT_TRUSTED: NO
AUTHORITY_TRANSFER: NONE
NEW_PERSISTENCE: NO
EXECUTOR_AMENDMENT_REMAINS_MINOR: YES
EXECUTOR_AMENDMENT_AC_DELTA_COUNT: 3
EXECUTOR_AMENDMENT_CC_DELTA_COUNT: 3
EXECUTOR_AMENDMENT_V2_ACTIVATION_CREATED: NO
CANONICAL_MUTATION_PATH_COUNT: 2
SOURCE_MUTATIONS: 0
TEST_MUTATIONS: 0
CURRENT_MUTATION: NO
ROADMAP_MUTATION: NO
STAGED_PATHS: 0
COMMIT: NO
PUSH: NO
NEXT_SINGLE_GATE: FRESH_INDEPENDENT_REVIEW_PL09_RUNRECEIPT_V2_DEPENDENT_EXECUTOR_LIFECYCLE_DEFINITION_AMENDMENTS
```

The ordinary full-file SHA-256 is reported after final write to avoid a
self-referential digest field.
