# PL-V39-05-C — Formal Readiness Verdict

- Document ID: `PL-V39-05-C-FORMAL-READINESS-VERDICT-001`
- Date: `2026-09-03`
- Change: `CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001`
- Definition: approved
- Plan: approved by owner, revision `e93e7e8fa0aa80cdbad5dfb0861460c4f2990495c6313c9d1321929a45e67943`
- Verdict: `READY`
- Implementation authorization: `NO`

## 1. Readiness boundary and method

This is a read-only Formal Readiness pass. It revalidated only the frozen
authority artifacts, current Git/status/hash state, concrete write-surface and
implementation seams, conditional paths, and the planned verification gates.
No broad architecture discovery was repeated. No implementation test, product
test, consumer operation, ledger creation, or lifecycle mutation was performed.

## 2. Exact execution baseline

```text
repository root: D:\documents\planning-lite
branch: reconcile/current-design-spine-2026-08-25
HEAD: a40019209c133785a4babe06b5e96dfd4673c4f5
index: clean
working tree at readiness start: DIRTY(13)
implementation surfaces changed: none
```

The recorded readiness-start baseline is `DIRTY(13)`. After the existing
Readiness artifact was created, this bounded in-place correction leaves the
tree `DIRTY(14)` (the same known Planning/incoming files plus this artifact),
with the same HEAD and no product/runtime/template/test path changed. T-01
must recapture the exact live values instead of inferring either count.

The dirty state is fully known, but it is not a clean committed baseline:

- tracked Planning pointer modified: `docs/design/project-spine/CURRENT.md`;
- untracked frozen/active 05-C artifacts:
  `01_PL_V39_05_C_AUTHORITY_BINDING_REPORT.md`,
  `02_PL_V39_05_C_IMPLEMENTATION_START_CONTRACT.md`,
  `PL_V39_05_C_INCOMING_ADJUDICATION.md`,
  `PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-CHANGE-DEFINITION-v1.md`,
  `PL-V39-05-C-DEFINITION-ACTIVATION-v1.md`,
  `PL-V39-05-C-IMPLEMENTATION-PLAN-v1.md`;
- six pre-existing incoming files already adjudicated by
  `PL_V39_05_C_INCOMING_ADJUDICATION.md`.

No unknown or unadjudicated dirt was found. Definition Activation already
adjudicated this known Planning/incoming dirt as the pre-execution baseline.
It is retained as-is; T-01 must record the exact live HEAD, status, and changed
paths as its first execution-ledger entry. A clean commit is not a prerequisite
for Formal Readiness or T-01.

### Bounded adjudication of the alleged `R-00` blocker

The frozen approved Plan revision
`e93e7e8fa0aa80cdbad5dfb0861460c4f2990495c6313c9d1321929a45e67943` contains
no `R-00` rule requiring a clean committed central baseline before Readiness or
T-01. Its explicit lifecycle sequence is owner Plan approval → read-only
Formal Readiness → separate owner Execution authorization → T-01 through T-06.
T-01 itself depends on `Formal Readiness PASS` and separate Execution
authorization; it does not depend on a commit.

The earlier authorities agree:

- Definition Activation §2 accepts the known dirty Planning/incoming tree and
  records no material authority drift.
- The Implementation Start Contract §10 puts the committed-candidate
  dependency on T-07/T-08, not on Readiness or T-01.
- The Contract §14 requires a clean committed source for consumer/update smokes,
  i.e. the release-like verification fixture, not for the pre-execution gate.
- The approved Plan's Central Candidate Gate requires separate commit
  authorization and a clean committed candidate immediately before T-07/T-08;
  its stop condition is likewise scoped to T-07/T-08.

The bounded evidence amendment changed only task evidence aggregation. It did
not authorize a sequencing or dependency change. Therefore the previous
interpretation of a pre-Readiness clean-commit requirement is an
`UNAUTHORIZED_PLAN_DRIFT / VERIFIER_DEFECT`: it moved the Central Candidate
Gate backward and is not an owner requirement. No Plan, Definition, or Contract
scope correction is made here.

## 3. Frozen-authority drift check

| Artifact | Current SHA256 | Result |
|---|---|---|
| `01_PL_V39_05_C_AUTHORITY_BINDING_REPORT.md` | `1d85b17b466bb0b0dad0b110047d25d5ee16bf753b38dc4da5a935778b7bce81` | unchanged |
| `02_PL_V39_05_C_IMPLEMENTATION_START_CONTRACT.md` | `ad18eaf8ef810af92bf31121f1a7e8e5521dab50fa0400c428e92cd897580d5d` | unchanged |
| `PL_V39_05_C_INCOMING_ADJUDICATION.md` | `6d5179f2f1992bcfbdceb6cf920042925219086df71304b7e641167433676283` | unchanged |
| approved Change Definition | `98769cceedd226fd602890daa308c9c47682089f89fd99ff2e6748c1a5932751` | unchanged |
| Definition Activation | `39c80d87469f478bc9e383dfe04c93cad85baefa1e524655a24bdbf66ece2b45` | unchanged |
| approved Implementation Plan | `e93e7e8fa0aa80cdbad5dfb0861460c4f2990495c6313c9d1321929a45e67943` | unchanged at readiness start |
| canonical `CURRENT.md` | `3c1797fae3ded3cc02a2c1654c68299e48720f597c4e8e7fe37896b0327c6cf9` | readiness-start pointer was `run_pl_v39_05_c_formal_readiness`; corrected in place by this adjudication |
| canonical `roadmap/ROADMAP.md` | `a440375b85a5cd990b8d2641f19857b1a3cf3b6189c0cc6ad04671279c0ea337` | unchanged |

No material authority drift was found.

## 4. Conditional write-surface resolution

| Conditional path | Resolution | Evidence and execution rule |
|---|---|---|
| `template/.planning/framework/OWNERSHIP.yml` | `NOT REQUIRED` | Existing `.planning/assessments/*_TEMPLATE.md` classifies managed templates, and `.planning/assessments/current/**` classifies materialized project-owned state. No topology runtime path is centrally rendered. |
| `copier.yml` | `NOT REQUIRED` | Existing `_skip_if_exists` preserves `CONFIG.yml`, project state, assessment current/archive, active/completed changes, indexes, and other runtime records. Split `.planning/.git`/`.gitignore` are runtime topology outputs, not Copier outputs. |
| `template/.planning/control/PROJECT_BOOTSTRAP.md` | `NOT REQUIRED` for the approved acceptance boundary | Current bootstrap already routes project-owned configuration/project-document initialization. No new bootstrap write or policy authority is required; any operator guidance belongs to the central operator docs already in scope. |
| `tests/test_template_source.py` | `REQUIRED` | Current update/check parsers expose `--vcs-ref` but no `--template-source`; the explicit update-source rebind contract therefore needs owner-test coverage. |
| `tests/test_template.py` | `REQUIRED` | The approved implementation changes managed defaults/control/template contracts; the current test only covers basic config/default and suffix invariants. |
| `tests/test_versioning.py` | `NOT REQUIRED` | No version-source rule changes. Git tags remain the sole release-version authority. |

No conditional path is a `MATERIAL GAP` requiring Definition or Plan scope
change. `OWNERSHIP.yml` and `copier.yml` must remain unchanged unless a direct
implementation fact contradicts this resolution; that would stop execution for
adjudication.

## 5. Concrete seam checks

| Seam | Current evidence | Readiness result |
|---|---|---|
| Home/config resolution | `src/planning_lite/cli.py:28,93-100` has the existing user `config.toml` seam; `_discover_template_source` is separate at `:117-134`. | `workspace.py` is the approved T-02 addition for `--home → PLANNING_LITE_HOME → Path.home()/.config/planning-lite`; no second home is needed. |
| Atomic writes | Existing proven pattern in `src/planning_lite/campaign/campaign.py:1655-1683` uses sibling temp + replace and fsync append. | Reuse only the small pattern in T-02/T-06; no Campaign semantic coupling. Registry atomic replace and serialized JSONL append are implementation obligations, not scope ambiguity. |
| Path normalization/root containment | `local_update.py:62-66,169-175` normalizes/resolves; campaign evidence uses `resolve()` plus `relative_to()`. | T-02/T-03/T-04 must add explicit product/Planning root containment and fail-closed symlink/reparse checks. This is an approved implementation seam, not a new feature. |
| Product Git | `cli.py:50-68,71-78` provides `git -C <target>` output/status/ignore helpers. | Reusable as `product_git`; all new operations must receive explicit root/context. |
| Control Git | No current `workspace.py` or `--git-dir/--work-tree` helper exists. | Approved T-03 addition: `control_git(planning_root, git_dir, ...)`; absence is expected planned work, not a Definition gap. |
| Local-only update | `local_update.py:136-141,169-233,255-304` has ownership planning and rollback, but recursively scans all files and copies directly. | T-04 must exclude every `.git`, bound scans, preserve topology metadata, and retain project-owned byte checks. |
| Doctor | `cli.py:633-682` validates required rendered files, answers, Jinja residue, and product Git only. | T-04 must label/check product and control contexts independently; no current Doctor seam contradicts the approved boundary. |
| Source precedence/rebind | Install/adopt already accept `--template-source`; update candidate rendering trusts answers `_src_path` (`cli.py:286-315`), while update/check parsers lack the explicit option (`:737-758`). | T-04 must add explicit update/check rebind with `explicit override → answers source`, fail closed when unavailable, and update source metadata. |
| Ownership | `OWNERSHIP.yml` already separates managed framework/assessment templates from project-owned `CONFIG.yml`, project, assessment current/archive, and lifecycle paths. | Existing ownership is sufficient; no manifest semantic edit is indicated. |
| Manifest/SHA | Direct probe: template files `162`, manifest listing matches, SHA path set matches, canonical-LF mismatches `0`. Existing owner tests are `test_project_shaping_foundation.py:257-277` and `test_direction_foundation.py:133-165`; prior T-03 receipt records canonical `CRLF → LF` regeneration. | T-05 may regenerate `MANIFEST_V4.md`/`SHA256SUMS.txt` once after settled edits; no new generator taxonomy is needed. |

## 6. Contract determinacy

The approved policy, registry, Git, update, and RunReceipt contracts are
implementation-determinate for the required observable behavior:

- policy namespace, defaults/override authority, allowed modes, and legacy-null
  behavior are explicit;
- registry schema, allowed portfolio status, duplicate/root-overlap failures,
  live-source inspection, atomic replacement, and no-history-copy boundary are
  explicit;
- CLI command shapes and dry-run/idempotence/fail-closed rules are explicit;
- product/control Git commands, external gitdir requirement, gitfile topology,
  independent status/HEAD, and no automatic history operations are explicit;
- RunReceipt v1 shape, nullable unknowns, provenance sources, outcome values,
  duplicate-byte idempotence/conflict failure, partial-line corruption, disabled
  behavior, and no lifecycle mutation are explicit.

No material contract ambiguity was found that requires an amendment. Identity
strings whose lexical format is intentionally unspecified remain opaque and must
not acquire invented normalization or adapter-derived meaning. Serialization
formatting and lock mechanism may be selected by implementation as long as the
specified parsed structure, atomicity, append safety, and direct observable
invariants hold. This is a deferred implementation detail, not a new feature.

## 7. Focused verification/discriminator strategy

No implementation tests were run in this readiness pass. The approved seams and
their focused evidence are:

| Work | Focused evidence after separate Execution authorization |
|---|---|
| T-02 | Add `tests/test_workspace_registry.py`; test home precedence, policy merge, schema/path validation, duplicate/overlap failure, atomic/idempotent registry, read-only inspection, and legacy-null mode. |
| T-03 | Add `tests/test_split_control_history.py`; use temporary dual-Git fixtures to prove gitfile externality, explicit contexts, ownership-derived `.gitignore`, product preservation, refusal/idempotence, and no `.git` traversal. |
| T-04 | Extend `tests/test_cli.py`, `tests/test_local_only_update.py`, and required `tests/test_template_source.py`; discriminate tracked/local-only/split selection, Doctor labels, explicit source rebind, stale source failure, topology preservation, and second preview/apply idempotence. |
| T-05 | Extend `tests/test_template.py` only for changed managed contracts; reuse `test_project_shaping_foundation.py`/`test_direction_foundation.py` integrity owners and direct manifest/SHA checks. Conditional `OWNERSHIP.yml`/`copier.yml` tests remain unnecessary unless their status changes. |
| T-06 | Add `tests/test_run_receipts.py`; test exact fields/types, null/provenance, disabled no-write, append safety, duplicate/conflict, partial-line corruption, and no lifecycle/model call. |
| T-07 | Disposable Poker byte snapshot only; prove project-owned hashes, existing lifecycle, external control Git, Doctor, exact source update, idempotence, and all-null receipt. |
| T-08 | Disposable mood unborn/adoption snapshot only; prove source rebind, split history, first-commit separation, project-owned hashes, Doctor, idempotence, and no product HEAD assumption. |

Tests assert repository structures, parsed data, Git identities, bytes, and
hashes; they do not rely on help prose or human failure rendering.

## 8. Central Candidate Gate

The candidate-commit prerequisite is confirmed and remains unsatisfied:

```text
T-01…T-06 focused evidence: not yet run
central changed-path audit: planning-only baseline currently dirty
committed central candidate: ABSENT
separate commit authorization: NOT GRANTED
T-07/T-08 disposable proofs: NOT PERMITTED
```

T-07 and T-08 cannot use a dirty source or silently commit. A clean committed
central candidate and separate commit authorization are required before either
disposable consumer proof. This does not authorize a commit in the current turn.

## 9. Execution-ledger compatibility

The approved Plan's single
`docs/design/project-spine/checkpoints/PL-V39-05-C-EXECUTION-LEDGER-v1.md`
for T-01…T-08 is compatible with the central lifecycle surface:

- it lives under the existing canonical `checkpoints/` evidence directory;
- it records task outcomes/evidence without replacing `CURRENT.md` as the active
  pointer;
- each entry carries task ID, baseline, changed paths, verification, verdict,
  findings/stop-gates, and optional standalone-artifact links;
- no per-task receipt files are created automatically;
- T-09 remains a separate final Completion Review.

The ledger is not created during readiness or before Execution authorization.

## 10. Implementation write-boundary confirmation

The approved boundary remains unchanged. If Execution is later authorized, only
the Definition/Plan surfaces may be touched: `workspace.py`, `telemetry.py`, the
approved `cli.py`/`local_update.py` changes, listed template/control/docs/
integrity files, listed tests, disposable fixture directories, the single
execution ledger, and the final T-09 Completion Review. No current code,
template, test, Poker, mood, Roadmap, recommendation archive, or release state
was changed by this pass.

No Definition or Plan scope correction is required.

## 11. Verdict and exact correction

```text
PL_V39_05_C_FORMAL_READINESS: READY
implementation_authorized: NO
next gate: separate owner Execution authorization
```

Adjudication result:

```text
no authority requires a clean committed central baseline before Formal Readiness
or T-01; the known dirty tree remains the adjudicated pre-execution baseline;
the clean committed candidate remains required only at the Central Candidate
Gate before T-07/T-08.
```

Exact correction before execution:

1. obtain separate owner Execution authorization;
2. at T-01, record the exact live baseline and first execution-ledger entry;
3. after T-01 through T-06 and their focused evidence, obtain separate owner
   authorization for the central checkpoint commit before the Central Candidate
   Gate; only then run T-07/T-08.

No commit, staging, cleaning, stashing, implementation, test execution, or live
consumer migration was performed by this adjudication. The current dirty state
is preserved for T-01; `implementation_authorized` remains `NO`.
