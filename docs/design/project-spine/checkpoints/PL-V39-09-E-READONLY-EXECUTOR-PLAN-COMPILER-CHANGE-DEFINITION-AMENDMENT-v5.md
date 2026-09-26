# PL-V39-09-E Read-Only Executor Plan Compiler Change Definition Amendment v5

## Surviving-Seams Adjudication

OPERATION: MATERIALIZE_09_E_SURVIVING_SEAMS_ADJUDICATION_AND_RUN_FORMAL_READINESS_V5
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
AMENDMENT: CHANGE_DEFINITION_AMENDMENT_V5
STATUS: OWNER-ADJUDICATED / FORMAL-READINESS BOUND
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO

This amendment binds the owner adjudication of the four surviving material
findings from the S1-S6 micro-correction candidate review. It defines the
minimum semantic correction contract and does not authorize product
implementation.

## 1. Owner review result

```text
OWNER_REVIEW_09_E_S1_S6_MICRO_CORRECTION_CANDIDATE: NEEDS_CORRECTION
S1_S6_MICRO_CORRECTION: PASS
NEW_MATERIAL_FINDING_COUNT: 4
COMMIT_AUTHORIZED: NO
```

The four findings are:

```text
F7 DERIVED_DECISION_ENVELOPE_CONTRADICTION_UNCHECKED
F8 ORIGINAL_ALREADY_DECIDED_SPLIT_ASSERTION_OVERBINDING
F9 C01_C13_NA_AUTHORITY_DRIFT
F10 CLI_ERROR_RENDERING_AUTHORITY_DRIFT
```

## 2. Owner adjudication F7

DerivedUnitV1 uses the same executor-envelope invariant as an unsplit final
unit. For every derived unit:

```text
SET(allowed_executor_decisions)
INTERSECT
SET(forbidden_executor_decisions)
==
EMPTY
```

A non-empty intersection is not malformed JSON/schema. It is a structurally
contradictory execution envelope and produces:

```text
EXECUTOR_PROFILE_MISMATCH
EXECUTOR_NOT_READY
CLI exit 3
```

No new finding code is introduced.

## 3. Owner adjudication F8

`already_decided` is a semantic decision carrier. It is not globally
redefined as the S1-S6 carrier.

The smallest v1 item shapes are:

```text
DecisionNoteV1:
non-empty JSON string
```

and:

```text
SplitAssertionV1:
{
  "assertion": "S1" | "S2" | "S3" | "S4" | "S5" | "S6",
  "verdict": "PASS" | "FAIL" | "N/A"
}
```

No alias keys are accepted. `criterion`, `id`, and `value` aliases and
string-form S assertions are invalid.

Disposition semantics:

```text
KEEP_UNIT:
already_decided contains zero or more DecisionNoteV1 strings.
SplitAssertionV1 objects are invalid.

CAPABILITY_COUPLED:
already_decided contains zero or more DecisionNoteV1 strings.
SplitAssertionV1 objects are invalid.

SPLIT_RECOMMENDED:
already_decided may contain zero or more DecisionNoteV1 strings
PLUS exactly one SplitAssertionV1 for each S1-S6.
```

For `SPLIT_RECOMMENDED`:

```text
duplicate S identity -> PROPOSAL_SCHEMA_INVALID / exit 2
missing S identity -> structural non-ready / exit 3
FAIL -> structural non-ready / exit 3
N/A -> structural non-ready / exit 3
```

Semantic DecisionNoteV1 values do not participate in S1-S6 multiplicity.

DerivedUnitV1:

```text
already_decided contains zero or more DecisionNoteV1 strings.
```

Derived units must not contain SplitAssertionV1. Any S1-S6 SplitAssertionV1
on a derived unit is `PROPOSAL_SCHEMA_INVALID / exit 2`.

This supersedes Definition Amendment v4 only where v4 required
`derived_units[].already_decided == []`. Amendment v4 remains authoritative
that S1-S6 belongs to the original split decision and is not repeated on
derived units.

A derived unit may carry its own semantic DecisionNoteV1 strings. No parent
semantic decision is automatically inherited into a derived unit; the
explicit semantic proposal states the bounded decisions applicable to each
derived unit.

## 4. Owner adjudication F9

The frozen C01-C13 semantics are restored. Allowed criterion verdicts remain:

```text
PASS
FAIL
N/A
```

`N/A` is a valid criterion disposition and does not by itself prevent
`EXECUTOR_READY` or `EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY`, provided the
C01-C13 set is complete, assertion shape is valid, reason is non-empty, and
no other material finding exists.

Classification:

```text
malformed assertion object shape/type
-> PROPOSAL_SCHEMA_INVALID / exit 2

unknown criterion identity, duplicate criterion identity, or invalid verdict
-> INVALID_CRITERION_VALUE / structural non-ready / exit 3

missing criterion
-> COVERAGE_INCOMPLETE / structural non-ready / exit 3

FAIL
-> UNRESOLVED_MATERIAL_FINDING / structural non-ready / exit 3

N/A
-> valid coverage value
```

This supersedes Amendment v3 wording that treated every non-PASS C01-C13
assertion as non-ready. It does not change S1-S6 semantics: S1-S6 N/A remains
non-ready.

## 5. Owner adjudication F10

No new JSON error-response protocol is introduced. The canonical JSON contract
applies to successful compiler results, including:

```text
EXECUTOR_READY
EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY
EXECUTOR_NOT_READY
```

Input/schema errors remain exit 2 with the existing PlanningLiteError stderr
rendering and no result JSON on stdout. Unexpected internal compiler contract
failures remain exit 1 with existing stderr rendering.

Amendment v3 and Plan Amendment v2 are superseded only where they imply that
exit-2 errors require a canonical structured JSON error object. The required
invariant is bounded error, correct exit classification, no traceback leak,
and no accidental result JSON; no new error schema is required.

## 6. Scope and supersession ledger

```text
SCOPE_CHANGE: NO
ARCHITECTURE_CHANGE: NO
TASK_GRAMMAR_CHANGE: NO
PATH_BUDGET_CHANGE: NO
NEW_RUNTIME_SUBSYSTEM: NO
NEW_AUTHORITY_SUBSYSTEM: NO

V3_SUPERSEDED:
- derived decision-envelope omission corrected
- C01-C13 non-PASS wording corrected for N/A
- canonical JSON error-rendering requirement removed

V4_SUPERSEDED:
- derived already_decided EMPTY_ARRAY_ONLY replaced by DecisionNoteV1 array

V4_PRESERVED:
- S1-S6 belongs only to original SPLIT_RECOMMENDED decision
- derived units do not carry S1-S6
```

No product path is changed by this materialization.

```text
NEXT_GATE: FORMAL_READINESS_V5
```
