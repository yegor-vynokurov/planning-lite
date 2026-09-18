# PL-V39-06 Operation-Depth Observation Bridge — Amended Implementation Candidate Review v1

Review date: 2026-09-18  
Reviewer: GPT-5.6 Luna / Extra High  
Review mode: fresh independent read-only implementation-candidate review

## Authority binding

Planning Authority: `a6e7c6d761495823a5a157cfa42abf77616d6b26`  
Observed HEAD: `a6e7c6d761495823a5a157cfa42abf77616d6b26` — PASS

The following authority hashes were independently read and verified:

| Artifact | Observed SHA256 | Result |
|---|---|---|
| Definition Amendment v1 | `EC3936215075687890EC45644983CB61746C1FBE25943F3BE491EDFC1B829903` | PASS |
| Implementation Plan v1 | `AF3D1E9F122351B9DDFCBD631278375203FB842F6AD0252F69717B3B31442273` | PASS against the amendment’s bound predecessor |
| Implementation Plan Amendment v1 | `321AF42BBB8E2063F6765AF14F97F191DDBD5F20E369731FA90FA9943748EA8B` | PASS |
| Formal Readiness Verdict v2 | `E7E8D1EF60503C6E77AAB2BCF48A66B8D2F474FFCC86C251824B7C033F86AF65` | READ |

The predecessor Definition SHA is `0E88BB67899AC1EC23C942C663DDCBB793742262DD3E7036B2F81A41E0FD3424`, matching the Definition Amendment’s bound predecessor. Formal Readiness is `READY` with `IMPLEMENTATION_AUTHORIZED: NO`; that governance state was preserved.

`AUTHORITY_BINDING: PASS`

## Candidate and write-surface audit

Expected candidate implementation paths were exactly:

- `src/planning_lite/context.py`
- `tests/test_context_resume.py`

`UNEXPECTED_IMPLEMENTATION_PATHS: 0`

Pre-existing governance dirt was limited to `docs/design/project-spine/CURRENT.md` and the untracked Formal Readiness Verdict v2. The review did not modify either. No template, PL07, PL08, PL09, staging, ledger, or Git history path was modified.

The historical pre-amendment patch was inspected only after current-source review. Its mapping-based observation boundary is absent from the candidate trust path; the current candidate has a producer-bound `ProducedResumeContextV1` carrier and exact-type gates for both start and expansion.

## Independent discriminator and source review

The real producer path is `_build_resume_context_product(...)`, shared by `build_resume_context(...)` and `build_observed_resume_context(...)`. It invokes the existing bounded context builder once, then produces either the ordinary mapping or the producer-bound carrier. `OperationDepthObservationV1.from_produced_context(...)` and `record_expansion(...)` accept only exact `ProducedResumeContextV1` instances.

Direct independent runtime reproduction results:

| Check | Result |
|---|---|
| Genuine producer start accepted | YES |
| Genuine exact expansion accepted | YES |
| Complete ordinary start Mapping rejected | REJECTED |
| Complete ordinary expansion Mapping rejected | REJECTED |
| JSON round-trip start provenance | REJECTED |
| JSON round-trip expansion provenance | REJECTED |
| Caller-controlled producer/observed/bound/provenance markers | REJECTED |
| Ordinary public `ProducedResumeContextV1(...)` constructor creates eligible carrier | NO |
| Public `from_dict`/`from_mapping`/`deserialize`/`restore_provenance` | NO |
| Normal subclass or duck type bypass | NO |
| Private capability serialized | NO |
| Start producer-bound | YES |
| Expansion producer-bound | YES |
| Start/expansion trust model symmetric | YES |

The supported mapping entry point `from_resume_context(...)` remains only as a fail-closed compatibility surface. Mapping-shaped expansion input is also rejected. The private `_from_product(...)` factory and process-local capability are within the approved threat model’s private-internal exclusion and are not serialized.

The observation projection consumed only carrier metadata. Spies that failed on filesystem reads, Git reads, or a second context build were not triggered. The real producer path ran once per producer call, and observation projection performed zero context builds.

`ONE_PRODUCER_OCCURRENCE_ONE_CONTEXT_BUILD: PASS`  
`SECOND_BUILD_FOR_PROVENANCE: NO`  
`OBSERVATION_FILESYSTEM_READ: NO`  
`OBSERVATION_GIT_READ: NO`  
`OBSERVATION_HOST_READ: NO`  
`OBSERVATION_CONTEXT_RECONSTRUCTION: NO`

## Bounds, provenance, retention, and compatibility

Independent source inspection and runtime checks verified:

- exact source schema, normalized repository-relative paths, SHA-256 format, fixed roles/reasons, storage classification, and exact heading rules;
- start artifact/section/count metadata and the five-event observation bound;
- contiguous one-based event sequence;
- repeat identity exactly `(normalized source path/reference, sha256, section)`;
- caller mutation isolation for carrier and observation `to_dict()` results;
- stale, superseded, missing, oversized, and unobservable cases remain fail-closed;
- `record_unavailable` cannot introduce an arbitrary unbound source reference;
- no source body, reasoning, prompt, response, transcript, or tool payload is retained;
- `build_resume_context(...)` returns the unchanged public Mapping shape;
- existing resume/JSON CLI behavior remains unchanged;
- no duplicate builder, selector, registry, credential store, deserializer, host observer, crypto, PL07 routing, PL08 evaluation, or PL09 semantic/compiler behavior was introduced.

`START_BOUNDS: PASS`  
`COUNT_VALIDATION: PASS`  
`CALLER_IMMUTABILITY: PASS`  
`TO_DICT_IMMUTABILITY: PASS`  
`REPEAT_IDENTITY: PASS`  
`SEQUENCE_EVENT_BOUND: PASS`  
`UNAVAILABLE_SEMANTICS: PASS`  
`RAW_CONTENT_RETENTION: NO`  
`BUILD_RESUME_CONTEXT_PUBLIC_MAPPING: UNCHANGED`  
`CLI_JSON: UNCHANGED`  
`LEGACY_MAPPING_PROVENANCE_PATH: ABSENT_OR_FAIL_CLOSED`

`SECURITY_CLAIM_SCOPE: CORRECT` — the claim is limited to supported public callers and does not claim security against hostile private Python access.

## Independent test evidence

Commands and exact results:

- `uv run --frozen pytest tests/test_context_resume.py -rA` — **33 passed**.
- `uv run --frozen pytest tests/test_context_resume.py tests/test_central_resume_contract.py -rA` — **47 passed**.
- `uv run --frozen pytest tests/test_cli.py -k resume -rA` — **4 passed, 4 deselected**.
- `uv run --frozen python scripts/maintainer_resume.py` — **PASS**; central resume succeeded, `implementation_authorized: NO` preserved, and the owner authorization action remained the next permitted action.
- `uv run --frozen pytest` — **457 passed, 2 failed, 88 warnings**.

The two full-suite failures were exactly the known baseline manifest/SHA coverage failures:

- `tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree`
- `tests/test_project_shaping_foundation.py::test_manifest_and_sha_receipts_cover_the_current_template_tree`

Both report the known extra template path `.planning/framework/architecture-knowledge/ARCHITECTURE_KNOWLEDGE_PACK.md`. The candidate changed no template, manifest, or SHA receipt path, and no new PL06/candidate-related failure occurred. These are therefore nonblocking baseline debt under the review instructions.

The first inline adversarial harness run exposed an indexing error in the harness while reading a second repeat event; the corrected independent harness rerun passed all checks. This was a verifier defect, not a product failure.

## Findings and verdict

`MATERIAL_FINDING_COUNT: 0`  
`MATERIAL_FINDINGS: NONE`  
`NON_BLOCKING_FINDINGS: known baseline manifest/SHA debt only; no candidate defect`

`CANDIDATE_VERDICT: REVIEW_PASS`

`CANDIDATE_STATE: UNCOMMITTED / INDEPENDENT_REVIEW_PASS / AWAITING_OWNER_CHECKPOINT_COMMIT_DECISION`

No correction, commit, push, CURRENT update, or execution-ledger update is authorized by this review.

## Required terminal receipt

```text
PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_AMENDED_IMPLEMENTATION_CANDIDATE_INDEPENDENT_REVIEW

OVERALL: REVIEW_PASS
REVIEWER: GPT-5.6_LUNA_EXTRA_HIGH
REVIEW_MODE: FRESH_INDEPENDENT_READ_ONLY
PLANNING_AUTHORITY_SHA: a6e7c6d761495823a5a157cfa42abf77616d6b26
AUTHORITY_BINDING: PASS
CANDIDATE_IMPLEMENTATION_PATHS: src/planning_lite/context.py; tests/test_context_resume.py
UNEXPECTED_IMPLEMENTATION_PATHS: 0
GENUINE_START_ACCEPTED: YES
GENUINE_EXPANSION_ACCEPTED: YES
PERFECT_FAKE_START_MAPPING: REJECTED
PERFECT_FAKE_EXPANSION_MAPPING: REJECTED
JSON_ROUNDTRIP_START_PROVENANCE: REJECTED
JSON_ROUNDTRIP_EXPANSION_PROVENANCE: REJECTED
CALLER_CONTROLLED_MARKER_PROVENANCE: REJECTED
ORDINARY_PUBLIC_CONSTRUCTOR_CREATES_ELIGIBLE_CARRIER: NO
PUBLIC_DESERIALIZER_RESTORES_PROVENANCE: NO
SUBCLASS_DUCK_TYPE_BYPASS: NO
PRIVATE_CAPABILITY_SERIALIZED: NO
START_PRODUCER_BOUND: YES
EXPANSION_PRODUCER_BOUND: YES
TRUST_MODEL_SYMMETRIC: YES
ONE_PRODUCER_OCCURRENCE_ONE_CONTEXT_BUILD: PASS
SECOND_BUILD_FOR_PROVENANCE: NO
OBSERVATION_FILESYSTEM_READ: NO
OBSERVATION_GIT_READ: NO
OBSERVATION_HOST_READ: NO
BUILD_RESUME_CONTEXT_PUBLIC_MAPPING: UNCHANGED
CLI_JSON: UNCHANGED
LEGACY_MAPPING_PROVENANCE_PATH: ABSENT_OR_FAIL_CLOSED
START_BOUNDS: PASS
COUNT_VALIDATION: PASS
CALLER_IMMUTABILITY: PASS
TO_DICT_IMMUTABILITY: PASS
REPEAT_IDENTITY: PASS
SEQUENCE_EVENT_BOUND: PASS
UNAVAILABLE_SEMANTICS: PASS
RAW_CONTENT_RETENTION: NO
SECURITY_CLAIM_SCOPE: CORRECT
FOCUSED_TESTS: 33 passed
CENTRAL_RESUME_TESTS: 47 passed
CLI_COMPATIBILITY_TESTS: 4 passed, 4 deselected
MAINTAINER_RESUME: PASS
FULL_REGRESSION: 457 passed, 2 known baseline failures, 88 warnings
NEW_REGRESSION_FAILURES: 0
KNOWN_BASELINE_FAILURES: 2 manifest/SHA coverage tests listed above
MATERIAL_FINDING_COUNT: 0
MATERIAL_FINDINGS: NONE
NON_BLOCKING_FINDINGS: known baseline manifest/SHA debt only
CANDIDATE_VERDICT: REVIEW_PASS
CANDIDATE_STATE: UNCOMMITTED / INDEPENDENT_REVIEW_PASS / AWAITING_OWNER_CHECKPOINT_COMMIT_DECISION
REVIEW_ARTIFACT: docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-AMENDED-IMPLEMENTATION-CANDIDATE-REVIEW-v1.md
CURRENT_MODIFIED: NO
EXECUTION_LEDGER_MODIFIED: NO
SOURCE_FILES_MODIFIED_BY_REVIEW: 0
TEST_FILES_MODIFIED_BY_REVIEW: 0
STAGED_PATHS: 0
COMMIT_PERFORMED: NO
PUSH_PERFORMED: NO
MAJOR_PL09_GATE: PRESERVED / UNCONSUMED
RESULT_DIGEST: The amended producer-bound candidate rejects perfect caller mappings, JSON round-trips, markers, subclasses, and duck types for both start and expansion. Independent tests and direct spies prove one producer build per occurrence, zero observation reads/rebuilds, unchanged public resume/CLI behavior, and no material finding.
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_CHECKPOINT_COMMIT
```
