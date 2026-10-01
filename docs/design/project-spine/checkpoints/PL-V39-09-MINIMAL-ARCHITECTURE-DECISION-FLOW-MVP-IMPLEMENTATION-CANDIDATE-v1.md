# PL-V39-09 Minimal Architecture Decision Flow MVP - Implementation Candidate v1

## Authorization and scope

CHANGE_ID: `CHG-PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-001`  
OWNER_IMPLEMENTATION_AUTHORIZATION: `AUTHORIZE_PL_V39_09_MINIMAL_ARCHITECTURE_DECISION_FLOW_MVP_IMPLEMENTATION` / explicit user decision / CONSUMED  
AUTHORIZED_TASKS: T-01 through T-04V only  
T-05_REAL_FIELD_PROOF: NOT AUTHORIZED IN THIS TRANSITION / NOT EXECUTED  
09-G: NOT STARTED  
P-05_REPAIR: NOT AUTHORIZED / NOT PERFORMED  
ROADMAP_MUTATION, RELEASE, PUSH: NOT AUTHORIZED / NOT PERFORMED

The implementation follows Definition v2 and the effective Plan (Plan v2 plus
Amendment v1). No additional design gate was created. The implementation
remains a candidate pending owner review; this checkpoint does not claim field
validation or Change closure.

## Effective contracts and entry baseline

| Authority | Path | SHA-256 |
|---|---|---|
| Definition v2 | `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-CHANGE-DEFINITION-v2.md` | `03b27174696ee828db9ac431d70194621e9ccf50d278bc1530e55ba3bfc1ced3` |
| Plan v2 | `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-IMPLEMENTATION-PLAN-v2.md` | `f8b7f53e0894932ad00583b46a80180f29a387eb42089f7c8f6c2bf145cfeffa` |
| Plan Amendment v1 | `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-IMPLEMENTATION-PLAN-AMENDMENT-v1.md` | `1c72dc11731ee9be9f5890e1d9b0fff76a3b56577828bb53fe873015c0099073` |
| Formal Readiness v2 | `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-FORMAL-READINESS-VERDICT-v2.md` | `8d80a97ab699168841c81a5ef9f0f552c6beca0569eb9de2073d37dd239fd680` |

ENTRY_HEAD: `f16fd50f93452f9f38a892d58fdad7c67f3bbcd8`  
ENTRY_AUTHORITY_STATE_ID: `9c7b1d32b5a0ce3ff8d75ac482cccb39caee921ff9620ce0cfc4df77c069dc39`  
ENTRY_CANDIDATE_STATE_ID: `d39a97a3a279ce4e2617601487fbac6943a1be50b90994fd2d8b847472ca0cf9`  
ENTRY_UNRELATED_DIRT_STATE_ID: `2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821`  
ENTRY_CURRENT_GATE: `OWNER_AUTHORIZE_PL_V39_09_MINIMAL_ARCHITECTURE_DECISION_FLOW_MVP_IMPLEMENTATION_AFTER_INTEGRITY_CORRECTION`  
ENTRY_INDEX_EMPTY: YES  
ENTRY_SYNC_STATE_ID: NOT_REPRODUCIBLE_BY_CURRENT_TOOLING (known limitation; not a stop condition)

The authorization baseline matched the expected HEAD, authority, candidate,
unrelated-dirt ID, effective-contract hashes, and CURRENT gate. Pre-existing
unrelated edits to `src/planning_lite/operation_lifecycle.py` and
`tests/test_operation_lifecycle.py`, plus the unrelated governance drafts,
were preserved. The only semantic test owner changed is
`tests/test_project_shaping_foundation.py`.

## Implemented path manifest

Exactly three semantic/template paths and two integrity receipt paths were
written. No sixth architecture template, runtime, schema, CLI, Copier, 09-E, or
Roadmap path was required.

| Class | Path | Canonical-LF SHA-256 |
|---|---|---|
| `template/.planning/control/ARCHITECTURE_DECISION_FLOW.md` | `b27589d21b7179f6e7024d57846fb65f15c24735f979c654bc6b7062514dc93c` |
| `template/.planning/control/ROOT_ROUTER.md` | `7c17a3a9559b96dc9ad50201d8fd6a94f3737b3ed85d093cbe3cb47ce6805fed` |
| `template/.planning/docs/MANIFEST_V4.md` | `e9f39bf28f4d84ce05b50758d3dc2978e02d8302e465151a771e41c7c6edb258` |
| `template/.planning/framework/SHA256SUMS.txt` | `ab1dd8c0dff2fa013e63b53aacc81babfaa51e295bc4e1a5b1d60f444a3c5bef` |
| `template/.planning/project/ARCHITECTURE_OVERVIEW.md` | `cb19d508b35781b36a0f7480699bf454d96ee783cf50606bcd0267a062c179b5` |
| `tests/test_project_shaping_foundation.py` | `b02b7f1a073e10f7c854d41d25c2026935a598fe363c857469a4376ebe85ff50` |

`MANIFEST_V4.md` lists 167 actual files under `template/.planning/`, including
the new guide. `SHA256SUMS.txt` has 166 rows, covers the same set except itself,
and records canonical-LF hashes. No semantic content was added to either
receipt. `template/.planning/templates/project/ARCHITECTURE_OVERVIEW.md` was
not changed. `ADDITIONAL_TEMPLATE_OWNER_REQUIRED: NO`.

## Semantic test owner and A01-A16

Selected semantic test owner: `tests/test_project_shaping_foundation.py`.
It naturally owns project-shaping/routing invariants. No second semantic test
module and no `tests/test_plan_compilation.py` change were needed.

| Acceptance | Result | Evidence in selected owner |
|---|---|---|
| A01 architecture-sensitive route reaches the flow | PASS | `test_architecture_decision_flow_is_opt_in_and_preserves_routine_routing` |
| A02 routine work is not forced through the flow | PASS | same route test; routine route remains ordinary |
| A03 one material question per invocation | PASS | `test_architecture_decision_flow_records_one_question_and_provenanced_drivers` |
| A04 exactly `DECISION_ACCEPTED` or `SPIKE_REQUIRED` | PASS | `test_architecture_decision_flow_requires_measurable_scenarios_and_credible_alternatives` |
| A05 material drivers carry source/provenance | PASS | question/driver test checks materiality, ID, source, capability/seam, uncertainty, confidence, and bound |
| A06 material quality scenarios are measurable | PASS | scenario/alternatives test checks measurable quality response and scenario fields |
| A07 two credible alternatives include a simpler option | PASS | scenario/alternatives test |
| A08 no arbitrary/universal score | PASS | scenario/alternatives test rejects weighted/arbitrary numeric winner |
| A09 TARGET, MVP-REFERENCE, and TRANSITION remain distinct | PASS | `test_architecture_decision_flow_keeps_horizons_and_local_risk_fields_bounded` |
| A10 three evolution fields remain decision-local and small | PASS | same horizon/risk-fields test |
| A11 replaceability seam remains optional | PASS | same test checks conditional flow guidance and optional carrier field |
| A12 a practical evidence/fitness route exists | PASS | same test checks at least one route for every material selected claim |
| A13 observed Brownfield topology is not Ideal authority | PASS | `test_architecture_decision_flow_preserves_brownfield_evidence_and_existing_handoff` |
| A14 semantic Plan remains authority; 09-E remains compiler | PASS | same Brownfield/handoff test checks `plan-compile` and that compiled output does not replace semantic authority |
| A15 no 09-G/runtime subsystem expansion is required | PASS | same test checks no 09-G, Context Compiler, SQLite/vector, Prompt Garden, schema, or runtime expansion |
| A16 a second consequential question is a separate record | PASS | question/driver test checks second question requires separate record and invocation |

The selected owner also verifies the compact carrier fields, exact terminal
values, project-owned reference-only boundary, and no new ADR authority.

## Deterministic integrity and test results

- Required detector: `uv run --frozen pytest tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree` ? PASS, 1 passed.
- Focused semantic and routing command: `uv run --frozen pytest -q tests/test_project_shaping_foundation.py tests/test_direction_foundation.py::test_direction_workflows_are_routed_and_versioned` ? PASS, 28 passed (27 selected-owner tests plus the existing router test).
- `uv sync --frozen`: PASS; 25 packages checked.
- Full `uv run --frozen pytest`: PASS, 815 passed, 88 existing `pathspec` deprecation warnings, 73.36 seconds.
- `uv run --frozen python scripts/maintainer_resume.py`: PASS after CURRENT was updated; it reports the candidate complete, authorization YES, and the exact next owner-review gate.
- `git diff --check`: PASS after CURRENT and this checkpoint were written; only Git line-ending notices were emitted.

## Clean-source smoke evidence

The temporary proof checkout began at `f16fd50f93452f9f38a892d58fdad7c67f3bbcd8` and contained the exact six
candidate paths above plus baseline repository bytes. The disposable synthetic
commit was `1d10fada3bbf60e2e0e86954e422360da11866f3`; it existed only outside the real checkout and
was removed with the temporary fixture.

The clean proof run asserted that `planning_lite` imported from the temporary
checkout's `src/planning_lite/` path, then ran:

- `uv run --frozen python scripts/test_template_update.py` ? PASS. Temporary
  adoption and consumer Doctor both passed.
- `uv run --frozen python scripts/test_local_only_update.py` ? PASS. The
  v4.2.0-to-current local-only update preserved project files and consumer
  Doctor passed.

The scripts reused already-installed local dependencies with synchronization
disabled because a fresh temporary environment could not retrieve build
requirements through the environment's TLS certificate chain. This did not
change the source under test: the CLI module import was explicitly verified to
resolve inside the clean synthetic checkout. Both smoke scripts passed.

REAL_HEAD_BEFORE_AND_AFTER: `f16fd50f93452f9f38a892d58fdad7c67f3bbcd8` / unchanged  
REAL_INDEX_BEFORE_AND_AFTER: EMPTY / unchanged  
REAL_STAGE: NO  
REAL_COMMIT: NO  
REAL_PUSH: NO

## State receipt and remaining gates

IMPLEMENTATION_CANDIDATE_STATE_ID: `ad347dd572762dc3538d60e9e2515e9cd6918991995e1e5e8f81c99d70eb6c06`  
IMPLEMENTATION_CANDIDATE_STATE_METHOD: SHA-256 of canonical UTF-8 JSON with
sorted keys and compact separators over `base_candidate_state_id` and sorted
`path_sha256_rows` for the six candidate paths above.  
EXIT_CURRENT_SHA256: `23606cd577de4ae4db93c8945cff9410bc0d09d09d9c87deff3439e7f8e778da`  
EXIT_AUTHORITY_STATE_ID: `1e8bb82627e78d33348dd0a98234f497ab6cfc3b0730e7cd639d5a4ded11e78f`  
EXIT_AUTHORITY_STATE_METHOD: SHA-256 of canonical UTF-8 JSON with sorted keys
and compact separators over `previous_authority_state_id`,
`candidate_state_id`, `current_sha256`, and `source_path_sha256_rows` below.  
EXIT_UNRELATED_DIRT_STATE_ID: `2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821` (preserved)  
EXIT_SYNC_STATE_ID: NOT REPRODUCIBLE BY CURRENT TOOLING  
EXIT_HEAD: `f16fd50f93452f9f38a892d58fdad7c67f3bbcd8` (unchanged)  
INDEX_EMPTY: YES; STAGE: NO; COMMIT: NO; PUSH: NO

| Authority source path | Canonical-LF SHA-256 |
|---|---|
| `copier.yml` | `92d9460e25a2178f3ada6d8badce9eb1c9aa2ca94765d374385885be752cb8ad` |
| `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-CHANGE-DEFINITION-v2.md` | `03b27174696ee828db9ac431d70194621e9ccf50d278bc1530e55ba3bfc1ced3` |
| `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-FORMAL-READINESS-VERDICT-v2.md` | `8d80a97ab699168841c81a5ef9f0f552c6beca0569eb9de2073d37dd239fd680` |
| `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-IMPLEMENTATION-PLAN-AMENDMENT-v1.md` | `1c72dc11731ee9be9f5890e1d9b0fff76a3b56577828bb53fe873015c0099073` |
| `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-IMPLEMENTATION-PLAN-v2.md` | `f8b7f53e0894932ad00583b46a80180f29a387eb42089f7c8f6c2bf145cfeffa` |
| `scripts/maintainer_resume.py` | `80ea9cb61498cc647f76a881c71b0003964f9d439cf33264fc572f565bb85a2d` |
| `scripts/test_local_only_update.py` | `6d3b3dc3bfb9fe6317619f04ed5553556fb8268ba4e273af1194d56b489333b6` |
| `scripts/test_template_update.py` | `0bf1541bfb3f80e4654512f0a8474f20c8c6542f25073faedb01a1fe4ca527e7` |
| `template/.planning/control/ARCHITECTURE_DECISION_FLOW.md` | `b27589d21b7179f6e7024d57846fb65f15c24735f979c654bc6b7062514dc93c` |
| `template/.planning/control/ROOT_ROUTER.md` | `7c17a3a9559b96dc9ad50201d8fd6a94f3737b3ed85d093cbe3cb47ce6805fed` |
| `template/.planning/docs/MANIFEST_V4.md` | `e9f39bf28f4d84ce05b50758d3dc2978e02d8302e465151a771e41c7c6edb258` |
| `template/.planning/framework/OWNERSHIP.yml` | `df9013d773cd1b5d433354dd82ba45e517835b1b92d3ce565260a6d496ac80ff` |
| `template/.planning/framework/SHA256SUMS.txt` | `ab1dd8c0dff2fa013e63b53aacc81babfaa51e295bc4e1a5b1d60f444a3c5bef` |
| `template/.planning/project/ARCHITECTURE_OVERVIEW.md` | `cb19d508b35781b36a0f7480699bf454d96ee783cf50606bcd0267a062c179b5` |
| `tests/test_direction_foundation.py` | `69f46fdc3254f096b9d0c2deb1e68f32671794e6e044dbc97e4657df0d3ed094` |
| `tests/test_project_shaping_foundation.py` | `b02b7f1a073e10f7c854d41d25c2026935a598fe363c857469a4376ebe85ff50` |

FIELD_PROOF: NOT EXECUTED; subject remains
`CONTEXT_MEMORY_ARCHITECTURE_FOR_FIRST_SEQUENTIAL_POST_MVP_TRUNK_FLOW`.  
P-05: OPEN / MATERIAL_PRE_09_G_BLOCKER; unchanged.  
09-G: NOT STARTED; unchanged.  
09-B parent: OPEN / PARTIALLY DESIGNED; unchanged.  
ROADMAP: unchanged.  
OPEN_MATERIAL_IMPLEMENTATION_FINDINGS: NONE.  
NEXT_SINGLE_GATE: `OWNER_REVIEW_PL_V39_09_MINIMAL_ARCHITECTURE_DECISION_FLOW_MVP_IMPLEMENTATION_AND_AUTHORIZE_FIELD_PROOF`.
