# PL-V39-09 Execution Efficiency Bootstrap — Implementation Plan v1

## 1. Plan Identity and Authority

- Plan ID: `CHG-PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-001-PLAN-001`
- Status: `APPROVED_BY_OWNER`
- Prepared on: `2026-09-14`
- Change: `CHG-PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-001`
- Change structure: `ONE_CHANGE_TWO_SLICES`
- Definition: `APPROVED_BY_OWNER`
- Owner approval: `USER / EXPLICIT — 2026-09-14`
- Owner Plan decision: `APPROVE`
- Independent review: `PASS`
- `PLAN-REV-01`: `CLOSED`
- `PLAN-REV-02`: `CLOSED`
- AC coverage: `15 / 15`
- Formal Readiness: `NOT RUN`
- Implementation authorization: `NO`
- Slice A execution: `NOT_AUTHORIZED`
- Slice B execution: `NOT_AUTHORIZED`
- Stage/commit/tag/push/merge/release authorization: `NO`

Entry authority is frozen to:

```text
baseline HEAD:
748fbe70dd6f3d5a6d7242df41ace2d573c40d55

approved Definition:
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-CHANGE-DEFINITION-v1.md
SHA256:
9AA61891CC31C1E784F6A7A7892D4535C5E0E4D1B25343AD995DC79B6D70912C

Definition Activation:
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-DEFINITION-ACTIVATION-v1.md
SHA256:
EE787BB0E9327BE35F173044201800DC3B4659527C9AE91911E303E4270E2087

CURRENT at Plan entry:
docs/design/project-spine/CURRENT.md
SHA256:
9A41E2F8C8E8504B6AB1686BF0D12697C406C0BF55298822BB68727DA304E869
```

This Plan operationalizes all 15 approved acceptance criteria without changing
the Definition. It authorizes no implementation. Owner approval of this Plan
authorizes only the separate read-only Formal Readiness gate; Slice A and Slice
B retain separate later execution authorizations.

## 2. Frozen Scope and Invariants

The topology is exact:

```text
Slice A: CODEX_TELEMETRY_CAPTURE
Slice B: EXECUTION_ROUTING_AND_PROMPT_DEDUP
third slice: NONE
```

The hard dependency and gates are:

```text
Plan owner approval
-> read-only Formal Readiness
-> separate owner authorization for Slice A execution
-> Slice A RED / implementation / GREEN / Walking Skeleton
-> independent Slice A review
-> owner Slice A acceptance
-> owner Slice A checkpoint-commit authorization
-> Slice A checkpoint commit
-> Slice A post-commit verification PASS
-> separate owner authorization for Slice B execution
-> Slice B RED / implementation / GREEN / Walking Skeleton
-> independent Slice B review
-> owner Slice B acceptance
-> owner Slice B checkpoint-commit authorization
-> Slice B checkpoint commit
-> Slice B post-commit verification PASS
-> bootstrap completion review
-> owner closure adjudication
-> canonical state checkpoint
-> fresh-session cutover
-> OWNER_DECISION_RESUME_PL_V39_09_AFTER_EXECUTION_EFFICIENCY_BOOTSTRAP
```

No Slice B implementation path may change during Slice A. Prompt-dedup cutover
cannot begin until Slice B is accepted and checkpointed. A material Slice A
finding blocks Slice B; a Slice B finding does not invalidate an already-correct
Slice A checkpoint.

Recommendation disposition remains evidence/lineage only:

```text
REC-PL-ROUTING-PROMPT-DEDUP:
LINEAGE_INPUT / NOT ABSORBED BY THIS CHANGE

REC-PL-CAPABILITY-CLOSURE-001:
PROPOSED_NOT_ABSORBED / LINEAGE_AND_PILOT_INPUT

REC-PL-CODE-CONSTRUCTION-QUALITY-CHECKLISTS:
PRESERVE_FOR_LATER / NOT IMPLEMENTED
```

09-B remains `CLOSED_COMPLETE`. Architecture Knowledge field validation is
`NOT_COMPLETE`; 09-E, 09-F, downstream production implementation, live consumer
mutation, and release remain unauthorized.

## 3. Minimal Implementation Architecture

### 3.1 Slice A — standalone bounded Codex projection

`scripts/capture_codex_run_receipts.py` is a central-maintainer command and an
importable test seam. It does not become a `planning-lite` CLI subcommand. It
imports and reuses `validate_receipt`, `canonical_bytes`, `append_receipt`, and
`ReceiptError` from `planning_lite.telemetry`; it does not copy or alter their
contracts and does not use a project registry.

The production command accepts only explicit bindings:

```text
--repo-root <central repository root>
--expected-head <40-character Git SHA>
--project-id planning-lite-central
--change-id <exact Change ID> | --null-change-id
--task-id <exact task/operation ID>
--run-family <exact shared run-family ID>
--outcome PASS|FAIL|BLOCKED|CANCELLED|UNKNOWN
--parent-rollout <exact rollout JSONL path>
--parent-session-id <exact session/thread ID>
--parent-turn-id <exact turn ID>
--child <exact rollout path> <exact session/thread ID> <exact turn ID> <non-negative invocation index>
```

`--child` is repeatable and its command-line order is retained. The parent
receipt uses `invocation_index = 0`; child indices are explicit non-negative
integers and must be unique among children. Role plus invocation index remains
part of identity, so a child index of zero does not alias the parent. Exactly
one of `--change-id` and `--null-change-id` is required. No default, current,
latest, newest, title, fuzzy, or timestamp-nearest selection exists.

The production receipt path is derived, not caller-selected:

```text
<resolved repo root>/.local/state/projects/planning-lite-central/telemetry/run-receipts.jsonl
```

The script verifies that `git -C <repo-root> rev-parse --show-toplevel` resolves
to the supplied root and that `git -C <repo-root> rev-parse HEAD` equals
`--expected-head` before inspecting rollout metadata or creating a directory.
`--project-id` must equal `planning-lite-central` exactly.

Internal responsibilities remain in this one script:

1. parse and validate the explicit operation/parent/children binding;
2. stream-classify the explicitly named rollout files using only the supported
   top-level host record discriminator;
3. decode only allowlisted structured session, turn, direct-parent-link,
   terminal-token, model, effort, and timestamp records;
4. reject an unsupported record envelope or any identity ambiguity;
5. map every parent/child candidate to RunReceipt v1;
6. validate and canonicalize every candidate before the first append;
7. classify every existing receipt ID as missing, byte-identical, or
   conflicting before the first append;
8. append missing candidates in parent-then-command-line-child order through
   the existing append owner; and
9. read back the stream and verify every expected ID and the exact expected
   operation receipt count.

Content-bearing prompt, assistant-message, tool-payload, and reasoning records
are never JSON-decoded, retained, hashed, logged, or used for attribution. The
metadata classifier must find a supported top-level type before a payload; if
the host shape does not permit content-free classification, capture fails as
`UNSUPPORTED_HOST_RECORD_SHAPE`. Error output must identify file/record ordinal
and failure class without echoing record bodies.

Within the exactly bound turn, the terminal counter is the last structurally
valid cumulative `token_count` record before that turn's explicit completion
record, by JSONL stream order. This is not session selection by recency. Missing
completion, no counter, a counter after completion, or more than one turn
matching the supplied identity fails closed. Formal Readiness must verify that
the retained host shape exposes these boundaries without content inspection;
otherwise it records `FORMAL_READINESS: BLOCKED`.

### 3.2 Exact RunReceipt v1 mapping

```text
schema_version        = 1
receipt_id            = deterministic identity defined in §3.3
occurred_at_utc       = terminal token-counter timestamp normalized to UTC
project_id            = explicit planning-lite-central
planning_lite_ref     = exact verified expected HEAD
change_id             = explicit value or explicit null
task_id               = explicit value
run_family            = explicit value
agent_role            = PARENT or CHILD
model_id              = exact structured host model identity
model_tier            = null
invocation_index      = 0 for parent; explicit value for child
outcome                = explicit command input; never inferred
tokens.input          = exact host input_tokens
tokens.output         = exact host output_tokens
tokens.cached         = exact host cached_input_tokens
tokens.reasoning      = exact host reasoning_output_tokens
tokens.total          = exact host total_tokens
tokens.source         = external_runtime
verifier_used         = null
reviewer_used         = null
model_escalation      = null
retry                 = null
recheck               = null
reads.planning        = null
reads.non_planning    = null
reads.source          = unavailable
runtime_source        = codex_rollout_jsonl_v1
```

Token values must be integers, not booleans, and non-negative. Cached input is
a subset of input and is not added to total. Cache-write tokens have no V1 field
and are not remapped. The adapter neither recomputes nor repairs host totals.
Reasoning effort is required binding evidence when exposed, but remains outside
RunReceipt v1 and is returned only in the structured capture summary for the
execution ledger.

Timestamp normalization parses the source ISO-8601 timestamp as an aware
instant, converts it to UTC, emits six fractional digits, and replaces `+00:00`
with `Z`. A missing/naive/invalid timestamp fails closed.

### 3.3 Receipt-ID encoding decision

The receipt identity input is this exact JSON object:

```json
{
  "agent_role": "PARENT|CHILD",
  "change_id": "<exact string or null>",
  "host_session_id": "<exact structured host session/thread ID>",
  "host_turn_id": "<exact structured host turn ID>",
  "invocation_index": 0,
  "planning_lite_ref": "<exact verified HEAD>",
  "project_id": "planning-lite-central",
  "run_family": "<exact input>",
  "schema": "planning-lite-codex-receipt-id-v1",
  "task_id": "<exact input>"
}
```

Construction is `json.dumps(identity, sort_keys=True, separators=(",", ":"),
ensure_ascii=False).encode("utf-8")`. The digest is lowercase
`hashlib.sha256(bytes).hexdigest()`, and the stored value is:

```text
codex-run-v1:<64 lowercase hexadecimal characters>
```

No rollout path, timestamp, token, model, effort, outcome, retry/recheck,
reviewer/verifier, or filesystem separator enters the ID. Exact tests freeze
the canonical identity bytes and one known digest vector, prove Unicode
stability, prove key-order independence, prove Windows/POSIX rollout paths do
not alter the ID, and prove every frozen identity input changes it.

Normative conformance vector:

```text
canonical UTF-8 JSON bytes interpreted as text:
{"agent_role":"CHILD","change_id":"CHG-PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-001","host_session_id":"session-child-001","host_turn_id":"turn-child-001","invocation_index":1,"planning_lite_ref":"748fbe70dd6f3d5a6d7242df41ace2d573c40d55","project_id":"planning-lite-central","run_family":"bootstrap-slice-b-review","schema":"planning-lite-codex-receipt-id-v1","task_id":"B-04"}

SHA-256:
8a5db46c63972343069db409940828848164a22cfaf297126c072e8bc8795283

receipt_id:
codex-run-v1:8a5db46c63972343069db409940828848164a22cfaf297126c072e8bc8795283
```

### 3.4 Batch, replay, and output contract

All candidate dictionaries pass `validate_receipt`, canonical-byte generation,
cross-candidate receipt-ID uniqueness, existing-stream structural validation,
and missing/identical/conflicting classification before the first append. One
invalid candidate therefore writes zero new receipts. A process interruption
during append may leave only a valid prefix. An identical rerun reclassifies
that prefix as byte-identical and appends the missing suffix. Same receipt ID
with different canonical bytes fails closed.

On success the command writes one compact JSON summary to stdout with:

```text
status
project_id / planning_lite_ref / change_id / task_id / run_family / outcome
receipt_path
expected_receipt_count / verified_receipt_count
records[]:
  agent_role / invocation_index / receipt_id
  session_id / turn_id / rollout_path
  model_id / reasoning_effort
  append_result = APPENDED | IDENTICAL_EXISTING
```

The summary contains structured evidence only. It is not persisted by the
adapter and grants no authority. The execution ledger records the exact command,
summary, and evidence pointers. Failure exits non-zero, emits no success
summary, and cannot change the ordinary governed task outcome.

### 3.5 Slice B — one policy, one pointer, one host profile

`template/.planning/control/EXECUTION_ROUTING.md` becomes the sole operational
vendor-neutral owner for:

- authority/envelope binding before routing;
- `DETERMINISTIC_OR_TOOL_PREFERRED`, `BOUNDED_MODEL_CAPABLE`, and
  `STRONG_JUDGMENT_REQUIRED`;
- strongest-material-requirement precedence and tool-first subwork;
- non-delegable parent responsibilities;
- routing preflight fields;
- the six-field bounded dispatch contract and bounded result contract;
- fail-closed binding behavior, stronger-child STOP, and default prohibition
  on nested delegation; and
- the exact prompt-dedup boundary.

`ROOT_ROUTER.md` gains one conditional pointer only: before executing or
delegating a material task, load `EXECUTION_ROUTING.md` and the adapter selected
by `.planning/AGENT_PROFILE.yml`. It contains no class names, model names,
dispatch fields, nesting rules, or escalation text.

The Codex adapter alone owns:

```text
STRONG_PARENT: GPT-5.6 Sol / High
DEFAULT_BOUNDED_CHILD: GPT-5.6 Luna / Extra High
NESTED_DELEGATION: FORBIDDEN_BY_DEFAULT
```

It requires explicit requested and confirmed model/effort evidence. Unavailable
confirmation permits safe direct-parent execution or
`SUBAGENT_MODEL_OVERRIDE_UNAVAILABLE`, never inherited Sol. Any tier above the
configured bounded child requires the exact stronger-child owner STOP fields
from the approved Definition.

`MANIFEST_V4.md` adds the new managed policy and increments its derived file
count. `SHA256SUMS.txt` is regenerated for the complete managed tree using
canonical LF bytes; it is never hand-edited selectively. Ownership remains
covered by the existing managed `.planning/control/**` rule, so
`OWNERSHIP.yml` and `copier.yml` remain unchanged.

## 4. Test-Backed Scaffold / RED-to-GREEN Rules

### 4.1 Common admissibility rule

Before either implementation begins, the ledger records:

```text
RED_COMMAND:
EXPECTED_FAILING_NODES:
EXPECTED_FAILURE_PREDICATES:
EXPECTED_PASSING_FIXTURE_OR_EXISTING_NODES:
OBSERVED_FAILURE_CLASS:
FORBIDDEN_FAILURE_CLASSES:
RED_PROBE_ADMISSIBLE: YES | NO
```

Only `YES` permits the next task. Syntax/import errors in the test itself,
missing pytest/dependencies, malformed or missing fixtures, wrong paths,
permission/environment failures, unrelated baseline failures, or an ambiguous
oracle are `HARNESS_OR_ENVIRONMENT_RED` and block continuation until corrected
and rerun. The correction may repair only the scaffold/harness, not weaken the
approved predicate.

### 4.2 Slice A first RED

A-01 creates only `tests/test_codex_run_receipt_capture.py`. Fixtures are built
under `tmp_path`; no permanent rollout fixture is added. The scaffold first
self-validates that its production-equivalent JSONL has exact parent/child
identity, direct linkage, terminal counters, model/effort, timestamps, and no
dependency on content records.

Exact first command:

```text
uv run --frozen pytest tests/test_codex_run_receipt_capture.py -rA
```

Expected passing node:

```text
test_production_equivalent_rollout_fixture_contract_is_valid
```

Expected failing nodes/predicates before the script exists:

```text
test_capture_walking_skeleton_maps_persists_and_reads_parent_and_child
  -> CAPTURE_CAPABILITY_MISSING

test_capture_preflight_rejects_one_invalid_candidate_without_writing
  -> CAPTURE_CAPABILITY_MISSING
```

The scaffold must emit the explicit marker only after its fixture self-check
passes. A missing fixture, JSON parse failure, collection failure, missing
dependency, syntax error, or wrong repository baseline is inadmissible.

```text
SLICE_A_RED_PROBE: BOUND
RED_PROBE_ADMISSIBLE: must be YES before A-02
```

### 4.3 Slice A GREEN discriminator set

The focused file must cover, without duplicating owner tests:

- exact parent and ordered child binding; direct child-parent linkage;
- no latest/newest/timestamp-nearest/fuzzy/title/content attribution;
- PARENT/CHILD separation, exact model, null model tier, and effort only in
  execution evidence;
- exact field/token/read/runtime mapping;
- the frozen receipt-ID vector and token/model/outcome/path exclusion;
- identical replay, conflict, and interrupted-prefix completion;
- full preflight and invalid-one-of-N zero-write behavior;
- unsupported host shape; missing/conflicting/multiple identity; missing final
  counter; invalid token type/range; unlinked child; duplicate child index; and
  HEAD mismatch;
- expected receipt-count verification; and
- privacy behavior proving content records are not decoded, persisted, hashed,
  echoed, or used.

GREEN means all focused tests pass and the two RED nodes now reach the real
adapter path. Replacing the RED marker with skip/xfail or weakening it to file
existence is forbidden.

### 4.4 Slice B first RED

B-01 modifies only `tests/test_field_control_pack_foundation.py` and adds these
four nodes:

```text
test_execution_routing_is_managed_and_single_source
test_root_router_conditionally_activates_execution_routing_without_duplication
test_codex_adapter_owns_fail_closed_model_binding_and_result_contract
test_execution_routing_manifest_and_canonical_lf_integrity
```

Exact first command:

```text
uv run --frozen pytest tests/test_field_control_pack_foundation.py -rA
```

The pre-existing nodes must remain green. The four new nodes must fail on the
absent policy, absent root pointer, absent adapter binding/contract, and absent
manifest/checksum entry respectively. A Python error, unrelated prior failure,
bad path, malformed existing file, dependency/environment failure, or assertion
that does not reach the intended seam is inadmissible.

```text
SLICE_B_RED_PROBE: BOUND
RED_PROBE_ADMISSIBLE: must be YES before B-02
```

The tests must prove the three exact classes, explicit binding confirmation,
no silent Sol inheritance, stronger-child owner STOP, default nested-delegation
prohibition, all six dispatch fields (`mission`, `source/scope boundary`,
`questions`, `required evidence`, `output contract`, `escalation rule`), child
PASS not being owner acceptance, root non-duplication, and manifest/checksum
coverage.

## 5. AC-to-Evidence Matrix

| AC | Implementation seam | RED / nearest-wrong discriminator | GREEN / Walking-Skeleton proof | Evidence location | Task owner |
|---|---|---|---|---|---|
| AC-01 | frozen two-slice task/write graph | any third subsystem/path or Slice B write during A fails scope audit | exact A=2 and B=6 implementation paths; gate sequence preserved | execution ledger scope manifests + completion review | A-01…A-05, B-01…B-04 |
| AC-02 | script maps through existing RunReceipt v1 owner | extra/missing V1 key, owner mutation, non-null tier, wrong runtime/token source | focused mapping tests plus existing `test_run_receipts.py` regression | focused pytest output + Slice A ledger | A-02, A-03 |
| AC-03 | explicit CLI binding and canonical receipt identity | latest/fuzzy/content selection; wrong/multiple identity; token/path changes ID | exact parent/child tests, known SHA-256 vector, explicit real/prod-equivalent binding summary | focused tests + A Walking Skeleton evidence | A-01…A-05 |
| AC-04 | metadata-only rollout reader and structured summary | content-derived attribution or content decode/hash/log sentinel trips | privacy fixture with hostile content sentinels remains unobserved and absent from output/receipts | focused privacy test + review | A-02, A-03, A-04 |
| AC-05 | batch preflight, existing-stream classification, sequential append/replay | invalid one-of-N, conflict, partial stream, duplicate index, unlinked child | zero-write preflight tests; idempotent replay; valid-prefix completion; separate records | focused tests + receipt read-back | A-02…A-04 |
| AC-06 | production-equivalent CLI-to-JSONL Walking Skeleton | script/parser unit green without persisted/read-back count is insufficient | exact operation -> bound turn(s) -> validator -> append -> deterministic read-back/count; finite real-host disposition with field-proof boundary | A-04/A-05 ledger evidence | A-04, A-05 |
| AC-07 | lifecycle gate between committed Slice A and Slice B | any B path changes before A post-commit PASS | exact Slice A commit and post-commit verification referenced by later Slice B authorization | ledger + checkpoint/post-commit receipts | parent / owner gates |
| AC-08 | policy/control/root/adapter ownership split | class/model prose in root or model names in vendor-neutral policy | static ownership/single-source tests and real activation traversal | focused B tests + B-04 evidence | B-01…B-04 |
| AC-09 | Codex adapter binding and policy STOP rules | unconfirmed binding inherits Sol; stronger child proceeds; nested child allowed | explicit Luna/xhigh request+confirmation in live skeleton; structured unavailable/STOP discriminators | focused tests + B-04 result contract | B-02, B-04 |
| AC-10 | exact candidate snapshot -> disposable consumer -> AGENTS -> root -> policy -> profile/adapter -> fresh rooted Codex task -> dispatch/result path | files/static tests green, stale-HEAD consumer, central-rooted child, or policy copied into the prompt cannot close | candidate/consumer hash equality, normal instruction discovery from disposable root, confirmed Luna/xhigh binding, child result, parent acceptance/rejection | B-04 execution ledger evidence | B-04 |
| AC-11 | prompt-dedup section in sole policy owner | task delta omits authority/scope/non-goals/evidence/STOP/hash/next gate, or root repeats policy | focused policy tests plus B-04 task-specific delta record | focused tests + B-04 contract | B-02, B-04 |
| AC-12 | Definition/Plan lineage and unchanged recommendation files | status/absorption mutation or Code Construction surface appears | hash/status audit shows recommendations unchanged and dispositions preserved | slice reviews + completion scope audit | parent / reviewers |
| AC-13 | enforced A-before-B and fresh-session closure sequence | B/cutover/measurement before A telemetry checkpoint is rejected | checkpoint receipts, B telemetry capture where applicable, and closure cutover record | lifecycle ledger + completion review | parent / owner gates |
| AC-14 | RED admissibility plus required A/B real paths | artifact existence, unit green, skipped RED, or missing activation/read-back cannot close | admissible RED -> GREEN plus A production-equivalent and B live Walking Skeleton evidence | both slice evidence tables + reviews | A-01…A-05, B-01…B-04 |
| AC-15 | exact write manifests and STOP list | any DB/registry/daemon/schema/Roadmap/AGENTS/skill/09-E/09-F/live-consumer/release path | exact Git/status audit, unchanged owner hashes where bound, no unauthorized paths | slice and completion reviews | all tasks / parent |

```text
AC_EVIDENCE_MATRIX_COUNT: 15
behavioral AC closed solely by prose inspection: NONE
```

## 6. Task Graph

```text
Plan owner approval
-> read-only Formal Readiness
-> owner Slice A execution authorization

A-01  Slice A RED scaffold + admissibility
A-02  minimal capture adapter
A-03  focused GREEN + RunReceipt owner regression
A-04  production-equivalent Walking Skeleton
A-05  finite real-host proof disposition + evidence consolidation

-> independent Slice A review
-> owner Slice A acceptance
-> owner Slice A checkpoint-commit authorization
-> Slice A checkpoint commit
-> Slice A post-commit verification

-> owner Slice B execution authorization

B-01  Slice B RED scaffold + admissibility
B-02  routing policy + root activation + Codex adapter
B-03  manifest/checksum + deterministic GREEN/regression
B-04  live read-only Walking Skeleton

-> independent Slice B review
-> owner Slice B acceptance
-> owner Slice B checkpoint-commit authorization
-> Slice B checkpoint commit
-> Slice B post-commit verification including managed-template adoption/update smoke

-> bootstrap completion review
-> owner closure adjudication
-> canonical state checkpoint
-> fresh-session cutover
-> OWNER_DECISION_RESUME_PL_V39_09_AFTER_EXECUTION_EFFICIENCY_BOOTSTRAP
```

## 7. Task Specifications — Slice A

### A-01 — RED scaffold and admissibility

- Preconditions: approved Plan, Formal Readiness `READY`, explicit Slice A
  execution authorization, exact execution-entry HEAD/status manifest.
- Writes: `tests/test_codex_run_receipt_capture.py` only, plus the separately
  authorized execution ledger.
- Action: generate temp fixtures; add the RED/self-check nodes and the complete
  approved discriminator skeleton before adapter code exists.
- Verify: run §4.2 command; record node outcomes and exact failure classes.
- Exit: `RED_PROBE_ADMISSIBLE: YES`.
- Stop: any wrong-reason RED or need for a tracked fixture.

### A-02 — Minimum real capture adapter

- Dependency: A-01 admissible RED.
- Writes: `scripts/capture_codex_run_receipts.py`, focused tests, ledger.
- Action: implement §3.1–§3.4 only: explicit argument contract, repository/HEAD
  guard, metadata-only parser, exact binding, mapping, ID, batch preflight,
  replay-safe append, read-back count, and structured summary.
- Stop: RunReceipt V1/owner mutation, CLI/workspace mutation, content inspection,
  persistent binding state, background capture, or unlisted path.

### A-03 — Focused GREEN and owner regression

- Dependency: A-02.
- Writes: focused test/adapter corrections inside the two-path surface; ledger.
- Commands:

```text
uv run --frozen pytest tests/test_codex_run_receipt_capture.py -rA
uv run --frozen pytest tests/test_run_receipts.py -rA
git diff --check
```

- Verify exact implementation surface by combining:

```powershell
@(git diff --name-only -- scripts src tests template) +
@(git ls-files --others --exclude-standard -- scripts src tests template) |
Sort-Object -Unique
```

Expected implementation paths are exactly:

```text
scripts/capture_codex_run_receipts.py
tests/test_codex_run_receipt_capture.py
```

- Stop: any regression, unauthorized implementation path, or a GREEN achieved
  by skip/xfail/weakened assertions.

### A-04 — Production-equivalent Walking Skeleton

- Dependency: A-03 GREEN.
- Write target: temp fixture repository/rollouts and temp `.local` receipt path;
  ledger only for durable evidence.
- Exact command:

```text
uv run --frozen pytest tests/test_codex_run_receipt_capture.py::test_capture_walking_skeleton_maps_persists_and_reads_parent_and_child -rA
```

- Required path: explicit operation identity -> exact parent and linked child ->
  structured counters -> actual script command -> existing validator -> actual
  append-only JSONL -> second identical invocation -> deterministic read-back.
- Required proof: expected count equals actual count; separate PARENT/CHILD
  records; receipt IDs equal the known construction; first run appends; second
  run is identical/idempotent; no content sentinel appears anywhere.
- Stop: component-only invocation, mocked append/validator, missing read-back, or
  missing expected-count proof.

### A-05 — Bounded real-host proof and evidence consolidation

- Dependency: A-04 PASS.
- Formal Readiness must have classified the prerequisites as exactly one of
  `AVAILABLE` or `EXPECTED_UNAVAILABLE_WITH_BOUNDED_REASON`; `UNRESOLVED`
  blocks execution before A-05.
- Before capture, record in the ledger the exact rollout path(s), session/thread
  and turn IDs, parent-child topology, expected HEAD, task/run identity, outcome,
  expected receipt count, and the fully expanded command. Selection is explicit;
  discovery of “latest” is forbidden.
- If prerequisites were `AVAILABLE`, recheck them and run the recorded command
  against only those bound records and the accepted local telemetry path. Record
  generated IDs, count, model identity, reasoning effort evidence pointer, and
  append/read-back result. If prerequisites were
  `EXPECTED_UNAVAILABLE_WITH_BOUNDED_REASON`, recheck the same bounded condition
  and do not attempt a weakened proof.
- The disposition vocabulary is finite and exact:

```text
REAL_HOST_PROOF:
PASS |
NOT_AVAILABLE_WITH_BOUNDED_REASON |
BLOCKED
```

`PASS` means a bounded real-host capture used explicitly bound host identity and
topology within the approved privacy boundary and every required assertion
passed. Record `SLICE_A_FIELD_PROOF: PROVEN`. Slice A may proceed to independent
review and owner acceptance only when every mandatory deterministic Slice A
result also passes; this state does not itself accept Slice A.

`NOT_AVAILABLE_WITH_BOUNDED_REASON` means A-04 and all mandatory focused and
regression evidence passed, but a live/retained host proof cannot run for one
specific, inspectable environment or host-access reason that is not evidence of
candidate failure. Allowed examples are an unexposed retained rollout/session,
safe structured metadata access unavailable in this environment, or an
unavailable live proof vehicle while the recorded production-equivalent fixture
remains valid. Record:

```text
REAL_HOST_PROOF: NOT_AVAILABLE_WITH_BOUNDED_REASON
BOUNDED_REASON: <concrete evidence-backed fact>
PRODUCTION_EQUIVALENT_WALKING_SKELETON: PASS
SLICE_A_FIELD_PROOF: NOT_PROVEN
LIVE_HOST_INTEGRATION_CLAIM: FORBIDDEN
```

This state may proceed to independent review and owner acceptance because AC-06
requires a real **or** production-equivalent path. It is forbidden when an
available parser cannot understand the host shape, the candidate cannot bind
the requested turn, privacy would require forbidden content, receipt identity or
count is wrong, expected runtime shape remains ambiguous, or an attempted
capture fails without a bounded environmental explanation.

`BLOCKED` means a live proof was expected or attempted and failed in a way that
may indicate a candidate, parser, binding, privacy, identity, topology, or
unresolved host-shape defect. Slice A cannot be owner-accepted, Slice B cannot
begin, and the work returns to bounded repair/adjudication. It must not be
reported as bounded unavailability.

- Exit: complete the Slice A evidence table with exactly one disposition and its
  required field-proof record. The production-equivalent Walking Skeleton is
  mandatory in every non-blocked path.

## 8. Slice A Walking Skeleton and Acceptance Gate

Slice A cannot enter independent review unless this table is complete:

| Evidence | Required result |
|---|---|
| RED result and admissibility | expected nodes fail for missing capability; `RED_PROBE_ADMISSIBLE: YES` |
| Focused GREEN | complete focused file PASS; RED nodes promoted to real mandatory GREEN |
| Existing owner regression | `tests/test_run_receipts.py` PASS |
| Write-surface audit | exactly two implementation paths |
| Production-equivalent Walking Skeleton | actual CLI/parser/validator/append/read-back path PASS |
| Real-host proof | exactly `PASS`, `NOT_AVAILABLE_WITH_BOUNDED_REASON`, or `BLOCKED`, with the acceptance effect defined by A-05 |
| Slice A field proof | `PROVEN` only with real-host PASS; otherwise `NOT_PROVEN` and no live-host integration claim |
| Receipt identity | expected and actual IDs recorded separately per invocation |
| Count | expected equals verified actual operation count |
| Binding evidence | exact rollout/session/turn and direct linkage pointers |
| Effort evidence | structured effort pointer; never `model_tier` |
| Privacy | no content inspection/output/persistence evidence |
| `git diff --check` | PASS |

Independent review performs spec conformance, standards conformance, direct
reproduction of the Walking Skeleton, and exact scope accounting. Reviewer PASS
is evidence only. Owner acceptance, checkpoint authorization, commit, and
post-commit verification remain separate gates.

Slice A post-commit verification reruns the A-03 commands and A-04 node from the
exact committed checkpoint, confirms a clean tracked implementation tree, and
records the commit SHA. Only its PASS permits an owner decision on Slice B
execution.

## 9. Task Specifications — Slice B

### B-01 — RED scaffold and admissibility

- Preconditions: Slice A accepted, committed, post-commit verified; separate
  Slice B execution authorization; exact Slice B entry manifest.
- Writes: `tests/test_field_control_pack_foundation.py` only, plus ledger.
- Action: add the four §4.4 tests before modifying policy/template files.
- Verify: run the exact §4.4 command and record all old/new node outcomes.
- Exit: `RED_PROBE_ADMISSIBLE: YES`.
- Stop: wrong-reason RED or any Slice A/source/other-test mutation.

### B-02 — Policy, root activation, and Codex profile

- Dependency: B-01 admissible RED.
- Writes: `EXECUTION_ROUTING.md`, `ROOT_ROUTER.md`, Codex adapter, focused test,
  and ledger only.
- Action order: add vendor-neutral policy; add one root conditional pointer;
  add provider-specific binding and fail-closed behavior to the adapter.
- Verify incrementally with the focused B command.
- Stop: duplicated root policy, provider name in durable policy, new router or
  skill, AGENTS/Roadmap/source mutation, silent stronger-child fallback, or
  nested delegation.

### B-03 — Manifest/checksum and deterministic GREEN

- Dependency: B-02.
- Writes: manifest, regenerated SHA receipts, focused test, and ledger; repairs
  may touch only the six-path B surface.
- Action: add the managed policy to the manifest, derive the new file count,
  regenerate the complete canonical-LF receipt set, then run:

```text
uv run --frozen pytest tests/test_field_control_pack_foundation.py -rA
uv run --frozen pytest tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree -rA
uv run --frozen pytest tests/test_template.py -rA
git diff --check
```

- Exact implementation-surface audit uses the A-03 PowerShell command and must
  return exactly the six paths in §11, with no `src`, other test, Roadmap,
  recommendation, skill, `AGENTS.md`, `OWNERSHIP.yml`, or `copier.yml` path.
- Stop: a GREEN obtained by prose-only checks, selective/stale hashes, or scope
  expansion.

### B-04 — Live read-only Walking Skeleton

- Dependency: B-03 GREEN.
- Task: one closed, low-risk, read-only review of the six-path Slice B candidate.
- Activation vehicle: an OS-temporary candidate-source snapshot and disposable
  Git consumer constructed from the exact uncommitted six-path candidate, then
  one fresh ephemeral Codex CLI task whose workspace root is that consumer.
- The parent constructs the candidate source with this exact PowerShell
  mechanism. `git archive` writes a file before extraction because piping its
  binary tar stream through Windows PowerShell is forbidden. No `--vcs-ref` is
  passed to Copier: the local non-Git snapshot is the source of candidate bytes.

```powershell
$centralRoot = (git rev-parse --show-toplevel).Trim()
$b04Root = Join-Path ([IO.Path]::GetTempPath()) ("planning-lite-b04-" + [Guid]::NewGuid().ToString("N"))
$candidateSource = Join-Path $b04Root "candidate-source"
$consumerRoot = Join-Path $b04Root "consumer"
$headArchive = Join-Path $b04Root "head.tar"
New-Item -ItemType Directory -Path $candidateSource, $consumerRoot | Out-Null
git -C $centralRoot archive --format=tar --output=$headArchive HEAD
tar -xf $headArchive -C $candidateSource

$sliceBPaths = @(
  "template/.planning/control/EXECUTION_ROUTING.md",
  "template/.planning/control/ROOT_ROUTER.md",
  "template/.planning/adapters/codex/README.md",
  "template/.planning/docs/MANIFEST_V4.md",
  "template/.planning/framework/SHA256SUMS.txt",
  "tests/test_field_control_pack_foundation.py"
)
foreach ($relativePath in $sliceBPaths) {
  $centralCandidate = Join-Path $centralRoot $relativePath
  $snapshotCandidate = Join-Path $candidateSource $relativePath
  if (-not (Test-Path -LiteralPath $centralCandidate -PathType Leaf)) {
    throw "Missing Slice B candidate: $relativePath"
  }
  New-Item -ItemType Directory -Force -Path (Split-Path -Parent $snapshotCandidate) | Out-Null
  Copy-Item -LiteralPath $centralCandidate -Destination $snapshotCandidate -Force
  if ((Get-FileHash -Algorithm SHA256 -LiteralPath $centralCandidate).Hash -ne
      (Get-FileHash -Algorithm SHA256 -LiteralPath $snapshotCandidate).Hash) {
    throw "Slice B overlay hash mismatch: $relativePath"
  }
}

uv run --frozen copier copy --trust --defaults `
  --data project_name=pl-v39-09-b04-disposable `
  --data agent_adapter=codex `
  --data agent=codex `
  $candidateSource $consumerRoot
git -C $consumerRoot init -b main
```

  The additional `agent=codex` render datum is required by the current
  `template/.planning/AGENT_PROFILE.yml.jinja`; `agent_adapter=codex` remains the
  recorded Copier answer. Formal Readiness must reproduce this local-source
  behavior rather than substitute `planning-lite adopt` or a Git ref that could
  resolve back to stale central HEAD/tag bytes.
- Before dispatch, compare SHA-256 for the central candidate and disposable
  consumer copies of `ROOT_ROUTER.md`, `EXECUTION_ROUTING.md`, and the Codex
  adapter. Verify the consumer `AGENTS.md` bridge names
  `.planning/control/ROOT_ROUTER.md`, the root names the canonical execution
  policy and active profile, and `.planning/AGENT_PROFILE.yml` resolves exactly
  to `.planning/adapters/codex/README.md`. Any absence or mismatch blocks B-04.
- The parent records a task-specific delta containing exact authority, target,
  read-only/no-write boundary, non-goals, evidence, STOP rules, revision/hash
  binding, and next gate. It must not copy capability classes, model/effort,
  nesting, binding-failure, escalation, or other routing-policy text into the
  proof prompt; those semantics must arrive through normal host discovery from
  the disposable consumer files.
- Classification must be `BOUNDED_MODEL_CAPABLE`; the parent records why the
  closed rubric is within the default child capability.
- Exact fresh-root runtime: installed Codex CLI `codex exec`, with global
  `-C/--cd` setting the agent workspace before request processing. The current
  inspected host is `codex-cli 0.146.0`; both the installed help and official
  Codex instruction-discovery contract bind `--cd` to workspace-root selection
  and normal root-to-current-directory `AGENTS.md` discovery. Dispatch is:

```powershell
$b04Prompt = @'
AUTHORITY:
read-only disposable proof

TARGET:
inspect the explicitly named project_name value in .copier-answers.planning-lite.yml

ALLOWED:
read-only inspection only

FORBIDDEN:
writes, commits, nested delegation

EVIDENCE:
return the discovered instruction/control references, routing classification,
requested and confirmed binding, Result Contract evidence, and inspected result

NEXT GATE:
return evidence to parent only
'@
$b04Prompt | codex --cd $consumerRoot --model gpt-5.6-luna `
  --sandbox read-only --ask-for-approval never --strict-config `
  -c 'model_reasoning_effort="xhigh"' exec --ephemeral --json -
```

  This is a new process/task, not a resumed session and not a central-rooted
  collaboration child. It uses no policy text in the prompt. `--ephemeral`
  prevents a retained CLI session; `--sandbox read-only` prohibits proof writes.
- Dispatch uses an exact Result Contract with mission, source/scope boundary,
  questions, required evidence, output contract, and escalation rule. The CLI
  request explicitly selects `GPT-5.6 Luna / Extra High`; the returned JSONL and
  retained structured host evidence must independently confirm both values and
  `nested delegation = NO`.
- The child returns findings/evidence and actual writes (`NONE`); the parent
  independently accepts or rejects contract satisfaction. Child PASS does not
  become owner acceptance.
- If the requested binding cannot be confirmed, do not substitute Sol or any
  stronger child. Record `SUBAGENT_MODEL_OVERRIDE_UNAVAILABLE`; the static
  candidate may remain correct, but AC-10/AC-14 and Slice B acceptance remain
  blocked until a conforming live path can run or the owner amends the claim.
- After evidence capture, resolve `$b04Root`, prove it remains below the OS
  temporary root, then delete that exact disposable tree. Nothing under the
  central repository or a live consumer is deleted or mutated.

## 10. Slice B Walking Skeleton and Acceptance Gate

The B-04 ledger record must include:

```text
DISPOSABLE_TEMPLATE_SOURCE: <exact OS-temporary candidate-source path>
DISPOSABLE_CONSUMER_ROOT: <exact OS-temporary consumer path>
CANDIDATE_ROOT_ROUTER_SHA256: <sha>
CONSUMER_ROOT_ROUTER_SHA256: <same sha>
CANDIDATE_EXECUTION_ROUTING_SHA256: <sha>
CONSUMER_EXECUTION_ROUTING_SHA256: <same sha>
CANDIDATE_CODEX_ADAPTER_SHA256: <sha>
CONSUMER_CODEX_ADAPTER_SHA256: <same sha>
AGENTS_TO_ROOT_ROUTER_BRIDGE: PASS
ROOT_TO_EXECUTION_ROUTING_ACTIVATION: PASS
AGENT_PROFILE_TO_CODEX_ADAPTER: PASS
CODEX_TASK_ROOT: <exact disposable consumer root>
FRESH_TASK: YES
ROUTING_POLICY_COPIED_IN_PROMPT: NO
TASK_REASONING_CLASS: BOUNDED_MODEL_CAPABLE
DELEGATION_DECISION: DELEGATE
SELECTED_EXECUTION_TIER: DEFAULT_BOUNDED_CHILD
HOST_PROFILE_REF: .planning/adapters/codex/README.md
REQUESTED_CHILD_MODEL: GPT-5.6 Luna
REQUESTED_CHILD_EFFORT: Extra High
CONFIRMED_CHILD_MODEL: GPT-5.6 Luna
CONFIRMED_CHILD_EFFORT: Extra High
MODEL_BINDING_CONFIRMED: YES
DELEGATION_REASON: <bounded reason>
NESTED_DELEGATION: NO
STRONGER_CHILD_ESCALATION_REQUIRED: NO
RESULT_CONTRACT: PRESENT / <six exact fields>
CHILD_RESULT: <direct evidence pointer>
PARENT_ACCEPTANCE_OR_REJECTION: <decision + reason>
```

Slice B cannot enter review on policy existence or static GREEN alone. It
requires all three candidate/consumer hash equalities, the live disposable-root
activation traversal, successful bounded-child binding, child result, and parent
decision. `SUBAGENT_MODEL_OVERRIDE_UNAVAILABLE`, stale source bytes, a
central-rooted task, manual policy injection, or missing instruction-chain
evidence makes B-04 `BLOCKED`; AC-10 cannot close. Independent review reproduces
static checks, audits single-source placement, inspects the live evidence, and
verifies no prompt-dedup cutover occurred.

After owner acceptance and separately authorized checkpoint commit, post-commit
verification runs from the exact clean committed central candidate:

```text
uv run --frozen pytest tests/test_field_control_pack_foundation.py -rA
uv run --frozen pytest tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree -rA
uv run --frozen pytest tests/test_template.py -rA
uv run --frozen python scripts/test_template_update.py
uv run --frozen python scripts/test_local_only_update.py
git diff --check
git status --short --untracked-files=all
```

The smokes must prove normal managed-template adoption and update, Doctor in the
disposable consumer, delivery of `EXECUTION_ROUTING.md`, and preservation of
project-owned files. They must not run at the central root through
`planning-lite doctor .` and must not mutate a live consumer.

## 11. Write-Surface Manifest

### Slice A implementation

| Path | Action |
|---|---|
| `scripts/capture_codex_run_receipts.py` | `ADD` |
| `tests/test_codex_run_receipt_capture.py` | `ADD` |

### Slice B implementation

| Path | Action |
|---|---|
| `template/.planning/control/EXECUTION_ROUTING.md` | `ADD` |
| `template/.planning/control/ROOT_ROUTER.md` | `MODIFY` |
| `template/.planning/adapters/codex/README.md` | `MODIFY` |
| `template/.planning/docs/MANIFEST_V4.md` | `MODIFY` |
| `template/.planning/framework/SHA256SUMS.txt` | `REGENERATE` |
| `tests/test_field_control_pack_foundation.py` | `MODIFY` |

Read-only Slice A owners are:

```text
src/planning_lite/telemetry.py
src/planning_lite/workspace.py
src/planning_lite/cli.py
tests/test_run_receipts.py
```

Governance/evidence surfaces are separately gated and not implementation
surface. Their planned exact carriers are:

```text
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-EXECUTION-LEDGER-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-SLICE-A-INDEPENDENT-REVIEW-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-SLICE-A-POST-COMMIT-VERIFICATION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-SLICE-B-INDEPENDENT-REVIEW-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-SLICE-B-POST-COMMIT-VERIFICATION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-COMPLETION-REVIEW-v1.md
docs/design/project-spine/CURRENT.md
```

Creating or mutating any of these requires its named lifecycle gate.

Local telemetry remains untracked at:

```text
.local/state/projects/planning-lite-central/telemetry/run-receipts.jsonl
```

It is evidence data, not a project artifact and not a new registry/database.

## 12. Verification Strategy

Verification follows the smallest evidence stack that distinguishes the new
behavior:

```text
admissible focused RED
-> focused GREEN
-> nearest existing owner regression
-> exact Git/write-boundary audit
-> required Walking Skeleton
-> independent review
-> committed-candidate post-commit verification
-> broader completion evidence
```

For B-04, the required Walking Skeleton is the exact disposable-candidate and
fresh-rooted Codex command in §9. It is temporary evidence infrastructure, adds
no central tracked path, and is not replaced by the later committed-source
adoption/update smokes.

No check asserts CLI help wording, pytest rendering, general prose formatting,
or another presentation detail unless the literal is the accepted control
token. A failing custom verifier is classified as product defect versus
verifier/harness defect before product changes.

At bootstrap completion review, after both slice post-commit verifications:

```text
uv sync
uv run --frozen pytest
uv run --frozen python scripts/test_template_update.py
uv run --frozen python scripts/test_local_only_update.py
git diff --check
git status --short --untracked-files=all
```

The completion review binds exact slice commits, 15/15 AC evidence, no open
material findings, unchanged recommendation/Roadmap/09-B boundaries, and no
unauthorized path. Full suite and consumer smokes are completion evidence, not
substitutes for either Walking Skeleton.

## 13. Formal Readiness Contract

Formal Readiness is read-only and runs only after explicit owner Plan approval.
It must report all independent blockers in one pass and verify:

1. Definition, Activation, approved Plan, and `CURRENT` paths/hashes and active
   lifecycle authority match exactly.
2. The approved Plan SHA is bound and implementation remains unauthorized.
3. Slice A's two-path and Slice B's six-path surfaces are exact; governance and
   local telemetry surfaces are classified separately.
4. `telemetry.py` still exposes RunReceipt v1, `validate_receipt`,
   `canonical_bytes`, and append semantics required here without mutation.
5. The §3.3 receipt-ID bytes, SHA-256 prefix, included/excluded inputs, timestamp
   rule, and exact test vector are fully implementable with the standard library.
6. The retained Codex rollout envelope exposes exact session/turn, direct parent
   linkage, model, reasoning effort, terminal cumulative counters, completion,
   and timestamps sufficiently for the bounded parser.
7. Record-type discrimination and selected metadata can be obtained without
   decoding, hashing, retaining, logging, or inferring from prompt, assistant,
   tool-payload, or hidden-reasoning content.
8. The pytest/runtime environment and every currently present owner/regression
   command collect and run without project mutation. Because the two new RED
   nodes are themselves the first separately authorized implementation writes,
   Readiness must not falsely claim to collect their not-yet-existing files. It
   instead verifies their exact path/node command grammar and that A-01/B-01 are
   the only tasks permitted to create those nodes; actual collection and RED
   admissibility are the mandatory first checks before adapter/policy writes.
9. GREEN/regression commands resolve to current tests and dependencies.
10. The production-equivalent Slice A evidence channel is available and
    real-host prerequisites have exactly one disposition:
    `REAL_HOST_PROOF_PREREQUISITES: AVAILABLE |
    EXPECTED_UNAVAILABLE_WITH_BOUNDED_REASON | UNRESOLVED`. `AVAILABLE` requires
    A-05 to attempt the bounded proof; expected unavailability requires a
    concrete inspectable reason and recheck in A-05; `UNRESOLVED` blocks
    Readiness. Readiness never pre-awards real-host `PASS`.
11. Existing managed-template canonical-LF integrity and clean committed-source
    requirements are understood for Slice B post-commit smokes.
12. There is no hidden requirement for RunReceipt v2, a database/registry/
    daemon, persistent binding stream, new fixture path, or mutation of
    telemetry/workspace/CLI owners.
13. There is no hidden need for Roadmap, `AGENTS.md`, skill, other test, source
    runtime, Copier, or ownership mutation in Slice B.
14. Windows-safe `git archive --output` plus `tar -xf`, the six explicit
    overlays, and local `copier copy` are available. A temp-only sentinel probe
    must prove the local non-Git source consumes overlaid bytes rather than
    central HEAD/tag bytes: alter only a copied temporary router with a harmless
    comment, render it, verify the consumer hash equals the temporary overlay and
    differs from HEAD, then delete the probe.
15. Copier accepts both `agent_adapter=codex` and the current template's required
    `agent=codex` render datum; the generated `AGENTS.md` bridge and
    `.planning/AGENT_PROFILE.yml` exist, and the latter resolves exactly to
    `.planning/adapters/codex/README.md`.
16. The installed Codex host exposes a fresh non-interactive task through
    `codex exec`; `--cd/-C` sets the disposable consumer workspace before
    request processing, `--ephemeral` starts no resumed session,
    `--sandbox read-only` is available, and normal project instruction discovery
    loads the consumer `AGENTS.md`. Readiness runs a harmless temp-consumer
    discovery probe and records the exact CLI version and root evidence.
17. The B-04 prompt remains task-specific delta only. The discovery probe and
    planned B-04 command require no copied routing, model, nesting,
    binding-failure, or escalation policy text.
18. `GPT-5.6 Luna / Extra High` remains explicitly requestable and confirmable
    through this CLI path. Inability to confirm it is a readiness blocker for
    the planned AC-10 channel, not permission to substitute another model.
19. The snapshot, consumer, and Codex proof require no central tracked write,
    live-consumer mutation, permanent helper, or new product/runtime owner.

The exact non-mutating command-viability stack is:

```text
uv run --frozen pytest --collect-only tests/test_run_receipts.py tests/test_field_control_pack_foundation.py tests/test_direction_foundation.py tests/test_template.py
uv run --frozen pytest tests/test_run_receipts.py tests/test_field_control_pack_foundation.py tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree tests/test_template.py -rA
uv run --frozen python -c "from planning_lite.telemetry import ReceiptError, append_receipt, canonical_bytes, validate_receipt"
```

The future focused-file commands are verified against the exact declared paths
and node names in §§4.2 and 4.4, then actually collected/run only after the
corresponding scaffold write is authorized. If owner policy instead requires
the final new test files themselves to collect before Slice A/B execution
authorization, Readiness must report `PLAN_SCOPE_CONFLICT`: that would require a
new pre-execution test-write gate not authorized by the Definition or this Plan.

Any material unresolved item yields:

```text
FORMAL_READINESS: BLOCKED
implementation_authorized: NO
```

A Readiness PASS still grants no Slice A execution authority.

## 14. Stop / Amendment Conditions

Stop the dependent work and request owner adjudication/amendment if execution
requires or discovers:

- RunReceipt v2 or mutation of `telemetry.py`, `workspace.py`, or `cli.py`;
- a persistent host-binding registry, database, daemon, background capture, or
  automatic host-history mining;
- prompt/assistant/tool/hidden-reasoning content inspection or attribution
  without exact unique identity;
- a new tracked fixture or any implementation path outside the exact slice
  manifest;
- a Roadmap, `AGENTS.md`, skill, mode router, workflow, ownership, Copier,
  recommendation, other source, or other test mutation;
- a third slice, new routing subsystem, duplicated root policy, host-specific
  durable policy, automatic stronger child, or nested delegation;
- Code Construction implementation, a PL08 False-Done fixture subsystem,
  Architecture Knowledge execution/field validation, 09-E, 09-F, Context
  Compiler, or production implementation outside this bootstrap;
- live consumer mutation, retrospective savings claim, tag/push/merge/release;
- candidate materialization that resolves to stale HEAD/tag bytes, cannot render
  the Codex profile, needs a permanent helper, or adds a central tracked path;
- a Codex host that cannot guarantee a fresh task rooted at the disposable
  consumer, normal `AGENTS.md` instruction discovery from that root, or exact
  Luna / Extra High request and confirmation;
- manual routing-policy injection into the B-04 proof prompt;
- Slice B work before Slice A post-commit verification PASS;
- prompt-dedup cutover before Slice B acceptance/checkpoint; or
- a RED probe failing for any wrong/harness/environment reason.

An unsupported host shape blocks only telemetry-dependent proof and produces no
receipt. It does not change the correctness or authorization result of the
ordinary governed operation.

If the exact disposable-candidate construction or fresh-rooted Codex mechanism
is unavailable, record `PLAN_REV_02_ACTIVATION_VEHICLE_UNAVAILABLE`, keep AC-10
open, and return for owner adjudication. Do not weaken the activation claim or
invent a new product command, tracked fixture, script, CLI owner, or runtime.

## 15. Completion / Fresh-Session Cutover

Neither slice is complete at `IMPLEMENTED` or static `GREEN`:

```text
Slice A complete evidence:
admissible RED -> GREEN -> owner regression -> actual validator/append/read-back
-> expected count -> finite real-host disposition and field-proof boundary
-> independent review -> owner acceptance -> checkpoint
-> post-commit verification

Slice B complete evidence:
admissible RED -> GREEN -> exact candidate overlay -> disposable consumer hash
equality -> AGENTS/root/policy/profile/adapter live traversal from a fresh Codex
task root -> confirmed bounded-child binding -> parent decision -> independent
review -> owner acceptance -> checkpoint -> post-commit verification/adoption/
update smoke
```

After both slices, a separate completion review proves 15/15 ACs and exact scope.
Owner closure then authorizes canonical state checkpointing. Only after that
checkpoint does a fresh Codex session resume from `CURRENT.md`; that prospective
real PL09 continuation begins the fair measurement window. Historical partial
counters remain calibration evidence and cannot support a retrospective savings
claim.

The return gate remains exactly:

```text
OWNER_DECISION_RESUME_PL_V39_09_AFTER_EXECUTION_EFFICIENCY_BOOTSTRAP
```

## 16. Next Gate

```text
PLAN_STATUS: APPROVED_BY_OWNER
OWNER_PLAN_DECISION: APPROVE
INDEPENDENT_REVIEW: PASS
PLAN_REV_01: CLOSED
PLAN_REV_02: CLOSED
AC_EVIDENCE_MATRIX_COUNT: 15
SLICE_A_RED_PROBE: BOUND
SLICE_A_RED_ADMISSIBILITY: BOUND
SLICE_A_WALKING_SKELETON: BOUND
SLICE_A_REAL_HOST_PROOF: PASS | NOT_AVAILABLE_WITH_BOUNDED_REASON | BLOCKED
SLICE_A_FIELD_PROOF: PROVEN | NOT_PROVEN
RECEIPT_ID_ENCODING: SPECIFIED
SLICE_B_RED_PROBE: BOUND
SLICE_B_RED_ADMISSIBILITY: BOUND
SLICE_B_DISPOSABLE_CANDIDATE_SOURCE: BOUND
SLICE_B_FRESH_CODEX_TASK_ROOT: BOUND
SLICE_B_WALKING_SKELETON: BOUND / REAL ACTIVATION REQUIRED
NO_FALSE_DONE_CLOSURE: OPERATIONALIZED
FORMAL_READINESS_CONTRACT: BOUND
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS: NOT_RUN
```

Next single gate:

```text
RUN_PL_V39_09_EXECUTION_EFFICIENCY_BOOTSTRAP_FORMAL_READINESS
```

Owner Plan approval authorizes only the separate read-only Formal Readiness
gate. The approved Plan grants no execution, Git-history, cutover, downstream
PL09, or release authority.
