# Change definition

Use in Planning mode to turn a confirmed direction into a bounded proposed change. Do not edit production code.

Follow `CHANGE_LIFECYCLE.md`. Load `disciplines/DOMAIN_MODELING.md` only when domain language or invariants are material.

## Procedure

1. Confirm the selected direction, source Roadmap outcome, source recommendation, or direct user request. When Project Spine is the source, require `project/ROADMAP.md` status = `CURRENT_BASELINE` and use the accepted `NOW` outcome; do not infer priority from historical Roadmaps.
2. Separate repository-answerable facts from user decisions; resolve material facts before freezing scope.
3. Check active work and IDs to avoid duplicate or competing changes.
4. Initialize `.planning/changes/active/CHG-NNNN-short-name/` through `CHANGE_SCAFFOLD.md`.
5. Set lifecycle state to `Definition / In progress`.
6. During definition, draft only:
   - `proposal.md`;
   - `specification.md`;
   - `requirements-checklist.md`.
7. Leave later-stage files in initialized template state.
8. State goal, scope, non-goals, user-visible outcome, interfaces, invariants, constraints, risks, migration or recovery needs, and measurable acceptance criteria.
9. Record exact lineage for the bounded scope. When a Roadmap outcome is the source, record its canonical ID, the direct/dependent Gap refs actually served by this Change, and whether the Change is a partial contribution or genuinely completes the outcome. Link source recommendations in both directions under `RECOMMENDATION_LIFECYCLE.md`; when semantic units exist, record the exact `Source recommendation units` selected by scope rather than implying whole-parent coverage.
10. Preserve the boundaries `Change completion != RoadmapOutcome completion` and `Change completion != Gap closure`; a Roadmap outcome may require several governed Changes.
11. Verify scaffold integrity and confirm no nested `.gitkeep` or unexpected scaffold artifact exists.
12. Set `Definition / Awaiting approval` and ask the user to approve, revise, defer, or reject the definition.

## Approval

Only explicit user confirmation changes the proposal status to `Approved`. After approval, transition to `Planning / In progress`; implementation remains unauthorized.
