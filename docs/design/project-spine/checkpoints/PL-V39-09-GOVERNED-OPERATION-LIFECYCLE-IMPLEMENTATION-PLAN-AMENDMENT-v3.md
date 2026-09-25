# PL09 Governed Operation Lifecycle — Implementation Plan Amendment v3

## Authority and purpose

CHANGE_ID:
CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001

AMENDMENT_KIND:
IMPLEMENTATION_PLAN_AMENDMENT

AMENDMENT_PURPOSE:
TARGETED S6 FORMAL READINESS BINDING CORRECTION

PREDECESSOR_PLAN_AMENDMENT_V1:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-AMENDMENT-v1.md

PREDECESSOR_PLAN_AMENDMENT_V1_SHA256:
6639A27B1ED6504814A56FD55A21BFD49A3C69745DD981226D92872143D46BE1

PREDECESSOR_PLAN_AMENDMENT_V2:
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-AMENDMENT-v2.md

PREDECESSOR_PLAN_AMENDMENT_V2_SHA256:
7BFDFEBCCFB25ADE027FA23D3E1B0FA4384B5A163997ED21DCF75D87B0B5595F

ARCHITECTURE_BLOCKERS_FOUND:
0

BOUNDED_LIVE_BINDING_CORRECTIONS:
4

INVALID_READINESS_REQUIREMENT_WITHDRAWN:
1

IMPLEMENTATION_AUTHORIZED:
NO

The effective Plan is:

Implementation Plan v1
+ Implementation Plan Amendment v1
+ Implementation Plan Amendment v2
+ this Implementation Plan Amendment v3

Amendment v3 changes only the exact clauses below. Everything in Amendment v2 not explicitly replaced remains in force.

## Correction 1: TechnicalEvaluation live fields

Replace every Amendment v2 requirement for evaluation_status and evaluation_reason with the exact live PL08 fields:

evaluation_outcome
evaluation_reason_codes

PostEvaluationCheckpointV1 is exactly:

attempt_id: str
result_id: str
evaluation_id: str
evaluation_outcome: str
evaluation_reason_codes: tuple[str, ...]

Requirements:

attempt_id:
non-empty / no CR / no LF

result_id:
non-empty / no CR / no LF

evaluation_id:
non-empty / no CR / no LF

evaluation_outcome:
non-empty / no CR / no LF

evaluation_reason_codes:
tuple
each element non-empty
each element contains no CR or LF
preserve live PL08 order exactly
no sorting
no inferred fallback

The post-PL08 checkpoint line is:

- Last verified checkpoint: POST_PL08 attempt=<attempt_id> result=<result_id> evaluation=<evaluation_id> outcome=<evaluation_outcome> reasons=<reason1,reason2,...>

Reason codes are joined in their existing tuple order with literal comma and no added spaces.

An empty reason-code tuple is represented as:

reasons=NONE

No reason may be invented.

## Correction 2: existing lifecycle downstream result

Withdraw every Amendment v2 statement asserting that GovernedLifecycleResultV1.status_projection exists.

It does not exist. Do not add such a field.

Preserve the live GovernedLifecycleResultV1 contract and its existing downstream field.

After successful Project Spine checkpoint and authoritative readback:

authoritative Project Spine reread
-> existing build_compact_status/read-only context projection
-> existing GovernedLifecycleResultV1.downstream

The existing compact status remains exactly six keys:

where_we_are
what_is_done
what_is_current
what_next
resources
state

what_next must quote the post-PL08 authoritative next_permitted_action.

No seventh key. No lifecycle-owned next-gate field.

If the existing live downstream carrier cannot accept the existing six-key compact projection without changing its public contract, Formal Readiness must BLOCK rather than invent a replacement contract.

## Correction 3: snapshot does not depend on ResumeContext having been built

Withdraw the Amendment v2 assumption that command_execute always already has a pre-execution ResumeContext.

Every production call to execute_governed_operation must have one ProjectSpineSnapshotV1 captured from the target .planning/ACTIVE.md before lifecycle execution begins.

capture_project_spine_snapshot(target_root) reads Project Spine authority directly. It does not require a pre-existing ResumeContext.

When a ResumeContext already exists, consistency with the snapshot may be checked.

When no ResumeContext exists because supplied guidance is already available, the snapshot remains sufficient Project Spine authority evidence.

Do not perform a second guidance selection. Do not make ResumeContext a prerequisite merely to capture Project Spine state.

## Correction 4: all live lifecycle callers

The S6 contract applies to every live production caller of execute_governed_operation.

Current live callers include at least:

src/planning_lite/cli.py::command_execute
src/planning_lite/cli.py::command_finish

Both must satisfy the same pre-execution snapshot and post-PL08 Project Spine handoff contract. Neither route may bypass S6.

Within src/planning_lite/cli.py:

command_execute:
capture exactly one ProjectSpineSnapshotV1 before lifecycle invocation
pass it unchanged to lifecycle

command_finish:
capture exactly one ProjectSpineSnapshotV1 before lifecycle invocation
pass it unchanged to lifecycle

If current CLI factoring permits one shared private helper inside cli.py, that is allowed.

No new product path is required.

CLI still:

does not write ACTIVE
does not call record_post_evaluation_checkpoint
does not select next gate
does not interpret PL08 outcome as a gate

## Correction 5: Traversability false-done ownership

Withdraw the Amendment v2 requirement that a caller-supplied SeamObservationV1 PASS with a pre-execution next gate and no post-PL08 owner handoff must be rejected by check_critical_journey_smoke itself.

That requirement conflicts with the existing System Traversability contract.

The traversability checker is a pure reducer over supplied observations and evidence/probe references. It does not discover or authenticate runtime facts.

Therefore:

src/planning_lite/traversability.py:
READ_ONLY / NO MUTATION REQUIRED

False-done resistance is proved at the production-shaped evidence construction boundary.

tests/test_system_traversability.py must demonstrate:

1. execute the real/prod-equivalent S1-S6 journey;
2. do not construct the S6 PASS observation until PL08 completed, the Project Spine checkpoint succeeded, and authoritative post-PL08 ACTIVE readback succeeded;
3. bind the resulting real handoff/readback evidence refs into the supplied S6 SeamObservationV1;
4. only then call check_critical_journey_smoke;
5. assert PASSING.

Negative regression:

If no post-PL08 Project Spine handoff/readback evidence exists, the production-shaped harness must construct S6 = FAIL or an evidence/admissibility state that cannot promote the journey to PASSING.

The negative test is against the evidence construction/harness contract, not against the pure reducer's ability to distrust a deliberately fabricated input object.

A unit test may demonstrate that the pure checker accepts a syntactically valid supplied PASS observation, because that is its intended boundary. Such a unit test is not system evidence and must never be used alone to claim the real journey PASSING.

## Revised exact implementation write surface

The implementation surface remains exactly seven paths:

ADD:
src/planning_lite/project_spine.py
tests/test_project_spine.py

MODIFY:
src/planning_lite/operation_lifecycle.py
src/planning_lite/cli.py
tests/test_operation_lifecycle.py
tests/test_cli.py
tests/test_system_traversability.py

src/planning_lite/traversability.py:
READ_ONLY_DEPENDENCY / NOT_MODIFIED

No eighth product path is authorized.

## Revised test obligations

tests/test_project_spine.py is unchanged from Amendment v2 except it uses the exact live evaluation carrier names:

evaluation_outcome
evaluation_reason_codes

tests/test_operation_lifecycle.py additionally proves:

TechnicalEvaluationV1.outcome is passed as evaluation_outcome

TechnicalEvaluationV1.reason_codes is passed unchanged and in-order as evaluation_reason_codes

existing GovernedLifecycleResultV1.downstream remains the result carrier

no status_projection attribute is added

tests/test_cli.py additionally proves both routes:

command_execute captures and passes one snapshot

command_finish captures and passes one snapshot

supplied-guidance execute route still captures snapshot

neither CLI route writes ACTIVE directly

tests/test_system_traversability.py proves:

real S6 evidence exists before constructing S6 PASS

missing real S6 evidence cannot be represented by the production-shaped harness as S6 PASS

check_critical_journey_smoke remains unchanged and pure

## Preserved exclusions

Still do not modify:

src/planning_lite/traversability.py
src/planning_lite/context.py
src/planning_lite/attempt_evaluation.py
src/planning_lite/attempt_runtime.py
src/planning_lite/telemetry.py
src/planning_lite/governed_executor.py
src/planning_lite/operation_trace.py
template/.planning/changes/templates/progress.md
tests/test_operation_trace.py

Change 2 remains separate. Change 3 remains separate.

## Readiness finding adjudication

FR_FINDING_1:
RESOLVED_BY_V3_LIVE_FIELD_BINDING
NON_ARCHITECTURAL

FR_FINDING_2:
RESOLVED_BY_V3_EXISTING_DOWNSTREAM_BINDING
NON_ARCHITECTURAL

FR_FINDING_3:
RESOLVED_BY_V3_SNAPSHOT_INDEPENDENCE_FROM_RESUME_CONTEXT
NON_ARCHITECTURAL

FR_FINDING_4:
RESOLVED_BY_V3_ALL_LIVE_CALLER_COVERAGE
MATERIAL_CORRECTNESS_BINDING / NO_NEW_PATH

FR_FINDING_5:
READINESS_REQUIREMENT_ADJUDICATED_INVALID
TRAVERSABILITY_PURE_REDUCER_BOUNDARY_PRESERVED
NO_TRAVERSABILITY_SOURCE_MUTATION

## Change boundaries

LIFECYCLE_PREREQUISITE:
REOPENED / S6 CORRECTION PLANNED

CHANGE_2:
BLOCKED / VALID / PAUSED

CHANGE_2_FRESH_FORMAL_READINESS:
NOT AUTHORIZED

CHANGE_3:
NOT_ABSORBED

MAJOR_PL09_NEXT_SLICE_GATE:
PRESERVED / UNCONSUMED

## Next gate

After successful v3 materialization:

FRESH_FORMAL_READINESS_PL09_LIFECYCLE_S6_CORRECTION_V3

Still no implementation authorization.

## Materialization boundary

Allowed governance writes only:

docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-AMENDMENT-v3.md
docs/design/project-spine/CURRENT.md

CURRENT receives only a bounded next-gate update from the v2 readiness blocker to:

NEXT_PERMITTED_ACTION:
FRESH_FORMAL_READINESS_PL09_LIFECYCLE_S6_CORRECTION_V3

Do not otherwise clean or reconcile CURRENT.

## Git boundary

Preserve unrelated dirt.

Stage only exact governance paths.

Run git diff --cached --check.

Create one bounded governance commit.

Do not push.

## Materialization result contract

ARCHITECTURE_BLOCKER_COUNT:
0

WRITE_PATH_COUNT:
7

TRAVERSABILITY_SOURCE_MUTATION_PLANNED:
NO

OVERALL:
PASS_S6_PLAN_AMENDMENT_V3_MATERIALIZED

NEXT_SINGLE_GATE:
FRESH_FORMAL_READINESS_PL09_LIFECYCLE_S6_CORRECTION_V3
