# Session checkpoint

Use when the user requests a checkpoint, prepares for context compaction, a new conversation, or an agent switch.

## Boundary

Stop production-code edits while checkpointing. A checkpoint preserves the current lifecycle stage; it does not advance, verify, or close a change. The agent does not claim to execute client UI actions such as `/compact` or `/new`.

## Procedure

1. Follow `CHANGE_LIFECYCLE.md` and normalize legacy lifecycle fields when needed.
2. Verify current mode, active change, lifecycle stage, current task, blockers, and authorization.
3. Update task states in `tasks.md`.
4. Append meaningful work and verification to `progress.md`.
5. Refresh compact `context.md` with exact files, symbols, commands, decisions, blockers, and next reads.
6. Update `.planning/ACTIVE.md` with unchanged stage, checkpoint reference, next gate, and next permitted action.
7. Record branch, HEAD, status, stats, changed paths, staged state, and bounded commit range. Avoid a full raw diff.
8. Report only checkpoint readiness, files updated, compact Git state, blocker, and next action.
