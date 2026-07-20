# Change closure

## Purpose

Use this workflow in Audit mode to review and, when authorized, close an approved change. Completion review and final closure are separate operations. This workflow does not authorize production-code edits.

## Authorization boundary

A request to review, inspect, or audit authorizes preparation of the completion verdict only. It does not authorize moving the change folder, clearing `.planning/ACTIVE.md`, or finalizing recommendation statuses.

Closure is authorized only when the user explicitly asks to close the change or approves the proposed verdict. `Completed with accepted limitations` requires explicit acceptance of those limitations.

## Minimum context

Read:

1. `.planning/ACTIVE.md`, Audit mode, and `CHANGE_SCAFFOLD.md`;
2. this workflow and applicable Definition of Done sections;
3. the active change proposal, specification, requirements checklist, plan, tasks, amendments, progress, context, readiness, and review;
4. every source recommendation and the recommendation index;
5. `GIT_CHANGE_REVIEW.md` for a non-trivial change.

Read other project documents only when the delivered change may have made them stale.

## Completion verdicts

Use exactly one:

- `Completed`: all mandatory acceptance criteria pass, required verification and Definition of Done requirements are satisfied, and no blocker remains.
- `Completed with accepted limitations`: all mandatory criteria still pass; limitations are non-blocking and explicitly accepted.
- `Not complete`: a mandatory criterion fails, required evidence is missing, unresolved drift or critical risk remains, or closure integrity cannot be established.

A failed mandatory criterion is not an accepted limitation.

## Completion review

1. Verify scaffold integrity through `CHANGE_SCAFFOLD.md`; restore only missing initialized files and preserve populated records.
2. Identify the change, branch, working-tree state, and bounded implementation commit range.
3. Compare delivered behavior with approved scope, non-goals, criteria, plan, and amendments.
4. Record `Pass`, `Fail`, or `Partial` and exact evidence for every acceptance criterion.
5. Apply relevant Definition of Done categories.
6. Separate blockers, accepted limitations, follow-up recommendations, and unrelated observations.
7. Complete `review.md` with the proposed verdict.
8. If closure is not already authorized, stop and request approval of the verdict.

Checked task boxes are not completion evidence.

## Recommendation reconciliation

For every source recommendation:

1. open the item and verify the change link;
2. determine `Full`, `Partial`, or `None` coverage;
3. update `Last reviewed`, the item, the index, and the matching row in `review.md`;
4. apply `RECOMMENDATION_LIFECYCLE.md`.

Do not mark a recommendation `Completed` merely because one linked change completed. Resolve item/index disagreement before closure.

## Project-memory synchronization

Update only factual documents made stale by the delivered work, using `PROJECT_STATE_REFRESH.md`. Create follow-up recommendations only for durable non-blocking work outside approved scope.

## Final closure

After authorization:

1. finalize tasks, progress, context, amendments, and review;
2. reconcile recommendations and affected project memory;
3. move `.planning/changes/active/<change-folder>/` to `.planning/changes/completed/<change-folder>/`;
4. reset only the active-change section of `.planning/ACTIVE.md`;
5. do not automatically activate another change.

## Integrity checks

Before reporting closure, verify:

- the completed folder exists exactly once and no active copy remains;
- `review.md` contains verdict, authorization, date, and final location;
- acceptance evidence and change records are consistent;
- recommendation items, index, and review agree;
- `.planning/ACTIVE.md` no longer points to the closed change;
- affected project documents contain no stale active-change facts;
- Git status contains no unexpected artifacts;
- closure edited no production code.

If any check fails, report closure as blocked.

## Output contract

Report verdict, authorization state, verification summary, planning records updated, final location, recommendation transitions, follow-ups, and the next permitted action.
