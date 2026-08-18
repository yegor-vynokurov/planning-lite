# Target-State explorer

- Workflow ID: `PW-DIR-002`
- Workflow version: `1.0.0`
- Source lineage: `REC-PL-DIRECTION-001-v2` / Poker Project Spine pilot
- Mode: Planning

Use to draft or materially revise the desired completed state of a project after direction authority and current-state consistency are sufficiently established.

This workflow may create or revise a **draft** Target State. It does not accept the Target, derive Gaps, prioritize work, create a Change, or authorize implementation.

## Preconditions

Prefer a current `.planning/assessments/current/direction-inventory.md` with:

```text
Current-State Consistency Gate: PASS
```

If no such evidence exists or material direction authority may have changed, route to `DIRECTION_INVENTORY.md` first.

## Allowed write scope

May update only:

- `.planning/project/TARGET_STATE.md`;
- `.planning/ACTIVE.md` when recording the next planning gate.

If the user decision also requires a charter/completion-criteria rewrite, record that decision and route the durable-document refresh separately instead of broadening this workflow.

Do not edit `.planning/project/CAPABILITY_MODEL.md` in this workflow.

## Deliverable class first

Establish the intended deliverable class before expanding detailed Target properties. Examples include:

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

Do not infer a maintained product merely because the repository contains executable code, adapters, a CLI, or an old integration idea.

If materially different deliverable classes remain plausible and would change required capabilities, surface the choice to the user instead of averaging them together.

## Perspective sweep

Use only the perspectives relevant to the project, but deliberately check each before declaring the draft complete:

```text
PURPOSE
PRIMARY AUDIENCE
KEY JOURNEYS OR REVIEW PATHS
FUNCTIONAL OUTCOMES
CORRECTNESS / VERIFIABILITY
FAILURE / RECOVERY
DATA / SOURCE OF TRUTH
SAFETY / MISUSE
OBSERVABILITY / EXPLAINABILITY
PERFORMANCE / COST
OPERABILITY
API / INTEGRATION
EVOLUTION
HUMAN CONTROL
NON-GOALS
```

The Target describes durable desired outcomes, not file edits, implementation tasks, or speculative architecture.

## Claim provenance

Direction-inventory source classes map into Target claim provenance rather than being copied blindly:

```text
EXPLICIT_USER_DECISION     → USER_DECISION
CURRENT_PROJECT_DIRECTION  → EXISTING_DIRECTION
REPOSITORY_EVIDENCE        → REPOSITORY_EVIDENCE
INFERRED                    → INFERRED
UNRESOLVED                  → UNRESOLVED
HISTORICAL_DIRECTION        → historical evidence only; not a Target claim source unless re-accepted
```

Every material Target claim must carry one source class:

- `USER_DECISION`;
- `EXISTING_DIRECTION`;
- `REPOSITORY_EVIDENCE`;
- `INFERRED`;
- `UNRESOLVED`.

`INFERRED` claims are draft synthesis only. They do not become accepted project authority merely because they are written into the draft.

Repository evidence may establish feasibility or current facts, but current implementation does not automatically define the desired Target.

## Procedure

1. Read the current direction inventory, charter, completion criteria, existing Target State, Roadmap only where it carries accepted direction, and targeted evidence needed for disputed claims.
2. Establish or surface the deliverable-class decision.
3. Draft purpose, primary audience, successful-completion meaning, key journeys, and explicit non-goals.
4. Run the perspective sweep and add only material Target properties.
5. Tag material claims with source class and evidence/decision anchors.
6. Record unresolved questions without forcing them into implementation detail.
7. Keep status `DRAFT`.
8. Route the result to `TARGET_BASELINE_CALIBRATION.md`.

## Hard checks

- `CHK-TARGET-QUALITY-001`: deliverable class is explicit or recorded as a blocking Target question.
- `CHK-TARGET-QUALITY-002`: required Target properties describe outcomes/capabilities, not tasks or files.
- `CHK-TARGET-QUALITY-003`: non-goals are explicit enough to prevent known historical scope from silently re-entering.
- `CHK-TARGET-QUALITY-004`: agent inference is visibly distinguishable from user/current-direction authority.
- `CHK-TARGET-QUALITY-005`: current architecture or implementation is not treated as the Target merely because it exists.

## Output contract

Report the draft Target path, deliverable class, strongest accepted/current direction anchors, inferred claims, unresolved Target questions, explicit non-goals, and the calibration gate. Do not create implementation tasks or Gaps.
