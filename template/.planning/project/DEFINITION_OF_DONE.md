# Definition of Done for a change

Status: `Template - adapt to repository`
Last reviewed: `YYYY-MM-DD`

A change is complete only when all applicable criteria below are satisfied or an explicit exception is recorded in its review.

## Scope and behavior

- [ ] The implementation matches the approved specification.
- [ ] Every acceptance criterion has evidence.
- [ ] No unapproved material scope expansion is hidden in the change.
- [ ] Known limitations and non-goals are documented.

## Code and architecture

- [ ] The implementation follows project rules and established architecture.
- [ ] Significant decisions are recorded in an ADR or the change plan.
- [ ] Dead code, debug artifacts, and accidental generated files are removed.
- [ ] Public interfaces and compatibility implications are documented.

## Verification

- [ ] Relevant automated tests pass.
- [ ] Regression tests exist for fixed defects where practical.
- [ ] Lint, formatting, type checks, and builds pass when applicable.
- [ ] Important runtime or end-to-end behavior was exercised.
- [ ] Commands run and outcomes are recorded in `review.md`.

## Data, migration, and recovery

- [ ] Data-format or schema changes have migration and rollback/recovery handling.
- [ ] Repeated execution, partial failure, and resumption behavior are verified when relevant.
- [ ] Existing valid data or artifacts are preserved.

## Documentation and operations

- [ ] README, architecture, configuration, examples, and docstrings are updated where affected.
- [ ] Setup and run instructions are sufficient for the intended user.
- [ ] Logging, diagnostics, and error messages are adequate.
- [ ] Deployment or release notes are updated when applicable.

## Project bookkeeping

- [ ] `tasks.md` and `progress.md` reflect reality.
- [ ] Residual gaps became recommendations or accepted risks.
- [ ] `CURRENT_STATE.md`, roadmap, completion criteria, and recommendation index are updated when affected.
- [ ] The final review records `Completed`, `Completed with accepted limitations`, or `Not complete`.
