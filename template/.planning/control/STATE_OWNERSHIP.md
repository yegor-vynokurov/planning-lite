# State ownership

Each fact has one primary home.

| File | Authoritative responsibility |
|---|---|
| `.planning/ACTIVE.md` | active pointer, stage, next permitted action, authorization, blocking decision, context path |
| active `tasks.md` | task definitions, dependencies, and current task status |
| active `progress.md` | append-only implementation and verification evidence |
| active `context.md` | compact resumable handoff packet |
| active `amendments.md` | approved or permitted deviations from the original plan |
| active `readiness.md` | pre-implementation audit evidence and verdict |
| active `review.md` | completion evidence, closure authorization, recommendation outcomes, final location |
| recommendation item | authoritative recommendation content and lifecycle status |
| recommendation `INDEX.md` | discovery summary; must agree with items |
| decision record | durable decision and rationale |
| project documents | current durable facts, not session history |

## Duplication rules

- `ACTIVE.md` points to detail; it does not repeat plans or progress history.
- `context.md` summarizes only what is needed to resume; it does not copy full specifications.
- `progress.md` records evidence; it does not redefine tasks.
- Indexes are summaries, not independent status authorities.
- When duplicate state disagrees, repair it before closure or handoff.
