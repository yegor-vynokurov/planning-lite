# PL-V39-08 RunReceipt Measurement Correction Route B Formal Readiness Verdict v1

Transition: RUN_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_FORMAL_READINESS  
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001  
Decision date: 2026-09-29

## Verdict

FORMAL_READINESS_SCOPE: ROUTE_B / T-01..T-05  
VERDICT: READY  
MATERIAL_BLOCKER_COUNT: 0  
FIRST_BROKEN_SEAM: NONE

This fresh evaluation finds the active Definition v6, activated Plan v5, canonical baseline, ownership seams, and accepted evidence sufficiently specific and internally compatible to begin T-01..T-05 after a separate human implementation authorization. It does not authorize implementation or T-06.

## Entry binding and authority

HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858  
ENTRY_INDEX_EMPTY: YES  
ENTRY_AUTHORITY_STATE_ID: f55b4a51ab65199d330ebd43bd97457a3fdb494c814065fe260242be1725d933  
ENTRY_CANDIDATE_STATE_ID: 44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a  
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a  
ENTRY_SYNC_STATE_ID: 78aa6ebfbdf8938bb836152870412fe6f321e305815a110a74bc7e938eec12d3  
ENTRY_CAPSULE: strict reconciled 12-field SYNC_CAPSULE_V1; UTF-8, sorted keys, compact separators, exactly one final LF; `semantic_projection` and `sync_state_id` excluded from hashed bytes.  
ENTRY_DIRTY_PATH_COUNT: 64 (authority 52 / semantic candidate 0 / unrelated 12)

ACTIVE_EFFECTIVE_DEFINITION: PREDECESSOR + AMENDMENT V2 + AMENDMENT V6  
DEFINITION_AMENDMENT_V6_PATH: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v6.md  
DEFINITION_AMENDMENT_V6_SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74  
ACTIVE_EFFECTIVE_PLAN: PREDECESSOR + PLAN AMENDMENT V4 + PLAN AMENDMENT V5  
PLAN_AMENDMENT_V5_PATH: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5.md  
PLAN_AMENDMENT_V5_SHA256: b68ecd94456c9d00fcbca6524ee8063165fa95889e16f834a0416105fd2454db  
PLAN_AMENDMENT_V5_REVIEW: REVIEW_PASS / 0 MATERIAL FINDINGS  
PLAN_AMENDMENT_V5_ACTIVATION_PATH: docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5-ACTIVATION-v1.md  
PLAN_AMENDMENT_V5_ACTIVATION_SHA256: 3a7c4f47222252aaa83ae99b49e519628109730d88eecee0dfe67362d34127e2

## FR-01 ? Authority closure: PASS

Definition v6 and Plan v5 settle the implementation choices needed for this slice: Attempt attribution is not required; membership is prospective and deterministic; timestamps alone never establish membership; estimates and guessed allocations are disallowed; a BOUNDED producer is not required in the first Codex slice; `configuration_ref` is a caller-declared immutable comparison-arm reference, not provider-verified evidence; no efficiency judgment or 09-G behavior belongs here; and collection/open/finalize are explicit rather than automatic. T-01 may finalize persisted field names within the accepted semantics.

## FR-02 ? Baseline isolation: PASS

PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION: COMPLETED / ARCHIVED / RESTORED_TO_CANONICAL_HEAD  
HISTORICAL_CANDIDATE: ARCHIVED / NOT LIVE  
HISTORICAL_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555  
ARCHIVE_MANIFEST_SHA256: 96fcef0094cb0fb41a73f6d40d49f323f55f1c20ba2a79ce73ec4d9be79f1aff  
LIVE_CANDIDATE_PATH_COUNT: 0  
CANDIDATE_CONTAMINATION_REMAINING: NO  
ROUTE_B_BASELINE_ISOLATED: YES  
ROUTE_B_BASELINE_SOURCE: HEAD 19217522f3dac695602a8534d7ddb8f9bbee5858

All six historical paths have empty `git diff HEAD` output and Git-cleaned object identities equal to their HEAD blob identities. Raw Windows CRLF byte IDs are recorded separately in the disposition checkpoint; this is checkout representation only and contains no candidate hunks. The archive is external evidence, not an implementation dependency. M14 is archived only and is not required before T-01.

| Former candidate path | HEAD blob OID | Canonical Git comparison |
|---|---|---|
| `src/planning_lite/telemetry.py` | `73f8518522d3531b0a0502df2022d45b41ec76e9` | PASS |
| `scripts/capture_codex_run_receipts.py` | `8351ebcf05b93753f1ec650249e1be5694eb475a` | PASS |
| `src/planning_lite/operation_lifecycle.py` | `a6a71e6087d5e64b3ef1c866cdd6c922e210b1df` | PASS |
| `tests/test_run_receipts.py` | `12c58efd671efe0ba0898dfd3487f89c4663153c` | PASS |
| `tests/test_codex_run_receipt_capture.py` | `c0cfc3403a215133e68637cccafbfc8feb1840b6` | PASS |
| `tests/test_operation_lifecycle.py` | `405a639d0f6daedfe61657e4cad368e5d563cc92` | PASS |

## FR-03 ? Product write surface: PASS

The four accepted paths are sufficient: `telemetry.py` owns the provider-neutral carrier/store; `capture_codex_run_receipts.py` owns the existing receipt-stream reader; the new `codex_work_window.py` owns the Codex-specific bounded source adapter; and `cli.py` owns explicit commands. `workspace.py` already exposes registered project identity, telemetry policy, and `receipt_path` through `inspect_project`; it need not change. `pyproject.toml` already exposes `planning-lite = planning_lite.cli:main` and packages the whole `src/planning_lite` directory. `operation_lifecycle.py` and `operation_trace.py` are not required because the observation is a WORK_WINDOW with no Attempt bridge. No target-project configuration mutation is needed.

## FR-04 ? Test write surface: PASS

The accepted four test paths cover the existing carrier, legacy capture reader, new adapter, and CLI. `tests/test_codex_work_window.py` is a valid new pytest path under configured `testpaths = ["tests"]` and default `test_*.py` discovery. No operation-lifecycle test mutation is required for this slice.

## FR-05 ? Telemetry carrier feasibility: PASS

Canonical `telemetry.py` already provides exact RunReceipt v1/v2 validators, sorted compact UTF-8 canonical JSON, strict JSONL scan, thread and process locking (including Windows `msvcrt`), lock-protected scan/check/append, flush/fsync attempt, identity replay rejection, and exact persisted-byte readback. Its current scanner is intentionally receipt-only; T-01/T-02 can add an explicit tagged dispatcher, separate registration/observation identity indexes, and versioned typed siblings in the same stream while keeping existing public APIs receipt-only. The Plan specifies rejection of unknown/malformed tags, append concurrency, and unchanged RunReceipt shapes. No new store, migration, or extra owner path is needed.

## FR-06 ? Legacy capture compatibility: PASS

The current `_read_existing` in `capture_codex_run_receipts.py` strictly validates every stream row as a RunReceipt and indexes only `receipt_id`. The accepted T-02 change is local and explicit: validate known typed siblings, exclude them from receipt duplicate/result semantics, and continue appending and returning RunReceipts under the existing command contract. This requires neither a second persistence layer nor a public ownership-contract change.

## FR-07 ? Codex adapter feasibility: PASS

The accepted new adapter path can own explicit `source_ref`, platform file identity, start/end byte offsets, prefix anchor, stable bounded reads, exact segment digest, allowlisted structural parsing, `token_usage_record.usage` aggregation, deduplication, and adapter provenance. Accepted T00 Q5 supports bounded stable reads; Q6 supports the inspected structured usage contract; Q7 supports typed sibling coexistence as structural feasibility. Q1-Q4 remain not proven for exact Attempt attribution/closure and are not required by this coarse Route B scope. No lifecycle/operation-trace mutation is technically required.

## FR-08 ? Windows byte-boundary contract: PASS

Plan v5 specifies `[start_offset_bytes, end_offset_bytes)`, LF-terminated JSONL boundaries, binary bounded reads, identity checks, exact digests, and retry behavior. A binary-mode source handle preserves raw byte offsets and prevents text newline translation. The Plan's LF checks apply to the Codex source bytes; repository CRLF checkout behavior does not define or alter rollout-source boundaries. T00 Q5's observed growth with unchanged mtime/file identity is handled by a captured end bound and exact bounded-byte digest rather than treating mtime as the membership boundary.

## FR-09 ? Source identity contract: PASS

The Plan combines an explicit resolved path, open-handle/platform identity, prospective start offset, prefix-anchor digest, explicit finalize end offset, bounded segment digest checked twice, path/handle identity recheck, and one immediate retry for transient instability. The declared source membership is the exact registered interval; later growth past the captured end is excluded. A Windows implementation can use the platform file identity and binary handle APIs without inventing a cross-platform membership policy or relying on timestamps.

## FR-10 ? Codex usage contract: PASS

Accepted T00 Q6 records 494 inspected structured usage records and supports `input_tokens`, `cached_input_tokens`, `output_tokens`, `reasoning_output_tokens`, and `total_tokens`; the sampled values were nonnegative integers, cached input did not exceed input, total reconciled to input plus output, and reasoning did not exceed output. Plan v5 requires nonnegative integer validation with Boolean rejection, missing optional metrics as absent/null with completeness, response identity deduplication with conflicting duplicates failing closed, and reconciliation only where source semantics agree. The sample's `cache_write_input_tokens` was zero and does not establish future nonzero semantics; Plan v5 explicitly makes nonzero unmodeled values unavailable with `USAGE_RECORD_INVALID`. No accepted evidence contradicts those rules.

## FR-11 ? Configuration reference contract: PASS

Plan v5 accepts one caller-supplied immutable string: a versioned external reference or `sha256:<64 lowercase hex>`, retained after whitespace validation without registry resolution. The Plan activation labels it `DECLARED_IMMUTABLE_COMPARISON_ARM_REFERENCE / NOT AUTOMATICALLY PROVIDER-VERIFIED` and explicitly says caller input is not provider-verified runtime evidence. No Prompt or Experiment Registry is needed, and no accepted field requires a provider-verification claim.

## FR-12 ? Finalization state machine: PASS

The Plan defines prospective OPEN registration and idempotent same-intent replay; unstable or incomplete FINALIZE returns `REQUEST_NOT_YET_FINALIZABLE` without a final observation; terminal integrity/usage failure persists one final `UNAVAILABLE`; stable complete supported totals produce `DIRECT / COMPLETE_SCOPE_TOTAL`; identical final replay returns persisted canonical bytes; and conflicting terminal replay returns `WINDOW_ALREADY_FINALIZED_CONFLICT`. The existing lock/identity model supports serialized scan/check/append and replay.

## FR-13 ? Backward compatibility: PASS

RunReceipt v1/v2 shapes, identities, cumulative fields, delta meanings, historical rows, capture behavior, and receipt-only public return shapes remain unchanged. The Plan prohibits migration/backfill and prohibits writing Work Window totals into legacy delta fields. New tagged records are additive siblings.

## FR-14 ? Acceptance executability: PASS

Each of the 20 Plan v5 cases is executable by deterministic local tests using temporary streams, synthetic rollout bytes, controlled mutations, and coordinated concurrency. The real-world assertion that the chosen Codex source is dedicated to one configuration arm is evidenced separately by T-06, as the Plan explicitly allows; it does not make a T-01..T-05 case field-only.

| Case | Classification |
|---|---|
| A-01 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-02 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-03 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-04 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-05 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-06 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-07 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-08 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-09 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-10 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-11 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-12 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-13 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-14 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-15 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-16 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-17 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-18 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-19 | EXECUTABLE_BY_DETERMINISTIC_TEST |
| A-20 | EXECUTABLE_BY_DETERMINISTIC_TEST |

T-06 remains the separately authorized real-provider field proof. No A-01..A-20 case requires live provider activity to review the T-01..T-05 implementation.

## FR-15 ? Baseline test health: PASS

BASELINE_TEST_COMMAND: `uv run --frozen pytest tests/test_run_receipts.py tests/test_codex_run_receipt_capture.py tests/test_cli.py`  
BASELINE_TEST_COUNTS: 90 passed / 0 failed  
BASELINE_TEST_RESULT: PASS

The command completed in 14.92 seconds. It exercises the existing telemetry/receipt owner, Codex capture owner, and CLI. The accepted new adapter test file does not yet exist and was not required for baseline.

## FR-16 ? M14: PASS

M14_CURRENT_STATUS: ARCHIVED_REUSABLE_HUNK  
M14_REQUIRED_FOR_IMPLEMENTATION_START: NO  
M14_REINTRODUCTION_DECISION: DEFERRED_TO_AUTHORIZED_T05  
M14_LIVE_WORKTREE: NO  
M14_HUNK_SHA256: 9c1957d2df32557259b8c6195c5ffdd455d1b28a05b141dff3cac556ea442348

No M14 bytes were reintroduced during Formal Readiness.

## FR-17 ? Out-of-scope guard: PASS

T-01..T-05 can be implemented without Attempt measurement or bridge, multi-source windows, automatic discovery/open/finalize, daemon/scheduler, other provider adapters, cross-provider normalization, cost/efficiency scoring, registries, 09-G, or Roadmap changes. These remain excluded in active Definition v6 and Plan v5.

## Lifecycle and write boundary

FORMAL_READINESS_BLOCKED_PENDING_CANDIDATE_DISPOSITION: NO  
FORMAL_READINESS_FOR_ROUTE_B: READY  
ROUTE_B_MATERIAL_BLOCKERS: NONE  
IMPLEMENTATION_AUTHORIZED: NO  
T01_T05_EXECUTION_AUTHORIZED: NO  
T06_FIELD_PROOF_AUTHORIZED: NO  
T00_REEXECUTION_AUTHORIZED: NO  
09_G_STARTED: NO  
NEXT_SINGLE_GATE: OWNER_AUTHORIZE_CHANGE_3_ROUTE_B_IMPLEMENTATION_T01_T05

This transition changed only this verdict checkpoint and `docs/design/project-spine/CURRENT.md`. Source, tests, Roadmap, candidate archive, T00 evidence, and unrelated dirt were not changed. No implementation, field proof, T00 rerun, staging, commit, push, or release occurred.
