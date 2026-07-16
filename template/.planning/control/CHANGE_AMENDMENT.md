# Change amendment

Use when an approved change must differ from its approved definition or plan.

## Classification

### Implementation-detail amendment

The promised outcome, scope, non-goals, acceptance criteria, public contract, persisted data, migration, security, compatibility, architecture boundaries, and production dependencies remain unchanged.

The agent may record the amendment before continuing when it is necessary, low-risk, and consistent with the approved outcome. Update `amendments.md`, plan or tasks, `context.md`, and verification steps.

### Scope amendment

Any change to the protected elements above is a scope amendment. Stop the affected execution, explain the reason and impact, and request explicit user approval.

## Procedure

1. State the observed contradiction or new evidence.
2. Classify the amendment and justify the classification.
3. Describe the old and proposed approach, affected artifacts, risks, and verification changes.
4. Record the amendment in `amendments.md`.
5. Synchronize proposal, specification, requirements, plan, tasks, context, recommendations, or decisions only where affected.
6. For a scope amendment, obtain approval and rerun `CHANGE_READINESS.md` before resuming execution.

Do not use an amendment to conceal unrelated scope or retroactively legitimize unauthorized work.
