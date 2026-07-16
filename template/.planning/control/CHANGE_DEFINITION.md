# Change definition

Use in Planning mode to turn an accepted direction into a bounded proposed change. Do not edit production code.

## Procedure

1. Confirm the source recommendation or direct user request.
2. Check active work and IDs to avoid duplicate or competing changes.
3. Create `.planning/changes/active/CHG-NNNN-short-name/` from the templates.
4. Draft `proposal.md`, `specification.md`, and `requirements-checklist.md`.
5. State goal, scope, non-goals, affected contracts, constraints, risks, migration or recovery needs, and measurable acceptance criteria.
6. Surface material unknowns and alternatives before freezing the definition.
7. Link every source recommendation in both directions under `RECOMMENDATION_LIFECYCLE.md`.
8. Ask the user to approve, revise, defer, or reject the proposed definition.

## Approval

Only explicit user confirmation changes the proposal status to `Approved`. After approval, update `.planning/ACTIVE.md` to stage `Planning`; implementation remains unauthorized.
