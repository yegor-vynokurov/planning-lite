# Synchronize quick changes and audit plan drift

Mode: Audit.

## Trigger

Run when a scheduled threshold or immediate trigger in `DRIFT_POLICY.md` is reached, or when the user asks for a current alignment slice.

## Procedure

1. Read only unsynced rows in `QUICK_CHANGES.md` and their diffs or commits.
2. Calculate count, period, distinct files, approximate changed lines, and repeated patterns.
3. Compare changes with:
   - active proposal, specification, plan, tasks, amendments, and ADRs;
   - project rules, current state, architecture, and completion criteria where affected.
4. Create a dated report from `drift/reviews/TEMPLATE.md`.
5. Classify each mismatch and choose outcomes:
   - aligned;
   - documentation sync;
   - plan amendment;
   - scope amendment requiring approval;
   - new recommendation;
   - new change;
   - critical mismatch.
6. Update planning documents only when the evidence and existing approval already determine the correction.
7. Do not edit production code.
8. Mark reviewed quick-fix rows with the drift report ID.
9. Update `.planning/ACTIVE.md` and the ledger’s last-sync fields.

## Output

Lead with whether execution may continue. Then list drift, required amendments, recommendations, conflicts, and decisions needed.
