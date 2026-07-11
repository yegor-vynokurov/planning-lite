# Perform a quick fix

Mode: Quick fix.

## Qualification

Check the effective configuration and `control/DRIFT_POLICY.md`. If any criterion fails or risk is unclear, stop and propose Planning mode instead.

## Procedure

1. Confirm the narrow requested outcome.
2. Inspect the smallest relevant flow.
3. Make the minimum edit.
4. Run focused verification.
5. Add the next `QF-NNNN` row to `.planning/drift/QUICK_CHANGES.md`.
6. Link the active change only when affected.
7. Check drift-sync thresholds and immediate triggers.
8. If a systemic issue appears, create a recommendation and do not expand the fix.

## Output

Report the edit, verification, ledger ID, and whether drift sync is now required.
