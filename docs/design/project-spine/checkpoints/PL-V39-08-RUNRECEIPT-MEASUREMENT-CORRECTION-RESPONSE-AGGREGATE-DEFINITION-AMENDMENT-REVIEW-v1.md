# PL-V39-08 RunReceipt Measurement Correction - Definition Amendment v1 Owner Review

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
review_gate: OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_DEFINITION_AMENDMENT
review_verdict: REVIEW_FAIL / 2 MATERIAL FINDINGS
material_finding_count: 2
review_source: EXPLICIT_HUMAN_OWNER
reviewed_candidate: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v1.md
reviewed_candidate_sha256: ec31d84aa97b1aecf2b8763e3423221d10072ac85a8799eed5700b81aeee7335
review_date: 2026-09-28

## Disposition

```text
OPTION_C_DIRECTION_REJECTED: NO
OPTION_C_DIRECTION_PRESERVED: YES
DEFINITION_AMENDMENT_V1_APPROVED: NO
CORRECTED_AMENDMENT_REQUIRED: YES
IMPLEMENTATION_AUTHORIZED: NO
PLAN_AMENDMENT_AUTHORIZED: NO
09_G_STARTED: NO
```

The review rejects approval of the exact v1 Amendment text, while preserving the
owner's semantic Option C decision. The v1 candidate remains unchanged as review
history. A corrected v2 candidate has been prepared at:

```text
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v2.md
```

The v2 candidate is not approved or activated. It requires a fresh owner review.
No Plan Amendment is prepared, and implementation remains unauthorized.

## Material finding A-01 - DESCRIPTIVE_COMPLETENESS_SEMANTICS_REGRESSED

The v1 candidate made complete telemetry part of `BOUNDARY_DELTA` safety and
said a completeness failure produces `UNAVAILABLE`. This regresses the approved
predecessor Definition's separation between measurement safety and descriptive
metadata completeness. Missing `actual_model`, `actual_effort`, or `agent_role`
alone must not make otherwise safe evidence `UNAVAILABLE`; each missing value
must be represented explicitly as `null`, and descriptive completeness must be
reported as `telemetry_completeness: PARTIAL`.

This independence applies to both `BOUNDARY_DELTA` and `RESPONSE_AGGREGATE`.
The predecessor semantics allow `SAFE + COMPLETE`, `SAFE + PARTIAL`, and
`UNAVAILABLE + PARTIAL`; `UNAVAILABLE + COMPLETE` is invalid under the
predecessor v1 contract. No metadata may be guessed. This finding does not
weaken method-specific numeric, source, identity, scope, binding, reconciliation,
route, or fail-closed requirements.

Disposition: corrected in the v2 candidate; pending owner review.

## Material finding G-01 - SYNC_PARTITION_AND_STATE_ID_SEMANTICS_DRIFT

The historical Option C owner-decision checkpoint records state IDs using
noncanonical state-ID and partition semantics. This is a bookkeeping defect in
that checkpoint only. It does not invalidate or alter
`SELECT_OPTION_C_RESPONSE_BOUND_OPERATION_MEASUREMENT`, the accepted external
evidence bindings, or the semantic Option C direction.

The exact superseding bookkeeping correction and canonical reconciliation are
recorded in:

```text
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-OPTION-C-SYNC-CORRECTION-v1.md
```

That checkpoint supersedes only the noncanonical repository state-ID/partition
bookkeeping. The historical owner-decision checkpoint itself remains unchanged.

## Next gate

```text
OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_DEFINITION_AMENDMENT_V2
```
