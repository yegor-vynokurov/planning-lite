# PL-V39-08 RunReceipt Measurement Correction — Definition Amendment v4 Review

Review date: 2026-09-29
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Review action: OWNER_REVIEW_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V4
Reviewed candidate: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v4.md
Reviewed candidate SHA256: b4f12b4eba25ba24063c68d310009233018014d48a70f4e264513e08fe2d60eb

Entry state:
- HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
- AUTHORITY_STATE_ID: c1560e8349c32b594422d9c831486988b23e16ea19878dc04eef9bb386a3ed4b
- CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
- UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
- SYNC_STATE_ID: d876f4367fb3a1476c115ce21ad26d20d12e9f2f2df4861e5a71f55972c598f6
- INDEX_EMPTY: YES

## Owner review verdict

OWNER_REVIEW_VERDICT: REVIEW_FAIL / 1 MATERIAL FINDING
MATERIAL_FINDING_COUNT: 1
ROUTE_B_DIRECTION_REJECTED: NO
ROUTE_B_DIRECTION_PRESERVED: YES
V3_01: CLOSED_BY_V4
V3_02: CLOSED_BY_V4
AMENDMENT_V4_APPROVED: NO
CORRECTED_V5_REQUIRED: YES
IMPLEMENTATION_AUTHORIZED: NO
09_G_STARTED: NO

## Material finding V4-01 — bounded complete-total quality contradiction

V4 defines BOUNDED as a source-derived numeric claim whose explicit limitation
prevents a stronger or complete-scope claim. It then permits a BOUNDED numeric
value to use COMPLETE_TOTAL, including for the whole declared WORK_WINDOW when
membership and coverage are complete. Those rules conflict: a number cannot
simultaneously be a BOUNDED incomplete-scope claim and a complete total for
that same declared scope without a distinct semantic limitation. As written, a
consumer could see DIRECT / COMPLETE_TOTAL / 10M and BOUNDED / COMPLETE_TOTAL /
7M with no coherent quality distinction, recreating comparison ambiguity.

V3-01 and V3-02 are closed by v4's prospective, auditable work-window
membership rules and its explicit bounded-subset/lower-bound semantics. The
remaining correction is limited to V4-01: separate scope, quality, numeric
claim kind, and completeness; require a whole-scope exact total to be DIRECT
with COMPLETE_SCOPE_TOTAL; prohibit BOUNDED from claiming COMPLETE_SCOPE_TOTAL
for its declared scope; and define structured comparison safety. Exact
persisted field names need not be frozen.

## Disposition and next gate

Route B remains the owner-selected direction. Amendment v4 is not approved and
remains inactive. This review does not activate a Definition or Plan,
authorize implementation, alter T00 evidence, adjudicate the preserved
candidate, or start 09-G.

Prepare a narrowly corrected Amendment v5 candidate addressing V4-01 only.
Keep the effective Definition at predecessor plus Amendment v2 and the
effective Plan at predecessor plus Plan Amendment v4. Implementation remains
unauthorized; the preserved corrective candidate remains unchanged with
disposition unresolved.

NEXT_SINGLE_GATE: OWNER_REVIEW_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V5
