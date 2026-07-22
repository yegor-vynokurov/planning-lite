# State ownership

Each fact has one primary home.

| File | Authoritative responsibility |
|---|---|
| `.planning/ACTIVE.md` | active pointer, lifecycle stage, stage status, next gate, next permitted action, authorization, blocking decision, context path |
| active `plan.md` | approved implementation design and delivery strategy |
| active `tasks.md` | task outcomes, slice types, dependencies, verification, and task status |
| active `progress.md` | append-only implementation and verification evidence |
| active `context.md` | compact resumable handoff packet and latest stage transition |
| active `amendments.md` | approved or permitted deviations from definition or plan |
| active `readiness.md` | pre-implementation spec-readiness and engineering-readiness evidence and verdict |
| active `review.md` | spec-conformance, standards-conformance, completion evidence, closure authorization, recommendation outcomes, final location |
| recommendation item | authoritative recommendation content and lifecycle status |
| recommendation `INDEX.md` | discovery summary; must agree with items |
| decision record | durable decision and rationale |
| project glossary | canonical domain language, invariants, aliases, and anchors |
| project documents | current durable facts, not session history |
| skill usage CSV | optional best-effort frequency log; never authoritative project state |

## Duplication rules

- `ACTIVE.md` points to detail; it does not repeat plans or progress history.
- `context.md` summarizes only what is needed to resume; it does not copy full specifications.
- `progress.md` records evidence; it does not redefine tasks.
- Indexes are summaries, not independent status authorities.
- When duplicate state disagrees, repair it before closure or handoff.
