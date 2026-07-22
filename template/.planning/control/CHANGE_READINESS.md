# Change readiness audit

Use in Audit mode as an independent check before execution. Do not edit production code.

Follow `CHANGE_LIFECYCLE.md`. Verify the complete scaffold through `CHANGE_SCAFFOLD.md`; restore only missing initialized files and preserve populated records.

Require an approved proposal and approved plan.

## Pass 1: specification readiness

Verify:

- scope and non-goals are unambiguous;
- every requirement and acceptance criterion is traceable;
- task outcomes and verification can establish the promised behavior;
- facts are verified and remaining decisions are explicit.

## Pass 2: engineering readiness

Verify:

- tasks are dependency-ordered and blocking edges are explicit;
- architecture, seams, public contracts, data, migration, recovery, security, compatibility, dependencies, tests, documentation, blast radius, and rollback are addressed where applicable;
- no execution detail still requires an unapproved architecture decision.

Record evidence and one verdict in `readiness.md`:

- `Ready`;
- `Needs revision`;
- `Blocked`.

`Ready` sets lifecycle state to `Readiness / Ready` and permits the user to authorize execution. It does not itself authorize execution.

On `Needs revision`, return to `Planning / In progress`. On `Blocked`, keep the narrowest defensible stage and record the blocking decision and next permitted action.
