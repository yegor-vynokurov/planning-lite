# Planning Lite

Planning Lite is a repository-local control system for human-guided coding agents.
It keeps durable project state in files while loading only the instructions needed for the current operation.

## Runtime architecture

- `control/`: authoritative policies and functional workflows.
- `modes/`: short behavioral contracts.
- `skills/`: thin agent-discoverable entry points with response contracts.
- `prompts/`: short human-facing entry points that route to one workflow.
- `project/`, `changes/`, `recommendations/`, `decisions/`, `assessments/`, `drift/`: durable project-owned state.
- `adapters/`: client-specific invocation and operator guidance.

## Reading rule

Start from `.planning/ACTIVE.md`, effective configuration, one mode, and at most one functional workflow.
Do not preload the entire tree.

## Source-of-truth rule

Router decides where to go. Mode defines how to behave. Workflow defines what to do. Policy defines what is allowed. Template defines what to record. State records what is true now. Skill exposes the route to an agent.
