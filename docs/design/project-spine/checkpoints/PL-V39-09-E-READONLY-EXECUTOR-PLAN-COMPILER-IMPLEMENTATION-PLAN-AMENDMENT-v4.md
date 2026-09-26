# PL-V39-09-E Read-Only Executor Plan Compiler Implementation Plan Amendment v4

## Surviving-Seams Correction Plan

OPERATION: MATERIALIZE_09_E_SURVIVING_SEAMS_ADJUDICATION_AND_RUN_FORMAL_READINESS_V5
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
AMENDMENT: IMPLEMENTATION_PLAN_AMENDMENT_V4
STATUS: OWNER-ADJUDICATED / FORMAL-READINESS BOUND
IMPLEMENTATION_AUTHORIZED: NO

This amendment binds the smallest implementation and verification surface for
F7-F10. It does not perform product implementation and does not authorize a
product commit.

## 1. Correction surface and path budget

The effective implementation candidate remains exactly six product paths:

```text
src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
src/planning_lite/cli.py
tests/test_cli.py
template/.planning/changes/templates/tasks.md
template/.planning/framework/SHA256SUMS.txt
```

The likely required product writes are limited to:

```text
src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
```

CLI code is expected to remain unchanged because F10 adopts the existing CLI
error behavior. `tests/test_cli.py` may be changed only to tighten direct
evidence of the existing stderr/exit-2 contract. The template and checksum
paths must remain byte-identical. No seventh path is allowed.

## 2. Required semantic corrections

The implementation must:

1. Reject a derived allowed/forbidden executor-decision overlap as the
   existing `EXECUTOR_PROFILE_MISMATCH` finding and make the result
   `EXECUTOR_NOT_READY`.
2. Parse `already_decided` by disposition using DecisionNoteV1 strings and,
   only on the original `SPLIT_RECOMMENDED` unit, exact SplitAssertionV1
   objects.
3. Preserve parent S1-S6 multiplicity, duplicate, missing, FAIL, and N/A
   semantics. DecisionNoteV1 strings do not count toward S1-S6 completeness.
4. Permit derived DecisionNoteV1 strings and preserve them in the compiled
   derived-unit projection. Derived SplitAssertionV1 objects remain invalid.
5. Treat a complete, well-shaped C01-C13 assertion with verdict `N/A` as a
   valid coverage value that does not by itself prevent readiness.
6. Preserve FAIL, missing, duplicate, unknown, and malformed coverage
   classifications exactly as defined by Amendment v5.
7. Preserve the existing thin CLI adapter, exit mapping, stderr rendering,
   no-result-JSON-on-exit-2 behavior, and no-traceback boundary.

## 3. Required direct challenge tests

```text
P01 derived allowed/forbidden overlap -> EXECUTOR_NOT_READY
     + EXECUTOR_PROFILE_MISMATCH
P02 KEEP_UNIT with non-empty DecisionNoteV1 -> valid and preserved
P03 CAPABILITY_COUPLED with non-empty DecisionNoteV1 -> valid and preserved
P04 SPLIT_RECOMMENDED with DecisionNoteV1 + exact S1-S6 PASS
     -> split validation succeeds
P05 DecisionNoteV1 does not count toward S1-S6 completeness
P06 S assertion object on KEEP_UNIT -> PROPOSAL_SCHEMA_INVALID
P07 S assertion object on derived unit -> PROPOSAL_SCHEMA_INVALID
P08 derived non-empty DecisionNoteV1 -> valid and preserved
P09 duplicate parent S identity remains PROPOSAL_SCHEMA_INVALID
P10 missing parent S remains structural NOT_READY
P11 parent S N/A remains structural NOT_READY
P12 one genuine C01-C13 N/A with bounded reason -> does not by itself prevent READY
P13 C01-C13 FAIL remains NOT_READY
P14 unknown/duplicate C criterion remains structural NOT_READY
P15 malformed criterion object shape remains PROPOSAL_SCHEMA_INVALID
P16 schema error through CLI remains exit 2, stdout contains no result JSON,
     stderr contains bounded Planning Lite error, and no traceback
```

## 4. Retained verification

Retain all M01-M08, C01-C16, prior plan-compilation, CLI, template/foundation,
whole-organism, path-boundary, status, controlled-discovery, and readiness
tests. Update fixtures only where DecisionNoteV1 semantics intentionally
supersede Amendment v4. The six-path boundary and template/checksum byte
identity remain acceptance conditions. No product tests need to be rerun by
the governance/readiness gate itself.

## 5. Stop conditions

```text
new product or governance path outside the stated budget
task/template grammar change
new DerivedUnitV1 decision vocabulary beyond DecisionNoteV1 and SplitAssertionV1
change to parent S1-S6 ownership or semantics
new CLI error-response protocol or exit semantics
new runtime, persistence, filesystem, network, telemetry, model, or authority subsystem
template or checksum mutation
whole-organism owner change
```

```text
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
NEXT_GATE: FORMAL_READINESS_V5
```
