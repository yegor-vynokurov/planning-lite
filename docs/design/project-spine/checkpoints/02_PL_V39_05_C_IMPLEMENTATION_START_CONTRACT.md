# PL-V39-05-C — Implementation Start Contract

- Status: `READY FOR OWNER BOUNDARY REVIEW / NOT AUTHORIZED`
- Date: `2026-09-03`
- Slice: `PL-V39-05-C`
- Subject: `Consumer Control Topology + Project Policy + Telemetry Baseline`
- Binding report: `docs/design/project-spine/checkpoints/01_PL_V39_05_C_AUTHORITY_BINDING_REPORT.md`
- Central source revision audited: `a40019209c133785a4babe06b5e96dfd4673c4f5`
- Implementation authorization: `NO`
- Live consumer migration authorization: `NO`
- Release/tag/push/merge authorization: `NO`

## 1. Start gate

This contract does not authorize implementation.

Implementation may start only after all of the following occur in the normal
central lifecycle:

1. the owner explicitly accepts or amends this `05-C` boundary;
2. the six pre-existing untracked central files are adjudicated without silent
   adoption, deletion, or overwrite;
3. a bounded central Change Definition is created and explicitly approved;
4. its implementation Plan is explicitly approved;
5. Formal Readiness returns `READY`;
6. the owner separately authorizes Execution.

Readiness is not Execution authorization. Central implementation is not live
Poker/mood migration authorization. Completion is not release authorization.

## 2. Exact authoritative inputs

Authority is bound to the following revisions/content:

| Input | SHA-256 / identity | Authority supplied |
|---|---|---|
| Live central checkout | `a40019209c133785a4babe06b5e96dfd4673c4f5` | source identity |
| Owner request `PL-V39-05-C — CURRENT AUTHORITY BINDING...` | `f47016c94ff8c7f4e608f0998076e4bc152897b51aa1f6871872e95fc909015b` | accepted design constraints and audit scope |
| `docs/design/project-spine/CURRENT.md` | `be506b15e2a11edaf567a26a97a033926acdbd72fa8ee4b685f4eaf4e031eb2b` | current lifecycle/navigation |
| `docs/design/project-spine/roadmap/ROADMAP.md` | `a440375b85a5cd990b8d2641f19857b1a3cf3b6189c0cc6ad04671279c0ea337` | current major sequence and `05/06/07/08` ownership |
| `docs/design/project-spine/INFORMATION-ARCHITECTURE-v1.md` | `24a66d4b8fc2c48bf36a103af08e7f7fbb6515ef1ffd83ce53f815e38d59058a` | authority precedence |
| `01_PL_V39_05_C_AUTHORITY_BINDING_REPORT.md` | `1d85b17b466bb0b0dad0b110047d25d5ee16bf753b38dc4da5a935778b7bce81` | audited implementation boundary |
| `template/.planning/framework/OWNERSHIP.yml` | `2673c6defbb1396d068c5f00ad4e5ace4b6bf1f3ba8657c0b4f1b0a831440a6d` | existing ownership taxonomy |
| `template/.planning/framework/defaults.yml` | `ab8c2b0f4a13fc707ee25ad4f1c5da40d97fe336d04ce6c6fe88e621161a3165` | existing configuration defaults |
| `src/planning_lite/cli.py` | `b28adb5a0c000e9de76f0c0bf1b7b905aaaa5cb39bc4f661dcdb431f701e3319` | existing CLI/Git/update/Doctor behavior |
| `src/planning_lite/local_update.py` | `bc1296a3cd5806d46b5e22da003eb0639737acce57bc4d3f44eaab8f0674e025` | current local-only update behavior |

Before activation, re-hash all path inputs. Any material drift requires a
bounded amendment or a repeated binding check; do not silently use stale line
references.

The following are evidence, not direction authority:

- the five untracked field-recommendation/adjudication files;
- the untracked updated Roadmap snapshot;
- Poker and mood live consumer state;
- Campaign integration documentation and tests.

## 3. Exact implementation outcome

After the separately authorized central Change, Planning Lite must support this
deterministic local topology:

```text
product repository
├── normal product Git
├── .planning/                 control working tree
│   └── .git                   gitfile only in split-control mode
├── .agents/                   managed/reproducible adapters
└── .copier-answers.planning-lite.yml

Planning Lite home
├── config.toml                existing user configuration
├── projects.yml               topology/locator registry
├── control/<project-id>.git/  external control Git metadata
└── telemetry/<project-id>/run-receipts.jsonl
```

Supported control-history modes are exactly:

```text
single-repo
split-control
local-only
```

- `single-repo`: current project-owned Planning state may be tracked by product
  Git; no separate control Git is required.
- `split-control`: product Git ignores `.planning`; `.planning` is the control
  work tree; its `.git` is a gitfile pointing to external metadata under home.
- `local-only`: product Git ignores `.planning`; no control Git is required.

`.agents` remains managed/reproducible and need not be tracked by control Git.

## 4. Exact project-policy contract

Do not add `PROJECT_POLICY.yml`, `POLICY.yml`, or another policy subsystem.

Extend the effective configuration with one namespaced block:

```yaml
project_policy:
  schema_version: 1
  project_id: null
  planning_root: .planning
  agents_root: .agents
  control_history_mode: null
  language: null
  intermediate_data_policy: project_defined
  secret_storage: prohibited
  forbidden_read_paths: []
  product_commit:
    planning_vocabulary_required: false
  public_changelog:
    mode: optional
  telemetry:
    enabled: false
```

Contract rules:

- defaults live in managed `framework/defaults.yml`;
- project-specific values live in project-owned `CONFIG.yml`;
- `project_id` and `control_history_mode` are required for registration,
  split-control, and telemetry operations; both may remain `null` for backward
  compatibility before explicit registration;
- non-null `control_history_mode` is exactly `single-repo`, `split-control`, or
  `local-only`; legacy `null` keeps today's update-mode detection and does not
  assert a false history mode;
- roots are normalized repository-relative paths and may not escape the product
  root; `planning_root` and `agents_root` may not overlap;
- host-local absolute `project_root`, external `control_git_dir`, and telemetry
  storage path belong in the home registry, not portable `CONFIG.yml`;
- `secret_storage: prohibited` is the only `05-C` secret policy; no vault or
  secret scanner is introduced;
- `forbidden_read_paths` affects new `05-C` scans/inspection only; it does not
  claim complete host-enforced access control;
- durable prose conventions remain in `PROJECT_RULES.md` or
  `PROJECT_INSTRUCTIONS.md`;
- policy never lives in `ACTIVE`, Change, tasks, progress, handoff, receipts, or
  memory.

## 5. Exact home and registry contract

### 5.1 Home resolution

Resolution order is exactly:

```text
explicit --home
→ PLANNING_LITE_HOME
→ existing Path.home()/.config/planning-lite
```

The existing template-source precedence remains separate and unchanged unless
the explicit update-source repair in §9 is being exercised.

### 5.2 Registry schema

`<home>/projects.yml` has one schema and contains topology/locators only:

```yaml
schema_version: 1
projects:
  - project_id: poker
    project_root: D:/documents/poker
    planning_root: D:/documents/poker/.planning
    agents_root: D:/documents/poker/.agents
    control_history:
      mode: split-control
      git_dir: C:/.../.config/planning-lite/control/poker.git
    project_status: paused
    installed_ref_source: D:/documents/poker/.copier-answers.planning-lite.yml
    lifecycle_source: D:/documents/poker/.planning/ACTIVE.md
    recommendation_index_source: D:/documents/poker/.planning/recommendations/INDEX.md
    telemetry:
      enabled: true
      receipt_path: C:/.../.config/planning-lite/telemetry/poker/run-receipts.jsonl
```

Allowed `project_status` values are `active`, `paused`, and `archived`. This is
portfolio/enrollment status, not a copy of Change lifecycle status.

Registry invariants:

- one `project_id` maps to one normalized product root;
- one normalized product root maps to one `project_id`;
- duplicate/conflicting registration fails closed;
- paths are absolute, normalized, and cannot point inside another registered
  project's control Git directory;
- split `git_dir` is outside the product root and Planning root;
- installed ref and live lifecycle are read from their source files during
  inspection; cached copies are not competing truth;
- registration does not copy project documents, recommendations, Changes, or
  telemetry into the registry;
- writes use a temporary sibling plus atomic replace;
- unknown schema versions fail closed;
- no recursive multi-project scan is added.

### 5.3 Required commands

Add these flat distribution CLI commands:

```text
planning-lite control-init TARGET --project-id ID [--home PATH] [--dry-run]
planning-lite register TARGET --mode MODE --status STATUS [--telemetry] [--home PATH] [--dry-run]
planning-lite projects [--home PATH] [--json]
planning-lite inspect TARGET [--home PATH] [--json]
planning-lite receipt TARGET --input RECEIPT.json [--home PATH]
```

Rules:

- `control-init` creates only split-control topology; it never stages, commits,
  pushes, or changes product `.gitignore`;
- `--dry-run` writes nothing and prints exact proposed paths/actions;
- `register --mode split-control` requires a valid control gitfile/repository
  already created by `control-init`;
- `register` records `project_id` and the explicit mode in `CONFIG.yml` for all
  modes; for `single-repo`/`local-only` it creates no Git metadata;
- repeated identical operations are idempotent;
- a conflicting repeat fails before mutation;
- `projects` and `inspect` are read-only;
- `receipt` is append-only and never invokes a model/runtime itself.

## 6. Exact product/control Git contract

### 6.1 Split-control creation

`control-init` must:

1. validate explicit product root and existing `.planning` root;
2. require outer product Git to ignore `.planning`;
3. refuse if `.planning/.git` already exists but does not match the requested
   external Git directory;
4. choose `<home>/control/<project-id>.git` by default;
5. refuse any external Git directory inside product or Planning roots;
6. create a Git repository with work tree exactly `<product>/.planning` and a
   `.planning/.git` gitfile pointing to the external Git directory;
7. create a deterministic `.planning/.gitignore` from the
   `.planning/**` entries classified `project_owned` by `OWNERSHIP.yml`, while
   excluding `.git` itself and ignoring managed/reproducible bulk;
8. add only `project_id` and `control_history_mode: split-control` to the
   `project_policy` override, preserving all existing config content;
9. leave staging and the initial control commit to the operator;
10. leave product HEAD/index/work-tree bytes unchanged except the separately
    authorized config/topology files that product Git already ignores.

If deterministic generation from ownership cannot express the allow-list
without tracking managed files or hiding project-owned files, stop for design
amendment; do not hand-maintain a second ownership list.

### 6.2 Explicit Git contexts

The implementation must expose two unambiguous helpers:

```text
product_git(project_root, ...)
  → git -C <project_root> ...

control_git(planning_root, git_dir, ...)
  → git --git-dir <git_dir> --work-tree <planning_root> ...
```

No consumer operation may select either repository from ambient cwd.

Product cleanliness never proves control cleanliness. Control cleanliness never
proves product cleanliness. Doctor/inspect output must label both independently.

### 6.3 Update/scan compatibility

- local-only/split updates must never descend into any `.git` directory;
- `.planning/.git` gitfile and `.planning/.gitignore` are topology metadata and
  must be preserved unless an explicit topology command owns the change;
- target scanning must be bounded to governed template paths plus explicit
  metadata, not the entire product repository;
- symlink/reparse-point escape from product/Planning roots fails closed;
- ordinary Copier behavior remains the owner of `single-repo` tracked updates;
- project-owned byte-preservation remains unchanged;
- update performs no Git commit in either history.

### 6.4 Product history vocabulary

Default product commit policy is:

```text
Planning Lite IDs required in product commit subject: false
```

Change `progress.md` and `review.md` must gain explicit aggregate fields:

```text
Product commit SHA(s): []
Control commit SHA(s): []
Public changelog Planning ref: null
```

The Change remains the authoritative mapping from Planning work to product
SHAs. Product `CHANGELOG.md` may include `Planning ref: CHG-XXXX`; it is never a
generated control-history dump. No commit hook or commit-message validator is
added.

## 7. Exact telemetry baseline contract

### 7.1 Storage and collector boundary

Store one append-only stream per registered project:

```text
<home>/telemetry/<project-id>/run-receipts.jsonl
```

Planning Lite validates and records externally supplied facts. It does not call
models, inspect private reasoning, scrape host logs, estimate token values, or
instrument every file read.

### 7.2 RunReceipt v1

Every JSON line contains exactly this shape; nullable fields must be present:

```json
{
  "schema_version": 1,
  "receipt_id": "runtime-unique-id",
  "occurred_at_utc": "2026-09-03T00:00:00Z",
  "project_id": "poker",
  "planning_lite_ref": "vX.Y.Z",
  "change_id": null,
  "task_id": null,
  "run_family": null,
  "agent_role": null,
  "model_id": null,
  "model_tier": null,
  "invocation_index": null,
  "outcome": "UNKNOWN",
  "tokens": {
    "input": null,
    "output": null,
    "cached": null,
    "reasoning": null,
    "total": null,
    "source": "unavailable"
  },
  "verifier_used": null,
  "reviewer_used": null,
  "model_escalation": null,
  "retry": null,
  "recheck": null,
  "reads": {
    "planning": null,
    "non_planning": null,
    "source": "unavailable"
  },
  "runtime_source": null
}
```

Allowed `outcome` values:

```text
PASS
FAIL
BLOCKED
CANCELLED
UNKNOWN
```

Receipt invariants:

- `project_id` must match the registered target;
- `planning_lite_ref` is taken from the consumer answers file by the collector,
  not trusted from input;
- exact unknown values remain JSON `null`;
- `tokens.source` and `reads.source` are `external_runtime`, `operator`, or
  `unavailable`;
- non-null counts are non-negative integers;
- when all component token categories are supplied and runtime semantics make
  them additive, declared total must be consistent; otherwise no derived total
  is invented;
- `agent_role`, `model_id`, and `model_tier` are opaque externally supplied
  identities; adapter names must not be substituted for model identities;
- one receipt represents one invocation; invocation counts are deterministic
  counts of receipts grouped by project/change/task/family/role/model, never an
  estimated field;
- duplicate `receipt_id` with identical bytes is idempotent; conflicting reuse
  fails closed;
- append is serialized safely and a partial final line is treated as corruption;
- telemetry disabled in effective policy causes `receipt` to fail without write;
- no receipt changes lifecycle, recommendation, policy, routing, or authority.

### 7.3 Relationship to existing observability/Campaign

- preserve `.planning/observability/SKILL_USAGE.csv` unchanged;
- do not migrate or duplicate it automatically;
- do not refactor Campaign manifests/journals into generic project state;
- reuse only small proven serialization/hash/timestamp patterns when doing so
  reduces code without importing Campaign semantics;
- Campaign may become one future external producer of RunReceipt, but no adapter
  is required in `05-C`.

## 8. Expected files/modules to modify

The Definition/Plan may reduce this list when an existing owner can absorb the
behavior, but may not introduce additional architectural surfaces without an
amendment.

### Python distribution

```text
src/planning_lite/cli.py                         MODIFY
src/planning_lite/local_update.py                MODIFY
src/planning_lite/workspace.py                   ADD
src/planning_lite/telemetry.py                   ADD
```

`workspace.py` owns home resolution, policy loading/validation, registry,
explicit Git contexts, split-control topology, and live project inspection.
`telemetry.py` owns RunReceipt validation and append-only storage. Do not add a
larger package tree unless Formal Readiness proves these two modules are
materially incoherent.

### Template/control surfaces

```text
template/.planning/framework/defaults.yml        MODIFY
template/.planning/framework/OWNERSHIP.yml       MODIFY only if topology metadata classification requires it
template/.planning/control/CONFIG_RESOLUTION.md  MODIFY
template/.planning/control/STATE_OWNERSHIP.md    MODIFY
template/.planning/control/GIT_CHANGE_REVIEW.md  MODIFY
template/.planning/control/PROJECT_BOOTSTRAP.md  MODIFY only for policy initialization guidance
template/.planning/project/PROJECT_INSTRUCTIONS.md MODIFY
template/.planning/templates/project/PROJECT_INSTRUCTIONS.md MODIFY in lockstep
template/.planning/changes/templates/progress.md MODIFY
template/.planning/changes/templates/review.md   MODIFY
template/.planning/docs/ARCHITECTURE.md          MODIFY
template/.planning/docs/MANIFEST_V4.md           MODIFY
template/.planning/framework/SHA256SUMS.txt      REGENERATE canonically
copier.yml                                       MODIFY only if a new project-owned topology metadata path is classified
```

Do not add a project policy file. `.planning/.git` and `.planning/.gitignore`
are runtime topology outputs of the explicit command, not centrally overwritten
semantic project state.

### Central docs/release notes

```text
docs/ARCHITECTURE.ru.md                           MODIFY
docs/UPDATABLE_INSTALLATION.ru.md                 MODIFY
docs/OPERATOR_WORKFLOW.ru.md                      MODIFY
CHANGELOG.md                                      MODIFY under ## Unreleased
```

### Tests

```text
tests/test_workspace_registry.py                  ADD
tests/test_split_control_history.py               ADD
tests/test_run_receipts.py                        ADD
tests/test_cli.py                                 MODIFY
tests/test_local_only_update.py                   MODIFY
tests/test_template_source.py                     MODIFY if update source rebind changes precedence
tests/test_template.py                            MODIFY if template contract changes
tests/test_versioning.py                          MODIFY only for a new version-source invariant
```

Prefer these owner tests over duplicative prose-literal assertions.

## 9. Update-source repair

`check` and `update` must accept `--template-source` so a consumer whose answers
file points to an unavailable/stale local source can be deliberately rebound.

Resolution for update is:

```text
explicit --template-source
→ existing answers _src_path
```

When the answers source is absent/unusable and no explicit override is given,
fail closed with guidance; do not silently change a consumer's source.

For initial install/adopt, preserve the current tested precedence:

```text
explicit override
→ PLANNING_LITE_TEMPLATE
→ nearby central checkout
→ user config
→ official fallback
```

An explicit successful rebind must cause the rendered installer metadata to
record the selected source. Update the source-precedence tests whenever this
behavior changes.

## 10. Task decomposition

| Task | Outcome | Slice | Blocking edge | Verification seam |
|---|---|---|---|---|
| T-01 | Freeze policy/home/registry/RunReceipt v1 contracts in approved Change artifacts | Tracer | owner boundary approval | completeness/determinacy review |
| T-02 | Add home resolution, effective project-policy loader, registry and read-only inspection | Tracer | T-01 | focused registry/path/schema tests |
| T-03 | Add explicit product/control Git contexts and split-control dry-run/apply | Tracer | T-02 | real temporary dual-Git test, gitfile externality, idempotence |
| T-04 | Make local update and Doctor topology-aware; add update source rebind | Expand-contract | T-03 | local-only + tracked + split tests; source precedence |
| T-05 | Extend existing config/state/Git-review/Change templates and integrity metadata | Tracer | T-01 | semantic owner tests + manifest/canonical-LF SHA verification |
| T-06 | Add raw RunReceipt validation/collector and CLI | Tracer | T-02 | null/provenance/idempotence/corruption/disabled tests |
| T-07 | Prove Poker brownfield migration on a disposable byte snapshot | Acceptance | T-03–T-06 + committed central candidate | project-owned hashes, dual Git, Doctor, update idempotence |
| T-08 | Prove mood unborn/early-adoption migration on a disposable byte snapshot | Acceptance | T-03–T-06 + committed central candidate | no product HEAD assumption, source rebind, history separation, Doctor |
| T-09 | Central completion verification and ownership/scope review | Gate | T-01–T-08 | `uv sync`, focused tests, full tests, adopt/update smokes |

No task may modify the live Poker or mood directory.

## 11. Acceptance criteria

### AC-01 — Authority and scope

- no Roadmap phase is added;
- `05-C` remains a bounded contribution under `PL-V39-05`;
- `06/07/08` ownership is unchanged;
- no live consumer is mutated.

### AC-02 — Policy reuse

- effective policy resolves from existing defaults + `CONFIG.yml`;
- no new policy artifact exists;
- policy is separate from lifecycle/history/memory;
- old consumers with `{}` config retain current legacy mode detection and
  telemetry disabled until explicitly registered/migrated.

### AC-03 — Registry

- duplicate IDs/roots and path overlap fail closed;
- registry writes are atomic and idempotent;
- inspection reads installed ref and lifecycle from live authority paths;
- registry contains no copied semantic project history.

### AC-04 — Product/control Git

- split mode uses external metadata plus `.planning/.git` gitfile;
- product and control HEAD/status are independently addressable;
- product Git need not track `.planning/**`;
- update/Doctor do not mistake one repository for the other;
- no command commits, pushes, tags, merges, rebases, resets, or cleans;
- nested Git metadata is not recursively scanned.

### AC-05 — Product history

- ordinary product commit subjects are accepted without Planning vocabulary;
- Change artifacts can record zero/one/many product and control SHAs;
- changelog Planning reference remains optional;
- no Git hook or automatic changelog generation is added.

### AC-06 — Telemetry baseline

- every required RunReceipt field is present and nullable where defined;
- unavailable exact values stay `null` with an explicit source;
- no model identity is inferred from agent adapter;
- invocation count is derived only from recorded invocation receipts;
- disabled telemetry writes nothing;
- the collector performs no model call and no lifecycle transition;
- Campaign behavior remains backward compatible.

### AC-07 — Update compatibility

- tracked, local-only, and split-control consumers select the correct path;
- a v4.2.0/current update regression still preserves project-owned bytes;
- topology metadata survives repeated updates;
- explicit update source rebind works and no silent rebind occurs;
- second preview/apply is idempotent.

### AC-08 — Security boundary

- registry/receipt schemas contain no secret fields, fixtures contain no
  secrets, and docs state that control Git is not a secret store;
- external Git directory cannot overlap consumer roots;
- new scanners honor explicit root boundaries and do not traverse `.git`;
- no claim of complete access-control enforcement is made.

## 12. Poker migration criteria

### Current audited baseline

```text
root: D:/documents/poker
product HEAD: f7b1db0ebd6db936450d49ce177caf0e8f37bf4c
branch: planning/continuation-baseline
product dirt: handoffs/<HEAD>/handoff.json (untracked)
installed ref: v4.3.0-45-gc9deee6
mode: ignored .planning + ignored .agents / local-only
active Change: CHG-0009-bayesian-study-harness
lifecycle: Verification / Ready
implementation authorized: No
```

Disposable proof must pass before any live request:

1. capture byte hashes of every existing project-owned `.planning` file;
2. preserve `ACTIVE` and `CHG-0009` lifecycle exactly;
3. initialize external control Git in a temporary home with `.planning` as work
   tree and prove the gitfile points outside Poker;
4. prove product status does not start reporting `.planning`;
5. create an operator-controlled initial control commit in the fixture only;
6. register Poker as `paused` and inspect live installed/lifecycle sources;
7. preview and apply update to the exact committed `05-C` candidate/tag through
   the local-only/split path;
8. prove all pre-existing project-owned hashes unchanged except explicitly
   approved `CONFIG.yml` topology keys and generated topology metadata;
9. run consumer Doctor and second idempotence pass;
10. record one all-null/unavailable telemetry receipt only in the temporary home
    and prove no consumer lifecycle change.

Live migration stop gates:

- explicit owner migration authorization is required;
- the untracked handoff must be adjudicated first; do not bypass it merely with
  `--allow-dirty`;
- no automatic CHG-0009 close/archive/verdict/reopen;
- no product commit, control commit, release, or push without separate approval.

## 13. mood migration criteria

### Current audited baseline

```text
root: D:/documents/mood
product HEAD: none (unborn Git repository)
branch: master
product tree: entirely untracked baseline
installed ref: v4.3.0-30-g1a027a6
answers source: D:/documents/planning-lite-validated-1a027a
current ignore intent: managed Planning files ignored; project-owned Planning paths exposed
active Change: CHG-0001-repository-baseline-preparation
lifecycle: Execution / Complete; awaiting owner decision
implementation authorized: No
```

Disposable proof must pass before any live request:

1. reproduce the unborn repository and exact selective-ignore shape;
2. hash all project-owned Planning files;
3. prove `control-init` fails until outer product `.gitignore` unambiguously
   ignores `.planning` for split mode;
4. in the fixture only, apply the intended full `.planning` product-ignore
   policy and initialize external control Git;
5. prove the first control commit can capture project-owned Planning history
   while the first product commit excludes `.planning`;
6. use explicit `--template-source` to rebind from the old local snapshot to the
   official/exact committed `05-C` source;
7. preview/apply update, preserve project-owned hashes except approved policy
   keys/topology metadata, and run Doctor;
8. register mood as `paused`; prove live lifecycle/ref inspection;
9. prove repeated control-init/register/update is idempotent;
10. prove no Change closure, staging, product commit, or control commit is done
    by Planning Lite commands.

Live migration requires a separate owner decision covering:

- whether mood uses `split-control` rather than its earlier selective
  single-repo proposal;
- the outer `.gitignore` change;
- initial product/control commit ordering;
- the source rebind;
- any repair of blank `AGENT_PROFILE.yml` identity.

## 14. Verification requirements

Use the smallest evidence stack per task, then the full completion gate.

### Focused owner tests

```text
uv run --frozen pytest -q tests/test_workspace_registry.py
uv run --frozen pytest -q tests/test_split_control_history.py
uv run --frozen pytest -q tests/test_run_receipts.py
uv run --frozen pytest -q tests/test_local_only_update.py tests/test_template_source.py tests/test_cli.py
```

Tests must inspect structures/files/Git identities directly. Do not assert CLI
help wording or parse human error rendering as machine state.

### Central completion gate

Before declaring the framework Change complete:

```text
uv sync
uv run pytest
uv run python scripts/test_template_update.py
uv run python scripts/test_local_only_update.py
```

Additionally:

1. adopt the template into a temporary clean Git repository and run
   `planning-lite doctor` there;
2. test update from the last applicable release tag to the committed `05-C`
   candidate/tag;
3. verify all project-owned files remain byte-identical unless the fixture
   explicitly authorized policy initialization;
4. run a real temporary external-gitdir/gitfile split-control test;
5. prove independent product/control dirt and HEAD reporting;
6. run disposable Poker and mood snapshot migrations;
7. verify MANIFEST count, ownership classification, and canonical-LF SHA
   receipts directly;
8. confirm working-tree changes match the approved file surface.

Consumer/update smokes whose source identity depends on Git metadata must run
from a clean committed central source. Do not treat a dirty working source as a
release-like update fixture.

### Verifier independence

Formal Readiness and completion review must be performed as independent review
passes. The verifier must distinguish:

```text
product defect
verifier defect
consumer precondition failure
external runtime capability unavailable
```

No missing runtime metric may be converted into zero or guessed identity.

## 15. Explicitly forbidden files/responsibilities

The `05-C` product implementation must not modify or introduce semantics in:

```text
docs/design/project-spine/roadmap/ROADMAP.md
docs/design/project-spine/roadmap/archive/**
docs/design/project-spine/recommendations/archive/**
.planning-lab/**
live D:/documents/poker/**
live D:/documents/mood/**
```

Normal central lifecycle records under `docs/design/project-spine/checkpoints/`
and the top Resume Contract in `CURRENT.md` may change only through the
separately approved Change activation/progress/closure workflow. They are not
product implementation surfaces.

Forbidden responsibilities:

- memory/knowledge retrieval or semantic project aggregation;
- model selection, model-tier routing, escalation policy, or agent scheduling;
- task/verifier baseline checklist implementation;
- Pre-Readiness Closure Completeness logic;
- governed exception, failure-separation, attempt-lifecycle, preflight,
  nominal-type, operational-admissibility, authority-rollover, or
  diagnostic-escalation policy;
- analytics, dashboards, scoring, eval judgment, recommendations from metrics;
- automatic recommendation copying/dedup/absorption across consumers;
- daemon, service, database, remote sync, backup, or hosting;
- secret management/vault/scanning subsystem;
- automatic Git add/commit/tag/push/merge/rebase/reset/clean/stash;
- automatic product `.gitignore` edits;
- universal migration framework;
- Copier tasks/migrations or `--trust` unless a separately reviewed amendment
  documents the security reason.

## 16. Stop conditions

Stop and request adjudication/amendment if any of the following occurs:

1. implementation requires a new major Roadmap phase or changes `06/07/08`
   ownership;
2. the untracked alternative `05-C` Roadmap snapshot is promoted to authority
   without reconciling the identity collision;
3. pre-existing central dirt overlaps a planned output and has not been
   adjudicated;
4. a new project policy file/database is required instead of extending current
   config;
5. split-control safety requires Copier `--trust`, automatic product ignore
   edits, or automatic commits;
6. `.planning/.git` cannot be excluded from scans or external gitdir overlap
   cannot be prevented;
7. preserving current project-owned bytes conflicts with topology creation;
8. generic receipts require Campaign semantics, a daemon, or automatic host
   instrumentation;
9. a required model/token/read value is unavailable and implementation would
   need to infer it;
10. Poker or mood migration needs a consumer lifecycle transition rather than
    a topology/update operation;
11. mood's unborn baseline cannot be made recoverable before its first product
    commit;
12. a product/control history behavior lacks a focused temporary-repository
    acceptance proof;
13. source-version metadata remains inconsistent after `uv sync` and clean
    committed verification.

## 17. Authorization boundaries

This contract authorizes only future planning/readiness after explicit owner
acceptance. It does not authorize any current mutation beyond preparation of
the two requested read-only design outputs.

Separate authorizations are required for:

```text
central Change Definition acceptance
central Plan acceptance
central Execution
live Poker migration
live mood migration
central release/tag
any product/control commit
push/merge
```

## 18. Completion boundary and next major step

`05-C` implementation is complete only when AC-01 through AC-08, T-01 through
T-09, central verification, and both disposable consumer proofs pass with no
unresolved material product defect.

Completion does not itself close the Change or release a version. After
separately authorized closure and release, consumer migrations remain separate
owner-gated operations.

Once `05-C` is closed, the next major Roadmap step remains:

```text
PL-V39-06
Context / Memory / Handoffs
```

Registry and receipts may supply project identity and raw facts to that later
work, but must never become a second semantic memory authority.

```text
Implementation contract: READY FOR OWNER BOUNDARY REVIEW
Implementation authorized: NO
Live migrations authorized: NO
Release authorized: NO
```
