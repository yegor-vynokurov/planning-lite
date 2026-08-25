# Planning Lite Roadmap v3.9.1 — SECOND-PASS INTEGRATED DRAFT
## Project Spine, Target Reality, Context, Execution Contracts, Evaluation, and Governed Orchestration

**Status:** `DRAFT / SECOND-PASS RECONCILED / RECOMMENDATION-ABSORPTION CANDIDATE / NOT AUTHORITATIVE`
**Date:** `2026-08-21`
**Current authoritative roadmap until explicit acceptance:** `PLANNING-LITE-ROADMAP-v3.8.7.ru.md`
**Current operational checkpoint used:** `PL-V38-CURRENT.md` dated 2026-08-20

This draft is intentionally self-hosted: Planning Lite is using its own recommendation-reconciliation semantics to absorb unanchored recommendations into a new coherent roadmap.

---

# 0. What this draft is trying to achieve

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

This draft therefore applies a strict **anti-hair rule**:

> A recommendation gets a new Roadmap vertebra only if it introduces a genuinely new dependency boundary, owner, and evidence-bearing exit gate.

Otherwise it must:
- strengthen an existing Roadmap block;
- become a cross-cutting invariant/checklist;
- remain a future seed;
- or be rejected/superseded.

---

# 1. Source-of-truth and lineage

## 1.1 Current primary source

The newest roadmap in the supplied source material is:

```text
PLANNING-LITE-ROADMAP-v3.8.7.ru.md
```

It remains authoritative until this draft is explicitly accepted.

v3.8.7 established/completed:

```text
PL-V38-00  central reconciliation
PL-V38-01  Direction foundation
PL-V38-02  Current Capability Assessment + causal Gap Map
PL-V38-03  Recommendation semantic residue + historical reconciliation
PL-V38-04  Roadmap synthesis + prioritization + Change handoff
PL-V38-PREP-01 local-only update safety
```

Its source snapshot leaves:

```text
PILOT-PL-DIRECTION-002
→ current field gate
→ Attempt 002 next in that snapshot

PL-V38-05+
→ intentionally stopped pending field reconciliation
```

This draft does not pretend that later field events occurred unless they are separately reconciled when the draft is adopted.

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

## 1.3 Recommendation sources absorbed by this draft

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


## 1.4 Exact recommendation-source manifest used in this absorption pass

From `design.zip`:

```text
REC-PL-DIRECTION-001-v2.md
REC-PL-DIRECTION-002-v1.md
REC-PL-READINESS-001-v1.md
REC-PL-CONTEXT-HANDOFF-001-v1.md
REC-PL-MATERIALITY-SIMPLICITY-001-v1.md
REC-PL-CHANGE-COST-001-v1.md
REC-PL-WEAK-MODEL-EXECUTION-001-v1.md
REC-PL-WEAK-MODEL-EXECUTION-001-v2.md
REC-PL-WEAK-MODEL-EXECUTION-001-v3.md
REC-PL-WEAK-MODEL-EXECUTION-001-v3-1.md
```

Important source-file note:

```text
REC-PL-WEAK-MODEL-EXECUTION-001-v3-1.md
```

contains the titled recommendation:

```text
REC-PL-EXECUTABLE-TARGET-CONTRACT-001 v1
```

and is treated by semantic title, not by the misleading source filename.

From `active.zip`:

```text
REC-PL-DIRECTION-001-v2.md
REC-PL-LEARNING-LOOP.ru.md
REC-PL-MEMORY-EFFICIENCY.ru.md
REC-PL-CONTROLLED-EVOLUTION.ru.md
REC-PL-RULE-PLAYBOOK-CURATION.ru.md
```

Duplicate `REC-PL-DIRECTION-001-v2` copies are one recommendation lineage, not two recommendation units.

Supporting non-recommendation sources used for reconciliation include:
- v3.7 and v3.8/v3.8.7 roadmaps;
- current operational checkpoint;
- Direction Workflow Playbooks;
- research-asset ownership;
- code-seed companions;
- source/research reviews.

They are evidence or reusable assets, not orphan recommendations requiring their own roadmap destination.


# 2. Recommendation Absorption Protocol v0.1

This is the process being field-tested by this roadmap revision.

## 2.1 Unit-first, not document-first

A recommendation document is a container.

For reconciliation, treat meaningful statements as `RecommendationUnit`s.

One document may become:

```text
unit A → absorbed into current Roadmap block
unit B → cross-cutting checklist
unit C → future seed
unit D → superseded
```

The source recommendation is not "done" merely because one unit was implemented.

## 2.2 Allowed dispositions

Every touched unit must receive exactly one primary disposition:

```text
ABSORB_EXISTING
ADD_VERTEBRA
CROSS_CUTTING
FUTURE_SEED
REJECT
SUPERSEDE
ALREADY_REALIZED
```

## 2.3 New-vertebra test

A recommendation receives a new roadmap block only if all are true:

```text
[ ] It introduces a distinct capability not already owned.
[ ] It has a real dependency relation with neighboring roadmap blocks.
[ ] It has an identifiable owner/work surface.
[ ] It has a verifiable exit gate.
[ ] Folding it into an existing block would hide a material sequencing constraint.
```

If any answer is `NO`, prefer absorption rather than expansion.

## 2.4 Placement determinacy test

Before assigning a material RecommendationUnit to an owner, ask:

> Can two materially different placements both satisfy the current Roadmap text?

Examples:

```text
same rule could live in workflow OR skill OR checklist
Target Skeleton could be created by Direction workflow OR governed Execution
Target Scenario could be canonical project intent OR only an EvalCase
Context Compiler could be optional experiment OR hidden release prerequisite
```

If both placements remain legal and they change authority, sequencing, evidence,
or lifecycle semantics, the absorption is underdetermined.

Resolve ownership before accepting the Roadmap.

Semantic-neutral implementation detail does not require this treatment.

## 2.5 Anti-hair test

Before adding a Roadmap item ask:

> If I remove the recommendation's title, is this actually a new project capability, or merely a rule for doing an existing capability better?

Examples:

```text
Materiality/Simplicity
→ not a stage
→ cross-cutting Planning/Readiness rule

Four-layer Contract Closure
→ not a stage
→ Planning/Readiness/Execution contract

Context Bootstrap Capsule
→ part of Context/Memory

Assumptions Ledger
→ part of Adaptive Planning interaction

Control-plane behavioral eval
→ part of Evaluation/Learning
```

## 2.6 No silent residue

For every source recommendation touched by this revision:

```text
source units
=
absorbed
+ already realized
+ future-seeded
+ rejected/superseded
```

Nothing useful disappears merely because the source file is later archived.

## 2.7 Safe deletion condition for old recommendation files

A source recommendation may be removed from the active recommendation set only after:

```text
1. its useful current units have Roadmap/checklist/skill destinations;
2. all deferred units appear in FUTURE-RECOMMENDATIONS;
3. superseded/rejected units are explicitly recorded;
4. source lineage remains discoverable;
5. no unit is silently unaccounted.
```

This is the criterion by which Planning Lite can eventually delete the current pile of orphan recommendation files safely.

---

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


## 4.8 Control-artifact ownership is explicit

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

This draft preserves the field gate rather than assuming its outcome.

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

## 12.1 Recommendation reconciliation

After material Changes or before roadmap release:

```text
which RecommendationUnits were realized?
which remain?
which became future seeds?
which new field findings appeared?
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
```

This checklist is current practice.
A productized automated absorption workflow remains future work.

Do not require convergence work after every tiny edit.

## 12.2 Actual-cost receipts

Collect opportunistically in normal work.
Do not turn measurement into a project tax.

## 12.3 Operational field fixtures

Poker, Wiki and other real projects remain evidence sources.
Do not force every finding into the roadmap immediately.

## 12.4 Code/research asset check

Run before designing non-trivial new machinery.
Not required for trivial local changes.

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


# 14A. Compatibility mapping from v3.8.7 to this draft

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

# 16. Recommendation absorption ledger

| Source | Primary disposition | Integrated destination |
|---|---|---|
| `REC-PL-DIRECTION-001-v2` | `ALREADY_REALIZED + ABSORB_EXISTING` | completed PL-V38-01..04; residual workflow/context/eval semantics in 05/06/07/08 |
| `REC-PL-DIRECTION-002-v1` | `CROSS_CUTTING / FIELD` | current field gate; authority seams in 06; eval fixtures in 08; orchestration guards in 09 |
| `REC-PL-READINESS-001-v1` | `CROSS_CUTTING` | PL-V39-07 Readiness completeness + residual finding routing |
| `REC-PL-CONTEXT-HANDOFF-001-v1` | `ABSORB_EXISTING` | PL-V39-06; experiment/promotion in 09 |
| `REC-PL-MATERIALITY-SIMPLICITY-001-v1` | `CROSS_CUTTING` | 05/07/08/09 anti-overengineering |
| `REC-PL-CHANGE-COST-001-v1` | `ABSORB_EXISTING` | Roadmap comparison in 05; actual-cost calibration in 08 |
| `REC-PL-WEAK-MODEL-EXECUTION-001-v3` | `ABSORB_EXISTING` | PL-V39-07; eval fixtures in 08 |
| `REC-PL-EXECUTABLE-TARGET-CONTRACT-001-v1` | `ABSORB_EXISTING` | PL-V39-05; eval adapters in 08 |
| `REC-PL-MEMORY-EFFICIENCY` | `ABSORB_EXISTING` | PL-V39-06 |
| `REC-PL-LEARNING-LOOP` | `ABSORB_EXISTING` | PL-V39-08 |
| `REC-PL-CONTROLLED-EVOLUTION` | `ABSORB_EXISTING` | PL-V39-08 |
| `REC-PL-RULE-PLAYBOOK-CURATION` | `ABSORB_EXISTING + FUTURE_SEED` | checklist/rule identity in 07; measured curation in 08; automatic curator deferred |
| `ROADMAP-NOTE-CODE-ASSET-CHECK-v1` | `CROSS_CUTTING` | continuous pre-design rule + PL-V39-08A |
| `RESEARCH-ASSET-OWNERSHIP-v1` | `ABSORB_EXISTING` | PL-V39-08A |
| v3.7 Reusable Prompt/Eval Core | `REACTIVATE / ABSORB_EXISTING` | PL-V39-08B |
| v3.7 Fixture Qualification | `REACTIVATE / ABSORB_EXISTING` | PL-V39-08B |
| v3.7 Skill/Checklist phases | `REACTIVATE / ABSORB_EXISTING` | PL-V39-07 |
| v3.7 semantic/procedural memory | `RECONCILE / ABSORB_EXISTING` | PL-V39-06 |
| v3.7 Behavior Localization / state-register design | `PARTIAL ABSORB + FUTURE_SEED` | optional change-local behavior/state capsule in 07; full persistent handbook deferred |
| v3.7 Typed PlanningProblem / bounded candidate planning | `DECOMPOSED / PARTIAL ABSORB + FUTURE_SEED` | eligible-before-cost in 05/07; plan-shape eval in 08; full typed optimizer/memo deferred |
| v3.7 Execution Environment Contract | `ABSORB_EXISTING` | PL-V39-07 Execution Envelope/preflight |
| v3.7 semantic errors / `next_action` | `ABSORB_EXISTING` | structured blockers in 07; bounded-detour resume in 09 |
| lecture/repository synthesis | `DECOMPOSED / ABSORBED` | Survey/Outcome/Skeleton in 05; memory in 06; routing in 07; eval/insights in 08; host/orchestration in 09 |
| code companion seed documents | `REFERENCE_ONLY` | reusable assets; not roadmap work |

Superseded weak-model recommendation versions `v1/v2` are lineage/history, not active roadmap sources once `v3` is accepted as the consolidated recommendation.

---

# 17. Acceptance criteria for this roadmap revision itself

Before this draft becomes the new canonical roadmap, perform a bounded reconciliation review.

Require:

```text
1. newest source state verified;
2. no active recommendation source silently lost;
3. Future Recommendations document exists for deferred residue;
4. no new stage exists solely because a recommendation had a title;
5. dormant v3.7 eval/skill/memory work is either revived or explicitly deferred;
6. current field gate is not overwritten by a speculative future sequence;
7. small-change lightweight path remains intact;
8. each new major roadmap block has dependency reason + exit gate;
9. placement-determinacy review finds no material unit with two competing owners;
10. Target Skeleton/Target Contract definitions cannot bypass governed Change execution;
11. Context Compiler experiment is not a hidden release prerequisite;
12. skill/checklist pilot cannot scale before reusable eval evidence;
13. contradictions between current v3.8.7 and this draft are explicit;
14. human explicitly accepts before canonical replacement.
```

---

# 18. Proposed next step after second-pass review

The bounded recommendation-absorption acceptance pass has now been performed in:

```text
PL-V39-RECOMMENDATION-ABSORPTION-SECOND-PASS-REVIEW-v1.ru.md
```

Result:

```text
PASS WITH BOUNDED INTEGRATED REVISIONS
```

Do not immediately implement PL-V39-05.

Next gate is explicit human acceptance/revision of the v3.9.1 ownership and
sequencing decisions.

If accepted:

```text
v3.9.1 becomes the current canonical directional baseline
Future Recommendations v1.1 becomes the single active deferred-residue carrier
old recommendation documents may be archived progressively
only after unit-level lineage/disposition receipts
```

Preserve the second-pass review as the first self-hosted fixture for the future
Recommendation Absorption skill/eval.
