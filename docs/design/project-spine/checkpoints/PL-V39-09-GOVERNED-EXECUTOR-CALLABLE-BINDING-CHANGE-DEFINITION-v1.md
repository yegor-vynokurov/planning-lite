# PL-V39-09 Governed Executor Callable Binding — Approved Change Definition v1

Status: CANONICAL / APPROVED CHANGE DEFINITION

## 1. CHANGE IDENTITY

CHANGE_ID: CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001
NAME: PL09 Governed Executor Callable Binding
CAPABILITY: GOVERNED_EXECUTOR_CALLABLE_BINDING
CAPABILITY_KIND: BOUNDED_SYNCHRONOUS_EXECUTION_ADAPTER
ROADMAP_EFFECT: NO_NEW_VERTEBRA
MAJOR_PL09_NEXT_SLICE_GATE: PRESERVED / UNCONSUMED
DEFINITION_STATUS: CANONICAL / APPROVED CHANGE DEFINITION
OWNER_DECISION: APPROVE_PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_CHANGE_DEFINITION
APPROVAL_DATE: 2026-09-22

This Definition is the canonical semantic boundary for the Change. It is
approved for Plan preparation only. It is not an Implementation Plan and does
not authorize source mutation, test mutation, runtime execution, Formal
Readiness, staging, commit, push, or release.

## 2. AUTHORITY AND LINEAGE

Owner approval gate:
OWNER_APPROVAL_PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_CHANGE_DEFINITION

Owner decision:
APPROVE_PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_CHANGE_DEFINITION

Entry HEAD:
e5cf0eb42509a4193550f77a0a6634cca556e91c

Empirical discovery:
.local/work/experiments/PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_EMPIRICAL_DISCOVERY.md

Empirical discovery SHA256:
BBB0B15EC47077175BF2F909ABA3D4F3250BB8C71C82425C9714491491D531CE

Empirical discovery verdict:
PASS_NO_EXISTING_CALLABLE_NEW_BOUNDED_BINDING_REQUIRED

Approved shaping:
.local/work/experiments/PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_SHAPING.md

Shaping full-file SHA256:
FF8DEEDA0E8027A84B8088AA1672FCBBCB3546613B8AC23F66BCF4BF40BB76B4

Shaping self-excluding normalized SHA256:
253A807FCB9E2481798E1D87966DB724142753D089C4E08426EF892DD2E3A712

Shaping digest convention:
UTF-8 / LF bytes with the line declaring SHAPING_ARTIFACT_SHA256 omitted.
The full-file and self-excluding digests are distinct identities.

Closed prerequisite: Attempt Action Authorization
CLOSED / COMPLETE

Closed prerequisite: Attempt Runtime Access
CLOSED / COMPLETE

Attempt Runtime Closure:
docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CLOSURE-v1.md

Attempt Runtime Closure SHA256:
3E96782EC6F70DB5F6835CDEB90F4E2EE2AEF4E92AC8CC21F463E639CC101A6E

Neither prerequisite is reopened, amended, or reinterpreted by this Change.

## 3. PROBLEM STATEMENT

The repository has authoritative Attempt Runtime access, PL07 guidance
selection, RunReceipt capture and validation surfaces, and PL08 evaluation,
but has no production callable that performs one already-authorized,
already-selected operation invocation while preserving exact Attempt identity
and deterministic same-invocation receipt association.

The absence is a wiring gap at the Governed Executor Callable Binding seam.
Existing Attempt Runtime operations are state and fact boundaries, PL07 is a
pure route/guidance projection, telemetry is an evidence boundary, and PL08
is an evaluation boundary. None is an executor callable, and no current
production host bridge satisfies the missing seam.

## 4. OBJECTIVE

Add one bounded synchronous callable production boundary that executes exactly
one authorized operation and returns typed execution and evidence facts
without taking ownership of:

- execution authorization;
- route selection;
- Attempt state;
- lifecycle sequencing;
- telemetry authority;
- PL08 evaluation;
- retry policy;
- Project Spine or next-gate state.

The callable must be reusable by the future Governed Operation Lifecycle while
remaining independently closable through a real production-equivalent host
proof. The Change must not claim that the full self-hosted governed-operation
journey is passing.

## 5. SEMANTIC OWNER

OWNER_PATH: src/planning_lite/governed_executor.py
PUBLIC_SYMBOL: invoke_governed_operation
PUBLIC_CONTRACT_FAMILY: GovernedExecutionRequestV1 / GovernedExecutionResultV1

The new bounded module is the semantic owner of the lifecycle-facing callable
contract. Exact Python field representation, exception mechanics, payload
serialization, host launch plumbing, and capture-summary projection remain
Implementation Plan choices within this Definition.

The module must expose one complete bounded invocation seam rather than
low-level storage, receipt-file, Attempt Runtime, or host-process half
operations.

## 6. CALLABLE LIFETIME

The required lifetime is:

one call
-> validation or rejection
-> one host invocation if accepted
-> one deterministic execution outcome
-> same-invocation receipt association or explicit evidence failure
-> return.

SYNCHRONOUS: YES
PERSISTENT_EXECUTOR_STATE: NO
BACKGROUND_WORKER: NO
QUEUE: NO
LEASE: NO
SCHEDULER: NO
REGISTRY: NO
DAEMON: NO

One public call represents one invocation only. No pending, background, or
long-lived executor state is returned or retained.

## 7. EXECUTION AUTHORITY BOUNDARY

Execution coordination is not execution authority:

EXECUTION_COORDINATION != EXECUTION_AUTHORITY

The binding consumes already-established execution authority supplied by the
owner/Change lifecycle contract and projected into the selected guidance and
request. It may validate authority provenance and scope. It may not grant,
reconstruct, broaden, substitute, or infer execution authority.

NEW_EXECUTION_AUTHORIZATION_MODEL: NO
EXECUTION_AUTHORITY_TRANSFER: NO

No AuthorizationAction.EXECUTION, execution token registry, second authority
model, or self-authorization path is introduced by this Definition.

## 8. PL07 ROUTE AND GUIDANCE BOUNDARY

PL07 remains the sole authority for:

- operation selection;
- route identity;
- capability class;
- expected result;
- STOP references;
- authority references.

Input shape:
FULL_IMMUTABLE_OPERATION_GUIDANCE_V1

The binding consumes the already-selected guidance snapshot. It must not call
the guidance selector, inspect a new ResumeContext, reinterpret
next_permitted_action, or select a different capability class.

EXECUTOR_SELECTS_ROUTE: NO
EXECUTOR_RESELECTS_GUIDANCE: NO
ROUTE_AUTHORITY_TRANSFER: NO

The supplied guidance must be a matched and authorized projection with the
operation, route, authority, task, verification, result, stop, escalation, and
next-gate references required by the call. The binding does not make a new
route decision.

## 9. ATTEMPT INPUT AND AUTHORITY BOUNDARY

Attempt input shape:
FULL_ATTEMPT_RECORD_INPUT

The future lifecycle supplies the exact already-selected and already-claimed
AttemptRecordV1. The binding consumes its immutable identity and validates
continuity with the supplied guidance, payload, host invocation, result, and
receipt refs.

The binding:

- consumes the exact Attempt record;
- preserves AttemptRecordV1.attempt_id;
- rejects cross-Attempt facts;
- never discovers the latest or current Attempt;
- never claims an Attempt;
- never terminalizes an Attempt;
- never invokes owner recovery;
- never repairs or resets runtime state.

EXECUTOR_OWNS_ATTEMPT_SOURCE: NO
EXECUTOR_OWNS_ATTEMPT_CLAIM: NO
EXECUTOR_OWNS_ATTEMPT_RUNTIME_STATE: NO
ATTEMPT_AUTHORITY_TRANSFER: NO

Attempt Runtime remains the sole owner of Attempt occurrence truth, exact
lookup, admissibility, claim, normal terminalization, and explicit owner
recovery.

## 10. EXECUTION PAYLOAD BOUNDARY

Semantic payload source:
EXPLICIT_OWNER_OR_LIFECYCLE_SUPPLIED_BOUNDED_TASK_PAYLOAD_BOUND_TO_GUIDANCE_TASK_BINDING_REFS

The request carries an explicit immutable bounded task or operation payload.
The payload is bound to the exact Attempt task identity and to the task
binding references in the selected guidance. Reference resolution, if used,
must be exact and fail closed.

The binding must not read arbitrary chat text, session history, ambient
conversation, latest files, or current prose as an execution contract.

AMBIENT_CHAT_IS_EXECUTION_CONTRACT: NO
ARBITRARY_MODEL_OR_EFFORT_SELECTION_BY_EXECUTOR: NO

No fuzzy, latest, temporal, or reconstructed payload resolution is permitted.

## 11. HOST PROJECTION AND ADAPTER ARCHITECTURE

The request may carry already-selected host, model, and effort facts needed
mechanically by the current host profile. The binding consumes these facts and
does not independently select them.

HOST_ADAPTER_SHAPE:
HOST_NEUTRAL_PUBLIC_CONTRACT + CURRENT_HOST_PRIVATE_ADAPTER

The lifecycle-facing public contract is host-neutral and typed. The private
adapter is bounded to the current Codex/VS Code host profile and existing
receipt-capture surface. It translates the approved execution projection,
invokes one supported host mechanism, receives completion or failure facts,
and invokes the existing capture producer for that same host invocation.

GENERIC_PLUGIN_REGISTRY: NO
MULTI_PROVIDER_FRAMEWORK: NO
BACKEND_DISCOVERY_SYSTEM: NO

The current repository has no existing host launch callable. Implementation
Planning must identify the real current-host path, but it may not introduce a
generic multi-host architecture to compensate.

## 12. PUBLIC RESULT CONTRACT

The public result contract family is:

GovernedExecutionResultV1

The result must carry, semantically:

- exact attempt_id;
- ephemeral execution_invocation_id;
- invocation accepted or rejected state;
- deterministic execution outcome;
- result identity when an execution fact exists;
- host invocation reference when available;
- bounded changed-path, fact, and artifact references when authoritative;
- exact receipt reference or references;
- one bounded failure category when the result is not a clean completion.

The exact Python field layout is Plan-owned. The public result is a typed fact
carrier and reference set. It does not expose receipt files, storage paths,
Attempt Runtime JSON, lifecycle state, or next-gate operations.

Accepted calls return one terminal execution or evidence outcome. Rejected
calls do not fabricate execution or receipt facts.

## 13. EXECUTION INVOCATION IDENTITY

EXECUTION_INVOCATION_ID_REQUIRED: YES
IS_SECOND_ATTEMPT_IDENTITY: NO

The invocation ID is:

- ephemeral;
- generated before host invocation;
- scoped to one bounded executor call;
- bound in memory to the exact Attempt and selected guidance;
- returned with execution and receipt facts;
- not persisted in a second executor store;
- not a replacement for AttemptRecordV1.attempt_id.

Existing host session, turn, invocation-index, and receipt identities remain
host or telemetry identities. The new invocation ID is the local association
key that prevents post-hoc receipt matching.

## 14. FAILURE SEMANTICS

The bounded failure categories are:

- EXECUTOR_UNAVAILABLE: the required current host adapter cannot be reached
  before invocation.
- INVOCATION_REJECTED: request, guidance, authority, payload, or precondition
  is rejected before host execution.
- HOST_INVOCATION_FAILED: the host boundary fails before a valid execution
  fact is returned.
- EXECUTION_FAILED: the accepted host invocation returns a valid failed
  execution fact.
- EXECUTION_INTERRUPTED: the accepted host invocation returns an interruption
  or loss fact; this is ordinary execution evidence, not owner recovery.
- INVALID_EXECUTION_RESULT: the host result is malformed, unsupported, or
  internally inconsistent.
- ATTEMPT_IDENTITY_MISMATCH: request, host result, receipt, or returned facts
  do not carry the exact Attempt identity expected by the call.
- RECEIPT_MISSING: required same-invocation receipt evidence is absent.
- RECEIPT_INVALID: receipt evidence fails the existing RunReceipt contract.
- RECEIPT_ATTEMPT_ASSOCIATION_MISMATCH: the receipt ref does not belong to
  the exact host invocation associated with this Attempt.

The taxonomy remains intentionally bounded. Implementation Planning may choose
exact enum spelling but may not collapse materially different authority,
execution, identity, or evidence semantics.

## 15. RETRY AND RECOVERY BOUNDARY

EXECUTOR_BINDING_OWNS_RETRY_POLICY: NO

The binding performs one bounded invocation. Retry, recheck, escalation,
recovery, and next-gate decisions remain explicit lifecycle or control
decisions.

An ordinary executor-produced INTERRUPTED outcome is ordinary terminal
execution evidence. It is not owner-authorized recovery and must not be routed
through resolve_interrupted_attempt.

## 16. RUNRECEIPT OWNER BOUNDARY

Existing telemetry and capture surfaces remain owners of:

- receipt production mechanics;
- RunReceipt validation;
- append-only storage;
- receipt stream consistency.

The binding must not become telemetry authority, invent receipt IDs, write
arbitrary telemetry records, or treat receipt evidence as execution authority.

TELEMETRY_AUTHORITY_TRANSFER: NO
RECEIPT_PRODUCTION != RECEIPT_VALIDATION
RECEIPT_VALIDATION != EXECUTION_AUTHORITY
TELEMETRY != LIFECYCLE

## 17. RUNRECEIPT RESPONSIBILITY

The binding responsibility is:

INVOKE_EXISTING_CAPTURE_PRODUCER_FOR_THE_SAME_BOUNDED_HOST_INVOCATION_AND_RETURN_EXACT_RECEIPT_REFS

The binding invokes the existing capture producer at the end of the same
bounded host call, supplies the exact host rollout/session/turn/invocation
facts for that call, and projects the exact returned receipt IDs into the
typed result.

The binding must not:

- invent receipt IDs;
- select the latest receipt;
- search receipts after the fact;
- match by timestamp or task alone;
- write arbitrary telemetry records directly.

## 18. SAME-ATTEMPT RECEIPT ASSOCIATION

SAME_ATTEMPT_RECEIPT_ASSOCIATION: INVOCATION_LOCAL
POST_HOC_RECEIPT_MATCHING: NO
RUNRECEIPT_SCHEMA_CHANGE_REQUIRED: NO

The association mechanism is:

exact Attempt
-> ephemeral execution invocation ID
-> exact host invocation/session/turn facts
-> capture in the same bounded execution call
-> exact returned receipt references.

The result carries Attempt ID, invocation ID, host invocation reference, and
receipt references together. The future lifecycle validates those facts and
includes the receipt references in the terminal evidence supplied to
Attempt Runtime.

RunReceipt v1 remains unchanged. The association is carried by the
invocation-local typed result and the exact evidence reference; no
latest/time/task-only post-hoc matching is permitted.

If Implementation Planning proves that this approved invocation-local
association cannot satisfy exact identity without a RunReceipt schema change,
Planning must stop for owner adjudication under
PLAN_ARCHITECTURE_STOP_OWNER_ADJUDICATION_REQUIRED. It must not silently amend
telemetry.

## 19. RESULT CONTRACT REUSE AND OBSERVEDRESULT OWNERSHIP

EXECUTOR_RESULT_CONTRACT_REUSE: PARTIAL

ObservedResultV1 is not the raw host return. It remains the Attempt Runtime
terminal fact carrier with exact Attempt identity and supported terminal
statuses.

OBSERVED_RESULT_ROLE:
FUTURE_LIFECYCLE_CONSTRUCTS_OBSERVED_RESULT_V1_FROM_VALIDATED_EXECUTOR_FACTS_AT_ATTEMPT_RUNTIME_TERMINALIZATION

The future lifecycle receives the executor result, validates identity and
receipt evidence, constructs ObservedResultV1 with the exact Attempt ID and
result ID, and passes it to Attempt Runtime.

## 20. TERMINALIZATION BOUNDARY

TERMINALIZATION_CALL_OWNER: FUTURE_GOVERNED_OPERATION_LIFECYCLE

The required relationship is:

executor facts
-> lifecycle validates identity and evidence
-> lifecycle constructs ObservedResultV1
-> lifecycle calls Attempt Runtime normal terminalization.

The executor binding does not terminalize, persist, recover, or mutate the
Attempt. Normal executor failure and interruption are terminal facts; explicit
owner recovery remains a separate authorization operation.

## 21. PL08 BOUNDARY

EXECUTOR_OWNS_PL08_HANDOFF: NO
PL08_AUTHORITY_TRANSFER: NO

The executor binding returns facts only. The future lifecycle later supplies
the validated Attempt and evidence bundle to
src/planning_lite/attempt_evaluation.py::evaluate_technical.

The evaluator is not an executor, and telemetry evidence is not evaluation or
execution authority.

## 22. LIFECYCLE BOUNDARY

Required direction:

Lifecycle -> Governed Executor Callable Binding

Forbidden direction:

Executor -> Lifecycle

EXECUTOR_OWNS_LIFECYCLE: NO

The future Governed Operation Lifecycle owns orchestration order: exact
Attempt preparation and claim, guidance acceptance, one binding call, result
and evidence validation, Attempt terminalization, PL08 handoff, and next-gate
decision. The binding returns one result and does not call back into the
lifecycle or choose continuation.

## 23. CLI AND OWNER INTERACTION BOUNDARY

Future production topology:

VS Code chat agent / owner instruction
-> trusted local application/control plane
-> planning-lite execute
-> Governed Operation Lifecycle
-> Governed Executor Callable Binding.

CLI_PATH_IN_EXECUTOR_BINDING_CHANGE: NO

This Change does not add planning-lite execute or modify src/planning_lite/cli.py.
The CLI-to-lifecycle integration belongs to later lifecycle work.

PRIMARY_OWNER_INTERACTION_STYLE: VS_CODE_CHAT_AGENT
MANUAL_CLI_TYPING_REQUIRED_FROM_OWNER: NO
NEW_VS_CODE_EXTENSION_REQUIRED: NO
NEW_CHAT_SUBSYSTEM_REQUIRED: NO
CHAT_TEXT_ALONE_IS_MACHINE_AUTHORIZATION: NO
OWNER_DECISION_AUTHORITY_TRANSFER_TO_AGENT: NO
DIRECT_CLI_EXECUTOR_BINDING: NO

## 24. PERSISTENCE AND SUBSYSTEM BOUNDARY

NEW_SUBSYSTEM: NO
PERSISTENCE: NO
REGISTRY: NO
SCHEDULER: NO
DAEMON: NO
BACKGROUND_WORKER: NO
QUEUE: NO
LEASE: NO

No durable executor store, receipt database/service, worker, queue, scheduler,
registry, daemon, RPC layer, or generic workflow engine is introduced.
Existing Attempt Runtime and telemetry owners retain their own durable state.

## 25. CHANGE-2 AND CHANGE-3 BOUNDARIES

MEASUREMENT_CORRECTION_ABSORBED: NO

Token, effort, delta, and other PL08 RunReceipt measurement correction remains
separate Change-3 work.

CHANGE_2_TRACE_REQUIRED_FOR_EXECUTOR_BINDING: NO

Compact Semantic Operation Trace is not used to retroactively infer Attempt
and receipt association. Same-Attempt association exists through the approved
invocation-local mechanism before Change-2.

## 26. SYSTEM TRAVERSABILITY OBLIGATION

Current seam:

GOVERNED_EXECUTOR_CALLABLE_BINDING / WIRING_GAP

Expected local closure delta:

NO_CALLABLE_PRODUCTION_EXECUTOR
-> CALLABLE_PRODUCTION_EXECUTOR_BINDING_AVAILABLE

This Change does not make the full
PL_SELF_HOSTED_GOVERNED_OPERATION journey PASSING. Lifecycle orchestration,
terminalization, receipt evidence handoff, PL08 evaluation, and next-gate
traversal remain later seams.

tests/test_system_traversability.py remains unchanged in this Change because
the full journey is not yet wired.

## 27. PRODUCTION-EQUIVALENT CLOSURE PROOF

EXECUTOR_BINDING_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: YES
PERSISTENT_UPSTREAM_CALLER_REQUIRED_FOR_CLOSURE: NO
REAL_PRODUCTION_HOST_PATH_PROOF_REQUIRED: YES

Independent closure requires a production-equivalent integration proof that
directly invokes:

real public callable
-> real current-host private adapter
-> real capture producer
-> deterministic typed result
-> exact same-invocation receipt reference or references.

A durable upstream lifecycle or CLI caller is not required for independent
executor-binding closure. A fake host, test-only helper, or unused callable is
insufficient.

## 28. LIFECYCLE IMPACT

EXECUTOR_BINDING_CAN_CLOSE_BEFORE_LIFECYCLE_IMPLEMENTATION: YES
LIFECYCLE_PLANNING_RESUME_AFTER_EXECUTOR_CLOSURE: YES
LIFECYCLE_DEFINITION_IMPACT: NO_CHANGE

The existing lifecycle Definition already requires a real executor binding and
the desired Lifecycle -> Binding direction. This Change adds no semantic
redesign to that Definition. Lifecycle planning may resume after this
prerequisite is independently closed and the next gate authorizes it.

## 29. DEFINITION-LEVEL PRODUCTION SURFACE

Authorized future implementation surface at Definition level:

Production:

ADD: src/planning_lite/governed_executor.py

Tests:

ADD: tests/test_governed_executor.py

Read-only dependencies may include:

- src/planning_lite/attempt_runtime.py;
- src/planning_lite/attempt_evaluation.py;
- src/planning_lite/execution_guidance.py;
- src/planning_lite/telemetry.py;
- scripts/capture_codex_run_receipts.py;
- template/.planning/adapters/codex/README.md.

The surface budget does not authorize a final path list, source edits, test
edits, lifecycle module creation, CLI modification, telemetry schema change,
or host implementation. Those require separately authorized Implementation
Planning and subsequent gates.

## 30. ACCEPTANCE CRITERIA

Exactly twelve acceptance criteria are frozen.

AC-01. A real importable production callable exists at
src/planning_lite/governed_executor.py::invoke_governed_operation.

AC-02. A real current-host path exercises the callable and returns a
deterministic typed result; a dead helper or test-only fake is insufficient.

AC-03. The exact supplied AttemptRecordV1.attempt_id is preserved and
cross-Attempt input or result facts are rejected.

AC-04. The supplied OperationGuidanceV1 is consumed unchanged; no route
selection or guidance reselection occurs inside the binding.

AC-05. Existing execution authority is consumed without grant, reconstruction,
broadening, substitution, or transfer.

AC-06. One call yields one deterministic bounded typed result distinguishing
accepted/rejected invocation and terminal or failure classes.

AC-07. Same-invocation capture yields exact receipt references without latest,
time-based, task-only, or post-hoc matching.

AC-08. Missing, invalid, or mismatched receipt evidence fails closed.

AC-09. The binding performs no retry, background work, persistence, scheduler,
registry, daemon, queue, or lifecycle callback.

AC-10. A future lifecycle can construct ObservedResultV1 and terminalize the
Attempt without changing the executor contract or moving Attempt Runtime
authority.

AC-11. Negative coverage includes unavailable host, rejected request,
authority/guidance mismatch, Attempt mismatch, invalid result, missing receipt,
invalid receipt, and receipt association mismatch.

AC-12. The public result exposes typed facts and references, not storage paths,
receipt files, runtime JSON, or next-gate operations.

AC_COUNT: 12

## 31. CLOSURE CRITERIA

Exactly ten closure criteria are frozen.

CC-01. The public callable and a real production-host path are identified and
proven together.

CC-02. A clean integration probe preserves exact Attempt ID, invocation ID,
result ID, and host invocation identity.

CC-03. The same bounded call produces and validates exact receipt references
without post-hoc selection.

CC-04. Executor facts can be projected to ObservedResultV1 without moving
Attempt Runtime authority.

CC-05. Identity, host, result, and evidence negative cases fail closed.

CC-06. No route reselection, authorization grant, Attempt claim or store write,
retry, lifecycle callback, PL08 call, or next-gate mutation occurs inside the
binding.

CC-07. The Codex-specific adapter remains private and no provider/plugin
hierarchy is added.

CC-08. Invocation remains synchronous and bounded with no executor persistence
or background worker.

CC-09. RunReceipt schema remains unchanged and telemetry remains the
validation/storage owner.

CC-10. Focused owner/product tests and existing owner regressions pass.

CC_COUNT: 10

## 32. STOP CONDITIONS

Implementation Planning or implementation must stop for owner adjudication if
any of the following becomes necessary:

- a new execution authorization model;
- a second Attempt identity;
- Attempt discovery through latest/current semantics;
- route selection inside the executor;
- persistent executor state;
- worker, queue, scheduler, daemon, or lease;
- generic plugin/provider registry;
- RunReceipt schema mutation;
- post-hoc receipt matching;
- executor-owned retry policy;
- executor ownership of lifecycle;
- direct CLI-to-executor topology;
- executor-owned Attempt terminalization;
- PL08, telemetry, or next-gate authority transfer;
- Change-2 or Change-3 absorption;
- a new Roadmap vertebra.

The prescribed planning stop is:

PLAN_ARCHITECTURE_STOP_OWNER_ADJUDICATION_REQUIRED

## 33. EXPLICIT NON-GOALS

This Change does not include:

- Governed Operation Lifecycle implementation;
- planning-lite execute;
- Change-2 Compact Semantic Operation Trace;
- Change-3 measurement correction;
- a new receipt database or telemetry service;
- a host plugin or provider framework;
- multi-provider routing;
- background execution;
- retries;
- a generic workflow engine;
- Project Spine mutation;
- next-gate selection;
- raw conversation or prompt retention;
- source or test mutation under this Definition gate;
- Definition Activation beyond the separately authorized activation artifact;
- Formal Readiness, implementation, staging, commit, push, or release.

## 34. DEFINITION / PLAN / IMPLEMENTATION AUTHORIZATION

The owner approval grants:

CHANGE_DEFINITION: APPROVED
PLAN_PREPARATION: AUTHORIZED

The owner approval does not grant:

PLAN_APPROVAL: NOT GRANTED
FORMAL_READINESS: NOT AUTHORIZED
IMPLEMENTATION: NOT AUTHORIZED
SOURCE_MUTATION: NOT AUTHORIZED
TEST_MUTATION: NOT AUTHORIZED
COMMIT: NOT AUTHORIZED
PUSH: NOT AUTHORIZED

The next gate prepares a derived noncanonical Implementation Plan candidate
only. No implementation may begin from this Definition or its Activation.

## 35. PRESERVED CROSS-CHANGE STATE

CURRENT_MUTATION: NO
CURRENT.md: UNCHANGED

CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001:
DEFINITION_APPROVED / PLANNING_BLOCKED_BY_EXECUTOR_PREREQUISITE / IMPLEMENTATION_NOT_AUTHORIZED

CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001:
BLOCKED / VALID / PAUSED

MAJOR_PL09_NEXT_SLICE_GATE:
PRESERVED / UNCONSUMED

## 36. DEFINITION FIDELITY REVIEW

SHAPING_TO_DEFINITION_FIDELITY: PASS

The canonical Definition preserves, without semantic drift:

- owner path src/planning_lite/governed_executor.py;
- public symbol invoke_governed_operation;
- full Attempt record input;
- full immutable OperationGuidanceV1 input;
- explicit owner/lifecycle bounded payload;
- host-neutral public contract plus current-host private adapter;
- existing capture producer responsibility;
- no RunReceipt schema change;
- ephemeral invocation identity;
- lifecycle-owned terminalization;
- no authority transfer;
- twelve of twelve acceptance criteria;
- ten of ten closure criteria;
- zero unresolved architecture choices.

## 37. CANONICAL DEFINITION VERDICT

DEFINITION_CANDIDATE_STATUS: CANONICAL / APPROVED CHANGE DEFINITION
DEFINITION_APPROVED: YES
DEFINITION_ACTIVATION: AUTHORIZED
PLAN_PREPARATION: AUTHORIZED
PLAN_APPROVAL: NOT GRANTED
IMPLEMENTATION_PLAN: NOT CREATED
FORMAL_READINESS: NOT RUN
IMPLEMENTATION: NOT AUTHORIZED
CANONICAL_DEFINITION_SHA256: COMPUTED_AFTER_WRITE_AND_REPORTED_IN_DEFINITION_ACTIVATION

## 38. TERMINAL RECEIPT

PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_CHANGE_DEFINITION_APPROVAL
OVERALL: PASS_DEFINITION_APPROVED_AND_ACTIVATED
EXECUTOR: GPT-5.6_LUNA_EXTRA_HIGH
ENTRY_HEAD: e5cf0eb42509a4193550f77a0a6634cca556e91c
DISCOVERY_SHA256: BBB0B15EC47077175BF2F909ABA3D4F3250BB8C71C82425C9714491491D531CE
SHAPING_FULL_FILE_SHA256: FF8DEEDA0E8027A84B8088AA1672FCBBCB3546613B8AC23F66BCF4BF40BB76B4
SHAPING_SELF_EXCLUDING_DIGEST: 253A807FCB9E2481798E1D87966DB724142753D089C4E08426EF892DD2E3A712
SHAPING_DIGEST_CONVENTIONS_DISTINCT: YES
OWNER_DEFINITION_DECISION: APPROVE
CANONICAL_DEFINITION: docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md
CANONICAL_DEFINITION_SHA256: COMPUTED_AFTER_WRITE_AND_REPORTED_IN_DEFINITION_ACTIVATION
CAPABILITY_KIND: BOUNDED_SYNCHRONOUS_EXECUTION_ADAPTER
OWNER_PATH: src/planning_lite/governed_executor.py
PUBLIC_SYMBOL: invoke_governed_operation
ATTEMPT_INPUT_SHAPE: FULL_ATTEMPT_RECORD_INPUT
GUIDANCE_INPUT_SHAPE: FULL_IMMUTABLE_OPERATION_GUIDANCE_V1
HOST_ADAPTER_SHAPE: HOST_NEUTRAL_PUBLIC_CONTRACT + CURRENT_HOST_PRIVATE_ADAPTER
RUNRECEIPT_SCHEMA_CHANGE_REQUIRED: NO
SAME_ATTEMPT_RECEIPT_ASSOCIATION: INVOCATION_LOCAL
EXECUTION_INVOCATION_ID_REQUIRED: YES
TERMINALIZATION_CALL_OWNER: FUTURE_GOVERNED_OPERATION_LIFECYCLE
NEW_AUTHORIZATION_MODEL: NO
NEW_SUBSYSTEM: NO
PERSISTENCE: NO
REGISTRY: NO
SCHEDULER: NO
EXECUTOR_BINDING_OWNS_RETRY_POLICY: NO
AC_COUNT: 12
CC_COUNT: 10
UNBOUND_ARCHITECTURE_CHOICES: 0
SHAPING_TO_DEFINITION_FIDELITY: PASS
PLAN_PREPARATION: AUTHORIZED
PLAN_APPROVAL: NOT GRANTED
IMPLEMENTATION: NOT AUTHORIZED
CURRENT_MUTATION: NO
CANONICAL_MUTATION_PATH_COUNT: 2
STAGED_PATHS: 0
COMMIT: NO
PUSH: NO
LIFECYCLE_CHANGE: DEFINITION_APPROVED / PLANNING_BLOCKED_BY_EXECUTOR_PREREQUISITE / IMPLEMENTATION_NOT_AUTHORIZED
CHANGE_2: BLOCKED / VALID / PAUSED
MAJOR_PL09_NEXT_SLICE_GATE: PRESERVED / UNCONSUMED
EXECUTOR_BINDING_CHANGE: DEFINITION_APPROVED / PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_IMPLEMENTATION_PLANNING
