# PL-V39-09 09-E Capability-Aware Plan Compilation Start Contract v1

## Authority and bounded disposition

```text
CONTRACT_ID: 09-E-PLAN-COMPILATION-CONTRACT-AND-FIELD-PROOF
OWNER_SELECTION: PRIMARY_SEMANTIC_CONTROL_PLANE
OWNER_SELECTED: YES
WORK_CLASS: BOUNDED DESIGN + FIELD PROOF
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
AUTOMATIC_EXECUTOR_ROUTING_AUTHORIZED: NO
09_F_AUTHORIZED: NO
09_G_AUTHORIZED: NO
09_B: OPEN / PARTIALLY DESIGNED
09_E: OWNER_SELECTED / START_CONTRACT_MATERIALIZED
CHANGE_3: NOT_ABSORBED / DEFERRED CANDIDATE
CURRENT_PL09_SLICE: 09-E-PLAN-COMPILATION-CONTRACT-AND-FIELD-PROOF
NEXT_PERMITTED_ACTION: RUN_09_E_LIVE_SURFACE_BINDING_AND_FIELD_FIXTURE_PREPARATION
```

This start contract records the primary semantic owner's selected bounded PL09
slice. It is a design-and-field-proof entry contract, not an implementation
plan approval, product authorization, executor authorization, or automatic
routing authorization.

The precondition is the accepted whole-organism baseline:

```text
GATE_A: CLOSED / PASS
09_CORE: CLOSED / WHOLE-ORGANISM PROVEN
09_B: OPEN / PARTIALLY DESIGNED
09_E: OPEN before this materialization
09_F: OPTIONAL EXPERIMENT / NOT RELEASE PREREQUISITE
CHANGE_3: NOT_ABSORBED / VALID CANDIDATE / NOT AUTOMATIC NEXT
```

## Bounded semantic responsibility

The 09-E slice owns the bounded design and field proof of:

- capability-aware work decomposition;
- dependency completeness;
- executor-readiness contracts;
- executor decision budget;
- typed handoffs between capability units;
- plan verification coverage;
- failure and STOP behavior;
- progressive estimation;
- uncertainty and spike handling;
- plan-vs-actual comparison.

The field-proof pass binds these responsibilities to existing repository
surfaces and accepted historical fixtures. It may record exact field coverage,
absence, or an evidence-backed gap. It does not promote an absence into a new
runtime requirement merely because an exact 09-E type is not already present.

## Explicit exclusions and authority ceiling

The following remain outside this start contract:

- product source implementation;
- product test implementation;
- template or consumer mutation;
- automatic executor routing;
- new executor/profile authority;
- creation of a new runtime schema, callback, adapter, or persistence owner;
- execution of 09-B;
- Change 3 execution or absorption;
- 09-F comparator or Context Compiler work;
- 09-G safe orchestration work;
- Roadmap redesign or candidate re-adjudication;
- push, release, merge, or consumer adoption.

`09-B` remains `OPEN / PARTIALLY DESIGNED`. `09-F` and `09-G` require their
own later owner gates. Change 3 remains a separate deferred candidate and is
not an automatic next Change.

## Existing live input and fixture surfaces

The following are the current repository surfaces to bind during the next
09-E gate. Their existing semantics remain authoritative; this contract does
not introduce replacement schemas.

### Plan and task semantics

- `template/.planning/changes/templates/plan.md`
  - approved outcome and exclusions;
  - design summary;
  - modules, interfaces, seams, and adapters;
  - affected paths and symbols;
  - contracts and state transitions;
  - delivery strategy, blocking edges, and blast radius;
  - data, migration, recovery, and repeated execution;
  - verification strategy and seams;
  - risks, rollback, and dependency order.
- `template/.planning/changes/templates/tasks.md`
  - authoritative task-status table;
  - task outcome, slice type, blocking edge, verification seam or command,
    blast radius, and status.
- `template/.planning/changes/templates/specification.md`
  - required behavior, domain invariants, interfaces/contracts, acceptance
    criteria, compatibility, and explicit exclusions.
- `template/.planning/changes/templates/requirements-checklist.md`
  - requirement-to-specification, plan, task, and verification mapping.

These document surfaces are the current semantic Plan/task carriers. No
standalone dependency graph or capability-aware compilation result type is
claimed by this start contract.

### Dependency, capability, executor, and profile semantics

- `template/.planning/control/CHANGE_PLANNING.md`
  - planning obligations, affected journeys, carriers, ordered seams, task
    and proof bindings, dependency ordering, and architecture STOP behavior.
- `template/.planning/control/CHANGE_EXECUTION.md`
  - execution envelope and bounded execution responsibilities.
- `template/.planning/control/EXECUTION_ROUTING.md`
  - dispatch envelope, material task routing, result contract, authority
    boundary, STOP/escalation behavior, and no-implicit-delegation rule.
- `src/planning_lite/execution_guidance.py`
  - `OperationGuidanceV1`;
  - `CapabilitySpec`;
  - `OperationBinding`;
  - `PRODUCTION_BINDINGS`;
  - `select_operation_guidance`.
- `src/planning_lite/governed_executor.py`
  - `GovernedExecutionEnvelopeV1`;
  - `GovernedExecutionCompletionV1`;
  - `prepare_governed_operation`;
  - `validate_governed_completion`.
- `template/.planning/AGENT_PROFILE.yml.jinja`
  - rendered agent/profile and adapter-path representation.
- `template/.planning/control/AGENT_ADAPTER_CONTRACT.md`
  - adapter translation boundary and prohibition on redefining workflow,
    ownership, approval, or evidence semantics.

These are existing guidance, envelope, profile, and routing surfaces. They are
inputs for field proof only; the contract does not authorize automatic routing
or executor behavior changes.

### Handoff, verification, and evidence semantics

- `src/planning_lite/context.py`
  - `validate_handoff`;
  - `build_resume_context`;
  - `ProducedResumeContextV1`;
  - `OperationDepthObservationV1`.
- `template/.planning/changes/templates/context.md`
  - bounded execution envelope, allowed/forbidden surface, owned
    responsibility, blockers, and next permitted action.
- `template/.planning/changes/templates/review.md`
  - specification/standards evidence, completion, technical evaluation,
    findings, superseded evidence, and owner disposition boundary.
- `template/.planning/changes/templates/readiness.md`
  - exhaustive readiness, blocker ledger, determinacy, materiality, and
    separate implementation authorization.
- `template/.planning/changes/templates/progress.md`
  - progress and Governed Attempt / Technical Evaluation evidence carriers.
- `src/planning_lite/attempt_evaluation.py`
  - `AttemptRecordV1`, `ObservedResultV1`, `VerifierContractV1`,
    `AcceptanceContractV1`, `EvidenceApplicabilityV1`,
    `FindingApplicabilityV1`, `VerifierEvidenceV1`,
    `EvidenceSupersessionV1`, `FindingV1`, `TechnicalEvaluationV1`, and
    `evaluate_technical`.
- `src/planning_lite/traversability.py`
  - `SeamObservationV1`, `CriticalJourneyProjectionV1`, `SeamResultV1`,
    `JourneySmokeResultV1`, `SystemTraversabilityResultV1`, and
    `check_system_traversability`.
- `src/planning_lite/project_spine.py`
  - `ProjectSpineSnapshotV1` and `record_post_evaluation_checkpoint`.
- `src/planning_lite/telemetry.py`
  - `collect_governed_receipt` readback surface.

These surfaces provide existing handoff, verification, evaluation, journey,
checkpoint, and receipt evidence carriers. Their presence does not transfer
Project Spine ownership or authorize lifecycle/runtime persistence changes.

## Immutable field-proof fixture candidates

The following tracked historical plans are suitable read-only fixtures for
field binding and comparison:

1. `docs/design/project-spine/checkpoints/PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-IMPLEMENTATION-PLAN-v1.md`
   - accepted guidance, candidate binding, authority, provenance, task graph,
     verification, and STOP field coverage.
2. `docs/design/project-spine/checkpoints/PL-V39-08-IMPLEMENTATION-PLAN-v1.md`
   - accepted task graph, dependency order, acceptance traceability,
     verification matrix, applicability/supersession, evidence economy, and
     07/08/09 boundary fields.
3. `docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-v1.md`
   - accepted lifecycle contracts, governed execution boundaries, and
     lifecycle evidence fields.
4. `docs/design/project-spine/checkpoints/PL-V39-06-OPERATION-DEPTH-OBSERVATION-BRIDGE-IMPLEMENTATION-PLAN-v1.md`
   - accepted producer-bound observation, handoff, and verification field
     coverage.

The next gate must verify exact field locations and identity from the live
repository. Fixture status does not authorize copying, rewriting, or
materializing any fixture as a new runtime artifact.

## Field-proof method and stop boundary

The next permitted gate is:

```text
OWNER_REVIEW_09_E_LIVE_SURFACE_BINDING_AND_FIELD_FIXTURE_PREPARATION
```

That gate may inspect the listed surfaces, bind existing fields to the 09-E
responsibilities, and prepare an owner-reviewable field fixture map. It must
report each material absent carrier or contradictory ownership evidence and
stop on an unsafe shared-contract conflict. It may not implement source or
tests, mutate templates or consumers, alter the Roadmap, absorb Change 3, or
start 09-B, 09-F, or 09-G.

```text
NEXT_PERMITTED_ACTION:
RUN_09_E_LIVE_SURFACE_BINDING_AND_FIELD_FIXTURE_PREPARATION
```
