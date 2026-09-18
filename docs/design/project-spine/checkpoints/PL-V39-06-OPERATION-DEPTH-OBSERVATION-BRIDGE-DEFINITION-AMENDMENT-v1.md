# PL-V39-06 Operation-Depth Observation Bridge — Definition Amendment v1

Status: `APPROVED_BY_OWNER`

## 1. Amendment identity and approval

```text
Amendment ID: PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-AMENDMENT-001
Change ID: CHG-PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-001
Title: Producer-Bound Observation Trust Boundary
Prepared: 2026-09-18
Owner adjudication: ACCEPT_AS_PLAN_TRUST_BOUNDARY_GAP
Selected direction: PRODUCER_BOUND_OBSERVATION
Definition amendment approval: APPROVE / USER / EXPLICIT / 2026-09-18
Implementation authorization: NO
Staging, commit, push authorization: NO
Approval authority: OWNER / EXPLICIT / EXERCISED
Canonical artifact: docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-AMENDMENT-v1.md
Approved source candidate SHA256: 1FBB526271CD5C61DAD1C3ABEDE04C9EB3187C8627647DC69F381394841E7329
```

This canonical artifact records the owner's approved bounded delta to the
approved predecessor Definition. Together with the predecessor Definition, it
is the current Change scope authority for the producer-bound observation
semantics. The Change ID and compact operation-depth observation goal remain
unchanged.

This approval combines the predecessor Definition with this amendment as the
current Change scope authority. Every predecessor clause not explicitly
amended below remains in force. The predecessor Definition is not rewritten or
superseded as historical evidence.

## 2. Bound predecessor authority

| Authority | Path / identity | SHA256 / revision |
|---|---|---|
| approved predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-CHANGE-DEFINITION-v1.md` | `0E88BB67899AC1EC23C942C663DDCBB793742262DD3E7036B2F81A41E0FD3424` |
| Definition activation | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-ACTIVATION-v1.md` | `ED70C5611B94AF8690B31539D6E608AC6B69CB51EE69115A01EC81C1D5AEFFEA` |
| approved predecessor Plan | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-IMPLEMENTATION-PLAN-v1.md` | `AF3D1E9F122351B9DDFCBD631278375203FB842F6AD0252F69717B3B31442273` |
| predecessor Planning Authority | Git commit | `f34429aefbf09fcae43226ff74eafefd580b3b88` |
| canonical Definition Amendment | `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-AMENDMENT-v1.md` | approved by this transition |
| approved source candidate | `.local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_DEFINITION_AMENDMENT_CANDIDATE.md` | `1FBB526271CD5C61DAD1C3ABEDE04C9EB3187C8627647DC69F381394841E7329` |

The predecessor Planning Authority remains immutable historical authority for
the predecessor design. It does not authorize implementation under the
approved producer-bound semantics.

## 3. Bound review evidence, not authority

| Evidence | SHA256 | Bound conclusion |
|---|---|---|
| `.local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_CANDIDATE_REVIEW.md` | `F06296071AAB66A32E40092745BE5063DA66E9DDBAE76F2EB2AECB773BC2227A` | first independent review: `REVIEW_FAIL`; F-01 through F-04 identified |
| `.local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_CANDIDATE_REVIEW_CHECKPOINT.md` | `A3585FE48E84771CC01B716D254E551D0E5686E6611B7FFFAD606CFB29B212A7` | compact first-review finding and stop disposition |
| `.local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_CORRECTIVE_PASS_CHECKPOINT.md` | `461B779EB3083900B41DE13A118030C3E5BBFCF96F1FE89449EC0D4C8BE5C45C` | bounded correction closed F-01, F-03, and F-04 but did not establish producer provenance |
| `.local/work/experiments/PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_IMPLEMENTATION_CANDIDATE_RE_REVIEW_CHECKPOINT.md` | `361518897ED79CDC710628F8C499DA08F135B282B32ED0F608C8C897CAE223EF` | fresh independent `RE_REVIEW_FAIL`; F-02 remains open |

These records establish why an amendment is needed. They do not approve the
amendment, change current state, authorize implementation, or replace the
bound Definition, Plan, or Planning Authority.

## 4. Reason for amendment

The predecessor Definition correctly requires the observation to record only
explicit expansions that pass an approved Planning Lite seam and to report
unobservable reads as `UNAVAILABLE`. The predecessor Plan then operationalized
the seam as public methods accepting already-built ResumeContext-shaped
mappings.

A mapping can establish structural validity but cannot establish origin. The
second independent review demonstrated a structurally complete caller-created
eligible expansion, with matching baseline metadata and revision but a
fabricated path and SHA, being accepted as a `COMPLETE` observed event. The
same logical defect applies to an arbitrary caller-created operation-start
mapping.

```text
shape validation != provenance
MATERIAL_NOW: PLAN_TRUST_BOUNDARY_GAP
```

Adding roles, marker fields, booleans, nonces, provenance enums, hashes of the
mapping, or more cross-field validation would leave provenance self-asserted by
the caller. The smallest coherent correction is to bind observed facts to an
in-process value created only by the approved PL06 producer path in normal
supported use.

This is architectural provenance, not cryptographic attestation. Deliberately
hostile Python code using reflection, monkey patching, private internals, or an
interpreter compromise is outside this Change's threat model.

## 5. Amended meaning of observed context

For this Change, `observed` is amended to mean:

```text
approved PL06 producer occurrence
-> producer-bound in-process value
-> bounded OperationDepthObservationV1 projection
-> COMPLETE or PARTIAL observed fact
```

`COMPLETE` or `PARTIAL` start or expansion facts require producer-bound PL06
provenance. Structural validity remains necessary for safe projection, but it
is not sufficient provenance.

The following values cannot establish `COMPLETE` or `PARTIAL` observation
provenance, regardless of how accurately they reproduce the schema, hashes,
roles, revision, counts, bounds, or reason strings:

- a caller-created `dict` or other `Mapping`;
- a hand-written metadata object;
- parsed JSON or deserialized CLI output;
- a mapping containing a caller-supplied producer marker, flag, nonce, enum,
  or digest; or
- a copied or reconstructed serialized representation.

No public observation method may elevate one of those values into a
producer-observed fact.

## 6. Producer-bound start and expansion rule

The trust rule is symmetric:

```text
START:     PRODUCER_BOUND
EXPANSION: PRODUCER_BOUND
```

An operation start may be `COMPLETE` only when its metadata is projected from
an eligible in-process value emitted by the approved PL06 context producer.
An explicit expansion may be `COMPLETE` or `PARTIAL` only when its metadata is
projected from a separate eligible producer-bound value emitted for that exact
bounded include occurrence.

The producer-bound value must be immutable or effectively immutable, contain
only deterministic bounded metadata already owned by PL06, retain no source
body, carry no durable identity or authority, and be constructible only by the
producer-controlled path in normal public use. A private process-local factory
capability is permitted as an implementation fence; it is not a secret or a
security claim.

Both the producer-bound value and the ordinary mapping representation must be
derivable from one underlying context-selection/build occurrence. The
observation projection must not invoke a second context build, rescan the
repository, reread the filesystem, or infer host activity.

## 7. Representation and serialization boundary

The existing public ResumeContext mapping and CLI JSON remain useful for
compatibility, display, reporting, and evidence readback. They are
representations, not transferable provenance capabilities.

```text
producer-bound in-process value -> may establish observed provenance
ordinary mapping / JSON         -> representation only
JSON parse back to Mapping      -> provenance remains absent
```

Serializing a real producer-bound value and parsing the representation back
must intentionally lose eligibility for trusted observation input. Field
equality does not restore producer provenance. No registry, durable token, or
signature may be introduced to make provenance survive serialization.

## 8. `UNAVAILABLE` remains the honest outside-seam result

When Planning Lite does not receive a start or read through the approved
producer-bound seam, the observation records `UNAVAILABLE` with a bounded
reason rather than guessing or accepting caller-authored metadata.

`record_unavailable(...)` may carry no new source identity. It may reference a
source only when that exact reference was already bound to the same observation
by an eligible producer-bound start or expansion. `UNAVAILABLE` is an honest
absence of observation, not a weaker path for fabricated provenance.

## 9. Preserved goal, ownership, and semantics

The amendment preserves the original outcome: a compact, deterministic,
derived operation-depth observation over bounded PL06 context selections and
explicit expansions. It remains disposable, in-memory/JSON-compatible as an
output projection, and nonauthoritative.

| Owner | Preserved boundary |
|---|---|
| PL06 | owns context construction, exact selection, paths, hashes, roles, sections, bounds, freshness, and the producer-bound carrier |
| PL07 | continues to own operation guidance, route/capability semantics, and authorization; the carrier and observation grant none |
| PL08 | continues to own attempts, evaluation, facts, and result interpretation; the observation performs no evaluation |
| PL09 | continues to own later compiler/orchestration and semantic-cycle work; no Change 2 schema or attachment policy is frozen here |

The observation remains neither memory authority, lifecycle state, route
selection, permission, evaluation, a transcript, nor a persistent receipt.
The major PL09 next-slice gate remains preserved and unconsumed.

## 10. Amended acceptance and nearest-wrong criteria

The predecessor acceptance criteria remain in force with these mandatory
clarifications:

1. A real producer-bound start value is accepted and projects the same bounded
   metadata as its public ResumeContext representation.
2. A real producer-bound exact include value is accepted as one ordered
   expansion; a real bounded oversize result may be `PARTIAL` under existing
   PL06 semantics.
3. A structurally perfect fabricated start or expansion mapping is rejected as
   trusted input and cannot become `COMPLETE` or `PARTIAL`.
4. A real producer value serialized to JSON and parsed back cannot re-enter the
   trusted observation path.
5. Start and expansion use the same producer-bound eligibility rule.
6. Existing exact repeat identity, sequencing, source/path/freshness guards,
   artifact/section/character limits, and `MAX_EXPANSIONS` remain authoritative.
7. Projection from an already produced eligible value performs no filesystem
   read and no second context construction.
8. The ordinary `build_resume_context(...)` mapping and default CLI resume JSON
   remain compatible unless a later material contradiction is separately
   adjudicated.
9. No source body or other forbidden raw material can enter the carrier or
   projection.

The mandatory provenance discriminator is:

```text
real in-process producer value -> COMPLETE/PARTIAL eligible
same value -> public JSON -> parsed Mapping -> not producer eligible
```

## 11. Amended walking-skeleton proof

The predecessor walking skeleton is amended only at its trust input:

1. In a disposable clean product fixture, invoke the approved in-process PL06
   producer once for the operation start and receive its producer-bound value.
2. Invoke the same producer seam once for one exact path/heading expansion and
   receive a producer-bound expansion value.
3. Create the observation from the start value, record the expansion value,
   repeat it, and verify exact repeat identity and bounded output.
4. Record one bypassed read as `UNAVAILABLE` without a new inferred source.
5. Separately confirm that the public ResumeContext mapping and CLI JSON remain
   correct and read-only.
6. Serialize a genuine producer value to JSON, parse it, and prove that the
   resulting mapping is rejected as observed provenance.

CLI JSON is no longer an eligible trusted input to the observation. This
change does not require a new CLI command.

## 12. Explicit exclusions and STOP conditions

This amendment does not authorize or require:

- a registry, database, persistent provenance ledger, file-per-operation log,
  or new memory authority;
- cryptographic signing, secrets, durable tokens, or hostile-code attestation;
- a host observer, host-log capture, tool-payload capture, or arbitrary-read
  instrumentation;
- a second context construction or filesystem reread by the observation;
- transcript, prompt, response, source-body, hidden-reasoning, or raw tool-body
  retention;
- semantic similarity, semantic search, inferred reopen, or model judgment;
- a new CLI observer command or a provenance-bearing JSON format;
- PL07 route or authorization ownership, PL08 evaluation ownership, PL09
  compiler/orchestration work, or Change 2 semantic-cycle scope; or
- any new lifecycle stage, owner gate, tracked implementation path, or durable
  authority.

Stop for owner adjudication if implementation requires any excluded mechanism,
cannot preserve one build per producer occurrence, cannot reject a perfect
caller-fabricated mapping, or cannot remain within the planned two-file source
and test surface.

## 13. Contradiction classification

| Question | Classification | Resolution |
|---|---|---|
| 1. Producer provenance inside `context.py` without a registry | `RESOLVABLE` | Use a producer-created in-process typed carrier with factory-only normal construction. |
| 2. No second context build | `RESOLVABLE` | One shared internal producer occurrence yields both the carrier and its ordinary representation. |
| 3. Public ResumeContext/CLI compatibility | `RESOLVABLE` | Keep `build_resume_context(...) -> dict` and default CLI serialization unchanged. |
| 4. Plain Mapping/JSON cannot confer provenance | `RESOLVABLE` | Trusted methods accept only the exact producer-bound carrier type, never Mapping-shaped substitutes. |
| 5. Symmetric start and expansion rule | `RESOLVABLE` | Both are produced through the same carrier-producing seam. |
| 6. Useful serialization with provenance loss | `RESOLVABLE` | Carrier export remains ordinary data; deserialization returns representation only. |
| 7. Two-file implementation boundary | `RESOLVABLE` | Carrier, shared producer, and projection stay in `context.py`; focused coverage stays in `test_context_resume.py`. |
| 8. Security/cryptography infrastructure | `RESOLVABLE` | Explicitly unnecessary and excluded; this is a normal-use architectural boundary. |
| 9. Leakage into Change 2 | `RESOLVABLE` | No cycle identity, attachment, semantic digest, or persistence is added. |
| 10. Scope beyond the original observability goal | `RESOLVABLE` | The amendment makes the original approved-seam meaning enforceable; it does not broaden the goal. |

```text
MATERIAL_CONTRADICTIONS: 0 / NONE
MATERIAL_LATER: hostile-code attestation and persistent cross-process provenance remain explicit non-goals
```

## 14. Current failed candidate and readiness disposition

```text
CURRENT_IMPLEMENTATION_CANDIDATE:
UNCOMMITTED / RE_REVIEW_FAIL / PENDING_AMENDED_AUTHORITY

PREDECESSOR_FORMAL_READINESS:
HISTORICAL_EVIDENCE_FOR_PREDECESSOR_PLAN / NO_LONGER_SUFFICIENT_FOR_FURTHER_EXECUTION

IMPLEMENTATION_CORRECTION: PAUSED
```

The failed candidate is retained as review history and is neither deleted nor
corrected by this transition. It is not acceptable under the approved amended
trust boundary until a later authorized correction and fresh independent
review prove the producer-bound discriminator.

Further implementation requires, in order:

1. a new owner-authorized Planning Authority checkpoint;
2. renewed read-only Formal Readiness with result `READY`; and
3. separate owner implementation authorization.

No earlier implementation authorization carries forward to the amended design.

## 15. Retention invariants

```text
RAW_TRANSCRIPT_COPY_INTO_PLANNING_LITE: FORBIDDEN
RAW_PROMPT_STORAGE: FORBIDDEN
RAW_RESPONSE_STORAGE: FORBIDDEN
SOURCE_BODY_COPY_FOR_OBSERVABILITY: FORBIDDEN
TOOL_PAYLOAD_OR_HIDDEN_REASONING_RETENTION: FORBIDDEN
PERSISTENT_PROVENANCE_RECORD: FORBIDDEN
HOST_RAW_TRANSCRIPT: EXTERNAL / OPTIONAL / RETENTION_DEPENDENT / NONAUTHORITY
PLANNING_LITE_OPERATION_MEMORY: COMPACT_DERIVED_METADATA_AND_SOURCE_REFS_ONLY
```

## 16. Approval state and next gate

```text
DEFINITION_AMENDMENT: APPROVED_BY_OWNER
OWNER_DEFINITION_AMENDMENT_DECISION: APPROVE
APPROVAL_AUTHORITY: USER / EXPLICIT / 2026-09-18
APPROVED_SOURCE_CANDIDATE_SHA256: 1FBB526271CD5C61DAD1C3ABEDE04C9EB3187C8627647DC69F381394841E7329
CANONICAL_ARTIFACT: docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-DEFINITION-AMENDMENT-v1.md
DEFINITION_AMENDMENT_REQUIRED: YES / SATISFIED_BY_THIS_APPROVAL
PLAN_AMENDMENT_REQUIRED: YES / APPROVED_SEPARATELY
RENEWED_PLANNING_AUTHORITY_REQUIRED: YES
RENEWED_FORMAL_READINESS_REQUIRED: YES
IMPLEMENTATION_CORRECTION_PAUSED: YES
NEXT_OWNER_GATE: OWNER_AUTHORIZATION_PL06_OPERATION_DEPTH_OBSERVATION_BRIDGE_AMENDED_PLANNING_AUTHORITY_CHECKPOINT
```

This approval does not create the amended Planning Authority checkpoint, run
renewed Formal Readiness, authorize source/test mutation, authorize staging or
commit, or consume the major PL09 next-slice gate. The prior implementation
authorization does not carry forward.
