# PL-V39-09 / 09-E Read-Only Executor Plan Compiler — Change Definition v1

Status: PROPOSED_FOR_OWNER_REVIEW

This is a bounded Change Definition prepared from the owner-provided
`PL-V39-09 / 09-E Read-Only Executor Plan Compiler / Owner Productization
Definition v1`. It is not an Implementation Plan, Formal Readiness verdict,
implementation authorization, executor route, or product change.

## 1. Change identity and authority

```text
CHANGE_ID:
CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001

TITLE:
PL-V39-09 / 09-E Read-Only Executor Plan Compiler

CHANGE_CLASS:
PRODUCTIZATION

SEMANTIC_AUTHORITY:
PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-SEMANTIC-FREEZE-v1

SEMANTIC_AUTHORITY_SHA256:
B582C2DBC8DB46942768C0EB0E7F8367CE4CEC7D457E2430A369903EA7536829

DEFINITION_STATUS:
PROPOSED_FOR_OWNER_REVIEW

IMPLEMENTATION_AUTHORIZED:
NO
AUTOMATIC_EXECUTOR_ROUTING_AUTHORIZED:
NO
09_F_AUTHORIZED:
NO
09_G_AUTHORIZED:
NO
CHANGE_3:
NOT_ABSORBED / DEFERRED CANDIDATE
```

The entry repository HEAD was `fa48b0fcc7e1067abaed04eafafee88a49838527`.
The next gate after this preparation is owner review of this Definition.

## 2. Problem and bounded outcome

09-E v1 semantics are frozen and field-proven, but currently exist only as a
design/field-proof capability. Planning Lite has no product seam that accepts
an existing semantic Plan, its task graph, and an explicit capability/executor
compilation proposal and deterministically determines whether that proposal
satisfies the frozen 09-E invariants.

The missing capability is validation/compilation, not autonomous semantic
planning. The bounded future outcome is a derived, read-only, non-authoritative
executor-compiled Plan projection with deterministic findings and readiness.
This Definition itself makes no product or template change.

## 3. Selected architecture

```text
EXISTING PLAN/TASK SOURCES
+ EXPLICIT SEMANTIC COMPILATION PROPOSAL
-> PURE DETERMINISTIC 09-E CORE
-> DERIVED EXECUTOR-COMPILED PLAN + FINDINGS + READINESS
```

No model or semantic classifier runs inside the deterministic core. The
preferred future product seam is:

```text
src/planning_lite/plan_compilation.py
```

It must remain separate from `context.py`, `attempt_evaluation.py`,
`operation_lifecycle.py`, and `execution_guidance.py`. A thin read-only CLI
adapter is allowed only if a later live-bound Implementation Plan proves it is
the smallest useful surface.

## 4. Existing authority boundaries

```text
plan.md
= semantic Plan authority for accepted Plan content

tasks.md
= task-state / task-graph carrier

ACTIVE / CURRENT
= current-state authority

PL06
= context / memory / handoff authority

PL07
= operation guidance / authorization projection

PL08
= evaluation / Finding / evidence authority

09-E compiler result
= DERIVED / RECONSTRUCTABLE / NONAUTHORITATIVE / READ_ONLY
```

A compiled result cannot approve a Plan, authorize execution, grant a
capability, select the next gate, mutate task status, create an Attempt, select
the PL07 route, or run the governed lifecycle.

## 5. Explicit proposal boundary

The deterministic core MUST NOT infer from arbitrary prose:

```text
Work Capabilities
Executor Profile
capability coupling
split suitability
semantic completeness
allowed semantic decisions
```

These values enter only through an explicit bounded proposal. A proposal
assertion preserves planner assertion provenance; the runtime may prove only
deterministic structural facts such as enum validity, source identity, unit
completeness, coverage completeness, DAG preservation, split structure,
handoff completeness, dependency consistency, and readiness consistency.

## 6. Exact source binding

A compilation request must bind exact identities:

```text
plan_ref
plan_sha256
tasks_ref
tasks_sha256
proposal identity / digest
```

Source drift is rejected. No latest/nearest/same-Change/mtime/directory-search
association is permitted.

The original task graph is reconstructed only from the accepted task surface
under a deterministic grammar. Ordinary v1 compilation preserves original
units, external dependency edges, and parallelism:

```text
PLAN_REPAIR_AUTHORITY: NO
```

An external DAG mutation is rejected unless a separately authorized Plan repair
is represented; such repair authority is outside this Change.

## 7. CompilationProposalV1 contract

The conceptual proposal contains:

```text
schema_version
source_binding
units[]
existing_dependency_handoffs[]
semantic_assessment_source
semantic_evidence_refs[]
```

Each original unit carries:

```text
original_unit_id
work_capabilities[]
cross_cutting_tags[]
target_executor_profile
already_decided[]
allowed_executor_decisions[]
forbidden_executor_decisions[]
disposition: KEEP_UNIT | CAPABILITY_COUPLED | SPLIT_RECOMMENDED
derived_units[]
new_internal_edges[]
internal_handoffs[]
criterion_assertions: C01..C13
material_findings[]
```

`derived_units`, `new_internal_edges`, and `internal_handoffs` are present only
for a genuine split. Exact serialization remains an Implementation Plan
question and is not frozen by this Definition.

## 8. Split and handoff invariants

For `SPLIT_RECOMMENDED`, the compiler must require one original unit to produce
at least two derived compiled units, new internal dependency edge(s), typed
handoff(s), and explicit satisfaction of S1-S6. It rejects same-count relabels,
neighbor relabels, serialization of existing parallel units, and new external
edges.

Typed handoffs may enrich only genuine existing dependency edges. For parallel
siblings `U1 -> U3` and `U2 -> U3` are valid existing-edge handoffs; `U1 -> U2`
is invalid unless that edge already exists.

## 9. Frozen capability and profile vocabulary

The core Work Capability v1 vocabulary is exactly:

```text
INTENT_REQUIREMENTS
DOMAIN_SEMANTICS
REPOSITORY_UNDERSTANDING
ARCHITECTURE_INTERFACES
DEPENDENCY_PLANNING
IMPLEMENTATION
TOOL_RUNTIME_OPERATION
VERIFICATION_TEST_DESIGN
SEMANTIC_REVIEW
EVIDENCE_GOVERNANCE
```

The accepted cross-cutting capability is `LONG_CONTEXT_SYNTHESIS`.
`ESTIMATION_UNCERTAINTY` and `RESEARCH_DISCOVERY` remain provisional and may
be accepted only where the effective contract explicitly permits them.

The four planning profiles are exactly:

```text
STRONG_AUTONOMOUS
BOUNDED_WORKER
JUNIOR_EXECUTOR
MECHANICAL_EDITOR
```

They must not automatically map to provider, model, adapter, or runtime
routing tier. Existing execution-routing policy remains separate.

## 10. Coverage, findings, and readiness

Every original or derived executable unit must have C01-C13 coverage with
`PASS`, `FAIL`, or `N/A` and a bounded evidence/reason. Missing cells and
missing units are not silent.

The minimum deterministic structural finding classes are:

```text
SOURCE_IDENTITY_MISMATCH
UNKNOWN_ORIGINAL_UNIT
OMITTED_EXECUTABLE_UNIT
DEPENDENCY_EDGE_INVENTION
DEPENDENCY_EDGE_LOSS
PARALLELISM_LOSS
FALSE_CAPABILITY_SPLIT
INVALID_SPLIT_STRUCTURE
INVALID_COUPLING_DECLARATION
MISSING_REQUIRED_HANDOFF
INVALID_HANDOFF
HANDOFF_EDGE_MISMATCH
COVERAGE_INCOMPLETE
INVALID_CRITERION_VALUE
EXECUTOR_PROFILE_MISMATCH
READINESS_CONTRADICTION
UNRESOLVED_MATERIAL_FINDING
```

The product computes only:

```text
EXECUTOR_READY
EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY
EXECUTOR_NOT_READY
```

`EXECUTOR_READY` requires complete unit coverage, valid C01-C13 values,
absence of unresolved material findings, DAG preservation, valid split/coupling
dispositions, valid required handoffs, and no executor-envelope contradiction.
Proposal input cannot upgrade readiness by request.

Controlled discovery, when applicable, must carry:

```text
question
scope/bound
stop_condition
output_contract
verification_before_dependent_work
```

Generic discovery instructions are invalid.

## 11. Derived result and persistence boundary

The conceptual result is:

```text
PlanCompilationResultV1
  source_binding
  original_graph
  compiled_graph
  compiled_units[]
  existing_edge_handoffs[]
  internal_split_handoffs[]
  coverage[]
  findings[]
  readiness
  semantic_assertion_provenance
```

```text
PERSIST_RESULT: NO
```

V1 returns an in-memory/deterministic stdout result. It creates no compilation
registry, database, persistent history, new Change authority, automatic
`tasks.md` rewrite, or automatic `plan.md` rewrite.

The candidate CLI, still subject to live-binding and Plan approval, is:

```text
planning-lite plan-compile TARGET
  --plan <exact path>
  --tasks <exact path>
  --proposal <json path>
  --json
```

It is read-only, emits no output file by default, performs no execution, and
does not approve a Plan.

## 12. Filesystem and parser boundaries

The pure core has no filesystem, Git, network, telemetry, model invocation, or
persistence dependency. A thin adapter may read only explicitly supplied
source paths under a validated root; it must not scan for sources.

`plan.md` may supply exact identity, deterministic approval/status identity,
and explicitly supported structural fields. It must not be mined for arbitrary
semantic prose.

`tasks.md` is the primary deterministic unit/task-graph input. The later
Implementation Plan must bind the exact accepted table columns, Blocking edge
grammar, historical/current compatibility, `Cancelled` handling, and
duplicate/malformed-ID behavior. If the current grammar cannot be parsed
safely, implementation planning stops for minimal managed-template clarification
and must not invent a heuristic parser.

## 13. Live repository binding

The live repository was inspected before this Definition was prepared.

| Concern | Existing live surface | Fact bound for this Change |
|---|---|---|
| Current Plan structure | `template/.planning/changes/templates/plan.md` | Template carries status, outcome, design, affected paths, contracts, delivery, verification, risks, and dependency-order sections; it is not a compiler. |
| Current task structure | `template/.planning/changes/templates/tasks.md` | Exact columns are `ID`, `Outcome`, `Slice type`, `Blocking edge`, `Verification seam / command`, `Blast radius`, `Status`; allowed statuses are `Pending`, `In progress`, `Blocked`, `Done`, `Cancelled`. |
| Plan/task validation | `src/planning_lite/cli.py::build_parser`, `main`; existing `doctor`/update paths | No existing Plan/task compiler, deterministic Plan parser, or `plan-compile` command was found. No new validation surface is inferred here. |
| Current authority | `docs/design/project-spine/CURRENT.md`; `src/planning_lite/context.py::_current_state` | CURRENT/ACTIVE-style state remains authoritative and is not replaced by a derived compilation result. |
| Capability envelope | `src/planning_lite/execution_guidance.py::OperationGuidanceV1`, `CapabilitySpec`, `OperationBinding`, `CAPABILITY_IDS`, `CAPABILITY_STATES`, `PRODUCTION_BINDINGS` | Existing capability states are operation authorization capabilities, not the frozen 09-E Work Capability vocabulary. |
| Executor envelope | `src/planning_lite/governed_executor.py::GovernedExecutionEnvelopeV1`, `prepare_governed_operation`, `validate_governed_completion` | Existing governed execution identity/completion remains authoritative; 09-E does not replace or extend it in this Definition. |
| Handoff | `src/planning_lite/context.py::validate_handoff`, `build_resume_context`, `build_observed_resume_context` | Existing bounded context handoff and producer-bound observation are reused only as external authority; no compiler handoff carrier is created now. |
| Verification/evidence | `src/planning_lite/attempt_evaluation.py::{ObservedResultV1, VerifierContractV1, AcceptanceContractV1, VerifierEvidenceV1, FindingV1, TechnicalEvaluationV1, evaluate_technical}`; `src/planning_lite/telemetry.py::{validate_receipt, append_receipt, collect_governed_receipt}` | PL08 evaluation, findings, evidence, and RunReceipt ownership remain unchanged. |
| Historical fixtures | `docs/design/project-spine/checkpoints/PL-V39-05-C-IMPLEMENTATION-PLAN-v1.md`, `PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-v1.md`, `PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-IMPLEMENTATION-PLAN-v1.md`, and frozen 09-E E0/E0-B2 evidence | These are immutable candidate fixtures for a later Implementation Plan; they do not authorize execution. |

No material live-binding blocker was found for Definition preparation. The exact
task grammar/serialization questions remain explicit Implementation Planning
work and are not silently resolved here.

## 14. Scope

In scope for this Change, after separate Definition approval, Planning,
Formal Readiness, and implementation authorization:

- a pure deterministic 09-E contract/core;
- exact Plan/task/proposal source binding;
- explicit proposal validation;
- preservation of the original DAG and parallelism;
- validation of true splits and existing-edge handoffs;
- complete C01-C13 coverage;
- deterministic findings and readiness;
- a reconstructable derived compiled-plan projection;
- read-only/non-authoritative behavior;
- frozen E0/E0-B2 fixtures and the smallest whole-organism non-regression.

## 15. Non-goals and stop boundaries

This Change does not include LLM classification, automatic capability
inference, automatic decomposition, automatic Plan repair, model selection,
economic routing, AgentWorkPacket, Context Compiler, orchestration, scheduler,
worker behavior, Change 3 telemetry correction, 09-G economics, or persistent
compilation history.

Planning or implementation must stop for owner adjudication if it would require
a new authority, registry, lifecycle, scheduler, runtime route, automatic
semantic inference, external DAG repair, 09-F/09-G semantics, or a material
change to the frozen 09-E contract.

## 16. Acceptance criteria for later Plan and closure

The future productization is successful only when it can:

1. bind exact Plan/task sources and reject drift;
2. validate one explicit semantic compilation proposal;
3. preserve the original DAG, external edges, and parallelism;
4. validate true splits and existing-edge handoffs;
5. enforce complete C01-C13 coverage;
6. produce deterministic findings and readiness;
7. emit a reconstructable derived projection;
8. remain read-only and non-authoritative; and
9. pass the smallest applicable whole-organism regression showing no change to
   PL06, PL07, Attempt/lifecycle, receipts, PL08, or Project Spine and no new
   authority.

The later test surface must cover at least KEEP_UNIT, true 1-to-2 split,
coupling, parallel branch, existing-edge handoff, false split, invented/lost
edge, parallelism loss, unknown/omitted task, source hash drift, coverage
omission, profile/readiness contradiction, controlled-discovery validation,
deterministic repeat, and no-write proof.

## 17. Critical Journey and state boundary

```text
AFFECTED_CRITICAL_JOURNEYS:
PL_SELF_HOSTED_GOVERNED_OPERATION

EXPECTED_JOURNEY_STATE_DELTA:
NO CHANGE; the future compiler is read-only and non-authoritative

SYSTEM_PROOF_REQUIRED:
YES, at implementation closure

FIRST_BROKEN_SEAM:
NONE_EXPECTED; reassess from live Plan before implementation

PL09_SLICE:
09-E-READONLY-EXECUTOR-PLAN-COMPILER

09_E:
OPEN / PRODUCTIZATION DEFINITION PREPARED

09_B:
OPEN / PARTIALLY DESIGNED

09_F:
OPTIONAL / NOT RELEASE PREREQUISITE / NOT AUTHORIZED

09_G:
OPEN / NOT AUTHORIZED

PRODUCT_IMPLEMENTATION_AUTHORIZED:
NO

NEXT_SINGLE_GATE:
OWNER_REVIEW_09_E_PRODUCTIZATION_CHANGE_DEFINITION
```

This Change does not close 09-E overall, reopen 09-B, authorize 09-F or 09-G,
absorb Change 3, alter the Roadmap, or authorize product implementation.

## 18. Owner decision required

Owner review must choose one of `APPROVE`, `REVISE`, `DEFER`, or `REJECT` for
this bounded Definition. Only explicit owner approval may advance it to
Planning. Approval would authorize preparation of one Implementation Plan only;
it would not authorize source/test/template mutation, implementation, staging,
commit, push, executor routing, or lifecycle execution.

```text
NEXT_SINGLE_GATE:
OWNER_REVIEW_09_E_PRODUCTIZATION_CHANGE_DEFINITION
```
