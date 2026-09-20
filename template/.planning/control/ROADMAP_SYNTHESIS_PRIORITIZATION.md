# Roadmap synthesis + qualitative prioritization

**Workflow ID:** `PW-DIR-007`
**Mode:** Planning

Use after the accepted Project Spine and current direction-history reconciliation are ready. This workflow turns accepted direction evidence into a compact, outcome-oriented current Roadmap proposal, compares credible alternatives qualitatively, proposes one preferred next Roadmap outcome, and, on a later explicitly authorized turn, records the accepted Roadmap baseline.

This workflow does **not** create a Change, authorize implementation, or rank work by inherited historical order.

## Preconditions

Formal Roadmap synthesis requires all of the following:

- `project/TARGET_STATE.md` status = `ACCEPTED`;
- `project/CAPABILITY_MODEL.md` status = `CURRENT_BASELINE`;
- `assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md` status = `CURRENT`;
- `project/GAP_MAP.md` status = `CURRENT_BASELINE`;
- `assessments/current/DIRECTION_HISTORY_RECONCILIATION.md` status = `CURRENT`;
- reconciliation readiness = `READY_FOR_ROADMAP_SYNTHESIS`;
- no unresolved material Current-State consistency failure.

If a prerequisite is stale, missing, or blocked, stop and route to the owning earlier workflow. Do not repair missing direction by reading historical Roadmap order as current authority.

## Context profile

Start from the accepted/current Project Spine and reconciliation artifacts:

```text
TARGET_STATE.md
CAPABILITY_MODEL.md
CURRENT_CAPABILITY_ASSESSMENT.md
GAP_MAP.md
DIRECTION_HISTORY_RECONCILIATION.md
current ROADMAP.md only as lineage/current-baseline context
```

Treat the reconciliation snapshot as the normal history boundary. Do not reopen broad recommendations, old Roadmaps, completed Changes, or repository code merely to perform prioritization. Expand targeted evidence only when a candidate outcome or comparison criterion cannot be supported from the current artifacts.

Historical order is evidence of prior intent only:

```text
historical Roadmap order != current priority
```

## RoadmapOutcome synthesis

Synthesize a **small** set of coherent candidate outcomes. A RoadmapOutcome describes a durable project result, not a task list, file list, or implementation Change.

Draft candidates use local analysis IDs:

```text
RMO-CAND-01
RMO-CAND-02
...
```

Canonical project Roadmap IDs are minted only when the Roadmap is explicitly accepted. Preserve any already-current canonical Roadmap outcome IDs whose meaning remains materially unchanged.

A candidate outcome records:

- outcome statement;
- Target capabilities advanced;
- direct Gap refs;
- dependent Gap refs, if any;
- recommendation-unit / accepted-direction lineage where material;
- existing foundations to reuse;
- outcome exit condition;
- logical dependencies or gates;
- explicit exclusions / non-goals;
- likely delivery shape;
- applicable CriticalJourney IDs, ordered seam surface, System Walking Skeleton
  or honest-placeholder obligation, and the cheapest adequate proof boundary;
- uncertainty that matters to sequencing.

### Natural Gap bundling

One RoadmapOutcome may address several Gaps only when they form one natural result, evidence chain, public boundary, or decision boundary.

Good bundling evidence includes:

- one deliverable naturally supplies evidence for several Gap closure checks;
- the Gaps share one inseparable user/reviewer-facing contract;
- splitting would duplicate the same protocol, evidence chain, or acceptance decision.

Do **not** bundle merely because Gaps are adjacent, historically listed together, or convenient for one large Change.

Hard boundary:

```text
RoadmapOutcome identity != Gap identity != Change identity
one RoadmapOutcome -> several Gap refs is allowed
Gap closure checks remain independent
RoadmapOutcome completion does not automatically close a Gap
Gap closure does not automatically complete a RoadmapOutcome
```

## Credible alternatives

Before choosing a preferred outcome, compare the preferred candidate with the strongest credible alternatives. Normally compare at least two candidates. If only one candidate is genuinely credible, state why the alternatives are blocked, out of Target, or not yet ready instead of manufacturing fake competition.

Do not use a weighted score or fake numeric precision by default.

Use qualitative evidence such as `HIGH / MEDIUM / LOW` only where it clarifies the tradeoff. Core comparison criteria are:

- `TARGET_CRITICALITY`: how directly the outcome advances required accepted Target capabilities;
- `GAP_LEVERAGE`: how much accepted causal Gap structure it can resolve through one coherent result;
- `DEPENDENCY_LEVERAGE`: whether settling it enables or de-risks other required outcomes;
- `EVIDENCE_READINESS`: whether enough foundations exist to make the outcome actionable without pretending unknowns are solved;
- `BOUNDEDNESS`: whether the result can remain reviewable and resist scope creep;
- `UNCERTAINTY`: material design/research unknowns that affect sequencing;
- `PREMATURE_FREEZE_RISK`: risk of freezing an interface/model/architecture before necessary evidence exists.

Add a context-specific criterion only when the accepted Target or a real external constraint makes it decision-relevant. Examples include safety criticality, deadline/external dependency, migration risk, or portfolio/publication value. Do not create criteria merely to justify a preferred answer.

Explicit user timing, regulatory, operational, or external dependency constraints may override the default preference. Record the override and its authority.

## Qualitative prioritization

Choose the preferred next Roadmap outcome from the accepted evidence, not from historical sequence position, easiest implementation, agent familiarity, or largest file diff.

The draft must state:

1. the preferred candidate;
2. why it is preferred now;
3. why the strongest credible alternatives do not precede it;
4. what the preferred outcome deliberately excludes;
5. whether it is likely to require one or several bounded Changes;
6. the proposed sequence positions for the accepted outcome set.

Canonical sequence labels are:

- `NOW`: exactly one preferred open outcome when direction is actionable;
- `NEXT`: zero or one likely successor when evidence supports a real ordering relation;
- `LATER`: required outcomes without a justified total order;
- `FINAL_GATE`: review/acceptance outcome that depends on preceding required outcomes;
- `DEFERRED`: explicitly postponed or non-current outcomes preserved without current priority.

Do not impose an order among `LATER` outcomes without evidence.

## Research-heavy outcomes

For a research-heavy candidate, explicitly decide whether protocol-first composition is necessary.

Use protocol-first when scientific validity, epistemic roles, evaluation design, decision rules, or evidence interpretation must be frozen before implementation evidence can be judged. Preserve:

```text
study_complete != production_integrated
synthetic recovery != independent validation
study validity != model result != production disposition
```

A rigorous negative or non-adoption result may satisfy a research Roadmap outcome when the accepted exit condition is a controlled evidence-backed decision.

Do not force protocol-first onto routine engineering outcomes.

## Draft output

Use `.planning/assessments/ROADMAP_SYNTHESIS_TEMPLATE.md` to write:

```text
.planning/assessments/current/ROADMAP_SYNTHESIS.md
```

During synthesis:

- assessment status = `DRAFT`;
- canonical `project/ROADMAP.md` remains unchanged;
- no canonical Roadmap outcome ID is minted for a new candidate;
- no Change is created or selected.

The draft ends with exactly one readiness verdict:

- `READY_FOR_DIRECTION_ACCEPTANCE`: one preferred outcome and a coherent sequence proposal are supported, alternatives are compared, and uncertainty is bounded;
- `BLOCKED`: material authority, evidence, dependency, or candidate-boundary uncertainty prevents a responsible current Roadmap decision.

Stop the turn after the DRAFT synthesis. Ask the user to accept, revise, defer, or reject the direction proposal.

## Acceptance turn

Only explicit user acceptance authorizes canonical Roadmap mutation.

On a later authorized turn using this same workflow:

1. preserve materially unchanged existing canonical Roadmap outcome IDs;
2. mint stable canonical IDs for accepted new outcomes using the project's Roadmap ID convention (default `RM-NNNN`);
3. update `project/ROADMAP.md` using the current managed pristine schema when practical;
4. set Roadmap status = `CURRENT_BASELINE`;
5. record acceptance authority/evidence and baseline date;
6. record exactly one `NOW` outcome when actionable, plus justified `NEXT`, unordered `LATER`, `FINAL_GATE`, and `DEFERRED` outcomes as applicable;
7. mark the synthesis assessment status = `CURRENT` and record the canonical IDs assigned;
8. preserve Gap identities and independent Gap closure checks;
9. do not create or activate a Change.

If the user accepts only part of the proposal, record only the accepted current baseline and leave unresolved candidates out of canonical priority unless explicitly `DEFERRED`.

## Bounded-Change handoff

After a Roadmap baseline is `CURRENT_BASELINE`, the next turn may use existing `CHANGE_DEFINITION.md` for the accepted `NOW` outcome.

The handoff supplies:

- exact source Roadmap outcome ID;
- direct/dependent Gap refs relevant to the bounded slice;
- exact source recommendation units when they fall inside the proposed Change scope;
- outcome exit condition and exclusions;
- likely delivery shape / protocol-first constraint where applicable.
- applicable CriticalJourney IDs and exact carrier lineage;
- System Walking Skeleton or honest-placeholder obligation;
- unresolved no-path visibility in candidate fields rather than silent omission;
- downstream Change proof obligations for the journey state and first broken seam.

A RoadmapOutcome may require several governed Changes. Therefore:

```text
Change completion != RoadmapOutcome completion
Change completion != Gap closure
```

`CHANGE_DEFINITION` must bound one reviewable contribution and must not imply whole-outcome coverage unless the approved scope and evidence genuinely support it.

## Stop boundary

Stop after the DRAFT synthesis, or after an explicitly authorized Roadmap acceptance update. Do not continue into `CHANGE_DEFINITION` in the same turn. Do not scaffold a Change, start planning/execution, reopen Poker automatically, or continue into PL-V38-05.
