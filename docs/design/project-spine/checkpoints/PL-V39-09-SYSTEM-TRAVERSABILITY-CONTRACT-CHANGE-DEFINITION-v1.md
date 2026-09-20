# PL-V39-09 System Traversability Contract and Critical Journey Binding - Approved Definition v1

Status: APPROVED_BY_OWNER

This canonical Definition is the approved scope authority for
CHG-PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-001. It preserves the approved
semantics of the reviewed candidate. It does not authorize Planning,
implementation, runtime execution, staging, commit, release, or resumption of
paused work.

This corrected candidate supersedes the reviewed predecessor candidate with SHA-256
4836821DEB6D3C2B5D14CA80B148F9826CA2297446D31E5CD67B68041A438CCA. The
empirical binding and owner-approved shaping remain historical, nonauthoritative
inputs and are not modified by this correction.

## 1. Change identity

~~~text
DOCUMENT_ID: PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-DEFINITION-001
CHANGE_ID: CHG-PL-V39-09-SYSTEM-TRAVERSABILITY-CONTRACT-001
CHANGE_NAME: System Traversability Contract and Critical Journey Binding
CHANGE_KIND: CROSS_CUTTING_CORRECTIVE_CHANGE
STATUS: APPROVED_BY_OWNER
OWNER_APPROVAL: USER / EXPLICIT / current conversation
DEFINITION_DECISION: APPROVE
FINAL_FOCUSED_REVIEW: PASS
MATERIAL_FINDINGS: 0
DEFINITION_MANDATED_PATH_COUNT: 15
IMPLEMENTATION_AUTHORIZED: NO
PLANNING_AUTHORIZED: NO
SOURCE_CANDIDATE: .local/work/experiments/PL_SYSTEM_TRAVERSABILITY_CORRECTION_CHANGE_DEFINITION_CANDIDATE.md
SOURCE_CANDIDATE_SHA256: DCDBC579E9D88F0BB4049E254AF5D976D1D23A89F4D49F931D13328711418A43
BASELINE_HEAD: befa1780093335c99318526a3b3368c0f2a23ee0
CANONICALIZATION_SEMANTIC_DELTA: NONE
ACTIVATION: DEFINITION_APPROVED / PLANNING_NOT_YET_AUTHORIZED
NEXT_GATE: OWNER_AUTHORIZATION_PL_SYSTEM_TRAVERSABILITY_IMPLEMENTATION_PLANNING
~~~

## 2. Problem / empirical evidence

The repository has local capability and evaluation contracts but no durable
cross-Change carrier for an applicable multi-stage journey. Target Skeleton and
Executable Target Contract remain conditional in the canonical Roadmap; PL05
completed without a CriticalJourney obligation; PL07 owns local execution
guidance but not a system journey; PL08 evaluates evidence but does not own a
runtime pump; and PL09 has no current in-process operation consumer spanning
guidance, execution, receipt, result/evidence, and next gate.

The self-hosted path is therefore not a complete system claim:

~~~text
Attempt -> OperationGuidance -> Governed Operation Lifecycle -> Execution
-> validated RunReceipt -> PL08 Result/Evidence -> authoritative Next Gate
~~~

The exact pre-correction observation is WIRED_FAIL at
OperationGuidance -> Governed Operation Lifecycle, with ORCHESTRATION_GAP and
NO_LEGITIMATE_RUNTIME_LIFETIME_OWNER.

## 3. Root failure

~~~text
ROOT_FAILURE: UNGOVERNED_CRITICAL_JOURNEY_TRAVERSABILITY
~~~

A component or local capability can appear complete while the ordered system path
is absent, cannot be activated, loses identity, lacks a bounded runtime lifetime
owner, or cannot produce admissible evidence.

## 4. Goal

Introduce the smallest cross-cutting contract that makes required system
journeys explicit, durable, evaluable, and honest about broken seams while
preserving current authority boundaries. The Change establishes the carrier,
workflow obligations, pure check result, evidence linkage, and focused
regression cases. It does not implement the paused runtime pump.

## 5. Authority / lineage

Binding architecture and source evidence:

- SYSTEM_TRAVERSABILITY_CONTRACT_AS_CROSS_CUTTING_INVARIANT;
- .local/work/experiments/PL_SYSTEM_VITALITY_TRAVERSABILITY_SHAPING.md,
  SHA-256 68B9BF58DCC086F76BCFE7BA7613EFE5D15B5AA4D26F5045DAA737F27EF69D0C;
- .local/work/experiments/PL_SYSTEM_TRAVERSABILITY_CORRECTION_EMPIRICAL_BINDING.md,
  SHA-256 9A044E56B955459DDABEF520B54BBE27F25762D5843E319943C8D222BA954746;
- predecessor candidate SHA-256:
  4836821DEB6D3C2B5D14CA80B148F9826CA2297446D31E5CD67B68041A438CCA;
- current baseline HEAD:
  befa1780093335c99318526a3b3368c0f2a23ee0.

The correction is a partial cross-cutting contribution to the existing Project
Spine/PL09 direction, not a new Roadmap vertebra. It preserves the current
Project Spine, PL05, PL07, PL08, and PL09 ownership decisions.

## 6. System Traversability Contract

For each applicable materially multi-stage Target flow, the repository must
carry one durable CriticalJourney record with an authorized entry, ordered
nodes and seams, identity continuity, runtime-lifetime ownership or an honest
Gap, placeholder semantics, evidence channel, current state, Gap refs, and
Roadmap refs.

The check observes supplied facts. It does not select routes, execute work,
persist state, authorize a result, promote a next gate, or become the runtime
pump. The contract is cross-cutting, not a subsystem.

## 7. CriticalJourney contract

The durable carrier is:

~~~text
template/.planning/project/CRITICAL_JOURNEYS.md
~~~

with the pristine source copy at:

~~~text
template/.planning/templates/project/CRITICAL_JOURNEYS.md
~~~

Each record uses the minimum fields:

~~~text
journey_id
applicability
target_refs
roadmap_refs
entry_ref
ordered_nodes
ordered_seams
runtime_lifetime_owner_ref
identity_continuity_ref
placeholder_policy
terminal_semantics
evidence_channel_ref
current_state
gap_refs
last_observation_ref
~~~

Applicability and state are distinct. The carrier is project-owned and
human-reviewable. It is not a registry, database, graph, scheduler, append-only
runtime store, event/history store, or replacement for Target, Capability, Gap,
Roadmap, Change, or evidence authority. It stores one current state and one
latest-observation pointer; runtime history remains in Change, progress, review,
and evidence records.

## 8. Applicability rule

The applicability decision is explicit:

~~~text
APPLICABILITY_DECISION: APPLICABLE | NOT_APPLICABLE
~~~

An accepted Target outcome is APPLICABLE when either condition holds:

1. it requires two or more separately owned runtime capability nodes connected by
   material handoff seams; or
2. one operation identity or runtime lifetime crosses a process, persistence,
   host, authority, or lifecycle boundary where loss would invalidate the
   outcome.

APPLICABLE maps to a durable CriticalJourney record with:

~~~text
applicability: REQUIRED
current_state: NOT_DEFINED until the record is complete
~~~

NOT_APPLICABLE requires an explicit reason and means that the accepted Target
outcome has no material CriticalJourney surface under the two conditions above.
It is a carrier applicability decision, not a per-Change proof disposition and
not a canonical journey state.

Applicability is decided from accepted Target outcomes and key journeys during
Target Baseline Calibration. A materially affected Change cannot silently use
the unrelated-work bypass.

## 9. Journey states

The only canonical states are:

~~~text
NOT_DEFINED
DEFINED
WIRED_FAIL
WIRED_TRAVERSABLE
PASSING
~~~

Meanings:

- NOT_DEFINED means applicability is REQUIRED but the record or contract is
  absent or incomplete;
- DEFINED means identity, entry, ordered seams, evidence, ownership
  expectations, placeholder policy, and terminal semantics exist, but traversal
  is not yet proven;
- WIRED_FAIL means the declared path reaches a causally localized broken seam;
- WIRED_TRAVERSABLE means every required seam traverses with honest placeholder
  or fixture-only behavior where allowed;
- PASSING requires the required real behavior and admissible evidence in addition
  to traversal.

WIRED_TRAVERSABLE is not PASSING. A check disposition of PASS is an observation
of the supplied check predicates; it is not automatic promotion of the durable
journey state.

The durable state relation is:

~~~text
NOT_DEFINED -> DEFINED
DEFINED -> WIRED_FAIL | WIRED_TRAVERSABLE
WIRED_FAIL -> WIRED_FAIL | WIRED_TRAVERSABLE
WIRED_TRAVERSABLE -> WIRED_FAIL | WIRED_TRAVERSABLE | PASSING
PASSING -> PASSING | WIRED_TRAVERSABLE | WIRED_FAIL
~~~

A transition to PASSING is valid only after the same journey satisfies the
traversable-path predicate, required real behavior predicate, and admissible
evidence predicate. A placeholder cannot satisfy the real-behavior predicate.
A broken observation can regress a durable state, but no check result
automatically mutates the carrier.

A governed lifecycle or Project Spine reconciliation accepts the derived
observation and updates current_state. The pure validator never writes
CRITICAL_JOURNEYS.md. Environment blocks, missing-probe blocks, and invalid
fixtures do not promote a durable state.

## 10. Gap taxonomy

The existing CAUSAL_GAP_DERIVATION.md / GAP_MAP.md owner carries:

~~~text
IMPLEMENTATION_GAP
WIRING_GAP
ORCHESTRATION_GAP
EVIDENCE_GAP
~~~

Meanings:

- IMPLEMENTATION_GAP is absent required behavior or property when the relevant
  path and owner are present;
- WIRING_GAP is an absent, incompatible, unreachable, or inactive required
  producer-consumer seam or activation path;
- ORCHESTRATION_GAP is absent legitimate bounded runtime-lifetime ownership,
  identity-carrying pump, or required phase continuity;
- EVIDENCE_GAP is absent admissible evidence, probe, or identity proof when no
  behavioral, wiring, or orchestration failure has been established.

Activation is a qualifier/subclass of WIRING_GAP, not a fifth top-level class.
There is no parallel Gap registry.

For one ordered journey observation, choose one primary causal class for the
first broken seam:

1. ORCHESTRATION_GAP when the required runtime lifetime or identity carrier is
   the missing condition;
2. WIRING_GAP when the runtime lifetime is not the blocker and the named
   producer-consumer seam or activation is absent, incompatible, or inactive;
3. IMPLEMENTATION_GAP when the path and seam exist but required node behavior is
   absent;
4. EVIDENCE_GAP only when no behavior, seam, activation, or orchestration
   failure is established and admissible proof is missing.

DOWNSTREAM_UNREACHABLE is a seam observation, not a Gap class. Independent
secondary Gap references may be retained when separately evidenced, but they do
not replace the primary first-cause classification. A missing probe or
environment block is not converted into a behavioral Gap.

## 11. System Walking Skeleton contract

A Capability Walking Skeleton proves the smallest local capability path. A
System Walking Skeleton proves the minimum ordered path through all required
journey seams, including identity continuity, activation, runtime lifetime,
receipt/result handoff, and evidence boundary where applicable.

The first Change that materially affects an applicable journey must declare an
early System Walking Skeleton obligation. It may use NOT_IMPLEMENTED or
FIXTURE_ONLY placeholders to preserve traversal. A placeholder cannot produce
PASSING or claim production success.

## 12. Local vs system proof

For an affected journey:

~~~text
LOCAL_PROOF
+
CHEAPEST_ADEQUATE_SYSTEM_TRAVERSABILITY_NONREGRESSION
~~~

Local capability PASS never overrides a journey WIRED_FAIL.

An unrelated local Change may use the existing cheap bypass only when all of the
following are true:

~~~text
AFFECTED_CRITICAL_JOURNEYS: NONE
affected-surface check: PASS
SYSTEM_PROOF_NOT_APPLICABLE_REASON: explicit and evidence-backed
~~~

The affected-surface check must establish that the Change does not modify or
semantically affect any required journey entry, required node behavior, required
seam, activation path, operation identity, runtime lifetime ownership,
placeholder semantics, terminal semantics, evidence channel/probe, or
journey-state authority. If any listed surface may change, system proof is
required. The carrier applicability of an existing required journey remains
REQUIRED; only this Change's proof disposition is NOT_APPLICABLE.

This bypass does not require a global runtime smoke for genuinely unrelated
work, and it cannot be used to hide an affected journey.

## 13. Early vertical-flow rule

The correction binds this order without restructuring the macro Roadmap:

~~~text
accepted Target
 -> applicable CriticalJourneys DEFINED
 -> first affected implementation Change declares an early System Walking Skeleton
 -> before first material journey capability is claimed complete:
    minimum real path WIRED_TRAVERSABLE with honest placeholders if necessary
 -> subsequent Changes deepen behavior and preserve traversability
 -> release/Target completion requires PASSING journeys or explicit owner-accepted
    exception with evidence and visible residual risk
~~~

The macro sequence remains PL05 -> PL06 -> PL07 -> PL08 -> PL09.

## 14. Project Spine duties

Project Spine owns:

- CriticalJourney identity and applicability;
- current journey state and latest observation pointer;
- Target, Capability, Gap, and Roadmap references;
- cross-Change durability and orphan/no-path detection;
- governed acceptance of derived observations before current-state updates.

The new carrier is added to the State Ownership table. The Roadmap orphan check
is extended to surface an applicable journey with no defined contract, entry path,
traversable seam path, runtime-lifetime owner, evidence channel, Gap linkage, or
Roadmap lineage. History remains in evidence/Change records.

## 15. PL05 duties

PL05 extends its existing Target Baseline Calibration surface:

- apply the two-branch applicability trigger to accepted Target outcomes and key
  journeys;
- record APPLICABLE or NOT_APPLICABLE with an explicit reason;
- create or require REQUIRED CriticalJourney records in DEFINED state before
  downstream implementation work;
- seed the initial System Skeleton contract;
- record allowed placeholders and the initial evidence channel.

PL05 does not own current satisfaction, runtime execution, or cross-Change state
history. No new PL05 workflow file is created. Target-State Explorer remains the
existing source of Target journey intent.

## 16. PL07 duties

PL07 extends existing Delivery Slices and Change Execution Envelope semantics:

- distinguish Capability and System Walking Skeletons;
- declare affected journeys and ordered seams;
- bind activation expectations and local execution proof;
- require local plus system proof for affected journeys;
- preserve the exact unrelated-work bypass;
- fail closed on authority transfer, future orchestration, or unapproved
  persistence.

Existing routing remains the generic authority-envelope projection. It does not
become a second journey owner or require a separate journey lifecycle branch.
No new checklist taxonomy is introduced. Existing DELIVERY_SLICES.md,
CONTRACT_CLOSURE.md, Change-local requirements traceability, and the Execution
Envelope remain the applicable guidance.

## 17. PL08 duties

PL08 remains the owner of:

- false-done discriminators;
- probe and evidence validity/applicability;
- system-smoke evaluation;
- failure-class findings and evidence-backed learning.

The existing attempt_evaluation.py contracts consume the declared smoke result as
evidence. Progress and review records carry evidence references through their
existing generic evidence sections. PL08 does not select or execute the
operation, own runtime lifetime, or authorize route, result, evidence truth, or
next gate.

## 18. PL09 duties

PL09 owns the safe orchestration boundary and bounded runtime lifecycle
primitives only when orchestration is material. Its later runtime pump must:

- retain one bounded operation lifetime where required;
- preserve identity across seams;
- hand validated results to existing receipt/evidence owners;
- preserve human gates and Project Spine authority.

PL09 does not own the CriticalJourney record, route authority, result truth,
next-gate authority, or evidence truth. Global journey validation uses the pure
system check and hands observations to PL08; it does not become a second
evaluator or state store.

## 19. Change lifecycle duties

The existing lifecycle stages remain unchanged. The following fields become
required only when material:

~~~text
AFFECTED_CRITICAL_JOURNEYS
EXPECTED_JOURNEY_STATE_DELTA
SYSTEM_PROOF_REQUIRED
SYSTEM_PROOF_NOT_APPLICABLE_REASON
AFFECTED_JOURNEY_SURFACE_CHECK
FIRST_BROKEN_SEAM
~~~

The Change Definition records affected journey scope and lineage; Planning binds
exact seams; Readiness audits all affected journeys; Execution keeps proof inside
the Execution Envelope; Closure reports state/evidence and separately reconciles
Gap/Roadmap contribution. Existing Change record templates remain generic
scaffolding; their stage-specific journey content is required by the controlling
workflow and may be filled without duplicating policy text in every template.

Change completion is not Gap closure and is not Roadmap completion.

## 20. Critical Journey Smoke / System Traversability Check

The minimum validation shape is one pure helper module with two bounded symbols:

~~~text
src/planning_lite/traversability.py
  check_critical_journey_smoke(...)
  check_system_traversability(...)
~~~

The per-journey smoke consumes a declared CriticalJourney projection, explicit
carrier applicability, ordered seam observations, and supplied evidence/probe
references. A seam observation identifies the declared seam, PASS or FAIL,
causal reason, reachability, activation, and identity-continuity result. The
helper does not discover these facts.

A seam PASS means its declared producer-consumer handoff is exercised or
deterministically established with the required carried identity and compatible
typed contract. A seam FAIL means the required seam is absent, incompatible,
inactive, or cannot be traversed for the supplied reason. The first ordered
FAIL is FIRST_BROKEN_SEAM. Every later required seam that depends on it is
DOWNSTREAM_UNREACHABLE and is never reported as PASS.

The observed journey state is derived as follows:

- all required seams do not pass: WIRED_FAIL with the primary Gap class from
  Section 10;
- all required seams pass with an allowed NOT_IMPLEMENTED or FIXTURE_ONLY
  placeholder: WIRED_TRAVERSABLE, never PASSING;
- all required seams pass, required real behavior is present, and admissible
  evidence is present: PASSING;
- behavior may be traversable but required evidence/probe is absent or invalid:
  EVIDENCE_GAP with BLOCKED_BY_MISSING_PROBE, and no PASSING promotion;
- the environment prevents the required observation:
  BLOCKED_BY_ENVIRONMENT, and no state promotion;
- the journey carrier applicability is NOT_APPLICABLE:
  NOT_APPLICABLE check disposition, not a journey state.

For a valid applicable journey, `CHECK_DISPOSITION: PASS` means that every
required seam is observed as PASS and the required traversal observation/probe
is admissible. This is a traversal-check disposition: it may accompany
`OBSERVED_TRAVERSABILITY_STATE: WIRED_TRAVERSABLE` when honest placeholders are
present, and it never means durable `PASSING` or release/Change-2 acceptance.

For a blocked observation, no causal failure is inferred from the block. Valid
supplied seam PASS observations remain PASS; any seam not observed is
`UNOBSERVED`; `FIRST_BROKEN_SEAM` is `NONE` when no causal FAIL was supplied;
and the supplied carrier `current_state` is repeated as
`OBSERVED_TRAVERSABILITY_STATE` as an unchanged snapshot. The snapshot is not a
new promotion or regression. `BLOCKED_BY_ENVIRONMENT` has no Gap class;
`BLOCKED_BY_MISSING_PROBE` has `EVIDENCE_GAP` only when no behavioral, wiring,
or orchestration failure was established. Neither disposition updates or
regresses the durable state. A valid causal FAIL takes precedence over a later
probe/environment block and retains `WIRED_FAIL` with its downstream-unreachable
seams. An invalid fixture is `TEST_HARNESS_FAILURE`; its result is not
admissible for reconciliation and the durable state remains unchanged.

The check result includes:

~~~text
JOURNEY_ID
APPLICABILITY
OBSERVED_TRAVERSABILITY_STATE
per-seam: PASS | FAIL | DOWNSTREAM_UNREACHABLE | UNOBSERVED
FIRST_BROKEN_SEAM
GAP_CLASS
CHECK_DISPOSITION:
  PASS | WIRED_FAIL | BLOCKED_BY_ENVIRONMENT |
  BLOCKED_BY_MISSING_PROBE | NOT_APPLICABLE
~~~

check_system_traversability is the deterministic applicability-aware
aggregation of declared journey-smoke observations for the required journey set.
The required set is every carrier record with `applicability: REQUIRED`. Its
aggregate disposition is:

1. `NOT_APPLICABLE` when the required set is empty;
2. `PASS` only when every required journey has per-journey
   `CHECK_DISPOSITION: PASS`;
3. `WIRED_FAIL` when any required journey has `WIRED_FAIL`;
4. `BLOCKED_BY_ENVIRONMENT` when no required journey has `WIRED_FAIL` and at
   least one is blocked by environment; or
5. `BLOCKED_BY_MISSING_PROBE` when none of the preceding conditions applies
   and at least one required journey is blocked by a missing probe.

The aggregate is non-green for every disposition except `PASS` and an empty
required set. Per-journey results remain authoritative observations for their
own reconciliation; aggregate `PASS` never means every journey is durably
`PASSING`, and no aggregate or per-journey check result directly updates
`CRITICAL_JOURNEYS.md`. The helper does not select routes, execute work, scan
the repository, persist state, authorize a result, promote a gate, or become a
runtime pump.

## 21. Self-hosted regression case

The first fixture is:

~~~text
PL_SELF_HOSTED_GOVERNED_OPERATION
EXPECTED STATE: WIRED_FAIL
FIRST_BROKEN_SEAM: OperationGuidance -> Governed Operation Lifecycle
GAP: ORCHESTRATION_GAP
REASON: NO_LEGITIMATE_RUNTIME_LIFETIME_OWNER
~~~

The journey is:

~~~text
Attempt
 -> OperationGuidance
 -> Governed Operation Lifecycle
 -> Execution
 -> validated RunReceipt
 -> PL08 Result/Evidence
 -> authoritative Next Gate
~~~

The pre-correction regression is EXPECTED_SEMANTIC_RED only when the exact
journey, first broken seam, Gap, reason, and downstream-unreachable seams are
observed. It reuses the existing OperationGuidanceV1, Attempt/evaluation,
RunReceipt, and resume-next-gate contracts. It must not fake, invoke, or
implement the future runtime pump, execution runner, same-Attempt receipt
binding, result continuity, or gate continuity.

The harness must distinguish:

~~~text
EXPECTED_SEMANTIC_RED
TEST_HARNESS_FAILURE
ENVIRONMENT_FAILURE
MISSING_PROBE
UNEXPECTED_DIFFERENT_RED
~~~

Only EXPECTED_SEMANTIC_RED satisfies this regression criterion. A test
construction/assertion failure, environment failure, missing admissible probe,
different first broken seam, different state, different Gap, or different
downstream pattern is not expected red. Any such result forces STOP; an
unexpected semantic result requires owner amendment/adjudication before
continuation. The fixture cannot be changed merely to make the expected-red
assertion pass.

## 22. Acceptance criteria

1. Every required materially multi-stage flow has one durable CriticalJourney
   record and one current state.
2. The two-branch applicability trigger is applied explicitly, with
   APPLICABLE/REQUIRED or NOT_APPLICABLE plus reason.
3. Target acceptance requires applicable journeys to be DEFINED.
4. The first journey-affecting Change declares the early System Walking Skeleton
   obligation.
5. The state relation and Project Spine update boundary prevent direct
   validator-to-carrier mutation and false PASSING promotion; blocked or invalid
   observations leave the durable state unchanged.
6. The pure check reports the required V1 fields, localizes the first broken
   seam, marks dependent later seams DOWNSTREAM_UNREACHABLE, and applies the
   frozen blocked-observation and aggregate-disposition rules.
7. WIRING_GAP, ORCHESTRATION_GAP, Activation qualification, IMPLEMENTATION_GAP,
   and EVIDENCE_GAP semantics remain in the existing Gap authority with one
   primary causal class.
8. WIRED_TRAVERSABLE can use an honest placeholder but cannot become PASSING
   without real behavior and evidence.
9. A local capability PASS cannot override journey WIRED_FAIL.
10. A touched journey gets system nonregression; unrelated local work gets only
    the explicit evidence-backed per-Change bypass.
11. PL08 evaluates smoke/evidence and never becomes the runtime pump.
12. PL09 remains bounded to safe orchestration/lifecycle facts and does not
    receive route/result/next-gate/evidence authority.
13. The self-hosted pre-correction regression is EXPECTED_SEMANTIC_RED at the
    exact Guidance-to-Lifecycle seam, and all other red classes STOP.
14. Change 2 cannot resume until the full non-circular resume conjunction is
    satisfied, including observed journey state PASSING and fresh readiness.
15. No registry, database, scheduler, graph engine, biological schema, broad E2E
    platform, or duplicated lifecycle is added.
16. The major PL09 gate, runtime prerequisite boundary, recommendation lineage,
    and both paused work items remain preserved.

## 23. Failure / stop conditions

Stop the Change for owner adjudication if:

- CriticalJourney ownership cannot remain singular;
- the Gap owner or class semantics require a parallel registry;
- the validator needs persistence, authority, route selection, runtime, or a
  second evaluation subsystem;
- the two-branch applicability trigger cannot be applied from accepted Target
  evidence;
- an applicable journey has no exact entry, ordered seam, identity, evidence,
  or runtime-owner decision;
- the state transition/update boundary cannot remain Project Spine-governed;
- a placeholder is being used to claim PASSING;
- the self-hosted regression is not EXPECTED_SEMANTIC_RED for the exact seam,
  Gap, reason, and downstream pattern;
- the self-hosted result is a harness failure, environment failure, missing
  probe, or unexpected different red;
- a materially affected Change attempts the small-change bypass;
- implementation needs to resume or absorb the Governed Operation Lifecycle
  prerequisite or paused Change 2;
- the proposed scope consumes the major PL09 gate, adds a Roadmap vertebra, or
  changes macro sequence;
- the source/test/template surface exceeds the semantic Definition budget;
- a Plan-time architecture-stop condition in the subsection below is met;
- owner authority, user acceptance, or release authority would be inferred.

### Plan-time architecture stop contract

Planning may choose serialization, dataclass or helper layout, mechanical
projection paths, test-helper organization, file order, manifest/checksum
mechanics, and other bounded implementation details that preserve every frozen
Definition rule. Planning may not silently resolve a newly discovered material
architecture contradiction or invent a new material authority boundary.

Stop before treating the Plan as complete and return to owner adjudication when
empirical planning shows that satisfying this Definition would require any of
the following:

- a second CriticalJourney authority;
- moving current journey state out of the singular Project Spine carrier;
- a parallel Gap registry or materially different Gap taxonomy;
- validator persistence or repository-discovery authority;
- validator-driven Project Spine mutation;
- PL08 runtime orchestration;
- route, result, next-gate, or evidence authority transfer;
- a persistent runtime workflow registry;
- a new orchestration subsystem;
- a new Roadmap vertebra;
- splitting this Change across independently governed authority boundaries;
- materially changing the five journey states;
- materially changing the approved applicability trigger;
- materially changing the local/system proof boundary;
- weakening the unrelated-work bypass discriminator;
- inability to reproduce the honest self-hosted `EXPECTED_SEMANTIC_RED`;
- material change to the Governed Operation Lifecycle prerequisite architecture;
- semantic redesign of Change 2 rather than an integration update; or
- any additional material architecture choice not already decided by this
  Definition.

The stop output is:

~~~text
PLAN_ARCHITECTURE_STOP: YES
BLOCKING_FACT: <exact repository fact>
CONTRADICTED_DEFINITION_RULE: <exact frozen rule>
ARCHITECTURE_CHOICE_REQUIRED: <exact unresolved choice>
IMPLEMENTATION_AUTHORIZATION: NO
NEXT_GATE: OWNER_ADJUDICATION_PL_SYSTEM_TRAVERSABILITY_PLAN_ARCHITECTURE_BLOCKER
~~~

This signal uses the existing Planning/Readiness evidence carrier and does not
create a new persistent artifact type. A Plan that reaches no such condition
continues to independent Formal Readiness; this stop does not replace that
gate.

## 24. Explicit non-goals

This Change does not create:

- a Vitality subsystem, registry, database, scheduler, graph engine, or broad
  E2E platform;
- a general orchestration framework or autonomous repair loop;
- route, result, next-gate, evidence-truth, or release authority transfer;
- a new lifecycle stage, checklist taxonomy, CLI, registry, or persistent
  runtime state machine;
- a replacement for Target, Capability Model, Current Assessment, Gap Map,
  Roadmap, Change records, or RunReceipt;
- implementation of the Governed Operation Lifecycle runtime pump;
- F01/F02/F03 operation-trace implementation;
- recommendation absorption, Roadmap reprioritization, or release/tag/push.

## 25. Expected write surfaces

The Definition-mandated semantic surface is:

~~~text
CANONICAL_DESIGN / MODIFY
  docs/design/project-spine/roadmap/ROADMAP.md

TEMPLATE_CONTROL / MODIFY
  template/.planning/control/STATE_OWNERSHIP.md
  template/.planning/control/TARGET_BASELINE_CALIBRATION.md
  template/.planning/control/CAUSAL_GAP_DERIVATION.md
  template/.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md
  template/.planning/control/CHANGE_DEFINITION.md
  template/.planning/control/CHANGE_PLANNING.md
  template/.planning/control/CHANGE_READINESS.md
  template/.planning/control/CHANGE_EXECUTION.md
  template/.planning/control/CHANGE_CLOSURE.md
  template/.planning/disciplines/DELIVERY_SLICES.md

PROJECT_TEMPLATE / ADD
  template/.planning/project/CRITICAL_JOURNEYS.md
  template/.planning/templates/project/CRITICAL_JOURNEYS.md

VALIDATOR / HELPER / ADD
  src/planning_lite/traversability.py

TEST / EVAL / ADD
  tests/test_system_traversability.py
~~~

Definition-mandated semantic path count: 15.

These paths are the semantic owners, carriers, validator, and focused regression
required by the contract. The existing ownership patterns already protect the
project-owned carrier; no ownership-pattern mutation is in scope.

The following paths are not Definition-mandated semantic owners:

~~~text
template/.planning/control/ROOT_ROUTER.md
template/.planning/control/CONTEXT_POLICY.md
template/.planning/control/TARGET_STATE_EXPLORER.md
template/.planning/control/EXECUTION_ROUTING.md
template/.planning/changes/templates/proposal.md
template/.planning/changes/templates/specification.md
template/.planning/changes/templates/plan.md
template/.planning/changes/templates/readiness.md
template/.planning/changes/templates/context.md
template/.planning/changes/templates/progress.md
template/.planning/changes/templates/review.md
template/.planning/docs/MANIFEST_V4.md
template/.planning/framework/SHA256SUMS.txt
~~~

The first 11 are existing-generic or Plan-resolved projections if a concrete
implementation need is demonstrated. The manifest and checksum are mechanical
integrity consequences of existing contracts. Existing Change templates may
carry stage-specific journey facts in their generic sections; the same policy
is not duplicated into every template.

~~~text
PLAN_RESOLVED_OR_MECHANICAL_PATH_COUNT: 13
TOTAL_HISTORICAL_EMPIRICAL_PATH_COUNT: 28
REMOVED_FROM_DEFINITION_MANDATE: 13
~~~

## 26. Recommendation lineage/disposition

Lineage only; no recommendation status mutation or absorption:

~~~text
REC-PL-CAPABILITY-CLOSURE-001:
  PARTIAL_ABSORPTION_RECOMMENDED / NOT ABSORBED BY THIS PREPARATION
  Use only for bounded local-closure, walking-skeleton, and false-done
  discriminators.

PL-REC-PRE-READINESS-CLOSURE-COMPLETENESS-001:
  RETAIN_SEPARATELY_AND_REFERENCE
  Use for exhaustive within-scope readiness and downstream usability; no new
  lifecycle is created.
~~~

The absorbed Executable Target Contract material is referenced as historical
lineage for Target Skeleton/target-scenario semantics only; it is not silently
promoted or status-mutated here.

## 27. Impact on Governed Operation Lifecycle prerequisite

The prerequisite remains:

~~~text
CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
SHAPED / PAUSED_BEFORE_EMPIRICAL_DISCOVERY
MINOR_REFRAME_REQUIRED
~~~

Its later reframe is the bounded runtime-lifetime owner for
PL_SELF_HOSTED_GOVERNED_OPERATION. It may close the self-hosted
ORCHESTRATION_GAP by providing a bounded pump and identity-continuous operation
lifetime. It must not become a general orchestration subsystem or implement
F01/F02/F03. This candidate neither resumes nor absorbs it.

## 28. Impact on paused Change 2

~~~text
CHG-PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-001:
BLOCKED / VALID / PAUSED
IMPLEMENTATION: NOT_AUTHORIZED
~~~

The correction uses the empirical absence-of-consumer findings as evidence only.
It does not amend its Definition/Plan, implement operation tracing, or convert
its missing integration into a new authority path.

Change 2 may resume only after this exact conjunction:

~~~text
SYSTEM_TRAVERSABILITY_CORRECTION_CLOSED
+ GOVERNED_OPERATION_LIFECYCLE_PREREQUISITE_CLOSED
+ PL_SELF_HOSTED_GOVERNED_OPERATION CRITICAL_JOURNEY_SMOKE = PASS
+ observed journey state = PASSING
+ CHANGE_2_AMENDMENT_INTEGRATION_UPDATE
+ FRESH_FORMAL_READINESS = READY
+ SEPARATE_IMPLEMENTATION_AUTHORIZATION
~~~

The PASSING requirement is intentional. WIRED_TRAVERSABLE with a placeholder is
not sufficient for Change 2's base governed-operation consumer. This sequence is
not circular: the correction defines and observes the journey, the runtime
prerequisite closes its runtime-lifetime gap, and Change 2 consumes the proven
base operation only after its own amendment and fresh gates.

## 29. Major PL09 gate preservation

~~~text
OWNER_ADJUDICATION_PL_V39_09_NEXT_SLICE_AFTER_09-B_CLOSURE
PRESERVED / UNCONSUMED
MAJOR_PL09_GATE_CONSUMED: NO
ROADMAP_EFFECT: NO_NEW_VERTEBRA
~~~

This corrective Change is not silently classified as the major next PL09 slice,
and it does not alter the macro PL05 -> PL06 -> PL07 -> PL08 -> PL09 sequence.

## 30. Next owner gate

~~~text
NEXT_SINGLE_GATE: OWNER_AUTHORIZATION_PL_SYSTEM_TRAVERSABILITY_IMPLEMENTATION_PLANNING
OWNER_ACTION: separately authorize preparation of one bounded Implementation Plan against the exact canonical Definition SHA256
IMPLEMENTATION_AUTHORIZED: NO
PLANNING_AUTHORIZED: NO
~~~

Canonical Definition approval records scope authority only. It does not
authorize Planning, Formal Readiness, implementation, runtime resumption,
Change 2 resumption, Change 3, runtime prompt deduplication, major PL09 slice
selection, staging, commit, push, or release.


