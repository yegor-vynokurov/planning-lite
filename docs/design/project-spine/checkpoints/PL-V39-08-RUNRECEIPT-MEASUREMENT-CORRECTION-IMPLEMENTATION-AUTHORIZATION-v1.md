# PL-V39-08 RunReceipt Measurement Correction — Implementation Authorization v1

## Authorization identity

```text
checkpoint_id: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-AUTHORIZATION-v1
change_id: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
owner_decision: AUTHORIZE / BOUNDED IMPLEMENTATION
implementation_authorized: YES / BOUNDED CHANGE 3 PLAN ONLY
implementation_executed: NO
09-G_started: NO
```

## Accepted authority

```text
definition: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-v1.md
definition_sha256: cef899a6a6b2ced4d1bef1e266969cd2b57981d5b59275b77e8e093e2d9d21cc
implementation_plan: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-v1.md
implementation_plan_sha256: 91db4e0788b20f342418604e827c2f73b0fc8f16f42fa21139b218130e868f54
formal_readiness_verdict: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-FORMAL-READINESS-VERDICT-v1.md
formal_readiness_verdict_sha256: 09aa37a64832948f02f8451fa0a20c9e09a4b03832a58d0c04f11dfd7925a439
controlled_discovery_review: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CONTROLLED-DISCOVERY-REVIEW-v1.md
controlled_discovery_review_sha256: 3b08aa18cef784782c7e039a70414a7d48aacefd2481f4066114ca5a5c74584d
```

## Accepted discovery consequence

```text
controlled_discovery_result: NOT_PROVEN / OWNER_ACCEPTED
current_real_path_safe_delta_proven: NO
current_real_path_measurement_disposition: UNAVAILABLE
terminal_cumulative_counter: CUMULATIVE EVIDENCE ONLY
definition_amendment_required: NO
plan_amendment_required: NO
architecture_expansion_authorized: NO
```

The current real Codex host/capture path has no proven authoritative
pre-operation counter boundary and no proven explicit compatible
counter_scope. It must not produce a SAFE operation-local delta from the
existing terminal cumulative counter. The accepted additive measurement
representation must fail closed to delta_status=UNAVAILABLE with the
applicable stable reason on that real path.

SAFE measurement remains permitted only for structured cases with explicitly
supplied/proven same-session before and after boundaries and compatible
counter scope. Missing descriptive metadata follows the accepted Plan's
PARTIAL/null semantics. Expected route remains source-bound to the existing
pre-execution guidance/operation-trace path.

## Frozen later implementation write surface

```text
product_write_surface:
  - src/planning_lite/telemetry.py
  - src/planning_lite/operation_lifecycle.py
  - scripts/capture_codex_run_receipts.py
test_write_surface:
  - tests/test_run_receipts.py
  - tests/test_operation_lifecycle.py
  - tests/test_codex_run_receipt_capture.py
read_only_dependencies:
  - src/planning_lite/operation_trace.py
  - tests/test_operation_trace.py
```

No new host instrumentation, producer, store, service, identity, telemetry
authority, route selector, or architecture is authorized. The later
implementation must preserve cumulative receipt semantics, append-only
canonical persistence, exact readback, identical replay behavior, hard
conflicting identity failure, content blindness, and existing Attempt/task/
run-family/invocation ownership.

The next permitted gate is RUN_CHANGE_3_IMPLEMENTATION. This checkpoint
authorizes the bounded plan only; implementation execution has not started.
