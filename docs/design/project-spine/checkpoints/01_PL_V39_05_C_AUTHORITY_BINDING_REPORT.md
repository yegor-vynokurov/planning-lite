# PL-V39-05-C — Authority Binding Report

- Status: `READ-ONLY DISCOVERY / DESIGN BINDING`
- Date: `2026-09-03`
- Audited central HEAD: `a40019209c133785a4babe06b5e96dfd4673c4f5`
- Branch: `reconcile/current-design-spine-2026-08-25`
- Owner input SHA-256: `f47016c94ff8c7f4e608f0998076e4bc152897b51aa1f6871872e95fc909015b`
- Implementation authorized: `NO`
- Change created: `NO`
- Roadmap/lifecycle state changed: `NO`

```text
PL_V39_05_C_AUTHORITY_BINDING:
PASS
```

## 1. Executive verdict

`PL-V39-05-C` can be bound to the current Planning Lite architecture without a
new Roadmap phase and without taking ownership from `PL-V39-06/07/08`.

The smallest coherent boundary is a foundation, not a platform:

```text
existing repository-local .planning/.agents
+ existing CONFIG / ownership / Copier / Doctor / Change records
+ one local Planning Lite home resolver
+ one project registry
+ explicit product-Git vs control-Git contexts
+ one externally-fed raw RunReceipt stream
+ disposable Poker/mood migration proofs
```

The implementation must not add semantic memory, model routing, checklists,
eval interpretation, analytics, orchestration, a daemon, or centralized copies
of consumer control history.

Three current facts materially shape the contract:

1. current CLI/update logic already supports Git-ignored local-only
   `.planning/.agents`, so product Git tracking is not a product requirement;
2. split-control Git is not yet a supported topology: Git checks address only
   the product repository and Doctor cannot validate a control repository;
3. the Campaign runtime proves that append-only receipts and externally supplied
   `total_tokens` are viable, but it is specialized evaluation infrastructure
   and must not be reused as the semantic model for ordinary project runs.

No material authority conflict blocks the contract. The tracked architecture
document's claim that consumers contain no nested `.git` conflicts with the new
owner constraint, but the owner constraint expressly chooses independent
control history. The bounded implementation must update that obsolete document;
it does not require another owner decision.

## 2. Current canonical authority

### 2.1 Precedence

The current precedence is explicit in
`docs/design/project-spine/INFORMATION-ARCHITECTURE-v1.md`:

1. live Git checkout identity;
2. `docs/design/project-spine/CURRENT.md` for resume/navigation;
3. `docs/design/project-spine/roadmap/ROADMAP.md` for direction/sequence;
4. a tracked active Change or transition receipt referenced by `CURRENT.md`;
5. checkpoints/support as evidence;
6. archived Roadmaps/recommendations as lineage;
7. `.planning-lab/**` as non-canonical research state.

The Resume Contract at the top of `CURRENT.md` explicitly overrides historical
prose later in that file.

### 2.2 Current source/version identity

| Identity | Observed value | Meaning |
|---|---|---|
| Git root | `D:/documents/planning-lite` | inspected central source |
| HEAD | `a40019209c133785a4babe06b5e96dfd4673c4f5` | exact current source identity |
| Git describe | `v4.3.0-46-ga400192` | 46 commits after latest stable tag |
| Latest stable tag | `v4.3.0` | current released baseline |
| `uv run planning-lite --version` | `4.3.1.dev34+g4fbfb3179` | stale installed `.venv` metadata, not current source identity |

Planning Lite has no hard-coded package/template version. `pyproject.toml` uses
`hatch-vcs`; `src/planning_lite/__init__.py` reads installed distribution
metadata; consumers read `_commit`/`_vcs_ref` from
`.copier-answers.planning-lite.yml`. Until environment metadata is refreshed,
the exact current development source is identified by Git HEAD, not by the
stale CLI value.

### 2.3 Roadmap and lifecycle

- Canonical Roadmap: `docs/design/project-spine/roadmap/ROADMAP.md`, design
  revision `v3.9.3`.
- Central active Change: `NONE`.
- Central lifecycle gate: `DISCOVERY_READY`.
- Implementation authorized: `NO`.
- Next permitted action: `plan_next_pl_v39_05_slice`.
- `PL-V39-05-A`: closed.
- `PL-V39-05-B`: closed.
- `PL-V39-05`: still the current major Roadmap block; its exit gate is not yet
  declared complete.

### 2.4 Does canonical `PL-V39-05-C` already exist?

No tracked canonical artifact currently defines a `PL-V39-05-C` sub-slice.

An untracked file,
`docs/design/project-spine/roadmap/UPDATED-ROADMAP-PLANNING-LITE-POKER-CHG-0009-2026-09-01.md`,
uses the label `PL-V39-05-C` for `Adaptive Engagement + Strategy Portfolio`.
It is not canonical because:

- it is untracked;
- `CURRENT.md` names only `roadmap/ROADMAP.md` as current;
- current precedence does not allow a similarly named snapshot to override the
  stable Roadmap.

The owner input for this audit assigns `PL-V39-05-C` to `Consumer Control
Topology + Project Policy + Telemetry Baseline`. This can be used as the
candidate bounded-slice identity without creating a new major phase. The
untracked collision must remain untouched and be explicitly adjudicated before
implementation writes begin.

### 2.5 Canonical consumer artifact representations

| Meaning | Canonical representation |
|---|---|
| Active pointer/lifecycle | `.planning/ACTIVE.md` |
| Change | `.planning/changes/active|completed/<change>/proposal.md` and `specification.md` |
| Approved plan | active Change `plan.md` |
| Task state | active Change `tasks.md` |
| Progress/evidence | active Change `progress.md` |
| Readiness | active Change `readiness.md` |
| Completion/closure | active/completed Change `review.md` |
| Handoff | active Change `context.md`; session transitions use `control/SESSION_CHECKPOINT.md` |
| Amendments | active Change `amendments.md` |
| Decision | `.planning/decisions/<item>` with `decisions/INDEX.md` as summary |
| Recommendation | `.planning/recommendations/items/<item>`; item authoritative, `INDEX.md` summary |
| Durable project facts/rules | `.planning/project/**` |
| Machine configuration | managed `.planning/framework/defaults.yml` plus project-owned `.planning/CONFIG.yml` |
| Ownership/update policy | `.planning/framework/OWNERSHIP.yml` plus `copier.yml` |

Evidence: `template/.planning/control/STATE_OWNERSHIP.md`,
`template/.planning/changes/templates/**`, and
`template/.planning/control/CONFIG_RESOLUTION.md`.

## 3. Existing architecture relevant to 05-C

### 3.1 Fixed consumer topology

The current template and CLI assume repository-relative roots:

```text
<project>/.planning
<project>/.agents
<project>/.copier-answers.planning-lite.yml
<project>/AGENTS.md
```

Evidence:

- `src/planning_lite/cli.py` constants and `_iter_required_paths()`;
- `template/AGENTS.md`;
- `copier.yml`;
- `template/.planning/framework/OWNERSHIP.yml`;
- `tests/test_template.py`, `tests/test_cli.py`,
  `tests/test_local_only_update.py`.

There is no configurable Planning root, Agents root, consumer registry, or
repository discovery command. CLI target paths are explicit and resolved to an
absolute path. The only parent walk is `_discover_template_source()`, which
discovers the central template source from the current directory.

### 3.2 CLI/install/adopt/update/Doctor

- `install`: renders the template; Git is not required.
- `adopt`: requires a Git repository and normally a clean product tree.
- `check`: previews update; auto-detects ignored/local-only managed roots.
- `update`: uses ordinary Copier for tracked managed trees or the explicit
  ownership-aware local-only path for ignored roots.
- `doctor`: validates required files, bridge, answers YAML, stray `*.jinja`, and
  product Git presence/dirty state; it reports the installed ref from Copier
  metadata.
- There is no CLI named `hydrate`, `init`, registry, split-control, or generic
  run-receipt command.
- Project-document hydration is an agent workflow in
  `.planning/control/PROJECT_BOOTSTRAP.md`, not a distribution CLI operation.

### 3.3 Recursive scans

`src/planning_lite/local_update.py::iter_files()` recursively enumerates the
entire target and candidate trees with `Path.rglob("*")`. Candidate paths fail
closed when ownership is unknown, but target extras are generally preserved.
The target scan does not prune `.git`, nested control Git metadata, virtual
environments, or policy-forbidden read paths.

`command_doctor()` also performs a target-wide `rglob("*.jinja")`.

This is acceptable for today's single/local-only topology but is an explicit
split-control compatibility gap. `05-C` must prevent traversal of `.git`
metadata and must not turn forbidden-read policy into a broad security product.

## 4. Product/control Git compatibility

### B1 — Can `.planning` already be a separate Git working tree?

Not as a supported Planning Lite topology.

The filesystem/update algorithm will normally preserve an extra
`.planning/.git` gitfile or directory because it is absent from the candidate
and not classified as managed. However, current docs, Doctor, Git cleanliness
checks, and lifecycle review know only the product repository. There is no test
proving nested/external control Git behavior. Therefore physical survivability
is not sufficient to claim compatibility.

### B2 — Does code assume product Git equals Planning/control Git?

Yes, wherever Planning Lite asks Git questions. `src/planning_lite/cli.py`
implements `_git_output(target, ...)` as `git -C <target>` and uses it for repo
identity, dirty state, tags, and ignore detection. `target` is always the
consumer/project root for install/update/Doctor paths. There is no second Git
context.

The Campaign runtime uses explicit artifact roots and does not solve consumer
control Git.

### B3 — Must `.planning/**` be tracked by product Git?

No product check requires that today.

Positive evidence:

- `_local_only_managed_roots()` detects ignored `.planning/.agents`;
- ordinary update is blocked fail-closed for that mode;
- explicit local-only update preserves project-owned files byte-for-byte;
- `tests/test_local_only_update.py` owns this behavior;
- `docs/UPDATABLE_INSTALLATION.ru.md` and `docs/OPERATOR_WORKFLOW.ru.md`
  document intentionally ignored Planning roots.

Limitation: workflow-level Git reviews and task attribution that use ordinary
product `git status` cannot observe ignored control files. The untracked
`PL-REC-TASK-VERIFIER-BASELINE-SNAPSHOT-001-v1.1.md` records this field defect,
but its checklist implementation remains routed to `PL-V39-07/08`.

### B4 — What happens with `.planning/.git`?

Current expected behavior by code inspection:

- a gitfile is an unknown target-only file and is preserved;
- a nested `.git` directory is recursively enumerated as target extras and
  preserved, but its metadata is unnecessarily discovered;
- managed/project-owned update actions still address paths beneath
  `<project>/.planning`;
- product Git status/cleanliness remains the only Git gate;
- Doctor does not validate the control Git identity, work tree, dirty state,
  gitfile target, or overlap with product Git;
- no existing test owns this case.

The bounded supported form should therefore be a `.planning/.git` gitfile whose
Git directory is outside the product tree under Planning Lite home. A nested
metadata directory should not be the preferred form.

### B5 — Raw cwd-based Git calls

Consumer Git helpers use explicit `git -C <target>`. Raw Git calls with
`cwd=<target>` exist in the central release command and test/operator scripts;
they are intentional for the central/source repository. Ordinary Copier update
runs with the consumer product root as cwd and Copier owns its internal Git
behavior.

The gap is not accidental cwd selection inside consumer helpers; it is the
absence of an explicit control-repository helper/context. `05-C` must add one
and must forbid bare consumer `git` calls that rely on ambient cwd.

### Documentation conflict

`docs/ARCHITECTURE.ru.md` currently states that a working project has no nested
`.git` and that installed files are ordinary parts of product history. This is
already too strong for the supported local-only mode and directly conflicts
with split-control mode. It must be corrected during `05-C`.

## 5. Existing project-policy/config surfaces

| Surface | Classification | Reason |
|---|---|---|
| `.planning/framework/defaults.yml` | `EXTEND` | canonical managed defaults; suitable for default policy values |
| `.planning/CONFIG.yml` | `EXTEND` | canonical project-owned machine overrides; correct home for stable executable project policy |
| `.planning/control/CONFIG_RESOLUTION.md` | `EXTEND` | already defines defaults + project override precedence |
| `.planning/project/PROJECT_INSTRUCTIONS.md` | `REUSE` | durable repository-specific operational prose, explicitly not session history |
| `.planning/project/PROJECT_RULES.md` | `REUSE` | hard constraints, engineering, data/safety, compatibility, exceptions |
| `.planning/framework/OWNERSHIP.yml` | `REUSE/EXTEND` | owns managed/project-owned/installer metadata boundaries, not semantic policy |
| `.copier-answers.planning-lite.yml` | `CONFLICT` as policy | installer-owned/overwritten; correct for source/ref, wrong for project rules |
| `.planning/AGENT_PROFILE.yml` | `INSUFFICIENT` | agent adapter identity only; not model identity or project policy |
| `.planning/ACTIVE.md` | `CONFLICT` as policy | transient lifecycle pointer; policy must not be stored here |
| active Change files | `CONFLICT` as policy | bounded work/history, not project-lifetime invariants |
| `PROJECT_CHARTER.md` | `INSUFFICIENT` | product purpose/scope, not operational control configuration |
| `REPOSITORY_MAP.md` | `INSUFFICIENT` | discovery cache, explicitly not unquestioned truth |

The correct machine-readable surface already exists: add a namespaced
`project_policy` block to the effective configuration contract. Keep host-local
absolute paths (product root and external Git directory) in the central
registry, not in portable project policy. Keep domain-specific prose rules in
`PROJECT_RULES.md`/`PROJECT_INSTRUCTIONS.md`.

No new `POLICY.yml` is justified.

## 6. Existing global/home/registry surfaces

Current global state is limited to:

```text
~/.config/planning-lite/config.toml
PLANNING_LITE_TEMPLATE
```

`config.toml` stores only a user template-source override.
`src/planning_lite/cli.py::CONFIG_PATH` is the existing stable directory seam.

Absent today:

- `PLANNING_LITE_HOME`;
- project/consumer/workspace registry;
- global state/cache root distinction;
- control Git location registry;
- generic telemetry root.

Minimal extension:

```text
PLANNING_LITE_HOME (optional override)
default = existing ~/.config/planning-lite directory

<home>/config.toml
<home>/projects.yml
<home>/control/<project-id>.git
<home>/telemetry/<project-id>/run-receipts.jsonl
```

This reuses the existing global config directory. It adds no daemon, server,
database, discovery crawler, remote backup, or centralized semantic memory.

The registry stores topology and locators. Live installed ref and Planning
lifecycle are read from the registered consumer on inspection rather than
copied as competing truth.

## 7. Existing telemetry capability

### 7.1 Current surfaces

1. `.planning/observability/SKILL_USAGE.csv` is optional and disabled by
   default. Its current fields are `timestamp_utc, skill, invocation,
   lifecycle_stage, change_id`. It is best-effort and non-authoritative.
2. Change `progress.md`, `context.md`, `readiness.md`, and `review.md` preserve
   execution/verification/handoff evidence, but not a normalized per-invocation
   receipt.
3. `planning_lite.campaign` has immutable manifests, timestamped hash-linked
   journal events, attempts, reviewer roles, outcomes, handoffs, budgets,
   duration, and externally supplied `total_tokens`.
4. The balanced-suite adapter reads only `tokens.total_tokens` from external
   `metrics.json`; it does not project input/output/cached/reasoning tokens or
   model identity.

Campaign is an opt-in evaluation candidate with an operator-supplied
`campaign_root`. It must not be made the generic consumer-run registry.

### 7.2 Field availability matrix

| Field | Status now | Exact boundary/evidence |
|---|---|---|
| Project | `DERIVABLE NOW` | Copier `project_name` and target path; no stable project ID |
| Installed Planning Lite ref | `AVAILABLE NOW` | consumer `.copier-answers.planning-lite.yml` `_commit`/`_vcs_ref` |
| Change | `AVAILABLE NOW` | `.planning/ACTIVE.md` and Change folder |
| Task | `AVAILABLE NOW` | `ACTIVE.md` and `tasks.md` |
| Run/task family | `NOT AVAILABLE` generally | Campaign has `eval_id`/adapter only for its own suites |
| Agent shell/adapter | `DERIVABLE NOW` | answers/`AGENT_PROFILE.yml`; current Poker/mood profiles are blank and therefore unreliable |
| Agent role | `DERIVABLE NOW` in bounded cases | Campaign has independent reviewer role; generic executor/verifier role is not normalized |
| Model/model tier | `AVAILABLE FROM EXTERNAL RUNTIME ONLY` | no Planning Lite API receives Luna/Sol/model tier |
| Invocation count | `NOT AVAILABLE` generally | campaign attempts and skill rows are narrower proxies, not model-call accounting |
| PASS/FAIL/BLOCKED outcome | `DERIVABLE NOW` | lifecycle/eval artifacts exist, but no generic run outcome record |
| Input tokens | `AVAILABLE FROM EXTERNAL RUNTIME ONLY` | not ingested today |
| Output tokens | `AVAILABLE FROM EXTERNAL RUNTIME ONLY` | not ingested today |
| Cached tokens | `AVAILABLE FROM EXTERNAL RUNTIME ONLY` | not ingested today |
| Reasoning tokens | `AVAILABLE FROM EXTERNAL RUNTIME ONLY` | not ingested today; private reasoning content is out of scope |
| Total tokens | `AVAILABLE FROM EXTERNAL RUNTIME ONLY` | Campaign stores it only when external suite metrics supply it |
| Token-count source | `NOT AVAILABLE` | current receipt does not record provenance for the count |
| Verifier/reviewer use | `DERIVABLE NOW` | review artifacts/Campaign roles, not normalized per invocation |
| Model escalation | `NOT AVAILABLE` | routing/escalation is future `PL-V39-07` |
| Retry/recheck | `DERIVABLE NOW` incompletely | attempts and repeated evidence can imply it, but there is no reliable generic field |
| Planning/non-Planning read counts | `AVAILABLE FROM EXTERNAL RUNTIME ONLY` | no current file-access instrumentation |
| Timestamps | `AVAILABLE NOW` in Campaign; partial elsewhere | Campaign journal timestamps are explicit |
| Execution receipt | `AVAILABLE NOW` only for Campaign/review-specific flows | no generic consumer RunReceipt |
| Handoff | `AVAILABLE NOW` | Change context and Campaign handoff capsules |
| Evaluation | `AVAILABLE NOW` for Campaign | not general task telemetry |
| Model routing | `NOT AVAILABLE` | Roadmap ownership is `PL-V39-07` |

### 7.3 F1/F2/F3 verdicts

- F1: Planning Lite cannot obtain exact token categories by itself. The raw
  collector may accept them from an external runtime and must store `null` plus
  `source: unavailable` when absent. No estimation is allowed.
- F2: Planning Lite cannot reliably distinguish Luna, Sol, or other model tiers
  today. Agent adapter identity is not model identity.
- F3: `Luna implementation × N / Sol verification × N` cannot be reliably
  computed today. It becomes derivable only from one normalized receipt per
  externally identified invocation.

## 8. Version/hydration/migration mechanism

### 8.1 Canonical current mechanism

- release version source: annotated Git tags;
- Python distribution version: `hatch-vcs` metadata;
- installed consumer framework ref: Copier answers `_commit`/`_vcs_ref`;
- source path: Copier `_src_path`;
- update: Copier for tracked mode, ownership-aware atomic local update for
  ignored/local-only mode;
- managed/project-owned boundaries: `OWNERSHIP.yml` and `copier.yml`;
- repair: fail-closed ownership checks plus in-process rollback for local-only
  writes;
- migrations: managed migration docs and ordinary governed Changes; no general
  migration engine or rollback command.

### 8.2 What “update Poker and mood to PL-V39-05-C” must mean

It cannot mean writing the label `PL-V39-05-C` into either consumer.

It means, after central implementation completion and a separately authorized
release:

1. install/use one exact new stable Planning Lite tag;
2. preview each consumer update against that exact tag;
3. apply only the correct update mode;
4. preserve all existing project-owned control bytes except separately approved
   topology/policy additions;
5. register the project and validate its selected control-history mode;
6. prove product Git and control Git independence where split mode is selected;
7. run consumer Doctor and project-specific acceptance;
8. record the new exact `_commit` in Copier metadata;
9. do not close, reopen, or reprioritize consumer Changes as a side effect.

Current facts:

- Poker is at `_commit: v4.3.0-45-gc9deee6`, ignores `.planning` and `.agents`,
  has active `CHG-0009` in `Verification / Ready`, and has one untracked
  `handoffs/**` file in product Git.
- mood is at `_commit: v4.3.0-30-g1a027a6`, has no product HEAD, has an entirely
  untracked baseline, and its `_src_path` points to a local validated snapshot.
  Its completed execution awaits an owner decision.

The current update CLI cannot explicitly override `_src_path` during update;
that is a concrete `05-C` migration gap for mood. Initial install/adopt must
retain the tested precedence `explicit override → environment → nearby central
checkout → configured source → official fallback`. Update must retain the
installed answers source unless an explicit rebind is requested.

## 9. Recommendation collection mechanism

### 9.1 Consumer mechanism

Consumer recommendations already have:

- item identity/status/source fields;
- optional stable semantic-unit IDs;
- converted Change links;
- unit disposition and primary lineage;
- item authority plus `INDEX.md` discovery summary;
- overlap search, manual deduplication, reconciliation, and absorption rules.

Evidence:

- `template/.planning/recommendations/TEMPLATE.md`;
- `template/.planning/recommendations/INDEX.md`;
- `template/.planning/control/RECOMMENDATION_LIFECYCLE.md`;
- `template/.planning/control/RECOMMENDATION_ABSORPTION.md`.

### 9.2 Central Planning Lite mechanism

Central recommendations use `inbox/`, `active/`, `FUTURE-RESERVE.md`, and
archives under `docs/design/project-spine/recommendations/`. Absorption is
manual/unit-aware. The central source currently has no live recommendation
index file; `active/` contains only its README.

The five field documents in central inbox are currently untracked. Two files
carry the same task-verifier recommendation ID (`v1.0` and `v1.1`), with v1.1
declaring supersession. This is concrete evidence that index/dedup remains a
manual governance operation.

The desired model is compatible with current semantics:

```text
consumer control history
  = authoritative recommendation item and unit ledger

central Planning Lite home/source
  = project locator + optional recommendation-index locator/metadata
  != copied consumer history
```

`05-C` should register only the consumer recommendation-index path and
availability. Cross-project semantic ingestion, deduplication, prioritization,
and learning remain `PL-V39-08`/continuous governance work.

### 9.3 Deferred field findings

The following are preserved and routed, not implemented in `05-C`:

| Finding | Destination |
|---|---|
| Pre-Readiness Closure Completeness Sweep | `PL-V39-07`, eval follow-through `08` |
| Task-Verifier Pre-Execution Baseline | `PL-V39-07`, verifier eval `08` |
| Ignored Planning control-path baseline | `PL-V39-07/08` |
| Governed exception identity | `PL-V39-07/08` |
| Primary/secondary failure separation | `PL-V39-07/08` |
| Attempt lifecycle state | `PL-V39-07/08` |
| Governed preflight-only mode | `PL-V39-07` |
| Semantic interface vs concrete type | `PL-V39-07` |
| Nominal identity types | `PL-V39-07/08` |
| Operational admissibility | `PL-V39-08`, with `07` contract input |
| Execution-authority rollover | `PL-V39-07` |
| Diagnostic-to-corrective escalation | `PL-V39-07/08` |

The generic `RunReceipt` transport may later carry facts about retries or roles;
it must not implement these policies.

## 10. Conflicts / unknowns

| Item | Classification | Disposition |
|---|---|---|
| `docs/ARCHITECTURE.ru.md` forbids nested Git by assertion | Current-doc conflict with owner direction | update in `05-C`; no owner re-decision required |
| Untracked Roadmap snapshot assigns another meaning to `05-C` | Non-authoritative name collision | preserve untouched; adjudicate before writes |
| Six pre-existing untracked central files | Implementation-start blocker until adjudicated | do not overwrite/adopt implicitly |
| `.venv` distribution metadata points to old commit | Environment drift | refresh with `uv sync`; Git remains source identity |
| Poker/mood `AGENT_PROFILE.yml` has empty `primary_agent` | Current data-quality defect | do not infer model/role from it; migration validation may repair only with authorization |
| No generic model/token API | Capability boundary | nullable externally supplied telemetry fields |
| No nested/external control Git tests | Engineering gap | add focused tests before field migration |
| mood has no product HEAD and a fully untracked baseline | Material migration precondition | owner must authorize baseline split/order before live mutation |
| Poker product tree has an untracked handoff and active Change | Material migration precondition | checkpoint/adjudicate; do not bypass with casual `--allow-dirty` |
| mood answers source is a local snapshot | Update-source gap | add explicit update source rebind while preserving precedence |
| Central recommendation inbox has duplicate revision identity and no index | Governance gap | preserve/route; do not build semantic DB in `05-C` |

## 11. Reuse vs new implementation map

| Capability | Existing mechanism | Evidence path | Reuse / Extend / New | 05-C / 06 / 07 / 08 |
|---|---|---|---|---|
| Repository-local Planning root | fixed `.planning` | `src/planning_lite/cli.py`, `template/` | Reuse | 05-C |
| Agent adapter root | fixed `.agents` | `template/.agents`, `OWNERSHIP.yml` | Reuse | 05-C |
| Managed/project-owned split | ownership manifest + Copier skip | `OWNERSHIP.yml`, `copier.yml` | Extend only for topology metadata | 05-C |
| Consumer installed ref | Copier answers | `cli.py::command_doctor` | Reuse | 05-C |
| Template source precedence | `_discover_template_source()` | `cli.py`, `test_template_source.py` | Extend for update rebind | 05-C |
| Local-only update | atomic ownership-aware plan/apply | `local_update.py`, `test_local_only_update.py` | Extend for Git-metadata pruning | 05-C |
| Consumer Doctor | structural validation | `cli.py::command_doctor` | Extend for registered topology/dual Git | 05-C |
| Machine project policy | defaults + `CONFIG.yml` | `CONFIG_RESOLUTION.md` | Extend | 05-C |
| Prose project invariants | `PROJECT_RULES/INSTRUCTIONS` | `template/.planning/project/` | Reuse | 05-C |
| Product/control commit linkage | progress Git reference | Change templates | Extend with explicit aggregate SHAs | 05-C |
| Global config directory | `~/.config/planning-lite` | `cli.py::CONFIG_PATH` | Extend as home | 05-C |
| Project registry | none | — | New, one local YAML file | 05-C |
| Split-control Git resolver | none | — | New, explicit Git context | 05-C |
| Separate control Git storage | none | — | New, external gitdir + gitfile | 05-C |
| Generic raw RunReceipt | none | Campaign is specialized | New, one nullable schema/collector | 05-C |
| Receipt integrity patterns | Campaign JSON/hash/timestamps | `src/planning_lite/campaign/` | Reuse patterns, not domain model | 05-C |
| Skill usage log | optional CSV | `SKILL_USAGE_LOGGING.md` | Reuse unchanged | 07/08 consumer |
| Context/memory/handoff semantics | existing context + future Roadmap | `ROADMAP.md` §8 | No expansion | 06 |
| Model/effort routing | future Roadmap owner | `ROADMAP.md` §9 | Not implemented | 07 |
| Checklists/task-verifier policy | field recommendations | untracked inbox inputs | Preserve/route | 07/08 |
| Analytics/eval/learning | Campaign + future Roadmap | `ROADMAP.md` §10 | Not generalized | 08 |
| Recommendation semantic aggregation | manual absorption | recommendation governance | Not centralized | 08/continuous |

## 12. Proposed exact PL-V39-05-C boundary

All candidate items C-01 through C-08 fit one bounded slice only under these
interpretations:

- C-01: document and enforce explicit product/control Git contexts; no Git
  hosting, backup, or automatic commits.
- C-02: extend the existing global config directory into a local home; no
  daemon/server/database.
- C-03: one atomic local registry of topology/locators; live lifecycle/version
  is derived on inspection; no semantic project copy.
- C-04: extend `CONFIG.yml`/defaults and existing project rules; no new policy
  artifact.
- C-05: product commits use ordinary subjects; Change review/progress records
  product SHA(s); public changelog reference is optional.
- C-06: externally fed raw receipts with explicit `null/unavailable`; no
  automatic host instrumentation, aggregation, evaluation, or dashboard.
- C-07: disposable Poker replay and a separately gated live migration recipe;
  no live Poker mutation in central implementation.
- C-08: disposable unborn/early mood replay and a separately gated live
  adoption recipe; no live mood mutation in central implementation.

If live consumer migration, semantic recommendation indexing, analytics, or
automatic runtime instrumentation is made part of the same authorization, the
slice ceases to be bounded and must stop for amendment.

## 13. Roadmap impact

No new major Roadmap phase is required and this audit does not edit the current
Roadmap.

The dependency boundary is:

```text
PL-V39-05-C
  topology identity + durable policy + raw measurement transport
        ↓
PL-V39-06
  context / memory / handoffs consume registered project identity,
  but registry/telemetry never become semantic memory
        ↓
PL-V39-07
  execution roles, routing, checklists, escalation, verifier policy
        ↓
PL-V39-08
  eval interpretation, aggregation, learning, PromptOps
```

After `05-C` is separately defined, approved, implemented, verified, and
closed, the existing next major Roadmap block remains `PL-V39-06`.

This report is design evidence only. It creates no Change, accepts no Roadmap
mutation, authorizes no implementation, initializes no control Git, installs no
telemetry, and migrates no consumer.

```text
PL_V39_05_C_AUTHORITY_BINDING:
PASS
```
