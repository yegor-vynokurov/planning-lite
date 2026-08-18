# Planning Lite Direction Workflow Playbooks v1.2

**Status:** canonical design specification, not yet released behavior
**Origin:** Poker Project Spine pilot
**Alignment:** Planning Lite v3.8.1 implementation route

---

# 1. What changed from v1

The semantic procedures discovered in Poker remain valid.

The implementation interpretation changed after W0:

```text
v1 conceptual abstraction:
PlanningWorkflowPlaybook object/runtime

v1.1 first implementation owner:
template/.planning/control/*.md
```

Existing control workflows already provide the important playbook properties:

- operation trigger;
- required reads;
- ordered procedure;
- allowed write scope;
- hard guards;
- output contract;
- human authorization boundary.

Therefore do not create a separate PlaybookEngine in the first Project Spine changes.

---

# 2. Canonical workflow contract

Every new Direction control workflow should make these fields explicit, in Markdown rather than requiring a Python schema:

```text
WORKFLOW ID / VERSION
PURPOSE
APPLIES WHEN
DOES NOT APPLY WHEN
AUTHORITY ORDER
REQUIRED READS
OPTIONAL EXPANSION RULES
PROCEDURE
DECISION POINTS
HARD CHECKS
FORBIDDEN ACTIONS
OUTPUT CONTRACT
HUMAN GATES
HANDOFF
CONTEXT PROFILE
SOURCE LINEAGE
```

Stable checklist-like IDs may be embedded initially, for example:

```text
CHK-DIR-CONSISTENCY-001
CHK-DIR-TARGET-001
CHK-DIR-CAPABILITY-001
CHK-DIR-GAP-001
```

A separate checklist subsystem is deferred until repetition justifies extraction.

---

# 3. Universal direction sequence

```text
PW-DIR-001 Inventory + Consistency
        ↓
PW-DIR-002 Target Explorer
        ↓
PW-DIR-003 Target Calibration
        ↓
     HUMAN TARGET ACCEPTANCE
        ↓
PW-DIR-004 Current Capability Assessment
        ↓
PW-DIR-005 Causal Gap Derivation
        ↓
PW-DIR-006 Recommendation/Roadmap Reconciliation
        ↓
PW-DIR-007 Roadmap Synthesis + Prioritization
        ↓
     HUMAN DIRECTION ACCEPTANCE
        ↓
existing CHANGE_DEFINITION
        ↓
existing CHANGE_PLANNING / READINESS / EXECUTION / CLOSURE
```

`PW-CHG-*` and `PW-READY-*` from v1 are not initially new runtime workflows when existing Change control files already own the same lifecycle stage.

Instead, Poker-derived rules should be integrated into those existing workflows only where they add a demonstrated missing invariant.

---

# 4. PW-DIR-001 — Direction Inventory + Current-State Consistency

## Applies when

- onboarding an existing project;
- direction is unclear or stale;
- resuming after a long pause;
- before Target↔Current gap derivation;
- lifecycle/project records may disagree.

## Required reads

```text
project direction/charter sources
CURRENT_STATE
ACTIVE
ROADMAP
active/completed Change index
Git/repository boundary
```

## Procedure

```text
1. discover existing direction sources
2. classify authority
3. classify freshness
4. identify conflicts
5. verify repository boundary
6. compare repository truth with planning truth
7. if materially inconsistent:
       STOP direction derivation
       route to bounded reconciliation
8. else:
       emit DirectionInventory / consistency result
```

## Hard guards

```text
Git clean != planning consistent
historical instruction != current authority
agent inference != accepted Target
```

## Output

```text
DIRECTION_INVENTORY
CURRENT_STATE_CONSISTENCY = PASS | FAIL
authority hierarchy
conflicts/stale sources
safe next stage
```

---

# 5. PW-DIR-002 — Target-State Explorer

## Starting rule

Determine deliverable class early:

```text
product
library
service
internal tool
research demonstrator
reference implementation
portfolio artifact
learning project
infrastructure component
other explicit class
```

## Perspective sweep

```text
purpose
audience
user/reviewer journeys
function
correctness/verifiability
failure/recovery
data/source-of-truth
safety/misuse
observability/explainability
performance/cost
operability
API/integration
evolution
human control
non-goals
```

## Claim provenance

Each Target claim should distinguish:

```text
USER_DECISION
EXISTING_DIRECTION
REPOSITORY_EVIDENCE
INFERRED
UNRESOLVED
```

## Guard

Current architecture is evidence about Current State, not automatic Target definition.

---

# 6. PW-DIR-003 — Target Baseline Calibration

Every unresolved question becomes one of:

```text
TARGET_BOUNDARY_QUESTION
CAPABILITY_DESIGN_QUESTION
RESEARCH_QUESTION
```

Only Target-boundary questions block Target convergence.

If none remain:

```text
TargetStatus = PROVISIONAL_TARGET_BASELINE
```

Target changes later only via:

```text
explicit authority decision
or
explicit TARGET_STATE_SIGNAL
```

Human acceptance is required before the Target becomes accepted direction.

---

# 7. PW-DIR-004 — Current Capability Assessment

Use two independent dimensions:

```text
Coverage:
SATISFIED
PARTIAL
NOT_SATISFIED
UNCERTAIN

EvidenceConfidence:
HIGH
MEDIUM
LOW
```

For each capability record:

```text
target summary
coverage
confidence
satisfied current properties
missing target properties
evidence limitations
owned downstream questions
evidence refs
```

Do not infer satisfaction from roadmap/recommendation/change titles alone.

Do not derive Gaps or priority in this stage.

Context profile:

```text
Target/Capability + current evidence first
history only when current evidence cannot establish a material claim
```

---

# 8. PW-DIR-005 — Causal Gap Derivation

Definition:

```text
Gap = material Target-State property not currently demonstrated
```

Not automatically a Gap:

```text
every PARTIAL capability
every evidence limitation
every stale document
every uncertainty
every old recommendation
every desirable enhancement
```

Procedure:

```text
1. collect missing Target properties
2. cluster causal overlaps
3. separate PRIMARY vs DEPENDENT capability effects
4. consolidate duplicate symptoms
5. preserve separate closure criteria where semantics differ
6. assign stable Gap identity
7. do not prioritize
```

Gap closure must be outcome-oriented, not a file-edit tactic.

---

# 9. PW-DIR-006 — Recommendation + Historical Roadmap Reconciliation

This is the stage where broad historical reads are intentionally appropriate.

Recommendation procedure:

```text
1. read recommendation registry
2. decompose recommendations into semantic units
3. account for every unit
4. map each unit to current Gap / Target signal / local tactic /
   optional future / outside target / unanchored
5. preserve future seeds
6. derive parent reconciliation state
7. run residue invariant
```

Semantic unit states:

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

Parent states:

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

Historical Roadmap dispositions:

```text
KEEP
REFRAME
SPLIT
MERGE_CANDIDATE
DEFER
COMPLETE
RETIRE_FROM_BOUNDED_TARGET
UNCERTAIN
```

Hard invariant:

```text
all original semantic units are accounted for
```

Historical priority is not inherited automatically.

---

# 10. PW-DIR-007 — Roadmap Synthesis + Qualitative Prioritization

Procedure:

```text
1. synthesize a small set of coherent Roadmap outcomes
2. test natural Gap bundles
3. preserve separate Gap closure identities
4. identify real dependencies
5. compare outcomes qualitatively
6. test credible alternatives
7. select exactly one preferred next outcome
8. produce compact default-memory representation
```

Candidate qualitative dimensions:

```text
TARGET_CRITICALITY
FINAL_DELIVERABLE_VALUE
GAP_LEVERAGE
DEPENDENCY_LEVERAGE
EVIDENCE_READINESS
BOUNDEDNESS
RESEARCH_UNCERTAINTY
PREMATURE_FREEZE_RISK
relevant release/user/publication value
```

Do not use fake numeric precision by default.

Human direction acceptance remains required.

---

# 11. Research-heavy composition

The Poker CHG-0008 episode adds reusable rules for research-heavy Changes.

Integrate these rules into existing Change planning when the selected Roadmap outcome is research-heavy:

```text
protocol first
→ implementation later
→ evidence
→ scientific disposition
→ optional production integration
```

Epistemic invariants:

```text
synthetic recovery/sanity != independent validation
development/calibration != final evaluation
study validity != model result != production disposition
study_complete != production_integrated
```

Protocol closure requires:

```text
one executable primary study design
zero study-critical TBDs
```

A valid negative/non-adoption result can complete a research outcome.

---

# 12. Context routing policy

Workflow stage determines justified context depth.

```text
PW-DIR-001:
current direction/lifecycle + repository boundary

PW-DIR-002/003:
high-authority direction + bounded repository evidence

PW-DIR-004:
Target/Capability + current evidence; minimal history

PW-DIR-005:
Spine artifacts; no broad recommendation history

PW-DIR-006:
broad recommendation/Roadmap history intentionally allowed

PW-DIR-007:
reconciled Spine artifacts; avoid source/history replay

Change definition:
compact accepted direction + targeted feasibility reads
```

This policy can be encoded in existing `CONTEXT_POLICY.md` before any Context Compiler exists.

---

# 13. Future ContextTrace

Candidate observational fields:

```text
starting_artifacts
additional_current_reads
historical_changes_opened
recommendations_opened
unnecessary_reads
missing_context_recovery
semantic_fallback
```

The optimization target is **appropriate depth**, not minimum read count.

---

# 14. Human authority map

Productized Planning Lite should stop mainly at material authority boundaries:

```text
Target acceptance
Roadmap/direction acceptance
Change plan approval
execution authorization
closure authorization
destructive/promotion decisions
semantic adjudication
```

Intermediate deterministic/read-only derivations may later be orchestrated after evaluation.

---

# 15. Implementation rule

The exact large Poker prompts are evidence of successful workflow semantics.

Canonical released behavior should be encoded as:

```text
managed control workflow
+
project-owned direction state
+
inline/stable hard checks
+
existing router/context policy
```

not as one immutable giant prompt string.


---

# Research-asset reuse boundary (v1.2)

The workflow semantics are product design. The evaluation infrastructure is not part of the consumer workflow runtime.

Use the following ownership boundary:

```text
Planning Lite control workflows
→ authoritative released planning procedure

planning-lite-lab
→ research evidence / qualification / provenance

planning_lite_tools step-16.4.1
→ current Context Pilot / Eval Harness reference for later context and evaluation work
```

Rules:

1. PL-V38-01..04 must not depend on either external folder at runtime.
2. PL-V38-05 may reuse **ideas/contracts** from Context Pilot 16.4.1 after explicit comparison; do not copy the package wholesale.
3. PL-V38-06A must reconcile Lab current state from the terminal 2026-08-14 closeout checkpoint before new experiments.
4. PL-V38-06A must qualify the `step-16.4.1` tools lineage before old versions are archived or deleted.
5. PL-V38-06B/07 should reuse qualified harness mechanisms for immutable evidence, file-access observation, balanced suites and routing/resolution metrics.
6. Campaign Core may govern repeated evidence but does not own workflow semantics.
