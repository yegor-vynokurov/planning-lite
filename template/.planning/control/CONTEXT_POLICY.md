# Context policy

Presence on disk does not imply loading.

## Tier 0: always small

Read only:

1. the root `AGENTS.md` bridge;
2. `.planning/ACTIVE.md`;
3. effective configuration through `CONFIG_RESOLUTION.md`;
4. one selected mode.

## Tier 1: one operation

Load at most one authoritative functional workflow for the current operation. A skill or numbered prompt should route to it, not duplicate it.

For active work, prefer the active change `context.md`, current `tasks.md` section, exact relevant requirements, and targeted code or tests.

## Tier 2: governing project context

Read only applicable sections of project rules, completion criteria, Definition of Done, architecture, repository map, roadmap, or named decisions.

## Tier 3: history on demand

Load assessments, completed changes, old recommendations, drift history, raw diffs, and archives only for a concrete question.

## Discovery rules

- Use `project/REPOSITORY_MAP.md` before broad exploration, then verify relevant claims.
- A full repository rescan requires a stated reason.
- Prefer exact paths, symbols, tests, and line ranges.
- Read templates only when creating that artifact.
- Never load all prompts, skills, recommendations, or adapters by default.
- After a fresh conversation, resume from durable state rather than rescanning automatically.

## Context packet

The active change `context.md` is the resumable packet. Keep it compact and update it at meaningful checkpoints, decisions, amendments, or before a new session.
