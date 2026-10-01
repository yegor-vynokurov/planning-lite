# Material Code Documentation and Maintainability Binding — Formal Readiness v2

```text
CHANGE_ID: CHG-PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-001
OWNER_REVIEW_VERDICT: SEMANTIC_CONTRACT_PASS / FORMAL_READINESS_HOLD_FOR_ONE_TEMPLATE_INTEGRITY_PLAN_CORRECTION
OWNER_FINDING: DOC-MAINT-RF-01_TEMPLATE_INTEGRITY_SURFACE_OMITTED
DEFINITION_V1: ACCEPTED SEMANTIC CONTRACT / BYTE-IDENTICAL
PLAN_V1: BYTE-IDENTICAL / AMENDED BY PLAN AMENDMENT V1
FORMAL_READINESS: READY / v2
IMPLEMENTATION_AUTHORIZED: NO
ENTRY_HEAD: 7bbf5937094484b074d20224aadb370c0d3ae493
ENTRY_GATE: OWNER_REVIEW_MATERIAL_CODE_DOCUMENTATION_AND_MAINTAINABILITY_BINDING_DEFINITION_PLAN_AND_READINESS
```

## Fresh review scope

This fresh Formal Readiness evaluates the effective contract formed by:

1. Definition v1, SHA-256
   `4eba43b069348750bd860441866b8c6f09ac7a17d36d547e1895b6110eaf89a6`;
2. Plan v1, SHA-256
   `a1e0f00e2b48333ba01ec526a06fce20c472a887c61999dfc9ede21acf1db204`; and
3. Plan Amendment v1, adding the integrity paths, deterministic receipt
   behavior, mandatory verification, and clean-source field/update proof.

Definition v1's accepted semantic decision is unchanged. Plan v1 is
byte-identical. The earlier readiness hold concerned one omitted existing
integrity contract; this v2 checks that correction against the live template
tree and current integrity detector. No template/test implementation or field
proof was performed during this governance transition.

Live detector evidence is
`tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree`:
it asserts manifest listed paths equal the actual `.planning/` tree, the
manifest count matches, SHA receipt paths exactly cover the tree except
`SHA256SUMS.txt`, and every receipt equals the canonical-LF SHA-256 of the
covered file. The two requested update smokes exist and operate on temporary
Git consumers; the template-update script explicitly requires a clean,
Git-versioned central source. The candidate proof-source requirement therefore
uses a disposable isolated clean proof checkout with exact candidate hashes
and a temporary synthetic commit, not the dirty central source.

## Readiness criteria

| ID | Criterion | Result | Evidence |
|---|---|---|---|
| R01 | Single normative owner identified. | PASS | CODEBASE_DESIGN remains the sole normative owner; CODE_REVIEW verifies it, and DoD remains broad. |
| R02 | Material-code applicability is bounded. | PASS | Definition v1's finite triggers and constrained hidden-contract catch-all are unchanged. |
| R03 | Trivial/private no-doc cases remain legal. | PASS | Definition v1 retains explicit exemptions; no coverage quota was added. |
| R04 | Documentation meaning differs from mere presence. | PASS | Definition v1 retains separate presence and semantic adequacy checks, including rejection of tautology. |
| R05 | Stale or contradictory documentation is rejectable. | PASS | Definition v1 requires consistency with behavior/invariants and same-Change updates. |
| R06 | Planning creates a concrete symbol-level obligation. | PASS | Plan v1's marker/location/form/verification obligation remains unchanged; the amendment changes only integrity and execution-proof details. |
| R07 | Readiness can test the applicability and obligation. | PASS | Plan v1 and Definition v1 still specify a scope/evidence comparison, a determinate symbol obligation, and an available verification route. |
| R08 | Execution receives CODEBASE_DESIGN before/during applicable generation. | PASS | The approved Plan marker conditionally selects the workflow-loaded CODEBASE_DESIGN contract; newly discovered scope uses the existing amendment route. Runtime schema remains unchanged. |
| R09 | Closure checks the same rule without duplication. | PASS | CODE_REVIEW remains the review procedure and refers to the one CODEBASE_DESIGN norm; no normative duplication was introduced. |
| R10 | Maintainability contract remains coherent with CODEBASE_DESIGN. | PASS | Small coherent design, explicit contracts/ownership, locality, bounded coupling, thin orchestration, useful seams, and evidence-based abstractions remain the accepted semantics. |
| R11 | Performance optimization is not implicitly required. | PASS | Performance work still requires evidence of need; no profiler or performance target was added. |
| R12 | Existing code debt is not a retrofit mandate. | PASS | Applicability remains prospective; existing omissions remain observed debt absent separate authorization. |
| R13 | M0–M4 selector proof is feasible. | PASS | Amendment v1 requires the ordinary consumer route, marker-to-scope Readiness check, observable pre/during-generation load, CODE_REVIEW closure check, and separate selector/review evidence for M0–M4 without hidden prompt injection. |
| R14 | No unnecessary runtime/schema/service is introduced. | PASS | Effective semantics remain managed policy plus focused tests; no Python runtime or schema path is authorized. |
| R15 | Sequential whole-organism proof remains NOT STARTED. | PASS | It is explicitly outside this Change and was not run. |
| R16 | 09-G remains NOT STARTED. | PASS | It is explicitly outside this Change and was not started. |
| R17_WRITE_AND_INTEGRITY_SURFACE | Six semantic managed template paths, one focused test, and two integrity receipt paths are included. | PASS | Amendment v1 names exactly six semantic `template/.planning/**` paths, `tests/test_field_control_pack_foundation.py`, and receipt-only `MANIFEST_V4.md` / `SHA256SUMS.txt`. No Python runtime path is present. |
| R18_TEMPLATE_INTEGRITY_EXECUTABILITY | Receipt order/detector/smokes/clean-source identity are executable without weakening ownership or tests. | PASS | T-04I follows stable semantic bytes and defines path/count/set/canonical-LF checks; T-04V mandates the existing detector and focused semantic/execution regression tests; no weakening, exclusion, or xfail is proposed; T-05 binds the field proof and T-06 both update smokes to the exact-candidate clean proof source identity, with `uv sync`, full pytest, temporary consumer adoption/Doctor. |

## Effective future implementation surface

Semantic managed template paths (6):

- `template/.planning/disciplines/CODEBASE_DESIGN.md`
- `template/.planning/control/CHANGE_PLANNING.md`
- `template/.planning/control/CHANGE_READINESS.md`
- `template/.planning/control/CHANGE_EXECUTION.md`
- `template/.planning/control/CHANGE_CLOSURE.md`
- `template/.planning/disciplines/CODE_REVIEW.md`

Focused test path (1): `tests/test_field_control_pack_foundation.py`.

Integrity receipt paths (2):

- `template/.planning/docs/MANIFEST_V4.md` — allowed for deterministic
  regeneration/verification and expected byte-identical because path set and
  count do not change;
- `template/.planning/framework/SHA256SUMS.txt` — expected to change for the
  six modified semantic template files.

No runtime, schema, Plan template, skill, mode, ownership, Copier, or Roadmap
path is required. Existing `tests/test_direction_foundation.py` integrity
coverage is mandatory, not weakened, excluded, or xfailed. The ordinary
execution guidance regression retains `discipline_refs == []`.

## Verification readiness

Amendment v1 makes the implementation sequence executable. After implementation
authorization, finalize the six semantic template bytes, then perform T-04I
receipt reconciliation, followed by these mandatory T-04V checks:

```text
uv run --frozen pytest -q tests/test_field_control_pack_foundation.py
uv run --frozen pytest -q tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree
uv run --frozen pytest -q tests/test_execution_guidance.py::test_contract_route_projects_contract_closure_and_zero_discipline_is_explicit
```

Only after T-04V passes may the disposable selector/M0–M4 field proof begin.
T-06 requires the clean-source template/update smokes:

```text
uv run --frozen python scripts/test_template_update.py
uv run --frozen python scripts/test_local_only_update.py
```

It also requires `uv sync`, `uv run pytest`, clean temporary consumer adoption
and Doctor as required by central verification policy, and candidate review.
Because the central checkout is dirty, these source-identity-dependent checks
must use a disposable clean proof checkout populated with the exact reviewed
candidate bytes and a temporary synthetic commit. Bind the exact path hashes
and temporary commit ID in the later implementation checkpoint. The temporary
commit does not alter central HEAD, stage central paths, or grant any commit or
release authority.

The manifest is not expected to change. If its path set/count are unchanged but
deterministic regeneration changes its bytes, inspect and explain the
difference. Unexplained drift blocks under
`DOC_MAINT_MANIFEST_UNEXPECTED_DRIFT`. A newly required path blocks under
`DOC_MAINT_ADDITIONAL_TEMPLATE_OWNER_REQUIRED`.

## Verdict and authority boundary

R01–R18 pass. `DOC-MAINT-RF-01_TEMPLATE_INTEGRITY_SURFACE_OMITTED` is
`CLOSED_BY_PLAN_CORRECTION`. Therefore `FORMAL_READINESS: READY / v2` for the
amended implementation plan. Implementation remains `NOT AUTHORIZED` and
requires the next separate owner gate. No implementation, template/test
mutation, consumer proof, staging, commit, or push occurred here. Whole-
organism proof remains `NOT STARTED`; 09-G remains `NOT STARTED`; Roadmap is
unchanged.

Next single gate:
`OWNER_AUTHORIZE_MATERIAL_CODE_DOCUMENTATION_AND_MAINTAINABILITY_BINDING_IMPLEMENTATION_AFTER_INTEGRITY_CORRECTION`.

## Transition state receipt

```text
ENTRY_HEAD: 7bbf5937094484b074d20224aadb370c0d3ae493
ENTRY_GATE: OWNER_REVIEW_MATERIAL_CODE_DOCUMENTATION_AND_MAINTAINABILITY_BINDING_DEFINITION_PLAN_AND_READINESS
ENTRY_CURRENT_CANONICAL_LF_SHA256: 118970d9f008d48e6751b390791bb01f8043804d0b87c29bf214eca36a247439
ENTRY_AUTHORITY_STATE_ID: baccfbf763ea54086a5504936e2893c9ee36bd10fcf8e980242063f8281db273
ENTRY_UNRELATED_DIRT_PATHS: 14
ENTRY_UNRELATED_DIRT_STATE_ID: 2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821
ENTRY_INDEX_EMPTY: YES

DEFINITION_UNCHANGED: YES
DEFINITION_SHA256: 4eba43b069348750bd860441866b8c6f09ac7a17d36d547e1895b6110eaf89a6
PLAN_V1_UNCHANGED: YES
PLAN_V1_SHA256: a1e0f00e2b48333ba01ec526a06fce20c472a887c61999dfc9ede21acf1db204
PLAN_AMENDMENT_SHA256: 5e9b2bc6c22391b6ca7280cb20cddaf50e7aff071cd04fba4080514fed7f39f5
FORMAL_READINESS_V1_SHA256: a4f6c3a54bfa7386745a417f8f57368db36988ad902c5c84b50e001f114bc0ea
CANDIDATE_STATE_ID: cb758806cafc30458aaa6207073f69d4f49ad314cacd9826e4f997eeafc322df
CANDIDATE_STATE_ID_METHOD: SHA-256 of canonical UTF-8 JSON (sorted keys, compact separators) over sorted source_path_sha256_rows for Definition v1, Plan v1, and Plan Amendment v1. Formal Readiness v2 is the separate verdict receipt and excluded from this candidate identity.

EXIT_HEAD: 7bbf5937094484b074d20224aadb370c0d3ae493 / UNCHANGED
EXIT_CURRENT_CANONICAL_LF_SHA256: 18897ade6e3063d5f9711cacd8253116d56892b55b3cfc66a3840df265435be8
EXIT_AUTHORITY_STATE_ID: 3b8fb80d21f48df2ad1301b9444f4b67a8525ea9c9dbfebdc53032d11b54fe6c
EXIT_AUTHORITY_STATE_ID_METHOD: SHA-256 of canonical UTF-8 JSON (sorted keys, compact separators) over previous_authority_state_id, candidate_state_id, current_sha256, and sorted source_path_sha256_rows below. CURRENT is represented separately by current_sha256. Formal Readiness v2 is excluded from its own digest.
EXIT_CANDIDATE_STATE_ID: cb758806cafc30458aaa6207073f69d4f49ad314cacd9826e4f997eeafc322df
EXIT_UNRELATED_DIRT_PATHS: 14
EXIT_UNRELATED_DIRT_STATE_ID: 2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821 / PRESERVED
EXIT_SYNC_STATE_ID: NOT_REPRODUCIBLE_BY_CURRENT_TOOLING
ROADMAP_CANONICAL_LF_SHA256: 056933c1116e3adbaf2330baba32718498aa5cf2f88eb4ea1ef576433392f0bc / UNCHANGED
EXIT_INDEX_EMPTY: YES
STAGE: NO
COMMIT: NO
PUSH: NO
IMPLEMENTATION_AUTHORIZED: NO
SEQUENTIAL_WHOLE_ORGANISM_PROOF: NOT STARTED
09-G: NOT STARTED
```

The sorted `source_path_sha256_rows` used by the authority digest are
canonical-LF SHA-256 values:

| Path | SHA-256 |
|---|---|
| `copier.yml` | `92d9460e25a2178f3ada6d8badce9eb1c9aa2ca94765d374385885be752cb8ad` |
| Definition v1 | `4eba43b069348750bd860441866b8c6f09ac7a17d36d547e1895b6110eaf89a6` |
| Formal Readiness v1 | `a4f6c3a54bfa7386745a417f8f57368db36988ad902c5c84b50e001f114bc0ea` |
| Plan Amendment v1 | `5e9b2bc6c22391b6ca7280cb20cddaf50e7aff071cd04fba4080514fed7f39f5` |
| Plan v1 | `a1e0f00e2b48333ba01ec526a06fce20c472a887c61999dfc9ede21acf1db204` |
| Accepted vitality challenge | `a337a1c7ef947ab423d6c81a57ac61b12f93b6420d084391a92a920d3c5acf18` |
| `docs/design/project-spine/roadmap/ROADMAP.md` | `056933c1116e3adbaf2330baba32718498aa5cf2f88eb4ea1ef576433392f0bc` |
| `scripts/maintainer_resume.py` | `80ea9cb61498cc647f76a881c71b0003964f9d439cf33264fc572f565bb85a2d` |
| `scripts/test_local_only_update.py` | `6d3b3dc3bfb9fe6317619f04ed5553556fb8268ba4e273af1194d56b489333b6` |
| `scripts/test_template_update.py` | `0bf1541bfb3f80e4654512f0a8474f20c8c6542f25073faedb01a1fe4ca527e7` |
| `src/planning_lite/execution_guidance.py` | `7a7c7a0c96f3dd3d9f2d21c7453b156e7c34d00513ae0a0589d0ecc3f71bd33e` |
| `template/.planning/changes/templates/plan.md` | `251e6148258e865bf20f854bdbb95016f6cd1197d4865e9d4dfcf3a723f56703` |
| `template/.planning/control/CHANGE_CLOSURE.md` | `669f27475d6ab9928ecf1ac70b4117e9a52a17ade4e68f592bfe2ab898beff75` |
| `template/.planning/control/CHANGE_EXECUTION.md` | `e4960eab37e572b9f838c9e4cf601c456e7b90ca0c58b75cbba6c36276d16c20` |
| `template/.planning/control/CHANGE_PLANNING.md` | `dc7ebbeb872c4cd9f213eadc6134876712a3cbe833d405dbca3b29252091cd57` |
| `template/.planning/control/CHANGE_READINESS.md` | `84573edf2cf63365ae7d932e622f751b46ce7f9a1932fb9d1c2c505789df72c1` |
| `template/.planning/disciplines/CODEBASE_DESIGN.md` | `2e1624e966e911a03c348eba7a0f9685339a4d661bd3137d8846877ceade0a9e` |
| `template/.planning/disciplines/CODE_REVIEW.md` | `f50dd7fa7ddbd6ba86ff66385fabc044cb94de42f379ab4223cec6cd3cf0857b` |
| `template/.planning/docs/MANIFEST_V4.md` | `e9f39bf28f4d84ce05b50758d3dc2978e02d8302e465151a771e41c7c6edb258` |
| `template/.planning/framework/OWNERSHIP.yml` | `df9013d773cd1b5d433354dd82ba45e517835b1b92d3ce565260a6d496ac80ff` |
| `template/.planning/framework/SHA256SUMS.txt` | `ab1dd8c0dff2fa013e63b53aacc81babfaa51e295bc4e1a5b1d60f444a3c5bef` |
| `template/.planning/modes/EXECUTE.md` | `86334ad9146bb175a24fb742d12a1b305fc29727afc853705d1804cc3449dbef` |
| `template/.planning/modes/PLAN.md` | `87d000a96a34e115de24c23eff4e2c9a82db13e04d7cc431c312f50eea457f71` |
| `template/.planning/skills/planning-audit/SKILL.md` | `2f0596b16cb6b7b36ff6a3a9ee07652258c7f7cf636d1476a1a5e18caba96283` |
| `template/.planning/skills/planning-execute/SKILL.md` | `0eb65e095de5e92ba9199eb039fd0361f3415b243de594d40d0578eee608bf4a` |
| `template/.planning/skills/planning-plan/SKILL.md` | `03170663e2c080df19f155cd483791cd06d4b5c7a5bf9fe7a4b879ddfbe49f19` |
| `tests/test_direction_foundation.py` | `69f46fdc3254f096b9d0c2deb1e68f32671794e6e044dbc97e4657df0d3ed094` |
| `tests/test_execution_guidance.py` | `91338fe086c8475bb042d6e3d6105094b4d7ce551dccab5903bbc51f18da3fa5` |
| `tests/test_field_control_pack_foundation.py` | `a3cf5b6d7dff5ee60c633c7c03167c04f54047e29ffdc04e1d0fe495066b61ce` |
