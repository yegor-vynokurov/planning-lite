# PL-V39-09 Governed Executor Callable Binding — Definition Amendment v1

Status: `APPROVED / CANONICAL DEFINITION AMENDMENT`

## 1. Amendment identity

```text
AMENDMENT_ID: PL09_PATTERN_B_EXECUTOR_CALLABLE_BINDING_DEFINITION_AMENDMENT-001
CHANGE_ID: CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001
APPROVAL_GATE: OWNER_APPROVAL_PL09_PATTERN_B_EXECUTOR_AND_LIFECYCLE_DEFINITION_AMENDMENTS
OWNER_DECISION: APPROVE_AND_ACTIVATE_PL09_PATTERN_B_EXECUTOR_AND_LIFECYCLE_DEFINITION_AMENDMENTS
APPROVAL_DATE: 2026-09-22
APPROVAL_AUTHORITY: USER / EXPLICIT / CURRENT OWNER GATE
DEFINITION_STATUS: APPROVED / CANONICAL DEFINITION AMENDMENT
IMPLEMENTATION_AUTHORIZATION: NO
FORMAL_READINESS: NOT_RUN
COMMIT_TAG_PUSH_RELEASE: NO
```

This amendment is additive authority. The effective Definition is:

```text
PREDECESSOR_DEFINITION
+
APPROVED_EXECUTOR_DEFINITION_AMENDMENT
=
EFFECTIVE_EXECUTOR_DEFINITION
```

Unchanged predecessor clauses remain effective. Only the semantic surfaces
explicitly replaced below are superseded. This record does not authorize
Implementation Planning by itself, source or test mutation, runtime execution,
staging, commit, push, release, hook cleanup, or Lifecycle implementation.

## 2. Bound authority and lineage

| Authority | Path / identity | SHA-256 |
| --- | --- | --- |
| predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md` | `127F19F505527B622BF3F45D6AA83D432B8F5BE93BD5856CE516C4CEE34BE332` |
| predecessor Definition Activation | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-ACTIVATION-v1.md` | `2CDE29CA69D29FF3FC327B82C05EAF6A3CCB54143F1B30B8953B2FC07BFAD4C7` |
| approved shaping authority | `.local/work/experiments/PL09_PATTERN_B_EXECUTOR_AND_LIFECYCLE_DEFINITION_AMENDMENT_SHAPING.md` | `55B256F7A4AC4AF82B323B9944DAEF4D0C3B81DC05156434F7506C8AAAA0AAD6` |
| architecture adjudication | `.local/work/experiments/PL09_GOVERNED_EXECUTOR_PATTERN_B_STOP_HOOK_HOST_UNAVAILABLE_ADJUDICATION.md` | `C0C9BE2D05089C2817EBE684A0F62CC73F4E9E6236902464D409FCD3608702B7` |
| entry HEAD | Git | `e5cf0eb42509a4193550f77a0a6634cca556e91c` |

The architecture adjudication verdict is
`PASS_SELECT_REENTRANT_LIFECYCLE_WITH_EXECUTOR_CONTRACT_AMENDMENT`. The shaping
verdict is `PASS_PATTERN_B_EXECUTOR_AND_LIFECYCLE_AMENDMENTS_READY`, with zero
unbound architecture choices and zero unbound material semantic choices.

## 3. Reason for amendment

Empirical host discovery disproved the predecessor assumption that Planning
Lite can synchronously invoke the current VS Code sidebar agent:

```text
PREDECESSOR_ASSUMPTION: PLANNING_LITE -> SYNCHRONOUSLY_INVOKE_CURRENT_VS_CODE_SIDEBAR_AGENT
EMPIRICAL_RESULT: CURRENT_IDE_HOST_CALLBACK_SEAM_NOT_AVAILABLE
PATTERN_A: REJECTED
PATTERN_B: SELECTED
```

The supported architecture is an external sidebar execution operator paired
with Planning Lite as the typed execution and lifecycle authority. The
amendment preserves the existing authority boundaries while removing the false
host-invocation meaning from the Executor Binding.

## 4. Amended Executor role

```text
EXECUTOR_ROLE: TYPED_EXECUTION_CONTRACT
```

The Executor Binding owns:

- exact preparation validation;
- exact `AttemptRecordV1.attempt_id` identity continuity;
- immutable `OperationGuidance` continuity;
- bounded payload identity and binding validation;
- authority provenance validation without granting authority;
- canonical immutable execution-envelope construction;
- deterministic execution invocation identity;
- structured machine completion validation;
- a fail-closed `GovernedExecutionResultV1` contract.

The Executor does not own:

- sidebar-agent invocation;
- host callbacks, notify, Stop hooks, hidden sessions, or private IPC;
- cross-turn Lifecycle sequencing;
- persistent orchestration, a registry, queue, worker, or scheduler;
- RunReceipt production, storage, or telemetry authority;
- Attempt claim, terminalization, or recovery;
- PL08 evaluation or handoff authority;
- next-gate selection.

```text
EXECUTOR_OWNS_ATTEMPT_SOURCE: NO
EXECUTOR_OWNS_ATTEMPT_CLAIM: NO
EXECUTOR_OWNS_ATTEMPT_RUNTIME_STATE: NO
EXECUTOR_OWNS_LIFECYCLE: NO
EXECUTOR_OWNS_PL08_HANDOFF: NO
TELEMETRY_AUTHORITY_TRANSFER: NO
```

## 5. Amended internal contract

The canonical amended contract is:

```text
prepare_governed_operation(...)
-> GovernedExecutionEnvelopeV1

validate_governed_completion(...)
-> GovernedExecutionResultV1
```

`invoke_governed_operation(...)` is not the semantic center of the effective
Definition. Its predecessor host-invocation semantics are superseded:

```text
INVOKE_GOVERNED_OPERATION_PREDECESSOR_SEMANTICS: SUPERSEDED
EXECUTOR_PUBLIC_SYMBOL_DISPOSITION: REPLACE
```

The exact private Python layout, exception mechanics, import wiring, and
ordinary adapter mechanics remain Implementation Planning details. They may
not reintroduce host-invocation ownership or a second authority model.

## 6. Execution envelope and invocation identity

The immutable `GovernedExecutionEnvelopeV1` binds the exact Attempt, selected
Guidance, authority provenance, bounded task payload, contract version, and
execution identity inputs. It grants no authority beyond the already-authorized
current state.

```text
EXECUTION_INVOCATION_ID_MODEL: DOMAIN-SEPARATED SHA-256 OF VERSIONED CANONICAL EXECUTION ENVELOPE
EXECUTION_INVOCATION_ID: DETERMINISTIC / CONTENT-BOUND / RECOMPUTABLE
IS_SECOND_ATTEMPT_IDENTITY: NO
NEW_EXECUTOR_PERSISTENCE: NO
```

The invocation identity is ephemeral, scoped to the bounded contract, and
checked again during completion. No registry, pending-operation store, executor
database, worker, queue, scheduler, daemon, or persistent process is added.

## 7. Completion and receipt boundary

The Executor validates the exact envelope and structured completion facts. It
does not close the Lifecycle or terminalize an Attempt.

```text
RUNRECEIPT_REQUIRED_BEFORE_EXECUTOR_BINDING_RESULT: NO
RECEIPT_OWNER: EXISTING_TELEMETRY_OWNER
RUNRECEIPT_SCHEMA_CHANGE_REQUIRED: NO
```

Receipt production, validation, append-only storage, and stream consistency
remain outside the Executor. The Lifecycle coordinates the later exact receipt
handoff and terminalization order. No post-hoc latest, timestamp, task-only,
fuzzy, or text matching is allowed.

```text
EXECUTOR_BINDING_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: NO
EXECUTOR_CLOSURE_REQUIRES: INTEGRATED_EXECUTOR_AND_LIFECYCLE_PROOF
```

This explicitly replaces the predecessor independent-closure assumption.

## 8. Preserved authority matrix

| Concern | Authority | Executor boundary |
| --- | --- | --- |
| route and Guidance | PL07 | consumes exact immutable projection; never reselects |
| Attempt identity/claim/state | Attempt Runtime | consumes exact Attempt ID; never claims or terminalizes |
| typed preparation/completion | Executor Binding | sole owner of this contract |
| cross-turn sequencing | Governed Operation Lifecycle | outside Executor |
| RunReceipt | existing telemetry owner | no transfer |
| evaluation | PL08 | no transfer |
| current state and next gate | Project Spine / owner-authorized lifecycle | no transfer |
| sidebar execution | current sidebar agent | external operator, not Executor-owned host invocation |

`AUTHORITY_TRANSFER: NONE` except the explicitly documented semantic removal of
the false predecessor host-invocation responsibility.

## 9. Effective interaction contract

The effective sequence is:

```text
authoritative current state + exact Attempt + Guidance
-> prepare_governed_operation
-> immutable GovernedExecutionEnvelopeV1
-> sidebar agent performs the authorized work
-> validate_governed_completion
-> GovernedExecutionResultV1
-> Lifecycle receipt/evidence coordination
```

The sidebar agent is an execution operator and call-sequence driver. It is not
execution authority, Lifecycle-rule authority, or next-gate authority. Owner
chat text is not an execution contract or machine authorization.

## 10. Acceptance criteria for later implementation

1. Preparation rejects missing, stale, contradictory, cross-Attempt, or
   unauthorized inputs without creating execution facts.
2. The envelope contains exact Attempt and Guidance continuity and immutable
   bounded payload identity.
3. Invocation identity is the required domain-separated SHA-256 and is
   recomputed during completion.
4. Completion returns a structured typed result or a bounded fail-closed
   failure; it cannot fabricate receipt, result, or Attempt facts.
5. Executor does not select routes, claim Attempts, terminalize Attempts,
   evaluate PL08, store receipts, or choose next gates.
6. No new executor persistence, registry, worker, queue, scheduler, daemon, or
   host-wide bridge is introduced.
7. RunReceipt v1 remains unchanged and telemetry authority remains outside the
   Executor.
8. Executor closure is blocked until integrated Lifecycle proof exists.
9. False-done evidence is rejected when an isolated helper exists without the
   Lifecycle path and exact evidence continuity.
10. Pattern B is preserved and host callbacks/hooks/API fallback are not made a
    production dependency.

## 11. Plan boundary and closure impact

Implementation Planning must still bind the exact live call graph, private
symbols, adapter mechanics, and tests. It must stop for owner adjudication if it
discovers a need for persistent Executor state, a new authority owner, a second
Attempt identity, RunReceipt schema change, callback/private IPC dependency,
host invocation ownership, or independent Executor closure.

The Lifecycle Definition amendment is a material dependency. The Executor
Change remains semantically distinct and is not merged with the Lifecycle Change.

```text
LIFECYCLE_DEFINITION_AMENDMENT: REQUIRED / EFFECTIVE AS COORDINATED RECORD
CHANGE_MERGE_REQUIRED: NO
IMPLEMENTATION: NOT_AUTHORIZED
```

## 12. Boundaries preserved

```text
ATTEMPT_RUNTIME_AMENDMENT_REQUIRED: NO
RUNRECEIPT_SCHEMA_CHANGE_REQUIRED: NO
NORMAL_OWNER_UX_REQUIRES_HOOKS: NO
SIDEBAR_CALLBACK_REQUIRED: NO
CHANGE_2: BLOCKED
MAJOR_PL09_NEXT_SLICE_GATE: PRESERVED / UNCONSUMED
```

The experimental Stop hook has no production role and remains untouched under
this amendment. Cleanup is a separate owner-authorized action. Change 2 and the
PL08 RunReceipt measurement correction remain outside this amendment.

## 13. Activation and next gate

This amendment becomes effective only together with its coordinated Activation
record and the Lifecycle amendment/Activation record. Its effective authority
is the predecessor Definition plus this amendment; unchanged predecessor
clauses remain valid.

```text
EXECUTOR_CHANGE_STATE: DEFINITION_AMENDED / DEPENDENT_ON_LIFECYCLE_IMPLEMENTATION / IMPLEMENTATION_NOT_AUTHORIZED
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_PLANNING_RESUME_PATTERN_B
```

No `CURRENT.md` mutation is required by the existing central-source
Definition/Activation convention.
