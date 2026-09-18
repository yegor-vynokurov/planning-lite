# CHG-PL-V39-06 Operation-Depth Observation Bridge — Implementation Plan Amendment v1

Status: `APPROVED_BY_OWNER`

## 1. Plan amendment identity and authority

```text
Plan Amendment ID: PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-PLAN-AMENDMENT-001
Change ID: CHG-PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-001
Prepared: 2026-09-18
Selected direction: PRODUCER_BOUND_OBSERVATION
Plan amendment approval: APPROVE / USER / EXPLICIT / 2026-09-18
Formal Readiness: NOT RUN / RENEWED READINESS REQUIRED
Implementation authorization: NO
Implementation tasks: NOT STARTED
Approval authority: OWNER / EXPLICIT / EXERCISED
Canonical artifact: docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-IMPLEMENTATION-PLAN-AMENDMENT-v1.md
Approved source candidate SHA256: B13942E66BA0B8B57C40F1C502F688B7434EFE8E25504C2D37DECCCCE95B20E4
```

This canonical artifact records the owner's approved bounded delta to the
approved predecessor Plan. It does not create the amended Planning Authority
checkpoint, run renewed Formal Readiness, authorize implementation, or
authorize Git mutation.

## 2. Exact authority and draft binding

| Input | Path / identity | SHA256 / revision |
|---|---|---|
| approved predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-CHANGE-DEFINITION-v1.md` | `0E88BB67899AC1EC23C942C663DDCBB793742262DD3E7036B2F81A41E0FD3424` |
| Definition activation | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-ACTIVATION-v1.md` | `ED70C5611B94AF8690B31539D6E608AC6B69CB51EE69115A01EC81C1D5AEFFEA` |
| approved predecessor Plan | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-IMPLEMENTATION-PLAN-v1.md` | `AF3D1E9F122351B9DDFCBD631278375203FB842F6AD0252F69717B3B31442273` |
| predecessor Planning Authority | Git commit | `f34429aefbf09fcae43226ff74eafefd580b3b88` |
| approved Definition Amendment source candidate | `.local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_DEFINITION_AMENDMENT_CANDIDATE.md` | `1FBB526271CD5C61DAD1C3ABEDE04C9EB3187C8627647DC69F381394841E7329` |
| canonical Definition Amendment | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-AMENDMENT-v1.md` | `EC3936215075687890EC45644983CB61746C1FBE25943F3BE491EDFC1B829903` |
| canonical Plan Amendment | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-IMPLEMENTATION-PLAN-AMENDMENT-v1.md` | approved by this transition |

This approved Plan Amendment is bound to the exact approved Definition
Amendment source candidate hash and the canonical Definition Amendment hash
recorded above. Any later semantic change requires reconciliation and renewed
owner approval.

The first and second independent review records bound by the Definition
Amendment remain evidence, not authority. Both amendments are approved. The
predecessor Plan remains controlling for unchanged evidence, verification,
retention, rollback, and gate semantics; this amendment replaces only the
mapping-based trust input, affected API/task/test wording, walking skeleton,
and resulting lifecycle disposition.

## 3. Architecture decision

### 3.1 One producer occurrence, two deliberately different products

Refactor the existing PL06 builder inside `src/planning_lite/context.py` so one
internal context-selection/build occurrence produces an immutable
producer-bound value from the same bounded result used for the existing public
mapping:

```text
single internal PL06 context build
  -> ProducedResumeContextV1       # in-process provenance-capable carrier
       -> to_dict()                 # ordinary public ResumeContext mapping
       -> OperationDepthObservationV1
```

There is no second selection, scan, hash pass, or filesystem read for an
observation projection. `build_resume_context(...)` and the default CLI keep
returning/serializing the ordinary mapping. An observation-aware in-process
caller invokes a sibling producer function once and receives the carrier; it
may call `carrier.to_dict()` when it also needs the compatible mapping from the
same producer occurrence.

### 3.2 Exact carrier and construction fence

Add this exact logical contract in `context.py`:

```text
ProducedResumeContextV1
  frozen: YES
  slots: YES
  public constructor: DISABLED
  normal creator: internal PL06 producer only
  retained value: recursively frozen, bounded, body-free ResumeContextV1 metadata
  supported representation: to_dict() -> ordinary deep independent dict
  authority semantics: NONE
  persistence identity: NONE
```

The supported implementation is a frozen, slotted, `init=False` value whose
normal constructor raises `ContextError`. A module-private creation method
requires identity with one module-private process-local capability object. The
shared internal producer owns that capability and creates the carrier only
after it has built the real bounded PL06 result. `OperationDepthObservationV1`
uses an exact runtime type check and does not accept mappings or carrier
substitutes.

The private capability is an accidental-construction fence for normal public
use. It is not a secret, signature, durable token, or defense against
reflection, monkey patching, private-internal access, or interpreter
compromise. Those hostile-code cases remain outside scope.

The carrier may retain the exact recursively frozen public ResumeContext
result because that result is already bounded metadata and contains no source
body. It must not retain file handles, paths outside the existing normalized
metadata, producer callables, source bodies, prompts, responses, transcripts,
tool payloads, hidden reasoning, or mutable caller-owned leaves. Its
`to_dict()` output is a fresh deep representation; mutating it cannot affect
the carrier or an observation.

The carrier has no supported reconstruction or persistence API. JSON
serialization is performed only over `to_dict()` and yields an ordinary
mapping with no carrier eligibility.

### 3.3 Shared builder shape

The existing `build_resume_context` body becomes one private internal producer
implementation. Exact private names may follow repository naming conventions,
but behavior is frozen as:

```text
_build_resume_context_product(target, include=(), handoff=None)
  -> ProducedResumeContextV1

build_resume_context(target, include=(), handoff=None)
  -> _build_resume_context_product(...).to_dict()

build_observed_resume_context(target, include=(), handoff=None)
  -> _build_resume_context_product(...)
```

`build_observed_resume_context` is the only new supported producer entrypoint.
It performs the same one context build as `build_resume_context`; it does not
call `build_resume_context` and then rebuild or wrap caller-supplied data. Both
entrypoints share one internal implementation, so public mapping semantics
cannot drift from producer-bound semantics.

`ProducedResumeContextV1` is exported for type annotation and inspection, but
it has no supported public construction path. Exporting its name does not make
`_from_producer` or the private capability public API.

## 4. Explicit A–K design decisions

### A. Exact value that establishes producer provenance

Only an exact `ProducedResumeContextV1` instance created by the internal PL06
producer capability establishes provenance. A subclass, duck-typed object,
mapping proxy, `dict`, JSON object, copied metadata structure, or object with a
matching marker is ineligible.

### B. Creator function/factory

Only the shared private `_build_resume_context_product(...)` producer may call
the carrier's private capability-guarded factory. Public callers obtain the
result only by invoking `build_observed_resume_context(...)`.

### C. Direct ordinary caller construction

`NO`. The carrier's normal constructor is disabled and the public observation
API contains no `from_mapping`, `from_dict`, deserializer, token, marker, or
factory accepting caller-authored metadata. Hostile access to private Python
internals is not a supported path and is outside the threat model.

### D. Existing `build_resume_context` result

`YES`: `build_resume_context(...)` continues to return its compatible public
`dict[str, Any]`; the existing `resume_context` and
`validate_resume_context` aliases and default CLI JSON remain compatible. The
mapping is a representation and cannot establish observation provenance.

### E. Producer-bound operation start without a second build

An observation-aware operation calls
`build_observed_resume_context(target, handoff=...)` once. That single producer
occurrence returns the carrier. The operation passes the carrier to
`OperationDepthObservationV1.from_produced_context(...)` and uses
`carrier.to_dict()` if it also needs the ordinary ResumeContext mapping. The
projection performs no producer call or filesystem read.

### F. Producer-bound exact include expansion

The operation calls
`build_observed_resume_context(target, include=[exact_selector], handoff=...)`
once for that expansion occurrence. It passes the returned carrier to
`record_expansion(...)`. Existing PL06 exact-selector, path, freshness,
artifact, section, character, and expansion-result rules remain the producer
authority.

### G. Serialization and deserialization

`carrier.to_dict()` and JSON serialization produce an ordinary public
representation. Parsing or copying that representation returns a `Mapping`,
not a `ProducedResumeContextV1`; provenance is intentionally lost and cannot
be restored through a public API. Feeding the parsed value to
`from_produced_context` or `record_expansion` raises `ContextError` and cannot
produce a `COMPLETE` or `PARTIAL` fact.

### H. `record_unavailable`

`record_unavailable(reason_code, sequence_index=None, source_ref=None)` remains
an immutable bounded operation and does not require a carrier because it makes
no positive observation claim. A non-null `source_ref` is permitted only when
the exact path/SHA pair is already bound to that observation by its genuine
producer-bound start or a prior genuine producer-bound expansion. Otherwise it
raises `ContextError`. No source body or unobserved identity is accepted.

Add `OperationDepthObservationV1.unavailable_start(reason_code,
operation_ref=None)` for the case where no producer-bound start exists. It
accepts only `INVALID_START_CONTEXT` or `NO_APPROVED_SEAM`, accepts no mapping
or source metadata, and creates only an `UNAVAILABLE` start. A producer
expansion cannot become `COMPLETE`/`PARTIAL` against an unavailable start
because there is no producer-bound baseline; later reads may only be recorded
unavailable until a new observation is created from a genuine start.

### I. Repeat/reopen identity

Preserve the exact producer-derived identity tuple:

```text
(normalized source path/reference, sha256, section)
```

The first genuine occurrence is `NO`; a later genuine producer-bound event
with the same tuple is `YES`; any path, hash, or section difference is `NO`.
No mapping, serialized report, similarity inference, or timing signal
participates.

### J. Existing bounds

The shared producer continues to own and enforce `MAX_EXPANSIONS`,
`MAX_TOTAL_ARTIFACTS`, `DEFAULT_MAX_ARTIFACTS`, `SECTION_MAX_CHARS`,
`CURRENT_STATE_MAX_CHARS`, `ACTIVE_CONTEXT_MAX_CHARS`, exact include count,
and the existing path/storage/freshness rules. The carrier copies the actual
producer result and no caller can supply replacement bounds. The observation
also uses `MAX_EXPANSIONS` as its total event cap and keeps one-based contiguous
sequence validation. No duplicate constants or weaker observation limits are
introduced.

### K. Corrected `OperationDepthObservationV1` public API

```text
OperationDepthObservationV1.from_produced_context(
    produced_context: ProducedResumeContextV1,
    operation_ref: str | None = None,
) -> OperationDepthObservationV1

OperationDepthObservationV1.unavailable_start(
    reason_code: str,
    operation_ref: str | None = None,
) -> OperationDepthObservationV1

observation.record_expansion(
    produced_context: ProducedResumeContextV1,
    sequence_index: int | None = None,
) -> OperationDepthObservationV1

observation.record_unavailable(
    reason_code: str,
    sequence_index: int | None = None,
    source_ref: Mapping[str, Any] | None = None,
) -> OperationDepthObservationV1

observation.to_dict() -> dict[str, Any]
```

Remove the uncommitted mapping-based
`OperationDepthObservationV1.from_resume_context(...)` API. Change
`record_expansion(...)` to reject all plain mappings. No compatibility alias
may retain the defective provenance behavior. API cleanup is deliberately
performed before the uncommitted candidate becomes public.

## 5. Projection behavior and invariants

`from_produced_context` validates the exact carrier and projects only the
approved start fields already named by the predecessor Plan. A genuine current
carrier with zero requested expansions, no explicit-expansion source, and no
expansion result yields a `COMPLETE` start. A genuine carrier whose existing
PL06 status is stale, superseded, missing, or otherwise unusable yields the
corresponding bounded `UNAVAILABLE` start without fabricated source facts. A
carrier containing an include result is not a valid operation-start input.

`record_expansion` accepts only a genuine carrier whose producer request count
is exactly one for one exact include occurrence, preserves the predecessor
rule of exactly one explicit expansion or one bounded
`EXPANSION_TOO_LARGE` result, requires the genuine baseline sources and
revision to match the genuine current start, and returns a new immutable
observation. A valid explicit source is `COMPLETE`; a genuine bounded oversize
result may be `PARTIAL`; stale, superseded, missing, malformed, or
baseline-mismatched inputs fail closed under the predecessor semantics.

The carrier establishes origin, not correctness by itself. Existing exact
shape, raw-field, status, baseline, count, sequence, and bounds validations
remain defense-in-depth over producer output. They must not be described as the
provenance mechanism.

The observation never calls a builder, filesystem helper, Git helper, CLI, or
host log. It derives a smaller immutable projection and exposes only fresh
independent JSON-compatible dictionaries from `to_dict()`.

## 6. Exact implementation surface

Future implementation under renewed authority may modify only:

```text
src/planning_lite/context.py
tests/test_context_resume.py
```

No additional implementation file is needed. No `template/`, CLI source,
telemetry, RunReceipt, routing, adapter, CURRENT, Roadmap, recommendation,
ledger schema, registry, database, host observer, persistent provenance file,
or Change 2 path is permitted. If the two-file boundary proves insufficient,
classify `MATERIAL_NOW` and stop for owner adjudication rather than expanding
the surface.

## 7. Amended task graph

### A-T01 — Introduce the producer-bound carrier and shared producer

- Factor the current builder body into the single internal producer.
- Add the frozen carrier, disabled ordinary constructor, private capability-
  guarded producer factory, exact type eligibility, and deep independent
  `to_dict()` representation.
- Preserve byte/schema-equivalent public mapping and default CLI behavior.
- Stop if a second build, registry, durable token, secret, or third tracked
  implementation path is required.

### A-T02 — Correct the observation API and preserve invariants

- Replace mapping-based start/expansion inputs with the exact carrier type.
- Add explicit unavailable-start construction with no source metadata.
- Preserve projection shape, repeat identity, sequence, bounds, immutability,
  finite reasons, and raw-retention prohibitions.
- Prove projection methods perform no filesystem or producer call.

### A-T03 — Add provenance discriminators and compatibility tests

- Add the complete test matrix in section 8 to the existing test module.
- Retain existing producer, path/freshness, raw, bound, CLI, and observation
  coverage without duplicating invariants that already have an owner test.
- Adjudicate failures as product versus verifier defects before changing code.

### A-T04 — Run the amended walking skeleton and focused verification

- Exercise start and expansion through the in-process producer-bound path.
- Separately verify ordinary mapping/CLI output.
- Prove JSON round-trip provenance loss, no writes, no body retention, and no
  second build.
- Stop after evidence preparation for fresh independent review; no commit is
  implied.

Dependency order: `A-T01 -> A-T02 -> A-T03 -> A-T04`.

## 8. Required amended test matrix

All focused tests remain in `tests/test_context_resume.py`.

| # | Case | Required proof |
|---:|---|---|
| 1 | Genuine producer start | `build_observed_resume_context(...)` returns a carrier accepted by `from_produced_context`; start metadata matches its public representation. |
| 2 | Genuine exact include | A carrier from one exact path/heading include is accepted and produces the expected `COMPLETE` event. |
| 3 | Genuine exact repeat | Recording the same genuine carrier twice yields `NO`, then `YES`, using exact path/SHA/section identity. |
| 4 | Perfect fabricated start mapping | A structurally perfect mapping copied or handwritten from a real start is rejected and cannot become observed. |
| 5 | Perfect fabricated expansion mapping | A fully shaped eligible expansion with fabricated path/SHA is rejected and cannot become `COMPLETE` or `PARTIAL`. |
| 6 | Every expected field present | Role, hash, revision, counts, bounds, reasons, and markers still do not make a mapping eligible. |
| 7 | JSON provenance loss | Genuine carrier -> `to_dict()` -> JSON encode/decode -> mapping; feeding it back is rejected. |
| 8 | Construction boundary | Normal constructor use and supported public factories cannot directly instantiate an eligible carrier from caller metadata. |
| 9 | Fake capability markers | Producer strings, booleans, nonce/enum fields, mapping hashes, subclasses, and duck types do not confer eligibility. |
| 10 | No second context build | One start producer invocation and one expansion producer invocation each execute selection once; projection executes zero builds. |
| 11 | No projection filesystem read | After carriers exist, spies on `_read`, hash/Git, and producer helpers remain untouched during observation projection. |
| 12 | Public mapping unchanged | Existing `build_resume_context(...)` result remains schema/value compatible for identical fixture state. |
| 13 | Default CLI JSON unchanged | Existing resume JSON output and read-only behavior remain compatible; no observer command is added. |
| 14 | Raw retention impossible | Carrier and observation reject/do not expose bodies, prompts, responses, transcripts, tool payloads, or hidden reasoning; no raw sentinel appears. |
| 15 | Bounds preserved | Start artifact/section/character limits and `MAX_EXPANSIONS` are producer-owned; observation event cap and sequence remain enforced. |
| 16 | Immutability preserved | Carrier, observation, and retained leaves resist caller mutation; each `to_dict()` is independent. |
| 17 | `UNAVAILABLE` preserved | Outside-seam start/read has bounded reason and no new source identity; already-bound refs are the only permitted optional refs. |
| 18 | In-process walking skeleton | Genuine start + genuine exact expansion + repeat + unavailable succeed without tracked writes or a second build. |
| 19 | Known suite debt | The two unchanged template-manifest failures are re-adjudicated as pre-existing/out of scope unless their baseline or failure identity changes. |

Existing tests for stale/superseded/missing status, exact headings, oversize
sections, forbidden/outside/glob/symlink paths, deterministic output, invalid
sequence, and five-event cap remain authoritative and are adapted only where
the input type changes.

## 9. Amended walking skeleton

Use a disposable clean Git fixture and the real in-process PL06 producer:

1. Call `build_observed_resume_context(FIXTURE)` once; retain its carrier and
   ordinary `to_dict()` representation.
2. Construct the observation with `from_produced_context(start_carrier)`.
3. Call `build_observed_resume_context(FIXTURE,
   include=[EXACT_PATH_OR_HEADING])` once and record its carrier twice.
4. Record a bypassed/forbidden read as `UNAVAILABLE` without adding an
   unobserved source identity.
5. Inspect canonical observation JSON for exact source refs, hashes, revision,
   bounds, sequence, repeat status, and absence of raw bodies.
6. Separately run the existing public `build_resume_context` and default resume
   CLI and compare their representation with the established compatible
   contract.
7. JSON-serialize and parse a genuine carrier representation, then prove that
   the parsed mapping is rejected by both trusted observation inputs.
8. Compare fixture file/Git inventories before and after and prove projection
   caused no reads, writes, registry entry, or extra producer invocation.

The previous `CLI JSON -> parsed dict -> trusted observation` assumption is
removed. CLI JSON remains reporting/evidence representation only.

## 10. Evidence before later owner acceptance

- Exact approved Definition and Plan Amendment hashes and renewed Planning
  Authority binding.
- Renewed Formal Readiness `READY` against that committed authority.
- Focused provenance discriminator results for all 19 matrix cases.
- Existing context and central-resume regression results.
- Public mapping/default CLI compatibility evidence.
- In-process walking-skeleton readback with exact hashes/revision/bounds.
- Spies or equivalent direct evidence proving one build per producer
  occurrence and zero projection filesystem reads.
- Raw/privacy, immutability, write-boundary, and Git-scope audits.
- Fresh independent implementation review with F-02 explicitly closed.
- Full suite at the integration gate, with the two known template-manifest
  failures adjudicated against the frozen baseline rather than waived.

No single PASS label, executor ledger claim, or structural validator substitutes
for the real-producer versus perfect-fabrication discriminator.

## 11. Contradiction classification

| Question | Classification | Plan handling |
|---|---|---|
| 1. Provenance in `context.py` without registry | `RESOLVABLE` | Factory-only exact carrier type and process-local private capability. |
| 2. No second build | `RESOLVABLE` | Both public entrypoints share one internal producer; carrier supplies its representation. |
| 3. Mapping/CLI compatibility | `RESOLVABLE` | Existing public function and CLI continue emitting the ordinary dict/JSON contract. |
| 4. Plain Mapping/JSON exclusion | `RESOLVABLE` | Exact type input; remove mapping-based observation APIs and aliases. |
| 5. Start/expansion symmetry | `RESOLVABLE` | Both use `ProducedResumeContextV1` from the same sibling producer. |
| 6. Useful serialization with provenance loss | `RESOLVABLE` | `to_dict()` remains useful output; no public deserializer creates a carrier. |
| 7. Two-file boundary | `RESOLVABLE` | All producer/carrier/projection logic and focused tests fit the existing owner files. |
| 8. Security/cryptography drift | `RESOLVABLE` | Capability is a private construction fence, not a security token; hostile-code defense is excluded. |
| 9. Change 2 leakage | `RESOLVABLE` | No semantic cycle, digest, attachment, persistence, compiler, or orchestration fields. |
| 10. Definition scope expansion | `RESOLVABLE` | The amendment enforces the already intended approved-seam observation claim. |

```text
MATERIAL_CONTRADICTIONS: 0 / NONE
ADDITIONAL_IMPLEMENTATION_PATH_REQUIRED: NO
```

## 12. STOP conditions

Stop and return to owner adjudication if implementation:

- accepts any plain mapping, parsed JSON, marker, copied digest, caller nonce,
  enum, or duck type as `COMPLETE`/`PARTIAL` observed provenance;
- leaves either start or expansion on the arbitrary-Mapping trust rule;
- calls the context builder twice for one producer occurrence or lets the
  observation reread files/Git;
- changes default ResumeContext/CLI output without a separately adjudicated
  material need;
- requires a third tracked source/test path, CLI command, host hook, service,
  registry, database, persistent provenance log, signature, secret, or token;
- retains a source body, prompt, response, transcript, tool payload, hidden
  reasoning, or mutable caller-owned object;
- changes PL07 routing, PL08 evaluation, PL09 compiler/orchestration, Change 2,
  RunReceipt, telemetry, roadmap, or major PL09 next-slice authority;
- weakens existing source/path/freshness/bounds rules or creates unbounded
  events; or
- finds any other material contradiction affecting scope, safety, authority,
  acceptance evidence, or lifecycle truth.

## 13. Rollback, retention, and compatibility

The future correction remains additive and derived-only. It creates no stored
records or migration. Reverting the later reviewed source/test patch restores
the prior committed behavior; in-process carriers disappear with the process.
The uncommitted failed candidate is review history, not a compatibility
baseline.

All predecessor raw-retention invariants remain in force. The carrier adds no
authority and may not be persisted as a provenance credential. Its mapping
representation remains ordinary nonauthoritative data.

## 14. Current candidate and lifecycle disposition

```text
CURRENT_IMPLEMENTATION_CANDIDATE:
UNCOMMITTED / RE_REVIEW_FAIL / PENDING_AMENDED_AUTHORITY

PREDECESSOR_FORMAL_READINESS:
HISTORICAL_EVIDENCE_FOR_PREDECESSOR_PLAN / NO_LONGER_SUFFICIENT_FOR_FURTHER_EXECUTION

IMPLEMENTATION_CORRECTION: PAUSED
```

Do not delete, reset, commit, or continue patching the candidate before the
new Planning Authority and renewed Formal Readiness gates. The prior
implementation authorization does not carry forward to this amended design.

Required later lifecycle:

```text
owner approves Definition Amendment
+ owner approves Plan Amendment
-> bounded canonical amendment and CURRENT alignment
-> owner-authorized new Planning Authority checkpoint
-> renewed read-only Formal Readiness
-> separate owner implementation authorization
-> bounded two-file corrective implementation
-> fresh independent implementation review
-> separate checkpoint-commit authorization
```

```text
amendment draft != amendment approval
amendment approval != Planning Authority
Planning Authority != Formal Readiness READY
Formal Readiness READY != implementation authorization
implementation authorization != staging or commit authorization
```

## 15. Approval state and next gate

```text
PLAN_AMENDMENT: APPROVED_BY_OWNER
OWNER_PLAN_AMENDMENT_DECISION: APPROVE
APPROVAL_AUTHORITY: USER / EXPLICIT / 2026-09-18
APPROVED_SOURCE_CANDIDATE_SHA256: B13942E66BA0B8B57C40F1C502F688B7434EFE8E25504C2D37DECCCCE95B20E4
BOUND_DEFINITION_AMENDMENT_SHA256: 1FBB526271CD5C61DAD1C3ABEDE04C9EB3187C8627647DC69F381394841E7329
BOUND_CANONICAL_DEFINITION_AMENDMENT_SHA256: EC3936215075687890EC45644983CB61746C1FBE25943F3BE491EDFC1B829903
CANONICAL_DEFINITION_AMENDMENT_PATH: docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-AMENDMENT-v1.md
CANONICAL_ARTIFACT: docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-IMPLEMENTATION-PLAN-AMENDMENT-v1.md
PRODUCER_BOUND_START: YES
PRODUCER_BOUND_EXPANSION: YES
PLAIN_MAPPING_ESTABLISHES_PROVENANCE: NO
JSON_ROUNDTRIP_ESTABLISHES_PROVENANCE: NO
SECOND_CONTEXT_BUILD_REQUIRED: NO
NEW_REGISTRY_REQUIRED: NO
CRYPTOGRAPHIC_ATTESTATION_REQUIRED: NO
HOST_OBSERVER_REQUIRED: NO
IMPLEMENTATION_CORRECTION_PAUSED: YES
NEXT_OWNER_GATE: OWNER_AUTHORIZATION_PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_AMENDED_PLANNING_AUTHORITY_CHECKPOINT
```

This approval does not create the amended Planning Authority checkpoint, run
renewed Formal Readiness, authorize source/test mutation, authorize staging or
commit, or consume the major PL09 next-slice gate. The prior implementation
authorization does not carry forward.
