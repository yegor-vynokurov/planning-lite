# CHG-NNNN: Requirements quality checklist

This checklist tests the written requirements, not the implementation.

## Completeness

- [ ] Are all intended users and workflows identified?
- [ ] Are success and failure paths specified?
- [ ] Are inputs, outputs, state changes, and side effects defined?
- [ ] Are migration, recovery, and repeated-execution requirements included when relevant?
- [ ] Are non-functional requirements included or explicitly marked not applicable?

## Clarity

- [ ] Are vague words such as fast, robust, easy, recent, correct, or complete quantified or contextualized?
- [ ] Can a new agent distinguish requirements from suggestions and assumptions?
- [ ] Are project terms used consistently with the glossary?

## Consistency

- [ ] Do requirements align with the project charter, rules, and completion criteria?
- [ ] Do acceptance criteria match the stated requirements?
- [ ] Do scope and non-goals avoid contradiction?

## Measurability

- [ ] Can every acceptance criterion be objectively verified?
- [ ] Is expected evidence named?
- [ ] Are thresholds and tolerances explicit where needed?

## Coverage

- [ ] Are boundary conditions and empty states covered?
- [ ] Are invalid, corrupted, partial, and duplicate inputs covered when relevant?
- [ ] Are interruption, retry, resume, timeout, and dependency failure behaviors covered when relevant?
- [ ] Are permissions, privacy, security, and licensing impacts covered when relevant?

## Dependencies and assumptions

- [ ] Are external dependencies and versions identified?
- [ ] Are assumptions clearly marked and validated or assigned for validation?
- [ ] Are user decisions separated from technical investigations?

## Plan and task traceability

Complete this after planning:

- [ ] Every requirement maps to plan sections and tasks.
- [ ] Every acceptance criterion maps to at least one verification task.
- [ ] Every implementation task is justified by approved scope.
- [ ] No critical unknown is hidden inside a task.

## Audit findings

| ID | Severity | Finding | Affected artifact | Resolution |
|---|---|---|---|---|
| Q-001 | `Critical / Major / Minor` | | | |
