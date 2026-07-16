# Change planning

Use in Planning mode for an approved change. Do not edit production code.

## Minimum context

Read the active `context.md`, proposal, specification, requirements checklist, relevant project rules, repository map, and only the code or tests needed to resolve planning uncertainties.

## Procedure

1. Verify that the proposal is `Approved`.
2. Resolve material unknowns before converting them into tasks.
3. Fill `plan.md` with exact paths, symbols, contracts, state transitions, migrations, recovery, tests, documentation, and verification commands.
4. Prefer the smallest coherent design compatible with the existing architecture.
5. Fill `tasks.md` with dependency-ordered, atomic, verifiable tasks.
6. Map each requirement and acceptance criterion to plan sections and tasks.
7. Record durable architectural decisions separately when needed.
8. Update `context.md` and `.planning/ACTIVE.md` to stage `Readiness audit`.

Do not hide uncertainty, compatibility work, or recovery behavior inside generic implementation tasks.
