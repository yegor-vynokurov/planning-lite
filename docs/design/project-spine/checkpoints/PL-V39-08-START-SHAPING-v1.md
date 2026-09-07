# PL-V39-08 Start Shaping v1

## 1. Starting State

```text
decision: OWNER_DECISION_START_PL_V39_08
mode: BOUNDED SHAPING / PROBLEM DEFINITION ONLY
baseline HEAD: f2176dcafa5df0e086eb3235444c30f7b11d8bb6
baseline worktree: CLEAN
PL-V39-07: CLOSED / COMPLETE
PL-V39-08: SHAPING STARTED / NOT YET DEFINED
implementation_authorized: NO
```

PL-V39-07 closed with:

```text
implementation candidate: 3d861f18997f68ea7ea8a2e97cc2208c40e96fe8
closure commit: f2176dcafa5df0e086eb3235444c30f7b11d8bb6
T-01…T-09: PASS
AC: 9/9 PASS
open material findings: NONE
```

Its evidence lineage remains intentionally non-flat:

```text
initial candidate review FAIL — M-01 + M-02
→ first correction PASS
→ first re-review FAIL — RR-M01-01
→ second correction PASS
→ second re-review PASS
→ disposable field proofs PASS
→ Completion Review PASS
→ owner closure
```

The canonical macro-sequence is unchanged:

```text
PL-V39-05-C Consumer Control Topology
→ PL-V39-06 Context / Memory / Handoff
→ PL-V39-07 Deterministic Operation Guidance
→ PL-V39-08 Evaluation / Learning / PromptOps
→ PL-V39-09 Compilation / Orchestration / Release
```

This shaping used the closed PL-V39-07 Completion Review and Execution Ledger,
the canonical PL-V39-08 Roadmap sections, and only targeted support evidence
already routed to attempt lifecycle, verifier baseline, evaluation, learning,
PromptOps, and recommendation intake. It did not reopen repository-wide
architecture discovery.

## 2. Empirical Trigger from PL-V39-07

PL-V39-07 supplied a concrete discriminator that ordinary test success cannot
represent alone:

```text
306 green tests
→ independent review FAIL (M-01 + M-02)

313 green tests
→ independent re-review FAIL (RR-M01-01)

324 green tests
→ adversarial re-review PASS

disposable T-07/T-08 field proofs
→ PASS on the same committed candidate
```

Nothing in this history is contradictory. Each result answers a different
question. The test suite established the predicates it contained; independent
review tested contract completeness and adversarial boundaries; field proofs
tested observable behavior in disposable consumer-shaped environments; owner
acceptance considered all required evidence and preserved N-01 as debt.

The architectural gap is the absence of a small common representation that can
bind those facts to one execution/correction lineage and explain why one PASS
is necessary yet insufficient for acceptance.

## 3. Problem Statement

```text
PL-V39-08 primary problem:
Planning Lite cannot yet reconcile an owner-authorized attempt, its observed
result, heterogeneous verifier evidence, technical evaluation, findings, and
owner-governed disposition as one bounded lineage without conflating evidence
with authority.

Primary capability:
GOVERNED_ATTEMPT_EVALUATION
```

```text
PRIMARY_PROBLEM: TECHNICAL_EVALUATION_SEPARATED_FROM_OWNER_DISPOSITION
```

The capability answers:

```text
Given an already selected and separately authorized operation,
what happened, what evidence was produced, which required checks ran,
which expectations were or were not satisfied, what findings remain,
and what owner decision is permitted next?
```

It does not select the operation, grant execution authority, execute the task,
authorize remediation, or start another attempt.

## 4. Vocabulary

Authority labels in this table mean:

- `EXISTING AUTHORITY REF`: the term points to already approved Definition,
  Plan, owner decision, or Operation Guidance; PL-V39-08 does not create a new
  authority source.
- `EVIDENCE`: a recorded fact or result that informs a later gate.
- `DERIVED`: reproducible interpretation of frozen inputs and evidence.
- `NON-AUTHORITATIVE`: may support a recommendation but cannot authorize work.

| Term | Definition | Owner | Authority status | Persistent or derived | Exists conceptually | PL-V39-08 decision |
|---|---|---|---|---|---|---|
| Attempt | One bounded occurrence of executing an already selected and separately authorized task/operation. Authorization without execution is not an attempt. | Executor records it; owner authorizes it. | `EVIDENCE`; authority remains the referenced owner decision and 07 boundary. | Persist a compact ledger record when materially evaluated. | Yes, implicit in task/corrective history. | Introduce the minimum explicit record semantics. |
| Attempt identity | Stable local identity: Change ID + task/operation ID + attempt ordinal, bound to authorization and input baseline. It is not a random global ID. | Existing lifecycle/ledger. | `EVIDENCE` identity only. | Persist. | Partly, through task IDs and headings. | Add a deterministic ledger-scoped form such as `T-06/A2`. |
| Attempt input | Candidate identity/fingerprint, authority and contract refs, bounded parameters, topology, and declared verifier set used for that attempt. | Task contract plus executor. | Governed by `EXISTING AUTHORITY REF`; not new authority. | Persist refs/digests needed for reproduction; derive copied facts when possible. | Scattered across Plan, ledger, Git, and proof fixtures. | Bind, do not duplicate bodies. |
| Attempt boundary | The authorized write surface, capability envelope, environmental constraints, and stop gates within which the attempt may act. | Owner decision + PL-V39-07 Operation Guidance/Plan. | `EXISTING AUTHORITY REF`. | Persist references and deviations, not a second policy copy. | Yes. | Reuse unchanged. |
| Observed result | What actually occurred: process outcome, changed paths, outputs, hashes, errors, and other directly measured facts. | Executor/evidence recorder. | `EVIDENCE`. | Persist bounded facts or artifact refs. | Yes, in ledgers and receipts. | Normalize only enough for evaluation. |
| Expected result | The result/evidence contract and acceptance predicates frozen before evaluation. It is not inferred from the observed result. | Definition/Plan/task/Operation Guidance. | `EXISTING AUTHORITY REF`. | Persist stable refs/digests; authority body remains at source. | Yes. | Reuse and bind explicitly. |
| Verification | Applying a declared check to attempt evidence to answer one bounded predicate. | The declared verifier procedure. | Produces `EVIDENCE`; grants no authority. | Run result persists when required; computation may be derived. | Yes. | Clarify as distinct from execution and acceptance. |
| Verifier | A named/versioned bounded predicate or review procedure with defined inputs, evidence output, and failure semantics. It is not a generic plugin. | Plan/task contract binds it; its implementation owns the check. | Subordinate contract under existing authority. | Persist identity/version/ref; logic remains in its owning surface. | Yes: tests, diff checks, review, field proof. | Use a contract-only model, no registry. |
| Verification evidence | Direct output and provenance from a verifier: command/result, review finding, fixture observation, hashes, or artifact reference. | Verifier. | `EVIDENCE`. | Persist bounded evidence or a stable reference. | Yes. | Reuse ledger and Completion Review surfaces. |
| Evaluation | Combining the required verifier results against the frozen expected result while preserving disagreements and missing evidence. | Deterministic evaluator or independent reviewer. | `DERIVED`; does not authorize remediation or acceptance. | Recomputable when inputs are durable; persist the gate-facing result. | Partly, in reviews. | Introduce a bounded deterministic contract. |
| Evaluation result | `SATISFIED`, `NOT_SATISFIED`, `INDETERMINATE`, or `NOT_EVALUATED`, plus reasons and verifier completeness. | Evaluator/reviewer. | `DERIVED EVIDENCE`. | Persist for gate audit. | Implicit PASS/FAIL/BLOCKED. | Make the distinction explicit; do not collapse it into exit status. |
| Finding | A traceable discrepancy, risk, debt, or observation produced by verification/evaluation and linked to evidence. | Verifier/evaluator; owner adjudicates disposition. | `NON-AUTHORITATIVE EVIDENCE`. | Persist when material, deferred, recurrent, or needed for lineage. | Yes: M-01, M-02, RR-M01-01, N-01. | Reuse, with minimum common fields. |
| Material finding | A finding that fails a predeclared acceptance/safety predicate or makes required evidence indeterminate and therefore blocks the relevant gate. | Materiality rule comes from authority; evaluator applies it; owner adjudicates closure. | Gate-relevant evidence, not execution authority. | Persist with status and closure evidence. | Yes. | Define without adding a separate authority layer. |
| Non-blocking finding | A finding that does not fail the current acceptance contract but remains true and may be deferred. | Evaluator proposes; owner accepts/defer disposition. | `NON-AUTHORITATIVE EVIDENCE`. | Persist if durable; closure must not erase it. | Yes: N-01. | Preserve explicitly across acceptance and closure. |
| Failure class | A bounded causal/domain classification attached to a finding; one or more of `CANDIDATE`, `CONTRACT_AUTHORITY`, `VERIFIER_EVIDENCE`, `FIXTURE_ENVIRONMENT`, or `SCOPE_IDENTITY`. | Evaluator/reviewer. | `DERIVED`; may be owner-corrected. | Persist with the finding. | Informal labels already exist. | Introduce only these five domains; severity, acceptance impact, and disposition stay separate axes. |
| Baseline | A qualified pre-attempt identity/provenance anchor. The unqualified word `baseline` is insufficient. | Task contract/executor. | `EVIDENCE` binding. | Persist refs/digests only where later comparison requires them. | Yes, with several meanings. | Require a baseline kind; reject a universal snapshot. |
| Verifier baseline | Verifier identity/version, case/config identity, expected predicate, and relevant mutable-input hashes used for one result. | Task contract + verifier owner. | Subordinate expected-result contract. | Persist refs/digests; derive Git-tracked content from SHA. | Partly; v1.1 recommendation was deferred/routed. | `PARTIAL`: bind mutable/non-Git inputs, never duplicate Git. |
| Regression | A previously satisfied comparable predicate that now fails under an equivalent or explicitly migrated verifier baseline. | Evaluator. | `DERIVED EVIDENCE`. | Persist as a finding with both result refs. | Yes in tests/reviews, not uniformly bound. | Require comparability before using the label. |
| Acceptance criterion result | Per-AC conclusion supported by named verifier/evaluation evidence; it is not the acceptance decision itself. | Completion Review/evaluator; owner accepts the Change. | `DERIVED EVIDENCE`. | Persist in Completion Review. | Yes. | Reuse; add explicit evidence lineage where needed. |
| Learning signal | A repeated or severe, evidenced and potentially transferable finding that merits candidate review. | Evaluation/learning review. | `NON-AUTHORITATIVE`. | Persist only after no-op, privacy, recurrence/transferability checks. | Yes in recommendation governance. | Bounded recommendation input only. |
| PromptOps evidence | Prompt/version/hypothesis-to-attempt-to-evaluation lineage used to compare a prompt candidate. | PromptOps evaluator/central maintainer. | `NON-AUTHORITATIVE EVIDENCE`. | Persist with a bounded candidate; no automatic mutation. | Conceptually present in Roadmap/support. | Defer prompt mutation; first establish reusable evaluation semantics. |
| Retry / re-attempt | A new, separately authorized attempt made after a prior result/finding. It is not an automatic transition. | Owner authorizes; executor performs. | New owner authorization remains required. | Persist as another attempt record. | Yes in corrective passes. | Require explicit parent/finding links. |
| Attempt lineage | Links from attempt N+1 to its prior attempt, findings addressed, changed candidate/input, and new authorization. | Existing ledger. | Descriptive `EVIDENCE`. | Persist. | Informal review chain exists. | Add bounded links; no graph database. |

No term above creates a new source of execution, acceptance, policy, or routing
authority.

## 5. Ownership Boundaries

| Layer | Owns | Does not own |
|---|---|---|
| PL-V39-06 Resume/Context | Current authority selection, bounded context, handoff, freshness. | Attempt evaluation, operation selection, learning policy. |
| PL-V39-07 Operation Guidance | Applicable operation, route identity, route-specific predicate, capability envelope, result/evidence destinations, STOP and descriptive next gate. | Execution, success judgment, remediation, re-routing during evaluation. |
| Executor | Performs the separately authorized operation and records observed facts. | Declaring itself successful, changing verifier requirements, authorizing retry. |
| Verifier contract | Defines one check, required inputs, evidence, and result semantics. | Aggregate acceptance, authority changes, remediation. |
| Evaluation | Reconciles required verifier results with expected results; emits an evaluation result and findings. | Operation selection, execution, automatic repair/retry, policy mutation. |
| Owner/lifecycle gate | Authorizes attempts, adjudicates material findings, accepts/rejects/defer debt, and authorizes any retry/promotion. | Fabricating missing evidence. |
| Learning/PromptOps | Derives evidence-backed, non-authoritative improvement recommendations. | Editing prompts/policies, promoting a Change, or chaining another attempt automatically. |
| PL-V39-09 | Future compiler, work-packet, orchestration, chaining, and release concerns. | The evaluation semantics owned by PL-V39-08. |

The required separations are therefore:

```text
Operation Guidance does not execute.                         — PL-V39-07
Execution authorization does not imply success.              — owner/executor boundary
Successful process exit does not imply contract satisfaction.— verifier boundary
Green tests do not imply complete verification.              — required-verifier contract
Verification does not authorize remediation.                 — evaluator/owner boundary
Evaluation findings do not authorize another attempt.        — owner gate
```

## 6. Attempt Semantics

An explicit attempt abstraction is required, but an attempt lifecycle engine is
not. Existing task and ledger semantics need only a compact attempt record:

```text
attempt_ref: <Change>/<task-or-operation>/A<n>
authorization_ref: <owner decision or governed gate>
operation_ref: <OperationGuidance operation/route>
input_baseline_refs: <candidate + authority + bounded mutable inputs>
boundary_ref: <scope/capability contract>
observed_result: <bounded facts/artifact refs>
verifier_set_ref: <required and advisory verifier contracts>
verification_results: <zero or more refs>
evaluation_result: <one derived result>
finding_refs: <zero or more>
acceptance_decision_ref: <owner gate or PENDING>
parent_attempt_ref: <optional>
addresses_findings: <zero or more>
evidence_applicability: <attempt/candidate scope>
evidence_supersession_refs: <optional refs + reason>
```

The identity is local and deterministic. `T-06/A1`, `T-06/A2`, and `T-06/A3`
are distinct because the ledger ordinal and bound candidate/input snapshot are
distinct. Candidate SHA alone is insufficient: pre-commit corrections may
share the same HEAD while their scoped working-tree fingerprints differ.

PL-V39-08 needs four orthogonal milestones, not one state machine:

| Question | Minimum recorded fact |
|---|---|
| Did execution happen? | observed result exists, or explicit interrupted/invalid result |
| Did required verification happen? | verifier-set completeness plus individual results |
| Did evaluation happen? | one evaluation result with evidence refs |
| Was the result accepted? | separate owner acceptance/remediation/rejection/defer decision |

`PREPARED` is already represented by Plan/task plus authorization. `RUNNING` is
normally ephemeral. `COMPLETED`, `VERIFICATION_FAILED`, `EVALUATION_FAILED`, and
`ACCEPTED` should not become mutually exclusive lifecycle states because the
underlying facts are independent: an execution may complete while verification
fails, and an accepted Change may retain non-blocking debt.

Attempt N+1 must reference attempt N and the findings it claims to address.
The new authorization, candidate/input delta, verifier baseline, and evidence
applicability/supersession relation must remain visible. Supersession may change
which evidence applies to current acceptance, but never deletes or rewrites the
historical evidence. Retry is never inferred from a finding and never automatic.

## 7. Verification / Evaluation Semantics

### Distinct evidence activities

| Activity | Question answered | PL-V39-07 specimen |
|---|---|---|
| Test execution | Did the executable test predicates pass? | 306/313/324 green suites |
| Verification | Does one declared predicate hold for this attempt and baseline? | pytest, diff/scope checks, SHA checks |
| Independent review | Does an independently applied semantic/adversarial contract verifier pass? | M-01/M-02 and RR-M01-01 reviews |
| Field proof | Does observable behavior hold in a qualified disposable consumer topology? | T-07/T-08 |
| Evaluation | Are all required verifier results sufficient and mutually admissible for the expected contract? | Completion Review reconciliation |
| Acceptance | Does the owner accept the evaluated candidate and residual debt? | owner closure |

A task may have multiple verifier classes. A verifier can be required yet
insufficient. The minimum contract is a bounded list, not a plugin registry:

```text
verifier_id/version
class: deterministic_test | structural_check | independent_review | field_proof | independent_human_review
required: YES | NO
input/evidence refs
expected predicate
result: PASS | FAIL | INVALID | NOT_RUN
failure semantics
independence/provenance where material
```

```text
OWNER_GATE != VERIFIER
```

`independent_human_review` may produce verification/evaluation evidence and
findings. An owner gate is governance authority and is not a verifier, result,
retry permission, implementation permission, or Git permission.

Aggregate evaluation uses hard requirements:

```text
SATISFIED
  all required verifiers PASS and evidence is admissible

NOT_SATISFIED
  at least one required verifier validly FAILS

INDETERMINATE
  required evidence is missing, invalid, incomparable, or its verifier is defective

NOT_EVALUATED
  evaluation has not run, including an infrastructure-invalid attempt
```

No average score can erase a failed safety, authority, scope, or material
contract verifier. Advisory results may produce non-blocking findings but cannot
upgrade a failed required result.

This makes `324 passed` and `candidate failed review` consistent: the test
verifier is `PASS`; the independent contract verifier is `FAIL`; the aggregate
evaluation is `NOT_SATISFIED`.

## 8. Baseline and Provenance

The word `baseline` is valid only with a kind:

| Baseline kind | Meaning | Capture before attempt? | Persist? | Reconstruction rule |
|---|---|---|---|---|
| Repository source baseline | Central/consumer Git HEAD and relevant status | YES when source identity affects evidence | SHA + bounded dirty manifest | Reconstruct tracked bytes from Git; do not copy them. |
| Candidate identity | Exact artifact under evaluation | YES | Commit SHA, or scoped manifest/digests for an uncommitted candidate | Never equate HEAD alone with a dirty candidate. |
| Expected contract baseline | Approved authority, AC, result/evidence and capability refs | YES | Stable refs and hashes where drift matters | Read frozen authority; do not duplicate its body. |
| Verifier baseline | Verifier version, cases/config, expected predicate, mutable inputs | YES for required verifiers | Refs/digests; bounded non-Git hashes when necessary | Git-tracked verifier content comes from its SHA. |
| Test-result baseline | Prior comparable result used to claim regression/improvement | NO for ordinary execution; YES only for comparison claims | Prior result ref | Reuse ledger/eval history. |
| Field-proof baseline | Fixture HEAD/status/topology and bounded authority hashes | Conditional: YES for consumer proof | Bounded facts/hashes | Fixture may be disposable, so persist the minimum proof facts. |

The baseline model is therefore `PARTIAL`: identity, authority, verifier, and
non-reconstructable mutable inputs are captured; no universal filesystem
snapshot is introduced. The two-layer baseline idea from the deferred v1.1
recommendation is retained only as this rule: Git identifies tracked inputs;
bounded hashes/manifest identify relevant ignored or external control inputs.
Git remains the source store.

## 9. Finding / Retry Lineage

### Minimum classification

Use four orthogonal fields:

```text
severity:
  MATERIAL
  NON_BLOCKING

responsibility_domains:
  one or more of CANDIDATE, CONTRACT_AUTHORITY, VERIFIER_EVIDENCE,
  FIXTURE_ENVIRONMENT, SCOPE_IDENTITY

acceptance_impact:
  BLOCKS_CURRENT_ACCEPTANCE
  DOES_NOT_BLOCK_CURRENT_ACCEPTANCE

disposition:
  OPEN
  OWNER_ADJUDICATED
  REMEDIATION_REQUIRED
  DEFERRED
  CLOSED
  SUPERSEDED
```

Specific finding IDs and prose retain the useful detail. The small domain set is
multi-valued, so a finding can correctly implicate both a candidate and verifier
coverage without forcing a false single owner. `severity` is distinct from
responsibility; `acceptance_impact` is distinct from both; `disposition` records
the owner-governed outcome. `test coverage defect` belongs to
`VERIFIER_EVIDENCE`; environment defect belongs to `FIXTURE_ENVIRONMENT`; scope
drift and candidate drift belong to `SCOPE_IDENTITY`.

### Empirical cases

| Case | Representation |
|---|---|
| A — tests green, review fails | Same attempt: test verifier `PASS`, independent contract verifier `FAIL`, technical evaluation `NOT_SATISFIED`, material findings M-01/M-02. No contradiction and no owner disposition. |
| B — correction exposes another defect | A2 points to A1 and addresses M-01/M-02. Re-review closes those claims for A2 but emits RR-M01-01. A3 points to A2 and RR-M01-01; its re-review passes. Earlier failures remain historical and are superseded only for current acceptance of the corrected candidate. |
| C — field proof succeeds | T-07/T-08 field-proof verifier results bind the same committed candidate SHA, qualified disposable fixtures, topology, and no-mutation observations. They supplement rather than replace central checks/review. |
| D — debt survives acceptance | N-01 has `severity=NON_BLOCKING`, `responsibility_domains={VERIFIER_EVIDENCE}`, `acceptance_impact=DOES_NOT_BLOCK_CURRENT_ACCEPTANCE`, and `disposition=DEFERRED`. Owner disposition references it as residual debt; closure does not mark it fixed. |
| E — verifier is defective | Emit a `MATERIAL` finding with `responsibility_domains={VERIFIER_EVIDENCE}`; mark the verifier result `INVALID` and aggregate evaluation `INDETERMINATE` or `NOT_EVALUATED`. Do not blame or repair the candidate automatically. |

Every corrective attempt records `parent_attempt_ref`, `addresses_findings`,
new authorization, candidate/input delta, evidence applicability, and explicit
supersession references where applicable. A later PASS closes only findings
that its verifier actually rechecked; it does not erase or rewrite the failed
record.

## 10. Learning / PromptOps Boundary

### Learning

For Planning Lite, learning is the bounded derivation of a non-authoritative
recommendation candidate from repeated or severe evaluated findings. It is not
runtime adaptation.

```text
evidence collection                 may be automated
verification/evaluation             may be automated when deterministic
finding classification              may be automated with visible provenance
human/owner adjudication             remains governed
candidate recommendation            may be generated, never self-promoted
policy/prompt/skill/template change  requires an ordinary central Change
automatic retry                      forbidden without separate authorization
```

A learning signal must retain attempt, finding, evidence, applicability,
privacy, recurrence/transferability, and no-op analysis. The default is no
recommendation.

### PromptOps

The smallest useful definition is:

```text
versioned prompt/instruction identity
+ explicit change reason and hypothesis
+ prompt-to-attempt lineage
+ qualified verifier evidence
+ finding-to-recommendation lineage
+ owner-governed comparison/promotion decision
```

PromptOps in PL-V39-08 is recommendation/evidence-first. It does not mean prompt
search, automatic rewriting, self-modifying policy, or automatic champion
replacement. A future prompt comparison may reuse the same attempt/evaluation
contract, but the first Change does not require Prompt Garden integration,
model judging, or prompt mutation.

## 11. Recommendation Inbox Placement

The deferred recommendation-inbox pilot belongs inside PL-V39-08 as a bounded,
self-hosted behavioral evaluation fixture after the minimum attempt/evaluation
contract is stable:

```text
evaluated finding
→ recommendation candidate
→ existing inbox/intake surface
→ explicit owner disposition
```

This placement follows the canonical Roadmap, which reserves the next
recommendation-intake exercise as a PL-V39-08 behavioral eval fixture. It is no
longer a PL-V39-07-adjacent proof because PL-V39-07 is closed. The inbox remains
an intake/evidence surface, not a registry or authority store. This shaping does
not implement or populate it.

## 12. PL-V39-09 Boundary and Compatibility

PL-V39-08 explicitly excludes:

```text
Context Compiler
AgentWorkPacket productization
multi-agent orchestration
automatic workflow chaining
automatic retry orchestration
release orchestration
general release automation
```

PL-V39-08 may emit bounded evaluation evidence and accepted contracts that a
future PL-V39-09 system consumes. It must not schedule or route that system.

The baseline capability must work offline in all PL-V39-05-C topologies:

```text
single-repo
split-control
local-only
```

It may use Git identity and local bounded hashes, but cannot require a network,
central cloud service, hidden database, daemon, vector store, embeddings, or
semantic retrieval. Evaluation history is referenced through existing ledger,
review, Git, and evidence artifacts; it is not a second PL-V39-06 context or
memory authority.

## 13. Minimum Viable Architecture

### Operational grammar

Derived from the PL-V39-07 evidence, the proposed grammar is:

```text
[AUTHORITY] governed operation
→ [AUTHORITY] owner-authorized attempt
→ [EVIDENCE] observed result
→ [AUTHORITY REF] required verifier contracts
→ [EVIDENCE] verifier evidence
→ [DERIVED] technical evaluation
→ [DERIVED] findings
→ [DERIVED] technical acceptance state
→ [AUTHORITY] owner-governed disposition/remediation/continuation gate
→ [NON-AUTHORITATIVE] optional learning or PromptOps recommendation
```

```text
AUTHORITY POINTS:
operation authorization; attempt authorization; owner disposition;
retry/remediation authorization

DERIVED / EVIDENCE POINTS:
observed result; verifier evidence; technical evaluation; finding;
technical acceptance state; learning recommendation; PromptOps recommendation
```

### Composition

```text
ResumeContext
+ OperationGuidance
+ existing task/result/evidence contracts
+ existing Execution Ledger and Completion Review
+ minimal AttemptEvaluationV1-shaped records
```

`AttemptEvaluationV1-shaped` means a bounded contract, not necessarily a new
standalone file or global entity. The first Change should prefer structured
blocks within the existing cumulative ledger and derived evaluation output.
A separate artifact is justified only for an independently valuable large
review/eval report, as Completion Review already demonstrates.

No new event bus, database, global registry, workflow engine, agent registry,
or lifecycle engine is justified. The verifier set is declared by the existing
task/operation authority. Git and bounded evidence hashes provide provenance.

### Required decisions

```text
New persistent authority: NO
New registry: NO
New lifecycle engine: NO
New database: NO
New skill: NO for the first Change
New CLI surface: NO for the first Change
Attempt abstraction: REQUIRED / ledger-scoped contract only
Verifier abstraction: CONTRACT_ONLY
Baseline snapshot: PARTIAL
```

The first Change can prove the semantic contract through pure evaluation logic,
existing execution/review surfaces, and tests. A later CLI or skill proposal
requires its own evidence and owner-approved scope.

## 14. Candidate Internal Phases

Keep one PL-V39-08 roadmap vertebra. The phase counts are explicit:

```text
PRE_DEFINITION_RECONCILIATION: 1
IMPLEMENTATION_PHASES: 2
```

`08-A — Research Asset Reconciliation` is bounded pre-Definition
reconciliation only. It classifies already-routed support/design evidence as
`REUSE`, `ADAPT`, `REFERENCE_ONLY`, `ARCHIVE_REQUIRED`, or `ARCHIVE_SAFE`,
preserves lineage, and freezes the PL-V39-07 empirical cases. It is not an
implementation phase and introduces no registry, knowledge base, retrieval,
ingestion, database, or persistent asset model.

The actual implementation phases are:

1. `08-B — Governed Attempt Evaluation`: define the minimal attempt identity,
   verifier contract, partial baseline, technical evaluation result,
   orthogonal finding model, evidence applicability/supersession, retry
   lineage, and qualified control-plane case behavior. This is the smallest
   coherent first implementation Change.
2. `08-C — Controlled Learning and PromptOps Evidence`: consume 08-B findings
   and evidence for finding-to-recommendation-to-owner disposition, including
   the recommendation-inbox fixture; add prompt/version comparison evidence
   only after 08-B is stable. It introduces no PL-V39-09 orchestration.

These are internal phases, not new Roadmap slices. PL-V39-09 remains the next
macro-phase.

## 15. Candidate Acceptance Dimensions

The later Change Definition should refine, not copy blindly, these ten
dimensions:

1. Deterministic ledger-scoped attempt identity and explicit parent/finding
   lineage across corrections.
 2. Exact preservation of PL-V39-07 authority/capability boundaries: technical
    evaluation grants no execution, repair, retry, staging, acceptance, or
    continuation authority; owner disposition remains separate.
3. Observable-result versus expected-result separation, including successful
   exit with unsatisfied contract.
4. Bounded required/advisory verifier binding with multiple verifier classes and
   hard-gate semantics.
5. Deterministic aggregate outcomes for PASS, FAIL, invalid/missing evidence,
   and infrastructure-invalid runs.
6. Partial baseline/provenance sufficient for committed and dirty candidates,
   mutable verifier inputs, and disposable field fixtures without duplicating
   Git.
 7. Multi-valued responsibility domains, distinct severity and acceptance
    impact, and preservation of historical failed reviews, corrections, and
    evidence applicability/supersession/closure evidence.
8. Acceptance that can coexist with explicitly deferred non-blocking debt.
9. Non-authoritative learning/PromptOps recommendation lineage and existing
   inbox owner gate, with no automatic mutation or retry.
10. Offline single-repo/split-control/local-only compatibility and explicit
    07/08/09 boundary preservation without database, registry, memory, or
    orchestration expansion.

These are shaping dimensions, not final acceptance criteria.

## 16. Nearest-Wrong Architectures

| ID | Risk | Why tempting | Bounded prevention |
|---|---|---|---|
| A | `test passed = task succeeded` | Tests are cheap, binary, and already visible. | Treat test execution as one verifier result; acceptance requires the declared verifier set and evaluation. |
| B | Evaluation becomes another authority layer | An evaluator appears to know whether work is good. | Evaluation emits derived evidence/findings only; owner/lifecycle retains authorization and acceptance. |
| C | Evaluation becomes another memory/database system | Attempt history looks queryable and relational. | Persist compact refs in existing ledgers/reviews and Git; no hidden store, RAG, or always-loaded history. |
| D | One giant generic verifier framework | Tests, review, field proof, and model judging share vocabulary. | Use a small contract and bounded declared list; no plugins/registry; first consumer is PL-V39-07 evidence. |
| E | PromptOps becomes autonomous prompt mutation | Execute-evaluate-rewrite loops are easy to demonstrate. | Recommendation/evidence only; versioned challenger requires owner-governed central Change and regression evidence. |
| F | Attempt lifecycle becomes orchestration | PREPARED/RUNNING/RETRY resemble a workflow state machine. | Record four orthogonal milestones; no scheduler, auto-transition, or lifecycle engine. |
| G | Retry becomes automatic authorization | A material failure seems to imply the next corrective action. | Every re-attempt has a separate authorization ref and parent/finding links; evaluator cannot execute. |
| H | Baseline duplicates Git | Reproducibility invites full snapshots. | Persist SHA/refs and only bounded hashes for dirty, ignored, or external inputs. |
| I | Finding taxonomy explodes | Every historic defect suggests a new category. | Five bounded, multi-valued responsibility domains plus separate severity, acceptance impact, and disposition; detailed meaning stays in the finding itself. |

## 17. Open Questions and Support-Evidence Adjudication

### Resolved support direction

- The canonical Roadmap's broad Reusable Eval Core is compatible with this
  shape, but its full dormant entity list is design input, not an automatically
  approved first-Change schema. Empirical evidence supports starting with the
  smaller attempt/verifier/evaluation subset.
- The Roadmap verifier hierarchy permits structured graders, model judges, and
  human review. The first Change requires none of them as a generic runtime;
  it requires only explicit verifier contracts and uses the cheapest reliable
  evidence.
- The support review says Evaluation and Controlled Evolution are broad but
  should remain one limb to avoid a second runtime. The pre-Definition
  reconciliation plus two implementation phases preserve that one-limb decision.
- The absorbed learning and controlled-evolution recommendations agree that
  observation may produce a hypothesis/recommendation, while framework changes
  still require a normal central Change. There is no material contradiction.
- The current checkout no longer contains the original verifier-baseline v1.0,
  v1.1, or CHG-0009 incoming files. Their canonical Incoming Adjudication
  preserves identities, hashes, dispositions, and the bounded two-layer
  baseline summary. This shaping does not invent missing details or promote the
  absent files to authority.

### Questions deferred to Definition/Plan detail, not architectural blockers

1. Which dormant v3.7 assets are `REUSE` versus `ADAPT` after the bounded 08-A
   reconciliation?
2. Whether the structured ledger payload is represented as Markdown fields or
   an embedded versioned data block; either must remain human-reviewable and
   deterministic.
3. The exact first verifier-set names and case IDs for the PL-V39-07 fixture;
   the Definition must freeze them before implementation.

No current question requires a new authority store, registry, database, skill,
CLI, or lifecycle engine.

## 18. Recommended Change Shape

Proposed identifier, not yet created or approved:

```text
CHG-PL-V39-08-GOVERNED-ATTEMPT-EVALUATION-001
```

Proposed one-sentence objective:

```text
Define and prove a minimal offline contract that binds an authorized operation
attempt to observed results, multiple required verifier results, deterministic
evaluation, findings, residual debt, and explicit retry/acceptance lineage
without creating new authority or orchestration.
```

Proposed in-scope shape:

- bounded reconciliation/disposition of only the eval assets required by this
  Change;
- minimal attempt identity/input/boundary/result contract attached to existing
  task and ledger evidence;
- contract-only verifier declarations and deterministic aggregate outcomes;
- partial baseline/provenance for Git and non-reconstructable bounded inputs;
- orthogonal finding severity/responsibility/acceptance-impact/disposition plus
  evidence applicability and retry lineage;
- executable cases A–E derived from PL-V39-07;
- offline topology and 07/08/09 boundary discriminators.

Explicitly out of scope:

- global eval/plugin registry, database, service, event bus, model-judge
  platform, generic campaign engine, scoring dashboard, or new memory system;
- new public CLI or skill in the first Change;
- Prompt Garden/product prompt optimization, automatic prompt/policy mutation,
  auto-retry, recommendation promotion, orchestration, compiler, work packet,
  release automation, or PL-V39-09 implementation.

Status summary:

```text
PL-V39-08 primary problem: TECHNICAL_EVALUATION_SEPARATED_FROM_OWNER_DISPOSITION
Primary capability: GOVERNED_ATTEMPT_EVALUATION
New persistent authority: NO
New registry: NO
New lifecycle engine: NO
New database: NO
New skill: NO
New CLI surface: NO
Attempt abstraction: REQUIRED
Verifier abstraction: CONTRACT_ONLY
Baseline snapshot: PARTIAL
Owner gate as verifier: NO
Responsibility domains: MULTI_VALUED
Evidence supersession lineage: EXPLICIT / HISTORY PRESERVED
Pre-Definition reconciliation: 1
Implementation phases: 2
08-A implementation phase: NO
PromptOps: versioned recommendation/evidence lineage; no automatic mutation
Learning: non-authoritative evidence-to-recommendation signal; owner promotion
Recommendation inbox: INSIDE PL-V39-08 AS A LATER BOUNDED EVAL FIXTURE
PL-V39-09 boundary: COMPILER / ORCHESTRATION / CHAINING / RELEASE EXCLUDED
Definition: NOT CREATED
Implementation: NOT STARTED / NOT AUTHORIZED
```

## 19. Exact Next Owner Gate

```text
OWNER_AUTHORIZATION_PL_V39_08_CHANGE_DEFINITION
```

The reviewed shaping is ready for the separate owner authorization gate for
Change Definition drafting. This does not authorize Definition approval,
Implementation Plan, Formal Readiness, implementation, recommendation-inbox
execution, PL-V39-09 work, staging, commit, tag, push, merge, or release.

## 20. Tightening Binding Check

```text
TIGHTENING_01: APPLIED
TIGHTENING_02: APPLIED
TIGHTENING_03: APPLIED
TIGHTENING_04: APPLIED
TIGHTENING_05: APPLIED
PRIMARY_CAPABILITY: GOVERNED_ATTEMPT_EVALUATION
ATTEMPT: MINIMAL
VERIFIER: CONTRACT_ONLY
OWNER_GATE_AS_VERIFIER: NO
RESPONSIBILITY_DOMAINS: MULTI_VALUED
EVIDENCE_SUPERSESSION: EXPLICIT / HISTORY_PRESERVED
08-A_IMPLEMENTATION_PHASE: NO
IMPLEMENTATION_PHASES: 2
NEW_SYSTEMS: NONE
```
