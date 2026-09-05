# CHG-PL-V39-06-CONTEXT-MEMORY-HANDOFF-001 — Change Definition

- Status: `APPROVED / CENTRAL DEFINITION / NO IMPLEMENTATION AUTHORITY`
- Date: `2026-09-05`
- Roadmap source: `PL-V39-06 — Context, Memory, Visibility, and Handoffs`
- Slice: `PL-V39-06 — Context / Memory / Handoffs`
- Definition baseline: `7e8a3796b4722f98ab1dacb0a2bd67e168704b51`
- Canonical repository: `D:\documents\planning-lite`
- Implementation authorization: `NO`
- Activation: `PENDING IN THIS GOVERNANCE STEP`
- Plan / Formal Readiness: `NOT CREATED`
- Live Poker/mood migration: `NO`

## 1. Authority and purpose

This Definition is bounded by the canonical Project Spine Roadmap and `CURRENT.md`,
the closed 05-C Definition/Completion Review/Execution Ledger, and the
companion `PL-V39-06-AUTHORITY-AND-SCOPE-BINDING-v1.md`. The 05-C foundation is
accepted evidence, not a reason to reopen its architecture. Deferred memory and
context recommendations are requirements input only; inbox material remains
noncanonical operational intake.

The Definition freezes a problem, goal, scope, invariants, acceptance boundary,
and authorization boundary. Owner approval is recorded below; activation is the
separate lifecycle transition performed by this governance step. It does not
create a Plan, run Readiness, or authorize implementation.

Owner decision recorded by this governance step:

```text
OWNER_DEFINITION_DECISION: APPROVE
approved scope: unchanged
acceptance criteria: 9 (unchanged)
implementation authorization: NO
```

## 2. Problem

Planning Lite now has compact current pointers, Change/evidence lifecycle
records, project-local state, raw receipts, and bounded handoff observations,
but it lacks one explicit, reusable rule for deciding what durable context a
fresh stage/session should inherit. Without that rule, a mature consumer can
pay repeated rediscovery cost while an early consumer can inherit too much,
too little, or stale history. A new memory authority would create a worse
boundary problem, so the Change must govern existing surfaces and derived views.

## 3. Goal

Define and later prove a minimal memory/context/handoff model that:

- keeps `CURRENT.md` compact and schema-bound;
- distinguishes retained memory, bounded context, current state, and handoff;
- classifies existing surfaces into explicit storage classes;
- selects deterministic, authority-first resume context without full-history
  loading;
- carries semantic and authorization facts across a stage/agent boundary;
- detects stale or superseded context and defers safely when required facts are
  missing; and
- remains reusable for both mature brownfield and early/unborn consumers.

## 4. Bound architecture and semantics

### 4.1 No second memory authority

Reuse Project Spine, `CURRENT.md`, existing Change/evidence lifecycle, consumer
`.planning` state, and the already proven 05-C registry/receipt/control seams.
No general database, graph, embedding-first store, `.memory/` tree,
`_snapshots/` tree, or parallel resume taxonomy is introduced by this Change.
`Context Bootstrap Capsule`, `ContextTrace`, and `AgentWorkPacket` are logical
or derived views/packets. PL-V39-06 does not require a persistent directory,
registry, database, or new storage authority for any of them. They may be
reconstructed from authoritative sources unless a later approved lifecycle
boundary explicitly requires durable evidence. No `.memory/`, `.context/`,
`.snapshots/`, or new registry/database is authorized.

### 4.2 Four explicit concepts

- **Memory** is admitted, retained, lineage-addressable information.
- **Context** is a bounded selection for the current task/session.
- **Current state** is the compact governed pointer owned by `CURRENT.md` or a
  consumer's canonical equivalent.
- **Handoff** is a minimal stage/agent continuation contract resolved through
  authoritative pointers.

The Context Bootstrap Capsule remains derived and small; `ContextTrace` records
why a bounded selection was made; an `AgentWorkPacket` is task-specific and
ephemeral/derived. None replaces canonical state or becomes a storage system.

### 4.3 Storage classes and lifecycle

Use the five classes `TRACKED_CANONICAL`, `TRACKED_EVIDENCE_HISTORY`,
`LOCAL_OPERATIONAL`, `RECONSTRUCTABLE`, and `EPHEMERAL`. Admission follows:

```text
capture → classify → retain → select → handoff → supersede/archive
```

Supersession changes visibility and lineage; it does not delete canonical truth
because an item is old. Derived context is replaceable and must identify its
source revision/freshness.

### 4.4 Resume selection

The default resume packet includes project identity, current governed state,
active/last Change, relevant implementation identity, constraints,
authorization, blockers, recent accepted decisions, next permitted action,
authoritative pointers, and freshness. `ALWAYS_LOAD` is limited to the compact
identity/gate/action facts; stage artifacts and accepted decisions are
`LOAD_IF_RELEVANT`; full ledgers, raw logs, rejected history, and archive bodies
are `DO_NOT_AUTOLOAD`. Selection is authority/lineage-first and deterministic.
In this Change, relevance expansion means bounded authority/lineage-based
artifact selection only. Semantic retrieval, embeddings, vector search, RAG,
and embedding-first context selection are not required for acceptance and
remain deferred.

When context is missing or stale, the safe gate remains in force and the owner
artifact is pointed to; no inferred action or authority is created.

### 4.5 Handoff

A handoff records identity, changed state/paths, current gate/status,
verification, blockers/findings, accepted dispositions, next permitted action,
and material artifact/revision/hash pointers. It deliberately does not copy a
full Definition, Plan, ledger, raw log, or scratch narrative. A handoff is not a
current-state authority. It is a `RECONSTRUCTABLE` transition packet or, only
where an existing lifecycle explicitly requires durable evidence,
`TRACKED_EVIDENCE_HISTORY`; it is never a parallel `CURRENT`, parallel project
state, or second memory authority. The receiving stage/agent must resolve
authoritative pointers and freshness before acting.

### 4.6 Explicit boundary confirmation

`CURRENT.md` remains compact and schema-bound. Derived packets do not become
authority. Full recommendation discovery is out of scope. Semantic retrieval,
embeddings, vector search, RAG, and embedding-first context selection are out
of scope and deferred. Live Poker/mood migration is out of scope. Skills,
checklists, and routing belong to PL-V39-07; evaluation, learning, and PromptOps
belong to PL-V39-08.

## 5. In scope

- explicit semantics for memory, context, current state, and handoff;
- storage-class and retention/supersession rules for existing surfaces;
- bounded authority-first resume/context selection;
- minimal handoff and freshness/staleness contract;
- derived Context Bootstrap Capsule and ContextTrace semantics only where
  needed to make selection explainable;
- focused proof seams for fresh/post-compaction resumes, mature Poker and early
  mood-style consumers, missing/stale context, and no duplicate authority;
- manual routing of relevant recommendation residue without automatic
  promotion; and
- documentation/evidence sufficient for a later bounded Plan and Readiness.

## 6. Explicitly out of scope

- implementation before separate owner authorization;
- live Poker or mood migration, control-Git placement, or control-repository
  mutation;
- changes to product/runtime/template/test files in this definition turn;
- a new memory service/database, graph, embeddings, RAG, or general knowledge
  base;
- broad recommendation discovery, automatic promotion, or a recommendation
  registry;
- skills, checklists, routing, orchestration, or multi-agent scheduling;
- evaluation, learning, PromptOps, or quality loops (PL-V39-08);
- execution-contract/lifecycle refinements owned by PL-V39-07;
- expansion of `CURRENT.md` into general history;
- automatic archive deletion, hidden local authority, or inferred runtime facts;
- Roadmap redesign, release, commit, tag, push, merge, rebase, or reset.

## 7. Frozen invariants

1. Canonical Project Spine and consumer-owned state remain the authority for
   facts they own; derived context never outranks them.
2. `CURRENT.md` stays compact, schema-bound, and current-state oriented.
3. Durable evidence remains inspectable and is retrieved by lineage, not copied
   wholesale into active context.
4. Raw recommendations and raw receipts do not become semantic memory without
   an explicit governed disposition.
5. Stale/missing context fails safe and cannot invent authorization, blockers,
   or next actions.
6. Selection is bounded, deterministic, and explainable through authoritative
   pointers and optional ContextTrace.
7. 05-C's product/control Git separation and no-live-migration boundary remain
   unchanged; its proven mechanism is evidence, not a migration mandate.
8. No Change, Plan, Readiness, or implementation authority is implied by this
   draft.

## 8. Acceptance criteria

The future approved implementation must prove at least these small criteria:

| ID | Criterion |
|---|---|
| AC-01 | A fresh session resumes with project identity, governed current state, active Change if one exists (otherwise the last completed / next authorized lifecycle pointer), lifecycle gate, authorization, open blocker if one exists, and next permitted action without loading full history or inventing a Change or blocker. |
| AC-02 | Resume selection has one deterministic authority/lineage-first order and records source revision/freshness. |
| AC-03 | `CURRENT.md` remains compact and no second current/memory authority is created. |
| AC-04 | A stale or superseded context/handoff is detected and safely defers to its owner artifact. |
| AC-05 | A handoff preserves changed state, verification, gate, blocker/findings, disposition, next action, and material identity pointers without duplicating ledger/plan/raw logs. |
| AC-06 | Existing surfaces are classified into the five storage classes; raw inbox material is not auto-canonical. |
| AC-07 | A mature brownfield continuation (Poker-shaped) and an early/unborn continuation (mood-shaped) both recover the minimum bounded packet while preserving their actual Git/baseline state. |
| AC-08 | Context selection is bounded and explainable; full history is loaded only by explicit bounded authority/lineage-based artifact expansion. Semantic retrieval, embeddings, vector search, RAG, and embedding-first selection are not required and remain deferred. |
| AC-09 | No live consumer migration or control-Git placement is required for acceptance; the 05-C disposable mechanism remains unchanged. |

## 9. Verification and evidence seams

The later Plan should use existing owner/product tests and focused discriminators
for: current/resume schema; authority precedence; stale/superseded pointers;
handoff omission/duplication; bounded selection and ContextTrace; raw-intake
non-promotion; and mature/early consumer fixtures. It should verify Git/write
boundaries and derived/reconstructable behavior without broad architecture
rediscovery. Full regression is a gate decision, not a definition requirement.

## 10. Dependencies and risks

Dependencies are the canonical Project Spine/current-state schemas, existing
Change/evidence lifecycle, consumer routers, and the 05-C accepted topology and
receipt contracts. Deferred production Context Compiler, semantic retrieval,
learning/utility ledgers, automatic routing, and recommendation absorption are
future dependencies only and must not be smuggled into this Change.

Key risks are duplicate authority, stale handoff contamination, unbounded
context, archive accumulation, current-state expansion, hidden local state,
consumer-specific coupling, and premature physical storage decisions. These are
acceptance/test concerns, not permission to widen scope.

## 11. Authorization and next gate

```text
Change Definition: APPROVED BY OWNER
owner approval: APPROVE (this governance step)
activation: PENDING / canonical activation receipt
Implementation Plan: NOT CREATED
Formal Readiness: NOT RUN
implementation_authorized: NO
live Poker/mood: UNCHANGED
next permitted action: PREPARE PL-V39_06_IMPLEMENTATION_PLAN (after activation)
```

The recorded approval preserves the stated scope, dependencies, 9 acceptance
criteria, 06/07/08 boundary, Central Project Spine authority, no second memory
authority, no new persistent memory store, and no-live-migration constraint.
No implementation begins from this document.
