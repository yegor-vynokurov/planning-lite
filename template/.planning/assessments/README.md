# Current-state assessments

Assessments are dated, evidence-based snapshots. They are not plans and do not authorize implementation.

## File lifecycle

- Create new assessments in `current/` using `TEMPLATE.md`.
- Keep the latest authoritative assessment linked from `.planning/project/CURRENT_STATE.md` and `.planning/ACTIVE.md`.
- Move superseded assessments to `archive/` without rewriting their historical conclusions.

## Evidence rule

Every important conclusion should point to repository evidence, such as:

- file and directory paths;
- functions, classes, schemas, and commands;
- tests and their outcomes;
- configuration and dependency files;
- generated artifacts;
- Git history when available;
- user-provided intent.

## Scoring rule

Use dimension scores only when helpful. Never hide uncertainty behind a polished number. If the target is unclear, say `Not currently scorable` and recommend clarifying the target.
