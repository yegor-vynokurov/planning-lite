# Review and close a change

## Goal

Determine whether the approved change is actually complete and update the repository's project memory.

## Procedure

1. Compare implementation with every specification requirement and acceptance criterion.
2. Run or inspect the promised verification and record exact outcomes in `review.md`.
3. Apply `.planning/project/DEFINITION_OF_DONE.md` and record exceptions.
4. Review compatibility, migration, rollback, recovery, repeated execution, and documentation as applicable.
5. Identify residual limitations, defects, risks, and follow-up opportunities.
6. Create recommendation items for non-blocking follow-ups.
7. Decide:
   - Completed;
   - Completed with accepted limitations;
   - Not complete.
8. Update:
   - `.planning/project/CURRENT_STATE.md`;
   - completion-criteria evidence and statuses;
   - architecture overview;
   - roadmap;
   - recommendation index;
   - decision index;
   - `.planning/ACTIVE.md`.
9. If complete, move the folder from `changes/active/` to `changes/completed/` without losing history.

## Integrity rule

A checked task list is not sufficient evidence. Completion requires observable outcomes and the applicable Definition of Done.
