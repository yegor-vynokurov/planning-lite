# PL-V39-08 RunReceipt Measurement Correction Provider-Neutral Coarse Efficiency Owner Decision v1

```text
Transition: OWNER_DECISION_CHANGE_3_RESPONSE_AGGREGATE_POST_T00_SEAM_DISPOSITION
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Decision date: 2026-09-29
Decision source: EXPLICIT_HUMAN_OWNER

OWNER_DECISION: SELECT_ROUTE_B_PROVIDER_NEUTRAL_COARSE_EFFICIENCY_MEASUREMENT
ROUTE_STATUS: OWNER_SELECTED / NOT YET MATERIALIZED AS EFFECTIVE DEFINITION
EXACT_ATTEMPT_BRIDGE_MVP_REQUIRED: NO
EXACT_ATTEMPT_ATTRIBUTION: DEFERRED_PRECISION_UPGRADE
PROVIDER_NEUTRAL_CORE: REQUIRED
COARSE_SCOPE_MEASUREMENT: ACCEPTED DIRECTION
ATTRIBUTION_GRANULARITY_SEPARATE_FROM_CONFIDENCE: YES
TOKEN_SAVINGS_ALONE_SUFFICIENT: NO
UNIVERSAL_EFFICIENCY_SCALAR_REQUIRED: NO
FIXED_STATISTICAL_TOLERANCE_PROMISED: NO

DEFINITION_AMENDMENT_REQUIRED: YES
PLAN_AMENDMENT_REQUIRED_AFTER_DEFINITION: YES
IMPLEMENTATION_AUTHORIZED: NO
CANDIDATE_DISPOSITION_AUTHORIZED: NO
09_G_STARTED: NO
09_G_SEMANTICS_REPLACED: NO
NEXT_SINGLE_GATE: PREPARE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V3
```

## Entry state and accepted T00 record

The strict entry `SYNC_CAPSULE_V1` reproduced with SHA256
`aa50d323967ccc84cd55d612b886d08ad21292f02b1961af7cdbd48165d2ac99`.
Entry HEAD was `19217522f3dac695602a8534d7ddb8f9bbee5858`; the index was empty.
The accepted T00 review checkpoint
`docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-RESPONSE-AGGREGATE-T00-CONTROLLED-DISCOVERY-REVIEW-v1.md`
matched SHA256
`790ac10491c0d175cb099c45b00903bf61ea088e2fd0fe11da1d47d631f066dd`.
T00 was executed once, returned `STOP_WITH_PROVEN_SEAM`, and is consumed. It
is not reexecuted. The prior `READY_WITH_CONTROLLED_DISCOVERY` Formal Readiness
verdict remains historical; current closure remains
`BLOCKED_AFTER_CONTROLLED_DISCOVERY`, with implementation unauthorized.

The accepted runtime evidence remains four official not-proven material seams:
three roots (`AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING_NOT_PROVEN`,
`ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN`, and
`POST_TURN_COMPLETION_SIGNAL_NOT_PROVEN`) plus the dependent
`POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`, which materially depends
on Q1. No seam was closed by this owner decision. Q5-Q8 remain accepted only
within their recorded bounded scope: stable provider-source reading is
feasible; inspected Codex structured native usage is usable; typed sibling
coexistence is structurally feasible but unimplemented; and the prior
eight-path surface was sufficient for the exact-response design. Q8 does not
establish the write surface for the future provider-neutral MVP.

## Owner direction

The owner selected Route B. Change 3 should be semantically revised toward a
provider-neutral, coarse-grained resource-observation capability for later
Planning Lite efficiency comparisons. The MVP will not require a Codex-specific
Attempt-to-turn/response bridge. Exact Attempt-level attribution is deferred
as a precision upgrade, and exact response-aggregate Attempt mode is preserved
as a future optional precision capability.

The primary purpose is to compare useful work against resource use across
prompt, skill, checklist, provider, model, and other relevant configuration
versions. Coarse comparisons may identify approximately doubled context,
substantially reduced resource use, materially more rework for similar spend,
or materially better accepted output for similar spend. Differences around ten
percent are not the present primary target. This decision makes no fixed
statistical tolerance promise.

Planning Lite owns a provider-neutral semantic layer. Provider-specific
telemetry belongs behind adapters or evidence producers. Provider-native token
counts retain provider, model, native usage semantics, measurement method,
measurement scope, and confidence/provenance. The system must not assume a
token from one provider or model is a universally comparable physical unit.
Direct token deltas are strongest with provider/model and relevant conditions
held sufficiently stable. Cross-provider analysis belongs to a wider future
efficiency vector that may include cost, time, accepted output, rework, review
burden, and owner attention.

The future Definition should distinguish measurement scope or attribution
granularity from measurement confidence or quality. Conceptual scopes may
include work window, session, turn, and Attempt; conceptual quality states may
include exact, bounded, estimated, and unavailable. These names and invariants
are not frozen here. A truthful coarse scope with strong confidence is
preferable to guessed Attempt attribution. Never divide provider usage among
Attempts to manufacture operation-local measurements: no equal division,
timestamp-proportional division, latest-turn heuristic, or proximity
attribution.

Efficiency is multidimensional. Token savings alone are insufficient, and
Change 3 does not define a universal scalar Efficiency Score. Preserve a vector
of relevant observations, potentially including accepted outputs and plan/task
items, quality/correctness, rework, retries, review/readiness loops, owner
interventions, context/resource use, meaningful wall-clock time, and available
financial or compute cost.

## Authority effect and limits

The existing Definition Amendment v2 and Plan Amendment v4 remain effective
authority until formally amended or superseded. This owner decision does not
itself change active product semantics, adopt a storage or serialization
schema, amend the Definition or Plan, adjudicate the preserved corrective
candidate, authorize implementation, or start 09-G. It authorizes preparation
of a new Definition Amendment candidate only. A Plan Amendment is required
after the Definition Amendment. The amendment preparation must reconcile the
predecessor operation-local SAFE/UNAVAILABLE semantics, Option C, E1, T00
seams and proven Q5-Q8, coarse scopes, provider neutrality,
attribution/confidence semantics, compatibility and backward readability,
deferred exact Attempt attribution, and work reserved for later efficiency and
09-G capabilities.

PL_V39_09_G_STARTED: NO
PL_V39_09_G_SEMANTICS_REPLACED: NO
IMPLEMENTATION_AUTHORIZED: NO
PRESERVED_CANDIDATE: UNCHANGED / DISPOSITION UNRESOLVED
CANDIDATE_DISPOSITION_AUTHORIZED: NO
T00_REEXECUTION_AUTHORIZED: NO

## Next permitted action

`PREPARE_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V3`

Preparation is limited to a candidate amendment for independent review. It is
not activation, a Plan amendment, candidate disposition, Formal Readiness,
implementation, or 09-G execution.

## Write and validation boundary

The only repository paths authorized for this transition are:

1. `docs/design/project-spine/CURRENT.md`
2. This owner-decision checkpoint.

No source, test, Roadmap, existing Definition or Plan, T00 evidence,
Formal Readiness verdict, candidate, or unrelated-dirt path is authorized to
change. No staging, commit, push, release, implementation, candidate
disposition, or T00 reexecution is part of this transition.
