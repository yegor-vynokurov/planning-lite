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

For dependency-aware Changes, use stable unique amendment IDs in governance
order and record each exact changed projection field with complete canonical
before/after JSON values. Keep implementation-detail versus Scope approval
requirements above; dependency materiality is derived separately for the
dependent edge and each independent task, not selected in a row by a caller.
Reconcile authorized changes into the current Plan/task semantics at the
existing Plan approval or authorized amendment/reconciliation transition,
recompute the existing Plan and fixed-edge
digests, and regenerate the final seven-field receipt. A material edit and a
material reversion both remain in the affected projection's ordered effect
history. A fully evidenced unrelated effect may be outside another task's
projection while changing general Plan provenance. Missing IDs, legacy prose
effects, incomplete before/after chains, unresolved values, or a stale receipt
block resolution until governed bring-forward is complete. Refreshing a digest
or receipt never retroactively approves an amendment or authorizes execution.

Do not use an amendment to conceal unrelated scope or retroactively legitimize unauthorized work.
