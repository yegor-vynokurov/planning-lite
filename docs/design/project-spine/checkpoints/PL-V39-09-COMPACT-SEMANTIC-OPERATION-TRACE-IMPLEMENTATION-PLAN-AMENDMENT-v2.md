# PL-V39-09 Compact Semantic Operation Trace
## Implementation Plan Amendment v2

**Amendment purpose:** `POST-S6 LIVE INTEGRATION AND DURABLE TRACE PERSISTENCE CORRECTION`

This Amendment is cumulative over:

```text
Implementation Plan v1
+ Implementation Plan Amendment v1
+ Implementation Plan Amendment v2
```

Amendment v2 replaces only the exact stale or unresolved integration clauses
defined below.

All unaffected Definition and Plan semantics remain in force.

# 2. Owner adjudication

Materialize:

```text
ARCHITECTURE_CHANGE_REQUIRED:
NO

DEFINITION_AMENDMENT_REQUIRED:
NO

NEW_AUTHORITY:
NO

NEW_OPERATION_IDENTITY:
NO

NEW_TRACE_STORE:
NO

NEW_DATABASE:
NO

NEW_REGISTRY:
NO

CHANGE3_PREREQUISITE:
NO

MATERIAL_FINDING_COUNT:
1

MATERIAL_FINDING:
NO_EXECUTABLE_PROGRESS_EVIDENCE_PERSISTENCE

MATERIAL_FINDING_DISPOSITION:
RESOLVED_BY_BOUNDED_LIFECYCLE_PERSISTENCE_TRANSPORT

BOUNDED_BINDING_CORRECTION_COUNT:
4
```

The architecture remains:

```text
SELECTED_TOPOLOGY:
ATTEMPT_ANCHORED_HYBRID_REFERENCE_TRACE

PRIMARY_OPERATION_IDENTITY:
AttemptRecordV1.attempt_id

TRACE:
DERIVED / NONAUTHORITATIVE

EXPECTED_ROUTE_OWNER:
PL07

CONTEXT_OBSERVATION_OWNER:
PL06

RESULT_EVIDENCE_OWNER:
PL08

LIVE_NEXT_ACTION_OWNER:
Project Spine / .planning/ACTIVE.md
```

# 3. Current real runtime authority

Supersede Amendment v1's historical lifecycle-closure binding with:

```text
GOVERNED_OPERATION_LIFECYCLE:
CLOSED / COMPLETE

LIFECYCLE_RECLOSURE_SHA256:
5899084FED87B160FC61FEB6789EE4B7231D208E1D60315B5B97F933FCBBCFED

CRITICAL_JOURNEY:
PL_SELF_HOSTED_GOVERNED_OPERATION

CRITICAL_JOURNEY_SMOKE:
PASS

OBSERVED_TRAVERSABILITY_STATE:
PASSING

FIRST_BROKEN_SEAM:
NONE

GAP_CLASS:
NONE
```

Accepted real path:

```text
AttemptRecordV1
-> supplied OperationGuidanceV1
-> Governed Operation Lifecycle
-> governed execution
-> validated persisted RunReceipt
-> exact receipt readback
-> ObservedResultV1
-> Attempt terminalization
-> PL08 TechnicalEvaluationV1
-> Project Spine post-evaluation checkpoint
-> authoritative .planning/ACTIVE.md readback
-> authoritative next gate / next permitted action
```

# 4. F01 PRE binding

Supersede all old F01 call-point assumptions referring to `command_resume` or
an absent generic PL08 runtime workflow.

Exact production call point:

```text
src/planning_lite/operation_lifecycle.py::execute_governed_operation
```

Exact timing:

```text
after:
authoritative Attempt lookup
-> admissibility
-> claim
-> supplied matched OperationGuidanceV1 validation

before:
invoke_governed_operation(...)
```

Exact live sources:

```text
attempt_id:
attempt.attempt_id
where attempt = claimed.attempt

operation_guidance_ref:
attempt.operation_guidance_ref

guidance:
selected_guidance
where selected_guidance is the already-supplied validated guidance mapping
```

No guidance reselection.

No route inference.

The existing F01 additive semantic field contract remains unchanged.

# 5. F02 receipt binding

Supersede old references to:

```text
scripts/capture_codex_run_receipts.py::capture()
planning_lite.telemetry.append_receipt()
```

as the production Change 2 call point.

Exact current call point:

```text
execute_governed_operation
after collect_governed_receipt(...) returns its exact persisted readback
and after the identity triangle passes
before ObservedResultV1 construction
```

Live sources:

```text
attempt_id:
attempt.attempt_id

receipt_id:
persisted["receipt_id"]

validated_receipt:
persisted

receipt path:
the exact receipt path supplied by the existing lifecycle receipt context
```

There is no independent receipt identity to invent.

Define the historical locator deterministically as:

```text
actual_executor_receipt_ref =
<existing lifecycle receipt path>#receipt_id=<persisted receipt_id>
```

The path component must be the exact existing lifecycle/telemetry receipt path
for this operation, normalized to the same repository-relative or target-relative
representation already used by that lifecycle context.

No search.

No newest receipt selection.

No ledger adjacency inference.

No matching by time/model/role/change/task.

`actual_executor_receipt_id` remains exactly:

```text
persisted["receipt_id"]
```

`actual_executor_planning_lite_ref` remains exactly:

```text
persisted["planning_lite_ref"]
```

# 6. F03 post-S6 authority binding

All Amendment v1 / Plan clauses that use:

```text
scripts/maintainer_resume.py::load_resume
docs/design/project-spine/CURRENT.md
```

as the POST F03 authority are superseded.

They are stale for this runtime seam.

The exact POST sequence is:

```text
evaluate_technical(...)
-> record_post_evaluation_checkpoint(...)
-> ProjectSpineSnapshotV1 authoritative readback
-> build_compact_status / authoritative resume projection
```

Change 2 must retain the exact returned
`ProjectSpineSnapshotV1` from:

```text
record_post_evaluation_checkpoint(...)
```

instead of discarding it.

This retention is observation only.

It does not change Project Spine authority.

F03 binds:

```text
attempt_id:
attempt.attempt_id

next_gate_ref:
post_spine_snapshot.next_permitted_action

next_gate_source_ref:
.planning/ACTIVE.md#Active change/Next permitted action

next_gate_source_sha256:
lowercase(post_spine_snapshot.active_sha256)
```

The existing persisted field name `next_gate_ref` is preserved for backward
compatibility, but its semantic source is explicitly the authoritative
post-operation `next_permitted_action`, matching the predecessor Plan's actual
historical value semantics.

The true owner gate remains separately available as:

```text
post_spine_snapshot.next_gate
```

but Change 2 does not need to create an additional persisted field for it.

Do not add a second gate authority.

Do not infer a gate from PL08 outcome.

Later mutation of ACTIVE cannot alter this historical F03 evidence because the
Attempt entry retains:

```text
next_gate_ref
next_gate_source_ref
next_gate_source_sha256
```

captured from the exact post-S6 readback.

# 7. DURING / PL06 observation

Preserve Amendment v1 semantics:

```text
PL06 remains the only owner of OperationDepthObservationV1.
```

Make the lifecycle integration explicit:

`execute_governed_operation` may accept one optional already-produced:

```text
OperationDepthObservationV1
```

for Change 2 observation only.

Requirements:

```text
operation_depth_observation.operation_ref == attempt.attempt_id
```

when a complete observation is supplied.

Lifecycle must not:

```text
build PL06 observation
reopen context
read arbitrary files for depth
infer host reads
derive expansion events
```

If no lawful observation is supplied:

```text
TRACE_COMPONENT:
DURING_UNAVAILABLE

TRACE_COMPLETENESS:
TRACE_PARTIAL
```

This is allowed.

Missing DURING observation does not block the governed operation.

No CLI change is required by Change 2.

A production caller that does not supply a PL06 observation produces an honest
partial trace rather than fabricated completeness.

# 8. Persistent owner

The persistent evidence owner remains:

```text
active Change progress.md
```

The template owner remains:

```text
template/.planning/changes/templates/progress.md
:: Governed Attempt / Evaluation evidence
```

`operation_trace.py` remains pure.

It performs:

```text
NO filesystem reads
NO filesystem writes
NO Git operations
NO route selection
NO lifecycle mutation
NO Project Spine mutation
NO telemetry append
NO raw-content retention
```

It constructs, validates, reads, and classifies only the derived trace mapping.

# 9. Runtime progress path

The lifecycle resolves the exact runtime progress owner from the already
authoritative active context path.

Rule:

```text
1. use target consumer root
2. read the same authoritative .planning/ACTIVE.md state
3. obtain Active context packet
4. require it resolves inside:
   .planning/changes/active/<active-change>/
5. require the path basename is context.md
6. replace only the final context.md component with progress.md
7. require the resulting progress.md parent directory matches Active change
```

No glob.

No recursive search.

No newest directory selection.

No fuzzy Change ID matching.

No heuristic fallback.

# 10. Missing progress.md

Lifecycle must NOT create an absent active `progress.md`.

The existing Change Scaffold already requires every active Change folder to
contain the complete Change scaffold including `progress.md`.

Therefore:

```text
RUNTIME_PROGRESS_MISSING:
INVALID_CHANGE_SCAFFOLD / TRACE_PERSISTENCE_UNAVAILABLE
```

Do not copy a template automatically from lifecycle execution.

Do not repair the Change scaffold.

Do not create a second progress location.

Scaffold repair remains owned by the existing Change Scaffold workflow.

A trace-persistence failure does not transfer semantic authority to Change 2.

# 11. Marker structure

Modify:

`template/.planning/changes/templates/progress.md`

inside the existing:

```text
## Governed Attempt / Evaluation evidence
```

section.

Add exactly one bounded container:

```text
<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->
<!-- PL_OPERATION_TRACE_ENTRIES_END -->
```

Each Attempt entry inside that container uses:

```text
<!-- PL_OPERATION_TRACE_ENTRY_BEGIN -->
- Attempt ref: `<attempt_id>`
... exact additive trace fields ...
<!-- PL_OPERATION_TRACE_ENTRY_END -->
```

The marker strings are structural delimiters only.

Attempt identity remains the exact `AttemptRecordV1.attempt_id` bullet field.

The writer must require:

```text
exactly one owner section
zero or one trace container
zero or one entry matching the exact Attempt ID
proper marker pairing
no nested entry markers
no duplicate Attempt entries
```

If the legacy owner section exists without the container markers, the first
Change 2 PRE write may insert the empty marker container at the deterministic
end of that owner section, immediately before the next level-2 heading or EOF,
without changing existing owner-section content.

This is an on-demand additive schema upgrade, not a bulk migration.

No existing historical progress file is rewritten proactively.

# 12. PRE persistence

PRE persistence occurs before real execution.

Sequence:

```text
resolve exact progress.md
-> read exact raw bytes
-> locate exact owner section
-> initialize marker container if legacy-but-valid section
-> locate zero or one exact Attempt entry
-> call pure record_governed_attempt_evidence(PRE)
-> serialize exact Attempt trace entry
-> preserve all unrelated bytes
-> atomic same-directory replace
-> reread exact file
-> verify exact Attempt PRE entry
-> retain raw SHA of persisted PRE file
```

F01 must therefore survive a later execution failure or interruption.

# 13. POST persistence

After:

```text
receipt persistence/readback
ObservedResult construction
Attempt terminalization
PL08 evaluation
Project Spine checkpoint
authoritative ProjectSpineSnapshotV1 readback
```

perform:

```text
reread exact progress.md
-> require current raw SHA equals the PRE readback SHA
-> locate exact same Attempt entry
-> call pure record_governed_attempt_evidence(POST)
-> add F02/F03 only
-> preserve F01 exactly
-> preserve unrelated bytes
-> atomic same-directory replace
-> reread exact Attempt entry
-> call read_operation_trace_evidence(...)
```

No automatic merge.

No retry.

No latest-wins behavior.

If progress changed between PRE and POST:

```text
TRACE_POST_PERSISTENCE:
FAIL_CLOSED / STALE_PROGRESS

MAIN_OPERATION_FACTS:
PRESERVED
```

Do not overwrite concurrent owner work.

Do not roll back:

```text
execution
receipt
Attempt terminalization
PL08
Project Spine checkpoint
```

# 14. Trace-local failure semantics

The compact semantic trace remains derived and non-authoritative.

Therefore a trace-construction or trace-persistence failure:

```text
MUST NOT:
change route
change execution authorization
select next gate
rewrite PL08 outcome
roll back execution
overwrite concurrent progress
```

Before execution, a malformed/missing progress owner means the trace cannot
persist F01.

The implementation must report the trace as unavailable/fail-closed and must
not fabricate a successful trace.

The governed operation remains governed by its existing lifecycle authority,
not by Change 2 trace completeness.

After execution, a stale/malformed progress owner similarly leaves the trace
`TRACE_PARTIAL` or `TRACE_UNAVAILABLE` according to the trusted evidence that
remains.

Change 2 measures and exposes incompleteness; it does not become a new
execution gate.

# 15. Atomic transport

The bounded lifecycle persistence helper may live privately inside:

`src/planning_lite/operation_lifecycle.py`

Its responsibility is transport only:

```text
resolve exact owner path
read exact bytes
verify marker structure
invoke pure operation_trace mapping function
replace bounded marker entry
atomic persist
exact readback
raw-SHA stale protection
```

Use same-directory temporary file plus atomic replacement.

Preserve:

```text
LF or CRLF convention
all bytes outside bounded insertion/replacement span
existing populated progress history
```

Clean temporary files on failure where possible.

No general Markdown parser is required.

# 16. Authority boundary

Materialize explicitly:

```text
operation_trace.py:
semantic constructor / validator / readback classifier

operation_lifecycle.py:
bounded transport coordinator only

progress.md:
persistent evidence owner

PL06:
context observation owner

PL07:
route owner

PL08:
result/evaluation owner

Project Spine:
next gate / next permitted action owner
```

Opening and atomically writing `progress.md` does not make lifecycle the
semantic evidence authority.

Lifecycle must not interpret trace fields beyond the exact pure contract.

# 17. Revised implementation write surface

The exact Change 2 implementation surface becomes five paths:

```text
ADD:
src/planning_lite/operation_trace.py
tests/test_operation_trace.py

MODIFY:
src/planning_lite/operation_lifecycle.py
tests/test_operation_lifecycle.py
template/.planning/changes/templates/progress.md
```

Exactly:

```text
FUTURE_IMPLEMENTATION_WRITE_PATH_COUNT:
5
```

No CLI change.

No context.py change.

No telemetry.py change.

No attempt_evaluation.py change.

No project_spine.py change.

No traversability.py change.

No Change 3 path.

# 18. operation_trace.py contracts preserved

Preserve the predecessor ADD symbols:

```text
OperationTraceError
OperationTraceEvidenceEntry
record_governed_attempt_evidence
write_expected_route_evidence
bind_attempt_run_receipt
write_historical_next_gate_evidence
OperationTraceView
read_operation_trace_evidence
```

Do not move filesystem persistence into this module.

Keep:

```text
TRACE_COMPLETE
TRACE_PARTIAL
TRACE_UNAVAILABLE
```

semantics.

Old trusted Attempt evidence lacking new fields remains readable as
`TRACE_PARTIAL`.

No backfill.

No heuristic fill.

# 19. Required focused tests

`tests/test_operation_trace.py` owns pure semantic contracts.

It must prove at minimum:

```text
F01 exact expected-route mapping
F01 wrong Attempt/guidance failure
F02 exact receipt binding
F02 wrong Attempt failure
F02 no heuristic receipt match
F03 exact ACTIVE historical binding
F03 later ACTIVE mutation does not alter persisted history
DURING exact operation_ref acceptance
missing DURING -> TRACE_PARTIAL
old entry -> TRACE_PARTIAL
malformed/conflicting identity -> fail closed
no raw content
no authority effect
no second operation identity
```

`tests/test_operation_lifecycle.py` owns integration/persistence proof.

It must prove at minimum:

```text
PRE trace persistence occurs after claim/guidance and before execution

F01 uses same Attempt and same selected guidance

F02 uses exact persisted receipt readback

F03 uses returned post-S6 ProjectSpineSnapshotV1

CURRENT.md is not consulted for F03

maintainer_resume.py is not consulted for F03

PRE progress survives later execution failure

POST enriches the same exact Attempt entry

PRE F01 remains byte-semantically unchanged by POST

progress path derives only from Active context packet

wrong active Change/path relationship fails trace persistence

missing progress.md is not auto-created

legacy valid owner section receives marker container on first PRE write

duplicate owner section fails closed

duplicate Attempt entry fails closed

malformed markers fail closed

concurrent progress mutation between PRE and POST fails stale check

no merge
no retry

LF preserved
CRLF preserved
unrelated progress bytes preserved

trace failure does not select route/gate or rewrite PL08/lifecycle authority
```

# 20. Walking skeletons

Walking Skeleton A:

```text
one Attempt
-> matched PL07 guidance
-> F01 PRE persisted
-> genuine no-expansion PL06 observation supplied with operation_ref == attempt_id
-> governed execution
-> exact F02 persisted receipt binding
-> PL08
-> S6 authoritative ACTIVE readback
-> exact F03 persisted historical next action
-> readback
-> TRACE_COMPLETE
```

Walking Skeleton B:

```text
B1:
F01
+ one genuine PL06 expansion
+ BLOCKED/result finding lineage
+ exact F02
+ deliberately missing F03
-> TRACE_PARTIAL

B2:
new Attempt
+ parent_attempt_ref / addresses_finding_refs as already owned by PL08
+ F01/F02/F03
-> separate trace identity by Attempt
```

No latest-wins behavior.

No cross-Attempt filling.

# 21. Template / compatibility

Template change is additive only.

Existing runtime progress files do not require bulk migration.

A legacy valid owner section can be marker-initialized on first eligible PRE
write.

Existing old evidence remains readable as partial.

No public schema change.

No RunReceipt schema change.

No CURRENT schema change.

No ACTIVE schema change.

# 22. Change boundaries

Preserve:

```text
CHANGE_2:
VALID / PAUSED_PENDING_FRESH_FORMAL_READINESS

IMPLEMENTATION_AUTHORIZED:
NO

CHANGE_3:
NOT_ABSORBED

MAJOR_PL09_NEXT_SLICE_GATE:
PRESERVED / UNCONSUMED
```

The lifecycle prerequisite is now:

```text
CLOSED / COMPLETE
```

# 23. Formal Readiness gate

This Amendment does not claim READY.

After materialization:

```text
NEXT_SINGLE_GATE:
FRESH_FORMAL_READINESS_CHANGE_2_AFTER_AMENDMENT_V2
```

Formal Readiness must specifically verify:

```text
five-path sufficiency
exact PRE/F02/F03 live bindings
progress path determinacy
marker update determinacy
legacy first-write marker insertion
atomic persistence
raw-SHA stale protection
trace-local nonauthority
post-S6 F03 authority
no Change 3 dependency
walking skeleton testability
```

# 24. Materialization writes

Allowed governance writes exactly:

```text
docs/design/project-spine/checkpoints/PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-IMPLEMENTATION-PLAN-AMENDMENT-v2.md
docs/design/project-spine/CURRENT.md
```

CURRENT receives only a bounded Change 2 projection:

```text
ACTIVE_CHANGE:
CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001

CHANGE_2:
VALID / PAUSED_PENDING_FRESH_FORMAL_READINESS

LIFECYCLE_PREREQUISITE:
CLOSED / COMPLETE

CRITICAL_JOURNEY:
PASSING

IMPLEMENTATION_AUTHORIZED:
NO

NEXT_PERMITTED_ACTION:
FRESH_FORMAL_READINESS_CHANGE_2_AFTER_AMENDMENT_V2
```

Do not clean unrelated CURRENT content.
