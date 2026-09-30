# PL-V39-08 RunReceipt Measurement Correction — Definition Amendment v3 Review

Review date: 2026-09-29
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Review action: OWNER_REVIEW_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V3
Reviewed candidate: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v3.md
Reviewed candidate SHA256: e3d18b2cbd70f00f764c968d0a13e619ccef6a395703fed9ecb21c734103dbf0

Entry state:
- HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
- AUTHORITY_STATE_ID: 34cc8696249c671c4726d97da6de2534d12173650c6b31e9eb8520c9a3845f8c
- CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
- UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
- SYNC_STATE_ID: f3033cdb04e9a73b1a4a34cb370890d9502b96a10c9af408cf3631adc2094161
- INDEX_EMPTY: YES

## Review verdict

REVIEW_VERDICT: REVIEW_FAIL / 2 MATERIAL FINDINGS

V3_01: WORK_WINDOW_MEMBERSHIP_AND_SOURCESET_BINDING_UNDERDEFINED

V3_02: BOUNDED_NUMERIC_CLAIM_SEMANTICS_UNDERDEFINED

ROUTE_B_DIRECTION_REJECTED: NO
ROUTE_B_DIRECTION_PRESERVED: YES
AMENDMENT_V3_APPROVED: NO
CORRECTED_V4_REQUIRED: YES
IMPLEMENTATION_AUTHORIZED: NO
09_G_STARTED: NO

## Material finding V3-01 — work-window membership and source-set binding

V3 names a predeclared work window and configuration arm, but a temporal interval does not establish which concrete provider records belong to that arm. The same provider may be used for Poker and unrelated work during the same week. Timestamp overlap alone therefore cannot prove configuration attribution or source membership.

A corrected definition must require stable window and configuration/arm identities, declared start and closure semantics, and a prospective deterministic membership rule with explicit inclusions and exclusions. It must preserve auditable per-source provenance showing the source identity, binding, rule/version, configuration identity, inclusion decision, and reason. The concrete future session list need not be known before the window starts; sources can be registered deterministically as they appear.

Membership may be established by a dedicated session bound to the window, sessions explicitly registered to it, records carrying an independently reliable window/configuration binding, or another deterministic provider-neutral mechanism. The definition must prohibit timestamp-only membership, post-hoc semantic/content or prompt/body classification, latest/nearest/proximity selection, and retrospective cherry-picking.

A source containing inseparable target-configuration and unrelated work cannot have its whole total reported as DIRECT usage for the target configuration. A truthful narrower bounded claim may be reported only with explicit numeric claim semantics and a declared subject/source set; otherwise the target claim is UNAVAILABLE.

## Material finding V3-02 — bounded numeric claim semantics

V3 says BOUNDED is not estimation and that incomplete coverage is not a complete total, but a consumer could still mistake a number such as WORK_WINDOW / BOUNDED / 7M tokens for a complete-window total when comparing it with a DIRECT total.

Every BOUNDED numeric observation must expose machine-readable or otherwise explicit claim semantics that distinguish a complete total from an exact observed subset, a proven lower bound, or another precisely defined bounded claim. The claim must name its subject/source set. BOUNDED must never mean that an observed fraction is probably close to a total. Extrapolation, scaling, statistical filling, and guessed missing usage are prohibited. If the visible fraction is unknown and no useful truthful numeric claim exists, use UNAVAILABLE.

Quality describes which epistemic claim is justified for the numeric quantity. Completeness describes which expected sources and requested or optional metrics are present, absent, partial, or unknown. These axes are independent. Exact whole-window input/output with an absent optional reasoning metric may remain DIRECT for the supported quantities while metric completeness is PARTIAL. Populated fields for only some observed source records do not make complete-window usage DIRECT.

## Disposition and next gate

Route B remains the owner-selected direction. This review does not reject or replace it, does not close or redefine any accepted T00 seam, and does not activate a definition or plan. Amendment v3 remains immutable failed-review history and is not approved.

Prepare a corrected Amendment v4 candidate addressing both findings. Keep the effective Definition at predecessor plus Amendment v2 and the effective Plan at predecessor plus Plan Amendment v4. Implementation remains unauthorized; the preserved corrective candidate remains unchanged with disposition unresolved; 09-G remains not started.

NEXT_SINGLE_GATE: OWNER_REVIEW_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V4
