# PL-V39-09 Governed Operation Lifecycle Runtime - Approved Definition v1

Status: APPROVED_BY_OWNER

This canonical Definition is the approved scope authority for
CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001. It preserves the approved
semantics of the reviewed candidate. It does not authorize Planning,
implementation, runtime execution, staging, commit, release, or resumption of
paused work.

The two reviewed nonblocking findings were accepted as clarity/redundancy-only
findings and do not change the approved Definition semantics.

## 1. CHANGE IDENTITY

```text
DOCUMENT_ID: PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-001
CHANGE_ID: CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
CHANGE_NAME: PL09 Governed Operation Lifecycle Runtime
STATUS: APPROVED_BY_OWNER
OWNER_APPROVAL: USER / EXPLICIT / current owner gate
DEFINITION_DECISION: APPROVE_PL09_GOVERNED_OPERATION_LIFECYCLE_CHANGE_DEFINITION
INDEPENDENT_REVIEW: PASS_WITH_NON_BLOCKING_FINDINGS
MATERIAL_FINDINGS: 0
NONBLOCKING_FINDINGS: 2
IMPLEMENTATION_AUTHORIZED: NO
PLANNING_AUTHORIZED: NO
IMPLEMENTATION_PLAN: NOT_CREATED
FORMAL_READINESS: NOT_RUN
SOURCE_CANDIDATE: .local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_CHANGE_DEFINITION_CANDIDATE.md
SOURCE_CANDIDATE_SHA256: 6B36F95AFE10BC6546A7F2F107FDA5971BADC677A55D128A1490A7C88D123132
BASELINE_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
CANONICALIZATION_SEMANTIC_DELTA: NONE
ACTIVATION: DEFINITION_APPROVED / PLANNING_NOT_YET_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED
NEXT_GATE: OWNER_AUTHORIZATION_PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_PLANNING
```

```text
CHANGE_ID: CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
CHANGE_NAME: PL09 Governed Operation Lifecycle Runtime
MODE: BOUNDED CHANGE DEFINITION SHAPING
OWNER_GATE: OWNER_AUTHORIZATION_PL_V39_09_GOVERNED_OPERATION_LIFECYCLE_CHANGE_DEFINITION_SHAPING
OWNER_DECISION: AUTHORIZE_PL_V39_09_GOVERNED_OPERATION_LIFECYCLE_CHANGE_DEFINITION_SHAPING
EXECUTOR: GPT-5.6_LUNA_EXTRA_HIGH
```

## 2. AUTHORITY AND LINEAGE

The candidate is derived from the following bounded authorities:

```text
ENTRY_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
SYSTEM_TRAVERSABILITY_CLOSURE:
  docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-CLOSURE-v1.md
SYSTEM_TRAVERSABILITY_CLOSURE_SHA256: F051B62705C5B39D1D3AC9B9AE4D5ED42847AFB2E0AB6E5CBC09E0F83E26F05B
ORIGINAL_PREREQUISITE_SHAPING:
  .local/work/experiments/PL09_RUNTIME_ORCHESTRATION_PREREQUISITE_SHAPING.md
ORIGINAL_PREREQUISITE_SHAPING_SHA256: 238FC50A841BA7B99142A9E6718091605A59DE1F2277F3575AFFEC757B357CF8
EMPIRICAL_DISCOVERY:
  .local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_EMPIRICAL_DISCOVERY.md
EMPIRICAL_DISCOVERY_SHA256: 27EC4B2B898E749D45CF1839450A6BCBD10C082132E0D0B9A528A72C60C9ED8F
EMPIRICAL_RESULT: PASS_EMPIRICAL_DISCOVERY_DEFINITION_CANDIDATE_READY
```

The empirical discovery refines the earlier shaping. Its topology, identity,
runtime-lifetime, and authority conclusions are binding for this candidate.
No authority is transferred by this document.

## 3. PROBLEM STATEMENT

The closed self-hosted Critical Journey is:

```text
Attempt
  -> OperationGuidance
  -> Governed Operation Lifecycle
  -> Execution
  -> validated RunReceipt
  -> PL08 Result/Evidence
  -> authoritative Next Gate
```

The journey is currently:

```text
WIRED_FAIL / ORCHESTRATION_GAP
FIRST_BROKEN_SEAM: OperationGuidance -> Governed Operation Lifecycle
REASON: NO_LEGITIMATE_RUNTIME_LIFETIME_OWNER
DOWNSTREAM: DOWNSTREAM_UNREACHABLE
```

Empirical evidence shows that the repository has individual contracts for
Attempt identity, guidance selection, receipt handling, PL08 evaluation, and
resume authority, but no production runtime consumer preserves one governed
operation across those boundaries.

## 4. EMPIRICAL TOPOLOGY

```text
PRIMARY_TOPOLOGY: TOPOLOGY_B_NEW_BOUNDED_IN_PROCESS_LIFETIME_PRIMITIVE_REQUIRED
PERSISTENT_RUNTIME_STATE_REQUIRED: NO
NEW_SUBSYSTEM_REQUIRED: NO
NEW_REGISTRY_REQUIRED: NO
SCHEDULER_REQUIRED: NO
AUTHORITY_TRANSFER_REQUIRED: NO
PL08_RUNTIME_ORCHESTRATION: NONE
CURRENT_RUNTIME_CONSUMER: NONE
```

This is a new bounded primitive within the existing PL09 Safe Orchestration
semantic family, not a new subsystem or general orchestration platform.

## 5. AFFECTED CRITICAL JOURNEY

```text
JOURNEY_ID: PL_SELF_HOSTED_GOVERNED_OPERATION
INITIAL_STATE: WIRED_FAIL / ORCHESTRATION_GAP
FIRST_BROKEN_SEAM: OperationGuidance -> Governed Operation Lifecycle
DOWNSTREAM_UNREACHABLE: YES
```

The affected journey is the self-hosted governed operation itself. A local
unit-test-only surface is not sufficient evidence for this Change.

## 6. PURPOSE

Define the smallest governed runtime lifecycle primitive that accepts an
already-authorized operation/guidance context, preserves one canonical Attempt
identity during one bounded runtime realization, activates existing execution
authority, validates and binds the resulting RunReceipt, hands facts to the
existing PL08 evaluator, and hands downstream facts to existing resume/next-
gate machinery.

The primitive stops fail-closed when a required identity, contract, receipt,
evaluation handoff, or downstream handoff cannot be established.

## 7. SCOPE

The Definition covers only:

- one bounded in-process lifecycle realization of one existing Attempt;
- explicit binding of that Attempt to the already-authorized OperationGuidance;
- canonical sequencing of guidance, execution, receipt validation, PL08
  handoff, and downstream fact handoff;
- identity continuity without introducing a second operation identity;
- fail-closed lifecycle outcomes and authoritative fact references;
- a legitimate production entry path for the self-hosted governed operation;
- local proof and System Traversability non-regression proof;
- architectural guards against persistence, registry, scheduler, subsystem,
  and authority transfer.

The Definition freezes semantic behavior and proof obligations. It does not
freeze ordinary helper names, private decomposition, test names, patch order,
or code layout beyond the bounded owner family identified by empirical work.

## 8. OUT OF SCOPE

The lifecycle does not become any of the following:

- target shaping, routing, planning, or Attempt definition;
- operation authorization or guidance selection policy;
- execution implementation or execution contract semantics;
- receipt truth authority or evidence authority;
- PL08 evaluation policy or PL08 runtime orchestration;
- Project Spine truth, resume truth, or next-gate decision authority;
- a retry scheduler, worker pool, queue, registry, database, or event store;
- persistent workflow state, daemon, background coordinator, or distributed
  runtime;
- generalized operation history or Change-2 semantic trace persistence;
- Change-3 measurement correction;
- a new Roadmap vertebra or authority transfer;
- canonical Definition creation, planning, Formal Readiness, or implementation
  authorization as part of this candidate.

## 9. PRIMARY OPERATION IDENTITY

```text
PRIMARY_OPERATION_IDENTITY: AttemptRecordV1.attempt_id
IDENTITY_CARRIER: AttemptRecordV1.attempt_id
IDENTITY_MODEL: one canonical Attempt identity per bounded lifecycle
SECOND_OPERATION_ID: PROHIBITED
PERSISTENT_LIFECYCLE_ID: PROHIBITED
```

`AttemptRecordV1.attempt_id` is the canonical identity established by the
existing Attempt contract and empirical discovery. The lifecycle input must
carry a reference to that Attempt together with the already-authorized
OperationGuidance. An operation, trace, orchestration-run, or lifecycle ID
must not replace it.

## 10. IDENTITY CONTINUITY

The governing invariant is:

> A governed lifecycle is one bounded runtime realization of one canonical
> Attempt identity.

The same identity must remain attributable through:

```text
AttemptRecordV1.attempt_id
  -> authorized OperationGuidance binding
  -> lifecycle activation
  -> execution invocation
  -> produced RunReceipt
  -> validated receipt binding
  -> PL08 result/evidence handoff
  -> authoritative resume/next-gate fact handoff
```

The Definition requires identity continuity, not gratuitous field duplication.
An existing canonical reference relationship may carry the identity. The
implementation must nevertheless make the relationship explicit enough to
prove that a receipt belongs to this Attempt rather than merely existing or
being structurally valid.

## 11. LIFECYCLE START / END

`LIFECYCLE_START` is the point at which an already-authorized
OperationGuidance, explicitly bound to an existing Attempt, becomes eligible
for governed runtime activation.

The start is not target shaping, routing, planning, Attempt creation, or the
authorization decision. Those authorities remain upstream.

`LIFECYCLE_END` is the first point after the primitive has either:

1. produced and handed off the validated runtime facts required by existing
   PL08 evaluation and authoritative resume/next-gate machinery; or
2. produced a fail-closed disposition identifying the first broken continuity
   or contract seam.

The lifecycle has no live existence after this bounded handoff. It is not a
workflow daemon, scheduler, or durable Project truth carrier.

## 12. RUNTIME LIFETIME

```text
LIFETIME_MODEL: BOUNDED_IN_PROCESS
LIFETIME_BOUNDED: YES
PERSISTENT_LIFECYCLE_STATE: NO
ASYNC_MODEL: SYNC
```

The primitive may coordinate an executor that uses subprocess mechanics, but
that process boundary does not turn the lifecycle into distributed
orchestration. The lifecycle remains an in-process bounded coordinator.

## 13. RESPONSIBILITIES

The primitive has exactly these responsibility classes:

`SEQUENCE` — coordinate already-authorized runtime steps in canonical order.

`CONTINUITY` — preserve and prove the same Attempt identity across the
bounded runtime chain.

`ACTIVATION` — activate the existing execution contract/entrypoint without
owning execution semantics.

`FACT_HANDOFF` — carry execution, receipt, result, evidence, and disposition
facts to the next existing owner through canonical boundaries.

`FAIL_CLOSED` — stop progression when required continuity or validated runtime
facts are absent, invalid, or cannot be handed off.

The primitive may coordinate these responsibilities only for one bounded
lifecycle realization. It does not decide the policies owned by the existing
contracts.

## 14. NON-RESPONSIBILITIES

The lifecycle does not own:

- route selection, target shaping, planning, or Attempt allocation;
- operation authorization or guidance policy;
- execution contract semantics or execution implementation;
- receipt production truth, receipt validation policy, or evidence authority;
- PL08 evaluation semantics, evidence sufficiency, or Gap authority;
- Project Spine truth, durable resume state, or next-gate decision authority;
- automatic retries as a scheduler or recovery policy;
- lifecycle history, event sourcing, registry, database, queue, or scheduler;
- distributed orchestration or host-wide coordination;
- Change-2 compact semantic trace persistence, analytics, or retention;
- Change-3 measurement correction;
- any authority transfer.

## 15. AUTHORITY MATRIX

| Concern | EXISTING_OWNER | LIFECYCLE_COORDINATES | LIFECYCLE_DECIDES |
| --- | --- | --- | --- |
| Target shaping and routing | existing planning/routing authority | NO | NO |
| Attempt identity and lineage | `AttemptRecordV1` contract in `attempt_evaluation` | YES, by reference | NO |
| Operation guidance selection | `planning_lite.execution_guidance.select_operation_guidance` | YES, consumes output | NO |
| Operation authorization | existing authorization contract/owner gate | YES, checks supplied authorization | NO |
| Execution behavior | existing execution authority/entrypoint | YES, activates it | NO |
| RunReceipt production | executing runtime / receipt producer | YES, receives output | NO |
| RunReceipt validation | existing `telemetry.validate_receipt` contract | YES, invokes/checks it | NO |
| PL08 technical evaluation | existing PL08 evaluator, including `evaluate_technical` | YES, hands off facts | NO |
| Evidence truth and applicability | existing verifier/evidence contracts | YES, carries references | NO |
| Project Spine resume state | Project Spine `CURRENT.md` and lifecycle owner | YES, supplies facts | NO |
| `next_permitted_action` / next gate | existing resume/next-gate authority | YES, hands off facts | NO |
| Change-2 trace semantics | `CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001` | NO | NO |
| Lifecycle sequencing and disposition | new bounded PL09 primitive | YES | NO over external authority |

```text
AUTHORITY_TRANSFER: NONE
```

Any implementation that requires the lifecycle to decide one of the matrix
concerns must stop at the Plan-time Architecture STOP and obtain owner
adjudication.

## 16. EXECUTION BOUNDARY

```text
EXECUTION_COORDINATION != EXECUTION_AUTHORITY
```

The lifecycle may activate an existing executor using an already-authorized
contract and may receive its result. It must not reinterpret execution policy,
become the execution implementation, or grant itself execution authority.

Empirical discovery found no current governed production execution consumer
and no exact executor symbol to freeze as a public API. Plan may bind the
actual self-hosted entrypoint from the live call graph, but the semantic owner
and authority boundary above are fixed.

Subprocess calls elsewhere in the repository are administrative Git, Copier,
update, or release helpers; they are not evidence of a governed operation
lifecycle.

## 17. RUNRECEIPT CONTINUITY

```text
RUNRECEIPT_ATTEMPT_BINDING: ABSENT_IN_CURRENT_RUNTIME
REQUIRED_FUTURE_BINDING: SAME_ATTEMPT_AND_STRUCTURALLY_VALID
```

The lifecycle must distinguish all three conditions:

1. a receipt exists;
2. the receipt is attributable to the same canonical Attempt; and
3. the receipt satisfies the existing structural and contractual validation.

The lifecycle must fail closed if any condition is missing. It may invoke the
existing pure receipt validation contract, but it must not move receipt truth
or validation authority into the lifecycle. The final proof must use the
receipt produced and consumed by the real self-hosted lifecycle path, not only
a mock receipt or isolated schema test.

## 18. PL08 BOUNDARY

```text
PL08_IS_EVALUATOR_NOT_PUMP: YES
PL08_RUNTIME_ORCHESTRATION_OWNER: NO
```

The lifecycle may invoke or hand facts to the existing PL08 evaluator through
canonical contracts. PL08 retains evaluation policy, result semantics, and
evidence requirements. The lifecycle must not turn PL08 into a runtime pump,
or reinterpret a negative evaluation outcome as lifecycle failure when the
runtime facts were validly handed off.

## 19. NEXT-GATE BOUNDARY

```text
NEXT_GATE_AUTHORITY_OWNER: Project Spine docs/design/project-spine/CURRENT.md / lifecycle owner
NEXT_GATE_AUTHORITY_TRANSFER: NO
```

The lifecycle may provide the facts consumed by existing `load_resume` and
`next_permitted_action` flow. It must not choose, synthesize, or return its own
authoritative next action. A successful lifecycle handoff is not a gate
approval and does not mutate Project Spine truth by itself.

## 20. PERSISTENCE BOUNDARY

```text
PERSISTENT_RUNTIME_STATE_REQUIRED: NO
PERSISTENT_RUNTIME_STATE: NO
```

The implementation must not introduce a lifecycle database, registry, durable
orchestration queue, persistent state machine, or lifecycle event-sourcing
store. Existing durable Attempt, receipt, evidence, Project Spine, or Change
artifacts remain owned by their existing contracts and may be consumed or
emitted through those contracts. The lifecycle itself is not durable state.

## 21. RETRY / CONCURRENCY / ASYNC BOUNDARIES

```text
RETRY_IDENTITY_MODEL: new AttemptRecordV1 with next ordinal and parent reference
AUTOMATIC_RETRY: NO
CONCURRENCY_MODEL: SINGLE_ACTIVE candidate / multiple independent operations out of scope
ASYNC_MODEL: SYNC
PROCESS_BOUNDARY: no governed process bridge; external receipt input is independently supplied
HOST_BOUNDARY: external_runtime/operator/unavailable receipt source; future adapter boundary only
```

A retry or corrective operation is a new Attempt with the next contiguous
ordinal and, where applicable, a parent Attempt reference. The lifecycle does
not schedule or choose retries.

One lifecycle invocation owns one active Attempt realization. No global worker
pool, locking subsystem, job queue, or cross-host coordination is required.
Independent host-level concurrency is not a contract of this Change and must
not be converted into persistent orchestration state.

The lifecycle's identity boundary is distinct from executor subprocess
mechanics and from external receipt source labels.

## 22. FAILURE SEMANTICS

The lifecycle is bounded and fail-closed for at least these empirically
supported conditions:

- authorized guidance cannot be activated;
- the input cannot be bound to one canonical Attempt identity;
- the operation identity cannot be preserved at a handoff;
- the existing execution contract cannot be invoked;
- execution produces no admissible receipt;
- the receipt is not attributable to the same Attempt;
- receipt validation fails;
- PL08 result/evidence handoff cannot be formed through its contract;
- authoritative downstream resume/next-gate handoff cannot be formed.

Each failure must expose the first broken seam and relevant authoritative
fact/error references. The lifecycle must not invent a retry, recovery, next
gate, or authority transfer in response.

## 23. SUCCESS SEMANTICS

Successful lifecycle completion means that one authorized runtime path was
coordinated with preserved Attempt identity, an admissible same-Attempt receipt
was validated, and the required PL08 and downstream fact handoffs were formed.

Successful lifecycle completion does not mean:

- the Target or Change is complete;
- the next gate is approved;
- PL08 returned `PASS`;
- the Critical Journey is `PASSING`;
- Change 2 is resumed or implemented.

A valid lifecycle may hand off a negative evaluation result.

## 24. RESULT CONTRACT

The minimum lifecycle result must distinguish:

```text
COMPLETED_WITH_FACTS
STOPPED_FAIL_CLOSED
```

The result must carry or reference:

- the canonical Attempt identity/reference;
- lifecycle disposition and first broken seam, when applicable;
- operation guidance and execution invocation/result references;
- the validated same-Attempt receipt reference, when available;
- PL08 result/evidence references, when available;
- downstream handoff references or the reason the handoff could not be formed.

The result must not contain a competing authoritative next action, generalized
event trace, semantic operation history, or Change-2 trace retention.

## 25. CHANGE-2 BOUNDARY

```text
CHANGE_2: CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001
CHANGE_2_STATE: BLOCKED / VALID / PAUSED
CHANGE2_SCOPE_SEPARATION: HARD_BOUNDARY
CHANGE2_F01: OUT_OF_SCOPE
CHANGE2_F02: OUT_OF_SCOPE
CHANGE2_F03: OUT_OF_SCOPE
```

This prerequisite must not implement compact semantic trace retention,
generalized operation history, trace analytics, or persistent trace state.
Change-2 remains a separate future Change.

## 26. CHANGE-3 BOUNDARY

```text
CHANGE3_PREREQUISITE: NO
```

This Change does not depend on `PL08_RUNRECEIPT_MEASUREMENT_CORRECTION`.
Only new contradictory live evidence could alter that conclusion, and such
evidence would require owner adjudication rather than silent Definition drift.

## 27. SYSTEM TRAVERSABILITY OBLIGATION

This Change affects the self-hosted System Walking Skeleton. It must provide
both:

```text
LOCAL_PROOF: required
SYSTEM_TRAVERSABILITY_NONREGRESSION: required
SELF_HOSTED_CRITICAL_JOURNEY_SMOKE: required
N_A_BYPASS: prohibited
```

The proof must exercise the real production binding, not merely instantiate a
new helper or class. It must demonstrate the same Attempt identity through the
real lifecycle path, receipt handoff, PL08 handoff, and downstream resume/gate
surface while preserving all existing authority boundaries.

## 28. EXPECTED CRITICAL JOURNEY DELTA

The exact empirical minimum is:

```text
MINIMUM_EXPECTED_DELTA: WIRED_FAIL / ORCHESTRATION_GAP -> WIRED_TRAVERSABLE at OperationGuidance seam
FULL_SUCCESS_DELTA: not claimed by this prerequisite; PASSING requires the complete governed conjunction
```

This Change alone must not claim `PASSING`. The observed journey state must be
proved after implementation and system smoke; any later `PASSING` result still
requires the frozen resume conjunction.

## 29. PRODUCTION BINDING

The implementation must have at least one legitimate production entry path for
the self-hosted governed operation:

```text
AUTHORIZED_GUIDANCE + EXISTING_ATTEMPT_REFERENCE
  -> real production lifecycle invocation
  -> existing execution authority
  -> validated same-Attempt receipt
  -> PL08 handoff
  -> existing downstream resume/next-gate surface
```

`planning_lite.cli.command_resume` is currently a read-only renderer and does
not satisfy this binding. A utility or helper that is never called by the
self-hosted flow is not completion.

```text
IMPLEMENTED_BUT_UNBOUND != COMPLETE
PRODUCTION_BINDING_REQUIRED: YES
```

The Definition-level semantic owner is the PL09 Safe Orchestration family,
with one candidate bounded module under `src/planning_lite/` permitted by the
empirical topology. The exact private symbols and ordinary import wiring remain
Plan-level mechanics.

## 30. FALSE-DONE RESISTANCE

The Definition explicitly rejects the following false completion: a lifecycle
class or helper exists, isolated unit tests pass, but no production flow calls
it and no same-Attempt system journey is traversable.

Closure therefore requires source-level and runtime evidence of the real
self-hosted production binding, same-Attempt continuity, receipt production
and consumption on that path, PL08 handoff, and downstream non-authoritative
resume/gate handoff.

## 31. DEFINITION-LEVEL SURFACE

The minimum semantic/integration surface is:

| Classification | Definition-level surface |
| --- | --- |
| `SEMANTIC_OWNER_REQUIRED` | One bounded PL09 Safe Orchestration owner path under `src/planning_lite/` (empirical candidate: `src/planning_lite/operation_lifecycle.py`). Count: 1. |
| `CONTRACT_INTEGRATION_REQUIRED` | Existing Attempt/lineage contract in `src/planning_lite/attempt_evaluation.py`; guidance producer in `src/planning_lite/execution_guidance.py`; producer-bound PL06 observation in `src/planning_lite/context.py`; receipt validation/handling in `src/planning_lite/telemetry.py`; the real self-hosted production entry and downstream resume/gate boundary. |
| `TEST/EVIDENCE_REQUIRED` | Owner/product tests and a focused self-hosted Critical Journey smoke proving production binding, same-Attempt continuity, receipt binding, PL08 handoff, downstream non-authority, fail-closed behavior, and traversability non-regression. |
| `MECHANICAL_INTEGRITY_ONLY` | Package/import wiring or manifest adjustment only if required to expose the real bounded owner path; no new semantic owner or runtime surface. |
| `OUT_OF_SCOPE` | Project Spine checkpoint files, Change-2 trace files, Change-3 measurement correction, registry/database/queue/scheduler infrastructure, unrelated CLI/admin helpers, and canonical lifecycle metadata. |

```text
DEFINITION_LEVEL_SEMANTIC_OWNER_PATH_COUNT: 1
```

This is a semantic surface inventory, not an implementation sequence or patch
plan. Plan must verify the exact live call graph while preserving the single
bounded owner family.

## 32. ACCEPTANCE CRITERIA

Each criterion is Definition-level and objectively verifiable; none is an
implementation task ID.

`AC-01` — A bounded in-process lifecycle has an explicit authorized start and
fact-handoff-or-fail-closed end.

`AC-02` — A real self-hosted production entry path invokes the lifecycle for an
already-authorized OperationGuidance bound to an existing Attempt.

`AC-03` — `AttemptRecordV1.attempt_id` remains the sole canonical operation
identity and is attributable across the full governed runtime chain.

`AC-04` — The lifecycle uses existing guidance and authorization contracts and
does not move routing, shaping, planning, Attempt, or authorization authority.

`AC-05` — Existing execution authority is activated through its contract while
execution semantics remain outside the lifecycle.

`AC-06` — The real lifecycle path proves receipt existence, same-Attempt
association, and structural/contractual validation as separate facts.

`AC-07` — Valid runtime facts reach the existing PL08 evaluator through
canonical boundaries, while `PL08_IS_EVALUATOR_NOT_PUMP` remains true.

`AC-08` — Downstream facts reach existing resume/next-gate machinery without
the lifecycle selecting or authorizing a next gate.

`AC-09` — Missing identity, broken continuity, unavailable execution,
inadmissible receipt, failed validation, or failed downstream handoff stops the
lifecycle fail-closed and identifies the first broken seam.

`AC-10` — Lifecycle success means valid coordination and fact handoff only; it
does not imply Target completion, Change completion, PL08 PASS, or journey
PASSING.

`AC-11` — Runtime lifecycle state is bounded in-process and no persistent
lifecycle state, database, registry, queue, or event store is introduced.

`AC-12` — No scheduler, worker pool, distributed coordinator, or new subsystem
boundary is introduced.

`AC-13` — The authority matrix remains unchanged and
`AUTHORITY_TRANSFER: NONE` is demonstrable.

`AC-14` — Retry identity, single-active concurrency, synchronous execution,
and process/host boundaries follow the empirical model without auto-retry.

`AC-15` — Change-2 F01/F02/F03 and semantic trace persistence remain hard
out-of-scope, and Change 2 remains `BLOCKED / VALID / PAUSED`.

`AC-16` — Change-3 measurement correction is not a prerequisite.

`AC-17` — Local proof and System Traversability non-regression proof exercise
the real self-hosted journey and establish at least the required
`WIRED_TRAVERSABLE` delta without claiming `PASSING` prematurely.

`AC-18` — The implementation is not accepted when a lifecycle helper exists
without production binding, same-Attempt proof, receipt proof, PL08 handoff,
and downstream next-gate non-authority proof.

```text
ACCEPTANCE_CRITERIA_COUNT: 18
```

## 33. CLOSURE CRITERIA

The Change may close only when all of the following are satisfied:

`CC-01` — The implemented bounded primitive matches this Definition's
start/end, responsibility, lifetime, and authority boundaries.

`CC-02` — A real self-hosted production binding is demonstrated; an unused
helper or unit-test-only path is explicitly insufficient.

`CC-03` — One canonical Attempt identity is proven across guidance, activation,
execution, receipt, evaluation handoff, and downstream fact handoff.

`CC-04` — The receipt actually produced and consumed by the real path is
validated and proven to belong to the same Attempt.

`CC-05` — Real lifecycle output reaches the existing PL08 evaluator without
making PL08 a pump or transferring evaluation authority.

`CC-06` — Real lifecycle output reaches the existing resume/next-gate surface
without the lifecycle deciding or returning authoritative next-gate truth.

`CC-07` — Required broken-continuity cases fail closed with first-seam facts,
without invented retry or recovery policy.

`CC-08` — Static and/or structural evidence proves no persistent lifecycle
state, registry, scheduler, database, distributed coordinator, new subsystem,
authority transfer, or Change-2 trace retention was introduced.

`CC-09` — Local proof and self-hosted System Traversability smoke establish the
required minimum state delta to `WIRED_TRAVERSABLE` and non-regression of the
closed System Traversability contract.

`CC-10` — Closure is recorded independently of Change 2 and does not weaken
the existing Change-2 resume conjunction or substitute for fresh Formal
Readiness and separate implementation authorization.

```text
CLOSURE_CRITERIA_COUNT: 10
```

## 34. PLAN-TIME ARCHITECTURE STOP

Implementation Planning must stop and obtain owner adjudication if it
discovers a need for any of the following:

- durable lifecycle state, lifecycle database, or persistent state machine;
- new registry, database, queue, worker pool, or scheduler;
- distributed runtime coordinator or host-wide lifecycle bridge;
- a semantic owner other than the bounded PL09 Safe Orchestration family;
- route, operation, execution, evidence, evaluation, receipt, or next-gate
  authority transfer;
- PL08 as runtime pump or PL07 as runtime owner;
- merged Change-2 behavior, semantic trace persistence, or trace analytics;
- a new Roadmap vertebra;
- a materially different operation identity, trace ID replacement, or
  persistent lifecycle ID;
- a prerequisite dependency on Change 3;
- a claim that the prerequisite alone establishes `PASSING` without the
  required full conjunction;
- any other architecture or material semantic decision not frozen here.

The STOP is a governance condition, not an invitation to enlarge this Change.

## 35. DEFINITION / PLAN BOUNDARY

This candidate freezes:

- what the bounded lifecycle must make true;
- the canonical Attempt identity and continuity invariant;
- lifecycle start and termination boundaries;
- authority ownership and prohibited transfers;
- responsibilities and non-responsibilities;
- runtime, persistence, retry, concurrency, async, process, and host bounds;
- receipt, PL08, next-gate, Change-2, Change-3, and System Traversability
  contracts;
- production binding, false-done resistance, acceptance, and closure proofs;
- prohibited architecture and Plan-time STOP conditions.

This candidate leaves ordinary implementation mechanics to Plan:

- exact helper/function/class names;
- private state representation where semantically equivalent;
- exact adapter decomposition and call ordering inside the frozen sequence;
- import/export wiring;
- test function names and patch sequence;
- ordinary local data layout that does not create a new identity or authority.

Plan may not use this boundary to reopen a material semantic or architectural
choice. Any such discovery triggers the Architecture STOP.

## 36. OPEN QUESTIONS

```text
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_MATERIAL_SEMANTIC_CHOICES: 0
OPEN_MATERIAL_QUESTIONS: NONE
```

The exact private symbol names, ordinary adapter decomposition, and final
mechanical import wiring are Plan-level choices. They do not alter the frozen
semantic contract. No new operation identity, persistence model, authority
owner, topology, or journey delta remains open.

## 37. DEFINITION CANDIDATE VERDICT

```text
DEFINITION_CANDIDATE_STATUS: DERIVED / NONAUTHORITATIVE / CHANGE DEFINITION CANDIDATE
DEFINITION_CANDIDATE_READY: YES
VERDICT: PREPARED_FOR_INDEPENDENT_REVIEW
CANONICALIZATION: NOT_AUTHORIZED_BY_THIS_GATE
IMPLEMENTATION_PLAN: NOT_AUTHORIZED
FORMAL_READINESS: NOT_AUTHORIZED
IMPLEMENTATION: NOT_AUTHORIZED
```

The candidate is sufficiently bounded for a deterministic Plan without a new
architecture or material semantic decision. Independent review is required
before any canonicalization or later gate.

## 38. TERMINAL RECEIPT

```text
PL09_GOVERNED_OPERATION_LIFECYCLE_CHANGE_DEFINITION_SHAPING
OVERALL: PASS_DEFINITION_CANDIDATE_PREPARED
EXECUTOR: GPT-5.6_LUNA_EXTRA_HIGH
ENTRY_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
EMPIRICAL_DISCOVERY_SHA256: 27EC4B2B898E749D45CF1839450A6BCBD10C082132E0D0B9A528A72C60C9ED8F
EMPIRICAL_TOPOLOGY: TOPOLOGY_B_NEW_BOUNDED_IN_PROCESS_LIFETIME_PRIMITIVE_REQUIRED
PRIMARY_OPERATION_IDENTITY: AttemptRecordV1.attempt_id
LIFECYCLE_MODEL: BOUNDED_IN_PROCESS
PERSISTENT_RUNTIME_STATE: NO
NEW_SUBSYSTEM: NO
NEW_REGISTRY: NO
SCHEDULER: NO
AUTHORITY_TRANSFER: NO
PL08_IS_PUMP: NO
NEXT_GATE_AUTHORITY_TRANSFER: NO
CHANGE2_SCOPE_SEPARATION: PASS
CHANGE3_PREREQUISITE: NO
AFFECTED_CRITICAL_JOURNEY: PL_SELF_HOSTED_GOVERNED_OPERATION
INITIAL_JOURNEY_STATE: WIRED_FAIL / ORCHESTRATION_GAP
EXPECTED_JOURNEY_DELTA: WIRED_FAIL / ORCHESTRATION_GAP -> WIRED_TRAVERSABLE at OperationGuidance seam; no PASSING claim
PRODUCTION_BINDING_REQUIRED: YES
SAME_ATTEMPT_CONTINUITY_REQUIRED: YES
FALSE_DONE_RESISTANCE: DEFINED
ACCEPTANCE_CRITERIA_COUNT: 18
CLOSURE_CRITERIA_COUNT: 10
DEFINITION_LEVEL_SEMANTIC_OWNER_PATH_COUNT: 1
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_MATERIAL_SEMANTIC_CHOICES: 0
PLAN_TIME_ARCHITECTURE_STOP: PRESENT
DEFINITION_CANDIDATE_READY: YES
SOURCE_MUTATIONS: 0
STAGED_PATHS: 0
COMMIT: NO
PUSH: NO
CHANGE_2: BLOCKED / VALID / PAUSED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
CANDIDATE: .local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_CHANGE_DEFINITION_CANDIDATE.md
CANDIDATE_SHA256: COMPUTED_AFTER_WRITE_AND_REPORTED_IN_TERMINAL_RECEIPT
NEXT_SINGLE_GATE: FRESH_INDEPENDENT_REVIEW_PL09_GOVERNED_OPERATION_LIFECYCLE_CHANGE_DEFINITION
```

The empirical topology requires one new bounded in-process lifecycle primitive
inside the existing PL09 Safe Orchestration family. AttemptRecordV1.attempt_id
remains the sole canonical operation identity. The lifecycle coordinates
existing guidance, execution, receipt, PL08, and resume contracts without
acquiring their authority. Its runtime state is ephemeral, synchronous, and
nonpersistent. The real self-hosted production binding is mandatory, so an
unused helper cannot satisfy closure. The minimum expected Critical Journey
delta is `WIRED_FAIL / ORCHESTRATION_GAP` to `WIRED_TRAVERSABLE`, not `PASSING`.
Change 2 and Change 3 remain outside this prerequisite. The next gate is fresh
independent review of this candidate.
