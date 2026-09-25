# PL-V39-09 Compact Semantic Operation Trace — Implementation Plan Amendment v1

```text
AMENDMENT_ID: PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-PLAN-AMENDMENT-001
CHANGE_ID: CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001
AMENDMENT_KIND: IMPLEMENTATION_PLAN_AMENDMENT
AMENDMENT_STATUS: APPROVED_BY_OWNER / MATERIALIZED
OWNER_GATE: CHANGE_2_AMENDMENT_INTEGRATION_UPDATE
OWNER_DECISION: AUTHORIZE_CHANGE_2_AMENDMENT_INTEGRATION_UPDATE
ENTRY_HEAD: 15cd99ae2aad29ff7298b6a78376e81d59cd0fb6
FORMAL_READINESS: NOT RUN / FRESH REVIEW REQUIRED
IMPLEMENTATION_AUTHORIZED: NO
```

This is the smallest bounded amendment required to reconcile the immutable
Change 2 Plan with the now-real governed operation runtime. It changes the
integration call-point and dependency mapping only. It does not implement
Change 2, run Formal Readiness, grant implementation authorization, or consume
the major PL09 gate.

## 1. Predecessor authority and old readiness

```text
PREDECESSOR_DEFINITION:
docs/design/project-spine/checkpoints/PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-CHANGE-DEFINITION-v1.md
PREDECESSOR_DEFINITION_SHA256: 9E544F41C4358AA25EF5FB814EFC60518B724565A9B4B7FA4FABEB3D1B022886
DEFINITION_ACTIVATION:
docs/design/project-spine/checkpoints/PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-DEFINITION-ACTIVATION-v1.md
DEFINITION_ACTIVATION_SHA256: 6DC440822B51ECA89A817DD6F39DA45402354F9A7AB30D3FD4CFB4A2E7C31F6A
PREDECESSOR_PLAN:
docs/design/project-spine/checkpoints/PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-IMPLEMENTATION-PLAN-v1.md
PREDECESSOR_PLAN_SHA256: 953292D4EF6D3477FF45C1E8983C69677AF40ED3881616CF08C4C7718D126E31
PLAN_APPROVAL_READINESS_ENTRY:
docs/design/project-spine/checkpoints/PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-PLAN-APPROVAL-READINESS-ENTRY-v1.md
PLAN_APPROVAL_READINESS_ENTRY_SHA256: CBBD37B3791921B0572E2D196A88AEE67D5948935199B696CF09D2E71198774D
OLD_FORMAL_READINESS:
docs/design/project-spine/checkpoints/PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-FORMAL-READINESS-VERDICT-v1.md
OLD_FORMAL_READINESS_SHA256: C0885BB121FD40A79AC34DE4B9B26A9706D604F348EB1AE3B7068674C0F4A60E
OLD_FORMAL_READINESS_VERDICT: BLOCKED
OLD_FORMAL_READINESS_BLOCKER_COUNT: 1
```

The old verdict remains immutable historical evidence. It is superseded only
for a future fresh Formal Readiness review; it is not edited, overwritten, or
reclassified as a passing verdict by this amendment.

## 2. Exact blocker reconstruction

The old single material blocker was:

```text
OLD_BLOCKER_1:
The exact existing PL08 evidence workflow/caller required by F-01/F-02/F-03
was absent. Implementing the Plan required an unplanned production integration
path and an owner/call-point decision.
```

The same root blocker caused these observed readiness failures:

```text
F01_CALL_POINT: BLOCKED
F02_CALL_POINT: BLOCKED
F03_CALL_POINT: BLOCKED
F01_IMPLEMENTABLE: NO
F02_BOTH_IDENTITIES_AVAILABLE_AT_PLANNED_SEAM: NO
F03_REQUIRED_FACTS_AVAILABLE: NO
SCHEMA_READINESS: BLOCKED
BACKWARD_COMPATIBILITY: BLOCKED
PL08_PREREQUISITES: BLOCKED
UNPLANNED_SOURCE_PATH_REQUIRED: YES
UNPLANNED_PATH_COUNT: 1
```

The blocker was evidence-based and did not justify product repair at the old
gate. This amendment resolves the authority/call-point ambiguity by binding
the future trace adapter to the committed Governed Operation Lifecycle and by
keeping all source-owner boundaries explicit.

## 3. Blocker adjudication against current evidence

```text
BLOCKER_CLOSED_BY_GOVERNED_OPERATION_LIFECYCLE: YES / ROOT CALLER BOUND
BLOCKER_CLOSED_BY_SYSTEM_TRAVERSABILITY: YES / JOURNEY REACHABILITY PROVED
BLOCKER_CLOSED_BY_BOTH_REQUIRED: YES / COMBINED CURRENT EVIDENCE
GENUINELY_OPEN_MATERIAL_BLOCKER: NONE IDENTIFIED BY THIS INTEGRATION UPDATE
```

The Governed Operation Lifecycle now provides the real bounded production
occurrence that the old Plan could not locate. System Traversability confirms
that the occurrence can be traversed through all required seams. Formal
Readiness must independently re-evaluate these facts later; this artifact does
not claim its verdict.

The following assumptions remain valid without amendment:

```text
UNCHANGED_ASSUMPTION_1: PL06 remains authoritative for producer-bound context observation.
UNCHANGED_ASSUMPTION_2: PL07 remains authoritative for OperationGuidance selection.
UNCHANGED_ASSUMPTION_3: PL08 remains authoritative for Attempt, result, evaluation, findings, and rework.
UNCHANGED_ASSUMPTION_4: RunReceipt remains authoritative only for executor facts it proves.
UNCHANGED_ASSUMPTION_5: CURRENT/ACTIVE and lifecycle owners remain authoritative for state and permission.
UNCHANGED_ASSUMPTION_6: Change 3 measurement correction remains independent and not required.
UNCHANGED_ASSUMPTION_7: derived trace identity never replaces AttemptRecordV1.attempt_id.
```

## 4. Runtime closure and critical-journey binding

```text
RUNTIME_CLOSURE_ARTIFACT:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CLOSURE-v1.md
RUNTIME_CLOSURE_SHA256: 99BAE9E72AD7E9B956E099E8EC57E8E4CF456B0BC98636A1AD3CAF584AFB465F
RUNTIME_CLOSURE_STATUS: CLOSED / COMPLETE

SYSTEM_TRAVERSABILITY_ARTIFACT:
docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-CLOSURE-v1.md
SYSTEM_TRAVERSABILITY_ARTIFACT_SHA256: F051B62705C5B39D1D3AC9B9AE4D5ED42847AFB2E0AB6E5CBC09E0F83E26F05B
SYSTEM_TRAVERSABILITY_CORRECTION: CLOSED / COMPLETE

CRITICAL_JOURNEY: PL_SELF_HOSTED_GOVERNED_OPERATION
CRITICAL_JOURNEY_SMOKE: PASS
OBSERVED_TRAVERSABILITY_STATE: PASSING
FIRST_BROKEN_SEAM: NONE
GAP_CLASS: NONE
```

The accepted real path is:

```text
AttemptRecordV1
-> OperationGuidanceV1
-> Governed Operation Lifecycle
-> GovernedExecutionEnvelopeV1 / CompletionV1 / ResultV1
-> validated persisted RunReceipt
-> exact receipt readback
-> ObservedResultV1
-> Attempt terminalization
-> PL08 TechnicalEvaluation
-> authoritative next-gate projection
```

The trace observes this path by reference. It does not own the lifecycle,
receipt, evaluation, terminalization, or next-gate authority.

## 5. Exact current integration anchors

The following existing symbols are authoritative read/consume dependencies:

```text
src/planning_lite/execution_guidance.py::OperationGuidanceV1
src/planning_lite/execution_guidance.py::select_operation_guidance
src/planning_lite/execution_guidance.py::OperationBinding
src/planning_lite/attempt_evaluation.py::AttemptRecordV1
src/planning_lite/attempt_evaluation.py::ObservedResultV1
src/planning_lite/attempt_evaluation.py::evaluate_technical
src/planning_lite/governed_executor.py::GovernedExecutionEnvelopeV1
src/planning_lite/governed_executor.py::GovernedExecutionCompletionV1
src/planning_lite/governed_executor.py::GovernedExecutionResultV1
src/planning_lite/governed_executor.py::prepare_governed_operation
src/planning_lite/governed_executor.py::invoke_governed_operation
src/planning_lite/telemetry.py::validate_receipt
src/planning_lite/telemetry.py::collect_governed_receipt
src/planning_lite/attempt_runtime.py::lookup_attempt
src/planning_lite/attempt_runtime.py::check_activation_admissibility
src/planning_lite/attempt_runtime.py::claim_attempt
src/planning_lite/attempt_runtime.py::terminalize_attempt
src/planning_lite/context.py::build_observed_resume_context
src/planning_lite/context.py::OperationDepthObservationV1
```

The exact bounded integration owner/call point is:

```text
src/planning_lite/operation_lifecycle.py::execute_governed_operation
```

Its existing order is lookup, admissibility, claim, supplied matched guidance,
governed execution, typed completion/carrier validation, governed receipt
collection and readback, identity-triangle validation, ObservedResult
construction, terminalization, and `evaluate_technical`.

## 6. Amended integration mapping

The predecessor Definition semantics remain unchanged. The predecessor Plan is
amended as follows:

```text
PRE:
  consume AttemptRecordV1.attempt_id and operation_guidance_ref after the
  existing Attempt claim and supplied OperationGuidanceV1 match.
  invoke the pure trace PRE writer from the lifecycle adapter before the real
  governed execution call. Route selection remains owned by PL07.

DURING:
  consume only a genuine OperationDepthObservationV1 produced through
  context.py::build_observed_resume_context and bound by exact operation_ref.
  If no lawful observation is supplied at the bounded observation seam, record
  the explicit unavailable/incomplete reason; do not synthesize a mapping or
  infer host reads.

POST:
  invoke the pure trace POST writers from the lifecycle adapter only after the
  validated receipt/readback and existing ObservedResult/PL08 facts are
  available. Bind receipt_id, result/evaluation/finding/supersession refs, and
  the observed next-gate reference by exact Attempt identity.

TRACE_IDENTITY:
  AttemptRecordV1.attempt_id remains the canonical occurrence identity.
  Any Change 2 trace identity is derived and may not replace Attempt identity,
  RunReceipt identity, or lifecycle authority.
```

The lifecycle adapter must not reselect guidance, duplicate execution, create
a receipt, call PL08 as a runtime pump, terminalize a second time, infer a
next gate, or persist raw content.

## 7. Future implementation write surface

The predecessor three-path trace surface remains in force and is extended by
one genuine integration adapter path required to wire the now-identified
production call point:

```text
FUTURE_IMPLEMENTATION_WRITE_SURFACE_CHANGED: YES / ONE BOUNDED ADAPTER PATH
FUTURE_IMPLEMENTATION_WRITE_SURFACE:
  src/planning_lite/operation_trace.py
  src/planning_lite/operation_lifecycle.py
  template/.planning/changes/templates/progress.md
  tests/test_operation_trace.py
FUTURE_IMPLEMENTATION_WRITE_PATH_COUNT: 4
```

`operation_lifecycle.py` is an integration adapter only. It does not become a
second lifecycle, an Attempt owner, a receipt owner, a PL08 owner, or a
next-gate authority. The other listed paths retain their predecessor roles.

The following remain read/consume dependencies and are not future Change 2
write paths:

```text
READ_CONSUME_ONLY:
  src/planning_lite/governed_executor.py
  src/planning_lite/attempt_runtime.py
  src/planning_lite/telemetry.py
  src/planning_lite/attempt_evaluation.py
  src/planning_lite/context.py
  src/planning_lite/execution_guidance.py
UNBOUND_IMPLEMENTATION_CHOICES: NONE MATERIAL
```

No new database, registry, scheduler, worker, daemon, trace store, RunReceipt
schema, public authority, automatic routing, workflow chaining, raw-content
carrier, or second operation identity is introduced.

## 8. Scope and boundary preservation

```text
CHANGE2_SEMANTIC_DELTA: NONE
CHANGE2_INTEGRATION_DELTA: BIND PRE/DURING/POST TO REAL LIFECYCLE AND OWNER FACTS
CHANGE2_SCOPE_EXPANSION: NO / BOUNDED ADAPTER PATH ONLY
TRACE_AUTHORITY: DERIVED / NON-AUTHORITATIVE
ATTEMPT_RUNTIME_OWNERSHIP: NO
RECEIPT_OWNERSHIP: NO
PL08_OWNERSHIP: NO
NEXT_GATE_AUTHORITY: NO
CHANGE3_ABSORBED: NO
CHANGE3: NOT_ABSORBED
MAJOR_PL09_NEXT_SLICE_GATE: PRESERVED / UNCONSUMED
```

The existing compact semantic trace purpose remains the same: one derived
observation linking existing PRE, DURING, and POST facts without copying their
source bodies or taking authority from their owners.

## 9. Current projection and gate transition

```text
CURRENT_ALIGNMENT_REQUIRED: YES / BOUNDED CHANGE2 RESUME PROJECTION
CURRENT_CHANGED_SCOPE:
  top PLANNING_LITE_RESUME_CONTRACT_V1 block only;
  Change 2 projection updated from old missing-caller blocker to amended
  integration complete / fresh Formal Readiness pending.
IMPLEMENTATION_AUTHORIZED: NO
CHANGE_2: VALID / PAUSED_PENDING_FRESH_FORMAL_READINESS
RUNTIME_PREREQUISITE: CLOSED / COMPLETE
CRITICAL_JOURNEY: PASS / PASSING
```

The old Formal Readiness record remains historical. No `READY` verdict is
projected by this amendment.

## 10. Gate and materialization boundary

```text
DEFINITION_AMENDMENT_REQUIRED: NO
DEFINITION_ACTIVATION_REQUIRED: NO
PLAN_AMENDMENT_REQUIRED: YES
FORMAL_READINESS_EXECUTED: NO
IMPLEMENTATION_AUTHORIZATION_GRANTED: NO
PRODUCT_SOURCE_MUTATIONS: 0
TEST_MUTATIONS: 0
TEMPLATE_MUTATIONS: 0
RECOMMENDATION_INBOX_COMMITTED: NO
PUSH: NO
```

The next gate is:

```text
NEXT_SINGLE_GATE: FRESH_FORMAL_READINESS_CHANGE_2
```

Fresh Formal Readiness must verify the amended path from the committed
governance state. It owns the future `READY` or `BLOCKED` verdict.
