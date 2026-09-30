# PL-V39-08 RunReceipt Measurement Correction — Controlled Discovery Authorization v1

## 1. Transition identity and owner decision

```text
Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CONTROLLED-DISCOVERY-AUTHORIZATION-001
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Owner Formal Readiness review: PASS / ACCEPTED
Formal Readiness: READY_WITH_CONTROLLED_DISCOVERY
Controlled Discovery ID: CHANGE_3_BOUNDARY_SOURCE_DISCOVERY_V1
Implementation authorization: NO
Discovery execution authorization: YES / ONE BOUNDED READ-ONLY DISCOVERY
Discovery execution performed: NO
Repository product mutation authorization: NO
09-G: NOT STARTED
09-F: NOT REQUIRED
```

This checkpoint performs one governance transition: it accepts the prepared
Formal Readiness verdict and authorizes exactly one later bounded read-only
Controlled Discovery. It does not execute that discovery and does not authorize
Change 3 implementation.

## 2. Accepted authority identities

```text
Definition:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-v1.md
Definition SHA256:
cef899a6a6b2ced4d1bef1e266969cd2b57981d5b59275b77e8e093e2d9d21cc

Implementation Plan:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-v1.md
Implementation Plan SHA256:
91db4e0788b20f342418604e827c2f73b0fc8f16f42fa21139b218130e868f54

Formal Readiness verdict:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-FORMAL-READINESS-VERDICT-v1.md
Formal Readiness verdict SHA256:
09aa37a64832948f02f8451fa0a20c9e09a4b03832a58d0c04f11dfd7925a439
```

The accepted Formal Readiness first broken seam remains:

```text
No existing structured evidence currently proves an authoritative same-session
before boundary and compatible counter scope. The current host adapter exposes
only a terminal cumulative counter.
```

## 3. Authorized discovery contract

### Question

Which existing structured host/capture event and field can provide the
operation's authoritative before boundary and after boundary with:

- the same host session;
- compatible explicitly identifiable counter scope;

and how does that evidence enter one of the already-accepted producer paths?

The discovery may also record:

- whether existing pre-execution route evidence travels with those facts;
- actual model availability;
- actual effort availability;
- agent role availability.

### Scope

The discovery is limited to read-only inspection of:

```text
src/planning_lite/telemetry.py
src/planning_lite/operation_lifecycle.py
src/planning_lite/operation_trace.py
scripts/capture_codex_run_receipts.py
tests/test_run_receipts.py
tests/test_operation_lifecycle.py
tests/test_codex_run_receipt_capture.py
tests/test_operation_trace.py
```

It may inspect existing structured rollout records already accepted by the
current capture seam. It may produce only an external evidence artifact:

```text
D:\documents\planning-lite-sync\CHANGE_3_BOUNDARY_SOURCE_DISCOVERY_V1.yaml
```

### Result space

The only permitted discovery results are:

```text
PROVEN
NOT_PROVEN
```

`PROVEN` requires concrete existing evidence for all of the following:

- authoritative before boundary;
- authoritative after boundary;
- same host session;
- compatible identifiable counter scope;
- an already-accepted producer path.

A terminal cumulative snapshot alone is insufficient. `NOT_PROVEN` must name
the missing event or field and does not authorize architecture invention.

### Discovery output contract

The external evidence artifact must contain:

```yaml
schema_version: 1
discovery_id: CHANGE_3_BOUNDARY_SOURCE_DISCOVERY_V1
result: PROVEN | NOT_PROVEN
producer_path:
before_boundary:
  record_type:
  field_path:
  session_id:
  turn_id:
  counter_scope:
after_boundary:
  record_type:
  field_path:
  session_id:
  turn_id:
  counter_scope:
same_session: YES | NO | NOT_PROVEN
compatible_counter_scope: YES | NO | NOT_PROVEN
expected_route_source:
actual_model:
actual_effort:
agent_role:
telemetry_completeness:
reason:
```

### Stop and verification conditions

Stop as soon as one existing structured path proves both boundaries, same
session, and compatible counter scope, or as soon as bounded inspection shows
that no such existing fact is present. If no fact is present, record
`NOT_PROVEN`; do not select a new source or architecture.

Before any dependent implementation work, verify the external evidence against
the accepted Definition Sections 6 and 9 and the accepted Plan Sections 6 and
9. A `PROVEN` discovery result alone does not authorize implementation. If the
result would expand a source surface or architecture, stop and obtain another
owner decision.

## 4. Explicit prohibitions

During the later discovery, do not:

- modify repository files;
- add host instrumentation;
- invent a before or after event;
- treat terminal cumulative counters as operation-local deltas;
- infer same-session scope from parent/child linkage;
- invent or default counter scope;
- substitute zero or approximate missing counters;
- reconstruct route identity from post-execution free text;
- modify `operation_trace.py`;
- add a producer, store, service, or identity;
- change Definition, Plan, Formal Readiness semantics, reason vocabulary,
  precedence, or governance architecture;
- start 09-G, 09-F, or implementation;
- stage, commit, push, clean, reset, stash, or repair unrelated dirt.

## 5. Resume and lifecycle transition

The strict `PLANNING_LITE_RESUME_CONTRACT_V1` remains schema-compatible and
uses only its existing keys. The transition is:

```text
lifecycle_gate:
FORMAL_READINESS_ACCEPTED / CONTROLLED_DISCOVERY_AUTHORIZED

blockers:
CONTROLLED_DISCOVERY_REQUIRED

next_permitted_action:
RUN_CHANGE_3_BOUNDARY_SOURCE_CONTROLLED_DISCOVERY

implementation_authorized:
NO
```

The corresponding CURRENT transition receipt is this checkpoint. The discovery
is authorized but not executed.

