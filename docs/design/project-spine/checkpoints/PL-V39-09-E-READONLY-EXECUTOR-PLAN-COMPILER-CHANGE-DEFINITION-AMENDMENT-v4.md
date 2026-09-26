# Change Definition Amendment v4

## S1-S6 Scope Correction

OPERATION: MATERIALIZE_09_E_S1_S6_SCOPE_CORRECTION_AND_RUN_FORMAL_READINESS_V4
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
AMENDMENT: DEFINITION_AMENDMENT_V4
STATUS: OWNER-ADJUDICATED / S1-S6 SCOPE CORRECTED
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
PRODUCT_IMPLEMENTATION_PERFORMED: NO

This amendment corrects one semantic scope drift introduced by Definition
Amendment v3. It does not change the approved product scope, architecture,
path budget, compiler ownership, task grammar, readiness states, capability
taxonomy, executor-profile taxonomy, split topology, or handoff contract.

## 1. Correct S1-S6 owner

S1-S6 evaluate the decision to split one original executable unit.

Their semantic owner is:

units[].already_decided

when:

disposition = SPLIT_RECOMMENDED

For a SPLIT_RECOMMENDED original unit, the parent decision must contain exactly
one assertion for each of:

S1
S2
S3
S4
S5
S6

Duplicate S identity is malformed proposal schema and produces:

PlanCompilationInputError
code = PROPOSAL_SCHEMA_INVALID

For a structurally well-formed SPLIT_RECOMMENDED decision, missing S assertions,
N/A, or any non-PASS S verdict prevents executor readiness through the existing
split-structure/non-ready contract.

A later PASS must never mask an earlier duplicate or invalid assertion.

## 2. Derived units do not repeat S1-S6

The requirement in Definition Amendment v3 that every derived unit independently
carry S1-S6 is superseded.

Derived units do not independently re-evaluate whether their parent should have
been split.

Therefore:

S1_S6_REQUIRED_ON_DERIVED_UNITS: NO

The split itself is tested once at the original-unit boundary.

Derived units are validated through their own bounded execution semantics:

- distinct outcome and responsibility;
- own work-capability signature;
- own cross-cutting tags;
- own executor profile;
- own allowed and forbidden executor decisions;
- complete C01-C13 coverage;
- own material findings;
- exact internal edge/handoff relation.

## 3. DerivedUnitV1 already_decided v1 rule

DerivedUnitV1 retains the `already_decided` key in its exact schema.

No independent derived-unit `already_decided` semantic vocabulary was frozen
before Amendment v3.

V1 therefore uses the smallest fail-closed rule:

derived_units[].already_decided MUST equal []

Any non-empty value is malformed v1 proposal schema and produces:

PlanCompilationInputError
code = PROPOSAL_SCHEMA_INVALID

This rule prevents the compiler or implementer from inventing an implicit
second decision language.

A future owner-approved amendment may define a non-empty derived-unit
already_decided contract.

## 4. Amendment v3 supersession boundary

Definition Amendment v3 remains authoritative for:

- exact DerivedUnitV1 keys;
- distinct derived outcomes and bounded responsibilities;
- derived capability/tag/profile/decision fields;
- exact parent capability and tag unions;
- parent material-finding preservation;
- internal edge ↔ typed-handoff equality;
- proposal schema error classification;
- structural non-readiness distinction;
- canonical dependency ordering.

Definition Amendment v3 section C is superseded only where it requires
S1-S6 on every derived unit.

Any v3 text that implies non-empty or S1-S6-bearing derived-unit
`already_decided` is superseded by this Amendment v4.

## 5. Effective split model

The effective v1 model is:

Original unit
  -> disposition = SPLIT_RECOMMENDED
  -> parent already_decided contains S1-S6
  -> split produces >=2 derived units
  -> derived already_decided = []
  -> each derived unit has its own execution envelope
  -> C01-C13 applies to every final executable unit
  -> internal handoffs exactly match internal edges

S1-S6 is not duplicated across children.

## 6. Scope and authority

SCOPE_CHANGE: NO
ARCHITECTURE_CHANGE: NO
PATH_BUDGET_CHANGE: NO
NEW_RUNTIME_SUBSYSTEM: NO
NEW_AUTHORITY_SUBSYSTEM: NO
TASK_GRAMMAR_CHANGE: NO
READINESS_STATE_CHANGE: NO

PRODUCT_IMPLEMENTATION_AUTHORIZED: NO

NEXT_GATE:
FORMAL_READINESS_V4
