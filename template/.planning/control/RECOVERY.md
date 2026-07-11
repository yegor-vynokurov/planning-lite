# Recovery from the wrong mode or missing approval

Use this when an agent generated a plan, changed planning state, or edited code beyond the current authorization.

## Immediate actions

1. Stop the affected work.
2. Do not silently continue merely to “finish cleanly”.
3. Do not automatically delete, reset, or revert user-visible work.
4. Identify exactly what was created or changed.
5. Mark unauthorized planning artifacts `Draft - not approved`.
6. Keep proposal status unchanged unless approval was explicit.
7. Create a drift review when code or durable project state changed.

## Report to the user

Provide:

- intended mode and actual mode;
- files changed;
- commands and side effects already executed;
- whether data, dependencies, APIs, or external systems were affected;
- tests or checks run;
- safest options.

## User options

Offer concrete paths without choosing on the user’s behalf:

- `Adopt`: convert the work into an approved change and review it.
- `Keep as draft`: preserve planning artifacts but authorize nothing.
- `Revise`: negotiate scope or plan before further work.
- `Revert`: revert selected edits after explicit approval.
- `Split`: keep a safe subset and move the rest to recommendations or another change.

## If only a plan was generated too early

- retain it as a draft unless the user asks to discard it;
- do not create executable authorization from the draft;
- return to Dialogue / critic or Planning dialogue;
- revise after decisions are made.

## If code was written too early

- preserve the diff for review;
- stop further edits;
- run only non-destructive checks needed to understand its state;
- log it in `QUICK_CHANGES.md` or a drift report as out-of-band work;
- do not mark planned tasks complete until the user adopts the work and it passes the proper review.
