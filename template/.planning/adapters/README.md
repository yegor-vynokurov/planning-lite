# Agent adapters

Planning Lite separates a neutral repository workflow from the agent shell that exposes it.

## Neutral core

The following remain unchanged when switching agents or models:

- `.planning/project/`, assessments, recommendations, changes, decisions, and drift records;
- `.planning/control/`, `.planning/modes/`, and `.planning/prompts/`;
- canonical skills under `.planning/skills/`;
- `AGENTS.md`, which contains tool-neutral routing and approval rules;
- Git history, tests, checkpoints, and active context packets.

## Adapter responsibilities

An adapter may define only:

1. which persistent instruction file the client reads;
2. where project skills must be exposed;
3. explicit skill invocation syntax;
4. operator-only commands for compaction, new sessions, forks, or plan modes;
5. optional hooks or permissions that enforce boundaries more strictly.

Adapters must not redefine project scope, approval gates, Definition of Done, or change state.

## Available architectural adapters

- `codex/`: active by default in this package.
- `claude-code/`: ready-to-materialize templates; not activated automatically.
- `hermes/`: external-skill-directory approach; not activated automatically.
- `generic/`: natural-language and direct-file fallback.

Use `registry.yml` as a machine-readable capability map. Current client commands should be verified against the installed client before activation.
