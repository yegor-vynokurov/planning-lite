# Audit before implementation

Mode: Audit.

## Authorization boundary

Audit and repair planning artifacts only. Do not implement production code.

## Compare

- original user request and explicit approvals;
- all source recommendations and intended coverage;
- project rules, completion criteria, and Definition of Done;
- proposal, specification, requirements checklist, plan, tasks, context, and amendments;
- current code, tests, data contracts, configuration, and interfaces.

## Check for

- missing or vague requirements;
- recommendation intent lost during conversion;
- contradictions and hidden assumptions;
- scenario, boundary, invalid, empty, duplicate, partial, repeated, and interrupted states;
- retry, timeout, rollback, recovery, and resume behavior;
- compatibility, migration, data loss, security, privacy, licensing, and external side effects;
- performance and resource limits;
- acceptance criteria without verification tasks;
- tasks not justified by approved scope;
- out-of-plan quick changes affecting this work;
- over-engineering and speculative abstractions.

## Procedure

1. Record findings with severity in `requirements-checklist.md`.
2. Resolve planning-only gaps where the approved scope already determines the answer.
3. Draft amendments for material changes.
4. Block implementation when scope or acceptance approval is required.
5. Create recommendations for unrelated opportunities.
6. Update `context.md` and `.planning/ACTIVE.md`.

## Output

State resolved gaps, remaining blockers, amendments requiring approval, drift concerns, and whether implementation is ready for a direct user command.
