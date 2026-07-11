# Assess current state and recommend next steps

Mode: Audit.

## Goal

Produce an evidence-based snapshot of the repository and a separate, non-executable recommendation set.

## Procedure

1. Define revision, scope, and confidence.
2. Read `REPOSITORY_MAP.md` first. Validate its relevant claims with targeted code, test, configuration, and documentation checks. Expand to broader discovery only when the audit scope or contradictory evidence requires it.
3. Distinguish observed fact, inference, unknown, risk, and recommendation.
4. Assess major flows and criteria as complete, partial, absent, failing, or not assessable.
5. Use a percentage only when denominator, weights, evidence, and confidence are explicit.
6. Create or update recommendation items for gaps and opportunities.
7. Relate recommendations when they overlap, conflict, depend on one another, or may be combined.
8. Propose sequencing, but do not create executable changes or code.
9. Refresh only affected rows in `REPOSITORY_MAP.md`, or record why a broader refresh was necessary.
10. Update `CURRENT_STATE.md` and `.planning/ACTIVE.md`.

## Output

Lead with the most important truth about current state, then evidence, limitations, recommendations, and user decisions required.
