# PL-V39-08 RunReceipt Measurement Correction ? T00 Controlled Discovery Review v1

```text
Transition: OWNER_REVIEW_CHANGE_3_RESPONSE_AGGREGATE_T00_CONTROLLED_DISCOVERY
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Review date: 2026-09-29
Reviewer: Codex / independent evidence review

REVIEW_VERDICT: REVIEW_PASS / 0 MATERIAL EVIDENCE FINDINGS
T00_RESULT_ACCEPTED: STOP_WITH_PROVEN_SEAM
T00_AUTHORIZATION: CONSUMED
T00_REEXECUTION_AUTHORIZED: NO

FORMAL_READINESS_CLOSURE: BLOCKED_AFTER_CONTROLLED_DISCOVERY
MATERIAL_NOT_PROVEN_SEAM_COUNT: 4
IMPLEMENTATION_AUTHORIZED: NO
CANDIDATE_DISPOSITION_AUTHORIZED: NO
09_G_STARTED: NO

NEXT_SINGLE_GATE:
OWNER_DECISION_CHANGE_3_RESPONSE_AGGREGATE_POST_T00_SEAM_DISPOSITION
```

## Evidence reviewed

The strict entry preflight reproduced the authorized 12-field SYNC_CAPSULE_V1
digest. Entry HEAD was
`19217522f3dac695602a8534d7ddb8f9bbee5858`; AUTHORITY was
`cff9e899f85cc9bf46a29f026131911d7be2a24511ec27d04dd7e8f0d5f70674`;
CANDIDATE was
`37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555`;
UNRELATED was
`2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a`;
SYNC was
`1b52304e6e8ff86066c552c414c25307580424f1459576ea74a51a8b8240a43d`.
The index was empty. The authorization checkpoint SHA256 matched its authorized
value.

The three external T00 artifacts exist and match their expected SHA256 values:

| Artifact | SHA256 |
|---|---|
| `CHANGE_3_RESPONSE_AGGREGATE_T00_CONTROLLED_DISCOVERY_V1.md` | `d242a66a85a63b16a24ce104c7897a64a626ffd6636b3c91f8d9019c4d35156d` |
| `CHANGE_3_RESPONSE_AGGREGATE_T00_CONTROLLED_DISCOVERY_V1.json` | `7397858e862ac0c7547638d78d61ed2f524221ccab0e03bc7ae8616953ba42d5` |
| `CHANGE_3_RESPONSE_AGGREGATE_T00_METADATA_SAMPLE_V1.json` | `e86ab92157ec3bc9403f2127e370177069c8bb659ede39b7177d9c7ff0b8e1ea` |

The structured report and sample JSON parse successfully. The review accepts the
bounded conclusions and limitations recorded there. No prompt, response,
reasoning, tool-result, or other rollout content bodies were reviewed.

## Accepted Q1?Q8 dispositions

### Q1 ? NOT_PROVEN

`AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING_NOT_PROVEN`

The lifecycle owns exact Attempt identity and selected route before governed
execution. No authoritative host thread/active structured turn tuple is proven
to reach that pre-execution seam. The local process thread matched the
2026-09-28 rollout sample; the earlier mismatch came from inspecting a different
2026-09-29 session. That correction does not create a lifecycle handoff.

### Q2 ? C / NOT_PROVEN

`ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN`

Structured response usage provides thread/turn/response identity and usage but
no Planning Lite Attempt identity, route reference, or authoritative
Attempt-response membership signal. Neither whole-turn equivalence nor an
exact source-bound subset is proven.

### Q3 ? NOT_PROVEN

`POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`

The existing explicit capture command is a feasible owner for the E1 request
shape and can be extended without a new service or hook. Exact Attempt/source
validation cannot currently be proven because the authoritative host binding
required by Q1 is absent.

`Q3_DEPENDS_MATERIALLY_ON_Q1: YES`

This is not evidence that a daemon or scheduler is required.

### Q4 ? NOT_PROVEN

`POST_TURN_COMPLETION_SIGNAL_NOT_PROVEN`

`task_complete` exists. Nine bounded completed-turn observations showed all
same-turn response usage before it, zero after it, and exact final aggregate
reconciliation. This is empirical ordering evidence, not an authoritative host
contract proving response-scope closure.

### Q5 ? PROVEN / BOUNDED STABLE SOURCE READ FEASIBLE

The inspected explicit rollout sources support the bounded stable-read model.
The stability signature must include file size in addition to identity and
`mtime_ns`; one source grew between observations while its sampled mtime and
file identity remained unchanged.

### Q6 ? PROVEN FOR INSPECTED STRUCTURED RECORD CONTRACT

Primary source: `token_usage_record.usage`.

Accepted numeric mapping: `input_tokens`, `cached_input_tokens`,
`output_tokens`, `reasoning_output_tokens`, and `total_tokens`. In 494
records, `cache_write_input_tokens` was present and zero; it is outside the
accepted operation-usage mapping and had no observed reconciliation effect.
No universal future-zero claim is made.

### Q7 ? PROVEN AS STRUCTURAL FEASIBILITY / NOT IMPLEMENTED

Typed `operation_measurement_v2` coexistence is feasible inside the current
telemetry and capture owners, preserving receipt-only APIs and separate
measurement identity. No new store is required. This is feasibility evidence;
coexistence is not implemented.

### Q8 ? PROVEN

The eight-path surface is sufficient for the defined scope. No mandatory
additional path was found. The six candidate overlaps remain unchanged.
Candidate disposition is still a separate owner prerequisite before
implementation.

## Root-seam interpretation

The three root runtime seams are:

1. `AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING_NOT_PROVEN`
2. `ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN`
3. `POST_TURN_COMPLETION_SIGNAL_NOT_PROVEN`

The fourth official material seam,
`POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN`, depends materially on
the missing exact Attempt/source binding from Q1. This dependency classification
is explanatory only; the official material seam count remains four. No seam
is closed by inference.

## Readiness and next decision

Plan Amendment v4 remains `APPROVED_BY_OWNER / ACTIVE`. The prior Formal
Readiness verdict `READY_WITH_CONTROLLED_DISCOVERY` remains immutable
historical evidence. T00 was executed once and returned
`STOP_WITH_PROVEN_SEAM`; current Formal Readiness closure is
`BLOCKED_AFTER_CONTROLLED_DISCOVERY`, not READY.

The next question requires an owner decision; it is not discoverable under the
consumed T00 authority. This review selects no future route and makes no
Definition, Plan, capability, or semantic amendment. Implementation remains
unauthorized. The preserved candidate is neither adopted nor rejected; its
disposition remains required before any implementation. 09-G has not started.

## Write and validation boundary

The only authorized repository paths for this transition are:

1. `docs/design/project-spine/CURRENT.md`
2. This review checkpoint.

No source, test, Roadmap, Definition, Plan, E1, Formal Readiness verdict,
authorization checkpoint, candidate, or unrelated-dirt path is authorized to
change. No product tests, staging, commit, push, release, implementation, or
candidate adjudication is part of this transition.
