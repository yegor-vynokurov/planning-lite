# PL-V39-07 Implementation Plan Amendment v1

## 1. Plan Amendment Identity

- Plan Amendment ID: `PL-V39-07-IMPLEMENTATION-PLAN-AMENDMENT-001`
- Change: `CHG-PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-001`
- Logical capability: `Deterministic Operation Guidance`
- Status: `APPROVED_BY_OWNER`
- Prepared on: `2026-09-06`
- Owner approval: `USER / EXPLICIT — 2026-09-06`
- Drafting baseline HEAD: `7e28a1967178f41fb6674c2a51a7896980bf5efb`
- Active lifecycle at drafting: `PLANNING_IN_PROGRESS / UNCHANGED`
- Formal Readiness: `NOT RUN / REMAINS PAUSED`
- Implementation authorization: `NO`
- Implementation tasks: `NOT STARTED`

Owner decision recorded by this governance step:

```text
OWNER_PLAN_AMENDMENT_DECISION: APPROVE
A-01: SEMANTIC_CLARIFICATION / APPLIED
A-02: SEMANTIC_CLARIFICATION / APPLIED
A-03: SEMANTIC_CLARIFICATION / APPLIED
A-04: EXPLICIT_SCOPE_ACCOUNTING / APPLIED
```

This approved artifact is the bounded delta to the approved predecessor Plan.
It does not create a Planning Authority checkpoint, run Formal Readiness,
authorize implementation, or authorize Git mutation.

## 2. Authority and Draft Binding

| Input | Path / identity | SHA256 / revision |
|---|---|---|
| approved predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-07-PROPOSED-CHANGE-DEFINITION-v1.md` | `654c854311dc69a4444cc019aa50f49a18c86eeb5d01ac8225196c8c20a8e627` |
| approved predecessor Plan | `docs/design/project-spine/checkpoints/PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-IMPLEMENTATION-PLAN-v1.md` | `a09f4b42509f434fe56c35a8f47e8e16d76fdcc9644c4fb16a6efdf5499e6ae1` |
| predecessor Planning Authority | Git commit | `7e28a1967178f41fb6674c2a51a7896980bf5efb` |
| approved Definition Amendment | `docs/design/project-spine/checkpoints/PL-V39-07-DEFINITION-AMENDMENT-v1.md` | `6b3e4d33d61174d38894d65bc564f78a4ca682c2c6831f07ed39be937bec1576` |
| empirical reconciliation | `D:\documents\PL-V39-07-EMPIRICAL-SKILL-POLICY-CHECKLIST-RECONCILIATION.md` | `65497c65282db94c7f23e5285b9ef5aaa5a86e03846ace685ce0cad60b90e36e` |
| support-aware addendum | `D:\documents\PL-V39-07-SUPPORT-AWARE-ARCHITECTURE-ADDENDUM.md` | `ce898c6a39a0806e7a7e1dbd08be868f067345e90a1cb3299628821cfcd26977` |

The evidence records support the amendment but do not authorize it. This Plan
Amendment is approved only with the exact Definition Amendment hash above. If
that Definition Amendment changes materially, this Plan must be reconciled and
reapproved before Readiness.

Both amendments are approved. The predecessor Plan remains controlling for
unchanged gate/evidence/verification semantics; this amendment replaces only
the execution-only operation model, affected task details, write surfaces, and
discriminators identified below.

```text
predecessor Definition + approved Definition Amendment
= current Change scope authority

predecessor Plan + approved Plan Amendment
= current implementation planning authority

new committed Planning Authority checkpoint
= PENDING SEPARATE OWNER AUTHORIZATION
```

## 3. Architecture Decision

```text
RUNTIME_SEAM: KEEP
```

Preserve the proven direction:

```text
one focused downstream guidance module
+ the same single ResumeContextV1 snapshot
+ opt-in planning-lite resume guidance projection
+ pure finite selector
+ no new persistent registry
```

`src/planning_lite/execution_guidance.py` may remain the implementation filename
for compatibility and boundedness in this Change. Its public logical contract
is generalized to `OperationGuidanceV1`; runtime-symbol/file renaming is not
required and must not be performed merely for terminology consistency.

The invocation remains:

```text
one resume --guidance invocation
  -> build ResumeContext once
  -> preserve that exact mapping
  -> pure select_operation_guidance(ResumeContextV1)
  -> return unchanged resume + derived OperationGuidanceV1 wrapper
```

The implementation module remains downstream of `context.py`. It must not call
the context builder, rescan the repository, read Git history, resolve another
home, load all guidance files, or accept a caller-supplied authority decision.
The `ResumeContextV1` and default plain-resume schemas stay unchanged.

```text
GUIDANCE_INPUT_IDENTITY: SAME_RESUME_SNAPSHOT
ROUTE_PREDICATE_INPUTS: SAME_RESUME_SNAPSHOT_ONLY
ROUTE_TIME_AUTHORITY_READS: NONE
PERSISTENT_NEW_REGISTRY_REQUIRED: NO
SECOND_CONTEXT_BUILDER: NO
```

The owning workflow validates upstream prerequisites and emits the canonical
lifecycle/stage/next-action projection owned by `ACTIVE`/current authority.
Operation Guidance consumes only that projection and other facts already
present in the same validated ResumeContext. It must not reopen Definition,
Plan, or `readiness.md`; rerun Readiness; infer approval from prose; build
context again; or add route-time reads. An unobservable required predicate fact
stops for later amendment rather than expanding `ResumeContextV1`.

## 4. Exact Operation Guidance Contract

The JSON-compatible logical result is:

```text
OperationGuidanceV1 {
  schema_version: 1,
  outcome: MATCHED
         | NO_APPLICABLE_OPERATION
         | AMBIGUOUS_OPERATION
         | NOT_AUTHORIZED
         | MISSING_OR_UNUSABLE_CONTEXT,
  reason_code: <finite exact value>,
  operation: null | {
    operation_id,
    operation_class,
    route_id
  },
  authority: null | {
    predicate_id,
    predicate_result: AUTHORIZED_FOR_THIS_OPERATION | NOT_AUTHORIZED,
    authority_refs[]
  },
  capabilities: [],
  guidance: null | {
    procedure_ref,
    mode_ref,
    skill_ref,
    policy_refs[],
    discipline_refs[],
    task_binding_refs[],
    precondition_refs[],
    scope_refs[],
    verification_refs[],
    result_contract_refs[],
    evidence_refs[],
    stop_condition_refs[],
    escalation_ref,
    next_gate_ref,
    next_gate_owner_ref
  },
  provenance: {
    candidate_set_id,
    resume_schema_version,
    resume_status,
    source_revision,
    authority_refs[] {path, sha256},
    selection_reason
  }
}
```

Each `capabilities[]` item has a fixed pilot capability identity, one of these
states, and an owning authority reference when material:

```text
{
  capability_id,
  state: ALLOWED | FORBIDDEN | REQUIRES_SEPARATE_AUTHORIZATION | NOT_APPLICABLE,
  authority_ref
}
```

The pilot capability identities are declared in the finite route definitions;
they are not a persistent global permission enum. Array order is declaration
order, duplicates are invalid by construction, and serialization reuses the
existing stable JSON/YAML behavior.

`guidance` is non-null only for `MATCHED`. `operation` and the evaluated
authority record may remain present on `NOT_AUTHORIZED` so the observable result
identifies the exact selected route that failed its predicate. No prior result,
provenance record, route ID, skill, or capability projection is accepted as
authority input.

Capability states describe the selected separately governed operation under
current authority. They do not authorize actions by the guidance command.

```text
planning-lite resume --guidance: READ_ONLY
```

This invariant holds for every outcome and capability projection, including a
matched result with `PRODUCT_WRITE = ALLOWED` or `GOVERNANCE_WRITE = ALLOWED`.
Those states describe the later separately invoked operation; the guidance
command itself never writes.

## 5. Required Routing Order and Failure Precedence

The selector must use this order:

1. validate one `ResumeContextV1` object and required current-authority facts;
2. obtain the exact operation identity from the validated authoritative
   `next_permitted_action` using only finite exact identity handling;
3. validate the immutable bounded candidate set;
4. find zero, one, or multiple exact candidate bindings for that operation;
5. if exactly one route applies, evaluate that route's workflow prerequisites,
   required owner decision, and requested capability contract;
6. only for an implementation route, evaluate
   `implementation_authorized == true` as a mandatory route predicate;
7. if authorized, project fixed skill/workflow/policy/discipline/task/evidence/
   result references and bounded provenance;
8. return the derived result and never execute its next gate.

The first applicable failure is final in this exact precedence:

| Order | Condition | Outcome | Primary `reason_code` |
|---:|---|---|---|
| 1 | resume object/schema/current facts unusable | `MISSING_OR_UNUSABLE_CONTEXT` | existing specific context reason (`INVALID_RESUME_CONTEXT`, `RESUME_NOT_CURRENT`, `MISSING_ACTIVE_CHANGE`, or `MISSING_ACTIVE_CONTEXT`) |
| 2 | immutable candidate-set shape/bound/integrity invalid | `MISSING_OR_UNUSABLE_CONTEXT` | `INVALID_CANDIDATE_SET` |
| 3 | no exact operation binding | `NO_APPLICABLE_OPERATION` | `UNMAPPED_OPERATION` |
| 4 | multiple exact operation bindings | `AMBIGUOUS_OPERATION` | `MULTIPLE_EXACT_BINDINGS` |
| 5 | selected workflow/lifecycle prerequisite is not met | `NOT_AUTHORIZED` | `ROUTE_PREREQUISITE_NOT_MET` |
| 6 | selected route's required owner decision is absent | `NOT_AUTHORIZED` | route-specific code, including `IMPLEMENTATION_NOT_AUTHORIZED` |
| 7 | route definition requests an unowned/contradictory capability | `MISSING_OR_UNUSABLE_CONTEXT` | `INVALID_CAPABILITY_CONTRACT` |
| 8 | one exact route and its required authority are valid | `MATCHED` | `EXACT_OPERATION_BINDING` |

An open blocker is not evaluated as a universal pre-routing gate. The selected
workflow predicate decides whether the blocker prevents that operation, is an
input to an audit, or is unrelated. A Formal Readiness route may inspect known
blockers; an implementation route must reject any blocker that prevents its
authorized task.

There is no semantic/fuzzy/model fallback and no later condition upgrades an
earlier failure.

## 6. Finite Candidate Set

```text
CANDIDATE_SET_MECHANISM:
one immutable finite ordered tuple in execution_guidance.py;
duplicate identities validated before lookup;
no filesystem/config/plugin registry;
no recursive scan;
no load-all-and-choose

ACTION_CLASS_MAPPING: FINITE_EXACT
```

The production pilot contains exactly three action bindings in two materially
different route families:

| Exact canonical `next_permitted_action` | Operation class | Route ID | Existing producer / procedure | Skill | Discipline |
|---|---|---|---|---|---|
| `RUN_FORMAL_READINESS` | `FORMAL_READINESS_AUDIT` | `FORMAL_READINESS_V1` | producer clarification in `.planning/control/CHANGE_PLANNING.md`; procedure `.planning/control/CHANGE_READINESS.md` | `.planning/skills/planning-audit/SKILL.md` | zero or conditional existing discipline as selected by exact task facts |
| `EXECUTE_AUTHORIZED_TASK` | `EXECUTE_CHANGE_TASK` | `CHANGE_EXECUTION_V1` | `.planning/control/CHANGE_EXECUTION.md` | `.planning/skills/planning-execute/SKILL.md` | none |
| `EXECUTE_AUTHORIZED_CONTRACT_TASK` | `EXECUTE_CONTRACT_CLOSURE_TASK` | `CHANGE_EXECUTION_V1` | `.planning/control/CHANGE_EXECUTION.md` | `.planning/skills/planning-execute/SKILL.md` | `.planning/disciplines/CONTRACT_CLOSURE.md` |

`CHANGE_PLANNING.md` receives the one exact optional readiness action identity
at the already-owned Plan-approval transition. `CHANGE_READINESS.md` receives
only the matching entry/result clarification. `CHANGE_EXECUTION.md` retains the
predecessor Plan's two exact optional implementation producer identities.
Producer clarifications do not create state authority; `.planning/ACTIVE.md`
continues to own the actual current value.

`RUN_FORMAL_READINESS` belongs to the finite exact managed consumer lifecycle
identity namespace. It is not an alias for the central/self-hosted
`RUN_PL_V39_07_FORMAL_READINESS` string or for another project-specific action.

```text
ACTION_IDENTITY_NAMESPACE: FINITE_EXACT_MANAGED_IDENTITIES
```

No project-ID stripping, normalization, alias, prefix/suffix, or fuzzy
equivalence is permitted. Any project-specific action not separately declared
in the production tuple returns `NO_APPLICABLE_OPERATION`. The central
self-hosted `CURRENT.md` need not be rewritten merely to make this future
consumer route match.

Exact comparison follows the existing cleaned markdown scalar value and then
uses Unicode equality. No case folding, alias, prefix/suffix, substring, regex,
tokenization, edit distance, heuristic, semantic, or model match is allowed.

The private bounded test seam may retain the predecessor maximum of eight
candidate entries only to prove invalid, zero, one, and multiple exact results.
The public builder always uses the immutable three-entry production tuple.

No Git-checkpoint route is added to the minimum candidate set. Git independence
is demonstrated by capability projection, the `planning-checkpoint` contract,
and a negative test; a fourth route would add producer semantics solely for
coverage decoration.

## 7. Route-Specific Predicate and Capability Matrix

The route table owns only finite predicate references and capability
projections. Current state, workflows, approved task/Plan, and owner decisions
remain authority.

| Route | READ | GOVERNANCE_WRITE | PRODUCT_WRITE | GIT_STAGE | GIT_COMMIT | NETWORK / EXTERNAL | DISPOSABLE_CONSUMER | LIVE_CONSUMER | `implementation_authorized` |
|---|---|---|---|---|---|---|---|---|---|
| `FORMAL_READINESS_V1` | `ALLOWED` within readiness scope | `ALLOWED` only for the workflow's bounded readiness evidence/state record; otherwise `FORBIDDEN` | `FORBIDDEN` | `FORBIDDEN` | `FORBIDDEN` | `REQUIRES_SEPARATE_AUTHORIZATION` | `FORBIDDEN` | `FORBIDDEN` | not required and cannot elevate |
| `CHANGE_EXECUTION_V1` ordinary | `ALLOWED` within exact task/Envelope | `ALLOWED` only for existing progress/ledger/state evidence owned by the workflow | `ALLOWED` only within approved task/Envelope | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | required |
| `CHANGE_EXECUTION_V1` contract closure | same as ordinary implementation | same as ordinary implementation | same as ordinary implementation | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | `REQUIRES_SEPARATE_AUTHORIZATION` | required |

`ALLOWED` never means unbounded. The exact active task/Plan/Execution Envelope
continues to own paths and commands. `REQUIRES_SEPARATE_AUTHORIZATION` is an
explicit non-grant and does not block a selected route when that capability is
not part of the requested operation.

The Formal Readiness predicate requires a `CURRENT` ResumeContext, an active
Change, the exact Readiness lifecycle/stage/action emitted by the approved
planning transition, and no bounded current-authority conflict that makes the
audit undefined. `CHANGE_PLANNING.md` owns the upstream approved-Plan
prerequisite. The selector consumes its canonical lifecycle/action projection;
it does not independently read or validate Definition/Plan bodies. It does not
require implementation authorization.

The implementation predicate consumes only a `CURRENT` ResumeContext, active
Change, implementation-capable lifecycle/stage, exact supported implementation
action, `implementation_authorized = YES`, and route-relevant current blocker/
context facts. The owning lifecycle/workflow is responsible for emitting that
action only after its approved-Plan/Ready prerequisites are satisfied. The
selector does not independently read or validate Definition, Plan, or Readiness
bodies. Presence of the execution skill or an earlier matched guidance result
cannot satisfy any predicate.

## 8. Result, Evidence, and Provenance Boundary

The result must make these distinctions observable:

```text
operation identity != route authority
MATCHED != durable permission token
capability projection != capability grant beyond current authority
evidence != authorization
descriptive next gate != next gate execution
session checkpoint != Git staging/commit
```

Fixed procedure/mode/skill/policy/discipline/gate pointers are literals in the
finite mapping. Dynamic task/context/evidence pointers come only from the
already validated `ResumeContextV1` bounded source set. The selector performs no
route-time file read or hash and copies no workflow, Plan, envelope, checklist,
or evidence body.

Provenance contains only the candidate-set identity, stable selection reason,
resume schema/status/source revision, and bounded authority identities/hashes
already emitted by the same resume snapshot. It is returned in memory/stdout,
is not persisted, and cannot be supplied back as authority or candidate config.

CLI exit behavior remains:

```text
MATCHED                                      -> 0
structured non-match / non-authorization    -> 3
malformed invocation / existing CLI error   -> 2
plain resume without --guidance              -> existing behavior
```

For every capability-state combination and every `MATCHED` result, focused
tests compare filesystem inventory/content and Git status before and after
`resume --guidance`; all must remain unchanged.

## 9. Thin Skill and Managed-Control Normalization

Canonical skill bodies under `.planning/skills/**` own reusable semantics.
Codex adapters under `.agents/skills/**` remain thin discovery/host projections
and must not own routing or authorization rules.

Only these four canonical skill plus adapter pairs may be clarified:

| Skill | Canonical clarification | Adapter alignment |
|---|---|---|
| `planning-audit` | legal read-only readiness/review/adjudication uses the selected workflow predicate; implementation authorization is not borrowed | align the description with canonical readiness/review/project-state triggers; retain canonical pointer |
| `planning-checkpoint` | session/state handoff preserves stage and does not grant Git stage/commit | align the description; retain canonical pointer and no Git semantics in adapter body |
| `planning-dialogue` | non-mutating exploration has an anti-trigger against silent recommendation promotion or governed work start | align discovery wording; retain canonical pointer |
| `planning-plan` | Definition/Plan/recommendation/amendment work uses planning workflow gates and never authorizes production writes | align discovery wording; retain canonical pointer |

The other four canonical skills and adapters are unchanged. No skill schema,
registry, merge, split, deprecation, or new recommendation skill is permitted.

Managed control clarifications remain narrow:

- `CHANGE_PLANNING.md`: exact readiness action producer after explicit Plan
  approval;
- `CHANGE_READINESS.md`: exact readiness operation entry/result and continued
  non-authorization of Execution;
- `CHANGE_EXECUTION.md`: the two exact implementation action producers and
  capability non-elevation;
- `SESSION_CHECKPOINT.md`: explicit no-standing-Git-stage/commit boundary;
- `APPROVAL_GATES.md`: Git mutation and external/live-consumer capabilities do
  not follow from Gate D or checkpoint activation;
- `STATE_OWNERSHIP.md`: Operation Guidance/provenance is derived,
  non-authoritative, and non-persistent.

No root/mode router, lifecycle, discipline body, recommendation workflow, or
adapter-owned routing semantics changes.

## 10. Exact Planned Write Surface

The predecessor Plan listed 10 implementation/evidence paths. The approved
semantic amendment intentionally expands that future surface:

```text
PLANNED_WRITE_SURFACE_CHANGE: 10 -> 22
CLASS: MATERIAL_BUT_BOUNDED_BY_APPROVED_AMENDMENT

RUNTIME: 1
CLI: 1
MANAGED_CONTROL: 6
CANONICAL_SKILL: 4
THIN_ADAPTER: 4
MANAGED_INTEGRITY: 1
TEST: 3
GOVERNANCE_EVIDENCE: 2
TOTAL: 22
```

After the new committed Planning Authority, `READY` Formal Readiness, and
separate Execution authorization, implementation may write only:

| Path | Class | Responsibility | Required by task / amended AC |
|---|---|---|---|
| `src/planning_lite/execution_guidance.py` | `RUNTIME` | focused `OperationGuidanceV1`, finite three-binding model, route predicates, capability/result projection, precedence, and provenance | T-01, T-02, T-03 / AC-01…AC-05, AC-08 |
| `src/planning_lite/cli.py` | `CLI` | existing opt-in `resume --guidance` wrapper and exact exit behavior; plain resume unchanged | T-05 / AC-01, AC-03…AC-05, AC-07 |
| `template/.planning/control/CHANGE_PLANNING.md` | `MANAGED_CONTROL` | exact `RUN_FORMAL_READINESS` producer at the existing Plan-approval transition | T-04 / AC-02, AC-03, AC-08 |
| `template/.planning/control/CHANGE_READINESS.md` | `MANAGED_CONTROL` | exact readiness entry/result clarification | T-04 / AC-03, AC-04, AC-08 |
| `template/.planning/control/CHANGE_EXECUTION.md` | `MANAGED_CONTROL` | two implementation action producer identities and capability non-elevation | T-04 / AC-03, AC-04, AC-06, AC-08 |
| `template/.planning/control/SESSION_CHECKPOINT.md` | `MANAGED_CONTROL` | session checkpoint versus Git mutation clarification | T-04 / AC-03, AC-06, AC-07 |
| `template/.planning/control/APPROVAL_GATES.md` | `MANAGED_CONTROL` | independent Git/external/live-consumer capability authority | T-04 / AC-03, AC-04, AC-08 |
| `template/.planning/control/STATE_OWNERSHIP.md` | `MANAGED_CONTROL` | derived Operation Guidance/provenance ownership | T-04 / AC-04, AC-07 |
| `template/.planning/skills/planning-audit/SKILL.md` | `CANONICAL_SKILL` | bounded trigger/authority clarification | T-04 / AC-03, AC-06 |
| `template/.planning/skills/planning-checkpoint/SKILL.md` | `CANONICAL_SKILL` | bounded checkpoint/Git anti-trigger | T-04 / AC-03, AC-06 |
| `template/.planning/skills/planning-dialogue/SKILL.md` | `CANONICAL_SKILL` | bounded non-mutating anti-trigger | T-04 / AC-06, AC-07 |
| `template/.planning/skills/planning-plan/SKILL.md` | `CANONICAL_SKILL` | bounded planning-gate/non-authorization clarification | T-04 / AC-03, AC-06 |
| `template/.agents/skills/planning-audit/SKILL.md` | `THIN_ADAPTER` | align discovery description only | T-04 / AC-06, AC-07 |
| `template/.agents/skills/planning-checkpoint/SKILL.md` | `THIN_ADAPTER` | align discovery description only | T-04 / AC-06, AC-07 |
| `template/.agents/skills/planning-dialogue/SKILL.md` | `THIN_ADAPTER` | align discovery description only | T-04 / AC-06, AC-07 |
| `template/.agents/skills/planning-plan/SKILL.md` | `THIN_ADAPTER` | align discovery description only | T-04 / AC-06, AC-07 |
| `template/.planning/framework/SHA256SUMS.txt` | `MANAGED_INTEGRITY` | deterministic regeneration for changed managed files | T-04 / AC-07 |
| `tests/test_execution_guidance.py` | `TEST` | focused contract, operation routes, predicates, capabilities, precedence, provenance, and fixture shapes | T-01, T-02, T-03, T-07, T-08 / AC-01…AC-09 |
| `tests/test_cli.py` | `TEST` | wrapper, serialization, exits, plain-resume compatibility, same snapshot, and no writes | T-05 / AC-01, AC-03…AC-05, AC-07 |
| `tests/test_field_control_pack_foundation.py` | `TEST` | exact producers, skill/adapter ownership, checkpoint/Git boundary, no new skill/registry/router/lifecycle | T-04, T-06 / AC-06, AC-07, AC-09 |
| `docs/design/project-spine/checkpoints/PL-V39-07-EXECUTION-LEDGER-v1.md` | `GOVERNANCE_EVIDENCE` | one cumulative T-01…T-08 record | T-01…T-08 / AC-07 |
| `docs/design/project-spine/checkpoints/PL-V39-07-COMPLETION-REVIEW-v1.md` | `GOVERNANCE_EVIDENCE` | T-09 final review only | T-09 / AC-01…AC-09 |

```text
PLANNED_WRITE_SURFACE_JUSTIFIED: 22/22
ORPHANED_PATHS: NONE
```

The two approved amendment artifacts are governance authority, not
implementation paths. `tests/test_context_resume.py`,
`tests/test_central_resume_contract.py`, and `tests/test_template.py` remain
read-only verification surfaces unless a material failure forces amendment.

Explicitly unchanged: `context.py`, `ResumeContextV1`, `ROOT_ROUTER.md`,
`MODE_ROUTER.md`, `CHANGE_LIFECYCLE.md`, discipline bodies, recommendation
 surfaces, `copier.yml`, `OWNERSHIP.yml`, product registry/update/Doctor/Campaign
 code, Roadmap, the aligned `CURRENT`, live consumers, and release files.

Any required write outside the table stops the dependent task for owner
amendment/adjudication.

## 11. Amended Nine-Task Graph

```text
TASK_COUNT: 9 UNCHANGED
```

### T-01 — Logical Operation Guidance contract

- Outcome: implement `OperationGuidanceV1`, finite outcomes/reasons, capability
  states, result/evidence fields, and the operation-before-authorization
  precedence skeleton over one preserved resume snapshot.
- Dependencies: approved amendments, committed Planning Authority, Formal
  Readiness `READY`, and separate owner Execution authorization.
- Write surface: `execution_guidance.py`, focused test file, cumulative ledger.
- Verification seam: exact shape/order; failure precedence; invalid/duplicate
  capabilities and candidate definitions rejected; no persistence.
- Stop: `ResumeContextV1` must change, a universal permission enum/registry is
  required, or failure identity becomes non-deterministic.

### T-02 — Finite operation mapping and route-specific predicates

- Outcome: implement the exact three-binding/two-family candidate set,
  readiness and implementation predicates, and bounded capability matrix.
- Dependencies: T-01 PASS.
- Write surface: `execution_guidance.py`, focused tests, ledger.
- Verification seam: exact readiness and two implementation identities; zero,
  one, injected-two, invalid, case/alias/near-match, and out-of-bound cases;
  readiness ignores the implementation flag while implementation requires it.
- Stop: a scan, registry, fuzzy/semantic/model classifier, or caller-supplied
  route/authority source becomes necessary.

### T-03 — Deterministic selector and bounded provenance

- Outcome: select operation first, evaluate only its route predicate, project
  capabilities and fixed references, and bind bounded provenance to the same
  resume snapshot without additional reads.
- Dependencies: T-02 PASS.
- Write surface: `execution_guidance.py`, focused tests, ledger.
- Verification seam: matched readiness with implementation false; rejected
  implementation with false; matched implementation with true but Git commit
  not granted; stale/missing/blocked/ambiguous contexts; repeated input is
  byte-equivalent; prior provenance cannot feed authority.
- Stop: path discovery, second context construction, Plan/workflow body copying,
  or another authority source is required.

### T-04 — Managed workflow, policy, skill, and adapter normalization

- Outcome: make only the listed producer/ownership/gate clarifications, update
  the four canonical skill contracts and four thin adapter descriptions,
  regenerate SHA coverage, and prove all eight skills remain.
- Dependencies: T-02 PASS; may proceed independently of T-03.
- Write surface: listed managed control/skill/adapter/SHA files, foundation
  test, ledger.
- Verification seam: canonical skill owns semantics; adapter remains thin;
  readiness and implementation producers are exact; zero/conditional
  discipline remains legal; checkpoint does not grant Git mutation; no new
  skill/registry/router/lifecycle/checklist.
- Stop: any fifth skill needs modification, a new skill/checklist/policy owner is
  needed, or adapter-owned routing semantics appears necessary.

### T-05 — Opt-in resume/CLI integration

- Outcome: expose the public selector through existing `resume --guidance`,
  returning unchanged resume plus `OperationGuidanceV1` with exact `0/3/2`
  exits while preserving plain resume.
- Dependencies: T-03 PASS and T-04 PASS.
- Write surface: `cli.py`, `test_cli.py`, focused test file, ledger.
- Verification seam: JSON/YAML matched/nonmatched results, same snapshot,
  capability/result projection, plain output equivalence, and no filesystem,
  home, target, status, or next-gate mutation.
- Stop: a new CLI command, writable operational registry, or second context
  builder is required.

### T-06 — Central integration and candidate verification

- Outcome: run the bounded central evidence stack, inspect exact changed paths,
  complete independent implementation review, and establish a reviewable tree.
- Dependencies: T-01…T-05 PASS.
- Write surface: cumulative ledger only; deterministic SHA regeneration is
  limited to the already-listed manifest.
- Verification seam: focused suites, resume regression, foundation/template
  integrity, full suite, clean temporary adoption plus Doctor, read-only and
  scope audits, `git diff --check`, and independent review.
- Stop: any regression, unauthorized path, authority leak, semantic routing,
  manifest mismatch, unresolved material review finding, or 07/08/09 drift.

### Central Implementation Candidate Review Gate

After T-06, stop. Independent/bounded review must find no material defect.
Separate owner authorization is required before staging/commit. Only the
resulting clean committed central candidate may be used for T-07/T-08.

### T-07 — Disposable Formal Readiness operation proof

- Outcome: from the exact committed candidate, create a disposable consumer
  fixture whose approved planning transition has projected Readiness in
  progress, exact
  `RUN_FORMAL_READINESS`, and `implementation_authorized = NO`; prove
  `FORMAL_READINESS_V1` matches and projects only its bounded read/readiness-
  evidence capabilities, stop, evidence, and next gate.
- Dependencies: clean committed central candidate and separate owner
  authorization for disposable proofs.
- Write surface: disposable temporary repository plus cumulative ledger; live
  Poker/mood have no read/write requirement.
- Verification seam: exact route/predicate/capabilities/output/exit; no product,
  Git, network, live-consumer, or automatic next-gate mutation; before/after
  disposable status and hashes.
- Stop: proof requires live consumer access, source changes after candidate
  commit, or readiness must borrow implementation authorization.

### T-08 — Disposable implementation and capability-separation proof

- Outcome: on the same candidate, prove both implementation authorization
  states for an exact implementation route and show that the authorized case
  still projects Git stage/commit as separately gated. Reuse a reduced
  Poker-shaped contract-closure fixture for the positive case and a reduced
  mood-shaped/no-active-Change case only as a supporting nearest-wrong
  discriminator.
- Dependencies: same gate as T-07; independent of T-07 after candidate/proof
  authorization exists.
- Write surface: disposable temporary repository plus cumulative ledger; live
  Poker/mood remain untouched.
- Verification seam: false implementation flag -> `NOT_AUTHORIZED`; true flag
  -> `MATCHED` with bounded product write but no Git grant; existing
  `planning-execute`/Contract Closure refs; mood-shaped context fails closed;
  before/after filesystem and Git evidence.
- Stop: a matched Git-checkpoint route becomes necessary, live consumer
  mutation is required, or any proof tries to stage/commit.

### T-09 — Completion Review

- Outcome: independently reconcile implementation and disposable evidence
  against all nine amended ACs, both approved amendment hashes, original
  authority lineage, exact candidate identity, scope, and 07/08/09 exclusions.
- Dependencies: T-01…T-08 PASS and no open material finding.
- Write surface: `PL-V39-07-COMPLETION-REVIEW-v1.md` only, plus final status in
  the existing cumulative ledger when required.
- Verification seam: AC 9/9 evidence matrix, spec/standards conformance, exact
  candidate SHA, live consumers unchanged/not accessed, and no persistent new
  authority/registry.
- Stop: any AC lacks direct evidence or source differs from the proven
  candidate.

## 12. Acceptance-Criteria Traceability

| AC | Primary implementation seam | Required discriminator | Tasks |
|---|---|---|---|
| AC-01 | downstream pure selector over one unchanged ResumeContext snapshot | one build/invocation; no extra scan/read/write; plain resume unchanged | T-01, T-03, T-05, T-06 |
| AC-02 | immutable exact operation/route map | stable exact match; zero/two; near-wrong; bounded provenance | T-01, T-02, T-03 |
| AC-03 | route-specific predicate after operation classification | readiness + auth false matches; implementation + false rejects; skill/prior guidance cannot elevate | T-02, T-03, T-05, T-07, T-08 |
| AC-04 | capability plus result/evidence projection | allowed/forbidden/separately gated capabilities and all bounded references present; no bodies copied | T-01, T-03, T-04, T-05 |
| AC-05 | finite failure model and exact exits | unmapped, ambiguous, stale/missing, route prerequisite, absent owner decision, invalid candidate/capability | T-01, T-02, T-03, T-05 |
| AC-06 | eight existing skills, four clarifications, conditional disciplines | canonical/adapter ownership; contract discipline versus explicit zero; no authority elevation | T-02, T-04, T-08 |
| AC-07 | existing resume/control/evidence surfaces | no registry/new skill/router; one ledger and one review; scope audit | T-04, T-05, T-06, T-09 |
| AC-08 | two materially different route proofs on one committed candidate | T-07 readiness; T-08 implementation false/true plus independent Git gating; reduced Poker/mood support | T-07, T-08 |
| AC-09 | fixed map and structural exclusions | no later-07 preflight platform, 08 eval/learning, or 09 compiler/orchestration surfaces | T-04, T-06, T-09 |

```text
AC_PLAN_COVERAGE: 9/9
orphan tasks: NONE
implementation task after T-09: NONE
```

## 13. Focused Verification and Failure Discriminators

### Focused model, route, and CLI suite

```text
uv run --frozen pytest tests/test_execution_guidance.py tests/test_cli.py -rA
```

Required cases include:

| Case | Exact expected result |
|---|---|
| valid Formal Readiness facts, implementation authorization false | `MATCHED / EXACT_OPERATION_BINDING / FORMAL_READINESS_V1` |
| exact readiness action with a non-Readiness lifecycle/stage | `NOT_AUTHORIZED / ROUTE_PREREQUISITE_NOT_MET` |
| valid implementation action, implementation authorization false | `NOT_AUTHORIZED / IMPLEMENTATION_NOT_AUTHORIZED` |
| valid implementation action, implementation authorization true | `MATCHED`; bounded product write; `GIT_STAGE` and `GIT_COMMIT` remain `REQUIRES_SEPARATE_AUTHORIZATION` |
| checkpoint skill present/requested without exact Git authority | no Git grant; no matched Git route in the pilot candidate set |
| valid current context with unknown action | `NO_APPLICABLE_OPERATION / UNMAPPED_OPERATION` |
| central/self-hosted `RUN_PL_V39_07_FORMAL_READINESS` action | `NO_APPLICABLE_OPERATION / UNMAPPED_OPERATION`; it is not an alias |
| case/prefix/suffix/fuzzy/alias near-match | `NO_APPLICABLE_OPERATION / UNMAPPED_OPERATION` |
| two injected materially valid exact bindings | `AMBIGUOUS_OPERATION / MULTIPLE_EXACT_BINDINGS` |
| malformed/over-bound/duplicate candidate or invalid capability definition | exact `MISSING_OR_UNUSABLE_CONTEXT` reason |
| missing/malformed/stale/superseded resume authority | first exact context failure |
| route-relevant blocker/prerequisite failure | route-specific `NOT_AUTHORIZED`, not a universal implementation check |
| prior matched provenance supplied as handoff/authority | rejected by the existing context contract |
| plain resume | byte/schema/exit-compatible existing behavior |

No test may assert help prose, formatting trivia, pytest rendering, or other
non-contractual presentation text.

### Resume regression

```text
uv run --frozen pytest tests/test_context_resume.py tests/test_central_resume_contract.py -rA
```

No PL-V39-06 schema change is expected. Determinism, bounded sources, path
safety, freshness, handoff non-elevation, and central resume behavior must pass.

### Managed template and skill ownership

```text
uv run --frozen pytest tests/test_field_control_pack_foundation.py tests/test_template.py -rA
```

The suite must derive structural facts from the actual managed files and SHA
manifest. It verifies three exact action producers, canonical skill ownership,
thin adapter pointers/descriptions, eight-skill count, checkpoint/Git
separation, conditional disciplines, and absence of new registries/routers/
lifecycles. It must not parse human failure rendering as machine state.

### Integration gate

```text
uv sync
uv run --frozen pytest
git diff --check
git status --short --untracked-files=all
```

Then adopt the exact candidate template into a temporary clean Git repository
and run `planning-lite doctor` there. Update behavior is unchanged, so a two-tag
update migration is not required unless actual implementation drifts into
update/ownership behavior.

## 14. Gate and Checkpoint Topology

```text
Definition Amendment APPROVED
+ Plan Amendment APPROVED
-> owner review and explicit approval of each amendment (COMPLETE)
-> bounded CURRENT alignment and owner-authorized Planning Authority checkpoint
-> read-only Formal Readiness
-> separate owner Execution authorization
-> T-01…T-06 central implementation and verification
-> CENTRAL IMPLEMENTATION CANDIDATE REVIEW GATE
-> separate owner checkpoint-commit authorization
-> clean committed central implementation candidate
-> separate owner authorization for disposable proofs
-> T-07 / T-08
-> T-09 Completion Review
-> separate owner closure decision
```

```text
amendment draft != amendment approval
Plan approval != implementation authorization
Formal Readiness READY != implementation authorization
implementation authorization != checkpoint commit authorization
matched Operation Guidance != execution or next-gate authorization
```

Formal Readiness requires the newly approved and committed Planning Authority,
but not a pre-existing implementation candidate. T-07/T-08 require the later
clean committed central implementation candidate.

## 15. Disposable Proof Strategy and Existing Fixtures

```text
POKER_FIXTURE_DISPOSITION: REDUCE
MOOD_FIXTURE_DISPOSITION: REDUCE
LIVE_POKER_MOOD_ACCESS: NOT REQUIRED / NOT AUTHORIZED
```

Poker remains useful as a mature exact implementation/Contract Closure shape,
but it no longer serves as the only positive architecture proof. Mood remains a
useful no-active-Change nearest-wrong shape, but it no longer owns the entire
second field task. The mandatory materially different pair is Formal Readiness
versus Implementation; independent Git non-authorization is projected within
the implementation proof.

Both formal proofs use disposable repositories created from the same separately
authorized clean committed candidate. They record exact candidate SHA,
commands, structured output, before/after status/hashes, and cleanup disposition
in the single ledger. Neither proof reads or mutates `D:\documents\poker` or
`D:\documents\mood` unless a later separate authorization explicitly changes
that boundary.

The local recommendation inbox pilot remains:

```text
PLANNING_LITE_LOCAL_RECOMMENDATION_INBOX_PILOT:
DEFERRED_TO_LATER_BOUNDED_07_FIELD_PROOF

INBOX_PILOT_READINESS:
READY_AFTER_CLARIFICATION
```

It is not needed to correct or prove the universal-authorization defect.

## 16. Evidence Economy

```text
one cumulative PL-V39-07-EXECUTION-LEDGER-v1.md for T-01…T-08
+
one PL-V39-07-COMPLETION-REVIEW-v1.md for T-09
```

No per-route receipt files, capability report, skill-normalization report,
decision log, or general receipt registry are created. The ledger records task
ID, execution baseline/revision when material, actual changed paths, exact
verification/evidence, PASS/FAIL/BLOCKED, material finding/stop gate, and links
only to independently valuable diagnostics.

## 17. Internal Sequence and Roadmap Boundary

```text
07-A Empirical grammar + authority reconciliation
     EVIDENCE COMPLETE / OWNER AMENDMENT APPROVED
-> 07-B Thin skill/policy normalization
-> 07-C Route-specific deterministic Operation Guidance
-> 07-D Derived binding + empirical proofs
```

No additional phase is introduced.

```text
ROADMAP_MAJOR_CHANGE_REQUIRED: NO
```

The current `PL-V39-07 — Execution Contracts, Skills, Checklists, and Routing`
already owns deterministic operation identity, thin skills, route-specific
authority, capability envelope, conditional disciplines, and derived
result/evidence guidance.

Boundary remains:

| Roadmap slice | Retained owner |
|---|---|
| PL-V39-07 | explicit deterministic operation semantics, thin skills, route predicates, capability envelope, conditional disciplines, derived result/evidence guidance, and bounded proofs |
| PL-V39-08 | evaluation, attempt lifecycle, task-verifier baseline snapshot, learning, PromptOps, quality scoring, and adaptive/semantic/model routing |
| PL-V39-09 | Context Compiler, AgentWorkPacket productization, orchestration, delegation, automatic chaining, and release automation |

General preflight-only operation productization remains a later bounded 07
Change. No boundary moves into this amendment.

## 18. Risks and Stop Conditions

Stop the affected task and use the approved amendment/adjudication path if:

- either approved amendment hash, active Change, Planning Authority, or current
  authority drifts;
- implementation requires changing `ResumeContextV1`, calling its builder
  twice, or accepting caller-supplied operation/authority/capability decisions;
- operation identity cannot be produced from the exact bounded mapping;
- a registry, recursive discovery, semantic/fuzzy/model classification,
  persistent result log, new skill/checklist/lifecycle/router/mode, or unlisted
  write path becomes necessary;
- a fifth skill needs semantic clarification or adapter content begins to own
  routing/authorization;
- a route would copy authority bodies, broaden the Plan/Envelope, or treat a
  separately gated capability as granted;
- a failure cannot obey the frozen precedence;
- Formal Readiness requires implementation authorization or implementation
  grants Git/network/live-consumer capability implicitly;
- full/focused verification, adoption/Doctor, or disposable proof finds a
  material regression;
- live Poker/mood, recommendation automation, general preflight platform,
  PL-V39-08 evaluation/learning, or PL-V39-09 orchestration becomes necessary;
  or
- source differs after the candidate commit used by T-07/T-08.

## 19. Owner Plan Amendment Decision and Next Gate

```text
PL_V39_07_IMPLEMENTATION_PLAN_AMENDMENT: APPROVED_BY_OWNER
Plan Amendment approved: YES / USER EXPLICIT / 2026-09-06
Definition Amendment approved: YES / USER EXPLICIT / 2026-09-06
RUNTIME_SEAM: KEEP
ROUTE_PREDICATE_INPUTS: SAME_RESUME_SNAPSHOT_ONLY
ROUTE_TIME_AUTHORITY_READS: NONE
ACTION_IDENTITY_NAMESPACE: FINITE_EXACT_MANAGED_IDENTITIES
GUIDANCE_COMMAND_MUTATION: READ_ONLY
production candidate bindings: 3
route families: 2
AC_PLAN_COVERAGE: 9/9
task count: 9
planned implementation/evidence paths: 22 / JUSTIFIED 22/22
canonical skills: 8 UNCHANGED
skills to clarify: 4
new skills: 0
new recommendation skill: NO
new registry: NO
Roadmap major change required: NO
07/08/09 boundary: PRESERVED
CURRENT: ALIGN TO NEW PLANNING-AUTHORITY CHECKPOINT GATE
amendment activation receipt: NOT REQUIRED / APPROVED AMENDMENTS + CURRENT ALIGNMENT
Planning Authority checkpoint: NOT CREATED
Formal Readiness: NOT RUN / REQUIRED AGAINST NEW COMMITTED AMENDED PLANNING AUTHORITY
implementation_authorized: NO
T-01…T-09: NOT STARTED
next owner gate: OWNER_AUTHORIZATION_NEW_PL_V39_07_PLANNING_AUTHORITY_CHECKPOINT
```

Owner approval of this Plan Amendment permits only the bounded `CURRENT`
alignment recorded by this governance step. It does not create the Planning
Authority checkpoint, run Formal Readiness, authorize implementation or
disposable proofs, stage, commit, or execute any later gate. Each remains
separate under the topology above.
