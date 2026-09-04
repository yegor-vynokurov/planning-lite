# Instruction architecture

Planning Lite separates seven concerns:

1. router: select mode and workflow;
2. mode: behavioral constraints;
3. workflow or policy: authoritative operation and authority boundary;
4. discipline: conditional engineering vocabulary and practice;
5. template: artifact schema or canonical pristine scaffold;
6. state: current project truth and lifecycle stage;
7. skill or prompt: thin discovery entry point.

Managed pristine copies under `.planning/templates/` support safe classification, full-file bootstrap materialization, scaffold repair, and optional log initialization without overwriting live project-owned state.

Typical runtime load is `ACTIVE + effective config + one mode + one workflow + targeted project/code context`, plus one discipline only when its terminology changes the operation.

The effective configuration includes one namespaced `project_policy` block.
The central home registry contains only project locators and topology metadata;
project documents and lifecycle history stay in the project. In split-control
mode, `.planning` is an explicit control work tree with external Git metadata;
product and control Git identities are always inspected separately.

For Project Spine direction work, keep completed-state intent (`TARGET_STATE.md`, `CAPABILITY_MODEL.md`), current evidence/decision snapshots (`assessments/current/`), causal direction truth (`GAP_MAP.md`), and explicitly accepted current outcome direction (`ROADMAP.md`) as separate artifact classes. Roadmap synthesis evidence does not become canonical priority until explicit acceptance.
