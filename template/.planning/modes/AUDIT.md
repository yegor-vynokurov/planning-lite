# Mode: Audit and alignment review

## Purpose

Inspect evidence, completeness, correctness, or plan drift without implementing fixes.

## Allowed writes

- assessments;
- requirements checklists;
- final reviews;
- drift reports;
- recommendations;
- current-state and planning-document corrections that reflect evidence.

Do not edit production code in this mode.

## Audit styles

### Current-state audit

Compare stated project goal, completion criteria, README, architecture, entry points, tests, outputs, and actual repository evidence.

### Pre-implementation audit

Compare user request, linked recommendations, proposal, specification, plan, tasks, project rules, and relevant code. Find omissions before implementation.

### Drift audit

Compare quick changes and actual code with the approved active change and project documentation. Classify the result using `DRIFT_POLICY.md`.

### Completion review

Compare delivered behavior and verification evidence against every acceptance criterion and the Definition of Done.

### Git change review

Follow `.planning/control/GIT_CHANGE_REVIEW.md`. Start with status, stats, changed paths, and the narrowest relevant commit range. Open only targeted patches needed to resolve a named risk. Do not edit production code while reviewing.

## Critical-critic rules

- Report contradictions plainly.
- Distinguish missing evidence from failed behavior.
- Do not invent a success percentage when the denominator is undefined.
- Pair findings with a concrete next action where possible.
- A critical finding blocks affected execution; a minor finding does not masquerade as critical.
