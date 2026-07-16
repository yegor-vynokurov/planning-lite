# Quick fix and drift policy

## Quick-fix eligibility

A quick fix requires an explicit user request and must be tiny, low-risk, locally understandable, easily reversible, and verifiable. Apply effective configured size thresholds.

It must not change public APIs, persisted schemas or formats, migrations, security or privacy, architecture boundaries, production dependencies, acceptance criteria, destructive data behavior, or external billing.

## Quick-fix procedure

1. Confirm eligibility before editing.
2. Change the minimum files.
3. Run a narrow check.
4. Append one row to `.planning/drift/QUICK_CHANGES.md` with scope, evidence, and sync status.
5. Stop and route to Planning when any criterion fails.

## Drift sync triggers

Run a sync when configured count, age, cumulative size, repeated-pattern, semantic-risk, recovery, or user-requested triggers fire. Semantic risk overrides numeric thresholds.

## Drift sync procedure

1. Review unsynchronized ledger rows and related Git summaries.
2. Classify each as harmless local correction, project-state update, plan amendment, scope amendment, new recommendation, or unauthorized work requiring recovery.
3. Update affected durable state and mark reviewed rows.
4. Record a drift review under `.planning/drift/reviews/`.
5. State whether current execution may continue.

Do not use the ledger as a shadow backlog or as permission to accumulate architecture work outside changes.
