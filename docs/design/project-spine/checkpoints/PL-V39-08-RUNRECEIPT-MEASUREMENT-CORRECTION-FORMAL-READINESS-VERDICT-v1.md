# PL-V39-08 RunReceipt Measurement Correction — Formal Readiness Verdict v1

## 1. Verdict identity and authority boundary

```text
Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-FORMAL-READINESS-VERDICT-001
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Definition: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-001
Definition SHA256: cef899a6b2ced4d1bef1e266969cd2b57981d5b59275b77e8e093e2d9d21cc
Implementation Plan: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-001
Implementation Plan SHA256: 91db4e0788b20f342418604e827c2f73b0fc8f16f42fa21139b218130e868f54
Readiness status: PREPARED_FOR_OWNER_REVIEW
Implementation authorization: NO
09-G: NOT STARTED
09-F: NOT REQUIRED
```

This checkpoint records a Formal Readiness evidence gate only. It does not
implement Change 3, authorize implementation, change the accepted Definition or
Plan, or update CURRENT, Roadmap, source, tests, telemetry, templates, or host
capture code.

```text
IMPLEMENTATION_AUTHORIZED:
NO
```

## 2. Entry synchronization binding

The required read-only preflight matched the live repository and the entry
capsule before this checkpoint was created:

```yaml
entry_head: 19217522f3dac695602a8534d7ddb8f9bbee5858
entry_authority_state_id: e351d2501892e6d453cadea616775d74aa6c28615184aef22fe34cb4b540c936
entry_candidate_state_id: 35bba4963a6ba24ad7f6588cf98d41f02e4c51b88032b1120e36434e28d646cf
entry_unrelated_dirt_state_id: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
entry_sync_state_id: b303637d8c5156f63345c2575f867b5cb0a2e1c95d2437aef59f8bc4e5059d22
entry_index_empty: YES
```

The accepted Plan was checked at its owner-accepted SHA. The twelve unrelated
PL-V39-09 checkpoint files remain outside this Change and were not cleaned,
absorbed, or rewritten.

## 3. Read-only repository evidence

### 3.1 Existing telemetry owner

`src/planning_lite/telemetry.py` is the single existing receipt validation and
append/readback owner.

- `_validate_receipt_record` accepts only the exact current v1/v2 receipt shape
  and validates the existing cumulative `tokens` fields.
- `TOP_LEVEL_KEYS`, `TOP_LEVEL_KEYS_V1`, `TOP_LEVEL_KEYS_V2`,
  `SCHEMA_TOP_LEVEL_KEYS`, and `TOKEN_KEYS` contain no measurement block,
  before/after boundary, counter scope, or delta fields.
- `append_receipt` rejects schema v2 input and delegates v1 records to the
  existing append path.
- `collect_governed_receipt` injects collector-owned `planning_lite_ref` and
  Attempt/execution identity, then calls the existing append and exact
  persisted-byte readback path.
- `_append_validated_receipt` returns identical duplicate behavior and raises
  `ReceiptError("Conflicting reuse of receipt_id")` for conflicting identity
  reuse.
- `_read_receipt_by_id` verifies that the persisted bytes equal the expected
  canonical payload.

Evidence: `telemetry.py:23-33`, `telemetry.py:117-186`,
`telemetry.py:203-347`.

This proves the existing persistence seam and the compatibility boundary. It
does not prove a safe operation-local delta source.

### 3.2 Governed lifecycle and expected-route owner

`src/planning_lite/operation_lifecycle.py` has the existing governed operation
seam:

- `_trace_persist_pre` receives the already-selected guidance and writes the
  pre-execution trace through `record_governed_attempt_evidence("PRE", ...)`.
- `execute_governed_operation` accepts the exact supplied PL07 guidance and
  explicitly does not reselect it.
- The current lifecycle order is lookup, admissibility, claim, guidance,
  pre-trace, execution, governed receipt collection, terminalization, PL08
  evaluation, post-trace, and downstream handoff.
- `collect_governed_receipt` is called with the supplied receipt and governed
  Attempt/execution identity. No host counter boundary is obtained by this
  function.
- `_trace_persist_post` binds the persisted receipt to the pre-trace entry by
  exact receipt reference and performs trace readback.

Evidence: `operation_lifecycle.py:607-638`,
`operation_lifecycle.py:641-679`, `operation_lifecycle.py:682-825`.

`src/planning_lite/operation_trace.py` provides the existing source-bound route
evidence. `write_expected_route_evidence` copies the exact already-selected
guidance projection, including operation/route identity and provenance;
`bind_attempt_run_receipt` validates the receipt Attempt and core identity; and
`read_operation_trace_evidence` uses only the exact persisted receipt locator.

Evidence: `operation_trace.py:157-198`, `operation_trace.py:201-246`,
`operation_trace.py:436-490`.

This proves that expected-route evidence can be carried from pre-execution
guidance without post-execution free-text reconstruction. It does not require a
new `operation_trace.py` authority or a new route selector.

### 3.3 Existing structured host/capture owner

`scripts/capture_codex_run_receipts.py` is the current structured Codex rollout
adapter.

- `_record_type_and_metadata` allowlists `session_meta`, `turn_context`, and
  token/completion metadata while keeping content records opaque.
- `_extract_session` obtains the rollout/session identity and parent identity.
- `_extract_turn` obtains turn identity, model, optional reasoning effort, and
  optional parent linkage.
- `_usage` validates non-negative input, output, cached, reasoning, and total
  counters and rejects cached input greater than input.
- `parse_rollout` gathers `event_msg/token_count` counters and completion
  markers, rejects counters after completion, and returns only
  `counters[-1]` as `InvocationFacts.terminal_timestamp` and `tokens`.
- `_make_receipt` persists the current cumulative token observation, actual
  model, and assigned agent role through the existing v1 receipt shape. It does
  not persist reasoning effort and has no before-boundary or counter-scope
  carrier.
- `capture` performs candidate preflight, delegates append to
  `planning_lite.telemetry.append_receipt`, and verifies canonical readback.

Evidence: `capture_codex_run_receipts.py:397-422`,
`capture_codex_run_receipts.py:471-619`,
`capture_codex_run_receipts.py:653-701`.

The current host adapter therefore proves an after-like terminal cumulative
snapshot for one explicit rollout. It does not prove an operation-local before
boundary, same-session subtraction scope, or a route binding into that receipt.

### 3.4 Focused test evidence

The existing tests prove adjacent contracts, not the accepted Change 3
measurement contract:

- `tests/test_run_receipts.py` covers v1/v2 shape, collector identity, append
  idempotence, conflicting receipt IDs, and exact persisted-byte readback.
- `tests/test_operation_lifecycle.py` covers lifecycle ordering, supplied
  guidance, receipt identity, pre/post trace behavior, and readback. Its
  collector is monkeypatched in the lifecycle-order tests; it does not prove a
  real Change 3 boundary carrier.
- `tests/test_operation_trace.py` covers source-bound expected route evidence,
  same-Attempt receipt binding, and partial trace behavior.
- `tests/test_codex_run_receipt_capture.py` exercises the real capture script
  with disposable rollout fixtures, including session/turn/model/effort
  extraction, terminal counter selection, content blindness, append/readback,
  and replay conflict. Its counters are cumulative rollout observations, not
  before/after operation boundaries.

The accepted Plan's three production surfaces and three focused test surfaces
are all existing paths. No new file, store, service, identity, or authority is
required by the evidence currently inspected.

## 4. Section 3.4 question disposition

| # | Question | Evidence-based disposition |
|---|---|---|
| 1 | Exact existing structured fact for the authoritative before boundary | NOT RESOLVED. The current adapter exposes token counters only inside one rollout and selects the final counter before completion; no operation-start counter fact is defined or carried. |
| 2 | Exact existing structured fact for the authoritative after boundary | PARTIAL. `event_msg/token_count` immediately represented by `counters[-1]` before the matching completion is the current terminal cumulative observation. It is not yet proven to be the after boundary for the governed operation. |
| 3 | Same-session identity and compatible counter scope | PARTIAL / NOT PROVEN. Session and turn identities are validated by `_extract_session`, `_extract_turn`, and `parse_rollout`; counter scope has no current field or equality validation across boundaries. |
| 4 | Carry pre-execution expected-route evidence | RESOLVED. Matched guidance enters `execute_governed_operation`, `_trace_persist_pre`, `write_expected_route_evidence`, and the post receipt binding. No post-execution free-text route reconstruction is accepted. |
| 5 | Actual model, effort, and agent role | PARTIAL BUT CONTRACT-BOUND. Model and optional effort are extracted from `turn_context`; role is assigned by the existing producer. Current receipt persistence omits effort, but the accepted Plan already freezes missing descriptive metadata as explicit `null` with `telemetry_completeness=PARTIAL`, independent of delta safety. |
| 6 | Existing authoritative producer/collector path | PARTIAL. The existing collectors are `capture -> append_receipt` for the host adapter and `execute_governed_operation -> collect_governed_receipt` for governed execution. Their common future measurement carrier is not present, and the current host adapter has no proven before-boundary source. |
| 7 | Fit with three production and three test surfaces | RESOLVED. The accepted Plan names existing `telemetry.py`, `operation_lifecycle.py`, and `capture_codex_run_receipts.py`, with existing focused tests in `test_run_receipts.py`, `test_operation_lifecycle.py`, and `test_codex_run_receipt_capture.py`. |
| 8 | Need for `operation_trace.py`, a new file/store/authority, or new architecture | RESOLVED NEGATIVE on current evidence. Existing operation-trace route binding is sufficient as the route-evidence owner. No new path or authority is justified. If boundary discovery finds no existing fact, implementation remains blocked rather than expanding architecture. |

## 5. False-ready challenge

The challenge passes because each plausible false-ready claim is rejected or
bounded rather than promoted to `SAFE` evidence.

| False-ready case | Result |
|---|---|
| Only an after cumulative counter exists | PASS — current `counters[-1]` is treated as cumulative evidence only; it cannot establish a safe delta. |
| Before and after belong to different sessions | PASS — session mismatch must remain `UNAVAILABLE`; parent/child linkage is not same-session proof. |
| Counter scope cannot be proven identical | PASS — no scope field is inferred; the seam is unresolved and requires controlled discovery. |
| Route identity can only be reconstructed after execution | PASS — existing pre-execution guidance/trace is the only accepted route source; post hoc text is rejected. |
| Descriptive metadata is absent but delta boundaries are valid | PASS — missing model, effort, or role is `null` with `PARTIAL`; it does not invalidate an independently safe delta. |
| Implementation would need a new parallel producer | PASS — no parallel producer is authorized; discovery must identify an existing producer or stop. |
| Implementation silently modifies `operation_trace.py` | PASS — the existing route-evidence owner is reused; silent mutation is prohibited. |
| A manually assembled receipt passes without a real governed capture path | PASS — existing fixtures do not prove the new measurement end to end; the real capture-to-append/readback proof remains a dependent implementation requirement. |

## 6. Exact expected implementation and test surfaces

The accepted Plan remains bounded to these exact production paths:

1. `src/planning_lite/telemetry.py`
2. `src/planning_lite/operation_lifecycle.py`
3. `scripts/capture_codex_run_receipts.py`

And these exact focused test paths:

1. `tests/test_run_receipts.py`
2. `tests/test_operation_lifecycle.py`
3. `tests/test_codex_run_receipt_capture.py`

`src/planning_lite/operation_trace.py` and `tests/test_operation_trace.py`
remain existing route-evidence owners, not an authorized mutation surface for
this gate. No new production file, test authority, database, service, identity,
or parallel producer is authorized.

## 7. Controlled discovery contract

### Discovery ID

`CHANGE_3_BOUNDARY_SOURCE_DISCOVERY_V1`

### question

Which existing structured host/capture event and field can provide the
operation's authoritative before boundary and after boundary with the same host
session and a compatible, explicitly identifiable counter scope, and how does
that evidence enter one of the already-accepted producer paths?

The discovery must also record whether the existing pre-execution route binding
can be carried alongside those facts and whether model, effort, and role are
available as structured metadata or must be explicit `null`/`PARTIAL` values.

### scope_bound

Inspect only the existing repository and structured host/capture evidence used
by the accepted surfaces:

- `src/planning_lite/telemetry.py`;
- `src/planning_lite/operation_lifecycle.py`;
- `src/planning_lite/operation_trace.py`;
- `scripts/capture_codex_run_receipts.py`;
- the focused tests named in Section 6;
- structured rollout records already accepted by the current capture seam.

Do not add host instrumentation, decode prompt/response/tool bodies, use
network or external research, create a new file/store/service, change the
Definition or Plan, or alter route/identity ownership.

### stop_condition

Stop as soon as one existing structured path proves both boundaries, same
session identity, and compatible counter scope, or as soon as inspection shows
that no such existing fact exists in the bounded scope. If no fact exists, the
discovery result is `NOT_PROVEN` and implementation remains not authorized; no
new architecture may be selected inside discovery.

### output_contract

Produce one external, read-only evidence record with this shape:

```yaml
schema_version: 1
discovery_id: CHANGE_3_BOUNDARY_SOURCE_DISCOVERY_V1
result: PROVEN | NOT_PROVEN
producer_path:
before_boundary:
  record_type:
  field_path:
  session_id:
  turn_id:
  counter_scope:
after_boundary:
  record_type:
  field_path:
  session_id:
  turn_id:
  counter_scope:
same_session: YES | NO | NOT_PROVEN
compatible_counter_scope: YES | NO | NOT_PROVEN
expected_route_source:
actual_model:
actual_effort:
agent_role:
telemetry_completeness:
reason:
```

`PROVEN` is allowed only when all required boundary and scope fields are
concretely identified. `NOT_PROVEN` must name the missing field or event. A
terminal cumulative counter alone cannot produce `PROVEN`.

### verification_before_dependent_work

Before any implementation-dependent work, verify the discovery record against
the accepted Definition Section 6 carrier and Section 9 failure rules, confirm
that it uses one accepted producer path, and rerun Formal Readiness or obtain a
new owner decision if the result would expand a source surface or architecture.
No implementation authorization follows from a `PROVEN` discovery result by
itself.

### forbidden_decisions

Discovery may not:

- choose or invent a new before/after host event;
- treat a terminal cumulative snapshot as an operation-local delta;
- infer same-session scope from parent/child linkage;
- introduce a counter scope default, zero, approximation, or concealment;
- reconstruct expected route after execution;
- select a model, provider, route, or economic policy;
- modify `operation_trace.py`, add a producer, add a store/service, or create a
  new identity;
- change the accepted Definition, Implementation Plan, reason vocabulary,
  precedence, or governance state.

## 8. Readiness verdict

```text
FORMAL_READINESS:
READY_WITH_CONTROLLED_DISCOVERY

SECTION_3_4_QUESTIONS_RESOLVED:
PARTIAL

CONTROLLED_DISCOVERY_REQUIRED:
YES

FIRST_BROKEN_SEAM:
No existing structured evidence currently proves an authoritative same-session
before boundary and compatible counter scope. The current host adapter exposes
only a terminal cumulative token counter (`parse_rollout` -> `counters[-1]`),
while the governed lifecycle accepts a receipt but has no host-counter boundary
provider.

IMPLEMENTATION_AUTHORIZED:
NO
```

This verdict does not claim that the missing host fact exists. It authorizes no
discovery execution and no implementation. The next single gate is owner review
of this Formal Readiness verdict; any controlled discovery requires separate
authorization.

