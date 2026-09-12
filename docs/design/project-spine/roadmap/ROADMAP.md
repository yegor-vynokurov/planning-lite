# Planning Lite Roadmap v3.9.3 — Integrated Design Baseline
## Project Spine, Target Reality, Context, Execution Contracts, Evaluation, and Governed Orchestration

**Status:** `CURRENT DESIGN BASELINE / DOCUMENTATION-ARCHITECTURE RECONCILED / NO PRODUCT EXECUTION AUTHORITY`
**Date:** `2026-08-21`
**Stable path:** `docs/design/project-spine/roadmap/ROADMAP.md`
**Product release baseline remains separate:** Planning Lite `v4.3.0` lineage
**Current operational checkpoint:** `docs/design/project-spine/PL-V38-CURRENT.md` dated 2026-08-20

This baseline is intentionally self-hosted: Planning Lite is using its own recommendation-reconciliation semantics to absorb unanchored recommendations into a new coherent roadmap.

---

# 0. What this baseline is trying to achieve

The goal is **not** to preserve every recommendation as a visible roadmap branch.

The goal is:

```text
many useful observations
        ↓
semantic reconciliation
        ↓
few coherent capabilities
        ↓
one executable roadmap
```

A bad result would look like:

```text
Project Spine
├── memory recommendation
├── eval recommendation
├── lecture recommendation
├── weak-model recommendation
├── target-skeleton recommendation
├── another eval recommendation
├── another context recommendation
└── ...
```

A good result should look like one living system whose existing organs became more complete.

This baseline therefore applies a strict **anti-hair rule**:

> A recommendation gets a new Roadmap vertebra only if it introduces a genuinely new dependency boundary, owner, and evidence-bearing exit gate.

Otherwise it must:
- strengthen an existing Roadmap block;
- become a cross-cutting invariant/checklist;
- remain a future seed;
- or be rejected/superseded.

---

# 1. Source-of-truth and lineage

## 1.1 Current baseline and compatibility source

This v3.9.3 document is the current **development design roadmap** in this
reorganized source package.

It does not by itself:
- release Planning Lite product behavior;
- authorize implementation;
- replace the operational field checkpoint;
- claim that the current Poker field gate has completed.

The last previously canonical implementation-facing roadmap is archived at:

```text
docs/design/project-spine/roadmap/archive/PLANNING-LITE-ROADMAP-v3.8.7.ru.md
```

That baseline established/completed:

```text
PL-V38-00  central reconciliation
PL-V38-01  Direction foundation
PL-V38-02  Current Capability Assessment + causal Gap Map
PL-V38-03  Recommendation semantic residue + historical reconciliation
PL-V38-04  Roadmap synthesis + prioritization + Change handoff
PL-V38-PREP-01 local-only update safety
```

The operational field gate remains separately controlled by
`PL-V38-CURRENT.md`.

## 1.2 v3.7 is not discarded history

`PLAN-PL-LEARNING-CONTEXT-ROADMAP-v3.7.ru.md` contains mature branches that v3.8.7 narrowed out of its immediate Project Spine sequence, including:

- Skill Engineering;
- Checklist Control Layer;
- Reusable Prompt/Eval Core;
- fixture qualification;
- semantic/procedural memory;
- learning candidates;
- controlled scaffold evolution;
- rule/checklist evolution.

These are not reintroduced as duplicate roadmaps. Their useful semantics are absorbed into the integrated future sequence below.

## 1.3 Recommendation sources absorbed by this baseline

Primary recommendation families:

```text
REC-PL-DIRECTION-001-v2
REC-PL-DIRECTION-002-v1
REC-PL-READINESS-001-v1
REC-PL-CONTEXT-HANDOFF-001-v1
REC-PL-MATERIALITY-SIMPLICITY-001-v1
REC-PL-CHANGE-COST-001-v1
REC-PL-WEAK-MODEL-EXECUTION-001-v3
REC-PL-EXECUTABLE-TARGET-CONTRACT-001-v1
REC-PL-LEARNING-LOOP
REC-PL-MEMORY-EFFICIENCY
REC-PL-CONTROLLED-EVOLUTION
REC-PL-RULE-PLAYBOOK-CURATION
ROADMAP-NOTE-CODE-ASSET-CHECK
```

Supporting research/code assets are references, not roadmap items.

---


## 1.4 Source archive after absorption

The active Roadmap no longer depends on a forest of recommendation documents
being loaded together.

Source recommendations used in this reconciliation are preserved under:

```text
docs/design/project-spine/recommendations/archive/absorbed/
docs/design/project-spine/recommendations/archive/superseded/
```

Deferred semantic residue is preserved in one active carrier:

```text
docs/design/project-spine/recommendations/FUTURE-RESERVE.md
```

New untriaged recommendations go to:

```text
docs/design/project-spine/recommendations/inbox/
```

Observations/facts that do not yet propose action go to:

```text
docs/design/project-spine/discoveries/
```

The local `.planning-lab/` remains a non-canonical research/lab source and is
not the place to discover the current Planning Lite development Roadmap.

The full source/disposition ledger is preserved in:

```text
docs/design/project-spine/recommendations/archive/ABSORPTION-2026-08-21.md
```

### 1.5 Superseded-lineage residue audit

A newly recovered predecessor was reviewed separately:

```text
REC-PL-DIRECTION-001 — Project Spine, Direction Memory and Recommendation Lifecycle
```

It is explicitly superseded by `REC-PL-DIRECTION-001-v2`, so it does not become
another active recommendation source.

However:

```text
SUPERSEDED
!=
SEMANTICALLY EXHAUSTED
```

Before archival, predecessor-only RecommendationUnits must be checked against:
- the successor recommendation;
- the current Roadmap;
- the Future Recommendations carrier.

This pass recovered several useful predecessor-only units into existing owners
without adding a new Roadmap vertebra.

## 1.6 Development information architecture

For Planning Lite's own development/design work, use stable semantic locations:

```text
docs/design/project-spine/
├── CURRENT.md
├── roadmap/
│   ├── ROADMAP.md
│   └── archive/
├── recommendations/
│   ├── inbox/
│   ├── active/
│   ├── FUTURE-RESERVE.md
│   └── archive/
├── discoveries/
│   ├── INDEX.md
│   ├── items/
│   └── archive/
├── governance/
│   └── RECOMMENDATION-ABSORPTION.md
└── support/
    ├── code-seeds/
    ├── playbooks/
    ├── field-evidence/
    ├── reviews/
    ├── research/
    └── checkpoints/
```

Authority rule:

```text
roadmap/ROADMAP.md
= current development direction

recommendations/FUTURE-RESERVE.md
= deferred semantic residue + dormant contingency routes
!= second roadmap

recommendations/inbox/
= untriaged proposed actions

discoveries/
= observations/facts; no implementation implication

support/
= evidence and reusable assets; not direction authority
```

Old versioned design files belong in archive/support, not at the discovery root.

# 2. Recommendation Absorption governance

The detailed reusable process now lives at the stable path:

```text
docs/design/project-spine/governance/RECOMMENDATION-ABSORPTION.md
```

This Roadmap relies on the following invariants only:

```text
unit-first, not document-first
Discovery != Recommendation
placement determinacy
anti-hair
no silent residue
supersede-residue check
one active Roadmap
one Future Reserve
contingency route != second Roadmap
```

A recommendation receives a new Roadmap vertebra only when it introduces a
genuinely new dependency boundary, owner, and evidence-bearing exit gate.

Otherwise it:
- enriches an existing Roadmap block;
- becomes cross-cutting governance/checklist semantics;
- becomes Future Reserve residue;
- remains unanchored;
- or is rejected/superseded.

# 3. Integrated product model

Planning Lite now has one canonical **Project Spine**, surrounded by four supporting systems.

```text
                         TARGET / VALUE
                              │
                              ▼
                       PROJECT SPINE
          Target → Capability → Gap → Roadmap → Change
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
  CONTEXT / MEMORY      EXECUTION CONTROL      EVALUATION / LEARNING
        │                     │                     │
        └───────────────┬─────┴───────────────┬─────┘
                        ▼                     ▼
                TARGET REALITY          CONTROLLED EVOLUTION
```

The roadmap should develop these as one system, not as separate recommendation families.

---

# 4. Cross-cutting invariants

These do not get standalone roadmap stages.

## 4.1 Authority-first

Current facts are validated through their authoritative owner.

Examples:

```text
Git
→ branch/HEAD/tracked state

ACTIVE
→ lifecycle/gate/authorization

Project Spine artifacts
→ target/gap/roadmap semantics

receipts/manifests
→ machine-critical current assertions
```

Historical tokens are not current truth.

## 4.2 Human authority at semantic gates

Never automate away:

```text
Target acceptance
Roadmap acceptance
material semantic adjudication
plan approval
execution authorization
closure/promotion authorization
destructive decisions
```

Interaction style may vary, authority does not.

## 4.3 Materiality and Simplicity

For proposed machinery:

```text
CURRENT evidence?
simplest sufficient shape?
deferable?
can invalid state be removed instead of guarded?
```

No speculative infrastructure merely because it is imaginable.

## 4.4 Four-layer Contract Closure

Contract-heavy work closes, where applicable:

```text
SHAPE
SEMANTICS
ENCODING
OWNERSHIP
```

Readiness must test determinacy.
Execution must not invent missing material semantics.

## 4.5 No fake precision

Use evidence-derived Change Cost profiles and qualitative value/risk comparisons.

Do not collapse uncertain prioritization into arbitrary `1–10` LLM scores.

## 4.6 Reusable asset check before invention

Before non-trivial new:
- mechanism;
- prompt;
- checklist;
- evaluator;
- harness;
- scaffold;

check:

```text
code companion
planning-lite-lab
planning_lite_tools
qualified templates/archetypes
existing workflow/checklist assets
```

Classify:

```text
REUSE
ADAPT
REFERENCE_ONLY
NO_MATCH
```

Do not copy merely because an asset exists.

## 4.7 Small changes stay small

Routine bugfix/docs/local edits must not require:
- full Project Spine bootstrap;
- Outcome Ladder;
- Target Skeleton;
- multi-perspective strategy analysis;
- independent agent team;
- full behavioral campaign.

Depth is routed by material change facts.


## 4.8 Project Spine consistency precedes Gap derivation

For material direction work:

```text
direction authority discovery
+
current lifecycle/state evidence
+
repository/current assertions
→ CURRENT-STATE CONSISTENCY GATE
```

Only then derive `Current ↔ Target → Gap`.

A clean repository proves only repository cleanliness.
It does not prove planning/lifecycle consistency.

When inconsistency is found:

```text
bounded factual reconciliation
→ resume the original direction question
```

Do not silently reprioritize the Roadmap during the detour.

## 4.9 Control-artifact ownership is explicit

Planning Lite should not allow the same reusable rule to drift between several
control surfaces merely because all placements look plausible.

Default ownership:

| Surface | Owns |
|---|---|
| root / mode router | activation and high-level routing only |
| workflow playbook / `control/*.md` | lifecycle sequence, authority gates, stop/resume semantics |
| skill | reusable capability procedure and conditional reference routing |
| checklist | reusable verification/quality obligations and evidence requirements |
| task acceptance criteria | Change-specific required outcome |
| System Claim / Target Scenario | project-level observable target behavior |
| EvalCase | executable, versioned evidence instance used to test an artifact/claim |
| Project Spine | accepted current direction truth |
| Survey / archaeology capsule | current-state evidence, never competing direction authority |
| Context Bootstrap Capsule | tiny derived current-state re-entry surface |
| AgentWorkPacket | task-specific ephemeral/derived context packet |

A rule may project into more than one surface only when one is explicitly
canonical and the others are derived projections.

Preferred mutable order remains:

```text
checklist
→ conditional reference
→ workflow/rule/playbook
→ skill body
→ root/control prompt only when necessary
```

---


## 4.10 Evidence-efficient verification

Verification should use the smallest sufficient evidence set for the actual
novelty and blast radius.

Preferred evidence stack:

```text
existing owner/product tests
→ one focused acceptance probe for genuinely new behavior
→ Git/write-boundary verification
→ broader/full suite at meaningful integration, completion, or release gates
```

Do not improve confidence by mechanically multiplying bespoke assertions.

In particular:

- direct repository state outranks presentation/rendering text when both express the same fact;
- CLI help prose, pytest failure formatting, and human-oriented diagnostics are not APIs unless explicitly contracted as such;
- an invariant already owned by an existing product test should normally be reused, not reimplemented in orchestration code;
- a failed custom verifier is first classified as `PRODUCT_DEFECT` or `VERIFIER_DEFECT`;
- consumer/update verification that depends on source revision identity runs from a clean committed source;
- verification depth scales with semantic materiality and blast radius, not with the number of available tests.

This is a cross-cutting evidence discipline, not a new workflow stage or testing subsystem.

# 5. Current completed foundation

The integrated roadmap preserves the completed v3.8.7 work.

## COMPLETE — PL-V38-00…04 + PREP-01

The following are treated as existing substrate:

```text
Direction Inventory
Target-State Explorer
Target Baseline Calibration
Current Capability Assessment
Causal Gap Derivation
Recommendation/History Reconciliation
Roadmap Synthesis/Prioritization
bounded Change handoff
local-only consumer update safety
```

The existing `PW-DIR-001…007` workflow chain remains the primary direction workflow architecture.

No second workflow engine is introduced.

---

# 6. CURRENT FIELD GATE — finish and reconcile Project Spine field evidence

## FIELD — PILOT-PL-DIRECTION-002

The source snapshot leaves Attempt 002 as next.

This baseline preserves the field gate rather than assuming its outcome.

Required reconciliation before feature expansion:

```text
authority-owned current-state validation
bounded detour/resume semantics
Change-handoff behavior
human proposal/selection boundary
context sufficiency
historical-state false-positive resistance
```

If this field gate has already progressed in the live repository when v3.9 is adopted:

```text
do not replay it merely to satisfy this document;
import the actual field receipt and reconcile its findings.
```

### Exit gate

```text
Project Spine handoff behavior is field-adjudicated
+
active REC-PL-DIRECTION-002 units have explicit disposition
+
no unresolved blocker requires a bounded correction before future work
```

Only then continue to the integrated future sequence.

---

# 7. PL-V39-05 — Project Shaping and Target Reality
## Enrich the Project Spine without adding another planning system

**Purpose:** make target direction more valuable, falsifiable, and physically tangible before heavy implementation.

This is the only genuinely new major vertebra introduced by this integration.

It does not replace `PW-DIR-001…007`.
It enriches their inputs/outputs and adds optional brownfield/greenfield patterns.

### PL-V39-05 Project Spine entry contract

Before broad shaping, preserve three already field-supported distinctions:

```text
1. discover direction authority before inventing Target material;
2. identify deliverable class early;
3. classify unresolved questions by semantic owner.
```

Deliverable-class examples include:

```text
end-user application
library/service
internal tool
research demonstrator
reference implementation
portfolio artifact
learning project
infrastructure component
```

This prevents historical aspiration or current implementation from silently
becoming the target.

Unresolved questions use:

```text
TARGET_BOUNDARY_QUESTION
CAPABILITY_DESIGN_QUESTION
RESEARCH_QUESTION
```

Only `TARGET_BOUNDARY_QUESTION` blocks Target convergence.

Capability-design and research questions remain attached to the relevant
capability and are retrieved when that layer becomes active.

This is not another workflow stage; it is an entry/ownership contract for the
existing Project Spine workflows.

---

## 7.1 Project Survey / current architecture snapshot

For material brownfield work, create a bounded AS-IS snapshot:

```text
reflects_revision
system boundaries
components/modules
datastores/state
external integrations
main execution paths
build/test/run commands
important conventions + source evidence
constraints
relevant debt
reusable assets
```

Rule:

```text
SURVEY = AS-IS EVIDENCE
TARGET = TO-BE ACCEPTED INTENT
```

Survey does not become a second `CURRENT_STATE`, Capability Assessment, or Gap authority.
It supplies bounded repository/runtime evidence to the existing Project Spine workflows,
which own interpretation, coverage/confidence, and Gap semantics.

Refresh only on material drift or when planning leaves surveyed scope.

This strengthens Direction Inventory / Current Capability Assessment rather than becoming a permanent separate lifecycle stage.

---

## 7.2 Brownfield Recovery when green tests are not trustworthy

For legacy/refactor/migration work, Survey may be insufficient.

Use a bounded archaeology/characterization pattern:

```text
scope
→ archaeology capsule
→ target skeleton plan
→ characterization/contract evidence
→ refine plan
```

Recovered facts carry provenance such as:

```text
OBSERVED_IN_CODE
OBSERVED_AT_RUNTIME
CHARACTERIZED_BY_TEST
DOCUMENTED
INFERRED
HUMAN_CONFIRMED
UNKNOWN
```

Never rewrite inferred current behavior as historical intent.

---

## 7.3 Outcome Ladder

For broad projects, allow several legitimate levels of success.

Candidate semantics:

```text
L4 NORTH_STAR
L3 TARGET
L2 USEFUL
L1 DEMONSTRABLE
L0 SALVAGE_FLOOR
```

Each level defines:

```text
value receiver
minimum capability claims
quality floor
required evidence
what may still be absent
```

Lower level means less scope, not lower correctness.

The ladder is a shaping aid, not several simultaneous canonical Targets.
Human Target acceptance selects one active Target State for the Project Spine.
Other levels remain value horizons, fallback stopping points, or future options.

`highest demonstrated level` is evidence-derived during Verification; it is not
a second aspirational target and does not mutate Target automatically.

Roadmap should know:
- current intended level when a ladder is used;
- highest demonstrated level;
- evidence needed for the next level.

The `L0…L4` labels are examples, not a universal fixed ontology.

Small Changes may omit the ladder entirely.

---

## 7.4 Adaptive engagement

Separate three axes conceptually:

```text
interaction cadence
analysis depth
model/effort routing
```

PL-V39-05 owns the first two as shaping/interaction choices.
Model/effort routing is an execution policy owned by PL-V39-07 and may consume
the selected depth as an input; Project Shaping must not create a competing model router.

Supported planning interaction patterns:

```text
FAST_WITH_LEDGER
SOCRATIC
BATCH_CLARIFICATION
HUMAN_GATES_ONLY
```

### FAST_WITH_LEDGER

For reversible, precedent-covered, low-blast choices:

```text
agent selects default
→ records one-line assumption + rationale
→ human receives one batch veto before commitment
```

A vetoed assumption becomes a real question.

### SOCRATIC

One material choice at a time.
The next question depends on the previous answer.

Use when choices interact or the user wants exploratory dialogue.

No interaction mode weakens hard correctness/authority floors.

---

## 7.5 Clarification and Project Lexicon

Use a bounded Clarification Sweep when ambiguity is material.

Check:

```text
open questions
goal/non-goal conflict
unstated assumptions
edge cases
term ambiguity
acceptance/evidence gaps
semantic owner ambiguity
```

For contract-heavy statements use the determinacy test:

> Can two reasonable implementers build materially different things while both satisfying the text?

If yes and the difference is material, clarify before Execution.

Do not let every unresolved question hold the whole Target hostage:

```text
TARGET_BOUNDARY_QUESTION
→ resolve before Target acceptance

CAPABILITY_DESIGN_QUESTION
→ defer to capability design

RESEARCH_QUESTION
→ resolve through the governed research capability
```

A lightweight Project Lexicon is triggered only by meaningful term drift:

```text
canonical term
definition
scope
accepted aliases
NOT / commonly confused with
source
```

Do not glossary-ify ordinary technical vocabulary.

---

## 7.6 Strategy Portfolio

For materially uncertain direction:

```text
generate 2–3 compact strategy cards
→ choose ONE active route
→ keep alternatives as contingency cards
```

A strategy card contains:

```text
route hypothesis
what it optimizes
key assumptions
major dependencies
major risks
Change Cost profile
expected Outcome Level reach
switch trigger
```

Do not maintain several full synchronized roadmaps.

Strategy route and execution pattern are different objects:

```text
strategy route
→ project-level way to reach the target

execution pattern
→ per-task way to perform authorized work
```

Before comparing value/cost, eliminate strategies that violate hard authority,
evidence, feasibility, or required-target constraints:

```text
eligible first
→ compare value / risk / Change Cost second
```

A dormant trigger does not switch the Roadmap automatically.
It makes the route eligible for reconciliation against current Target/Gaps/evidence.
Activation requires the normal human direction gate, and the dormant card is
revalidated rather than assumed current.

A dormant route expands only after that reconciliation.

---

## 7.7 Target Skeleton

For projects where end-to-end shape matters, create the thinnest traversable representation of the target.

### Greenfield

Either:

```text
ADDITIVE
minimal skeleton → add necessary seams
```

or, when a trusted archetype is semantically close:

```text
SUBTRACTIVE
known-good archetype → remove irrelevant capabilities
```

### Brownfield catch-up

```text
AS-IS real pieces
→ place into target silhouette
→ add minimum structural seams
→ explicit placeholders for missing capabilities
→ end-to-end skeleton smoke
```

Critical rule:

```text
placeholder != success
```

Missing capability must remain visibly:
- NOT_IMPLEMENTED;
- disabled;
- fixture-only;
- or otherwise non-passing.

No fake production success.

Ownership boundary:

```text
Project Shaping / Direction
→ defines target silhouette, Skeleton Contract, placeholder semantics,
  and proposes the bounded skeleton contribution

governed Change / Execution
→ materializes or rewires actual project files after normal authorization
```

Direction workflow must not mutate production merely to make the ideal picture
physically present. An early Skeleton Change is encouraged when valuable, but it
still uses the ordinary Change lifecycle.

---

## 7.8 Executable Target Contract

Translate the selected Outcome Level into a small set of System Claims.

Claim families:

```text
STRUCTURAL
SUCCESS_BEHAVIOR
FAILURE_OR_DEGRADATION
```

Then define canonical Target Scenarios with statuses:

```text
DEFINED
WIRED
PASSING
```

Track:

```text
Implementation Gap
Evidence Gap
```

The Target Skeleton may become structurally green while behavior remains honestly red.

Evidence channel is chosen from the failure class:

```text
unit/property
integration/e2e
browser/live UI
restart/recovery
benchmark
negative/adversarial
controlled experiment/holdout
rerun/identity
smoke/observability
human review
LLM eval/rubric where needed
```

Do not use unit tests as a universal sensor.

Ownership boundary:

```text
PL-V39-05
→ owns System Claims + Target Scenarios at least through DEFINED

governed project Execution / eval adapter
→ wires executable probes

Verification / PL-V39-08 adapters
→ records PASSING evidence
```

A Target Scenario is project intent/evidence need, not an EvalCase authority.
One Target Scenario may project into one or more versioned EvalCases; EvalCase
provenance must not redefine the project claim.

Claim failure may inform Implementation/Evidence Gaps, but does not automatically
create or close a canonical Project Spine Gap.

---

## 7.9 Roadmap synthesis enrichment

`PW-DIR-007` should eventually understand, without becoming larger in normal context:

```text
current Outcome Level
active strategy route
contingency triggers
System Claims
Target Skeleton status
Implementation Gap
Evidence Gap
Change Cost drivers
```

Roadmap dependency edge must have a reason.

Separate:

```text
DEPENDENCY
PRIORITY
ACTIVE EXECUTION PATH
STATUS
```

Historical order remains non-authoritative.

### Recommendation detail cards

- [PL-REC-SPLIT-CONTROL-HISTORY-V1 — Separate Product History from Planning / Control History](../recommendations/inbox/PLANNING_LITE_RECOMMENDATION_SPLIT_CONTROL_HISTORY_V1.md) — INBOX / CANDIDATE / ROUTED_RECHECK; detail pointer only, not absorbed or prioritized.

Future detail:

- [FUT-LEX-001 — Automated semantic term-drift detector](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-CLAR-001 — Automated ambiguity challenger](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.
- [FUT-OUT-001 — Automated Outcome Ladder proposal](../recommendations/FUTURE-RESERVE.md) — FUTURE / WATCH; detail pointer only, not scheduled.
- [FUT-STRAT-001 — Automatic contingency route activation](../recommendations/FUTURE-RESERVE.md) — FUTURE / REJECTED_FORM FOR NOW; detail pointer only, not scheduled.
- [FUT-STRAT-002 — Multiple full synchronized roadmaps](../recommendations/FUTURE-RESERVE.md) — FUTURE / REJECTED_FORM; detail pointer only, not scheduled.
- [FUT-SCAF-001 — Full verified scaffold self-evolution](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-SCAF-002 — Reusable subtractive archetype library](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.
- [FUT-SCAF-003 — Universal non-software Target Skeleton tooling](../recommendations/FUTURE-RESERVE.md) — FUTURE / WATCH; detail pointer only, not scheduled.
- [Dormant Contingency Route A — Adaptive Scale Route](../recommendations/FUTURE-RESERVE.md) — FUTURE / DORMANT / NO SCHEDULING PROMISE; detail pointer only, not scheduled.

### PL-V39-05 exit gate

A representative complex fixture can demonstrate:

```text
AS-IS grounded
+
target/value level explicit
+
one active strategy selected
+
optional contingencies bounded
+
target skeleton semantics honest
+
small executable target claim set defined
+
no fake green placeholders
+
Roadmap derived without multiplying stages for each recommendation
```

Small routine changes still bypass unnecessary shaping machinery.

---

# 8. PL-V39-06 — Context, Memory, Visibility, and Handoffs
## One memory system, several resolutions

This absorbs the old `PL-V38-05`, `REC-PL-MEMORY-EFFICIENCY`, `REC-PL-CONTEXT-HANDOFF`, and direction-memory units from v3.7.

Do not create a second memory architecture.

---

## 8.1 Direction-aware visibility

Extend context policy with:

```text
ACTIVE_DIRECTION
DEFERRED_VISIBLE
ARCHIVE_INDEXED
UNANCHORED_BACKLOG
```

Use visibility decay, not information deletion.

Interpret the Project Spine itself as a long-horizon memory index:

```text
TARGET STATE
→ very slow directional memory

ROADMAP
→ long-term directional memory

GAP MAP
→ active incompleteness memory

ACTIVE CHANGES
→ working memory

COMPLETED CAPSULES / EVIDENCE
→ durable archived memory
```

Roadmap/Gaps retain compact identity, outcome and lineage, not full history.

Use multi-resolution retrieval:

```text
L3 = IDs / relations / status
L2 = one-line outcome
L1 = bounded capsule
L0 = full evidence
```

Default project/stage entry prefers Project Spine `L3/L2`.
Expand through lineage to `L1/L0` only when needed.

```text
archive
=
not injected by default
!=
forgotten
```

Default retrieval begins with deterministic lineage.

---

## 8.2 Three-plane state model

Keep separate:

```text
WORKSPACE / SCRATCH
DURABLE EVIDENCE / TRACE
STAGE HANDOFF STATE
```

Durable history is not inherited active context.

---

## 8.3 Context Bootstrap Capsule

At:
- fresh session;
- stage transition;
- model handoff;
- post-compaction;

provide a tiny derived capsule such as:

```text
project/change identity
current lifecycle/stage
current target/outcome level
active route
hard authority constraints
authoritative artifact pointers
current revision/freshness seam
```

Generate it from canonical state.
Do not hand-maintain a second source of truth.

### Canonical Boundary Capsule

Distinguish the re-entry capsule above from a gate/stage boundary artifact.

Where downstream stages need exact IDs, hashes, contracts, dispositions or
other machine-critical facts:

```text
upstream owner
→ emits canonical machine-readable boundary
→ downstream stage consumes it
```

Do not repeatedly copy/retype the same SHA/ID/contract into prompts and
documents.

The boundary capsule is canonical for the facts it owns.
The Context Bootstrap Capsule is a derived view over current canonical state.

---

## 8.4 Stage-specific bounded context

Context selection order:

```text
authority/lineage
→ compact current state
→ relevant stage artifacts
→ relevant capsules
→ raw evidence only when needed
→ semantic retrieval only when lineage is insufficient
```

Historical Readiness/plans are retrieval-on-demand.

---

## 8.5 Authority-owned current assertions

Machine validation targets current-authority seams, not whole-document negative token scans.

Prefer a small stable provenance/current assertion seam where needed.

No general Python Project Spine domain model unless evidence requires one.

---

## 8.6 ContextTrace

Every meaningful stage/agent packet should be able to record:

```text
what was loaded
why it was loaded
what authoritative path selected it
what extra context was requested
what history was intentionally excluded
```

ContextTrace is observation first, optimization later.

---

## 8.7 Subagent Result Contracts

Isolation must apply to both input and output.

A subagent dispatch should specify:

```text
mission
source/scope boundary
questions
required evidence
output contract
escalation rule
```

The parent receives:
- material findings;
- evidence pointers;
- unresolved questions;

not the entire subagent scratch narrative.

---

## 8.8 Memory admission remains governed

Project observations do not automatically become central memory/rules.

Preserve:

```text
local evidence
→ recommendation/learning candidate
→ governed promotion
```

### Recommendation detail cards

Future detail:

- [FUT-MEM-001 — Semantic retrieval / embeddings after lineage routing](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-MEM-002 — Episodic timeline + temporal summary tree](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.
- [FUT-MEM-003 — Memory utility ledger and evidence-based forgetting](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-MEM-004 — Semantic memory maintenance automation](../recommendations/FUTURE-RESERVE.md) — FUTURE / WATCH; detail pointer only, not scheduled.
- [FUT-ARCH-001 — Graph database for Project Spine](../recommendations/FUTURE-RESERVE.md) — FUTURE / REJECTED_FORM UNTIL EVIDENCE; detail pointer only, not scheduled.

### PL-V39-06 exit gate

Paired field fixtures demonstrate:

```text
bounded handoff preserves semantic/authorization correctness
historical context is not loaded by default
missing context defers safely
ContextTrace explains selection
fresh session/post-compaction resumes from a small capsule
subagent result contracts prevent context re-expansion
```

No Context Compiler production runtime yet.

---

# 9. PL-V39-07 — Execution Contracts, Skills, Checklists, and Routing
## Make execution precise without making the root prompt huge

This reconnects v3.7 Skill Engineering + Checklist Control with the newer weak-model and readiness evidence.

---

## 9.1 Checklist Control Layer

Start/continue with a small stable checklist registry.

A checklist is distinct from task-specific acceptance criteria.

High-value checklist families may include:

```text
EXEC_PREFLIGHT
DEFINITION_OF_DONE
CHANGE_READY
CHANGE_CLOSE
READINESS_COMPLETENESS
MATERIALITY_SIMPLICITY
CONTRACT_CLOSURE
EVAL_VALIDITY
```

Each hard item binds to evidence, not self-report.

One canonical checklist may have:
- operational projection;
- eval projection.

---

## 9.2 Skill Engineering

Distinguish:

```text
capability skill
workflow/policy skill
```

Keep skill bodies compact.
Route detailed references conditionally.

Description is an activation surface, not a duplicate manual.

Stable skill bodies should not churn when a checklist-only delta suffices.


## 9.2A Optional change-local Behavior / State Coverage Capsule

Recover the useful part of the older Behavior Localization design without
creating a permanent global handbook.

Activate only for work that is:
- cross-file or cross-module;
- state-coupled;
- search-hostile;
- recovery/cold-path sensitive;
- or has incomplete ownership.

The derived capsule may record:

```text
behavior delta
critical state fields
writers / readers / resets
must-never-be-inferred-from
verified current source anchors
cold/recovery paths
verification per behavior/state
coverage gaps
```

Source anchors are revalidated against live source before they become Planning
or Readiness evidence.

This is derived evidence, not canonical project truth.
Local obvious edits skip it.

---

## 9.3 Four-layer Contract Closure

For contract-heavy work:

```text
SHAPE
SEMANTICS
ENCODING
OWNERSHIP
```

Planning owns missing material semantics.

Readiness asks:
- can two materially different implementations satisfy the same text?
- where bytes/hashes matter, can the same state have two valid encodings?
- can two task ownership allocations both satisfy the plan?

Execution asks:
> Do I need to invent a material semantic choice?

If yes and not authoritative:

```text
BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY
```

---

## 9.4 Readiness completeness

Readiness is exhaustive within scope.

A negative verdict is not an early-stop condition.

Use:

```text
vertical audit
cross-contract/junction audit
counterfactual post-repair pass
materiality filter
```

Optional/speculative improvements are not blockers.

Readiness is multidimensional where the Change needs it:

```text
SEMANTIC_READY
DELIVERY_READY
CONTRACT_READY
EVIDENCE_READY
RUNTIME_READY
PROVENANCE_READY
ENVIRONMENT_READY
```

Select only applicable dimensions for the Change type.

General invariant:

```text
traceability-complete
!=
execution-ready
```

`READY` is the conjunction of the applicable dimensions, not a vibe and not a
requirement that every Change pay every readiness tax.

---

## 9.5 Materiality/Simplicity gate

For support machinery:

```text
evidence class
→ simplest sufficient form
→ deferability
→ classification:
   MUST_KEEP
   SIMPLIFY_NOW
   DEFER
   DROP
   HUMAN_DECISION
```

Prefer architecture that removes failure states rather than adding guards around self-created machinery.

---

## 9.6 Task Closure Review

For high-leverage task-owned contracts:

```text
task seam PASS
→ nearest-wrong probes
→ bounded independent closure review where warranted
→ freeze task
→ authorize dependent task
```

Do not turn this into a mandatory extra lifecycle stage for trivial tasks.

Local blocker blocks only its dependency cone when independent authorized work can continue.

---

## 9.7 Execution Pattern Router

Choose execution pattern from task shape.

Candidate patterns:

```text
BOUNDED_LOOP
TDD / CONTRACT_CLOSURE
PARALLEL_INDEPENDENT_LANES
FEEDBACK_LOOP
BACKGROUND/SCHEDULED where host supports it
STRONG_JUDGMENT / HUMAN_DIALOGUE
```

Routing facts:

```text
dependency shape
verification channel
risk/materiality
reversibility
contract criticality
expected duration
```

Do not use multi-agent orchestration merely because it is available.


## 9.7A Execution Envelope and structured blockers

Keep prose policy separate from what the execution environment actually permits.

For material tasks the authorized envelope may specify:

```text
readable/writable paths
forbidden paths
tool allowlist
network capability
Git capability
mutation authorization
execution profile
environment/provenance facts when material
```

Prefer host/sandbox enforcement when available.
Otherwise run bounded deterministic preflight and fail closed rather than relying
on the model to remember a long prohibition list.

A blocker should be machine/actionable where practical:

```text
failure_class
evidence
allowed_actions
forbidden_actions
next_action
```

Do not standardize numeric exit codes until a real tool surface requires them.

A fact-only reconciliation detour preserves the original governed question and
resumes it after the owning current-state seam is repaired; it does not silently
reprioritize the Roadmap.

## 9.7B Validation sufficiency

Execution selects the smallest evidence set sufficient for the actual blast radius
and failure class.

Typical ladder:

```text
isolated internal change
→ focused unit/static checks

public contract / producer-consumer change
→ contract + consumer checks

cross-boundary/state/routing change
→ broader integration/build/recovery checks

release boundary
→ release gate
```

The selected validation should state why it is sufficient.

This consumes the Feedback Channel Matrix from PL-V39-05 rather than creating a
second validation taxonomy.

---

## 9.8 Model / effort routing

Route by role, then calibrate with evals.

Candidate semantics:

```text
ambiguity/strategy/adjudication
→ strongest reasoning tier

closed bounded implementation
→ cheaper capable execution tier

deterministic extraction
→ code/cheap model

independent high-impact review
→ fresh strong tier
```

Do not hardcode vendor/model names into durable semantics.

---

## 9.9 Decision reversibility gate

```text
reversible + precedent-covered
→ agent may decide locally

reversible + novel
→ decide + record if material

high blast / expensive to reverse / semantic authority
→ explicit Planning/Human gate
```

This reduces unnecessary questions without surrendering authority.

## 9.10 Pilot-before-scale rule

PL-V39-07 may establish the minimum stable Skill/Checklist/Execution contracts
using existing deterministic checks and current harness mechanics.

Do not grow a large skill/checklist corpus before PL-V39-08 extracts/reconciles
the reusable Eval Core.

The intended loop is:

```text
small stable pilot semantics in 07
→ reusable/qualified eval in 08
→ evidence-backed scale-out or correction of 07 artifacts
```

This is a controlled loopback, not a new lifecycle stage.

### Recommendation detail cards

- [CHG-0009 Field Findings Adjudication](../recommendations/inbox/PLANNING-LITE-CHG0009-FIELD-ADJUDICATION-v1.md) — INBOX / ROUTED_RECHECK; detail pointer only, not absorbed or prioritized.
- [Prompt-Derived Governance Primitives and Reusable Agent Skills](<../recommendations/inbox/PL-REC — Prompt-Derived Governance Primitives and Reusable Agent Skills.md>) — INBOX / PROPOSED; detail pointer only, not absorbed or prioritized.
- [PL-REC-PRE-READINESS-CLOSURE-COMPLETENESS-001](../recommendations/inbox/PL-REC-PRE-READINESS-CLOSURE-COMPLETENESS-001.md) — INBOX / DEFERRED / ROUTED_RECHECK; detail pointer only, not absorbed or prioritized.
- [PL-REC-TASK-VERIFIER-BASELINE-SNAPSHOT-001 v1.1](../recommendations/inbox/PL-REC-TASK-VERIFIER-BASELINE-SNAPSHOT-001-v1.1.md) — INBOX / DEFERRED / ROUTED_RECHECK; detail pointer only, not absorbed or prioritized.
- [REC-PL-CODE-CONSTRUCTION-QUALITY-CHECKLISTS](../recommendations/inbox/REC-PL-CODE-CONSTRUCTION-QUALITY-CHECKLISTS.md) — INBOX / PROPOSED; detail pointer only, not absorbed or prioritized.
- [REC-PL-ROUTING-PROMPT-DEDUP](../recommendations/inbox/REC-PL-ROUTING-PROMPT-DEDUP.md) — INBOX / PROPOSED / NOT_RECONCILED; detail pointer only, not absorbed or prioritized.
- [Revised PL-V39-07 roadmap boundary](<../recommendations/inbox/Revised PL-V39-07 roadmap boundary.md>) — INBOX / STATUS NOT RECORDED; detail pointer only, not absorbed or prioritized.

Future detail:

- [FUT-EXEC-001 — Automatic Execution Pattern Router](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-EXEC-002 — General multi-agent team orchestration](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-EXEC-003 — Background/scheduled autonomous work as a Planning Lite primitive](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.
- [FUT-EXEC-004 — Full cross-host capability adapter matrix](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.
- [FUT-PLAN-001 — Persistent Behavior Localization / State Register Handbook](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-PLAN-002 — Typed PlanningProblem + bounded candidate-plan optimizer](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-DOC-001 — Semantic advisory Doctor](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.
- [SUP-001 — Weak Model Execution v1/v2](../recommendations/FUTURE-RESERVE.md) — LINEAGE / SUPERSEDED; predecessor evidence pointer only, not active authority.

### PL-V39-07 exit gate

Controlled fixtures demonstrate:

```text
precise skill activation
checklist evidence binding
weak model executes closed contract without semantic invention
under-specified contract blocks correctly
local blocker locality works
Readiness remains exhaustive
simple tasks remain lightweight
execution pattern choice improves fit without orchestration inflation
```

---

# 10. PL-V39-08 — Evaluation, Learning, PromptOps, and Controlled Evolution
## One coherent testing/learning limb

This is the major consolidation block.

It revives the strongest dormant v3.7 work instead of creating a new eval architecture from lecture notes.

It absorbs:

```text
old PL-V38-06A/06B intent
v3.7 Reusable Prompt/Eval Core
fixture qualification
REC-PL-CONTROLLED-EVOLUTION
REC-PL-LEARNING-LOOP
REC-PL-RULE-PLAYBOOK-CURATION
Change Cost actual receipts
new control-plane behavioral eval idea
Operational Insights
Prompt Garden future reuse
```

---

## 10.1 PL-V39-08A — Research asset reconciliation

Reconcile:

```text
planning-lite-lab
planning_lite_tools step-16.4.1
older lineage-required assets
code companion
existing prompt/eval seeds
```

Output:

```text
REUSE
ADAPT
REFERENCE_ONLY
ARCHIVE_REQUIRED
ARCHIVE_SAFE
```

No deletion before a lineage receipt.

---

## 10.2 PL-V39-08B — Reusable Eval Core

Preserve the v3.7 generic boundary:

```text
ArtifactUnderTest
ArtifactVersion
ChangeReason
Hypothesis
EvalCaseSet
ExecutionProfile
Run
Evidence
VerifierResult
AggregateResult
ExperimentDecision
```

Artifact kinds include:

```text
prompt
prompt_combination
skill
checklist
routing_policy
agent_workflow
memory_rule
tool_policy
control_logic
```

Planning Lite lifecycle semantics belong in adapters, not generic core.

### Case families

```text
positive activation
negative activation
production-derived
held-out acceptance
retention/regression
```

### Verifier hierarchy

```text
deterministic trace/artifact
→ structured grader
→ model judge
→ human review
```

Use the cheapest reliable verifier.

---

## 10.3 Fixture qualification

Keep distinct:

```text
CanonicalSourceBundle
DerivedArtifact
ScenarioOverlay
ExpectedSemanticProjection
FixtureQualificationReceipt
```

Infrastructure/preparation failures are not candidate-quality failures.

Separate:

```text
source/fixture admissibility
execution validity
evaluation outcome
```

An infrastructure-invalid run is evidence about the harness/environment and is
`not_evaluated` for candidate quality.

Cases are campaign-eligible only after qualification.

---

## 10.4 Control-plane behavioral regression

Planning Lite itself becomes an ArtifactUnderTest.

Start from real field regressions.

Examples:

```text
Readiness must continue after first blocker
Execution must not invent missing semantics
local blocker must not stop independent safe correction
historical tokens must not trigger false current-state staleness
bounded context should not load history unnecessarily
Materiality review must be able to delete self-created machinery
```

Grade observable outcomes.

Keep at least these dimensions distinguishable when material:

```text
outcome correctness
plan-shape / workflow correctness
negative safety / authorization
evidence validity
context/tool trace
efficiency/cost
```

A correct outcome reached through a forbidden or needlessly broad workflow is
not a fully successful control-plane run.

Do not grade exact prose.

Cheap deterministic validators remain separate from real-agent behavior evals.

---

## 10.4A Recommendation Absorption as a self-hosted control-plane fixture

The current v3.9.x reconciliation is itself a field fixture.

The manual acceptance rubric is:

```text
COVERAGE
→ no useful RecommendationUnit lost

PLACEMENT DETERMINACY
→ no material unit has two competing owners

ANTI_HAIR
→ no roadmap vertebra exists merely because a recommendation had a title

CONTRADICTIONS
→ merged units do not encode incompatible authority/sequencing semantics

FUTURE_PRESERVATION
→ deferred value has identity + trigger

NO_SILENT_RESIDUE
→ every touched unit has disposition
```

Use the same rubric later as a control-plane eval case before productizing the
workflow. Automation remains deferred.

## 10.5 Executable Target Contract as project eval input

System Claims/Target Scenarios defined in PL-V39-05 can be consumed by project-specific eval adapters.

This links:

```text
Outcome Level
→ System Claims
→ Target Scenarios
→ evidence channel
→ eval result
→ demonstrated level
```

No single test framework is forced across all project types.

Canonical ownership:

```text
Target Scenario
→ project-level claim/evidence intent

EvalCase
→ versioned executable case with fixture/provenance/verifier identity
```

Projection may be one-to-many.
Eval results update evidence/demonstration status; they do not silently rewrite
the Target Scenario.

---

## 10.6 PromptOps and Prompt Garden lineage

The old Prompt Garden is not a forgotten separate project.

It becomes a future/secondary consumer of the same reusable eval core:

```text
prompt registry
versions
change reason
hypothesis
case sets
run evidence
lineage
champion/challenger
```

Planning Lite control-plane eval is the first consumer.

Prompt Garden integration is not required for the first PL-V39-08 release gate.

---

## 10.7 Operational Insights

Use real Planning Lite receipts:

```text
Planning loops
Readiness loops
corrections
extra-context loads
tool/model routing
verification failures
human gates
Change Cost actuals
task closure findings
```

Insights pipeline:

```text
deterministic aggregation
→ transparent sampling
→ LLM synthesis
→ MEASURED vs INFERRED findings
→ Recommendation candidates
```

Every report states:
- time window;
- sample size;
- sample method;
- missing data;
- main vs subagent/session classes where relevant.

No insight auto-edits policy.

---

## 10.8 Change Cost calibration

Continue evidence-derived profiles:

```text
Change Surface
Propagation/blast radius
historical coupling
hotspot exposure
change entropy
Mechanism Delta
Verification burden
Carry cost
```

Add actual process receipts:

```text
Planning iterations
Readiness iterations
eval calls
closure reviews
tool calls
human gates
rework
wall-clock where reliable
```

Use cost to compare alternatives, not as a fake universal scalar initially.

---

## 10.9 Controlled Evolution

Framework learning remains conservative:

```text
field failure
→ diagnosis
→ minimal candidate delta
→ micro-eval
→ held-out/retention evidence
→ independent review
→ explicit central Change
→ promotion or rollback
```

Preferred mutable order:

```text
checklist delta
→ conditional reference
→ rule/playbook
→ skill body
→ root/control prompt only when necessary
```

No candidate changes its own evaluator or promotion gate.

No automatic self-improvement.

### Recommendation detail cards

- [PL-V39-08/09 — Empirical Fixtures: Coverage Failures](../recommendations/inbox/PL-V39-08-09-EMPIRICAL-FIXTURES-COVERAGE-FAILURES-v1.md) — INBOX / CAPTURED_FOR_FUTURE_EVALUATION; detail pointer only, not absorbed or prioritized.

Future detail:

- [FUT-EVAL-001 — Full Prompt Garden integration](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.
- [FUT-EVAL-002 — Broad LLM-judge infrastructure](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-EVAL-003 — Full behavioral eval suite on every commit](../recommendations/FUTURE-RESERVE.md) — FUTURE / REJECTED_FORM; detail pointer only, not scheduled.
- [FUT-EVAL-004 — Generalized mutation/fuzzing framework for contracts](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-EVAL-005 — Schema-driven code generation](../recommendations/FUTURE-RESERVE.md) — FUTURE / WATCH; detail pointer only, not scheduled.
- [FUT-INS-001 — Full session-mining Operational Insights service](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-MET-001 — Single scalar Change Cost score](../recommendations/FUTURE-RESERVE.md) — FUTURE / REJECTED_FORM / MAY REFRAME; detail pointer only, not scheduled.
- [FUT-MET-002 — Expected value / expected Change Cost ratio](../recommendations/FUTURE-RESERVE.md) — FUTURE / FUTURE_SEED; detail pointer only, not scheduled.

### PL-V39-08 exit gate

At least one Planning Lite control component can be evaluated end-to-end:

```text
qualified fixture
→ frozen candidate
→ deterministic/behavioral eval
→ execution-valid result
→ independent decision
→ preserved lineage
```

and:

```text
real Poker/project failures exist as regression cases
Prompt/Eval Core is reusable beyond one lifecycle harness
Operational Insights can produce evidence-backed candidate findings
Change Cost actual receipts are captured
```

---

# 11. PL-V39-09 — Context Compiler, Safe Orchestration, and Release Decision
## Automation last

This merges the old `PL-V38-07` and `PL-V38-08` rather than adding more final stages.

---

## 11.1 Context Compiler experiment

This is an optional comparator experiment, not a hidden prerequisite for release.

The bounded architectural result is maintained in the subordinate companion
[`companions/PL-V39-09-CONTEXT-COMPILATION-CONDITIONAL-SKELETON-v1.md`](companions/PL-V39-09-CONTEXT-COMPILATION-CONDITIONAL-SKELETON-v1.md).
It is detailed design subordinate to this Roadmap: the conditional skeleton is
`FROZEN`, the full Context Compilation contract is `NOT_FROZEN`, and production
implementation is `NOT_AUTHORIZED`. The companion cannot change macro
direction, authorize implementation, or override this Roadmap.

### 09-B Ideal Scaffold Knowledge architectural skeleton

The bounded architectural skeleton is maintained in the subordinate companion
[`companions/PL-V39-09-IDEAL-SCAFFOLD-KNOWLEDGE-SKELETON-v1.md`](companions/PL-V39-09-IDEAL-SCAFFOLD-KNOWLEDGE-SKELETON-v1.md).
It freezes only the Ideal-first, implementation-blind/domain-informed,
layered-fingerprint, driver-bound, question-first, structured-semantic and
bounded pack-guidance invariants. The validated Architecture Knowledge topology
and ownership seams are now `FROZEN_CANONICAL`; final pack contents and question
inventories remain `NOT_FROZEN`, field validation is `REQUIRED`, and production
implementation is `NOT_AUTHORIZED`. Portable supporting evidence is maintained
in the subordinate companion
[`companions/PL-V39-09-ARCHITECTURE-KNOWLEDGE-TOPOLOGY-FREEZE-EVIDENCE-v1.md`](companions/PL-V39-09-ARCHITECTURE-KNOWLEDGE-TOPOLOGY-FREEZE-EVIDENCE-v1.md).
This is framework knowledge supporting existing 09-B responsibility, not a new
top-level subsystem.

```text
IDEAL_SCAFFOLD_KNOWLEDGE_SKELETON:
FROZEN_CANONICAL

V1_ARCHITECTURE_KNOWLEDGE_TOPOLOGY:
FROZEN_CANONICAL

PACK_CONTENT:
NOT_FROZEN

FIELD_VALIDATION:
REQUIRED

PRODUCTION_IMPLEMENTATION:
NOT_AUTHORIZED
```

### Engineering Basis and Rationale Lineage semantic contract

The canonical V1 semantic contract is maintained in the subordinate companion
[`companions/PL-V39-09-ENGINEERING-BASIS-RATIONALE-LINEAGE-SEMANTIC-CONTRACT-v1.md`](companions/PL-V39-09-ENGINEERING-BASIS-RATIONALE-LINEAGE-SEMANTIC-CONTRACT-v1.md).
It freezes the owner-adjudicated Engineering Basis and Rationale Lineage
semantics only. Field validation remains required; serialization, storage, and
runtime design remain unfrozen; production implementation remains unauthorized;
and this materialization does not activate PL-V39-09 implementation.

```text
ENGINEERING_BASIS_RATIONALE_LINEAGE_SEMANTIC_CONTRACT:
CANONICAL_V1

FIELD_VALIDATION:
REQUIRED

SERIALIZATION:
NOT_FROZEN

STORAGE_MODEL:
NOT_FROZEN

PRODUCTION_IMPLEMENTATION:
NOT_AUTHORIZED

PL09_IMPLEMENTATION_ACTIVATION:
NONE
```

Possible terminal result:

```text
compiler non-inferior + materially better
→ eligible for bounded promotion decision

compiler not better / too costly
→ RETAIN CURRENT CONTEXT PATH
→ continue safe orchestration/release work
```

A losing experiment is a valid result.

Comparator arms:

```text
A raw canonical docs
B compact status snapshot
C snapshot + authoritative workflow
D Project Spine + workflow → compiled AgentWorkPacket
```

Measure:

```text
semantic correctness
authorization correctness
routing success
resolution success
safe deferral
file reads
extra-context requests
tokens
retries
timing
```

Promotion requires:

```text
non-inferior correctness
+
material context-discipline improvement
```

Token savings alone are insufficient.

---

## 11.2 AgentWorkPacket

Candidate packet:

```text
task
current state
target/outcome position
active route
gap/roadmap lineage
relevant constraints
allowed actions
open questions
canonical evidence refs
acceptance/evidence schema
```

Include Context Bootstrap Capsule semantics.

Keep the distinction:

```text
Context Bootstrap Capsule
→ tiny task-independent current-state re-entry surface

AgentWorkPacket
→ task-specific ephemeral/derived packet; may include the capsule plus task data
```

The packet is not a second memory authority.

Use Result Contracts for subagents.

---

## 11.3 Safe orchestration

Automate only transitions proven deterministic/read-only and behaviorally evaluated.

Candidate direction flow:

```text
inventory
→ consistency
→ target draft
→ clarification
→ target calibration
[HUMAN TARGET ACCEPTANCE]
→ current assessment
→ causal gaps
→ recommendation reconciliation
→ roadmap synthesis
[HUMAN DIRECTION ACCEPTANCE]
```

Existing governed Change lifecycle follows.

Orchestration uses the best validated current context surface.
It must not depend on Context Compiler promotion unless that experiment actually
wins its comparator and is separately accepted.

Bounded factual reconciliation detours resume the original governed question
after repair rather than silently creating a new priority.

Where current accepted direction supplies enough evidence, the agent should
propose bounded candidate slices/options; human authority means accept/reject/
adjudicate, not an obligation for the human to invent the next candidate.

Execution-pattern routing may be automated only after eval evidence shows the router is reliable.

---

## 11.4 Host-agnostic semantic core

Canonical Planning Lite semantics should be host-independent.

Possible primitives:

```text
ASK_USER
ASK_BATCH
SOCRATIC_TURN
FRESH_CONTEXT
ISOLATED_REVIEW
PARALLEL_EXPLORE
READ_CURRENT_STATE
RUN_DETERMINISTIC_CHECK
WRITE_ARTIFACT
```

Claude/Codex/etc. mappings are projections/adapters.

Do not bake one agent product's command vocabulary into the core lifecycle.

---

### Recommendation detail cards

- [Context Compiler Decision and Terminology Surface](<../recommendations/inbox/PL-REC — Context Compiler Decision and Terminology Surface.md>) — INBOX / UNADJUDICATED_RECOMMENDATION_CANDIDATE; detail pointer only, not absorbed or prioritized.
- [Human Guidance, Prompt Delta Memory, Context Compiler & PromptOps Analytics](../recommendations/inbox/PL-V39-09-HUMAN-GUIDANCE-PROMPT-DELTA-MEMORY-CONCEPT-NOTE-v1.md) — INBOX / PROPOSED / NOT YET ADJUDICATED; detail pointer only, not absorbed or prioritized.

Future detail:

- [FUT-CTX-001 — Production Context Compiler beyond experimental promotion](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-CTX-002 — Learned context selection policy](../recommendations/FUTURE-RESERVE.md) — FUTURE / WATCH; detail pointer only, not scheduled.

## 11.5 Release / promotion decision

Before a new release-level promotion require:

```text
small-change regression remains lightweight
Project Spine direction flow works
context policy works
weak-model execution behavior works
control-plane evals exist
rollback path exists
no hidden authority automation
research assets have disposition
future recommendation residue is accounted
```

Full autonomous scaffold evolution is not required for this release gate.

Production Context Compiler promotion is also not required.
If the compiler experiment does not demonstrate material benefit, release may
retain the validated bounded-context path. Broader compiler promotion remains a
future recommendation with its own evidence gate.

---

# 12. Continuous practices, not stages

## 12.1 Recommendation / Discovery lifecycle

### Recommendation detail card convention

Recommendation detail cards are visibility and lineage pointers only. They do
not imply absorption, acceptance, priority, implementation authority, or Change
authorization. Detailed semantics and recorded status remain in the linked
source.

Keep observations and actions distinct:

```text
DISCOVERY
= observed fact / behavior / evidence

RECOMMENDATION
= proposed action or policy change
```

A Discovery may produce zero, one or several Recommendations.
Do not force every interesting observation into Roadmap work.

Use three lightweight modes.

### TRIAGE

For rough/unanchored inputs:

```text
deduplicate
cluster
merge/split
challenge
classify
anchor only where justified
preserve unanchored residue
```

### RECONCILE

After a material Change or recommendation-absorption pass:

```text
which RecommendationUnits were realized?
which remain?
which became future seeds?
which Gap changed?
did Target/Roadmap receive a real signal?
```

### CONVERGE

Periodically, not after every tiny edit, detect:

```text
future seed whose trigger became true
stale partially-realized recommendation
accepted but never anchored item
"completed" recommendation with open residue
long-untriaged unanchored item
superseded/duplicate chain with unresolved residue
```

Use the bounded `RECOMMENDATION_ABSORPTION_ACCEPTANCE` checklist when absorbing
unanchored recommendations:

```text
coverage
placement determinacy
anti-hair
contradictions
future preservation
no silent residue
superseded-lineage residue
```

This is current practice.
A productized automated absorption/convergence workflow remains future work.

Recommendation details:

- [Out-of-Git Operational Intake and Working State](../recommendations/inbox/PL-REC-OUT-OF-GIT-OPERATIONAL-INTAKE-DISCOVERY-001.md) — INBOX / NEW; detail pointer only, not absorbed or prioritized.

Future detail:

- [FUT-REC-001 — Automated recommendation convergence / cemetery recovery](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-REC-002 — Automated recommendation unit extraction](../recommendations/FUTURE-RESERVE.md) — FUTURE / WATCH; detail pointer only, not scheduled.
- [FUT-REC-003 — Automatic rule curator / selective unlearning](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [FUT-ABSORB-001 — Productized Recommendation Absorption workflow](../recommendations/FUTURE-RESERVE.md) — FUTURE / DEFERRED_EXPERIMENT; detail pointer only, not scheduled.
- [SUP-002 — Older roadmap copies as active priority](../recommendations/FUTURE-RESERVE.md) — LINEAGE / SUPERSEDED AS CURRENT PRIORITY; historical-design pointer only, not active priority.

## 12.2 Actual-cost receipts

Collect opportunistically in normal work.
Do not turn measurement into a project tax.

## 12.3 Operational field fixtures

Poker, Wiki and other real projects remain evidence sources.
Do not force every finding into the roadmap immediately.

## 12.4 Code/research asset check

Run before designing non-trivial new machinery.
Not required for trivial local changes.

## 12.5 Project Spine integrity / orphan check

Use a lightweight structural check before Roadmap release and during periodic
convergence.

Detect or surface:

```text
target capability without fitness criterion
Gap without target capability
roadmap item without Gap lineage
active Change without roadmap lineage where lineage is required
completed roadmap item with still-open claimed Gap
accepted recommendation without anchor/explicit unanchored status
recommendation marked completed with semantic residue
future seed whose trigger is now true
target capability with no implementation/research path
repository capability not represented in Target State
```

The last item is a signal, not an automatic error: current implementation may
legitimately contain out-of-target or legacy capability.

This check should remain mostly deterministic/structural.
A broad semantic "Doctor" remains a separate future possibility.

---

# 13. What this roadmap deliberately does NOT add

No new standalone stages for:

```text
Materiality/Simplicity
Weak-model execution
Project Lexicon
Socratic dialogue
Assumptions Ledger
Subagent Result Contract
Feedback Channel Matrix
Change Cost
Task Closure Review
Operational Insights
Prompt Garden
```

These are methods/capabilities inside existing blocks.

No immediate:

```text
graph database
embedding-first memory
universal multi-agent team
automatic rule curator
automatic forgetting
full scaffold self-evolution
general fuzzing framework
schema compiler
semantic Doctor
three full synchronized roadmaps
```

Those are future seeds or rejected forms, not current roadmap anatomy.

---

# 14. Revised integrated sequence

```text
COMPLETED
PL-V38-00..04 + PREP-01
    ↓
CURRENT FIELD GATE
PILOT-PL-DIRECTION-002 reconcile actual field state
    ↓
PL-V39-05
Project Shaping + Target Reality
    ↓
PL-V39-06
Context + Memory + Handoffs
    ↓
PL-V39-07
Execution Contracts + Skills + Checklists + Routing
    ↓
PL-V39-08
Evaluation + Learning + PromptOps + Controlled Evolution
    ↓
PL-V39-09
Context Compiler + Safe Orchestration + Release Decision
```

This is one additional major future vertebra compared with v3.8.7, not a recommendation explosion.

## 14.1 Mainline dependency vs parallel preparation

The sequence above is the promotion/mainline order, not a ban on cheap read-only preparation.

Allowed preparation without skipping gates:

```text
after CURRENT FIELD GATE
→ PL-V39-08A research-asset reconciliation may begin read-only

during/after PL-V39-05
→ inventory existing skills/checklists and candidate field fixtures
   may begin without promoting new execution policy

after minimal PL-V39-07 artifact semantics
→ PL-V39-08 reusable eval extraction becomes the main gate before scale-out

after PL-V39-08 eval contracts stabilize
→ PL-V39-09 comparator harness preparation may begin
```

No parallel preparation authorizes production mutation or promotion early.

---


# 14A. Compatibility mapping from v3.8.7 to this baseline

The future sequence is reorganized, not discarded.

| v3.8.7 future block | v3.9 draft disposition |
|---|---|
| `PL-V38-05 Direction-aware context policy + visibility + ContextTrace` | becomes `PL-V39-06 Context, Memory, Visibility, and Handoffs` |
| `PL-V38-06A Research asset reconciliation` | becomes `PL-V39-08A Research asset reconciliation` |
| `PL-V38-06B Poker-derived fixture qualification` | becomes part of `PL-V39-08B/08C Evaluation + qualified behavioral fixtures` |
| `PL-V38-07 Context Compiler experiment` | becomes `PL-V39-09.1 Context Compiler experiment` |
| `PL-V38-08 Safe direction bootstrap orchestration + release` | becomes `PL-V39-09.3/09.5 Safe orchestration + release decision` |

Two capabilities become explicit enough to deserve visible sequencing:

```text
PL-V39-05
Project Shaping + Target Reality

PL-V39-07
Execution Contracts + Skills + Checklists + Routing
```

But the final Context Compiler and orchestration blocks are merged under `PL-V39-09`, so the net future spine grows by only one major block.

This is intentional:

```text
recommendation richness
should increase capability density,
not roadmap branch count.
```


# 15. Dependency reasons

## FIELD → PL-V39-05

Reason:
the new shaping rules should incorporate actual Project Spine handoff field findings rather than bypassing them.

## PL-V39-05 → PL-V39-06

Reason:
context selection needs richer current target/route/claim semantics before optimizing visibility/handoff.

## PL-V39-06 → PL-V39-07

Reason:
skills/execution should consume bounded authoritative packets, not invent another context mechanism.

## PL-V39-07 → PL-V39-08

Reason:
the Eval Core needs a small stable task/skill/checklist/contract surface as its first
consumer, while a large skill/checklist corpus must not scale before the reusable
eval boundary exists.

Therefore:

```text
07 minimal pilot semantics
→ 08 reusable/qualified eval
→ evidence-backed 07 scale-out/correction
```

PL-V39-08A research-asset reconciliation may be prepared read-only earlier.

## PL-V39-08 → PL-V39-09

Reason:
safe orchestration and any Context Compiler candidate must be tested by qualified
behavioral fixtures before product promotion.

Context Compiler itself may fail its comparator without blocking release of the
validated non-compiler path.

---

# 16. Recommendation absorption lineage

The detailed source-by-source ledger is no longer part of the active Roadmap.

Canonical receipt:

```text
docs/design/project-spine/recommendations/archive/ABSORPTION-2026-08-21.md
```

The active design contract is only:

```text
every source RecommendationUnit
→ absorbed into current Roadmap
OR
→ preserved in FUTURE-RESERVE
OR
→ explicitly archived as superseded/rejected
```

No active semantic residue is allowed to depend on reopening the old source
documents during normal planning.

---

# 17. Governance for this current design baseline

This v3.9.3 baseline is accepted as the **current development-design carrier**
for the reorganized project package.

It does not change the product release or authorize implementation.

Maintain these invariants:

```text
1. roadmap/ROADMAP.md is the only current development Roadmap.
2. old Roadmaps move to roadmap/archive/.
3. recommendations/FUTURE-RESERVE.md is not scheduling authority.
4. new Discoveries do not become Recommendations automatically.
5. new Recommendations enter inbox/ or active/ before absorption.
6. absorption follows governance/RECOMMENDATION-ABSORPTION.md.
7. superseded source documents are checked for semantic residue before archive.
8. .planning-lab is research evidence, not current direction authority.
9. the current field gate remains authoritative for immediate implementation sequencing.
```

---

# 18. Current next gate

The documentation/information-architecture reconciliation is complete.

The product Roadmap mainline remains:

```text
CURRENT FIELD GATE
→ PL-V39-05 Project Shaping / Target Reality
→ PL-V39-06 Context / Memory
→ PL-V39-07 Execution Contracts / Skills / Checklists
→ PL-V39-08 Evaluation / Learning / PromptOps
→ PL-V39-09 Context Compiler experiment / Safe Orchestration / Release
```

Do not start PL-V39-05 merely because this document was reorganized.

Immediate product work is still determined by the current field checkpoint and
its accepted reconciliation.

The next Planning Lite recommendation-intake exercise should use the new stable
Discovery / Recommendation / Future Reserve structure and preserve the result
as a behavioral eval fixture for `PL-V39-08`.
