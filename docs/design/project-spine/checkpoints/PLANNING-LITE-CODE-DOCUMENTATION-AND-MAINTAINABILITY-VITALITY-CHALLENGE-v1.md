# Planning Lite Code Documentation and Maintainability Vitality Challenge v1

```text
CHALLENGE_ID: PLANNING_LITE_CODE_DOCUMENTATION_AND_MAINTAINABILITY_VITALITY_CHALLENGE_V0_1
ENTRY_HEAD: 7bbf5937094484b074d20224aadb370c0d3ae493
ENTRY_GATE: OWNER_ADJUDICATION_FRESH_SESSION_SEQUENTIAL_WHOLE_ORGANISM_PROOF
P05_STATE: CLOSED / ADVERSARIAL_RECHALLENGE_PASS
RESULT: CODE_DOCUMENTATION_CAPABILITY PARTIAL / MAINTAINABILITY_CAPABILITY LIVE_NARROW
FIRST_BROKEN_SEAM: POLICY_TOO_VAGUE
IMPLEMENTATION_AUTHORIZED: NO
SEQUENTIAL_WHOLE_ORGANISM_PROOF: NOT STARTED / NOT AUTHORIZED
09_G: NOT STARTED
CENTRAL_PRODUCT_CHANGED: NO
TEMPLATES_CHANGED: NO
TESTS_CHANGED: NO
ROADMAP_CHANGED: NO
STAGE: NO
COMMIT: NO
PUSH: NO
```

## Scope, method, and boundaries

This is a read-only central-source capability challenge. The only central writes were this checkpoint and the current-gate update in `docs/design/project-spine/CURRENT.md`. No central product, template, test, or Roadmap path was changed or staged. No central commit, push, release, or whole-organism proof was performed. The pre-existing 14 unrelated dirty paths were preserved.

The disposable consumer was adopted from a clean clone of central HEAD `7bbf5937094484b074d20224aadb370c0d3ae493`, not from the dirty central worktree. It is at `C:\Users\yegor\AppData\Local\Temp\planning-lite-doc-vitality-1e084a241b5e47a289c89e85863717f9\consumer`. The framework adoption and Planning records were committed only inside that disposable Git repository (`f26694d` and `9810f93`). The consumer Change `CHG-0001-retry-after-parser` introduced a pure Retry-After header parser and five focused tests. Its Definition, Plan, and task did not request docstrings or source documentation. The Plan's Documentation and operations section recorded no separate user, deployment, monitoring, or support material as affected. The contract itself was present in the Change Specification and Plan.

This was an evaluator-operated, unblinded field challenge, not an independent-agent reliability study. It is evidence about selector behavior, available standards, and this bounded review occurrence; it does not estimate success frequency across coding agents.

## D01–D10: live authority and selectors

| Question | Finding |
|---|---|
| D01. Where is documentation quality defined? | `template/.planning/project/DEFINITION_OF_DONE.md` asks for user, developer, deployment, monitoring, and support documentation to be updated where affected. `CHANGE_PLANNING.md` asks the Plan to cover documentation; `CHANGE_READINESS.md` says documentation is addressed where applicable. `CODEBASE_DESIGN.md` defines an interface as what callers must know, including inputs, outputs, invariants, errors, ordering, and configuration. None defines source-docstring applicability or semantic content. |
| D02. Where is maintainability defined? | `disciplines/CODEBASE_DESIGN.md` defines modules, interfaces, seams, adapters, orchestrators, and locality; it prefers thin orchestrators, deep modules, explicit seams, and local reasoning. `disciplines/CODE_REVIEW.md` selects maintainability and repository conventions for standards review. |
| D03. Which workflow selects each rule during Planning? | `ROOT_ROUTER.md` selects one mode, workflow, and only-needed discipline. `modes/PLAN.md` and `CHANGE_PLANNING.md` select `CODEBASE_DESIGN.md` for architectural or structural work, and `DELIVERY_SLICES.md` for task decomposition. The disposable new public leaf module was treated as structural, so `CODEBASE_DESIGN.md` was loaded. Its interface/design contract was carried into the Plan, but it supplied no source-document obligation. |
| D04. Which workflow selects each rule during Readiness? | `planning-audit/SKILL.md` routes to one audit workflow. `CHANGE_READINESS.md` asks whether documentation is addressed where applicable; the managed `RUN_FORMAL_READINESS` projection selects that workflow with `discipline_refs: []`. It provides no concrete documentation-quality test. |
| D05. Which workflow selects each rule during code-writing Execution? | `planning-execute/SKILL.md` selects `modes/EXECUTE.md`, `CHANGE_EXECUTION.md`, ACTIVE, context, approval gates, and the mode output contract. `CHANGE_EXECUTION.md` requires the approved Plan and exact task envelope. The live `EXECUTE_AUTHORIZED_TASK` guidance result was `MATCHED`, route `CHANGE_EXECUTION_V1`, skill `planning-execute`, procedure `CHANGE_EXECUTION.md`, and `discipline_refs: []`. The precondition refs include `CHANGE_PLANNING.md` and `APPROVAL_GATES.md`, but neither selects a material source-document standard. Execution could proceed without loading one. |
| D06. Which workflow selects each rule during review/Closure? | `planning-audit/SKILL.md` loads `CODE_REVIEW.md` for code/completion review; `CHANGE_CLOSURE.md` requires separate spec and standards passes. Pass 2 checks the Definition of Done, interfaces, tests, and maintainability. This is a manual generic review, not a source-document checklist or semantic docstring detector. The field reviewer caught the direct M3 contradiction but did not reject M1/M2 under the selected standard. |
| D07. Is there one canonical owner for code-documentation quality? | No. General documentation is in Definition of Done; interface and maintainability design is in CODEBASE_DESIGN; selection is spread across Planning, Readiness, and Closure. No one source owns source-code documentation quality. |
| D08. Is docstring applicability explicit anywhere? | No. No current live rule says when a material public, state, persistence, authorization, or concurrency boundary requires a source docstring or another specific code-adjacent document. |
| D09. Is semantic docstring quality explicit anywhere? | No. There is no explicit test that distinguishes a present string from a material interface contract, or that checks documentation against behavior, side effects, failure, persistence, locking, or authorization semantics. A human can notice an obvious contradiction. |
| D10. Can coding Execution legally proceed without loading a concrete documentation-quality standard? | Yes. The ordinary execution route matched with no discipline refs. The approved Plan and Specification carried behavior details, but the route did not require a code-documentation quality standard before or during generation. |

### Actual references and test evidence

The exact live surfaces inspected were:

- `template/.planning/control/CHANGE_PLANNING.md`, `CHANGE_READINESS.md`, `CHANGE_EXECUTION.md`, `CHANGE_CLOSURE.md`, `CHANGE_DEFINITION.md`, `CHANGE_SCAFFOLD.md`, `CHANGE_LIFECYCLE.md`, `APPROVAL_GATES.md`, `ROOT_ROUTER.md`, `MODE_ROUTER.md`, `EXECUTION_ROUTING.md`, and `CONTEXT_POLICY.md`;
- `template/.planning/disciplines/CODE_REVIEW.md` and `CODEBASE_DESIGN.md`;
- `template/.planning/skills/planning-plan/SKILL.md`, `planning-audit/SKILL.md`, `planning-execute/SKILL.md`, and `planning-git-review/SKILL.md`;
- `template/.planning/modes/PLAN.md`, `AUDIT.md`, and `EXECUTE.md`; the active adapter/profile and `PROJECT_RULES.md` / `DEFINITION_OF_DONE.md`;
- `src/planning_lite/execution_guidance.py` and `tests/test_execution_guidance.py`.

`tests/test_execution_guidance.py::test_contract_route_projects_contract_closure_and_zero_discipline_is_explicit` asserts that ordinary execution has an empty `discipline_refs` list while the separate contract task route selects only `CONTRACT_CLOSURE.md`. `tests/test_field_control_pack_foundation.py` checks route identities and skill surfaces, not code-documentation selection. A targeted search of `template/`, `src/`, `tests/`, `scripts/`, and `pyproject.toml` found no docstring policy, pydocstyle rule, docstring coverage rule, or docstring-specific test.

The field's actual readiness projection matched `RUN_FORMAL_READINESS` / `FORMAL_READINESS_V1` with no discipline refs. Its ordinary execution projection matched `EXECUTE_AUTHORIZED_TASK` / `CHANGE_EXECUTION_V1` with no discipline refs. The execution agent had the approved Plan and Specification, not a concrete code-documentation standard.

## Phase B: AST inventory

Inventory method: parse every `src/planning_lite/**/*.py` file with Python `ast`; count all `ClassDef`, `FunctionDef`, and `AsyncFunctionDef` nodes, including nested definitions. A function/method is counted public when its name does not start with `_`, otherwise as a private helper. A docstring is the AST first-statement docstring; one-line/multi-line is based on `splitlines()` count.

```text
SOURCE_MODULE_COUNT: 26
MODULES_WITH_MODULE_DOCSTRING: 15
CLASS_COUNT: 117
CLASS_WITH_DOCSTRING_COUNT: 53
FUNCTION_METHOD_COUNT: 737
PUBLIC_FUNCTION_METHOD_COUNT: 246
PRIVATE_HELPER_COUNT: 491
FUNCTION_METHOD_WITH_DOCSTRING_COUNT: 116
ONE_LINE_DOCSTRING_COUNT: 95
MULTI_LINE_DOCSTRING_COUNT: 21
FUNCTION_METHOD_WITHOUT_DOCSTRING_COUNT: 621
```

The counts are descriptive only; they are not a coverage target. The material-symbol assessment is targeted, not a universal coverage score.

| Module | Module docstring | Classes with docstrings / all classes | Functions/methods | Public / private | Functions/methods with docstrings |
|---|---:|---:|---:|---:|---:|
| `__init__.py` | Yes | 0/0 | 0 | 0/0 | 0 |
| `attempt_evaluation.py` | Yes | 7/19 | 82 | 41/41 | 14 |
| `attempt_runtime.py` | Yes | 10/12 | 58 | 23/35 | 15 |
| `authorization.py` | Yes | 1/7 | 22 | 9/13 | 6 |
| `campaign/__init__.py` | Yes | 0/0 | 0 | 0/0 | 0 |
| `campaign/attempt_reconciliation.py` | No | 1/1 | 5 | 2/3 | 1 |
| `campaign/campaign.py` | No | 1/11 | 57 | 22/35 | 2 |
| `campaign/campaign_completion.py` | No | 1/4 | 24 | 7/17 | 1 |
| `campaign/campaign_suite.py` | No | 1/2 | 15 | 4/11 | 2 |
| `campaign/candidate_review.py` | No | 1/3 | 18 | 5/13 | 2 |
| `campaign/cli.py` | No | 0/0 | 5 | 3/2 | 0 |
| `campaign/independent_review.py` | No | 1/3 | 19 | 4/15 | 1 |
| `campaign/review_receipt.py` | No | 1/4 | 25 | 7/18 | 1 |
| `cli.py` | No | 1/2 | 67 | 25/42 | 5 |
| `codex_work_window.py` | Yes | 2/4 | 28 | 2/26 | 2 |
| `context.py` | Yes | 3/3 | 54 | 11/43 | 5 |
| `execution_guidance.py` | Yes | 3/3 | 20 | 5/15 | 4 |
| `governed_executor.py` | Yes | 4/4 | 23 | 9/14 | 4 |
| `local_update.py` | No | 1/4 | 21 | 8/13 | 5 |
| `operation_lifecycle.py` | Yes | 3/4 | 30 | 4/26 | 2 |
| `operation_trace.py` | Yes | 3/3 | 21 | 8/13 | 5 |
| `plan_compilation.py` | Yes | 4/10 | 38 | 11/27 | 5 |
| `project_spine.py` | No | 1/4 | 18 | 2/16 | 2 |
| `telemetry.py` | Yes | 1/3 | 33 | 13/20 | 15 |
| `traversability.py` | Yes | 1/6 | 18 | 2/16 | 2 |
| `workspace.py` | Yes | 1/1 | 36 | 19/17 | 15 |

## Material-symbol sample

The sample includes the six requested modules plus `execution_guidance.py`, a finite routing selector exercised by current tests. A symbol is classified by whether a maintainer can recover its material contract from its source documentation without reverse-engineering implementation details; aesthetics and private-helper coverage are not scored.

| Symbol | Classification | Evidence-based reason |
|---|---|---|
| `context.build_compact_status` | GOOD_ENOUGH | Multi-line contract states its bounded read-only projection and what it does not select or persist. |
| `context.validate_handoff` | THIN_BUT_USABLE | States exact HandoffV1 validation and copy return, but not the rejection details. |
| `attempt_runtime.AttemptEnvelopeV1` | GOOD_ENOUGH | Class documentation describes persisted Attempt provenance, terminal result, and recovery authorization reference. |
| `attempt_runtime.AttemptStoreV1` | THIN_BUT_USABLE | Names canonical target-local store; exact shape remains in code/schema. |
| `attempt_runtime._store_lock` | GOOD_ENOUGH | Describes thread/OS lock coverage and why the sidecar is not a second state store. |
| `attempt_runtime.prepare_attempt` | GOOD_ENOUGH | Explains authorization-before-state and lock-protected lineage/ordinal allocation. |
| `attempt_runtime.claim_attempt` | THIN_BUT_USABLE | States exact ACTIVATABLE to IN_FLIGHT transition, but omits authorization re-resolution and failure behavior. |
| `attempt_runtime.terminalize_attempt` | GOOD_ENOUGH | Describes allowed terminalization, recovery separation, durable write protocol, and forbidden retry/reset behavior. |
| `attempt_runtime.resolve_interrupted_attempt` | GOOD_ENOUGH | Describes exact recovery authority and scope prerequisite. |
| `authorization.issue_authorization` | THIN_BUT_USABLE | States immutable issue and opaque-reference return, but not detailed scope/action failure semantics. |
| `authorization.issue_preparation_authorization` | MISSING_MATERIAL_DOC | Public security boundary with no symbol docstring; action/scope/provenance contract is not stated at the symbol. |
| `authorization.validate_preparation_applicability` | MISSING_MATERIAL_DOC | Security decision boundary with no docstring describing exact action/scope outcomes. |
| `authorization.resolve_authorization` | THIN_BUT_USABLE | States exact resolution is non-mutating, but not the complete resolution/failure contract. |
| `operation_lifecycle.execute_governed_operation` | THIN_BUT_USABLE | Gives the important operation order in one line; stop outcomes, persistence boundaries, and side effects need source inspection. |
| `plan_compilation.parse_task_table` | THIN_BUT_USABLE | States one bounded table grammar, but the exact grammar/failure cases are not summarized. |
| `plan_compilation.compile_plan` | THIN_BUT_USABLE | Identifies a derived compilation and the binding substitution, but only a small portion of the large result contract. |
| `telemetry._process_lock` | THIN_BUT_USABLE | Identifies cross-process serialization and sidecar lock, with limited crash/replay semantics. |
| `telemetry.validate_telemetry_record` | THIN_BUT_USABLE | Names strict dispatch over supported record families, but not rejection/failure outcomes. |
| `telemetry.read_work_window_registration` | MISSING_MATERIAL_DOC | Persistence read boundary with no symbol docstring describing identity and absent/malformed behavior. |
| `telemetry.read_resource_observation_for_window` | MISSING_MATERIAL_DOC | Persisted observation lookup boundary with no docstring describing scope/readback semantics. |
| `telemetry.append_resource_observation` | THIN_BUT_USABLE | States terminal persistence and replay serialization, but not full lock, identity, or failure rules. |
| `telemetry.collect_receipt` | THIN_BUT_USABLE | States input/ref injection/append, but not disabled, version, and validation failures. |
| `execution_guidance.select_operation_guidance` | THIN_BUT_USABLE | States exact route from one snapshot; the module doc supplies purity/authority boundaries, while selection outcomes are not summarized at the symbol. |

| Sample result | Count |
|---|---:|
| Material symbols sampled | 23 |
| GOOD_ENOUGH | 6 |
| THIN_BUT_USABLE | 13 |
| MISSING_MATERIAL_DOC | 4 |
| MISLEADING_OR_STALE in current sampled source | 0 |
| TRIVIAL_DOC_NOT_REQUIRED in this material sample | 0 |

Straight-through accessors and tiny validators were excluded rather than counted as debt. The zero stale count is limited to the sampled current symbols and does not imply a whole-repository guarantee.

## Phase C: documentation quality model

The requested dimensions are not installed as policy by this challenge. Current CODEBASE_DESIGN covers some caller-known interface information generally, but neither it nor CODE_REVIEW defines a source-document content contract. In particular, no selected rule requires a material source document to state purpose, authoritative inputs, output/state change, failure semantics, side effects, persistence, lock behavior, authorization assumptions, or plausible non-goals. Existing prose may describe some of these in an individual docstring; there is no consistent policy or quality test.

The DoD's “documentation ... updated where affected” rule is broad and can motivate human judgment. It does not state whether a public API needs a docstring, where documentation must live, or how to reject a tautology while accepting concise useful prose.

## Phase D: routing and selection vitality

| Stage | Current requirement selection | Field observation |
|---|---|---|
| Definition | ABSENT for source-document quality; interfaces/invariants are captured generally. | Retry-After behavior was defined; there was no code-documentation criterion. |
| Planning | INDIRECTLY_REFERENCED. The Plan template has a Documentation and operations section; structural Planning loads CODEBASE_DESIGN. | The public function and behavior were concrete, but the Plan created no material source-document obligation. |
| Readiness | INDIRECTLY_REFERENCED. Docs are addressed “where applicable”; no specific doc evidence/test exists. | Readiness marked the scope Ready without a testable source-doc criterion. |
| Execution | ABSENT as a concrete doc-quality standard. The task/Plan is selected; ordinary Operation Guidance has `discipline_refs: []`. | Code writing legally proceeded from approved behavior and envelope with no source-doc standard loaded. The implementation had no docstring. |
| Review / Closure | INDIRECTLY_REFERENCED through CODE_REVIEW Pass 2 and the general DoD documentation category. | Manual review killed an outright false side-effect claim, but no selected rule rejected absence or a tautology. |

An ordinary coding Change can legally execute without any concrete source-documentation standard. The first broken seam is upstream: **POLICY_TOO_VAGUE**. Later gaps include missing execution binding and semantic quality detection.

## Phase E: disposable field challenge and adversarial mutants

The actual current route was followed in the isolated consumer: Definition, Plan approval, Readiness, direct execution authorization, Execution, focused tests, and manual two-pass review preparation. The task asked for a pure parser and focused tests without a documentation instruction. The Plan recorded the interface contract in the Change records but did not create a source-doc obligation. The five tests passed for the initial implementation and each mutant.

| Mutant | Valid challenge candidate? | Killed? | Detector and result |
|---|---|---|---|
| M1 — no function docstring | YES | NO | None. The accepted Specification/Plan carry the behavior contract, and current selected standards do not require the contract to be repeated at the source symbol. The AST observation showed no docstring; neither focused tests nor the current review route rejected it. Source SHA-256: `e164783df66604938ea8b101b99aed5f954fabf92852c72450e672569c2f762b`. |
| M2 — docstring “Process the data.” | YES | NO | None. Tests remained green; current rules do not distinguish DOCSTRING_PRESENT from MATERIAL_CONTRACT_DOCUMENTED. No semantic docstring detector was selected. Source SHA-256: `7fdf78f918f000289e59b12b6d68c264d6bdefc00b42344d327df3b5446b2de6`. |
| M3 — docstring says it persists to retry-settings.json | YES | YES | Manual CODE_REVIEW Pass 2: direct comparison of the docstring with the implementation and pure-function Specification exposed a false persistence claim. This is human review, not an automated or docstring-specific detector. Tests remained green. Source SHA-256: `193fd38631f224f520bef936e1daff11ce9aabc5710d71b57ced110bf68af186`. |

The no-docstring baseline was restored after the mutations. The focused consumer suite passed: 5 tests. No mutation or field code was copied into the central source repository. Because the challenge was unblinded, the M3 manual detection proves that an attentive selected reviewer can catch an obvious contradiction in this instance; it does not prove repeatable semantic-quality detection.

## Maintainability capability

`CODEBASE_DESIGN.md` makes these maintainability ideas available: smallest coherent structure; clear module/interface ownership; thin orchestration; explicit seams; local reasoning and coupling signals; classify generic helpers precisely; do not invent architecture during execution. Planning selected it for this structural Change and the accepted Plan gave one pure leaf function, no helper hub, and no speculative abstraction. Execution was constrained by the Plan and envelope. CODE_REVIEW also selects maintainability at closure.

This supports **MAINTAINABILITY_CAPABILITY: LIVE_NARROW** for a bounded structural Change. It does not show that the design discipline is selected directly during ordinary Execution (`discipline_refs` was empty) or that all maintainability qualities have an executable detector. No performance need was present, and no performance optimization was requested or performed. Maintainability optimization is structural clarity and bounded ownership; it is not performance tuning. Avoid speculative performance requirements absent measured need.

## Adjudication

```text
CODE_DOCUMENTATION_CAPABILITY: PARTIAL
MAINTAINABILITY_CAPABILITY: LIVE_NARROW
FIRST_BROKEN_SEAM: POLICY_TOO_VAGUE
M1_VALID: YES
M1_KILLED: NO
M1_DETECTOR: NONE
M2_VALID: YES
M2_KILLED: NO
M2_DETECTOR: NONE
M3_VALID: YES
M3_KILLED: YES
M3_DETECTOR: MANUAL CODE_REVIEW PASS 2 COMPARISON WITH IMPLEMENTATION AND SPECIFICATION
WHOLE_ORGANISM_PROOF_CAN_RELY_ON_CURRENT_DOC_CAPABILITY: NO
```

Do not treat the closure-only human catch for M3 as an end-to-end documentation capability. The route let code generation proceed without a concrete quality standard, and M1/M2 survived the selected current checks.

## Minimum correction alternatives

| Option | Correction surface | Benefit | Limitation |
|---|---|---|---|
| A. Extend CODE_REVIEW only | Add explicit applicability and semantic-document checks to the existing review discipline. | Smallest late-stage addition; reuses selected completion review. | Does not bind quality before/during generation or make Readiness test it. |
| B. Extend CODEBASE_DESIGN and bind it to Execution | Use CODEBASE_DESIGN as the one normative owner for material source-document applicability/content; add thin conditional references from Planning, Readiness, Execution, and CODE_REVIEW/Closure. | Reuses its existing interface contract and maintainability owner; reaches the agent before code generation without duplicating the normative rules. | Requires several selector references and owner agreement that CODEBASE_DESIGN owns code documentation as well as structure. |
| C. Add a conditional CODE_DOCUMENTATION / CODE_QUALITY discipline | One dedicated normative standard with thin workflow references at all four stages. | Clearest distinct policy owner and source-document scope. | More framework surface and new selection behavior than reusing CODEBASE_DESIGN. |
| D. Extend the Definition of Done as owner | Make material developer-interface documentation and semantic adequacy explicit there; add a thin Execution reference. | Small extension to the existing generic documentation owner. | Definition of Done is a broad project-owned completion record, and by itself is selected too late; it needs workflow bindings and may not remain centrally managed in consumers. |

The smallest plausible correction recommended for owner review is **Option B**: expand the existing CODEBASE_DESIGN normative contract to cover when material code interfaces need nearby documentation and what material meaning it must preserve; add thin selectors so Planning creates an obligation, Readiness can test it, Execution loads it before/during generation, and CODE_REVIEW verifies it at Closure. Keep content proportional to materiality and permit concise prose; do not require rigid headings. The owner has not accepted this option, and no policy change is authorized by this challenge.

## Relation to the whole-organism proof and next gate

The proof should include a material source-document and maintainability acceptance dimension. The current documentation capability cannot be relied on to pass that dimension without false-pass risk: M1 and M2 survived, Execution selected no concrete documentation standard, and no semantic-quality detector exists. If the upcoming proof writes production code, adjudicate and implement a bounded correction first, then include a nearest-wrong documentation challenge in the proof. Do not begin the proof or 09-G now.

```text
RECOMMENDED_NEXT_GATE:
OWNER_ADJUDICATION_BOUNDED_CODEBASE_DESIGN_CORRECTION_BEFORE_FRESH_SESSION_SEQUENTIAL_WHOLE_ORGANISM_PROOF

IMPLEMENTATION_AUTHORIZATION:
NO
```

## Current-state receipt

```text
CURRENT_ENTRY_CANONICAL_LF_SHA256: 092e2510e07c7965be2f0791bcb39869417c4de6f2e28877e4eb426ba03de6d0
CURRENT_EXIT_CANONICAL_LF_SHA256: 9d6eb92e95d03f8a2b55d4c5b8178679d3a744cdc962dbf356fa0623e3de9764
CURRENT_NEXT_PERMITTED_ACTION: OWNER_ADJUDICATION_BOUNDED_CODEBASE_DESIGN_CORRECTION_BEFORE_FRESH_SESSION_SEQUENTIAL_WHOLE_ORGANISM_PROOF
CURRENT_PROOF_STATUS: NOT STARTED / NOT AUTHORIZED
CURRENT_09_G_STATUS: NOT STARTED
```
