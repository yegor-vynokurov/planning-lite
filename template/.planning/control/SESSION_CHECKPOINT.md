# Session checkpoint

Use when the user requests a checkpoint, prepares for context compaction, a new conversation, or an agent switch.

## Boundary

Stop production-code edits while checkpointing. The agent prepares durable state but does not claim to execute client UI actions such as `/compact` or `/new`.

## Procedure

1. Verify current mode, active change, current task, blockers, and authorization.
2. Update task states in `tasks.md`.
3. Append meaningful work and verification to `progress.md`.
4. Refresh the compact `context.md` with exact files, symbols, commands, decisions, blockers, and next reads.
5. Update `.planning/ACTIVE.md` with the next permitted action and checkpoint reference.
6. Record branch, HEAD, status, stats, changed paths, staged state, and bounded commit range. Avoid a full raw diff.
7. Report readiness for the operator's next context action.
