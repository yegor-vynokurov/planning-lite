# Planning Lite v2.3

Planning Lite is a repository-local, model- and agent-portable workflow for human-guided coding agents. It separates durable project state from client-specific commands and skill discovery.

The package does not require a dedicated CLI. Codex is enabled by default through thin wrappers under `.agents/skills/`. Claude Code and Hermes adapters are included as architecture-ready templates but are not activated automatically.

## Architecture

```text
Neutral repository core
  AGENTS.md
  .planning/project + changes + state
  .planning/control + modes + prompts
  .planning/skills (canonical Agent Skills)
                    |
                    v
Agent adapter
  instruction bridge
  skill exposure path
  invocation syntax
  operator commands / hooks
                    |
                    v
Codex / Claude Code / Hermes / generic agent
```

## Core model

```text
Project goal + completion criteria + durable rules
                         |
                         v
             Evidence-based assessment
                         |
                         v
          Recommendations / opportunity backlog
                         |
              explicit human decision
                         v
    Change proposal + specification + acceptance criteria
                         |
              interactive planning dialogue
                         v
              plan + tasks + audit
                         |
              direct execution command
                         v
           implementation + verification
                         |
               review + project sync
```

Tiny low-risk corrections may use a controlled side path:

```text
explicit quick-fix request -> narrow edit -> verification
-> QUICK_CHANGES ledger -> periodic or immediate drift sync
```

## Neutral core

The following survive an agent or model switch:

- project goals, rules, completion criteria, architecture map, and Definition of Done;
- assessments, recommendations, approved changes, plans, tasks, decisions, and reviews;
- `ACTIVE.md`, context packets, checkpoints, Git ranges, and verification evidence;
- modes, approval gates, drift and recovery policies;
- canonical skills under `.planning/skills/`.

## Adapters

`.planning/adapters/` contains the capability registry and adapter documentation.

- Codex: active; `.agents/skills/` contains thin wrappers.
- Claude Code: templates for `CLAUDE.md` and `.claude/skills/` wrappers.
- Hermes: guidance for using `.planning/skills/` as an external skills directory.
- Generic: natural-language and direct-file fallback.

Read `.planning/control/AGENT_PORTABILITY.md` before changing the primary agent shell or model.

## Context principle

Do not read the whole `.planning/` tree by default. Start from `ACTIVE.md`, one mode file, the active context packet, and the one selected canonical skill. Expand only for a concrete uncertainty.

## Session control

Say `make checkpoint` or invoke the logical skill `planning-checkpoint` to freeze code edits, update durable state, and prepare for context compaction or a new session. Client-specific interface actions remain operator actions.

Use `planning-git-review` only when requested, triggered by semantic risk or thresholds, or before closing a non-trivial change. Git review starts with summaries and bounded ranges, then opens targeted patches.

## Framework and project ownership

Planning Lite is installed from a central versioned template.

- Centrally managed workflow files are listed in `.planning/framework/OWNERSHIP.yml`.
- Project goals, active changes, recommendations, decisions, configuration overrides, and runtime state are project-owned.
- `.planning/framework/defaults.yml` is updated centrally; `.planning/CONFIG.yml` contains only local overrides.
- The root `AGENTS.md` is a small project-owned bridge to the managed `.planning/control/ROOT_ROUTER.md`.

Do not edit `.copier-answers.planning-lite.yml` manually.
