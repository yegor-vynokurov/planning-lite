# PL-V38-PREP-01 — Local-only consumer update safety

**Status:** IMPLEMENTED CANDIDATE  
**Parent:** `e51320bf4ebb9fc3eecd88d1eb8e52a12a803b3e`  
**Trigger:** `PILOT-PL-DIRECTION-002` non-scored preparation finding

## Problem

Poker intentionally keeps `.planning/` and `.agents/` local and Git-ignored so Planning Lite control state does not pollute the public product repository.

A disposable pre-pilot update from the Poker v4.2.0 consumer to Planning Lite `e51320b` exposed an unsafe boundary in ordinary Copier update semantics:

```text
BEFORE managed/local snapshot: 254 files
AFTER ordinary Copier update:    174 files

observed delta:
REMOVED   96
CHANGED   26
ADDED     16
UNCHANGED 132
```

The removals included unchanged centrally managed files such as `CHANGE_PLANNING.md`, `framework/defaults.yml`, modes, skills, adapters, and templates. The central template itself had not intentionally deleted those files. Therefore this was an update-mode compatibility defect, not a legitimate framework migration.

The scored Poker attempt did **not** start. Canonical Poker remained frozen.

## Decision

Planning Lite now distinguishes ordinary tracked consumers from consumers whose managed roots are local-only / Git-ignored.

### Ordinary consumer

```text
tracked managed tree
→ existing Copier update path
```

### Local-only consumer

```text
.planning and/or .agents ignored
→ ordinary write update FAILS CLOSED
→ check renders a pristine candidate and emits an ownership-aware mutation plan
→ explicit `update --local-only` applies the same plan atomically
```

## Local-only invariants

1. Existing project-owned files are preserved byte-for-byte.
2. New project-owned first-class files are created only when missing.
3. Managed files are added/updated from the pristine candidate.
4. A managed file is removed only when the previous ownership manifest classified it as managed and the new candidate intentionally omits it.
5. Unknown candidate ownership stops the update.
6. `project_owned -> managed` ownership transitions stop the update until explicitly reconciled.
7. Previously unclassified files may become managed only when their existing bytes already equal the candidate bytes.
8. All planned writes are post-verified.
9. Failure during apply rolls back all touched paths.
10. Installer metadata is updated from the rendered candidate only after the same plan is accepted/applied.

## Operator contract

Preview:

```powershell
planning-lite check . --vcs-ref <exact-ref>
```

For a detected local-only consumer this prints file-level actions such as:

```text
ADD_MANAGED
UPDATE_MANAGED
REMOVE_MANAGED
ADD_PROJECT
KEEP_PROJECT
UPDATE_METADATA
UNCHANGED_MANAGED
```

Ordinary write is blocked:

```powershell
planning-lite update . --vcs-ref <exact-ref>
```

Safe explicit apply:

```powershell
planning-lite update . --vcs-ref <exact-ref> --local-only
```

Then run Doctor in the consumer project.

## Regression fixture

The test suite includes a v4.2.0 local-only consumer fixture upgraded to the current candidate. It verifies:

- no destructive managed removals when the central template did not delete managed files;
- representative v4.2 managed workflows survive;
- new Direction workflows appear;
- `ACTIVE`, `CURRENT_STATE`, `ROADMAP`, and Recommendation index remain byte-identical;
- metadata advances;
- a second local-only plan is idempotent.

## Pilot consequence

After this change passes local validation, repeat only the **non-scored migration preview** for `PILOT-PL-DIRECTION-002`.

Do not start scored Attempt 001 until:

```text
safe local-only check
→ expected mutation plan
→ safe local-only update on disposable preview
→ Doctor OK
→ project-owned hash preservation confirmed
→ PILOT_READY receipt
```

PL-V38-05 remains stopped.
