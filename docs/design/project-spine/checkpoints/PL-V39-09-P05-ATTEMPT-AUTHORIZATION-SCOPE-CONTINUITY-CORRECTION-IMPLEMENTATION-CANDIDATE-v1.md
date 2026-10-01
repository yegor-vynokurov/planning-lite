# P-05 Attempt Authorization Scope Continuity Correction - Implementation Candidate v1

Change: `CHG-PL-V39-09-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-001`  
Owner decision: `AUTHORIZE_P05_ATTEMPT_AUTHORIZATION_SCOPE_CONTINUITY_CORRECTION_IMPLEMENTATION_AND_RECHALLENGE` / CONSUMED  
Owner review verdict: `PASS / DEFINITION + PLAN + FORMAL READINESS ACCEPTED`  
Implementation: `CANDIDATE_COMPLETE`  
P-05: `CORRECTED / ADVERSARIAL_RECHALLENGE_PASS`

## Accepted inputs

| Contract | Path | SHA-256 |
|---|---|---|
| Definition v1 | `docs/design/project-spine/checkpoints/PL-V39-09-P05-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-CHANGE-DEFINITION-v1.md` | `faec34cb7f3d9ad103cd16fc7b09e7212f392d35a09053ec371667e04dcf2fa5` |
| Plan v1 | `docs/design/project-spine/checkpoints/PL-V39-09-P05-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-IMPLEMENTATION-PLAN-v1.md` | `19fa2e22f1180d19b03354f8047c658ad5dffdfde33c6de08be342fe352f3434` |
| Formal Readiness v1 | `docs/design/project-spine/checkpoints/PL-V39-09-P05-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-FORMAL-READINESS-VERDICT-v1.md` | `3d52315ebebf7430b7020c4bbb3344dd78d506cc53867d874e9fd2a2904e9e2b` |

## Entry baseline

```text
ENTRY_HEAD: 43c7da88e904231da1bd8c5d63447331d6196e80
ENTRY_AUTHORITY_STATE_ID: 241502fcd1b47bb2da174d54a25d032a16bc867f15573c699b013b84e9858969
ENTRY_CURRENT_SHA256: 78f80cd18ceb90a89ff4e375863d02df05946956d5bd6297c4cf214c98fa93e3
ENTRY_UNRELATED_DIRT_STATE_ID: 2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821
ENTRY_INDEX_EMPTY: YES
ENTRY_GATE: OWNER_REVIEW_P05_ATTEMPT_AUTHORIZATION_SCOPE_CONTINUITY_CORRECTION_DEFINITION_PLAN_AND_READINESS
OWNER_REVIEW_VERDICT: PASS
IMPLEMENTATION_AUTHORIZATION: CONSUMED
```

The accepted Definition, Plan, and Formal Readiness hashes matched at entry. The 14 unrelated dirty paths were captured at entry and remain byte-identical. Their state ID is preserved above.

## Product and test changes

Product path changed: `src/planning_lite/attempt_runtime.py` only. The prior implementation hashed to `0bd6a209c67327523ae005c31b19c28a530c250c5e4fd508c7dbcceb4a650dfe`; the candidate canonical-LF SHA-256 is `5689583d0273e41ca41889a001369cc2280f8550d4e2bb0b46a05cc6ed110dfe`.

Inside `claim_attempt`, the product root is resolved once and the existing store-location helper receives that root. While the existing Attempt mutation lock is held, after reading the authoritative row and confirming `ACTIVATABLE`, the function re-resolves `row.authorization_ref` as `AuthorizationAction.PREPARATION` against `PreparationScopeV1(row.attempt.change_id, row.attempt.task_or_operation_id)`. This occurs before `replace(row, runtime_state="IN_FLIGHT")` and before any replacement write. The resolver uses the stored structured scope, not caller values or a scope parsed from `attempt_id`.

Any non-authorized resolver result follows the existing `AttemptAuthorizationError` path. Rejection leaves the persisted identity, `ACTIVATABLE` state, and canonical store bytes unchanged. Preparation-time validation remains in place.

Test path changed: `tests/test_attempt_runtime.py` only. The prior implementation hashed to `021d2ba53eefb55df0315a0592f246831fdc50932619fdd58ca868eec1f47f64`; the candidate canonical-LF SHA-256 is `144c0817bb80787c1659aee85e4e63a8f28a2f34731bdc676cf59b537d1a318e`.

Two focused regressions construct valid canonical `AttemptRecordV1` mutants from a normally authorized and prepared Attempt. The foreign-Change mutation changes `change_id` and its derived `attempt_id`; the foreign-task mutation changes `task_or_operation_id` and its derived `attempt_id`. Both retain the original valid authorization reference and all unrelated fields. Each explicitly round-trips through `encode_attempt_store` → `decode_attempt_store` → `encode_attempt_store` with byte identity, verifies the original scope resolves `AUTHORIZED` and the mutated scope `WRONG_SCOPE`, then invokes the real `claim_attempt` path.

## P-05 red/green evidence

Pre-fix command:

```text
uv run --frozen pytest -q tests/test_attempt_runtime.py::test_p05_foreign_change_canonical_persisted_attempt_cannot_be_claimed
```

Pre-fix result: expected failure, `DID NOT RAISE AttemptAuthorizationError`. The canonical foreign-Change mutant passed the live scope checks and the unfixed production claim returned through the `IN_FLIGHT` transition.

The previously observed surviving canonical foreign-Change store was `5dfa4216b5faff321a9e7316108b298ef07f52eabdf8ae3a384d1c037d4d995f`; its fixture-local Authorization reference was `authz_e5fa52ff29b74ae62b3dc38986975394`. The fresh test issues a valid reference in its disposable target and recreates that exact scope mutation.

Post-fix results for both foreign-Change and foreign-task mutants:

```text
original authorization document valid: YES / AUTHORIZED
mutated scope resolution: WRONG_SCOPE
claim result: AttemptAuthorizationError
store bytes after rejection: BYTE-IDENTICAL
persisted state after rejection: ACTIVATABLE
persisted identity after rejection: MUTATED NEAREST-WRONG IDENTITY PRESERVED
silent repair: NONE
P05_MUTANT_VALID: YES
P05_PRE_FIX_SURVIVED: YES
P05_POST_FIX_KILLED: YES
DETECTOR: claim_attempt authorization-scope continuity validation
POST_FIX_STORE_BYTES_UNCHANGED: YES
```

The foreign-Change case uses the Definition's exact previously surviving scope mutation: `CHG-P05-ORIGINAL / T-P05-01 / A1` becomes `CHG-P05-FOREIGN / T-P05-01 / A1`; the original valid Authorization document and reference are retained, with a fresh fixture-local reference issued for this test run. The mutation round-trips through the canonical codec before the real production claim.

## A01-A10 acceptance

| Invariant | Result | Evidence |
|---|---|---|
| A01 - valid prepared Attempt claims to `IN_FLIGHT` | PASS | Existing valid claim and lifecycle tests pass. |
| A02 - foreign Change rejected | PASS | Original scope `AUTHORIZED`; foreign persisted scope `WRONG_SCOPE`; exception and unchanged bytes/state. |
| A03 - foreign task rejected | PASS | Original scope `AUTHORIZED`; foreign persisted scope `WRONG_SCOPE`; exception and unchanged bytes/state. |
| A04 - reference presence is insufficient | PASS | The retained reference resolves to a valid `AUTHORIZED` record for the original scope; the persisted foreign scope still rejects. |
| A05 - canonical codec mutant | PASS | Both mutants encode, decode, and re-encode byte-identically before claim. |
| A06 - no silent repair | PASS | Rejected claim preserves bytes and mutated identity, with state still `ACTIVATABLE`. |
| A07 - existing state constraints | PASS | Focused suite preserves no-double-claim, multiprocess one-winner, terminalization, safe replacement, and recovery coverage. |
| A08 - preparation check retained | PASS | Existing wrong-Change and wrong-task preparation cases remain rejected before Attempt store materialization. |
| A09 - exact P-05 rechallenge | PASS | Foreign-Change mutant survived before the correction and is killed afterward with unchanged store bytes. |
| A10 - no new authority | PASS | No new store, policy engine, schema/record, lifecycle state, migration, retry/recovery semantics, or persistence format. `authorization.py` is unchanged. |

## Verification

| Command | Result |
|---|---|
| `uv run --frozen pytest -q tests/test_attempt_runtime.py` | PASS; 29 test cases. |
| `uv run --frozen pytest -q tests/test_authorization.py tests/test_authorization_traversability.py tests/test_operation_lifecycle.py tests/test_system_traversability.py` | PASS. |
| Governed-executor direct-claim owner search | No separate `tests/test_governed_executor.py` case directly calls `claim_attempt`; the full suite includes that module. |
| `uv sync --frozen` | PASS; checked 25 packages. |
| `uv run --frozen pytest` | PASS; 817 passed, 88 existing `pathspec` deprecation warnings in 94.91 seconds. |
| `uv run --frozen python scripts/maintainer_resume.py` | PASS; final CURRENT contract validated after this checkpoint was added. |
| `git diff --check` | PASS. |

The 88 warnings are the existing `pathspec` `GitWildMatchPattern` deprecations from `tests/test_field_control_pack_foundation.py` (44 at each of two call sites). The final full suite was run after the product and test changes; subsequent changes are limited to this checkpoint and the authorized CURRENT projection.

## Lock, authority, and write-boundary review

The Attempt lock scope is unchanged. The retained resolver call is read-only: it scans the immutable Authorization records and does not acquire an Authorization write lock or mutate that store. The check adds no nested write-lock cycle or cross-store mutation. The focused multiprocess single-winner claim test passes.

```text
ATTEMPT_SCHEMA_CHANGED: NO
AUTHORIZATION_SCHEMA_CHANGED: NO
AUTHORIZATION_AUTHORITY_CHANGED: NO
NEW_AUTHORITY_INTRODUCED: NO
AUTHORIZATION_SOURCE_CHANGED: NO
ROADMAP_CHANGED: NO
```

Authorized writes in this transition:

```text
src/planning_lite/attempt_runtime.py
tests/test_attempt_runtime.py
docs/design/project-spine/checkpoints/PL-V39-09-P05-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-IMPLEMENTATION-CANDIDATE-v1.md
docs/design/project-spine/CURRENT.md
```

No other product or test path changed. The unrelated dirty paths remained byte-identical. No files were staged; no commit, push, or release was performed.

## Exit state

```text
EXIT_HEAD: 43c7da88e904231da1bd8c5d63447331d6196e80 / UNCHANGED
EXIT_AUTHORITY_STATE_ID: 18e3e3e34b52271abed321ba99b52c485d887399a8596cc7cd618dc11464766d
EXIT_AUTHORITY_STATE_METHOD: SHA-256 of canonical UTF-8 JSON with sorted keys and compact separators over previous_authority_state_id, candidate_state_id, current_sha256, and sorted source_path_sha256_rows represented as [path, sha256] pairs. CURRENT is represented by current_sha256; this implementation checkpoint is excluded from its own digest.
EXIT_CURRENT_SHA256: 2e229fa4c37e7349ef487e1d6c8652f85ed8681fa00d8031eb701d7f1bcf0987
EXIT_CANDIDATE_STATE_ID: ad347dd572762dc3538d60e9e2515e9cd6918991995e1e5e8f81c99d70eb6c06 / ARCHITECTURE MVP CANDIDATE UNCHANGED
EXIT_UNRELATED_DIRT_STATE_ID: 2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821 / PRESERVED
EXIT_SYNC_STATE_ID: NOT_REPRODUCIBLE_BY_CURRENT_TOOLING
EXIT_INDEX_EMPTY: YES
STAGE: NO
COMMIT: NO
PUSH: NO
RELEASE: NO
SEQUENTIAL_WHOLE_ORGANISM_PROOF: NOT EXECUTED
09-G: NOT STARTED
OPEN_MATERIAL_FINDINGS: NONE
NEXT_SINGLE_GATE: OWNER_REVIEW_P05_ATTEMPT_AUTHORIZATION_SCOPE_CONTINUITY_CORRECTION_IMPLEMENTATION_AND_RECHALLENGE
```

The authority digest source rows are sorted by repository path and use canonical-LF SHA-256. The implementation checkpoint is excluded from its own digest.

| Authority source path | Canonical-LF SHA-256 |
|---|---|
| `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-CHANGE-DEFINITION-v1.md` | `bad0445f477f99d110525d3adfae03e3c2cfe935b84cd2a46707a6f3e4c774cc` |
| `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-CLOSURE-v1.md` | `b16025a7170bc7f14430989c3a203449b95a3432abaeb7231831b59bd76e1e44` |
| `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CHANGE-DEFINITION-v1.md` | `81514c1519bbdf97d2908b1f0ef2a73cae19a76535d22923ed726c82a5c63db1` |
| `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CLOSURE-v1.md` | `3e96782ec6f70db5f6835cdeb90f4e2ee2aef4e92ac8cc21f463e639cc101a6e` |
| `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-FORMAL-READINESS-VERDICT-v1.md` | `b39a1cb5ecfd9cefd592f2bbef38705ede7875329b7d5c74387a60f427ee07ad` |
| `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-IMPLEMENTATION-PLAN-v1.md` | `3347577beb68ab907253c19706436b72d5ec1293f997f9d828990af5f4ce42c6` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-FORMAL-READINESS-VERDICT-v1.md` | `1df443ab1c1d4b493f720458467e5e72243b1600f82d87c987718574ddb36c59` |
| `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-v1.md` | `b38b977fd6858597380dd2db7d7685e7272bc3881776a69370c4e615e671abec` |
| `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-PRODUCT-COMMIT-AND-CLOSEOUT-v1.md` | `4ee775c6d4d5f67d3f142124ec1f04275bca6330d337a777c7f217e970b76960` |
| `docs/design/project-spine/checkpoints/PL-V39-09-P05-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-CHANGE-DEFINITION-v1.md` | `faec34cb7f3d9ad103cd16fc7b09e7212f392d35a09053ec371667e04dcf2fa5` |
| `docs/design/project-spine/checkpoints/PL-V39-09-P05-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-IMPLEMENTATION-PLAN-v1.md` | `19fa2e22f1180d19b03354f8047c658ad5dffdfde33c6de08be342fe352f3434` |
| `docs/design/project-spine/checkpoints/PLANNING-LITE-ORGANISM-VITALITY-AUDIT-v1.md` | `30357ebaa16438ca305dff7e1e373380432b297c92eac922d99135b060859089` |
| `docs/design/project-spine/roadmap/ROADMAP.md` | `056933c1116e3adbaf2330baba32718498aa5cf2f88eb4ea1ef576433392f0bc` |
| `src/planning_lite/attempt_evaluation.py` | `1bffa40ce6a9db27a7ce2e0b39047ca1ae435b9a482da3b9cb25bf5c9cf5cf40` |
| `src/planning_lite/attempt_runtime.py` | `5689583d0273e41ca41889a001369cc2280f8550d4e2bb0b46a05cc6ed110dfe` |
| `src/planning_lite/authorization.py` | `5799e475a58004a45a5816f8a7870e2167beab12adf524756f9ed2e3629499fb` |
| `src/planning_lite/governed_executor.py` | `53f3cb536bb1dc6cd4bf08993f21693f364e94b3f942d7c76c52ebea4d34b087` |
| `src/planning_lite/operation_lifecycle.py` | `71fa2970e567645beca6ef840836bc09f3fe50ec5ed89cdc4bf99c7cfb63f0c3` |
| `tests/test_attempt_runtime.py` | `144c0817bb80787c1659aee85e4e63a8f28a2f34731bdc676cf59b537d1a318e` |
| `tests/test_authorization.py` | `1c5bfbb02d1128ecc2cb1f240d1b838856aafcb1583603b57867679a1f24023a` |
| `tests/test_authorization_traversability.py` | `421b1e30e517551bbff78b8e001cfccb18e22918efaafd00777faec8e339cf48` |
| `tests/test_operation_lifecycle.py` | `b87a9a0040e108663dd64872db9d531a16b98fd8d8de61239ad20834a95ef085` |
| `tests/test_system_traversability.py` | `89f6fbf6d45b32f84e469bc11a5912ca7d2bf3544358295466f5ae917e8ba4a4` |
