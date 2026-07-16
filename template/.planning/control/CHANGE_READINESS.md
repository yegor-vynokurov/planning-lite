# Change readiness audit

Use in Audit mode as an independent check before execution. Do not edit production code.

## Audit

Verify:

- approved scope and non-goals are unambiguous;
- every requirement and acceptance criterion is traceable;
- tasks are complete, ordered, and verifiable;
- architecture, public contracts, data, migration, recovery, security, compatibility, dependencies, tests, and documentation are addressed where applicable;
- unresolved decisions and assumptions are explicit;
- planned verification can establish the promised outcome.

Record evidence and one verdict in `readiness.md`:

- `Ready`;
- `Needs revision`;
- `Blocked`.

`Ready` permits the user to authorize execution; it does not itself authorize execution. On `Needs revision` or `Blocked`, update `.planning/ACTIVE.md` with the next permitted action and route corrections to Planning.
