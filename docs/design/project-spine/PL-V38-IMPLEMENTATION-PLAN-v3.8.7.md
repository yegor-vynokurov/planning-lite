# PL-V38 implementation plan v3.8.7

**Status:** current stepwise implementation plan
**Date:** 2026-08-18
**Execution principle:** product semantics first, reuse proven research infrastructure, automation last.

---

# 1. Completed preparation

## W0 — Architecture/baseline/evidence freeze

Completed.

Key finding:

```text
Planning Lite is template/workflow-first.
```

## PL-V38-00 — Central working-tree reconciliation

Completed locally.

Current source boundary:

```text
57eb5bd docs: record post-v4.3 campaign repairs
0681b86 campaign: add strict attempt budget admission
0d7c923 campaign: reconcile legacy attempt suite evidence
0e66941 v4.3.0 release baseline
```

Local verification:

```text
114 passed
working tree clean
main ahead of origin/main by 3
```

The v3.8.2 design checkpoint is tracked at `40ca8cf`. PL-V38-01 implements Direction Foundation; its EOL-stable integrity-test hotfix is `782c785`. PL-V38-02 implements Current/Gap; PL-V38-03 implements recommendation semantic residue and historical reconciliation. PL-V38-04 implements Roadmap outcome synthesis, qualitative prioritization, human Roadmap acceptance, and bounded-Change lineage handoff. Non-scored Poker preparation then exposed a local-only consumer update defect; PL-V38-PREP-01 fixes that boundary before the scored field attempt.

## Research-asset review

Existing assets:

```text
D:\documents\planning-lite-lab
D:\documents\planning_lite_tools
```

Disposition:

```text
preserve both
reuse later
not consumer dependencies
not part of PL-V38-01 implementation
```

---

# 2. Current implementation sequence

```text
PL-V38-01   Direction foundation                         COMPLETE
PL-V38-02   Current assessment + causal Gap Map          COMPLETE
PL-V38-03   Recommendation residue/reconciliation        COMPLETE
PL-V38-04   Roadmap synthesis/prioritization + handoff    COMPLETE
PL-V38-PREP-01 Local-only consumer update safety          COMPLETE CORRECTIVE GATE
FIELD       Poker Field Pilot 2 / next-Change derivation  NEXT / STOP-GATE
PL-V38-05   Direction context/visibility/ContextTrace
PL-V38-06A  Lab + tools reactivation/lineage qualification
PL-V38-06B  Qualified Poker eval suite
PL-V38-07   Context Compiler experiment
PL-V38-08   Safe orchestration + release decision
```

---

# 3. PL-V38-01 — Direction foundation

## Result

The first three manually authored Poker direction procedures are now represented by managed Planning Lite workflows and project-owned direction artifacts.

## Managed workflow additions

```text
template/.planning/control/DIRECTION_INVENTORY.md
template/.planning/control/TARGET_STATE_EXPLORER.md
template/.planning/control/TARGET_BASELINE_CALIBRATION.md
```

## Project-owned artifacts/templates

```text
TARGET_STATE.md
CAPABILITY_MODEL.md
```

## Implemented semantics

```text
authority/freshness discovery
Current-State Consistency Gate
deliverable class
Target claim provenance
Target status
question ownership
Target flow-back rule
explicit human Target acceptance
```

## Preserved exclusions

```text
Gap derivation
RecommendationUnit
Roadmap prioritization
Context Compiler
new Python Playbook runtime
new graph/database
embeddings
Lab/Harness mutation
new LLM Campaign
```

## Research assets

For PL-V38-01 the external assets remain inactive:

```text
planning-lite-lab       reference only
planning_lite_tools     reference only
```

Do not create dependencies on either folder.

---

# 4. PL-V38-02 — Current assessment + causal Gap Map

## Result

Implemented two sequential workflow operations:

```text
PW-DIR-004 CURRENT_CAPABILITY_ASSESSMENT [Audit]
PW-DIR-005 CAUSAL_GAP_DERIVATION [Planning]
```

Artifact split:

```text
CURRENT_CAPABILITY_ASSESSMENT
→ project-owned evidence snapshot under assessments/current
→ created only when the Audit actually runs

GAP_MAP.md
→ durable project-owned causal direction artifact
→ managed pristine copy for safe installation/update
```

Core checks implemented:

```text
Coverage != EvidenceConfidence
PARTIAL separates satisfied/missing/evidence-limit properties
evidence limitation != automatic Gap
one causal Gap may affect several capabilities
PRIMARY != DEPENDENT effect
SATISFIED capability not silently reopened
Gap closure is outcome-oriented
Change completion != Gap closure
Gap != RoadmapOutcome != Change
CURRENT_BASELINE Gap Map requires explicit user acceptance
```

Poker fixture shapes informed semantics/static tests, but no permanent Poker runtime dependency was introduced.

---

# 5. PL-V38-03 — Recommendation residue + historical reconciliation

## Result

Implemented one bounded direction workflow:

```text
PW-DIR-006 RECOMMENDATION_HISTORY_RECONCILIATION [Planning]
```

Artifact split:

```text
recommendation item
→ remains authoritative project-owned record
→ may gain stable REC-NNNN/Ux semantic units
→ lifecycle Status remains separate from reconciliation review/parent state

DIRECTION_HISTORY_RECONCILIATION
→ project-owned assessment snapshot under assessments/current
→ DRAFT / CURRENT
→ created only when reconciliation actually runs
→ does not mutate canonical Roadmap priority
```

Core checks implemented:

```text
all original recommendation semantic units are accounted for
Change completion != Recommendation completion
unit state != primary lineage
future seed != current Gap/priority
CARRIED_FORWARD != implemented
historical Roadmap order != current priority
legacy/simple recommendations remain valid until reconciliation is needed
CURRENT reconciliation requires explicit user acceptance
Roadmap dispositions: KEEP / REFRAME / SPLIT / MERGE_CANDIDATE / DEFER / COMPLETE / RETIRE_FROM_BOUNDED_TARGET / UNCERTAIN
orphan + overlap + apparently-completed-residue audit
exact Source recommendation units may scope later Changes
```

Implementation refinement from the original design: parent reconciliation state `OPEN` is included for a current recommendation whose required units remain wholly open.

Broad historical reads are intentionally allowed only in this workflow stage. PL-V38-03 stops before prioritization or canonical Roadmap synthesis.

---

# 6. PL-V38-04 — Roadmap synthesis + prioritization

## Result

Implemented:

```text
PW-DIR-007 ROADMAP_SYNTHESIS_PRIORITIZATION [Planning]
assessments/ROADMAP_SYNTHESIS_TEMPLATE.md
project-owned ROADMAP.md CURRENT_BASELINE schema
exact Roadmap/Gap/Recommendation lineage in Change definition/closure
```

Semantic boundary:

```text
accepted Project Spine + current reconciliation
→ coherent RoadmapOutcome candidates
→ credible-alternative qualitative comparison
→ one preferred NOW proposal
→ explicit human Roadmap acceptance
→ later-turn CHANGE_DEFINITION handoff
```

Hard guards:

```text
historical Roadmap order != current priority
RoadmapOutcome != Gap != Change
Change completion != RoadmapOutcome completion
Change completion != Gap closure
no automatic Change creation
no PL-V38-05 continuation before field evidence
```

Research-heavy outcomes explicitly consider protocol-first composition rather than freezing production integration before scientific decision rules are defined.

---

# 7. FIELD — Poker Project Spine Field Pilot 2

PL-V38-04 is complete and PL-V38-PREP-01 repairs the local-only update boundary found during non-scored preparation. **Stop Planning Lite feature expansion now**. Repeat the disposable local-only migration preview, require `PILOT_READY`, then resume Poker from the clean post-CHG-0008 boundary.

Use Planning Lite itself to derive the next bounded Bayesian implementation Change. Capture failures/overreads/authority mistakes as new Planning Lite evidence.

Do not manually pre-create the Poker implementation Change before this pilot; that next-Change derivation is the field test.

---

# 8. PL-V38-05 — Direction context + visibility + ContextTrace

Extend existing Context Policy.

Before writing new context machinery, compare semantics with Context Pilot 16.4.1.
Reuse compatible concepts, especially:

```text
snapshot/lifecycle fast path
least-privilege targeted context
safe insufficient-context deferral
file-access observation
routing success vs resolution success
```

Do not copy the Pilot package wholesale.
Do not use Context Compiler yet.

---

# 9. PL-V38-06A — Research asset reactivation / qualification

This is the first stage where the two external research assets become active dependencies of the work.

## Lab

Reconcile current state from:

```text
planning-lite-lab/checkpoints/
2026-08-14-r3-closeout-budget-admission-validated/
```

Requirements:

```text
R3 remains terminal historical evidence
no R3 rerun
no old Campaign mutation
new experiment authority starts from a new explicit decision
```

## Context Pilot / Eval Harness

Qualify:

```text
planning_lite_tools/step-16.4.1/
```

as the current reference baseline.

Create recursive lineage/dependency manifest for older versions.
Classify each old version:

```text
still-required
archive-required
archive-safe
```

Deletion is not authorized merely by classification.

---

# 10. PL-V38-06B — Qualified Poker eval suite

Turn Poker field evidence into controlled-realistic fixture packages.

Use Lab for:

```text
source hashes
qualification receipts
provenance/checkpoints
archive discipline
```

Reuse Eval Harness mechanisms where compatible for:

```text
fixture staging
immutable evidence
verification
file-access metrics
suite aggregation
```

Initial P0 cases:

```text
current-state consistency
target-question ownership
coverage/confidence
causal Gap compression
recommendation residue
historical priority override
Change completion != Gap closure
```

---

# 11. PL-V38-07 — Context Compiler experiment

Only after workflow semantics and fixtures are stable.

Comparator arms:

```text
A raw canonical docs
B status snapshot
C snapshot + workflow
D Project Spine + workflow compiled packet
```

Prefer reusing the qualified 16.4.1 measurement stack rather than implementing another harness.

Measure:

```text
semantic correctness
authorization correctness
routing success
resolution success
safe deferral
files opened/reopened
retries
tokens
timing
operator corrections
```

Campaign Core is optional and only used if repeated governed runs are justified.

---

# 12. PL-V38-08 — Safe orchestration

Automate only proven read-only/deterministic transitions.

Do not automate material user authority.

Prove ordinary small changes remain lightweight.

---

# 13. Asset cleanup policy

Do not delete either research folder before PL-V38-06A.

Expected eventual target:

```text
planning-lite-lab
→ retained as research/evidence owner

planning_lite_tools/step-16.4.1
→ retained as qualified current reference or superseded by an explicitly qualified successor

older planning_lite_tools versions
→ moved into governed Lab archive when lineage review proves safe
```

Space saving is not a sufficient reason to destroy provenance.

---

# 14. Next execution gate

```text
PILOT-PL-DIRECTION-002
Poker continuation / next-Change derivation
```

Do not start PL-V38-05 before the repaired migration preview reaches `PILOT_READY`, this field gate is run, and its findings are reconciled. Do not manually pre-create the next Poker Change: deriving that bounded Change from the accepted Poker Roadmap is the test.
