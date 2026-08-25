# Poker Project Spine pilot — normalized operator commands v1

**Purpose:** preserve the tested sequence and instruction structure used during the Poker field pilot.
**Status:** source evidence / operator library; not a verbatim transcript and not released runtime behavior.

The original pilot happened through a sequence of conversational commands. The exact chat wording is less important than the semantic contract each command enforced. This document preserves normalized forms so the sequence is not lost and can be projected into managed Planning Lite workflows.

---

# Command 1 — Direction inventory and consistency gate

Use when an existing project's direction/history may be stale or inconsistent.

```text
Inspect the project's current direction and lifecycle before proposing new work.

Read the highest-authority direction sources, CURRENT_STATE, ACTIVE, Roadmap,
and the active/completed Change index. Verify the repository/Git boundary.

Classify each direction source by authority and freshness. Surface conflicts.

Run a Current-State Consistency Gate:
repository truth + ACTIVE + CURRENT_STATE + Change lifecycle + Roadmap claims.

Git-clean is not sufficient evidence of planning consistency.

If material inconsistency exists, stop direction derivation and produce a
bounded reconciliation requirement. Do not invent Target State yet.

Return:
- direction authority map;
- freshness/conflicts;
- consistency verdict;
- safe next stage.

Do not create a Change.
Do not prioritize work.
```

---

# Command 2 — Target-State Explorer

```text
Build a Target-State draft from authority-backed project evidence.

Determine the final deliverable class early: product, library, service,
research demonstrator, portfolio artifact, reference implementation, etc.

Cover:
purpose, audience, journeys, function, correctness/verifiability,
failure/recovery, data/source of truth, safety/misuse, observability,
performance/cost, operability, API/integration, evolution, human control,
and explicit non-goals.

For every Target claim label its source:
USER_DECISION / EXISTING_DIRECTION / REPOSITORY_EVIDENCE / INFERRED / UNRESOLVED.

Do not treat current architecture or historical aspiration as automatic Target.
Ask only high-value unresolved questions.

Return TARGET_STATE_DRAFT and a draft Capability Model.
Do not canonicalize or prioritize yet.
```

---

# Command 3 — Target calibration / question ownership

```text
Calibrate the Target draft without broadening implementation scope.

Classify every unresolved question as exactly one of:
TARGET_BOUNDARY_QUESTION
CAPABILITY_DESIGN_QUESTION
RESEARCH_QUESTION

Only TARGET_BOUNDARY_QUESTION blocks Target convergence.
Attach design/research questions to their capability owner.
Remove accidental implementation detail from Target.
Verify explicit non-goals.

If target-boundary questions reach zero, mark the result as a
PROVISIONAL_TARGET_BASELINE.

Add a flow-back rule: Target changes later only through explicit authority or
an explicit TARGET_STATE_SIGNAL.

Return the calibrated Target + Capability Model and unresolved-question map.
Stop for human Target acceptance.
```

---

# Command 4 — Current Capability Assessment

```text
Assess Current State against the accepted/provisional Target Capability Model.

For each capability record two independent dimensions:
Coverage = SATISFIED / PARTIAL / NOT_SATISFIED / UNCERTAIN
EvidenceConfidence = HIGH / MEDIUM / LOW

For PARTIAL, explicitly separate:
- satisfied target properties;
- missing target properties;
- evidence limitations.

Use current code/tests/docs/evidence. Do not infer satisfaction from module,
Roadmap, Recommendation or completed-Change titles.

Expand historical L1/L0 evidence only when current evidence cannot establish a
material claim.

Do not derive Gaps, priorities or the next Change in this stage.

Return CURRENT_CAPABILITY_ASSESSMENT.
```

---

# Command 5 — Causal Gap derivation

```text
Derive the minimum causal Gap Map from Target + Current Capability Assessment.

A Gap is a material Target property that is not currently demonstrated.

Do not create one Gap per PARTIAL capability.
Do not turn evidence limitations, stale documents, uncertainty, old
recommendations or optional enhancements into automatic required Gaps.

Cluster missing properties by common cause.
Distinguish PRIMARY and DEPENDENT capability effects.
Consolidate duplicate symptoms while preserving separate closure criteria where
semantics differ.

Each Gap must have:
- Target lineage;
- current evidence;
- missing target property;
- outcome-oriented closure condition;
- evidence required for closure;
- dependencies/questions.

Do not prioritize.
Return GAP_MAP_DRAFT.
```

---

# Command 6 — Recommendation + historical Roadmap reconciliation

```text
Now intentionally expand historical planning context.

Read the Recommendation registry and historical Roadmap material.

Decompose each recommendation into semantic units and account for every unit.
Classify units as implemented, still open, future seed, deferred, rejected,
superseded, carried forward, needs reframe or uncertain.

Map each surviving unit to:
current Gap / Target signal / local tactic / optional future /
outside bounded Target / unanchored backlog.

Never infer that a completed Change completed the entire Recommendation.
Preserve future seeds without scheduling them unless a real trigger exists.

Reconcile historical Roadmap items with dispositions such as:
KEEP / REFRAME / SPLIT / MERGE_CANDIDATE / DEFER / COMPLETE /
RETIRE_FROM_BOUNDED_TARGET / UNCERTAIN.

Run orphan checks:
Gap without Roadmap coverage; Recommendation without current Gap; historical
item without current Target support; residue loss; duplicate units.

Historical Roadmap order is not current priority.
Return recommendation and Roadmap reconciliation artifacts.
```

---

# Command 7 — Roadmap synthesis + qualitative prioritization

```text
Using only the accepted Target, Current assessment, Gap Map and reconciled
planning history, synthesize a compact current Roadmap.

Prefer a small number of coherent Roadmap outcomes. Allow one outcome to cover
multiple natural Gaps, but preserve each Gap's separate closure identity.

Identify only real logical dependencies.

Compare candidate outcomes qualitatively using:
Target criticality, final-deliverable value, Gap leverage, dependency leverage,
evidence readiness, boundedness, research uncertainty, premature-freeze risk,
and relevant user/release/publication value.

Do not inherit historical priority automatically.
Do not use fake numeric precision by default.
Test credible alternatives and explain why the selected outcome precedes them.

Select exactly one preferred next Roadmap outcome.
Do not create a Change yet.
Stop for human direction acceptance.
```

---

# Command 8 — Accepted Roadmap outcome → bounded Change definition

```text
Define one bounded Change from the accepted preferred Roadmap outcome.

Preserve lineage:
RoadmapOutcome → Gap(s) → Capability(s) → RecommendationUnit(s)/Evidence.

Decide whether the outcome needs one Change, several Changes, or a research
protocol first.

Specify exact in-scope / out-of-scope boundaries, acceptance criteria,
evidence requirements and verification.

Do not recycle a historically meaningful uninstantiated Change ID for a new
subject.

Create the standard Change planning packet.
Implementation remains unauthorized.
```

---

# Command 9 — Pre-approval plan calibration

```text
Review the drafted Change plan for material methodology/governance weaknesses
before approval.

Preserve the accepted scope and structure.
Patch planning artifacts only.

Check especially:
- exact execution/Git boundary;
- evidence/source adequacy;
- leakage/evaluation fairness for research;
- ambiguous closure criteria;
- options menus that leave critical design decisions to implementation;
- hidden production integration;
- AC ↔ task ↔ verification traceability.

For research protocol changes require one executable primary design and zero
study-critical TBDs at protocol closure.

Return READY_FOR_USER_AUTHORIZATION or NEEDS_WORK.
Do not implement.
```

---

# Command 10 — Formal readiness

```text
After explicit plan approval, run a formal readiness audit.

Verify:
- expected source/base identity;
- clean tracked boundary;
- dedicated execution branch transition;
- scope completeness;
- AC traceability;
- dependencies;
- protected paths;
- verification availability;
- authorization boundaries.

For research changes also verify that the evaluation source supports the
scientific claim, same-model synthetic recovery is not mislabeled as independent
validation, and leakage controls exist.

Return exactly READY or NOT_READY with blockers.
Formal readiness does not authorize implementation.
```

---

# Command 11 — Research completion scientific review

```text
At Verification, review the actual protocol/result semantically, not only by
checkbox presence.

Check mathematical definitions, non-degenerate baselines, metric scale,
uncertainty procedure, leakage boundaries, mutually exclusive decision rules,
and whether claimed evidence supports the claimed conclusion.

Separate:
study validity != model result != production disposition.

If fixable scientific issues remain inside approved scope, use a bounded
completion-review amendment rather than opening an unrelated new Change.

Do not close until requirements/checklist/review records reflect the verified
state.
```

---

# Command 12 — Closure authorization

```text
Close only after explicit user authorization.

Create a durable Git checkpoint for authorized tracked outputs.
Verify changed paths.
Perform governed closure bookkeeping.

Preserve parent semantics:
Change completion != Gap closure != RoadmapOutcome completion != Recommendation
completion unless independent reconciliation evidence supports those transitions.

Do not automatically create/start the next Change during closure.
Return the closure report and stop.
```

---

# Preservation rule

These operator forms are useful for:

- human/manual operation;
- regression fixtures;
- designing managed `control/*.md` workflows;
- later AgentWorkPacket compilation.

They should **not** become one always-loaded mega-prompt.
