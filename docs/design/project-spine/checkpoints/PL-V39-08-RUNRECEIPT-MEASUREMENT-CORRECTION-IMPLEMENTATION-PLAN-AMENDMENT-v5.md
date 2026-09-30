# PL-V39-08 RunReceipt Measurement Correction — Implementation Plan Amendment v5

## 1. Plan identity and governance status

Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-005
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Lineage: CHANGE_3 / ROUTE_B_PROVIDER_NEUTRAL_COARSE_EFFICIENCY_MEASUREMENT
Plan status: CANDIDATE_FOR_OWNER_REVIEW
Activation status: NOT_ACTIVE
Implementation authority: NO_IMPLEMENTATION_AUTHORITY
Formal Readiness: NOT_PERFORMED
T00: EXECUTED / ACCEPTED / CONSUMED / STOP_WITH_PROVEN_SEAM; NO RERUN
09-G: NOT_STARTED

This is the first actual Route B Implementation Plan Amendment v5. It is a
different artifact and lineage from the failed Definition Amendment v5. The
Definition Amendment v5 remains unchanged, inactive, and recorded as
REVIEW_FAIL / 1 MATERIAL GOVERNANCE FINDING.

Entry state for this preparation:
HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858
AUTHORITY_STATE_ID: 91f66c5430bd4f47c4ef3cd7bdab66236e69a309ab93247b4aa1d3f133876456
CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a
SYNC_STATE_ID: 73b6124edea9abc40ee22e4d270c52d1461996c411322d6bb23cebff6e55bf57
INDEX_EMPTY: YES

Active Definition:
PREDECESSOR DEFINITION + AMENDMENT V2 + AMENDMENT V6

Definition Amendment v6:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v6.md
SHA256: aea6aeb27bf3158c598e54e9003673be2af6e4d71fc04e9e14411fa4d270ac74
Review:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v6-REVIEW-v1.md
SHA256: 7ea6e8436850e5f761558691f7cb43bb92a8a630d0e5ffd2ec35038fa602b464
Activation:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v6-ACTIVATION-v1.md
SHA256: 94967e652ac0640a9465caa5af15b14f57438b1f4f71063489ecd5eb68b11dd6

Effective Plan before this candidate:
PREDECESSOR PLAN + IMPLEMENTATION PLAN AMENDMENT V4
Active Plan Amendment v4:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v4.md
SHA256: e9f2d09f4f8bac0fef81f8a9c79630cf8c65edd6b9084406fd2c9242a9430981
Plan v4 authority for active Route B implementation: NO. It was designed
around the prior exact Attempt-bound RESPONSE_AGGREGATE route and does not
authorize this provider-neutral coarse-measurement scope.

This candidate defines an executable narrow Route B slice. It does not approve
or activate itself, prepare Formal Readiness, authorize implementation,
resolve the preserved corrective candidate, rerun T00, start 09-G, or change
product/test files.

## 2. Goal, user path, and boundaries

The first candidate will prove one end-to-end resource-observation journey:

explicitly open one WORK_WINDOW
→ bind one immutable configuration reference and one dedicated explicit Codex local rollout source segment prospectively
→ perform work under that one comparison arm
→ explicitly finalize the window
→ read only structured provider-native usage inside the registered byte segment
→ persist one provider-neutral Resource Observation
→ return its canonical persisted readback.

The observation describes the declared window as a whole. It makes no
PLANNING_ATTEMPT, Attempt-to-thread, Attempt-to-turn, or Attempt-to-response
claim. It produces no efficiency winner, routing decision, or 09-G judgment.
No direct OpenAI API call, automatic per-Attempt capture, background process,
scheduler, or host instrumentation is part of this slice.

The first production route is:

ROUTE_B_VERTICAL_SLICE: WORK_WINDOW / ONE_DEDICATED_PROVIDER_SOURCE_SEGMENT
INITIAL_PROVIDER_ADAPTER: CODEX_LOCAL_ROLLOUT
EXACT_ATTEMPT_BRIDGE_REQUIRED: NO
MULTI_SOURCE_WORK_WINDOW: OUT_OF_SCOPE_FOR_FIRST_SLICE
AUTOMATIC_COLLECTION: NO

One source means one explicitly supplied local Codex rollout file and one
prospectively bounded byte segment within that file. The source must be
dedicated to one configuration/comparison arm for the measured period. If
known activity in that segment mixes configurations or unrelated work in a
way the source cannot separate truthfully, the whole-window claim is
UNAVAILABLE. No prompt, body, or semantic text classification is used to
guess membership.

## 3. Read-only inspection and current owner map

Inspection distinguished canonical tracked code at HEAD from the preserved
uncommitted corrective candidate. The current working-tree bytes in the six
candidate paths are not treated as canonical implementation input.

| Owner | Canonical responsibility and observed seam | Plan treatment |
|---|---|---|
| src/planning_lite/telemetry.py | Owns RunReceipt v1/v2 shape validation, canonical JSON, JSONL scan, process/thread locking, append/fsync attempt, identity replay, and exact persisted readback. The current scanner validates every row as a RunReceipt and indexes receipt_id. | Keep this as the provider-neutral carrier, typed-stream, and persistence owner. Add a versioned Resource Observation sibling; do not add Route B totals to RunReceipt measurement or delta fields. |
| scripts/capture_codex_run_receipts.py | The second production reader of the same receipt stream. It validates every existing line as RunReceipt, preflights receipt IDs before append, then checks readback. Its parser reads explicit local rollout paths and allowlisted metadata, but currently ignores token_usage_record. | Adapt its existing-record dispatch to recognize and skip validated typed siblings while preserving its RunReceipt-only result and old capture behavior. The new window parser is not an Attempt mode of this script. |
| src/planning_lite/cli.py | Owns the installed planning-lite argparse tree and receipt command. pyproject.toml already exposes planning-lite = planning_lite.cli:main. | Add the explicit work-window open/finalize user surface here; no new console entry point or pyproject change. |
| src/planning_lite/workspace.py | inspect_project returns registered project identity and the existing telemetry receipt_path under the Planning Lite home; it does not own record parsing. | Read its existing project/policy/path result. Derive the shared stream path from receipt_path. No workspace or target-project configuration mutation is planned. |
| src/planning_lite/operation_lifecycle.py and operation_trace.py | Own exact Attempt execution, route evidence, and receipt relationships; they do not currently supply a general WORK_WINDOW identity or own the local telemetry stream. | Leave unchanged. No Attempt bridge or operation_measurement_v2 requirement is introduced. |
| Codex local source | Accepted T00 bounded evidence found structured token_usage_record.usage rows and stable explicit source reads. The existing parser intentionally treats token_usage_record as opaque and reads a whole rollout, so it does not implement a registered byte segment. | Add a separate narrow package adapter that reads the explicit registered segment and aggregates structured native usage. |
| tests/test_run_receipts.py and tests/test_codex_run_receipt_capture.py | Own existing receipt validation/persistence and capture-reader compatibility acceptance. | Extend those existing owners for typed sibling interleaving and unchanged RunReceipt/capture behavior. |

A repository search found no reusable general configuration-reference type.
Existing source references use explicit path/hash provenance, while stable
prompt-prefix identity is specific to prompt composition and is not a
configuration-arm identity. This Plan uses one required caller-supplied,
immutable configuration reference string, either a versioned external
reference or a SHA256 fingerprint in the form sha256:<64 lowercase hex>.
Store it exactly after whitespace validation; do not resolve it through a new
registry. Record provider, model when known, and installed Planning Lite ref
separately. The owner supplies the reference for the relevant prompt, skill,
checklist, model, or other arm configuration; a mutable label is not accepted.

### Existing local Codex evidence and bounds

The accepted T00 review records that sampled token_usage_record entries carry
thread_id, turn_id, session_id, response_id, and structured usage fields. In
the bounded sample, five selected provider-native fields were nonnegative
integers; cached input did not exceed input; total matched input plus output;
reasoning output did not exceed output; and per-response sums reconciled to
sampled compatible turn totals. cache_write_input_tokens was observed as zero
in that sample, which does not establish semantics for a future nonzero value.

The current capture script deliberately ignores token_usage_record and
currently reads whole files into metadata rows. Its explicit rollout/session/
turn parser is Attempt-oriented. It is useful ownership and fixture evidence,
but its candidate changes are not treated as canonical Route B code. The new
adapter must stream only the registered byte interval, decode only allowlisted
structural metadata and token_usage_record.usage, and fail closed on unknown
source shapes that could hide resource usage.

## 4. Carrier, registration, and persistence choice

### Provider-neutral typed siblings

Use the existing per-project telemetry JSONL path returned as receipt_path.
Add two additive, explicitly tagged/versioned record types to that append-only
stream:

- WorkWindowRegistrationV1, record_type work_window_registration,
  schema_version 1. It is persistent prospective membership/request state.
- ResourceObservationV1, record_type resource_observation, schema_version 1.
  It is the provider-neutral semantic observation.

Existing RunReceipt v1/v2 rows remain untagged and keep their exact schema,
identities, cumulative fields, and historical meanings. Do not add a nested
measurement block to RunReceipt. Do not reuse operation_measurement_v2 or
populate legacy *_delta fields with a whole-window sum. No historical rows
are migrated or rewritten.

The tagged dispatcher first distinguishes an untagged legacy/RunReceipt row
from a known typed sibling. It validates each known record under its own
schema and rejects unknown or malformed record types. It maintains separate
identity namespaces: receipt_id for RunReceipt, window_id for registration,
and observation_id for Resource Observation. Existing RunReceipt APIs continue
to scan and return only RunReceipt rows. Registration and observation APIs
return only their typed records. Neither API may mistake another type's
identity for its own.

Keep registration and final observation in the same append-only stream. This
reuses the existing process-safe lock, canonical serializer, append, fsync
attempt, and exact readback owner without creating a registry, database, or
second store. The existing lock must cover the full scan/check/append decision
for each identity so concurrent replay cannot create duplicate registrations
or final observations. Invalid existing rows stop before the next append.
Existing RunReceipt v1/v2 calls and their public return shapes remain
unchanged.

The core Resource Observation schema should make the active v6 axes
machine-readable, with field names finalized during T-01:

- observation_id and project identity;
- scope kind WORK_WINDOW, stable window/scope ID, start/end boundary;
- source and prospective membership-rule provenance;
- provider, model when available, configuration_ref, method, and native
  quantity semantics;
- per-quantity value, quality, and numeric claim kind;
- source and requested/optional metric completeness, including explicit
  absent/partial status;
- limitations or one stable unavailable reason;
- adapter provenance such as rollout identity, byte offsets, segment digest,
  unique response count, and response-identity digest.

Provider-specific thread_id, turn_id, response_id, and rollout path belong
inside source/provenance fields. They are not mandatory universal identity
fields. A consumer must be able to tell DIRECT / COMPLETE_SCOPE_TOTAL from a
bounded noncomplete claim through structured data, not prose.

The carrier validator must represent v6 BOUNDED claims using
EXACT_OBSERVED_SUBSET, PROVEN_LOWER_BOUND, or
OTHER_PRECISELY_DEFINED_NONCOMPLETE_CLAIM. This first Codex producer emits
DIRECT supported totals or UNAVAILABLE; implementing a BOUNDED producer is not
a first-slice requirement. Completeness remains independent: an absent
optional reasoning metric is null/absent and marked absent or partial, never
zero. Other supported whole-window quantities may remain DIRECT /
COMPLETE_SCOPE_TOTAL when the source coverage for those quantities is complete.

### Prospective registration

The explicit open command requires a registered project with telemetry
enabled, window_id, immutable configuration_ref, and an explicit source_ref
path. It records provider=codex, optional known model, membership rule
DEDICATED_EXPLICIT_SOURCE_SEGMENT_V1, and the registration provenance. It
does not write into the consumer project.

At open, inspect the exact source path read-only through an open handle.
Resolve and persist the exact source reference and stable platform file
identity. Capture start_offset_bytes at the current EOF, only if the file is
empty or the current EOF is a complete LF record boundary. Capture a short
prefix-anchor digest immediately before the offset, the file identity, and
the registration time/provenance. This detects common replacement, compaction,
and truncate/regrow cases without hashing the entire old session. No previous
bytes before start_offset are members.

Append the registration before measured work begins. If the source cannot be
opened stably, is not at a record boundary, or lacks a reliable file identity,
do not append the registration. Require the operator to open the window before
using the dedicated source for measured work.

A repeated open with the same window_id and same immutable project,
configuration, provider, source, and membership intent returns the original
registration idempotently and never moves its start offset, even if the source
has since grown. Reuse of that window_id with a different source, configuration,
provider, or membership rule fails with a hard conflict. Use a new window_id
for a new comparison arm or period. An open registration persists across
process and shell restarts.

### Explicit finalization and stable source segment

Finalize is a user-invoked command. It loads the persisted registration by
window_id and opens the same source. It verifies path and open-handle identity
against registration, checks the prefix anchor, and rejects truncation below
the registered offset. A replacement, source-identity mismatch, or proven
truncation is terminal integrity failure; do not substitute a different file.

Capture end_offset_bytes from the opened handle at the explicit finalize
boundary. The measured member is exactly [start_offset_bytes, end_offset_bytes).
Later source growth is outside the captured interval and cannot change the
result. Require the interval to end on a complete LF-terminated JSONL record.
Read the exact interval with a streaming parser, bounded to that offset. Check
open-handle/path identity and that the handle still covers the bound; hash the
bounded bytes twice and require identical digests. Growth beyond end_offset is
ignored. One immediate bounded retry is permitted for a transient read; do not
wait for a quiet period or use timestamps to assign membership.

If the tail is incomplete or the bounded read is unstable, return
REQUEST_NOT_YET_FINALIZABLE and append no Resource Observation. The persisted
open registration remains available for explicit retry. If a stable terminal
integrity conflict prevents a truthful result, append one final UNAVAILABLE
observation with one stable reason. A finalized window never reopens. A
replayed finalize returns the exact persisted observation; any attempted
different final result for that window fails with
WINDOW_ALREADY_FINALIZED_CONFLICT.

### Codex native aggregation

The first adapter reads only the exact registered segment. It does not scan
for the latest rollout, enumerate sessions, use timestamp overlap, inspect
prompt/response/reasoning bodies, or call a provider API. It recognizes the
current allowlisted JSONL record envelope and extracts provider-native usage
only from token_usage_record.usage. Current compatible fields are:

- input_tokens;
- cached_input_tokens;
- output_tokens;
- reasoning_output_tokens;
- total_tokens.

Validate each supplied value as a nonnegative integer excluding Boolean.
Preserve the source-native values and semantics. Missing optional metrics stay
null/absent with metric-completeness facts. A field present on every unique
response can have its own DIRECT / COMPLETE_SCOPE_TOTAL claim for the entire
registered window. A missing optional field does not erase a different
supported total. If a metric necessary to the explicit request is absent, that
metric is unavailable; do not fill it with zero.

Deduplicate by stable (thread_id, response_id) response identity. An identical
duplicate usage row contributes once. Conflicting usage for the same identity
fails closed. Preserve unique response count and a deterministic digest of
sorted response identities. Require consistent source/thread identity and,
when known, one model/configuration for this one-arm window. Multiple or
conflicting model/configuration identities make the whole-window claim
UNAVAILABLE rather than silently combining configurations.

Sum supported fields using deterministic integer addition. Check cached input
does not exceed input and the accepted compatible total=input+output and
reasoning<=output relations where all fields are present and source semantics
match. Arithmetic conflict yields UNAVAILABLE. Do not derive cross-provider
units or efficiency. event_msg/token_count, thread_token_usage, and cumulative
counters are never the primary window usage. They may be retained or used only
as a same-scope checksum when source semantics and complete bounds prove
compatibility; no checksum is required for the initial vertical slice. A
nonzero unmodeled cache_write_input_tokens value is not silently discarded or
folded into another metric; until its semantics are accepted, report the
observation UNAVAILABLE with USAGE_RECORD_INVALID.

The explicit segment is the complete membership set for this one-source MVP.
Unregistered sources are excluded by construction. If the registered segment
contains known inseparable unrelated work or changes configuration, do not
claim a complete target-configuration window. Do not try to isolate work by
timestamps, turn recency, latest/current file, or content classification.
An empty segment or no structured usage rows is not measured zero; finalize as
UNAVAILABLE / REQUIRED_USAGE_MISSING.

## 5. Command surface and project-state boundary

Add two nested commands to the existing planning-lite CLI:

- planning-lite work-window open TARGET --window-id ID
  --configuration-ref IMMUTABLE_REF --source-ref CODEX_ROLLOUT_PATH
  [--model MODEL] [--home HOME]
- planning-lite work-window finalize TARGET --window-id ID [--home HOME]

The open subcommand is the only way this first slice creates a request and
prospective membership. Finalize is the only way it closes the window. Do not
add automatic discovery, automatic all-session coverage, an automatic
open/close hook, or a general read service. A repeated finalize is also the
canonical readback path for an already-finalized window.

Reuse inspect_project and its current project_id, telemetry-enabled policy,
and receipt_path. If telemetry is disabled or the target is not registered,
fail before reading the source or writing state. Store typed records under the
existing Planning Lite home telemetry route, next to that project's RunReceipt
stream; no target-project file, .planning configuration, registry, or product
repository path is changed. The finalization command returns the record read
back from persisted canonical bytes, not merely its in-memory aggregate.

## 6. Minimal stable failure vocabulary

| Reason | First-slice treatment |
|---|---|
| SOURCE_NOT_FOUND | No registration if absent at open; at finalize, retry only if presence is transient, otherwise final UNAVAILABLE. |
| SOURCE_IDENTITY_MISMATCH | Final UNAVAILABLE; never substitute a different source. |
| SOURCE_REPLACED_OR_TRUNCATED | Final UNAVAILABLE when proven by identity, boundary, or anchor check. |
| SOURCE_READ_UNSTABLE | REQUEST_NOT_YET_FINALIZABLE; append no final observation. |
| MEMBERSHIP_BINDING_MISMATCH | Fail closed; do not append a successful observation. |
| CONFIGURATION_BINDING_MISMATCH | Final UNAVAILABLE when source evidence conflicts with the registered single-arm configuration. |
| USAGE_RECORD_INVALID | Final UNAVAILABLE for malformed, unsupported, or contradictory usage semantics. |
| DUPLICATE_USAGE_CONFLICT | Final UNAVAILABLE; do not pick first/last/newest. |
| REQUIRED_USAGE_MISSING | Final UNAVAILABLE; do not invent zero. |
| AGGREGATE_RECONCILIATION_FAILED | Final UNAVAILABLE; do not write inconsistent totals. |
| WINDOW_ALREADY_FINALIZED_CONFLICT | Reject a second, different terminal result; preserve the first. |

A stable terminal failure produces one final UNAVAILABLE record and one
canonical reason. Transient instability is an invocation result, not a
persisted final measurement. Registration identity conflicts are hard errors
and never silently overwrite prior membership.

## 7. Preserved corrective candidate and pre-implementation gate

The preserved corrective implementation candidate remains unchanged:

CANDIDATE_STATE_ID:
37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555
Disposition: UNRESOLVED
Disposition authorized: NO

It must not be adopted, rejected, edited, reverted, or deleted during Plan
preparation. The candidate bytes in the current worktree are not canonical HEAD.

| Candidate path | Exact proposed-path overlap | Read-only classification |
|---|---|---|
| src/planning_lite/telemetry.py | YES — proposed product path | Base-code lock, canonical JSON, append, replay, and exact readback concepts are potentially reusable. Candidate nested Attempt-bound measurement/delta schema is incompatible as-is with the Resource Observation sibling. |
| scripts/capture_codex_run_receipts.py | YES — proposed product path | Explicit source path, content-blind parsing, preflight-before-write, and readback patterns are potentially reusable. Candidate automatic unavailable Attempt measurement is incompatible as-is; preserve the old command contract. |
| src/planning_lite/operation_lifecycle.py | NO | Candidate adds Attempt/route binding and lifecycle injection. Exact Attempt bridge is out of scope; neither code nor path is planned. |
| tests/test_codex_run_receipt_capture.py | YES — proposed test path | Existing source fixtures and receipt capture expectations remain useful. Candidate assertions for nested Attempt measurement are incompatible as acceptance for Route B. |
| tests/test_operation_lifecycle.py | NO | Candidate Attempt-lifecycle measurement tests are irrelevant/incompatible and no path change is planned. |
| tests/test_run_receipts.py | YES — proposed test path | Existing v1/v2 persistence owner tests should be extended for typed siblings. Candidate boundary-delta and Attempt-measurement cases are not Route B requirements. |

PRESERVED_CANDIDATE_OVERLAP_COUNT: 4
PRESERVED_CANDIDATE_OVERLAP_PATHS:
- src/planning_lite/telemetry.py
- scripts/capture_codex_run_receipts.py
- tests/test_codex_run_receipt_capture.py
- tests/test_run_receipts.py

PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION_GATE is mandatory before Formal
Readiness or implementation while these overlapping candidate paths exist.
After Plan review and explicit Plan activation, require a separate owner
decision to adjudicate the preserved candidate. Preserve its candidate-state
identity as evidence; do not treat its current worktree bytes as canonical
baseline. The gate must either establish an owner-approved disposition and
isolate the selected baseline, or stop. Route B work then starts from a clean,
verified baseline containing active Definition v6 and accepted Plan Amendment
v5. This Plan does not grant candidate disposition authority.

## 8. Exact proposed implementation and test surfaces

PROPOSED PRODUCT WRITE SURFACE: 4 paths
PROPOSED TEST WRITE SURFACE: 4 paths

### Product write surface: 4 paths

1. src/planning_lite/telemetry.py
   Add the provider-neutral versioned sibling schemas/validators, typed
   dispatcher, registration and observation append/replay/readback APIs, and
   preserve RunReceipt-only public behavior under the existing lock.
2. scripts/capture_codex_run_receipts.py
   Update its receipt-stream scan to use typed dispatch and retain only
   validated RunReceipt rows for its duplicate checks. It continues writing
   RunReceipts only and preserves its existing exact-binding command behavior.
3. src/planning_lite/codex_work_window.py
   New Codex evidence adapter for explicit source identity, start/end byte
   boundaries, stable bounded reads, allowlisted usage parsing, and exact
   provider-native aggregation. No provider-neutral policy or CLI orchestration
   belongs here.
4. src/planning_lite/cli.py
   Add the explicit work-window open/finalize command tree and wire it to the
   existing project telemetry route, provider-neutral store, and Codex adapter.

### Test write surface: 4 paths

1. tests/test_run_receipts.py
   Add mixed typed-stream cases while retaining existing v1/v2 tests: receipt
   append/readback across sibling rows, type-specific identity, malformed/
   unknown tag stop, and old receipt return shapes.
2. tests/test_codex_run_receipt_capture.py
   Verify existing capture can read a stream containing valid registration and
   observation siblings, still preflights and writes only its RunReceipt rows,
   and retains its existing binding and replay behavior.
3. tests/test_codex_work_window.py
   New focused fixtures for byte boundaries, stable read, allowlisted
   token_usage_record.usage aggregation, deduplication, optional metrics, and
   failure classification.
4. tests/test_cli.py
   Verify explicit open/finalize routing, telemetry-disabled and unregistered
   stops before source/state mutation, canonical readback, and no Attempt/
   efficiency result.

No product, test, workspace, project configuration, template, operation
lifecycle, Roadmap, release, or 09-G path outside these listed surfaces is in
the proposed implementation. The Plan candidate and CURRENT bookkeeping are
the only repository files this planning transition itself may write.

## 9. Task sequence

T-01 — Provider-neutral carrier and semantic validator.
Define versioned ResourceObservationV1 and WorkWindowRegistrationV1 records in
telemetry.py. Validate scope, identity, source/config provenance, provider-
native quantities, per-quantity quality/claim kind, completeness, unavailable
reason, and bounded claim representation. Keep v1/v2 receipt shapes exact.
Define deterministic work-window registration identity and replay contract.

T-02 — Typed append-only persistence and readback.
Add type dispatch, separate identity indexes, lock-protected registration and
final-observation append, exact canonical readback, and receipt-only API
filtering. Update the second production reader in
capture_codex_run_receipts.py. Run compatibility tests before adding any
Codex-specific production behavior.

T-03 — Codex dedicated-segment adapter.
Implement explicit path and open-handle identity checks, registration boundary
capture, prefix anchor, stable end boundary, bounded streaming parse, structured
usage aggregation, native arithmetic checks, dedup/conflict behavior, and
REQUEST_NOT_YET_FINALIZABLE versus final UNAVAILABLE behavior. Do not add
Attempt binding or use cumulative counters as the primary source.

T-04 — Explicit caller surface.
Add planning-lite work-window open/finalize commands. Resolve existing project
registration and telemetry policy; require explicit window/config/source
identity; persist registration before work; finalize only on explicit request;
return canonical persisted readback. Do not alter workspace registration,
target project state, or auto-collection behavior.

T-05 — Focused deterministic acceptance.
Implement the acceptance matrix in Section 10 at the existing test owners and
the two new test paths. Keep tests local and synthetic for contract failures.
Do not query a live Codex source in the automated suite. This task does not run
a whole-provider experiment or make an efficiency judgment.

T-06 — One bounded end-to-end field proof.
Only after separate candidate disposition, accepted Plan, fresh Route B
Formal Readiness, explicit implementation authorization, implementation
review, and explicit field-proof authorization, use one dedicated Codex
local rollout source segment for one configuration arm. Explicitly open,
perform real provider activity under that arm, explicitly finalize, verify a
DIRECT complete total for supported quantities or a stable final UNAVAILABLE,
and read the canonical persisted record back. Demonstrate unrelated source
files were not included. Do not divide totals among Attempts.

## 10. Focused acceptance matrix: 20 cases

A-01 Existing RunReceipt v1/v2 validation, append, replay, and readback keep
their current meanings and public receipt-only return shape.
A-02 Typed dispatch accepts each known versioned sibling, keeps separate
identity indexes, and rejects malformed or unknown record types before append.
A-03 Explicit registration persists in the Planning Lite home stream and is
available after process restart.
A-04 Same window ID and same immutable registration intent is idempotent and
does not move the original start boundary; conflicting intent fails closed.
A-05 Timestamp overlap alone never creates source membership; only the exact
prospectively registered source segment is included.
A-06 Replaced, truncated, identity-mismatched, or prefix-anchor-mismatched
source fails closed without substituting another path.
A-07 Partial final line or unstable exact-segment read returns
REQUEST_NOT_YET_FINALIZABLE with no final observation; later growth beyond a
captured end offset cannot change the finalized bytes or result.
A-08 Structured token_usage_record.usage rows aggregate deterministically for
the explicitly bounded interval; bodies and token_count are not the source.
A-09 Exact duplicate response identity and equal usage contributes once;
conflicting usage under the same response identity is unavailable.
A-10 Missing optional metrics are null/absent with explicit partial/absent
completeness, never fabricated zero.
A-11 Complete dedicated source segment yields per-supported-quantity
DIRECT / COMPLETE_SCOPE_TOTAL claims with provider-native semantics.
A-12 That coarse result needs no Attempt, thread-to-Attempt, or
turn-to-Attempt bridge; provider identifiers remain provenance.
A-13 Identical finalization replay returns the exact same persisted
observation; it does not append a second final record.
A-14 A conflicting terminal replay for an already finalized window fails with
WINDOW_ALREADY_FINALIZED_CONFLICT and preserves the first result.
A-15 Canonical readback after append reproduces the persisted semantic record
and canonical bytes.
A-16 Unregistered source paths and bytes outside the registered interval are
excluded, including later growth beyond the captured end.
A-17 No API, efficiency winner, cross-provider normalization, or 09-G
judgment is emitted.
A-18 Terminal usage absence, malformed usage, duplicate conflict, or
reconciliation failure produces one stable UNAVAILABLE reason, never zero.
A-19 Concurrent open/finalize or receipt writes are serialized so identity
replay cannot append duplicate or interleaved rows.
A-20 Telemetry-disabled or unregistered-project commands stop before source
inspection that is unnecessary and before any state write.

## 11. Field-proof contract

The proof uses exactly one explicitly opened WORK_WINDOW, one required
immutable configuration_ref, provider=codex, one explicit rollout path,
one prospective DEDICATED_EXPLICIT_SOURCE_SEGMENT_V1 membership, and one
bounded [start,end) byte interval. It starts before the measured provider work
and ends only after a human explicitly invokes finalize. It uses real provider
activity but no direct API call by the implementation.

The operator reserves that local source for the single configuration arm
during the window. No other source file, unregistered session, adjacent
timestamp, guessed turn, or prompt/body classification contributes. The
evidence includes the registration readback, source/file identity, offsets,
prefix anchor, exact segment digest, unique response count and identity digest,
per-metric completeness, provider/model when available, canonical persisted
Resource Observation, and final readback.

Expected supported-quantity result:
SCOPE: WORK_WINDOW
QUALITY: DIRECT
NUMERIC CLAIM KIND: COMPLETE_SCOPE_TOTAL

If optional metrics are absent, retain null/absent plus completeness and allow
other fully supported quantities to remain direct complete totals. If the
registered segment cannot be read stably, report REQUEST_NOT_YET_FINALIZABLE
and append no observation. For a proven terminal source/usage failure, append
one final UNAVAILABLE with one reason. Field proof validates evidence
collection and persistence only. It does not choose a winning configuration,
claim efficiency, or close 09-G.

## 12. Stop conditions and explicit exclusions

Stop without a numeric claim if source identity, segment boundary, membership,
configuration, provider/model provenance, usage row, duplicate handling, or
arithmetic semantics are ambiguous. Do not infer membership from timestamps,
recency, current/latest source, task text, response content, or proximity.
Do not extrapolate, scale, divide, statistically fill, or invent missing usage.
Do not turn a live partial segment into final UNAVAILABLE merely because it is
not yet stable.

First-slice exclusions:
- PLANNING_ATTEMPT measurement and any Attempt-to-Codex thread/turn/response
  bridge;
- multiple source segments, sessions, or providers in one WORK_WINDOW;
- automatic source discovery, session scanning, source selection, or
  all-Attempt/all-session coverage;
- automatic open/close, event hooks, daemon, scheduler, or orchestration;
- Claude, Gemini, Qwen, or other provider adapters;
- token normalization across providers/models, cost conversion, provider
  comparison, accepted-output normalization, rework or owner-attention analysis;
- universal Efficiency Score or any efficiency judgment;
- full Experiment Registry, Prompt Garden, or prompt/skill/checklist registry;
- historical RunReceipt backfill, migration, mutation, or delta reinterpretation;
- broad telemetry or operation-lifecycle refactor;
- T00 rerun, new 09-G work, Roadmap change, release, stage, commit, or push.

## 13. Post-Plan governance gates

1. Independent owner review of this exact Plan Amendment v5 candidate.
2. Separate explicit owner acceptance and activation of Plan Amendment v5.
3. PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION_GATE for the four exact overlap
   paths. This is required before Formal Readiness or implementation; it is a
   separate owner decision, not implicit in Plan acceptance.
4. Fresh Route B Formal Readiness against active Definition predecessor + v2
   + v6 and accepted Plan predecessor + v4 + v5, using an isolated verified
   baseline. Historical readiness and T00 results are not reused as current
   Route B readiness.
5. Separate explicit implementation authorization bounded by the accepted
   Plan and its four product paths.
6. Execute T-01 through T-05 and receive an independent implementation review.
7. Obtain separate explicit field-proof authorization before T-06 and any
   real-provider/local telemetry write.
8. Review the field proof and completion evidence; owner closure remains a
   separate gate.

Plan Amendment v5 remains CANDIDATE_FOR_OWNER_REVIEW / NOT_ACTIVE. The next
single gate is OWNER_REVIEW_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_IMPLEMENTATION_PLAN_AMENDMENT_V5.

