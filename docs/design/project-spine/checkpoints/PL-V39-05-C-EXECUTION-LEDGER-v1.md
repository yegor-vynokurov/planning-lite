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
