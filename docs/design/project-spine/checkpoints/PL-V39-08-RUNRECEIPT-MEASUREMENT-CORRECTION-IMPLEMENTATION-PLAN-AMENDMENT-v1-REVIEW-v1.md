# PL-V39-08 RunReceipt Measurement Correction - Plan Amendment v1 Review v1

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V1
reviewer: EXPLICIT_HUMAN_OWNER
review_date: 2026-09-29
reviewed_plan: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v1.md
reviewed_plan_sha256: 9e02ebe4dc61d2fbc70eba0973033a3406cbe889a060b4b4f4f47d12df5f5c08
review_verdict: REVIEW_FAIL / 2 MATERIAL FINDINGS
material_finding_count: 2

## Owner review verdict

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V1:
REVIEW_FAIL / 2 MATERIAL FINDINGS

P1-01 TURN_SCOPE_NOT_PROVEN_AS_ATTEMPT_SCOPE
P1-02 POST_TURN_MEASUREMENT_TRIGGER_NOT_PROVEN

OPTION_C_DIRECTION_REJECTED: NO
OPTION_C_DIRECTION_PRESERVED: YES
DEFINITION_AMENDMENT_V2_CHANGED: NO
DEFINITION_AMENDMENT_V2_STATUS: APPROVED_BY_OWNER / ACTIVE
PLAN_AMENDMENT_V1_APPROVED: NO
CORRECTED_PLAN_AMENDMENT_REQUIRED: YES
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS_AUTHORIZED: NO
09_G_STARTED: NO
```

## Material findings

### P1-01 TURN_SCOPE_NOT_PROVEN_AS_ATTEMPT_SCOPE

Plan Amendment v1 establishes a proposed Attempt-to-thread/turn binding, then
uses the entire host turn's response set as the Attempt measurement scope. That
binding does not prove each response in the turn belongs to the Attempt. A
pre-Attempt response or unrelated response can be present in the same turn, and
the absence of a second Attempt is not proof of exclusive response ownership.
This does not meet Definition Amendment v2's requirement for a completely
proven operation response scope.

The corrected Plan must separate Attempt-to-turn binding from
Attempt-to-response-scope ownership; require proof for whole-turn equivalence;
allow a subset only through a structured, source-bound ownership signal; and
fail closed with a response-scope ownership reason when neither is provable.
T00 must stop with `ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN` if the supported
sidebar shape cannot establish these semantics.

### P1-02 POST_TURN_MEASUREMENT_TRIGGER_NOT_PROVEN

Plan Amendment v1 requires collection after turn completion and allows the
collector to run in a later host turn, but it does not identify the normal
production invocation owner or trigger. A test can call the final collector
directly and pass aggregation/persistence checks even if the supported
operation path never invokes collection.

The corrected Plan must distinguish collector implementation from its
invocation, identify the supported post-turn trigger and exact binding handoff,
and make P-12/M20 prove that normal path. The candidate may use an explicit
user/agent command only if that is stated as the supported delayed/pull contract
with its no-later-command behavior; it must not claim automatic collection. If
no supported trigger can be proven without new host instrumentation, T00 stops
with `POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`.

## Preserved authority and transition boundary

Definition Amendment v2 and its activation remain unchanged and
`APPROVED_BY_OWNER / ACTIVE`. Option C remains the accepted semantic direction:
`RESPONSE_AGGREGATE` preferred when safe scope, source, and binding are proven;
`BOUNDARY_DELTA` remains its independently proven fallback. R-01 and R-02 retain
their scoped dispositions. This Plan review does not alter either historical
finding or the preserved corrective candidate.

Plan Amendment v1 remains byte-preserved as review history and is not approved.
One corrected Plan Amendment v2 candidate is required. It must preserve accepted
v1 design content except for the changes needed to close P1-01/P1-02, and must
remain `CANDIDATE / OWNER_REVIEW_REQUIRED` pending a separate owner review.

```text
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS: NOT STARTED / NOT AUTHORIZED
09_G: NOT STARTED
NEXT_SINGLE_GATE:
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V2
```
