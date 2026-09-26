# PL-V39-09 09-E Capability-Aware Plan Compilation Semantic Freeze v1

## Bounded slice closeout

```text
SLICE:
09-E-PLAN-COMPILATION-CONTRACT-AND-FIELD-PROOF

SLICE_STATUS:
CLOSED / COMPLETE

09_E_OVERALL:
OPEN / V1 CORE SEMANTICS FROZEN

PRODUCT_IMPLEMENTATION:
NOT YET AUTHORIZED

OWNER_REVIEW_E0:
PASS_WITH_ONE_MATERIAL_SEMANTIC_CORRECTION_REQUIRED

OWNER_REVIEW_E0_B2:
PASS / ACCEPTED

OPEN_MATERIAL_FINDINGS:
0

UNBOUND_MATERIAL_CHOICES:
0
```

Effective authority:

```text
START_CONTRACT:
docs/design/project-spine/checkpoints/PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-START-CONTRACT-v1.md
START_CONTRACT_SHA256:
CE499ADAB98A6E0C416AB85BC6411DFD8B77C272242138B42D43415C677514E5

START_CONTRACT_AMENDMENT:
docs/design/project-spine/checkpoints/PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-START-CONTRACT-AMENDMENT-v1.md
START_CONTRACT_AMENDMENT_SHA256:
1E94B8A3C5F956C51BEA6AE7E9FCFB7539BA77360294BB552C10E9A101233842
```

## Semantic boundary

```text
SEMANTIC_PLAN
!=
EXECUTOR_COMPILED_PLAN
!=
TASK_OR_OPERATION_CAPSULE
```

09-E v1 owns only:

```text
SEMANTIC_PLAN
->
EXECUTOR_COMPILED_PLAN
```

09-F remains separate and unauthorized.

## Capability concepts

```text
AUTHORIZATION_CAPABILITY
= what the operation is permitted to do

WORK_CAPABILITY
= what competence the work requires

EXECUTOR_PROFILE
= how much ambiguity / autonomy / decision load
  an executor may safely handle
```

These are independent dimensions. No one implies either of the others.

## Work Capability v1 core

```text
INTENT_REQUIREMENTS
DOMAIN_SEMANTICS
REPOSITORY_UNDERSTANDING
ARCHITECTURE_INTERFACES
DEPENDENCY_PLANNING
IMPLEMENTATION
TOOL_RUNTIME_OPERATION
VERIFICATION_TEST_DESIGN
SEMANTIC_REVIEW
EVIDENCE_GOVERNANCE
```

```text
CORE_TAXONOMY_FIELD_RESULT: SUFFICIENT_FOR_V1
TAXONOMY_GAPS: NONE
LONG_CONTEXT_SYNTHESIS: ACCEPTED / FIELD-EXERCISED
ESTIMATION_UNCERTAINTY: PROVISIONAL / NOT FIELD-EXERCISED IN E0
RESEARCH_DISCOVERY: PROVISIONAL / NOT FIELD-EXERCISED IN E0
```

Provisional cross-cutting tags are not frozen core categories.

## Executor profiles and readiness

```text
STRONG_AUTONOMOUS
BOUNDED_WORKER
JUNIOR_EXECUTOR
MECHANICAL_EDITOR

EXECUTOR_PROFILE_FIELD_RESULT: SUFFICIENT_FOR_V1
EXECUTOR_PROFILE_GAPS: NONE
```

No vendor/model identity belongs to this contract.

```text
EXECUTOR_READY
EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY
EXECUTOR_NOT_READY
```

```text
NO EXECUTABLE UNIT MAY CONTAIN
AN UNRESOLVED DECISION
THAT EXCEEDS
THE DECLARED DECISION / CAPABILITY ENVELOPE
OF ITS TARGET EXECUTOR PROFILE.
```

Violation yields `EXECUTOR_NOT_READY`, not implicit escalation.

## Dependency, split, and handoff semantics

```text
DEPENDENCY_EDGE_INVENTION: FORBIDDEN
DEPENDENCY_EDGE_LOSS: FORBIDDEN
SILENT_PARALLELISM_LOSS: FORBIDDEN
```

Compilation cannot rewrite Plan semantics. A graph change requires a separate
classified Plan-repair finding.

For an existing edge `U1 -> U2`, a typed handoff may be added without changing
unit count, graph, or split count. A true split changes one original unit `U`
into `U-A -> U-B [-> ...]`, requires a larger compiled-unit count for that
unit, and requires exact new internal handoffs. Without that,
`SPLIT_RECOMMENDED` is invalid.

The six-part split test is:

```text
S1 meaningful capability boundary exists
S2 bounded explicit handoff can carry upstream result
S3 handoff is independently verifiable
S4 downstream need not reconstruct hidden upstream reasoning
S5 authority/dependency/acceptance/failure survive split
S6 split reduces more coordination ambiguity than it creates
```

Allowed dispositions are exactly:

```text
KEEP_UNIT
SPLIT_RECOMMENDED
CAPABILITY_COUPLED
```

Multiple capabilities alone never imply a split.

## Typed handoff v1 minimum

```text
source_unit
target_unit
produced_refs
accepted_output_contract
required_downstream_inputs
authority_constraints
allowed_open_questions
forbidden_decisions
verification_evidence
failure_stop_state
```

A handoff is derived transport/contract information, not authority. Consumers
must resolve current authority through existing owners.

## Coverage and review contract

Every compiled executable unit must cover:

```text
C01 ATOMICITY / PRIMARY COMPLETION BOUNDARY
C02 DEPENDENCY COMPLETENESS AND ORDER
C03 PRECONDITIONS / INPUTS
C04 AUTHORITY AND SCOPE
C05 EXECUTOR DECISION BUDGET
C06 INTERFACE / CONTRACT SUFFICIENCY
C07 WORK-CAPABILITY SIGNATURE
C08 CAPABILITY SPLIT / COUPLING DECISION
C09 TYPED HANDOFF IF REQUIRED
C10 VERIFICATION
C11 EVIDENCE UPDATE
C12 FAILURE / STOP / RECOVERY
C13 DOWNSTREAM CONSISTENCY
```

Every cell is `PASS`, `FAIL`, or `N/A`; no executable unit may be omitted.

Review order is frozen as:

```text
structural lint
-> complete coverage matrix
-> bounded semantic perspective review
-> collect findings
-> merge/deduplicate findings
-> repair
-> rerun SAME coverage matrix
-> adversarial material-seam review
```

`PLAN_DEFECT` and `REVIEW_COVERAGE_FAILURE` remain distinct. Retained material
classes are:

```text
EXECUTOR_PROFILE_MISMATCH
CAPABILITY_SPLIT_ERROR
CAPABILITY_COUPLING_ERROR
HANDOFF_DEFECT
UNCERTAINTY_BLOCKER
TAXONOMY_GAP
DEPENDENCY_EDGE_INVENTION
DEPENDENCY_EDGE_LOSS
PARALLELISM_LOSS
FALSE_CAPABILITY_SPLIT
```

`EXECUTOR_READY` requires all mandatory cells to be `PASS` or justified `N/A`,
no unresolved material cross-unit finding, valid required handoffs, explicit
split/coupling decisions, and no unauthorized graph mutation.

## Field proof: simple plan

```text
CASE_A: PASS
PROCESS_INFLATION: NO
ORIGINAL_UNITS: 5
COMPILED_UNITS: 5
ARTIFICIAL_SPLITS: 0
```

09-E machinery is not itself a reason to create additional units.

## Field proof: true split

```text
FIXTURE: PL-V39-05-C / historical T-02
ORIGINAL_UNIT_COUNT: 1
COMPILED_UNIT_COUNT: 2
S1: PASS
S2: PASS
S3: PASS
S4: PASS
S5: PASS
S6: PASS
DISPOSITION: SPLIT_RECOMMENDED
TYPED_HANDOFF_COUNT: 1
DEPENDENCY_EDGE_INVENTION: NO
DEPENDENCY_EDGE_LOSS: NO
PARALLELISM_LOSS: NO
FALSE_CAPABILITY_SPLIT: NO
```

## Field proof: existing-edge handoffs

```text
T03: depends on T02
T04: depends on T02
T03_AND_T04: PARALLEL / INDEPENDENT
T05: depends on T03 + T04

T03 -> T05 / OperationGuidanceV1
T04 -> T05 / existing procedure-skill-checklist route contract
```

No `T03 -> T04` or `T04 -> T03` edge exists.

## Field proof: coupling

```text
CAPABILITY_COUPLED_UNITS:
C-T03
C-T04
C-T08

FALSE_SPLIT: NO
```

Material shared invariants are Attempt identity, OperationGuidance, invocation
identity, RunReceipt persistence/readback, ObservedResult, terminalization,
PL08 evaluation, and Project Spine handoff/readback.

## Whole-organism compatibility

```text
SELECTED_SMALLEST_SUITABLE_UNIT: C-T04

JUSTIFICATION:
smaller A units stop at PL06 observation;
smaller B units stop at guidance/routing/verification;
C-T03 stops at envelope construction;
C-T04 is the smallest accepted unit spanning the existing governed-operation path.

WHOLE_ORGANISM_INPUTS_AVAILABLE: YES
NEW_AUTHORITY_REQUIRED: NO
NEW_RUNTIME_SEAM_REQUIRED: NO
09_F_AGENTWORKPACK_REQUIRED: NO
```

This proves compatibility, not implementation of 09-E.

## Not frozen by v1 core

```text
automatic executor/model selection
economic routing
cheapest-executor policy
scalar capability score
capability-orderliness/disorder score
DSM thresholds
automatic plan repair
automatic decomposition
multi-agent routing
AgentWorkPacket production schema
Context Compiler
multi-operation orchestration
scheduler/worker
token/cost optimization
universal estimation formula
09-G calibration
```

Estimation/uncertainty integration remains future 09-E work where needed.

## Roadmap boundaries and regression invariant

```text
09_E_OVERALL: OPEN / V1 CORE SEMANTICS FROZEN
09_B: OPEN / PARTIALLY DESIGNED
CHANGE_3: NOT_ABSORBED / DEFERRED CANDIDATE
09_F: OPTIONAL / NOT REQUIRED FOR 09-E V1 PRODUCTIZATION
09_G: OPEN / NOT AUTHORIZED
09_H: FUTURE
```

Any future 09-E product implementation affecting existing organism surfaces
must run the smallest applicable whole-organism regression before closure.
