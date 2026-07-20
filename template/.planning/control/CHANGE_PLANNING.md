# Change planning

Use in Planning mode for an approved change. Do not edit production code.

## Minimum context

Read `.planning/ACTIVE.md`, `CHANGE_SCAFFOLD.md`, the proposal, specification, requirements checklist, relevant project rules, repository map, and only the code or tests needed to resolve planning uncertainties.

Verify and, when safe, repair the complete scaffold before reading or updating `context.md`. Missing initialized files may be restored from canonical templates. Populated records must be preserved.

## Procedure

1. Verify that the proposal is `Approved`.
2. Verify scaffold integrity through `CHANGE_SCAFFOLD.md`.
3. Resolve material unknowns before converting them into tasks.
4. Fill `plan.md` with exact paths, symbols, contracts, state transitions, migrations, recovery, tests, documentation, and verification commands.
5. Prefer the smallest coherent design compatible with the existing architecture.
6. Fill `tasks.md` with dependency-ordered, atomic, verifiable tasks.
7. Map each requirement and acceptance criterion to plan sections and tasks.
8. Record durable architectural decisions separately when needed.
9. Initialize or update `context.md` and update `.planning/ACTIVE.md` to stage `Readiness audit`.

Do not hide uncertainty, compatibility work, or recovery behavior inside generic implementation tasks.
