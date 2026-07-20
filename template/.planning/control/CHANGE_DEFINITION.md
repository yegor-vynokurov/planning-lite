# Change definition

Use in Planning mode to turn an accepted direction into a bounded proposed change. Do not edit production code.

## Procedure

1. Confirm the source recommendation or direct user request.
2. Check active work and IDs to avoid duplicate or competing changes.
3. Initialize `.planning/changes/active/CHG-NNNN-short-name/` through `CHANGE_SCAFFOLD.md`.
4. During definition, draft only:
   - `proposal.md`;
   - `specification.md`;
   - `requirements-checklist.md`.
5. Leave `plan.md`, `tasks.md`, `readiness.md`, `amendments.md`, `progress.md`, `context.md`, and `review.md` in their initialized template state until the matching workflow authorizes their use.
6. State goal, scope, non-goals, affected contracts, constraints, risks, migration or recovery needs, and measurable acceptance criteria.
7. Surface material unknowns and alternatives before freezing the definition.
8. Link every source recommendation in both directions under `RECOMMENDATION_LIFECYCLE.md`.
9. Verify scaffold integrity and confirm that the change folder contains no nested `.gitkeep` or unexpected scaffold artifact.
10. Ask the user to approve, revise, defer, or reject the proposed definition.

## Approval

Only explicit user confirmation changes the proposal status to `Approved`. After approval, update `.planning/ACTIVE.md` to stage `Planning`; implementation remains unauthorized.
