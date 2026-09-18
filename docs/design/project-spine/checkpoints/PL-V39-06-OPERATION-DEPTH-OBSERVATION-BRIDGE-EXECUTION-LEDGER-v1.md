# PL-V39-06 Operation-Depth Observation Bridge — Execution Ledger v1

Change: `CHG-PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-001`

Planning authority: `f34429aefbf09fcae43226ff74eafefd580b3b88`

This cumulative ledger is the sole execution evidence surface for T-01 through
T-05. No per-task reports or implementation-start contract were created.

## T-01 — Derived immutable projection

- status: PASS
- changed paths: `src/planning_lite/context.py`, `tests/test_context_resume.py`
- verification: `uv run --frozen pytest tests/test_context_resume.py -rA` — 28 passed
- material finding / stop-gate: none

`OperationDepthObservationV1` is frozen/slot-based, derived in memory, bounded,
and JSON-compatible through `to_dict()`; no persistence or authority surface was
added.

## T-02 — Existing resume-context binding

- status: PASS
- changed paths: `src/planning_lite/context.py`, `tests/test_context_resume.py`
- verification: start projection and CLI walking skeleton compare selected metadata, hashes, Git revision/status, freshness, counts, and bounds with producer snapshots
- material finding / stop-gate: none

The projection consumes already-built mappings and performs no filesystem read,
CLI call, source-body reread, recomputation, or second context construction.

## T-03 — Exact expansion, unavailable, and bounds semantics

- status: PASS
- changed paths: `src/planning_lite/context.py`, `tests/test_context_resume.py`
- verification: exact path/heading identity, repeat/reopen, different-source discrimination, stale/forbidden/unavailable, partial oversize, contiguous sequence, raw-field rejection, and five-event cap covered by focused tests
- material finding / stop-gate: none

Completeness precedence is `UNAVAILABLE > PARTIAL > COMPLETE`; finite reason
codes and the existing `MAX_EXPANSIONS = 5` bound are reused.

## T-04 — Focused deterministic compatibility tests

- status: PASS
- changed paths: `tests/test_context_resume.py`
- verification: 28 focused context-resume tests passed; 14 central resume-contract tests passed; existing default/CLI behavior remains passing
- material finding / stop-gate: none

The new cases remain in the existing test module and prove immutable prior
state, raw/privacy rejection, deterministic serialization, no second build, and
no fixture filesystem/Git mutation.

## T-05 — Disposable walking skeleton and scope evidence

- status: PASS
- changed paths: `src/planning_lite/context.py`, `tests/test_context_resume.py`
- verification: real CLI producer on disposable Git fixture; default start, exact `PATH#HEADING`, repeated exact `YES`, forbidden `UNAVAILABLE`, metadata-only serialization, matching bounds, unchanged file inventory/Git status
- material finding / stop-gate: two unrelated pre-existing full-suite template-manifest failures retained without repair

## Regression and boundary result

- maintainer resume: PASS; active Change exact, `EXECUTION_IN_PROGRESS`, implementation authorized `YES`, blockers `NONE`, candidate-review next gate
- full regression: `uv run --frozen pytest` — 452 passed, 2 failed, 88 warnings
- unrelated failures: `tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree` and `tests/test_project_shaping_foundation.py::test_manifest_and_sha_receipts_cover_the_current_template_tree`; both report the already-committed `template/.planning/framework/architecture-knowledge/ARCHITECTURE_KNOWLEDGE_PACK.md` missing from the existing manifest/sha receipts. No implementation or authorized surface touched template files; no repair authorized.
- `git diff --check`: PASS (Git line-ending warnings only)
- scope audit: PASS; implementation paths are exactly `src/planning_lite/context.py` and `tests/test_context_resume.py`; governance paths are CURRENT, the pre-existing formal-readiness verdict, and this ledger
- commit/stage/push: NOT PERFORMED / NOT AUTHORIZED

## Pre-correction candidate review gate

- T-01…T-05: PASS
- implementation candidate: `UNCOMMITTED / REVIEW_READY`
- commit authorization: `NO`
- push authorization: `NO`
- next permitted action: `RUN_PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_CANDIDATE_REVIEW`
- Change 2 semantic-cycle attachment: deferred

## Independent candidate review and owner adjudication

```text
INDEPENDENT_CANDIDATE_REVIEW: FAIL

OWNER_ADJUDICATION:
F-01 ACCEPTED / LOCAL_IMPLEMENTATION_DEFECT / TEST_COVERAGE_DEFECT
F-02 ACCEPTED / LOCAL_IMPLEMENTATION_DEFECT / TEST_COVERAGE_DEFECT
F-03 ACCEPTED / LOCAL_IMPLEMENTATION_DEFECT / TEST_COVERAGE_DEFECT
F-04 ACCEPTED / TEST_COVERAGE_DEFECT

CORRECTIVE_PASS_AUTHORIZED: YES / ONE_BOUNDED_PASS
DEFINITION_AMENDMENT_REQUIRED: NO
PLAN_AMENDMENT_REQUIRED: NO
FORMAL_READINESS_RERUN_REQUIRED: NO
```

## Bounded corrective evidence

### F-01 — raw / non-schema serialization

- status: CLOSED
- discriminator: direct public construction with `reasoning` and a caller-owned
  `bytearray` is rejected; all requested nested raw keys are rejected; unknown
  source metadata fails the exact schema; serialized valid output contains no
  sentinel.
- implementation: factory-only construction plus exact retained start/event
  schemas and JSON-scalar validation.

### F-02 — fabricated / unobserved provenance elevation

- status: CLOSED
- discriminator: structurally incomplete resume-shaped expansion, an
  `explicit_expansion` role with arbitrary host path, and direct forbidden,
  glob, outside-root, or otherwise unobserved unavailable source references all
  fail closed and do not appear in output.
- implementation: complete producer-shape validation, source/reason/storage/path
  invariants, start-source/revision binding, and already-bound-only unavailable
  references; no token, registry, database, or observer added.

### F-03 — start bounds and caller immutability

- status: CLOSED
- discriminator: a nine-source start and mismatched source/count metadata are
  rejected; caller-owned mutable leaves are rejected; mutation of nested
  `to_dict()` values does not alter retained observation state.
- implementation: existing `MAX_TOTAL_ARTIFACTS`, `MAX_EXPANSIONS`, and trace
  bounds/count invariants are enforced before retention; retained structures
  are immutable copies of approved scalar metadata.

### F-04 — adversarial public-boundary tests

- status: CLOSED
- discriminator: the focused module now runs 46 passing cases, including direct
  construction, nine raw-key parameters, fabricated/role-only expansion,
  four unavailable-reference attacks, over-bound/count disagreement,
  returned-copy mutation, and the real CLI walking skeleton. The original 28
  tests remain passing and were not weakened.

## Corrective verification and boundary result

- focused corrected suite: `uv run --frozen pytest tests/test_context_resume.py -rA` — 46 passed
- central resume contract: `uv run --frozen pytest tests/test_central_resume_contract.py -rA` — 14 passed
- accepted attack reproduction: PASS; all previously successful public-boundary attacks reject, valid output remains sentinel-free/detached, and no second build occurs
- walking skeleton: PASS; real CLI start/include, exact source SHA, `NO` then `YES`, bypass `UNAVAILABLE`, arbitrary ref rejection, no body retention, no fixture mutation
- full regression: `uv run --frozen pytest` — 470 passed, 2 failed, 88 warnings
- known failures: the exact two pre-existing template manifest/SHA receipt failures remain unchanged; no new regression failure
- corrective implementation paths: `src/planning_lite/context.py`, `tests/test_context_resume.py`
- governance updates: `docs/design/project-spine/CURRENT.md` and this ledger only
- Formal Readiness verdict: unchanged / `READY` / not rerun
- Definition and Plan: unchanged
- Change 2 semantic-cycle attachment: deferred / untouched
- commit/stage/push: NOT PERFORMED / NOT AUTHORIZED

## Post-correction candidate gate

- F-01: CLOSED
- F-02: CLOSED
- F-03: CLOSED
- F-04: CLOSED
- implementation candidate: `UNCOMMITTED / AWAITING_INDEPENDENT_RE_REVIEW`
- implementation authorization: `YES / bounded existing Change`
- commit authorization: `NO`
- next permitted action: `RUN_PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_CANDIDATE_RE_REVIEW`

## Amendment canonicalization and amended lifecycle alignment

The preceding execution and corrective entries remain immutable historical
evidence. The fresh independent re-review superseded the predecessor Plan's
F-02 disposition before any commit; this bounded section records the owner's
approved amendment transition and current lifecycle truth without rewriting
those entries.

```text
SECOND_RE_REVIEW: FAIL / F-02 OPEN UNDER PREDECESSOR PLAN
OWNER_ADJUDICATION: F-02 = PLAN_TRUST_BOUNDARY_GAP
OWNER_SELECTED_DIRECTION: PRODUCER_BOUND_OBSERVATION
DEFINITION_AMENDMENT: APPROVED_BY_OWNER
PLAN_AMENDMENT: APPROVED_BY_OWNER
IMPLEMENTATION_CORRECTION: PAUSED
PREVIOUS_IMPLEMENTATION_AUTHORIZATION: DOES_NOT_CARRY_FORWARD
CURRENT_CANDIDATE: UNCOMMITTED / RE_REVIEW_FAIL / PENDING_AMENDED_AUTHORITY
PREDECESSOR_PLANNING_AUTHORITY: f34429aefbf09fcae43226ff74eafefd580b3b88
AMENDED_PLANNING_AUTHORITY: NOT YET CREATED
PREDECESSOR_FORMAL_READINESS: HISTORICAL / NO LONGER SUFFICIENT FOR AMENDED IMPLEMENTATION
RENEWED_FORMAL_READINESS: REQUIRED / NOT YET RUN
NEXT: AMENDED_PLANNING_AUTHORITY_CHECKPOINT_OWNER_AUTHORIZATION
```

The approved amendments are canonically materialized at the tracked Definition
and Plan Amendment checkpoint paths. F-02 is architecturally addressed by the
producer-bound trust boundary, but implementation under that amended authority
has not happened and F-02 is not marked implementation-closed. No source/test
mutation, staging, commit, push, renewed Formal Readiness, or Planning
Authority creation occurred in this transition.

## Amended Planning Authority checkpoint authorization and lifecycle alignment

This append-only entry records the owner's explicit authorization for one
selective governance checkpoint commit. It does not rewrite the predecessor
execution history and does not close F-02 at implementation level.

```text
OWNER_AMENDED_PLANNING_AUTHORITY_CHECKPOINT_AUTHORIZATION: APPROVE
AMENDED_DEFINITION: APPROVED_BY_OWNER
AMENDED_PLAN: APPROVED_BY_OWNER
SELECTED_DIRECTION: PRODUCER_BOUND_OBSERVATION
IMPLEMENTATION_AUTHORIZED: NO
PREVIOUS_IMPLEMENTATION_AUTHORIZATION_CARRIED_FORWARD: NO
OLD_CANDIDATE: UNCOMMITTED / RE_REVIEW_FAIL / PENDING_AMENDED_AUTHORITY
FORMAL_READINESS: RENEWAL_REQUIRED / NOT_RUN
CHECKPOINT_COMMIT: AUTHORIZED / THIS GOVERNANCE CHECKPOINT
NEXT: PRE_READINESS_CANDIDATE_ISOLATION_OWNER_GATE
PREDECESSOR_PLANNING_AUTHORITY: f34429aefbf09fcae43226ff74eafefd580b3b88
AMENDED_PLANNING_AUTHORITY: APPROVED / CHECKPOINTED BY THIS GOVERNANCE COMMIT
PRE_READINESS_CANDIDATE_ISOLATION: REQUIRED / NOT AUTHORIZED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
```

## Amended implementation checkpoint

This append-only section records the one owner-authorized implementation
checkpoint commit. Historical task and review entries above remain unchanged;
this section does not close the Change or authorize Change 2.

```text
AMENDED_PLANNING_AUTHORITY: a6e7c6d761495823a5a157cfa42abf77616d6b26
FORMAL_READINESS_V2: READY
OWNER_IMPLEMENTATION_AUTHORIZATION: APPROVED / CONSUMED
IMPLEMENTATION: PASS
IMPLEMENTATION_PATHS:
src/planning_lite/context.py
tests/test_context_resume.py
FOCUSED_TESTS: 33 passed
CENTRAL_RESUME_TESTS: 47 passed
CLI_COMPATIBILITY_TESTS: 4 passed
FULL_REGRESSION: 457 passed / 2 known unrelated baseline failures
INDEPENDENT_REVIEW: REVIEW_PASS
MATERIAL_FINDINGS: 0
PRODUCER_BOUND_TRUST: PASS
CHECKPOINT_COMMIT_AUTHORIZATION: APPROVED
IMPLEMENTATION_AUTHORIZED_AFTER_CHECKPOINT: NO
PL09_GATE: PRESERVED / UNCONSUMED
NEXT: OWNER_CLOSURE_DECISION_PL_V39_06
```

## Final closure

This append-only section records the owner-approved closure after the completed
implementation checkpoint and post-commit verification. Earlier execution,
review, and checkpoint entries remain historical evidence and are not rewritten.

```text
IMPLEMENTATION_CHECKPOINT: 420113cce4c1cb56d2b620c9b770773b952c7825
COMPLETION_REVIEW: PASS
INDEPENDENT_REVIEW: REVIEW_PASS
MATERIAL_FINDINGS: 0
OWNER_CLOSURE_DECISION: APPROVE
CHANGE_STATE: CLOSED / COMPLETE
CAPABILITY: PRODUCER_BOUND_OPERATION_DEPTH_OBSERVATION_BRIDGE
IMPLEMENTATION_AUTHORIZED: NO
CHANGE2: NOT_STARTED / NOT_AUTHORIZED
PL08_RUNRECEIPT_CORRECTION: NOT_STARTED / NOT_AUTHORIZED
PROMPT_DEDUP_RUNTIME_ACTIVATION: NOT_AUTHORIZED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
NEXT: OWNER DECISION FOR NEXT BOUNDED CORRECTIVE CHANGE
```
