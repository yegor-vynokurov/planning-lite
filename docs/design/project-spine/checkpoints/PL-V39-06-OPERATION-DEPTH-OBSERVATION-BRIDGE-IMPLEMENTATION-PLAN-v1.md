# CHG-PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-001 — Implementation Plan v1

- Status: `APPROVED BY OWNER`
- Date: `2026-09-17`
- Change: `CHG-PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-001`
- Definition: `APPROVED BY OWNER`
- Definition artifact: `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-CHANGE-DEFINITION-v1.md`
- Definition activation: `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-ACTIVATION-v1.md`
- Reviewed Plan candidate: `.local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_PLAN_CANDIDATE.md`
- Reviewed Plan candidate SHA256: `E7A2A7C06D14C66A5532CFFE3222D8E6A28B6F82BC7044CF2E928691819D8FB5`
- Plan approval: `YES / USER EXPLICIT / current conversation`
- Formal Readiness: `NOT RUN`
- Planning Authority Checkpoint: `NOT AUTHORIZED / NOT PERFORMED`
- Implementation authorization: `NO`
- Commit/tag/push/merge/release authorization: `NO`

## 1. Plan identity and authority

This Plan is the implementation-design authority for the approved Change. It
does not grant implementation authorization or replace current-state
authority. Authority order is:

1. approved Change Definition;
2. Definition activation and canonical `CURRENT.md`;
3. this owner-approved Plan;
4. later separately authorized Planning Authority, readiness, and execution
   evidence.

The entry baseline is HEAD `9ed53bec583fe4432f0fd42405ef1cfa53df5a65` with
only the three preceding approved Definition-activation paths dirty:

```text
docs/design/project-spine/CURRENT.md
docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-CHANGE-DEFINITION-v1.md
docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-ACTIVATION-v1.md
```

No unrelated tracked dirt is part of this Plan. The major PL09 next-slice gate
`OWNER_ADJUDICATION_PL_V39_09_NEXT_SLICE_AFTER_09-B_CLOSURE` remains preserved
and unconsumed.

The owner decision recorded by this transition is:

```text
PLAN_STATUS: APPROVED_BY_OWNER
OWNER_PLAN_DECISION: APPROVE
FORMAL_READINESS: NOT_RUN
PLANNING_AUTHORITY_CHECKPOINT: NOT_AUTHORIZED / NOT_PERFORMED
IMPLEMENTATION_AUTHORIZED: NO
```

## 2. Implementation objective

Add one derived, immutable operation-depth observation projection that:

- captures the bounded start state already present in a `ResumeContextV1` /
  `ContextTraceV1` result;
- records only later exact expansions returned through the existing PL06
  `build_resume_context(..., include=...)` seam;
- preserves source identity, revision/hash, role, section, reason, freshness,
  bounded volume, and sequence from those existing outputs;
- detects repeated/reopened exact sources deterministically; and
- reports `UNAVAILABLE` for reads that Planning Lite cannot observe.

The existing resume output remains unchanged by default. The observation is
constructed on demand, in memory, and is never persisted by this Change.

## 3. Architecture decision

### 3.1 Existing owner surface only

Implement entirely in `src/planning_lite/context.py`. No adjacent helper is
justified: source selection, source metadata, freshness, storage class,
explicit-expansion bounds, and path/security checks already belong there.

Add one public immutable contract, following existing PL dataclass conventions:

```text
OperationDepthObservationV1  (frozen, slots, derived only)
  from_resume_context(resume_context, operation_ref=None)
  record_expansion(expansion_resume_context, sequence_index=None)
  record_unavailable(reason_code, sequence_index=None, source_ref=None)
  to_dict()
```

The methods return a new value rather than mutating an existing value. They do
not read the filesystem, invoke the CLI, inspect host logs, or reconstruct a
resume context. They accept already-built mappings returned by the existing
context builder and copy only the approved metadata projection.

Reuse `ContextError` for malformed or unsafe inputs; do not create a second
exception family. Keep `build_resume_context`, `resume_context`, and
`validate_resume_context` behavior and output compatible for existing callers.

### 3.2 Why no adjacent helper or CLI change

The CLI already exposes the approved producer as
`planning-lite resume TARGET --json --include PATH[#HEADING]`. Adding a CLI
observer, host hook, telemetry carrier, or separate helper would widen the
write/authority surface without improving the approved capability. The
walking skeleton imports the new projection from the existing module while
using the real CLI/resume producer for its input snapshots.

## 4. Exact implementation surface

The later authorized implementation may modify only:

```text
src/planning_lite/context.py
tests/test_context_resume.py
```

The existing context test module already owns deterministic selection, exact
heading expansion, freshness, forbidden paths, raw-field rejection, bounds,
and read-only behavior. Add focused tests there rather than creating a second
test subsystem. No `template/`, `telemetry.py`, RunReceipt, routing, adapter,
CURRENT, Roadmap, recommendation, skill/checklist, consumer, host-monitor,
registry, or database path is permitted.

## 5. Minimal data/projection shape

`OperationDepthObservationV1.to_dict()` exposes only the approved shape:

```text
operation_ref: opaque source-bound reference | null
start:
  context_trace_ref or inline derived identity
  source_revision / freshness
  selected_sources[] {path/ref, sha256, role, storage_class, reason, section}
  selected_artifact_count
  selected_section_count
  selected_character_count
  explicit_expansion_count
  bounds
expansions[]:
  sequence_index
  source_ref {path/ref, sha256} | null when no safe identity exists
  role / storage_class | null when unavailable
  reason_family | null when unavailable
  section | null
  source_revision / freshness
  bounded_volume | null
  repeated_or_reopened: YES | NO | UNAVAILABLE
  completeness: COMPLETE | PARTIAL | UNAVAILABLE
overall_completeness: COMPLETE | PARTIAL | UNAVAILABLE
unavailable_reasons[]
```

The start projection copies existing `context_trace` metadata and
`git_identity` revision/status; it does not compute a second trace or source
body digest. For an expansion event, `bounded_volume` is the existing bounded
`selected_character_count` metric from the supplied expansion snapshot (or
null when unavailable); the implementation must not reread or count source
body text. Depth remains a derived interpretation of event count and existing
roles/storage classes, not a new canonical enum.

`operation_ref` is optional, nonempty when supplied, has no newline, and is an
opaque linkage only. It cannot name a route, authorize work, encode a cycle,
or carry semantic results.

## 6. Operation-start construction

`OperationDepthObservationV1.from_resume_context` receives one already-built
`ResumeContextV1` mapping. It must:

1. Validate that `context_trace`, `git_identity`, and required trace fields
   exist and have expected bounded shapes.
2. Copy only each selected source's existing `path`, `sha256`, `role`,
   `storage_class`, `reason`, and `section` values.
3. Copy existing trace counts and `bounds` without recomputation.
4. Carry `git_identity.head`/`state` as source revision and resume status as
   freshness/status.
5. Start with an empty expansion tuple and `overall_completeness=COMPLETE`
   when the supplied snapshot is current and valid.

If required owner fields are absent or the supplied resume status is unusable,
return an explicit unavailable observation with `INVALID_START_CONTEXT` and no
fabricated source metadata. If the caller supplies a non-mapping, unknown/raw
source fields, an invalid operation reference, or another structurally unsafe
value, raise `ContextError` and retain no observation. Never call
`build_resume_context` again.

## 7. Explicit expansion recording

An approved observable expansion is produced only by an exact,
repository-relative path or exact Markdown heading passed to the existing
`build_resume_context(..., include=[...])` API (or equivalent read-only CLI
command). The returned snapshot is passed to `record_expansion`; the method
does not accept a raw path, body, prompt, response, host/tool log, timestamp,
or token signal as evidence.

For one later expansion snapshot, the method accepts exactly one explicit
source entry with `role=explicit_expansion`, or one bounded
`expansion_results` entry such as `EXPANSION_TOO_LARGE`. Zero or multiple event
entries is a malformed snapshot and raises `ContextError`; the caller uses
`record_unavailable(NO_APPROVED_SEAM)` for a bypassed read. It copies existing
source metadata and snapshot revision/status only; it does not reread files.

If the existing producer rejects a path or heading, the caller may record an
unavailable event using the finite reason code, but may not smuggle the
rejected path or body into the observation.

## 8. Deterministic repeat/reopen semantics

Use the exact source identity tuple:

```text
(normalized source path/reference, sha256, section)
```

The first occurrence is `repeated_or_reopened=NO`. A later event with the same
tuple is `YES`; a different path, hash, or section is `NO`, even when contents
look similar. A changed hash is not a repeat and is handled by freshness rules.
No similarity, prose, filename mention, host log, or timing inference is
permitted.

Sequence indexes are one-based, contiguous, and monotonic. An omitted index is
the next expected index. A supplied index that is not the next index raises
`ContextError` and leaves the prior immutable value unchanged.

## 9. `UNAVAILABLE` semantics

`record_unavailable` appends a bounded event with `completeness=UNAVAILABLE`
and `repeated_or_reopened=UNAVAILABLE`. `source_ref` is null unless an exact
safe reference was already returned by PL06; no unsafe path is copied.

Use this finite reason set:

```text
INVALID_START_CONTEXT
NO_APPROVED_SEAM
STALE_SOURCE
SUPERSEDED_SOURCE
MISSING_SOURCE
FORBIDDEN_SOURCE
EXPANSION_TOO_LARGE
```

`EXPANSION_TOO_LARGE` may be `PARTIAL` when exact source/heading metadata is
known but the existing PL06 limit prevented selection; bypassed, stale,
forbidden, missing, malformed, and otherwise unknowable reads are
`UNAVAILABLE`. Overall completeness precedence is:
`UNAVAILABLE` > `PARTIAL` > `COMPLETE`.

## 10. Bounds and fail-closed rules

- Reuse the existing `MAX_EXPANSIONS` value as the maximum total observed
  expansion events for one operation observation; no append stream is
  unbounded.
- Bound unavailable reasons to the same event limit and preserve event order.
- Reuse `_safe_path`, `_source`, `classify_storage`, `_sha`, existing forbidden
  read policy, exact-heading parsing, and current freshness/status semantics.
- Do not add a second selector, classifier, hash implementation, history scan,
  glob search, semantic search, or host-read hook.
- Reject unknown/raw fields in source metadata and expansion snapshots; raw
  body, prompt, response, tool payload, and hidden-reasoning keys never enter
  the projection.
- Reject non-normalized or unsafe operation references and source references.
- Invalid sequence, malformed snapshot, and over-limit event raise
  `ContextError` without mutating the prior immutable value; stale/superseded
  source and unsafe selector inputs fail closed through existing guards.

## 11. Task graph

### T-01 — Define the derived projection and invariants

Add the frozen `OperationDepthObservationV1` contract, exact `to_dict()` shape,
bounded reason codes, immutable copy/return behavior, and validation helpers
inside `context.py`. Preserve existing resume output compatibility.

### T-02 — Bind start state and approved expansion snapshots

Implement construction from an existing `ResumeContextV1` / `ContextTraceV1`
mapping and recording from one exact-expansion resume snapshot. Reuse existing
source metadata, revision/status, selector, and freshness guards; perform no
filesystem or host-log reads in the new projection.

### T-03 — Implement repeat, `UNAVAILABLE`, and bounds behavior

Add exact identity comparison, contiguous sequence validation, completeness
precedence, finite reason handling, raw-field rejection, and the five-event
observation cap.

### T-04 — Focused deterministic and nearest-wrong tests

Extend `tests/test_context_resume.py` with the required cases below and prove
the existing resume/CLI tests remain compatible.

### T-05 — Walking skeleton and scope/privacy evidence

Run the real disposable-fixture proof, read back canonical JSON, compare
identities/hashes/bounds, verify no product/tracked mutation, and prepare the
owner-acceptance evidence set. T-05 does not authorize implementation or
commit by itself.

Dependency order: `T-01 -> T-02 -> T-03 -> T-04 -> T-05`.

## 12. Focused test matrix

All tests belong in `tests/test_context_resume.py` and use the existing
disposable `_project` fixture pattern.

| Case | Proof |
|---|---|
| Start-only | Build one resume snapshot; projection start equals existing trace metadata, with no events and `COMPLETE`. |
| One explicit expansion | Exact path/heading snapshot yields one event with copied identity, revision, role, reason, section, bounded volume, and no body. |
| Repeated exact source | Record identical snapshot twice; second event is `YES`, with deterministic output. |
| Similar but different source | Same content at a different path or section remains `NO`. |
| Unobservable/bypassed read | Record `NO_APPROVED_SEAM`; event is `UNAVAILABLE` and contains no inferred path/body. |
| Stale source | Existing handoff freshness returns `STALE`; recording yields `STALE_SOURCE`/`UNAVAILABLE`, not current evidence. |
| Forbidden/outside-root | Existing builder rejects inbox, `.git`, glob, parent escape, and outside-root selectors; observation retains no rejected body/path. |
| Invalid sequence | First non-one or noncontiguous index raises `ContextError`; prior value is unchanged. |
| Raw-body rejection | Inject body/prompt/response/tool fields into supplied metadata; exact validator rejects and output contains no sentinel. |
| Deterministic repeated input | Two identical start/expansion inputs produce byte-equivalent canonical JSON. |
| Bounds | Five events are bounded; a sixth raises `ContextError` and leaves the prior value unchanged. |
| No tracked mutation | Snapshot construction and projection leave fixture files, Git status, and existing CLI read-only inventory unchanged. |

Retain existing tests for exact headings, oversize expansion,
`MISSING_OWNER_ARTIFACT`, `SUPERSEDED`, symlink/reparse, and fixed excluded
categories; do not duplicate their invariants unnecessarily.

## 13. Real walking-skeleton proof

Use a disposable clean Git fixture created by the existing test helper or an
equivalent temporary repository. Through the real producer:

1. run `uv run planning-lite resume FIXTURE --json` and pass the parsed result
   to `OperationDepthObservationV1.from_resume_context`;
2. create one eligible exact plan/heading and run
   `uv run planning-lite resume FIXTURE --include PATH#HEADING --json`;
3. pass that result to `record_expansion`, repeat it, and inspect canonical JSON
   and the repeat marker;
4. exercise a bypassed/forbidden read and record `UNAVAILABLE` without using
   host logs or raw content; and
5. compare source refs/hashes/bounds and fixture file/Git inventories before
   and after.

The proof demonstrates that the API consumes existing snapshots rather than
rebuilding them and that no body text, transcript, registry, or tracked state
is written. It is evidence for later acceptance, not a new production command.

## 14. Evidence before owner acceptance

- T-04 focused test results and nearest-wrong discriminator results;
- walking-skeleton output/readback with deterministic canonical JSON;
- source identity/hash/revision, role, section, reason, freshness, volume, and
  sequence comparison against producer snapshots;
- no-body/privacy inspection and raw-field rejection evidence;
- event-bound and invalid-sequence evidence;
- fixture write-boundary and Git-scope audit;
- confirmation that existing `build_resume_context` and CLI output remain
  compatible;
- review confirmation that PL07 routing, PL08 evaluation, RunReceipt v1, and
  deferred PL09/Change 2 boundaries remain untouched; and
- later readiness, implementation-authorization, acceptance, commit, and
  post-commit gates when authorized.

## 15. Contradiction classification

| Question | Classification | Handling |
|---|---|---|
| Existing ContextTrace already has start/expansion metadata | `RESOLVABLE` | Consume the existing snapshot; do not rebuild or duplicate context. |
| Existing builder can observe only exact approved expansions | `RESOLVABLE` | Make the seam explicit; all bypassed reads are `UNAVAILABLE`. |
| Per-event body length is unavailable without rereading source | `RESOLVABLE` | Use existing bounded aggregate volume or null; never copy/count body text. |
| Future semantic-cycle attachment and full trace fields | `MATERIAL_LATER` | Downstream Change 2 only; not frozen or implemented here. |
| Any need for template, telemetry, routing, registry, host observer, or extra lifecycle path | `MATERIAL_NOW` | None found; if discovered during implementation planning, STOP. |

## 16. STOP conditions

Stop without widening scope if implementation requires a tracked path other than
the two approved source/test surfaces; a new CLI/host observer; any raw prompt,
response, transcript, source body, tool payload, or hidden reasoning; persistent
memory/registry/database; a second selector/classifier; RunReceipt or
token/cache changes; prompt-dedup activation; semantic-cycle identity or digest
fields; expected-route binding; AgentWorkPacket/Context Compiler; unbounded
events; a new human gate; or PL07/PL08/PL09 authority transfer.

Also stop for a material contradiction affecting current scope, safety,
acceptance evidence, implementation shape, or lifecycle truth. Do not silently
resolve `MATERIAL_NOW`.

## 17. Explicit non-goals and Change 2 dependency

No semantic work-cycle identity, INPUT/OUTPUT digest schema, expected-route
binding, post-result semantic trace, full-cycle persistence, token/cache delta,
runtime prompt dedup, skill logging, dashboards, AgentWorkPacket schema,
Context Compiler, host monitoring, transcript retention, RunReceipt change, or
statistics/audit claim is part of this Plan.

Change 2 may consume this observation and define cycle linkage and semantic
pre/during/post/result fields under a separate Definition and owner gate. This
Plan remains independently implementable if Change 2 is deferred or rejected.

## 18. Rollback and reversibility

The implementation is additive and derived-only: no persisted records,
migrations, or consumer state are created. Reverting the reviewed source/test
patch restores the prior API and behavior without cleanup or data migration;
any in-memory observation is discarded with its invocation. Existing
`ResumeContextV1` output and external evidence remain readable.

## 19. Retention invariants

```text
RAW_TRANSCRIPT_COPY_INTO_PLANNING_LITE: FORBIDDEN
RAW_PROMPT_STORAGE: FORBIDDEN
RAW_RESPONSE_STORAGE: FORBIDDEN
SOURCE_BODY_COPY_FOR_OBSERVABILITY: FORBIDDEN
HOST_RAW_TRANSCRIPT: EXTERNAL / OPTIONAL / RETENTION_DEPENDENT / NONAUTHORITY
PLANNING_LITE_OPERATION_MEMORY: COMPACT_DERIVED_METADATA_AND_SOURCE_REFS_ONLY
```

## 20. Next lifecycle gate

```text
OWNER_AUTHORIZATION_PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_PLANNING_AUTHORITY_CHECKPOINT
```

The Plan approval transition does not create or authorize that checkpoint.
Formal Readiness, implementation authorization, execution, acceptance,
checkpoint commit, and closure remain separate later gates.
