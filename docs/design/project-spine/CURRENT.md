# Planning Lite development design — CURRENT

<!-- PLANNING_LITE_RESUME_CONTRACT_V1:BEGIN -->
repository_role: CENTRAL_SOURCE
resume_authority: docs/design/project-spine/CURRENT.md
current_roadmap: docs/design/project-spine/roadmap/ROADMAP.md
active_change: NONE
lifecycle_gate: DISCOVERY_READY
implementation_authorized: NO
blockers: NONE
next_permitted_action: plan_next_pl_v39_05_slice
last_transition_receipt: docs/design/project-spine/checkpoints/PL-V39-05-A-SHAPING-FOUNDATION-CLOSEOUT-v1.md
state_as_of: 2026-08-27
<!-- PLANNING_LITE_RESUME_CONTRACT_V1:END -->

> **Resume authority:** the block below is the canonical session-handoff state. Historical prose later in this file may preserve earlier checkpoints and must not override it.

<!-- PL_V39_05_A_CENTRAL_ACTIVATION_V1:BEGIN -->
## Current PL-V39-05-A central Change

The user explicitly approved Definition `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001`.

Approved Definition:

```text
docs/design/project-spine/checkpoints/PL-V39-05-A-APPROVED-DEFINITION-v1.md
```

Central activation receipt:

```text
docs/design/project-spine/checkpoints/PL-V39-05-A-DEFINITION-ACTIVATION-v1.md
```

This central-source repository does **not** use a consumer-style root
`.planning/changes/active/...` folder for its own development Change state.

Current lifecycle:

```text
Planning / In progress
implementation_authorized = NO
```

The approved Definition permits preparation of the bounded implementation Plan
and subsequent Formal Readiness only.

T-01 has not started.

Next permitted action:

```text
prepare_pl_v39_05_a_implementation_plan
```
<!-- PL_V39_05_A_CENTRAL_ACTIVATION_V1:END -->


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

<!-- PL_V39_05_A_PLAN_APPROVAL_V1:BEGIN -->
## PL-V39-05-A Plan approval / Formal Readiness

The user explicitly approved:

```text
CHG-PL-V39-05-A-SHAPING-FOUNDATION-001-CENTRAL-PLAN-001
```

Approved Plan:

```text
docs/design/project-spine/checkpoints/PL-V39-05-A-APPROVED-PLAN-v1.md
```

Readiness-entry receipt:

```text
docs/design/project-spine/checkpoints/PL-V39-05-A-PLAN-APPROVAL-READINESS-ENTRY-v1.md
```

Current gate:

```text
FORMAL_READINESS_IN_PROGRESS
implementation_authorized = NO
```

Formal Readiness is read-only with respect to product/template/src/test surfaces.
A Readiness PASS still requires separate explicit user Execution authorization.
<!-- PL_V39_05_A_PLAN_APPROVAL_V1:END -->

<!-- PL_V39_05_A_READINESS_VERDICT_V1:BEGIN -->
## PL-V39-05-A Formal Readiness verdict

Formal Readiness verdict:

```text
PASS
```

The preliminary R-04 blocker was reclassified as:

```text
VERIFIER_DEFECT
```

Reason: Planning Lite's canonical integrity receipt hashes template files after
normalizing line endings from CRLF to LF. The preliminary verifier compared raw
Windows bytes instead.

Corrected baseline verification:

```text
template files     = 159
MANIFEST entries   = 159
SHA receipts       = 158
canonical-LF hash mismatches = 0
integrity owner test = PASS
```

Implementation remains unauthorized.

Next gate:

```text
explicit user Execution authorization for PL-V39-05-A
```
<!-- PL_V39_05_A_READINESS_VERDICT_V1:END -->

<!-- PL_V39_05_A_EXECUTION_AUTH_V1:BEGIN -->
## PL-V39-05-A Execution authorization

The user explicitly authorized Execution of `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001` within the approved
Definition and Plan.

```text
implementation_authorized = YES
lifecycle = EXECUTION_IN_PROGRESS
first permitted task = T-01
```

Release, merge and push remain unauthorized.
<!-- PL_V39_05_A_EXECUTION_AUTH_V1:END -->

<!-- PL_V39_05_A_T01_V1:BEGIN -->
## PL-V39-05-A T-01 completion

```text
T-01 Project Survey contract + managed template: COMPLETED
T-02 Clarification Sweep: NOT STARTED
```

T-01 added only `template/.planning/assessments/PROJECT_SURVEY_TEMPLATE.md` and modified only `template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md`.

`MANIFEST_V4.md` and `SHA256SUMS.txt` remain intentionally pending until T-03,
as required by the approved Plan.
<!-- PL_V39_05_A_T01_V1:END -->

<!-- PL_V39_05_A_T02_V1:BEGIN -->
## PL-V39-05-A T-02 completion

```text
T-01 Project Survey: COMPLETED
T-02 Bounded Clarification Sweep: COMPLETED
T-03 Documentation / integrity seam: NOT STARTED
```

T-02 modified only:

```text
template/.planning/control/TARGET_BASELINE_CALIBRATION.md
```

No router, prompt, skill, project-state, Python runtime, ownership, Copier, or
integrity file was changed.

The exact expected pre-T03 integrity debt is:

```text
MANIFEST missing:
.planning/assessments/PROJECT_SURVEY_TEMPLATE.md

SHA receipts stale:
.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md
.planning/control/TARGET_BASELINE_CALIBRATION.md
```

The first stale receipt originates from T-01; the second from T-02.

Next permitted task: `T-03`.
<!-- PL_V39_05_A_T02_V1:END -->

<!-- PL_V39_05_A_T03_V1:BEGIN -->
## PL-V39-05-A T-03 completion

```text
T-01 Project Survey: COMPLETED
T-02 Bounded Clarification Sweep: COMPLETED
T-03 Documentation / ownership / integrity seam: COMPLETED
T-04 Focused product acceptance: NOT STARTED
```

T-03 modified product surfaces only:

```text
template/.planning/assessments/README.md
template/.planning/docs/MANIFEST_V4.md
template/.planning/framework/SHA256SUMS.txt
```

`OWNERSHIP.yml` and `copier.yml` were verified read-only and remained unchanged.

Integrity is fully reconciled:

```text
template files = 160
MANIFEST entries = 160
SHA receipts = 159
canonical-LF SHA mismatches = 0
```

Next permitted task: `T-04`.
<!-- PL_V39_05_A_T03_V1:END -->

<!-- PL_V39_05_A_T04_V1:BEGIN -->
## PL-V39-05-A T-04 completion

```text
T-01 Project Survey: COMPLETED
T-02 Bounded Clarification Sweep: COMPLETED
T-03 Documentation / integrity seam: COMPLETED
T-04 Focused deterministic product acceptance: COMPLETED
T-05 Consumer update-safety acceptance: NOT STARTED
```

T-04 added `tests/test_project_shaping_foundation.py` with 17 focused semantic/structural tests.

Verifier notes: optional Markdown bold is accepted, and test count is derived from Python AST rather than pytest presentation output.

Next permitted task: `T-05`.
<!-- PL_V39_05_A_T04_V1:END -->

<!-- PL_V39_05_A_T05_V1:BEGIN -->
## PL-V39-05-A T-05 completion

```text
T-01 Project Survey: COMPLETED
T-02 Bounded Clarification Sweep: COMPLETED
T-03 Documentation / integrity seam: COMPLETED
T-04 Focused product acceptance: COMPLETED
T-05 Consumer update-safety acceptance: COMPLETED
T-06 Completion review: NOT STARTED
```

Disposable local-only consumer acceptance proved that the managed `PROJECT_SURVEY_TEMPLATE.md` is added/updated with canonical-LF content equal to central source while a materialized `assessments/current/PROJECT_SURVEY.md` remains project-owned and raw-byte preserved.

No live external consumer was mutated.

Next permitted task: `T-06`.
<!-- PL_V39_05_A_T05_V1:END -->

<!-- PL_V39_05_A_T06_V1:BEGIN -->
## PL-V39-05-A T-06 completion review

```text
T-01 Project Survey: COMPLETED
T-02 Bounded Clarification Sweep: COMPLETED
T-03 Documentation / integrity seam: COMPLETED
T-04 Focused product acceptance: COMPLETED
T-05 Consumer update-safety acceptance: COMPLETED
T-06 Completion review: PASS
completion verdict: COMPLETED
closure authorization: NOT YET GRANTED
release/push: NOT AUTHORIZED
```

Completion review does not itself close the central Change. The next permitted action is an explicit user closure decision.
<!-- PL_V39_05_A_T06_V1:END -->

<!-- PL_V39_05_A_CLOSEOUT_V1:BEGIN -->
## PL-V39-05-A closeout

```text
Change: CHG-PL-V39-05-A-SHAPING-FOUNDATION-001
completion verdict: COMPLETED
closure: AUTHORIZED AND RECORDED
active_change: NONE
implementation_authorized: NO
release: NOT AUTHORIZED
tag/merge/push: NOT PERFORMED
```

This closeout ends the bounded PL-V39-05-A execution cycle and returns the central repository to discovery/planning readiness for the next PL-V39-05 slice.
<!-- PL_V39_05_A_CLOSEOUT_V1:END -->

## PL-V39-05-B closed

- Slice: `PL-V39-05-B / Brownfield Recovery + Outcome Ladder`
- Implementation: `COMPLETED`
- Field validation: `PASS BY ADJUDICATION`
- Material product defect open: `NO`
- Formal closeout: `COMPLETED / OWNER APPROVED`
- Brownfield Recovery: bounded/provisional recovery with provenance, conflict stop rules, and no silent authority promotion.
- Outcome Ladder: observable outcomes with inherited authority ceiling, minimum useful stopping level, and anti-task semantics.
- Persistent scenarios `S1..S5`: `PASS`.
- Central full regression: `PASS`.
- Real brownfield consumer: `math_drill_generator`; current-candidate projection and Doctor `PASS`; live consumer unchanged.
- `D-09` legacy `v3.1.0 -> current` ownership transition remains a separate migration-compatibility follow-up, outside this slice.
- Roadmap: unchanged intentionally.
- Release/tag/push: `NOT AUTHORIZED`.
- Next: select the next bounded shaping slice inside `PL-V39-05`; do not jump directly to `PL-V39-06`.
