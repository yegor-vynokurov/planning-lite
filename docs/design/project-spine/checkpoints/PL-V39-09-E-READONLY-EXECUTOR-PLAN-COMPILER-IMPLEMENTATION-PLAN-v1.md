# CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
## Implementation Plan v1

### 1. Plan identity

```text
PLAN_STATUS:
OWNER_PREPARED / READY_FOR_MATERIALIZATION

IMPLEMENTATION_AUTHORIZED:
NO

TARGET:
Planning Lite central repository

EXPECTED_ENTRY_HEAD:
b270b08f9ee5d99274152db4d04448d6dc089632
```

Effective Definition:

```text
PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-v1.md
SHA256:
6ED1FBD40605EFB5EB5F7689DBF72BA547D18DA289FB4F5A9A8A55CF77EA6A24

PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-AMENDMENT-v1.md
SHA256:
40868FFEC03590ACFBEBCC24737B495DFB2429093CA3F3D1D524D3BC24E86797
```

Frozen semantic authority:

```text
PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-SEMANTIC-FREEZE-v1.md
SHA256:
B582C2DBC8DB46942768C0EB0E7F8367CE4CEC7D457E2430A369903EA7536829
```

Plan approval does not authorize implementation.

Separate Formal Readiness and separate implementation authorization remain
required.

---

## 2. Bounded outcome

Implement one read-only Planning Lite product seam:

```text
existing plan.md bytes
+
existing tasks.md bytes
+
explicit UTF-8 JSON CompilationProposalV1
        ->
pure deterministic 09-E compiler
        ->
PlanCompilationResultV1
```

The result is:

```text
DERIVED
NONAUTHORITATIVE
RECONSTRUCTABLE
READ_ONLY
```

No model inference, plan mutation, task mutation, execution, routing or
persistence is introduced.

---

## 3. Architecture

### 3.1 Pure owner module

Add:

```text
src/planning_lite/plan_compilation.py
```

It owns:

```text
09-E value contracts
strict tasks.md table parsing
Blocking edge parsing
proposal validation
DAG construction/validation
split/coupling validation
typed-handoff validation
C01-C13 validation
readiness calculation
deterministic findings
canonical result serialization
```

The module must have:

```text
NO filesystem access
NO Git access
NO network access
NO telemetry
NO model invocation
NO persistence
NO import from CLI
```

It may use Python standard library only unless an already-required package is
demonstrably necessary.

It must not import semantic owners:

```text
context.py
execution_guidance.py
attempt_runtime.py
attempt_evaluation.py
operation_lifecycle.py
project_spine.py
```

09-E consumes compatible identities conceptually but does not acquire their
authority.

### 3.2 Thin CLI adapter

Modify:

```text
src/planning_lite/cli.py
```

Add:

```text
planning-lite plan-compile TARGET
  --plan <exact path>
  --tasks <exact path>
  --proposal <exact JSON path>
```

The CLI owns only:

```text
argument parsing
target/root containment
exact path resolution
UTF-8 byte reads
SHA-256 calculation
duplicate-key-safe JSON loading
pure compiler call
canonical JSON stdout
exit mapping
```

No semantic 09-E rule belongs in CLI.

### 3.3 Managed task-graph contract

Modify only:

```text
template/.planning/changes/templates/tasks.md
```

to document exact `Blocking edge` grammar:

```text
None
T-01
T-01, T-02
T-03, T-07, T-12
```

No range or prose form.

Regenerate only the existing checksum entry in:

```text
template/.planning/framework/SHA256SUMS.txt
```

No manifest mutation.

---

# 30. Implementation task graph

## T-01 - Pure contracts and source/task parser

Dependencies:

```text
approved Plan
Formal Readiness READY
separate owner implementation authorization
```

Writes:

```text
src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
```

Outcome:

```text
immutable contract constants/types
strict tasks table parser
Blocking edge parser
task/status validation
cycle detection
source-binding primitives
```

Required tests:

```text
valid simple graph
multi-edge graph
parallel graph
legacy prose rejection
range rejection
duplicate ID
unknown dependency
self-dependency
cycle
Cancelled fail-closed
deterministic parse
```

Stop:

```text
general Markdown parser needed
context.py helper required
new template schema required
```

## T-02 - Proposal validation and deterministic compiler

Depends on:

```text
T-01 PASS
```

Writes:

```text
src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
```

Outcome:

```text
strict CompilationProposalV1
Work Capability/profile validation
KEEP/COUPLED/SPLIT logic
S1-S6 completeness
existing-edge handoffs
TypedHandoffV1
compiled graph
C01-C13 validation
findings
readiness
PlanCompilationResultV1
```

Required field fixtures:

```text
simple KEEP_UNIT
true 1 -> 2 split
CAPABILITY_COUPLED
parallel siblings -> common dependent
existing-edge handoff
false split
invented edge
lost edge
parallelism loss
coverage omission
controlled discovery
source drift
```

Stop:

```text
semantic inference required
automatic repair required
new authority required
```

## T-03 - Thin CLI integration

Depends on:

```text
T-01 PASS
T-02 PASS
Formal Readiness exact path-safety decision
```

Writes:

```text
src/planning_lite/cli.py
tests/test_cli.py
```

Outcome:

```text
plan-compile parser
exact file reads
duplicate-safe JSON load
hash binding
core call
canonical JSON stdout
0/3/2/1 exit behavior
```

Required tests:

```text
ready -> 0
not ready -> 3 with body
invalid proposal -> 2
source hash mismatch -> 2
read-only repeat
no output file
no target mutation
canonical JSON repeat
```

Stop:

```text
new router/lifecycle needed
automatic source discovery needed
```

## T-04 - Managed Blocking edge grammar clarification

Depends on:

```text
T-01 parser contract stable
```

Writes:

```text
template/.planning/changes/templates/tasks.md
template/.planning/framework/SHA256SUMS.txt
```

Outcome:

```text
exact v1 dependency grammar documented
no new columns
no status change
checksum exact
```

Required verification:

```text
template integrity PASS
tasks.md checksum reproduces
all unrelated checksum rows unchanged
MANIFEST unchanged
```

Stop:

```text
another managed path required
manifest mutation required
```

## T-05 - Integrated read-only product proof

Depends on:

```text
T-01..T-04 PASS
```

Writes:

```text
NONE
```

Run focused stack:

```text
tests/test_plan_compilation.py
tests/test_cli.py
template/foundation integrity tests applicable to tasks.md/SHA256SUMS
```

Then run:

```text
full test suite
```

Required proof:

```text
all six implementation paths exact
no seventh path
pure-core dependency audit
no authority mutation
no persistence
no semantic inference
no automatic repair
```

## T-06 - Whole-organism non-regression

Depends on:

```text
T-05 PASS
```

Writes:

```text
NONE
```

Run existing whole-organism fixture/smoke without changing its test owner.

Prove:

```text
PL06 unchanged
PL07 unchanged
Authoritative Attempt Runtime unchanged
Governed Operation Lifecycle unchanged
RunReceipt behavior unchanged
PL08 unchanged
Project Spine unchanged
09-E result remains upstream derived analysis only
```

No new system fixture is required if existing smoke can establish
non-regression.

If existing smoke cannot prove this without modifying:

```text
tests/test_system_traversability.py
```

STOP for owner adjudication.

---

## 31. Task ordering

```text
T-01
  |
T-02
  |---------+
  |         |
  |         |
T-03       T-04
  |---------+
       |
      T-05
       |
      T-06
```

T-03 and T-04 may proceed independently after their respective prerequisites.

No owner gate is inserted between ordinary implementation tasks.

---

## 32. Formal Readiness matrix

Formal Readiness must explicitly answer:

```text
R01 AUTHORITY_BINDING
effective Definition SHA pair exact

R02 SIX_PATH_BUDGET
exactly six, no hidden path

R03 PURE_CORE_BOUNDARY
plan_compilation.py requires no filesystem/Git/network/model/persistence owner

R04 TASK_TABLE_GRAMMAR
machine grammar complete and template clarification sufficient

R05 STATUS_SEMANTICS
Cancelled fail-closed and other statuses preserved without hidden scheduling

R06 PROPOSAL_SCHEMA
exact JSON shapes implementable without material choice

R07 DAG_PRESERVATION
edge invention/loss/parallelism checks implementable

R08 SPLIT_HANDOFF
true split and existing-edge handoff implementable independently

R09 COVERAGE_READINESS
C01-C13 and three readiness states fully computable

R10 CLI_BINDING
thin command fits existing parser/handler architecture

R11 CLI_PATH_SAFETY
exact safe path behavior resolved without new policy

R12 EXIT_CODES
0/3/2/1 compatible with current command conventions

R13 TEMPLATE_INTEGRITY
tasks.md has one existing checksum row; no MANIFEST change

R14 TESTABILITY
all mandatory fixtures expressible without huge historical documents

R15 WHOLE_ORGANISM_NONREGRESSION
existing smoke sufficient without test-owner mutation

R16 FALSE_DONE_RESISTANCE
a parser-only or CLI-only implementation cannot satisfy readiness
```

Formal Readiness verdict:

```text
READY
```

only when all sixteen pass and:

```text
MATERIAL_BLOCKER_COUNT = 0
UNBOUND_MATERIAL_CHOICE_COUNT = 0
```

---

## 33. Mandatory false-done tests

Readiness and implementation review must reject these deceptive partial states:

```text
module exists but CLI cannot invoke it
CLI exists but source hashes are not checked
proposal parses but duplicate JSON keys are accepted
task table parses but prose Blocking edge is silently guessed
split result exists but original DAG is not preserved
C01-C13 strings exist but omitted cells do not block READY
result says READY because proposal requested READY
Cancelled task silently disappears
template prose changes but checksum is stale
all focused tests pass but product writes a result file
all focused tests pass but 09-E changes lifecycle authority
```

---

## 34. Acceptance criteria

```text
AC01
strict exact source/task/proposal binding

AC02
deterministic strict task graph parser

AC03
fail-closed legacy/freeform dependency grammar

AC04
exact proposal/schema validation

AC05
DAG preservation

AC06
true split validation

AC07
existing-edge handoff validation

AC08
C01-C13 complete coverage

AC09
deterministic three-state readiness

AC10
read-only CLI with exact exit semantics

AC11
managed Blocking edge grammar + exact checksum

AC12
no model inference / repair / routing / persistence

AC13
whole-organism non-regression

AC14
exact six-path implementation surface
```

All 14 must PASS.

---

## 35. Explicit non-goals

Still forbidden:

```text
automatic semantic classification
automatic capability inference
automatic task splitting
automatic plan repair
automatic executor/model selection
economic routing
AgentWorkPacket
Context Compiler
orchestration
scheduler
worker
Change 3 telemetry correction
persistent compiled-plan storage
new authority
```

---

## 36. Governance sequence

```text
materialize this Plan
-> owner Plan review/approval
-> Formal Readiness
-> owner review of Formal Readiness
-> separate implementation authorization
-> T-01..T-06
-> implementation review
-> bounded implementation commit
-> whole-organism post-commit verification
-> Change closure
```

No step implies the next.

---

## 37. Next gate after materialization

```text
OWNER_REVIEW_09_E_READONLY_PLAN_COMPILER_IMPLEMENTATION_PLAN
```

---

## 4. Exact implementation surface

Exactly six paths:

```text
ADD
src/planning_lite/plan_compilation.py

ADD
tests/test_plan_compilation.py

MODIFY
src/planning_lite/cli.py

MODIFY
tests/test_cli.py

MODIFY
template/.planning/changes/templates/tasks.md

MODIFY
template/.planning/framework/SHA256SUMS.txt
```

No seventh path is authorized.

Explicitly read-only:

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

Any required mutation outside the six paths is a STOP.

---

## 5. Core value contracts

Implement immutable JSON-compatible contracts sufficient for:

```text
CompilationProposalV1
PlanCompilationResultV1
OriginalTaskUnitV1
CompiledUnitV1
TypedHandoffV1
CoverageAssertionV1
CompilationFindingV1
ControlledDiscoveryV1
```

Python representation may use frozen dataclasses, immutable mappings or
equivalent.

Exact serialization must be deterministic.

Unknown keys are rejected where the Definition declares an exact schema.

---

## 6. CompilationProposalV1

Top-level exact keys:

```text
schema_version
source_binding
units
existing_dependency_handoffs
semantic_assessment_source
semantic_evidence_refs
```

Require:

```text
schema_version = 1
```

### 6.1 source_binding

Exact keys:

```text
plan_ref
plan_sha256
tasks_ref
tasks_sha256
```

SHA values may be supplied in upper or lower hexadecimal case.

Comparison is case-insensitive.

Canonical emitted SHA form:

```text
lowercase hexadecimal
```

### 6.2 units

Each entry exact keys:

```text
original_unit_id
work_capabilities
cross_cutting_tags
target_executor_profile
already_decided
allowed_executor_decisions
forbidden_executor_decisions
disposition
derived_units
new_internal_edges
internal_handoffs
criterion_assertions
material_findings
```

No omitted original executable unit is legal.

No unknown original unit is legal.

---

## 7. Proposal JSON parser boundary

CLI JSON loading must reject duplicate keys.

Use a bounded duplicate-key detector through:

```text
json.loads(..., object_pairs_hook=...)
```

or equivalent.

Reject:

```text
duplicate object keys
invalid UTF-8
non-object top level
missing required keys
unknown exact-schema keys
unsupported schema_version
```

These map to:

```text
PROPOSAL_SCHEMA_INVALID
```

or the nearest exact input finding where applicable.

The pure core must also defensively validate an already-parsed mapping.

---

## 8. tasks.md parser

The pure module receives task Markdown text.

It locates exactly one task table with exact columns:

```text
ID
Outcome
Slice type
Blocking edge
Verification seam / command
Blast radius
Status
```

Reject:

```text
missing task table
multiple eligible task tables
missing column
extra column
duplicate task ID
malformed task ID
unknown status
malformed row
```

Task ID grammar:

```text
T-[0-9]{2,}
```

Supported status exactly:

```text
Pending
In progress
Blocked
Done
Cancelled
```

No general-purpose Markdown parser is introduced.

---

## 9. Blocking edge parser

After supported Markdown inline-code unwrapping and outer-whitespace removal:

```text
None
```

or exact comma-separated known task IDs.

Reject:

```text
range syntax
prose
slash syntax
plus syntax
unknown ID
duplicate dependency
self dependency
```

Cycle detection is mandatory after all edges are parsed.

Canonical dependency order follows source task-table row order.

---

## 10. Status handling

Preserve source status on original unit projection.

For:

```text
Pending
In progress
Blocked
Done
```

status does not alter DAG and does not independently alter semantic 09-E
readiness.

For:

```text
Cancelled
```

emit:

```text
UNSUPPORTED_CANCELLED_TASK_STATE
```

as a material finding.

Final readiness cannot be:

```text
EXECUTOR_READY
```

when any source task is Cancelled.

No downstream rewiring is inferred.

---

## 11. Source identity

CLI computes hashes from exact file bytes.

Before semantic compilation require exact match with proposal:

```text
plan_ref
plan_sha256
tasks_ref
tasks_sha256
```

A mismatch emits:

```text
SOURCE_IDENTITY_MISMATCH
```

No nearest/latest/history fallback.

The core receives actual source refs/hashes from adapter inputs and compares
them with proposal binding.

---

## 12. Work Capability validation

Core exact values:

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

Accepted field-exercised cross-cutting tag:

```text
LONG_CONTEXT_SYNTHESIS
```

Allow provisional:

```text
ESTIMATION_UNCERTAINTY
RESEARCH_DISCOVERY
```

but preserve them as provisional tags in result provenance.

Unknown value:

```text
PROPOSAL_SCHEMA_INVALID
```

for v1.

---

## 13. Executor profiles

Exact values:

```text
STRONG_AUTONOMOUS
BOUNDED_WORKER
JUNIOR_EXECUTOR
MECHANICAL_EDITOR
```

No provider/model/runtime mapping exists.

---

## 14. Disposition validation

Exact:

```text
KEEP_UNIT
CAPABILITY_COUPLED
SPLIT_RECOMMENDED
```

For KEEP_UNIT / CAPABILITY_COUPLED:

```text
derived_units = []
new_internal_edges = []
internal_handoffs = []
```

Otherwise emit:

```text
INVALID_SPLIT_STRUCTURE
```

---

## 15. True split validation

For SPLIT_RECOMMENDED require:

```text
>= 2 derived_units
>= 1 new_internal_edge
required internal typed handoff(s)
all S1-S6 PASS
```

Derived unit IDs must be unique inside the proposal and must not collide with
original task IDs.

New internal edges may connect only derived units of that same original unit.

A split may not introduce dependencies between unrelated original units.

Same-count/relabel-only split emits:

```text
FALSE_CAPABILITY_SPLIT
```

---

## 16. S1-S6 representation

Proposal must provide explicit six assertions for every SPLIT_RECOMMENDED unit:

```text
S1 PASS
S2 PASS
S3 PASS
S4 PASS
S5 PASS
S6 PASS
```

No `N/A` for a true split.

The core validates completeness and allowed values.

It does not independently infer semantic truth of S1-S6.

Their provenance remains:

```text
semantic planner assertion
```

---

## 17. Existing-edge handoffs

Each top-level `existing_dependency_handoffs` entry must correspond to an
actual original DAG edge.

Reject handoff where:

```text
edge absent
source unknown
target unknown
source == target
```

with:

```text
HANDOFF_EDGE_MISMATCH
```

Adding such a handoff never changes the original graph.

---

## 18. TypedHandoffV1

Exact semantic keys:

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

All keys required.

Plural fields must be arrays.

No additional authority is inferred.

---

## 19. Original DAG preservation

Construct:

```text
original_graph
```

only from parsed `tasks.md`.

Construct:

```text
compiled_graph
```

by replacing only legitimate split units with their internal derived graph.

For every original external edge, connect the applicable compiled boundary
without changing semantic reachability.

Verification must explicitly detect:

```text
DEPENDENCY_EDGE_INVENTION
DEPENDENCY_EDGE_LOSS
PARALLELISM_LOSS
```

No ordinary v1 proposal may repair the original DAG.

---

## 20. Coverage assertions

Every final compiled executable unit must carry exact C01-C13 assertions.

Exact criterion identities:

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

Each assertion has at minimum:

```text
criterion
verdict
reason
evidence_refs
```

Verdict:

```text
PASS
FAIL
N/A
```

Missing criterion:

```text
COVERAGE_INCOMPLETE
```

Unknown or duplicate criterion:

```text
INVALID_CRITERION_VALUE
```

---

## 21. Controlled discovery

For a compiled unit that results in:

```text
EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY
```

require:

```text
question
scope_bound
stop_condition
output_contract
verification_before_dependent_work
```

No blank or generic value.

An invalid discovery contract prevents that readiness state.

---

## 22. Readiness calculation

The core computes readiness.

Proposal cannot dictate final readiness.

### EXECUTOR_READY

Only when:

```text
all executable units covered
all mandatory C01-C13 = PASS or justified N/A
no unresolved material finding
DAG preserved
split/coupling structure valid
required handoffs valid
no executor-profile contradiction
no Cancelled task
no controlled-discovery requirement
```

### EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY

Only when the only remaining bounded condition is one or more valid controlled-
discovery contracts and no other material structural finding exists.

### EXECUTOR_NOT_READY

All other valid compilation outcomes.

Malformed input is not a readiness state.

It is an input failure.

---

## 23. Finding severity

Every finding has:

```text
finding_code
material
unit_ref
evidence
message
```

For frozen structural classes in this Change:

```text
material = true
```

except a future explicitly nonblocking diagnostic, which v1 does not need to
introduce.

Do not build a general severity subsystem.

---

## 24. Deterministic finding classes

At minimum:

```text
SOURCE_IDENTITY_MISMATCH
UNKNOWN_ORIGINAL_UNIT
OMITTED_EXECUTABLE_UNIT

UNSUPPORTED_TASK_GRAPH_GRAMMAR
MALFORMED_TASK_ID
DUPLICATE_TASK_ID
UNKNOWN_DEPENDENCY_TASK
SELF_DEPENDENCY
TASK_GRAPH_CYCLE
UNSUPPORTED_CANCELLED_TASK_STATE

DEPENDENCY_EDGE_INVENTION
DEPENDENCY_EDGE_LOSS
PARALLELISM_LOSS

FALSE_CAPABILITY_SPLIT
INVALID_SPLIT_STRUCTURE
INVALID_COUPLING_DECLARATION

MISSING_REQUIRED_HANDOFF
INVALID_HANDOFF
HANDOFF_EDGE_MISMATCH

COVERAGE_INCOMPLETE
INVALID_CRITERION_VALUE

EXECUTOR_PROFILE_MISMATCH
READINESS_CONTRADICTION

UNRESOLVED_MATERIAL_FINDING
PROPOSAL_SCHEMA_INVALID
```

No dynamic registry.

---

## 25. PlanCompilationResultV1

Canonical result contains:

```text
schema_version
source_binding
proposal_sha256
original_graph
compiled_graph
compiled_units
existing_edge_handoffs
internal_split_handoffs
coverage
findings
readiness
semantic_assertion_provenance
```

Require:

```text
schema_version = 1
```

Canonical JSON:

```text
sort_keys = true
ensure_ascii = false
separators = (",", ":")
newline at CLI end
```

Repeated identical input must be byte-identical.

---

## 26. CLI exit codes

Freeze:

```text
EXECUTOR_READY
-> 0

EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY
or
EXECUTOR_NOT_READY
-> 3

invalid input / malformed proposal / source binding failure
-> 2

internal 09-E contract invariant failure
-> 1
```

`3` is a structured valid non-ready result.

`2` follows existing Planning Lite malformed/user-input convention.

`1` is reserved for an unexpected compiler contract failure, not a normal
finding.

---

## 27. CLI path safety

All three paths:

```text
--plan
--tasks
--proposal
```

must resolve from explicit user input.

`--plan` and `--tasks` must remain under TARGET.

For `--proposal`, Formal Readiness must inspect the existing CLI path-safety
convention and choose the smallest compatible behavior:

```text
ALLOW_EXPLICIT_EXTERNAL_PROPOSAL
```

or:

```text
REQUIRE_PROPOSAL_UNDER_TARGET
```

This is a live binding question, not an owner semantic choice.

No source scan or discovery is allowed.

If resolving it requires a new path-security policy, Formal Readiness fails.

---

## 28. Template contract

`tasks.md` documentation must make these facts explicit:

```text
Blocking edge accepts only:
None
one task ID
comma-separated task IDs

No prose or ranges.
```

Do not add new table columns.

Do not alter status values.

---

## 29. Checksum update

After final exact `tasks.md` bytes:

```text
compute canonical repository SHA-256
replace only existing tasks.md checksum row
preserve all unrelated SHA256SUMS entries byte-semantically
verify reproduction
```

No manifest mutation.
