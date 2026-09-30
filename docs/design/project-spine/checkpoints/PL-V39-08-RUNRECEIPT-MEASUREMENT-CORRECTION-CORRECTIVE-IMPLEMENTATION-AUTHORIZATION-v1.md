# PL-V39-08 Corrective Implementation Authorization

schema_version: 1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
transition: OWNER_DECISION_CHANGE_3_CORRECTIVE_IMPLEMENTATION_AUTHORIZATION
owner_decision_source: EXPLICIT_HUMAN_OWNER
owner_decision: AUTHORIZE / BOUNDED CHANGE 3 CORRECTIVE IMPLEMENTATION FOR F-01...F-04 ONLY

preserved_implementation_candidate_state_id: ff82d2e4ddb3811980b047bcf9ab97742b3b9d7a76070f2160732cf61daccf51
candidate_review_path: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-CANDIDATE-REVIEW-v1.md
candidate_review_sha256: 67a92b8f72377fd8f948a731380bf2dd7f40816a03e3541825840b7a61071aa8
candidate_review: REVIEW_FAIL / 4 MATERIAL FINDINGS / PRESERVED
current_projection_correction_path: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CANDIDATE-REVIEW-CURRENT-CORRECTION-v1.md
current_projection_correction_sha256: 4ea2fe8c30f42d5dc685c053bcba1871596f0b9409c6185ad0041f1a54168d43

entry_head: 19217522f3dac695602a8534d7ddb8f9bbee5858
entry_authority_state_id: 1170cd8f9aabbe4b4a929cd3650acbe829ea3775426dd0630a5dd9676caedbe8
entry_candidate_state_id: ff82d2e4ddb3811980b047bcf9ab97742b3b9d7a76070f2160732cf61daccf51
entry_unrelated_dirt_state_id: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
entry_sync_state_id: 149429e0bdee7836da796566c7f70a2dfd24023776a750f822068573d76e37bc

definition_sha256: cef899a6a6b2ced4d1bef1e266969cd2b57981d5b59275b77e8e093e2d9d21cc
implementation_plan_sha256: 91db4e0788b20f342418604e827c2f73b0fc8f16f42fa21139b218130e868f54
formal_readiness_sha256: 09aa37a64832948f02f8451fa0a20c9e09a4b03832a58d0c04f11dfd7925a439
controlled_discovery_review_sha256: 3b08aa18cef784782c7e039a70414a7d48aacefd2481f4066114ca5a5c74584d
original_implementation_authorization_sha256: 17eaae67764c3282210397360232ef347bee474757cb3cd5419d752726b4f311

corrective_implementation_authorized: YES / F-01...F-04 ONLY
corrective_implementation_execution: NOT STARTED
definition_amendment_required: NO
implementation_plan_amendment_required: NO
architecture_expansion_authorized: NO
09-G: NOT STARTED
next_single_gate: RUN_CHANGE_3_CORRECTIVE_IMPLEMENTATION

## Authorized findings and required outcomes

### F-01 — AUTHORITATIVE_MEASUREMENT_SOURCE_BINDING_BYPASS

- Governed lifecycle must not trust producer-supplied measurement route or
  operation references merely because they are structurally valid.
- Authoritative current lifecycle-owned pre-execution evidence must control or
  strictly verify `operation_trace_ref` and `expected_route_ref`.
- Forged, stale, foreign, or non-matching references must not survive as SAFE.
- Current real host path remains fail-closed `UNAVAILABLE`.
- Add no route authority, operation-trace authority, producer, store, service,
  or architecture.

### F-02 — M01_ADJACENT_TURN_CONTRACT_NOT_PROVEN

- M01 must prove the accepted adjacent-turn, same-session case.
- Before and after identities may be distinct valid turn identities; SAFE must
  not require `before_turn == after_turn` as a shortcut.
- Same-session continuity remains required.
- Operation/current host-turn binding must be source-backed.
- Genuinely missing or ambiguous identities remain fail-closed; do not invent
  adjacency evidence.

### F-03 — M13_REAL_GOVERNED_END_TO_END_PROOF_INCOMPLETE

- Prove one governed operation through the existing
  capture -> governed collection -> canonical append -> exact readback seam.
- Do not monkeypatch away the persistence/readback owner in the M13 proof.
- Current real host measurement remains
  `UNAVAILABLE / MISSING_BEFORE_BOUNDARY`; do not fabricate a SAFE measurement.
- If M13 cannot be proven inside the existing six-file surface and architecture,
  stop at the corrective candidate and report the exact first broken seam.

### F-04 — AMBIGUOUS_BOUNDARY_ALIASES_NOT_FAIL_CLOSED

- Conflicting duplicate representations of the same structured fact must
  never yield SAFE.
- Identity aliases such as `host_session_id`/`session_id` and
  `host_turn_id`/`turn_id` must not silently disagree.
- Nested counter values and top-level duplicate counter values must not silently
  disagree.
- Enforce one canonical representation or detect conflicts explicitly.
- Ambiguous structured facts fail closed under the existing frozen contract.
- Add no reason codes and change no frozen reason precedence.

## Accepted non-findings to preserve

Preserve, unless narrowly necessary to close the four authorized findings:

- measurement `schema_version=1` and additive nested measurement carrier;
- frozen unavailable reason vocabulary and reason precedence;
- SAFE / UNAVAILABLE semantics, including SAFE + COMPLETE, SAFE + PARTIAL,
  UNAVAILABLE + PARTIAL, and rejection of UNAVAILABLE + COMPLETE;
- missing `actual_model` / `actual_effort` / `agent_role` -> null + PARTIAL;
- all six UNAVAILABLE deltas null; measured zero distinct from unavailable;
- deterministic non-negative deltas and cached + uncached reconciliation;
- current real host result UNAVAILABLE with primary reason
  `MISSING_BEFORE_BOUNDARY`;
- cumulative top-level token semantics;
- legacy v1/v2 backward readability;
- append-only persistence, exact readback, identical replay idempotence, and
  conflicting replay hard failure;
- content blindness; Attempt/task/run-family/invocation ownership; and existing
  lifecycle ordering;
- no architecture expansion and 09-G NOT STARTED.

## Corrective implementation write ceiling

Exactly these six files are authorized; a strict subset may be changed:

Product:

1. `src/planning_lite/telemetry.py`
2. `src/planning_lite/operation_lifecycle.py`
3. `scripts/capture_codex_run_receipts.py`

Tests:

4. `tests/test_run_receipts.py`
5. `tests/test_operation_lifecycle.py`
6. `tests/test_codex_run_receipt_capture.py`

Read-only dependencies: `src/planning_lite/operation_trace.py` and
`tests/test_operation_trace.py`. No additional implementation file is
authorized.

Stop rather than widen scope if closure requires changing either read-only
dependency, adding a production or test file, new host instrumentation, producer,
store/database/service, identity or route/model-selection authority,
prompt/response/reasoning/tool-body decoding, changing Definition or Plan
semantics, expanding reason vocabulary, changing reason precedence, or
architecture expansion. If such a need appears after corrective mutation has
begun, preserve the candidate as-is, do not automatically revert, and report the
exact first broken seam for owner review.

This checkpoint records authorization only. Corrective implementation,
product tests, staging, commit, push, release, and 09-G have not been started by
this transition.
