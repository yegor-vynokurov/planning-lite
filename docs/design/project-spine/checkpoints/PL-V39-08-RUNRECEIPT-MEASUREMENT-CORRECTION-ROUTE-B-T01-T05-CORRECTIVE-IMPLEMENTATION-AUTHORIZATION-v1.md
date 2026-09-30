# Route B Corrective Implementation Authorization

## Explicit authorization record

```text
OWNER_DECISION_SOURCE:
EXPLICIT_HUMAN_OWNER

OWNER_DECISION:
AUTHORIZE_ROUTE_B_T01_T05_CORRECTIVE_IMPLEMENTATION_R5_01_R5_02

AUTHORIZED_FINDING_COUNT: 2
AUTHORIZED_FINDINGS:
- R5-01_PLANNING_LITE_REF_PROVENANCE_OMITTED
- R5-02_CODEX_SOURCE_ENVELOPE_FAIL_CLOSED_GAP

AUTHORIZED_PRODUCT_PATH_COUNT: 3
AUTHORIZED_PRODUCT_PATHS:
- src/planning_lite/telemetry.py
- src/planning_lite/codex_work_window.py
- src/planning_lite/cli.py

AUTHORIZED_TEST_PATH_COUNT: 3
AUTHORIZED_TEST_PATHS:
- tests/test_run_receipts.py
- tests/test_codex_work_window.py
- tests/test_cli.py

NONMATERIAL_ADVISORIES_AUTHORIZED_AS_REQUIRED_WORK:
NO

CORRECTIVE_IMPLEMENTATION_AUTHORIZED:
YES / R5-01 + R5-02 ONLY / NOT YET EXECUTED

CORRECTIVE_IMPLEMENTATION_EXECUTED:
NO

T06_FIELD_PROOF_AUTHORIZED:
NO

T00_REEXECUTION_AUTHORIZED:
NO

09_G_STARTED:
NO

NEXT_SINGLE_GATE:
RUN_CHANGE_3_ROUTE_B_T01_T05_CORRECTIVE_IMPLEMENTATION_R5_01_R5_02
```

## Owner decision

- Change: `CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001`
- Transition: `OWNER_AUTHORIZE_CHANGE_3_ROUTE_B_T01_T05_CORRECTIVE_IMPLEMENTATION`
- Decision source: `EXPLICIT_HUMAN_OWNER`
- Decision: `AUTHORIZE_ROUTE_B_T01_T05_CORRECTIVE_IMPLEMENTATION_R5_01_R5_02`
- Authorized finding count: **2**
- Authorized findings:
  - `R5-01_PLANNING_LITE_REF_PROVENANCE_OMITTED`
  - `R5-02_CODEX_SOURCE_ENVELOPE_FAIL_CLOSED_GAP`
- Entry HEAD: `19217522f3dac695602a8534d7ddb8f9bbee5858`
- Entry authority state: `918d54d7ecbb8c1ab6e70204067ea62f7d535c4806595fdbe2ef4f2cdceb103a`
- Entry candidate state: `5165b501284cdc06e5b219d4bc1863a104e9147e249a176ceb629f34850a175a`
- Entry unrelated dirt state: `2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a`
- Entry sync state: `63b210f180ba8f53546a7e2e4ccce6846e915e5051d54edd246df572cee3ab13`
- Index: empty

## Review authority and candidate baseline

The implementation review receipt is `docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-ROUTE-B-T01-T05-IMPLEMENTATION-CANDIDATE-REVIEW-v1.md`, SHA256 `b061d32f2721080021597b87f355eb631f72883e1efec92fa83a879443a8e8cd`. Its verdict is `REVIEW_FAIL / 2 MATERIAL FINDINGS`, with the two findings listed above open.

The existing T-01..T-05 implementation candidate remains the baseline for correction. It is not reverted or rebuilt from HEAD. Candidate state ID at authorization entry: `5165b501284cdc06e5b219d4bc1863a104e9147e249a176ceb629f34850a175a`.

## Authorized implementation scope

Exactly three product paths are authorized:

1. `src/planning_lite/telemetry.py`
2. `src/planning_lite/codex_work_window.py`
3. `src/planning_lite/cli.py`

Exactly three test paths are authorized:

1. `tests/test_run_receipts.py`
2. `tests/test_codex_work_window.py`
3. `tests/test_cli.py`

The scripts, `operation_lifecycle.py`, `operation_trace.py`, `workspace.py`, `pyproject.toml`, Roadmap, all other product paths, and all other test paths are outside this authorization.

### R5-01 ? installed Planning Lite ref provenance

Authorize only adding required immutable `planning_lite_ref` provenance to `WorkWindowRegistrationV1` and `ResourceObservationV1`, separate from `configuration_ref`. Resolve it from the target project's `.copier-answers.planning-lite.yml`, using `_commit` or `_vcs_ref` when `_commit` is absent. Do not add a CLI option, fall back to `configuration_ref`, use the executing package `__version__`, persist `unknown`, or create a registry/store/configuration format. If a usable installed project ref cannot be established, Work Window open must fail closed before source inspection and before registration append. Persist it prospectively, copy it unchanged to final observations, include it in replay/conflict semantics and observation/registration binding, preserve canonical readback, and leave RunReceipt v1/v2 meaning unchanged.

### R5-02 ? Codex bounded-segment envelope validation

Authorize only closing the reviewed Codex JSONL bounded-segment fail-closed gap. Preserve binary `[start,end)` boundaries, privacy/content boundaries, `token_usage_record.usage` as the resource source, and existing deduplication/arithmetic. Validate every bounded line as syntactically valid JSON with an unambiguous accepted envelope; reject duplicate JSON keys that affect envelope semantics, non-object rows, invalid or unknown top-level discriminators, and unknown/incompatible usage-adjacent nested discriminators. Validate only enough structure to safely classify known opaque/content-bearing families; do not inspect or persist prompt, assistant, reasoning, or tool body content. A malformed/incompatible stable segment must terminate as one `UNAVAILABLE` observation with an existing suitable reason, preferably `USAGE_RECORD_INVALID`, and must never support `COMPLETE` plus `DIRECT / COMPLETE_SCOPE_TOTAL`.

Required deterministic acceptance is bounded to the specified A01?A06 cases for R5-01 and R5-02, including valid replay, conflict, early fail-closed behavior, malformed/incomplete envelopes, unknown shapes, valid opaque content, and preservation of existing aggregation behavior.

## Explicit exclusions and execution state

- Nonmaterial advisories N5-A01 and N5-A02 authorized as required work: **NO**.
- T-06 field proof authorized: **NO**.
- T00 re-execution authorized: **NO**.
- 09-G started: **NO**.
- Corrective implementation executed in this authorization transition: **NO**.
- Source changed in this authorization transition: **NO**.
- Tests changed in this authorization transition: **NO**.
- Roadmap changed: **NO**.
- Stage, commit, push, release: **NOT PERFORMED**.

This receipt grants authority for the bounded corrections only. It does not execute them. After correction, the required focused suite is `uv run --frozen pytest tests/test_run_receipts.py tests/test_codex_run_receipt_capture.py tests/test_codex_work_window.py tests/test_cli.py`, followed by the strict resume validator and `git diff --check`. No live provider test is authorized.

## Authorization gate

- `T06_FIELD_PROOF_AUTHORIZED`: `NO`
- `T00_REEXECUTION_AUTHORIZED`: `NO`
- `09_G_STARTED`: `NO`
- Next single gate: `RUN_CHANGE_3_ROUTE_B_T01_T05_CORRECTIVE_IMPLEMENTATION_R5_01_R5_02`
