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
| recommendation item | authoritative recommendation content, lifecycle status, and accepted semantic-unit/reconciliation ledger when present |
| recommendation `INDEX.md` | discovery summary; must agree with items |
| decision record | durable decision and rationale |
| project glossary | canonical domain language, invariants, aliases, and anchors |
| `project/TARGET_STATE.md` | desired completed-state direction, claim provenance, non-goals, Target question ownership, acceptance evidence, and Target-state signals |
| `project/CAPABILITY_MODEL.md` | durable completed-state capabilities derived from the current Target; never current satisfaction status |
| `assessments/current/CURRENT_CAPABILITY_ASSESSMENT.md` | evidence snapshot of current capability Coverage and EvidenceConfidence against the accepted baseline; not a durable Target mutation |
| `project/GAP_MAP.md` | accepted causal missing conditions between demonstrated Current state and Target capabilities, with stable Gap identities and outcome-oriented closure conditions |
| `assessments/current/DIRECTION_HISTORY_RECONCILIATION.md` | snapshot reconciling recommendation semantic units and historical Roadmap lineage against the accepted Project Spine; not current Roadmap priority |
| `assessments/current/ROADMAP_SYNTHESIS.md` | evidence snapshot comparing coherent Roadmap outcome candidates, qualitative priority, alternatives, and proposed sequence; not canonical until explicit acceptance |
| `project/ROADMAP.md` | accepted current Roadmap outcome identities, sequence positions, Gap/capability lineage, exit conditions, exclusions, and accepted preferred direction; not Change authorization |
| project documents | current durable facts, not session history |
| skill usage CSV | optional best-effort frequency log; never authoritative project state |
| `project_policy` in effective configuration | topology/safety policy resolved from managed defaults plus project-owned `CONFIG.yml`; never lifecycle or history |

## Duplication rules

- `ACTIVE.md` points to detail; it does not repeat plans or progress history.
- `context.md` summarizes only what is needed to resume; it does not copy full specifications.
- `progress.md` records evidence; it does not redefine tasks.
- Indexes are summaries, not independent status authorities.
- When duplicate state disagrees, repair it before closure or handoff.
- The home registry stores locators only; it never becomes a second home for
  project documents, recommendations, Changes, or receipt history.
