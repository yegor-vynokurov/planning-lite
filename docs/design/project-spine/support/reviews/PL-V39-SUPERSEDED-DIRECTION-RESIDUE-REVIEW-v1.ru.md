# REC-PL-DIRECTION-001 v1 — superseded-lineage residue review
## Third-pass input to Planning Lite Roadmap v3.9.x

**Status:** `REVIEW COMPLETE / BOUNDED RESIDUE RECOVERED`
**Date:** `2026-08-21`

## 1. Lineage finding

The newly recovered file:

`REC-PL-DIRECTION-001 — Project Spine, Direction Memory and Recommendation Lifecycle`

is not a new independent recommendation family.

`REC-PL-DIRECTION-001-v2` explicitly supersedes it.

However, comparison showed that `v2` says the v1 core architecture remains valid
while no longer spelling out several useful v1 units. Some were also only
implicit or absent in Roadmap v3.9.1.

Therefore:

```text
SUPERSEDED
!=
SAFE TO IGNORE WITHOUT UNIT-LEVEL RESIDUE CHECK
```

This is direct self-hosted evidence for Recommendation Absorption.

## 2. Recovered units

### R1 — Deliverable class remains an explicit Target variable
Disposition: `ABSORB_EXISTING`
Owner: `PL-V39-05 Project Spine entry contract`

Why:
portfolio artifact vs product vs research demonstrator materially changes Target
and Roadmap.

### R2 — Current-State Consistency Gate is permanent, not only a pilot incident
Disposition: `CROSS_CUTTING`
Owner: Project Spine invariant + existing direction workflow

Rule:
do not derive Gap from inconsistent current planning truth.

### R3 — Open questions need semantic ownership
Disposition: `ABSORB_EXISTING`
Owner: `PL-V39-05 Clarification`

Classes:
- TARGET_BOUNDARY_QUESTION
- CAPABILITY_DESIGN_QUESTION
- RESEARCH_QUESTION

Only the first blocks Target convergence.

### R4 — Discovery is not Recommendation
Disposition: `CROSS_CUTTING`
Owner: continuous recommendation lifecycle

Benefit:
prevents observations from becoming automatic roadmap hair.

### R5 — Recommendation lifecycle needs three modes
Disposition: `ABSORB_EXISTING`
Owner: continuous practice

Modes:
- TRIAGE
- RECONCILE
- CONVERGE

No new lifecycle stage.

### R6 — Project Spine is also a memory index
Disposition: `ABSORB_EXISTING`
Owner: `PL-V39-06`

Time scales:
Target → Roadmap → Gap → active Change → archived evidence.

Resolution:
L3 IDs/relations/status
L2 one-line outcome
L1 capsule
L0 full evidence.

### R7 — Archive means not injected, not forgotten
Disposition: `ABSORB_EXISTING`
Owner: `PL-V39-06`

This makes visibility decay explicit.

### R8 — Canonical Boundary Capsules
Disposition: `ABSORB_EXISTING`
Owner: `PL-V39-06` handoff/boundary semantics

Purpose:
upstream stages emit machine-readable owned facts instead of repeatedly copying
SHA/IDs/contracts into downstream prompts.

This is distinct from Context Bootstrap Capsule:
- Boundary Capsule owns exact facts.
- Bootstrap Capsule is a derived re-entry view.

### R9 — Direction convergence / orphan detection
Disposition: `CROSS_CUTTING`
Owner: continuous Project Spine integrity check

Keep as lightweight structural/advisory check, not a new Doctor stage.

### R10 — Project bootstrap sequence
Disposition: `ALREADY_REALIZED / REFERENCE`
Owner: existing `PW-DIR-001…007` direction workflow family

No roadmap expansion needed.

### R11 — Governed deterministic orchestration
Disposition: `ALREADY_ABSORBED`
Owner: `PL-V39-09`

### R12 — Structured exceptions/adjudications
Disposition: `ALREADY_ABSORBED`
Owner: `PL-V39-07` structured blockers + `PL-V39-09` bounded detours

### R13 — Context Compiler / AgentWorkPacket
Disposition: `ALREADY_ABSORBED`
Owner: `PL-V39-09`

## 3. Optimization effect

No new major Roadmap block was added.

The recovered units make the existing spine more coherent:

```text
05 Project Shaping
gets:
deliverable class
question ownership

06 Context/Memory
gets:
explicit memory time scales
L3/L2/L1/L0
archive-not-inject
canonical boundary semantics

12 Continuous practices
gets:
Discovery/Recommendation separation
triage/reconcile/converge
Project Spine integrity check
```

This reduces hidden ambiguity without increasing major stage count.

## 4. New Recommendation Absorption lesson

Add a supersede-residue test:

> When B supersedes A, can any useful semantic unit exist in A that is neither
> represented in B nor explicitly disposed elsewhere?

If YES:
supersede lineage is incomplete.

The old recommendation must not be archived until the residue has an explicit
destination.

## 5. Final verdict

`REC-PL-DIRECTION-001 v1` should remain superseded, not reactivated.

Its useful residue is now absorbed into v3.9.2 draft.

No additional Future Recommendation is required solely because of this file.
