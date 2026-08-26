# Planning Lite

Planning Lite is a repository-local control system for human-guided coding agents. It keeps durable project state in files while loading only the instructions needed for the current operation.

## Runtime architecture

- `control/`: authoritative policies, lifecycle, and functional workflows.
- `modes/`: short behavioral contracts.
- `disciplines/`: conditionally loaded engineering vocabulary and practice.
- `skills/`: thin agent-discoverable entry points with response contracts.
- `prompts/`: short human-facing entry points that route to one workflow.
- `templates/`: managed canonical pristine copies and scaffolds used for safe materialization and repair.
- `project/`, `changes/`, `recommendations/`, `decisions/`, `assessments/`, `drift/`, `observability/`: durable project-owned state. Project direction is represented explicitly by `project/TARGET_STATE.md`, `project/CAPABILITY_MODEL.md`, `project/GAP_MAP.md`, and an explicitly accepted `project/ROADMAP.md`; formal current capability coverage and Roadmap/reconciliation decision evidence live in `assessments/current/` snapshots.
- `adapters/`: client-specific invocation and operator guidance.

## Reading rule

Start from `.planning/ACTIVE.md`, effective configuration, one mode, one functional workflow, and at most one relevant discipline. Do not preload the entire tree.

## Source-of-truth rule

Router selects the route. Mode defines behavior. Workflow defines the operation. Policy defines authority. Discipline supplies engineering language. Template defines fields. State records current truth. Skill exposes the route.

<!-- PL_FCP_RECOMMENDATION_ENTRY_V1:BEGIN -->
## Discovery and Recommendation accounting

Planning Lite distinguishes:

```text
Discovery
→ durable observation without executable authority

Recommendation
→ durable proposed action governed by the Recommendation lifecycle

Recommendation Absorption
→ manual unit-aware accounting of existing Recommendation meaning/residue
```

Primary controls:

```text
.planning/control/DISCOVERY_LIFECYCLE.md
.planning/control/RECOMMENDATION_LIFECYCLE.md
.planning/control/RECOMMENDATION_ABSORPTION.md
```

Absorption does not create a second Recommendation lifecycle and does not
automatically mutate the Roadmap or create a Change.
<!-- PL_FCP_RECOMMENDATION_ENTRY_V1:END -->
