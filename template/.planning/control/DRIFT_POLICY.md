# Quick changes and plan-drift policy

The purpose is to avoid bureaucracy for tiny corrections without allowing a planned change to dissolve into invisible side work.

## A request qualifies as a quick fix only when all are true

- The user directly requests the edit.
- Expected size is within the configured file and changed-line limits.
- The change is easy to understand, verify, and reverse.
- It does not materially alter approved scope or acceptance criteria.
- It does not affect any prohibited impact listed in the effective configuration.
- It does not require unresolved product, architectural, migration, or data decisions.
- It does not conceal a repeated systemic defect.

Examples that usually qualify:

- change cluster labels from lowercase to uppercase;
- correct a typo or a narrow user-facing string;
- add one missing test assertion for already approved behavior;
- fix formatting or a local private naming inconsistency.

Examples that do not qualify:

- change public API behavior;
- modify persisted data format or schema;
- add a production dependency;
- change error-handling policy across a pipeline;
- alter architecture boundaries;
- expand acceptance criteria;
- fix a symptom that has already appeared repeatedly.

## Quick-fix procedure

1. Classify and state any non-obvious risk.
2. Make the smallest edit.
3. Run focused verification.
4. Add one row to `.planning/drift/QUICK_CHANGES.md`.
5. Update active change progress only when the quick fix affects that change.
6. Check sync triggers.

## Scheduled drift-sync triggers

Run prompt `11-drift-sync.md` when any configured threshold is reached:

- unsynced quick-fix count;
- elapsed days since the first unsynced fix;
- cumulative distinct files;
- cumulative changed lines.

The defaults are heuristics and may be adapted. Count alone is not the safety boundary.

## Immediate drift-sync triggers

Audit immediately, regardless of count, when:

- a quick edit conflicts with proposal, specification, plan, or an ADR;
- one component receives the same kind of quick correction repeatedly;
- tests reveal a broader regression;
- cumulative fixes imply a missing abstraction or policy;
- a proposed fix touches a prohibited impact;
- the active change can no longer be completed as approved;
- the agent believes continued execution would create future conflict or rework.

## Drift-review outcomes

A drift report must choose one or more:

- `Aligned`: quick fixes do not require plan changes.
- `Documentation sync`: update current state, architecture, or docs.
- `Plan amendment`: implementation details or sequencing changed without changing approved outcome.
- `Scope amendment`: proposal/specification/acceptance criteria must change; user approval required.
- `New recommendation`: useful follow-up, not current work.
- `New change`: a separate bounded unit should be proposed.
- `Critical mismatch`: pause affected execution until resolved.

## Plan amendments versus scope amendments

Plan amendment, normally no new product approval:

- file paths or implementation sequence changed;
- a library call differs but contracts remain the same;
- a test strategy is strengthened;
- an internal design is simplified without changing behavior or risk class.

Scope amendment, explicit user approval required:

- requirements or acceptance criteria change;
- users or interfaces affected change;
- compatibility, migration, data, security, or external side effects change;
- an explicit non-goal becomes in scope;
- project completion criteria are reinterpreted.

Record both kinds in the active change `amendments.md`.
