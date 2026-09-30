# PL-V39-08 RunReceipt Measurement Correction - Implementation Plan Amendment v5 Review v1

Review date: 2026-09-29
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Review action: OWNER_REVIEW_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_IMPLEMENTATION_PLAN_AMENDMENT_V5
Reviewer: Codex / independent plan review

Reviewed candidate: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5.md
Reviewed candidate SHA256: b68ecd94456c9d00fcbca6524ee8063165fa95889e16f834a0416105fd2454db

## Entry state and active basis

HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
AUTHORITY_STATE_ID: 68875efc0da0788276b7de70631a78d3928e7073ba338028b712e122067e099d
CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
SYNC_STATE_ID: 63a806437d51e01b394b8bf36efa579bd7532bb6a5c761340f616fe0fb333643
INDEX_EMPTY: YES

Active Definition: PREDECESSOR + AMENDMENT V2 + AMENDMENT V6
Definition Amendment v6 SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74
Definition Amendment v6 review SHA256: 7ea6e8436850e5f761558691f7cb43bb92a8a630d0e5ffd2ec35038fa602b464
Definition Amendment v6 activation SHA256: 94967e652ac0640a9465caa5af15b14f57438b1f4f71063489ecd5eb68b11dd6
Effective Plan before v5: PREDECESSOR + PLAN AMENDMENT V4
Plan Amendment v4 SHA256: e9f2d09f4f8bac0fef81f8a9c79630cf8c65edd6b9084406fd2c9242a9430981

## Review verdict

REVIEW_VERDICT: REVIEW_PASS / 0 MATERIAL FINDINGS
MATERIAL_FINDING_COUNT: 0
PLAN_SEMANTIC_ALIGNMENT: PASS
PLAN_EXECUTABILITY: PASS
PLAN_SCOPE_DISCIPLINE: PASS
BACKWARD_COMPATIBILITY_PLAN: PASS
CANDIDATE_COLLISION_HANDLING: PASS
GOVERNANCE_SEQUENCE: PASS

The reviewed Plan v5 is aligned with the active provider-neutral Definition v6. Its scope and executable sequence are narrow enough for the first useful Route B slice, and the stated acceptance coverage is adequate for that slice. The Plan preserves legacy receipt behavior, contains the preserved candidate collision behind a required later disposition gate, and keeps all approval and readiness transitions separate.

## Accepted Route B shape

ROUTE_B_VERTICAL_SLICE: WORK_WINDOW / ONE_DEDICATED_PROVIDER_SOURCE_SEGMENT
INITIAL_PROVIDER_ADAPTER: CODEX_LOCAL_ROLLOUT

The proposed lifecycle is explicit: open the Work Window; prospectively persist one exact source segment and immutable configuration reference; perform measured work; explicitly finalize; capture the exact end boundary; read only the registered segment; aggregate structured provider-native usage; persist a provider-neutral Resource Observation; and return canonical persisted readback.

The first Codex producer intentionally targets WORK_WINDOW + DIRECT + COMPLETE_SCOPE_TOTAL for supported exact quantities. If truthful complete measurement cannot be produced, the Plan uses REQUEST_NOT_YET_FINALIZABLE for an unstable source or UNAVAILABLE for a proven terminal source state. A BOUNDED producer is not required in the first implementation slice.

EXACT_ATTEMPT_BRIDGE_REQUIRED: NO
PLANNING_ATTEMPT_PRODUCER_IN_FIRST_SLICE: NO
OPERATION_LIFECYCLE_MUTATION_REQUIRED: NO

The provider-neutral Resource Observation core is separate from the Codex source adapter. Codex thread_id, response_id, and rollout/source path remain adapter or provenance concepts, not required universal Resource Observation identity.

## Work Window membership and configuration reference

The Plan requires prospective persisted registration, an explicit source_ref, one dedicated source segment, stable start/end byte boundaries, and auditable source identity. It does not use timestamp-only membership, prompt/body classification, latest/nearest source selection, or automatic discovery.

CONFIGURATION_REF_ROLE: DECLARED_IMMUTABLE_COMPARISON_ARM_REFERENCE / NOT AUTOMATICALLY PROVIDER-VERIFIED

This is a nonblocking implementation interpretation of the Plan's caller-supplied immutable prospective arm reference/fingerprint. It must not be described as provider-verified configuration identity unless independent source evidence proves that stronger claim. This interpretation is not a material finding and requires no Plan revision.

## Carrier and compatibility

Existing RunReceipt v1/v2 records remain unchanged and untagged, with legacy semantics preserved. WorkWindowRegistrationV1 and ResourceObservationV1 are additive typed siblings in the existing telemetry stream. The Plan requires no legacy delta reinterpretation, historical migration/backfill, or operation_measurement_v2 carrier.

## Proposed write surfaces

PROPOSED_PRODUCT_PATH_COUNT: 4
1. src/planning_lite/telemetry.py
2. scripts/capture_codex_run_receipts.py
3. src/planning_lite/codex_work_window.py
4. src/planning_lite/cli.py

PROPOSED_TEST_PATH_COUNT: 4
1. tests/test_run_receipts.py
2. tests/test_codex_run_receipt_capture.py
3. tests/test_codex_work_window.py
4. tests/test_cli.py

## Task sequence and acceptance

TASK_COUNT: 6
T-01: provider-neutral carrier and semantic validator
T-02: typed persistence/readback and legacy capture compatibility
T-03: Codex dedicated source-segment adapter
T-04: explicit CLI open/finalize surface
T-05: focused deterministic acceptance
T-06: separately authorized bounded real field proof

ACCEPTANCE_CASE_COUNT: 20

The A-01 through A-20 matrix covers legacy RunReceipt compatibility; typed sibling dispatch; prospective persisted registration; registration replay/conflict; no timestamp membership; source identity, replacement, and truncation; unstable-read not-yet-finalizable behavior; structured native-usage aggregation; duplicate deduplication/conflict; optional-metric null semantics; DIRECT + COMPLETE_SCOPE_TOTAL; no Attempt bridge; idempotent and conflicting finalization; canonical readback; exclusion of unregistered source material; concurrent write serialization; telemetry-disabled/unregistered-project stops; and no efficiency or 09-G judgment.

## Preserved candidate and field proof

PRESERVED_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
OVERLAP_COUNT: 4
Overlap paths:
- src/planning_lite/telemetry.py
- scripts/capture_codex_run_receipts.py
- tests/test_codex_run_receipt_capture.py
- tests/test_run_receipts.py

PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION_GATE: REQUIRED
CANDIDATE_DISPOSITION_AUTHORIZED: NO

The Plan identifies the two non-overlapping candidate paths as outside its proposed surface and the four exact collisions above as incompatible or potentially reusable only by concept. Review does not choose a candidate disposition or treat its worktree bytes as the canonical baseline.

FIELD_PROOF_DEFINED: YES
FIELD_PROOF_AUTHORIZED: NO

T-06 is defined, but this review does not authorize it. The Plan correctly places field proof after Plan acceptance/activation, candidate disposition, fresh Formal Readiness, implementation authorization and implementation, independent implementation review, and separate field-proof authorization.

## Exclusions and governance order

The first slice excludes exact Attempt measurement or bridge, multi-source Work Windows, automatic discovery or lifecycle, daemons/schedulers, additional providers, cross-provider normalization, monetary cost conversion, efficiency scoring, rework/owner-attention analysis, Experiment Registry, Prompt Garden, 09-G, historical backfill, and broad telemetry/lifecycle refactoring.

The next lifecycle remains: Plan v5 review PASS; separate human owner acceptance/activation; separate candidate disposition; fresh Route B Formal Readiness; separate implementation authorization; bounded T-01 through T-05 implementation; independent implementation review; separate T-06 authorization; then field proof and completion review.

PLAN_AMENDMENT_V5_REVIEWED: YES
PLAN_AMENDMENT_V5_ACTIVATED: NO
IMPLEMENTATION_AUTHORIZED: NO
CANDIDATE_DISPOSITION_AUTHORIZED: NO
FORMAL_READINESS_PERFORMED: NO
FIELD_PROOF_AUTHORIZED: NO
09_G_STARTED: NO
T00_RERUN: NO

This checkpoint records review only. It does not accept or activate Plan Amendment v5, adjudicate the preserved candidate, perform Formal Readiness, authorize implementation or field proof, modify source/tests or Roadmap, rerun T00, start 09-G, or stage, commit, push, or release.

## Write and validation boundary

The only authorized repository paths for this transition are:

1. docs/design/project-spine/CURRENT.md
2. docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5-REVIEW-v1.md

The Plan candidate, active Definition v6 and its review/activation, Plan v4, preserved candidate, source, tests, Roadmap, and unrelated dirt remain unchanged. The index remains empty. Validation is limited to the strict resume validator and git diff --check; no product tests are run.

