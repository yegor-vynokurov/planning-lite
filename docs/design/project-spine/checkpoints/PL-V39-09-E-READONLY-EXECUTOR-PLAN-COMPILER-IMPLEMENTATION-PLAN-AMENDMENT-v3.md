# Implementation Plan Amendment v3

## S1-S6 Scope Micro-Correction

OPERATION: MATERIALIZE_09_E_S1_S6_SCOPE_CORRECTION_AND_RUN_FORMAL_READINESS_V4
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
AMENDMENT: IMPLEMENTATION_PLAN_AMENDMENT_V3
STATUS: OWNER-ADJUDICATED / MICRO-CORRECTION BOUND
IMPLEMENTATION_AUTHORIZED: NO

This amendment changes only the correction required for the S1-S6 authority
scope drift identified after the corrected-candidate inspection.

## 1. Product correction surface

The full implementation candidate remains exactly six paths.

The S1-S6 micro-correction is expected to require only:

src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py

src/planning_lite/cli.py and tests/test_cli.py remain eligible only if the
existing schema-error exit-2 mapping requires a directly demonstrated update.

The template and checksum paths remain byte-identical:

template/.planning/changes/templates/tasks.md
template/.planning/framework/SHA256SUMS.txt

No seventh path is allowed.

## 2. Required implementation correction

Remove the requirement that:

derived_units[].already_decided

contain S1-S6.

Retain the existing parent SPLIT_RECOMMENDED validation:

units[].already_decided
-> exactly one S1-S6 identity each
-> duplicate identity = PROPOSAL_SCHEMA_INVALID
-> missing/N/A/non-PASS prevents readiness

For DerivedUnitV1:

already_decided is required by the exact schema
and must equal []

Any non-empty derived-unit already_decided is:

PlanCompilationInputError
code = PROPOSAL_SCHEMA_INVALID

No new decision vocabulary is introduced.

## 3. Required direct tests

Add or amend tests in the existing test paths proving:

M01:
parent SPLIT_RECOMMENDED with complete S1-S6 PASS and derived
already_decided=[] can reach EXECUTOR_READY when all other conditions pass.

M02:
parent missing one S assertion cannot reach EXECUTOR_READY.

M03:
parent S assertion with FAIL cannot reach EXECUTOR_READY.

M04:
parent duplicate S identity raises PROPOSAL_SCHEMA_INVALID.

M05:
derived already_decided=[] is valid and does not require S1-S6.

M06:
derived already_decided containing S1-S6 is rejected as
PROPOSAL_SCHEMA_INVALID.

M07:
derived already_decided containing any other non-empty value is rejected as
PROPOSAL_SCHEMA_INVALID.

M08:
all C01-C16 tests from Implementation Plan Amendment v2 remain passing after
the semantic-scope correction, except any C test whose fixture must be updated
only to replace derived S1-S6 with derived already_decided=[].

## 4. Regression

Retain:

- all previous plan-compilation tests;
- all CLI tests;
- template/foundation integrity tests;
- whole-organism traversability tests;
- full suite;
- exact path accounting;
- no new authority/runtime seam.

## 5. Stop conditions

STOP if:

- a new path becomes necessary;
- the task/template grammar must change;
- DerivedUnitV1 needs a new semantic decision language;
- parent S1-S6 semantics must change;
- CLI exit semantics must change;
- whole-organism owner must change.

PRODUCT_IMPLEMENTATION_AUTHORIZED: NO

NEXT_GATE:
OWNER_REVIEW_09_E_S1_S6_FORMAL_READINESS_V4
