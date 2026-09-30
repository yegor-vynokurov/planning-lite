# PL-V39-08 RunReceipt Measurement Correction — Implementation Plan v1

## 1. Plan identity and governance status

```text
Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-001
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Lineage name: CHANGE_3
Plan status: PREPARED_FOR_OWNER_REVIEW
Definition authority: PL-V39-08 RunReceipt Measurement Correction — Approved Definition v1
Activation authority: PL-V39-08 RunReceipt Measurement Correction Definition Activation v1
Planning authorization: YES / BOUNDED IMPLEMENTATION PLAN PREPARATION ONLY
Implementation authorization: NO
Formal Readiness: NOT STARTED
09-G: NOT STARTED
09-F: NOT REQUIRED
```

This is one bounded implementation plan for the accepted Change 3 Definition.
Materializing this file does not approve the Plan, authorize implementation, or
change the Definition, Activation, CURRENT, Roadmap, source, tests, telemetry,
templates, or project state.

```text
IMPLEMENTATION_AUTHORIZED:
NO

FORMAL_READINESS:
NOT STARTED

NEXT_GATE_AFTER_PLAN_MATERIALIZATION:
OWNER_REVIEW_CHANGE_3_IMPLEMENTATION_PLAN
```

## 2. Frozen scope

The implementation must deliver only the additive, versioned, fail-closed
measurement extension defined by the accepted Definition:

1. Preserve the meaning of the existing cumulative receipt fields.
2. Capture or receive exact same-session before and after counter boundaries.
3. Validate counter scope and operation identity before deriving a delta.
4. Derive deterministic input, cached, uncached-input, output, reasoning, and
   total deltas only from compatible boundaries.
5. Persist either a source-bound `SAFE` measurement or an explicit
   `UNAVAILABLE` measurement with a reason.
6. Bind expected route evidence to the existing pre-execution Operation Guidance
   or accepted operation trace; do not select, relabel, or optimize a route.
7. Preserve append-only canonical persistence and identical-replay behavior.

The implementation must not add a second telemetry authority, a new database or
service, a new Attempt or operation identity, a route/model selector, billing or
duration economics, historical backfill, prompt/response/tool-body capture,
09-G, 09-F, Epistemic Robustness, or unrelated cleanup.

## 3. Existing ownership and implementation evidence

### 3.1 RunReceipt validation and persistence owner

`src/planning_lite/telemetry.py` is the current RunReceipt owner. The relevant
existing symbols are:

- `ReceiptError` for fail-closed validation/storage errors;
- `TOP_LEVEL_KEYS`, `TOP_LEVEL_KEYS_V1`, `TOP_LEVEL_KEYS_V2`,
  `SCHEMA_TOP_LEVEL_KEYS`, `TOKEN_KEYS`, and `READ_KEYS` for the current exact
  schema contract;
- `_validate_receipt_record` and `validate_receipt` for structural and current
  reference validation;
- `canonical_bytes` for deterministic JSON bytes;
- `_scan_existing_records` for stream validation and duplicate receipt identity;
- `_append_validated_receipt` for process-safe append-only persistence and
  identical-payload idempotence;
- `_read_receipt_by_id` for exact persisted-byte readback;
- `append_receipt` for the legacy v1 path;
- `collect_governed_receipt` for the governed v2 path, collector-owned
  `planning_lite_ref`, Attempt/execution identity injection, append, and exact
  readback;
- `collect_receipt` for the external legacy input path.

Current v1/v2 `tokens` are the existing cumulative/host-observed fields
`input`, `output`, `cached`, `reasoning`, `total`, and `source`. The current
validator requires those fields and the current collector rejects a v2 receipt
from the legacy `append_receipt` path. Change 3 must not reinterpret any of
those fields as operation-local deltas.

### 3.2 Governed operation and route-evidence seam

`src/planning_lite/operation_lifecycle.py` currently performs the governed
lookup, admissibility check, claim, exact supplied guidance check, pre-trace
write, governed execution, v2 receipt collection, terminalization, PL08
evaluation, post-trace write, and downstream Project Spine handoff. The
relevant symbols are `_receipt_context`, `_trace_persist_pre`,
`_trace_persist_post`, and `execute_governed_operation`.

The lifecycle passes the exact matched Operation Guidance projection through the
execution path; it does not reselect a route. The receipt is persisted through
`collect_governed_receipt`, and the post trace binds the persisted receipt to
the pre-execution route evidence. This is the bounded governed-operation seam
for the eventual capture → append → readback proof.

`src/planning_lite/operation_trace.py` remains the existing derived route and
receipt evidence owner. Its `write_expected_route_evidence`,
`bind_attempt_run_receipt`, `record_governed_attempt_evidence`, and
`read_operation_trace_evidence` contracts must be reused. It must not become a
second measurement or authority store.

### 3.3 Existing structured host capture seam

`scripts/capture_codex_run_receipts.py` is the current structured Codex host
adapter. Its relevant symbols are `Binding`, `ChildBinding`, `InvocationFacts`,
`parse_rollout`, `_extract_session`, `_extract_turn`, `_usage`,
`_make_receipt`, `_read_existing`, and `capture`.

The adapter safely reads metadata and terminal cumulative token counters,
extracts host session/turn identity, model, and reasoning effort, assigns the
existing agent role/invocation identity, delegates validation and append to
`planning_lite.telemetry`, and verifies canonical readback. It currently does
not prove a same-session before/after operation boundary, does not carry an
additive measurement block, and does not persist reasoning effort in the
current receipt shape. Its current terminal cumulative counter must not be
treated as a local operation delta merely because it is associated with one
turn.

### 3.4 Current evidence gaps to resolve during implementation

The following are implementation/readiness questions, not assumptions:

- Which existing host/capture event is the authoritative before boundary for a
  governed operation, and which event is the authoritative after boundary?
- Does that source expose a stable host session and turn identity on both
  boundaries and an unchanged counter scope? If not, the measurement must be
  `UNAVAILABLE`.
- How is the accepted pre-execution Operation Guidance or compact operation
  trace reference passed into the host capture producer without becoming a
  free-text post-execution route label?
- How is actual effort represented when the host omits it, and how does the
  implementation distinguish an observed zero from an unavailable value? A
  missing descriptive field is represented as `null` and makes telemetry
  completeness `PARTIAL`; it does not by itself make a proven delta
  `UNAVAILABLE`.
- Is the same capture producer used for the governed lifecycle and the Codex
  rollout adapter, or must the adapter hand off a bounded measurement carrier
  to the governed collector? The implementation must select an existing
  authoritative path before coding and must not create a parallel path.

If a counter boundary, counter scope, operation identity, expected-route
binding, or delta reconciliation fact cannot be proven from structured
evidence, the implementation must emit `UNAVAILABLE` with the frozen primary
reason contract below and retain the open question for owner review. If only a
descriptive metadata field is unavailable, it must emit that field as `null`
and set telemetry completeness to `PARTIAL`. It must not infer, approximate,
or silently omit the measurement.

## 4. Exact expected implementation surface

The expected product write surface is limited to these existing files:

1. `src/planning_lite/telemetry.py`
   - add the versioned measurement carrier, strict validation, deterministic
     boundary derivation, unavailable disposition, and governed persistence
     projection;
   - preserve current v1/v2 receipt validation and append/readback behavior;
   - keep the measurement logic pure until the existing collector persists it.
2. `src/planning_lite/operation_lifecycle.py`
   - preserve the current lookup → claim → guidance → execute → receipt →
     terminal → PL08 ordering;
   - pass only source-bound expected-route/operation evidence and the proven
     capture boundaries into the existing governed collector seam;
   - reject or carry `UNAVAILABLE` when those facts are missing, ambiguous, or
     incompatible; do not select a route or alter lifecycle authority.
3. `scripts/capture_codex_run_receipts.py`
   - adapt existing structured host metadata/counter observations into the
     versioned measurement carrier when exact boundaries are available;
   - preserve the existing content-blind parsing, explicit rollout bindings,
     identity derivation, preflight-before-write behavior, append ownership, and
     readback verification;
   - never promote its current terminal cumulative counter to a local delta
     without a proven before boundary.

No new production file, telemetry store, service, or authority is in scope.
`src/planning_lite/operation_trace.py` is an existing read-only route-evidence
owner for this Plan; it is not an expected write surface unless implementation
proves that a narrowly additive reference carrier is unavoidable and the owner
reviews that scope change.

## 5. Exact expected test surface

The expected focused test write surface is limited to these existing files:

1. `tests/test_run_receipts.py` — versioned carrier shape, validator,
   derivation, `SAFE`/`UNAVAILABLE`, cumulative-field compatibility,
   persistence, canonical readback, and replay/idempotence.
2. `tests/test_operation_lifecycle.py` — expected-route source binding, actual
   identity handoff, lifecycle ordering, one governed operation through capture
   → append → readback, and fail-closed missing-boundary behavior.
3. `tests/test_codex_run_receipt_capture.py` — structured host session/turn,
   model, effort, role, counter-scope, content-blind capture, explicit source
   binding, and real adapter replay/readback behavior.

`tests/test_operation_trace.py` remains the existing route-evidence contract
owner and is read-only for the planned change unless an implementation gap
requires a separately reviewed additive contract. No broad regression or
unrelated test expansion is part of this bounded Plan.

## 6. Measurement representation and compatibility contract

Use one additive nested measurement block on the existing governed receipt. The
block must have its own explicit version, for example:

```json
{
  "measurement": {
    "schema_version": 1,
    "operation_trace_ref": "...",
    "expected_route_ref": "...",
    "host_session_id": "...",
    "host_turn_id": "...",
    "parent_session_id": null,
    "parent_turn_id": null,
    "counter_scope": "...",
    "counter_before_boundary": {"...": "..."},
    "counter_after_boundary": {"...": "..."},
    "input_delta": 0,
    "cached_delta": 0,
    "uncached_input_delta": 0,
    "output_delta": 0,
    "reasoning_delta": 0,
    "total_delta": 0,
    "delta_status": "SAFE",
    "unavailable_reason": null,
    "actual_model": "...",
    "actual_effort": "...",
    "agent_role": "...",
    "telemetry_completeness": "COMPLETE"
  }
}
```

The exact field validators and the following v1 measurement semantics are
frozen before implementation. The example is a bounded shape, not permission
to add fields outside the accepted Definition. Existing top-level receipt
identity, Attempt, task, run-family, invocation, and cumulative token fields
remain authoritative and unchanged in meaning.

`delta_status` describes only whether operation-local counter deltas are safely
derivable. Its only values are `SAFE` and `UNAVAILABLE`. `SAFE` requires the
proven before and after boundaries, same host session, compatible known counter
scope, deterministic non-negative subtraction, bound operation identity,
source-bound expected route, and successful input/cache reconciliation where
applicable. Missing `actual_model`, `actual_effort`, or `agent_role` does not by
itself change an otherwise proven delta to `UNAVAILABLE`.

`telemetry_completeness` is independent from `delta_status`. Its only values
are `COMPLETE` and `PARTIAL`. `COMPLETE` means all required measurement
metadata fields are supported by structured evidence. `PARTIAL` means one or
more non-delta metadata facts are unavailable, or the delta itself is
unavailable. `SAFE + COMPLETE`, `SAFE + PARTIAL`, and `UNAVAILABLE + PARTIAL`
are valid; `UNAVAILABLE + COMPLETE` is invalid.

When structured evidence does not provide `actual_model`, `actual_effort`, or
`agent_role`, the missing field is explicitly `null`, never guessed,
free-text-reconstructed, defaulted, or converted to zero. Such absence sets
`telemetry_completeness=PARTIAL` but does not invalidate an independently safe
delta.

For `delta_status=SAFE`, `unavailable_reason` is `null`. For
`delta_status=UNAVAILABLE`, exactly one stable primary reason code is required.
The frozen v1 vocabulary is:

```text
MISSING_BEFORE_BOUNDARY
MISSING_AFTER_BOUNDARY
SESSION_MISMATCH
COUNTER_SCOPE_MISSING
COUNTER_SCOPE_MISMATCH
COUNTER_VALUE_MISSING
COUNTER_VALUE_INVALID
COUNTER_DECREASE
DELTA_RECONCILIATION_FAILED
OPERATION_IDENTITY_UNBOUND
EXPECTED_ROUTE_UNBOUND
BOUNDARY_LOST_OR_COMPACTED
```

When multiple conditions apply, select the first applicable code in this
deterministic order:

1. `MISSING_BEFORE_BOUNDARY`
2. `MISSING_AFTER_BOUNDARY`
3. `SESSION_MISMATCH`
4. `COUNTER_SCOPE_MISSING`
5. `COUNTER_SCOPE_MISMATCH`
6. `OPERATION_IDENTITY_UNBOUND`
7. `EXPECTED_ROUTE_UNBOUND`
8. `BOUNDARY_LOST_OR_COMPACTED`
9. `COUNTER_VALUE_MISSING`
10. `COUNTER_VALUE_INVALID`
11. `COUNTER_DECREASE`
12. `DELTA_RECONCILIATION_FAILED`

For `delta_status=UNAVAILABLE`, `input_delta`, `cached_delta`,
`uncached_input_delta`, `output_delta`, `reasoning_delta`, and `total_delta`
are all `null`. They must never contain guessed, approximate, inherited
cumulative, or zero-substituted values. A genuine measured zero remains
numeric `0` only under `delta_status=SAFE`.

Replay conflict is not an unavailable measurement reason. Conflicting reuse of
an existing receipt identity remains a hard validation/persistence failure
under the existing receipt contract.

Required rules:

- `delta_status=SAFE` requires a known before boundary, known after boundary,
  same host session, compatible known counter scope, deterministic
  non-negative subtraction, source-bound operation identity, source-bound
  expected route, and successful input/cache reconciliation where applicable.
  Descriptive metadata completeness is evaluated independently.
- Before and after identities must carry the host session/turn facts used for
  the comparison. A parent identity is retained only when applicable and
  proven.
- Every derived numeric delta must be a non-negative deterministic subtraction
  of the compatible after and before counters. Counter decrease, missing data,
  or ambiguous identity is not coerced to zero.
- When `input_delta`, `cached_delta`, and `uncached_input_delta` are all
  available, require:
  `cached_delta + uncached_input_delta == input_delta`.
- A measured numeric zero is valid evidence and must remain distinct from
  `UNAVAILABLE`.
- `delta_status=UNAVAILABLE` requires exactly one non-empty stable primary
  reason from the frozen vocabulary and all operation-local delta fields must
  be `null`. Missing values remain explicit unavailable values; they are not
  zero, approximate, inherited cumulative values, or concealed.
- `telemetry_completeness` must be explicit and independent from
  `delta_status`: `SAFE + COMPLETE`, `SAFE + PARTIAL`, and
  `UNAVAILABLE + PARTIAL` are valid, while `UNAVAILABLE + COMPLETE` is not.
  Completeness does not authorize a route or a Project Spine transition.
- Existing v1 receipts and existing v2 receipts without the new measurement
  remain readable with their existing cumulative semantics. No historical
  backfill is required.

## 7. Bounded implementation sequence

### Task 1 — Freeze the carrier and reason codes in the telemetry owner

In `src/planning_lite/telemetry.py`, define the versioned nested measurement
shape and strict validation without changing the existing cumulative token
fields. Add pure helpers for:

- boundary identity and counter-scope validation;
- same-session and operation-identity validation;
- deterministic per-field subtraction;
- cached/uncached/input reconciliation;
- `SAFE` versus `UNAVAILABLE` construction with the frozen primary reason
  codes;
- detached canonical projection used by the existing collector.

The helpers must reject or classify as `UNAVAILABLE` cross-session boundaries,
incompatible scopes, missing boundaries, counter decreases, ambiguous operation
identity, ambiguous route binding, and incomplete required boundary/counter
telemetry. Missing descriptive metadata must remain `null` with
`telemetry_completeness=PARTIAL` when the delta is otherwise safe. They must not
read prompt or response bodies, contact a network, choose a model, or alter
Project Spine.

### Task 2 — Bind the producer facts at the existing governed seam

In `src/planning_lite/operation_lifecycle.py`, retain the exact supplied
Operation Guidance and the pre-execution trace as the source of expected-route
evidence. Provide the measurement carrier to `collect_governed_receipt` only
from structured, source-bound facts. The implementation must not recreate a
route after execution from receipt text.

The before boundary must be captured before the governed operation begins, and
the after boundary must be captured from the same host session/counter scope
after the operation completes. If this lifecycle has no safe host-counter
provider, it must pass an explicit unavailable result or leave the operation
measurement unavailable; it must not use the cumulative receipt snapshot as a
substitute.

Keep the current order and authority boundaries intact:

```text
lookup → admissibility → claim → exact guidance → pre-trace
→ execute → governed receipt append/readback → terminalize
→ PL08 evaluation → post-trace → downstream handoff
```

The Plan does not authorize changing terminalization, evaluation, Project Spine,
route selection, or lifecycle outcome semantics.

### Task 3 — Adapt the existing structured host capture producer

In `scripts/capture_codex_run_receipts.py`, retain content-blind metadata
parsing and explicit rollout/session/turn bindings. Carry actual model,
structured effort, actual agent role, host session/turn identities, and the
counter scope into the measurement carrier.

The adapter must distinguish its existing terminal cumulative token observation
from a proven operation-local delta. If no before boundary from the same host
session and scope is available, produce `UNAVAILABLE` with the exact reason.
The adapter must preserve its current all-candidates-preflight-before-write,
explicit binding, canonical append, conflict detection, and readback checks.

If the host format cannot provide a required counter, boundary, identity, or
route fact without decoding content or using an unverified latest/decoy record,
the adapter must emit `UNAVAILABLE` according to the carrier contract. If it
cannot provide only descriptive model, effort, or role metadata, it must carry
that field as `null` and set `telemetry_completeness=PARTIAL` without changing
an independently safe delta to `UNAVAILABLE`.

### Task 4 — Persist and read back through the existing owner

Extend `collect_governed_receipt` and its validation path only enough to carry
the additive versioned measurement block through canonical JSON, append-only
storage, and `_read_receipt_by_id` exact-byte verification. Keep the legacy
`append_receipt` and `collect_receipt` semantics explicit; do not silently
upgrade a legacy cumulative record into a measured operation record.

Replay of the same bound evidence and receipt identity must return the same
canonical measurement. Conflicting reuse of an identity must remain a hard
failure and must not append a second or altered record.

### Task 5 — Prove the required evidence matrix with focused contracts

Add only the focused tests listed in Section 8. Every test must assert the
structured result or persisted data, not human-oriented rendering. Include the
real governed operation path in addition to pure fixtures.

### Task 6 — Run the bounded verification gate after later implementation

After a separately authorized implementation, verify the focused tests first,
then the existing owner/product suite at the appropriate completion gate. Check
Git/write boundaries and verify that existing cumulative receipt records retain
their prior meaning. Formal Readiness remains a later gate and is not performed
by this Plan.

## 8. Required evidence and contract-test matrix

The implementation must add or adapt focused tests for all rows below.

| ID | Required proof | Expected disposition |
|---|---|---|
| M01 | Adjacent-turn, same-session before/after fixture | `SAFE`; exact per-field deltas |
| M02 | Cached plus uncached input reconciliation | `SAFE`; equality holds exactly |
| M03 | Cross-session boundaries | `UNAVAILABLE`; `SESSION_MISMATCH` |
| M04 | Missing before boundary | `UNAVAILABLE`; `MISSING_BEFORE_BOUNDARY` |
| M05 | Missing after boundary | `UNAVAILABLE`; `MISSING_AFTER_BOUNDARY` |
| M06 | Incompatible counter scope | `UNAVAILABLE`; `COUNTER_SCOPE_MISMATCH` |
| M07 | Compaction or boundary-loss condition | `UNAVAILABLE`; `BOUNDARY_LOST_OR_COMPACTED` |
| M08 | Replay of identical bound evidence | same canonical result; one persisted record |
| M09 | Conflicting replay under same identity | hard conflict; no changed valid delta appended |
| M10 | Expected route from pre-execution guidance/trace | source-bound route accepted; otherwise `UNAVAILABLE`; `EXPECTED_ROUTE_UNBOUND`; post hoc free text is never accepted as route evidence |
| M11 | Actual model, effort, and agent role | captured from structured evidence; missing field is `null` and yields `PARTIAL` |
| M12 | Telemetry completeness | explicit independent `COMPLETE`/`PARTIAL` semantics; invalid `UNAVAILABLE + COMPLETE` rejected |
| M13 | One real governed operation | normal capture → append → exact readback path |
| M14 | Existing cumulative semantics | v1/v2 cumulative fields unchanged and backward-readable |
| M15 | Measured zero versus unavailable | zero remains numeric; unavailable remains non-numeric/explicit |
| M16 | Non-negative deterministic deltas | `UNAVAILABLE`; frozen primary reason selected under Section 6 precedence from `COUNTER_SCOPE_MISSING`, `COUNTER_SCOPE_MISMATCH`, `COUNTER_VALUE_MISSING`, `COUNTER_VALUE_INVALID`, `COUNTER_DECREASE`, or `DELTA_RECONCILIATION_FAILED` as applicable |

The real-operation test must exercise the normal governed lifecycle and the
existing collector/readback seam. A manually assembled receipt alone does not
prove M13.

## 9. Failure-closed rules

The implementation must return or persist `UNAVAILABLE` rather than infer when
any of these conditions holds:

- before or after boundary is missing;
- session continuity is uncertain or the session identities differ;
- counter scopes are unknown, incompatible, or change across the boundary;
- counters decrease or cannot be deterministically subtracted;
- operation/Attempt/turn identity is ambiguous or conflicts with the receipt;
- expected route cannot be traced to pre-execution guidance or the accepted
  compact operation trace;
- a required boundary, counter, operation identity, expected-route binding, or
  delta-reconciliation fact is missing; missing descriptive model, effort, or
  role metadata instead remains `null` with `telemetry_completeness=PARTIAL`;
- compaction destroys the boundary needed for safe subtraction;
- replay of the same evidence would produce a different canonical measurement;
  this is a hard validation/persistence conflict, not an `UNAVAILABLE`
  measurement reason;
- preserving existing cumulative semantics would require relabeling or
  reinterpretation.

For every `UNAVAILABLE` result, select exactly one primary reason from the
frozen vocabulary using the Section 6 precedence order and set every
operation-local delta field to `null`. No failure path may substitute zero, an
estimate, a latest snapshot, or a post-execution route label for missing
evidence. `UNAVAILABLE + COMPLETE` is invalid.

## 10. Non-goals and authority boundaries

This Plan does not authorize:

- implementation before owner review and later authorization;
- Formal Readiness;
- routing, route optimization, provider optimization, or automatic model
  selection;
- 09-G orchestration/economics policy or 09-F comparator work;
- duration/tool dashboards or billing reconstruction;
- prompt, response, reasoning-body, or tool-body storage;
- historical backfill;
- a new telemetry database/service or a second evidence authority;
- new Attempt or operation identity;
- Epistemic Robustness;
- Roadmap, CURRENT, template, release, stage, commit, push, or unrelated
  maintenance changes.

## 11. Exit conditions for later owner review

This Plan is ready for the next governance gate when the following are true:

1. The bounded source and test surfaces in Sections 4 and 5 remain the only
   intended product mutation surface.
2. The implementation questions in Section 3.4 are resolved by repository or
   host evidence, or are explicitly represented as `UNAVAILABLE` behavior.
3. The evidence matrix in Section 8 is accepted without enlarging Change 3.
4. The implementer can preserve existing cumulative fields and the current
   append/readback path.
5. The owner reviews this Plan as a separate decision.

Owner review of this Plan is the next single gate:

```text
OWNER_REVIEW_CHANGE_3_IMPLEMENTATION_PLAN
```

No successful Plan materialization is an implementation approval.
