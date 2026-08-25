# PL-V39 Recommendation Absorption Review — Second Pass v1
## Fresh-context reconciliation of Roadmap v3.9 draft + Future Recommendations

**Date:** 2026-08-21
**Status:** `SECOND-PASS REVIEW / PASS WITH BOUNDED INTEGRATED REVISIONS`
**Reviewed drafts:**
- `PLANNING-LITE-ROADMAP-v3.9-INTEGRATED-DRAFT.ru.md`
- `PLANNING-LITE-FUTURE-RECOMMENDATIONS-v1-DRAFT.ru.md`

**Reviewed source families:**
- current `PLANNING-LITE-ROADMAP-v3.8.7.ru.md`;
- historical-but-still-design-relevant `PLAN-PL-LEARNING-CONTEXT-ROADMAP-v3.7.ru.md`;
- active Project Spine recommendation set from `design.zip`;
- active learning/memory/curation recommendation set from `active.zip`;
- supporting skill/checklist/eval/plugin review and code-seed assets.

**Resulting revised drafts:**
- `PLANNING-LITE-ROADMAP-v3.9.1-SECOND-PASS-DRAFT.ru.md`
- `PLANNING-LITE-FUTURE-RECOMMENDATIONS-v1.1-SECOND-PASS-DRAFT.ru.md`

---

# 1. Review question

The review did not ask:

> "Can we fit every recommendation into the Roadmap?"

It asked:

```text
Can the newest Roadmap absorb the useful semantics
without multiplying anatomy,
creating competing owners,
or silently losing deferred value?
```

The acceptance lenses were:

```text
COVERAGE
HAIRINESS
CONTRADICTIONS
FUTURE PRESERVATION
PLACEMENT DETERMINACY
```

The Placement Determinacy test is the direct generalization of the Poker
two-implementation check:

> If two materially different placements/interpretations both satisfy the current
> Roadmap text, and the difference changes authority, sequencing, evidence, or
> lifecycle behavior, the Roadmap is underdetermined.

---

# 2. Overall verdict

**PASS WITH BOUNDED REVISIONS.**

No additional major Roadmap vertebra was required.

The five future organs remain:

```text
PL-V39-05  Project Shaping + Target Reality
PL-V39-06  Context + Memory + Handoffs
PL-V39-07  Execution Contracts + Skills + Checklists + Routing
PL-V39-08  Evaluation + Learning + PromptOps + Controlled Evolution
PL-V39-09  Context Compiler experiment + Safe Orchestration + Release
```

The second pass found several material ownership/sequence ambiguities inside
those organs. They were resolved by moving or sharpening small contracts, not
by adding new top-level phases.

---

# 3. Determinacy findings

## RD-A01 — Target Skeleton ownership

Two compliant readings existed:

```text
A. Direction/Project Shaping directly materializes the target skeleton.

B. Direction defines the skeleton; ordinary governed Change/Execution
   materializes project files.
```

These are materially different because they change authorization and lifecycle
semantics.

**Resolution:** choose B.

PL-V39-05 owns:
- target silhouette;
- Skeleton Contract;
- placeholder semantics;
- proposed bounded contribution.

Actual project mutation remains inside the normal Change lifecycle.

**State:** `CLOSED`.

---

## RD-A02 — Executable Target Contract ownership

Two readings existed:

```text
A. PL-V39-05 defines and wires executable probes.

B. PL-V39-05 defines claims/scenarios; Execution/eval adapters wire them.
```

**Resolution:** split ownership by status.

```text
PL-V39-05
→ System Claims + Target Scenarios at least through DEFINED

governed Execution / project eval adapter
→ WIRED

Verification / eval
→ PASSING evidence
```

**State:** `CLOSED`.

---

## RD-A03 — Target Scenario vs EvalCase

Two possible canonical models existed:

```text
A. Target Scenario is itself the canonical eval case.

B. Target Scenario is project intent; EvalCase is a versioned executable projection.
```

Model A would mix project target authority with evaluator fixture/version/provenance.

**Resolution:** choose B.

Projection may be one-to-many.

**State:** `CLOSED`.

---

## RD-A04 — Control rule placement

A reusable rule could plausibly live in:
- workflow playbook;
- skill;
- checklist;
- root prompt.

Without ownership, all four could be "correct" and still create duplication/drift.

**Resolution:** add explicit control-artifact ownership:

```text
root/router
→ activation only

workflow playbook
→ lifecycle sequence / authority / stop-resume

skill
→ reusable procedure + reference routing

checklist
→ reusable verification/evidence obligations

task AC
→ task-specific outcome

System Claim
→ project-level target behavior

EvalCase
→ executable evidence instance
```

**State:** `CLOSED`.

---

## RD-A05 — Project Survey vs current-state authority

Two readings existed:

```text
A. Survey becomes another current architecture/current-state truth.

B. Survey is bounded AS-IS evidence consumed by existing Project Spine workflows.
```

**Resolution:** choose B.

Survey/archaeology do not own:
- capability interpretation;
- coverage/confidence;
- Gap semantics;
- accepted direction.

**State:** `CLOSED`.

---

## RD-A06 — Outcome Ladder vs canonical Target

Two readings existed:

```text
A. L0...L4 are several simultaneously canonical Targets.

B. Ladder is a shaping/value aid; one Target State is accepted into Project Spine.
```

**Resolution:** choose B.

`highest demonstrated level` is Verification evidence, not another desired Target.

**State:** `CLOSED`.

---

## RD-A07 — Strategy route vs execution route

"Route" could refer to:
- project-level strategic alternative;
- per-task execution/orchestration pattern.

**Resolution:** separate identities.

```text
Strategy Route
→ how the project may reach target value.

Execution Pattern
→ how one authorized task should be carried out.
```

Strategy triggers make a dormant route eligible for reconciliation, never
silently active.

**State:** `CLOSED`.

---

## RD-A08 — Context Bootstrap Capsule vs AgentWorkPacket

Two possible memory systems could accidentally emerge:

```text
A. Bootstrap Capsule is the main task packet.

B. Bootstrap Capsule is tiny current-state re-entry;
   AgentWorkPacket is task-specific derived context.
```

**Resolution:** choose B.

Neither becomes a second canonical memory authority.

**State:** `CLOSED`.

---

## RD-A09 — Context Compiler vs release

The v3.9 draft grouped:
- Context Compiler experiment;
- orchestration;
- release.

This allowed two materially different release interpretations:

```text
A. compiler promotion is required before release.

B. compiler may lose; validated current context path remains releasable.
```

**Resolution:** choose B.

Context Compiler is a comparator experiment.
A losing result is valid and does not block safe orchestration/release.

Production compiler promotion remains a future evidence-gated recommendation.

**State:** `CLOSED`.

---

## RD-A10 — Skill/Checklist vs Eval Core ordering

Two plausible sequences existed:

```text
A. build many skills/checklists, then evaluate.

B. define a small stable pilot surface, extract/reuse Eval Core, then scale.
```

The old v3.7 design explicitly favored B before a large skill corpus.

**Resolution:** restore B.

```text
07 minimal pilot semantics
→ 08 reusable/qualified eval
→ evidence-backed 07 scale-out
```

This is a loopback, not another phase.

**State:** `CLOSED`.

---

# 4. Valuable older design pieces recovered in second pass

The first v3.9 draft correctly recovered v3.7 Skill/Checklist/Eval/Memory work,
but still left several mature v3.7 concepts without explicit disposition.

## 4.1 Behavior Localization

The full persistent Behavior Handbook is too much machinery for the current
Roadmap.

But one compact piece is immediately valuable for cross-file/state-coupled work:

```text
behavior delta
state writers/readers/resets
must-never-be-inferred-from
verified source anchors
cold/recovery paths
verification
```

**Current absorption:** optional change-local Behavior/State Coverage Capsule in PL-V39-07.

**Deferred residue:** full persistent Behavior/State Handbook in `FUT-PLAN-001`.

---

## 4.2 Typed PlanningProblem / bounded plan optimization

The complete typed planner/optimizer/memoization architecture is still too large.

But two principles are immediately useful:

```text
hard eligibility constraints before cost/value comparison

plan-shape correctness
!=
outcome correctness
```

**Current absorption:**
- strategy/execution eligibility in PL-V39-05/07;
- plan-shape dimension in PL-V39-08 eval.

**Deferred residue:** full typed planner in `FUT-PLAN-002`.

---

## 4.3 Execution Environment Contract

This was missing from v3.9 despite being mature in v3.7 and repeatedly useful in Poker prompts.

Recovered as an **Execution Envelope**:

```text
read/write surface
forbidden paths
tools
network/Git capability
mutation authorization
execution profile
```

Physical enforcement is preferred where the host supports it; otherwise bounded
preflight + fail closed.

No separate Roadmap stage is needed.

---

## 4.4 Semantic blockers / next action

Older v3.7 had a useful bounded error contract.

Recovered without committing to numeric exit-code infrastructure:

```text
failure_class
evidence
allowed_actions
forbidden_actions
next_action
```

This fits weak-model execution and bounded reconciliation detours.

---

## 4.5 Validation ladder

The first v3.9 draft had a project-level Feedback Channel Matrix but did not
explicitly connect it to per-task validation selection.

Recovered as:

```text
smallest sufficient validation
based on blast radius + failure class
```

This keeps both:
- "do not run everything after every edit";
- "do not under-test cross-boundary changes."

---

# 5. Readiness reconciliation

The v3.9 draft preserved exhaustive Readiness, but one important field-derived
idea from `REC-PL-READINESS-001` was too implicit:

```text
traceability-complete
!=
execution-ready
```

Second pass makes applicable Readiness dimensions explicit:

```text
SEMANTIC_READY
DELIVERY_READY
CONTRACT_READY
EVIDENCE_READY
RUNTIME_READY
PROVENANCE_READY
ENVIRONMENT_READY
```

They are selected by Change type, not imposed universally.

This gives Readiness a coherent place for:
- contract closure;
- evidence seams;
- runtime preflight;
- provenance;
- execution envelope.

---

# 6. Recommendation Absorption skill/checklist learning

The self-hosted exercise now suggests a compact manual checklist:

```text
RECOMMENDATION_ABSORPTION_ACCEPTANCE

1. COVERAGE
   Every useful unit accounted?

2. PLACEMENT DETERMINACY
   Could the same unit live in two materially different owners?
   If yes, resolve ownership.

3. ANTI-HAIR
   Is this really a new capability/sequence, or just a better rule?

4. CONTRADICTIONS
   Did merged units encode incompatible authority, state, or sequence?

5. FUTURE PRESERVATION
   Deferred value has identity + wake trigger?

6. NO SILENT RESIDUE
   Every touched unit has a disposition?

7. LINEAGE
   Can future review recover the original source and successor?
```

This checklist is useful **now**.

What remains future (`FUT-ABSORB-001`) is:
- managed workflow packaging;
- assisted unit extraction;
- automatic overlap detection;
- productized reconciliation tooling.

That distinction was sharpened in v1.1 Future Recommendations.

---

# 7. Hairiness review

The second pass did **not** add a major vertebra.

It added internal ownership/contracts only where ambiguity was material.

The following remain methods, not stages:

```text
Behavior/State Capsule
Execution Envelope
Validation sufficiency
Readiness dimensions
Recommendation Absorption checklist
Placement Determinacy
structured blocker/next_action
```

This passes the anti-hair test.

---

# 8. Future-preservation review

The Future Backlog remains a single non-scheduled carrier.

Second pass added two missing mature v3.7 residues:

```text
FUT-PLAN-001
Persistent Behavior Localization / State Register Handbook

FUT-PLAN-002
Typed PlanningProblem + bounded candidate-plan optimizer
```

It also clarified:

```text
FUT-CTX-001
Production Context Compiler is not a release prerequisite.

FUT-ABSORB-001
Manual absorption checklist is current;
automation/productization remains deferred.
```

No full second roadmap was created.

---

# 9. Sequencing improvement

The original v3.9 sequence looked more serial than necessary.

Second pass keeps one promotion mainline:

```text
05 → 06 → 07 → 08 → 09
```

but allows cheap read-only preparation:

```text
after field gate
→ 08A research-asset reconciliation may start

during/after 05
→ existing skill/checklist + fixture inventory may start

after minimal 07 semantics
→ 08 becomes the gate before scale-out

after 08 contracts
→ 09 comparator harness preparation may start
```

This makes the Roadmap more executable without weakening gates.

---

# 10. Remaining non-blocking observations

## 10.1 PL-V39-05 is broad but coherent

It contains Survey, Outcome, Strategy, Skeleton, and Target Contract.

Second pass considered splitting it.

The new-vertebra test did **not** justify a split because these are all inputs to
one capability:

```text
make accepted direction more valuable, testable, and actionable
before heavy implementation
```

Their sequence is local and they share the same Target/Roadmap handoff boundary.

Keep one vertebra.

---

## 10.2 PL-V39-08 is broad but coherent

Evaluation and Controlled Evolution could be split.

Do not split yet.

They share:
- ArtifactUnderTest lineage;
- qualified fixtures;
- evidence;
- verifier results;
- candidate decision;
- rollback/promotion.

Splitting now would risk a second eval/evolution runtime.

Keep one limb with subphases.

---

## 10.3 PL-V39-09 remains one final block only after decoupling compiler promotion

Without the second-pass clarification it was too ambiguous.

With:

```text
compiler may lose
+
orchestration can use validated non-compiler path
+
release is independent of compiler production promotion
```

the block is coherent enough to remain one final gate.

---

# 11. Final review verdict

After the bounded revisions:

```text
Coverage                 PASS
Hairiness                 PASS
Contradictions            PASS
Future preservation       PASS
Placement determinacy     PASS
No silent residue         PASS at current document-family granularity
```

No unresolved material contradiction was found that requires another Roadmap
vertebra or deletion of an existing one.

The revised drafts are suitable for human acceptance review.

They are **not yet canonical** until explicitly accepted.

---

# 12. Recommended next action

1. Human-review the changed ownership/sequence decisions in v3.9.1.
2. If accepted, make v3.9.1 the current Roadmap baseline.
3. Make Future Recommendations v1.1 the single active carrier for deferred residue.
4. Archive old recommendation documents progressively only after unit-level lineage/disposition receipts.
5. Preserve this review as the first self-hosted fixture for the future Recommendation Absorption skill/eval.
