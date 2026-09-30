# PL-V39-08 RunReceipt Measurement Correction - Measurement Eligibility E1 Owner Decision v1

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: OWNER_DECISION_CHANGE_3_MEASUREMENT_ELIGIBILITY_E1
owner_decision_source: EXPLICIT_HUMAN_OWNER
decision_date: 2026-09-29
active_effective_definition: PREDECESSOR DEFINITION + AMENDMENT V2

## Owner decision

```text
OWNER_DECISION: SELECT_E1_EXPLICIT_POST_TURN_COLLECTION_ELIGIBILITY
MEASUREMENT_ELIGIBILITY_MODE: EXPLICIT_POST_TURN_COLLECTION_REQUEST
AUTOMATIC_ALL_ATTEMPT_MEASUREMENT: NO
EVERY_GOVERNED_ATTEMPT_AUTOMATICALLY_ELIGIBLE: NO
NO_COLLECTION_REQUEST_MEANS: NO_MEASUREMENT_CLAIM
NO_COLLECTION_REQUEST_MEANS_UNAVAILABLE: NO
NO_COLLECTION_REQUEST_MEANS_ZERO: NO
NO_COLLECTION_REQUEST_MEANS_FAILURE: NO
AUTOMATIC_COVERAGE_REQUIRED_FOR_CHANGE_3: NO
UNIVERSAL_COVERAGE_IN_CHANGE_3: NO
NEW_DEFINITION_AMENDMENT_REQUIRED_FOR_E1: NO
IMPLEMENTATION_AUTHORIZED: NO
```

## E1 semantic contract

E1 defines eligibility for the current Codex `RESPONSE_AGGREGATE` capability. A
governed Planning Lite Attempt does not become measurement-eligible merely
because it executed. Eligibility is created only by an explicit, source-bound
post-turn collection request naming one exact existing Attempt.

The supported request identifies:

- the exact persisted `attempt_id`;
- an explicit rollout/source reference for the target host context, or an
authoritative equivalent only if the approved Plan and T00 prove that contract;
- the exact host thread/turn binding resolved from that Attempt's persisted
trace, without recency, timestamp, current-turn, or latest-record selection.

The public collection command is the eligibility-creation mechanism and its
caller owns invocation. A request grants neither routing authority nor execution
authority. It does not create an automatic collection obligation for any other
Attempt.

### No collection request

If no explicit request is made, no `operation_measurement_v2` claim is required
or emitted for that Attempt. There is no SAFE claim, UNAVAILABLE claim, or zero
value; the Attempt is not counted as measured; and absence is not a measurement
failure. Change 3 makes no automatic or per-every-Attempt coverage claim.

### Valid finalizable request

When an exact request targets a completed, finalizable turn, acceptance creates
measurement eligibility for that exact Attempt and source. The supported
command must produce one final semantic outcome: `SAFE` or `UNAVAILABLE` with
exactly one stable reason. Required terminal evidence may not be silently
dropped after acceptance. Missing or failed required evidence follows the
existing fail-closed contract.

### Not-yet-finalizable request

If the exact target is still live and no authoritative completion signal is
present, return the distinct invocation state `REQUEST_NOT_YET_FINALIZABLE`.
Do not append a final sibling, report final SAFE, or persist final UNAVAILABLE
solely because collection was requested while the turn is progressing. This is
not a completed eligible measurement. The caller may retry after authoritative
completion. A terminal fact proving the target cannot complete is governed by
the existing final UNAVAILABLE contract; a live turn alone is not that fact.

### Coverage and integrity

```text
MEASUREMENT_INTEGRITY:
Every accepted finalizable collection request resolves to SAFE or UNAVAILABLE.

MEASUREMENT_COVERAGE:
Only explicitly requested Attempts are covered by this Change 3 contract.

UNIVERSAL_AUTOMATIC_COVERAGE:
OUTSIDE CHANGE 3
```

Do not infer a 100% coverage rate or claim that all governed Attempts are
measured. A future universal-coverage capability would require separate design
and authorization and is not a prerequisite for Change 3.

## Definition compatibility

This decision is compatible with the active effective Definition
`PREDECESSOR DEFINITION + AMENDMENT V2`. The Definition governs the integrity of
an operation once it is eligible for measurement: it must resolve to
source-bound SAFE usage or explicit UNAVAILABLE under the selected method. It
does not require every governed Attempt to become automatically
measurement-eligible. E1 therefore clarifies eligibility and coverage without
weakening fail-closed evidence requirements or changing the Definition.

If later repository evidence contradicts this compatibility reading, stop and
return the exact contradiction for owner adjudication; do not silently amend
the Definition.

```text
FORMAL_READINESS_STARTED: NO
T00_STARTED: NO
T00_AUTHORIZED: NO
IMPLEMENTATION_AUTHORIZED: NO
09_G_STARTED: NO
NEXT_SINGLE_GATE:
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V4
```
