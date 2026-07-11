# Context and token policy

The repository may contain many prompts and historical artifacts. Presence on disk does not mean every file should be loaded into every request.

## Progressive reading

### Tier 0: always small

- `AGENTS.md` is discovered by the agent platform.
- Read `.planning/ACTIVE.md`.
- Read the effective configuration using `.planning/control/CONFIG_RESOLUTION.md`.
- Read one selected mode file.
- Use `.planning/project/REPOSITORY_MAP.md` as the default discovery index when code locations are not already named.

### Tier 1: current work only

For an active change, prefer:

- `<active-change>/context.md`;
- current section of `tasks.md`;
- exact relevant sections of `specification.md` and `plan.md`;
- directly affected code and tests.

Do not read the full change folder when the current task can be understood from the context packet and targeted sections. Do not repeat a repository-wide scan merely because a new conversation started.

### Tier 2: governing context when relevant

Read only applicable sections from:

- `project/PROJECT_RULES.md`;
- `project/PROJECT_COMPLETION_CRITERIA.md`;
- `project/DEFINITION_OF_DONE.md`;
- `project/ARCHITECTURE_OVERVIEW.md`;
- ADRs named by the active change.

### Tier 3: history on demand

Load assessments, completed changes, recommendation history, old drift reports, Git history, and archived documents only when they answer a concrete question.

## Repository map

`project/REPOSITORY_MAP.md` is a discovery cache, not an unquestioned source of truth. Read it before broad exploration, then verify the rows relevant to the current task. Update affected rows after architectural, entry-point, data-flow, or test-layout changes.

A full repository rescan requires an explicit reason such as initial bootstrap, conflicting evidence, major structural change, or a user-requested full audit. Record the revision and scope used to refresh the map.

## Active change context packet

Every active change contains `context.md`, kept below the configured line limit. It should summarize:

- approved outcome and exclusions;
- current stage and task;
- key constraints and decisions;
- relevant files and symbols;
- verification commands;
- unresolved blockers;
- exact documents to read next.

Update it after a meaningful checkpoint, plan amendment, user decision, or before ending a long session. Do not copy whole specifications into it.

## Reading behavior

- Start with the configured soft limit of files, then expand only when a named uncertainty requires it.
- Prefer targeted search, exact paths, symbols, line ranges, and test names over broad repository dumps.
- Read templates only when creating that artifact.
- Read one prompt at a time. Prompts are entry points, not a mandatory bundle.
- Do not load every recommendation to work on one recommendation; use the index and named IDs.
- Do not load completed changes unless compatibility or precedent depends on them.
- Avoid duplicating the same rule across AGENTS, mode files, plans, and prompts. Link to the authoritative source.

## Avoiding repeated repository reads

1. Start from `REPOSITORY_MAP.md` and the active `context.md`.
2. Name the uncertainty to resolve.
3. Search for exact symbols, imports, entry points, tests, or configuration keys.
4. Read only matching ranges and directly connected code.
5. Expand outward only when the evidence contradicts the map or the task crosses a documented boundary.
6. Update the map when the discovered structure is durable.

## Git context discipline

At checkpoint time, collect Git summaries first: branch, HEAD, status, stats, file names, staged state, and a bounded commit range. Do not load a full repository diff automatically. When review is required, follow `GIT_CHANGE_REVIEW.md`: summary first, then targeted high-risk patches. Store commit IDs, paths, findings, and verdicts; keep raw patches in Git.

## Conversation maintenance

Before compacting context or starting a fresh session:

1. invoke the checkpoint workflow or follow `SESSION_CHECKPOINT.md`;
2. update the active change `tasks.md`, `context.md`, and `progress.md`;
3. update `.planning/ACTIVE.md` with the next permitted action;
4. record unresolved user decisions and compact Git state;
5. then let the operator use the active client’s context-compaction or new-session feature.

Client-specific commands belong to `.planning/adapters/<agent>/`. They are operator actions: the agent prepares the checkpoint and may recommend the mapped action, but must not claim it ran. After compaction or a new session, verify mode, active change, current task, blockers, Git state, and approval state.

## Canonical skills and adapters

Canonical workflows live under `.planning/skills/` and follow the Agent Skills format. The active adapter may expose thin wrappers or external-directory references. Only the selected skill body should load for a request.

Do not load every skill or every adapter guide. Read `.planning/AGENT_PROFILE.yml` and the active adapter only when client-specific syntax or capabilities matter.
