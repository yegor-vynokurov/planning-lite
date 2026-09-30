# PL-V39-08 RunReceipt Measurement Correction ? Definition Amendment v6 Owner Acceptance and Activation

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: OWNER_ACCEPT_AND_ACTIVATE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V6
transition_date: 2026-09-29
owner_decision_source: EXPLICIT_HUMAN_OWNER
owner_decision: ACCEPT_AND_ACTIVATE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V6

OWNER_DECISION_SOURCE: EXPLICIT_HUMAN_OWNER
OWNER_DECISION: ACCEPT_AND_ACTIVATE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V6
AMENDMENT_V6: APPROVED_BY_OWNER / ACTIVE
AMENDMENT_V6_SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74
INDEPENDENT_REVIEW: REVIEW_PASS / 0 MATERIAL FINDINGS
ACTIVE_EFFECTIVE_DEFINITION: PREDECESSOR + AMENDMENT V2 + AMENDMENT V6
ACTIVE_MEASUREMENT_ROUTE: ROUTE_B_PROVIDER_NEUTRAL_COARSE_EFFICIENCY_MEASUREMENT
ACTIVE_EFFECTIVE_PLAN: PREDECESSOR + PLAN AMENDMENT V4
PLAN_V4_ROUTE_B_IMPLEMENTATION_AUTHORITY: NO
NEW_ROUTE_B_PLAN_AMENDMENT_REQUIRED: YES
NEW_ROUTE_B_PLAN_AMENDMENT_PREPARED: NO
FUTURE_PLAN_VERSION_PREASSIGNED: NO
FORMAL_READINESS_FOR_ROUTE_B: NOT PERFORMED
IMPLEMENTATION_AUTHORIZED: NO
CANDIDATE_DISPOSITION_AUTHORIZED: NO
T00_REEXECUTION_AUTHORIZED: NO
09_G_STARTED: NO
NEXT_SINGLE_GATE: PREPARE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_IMPLEMENTATION_PLAN_AMENDMENT

## Acceptance basis

Amendment v6 received independent review:

REVIEW_PASS / 0 MATERIAL FINDINGS
SEMANTIC_CONTRACT_REVIEW: PASS
GOVERNANCE_LINEAGE_REVIEW: PASS

Reviewed candidate:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v6.md

AMENDMENT_V6_SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74
INDEPENDENT_REVIEW_PATH: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v6-REVIEW-v1.md
INDEPENDENT_REVIEW_SHA256: 7ea6e8436850e5f761558691f7cb43bb92a8a630d0e5ffd2ec35038fa602b464
MATERIAL_FINDINGS: 0

## Owner decision and effective Definition

DEFINITION_AMENDMENT_V6: APPROVED_BY_OWNER / ACTIVE
ACTIVE_EFFECTIVE_DEFINITION: PREDECESSOR + AMENDMENT V2 + AMENDMENT V6
ACTIVE_MEASUREMENT_ROUTE: ROUTE_B_PROVIDER_NEUTRAL_COARSE_EFFICIENCY_MEASUREMENT
IMPLEMENTATION_AUTHORIZED: NO

Amendment v6 supersedes conflicting predecessor and Amendment v2 clauses
exactly as declared in its relationship-to-predecessor table. Historical
Definition v1 and Amendment v2 are not rewritten. Historical Option C, E1,
T00, and earlier amendment evidence remain immutable.

The accepted Route B semantic contract is now active. It defines a
provider-neutral Resource Observation core across WORK_WINDOW, PROVIDER_SESSION,
PROVIDER_TURN, and PLANNING_ATTEMPT scopes. WORK_WINDOW membership is
prospective and deterministic, separate from temporal boundaries, and carries
auditable inclusion/exclusion provenance. Mixed-source contamination fails
closed. Scope, quality, numeric claim kind, and completeness remain independent
axes. Quality values are DIRECT, BOUNDED, and UNAVAILABLE. Claim kinds are
COMPLETE_SCOPE_TOTAL, EXACT_OBSERVED_SUBSET, PROVEN_LOWER_BOUND, and
OTHER_PRECISELY_DEFINED_NONCOMPLETE_CLAIM. DIRECT plus COMPLETE_SCOPE_TOTAL is
used for supported exact whole-scope quantities; BOUNDED cannot claim a
complete total for its declared scope. Extrapolation, scaling, statistical
filling, and guessed attribution are prohibited. E1 is specialized to
PLANNING_ATTEMPT. NO REQUEST means NO MEASUREMENT CLAIM; the not-yet-finalizable
request state is generalized by declared scope. Resource Observation is not
an Efficiency Judgment. Provider-native resource semantics are retained with
no universal cross-provider token unit. Token savings alone cannot establish
an efficiency judgment, and no universal Efficiency Score is defined.
Historical RunReceipt v1/v2 meanings remain unchanged and no historical
backfill is authorized.

## Plan and readiness boundary

ACTIVE_EFFECTIVE_PLAN: PREDECESSOR PLAN + IMPLEMENTATION PLAN AMENDMENT V4
PLAN_AMENDMENT_V4_SHA256: e9f2d09f4f8bac0fef81f8a9c79630cf8c65edd6b9084406fd2c9242a9430981
PLAN_V4_ROUTE_B_IMPLEMENTATION_AUTHORITY: NO
NEW_ROUTE_B_PLAN_AMENDMENT_REQUIRED: YES
NEW_ROUTE_B_PLAN_AMENDMENT_PREPARED: NO
FUTURE_PLAN_VERSION_PREASSIGNED: NO
FORMAL_READINESS_FOR_ROUTE_B: NOT PERFORMED
ROUTE_B_FORMAL_READINESS_REQUIRES: NEW REVIEWED/ACCEPTED PLAN AMENDMENT FIRST

The prior BLOCKED_AFTER_CONTROLLED_DISCOVERY Formal Readiness closure remains
historical closure for the superseded implementation route; it is not a
current Route B readiness verdict. This activation does not prepare or approve
a Plan Amendment and does not authorize Formal Readiness or implementation.

## Preserved evidence and boundaries

T00: EXECUTED / ACCEPTED / CONSUMED / STOP_WITH_PROVEN_SEAM
T00_REEXECUTION_AUTHORIZED: NO
Q1-Q4: PRESERVED NOT_PROVEN EVIDENCE / NOT DECLARED REPAIRED
Q1-Q4_COARSE_ROUTE_BLOCKING: NO / SCOPE-SPECIFIC UNDER ACTIVE V6
Q5-Q8: PRESERVED BOUNDED SUPPORTING EVIDENCE
EXACT_ATTEMPT_MEASUREMENT: OPTIONAL FUTURE PRECISION
PRESERVED_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
CANDIDATE_DISPOSITION: UNRESOLVED
CANDIDATE_DISPOSITION_AUTHORIZED: NO
09_G_STARTED: NO
09_G_SEMANTICS_REPLACED: NO

Change 3 provides the resource-observation substrate only; 09-G remains
separate. The preserved corrective implementation candidate is unchanged and
its disposition remains unresolved.

NEXT_SINGLE_GATE:
PREPARE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_IMPLEMENTATION_PLAN_AMENDMENT
