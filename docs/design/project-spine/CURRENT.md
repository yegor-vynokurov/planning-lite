# Planning Lite development design — CURRENT

<!-- PLANNING_LITE_RESUME_CONTRACT_V1:BEGIN -->
repository_role: CENTRAL_SOURCE
resume_authority: docs/design/project-spine/CURRENT.md
current_roadmap: docs/design/project-spine/roadmap/ROADMAP.md
active_change: NONE
lifecycle_gate: DISCOVERY_READY
implementation_authorized: NO
blockers: NONE
next_permitted_action: review_pl_v39_05_project_shaping_entry_contract
last_transition_receipt: docs/design/project-spine/checkpoints/PLANNING-LITE-FIELD-CONTROL-PACK-CLOSEOUT-v1.md
state_as_of: 2026-08-26
<!-- PLANNING_LITE_RESUME_CONTRACT_V1:END -->

> **Resume authority:** the block below is the canonical session-handoff state. Historical prose later in this file may preserve earlier checkpoints and must not override it.

<!-- PL_FCP_CLOSEOUT_CURRENT_NOTE_V1:BEGIN -->
## Current Field Control Pack closeout

`CHG-PL-FIELD-CONTROL-PACK-001` is **Completed and closed**.

Canonical closeout:

```text
docs/design/project-spine/checkpoints/PLANNING-LITE-FIELD-CONTROL-PACK-CLOSEOUT-v1.md
```

The bounded behavioral pilot finished `6/6 PASS` with verdict
`release-candidate`.

Release has **not** been authorized or started.

The central repository now has no active Change. The next permitted activity is
review of the `PL-V39-05 Project Shaping / Target Reality` entry contract.
That review does not itself authorize PL-V39-05 implementation.
<!-- PL_FCP_CLOSEOUT_CURRENT_NOTE_V1:END -->


**Updated:** 2026-08-26
**Purpose:** stable navigation entry point for Planning Lite's own development/design work.

Read this file before opening historical Roadmaps or recommendation archives.

## Current development design baseline

```text
docs/design/project-spine/roadmap/ROADMAP.md
```

Roadmap revision inside that file:

```text
Planning Lite Roadmap v3.9.3
```

This is a **development design baseline**, not a Planning Lite product release and
not implementation authorization.

## Current operational field checkpoint

Compatibility/current field state remains recorded in:

```text
docs/design/project-spine/PL-V38-CURRENT.md
```

The immediate implementation sequence continues to follow that operational
checkpoint until the field gate is reconciled.

## Current deferred-residue carrier

```text
docs/design/project-spine/recommendations/FUTURE-RESERVE.md
```

It contains:
- Future Seeds;
- deferred experiments;
- rejected forms worth remembering;
- dormant Contingency Route A.

It is not a second Roadmap.

## New recommendation intake

```text
docs/design/project-spine/recommendations/inbox/
```

Accepted/unabsorbed items may move to:

```text
docs/design/project-spine/recommendations/active/
```

Absorption rules:

```text
docs/design/project-spine/governance/RECOMMENDATION-ABSORPTION.md
```

## Discoveries

Observations/facts with no action implication:

```text
docs/design/project-spine/discoveries/
```

Rule:

```text
Discovery != Recommendation
```

A Discovery may spawn zero, one, or several Recommendations.

## Historical / support material

Old Roadmaps:

```text
docs/design/project-spine/roadmap/archive/
```

Absorbed/superseded Recommendations:

```text
docs/design/project-spine/recommendations/archive/
```

Evidence, playbooks, reviews, code seeds, and research assets:

```text
docs/design/project-spine/support/
```

## Lab boundary

`.planning-lab/` is a research/lab workspace.

It may contain old local Roadmaps and source recommendations, but it is not
current Planning Lite development direction authority.

Do not add new central Planning Lite recommendations there.

## Immediate direction

Documentation reorganization does not authorize PL-V39-05.

Current mainline:

```text
CURRENT FIELD GATE
→ PL-V39-05 Project Shaping / Target Reality
→ PL-V39-06 Context / Memory
→ PL-V39-07 Execution Contracts / Skills / Checklists
→ PL-V39-08 Evaluation / Learning / PromptOps
→ PL-V39-09 Context Compiler experiment / Safe Orchestration / Release
```
