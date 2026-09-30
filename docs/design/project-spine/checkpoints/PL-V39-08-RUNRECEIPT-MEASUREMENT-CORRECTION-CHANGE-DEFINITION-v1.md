# PL-V39-08 RunReceipt Measurement Correction — Approved Definition v1

## 1. Change identity and approval

```text
Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-DEFINITION-001
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Lineage name: CHANGE_3
Title: RunReceipt Measurement Correction
Status: APPROVED_BY_OWNER / MATERIALIZED_PENDING_POST_MATERIALIZATION_REVIEW
Owner: PL-V39-08 telemetry / evaluation
Owner approval: USER / EXPLICIT / 2026-09-28
Definition decision: APPROVE
Implementation authorization: NO
Roadmap mutation authorization: NO
09-G status: NOT STARTED
09-F status: NOT REQUIRED
```

The human owner approved the semantic direction and Change boundary before this materialization.

This Definition is the bounded scope authority candidate for Change 3.

Materialization alone does not make repository text immune to semantic-drift review. The materialized file must receive post-materialization owner review before the project proceeds to Plan preparation.

This Definition does not authorize implementation.

---

## 2. Problem

Current RunReceipt telemetry persists host/session cumulative token counters.

Those values are legitimate raw observations but are insufficient for safe operation-level claims such as:

```text
this operation used X input tokens
this operation used Y cached tokens
route A cost less than route B
one executor/model choice was economically preferable
```

unless exact operation boundaries and counter scope are proven.

The current receipt does not guarantee all of:

```text
same-session before/after boundary
counter scope
safe deterministic subtraction
expected-route binding
actual effort binding
measurement completeness
```

Therefore:

```text
CURRENT RECEIPT OBSERVABILITY
!=
SAFE OPERATION-LEVEL ECONOMICS
```

This is a measurement-integrity gap, not a routing defect.

---

## 3. Goal and corrected capability claim

For future eligible measured operations, receipt-backed operation-level token/cache claims are permitted only when measurement boundaries are proven safe.

Every newly eligible measured operation must produce either:

```text
A) SAFE, source-bound per-operation deltas

or

B) explicit UNAVAILABLE status with a reason
```

A cumulative snapshot must never be silently interpreted as an operation-local delta.

`UNAVAILABLE` is a valid evidence state.

Its presence is not itself an implementation failure.

It must not be concealed, approximated away, or replaced with zero.

---

## 4. Frozen architectural direction

Selected direction:

```text
ADDITIVE VERSIONED MEASUREMENT EXTENSION
+
EXISTING APPEND-ONLY TELEMETRY PATH
+
FAIL-CLOSED DELTA SEMANTICS
```

Existing cumulative receipt/token fields must retain their existing semantics.

They may not be renamed, reinterpreted, retroactively converted into operation-local values, or silently migrated to a new meaning.

The measurement extension must be additive and versioned.

Permitted future implementation forms are:

```text
versioned nested measurement block

or

explicitly versioned sibling measurement record
```

provided that the result remains on the existing PL08 telemetry/evidence path.

No second telemetry authority, parallel receipt system, or new telemetry database is introduced.

---

## 5. Existing ownership boundaries

| Concern | Existing owner / source | Change 3 boundary |
|---|---|---|
| expected route / capability decision | PL07 Operation Guidance or accepted pre-execution semantic trace | PL08 may reference it; telemetry cannot choose or rewrite it |
| Attempt / operation / task identity | existing governed operation / Attempt ownership | reuse by reference; do not create replacement identity |
| actual model / effort / role | structured host/capture evidence | observe and persist when safely bound |
| token/cache counters | host telemetry through existing capture path | derive safe operation-local measurement or UNAVAILABLE |
| evaluation / later economics | PL08 and future 09-G consumers | Change 3 supplies trustworthy evidence, not optimization policy |
| project state / next gate | Project Spine / owner governance | telemetry carries no authority |

Telemetry observes routing.

Telemetry does not own routing.

---

## 6. Minimum measurement contract

The future minimum measurement carrier must be capable of representing:

```text
operation_trace_ref / expected_route_ref

host_session_id
host_turn_id

parent_session_id
parent_turn_id
  when applicable

counter_scope

counter_before_boundary
counter_after_boundary

input_delta
cached_delta
uncached_input_delta
output_delta
reasoning_delta
total_delta

delta_status:
  SAFE
  UNAVAILABLE

unavailable_reason

actual_model
actual_effort
agent_role

telemetry_completeness
```

Existing operation / Attempt / task / run-family / invocation identity remains authoritative where already owned.

The measurement extension links to those identities rather than inventing replacements.

---

## 7. SAFE boundary semantics

A delta may be classified as `SAFE` only when all required boundary facts are established.

At minimum:

```text
same host session
+
known before boundary
+
known after boundary
+
compatible counter scope
+
deterministic subtraction
+
operation identity binding
```

A numeric value alone is not sufficient evidence of safety.

---

## 8. UNAVAILABLE boundary semantics

Measurement must become `UNAVAILABLE` whenever a material measurement prerequisite is missing or ambiguous.

Examples include:

```text
cross-session subtraction
missing before boundary
missing after boundary
unknown counter scope
non-bindable operation boundary
host/session transition that destroys safe subtraction
compaction that destroys the required boundary
incomplete telemetry
ambiguous operation identity
ambiguous expected-route linkage
```

An unavailable measurement must remain explicitly unavailable.

It must not be reconstructed from guesswork.

---

## 9. Token/cache invariants

The Change must preserve:

```text
I01
Existing cumulative receipt counters remain unchanged.

I02
No cumulative counter may be relabeled as operation-local.

I03
Cross-session subtraction is forbidden.

I04
Unsafe or ambiguous subtraction yields UNAVAILABLE.

I05
cached_delta + uncached_input_delta
must reconcile with input_delta
when all three are available under the same safe boundary.

I06
Replay/idempotent processing must not create a different valid delta
for the same bound evidence.

I07
Missing measurement data must never be replaced with guessed zero.

I08
A measured zero is materially different from UNAVAILABLE.

I09
Measurement completeness must be explicit.

I10
Measurement remains evidence, not authority.
```

---

## 10. Expected-route binding

`expected_route_ref` must originate from an existing pre-execution source already bound to the operation, such as:

```text
PL07 Operation Guidance

or

the accepted compact semantic operation trace
```

It must not be an unverified free-text route classification created after execution by an evaluator.

The measurement may record:

```text
expected route
actual model
actual effort
actual role
observed token/cache measurement
```

but it may not choose or retroactively redefine the expected route.

---

## 11. Minimum implementation surface for a later approved Plan

No implementation is authorized by this Definition.

If a later Plan is approved, the expected minimum implementation surface is limited to the existing PL08 telemetry/capture path and focused tests necessary to prove the invariant.

Likely owners include:

```text
src/planning_lite/telemetry.py
existing telemetry capture path
focused telemetry / receipt contract tests
```

Exact implementation paths must be determined and frozen by the later Plan.

This Definition does not authorize mutation of those paths.

---

## 12. Required eventual evidence

Technical completion must eventually include at least:

```text
E01
adjacent-turn same-session delta fixture

E02
cached + uncached reconciliation fixture

E03
cross-session subtraction rejection

E04
missing-boundary -> UNAVAILABLE case

E05
compaction / boundary-loss case

E06
replay / idempotence proof

E07
expected-route source-binding proof

E08
actual model / effort / role binding proof

E09
one real bounded governed operation through
capture -> persistence -> readback

E10
proof that existing cumulative receipt fields
retain their previous semantics
```

The real-operation proof must exercise the normal production capture path.

Manually assembled fixtures alone are insufficient for completion.

---

## 13. Completion criteria

The Change may be considered technically complete only when:

1. Every newly eligible measured operation produces safe deltas or explicit `UNAVAILABLE`.
2. No accepted path permits a cumulative snapshot to masquerade as an operation-local delta.
3. Expected route/class evidence is source-bound.
4. Actual model/effort/role evidence is safely bound.
5. The additive versioned measurement representation survives persistence/readback.
6. Replay does not alter valid measurement meaning.
7. Existing receipt semantics remain backward-compatible.
8. Focused contract tests pass.
9. At least one real governed operation proves the end-to-end seam.
10. No new telemetry, routing, project-state, or execution authority is created.

---

## 14. Explicit non-goals

This Change does not authorize or require:

```text
automatic model selection
automatic routing
route optimization
provider optimization
multi-operation scheduling
09-G orchestration
09-G economics policy
09-F comparator execution
duration optimization
tool-call-count optimization
cost dashboards
billing reconstruction
historical receipt backfill
raw prompt storage
raw response storage
raw tool-body storage
new telemetry database/service
new Attempt identity
new operation identity
Prompt Garden implementation
release
promotion
```

Duration and tool-call counts remain outside the minimum correction unless a separate later Change proves exact operation binding and authorizes them.

---

## 15. Relationship to 09-G

Change 3 is a prerequisite for trustworthy receipt-backed Execution Economics / Calibration evidence.

It is not itself 09-G.

```text
CHANGE_3
-> makes operation-level economics safely measurable

09-G
-> may later consume trustworthy measurements
   for bounded orchestration / economics / calibration
```

09-G must not silently redefine Change 3 measurement semantics.

09-G remains not started and not authorized by this Definition.

---

## 16. Relationship to Epistemic Robustness

Epistemic Robustness remains a separate bounded experiment.

It is not part of the RunReceipt schema or telemetry lifecycle.

After trustworthy measurements exist, a later experiment may ask whether plausible bounded changes in assumptions change a material economics/calibration decision.

That experiment is not authorized here.

---

## 17. Failure and stop conditions

A later implementation must fail closed or return `UNAVAILABLE` rather than infer when:

```text
counter scope cannot be established
before/after boundaries cannot be bound
session continuity is uncertain
expected-route source cannot be verified
receipt identity conflicts with operation/trace identity
measurement replay produces inconsistent results
existing cumulative semantics would require reinterpretation
the implementation would require authority expansion
```

Authority-expanding findings require owner review rather than silent scope growth.

---

## 18. False-done checks

The Change is not complete merely because:

```text
a new schema field exists
tests are green
some operations produce numbers
a dashboard can display numbers
cumulative subtraction works in one fixture
route labels appear somewhere in a receipt
```

Mandatory false-done question:

```text
CAN AN UNSAFE OR AMBIGUOUS BOUNDARY
STILL PRODUCE A NUMBER THAT LOOKS
LIKE A VALID PER-OPERATION COST?
```

If `YES`, the Change is not complete.

---

## 19. Authority boundary

This Definition approves Change semantics and boundaries only.

It does not authorize:

```text
Implementation Plan execution
product mutation
test mutation
telemetry schema mutation
CURRENT mutation
Roadmap mutation
Formal Readiness
implementation
stage
commit
push
release
promotion
09-G
```

A later Implementation Plan requires separate preparation, review, and owner approval.

Implementation requires a still later explicit authorization after Formal Readiness.

---

## 20. Next lifecycle gate

After successful materialization, the only next gate is:

```text
OWNER_REVIEW_MATERIALIZED_CHANGE_3_CANONICAL_DEFINITION
```

No Implementation Plan work is authorized before that review.
