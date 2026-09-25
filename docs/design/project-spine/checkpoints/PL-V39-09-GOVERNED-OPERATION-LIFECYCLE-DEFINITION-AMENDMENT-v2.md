# PL-V39-09 Governed Operation Lifecycle - Definition Amendment v2

Status: `PROPOSED_FOR_OWNER_REVIEW`

## 1. Amendment Identity

```text
AMENDMENT_ID: PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-002
CHANGE_ID: CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
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
| predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CHANGE-DEFINITION-v1.md` | `56DFD7C6B7610262A1DD61BCE7771B320F645DAB901EC90DB6B3B3685815611B` |
| approved Amendment v1 | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v1.md` | `2C5FFB3D1902424ACBCCA41505CF5113E6C7365AD632831B80C859795B249DA6` |
| Amendment v1 Activation | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v1.md` | `DA55C416AFCC4933D05F2459773C56CAA10C639242AA71D1040A7CE9C671E84B` |
| coordinated Executor Amendment v2 | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v2.md` | `PROPOSED_IN_THIS_GATE` |
| shaping authority | `.local/work/experiments/PL09_RUNRECEIPT_V2_DEPENDENT_EXECUTOR_LIFECYCLE_DEFINITION_AMENDMENT_SHAPING.md` | `A626164475296704EB1E81B5FC9E80EB6CA9CE83E63D3043CFCB6980F94C7371` |
| approved RunReceipt prerequisite | `docs/design/project-spine/checkpoints/PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-CHANGE-DEFINITION-v1.md` | `9B55A79681B9C3151BD698B6ED60BC7BDA87A5C263E562C7918CD7A5D81CB71D` |
| RunReceipt prerequisite Activation | `docs/design/project-spine/checkpoints/PL-V39-09-RUNRECEIPT-ATTEMPT-INVOCATION-BINDING-DEFINITION-ACTIVATION-v1.md` | `210A5D7F6C61353B559C6D207796EB4AABF44AE760A18ABF07343813A93E8969` |

The effective authority before this proposed amendment is:

```text
PREDECESSOR_DEFINITION
+
APPROVED_LIFECYCLE_AMENDMENT_V1
=
EFFECTIVE_LIFECYCLE_DEFINITION_BEFORE_V2
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

The effective Lifecycle Definition already requires receipt evidence before
Attempt terminalization and PL08 evaluation. Its v1 wording does not yet bind
that evidence to the exact Attempt and exact governed invocation across the
Pattern-B reentrant boundary, and it states that no RunReceipt schema change is
required.

The active prerequisite resolves only that missing provenance edge. This
Amendment v2 makes the receipt gate identity-bound while preserving the
Lifecycle's existing sequencing, owner UX, status, metrics, PL08, and
authority boundaries.

## 5. Exact Semantic Delta

Governed completion requires all of the following before Attempt
terminalization:

```text
authoritative Attempt
+ exact canonical GovernedExecutionEnvelopeV1
+ verified execution_invocation_id
+ GovernedExecutionResultV1(attempt_id, execution_invocation_id)
+ identity-bound RunReceipt v2
```

The normative collection order is:

```text
1. Executor validates completion.
2. GovernedExecutionResultV1 is produced.
3. Lifecycle obtains the exact authoritative IN_FLIGHT Attempt.
4. Lifecycle recomputes and verifies execution_invocation_id from the exact canonical envelope.
5. Lifecycle checks result identity against the Attempt and invocation.
6. Lifecycle supplies authoritative attempt_id and execution_invocation_id as governed collection context.
7. Telemetry-owned governed collector injects both identities.
8. Collector validates RunReceipt v2.
9. Collector appends through existing telemetry storage.
10. Exact stored receipt is read back.
11. Lifecycle verifies exact receipt identity and result/receipt consistency.
12. Only then may Attempt terminalization proceed.
```

## 6. Preserved Semantics

```text
GOVERNED_OPERATION_LIFECYCLE_RUNTIME_MODEL: AGENT_DRIVEN_REENTRANT_BOUNDED_LIFECYCLE
RUNRECEIPT_REQUIRED_BEFORE_ATTEMPT_TERMINALIZATION: YES
RUNRECEIPT_REQUIRED_BEFORE_PL08_EVALUATION: YES
TELEMETRY_OWNER: src/planning_lite/telemetry.py
PL08_IS_EVALUATOR_NOT_PUMP: YES
PRE_FINAL_IDENTITY_BOUND_RECEIPT_FEASIBLE: YES
RUNRECEIPT_IDENTITY_CHANGE_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: YES
CHANGE_MERGE_REQUIRED: NO
PERSISTENT_LIFECYCLE_STATE: NO
ATTEMPT_RUNTIME_AMENDMENT_REQUIRED: NO
```

The Lifecycle remains sequencing and coordination authority. It does not
become telemetry storage authority, write telemetry JSONL directly, create a
second lifecycle identity, invoke a host callback, or select a next gate.

## 7. Authority Boundary

| Concern | Authority | Effective responsibility |
| --- | --- | --- |
| Attempt occurrence and state | Attempt Runtime | exact Attempt lookup, claim, state, and terminalization |
| envelope, invocation identity, typed completion result | Executor | validate and return exact result facts |
| sequencing and identity coordination | Governed Operation Lifecycle | order completion, receipt readback, and terminalization |
| RunReceipt v1/v2 validation, injection, storage/readback | `src/planning_lite/telemetry.py` | governed identity injection and exact persistence/readback |
| evaluation | PL08 | evaluation only |
| current position and next gate | Project Spine / owner | authoritative state and next action |
| execution operator and call sequence | Sidebar agent | performs authorized work; no authority transfer |

```text
AUTHORITY_TRANSFER: NONE
```

## 8. AC Delta

Exactly six additive Amendment v2 acceptance criteria are proposed:

```text
AC-L2-01 V2_ONLY_GOVERNED_TERMINALIZATION:
Governed terminalization accepts only RunReceipt v2; a valid v1 receipt may
remain general telemetry but is not a governed fallback.

AC-L2-02 AUTHORITATIVE_IDENTITY_INJECTION:
Lifecycle supplies the authoritative attempt_id and verified
execution_invocation_id as separate context to the telemetry-owned governed
collector; external identity cannot override them.

AC-L2-03 EXACT_SAME_ATTEMPT:
The governed receipt has schema_version 2 and
receipt.attempt_id == authoritative_attempt.attempt_id.

AC-L2-04 EXACT_SAME_INVOCATION:
The governed receipt has
receipt.execution_invocation_id == the recomputed identity of the exact
canonical GovernedExecutionEnvelopeV1.

AC-L2-05_EXACT_READBACK_AND_CONSISTENCY:
Existing telemetry append is followed by exact stored readback, and the
Lifecycle verifies receipt identity against both the authoritative Attempt and
GovernedExecutionResultV1.

AC-L2-06_TERMINALIZATION_ORDER_AND_SUBSTITUTION_FAILURE:
Cross-Attempt, cross-invocation, legacy-v1, external-identity, latest/time/task,
and pre-readback substitutions fail closed before Attempt terminalization.
```

```text
LIFECYCLE_AMENDMENT_AC_DELTA_COUNT: 6
```

Unaffected predecessor and Amendment v1 acceptance criteria are not duplicated.

## 9. CC Delta

Exactly four additive Amendment v2 closure criteria are proposed:

```text
CC-L2-01 INTEGRATED_IDENTITY_BOUND_PATH:
Real integrated completion proof uses the Executor result, telemetry-owned v2
collection, exact readback, and the required terminalization order.

CC-L2-02 CROSS_ATTEMPT_FAILURE:
Attempt B receipt evidence fails closed when consumed for Attempt A.

CC-L2-03 CROSS_INVOCATION_FAILURE:
Attempt A / invocation I2 receipt evidence fails closed when completing Attempt
A / invocation I1.

CC-L2-04 NO_FALSE_RECEIPT_CLOSURE:
Schema compatibility, a manually authored v2 receipt, valid v1 telemetry,
external identity, fuzzy matching, direct storage, or pre-readback
terminalization cannot establish Lifecycle closure.
```

```text
LIFECYCLE_AMENDMENT_CC_DELTA_COUNT: 4
RUNRECEIPT_IDENTITY_CHANGE_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: YES
```

The prerequisite closure remains independent; Lifecycle closure still requires
the full integrated Lifecycle proof and separate authorization.

## 10. No-False-Done Conditions

The proposed amendment is not satisfied by:

- a structurally valid v1 receipt used for governed terminalization;
- a v2 receipt without exact Attempt equality;
- a v2 receipt without exact invocation equality;
- result identity differing from receipt identity;
- latest, timestamp, text, task-only, or agent-memory association;
- external identity overriding Planning Lite authority context;
- terminalization before exact readback;
- schema constants, a manually authored receipt, or storage existence without
  the real integrated path.

## 11. Downstream Dependency

The Lifecycle consumes the proposed Executor Amendment v2 result contract:

```text
GovernedExecutionResultV1(attempt_id, execution_invocation_id)
-> authoritative Attempt and canonical envelope verification
-> telemetry-owned RunReceipt v2 collection context
-> exact readback
-> Attempt terminalization
-> PL08 evaluation and authoritative continuation
```

```text
EXECUTOR_AMENDMENT_V2:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v2.md
CHANGE_MERGE_REQUIRED: NO
DEPENDENCY_GOVERNANCE_ORDER: B
```

## 12. Explicit Non-Goals

This amendment does not include:

- RunReceipt schema or collector implementation;
- direct telemetry persistence by Lifecycle;
- Executor implementation;
- status implementation or owner intent-routing changes;
- Pattern-B redesign, Attempt Runtime mutation, or PL08 authority change;
- Change 2 or Change 3;
- hooks, callback infrastructure, or automatic completion;
- Lifecycle Plan correction or Formal Readiness;
- source, test, template, script, CURRENT.md, or Roadmap mutation.

## 13. Activation / Approval Boundary

```text
STATUS: PROPOSED_FOR_OWNER_REVIEW
APPROVAL: NO
ACTIVATION: NO
IMPLEMENTATION_AUTHORIZATION: NO
FORMAL_READINESS: NOT_RUN
LIFECYCLE_AMENDMENT_V2_ACTIVATION_CREATED: NO
CURRENT_MUTATION: NO
ROADMAP_MUTATION: NO
SOURCE_MUTATIONS: 0
TEST_MUTATIONS: 0
OWNER_UX_CHANGED: NO
DEPTH_METRIC_PLAN_FIX: DISPLAY_UNAVAILABLE
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
SHAPING_TO_LIFECYCLE_AMENDMENT_FIDELITY: PASS
RUNRECEIPT_REQUIRED_BEFORE_EXECUTOR_BINDING_RESULT: NO
RUNRECEIPT_REQUIRED_BEFORE_ATTEMPT_TERMINALIZATION: YES
RUNRECEIPT_REQUIRED_BEFORE_PL08_EVALUATION: YES
EXECUTOR_RESULT_IDENTITY_FIELDS: attempt_id; execution_invocation_id
EXECUTOR_OWNS_RUNRECEIPT_COLLECTION: NO
EXECUTOR_OWNS_RUNRECEIPT_STORAGE: NO
GOVERNED_OPERATION_ACCEPTS_LEGACY_UNBOUND_RECEIPT: NO
GOVERNED_IDENTITY_EXTERNAL_INPUT_TRUSTED: NO
TELEMETRY_OWNER: src/planning_lite/telemetry.py
AUTHORITY_TRANSFER: NONE
NEW_PERSISTENCE: NO
PRE_FINAL_IDENTITY_BOUND_RECEIPT_FEASIBLE: YES
OWNER_UX_CHANGED: NO
CHANGE_2: BLOCKED / VALID / PAUSED
CHANGE_3: NOT_ABSORBED
DEPTH_METRIC_PLAN_FIX: DISPLAY_UNAVAILABLE
EXECUTOR_AMENDMENT_AC_DELTA_COUNT: 3
EXECUTOR_AMENDMENT_CC_DELTA_COUNT: 3
LIFECYCLE_AMENDMENT_AC_DELTA_COUNT: 6
LIFECYCLE_AMENDMENT_CC_DELTA_COUNT: 4
SHAPING_TO_LIFECYCLE_AMENDMENT_FIDELITY: PASS
LIFECYCLE_AMENDMENT_V2_ACTIVATION_CREATED: NO
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
