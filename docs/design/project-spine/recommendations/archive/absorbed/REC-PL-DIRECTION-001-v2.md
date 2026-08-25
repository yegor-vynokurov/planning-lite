# REC-PL-DIRECTION-001 v2 — Project Spine, Direction Workflows, Recommendation Residue and Lineage-First Planning

**Status:** Proposed for bounded implementation design
**Supersedes:** `REC-PL-DIRECTION-001 — Project Spine, Direction Memory and Recommendation Lifecycle`
**Date:** 2026-08-18
**Evidence base:** Planning Lite Roadmap v3.7 design + `POKER-PROJECT-SPINE-PILOT-001` Steps 1–8 + CHG-0008 planning/calibration observations
**Disposition:** Promote from “field-pilot only” to **bounded Planning Lite implementation candidate**. Do not implement the whole architecture in one change.

---

## 1. Why this revision exists

The first recommendation proposed a Project Spine and explicitly said:

```text
Poker real work
→ project-local Project Spine pilot
→ collect field evidence
→ only then decide whether Planning Lite should implement it
```

That condition has now been met far enough to change the recommendation status.

The Poker pilot exercised the full direction chain:

```text
existing project evidence
→ current-state consistency reconciliation
→ Target-State Explorer
→ Target State calibration
→ Capability Model
→ Current Capability Assessment
→ causal Gap Map
→ Recommendation/Roadmap reconciliation
→ Roadmap synthesis
→ qualitative prioritization
→ selection of a real next Roadmap outcome
→ definition/calibration of a governed Change
```

The result was not merely a planning document. It changed the selected next work from the historically preferred API change to a bounded Bayesian research-protocol change, while preserving old useful ideas without promoting them into current scope.

This is enough evidence to stop treating Project Spine as only a conceptual addendum.

---

# 2. Core architecture remains valid

The v1 architecture is preserved:

```text
TARGET STATE
    ↓
CAPABILITY MODEL
    ↓
CURRENT STATE
    ↓
CURRENT ↔ TARGET
    ↓
GAP MAP
    ↓
ROADMAP
    ↓
RECOMMENDATIONS / DISCOVERIES / DECISIONS
    ↓
GOVERNED CHANGE
    ↓
EVIDENCE
    ↓
RECONCILIATION
    ↙             ↘
CURRENT       TARGET / GAP / ROADMAP / RECOMMENDATIONS
```

The new finding is that the arrows are not mere conceptual relationships.

They correspond to reusable **planning workflows with distinct evidence contracts**.

---

# 3. Field findings promoted from Poker

## FINDING-001 — Direction authority must be discovered before a target is invented

Existing charter/vision/roadmap material may already contain stronger authority than remembered user summaries or stale agent instructions.

Required behavior:

```text
discover direction sources
→ classify authority
→ classify freshness
→ surface conflicts
→ only then infer missing target material
```

Agent inference is draft evidence, not authority.

---

## FINDING-002 — Deliverable class is an early Target-State variable

The same repository can imply radically different roadmaps depending on whether the intended deliverable is:

```text
end-user product
library
service
internal tool
research demonstrator
reference implementation
portfolio artifact
learning project
infrastructure component
```

Poker initially looked like a possible poker assistant. Once classified as a bounded portfolio/research artifact, Telegram, persistent opponent profiles, full game-tree EV and commercial packaging stopped being required target outcomes.

**Planning Lite requirement:** Target-State Explorer must establish deliverable class early.

---

## FINDING-003 — Repository-clean is not planning-consistent

Poker was Git-clean while lifecycle/planning truth was inconsistent.

Required gate:

```text
repository boundary
+
ACTIVE
+
CURRENT_STATE
+
active/completed Change state
+
Roadmap claims
→ CURRENT-STATE CONSISTENCY GATE
```

A Direction workflow must stop and reconcile lifecycle truth before deriving Target↔Current gaps.

---

## FINDING-004 — Target questions need ownership

Open questions must be classified by the layer that owns their resolution:

```text
TARGET_BOUNDARY_QUESTION
CAPABILITY_DESIGN_QUESTION
RESEARCH_QUESTION
```

Only `TARGET_BOUNDARY_QUESTION` blocks Target-State convergence.

A Target State may therefore become a:

```text
PROVISIONAL TARGET BASELINE
```

while design and research questions remain open under specific capabilities.

Target updates then require:

```text
explicit user/authority decision
or
explicit TARGET_STATE_SIGNAL
```

Ordinary implementation discoveries must not silently rewrite the target.

---

## FINDING-005 — Capability assessment needs two axes

A single status such as `PARTIAL` is insufficient.

Poker successfully used:

```text
TARGET COVERAGE:
SATISFIED
PARTIAL
NOT_SATISFIED
UNCERTAIN

EVIDENCE CONFIDENCE:
HIGH
MEDIUM
LOW
```

This prevents:

```text
implementation exists
```

from being confused with:

```text
target capability is adequately demonstrated
```

For a PARTIAL capability, the assessment should explicitly record:

```text
satisfied target properties
missing target properties
evidence limitations
```

---

## FINDING-006 — Gap derivation must compress causes, not enumerate symptoms

Poker had eight PARTIAL capabilities and one NOT_SATISFIED capability, but the Gap Map compressed them into six causal gaps.

Rules validated by the pilot:

```text
PARTIAL capability
≠ automatically one Gap

evidence limitation
≠ automatically a Gap

stale document
≠ automatically a Gap

one causal missing property
→ may affect several capabilities
```

Gap records should distinguish:

```text
PRIMARY capability effect
DEPENDENT capability effect
```

and require outcome-oriented closure conditions.

Example:

```text
good:
supported output semantics consistently distinguish
validated / heuristic / Bayesian / experimental quantities

bad:
rename field X in file Y
```

The first is a Gap. The second is an implementation tactic.

---

## FINDING-007 — Gap is not Roadmap item and Roadmap item is not Change

The pilot validated three distinct planning layers:

```text
Gap
→ what Target property is false

Roadmap outcome
→ what coherent result should become true

Change
→ one governed bounded implementation/research slice
```

One Roadmap outcome may close multiple Gaps while preserving separate Gap closure checks.

One Gap may require multiple Changes.

Change completion therefore must never directly imply Gap closure without reconciliation.

---

## FINDING-008 — Roadmap synthesis may bundle natural outcomes without merging their truth conditions

Poker bundled:

```text
Bayesian study Gap
+
controlled experiment-to-decision Gap
→ one Roadmap outcome
```

and:

```text
supported API Gap
+
strict failure-contract Gap
→ one Roadmap outcome
```

But the individual Gap closure checks remained separate.

This is the correct abstraction:

```text
shared work/evidence
≠ identical semantics
```

Planning Lite should support bundled Roadmap outcomes with preserved Gap identities.

---

## FINDING-009 — Prioritization must defeat historical inertia

Before Project Spine, a small integration API had been the preferred next Poker change.

After Target→Current→Gap reconciliation, the preferred next outcome became a Bayesian research study.

Historical Roadmap order is therefore evidence of prior intent, not an inherited priority.

Prioritization should compare candidate Roadmap outcomes on qualitative dimensions such as:

```text
TARGET_CRITICALITY
PORTFOLIO / USER VALUE
GAP_LEVERAGE
DEPENDENCY_LEVERAGE
EVIDENCE_READINESS
BOUNDEDNESS
RESEARCH_UNCERTAINTY
PREMATURE_FREEZE_RISK
FINAL-DELIVERABLE RELEVANCE
```

Do not require fake numeric precision.

The system must also explicitly test credible alternatives and explain why the selected outcome precedes them.

---

## FINDING-010 — Recommendation decomposition preserved semantic residue

Poker reconciliation decomposed:

```text
12 recommendations
→ 52 semantic units
```

Closed/converted recommendations contained surviving meaning that would have been lost under a binary completion model.

Validated unit states include:

```text
IMPLEMENTED
STILL_OPEN
FUTURE_SEED
DEFERRED
REJECTED
SUPERSEDED
CARRIED_FORWARD
NEEDS_REFRAME
UNCERTAIN
```

Validated parent outcomes include:

```text
COMPLETED
PARTIALLY_REALIZED
CLOSED_WITH_CARRYFORWARD
DEFERRED
SUPERSEDED
REJECTED
UNANCHORED
NEEDS_REFRAME
UNCERTAIN
```

Hard invariant:

```text
all original semantic units
=
implemented
+ rejected
+ superseded
+ carried_forward
+ deferred/future_seed
+ still_open
+ explicit uncertainty/reframe
```

No unit disappears because a Change closed.

---

## FINDING-011 — Future seeds and out-of-target ideas need identity, not scheduling

The Poker reconciliation preserved nine explicit future seeds.

Useful ideas can remain:

```text
OPTIONAL_FUTURE
OUTSIDE_BOUNDED_TARGET
UNANCHORED_BACKLOG
```

without becoming required Roadmap work.

A future seed should have a trigger only when evidence supports a real trigger.

Never invent a schedule merely to make the record look actionable.

---

## FINDING-012 — Historical Change candidate IDs should not be semantically reused

Poker had a long-lived historical candidate identity:

```text
CHG-0007-small-integration-api
```

It was never instantiated, but reusing `CHG-0007` for an unrelated Bayesian change would have made provenance ambiguous.

Required identity rule:

```text
historically meaningful candidate identity
→ may be RETIRED / UNINSTANTIATED
→ do not silently recycle for another subject
```

Stable identity applies even to important uninstantiated planning candidates.

---

## FINDING-013 — Memory visibility tiers worked in practice

Poker reconciliation naturally produced:

```text
ACTIVE_DIRECTION
DEFERRED_VISIBLE
ARCHIVE_INDEXED
UNANCHORED_BACKLOG
```

After Roadmap synthesis, the default memory could shrink to a compact five-row Roadmap + six Gap identities + target/capability indexes.

The full 52-unit recommendation reconciliation and 26-item historical roadmap reconciliation could become `ARCHIVE_INDEXED`.

This demonstrates:

```text
visibility decay
not
information deletion
```

---

## FINDING-014 — Lineage-first retrieval showed adaptive depth, not just smaller context

Context traces showed different historical expansion by workflow stage.

Observed pattern:

```text
Current Capability Assessment
→ 12 capabilities assessed
→ only 1 historical completed-change packet opened
→ 0 recommendation files opened

Gap derivation
→ authoritative Spine artifacts were sufficient
→ no source/history expansion needed

Recommendation/Roadmap reconciliation
→ intentionally expanded all 12 recommendation records
→ only 4 completed-change reviews were required

Roadmap synthesis/prioritization
→ six Spine artifacts were sufficient
→ no source/tests/recommendations/completed changes reopened

real Change planning
→ compact direction context + targeted feasibility reads
→ no recommendation/history replay required
```

This supports a stronger hypothesis than “always read less”:

> **The correct context depth is workflow-stage dependent.**

Project Spine should route history only when the current operation requires it.

---

## FINDING-015 — ContextTrace should become a standard observational output

A lightweight `ContextTrace` is useful for both debugging and future evaluation.

Suggested fields:

```text
starting_artifacts
additional_current_sources
historical_changes_opened
recommendations_opened
reads_judged_unnecessary
missing_context_recovery
fallback_to_semantic_search
```

It should normally be observational, not an optimization target during production work.

Later Campaign evaluation can compare:

```text
correctness
context tokens
historical files opened
reopens
missing-context recovery
operator corrections
```

---

## FINDING-016 — Complex planning prompts are reusable workflow contracts

The Project Spine pilot relied on long, multi-layer prompts that a normal operator should not be expected to author manually.

The reusable unit is not the exact prose prompt.

It is a versioned **Planning Workflow Playbook** containing:

```text
workflow_id
trigger / applicability
authority inputs
required reads
optional expansion rules
semantic procedure
hard guards
output artifact schema
validation contract
stop / human-approval boundaries
handoff contract
ContextTrace policy
```

A concrete prompt should be a projection:

```text
Workflow Playbook
+
relevant Checklists
+
Project Spine context
+
current lifecycle state
+
task-specific parameters
→ AGENT WORK PACKET / runtime prompt
```

This connects Project Spine to the existing Planning Lite Skill/Checklist architecture.

---

## FINDING-017 — Workflow playbooks and checklists are different layers

A playbook describes:

```text
what sequence of reasoning/work to perform
```

A checklist describes:

```text
what must be true / checked / evidenced
```

Example:

```text
PW-DIRECTION-GAP-DERIVATION
→ derive causal gaps from Target and Current

CHK-DIRECTION-GAP-QUALITY
→ every Gap maps to Target
→ evidence limitation alone is not a Gap
→ duplicate causal gaps are consolidated
→ satisfied capabilities are not silently reopened
```

This separation allows playbook prose to remain stable while hard checks evolve.

---

## FINDING-018 — Small semantic stages do not require many manual approvals

The Poker pilot used many explicit conversational prompts because it was a research exercise.

A productized Planning Lite should preserve the semantic stages but automate safe transitions.

Potential orchestration:

```text
inventory
→ consistency gate
→ target draft
→ target calibration
[HUMAN TARGET ACCEPTANCE]
→ current assessment
→ gap derivation
→ recommendation/roadmap reconciliation
→ roadmap synthesis/prioritization proposal
[HUMAN DIRECTION ACCEPTANCE]
→ bounded Change definition
[HUMAN PLAN / READINESS / EXECUTION GATES]
```

Human stops should remain at material authority boundaries, not every deterministic analysis hop.

---

## FINDING-019 — Research-heavy changes benefit from protocol-first planning

Poker's first selected Roadmap outcome contained high research uncertainty.

The safe change shape became:

```text
research protocol first
→ implementation later
→ evidence
→ adoption/non-adoption decision
→ production integration only through a separate governed decision
```

General research capability contract:

```text
study_complete != production_integrated
```

A rigorous negative result may satisfy a research capability.

This should become a reusable Planning Lite research-change playbook.

---

## FINDING-020 — Scientific planning needs anti-leakage and epistemic-role contracts

Calibration of CHG-0008 exposed reusable research rules:

```text
synthetic recovery/sanity
!=
independent model validation

study validity
!=
model performance
!=
production disposition
```

Planning must also distinguish:

```text
development/calibration data
from
final evaluation data
```

and prohibit final evaluation from silently selecting/tuning the candidate after results are visible.

For research protocol changes, closure should require:

```text
one executable primary study design
zero study-critical TBDs
```

Alternatives may remain only as rejected, sensitivity, or conditional variants.

---

# 4. Proposed new artifact: Planning Workflow Playbook

## 4.1. Identity

Suggested object:

```text
PlanningWorkflowPlaybook
```

Minimum fields:

```text
playbook_id
version
title
purpose
applies_when
does_not_apply_when
required_inputs
authority_order
read_strategy
steps
decision_points
human_gates
hard_guards
output_schema
verification
handoff
context_trace
source_lineage
```

## 4.2. Projection rule

Do not maintain giant runtime prompts as canonical truth.

Canonical:

```text
Playbook
Checklist refs
Project Spine refs
Lifecycle state
```

Derived:

```text
AgentWorkPacket / runtime prompt
```

The derived packet is disposable and reproducible.

---

# 5. Initial reusable playbook family validated by Poker

Candidate identities:

```text
PW-DIR-001  Direction Inventory + Current-State Consistency
PW-DIR-002  Target-State Explorer
PW-DIR-003  Target Baseline Calibration
PW-DIR-004  Current Capability Assessment
PW-DIR-005  Causal Gap Derivation
PW-DIR-006  Recommendation + Historical Roadmap Reconciliation
PW-DIR-007  Roadmap Synthesis + Qualitative Prioritization
PW-CHG-001  Gap/Roadmap → Bounded Change Definition
PW-CHG-002  Pre-Approval Plan Calibration
PW-RES-001  Protocol-First Research Change
PW-READY-001 Formal Readiness Audit
```

These should initially exist as versioned workflow/policy assets, not as hardcoded autonomous behavior.

---

# 6. Promotion decision

The previous disposition was:

```text
ACCEPT FOR FIELD PILOT
DEFER CORE IMPLEMENTATION
```

The new disposition is:

```text
FIELD PILOT:
SUCCESSFUL ENOUGH FOR BOUNDED PROMOTION

NEXT:
design and implement a minimal Project Spine substrate
+
versioned Direction Workflow Playbooks
+
RecommendationUnit reconciliation
in small independently reviewable changes

DO NOT:
implement all Direction/Memory/Compiler features at once
```

---

# 7. Recommended implementation boundary

The first Planning Lite implementation should prioritize durable semantics and read-only planning before automation.

Suggested staged order:

```text
1. Project Spine schemas + consistency/authority collectors
2. Direction Workflow Playbook substrate + first read-only playbooks
3. Capability assessment + causal Gap Map
4. RecommendationUnit reconciliation + visibility states
5. Roadmap synthesis/prioritization proposal
6. direction lineage/indexed memory views
7. Context Compiler experiment
8. only later: safe orchestration of multi-stage direction bootstrap
```

Do not begin with a graph database, embeddings, autonomous roadmap mutation, or one giant `analyze project` command.

---

# 8. Required evaluation fixtures

Convert Poker evidence into controlled-realistic cases instead of repeatedly testing on live Poker state.

Recommended case families:

```text
CASE-DIR-AUTHORITY-CONFLICT
stale agent instruction vs newer project charter

CASE-DIR-CURRENT-INCONSISTENT
Git clean but ACTIVE/CURRENT/Change lifecycle disagree

CASE-DIR-TARGET-QUESTION-OWNERSHIP
target blocker vs capability-design vs research question

CASE-DIR-CAPABILITY-EVIDENCE
implementation exists but target evidence remains partial

CASE-DIR-GAP-COMPRESSION
many partial capabilities collapse into fewer causal gaps

CASE-DIR-RECOMMENDATION-RESIDUE
completed/converted recommendation contains surviving units

CASE-DIR-HISTORICAL-PRIORITY
old preferred change must lose priority after gap reconciliation

CASE-DIR-VISIBILITY-ROUTING
history remains retrievable while default context contracts

CASE-RES-PROTOCOL-FIRST
research outcome requires protocol, leakage controls and non-adoption path
```

These fixtures should follow the existing Planning Lite source-integrity / fixture-admissibility discipline.

---

# 9. Success criteria for Planning Lite promotion

A bounded implementation is successful if it can reproduce the useful Poker behavior while reducing operator-crafted prompt burden.

Measure:

```text
direction correctness
Target authority errors
gap causal-duplication rate
recommendation residue loss
future-seed loss
historical-priority inheritance errors
next-change rationale quality
human correction rate
historical files opened
reopened files
input context
missing-context recovery
playbook activation precision
checklist hard-gate compliance
```

A workflow is not successful merely because it produces the expected file names.

---

# 10. Final recommendation

Promote Project Spine from a design-only field experiment to a **first-class Planning Lite roadmap workstream**.

At the same time, avoid encoding the successful Poker prompts as monolithic prompt strings.

The correct architectural promotion is:

```text
Project Spine
→ durable project-direction semantics

Planning Workflow Playbooks
→ reusable semantic procedures

Checklists
→ versioned hard requirements

Context / Direction lineage
→ relevance router

Context Compiler
→ task-specific minimal packet

Eval/Campaign
→ verifies correctness, cost and activation behavior
```

This is the next coherent Planning Lite layer.
