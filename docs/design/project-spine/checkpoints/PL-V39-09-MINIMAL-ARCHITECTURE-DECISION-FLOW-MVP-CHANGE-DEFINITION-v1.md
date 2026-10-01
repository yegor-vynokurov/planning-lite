# PL-V39-09 Minimal Architecture Decision Flow MVP — Change Definition Candidate

Status: CANDIDATE / OWNER REVIEW REQUIRED  
Change ID: `CHG-PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-001`  
Prepared: 2026-09-30

This is a candidate Definition for combined owner review. It does not approve
itself or authorize implementation, testing, 09-G, release, or Roadmap change.

## Problem

Planning Lite has the necessary 09-B architecture-knowledge boundaries and
09-E capability-aware plan compiler, but does not yet prove one compact,
owner-led path from an architecture-sensitive goal to a justified decision,
fitness evidence, and an executor-aware semantic Plan. Without that walking
skeleton, adding broader architecture machinery risks duplicating existing
owners or forcing routine work through heavyweight architecture ceremony.

## Owner-selected intent

Prove exactly one minimal end-to-end Architecture Decision Flow MVP as a delta
within live PL-V39-09. Preserve solution-light intent, simplest sufficient
architecture, human authority at material semantic gates, and uncertainty as
a valid outcome. Architecture labels must not choose technologies, and
implementation topology must not define the initial Ideal.

The user journey is:

```text
GOAL / SELECTED TIER + ONE CRITICAL FLOW + MATERIAL FACTS / HARD CONSTRAINTS
→ explicit architecture drivers
→ 1–3 measurable material scenarios, as applicable
→ at least two credible alternatives for a consequential choice
→ DECISION_ACCEPTED or SPIKE_REQUIRED
→ relevant TARGET / MVP-REFERENCE / TRANSITION distinction
→ material evidence or fitness obligation
→ ordinary semantic Plan
→ existing 09-E executor-aware plan compilation
```

The flow is opt-in for architecture-sensitive work. Routine work remains on
the ordinary Planning Lite path.

## In-scope semantics

### Intent and drivers

Capture the goal and selected tier where available, one critical flow, known
hard constraints, material facts, and project context (`GREENFIELD` or
`BROWNFIELD` where applicable). Record only material architecture drivers.
Each driver identifies its ID, provenance, affected capability or seam, type
(`FUNCTIONAL`, `QUALITY`, `CONSTRAINT`, `RISK`, or `EVOLUTION`), why it matters
architecturally, uncertainty/confidence, and a measurable response or bound
when known. Questionnaire answers are not automatically drivers.

### Scenarios and alternatives

Support one to three material quality, change, failure, or cost scenarios as
applicable. A scenario states stimulus, environment/context, affected
system/asset, required response, and response measure. A material quality
concern must yield at least one measurable scenario; no scenario category is
universally required.

For each consequential decision, capture at least two credible alternatives,
including a simpler credible alternative unless the simpler option is itself
the baseline. For each, record intended benefit, main trade-off, operational
burden, reversibility, and key evidence needed. Do not add a universal score or
arbitrary numeric ranking.

### Decision and uncertainty

The result is exactly one of:

- `DECISION_ACCEPTED`: record the selected alternative, why available evidence
  supports it, the accepted material trade-off, and what is intentionally not
  selected.
- `SPIKE_REQUIRED`: record the missing empirical fact, a bounded evidence
  request/benchmark/spike with a stop condition, and the decision it will
  unlock. Do not force a technology choice or present a hypothesis as fact.

Owner decision authority stays with the existing Project Spine and decision
authorities. The carrier records rationale and references; it does not become
a new decision authority or ADR subsystem.

### Delivery horizons and evolution

Distinguish only relevant parts of `TARGET`, `MVP / REFERENCE`, and
`TRANSITION`. A Target component does not automatically enter the MVP.
For every accepted material architecture decision record:

- `REPLACEMENT_OR_SCALE_RISK`;
- `REOPEN_TRIGGER`;
- `NEXT_TRANSITION`.

An optional `CHEAP_REPLACEABILITY_SEAM` is justified only when volatility,
replacement impact, and coupling risk make preserving that seam now worthwhile.
This Change does not create a general Evolvability/Replaceability Contract.

### Evidence and semantic-plan handoff

Attach at least one practical evidence/fitness route to each material selected
architecture claim: an existing or contract test, static rule, scenario check,
benchmark, load/performance observation, security/trust invariant, manual
review, or bounded spike. Automation is optional when disproportionate.

The accepted record must produce or reference a semantic Plan explicit enough
for existing 09-E. Use the existing capabilities, executor profile, task and
proposal inputs, controlled-discovery contract, and `planning-lite plan-compile`
path. Do not create a parallel plan compiler, rewrite semantic dependencies,
invent decisions, or let compiled executor detail replace the semantic Plan.

### Brownfield minimum

For a brownfield case, initial Ideal/Target reasoning must not silently derive
authority from current repository topology. During bounded reconciliation,
observed reality may contribute sourced facts and classify material
differences, where applicable, as:

- `MATCH / CARRY_FORWARD`;
- `JUSTIFIED_REALITY`;
- `HARD_CONSTRAINT`;
- `MIGRATION / COMPATIBILITY BURDEN`;
- `LEGACY / HISTORICAL ACCIDENT`;
- `UNKNOWN / SPIKE_REQUIRED`.

This is a provenance boundary and bounded reconciliation, not the full 09-C
reality-model system.

## Ownership boundaries

- Use the existing consumer-owned `.planning/project/ARCHITECTURE_OVERVIEW.md`
  as the compact structured carrier and accepted architecture-model location.
- Route users through the existing control surface; any new guide remains
  concise and subordinate to the ROOT_ROUTER.
- Reuse 09-B Ideal Scaffold and Architecture Knowledge ownership contracts;
  do not add a second scaffold path or expand the canonical knowledge pack.
- Reuse existing Goal, Critical Flow, Target, decision, evidence, and semantic
  Plan owners by reference. Do not duplicate their authority in the carrier.
- Preserve 09-E as the only executor-aware plan compiler.
- Do not make the central framework authoritative over project-owned accepted
  decisions or existing project state.

## Explicit deferrals and non-goals

Out of scope: full scale-envelope/trigger framework; full
Evolvability/Replaceability Contract; universal seam-conformance tests;
deployable system manifest; full review-trigger matrix; universal transition
recipe library; Project Doctor; production-readiness evidence gate; full
Deployment Sophistication Ladder; full ADR subsystem; full AI Evaluation
Contract; automatic architecture decision execution; whole-project
orchestration; multi-agent scheduler; workflow engine; LangGraph, Temporal, or
queue substrate selection; 09-G implementation; and 09-H release logic.

This Change does not create a new top-level architecture domain or Roadmap
branch, and does not implement the complete architecture methodology.

## Success criteria for the eventual implementation

The reviewed implementation must demonstrate the following acceptance target:

1. One architecture-sensitive request traverses the complete MVP flow.
2. Drivers are explicit and traceable to source/provenance.
3. A material quality concern produces at least one measurable scenario.
4. A consequential choice has at least two credible alternatives, including a
   simpler credible alternative.
5. No mechanism or technology is selected merely from a project label.
6. Insufficient evidence yields `SPIKE_REQUIRED`, not invented certainty.
7. Target, MVP/Reference, and Transition are distinguishable.
8. Each accepted material decision has replacement/scale risk, reopen trigger,
   and next transition.
9. A cheap replaceability seam is optional and justified.
10. A material claim has a practical evidence/fitness obligation.
11. Brownfield reality does not overwrite initial Ideal reasoning.
12. The result hands off to the existing 09-E plan compilation path.
13. Routine, non-architecture-sensitive work is not forced through this flow.
14. No 09-G orchestration behavior is introduced.
15. One later real field proof completes the flow without inventing unresolved
    architecture decisions.

## Field-proof acceptance

After separate owner review and implementation authorization, use one real
architecture-sensitive case. The proof must trace the owner's question through
drivers, measurable scenarios, alternatives including a simpler one, an
accepted decision or bounded spike, Target/MVP/Transition, evolution mini-fields,
an evidence obligation, a semantic Plan, and existing 09-E compilation. The
exact case may be selected in the reviewed Plan or later owner gate if no
single current candidate is clearly best. This Definition-preparation Change
does not execute the proof.

## Failure and stop semantics

Stop and retain uncertainty when provenance, owner authority, a material fact,
scenario measure, credible alternative, or decision rationale is insufficient.
Use `SPIKE_REQUIRED` only with a bounded evidence request and the decision it
unlocks. Do not silently promote observed topology into Ideal authority, invent
precision, default to a technology, or continue into unrelated architecture
machinery. If the compact carrier cannot express a needed semantic without
duplicating an existing owner, record that as a review finding and stop for
owner adjudication before expanding scope.

## Authorization boundary

This candidate Definition authorizes no product source, template, schema, or
test mutation. Those are only proposed for a later reviewed Plan. It authorizes
no tests, field proof, 09-G, Roadmap rewrite, stage, commit, push, or release.
