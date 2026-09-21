# PL-V39-09 Authoritative Attempt Action Authorization - Implementation Plan v1

Status: PLAN_APPROVED / FORMAL_READINESS_NOT_YET_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED

This canonical Implementation Plan checkpoint materializes the owner-approved,
freshly reviewed V2 Plan candidate. It is Plan authority and evidence only.
It does not authorize Formal Readiness, implementation, Attempt Runtime work,
executor work, lifecycle resumption, Change-2/Change-3 work, staging, commit,
push, or release.

~~~text
OWNER_DECISION: APPROVE_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_IMPLEMENTATION_PLAN
CANONICALIZATION: CANONICAL_PLAN_CREATED
PLAN_STATUS: PLAN_APPROVED
FORMAL_READINESS_STATUS: NOT_YET_AUTHORIZED
IMPLEMENTATION_AUTHORIZED: NO
SEMANTIC_DRIFT: NO
~~~

## Canonical checkpoint lineage

~~~text
CANONICAL_PLAN_PATH: docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-IMPLEMENTATION-PLAN-v1.md
APPROVED_SOURCE_PLAN_PATH: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_IMPLEMENTATION_PLAN_CANDIDATE_CORRECTED_V2.md
APPROVED_SOURCE_PLAN_SHA256: 4E432C183A979539EE5E3CD8490A85B7AEF4FF511BE0A98CE124EF33FFFBBD48
CANONICAL_DEFINITION_PATH: docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-CHANGE-DEFINITION-v1.md
CANONICAL_DEFINITION_SHA256: BAD0445F477F99D110525D3ADFAE03E3C2CFE935B84CD2A46707A6F3E4C774CC
DEFINITION_ACTIVATION_PATH: docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-DEFINITION-ACTIVATION-v1.md
DEFINITION_ACTIVATION_SHA256: CDB559DA4459B5535B8310602F1FA4F9060977ADADABF9F59929B5BADDD0D01F
APPROVING_FRESH_REVIEW_PATH: .local/work/experiments/PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_SECOND_CORRECTED_IMPLEMENTATION_PLAN_FRESH_REVIEW.md
APPROVING_FRESH_REVIEW_SHA256: B68963A0F6EEDCE5DB06ED4B8003B06D62B1BED7219BF5CA35CE10402908BADA
APPROVING_FRESH_REVIEW_VERDICT: PASS
SEMANTIC_DELTA_FROM_APPROVED_PLAN: NONE
CANONICALIZATION_DELTA: HEADER_STATUS_PATH_LINEAGE_AND_RECEIPT_METADATA_ONLY
BASELINE_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
NEXT_SINGLE_GATE: FORMAL_READINESS_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION
~~~

## 1. Plan identity and exact authority

~~~text
CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-001
PLAN_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-001-IMPLEMENTATION-PLAN-V1
PLAN_STATUS: PLAN_APPROVED
PLANNING_AUTHORIZED: YES
FORMAL_READINESS_AUTHORIZED: NO
IMPLEMENTATION_AUTHORIZED: NO
~~~

The canonical Plan preserves the approved V2 candidate semantics below without
reinterpretation. A changed Definition, source-candidate, or approving-review
digest invalidates this checkpoint and requires a new owner gate.

## Frozen authority topology

```text
AUTHORIZATION_OWNER_PATH: src/planning_lite/authorization.py
AUTHORIZATION_STORE_LOCATION: <target>/<effective planning_root>/project/authorizations/
SELECTED_STORAGE_MECHANISM: ONE_IMMUTABLE_CANONICAL_JSON_FILE_PER_AUTHORIZATION
AUTHORITATIVE_AUTHORIZATION_STORE_COUNT: 1
PRODUCTION_ISSUER_PREPARATION: planning-lite authorize-preparation TARGET --change-id CHANGE_ID --task-or-operation-id TASK_OR_OPERATION_ID --decision-provenance-ref REF
PRODUCTION_ISSUER_RECOVERY: planning-lite authorize-recovery TARGET --attempt-id ATTEMPT_ID --decision-provenance-ref REF
RESOLVER_SYMBOL: planning_lite.authorization::resolve_authorization
PREPARATION_VALIDATOR_SYMBOL: planning_lite.authorization::validate_preparation_applicability
RECOVERY_VALIDATOR_SYMBOL: planning_lite.authorization::validate_recovery_applicability
SCOPE_COMPARISON: EXACT_STRING_EQUALITY_AFTER_CANONICAL_STRUCTURAL_VALIDATION
TASK_ID_DRIFT: NO
TASK_SEMANTIC_DRIFT: NO
VERIFICATION_ID_DRIFT: NO
VERIFICATION_SEMANTIC_DRIFT: NO
```

## ENTRY GIT STATE

```text
BASELINE_HEAD: 3a066d248e117052397dfb7a33327fcdc41f66d5
PRE_EXISTING_DIRT: PRESERVE_EXACTLY
INDEX: EMPTY
SOURCE_MUTATIONS_BY_THIS_CORRECTION: 0
STAGED_PATHS_BY_THIS_CORRECTION: 0
```

The modified `docs/design/project-spine/CURRENT.md` and the pre-existing
untracked design-spine checkpoint files remain untouched user-owned dirt.

## DEFINITION FIDELITY AND PRESERVED ARCHITECTURE

```text
DEFINITION_FIDELITY: PASS
TRUST_ROOT: TRUSTED_LOCAL_OWNER_CONTROL_PLANE
OWNER_DECISION_EVENT: EXPLICIT_LOCAL_CONTROL_PLANE_ISSUANCE
MACHINE_AUTHORIZATION_RECORD_AUTHORITY: PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_AUTHORITY
SUPPORTED_ACTION_TYPE_COUNT: 2
AUTHORIZATION_RECORD_MUTABILITY: IMMUTABLE
REVOCATION_REQUIRED_IN_V1: NO
AUTHORIZATION_USE_ENFORCEMENT_OWNER: PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_AUTHORITY
CROSS_STORE_ATOMIC_TRANSACTION_REQUIRED: NO
ATTEMPT_RUNTIME_IMPLEMENTATION_INCLUDED: NO
ATTEMPT_RUNTIME_INDEPENDENT_CLOSURE_PLAN: PASS
EXECUTOR_DEPENDENCY: NO
LIFECYCLE_DEPENDENCY: NO
PL08_RUNTIME_ORCHESTRATION_CREATED: NO
DEFINITION_AMENDMENT_REQUIRED: NO
PLAN_ARCHITECTURE_STOP: NO
PLAN_ARCHITECTURE_REOPEN_REQUIRED: NO
```

The already-closed canonical JSON, duplicate handling, collision budget,
identifier semantics, file-per-authorization store, two explicit CLI issuers,
shared resolver, two validators, immutable/no-consumption source, and
Attempt-Runtime-independent boundary are carried forward unchanged.

## AUTHORITATIVE STORE AND AUTHORIZATION OWNER

`src/planning_lite/authorization.py` remains the sole authorization owner. It
owns typed records, strict codec, effective-root store discovery, opaque ref
allocation, immutable publication, resolver, and exact applicability.

The authoritative location is exactly:

```text
AUTHORIZATION_STORE_ROOT_POLICY: EFFECTIVE_ROOT
AUTHORIZATION_STORE_LOCATION: <target>/<effective planning_root>/project/authorizations/
RECORD_FILENAME: <authorization_ref>.json
RECORD_ENUMERATION: *.json EXCLUDING TEMPORARY FILES
AUTHORITATIVE_SOURCE_COUNT: 1
```

No fixed `.planning` fallback, CURRENT/ACTIVE/local artifact, Git history,
prose, Attempt state, or alternate source is consulted.

## CLOSED JSON, REF, AND IDENTIFIER CONTRACTS

These bindings are preserved exactly and are not reopened:

```text
JSON_ENCODING: UTF-8
JSON_SORT_KEYS: YES
JSON_ENSURE_ASCII: NO
JSON_SEPARATORS: (",", ":")
JSON_INDENT: NONE
JSON_TRAILING_NEWLINE: EXACTLY_ONE_LF
DUPLICATE_JSON_MEMBER_REJECTION: REQUIRED
DUPLICATE_MEMBER_SCOPE: ALL_OBJECT_LEVELS
NONCANONICAL_BYTE_TREATMENT: REJECT_IF_RAW_BYTES_DIFFER_FROM_VALIDATED_CANONICAL_REENCODING
CANONICAL_ROUND_TRIP: RAW_BYTES -> STRICT_DECODE -> VALIDATED_RECORD -> CANONICAL_ENCODE -> EXACT_RAW_BYTE_EQUALITY
AUTHORIZATION_REF_FORMAT: authz_[0-9a-f]{32}
AUTHORIZATION_REF_MAX_ALLOCATION_ATTEMPTS: 16
COLLISION_EXHAUSTION_OUTCOME: AUTHORIZATION_REF_ALLOCATION_EXHAUSTED
```

All identifiers require string, nonempty, `value == value.strip()`, and no
CR/LF; accepted values are preserved exactly. No casefolding, lowercasing,
Unicode normalization, separator rewriting, Attempt-ID parsing, or provenance
prose dereference is permitted. Applicability uses exact case-sensitive string
equality after structural validation.

## MF2-01 EFFECTIVE-ROOT LITERAL-PATH CONTRACT

```text
EFFECTIVE_ROOT_POLICY: EFFECTIVE_ROOT
LITERAL_PATH_INVARIANT: EFFECTIVE_PLANNING_ROOT_IS_A_LITERAL_FILESYSTEM_PATH_NOT_A_GLOB_PATTERN
DYNAMIC_OWNERSHIP_SCOPE: EXACT_EFFECTIVE_ROOT_PROJECT_SUBTREE
GLOB_SYNTHESIS_FROM_EFFECTIVE_ROOT: FORBIDDEN
LITERAL_SAFE_OWNERSHIP_MECHANISM: SEPARATE_LITERAL_PROJECT_ROOTS_PLUS_PATH_EQUALITY_OR_IS_RELATIVE_TO
```

The dynamic boundary is the literal repository-relative path
`<effective planning_root>/project`. It owns exactly that directory and its
descendants. It does not own the parent, framework subtree, sibling roots, or
other descendants of the effective root. The implementation must never create
`f"{planning_root}/project/**"` or pass any root-derived string to a glob
matcher.

## LITERAL-SAFE OWNERSHIP IMPLEMENTATION

`src/planning_lite/local_update.py` remains the sole mechanical path. Add a
separate optional keyword `literal_project_owned_roots` to the ownership
classification/planning/apply flow (`classify_path`, candidate classification,
`build_local_update_plan`, project-owned hashing, and `apply_local_update_plan`)
with an empty tuple default.

`_command_local_only_update` obtains the validated
`project_policy["planning_root"]` from `load_effective_policy(target)`, joins
the literal `project` component, and passes that one repository-relative Path
boundary to both plan construction and apply. It is never merged into the
static `OwnershipPolicy.project_owned` glob tuple.

Dynamic classification is true only when the normalized candidate path is
exactly the boundary or `candidate.is_relative_to(boundary)`. Static manifest
matching remains `fnmatchcase`-based and unchanged.

## PATH NORMALIZATION / CONTAINMENT

```text
PATH_NORMALIZATION_RULE: REPOSITORY_RELATIVE_SEPARATOR_NORMALIZATION_THEN_HOST_PATH_EQUALITY_OR_IS_RELATIVE_TO_WITH_ABSOLUTE_AND_DOTDOT_REJECTION_NO_RESOLVE
```

The exact algorithm is:

1. accept repository-relative paths only;
2. apply the existing slash normalization (`\\` to `/`, remove leading `./`);
3. construct the host-native relative `Path`, collapsing redundant separators
   and `.` components;
4. reject absolute paths and any `..` component;
5. compare Path objects by equality or `is_relative_to`; and
6. never call `resolve`, dereference symlinks, casefold manually, or Unicode-
   normalize for ownership classification.

`workspace._relative_root` already validates target containment and emits a
repository-relative POSIX value. `iter_files` already emits repository-relative
POSIX paths. Host-native Path comparison therefore preserves case-sensitive
POSIX and Windows-flavour case-insensitive behavior without a second policy
authority.

## OWNERSHIP PRECEDENCE

```text
OWNERSHIP_PRECEDENCE: INSTALLER_METADATA_THEN_HIGHEST_EXISTING_SPECIFICITY_ACROSS_STATIC_MATCHES_AND_LITERAL_DYNAMIC_PROJECT_SUBTREE_WITH_CROSS_CLASS_TIES_FAIL_CLOSED
```

Installer metadata always wins. Existing static matches retain
`_pattern_specificity`. A dynamic literal match contributes a project-owned
specificity rank equal to a descendant-subtree rule at its boundary,
`(0, -2, len(boundary.as_posix()) + 3)`, computed numerically without building
or evaluating a glob. The highest specificity wins; exact/narrower explicit
framework rules beat the dynamic match, while a broad containing managed glob
loses to the deeper dynamic project subtree. Equal cross-class specificity is
an ambiguity and fails closed.

## METACHARACTER AND BOUNDEDNESS TEST MATRIX

`tests/test_local_only_update.py` must cover:

```text
ROOTS: .planning; managed-planning; managed[1]-planning; star*root; query?root
POSITIVE: exact <root>/project and descendant <root>/project/authorizations/x.json
NEGATIVE: <root>-other/project/x; glob-lookalike siblings; parent; framework; other subtrees
NORMALIZATION: slash/backslash, redundant separators, '.', absolute, '..'
PRECEDENCE: broad managed glob, exact/narrow managed rule, installer metadata, cross-class tie
```

`*` and `?` are tested structurally because they are accepted by the current
policy grammar but cannot be materialized as Windows filenames. The real
cross-platform filesystem fixture is `managed[1]-planning`, which is legal on
Windows and POSIX. The tests must prove `foo[1]` matches literally and never
matches `foo1`, and `managed` never matches `managed-other`.

## PRODUCTION ISSUERS / RESOLVER / PUBLICATION

The only production issuers remain:

```text
planning-lite authorize-preparation TARGET --change-id CHANGE_ID --task-or-operation-id TASK_OR_OPERATION_ID --decision-provenance-ref REF
planning-lite authorize-recovery TARGET --attempt-id ATTEMPT_ID --decision-provenance-ref REF
```

`issue_authorization(...)` is internal mechanical support, not closure proof.
`resolve_authorization` remains pure with outcomes `AUTHORIZED`,
`INVALID_REFERENCE`, `NOT_FOUND`, `CORRUPT_CONFLICT`, `WRONG_ACTION`, and
`WRONG_SCOPE`. Publication retains temp materialization, fsync, platform locks,
lock-held absence, same-directory publish, reread/hash verification, and no
overwrite. No consumption or cross-store transaction is added.

## EXACT IMPLEMENTATION PATHS

| Path | Operation | Scope |
|---|---|---|
| `src/planning_lite/authorization.py` | ADD | Record/store/codec/allocation/resolver |
| `src/planning_lite/cli.py` | MODIFY | Issuers and literal-root update wiring |
| `src/planning_lite/local_update.py` | MODIFY | Separate literal containment and precedence |
| `tests/test_authorization.py` | ADD | Codec/ref/resolver/identifier evidence |
| `tests/test_cli.py` | MODIFY | Issuer and CLI contract evidence |
| `tests/test_authorization_traversability.py` | ADD | Real issuance-to-resolution evidence |
| `tests/test_local_only_update.py` | MODIFY | Literal roots, precedence, causal V-21 fixture |

```text
SEMANTIC_PRODUCTION_PATH_COUNT: 2
TEST_EVIDENCE_PATH_COUNT: 4
MECHANICAL_INTEGRITY_PATH_COUNT: 1
TOTAL_PLANNED_PATH_COUNT: 7
UNJUSTIFIED_PATH_COUNT: 0
COPIER_RULE_UPDATE_REQUIRED: NO
```

## TASK GRAPH

```text
T-01 -> T-02 -> T-03 -> T-04 -> T-05 -> T-06 -> T-07 -> T-08 -> T-09
TASK_COUNT: 9
TASK_GRAPH_ACYCLIC: YES
```

- T-01 captures authority, live matcher, CLI, policy, and baseline state.
- T-02 adds owner/store/codec, safe publication, and separate literal-root
  ownership inputs with normalization and precedence.
- T-03 adds resolver and exact validators.
- T-04 adds the two explicit issuers and passes the literal boundary through
  local-only planning/apply.
- T-05 adds owner/store/codec/ref/identifier/precedence tests.
- T-06 extends CLI tests.
- T-07 adds real two-action traversability.
- T-08 adds local-update metacharacter, boundedness, and causal custom-root
  preservation tests plus boundary evidence.
- T-09 executes the complete 21-verification stack and Git receipt.

## VERIFICATION PLAN

Every V row has a target, exact command/inspection, expected result, and
evidence carrier. Existing V-01 through V-20 retain the first corrected Planâ€™s
bindings, including strict JSON, duplicate members, collision exhaustion,
identifiers, `uv sync`, full `uv run pytest`, clean adoption, and Doctor.

| V | Exact target/command or inspection | Expected result | Evidence |
|---|---|---|---|
| V-01 | Authority hashes; `git rev-parse HEAD`; status/diff/index inspection | Pinned inputs, expected HEAD, known dirt, empty index | Receipt |
| V-02 | `uv run --frozen pytest tests/test_authorization.py -k "codec or schema or duplicate or canonical"` | Strict compact bytes, duplicate and round-trip rejection | Pytest/fixtures |
| V-03 | Owner tests for default/custom roots plus injected allocator | Exact store/ref identity and 16-collision exhaustion | Inventory/hashes |
| V-04 | `uv run --frozen pytest tests/test_authorization_traversability.py -k preparation_positive` | Real preparation CLI -> resolver `AUTHORIZED` | Pytest/record |
| V-05 | `uv run --frozen pytest tests/test_authorization.py -k preparation_negative` | Preparation malformed/default/identifier negatives, no write | Digest/pytest |
| V-06 | `uv run --frozen pytest tests/test_authorization_traversability.py -k recovery` | Real recovery CLI -> exact Attempt resolution | Pytest/digest |
| V-07 | Resolver success/rejection hash snapshot tests | Six outcomes and no resolver mutation | Hash assertions |
| V-08 | Concurrent process and forced same-ref allocator tests | No overwrite/partial record; bounded failure | Process/inventory |
| V-09 | `rg` call-site inventory plus AST/source inspection | Only two CLI issuer roots; no hidden issuer | Call graph |
| V-10 | Decoy CURRENT/ACTIVE/local/prose/receipt/Attempt temp-target tests | Decoys cannot issue/resolve authority | Negative/source evidence |
| V-11 | Issue, hash, resolve repeatedly; inspect keys/commands | Immutable bytes, no revoke/consume state | Hash/schema evidence |
| V-12 | Source import/call graph plus `pytest -k independent_closure` | No Runtime/executor/lifecycle/PL08 dependency | Imports/pytest |
| V-13 | `uv run --frozen pytest tests/test_authorization_traversability.py -k traversability` | Both bounded real system seams; Runtime remains next gap | System pytest |
| V-14 | `uv run --frozen pytest tests/test_cli.py -k "authorize or explicit or required"` | Required args/no defaults/error mapping | CLI pytest |
| V-15 | `uv run --frozen pytest tests/test_authorization.py tests/test_authorization_traversability.py tests/test_cli.py tests/test_local_only_update.py` | Four focused paths pass | Focused pytest |
| V-16 | `uv run pytest` | Full repository regression passes | Full pytest |
| V-17 | `uv run --frozen pytest tests/test_local_only_update.py -k "effective_root or authorization or project_owned or literal or precedence"` plus source inspection | Literal roots, siblings, normalization, precedence, hashes pass | Plan/apply/hashes |
| V-18 | Count AC/CC/T/V rows; inspect seven paths; recapture Git/index | 24/24, 13/13, 9, 21, 7; no mutation | Audit receipt |
| V-19 | `uv sync` from central checkout | Synchronization exits 0 | Command receipt |
| V-20 | Disposable clean consumer: `uv run planning-lite adopt <CONSUMER> --template-source <SOURCE> --vcs-ref v0.0.0.dev1`; then `uv run planning-lite doctor <CONSUMER>` | Adoption and Doctor exit 0; healthy consumer | Adoption/Doctor receipt |
| V-21 | Exact causal setup and commands below | Literal custom-root authorization preserved while tagged managed content changes | Hashes/plan/resolver/Git diff |

## V-21 EXACT UPDATE PRESERVATION

```text
V21_CORRECTION_MODE: REWRITE_SINGLE_V21
VERIFICATION_COUNT: 21
```

### SETUP

Create disposable clean Git repositories `<SOURCE>` and `<CONSUMER>`, configure
test Git identity, commit the source template baseline, and create annotated
source tag `v0.0.0.dev1`. Initialize and baseline-commit the consumer. Run:

```text
uv run planning-lite adopt <CONSUMER> --template-source <SOURCE> --vcs-ref v0.0.0.dev1
```

Add `.planning/` and `.agents/` to the consumer `.gitignore`; commit the
adoption bridge, answers, and ignore rule. In ignored `.planning/CONFIG.yml`,
set `project_policy.planning_root: managed[1]-planning`. Issue a real
preparation authorization against the consumer, capture its ref, and commit
the resulting sentinel record at the exact path below so the consumer is
clean:

```text
SENTINEL_AUTHORIZATION_PATH:
managed[1]-planning/project/authorizations/<authorization_ref>.json
SENTINEL_PRE_SHA256: capture SHA256 of the committed real record before update
```

In `<SOURCE>`, append `PL09_V21_AFTER` to `template/.planning/README.md` and
add a candidate file at the same `template/managed[1]-planning/project/
authorizations/<authorization_ref>.json` destination with deliberately
different bytes. Commit and create annotated tag `v0.0.0.dev2`; require the
source and consumer to be clean before the commands below.

### LOCAL_UPDATE_COMMAND

```text
uv run planning-lite check <CONSUMER> --template-source <SOURCE> --vcs-ref v0.0.0.dev2 --local-only
uv run planning-lite update <CONSUMER> --template-source <SOURCE> --vcs-ref v0.0.0.dev2 --local-only
```

`check` is the exact dry-run preview; `update --local-only` is the exact
atomic apply. Both traverse the runtime literal ownership input. No
`--allow-dirty` is used.

### TAGGED_UPDATE_COMMAND

```text
uv run planning-lite update <CONSUMER> --template-source <SOURCE> --vcs-ref v0.0.0.dev2 --local-only
```

The command syntax is intentionally identical to the local-source command. The
two proof dimensions are distinct in environment: `<SOURCE>` is a disposable
local Git source, and `v0.0.0.dev2` is a committed tagged ref after adoption
from `v0.0.0.dev1`. Ordinary tracked Copier update is not claimed as evidence
because it bypasses `local_update.py`.

```text
LOCAL_UPDATE_MODE_REQUIRED: YES
LOCAL_UPDATE_COMMAND: uv run planning-lite update <CONSUMER> --template-source <SOURCE> --vcs-ref v0.0.0.dev2 --local-only
TAGGED_UPDATE_MODE_REQUIRED: YES
TAGGED_UPDATE_COMMAND: uv run planning-lite update <CONSUMER> --template-source <SOURCE> --vcs-ref v0.0.0.dev2 --local-only
TARGET: clean disposable local-only <CONSUMER>
SOURCE_OR_TAG: local disposable Git <SOURCE>, installed v0.0.0.dev1, requested v0.0.0.dev2
PRECONDITIONS: ignored .planning/.agents; managed[1]-planning config; issued sentinel committed; source and consumer clean
EXPECTED_EXIT: check 0; apply 0
EXPECTED_PRESERVED_FILE: managed[1]-planning/project/authorizations/<authorization_ref>.json
EXPECTED_PRESERVED_SHA256: exactly SENTINEL_PRE_SHA256
EXPECTED_MANAGED_MARKER_CHANGE: .planning/README.md contains PL09_V21_AFTER; answers ref advances to v0.0.0.dev2
EVIDENCE_CARRIER: preview plan, command transcripts, before/after SHA256, resolver AUTHORIZED result, source/consumer status/diff/inventory
```

The different candidate bytes make preservation causal: correct literal
classification yields `KEEP_PROJECT`; an unsafe or absent dynamic projection
cannot silently pass as untouched state. The README marker proves update
execution changed managed content.

## AC / CC TRACEABILITY

All canonical rows remain substantive at 24/24 and 13/13. The corrected rows
are explicitly strengthened as follows; unaffected rows preserve their first
corrected mappings.

| AC | Corrected evidence | Tasks | Verifications |
|---|---|---|---|
| AC-01 | Existing decision authorities; CLI only | T-02,T-04 | V-02,V-04,V-06,V-12 |
| AC-02 | No self-issue/runtime issuer | T-02,T-08 | V-09,V-12 |
| AC-03 | One effective-root source and literal subtree ownership | T-02,T-04,T-08 | V-03,V-17,V-21 |
| AC-04 | Opaque ref and finite allocation | T-02,T-05 | V-02,V-03,V-08 |
| AC-05 | Closed two-action enum | T-02,T-04 | V-02,V-14 |
| AC-06 | Exact preparation scope/IDs | T-03,T-05,T-06 | V-04,V-05,V-14 |
| AC-07 | Exact recovery scope/Attempt ID | T-03,T-05,T-06 | V-06,V-14 |
| AC-08 | Two real CLI issuers | T-04,T-06,T-07 | V-04,V-06,V-09,V-13 |
| AC-09 | Explicit required target/scope/provenance | T-04,T-06 | V-05,V-06,V-10,V-14 |
| AC-10 | Seven-key strict record | T-02,T-05 | V-02,V-03 |
| AC-11 | Shared resolver/two validators | T-03 | V-07,V-13 |
| AC-12 | Corruption/duplicate/noncanonical/conflict rejection | T-02,T-03,T-05 | V-02,V-03,V-05,V-06,V-08 |
| AC-13 | Wrong action | T-03,T-05 | V-05,V-06,V-07 |
| AC-14 | Wrong exact scope | T-03,T-05 | V-05,V-06,V-07 |
| AC-15 | No routing/prose/history authority | T-08 | V-09,V-10,V-17 |
| AC-16 | Immutable source and causal update preservation | T-02,T-05,T-08 | V-08,V-11,V-17,V-21 |
| AC-17 | Preparation downstream single-use boundary | T-08 | V-12 |
| AC-18 | Recovery downstream single-use boundary | T-08 | V-12 |
| AC-19 | No source consumption/transaction | T-02,T-08 | V-11,V-12 |
| AC-20 | No subsystem/runtime expansion | T-08,T-09 | V-09,V-12,V-17,V-21 |
| AC-21 | Real positive/negative/trust proof | T-04,T-07,T-08 | V-04,V-06,V-09,V-10,V-13 |
| AC-22 | Bounded seam and next gap | T-07,T-09 | V-13,V-18 |
| AC-23 | Trust root/anchor/event | T-04,T-08 | V-09,V-10,V-18 |
| AC-24 | No defaults/implicit/runtime issuer | T-04,T-08 | V-09,V-10,V-14 |

```text
AC_T_V_TRACEABILITY: PASS
AC_TRACEABILITY_COUNT: 24/24
AC_REMEDIATION: COMPLETE
AFFECTED_AC_IDS: AC-03,AC-16
```

| CC | Closure evidence | Tasks | Verifications |
|---|---|---|---|
| CC-01 | Real issuer -> durable record -> ref | T-04,T-06,T-07,T-09 | V-04,V-06,V-09,V-13,V-20 |
| CC-02 | Exact preparation issue/resolve | T-03,T-04,T-07 | V-04,V-05,V-13 |
| CC-03 | Preparation negative matrix | T-03,T-05,T-06 | V-03,V-05,V-10,V-14 |
| CC-04 | Exact recovery issue/resolve | T-03,T-04,T-07 | V-06,V-13 |
| CC-05 | Recovery negative matrix | T-03,T-05,T-06 | V-03,V-06,V-10,V-14 |
| CC-06 | Strict schema/conflict proof | T-02,T-03,T-05 | V-02,V-03,V-07,V-08 |
| CC-07 | Synthetic downstream reuse contract | T-08 | V-12 |
| CC-08 | Immutable/no-overwrite/causal update preservation | T-02,T-05,T-08 | V-08,V-11,V-17,V-21 |
| CC-09 | Routing/local/prose boundary | T-08 | V-09,V-10,V-17 |
| CC-10 | No Runtime/executor/lifecycle/PL08 | T-08,T-09 | V-12,V-17,V-20 |
| CC-11 | No auth/policy/multiple-source expansion | T-02,T-04,T-08 | V-09,V-17,V-18,V-21 |
| CC-12 | Bounded end-to-end traversability | T-07,T-09 | V-13,V-18,V-20 |
| CC-13 | Trust root/no defaults/no alternate issuer | T-04,T-08,T-09 | V-09,V-10,V-14,V-18,V-20 |

```text
CC_TRACEABILITY: PASS
CC_TRACEABILITY_COUNT: 13/13
CC_REMEDIATION: COMPLETE
AFFECTED_CC_IDS: CC-08
```

## COMPLETION, INDEPENDENCE, AND FALSE-DONE BOUNDARY

```text
UV_SYNC_REQUIRED: YES
CLEAN_GIT_ADOPTION_REQUIRED: YES
ADOPTED_CONSUMER_DOCTOR_REQUIRED: YES
ATTEMPT_RUNTIME_IMPLEMENTATION_INCLUDED: NO
ATTEMPT_RUNTIME_INDEPENDENT_CLOSURE_PLAN: PASS
FALSE_DONE_REMEDIATION: COMPLETE
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_MATERIAL_IMPLEMENTATION_CHOICES: 0
```

The Plan cannot pass while a literal-special root is treated as a glob, a
sibling is classified, preservation is accidental, update commands are vague,
or adoption/Doctor substitutes for update proof. V-21 requires an observable
managed marker and a different candidate file at the exact sentinel path.
## Canonical Plan approval boundary

This Plan is approved and canonicalized, but Formal Readiness has not been
adjudicated. It does not authorize implementation, Attempt Runtime planning,
executor-prerequisite work, lifecycle resumption, Change 2 or Change 3 work,
source/template/test mutation, staging, commit, push, or release.

~~~text
PLAN_APPROVED: YES
FORMAL_READINESS: NOT_YET_ADJUDICATED
IMPLEMENTATION_AUTHORIZED: NO
ATTEMPT_RUNTIME_IMPLEMENTATION_INCLUDED: NO
ATTEMPT_RUNTIME_INDEPENDENT_CLOSURE_PLAN: PASS
EXECUTOR_DEPENDENCY: NO
LIFECYCLE_DEPENDENCY: NO
CHANGE_2: BLOCKED / VALID / PAUSED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
SEMANTIC_DRIFT: NO
~~~

## Canonical terminal receipt

~~~text
PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_IMPLEMENTATION_PLAN_APPROVAL_CANONICALIZATION
OVERALL: PASS_CANONICAL_IMPLEMENTATION_PLAN_CREATED
OWNER_PLAN_APPROVAL: APPROVE_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION_IMPLEMENTATION_PLAN
APPROVED_SOURCE_PLAN_SHA256: 4E432C183A979539EE5E3CD8490A85B7AEF4FF511BE0A98CE124EF33FFFBBD48
APPROVING_FRESH_REVIEW_SHA256: B68963A0F6EEDCE5DB06ED4B8003B06D62B1BED7219BF5CA35CE10402908BADA
SEMANTIC_DRIFT: NO
SOURCE_MUTATIONS: 0
STAGED_PATHS: 0
COMMIT: NO
PUSH: NO
NEXT_SINGLE_GATE: FORMAL_READINESS_PL09_AUTHORITATIVE_ATTEMPT_ACTION_AUTHORIZATION
~~~
