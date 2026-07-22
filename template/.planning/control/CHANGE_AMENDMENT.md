# Change amendment

Use when an approved change must differ from its approved definition or plan.

Follow `CHANGE_LIFECYCLE.md`. Verify the scaffold and preserve populated records.

## Classification

### Implementation-detail amendment

The promised outcome, scope, non-goals, acceptance criteria, public contract, persisted data, migration, security, compatibility, architecture boundaries, and production dependencies remain unchanged.

The agent may record the amendment before continuing when it is necessary, low-risk, and consistent with the approved outcome. Update `amendments.md`, plan or tasks, `context.md`, and verification steps. Preserve the current lifecycle stage.

### Scope amendment

Any change to the protected elements above is a scope amendment. Stop affected execution, set lifecycle state to `Planning / Awaiting approval`, explain reason and impact, and request explicit user approval.

## Procedure

1. State the contradiction or new evidence.
2. Classify and justify the amendment.
3. Describe old and proposed approach, interfaces or seams affected, blast radius, risks, and verification changes.
4. Record the amendment in `amendments.md`.
5. Synchronize only affected proposal, specification, requirements, plan, tasks, context, recommendations, or decisions.
6. For a scope amendment, obtain approval, reapprove the plan, and rerun `CHANGE_READINESS.md` before resuming execution.

Do not use an amendment to conceal unrelated scope or retroactively legitimize unauthorized work.
