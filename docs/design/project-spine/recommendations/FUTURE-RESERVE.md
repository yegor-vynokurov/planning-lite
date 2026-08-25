# Planning Lite — Future Reserve v1.2
## Deferred recommendation residue and dormant contingency routes

**Status:** `CURRENT DEFERRED-RESIDUE CARRIER / NO IMPLEMENTATION AUTHORITY`
**Date:** `2026-08-21`
**Stable path:** `docs/design/project-spine/recommendations/FUTURE-RESERVE.md`
**Companion:** `docs/design/project-spine/roadmap/ROADMAP.md`

This document exists to satisfy the recommendation-reconciliation invariant:

```text
nothing useful disappears merely because
we want a cleaner Roadmap
```

It is not a second roadmap.

Items here have no current scheduling promise.

Each item requires a concrete trigger before it can be promoted into:
- a Gap;
- a Roadmap outcome;
- a Change;
- or an eval/research experiment.

---

# 1. Status semantics

```text
FUTURE_SEED
useful idea, no current scheduling need

DEFERRED_EXPERIMENT
worth testing after prerequisites exist

WATCH
keep evidence, no design commitment

SUPERSEDED
use successor, retain lineage only

REJECTED_FORM
the problem may be real but this proposed form should not return
without new evidence
```

A trigger firing does not automatically schedule work.
It only makes the item eligible for reconciliation.

---

# 2. Context / Memory future seeds

## FUT-MEM-001 — Semantic retrieval / embeddings after lineage routing

**Status:** `DEFERRED_EXPERIMENT`

Idea:
use semantic retrieval as a second-stage fallback when deterministic lineage/current-state routing is insufficient.

Why not active:
current architecture explicitly prefers authority/lineage first and has not yet evaluated the Context Compiler.

Trigger:

```text
bounded context fixtures repeatedly require relevant history
that deterministic lineage cannot retrieve reliably
```

Then compare:
- lineage only;
- lineage + semantic fallback.

Do not deploy embedding-first memory by default.

Sources:
- v3.7 memory architecture;
- `REC-PL-MEMORY-EFFICIENCY`;
- Context Handoff external research.

---

## FUT-MEM-002 — Episodic timeline + temporal summary tree

**Status:** `FUTURE_SEED`

Idea:
append-only episodic timeline for eval runs/incidents/completed Changes plus rebuildable temporal summaries.

Why not active:
useful but significantly more machinery than current Project Spine/context needs.

Trigger:
operational history becomes too large for current capsules/lineage and time-range retrieval is a demonstrated bottleneck.

Source:
v3.7 Phase 4 memory.

---

## FUT-MEM-003 — Memory utility ledger and evidence-based forgetting

**Status:** `DEFERRED_EXPERIMENT`

Idea:
track retrieval, verified usefulness, conflict, correction and cost; test with/without retrieval before automated demotion/forgetting.

Why not active:
requires mature retrieval instrumentation and enough repeated cases.

Trigger:
PL-V39-06 ContextTrace + PL-V39-08 eval data provide repeated retrieval evidence.

Never delete canonical/admitted truth merely due to age.

---

## FUT-MEM-004 — Semantic memory maintenance automation

**Status:** `WATCH`

Idea:
automatic consolidation/demotion/quarantine based on evidence.

Why not active:
risk of silent information loss and premature self-modification.

Trigger:
manual/controlled memory utility experiments demonstrate stable criteria.

---

# 3. Recommendation / learning future seeds

## FUT-REC-001 — Automated recommendation convergence / cemetery recovery

**Status:** `DEFERRED_EXPERIMENT`

Idea:
tooling that periodically finds:
- stale partially-realized recommendations;
- unanchored accepted units;
- future triggers now satisfied;
- broken successor lineage.

Why not active:
the current self-hosted absorption exercise should first validate the semantics manually.

Trigger:
this v3.9 absorption pass succeeds and at least one additional project uses the same reconciliation protocol.

Source:
v3.7 recommendation convergence.

---

## FUT-REC-002 — Automated recommendation unit extraction

**Status:** `WATCH`

Idea:
LLM/code-assisted decomposition of long recommendation documents into RecommendationUnits.

Why not active:
semantic unit boundaries are easy to invent incorrectly.

Trigger:
manual unit reconciliation becomes a measured bottleneck across multiple projects.

Require human review before unit identity becomes durable.

---

## FUT-REC-003 — Automatic rule curator / selective unlearning

**Status:** `DEFERRED_EXPERIMENT`

Idea:
use rule effect evidence to add/update/merge/remove rules.

Why not active:
high risk of post-hoc attribution and control-plane self-modification.

Trigger:
PL-V39-08 has stable rule/checklist evals, repeated attribution evidence, held-out retention, and rollback.

Preferred curation order remains:

```text
checklist
→ reference
→ rule/playbook
→ skill
```

Source:
`REC-PL-RULE-PLAYBOOK-CURATION`.

---

# 4. Evaluation / PromptOps future seeds

## FUT-EVAL-001 — Full Prompt Garden integration

**Status:** `FUTURE_SEED`

Idea:
make the historical Prompt Garden a second consumer of the reusable Eval Core:

```text
prompt registry
versions
hypotheses
case sets
results
lineage
```

Why not active:
Planning Lite control-plane eval should prove the generic core first.

Trigger:
PL-V39-08B can evaluate at least one non-prompt artifact reliably and Prompt Garden has a concrete active use case.

---

## FUT-EVAL-002 — Broad LLM-judge infrastructure

**Status:** `DEFERRED_EXPERIMENT`

Idea:
general model-judge layer for semantic evals.

Why not active:
deterministic/structured verifiers should remain preferred and judge correlation can create false confidence.

Trigger:
a repeated eval class cannot be graded adequately by deterministic/structured/human-light methods.

Require frozen:
- model;
- prompt;
- rubric;
- evidence policy;
- budget.

---

## FUT-EVAL-003 — Full behavioral eval suite on every commit

**Status:** `REJECTED_FORM`

Problem is real:
control-plane regressions need testing.

Rejected form:
expensive real-agent suite as unconditional per-commit gate.

Current direction:
- deterministic checks frequently;
- targeted agent evals on relevant control changes;
- broader scheduled/on-demand suites.

Reconsider only if cost becomes negligible and flakiness is controlled.

---

## FUT-EVAL-004 — Generalized mutation/fuzzing framework for contracts

**Status:** `DEFERRED_EXPERIMENT`

Idea:
automatically mutate valid contracts:
- extra fields;
- missing fields;
- wrong variants;
- neighboring identity fields;
- forbidden transitions.

Why not active:
nearest-wrong deterministic probes cover current needs without a new framework.

Trigger:
same mutation patterns recur across several contract-heavy projects.

Source:
Weak-Model Execution recommendations.

---

## FUT-EVAL-005 — Schema-driven code generation

**Status:** `WATCH`

Idea:
generate validators/serialization/negative tests from canonical schemas.

Why not active:
could create a second framework and hide semantics in tooling.

Trigger:
multiple manually-maintained exact schemas demonstrate repeated drift that generation would materially reduce.

---

# 5. Scaffold / Template future seeds

## FUT-SCAF-001 — Full verified scaffold self-evolution

**Status:** `DEFERRED_EXPERIMENT`

Idea:
bounded candidate campaigns evolving scaffold components with independent promotion and rollback.

Why not active:
v3.7 design is mature but product need should be re-proven after PL-V39-08 component-level evals.

Trigger:

```text
control-plane eval core stable
+
component candidate experiments repeatedly show measurable benefit
+
manual promotion/rollback semantics proven
```

Then revive v3.7 Phase 6 rather than redesigning it.

---

## FUT-SCAF-002 — Reusable subtractive archetype library

**Status:** `FUTURE_SEED`

Idea:
maintain known-good full archetypes and generate project skeletons by removing unselected capabilities.

Why not active:
Planning Lite does not yet have enough semantically similar target projects to justify maintaining several archetypes.

Trigger:
2–3 projects repeatedly bootstrap the same integrated stack/topology.

Each archetype must have profile regression tests.

---

## FUT-SCAF-003 — Universal non-software Target Skeleton tooling

**Status:** `WATCH`

Concept:
Target Skeleton is intentionally universal.

Potential future tooling for:
- research protocols;
- data pipelines;
- operational workflows;
- documentation chains.

Why not active:
first validate the concept on software/research fixtures without building generalized machinery.

Trigger:
at least two non-software projects independently benefit from the same representation.

---

# 6. Execution / Orchestration future seeds

## FUT-EXEC-001 — Automatic Execution Pattern Router

**Status:** `DEFERRED_EXPERIMENT`

Idea:
derive bounded-loop/TDD/parallel/feedback/background execution pattern automatically from task facts.

Why not active:
PL-V39-07 should first use explicit/advisory routing and collect outcomes.

Trigger:
enough labeled task receipts exist to evaluate router decisions.

No pattern should be selected because it is "more agentic."

---

## FUT-EXEC-002 — General multi-agent team orchestration

**Status:** `DEFERRED_EXPERIMENT`

Idea:
dynamic teams beyond isolated bounded reviewers/explorers.

Why not active:
context/cost/coordination risks are high and many tasks do not need it.

Trigger:
dependency graph shows repeated genuinely parallel lanes where isolated workers materially reduce cost/time without quality loss.

---

## FUT-EXEC-003 — Background/scheduled autonomous work as a Planning Lite primitive

**Status:** `FUTURE_SEED`

Idea:
formal long-running task execution semantics where hosts support it.

Why not active:
host capability varies and core lifecycle should remain portable.

Trigger:
real projects need governed long-running/scheduled execution with evidence and resume semantics.

---

## FUT-EXEC-004 — Full cross-host capability adapter matrix

**Status:** `FUTURE_SEED`

Idea:
explicit mapping of semantic primitives to Claude/Codex/other hosts.

Why not active:
first stabilize the semantic primitives in PL-V39-09.

Trigger:
two or more supported hosts need materially different implementation projections.

---

# 7. Insights / Metrics future seeds

## FUT-INS-001 — Full session-mining Operational Insights service

**Status:** `DEFERRED_EXPERIMENT`

Idea:
mine large session/task histories and synthesize workflow findings.

Why not active:
sampling/coverage/session-classification errors can produce confident nonsense.

Current roadmap only requires transparent receipt aggregation.

Trigger:
sufficient Planning Lite receipts exist with:
- stable session/task identity;
- main vs subagent distinction;
- time windows;
- measured coverage.

Any LLM synthesis must label:
`MEASURED` vs `INFERRED`.

---

## FUT-MET-001 — Single scalar Change Cost score

**Status:** `REJECTED_FORM / MAY REFRAME`

Problem:
Roadmap needs cost comparison.

Rejected current form:
opaque universal scalar or LLM `1–10`.

Current direction:
cost vector + calibrated actuals.

Reconsider only if empirical calibration later supports a transparent aggregate for a specific decision class.

---

## FUT-MET-002 — Expected value / expected Change Cost ratio

**Status:** `FUTURE_SEED`

Idea:
later economic prioritization using calibrated value and cost.

Why not active:
value and cost are intentionally separate until enough calibration data exists.

Trigger:
several comparable Changes have trustworthy cost actuals and outcome evidence.

---

# 8. Lexicon / Clarification future seeds

## FUT-LEX-001 — Automated semantic term-drift detector

**Status:** `DEFERRED_EXPERIMENT`

Idea:
detect when the same project term acquires materially incompatible meanings.

Why not active:
semantic false positives could create bureaucracy.

Trigger:
manual Project Lexicon usage reveals repeated drift that deterministic alias checks cannot catch.

Output should be advisory, never auto-rewrite.

---

## FUT-CLAR-001 — Automated ambiguity challenger

**Status:** `FUTURE_SEED`

Idea:
specialized fresh-context agent that systematically attempts two materially different compliant interpretations.

Why not active:
the determinacy question can initially live in Planning/Readiness prompts/checklists.

Trigger:
manual determinacy checks become frequent and materially costly.

---

# 9. Outcome / Strategy future seeds

## FUT-OUT-001 — Automated Outcome Ladder proposal

**Status:** `WATCH`

Idea:
agent proposes likely L0…Ln value levels from project goals.

Why not active:
Outcome Level is a strategic/human-value construct, easy to overformalize.

Current direction:
optional assisted drafting + explicit human target acceptance.

Trigger:
repeated broad projects show stable ladder patterns.

---

## FUT-STRAT-001 — Automatic contingency route activation

**Status:** `REJECTED_FORM FOR NOW`

Current strategy:
route trigger becoming true makes the alternative eligible for reconciliation.

Rejected:
silent automatic roadmap switch.

Reason:
route changes are strategic and may change value/cost assumptions.

Reconsider only for purely operational equivalent paths with explicit pre-authorization.

---

## FUT-STRAT-002 — Multiple full synchronized roadmaps

**Status:** `REJECTED_FORM`

The useful idea is optionality.

The rejected implementation is maintaining several full roadmaps in parallel.

Current replacement:

```text
one active roadmap
+
compact contingency strategy cards
```

Only expand a dormant route when triggered.

---

# 10. Context Compiler / Memory future seeds

## FUT-CTX-001 — Production Context Compiler beyond experimental promotion

**Status:** `DEFERRED_EXPERIMENT`

The active Roadmap includes a Context Compiler comparator experiment.

This future seed refers only to production promotion/generalization after the experiment.

A losing comparator is a valid outcome and does not block Planning Lite release;
the validated bounded-context path may remain the product path.

Trigger:
PL-V39-09 comparator demonstrates non-inferior correctness and material context benefit across several task classes.

---

## FUT-CTX-002 — Learned context selection policy

**Status:** `WATCH`

Idea:
learn context selection from successful traces.

Why not active:
would place a probabilistic policy before deterministic lineage semantics are proven.

Trigger:
large qualified ContextTrace dataset + stable deterministic baseline.

---

# 11. Planning / behavior-localization future seeds

## FUT-PLAN-001 — Persistent Behavior Localization / State Register Handbook

**Status:** `DEFERRED_EXPERIMENT`

Idea:
maintain a derived index for critical cross-file/state-coupled behaviors with:

```text
behavior cards
source anchors
state-register writers/readers/resets
cold/recovery paths
verification sites
coverage status
```

Why not active:
the older v3.7 design is rich, but a permanent handbook introduces synchronization,
anchor-staleness, and maintenance cost.

Current roadmap keeps only a bounded change-local Behavior/State Coverage Capsule.

Trigger:
several real cross-file/state-coupled Changes repeatedly benefit from the same
behavior/state mappings and rebuilding the capsule becomes a measured cost or
source of missed coverage.

Any persistent handbook remains:
- derived, not canonical;
- live-source revalidated;
- optional for local obvious edits.

Source:
v3.7 Behavior Localization and Harness Handbook.

---

## FUT-PLAN-002 — Typed PlanningProblem + bounded candidate-plan optimizer

**Status:** `DEFERRED_EXPERIMENT`

Idea:
reintroduce the mature v3.7 typed planning layer:

```text
PlanningProblem
→ 2–4 eligible CandidatePlans
→ hard constraints
→ cost/coverage comparison
→ plan consistency
→ explain/analyze
```

Potential later additions:
- memoization of repeated planning subproblems;
- provider-based introspection;
- synthetic plan-selection fixtures.

Why not active:
PL-V39-05 Strategy Portfolio and PL-V39-07 Execution Pattern Router can first
exercise the useful decision semantics without introducing a planner IR/runtime.

Current absorbed principles are:

```text
eligible/hard-gate first
→ cost/value second

plan-shape correctness
!=
outcome correctness
```

Trigger:
manual/advisory routing repeatedly compares the same candidate forms, plan-shape
errors remain material, and qualified eval data is sufficient to test a typed
planner against the simpler baseline.

Source:
v3.7 Typed Planning Problem and Bounded Plan Optimization.

---

# 12. Doctor / diagnostics future seeds


## FUT-DOC-001 — Semantic advisory Doctor

**Status:** `FUTURE_SEED`

Idea:
separate deterministic installation/lifecycle Doctor from advisory semantic checks:
- conflicting authoritative definitions;
- term drift;
- duplicate authority;
- target/current contradiction.

Why not active:
easy to turn Doctor into an open-ended architecture reviewer.

Trigger:
deterministic Doctor remains stable and repeated semantic inconsistencies have precise bounded checks.

Semantic findings remain advisory unless tied to executable material failure.

---

# 13. Memory / graph forms explicitly not current

## FUT-ARCH-001 — Graph database for Project Spine

**Status:** `REJECTED_FORM UNTIL EVIDENCE`

Current typed lineage can remain Markdown/structured fields.

Trigger for reconsideration:
measured lineage/query complexity cannot be handled by current artifacts without material correctness or maintenance cost.

---

## FUT-ARCH-002 — Embedding-first project memory

**Status:** `REJECTED_FORM`

Current direction:
authority/lineage first, semantic retrieval only as fallback experiment.

Do not revive merely because embeddings are available.

---

# 14. Recommendation-process future seeds

## FUT-ABSORB-001 — Productized Recommendation Absorption workflow

**Status:** `DEFERRED_EXPERIMENT`

This current roadmap revision is the first self-hosted fixture.

Potential future managed workflow:

```text
recommendation inventory
→ unit decomposition
→ overlap/contradiction
→ absorb/add-vertebra/future/reject
→ no-residue audit
→ roadmap/future-backlog synthesis
```

Why not immediately implement:
the bounded manual acceptance checklist is now part of current Roadmap practice;
what remains deferred is productized automation, unit extraction assistance, and
managed workflow packaging.

Trigger:
this Planning Lite self-absorption pass and at least one external-project recommendation intake succeed with comparable semantics.

This is the direct learning target of the current exercise.

---

# 15. Superseded/lineage-only sources

These are not future ideas but should not remain active recommendation authorities after v3.9 acceptance.

## SUP-001 — Weak Model Execution v1/v2

**Status:** `SUPERSEDED`

Use:
`REC-PL-WEAK-MODEL-EXECUTION-001-v3`

Retain older versions only for lineage/evidence until archive policy allows removal.

---

## SUP-002 — Older roadmap copies as active priority

**Status:** `SUPERSEDED AS CURRENT PRIORITY`

`v3.7` and `v3.8` proposal remain valuable design/history sources.

Current priority should come only from the accepted newest roadmap.

Do not resurrect old chronological ordering as priority.

---


# 16. Dormant Contingency Route A — Adaptive Scale Route

**Status:** `DORMANT / NO SCHEDULING PROMISE`

This route groups several Future Seeds without turning them into a second Roadmap.

Premise:

```text
the explicit/advisory mainline remains correct
but becomes a measured recurring scaling bottleneck
```

Route-level activation requires:

```text
stable eval baseline
+
actual-cost/context receipts
+
rollbackable explicit baseline
+
at least two coupled recurring scale failures
```

Core candidates:

```text
FUT-INS-001
FUT-PLAN-002
FUT-EXEC-001
FUT-MEM-001
FUT-CTX-002
FUT-REC-001
```

Later candidates:

```text
FUT-DOC-001
FUT-LEX-001
FUT-REC-003
FUT-EXEC-004
```

Route spine:

```text
A0  Diagnose the measured scaling failure
↓
A1  Automate ONE repeated decision surface
↓
A2  Add adaptive context only if context is the evidenced bottleneck
↓
A3  Add adaptive maintenance/diagnostics only after evaluated automation exists
↓
A4  Generalize across hosts/projects only when scale is genuinely organizational
```

Hard invariants:

```text
no automatic strategic route switching
no embedding-first memory
no self-grading promotion
no hidden control-plane mutation
keep explicit baseline + rollback
```

A candidate that fails to beat the explicit baseline is a valid experiment
outcome:

```text
NO PROMOTION
→ RETAIN CURRENT MAINLINE
```

Optional side branch:

```text
FUT-SCAF-001 / FUT-SCAF-002
```

becomes eligible only when several projects repeat the same topology and
scaffold creation itself is the measured bottleneck.

This contingency route is a strategic relationship among Future Seeds.
The individual Future Seed identities/triggers remain authoritative.

---

# 17. How to wake a Future Recommendation

A future item becomes eligible for triage only when:

```text
trigger evidence exists
+
current target still benefits
+
no newer mechanism supersedes it
```

Then classify:

```text
ROADMAP_REFINEMENT
NEW_GAP
LOCAL_TACTIC
EXPERIMENT
REJECT/SUPERSEDE
```

Do not directly create a Change from this backlog.

---

# 18. Safe archival rule after v3.9.3 baseline

Once the v3.9.3 Roadmap absorption ledger and this Future Backlog are explicitly accepted:

1. mark source recommendation units with their destinations;
2. preserve source lineage;
3. archive superseded recommendation versions;
4. archive fully absorbed recommendation files if repository policy permits;
5. keep this Future Backlog as the single active carrier for deliberately deferred residue;
6. periodically reconcile triggers without loading the whole archive into normal context.

The target state is:

```text
few current authoritative design artifacts
+
rich archive
+
one compact future-seed registry
```

not a growing active forest of recommendation documents.
