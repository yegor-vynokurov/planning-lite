# CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
## Implementation Plan Amendment v1
### ControlledDiscoveryV1 Implementation Binding

```text
BASE_IMPLEMENTATION_PLAN_SHA256:
9753EC53A123A1B51C7C07E99C90003BE4AA165215FF2BEDEF995D40AC6D5520

DEFINITION_AMENDMENT_V2:
BIND_ON_MATERIALIZATION

TASK_GRAPH_CHANGE:
NO

IMPLEMENTATION_PATH_CHANGE:
NO

FORMAL_READINESS_MATRIX_COUNT_CHANGE:
NO

AC_COUNT_CHANGE:
NO

PRODUCT_IMPLEMENTATION_AUTHORIZED:
NO
```

## 1. Proposal contract update

T-02 must implement the effective seven-key top-level proposal:

```text
schema_version
source_binding
units
existing_dependency_handoffs
controlled_discoveries
semantic_assessment_source
semantic_evidence_refs
```

## 2. ControlledDiscoveryV1 core validation

T-02 must validate exact keys:

```text
unit_ref
question
scope_bound
stop_condition
output_contract
verification_before_dependent_work
```

and enforce:

```text
required array carrier
exact keys
string types
non-empty trimmed values
final-unit reference
one entry maximum per final unit
deterministic ordering
```

## 3. Split interaction

Compiler order must be:

```text
parse original graph
-> validate proposal units/dispositions
-> derive final compiled units
-> validate controlled_discoveries against final units
-> validate coverage/findings
-> compute readiness
```

This prevents controlled discovery from attaching to a replaced split parent.

## 4. Readiness computation

T-02 implements exactly:

```text
no controlled discovery + all READY predicates
-> EXECUTOR_READY

one or more valid controlled discoveries
+ all other READY predicates
-> EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY

any other material defect
-> EXECUTOR_NOT_READY
```

Proposal does not supply final readiness.

## 5. Result update

`PlanCompilationResultV1` exact result keys become:

```text
schema_version
source_binding
proposal_sha256
original_graph
compiled_graph
compiled_units
existing_edge_handoffs
internal_split_handoffs
controlled_discoveries
coverage
findings
readiness
semantic_assertion_provenance
```

## 6. Deterministic findings

Add these findings to T-02 focused validation:

```text
INVALID_CONTROLLED_DISCOVERY
UNKNOWN_CONTROLLED_DISCOVERY_UNIT
DUPLICATE_CONTROLLED_DISCOVERY_UNIT
```

## 7. Test additions within existing path budget

Add focused tests only in `tests/test_plan_compilation.py` for:

```text
empty controlled_discoveries -> READY possible
valid controlled discovery on KEEP_UNIT -> READY_WITH_CONTROLLED_DISCOVERY
valid controlled discovery on CAPABILITY_COUPLED -> READY_WITH_CONTROLLED_DISCOVERY
valid controlled discovery on derived split unit -> READY_WITH_CONTROLLED_DISCOVERY
controlled discovery on replaced split parent -> UNKNOWN_CONTROLLED_DISCOVERY_UNIT
unknown unit_ref -> UNKNOWN_CONTROLLED_DISCOVERY_UNIT
duplicate unit_ref -> DUPLICATE_CONTROLLED_DISCOVERY_UNIT
missing field -> INVALID_CONTROLLED_DISCOVERY
extra field -> INVALID_CONTROLLED_DISCOVERY
blank field -> INVALID_CONTROLLED_DISCOVERY
valid controlled discovery plus another material finding -> EXECUTOR_NOT_READY
proposal cannot force READY_WITH_CONTROLLED_DISCOVERY
```

No new fixture or test file.

## 8. R06 clarification

R06 passes only if the seven-key proposal including
`controlled_discoveries` is exact and implementable without schema inference.

## 9. R09 clarification

R09 passes only if all three readiness states are fully computable, including
the exact controlled-discovery carrier and schema.

## 10. R14 clarification

R14 passes only if compact synthetic fixtures cover the controlled-discovery
cases in section 7 without another test path.

## 11. R16 false-done addition

Add one false-done condition:

```text
READY_WITH_CONTROLLED_DISCOVERY is emitted
without a valid ControlledDiscoveryV1 bound to a final executable unit
```

This must be rejected.

## 12. Path budget unchanged

Still exactly six implementation paths:

```text
src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
src/planning_lite/cli.py
tests/test_cli.py
template/.planning/changes/templates/tasks.md
template/.planning/framework/SHA256SUMS.txt
```

No seventh path.

## 13. Task graph unchanged

Still:

```text
T-01
  |
T-02
  |---------+
  |         |
T-03       T-04
  |---------+
       |
      T-05
       |
      T-06
```

## 14. Formal Readiness rerun

Formal Readiness v1 remains historical:

```text
BLOCKED
```

After this Amendment and Definition Amendment v2 are owner-accepted, run a
fresh `FORMAL_READINESS_VERDICT_V2` against the complete effective authority.
Previously passing R01-R08/R10-R13/R15-R16 must be revalidated, not blindly
copied. R09 and R14 must be freshly evaluated against the now-closed carrier.

## 15. Amendment success

```text
CONTROLLED_DISCOVERY_SCHEMA:
BOUND

CONTROLLED_DISCOVERY_LOCATION:
BOUND

R09_DESIGN_BLOCKER:
RESOLVED

R14_DESIGN_BLOCKER:
RESOLVED

UNBOUND_MATERIAL_PLAN_CHOICES:
0
```
