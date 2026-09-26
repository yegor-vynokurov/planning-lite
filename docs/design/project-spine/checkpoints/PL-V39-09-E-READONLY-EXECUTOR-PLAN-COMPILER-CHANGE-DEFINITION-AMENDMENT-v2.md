# CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
## Change Definition Amendment v2
### ControlledDiscoveryV1 Proposal Carrier Closure

```text
AMENDMENT_STATUS:
PREPARED / OWNER-AUTHORED

BASE_DEFINITION_SHA256:
6ED1FBD40605EFB5EB5F7689DBF72BA547D18DA289FB4F5A9A8A55CF77EA6A24

AMENDMENT_V1_SHA256:
40868FFEC03590ACFBEBCC24737B495DFB2429093CA3F3D1D524D3BC24E86797

SCOPE_CHANGE:
NO

GOAL_CHANGE:
NO

SELECTED_ARCHITECTURE_CHANGE:
NO

IMPLEMENTATION_PATH_BUDGET_CHANGE:
NO

PRODUCT_IMPLEMENTATION_AUTHORIZED:
NO
```

## 1. Problem closed

Formal Readiness v1 found one material blocker:

```text
CONTROLLED_DISCOVERY_PROPOSAL_CARRIER_SCHEMA_UNBOUND
```

The frozen semantic contract defines controlled discovery conceptually, but the
proposal did not specify its exact location or serialized shape. This Amendment
closes only that omission.

## 2. CompilationProposalV1 top-level shape

Effective exact top-level keys become:

```text
schema_version
source_binding
units
existing_dependency_handoffs
controlled_discoveries
semantic_assessment_source
semantic_evidence_refs
```

`controlled_discoveries` is required and always an array. The explicit
no-discovery value is:

```json
"controlled_discoveries": []
```

No omitted field and no `null` top-level value is valid.

## 3. ControlledDiscoveryV1 exact schema

Each `controlled_discoveries[]` entry contains exactly:

```text
unit_ref
question
scope_bound
stop_condition
output_contract
verification_before_dependent_work
```

No additional keys. All six values are required strings and, after trimming
surrounding whitespace, every value must be non-empty.

## 4. Location semantics

`unit_ref` identifies exactly one FINAL executable unit in the compiled plan.
For `KEEP_UNIT` and `CAPABILITY_COUPLED`, the final identity is the original
unit ID. For `SPLIT_RECOMMENDED`, the original unit is replaced for execution
by its derived units; discovery may reference only a valid derived unit ID,
not the replaced original unit ID.

## 5. Cardinality

V1 permits at most one `ControlledDiscoveryV1` per final executable unit.
Duplicate `unit_ref` entries are invalid. If one executable unit requires
multiple independent discovery operations, v1 does not merge or infer them;
that unit is:

```text
EXECUTOR_NOT_READY
```

until the semantic proposal presents one bounded discovery operation or the
Plan is otherwise refined.

## 6. Semantic boundary

The deterministic core proves only:

```text
all required fields exist
all values are strings
all values are non-empty after trim
unit_ref names one final compiled executable unit
unit_ref is unique in controlled_discoveries
```

The core does not infer whether a natural-language question is intellectually
sufficient, wise, or domain-complete. Semantic boundedness remains a semantic
planner assertion cross-checked through the frozen C01-C13 coverage/evidence
contract. No LLM/model call is introduced.

## 7. Authority invariant

Controlled discovery:

```text
does not grant authority
does not expand allowed writes
does not alter the original DAG
does not alter current lifecycle state
does not authorize execution
does not select an executor/model
```

The dependent work must still resolve current authority normally.

## 8. Readiness semantics

`EXECUTOR_READY` requires:

```text
controlled_discoveries = []
```

in addition to all previously frozen READY requirements.

`EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY` requires all of:

```text
controlled_discoveries contains at least one valid entry
every referenced final executable unit is otherwise structurally ready
all mandatory C01-C13 assertions are PASS or justified N/A
no unresolved material finding exists
DAG preservation passes
split/coupling validation passes
all required typed handoffs pass
no executor-profile contradiction exists
no Cancelled task exists
```

Controlled discovery must be the only remaining bounded execution prerequisite.
Any other material defect yields `EXECUTOR_NOT_READY`, not
`EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY`.

## 9. Coverage interaction

Controlled discovery does not itself force a C01-C13 cell to FAIL. The matrix
evaluates whether the compiled unit and discovery contract are sufficiently
bounded. C03/C05/C06/C10/C12/C13 may PASS when the unresolved fact is explicitly
bounded by a valid discovery contract. The compiler does not fabricate those
PASS values; they remain explicit semantic proposal assertions.

## 10. Invalid controlled-discovery findings

Add exact deterministic, material finding classes:

```text
INVALID_CONTROLLED_DISCOVERY
UNKNOWN_CONTROLLED_DISCOVERY_UNIT
DUPLICATE_CONTROLLED_DISCOVERY_UNIT
```

`INVALID_CONTROLLED_DISCOVERY` covers structural shape, type, or empty-value
failure. `UNKNOWN_CONTROLLED_DISCOVERY_UNIT` covers a `unit_ref` that is not a
final compiled executable unit. `DUPLICATE_CONTROLLED_DISCOVERY_UNIT` covers
more than one entry for the same final unit.

## 11. Result projection

`PlanCompilationResultV1` continues to contain compiled units, readiness, and
findings. Add exact result field:

```text
controlled_discoveries
```

It contains the validated projection in deterministic final-unit order and is
derived/non-authoritative output.

## 12. No new persistence or authority

No registry, file-per-discovery store, queue, worker, scheduler, or lifecycle
surface is introduced.

```text
PERSIST_RESULT:
NO
```

## 13. Blocker disposition

```text
CONTROLLED_DISCOVERY_PROPOSAL_CARRIER_SCHEMA_UNBOUND:
RESOLVED

UNBOUND_MATERIAL_DEFINITION_CHOICES:
0
```
