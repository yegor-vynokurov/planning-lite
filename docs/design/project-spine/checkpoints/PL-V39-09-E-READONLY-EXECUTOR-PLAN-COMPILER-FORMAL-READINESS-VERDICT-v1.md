# PL-V39-09-E Read-Only Executor Plan Compiler - Formal Readiness Verdict v1

## 1. Verdict and authority boundary

```text
OPERATION: RUN_AND_MATERIALIZE_09_E_READONLY_PLAN_COMPILER_FORMAL_READINESS_V1
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
FORMAL_READINESS_EXECUTION: COMPLETE / READ-ONLY EVALUATION
FORMAL_READINESS: BLOCKED
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
PRODUCT_IMPLEMENTATION_PERFORMED: NO
ROADMAP_MUTATION_PERFORMED: NO
PUSH: NO
```

This artifact records the bounded Formal Readiness evaluation. It is evidence,
not implementation authorization. No T-01 through T-06 task was started, and
no product, test, template, roadmap, recommendation, lifecycle, or runtime
path was modified.

## 2. Entry identity and authority binding

```text
ENTRY_HEAD: fe322174a04e728fc6811d3820da79493285c72c
EXPECTED_ENTRY_HEAD: fe322174a04e728fc6811d3820da79493285c72c
ENTRY_HEAD_MATCH: YES
ENTRY_INDEX_EMPTY: YES
ENTRY_BRANCH: reconcile/current-design-spine-2026-08-25
ENTRY_UNRELATED_DIRT: 13 pre-existing untracked governance artifacts
ENTRY_UNRELATED_DIRT_PRESERVED: YES
```

Exact authority identities recomputed from the checkout:

```text
BASE_DEFINITION:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-v1.md
BASE_DEFINITION_SHA256: 6ED1FBD40605EFB5EB5F7689DBF72BA547D18DA289FB4F5A9A8A55CF77EA6A24

DEFINITION_AMENDMENT:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-AMENDMENT-v1.md
DEFINITION_AMENDMENT_SHA256: 40868FFEC03590ACFBEBCC24737B495DFB2429093CA3F3D1D524D3BC24E86797

SEMANTIC_FREEZE:
docs/design/project-spine/checkpoints/PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-SEMANTIC-FREEZE-v1.md
SEMANTIC_FREEZE_SHA256: B582C2DBC8DB46942768C0EB0E7F8367CE4CEC7D457E2430A369903EA7536829

IMPLEMENTATION_PLAN:
docs/design/project-spine/checkpoints/PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-IMPLEMENTATION-PLAN-v1.md
IMPLEMENTATION_PLAN_SHA256: 9753EC53A123A1B51C7C07E99C90003BE4AA165215FF2BEDEF995D40AC6D5520
```

The run request supplied the owner gate status `CURRENT_PLAN_STATE: APPROVED`
and `FORMAL_READINESS: AUTHORIZED`. The pre-entry CURRENT projection still
carried the prior `PREPARED / AWAITING OWNER REVIEW` wording; the bounded
CURRENT update below records the supplied owner status and this verdict. No
historical or proposed artifact substituted for the four hashed authorities.

## 3. R01-R04: authority, path budget, core, and task grammar

### R01 AUTHORITY_BINDING

```text
BASE_DEFINITION_SHA: PASS
DEFINITION_AMENDMENT_SHA: PASS
SEMANTIC_FREEZE_SHA: PASS
IMPLEMENTATION_PLAN_SHA: PASS
CURRENT_PLAN_STATE: APPROVED / OWNER-SUPPLIED GATE STATUS
R01_AUTHORITY_BINDING: PASS
```

The effective Definition is the base Definition plus Amendment v1, and the
semantic freeze and Implementation Plan hashes match exactly.

### R02 SIX_PATH_BUDGET

```text
EXPECTED_IMPLEMENTATION_PATH_COUNT: 6
STRICTLY_REQUIRED_ADDITIONAL_PATHS: []
HIDDEN_SECOND_ORDER_PATH_COUNT: 0
R02_SIX_PATH_BUDGET: PASS
```

The exact future surface is:

```text
ADD     src/planning_lite/plan_compilation.py
ADD     tests/test_plan_compilation.py
MODIFY  src/planning_lite/cli.py
MODIFY  tests/test_cli.py
MODIFY  template/.planning/changes/templates/tasks.md
MODIFY  template/.planning/framework/SHA256SUMS.txt
```

The package already discovers source modules under `src/planning_lite`, the
test tree needs no registration file, and the task-template change needs only
the existing checksum row. No new helper, manifest, persistence, or
documentation path is strictly required.

### R03 PURE_CORE_BOUNDARY

```text
PURE_CORE_IMPLEMENTABLE: YES
FORBIDDEN_OWNER_IMPORT_REQUIRED: NO
R03_PURE_CORE_BOUNDARY: PASS
```

The proposed module can own frozen value contracts, strict Markdown-table and
dependency parsing, proposal validation, graph checks, findings, readiness,
and canonical serialization using only Python standard-library facilities.
It need not import `context.py`, `execution_guidance.py`, `attempt_runtime.py`,
`attempt_evaluation.py`, `operation_lifecycle.py`, or `project_spine.py`; nor
does it need filesystem, Git, network, telemetry, model, or persistence access.

### R04 TASK_TABLE_GRAMMAR

```text
CURRENT_TASK_TABLE_COLUMNS:
ID | Outcome | Slice type | Blocking edge | Verification seam / command | Blast radius | Status
TASK_TABLE_COLUMNS_COMPATIBLE: YES
GRAMMAR_IMPLEMENTABLE_WITHOUT_HEURISTICS: YES
NEW_COLUMN_REQUIRED: NO
R04_TASK_TABLE_GRAMMAR: PASS
```

The live managed template has exactly the seven required columns. The Amendment
grammar is directly parseable after only the authorized inline-code unwrapping
and outer-whitespace removal:

```text
None
TASK_ID
TASK_ID, TASK_ID[, TASK_ID...]
TASK_ID := T-[0-9]{2,}
```

## 4. R05-R09: status, proposal, graph, split, and readiness semantics

### R05 STATUS_SEMANTICS

```text
EXACT_STATUS_VOCABULARY: Pending | In progress | Blocked | Done | Cancelled
STATUS_CONTRACT_IMPLEMENTABLE: YES
HIDDEN_LIFECYCLE_POLICY_REQUIRED: NO
R05_STATUS_SEMANTICS: PASS
```

The first four statuses remain source metadata, preserve the task graph, and do
not independently alter semantic 09-E readiness. `Cancelled` produces the
material `UNSUPPORTED_CANCELLED_TASK_STATE` finding and cannot yield
`EXECUTOR_READY`; no downstream repair or lifecycle policy is inferred.

### R06 PROPOSAL_SCHEMA

```text
PROPOSAL_TOP_LEVEL_KEYS:
schema_version | source_binding | units | existing_dependency_handoffs | semantic_assessment_source | semantic_evidence_refs
PROPOSAL_SCHEMA_IMPLEMENTABLE: YES
NEW_SCHEMA_LIBRARY_REQUIRED: NO
R06_PROPOSAL_SCHEMA: PASS
```

The Plan binds `schema_version = 1`, exact source-binding keys, exact unit
keys, and exact typed-handoff keys. Python standard-library UTF-8 decoding,
`json.loads`, an `object_pairs_hook` duplicate-key detector, exact-key checks,
version checks, and canonical sorted JSON are sufficient. The unresolved
controlled-discovery attachment is recorded under R09; it is not silently
resolved here by adding a proposal key.

### R07 DAG_PRESERVATION

```text
DEPENDENCY_EDGE_INVENTION_DETECTABLE: YES
DEPENDENCY_EDGE_LOSS_DETECTABLE: YES
PARALLELISM_LOSS_DETECTABLE: YES
UNKNOWN_DEPENDENCY_TASK_DETECTABLE: YES
SELF_DEPENDENCY_DETECTABLE: YES
TASK_GRAPH_CYCLE_DETECTABLE: YES
DAG_PRESERVATION_IMPLEMENTABLE: YES
R07_DAG_PRESERVATION: PASS
```

The original graph is deterministically reconstructed only from the accepted
task table. A compiled graph can replace only validated split units, compare
external edges and reachability, and reject invented/lost edges or reduced
parallelism. No semantic inference is required.

### R08 SPLIT_HANDOFF

```text
EXISTING_DEPENDENCY_HANDOFF != CAPABILITY_SPLIT: YES
TRUE_SPLIT_IMPLEMENTABLE: YES
EXISTING_EDGE_HANDOFF_IMPLEMENTABLE: YES
SEMANTIC_CONFLATION_REQUIRED: NO
R08_SPLIT_HANDOFF: PASS
```

The Plan requires a true split to have one original unit, at least two derived
units, new internal edges, typed internal handoffs, and explicit S1-S6 PASS
assertions. Existing-edge handoffs retain unit count, the original DAG, and
parallelism and are checked against actual original edges.

### R09 COVERAGE_READINESS

```text
C01_C13_IMPLEMENTABLE: YES
READINESS_COMPUTABLE: NO
SEMANTIC_MODEL_CALL_REQUIRED: NO
R09_COVERAGE_READINESS: FAIL
```

The Plan fully names C01-C13, their `PASS`/`FAIL`/`N/A` values, missing-cell
finding behavior, and the three computed readiness states. However, its exact
`CompilationProposalV1.units[]` key set contains no `controlled_discovery`
field, and no nested schema or other bound location carries the five required
fields for `ControlledDiscoveryV1`:

```text
question
scope_bound
stop_condition
output_contract
verification_before_dependent_work
```

Those fields are required by the Plan's controlled-discovery section and by the
mandatory T-02 fixture, but attaching them to `allowed_executor_decisions`,
`already_decided`, or a newly invented key would be a material schema choice.
Therefore the controlled-discovery state cannot be computed or tested exactly
from the approved Plan without owner adjudication or a Plan amendment.

## 5. R10-R16: live bindings, integrity, fixtures, organism proof, and false-done resistance

### R10 CLI_BINDING

```text
THIN_CLI_BINDING: PASS
NEW_ROUTER_REQUIRED: NO
R10_CLI_BINDING: PASS
```

The existing `argparse` subcommand architecture and `main` dispatch support the
frozen `plan-compile TARGET --plan --tasks --proposal` adapter without a router
or lifecycle subsystem.

### R11 CLI_PATH_SAFETY

```text
PROPOSAL_PATH_POLICY: ALLOW_EXPLICIT_EXTERNAL_PROPOSAL
BINDING_SOURCE: src/planning_lite/cli.py explicit --input JSON convention
NEW_PATH_SECURITY_POLICY_REQUIRED: NO
R11_CLI_PATH_SAFETY: PASS
```

Existing `command_attempt_prepare`, `command_execute`, `command_finish`,
`command_resume`, and `command_receipt` handlers read explicitly supplied JSON
paths without source discovery or target-root association. The frozen Plan
separately requires `--plan` and `--tasks` to resolve under TARGET; that is a
bounded adapter containment check, not a new proposal policy. No scan,
latest-file, same-Change, mtime, or history association is authorized.

### R12 EXIT_CODES

```text
EXIT_CODE_CONTRACT_COMPATIBLE: YES
R12_EXIT_CODES: PASS
```

The current CLI already returns structured success/non-success values and maps
malformed user input through `PlanningLiteError` to exit code 2. The Plan's
0-ready, 3-valid-not-ready, 2-invalid-input, and 1-unexpected-contract-error
mapping fits that architecture; code 3 is already used for a structured
non-match result.

### R13 TEMPLATE_INTEGRITY

```text
TASKS_CHECKSUM_ENTRY_EXISTS: YES
TASKS_CHECKSUM_ENTRY_UNIQUE: YES
MANIFEST_UPDATE_REQUIRED: NO
SECOND_INTEGRITY_PATH_REQUIRED: NO
R13_TEMPLATE_INTEGRITY: PASS
```

`template/.planning/framework/SHA256SUMS.txt` has exactly one tasks-template
row. The live canonical-LF checksum is
`5296dc6953bee108ee3794d8fa6e9d5ce9115ecede5fffb5b1c5aa1f1e1e636a`.
The path is already present in `MANIFEST_V4`; only the existing checksum row
would be replaced after the authorized template clarification.

### R14 TESTABILITY

```text
FOCUSED_FIXTURES_SUFFICIENT: NO
R14_TESTABILITY: FAIL
```

Compact synthetic fixtures cover the listed graph, split, handoff, status,
source-binding, duplicate-key, determinism, read-only, and false-done cases.
The mandatory controlled-discovery fixture is not expressible without choosing
where its five-field contract lives in the proposal. This is the same single
root blocker as R09, not a request for a seventh test path.

### R15 WHOLE_ORGANISM_NONREGRESSION

```text
EXISTING_WHOLE_ORGANISM_SMOKE_SUFFICIENT: YES
EXACT_EXISTING_TESTS_OR_SMOKE:
- tests/test_system_traversability.py
- docs/design/project-spine/checkpoints/PL-V39-09-WHOLE-ORGANISM-GATE-A-REVIEW-v1.md
TEST_OWNER_MUTATION_REQUIRED: NO
R15_WHOLE_ORGANISM_NONREGRESSION: PASS
```

The existing traversability family exercises the self-hosted governed path,
Attempt Runtime access, guidance/lifecycle entrypoints, receipt and PL08
identity carriers, Project Spine handoff, closed-boundary assertions, and
read-only template integrity. Gate A records `ORGANISM_STATE: ORGANISM_PASSING`,
185 focused passes, and 648 full-suite passes with two known unrelated
failures. The requested `tests/test_system_traversability.py` owner was not
modified.

### R16 FALSE_DONE_RESISTANCE

```text
FALSE_DONE_RESISTANCE: PASS
R16_FALSE_DONE_RESISTANCE: PASS
```

The Plan's mandatory false-done matrix rejects an unreachable module, missing
source hashes, duplicate JSON keys, guessed prose dependencies, DAG-changing
splits, omitted coverage, proposal-supplied readiness, disappearing
`Cancelled` tasks, stale checksums, result persistence, and lifecycle-authority
mutation. The R09 schema gap prevents readiness overall but does not erase the
Plan's explicit rejection obligations for the listed deceptive states.

## 6. Path-budget false-positive audit

```text
FORBIDDEN_PATH_MUTATION_REQUIRED: NO
```

The following remain mutation-forbidden and were not changed:

```text
src/planning_lite/context.py
src/planning_lite/execution_guidance.py
src/planning_lite/attempt_runtime.py
src/planning_lite/attempt_evaluation.py
src/planning_lite/operation_lifecycle.py
src/planning_lite/project_spine.py
src/planning_lite/traversability.py
tests/test_system_traversability.py
template/.planning/docs/MANIFEST_V4.md
```

## 7. Baseline regression disposition

```text
BASELINE_FOCUSED_TESTS:
uv run pytest tests/test_cli.py tests/test_field_control_pack_foundation.py tests/test_project_shaping_foundation.py tests/test_direction_foundation.py tests/test_system_traversability.py
RESULT: 104 passed

BASELINE_FULL_SUITE:
uv run pytest
RESULT: 648 passed, 2 failed

BASELINE_FAILURE_DISPOSITION: PREEXISTING_UNRELATED_FAILURE
```

The two full-suite failures are:

```text
tests/test_central_resume_contract.py::test_helper_is_read_only_on_actual_checkout
tests/test_central_resume_contract.py::test_current_contains_complete_semantic_resume_state
```

They fail because the pre-existing CURRENT resume block contains the repository's
extra semantic keys (`formal_readiness`, `first_broken_seam`, `gap_class`,
`critical_journey`, and `change_2`) that the current helper rejects. Repairing
that unrelated contract would require out-of-scope changes and was not done.
`uv sync --locked` also completed successfully.

## 8. Material blockers and final verdict

```text
MATERIAL_BLOCKER_COUNT: 1
MATERIAL_BLOCKERS:
1. CONTROLLED_DISCOVERY_PROPOSAL_CARRIER_UNBOUND
   The approved Plan requires a controlled-discovery readiness state and fixture
   but does not bind the five-field ControlledDiscoveryV1 contract to any exact
   CompilationProposalV1 field or nested schema. Resolving that requires owner
   adjudication or a Plan amendment; this readiness gate does not invent it.

UNBOUND_MATERIAL_CHOICE_COUNT: 1
UNBOUND_MATERIAL_CHOICES:
1. The proposal location and exact schema for controlled-discovery contracts.

STRICTLY_REQUIRED_ADDITIONAL_PATHS: []
FORMAL_READINESS: BLOCKED
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
```

## 9. Materialization and next gate

```text
FORMAL_READINESS_ARTIFACT: THIS FILE
PRODUCT_MUTATIONS: NONE
TEST_MUTATIONS: NONE
TEMPLATE_MUTATIONS: NONE
ROADMAP_MUTATIONS: NONE
RECOMMENDATION_MUTATIONS: NONE
STAGED_GOVERNANCE_PATHS: THIS FILE and docs/design/project-spine/CURRENT.md
COMMIT_SCOPE: exactly the two governance paths above
PUSH: NO

NEXT_SINGLE_GATE: OWNER_ADJUDICATION_09_E_READONLY_PLAN_COMPILER_READINESS_BLOCKER
OVERALL: BLOCKED_09_E_READONLY_PLAN_COMPILER_FORMAL_READINESS
```
