# PL-V39-09 Governed Executor Callable Binding Definition Activation v1

- Document ID: PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-ACTIVATION-001
- Status: CANONICAL / DEFINITION ACTIVATION
- Activation date: 2026-09-22
- Baseline HEAD: e5cf0eb42509a4193550f77a0a6634cca556e91c
- Change: CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001
- Capability: GOVERNED_EXECUTOR_CALLABLE_BINDING
- Capability kind: BOUNDED_SYNCHRONOUS_EXECUTION_ADAPTER

## 1. OWNER APPROVAL

Approval authority:
USER / EXPLICIT / current conversation

Owner gate:
OWNER_APPROVAL_PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_CHANGE_DEFINITION

Definition decision:
APPROVE_PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_CHANGE_DEFINITION

Definition decision shorthand:
APPROVE

The owner approval freezes the approved Definition's problem, objective,
semantic owner, callable direction, authority matrix, Attempt boundary,
guidance boundary, host boundary, result boundary, receipt association,
no-retry rule, no-persistence rule, lifecycle boundary, CLI boundary,
AC-01 through AC-12, CC-01 through CC-10, stop conditions, and non-goals.

## 2. APPROVED DEFINITION

Approved Definition:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md

Approved Definition SHA256:
127F19F505527B622BF3F45D6AA83D432B8F5BE93BD5856CE516C4CEE34BE332

Definition canonical status:
CANONICAL / APPROVED CHANGE DEFINITION

Definition fidelity:
SHAPING_TO_DEFINITION_FIDELITY: PASS

The Definition preserves the approved shaping without semantic drift:

- owner path src/planning_lite/governed_executor.py;
- public symbol invoke_governed_operation;
- full AttemptRecordV1 input;
- full immutable OperationGuidanceV1 input;
- explicit bounded owner/lifecycle payload;
- host-neutral public contract plus current-host private adapter;
- existing capture producer responsibility;
- no RunReceipt schema change;
- invocation-local same-Attempt receipt association;
- ephemeral execution invocation identity;
- lifecycle-owned terminalization;
- no authority transfer;
- exactly 12 acceptance criteria;
- exactly 10 closure criteria;
- zero unresolved architecture choices.

## 3. DISCOVERY AND SHAPING LINEAGE

Empirical discovery:
.local/work/experiments/PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_EMPIRICAL_DISCOVERY.md

Discovery SHA256:
BBB0B15EC47077175BF2F909ABA3D4F3250BB8C71C82425C9714491491D531CE

Discovery verdict:
PASS_NO_EXISTING_CALLABLE_NEW_BOUNDED_BINDING_REQUIRED

Approved shaping:
.local/work/experiments/PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_SHAPING.md

Shaping full-file SHA256:
FF8DEEDA0E8027A84B8088AA1672FCBBCB3546613B8AC23F66BCF4BF40BB76B4

Shaping self-excluding normalized digest:
253A807FCB9E2481798E1D87966DB724142753D089C4E08426EF892DD2E3A712

Shaping digest conventions distinct:
YES

Shaping verdict:
PASS_SHAPING_DEFINITION_READY

## 4. CLOSED PREREQUISITES

Attempt Action Authorization:
CLOSED / COMPLETE

Attempt Runtime Access:
CLOSED / COMPLETE

Attempt Runtime Closure:
docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CLOSURE-v1.md

Attempt Runtime Closure SHA256:
3E96782EC6F70DB5F6835CDEB90F4E2EE2AEF4E92AC8CC21F463E639CC101A6E

Neither prerequisite is reopened or amended.

## 5. ACTIVATED SEMANTIC STATE

CHG-PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-001:
DEFINITION_APPROVED / PLANNING_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED

OWNER_PATH:
src/planning_lite/governed_executor.py

PUBLIC_SYMBOL:
invoke_governed_operation

ATTEMPT_INPUT_SHAPE:
FULL_ATTEMPT_RECORD_INPUT

GUIDANCE_INPUT_SHAPE:
FULL_IMMUTABLE_OPERATION_GUIDANCE_V1

HOST_ADAPTER_SHAPE:
HOST_NEUTRAL_PUBLIC_CONTRACT + CURRENT_HOST_PRIVATE_ADAPTER

RUNRECEIPT_SCHEMA_CHANGE_REQUIRED:
NO

SAME_ATTEMPT_RECEIPT_ASSOCIATION:
INVOCATION_LOCAL

EXECUTION_INVOCATION_ID_REQUIRED:
YES

TERMINALIZATION_CALL_OWNER:
FUTURE_GOVERNED_OPERATION_LIFECYCLE

NEW_AUTHORIZATION_MODEL:
NO

NEW_SUBSYSTEM:
NO

PERSISTENCE:
NO

REGISTRY:
NO

SCHEDULER:
NO

EXECUTOR_BINDING_OWNS_RETRY_POLICY:
NO

## 6. AUTHORIZATION SCOPE AFTER ACTIVATION

CHANGE_DEFINITION:
APPROVED

PLAN_PREPARATION:
AUTHORIZED

PLAN_APPROVAL:
NOT GRANTED

IMPLEMENTATION:
NOT AUTHORIZED

SOURCE_MUTATION:
NOT AUTHORIZED

TEST_MUTATION:
NOT AUTHORIZED

TELEMETRY_SCHEMA_MUTATION:
NOT AUTHORIZED

ATTEMPT_RUNTIME_MUTATION:
NOT AUTHORIZED

GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION:
NOT AUTHORIZED

CLI_EXECUTE:
NOT AUTHORIZED

FORMAL_READINESS:
NOT AUTHORIZED

COMMIT:
NOT AUTHORIZED

PUSH:
NOT AUTHORIZED

RELEASE:
NOT AUTHORIZED

This activation authorizes only preparation of a derived noncanonical
Implementation Plan candidate under the next separately authorized gate.

## 7. PRESERVED CROSS-CHANGE STATE

Governed Operation Lifecycle:

CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001:
DEFINITION_APPROVED / PLANNING_BLOCKED_BY_EXECUTOR_PREREQUISITE / IMPLEMENTATION_NOT_AUTHORIZED

Compact Semantic Operation Trace:

CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001:
BLOCKED / VALID / PAUSED

Major PL09 next-slice gate:

MAJOR_PL09_NEXT_SLICE_GATE:
PRESERVED / UNCONSUMED

CURRENT.md:

CURRENT_MUTATION:
NO

The Definition and Activation artifacts carry the durable prerequisite state.
CURRENT.md remains unchanged.

## 8. MUTATION AND GIT BOUNDARY

Authorized canonical mutation paths in this gate:

1. docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md
2. docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-ACTIVATION-v1.md

CANONICAL_MUTATION_PATH_COUNT:
2

SOURCE_MUTATIONS:
0

TEST_MUTATIONS:
0

CANONICAL_GOVERNANCE_MUTATIONS:
2

STAGED_PATHS:
0

COMMIT:
NO

PUSH:
NO

PRE_EXISTING_UNRELATED_DIRT_PRESERVED:
YES

The two existing canonical artifacts are uncommitted governance dirt pending
later checkpointing. No unrelated file was rewritten.

## 9. BYTE AND HASH RECORD

Both canonical artifacts are required to be UTF-8, LF-terminated, exactly one
terminal LF, and free of trailing spaces or tabs.

Definition SHA256 is recorded above as the full-file SHA256 after final write.

Definition Activation full-file SHA256:
COMPUTED_AFTER_FINAL_WRITE_AND_REPORTED_IN_TERMINAL_RECEIPT

No self-referential digest field is used for the Activation artifact.

## 10. NEXT GATE

NEXT_SINGLE_GATE:
OWNER_AUTHORIZATION_PL09_GOVERNED_EXECUTOR_CALLABLE_BINDING_IMPLEMENTATION_PLANNING

Executor:
GPT-5.6 Luna / Extra High

The next gate prepares a derived noncanonical Implementation Plan candidate
only. It does not inherit implementation authorization from this Activation.
