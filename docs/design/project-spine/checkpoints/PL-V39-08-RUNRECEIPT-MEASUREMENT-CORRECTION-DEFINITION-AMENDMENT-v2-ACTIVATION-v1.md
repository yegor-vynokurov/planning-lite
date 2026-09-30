# PL-V39-08 RunReceipt Measurement Correction - Definition Amendment v2 Activation

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: OWNER_REVIEW_ACCEPT_AND_ACTIVATE_DEFINITION_AMENDMENT_V2
owner_decision_source: EXPLICIT_HUMAN_OWNER
transition_date: 2026-09-29
review_gate: OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_DEFINITION_AMENDMENT_V2
review_verdict: REVIEW_PASS / 0 MATERIAL FINDINGS
material_finding_count: 0
reviewed_candidate: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v2.md
reviewed_candidate_sha256: e7a47f46c9838ba94ae66acea56c76768e72844a881bf394cfa8fd28bbafa544

## Owner review and acceptance

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_DEFINITION_AMENDMENT_V2:
REVIEW_PASS / 0 MATERIAL FINDINGS

A_01_DESCRIPTIVE_COMPLETENESS_SEMANTICS_REGRESSED:
CLOSED

OPTION_C_DIRECTION:
ACCEPTED

DEFINITION_AMENDMENT_V2:
APPROVED_BY_OWNER / ACTIVE

PREDECESSOR_DEFINITION:
IMMUTABLE HISTORICAL AUTHORITY

EFFECTIVE_CHANGE_3_DEFINITION:
PREDECESSOR + AMENDMENT_V2

IMPLEMENTATION_AUTHORIZED:
NO

PLAN_AMENDMENT_REQUIRED:
YES

09_G_STARTED:
NO
```

The review accepts the exact v2 candidate. Its descriptive-completeness
semantics preserve safety independently from missing `actual_model`,
`actual_effort`, or `agent_role`; missing values remain explicit `null` and
`telemetry_completeness: PARTIAL`. Method-specific identity, response scope,
numeric usage, binding, deduplication, reconciliation, route, and fail-closed
requirements remain in force. This acceptance does not authorize implementation
or alter historical RunReceipt data.

The owner accepts `SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT` as the
semantic direction. `RESPONSE_AGGREGATE` is the preferred Codex method when its
exact source and binding contract is proven. `BOUNDARY_DELTA` remains a fallback
only under its own proven authoritative-boundary contract. Existing cumulative
fields and predecessor v1 delta meanings remain unchanged.

## Scoped disposition of R-01 and R-02

```text
R-01 SAFE_BOUNDARY_PROVENANCE_NOT_BOUND:
REMAINS OPEN FOR BOUNDARY_DELTA CURRENT CORRECTIVE CANDIDATE
/
SUPERSEDED AS A CODEX RESPONSE_AGGREGATE BLOCKER

R-02 M13_CAPTURE_TO_GOVERNED_HANDOFF_NOT_PROVEN:
REMAINS OPEN FOR BOUNDARY_DELTA CURRENT CORRECTIVE CANDIDATE
/
SUPERSEDED AS A CODEX RESPONSE_AGGREGATE BLOCKER
```

Neither historical finding is represented as fixed. Both remain true against
the preserved boundary-delta-only corrective candidate. They do not block the
separately accepted response-aggregate path. Its first unresolved seam is
`AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING`.

## Effective authority and boundaries

The approved predecessor Definition remains immutable historical authority.
Amendment v2 is active as an additive semantic amendment; the effective Change
3 Definition is the predecessor plus Amendment v2. The earlier v1 Amendment
candidate remains unchanged review history and is not approved. The Option C
sync-correction v2 clarifies historical state-ID bookkeeping without rewriting
the v1 correction or the Option C owner-decision checkpoint.

```text
IMPLEMENTATION_PLAN_AMENDMENT:
CANDIDATE PREPARATION AUTHORIZED / OWNER REVIEW REQUIRED

IMPLEMENTATION_AUTHORIZED:
NO

FORMAL_READINESS:
NOT STARTED

09_G:
NOT STARTED

NEXT_SINGLE_GATE:
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_IMPLEMENTATION_PLAN_AMENDMENT_V1
```

Preparation of one Implementation Plan Amendment candidate is authorized by
this transition. That candidate remains unapproved. Any later implementation
requires owner review of that Plan Amendment, Formal Readiness, and a separate
explicit implementation authorization.
