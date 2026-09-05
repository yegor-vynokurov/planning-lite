# CHG-PL-V39-06-CONTEXT-MEMORY-HANDOFF-001 — Implementation Plan v1

- Status: `APPROVED BY OWNER`
- Date: `2026-09-05`
- Change: `CHG-PL-V39-06-CONTEXT-MEMORY-HANDOFF-001`
- Definition: `APPROVED BY OWNER`
- Definition artifact: `docs/design/project-spine/checkpoints/PL-V39-06-CONTEXT-MEMORY-HANDOFF-CHANGE-DEFINITION-v1.md`
- Activation artifact: `docs/design/project-spine/checkpoints/PL-V39-06-DEFINITION-ACTIVATION-v1.md`
- Planning baseline HEAD: `7e8a3796b4722f98ab1dacb0a2bd67e168704b51`
- Plan approval: `YES / USER EXPLICIT / 2026-09-05`
- Formal Readiness: `NOT RUN`
- Implementation authorization: `NO`
- Live Poker/mood migration: `NOT REQUIRED / NOT AUTHORIZED`

## 1. Plan Identity and Authority

This Plan derives only the smallest implementation needed to prove the nine
approved acceptance criteria. Authority is, in descending order:

1. the approved Change Definition;
2. the Definition Activation and canonical `CURRENT.md` Resume Contract;
3. `PL-V39-06-AUTHORITY-AND-SCOPE-BINDING-v1.md` as shaping evidence;
4. closed 05-C artifacts only for already-proven registry, safe-read, Git
   identity, RunReceipt, and disposable-consumer seams.

The preflight working tree contains only the expected PL-V39-06 governance
state: modified `CURRENT.md` and the untracked Authority Binding, approved
Definition, and activation artifact. No source, test, template, Poker, mood, or
unrelated change was present.

The owner approved this tightened Plan and chose one governance-only checkpoint
commit to freeze the planning authority before Formal Readiness. This is a
Change-local sequencing decision, not a universal claim that Formal Readiness
always requires a prior clean commit and not a revival of the rejected 05-C
verifier rule. The two identities are distinct:

```text
PLANNING_AUTHORITY_CHECKPOINT
!=
CENTRAL_IMPLEMENTATION_CANDIDATE

approved governance checkpoint (this gate)
→ T-01…T-06 implementation after later authorization
→ central implementation candidate (later separate commit)
```

The Central Candidate Gate still requires a later clean committed
implementation candidate only before T-07/T-08 and only after T-01…T-06 PASS.

Owner decision recorded by this governance step:

```text
OWNER_PLAN_DECISION: APPROVE
Formal Readiness: NOT RUN
implementation_authorized: NO
```

This approval does not start Formal Readiness or authorize implementation,
consumer proofs, migration, or any later implementation checkpoint/release
operation.

## 2. Frozen Scope and Invariants

The implementation must preserve this authority topology:

```text
CURRENT.md / consumer ACTIVE.md
= compact current-state authority

Change / Plan / Ledger / Review
= canonical lifecycle and evidence

consumer-owned .planning
= consumer authority for the facts it owns

ResumeContext / ContextBootstrapCapsule / ContextTrace / AgentWorkPacket / Handoff
= subordinate derived or transition views
```

Frozen invariants:

1. No `.memory/`, `.context/`, `.snapshots/`, persistent ContextTrace or capsule
   registry, database, vector store, second current-state file, or new authority.
2. Derived outputs are emitted to stdout or returned as in-memory values. The
   implementation does not persist them.
3. A supplied handoff is never current-state authority. Current authority is
   re-read and freshness is checked before the handoff can inform output.
4. Relevance expansion is exact path/heading and lineage selection, never
   semantic retrieval, embeddings, vector search, or RAG.
5. An absent active Change and absent blocker are valid states. The
   implementation must not synthesize either.
6. Raw `recommendations/inbox/**` remains `LOCAL_OPERATIONAL`, noncanonical,
   locally Git-excluded, and ineligible for automatic selection or promotion.
7. Live Poker/mood migration, a final control-home placement, skills,
   checklists, routing, orchestration, evaluation, learning, and PromptOps are
   outside this Plan.

## 3. Minimal Implementation Architecture

### 3.1 One read-only resume seam

Add one product command:

```text
planning-lite resume TARGET [--include PATH[#HEADING]]...
                            [--handoff INPUT.json]
                            [--json]
```

It reads an existing consumer project and emits a derived bounded resume view.
It performs no registration, migration, control-Git creation, receipt append,
template update, or project write. `TARGET` need not be registered, so an early
or unborn consumer has no Planning Lite home dependency.

The implementation is split only where responsibility is already distinct:

| Seam | Responsibility |
|---|---|
| `src/planning_lite/context.py` | Immutable value contracts, Markdown field/section parsing, storage classification, deterministic selection, freshness/handoff validation, and ContextTrace metrics |
| `src/planning_lite/workspace.py` | Reuse/expose existing root containment, forbidden-read, effective-policy, and product Git identity primitives; no semantic state ownership |
| `src/planning_lite/cli.py` | Parse the single `resume` command and render deterministic YAML/JSON stdout |

No campaign-specific `ResumeCapsule` or review handoff is generalized. Those
contracts keep their existing domain ownership.

### 3.2 Inputs, selection order, and bounds

Required default inputs are exact existing authorities:

```text
1. TARGET/.planning/ACTIVE.md
2. TARGET/.planning/project/CURRENT_STATE.md
3. the Active context packet path, only when ACTIVE names one for an active Change
```

Project identity resolves from effective `project_policy.project_id`, then the
resolved target directory name when no ID is configured. Product Git identity
is observed through the existing explicit product-root seam and represents a
commit SHA or `UNBORN`, branch/detached state, and clean/dirty/unavailable state.
It is evidence, not lifecycle authority.

The selection order is fixed:

```text
authority identity and exact pointers
→ ACTIVE compact current state
→ CURRENT_STATE preamble/current-state pointer
→ active context packet fields when applicable
→ up to five explicit exact lineage expansions
```

Structural bounds:

- default selected artifacts: maximum `3`;
- explicit expansions: maximum `5`; total selected artifacts: maximum `8`;
- `CURRENT_STATE.md`: only the preamble before the first level-2 heading,
  maximum `12` bullet items and `8,192` characters;
- active `context.md`: only the existing named top-level packet fields,
  maximum `12` fields and `16,384` characters total;
- an explicit selector is `repo-relative-path` for identity/hash only or
  `repo-relative-path#exact-heading` for one Markdown section;
- one expanded section is limited to `4,096` characters; oversize content is
  not truncated and returns a safe `EXPANSION_TOO_LARGE` result with its path;
- paths must remain under the resolved product root, must not traverse `.git`,
  and must pass effective `forbidden_read_paths` checks.

Default selection never scans completed Changes, ledgers, recommendations,
archives, or raw logs. Exact expansion paths under `.planning/project/**`,
`.planning/changes/active/**`, `.planning/changes/completed/**`, and
`.planning/decisions/**` are eligible. `recommendations/inbox/**`, `.git/**`,
and paths outside the product root are always rejected. No glob, similarity,
keyword, or recency search exists.

### 3.3 Derived representations

| Representation | Runtime form | Persistent? | Class / authority |
|---|---|---|---|
| `ResumeContextV1` | Immutable mapping/model returned by API and stdout | `NO` | `RECONSTRUCTABLE`; subordinate to referenced sources |
| `ContextBootstrapCapsuleV1` | Compact identity/gate/action subset inside `ResumeContextV1` | `NO` | `RECONSTRUCTABLE`; not authority |
| `ContextTraceV1` | Selected/excluded source identities, reasons, bounds, and structural metrics | `NO` | `RECONSTRUCTABLE`; selection evidence only |
| `AgentWorkPacket` | Logical task-specific consumer projection | `NO` | `EPHEMERAL`; no standalone PL-V39-06 model or compiler |
| `HandoffV1` | Optional externally supplied JSON validated in memory | `NO` by this implementation | `RECONSTRUCTABLE` transition input; only an existing later lifecycle may retain a copy as `TRACKED_EVIDENCE_HISTORY` |

`ResumeContextV1` has one exact top-level schema:

```text
schema_version
status
project_identity
git_identity
current_state
bootstrap
selected_sources
handoff
context_trace
```

`bootstrap` contains only:

```text
project_id
active_change | null
last_completed_or_next_pointer | null
lifecycle_stage
stage_status
implementation_authorized
open_blocker | null
next_permitted_action
active_context_path | null
source_revision
```

`ACTIVE.md` labels are parsed from the existing fields: Change, Lifecycle stage,
Stage status, Implementation authorized, Blocking decision, Next permitted
action, Active context packet, and Last verified checkpoint. Change and blocker
may be explicit `None`; lifecycle/authorization/next-action are required. A
missing required current field yields `MISSING_REQUIRED_CURRENT_STATE` and does
not invent a value.

### 3.4 Storage-class and authority resolution

The classifier uses exact known roles/paths, not content similarity:

| Surface | Class | Selection rule |
|---|---|---|
| `ACTIVE.md`, `CURRENT_STATE.md`, approved active Definition/Plan | `TRACKED_CANONICAL` | Current facts load first according to their owning role |
| Ledger/progress, Completion Review/review, completed Changes, accepted decisions | `TRACKED_EVIDENCE_HISTORY` | Pointer by default; exact bounded expansion only |
| `recommendations/inbox/**`, local raw operational intake | `LOCAL_OPERATIONAL` | Never selected as canonical memory; no promotion |
| Resume/bootstrap/trace output | `RECONSTRUCTABLE` | Regenerated from sources; never persisted by command |
| AgentWorkPacket and unretained handoff input | `EPHEMERAL` | Current invocation only |

Tracking state alone never grants authority. A project-owned file keeps the
role defined by `STATE_OWNERSHIP.md`; a local/untracked Git state is reported
without being upgraded or rejected solely for being uncommitted.

### 3.5 Freshness, missing, and supersession

Every selected source reference contains normalized repo-relative path and
SHA-256 of the exact bytes read. The output also records product Git identity
and the governing ACTIVE tuple:

```text
(active_change, lifecycle_stage, stage_status,
 implementation_authorized, next_permitted_action, active_context_path)
```

`validate_resume_context` and optional handoff validation produce exactly:

| Result | Condition | Behavior |
|---|---|---|
| `CURRENT` | Required sources exist, hashes match, and governing ACTIVE tuple matches | Derived output may be used |
| `STALE` | A referenced required source exists but its SHA differs | Preserve current authority, report changed pointer, require regeneration |
| `SUPERSEDED` | Current ACTIVE tuple or active-context pointer identifies a later/different lifecycle state | Discard transition claims; regenerate from current authority |
| `MISSING_OWNER_ARTIFACT` | Required ACTIVE/CURRENT_STATE/declared active context or handoff artifact ref is absent/forbidden | Fail soft with the missing owner path and safe current gate; no inferred action |

An absent active Change or blocker is valid and is not a missing-artifact
condition. An unborn Git repository is valid and recorded as `UNBORN`.

### 3.6 Minimal handoff contract

`HandoffV1` is exact-key, externally supplied input:

```text
schema_version
project_id
change_id | null
changed_paths[]
lifecycle_stage
stage_status
implementation_authorized
verification[] {command, outcome, evidence_pointer | null}
open_blocker | null
accepted_dispositions[] {id, disposition, artifact_pointer | null}
next_permitted_action
artifact_refs[] {path, sha256}
source_revision {head | null, state}
```

Bounds are: at most 64 changed paths, 32 verification entries, 16 dispositions,
and 16 artifact refs; paths are normalized, relative, and contained. Unknown or
missing keys fail closed. `implementation_authorized` must agree with current
authority; the handoff cannot elevate it. Current project/change identity,
ACTIVE tuple, and referenced hashes are resolved before any handoff value is
included. Full Definition/Plan/Ledger/raw-log bodies have no schema field and
therefore cannot be duplicated into the handoff.

### 3.7 ContextTrace and structural efficiency

`ContextTraceV1` records only:

```text
selected[] {path, sha256, role, storage_class, reason, section | null}
excluded_by_default[] {category, reason}
selected_artifact_count
selected_section_count
selected_character_count
explicit_expansion_count
bounds
```

It records no token/model/cost estimate. It is emitted with the resume result
and is not appended to a registry, receipt stream, or project file.
`excluded_by_default` contains the fixed policy categories and reasons only:

```text
completed changes: not loaded by default
full ledgers: not loaded by default
archives: not loaded by default
raw logs: not loaded by default
historical proposals: not loaded by default
```

It is not an inventory of excluded paths. ContextTrace reports the selection
policy and actual selected sources; producing it must not recursively scan or
enumerate history, archives, or completed Changes.

## 4. AC-to-Evidence Matrix

All nine ACs have executable proof. The cumulative Execution Ledger is the
normal durable task evidence; runtime output remains disposable unless a later
existing lifecycle explicitly retains it.

| AC | Implementation seam | Test / nearest-wrong discriminator | Evidence | Task owner |
|---|---|---|---|---|
| AC-01 | ACTIVE/CURRENT_STATE parser and bootstrap model | Fresh fixture resumes from max 3 default sources; no Change/blocker fixture yields nulls, not invented objects | Ledger focused results | T-01, T-03, T-09 |
| AC-02 | Ordered selector and source identities | Permuted filesystem creation order produces byte-equivalent JSON; stage/history cannot outrank ACTIVE | Ledger hashes/results | T-02, T-03 |
| AC-03 | Derived-only output and ownership docs | Command leaves target/home bytes and status unchanged; forbidden second-store path audit | Ledger scope audit | T-03, T-05, T-06 |
| AC-04 | Hash/ACTIVE-tuple validator | Changed hash=`STALE`; changed active tuple=`SUPERSEDED`; absent/forbidden owner path=`MISSING_OWNER_ARTIFACT` | Ledger discriminator table | T-04 |
| AC-05 | Exact `HandoffV1` validator | Extra full-body/log fields rejected; conflicting authorization/identity/hash rejected; current authority wins | Ledger handoff results | T-01, T-04 |
| AC-06 | Exact storage classifier | All five classes covered; inbox path remains local/noncanonical and cannot be selected even explicitly | Ledger classification results | T-02 |
| AC-07 | Two distinct disposable fixtures | Poker-shaped mature and mood-shaped early/unborn tests prove different state/history conditions | Ledger consumer proof sections | T-07, T-08 |
| AC-08 | Bounded exact selector and ContextTrace | Default max 3, total max 8, exact heading only, no glob/search; fixture history skipped and metrics explain selection | Ledger efficiency comparison | T-03, T-06, T-07 |
| AC-09 | Direct-target read-only CLI | Resume works without home/registration/control Git; before/after target and live consumer state unchanged | Ledger scope/consumer proof | T-05, T-07, T-08 |

## 5. Task Graph

```text
Plan owner approval
→ governance-only planning-authority checkpoint commit
→ clean frozen planning baseline
→ read-only Formal Readiness
→ separate bounded Execution authorization
→ T-01 → T-02 → T-03 → T-04 → T-05 → T-06
→ separate owner checkpoint-commit authorization
→ clean committed central candidate
→ separate owner authorization for T-07/T-08
→ T-07 and T-08
→ T-09 Completion Review
→ separate owner closure decision
```

Dependencies:

| Task | Depends on | May run with |
|---|---|---|
| T-01 | Approved Plan, Readiness `READY`, Execution authorization | — |
| T-02 | T-01 | — |
| T-03 | T-02 | — |
| T-04 | T-03 | — |
| T-05 | T-04 | — |
| T-06 | T-05 | — |
| T-07 | T-06 + clean committed candidate + consumer-proof authorization | T-08 after common gate |
| T-08 | T-06 + clean committed candidate + consumer-proof authorization | T-07 after common gate |
| T-09 | T-07 and T-08 PASS | — |

T-01 through T-06 are one sensible central authorization block. T-07/T-08 are
one later disposable-proof block. No owner gate is inserted between ordinary
dependent tasks unless a task hits a stop condition.

## 6. Task Specifications

### T-01 — Contract lock and execution baseline

- Purpose: record exact execution HEAD/status and implement the immutable schema,
  enums, nullability, caps, and validation errors described in Section 3.
- Dependencies: approved Plan, Formal Readiness `READY`, explicit T-01…T-06
  authorization.
- Write surfaces: `src/planning_lite/context.py`,
  `tests/test_context_resume.py`, cumulative Execution Ledger, bounded CURRENT
  task pointer only if the lifecycle requires it.
- Read surfaces: approved Definition/Plan, existing ACTIVE/current/context
  templates, existing Git/path safety helpers.
- ACs: AC-01, AC-05.
- Tests/evidence: exact-key, null Change/blocker, enum/cap, unknown/missing-field,
  and no-full-body-field discriminators; `git diff --check`.
- Stop: any schema needs persistence, semantic retrieval, a second authority,
  or a material Definition choice.

### T-02 — Authority and storage-class resolution

- Purpose: implement exact role/path classification and safe source resolution
  without recursive discovery.
- Dependencies: T-01 PASS.
- Write surfaces: `src/planning_lite/context.py`, narrow public wrappers in
  `src/planning_lite/workspace.py` only for reuse of existing containment,
  forbidden-read, policy, and product-Git seams; focused tests; ledger.
- Read surfaces: `workspace.py`, effective policy, `STATE_OWNERSHIP.md`, 05-C
  proof results.
- ACs: AC-02, AC-06.
- Tests/evidence: all five classes; path escape/symlink/reparse/`.git` rejection;
  raw inbox rejection; tracked/local status cannot alter authority; no broad scan.
- Stop: registry/history content becomes a second semantic source or safe reads
  require changing 05-C topology semantics.

### T-03 — Bounded resume selection and ContextTrace

- Purpose: implement default selection, exact bounded expansion, bootstrap, and
  explainable structural metrics.
- Dependencies: T-02 PASS.
- Write surfaces: `src/planning_lite/context.py`, focused tests, ledger.
- Read surfaces: resolved authority files only.
- ACs: AC-01, AC-02, AC-03, AC-08.
- Tests/evidence: default/total caps, deterministic ordering/JSON, heading-only
  expansion, oversize fail-soft, no history scan, trace reasons/counts/characters,
  target/home no-write guard.
- Stop: meeting the criteria requires tokens, model inference, keyword search,
  semantic scoring, persistence, or unbounded content.

### T-04 — Freshness, stale/missing behavior, and handoff

- Purpose: validate source hashes/ACTIVE tuple and optional exact HandoffV1
  against current authority.
- Dependencies: T-03 PASS.
- Write surfaces: `src/planning_lite/context.py`, focused tests, ledger.
- Read surfaces: selected source paths and optional handoff input only.
- ACs: AC-04, AC-05.
- Tests/evidence: CURRENT/STALE/SUPERSEDED/MISSING_OWNER_ARTIFACT; missing active
  context; valid no-Change/no-blocker; handoff identity/auth/hash conflict;
  anti-duplication extra-field rejection.
- Stop: handoff needs authority precedence over ACTIVE/CURRENT_STATE or a new
  durable handoff repository.

### T-05 — CLI, managed policy, and integrity integration

- Purpose: expose the read-only command and align existing consumer policy and
  context-template wording with the implemented contract.
- Dependencies: T-04 PASS.
- Write surfaces: `src/planning_lite/cli.py`,
  `template/.planning/control/CONTEXT_POLICY.md`,
  `template/.planning/control/STATE_OWNERSHIP.md`,
  `template/.planning/changes/templates/context.md` only as
  `CONDITIONAL_WITHIN_EXISTING_SEMANTICS`,
  `template/.planning/framework/SHA256SUMS.txt`,
  `docs/OPERATOR_WORKFLOW.ru.md`, `CHANGELOG.md` under `## Unreleased`,
  `tests/test_cli.py`, focused tests, ledger.
- Read surfaces: `MANIFEST_V4.md`, `OWNERSHIP.yml`, `copier.yml`, CLI patterns,
  existing template owner tests.
- ACs: AC-03, AC-05, AC-09.
- Tests/evidence: YAML/JSON output, error mapping, no output-file option, no
  target/home mutation, current ownership rules, canonical-LF receipt equality.
- Stop: a new template path, Copier task/migration, ownership classification,
  trust boundary, router, skill, checklist, or control-home change is required.

The existing `context.md` remains an active context packet and lifecycle
surface. It does not become HandoffV1 storage, HandoffV1 schema authority, a
persistent handoff database, parallel `CURRENT`, or parallel project-state
authority. Modify its managed template only if the existing context-packet
semantics independently need bounded wording/alignment for an AC; do not modify
it merely to encode or persist HandoffV1. If Formal Readiness finds no such
independent need, leave it unchanged. No replacement handoff file/tree/store is
permitted.

### T-06 — Focused integration, efficiency proof, and central regression

- Purpose: close the central implementation candidate before consumer proofs.
- Dependencies: T-05 PASS.
- Write surfaces: tests only if an actual defect needs an in-scope correction;
  Execution Ledger and bounded CURRENT status; no new evidence document.
- Read surfaces: all changed paths, relevant owner tests, Git state.
- ACs: AC-01…AC-09 central evidence.
- Tests/evidence: focused context/CLI/template suite; existing registry and
  central resume compatibility; template integrity; structural FULL_HISTORY vs
  BOUNDED_RESUME comparison; full regression once; `git diff --check`; exact
  scope audit.
- Stop: any AC lacks executable evidence, full regression has a material failure,
  or write surface expands beyond Section 7.

### Central Candidate Gate

After T-06 PASS, stop. A separate owner authorization is required to create one
central checkpoint commit. T-07/T-08 require:

```text
all T-01…T-06 evidence PASS
focused and full regression PASS
exact implementation diff reviewed
owner checkpoint-commit authorization
clean committed candidate exists
separate owner disposable-proof authorization
```

No clean-commit prerequisite is moved backward to Formal Readiness or T-01.

### T-07 — Poker-shaped mature consumer proof

- Purpose: prove a mature brownfield resume with deep history, accepted
  decisions, implementation identity, and stale historical material.
- Dependencies: Central Candidate Gate and consumer-proof authorization.
- Write surfaces: disposable temporary fixture only; ledger. Live Poker is
  read-only/non-mutated and is not required at execution.
- Read surfaces: committed central candidate and deterministic Poker-shaped
  fixture.
- ACs: AC-01, AC-02, AC-04, AC-07, AC-08, AC-09.
- Tests/evidence: exact focused node
  `tests/test_context_resume.py::test_poker_shaped_resume_is_bounded_and_excludes_stale_history`;
  invoke installed candidate CLI in a temporary Git project; before/after hashes
  and Git status; selected/skipped structural counts.
- Stop: proof needs live Poker mutation, broad history loading, or noncommitted
  central source identity.

### T-08 — mood-shaped early/unborn consumer proof

- Purpose: prove useful resume for an early/unborn project with no active Change
  and no blocker, while preserving actual baseline state.
- Dependencies: Central Candidate Gate and consumer-proof authorization.
- Write surfaces: disposable temporary fixture only; ledger. Live mood is
  read-only/non-mutated and is not required at execution.
- Read surfaces: committed central candidate and deterministic mood-shaped
  fixture.
- ACs: AC-01, AC-04, AC-07, AC-09.
- Tests/evidence: exact focused node
  `tests/test_context_resume.py::test_mood_shaped_resume_preserves_unborn_no_change_no_blocker`;
  invoke installed candidate CLI without home/registration/control Git;
  before/after bytes/status; null Change/blocker and `UNBORN` assertions.
- Stop: proof invents a Change/blocker/HEAD, needs live mood mutation, or writes
  registration/control state.

### T-09 — Completion Review

- Purpose: reconcile all nine ACs, tasks, gates, regression, consumer proofs,
  scope, and deferred items without closing the Change.
- Dependencies: T-07 and T-08 PASS.
- Write surfaces:
  `docs/design/project-spine/checkpoints/PL-V39-06-COMPLETION-REVIEW-v1.md`,
  final ledger entry, bounded CURRENT completion-review pointer if required.
- Read surfaces: approved Definition/Plan/Readiness, cumulative ledger, candidate
  commit, final diff and Git status.
- ACs: AC-01…AC-09 final reconciliation.
- Tests/evidence: no automatic suite rerun unless evidence is stale; verify exact
  candidate/ledger identities, `git diff --check`, and scope.
- Stop: any task/AC is not PASS, evidence does not bind the reviewed candidate,
  or live consumer state changed.

T-09 creates a review verdict only. Closure remains a separate owner decision.

## 7. Write-Surface Manifest

No path outside this manifest may change without Plan/Definition adjudication.

| Path | Class | Operation | AC reason |
|---|---|---|---|
| `src/planning_lite/context.py` | schema/model + runtime | ADD | AC-01/02/04/05/06/08 core contracts and selection |
| `src/planning_lite/workspace.py` | runtime | MODIFY narrowly | Reuse AC-02/09 root, policy, Git, and forbidden-read seams |
| `src/planning_lite/cli.py` | CLI | MODIFY | Read-only resume entry point for AC-01/07/09 |
| `tests/test_context_resume.py` | tests | ADD | All new focused discriminators and both disposable fixture shapes |
| `tests/test_cli.py` | tests | MODIFY | CLI parsing/rendering/error/no-write contract |
| `template/.planning/control/CONTEXT_POLICY.md` | docs/template | MODIFY | AC-02/03/08 bounded authority-first policy |
| `template/.planning/control/STATE_OWNERSHIP.md` | docs/template | MODIFY | AC-03/05/06 authority/storage ownership |
| `template/.planning/changes/templates/context.md` | docs/template | `CONDITIONAL_WITHIN_EXISTING_SEMANTICS` | Only bounded active-context wording if independently required by AC-03/05; never HandoffV1 storage/schema |
| `template/.planning/framework/SHA256SUMS.txt` | integrity | REGENERATE | Managed-template integrity for changed files |
| `docs/OPERATOR_WORKFLOW.ru.md` | docs | MODIFY | Document read-only resume command and limitations |
| `CHANGELOG.md` | docs/release note | MODIFY under `## Unreleased` | Record user-visible command/contract without release |
| PL-V39-06 Execution Ledger / Completion Review / `CURRENT.md` | canonical governance | CREATE/MODIFY only at named gates | Execution continuity and final review |

Explicitly unchanged/read-only: `copier.yml`, `OWNERSHIP.yml`,
`MANIFEST_V4.md` (no template path is added/removed), defaults/config schema,
registry format, RunReceipt schema, local-update behavior, Doctor, campaign
package, router/modes/skills/checklists, and live consumers.

The only conditional write surface is
`template/.planning/changes/templates/context.md` under the rule above. Formal
Readiness must resolve it as `REQUIRED` or `NOT REQUIRED` before execution. If
any other additional surface is materially required, execution stops for owner
adjudication instead of treating it as implicitly allowed.

## 8. Verification Strategy

### Focused discriminator layer

```text
uv run --frozen pytest -q tests/test_context_resume.py tests/test_cli.py
uv run --frozen pytest -q tests/test_field_control_pack_foundation.py
  tests/test_project_shaping_foundation.py tests/test_direction_foundation.py
  tests/test_roadmap_synthesis_handoff.py
```

Required named discriminators include:

```text
fresh current resume
stale source hash
superseded ACTIVE tuple/context pointer
missing/forbidden owner artifact
no active Change
no blocker
bounded default history exclusion
explicit exact lineage expansion
handoff extra-body and authority-conflict rejection
raw recommendation inbox non-promotion
derived context cannot outrank current authority
path escape/.git/symlink/reparse rejection where applicable
```

### Bounded integration layer

```text
uv run --frozen pytest -q tests/test_context_resume.py tests/test_cli.py
  tests/test_workspace_registry.py tests/test_central_resume_contract.py
```

This layer proves direct-target/no-home behavior, existing workspace safety,
central resume compatibility, deterministic JSON/YAML, and no writes.

### Full regression gate

Run once at T-06 after focused/integration PASS:

```text
uv run --frozen pytest
git diff --check
git status --short --untracked-files=all
git diff --name-status
```

Do not run the full suite after each task. Before declaring framework completion,
the later completion gate must also follow repository-level `uv sync`, clean
temporary adoption, consumer Doctor, and update safety requirements when they
are applicable to the actual changed template surface. Never run Doctor at the
central repository root.

## 9. Consumer Proof Strategy

The two fixture families are deliberately non-equivalent:

| Proof | Fixture facts | Required result |
|---|---|---|
| Poker-shaped | Tracked mature repo, active Change, accepted decision, implementation SHA, many completed Changes/ledgers, stale historical candidate | Maximum 3 default sources; current active/gate/action wins; history/rejected material absent; one exact lineage expansion is explained |
| mood-shaped | Unborn repo, minimal CURRENT_STATE, no active Change, no blocker, no registration/home/control Git | Useful bootstrap with null Change/blocker, `UNBORN`, exact next action, and zero invented lifecycle facts |

Each proof uses a temporary project created by the test and the clean committed
central candidate. Before/after file hashes and Git status prove read-only
behavior. The live repositories at `D:\documents\poker` and
`D:\documents\mood` are not migration targets and need not be opened during
execution.

## 10. Context-Efficiency Proof

The proof uses structure, never inferred token/provider telemetry.

For each fixture, the test separately inventories the known fixture history and
records:

```text
FULL_HISTORY_BASELINE:
  available history artifact count
  available history character/byte size

BOUNDED_RESUME:
  selected artifact count
  selected section count
  selected character count
  explicit expansion count

EXCLUDED_BY_DEFAULT:
  full ledgers
  raw logs
  historical proposals
  rejected hypotheses
  archive bodies
```

Pass requires deterministic repeated output, default selected artifacts `<= 3`,
total selected artifacts `<= 8`, explicit expansions `<= 5`, no excluded body in
the output, and at least one skipped history artifact in the mature fixture.
The test harness, not the runtime selector, inventories the full fixture so the
product command does not perform a history scan merely to report savings.
Runtime `ContextTraceV1.excluded_by_default` reports only the five fixed
categories/reasons and actual selected sources; it never enumerates skipped
artifacts.

## 11. Gates and Authorization

| Gate | Required state | Authority created by this Plan? |
|---|---|---|
| Definition | Already `APPROVED` | No |
| Plan | `APPROVED BY OWNER` | No implementation authority |
| Planning-authority checkpoint | One owner-authorized governance-only commit, then clean baseline | Freezes Definition/Plan/activation/CURRENT only; not an implementation candidate |
| Formal Readiness | Next gate after this Change-local governance checkpoint; read-only | No implementation authority |
| Central execution | Separate owner authorization after `READY` | Bounded T-01…T-06 only |
| Central checkpoint | Separate owner commit authorization after T-06 PASS | One candidate commit only |
| Consumer proofs | Clean committed candidate + separate owner authorization | Disposable T-07/T-08 only |
| Completion Review | T-07/T-08 PASS | Review only; no closure |
| Closure/release | Separate owner decisions | Not authorized here |

Global stop conditions:

- Definition or AC semantics must change;
- a persistent derived store or parallel authority appears necessary;
- semantic retrieval, adaptive scoring, routing, skills, evaluation, or
  orchestration becomes necessary;
- an unlisted source/test/template/runtime path must change;
- current authority cannot be parsed without inventing values;
- safety requires live consumer mutation or control-home placement;
- unexpected pre-existing dirt, a material regression, or consumer drift is
  found.

## 12. Evidence Discipline

T-01 through T-08 use one cumulative existing-lifecycle artifact:

```text
docs/design/project-spine/checkpoints/PL-V39-06-EXECUTION-LEDGER-v1.md
```

Each entry records task ID, baseline/revision when material, actual changed
paths, exact verification/evidence, PASS/FAIL/BLOCKED, and a material finding or
stop gate. No per-task receipt file is created merely because a task ran. A
standalone diagnostic is allowed only when it has independent value or an
existing canonical lifecycle requires it.

T-09 alone creates:

```text
docs/design/project-spine/checkpoints/PL-V39-06-COMPLETION-REVIEW-v1.md
```

Machine output from resume/handoff proofs stays disposable unless an existing
later lifecycle explicitly requires durable evidence.

## 13. Deferred / Routed Items

- PL-V39-07: skills, checklists, execution routing/contracts, and complex
  lifecycle execution refinements.
- PL-V39-08: quality scoring, learning, adaptive context policy, semantic
  relevance evaluation, and PromptOps.
- Later: multi-agent orchestration and production Context Compiler experiments.
- Deferred memory work: embeddings/vector search/RAG, semantic memory
  automation, episodic summary trees, utility/forgetting ledgers, graph stores.
- Deferred recommendation work: discovery, automatic promotion/absorption,
  registry, and routing.
- Separate owner decision: any live Poker/mood migration or final external
  control-home placement.

None is a hidden dependency for AC-01…AC-09.

## 14. Plan-Quality Self-Review

```text
removable/mergeable task without losing an AC: NONE
new persistent authority: NONE
derived artifact persisted without necessity: NO
semantic retrieval introduced: NO
live Poker/mood migration required: NO
PL-V39-07 work imported: NO
PL-V39-08 work imported: NO
ACs with executable proof: 9/9
consumer proofs materially distinct: YES
context reduction measured structurally: YES
owner gates limited to material authority boundaries: YES
```

Nine tasks are the minimum useful graph here: contract, authority resolution,
selection, freshness/handoff, integration surface, central verification, two
distinct consumer discriminators, and completion review. Merging either
consumer proof would hide the mature-versus-early distinction; splitting any
core task further would create receipt-only granularity.

## 15. Completion Conditions and Current Gate

The Change can reach Completion Review only when all nine ACs and T-01…T-08 are
PASS on the exact committed candidate, live Poker/mood are unchanged, the full
regression and integrity gates pass, and the ledger contains no unresolved
material finding.

Current state after this Plan preparation:

```text
Plan: APPROVED BY OWNER
planning authority checkpoint: REQUIRED IN THIS GOVERNANCE STEP
Formal Readiness: NOT RUN
implementation_authorized: NO
T-01…T-09: NOT STARTED
next permitted action after checkpoint: RUN_PL_V39_06_FORMAL_READINESS
```

Owner approval is recorded. After the governance checkpoint is cleanly created,
only read-only Formal Readiness may follow; implementation still requires a
later explicit authorization.
