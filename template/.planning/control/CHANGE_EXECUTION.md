# Change execution

Use in Execution mode only after Gate D is satisfied.

Follow `CHANGE_LIFECYCLE.md`. On valid direct authorization, set lifecycle state to `Execution / In progress` and record the authorized task scope.

## Procedure

1. Verify scaffold integrity and stop on ambiguous or conflicting records.
2. Read `.planning/ACTIVE.md`, active `context.md`, current task, exact relevant plan and specification sections, and targeted code or tests.
3. Execute approved tasks in dependency order, one coherent slice at a time.
4. Keep edits inside approved scope and respect named seams, interfaces, blocking edges, and blast radius.
5. Run the narrowest meaningful check after each slice and configured broader checks at milestones.
6. Update `tasks.md`, append evidence to `progress.md`, and refresh `context.md` at meaningful checkpoints.
7. Do not narrate routine reads, edits, or checks. Report only a blocker, decision, risk, or completed milestone that changes the next action.

## Divergence

When reality differs from the plan, follow `CHANGE_AMENDMENT.md` before continuing the affected work. Do not hide attractive unrelated work inside implementation.

## Completion

When all approved tasks are complete and required implementation checks have run, transition to `Verification / Ready`. Finishing tasks prepares completion review; it does not authorize closure.
