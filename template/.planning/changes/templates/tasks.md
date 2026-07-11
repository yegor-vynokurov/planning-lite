# CHG-NNNN: <change title> - Tasks

Status: `Not yet prepared`

Each task must have one verifiable result. Use exact paths where known. Order tasks by dependency.

## Investigation and baseline

- [ ] T001 Confirm current behavior and record a reproducible baseline. Verification: `<command or evidence>`

## Specification and tests

- [ ] T002 Add or update tests that express the approved behavior. Verification: `<test command>`

## Implementation

- [ ] T003 Implement `<specific bounded result>` in `<path>`. Verification: `<command>`

## Documentation and migration

- [ ] T004 Update affected documentation and migration notes. Verification: `<inspection or command>`

## Final verification

- [ ] T005 Run the complete relevant verification set and record results in `review.md`.
- [ ] T006 Compare implementation against every acceptance criterion and Definition of Done item.
- [ ] T007 Update project state, recommendation links, roadmap, completion evidence, and architecture docs where affected.

## Dependency notes

- `T003 depends on T001 and T002.`

## Parallel work

Mark genuinely independent tasks with `[P]`. Do not mark tasks parallel when they edit the same state or depend on unverified contracts.
