# Changes

An approved change is the only normal container for non-trivial implementation.

Every concrete active change receives the complete scaffold at creation time. Follow `.planning/control/CHANGE_SCAFFOLD.md`.

Required files:

- `proposal.md`: authority, scope, non-goals, source recommendations;
- `specification.md`: requirements and acceptance criteria;
- `requirements-checklist.md`: traceability;
- `plan.md`: executable design;
- `tasks.md`: authoritative task status;
- `readiness.md`: pre-implementation audit;
- `amendments.md`: controlled deviations;
- `progress.md`: append-only evidence;
- `context.md`: compact handoff packet;
- `review.md`: completion and closure record.

Content matures progressively:

- Definition: `proposal.md`, `specification.md`, `requirements-checklist.md`;
- Planning: `plan.md`, `tasks.md`, `context.md`;
- Readiness: `readiness.md`;
- Execution: `tasks.md`, `progress.md`, `context.md`, and `amendments.md` when needed;
- Closure: `review.md` and final synchronization of all records.

A concrete change folder must not contain `.gitkeep`.

A checked task list does not close a change. Follow `.planning/control/CHANGE_CLOSURE.md`.
