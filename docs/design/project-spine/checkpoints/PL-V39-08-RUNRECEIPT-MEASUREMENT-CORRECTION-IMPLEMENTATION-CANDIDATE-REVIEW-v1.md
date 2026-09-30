# PL-V39-08 RunReceipt Measurement Correction — Implementation Candidate Review

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
review_gate: OWNER_REVIEW_CHANGE_3_IMPLEMENTATION_CANDIDATE
review_verdict: REVIEW_FAIL / MATERIAL_FINDINGS
material_finding_count: 4

entry_head: 19217522f3dac695602a8534d7ddb8f9bbee5858
entry_authority_state_id: 2b14fa8259b254d75c28f8010ab58991193e24caadf3077b9ac16f6c45796ca8
entry_candidate_state_id: ff82d2e4ddb3811980b047bcf9ab97742b3b9d7a76070f2160732cf61daccf51
entry_unrelated_dirt_state_id: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
entry_sync_state_id: b4b78e98c00611d87c9aa475f16bb5b6001e58e359b9d8a11c343c25dec4591d

implementation_execution_report: D:\documents\planning-lite-sync\CHANGE_3_IMPLEMENTATION_EXECUTION_V1.md
implementation_execution_report_sha256: 2e91ce34e741b055aa7b24766f79541ee56632b8e2425e422083f5e3c86a092b
implementation_candidate_patch: D:\documents\planning-lite-sync\CHANGE_3_IMPLEMENTATION_CANDIDATE.patch
implementation_candidate_patch_sha256: 5e213def593be6755cdf60b48d77b0cdd185919582439bd15832448045571242

## Review disposition

The six-file implementation candidate is preserved in place. Execution evidence and
six-path scope compliance are accepted as evidence, but the candidate is not
accepted because four material semantic/evidence findings remain open.

## F-01 — AUTHORITATIVE_MEASUREMENT_SOURCE_BINDING_BYPASS

Severity: MATERIAL / SAFETY CONTRACT

Finding:

The governed lifecycle synthesizes the authoritative fail-closed measurement
only when the incoming v2 receipt does not already contain "measurement".

If an incoming receipt already contains a measurement block, the lifecycle can
pass it through to collection.

The measurement validator establishes structural validity, arithmetic validity,
and non-empty operation_trace_ref / expected_route_ref values, but it does not
prove that those refs equal the actual current pre-execution trace and accepted
Operation Guidance for this governed operation.

Therefore an incoming producer-supplied measurement can potentially claim SAFE
using syntactically valid but non-authoritative refs.

This violates the accepted contract that the governed seam passes only
source-bound operation and expected-route evidence.

M10 is therefore NOT CLOSED by the current candidate.

Required correction class:

- the governed lifecycle must not trust an incoming producer-owned measurement
  as authoritative;
- current lifecycle-owned source bindings must control or strictly verify the
  measurement projection;
- a forged/non-matching incoming operation_trace_ref or expected_route_ref must
  not survive as SAFE;
- current real host path must remain UNAVAILABLE;
- do not introduce new authority, producer, store, or operation_trace mutation.

Exact implementation form is left to the bounded corrective pass within the
accepted Plan and existing write surface.

## F-02 — M01_ADJACENT_TURN_CONTRACT_NOT_PROVEN

Severity: MATERIAL / REQUIRED CAPABILITY + FALSE-PASS TEST

Finding:

The current SAFE derivation requires the before-boundary turn id and
after-boundary turn id to be equal to each other and equal to host_turn_id.

The accepted M01 contract requires:

Adjacent-turn, same-session before/after fixture
-> SAFE with exact per-field deltas.

The current M01 fixture uses the same turn id for both boundaries, so it proves a
same-turn case rather than the required adjacent-turn case.

A legitimate same-session pair with distinct before-turn and after-turn
identities is currently classified as SESSION_MISMATCH.

Therefore:

M01 current report disposition:
NOT PROVEN

Required correction class:

- preserve same-session proof;
- preserve explicit before and after turn identities;
- do not require before_turn == after_turn merely to obtain SAFE;
- bind the operation/current host turn according to the accepted contract
  without inventing adjacency metadata that the source does not provide;
- update M01 so before and after use distinct turn identities and the SAFE result
  is asserted;
- retain fail-closed behavior for genuinely ambiguous/missing identities.

## F-03 — M13_REAL_GOVERNED_END_TO_END_PROOF_INCOMPLETE

Severity: MATERIAL / REQUIRED EVIDENCE

Finding:

The accepted M13 requires one real governed operation through the normal:

capture -> append -> exact readback

path.

The current added governed-lifecycle M13 test monkeypatches
collect_governed_receipt, so the normal persistence/readback owner is bypassed.

The capture walking-skeleton test separately proves the capture adapter path, but
the two tests do not establish one governed operation crossing the required
end-to-end seam.

Therefore:

M13 current report disposition:
NOT PROVEN

Required correction class:

- add a bounded test using the actual existing governed collector and actual
  append/readback path;
- prove the persisted measurement bytes/data are read back through the existing
  owner;
- real current host/capture evidence must still result in UNAVAILABLE /
  MISSING_BEFORE_BOUNDARY;
- do not fabricate a SAFE real-host measurement merely to satisfy M13;
- if the required end-to-end proof cannot be achieved inside the already
  authorized six-file surface and existing architecture, STOP and report the
  exact first broken seam instead of widening scope.

## F-04 — AMBIGUOUS_BOUNDARY_ALIASES_NOT_FAIL_CLOSED

Severity: MATERIAL / STRICT VALIDATION

Finding:

The new boundary representation accepts multiple aliases/sources for the same
fact, including:

host_session_id and session_id
host_turn_id and turn_id
nested counters and top-level counter fields

When more than one representation is present with conflicting values, the
current helpers select one value rather than treating the structured evidence as
ambiguous.

The accepted measurement semantics require ambiguous identity/counter evidence
to fail closed.

Required correction class:

- conflicting duplicate representations of the same identity or counter fact
  must never yield SAFE;
- either enforce one canonical representation or explicitly detect conflicts;
- ambiguous structured facts must become the appropriate fail-closed
  UNAVAILABLE disposition or strict validation failure according to the
  accepted frozen semantics;
- do not expand the reason vocabulary or change reason precedence.

## Non-findings / accepted parts

Preserve the following candidate work unless correction requires a narrowly
necessary adjustment:

- schema_version=1 additive measurement carrier;
- frozen reason vocabulary;
- frozen primary-reason precedence;
- SAFE / UNAVAILABLE distinction;
- SAFE + COMPLETE;
- SAFE + PARTIAL;
- UNAVAILABLE + PARTIAL;
- rejection of UNAVAILABLE + COMPLETE;
- missing descriptive metadata -> null + PARTIAL;
- all six UNAVAILABLE deltas null;
- measured numeric zero only under SAFE;
- current real host disposition UNAVAILABLE;
- current real host primary reason MISSING_BEFORE_BOUNDARY;
- cumulative top-level token semantics unchanged;
- append-only persistence;
- identical replay idempotence;
- conflicting replay remains hard failure;
- content blindness;
- no architecture expansion;
- no 09-G.

## Governance disposition

execution_discipline: PASS / six authorized files only
focused_test_receipt: ACCEPTED / 88 focused passed
operation_trace_regression_receipt: ACCEPTED / 8 passed
full_suite_receipt: ACCEPTED / 738 passed with 88 warnings
candidate_disposition: PRESERVE FOR BOUNDED CORRECTIVE PASS
candidate_revert: NOT AUTHORIZED
implementation_authorization: YES / EXISTING BOUNDED CHANGE 3 PLAN
corrective_implementation_authorized: NO
architecture_expansion: NOT AUTHORIZED
09-G: NOT STARTED
commit: NOT AUTHORIZED
push: NOT AUTHORIZED
next_single_gate: OWNER_DECISION_CHANGE_3_CORRECTIVE_IMPLEMENTATION_AUTHORIZATION

