# PL-V39-08 RunReceipt Measurement Correction - Fresh Formal Readiness v1

```text
Transition: FORMAL_READINESS_CHANGE_3_RESPONSE_AGGREGATE_PLAN_V4
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Evaluation date: 2026-09-29
Evaluator: Codex / read-only Formal Readiness
Evaluation scope: CURRENT EFFECTIVE AUTHORITY AND ENTRY WORKING STATE
Product/source/test mutation: NO
T00 executed: NO

ENTRY_HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
ENTRY_AUTHORITY_STATE_ID: 0fbeea8b2b0e56df1b4eb90a52efd66b84b8846742df190876731daa62c0cb1f
ENTRY_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
ENTRY_SYNC_STATE_ID: fe40d34fff8af89707736351d5a6d1f84de4c0335ebd66b52d22ad74ab7801c1
ENTRY_INDEX_EMPTY: YES
ENTRY_PARTITIONS: AUTHORITY 29 / CANDIDATE 6 / UNRELATED 12

EFFECTIVE_DEFINITION: PREDECESSOR DEFINITION + AMENDMENT V2
DEFINITION_AMENDMENT_V2: APPROVED_BY_OWNER / ACTIVE
DEFINITION_AMENDMENT_V2_SHA256: e7a47f46c9838ba94ae66acea56c76768e72844a881bf394cfa8fd28bbafa544
DEFINITION_AMENDMENT_V2_ACTIVATION_SHA256: 7e8c1232b29ffc6cdbbc35f7ce3b7356ce5d603ebfb4ab53dc9f2786cd05ca00
EFFECTIVE_PLAN: PREDECESSOR PLAN + PLAN AMENDMENT V4
PLAN_AMENDMENT_V4: APPROVED_BY_OWNER / ACTIVE
PLAN_AMENDMENT_V4_SHA256: e9f2d09f4f8bac0fef81f8a9c79630cf8c65edd6b9084406fd2c9242a9430981
PLAN_AMENDMENT_V4_ACTIVATION_SHA256: 1aa6e9358b11f4a7a7d9e13bc6f6ed0b898ec209dea32ed88a23f88abb4036c4
E1_OWNER_DECISION_SHA256: 9fb067c75c48fbcaa434655dd6e5a2c614c81c75c7eb1f3a3e86d4ad4fe2e8b2
OPTION_C: ACTIVE
E1: ACTIVE

MEASUREMENT_ELIGIBILITY_MODE: EXPLICIT_POST_TURN_COLLECTION_REQUEST
AUTOMATIC_ALL_ATTEMPT_MEASUREMENT: NO
NO_REQUEST: NO_MEASUREMENT_CLAIM
NOT_YET_FINALIZABLE: REQUEST_NOT_YET_FINALIZABLE / NO FINAL SIBLING / RETRY ALLOWED
ACCEPTED_FINALIZABLE_REQUEST: EXACTLY ONE FINAL SAFE OR UNAVAILABLE RESULT
UNIVERSAL_AUTOMATIC_COVERAGE: OUTSIDE CHANGE 3

FINAL_READINESS_VERDICT: READY_WITH_CONTROLLED_DISCOVERY
MATERIAL_READINESS_BLOCKER_COUNT: 0
CONTROLLED_DISCOVERY_REQUIRED: YES
T00_AUTHORIZED: NO
IMPLEMENTATION_AUTHORIZED: NO
09_G_STARTED: NO
PRE_IMPLEMENTATION_OWNER_DISPOSITION_REQUIRED: YES
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_CHANGE_3_RESPONSE_AGGREGATE_T00_CONTROLLED_DISCOVERY
```

## Freshness and evidence basis

This is a fresh evaluation of the active Definition Amendment v2, active Plan
Amendment v4, E1, the current source/test/candidate state, and current
read-only local evidence. The prior Change 3 Formal Readiness artifact
`PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-FORMAL-READINESS-VERDICT-v1.md`
(SHA256 `09aa37a64832948f02f8451fa0a20c9e09a4b03832a58d0c04f11dfd7925a439`)
is historical evidence / precedent only. Its verdict was not inherited.

Effective authority was verified by path and hash: Definition Amendment v2
(`e7a47f46c9838ba94ae66acea56c76768e72844a881bf394cfa8fd28bbafa544`) and its
activation (`7e8c1232b29ffc6cdbbc35f7ce3b7356ce5d603ebfb4ab53dc9f2786cd05ca00`);
predecessor Plan (`91db4e0788b20f342418604e827c2f73b0fc8f16f42fa21139b218130e868f54`);
Plan Amendment v4 (`e9f2d09f4f8bac0fef81f8a9c79630cf8c65edd6b9084406fd2c9242a9430981`)
and activation (`1aa6e9358b11f4a7a7d9e13bc6f6ed0b898ec209dea32ed88a23f88abb4036c4`);
and E1 decision (`9fb067c75c48fbcaa434655dd6e5a2c614c81c75c7eb1f3a3e86d4ad4fe2e8b2`).

The entry candidate is the unchanged six-path source/test state
`37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555`. The
SHA256 of the canonical sorted path-to-content-hash map for all tracked `src/`
and `tests/` files at entry is
`f9eef25162136bcf147ac48db57013b679e39d862c3685b8a727c2536333f85e`. The
Roadmap SHA256 is `4682e29322a574ef77040ea173e06352a99b3da18b527a8b22f3a8c9ffc7d1b0`.

The owner-accepted local probes were checked against their recorded hashes:

| Evidence | SHA256 |
|---|---|
| `CHANGE_3_CODEX_TOKEN_USAGE_RECORD_LOCAL_PROBE_V1.md` | `9cf4d33c90f0a8522c4cc45ba9ade246c82ee1dba5297f0b559cc26cd8139427` |
| `CHANGE_3_CODEX_TOKEN_USAGE_RECORD_LOCAL_PROBE_V1.json` | `f935042e962d3d5fa0707e51091f3757c37dd9121d1ed1830ce856e4a80cb934` |
| `CHANGE_3_PLANNING_LITE_ATTEMPT_TO_CODEX_TURN_MAPPING_PROBE_V1.md` | `ac77d7c175e92ec8ce6ba834b5e920062fd80ca4a1db2fc42fa183c6dad6b0b3` |
| `CHANGE_3_PLANNING_LITE_ATTEMPT_TO_CODEX_TURN_MAPPING_PROBE_V1.json` | `8c235bfb9bb95d8ff1182a330ec25eb77ccfb41658b32e68482dd9f950440246` |

A bounded metadata-only snapshot of the newest local rollout was stable while
read: `C:/Users/yegor/.codex/sessions/2026/09/29/rollout-2026-09-29T07-27-49-01a0eb6b-3dfb-71b2-a1f5-5ac27d26c111.jsonl`, 4,536,329 bytes,
SHA256 `484cdee2e346161e3049d586f39bdff5ce5d60a7cb58a0e57b60c2d768913514`.
The metadata projection showed `session_meta`, structured `turn_context`,
`task_complete`, and per-response `token_usage_record` records. In two
completed turns, 40 and 48 same-turn usage records respectively preceded
`task_complete`; none followed it in this snapshot. Another turn was active.
`CODEX_THREAD_ID` was present in the probe process but did not match this
snapshot's `session_meta.id`. No rollout body content is included here. These
observations are bounded examples, not ownership or completion guarantees.

The earlier mapping probe found one completed root turn with 11 unique response
records whose summed usage matched the compatible final `turn_token_usage`.
It also classified Attempt-to-thread/turn binding as PARTIAL and the local
receipt-to-Attempt reference as NOT PROVEN. This is capability evidence, not
Attempt-to-response-scope proof or proof of a production persistence path.

## Frozen semantics and authority boundaries

Option C is active: `RESPONSE_AGGREGATE` is preferred only when every SAFE
requirement is source-bound; `BOUNDARY_DELTA` remains an independent fail-closed
fallback. E1 is active and frozen: only an explicit post-turn request for one
exact Attempt and source creates eligibility; no request means no measurement
claim; a live target returns `REQUEST_NOT_YET_FINALIZABLE` with no final sibling
and retry allowed; an accepted finalizable request resolves to exactly one
final SAFE or UNAVAILABLE result. Universal automatic coverage is outside
Change 3. T00 may not revise these semantics.

## FR-01 - authoritative pre-execution host binding

**Classification: T00_REQUIRED.** The existing lifecycle proves that it owns
the exact claimed `attempt_id`, matched guidance, expected route, and pre-trace
ordering: `src/planning_lite/operation_lifecycle.py:729-784`. Its current
function signature has no host thread or active turn input. The current
`operation_trace.py` trace fields retain expected route and Attempt receipt
associations, but no host thread/turn tuple. Read-only search of `src/` and
`scripts/` found no `CODEX_THREAD_ID` handoff. The current local snapshot and
prior probe show that thread IDs and structured turn contexts can exist, but
the latest snapshot's process ID did not match its rollout session identity;
the prior exact rollout match still did not prove a lifecycle pre-execution
handoff. Attempt ID and expected-route reference are currently owned; exact
host thread and active turn at the required seam are not proven. T00 can
resolve whether the supported invocation exposes these existing facts without
instrumentation; if not, it must stop with
`AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING_NOT_PROVEN`.

## FR-02 - Attempt response-scope ownership

**Current scope class: C / NOT_YET_PROVEN.** No evidence proves complete root
turn equivalence to one Attempt or an authoritative structured subset. The
observed 11-response aggregate and matching turn total do not join responses to
a Planning Lite Attempt. T00 can classify A, B, or C from existing structured
host/lifecycle evidence (`T00_CAN_RESOLVE_WITHIN_APPROVED_BOUNDARY: YES`): it
may prove A or B only with authoritative ownership evidence; otherwise it
records C and fails closed with `ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN`.
A turn ID, one example, absent second Attempt, timestamps, or sequence proximity
cannot establish ownership.

## FR-03 - E1 explicit request entrypoint

**Assessment: FEASIBLE_WITHIN_EXISTING_COMMAND_BOUNDARY / T00_RUNTIME_HANDOFF_REQUIRED.**
The current standalone `scripts/capture_codex_run_receipts.py` CLI already
accepts an explicit rollout, session ID, and turn ID and preflights all
candidates before append. Its current arguments do not include `attempt_id` or
`source_ref`, and no in-repository production caller automatically invokes it
after `task_complete`. Adding the exact E1 request fields and persisted
Attempt-trace lookup to this existing explicit command fits its current owner
and requires no daemon, scheduler, Stop hook, watcher, sidecar, service, new
Attempt identity, or authority. T00 must verify the exact source handoff and
that lookup/replay never uses recency or latest-record heuristics; if not
technically supported, it stops with
`POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`.

## FR-04 - completion semantics

**Classification: T00_REQUIRED.** Structured `task_complete` exists, and the
bounded samples show same-turn response usage before completion. One prior
completed root turn reconciled exactly to its final host turn aggregate. This
proves event existence and example ordering only. It does not prove that no
later eligible `token_usage_record` can belong to the target scope. T00 must
check the supported sidebar shape's event ordering and stable post-turn source
records. It may not substitute a quiet period, timer, or heuristic for an
authoritative completion signal; failure stops with
`POST_TURN_COMPLETION_SIGNAL_NOT_PROVEN`.

## FR-05 - stable post-turn source read

**Classification: T00_RUNTIME_FACT plus IMPLEMENTATION_DETAIL; no current
architecture blocker.** The current command accepts an exact caller-supplied
rollout path and session/turn IDs. Its `_read_rollout` reads JSONL by line, but
currently has no before/after file identity, size/mtime consistency check, or
bounded stability retry. T00 must confirm the explicit source handoff and
whether a stable post-turn snapshot is observable. Streamed allowlisted parsing,
complete-line enforcement, bounded retry, `(thread_id, response_id)` dedup,
and body-blind usage extraction are implementation details in the existing
capture owner. If source stability cannot be established, stop before product
mutation; do not invent timer semantics.

## FR-06 - append-only sibling compatibility

**SIBLING_COMPATIBILITY: T00_REQUIRED (STRUCTURALLY FEASIBLE_WITHIN_PLAN).**
The current `telemetry.py` scanner validates every line as a RunReceipt and
indexes by `receipt_id`; `capture_codex_run_receipts.py` independently performs
the same receipt-only scan. `workspace.py` resolves the stream path but is not
a record reader. Current write, canonical JSON, lock, fsync, duplicate receipt
identity, and exact receipt readback owners are in `telemetry.py`. A tagged
type-dispatch with separate receipt and measurement indexes/APIs remains inside
that owner and the existing capture adapter; no new store, service, or authority
is indicated. Compatibility is not already implemented. T00 must verify all
supported readers, unchanged old receipt bytes, measurement replay/conflict
behavior, and exact readback; if not safe within these two owners, stop with
`APPEND_ONLY_SIBLING_RECORD_COMPATIBILITY_NOT_PROVEN`.

## FR-07 - minimum implementation surface

**PROPOSED_SURFACE_SUFFICIENT: YES.** Plan v4's eight paths match current
owners: `src/planning_lite/operation_trace.py`,
`src/planning_lite/operation_lifecycle.py`,
`scripts/capture_codex_run_receipts.py`, `src/planning_lite/telemetry.py`,
`tests/test_operation_trace.py`, `tests/test_operation_lifecycle.py`,
`tests/test_codex_run_receipt_capture.py`, and `tests/test_run_receipts.py`.
The operation-trace and receipt test owners exist. Read-only source search found
no additional production reader of `run-receipts.jsonl`; `workspace.py` only
resolves its path. No mandatory ninth production or test path is identified.
T00 must confirm the call graph and stop before enlarging this surface if it
finds a missing owner.

## FR-08 - preserved corrective candidate collision

**Overlapping candidate paths (6):**

- `scripts/capture_codex_run_receipts.py`
- `src/planning_lite/operation_lifecycle.py`
- `src/planning_lite/telemetry.py`
- `tests/test_codex_run_receipt_capture.py`
- `tests/test_operation_lifecycle.py`
- `tests/test_run_receipts.py`

The candidate does not modify `operation_trace.py` or
`tests/test_operation_trace.py`. Plan v4 Section 13 identifies potentially
reusable, after owner review, exact Attempt/route checks, receipt identity and
append/readback discipline, content-blind JSONL scanning, all-candidate
preflight-before-write, and focused identity/replay fixtures. The candidate's
lifecycle trace/route reference guard may inform the future implementation but
is post-execution and does not provide the planned host tuple. The candidate's
`counter_before_boundary`, `counter_after_boundary`, `delta_status`,
boundary-specific reason precedence, and tests for cumulative deltas do not
implement `RESPONSE_AGGREGATE`; they are not selected or ported into that
method. They may remain only for the independent `BOUNDARY_DELTA` fallback.
The current capture hunk adds an UNAVAILABLE measurement inside each RunReceipt;
that is not compatible as-is with E1's no-request/no-claim rule or the v4
sibling carrier. Existing identity/replay and parser primitives can be retained
only after owner review and without changing the preserved candidate bytes.

**Can current candidate bytes be treated as the implementation baseline: NO.**
They are preserved evidence, not an automatic baseline. A separate owner
disposition is required before any implementation write or adoption of
overlapping candidate hunks. **T00 readiness impact: NONE.** T00 is read-only
and must leave all six candidate paths unchanged.

## FR-09 - bounded T00 scope sufficiency

**T00_REQUIRED: YES. T00_QUESTION_COUNT: 8.** One bounded read-only T00 can
settle the runtime facts or return the exact Plan stop seam without changing
Definition, Plan, semantics, identity authority, or architecture:

1. **Pre-execution binding:** determine whether the existing invocation owner
   receives the exact Attempt ID, host thread, one active structured turn, and
   expected route before measured execution; verify exact binding persistence.
2. **Response ownership:** classify A/B/C using source-bound evidence; identify
   pre-Attempt/unrelated responses; never infer ownership from turn equality,
   absence, timestamps, proximity, or one example.
3. **E1 request/source handoff:** verify the public explicit command can take
   exact `attempt_id` and `source_ref`, resolve the persisted binding and route,
   and reject conflicting or heuristic lookup.
4. **Completion/finalizability:** verify `task_complete` closes the eligible
   response set, no later eligible usage appears, and live requests create no
   final sibling and remain retryable.
5. **Stable source read:** verify exact source identity, complete lines, stable
   size/mtime or equivalent, bounded retry, and no body parsing.
6. **Structured usage:** verify eligible response identity, required numeric
   usage, deterministic deduplication, final-turn reconciliation, and fail-closed
   outcomes for the target scope.
7. **Tagged sibling compatibility:** inspect all supported stream readers and
   the existing append owner for unchanged receipts, typed dispatch, idempotent
   identical replay, conflicting replay rejection, and exact readback.
8. **Owner/surface boundary:** confirm the planned eight paths suffice and record
   the six candidate overlaps without modifying or adjudicating them. Candidate
   disposition remains an owner decision before implementation.

T00 must not execute the collector, append records, mutate source/tests, choose
eligibility/coverage semantics, add instrumentation, or authorize implementation.
A failed runtime fact stops before product mutation with the exact Plan-defined
seam.

## FR-10 - false-ready defense

| Hypothesis | Defense |
|---|---|
| FRA-01: `CODEX_THREAD_ID` exists but not at the pre-execution seam. | `PASS_FALSE_READY_DEFENSE` - current source has no host handoff; exact seam is a mandatory T00 gate and failure stops. |
| FRA-02: Attempt is bound to a turn but response ownership is unproven. | `PASS_FALSE_READY_DEFENSE` - current class is C / NOT_YET_PROVEN; T00 must prove A/B or stop fail-closed. |
| FRA-03: `task_complete` exists but does not close eligible usage. | `PASS_FALSE_READY_DEFENSE` - sample ordering is not a closure guarantee; T00 verifies exact response-set closure. |
| FRA-04: capture command cannot carry exact Attempt/source without heuristic lookup. | `PASS_FALSE_READY_DEFENSE` - current args are explicit but lack those fields; T00 proves the proposed extension or stops. |
| FRA-05: mixed telemetry breaks an existing receipt reader. | `PASS_FALSE_READY_DEFENSE` - both current readers are identified and strict; tagged-sibling compatibility is a mandatory T00 stop gate. |
| FRA-06: implementation needs a path outside the eight paths. | `PASS_FALSE_READY_DEFENSE` - current reader inventory shows no ninth owner; T00 confirms before any path expansion. |
| FRA-07: preserved candidate must be destructively replaced. | `PASS_FALSE_READY_DEFENSE` - candidate is not an automatic baseline; separate owner disposition is required before overlapping writes. |
| FRA-08: T00 would need to make a semantic or architecture decision. | `PASS_FALSE_READY_DEFENSE` - E1 semantics are fixed; T00 may discover facts only and must stop for owner review if expansion is needed. |

No false-ready hypothesis is accepted as proven. No material prerequisite outside
the bounded T00 boundary is currently established. The outstanding preserved
candidate disposition is a pre-implementation owner gate and does not authorize
or block read-only T00.

## Verdict and next legal gate

**FORMAL READINESS VERDICT: READY_WITH_CONTROLLED_DISCOVERY**

The present state is not `READY` because mandatory binding, response-scope,
completion, stable-read, and sibling-compatibility facts are not proven. It is
not `BLOCKED` because those facts are explicitly bounded read-only T00 questions
under the active Plan, and no new semantic decision or architecture is required
to investigate them. No implementation authorization follows from this verdict.

```text
CONTROLLED_DISCOVERY_REQUIRED: YES
T00_AUTHORIZED: NO
IMPLEMENTATION_AUTHORIZED: NO
09_G_STARTED: NO
PRE_IMPLEMENTATION_OWNER_DISPOSITION_REQUIRED: YES
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_CHANGE_3_RESPONSE_AGGREGATE_T00_CONTROLLED_DISCOVERY
```

This checkpoint records Formal Readiness only. It does not perform T00, mutate
product source/tests, change Roadmap or the preserved candidate, stage, commit,
push, release, or start 09-G.
