# PL09 Authoritative Attempt Runtime Access â€” Second Corrected Implementation Plan Candidate

Status: `CANONICAL / IMPLEMENTATION PLAN`

## PLAN IDENTITY

```text
PLAN_ID: PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_IMPLEMENTATION_PLAN
CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001
OWNER_GATE: OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_CANONICAL_IMPLEMENTATION_PLAN
OWNER_DECISION: AUTHORIZE_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_CANONICAL_IMPLEMENTATION_PLAN
EXECUTOR: GPT-5.6_LUNA_EXTRA_HIGH
MODE: CANONICAL IMPLEMENTATION PLAN CREATION
ENTRY_HEAD: 96b03dfce442d0ddfbc9329f7d8d4ead9e2cf600
STATUS: CANONICAL / IMPLEMENTATION PLAN
DEFINITION_AMENDMENT: NO
CANONICAL_PLAN_CREATED: YES
FORMAL_READINESS: NOT_YET_RUN
IMPLEMENTATION_AUTHORIZED_BY_THIS_ARTIFACT: NO
```

This canonical Implementation Plan is the reviewed V2 semantic source with
canonical status, authority lineage, and path references. It preserves the two
reviewed corrections: the safe-replacement protocol and operational verification
rows. Canonicalization does not amend the Definition, reopen the Authorization
prerequisite, implement source or tests, or perform executor, lifecycle,
Change-2, staging, commit, or push work.

## AUTHORITY AND LINEAGE

```text
CANONICAL_DEFINITION_PATH: docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CHANGE-DEFINITION-v1.md
CANONICAL_DEFINITION_SHA256: 81514C1519BBDF97D2908B1F0EF2A73CAE19A76535D22923ED726C82A5C63DB1
DEFINITION_ACTIVATION_PATH: docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-DEFINITION-ACTIVATION-v1.md
DEFINITION_ACTIVATION_SHA256: 0DE397A60FCE5E1ABB3257BD0F7DC3C66F5DEF851274033D2A1C14B8A5A7BB3D
AUTHORIZATION_CLOSURE_PATH: docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-CLOSURE-v1.md
AUTHORIZATION_CLOSURE_SHA256: B16025A7170BC7F14430989C3A203449B95A3432ABAEB7231831B59BD76E1E44
AUTHORIZATION_PREREQUISITE: CLOSED
CANONICAL_PLAN_PATH: docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-IMPLEMENTATION-PLAN-v1.md
REVIEWED_V2_PLAN_SHA256: 4AB17312F6FD01AE644319636FF5BBCB0D69605E3F9F588E05A9A369FC977513
V2_FRESH_REVIEW_FULL_FILE_SHA256: 2C00DFC955E8C6333DB81D0A0E6FA7639B67BA2539815E2496EB132BDFAFABB9
V2_FRESH_REVIEW_SELF_EXCLUDING_DIGEST: 92B6505217AEBEC0E6C1BB2CE6EC5B39BC8E116413DA99A20E4344B0FD4FD3F3
V2_FRESH_REVIEW_DIGEST_CONVENTION: DUAL / FULL_FILE_EXTERNAL + SELF_EXCLUDING_INTERNAL
SEMANTIC_DRIFT_FROM_REVIEWED_V2: NO
CANONICALIZATION_RESULT: PASS_DIGEST_RECONCILED_CANONICAL_IMPLEMENTATION_PLAN_CREATED
CANONICAL_PLAN_APPROVED: YES
FORMAL_READINESS: NOT_YET_RUN
IMPLEMENTATION_AUTHORIZED: NO
FIRST_CORRECTED_PLAN_PATH: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_IMPLEMENTATION_PLAN_CANDIDATE_CORRECTED_AUTHORIZATION_BINDING.md
FIRST_CORRECTED_PLAN_SEMANTIC_SHA256: 7D889547FD86ED71714BCD5BC31EEA9094FAE248E9F094D9BA673A4A253B9971
FIRST_CORRECTED_REVIEW_PATH: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_CORRECTED_IMPLEMENTATION_PLAN_FRESH_REVIEW.md
FIRST_CORRECTED_REVIEW_SEMANTIC_SHA256: 99CE6791D14E14F1B725C506BB0BB436597F358A1A7CD9F5DC1312B6DA8E36DA
AUTHORITY_RESULT: VERIFIED
```

The first corrected candidate and first fresh review hashes are verified under
their declared self-excluding UTF-8/LF conventions. The closed
`src/planning_lite/authorization.py` module remains a read-only dependency.

## REVIEW FINDINGS

```text
MF3-01: SAFE_REPLACEMENT_PROTOCOL_UNDERBOUND
MF3-02: VERIFICATION_ROWS_NOT_OPERATIONAL_ENOUGH
```

Both findings are corrected in this artifact. The first finding is resolved by
the mandatory store mutation protocol and failure contract below. The second
is resolved by a concrete 24-row table in which every row has a subject,
exact probe, fixture/input, expected result, durable evidence location, and
failure meaning.

## PRESERVED PASSED SEMANTICS

The following previously passed semantics are retained without reopening:

```text
PREPARATION_AUTHORIZATION_BINDING: PRESERVED
RECOVERY_AUTHORIZATION_BINDING: PRESERVED
PREPARATION_SINGLE_USE: PRESERVED
RECOVERY_SINGLE_USE: PRESERVED
NO_CROSS_STORE_TRANSACTION: PRESERVED
AUTHORIZATION_DEPENDENCY_DIRECTION: AUTHORIZATION -> CONSUMED_BY_ATTEMPT_RUNTIME
RUNTIME_SELF_AUTHORIZATION: FORBIDDEN
CHAT_AGENT_OPERATOR_MODEL: PRESERVED
OWNER_AUTHORITY: PRESERVED
CLI_THINNESS: PRESERVED
MANUAL_CLI_TYPING_REQUIRED_FROM_OWNER: NO
ATTEMPT_RUNTIME_OWNER: PRESERVED
SOLE_ATTEMPT_IDENTITY: AttemptRecordV1.attempt_id
RUNTIME_STATE_MODEL: ACTIVATABLE / IN_FLIGHT / TERMINAL
LOOKUP_SEMANTICS: PRESERVED
ADMISSIBILITY: PRESERVED
ATOMIC_CLAIM: PRESERVED
ABRUPT_LOSS: PRESERVED
TERMINALIZATION: PRESERVED
EXECUTOR_INDEPENDENT_CLOSURE: PRESERVED
PL08_BOUNDARY: PRESERVED
LIFECYCLE_BOUNDARY: PRESERVED
FIVE_PATH_BUDGET: PRESERVED
TASK_COUNT: 9
AC_COUNT: 22
CC_COUNT: 11
```

## CORRECTION SCOPE

This V2 correction adds no semantic owner, storage domain, state, authority
source, or path. It binds the local mutation invariant to all four existing
Attempt Runtime mutation operations and replaces the prior verification
obligation labels with operational rows. Read-only lookup and admissibility do
not use replacement.

## SAFE REPLACEMENT PROTOCOL

The mandatory Change-local mutation invariant for every authoritative Attempt
Runtime store mutation is:

```text
SAFE_REPLACEMENT:
prepare -> validate -> replace -> verify -> hash
```

The protocol applies to initial materialization, atomic claim
`ACTIVATABLE -> IN_FLIGHT`, normal terminalization, and interrupted recovery
terminalization. It does not apply to lookup or admissibility.

### PREPARE

`PREPARE` constructs the complete proposed authoritative store document in
memory, including all unchanged records and the intended new or transitioned
record. It canonical-encodes the complete bytes, creates a same-directory
temporary file with exclusive creation, writes only the temporary file, flushes
the contents, and fsyncs the temporary file. The valid authoritative target is
not modified, truncated, unlinked, or replaced during this phase.

```text
VALID_TARGET_UNTOUCHED_BEFORE_PREPARED_REPLACEMENT_EXISTS: YES
VALID_TARGET_UNTOUCHED_BEFORE_VALIDATED_REPLACEMENT: YES
TEMPORARY_FILE: SAME_DIRECTORY / EXCLUSIVE_CREATE
TEMPORARY_CONTENTS: COMPLETE_CANONICAL_DOCUMENT
TEMPORARY_FSYNC_BEFORE_REPLACE: YES
```

For materialization, input decoding may occur before the mutation lock, but the
authoritative store read, complete-lineage check, ordinal allocation, proposed
document construction, and replacement protocol occur under the resolved
Attempt-store mutation lock. Claim and both terminalization operations hold
that lock from authoritative read and transition check through replacement and
verification. The lock is not a lease or runtime state.

### VALIDATE

`VALIDATE` validates the complete prepared replacement before the target can be
replaced. It uses the strict store decoder, rejects duplicate JSON members,
validates schema/version, validates every Attempt identity and embedded identity,
validates runtime-state and terminal-result consistency, validates exact
authorization-reference placement where applicable, canonical-re-encodes the
document, and requires the prepared bytes to equal those canonical bytes.

Validation also proves that every unrelated authoritative record from the
pre-mutation document remains present and unchanged in the proposed document.
If validation fails, the authoritative target remains unchanged, the temporary
file is removed where possible, and the operation fails closed.

### REPLACE

`REPLACE` occurs only after successful preparation and validation while the
required authoritative mutation lock is held. It uses same-filesystem,
repository/platform-approved atomic replacement, expected to be `os.replace`
with the temporary file and target in the same directory. Never delete/truncate
a valid target before replacement has been successfully materialized and
validated. The protocol never deletes or truncates the valid target first. A
pre-replace failure preserves the
previous valid target.

### VERIFY

`VERIFY` immediately rereads the actual target bytes after replacement while
the mutation ownership/lock semantics still protect the transition. It strictly
decodes and validates the whole authoritative document, proves that the
intended materialization or state transition exists exactly, proves unrelated
records remain intact, and compares the actual bytes with canonical bytes where
applicable. A post-replace verification failure returns a hard storage or
integrity error; it does not silently claim mutation success and does not invent
an unsafe rollback protocol.

### HASH

`HASH` computes SHA256 from the verified authoritative bytes after successful
reread. The hash is evidence only. It is not authority and does not modify the
store or promote an otherwise failed operation.

## SAFE REPLACEMENT FAILURE SEMANTICS

```text
BEFORE_REPLACE_FAILURE: PREVIOUS_VALID_TARGET_PRESERVED
AFTER_ATOMIC_REPLACE_BEFORE_CALLER_RECEIPT: NEW_COMPLETE_STATE_MAY_ALREADY_BE_DURABLE
CALLER_UNCERTAINTY: NO_IMPLICIT_REPLAY_OR_RESET
ABRUPT_LOSS_AFTER_CLAIM: IN_FLIGHT_PRESERVED
AUTOMATIC_ROLLBACK: NO
AUTOMATIC_RETRY: NO
AUTOMATIC_RESET: NO
LEASE_EXPIRY: NO
WATCHDOG_TRANSITION: NO
```

If the process fails before replacement, the prior valid target remains. If it
fails after atomic replacement but before the caller receives a result, the
next exact lookup determines the authoritative state; the caller must not
replay, reset, or infer that the authorization or transition was unused. A
crash after claim therefore leaves durable `IN_FLIGHT` until explicit owner
recovery. A missing target before initial materialization is allowed, but no
valid existing target may be destroyed before a validated replacement exists.

## ATTEMPT RUNTIME OWNER

```text
SEMANTIC_OWNER: PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY
OWNER_PATH: src/planning_lite/attempt_runtime.py
AUTHORITATIVE_SOURCE_COUNT: 1
SECOND_ATTEMPT_STORE: NO
ATTEMPT_IDENTITY: AttemptRecordV1.attempt_id
STATE_SET: ACTIVATABLE / IN_FLIGHT / TERMINAL
```

The runtime owner alone owns store discovery, strict decoding, complete
document validation, locking, safe replacement, materialization, exact lookup,
admissibility, claim, terminalization, and explicit interruption recovery. It
does not own authorization issuance, execution authority, lifecycle state,
receipts, or evaluation policy.

## AUTHORIZATION BINDINGS

Preparation continues to resolve:

```text
resolve_authorization(target, authorization_ref,
                      OWNER_AUTHORIZED_ATTEMPT_PREPARATION,
                      PreparationScopeV1(change_id, task_or_operation_id))
```

The exact record must be `AUTHORIZED` and pass the preparation applicability
validator before lineage validation, ordinal allocation, or materialization.
Malformed, absent, not-found, corrupt, wrong-action, wrong-scope,
non-`AUTHORIZED`, fabricated, and decoy references fail closed.

Recovery continues to resolve:

```text
resolve_authorization(target, authorization_ref,
                      OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION,
                      RecoveryScopeV1(attempt_id))
```

The exact Attempt must be `IN_FLIGHT`; the exact record must be `AUTHORIZED`
and pass the recovery applicability validator before same-Attempt interrupted
terminalization. Preparation authorization cannot recover, recovery
authorization cannot prepare, and `attempt_id` possession is not authority.

Successful preparation single-use remains enforced by the Attempt-store lock
and the exact immutable `authorization_ref` stored in the successful
`AttemptRecordV1`. Successful recovery single-use remains enforced by the
irreversible `IN_FLIGHT -> TERMINAL` state transition and persisted recovery
reference. The authorization source is not mutated and no consumption registry
is added.

## PREPARATION FLOW

The production application seam remains:

```text
explicit owner decision
  -> trusted local authorization issuer
  -> planning-lite attempt-prepare <target> --input <PREPARATION.json>
  -> exact preparation resolver and applicability validation
  -> Attempt-store lock and complete lineage validation
  -> safe replacement: prepare -> validate -> replace -> verify -> hash
  -> authoritative readback by returned attempt_id
```

The owner need not hand-type CLI arguments or preparation JSON. The agent or a
bounded local control-plane action may construct machine input only after the
owner decision. The adapter never executes, claims, terminalizes, selects
guidance, infers identity, or creates a retry.

## LOOKUP / ADMISSIBILITY

Exact lookup accepts only a complete `attempt_id` and returns `FOUND`,
`NOT_FOUND`, `INVALID_ID`, or `CORRUPT_CONFLICT`, with any `INVALID_RECORD`
treatment bounded to the accepted mechanical fail-closed alias. It never uses
latest, fuzzy, receipts, CURRENT, ACTIVE, Git, `.local`, environment strings,
or reconstructed records.

Admissibility is pure and read-only. It returns `ADMISSIBLE` only for one valid
authoritative `ACTIVATABLE` record and rejects invalid, absent, corrupt,
`IN_FLIGHT`, and `TERMINAL` records without granting authority or mutating the
store.

## ATOMIC CLAIM

Under the Attempt-store mutation lock, claim reads and validates the complete
authoritative document, confirms the exact record is `ACTIVATABLE`, constructs
the complete proposed document with `IN_FLIGHT`, and applies the safe
replacement protocol. Exactly one competing process can win. A repeated or
losing claim fails closed. Claim is reservation of an already-authorized
Attempt occurrence, not execution authorization.

## TERMINALIZATION / RECOVERY

Normal terminalization accepts a same-Attempt `ObservedResultV1` with one of
`COMPLETED`, `FAILED`, `INTERRUPTED`, or `INVALID`, only from current
`IN_FLIGHT`, and persists the irreversible `TERMINAL` envelope using safe
replacement. It remains a future executor fact flow for normal operation.

Interrupted recovery requires exact `attempt_id`, current `IN_FLIGHT`, exact
owner recovery authorization, and an `ObservedResultV1(INTERRUPTED)` fact. It
uses the same lock and safe replacement protocol to persist the terminal fact
and exact recovery reference. Races, wrong-Attempt facts, terminal replay,
direct `ACTIVATABLE -> TERMINAL`, and reactivation fail closed.

## HUMAN / AGENT INTERACTION

```text
PRIMARY_OWNER_INTERACTION_STYLE: VS_CODE_CHAT_AGENT
MANUAL_CLI_TYPING_REQUIRED_FROM_OWNER: NO
CHAT_TEXT_ALONE_IS_MACHINE_AUTHORIZATION: NO
OWNER_DECISION_AUTHORITY_TRANSFER_TO_AGENT: NO
NEW_VS_CODE_EXTENSION_REQUIRED: NO
NEW_CHAT_SUBSYSTEM_REQUIRED: NO
```

The owner explicitly decides in chat. The agent is an operator of the trusted
local application/control-plane seam after that decision, not the authority
issuer or decision-maker. The CLI remains a machine-facing application
adapter.
CLI_APPLICATION_ADAPTER_RETAINED: YES

## EXACT IMPLEMENTATION SURFACE

```text
src/planning_lite/attempt_runtime.py
src/planning_lite/cli.py
tests/test_attempt_runtime.py
tests/test_cli.py
tests/test_system_traversability.py
```

`src/planning_lite/authorization.py` is a `READ_ONLY_DEPENDENCY`. Its resolver,
validators, issuer behavior, codec, and owner tests are reused; no source or
test mutation is planned there.

## PATH BUDGET

```text
TOTAL_PLANNED_PATH_COUNT: 5
HISTORICAL_PATH_COUNT: 5
PATH_BUDGET_DELTA: 0
AUTHORIZATION_MODULE_MUTATION_REQUIRED: NO
UNJUSTIFIED_PATH_COUNT: 0
```

Safe-replacement tests live in `tests/test_attempt_runtime.py`; no new path is
needed. Production adapter and system seam tests remain in the existing CLI and
system test paths.

## TASK GRAPH

| Task | Responsibility | Depends on | Implementation/evidence boundary |
|---|---|---|---|
| T-01 | Runtime owner, canonical envelope, strict decoder, store path, lock, safe replacement protocol | none | implementation in `attempt_runtime.py`; no authorization issuance |
| T-02 | Preparation resolver binding, lineage validation, ordinal allocation, preparation single-use | T-01 | implementation in runtime owner; exact auth action/scope before mutation |
| T-03 | Lookup, admissibility, claim, terminalization, recovery state machine | T-01, T-02 | implementation in runtime owner; all mutations use safe replacement |
| T-04 | Thin preparation CLI/application adapter | T-01, T-02 | implementation in `cli.py`; delegate only |
| T-05 | Thin interrupted-recovery CLI/application adapter | T-01, T-03 | implementation in `cli.py`; delegate only |
| T-06 | Direct runtime, codec, fault, process-boundary, and state evidence | T-01, T-02, T-03 | evidence in `test_attempt_runtime.py`; no hidden product task |
| T-07 | Real CLI production-equivalent authorization and reuse evidence | T-04, T-05, T-06 | evidence in `test_cli.py`; no hidden issuer subsystem |
| T-08 | System traversability, authority-routing, decoy, and false-done evidence | T-04, T-05, T-07 | evidence in `test_system_traversability.py` |
| T-09 | Completion checks, write-boundary adjudication, and handoff receipt | T-01 through T-08 | later gate evidence; no implementation or downstream work |

TASK_GRAPH_ACYCLIC: YES

The dependency graph is acyclic and ordered. Authorization integration occurs
in T-02/T-03 before dependent production and system proofs. T-06 through T-09
are evidence or handoff tasks and do not conceal implementation.

## VERIFICATION CONTRACT

Every verification row below is a distinct closure obligation and contains:

```text
V_ID
SUBJECT
PROBE / EXACT OPERATION
INPUT / FIXTURE
EXPECTED RESULT
EVIDENCE LOCATION
FAILURE MEANING
```

The exact test names are planned names; implementation may choose equivalent
names only if it preserves the stated operation, observable result, evidence
owner, and failure meaning. A helper-only pass cannot close a row whose subject
requires a production seam. Every mutation probe observes the authoritative
store and, where relevant, authorization bytes before and after the operation.

## VERIFICATION TABLE

| V_ID | Subject | Probe / exact operation | Fixture/input | Expected result | Evidence location | Failure meaning |
|---|---|---|---|---|---|---|
| V-01 | Authority and precondition integrity | Run `git rev-parse HEAD`, verify index empty, and compute SHA256 for Definition, Activation, Authorization Closure, first corrected Plan, and first review under declared conventions | Pinned hashes and expected HEAD from the owner gate | Every hash and HEAD matches; index is empty; no tracked source/test mutation is attributed to this Plan | `tests/test_attempt_runtime.py::test_entry_authority_hashes_and_write_boundary`; later owner-gate receipt | Any mismatch blocks the correction as authority drift or baseline drift |
| V-02 | Store schema and canonical codec | Call planned strict encode/decode and inject duplicate keys, wrong schema, malformed JSON, noncanonical bytes, invalid identity, invalid state/result pairing, and invalid auth-reference placement | Complete valid envelope plus one mutation per malformed fixture | Valid canonical bytes round-trip; every malformed or noncanonical fixture fails closed without target mutation | `tests/test_attempt_runtime.py::test_store_codec_strict_fail_closed` | Failure leaves store integrity and lookup contract unproven |
| V-03 | Store ownership and path | Resolve the store through effective target policy and inspect the path used by every runtime operation | Disposable target with valid planning root plus alternate `.local`, receipt, and central paths | Exactly one target-local store is selected; lookup does not create it; no alternate path is read or written | `tests/test_attempt_runtime.py::test_store_path_is_policy_resolved_and_owner_scoped` | Failure permits a second authority or unstable store location |
| V-04 | Preparation production seam | Issue valid preparation authority through the existing issuer, invoke `planning-lite attempt-prepare <target> --input <fixture>`, then read back by returned ID | Disposable target; exact Change/task scope; complete canonical preparation input | Real adapter returns one canonical ID; authoritative store contains one `ACTIVATABLE` Attempt with exact auth ref; authorization bytes are unchanged | `tests/test_cli.py::test_attempt_prepare_uses_production_runtime_adapter` | Failure means production materialization is absent or fake-store-only |
| V-05 | Preparation authorization fail-closed matrix | Invoke the real preparation adapter once per parameterized invalid case and inspect exit/result, Attempt store, and authorization bytes | Missing, malformed, absent, corrupt, wrong-action, wrong-Change, wrong-task, non-`AUTHORIZED`, fabricated, and decoy refs | Every case rejects before allocation/materialization; no new Attempt; authorization source remains unchanged | `tests/test_attempt_runtime.py::test_preparation_authorization_negative_matrix`; `tests/test_cli.py::test_cli_preparation_authorization_negative_matrix` | Failure reopens MF-01 and permits arbitrary or cross-scope authority |
| V-06 | Preparation single-use and non-consumption | Run valid preparation twice with the same ref, then run a failure before publication followed by a valid retry; compare store and auth bytes | One valid preparation ref; invalid lineage and injected pre-replace failure fixtures | First call succeeds once; second call rejects; failed pre-publication call leaves no Attempt and later valid call succeeds; auth bytes never change | `tests/test_attempt_runtime.py::test_preparation_single_use_and_failed_attempt_non_consumption` | Failure permits reuse or ambiguous consumed-without-Attempt state |
| V-07 | Identity, lineage, and ordinal allocation | Prepare sequential and concurrent same-scope inputs, then decode complete authoritative lineage and apply existing ordinal validator | Complete same Change/task lineage, foreign lineage, gaps, duplicate ordinals, and concurrent preparations | IDs are exact `AttemptRecordV1.attempt_id`; ordinals are contiguous and unique; foreign/gapped lineage fails closed | `tests/test_attempt_runtime.py::test_identity_lineage_and_ordinal_allocation` | Failure permits second identity, reconstructed identity, or duplicate occurrence |
| V-08 | Exact lookup | Call lookup with exact valid ID, absent valid ID, malformed ID, duplicate/conflicting store, and corrupt bytes | Materialized target plus each lookup-negative fixture | Results are exactly `FOUND`, `NOT_FOUND`, `INVALID_ID`, or `CORRUPT_CONFLICT`; no fallback or reconstruction occurs | `tests/test_attempt_runtime.py::test_exact_lookup_contract` | Failure permits fuzzy/latest lookup or non-authoritative reconstruction |
| V-09 | Pure admissibility | Call admissibility for valid `ACTIVATABLE`, `IN_FLIGHT`, `TERMINAL`, absent, invalid, and corrupt records while snapshotting store bytes | One target fixture for each state/outcome | Only valid `ACTIVATABLE` returns `ADMISSIBLE`; operation is read-only and grants no authority | `tests/test_attempt_runtime.py::test_admissibility_is_pure_and_state_bounded` | Failure leaks authority or mutates runtime truth during a read |
| V-10 | Atomic multi-process claim | Spawn competing processes against one `ACTIVATABLE` ID, collect results, and reread authoritative state | One valid materialized Attempt; at least two independent processes | Exactly one process succeeds; all others fail closed; final state is `IN_FLIGHT`; no automatic reset occurs | `tests/test_attempt_runtime.py::test_multiprocess_claim_has_one_winner` | Failure means the claim transition is not atomic or is thread-only |
| V-11 | Abrupt loss and durable `IN_FLIGHT` | Child process claims then is terminated before caller completion; parent rereads, attempts a second claim, and performs a valid owner-store operation to prove lock release | Disposable target; materialized Attempt; controlled child termination | Reread shows durable `IN_FLIGHT`; second claim rejects; no timeout/retry/reset; lock can be reacquired for explicit owner recovery | `tests/test_attempt_runtime.py::test_abrupt_loss_preserves_in_flight_and_releases_lock` | Failure permits hidden rollback, lease, watchdog, or ambiguous lock state |
| V-12 | Recovery authorization fail-closed matrix | Invoke real recovery adapter for each invalid authority/state combination and inspect terminal store bytes | Malformed, missing, not-found, corrupt, preparation ref, other-Attempt ref, ID-only request, `ACTIVATABLE`, `TERMINAL`, and wrong-scope fixtures | Every invalid case rejects; no terminal mutation; exact valid recovery succeeds only for matching `IN_FLIGHT` Attempt | `tests/test_cli.py::test_cli_recovery_authorization_negative_matrix`; `tests/test_attempt_runtime.py::test_recovery_authorization_negative_matrix` | Failure reopens MF-02 and permits unauthorized or cross-Attempt interruption |
| V-13 | Recovery single-use and replay | Run valid recovery once, repeat the same request, and try the same ref against another ID | One in-flight Attempt and exact recovery authority | First request creates one `TERMINAL` `INTERRUPTED` fact; replay and cross-Attempt use reject; no reactivation | `tests/test_attempt_runtime.py::test_recovery_single_use_and_replay` | Failure permits recovery replay or reuse |
| V-14 | Terminal contract and irreversibility | Call terminalization with same-Attempt `COMPLETED`, `FAILED`, `INTERRUPTED`, and `INVALID`; then test wrong ID, direct activation terminalization, and conflicting second fact | In-flight fixtures and one canonical `ObservedResultV1` per status | Each supported status terminalizes exactly once; wrong/conflicting/direct-transition cases fail; terminal is irreversible | `tests/test_attempt_runtime.py::test_terminal_status_contract_and_irreversibility` | Failure changes canonical status or permits terminal overwrite |
| V-15 | Safe-replacement fault preservation | Inject validation failure, temporary-write failure, pre-replace failure, and post-replace verification fault; inspect old/new bytes and SHA256 | Valid target with unrelated record; fault-injection hooks at each phase | Before replace, old target bytes/hash and unrelated records remain unchanged; replace sees only fully validated bytes; post-replace verification failure is hard error; no delete/truncate precedes replacement | `tests/test_attempt_runtime.py::test_safe_replacement_fault_preservation` | Failure reopens MF3-01 and permits store loss or false success |
| V-16 | CLI thinness and authority separation | Inspect planned handlers through direct adapter tests and invoke each command with valid/invalid inputs; assert runtime owner is the only mutator | Preparation and recovery command fixtures | CLI parses/delegates/renders only; no CLI state machine, alternate store, issuer decision, receipt, lifecycle, or guidance selection is used | `tests/test_cli.py::test_attempt_commands_are_thin_adapters` | Failure transfers runtime or owner authority into CLI |
| V-17 | Decoy authority rejection | Place decoy values in CURRENT, ACTIVE, `.local`, RunReceipt, prose, request body, Git message, and environment; invoke real adapters | Each decoy carries a valid-looking or conflicting ref while authoritative store lacks matching proof | No decoy routes or authorizes preparation/recovery; only target-local resolver result is accepted | `tests/test_system_traversability.py::test_decoy_authority_sources_cannot_authorize_attempts` | Failure creates a second authority model or false-done route |
| V-18 | Authorization module boundary | Run the focused tests with `authorization.py` and its owner tests unchanged; inspect Git path ownership after planned implementation | Closed module hash/path and five-path mutation allowlist | Runtime imports/reuses resolver/validators; no Authorization source/test path changes; no second resolver, issuer, or store | `tests/test_cli.py::test_attempt_runtime_reuses_closed_authorization_boundary`; later `git diff --name-only` receipt | Failure is closed-prerequisite incompatibility and blocks this Plan |
| V-19 | PL08, executor, and lifecycle separation | Inspect imports/call graph and exercise runtime APIs without executor, lifecycle, or Change-2 modules | PL08 contract fixtures; absent executor/lifecycle/Change-2 implementation | Runtime reuses Attempt/ObservedResult contracts but owns persistence; no evaluator pump, executor call, lifecycle store, or Change-2 state appears | `tests/test_attempt_runtime.py::test_authority_boundaries_are_separate`; `tests/test_system_traversability.py::test_downstream_executor_remains_next_break` | Failure transfers authority or makes closure executor-dependent |
| V-20 | Production preparation proof | In a clean disposable target, create authority via trusted issuer, invoke the actual preparation CLI, read back exact ID, inspect state/provenance, and attempt helper-only bypass comparison | Clean Git target; valid issuer record; no pre-seeded Attempt store | Production command alone materializes the valid Attempt; helper-only or manually seeded record cannot substitute; whole auth/occurrence distinction is observed | `tests/test_cli.py::test_clean_target_production_preparation_materialization`; later disposable adoption receipt | Failure means the claimed production seam is not wired |
| V-21 | Production recovery proof | In the same production-equivalent target, claim through runtime, simulate process loss, create exact owner recovery authority, invoke actual recovery CLI, and reread terminal state | Clean target; one `IN_FLIGHT` Attempt; exact recovery authority; executor absent | Actual recovery adapter produces same-Attempt `TERMINAL(INTERRUPTED)` with exact recovery ref; invalid/replay paths remain rejected | `tests/test_cli.py::test_clean_target_production_interrupted_recovery`; later recovery evidence receipt | Failure means owner recovery is helper-only or not callable |
| V-22 | Bounded system traversability | Run the production-equivalent walking skeleton and feed only observed seam facts into the existing traversability projection | Valid preparation, exact lookup, admissibility, claim, and valid recovery; executor callable absent | Attempt-access seam is `WIRED_TRAVERSABLE`; next break is `GOVERNED_EXECUTOR_CALLABLE_BINDING / WIRING_GAP`; whole journey is not passing | `tests/test_system_traversability.py::test_attempt_access_seam_is_wired_traversable` | Failure prevents claiming the bounded seam and exposes the earlier break |
| V-23 | False-done and forbidden-shortcut matrix | Run one nearest-wrong case for fabricated/cross-scope/reused authority, chat/prose/decoy authority, fake-store proof, thread-only claim, CLI state, and executor overclaim | Parameterized forbidden shortcut fixtures and absent downstream prerequisites | Every shortcut rejects or remains explicitly non-passing; only production seam and process proof satisfy closure | `tests/test_system_traversability.py::test_false_done_shortcuts_are_rejected`; later owner review receipt | Failure allows green-looking evidence without semantic closure |
| V-24 | Repository completion and integrity checks | Run `uv sync`, focused suite, full `uv run pytest`, `git diff --check`, clean disposable adoption, `planning-lite doctor`, and later clean-checkout verification | Clean committed central source for adoption/doctor; implementation-gate allowlist; no staged paths | All required checks pass; project-owned files remain unchanged; no tracked mutation outside five paths; clean-checkout receipt is produced at the later authorized gate | T-09 completion receipt; `tests/test_system_traversability.py` for system portion; later clean adoption and doctor receipts | Failure blocks handoff or proves repository/write-boundary closure incomplete |

```text
VERIFICATION_COUNT: 24
DUPLICATE_OR_COSMETIC_V_COUNT: 0
VERIFICATION_TABLE_OPERATIONAL: PASS
EVERY_V_HAS_EXACT_PROBE: YES
EVERY_V_HAS_EXPECTED_RESULT: YES
EVERY_V_HAS_EVIDENCE_LOCATION: YES
EVERY_V_HAS_FAILURE_MEANING: YES
```

## AC TRACEABILITY

```text
AC_COUNT: 22
```

| AC | Responsible task(s) | Verification IDs | Exact expected proof |
|---|---|---|---|
| AC-01 | T-01, T-06, T-08 | V-01, V-03, V-18, V-19, V-22 | One PL09 runtime owner and one target-local source exist; evidence surfaces and closed Authorization remain consumers only. |
| AC-02 | T-01, T-02, T-06 | V-02, V-07, V-08 | `AttemptRecordV1.attempt_id` and Change/task/ordinal identity validate exactly; no alternate identity or reconstruction is accepted. |
| AC-03 | T-01, T-06 | V-02, V-03, V-07, V-15 | One durable source preserves immutable provenance, uniqueness, complete records, and unrelated records across replacement. |
| AC-04 | T-02, T-04, T-07, T-08 | V-04, V-20, V-22 | Real preparation adapter materializes one authorized Attempt before execute and returns exact readback ID. |
| AC-05 | T-01, T-02, T-04, T-05, T-07, T-08 | V-04, V-05, V-12, V-16, V-17, V-18 | Authority is resolved from exact action/scope records; PL08 supplies identity rules; runtime persists but cannot invent authority. |
| AC-06 | T-02, T-06, T-07 | V-08 | Exact lookup returns only the four bounded outcomes and never uses latest, fuzzy, fallback, or reconstruction. |
| AC-07 | T-02, T-03, T-06, T-07, T-08 | V-02, V-05, V-12, V-17, V-23 | Malformed, duplicate, corrupt, fabricated, decoy, wrong-scope, and invalid-state inputs fail closed through real boundaries. |
| AC-08 | T-01, T-03, T-06 | V-09, V-11, V-14 | Only `ACTIVATABLE`, `IN_FLIGHT`, and `TERMINAL` exist; abrupt loss leaves `IN_FLIGHT` and terminal facts are irreversible. |
| AC-09 | T-02, T-06, T-07 | V-09, V-17 | Pure admissibility succeeds only for one valid `ACTIVATABLE` record and causes no mutation or authority grant. |
| AC-10 | T-03, T-06 | V-10, V-11 | Multi-process claim has exactly one winner and all competing/repeated claims fail closed. |
| AC-11 | T-03, T-06 | V-11 | Process loss preserves durable `IN_FLIGHT` with no reset, retry, lease, timeout, or watchdog transition. |
| AC-12 | T-03, T-05, T-07 | V-12, V-13, V-21 | Explicit exact owner recovery is the only interruption path and terminalizes only the same in-flight Attempt. |
| AC-13 | T-03, T-06 | V-14 | Same-Attempt `ObservedResultV1` statuses `COMPLETED`, `FAILED`, `INTERRUPTED`, and `INVALID` terminalize once and cannot be overwritten. |
| AC-14 | T-01, T-02, T-03, T-04, T-05, T-08 | V-04, V-05, V-10, V-12, V-16, V-19, V-22 | Preparation, claim, normal terminalization, and recovery each use the required authority owner and runtime enforcement boundary. |
| AC-15 | T-02, T-03, T-04, T-05, T-07, T-08 | V-04, V-05, V-08, V-12, V-16, V-17, V-20, V-21 | Reusable application APIs and thin adapters prove authority and exact access without CLI ownership or decoy routing. |
| AC-16 | T-02, T-03, T-06 | V-09, V-19, V-22 | Future lifecycle consumption is bounded to existing Attempt access and cannot create, own, reconstruct, or persist runtime truth. |
| AC-17 | T-01, T-06 | V-02, V-14, V-19 | PL08 contracts remain canonical and evaluator-owned; runtime uses them without moving evaluation or orchestration authority. |
| AC-18 | T-03, T-05, T-08 | V-14, V-19, V-21, V-22, V-24 | Executor callable behavior and normal production facts remain outside this Change; executor is the explicitly recorded next seam. |
| AC-19 | T-01, T-04, T-05, T-06, T-07, T-08, T-09 | V-15, V-16, V-17, V-18, V-19, V-23, V-24 | No receipt/evidence/CLI/lifecycle/registry/Change-2 surface becomes Attempt truth or an authority shortcut. |
| AC-20 | T-04, T-05, T-06, T-07, T-08 | V-04, V-20, V-21, V-22 | Real production preparation, lookup, admissibility, claim, recovery, and durable readback prove bounded closure before executor work. |
| AC-21 | T-03, T-06 | V-14 | Contract-level tests cover all four terminal statuses and irreversibility without requiring executor or RunReceipt. |
| AC-22 | T-08, T-09 | V-01, V-22, V-23, V-24 | The bounded Attempt-access seam is traversable, the executor callable binding remains next, and no whole-journey PASS is claimed. |

```text
AC_TRACEABILITY: 22/22
AC_TRACEABILITY_SUBSTANTIVE: PASS
```

## CC TRACEABILITY

```text
CC_COUNT: 11
```

| CC | Implementation prerequisite | Verification IDs | Closure evidence location |
|---|---|---|---|
| CC-01 | T-01 owner and T-08 boundary proof | V-01, V-03, V-18, V-19, V-22 | `tests/test_attempt_runtime.py`, `tests/test_system_traversability.py`, and later write-boundary receipt |
| CC-02 | T-01 strict durable source and T-03 mutation protocol | V-02, V-03, V-11, V-14, V-15 | `tests/test_attempt_runtime.py` codec/state/fault rows and verified store readback |
| CC-03 | T-02 preparation binding and T-04/T-07 production adapter | V-04, V-05, V-06, V-07, V-20 | `tests/test_cli.py` production preparation rows plus disposable-target receipt |
| CC-04 | T-02/T-06 lookup and T-07 adapter evidence | V-08, V-17, V-20 | `tests/test_attempt_runtime.py`, `tests/test_system_traversability.py`, exact lookup readback |
| CC-05 | T-02/T-06 pure admissibility | V-09 | `tests/test_attempt_runtime.py::test_admissibility_is_pure_and_state_bounded` |
| CC-06 | T-03/T-06 atomic claim | V-10, V-11 | `tests/test_attempt_runtime.py` multi-process and abrupt-loss evidence |
| CC-07 | T-03/T-05/T-07 recovery binding and adapter | V-12, V-13, V-21 | `tests/test_cli.py`, `tests/test_attempt_runtime.py`, production recovery receipt |
| CC-08 | T-03/T-06 terminal contract | V-14, V-19, V-24 | `tests/test_attempt_runtime.py`, boundary test, and completion receipt |
| CC-09 | T-02/T-03/T-07/T-08 negative and false-done proof | V-05, V-08, V-12, V-17, V-23 | `tests/test_attempt_runtime.py`, `tests/test_cli.py`, `tests/test_system_traversability.py` |
| CC-10 | T-01 through T-08 adapter and ownership boundary | V-09, V-16, V-18, V-19, V-22 | runtime/CLI/system tests and closed-module Git path receipt |
| CC-11 | T-04/T-05/T-08/T-09 bounded seam and handoff | V-04, V-20, V-21, V-22, V-23, V-24 | `tests/test_system_traversability.py` plus clean adoption/doctor and later handoff receipts |

```text
CC_TRACEABILITY: 11/11
CC_TRACEABILITY_SUBSTANTIVE: PASS
```

## INDEPENDENT CLOSURE SIMULATION

```text
EXECUTOR_PREREQUISITE: ABSENT
LIFECYCLE_IMPLEMENTATION: ABSENT
CHANGE_2: PAUSED
PL08_ROLE: CONTRACT_AND_EVALUATOR_ONLY
EXECUTOR_DEPENDENCY: NO
RUNRECEIPT_DEPENDENCY: NO
EXECUTOR_INDEPENDENT_CLOSURE_PLAN: PASS
EXECUTOR_INDEPENDENT_CLOSURE_SIMULATION: PASS
```

The simulation uses V-04, V-08, V-09, V-10, V-11, V-12, V-13, V-14, V-20,
V-21, and V-22. It proves preparation, exact access, admissibility, one-winner
claim, durable abrupt-loss handling, and explicit owner recovery without a
callable executor, lifecycle persistence, Change-2 state, or evaluator pump.
Normal executor-produced terminal facts remain future consumers.

## SYSTEM TRAVERSABILITY

```text
BEFORE: NO_AUTHORITATIVE_ATTEMPT_RUNTIME_SOURCE / ORCHESTRATION_GAP
AFTER: AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_AVAILABLE
ATTEMPT_ACCESS_SEAM: WIRED_TRAVERSABLE
BOUNDED_SEAM: valid preparation -> lookup -> admissibility -> claim -> valid owner recovery
NEXT_BROKEN_SEAM: GOVERNED_EXECUTOR_CALLABLE_BINDING / WIRING_GAP
WHOLE_SELF_HOSTED_JOURNEY: NOT_CLAIMED_PASSING
```

V-20 and V-21 require real production-equivalent application seams. V-22
projects only observed facts into the existing traversability contract. A
helper-only result cannot promote the system seam.

## FALSE-DONE RESISTANCE

The corrected Plan rejects completion based on arbitrary or cross-scope refs,
preparation reuse, recovery replay, self-authorization, chat/prose authority,
CURRENT/ACTIVE/.local/receipt/Git/environment decoys, fake-store seeding,
thread-only claim proof, unsafe replacement, CLI-local state, executor absence,
or whole-journey overclaim. V-15 and V-23 are direct probes for the two ways a
green row count could otherwise conceal a false result.

## COMPLETION VERIFICATION

The later authorized implementation gate must run:

```text
uv sync
uv run pytest tests/test_attempt_runtime.py tests/test_cli.py tests/test_system_traversability.py
uv run pytest
git diff --check
clean disposable Git adoption
planning-lite doctor in the disposable target
later clean-checkout and post-commit verification
```

V-24 owns these completion checks. Consumer/update smoke tests whose source
identity depends on Git metadata must use a clean committed central source.
This V2 artifact itself performs no implementation tests and authorizes no
source, test, staging, commit, or push mutation.

## CODING QUALITY GUIDANCE

Prospective Attempt Runtime source must include a module responsibility
docstring, public symbol docstrings, rationale comments for lock lifetime,
single-use enforcement, crash semantics, and safe replacement, and explicit
side-effect/fail-closed documentation. Comments explain why the invariant is
needed rather than paraphrasing code. These remain coding guidance, not new
Definition ACs.

## ARCHITECTURE STOP

```text
PLAN_ARCHITECTURE_STOP: NO
ARCHITECTURE_STOP_REASON: neither correction adds an owner, storage domain, state, or authority model
MODEL_ESCALATION: NOT_TRIGGERED
```

Safe replacement is local mutation mechanics and verification precision within
the existing runtime owner. No Definition amendment, Authorization source
change, or new architecture is required.

## UNBOUND CHOICE BUDGET

```text
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_MATERIAL_IMPLEMENTATION_CHOICES: 0
PLAN_DETERMINACY: PASS
```

The mutation order, lock lifetime, failure preservation, post-replace
verification, hash timing, exact probes, expected results, evidence owners,
and failure meanings are now fixed. Remaining mechanical choices such as
private symbol names and test function spelling cannot change semantics or
evidence quality.

## Canonical Plan status

```text
CANONICAL_PLAN_STATUS: CANONICAL / IMPLEMENTATION PLAN
CANONICAL_PLAN_APPROVED: YES
FORMAL_READINESS: NOT_YET_RUN
FORMAL_READINESS_AUTHORIZED: NO
IMPLEMENTATION_AUTHORIZED: NO
SEMANTIC_DRIFT_FROM_REVIEWED_V2: NO
ATTEMPT_RUNTIME_CHANGE: DEFINITION_APPROVED / PLAN_APPROVED / FORMAL_READINESS_NOT_RUN / IMPLEMENTATION_NOT_AUTHORIZED
EXECUTOR_PREREQUISITE: NOT_STARTED
LIFECYCLE_CHANGE: DEFINITION_APPROVED / PLANNING_BLOCKED_BY_PREREQUISITE / IMPLEMENTATION_NOT_AUTHORIZED
CHANGE_2: BLOCKED / VALID / PAUSED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
NEXT_SINGLE_GATE: FORMAL_READINESS_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS
```

This canonical Plan preserves the reviewed V2 semantics and does not authorize
Formal Readiness, implementation, executor work, lifecycle work, Change-2 or
Change-3 work, staging, commit, or push.
