# CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001 — Central Implementation Plan v1

- Plan ID: `CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001-CENTRAL-PLAN-001`
- Status: `APPROVED BY OWNER`
- Date: `2026-09-03`
- Definition: `APPROVED`
- Active Change: `CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001`
- Plan approval date: `2026-09-03`
- Implementation authorization: `NO`
- Target: Planning Lite central source at `D:\documents\planning-lite`
- Baseline branch: `reconcile/current-design-spine-2026-08-25`
- Baseline HEAD: `a40019209c133785a4babe06b5e96dfd4673c4f5`
- Approved Definition SHA256: `98769cceedd226fd602890daa308c9c47682089f89fd99ff2e6748c1a5932751`

## 1. Authority and planning rule

This Plan sequences the already bound architecture. It does not reopen or repeat
the full design held by:

- `01_PL_V39_05_C_AUTHORITY_BINDING_REPORT.md`;
- `02_PL_V39_05_C_IMPLEMENTATION_START_CONTRACT.md`;
- `PL_V39_05_C_INCOMING_ADJUDICATION.md`;
- the approved Change Definition;
- `PL-V39-05-C-DEFINITION-ACTIVATION-v1.md`.

If this Plan and a detailed architectural statement differ, the approved
Definition and Implementation Start Contract govern. A change to their scope or
invariants requires a Definition amendment, not an implementation convenience.

## 2. Lifecycle gates

```text
owner Plan approval
        ↓
read-only Formal Readiness
        ↓
Readiness PASS
        ↓
separate owner Execution authorization
        ↓
T-01 through T-06 central implementation
        ↓
separate commit authorization + committed central candidate
        ↓
T-07 and T-08 disposable consumer proofs
        ↓
T-09 completion review
        ↓
separate owner closure/release decisions
```

Plan approval is not implementation authorization. Readiness PASS is not
implementation authorization. No commit, live migration, or release is implicit
in any task.

## 3. Execution sequence and dependencies

The planned execution order is:

```text
T-01 → T-02 → T-03 → T-04 → T-06 → T-05
                                      ↓
                         CENTRAL CANDIDATE GATE
                                      ↓
                                T-07 → T-08
                                      ↓
                                     T-09
```

Rationale limited to sequencing:

- T-02 establishes the shared home/policy/registry primitives.
- T-03 adds the control-Git topology on those primitives.
- T-04 integrates the highest-risk update/Doctor/source-rebind seam after Git
  contexts are explicit.
- T-06 then adds its CLI surface serially, avoiding concurrent edits to
  `cli.py`.
- T-05 documents and publishes only the settled behavior, then regenerates
  integrity metadata once.
- T-07/T-08 require all central behavior plus an exact committed candidate;
  they are serial to keep consumer-precondition failures attributable.
- T-09 is evidence aggregation/review, not another feature task.

Logical dependencies remain those in the Implementation Start Contract even
where this Plan deliberately chooses a stricter serial order.

## 4. Global write boundary

Only the following product surfaces are eligible across T-02 through T-08:

### Python distribution

```text
src/planning_lite/cli.py                          MODIFY
src/planning_lite/local_update.py                 MODIFY
src/planning_lite/workspace.py                    ADD
src/planning_lite/telemetry.py                    ADD
```

### Template/control and integrity

```text
template/.planning/framework/defaults.yml         MODIFY
template/.planning/control/CONFIG_RESOLUTION.md   MODIFY
template/.planning/control/STATE_OWNERSHIP.md     MODIFY
template/.planning/control/GIT_CHANGE_REVIEW.md   MODIFY
template/.planning/project/PROJECT_INSTRUCTIONS.md MODIFY
template/.planning/templates/project/PROJECT_INSTRUCTIONS.md MODIFY IN LOCKSTEP
template/.planning/changes/templates/progress.md  MODIFY
template/.planning/changes/templates/review.md    MODIFY
template/.planning/docs/ARCHITECTURE.md           MODIFY
template/.planning/docs/MANIFEST_V4.md            MODIFY
template/.planning/framework/SHA256SUMS.txt       REGENERATE CANONICALLY
```

### Conditional surfaces

```text
template/.planning/control/PROJECT_BOOTSTRAP.md   only for policy-initialization guidance
template/.planning/framework/OWNERSHIP.yml        only if topology metadata classification requires it
copier.yml                                        only if a new project-owned topology path must be classified
tests/test_template_source.py                     only if source-rebind coverage requires it
tests/test_template.py                            only if template contract coverage requires it
tests/test_versioning.py                          only if a new version-source invariant is introduced
```

Every conditional write must be resolved in Formal Readiness or stopped for
adjudication before mutation. Copier tasks/migrations and `--trust` are outside
the approved boundary.

### Central docs and release notes

```text
docs/ARCHITECTURE.ru.md                            MODIFY
docs/UPDATABLE_INSTALLATION.ru.md                  MODIFY
docs/OPERATOR_WORKFLOW.ru.md                       MODIFY
CHANGELOG.md                                       MODIFY under ## Unreleased
```

### Tests

```text
tests/test_workspace_registry.py                   ADD
tests/test_split_control_history.py                ADD
tests/test_run_receipts.py                         ADD
tests/test_cli.py                                  MODIFY
tests/test_local_only_update.py                    MODIFY
```

Normal central lifecycle receipts under
`docs/design/project-spine/checkpoints/` and the top resume contract in
`CURRENT.md` are Planning state, not product implementation surface.

Any other product path is forbidden until a reviewed Plan/Definition amendment.

## 4.1 Task evidence model

T-01 through T-08 use one compact accumulating execution ledger on the existing
central checkpoint surface:

```text
docs/design/project-spine/checkpoints/PL-V39-05-C-EXECUTION-LEDGER-v1.md
```

The ledger is created on the first authorized execution entry and appended for
each subsequent T-01…T-08 task. It is not a new parallel lifecycle taxonomy.
Each task entry records only what continuation and adjudication need:

```text
task ID
execution baseline/revision, when material
actual changed paths
verification commands/evidence
PASS / FAIL / BLOCKED
material finding or stop-gate, when present
link to a standalone diagnostic/evidence artifact, only when one exists
```

No separate receipt/checkpoint file is created automatically for an individual
T-01…T-08 task. A standalone task artifact is permitted only when the task
produces a materially valuable diagnostic/evidence object or an existing
canonical architecture explicitly requires that document. A receipt alone is
not a reason to create another file.

T-09 retains its separate final surface:

```text
docs/design/project-spine/checkpoints/PL-V39-05-C-COMPLETION-REVIEW-v1.md
```

## 5. Task contracts

### T-01 — Contract lock and execution baseline

Dependencies: approved Plan, Formal Readiness PASS, separate Execution
authorization.

Writes:

```text
CURRENT.md                                                           lifecycle progress only
```

The T-01 result is the first entry in
`PL-V39-05-C-EXECUTION-LEDGER-v1.md`; no T-01 receipt file is created.

Outcome: bind the live execution baseline to the approved Definition and exact
policy/home/registry/Git/RunReceipt contracts without changing product files.

Verification seam: re-hash all authority inputs; record exact HEAD/status and
the approved/conditional/forbidden surfaces; confirm no unresolved Readiness
condition.

Stop gate: any material authority drift, overlapping unadjudicated dirt, or
schema ambiguity returns to owner adjudication before product writes.

### T-02 — Home, effective policy, registry, and inspection

Dependencies: T-01 PASS.

Writes:

```text
src/planning_lite/workspace.py           ADD
src/planning_lite/cli.py                 MODIFY
tests/test_workspace_registry.py         ADD
tests/test_cli.py                        MODIFY only for new command behavior
```

Record the T-02 result in the accumulating execution ledger.

Outcome: implement home resolution, defaults-plus-`CONFIG.yml` effective policy,
topology-only `projects.yml`, atomic/idempotent registration, bounded live
inspection, and fail-closed path/identity validation.

Verification seam: focused registry/schema/path tests; duplicate IDs/roots,
overlap, escape, legacy `{}` config, dry-run, idempotence, and live-authority
inspection cases.

Stop gate: a new policy file/database, semantic project-history copy, second
home product, secret field, or unbounded scanner requires amendment.

### T-03 — Explicit Git contexts and split-control topology

Dependencies: T-02 PASS.

Writes:

```text
src/planning_lite/workspace.py              MODIFY
src/planning_lite/cli.py                    MODIFY
tests/test_split_control_history.py          ADD
tests/test_workspace_registry.py            MODIFY if shared invariants require it
```

Record the T-03 result in the accumulating execution ledger.

Outcome: explicit product/control Git contexts and `control-init` dry-run/apply
using `.planning` as work tree, external `<home>/control/<project-id>.git`, and
`.planning/.git` as a gitfile.

Verification seam: real temporary dual-Git repository; externality and
non-overlap; independent HEAD/status/dirt; deterministic generated control
`.gitignore`; conflicting repeat rejection; identical repeat idempotence; product
HEAD/index/work-tree preservation.

Stop gate: automatic product `.gitignore` edit, automatic Git history operation,
unsafe external gitdir overlap, `.git` traversal, or inability to preserve
project-owned bytes.

### T-04 — Topology-aware update/Doctor and explicit source rebind

Dependencies: T-03 PASS.

Writes:

```text
src/planning_lite/cli.py                MODIFY
src/planning_lite/local_update.py       MODIFY
tests/test_cli.py                       MODIFY
tests/test_local_only_update.py         MODIFY
tests/test_split_control_history.py     MODIFY
tests/test_template_source.py           CONDITIONAL MODIFY
```

Record the T-04 result in the accumulating execution ledger.

Outcome: correct tracked/local-only/split selection, bounded governed-path scans,
topology-metadata preservation, and explicit `--template-source` rebind for
`check`/`update` with no silent fallback.

Verification seam: three-mode temporary fixtures; existing local-only regression;
source-precedence tests; stale/unavailable answer source; explicit successful
rebind metadata; second preview/apply idempotence; no nested `.git` scan.

Stop gate: Copier `--trust`, silent source substitution, whole-product recursive
scan, project-owned overwrite, or inability to distinguish product/control Git.

### T-06 — Raw RunReceipt v1

Dependencies: T-02 PASS and scheduled after T-04 to serialize `cli.py` writes.

Writes:

```text
src/planning_lite/telemetry.py           ADD
src/planning_lite/cli.py                 MODIFY
tests/test_run_receipts.py               ADD
tests/test_cli.py                        MODIFY
```

Record the T-06 result in the accumulating execution ledger.

Outcome: exact validation and append-only storage of externally supplied raw
RunReceipt v1 JSONL at the registered telemetry path.

Verification seam: exact required/nullable fields, explicit provenance,
all-null/unavailable receipt, disabled no-write behavior, append/idempotence
rules, corruption handling, concurrency boundary, and Campaign compatibility.

Stop gate: model/runtime invocation, inferred model/token/cost facts, metric
interpretation, lifecycle mutation, Campaign coupling, daemon/service/database,
or secret storage.

### T-05 — Template policy, linkage, documentation, and integrity

Dependencies: T-02 through T-04 and T-06 semantically stable.

Writes: only the template/control, central-doc, release-note, test, and
conditional surfaces in Section 4.

Record the T-05 result in the accumulating execution ledger.

Outcome: expose settled project policy and explicit Git/history/receipt semantics
through existing authorities; extend progress/review linkage fields; document
operator and update behavior; update `CHANGELOG.md`; regenerate manifest/SHA
metadata once.

Verification seam: focused semantic owner tests, template rendering, ownership
classification, manifest count, canonical-LF SHA verification, and exact
lockstep equality of the two `PROJECT_INSTRUCTIONS.md` sources.

Stop gate: new policy authority, router/memory/checklist semantics, ownership
ambiguity, unexplained `copier.yml` change, or integrity generation that cannot
be reproduced from current repository mechanisms.

### Central candidate gate

Dependencies: T-01 through T-06 PASS and focused integration evidence PASS.

Required before T-07/T-08:

```text
exact central changed-path audit
focused owner tests PASS
project-owned preservation evidence PASS
separate explicit owner authorization for a central checkpoint commit
clean committed candidate identity
```

The current approval does not authorize this commit. Without a committed
candidate, stop; do not imitate release-like consumer updates from a dirty source.

### T-07 — Disposable Poker brownfield proof

Dependencies: T-03 through T-06 PASS and central candidate gate PASS.

Writes:

```text
temporary disposable Poker byte snapshot only
tests/test_split_control_history.py      MODIFY if the durable scenario belongs there
tests/test_local_only_update.py          MODIFY if the durable update scenario belongs there
```

Record the T-07 result in the accumulating execution ledger. A separate Poker
artifact is allowed only if the disposable proof itself produces an independently
valuable diagnostic/evidence object.

Verification seam: exact pre/post project-owned hashes; preserved ACTIVE/CHG-0009
lifecycle; external gitdir/gitfile; independent Git state; paused registry entry;
exact-source update; Doctor; idempotence; all-null receipt; no lifecycle change.

Stop gate: live Poker access requiring mutation, unadjudicated handoff bypass,
consumer Change transition, or any product/control commit outside the disposable
fixture.

### T-08 — Disposable mood unborn/adoption proof

Dependencies: T-03 through T-06 PASS, central candidate gate PASS, and T-07
evidence adjudicated.

Writes:

```text
temporary disposable mood byte snapshot only
tests/test_split_control_history.py      MODIFY if shared durable scenario belongs there
tests/test_template_source.py            CONDITIONAL MODIFY for rebind regression
```

Record the T-08 result in the accumulating execution ledger. A separate mood
artifact is allowed only under the same standalone-evidence exception.

Verification seam: unborn product repository; exact selective-ignore baseline;
required refusal before full `.planning` ignore; fixture-only ignore adjustment;
separate control history; explicit source rebind; project-owned hashes; Doctor;
repeat idempotence; no implicit product HEAD assumption.

Stop gate: live mood mutation, automatic ignore edit, unrecoverable unborn state,
silent source rebind, initial commit outside the fixture, or lifecycle transition.

### T-09 — Central completion verification and review

Dependencies: T-01 through T-08 PASS with no unresolved material product defect.

Writes:

```text
docs/design/project-spine/checkpoints/PL-V39-05-C-COMPLETION-REVIEW-v1.md ADD
CURRENT.md                                                              lifecycle progress only
```

No new product feature write is permitted in T-09.

Verification seam: Section 6 completion stack, exact changed-path/ownership/scope
audit, consumer-proof evidence, and explicit classification of every failure as
product defect, verifier defect, consumer precondition failure, or unavailable
external runtime capability.

Stop gate: completion cannot be declared with a material defect, failed required
proof, out-of-scope write, guessed runtime fact, or unreviewed conditional surface.
T-09 review does not itself authorize Change closure, release, tag, push, merge,
or live migration.

## 6. Verification plan

Use the smallest task-local evidence first:

```text
T-02: uv run --frozen pytest -q tests/test_workspace_registry.py
T-03: uv run --frozen pytest -q tests/test_split_control_history.py
T-04: uv run --frozen pytest -q tests/test_local_only_update.py tests/test_template_source.py tests/test_cli.py
T-06: uv run --frozen pytest -q tests/test_run_receipts.py tests/test_cli.py
T-05: directly affected template/ownership/integrity owner tests
T-07/T-08: bounded disposable fixture probes plus their owning regressions
```

Do not duplicate invariants with prose-literal tests and do not parse
human-oriented CLI failure rendering as machine state.

At the T-09 completion gate:

```text
uv sync
uv run pytest
uv run python scripts/test_template_update.py
uv run python scripts/test_local_only_update.py
```

Additionally:

1. adopt into a temporary clean Git repository and run consumer Doctor there;
2. test update from the last applicable release tag to the exact committed
   candidate;
3. verify project-owned bytes and topology metadata directly;
4. run a real temporary external-gitdir/gitfile split-control proof;
5. prove independent product/control dirt and HEAD reporting;
6. verify manifest, ownership, canonical-LF SHA, and exact changed paths;
7. confirm the live Poker and mood trees were not mutated.

Do not run `planning-lite doctor .` at the central repository root.

## 7. Formal Readiness after Plan approval

Formal Readiness is a separate read-only pass. It must resolve:

- exact live HEAD/status and approved authority hashes;
- every ADD/MODIFY/CONDITIONAL path against current ownership and source;
- whether `OWNERSHIP.yml`, `copier.yml`, `PROJECT_BOOTSTRAP.md`,
  `test_template_source.py`, `test_template.py`, or `test_versioning.py` is
  actually required;
- the existing atomic-write, path-normalization, Git-command, Doctor, update,
  manifest, and SHA owner seams;
- exact focused test commands and temporary-fixture strategy;
- protected-path baseline hashes;
- the committed-candidate prerequisite for T-07/T-08;
- that two reasonable implementers cannot materially diverge on the approved
  schemas and stop conditions.

Readiness must end with one of:

```text
READY / implementation_authorized = NO
NEEDS_REVISION / implementation_authorized = NO
BLOCKED / implementation_authorized = NO
```

Only a later explicit owner decision may authorize Execution.

## 8. Global stop conditions

Stop and request owner adjudication or amendment if:

1. any required write leaves the Section 4 surface;
2. a new Roadmap phase or changed `06/07/08` ownership is required;
3. a second policy, memory, routing, checklist, analytics, service, database,
   backup/sync, or secret-management authority appears necessary;
4. topology safety requires automatic product ignore edits, automatic commits,
   Copier tasks/migrations, or `--trust`;
5. product/control roots cannot remain explicit, non-overlapping, and safe from
   `.git` or link/reparse-point traversal;
6. project-owned bytes cannot be preserved;
7. unavailable runtime values would need inference;
8. source rebind cannot remain explicit and fail-closed;
9. live Poker or mood mutation appears necessary;
10. a required product/control behavior lacks a focused temporary-repository
    acceptance proof;
11. clean committed-source identity is unavailable for T-07/T-08;
12. source-version metadata remains inconsistent after the completion sync and
    committed-candidate verification.

## 9. Current verdict and next gate

```text
Definition approved: YES
Central Change active: YES
Plan prepared: YES
Plan approved: YES / OWNER
Formal Readiness: NEXT PERMITTED ACTION
Implementation authorized: NO
T-01 started: NO
Commit authorized: NO
Live Poker/mood migration authorized: NO
Release/tag/push/merge authorized: NO

next gate: run read-only Formal Readiness
```

Do not begin Formal Readiness in this turn and do not begin implementation
automatically.
