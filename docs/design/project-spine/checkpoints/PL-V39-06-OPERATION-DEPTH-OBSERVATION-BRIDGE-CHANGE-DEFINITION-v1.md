# PL-V39-06 Operation-Depth Observation Bridge — Approved Definition v1

## 1. Change identity and approval

```text
Document ID: PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-001
Change ID: CHG-PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-001
Title: Operation-Depth Observation Bridge
Status: APPROVED_BY_OWNER
Owner: PL-V39-06 Context / Memory / Handoffs
Owner approval: USER / EXPLICIT / current conversation
Definition decision: APPROVE
Implementation authorization: NO
Source candidate: .local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_DEFINITION_CANDIDATE.md
Source candidate SHA256: B6E8E3FA5DA4E4131197241DBDED892F3D29AE1557C1D346D86E4D39B035598C
```

This approved Definition is the scope authority for the bounded Change. It is
not current-state authority, execution authorization, a route decision, or a
semantic-cycle contract. It does not consume or replace the outstanding
`OWNER_ADJUDICATION_PL_V39_09_NEXT_SLICE_AFTER_09-B_CLOSURE` gate.

## 2. Problem

PL06 already produces bounded, deterministic `ResumeContextV1` and
`ContextTraceV1` data for operation start. That output identifies selected
sources, exact revision/hash, role, reason, section, bounds, freshness, and
structural volume, but it has no operation-compatible observation seam for
explicitly observable context expansions after start. It cannot therefore
distinguish a no-expansion operation from one that needed bounded additional
context, or safely state when a later host/tool read was outside Planning
Lite's knowledge.

This is an observability gap, not permission to capture a transcript or infer
arbitrary reads.

## 3. Goal and bounded outcome

Expose a compact, deterministic, derived context-depth observation that a later
owner may attach to one semantic/work cycle. At operation start it references
the existing `ResumeContext` / `ContextTrace`; later it records only explicit
expansions that pass an approved Planning Lite seam. An unobservable read is
recorded as `UNAVAILABLE` with a reason rather than guessed.

The result is an in-memory/JSON-compatible projection or existing evidence
reference. It is not memory authority, lifecycle state, authorization, route
selection, a transcript, or a registry record.

## 4. Existing owners and contradiction resolution

| Owner | Reused responsibility | Boundary |
|---|---|---|
| PL06 `src/planning_lite/context.py` | Resume selection, source identity/hash, roles, sections, bounds, freshness, ContextTrace metrics | No persistent ContextTrace, memory store, or source-body copy |
| PL07 operation guidance | Operation identity, route/capability envelope, authority, result/STOP/next-gate references | Observation cannot select routes, authorize work, or redefine policy |
| PL08 attempt/evaluation | Existing Attempt/ObservedResult/fact/artifact references and later interpretation | No evaluation, verdict, telemetry-schema amendment, or promotion |
| PL09 future semantic trace | Later cycle linkage and semantic pre/during/post work | Full cycle schema and semantic fields remain later work |

The owner direction versus PL06's nonpersistent ContextTrace rule is
`RESOLVABLE`: use a derived projection and exact source references. Observation
metadata versus PL07 authority and PL08 evidence ownership is likewise
`RESOLVABLE`: the projection is non-authorizing facts only. The unfrozen PL09
semantic-cycle attachment is `MATERIAL_LATER`, so Change 1 does not freeze its
identity or fields. No `MATERIAL_NOW` contradiction was found.

## 5. In scope

- A start projection referencing the existing `ContextTraceV1` selection,
  source revision, and freshness.
- A bounded ordered sequence of explicit expansion projections for exact
  path/heading reads through an approved Planning Lite seam.
- Deterministic metadata: source identity/reference, SHA or exact revision,
  source role, storage class, reason family, section, already-available
  bounded volume, freshness, sequence, and completeness.
- A repeat/reopen indicator only when the same source identity/reference is
  observed again; no semantic similarity or inferred reopen.
- `UNAVAILABLE` plus reason when an expansion is outside the seam or otherwise
  unobservable.
- An opaque, source-bound operation linkage reference that carries no authority
  and does not freeze the future cycle schema.
- Diagnostic depth interpretation from existing roles and provenance. Labels
  such as `DEFAULT_RESUME_AUTHORITY`, `EXACT_BOUNDED_EXPANSION`,
  `CURRENT_EVIDENCE_DEEP_READ`, and
  `HISTORY_ARCHIVE_RECOMMENDATION_DEEP_READ` are not canonical product enums
  in this Change.

## 6. Exact missing seam

The smallest seam is an operation-scoped in-memory observation wrapper around
the existing start `ContextTraceV1` plus an explicit-expansion recording
operation. It accepts only normalized approved source references/metadata
already obtained by PL06 and reuses existing source, path, and freshness
guards. It does not observe or claim to observe arbitrary host file reads, tool
payloads, host-selected context, or semantic interpretation.

## 7. Candidate observation projection

This is a derived projection contract, not a durable registry schema:

```text
OperationDepthObservationV1
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
    source_ref {path/ref, sha256}
    role / storage_class
    reason_family
    section | null
    source_revision / freshness
    bounded_volume | null
    repeated_or_reopened: YES | NO | UNAVAILABLE
    completeness: COMPLETE | PARTIAL | UNAVAILABLE
  overall_completeness: COMPLETE | PARTIAL | UNAVAILABLE
  unavailable_reasons[]
```

The field set remains minimal and is versioned only if the owning PL06
contract requires it. `operation_ref` cannot authorize work, identify a route,
or freeze Change 2. Source bodies, prompts, responses, hidden reasoning, and
tool payload bodies never appear.

## 8. Minimum implementation surface (for a later approved Plan)

No implementation is authorized by this Definition. If later authorized, the
minimum expected surface is:

```text
src/planning_lite/context.py
tests/test_context_resume.py
tests/test_context_depth_observation.py  # only if existing tests cannot express the invariant
```

No `template/`, telemetry/RunReceipt, routing policy, adapter, roadmap,
recommendation, ledger, registry, database, host-monitor, consumer, or
CURRENT surface is implementation scope. Any additional tracked path requires
an explicit Plan-level finding that the canonical lifecycle requires it.

## 9. Acceptance criteria

1. A clean operation-start fixture produces a deterministic observation whose
   start projection exactly matches existing ContextTrace identities, hashes,
   roles, reasons, sections, counts, characters, and bounds.
2. A permitted exact path/heading expansion produces one ordered event with
   normalized identity, exact revision/hash, role, reason family, section,
   bounded volume, and complete status; no body text is present.
3. Re-observing the same exact source identity produces a deterministic
   repeat/reopen signal; a different or merely similar source never does.
4. A read not delivered through the approved seam produces `UNAVAILABLE` with
   a reason; arbitrary host/tool reads are never inferred.
5. Missing, stale, superseded, hash-mismatched, outside-root, symlinked,
   globbed, `.git`, or forbidden sources fail closed or become `UNAVAILABLE`
   under existing PL06 freshness/path semantics.
6. Existing exact-selector bounds remain in force: no glob/semantic search and
   no recursive history/archive/recommendation scan or unbounded event stream.
7. The result is derived/disposable unless a later existing owner explicitly
   references it through an approved evidence carrier; no registry, database,
   file-per-turn log, memory directory, or second authority is created.
8. The projection carries no route authorization, expected-route binding,
   token/cache delta, prompt-dedup decision, skill log, semantic digest, or
   AgentWorkPacket/Context Compiler production field.
9. A real walking-skeleton run proves start-only, explicit-expansion,
   repeat/reopen, and unobservable-read cases without writing product/tracked
   state.

## 10. Walking-skeleton proof

In a disposable clean product fixture, use the production-equivalent
`planning-lite resume ... --json` path to: capture the default start
projection; request one permitted exact path/heading; request that source again;
attempt a bypassed expansion and verify `UNAVAILABLE`; then read back the
derived output and compare hashes/bounds. Verify no source body, transcript,
registry, or tracked file was written. This is acceptance evidence, not a new
lifecycle stage or gate, and source-identity evidence must run from a clean
committed central source.

## 11. Nearest-wrong and fail-closed cases

- Arbitrary host/tool read presented as an expansion: reject or `UNAVAILABLE`.
- Outside-root, parent traversal, glob/pattern, symlink/reparse, `.git`,
  forbidden inbox/history source: existing PL06 guard rejects it.
- Changed source hash/revision: `STALE`/`SUPERSEDED` or `UNAVAILABLE`; current
  authority remains authoritative.
- Duplicate/non-monotonic sequence or reopen without identical source
  identity: invalid observation; do not manufacture depth.
- Full source body, prompt, response, tool payload, hidden reasoning, or host
  transcript supplied: reject and do not retain.
- Route, token, dedup, semantic-cycle, or AgentWorkPacket fields supplied:
  scope violation and STOP.
- Missing/invalid start ContextTrace: no fabricated baseline; `UNAVAILABLE`.

## 12. Explicit non-goals

This Change does not implement semantic pre/during/post trace, input/output
semantic digests, expected-route binding, token/cache delta telemetry, runtime
prompt dedup, skill logging, dashboards, AgentWorkPacket production schema,
Context Compiler production path, semantic retrieval/embeddings/RAG,
host-monitoring, transcript retention, or any lifecycle/gate change. It does
not repair PL-V39-09/09-B, alter RunReceipt v1, promote recommendations, or
make statistics claims.

## 13. Dependency on later Change 2

Change 2 may attach this compact observation to a semantic/work cycle and add
semantic pre/during/post fields, input/output digests, expected-route binding,
or result interpretation under its own Definition and owner gate. Cycle
identity, fields, and attachment/persistence policy are intentionally not
frozen here. Change 1 remains independently useful if Change 2 is deferred or
rejected.

## 14. Gates and STOP conditions

This Change uses the existing sequence: Definition approval/activation →
Implementation Plan → readiness/implementation authorization → focused
execution/review → acceptance/commit/verification → closure. No new human gate
is introduced. The semantic checkpoints are derived and nonauthoritative.

STOP if implementation requires a persistent registry or second authority,
arbitrary host-read capture, raw-body copying, a host service, a full semantic
cycle schema, PL07/PL08/PL09 ownership transfer, a RunReceipt schema change, a
new lifecycle stage/gate, unbounded scanning, or token/prompt-dedup/route
semantics. A material contradiction affecting scope, safety, authority, or
completion fails closed.

## 15. Completion evidence

Later completion requires focused deterministic tests, walking-skeleton and
nearest-wrong evidence, exact output readback with hashes/revisions/bounds,
Git/write-boundary and privacy audits, confirmation of PL07/PL08/PL09 boundary
preservation, and the existing readiness, acceptance, commit, and post-commit
checks. This Definition makes no completion claim.

## 16. Retention invariants

```text
RAW_TRANSCRIPT_COPY_INTO_PLANNING_LITE: FORBIDDEN
RAW_PROMPT_STORAGE: FORBIDDEN
RAW_RESPONSE_STORAGE: FORBIDDEN
SOURCE_BODY_COPY_FOR_OBSERVABILITY: FORBIDDEN
HOST_RAW_TRANSCRIPT: EXTERNAL / OPTIONAL / RETENTION_DEPENDENT / NONAUTHORITY
PLANNING_LITE_OPERATION_MEMORY: COMPACT_DERIVED_METADATA_AND_SOURCE_REFS_ONLY
```

## 17. Next permitted action

```text
PREPARE_PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_PLAN
implementation_authorized: NO
```
