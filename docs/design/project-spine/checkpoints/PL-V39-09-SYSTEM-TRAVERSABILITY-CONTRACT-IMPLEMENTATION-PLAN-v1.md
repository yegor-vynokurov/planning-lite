# PL-V39-09 System Traversability Contract and Critical Journey Binding - Implementation Plan v1

Status: PLAN_APPROVED / FORMAL_READINESS_NOT_YET_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED

This canonical Implementation Plan checkpoint materializes the approved
noncanonical Plan candidate after explicit owner approval and final focused
review.

~~~text
OWNER_DECISION: APPROVE_PL_SYSTEM_TRAVERSABILITY_FINAL_IMPLEMENTATION_PLAN
CANONICALIZATION: CANONICAL_PLAN_CREATED
PLAN_STATUS: PLAN_APPROVED
FORMAL_READINESS_STATUS: NOT_YET_AUTHORIZED
IMPLEMENTATION_AUTHORIZED: NO
~~~

It is Plan authority and evidence only. It does not authorize Formal Readiness,
authorize implementation, resume the runtime prerequisite, resume Change 2,
consume the major PL09 gate, or authorize staging, commit, push, or release.


### Canonical checkpoint lineage

~~~text
CANONICAL_PLAN_PATH: docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-IMPLEMENTATION-PLAN-v1.md
APPROVED_SOURCE_PLAN_PATH: .local/work/experiments/PL_SYSTEM_TRAVERSABILITY_IMPLEMENTATION_PLAN_CANDIDATE.md
APPROVED_SOURCE_PLAN_SHA256: 71FF99DDAB1C49D5183C30FE2724DC32E777AC5066E5D302A8FDEE1F9CA94B4B
CANONICAL_DEFINITION_PATH: docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-CHANGE-DEFINITION-v1.md
CANONICAL_DEFINITION_SHA256: 764E8D2702B964DD6F7B7C4A37289DB49271331A07270AE1BE9D99089C592820
DEFINITION_ACTIVATION_PATH: docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-DEFINITION-ACTIVATION-v1.md
DEFINITION_ACTIVATION_SHA256: 2953BFD736B72AC08525EE095CCE89958EF0EC3B8AB189F6A7CCCB447BC11805
FINAL_FOCUSED_REVIEW_PATH: .local/work/experiments/PL_SYSTEM_TRAVERSABILITY_FINAL_IMPLEMENTATION_PLAN_FOCUSED_REVIEW.md
FINAL_FOCUSED_REVIEW_SHA256: 89C3F250AB1FB9A9D474F9F8C0986F9D2ABCFDA1FC14AFF0C7313B50CDA69991
FINAL_FOCUSED_REVIEW_VERDICT: PASS
SEMANTIC_DELTA_FROM_APPROVED_PLAN: NONE
CANONICALIZATION_DELTA: HEADER_STATUS_PATH_LINEAGE_AND_RECEIPT_METADATA_ONLY
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_PL_SYSTEM_TRAVERSABILITY_FORMAL_READINESS
~~~

## 1. Plan identity and exact authority binding

~~~text
CHANGE_ID: CHG-PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-001
CHANGE_NAME: System Traversability Contract and Critical Journey Binding
CANONICAL_DEFINITION: docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-CHANGE-DEFINITION-v1.md
CANONICAL_DEFINITION_SHA256: 764E8D2702B964DD6F7B7C4A37289DB49271331A07270AE1BE9D99089C592820
DEFINITION_ACTIVATION: docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-DEFINITION-ACTIVATION-v1.md
DEFINITION_ACTIVATION_SHA256: 2953BFD736B72AC08525EE095CCE89958EF0EC3B8AB189F6A7CCCB447BC11805
APPROVED_CANDIDATE_SHA256: DCDBC579E9D88F0BB4049E254AF5D976D1D23A89F4D49F931D13328711418A43
BASELINE_HEAD: befa1780093335c99318526a3b3368c0f2a23ee0
OWNER_DECISION: APPROVE_PL_SYSTEM_TRAVERSABILITY_FINAL_IMPLEMENTATION_PLAN
PLANNING_AUTHORIZED: YES
IMPLEMENTATION_AUTHORIZED: NO
FORMAL_READINESS_AUTHORIZED: NO
~~~

Planning is bound to the exact canonical Definition digest above. A changed
Definition digest invalidates this candidate and requires a new owner gate.
This candidate does not claim that the currently active central CURRENT.md
Change 2 state has been replaced; the authorized output is intentionally an
ignored local planning artifact awaiting independent review.

## 2. Planning objective and result boundary

Prepare one deterministic plan for the minimum coherent realization of
SYSTEM_TRAVERSABILITY_CONTRACT_AS_CROSS_CUTTING_INVARIANT.

The plan must establish the semantic carrier, workflow obligations, pure
observation helpers, focused regression evidence, integrity projections, and
later readiness evidence. It must preserve all frozen ownership boundaries and
must not implement the Governed Operation Lifecycle prerequisite or any runtime
pump.

The canonical Plan deliverable is exactly:

~~~text
docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-IMPLEMENTATION-PLAN-v1.md
~~~

Its lifecycle status is PLAN_APPROVED / FORMAL_READINESS_NOT_YET_AUTHORIZED /
IMPLEMENTATION_NOT_AUTHORIZED. The approved source candidate, active consumer
Change record, CURRENT.md, and implementation paths remain unchanged by this
canonicalization.

## 3. Frozen semantic constraints

The implementation must preserve, without reinterpretation:

- one Project Spine-owned CriticalJourney carrier for each applicable
  materially multi-stage Target flow;
- separate Capability Walking Skeleton and System Walking Skeleton;
- exactly five durable journey states:
  NOT_DEFINED, DEFINED, WIRED_FAIL, WIRED_TRAVERSABLE, PASSING;
- exactly four top-level Gap classes:
  IMPLEMENTATION_GAP, WIRING_GAP, ORCHESTRATION_GAP, EVIDENCE_GAP;
- Activation only as a qualifier/subclass of WIRING_GAP;
- FIRST_BROKEN_SEAM and DOWNSTREAM_UNREACHABLE;
- local proof plus the cheapest adequate system traversability non-regression
  for affected journeys;
- an evidence-backed per-Change bypass only for genuinely unaffected work;
- pure, deterministic, no-authority validation over caller-supplied facts;
- no validator persistence, repository scan, routing, execution, state mutation,
  next-gate decision, runtime-lifetime ownership, or evidence authority;
- durable current_state updates only through governed lifecycle / Project Spine
  reconciliation;
- the early vertical-flow rule;
- the self-hosted expected-red regression;
- the complete non-circular Change 2 resume conjunction;
- no Vitality subsystem, registry, database, scheduler, graph engine, broad
  E2E platform, duplicated lifecycle, new Roadmap vertebra, or authority
  transfer.

The 15 Definition paths are semantic owners/surfaces. Any additional path in
this plan is mechanical integrity or an existing generic projection only. No
additional semantic owner is introduced.

## 4. Exact path budget

~~~text
DEFINITION_MANDATED_PATH_COUNT: 15
PLAN_RESOLVED_PROJECTION_PATH_COUNT: 0
MECHANICAL_INTEGRITY_PATH_COUNT: 2
PLAN_ADDITIONAL_PATH_COUNT: 2
TOTAL_PLANNED_PATH_COUNT: 17
NEW_SEMANTIC_OWNER_COUNT_OUTSIDE_DEFINITION: 0
~~~

### 4.1 Definition-mandated path inventory

| Path | ADD/MODIFY | Surface class | Exact planned binding |
|---|---|---|---|
| docs/design/project-spine/roadmap/ROADMAP.md | MODIFY | CANONICAL_DESIGN | Extend existing Target Skeleton, cross-cutting invariant, small-change, and Project Spine integrity/orphan guidance without adding a Roadmap outcome or vertebra. |
| template/.planning/control/STATE_OWNERSHIP.md | MODIFY | TEMPLATE_CONTROL | In the `# State ownership` table, after the exact `project documents` row, add singular ownership for `project/CRITICAL_JOURNEYS.md`; append the derived-history rule under `## Duplication rules`. |
| template/.planning/control/TARGET_BASELINE_CALIBRATION.md | MODIFY | TEMPLATE_CONTROL | Extend `## Allowed write scope`; in `## Procedure`, after item 9 before item 10, add the applicability, REQUIRED/NOT_APPLICABLE reason, DEFINED prerequisite, System Walking Skeleton handoff, and evidence-channel output. |
| template/.planning/control/CAUSAL_GAP_DERIVATION.md | MODIFY | TEMPLATE_CONTROL | Extend `## Gap definition`, `## Gap record contract`, and `## Hard checks` with the four traversability classes, first-cause/Activation seam relation, journey-linked closure, and no-parallel-registry rule. |
| template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md | MODIFY | TEMPLATE_CONTROL | Extend `## RoadmapOutcome synthesis` after its required candidate fields and `## Bounded-Change handoff` after its handoff fields with journey lineage, skeleton obligation, no-path visibility, and downstream Change binding. |
| template/.planning/control/CHANGE_DEFINITION.md | MODIFY | TEMPLATE_CONTROL | Require material Change definitions to declare affected journeys, expected state delta, system-proof requirement or evidence-backed bypass, affected-surface check, and first broken seam where known. |
| template/.planning/control/CHANGE_PLANNING.md | MODIFY | TEMPLATE_CONTROL | Bind exact seams, carrier projections, pure helper contracts, vertical sequence, evidence, and mandatory architecture STOP output to Plan preparation. |
| template/.planning/control/CHANGE_READINESS.md | MODIFY | TEMPLATE_CONTROL | Add exhaustive affected-journey audit, blocked/placeholder/PASSING distinctions, expected-red evidence, no false promotion, bypass proof, and no-authority-transfer checks. |
| template/.planning/control/CHANGE_EXECUTION.md | MODIFY | TEMPLATE_CONTROL | Add Execution Envelope obligations for affected journeys, system proof, reconciliation boundary, and explicit prohibition on validator-to-carrier mutation or future orchestration absorption. |
| template/.planning/control/CHANGE_CLOSURE.md | MODIFY | TEMPLATE_CONTROL | Require closure evidence for observed journey state/latest observation and separate Project Spine Gap/Roadmap reconciliation; completion never auto-promotes state or closes Gap. |
| template/.planning/disciplines/DELIVERY_SLICES.md | MODIFY | TEMPLATE_CONTROL | Define System Walking Skeleton as a tracer-bullet slice and require outcome, blocking edge, verification seam, blast radius, and recovery for each journey-affecting task. |
| template/.planning/project/CRITICAL_JOURNEYS.md | ADD | PROJECT_TEMPLATE / project-owned carrier seed | Add the human-reviewable current carrier with the exact minimum CriticalJourney fields and five-state model. |
| template/.planning/templates/project/CRITICAL_JOURNEYS.md | ADD | PROJECT_TEMPLATE / pristine source | Add the pristine managed source for the project-owned carrier; updates remain protected by existing project ownership rules. |
| src/planning_lite/traversability.py | ADD | VALIDATOR / HELPER | Add the pure deterministic V1 input/result types and exactly the two bounded public helpers for per-journey smoke and aggregate system traversability. |
| tests/test_system_traversability.py | ADD | TEST / EVAL | Add focused executable coverage for the carrier projection, states, Gap semantics, blocked precedence, pure boundary, bypass distinction, expected red, and no-authority constraints. |

### 4.2 Plan-resolved mechanical integrity paths

| Path | Class | WHY_REQUIRED | Exact handling |
|---|---|---|---|
| template/.planning/docs/MANIFEST_V4.md | MECHANICAL_INTEGRITY | Existing tests require manifest paths to equal the complete template tree and the file count to match. Two new project template files otherwise fail exact-tree integrity. | Add both CriticalJourneys template paths and update the file count; no new semantic guidance is placed here. |
| template/.planning/framework/SHA256SUMS.txt | MECHANICAL_INTEGRITY | Existing tests require one canonical-LF checksum for every template file except the checksum file itself. The two added template files require receipts and all modified template files require refreshed digests. | Regenerate from the complete manifest-aligned template tree after all template edits; do not hand-maintain stale hashes. |

No ROOT_ROUTER.md, CONTEXT_POLICY.md, TARGET_STATE_EXPLORER.md,
EXECUTION_ROUTING.md, Change record template, copier.yml, OWNERSHIP.yml,
source runtime module outside traversability.py, or existing test file is
required by the current repository evidence. Adding any of those paths requires
a concrete contract failure and explicit Plan-time architecture review.

## 5. CriticalJourney carrier realization

Both project carrier files will use the same pristine markdown structure. The
project file is the project-owned current record; the templates file is the
managed source. The carrier is not parsed as a runtime database and does not
store event history.

The carrier has one deterministic, human-reviewable serialization. The exact
format is:

~~~text
# Critical Journeys

## Journey: <journey_id>
- journey_id: `<nonempty-token>`
- applicability: REQUIRED | NOT_APPLICABLE
- applicability_reason: `<nonempty-single-line-text>`
- target_refs: [] | [`<ref>`, ...]              # lexicographically sorted
- roadmap_refs: [] | [`<ref>`, ...]             # lexicographically sorted
- entry_ref: `<ref>` | NONE_DECLARED
- ordered_nodes: [] | [1:`<ref>`, 2:`<ref>`, ...]
- ordered_seams: [] | [1:`<ref>`, 2:`<ref>`, ...]
- runtime_lifetime_owner_ref: `<ref>` | NONE_DECLARED
- identity_continuity_ref: `<ref>` | NONE_DECLARED
- placeholder_policy: NONE | NOT_IMPLEMENTED | FIXTURE_ONLY
- terminal_semantics: `<nonempty-single-line-text>`
- evidence_channel_ref: `<ref>` | NONE_DECLARED
- current_state: NOT_DEFINED | DEFINED | WIRED_FAIL | WIRED_TRAVERSABLE | PASSING | NONE
- gap_refs: [] | [`<ref>`, ...]                 # lexicographically sorted
- last_observation_ref: `<ref>` | NONE
~~~

The H1 is exactly `# Critical Journeys`. Every record starts with exactly
`## Journey: <journey_id>`, contains no nested heading, uses the 16 bullets
above exactly once and in that order, and is separated from the next record by
one blank line. Records are sorted lexicographically by journey_id and duplicate
IDs are invalid. Lists use `[]` for empty values; non-empty unordered lists are
lexicographically sorted and ordered lists preserve their displayed indexes.
`NONE` is a serialization sentinel for current_state only when
applicability is NOT_APPLICABLE; it is not a sixth journey state. A REQUIRED
record must use one of the five canonical states. A NOT_APPLICABLE record must
have a non-empty reason, `current_state: NONE`, no required journey-state
transition, and must not be used as a per-Change bypass. A REQUIRED record must
have `applicability_reason`, target lineage, an explicit entry/lifetime/
identity/evidence decision, and `current_state: NOT_DEFINED` until its contract
is complete. The focused validator tests this exact shape, field order, enum
set, list encoding, uniqueness, and applicability/state separation.

Each journey ID occurs once. Each REQUIRED record has one current_state and one
latest-observation pointer. Runtime observations, append-only history, receipts,
event logs, schedules, registry entries, and evidence truth stay in their
existing owners.

Applicability is decided from accepted Target outcomes and key journeys:

1. two or more separately owned runtime capability nodes are connected by
   material handoff seams; or
2. one operation identity or runtime lifetime crosses a process, persistence,
   host, authority, or lifecycle boundary where loss invalidates the outcome.

An applicable outcome gets a REQUIRED carrier record and starts NOT_DEFINED
until its contract is complete. The first affected implementation Change must
not proceed as if the journey were absent; it must establish DEFINED and its
early System Walking Skeleton obligation.

The durable state relation is exactly:

~~~text
NOT_DEFINED -> DEFINED
DEFINED -> WIRED_FAIL | WIRED_TRAVERSABLE
WIRED_FAIL -> WIRED_FAIL | WIRED_TRAVERSABLE
WIRED_TRAVERSABLE -> WIRED_FAIL | WIRED_TRAVERSABLE | PASSING
PASSING -> PASSING | WIRED_TRAVERSABLE | WIRED_FAIL
~~~

NOT_APPLICABLE never enters this state relation. No check result directly
rewrites current_state.

## 6. Pure helper module contract

The module src/planning_lite/traversability.py will be standard-library-only and
will not import filesystem, Git, subprocess, YAML, CLI, routing, telemetry,
runtime, or persistence facilities.

The implementation will use immutable, validated dataclasses in the style of
the existing pure contract modules. The plan binds these names so the focused
tests and later consumers have one stable seam:

~~~text
class TraversabilityError(ValueError)

JOURNEY_STATES = (
  "NOT_DEFINED",
  "DEFINED",
  "WIRED_FAIL",
  "WIRED_TRAVERSABLE",
  "PASSING",
)

GAP_CLASSES = (
  "IMPLEMENTATION_GAP",
  "WIRING_GAP",
  "ORCHESTRATION_GAP",
  "EVIDENCE_GAP",
)

APPLICABILITY_VALUES = ("REQUIRED", "NOT_APPLICABLE")
PLACEHOLDER_VALUES = ("NONE", "NOT_IMPLEMENTED", "FIXTURE_ONLY")
SEAM_DISPOSITIONS = ("PASS", "FAIL", "DOWNSTREAM_UNREACHABLE", "UNOBSERVED")
CHECK_DISPOSITIONS = (
  "PASS",
  "WIRED_FAIL",
  "BLOCKED_BY_ENVIRONMENT",
  "BLOCKED_BY_MISSING_PROBE",
  "NOT_APPLICABLE",
)
~~~

The exact V1 input/result types are:

~~~text
@dataclass(frozen=True, slots=True)
class SeamObservationV1:
    seam_ref: str
    producer_ref: str
    consumer_ref: str
    status: "PASS" | "FAIL"
    causal_reason: str | None
    reachable: bool
    activated: bool
    identity_continuous: bool
    contract_compatible: bool
    gap_class: str | None
    activation_qualifier: bool

@dataclass(frozen=True, slots=True)
class CriticalJourneyProjectionV1:
    journey_id: str
    applicability: "REQUIRED" | "NOT_APPLICABLE"
    current_state: str
    ordered_seams: tuple[SeamObservationV1, ...]
    placeholder_policy: "NONE" | "NOT_IMPLEMENTED" | "FIXTURE_ONLY"
    real_behavior_present: bool
    traversal_probe_admissible: bool
    evidence_admissible: bool
    observation_block: "NONE" | "BLOCKED_BY_ENVIRONMENT" | "BLOCKED_BY_MISSING_PROBE"

@dataclass(frozen=True, slots=True)
class SeamResultV1:
    seam_ref: str
    disposition: "PASS" | "FAIL" | "DOWNSTREAM_UNREACHABLE" | "UNOBSERVED"
    causal_reason: str | None

@dataclass(frozen=True, slots=True)
class JourneySmokeResultV1:
    journey_id: str
    applicability: str
    observed_traversability_state: str | None
    seams: tuple[SeamResultV1, ...]
    first_broken_seam: str | None
    gap_class: str | None
    activation_qualifier: bool
    check_disposition: str

@dataclass(frozen=True, slots=True)
class SystemTraversabilityResultV1:
    required_journey_ids: tuple[str, ...]
    journey_results: tuple[JourneySmokeResultV1, ...]
    check_disposition: str
~~~

The only bounded public behavior symbols are:

~~~text
check_critical_journey_smoke(
    journey: CriticalJourneyProjectionV1,
) -> JourneySmokeResultV1

check_system_traversability(
    observations: Sequence[JourneySmokeResultV1],
) -> SystemTraversabilityResultV1
~~~

The helper may expose the immutable input/result types and the validation
exception as support types. It must not add a third workflow/evaluation
subsystem or a persistence API.

### 6.1 Per-journey decision order

The helper validates normalized identifiers, unique ordered seam references,
allowed values, and boolean facts. Malformed or contradictory supplied facts
raise TraversabilityError; the test harness classifies that as
TEST_HARNESS_FAILURE. The helper never repairs malformed input.

For a valid journey:

1. NOT_APPLICABLE returns check disposition NOT_APPLICABLE and no durable
   journey state. It does not become a sixth state and does not authorize the
   per-Change bypass.
2. The first ordered causal seam failure is FIRST_BROKEN_SEAM. A seam is PASS
   only when its supplied status and required reachability, activation,
   identity-continuity, and contract-compatibility facts all support the
   declared handoff.
3. Every later seam dependent on the first failure is
   DOWNSTREAM_UNREACHABLE; it is not reclassified as PASS and cannot replace
   the first cause.
4. The first broken seam carries exactly one primary Gap class. The class
   precedence is ORCHESTRATION_GAP for missing runtime lifetime or identity
   carrier, WIRING_GAP for absent/incompatible/inactive handoff or Activation,
   IMPLEMENTATION_GAP for missing node behavior on an existing path, and
   EVIDENCE_GAP only when no behavioral, wiring, or orchestration failure is
   established.
5. Activation is represented by activation_qualifier=True with
   gap_class=WIRING_GAP; it never creates a fifth Gap class.
6. A causal failure takes precedence over a later environment or probe block and
   retains WIRED_FAIL plus downstream-unreachable seams.
7. With no causal failure, BLOCKED_BY_ENVIRONMENT returns an unchanged snapshot
   of supplied current_state and never promotes or regresses durable state.
8. With no causal failure, BLOCKED_BY_MISSING_PROBE returns an unchanged
   snapshot; it may report EVIDENCE_GAP only where no behavior, wiring, or
   orchestration failure was established.
9. With all required seams passing and an admissible traversal probe, an honest
   NOT_IMPLEMENTED or FIXTURE_ONLY placeholder yields WIRED_TRAVERSABLE, never
   PASSING.
10. PASSING requires all required seams passing, real_behavior_present=True, and
    evidence_admissible=True.
11. A check disposition PASS describes the supplied observation only. It never
    mutates the input projection or carrier, never promotes current_state, and
    never authorizes a result, route, next gate, release, or Change 2.

### 6.2 Aggregate decision order

check_system_traversability receives only derived per-journey observations. It
does not discover carrier records or scan a repository.

The aggregate required set is every observation with applicability REQUIRED:

1. empty required set -> NOT_APPLICABLE;
2. every required journey check disposition PASS -> PASS;
3. any required journey WIRED_FAIL -> WIRED_FAIL;
4. otherwise any BLOCKED_BY_ENVIRONMENT -> BLOCKED_BY_ENVIRONMENT;
5. otherwise any BLOCKED_BY_MISSING_PROBE -> BLOCKED_BY_MISSING_PROBE.

The aggregate remains non-green except for PASS and an empty required set.
Per-journey results remain the observations for their own reconciliation.
Aggregate PASS never means every durable journey state is PASSING.

## 7. State update and authority boundary

The implementation will document and test this one-way boundary:

~~~text
declared carrier facts + supplied seam/probe/evidence facts
    -> pure derived observation
    -> governed lifecycle / Project Spine reconciliation
    -> accepted evidence
    -> durable CRITICAL_JOURNEYS.md current_state update
~~~

No helper receives a filesystem path, Project Spine writer, router, runtime
owner, next-gate callback, or evidence-authority callback. No helper writes or
returns an authorization decision. The reconciliation procedure is described
in the control surfaces but is not implemented as a new persistence subsystem
in this Change.

The carrier's latest-observation pointer may be updated only by the existing
governed reconciliation owner after admissible evidence acceptance. A blocked
or invalid observation leaves the durable state unchanged.

## 8. Small-change bypass realization

The control surfaces will make the distinction explicit in the existing generic
Change records. The controlled block is bound as follows:

~~~text
AFFECTED_CRITICAL_JOURNEYS: NONE
affected-surface check: PASS
SYSTEM_PROOF_NOT_APPLICABLE_REASON: <explicit, evidence-backed reason>
AFFECTED_JOURNEY_SURFACE_CHECK: PASS
~~~

This is a per-Change proof disposition, not a carrier applicability decision.
The bypass is legal only when the Change cannot modify or semantically affect
entry, required node behavior, required seam, Activation, operation identity,
runtime lifetime, placeholder semantics, terminal semantics, evidence/probe
channel, or journey-state authority.

A Change that may affect any listed surface must declare the affected journey
and provide local proof plus the cheapest adequate system traversability
non-regression. No global runtime smoke is imposed on genuinely unrelated
local work. The validator itself does not decide whether a Change is affected;
the controlling Change Definition/Planning workflow records the evidence-backed
disposition in `proposal.md::## Scope`, `proposal.md::## Constraints`,
`specification.md::## Interfaces and contracts`, and
`specification.md::## Acceptance criteria`; Planning repeats the exact
disposition in `plan.md::## Verification strategy and seams` and Readiness
consumes it from `readiness.md::## Traceability, blocking edges, and
verification`. The bypass must name the exact affected-surface inspection and
its evidence reference; absence of a listed field is a failed bypass, not an
implicit N/A.

## 9. Self-hosted expected-red regression

The first fixture in tests/test_system_traversability.py is:

~~~text
PL_SELF_HOSTED_GOVERNED_OPERATION
EXPECTED STATE: WIRED_FAIL
FIRST_BROKEN_SEAM: OperationGuidance -> Governed Operation Lifecycle
GAP: ORCHESTRATION_GAP
REASON: NO_LEGITIMATE_RUNTIME_LIFETIME_OWNER
~~~

The declared ordered path is:

~~~text
Attempt
 -> OperationGuidance
 -> Governed Operation Lifecycle
 -> Execution
 -> validated RunReceipt
 -> PL08 Result/Evidence
 -> authoritative Next Gate
~~~

The fixture binds the following existing symbols and no substitutes:

| Contract role | Exact read-only symbol | Fixture use | Deliberate boundary |
|---|---|---|---|
| Attempt identity | `src/planning_lite/attempt_evaluation.py::AttemptRecordV1` | construct the declared Attempt input | no same-Attempt receipt is fabricated |
| Attempt ordinal | `src/planning_lite/attempt_evaluation.py::allocate_attempt_ordinal` | allocate the fixture ordinal before dispatch | no runtime lifecycle is started |
| Operation guidance | `src/planning_lite/execution_guidance.py::OperationGuidanceV1` and `select_operation_guidance` | produce the real guidance result from a valid resume mapping | no route or authority is returned |
| Receipt contract | `src/planning_lite/telemetry.py::validate_receipt` | bind the downstream validation contract by symbol identity | not invoked with a fabricated receipt; `append_receipt` and `collect_receipt` are not called |
| Result/evidence contract | `src/planning_lite/attempt_evaluation.py::ObservedResultV1`, `VerifierEvidenceV1`, `TechnicalEvaluationV1`, and `evaluate_technical` | bind the PL08 downstream contract by symbol identity | none is constructed or invoked because the first lifecycle seam is absent |
| Resume/next gate | `scripts/maintainer_resume.py::CURRENT_REL`, `REQUIRED_KEYS`, `parse_resume_block`, `load_resume`, and `next_permitted_action` | validate the declared resume/next-gate contract identity in a read-only fixture block | central `CURRENT.md` is not written and no next gate is selected |

The exact test is
`tests/test_system_traversability.py::test_self_hosted_governed_operation_pre_correction`.
It constructs only the real Attempt/guidance inputs, verifies the guidance
shape, records the absent `OperationGuidance -> Governed Operation Lifecycle`
seam, and expects the exact semantic red. The fixture does not invoke a runtime
pump, execute work, fabricate a same-Attempt receipt, fabricate result
continuity, fabricate next-gate continuity, or write any project state. It
honestly stops at the absent runtime-lifetime seam. Later Execution, RunReceipt,
Result/Evidence, and Next Gate seams are `DOWNSTREAM_UNREACHABLE`, not fake PASS
observations. `parse_resume_block` may inspect only the fixture text; it must
not call `load_resume` against the dirty central checkout.

The test harness must classify outcomes into:

~~~text
EXPECTED_SEMANTIC_RED
TEST_HARNESS_FAILURE
ENVIRONMENT_FAILURE
MISSING_PROBE
UNEXPECTED_DIFFERENT_RED
~~~

Only EXPECTED_SEMANTIC_RED satisfies the regression contract. A different first
broken seam, state, Gap, reason, or downstream pattern is a STOP, not a fixture
repair opportunity.

## 10. Control-surface edits

The implementation Plan binds these exact edits and does not create new
workflow files.

### 10.1 ROADMAP.md

Modify existing sections only:

- In 4.7 Small changes stay small, add that a materially affected journey
  requires the cheapest adequate system proof while genuinely unrelated work
  retains the evidence-backed bypass.
- In 7.7 Target Skeleton, distinguish the local Capability Walking Skeleton
  from the System Walking Skeleton. Preserve honest placeholders and
  placeholder != success.
- In 7.8 Executable Target Contract, state that the CriticalJourney carrier's
  five-state model is the system-journey state authority and is distinct from
  local Target Scenario shorthand; do not add a sixth state or replace the
  existing Target contract.
- In 12.5 Project Spine integrity / orphan check, add deterministic structural
  signals for an applicable journey lacking a carrier record, DEFINED contract,
  entry, ordered seam path, runtime-lifetime owner decision, evidence channel,
  Gap linkage, or Roadmap lineage. Keep semantic Doctor behavior out of scope.
- Preserve the macro PL05 -> PL06 -> PL07 -> PL08 -> PL09 sequence and do not
  mint a new Roadmap outcome, stage, vertebra, or major PL09 slice.

### 10.2 Project Spine and direction controls

- `STATE_OWNERSHIP.md::# State ownership`, immediately after the exact table
  row `| project documents | current durable facts, not session history |`,
  adds the `project/CRITICAL_JOURNEYS.md` row as the sole owner of journey
  identity, applicability, current state, and latest-observation pointer.
  `STATE_OWNERSHIP.md::## Duplication rules`, after the existing final bullet,
  adds that runtime history, derived validation, and evidence remain in their
  existing owners and cannot become a second journey authority.
- `TARGET_BASELINE_CALIBRATION.md::## Allowed write scope`, after the existing
  allowed-write list, adds the project-owned CriticalJourney carrier.
  `TARGET_BASELINE_CALIBRATION.md::## Procedure`, immediately after item 9 and
  before current item 10, adds the explicit APPLICABLE/NOT_APPLICABLE decision,
  reason, REQUIRED record, DEFINED prerequisite, initial System Walking
  Skeleton handoff, and initial evidence-channel output. It does not derive
  current satisfaction or Gaps.
- `CAUSAL_GAP_DERIVATION.md::## Gap definition`, after the existing Gap ID
  rule, adds the four fixed traversability classes and Activation qualifier.
  `CAUSAL_GAP_DERIVATION.md::## Gap record contract`, after the existing field
  list, adds journey refs, FIRST_BROKEN_SEAM, DOWNSTREAM_UNREACHABLE, and
  journey-linked closure evidence. `CAUSAL_GAP_DERIVATION.md::## Hard checks`,
  after `CHK-GAP-010`, adds first-cause, Activation, and no-parallel-registry
  checks.
- `ROADMAP_SYNTHESIS_PRIORITIZATION.md::## RoadmapOutcome synthesis`, after
  the existing candidate-field list, adds CriticalJourney lineage, System
  Walking Skeleton/placeholder obligation, and unresolved no-path visibility.
  `ROADMAP_SYNTHESIS_PRIORITIZATION.md::## Bounded-Change handoff`, after the
  existing handoff fields, adds the exact journey refs and downstream Change
  proof handoff while preserving RoadmapOutcome/Gap/Change separation.

### 10.3 Change controls

- `CHANGE_DEFINITION.md::## Procedure`: immediately after item 8 and before
  current item 9, require the controlled fields
  `AFFECTED_CRITICAL_JOURNEYS`, `EXPECTED_JOURNEY_STATE_DELTA`,
  `SYSTEM_PROOF_REQUIRED`, `SYSTEM_PROOF_NOT_APPLICABLE_REASON`,
  `AFFECTED_JOURNEY_SURFACE_CHECK`, and material `FIRST_BROKEN_SEAM`.
  `CHANGE_DEFINITION.md::## Approval`, immediately after the existing approval
  sentence, requires the same `proposal.md::## Scope` journey block to be
  consumed by Planning without reinterpretation.
- `CHANGE_PLANNING.md::## Minimum context`: append exact reads of the carrier,
  Definition journey block, Specification contract block, and applicable
  bypass evidence. `CHANGE_PLANNING.md::## Procedure`, immediately after item 4
  and before item 5, binds journey IDs, ordered seams, expected state delta,
  task/proof IDs, and the architecture-STOP output; a missing carrier or
  unbound material choice stops Planning.
- `CHANGE_READINESS.md::## Pass 2: engineering readiness`, immediately after
  its final existing bullet and before “Record evidence…”, adds an exhaustive
  per-journey check for carrier encoding, state relation, first broken seam,
  downstream-unreachable results, blocked precedence, placeholders, no false
  PASSING promotion, bypass proof, and no authority transfer.
  `### Shared Contract Closure` and `### Determinacy` consume the same
  exact serialization and carrier/proof fields. Readiness PASS remains distinct
  from execution authorization.
- `CHANGE_EXECUTION.md::## Procedure`, immediately after item 4 and before
  item 5, requires the approved Execution Envelope to carry journey IDs,
  expected proof, observation references, and reconciliation boundary.
  `### Execution Envelope`, immediately after the existing code block, adds
  `FIRST_BROKEN_SEAM`, `GAP_CLASS`, `DOWNSTREAM_UNREACHABLE`, and evidence
  disposition fields. Direct validator-to-carrier mutation, runtime-pump work,
  and authority absorption are forbidden.
- `CHANGE_CLOSURE.md::## Completion review`, immediately after item 5 and
  before item 6, requires comparison of observed versus durable state and
  fail-closed handling of missing or blocked evidence. `## Roadmap / Gap
  contribution`, immediately after the existing paragraph, records the latest
  observation and final disposition separately from Gap/Roadmap reconciliation.
- `DELIVERY_SLICES.md::## Decomposition rules`, immediately after the
  expand-contract paragraph, defines the System Walking Skeleton tracer bullet;
  `## Completion criterion` requires each journey-affecting task to name its
  verification seam, blocking edge, blast radius, recovery boundary, and
  stable task/proof IDs.

### 10.4 Exact generic Change-record carriers

The following are controlled subheadings/blocks in the existing generic
consumer records under an active Change. They are not new templates, schemas,
or owners. The Plan must write and later stages must read the same fields at
these exact anchors:

| Existing record and anchor | Controlled carrier block | Written by | Read by |
|---|---|---|---|
| `proposal.md::## Scope` | `Critical Journey Scope`: `AFFECTED_CRITICAL_JOURNEYS`, `SYSTEM_PROOF_REQUIRED`, `SYSTEM_PROOF_NOT_APPLICABLE_REASON`, `AFFECTED_JOURNEY_SURFACE_CHECK` | Definition | Planning, Readiness |
| `proposal.md::## Constraints` | authority/bypass failure-close rule and `EXPECTED_JOURNEY_STATE_DELTA` | Definition | Planning |
| `specification.md::## Interfaces and contracts` | `Critical Journey Contract`: journey IDs, ordered nodes/seams, identity/lifetime/evidence obligations, `FIRST_BROKEN_SEAM` when known | Definition | Planning, Readiness |
| `specification.md::## Acceptance criteria` | stable `AC-01`…`AC-16` rows for journey proof, bypass, state, authority, and integrity | Definition | Readiness, Closure |
| `plan.md::## Affected paths and symbols` | exact carrier paths, record anchors, source/test symbols, and seam bindings | Planning | Readiness, Execution |
| `plan.md::## Contracts and state transitions` | expected state delta, five-state relation, `NOT_APPLICABLE` sentinel rule, and reconciliation boundary | Planning | Readiness, Execution |
| `plan.md::## Verification strategy and seams` | `T-*` task IDs, `V-*` verification IDs, local/system proof, bypass evidence, and expected-red result identity | Planning | Readiness, Execution |
| `context.md::## Execution Envelope` | authorized journey tasks, allowed/forbidden surface, owned responsibility, evidence channel, next action | Execution context | Execution |
| `readiness.md::## Traceability, blocking edges, and verification` | AC/T/V mapping, carrier/proof completeness, finding refs, and blocking edge | Readiness | Execution, Closure |
| `readiness.md::### Determinacy` | exact serialization, symbol, anchor, expected-result, and failure-meaning closure | Readiness | Execution, Closure |
| `progress.md::## YYYY-MM-DD` | `Critical Journey Observation`: observation ref, first broken seam, Gap class, downstream list, probe/evidence refs, disposition, and durable-state reconciliation status | Execution | Closure |
| `progress.md::## Governed Attempt / Evaluation evidence` | exact Attempt/ObservedResult/VerifierEvidence/TechnicalEvaluation refs when genuinely available; otherwise explicit `NOT_REACHED` | Execution | Closure |
| `review.md::## Pass 1: specification conformance` | final per-journey observed state and evidence disposition | Closure | Owner |
| `review.md::## Pass 2: standards conformance` | no-authority-transfer, no-persistence, no-pump, and write-boundary result | Closure | Owner |
| `review.md::## Roadmap / Gap contribution` | latest observation ref, Gap class/refs, Roadmap refs, and independent disposition | Closure | Owner |

The generic record anchors are sufficient for this Change; no
`template/.planning/changes/templates/*` path is modified and no second policy
system is introduced.

## 11. Implementation sequencing

Use an early vertical flow with no horizontal "write all models first" phase.

### Slice 1 - carrier and direction/control semantics

Modify the 11 semantic markdown surfaces and add both CriticalJourneys files.
Establish field ownership, applicability, five states, four Gap classes,
local/system proof, early System Walking Skeleton, lifecycle obligations, and
STOP boundaries. Do not change source code or runtime behavior in this slice.

Verification seam:
exact path inventory, ownership/skip behavior, markdown field presence, and
template manifest/checksum regeneration.

### Slice 2 - pure validator

Add src/planning_lite/traversability.py with the exact V1 contracts and the two
helpers. Keep all inputs caller-supplied and all outputs immutable. Do not add
CLI, persistence, repository scanning, routing, or runtime integration.

Verification seam:
focused unit tests for validation, state derivation, first-cause localization,
blocked precedence, aggregate precedence, and input immutability.

### Slice 3 - self-hosted expected-red

Add `tests/test_system_traversability.py::test_self_hosted_governed_operation_pre_correction`
using `AttemptRecordV1`, `allocate_attempt_ordinal`, `OperationGuidanceV1`,
`select_operation_guidance`, the declared telemetry `validate_receipt` shape,
the `ObservedResultV1`/`VerifierEvidenceV1`/`TechnicalEvaluationV1` contract
symbols, and the read-only `parse_resume_block`/`next_permitted_action`
contract. Assert the exact expected semantic red and downstream-unreachable
pattern. Do not construct a fake runtime result, receipt, evaluation, or next
gate.

Verification seam:
one test returns EXPECTED_SEMANTIC_RED; all harness/environment/missing-probe/
different-red outcomes fail the test and require STOP.

### Slice 4 - generic lifecycle/control projections

Complete workflow wording and any required projection fields in the existing
generic control surfaces. Keep Project Spine reconciliation as the only durable
state-update owner. Do not modify Change record templates unless a later
empirical contract proves a generic projection is necessary; current planning
finds none.

Verification seam:
contract-control tests and review of no-authority-transfer/no-new-router/no-new-
lifecycle constraints.

### Slice 5 - focused and integrity verification

Run the focused system-traversability tests, exact template-manifest/checksum
tests, relevant existing direction/control/template suites, and then the full
suite at the implementation completion gate. Verify no false durable promotion,
no validator mutation, no source/template ownership breach, and no runtime pump.

## 12. Focused test and evaluation strategy

Create tests/test_system_traversability.py with these contractual groups. Test
names may be implementation-local, but every listed behavior must have one
focused assertion or a justified reused owner test.

### 12.1 Applicability and carrier distinction

- required applicability creates/accepts a declared CriticalJourney projection;
- NOT_APPLICABLE produces NOT_APPLICABLE check disposition and no journey state;
- carrier REQUIRED versus per-Change proof N/A remains distinct;
- evidence-backed unaffected Change bypass is accepted only with
  AFFECTED_CRITICAL_JOURNEYS = NONE and a passing affected-surface check;
- an affected entry/node/seam/Activation/identity/lifetime/placeholder/terminal/
  evidence/state-authority surface cannot use that bypass.

### 12.2 State, seam, and Gap behavior

- only the five canonical journey states are accepted;
- DEFINED, WIRED_FAIL, WIRED_TRAVERSABLE, and PASSING observations are derived
  under their exact predicates;
- FIRST_BROKEN_SEAM identifies the first ordered causal failure;
- dependent later seams become DOWNSTREAM_UNREACHABLE;
- WIRING_GAP, ORCHESTRATION_GAP, IMPLEMENTATION_GAP, and EVIDENCE_GAP are
  classified with one primary first-cause class;
- Activation is a WIRING_GAP qualifier, never a fifth class;
- an honest NOT_IMPLEMENTED placeholder yields WIRED_TRAVERSABLE;
- a placeholder cannot yield PASSING;
- real behavior plus admissible evidence yields PASSING;
- PASSING regresses to WIRED_TRAVERSABLE or WIRED_FAIL when supplied facts
  regress.

### 12.3 Blockers, purity, and authority

- blocked environment does not promote or regress durable state;
- missing probe does not promote durable state and reports evidence blocking
  only under the frozen precedence;
- a causal fail takes precedence over a later probe/environment block;
- the validator does not mutate a carrier or input projection;
- local capability PASS cannot override journey WIRED_FAIL;
- aggregate results obey empty-required/PASS/WIRED_FAIL/environment/probe order;
- the module has no filesystem, Git, subprocess, YAML, routing, persistence,
  or execution dependency;
- no result contains authority to write state, select a route, promote a gate,
  or own runtime lifetime;
- no persistent state/registry/database/scheduler is introduced.

### 12.4 Self-hosted and non-goal regression

- exact PL_SELF_HOSTED_GOVERNED_OPERATION expected semantic red;
- exact first broken seam, Gap, reason, and downstream-unreachable seams;
- harness failure, environment failure, missing probe, and different red are
  distinct failures;
- no runtime pump implementation is present or invoked;
- no authority transfer occurs to PL08, PL09, the validator, or the carrier.

Existing owner tests remain the owners for Attempt/evaluation, Operation Guidance,
RunReceipt, manifest/checksum integrity, template source/update behavior, and
central resume safety; the new test file must not duplicate those invariants.

## 13. Compatibility and integrity projections

- Python target remains >=3.11 and the helper uses standard library only.
- No dependency, CLI, package init, telemetry, context, workspace, or existing
  runtime module changes are planned.
- Existing OperationGuidance, Attempt/evaluation, RunReceipt, and resume
  contracts are read-only inputs to the expected-red fixture.
- Adding template/.planning/project/CRITICAL_JOURNEYS.md remains safe because
  copier.yml already skips .planning/project/** and OWNERSHIP.yml already marks
  project/** as project-owned.
- Adding the pristine template source is managed framework content and must be
  reflected in MANIFEST_V4.md and SHA256SUMS.txt.
- All template hashes use canonical LF bytes, matching existing manifest tests.
- No consumer project is edited and no consumer active Change directory is
  created.
- Existing generic Change stage records are the carriers: the exact
  `proposal.md`, `specification.md`, `plan.md`, `readiness.md`, `context.md`,
  `progress.md`, and `review.md` anchors listed in Section 10.4 are populated
  by workflow guidance. No `template/.planning/changes/templates/*` path is
  modified, and no new Change-record schema or policy subsystem is introduced.
- No runtime carrier history or scheduler storage is added.

## 14. Plan-time architecture STOP contract

This planning pass currently reports:

~~~text
PLAN_ARCHITECTURE_STOP: NO
UNBOUND_ARCHITECTURE_CHOICES: 0
UNBOUND_IMPLEMENTATION_CHOICES: 0
~~~

The following are ordinary non-material implementation choices still allowed
inside the frozen contract: exact dataclass normalization, helper-private
validation layout, test fixture organization, file order, manifest
regeneration, and checksum mechanics. Carrier serialization, generic Change
record anchors, lifecycle insertion points, downstream symbols, task/proof
identity, and failure meanings are frozen below and are not implementation
choices.

STOP before treating the Plan as complete if repository evidence requires any
material decision outside the Definition, including:

- a second CriticalJourney authority;
- moving current journey state out of the singular Project Spine carrier;
- a parallel Gap registry or changed four-class taxonomy;
- validator persistence, repository-discovery authority, route selection, or
  runtime execution;
- validator-driven carrier mutation;
- PL08 runtime orchestration or PL09 route/result/next-gate/evidence authority;
- a persistent runtime workflow registry or new orchestration subsystem;
- a new Roadmap vertebra or major PL09 slice consumption;
- an independently governed Change split;
- a changed five-state model or applicability trigger;
- a weakened affected-surface bypass;
- inability to reproduce the honest expected semantic red;
- material redesign of the Governed Operation Lifecycle prerequisite;
- semantic redesign of Change 2; or
- any new material architecture choice not decided by the canonical Definition.

Required STOP output:

~~~text
PLAN_ARCHITECTURE_STOP: YES
BLOCKING_FACT: <exact repository fact>
CONTRADICTED_DEFINITION_RULE: <exact frozen rule>
ARCHITECTURE_CHOICE_REQUIRED: <exact unresolved choice>
IMPLEMENTATION_AUTHORIZATION: NO
NEXT_GATE: OWNER_ADJUDICATION_PL_SYSTEM_TRAVERSABILITY_PLAN_ARCHITECTURE_BLOCKER
~~~

No such STOP is silently resolved in this Plan.

## 15. Verification commands

The implementation turn, after separate implementation authorization, must use the
smallest sufficient evidence stack in this order.

### 15.1 Focused checks

~~~text
uv run pytest tests/test_system_traversability.py
uv run pytest tests/test_direction_foundation.py tests/test_current_capability_gap_foundation.py tests/test_roadmap_synthesis_handoff.py tests/test_field_control_pack_foundation.py tests/test_project_shaping_foundation.py tests/test_template.py tests/test_template_source.py
~~~

The focused output must show the exact five-state model, four Gap classes,
carrier ownership, expected-red facts, no mutation, no authority transfer, and
template integrity.

### 15.2 Broader checks

~~~text
uv sync
uv run pytest
git diff --check
git status --short --untracked-files=all
~~~

Adjudicate any custom-verifier failure as product defect versus verifier defect
before changing implementation.

### 15.3 Clean consumer/update evidence

At the meaningful integration gate:

1. adopt the template into a temporary clean Git repository;
2. run planning-lite doctor there;
3. verify the two CriticalJourneys files seed correctly;
4. verify an existing project-owned .planning/project/CRITICAL_JOURNEYS.md is
   preserved on update;
5. when update behavior changed, test an update between two committed central
   Git tags and verify project-owned files remain unchanged;
6. run the consumer smoke from clean committed central source identity.

No consumer update evidence is claimed by this Plan.

## 16. Acceptance-to-evidence mapping

Stable implementation task identity:

| Task ID | Bounded outcome | Primary surface | Blocking edge |
|---|---|---|---|
| T-01 | deterministic CriticalJourney carrier serialization and singular ownership | `template/.planning/project/CRITICAL_JOURNEYS.md`, pristine source, `STATE_OWNERSHIP.md` | carrier shape must be exact before validation |
| T-02 | applicability, `NOT_APPLICABLE` separation, Gap/Activation and bypass controls | Target calibration, causal Gap, Change Definition/Planning controls | affected/unaffected disposition must be explicit |
| T-03 | pure V1 validator and five-state/aggregate derivation | `src/planning_lite/traversability.py` | no persistence, authority, or filesystem dependency |
| T-04 | focused validator, carrier, immutability, blocked-precedence, and bypass tests | `tests/test_system_traversability.py` | test failures stop dependent slices |
| T-05 | exact self-hosted expected-red fixture using real existing symbols | `tests/test_system_traversability.py::test_self_hosted_governed_operation_pre_correction` | exact first seam/reason/downstream tuple must match |
| T-06 | exact lifecycle section bindings and generic Change-record carrier projections | existing control surfaces and active Change records | no template/schema or second policy system |
| T-07 | early System Walking Skeleton and delivery-slice/task identity | ROADMAP, DELIVERY_SLICES, Plan task graph | no horizontal implementation phase or new Roadmap vertebra |
| T-08 | manifest/checksum and relevant existing owner regression coverage | `MANIFEST_V4.md`, `SHA256SUMS.txt`, existing owner tests | project-owned files and source boundaries remain intact |
| T-09 | final evidence reconciliation and write-boundary proof | readiness/progress/review records | no Formal Readiness or implementation authorization is inferred |

Stable verification identity:

| Verification ID | Proof / inspection |
|---|---|
| V-01 | exact carrier serialization, field order, uniqueness, ownership, and pristine/project copy inspection |
| V-02 | applicability/state/Gap/Activation matrix and positive/negative bypass checks |
| V-03 | pure validator import boundary, input/carrier immutability, and no-authority result inspection |
| V-04 | exact self-hosted expected-red symbol binding and result tuple |
| V-05 | exact generic carrier anchors and lifecycle control-surface inspection |
| V-06 | affected proof required versus evidence-backed unaffected bypass, including negative cases |
| V-07 | manifest/checksum exact-tree and canonical-LF integrity |
| V-08 | `uv run pytest tests/test_system_traversability.py` |
| V-09 | relevant existing owner suites: `tests/test_direction_foundation.py`, `tests/test_current_capability_gap_foundation.py`, `tests/test_roadmap_synthesis_handoff.py`, `tests/test_field_control_pack_foundation.py`, `tests/test_project_shaping_foundation.py`, `tests/test_template.py`, `tests/test_template_source.py`, `tests/test_execution_guidance.py`, `tests/test_attempt_evaluation.py`, `tests/test_run_receipts.py`, and central resume-contract coverage |
| V-10 | later integration gate: `uv sync`, full `uv run pytest`, clean adoption/doctor, and tagged update smoke where in scope |
| V-11 | Git/write-boundary inspection: no consumer, CURRENT, staging, commit, push, authority transfer, or unrelated path mutation |

Every Definition acceptance criterion has one stable task, primary binding,
proof type, verification identity, evidence carrier, and failure meaning:

| AC_ID | Frozen requirement | Task | Primary path / symbol / anchor | Proof type | Verification | Expected result | Evidence carrier | Failure meaning |
|---|---|---|---|---|---|---|---|---|
| AC-01 | one durable carrier and current state per required journey | T-01 | carrier files + `STATE_OWNERSHIP.md` | structural inspection + focused test | V-01, V-08 | exact one-record/one-state shape | `readiness.md::Traceability`, `review.md::Pass 1` | carrier/ownership defect; STOP |
| AC-02 | explicit two-branch applicability with reason | T-02 | `TARGET_BASELINE_CALIBRATION.md`, carrier `applicability` | decision matrix | V-02 | REQUIRED or NOT_APPLICABLE is explicit and valid | `proposal.md::Scope`, `progress.md` | hidden applicability or missing reason; STOP |
| AC-03 | applicable Target acceptance requires DEFINED | T-02 | calibration output + `current_state` | workflow/control inspection | V-02, V-05 | downstream work is blocked before DEFINED | `readiness.md::Determinacy` | early implementation without DEFINED; readiness fail |
| AC-04 | first affected Change declares early System Walking Skeleton | T-07 | ROADMAP 7.7/7.8 + `DELIVERY_SLICES.md` | ordered task inspection | V-05 | early vertical-flow obligation is present | `plan.md::Dependency order`, `tasks.md` | horizontal or late-flow plan; STOP |
| AC-05 | state relation and Project Spine update boundary prevent false promotion/mutation | T-03 | `check_critical_journey_smoke`, `check_system_traversability` | immutability and blocked-state tests | V-03, V-08 | no direct write; blocked/invalid unchanged | `progress.md::Critical Journey Observation` | authority/mutation defect; STOP |
| AC-06 | V1 check fields, first cause, downstream unreachable, blocked and aggregate rules | T-03/T-04 | V1 dataclasses and helper outputs | exact result assertions | V-03, V-08 | exact disposition and seam result tuple | `readiness.md::Traceability`, `progress.md` | result-contract defect; STOP |
| AC-07 | four Gap classes and Activation qualifier remain in existing authority | T-02/T-03 | `CAUSAL_GAP_DERIVATION.md`, `GAP_CLASSES` | classification matrix | V-02, V-08 | one primary class; Activation only qualifier | `progress.md`, `review.md::Roadmap / Gap contribution` | taxonomy/authority drift; owner adjudication |
| AC-08 | placeholder traversable but never PASSING | T-03/T-04 | placeholder policy + state derivation | positive/negative behavior test | V-02, V-08 | placeholder gives WIRED_TRAVERSABLE only | `progress.md::Critical Journey Observation` | false success; STOP |
| AC-09 | local capability PASS cannot override journey WIRED_FAIL | T-02/T-04 | Change proof block + aggregate result | conflict test and control inspection | V-02, V-06 | affected journey remains non-green | `readiness.md`, `review.md::Pass 1` | local/system proof breach; STOP |
| AC-10 | affected journey gets system nonregression; unrelated work gets exact bypass | T-02/T-06 | `proposal.md::Scope`, `plan.md::Verification strategy and seams` | positive/negative evidence test | V-05, V-06 | only genuinely unaffected Change may bypass | `proposal.md`, `readiness.md` | unsafe bypass; readiness fail |
| AC-11 | PL08 evaluates smoke/evidence and is not runtime pump | T-05/T-06 | attempt/evaluation symbols + lifecycle anchors | symbol/import/control inspection | V-04, V-05, V-11 | no runtime pump or authority transfer | `progress.md::Governed Attempt / Evaluation evidence`, `review.md::Pass 2` | PL08 ownership drift; STOP |
| AC-12 | PL09 remains bounded and lacks route/result/next-gate/evidence authority | T-05/T-06 | resume/guidance bindings + control surfaces | expected-red and authority inspection | V-04, V-05, V-11 | exact seam stops before lifecycle authority | `review.md::Pass 2` | authority absorption; STOP |
| AC-13 | self-hosted pre-correction regression is exact expected semantic red | T-05 | `test_self_hosted_governed_operation_pre_correction` | executable expected-red result | V-04, V-08 | exact seam, Gap, reason, downstream list | `progress.md::Governed Attempt / Evaluation evidence` | any different red; STOP |
| AC-14 | Change 2 full non-circular resume conjunction is preserved | T-09 | preserved-state block + Change 2 records | text/Git boundary inspection | V-11 | no Change 2 mutation; conjunction unchanged | `readiness.md`, `review.md` | resume-integrity breach; STOP |
| AC-15 | no registry/database/scheduler/graph engine/duplicated lifecycle | T-03/T-06/T-08 | path inventory, imports, control surfaces | static/path inspection | V-03, V-05, V-07, V-11 | only 15 semantic + 2 mechanical paths | `plan.md::Affected paths and symbols`, `review.md::Pass 2` | architecture expansion; STOP |
| AC-16 | major gate, prerequisite, recommendations, and paused work preserved | T-09 | candidate preserved-state block | Git/write-boundary inspection | V-11 | all paused/gate states unchanged | `review.md::Final bookkeeping` | unrelated scope consumption; STOP |

For every row, a missing expected result, absent evidence carrier, or mismatched
verification identity is a material Plan defect rather than an implementation
detail. The mapping is consumed by Readiness and Closure; it does not authorize
implementation or Formal Readiness.

## 17. Evidence required for later Formal Readiness and execution authorization

Formal Readiness is not run or authorized by this Plan. It may be run only
after the separate owner authorization gate named in the terminal receipt.

The later readiness packet must include:

- the exact canonical Definition SHA256 and canonical Plan SHA256;
- approved Plan and any explicit amendments;
- final changed-path manifest with the 15 semantic paths and the two mechanical
  paths classified exactly as above;
- carrier schema and ownership evidence;
- pure helper API/result evidence;
- focused test output for every mandatory behavior;
- exact expected-red result classified EXPECTED_SEMANTIC_RED;
- evidence that no validator or check mutated CRITICAL_JOURNEYS.md;
- evidence that blocked/missing-probe/invalid observations did not promote state;
- evidence that local PASS cannot override journey WIRED_FAIL;
- evidence that no runtime pump, registry, scheduler, graph engine, new
  lifecycle, authority transfer, Change 2 amendment, or runtime-prerequisite
  implementation entered the diff;
- relevant existing regression-suite output;
- manifest/checksum integrity output;
- clean temporary adoption and planning-lite doctor output;
- clean tagged update smoke when template update behavior is in scope;
- Git/write-boundary evidence showing no CURRENT.md, consumer project, staging,
  commit, push, or release mutation by the planning or readiness operation.

Later execution authorization must remain a separate owner decision after
Formal Readiness = READY. Readiness PASS never authorizes implementation.

## 18. Preserved relationships and explicit non-goals

~~~text
CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001
BLOCKED / VALID / PAUSED
IMPLEMENTATION: NO

CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
SHAPED / PAUSED_BEFORE_EMPIRICAL_DISCOVERY

OWNER_ADJUDICATION_PL_V39_09_NEXT_SLICE_AFTER_09-B_CLOSURE
PRESERVED / UNCONSUMED

SAFE_FILE_MUTATION_HYGIENE
PRESERVED / SEPARATE
~~~

This Change does not implement or absorb the Governed Operation Lifecycle
prerequisite, Change 2, F01/F02/F03 operation tracing, runtime prompt
deduplication, recommendations, Roadmap reprioritization, Change 3, or the
major PL09 next slice.

Change 2 remains resumable only after the exact conjunction:

~~~text
SYSTEM_TRAVERSABILITY_CORRECTION_CLOSED
+ GOVERNED_OPERATION_LIFECYCLE_PREREQUISITE_CLOSED
+ PL_SELF_HOSTED_GOVERNED_OPERATION CRITICAL_JOURNEY_SMOKE = PASS
+ observed journey state = PASSING
+ CHANGE_2_AMENDMENT_INTEGRATION_UPDATE
+ FRESH_FORMAL_READINESS = READY
+ SEPARATE_IMPLEMENTATION_AUTHORIZATION
~~~

## 19. Rollback, failure, and stop handling

This canonical Plan has no product rollback because it writes no product path.
If a later governed review rejects or revises it, supersede only this
governance checkpoint through an explicitly authorized local mutation; do not
alter the canonical Definition or CURRENT.md as a repair shortcut.

During implementation, a failed focused test stops only the dependent slice
unless it demonstrates a shared Definition contradiction. A custom verifier
failure is adjudicated as product defect or verifier defect. A material
contract contradiction emits the exact Plan-time architecture STOP and routes
to owner adjudication; it is not hidden in a task or resolved by broadening
the path budget.

## 20. Terminal receipt

~~~text
PL_SYSTEM_TRAVERSABILITY_IMPLEMENTATION_PLAN_CANONICALIZATION

OVERALL: PLAN_APPROVED / FORMAL_READINESS_NOT_YET_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED

EXECUTOR: GPT-5.6_LUNA_EXTRA_HIGH

CANONICAL_DEFINITION:
docs/design/project-spine/checkpoints/PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-CHANGE-DEFINITION-v1.md

CANONICAL_DEFINITION_SHA256:
764E8D2702B964DD6F7B7C4A37289DB49271331A07270AE1BE9D99089C592820

DEFINITION_ACTIVATION_SHA256:
2953BFD736B72AC08525EE095CCE89958EF0EC3B8AB189F6A7CCCB447BC11805

DEFINITION_MANDATED_PATH_COUNT:
15

PLAN_RESOLVED_PROJECTION_PATH_COUNT:
0

MECHANICAL_INTEGRITY_PATH_COUNT:
2

PLAN_ADDITIONAL_PATH_COUNT:
2

TOTAL_PLANNED_PATH_COUNT:
17

PLAN_ARCHITECTURE_STOP:
NO

UNBOUND_ARCHITECTURE_CHOICES:
0

UNBOUND_IMPLEMENTATION_CHOICES:
0

MATERIAL_FINDING_COUNT_FROM_REVIEW:
5

MF-01:
CLOSED_BY_PLAN_CORRECTION

MF-02:
CLOSED_BY_PLAN_CORRECTION

MF-03:
CLOSED_BY_PLAN_CORRECTION

MF-04:
CLOSED_BY_PLAN_CORRECTION

MF-05:
CLOSED_BY_PLAN_CORRECTION

PLAN_CORRECTED:
YES

SELF_HOSTED_EXPECTED_RED_PLAN:
FROZEN

VALIDATOR_PLAN:
FROZEN

STATE_UPDATE_BOUNDARY:
FROZEN

SMALL_CHANGE_BYPASS:
FROZEN

NO_AUTHORITY_TRANSFER:
PASS

CHANGE_2:
BLOCKED / VALID / PAUSED

RUNTIME_PREREQUISITE:
SHAPED / PAUSED_BEFORE_EMPIRICAL_DISCOVERY

MAJOR_PL09_GATE:
PRESERVED / UNCONSUMED

IMPLEMENTATION_AUTHORIZED:
NO

FORMAL_READINESS_AUTHORIZED:
NO

APPROVED_SOURCE_PLAN_PATH:
.local/work/experiments/PL_SYSTEM_TRAVERSABILITY_IMPLEMENTATION_PLAN_CANDIDATE.md

APPROVED_SOURCE_PLAN_SHA256:
71FF99DDAB1C49D5183C30FE2724DC32E777AC5066E5D302A8FDEE1F9CA94B4B

TRACKED_PATHS_CHANGED:
0

STAGED_PATHS:
0

COMMIT:
NO

PUSH:
NO

NEXT_SINGLE_GATE:
OWNER_AUTHORIZATION_PL_SYSTEM_TRAVERSABILITY_FORMAL_READINESS

RESULT_DIGEST:
The canonical Plan materializes the approved source Plan with no semantic
delta and remains bound to the exact canonical Definition SHA256
764E8D2702B964DD6F7B7C4A37289DB49271331A07270AE1BE9D99089C592820.
The Plan freezes the 15 semantic paths and adds only two empirically required
mechanical manifest/checksum paths, for a total planned path count of 17.
The CriticalJourney carrier, pure validator, state-update boundary, bypass,
self-hosted expected red, early vertical flow, and all task/evidence bindings
remain fully bound.
No Plan-time architecture contradiction was found, so PLAN_ARCHITECTURE_STOP is
NO; any later contradiction must route to owner adjudication.
Formal Readiness is not run or authorized, implementation remains unauthorized,
Change 2 and the runtime prerequisite remain paused, CURRENT.md is unchanged,
and the major PL09 gate remains preserved and unconsumed.
The next single gate is OWNER_AUTHORIZATION_PL_SYSTEM_TRAVERSABILITY_FORMAL_READINESS.
~~~
