# Planning Lite

Planning Lite is a repository-local control system for human-guided coding agents. It keeps durable project state in files while loading only the instructions needed for the current operation.

## Runtime architecture

- `control/`: authoritative policies, lifecycle, and functional workflows.
- `modes/`: short behavioral contracts.
- `disciplines/`: conditionally loaded engineering vocabulary and practice.
- `skills/`: thin agent-discoverable entry points with response contracts.
- `prompts/`: short human-facing entry points that route to one workflow.
- `templates/`: managed canonical pristine copies and scaffolds used for safe materialization and repair.
- `project/`, `changes/`, `recommendations/`, `decisions/`, `assessments/`, `drift/`, `observability/`: durable project-owned state.
- `adapters/`: client-specific invocation and operator guidance.

## Reading rule

Start from `.planning/ACTIVE.md`, effective configuration, one mode, one functional workflow, and at most one relevant discipline. Do not preload the entire tree.

## Source-of-truth rule

Router selects the route. Mode defines behavior. Workflow defines the operation. Policy defines authority. Discipline supplies engineering language. Template defines fields. State records current truth. Skill exposes the route.
