# PL-V39-08 Implementation Plan v1

## 1. Plan Identity

```text
Change: CHG-PL-V39-08-GOVERNED-ATTEMPT-EVALUATION-001
Plan status: FROZEN / OWNER-APPROVED
Prepared on: 2026-09-07
Definition authority SHA: 6c5ba10d3b3bbf978451623be3243822c7525d2d
Primary capability: GOVERNED_ATTEMPT_EVALUATION
Implementation phases: 2
Implementation authorization: NO
Formal Readiness: NOT RUN
Implementation tasks: NOT STARTED
Owner adjudication: seven review findings classified as PLAN_CONTRACT_DEFECT and/or PLAN_TESTABILITY_DEFECT
Definition amendment: NO
Task-count change: NO
Write-surface expansion: NO
```

This Plan describes later implementation and proof work. It grants no product,
template, test, staging, commit, consumer, or lifecycle authority.

## 2. Definition Authority Binding

The frozen Definition is:

```text
docs/design/project-spine/checkpoints/PL-V39-08-PROPOSED-CHANGE-DEFINITION-v1.md
Git authority: 6c5ba10d3b3bbf978451623be3243822c7525d2d
```

The Plan preserves its ten ACs, exact Attempt discriminator, evaluation
precedence, orthogonal Finding model, evidence applicability/supersession,
partial baseline, non-authoritative technical acceptance, and 07/08/09
boundary. It introduces no Definition amendment.

The cache-ready Prompt Composition refinement is within Definition AC-01,
AC-06, AC-07, AC-09, and AC-10: it records prompt/context provenance associated
with an Attempt and supports bounded comparison. It neither assembles nor
executes context and remains evidence only.

```text
DEFINITION_BINDING: PASS
DEFINITION_DRIFT: NO
DEFINITION_AMENDMENT_REQUIRED: NO
AC_COUNT: 10
```

## 3. Delivery Strategy

Delivery is split at the semantic dependency boundary:

```text
08-B — GOVERNED_ATTEMPT_EVALUATION
Attempt/evidence/evaluation substrate
→ independent bounded review
→ separate owner continuation gate
→ 08-C — CONTROLLED_LEARNING_AND_PROMPTOPS_EVIDENCE
Prompt composition provenance, comparison, recommendations, and fixture
```

08-B is independently useful and testable without 08-C. The intermediate
review does not require a commit or release. 08-C may begin only after 08-B
review has no unresolved blocking contract/evidence defect and the owner
separately authorizes continuation.

One cohesive pure module owns both phases so the second phase extends the
evidence model instead of creating another subsystem. Managed templates expose
only compact evidence fields. One cumulative Execution Ledger carries T-01…T-11
evidence; one Completion Review performs final technical reconciliation.

## 4. Existing-Surface Reconciliation

| Existing surface | Decision | Reason |
|---|---|---|
| `execution_guidance.py::OperationGuidanceV1` | `REUSE BY REFERENCE / NO MODIFY` | Supplies selected operation, authority, capability, result, and evidence refs. Evaluation consumes those refs but must not select or authorize an operation. |
| `telemetry.py::RunReceipt v1` | `REFERENCE AS OPTIONAL EVIDENCE / NO MODIFY` | It is a strict externally supplied runtime/usage receipt with collector-owned source identity. Expanding its exact schema would conflate telemetry with governed evaluation. |
| `campaign/**` attempt/journal/review code | `DO NOT GENERALIZE / NO MODIFY` | It owns campaign budgets, candidates, transitions, and append-only campaign state. Reusing it would import a forbidden lifecycle engine and campaign semantics. |
| `context.py::ResumeContextV1` | `REFERENCE / NO MODIFY` | Supplies current authority and Git/current facts. Attempt evaluation must not become another context builder or current-state authority. |
| change `progress.md` template | `EXTEND` | It is the existing cumulative evidence surface but lacks deterministic Attempt, verifier, evaluation, and composition fields. |
| change `review.md` template | `EXTEND` | It already owns technical Completion Review and owner-closure separation; it needs exact evaluation/finding/supersession references. |
| recommendation `TEMPLATE.md` | `EXTEND` | It already owns non-authoritative recommendation evidence and lifecycle; it needs source Attempt/Finding/composition provenance and explicit no-auto-promotion semantics. |
| Git SHA and SHA receipt conventions | `REUSE` | They already provide reconstructable source identity and canonical template integrity. |

The missing product seam is a pure, domain-focused contract/evaluator. It
cannot safely live in `execution_guidance.py` because that module owns
pre-execution selection; in `telemetry.py` because RunReceipt v1 is external
telemetry; or in Campaign because Campaign owns a state machine. Therefore one
minimal module, `src/planning_lite/attempt_evaluation.py`, is justified.

## 5. 08-B Architecture

08-B implements immutable/validated JSON-compatible records and pure functions:

```text
existing authority and OperationGuidance refs
+ bounded candidate/input identity
→ AttemptRecordV1
+ ObservedResultV1
+ required VerifierContractV1 declarations
+ VerifierEvidenceV1
+ applicable FindingV1 records
→ TechnicalEvaluationV1
```

The module performs no filesystem, Git, network, provider, CLI, lifecycle, or
template mutation. Callers supply already-observed refs/facts. Construction and
evaluation validate exact schemas and fail closed; persistence remains the
existing ledger/review responsibility.

08-B exposes a nullable `prompt_composition_ref` on the Attempt input contract.
It is an opaque evidence identity in this phase. 08-B does not compare prompt
compositions or derive learning recommendations.

## 6. 08-C Architecture

08-C extends the same pure module with:

```text
PromptComponentRefV1
PromptCompositionRefV1
ContextResidencyClass
StablePrefixIdentity derivation
PromptCompositionComparisonV1
non-authoritative recommendation evidence
```

It consumes Attempt and Finding records from 08-B. Comparison returns small
facts and evidence references, never a quality score, authority decision, file
mutation, provider operation, or automatic recommendation promotion.

The recommendation-inbox proof uses the existing project-owned inbox only in a
disposable synthetic fixture. No runtime command writes recommendations and no
live Poker/mood project is read or changed.

## 7. Attempt / Evaluation Structures

The public logical mappings are schema-versioned and immutable after
validation. Internal dataclass versus TypedDict representation is not
contractual; these fields and outcomes are.

### `AttemptRecordV1`

```text
schema_version: 1
attempt_id: <Change>/<task-or-operation>/A<positive ordinal>
change_id: non-empty canonical identity
task_or_operation_id: non-empty canonical identity
attempt_ordinal: positive integer
authorization_ref: stable external owner/gate reference
operation_guidance_ref: optional stable OperationGuidance evidence ref
candidate_identity: CandidateIdentityV1
baseline_refs: ordered non-empty IdentityRefV1[]
prompt_composition_ref: optional composition identity
parent_attempt_ref: optional earlier Attempt identity
addresses_finding_refs: ordered unique Finding identities
observed_result_ref: optional evidence identity
verifier_contract_refs: ordered unique contract identities
```

`attempt_id` is derived from Change, task/operation, and ordinal and must match
those fields. Every distinct governed execution occurrence increments the
ordinal. A distinct execution-authorization instance, materially changed
Attempt input, materially changed candidate/source, or corrective execution is
a new Attempt even under the same task or HEAD. A verifier-only rerun stays on
the same Attempt only when no governed work executes, candidate/source and
relevant inputs remain unchanged, and no new execution authorization is
consumed.

Attempt allocation consumes an explicitly supplied ledger-scoped lineage for the
same bounded Change plus task/operation. The supplied lineage must contain the
complete existing ordinal sequence `A1…An`, with one record per governed
execution, no duplicate ordinal, no gap, no reused ordinal, and matching Change
and task/operation identities. Malformed, non-contiguous, or mismatched lineage
fails closed. A new governed execution is allocated exactly `A(n+1)`; an empty
valid lineage allocates `A1`. The module does not scan the filesystem, infer an
ordinal from Git, or maintain a global allocator. A verifier-only rerun under
the frozen same-Attempt conditions never calls this allocation seam.

### `CandidateIdentityV1` and refs

```text
kind: GIT_COMMIT | DIRTY_SCOPE
head: exact Git SHA
dirty_manifest: ordered canonical DirtyPathEntryV1[]; empty for GIT_COMMIT
```

For `DIRTY_SCOPE`, each `DirtyPathEntryV1` contains `path`, `change_kind`, and
`content_identity`. `change_kind` is one of `ADD`, `MODIFY`, `DELETE`, `RENAME`,
or `TYPE_CHANGE`. `content_identity` is an explicit `{before, after}` pair;
each side is a lowercase SHA-256 identity or the literal marker `ABSENT`.
`RENAME` additionally carries the normalized `source_path` so source and
destination remain distinguishable. A type change preserves both bounded
content identities and its explicit `TYPE_CHANGE` kind. Entries are sorted by
normalized repo-relative destination path and then source path using the
existing repo-relative path convention; duplicate paths, invalid kinds, missing
markers, and non-canonical ordering fail closed. No timestamp, random value, or
filesystem snapshot is part of the manifest.

`IdentityRefV1` is `{ref, identity}` where `identity` is a revision/hash when
drift matters and may be null only when the owning authority defines a stable
immutable identity. It references source/authority; it never copies a body.

### `ObservedResultV1`

```text
schema_version: 1
result_id
attempt_id
execution_status: COMPLETED | FAILED | INTERRUPTED | INVALID
changed_paths: ordered unique repo-relative paths
fact_refs: ordered unique evidence refs
artifact_refs: ordered unique evidence refs
```

Execution status is descriptive. Exit zero, produced artifact, negative-test
success, verifier PASS, and technical acceptance remain distinct facts.

### Verifier and evaluation records

```text
VerifierContractV1:
  acceptance_contract_ref
  contract_id
  contract_version_or_ref
  required: boolean
  evidence_class: non-empty descriptive identity
  predicate
  required_evidence_refs[]
  failure_semantics

VerifierEvidenceV1:
  evidence_id
  attempt_id
  candidate_identity
  verifier_contract_id/version
  outcome: PASS | FAIL | INVALID | NOT_RUN
  evidence_refs[]
  applicability: EvidenceApplicabilityV1

TechnicalEvaluationV1:
  evaluation_id
  attempt_id
  candidate_identity
  acceptance_contract_ref
  declared_verifier_contract_refs[]
  required_verifier_contract_refs[]
  outcome: NOT_EVALUATED | NOT_SATISFIED | INDETERMINATE | SATISFIED
  evidence_complete: boolean
  required_evidence_refs[]
  applicable_finding_refs[]
  reason_codes[]
```

The evaluator input contains the complete approved acceptance-contract carrier:
`acceptance_contract_ref`, the full ordered declared verifier set, and its full
required subset. The Attempt's `verifier_contract_refs` must match that complete
declared set exactly; omission, duplication, or an undeclared contract is a
fail-closed contract error and cannot silently reduce the required set. Required
membership comes only from this approved carrier. The implementation does not
discover, register, or infer verifiers.

For each verifier contract, current evidence is selected only by exact
`verifier_contract_ref`, matching Attempt/candidate applicability, and an
explicit evidence-supersession relation. There is no "latest result wins"
rule. If more than one currently applicable result remains for one contract
without an explicit supersession relation, the result is conflicting and the
aggregate is `INDETERMINATE` unless an applicable admissible `FAIL` already
requires `NOT_SATISFIED`. An old `FAIL` and later `PASS` without supersession
therefore retain the old FAIL as applicable. A missing required contract result
is likewise `INDETERMINATE`; a missing/invalid acceptance-contract carrier is
`NOT_EVALUATED` because no candidate-quality evaluation can legally apply.

Evaluation applies this exact precedence:

1. `NOT_EVALUATED` when evaluation did not run or no candidate-quality
   evaluation can legally apply because Attempt/fixture is invalid;
2. `NOT_SATISFIED` when any applicable admissible required verifier is `FAIL`
   or an applicable unresolved blocking Finding exists, even if other evidence
   is incomplete;
3. `INDETERMINATE` when no decisive FAIL/blocker exists but required evidence
   is missing, invalid, incomparable, or ambiguously applicable; and
4. `SATISFIED` only when all required evidence applies and passes and no
   applicable unresolved blocker exists.

`evidence_complete` is calculated separately and cannot change authority.

## 8. Finding / Evidence Structures

### `FindingV1`

```text
finding_id
statement
severity: MATERIAL | NON_MATERIAL
responsibility_domains: ordered unique 1..N values from the bounded domain set
acceptance_impact: BLOCKING | NON_BLOCKING
disposition: OPEN | REMEDIATION_REQUIRED | DEFERRED | CLOSED
owner_adjudication_ref: null | external owner decision reference
evidence_refs: ordered unique non-empty refs
```

The bounded responsibility domain set begins exactly with:

```text
IMPLEMENTATION
VERIFICATION_TEST_COVERAGE
CONTRACT
AUTHORITY
FIXTURE_HARNESS
ENVIRONMENT
SCOPE_PROVENANCE
```

PromptOps-originated findings use these existing domains as applicable, together
with their finding statement, evidence references, Attempt/composition
provenance, and recommendation lineage. PromptOps origin is provenance, not a
new responsibility-domain value. Domains are multi-valued and do not imply
severity, impact, or disposition. Therefore:

```text
DEFINITION_ENUM_EXPANSION: NO
```

`OPEN` and `REMEDIATION_REQUIRED` are unresolved. `DEFERRED` is resolved for
current acceptance only with `NON_BLOCKING` impact and an owner adjudication
ref; historical truth remains. `CLOSED` requires an owner adjudication ref plus
closure evidence. Validation rejects owner-governed dispositions without their
provenance. Verifier PASS and evaluation SATISFIED may supply evidence but may
not set disposition.

### Applicability and supersession

```text
EvidenceApplicabilityV1:
  attempt_id
  candidate_identity
  verifier_contract_ref
  finding_refs[]
  evaluation_scope_ref

EvidenceSupersessionV1:
  prior_evidence_ref
  successor_evidence_ref
  current_acceptance_scope_ref
  rechecked_claim_refs[]
  reason
```

Evidence may aggregate only when Attempt, candidate/input, verifier contract,
and evaluation scope match their declared applicability. Candidate A evidence
cannot satisfy candidate B. Supersession changes current applicability only for
the stated rechecked claims; it never edits the prior record or directly closes
a Finding. Partial supersession is therefore representable.

## 9. Prompt Composition Provenance

`PromptCompositionRefV1` is derived evidence describing the ordered
prompt/context composition associated with an Attempt:

```text
schema_version: 1
composition_identity: sha256 of canonical full-composition payload
ordered_component_refs: PromptComponentRefV1[]
prompt_version_ref: optional identity reference
agent_adapter_ref: optional identity reference
stable_prefix_identity: sha256 of canonical stable-prefix payload
```

Each component contains:

```text
component_ref
component_identity_or_hash
component_role
residency_class
canonical_order: zero-based integer
```

The input array must already have unique contiguous `canonical_order` values
`0..N-1` in array order. The implementation neither discovers components nor
reorders context. Duplicate/gapped/out-of-order values fail validation.

`composition_identity` hashes exactly the canonical JSON object containing
`schema_version`, `ordered_component_refs`, `prompt_version_ref`, and
`agent_adapter_ref`; optional refs are always present with JSON `null` when
absent. The stored `composition_identity` and `stable_prefix_identity` fields
are excluded from that input to avoid self-reference. Component records contain
exactly their declared keys; no extra or omitted field is implementation-defined.
The composition ref is an Attempt-associated evidence reference and never
allocates Attempt identity, owns acceptance or Finding disposition, compiles
context, invokes a provider, or stores copied prompt bodies.

```text
PromptCompositionRef != authority
PromptCompositionRef != prompt source of truth
PromptCompositionRef != Context Compiler
PromptCompositionRef != provider request
composition_identity != attempt_identity
```

## 10. Context Residency

`ContextResidencyClass` is the exact metadata vocabulary:

```text
FRAMEWORK_STATIC
ENVIRONMENT_STABLE
CHANGE_STABLE
RUN_DYNAMIC
ON_DEMAND
```

It describes volatility/reuse only. It is not a storage, authority, permission,
or provider-cache class.

These reserved component roles must validate as `RUN_DYNAMIC`:

```text
OWNER_AUTHORIZATION
IMPLEMENTATION_AUTHORIZATION
GIT_MUTATION_AUTHORIZATION
NEXT_PERMITTED_ACTION
BLOCKER
TASK_RESULT
GIT_HEAD
GIT_STATUS
RUNTIME_EVIDENCE
```

They can participate in full composition identity but never Stable Prefix
identity. `ON_DEMAND` components participate only when actually present and are
always outside the stable prefix. Absence is not represented by a fabricated
component.

`AGENT_ADAPTER` may be an `ENVIRONMENT_STABLE` component. It is optional
adapter metadata, not Planning Lite authority; changing/removing it may change
composition identities but cannot change governance results or authority refs.
Agents/providers that do not use `AGENTS.md` remain supported.

## 11. Stable Prefix Identity

The Stable Prefix is the longest leading contiguous component sequence whose
residency is one of:

```text
FRAMEWORK_STATIC
ENVIRONMENT_STABLE
CHANGE_STABLE
```

The first `RUN_DYNAMIC` or `ON_DEMAND` component ends the prefix. Later stable
components do not re-enter it. This preserves actual prefix semantics and makes
dynamic-before-stable placement observable.

Canonical serialization is UTF-8 JSON with sorted object keys, compact
separators, and array order preserved. The exact byte contract is UTF-8 with
Unicode characters emitted directly (`ensure_ascii=false` equivalent), no BOM,
no trailing newline, lexicographically sorted object keys, and no whitespace
outside structural separators. Optional fields are represented by explicit
`null`, never by omission; arrays preserve their validated order. Identifiers/
refs must be non-empty, contain no leading/trailing whitespace or CR/LF, and are
otherwise preserved exactly—no case folding or Unicode/fuzzy normalization.
Hashes are lowercase SHA-256 over those exact bytes. There are no timestamps,
random IDs, runtime metrics, or provider data in either identity input.

`stable_prefix_identity` hashes exactly the canonical JSON object
`{"components": [...], "schema_version": 1}` where `components` contains the
validated leading component records and no other field. Top-level
prompt/adapter refs affect the full composition; they affect the Stable Prefix
only when represented by a component inside that leading stable sequence.

The empty prefix has the deterministic hash of the canonical empty-prefix
payload. Non-canonical component order is rejected; the implementation never
silently reorders components. Changing only owner authorization, implementation
authorization, Git mutation authorization, next permitted action, blocker,
HEAD, Git status, task result, or runtime evidence changes the full composition
as applicable but leaves the Stable Prefix identity unchanged.

```text
StablePrefixIdentity != provider cache key
StablePrefixIdentity != cache hit/miss
StablePrefixIdentity != cached_tokens
StablePrefixIdentity != authority
```

## 12. Cache-Ready / Cache-Enabled Boundary

PL-V39-08 may derive only cache-readiness facts:

```text
stable_prefix_reused
component_order_stable
stable_component_changed
dynamic_component_before_stable_boundary
unexpected_component_churn
prompt_version_changed
composition_changed_between_attempts
```

It must not emit `cached_tokens`, cache hit/miss/write, latency saving, cost
saving, or provider-cache effectiveness unless such values arrive as external
runtime evidence; even then they remain opaque evidence and do not affect the
Stable Prefix algorithm.

No `cache.py`, `prompt_cache.py`, `provider_cache.py`, provider adapter, cache
key, cache breakpoint, provider invocation, or cache integration is permitted.

```text
PL-V39-08: CACHE-READY
PL-V39-08: NOT CACHE-ENABLED
```

## 13. Task Graph

```text
Plan owner review/approval
→ Planning authority checkpoint
→ read-only Formal Readiness
→ separate owner Execution authorization
→ T-01 → T-02 → T-03 → T-04 → T-05 → T-06
→ CENTRAL_08_B_CANDIDATE_REVIEW_GATE
→ separate owner continuation authorization
→ T-07 → T-08 → T-09 → T-10 → T-11
→ CENTRAL_PL_V39_08_IMPLEMENTATION_CANDIDATE_REVIEW
→ separate owner checkpoint-commit authorization
→ clean committed candidate
→ conditional separately authorized disposable field proof, if readiness/review requires it
→ Completion Review
→ separate owner closure
```

T-04 may begin after T-02 and proceed alongside T-03 only if one executor keeps
the shared module edits serialized; otherwise the listed linear order applies.
No intermediate 08-B commit is required.

## 14. Task Details

### T-01 — Attempt and provenance foundation

- Outcome: add the one cohesive pure module with exact Attempt identity,
  CandidateIdentity, IdentityRef, ObservedResult, canonical validation, and the
  nullable PromptComposition hook.
- Dependencies: approved Plan, planning checkpoint, Formal Readiness READY, and
  separate owner Execution authorization.
- Writes: new module, 08-B focused test, progress template, SHA receipts,
  cumulative ledger.
- Proof: repeated task/new authorization, same SHA/different input, correction,
  same-Attempt verifier reruns, dirty/clean candidates, Attempt non-authority.
- Stop: filesystem/registry/lifecycle ownership or a changed Definition is
  required.

### T-02 — Verifier contracts and evidence

- Outcome: implement contract-only required/advisory declarations and evidence
  applicability; bind required membership exclusively from the supplied
  acceptance contract.
- Dependencies: T-01 PASS.
- Writes: module, 08-B test, progress template if contract wording needs its
  already-planned block, SHA receipts, ledger.
- Proof: multiple evidence classes, one PASS insufficient, missing/invalid
  evidence, no registry/runner/discovery, owner gate never verifier.
- Stop: inferred verifier membership or plugin/runner architecture is needed.

### T-03 — Technical evaluation precedence

- Outcome: implement the four-state aggregate and separate completeness value.
- Dependencies: T-02 PASS.
- Writes: module, 08-B test, ledger.
- Proof: `FAIL + missing → NOT_SATISFIED`; no FAIL + missing →
  `INDETERMINATE`; invalid Attempt/fixture → `NOT_EVALUATED`; all required PASS
  and no blocker → `SATISFIED`; tests PASS plus required review FAIL remains
  `NOT_SATISFIED`.
- Stop: outcome overlap or authority elevation remains.

### T-04 — Finding and disposition boundary

- Outcome: implement four independent axes, multi-valued domains, separate
  owner provenance, unresolved rules, and closure validation; align progress
  and review templates.
- Dependencies: T-02 PASS.
- Writes: module, 08-B test, progress/review templates, SHA receipts, ledger.
- Proof: all four orthogonal cases are explicit: MATERIAL+NON_BLOCKING may
  coexist with technical acceptance; NON_MATERIAL+BLOCKING blocks; MATERIAL+
  BLOCKING blocks; NON_MATERIAL+NON_BLOCKING does not block. Deferred N-01-shaped
  debt remains reportable alongside acceptance; PASS cannot close; owner
  provenance is required for DEFERRED/CLOSED/REMEDIATION_REQUIRED.
- Stop: verifier/evaluator can set owner disposition or axes determine one
  another.

### T-05 — Applicability, supersession, and re-attempt lineage

- Outcome: implement exact applicability and partial supersession relations,
  immutable prior evidence, and corrective parent/finding links.
- Dependencies: T-01…T-04 PASS.
- Writes: module, 08-B test, ledger.
- Proof: candidate A evidence rejected for B; partial claim supersession;
  historical FAIL preserved; successor PASS supplies evidence but not closure;
  failed evaluation cannot authorize retry.
- Stop: event store, history rewrite, or automatic retry is required.

### T-06 — 08-B integration and central verification

- Outcome: integrate T-01…T-05, verify template semantics/integrity, and prepare
  a reviewable 08-B candidate without starting 08-C.
- Dependencies: T-01…T-05 PASS.
- Writes: focused test/template refinements already listed, SHA receipts,
  cumulative ledger only.
- Proof: 08-B focused suite, relevant existing Operation Guidance/RunReceipt/
  context regressions, all four Finding severity/acceptance-impact cases,
  complete required-verifier-set and multiple-evidence resolution, template
  integrity, scope audit, `git diff --check`.
- Stop: any applicable unresolved BLOCKING finding, invalid required evidence,
  unexpected path, or 08-C dependency.

### CENTRAL_08_B_CANDIDATE_REVIEW_GATE

An independent bounded review must verify AC-01…AC-08 foundation semantics,
the PL-V39-07 green-tests/failed-review discriminator, applicable unresolved
BLOCKING findings, and no authority or Campaign/lifecycle leakage. Its result
is exactly `PASS`, `FAIL`, or `BLOCKED`; a PASS only means the 08-B review gate
is clear and never authorizes continuation. Stop for the separate owner gate:
`OWNER_AUTHORIZATION_CONTINUE_PL_V39_08_08_C`. No commit is required or
implied.

### T-07 — Prompt Composition and Stable Prefix

- Outcome: implement component/composition schemas, residency validation,
  canonical full identity, and longest-leading-stable-prefix identity.
- Dependencies: 08-B review PASS and separate owner continuation authorization.
- Writes: module, 08-C test, progress template, SHA receipts, ledger.
- Proof: same stable components/different dynamic tail gives same prefix;
  changed stable component changes it; owner auth or HEAD/status-only changes do
  not; implementation auth, Git mutation auth, next action, blocker, task
  result, and runtime evidence are each parameterized with the same exclusion;
  reorder is rejected as non-canonical; optional agent adapter cannot change
  governance authority. Null optional fields and Unicode component refs use the
  exact frozen canonical bytes.
- Stop: context assembly, provider behavior, or Attempt identity redefinition.

### T-08 — Composition comparison and PromptOps evidence

- Outcome: implement a pure comparison result containing exact added, removed,
  moved, identity-changed, residency-changed, prompt-version, adapter, stable-
  prefix, and dynamic-tail facts; derive PromptOps findings through the common
  Finding model.
- Dependencies: T-07 PASS.
- Writes: module, 08-C test, ledger.
- Proof: Attempt A/B comparisons for same/different prefix, changed version,
  add/remove/reorder, residency drift, unexpected churn, and no “better” or
  cache-effectiveness claim. PromptOps findings retain existing responsibility
  domains plus composition/evidence provenance; no new PromptOps domain is
  introduced.
- Stop: scoring, provider integration, or a separate PromptOps finding system.

### T-09 — Controlled recommendation evidence

- Outcome: derive the bounded `RecommendationEvidenceV1` contract below, or an
  explicit no-op, from supplied evaluated findings and comparison facts; extend
  the existing recommendation template.
- Dependencies: T-08 PASS.
- Writes: module, 08-C test, recommendation template, SHA receipts, ledger.
- Proof: eligible and non-eligible inputs produce the exact recommendation/no-op
  outcomes; recommendations remain non-authoritative; no automatic prompt,
  AGENTS, policy, workflow, verifier, or product mutation; promotion requires
  external owner authority.
- Stop: generic recommendation engine/backlog or automatic action is required.

`RecommendationEvidenceV1` is the smallest derived recommendation contract:

```text
schema_version: 1
outcome: NO_RECOMMENDATION | RECOMMENDATION
reason_code: non-empty deterministic code
recommendation_kind: null | STABLE_CARRIER_REUSE
statement: null | bounded non-authoritative statement
evidence_refs: ordered unique refs
finding_refs: ordered unique refs
target_ref: null | bounded carrier/reference identity
non_authoritative: true
owner_adjudication_ref: null | external owner decision reference
```

The input is the exact current-applicable evaluated evidence/findings plus
bounded `PromptCompositionComparisonV1` facts. A recommendation is eligible
only when an applicable comparison contains `unexpected_component_churn` or
`dynamic_component_before_stable_boundary` and the corresponding Finding and
evidence references are admissible. That finite pattern yields
`recommendation_kind=STABLE_CARRIER_REUSE`; all other inputs yield
`NO_RECOMMENDATION`. The output is deterministic, carries no authority, and
cannot authorize retry, mutate a prompt/policy, create implementation
authorization, or promote itself. No recommendation registry or engine is
introduced.

### T-10 — Recommendation-inbox disposable behavioral proof

- Outcome: in a synthetic disposable fixture, prove eligible
  Attempt/composition churn evidence → existing-domain Finding with PromptOps
  provenance → non-authoritative recommendation, and non-eligible evidence →
  `NO_RECOMMENDATION`, followed by explicit owner adjudication with no automatic
  mutation.
- Dependencies: T-07…T-09 PASS.
- Writes: disposable temp fixture and cumulative ledger; no live consumer.
- Proof: byte/status baseline, exact provenance, pending recommendation before
  supplied owner decision, no source/prompt/AGENTS mutation, cleanup evidence.
- Stop: live Poker/mood, persistent authority, or runtime recommendation writer.

### T-11 — 08-C integration / full PL-V39-08 candidate verification

- Outcome: reconcile both phases, all ten ACs, template integrity, and exact
  write scope into one independently reviewable implementation candidate.
- Dependencies: T-01…T-10 PASS.
- Writes: only planned product/test/template paths plus cumulative ledger.
- Proof: focused suites, relevant regressions, `uv sync`, full pytest, template
  integrity, clean temporary adoption + Doctor, scope/diff audit, independent
  adversarial review. No central-root Doctor.
- Stop: any AC lacks evidence, any applicable unresolved BLOCKING finding
  remains, or candidate/source identity drifts.

## 15. AC-to-Task Matrix

Each AC has exactly one primary task owner. Secondary tasks provide integration
or refinement evidence; every task appears at least once.

| AC | Definition requirement | Implementation seam | Primary task | Secondary tasks | Verification class | Field proof |
|---|---|---|---|---|---|---|
| AC-01 | deterministic minimal Attempt identity/lineage | AttemptRecord constructor/discriminator; composition ref remains input provenance | T-01 | T-05, T-07, T-06 | unit/contract + integration | no |
| AC-02 | authorization provenance and non-elevation | external authorization ref; validation never grants authority | T-01 | T-03, T-04, T-06 | negative contract + independent review | no |
| AC-03 | contract-only verifier multiplicity | supplied required/advisory VerifierContract set | T-02 | T-03, T-06 | unit truth matrix + review | no |
| AC-04 | observation/verification/evaluation separation | ObservedResult plus exact aggregate precedence/completeness | T-03 | T-02, T-06 | unit truth table + PL-V39-07 discriminator | no |
| AC-05 | orthogonal Finding semantics | Finding validation, multi-domain axes, separate owner ref | T-04 | T-06, T-08 | unit/contract + independent review | no |
| AC-06 | applicability/supersession/history | applicability validator and partial supersession relation | T-05 | T-08, T-10, T-11 | unit/integration + review | synthetic T-10 |
| AC-07 | partial baseline/provenance | dirty/committed CandidateIdentity and Attempt input refs; PromptComposition identity without body copies | T-01 | T-05, T-07, T-11 | unit/integration + disposable topology where needed | conditional synthetic |
| AC-08 | re-attempt lineage and residual debt | parent/addressed findings plus deferred N-01 semantics | T-05 | T-04, T-06, T-11 | lineage integration + review | no |
| AC-09 | non-authoritative learning/PromptOps | comparison findings and recommendation/no-op evidence | T-09 | T-07, T-08, T-10, T-11 | contract/integration + disposable behavior | T-10 |
| AC-10 | reuse/no forbidden systems/07-08-09 boundary | one pure module, managed templates, structural scope guards | T-11 | T-06, T-07, T-10 | scope audit + independent review + adoption/Doctor | conditional only |

```text
AC_PLAN_COVERAGE: 10/10
ORPHAN_AC: 0
ORPHAN_TASK: 0
```

Prompt Composition adds no AC-11. Its primary acceptance belongs to AC-09,
with baseline/provenance support under AC-01, AC-06, AC-07, and AC-10. AC-07's
primary owner is T-01 because committed/dirty CandidateIdentity and Attempt
input provenance originate there; T-07 is a secondary composition-provenance
seam.

## 16. Verification Matrix

| Evidence class | Scope | Required gate |
|---|---|---|
| unit/contract | exact records, validation, Attempt discriminator, evaluation precedence, Finding rules, canonical identities/comparison | each owning task |
| integration | OperationGuidance refs → Attempt; Attempt/evidence/evaluation chain; template blocks; recommendation/no-op chain | T-06 and T-11 |
| independent adversarial review | authority leaks, mixed verifier outcomes, partial supersession, dynamic-prefix exclusions, 07/08/09 drift | Gate A and central candidate review |
| disposable behavioral proof | synthetic recommendation inbox and, only if needed, consumer-shaped topology evidence | T-10 and separately authorized conditional post-commit gate |

The focused discriminators additionally require: malformed/non-contiguous or
reused Attempt lineage fails closed; DELETE/RENAME/TYPE_CHANGE dirty inputs have
deterministic manifests; an omitted required verifier cannot be silently
accepted; old FAIL plus new PASS without supersession remains FAIL; all four
severity/acceptance-impact combinations are exercised; null optional fields and
Unicode component refs hash deterministically; every reserved RUN_DYNAMIC role
is excluded; eligible and ineligible recommendation inputs produce
`RECOMMENDATION` and `NO_RECOMMENDATION`; and the AC-07 primary owner is T-01.

Focused commands are planned as:

```text
uv run --frozen pytest tests/test_attempt_evaluation.py -rA
uv run --frozen pytest tests/test_prompt_composition.py -rA
uv run --frozen pytest tests/test_execution_guidance.py tests/test_run_receipts.py -rA
uv run --frozen pytest tests/test_context_resume.py tests/test_central_resume_contract.py -rA
uv run --frozen pytest tests/test_template.py -rA
```

T-11 then runs:

```text
uv sync
uv run --frozen pytest
git diff --check
git status --short --untracked-files=all
```

It adopts the candidate template into a temporary clean Git repository and runs
`planning-lite doctor` there. It never runs Doctor at the central repository
root. A two-tag update migration is not required unless actual implementation
drifts into update/ownership behavior, which is a stop condition rather than
implicit scope.

Mandatory 08-B discriminators include all cases in Definition §§7–14,
especially automated PASS plus required review FAIL. Mandatory 08-C cases
include the owner-authorization X/Y same-prefix discriminator and agent-adapter
non-authority discriminator. Green automated tests alone never satisfy either
candidate review gate.

## 17. Planned Write Surface

Nine later implementation/evidence paths are proposed. The Plan and CURRENT
written by this planning step are not implementation paths.

| Path | Class | Phase | Responsibility |
|---|---|---|---|
| `src/planning_lite/attempt_evaluation.py` | `NEW_MINIMAL` | 08-B + 08-C | one pure cohesive contract, validators, evaluation, composition identity/comparison, recommendation evidence |
| `tests/test_attempt_evaluation.py` | `TEST` | 08-B | focused Attempt/verifier/evaluation/Finding/lineage cases |
| `tests/test_prompt_composition.py` | `TEST` | 08-C | residency, identity, comparison, adapter, recommendation and no-cache cases |
| `template/.planning/changes/templates/progress.md` | `TEMPLATE / EXISTING_MODIFY` | 08-B + 08-C | compact cumulative Attempt/evidence/composition record fields |
| `template/.planning/changes/templates/review.md` | `TEMPLATE / EXISTING_MODIFY` | 08-B | technical evaluation, residual findings, supersession, and owner-closure separation |
| `template/.planning/recommendations/TEMPLATE.md` | `TEMPLATE / EXISTING_MODIFY` | 08-C | source Attempt/Finding/composition refs and non-authoritative owner gate |
| `template/.planning/framework/SHA256SUMS.txt` | `TEMPLATE / EXISTING_MODIFY` | both | regenerate canonical-LF hashes for changed managed templates |
| `docs/design/project-spine/checkpoints/PL-V39-08-EXECUTION-LEDGER-v1.md` | `GOVERNANCE_EVIDENCE` | both | one cumulative T-01…T-11 execution/review/proof record |
| `docs/design/project-spine/checkpoints/PL-V39-08-COMPLETION-REVIEW-v1.md` | `GOVERNANCE_EVIDENCE` | final | final technical reconciliation; not owner closure |

`NEW_MINIMAL` justification: the single new module owns a general governed
Attempt evaluation seam absent from current product code. Extending Operation
Guidance would mix pre-execution routing with post-execution evaluation;
extending RunReceipt would break a strict external telemetry schema; extending
Campaign would generalize a stateful Campaign lifecycle forbidden by the
Definition. Two new test files are phase-focused test surfaces, not product
subsystems.

No new template path is added, so `MANIFEST_V4.md` and `OWNERSHIP.yml` should
remain byte-unchanged; their existing managed coverage is verified. `copier.yml`,
`cli.py`, `context.py`, `execution_guidance.py`, `telemetry.py`, all Campaign
code, AGENTS adapters, live projects, docs/Roadmap, and release files are outside
the write surface.

Any required unlisted path stops the task for amendment/adjudication.

## 18. Candidate Review Gates

### Gate A — `CENTRAL_08_B_CANDIDATE_REVIEW_GATE`

Requires T-01…T-06 PASS, exact Definition semantics, focused/resume/template
regressions PASS, no applicable unresolved BLOCKING finding, no authority
leakage, and independent review PASS. Non-blocking findings remain visible in
the review record and do not become blocking solely because their severity is
MATERIAL. It authorizes nothing. Owner continuation is separately required
before T-07.

### Gate B — `CENTRAL_PL_V39_08_IMPLEMENTATION_CANDIDATE_REVIEW`

Requires T-01…T-11 PASS, AC 10/10 evidence, full regression and temporary
adoption/Doctor PASS, exact scope, template integrity, no provider/cache/context
compiler behavior, no applicable unresolved BLOCKING finding, and independent
review. Non-blocking debt remains reportable and historically preserved.

After Gate B, a separate owner authorization is required for the checkpoint
commit. Only that commit creates a clean candidate for any separately required
source-identity-dependent field proof. Neither gate performs staging or commit.

## 19. Disposable Proof Strategy

T-10 uses a reduced synthetic fixture rather than live consumers. It constructs
two Attempts whose compositions differ by unnecessary stable-prefix churn,
derives an existing-domain Finding with PromptOps provenance and a
`STABLE_CARRIER_REUSE` recommendation, then proves:

```text
recommendation before supplied owner decision: NON_AUTHORITATIVE / PENDING
source prompt/policy/AGENTS mutation: NONE
retry/execution: NONE
owner adjudication: external explicit input only
```

The fixture records before/after paths and hashes and is removed after evidence
capture. `D:\documents\poker` and `D:\documents\mood` have no read or write
surface.

A post-commit consumer-shaped disposable proof is conditional, not automatic.
Formal Readiness or candidate review must identify a genuine topology seam, and
the owner must separately authorize it. Existing PL-V39-05-C topology evidence
is reused where the pure module and managed-template update add no new topology
behavior.

## 20. Evidence Economy

Implementation evidence uses exactly:

```text
one cumulative PL-V39-08-EXECUTION-LEDGER-v1.md
+ one final PL-V39-08-COMPLETION-REVIEW-v1.md
```

The ledger records task ID, execution baseline/Attempt, actual changed paths,
verification commands/results, PASS/FAIL/BLOCKED, findings, candidate review,
and proof outcomes. Separate diagnostics are created only when independently
valuable and separately authorized. There are no per-task receipts.

Disposable fixture data remains temporary; the ledger retains only bounded
facts/hashes/refs required to interpret the result. Completion Review reconciles
ACs, open/deferred Findings, Definition/Plan drift, exact candidate SHA, and
technical acceptance. It is not owner closure.

## 21. Authority / Git Gates

```text
Plan PREPARED != Plan APPROVED
Plan APPROVED != Formal Readiness READY
Formal Readiness READY != implementation authorization
PRODUCT_WRITE != GIT_STAGE != GIT_COMMIT
technical acceptance != owner disposition
finding/recommendation != retry authorization
```

Required lifecycle:

```text
owner Plan review/approval
→ separately authorized planning authority checkpoint
→ read-only Formal Readiness
→ separate owner 08-B Execution authorization
→ Gate A review
→ separate owner 08-C continuation authorization
→ Gate B review
→ separate owner checkpoint-commit authorization
→ conditional separate disposable-proof authorization, if required
→ Completion Review authorization
→ owner closure
```

No authority is inferred from this Plan, test PASS, technical evaluation,
Finding disposition, Prompt Composition identity, or recommendation.

## 22. 07/08/09 Boundary

```text
PL-V39-07:
selects the operation and exposes route/capability/authority/evidence refs.

PL-V39-08:
observes and identifies Attempt/composition provenance, verifies/evaluates,
records Findings and applicability/supersession, and derives non-authoritative
learning/PromptOps recommendations.

PL-V39-09:
assembles, orders, renders, or emits production context/AgentWorkPackets;
owns Context Compiler, agent adapters as rendered output, orchestration,
automatic workflow chaining, and release automation.

Provider adapter:
may later consume compiled stable-prefix identity/residency and implement cache
behavior under separate scope.
```

PL-V39-08 does not implement `planning-lite context`, `pl context assemble`,
`PL_AGENT_CONTEXT.md`, AGENTS generation, context injection, tool ordering,
provider invocation, cache keys/breakpoints, or provider metrics.

```text
08 OBSERVES / IDENTIFIES / EVALUATES COMPOSITION
09 ASSEMBLES / ORDERS / EMITS COMPOSITION
PROVIDER ADAPTER MAY CACHE IT
07_08_09_BOUNDARY: CLOSED
```

## 23. Stop Conditions

Stop the affected task and seek amendment/adjudication if:

- Definition authority SHA, Plan authority, active lifecycle, or authorized
  write surface materially drifts;
- an exact Attempt discriminator or evaluation precedence cannot be preserved;
- verifier evidence or technical acceptance would grant authority;
- Finding disposition can be changed without owner provenance;
- historical evidence must be rewritten or candidate-mismatched evidence
  aggregated;
- a registry, database, lifecycle engine, event store, plugin/generic runner,
  new CLI/skill, provider/cache module, or extra product subsystem is needed;
- Prompt Composition would assemble/render/inject context or control an agent;
- dynamic authority, live Git state, task result, runtime evidence, or ON_DEMAND
  content enters Stable Prefix identity;
- unavailable cache/provider metrics would be inferred;
- an unlisted path, live Poker/mood access, PL-V39-09 behavior, or automatic
  recommendation/prompt/policy mutation becomes necessary;
- focused/full tests, template integrity, adoption/Doctor, scope audit, or
  independent review fails; or
- 08-C cannot proceed without changing the accepted 08-B contract.

No stop condition authorizes repair, retry, staging, commit, or scope expansion.

## 24. Plan Self-Check

Nearest-wrong pairs were resolved as follows:

| Axis | Rejected implementation | Bound implementation |
|---|---|---|
| Attempt authority | Attempt record grants permission | record references external authority only |
| repeat execution | same task collapses all runs | every governed occurrence gets next ordinal |
| verifier rerun | every check creates an Attempt | unchanged verifier-only rerun stays on Attempt |
| mixed evidence | FAIL + missing becomes ambiguous | Definition precedence yields NOT_SATISFIED |
| invalid fixture | also INDETERMINATE | NOT_EVALUATED exclusively when no legal candidate-quality evaluation applies |
| Finding axes | materiality determines blocking | severity and impact validate independently |
| disposition | verifier PASS closes Finding | only owner-referenced disposition closes/defers/remediates |
| supersession | successor rewrites prior FAIL | scoped applicability changes; prior evidence immutable |
| composition identity | unordered set/hash | validated observed order and canonical serialization |
| residency | storage/permission class | volatility metadata only; reserved authority roles RUN_DYNAMIC |
| Stable Prefix | arbitrary stable subset or provider key | longest leading stable run; evidence-only SHA-256 |
| owner authorization | stable/cached component | mandatory RUN_DYNAMIC; excluded from Stable Prefix |
| phase boundary | evaluator compiles provider context | 08 observes; 09 assembles; provider may cache later |

```text
DEFINITION_DRIFT: NO
DEFINITION_ENUM_EXPANSION: NO
AC_COUNT: 10
ORPHAN_AC: 0
ORPHAN_TASK: 0
ATTEMPT_IDENTITY_PLAN: CLOSED
EVALUATION_PRECEDENCE_PLAN: CLOSED
FINDING_MODEL_PLAN: CLOSED
EVIDENCE_LINEAGE_PLAN: CLOSED
STABLE_PREFIX_DETERMINISM: CLOSED
PROMPT_COMPOSITION_REF: CLOSED
RECOMMENDATION_CONTRACT: CLOSED
PROMPT_COMPOSITION_REQUIRES_DEFINITION_AMENDMENT: NO
CONTEXT_COMPILER_IMPLEMENTED_IN_08: NO
PROVIDER_CACHE_IMPLEMENTED: NO
CACHE_EFFECTIVENESS_CLAIM: NO
OWNER_AUTHORIZATION_IN_STABLE_PREFIX: NO
NEW_PERSISTENT_AUTHORITY: NO
NEW_REGISTRY: NO
NEW_DATABASE: NO
NEW_LIFECYCLE_ENGINE: NO
NEW_SKILL: NO
NEW_CLI_SURFACE: NO
07_08_09_BOUNDARY: CLOSED
IMPLEMENTATION_PLAN_UNDERDETERMINED: NO
FORMAL_READINESS_INPUT_QUALITY: READY_FOR_OWNER_APPROVAL
```

## 25. Exact Next Owner Gate

```text
RUN_PL_V39_08_FORMAL_READINESS
```

The owner-approved Plan permits the separate read-only Formal Readiness gate.
Formal Readiness does not authorize implementation, create the Execution
Ledger, stage/commit, start a disposable proof, or begin PL-V39-09.
