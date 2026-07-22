# Wayfinding

Use in Dialogue or Planning when an effort is too uncertain for a bounded specification.

## Trigger

Use wayfinding when at least one is true:

- several material unknowns depend on each other;
- the work is likely to exceed one fresh context window before it can be specified;
- repository facts, product decisions, and prototypes are mixed together;
- the next legal change cannot yet be stated with measurable acceptance criteria.

Do not use it for an ordinary feature that can already be defined.

## Frontier assessment

Create or update one assessment under `.planning/assessments/current/` with a frontier table:

| ID | Type | Question or outcome | Blocked by | State | Evidence or decision |
|---|---|---|---|---|---|

Allowed types: `Research`, `Decision`, `Prototype`, `Task`.

Allowed states: `Open`, `Blocked`, `Resolved`, `Deferred`.

Work only on open, unblocked frontier items. Repository-answerable questions are facts and should be investigated. Product, scope, and architecture choices are decisions and require the user.

A prototype that edits production code requires its own approval path; wayfinding itself is read-only.

## Exit

Exit when the remaining work can be expressed as either:

- a durable recommendation;
- a bounded change definition;
- an explicit decision to stop or defer.

Summarize resolved facts, user decisions, discarded alternatives, and remaining uncertainty. Do not keep a wayfinding assessment alive after it has served its purpose.
