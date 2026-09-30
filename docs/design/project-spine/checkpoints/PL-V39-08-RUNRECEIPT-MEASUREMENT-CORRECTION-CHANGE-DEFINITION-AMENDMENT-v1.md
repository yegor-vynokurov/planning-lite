# PL-V39-08 RunReceipt Measurement Correction — Definition Amendment v1

## 1. Candidate identity and authority

```text
Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-DEFINITION-AMENDMENT-001
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Lineage name: CHANGE_3
Owner decision: SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT
Status: CANDIDATE / OWNER_REVIEW_REQUIRED
Predecessor Definition: PL-V39-08 RunReceipt Measurement Correction — Approved Definition v1
Predecessor Definition path: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-v1.md
Predecessor Definition SHA256: cef899a6a6b2ced4d1bef1e266969cd2b57981d5b59275b77e8e093e2d9d21cc
Owner decision checkpoint: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-OPTION-C-OWNER-DECISION-v1.md
Approval: NOT GRANTED
Activation: NOT GRANTED
Implementation authorization: NO
Plan Amendment: REQUIRED AFTER DEFINITION ACCEPTANCE / NOT PREPARED
09-G: NOT STARTED
```

This document is one proposed semantic amendment for owner review. It does not
approve, activate, or replace the predecessor Definition. The approved v1
Definition remains immutable historical authority for the semantics under
which the existing corrective implementation candidate was prepared. Only a
later explicit owner acceptance and activation can make amended semantics
authoritative. No product, test, telemetry, or Plan changes are authorized by
this candidate.

## 2. Proposed amended capability

The predecessor describes boundary-subtraction-only operation measurement. The
proposed amendment generalizes that contract to:

```text
SOURCE-BOUND OPERATION-LOCAL MEASUREMENT
```

For each eligible governed operation, the system may claim `SAFE` usage only
when one explicitly identified and versioned measurement method satisfies its
own evidence requirements and the source, identity, route, completeness, and
fail-closed invariants below. Otherwise the method-specific result is
`UNAVAILABLE` with a reason. A numeric value by itself does not establish a
safe operation-local claim.

The methods are:

1. `RESPONSE_AGGREGATE` — preferred for a runtime such as Codex when authoritative
   per-response usage records and exact operation binding are available.
2. `BOUNDARY_DELTA` — fallback when compatible authoritative before/after
   cumulative counters are the available operation-local source.

The owner decision rejects further pursuit of a new cumulative before/after
host-counter handoff as the preferred Change 3 path. It does not remove the
existing boundary-delta capability or authorize its implementation candidate
to be reverted.

## 3. Method A — RESPONSE_AGGREGATE

`RESPONSE_AGGREGATE` sums structured usage from the unique responses belonging
to one completely proven operation scope. It does not use cumulative
before/after subtraction.

### 3.1 SAFE requirements

All of the following are required before a response aggregate may be `SAFE`:

1. The existing authoritative Planning Lite Attempt and operation identity are
   bound to the measured scope. No replacement Attempt or operation identity
   is created.
2. The expected route comes from its existing source-bound owner, such as the
   pre-execution Operation Guidance or accepted operation trace. Measurement
   does not select or rewrite that route.
3. Authoritative host session/thread and host turn identities bind the complete
   claimed scope. The source-bound join from Attempt/operation to
   `(thread_id, turn_id)` must be exact and auditable.
4. The turn is completed, or an equivalent structured signal proves the
   response scope complete. A partial live turn cannot be reported as a
   complete aggregate.
5. Per-response usage and identifiers come from structured host telemetry.
   Prompt, response, reasoning, and tool-result body parsing is not a source of
   identity or usage.
6. Records are deduplicated deterministically by stable response identity,
   preferably `(thread_id, response_id)`. Missing or conflicting identity,
   duplicate identity with conflicting usage, or missing required numeric
   fields makes the affected scope `UNAVAILABLE`.
7. Each supported numeric usage field is summed deterministically across the
   unique eligible records. Derived fields such as uncached input may be
   reported only when their source fields are complete, semantically
   compatible, and arithmetically valid within that same scope.
8. When a host turn aggregate is present and semantically compatible, the
   per-response sum reconciles exactly to it for every comparable field. A
   mismatch fails closed. If the host aggregate is absent or not semantically
   comparable, that fact is explicit and is not presented as a successful
   reconciliation.
9. There is no missing or ambiguous response ownership within the claimed
   operation scope. If multiple Planning Lite Attempts share one Codex turn and
   the responses cannot be assigned deterministically to each Attempt, each
   per-Attempt measurement is `UNAVAILABLE`; the turn total must not be divided,
   apportioned, or guessed.

No cumulative before/after counter is required for this method. Direct OpenAI
API calls and new Codex instrumentation are not required to calculate a root
turn aggregate from the already persisted local response records.

### 3.2 Root and child scope

A fully proven root-turn scope may be `SAFE` independently of whole-agent-tree
attribution. Child or subagent usage is excluded from a parent/root aggregate
unless the relevant lineage and ownership are separately proven. Partial
whole-tree attribution does not block a root-only measurement, and root-only
evidence does not imply whole-tree completeness.

### 3.3 Present binding seam

The accepted local evidence establishes that sidebar sessions persist
structured per-response usage; thread, turn, session, root-turn, response, and
numeric usage fields are available; current turn identity can be read from
structured metadata; and a completed observed root turn can be aggregated and
reconciled without boundary subtraction. Existing receipt structures carry
host session and turn identities, and receipt schema v2 permits `attempt_id`.

The exact authoritative Attempt-to-`(thread_id, turn_id)` join is not yet
implemented or proven. The candidate therefore defines a permitted method and
its safety contract; it does not claim that the current capture path already
produces a `SAFE` governed response aggregate.

## 4. Method B — BOUNDARY_DELTA

`BOUNDARY_DELTA` preserves the predecessor Definition's boundary semantics.
It is available as a fallback when compatible authoritative before/after
counters are the operation-local source. A result is `SAFE` only when the
existing requirements remain proven, including:

```text
same authoritative host session
+ known before and after boundaries
+ compatible counter scope
+ deterministic subtraction
+ authoritative operation binding
+ source-bound expected route
+ complete telemetry
```

Missing or ambiguous boundary provenance, counter scope, session continuity,
operation binding, route linkage, or completeness produces `UNAVAILABLE` with
a reason. Cumulative snapshots retain their cumulative meaning and are never
relabeled as deltas. In particular, the terminal cumulative counter is not an
operation-local measurement.

All predecessor v1 delta equations and fail-closed rules remain applicable to
`BOUNDARY_DELTA`, including cached plus uncached input reconciling with input
when all values are available under the same safe boundary. This candidate does
not weaken the boundary method to make the current corrective candidate pass.

## 5. Invariants shared by both methods

Every method remains evidence, not authority. It must preserve existing
Attempt, operation, task, run-family, invocation, route, and identity ownership;
bind the measurement to the source records that support it; report completeness
and method explicitly; preserve deterministic replay/idempotence; distinguish
a measured zero from `UNAVAILABLE`; and never substitute guessed zero or an
approximation for missing evidence. Measurement cannot select or retroactively
redefine a route, create execution authority, or claim economics policy.

The receipt's existing cumulative token fields remain unchanged and
cumulative. Raw cumulative snapshots are never silently converted, renamed, or
reinterpreted as operation-local values. Unsafe or ambiguous evidence must not
produce a number that looks like a valid operation measurement.

## 6. Additive, versioned representation

The existing measurement schema v1 and its delta fields keep their current
meaning: v1 represents `BOUNDARY_DELTA` under the predecessor contract. No
response sum may be written into a v1 `*_delta` field, and no existing v1
field is silently reinterpreted.

The proposed additive representation is a versioned sibling record named
`operation_measurement_v2`, with `schema_version: 2`, an explicit
`measurement_method` (`RESPONSE_AGGREGATE` or `BOUNDARY_DELTA`), a method
version, source-bound operation/Attempt and host identity references, explicit
scope/completeness, status, and method-specific payload. Its
`RESPONSE_AGGREGATE` payload carries the response source, stable deduplication
basis, eligible unique response count, supported aggregate usage fields, and
host-turn reconciliation state. Its `BOUNDARY_DELTA` payload carries the
existing boundary and delta semantics. The two payloads do not share ambiguous
field names that could make a response sum appear to be a subtraction.

This sibling is additive to existing receipt content. It does not migrate,
overwrite, or backfill historical v1 records, and it does not change the
independent RunReceipt schema version. The exact persisted carrier remains a
later implementation detail only within this explicit versioned semantic
boundary; implementation and focused tests require a separately reviewed Plan
Amendment and authorization.

## 7. Findings and current candidate

The existing corrective implementation candidate remains preserved as
historical and implementation evidence, with state ID
`37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555`. It is
not edited, reverted, or accepted by this candidate.

`R-01 SAFE_BOUNDARY_PROVENANCE_NOT_BOUND` and
`R-02 M13_CAPTURE_TO_GOVERNED_HANDOFF_NOT_PROVEN` remain open findings against
the boundary-delta-only corrective candidate. The new response evidence offers
a different Codex measurement route that may supersede the need to resolve one
or both findings for `RESPONSE_AGGREGATE`; it does not close either finding by
fiat. Owner review must decide exact closure or supersession wording. Until
then, boundary delta remains fail-closed wherever provenance is missing, and
the response route remains unavailable until exact Attempt-to-turn ownership
and all other SAFE requirements are proven.

## 8. Evidence references and limits

The owner-accepted read-only evidence is recorded in the Option-C decision
checkpoint and consists of these external artifacts:

| Artifact | SHA256 |
|---|---|
| `D:\documents\planning-lite-sync\CHANGE_3_CODEX_TOKEN_USAGE_RECORD_LOCAL_PROBE_V1.md` | `9cf4d33c90f0a8522c4cc45ba9ade246c82ee1dba5297f0b559cc26cd8139427` |
| `D:\documents\planning-lite-sync\CHANGE_3_CODEX_TOKEN_USAGE_RECORD_LOCAL_PROBE_V1.json` | `f935042e962d3d5fa0707e51091f3757c37dd9121d1ed1830ce856e4a80cb934` |
| `D:\documents\planning-lite-sync\CHANGE_3_PLANNING_LITE_ATTEMPT_TO_CODEX_TURN_MAPPING_PROBE_V1.md` | `ac77d7c175e92ec8ce6ba834b5e920062fd80ca4a1db2fc42fa183c6dad6b0b3` |
| `D:\documents\planning-lite-sync\CHANGE_3_PLANNING_LITE_ATTEMPT_TO_CODEX_TURN_MAPPING_PROBE_V1.json` | `8c235bfb9bb95d8ff1182a330ec25eb77ccfb41658b32e68482dd9f950440246` |

One completed observed root turn had 11 unique response records. Their aggregate
was input `547702`, cached input `468224`, uncached input `79478`, output
`56429`, reasoning output `25178`, and total `604131`; it exactly matched the
final host `turn_token_usage`. The evidence establishes local measurement
capability, not governed Attempt binding, current product integration, child
lineage completeness, or whole-agent-tree safety.

## 9. Authority and next gate

This candidate authorizes no product or test mutation, schema implementation,
additional corrective pass, Roadmap change, Plan Amendment preparation,
Formal Readiness, stage, commit, push, release, promotion, or 09-G work. The
existing Plan remains historical authority for its original scope only. After
the owner accepts an exact Definition Amendment, a separate Plan Amendment is
required before implementation of the amended semantics.

The only next gate is:

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_DEFINITION_AMENDMENT
```

