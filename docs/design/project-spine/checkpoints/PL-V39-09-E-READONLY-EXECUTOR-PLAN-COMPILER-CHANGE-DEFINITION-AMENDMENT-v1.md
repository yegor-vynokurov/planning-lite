# CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
## Change Definition Amendment v1

### Status

```text
AMENDMENT_STATUS:
PREPARED / AWAITING_OWNER_MATERIALIZATION

BASE_DEFINITION_SHA256:
6ED1FBD40605EFB5EB5F7689DBF72BA547D18DA289FB4F5A9A8A55CF77EA6A24

SCOPE_CHANGE:
NO

GOAL_CHANGE:
NO

SELECTED_ARCHITECTURE_CHANGE:
NO

PRODUCT_IMPLEMENTATION_AUTHORIZED:
NO
```

This Amendment closes the material omissions discovered by the read-only
Definition review.

Effective Definition after approval is:

```text
Change Definition v1
+
Change Definition Amendment v1
```

## 1. Complete authority binding

The effective Definition binds all three 09-E semantic authorities:

```text
PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-START-CONTRACT-v1.md
SHA256:
CE499ADAB98A6E0C416AB85BC6411DFD8B77C272242138B42D43415C677514E5

PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-START-CONTRACT-AMENDMENT-v1.md
SHA256:
1E94B8A3C5F956C51BEA6AE7E9FCFB7539BA77360294BB552C10E9A101233842

PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-SEMANTIC-FREEZE-v1.md
SHA256:
B582C2DBC8DB46942768C0EB0E7F8367CE4CEC7D457E2430A369903EA7536829
```

No later Plan may weaken any of these contracts.

## 2. Selected architecture remains unchanged

Exactly:

```text
EXPLICIT SEMANTIC PROPOSAL
+
PURE DETERMINISTIC READ-ONLY COMPILER
```

The product core performs no LLM/model semantic inference.

It does not infer:

```text
Work Capability
Executor Profile
split suitability
capability coupling
semantic completeness
Plan repair
```

from arbitrary prose.

## 3. Blocking-edge grammar v1

The current managed `tasks.md` template requires one minimal contract
clarification.

For future managed task surfaces, `Blocking edge` uses this exact semantic
grammar after Markdown inline-code unwrapping and outer-whitespace removal:

```text
None
```

or:

```text
TASK_ID
```

or:

```text
TASK_ID, TASK_ID[, TASK_ID...]
```

where:

```text
TASK_ID := T-[0-9]{2,}
```

Examples:

```text
None
T-01
T-01, T-02
T-03, T-07, T-12
```

Not legal:

```text
T-01–T-04
T-01 through T-04
after owner approval
test failures stop dependent slices
T-01/T-02
T-01 + T-02
any prose dependency description
```

## 4. Dependency parser rules

The v1 parser must:

```text
strip only the explicitly supported Markdown inline-code wrapper
parse exact comma-separated task IDs
reject malformed IDs
reject duplicate IDs within one dependency cell
reject self-dependency
reject dependency references to unknown task IDs
detect graph cycles
preserve all legal original external edges
preserve original parallelism
```

For a syntactically valid multi-edge cell, output dependency ordering is
canonicalized by source task-table row order.

The input order itself is not semantic authority.

## 5. Historical/freeform compatibility

No heuristic compatibility parser is authorized.

A legacy/freeform dependency cell yields:

```text
UNSUPPORTED_TASK_GRAPH_GRAMMAR
```

and the compilation result cannot be `EXECUTOR_READY`.

No:

```text
range expansion
keyword interpretation
natural-language dependency inference
best-effort ID extraction
```

is permitted.

There is currently no requirement to migrate historical prose-bearing Planning
documents merely to satisfy this Change.

## 6. Managed-template clarification

The future implementation is authorized to clarify only the existing `Blocking
edge` contract in:

```text
template/.planning/changes/templates/tasks.md
```

The template must document the v1 grammar above.

This is a contract clarification, not a new authority or schema subsystem.

Because this managed template changes, update only its existing entry in:

```text
template/.planning/framework/SHA256SUMS.txt
```

No manifest path is added or removed.

No `MANIFEST_V4.md` mutation is required unless later Formal Readiness proves
otherwise.

If another integrity path becomes strictly required, implementation stops for
owner adjudication.

## 7. Task-status semantics v1

Accepted source status values remain exactly:

```text
Pending
In progress
Blocked
Done
Cancelled
```

09-E v1 distinguishes:

```text
SEMANTIC EXECUTOR READINESS
```

from:

```text
CURRENT RUNTIME EXECUTION ELIGIBILITY
```

These are not the same concept.

### Pending / In progress / Blocked / Done

For v1 plan compilation:

```text
all remain source task nodes
status is preserved as source metadata
status does not add/remove dependency edges
status does not grant authority
status does not by itself change 09-E EXECUTOR_READY
```

`Blocked` propagation and current execution eligibility remain owned by the
existing lifecycle/runtime surfaces.

`Done` does not cause the compiler to delete the unit or rewrite the historical
graph.

### Cancelled

Cancellation may imply a semantic Plan repair, which ordinary 09-E v1 does not
own.

Therefore any source task with:

```text
Status = Cancelled
```

produces:

```text
UNSUPPORTED_CANCELLED_TASK_STATE
```

as a material finding for v1 and prevents:

```text
EXECUTOR_READY
```

The compiler must not guess whether downstream tasks should be removed,
rewired, revived, or considered satisfied.

### Mixed status

Mixed statuses are legal input except for the fail-closed `Cancelled` rule
above.

Status combinations do not create hidden dependency/readiness rules.

## 8. Exact proposal carrier v1

The semantic proposal carrier is:

```text
UTF-8 JSON
```

only.

No YAML proposal format is part of v1.

The core API may consume the already-parsed equivalent mapping, but the product
file/CLI carrier is JSON.

Top-level `CompilationProposalV1` contains exactly:

```text
schema_version
source_binding
units
existing_dependency_handoffs
semantic_assessment_source
semantic_evidence_refs
```

Requirements:

```text
schema_version = 1
unknown top-level keys rejected
missing keys rejected
duplicate JSON keys rejected
unit IDs unique
handoff identities unique
```

## 9. Source binding serialization

`source_binding` contains exactly:

```text
plan_ref
plan_sha256
tasks_ref
tasks_sha256
```

The proposal file itself is bound by:

```text
proposal_sha256
```

at the adapter/request boundary.

No source may be associated by:

```text
latest
nearest
same Change name
same filename
similar filename
mtime
directory scan
history search
```

## 10. Unit proposal shape

Each `units[]` entry contains exactly:

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

Disposition exactly:

```text
KEEP_UNIT
CAPABILITY_COUPLED
SPLIT_RECOMMENDED
```

For `KEEP_UNIT` and `CAPABILITY_COUPLED`:

```text
derived_units = []
new_internal_edges = []
internal_handoffs = []
```

unless an existing dependency handoff is represented separately in
`existing_dependency_handoffs`.

## 11. True split semantics

`SPLIT_RECOMMENDED` is valid only when one original unit becomes at least two
derived executable units.

Require:

```text
ORIGINAL_UNIT_ID
DERIVED_UNIT_IDS
NEW_INTERNAL_DEPENDENCY_EDGES
INTERNAL_TYPED_HANDOFFS
```

and all S1-S6 PASS.

Same-count relabeling is:

```text
FALSE_CAPABILITY_SPLIT
```

## 12. Frozen S1-S6 split test

Exactly:

```text
S1
a meaningful capability boundary exists

S2
the upstream result can be represented as a bounded explicit handoff

S3
the handoff is independently verifiable

S4
downstream work does not require reconstruction of material hidden reasoning
from the upstream executor

S5
authority, dependency, acceptance, verification and failure semantics survive
the split

S6
the split reduces more coordination ambiguity / decision burden than it creates
```

Multiple Work Capabilities alone never imply a split.

## 13. Existing dependency handoff is not split

Freeze literally:

```text
EXISTING_DEPENDENCY_HANDOFF
!=
CAPABILITY_SPLIT
```

For an already-existing edge:

```text
U1 -> U2
```

09-E may add a typed handoff without changing:

```text
unit count
dependency graph
parallelism
split count
```

For:

```text
U1 --+
     +--> U3
U2 --+
```

the compiler may validate:

```text
U1 -> U3 handoff
U2 -> U3 handoff
```

but may not invent:

```text
U1 -> U2
U2 -> U1
```

Freeze literally:

```text
SILENT_PARALLELISM_LOSS:
FORBIDDEN
```

## 14. Typed Handoff v1 minimum

Every required typed handoff contains exactly these semantic fields:

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

It remains derived and non-authoritative.

## 15. C01-C13 frozen coverage meanings

Exactly:

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

Every required cell is:

```text
PASS
FAIL
N/A
```

with bounded reason/evidence.

No unit or mandatory criterion may be silently omitted.

## 16. Review order

Freeze exactly:

```text
structural lint
-> complete coverage matrix
-> bounded semantic perspective review
-> collect all findings
-> merge / deduplicate findings
-> repair
-> rerun the SAME coverage matrix
-> adversarial material-seam review
```

Freeze:

```text
FINDING_SEARCH_BEFORE_REPAIR:
REQUIRED
```

The deterministic compiler itself does not autonomously perform semantic repair.

## 17. Additional deterministic failure classes

In addition to the base Definition taxonomy, v1 includes:

```text
UNSUPPORTED_TASK_GRAPH_GRAMMAR
MALFORMED_TASK_ID
DUPLICATE_TASK_ID
UNKNOWN_DEPENDENCY_TASK
SELF_DEPENDENCY
TASK_GRAPH_CYCLE
UNSUPPORTED_CANCELLED_TASK_STATE
PROPOSAL_SCHEMA_INVALID
```

These do not replace the frozen existing classes.

## 18. Neutral parser ownership

Do not reuse:

`src/planning_lite/context.py::_heading_section`

or move 09-E parsing semantics into PL06.

The minimal v1 parser belongs privately inside:

`src/planning_lite/plan_compilation.py`

unless Implementation Plan review proves a separate neutral module is strictly
necessary.

No general-purpose Markdown parsing subsystem is authorized.

The pure module may accept already-read strings/bytes/mappings and remains free
of filesystem, Git, network, telemetry, model invocation and persistence.

## 19. CLI decision

The v1 product includes one thin read-only CLI seam.

Freeze:

```text
planning-lite plan-compile TARGET
  --plan <exact path>
  --tasks <exact path>
  --proposal <exact JSON path>
```

Output:

```text
deterministic JSON to stdout
```

only.

No YAML output is required in v1.

The CLI owns only:

```text
argument parsing
validated exact path reads
byte SHA256 binding
JSON proposal loading
call into pure 09-E core
deterministic stdout / exit mapping
```

It does not own 09-E semantic rules.

## 20. Exit behavior

Implementation Plan must define exact numeric codes, but semantic classes are:

```text
SUCCESS_READY
SUCCESS_NOT_READY
INVALID_INPUT_OR_SCHEMA
INTERNAL_CONTRACT_ERROR
```

`SUCCESS_NOT_READY` is a valid compiler result, not a runtime crash.

Exact numeric encoding is a nonmaterial Implementation Plan choice provided it
is deterministic and tested.

## 21. Exact implementation path budget

The intended maximum implementation surface is exactly six paths:

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

No other source/test/template/integrity path is authorized by this Definition.

Existing whole-organism suites may be RUN without modification.

If implementation requires:

```text
tests/test_system_traversability.py mutation
new Markdown helper module
MANIFEST_V4.md mutation
new docs/operator path
new persistent proposal/result file
```

the affected work stops for owner adjudication.

## 22. Whole-organism owner names

The Change must preserve without authority transfer:

```text
PL06 Context / Resume / Handoff
PL07 Operation Guidance
Authoritative Attempt Runtime
Governed Operation Lifecycle
RunReceipt / telemetry owner
PL08 Attempt Evaluation
Project Spine
```

09-E remains upstream derived planning analysis only.

## 23. Definition success state

After this Amendment is accepted:

```text
BLOCKING_EDGE_GRAMMAR:
BOUND

TASK_STATUS_SEMANTICS:
BOUND

PROPOSAL_SERIALIZATION:
BOUND

CLI_PRESENCE:
BOUND

PARSER_OWNER:
BOUND

IMPLEMENTATION_PATH_BUDGET:
BOUND

FROZEN_S1_S6:
BOUND

TYPED_HANDOFF_MINIMUM:
BOUND

C01_C13_MEANINGS:
BOUND

REVIEW_ORDER:
BOUND

UNBOUND_MATERIAL_DEFINITION_CHOICES:
0
```

## 24. Next gate

Materialization of this Amendment does not authorize implementation.

After exact materialization and owner acceptance:

```text
NEXT_SINGLE_GATE:
PREPARE_09_E_READONLY_PLAN_COMPILER_IMPLEMENTATION_PLAN
```
