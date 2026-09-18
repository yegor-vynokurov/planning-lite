# PL-V39-06 Operation-Depth Observation Bridge — Completion Review v1

Review date: 2026-09-18
Change: `CHG-PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-001`
Owner closure decision: `APPROVE / CLOSED_COMPLETE`

## Authority and accepted implementation identity

```text
PLANNING_AUTHORITY: a6e7c6d761495823a5a157cfa42abf77616d6b26
IMPLEMENTATION_CHECKPOINT: 420113cce4c1cb56d2b620c9b770773b952c7825
IMPLEMENTATION_CHECKPOINT_PARENT: a6e7c6d761495823a5a157cfa42abf77616d6b26
DEFINITION_AMENDMENT_SHA256: EC3936215075687890EC45644983CB61746C1FBE25943F3BE491EDFC1B829903
PLAN_AMENDMENT_SHA256: 321AF42BBB8E2063F6765AF14F97F191DDBD5F20E369731FA90FA9943748EA8B
FORMAL_READINESS: READY / v2
INDEPENDENT_REVIEW: REVIEW_PASS
MATERIAL_FINDINGS: 0
```

The implementation checkpoint is committed, has the required parent, contains
exactly the reviewed source/test candidate plus the authorized governance
evidence, and the product worktree is clean. The committed independent review
records `CANDIDATE_VERDICT: REVIEW_PASS` and `MATERIAL_FINDING_COUNT: 0`.

## Completion requirement/evidence matrix

| Requirement | Committed evidence | Result |
|---|---|---|
| Deterministic producer-bound start projection matches ContextTrace identity, roles, reasons, sections, counts, characters, bounds | `test_genuine_producer_start_and_public_mapping_are_compatible`; producer/trace projection | PASS |
| Genuine exact path/heading expansion produces one ordered complete event without body text | `test_genuine_exact_expansion_and_repeat_identity`; `record_expansion` metadata-only projection | PASS |
| Exact repeat/reopen uses path/reference, SHA, and section identity | Repeat test; `_depth_identity` and event construction | PASS |
| Different or merely similar source cannot become a repeat | Exact tuple comparison; no similarity comparison exists | PASS |
| Unobservable read is `UNAVAILABLE` with a finite reason and no inferred source | `test_unavailable_start_and_arbitrary_identity_are_fail_closed`; bound-reference check | PASS |
| Missing, stale, superseded, oversized, forbidden, outside-root, glob, `.git`, and symlink cases fail closed or become unavailable | Existing focused resume tests and status handling | PASS |
| Exact-selector and event bounds remain enforced | Existing selector tests; five-event and contiguous-sequence tests | PASS |
| Result is derived/disposable with no registry, database, memory store, log, or second authority | Two-file implementation diff and source inspection | PASS |
| No route, authorization, token/cache, prompt-dedup, skill, semantic, AgentWorkPacket, or compiler fields are added | Source inspection and committed diff scope | PASS |
| Walking skeleton proves start, exact expansion, repeat, unavailable, and read-only behavior | Focused producer tests, independent harness, and CLI tests | PASS |
| Producer-bound start provenance is required | Exact `ProducedResumeContextV1` gate in `from_produced_context` | PASS |
| Producer-bound expansion provenance is required | Exact `ProducedResumeContextV1` gate in `record_expansion` | PASS |
| Perfect ordinary Mapping cannot establish start provenance | Mapping rejection test and direct perfect-mapping reproduction | PASS |
| Perfect ordinary Mapping cannot establish expansion provenance | Mapping rejection test and direct expansion reproduction | PASS |
| JSON round-trip cannot restore start or expansion provenance | JSON rejection test and direct JSON reproduction | PASS |
| Markers, flags, copied hashes, revisions, counts, or bounds cannot establish provenance | Marker/copy attack test and direct reproduction | PASS |
| Supported public construction/factories cannot create an eligible carrier | Constructor rejection; no public deserializer | PASS |
| Subclass and duck type cannot bypass the boundary | Subclass/duck test and exact-type checks | PASS |
| Private capability is not serialized | Carrier `to_dict()`/JSON contain metadata only; no sentinel | PASS |
| One producer occurrence equals one context build; observation does not rebuild | Call-count test and direct spies | PASS |
| Observation performs no filesystem, Git, host-log, or reconstruction reads | Projection spies and source inspection | PASS |
| Ordinary `build_resume_context` Mapping remains compatible | Public mapping equality test and direct comparison | PASS |
| Default resume CLI JSON remains compatible and read-only | CLI read-only test and CLI subset | PASS |
| Start/event bounds and count consistency remain enforced | Bounds/count tests and producer-owned validation | PASS |
| Caller mutation and `to_dict()` mutation do not alter retained state | `test_carrier_and_observation_to_dict_are_detached` | PASS |
| Raw body, prompt, response, transcript, tool payload, and reasoning retention is forbidden | Raw-field test, `_DEPTH_RAW_KEYS`, metadata-only schema | PASS |
| PL06, PL07, PL08, and PL09 ownership boundaries remain unchanged | Two-file implementation surface and no adjacent subsystem changes | PASS |
| Major PL09 next-slice gate remains preserved/unconsumed | Current/ledger state and no PL09 authority change | PASS |
| Change 2 remains unstarted and unauthorized | Current/ledger state and explicit non-authorization | PASS |

The matrix covers the predecessor Definition acceptance criteria and walking
skeleton, the Definition Amendment’s mandatory producer-bound criteria, the
predecessor Plan’s focused matrix and evidence obligations, and all 19 cases
of the amended Plan matrix. Existing owner tests remain authoritative for
stale/superseded/missing, exact headings, oversized sections, forbidden and
symlink paths, deterministic output, invalid sequence, and event caps.

## Trust-boundary closure

```text
approved PL06 producer occurrence
-> exact producer-bound in-process carrier
-> bounded OperationDepthObservationV1 projection
-> COMPLETE or PARTIAL observed fact
```

Both start and expansion use the same exact carrier eligibility rule. Ordinary
mappings, copied metadata, parsed JSON, self-declared markers, subclasses, and
duck types cannot cross the boundary. The private factory fence is an
implementation detail, is not serialized, and makes no hostile-process
security claim.

## Post-commit verification

| Command | Result |
|---|---|
| `uv run --frozen pytest tests/test_context_resume.py -rA` | **33 passed** |
| `uv run --frozen pytest tests/test_context_resume.py tests/test_central_resume_contract.py -rA` | **47 passed** |
| `uv run --frozen pytest tests/test_cli.py -k resume -rA` | **4 passed, 4 deselected** |
| `uv run --frozen python scripts/maintainer_resume.py` | **PASS**; clean checkpoint, implementation authorization NO |
| `uv run --frozen pytest` | **457 passed, 2 known baseline failures, 88 warnings** |

The two full-suite failures are unchanged and independent:

- `tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree`
- `tests/test_project_shaping_foundation.py::test_manifest_and_sha_receipts_cover_the_current_template_tree`

Both fail because the existing manifest/SHA receipts omit the already-present
`.planning/framework/architecture-knowledge/ARCHITECTURE_KNOWLEDGE_PACK.md`.
The accepted implementation changed no template, manifest, or SHA receipt
path, and no candidate-related failure appeared. This is known baseline debt,
not a completion blocker.

## Write-surface, privacy, and ownership closure

The implementation checkpoint modified only the approved implementation/test
paths plus authorized evidence and governance. This closure operation is
limited to:

```text
docs/design/project-spine/CURRENT.md
docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-EXECUTION-LEDGER-v1.md
docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-COMPLETION-REVIEW-v1.md
```

No source, test, amendment, Plan, Roadmap, template, PL07, PL08, PL09, or
manifest/SHA file is changed by closure. The implementation retains only
bounded metadata and source references; no source bodies, prompts, responses,
transcripts, hidden reasoning, or tool payloads are retained.

PL06 remains the owner of context selection and the producer-bound carrier.
PL07 route/capability/authorization semantics, PL08 attempts/evaluation/
RunReceipt ownership, and PL09 semantic/compiler/orchestration ownership are
unchanged. Change 2 is not started, selected, or authorized.

## Completion disposition

```text
OPEN_MATERIAL_FINDINGS: NONE
COMPLETION_VERDICT: PASS
OWNER_CLOSURE_DECISION: APPROVE / CLOSED_COMPLETE
CHANGE_STATE_AFTER_CLOSURE: CLOSED / COMPLETE
CAPABILITY: PRODUCER_BOUND_OPERATION_DEPTH_OBSERVATION_BRIDGE / COMPLETE
IMPLEMENTATION_AUTHORIZED: NO
CHANGE2: NOT_STARTED / NOT_AUTHORIZED
PL08_RUNRECEIPT_CORRECTION: NOT_STARTED / NOT_AUTHORIZED
PROMPT_DEDUP_RUNTIME_ACTIVATION: NOT_AUTHORIZED
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
NEXT_SINGLE_GATE: OWNER_DECISION_START_PL09_COMPACT_SEMANTIC_OPERATION_TRACE_CORRECTIVE_CHANGE
```

The next gate is an owner decision to start or activate a distinct bounded
corrective Change. This closure does not consume
`OWNER_ADJUDICATION_PL_V39_09_NEXT_SLICE_AFTER_09-B_CLOSURE` and does not
authorize execution, Definition preparation, or implementation of that next
Change.
