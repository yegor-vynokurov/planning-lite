# PL-V39-08 RunReceipt Measurement Correction — Corrective Candidate Review

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
review_gate: OWNER_REVIEW_CHANGE_3_CORRECTIVE_IMPLEMENTATION_CANDIDATE
review_verdict: REVIEW_FAIL / 2 MATERIAL FINDINGS
material_finding_count: 2

entry_head: 19217522f3dac695602a8534d7ddb8f9bbee5858
entry_authority_state_id: e59579875dbd20fa3663d207e2815a59edb3cb6485226e5deed8153ccb21167f
entry_candidate_state_id: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
entry_unrelated_dirt_state_id: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
entry_sync_state_id: 002fb6ee8f5a7fef6507f54d9d50f4814010c9cf90d0819b3375671ea14a9c62
entry_index_empty: YES

corrective_execution_report: D:\documents\planning-lite-sync\CHANGE_3_CORRECTIVE_IMPLEMENTATION_EXECUTION_V1.md
corrective_execution_report_sha256: b7c1e0a517c0770d77d57a8de0bfd52e76592c98ab40ed9b0f19bf35c99a490f
corrective_candidate_patch: D:\documents\planning-lite-sync\CHANGE_3_CORRECTIVE_IMPLEMENTATION_CANDIDATE.patch
corrective_candidate_patch_sha256: c6649bc64f83bdbaf850fe8f7492f5ed5bc4f5aec9fcfe0907a0f9560e119686
corrective_implementation_authorization_sha256: 46ee8ac642588b946e1d8af085d95661ebae03389b4629885faafd187406edbc
prior_candidate_review_sha256: 67a92b8f72377fd8f948a731380bf2dd7f40816a03e3541825840b7a61071aa8

## Accepted corrective results

- F-02 `M01_ADJACENT_TURN_CONTRACT_NOT_PROVEN`: CLOSED. M01 uses distinct same-session before/after turn identities and asserts exact SAFE deltas.
- F-04 `AMBIGUOUS_BOUNDARY_ALIASES_NOT_FAIL_CLOSED`: CLOSED. Conflicting session, turn, and counter aliases fail closed; equal duplicate aliases remain valid.
- F-01 authoritative operation/route reference-binding subproblem: CLOSED. Current lifecycle-owned pre-execution evidence controls the operation trace and expected-route references; forged references cannot survive as SAFE.
- F-03 persistence/readback subproblem: CLOSED. M13 uses the real `collect_governed_receipt`, canonical append, and persisted readback without monkeypatching the persistence owner.

## Open material findings

### R-01 — SAFE_BOUNDARY_PROVENANCE_NOT_BOUND

Severity: MATERIAL / SAFETY CONTRACT

The corrective lifecycle binding proves the current `operation_trace_ref` and `expected_route_ref`, but does not prove provenance or timing for incoming `counter_before_boundary`, `counter_after_boundary`, `counter_scope`, or host session/turn counter facts. Internally valid supplied values and matching lifecycle references can therefore remain SAFE without proving that the before boundary was captured before the governed operation or that the after boundary came from the same host session and compatible counter scope.

Controlled Discovery established that the current accepted host capture seam has no authoritative pre-operation counter boundary, no proven explicit `counter_scope`, no proven same-session before/after pair, and no proven compatible counter scope. Arithmetic validity and matching route/trace references are insufficient evidence of authoritative operation-local observations. The current manually constructed SAFE measurement test proves reference binding, not boundary provenance.

Disposition: Do not accept the candidate while a current governed path can retain SAFE without proven boundary provenance. Do not widen architecture in this review.

### R-02 — M13_CAPTURE_TO_GOVERNED_HANDOFF_NOT_PROVEN

Severity: MATERIAL / REQUIRED END-TO-END EVIDENCE

Corrected M13 proves `execute_governed_operation` → real `collect_governed_receipt` → canonical append → persisted readback, but its input `RunReceipt` is manually constructed with `runtime_source=external_runtime`. It does not exercise `scripts/capture_codex_run_receipts.py`. The separate capture walking-skeleton test proves that adapter's own capture → append/readback path, but does not pass the captured evidence into the governed lifecycle and collector.

The required single chain remains unproven: existing structured capture producer → governed lifecycle → governed collector → canonical append → exact readback. M13 is NOT PROVEN. Do not invent a handoff or add instrumentation, producer, store, authority, or architecture during review.

FIRST_BROKEN_SEAM: `NO_AUTHORITATIVE_CAPTURE_TO_GOVERNED_BOUNDARY_HANDOFF_PROVEN`

## Execution evidence accepted

Accept the corrective execution evidence: the authorized six-file ceiling was respected and only four authorized files changed; 96 focused tests, 8 operation-trace regression tests, and 746 full-suite tests passed (88 warnings); strict resume validation and `git diff --check` passed; the index was empty; unrelated dirt was unchanged; governance was unchanged during implementation; no architecture expansion occurred; and 09-G did not start. These execution facts do not override R-01 or R-02.

## Candidate and governance disposition

corrective_candidate_state_id: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
candidate_disposition: PRESERVE / DO NOT COMMIT
candidate_revert: NOT AUTHORIZED
commit_authorized: NO
architecture_expansion_authorized: NO
implementation_authorized: YES / EXISTING BOUNDED CHANGE 3 PLAN; NO ADDITIONAL CORRECTIVE PASS AUTHORIZED
09-G: NOT STARTED
owner_decision_A_or_B: NOT SELECTED
next_single_gate: OWNER_DECISION_CHANGE_3_BOUNDARY_PROVENANCE_AND_CAPTURE_HANDOFF_DISPOSITION

This owner-review transition does not mutate the corrective implementation candidate, source, tests, telemetry, templates, Roadmap, or unrelated dirt. It does not stage, commit, push, authorize another corrective pass, select option A or B, expand architecture, or start 09-G.
