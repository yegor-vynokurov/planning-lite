# PL09 Governed Operation Lifecycle — Implementation Plan Amendment v2

## Authority lineage

CHANGE_ID:
CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001

AMENDMENT_KIND:
IMPLEMENTATION_PLAN_AMENDMENT

AMENDMENT_PURPOSE:
TARGETED S6 POST-PL08 PROJECT SPINE HANDOFF CORRECTION

PREDECESSOR_PLAN:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-v1.md

PREDECESSOR_PLAN_SHA256:
B38B977FD6858597380DD2DB7D7685E7272BC3881776A69370C4E615E671ABEC

PREDECESSOR_PLAN_AMENDMENT_V1:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-AMENDMENT-v1.md

PREDECESSOR_PLAN_AMENDMENT_V1_SHA256:
6639A27B1ED6504814A56FD55A21BFD49A3C69745DD981226D92872143D46BE1

CLOSURE_CORRECTION:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CLOSURE-CORRECTION-v1.md

CLOSURE_CORRECTION_SHA256:
441B7C75A5C1E17BF079EE1A055C925D316BB24B3B3D334CED64223C7994118B

CLOSURE_CORRECTION_COMMIT:
42df71659473e5c1308fba009d71bc32abb96620

IMPLEMENTATION_AUTHORIZED:
NO

Amendment v1 remains fully in force for its entry and evidence bindings.

Amendment v2 is cumulative over:

Plan v1
+ Implementation Plan Amendment v1
+ this Amendment v2

It replaces only the S6/downstream Project Spine integration assumptions described below.

## Preserved evidence

The following remain accepted and are not reopened:

S1 Attempt -> OperationGuidance:
PASS

S2 OperationGuidance -> Lifecycle:
PASS

S3 Lifecycle -> Execution:
PASS

S4 Execution -> validated RunReceipt:
PASS

S5 RunReceipt -> terminalization / PL08:
PASS

CLI typed-result serialization repair:
PRESERVED

production-shaped typed-completion repair:
PRESERVED

receipt persistence:
PASS / PRESERVED

receipt exact readback:
PASS / PRESERVED

identity triangle:
PASS / PRESERVED

Attempt terminalization:
PASS / PRESERVED

PL08 handoff:
PASS / PRESERVED

PL08_RESULT:
SATISFIED

PL08_REASON:
ALL_REQUIRED_PASS

Only S6 is reopened.

## Material finding

S6:
PL08 Result/Evidence -> authoritative Next Gate

CURRENT_STATE:
FAIL / POST_PL08_DOWNSTREAM_HANDOFF_ABSENT

FIRST_BROKEN_SEAM:
PL08 Result/Evidence -> authoritative Next Gate

GAP_CLASS:
WIRING_GAP

S6_SURFACE_CLASS:
C_OWNER_AUTHORITY_EXISTS_BUT_NO_EXECUTABLE_TRANSITION_SURFACE

Live evidence established:

.planning/ACTIVE.md has an authoritative owner contract.

No executable ACTIVE.md runtime writer exists.

No post-result Project Spine transition contract exists.

execute_governed_operation ends after evaluate_technical(...).

No post-PL08 ACTIVE read/write or owner handoff occurs.

The historical Seam 6 PASS used caller-supplied seam facts and a pre-execution next_permitted_action value.

## Authority invariant

.planning/ACTIVE.md remains authoritative for:

Change
Change status
Lifecycle stage
Stage status
Current task
Last verified checkpoint
Next gate
Next permitted action
Implementation authorized
Active context packet
Blocking decision

Project Spine / change-owner remains the owner of gate truth.

The repair must preserve:

lifecycle selects next gate:
NO

lifecycle authorizes next gate:
NO

PL08 selects next gate:
NO

Project Spine / change-owner remains authority:
YES

## Repair architecture

Add one bounded Project Spine owner adapter:

src/planning_lite/project_spine.py

This module is not:

a lifecycle engine
a workflow engine
a scheduler
a worker
a queue
a daemon
a registry
a database
a retry owner
a callback runtime
a second Attempt store
a second Project Spine

Its only mutation responsibility is one bounded post-evaluation checkpoint against the already-authoritative consumer .planning/ACTIVE.md.

## Exact new public contracts

Add exactly these public symbols:

ProjectSpineHandoffError
ProjectSpineSnapshotV1
PostEvaluationCheckpointV1
capture_project_spine_snapshot
record_post_evaluation_checkpoint

### ProjectSpineSnapshotV1

Immutable typed carrier with exactly:

active_change
lifecycle_stage
stage_status
next_gate
next_permitted_action
implementation_authorized
active_context_path
active_sha256

active_sha256 is uppercase SHA-256 over the exact raw bytes of the target .planning/ACTIVE.md.

The snapshot is a concurrency/staleness guard. It is not authority after capture and retains no raw ACTIVE content.

### PostEvaluationCheckpointV1

Immutable typed carrier with exactly:

attempt_id
result_id
evaluation_id
evaluation_status
evaluation_reason

All five values must be non-empty strings and must contain no CR or LF.

No prompt, response, transcript, receipt body, result body, context body, or arbitrary free text may be carried.

## capture_project_spine_snapshot

Exact call shape:

capture_project_spine_snapshot(target_root) -> ProjectSpineSnapshotV1

Behavior:

1. Resolve target_root/.planning/ACTIVE.md.
2. Read exact raw bytes once.
3. Parse the authoritative ACTIVE fields using the same field semantics as the existing context/resume contract.
4. Require exactly one authoritative value for all snapshot fields.
5. Compute uppercase SHA-256 over the exact raw bytes.
6. Return ProjectSpineSnapshotV1.
7. Perform no write.

Missing, malformed, ambiguous, duplicate, or contradictory authority fields fail closed with ProjectSpineHandoffError.

## record_post_evaluation_checkpoint

Exact call shape:

record_post_evaluation_checkpoint(
    target_root,
    *,
    pre_execution_snapshot: ProjectSpineSnapshotV1,
    checkpoint: PostEvaluationCheckpointV1,
    operation_guidance: OperationGuidanceV1,
) -> ProjectSpineSnapshotV1

### Authorization precondition

Before any write, require the supplied live OperationGuidanceV1 to prove:

outcome == MATCHED

authority.predicate_result == AUTHORIZED_FOR_THIS_OPERATION

capabilities contains:
  capability_id == GOVERNANCE_WRITE
  state == ALLOWED

guidance.next_gate_owner_ref == change-owner

guidance.next_gate_ref == .planning/ACTIVE.md#Active change

Failure is fail-closed and performs no mutation.

The adapter does not call select_operation_guidance. It validates only the already-selected supplied guidance.

### Concurrency/staleness guard

Before writing:

1. Read current ACTIVE raw bytes.
2. Compute current SHA-256.
3. Require current_sha256 == pre_execution_snapshot.active_sha256.
4. Parse current authority fields.
5. Require the current values of active_change, lifecycle_stage, stage_status, next_gate, next_permitted_action, implementation_authorized, and active_context_path to equal the pre-execution snapshot exactly.

Any mismatch means Project Spine state changed while the operation was running.

Response:

FAIL CLOSED
NO WRITE
NO MERGE
NO RETRY
NO INFERENCE

Never overwrite a newer owner decision.

## Exact checkpoint mutation

The operation is a Project Spine checkpoint, not a lifecycle transition.

Existing invariant remains:

A checkpoint preserves the current stage.
It never advances or closes a change.

Modify exactly one ACTIVE field:

Last verified checkpoint

No other ACTIVE field may change.

The new deterministic value is:

POST_PL08 attempt=<attempt_id> result=<result_id> evaluation=<evaluation_id> status=<evaluation_status> reason=<evaluation_reason>

serialized onto one Markdown field line with single ASCII spaces between segments and no newline inside the value.

Exact rendered field:

- Last verified checkpoint: POST_PL08 attempt=<attempt_id> result=<result_id> evaluation=<evaluation_id> status=<evaluation_status> reason=<evaluation_reason>

All carrier values must already satisfy the no-CR/no-LF validation.

The implementation must replace exactly one existing - Last verified checkpoint: field inside ## Active change. Zero matches or multiple matches fail closed.

Preserve every byte outside the replaced field value/span, including the existing newline convention. Do not rewrite or reserialize the whole Markdown document.

Persist atomically using a same-directory temporary file followed by atomic replacement. No partial target file may be observable.

## Protected owner state

The checkpoint is forbidden to alter:

Change
Change status
Lifecycle stage
Stage status
Current task
Next gate
Next permitted action
Implementation authorized
Active context packet
Blocking decision

It also must not create missing authority fields.

After atomic persistence:

1. reread target .planning/ACTIVE.md through the authoritative existing resume/context read path;
2. independently reread its raw bytes and SHA-256;
3. verify the protected owner state remains unchanged;
4. return a new ProjectSpineSnapshotV1 representing the post-write authoritative owner state.

The returned snapshot therefore has a new active_sha256 but the same authoritative gate/action/stage values unless an external owner mutation occurred, in which case the operation fails closed rather than claiming S6.

## Lifecycle integration

Extend:

src/planning_lite/operation_lifecycle.py::execute_governed_operation

with exact keyword-only inputs:

target_root
pre_execution_project_spine_snapshot: ProjectSpineSnapshotV1

Preserve the existing S1-S5 order unchanged.

The only new tail is:

evaluate_technical(...) exactly once
-> construct PostEvaluationCheckpointV1 from the exact live Attempt / ObservedResult / TechnicalEvaluation identities
-> call record_post_evaluation_checkpoint(...) exactly once
-> require successful authoritative ProjectSpineSnapshotV1 readback
-> build/expose final status projection from the post-checkpoint authoritative state
-> return GovernedLifecycleResultV1

The lifecycle must not write ACTIVE directly.

The lifecycle must not derive a gate from:

evaluation_status
evaluation_reason
execution_status
findings
receipt
Attempt terminal state

The authoritative next_gate and next_permitted_action used after PL08 must come only from the returned post-write Project Spine owner snapshot/readback.

## S6 failure semantics

If the Project Spine checkpoint or authoritative readback fails after PL08:

LIFECYCLE_DISPOSITION:
STOPPED_FAIL_CLOSED

FAILURE_STAGE:
PROJECT_SPINE_HANDOFF

FIRST_BROKEN_SEAM:
PL08 Result/Evidence -> authoritative Next Gate

GAP_CLASS:
WIRING_GAP

Do not roll back:

real execution
persisted RunReceipt
Attempt terminalization
ObservedResult
TechnicalEvaluation

Those remain historical facts. No automatic retry.

## CLI integration

Modify:

src/planning_lite/cli.py

only as follows:

1. command_execute already resolves target root and builds pre-execution resume context.
2. Before execute_governed_operation, call capture_project_spine_snapshot(target_root) exactly once.
3. Verify its authoritative values are coherent with the already-built pre-execution resume context.
4. Pass target_root and the typed snapshot into execute_governed_operation.
5. CLI never writes ACTIVE directly.
6. CLI never calls record_post_evaluation_checkpoint.
7. CLI never selects or interprets the next gate.

## Context boundary

src/planning_lite/context.py remains read-only.

No mutation is authorized there. Its existing resume/context producer remains the authoritative state readback path used after the checkpoint.

## Existing result contract

Do not create a second next-gate result contract.

Use the existing GovernedLifecycleResultV1.status_projection downstream surface. Its final projection must be constructed only after successful post-PL08 owner checkpoint/readback.

The what_next value must quote the authoritative post-PL08 next_permitted_action. No new lifecycle gate-selection field is added.

## Exact future implementation write surface

Exactly seven paths:

ADD:
src/planning_lite/project_spine.py
tests/test_project_spine.py

MODIFY:
src/planning_lite/operation_lifecycle.py
src/planning_lite/cli.py
tests/test_operation_lifecycle.py
tests/test_cli.py
tests/test_system_traversability.py

No other product, test, or template path belongs to this repair.

## Explicit exclusions

Do not modify during S6 repair:

src/planning_lite/context.py
src/planning_lite/attempt_evaluation.py
src/planning_lite/attempt_runtime.py
src/planning_lite/telemetry.py
src/planning_lite/governed_executor.py
src/planning_lite/operation_trace.py
template/.planning/changes/templates/progress.md
tests/test_operation_trace.py

The final three remain Change 2 work and are not absorbed. No template mutation is required for S6.

## Required project_spine tests

tests/test_project_spine.py must prove:

capture reads the real ACTIVE authority fields
capture SHA binds exact raw ACTIVE bytes
checkpoint requires GOVERNANCE_WRITE=ALLOWED
checkpoint requires next_gate_owner_ref=change-owner
checkpoint requires next_gate_ref=.planning/ACTIVE.md#Active change
exactly one Last verified checkpoint field changes
next gate is byte-semantically unchanged
next permitted action is unchanged
lifecycle stage is unchanged
stage status is unchanged
implementation authorization is unchanged
blocking decision is unchanged
all bytes outside the checkpoint field/span are preserved
stale raw SHA fails before write
changed protected owner state fails before write
missing checkpoint field fails closed
duplicate checkpoint field fails closed
malformed ACTIVE fails closed
malformed checkpoint carrier fails closed
atomic write/readback returns a new authoritative snapshot

## Required lifecycle tests

tests/test_operation_lifecycle.py must prove exact temporal order:

...
Attempt terminalization
-> PL08 evaluate_technical
-> Project Spine checkpoint
-> Project Spine authoritative readback
-> final status projection

Also prove:

PL08 called exactly once
Project Spine checkpoint called exactly once
same Attempt/result/evaluation identities reach checkpoint
lifecycle does not select or rewrite gate/action
Project Spine failure produces S6 fail-closed
pre-execution gate value alone cannot satisfy S6
successful post-PL08 readback supplies final owner gate/action projection

## Required CLI tests

tests/test_cli.py must prove:

command_execute captures one pre-execution ProjectSpineSnapshotV1
same typed snapshot is passed to lifecycle
CLI never invokes the post-evaluation writer directly
CLI rendering remains JSON-compatible
existing execute error/exit behavior remains preserved

## Required system traversability tests

tests/test_system_traversability.py must prove the real positive journey:

Attempt
-> OperationGuidance
-> Lifecycle
-> Execution
-> validated persisted RunReceipt
-> exact readback / identity triangle
-> Attempt terminalization
-> PL08 SATISFIED
-> Project Spine post-evaluation checkpoint
-> authoritative ACTIVE reread after PL08
-> authoritative next gate/action observation

Required successful terminal:

S1: PASS
S2: PASS
S3: PASS
S4: PASS
S5: PASS
S6: PASS

POST_PL08_OWNER_HANDOFF:
PASS

POST_PL08_AUTHORITATIVE_READBACK:
PASS

NEXT_GATE_SELECTED_BY_LIFECYCLE:
NO

NEXT_GATE_AUTHORIZED_BY_LIFECYCLE:
NO

CRITICAL_JOURNEY_SMOKE:
PASS

OBSERVED_TRAVERSABILITY_STATE:
PASS

Required negative regression:

caller-supplied SeamObservationV1 PASS
+ pre-execution next gate
+ no post-PL08 owner handoff

MUST NOT produce PASSING.

## Closure requirement

The Lifecycle prerequisite may reclose only after a fresh disposable consumer proves the complete real journey including S6.

The historical Closure v1 remains immutable. Closure Correction v1 remains valid lineage until a later explicit reclosure.

## Change boundaries

CHANGE_2:
BLOCKED / VALID / PAUSED

CHANGE_2_FRESH_FORMAL_READINESS:
NOT AUTHORIZED

CHANGE_3:
NOT_ABSORBED

MAJOR_PL09_NEXT_SLICE_GATE:
PRESERVED / UNCONSUMED

Change 2 Amendment v1 remains materialized historical governance but cannot be used as a basis for Change 2 Fresh Formal Readiness until this prerequisite is reclosed.

## Next gate

This Amendment does not authorize implementation.

After successful materialization:

NEXT_SINGLE_GATE:
FRESH_FORMAL_READINESS_PL09_LIFECYCLE_S6_CORRECTION
## Materialization boundary

Allowed governance writes:

docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-AMENDMENT-v2.md
docs/design/project-spine/CURRENT.md

CURRENT.md may receive only the bounded active resume projection needed to state:

ACTIVE_CHANGE:
CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001

LIFECYCLE_STATE:
S6_CORRECTION_PLANNED / PENDING_FRESH_FORMAL_READINESS

IMPLEMENTATION_AUTHORIZED:
NO

CHANGE_2:
BLOCKED / VALID / PAUSED

NEXT_PERMITTED_ACTION:
FRESH_FORMAL_READINESS_PL09_LIFECYCLE_S6_CORRECTION

Do not clean unrelated historical CURRENT content.

## Git boundary

Preserve unrelated dirt. Do not use git add . or git add -A.

Stage only the exact governance paths changed by this materialization. Run git diff --cached --check, create one bounded governance commit, and do not push.

## Materialization result contract

PLAN_AMENDMENT_V2_STATUS:
MATERIALIZED / OWNER_AUTHORED / IMPLEMENTATION_NOT_AUTHORIZED

LIFECYCLE_PREREQUISITE:
REOPENED / S6 CORRECTION PLANNED

NEXT_SINGLE_GATE:
FRESH_FORMAL_READINESS_PL09_LIFECYCLE_S6_CORRECTION
