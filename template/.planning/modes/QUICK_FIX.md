# Mode: Quick fix

## Purpose

Perform a tiny, explicit, low-risk correction without opening a full change folder.

## Qualification

Read `DRIFT_POLICY.md` and the effective configuration. Every quick-fix condition must pass. If any material uncertainty remains, route to Planning.

## Procedure

1. State briefly why the request qualifies, only when not obvious.
2. Inspect the narrow affected flow.
3. Make the smallest edit.
4. Run focused verification.
5. Add one compact row to `.planning/drift/QUICK_CHANGES.md`.
6. Check immediate and scheduled drift-sync triggers.
7. If the fix reveals a broader issue, create a recommendation instead of expanding the edit.

## Restrictions

- no public API, schema, migration, architecture, dependency, security, external-service, destructive-data, or acceptance-criteria changes;
- no repeated symptom fixes that conceal a systemic defect;
- no unrelated cleanup bundle;
- no unverified “obvious” edit when a focused test or inspection is available.

A capitalization correction usually qualifies. Changing how cluster labels are generated, stored, or consumed may not.
