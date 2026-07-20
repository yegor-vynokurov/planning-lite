# Change scaffold

Use this workflow whenever an active change folder is initialized, inspected for integrity, or repaired. It defines file existence only; it does not authorize completion of later-stage content or production-code edits.

## Canonical scaffold

Every active change folder must contain exactly one of each required file:

- `proposal.md`;
- `specification.md`;
- `requirements-checklist.md`;
- `plan.md`;
- `tasks.md`;
- `readiness.md`;
- `amendments.md`;
- `progress.md`;
- `context.md`;
- `review.md`.

Canonical sources live under:

```text
.planning/changes/templates/
```

A concrete change folder must not contain `.gitkeep`.

## Initialization

When creating `.planning/changes/active/CHG-NNNN-short-name/`:

1. create the folder;
2. copy every required canonical template into it, one file at a time;
3. do not copy `.gitkeep` or unrelated files;
4. verify that all required files exist exactly once;
5. leave later-stage files in their initialized template state until their workflow authorizes content changes.

Do not initialize a change with only the files needed for the current stage.

## Repair of an existing active change

Classify each required file as:

- `Missing`;
- `Initialized template`;
- `Populated change record`;
- `Ambiguous or conflicting`.

Apply these rules:

- `Missing`: copy the matching canonical template without changing existing records;
- `Initialized template`: preserve it;
- `Populated change record`: preserve it exactly unless the active workflow authorizes a targeted edit;
- `Ambiguous or conflicting`: stop and report the conflict.

Remove a nested `.gitkeep` from a concrete change folder after confirming that the folder contains real change records.

Do not replace populated records with canonical templates. Do not silently rename or delete unexpected files; report them for review.

## Integrity check

Before leaving scaffold initialization or repair, verify:

- all ten required files exist exactly once;
- filenames match the canonical names;
- no nested `.gitkeep` remains;
- existing populated records were preserved;
- no files outside the active change folder changed;
- the folder is ready for stage-specific content to mature progressively.
