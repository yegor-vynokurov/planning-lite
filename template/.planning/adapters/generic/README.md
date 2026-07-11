# Generic agent adapter

Use this fallback when an agent can read repository files but has no native `AGENTS.md` or Agent Skills integration.

At session start, explicitly ask the agent to read `AGENTS.md`. Invoke workflows by natural language or by naming the canonical file, for example:

- `Use the planning-checkpoint skill from .planning/skills/planning-checkpoint/SKILL.md.`
- `Use Planning mode and prepare a planning brief. Do not edit production code.`

The agent must still obey approval gates and maintain durable state. Client-specific context-management actions remain operator actions.
