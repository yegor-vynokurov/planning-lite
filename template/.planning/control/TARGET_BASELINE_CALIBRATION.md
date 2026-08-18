# Target baseline calibration and Capability Model foundation

- Workflow ID: `PW-DIR-003`
- Workflow version: `1.0.0`
- Source lineage: `REC-PL-DIRECTION-001-v2` / Poker Project Spine pilot
- Mode: Planning

Use after a Target-State draft exists. The workflow separates true Target-boundary uncertainty from downstream design/research questions, establishes a provisional or explicitly accepted Target baseline, and derives the first Capability Model.

It does not assess current capability coverage, derive Gaps, reconcile recommendations, synthesize the Roadmap, or create a Change.

## Allowed write scope

May update only:

- `.planning/project/TARGET_STATE.md`;
- `.planning/project/CAPABILITY_MODEL.md`;
- `.planning/ACTIVE.md` for the next planning gate.

## Question ownership

Every unresolved material question must be assigned exactly one owner class:

- `TARGET_BOUNDARY_QUESTION`: the answer could materially change project purpose, deliverable class, primary audience, required completed-state properties, or explicit non-goals;
- `CAPABILITY_DESIGN_QUESTION`: the Target can remain stable while implementation/interface/design choices remain open inside one capability;
- `RESEARCH_QUESTION`: the Target can remain stable while evidence must determine whether a hypothesis, model, method, or intervention works.

Only `TARGET_BOUNDARY_QUESTION` blocks Target convergence.

Do not keep the whole project in Target discovery merely because capability design or research remains uncertain.

## Target statuses

Canonical statuses:

```text
DRAFT
PROVISIONAL_TARGET_BASELINE
ACCEPTED
```

Rules:

- `DRAFT`: material Target-boundary questions remain, or calibration is incomplete.
- `PROVISIONAL_TARGET_BASELINE`: no unresolved Target-boundary question remains, provenance/non-goals are coherent, but explicit user acceptance has not yet been recorded.
- `ACCEPTED`: the user explicitly accepts the Target as the current project-direction baseline.

An agent must never promote `PROVISIONAL_TARGET_BASELINE` to `ACCEPTED` without explicit user authority.

## Target flow-back rule

Ordinary implementation discoveries do not silently rewrite the Target.

A future Target revision requires one of:

```text
explicit user/durable authority decision
or
explicit TARGET_STATE_SIGNAL
```

A `TARGET_STATE_SIGNAL` is a recorded discovery showing that an accepted Target assumption, boundary, audience, deliverable class, or required property is materially wrong or impossible. It routes back to direction calibration; it does not authorize an automatic Target edit.

## Capability Model

After the Target reaches at least `PROVISIONAL_TARGET_BASELINE`, derive a bounded Capability Model.

Capability Model statuses are:

```text
DRAFT
CURRENT_BASELINE
```

`CURRENT_BASELINE` requires explicit user acceptance of the presented Capability Model. Target acceptance and Capability-Model acceptance may occur in the same user decision, but neither is inferred from the other.

A capability is a durable property the completed project must exhibit. It is not:

- a task;
- a file;
- a Change;
- a technology choice by itself;
- a claim that the capability is currently satisfied.

Use stable IDs such as `CAP-001`, `CAP-002`, ... within the project.

Each capability should record:

```text
Capability ID
Capability name
Target property or journey served
Successful completed-state meaning
Evidence expected when complete
Owned CAPABILITY_DESIGN_QUESTION / RESEARCH_QUESTION items
```

Current satisfaction, `PARTIAL`, `SATISFIED`, evidence confidence, and causal Gaps belong to the later Current Capability Assessment workflow, not this file.

## Procedure

1. Read the current direction inventory, Target draft, charter/completion criteria, and only targeted evidence needed to adjudicate Target-boundary questions.
2. Reclassify every material unresolved question by owner class.
3. Remove implementation detail that accidentally entered the Target.
4. Verify explicit non-goals against known historical scope pressure.
5. If any Target-boundary question remains, keep `DRAFT` and stop before presenting the Target as a baseline.
6. If no Target-boundary question remains, set `PROVISIONAL_TARGET_BASELINE`.
7. Derive or refresh `CAPABILITY_MODEL.md` from the calibrated Target.
8. Present the calibrated Target and Capability Model as the direction baseline. If the user explicitly accepts the Target, record evidence and set Target status `ACCEPTED`. If the user explicitly accepts the Capability Model, record evidence and set its status `CURRENT_BASELINE`.
9. Downstream Current Capability Assessment requires both an `ACCEPTED` Target and a `CURRENT_BASELINE` Capability Model.
10. Do not assess current coverage or derive Gaps.

## Hard checks

- `CHK-TARGET-CALIBRATION-001`: every unresolved material question has exactly one owner class.
- `CHK-TARGET-CALIBRATION-002`: zero Target-boundary questions are required for `PROVISIONAL_TARGET_BASELINE`.
- `CHK-TARGET-CALIBRATION-003`: `ACCEPTED` has explicit user/authority evidence.
- `CHK-TARGET-CALIBRATION-004`: Capability Model entries are outcome-oriented and map back to Target properties/journeys.
- `CHK-TARGET-CALIBRATION-005`: current implementation status is absent from Capability Model semantics.
- `CHK-TARGET-CALIBRATION-006`: `CURRENT_BASELINE` Capability Model has explicit user acceptance evidence.
- `CHK-TARGET-CALIBRATION-007`: Target flow-back requires explicit authority or `TARGET_STATE_SIGNAL`.

## Output contract

Report Target status, Target-boundary question count, downstream design/research questions, Capability Model path and capability count, acceptance evidence when present, and the next permitted action. Do not derive Gaps or create a Change.
