# Assessments

Assessments are evidence-based snapshots. They may update factual project state and propose recommendations, but they do not authorize implementation.

Formal whole-project capability assessment uses `CURRENT_CAPABILITY_ASSESSMENT_TEMPLATE.md` and `control/CURRENT_CAPABILITY_ASSESSMENT.md`; informal assessment gaps are not formal Project Spine Gap identities.

Project Spine historical reconciliation uses `DIRECTION_HISTORY_RECONCILIATION_TEMPLATE.md` with `control/RECOMMENDATION_HISTORY_RECONCILIATION.md`. It is a lineage/residue snapshot and does not authorize Roadmap priority or implementation.

Roadmap synthesis/prioritization uses `ROADMAP_SYNTHESIS_TEMPLATE.md` with `control/ROADMAP_SYNTHESIS_PRIORITIZATION.md`. It is decision evidence until explicit acceptance; accepted current priority lives in project-owned `ROADMAP.md`, and no Change is created by the synthesis workflow.

<!-- PL_V39_05_A_PROJECT_SURVEY_DOC_V1:BEGIN -->
## Project Survey

`PROJECT_SURVEY_TEMPLATE.md` is a managed pristine template for an optional,
bounded AS-IS evidence snapshot.

When `PW-DIR-004 CURRENT_CAPABILITY_ASSESSMENT` satisfies its three-part Survey
trigger, materialize project-owned evidence at:

```text
.planning/assessments/current/PROJECT_SURVEY.md
```

The trigger requires all three:

```text
material brownfield/current-state work
AND
assessment depends on repository/runtime structure
AND
existing current evidence is not sufficiently bounded/fresh
```

Routine or small work may bypass Project Survey.

Authority boundary:

```text
SURVEY = AS-IS EVIDENCE
TARGET = TO-BE ACCEPTED INTENT
```

Project Survey does not own or replace Current State, Current Capability
Assessment, Capability Model, Gap Map, Target State, or Roadmap.

A Survey records `Reflects revision`, `Survey scope`, and `Evidence sources`.
Refresh or narrow it only when material repository/runtime drift occurs or active
work leaves the surveyed scope. Unrelated minor drift does not automatically
invalidate it.

Ownership/update boundary:

```text
managed:
.planning/assessments/PROJECT_SURVEY_TEMPLATE.md

project-owned:
.planning/assessments/current/PROJECT_SURVEY.md
```

The managed template may update with Planning Lite. A materialized current Survey
belongs to the consumer project and must be preserved by update behavior.
<!-- PL_V39_05_A_PROJECT_SURVEY_DOC_V1:END -->


<!-- PL_V39_05_B_RECOVERY_LADDER_DOC_V1:BEGIN -->
## Brownfield Recovery + Outcome Ladder

Managed templates:
```text
.planning/assessments/BROWNFIELD_RECOVERY_TEMPLATE.md
.planning/assessments/OUTCOME_LADDER_TEMPLATE.md
```

Project-owned materializations:
```text
.planning/assessments/current/BROWNFIELD_RECOVERY.md
.planning/assessments/current/OUTCOME_LADDER.md
```

Brownfield Recovery is bounded provenance/direction evidence. It supports
`REUSE_CURRENT_ACCEPTED_DIRECTION` or a
`RECOVERED_DIRECTION_CANDIDATE / PROVISIONAL`, and it never accepts Target intent
by itself. Recovery stops on `BR-STOP-01` through `BR-STOP-04`.

Outcome Ladder describes increasingly strong observable project outcomes. It
inherits the authority ceiling of its grounding direction, is not a Roadmap or
task sequence, and records a minimum useful stopping level.

Managed templates may update with Planning Lite. Materialized current artifacts
belong to the consumer project and must be preserved by update behavior.
<!-- PL_V39_05_B_RECOVERY_LADDER_DOC_V1:END -->
