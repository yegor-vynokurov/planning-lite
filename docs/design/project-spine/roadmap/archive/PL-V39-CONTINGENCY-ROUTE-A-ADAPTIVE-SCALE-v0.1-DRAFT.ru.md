# Planning Lite — Contingency Route A
## Adaptive Scale Route
### Compact strategic reserve, not a second roadmap

**Status:** `DRAFT / DORMANT CONTINGENCY ROUTE / NO IMPLEMENTATION AUTHORITY`
**Date:** `2026-08-21`

**Companions:**
- `PLANNING-LITE-ROADMAP-v3.9.1-SECOND-PASS-DRAFT.ru.md`
- `PLANNING-LITE-FUTURE-RECOMMENDATIONS-v1.1-SECOND-PASS-DRAFT.ru.md`

---

# 0. Purpose

This document is deliberately **not** a second Planning Lite roadmap.

It is a compact reserve strategy that may become eligible for reconciliation if the current mainline strategy reaches a demonstrated scaling ceiling.

Current mainline philosophy:

```text
explicit semantics
→ bounded artifacts
→ deterministic lineage
→ advisory/manual routing first
→ qualified evals
→ automation last
```

Contingency Route A asks:

> What if this approach remains correct but becomes too expensive to operate across many projects, tasks, agents, hosts, or accumulated histories?

The reserve strategy is then:

```text
MEASURE THE SCALING FAILURE
        ↓
AUTOMATE ONLY THE REPEATED DECISION SURFACES
        ↓
KEEP QUALIFIED BASELINES AND ROLLBACK
        ↓
MOVE FROM EXPLICIT ADVISORY CONTROL
TO EVIDENCE-CALIBRATED ADAPTIVE CONTROL
```

The route changes **how Planning Lite scales**, not its authority model or product goal.

---

# 1. Why this route exists

The Future Recommendations backlog contains a coherent cluster that should not all be scheduled now, but together form a plausible alternative strategy.

The cluster includes:

```text
FUT-INS-001   Operational Insights service
FUT-PLAN-002  Typed PlanningProblem + bounded optimizer
FUT-EXEC-001  Automatic Execution Pattern Router
FUT-MEM-001   Semantic retrieval fallback
FUT-CTX-002   Learned context selection
FUT-REC-001   Automated recommendation convergence
FUT-REC-003   Rule curator / selective unlearning
FUT-DOC-001   Semantic advisory Doctor
FUT-LEX-001   Semantic term-drift detector
FUT-EXEC-004  Cross-host capability adapter matrix
```

These ideas share one strategic premise:

> repeated manual/advisory decisions can eventually become measurable enough to automate safely.

They therefore form a meaningful contingency route.

---

# 2. What this route is NOT

It is not:

```text
"turn on all future automation"
```

It is not:

```text
"the main roadmap failed, so replace it"
```

It is not:

```text
"build a self-improving agent framework"
```

It is not automatic route switching.

It does not authorize:
- production mutation;
- autonomous strategic reprioritization;
- automatic rule promotion;
- embedding-first memory;
- unrestricted multi-agent teams.

A trigger firing means only:

```text
ROUTE A ELIGIBLE FOR RECONCILIATION
```

Human/Planning authority still decides whether to activate any part.

---

# 3. Strategic contrast with the current mainline

## Mainline

Optimize for:

```text
clarity
auditability
small explicit mechanisms
manual/advisory decisions
deterministic routing where possible
automation only after proof
```

## Contingency Route A

Optimize for:

```text
scale
repeated decision automation
cross-project reuse
adaptive context/routing
lower recurring coordination cost
```

The reserve route should activate only when the mainline's explicitness becomes a **measured operational bottleneck**, not because automation looks attractive.

---

# 4. Entry prerequisites

The route must not activate before Planning Lite has a trustworthy baseline.

Minimum prerequisites:

```text
[ ] PL-V39-08 Reusable Eval Core is stable enough to compare candidates.
[ ] Representative behavioral regression fixtures exist.
[ ] Change Cost / actual receipts are captured.
[ ] ContextTrace or equivalent context-use evidence exists.
[ ] Current deterministic/advisory mechanisms have known performance.
[ ] Rollback to the explicit baseline is possible.
[ ] Candidate automation cannot modify its own evaluator/promotion gate.
```

Without these, there is nothing reliable to optimize against.

---

# 5. Activation triggers

Activation requires **evidence of recurring scale friction**.

One isolated inconvenience is insufficient.

Candidate trigger families:

## T1 — Planning decision repetition

Repeated Changes require substantially the same:

```text
candidate-plan comparison
route eligibility check
cost/coverage comparison
```

and manual/advisory planning becomes a measured recurring cost.

Relevant future seed:

```text
FUT-PLAN-002
```

---

## T2 — Context selection ceiling

Bounded lineage/capsule routing repeatedly either:

```text
misses required relevant context
OR
loads materially too much context
```

across qualified task classes.

Relevant seeds:

```text
FUT-MEM-001
FUT-CTX-002
```

---

## T3 — Execution-routing repetition

Humans/strong models repeatedly select the same execution pattern from the same observable task facts.

Relevant seed:

```text
FUT-EXEC-001
```

---

## T4 — Learning/recommendation maintenance ceiling

The recommendation/future backlog becomes large enough that manual reconciliation repeatedly misses:

```text
satisfied triggers
stale partially-realized units
broken successor lineage
duplicate active rules
```

Relevant seeds:

```text
FUT-REC-001
later FUT-REC-003
```

---

## T5 — Diagnostic ambiguity at scale

Semantic contradictions/term drift become frequent enough that manual review is a recurring cost.

Relevant seeds:

```text
FUT-DOC-001
FUT-LEX-001
```

---

## T6 — Host projection friction

Multiple supported agent hosts repeatedly require different capability mappings and projection drift becomes material.

Relevant seed:

```text
FUT-EXEC-004
```

---

# 6. Activation threshold

Do not activate the whole route because one trigger fires.

Use a bounded rule:

```text
one trigger
→ local experiment candidate

multiple coupled triggers
→ consider activating Contingency Route A as a strategic route
```

A route-level activation should normally require:

```text
at least two coupled scaling failures
+
measured recurring cost or escaped error
+
stable eval baseline
```

Example:

```text
context-selection misses
+
execution routing repeatedly consumes strong-model review
```

may justify a broader adaptive-control route.

---

# 7. Route spine

The route is intentionally short.

## A0 — Scale Diagnosis

Use existing receipts/evals before building new machinery.

Establish:

```text
what is actually failing to scale?
frequency
cost
error class
affected task/project classes
current baseline
```

Candidate support:

```text
FUT-INS-001
```

But start with deterministic receipt aggregation before full session-mining.

### Exit

One or more repeated scaling problems are evidenced and bounded.

Otherwise:

```text
RETURN TO MAINLINE
```

---

## A1 — Automate one repeated decision surface

Choose the smallest proven bottleneck.

Examples:

### Planning bottleneck

```text
FUT-PLAN-002
Typed PlanningProblem / bounded candidate comparison
```

### Execution-routing bottleneck

```text
FUT-EXEC-001
Automatic Execution Pattern Router
```

### Recommendation-maintenance bottleneck

```text
FUT-REC-001
Recommendation convergence tooling
```

Do **not** implement all three.

### Comparator requirement

Every candidate is compared against the current explicit/advisory baseline.

Require:

```text
non-inferior correctness/safety
+
material recurring-cost benefit
```

### Exit

One automated decision surface is proven, rejected, or rolled back.

A failed candidate is a valid route outcome.

---

## A2 — Adaptive Context only if context is the evidenced bottleneck

If lineage/capsule selection itself is the scale ceiling:

```text
deterministic lineage baseline
        ↓
semantic fallback experiment
        ↓
only later learned selection
```

Sequence:

```text
FUT-MEM-001
before
FUT-CTX-002
```

Never reverse this ordering.

### Comparator arms

Example:

```text
A deterministic lineage/capsule
B A + semantic fallback
C learned policy candidate
```

### Promotion

Requires:

```text
non-inferior correctness
no authority regression
material context/retrieval benefit
qualified held-out tasks
rollback
```

Embedding-first or learned-first memory remains rejected.

---

## A3 — Adaptive maintenance / diagnostics

Only after evaluated automation exists.

Possible surfaces:

```text
recommendation convergence
semantic drift advisory
semantic Doctor advisory
rule effect measurement
```

Candidate order:

```text
FUT-REC-001
→ FUT-LEX-001 / FUT-DOC-001
→ only much later FUT-REC-003
```

Automatic rule curation is the last step because it changes the control plane.

### Promotion rule

No automatic curator may:
- modify its own eval;
- modify its promotion rule;
- remove canonical truth without governed evidence;
- bypass independent review.

---

## A4 — Cross-project / cross-host generalization

Only if scale is now organizational rather than local.

Candidates:

```text
FUT-EXEC-004
cross-host capability matrix
```

Potentially later:

```text
FUT-EXEC-002
multi-agent teams
```

but only when real dependency graphs repeatedly demonstrate useful parallelism.

The goal is not "more agents."

The goal is:

```text
same semantic Planning Lite
→ reliable projections across hosts
```

---

# 8. Optional terminal branch: verified scaffold evolution

This is **not** part of the default route spine.

If repeated projects share stable topologies and component evals are mature, a side branch may become eligible:

```text
FUT-SCAF-001
verified scaffold self-evolution

FUT-SCAF-002
subtractive archetype library
```

Trigger:

```text
same integrated topology reused across 2–3 projects
+
manual skeleton creation is recurring cost
+
profile regression tests exist
```

This is a topology-reuse contingency, not the general adaptive-scale route.

Do not activate it merely because the main route encounters planning/context friction.

---

# 9. Explicitly excluded future seeds

The following do NOT belong to Route A's default spine.

## Memory timeline / forgetting

```text
FUT-MEM-002
FUT-MEM-003
FUT-MEM-004
```

These solve long-history memory maintenance, not the same immediate scale problem.

They may later become a separate Memory Scale branch if their triggers fire.

## Prompt Garden

```text
FUT-EVAL-001
```

It is a consumer of Eval Core, not a fallback strategy for Planning Lite.

## Broad LLM judge / fuzzing / codegen

```text
FUT-EVAL-002
FUT-EVAL-004
FUT-EVAL-005
```

These are eval implementation options, not strategic route steps.

## Outcome automation

```text
FUT-OUT-001
```

Strategic value definition should remain human-governed unless separate evidence later justifies assistance.

## Automatic route switching

```text
FUT-STRAT-001
```

Still rejected.

The existence of this route does not change that.

---

# 10. Placement determinacy check

Question:

> Could this same future cluster reasonably form a second full roadmap instead?

Yes structurally, but doing so would create duplicated current-state, target, execution, and eval planning.

That placement changes maintenance and authority semantics.

Therefore:

```text
FULL SECOND ROADMAP
→ reject

COMPACT CONTINGENCY ROUTE CARD
→ accept
```

Question:

> Could scaffold/template evolution be merged into the same route?

Only superficially.

It solves:

```text
repeated topology/bootstrap cost
```

whereas Route A primarily solves:

```text
repeated planning/context/routing/maintenance decision cost
```

Because triggers and owners differ, scaffold evolution remains an optional side branch.

This closes the placement ambiguity.

---

# 11. Route invariants

Even after activation, preserve:

```text
human authority at strategic gates
qualified eval before promotion
current explicit baseline retained
rollback
no self-grading promotion
no automatic strategic roadmap switch
no opaque scalar cost as sole decision
no embedding-first authority
no hidden control-plane mutation
```

The contingency route changes the mechanism, not the governance constitution.

---

# 12. Route success criteria

Route A is successful if it produces one or more proven adaptive mechanisms that:

```text
reduce repeated operating cost
OR
reduce escaped errors
OR
reduce context/tool burden
```

while remaining:

```text
non-inferior on correctness
non-inferior on authorization
auditable
rollbackable
```

It does **not** need to automate every future seed.

A valid success might be only:

```text
typed planning comparator works;
everything else remains explicit.
```

---

# 13. Route failure / return condition

Return to the current explicit mainline when:

```text
automation benefit is small
candidate increases hidden complexity
eval variance is too high
authority becomes harder to audit
maintenance cost exceeds saved cost
behavior becomes host/model-fragile
```

The route must be able to terminate with:

```text
NO PROMOTION
→ RETAIN CURRENT EXPLICIT MECHANISM
```

That is a successful experiment outcome, not strategic failure.

---

# 14. Minimal strategy card

```yaml
route_id: PL-CONTINGENCY-A
name: Adaptive Scale Route
status: dormant

optimizes_for:
  - recurring operating cost
  - cross-project scale
  - repeated decision automation

premise: >
  Planning Lite's explicit/advisory mechanisms remain correct but become
  a measured recurring bottleneck at scale.

prerequisites:
  - stable eval baseline
  - actual-cost receipts
  - rollbackable explicit baseline
  - context/decision traces where relevant

activation:
  route_level:
    - at_least_two_coupled_scaling_triggers
    - repeated_measured_cost_or_error
    - qualified_comparator_possible

first_action:
  - diagnose_scale_failure
  - automate_only_one_repeated_decision_surface

core_candidates:
  - FUT-INS-001
  - FUT-PLAN-002
  - FUT-EXEC-001
  - FUT-MEM-001
  - FUT-CTX-002
  - FUT-REC-001

later_candidates:
  - FUT-DOC-001
  - FUT-LEX-001
  - FUT-REC-003
  - FUT-EXEC-004

side_branch:
  - FUT-SCAF-001
  - FUT-SCAF-002

forbidden:
  - automatic_strategic_route_switch
  - embedding_first_memory
  - self_grading_promotion
  - full_parallel_second_roadmap

return_condition: >
  Candidate automation does not beat the explicit/advisory baseline on
  material cost/error reduction without correctness or authority regression.
```

---

# 15. Recommended relationship to the Future Backlog

Do not remove the individual Future Recommendation entries.

Instead add one lightweight grouping field or route annotation:

```text
contingency_route:
  PL-CONTINGENCY-A
```

to the relevant entries.

Reason:

```text
Future Recommendation
→ preserves unit identity + trigger

Contingency Route
→ preserves strategic relationship among several units
```

Neither replaces the other.

This provides optionality without rebuilding a second roadmap.

---

# 16. Recommendation for the current v3.9.1 draft

Do not add Route A as another PL-V39 roadmap stage.

At most add one pointer under Strategy Portfolio / Future Recommendations:

```text
Dormant contingency:
PL-CONTINGENCY-A — Adaptive Scale Route

Eligible only after measured scale friction and stable eval baselines.
```

That is sufficient.

The active roadmap remains one roadmap.
