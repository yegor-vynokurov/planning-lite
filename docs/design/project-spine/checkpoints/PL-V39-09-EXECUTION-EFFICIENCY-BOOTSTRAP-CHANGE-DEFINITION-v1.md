# PL-V39-09 Execution Efficiency Bootstrap Change Definition v1

## 1. Change Identity

```text
Change ID: CHG-PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-001
Title: Execution Efficiency Bootstrap
Status: APPROVED_BY_OWNER
Prepared on: 2026-09-12
Owner approval: USER / EXPLICIT — 2026-09-13
Definition decision: APPROVE
Independent review: PASS
DEF-REV-01: CLOSED
Entry authority SHA: 748fbe70dd6f3d5a6d7242df41ace2d573c40d55
Source Roadmap area: PL-V39-09
Change structure: ONE_CHANGE_TWO_SLICES
Slice A: CODEX_TELEMETRY_CAPTURE
Slice B: EXECUTION_ROUTING_AND_PROMPT_DEDUP
Activation: ACTIVE / PLANNING_IN_PROGRESS
Implementation authorization: NO
Next gate: PREPARE_PL_V39_09_EXECUTION_EFFICIENCY_BOOTSTRAP_IMPLEMENTATION_PLAN
```

This approved Definition is scope authority for one bounded bridge Change. Its
activation authorizes preparation of one bounded Implementation Plan only. It
does not create an Implementation Plan, run Formal Readiness, authorize either
slice, change routing behavior, capture telemetry, or authorize downstream
PL-V39-09 work.

## 2. Problem / Current Evidence

The current evidence establishes all of the following:

1. PL-V39-08 Eval Core is usable and remains the owner of governed Attempt,
   evidence, evaluation, Finding, and recommendation semantics.
2. `src/planning_lite/telemetry.py` already owns strict RunReceipt v1 validation
   and append-only storage. RunReceipt v1 accepts externally supplied exact token
   facts and already carries project/ref, Change/task/run, agent role, model,
   invocation, outcome, verifier/reviewer, retry/recheck, read, and runtime-source
   fields.
3. Normal Planning Lite work currently produces no continuous real-work
   RunReceipt stream. Existing disposable samples and historical Campaign totals
   do not form a complete normal-work baseline.
4. Retained structured Codex host records contain exact session/turn identity,
   parent/child relationships, token counters, model identity, and observed
   reasoning effort for applicable retained work, but Planning Lite does not
   project those facts into RunReceipt v1.
5. Planning Lite already owns durable, vendor-neutral model/effort and execution
   routing semantics in its PL-V39-07/Roadmap control model.
6. `AGENTS.md -> .planning/control/ROOT_ROUTER.md` is a reliable activation
   chain, but no canonical cross-mode operational execution-routing control is
   activated from that root.
7. Stable routing, model-binding, nesting, binding-failure, escalation, and
   subagent-result prose is repeatedly copied into task prompts.
8. Historical token evidence is `PARTIAL`, retention-dependent calibration and
   sanity evidence. It cannot support a retrospective savings claim.
9. Planning Lite has demonstrated a false-completion failure class: artifact or
   component completion can be mistaken for working capability completion when
   the real activation, wiring, or required field-evidence path is absent.

The gap is a missing bounded connection between existing owners. It is not a
need for a new telemetry platform, evaluation lifecycle, routing authority,
registry, orchestration subsystem, or general capability-closure subsystem.

## 3. Goal

Enable measured, fail-closed execution routing for normal Planning Lite work
while reducing repeated prompt boilerplate, preserving existing authority and
evidence ownership, and proving new behavior through thin real Walking Skeleton
paths rather than component existence alone. The Change creates no new
telemetry, evaluation, orchestration, or capability-closure subsystem.

Success has this order:

```text
telemetry capture available and accepted first
-> its thin real end-to-end path demonstrated
-> routing / prompt-dedup policy available and accepted second
-> its root / policy / adapter activation path demonstrated
-> canonical bootstrap closure and fresh-session cutover
-> prospective measured evidence from real PL09 continuation
```

Success does not mean proving that Luna is cheaper, proving token savings,
completing PL-V39-09, completing Architecture Knowledge, or building general
multi-agent orchestration or a universal capability-closure framework.

## 4. Authority and Lineage

This Definition is bounded by:

- `docs/design/project-spine/CURRENT.md` at
  `748fbe70dd6f3d5a6d7242df41ace2d573c40d55`, which closes 09-B, preserves the
  Roadmap visibility checkpoint, and authorizes
  preparation of this Definition only;
- `docs/design/project-spine/roadmap/ROADMAP.md`, which owns durable
  vendor-neutral execution semantics and the PL-V39-07/08/09 boundaries;
- the accepted owner adjudication
  `.local/work/experiments/01_PL09_EXECUTION_EFFICIENCY_BOOTSTRAP_OWNER_ADJUDICATION.md`;
- the bounded evidence audits
  `.local/work/experiments/01_PL08_OPERATIONAL_RECEIPTS_TOKEN_BASELINE_AUDIT.md`
  and
  `.local/work/experiments/01_AGENT_SUBAGENT_ROUTING_POLICY_PLACEMENT_AUDIT.md`;
- existing RunReceipt v1 ownership in `src/planning_lite/telemetry.py`;
- the existing consumer activation and managed-content owners under
  `template/.planning/**`;
- proposed recommendation `REC-PL-CAPABILITY-CLOSURE-001`, used only as bounded
  lineage and pilot input for the two already-approved slices.

Authority remains separated:

```text
project and owner gates -> permission and acceptance
PL07 / Roadmap -> durable vendor-neutral routing semantics
ROOT_ROUTER.md -> activation pointer
EXECUTION_ROUTING.md -> operational cross-mode routing policy
Codex adapter -> replaceable host/model/effort bindings
RunReceipt v1 -> receipt validation and append ownership
PL08 -> applicability, evaluation, findings, and measured-evidence interpretation
```

Child output and telemetry are evidence. Neither grants authority, accepts a
task, changes owner state, or changes the meaning of an otherwise governed task.

## 5. Scope

The Change has exactly two ordered slices and no third subsystem:

```text
Slice A — CODEX_TELEMETRY_CAPTURE
Slice B — EXECUTION_ROUTING_AND_PROMPT_DEDUP
```

Both slices serve one operational cutover: establish measurement first, then
materialize routing and prompt composition policy, then measure real PL09 work.
They retain separate execution authorization, independent review, owner
acceptance, checkpoint commit, and post-commit verification.

In scope:

- an explicitly bound, central-maintainer Codex-host projection into existing
  RunReceipt v1 records;
- one vendor-neutral operational execution-routing control;
- one conditional root activation pointer;
- a replaceable Codex host profile;
- managed manifest and integrity reconciliation for Slice B;
- focused tests for each bounded slice;
- one thin real or production-equivalent Walking Skeleton for each slice's
  actual capability claim;
- a pre-implementation expected-red acceptance probe for each slice where
  practical, with intended failure distinguished from harness/environment
  failure;
- prospective measurement after bootstrap closure and fresh-session cutover.

## 6. Slice A Contract — CODEX_TELEMETRY_CAPTURE

### Responsibility and owner

Slice A defines one narrow central-maintainer Codex-host adapter that maps
explicitly bound parent and child invocations into separate existing RunReceipt
v1 records. The canonical receipt validator and append owner remains
`src/planning_lite/telemetry.py`.

Expected bounded implementation write surface:

```text
scripts/capture_codex_run_receipts.py
tests/test_codex_run_receipt_capture.py
```

`src/planning_lite/telemetry.py` and `tests/test_run_receipts.py` are current
reference/owner surfaces, not expected Slice A writes. A demonstrated need to
change RunReceipt v1 or its owner requires amendment and owner adjudication.

### Explicit input and selection

Every capture invocation must receive explicitly:

```text
central repository root
exact expected Git HEAD
project_id = planning-lite-central
change_id or an explicitly supplied null
task_id
run_family
declared governed operation outcome
exact parent rollout path
exact parent session/thread ID
exact parent turn ID
ordered child bindings, each with:
  exact rollout path
  exact child session/thread ID
  exact child turn ID
  explicit non-negative invocation_index
```

Selection must never use:

- latest session or newest file;
- nearest timestamp;
- visible task label alone;
- fuzzy title matching;
- inference from prompt content.

A child is admissible only when structured host metadata directly links it to
the declared parent.

The host adapter may inspect only structured metadata necessary for binding and
exact telemetry: session/turn identity, direct parent-child linkage, exact token
counter events, exact model identity, reasoning effort as observable host
evidence, and timestamps only where they are directly bound.

It must not read, persist, hash, summarize, classify, or infer from prompt
bodies, assistant message content, tool payload content, or hidden reasoning.

### RunReceipt v1 mapping

```text
one host invocation -> one RunReceipt v1
parent and each child -> separate records
project_id -> planning-lite-central
planning_lite_ref -> exact verified central HEAD
change_id -> explicit capture input; nullable only when explicitly supplied null
task_id -> explicit capture input
run_family -> explicit capture input
agent_role -> PARENT for the parent receipt; CHILD for each child receipt
model_id -> exact structured host model identity
model_tier -> null in RunReceipt v1
invocation_index -> explicit stable operation ordering
outcome -> explicit governed operation outcome; never inferred from token events
tokens.input/output/cached/reasoning/total -> exact host counters
tokens.source -> external_runtime
reads.planning/non_planning -> null unless separately exact
reads.source -> unavailable unless separately exact
runtime_source -> codex_rollout_jsonl_v1
```

Reasoning effort must be verified from the host binding when available and
retained as execution evidence. It must not be encoded into `model_tier` or
forced into another RunReceipt field. Exact host session/turn identity,
reasoning effort, and generated receipt IDs are recorded in the existing
task/execution evidence ledger or an equivalent existing evidence surface; no
RunReceipt v1 field is added for them.

The stable join surface is `project_id`, `planning_lite_ref`, `change_id`,
`task_id`, `run_family`, `agent_role`, `invocation_index`, and `receipt_id`, with
the exact host session/turn binding retained in that existing execution evidence.
RunReceipt v1 remains sufficient for this Change unless implementation evidence
demonstrates otherwise.

### Deterministic receipt identity and replay

`receipt_id` must be deterministic from stable project/operation identity, exact
session/turn identity, agent role, invocation index, and any additional stable
lineage fields already required by the accepted operation identity. Token values
must be excluded from the ID. The exact hash algorithm and string encoding are
left to the later Plan/implementation, but the identity inputs and conflict
semantics are not.

An identical rerun with the same stable invocation identity and identical
canonical receipt bytes is idempotent: an existing identical receipt is not
duplicated. The rerun may complete receipts still missing after an interrupted
previously valid append sequence. Reuse of the same deterministic `receipt_id`
with different canonical receipt bytes is a conflict and must fail closed rather
than create a second observation.

### Fail-closed behavior

The adapter must reject the telemetry-dependent claim and write no invalid
receipt when any of these occurs:

- unknown or unsupported host-record shape;
- missing or conflicting identity;
- more than one matching turn;
- missing final token counter;
- invalid token types or ranges;
- a child is not directly linked to the declared parent;
- duplicate child `invocation_index`;
- expected HEAD mismatch;
- invalid RunReceipt v1 mapping;
- conflicting `receipt_id` reuse.

All candidate parent and child receipts must be parsed, mapped, schema-validated,
and cross-checked for operation identity, role, and invocation ordering before
the first append. This pre-append pass must also compare every deterministic
`receipt_id` with existing persisted records and classify it as missing,
byte-identical, or conflicting before any new record is written. Any pre-append
validation failure writes zero new receipts. An interruption during append may
leave only an already-valid prefix; identical replay completes the remaining
records idempotently. Completion additionally
requires verification of the expected parent/child receipt count. No retry,
role, result, or linkage may be inferred from content or proximity.

Telemetry failure has this exact authority consequence:

```text
ordinary governed task correctness / authorization -> UNCHANGED
telemetry-dependent claim -> BLOCKED
receipt write on ambiguous or invalid binding -> NONE
```

Parent and child token values remain in separate receipts and are never silently
summed. Any later aggregate must expose the parent component, every child
component, and the aggregation formula; aggregation itself is not Slice A scope.

The following require Definition amendment rather than silent expansion:

- RunReceipt v2;
- a new database or registry;
- a persistent session-binding stream;
- a background daemon;
- broad telemetry schema redesign;
- automatic host-history mining.

## 7. Slice A Walking Skeleton / No-False-Done Closure

The later Plan must bind a thin real path equivalent to:

```text
one explicitly governed Planning Lite operation
-> one exactly bound Codex parent turn
-> exact structured token facts
-> capture adapter
-> RunReceipt v1 validation
-> append-only persisted receipt
-> deterministic read-back and identity verification
```

The Slice A capability cannot close merely because the capture script exists or
parser/unit tests pass. Accepted evidence must demonstrate the actual bounded
path through host binding, adapter projection, existing validation, persistence,
and read-back.

Before Slice A implementation begins, the Plan should bind a pre-implementation
acceptance probe expected to fail for the intended missing-adapter/path reason
where practical. An expected-red caused by a broken fixture, environment,
unrelated dependency, ambiguous oracle, or wrong seam is inadmissible and does
not establish a Test-Backed Scaffold.

This pilot obligation does not create a universal closure state machine, add a
slice, or require a Walking Skeleton for routine local edits.

## 8. Slice B Contract — EXECUTION_ROUTING_AND_PROMPT_DEDUP

### Canonical ownership and expected write surface

Durable semantics remain vendor-neutral and owned by the existing Roadmap /
PL-V39-07 model. Slice B projects those semantics into these exact owners:

```text
template/.planning/control/EXECUTION_ROUTING.md
template/.planning/control/ROOT_ROUTER.md
template/.planning/adapters/codex/README.md
template/.planning/docs/MANIFEST_V4.md
template/.planning/framework/SHA256SUMS.txt
tests/test_field_control_pack_foundation.py
```

No Roadmap, `template/AGENTS.md`, mode-router, skill, workflow, source-runtime,
RunReceipt, Copier, or ownership-file mutation is expected or authorized by this
Definition.

### Capability classification

Authority and the execution envelope are bound before classification. The
operational policy must project exactly these vendor-neutral classes:

```text
DETERMINISTIC_OR_TOOL_PREFERRED
BOUNDED_MODEL_CAPABLE
STRONG_JUDGMENT_REQUIRED
```

The strongest material requirement wins for the task. Deterministic subwork
remains tool-first even inside a model-capable task.

The parent retains:

- authority binding;
- task capability classification;
- bounded dispatch contract;
- write-scope accounting;
- child-result acceptance or rejection;
- material escalation;
- the owner gate.

Delegation is allowed only when the mission, source/scope boundary, questions,
required evidence, output contract, and escalation rule are closed. Child PASS
is evidence, not owner acceptance or new authority.

### Replaceable Codex host profile

The current host mapping belongs only in the Codex adapter:

```text
STRONG_PARENT: GPT-5.6 Sol / High
DEFAULT_BOUNDED_CHILD: GPT-5.6 Luna / Extra High
NESTED_DELEGATION: FORBIDDEN_BY_DEFAULT
```

Every child dispatch must explicitly request and confirm the configured model
and effort binding. If the default binding cannot be confirmed, the parent may
execute directly when safe or report:

```text
SUBAGENT_MODEL_OVERRIDE_UNAVAILABLE
```

The system must not silently inherit or spawn Sol. A child tier above the
configured default bounded-child tier requires a STOP with:

```text
STRONGER_CHILD_ESCALATION_REQUIRED: YES
REQUESTED_CHILD_TIER: <tier/model>
WHY_DEFAULT_BOUNDED_CHILD_IS_INSUFFICIENT: <reason>
PROPOSED_CHILD_MISSION: <bounded mission>
EXPECTED_BENEFIT_OR_FAILURE_AVOIDED: <reason>
EXECUTION_STOPPED_FOR_OWNER_AUTHORIZATION: YES
```

Nested delegation and automatic stronger-child escalation remain forbidden.

### Root activation

`ROOT_ROUTER.md` receives one conditional pointer to the canonical execution
routing control and active adapter profile before material execution or
delegation. It must not duplicate capability classes, provider/model names,
dispatch fields, nesting rules, binding-failure behavior, or escalation prose.

### Prompt-dedup cutover

No prompt-dedup cutover occurs before Slice B is accepted and checkpointed.
After that checkpoint, normal task prompts may use this steady-state shape:

```text
Follow canonical Planning Lite execution routing,
the active host adapter,
and the applicable workflow/checklist/result contract.

TASK-SPECIFIC DELTA:
- authority
- target
- allowed and forbidden surface
- acceptance and evidence
- STOP conditions
- revision/hash binding
- next gate
```

Deduplication must never remove task-specific authority, mutation boundary,
non-goals, required output/evidence, STOP conditions, revision/hash binding, or
next gate. Only stable routing/model/nesting/binding-failure/escalation
boilerplate becomes canonical policy.

## 9. Slice B Walking Skeleton / No-False-Done Closure

The later Plan must bind a thin real activation path equivalent to:

```text
one bounded material task
-> ROOT_ROUTER activation
-> canonical EXECUTION_ROUTING policy
-> active Codex adapter
-> explicit Luna / Extra High binding
-> bounded Subagent Result Contract
-> child result
-> parent acceptance or rejection
```

The Slice B capability cannot close merely because the policy file, root
pointer, adapter prose, or structural unit tests exist. Accepted evidence must
demonstrate reachability through the real root/policy/adapter/result-contract
activation chain. Requested model/effort identity must remain distinct from
confirmed/observed binding evidence.

An expected-red pre-implementation probe may be used where practical, but only
when it reaches the intended missing activation seam and fails for that reason.
No PL08 False-Done fixture corpus or general Capability Closure machinery is
implemented by this pilot.

## 10. Slice Dependency / Lifecycle

Hard dependency:

```text
Slice A accepted
-> Slice A checkpoint committed
-> Slice A post-commit verification PASS
-> Slice B execution may be separately authorized
```

A material Slice A defect blocks Slice B. A later Slice B defect does not
invalidate already-correct Slice A receipt capture.

Each slice requires its own execution authorization, independent review, owner
acceptance, checkpoint authorization/commit, and post-commit verification. Plan
approval and Formal Readiness do not authorize execution. This Definition
authorizes only activation into planning and preparation of one bounded
Implementation Plan.

After both slices are accepted and post-commit verified:

```text
bootstrap owner closure
-> canonical state checkpoint
-> fresh Codex session
-> resume from CURRENT.md
-> bounded current context
-> measured real PL09 continuation
-> OWNER_DECISION_RESUME_PL_V39_09_AFTER_EXECUTION_EFFICIENCY_BOOTSTRAP
```

Ordinary PL09 downstream branches are neither selected nor authorized here.

## 11. Acceptance Criteria

### AC-01 — CHANGE_BOUNDARY

The Change contains exactly the two ordered slices defined here and creates no
third telemetry, evaluation, routing, or orchestration subsystem.

### AC-02 — TELEMETRY_REUSE

Slice A maps exact host facts into RunReceipt v1 and reuses the existing receipt
validation, canonicalization, idempotency/conflict, and append ownership without
changing its schema or authority. It preserves the exact field mapping frozen in
Section 6, including `agent_role = PARENT/CHILD`, `model_tier = null`, explicit
lineage inputs, exact token counters, and `runtime_source`.

### AC-03 — EXPLICIT_HOST_BINDING

Capture requires exact operation, expected HEAD, parent turn, child turn, direct
linkage, and invocation-index binding. Latest/newest/time-nearest/fuzzy/visible
label/content-derived attribution is rejected. `receipt_id` is deterministic
from the stable operation/invocation identity and excludes token values; exact
session/turn identity, reasoning effort, and generated IDs remain bound in the
existing execution evidence rather than being invented as new receipt fields.

### AC-04 — PRIVACY_AND_EVIDENCE_BOUNDARY

Only structured binding metadata and exact telemetry may be inspected. Prompt,
assistant, tool-payload, and hidden-reasoning content is neither read nor
persisted nor used for inference.

### AC-05 — SEPARATE_RECEIPTS_AND_FAIL_CLOSED

Parent and child invocations produce separate RunReceipt v1 records; token
totals are not silently summed; ambiguous, invalid, mismatched, incomplete, or
conflicting telemetry cannot produce an invalid receipt or a successful capture
claim. All candidates are parsed, mapped, schema-validated, and cross-checked
before the first append. Identical replay is idempotent; conflicting replay fails
closed; an interrupted valid prefix may be completed by identical replay.

### AC-06 — SLICE_A_WALKING_SKELETON

Slice A cannot close from component existence or parser/unit green alone. One
real or production-equivalent end-to-end path must prove exact host binding,
projection, RunReceipt v1 validation, persistence, and deterministic read-back.
The telemetry claim remains incomplete until the expected parent/child receipt
count and the execution-evidence binding are verified.

### AC-07 — SLICE_DEPENDENCY

Slice B execution remains impossible until Slice A is separately accepted,
checkpointed, and post-commit verified. A material open Slice A finding stops
the transition.

### AC-08 — ROUTING_SINGLE_SOURCE

One vendor-neutral operational control owns routing policy, the root only
activates it, and concrete Codex model/effort bindings remain isolated in the
replaceable Codex adapter.

### AC-09 — BOUNDED_CHILD_SAFETY

The default Luna / Extra High child binding is explicit and confirmed; silent
Sol inheritance is forbidden; a stronger child requires owner STOP; nested
delegation remains forbidden by default; parent authority remains intact.

### AC-10 — SLICE_B_WALKING_SKELETON

Slice B cannot close from policy-file or structural-test existence alone. One
real activation path must demonstrate root routing, canonical policy, active
adapter, explicit binding, bounded result contract, child result, and parent
acceptance or rejection.

### AC-11 — PROMPT_DEDUP_BOUNDARY

Only stable routing boilerplate is deduplicated. Every task retains explicit
authority, scope, non-goals, evidence/output, STOP, revision/hash, and next-gate
terms.

### AC-12 — RECOMMENDATION_LINEAGE

`REC-PL-ROUTING-PROMPT-DEDUP` is preserved as lineage input without automatic
absorption or completion. Code Construction remains preserved for later and is
not implemented by either slice. `REC-PL-CAPABILITY-CLOSURE-001` remains
proposed/not absorbed and contributes only bounded pilot completion semantics.

### AC-13 — MEASUREMENT_ORDER

Telemetry is available before the routing cutover. The first fair prospective
measurement window begins only after bootstrap closure, canonical state
checkpoint, and fresh-session resume into real PL09 work.

### AC-14 — NO_FALSE_DONE

For both slices, implementation is not capability completion unless the required
wiring or activation and accepted evidence for the actual capability claim are
present. Expected-red is admissible only when it reaches the intended seam and
fails for the intended absent-capability reason.

### AC-15 — NO_SCOPE_EXPANSION

The Change adds no new telemetry/evaluation/orchestration/capability-closure
subsystem, no PL08 False-Done fixture implementation, no 09-E or 09-F work, no
Architecture Knowledge execution, no production implementation outside the
bounded bootstrap, and no release authority.

The later Plan and Formal Readiness own exact verification commands and
discriminators. This Definition freezes observable obligations, not a test-command
inventory.

## 12. Explicit Non-Goals

This Change excludes:

- a full Operational Insights service;
- a background telemetry daemon;
- a new telemetry database or registry;
- automatic or ambiguous host-history mining;
- latest-session capture;
- prompt-body, assistant-content, tool-payload, or hidden-reasoning capture;
- RunReceipt v2 unless separately amended;
- a universal token budget, sample count, savings threshold, or promotion score;
- automatic provider/model benchmarking or model selection;
- a large synthetic routing campaign;
- a general multi-agent platform;
- nested delegation or automatic stronger-child escalation;
- a universal capability-closure subsystem or persistent closure state machine;
- PL08 False-Done fixture implementation;
- mandatory Walking Skeleton campaigns for routine local edits;
- Code Construction checklist implementation;
- Architecture Knowledge pack materialization or field validation;
- 09-E capability/executor work;
- 09-F AgentWorkPacket/context work;
- Context Compiler comparator execution;
- production implementation outside the bounded bootstrap;
- live consumer mutation;
- recommendation absorption;
- release, tag, push, or merge.

## 13. Expected Write Surfaces

Definition preparation changes only this file. Later implementation, if
separately authorized, is expected to remain within:

```text
Slice A:
scripts/capture_codex_run_receipts.py
tests/test_codex_run_receipt_capture.py

Slice B:
template/.planning/control/EXECUTION_ROUTING.md
template/.planning/control/ROOT_ROUTER.md
template/.planning/adapters/codex/README.md
template/.planning/docs/MANIFEST_V4.md
template/.planning/framework/SHA256SUMS.txt
tests/test_field_control_pack_foundation.py
```

Planning lifecycle evidence, Plan, readiness, review, checkpoint, and canonical
state surfaces remain separately owner-gated and are not implementation write
surface. No live consumer write is included.

## 14. Stop / Amendment Conditions

Stop for owner adjudication or Definition amendment if implementation requires:

- a third slice or subsystem;
- general Capability Closure infrastructure, a persistent closure state model,
  or PL08 False-Done fixture implementation;
- a RunReceipt v1/schema/validator change;
- any Slice A or Slice B tracked path outside the expected surfaces;
- a database, registry, daemon, persistent session-binding stream, or broad host
  telemetry architecture;
- prompt/content/reasoning inspection to establish identity;
- attribution without exact unique binding;
- a Roadmap, `AGENTS.md`, mode-router, skill, workflow, Copier, ownership, source
  runtime, or recommendation mutation;
- duplicated routing semantics in the root or host-specific names in the durable
  policy;
- silent model-binding fallback, nested delegation, or automatic strong-child
  escalation;
- Code Construction, AgentWorkPacket, Context Compiler, 09-E, or 09-F semantics;
- Architecture Knowledge materialization/validation, live consumer mutation, or
  release authority;
- a retrospective savings claim from the partial historical baseline.

Any material ambiguity that could produce different observable binding,
fail-closed, receipt, routing, activation, cutover, or authority behavior must be
resolved before execution rather than delegated to implementer preference.

## 15. Evidence and Evaluation Boundary

Historical token and task evidence is `PARTIAL` and may be used only for
calibration, sanity checks, and candidate discriminator design. It is not a fair
before-baseline and cannot establish retrospective savings.

The first fair prospective window begins after:

```text
both slices accepted and checkpointed
-> bootstrap closed
-> canonical state checkpointed
-> fresh session
-> resume from CURRENT.md
-> real, bounded PL09 continuation
```

PL08 later determines evidence applicability and evaluates matched real-work
evidence. Token reduction alone cannot establish success. Quality, correctness,
authority preservation, rework, model-binding evidence, and task comparability
remain material. This Change freezes no universal sample count, token budget,
savings threshold, promotion score, or provider-cost claim.

Telemetry unavailability is recorded as unavailable and blocks only claims that
depend on it. It must not be transformed into zero, inferred from elapsed time,
or treated as task failure.

For the two pilot capabilities, component/artifact existence is not sufficient
evidence. Closure consumes the smallest sufficient evidence for the actual path:
binding, wiring/activation, observable result, and field proof only where the
accepted capability claim requires it. Routine local work with an unchanged
activation path remains outside this stronger pilot discipline.

## 16. Recommendation Lineage

```text
REC-PL-ROUTING-PROMPT-DEDUP:
LINEAGE_INPUT_TO_THIS_CHANGE
STATUS_UNCHANGED_BY_DEFINITION_PREPARATION
ABSORPTION_NOT_PERFORMED

REC-PL-CODE-CONSTRUCTION-QUALITY-CHECKLISTS:
PRESERVE_FOR_LATER
OUT_OF_SCOPE_FOR_THIS_CHANGE
STATUS_UNCHANGED

REC-PL-CAPABILITY-CLOSURE-001:
LINEAGE_AND_PILOT_INPUT
PROPOSED_NOT_ABSORBED
STATUS_UNCHANGED_BY_DEFINITION_PREPARATION
NO_GENERAL_CLOSURE_SUBSYSTEM_IMPORTED

PL-REC — Prompt-Derived Governance Primitives and Reusable Agent Skills:
REFERENCE / RECONCILIATION_LATER
NO_SKILL_OR_SCHEMA_SCOPE_IMPORTED

PL-V39-09 Human Guidance / Prompt Delta Memory concept note:
REFERENCE / RECONCILIATION_LATER
NO_AGENTWORKPACKET_OR_CONTEXT_COMPILER_SCOPE_IMPORTED
```

Preparing or later accepting this Definition does not mark any recommendation
absorbed, implemented, completed, prioritized, or authoritative. Semantic-unit
disposition remains normal recommendation-reconciliation work.

## 17. Exit Gate / Next Owner Decision

```text
DEFINITION_STATUS: APPROVED_BY_OWNER
CHANGE_ID: CHG-PL-V39-09-EXECUTION-EFFICIENCY-BOOTSTRAP-001
CHANGE_STRUCTURE: ONE_CHANGE_TWO_SLICES
AC_COUNT: 15
RUNRECEIPT_V1_REUSED: YES
SLICE_A_WALKING_SKELETON_BOUND: YES
SLICE_B_WALKING_SKELETON_BOUND: YES
NO_FALSE_DONE_CLOSURE_BOUND: YES
CAPABILITY_CLOSURE_RECOMMENDATION: PROPOSED_NOT_ABSORBED / LINEAGE_AND_PILOT_INPUT
ROADMAP_MUTATION_REQUIRED: NO
CURRENT_MUTATION_REQUIRED: NO
ACTIVATION: ACTIVE / PLANNING_IN_PROGRESS
IMPLEMENTATION_AUTHORIZED: NO
SLICE_A_EXECUTION_AUTHORIZED: NO
SLICE_B_EXECUTION_AUTHORIZED: NO
```

Next gate:

```text
PREPARE_PL_V39_09_EXECUTION_EFFICIENCY_BOOTSTRAP_IMPLEMENTATION_PLAN
```

The explicit owner approval and independent-review PASS are recorded above. No
Plan has been created; readiness, execution, checkpoint, cutover, downstream
PL09 work, and release action remain unauthorized.
