# PL-V39-08 RunReceipt Measurement Correction - Plan Amendment v3 Review v1

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V3
reviewer: EXPLICIT_HUMAN_OWNER
review_date: 2026-09-29
reviewed_plan: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v3.md
reviewed_plan_sha256: 53c7d59b2f119926198b436404165c725ef9fb86d0d48b4b373f599323be898a
review_verdict: REVIEW_FAIL / 1 MATERIAL FINDING
material_finding_count: 1

## Owner review verdict

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V3:
REVIEW_FAIL / 1 MATERIAL FINDING

P3-01 MEASUREMENT_ELIGIBILITY_AND_COVERAGE_DEFERRED_TO_DISCOVERY

P1_01_DESIGN_CORRECTION_ACCEPTED: YES / RUNTIME PROOF REMAINS T00-GATED
P1_02_DESIGN_CORRECTION_ACCEPTED: YES / RUNTIME PROOF REMAINS T00-GATED
P2_01_CLOSED_IN_V3_DESIGN: YES
OPTION_C_PRESERVED: YES
DEFINITION_AMENDMENT_V2_PRESERVED: YES
PLAN_AMENDMENT_V3_APPROVED: NO
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS_STARTED: NO
T00_AUTHORIZED: NO
09_G_STARTED: NO
```

## Material finding

### P3-01 MEASUREMENT_ELIGIBILITY_AND_COVERAGE_DEFERRED_TO_DISCOVERY

Plan Amendment v3 places in T00 the question whether Change 3 may cover only
explicitly collected Attempts, and says T00 must stop for an owner decision if
automatic or every-Attempt measurement is required. That is an owner-level
measurement eligibility and coverage decision, not a runtime fact discovery.
T00 may establish whether the source, binding, completion, response ownership,
command, and persistence mechanics work. It must not decide what makes an
operation measurement-eligible or what coverage Change 3 promises.

The v3 lifecycle correction is accepted: Plan acceptance precedes Formal
Readiness; any controlled T00 discovery requires its own bounded authorization;
T00 evidence is reviewed before readiness closure/READY; and separate
implementation authorization precedes T01-T06. P2-01 is closed in v3 design.
P1-01 and P1-02 remain design-corrected with their runtime proofs T00-gated.

## Preserved authority

Option C and the active Definition Amendment v2 remain unchanged. The
Attempt-to-turn binding remains distinct from Attempt-to-response-scope
ownership. The explicit delayed/pull command remains a candidate technical
trigger, subject to runtime proof. This review does not approve Plan Amendment
v3, authorize implementation, start Formal Readiness or T00, or start 09-G.

The explicit owner E1 decision in the companion checkpoint resolves the
eligibility and coverage policy finding for the v4 candidate. T00 retains only
runtime fact discovery and may still find the proposed command technically
unsupported; it may not require automatic coverage as a policy condition.

```text
NEXT_SINGLE_GATE:
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V4
```
