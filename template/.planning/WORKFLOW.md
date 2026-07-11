# Workflow and approval gates

## Stage 0: Bootstrap an existing project

Mode: Audit.
Prompt: `00-bootstrap-existing-project.md`.

Outputs:

- project charter and completion criteria;
- durable project rules;
- architecture and current-state summary;
- dated assessment;
- recommendations and index.

Gate: no production code and no executable change is implied.

## Stage 1: Dialogue and assessment

Modes: Dialogue / critic or Audit.

Use discussion to challenge goals and assumptions. Use assessment to record evidence. Recommendations may be created, but remain non-executable.

## Stage 2: Recommendation triage

Prompt: `03-capture-or-triage-recommendations.md`.

A recommendation can be accepted, deferred, rejected, related to other recommendations, or converted into one or more changes. Acceptance of direction is not implementation authorization.

## Stage 3: Create bounded change

Mode: Planning.
Prompt: `04-create-approved-change.md`.

One change may list several source recommendations. One recommendation may list several converted changes.

First freeze outcome, scope, non-goals, requirements, acceptance criteria, and user decisions. Plan and tasks may remain unprepared.

## Stage 4: Interactive planning

Mode: Planning.
Prompt: `05-plan-approved-change.md`.

Pass A: planning dialogue, unknowns, options, trade-offs, decisions.

Pass B: plan, tasks, traceability, context packet, and pre-implementation audit.

Gate: unresolved critical gaps block implementation.

## Stage 5: Execute

Mode: Execution.
Prompt: `07-implement-approved-change.md`.

Requires direct user implementation command. Work through verified tasks. Record amendments before continuing when reality differs.

## Side path: Quick fix

Mode: Quick fix.
Prompt: `10-quick-fix.md`.

Use only for explicit tiny low-risk requests. Log each edit. Run drift sync at configured thresholds or immediate triggers.

## Stage 6: Drift sync and amendments

Modes: Audit or Planning.

- `11-drift-sync.md` compares quick changes and code with approved work.
- `12-amend-active-change.md` records plan or scope amendments.

Scope amendments require user approval before affected execution continues.

## Stage 7: Review and close

Mode: Audit.
Prompt: `08-review-and-close-change.md`.

Compare implementation with every acceptance criterion and Definition of Done. Review recommendation coverage individually before changing recommendation statuses.

## Stage 8: Recovery and out-of-band work

- `09-refresh-project-state.md` reconciles legitimate out-of-band changes.
- `13-recover-from-wrong-mode.md` handles work begun without the right approval.

Do not rewrite history to make unapproved work look approved.

## Cross-stage control: Session checkpoint

Trigger: `Выполни чекпоинт`, the logical skill `planning-checkpoint`, or preparation for context compaction or a new session.

Stop production-code edits. Update tasks, progress, active context, and `ACTIVE.md`; collect a compact Git summary; report readiness. The operator executes client-interface commands through the active adapter.

## Cross-stage control: Git change review

Trigger: direct request, configured semantic or quantitative risk, drift or recovery, or closure of a non-trivial change.

Start with Git metadata and a bounded commit range. Inspect only selected high-risk patches unless broader closure evidence is required. Record a verdict and route corrections to the appropriate mode.
