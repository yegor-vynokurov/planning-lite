# PL-V39-08 RunReceipt Measurement Correction - Implementation Plan Amendment v2

## 1. Plan Amendment identity and governance status

```text
Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-002
Corrected from: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v1.md
Source Plan Amendment v1 SHA256: 9e02ebe4dc61d2fbc70eba0973033a3406cbe889a060b4b4f4f47d12df5f5c08
Plan Amendment v1 review: REVIEW_FAIL / 2 MATERIAL FINDINGS; NOT APPROVED
Corrected findings: P1-01 TURN_SCOPE_NOT_PROVEN_AS_ATTEMPT_SCOPE; P1-02 POST_TURN_MEASUREMENT_TRIGGER_NOT_PROVEN
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Lineage name: CHANGE_3
Plan Amendment status: CANDIDATE / OWNER_REVIEW_REQUIRED
Owner decision: SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT / ACCEPTED
Effective Definition: PREDECESSOR DEFINITION + AMENDMENT V2
Definition Amendment v2: APPROVED_BY_OWNER / ACTIVE
Definition Activation: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-DEFINITION-AMENDMENT-v2-ACTIVATION-v1.md
Definition Activation SHA256: 7e8c1232b29ffc6cdbbc35f7ce3b7356ce5d603ebfb4ab53dc9f2786cd05ca00
Predecessor Plan: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-v1.md
Predecessor Plan SHA256: 91db4e0788b20f342418604e827c2f73b0fc8f16f42fa21139b218130e868f54
Implementation authorization: NO
Formal Readiness: NOT STARTED
09-G: NOT STARTED
```

This is one corrected candidate Plan Amendment for owner review. It preserves the
accepted Codex implementation path of Attempt-bound completed-turn per-response
aggregation, while retaining `BOUNDARY_DELTA` as an independently safe fallback.
It corrects the v1 review findings by separating Attempt-to-turn binding from
Attempt-to-response-scope ownership, and by specifying a post-turn invocation
contract distinct from collector implementation. These are candidate design and
T00 proof gates; they do not assert that either scope ownership or a production
trigger has already been proven. Existing RunReceipt, Attempt, route, lifecycle,
persistence, and authority contracts remain in force unless this candidate
states a narrowly additive change.

Plan Amendment approval is not granted by preparing this candidate. Even after
Plan Amendment acceptance, implementation requires Formal Readiness and a
separate explicit owner implementation authorization. This candidate authorizes
no source, test, template, Roadmap, persistence, or runtime mutation.

```text
PLAN_AMENDMENT_APPROVAL: NOT GRANTED
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS: NOT STARTED
NEXT_SINGLE_GATE_AFTER_MATERIALIZATION:
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V2
```

## 2. Frozen scope and accepted Definition semantics

The implementation scope, if later authorized, is a source-bound
operation-local measurement with exactly one finalized method/status per
Attempt:

1. `RESPONSE_AGGREGATE` is the preferred Codex method when its exact binding,
   complete response scope, structured usage, and other SAFE requirements are
   proven.
2. `BOUNDARY_DELTA` remains an independent fallback only when its own
   authoritative same-session boundaries, compatible counter scope, operation
   binding, route evidence, and subtraction requirements are proven.
3. Existing RunReceipt v1/v2 cumulative token fields remain cumulative.
   Existing v1 measurement fields and `*_delta` fields retain
   `BOUNDARY_DELTA` meaning. A response sum must never be written into them.
4. `operation_measurement_v2` is an additive, explicitly versioned sibling
   record. It is never backfilled into or used to rewrite a persisted historical
   RunReceipt.
5. Measurement safety is independent from descriptive metadata completeness.
   Missing `actual_model`, `actual_effort`, or `agent_role` is represented as
   `null`, sets `telemetry_completeness: PARTIAL`, and alone does not invalidate
   an otherwise safe measurement. No descriptive value is guessed.
6. The initial response scope is root-only. Child/subagent usage is excluded
   unless its lineage and per-Attempt ownership are separately proven.
7. Root-turn usage comes from existing local Codex records; direct OpenAI API
   calls and new Codex instrumentation are not required for this local ledger.
8. A live or partial turn is never reported as a completed SAFE aggregate.
   Ambiguous multi-Attempt response ownership is unavailable; totals are never
   divided or allocated by timestamps.
9. Attempt-to-turn binding does not prove Attempt-to-response-scope ownership.
   `RESPONSE_AGGREGATE` is SAFE only when supported structured evidence proves
   either whole-turn equivalence for exactly one Attempt or the exact response
   subset owned by it; otherwise use `ATTEMPT_RESPONSE_SCOPE_NOT_PROVEN`.
10. The candidate post-turn producer is an explicit user/agent invocation of
    the existing capture command after turn completion. This is delayed
    collection, not an automatic trigger or a claim that every Attempt is
    measured.

This Plan does not authorize routing/model selection, execution authority,
economics policy, billing, duration analytics, or 09-G.

## 3. Owner review and finding dispositions

Definition Amendment v2 received
`REVIEW_PASS / 0 MATERIAL FINDINGS` and is active under the activation receipt
above. `A-01 DESCRIPTIVE_COMPLETENESS_SEMANTICS_REGRESSED` is closed by the
accepted v2 semantics.

The accepted scoped owner disposition is:

```text
R-01 SAFE_BOUNDARY_PROVENANCE_NOT_BOUND:
REMAINS OPEN FOR BOUNDARY_DELTA CURRENT CORRECTIVE CANDIDATE
/
SUPERSEDED AS A CODEX RESPONSE_AGGREGATE BLOCKER

R-02 M13_CAPTURE_TO_GOVERNED_HANDOFF_NOT_PROVEN:
REMAINS OPEN FOR BOUNDARY_DELTA CURRENT CORRECTIVE CANDIDATE
/
SUPERSEDED AS A CODEX RESPONSE_AGGREGATE BLOCKER
```

### Independent review of Plan Amendment v1

The owner review of Plan Amendment v1 is `REVIEW_FAIL / 2 MATERIAL FINDINGS`.
The v1 candidate remains unchanged and is not approved. The findings are:

```text
P1-01 TURN_SCOPE_NOT_PROVEN_AS_ATTEMPT_SCOPE
P1-02 POST_TURN_MEASUREMENT_TRIGGER_NOT_PROVEN
```

P1-01 is valid because an exact Attempt-to-thread/turn tuple does not prove that
every response in that host turn belongs to that Attempt. A unique Attempt in a
turn, matching IDs, or one observed example is insufficient evidence of
whole-turn equivalence. P1-02 is valid because v1 required collection after
completion but did not identify the production invocation owner or trigger; a
test that directly calls the collector could pass without the normal path ever
producing a measurement.

Plan Amendment v2 addresses both findings as explicit design questions,
fail-closed scope rules, a proposed explicit post-turn command contract, and T00
proof/stop gates. The v2 candidate does not mark the findings resolved by
assertion: runtime scope ownership and supported trigger behavior remain
unproven until the required discovery evidence exists.

R-01 and R-02 remain true findings against the preserved boundary-delta-only
candidate; this Plan does not claim to fix them. They do not need to be solved
for the separately accepted response route. The first unresolved response
route seam is `AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING`. The exact host
binding, post-turn collection, and append-only carrier questions below remain
explicit implementation gates.

## 4. Read-only source inspection and ownership map

The Plan is based on read-only inspection of the canonical entry working state
(HEAD plus the preserved candidate and governance partitions). The existing
owners and exact current seams are:

- `AttemptRecordV1.attempt_id` is authoritative and already includes the
  Change, task/operation, and attempt ordinal. `lookup_attempt` and
  `claim_attempt` resolve and claim that exact identity; no replacement
  Attempt or operation identity is permitted.
- `operation_lifecycle.execute_governed_operation` claims the Attempt, accepts
  the exact matched Operation Guidance, writes a pre-execution operation trace,
  executes, collects a governed RunReceipt v2, and later binds the receipt in
  the same Attempt trace. It is the owner that can carry the already-authorized
  Attempt identity into an invocation binding.
- `operation_trace.py` is the existing per-Attempt derived evidence owner. It
  stores the selected route and receipt relationship under `attempt_id`, and
  rejects unknown fields. It currently has no authoritative Codex thread/turn
  binding. A narrowly additive binding component is therefore included in the
  expected surface, subject to the discovery gate in Section 5.
- `capture_codex_run_receipts.py` accepts explicit rollout/session/turn
  bindings, reads `session_meta`, `turn_context`, `task_complete`, and terminal
  `token_count` metadata, preflights all candidates before appending, and checks
  canonical readback. It currently ignores `token_usage_record`, requires one
  `task_complete` for its explicit turn, and has no live-file size/mtime
  stability check. Its receipt does not prove an Attempt-to-turn join.
- `telemetry.py` owns strict RunReceipt v1/v2 validation, canonical JSON,
  process-safe append, duplicate receipt identity behavior, and exact
  `receipt_id` readback. `_scan_existing_records` currently validates every
  line as a RunReceipt; `_read_receipt_by_id` only indexes receipts. The
  capture script also directly validates every line in the same stream as a
  RunReceipt. Neither reader currently accepts a sibling measurement record.
- The accepted read-only local evidence proves that structured
  `token_usage_record.usage`, thread/turn/session/response identities, and a
  `task_complete` event exist in the observed Codex rollout. One completed root
  turn's unique per-response sums exactly matched its compatible final
  `turn_token_usage`. The evidence proves local measurement capability, not the
  governed Attempt join or the complete production persistence seam.

The external probes and their hashes remain bound by the immutable Option C
owner-decision checkpoint. They are design evidence, not substitutes for the
source-faithful end-to-end proof required by this Plan.

- A read-only source/CLI call-site search found no in-repository production
  caller that schedules `capture_codex_run_receipts.py` after `task_complete`.
  The script is directly invocable as an explicit command, but the current
  lifecycle does not prove automatic post-turn invocation. The v2 candidate
  proposes explicit user/agent post-turn collection as its narrow contract;
  T00 must verify that this is a supported contract for the target sidebar
  shape. No automatic measurement claim is made.

## 5. P-01 - authoritative Attempt-to-thread/turn binding

### Binding design

Use the existing `AttemptRecordV1.attempt_id` as the sole operation identity.
Capture one immutable host-turn binding after exact Attempt lookup/claim and
matched Operation Guidance, immediately before governed execution and before
any measured response can be emitted. The existing `operation_lifecycle`
pre-trace owner writes the binding as an additive component of the same
`operation_trace.py` entry already keyed by `attempt_id`; it does not create a
new Attempt, receipt identity, or parallel route authority.

The binding tuple is:

```text
attempt_id
host_thread_id
host_session_id (only when separately present and unambiguous)
host_turn_id
operation_guidance_ref
expected_route_ref
binding_source_ref
```

`host_thread_id` comes from the host-provided `CODEX_THREAD_ID` at the governed
invocation seam and must exactly equal the rollout's unique `session_meta.id`
(thread/rollout identity). A separately exposed host session ID is stored in its
own field and compared to structured turn metadata; a parent-session alias is
never silently relabeled as the thread ID. `host_turn_id` comes from the unique
structured `turn_context.turn_id` for the active invocation. If
`turn_context.session_id` is present, it must agree with the proven host thread
or separately specified session relation. The binding includes a source
reference to the allowlisted structured host record, not a prompt/body excerpt.

### Capture owner and rejection rules

- The operation lifecycle supplies the existing claimed Attempt ID and exact
  pre-execution route evidence. The host capture adapter supplies the host
  thread and current structured turn facts. Capture occurs before the governed
  call can emit response usage.
- Before writing the binding, require exactly one coherent current
  `turn_context`, exact thread/session agreement, and an Attempt trace with the
  same `attempt_id`. If those facts are not available at this point, the
  ordinary governed operation may continue under its existing authority, but
  response measurement cannot become SAFE; no post hoc or latest-turn guess is
  allowed.
- On later collection, require the same immutable tuple in the Attempt trace
  and the exact explicit rollout. Re-used threads are acceptable only with an
  exact distinct `turn_id`; an adjacent turn, another `turn_context`, or a
  latest-record heuristic cannot satisfy the binding.
- Enforce uniqueness of `(host_thread_id, host_turn_id)` across Attempt
  bindings. A second Attempt for the same pair is ambiguous and fails closed
  unless structured per-response ownership is separately proven. Concurrent,
  stale, or conflicting bindings are rejected; timestamps are never used to
  allocate responses.
- A response measurement key is deterministically derived from the existing
  Attempt ID and the bound thread/turn tuple plus measurement schema/method
  version. Replaying identical binding and payload is idempotent. Reuse of the
  key with changed identity or payload is a hard conflict, not a replacement.

### Attempt-to-turn binding is not Attempt-to-response-scope ownership

```text
ATTEMPT_TO_TURN_BINDING != ATTEMPT_TO_RESPONSE_SCOPE_OWNERSHIP
T00_DISCOVERY_QUESTION: ATTEMPT_TURN_SCOPE_EQUIVALENCE
```

The immutable binding tuple above proves which host thread and turn are
associated with the Attempt. It does not, by itself, prove that all response
usage records in that turn belong to the Attempt. Response-scope ownership is a
separate required fact:

1. **Whole-turn equivalence (A):** the supported lifecycle contract must
   authoritatively prove that the complete root turn is the scope of exactly one
   Attempt, including that no pre-Attempt or unrelated response work in that
   turn is attributed to it. Matching `thread_id`/`turn_id`, absence of a second
   Attempt, temporal proximity, current/latest turn selection, and a single
   observed example do not prove equivalence.
2. **Structured subset (B):** if only some responses belong to the Attempt, a
   structured source-bound ownership signal must identify that exact response
   subset and its relation to the Attempt. Persist a reference to that signal.
   Sequence position is usable only if an authoritative stable source event
   establishes it. Do not infer membership from ordering or timestamps.
3. **Unproven ownership (C):** if neither whole-turn equivalence nor a
   structured subset is proven, the per-Attempt response measurement is
   `UNAVAILABLE` with `ATTEMPT_RESPONSE_SCOPE_NOT_PROVEN`. This is distinct
   from `RESPONSE_OWNERSHIP_AMBIGUOUS`, which denotes conflicting or ambiguous
   structured ownership claims (including multiple Attempts claiming one
   response).

T00 must determine which of A, B, or C describes the supported Planning Lite
sidebar execution shape from structured host and lifecycle evidence. A whole
turn may be SAFE only under A. Under B, aggregate only the proven subset. Under
C, do not emit a SAFE value and stop before product mutation if discovery cannot
settle the scope semantics.

### Controlled Discovery gate

The existing source does not yet show the host-context handoff into the
pre-trace. Before any product mutation, bounded read-only T00 discovery must
prove that `CODEX_THREAD_ID` and the active structured `turn_context` are
available to the existing invocation owner before execution, and confirm that
the existing Attempt-keyed trace is the correct owner for the narrow additive
binding extension. It must separately determine whether the supported sidebar
shape satisfies whole-turn equivalence, uses a structured response subset, or
cannot prove Attempt-to-response-scope ownership. The prior one-session probe
is insufficient to prove either lifecycle seam. If binding or response-scope
facts are unavailable or cannot be source-bound, stop with
`AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING_NOT_PROVEN` or
`ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN`, respectively. Keep affected
response measurements unavailable and return the exact seam to the owner. Do
not add a host hook, sidecar store, second Attempt identity, timestamp allocator,
or prompt parser as a workaround in this Change.

## 6. P-02 - turn completion and post-turn measurement point

The current structured `event_msg/task_complete` is the proposed completion
signal. The existing capture parser already requires exactly one such event
for the explicitly selected turn; accepted read-only evidence observed a
completed root turn with this event and exact compatible turn-usage
reconciliation.

### POST_TURN_MEASUREMENT_PRODUCER_AND_TRIGGER

Collector implementation and collector invocation are separate requirements.
The candidate contract is **explicit delayed/pull collection**: after the target
turn is complete, a user or agent explicitly invokes the existing
`scripts/capture_codex_run_receipts.py` command to collect that Attempt's final
measurement. This is the normal trigger proposed by v2; it is not automatic
collection at turn completion. The existing script is currently a capture
entrypoint, not proof that `operation_measurement_v2` is already collected or
persisted.

The command must name the exact `attempt_id` and explicit rollout source. It
must load the immutable thread/turn binding from that Attempt's existing trace,
validate source identity and the response-scope proof from Section 5, and then
run collection. It must not search for a pending Attempt by recency, choose the
latest turn, or infer identity from timestamps. Repeated invocation uses the
same deterministic measurement identity and is idempotent; a changed binding or
payload is a hard replay conflict. The invocation owner is the explicit user or
agent command runner. A direct call to an internal collector is not this
production trigger.

This contract makes no automatic or per-every-Attempt measurement claim. If no
later collection command runs, no final sibling measurement is produced and the
Attempt is not counted as measured or SAFE. That delayed absence is permitted
only for the explicitly requested-collection capability scope. If Change 3 is
expected to produce a measurement automatically or for every governed Attempt,
this trigger is insufficient and T00 must stop for a separate owner decision.

T00 must verify that the existing explicit command can be the supported
post-turn trigger for the supported sidebar shape, that it can receive or
resolve the exact Attempt binding without heuristic discovery, and that the
scope/route/source references survive until collection. If it cannot, stop with
`POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`. A new Stop hook, daemon,
scheduler, watcher, sidecar, or other host instrumentation is outside scope and
requires separate authorization.

The Plan never finalizes response usage inside the same live turn. The
`operation_measurement_v2` collector runs only after the target turn's
`task_complete` is present and a stable post-turn rollout snapshot has been
read. It may be invoked in a later host turn with the immutable pre-execution
Attempt/thread/turn binding. It selects the target by that exact tuple, not by
current/latest turn. It requires all eligible response usage records for the
target before completion, rejects target-turn usage appearing after completion,
and reconciles to the compatible final host turn aggregate when present. A
partial live turn returns an `UNAVAILABLE / TURN_INCOMPLETE` observation but
must not append a final sibling record while the turn remains live. Once an
explicit terminal interruption/closure proves that the turn cannot complete,
a final UNAVAILABLE record may be appended. The original RunReceipt is never
reopened or mutated.

Before implementation, Controlled Discovery must verify that `task_complete`
actually closes the target response-usage set for the supported host shape and
that post-turn stable reading exposes all eligible records. If completion order
or signal is not authoritative, stop with `POST_TURN_COMPLETION_SIGNAL_NOT_PROVEN`;
do not invent a timer, quiet period, final token record, or synthetic
completion event. A bounded stable read is an additional consistency check,
not a replacement for the structured completion signal.

## 7. P-03 - append-only `operation_measurement_v2` persistence

### Proposed carrier and owner

Append one tagged sibling record to the existing telemetry append-only stream
only after the target turn is complete and its measurement is final. Do not
modify, replace, or backfill the already persisted RunReceipt. The proposed
record is a distinct top-level stream object with a discriminator such as
`record_type: operation_measurement_v2` and its own `schema_version: 2`,
`measurement_id`, existing `attempt_id` and invocation references, host
thread/turn references, `measurement_method`, method version, semantic
`measurement_status`, `telemetry_completeness`, common descriptive metadata,
and method-specific payload. Response payloads use named usage fields and
response dedup/reconciliation evidence; boundary payloads preserve existing
boundary/delta meanings. `delta_status` and old `*_delta` fields are not used
for a response sum.

Reuse `telemetry.py`'s lock, canonical serialization, append/fsync, duplicate
identity, and exact readback ownership. Extend its scanner to type-dispatch
RunReceipt v1/v2 records and `operation_measurement_v2` records into distinct
validated indexes. Existing receipt append/read paths continue to validate,
index, and return only RunReceipts. Add a distinct measurement append/readback
API keyed by deterministic `measurement_id`. The capture adapter must use this
owner rather than independently interpreting a mixed stream. Existing receipt
bytes remain unchanged and old v1/v2 receipts remain readable.

### Mandatory storage stop gate

The current owner cannot accept a sibling today: `_scan_existing_records`
passes every line to the strict RunReceipt validator, and capture's
`_read_existing` does the same. Those are the exact compatibility seams. Task
T00 must prove that a tagged sibling can be added while preserving all supported
RunReceipt readers, no historical line mutation, identical replay, conflicting
replay failure, and exact readback. The proposed change stays inside the
existing telemetry owner and same append-only stream; it proposes no new file,
database, service, or registry. If type-dispatch cannot safely preserve
backward readability, stop with
`APPEND_ONLY_SIBLING_RECORD_COMPATIBILITY_NOT_PROVEN` and return that exact
broken seam to the owner. Do not propose or create a second store in this
Change.

## 8. P-04 / P-05 - structured response extraction and live JSONL safety

Primary usage comes only from structured local `token_usage_record.usage` for
response records whose thread, turn, response identities, and separately proven
Attempt-response ownership scope match. Thread/turn equality alone is not an
ownership filter. Under whole-turn equivalence, the complete root turn may be
selected only after the contract proof in Section 5; under a structured subset,
select only the source-bound response members. Read only an allowlist of
top-level discriminators and scalar/numeric metadata fields. Do not decode
prompt, response, reasoning, tool, or other content bodies; do not inject whole
rollout contents into model context.

The unique response key is `(thread_id, response_id)`. Require the target
`turn_id` and any present session/root identifiers to agree with the binding.
Deduplicate identical repeated records by that key. The same key with different
identity or usage is a hard `DUPLICATE_RESPONSE_CONFLICT`; missing/conflicting
response identity is unavailable. Sum only the supported per-response `usage`
fields, using strict non-negative integer validation (booleans are invalid).
The accepted numeric mapping is `input_tokens` to input, `cached_input_tokens`
to cached input, `output_tokens` to output, `reasoning_output_tokens` to
reasoning output, and `total_tokens` to total. Derive uncached input only when
`cached_input_tokens <= input_tokens`; require exact cached plus uncached
reconciliation to input. Missing required numeric fields never become zero. Do
not sum the repeated cumulative
`turn_token_usage` member or `event_msg/token_count` records. A compatible
final `turn_token_usage` may be used only for reconciliation/checking, never as
the primary operation usage.

Use a streaming JSONL reader over an explicit rollout path. Before opening,
capture the file identity (where supported), size, and `mtime_ns`; stream
complete newline-terminated records up to the observed size, retaining only
allowlisted metadata and a bounded set of response identities/totals. After the
read, compare the open-handle and path identity/size/mtime to the initial
snapshot. Require a complete final line and no replacement or mutation during
the scan. Permit at most one bounded retry after a changed signature; if the
second scan is not stable, return `SOURCE_READ_UNSTABLE`. Never claim complete
scope from a truncated line, unstable file, unsupported record, or a response
record after the target completion event. The stable read check supplements,
and does not replace, `task_complete`.

## 9. P-06 - deterministic method selection

Produce at most one finalized `operation_measurement_v2` per Attempt:

1. If `RESPONSE_AGGREGATE` satisfies every SAFE condition, select it as the
   authoritative method.
2. If response records for the bound turn are absent as a supported source, a
   separately proven `BOUNDARY_DELTA` may be selected as the fallback. Boundary
   data must satisfy its predecessor/Definition v2 scope, source, binding,
   route, counter compatibility, and subtraction requirements independently.
3. If response evidence is present but its Attempt scope is unproven, unstable,
   ambiguous, conflicting, incomplete, numerically invalid, or fails required
   reconciliation, do not
   conceal that defect by falling back to a second total. Finalize
   UNAVAILABLE with the response reason.
4. If both methods are SAFE and semantically comparable, RESPONSE_AGGREGATE is
   the sole authoritative total; BOUNDARY_DELTA is reconciliation evidence
   only. Any disagreement in a comparable field is a hard
   `ALTERNATE_METHOD_DISAGREEMENT` and the emitted measurement is UNAVAILABLE.
   If fields are not comparable, record that explicitly and do not call it a
   successful reconciliation.
5. Never persist two competing operation totals for one Attempt. Historical
   v1 delta fields remain unchanged even when the fallback method is selected.

## 10. P-07 - frozen response-unavailability vocabulary and precedence

For `RESPONSE_AGGREGATE`, freeze this bounded v2 primary-reason vocabulary and
use the first applicable reason in this exact order:

```text
1. SOURCE_READ_UNSTABLE
2. ATTEMPT_OPERATION_BINDING_UNAVAILABLE
3. EXPECTED_ROUTE_BINDING_UNAVAILABLE
4. HOST_THREAD_SESSION_IDENTITY_UNAVAILABLE
5. HOST_TURN_IDENTITY_UNAVAILABLE
6. TURN_INCOMPLETE
7. ATTEMPT_RESPONSE_SCOPE_NOT_PROVEN
8. RESPONSE_OWNERSHIP_AMBIGUOUS
9. RESPONSE_IDENTITY_MISSING_OR_CONFLICTING
10. DUPLICATE_RESPONSE_CONFLICT
11. REQUIRED_USAGE_MISSING_OR_INVALID
12. HOST_TURN_RECONCILIATION_FAILED
13. ALTERNATE_METHOD_DISAGREEMENT
```

These names describe response-source semantics and do not reuse boundary-only
reason names. `ATTEMPT_RESPONSE_SCOPE_NOT_PROVEN` means there is no authoritative
whole-turn equivalence or structured subset proof; `RESPONSE_OWNERSHIP_AMBIGUOUS`
means otherwise structured ownership is conflicting or ambiguous. A `SAFE`
result has no unavailable reason. A final
`UNAVAILABLE` record has exactly one reason and null operation usage fields.
The active turn's provisional `TURN_INCOMPLETE` observation is not persisted
until authoritative terminal evidence proves the scope cannot complete.
`BOUNDARY_DELTA` continues to use its separately frozen predecessor reason
contract.

## 11. P-08 through P-11 - descriptive fields, root scope, and compatibility

- The common sibling record retains `actual_model`, `actual_effort`,
  `agent_role`, and `telemetry_completeness`. Missing descriptive values are
  explicit `null`, never guessed, and yield `PARTIAL`; their absence alone does
  not make otherwise SAFE usage unavailable.
- `measurement_status` is method-independent (`SAFE` or `UNAVAILABLE`). Do
  not use `delta_status` for `RESPONSE_AGGREGATE`. Preserve the predecessor
  valid completeness combinations: `SAFE + COMPLETE`, `SAFE + PARTIAL`, and
  `UNAVAILABLE + PARTIAL`; `UNAVAILABLE + COMPLETE` remains invalid.
- Initial scope is `ROOT_ONLY RESPONSE_AGGREGATE`. Do not include child or
  subagent response usage unless separate lineage and ownership are later
  proven and separately authorized. Partial whole-agent-tree attribution does
  not block an independently proven root measurement.
- Attempt-to-turn binding is not sufficient to assign responses to an Attempt.
  Whole-turn use requires proven equivalence; subset use requires structured
  source-bound ownership. If neither is proven, return
  `ATTEMPT_RESPONSE_SCOPE_NOT_PROVEN`, even when only one Attempt is present.
- If one Codex turn contains multiple Planning Lite Attempts and structured
  ownership cannot disambiguate each response, each affected per-Attempt result
  is unavailable as `RESPONSE_OWNERSHIP_AMBIGUOUS`. Never divide the turn sum,
  allocate by timestamps, or assign the turn's whole usage to each Attempt.
- Preserve RunReceipt schemas v1 and v2, cumulative token meanings, existing
  receipt identities, old receipts without a measurement sibling, and
  append-only history. No backfill or migration is required.

## 12. P-12 - required real or source-faithful end-to-end proof

Before Change 3 implementation completion, exercise the actual existing
Attempt/lifecycle and telemetry owners with either a real host run or a
source-faithful rollout fixture. The proof must follow the complete chain:

```text
authoritative Attempt
-> source-bound pre-execution Attempt/thread/turn binding
-> authoritative whole-turn Attempt equivalence OR exact source-bound response subset
-> governed execution
-> completed and stable eligible response scope
-> normal supported post-turn trigger (the explicit capture command under this candidate contract)
-> unique structured response extraction
-> deterministic aggregation
-> compatible host-turn reconciliation
-> append-only operation_measurement_v2 persistence
-> exact measurement readback
-> correct association to the same Attempt and route
```

A manually assembled final measurement object or a test-only/direct internal
collector call is insufficient. The proof must invoke the selected public
post-turn command after completion, resolve the exact pending Attempt/thread/turn
binding and response-scope ownership, derive identity and usage from source
records, leave the original RunReceipt bytes unchanged, append one sibling, and
re-read its exact canonical bytes. Require negative proofs for incomplete live
turn, wrong turn, wrong thread/session, bound turn with unproven whole-turn
ownership, a pre-Attempt response in the same turn, unrelated response in the
same turn, ambiguous multi-Attempt turn, duplicate response conflict, missing
usage, host reconciliation mismatch, unstable source read, unavailable normal
trigger, test-only collector call, conflicting replay, and unproven child
attribution.

## 13. P-13 / P-14 - candidate reuse and minimum implementation surface

The preserved corrective candidate state remains
`37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555` and must
not change during Plan preparation or later implementation without a separate
owner-authorized disposition. It is preserved as evidence, not an automatic
implementation baseline.

Potentially reusable after owner review are the existing exact Attempt/route
binding checks, receipt identity and append/readback discipline, content-blind
raw JSONL scanning primitives, all-candidates-preflight-before-write behavior,
and focused identity/replay fixtures. The boundary-specific subtraction
helpers, `counter_before_boundary`/`counter_after_boundary`, `delta_status`,
boundary reason precedence, and tests asserting cumulative counter deltas do
not implement `RESPONSE_AGGREGATE`; for that Codex path they are superseded
and historical, and are not selected or ported into `operation_measurement_v2`.
They may remain only for the separately safe `BOUNDARY_DELTA` fallback. No
response sum may be routed through those delta
fields. The Plan does not assume every file in the six-file predecessor
candidate must change.

Proposed smallest write surface, subject to T00 gates:

| Surface | Planned use | Reason |
|---|---|---|
| `src/planning_lite/operation_trace.py` | Add and validate the narrow Attempt/thread/turn binding on the existing Attempt-keyed trace entry. | The current trace is the existing per-Attempt evidence owner and has no host binding; unknown fields are rejected. |
| `src/planning_lite/operation_lifecycle.py` | Capture the host binding before execution and carry the same Attempt/route references through the existing lifecycle. | It owns the claimed Attempt, exact guidance, and pre-trace ordering. |
| `scripts/capture_codex_run_receipts.py` | Extend the existing explicit user/agent command with stable post-turn response extraction, scope validation, method selection, and measurement append invocation. | It is the existing runnable capture entrypoint; T00 must verify it is the supported trigger and that exact Attempt binding can be resolved without a host hook. |
| `src/planning_lite/telemetry.py` | Validate and append/read back the tagged sibling through the existing lock/canonicalization owner. | It owns the append-only telemetry stream; T00 must prove typed sibling compatibility. |
| `tests/test_operation_trace.py` | Binding construction, conflict, same Attempt, and readback contracts. | Existing owner test for trace evidence. |
| `tests/test_operation_lifecycle.py` | Pre-execution binding handoff, exact route/Attempt association, and no authority-order change. | Existing lifecycle contract. |
| `tests/test_codex_run_receipt_capture.py` | Structured response usage, stable file scan, completion, deduplication, method selection, and source-faithful capture. | Existing host-adapter contract. |
| `tests/test_run_receipts.py` | Tagged sibling validation, append-only coexistence, exact measurement readback, replay, and old receipt compatibility. | Existing telemetry persistence contract. |

No new production module, service, database, telemetry file, registry, host
hook, scheduler, or parallel authority is proposed. The explicit command is a
user/agent pull trigger and makes no automatic-coverage claim. No new test file
is proposed. If T00 finds
that `operation_trace.py` is not a safe binding owner or that the existing
telemetry stream cannot safely host typed siblings, stop and return the exact
broken seam for owner review before enlarging this surface.

## 14. P-15 - explicit future boundary

Outside this Change are SQLite/LanceDB local registries, Prompt Garden
migration, automatic recommendations, generalized execution-economics
warehouses, whole-agent-tree analytics beyond root safety, billing/duration
analytics, provider/model selection, 09-G, and 09-F. None is a prerequisite or
implicit follow-on in this Plan Amendment.

## 15. Bounded implementation sequence after separate authorization

### T00 - Controlled Discovery: Attempt response scope, trigger, and persistence

T00 is bounded, read-only, and precedes all product mutation. It records source
references and hashes and must settle each gate below for the supported Planning
Lite sidebar execution shape:

1. **Attempt response scope.** Inspect structured host and Planning Lite
   lifecycle evidence to classify the shape as (A) complete root-turn equivalence
   to one Attempt, (B) a source-bound response subset, or (C) ownership not
   provable. Determine how pre-Attempt and unrelated responses are handled.
   Matching turn IDs, no second Attempt, temporal proximity, and one example are
   explicitly insufficient. Under A, prove the full turn is exclusively in
   scope. Under B, name the authoritative stable ownership signal and exact
   response membership rule. If neither is proven, stop with
   `ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN`.
2. **Post-turn producer and trigger.** Inspect the production call graph and
   existing command entrypoints to determine whether a completed turn already
   triggers collection. Distinguish the collector implementation from its
   caller. The v2 candidate proposes an explicit user/agent invocation of the
   existing capture command after `task_complete`, with explicit `attempt_id`
   and rollout source and exact binding lookup from the Attempt-keyed trace.
   Verify who invokes it, when, the exact binding handoff, replay behavior, and
   that it never selects a current/latest turn. This is delayed/pull collection,
   not automatic measurement. If no command can be established as the supported
   contract, stop with `POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`.
3. **Delayed absence.** Determine whether the capability is allowed to cover
   only explicitly collected Attempts. If no later command runs, no sibling
   measurement exists and the Attempt is not counted measured or SAFE. If the
   Change 3 claim requires every Attempt or automatic collection, the explicit
   command is insufficient; stop and return the exact owner decision required.
   Do not silently add a hook, daemon, watcher, scheduler, sidecar, or service.
4. **Completion and persistence.** Verify `task_complete` closes the selected
   response set and stable post-turn reading exposes all eligible records.
   Verify a typed sibling is compatible with every supported telemetry reader,
   with unchanged receipts, idempotent replay, hard conflicting replay failure,
   and exact readback. If completion is not authoritative, stop with
   `POST_TURN_COMPLETION_SIGNAL_NOT_PROVEN`. If sibling compatibility fails,
   stop with `APPEND_ONLY_SIBLING_RECORD_COMPATIBILITY_NOT_PROVEN`.
5. **Binding.** Verify pre-execution host identity reaches the existing
   Attempt-keyed trace and the exact pending binding survives until explicit
   post-turn collection. If unavailable, stop with
   `AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING_NOT_PROVEN`.

T00 does not run the collector or mutate product data. If any gate fails, stop
before product mutation and report the precise seam; do not expand architecture
or claim a production measurement path from a test-only collector call.

### T01 - Persist the source-bound host-turn binding

Extend only the existing Attempt-keyed operation trace and lifecycle handoff
with the exact Attempt/thread/turn binding and, only if T00 proves one, a
reference to the response-scope ownership signal in Section 5. Verify
pre-execution write/readback, thread/session agreement, unique turn, and
fail-closed missing/conflicting binding. Do not treat the tuple as proof of
response ownership. Keep Attempt identity, route selection, lifecycle order,
and execution authority unchanged.

### T02 - Extract and aggregate only completed response scope

Extend the current host adapter's allowlisted metadata parser for
`token_usage_record.usage`; implement stable streamed rollout reading,
completion checks, exact response-scope filtering from the T00-proven whole-turn
contract or source-bound subset, unique response identity, deterministic
aggregation, metadata null/partial handling, and the frozen reason precedence.
Do not change existing receipt totals or read body content. Select only the
method specified in Section 9.

### T03 - Append and read back the measurement sibling

After turn completion, validate `operation_measurement_v2` and append it with
the existing telemetry owner. Keep each existing RunReceipt byte-for-byte
unchanged. Type-dispatch existing records and the new sibling, make identical
replay idempotent, reject conflicting measurement identity, and prove exact
canonical readback. Abort this task if T00's compatibility gate did not pass.

### T04 - Prove governed association end to end

Exercise the existing Attempt claim, matched guidance, pre-trace, host binding,
proven response scope, governed execution, host completion, and the selected
normal post-turn trigger through its public command entrypoint. Then prove
capture, append/readback, and final association. The trigger may be explicit
user/agent collection under the proposed contract; an internal function call
alone does not satisfy the proof. Prove the receipt and measurement reference
the same Attempt and route evidence without creating another identity or
altering terminalization/PL08 semantics.

### T05 - Complete the focused matrix

Implement only the focused test surface in Section 13 and matrix in Section 16.
Use structured objects and persisted bytes as assertions, not CLI/help/prose
rendering. Preserve old receipt fixtures and current candidate evidence.

### T06 - Bounded later verification gate

After separately authorized implementation, run `uv sync`, the focused owner
tests first, and then `uv run pytest` at the integration/completion gate.
Verify the write boundary, unchanged historical receipt bytes, append-only
sibling coexistence, and exact readback. Adopt the template into a temporary
clean Git consumer and run `planning-lite doctor` there. If update behavior
changed, test an update between two Git tags and verify project-owned files
remain unchanged. Formal Readiness remains a separate later gate.

## 16. Required contract-test matrix

The implementation must add or adapt a named matrix covering every row below.

| ID | Required proof | Expected disposition |
|---|---|---|
| M01 | Exact authoritative Attempt/thread/turn binding and route association. | Same existing Attempt ID and bound tuple accepted; source refs exact. |
| M02 | Wrong thread/session for a bound Attempt. | `UNAVAILABLE`; `HOST_THREAD_SESSION_IDENTITY_UNAVAILABLE`; no SAFE claim. |
| M03 | Wrong or adjacent turn for a bound Attempt. | `UNAVAILABLE`; `HOST_TURN_IDENTITY_UNAVAILABLE`; no latest-turn substitution. |
| M04 | Live/incomplete target turn without `task_complete`. | `UNAVAILABLE`; `TURN_INCOMPLETE`; no finalized sibling append while still live. |
| M05 | Unique eligible response aggregation from `token_usage_record.usage`. | Exact per-field sums and derived uncached input; no cumulative-record summing. |
| M06 | Duplicate identical `(thread_id, response_id)` record. | One contribution; deterministic deduplication and replay stability. |
| M07 | Duplicate response identity with conflicting usage. | `UNAVAILABLE`; `DUPLICATE_RESPONSE_CONFLICT`; no guessed total. |
| M08 | Missing/invalid required per-response usage field. | `UNAVAILABLE`; `REQUIRED_USAGE_MISSING_OR_INVALID`; null usage fields. |
| M09 | Exact compatible host-turn aggregate. | Response sum reconciles exactly; state records compatible reconciliation. |
| M10 | Host-turn aggregate mismatch. | `UNAVAILABLE`; `HOST_TURN_RECONCILIATION_FAILED`; no competing total. |
| M11 | All method-required evidence and descriptive metadata present. | `SAFE + COMPLETE`. |
| M12 | Safe response evidence with one or more descriptive fields absent. | `SAFE + PARTIAL`; absent fields are explicit null. |
| M13 | Unsafe response evidence with incomplete descriptive metadata. | `UNAVAILABLE + PARTIAL`; exactly one stable reason. |
| M14 | Multiple Attempts share a turn without structured response ownership. | Per-Attempt `UNAVAILABLE`; `RESPONSE_OWNERSHIP_AMBIGUOUS`; never divide or timestamp-allocate. |
| M15 | Root-only scope with unproven child/subagent records. | Root may be SAFE; child usage excluded and not attributed. |
| M16 | Append-only `operation_measurement_v2` plus exact readback. | One sibling appended; source RunReceipt bytes unchanged; readback bytes exact. |
| M17 | Identical measurement replay under the same deterministic identity. | Idempotent; one record with unchanged canonical bytes. |
| M18 | Conflicting measurement replay under the same identity. | Hard conflict; no altered or second valid measurement appended. |
| M19 | Historical RunReceipt v1/v2 with no sibling measurement. | Remains readable with cumulative semantics unchanged. |
| M20 | Real or source-faithful Attempt-to-scope-to-normal-trigger-to-usage-to-persistence proof. | Full chain in Section 12 via the selected public post-turn trigger; internal/manual collector invocation alone fails. |
| M21 | Both methods SAFE and comparable, then disagreement. | Response aggregate is sole method; mismatch is hard UNAVAILABLE, never two totals. |
| M22 | Unstable/truncated/replaced rollout during read. | `UNAVAILABLE`; `SOURCE_READ_UNSTABLE`; no SAFE scope claim. |
| M23 | Unproven child response attribution. | Child excluded; no root allocation; root-only result remains separately evaluated. |
| M24 | Whole-turn Attempt ownership/equivalence is authoritatively proven for the supported execution shape. | Whole turn may be SAFE only with complete-scope proof and exact Attempt binding. |
| M25 | Attempt is bound to a turn, but whole-turn response ownership is not proven. | `UNAVAILABLE`; `ATTEMPT_RESPONSE_SCOPE_NOT_PROVEN`; no inference from a single Attempt. |
| M26 | A pre-Attempt response exists in the same host turn. | Exclude only under a proven structured subset; otherwise `ATTEMPT_RESPONSE_SCOPE_NOT_PROVEN`. |
| M27 | An unrelated response exists in the same host turn. | Exclude only under a proven structured ownership signal; otherwise unavailable, never whole-turn SAFE. |
| M28 | Structured subset ownership is proven, if such a supported mechanism exists. | Aggregate exactly the source-bound owned responses; reject sequence/timestamp allocation. |
| M29 | Normal post-turn production trigger. | Invoke the selected explicit public command after completion; exact Attempt binding, replay, append, and readback are proven end to end. |
| M30 | No supported production post-turn trigger exists. | T00 stops with `POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`; no product mutation or automatic claim. |
| M31 | Test-only/direct internal collector call without the selected trigger. | Does not satisfy M20 or normal-path E2E; only the supported public trigger can pass. |

## 17. Failure, stop, and authority boundaries

Stop before product mutation if T00 cannot prove the pre-execution binding,
Attempt-response scope ownership, supported post-turn producer/trigger,
completion signal/order, stable read, or append-only stream compatibility. Use
`ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN` for the scope seam and
`POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN` for the trigger seam. A
Plan-level stop is not permission to add an alternate identity, sidecar, new
database, Stop hook, daemon, scheduler, watcher, or other instrumentation.
Return the exact broken seam for a separate owner decision.

During later implementation, incomplete/ambiguous identity, response
ownership, missing/invalid usage, unstable source, failed reconciliation,
conflicting replay, or route binding failure cannot produce a SAFE number.
Keep the response-specific unavailable reason stable, keep numeric payload
fields null for final UNAVAILABLE, and do not weaken any existing
`BOUNDARY_DELTA` safety checks. Do not change existing cumulative RunReceipt
fields or rewrite persisted history.

This Plan Amendment does not authorize implementation, Formal Readiness,
Roadmap/CURRENT mutation after this candidate is materialized, template changes,
release, staging, commit, push, 09-G, or unrelated work.

## 18. Owner review and next gate

This candidate is ready only for its separate owner review when:

1. The accepted Definition Amendment v2 and scoped R-01/R-02 dispositions are
   represented without changing their meaning.
2. P-01 through P-15 are resolved by this design or held at explicit T00
   scope, trigger, completion, binding, or persistence stop gates. Neither
   P1-01 nor P1-02 is treated as factually proven by this candidate.
3. The named matrix M01-M31 covers whole-turn and subset ownership, pre-Attempt
   and unrelated response cases, trigger availability, safe/partial/unavailable
   outcomes, stability, persistence, compatibility, and normal-path E2E.
4. The proposed implementation surface remains the smallest existing owner
   surface and introduces no new store or authority.
5. Implementation remains unauthorized pending later Formal Readiness and
   separate explicit owner authorization.

The next single gate is:

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V2
```
