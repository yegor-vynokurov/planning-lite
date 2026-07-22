# Delivery slices discipline

Load when decomposing an approved change into implementation tasks.

## Leading terms

- **Tracer bullet**: the smallest end-to-end slice that proves a real path through the required layers and produces an observable result.
- **Expand-contract**: a staged migration that introduces the new path, moves callers or data, verifies compatibility, then removes the old path.
- **Blocking edge**: a dependency that must be resolved before another task can start.
- **Blast radius**: the affected code, data, contracts, tests, and operations.
- **Verification seam**: an observable boundary where the slice can be tested independently.

## Decomposition rules

Use tracer bullets by default for behavioral work. Each task should deliver a coherent outcome, cross the necessary layers, and have its own verification.

Use expand-contract for broad migrations, schema changes, compatibility transitions, or mechanical changes that cannot be safely delivered as one vertical slice.

Avoid horizontal layer tasks such as `create all models`, `add all repositories`, or `write tests later` unless the task is independently necessary and verifiable.

For every task record:

- outcome;
- slice type;
- blocking edge;
- verification seam and command;
- blast radius;
- rollback or recovery when material.

Keep a task small enough for one fresh context window unless a named blocking edge makes that impossible.

## Completion criterion

A task list is ready when each task has an observable outcome, dependency order is explicit, no verification is deferred to an unnamed final phase, and the sequence can stop safely after any completed slice.
