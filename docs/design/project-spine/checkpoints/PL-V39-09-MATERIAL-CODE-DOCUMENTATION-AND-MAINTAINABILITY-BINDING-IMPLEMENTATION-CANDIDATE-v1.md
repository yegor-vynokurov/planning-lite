# Implementation Candidate: Material Code Documentation and Maintainability Binding

## Decision and scope

Change: CHG-PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-001

Owner implementation authorization: OWNER_AUTHORIZE_MATERIAL_CODE_DOCUMENTATION_AND_MAINTAINABILITY_BINDING_IMPLEMENTATION_AFTER_INTEGRITY_CORRECTION / CONSUMED

Definition v1 SHA-256: 4eba43b069348750bd860441866b8c6f09ac7a17d36d547e1895b6110eaf89a6
Plan v1 SHA-256: a1e0f00e2b48333ba01ec526a06fce20c472a887c61999dfc9ede21acf1db204
Plan Amendment v1 SHA-256: 5e9b2bc6c22391b6ca7280cb20cddaf50e7aff071cd04fba4080514fed7f39f5
Formal Readiness v2 SHA-256: 26dc61953026a51742d9b5d1c4f6eb6bff9122d2a1eefd716ed97c7e890b0af8

Entry baseline:

- HEAD: 7bbf5937094484b074d20224aadb370c0d3ae493
- Authority state: 3b8fb80d21f48df2ad1301b9444f4b67a8525ea9c9dbfebdc53032d11b54fe6c
- Governance candidate state: cb758806cafc30458aaa6207073f69d4f49ad314cacd9826e4f997eeafc322df
- CURRENT canonical-LF SHA-256: 18897ade6e3063d5f9711cacd8253116d56892b55b3cfc66a3840df265435be8
- Unrelated dirt: 14 paths / 2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821
- Index: no staged changes

## Effective candidate surface

Exactly nine paths are bound below. No additional product, template, or test path was changed by this Change. MANIFEST_V4.md remains byte-identical. The 14 unrelated dirty paths remained byte-identical.

| Candidate path | Worktree byte SHA-256 | Canonical-LF SHA-256 | EOL |
|---|---|---|---|
| template/.planning/control/CHANGE_CLOSURE.md | ed9daef8e80e508ab4978180d0088393f77975eec5da557ad3dfb2bde090c6cf | 54c98ae2651bf55df1e07760d19d8b264c7c3f042e943d48e35b8d3f201cafc1 | CRLF |
| template/.planning/control/CHANGE_EXECUTION.md | 6158ee36a9a200c15f1e5dd979e635702b77be4cef6165592a5735af639415f0 | 357044a097f5177d41355145e57d15407a342534f477965fe3d9e71a06562da7 | CRLF |
| template/.planning/control/CHANGE_PLANNING.md | c5aa1a939be9c3c921048a4b906f9a3acc025b115603bfbf19dc922aef8df078 | eb1602961f26ea6a495bc5d30501abedf72d71fe94e8cffef3585a1c381fd4d0 | CRLF |
| template/.planning/control/CHANGE_READINESS.md | 25f2875dd53a272275e89535698ed53badb7f6c69f660b798e26363633a0bc31 | 6d80f0abb4b8f03398522cae1a309850c74fac1c70acb8cedeb7128b240e751e | CRLF |
| template/.planning/disciplines/CODEBASE_DESIGN.md | a5b9eb311de4ff5f033d75efe34beefa4107c99abe31873ec3e6973f2ab68d46 | 237f5ebd9cc83122231b20ae8b2553c331051597c48077965e8e71dd5b10c3ac | CRLF |
| template/.planning/disciplines/CODE_REVIEW.md | 329ecd6c4604f98629d3249010c38d56323beb475bc2edc1f5e8971843bb13b3 | 9c2528fdfc79ccece5d3b1ed491ce2ad83f69a61ccb1f8d5f56e5cf7c191e6ff | CRLF |
| tests/test_field_control_pack_foundation.py | 5cc2b64e6587669b29c46307b4490fdd57630d17b8f95fb70d7cae6b640711d4 | 0b09397c728098aa72b6262f0cbdea4e879ddaa5180010537e54a9612edf03f7 | CRLF |
| template/.planning/docs/MANIFEST_V4.md | e9f39bf28f4d84ce05b50758d3dc2978e02d8302e465151a771e41c7c6edb258 | e9f39bf28f4d84ce05b50758d3dc2978e02d8302e465151a771e41c7c6edb258 | LF |
| template/.planning/framework/SHA256SUMS.txt | 6faeb22c9aea9f8900350ef8a9f8fa1af10f8f65b5620b60c1dd1c7934ac1b4e | 6faeb22c9aea9f8900350ef8a9f8fa1af10f8f65b5620b60c1dd1c7934ac1b4e | LF |

The six semantic template files and the focused test use CRLF worktree bytes. MANIFEST_V4.md and SHA256SUMS.txt use LF. Candidate identity uses exact raw worktree bytes; canonical-LF identities are recorded separately.

## Semantic change

CODEBASE_DESIGN.md is the single normative owner for MATERIAL_CODE_CONTRACT and concrete maintainability semantics. It defines bounded applicability triggers, legal no-doc cases, appropriate nearby source documentation, semantic adequacy, rejection of tautological, generic, misleading, or contradictory text, same-Change updates for changed material contracts, prospective-only treatment of existing debt, and evidence-triggered performance optimization.

Planning records YES/NO and a concrete obligation or reason. Readiness independently checks classification, scope, determinacy, and review route. Execution conditionally loads CODEBASE_DESIGN for approved YES before or during dependent generation and routes newly discovered material contracts through amendment before dependent code. CODE_REVIEW remains a procedure and checks applicability, source-document presence and adequacy, consistency, and maintainability. Closure keeps the review path observable. No runtime schema or ordinary execution-guidance projection was added.

Focused F01-F16 tests cover these semantic relationships without freezing paragraph layout. tests/test_execution_guidance.py remained unchanged and ordinary execution guidance still projects discipline_refs == [].

## Integrity and focused verification

- Actual template tree: 167 paths.
- MANIFEST_V4.md entries: 167; path set equals the tree.
- MANIFEST_V4.md raw SHA-256: e9f39bf28f4d84ce05b50758d3dc2978e02d8302e465151a771e41c7c6edb258; byte-identical to entry.
- SHA256SUMS.txt covers the other 166 paths; its path set and canonical-LF digests match the template tree.
- F01-F16 focused acceptance: PASS; tests/test_field_control_pack_foundation.py, 39 passed.
- Integrity owner test: PASS; tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree.
- Execution-guidance regression: PASS; tests/test_execution_guidance.py::test_contract_route_projects_contract_closure_and_zero_discipline_is_explicit.

## Disposable consumer field proof

Consumer type: one disposable, isolated Planning Lite consumer adopted from the exact candidate source.
Field Change: CHG-0001-player-count-parser
Selector path: approved Plan YES -> Execution-loaded CODEBASE_DESIGN -> CODE_REVIEW Pass 2.

- S01_PLANNING: PASS. The semantic Plan selected MATERIAL_CODE_CONTRACT: YES and named the public parser symbol, accepted grammar and failure meaning, adjacent Python docstring location/form, and test/review route.
- S02_READINESS: PASS. Readiness independently compared the YES classification with the public callable, non-obvious grammar, and failure semantics.
- S03_EXECUTION: PASS. Before source generation, Execution loaded the consumer CODEBASE_DESIGN because of the approved YES marker. Direct workflow trace: 2026-10-01T17:31:47.011Z; loaded source worktree SHA-256 a5b9eb311de4ff5f033d75efe34beefa4107c99abe31873ec3e6973f2ab68d46.
- S04_CLOSURE: PASS. Closure preparation selected CODE_REVIEW; Pass 2 applied the same CODEBASE_DESIGN standard. Selector evidence and review outcome evidence were recorded separately.

The bounded parser accepts one ASCII character from 1 through 9, raises ValueError for invalid strings and TypeError for non-string values, and documents that contract nearby. The tiny private _is_ascii_digit helper has no docstring and owns no hidden contract. Its 23 focused behavior cases passed.

| Mutant | Valid | Expected | Observed | Detector | Rule owner | Selector path |
|---|---|---|---|---|---|---|
| M0_GOOD_MATERIAL_DOC | YES | PASS | PASS | Semantic adequacy | CODEBASE_DESIGN | Approved YES -> Execution load -> CODE_REVIEW Pass 2 |
| M1_MISSING_MATERIAL_DOC | YES | FAIL | FAIL | Required nearby source-document presence | CODEBASE_DESIGN | Approved YES -> Execution load -> CODE_REVIEW Pass 2 |
| M2_TAUTOLOGICAL_DOC | YES | FAIL | FAIL | Semantic adequacy; generic text does not state the contract | CODEBASE_DESIGN | Approved YES -> Execution load -> CODE_REVIEW Pass 2 |
| M3_CONTRADICTORY_DOC | YES | FAIL | FAIL | Contradiction with behavior/invariant | CODEBASE_DESIGN | Approved YES -> Execution load -> CODE_REVIEW Pass 2 |
| M4_TRIVIAL_PRIVATE_NO_DOC | YES | PASS | PASS | Bounded trivial/private no-doc exemption | CODEBASE_DESIGN | Approved YES -> Execution load -> CODE_REVIEW Pass 2 |

M0-M4 overall: PASS for this evaluator-operated bounded case. This does not claim general model reliability, automatic semantic-documentation judging, a success rate, or universal documentation quality.

## Clean-source and update proof

Disposable clean proof checkout: C:/Users/yegor/AppData/Local/Temp/pl-v39-09-doc-maint-d90446a1f61642158087201623840b57/source
Exact candidate synthetic local commit: 19d13186a7d7684686f7ce365f2cb91f6c921b21
The temporary commit was created only in that disposable checkout. It did not change central HEAD or stage central paths. The proof source was clean after commit and its nine candidate worktree bytes matched this candidate manifest.

- scripts/test_template_update.py from the clean proof source: PASS; temporary consumer adoption and Doctor passed.
- scripts/test_local_only_update.py from the clean proof source: PASS; v4.2.0 to local-only update passed, Doctor passed, and project-owned sentinels remained unchanged.
- Additional disposable consumer adoption and Doctor: PASS. Consumer: C:/Users/yegor/AppData/Local/Temp/pl-v39-09-doc-maint-d90446a1f61642158087201623840b57/consumer. The Codex profile was explicitly selected and committed as disposable-consumer setup after adoption.
- uv sync --frozen: PASS; 25 packages checked.
- uv run --frozen pytest: PASS; 833 passed, 88 existing warnings. The warnings were 44 each at the two existing pathspec GitWildMatchPattern deprecation sites in tests/test_field_control_pack_foundation.py; no new warning category.

## Candidate state and exit receipt

IMPLEMENTATION_CANDIDATE_STATE: exact raw worktree-byte map of the nine effective candidate paths below.
IMPLEMENTATION_CANDIDATE_STATE_ID: 6172007b1bbb9119bd8f80e36ee74e73319fd19e5b730cf99649a69153bd638d
IMPLEMENTATION_CANDIDATE_STATE_METHOD: SHA-256 of canonical UTF-8 JSON with sorted keys and compact separators over an object mapping each exact repository-relative candidate path to its raw worktree SHA-256.
WORKTREE_BYTE_ID: each raw digest in the nine-path manifest above.
CANONICAL_LF_BYTE_ID: each canonical-LF digest in the nine-path manifest above.
EOL_CLASSIFICATION: CRLF for semantic template/test files; LF for MANIFEST_V4.md and SHA256SUMS.txt.

EXIT_HEAD: 7bbf5937094484b074d20224aadb370c0d3ae493 / UNCHANGED
EXIT_CURRENT_CANONICAL_LF_SHA256: 422b04f43590476b898cf860381edfe13cb735d8006d7ceba9b2536813df455a
EXIT_AUTHORITY_STATE_ID: 9d62a0f39218f6e1d55ec72c9e4ec56105add92433382e7a8a33d075d71452c2
EXIT_AUTHORITY_STATE_ID_METHOD: SHA-256 of canonical UTF-8 JSON with sorted keys and compact separators over previous_authority_state_id, candidate_state_id, current_sha256, and sorted source_path_sha256_rows represented as [path, canonical-LF-sha256] pairs. CURRENT is represented separately by current_sha256. This checkpoint is excluded from its own authority digest.
EXIT_CANDIDATE_STATE_ID: 6172007b1bbb9119bd8f80e36ee74e73319fd19e5b730cf99649a69153bd638d
EXIT_UNRELATED_DIRT_PATHS: 14
EXIT_UNRELATED_DIRT_STATE_ID: 2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821 / PRESERVED
EXIT_SYNC_STATE_ID: NOT_REPRODUCIBLE_BY_CURRENT_TOOLING
EXIT_INDEX_EMPTY: YES
STAGE: NO
COMMIT: NO
PUSH: NO
RELEASE: NO
T-07: NOT AUTHORIZED
SEQUENTIAL_WHOLE_ORGANISM_PROOF: NOT STARTED
09-G: NOT STARTED
OPEN_MATERIAL_FINDINGS: NONE
NEXT_SINGLE_GATE: OWNER_REVIEW_MATERIAL_CODE_DOCUMENTATION_AND_MAINTAINABILITY_BINDING_IMPLEMENTATION_AND_FIELD_PROOF

The 29 authority source rows are sorted by repository path and use canonical-LF hashes:

| Authority source path | Canonical-LF SHA-256 |
|---|---|
| copier.yml | 92d9460e25a2178f3ada6d8badce9eb1c9aa2ca94765d374385885be752cb8ad |
| docs/design/project-spine/checkpoints/PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-CHANGE-DEFINITION-v1.md | 4eba43b069348750bd860441866b8c6f09ac7a17d36d547e1895b6110eaf89a6 |
| docs/design/project-spine/checkpoints/PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-FORMAL-READINESS-VERDICT-v1.md | a4f6c3a54bfa7386745a417f8f57368db36988ad902c5c84b50e001f114bc0ea |
| docs/design/project-spine/checkpoints/PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-IMPLEMENTATION-PLAN-AMENDMENT-v1.md | 5e9b2bc6c22391b6ca7280cb20cddaf50e7aff071cd04fba4080514fed7f39f5 |
| docs/design/project-spine/checkpoints/PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-IMPLEMENTATION-PLAN-v1.md | a1e0f00e2b48333ba01ec526a06fce20c472a887c61999dfc9ede21acf1db204 |
| docs/design/project-spine/checkpoints/PLANNING-LITE-CODE-DOCUMENTATION-AND-MAINTAINABILITY-VITALITY-CHALLENGE-v1.md | a337a1c7ef947ab423d6c81a57ac61b12f93b6420d084391a92a920d3c5acf18 |
| docs/design/project-spine/roadmap/ROADMAP.md | 056933c1116e3adbaf2330baba32718498aa5cf2f88eb4ea1ef576433392f0bc |
| scripts/maintainer_resume.py | 80ea9cb61498cc647f76a881c71b0003964f9d439cf33264fc572f565bb85a2d |
| scripts/test_local_only_update.py | 6d3b3dc3bfb9fe6317619f04ed5553556fb8268ba4e273af1194d56b489333b6 |
| scripts/test_template_update.py | 0bf1541bfb3f80e4654512f0a8474f20c8c6542f25073faedb01a1fe4ca527e7 |
| src/planning_lite/execution_guidance.py | 7a7c7a0c96f3dd3d9f2d21c7453b156e7c34d00513ae0a0589d0ecc3f71bd33e |
| template/.planning/changes/templates/plan.md | 251e6148258e865bf20f854bdbb95016f6cd1197d4865e9d4dfcf3a723f56703 |
| template/.planning/control/CHANGE_CLOSURE.md | 54c98ae2651bf55df1e07760d19d8b264c7c3f042e943d48e35b8d3f201cafc1 |
| template/.planning/control/CHANGE_EXECUTION.md | 357044a097f5177d41355145e57d15407a342534f477965fe3d9e71a06562da7 |
| template/.planning/control/CHANGE_PLANNING.md | eb1602961f26ea6a495bc5d30501abedf72d71fe94e8cffef3585a1c381fd4d0 |
| template/.planning/control/CHANGE_READINESS.md | 6d80f0abb4b8f03398522cae1a309850c74fac1c70acb8cedeb7128b240e751e |
| template/.planning/disciplines/CODEBASE_DESIGN.md | 237f5ebd9cc83122231b20ae8b2553c331051597c48077965e8e71dd5b10c3ac |
| template/.planning/disciplines/CODE_REVIEW.md | 9c2528fdfc79ccece5d3b1ed491ce2ad83f69a61ccb1f8d5f56e5cf7c191e6ff |
| template/.planning/docs/MANIFEST_V4.md | e9f39bf28f4d84ce05b50758d3dc2978e02d8302e465151a771e41c7c6edb258 |
| template/.planning/framework/OWNERSHIP.yml | df9013d773cd1b5d433354dd82ba45e517835b1b92d3ce565260a6d496ac80ff |
| template/.planning/framework/SHA256SUMS.txt | 6faeb22c9aea9f8900350ef8a9f8fa1af10f8f65b5620b60c1dd1c7934ac1b4e |
| template/.planning/modes/EXECUTE.md | 86334ad9146bb175a24fb742d12a1b305fc29727afc853705d1804cc3449dbef |
| template/.planning/modes/PLAN.md | 87d000a96a34e115de24c23eff4e2c9a82db13e04d7cc431c312f50eea457f71 |
| template/.planning/skills/planning-audit/SKILL.md | 2f0596b16cb6b7b36ff6a3a9ee07652258c7f7cf636d1476a1a5e18caba96283 |
| template/.planning/skills/planning-execute/SKILL.md | 0eb65e095de5e92ba9199eb039fd0361f3415b243de594d40d0578eee608bf4a |
| template/.planning/skills/planning-plan/SKILL.md | 03170663e2c080df19f155cd483791cd06d4b5c7a5bf9fe7a4b879ddfbe49f19 |
| tests/test_direction_foundation.py | 69f46fdc3254f096b9d0c2deb1e68f32671794e6e044dbc97e4657df0d3ed094 |
| tests/test_execution_guidance.py | 91338fe086c8475bb042d6e3d6105094b4d7ce551dccab5903bbc51f18da3fa5 |
| tests/test_field_control_pack_foundation.py | 0b09397c728098aa72b6262f0cbdea4e879ddaa5180010537e54a9612edf03f7 |

The authority state uses previous_authority_state_id 3b8fb80d21f48df2ad1301b9444f4b67a8525ea9c9dbfebdc53032d11b54fe6c, candidate_state_id 6172007b1bbb9119bd8f80e36ee74e73319fd19e5b730cf99649a69153bd638d, and the final CURRENT canonical-LF digest above. No product, test, closeout, or release commit was made.
