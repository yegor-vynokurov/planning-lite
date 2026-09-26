# PL-V39-09-E Read-Only Executor Plan Compiler - Formal Readiness Verdict v2

## 1. Verdict and authority boundary

```text
OPERATION: RUN_AND_MATERIALIZE_09_E_READONLY_PLAN_COMPILER_FORMAL_READINESS_V2
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
FORMAL_READINESS_EXECUTION: COMPLETE / FRESH READ-ONLY EVALUATION
FORMAL_READINESS: READY
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
PRODUCT_IMPLEMENTATION_PERFORMED: NO
ROADMAP_MUTATION_PERFORMED: NO
PUSH: NO
```

This is a fresh v2 evaluation after the owner-approved controlled-discovery
Definition Amendment v2 and Implementation Plan Amendment v1. It is a
governance receipt, not implementation authorization. No T-01 through T-06
task was started, and no product, test, template, roadmap, recommendation,
lifecycle, runtime, or persistence path was modified.

Formal Readiness v1 remains historical. Its blocked result was caused by the
then-unbound controlled-discovery carrier. The owner review supplied for this
run records Definition Amendment v2 and Implementation Plan Amendment v1 as
APPROVED and resolves both the R09 and R14 design blockers.

## 2. Entry identity and authority binding

```text
ENTRY_HEAD: d2ad7c7fe0c3a3250e39debb71e4fcbbb2eda671
EXPECTED_ENTRY_HEAD: d2ad7c7fe0c3a3250e39debb71e4fcbbb2eda671
ENTRY_HEAD_MATCH: YES
ENTRY_INDEX_EMPTY: YES
ENTRY_BRANCH: reconcile/current-design-spine-2026-08-25
ENTRY_UNRELATED_DIRT: 13 pre-existing untracked governance artifacts
ENTRY_UNRELATED_DIRT_PRESERVED: YES
```

The following eight authorities were recomputed from the entry checkout and
matched the supplied effective bindings:

```text
START_CONTRACT:
docs/design/project-spine/checkpoints/PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-START-CONTRACT-v1.md
START_CONTRACT_SHA256: CE499ADAB98A6E0C416AB85BC6411DFD8B77C272242138B42D43415C677514E5

START_CONTRACT_AMENDMENT:
docs/design/project-spine/checkpoints/PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-START-CONTRACT-AMENDMENT-v1.md
START_CONTRACT_AMENDMENT_SHA256: 1E94B8A3C5F956C51BEA6AE7E9FCFB7539BA77360294BB552C10E9A101233842

SEMANTIC_FREEZE:
docs/design/project-spine/checkpoints/PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-SEMANTIC-FREEZE-v1.md
SEMANTIC_FREEZE_SHA256: B582C2DBC8DB46942768C0EB0E7F8367CE4CEC7D457E2430A369903EA7536829

BASE_DEFINITION:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-v1.md
BASE_DEFINITION_SHA256: 6ED1FBD40605EFB5EB5F7689DBF72BA547D18DA289FB4F5A9A8A55CF77EA6A24

DEFINITION_AMENDMENT_V1:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-AMENDMENT-v1.md
DEFINITION_AMENDMENT_V1_SHA256: 40868FFEC03590ACFBEBCC24737B495DFB2429093CA3F3D1D524D3BC24E86797

DEFINITION_AMENDMENT_V2:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-AMENDMENT-v2.md
DEFINITION_AMENDMENT_V2_SHA256: 54C29D42E54C5F04AFF704F9449FA66F78DF5EECD0B1965BAB9913CB5C61F7C4

IMPLEMENTATION_PLAN:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-IMPLEMENTATION-PLAN-v1.md
IMPLEMENTATION_PLAN_SHA256: 9753EC53A123A1B51C7C07E99C90003BE4AA165215FF2BEDEF995D40AC6D5520

IMPLEMENTATION_PLAN_AMENDMENT_V1:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-IMPLEMENTATION-PLAN-AMENDMENT-v1.md
IMPLEMENTATION_PLAN_AMENDMENT_V1_SHA256: A0C67D47C062F4ACE88AFD110432CF231D3E7D7C2399998EC5FAFCA91451D5D5
```

Effective authority is the base Definition plus Amendments v1 and v2, and
the base Implementation Plan plus Amendment v1. The owner gate is
`PASS / APPROVED`; `UNBOUND_MATERIAL_CHOICES` is zero and
`PRODUCT_IMPLEMENTATION_AUTHORIZED` remains `NO`.

## 3. Fresh R01-R08 evaluation

### R01 AUTHORITY_BINDING - PASS

All eight authority paths and SHA-256 identities above match the effective
owner-approved contract. No historical v1 verdict was substituted for the
fresh v2 evaluation.

```text
R01_AUTHORITY_BINDING: PASS
EFFECTIVE_DEFINITION: BASE + AMENDMENT_V1 + AMENDMENT_V2
EFFECTIVE_IMPLEMENTATION_PLAN: BASE + AMENDMENT_V1
OWNER_REVIEW: PASS / APPROVED
```

### R02 SIX_PATH_BUDGET - PASS

The implementation surface remains exactly the six planned paths. There are
no required additional paths, no hidden second-order paths, and no seventh
path introduced for controlled discovery.

```text
EXPECTED_IMPLEMENTATION_PATH_COUNT: 6
STRICTLY_REQUIRED_ADDITIONAL_PATHS: []
HIDDEN_SECOND_ORDER_PATH_COUNT: 0
SEVENTH_PATH: NO
R02_SIX_PATH_BUDGET: PASS
```

### R03 PURE_CORE_BOUNDARY - PASS

The proposed compiler core remains a pure standard-library computation over
explicit inputs. It has no filesystem, Git, network, telemetry, model,
persistence, or import dependency on context, execution guidance, attempt
runtime, attempt evaluation, operation lifecycle, or Project Spine modules.

```text
PURE_CORE: YES
EXTERNAL_SIDE_EFFECTS: NONE
R03_PURE_CORE_BOUNDARY: PASS
```

### R04 TASK_GRAMMAR - PASS

The task row grammar remains the existing canonical seven-column grammar:

```text
ID | Outcome | Slice type | Blocking edge | Verification seam / command | Blast radius | Status
```

The accepted statuses remain `Pending`, `In progress`, `Blocked`, `Done`,
and `Cancelled`. Controlled discovery does not add a task-table column or
alter task status semantics.

```text
R04_TASK_GRAMMAR: PASS
```

### R05 STATUS_AND_CANCELLED_SEMANTICS - PASS

`Cancelled` remains a terminal explicit status and is not inferred from
missing work. Existing status behavior is unchanged; controlled discovery is
an explicit proposal input and does not silently convert a task or unit into
an executable status.

```text
R05_STATUS_AND_CANCELLED_SEMANTICS: PASS
```

### R06_PROPOSAL_AND_FINDINGS - PASS

The controlled-discovery proposal is now bound to one exact top-level shape:

```text
schema_version
source_binding
units
existing_dependency_handoffs
controlled_discoveries
semantic_assessment_source
semantic_evidence_refs
```

`controlled_discoveries` is required, must be an array, and must be explicitly
`[]` when empty. Each entry has exactly these six required nonempty string
fields and no extra keys:

```text
unit_ref
question
scope_bound
stop_condition
output_contract
verification_before_dependent_work
```

The structural validator uses the existing stdlib JSON path and deterministic
ordering. It rejects malformed shape, missing or null discovery arrays,
missing/empty fields, duplicate final-unit references, unknown final-unit
references, invalid derived split references, and extra keys. No semantic
inference or model call is introduced and no second schema subsystem is
required.

The three new material findings are exactly:

```text
INVALID_CONTROLLED_DISCOVERY
UNKNOWN_CONTROLLED_DISCOVERY_UNIT
DUPLICATE_CONTROLLED_DISCOVERY_UNIT
```

```text
R06_PROPOSAL_AND_FINDINGS: PASS
```

### R07_DEPENDENCY_GRAPH - PASS

Existing dependency validation remains a deterministic DAG check. Controlled
discovery is attached to final compiled units and does not create an implicit
graph edge. Invalid cycles, references, and ordering defects remain material
graph findings and continue to block readiness.

```text
R07_DEPENDENCY_GRAPH: PASS
```

### R08_SPLIT_AND_HANDOFF - PASS

KEEP and COUPLED units retain their original IDs. A split unit may reference
only valid derived final IDs; the replaced parent is not a final executable
unit. Existing dependency handoffs remain explicit and are evaluated before
controlled-discovery unit binding.

```text
R08_SPLIT_AND_HANDOFF: PASS
```

## 4. Fresh R09-R16 evaluation

### R09_CONTROLLED_DISCOVERY_COVERAGE - PASS

The controlled-discovery carrier, location, schema, and readiness behavior
are now all bound by the approved amendments:

```text
CONTROLLED_DISCOVERY_LOCATION: BOUND / proposal top-level field
CONTROLLED_DISCOVERY_SCHEMA: BOUND / exact seven-key proposal plus exact six-key entries
CONTROLLED_DISCOVERY_UNIT_BINDING: BOUND / final compiled executable unit
THREE_READINESS_STATES_COMPUTABLE: YES
R09_COVERAGE_READINESS: PASS
```

The compiler returns `controlled_discoveries` in deterministic final-unit
order. Empty controlled discovery plus otherwise-ready work yields `READY`.
One or more valid bounded prerequisites, with every other condition ready,
yields `READY_WITH_CONTROLLED_DISCOVERY`. Any other material defect yields
`NOT_READY`. The proposal cannot override a material defect, and multiple
independent discoveries remain `NOT_READY`.

### R10_THIN_CLI_BOUNDARY - PASS

The CLI remains a thin adapter around explicit JSON input, the pure compiler,
and deterministic result rendering. It does not acquire orchestration,
semantic inference, persistence, or hidden discovery behavior.

```text
R10_THIN_CLI_BOUNDARY: PASS
```

### R11_PATH_SAFETY - PASS

The explicit proposal path policy remains `ALLOW_EXPLICIT_EXTERNAL_PROPOSAL`.
The plan and task surfaces remain TARGET-contained through their explicit
adapter containment policy. Source, source-relative, and external proposal
path handling are distinct, deterministic, and auditable; no ambient
discovery scan or fallback path search is introduced.

```text
PROPOSAL_PATH_POLICY: ALLOW_EXPLICIT_EXTERNAL_PROPOSAL
PLAN_AND_TASK_PATH_POLICY: TARGET_CONTAINED_BY_EXPLICIT_ADAPTER
R11_PATH_SAFETY: PASS
```

### R12_EXIT_CODE_CONTRACT - PASS

The existing exit-code contract remains intact: successful compilation uses
the existing success result, structured non-match remains code `3`, and
unexpected `PlanningLiteError` remains code `2`. Controlled-discovery
findings are represented through the existing structured result path.

```text
R12_EXIT_CODE_CONTRACT: PASS
```

### R13_INTEGRITY_AND_OWNERSHIP - PASS

No project-owned goal, plan, recommendation, decision, active state,
configuration override, or completed work record is overwritten. The
framework ownership and Copier skip boundaries remain respected. No
generated consumer project was edited.

```text
R13_INTEGRITY_AND_OWNERSHIP: PASS
```

### R14_TEST_COVERAGE_AND_READINESS - PASS

The approved plan amendment keeps tests in the existing
`tests/test_plan_compilation.py` path. The fresh required coverage is:

```text
EMPTY_CONTROLLED_DISCOVERY: COVERED
VALID_SINGLE_BOUNDARY_DISCOVERY: COVERED
MISSING_OR_NULL_ARRAY: COVERED
MALFORMED_ENTRY: COVERED
DUPLICATE_FINAL_UNIT: COVERED
UNKNOWN_FINAL_UNIT: COVERED
INVALID_SPLIT_DERIVED_UNIT: COVERED
DETERMINISTIC_FINAL_UNIT_ORDER: COVERED
READINESS_READY: COVERED
READINESS_READY_WITH_CONTROLLED_DISCOVERY: COVERED
READINESS_NOT_READY: COVERED
MULTIPLE_INDEPENDENT_DISCOVERIES: COVERED
EXISTING_TEST_PATHS_ONLY: YES
SEVENTH_TEST_PATH: NO
R14_TEST_COVERAGE_AND_READINESS: PASS
```

### R15_WHOLE_ORGANISM_REGRESSION - PASS

The existing whole-organism owner remains `tests/test_system_traversability.py`.
The recorded Gate A artifact states `ORGANISM_STATE: ORGANISM_PASSING` and
the focused owner/product suite passed. No test file, whole-organism owner,
or unrelated test family was mutated for this governance receipt.

```text
WHOLE_ORGANISM_OWNER: tests/test_system_traversability.py
GATE_A: ORGANISM_PASSING
R15_WHOLE_ORGANISM_REGRESSION: PASS
```

### R16_FALSE_DONE_AND_STOP_CONDITIONS - PASS

The v2 evaluation does not treat structural compilation as proof of semantic
completion. It retains the following false-done stops:

```text
UNRESOLVED_DEPENDENCY: MATERIAL / NOT_READY
MALFORMED_PLAN_OR_TASK_SHAPE: MATERIAL / NOT_READY
INVALID_CONTROLLED_DISCOVERY: MATERIAL / NOT_READY
UNKNOWN_CONTROLLED_DISCOVERY_UNIT: MATERIAL / NOT_READY
DUPLICATE_CONTROLLED_DISCOVERY_UNIT: MATERIAL / NOT_READY
MULTIPLE_INDEPENDENT_DISCOVERIES: MATERIAL / NOT_READY
UNVERIFIED_BOUNDED_PREREQUISITE: MATERIAL / NOT_READY
```

```text
R16_FALSE_DONE_AND_STOP_CONDITIONS: PASS
```

## 5. Six-path and forbidden-path audit

```text
PATH_1: PURE COMPILER CORE / RETAINED
PATH_2: PROPOSAL STRUCTURE AND CONTROLLED-DISCOVERY VALIDATION / BOUND
PATH_3: FINAL-UNIT BINDING AND DETERMINISTIC RESULT / BOUND
PATH_4: READINESS PROJECTION / THREE STATES COMPUTABLE
PATH_5: THIN CLI ADAPTER / RETAINED
PATH_6: EXISTING TEST PATH / tests/test_plan_compilation.py
ADDITIONAL_REQUIRED_PATHS: []
FORBIDDEN_PATH_MUTATION: NO
PRODUCT_CODE_MUTATION: NO
TEST_CODE_MUTATION: NO
TEMPLATE_MUTATION: NO
ROADMAP_MUTATION: NO
CHANGE_3_MUTATION: NO
09_F_OR_09_G_MUTATION: NO
```

## 6. Verification evidence

The focused baseline was rerun from the entry checkout:

```text
FOCUSED_BASELINE_COMMAND: uv run pytest tests/test_cli.py tests/test_field_control_pack_foundation.py tests/test_project_shaping_foundation.py tests/test_direction_foundation.py tests/test_system_traversability.py
FOCUSED_BASELINE_RESULT: 104 passed, 88 warnings
```

The full suite was also rerun:

```text
FULL_BASELINE_COMMAND: uv run pytest
FULL_BASELINE_RESULT: 648 passed, 2 failed, 88 warnings
```

The two failures are the pre-existing
`tests/test_central_resume_contract.py::test_helper_is_read_only_on_actual_checkout`
and `tests/test_central_resume_contract.py::test_current_contains_complete_semantic_resume_state`.
Both fail because the existing `CURRENT.md` resume block contains the extra
keys `formal_readiness`, `first_broken_seam`, `gap_class`, `critical_journey`,
and `change_2`, which the current helper rejects. This v2 governance run did
not repair or otherwise mutate that unrelated baseline defect.

```text
MATERIAL_REGRESSION_INTRODUCED_BY_THIS_RUN: NO
BASELINE_FAILURES_ADJUDICATED: PRE-EXISTING / UNRELATED RESUME-CONTRACT MISMATCH
```

## 7. Final materialization gate

```text
R01: PASS
R02: PASS
R03: PASS
R04: PASS
R05: PASS
R06: PASS
R07: PASS
R08: PASS
R09: PASS
R10: PASS
R11: PASS
R12: PASS
R13: PASS
R14: PASS
R15: PASS
R16: PASS

MATERIAL_BLOCKER_COUNT: 0
UNBOUND_MATERIAL_CHOICE_COUNT: 0
UNBOUND_MATERIAL_CHOICES: []
STRICT_ADDITIONAL_PATHS: []
FORBIDDEN_PATH_MUTATION: NO
FORMAL_READINESS_V2: READY
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
NEXT_SINGLE_GATE: OWNER_REVIEW_09_E_READONLY_PLAN_COMPILER_FORMAL_READINESS_V2
```

The next and only permitted gate is owner review of this v2 artifact. Owner
approval is required before any product implementation authorization or T-01
through T-06 execution. The v1 verdict remains immutable historical evidence;
this artifact is the current fresh readiness projection.
