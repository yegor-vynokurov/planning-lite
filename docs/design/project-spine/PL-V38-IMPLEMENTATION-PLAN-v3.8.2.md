# PL-V38 implementation plan v3.8.2

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

No Project Spine behavior has been implemented yet.

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
PL-V38-01   Direction foundation
PL-V38-02   Current assessment + causal Gap Map
PL-V38-03   Recommendation residue/reconciliation
PL-V38-04   Roadmap synthesis/prioritization
PL-V38-05   Direction context/visibility/ContextTrace
PL-V38-06A  Lab + tools reactivation/lineage qualification
PL-V38-06B  Qualified Poker eval suite
PL-V38-07   Context Compiler experiment
PL-V38-08   Safe orchestration + release decision
```

---

# 3. PL-V38-01 — Direction foundation

## Goal

Replace the first three manually authored Poker direction prompts with managed Planning Lite workflows.

## Likely managed workflow additions

```text
template/.planning/control/DIRECTION_INVENTORY.md
template/.planning/control/TARGET_STATE_EXPLORER.md
template/.planning/control/TARGET_BASELINE_CALIBRATION.md
```

## Likely project-owned artifacts/templates

Minimal candidates:

```text
TARGET_STATE.md
CAPABILITY_MODEL.md
```

Exact Copier ownership/materialization must be designed from the current template before implementation.

## Required semantics

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

## Explicit exclusions

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

For PL-V38-01:

```text
planning-lite-lab       reference only
planning_lite_tools     reference only
```

Do not create dependencies on either folder.

---

# 4. PL-V38-02 — Current assessment + causal Gap Map

Add managed workflows for capability assessment and Gap derivation.

Core checks:

```text
Coverage != EvidenceConfidence
PARTIAL separates satisfied/missing/evidence-limit properties
evidence limitation != automatic Gap
one causal Gap may affect several capabilities
SATISFIED capability not silently reopened
Gap closure is outcome-oriented
```

Poker fixture shapes may guide static tests, but no permanent Poker runtime dependency is introduced.

---

# 5. PL-V38-03 — Recommendation residue + historical reconciliation

Extend existing recommendation lifecycle.

Preserve:

```text
semantic units
future seeds
carry-forward
unanchored recommendations
Change completion != Recommendation completion
```

Broad historical reads are intentionally allowed only in this workflow stage.

---

# 6. PL-V38-04 — Roadmap synthesis + prioritization

Add:

```text
outcome synthesis
natural Gap bundling
credible-alternative comparison
qualitative prioritization
preferred-next-outcome proposal
```

Human acceptance before canonical direction mutation.

Research-heavy outcomes compose protocol-first rules into existing Change planning.

---

# 7. PL-V38-05 — Direction context + visibility + ContextTrace

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

# 8. PL-V38-06A — Research asset reactivation / qualification

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

# 9. PL-V38-06B — Qualified Poker eval suite

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

# 10. PL-V38-07 — Context Compiler experiment

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

# 11. PL-V38-08 — Safe orchestration

Automate only proven read-only/deterministic transitions.

Do not automate material user authority.

Prove ordinary small changes remain lightweight.

---

# 12. Asset cleanup policy

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

# 13. Next execution gate

```text
PL-V38-01
Direction foundation
```

Before implementation, define exact:

```text
managed/project-owned paths
Copier ownership impact
workflow output contracts
initial deterministic fixture subset
```
