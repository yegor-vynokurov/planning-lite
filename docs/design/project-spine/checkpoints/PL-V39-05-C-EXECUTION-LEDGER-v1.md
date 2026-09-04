# PL-V39-05-C — Execution Ledger v1

- Change: `CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001`
- Execution authorization: `USER / EXPLICIT — 2026-09-03`
- Evidence model: one accumulating ledger for T-01…T-08; no automatic task receipts
- T-09: separate `PL-V39-05-C-COMPLETION-REVIEW-v1.md` (not created in this run)

## T-01 — Contract lock and execution baseline

```text
status: PASS
execution baseline:
  repository: D:\documents\planning-lite
  branch: reconcile/current-design-spine-2026-08-25
  HEAD: a40019209c133785a4babe06b5e96dfd4673c4f5
  index: clean
  working tree before ledger creation: DIRTY(14)
  dirty paths: known Planning/incoming artifacts only; no product/runtime/template/test path
changed paths:
  docs/design/project-spine/CURRENT.md (lifecycle pointer only)
  docs/design/project-spine/checkpoints/PL-V39-05-C-EXECUTION-LEDGER-v1.md
verification:
  uv run --frozen python scripts/maintainer_resume.py: PASS
  frozen authority SHA-256 recheck (Definition, Activation, Contract, Plan, Readiness,
  Binding Report, Incoming Adjudication): PASS / unchanged
  git status --short and HEAD/branch baseline: PASS
material finding / stop-gate: none
```

T-01 binds execution to the approved Definition, Contract, Plan, corrected
Formal Readiness, Activation, and Incoming Adjudication. The dirty baseline is
known and adjudicated; it is not converted into a pre-execution clean-commit
requirement. T-01 does not authorize a commit or any consumer operation.

## T-02 — Home, effective policy, registry, and inspection

```text
status: PASS
execution baseline: HEAD a40019209c133785a4babe06b5e96dfd4673c4f5; T-01 PASS
changed paths:
  src/planning_lite/workspace.py
  src/planning_lite/cli.py
  tests/test_workspace_registry.py
  tests/test_cli.py (no change required)
verification:
  uv run --frozen pytest -q tests/test_workspace_registry.py tests/test_cli.py: PASS (10 passed)
  home precedence explicit → PLANNING_LITE_HOME → default: PASS
  policy merge/legacy-null/path containment/overlap validation: PASS
  registry schema, duplicate/overlap rejection, atomic write and identical repeat: PASS
  read-only projects/inspect parser surfaces: PASS
material finding / stop-gate: none
```

T-02 adds no second policy authority: effective policy remains defaults plus
project-owned `CONFIG.yml`, and the registry stores topology/locators only.

## T-03 — Explicit Git contexts and split-control topology

```text
status: PASS
execution baseline: HEAD a40019209c133785a4babe06b5e96dfd4673c4f5; T-02 PASS
changed paths:
  src/planning_lite/workspace.py
  src/planning_lite/cli.py
  tests/test_split_control_history.py
verification:
  uv run --frozen pytest -q tests/test_split_control_history.py tests/test_workspace_registry.py tests/test_cli.py: PASS (13 passed)
  product_git(-C) and explicit control_git(--git-dir/--work-tree): PASS
  external gitfile topology and product HEAD/index preservation: PASS
  outer .planning ignore requirement and external-root containment: PASS
  deterministic managed-path control .gitignore and repeat idempotence: PASS
  no staging or commit: PASS
material finding / stop-gate: none
```

`control-init` leaves the initial control commit to the operator and does not
touch live consumer trees.

## T-04 — Topology-aware update/Doctor and explicit source rebind

```text
status: PASS
execution baseline: HEAD a40019209c133785a4babe06b5e96dfd4673c4f5; T-03 PASS
changed paths:
  src/planning_lite/cli.py
  src/planning_lite/local_update.py
  tests/test_local_only_update.py
  tests/test_template_source.py (no change required)
  tests/test_cli.py (no change required)
verification:
  focused local-only/source/CLI/split/registry suite: PASS (29 passed)
  post-execution source-path/control-topology recheck: PASS (32 passed)
  bounded scan excludes .git and preserves .planning/.git + .gitignore: PASS
  explicit source rebind and unavailable local source fail-closed: PASS
  local-only tracked/project-owned preservation and idempotence: PASS
  Doctor labels product/control Git independently: implemented seam; no broad consumer run
material finding / stop-gate: none
```

The ordinary Copier update path keeps its existing ownership behavior; explicit
source rebinding is temporary on dry-run/failure and retained only after a
successful update.

## T-06 — Raw RunReceipt v1

```text
status: PASS
execution baseline: HEAD a40019209c133785a4babe06b5e96dfd4673c4f5; T-04 PASS
changed paths:
  src/planning_lite/telemetry.py
  src/planning_lite/cli.py
  tests/test_run_receipts.py
  tests/test_cli.py (no change required)
verification:
  focused RunReceipt/local-only/source/CLI/split/registry suite: PASS (32 passed)
  exact v1 shape/types, nullable unknowns, provenance and outcome validation: PASS
  collector-owned answers ref, disabled no-write and no lifecycle mutation: PASS
  duplicate-byte idempotence, conflicting receipt_id and partial-line corruption: PASS
  append serialization/fsync boundary: implemented; no model/runtime invocation
material finding / stop-gate: none
```

RunReceipt storage remains an external-fact collector only; it does not infer
runtime values or mutate Planning lifecycle state.

## T-05 — Template policy, linkage, documentation, and integrity

```text
status: PASS
execution baseline: HEAD a40019209c133785a4babe06b5e96dfd4673c4f5; T-06 PASS
changed paths:
  CHANGELOG.md
  docs/ARCHITECTURE.ru.md
  docs/OPERATOR_WORKFLOW.ru.md
  docs/UPDATABLE_INSTALLATION.ru.md
  template/.planning/framework/defaults.yml
  template/.planning/control/CONFIG_RESOLUTION.md
  template/.planning/control/STATE_OWNERSHIP.md
  template/.planning/control/GIT_CHANGE_REVIEW.md
  template/.planning/project/PROJECT_INSTRUCTIONS.md
  template/.planning/templates/project/PROJECT_INSTRUCTIONS.md
  template/.planning/changes/templates/progress.md
  template/.planning/changes/templates/review.md
  template/.planning/docs/ARCHITECTURE.md
  template/.planning/docs/MANIFEST_V4.md (regenerated; byte-identical, no diff)
  template/.planning/framework/SHA256SUMS.txt
  tests/test_template.py
verification:
  uv sync: PASS
  uv run --frozen pytest: PASS (244 passed, 88 warnings)
  uv run --frozen python scripts/test_template_update.py: PASS
  uv run --frozen python scripts/test_local_only_update.py: PASS
  focused template/integrity tests: PASS (34 passed)
  manifest path set/count and canonical-LF SHA verification: PASS
  PROJECT_INSTRUCTIONS.md source/template lockstep: PASS
material finding / stop-gate: none
```

T-05 published only the approved policy, Git/linkage, documentation, and
integrity surfaces. No ownership or Copier conditional path was changed.

## Central Candidate Gate — NOT READY / STOP

```text
T-01…T-06: PASS
exact central changed-path audit: PASS (all implementation paths within approved surface)
focused owner/integration evidence: PASS
project-owned preservation evidence: PASS (local-only smoke)
separate owner authorization for checkpoint commit: NOT GRANTED
clean committed central candidate: ABSENT
T-07/T-08: NOT AUTHORIZED / NOT STARTED
```

The bounded Execution authorization ends here. Stop for separate owner
authorization of the exact central checkpoint commit; do not stage, commit, or
run T-07/T-08 in this execution.

## BOUNDARY CORRECTIVE PASS — 2026-09-04

```text
status: PASS
change: CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001
execution baseline: HEAD a40019209c133785a4babe06b5e96dfd4673c4f5; dirty pre-execution tree retained

C-01: PASS — managed defaults are the runtime policy authority; the minimal fallback is used only when legacy consumers lack project_policy; managed-default discriminator passed.
C-02: PASS — bounded traversal prunes .git before descent and rejects escaping links; nested-.git scandir discriminator passed.
C-03: PASS — forbidden_read_paths are enforced for inspection and local bounded scans, fail closed, while unrelated allowed paths continue.
C-04: PASS — inspect exposes independent product_git and control_git configured/available/head/clean contexts for normal, split-control, and local-only modes.
C-05: PASS — receipt append uses cross-process sidecar locking with fail-closed acquisition; duplicate/conflict, append-only, and fsync behavior passed.
C-06: PASS — token categories are opaque externally supplied values; no generic additive total constraint remains.
C-07: PASS — dry-run and apply share read-only plan_registration semantic validation; conflict and split-topology failures are parity-checked without writes.

changed paths:
  src/planning_lite/workspace.py
  src/planning_lite/local_update.py
  src/planning_lite/telemetry.py
  src/planning_lite/cli.py
  tests/test_workspace_registry.py
  tests/test_local_only_update.py
  tests/test_split_control_history.py
  tests/test_run_receipts.py
verification:
  focused corrective suite (`uv run --frozen pytest -q tests/test_workspace_registry.py tests/test_local_only_update.py tests/test_split_control_history.py tests/test_run_receipts.py tests/test_cli.py`): PASS (37 passed)
  uv run --frozen pytest: PASS (254 passed, 88 warnings)
  uv run --frozen python scripts/test_template_update.py: PASS
  uv run --frozen python scripts/test_local_only_update.py: PASS
  git diff --check: PASS
scope audit: PASS — implementation/test paths remain within approved surfaces; lifecycle artifacts are classified separately from pre-existing incoming material.
material findings / stop-gates: none; no new architecture, subsystem, or scope was introduced.

governance classification:
  CURRENT_CHANGE_LIFECYCLE: authority binding, implementation start contract, incoming adjudication, change definition, definition activation, implementation plan, formal readiness, execution ledger.
  PRE_EXISTING_INCOMING: recommendation inbox and prior roadmap snapshot; unchanged.

final state:
  T-01…T-06: PASS
  Central Candidate Gate: NOT READY / STOP
  reason: separate owner authorization for checkpoint commit is absent and a clean committed candidate is absent
  checkpoint commit: NOT DONE
  T-07/T-08: NOT STARTED
  Poker/mood: UNCHANGED
  tag/push/merge/release: NOT DONE
```

## FINAL MICRO-CORRECTIVE PASS — 2026-09-04

```text
status: PASS
change: CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001
execution baseline: HEAD a40019209c133785a4babe06b5e96dfd4673c4f5; existing dirty pre-execution tree retained

MC-01: PASS — legacy fallback is absence-only; present null/scalar managed project_policy fails closed; update validation uses actual managed defaults.
MC-02: PASS — symlink/junction/reparse detection is bounded and standard-library-only; Windows junction no-descent and escaping-target discriminators passed.
MC-03: PASS — non-empty forbidden_read_paths prevent unrestricted product/control Git status; identity/HEAD remain observable, clean is null with explicit status_reason; empty policy preserves clean/dirty behavior.

changed paths:
  src/planning_lite/workspace.py
  src/planning_lite/local_update.py
  tests/test_workspace_registry.py
  tests/test_local_only_update.py
  tests/test_split_control_history.py
focused verification:
  uv run --frozen pytest -q tests/test_workspace_registry.py tests/test_local_only_update.py tests/test_split_control_history.py: PASS (34 passed)
  Windows junction/reparse discriminator: PASS (not skipped)
  product/control Git status guard discriminators: PASS
full regression:
  uv run --frozen pytest: PASS (260 passed, 88 warnings)
git diff --check: PASS (no whitespace errors; standard LF→CRLF warnings only)
scope: PASS — no new architecture, subsystem, Definition/Plan scope, or out-of-boundary path.
material findings / stop-gates: none.

final state:
  C-01…C-07: CLOSED
  T-01…T-06: PASS
  Central Candidate Gate: NOT READY / STOP
  checkpoint commit: NOT PERFORMED
  T-07/T-08: NOT STARTED
  Poker/mood: UNCHANGED
  tag/push/merge/release: NOT DONE
```

## CANONICAL STATE ALIGNMENT / CENTRAL CANDIDATE GATE — 2026-09-04

```text
implementation checkpoint:
abce23b7a4afb0336c48e67b0f334c5b46bbe11a

checkpoint staged-manifest audit:
PASS

committed paths:
32 authorized paths

excluded incoming/history:
not included in implementation checkpoint

recommendation inbox housekeeping:
PASS

recommendation inbox Git exclusion:
PASS

literal clean committed candidate:
YES

Central Candidate Gate:
READY

T-07:
NOT STARTED

T-08:
NOT STARTED

consumer-proof authorization:
NOT GRANTED IN THIS STEP
```

`docs/design/project-spine/recommendations/inbox/**` is treated as local
noncanonical operational intake and is excluded through repository-local Git
exclude.

Future discovery/intake architecture is deferred through:
`PL-REC-OUT-OF-GIT-OPERATIONAL-INTAKE-DISCOVERY-001`.

## T-07 — Poker Disposable Consumer Proof — 2026-09-04

```text
status: BLOCKED
central implementation identity: abce23b7a4afb0336c48e67b0f334c5b46bbe11a
central state-alignment HEAD: 302d7eba2093bf5ae06c7bec72f61e79b8a1ecc2
disposable target: D:\documents\_planning_lite_disposable\poker-proof (removed after evidence)
mode/topology exercised: local-only; .planning/.agents Git-ignored; control Git not configured

registration and effective policy: PASS
registry topology/locators only: PASS
product/control Git separation: PASS (product Git explicit; control Git NOT CONFIGURED)
inspect: PASS
Doctor: PASS
local-only update preview: BLOCKED
stop-gate: Candidate template contains unclassified files: .planning/drift/reviews/.gitkeep
RunReceipt: NOT RUN — proof stopped before the applicable receipt seam

live Poker baseline/result:
  HEAD before: f7b1db0ebd6db936450d49ce177caf0e8f37bf4c
  HEAD after:  f7b1db0ebd6db936450d49ce177caf0e8f37bf4c
  status after: unchanged single expected untracked handoff
LIVE_POKER_MUTATION: NONE

field findings: 0
recommendations created: 0
T-08: NOT STARTED
```

The disposable update path failed closed before mutation because the Copier-
rendered candidate ownership manifest omitted the existing `.gitkeep`
classification. No implementation correction was attempted.

## T-07 BLOCKER CORRECTIVE PASS — 2026-09-04

```text
original T-07 status: BLOCKED
blocker:
  .planning/drift/reviews/.gitkeep ownership mismatch

root cause:
  OTHER_MATERIAL_CAUSE — the disposable proof rendered from the local central
  source without an explicit --vcs-ref, so Copier selected latest tag v4.3.0.
  That tag contains the .gitkeep artifact but predates its ownership entry.
  Frozen ref 302d7eba2093bf5ae06c7bec72f61e79b8a1ecc2 contains both.

correction:
  no runtime or template correction was required; the canonical local-only
  discriminator now explicitly asserts that the rendered .gitkeep is present
  and classified as managed. The proof rerun must bind Copier to the frozen
  central ref rather than implicitly selecting latest tag.

discriminator: PASS
  default Copier resolution: artifact present, ownership_classified=False
  frozen ref 302d7eba2093bf5ae06c7bec72f61e79b8a1ecc2: artifact present,
  ownership_classified=True
  genuinely unknown candidate path remains fail-closed: PASS

focused verification:
  uv run --frozen pytest tests/test_local_only_update.py tests/test_template.py -rA
  18 passed in 5.87s

full regression:
  uv run --frozen pytest
  FAIL — 2 failed, 258 passed, 88 warnings in 15.40s
  NEXT_DISCRIMINATOR_FOUND: existing maintainer_resume/CURRENT semantic
  contract mismatch (tests/test_central_resume_contract.py); unrelated to
  the T-07 ownership seam and not corrected in this bounded pass.

template/local-only smoke:
  uv run --frozen python scripts/test_template_update.py — PASS
  uv run --frozen python scripts/test_local_only_update.py — PASS

disposable reproduction:
  previous unknown-path blocker closed with explicit frozen ref; local-only
  preview passed beyond the blocker; no independent T-07 blocker observed.

live Poker: UNCHANGED
live mood: UNCHANGED
T-07: REQUIRES RERUN
T-08: NOT STARTED
checkpoint commit: NOT PERFORMED
new corrective commit: NOT PERFORMED
T-09: NOT STARTED
```

## CURRENT / MAINTAINER RESUME CONTRACT CORRECTIVE PASS — 2026-09-04

```text
trigger:
  2 full-regression failures after canonical state alignment

root cause:
  A_CURRENT_ALIGNMENT_EXCEEDED_EXISTING_SCHEMA — state alignment added
  implementation_state, corrective_state, implementation_checkpoint,
  checkpoint_commit_audit, literal_clean_committed_candidate,
  central_candidate_gate, recommendation_inbox_housekeeping,
  recommendation_inbox, recommendation_inbox_semantics, future_intake_design,
  T-07, T-08, and T-07_T-08_authorized to the Resume Contract v1 block.
  The existing canonical parser/allowlist permits only its established ten
  keys; it correctly rejected these additions.

correction:
  removed only the 13 non-contract keys from docs/design/project-spine/CURRENT.md.
  Their already-established evidence remains in the surrounding CURRENT prose
  and the Execution Ledger. No permissive parser or new schema vocabulary was
  introduced.

central resume focused:
  uv run --frozen pytest tests/test_central_resume_contract.py -rA
  PASS — 14 passed in 1.33s

local-only discriminator:
  uv run --frozen pytest tests/test_local_only_update.py tests/test_template.py -rA
  PASS — 18 passed in 5.53s

template/local-only smokes:
  uv run --frozen python scripts/test_template_update.py — PASS
  uv run --frozen python scripts/test_local_only_update.py — PASS

full regression:
  uv run --frozen pytest
  PASS — 260 passed, 88 warnings in 13.84s

runtime/template delta from implementation checkpoint:
  NONE — abce23b7a4afb0336c48e67b0f334c5b46bbe11a contains the drift-review
  .gitkeep and managed ownership declaration; current src/** and template/**
  are unchanged relative to that checkpoint.

T-07 previous .gitkeep blocker: CLOSED
T-07: READY_FOR_RERUN
T-08: NOT STARTED
Poker/mood: LIVE PROJECTS UNCHANGED
checkpoint commit: ALREADY EXISTS at abce23b7a4afb0336c48e67b0f334c5b46bbe11a
new corrective commit: REQUIRED AFTER PRE-COMMIT GATES
```

## T-07 — Poker Disposable Consumer Proof Rerun — 2026-09-04

```text
status: PASS
frozen implementation ref: abce23b7a4afb0336c48e67b0f334c5b46bbe11a
disposable mode/topology: split-control external control Git with local-only
  update path; disposable target and home removed after evidence

key assertions:
  registration / effective policy: PASS (paused; telemetry enabled)
  product/control Git separation: PASS
    disposable product HEAD: 75f26c97c2a8521b773eba7b2695af902809f5cc
    disposable control HEAD: c0e38855e19f54b6805ab49f9e68d82296f8fce4
  inspect / Doctor: PASS
  explicit --template-source D:\documents\planning-lite: PASS
  explicit --vcs-ref abce23b7a4afb0336c48e67b0f334c5b46bbe11a: PASS
  .planning/drift/reviews/.gitkeep present and managed: PASS
  genuinely unknown candidate path remains fail-closed: PASS
  local-only preview and apply: PASS
  project-owned Planning preservation: PASS
  forbidden-read guard: PASS
  repeated check/update idempotence: PASS
  all-null RunReceipt in disposable home: PASS
  disposable product/control commits only: PASS

live Poker before/after:
  HEAD: f7b1db0ebd6db936450d49ce177caf0e8f37bf4c / unchanged
  status: one expected untracked handoff / unchanged
LIVE_POKER_MUTATION: NONE

field findings: 0
recommendations created: 0
T-08: authorized to start
```

## T-08 — mood Disposable Consumer Proof — 2026-09-04

```text
status: BLOCKED
frozen implementation ref: abce23b7a4afb0336c48e67b0f334c5b46bbe11a
disposable mode/topology: fresh mood-derived unborn product fixture

key assertions:
  selective-ignore baseline reproduced: PASS
  exposed project-owned discriminator:
    .planning/project/CURRENT_STATE.md is not ignored: PASS
  control-init refusal before an unambiguous full .planning ignore: BLOCKED

material blocker:
  control-init accepted the selective-ignore baseline because its current
  outer-ignore check treats the directory path .planning/ as ignored when a
  child-glob matches, even though project-owned .planning/project/** remains
  exposed. This violates the accepted requirement that split-control setup
  wait for an unambiguous full .planning ignore.
  NEXT_DISCRIMINATOR_FOUND

source rebind / update / Doctor / receipt: NOT RUN after blocker
live mood before/after:
  HEAD: unborn / unchanged
  status: 50 untracked baseline paths / unchanged
LIVE_MOOD_MUTATION: NONE

field findings: 1 material accepted-AC blocker
recommendations created: 0
T-08: STOPPED
```

## T-08 CONTROL-INIT SELECTIVE-IGNORE CORRECTIVE PASS — 2026-09-04

```text
T-07: PASS
original T-08 status: BLOCKED
blocker:
  control-init accepted a selective-ignore baseline because the outer-ignore
  validation checked only selected .planning spellings; .planning/project/**
  could remain exposed while .planning/ was reported ignored.

root cause:
  IGNORE_VALIDATION_CHECKS_ONLY_SELECTED_PATHS

correction:
  narrowed the existing _outer_ignores_planning seam to require effective Git
  ignore coverage for the .planning root, representative project/control
  paths, and every existing top-level planning child. No .gitignore auto-write,
  partial acceptance, or second authority was introduced.

focused regression:
  uv run --frozen pytest -q tests/test_split_control_history.py
  tests/test_workspace_registry.py -rA — PASS — 23 passed
  selective-ignore project/** and control/** cases: FAIL CLOSED
  full-ignore (.planning/) and root-ignore (.planning) cases: PASS
  rejection mutation guard: PASS (no control Git, product HEAD unchanged,
  product .gitignore unchanged)

disposable invalid case: PASS — selective-ignore fixture rejected fail-closed
disposable valid case: PASS — fully ignored fixture initialized split control

applicable smokes:
  uv run --frozen python scripts/test_template_update.py — PASS
  uv run --frozen python scripts/test_local_only_update.py — PASS

full regression:
  uv run --frozen pytest
  PASS — 263 passed, 88 warnings in 17.24s

git diff --check: PASS (LF-to-CRLF warnings only)
scope audit: PASS — only src/planning_lite/workspace.py,
  tests/test_split_control_history.py, and this ledger changed

live Poker: UNCHANGED
live mood: UNCHANGED
T-08: REQUIRES RERUN
T-09: NOT STARTED
original implementation checkpoint:
  abce23b7a4afb0336c48e67b0f334c5b46bbe11a
corrective commit authorization: bounded and satisfied after all gates
```
