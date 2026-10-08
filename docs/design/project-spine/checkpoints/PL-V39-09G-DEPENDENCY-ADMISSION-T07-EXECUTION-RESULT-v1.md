# PL-V39-09G Dependency Admission T-07 Execution Result

## Decision state

```text
change_id: CHG-PL-V39-09G-DEPENDENCY-ADMISSION-001
gate: EXECUTE_09G_DEPENDENCY_ADMISSION_T07
role: T07_TWO_PHASE_IMPLEMENTER
overall: PASS_WITH_NONBLOCKING_REPOSITORY_TEST_HARNESS_LIMIT
T07A: PASS
T07B: PASS
T07_COMPLETE_CANDIDATE: YES
T07_COMPLETE: NO
owner_acceptance: PENDING
implementation_authorization_consumed: YES
T08_T09_AUTHORIZED: NO
```

The one authorized packet completed both `SOURCE_ENDPOINT_BINDING_CONFORMANCE`
and `GOVERNED_BYTE_INTEGRATION_AND_WALKING_SKELETON` without an intermediate
owner gate. This checkpoint submits T-07 for owner adjudication; it does not
accept T-07 or authorize T-08/T-09.

## Entry authority and baseline

```text
repository: D:\documents\planning-lite
branch: reconcile/current-design-spine-2026-08-25
HEAD: e1450c6390bd0630a11e8d1d4219a4228e26fd30
active_change: CHG-PL-V39-09G-DEPENDENCY-ADMISSION-001
Definition_v13_status: APPROVED / CURRENT
Definition_v13_canonical_LF_SHA256: 3cede7673670a7f1b91ff20b6e914461855266afac04e8a5893abc0a3856fc46
Definition_v13_owner_approval_raw_SHA256: e17019184fcd141a95911eda374ec31bd2ddbc7f0527c2a2c69266c233dd5e47
Plan_v11_status: APPROVED / CURRENT
Plan_v11_canonical_LF_SHA256: d0a6e425009c8254bbe79d229fa8a79dbe0407f8882ebdd60e9e856812203685
Plan_v11_owner_approval_raw_SHA256: 502f36a83acbc401d2e03ebf03e54395b11915cdc7baabdc90e038ec0e716a7a
T07_Formal_Readiness_v2: READY
T07_Formal_Readiness_v2_raw_SHA256: f4d4b04cea5c9f96d16039a6e7a28b81abf44df1f2396b12bdb9b30c45b61866
T07_execution_authorization_raw_SHA256: a5b6b89b8ba31f01320785caba639a36038beeab07e62267735954fcba3b6fc5
T06_final_owner_acceptance_raw_SHA256: b965211e2454762b40487fc1c80e18b7cd015c732b714fd7c23013026499b025
entry_HEAD: e1450c6390bd0630a11e8d1d4219a4228e26fd30
entry_worktree_status_paths: 131
entry_status_sha256: 9f2529492ddff5f4316a6f33a6c5f6adc09c232c714df356002c9a2bc8813ab1
entry_index_sha256: 4c53db33a3b01983526e58aba2ee11452bb064e2b20daaeeef78cab13960de8d
entry_staged_paths: 0
entry_refs_count: 31
entry_refs_sha256: 0b669899e9e6f7cdc5ebbd79a100be5fffef831dfdc382685602ffe172bb8063
entry_CURRENT_sha256: 9e5dd96da0e2c7c1d19a5c6928f5768bcb4993ab501d839135f8ac8055e438d0
entry_dirty_manifest: .local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/entry-dirty-manifest.json
entry_dirty_manifest_count: 131
entry_dirty_manifest_sha256: 1199139faff9ca34e60f198c8955bcc21816a03237f94069f325096ea48029e1
entry_snapshots: .local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/entry-files/
```

All authority identities above were recomputed from the live checkpoint bytes
before result creation and matched the authorized values. T-01 through T-06
remain COMPLETE / OWNER_ACCEPTED; T-06 was not reopened.

## T07A — source endpoint binding conformance

T-01 and T-02 now resolve the same dependent edge projection,
`DependencyRequirementV2`, requirement identity, semantic digest, and source /
successor edge tuple. Preparation scopes remain endpoint-specific and bind
only each endpoint's exact A1. Issuance checks both A1 identities through
Runtime before immutable Authorization publication; issuance creates no
Attempt. Existing pre-issued sibling authority remains valid only under its
own current binding and own endpoint availability predicates.

The public T-01/A1 claim branch uses the shared V2 Runtime lock and rechecks
its own current Preparation authority, exact expected Attempt ID, shared
requirement/binding, cancellation/tombstone/status, final governed and Attempt
reads, one atomic transition, and exact store readback. This path does not
consult admission, proof, artifact route/bytes, PL08, or successor eligibility.
The T-02 D11 branch remains intact; the full Runtime owner suite, including
the accepted T-06 regression cases, passed.

## T07B — governed byte integration and walking skeleton

`EvidenceContentInputV1` and `GovernedExecutionDependencyInputV1` are frozen,
slotted, exact two-field transient values. Completion carries producer artifact
bytes and exact-ref evidence bytes transiently. Neither value is persisted in
the ten-field `GovernedExecutionEnvelopeV1`, `bounded_payload`, nor its digest
preimage. The existing executor invocation accepts the dependency value as
one optional keyword-only argument for T-02.

Workspace owns one `publish_governed_artifact_output` operation. It derives the
existing canonical route, verifies containment and safe parent/final objects,
stages in the destination directory, installs without clobbering, independently
hashes and strictly rereads exact bytes, permits same-byte reuse, and rejects
conflicting bytes. The existing evidence-content owner remains the only
evidence publisher. Lifecycle requires exact invocation-associated Class-B
input matching; Class-A-only refs need no external bytes, and the existing
proof owner's A/B overlap equality check is unchanged.

The public positive skeleton follows the authorized order: both endpoint
Authorizations are issued while A1 is free; public T-01/A1 preparation and
claim; governed source invocation; receipt; terminal COMPLETED; one PL08
SATISFIED evaluation; artifact and Class-B evidence publication with strict
resolution; proof capture and CURRENT / Trigger A; public T-02/A1 preparation
using its pre-issued Authorization; Trigger B and immutable admission; legal
D11 claim; fresh route and raw-byte verification; typed transient input; and
the existing public successor executor invocation boundary. Instrumentation
asserts publication follows SATISFIED and verifies the exact input object and
producer bytes reach the successor boundary.

```text
walking_skeleton_test: tests/test_operation_lifecycle.py::test_public_t07_source_to_successor_bytes_use_one_satisfied_pl08_pass
PL08_evaluator_invocation_count: 1
producer_artifact_length_bytes: 26
producer_artifact_sha256: 542f6edf45cab0fb5df6413dde9c726463aec2eaa43bddc2e00645c812e02677
successor_dependency_input_raw_bytes_identical_to_producer: YES
post_claim_mutated_route_or_bytes: STOPPED_FAIL_CLOSED
post_claim_first_broken_seam: SUCCESSOR_DEPENDENCY_INPUT
post_claim_reason: DEPENDENCY_INPUT_INVALID
post_claim_successor_executor_calls: 0
post_claim_PL08_evaluator_calls: 0
post_claim_T02_attempt_state: IN_FLIGHT
post_claim_rollback: NO
post_claim_revocation: NO
post_claim_producer_rerun: NO
```

The negative case also verifies that no receipt, terminal result, observed
result, or technical evaluation is produced after invalid post-claim input; the
producer proof remains CURRENT.

## Verification

All pytest basetemp and cache paths remained under
`.local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/pytest/`.
No OS Temp was used.

| Command / evidence | Result |
| --- | --- |
| `uv sync --frozen` | PASS; 25 locked packages checked, lock unchanged |
| Six authorized owner suites: `test_dependency_admission.py`, `test_authorization.py`, `test_attempt_runtime.py`, `test_governed_executor.py`, `test_operation_lifecycle.py`, `test_workspace_registry.py` | PASS; 272 passed in 45.95s |
| Complete accepted T-06 Runtime regression | PASS; the full `tests/test_attempt_runtime.py` ran in the six-suite command |
| T-07 public walking skeleton, order, one PL08 pass, exact bytes, and post-claim negative | PASS; evidence above |
| Class-B exact match, missing, unrelated, duplicate, conflicting duplicate, Class-A-only | PASS; `test_t07_class_b_inputs_require_exact_refs_and_allow_class_a_only` |
| Workspace same-byte reuse, conflict/no-overwrite, unsafe parent, non-regular and symlink final target | PASS; workspace owner suite |
| A/B overlap byte-equality compatibility | PASS; existing dependency proof owner tests |
| `git diff --check` | PASS; whitespace clean (Git emitted only configured LF/CRLF advice) |
| Full repository suite with required in-repository basetemp | 3 unrelated fixture-context failures; all other collected tests passed |
| Post-result entry-delta / index-boundary probe: `test_entry_authority_hashes_and_write_boundary` | PASS; 1 passed, 80 deselected; result checkpoint and `CURRENT` are within the authorized governance boundary |

The three full-suite failures are limited to protected tests and share one
test-location cause. Because T-07 requires basetemp beneath this checkout's
`.local/.../pytest/`, those tests' temporary projects are descendants of the
central repository: Git root discovery therefore sees the parent checkout in
`test_non_git_snapshot_fails_closed_even_with_central_markers`, while local
template discovery sees the parent's `copier.yml` and `template` directory in
`test_default_template_source_is_the_official_repository` and
`test_configured_source_overrides_the_official_default`. No protected test,
CLI, resume helper, or template was modified. This is one non-blocking
repository-test-harness limitation, not a T-07 behavior finding.

Central template adoption / target doctor smoke was not run: this packet changes
no template or update behavior, and repository instructions require
Git-identity-dependent consumer smoke from a clean committed central source;
the checkout is dirty and the authorization forbids committing it.

## CODE_REVIEW

The review followed
`template/.planning/disciplines/CODE_REVIEW.md` Pass 1 and Pass 2 separately;
Pass 2 used `template/.planning/disciplines/CODEBASE_DESIGN.md` as the single
normative material-contract standard.

**Pass 1 — specification conformance: PASS.** The exact Definition v13, Plan
v11, and T-07 authorization were checked against endpoint projection and
issuance tests, T-01 own-authority claim tests, the unchanged complete T-06
Runtime regression, exact transient contracts, Workspace publication tests,
Class-B and overlap tests, and the instrumented public T-01-to-T-02 skeleton.
The required order, one PL08 evaluation, producer/successor byte identity,
post-claim fail-closed result, and exact twelve-path product/test boundary are
covered. No T-07 acceptance criterion is missing; no material spec finding.

**Pass 2 — standards conformance: PASS.** Runtime remains the sole Attempt
mutation owner; Authorization remains the Preparation authority owner;
Workspace remains the single artifact-route/publication owner;
`dependency_admission.py` remains the evidence/proof owner; and the existing
executor invocation seam is reused. No persisted envelope schema or digest
domain, registry, evaluator, trigger, retry, rebind, lifecycle state machine,
CLI, or template behavior was added. Source documentation explains the
projection, Preparation issuance/use, T-01 claim, transient records,
invocation seam, Workspace publisher, source publication order, and
post-claim failure contract. Exact-byte, no-clobber, safe-target, and failure
handling behavior has focused owner coverage. No material standards finding.

```text
MATERIAL_CONTRACT_DOCUMENTED: YES
CODE_REVIEW_PASS_1: PASS
CODE_REVIEW_PASS_2: PASS
MATERIAL_FINDING_COUNT: 0
NONBLOCKING_VALIDATION_FINDING_COUNT: 1
```

## Exact delta and final repository state

The exact T-07 product/test delta from the entry snapshots is these six source
and six test paths. Raw entry and result bytes are recorded for independent
comparison:

| Authorized path | Entry raw SHA-256 | Result raw SHA-256 |
| --- | --- | --- |
| `src/planning_lite/attempt_runtime.py` | `0c5c1926c87b122829fcd44c493bacf9f263b13fb919c5ec663e355818855e18` | `a54505f4233636e1df7c3ac96605748689ef8a406217cf5980de97655352cf53` |
| `src/planning_lite/authorization.py` | `989d94a5e62cffe6abbb93d85294e5924bbf890ce9c3a96f39a622f44370ccaf` | `df9f55b11bc16163b6a03e4771a51ae2c1682c66cc70fa9347941bbdd1d4c4c6` |
| `src/planning_lite/dependency_admission.py` | `bc0f792ccb768c67793f0f5449f661bacae7f491589a44bfea63974d6c2ad824` | `f1b6036eda0284a0192c6a94cb2464c359b0a918278494d0286b3ee5ddbf3369` |
| `src/planning_lite/governed_executor.py` | `53f3cb536bb1dc6cd4bf08993f21693f364e94b3f942d7c76c52ebea4d34b087` | `607a3b4d3ae91009763dc3f613f0c4ffce2f2c745ba20254c09788156c465642` |
| `src/planning_lite/operation_lifecycle.py` | `8c70a2560a7052c3cc2b0eaa94b0e079f4371c83bcf4b71633e7ffe761219786` | `58c76ae6c0ae57bd562964f6c1cf7bf300bd7d64cf93868f3e3903cc747c0ee9` |
| `src/planning_lite/workspace.py` | `8085cf9ef52caaa24788f2eef835f83377eeb1c3817fa2251b349a935efd9781` | `33d9d9b9a55da173e75ba4db9b61385c113d5f4d13d8abde83b519d18b122a46` |
| `tests/test_attempt_runtime.py` | `2f48bdf41073a90114ab694c58f2b852a3b189836bf1877ca9206b0b3731488c` | `c062c29ac6d389bfd0170b2e85e5ba9d927062f7c65db43b877cd9663e5be9ca` |
| `tests/test_authorization.py` | `cc510ae07198b3f76ba3cc5e00d1d3873da76388490eea2fe79a73ed413f4357` | `a2eb1f30463cf49ee1d33967f02d552867204a0225569e3c543ee51034ab894e` |
| `tests/test_dependency_admission.py` | `f843686c09126fc9c5c5c6ebf9645cbc2222cfb673c764bfa7d8af6372fde5f6` | `76e791e81fb2e0d221cae6426c3ee58de89a808bf234cdf07e8ecf01b003c882` |
| `tests/test_governed_executor.py` | `254e8ab3cbf7e229d899916b03c72e79e5128402a5a907159a9d249d7cfee6d3` | `c858b55c7e724aab67225f2fe2dfa1161788cdfe2d4599e8ef8ea876a03adc41` |
| `tests/test_operation_lifecycle.py` | `735cbea47d195c51990941699550dc6d792d1f5ca6da2a062cf1615183809a15` | `9a23e7b25ce16cc8abbc8e4851ee2facbd8db18384c27cc45cd6b2cf86055c2b` |
| `tests/test_workspace_registry.py` | `61c2dc3fcfac26ea9e25f29312b635ccabfe73852c6a4c9e3ba24e5d67fc8dbf` | `4d0a2eb6efd908cd6d39bb801b04c9950e91fe3fcb31a44f544854bef4076af2` |

Before the result/CURRENT writes, the only newly dirty paths relative to the
entry status were `src/planning_lite/governed_executor.py` and
`tests/test_governed_executor.py`; both are authorized. Every pre-existing
dirty-manifest entry outside the twelve authorized product/test paths and
`CURRENT.md` retained its entry bytes. Pre-existing dirt inside the authorized
paths was changed only within T-07 scope. No other product/test path changed.
This checkpoint and the corresponding `CURRENT.md` transition are the only
governance evidence writes for T-07.

```text
final_HEAD: e1450c6390bd0630a11e8d1d4219a4228e26fd30 / unchanged
final_index_sha256: 4c53db33a3b01983526e58aba2ee11452bb064e2b20daaeeef78cab13960de8d / unchanged
final_staged_paths: 0
final_refs_count: 31
final_refs_sha256: 0b669899e9e6f7cdc5ebbd79a100be5fffef831dfdc382685602ffe172bb8063 / identical entry set and bytes
HEAD_changed: NO
index_changed: NO
refs_intentionally_mutated: NO
staged: NO
committed: NO
pushed: NO
unrelated_entry_dirty_bytes_changed: 0
```

```text
OVERALL: PASS_WITH_NONBLOCKING_REPOSITORY_TEST_HARNESS_LIMIT
T07A: PASS
T07B: PASS
T07_COMPLETE_CANDIDATE: YES
T07_PUBLIC_WALKING_SKELETON: PASS
T06_REGRESSION_REVALIDATION: PASS
PL08_EVALUATOR_CALL_COUNT: 1
PRODUCER_SUCCESSOR_BYTE_IDENTITY: YES
POST_CLAIM_FAIL_CLOSED: PASS
MATERIAL_CONTRACT_DOCUMENTED: YES
CODE_REVIEW_PASS_1: PASS
CODE_REVIEW_PASS_2: PASS
AUTHORIZED_PRODUCT_TEST_PATHS_ONLY: YES / EXACTLY 6 SOURCE + 6 TEST
UNRELATED_DIRT_PRESERVED: YES
HEAD_CHANGED: NO
INDEX_CHANGED: NO
STAGED: NO
COMMITTED: NO
PUSHED: NO
OPEN_MATERIAL_FINDING_COUNT: 0
FIRST_BROKEN_SEAM: NONE_IN_T07
T08_T09_AUTHORIZED: NO
NEXT_SINGLE_GATE: OWNER_ADJUDICATION_09G_DEPENDENCY_ADMISSION_T07_EXECUTION_RESULT
```
