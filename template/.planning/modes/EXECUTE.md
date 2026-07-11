# Mode: Execute approved work

## Authorization

Proceed only when Gate D in `APPROVAL_GATES.md` passes. Otherwise switch to Planning or Dialogue / critic and explain the missing gate.

## Minimum context

Read:

- `.planning/ACTIVE.md`;
- active change `context.md`;
- current task block in `tasks.md`;
- relevant plan/specification sections;
- directly affected code and tests;
- applicable project rules.

Do not preload unrelated recommendations, assessments, completed changes, or all planning prompts.

## Execution behavior

1. Confirm the current task and baseline.
2. Make the smallest coherent in-scope change.
3. Follow repository formatting, linting, typing, testing, and architecture conventions.
4. For Python, use readable idiomatic Python and PEP 8. Apply DRY, KISS, YAGNI, and SOLID pragmatically.
5. Verify the task with the stated command or evidence.
6. Mark the task complete only after verification.
7. Update progress and the active context packet at meaningful checkpoints.
8. Report failures, unsupported assumptions, skipped checks, and partial completion honestly.

## Stop conditions

Pause the affected task and switch to Planning or Audit when:

- reality contradicts a requirement or approved assumption;
- a scope amendment is needed;
- data-loss, security, migration, or compatibility risk appears;
- tests expose a broader defect;
- the requested solution would create likely future conflict;
- user instructions conflict with durable project rules.

Implementation-detail deviations may continue only after they are recorded as plan amendments.

## Scope discipline

- Do not “helpfully” implement adjacent ideas.
- Record attractive follow-ups as recommendations.
- A tiny unrelated user-requested edit may use Quick fix mode and the drift ledger.
- Do not rewrite a working subsystem merely for style.

## Session checkpoint

After a meaningful verified batch, update `tasks.md`, `progress.md`, `context.md`, and `.planning/ACTIVE.md`. If context pressure is high or the work is changing phase, prepare a checkpoint and tell the operator whether context compaction or a new session is appropriate. Do not claim to have executed a client-interface action.
