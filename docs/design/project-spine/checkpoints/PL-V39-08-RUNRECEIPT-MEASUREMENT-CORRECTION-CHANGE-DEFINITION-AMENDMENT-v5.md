# PL-V39-08 RunReceipt Measurement Correction - Definition Amendment v5 Candidate

## 1. Candidate identity and authority

Prior candidate reviews:
Amendment v3: REVIEW_FAIL / 2 MATERIAL FINDINGS
Amendment v4: REVIEW_FAIL / 1 MATERIAL FINDING
Reviewed v4 candidate:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v4.md
V4 review checkpoint:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v4-REVIEW-v1.md
V4 review checkpoint SHA256: ae70817b4627d24378fd16c49903af65ad4ceda48530e6fb5f6e2ab770014334
Correction scope: V4-01 BOUNDED_COMPLETE_TOTAL_QUALITY_CONTRADICTION only. V3_01 and V3_02 remain CLOSED_BY_V4. V3 and v4 remain unchanged as failed-review history.

Prior candidate reviewed:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v3.md
Prior candidate disposition: REVIEW_FAIL / 2 MATERIAL FINDINGS
Review checkpoint:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v3-REVIEW-v1.md
Review checkpoint SHA256: 6ccd67473c613ea5dfb23c4edee2edcd9037f40f0372f863991db94af1ffc667
Correction scope: V3-01 and V3-02 only. The v3 candidate remains unchanged as failed-review history.

Document ID: PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-DEFINITION-AMENDMENT-005
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001
Lineage: CHANGE_3
Status: CANDIDATE_FOR_OWNER_REVIEW
Activation: NOT_ACTIVE
Implementation authority: NO_IMPLEMENTATION_AUTHORITY
Owner-selected direction: ROUTE_B_PROVIDER_NEUTRAL_COARSE_EFFICIENCY_MEASUREMENT
Owner decision: SELECT_ROUTE_B_PROVIDER_NEUTRAL_COARSE_EFFICIENCY_MEASUREMENT
Approval: NOT GRANTED
Review: NOT_REVIEWED
Plan Amendment: REQUIRED AFTER DEFINITION ACCEPTANCE
09-G: NOT STARTED

Owner decision checkpoint:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-PROVIDER-NEUTRAL-COARSE-EFFICIENCY-OWNER-DECISION-v1.md
SHA256: 80d0f6265516529e82faf73cb09e82af3730a0b2f601e8e704ebe83cf07360e5

Predecessor Definition:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-v1.md
SHA256: cef899a6a6b2ced4d1bef1e266969cd2b57981d5b59275b77e8e093e2d9d21cc

Existing active Definition Amendment v2:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-CHANGE-DEFINITION-AMENDMENT-v2.md
SHA256: e7a47f46c9838ba94ae66acea56c76768e72844a881bf394cfa8fd28bbafa544

Existing active Plan Amendment v5:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-IMPLEMENTATION-PLAN-AMENDMENT-v5.md
SHA256: e9f2d09f4f8bac0fef81f8a9c79630cf8c65edd6b9084406fd2c9242a9430981

Accepted T00 review:
docs/design/project-spine/checkpoints/PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-RESPONSE-AGGREGATE-T00-CONTROLLED-DISCOVERY-REVIEW-v1.md
SHA256: 790ac10491c0d175cb099c45b00903bf61ea088e2fd0fe11da1d47d631f066dd

Until separate owner acceptance and activation, the effective authority
remains the predecessor Definition plus Amendment v2 and the predecessor Plan
plus Plan Amendment v5. This candidate does not activate Route B or change
that authority. If accepted and activated, Amendment v5 adds to the Definition
chain and supersedes only conflicting clauses identified below. A Plan
Amendment is required before Formal Readiness or implementation of the amended
scope.

## 2. Purpose and proposed capability

The owner selected Route B: Change 3 should provide provider-neutral,
coarse-grained resource observations usable by later Planning Lite efficiency
analysis. The MVP reports provider-native resource use at the strongest scope
its source evidence supports.

COARSER TRUTH IS PREFERRED TO FINER GUESSED ATTRIBUTION.

A truthful Resource Observation may use a scope coarser than a Planning Lite
Attempt. Missing Attempt binding does not invalidate it. Exact Attempt
attribution is a deferred precision upgrade, not an MVP prerequisite.

Change 3 supplies resource evidence. It does not decide which configuration,
provider, model, route, prompt, skill, or checklist is better or more
efficient.

## 3. Provider-neutral Resource Observation

The semantic object belongs to Planning Lite, not a Codex-specific record. It
represents provider-native resource quantities for one declared scope, with
source and configuration provenance, method, quality, completeness, and
limitations needed to interpret the claim.

The semantic contract requires these concepts, without freezing persisted field
names:

- observation identity;
- declared scope and scope identity/boundaries;
- source and provenance references;
- provider and model where known or available;
- configuration reference where applicable;
- measurement method and quality;
- provider-native usage semantics and supported quantities;
- explicit scope and metric completeness/limitations;
- optional provider-specific evidence references.

The request and source bind the observation to the declared scope before
aggregation. Provider-specific identifiers may be retained as provenance;
they are not mandatory universal Planning Lite identity fields. The core
contract does not require Codex thread, turn, response, or Attempt IDs for
every observation.

Configuration identity may reference prompt, skill, checklist, provider,
model, Planning Lite version, comparison arm, or another relevant
configuration. A reference, fingerprint, or external identity is sufficient.
Change 3 does not build a Prompt Registry or Experiment Registry.

## 4. Scope and attribution granularity

Scope answers what the resource quantity belongs to. It is independent from
measurement quality.

| Scope | Meaning | Required limit |
|---|---|---|
| WORK_WINDOW | A predeclared bounded evaluation/work period associated with one known configuration or comparison arm. | Quantity belongs to the window as a whole; no allocation to individual Attempts is claimed. |
| PROVIDER_SESSION | Resource use belonging to one provider session/thread where its source supports that boundary. | No equivalence to Planning Lite Attempts is implied. |
| PROVIDER_TURN | Resource use belonging to one provider turn where its source supports that boundary. | No Attempt ownership is implied unless separately proven. |
| PLANNING_ATTEMPT | Resource use belonging to one exact existing Planning Lite Attempt. | Precision scope requiring authoritative attribution; otherwise the Attempt observation is UNAVAILABLE. |

A work window is bounded before measurement and has a stable identity. A
comparison arm identifies its configuration. If configuration changes within
a purported arm, represent separate scopes or disclose the change; do not
assign the combined total to one configuration retrospectively.

Scope must not be narrowed after records are missing merely to make an
incomplete total appear complete. A material source subset or boundary is
declared and visible.

WORK_WINDOW source membership is independent from its temporal boundary. A
valid window requires stable window and configuration/comparison-arm
identities, declared start and closure semantics, and a prospective
deterministic membership rule with explicit inclusion and exclusion criteria.
Declare the rule before or at the first registration decision for each source.
Concrete future sessions/files need not be known before the window opens;
sources may be registered deterministically as they appear.

The interval defines the temporal boundary only. Timestamp overlap alone does
not establish resource membership. Valid provider-neutral mechanisms may
include a dedicated provider session bound to the window, sessions explicitly
registered to it, records carrying an independently reliable
window/configuration binding, or another deterministic rule.

For each concrete source, retain auditable provenance: stable source/session
identity; window and configuration/arm identity; binding evidence/reference;
membership-rule identity and version; registration event/provenance; and the
inclusion or exclusion decision and reason. Prohibit timestamp-only membership,
post-hoc semantic/content selection, prompt/body classification as authoritative
binding, latest/nearest/proximity selection, and retrospective cherry-picking.

If a source contains inseparable target-configuration and unrelated work, its
whole total cannot be DIRECT usage for the target configuration or complete
WORK_WINDOW. A narrower claim is allowed only when its target subset and
numeric meaning are independently truthful and explicitly bounded under
Section 5; do not call it a complete configuration-window total. Otherwise
use UNAVAILABLE. Failure to prove PLANNING_ATTEMPT attribution invalidates
that fine-scope claim only; an independently supported WORK_WINDOW,
PROVIDER_SESSION, or PROVIDER_TURN observation may remain valid.

Critical example: a predeclared one-week Poker work window for prompt/skill/
checklist variant B has a source-bound Codex/model reference and an exact
deterministic sum of valid provider-native usage records covering the declared
window. It is a valid WORK_WINDOW Resource Observation, with no Attempt
attribution claim. It is not rejected merely because Q1 Attempt-to-turn binding
or Q2 Attempt-to-response ownership is unproven.

## 5. Scope, quality, numeric claim kind, and completeness

These are separate semantic axes:

1. SCOPE identifies the declared entity and boundary: WORK_WINDOW,
   PROVIDER_SESSION, PROVIDER_TURN, or PLANNING_ATTEMPT.
2. QUALITY describes how strongly the evidence supports the numeric claim:
   DIRECT, BOUNDED, or UNAVAILABLE.
3. NUMERIC CLAIM KIND states exactly what the number means.
4. COMPLETENESS describes whether expected member sources and requested or
   optional metrics are present, absent, partial, or unknown.

A numeric Resource Observation exposes its claim kind through structured
semantics, without requiring a consumer to infer it from prose. The definition
freezes these meanings, not persisted field names or serialization layout.
Use this small semantic vocabulary:

| Numeric claim kind | Meaning |
|---|---|
| COMPLETE_SCOPE_TOTAL | Exact total for the entire declared scope. All expected member sources and resources within that scope are included and source-supported or exactly aggregated. |
| EXACT_OBSERVED_SUBSET | Exact total only for the explicitly identified observed subset of the declared scope. It says nothing about unobserved sources or the larger scope total. |
| PROVEN_LOWER_BOUND | A source-supported minimum for the declared scope, with evidence that proves the lower bound. It is not a total. |
| OTHER_PRECISELY_DEFINED_NONCOMPLETE_CLAIM | Another precisely stated numeric claim that does not assert a complete total for the declared scope; its subject, boundary, evidence, and comparison limits are explicit. |

### DIRECT

For a numeric quantity covering the entire declared scope, with complete
membership and source coverage for that claim and an exact source-supported or
deterministic aggregation:

QUALITY: DIRECT
NUMERIC CLAIM KIND: COMPLETE_SCOPE_TOTAL

A complete whole-scope total must not remain BOUNDED merely because BOUNDED is
available as a weaker label. If a requested optional metric is absent, each
supported whole-scope quantity may still be DIRECT with
COMPLETE_SCOPE_TOTAL; report the missing metric on the separate completeness
axis as PARTIAL.

A narrower scope has its own total. If S1 is one complete, authoritative
provider session, a separate observation may be PROVIDER_SESSION / S1 with
DIRECT / COMPLETE_SCOPE_TOTAL. That does not make S1's value the complete
WORK_WINDOW total containing S1.

### BOUNDED

For the declared scope, BOUNDED never claims COMPLETE_SCOPE_TOTAL. Valid
bounded numeric claim kinds include EXACT_OBSERVED_SUBSET,
PROVEN_LOWER_BOUND, or OTHER_PRECISELY_DEFINED_NONCOMPLETE_CLAIM. Each names
the actual subject/source set and makes its limitation explicit. Do not
silently compare a bounded subset or lower bound as a complete-scope total.

Example: Poker week / prompt B expects member sources S1, S2, and S3. S1 and S2
have exact observed usage; S3 is not observed or truthfully quantifiable. The
WORK_WINDOW claim may be BOUNDED / EXACT_OBSERVED_SUBSET for S1 + S2, with
those sources named. It is not BOUNDED / COMPLETE_SCOPE_TOTAL for the work
window. If no useful truthful bounded claim is supportable, use UNAVAILABLE.

If source evidence proves usage is at least 7M while additional usage may
exist, report BOUNDED / PROVEN_LOWER_BOUND / 7M for the declared scope, with
the evidence for the bound. Do not label it a total.

If only an unknown fraction is visible and no useful exact subset, proven
lower-bound, or other precise bounded claim exists, use UNAVAILABLE.

### Comparison safety

A consumer must be able to determine from structured semantics, without prose,
whether two values are comparable as complete totals for equivalent declared
scopes. DIRECT / COMPLETE_SCOPE_TOTAL must not be silently treated as
equivalent to BOUNDED / EXACT_OBSERVED_SUBSET or BOUNDED /
PROVEN_LOWER_BOUND. Scope identity, claim kind, quality, source membership,
provider-native semantics, and completeness remain available to that decision.

No extrapolation, scaling, statistical filling, or guessed missing usage is
allowed. No ESTIMATED quality tier is required for this MVP. Statistical
estimation is not smuggled into BOUNDED. Any future estimated tier needs a
separate amendment and must never manufacture Attempt attribution.

## 6. Provider-native quantities and completeness

Resource quantities retain provider-native meaning and provenance. Optional
token-like quantities may include input, cached input, output, reasoning, and
total usage. No provider must expose every quantity, and providers may expose
different resource dimensions.

Report only source-supplied values or values derived exactly under the
provider's defined semantics. An absent or unsupported optional metric is
null/absent with explicit completeness information, not zero unless the source
supports zero or an allowed exact derivation proves zero. Completeness is
separate from scope and quality and discloses source coverage and which
requested/optional metrics are present, absent, partial, or unknown. Missing an
optional metric does not fabricate zero or erase another truthful metric. If a
missing metric is necessary for the requested claim, that claim is UNAVAILABLE.
Consumers must distinguish measured zero from absent, unsupported, incomplete,
and unavailable values.


Quality describes the epistemic claim justified for each numeric quantity.
Completeness describes which expected sources and requested/optional metrics
are present, absent, partial, or unknown. These axes are independent. Exact
whole-window input and output totals with an absent optional reasoning metric
may remain DIRECT for the supported quantities while metric completeness is
PARTIAL. If only some member-source records are observed, populated fields on
those records do not make a complete-window total DIRECT; report a truthful
bounded claim for the actual subject or UNAVAILABLE.

Derive relations such as cached plus uncached input equals input only when the
source defines fields compatibly and values cover the same scope. Existing v1
delta equations remain specific to boundary-delta meaning. A provider-native
total is never written into a legacy delta field. A numeric value alone does
not prove source, scope, completeness, configuration, or attribution.

## 7. Explicit requests and E1

NO REQUEST -> NO_MEASUREMENT_CLAIM

Change 3 adds no automatic measurement obligation for every Attempt and makes
no universal coverage claim.

General v5 eligibility comes from an explicit source-bound resource
observation request for one declared scope. It binds enough information for
scope and boundaries, source/provenance, provider/model where available,
configuration where applicable, requested quantities, and method or method
constraint. A coarse request does not need an Attempt ID merely to become
eligible. It must prevent recency, timestamp, latest-record, or proximity
heuristics from choosing a source after execution.

Existing E1 is SPECIALIZED to PLANNING_ATTEMPT. That request names one exact
existing Attempt and the authoritative source needed to prove its Attempt
binding. If attribution cannot be proven, the Attempt-scoped observation is
UNAVAILABLE. E1 is not the sole eligibility rule for all Resource
Observations.

A request grants no routing, execution, measurement-policy, or project-state
authority. This candidate does not implement a request interface or collector.

## 8. Scope-specific finalization

A request produces a final Resource Observation only when its declared scope
is finalizable under its source contract. Examples are a closed work window,
a provider session with supported closure, a completed provider turn where
supported, or a completed exact Attempt with authoritative evidence.

If the scope is still open or not finalizable, return
REQUEST_NOT_YET_FINALIZABLE, append no final observation, and allow retry when
the scope becomes finalizable. This invocation state is not a final
UNAVAILABLE observation. A terminal source condition proving the scope cannot
be completed may produce UNAVAILABLE with an explicit reason.

Codex task_complete is not a universal finalization primitive. A work window
or provider session may use another explicitly supported closure boundary.
Lack of task_complete does not prove every coarse scope is impossible.

## 9. Methods and provider adapters

Methods are evidence-production strategies behind the provider-neutral
contract; none defines the universal ontology.

- RESPONSE_AGGREGATE may remain a provider-specific strategy when stable,
  source-bound native records cover the declared scope with required identity
  and completeness. Exact Attempt response mode is optional precision and
  requires exact Attempt-to-source and response-scope ownership.
- BOUNDARY_DELTA may remain where compatible source-native before/after
  counters, same-session continuity, scope, boundaries, and deterministic
  subtraction are proven. Cross-session subtraction remains forbidden.
- Provider-native or window aggregation may be used where the source provides
  an exact total or complete source-native records for the declared coarse
  scope.

No method repairs missing evidence by changing scope after the fact, mixing
incompatible counters, choosing a source by recency, or allocating a coarse
total among Attempts. Method, source identity, and native semantics remain
explicit.

Adapters may understand Codex thread/turn/response IDs, Claude request/message
IDs, Gemini IDs, Qwen IDs, or future provider telemetry. Such IDs may be
provenance; none is a mandatory universal Planning Lite identity.

Q7 proves structural feasibility for typed sibling storage in existing
telemetry/capture owners; it does not require operation_measurement_v2 as the
only carrier or a new store. Any eventual representation must preserve
backward compatibility and be additive/versioned where needed. Exact record
type, persistence file, mixed-stream layout, modules, and APIs belong to a
separately reviewed Plan and implementation design.

## 10. Provider neutrality and cross-provider comparison

Freeze this invariant:

PROVIDER_NATIVE_TOKEN_COUNT IS NOT A UNIVERSAL CROSS_PROVIDER PHYSICAL UNIT

Keep provider, model, native usage semantics, method, scope, quality, and
provenance attached to each observation. Direct relative token comparisons are
strongest when provider/model and relevant conditions are sufficiently stable.
A raw token ratio across providers or models is not a complete efficiency
verdict. Keep incompatible native quantities separate; do not silently sum
them into a comparable total. A normalized cross-provider contract is outside
this amendment.

## 11. Resource observation is not an efficiency judgment

Freeze:

RESOURCE OBSERVATION != EFFICIENCY JUDGMENT
TOKEN_SAVINGS_ALONE_SUFFICIENT_FOR_EFFICIENCY_JUDGMENT: NO
UNIVERSAL_EFFICIENCY_SCALAR_REQUIRED: NO

Change 3 may provide a vector of resource observations to later consumers. It
does not decide whether a configuration is globally better, whether fewer
tokens outweigh lower quality, which provider is better, or whether to promote
a configuration.

Later analysis may consider accepted outputs and plan/task items,
quality/correctness, rework, retries, review/readiness loops, owner
interventions, resource use, meaningful wall-clock time, and available cost.
Intended initial comparisons are coarse material differences such as
approximately doubled context, substantially reduced resource use, materially
more rework for similar spend, or materially better accepted output for similar
spend. Differences near ten percent are not the current primary target. No
fixed statistical tolerance is promised.

## 12. T00 findings and scope-specific applicability

Accepted T00 findings remain valid. Amendment v5 changes which facts are
required for which scope; it does not redefine evidence or close a seam.

| Question | Accepted finding | Proposed v5 applicability |
|---|---|---|
| Q1 | AUTHORITATIVE_ATTEMPT_TO_CODEX_TURN_BINDING_NOT_PROVEN | Blocks exact PLANNING_ATTEMPT attribution when required; does not block an independently source-bound session, turn, or window. |
| Q2 | ATTEMPT_RESPONSE_SCOPE_OWNERSHIP_NOT_PROVEN | Blocks assigning response usage to an exact Attempt; not a provider turn/session/window total with independently proven boundary and completeness. |
| Q3 | POST_TURN_MEASUREMENT_PRODUCER_TRIGGER_NOT_PROVEN | Blocks the old exact-Attempt E1 producer path as designed; does not prove a separately requested coarse source-bound observation impossible. |
| Q4 | POST_TURN_COMPLETION_SIGNAL_NOT_PROVEN | Blocks using Codex task_complete as authoritative exact-response closure; coarse scopes may finalize under their own supported closure boundary. |
| Q5 | BOUNDED STABLE PROVIDER-SOURCE READ FEASIBLE | Reusable within the inspected bounded source contract; not proof for every provider. |
| Q6 | CODEX STRUCTURED NATIVE USAGE RECORDS USABLE | Reusable Codex-native evidence only; not mandatory for every provider. |
| Q7 | TYPED SIBLING STORAGE STRUCTURALLY FEASIBLE / NO NEW STORE REQUIRED | Feasibility only; selects no carrier and authorizes no storage implementation. |
| Q8 | EIGHT-PATH SURFACE SUFFICIENT FOR THE PRIOR EXACT-RESPONSE DESIGN ONLY | Does not establish the provider-neutral MVP write surface; later Definition/Plan must re-evaluate it. |

Four official not-proven material seams remain: roots Q1, Q2, Q4 and dependent
Q3. No seam is fixed or removed from the T00 record. Applicability is limited
to the claim and scope each fact constrains. This candidate infers no daemon,
scheduler, host hook, or new store.

## 13. Failure, conflict, replay, and false precision

A requested observation is UNAVAILABLE when its source cannot support the
declared boundary or necessary quantity; source identity or scope is ambiguous;
source completeness prevents a truthful claim; provider-native semantics
conflict; or deterministic processing leaves an unresolved conflict.

For the same observation identity, scope, source set, method, and evidence,
replay preserves the same semantic result. Duplicate source records are handled
deterministically under adapter identity rules. Conflicting duplicate
identities or values fail closed for the affected claim; never silently choose
the newest or last record.

Different declared scopes may produce distinct observations over overlapping
records. They are not merged into a competing total. A coarse observation never
becomes an Attempt observation by division or inference.

Prohibit:
- equal division of a session/window total among Attempts;
- timestamp-proportional allocation;
- nearest-turn or latest-turn attribution;
- inference from absence of another visible Attempt;
- deriving token counts from output length or another proxy;
- cross-provider token normalization without a later reviewed contract;
- converting missing/unsupported metrics to zero;
- presenting partial/unknown source coverage as a complete total;
- changing scope after observation to hide a limitation.

Unknown finer attribution remains unknown.

## 14. Backward compatibility and carrier boundary

Preserve RunReceipt v1/v2 meanings, cumulative token fields, existing
identities, and historical receipt contents. Never reinterpret cumulative
values as operation-local. Existing v1 measurement and *_delta fields retain
BOUNDARY_DELTA meaning. Do not write response, session, work-window, or other
provider-native totals into legacy delta fields.

Historical SAFE/UNAVAILABLE evidence remains readable under the scope and
contract in force when recorded. No old receipt is backfilled or migrated; no
historical SAFE result is retroactively reclassified.

A future implementation may add a versioned Resource Observation carrier.
This candidate freezes no serialization, storage location, record_type,
mixed-stream layout, module, or CLI. operation_measurement_v2 is not mandated
as the only carrier for provider-neutral coarse observations merely because it
was proposed in Plan Amendment v5. Q7 is feasibility evidence, not a storage
decision.

Measurements remain evidence. They do not own Attempt identity, configuration
authority, expected route, execution authority, project state, or efficiency
policy. Route references may be retained for a particular operation
comparison; they are not required for every work-window observation.

## 15. Relationship to predecessor semantics

These proposed dispositions take effect only after separate review, owner
acceptance, and activation.

| Predecessor clause or term | v5 disposition | Proposed treatment |
|---|---|---|
| RunReceipt v1/v2 cumulative fields and historical receipts | PRESERVED | Keep exact meanings; no reinterpretation, migration, or backfill. |
| v1 measurement fields and delta equations | PRESERVED | Keep BOUNDARY_DELTA and *_delta meanings; other-scope totals need an additive compatible representation. |
| SAFE / UNAVAILABLE for operation-local claims | GENERALIZED | Legacy labels stay unchanged; new scope-declared observations use DIRECT / BOUNDED / UNAVAILABLE. Exact Attempt claims still need authoritative attribution. |
| RESPONSE_AGGREGATE as preferred exact operation/Attempt path | SPECIALIZED | Provider-specific strategy at supported scopes; exact Attempt response mode is optional precision, not universal MVP. |
| BOUNDARY_DELTA as independent fallback | SPECIALIZED | Retain only where compatible source boundaries, continuity, scope, and subtraction are proven. |
| Option C as preferred active Change 3 direction | SUPERSEDED | Route B is proposed for the amended MVP. Until activation, Option C remains effective v2 authority; RESPONSE_AGGREGATE may remain optional precision. |
| E1 explicit post-turn request for one exact Attempt | SPECIALIZED | Retain stronger constraints for PLANNING_ATTEMPT; general v5 eligibility is an explicit source-bound request for a declared scope. |
| NO_MEASUREMENT_CLAIM when there is no request | PRESERVED | No request means no claim; no automatic all-Attempt measurement or coverage duty. |
| REQUEST_NOT_YET_FINALIZABLE | GENERALIZED | Keep as a non-final invocation state for any scope whose source contract has not closed. |
| Exact Attempt binding and response ownership | SPECIALIZED | Required for PLANNING_ATTEMPT claims; failure blocks that scope, not an independently valid coarse claim. |
| Telemetry completeness and explicit missing values | GENERALIZED | Keep legacy meanings; disclose new scope/source coverage and optional metric presence separately from scope and quality. |
| WORK_WINDOW temporal boundary and source membership | GENERALIZED | Time defines the boundary only; a prospective deterministic rule and auditable per-source binding establish membership. |
| Numeric claim kind and comparison safety | GENERALIZED | Structured semantics distinguish COMPLETE_SCOPE_TOTAL from bounded noncomplete subset, lower-bound, or other claims; consumers can determine complete-total comparability. |
| Quality and completeness axes | GENERALIZED | Quality describes the supported numeric claim; completeness describes expected source and metric coverage. Neither substitutes for the other. |
| Replay, idempotence, duplicate, and conflict semantics | PRESERVED | Same evidence replays deterministically; unresolved conflicts fail closed. |
| Root/child response-scope constraints | SPECIALIZED | Apply ownership limits to claims covering those records; root-only evidence does not imply whole-tree completeness. |
| Historical backward readability and append-only evidence | PRESERVED | Read historical evidence with original semantics; no backfill or mutation. |
| Measurement does not own route, authority, or economics policy | PRESERVED | Observations do not select routes, authorize execution, or make efficiency judgments. |

## 16. Minimum semantic success criteria

A later authorized semantic MVP must support:

1. one explicit provider-neutral Resource Observation request;
2. one coarse scope not requiring exact Attempt attribution;
3. source-bound provider-native resource values;
4. provider/model/native-semantics provenance where available;
5. explicit scope and attribution granularity;
6. quality independent from granularity;
7. honest source/metric completeness and null/absent optional metrics;
8. no false finer attribution or fabricated zero;
9. unchanged historical RunReceipt semantics; and
10. prospective, auditable WORK_WINDOW source membership;
11. explicit bounded numeric claim semantics and independent completeness;
12. a resource result usable by later analysis without Change 3 making an
    efficiency judgment.

These are future acceptance criteria, not evidence of implementation.

## 17. Adversarial Definition cases

These are contract answers, not executed product tests.

| Case | Input | Required result |
|---|---|---|
| D3-A01 | Exact Codex session usage is known, but cannot be bound to an Attempt. | A source-supported PROVIDER_SESSION observation may be DIRECT or BOUNDED as evidence warrants; make no Attempt claim. |
| D3-A02 | Exact native usage is known for a Poker work window spanning several Attempts. | Valid WORK_WINDOW observation; do not divide or assign the total among Attempts. |
| D3-A03 | Caller asks for Attempt usage, but only a session total exists. | PLANNING_ATTEMPT is UNAVAILABLE; a separately requested valid PROVIDER_SESSION observation may remain valid. |
| D3-A04 | Provider A reports 1,000,000 tokens and Provider B reports 900,000. | Do not conclude Provider B is universally 10% more efficient from raw counts alone. |
| D3-A05 | Optional cached-input or reasoning metric is absent. | Null/absent plus completeness semantics; never invent zero. Other truthful metrics may remain reportable. |
| D3-A06 | No explicit resource observation request exists. | NO_MEASUREMENT_CLAIM. |
| D3-A07 | Requested work window is still open. | REQUEST_NOT_YET_FINALIZABLE; append no final observation; retry after supported closure. |
| D3-A08 | Exact Attempt bridge later becomes available for one provider. | That provider may support PLANNING_ATTEMPT when all proof exists; provider-neutral core stays unchanged. |
| D3-A09 | Claude/Gemini/Qwen adapter uses provider-specific identifiers. | Permit them as adapter provenance; keep core contract unchanged. |
| D3-A10 | Coarse observation has 50% fewer tokens but twice the rework. | Change 3 reports resource use only; it declares no efficiency winner. |
| D3-A11 | Provider lacks response-level usage but exposes exact session-level usage. | A source-supported PROVIDER_SESSION observation may be valid; response records are not a universal prerequisite. |
| D3-A12 | Implementation divides session tokens by Attempt count. | REJECT as false precision; inferred Attempt allocations are UNAVAILABLE. |

| D4-A13 | A dedicated provider session is prospectively bound and registered to Poker B under the declared membership rule. | It may be a valid WORK_WINDOW member; preserve its binding, rule/version, registration, and inclusion reason. |
| D4-A14 | A session overlaps Poker B's week by timestamp only. | Do not include it solely because of temporal overlap; time defines a boundary, not membership. |
| D4-A15 | One session contains inseparable Poker B and unrelated work. | Its whole total cannot be DIRECT Poker-window usage. Use a truthful, explicitly bounded narrower claim if one exists; otherwise UNAVAILABLE. |
| D4-A16 | Arm A has a DIRECT complete-window total of 10M; Arm B has BOUNDED 7M from an explicit observed subset. | The 7M is labelled as an exact subset or other precise bound, never as Arm B's complete-window total. |
| D4-A17 | Only an unknown fraction of a declared work window is observable. | Report a useful truthful bounded claim only if its subject and numeric meaning are explicit; otherwise UNAVAILABLE. Never extrapolate or scale. |
| D4-A18 | Whole-window input and output are exact, while optional reasoning usage is absent. | Supported quantities may remain DIRECT; metric completeness records the absent optional metric and is PARTIAL. |

| D5-A19 | WORK_WINDOW A has full prospective membership and an exact complete provider-native total. | Supported quantities are DIRECT / COMPLETE_SCOPE_TOTAL. Do not label that same whole-scope total BOUNDED without another noncontradictory, explicitly defined semantic reason. |
| D5-A20 | WORK_WINDOW B expects S1, S2, and S3; S1 and S2 are completely observed, while S3 has unknown usage. | Their exact sum may be BOUNDED / EXACT_OBSERVED_SUBSET with S1 and S2 named. It is not COMPLETE_SCOPE_TOTAL for WORK_WINDOW B; if no useful bounded claim is supportable, use UNAVAILABLE. |

All 20 cases have explicit expected outcomes in this candidate. No product
test was run by this drafting transition.

## 18. Out of scope

Amendment v5 does not include or authorize:

- full Experiment Registry;
- Prompt Garden implementation;
- universal Efficiency Score;
- cross-provider normalized token unit;
- cost-per-accepted-plan engine;
- full Operational Insights;
- historical calibration;
- statistical significance or fixed tolerance framework;
- automatic framework optimization;
- PL-V39-09-G orchestration or semantics;
- exact Codex Attempt bridge implementation;
- Claude/Gemini/Qwen adapters themselves;
- new persistence infrastructure;
- historical receipt backfill;
- implementation CLI or product schema mutation;
- corrective candidate disposition.

## 19. Governance boundary and next gate

This document is CANDIDATE_FOR_OWNER_REVIEW, NOT_ACTIVE, and grants
NO_IMPLEMENTATION_AUTHORITY. It corrects V3-01 and V3-02 from the failed v3
review; v3 remains unchanged as failed-review history. Current Formal Readiness closure remains
BLOCKED_AFTER_CONTROLLED_DISCOVERY. The effective Definition remains the
predecessor plus Amendment v2; the effective Plan remains the predecessor
plus Plan Amendment v5. The existing Plan cannot authorize implementation of
semantics not yet active, and operation_measurement_v2 is not selected here
as the amended MVP carrier.

The preserved corrective candidate remains unchanged with disposition
unresolved. Q1-Q4 remain valid not-proven T00 findings; Q5-Q8 remain accepted
within their bounded scope. No T00 reexecution, product/test change, Roadmap
change, Formal Readiness, 09-G work, stage, commit, push, release, or
implementation is authorized.

After independent review and resolution of any findings, the next governance
action is an explicit owner review:

OWNER_REVIEW_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_DEFINITION_AMENDMENT_V5

Separate owner acceptance and activation are required before Amendment v5
becomes effective. A Plan Amendment must then be prepared, reviewed, accepted,
and activated, followed by separate Formal Readiness before implementation
authorization can be considered.
