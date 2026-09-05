# PL-V39-06 — Authority and Scope Binding

- Status: `DRAFT / SHAPING EVIDENCE / NO IMPLEMENTATION AUTHORITY`
- Date: `2026-09-05`
- Slice: `PL-V39-06 — Context / Memory / Handoffs`
- Proposed Change: `CHG-PL-V39-06-CONTEXT-MEMORY-HANDOFF-001`
- Canonical repository: `D:\documents\planning-lite`
- Binding baseline: `7e8a3796b4722f98ab1dacb0a2bd67e168704b51`
- Implementation authorization: `NO`
- Plan / Formal Readiness: `NOT CREATED`
- Live Poker/mood mutation or migration: `NOT AUTHORIZED / NOT PERFORMED`

This bounded shaping artifact records authority, existing-memory inventory,
consumer requirements, and a minimal definition boundary. It does not approve
the proposed Change and does not select a physical storage layout.

## 1. Preflight and authority resolution

Read-only preflight at the shaping baseline:

```text
git rev-parse HEAD
7e8a3796b4722f98ab1dacb0a2bd67e168704b51

git status --short --untracked-files=all
(clean before this shaping block)

git diff --check
(PASS / no output)
```

The canonical `CURRENT.md` top contract records `active_change: NONE`,
`lifecycle_gate: DISCOVERY_READY`, `implementation_authorized: NO`, and
`next_permitted_action: OWNER_AUTHORIZATION_FOR_PL_V39_06`. The 05-C closure
records COMPLETE and the corrected candidate `b33e76249989a952eb0995ba7062a345d4ec2935`.
No authority drift was found in this bounded read.

| Input | Classification | Use in this binding |
|---|---|---|
| `docs/design/project-spine/CURRENT.md` | `CANONICAL_AUTHORITY` | Current lifecycle, resume pointer, and 05-C closure boundary |
| `docs/design/project-spine/roadmap/ROADMAP.md` | `CANONICAL_AUTHORITY` | PL-V39-06 direction, Project Spine/context semantics, and 06/07/08 sequencing |
| `PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-CHANGE-DEFINITION-v1.md` | `ACCEPTED_EVIDENCE` | Closed 05-C architecture and explicit exclusion of semantic memory/context |
| `PL-V39-05-C-COMPLETION-REVIEW-v1.md` | `ACCEPTED_EVIDENCE` | 05-C completion, live-consumer non-mutation, and final candidate identity |
| `PL-V39-05-C-EXECUTION-LEDGER-v1.md` | `ACCEPTED_EVIDENCE` | Task/gate evidence and bounded control-Git proof |
| Absorbed `REC-PL-MEMORY-EFFICIENCY.ru.md` | `DEFERRED_INPUT` | Requirements and future ideas; not implementation authority |
| Absorbed `REC-PL-CONTEXT-HANDOFF-001-v1.md` | `DEFERRED_INPUT` | Field observations and questions about bounded inherited context |
| `recommendations/FUTURE-RESERVE.md` | `DEFERRED_INPUT` | Deferred retrieval/compiler/learning boundaries |
| `recommendations/inbox/**` | `NONCANONICAL_OPERATIONAL_INPUT` | Local intake only; never auto-promoted to authority |
| `docs/design/project-spine/support/checkpoints/PL-V38-CURRENT.md` | `HISTORICAL_INPUT` | Prior compact-current and no-broad-history evidence |
| Live Poker `.planning` state | `ACCEPTED_EVIDENCE` | Mature-consumer continuation and history-cost requirements, read-only |
| Live mood `.planning` state | `ACCEPTED_EVIDENCE` | Early/unborn-consumer minimum bootstrap requirements, read-only |
| Scratch/tool traces and unreferenced prose | `HISTORICAL_INPUT` | Not loaded or promoted by this shaping block |

## 2. Existing memory-like surface inventory

Only existing surfaces that carry state, evidence, or continuation context are
listed. No new registry, memory store, snapshot tree, or parallel taxonomy is
proposed here.

| Surface | Current role | Authority / tracking | Producer → consumer | Retention | Problem / candidate PL-V39-06 role |
|---|---|---|---|---|---|
| `CURRENT.md` | Compact governed current pointer | Canonical, tracked | Lifecycle owners → fresh sessions | Durable, superseded in place | Must stay schema-bound; derive bounded resume context, do not turn into a memory database |
| Change Definition | Scope, invariants, authorization | Canonical when approved, tracked | Owner/planning → plan/readiness/execution | Durable through Change lifecycle | Source for accepted decisions and scope lineage |
| Implementation Plan | Sequencing, dependencies, write surfaces | Canonical when approved, tracked | Planning → execution gates | Durable evidence | Select task-relevant context; never copy whole plan into handoff |
| Execution Ledger | Accumulated task evidence | Canonical evidence, tracked | Execution → review/closure | Durable history | Query by task/gate; not default active context |
| Completion Review | Completion and closure evidence | Canonical evidence, tracked | T-09/owner → future resume/review | Durable archive | Compact outcome capsule and lineage pointer |
| Handoff/resume contract | Stage transition packet | Canonical only for fields owned by emitting boundary; tracked | Current stage → next stage/agent | Superseded per transition | Define minimal semantic/authorization handoff; no second source |
| Project registry (`projects.yml`) | Project locators/topology | Canonical operational locator, tracked/local by 05-C policy | Workspace → commands | Current topology | Never semantic memory or project history |
| `RunReceipt v1` | Externally supplied raw run fact | Canonical raw evidence for receipt fields, local/append-only | Operator/tool → audit | Append-only history | Keep raw and bounded; no inferred model/context claims |
| Recommendation inbox/archive | Intake and deferred proposals | Inbox noncanonical local; archive governed/deferred | Observation/operator → reconciliation | Retained with disposition | Review relevant residue manually; no automatic promotion |
| Project-owned `.planning` state | Consumer goals/current state/changes | Project authority, tracked or local by consumer policy | Consumer lifecycle → consumer sessions | Durable per project | Consume through router and bounded selection, not central duplication |
| Historical proposals/roadmaps | Prior direction and rationale | Historical/deferred, tracked | Past shaping → current reconciliation | Durable, visibility decays | Retrieve through lineage when relevant; never default-load whole history |
| Telemetry/review receipts | Operational or review proof | Raw/evidence-specific; not semantic memory | Commands/review → audit | Durable where canonical | Keep provenance and status, not interpreted memory |
| Derived resume context / bootstrap capsule | Small re-entry projection | Reconstructable/derived, not competing authority | Canonical state → next session/stage | Replaceable | Bounded selection with freshness and authoritative pointers |

## 3. Consumer requirements

### Poker (mature brownfield, read-only observation)

Generalizable requirements entering the Definition:

1. Continue from a small identity/state/gate packet without rereading the full
   history or reconstructing architecture.
2. Preserve accepted decisions, blockers, implementation identity, and exact
   next permitted action with lineage to canonical evidence.
3. Prevent stale historical proposals and rejected hypotheses from appearing as
   current authority; allow deliberate expansion through lineage.
4. Preserve expensive evidence and full history for on-demand review while
   keeping inherited context bounded and deterministic.

Consumer-specific details not generalized: Poker's scientific workload,
research package, particular CHG-0009 task graph, and its production baseline.

### Mood (early/unborn, read-only observation)

Generalizable requirements entering the Definition:

1. A fresh session must recover project identity, goal/current governed state,
   active or last Change, constraints, and next permitted action before history.
2. An unborn or dirty project must represent its actual Git state without
   inventing a baseline commit, readiness, or implementation authority.
3. The packet must remain useful when detailed history is absent; missing context
   defers safely and points to the owning artifact.
4. Early-project state must not be copied into a central second authority.

Consumer-specific details not generalized: Mood's historical news pipeline,
large local data/notebook inventory, and the current CHG-0001 hygiene boundary.

## 4. Conceptual boundaries

- **Memory**: retained, lineage-addressable decisions/evidence/context facts
  whose admission and supersession are governed. It is not a new database or
  generic knowledge base.
- **Context**: the bounded selection loaded for a task/session, derived from
  authority and relevance. Context is not automatically retained memory.
- **Current state**: the compact, schema-bound governed pointer in `CURRENT.md`
  and consumer equivalents. It owns current lifecycle facts; it is not a
  general history store.
- **Handoff**: a stage/agent transition contract carrying enough authoritative
  state to continue safely. It is not a duplicate ledger, plan, or raw log.

`Context Bootstrap Capsule` remains a tiny derived current-state re-entry view;
`AgentWorkPacket` remains task-specific derived/ephemeral context. A canonical
boundary capsule may own the exact facts emitted by its upstream authority.

## 5. Storage classes

| Class | Meaning | Examples |
|---|---|---|
| `TRACKED_CANONICAL` | Governing current/approved intent | `CURRENT.md`, approved Definition, approved Plan, consumer-owned current state |
| `TRACKED_EVIDENCE_HISTORY` | Durable inspectable proof and lineage | Ledger, Completion Review, accepted decisions, review receipts |
| `LOCAL_OPERATIONAL` | Useful intake/operational data without authority | `recommendations/inbox/**`, local raw operational receipts where policy says so |
| `RECONSTRUCTABLE` | Derived from canonical state and replaceable | Bootstrap capsule, resume projection, context selection trace |
| `EPHEMERAL` | Task-local scratch or transient packet | AgentWorkPacket scratch, temporary working snapshot, tool output |

Implementation must classify current state, active Change, implementation
identity, next action, accepted decisions, execution/consumer proof, raw
recommendations, temporary snapshots, agent handoff, historical proposals,
telemetry receipts, and derived resume context using these classes. Physical
directories and final control-home placement remain undecided here.

## 6. Minimal lifecycle proposal

```text
capture → classify → retain → select → handoff → supersede/archive
```

| Stage | Producer / authority | Invalidation / supersession | Reconstructability |
|---|---|---|---|
| capture | Owning lifecycle, operator, or evidence command | Reject missing provenance or out-of-scope input | Raw input remains inspectable when accepted |
| classify | Schema/authority owner | Reclassify only through governed disposition | Class is explicit, not inferred from recency |
| retain | Canonical/evidence owner | New approved revision supersedes prior current view; history is not deleted | Derived views can be regenerated |
| select | Stage router/consumer policy | Freshness, lineage, gate, and relevance invalidate selection | Deterministic selection order |
| handoff | Exiting stage/agent | Next stage accepts or marks stale/missing fields | Rebuild from canonical pointers plus evidence |
| supersede/archive | Lifecycle owner | Visibility decays; canonical truth is never erased for age | Archive remains discoverable by ID/lineage |

## 7. Resume context model

The bounded default model contains: project identity; current governed state;
active/last Change; relevant implementation identity; hard constraints and
authorization; blockers; recent accepted decisions; next permitted action;
authoritative artifact pointers; revision/freshness. Selection order is:

```text
authority/lineage → compact current state → stage artifacts → capsules
→ raw evidence only when needed → semantic retrieval only if lineage is insufficient
```

| Load class | Fields / sources |
|---|---|
| `ALWAYS_LOAD` | Project identity, current governed state, active/last Change, lifecycle gate, authorization, blockers, next permitted action, authoritative pointers, freshness |
| `LOAD_IF_RELEVANT` | Accepted decisions, implementation identity, stage Definition/Plan/Readiness, selected evidence/capsules, consumer-specific constraints |
| `DO_NOT_AUTOLOAD` | Full ledgers, raw logs, all historical proposals, rejected hypotheses, archive bodies, semantic/embedding search results without lineage need |

Missing or stale context must fail soft: retain the safe gate, identify the
missing owner/artifact, and do not invent a next action. A ContextTrace may
record what was loaded, why, authoritative path, and intentionally excluded
history; it is evidence of selection, not a new authority.

## 8. Handoff contract

Every bounded handoff should carry only:

```text
project/change identity
changed paths or state surface
current gate and status
verification performed and result
open blocker / material finding
accepted decisions or recommendations (with disposition)
next permitted action
artifact paths, revisions, and hashes where material
```

It must not copy the full Definition, Plan, ledger, raw logs, or scratch
narrative. The receiving stage resolves those by pointer and checks freshness,
authority, and authorization before acting.

## 9. PL-V39-06 / 07 / 08 boundary

| Slice | Responsibility |
|---|---|
| `PL-V39-06` | Persistent memory/context model, current/resume semantics, bounded selection, handoff contract, storage classes, retention/supersession, and only the minimum retrieval/resume seam needed to prove them |
| `PL-V39-07` | Execution contracts, skills/checklists, routing, and lifecycle refinements |
| `PL-V39-08` | Evaluation, learning, PromptOps, and quality loops |

Full recommendation discovery, automatic routing, orchestration, semantic
retrieval/embeddings, production Context Compiler, graph/RAG storage, and
operational control-repo placement remain deferred or out of scope. This slice
must grow the existing Project Spine muscle, not add a second leg.

## 10. Control-Git readiness and migration boundary

05-C already proved the control-Git mechanism, source rebind, local-only path,
Doctor, and split-control topology in disposable fixtures. Live Poker and mood
migration was not performed. Final `D:\documents` control-home placement is not
canonically decided. PL-V39-06 therefore requires no live control-Git migration;
it may consume the proven contracts as evidence only.

## 11. Risks, non-goals, and open decisions

Material risks are duplicate authorities, archive pile-up, `CURRENT.md`
expansion, stale handoffs, unbounded context, consumer coupling, hidden local
state being treated as authority, premature control-repo placement, and
recommendation scope expansion. Non-goals are skills/checklists/routing,
evaluation/PromptOps, multi-agent orchestration, full recommendation registry or
discovery, live consumer migration, a general KB/RAG, and new services/databases.

Open decisions for owner/Definition review: exact field names/encoding for a
minimal handoff and ContextTrace; the smallest implementation surface for
bounded selection; and the later owner of any persistent derived capsule. None
requires changing 05-C or making a physical storage decision in this shaping
block.

## 12. Definition input verdict

The bounded evidence supports a small, testable PL-V39-06 Definition with no
architecture expansion and no implementation dependency on live Poker or mood.
The companion Change Definition is a draft only. Owner review is required
before activation, Plan, Formal Readiness, or any implementation authority.
