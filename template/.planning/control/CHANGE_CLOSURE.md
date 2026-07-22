# Change closure

Use in Audit mode to review and, when authorized, close an approved change. Completion review and final closure are separate operations. This workflow does not authorize production-code edits.

Follow `CHANGE_LIFECYCLE.md`, `CHANGE_SCAFFOLD.md`, and `disciplines/CODE_REVIEW.md`.

## Authorization boundary

A request to review, inspect, or audit authorizes preparation of the completion verdict only. It does not authorize moving the change folder, clearing `.planning/ACTIVE.md`, or finalizing recommendation statuses.

Closure is authorized only when the user explicitly asks to close the change or approves the proposed verdict. `Completed with accepted limitations` requires explicit acceptance of those limitations.

## Minimum context

Read `.planning/ACTIVE.md`, applicable Definition of Done sections, all active change records, source recommendations and index, and `GIT_CHANGE_REVIEW.md` for a non-trivial change. Read other project documents only when delivery may have made them stale.

## Completion verdicts

Use exactly one:

- `Completed`: all mandatory criteria pass, required verification and standards requirements are satisfied, and no blocker remains.
- `Completed with accepted limitations`: all mandatory criteria still pass; limitations are non-blocking and explicitly accepted.
- `Not complete`: a mandatory criterion fails, required evidence is missing, unresolved drift or critical risk remains, or closure integrity cannot be established.

A failed mandatory criterion is not an accepted limitation.

## Completion review

1. Verify scaffold integrity and transition to `Verification / In progress`.
2. Identify change, branch, working-tree state, and bounded implementation commit range.
3. Run **Pass 1: spec conformance** against approved scope, non-goals, requirements, criteria, plan, and amendments.
4. Run **Pass 2: standards conformance** against project rules, Definition of Done, architecture, tests, failure handling, data, migration, recovery, compatibility, security, operations, and maintainability.
5. Record `Pass`, `Fail`, or `Partial` and exact evidence for every criterion and material standard finding.
6. Separate blockers, accepted limitations, follow-up recommendations, and unrelated observations.
7. Complete `review.md` with both pass verdicts and the proposed completion verdict.
8. Set `Verification / Awaiting approval` when closure authorization is still required.

Checked task boxes are not completion evidence.

## Recommendation reconciliation

For every source recommendation, verify links, determine `Full`, `Partial`, or `None` coverage, update item and index, and apply `RECOMMENDATION_LIFECYCLE.md`. Do not mark a recommendation `Completed` merely because one linked change completed.

## Project-memory synchronization

Update only factual documents made stale by delivery, using `PROJECT_STATE_REFRESH.md`. Create follow-up recommendations only for durable non-blocking work outside approved scope.

## Final closure

After authorization:

1. transition to `Closure / In progress`;
2. finalize tasks, progress, context, amendments, and review;
3. reconcile recommendations and affected project memory;
4. move `.planning/changes/active/<change-folder>/` to `.planning/changes/completed/<change-folder>/`;
5. reset the active pointer to `Discovery / Ready` with no active change;
6. do not automatically activate another change.

## Integrity checks

Before reporting closure, verify the completed folder exists exactly once, review records both pass verdicts and authorization, acceptance evidence and change records agree, recommendation records agree, `.planning/ACTIVE.md` no longer points to the change, project facts are current, Git status contains no unexpected artifacts, and closure edited no production code.

If any check fails, report closure as blocked.

## Output contract

Lead with the completion verdict and closure state. Then report only failed or material checks, records changed, final location, recommendation transitions, follow-ups, and next permitted action.
