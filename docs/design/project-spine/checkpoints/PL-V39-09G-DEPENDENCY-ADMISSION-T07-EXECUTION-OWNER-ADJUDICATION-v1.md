# PL-V39-09G Dependency Admission T-07 Execution Owner Adjudication v1

## Owner decision

OWNER_T07_DECISION: DO_NOT_ACCEPT_T07_PENDING_CONTROLLED_CAUSALITY_EVIDENCE
T07_COMPLETE: NO
T07A: PASS
T07B: PASS
T08_T09_AUTHORIZED: NO
IMPLEMENTATION_AUTHORIZED: NO
FIRST_BROKEN_SEAM: CONTROLLED_PARENT_CHECKOUT_ISOLATION_FOR_TEMPLATE_SOURCE_TESTS
MATERIAL_FINDING_COUNT: 1
NONBLOCKING_FINDING_COUNT: 1
T07_PRODUCT_DEFECT_FINDING_COUNT: 0
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_09G_DEPENDENCY_ADMISSION_T07_TEMPLATE_DISCOVERY_ISOLATION_DIAGNOSTIC

This is the final owner adjudication of the exact completed T-07 candidate
identified below. T-07A, T-07B, the accepted T-06 regression, the walking
skeleton, the twelve-path candidate, and the source/test hygiene evidence
were rechecked. T-07 is not accepted because the mandated controlled
parent-discovery comparison has not been completed for two protected
template-source failures. No product or test correction is authorized or
performed. This decision does not start T-08 or T-09.

## Exact authority and result identity

~~~text
repository: D:\documents\planning-lite
branch: reconcile/current-design-spine-2026-08-25
HEAD: e1450c6390bd0630a11e8d1d4219a4228e26fd30
active_change: CHG-PL-V39-09G-DEPENDENCY-ADMISSION-001
CURRENT_at_adjudication_entry_raw_sha256: 001bb513a30a0acd71b66dc7387be1966fe842a33e57aece867a1d662f0cd121
CURRENT_expected_next_gate_at_entry: OWNER_ADJUDICATION_09G_DEPENDENCY_ADMISSION_T07_EXECUTION_RESULT
Definition_v13: APPROVED / CURRENT / 3cede7673670a7f1b91ff20b6e914461855266afac04e8a5893abc0a3856fc46
Definition_v13_owner_approval: docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-CHANGE-DEFINITION-V13-OWNER-ADJUDICATION-v1.md / e17019184fcd141a95911eda374ec31bd2ddbc7f0527c2a2c69266c233dd5e47
Plan_v11: APPROVED / CURRENT / d0a6e425009c8254bbe79d229fa8a79dbe0407f8882ebdd60e9e856812203685
Plan_v11_owner_approval: docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-IMPLEMENTATION-PLAN-V11-OWNER-REVIEW-v1.md / 502f36a83acbc401d2e03ebf03e54395b11915cdc7baabdc90e038ec0e716a7a
T07_Formal_Readiness_v2: READY / f4d4b04cea5c9f96d16039a6e7a28b81abf44df1f2396b12bdb9b30c45b61866
T07_execution_authorization: docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-T07-EXECUTION-AUTHORIZATION-v1.md / a5b6b89b8ba31f01320785caba639a36038beeab07e62267735954fcba3b6fc5
T06_final_owner_acceptance: docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-T06-FINAL-OWNER-ACCEPTANCE-v1.md / b965211e2454762b40487fc1c80e18b7cd015c732b714fd7c23013026499b025
T07_execution_result: docs/design/project-spine/checkpoints/PL-V39-09G-DEPENDENCY-ADMISSION-T07-EXECUTION-RESULT-v1.md
T07_execution_result_raw_sha256_before_adjudication: 49ae76475801852707a86458c4b3d028a95fb7ceaf77e4d740a964f47ab1f01b
result_claims: T07A PASS / T07B PASS / T07_COMPLETE_CANDIDATE YES / owner acceptance pending
~~~

The live CURRENT resume contract named this owner gate. The raw execution
checkpoint digest was recomputed before substantive review and matched the
digest embedded in CURRENT. Its bytes were checked again before this
adjudication checkpoint was written.

## The three full-repository failures

The execution packet reported three failures under its required in-checkout
pytest basetemp. I independently reran exactly those three protected nodes
under the same in-checkout condition. They failed again with the following
assertions and discovery paths.

| Exact test node | Exact assertion and observed error | First relevant frame | Actual T-07 full-suite fixture |
| --- | --- | --- | --- |
| tests/test_central_resume_contract.py::test_non_git_snapshot_fails_closed_even_with_central_markers | Line 90 expected NOT A VERIFIED CENTRAL GIT CHECKOUT in stderr. Actual stderr: Planning Lite resume: BLOCKED; Helper location is not the Git root scripts directory: resolved D:\documents\planning-lite | tests/test_central_resume_contract.py:90; scripts/maintainer_resume.py main, lines 177-182, resolves helper path and compares it with Git root | .local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/pytest/full-tmp/test_non_git_snapshot_fails_cl0/planning-lite |
| tests/test_template_source.py::test_default_template_source_is_the_official_repository | Line 37 expected https://github.com/yegor-vynokurov/planning-lite; observed D:\documents\planning-lite | tests/test_template_source.py:37; planning_lite.cli._discover_template_source scans resolved cwd and ancestors before config/default resolution | .local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/pytest/full-tmp/test_default_template_source_i0/ordinary-project |
| tests/test_template_source.py::test_configured_source_overrides_the_official_default | Line 102 expected https://example.invalid/from-config; observed D:\documents\planning-lite | tests/test_template_source.py:102; planning_lite.cli._discover_template_source scans resolved cwd and ancestors before loading configured source | .local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/pytest/full-tmp/test_configured_source_overrid0/ordinary-project |

The same three nodes were independently reproduced under
.local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/pytest/owner-adjudication-parent.
The resume fixture has no .git directory. Nevertheless
git -C <fixture>/planning-lite rev-parse --show-toplevel returned
D:/documents/planning-lite. The copied maintainer_resume.py derives its script
root from Path(__file__).resolve().parents[1], then resolve_git_root invokes
git -C on that location; Git discovers the enclosing checkout and main reports
the helper-location mismatch before the intended no-Git-checkout diagnostic.

For both template fixtures, Path.cwd().resolve() was beneath
D:\documents\planning-lite and its parents included that checkout. The
checkout's copier.yml exists and its template directory exists. The unchanged
cli._looks_like_template_repo predicate therefore returns the enclosing
checkout before the tests reach their user-config or official-fallback
expectations. This is a filesystem marker scan; it does not use Git discovery.

For every failure, the T-07 code causal-path review is:

~~~text
T07_CHANGED_CODE_ON_FAILURE_PATH: NO
SAME_FAILURE_MECHANISM_EXISTS_INDEPENDENT_OF_T07_SEMANTIC_CHANGES: YES
PROTECTED_FAILING_TEST_UNCHANGED_BY_T07: YES
ACCEPTING_T07_WOULD_CONCEAL_A_T07_PRODUCT_REGRESSION: NO_T07_CODE_PATH_FOUND
~~~

The first test executes the protected maintainer-resume helper and Git, not
the changed Planning Lite runtime symbols. The other two fail inside the
unchanged cli._discover_template_source and _looks_like_template_repo path;
the changed Workspace publisher is never reached, and no changed T-07 callable
is invoked before the assertion. This conclusion is based on the actual
discovery call paths, not merely on those test files being outside the
authorized surface. It does not waive the controlled-diagnostic requirement.

## Controlled causality diagnostic

With the parent checkout visible, all three exact nodes reproduced. For the
Git-root case, I mapped X: to the already-authorized repository-local T-07
scratch root and set GIT_CEILING_DIRECTORIES=X:\. The same protected
test node then passed: the fixture no longer resolved to the parent Git
checkout, and the helper produced the expected fail-closed outcome. The
candidate source and test bytes remained identical to the execution-result
hashes.

The same boundary did not isolate the two template-source tests. Both still
failed, because cli._discover_template_source calls Path.cwd().resolve();
Windows resolved the X: path back to D:\documents\planning-lite before
walking parent directories. GIT_CEILING_DIRECTORIES affects Git discovery and
cannot hide copier.yml or template from this filesystem scan. Thus the
controlled comparison proves disappearance for the Git-root failure only;
it does not show whether the two template failures disappear when the parent
checkout is actually absent from the resolved filesystem ancestry.

The T-07 execution authorization limits pytest basetemp to
.local/work/experiments/PL_V39_09G_DEPENDENCY_ADMISSION_T07_EXECUTION/pytest/
and states that no OS Temp is authorized. A physical basetemp outside the
checkout is required to isolate the template scanner without changing code,
tests, or candidate bytes. No separate authorization extends the scratch
boundary for this owner diagnostic. In accordance with that policy, I did not
use an external basetemp, monkeypatch discovery, edit tests, or alter
production code.

~~~text
PARENT_GIT_ROOT_DISCOVERY: PROVEN
PARENT_TEMPLATE_MARKER_DISCOVERY: PROVEN
GIT_FAILURE_CONTROLLED_DISAPPEARANCE: YES
TEMPLATE_FAILURE_CONTROLLED_DISAPPEARANCE: NOT_TESTED / REQUIRED_BOUNDARY_UNAVAILABLE
HARNESS_LIMIT_CAUSALITY_PROVEN_FOR_ALL_THREE: NO
T07_CAUSAL_FAILURE_COUNT: 0_CONFIRMED
UNRESOLVED_CONTROLLED_FAILURE_COUNT: 2
~~~

## Independent T-07 completion evidence

The six exact authorized owner suites were rerun after the candidate and
completed with 272 passed in 47.82s. The complete tests/test_attempt_runtime.py
suite ran in this command, including the accepted T-06 Runtime regression
cases. D11 predicates 1-6 remain covered; the existing
_dependent_claim_artifact_digest_locked, _dependent_claim_evidence_locked,
and _proof_blob_locked function bodies are byte-for-byte unchanged from the
T-07 entry snapshots. The six-suite run passed without weakening the accepted
T-02 claim contract.

T-07A is supported by the live dependency and authorization tests. T-01 and
T-02 resolve equal dependency requirements, requirement IDs, projections,
and semantic digests. Their Preparation scopes retain distinct exact
T-01/A1 and T-02/A1 identities. Both public endpoint Authorizations are
issued before either A1 exists. After T-01/A1 materializes, the pre-issued
T-02 sibling remains usable, while a new dependent Authorization is refused.
T-01 has a separate source-edge-member claim using its own current V2
Preparation authority and exact T-01/A1 binding. Its locked evidence path
does not read proof, admission, artifact route or bytes, PL08, or successor
eligibility. T-02 keeps its accepted D11 direct claim and all six predicates.

T-07B's tests assert that EvidenceContentInputV1 has exactly
evidence_ref and exact_raw_bytes, and
GovernedExecutionDependencyInputV1 has exactly
required_input_logical_ref and exact_raw_bytes. These are transient values:
the persisted execution envelope remains ten fields, dependency input is
T-02-only, and byte forwarding does not alter the envelope. Workspace remains
the single artifact-route owner and publisher;
dependency_admission remains the existing Class-B evidence owner. The
lifecycle uses its existing executor invocation and evaluator; no second
evaluator is added.

The public walking skeleton
tests/test_operation_lifecycle.py::test_public_t07_source_to_successor_bytes_use_one_satisfied_pl08_pass
uses public T-01 and T-02 preparation and claim paths. It observes receipt,
COMPLETED terminalization, one PL08 SATISFIED evaluation, then artifact and
Class-B publication, then proof capture and CURRENT. It resolves the T-02
route and raw bytes after legal claim and verifies exact byte identity at the
successor invocation. The post-claim mutation negative returns
STOPPED_FAIL_CLOSED at SUCCESSOR_DEPENDENCY_INPUT with
DEPENDENCY_INPUT_INVALID, makes no successor executor or evaluator call,
leaves T-02 IN_FLIGHT and the source proof CURRENT, and creates no terminal,
receipt, observed-result, or evaluation record.

The execution checkpoint's CODE_REVIEW Pass 1 (specification conformance)
and Pass 2 (CODEBASE_DESIGN standards conformance) both report PASS and zero
material code-contract findings. I checked the live exact transient types,
source-claim boundary, artifact publisher, lifecycle ordering and owner tests;
MATERIAL_CONTRACT_DOCUMENTED: YES is substantiated by the semantic code
contracts and the execution order/negative-path tests, not by docstring
presence alone.

~~~text
TARGET_SUITES: PASS / 272
T06_REGRESSION_REVALIDATION: PASS / full tests/test_attempt_runtime.py
PUBLIC_WALKING_SKELETON: PASS
PL08_EVALUATOR_CALL_COUNT: 1
PRODUCER_SUCCESSOR_BYTE_IDENTITY: YES
POST_CLAIM_FAIL_CLOSED: PASS
MATERIAL_CONTRACT_DOCUMENTED: YES
CODE_REVIEW_PASS_1: PASS
CODE_REVIEW_PASS_2: PASS
~~~

## Exact candidate delta and hygiene

Each of the exact twelve authorized product/test paths was compared with its
T-07 entry snapshot and with the current hash recorded in the execution
checkpoint. All twelve current raw SHA-256 values match the execution
checkpoint:

| Exact authorized path | Current candidate raw SHA-256 |
| --- | --- |
| src/planning_lite/attempt_runtime.py | a54505f4233636e1df7c3ac96605748689ef8a406217cf5980de97655352cf53 |
| src/planning_lite/authorization.py | df9f55b11bc16163b6a03e4771a51ae2c1682c66cc70fa9347941bbdd1d4c4c6 |
| src/planning_lite/dependency_admission.py | f1b6036eda0284a0192c6a94cb2464c359b0a918278494d0286b3ee5ddbf3369 |
| src/planning_lite/governed_executor.py | 607a3b4d3ae91009763dc3f613f0c4ffce2f2c745ba20254c09788156c465642 |
| src/planning_lite/operation_lifecycle.py | 58c76ae6c0ae57bd562964f6c1cf7bf300bd7d64cf93868f3e3903cc747c0ee9 |
| src/planning_lite/workspace.py | 33d9d9b9a55da173e75ba4db9b61385c113d5f4d13d8abde83b519d18b122a46 |
| tests/test_attempt_runtime.py | c062c29ac6d389bfd0170b2e85e5ba9d927062f7c65db43b877cd9663e5be9ca |
| tests/test_authorization.py | a2eb1f30463cf49ee1d33967f02d552867204a0225569e3c543ee51034ab894e |
| tests/test_dependency_admission.py | 76e791e81fb2e0d221cae6426c3ee58de89a808bf234cdf07e8ecf01b003c882 |
| tests/test_governed_executor.py | c858b55c7e724aab67225f2fe2dfa1161788cdfe2d4599e8ef8ea876a03adc41 |
| tests/test_operation_lifecycle.py | 9a23e7b25ce16cc8abbc8e4851ee2facbd8db18384c27cc45cd6b2cf86055c2b |
| tests/test_workspace_registry.py | 4d0a2eb6efd908cd6d39bb801b04c9950e91fe3fcb31a44f544854bef4076af2 |

No seventh product or test path changed since the T-07 entry snapshot.
Protected CLI, evaluator, maintainer-resume, and template-source paths
remain equal to HEAD bytes. Protected traversal tests and other pre-existing
dirty paths remain equal to their entry snapshots. All 131 pre-existing dirty-manifest
entries outside the twelve authorized paths and CURRENT retain their entry
bytes. The only governance writes for this owner gate are this checkpoint and
the corresponding CURRENT transition. Test artifacts remained in the
authorized repository-local T-07 pytest scratch.

~~~text
git diff --check: PASS / only configured LF-CRLF advice
HEAD: e1450c6390bd0630a11e8d1d4219a4228e26fd30 / unchanged
index_sha256: 4c53db33a3b01983526e58aba2ee11452bb064e2b20daaeeef78cab13960de8d / unchanged
staged_path_count: 0
committed: NO
pushed: NO
branch_head_release_tag_remote_refs: unchanged
codex_turn_diff_ref_pair_count: 2 rotated relative to execution entry
~~~

A read-only ref-map comparison found 31 entries, matching the execution-entry
count. The only ref-name replacements were two pairs in refs/codex/turn-diffs
(one capture and one checkpoint); all shared ref names retained their object
IDs, and branch, HEAD, release-tag, and remote-tracking refs matched the
execution-entry snapshot. These Codex capture/checkpoint refs rotate as later
turn/tool snapshots are recorded, so their generated names and object IDs are
transient. This audit issued no Git ref-update command and did not alter or
delete the refs. This is one nonblocking host-tooling observation, not T-07
product delta. No ref cleanup was attempted.

## Findings and next gate

F01 is one material, blocking verification-coverage/environment finding:
the two template-source failures are directly explained by the enclosing
checkout marker scan and no T-07 code path is involved, but the mandated
parent-absent controlled comparison has not been run. The first broken seam
is controlled isolation for cli._discover_template_source's filesystem
ancestor scan. There is no proven T-07 product defect, and no corrective
implementation is opened.

The one nonblocking hygiene observation is the two rotating
refs/codex/turn-diffs entries described above. No user branch, release tag,
remote reference, index entry, or candidate path changed by this gate.

The smallest next owner decision is whether to authorize one isolated
diagnostic for only the two unchanged template-source nodes using a physical
pytest basetemp outside the enclosing checkout, or to approve another
non-mutating isolation mechanism that actually prevents Path.resolve parent
discovery. That next decision grants no product/test write authority and no
T-08/T-09 authority. Once evidence is available, rerun owner adjudication
against the same execution-result hash and twelve candidate hashes.

~~~text
OVERALL: DO_NOT_ACCEPT / CONTROLLED_CAUSALITY_EVIDENCE_INCOMPLETE
OWNER_T07_DECISION: DO_NOT_ACCEPT_T07_PENDING_CONTROLLED_CAUSALITY_EVIDENCE
T07_COMPLETE: NO
T07A: PASS
T07B: PASS
TARGET_SUITES: PASS / 272 passed in 47.82s
T06_REGRESSION_REVALIDATION: PASS / full Runtime suite
PUBLIC_WALKING_SKELETON: PASS
PL08_EVALUATOR_CALL_COUNT: 1
PRODUCER_SUCCESSOR_BYTE_IDENTITY: YES
POST_CLAIM_FAIL_CLOSED: PASS
FULL_REPOSITORY_SUITE: FAIL / three protected test-context failures; not a pass
FULL_SUITE_FAILURE_COUNT: 3
HARNESS_LIMIT_CAUSALITY_PROVEN: NO / one controlled Git failure; two template failures unresolved
T07_CAUSAL_FAILURE_COUNT: 0 confirmed
MATERIAL_CONTRACT_DOCUMENTED: YES
CODE_REVIEW_PASS_1: PASS
CODE_REVIEW_PASS_2: PASS
AUTHORIZED_PRODUCT_TEST_PATHS_ONLY: YES / exactly six source plus six test
OPEN_MATERIAL_FINDING_COUNT: 1
OPEN_NONBLOCKING_FINDING_COUNT: 1
FIRST_BROKEN_SEAM: CONTROLLED_PARENT_CHECKOUT_ISOLATION_FOR_TEMPLATE_SOURCE_TESTS
T08_T09_AUTHORIZED: NO
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_09G_DEPENDENCY_ADMISSION_T07_TEMPLATE_DISCOVERY_ISOLATION_DIAGNOSTIC
~~~
