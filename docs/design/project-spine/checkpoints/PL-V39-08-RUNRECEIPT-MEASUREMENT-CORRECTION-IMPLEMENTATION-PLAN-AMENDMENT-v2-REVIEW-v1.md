# PL-V39-08 RunReceipt Measurement Correction - Plan Amendment v2 Review v1

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V2
reviewer: EXPLICIT_HUMAN_OWNER
review_date: 2026-09-29
reviewed_plan: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v2.md
reviewed_plan_sha256: a73d8084d5967c7451630b6a28016ff5c54b000d4d126c54d8b6aa995b8b45c8
review_verdict: REVIEW_FAIL / 1 MATERIAL FINDING
material_finding_count: 1

## Owner review verdict

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V2:
REVIEW_FAIL / 1 MATERIAL FINDING

P2-01 FORMAL_READINESS_AND_T00_GATE_ORDER_CONTRADICTORY

P1_01_DESIGN_CORRECTION_ACCEPTED: YES
P1_02_DESIGN_CORRECTION_ACCEPTED: YES
OPTION_C_PRESERVED: YES
DEFINITION_AMENDMENT_V2_CHANGED: NO
PLAN_AMENDMENT_V2_APPROVED: NO
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS_STARTED: NO
09_G_STARTED: NO
```

## Material finding

### P2-01 FORMAL_READINESS_AND_T00_GATE_ORDER_CONTRADICTORY

Plan Amendment v2 states that Plan acceptance is followed by Formal Readiness
and separate implementation authorization. Its Section 15, however, frames T00
as the first step of an implementation sequence after authorization. T00
contains read-only facts that determine readiness and must precede product
mutation. Section T06 also says Formal Readiness is a later gate after
implementation. Those statements permit the contradictory reading
`Plan acceptance -> implementation authorization -> T00/T01-T06 -> Formal
Readiness`, contrary to the established lifecycle.

The corrected candidate must place T00 before implementation authorization,
classify T00 as `READ_ONLY_PRE_IMPLEMENTATION_CONTROLLED_DISCOVERY`, and place
Formal Readiness and any required T00-specific authorization/evidence review in
one explicit sequence. T01-T05 alone are product/test implementation; T06 is
post-implementation verification. Formal Readiness must not be deferred until
after T06.

## Selected readiness pattern

Read-only inspection of the existing Change 3 Formal Readiness verdict found
`READY_WITH_CONTROLLED_DISCOVERY`, `CONTROLLED_DISCOVERY_REQUIRED: YES`, and an
explicit statement that controlled discovery is not authorized by that verdict
and requires separate authorization. Plan Amendment v3 therefore selects
Pattern B: accepted Plan -> Formal Readiness disposition -> separate bounded
owner authorization for T00 when readiness specifically identifies that
discovery -> read-only T00 -> T00 evidence review -> readiness closure/READY ->
separate implementation authorization. A blocked readiness result does not
authorize T00. This review does not start Formal Readiness or authorize T00.

## Preserved authority and accepted v2 corrections

P1-01 `TURN_SCOPE_NOT_PROVEN_AS_ATTEMPT_SCOPE` and P1-02
`POST_TURN_MEASUREMENT_TRIGGER_NOT_PROVEN` are accepted as semantically
corrected in v2's design. Runtime proof remains T00-gated. Preserve the
distinction between Attempt-to-turn binding and Attempt-to-response-scope
ownership, the A/B/C scope classification, the explicit delayed/pull post-turn
command contract as a candidate trigger, and the no-automatic-measurement claim.

Option C and Definition Amendment v2 remain unchanged. Plan Amendment v2 is not
approved; exactly one corrected Plan Amendment v3 candidate is required. It
remains `CANDIDATE / OWNER_REVIEW_REQUIRED` pending separate owner review.

```text
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS: NOT STARTED / NOT AUTHORIZED BY THIS TRANSITION
09_G: NOT STARTED
NEXT_SINGLE_GATE:
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V3
```
