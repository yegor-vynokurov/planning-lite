# Token-efficient Git change review

This workflow reviews either uncommitted work or a bounded commit range while avoiding an automatic repository-wide raw diff.

Use it when the user says any equivalent of:

- `Проведи Git review.`
- `Проведи дифф-ревью.`
- `Проверь текущий diff.`
- `Проверь изменения с последнего чекпоинта.`
- `Проверь change перед закрытием.`
- `$planning-git-review`

It may also be recommended by the checkpoint workflow when a configured trigger is reached.

## Purpose

Determine whether changes are:

- aligned with approved scope, plan, tasks, and acceptance criteria;
- technically coherent and adequately verified;
- free of accidental files or hidden scope expansion;
- ready for commit, checkpoint, closure, or further review.

This is an audit workflow. Do not edit production code while reviewing. Record findings and let the appropriate mode perform corrections.

## Review targets

Choose the narrowest target that answers the question:

1. **Working tree**: unstaged and untracked changes.
2. **Staged changes**: what is about to be committed.
3. **Single commit**: one atomic implementation step.
4. **Checkpoint range**: `<previous-checkpoint>..HEAD`.
5. **Change or PR range**: `<base>...HEAD` or the recorded change-start commit.

When work is committed regularly, prefer the checkpoint or task commit range instead of rereading the whole branch history.

## When review is required

A review is required or strongly recommended when any of these applies:

- the user explicitly requests it;
- a public API or external contract changed;
- a persisted schema, file format, migration, or recovery behavior changed;
- dependencies, lock files, build configuration, security, privacy, permissions, billing, or external services changed;
- architecture boundaries or cross-module responsibilities changed;
- acceptance criteria, compatibility promises, or approved scope may have changed;
- unexpected files, generated artifacts, or unrelated edits are present;
- drift, recovery, or failed tests indicate that implementation diverged from the plan;
- configured file, line, or commit thresholds are reached;
- a non-trivial change is being closed or prepared for PR review.

A deep review is normally unnecessary for a single verified quick fix when it is one atomic commit, the working tree is clean, no semantic trigger applies, and the quick-fix ledger is current.

## Progressive review ladder

Stop at the cheapest level that establishes sufficient confidence. Expand only for a named risk or finding.

### Level 1: metadata and scope map

Inspect summaries first:

```bash
git status --short --branch
git diff --stat
git diff --name-status
git diff --numstat
git diff --cached --stat
git diff --cached --name-status
```

For committed work:

```bash
git log --oneline <base>..HEAD
git diff --stat <base>..HEAD
git diff --name-status <base>..HEAD
git diff --numstat <base>..HEAD
```

Classify changed paths as:

- production code;
- tests;
- documentation;
- configuration and dependencies;
- migrations and persisted formats;
- generated, vendored, binary, cache, or output artifacts.

Do not paste all command output into planning documents. Record a compact inventory and the review range.

### Level 2: traceability and risk selection

Compare the inventory with:

- active `proposal.md`, `specification.md`, `plan.md`, `tasks.md`, and `amendments.md`;
- relevant project rules and Definition of Done;
- quick-fix or drift records where applicable.

Identify the exact files and hunks that need inspection. Prioritize:

- externally visible behavior;
- error, recovery, and repeated-execution paths;
- state transitions and persistence;
- interfaces between modules;
- security- or compatibility-sensitive code;
- tests that claim to verify acceptance criteria;
- surprising or unplanned files.

### Level 3: targeted patch inspection

Open only selected patches, for example:

```bash
git diff -- path/to/file.py
git diff --cached -- path/to/file.py
git show <commit> -- path/to/file.py
git diff <base>..HEAD -- path/to/file.py
```

For a large file, inspect named hunks or relevant functions rather than requesting the entire repository patch. Also inspect the current final implementation when correctness cannot be judged from the patch alone.

Generated, vendored, binary, dataset, cache, and output files should be summarized or excluded from raw patch reading unless their contract, source, or unexpected presence is itself under review.

### Level 4: verification evidence

Check whether:

- each reviewed behavior has a relevant test or inspection;
- tests actually ran and their result is recorded;
- documentation and migration notes match the implementation;
- failures, skipped tests, and residual risks are explicit;
- the range contains one coherent scope or clearly separated atomic commits.

Run only the narrow verification necessary for the review. A broader suite belongs to final change review when required by the plan or Definition of Done.

## Token controls

- Never begin with a full raw diff of the whole repository.
- Prefer `--stat`, `--name-status`, `--numstat`, and commit summaries first.
- Review a bounded commit range, not all history.
- Inspect only high-risk or surprising paths unless final closure requires broader coverage.
- Do not duplicate source code or patches in `context.md`, `progress.md`, or review reports.
- Store commit IDs, paths, findings, tests, and verdicts. Git remains the source for raw patches.
- If a formatter touched many files, separate semantic changes from formatting noise before detailed inspection.

## Output and recording

Record the review target and result in the active change `progress.md` or `review.md`. For out-of-plan or drift work, create a report under `.planning/drift/reviews/` when the finding is material.

Use one or more verdicts:

- `Aligned; deep patch review not required`
- `Aligned; ready for commit`
- `Aligned; ready for checkpoint`
- `Aligned; ready for change closure`
- `Documentation sync required`
- `Plan amendment required`
- `Scope approval required`
- `Unexpected or generated-noise cleanup required`
- `Tests or evidence incomplete`
- `Critical mismatch; execution must pause`

Report:

- target range or working-tree state;
- concise inventory;
- files and hunks actually inspected;
- findings ranked by severity;
- tests and evidence checked;
- required next action;
- whether execution, commit, checkpoint, or closure may proceed.
