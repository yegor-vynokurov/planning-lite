# PL-V39-09 Authoritative Attempt Runtime Access - Approved Definition v1

Status: APPROVED_BY_OWNER

This canonical Definition is the approved scope authority for
CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001. It preserves the
approved semantics of the corrected candidate. It does not authorize
Planning, implementation, runtime execution, staging, commit, release, or
resumption of paused work.

The accepted nonblocking finding NF2-01 is a clarity/redundancy-only
finding and does not change the approved Definition semantics.

## 1. CHANGE IDENTITY

```text
DOCUMENT_ID: PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-DEFINITION-001
CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001
CHANGE_NAME: PL09 Authoritative Attempt Runtime Access
STATUS: APPROVED_BY_OWNER
OWNER_APPROVAL: USER / EXPLICIT / current owner gate
DEFINITION_DECISION: APPROVE_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_CHANGE_DEFINITION
INDEPENDENT_REVIEW: PASS_WITH_NON_BLOCKING_FINDINGS
MATERIAL_FINDINGS: 0
NONBLOCKING_FINDINGS: 1
IMPLEMENTATION_AUTHORIZED: NO
PLANNING_AUTHORIZED: NO
IMPLEMENTATION_PLAN: NOT_CREATED
FORMAL_READINESS: NOT_RUN
SOURCE_CANDIDATE: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_CHANGE_DEFINITION_CANDIDATE_CORRECTED.md
SOURCE_CANDIDATE_SHA256: E5ED262EC0F847BBF79653FC0A79DF8A0163D86312E9FFE1E5022C7AA00FFCD5
BASELINE_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
CANONICALIZATION_SEMANTIC_DELTA: NONE
ACTIVATION: DEFINITION_APPROVED / PLANNING_NOT_YET_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED
NEXT_GATE: OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_IMPLEMENTATION_PLANNING
```

```text
CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001
TITLE: Authoritative Attempt Runtime Access
CHANGE_CLASS: BOUNDED_CORRECTIVE_PREREQUISITE
DEFINITION_CORRECTION_MODE: CORRECT_DEFINITION_IN_PLACE
ROADMAP_FAMILY: PL-V39-09 / SAFE ORCHESTRATION
CAUSAL_GAP: ORCHESTRATION_GAP
DEPENDENCY_POSITION:
  THIS_CHANGE
  -> CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001
  -> CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001 Planning resume
```

This corrected candidate preserves the Change identity and prerequisite
position. It does not create a new Roadmap vertebra, split the prerequisite,
amend the lifecycle Definition, authorize Planning, authorize implementation,
or authorize executor work.

## 2. AUTHORITY AND LINEAGE

```text
OWNER_GATE:
  OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_DEFINITION_CORRECTION
OWNER_DECISION:
  AUTHORIZE_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_DEFINITION_CORRECTION
ORIGINAL_CANDIDATE:
  .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_CHANGE_DEFINITION_CANDIDATE.md
ORIGINAL_CANDIDATE_SHA256:
  0300D0615BA2ED9505718D1E3595502B9FE3070EBED9F2B800C5FEB1D031B3ED
FRESH_REVIEW:
  .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_CHANGE_DEFINITION_FRESH_REVIEW.md
FRESH_REVIEW_SHA256:
  04F22C7DF3CF0B6A62AF030970A8FB7F61FACFFB67E2AEF9753ECE23078B50D3
FINDINGS_ADJUDICATION:
  .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_DEFINITION_FINDINGS_ADJUDICATION.md
FINDINGS_ADJUDICATION_SHA256:
  BD8AE40A86F747BB0B2F91F07EDBF9093FA73B008CF7748110A4E76E15CD1DB3
UPSTREAM_ADJUDICATION_SHA256:
  3EFDC97866B0A1EABCF5A6F2B28DB43D0A071C906DB883E203C6E979214B9143
DOWNSTREAM_LIFECYCLE_DEFINITION_SHA256:
  56DFD7C6B7610262A1DD61BCE7771B320F645DAB901EC90DB6B3B3685815611B
ENTRY_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
```

The original candidate remains historical failed-review evidence and is not
mutated or overwritten. The five material findings are resolved as follows:

| Finding | Corrected binding | Status |
| --- | --- | --- |
| `MF-01` | `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY` | `CLOSED` |
| `MF-02` | dedicated explicit Attempt preparation adapter | `CLOSED` |
| `MF-03` | stale provenance removed from v1 | `CLOSED` |
| `MF-04` | durable fail-closed `IN_FLIGHT` plus explicit owner interruption recovery | `CLOSED` |
| `MF-05` | executor-independent closure | `CLOSED` |

## 3. PROBLEM STATEMENT

`AttemptRecordV1` defines deterministic Attempt identity, immutable lineage and
evidence references, but the repository has no authoritative durable runtime
capability that can materialize a legitimate Attempt, retrieve it exactly by
`attempt_id`, or determine whether it remains activatable. A future explicit
`planning-lite execute --attempt-id <id>` therefore cannot legally obtain the
existing Attempt required by the approved lifecycle architecture.

The dedicated preparation action must create the Attempt before `execute`.
`execute` consumes an already-existing Attempt and never creates its target.
Constructing a record from command fragments, resume context, receipts, or Git
state proves only schema validity, not authoritative existence.

## 4. CAUSAL GAP

```text
ATTEMPT_RUNTIME_ACCESS_GAP: ORCHESTRATION_GAP
FIRST_BROKEN_SEAM:
  explicit Attempt preparation -> authoritative current AttemptRecordV1
DOWNSTREAM_UNREACHABLE:
  exact lookup/admissibility -> governed executor callable binding -> lifecycle
```

The identity/evaluation contracts exist, but the identity-carrying durable
runtime source and bounded preparation seam do not. This Change closes only
that prerequisite seam and must expose the executor callable binding as the
next broken seam.

## 5. PURPOSE

Define the smallest bounded PL09 capability that:

1. receives an already owner-authorized explicit Attempt-preparation request;
2. materializes one canonical Attempt occurrence through a real production
   preparation path;
3. retrieves exactly one authoritative Attempt by canonical `attempt_id`;
4. exposes the minimum `ACTIVATABLE / IN_FLIGHT / TERMINAL` state truth;
5. rejects missing, malformed, corrupt, in-flight, terminal, or otherwise
   inadmissible Attempts according to objective v1 facts;
6. prevents duplicate activation by an atomic claim;
7. supports explicit owner interruption recovery without reactivation; and
8. remains separate from authorization, execution, evaluation, lifecycle
   sequencing, retry, and next-gate authority.

## 6. SCOPE

The Change owns exactly:

- `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY` as the bounded runtime-truth
  owner inside the existing PL09 Safe Orchestration family;
- a dedicated explicit Attempt preparation application adapter;
- one authoritative durable current record per `attempt_id` at most;
- canonical Attempt identity and materialization-time immutable provenance;
- exact lookup and fail-closed corruption handling;
- the `ACTIVATABLE / IN_FLIGHT / TERMINAL` state envelope;
- pure state-based admissibility;
- atomic materialization and activation claim;
- normal and explicit owner-interruption terminalization contracts;
- production writer, readback, negative, concurrency, recovery, and bounded
  traversability evidence.

## 7. OUT OF SCOPE

This Change does not own operation authorization, route selection, guidance
selection, execution, executor invocation, execution result/error production,
RunReceipt production or association, PL08 evaluation policy, lifecycle
sequencing, lifecycle persistence, next-gate authority, retry or replacement
policy, scheduler, queue, lease, worker assignment, timeout, watchdog, hidden
crash recovery, generalized task/Change state, semantic operation trace,
Change-2 F01/F02/F03, Change 3, generic orchestration registry, arbitrary CRUD,
or a new Roadmap vertebra.

## 8. SEMANTIC OWNER

```text
ATTEMPT_RUNTIME_TRUTH_SEMANTIC_OWNER:
  PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY
OWNER_PLACEMENT: bounded capability inside existing PL09 Safe Orchestration
NEW_SUBSYSTEM_REQUIRED: NO
NEW_ROADMAP_VERTEBRA_REQUIRED: NO
EVIDENCE_AUTHORITY_REMAINS_EVIDENCE_ONLY: YES
```

The runtime owner alone owns durable authoritative Attempt occurrence truth,
exact lookup, uniqueness, and enforcement/persistence of the transitions frozen
here. It does not grant execution authority or decide owner dispositions.

Change Execution Ledger, progress, and review surfaces may consume, reference,
audit, and project Attempt runtime facts. They are evidence/audit consumers,
not mutable runtime source of truth. PL08 retains canonical Attempt and result
contracts and evaluation authority, but is not a runtime persistence owner or
pump. The future lifecycle is a consumer and requester, not the source owner.

## 9. ATTEMPT CONTRACT VS RUNTIME TRUTH

`AttemptRecordV1` remains the canonical contract in
`src/planning_lite/attempt_evaluation.py`. Its location does not confer
runtime persistence authority on PL08. The runtime owner uses the same model
and must not create a duplicate semantic model.

| Class | `AttemptRecordV1` fields | Runtime meaning |
| --- | --- | --- |
| `IDENTITY` | `attempt_id`, with `change_id`, `task_or_operation_id`, and `attempt_ordinal` as validated components | sole deterministic identity and lineage address |
| `IMMUTABLE_PROVENANCE` | `authorization_ref`, `acceptance_contract_ref`, `candidate_identity`, `baseline_refs`, `operation_guidance_ref`, `prompt_composition_ref`, `parent_attempt_ref`, `addresses_finding_refs` | frozen preparation inputs and lineage; validated at materialization and never reinterpreted |
| `RUNTIME_STATE_RELEVANT` | `observed_result_ref` | same-Attempt terminal-fact reference after terminalization; it is not an authorization or complete state machine |
| `EVALUATION_ONLY` | `verifier_contract_refs` | evaluation obligations that do not decide activation state |

The runtime owner persists the canonical record plus only the minimal state and
fact-reference envelope defined here. Immutable provenance has no v1
continuous-freshness or supersession semantics.

## 10. PRIMARY IDENTITY

```text
PRIMARY_ATTEMPT_IDENTITY: AttemptRecordV1.attempt_id
IDENTITY_SHAPE: <Change ID>/<task-or-operation ID>/A<positive ordinal>
SECOND_RUNTIME_ATTEMPT_ID: NO
ORCHESTRATION_ID: NO
STORAGE_GENERATED_SEMANTIC_ID: NO
IMPLICIT_LATEST_IDENTITY: NO
FUZZY_IDENTITY: NO
POST_HOC_IDENTITY_RECONSTRUCTION: NO
```

The identity rule is the existing `AttemptRecordV1` lineage and ordinal
allocation contract. Identity is never inferred from a receipt, result, CLI
request, filesystem search, timestamp, or latest record.

## 11. AUTHORITATIVE SOURCE OF TRUTH

The Change establishes exactly one owner-scoped authoritative durable source
under `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY`. Its invariant is:

```text
ONE_ATTEMPT_ID -> AT_MOST_ONE_AUTHORITATIVE_CURRENT_ATTEMPT_RECORD
```

`FOUND` means the runtime owner returned the canonical persisted record and its
authoritative state envelope. Duplicate, conflicting, undecodable, or
identity-inconsistent authoritative data fails closed. No source wins through
precedence, and no competing ledger/evidence store is authoritative.

```text
ATTEMPT_SOURCE_OF_TRUTH != ACTIVE_LIFECYCLE_REGISTRY
ATTEMPT_RUNTIME_TRUTH_PERSISTENCE: REQUIRED
GOVERNED_OPERATION_LIFECYCLE_PERSISTENCE: NO
```

The durable source persists only Attempt truth, immutable provenance, the
three-state envelope, and the minimum terminal fact reference. It does not
persist lifecycle continuation, route state, scheduler state, worker state,
semantic trace, generalized event history, or retry queue state.

## 12. MATERIALIZATION

```text
ATTEMPT_PREPARATION_HOST:
  DEDICATED_EXPLICIT_ATTEMPT_PREPARATION_APPLICATION_ADAPTER
ATTEMPT_PREPARATION_COMMAND_NAME_MUST_BE_FROZEN_NOW: NO
ATTEMPT_MATERIALIZATION_EVENT:
  explicit owner-authorized preparation of one new Attempt occurrence for a
  known Change/task/operation before execution activation
MATERIALIZATION_DEPENDENCY_ACYCLIC: YES
INITIAL_RUNTIME_STATE: ACTIVATABLE
```

The preparation adapter runs before:

```text
planning-lite execute --attempt-id <existing id>
```

The adapter receives complete Change/task/operation identity, explicit
authorization reference, bounded Attempt input/provenance, and exact lineage
scope. It obtains or verifies complete canonical lineage, invokes the existing
PL08 identity/ordinal rules, constructs a validated `AttemptRecordV1`, and
requests durable materialization from the runtime owner. The runtime owner
revalidates identity, lineage, uniqueness, and record shape atomically before
persisting `ACTIVATABLE` and returns the canonical `attempt_id`.

The adapter may not execute, select guidance, choose a route, start lifecycle,
invent Change/task identity, infer latest Attempt, or create retry policy.
`execute` may only consume an existing exact `attempt_id`.

## 13. LOOKUP SEMANTICS

Reusable domain/application lookup accepts one complete `attempt_id` and
returns exactly one of:

```text
FOUND(existing authoritative Attempt and state)
NOT_FOUND
INVALID_ID
CORRUPT_CONFLICT
```

`INVALID_ID` means the identity shape is invalid. `NOT_FOUND` means no
authoritative record exists. `CORRUPT_CONFLICT` covers duplicate, inconsistent,
undecodable, or structurally invalid authoritative data where a unique answer
cannot be trusted. A separately observable `INVALID_RECORD` result may be used
only if the runtime owner can distinguish it objectively from corruption; it
must not become UI wording or a fallback path.

Lookup has no latest, fuzzy, substring, fallback, cross-store precedence, or
reconstruction mode. All non-`FOUND` outcomes fail closed. The CLI and future
lifecycle are adapters/consumers; neither is the source of truth.

## 14. RUNTIME STATE MODEL

```text
THREE_STATE_MODEL_RETAINED: YES
STATE_SET: ACTIVATABLE | IN_FLIGHT | TERMINAL
```

`ACTIVATABLE` means an authoritative canonical Attempt has been durably
materialized and has not been claimed or terminalized. It requires no undefined
currentness or supersession check.

`IN_FLIGHT` means exactly one atomic activation claim succeeded for this
Attempt. It remains `IN_FLIGHT` through normal execution and may remain there
indefinitely after abrupt process/host loss until explicit owner recovery.

`TERMINAL` means an authoritative same-Attempt terminal fact was accepted.
Terminal is irreversible for that Attempt.

No `ABANDONED`, `FAILED`, `RECOVERING`, `RETRYING`, `RESERVED`, queue, worker,
lease, scheduler, or lifecycle-continuation state exists.

## 15. TERMINAL SEMANTICS

```text
TERMINAL_ATTEMPT_DEFINITION:
  an IN_FLIGHT Attempt becomes irreversibly TERMINAL when the runtime owner
  accepts one authoritative same-Attempt terminal fact whose
  execution_status is COMPLETED, FAILED, INTERRUPTED, or INVALID
```

The four values are the existing canonical execution statuses. Terminality is
independent of PL08 technical evaluation, verifier outcomes, Change closure,
and receipt existence. An optional unvalidated `observed_result_ref` alone is
not terminality.

Normal terminalization receives a same-Attempt execution-end fact from the
future governed executor binding. Owner interruption recovery receives the
explicit owner-authorized interruption fact defined below. A second,
conflicting, wrong-Attempt, or unsupported terminal fact fails closed.

## 16. ACTIVATION ADMISSIBILITY

The runtime owner exposes a pure/read-only state predicate:

```text
ADMISSIBLE
REJECTED(INVALID_ID | NOT_FOUND | CORRUPT_CONFLICT | INVALID_RECORD |
         IN_FLIGHT | TERMINAL)
```

`ADMISSIBLE` means one valid authoritative record exists in `ACTIVATABLE` and
may be atomically claimed. It does not grant execution authority. The caller
must already hold separately valid owner authorization and execution guidance.

The predicate depends only on authoritative source facts, exact identity,
immutable materialization-time validation, and state. It does not use
CLI-local state, lifecycle memory, receipt guessing, a hidden registry,
supersession, revocation inference, or Change-2 trace.

## 17. STATE TRANSITION AUTHORITY

```text
ATTEMPT_RUNTIME_STATE_AUTHORITY != EXECUTION_AUTHORIZATION_AUTHORITY
```

Atomic claim means that this already-authorized Attempt is reserved for its one
execution occurrence. It does not grant execution authority.

The exact transition authority matrix is:

| Transition | Request/fact authority | Decision/precondition | Enforcement and persistence | Result |
| --- | --- | --- | --- | --- |
| `MATERIALIZE` | `EXISTING_EXPLICIT_OWNER_AUTHORIZED_CHANGE_EXECUTION_PREPARATION` | `PL08 AttemptRecordV1` lineage/ordinal contract; valid exact record; identity absent and unique | `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY` | `ABSENT -> ACTIVATABLE` |
| `CLAIM_ACTIVATION` | future authorized activation caller with existing guidance | exact valid record is `ACTIVATABLE` | `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY`, atomic | `ACTIVATABLE -> IN_FLIGHT` |
| `TERMINALIZE_NORMAL` | future governed executor callable binding supplies canonical same-Attempt execution-end fact | exact identity, current `IN_FLIGHT`, supported status, no conflict | `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY` | `IN_FLIGHT -> TERMINAL` |
| `TERMINALIZE_INTERRUPTED_RECOVERY` | explicit owner/lifecycle control authority supplies owner-authorized same-Attempt interruption disposition | exact identity, current `IN_FLIGHT`, valid owner decision, `INTERRUPTED`, no conflict | `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY` | `IN_FLIGHT -> TERMINAL` |

The runtime owner enforces transitions but never decides that an interruption
occurred, invents authorization, selects guidance, or chooses retry.

## 18. DURABILITY

The runtime source and committed transitions survive process boundaries and are
deterministic, owner-scoped, identity-safe, unique, inspectable, testable, and
atomic enough for materialization, claim, and terminalization. Immutable
provenance remains immutable. A single authoritative storage domain is
sufficient; no distributed lock or lease architecture is required.

Storage technology remains Plan-level. Filesystem, structured file, database,
or another carrier is acceptable only if it proves the frozen durability,
uniqueness, conflict, process-boundary, and atomic-transition properties. The
Definition does not choose JSON, YAML, JSONL, SQLite, a directory layout, or a
serialization library.

## 19. CONCURRENCY / IN-FLIGHT BOUNDARY

```text
IN_FLIGHT_STATE_REQUIRED: YES
ATOMICITY_REQUIRED: compare-and-transition ACTIVATABLE -> IN_FLIGHT
ABRUPT_LOSS_POLICY: FAIL_CLOSED_OWNER_RECOVERY_REQUIRED
IN_FLIGHT_CAN_REMAIN_FAIL_CLOSED_PENDING_OWNER: YES
SCHEDULER_OR_QUEUE_REQUIRED: NO
LEASE_OR_DISTRIBUTED_LOCK_REQUIRED: NO
AUTOMATIC_TIMEOUT_RESET: NO
AUTOMATIC_ROLLBACK: NO
AUTOMATIC_RETRY: NO
```

Exactly one claimant may succeed. A losing or repeated claimant receives a
fail-closed `IN_FLIGHT` or terminal rejection. If the process/host disappears
after durable claim, the Attempt remains `IN_FLIGHT` indefinitely until
explicit owner recovery. No hidden watchdog, timeout, lease expiry, automatic
release, `IN_FLIGHT -> ACTIVATABLE`, replacement, or retry occurs.

## 20. PL08 BOUNDARY

```text
PL08_IS_EVALUATOR_NOT_PUMP: YES
PL08_RUNTIME_ORCHESTRATION_CREATED: NO
```

PL08 retains `AttemptRecordV1`, `ObservedResultV1`, verifier, Finding, and
technical-evaluation contracts and their evaluation authority. The runtime
owner persists and enforces Attempt truth; it does not move evaluation policy
or orchestration into PL08. `ObservedResultV1` is used as an existing fact
shape, not as a grant of runtime authority to the evaluator.

## 21. LIFECYCLE BOUNDARY

The future governed lifecycle may consume an already-existing Attempt, inspect
admissibility, request an owner-enforced claim, carry the exact `attempt_id`,
and hand normal terminal facts to the runtime owner. It may not prepare or
materialize Attempts, own runtime truth, reconstruct records, bypass rejection,
decide interruption, define retry, or persist its lifecycle.

```text
LIFECYCLE_OWNS_ATTEMPT_SOURCE: NO
GOVERNED_LIFECYCLE_PERSISTENCE_REQUIRED: NO
```

## 22. EXECUTOR-PREREQUISITE BOUNDARY

```text
EXECUTOR_PREREQUISITE:
  CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001 / NOT_STARTED
EXECUTOR_SCOPE_INCLUDED: NO
EXECUTOR_PRODUCED_TERMINAL_FACT_REQUIRED_FOR_THIS_CHANGE_CLOSURE: NO
```

This Change does not define executor callable behavior, host invocation,
execution result/error semantics, RunReceipt production, same-Attempt receipt
provenance, or real `COMPLETED`/`FAILED` executor output. The next prerequisite
will bind normal executor output to `TERMINALIZE_NORMAL` after this source and
its interruption recovery semantics close.

## 23. CHANGE-2 / CHANGE-3 BOUNDARIES

```text
CHANGE2_SCOPE_SEPARATION: HARD_BOUNDARY
CHANGE_2: BLOCKED / VALID / PAUSED
CHANGE3_REQUIRED: NO
```

Attempt runtime truth contains only identity, immutable provenance, minimal
state, and terminal fact reference. It is not semantic operation trace,
generalized execution history, event history, trace analytics, retention
policy, Change-2 F01/F02/F03, or Change-3 measurement work.

## 24. SYSTEM TRAVERSABILITY OBLIGATION

The bounded seam is:

```text
explicit preparation/materialization
-> exact authoritative Attempt lookup
-> state admissibility
-> atomic claim
-> explicit owner interruption recovery where needed
```

Closure requires local contract proof and the cheapest adequate production
system proof that a real preparation action materializes an Attempt, exact
lookup returns it, admissibility is objective, one claim wins, competing claims
fail closed, and owner recovery terminalizes only the same Attempt. Fake store
seeding, reconstruction, evidence-ledger mutation, and helper-only proof are
insufficient.

This Change closes only Attempt runtime access. The next broken seam remains:

```text
GOVERNED_EXECUTOR_CALLABLE_BINDING / WIRING_GAP
```

The overall self-hosted journey is not claimed `WIRED_TRAVERSABLE` or
`PASSING` by this prerequisite alone.

## 25. EXPECTED GAP DELTA

```text
BEFORE:
  NO_AUTHORITATIVE_ATTEMPT_RUNTIME_SOURCE / ORCHESTRATION_GAP
AFTER:
  AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_AVAILABLE
SEAM_DELTA:
  explicit preparation -> authoritative lookup -> admissibility -> atomic
  claim -> owner interruption recovery: WIRED_TRAVERSABLE
NEXT_BROKEN_SEAM:
  GOVERNED_EXECUTOR_CALLABLE_BINDING / WIRING_GAP
OVERALL_SELF_HOSTED_JOURNEY_AFTER_THIS_CHANGE:
  NOT CLAIMED WIRED_TRAVERSABLE; NOT CLAIMED PASSING
```

## 26. FALSE-DONE RESISTANCE

The following are insufficient for completion:

- a store with no real production preparation writer;
- a fake test-seeded Attempt;
- an Attempt reconstructed from request, resume, receipt, Git, or CLI state;
- multiple competing stores or evidence ledger used as mutable source;
- CLI-local runtime truth;
- atomic claim with no explicit owner recovery semantics;
- terminal proof that requires the future executor prerequisite;
- a helper with no production seam;
- a source expanded into lifecycle, scheduler, event-history, or registry
  behavior;
- a successful claim interpreted as execution authorization.

## 27. DEFINITION-LEVEL SURFACE

| Category | Required semantic surface |
| --- | --- |
| `SEMANTIC_OWNER_REQUIRED` | `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY` inside existing PL09 Safe Orchestration; ledger/progress/review remain evidence-only |
| `AUTHORITATIVE_SOURCE_REQUIRED` | one durable Attempt source with sole identity, immutable provenance, three-state envelope, uniqueness, and fail-closed conflict behavior |
| `PRODUCTION_MATERIALIZATION_INTEGRATION` | dedicated explicit Attempt preparation application adapter before `execute`, using canonical lineage/ordinal rules and a real production writer |
| `READ/ADMISSIBILITY_INTEGRATION` | exact lookup, objective v1 state admissibility, atomic claim, normal terminalization contract, and explicit owner interruption recovery |
| `TEST/EVIDENCE_REQUIRED` | preparation/materialization readback, lookup, negative, duplicate-claim, owner-recovery, terminal-contract, and bounded system seam evidence |
| `OUT_OF_SCOPE` | executor, RunReceipt, lifecycle persistence, stale/revocation semantics, scheduler/lease/retry, Change-2/3, generic registry, new subsystem, Roadmap vertebra |

Ordinary Plan mechanics remain open: module/file layout, storage carrier,
serialization, exact preparation command spelling, private APIs, atomic-write
mechanics consistent with this Definition, test organization, and
non-contractual error wording.

## 28. ACCEPTANCE CRITERIA

The following corrected ACs preserve the original candidate's strong identity,
lookup, durability, and false-done boundaries while recording semantic changes.

| Original AC | Corrected mapping |
| --- | --- |
| `OLD_AC-01` | `AC-02`, `AC-03` |
| `OLD_AC-02` | `AC-01`, `AC-05` |
| `OLD_AC-03` | `AC-04` |
| `OLD_AC-04` | `AC-06`, `AC-07` |
| `OLD_AC-05` | `AC-08` |
| `OLD_AC-06` | `AC-09` |
| `OLD_AC-07` | `AC-10` |
| `OLD_AC-08` | `AC-11`, `AC-12` |
| `OLD_AC-09` | `AC-13` |
| `OLD_AC-10` | `AC-09`, `AC-21` |
| `OLD_AC-11` | `AC-10`, `AC-11` |
| `OLD_AC-12` | `AC-14` |
| `OLD_AC-13` | `AC-15` |
| `OLD_AC-14` | `AC-16` |
| `OLD_AC-15` | `AC-17` |
| `OLD_AC-16` | `AC-17`, `AC-18` |
| `OLD_AC-17` | `AC-18`, `AC-19` |
| `OLD_AC-18` | `AC-20`, `AC-21` |
| `OLD_AC-19` | `AC-19` |
| `OLD_AC-20` | `AC-20`, `AC-21`, `AC-22` |

`AC-01` — The sole runtime-truth owner is
`PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY`; evidence surfaces remain
consumers/projections and no authority is transferred to them.

`AC-02` — `AttemptRecordV1.attempt_id` and its validated Change/task/ordinal
components remain the sole Attempt identity; no second, latest, fuzzy, or
reconstructed identity exists.

`AC-03` — One authoritative source preserves canonical identity and immutable
materialization-time provenance, with at most one authoritative current record
per `attempt_id`.

`AC-04` — A dedicated explicit preparation application adapter is a real
production writer that materializes a new authorized Attempt before `execute`;
`execute` consumes an existing Attempt and never creates its target.

`AC-05` — Request authority, PL08 identity-rule ownership, and runtime
persistence/uniqueness ownership are separate; the runtime owner cannot invent
Change/task identity or execution authority.

`AC-06` — Exact lookup returns only `FOUND`, `NOT_FOUND`, `INVALID_ID`, or
`CORRUPT_CONFLICT`, with no latest, fuzzy, fallback, cross-store, or
reconstruction mode.

`AC-07` — Missing, malformed, duplicate, conflicting, undecodable, structurally
invalid, and caller-fabricated records fail closed; fake store seeding cannot
prove production completion.

`AC-08` — The authoritative state model is exactly `ACTIVATABLE`, `IN_FLIGHT`,
and `TERMINAL`; no stale/currentness, revocation, supersession, recovery,
retry, queue, or lifecycle state is added.

`AC-09` — Pure admissibility returns `ADMISSIBLE` only for one valid
authoritative `ACTIVATABLE` record and rejects invalid/nonexistent/corrupt,
`IN_FLIGHT`, and `TERMINAL` records without granting execution authority.

`AC-10` — Activation atomically transitions exactly one authorized caller's
`ACTIVATABLE` Attempt to `IN_FLIGHT`; competing and repeated claims fail
closed.

`AC-11` — Abrupt process/host loss never automatically releases, retries,
replaces, or reactivates an `IN_FLIGHT` Attempt; it may remain fail-closed
pending explicit owner recovery.

`AC-12` — `OWNER_RESOLVE_INTERRUPTED_ATTEMPT` is the only bounded recovery path:
it never reactivates or replaces the same Attempt and requires explicit owner
control authority.

`AC-13` — Terminalization is irreversible and accepts only a same-Attempt
canonical execution-end fact with status `COMPLETED`, `FAILED`, `INTERRUPTED`,
or `INVALID`; evaluation and receipt existence alone are insufficient.

`AC-14` — The four-row transition authority matrix is enforced: preparation
requests, PL08 supplies identity rules, the future executor supplies normal end
facts, owner control supplies interruption disposition, and PL09 persists/enforces.

`AC-15` — Domain/application lookup, preparation, claim, and recovery surfaces
are reusable; CLI is an adapter and never the source of truth.

`AC-16` — The future lifecycle consumes an existing Attempt and may request
owner-enforced transitions, but cannot create, own, reconstruct, bypass, or
persist Attempt truth.

`AC-17` — `PL08_IS_EVALUATOR_NOT_PUMP` remains true; PL08 owns contracts and
evaluation facts but not runtime persistence, claim, or recovery authority.

`AC-18` — Executor callable behavior, host invocation, execution result/error
semantics, RunReceipt production, and same-Attempt receipt provenance remain in
the separate not-started executor prerequisite.

`AC-19` — No Change-2/3 behavior, semantic trace, generalized history,
orchestration registry, scheduler, lease, generic database subsystem, or new
Roadmap vertebra is created.

`AC-20` — Closure can be demonstrated before executor work using real
preparation/materialization, exact lookup, admissibility, atomic claim,
competing-claim rejection, owner interruption recovery, and durable readback.

`AC-21` — Contract-level terminalization tests cover all four canonical status
values without requiring a real executor or RunReceipt; only the future
executor binds normal production end facts.

`AC-22` — The bounded system seam changes from
`NO_AUTHORITATIVE_ATTEMPT_RUNTIME_SOURCE / ORCHESTRATION_GAP` to
`AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_AVAILABLE`, while the next broken seam
remains executor callable binding and no whole-journey PASS is claimed.

```text
ACCEPTANCE_CRITERIA_COUNT: 22
```

## 29. CLOSURE CRITERIA

`CC-01` — `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY` exists as one bounded
semantic owner, and evidence surfaces remain evidence-only.

`CC-02` — One durable inspectable authoritative source enforces canonical
identity, immutable provenance, uniqueness, conflict failure, and the exact
three-state envelope.

`CC-03` — A real dedicated preparation application path materializes an
Attempt from exact owner authorization, complete lineage, and the canonical
identity rule before `execute`.

`CC-04` — A production caller reads the materialized Attempt by exact
`attempt_id`; missing, invalid, corrupt, duplicate, and reconstructed cases
fail closed.

`CC-05` — Pure admissibility returns the corrected v1 outcomes and is based
only on authoritative identity, record validity, and state; no stale or
supersession semantics are inferred.

`CC-06` — Real atomic claim evidence proves exactly one winner and fail-closed
competing/repeated claim behavior.

`CC-07` — Real explicit `OWNER_RESOLVE_INTERRUPTED_ATTEMPT` behavior proves
durable owner-authorized `IN_FLIGHT -> TERMINAL` interruption recovery without
reactivation or replacement.

`CC-08` — Contract-level proof accepts/rejects same-Attempt terminal facts for
all four canonical statuses, while no executor or RunReceipt is required.

`CC-09` — Negative proof covers invalid, absent, fabricated, reconstructed,
ambiguous, in-flight, terminal, duplicate-claim, and conflicting-terminal
inputs.

`CC-10` — The future lifecycle/application boundary can consume a real
authoritative Attempt and state result without owning or recreating the source.

`CC-11` — Bounded system traversability evidence closes only the Attempt-access
seam, records executor callable binding as next broken seam, and proves no
PL08/lifecycle/executor/Change-2/registry authority leakage.

```text
CLOSURE_CRITERIA_COUNT: 11
```

All closure criteria are satisfiable before
`CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001` starts. Real normal
executor end production and RunReceipt binding are deliberately deferred.

## 30. PLAN-TIME ARCHITECTURE STOP

Planning must stop and obtain owner adjudication if it discovers a need for:

- a semantic owner other than `PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY`;
- mutable ledger/progress/review runtime ownership;
- a second identity, implicit/latest lookup, fuzzy lookup, or reconstruction;
- stale-provenance, revocation, or supersession machinery in v1;
- an additional runtime state;
- automatic crash recovery, timeout, lease, watchdog, queue, scheduler,
  rollback, or retry;
- more than one authoritative storage domain;
- lifecycle-owned or CLI-owned Attempt truth;
- executor implementation or RunReceipt production in this Change;
- executor-dependent closure;
- Change-2 trace, generic registry, new subsystem, or new Roadmap vertebra;
- authority transfer or a material semantic choice not frozen here.

The STOP is a governance condition, not an invitation to enlarge the Change.

## 31. DEFINITION / PLAN BOUNDARY

This Definition freezes semantic owner, evidence boundary, preparation host
semantics, identity roles, sole identity, source uniqueness, materialization,
lookup outcomes, v1 admissibility, three states, atomic claim, abrupt-loss
policy, owner recovery, terminal statuses, transition authority matrix,
executor-independent closure, traversability delta, false-done resistance,
forbidden architecture, and proof obligations.

Plan may choose only mechanical details:

- module/file layout;
- storage carrier and serialization implementation;
- exact preparation command spelling;
- private API names;
- atomic-write mechanics consistent with the frozen single-domain semantics;
- test organization;
- non-contractual error wording.

Plan may not reinterpret evidence as runtime truth, add stale semantics,
replace owner recovery with automatic release, require executor closure, or
transfer authority.

## 32. OPEN QUESTIONS

```text
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_MATERIAL_SEMANTIC_CHOICES: 0
PLAN_LEVEL_MECHANICAL_CHOICES:
  storage representation; owner-module placement; serialization library;
  exact preparation command spelling; private API names; atomic-write mechanics;
  test organization; non-contractual error prose
```

The runtime owner, preparation host, identity roles, no-stale v1 boundary,
three-state model, abrupt-loss semantics, owner recovery, transition matrix,
executor-independent closure, and dependency order are resolved.

## 33. DEFINITION CANDIDATE VERDICT

```text
OVERALL: PASS_CORRECTED_DEFINITION_CANDIDATE_PREPARED
EXECUTOR: GPT-5.6_LUNA_EXTRA_HIGH
ATTEMPT_RUNTIME_TRUTH_SEMANTIC_OWNER:
  PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY
EVIDENCE_AUTHORITY_REMAINS_EVIDENCE_ONLY: YES
ATTEMPT_PREPARATION_HOST:
  DEDICATED_EXPLICIT_ATTEMPT_PREPARATION_APPLICATION_ADAPTER
PRIMARY_IDENTITY: AttemptRecordV1.attempt_id
ATTEMPT_RUNTIME_TRUTH_PERSISTENCE_REQUIRED: YES
GOVERNED_OPERATION_LIFECYCLE_PERSISTENCE_REQUIRED: NO
AUTHORITATIVE_SOURCE_REQUIRED: YES
REAL_PRODUCTION_WRITER_REQUIRED: YES
DETERMINISTIC_LOOKUP_BY_ATTEMPT_ID: YES
IMPLICIT_LATEST_LOOKUP: NO
POST_HOC_RECONSTRUCTION: NO
STALE_PROVENANCE_IN_V1: REMOVED
THREE_STATE_MODEL: ACTIVATABLE / IN_FLIGHT / TERMINAL
THREE_STATE_MODEL_RETAINED: YES
ABRUPT_LOSS_POLICY: FAIL_CLOSED_OWNER_RECOVERY_REQUIRED
IN_FLIGHT_CAN_REMAIN_FAIL_CLOSED_PENDING_OWNER: YES
OWNER_INTERRUPTION_RECOVERY: DEFINED
OWNER_INTERRUPTION_FACT_CONTRACT:
  OWNER_AUTHORIZED_SAME_ATTEMPT_INTERRUPTION_DISPOSITION_PROJECTED_AS_OBSERVEDRESULTV1
TERMINAL_SEMANTICS_DEFINED: YES
ACTIVATION_ADMISSIBILITY_DEFINED: YES
STATE_TRANSITION_AUTHORITY_MATRIX: RESOLVED
EXECUTOR_PRODUCED_TERMINAL_FACT_REQUIRED_FOR_CLOSURE: NO
EXECUTOR_SCOPE_INCLUDED: NO
EXECUTOR_PREREQUISITE_REMAINS_SEPARATE: YES
MATERIALIZATION_DEPENDENCY_ACYCLIC: YES
PREREQUISITE_DEPENDENCY_ACYCLIC: YES
PL08_RUNTIME_ORCHESTRATION_CREATED: NO
LIFECYCLE_OWNS_ATTEMPT_SOURCE: NO
CHANGE2_SCOPE_SEPARATION: PASS
CHANGE3_REQUIRED: NO
NEW_SUBSYSTEM_REQUIRED: NO
NEW_ROADMAP_VERTEBRA_REQUIRED: NO
EXPECTED_GAP_DELTA:
  NO_AUTHORITATIVE_ATTEMPT_RUNTIME_SOURCE / ORCHESTRATION_GAP
  -> AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_AVAILABLE / WIRED_TRAVERSABLE bounded seam
FALSE_DONE_RESISTANCE: DEFINED
ACCEPTANCE_CRITERIA_COUNT: 22
CLOSURE_CRITERIA_COUNT: 11
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_MATERIAL_SEMANTIC_CHOICES: 0
PLAN_TIME_ARCHITECTURE_STOP: PRESENT
CORRECTED_DEFINITION_CANDIDATE_READY: YES
MF_01: CLOSED
MF_02: CLOSED
MF_03: CLOSED
MF_04: CLOSED
MF_05: CLOSED
EXECUTOR_PREREQUISITE:
  CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001 / NOT_STARTED
LIFECYCLE_CHANGE:
  DEFINITION_APPROVED / PLANNING_BLOCKED_BY_PREREQUISITE / IMPLEMENTATION_NOT_AUTHORIZED
CHANGE_2: BLOCKED / VALID / PAUSED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
```

The corrected candidate is ready for the separately authorized fresh
independent review gate. It does not authorize canonicalization, Planning,
implementation, executor work, lifecycle resume, staging, commit, or push.
