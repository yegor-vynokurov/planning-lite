# PL-V39-09 Governed Operation Lifecycle — Definition Amendment v1

Status: `APPROVED / CANONICAL DEFINITION AMENDMENT`

## 1. Amendment identity

```text
AMENDMENT_ID: PL09_PATTERN_B_GOVERNED_OPERATION_LIFECYCLE_DEFINITION_AMENDMENT-001
CHANGE_ID: CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
APPROVAL_GATE: OWNER_APPROVAL_PL09_PATTERN_B_EXECUTOR_AND_LIFECYCLE_DEFINITION_AMENDMENTS
OWNER_DECISION: APPROVE_AND_ACTIVATE_PL09_PATTERN_B_EXECUTOR_AND_LIFECYCLE_DEFINITION_AMENDMENTS
APPROVAL_DATE: 2026-09-22
APPROVAL_AUTHORITY: USER / EXPLICIT / CURRENT OWNER GATE
DEFINITION_STATUS: APPROVED / CANONICAL DEFINITION AMENDMENT
IMPLEMENTATION_PLANNING: AUTHORIZED_AFTER_BOTH_AMENDMENTS_EFFECTIVE
IMPLEMENTATION_AUTHORIZATION: NO
FORMAL_READINESS: NOT_RUN
COMMIT_TAG_PUSH_RELEASE: NO
```

The effective Lifecycle Definition is:

```text
PREDECESSOR_DEFINITION
+
APPROVED_LIFECYCLE_DEFINITION_AMENDMENT
=
EFFECTIVE_GOVERNED_OPERATION_LIFECYCLE_DEFINITION
```

Unchanged predecessor clauses remain effective. This amendment changes the
runtime, cross-turn completion, owner-intent, and read-only status surfaces
listed below. It does not authorize implementation, source/test mutation,
Formal Readiness, staging, commit, push, release, or hook cleanup.

## 2. Bound authority and lineage

| Authority | Path / identity | SHA-256 |
| --- | --- | --- |
| predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CHANGE-DEFINITION-v1.md` | `56DFD7C6B7610262A1DD61BCE7771B320F645DAB901EC90DB6B3B3685815611B` |
| predecessor Definition Activation | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-ACTIVATION-v1.md` | `F21B8DC151507EB0B937EEFE36CFD35012305808174C3067A4ABC9D0C7C1A53B` |
| coordinated Executor amendment | `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v1.md` | `AC012052CCCE524FD9770EEEF94D87181C320ABE0D863C2DC930928740F9B886` |
| approved shaping authority | `.local/work/experiments/PL09_PATTERN_B_EXECUTOR_AND_LIFECYCLE_DEFINITION_AMENDMENT_SHAPING.md` | `55B256F7A4AC4AF82B323B9944DAEF4D0C3B81DC05156434F7506C8AAAA0AAD6` |
| architecture adjudication | `.local/work/experiments/PL09_GOVERNED_EXECUTOR_PATTERN_B_STOP_HOOK_HOST_UNAVAILABLE_ADJUDICATION.md` | `C0C9BE2D05089C2817EBE684A0F62CC73F4E9E6236902464D409FCD3608702B7` |
| entry HEAD | Git | `e5cf0eb42509a4193550f77a0a6634cca556e91c` |

The shaping and architecture verdicts are respectively
`PASS_PATTERN_B_EXECUTOR_AND_LIFECYCLE_AMENDMENTS_READY` and
`PASS_SELECT_REENTRANT_LIFECYCLE_WITH_EXECUTOR_CONTRACT_AMENDMENT`.

## 3. Amended runtime model

```text
GOVERNED_OPERATION_LIFECYCLE_RUNTIME_MODEL: AGENT_DRIVEN_REENTRANT_BOUNDED_LIFECYCLE
```

Individual Planning Lite transitions remain synchronous and deterministic. One
governed operation may span more than one sidebar-agent interaction. Legal
continuation is reconstructed from authoritative existing state.

The model introduces no persistent Python process, lifecycle database,
orchestration registry, daemon, scheduler, background worker, queue, lease, or
workflow engine.

```text
PERSISTENT_LIFECYCLE_STATE: NO
ATTEMPT_RUNTIME_IN_FLIGHT_SUFFICIENT_FOR_CROSS_TURN_OCCURRENCE: YES
ATTEMPT_RUNTIME_AMENDMENT_REQUIRED: NO
PRIMARY_OCCURRENCE_IDENTITY: AttemptRecordV1.attempt_id
```

Attempt Runtime remains the sole authority for exact Attempt lookup, claim,
occurrence state, normal terminalization, and explicit recovery. The Lifecycle
reconstructs the continuation around the same exact IN_FLIGHT Attempt; it does
not create a second lifecycle identity.

## 4. Sidebar-agent role and authority

```text
SIDEBAR_AGENT_ROLE: EXECUTION_OPERATOR + CALL_SEQUENCE_DRIVER
EXECUTION_AUTHORITY: NO
LIFECYCLE_RULE_AUTHORITY: NO
NEXT_GATE_AUTHORITY: NO
OWNER_DECISION_AUTHORITY_TRANSFER_TO_AGENT: NO
```

The sidebar agent performs the authorized work and calls the explicit machine
completion action. It cannot turn an owner phrase, memory, or successful prose
summary into authorization or terminal state.

## 5. Canonical v1 completion path

The normal pre-final path is:

```text
agent performs authorized work
-> agent gathers available machine result/evidence facts
-> agent invokes Planning Lite completion before human-facing cycle closure
-> Executor validates exact Attempt/envelope/result identity
-> required receipt is validated/read back by existing telemetry ownership
-> Lifecycle terminalizes the exact Attempt
-> PL08 receives evidence and evaluates through its existing authority
-> authoritative continuation/next action is resolved
-> agent returns the final human-facing result
```

```text
PRE_FINAL_COMPLETION: SUPPORTED_V1_PATH
SIDEBAR_CALLBACK_REQUIRED: NO
RUNRECEIPT_REQUIRED_BEFORE_ATTEMPT_TERMINALIZATION: YES
RUNRECEIPT_REQUIRED_BEFORE_PL08_EVALUATION: YES
RECEIPT_ASSOCIATION_OWNER: EXISTING_TELEMETRY_OWNER_WITH_LIFECYCLE_COORDINATION
RUNRECEIPT_SCHEMA_CHANGE_REQUIRED: NO
```

The agent must not announce governed-cycle completion before the machine
completion transition succeeds. Automatic post-turn completion remains
deferred as a future enhancement and is not a v1 correctness dependency.

## 6. Owner completion intent

```text
OWNER_COMPLETION_TRIGGER: FINISH_CURRENT_GOVERNED_CYCLE
KEYWORD_MATCH_ALONE_SUFFICIENT: NO
COMPLETION_TRIGGER_INTENT_REQUIRED: YES
OWNER_COMPLETION_TRIGGER_IS_MACHINE_AUTHORIZATION: NO
OWNER_MANUAL_CLI: NO
RAW_OWNER_CHAT_AS_LIFECYCLE_STATE: NO
```

The sidebar routing layer recognizes a standalone or clearly imperative
cycle-closing intent. Normalized examples include:

```text
итоги
итог
финиш
заверши цикл
заканчиваем цикл
закончим цикл
закрываем цикл
заканчиваем
подытожим
подведём итоги
давай подведём итоги
завершаем
заверши работу
закончим на этом
```

These are examples, not a substring grammar. Incidental, interrogative,
quoted, explanatory, or differently scoped mentions must not trigger completion,
including:

```text
какие итоги исследования?
подытожим аргументы статьи
слово «финиш» здесь звучит странно
как завершить цикл в другой программе?
```

The recognized intent only requests an attempt to perform the legal completion
transition. Actual completion still requires authoritative current state, the
exact IN_FLIGHT Attempt, an allowed next action, required result/evidence facts,
and a valid typed completion contract. If no closable operation exists, the
Lifecycle fails readably and creates no fabricated state.

## 7. Read-only status contract

```text
STATUS_COMMAND: статус
STATUS_ACTION: SHOW_COMPACT_PROJECT_STATUS
STATUS_MUTATION_CAPABILITY: NONE
STATUS_SEMANTIC_OWNER: EXISTING_RESUME/PROJECT_STATE_PROJECTION
STATUS_APPLICATION_SURFACE: EXISTING_READ_ONLY_RESUME/INSPECT_SURFACE_WITH_COMPACT_STATUS_PROJECTION
```

The status action may not claim or terminalize an Attempt, authorize execution,
advance Lifecycle state, mutate Project Spine, change the next gate, stage,
commit, or push. It has no status database or registry.

The compact user-facing fields are:

1. `Где мы` — current Project Spine/Change and lifecycle position;
2. `Что сделано` — authoritative completed Attempt/result/evidence facts;
3. `Что сейчас` — current lifecycle and exact Attempt state;
4. `Что дальше` — existing `next_permitted_action`, rendered rather than chosen;
5. `Ресурсы` — trustworthy telemetry/PL06 observations or unavailable;
6. `Состояние` — existing authoritative project/lifecycle/Attempt state.

The default output is plain language, takes approximately 5–10 seconds to read,
and hides raw internal labels unless diagnostic detail is requested. Core status
remains available when optional token/depth metrics are absent.

## 8. Truth policy for token and depth metrics

```text
TOKEN_USAGE_POLICY: EXACT_IF_AUTHORITATIVE_ELSE_UNAVAILABLE
DEPTH_METRIC: AVERAGE_OBSERVED_CONTEXT_DEPTH
DEPTH_METRIC_SCOPE: CURRENT_CYCLE
STATUS_CORE_AVAILABLE_WITHOUT_OPTIONAL_METRICS: YES
```

Token usage is displayed exactly only when authoritative telemetry provides an
exact value. An approximation is displayed only when its source explicitly
marks it approximate. Text length, model name, or conversation intuition cannot
produce a token count.

Depth uses existing PL06 `OperationDepthObservationV1` semantics only. It is not
intelligence, reasoning quality, thinking power, or a newly invented score. The
narrowest truthful aggregation is the average observable context depth of
operations in the current governed cycle. If no authoritative current-cycle
observation exists, depth is unavailable; the scope is not silently widened.

Missing optional token/depth values do not fail the core status action.

## 9. Public command ownership and boundaries

```text
PUBLIC_AGENT_COMMAND_OWNER: GOVERNED_OPERATION_LIFECYCLE
PUBLIC_AGENT_COMMAND_FAMILY: planning-lite execute
MUTATION_PHASES: prepare / complete
READ_ONLY_STATUS_SURFACE: EXISTING_READ_ONLY_RESUME/INSPECT_SURFACE
```

Exact flags and symbols remain Implementation Planning details. Status is not
forced under a mutating command merely for symmetry. The owner need not type
the CLI; the sidebar agent routes the semantic intent to the lifecycle surface.

Change 2 does not become a prerequisite for this v1 status contract, and the
PL08 RunReceipt measurement correction is not absorbed.

## 10. Reconciled authority matrix

| Concern | Authority | Lifecycle responsibility |
| --- | --- | --- |
| route and Guidance | PL07 | consume exact guidance; no rerouting |
| Attempt occurrence/claim/terminal state | Attempt Runtime | coordinate exact calls; never redefine Runtime |
| preparation/completion contract | Executor | call and validate; no host ownership |
| sidebar execution | sidebar agent | drive operator sequence; no authority transfer |
| reentrant sequencing/completion coordination | Lifecycle | sole owner of this coordination |
| RunReceipt validation/storage | Telemetry | supply exact facts; no schema transfer |
| evaluation | PL08 | receive validated evidence; no Lifecycle evaluation |
| current position/next gate | Project Spine / owner-authorized state | read and hand off; no Lifecycle invention |
| context-depth observation | PL06 | read bounded projection; no redefining semantics |

```text
AUTHORITY_TRANSFER: NONE
```

## 11. Definition-level acceptance criteria

1. A valid operation can continue across bounded agent interactions using the
   same exact IN_FLIGHT Attempt identity.
2. Completion is explicit and occurs before the final human-facing cycle claim.
3. The Lifecycle performs the sequence of exact preparation, agent work,
   completion validation, receipt/evidence readback, terminalization, PL08
   handoff, and authoritative continuation.
4. Missing, stale, cross-Attempt, invalid, or incomplete facts fail closed at
   the first broken seam.
5. Lifecycle does not authorize execution, reselect Guidance, allocate an
   Attempt, redefine RunReceipt, evaluate PL08, or choose a next gate.
6. No persistent process, lifecycle database, registry, scheduler, worker,
   queue, daemon, or hidden callback is required.
7. `итоги`/finish intent is semantic, non-authorizing, and does not persist raw
   owner chat as lifecycle state.
8. `статус` is read-only, uses the existing resume/project-state projection, and
   keeps core fields available without optional metrics.
9. Token and depth values follow the exact/explicit-approximation/unavailable
   truth policy; no values are inferred or fabricated.
10. Change 2 and Change 3 remain separate, and the Stop hook has no production
    role.
11. Executor closure remains dependent on Lifecycle implementation and
    integrated proof.
12. Changes remain distinct; `CHANGE_MERGE_REQUIRED: NO`.

## 12. Closure and Plan-time stop conditions

Lifecycle closure requires integrated proof of exact Attempt continuity,
Executor contract use, receipt/evidence ordering, Attempt terminalization, PL08
handoff, next-gate non-authority, and self-hosted bounded operation traversal.
An isolated helper, prose summary, status-only output, or host callback is not
closure.

Implementation Planning must stop for owner adjudication if it discovers a need
for persistent Lifecycle state, a new authority owner, an API/private IPC or
hook callback dependency, RunReceipt schema change, Attempt Runtime amendment,
Change merge, Change 2/3 absorption, or automatic completion as a v1
precondition.

## 13. Effective boundaries and next gate

```text
EXECUTOR_DEFINITION_AMENDMENT: REQUIRED / COORDINATED AND EFFECTIVE
GOVERNED_OPERATION_LIFECYCLE_DEFINITION_AMENDMENT: REQUIRED / EFFECTIVE
LIFECYCLE_CHANGE_STATE: DEFINITION_AMENDED / IMPLEMENTATION_PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED
CHANGE_MERGE_REQUIRED: NO
CHANGE_2: BLOCKED
MAJOR_PL09_NEXT_SLICE_GATE: PRESERVED / UNCONSUMED
```

The experimental Stop hook remains untouched with
`EXPERIMENTAL_STOP_HOOK_PRODUCTION_ROLE: NONE` and
`HOOK_CLEANUP_NEXT_ACTION: SEPARATE_OWNER_CLEANUP`.

The next owner gate is:

```text
OWNER_AUTHORIZATION_PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_PLANNING_RESUME_PATTERN_B
```

That gate may prepare the renewed Lifecycle Implementation Plan only. It does
not authorize implementation.
