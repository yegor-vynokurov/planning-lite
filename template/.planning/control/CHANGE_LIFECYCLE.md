# Change lifecycle

This file is the authoritative state machine for active changes.

## Lifecycle stages

| Stage | Required durable result | Exit gate |
|---|---|---|
| `Discovery` | selected direction, recommendation, or wayfinding result | user selects a direction or requests a bounded change |
| `Definition` | complete scaffold; drafted proposal, specification, and requirements | proposal explicitly approved |
| `Planning` | approved `plan.md`, `tasks.md`, and resumable `context.md` | plan explicitly approved |
| `Readiness` | evidence-based `Ready` verdict | direct execution authorization |
| `Execution` | approved tasks implemented with progress evidence | approved tasks complete and checks run |
| `Verification` | spec-conformance and standards-conformance verdict | closure authorized or corrections routed |
| `Closure` | records reconciled, folder moved, active pointer reset | integrity checks pass |

After successful closure, the global pointer returns to `Discovery` with no active change.

## Stage status

Use exactly one:

- `Not started`;
- `In progress`;
- `Blocked`;
- `Awaiting approval`;
- `Ready`;
- `Complete`.

Stage is not task status. `tasks.md` remains authoritative for task progress.

## ACTIVE fields

The active pointer must contain:

- `Change`;
- `Change status`;
- `Lifecycle stage`;
- `Stage status`;
- `Current task`;
- `Last verified checkpoint`;
- `Next gate`;
- `Next permitted action`;
- `Implementation authorized`;
- `Active context packet`.

Do not copy plans or progress history into `.planning/ACTIVE.md`.

## Transition rules

- Enter `Definition` when a bounded change folder is initialized.
- Enter `Planning` only after proposal approval.
- Remain in `Planning / Awaiting approval` after drafting the plan until the user approves it.
- Enter `Readiness` only after plan approval.
- A `Ready` verdict sets `Readiness / Ready`; it does not enter Execution.
- Enter `Execution / In progress` only on direct implementation authorization.
- When approved tasks are complete, enter `Verification / Ready`.
- Completion review runs in `Verification`; final bookkeeping runs in `Closure`.
- A scope amendment returns the change to `Planning`, then requires renewed `Readiness`.
- A checkpoint preserves the current stage. It never advances or closes a change.

## Legacy normalization

An installed project may have an older `.planning/ACTIVE.md` without these fields.

Before the next planning, readiness, execution, verification, closure, or checkpoint operation:

1. infer the narrowest defensible stage from the active artifacts;
2. perform a targeted merge that adds missing lifecycle fields;
3. preserve all existing project-specific state;
4. never infer implementation or closure authorization.

Useful evidence:

- no active change: `Discovery / Ready`;
- draft proposal: `Definition / In progress` or `Awaiting approval`;
- approved proposal with unfinished plan: `Planning / In progress`;
- drafted unapproved plan: `Planning / Awaiting approval`;
- approved plan without readiness verdict: `Readiness / In progress`;
- readiness verdict `Ready`: `Readiness / Ready`;
- task status `In progress`: `Execution / In progress` only when execution authorization is recorded;
- all approved tasks complete: `Verification / Ready`.

If evidence conflicts, stop and report the inconsistency instead of guessing.

## Invariant check

Before every transition, verify that the required artifacts exist, their statuses agree, and the next gate is explicit. Record the transition in the active `context.md` and update `.planning/ACTIVE.md`.
