# PL-V39-07 Definition Amendment v1

## 1. Amendment Identity

- Amendment ID: `PL-V39-07-DEFINITION-AMENDMENT-001`
- Change: `CHG-PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-001`
- Logical capability after amendment: `Deterministic Operation Guidance`
- Status: `APPROVED_BY_OWNER`
- Prepared on: `2026-09-06`
- Owner approval: `USER / EXPLICIT — 2026-09-06`
- Approval authority: `OWNER / EXPLICIT / EXERCISED`
- Lifecycle effect: `ACTIVE CHANGE REMAINS PLANNING_IN_PROGRESS / RENEWED READINESS REQUIRED`
- Implementation authorization: `NO`
- Formal Readiness: `NOT RUN / REMAINS PAUSED`

Owner decision recorded by this governance step:

```text
OWNER_DEFINITION_AMENDMENT_DECISION: APPROVE
A-01: SEMANTIC_CLARIFICATION / APPLIED
A-02: SEMANTIC_CLARIFICATION / APPLIED
A-03: SEMANTIC_CLARIFICATION / APPLIED
A-04: EXPLICIT_SCOPE_ACCOUNTING / APPLIED
```

This approval combines the predecessor Definition with this amendment as the
current Change scope authority. It does not authorize Formal Readiness,
implementation, disposable proofs, staging, commit, or any automatic next gate.

## 2. Bound Predecessor Authority

| Authority | Path / identity | SHA256 / revision |
|---|---|---|
| active Change | `CHG-PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-001` | established lineage; ID unchanged |
| approved predecessor Definition | `docs/design/project-spine/checkpoints/PL-V39-07-PROPOSED-CHANGE-DEFINITION-v1.md` | `654c854311dc69a4444cc019aa50f49a18c86eeb5d01ac8225196c8c20a8e627` |
| Definition activation | `docs/design/project-spine/checkpoints/PL-V39-07-DEFINITION-ACTIVATION-v1.md` | `c29f6b9416cc723ab45b73f36bc7ed769d19a02762f6e2b0adc82eaedd87b442` |
| approved predecessor Plan | `docs/design/project-spine/checkpoints/PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-IMPLEMENTATION-PLAN-v1.md` | `a09f4b42509f434fe56c35a8f47e8e16d76fdcc9644c4fb16a6efdf5499e6ae1` |
| predecessor Planning Authority | Git commit | `7e28a1967178f41fb6674c2a51a7896980bf5efb` |
| current-state authority at drafting baseline | `docs/design/project-spine/CURRENT.md` | `0f3692802d0f722d1f3bb87ad3bedeb03ae6e9e2a529e65b90b3e4532b5d6d92` |
| Roadmap authority at drafting baseline | `docs/design/project-spine/roadmap/ROADMAP.md` | `a440375b85a5cd990b8d2641f19857b1a3cf3b6189c0cc6ad04671279c0ea337` |

The predecessor Planning Authority remains immutable evidence. The predecessor
Definition plus this approved amendment form the combined Change scope
authority; unchanged predecessor clauses remain in force.

## 3. Bound Review Evidence

The following records are review evidence, not project authority:

| Evidence | SHA256 | Bound conclusion |
|---|---|---|
| `D:\documents\PL-V39-07-EMPIRICAL-SKILL-EXECUTION-SURFACE-PACK.md` | `bfdcdaeaadf5b4a3bee3111e9a653a02c01ff083cd9dfb51dba6436bdf685ff2` | exact empirical skill/execution surfaces |
| `D:\documents\PL-V39-07-RECOMMENDATION-SURFACE-PACK.md` | `7b7c012b13ac48c84d8cdb72339c85a5cf780cdf6567a63414495e2cc518f584` | recommendation surfaces and boundaries |
| `D:\documents\PL-V39-07-EMPIRICAL-SKILL-POLICY-CHECKLIST-RECONCILIATION.md` | `65497c65282db94c7f23e5285b9ef5aaa5a86e03846ace685ce0cad60b90e36e` | `PASS_AMENDMENT_RECOMMENDED` |
| `D:\documents\PL-V39-07-SUPPORT-EVIDENCE-PACK.md` | `16ea77f7bc11bca96902e0ff29344a8378562be8128f20badd018c2a0428af26` | 12/12 support files inspected; zero deferred |
| `D:\documents\PL-V39-07-SUPPORT-AWARE-ARCHITECTURE-ADDENDUM.md` | `ce898c6a39a0806e7a7e1dbd08be868f067345e90a1cb3299628821cfcd26977` | `CONFIRMS_CURRENT_AMENDMENT` |

## 4. Reason for Amendment

The predecessor Definition models absent implementation authorization as a
universal reason to return non-executing guidance. The approved Plan makes that
rule operational by evaluating `implementation_authorized` before selecting an
operation and by limiting its candidate set to two implementation actions.

That model is materially incomplete. Planning, Formal Readiness, read-only
review/adjudication, session checkpointing, recommendation work, Completion
Review, and owner closure may each be legal while implementation authorization
is `NO`, subject to their own workflow and owner gates. Conversely,
implementation authorization does not authorize Git staging/commit, network or
external access, live-consumer mutation, proof execution, or closure.

The smallest coherent correction is therefore:

```text
classify the exact legal operation first
-> select one bounded route
-> evaluate that route's exact authority predicate
-> project only capabilities authorized for that operation
-> return one derived result/evidence contract
```

This is a semantic scope correction. It cannot be performed as an
implementation detail under the predecessor Definition/Plan and requires owner
approval plus renewed planning authority and Formal Readiness.

## 5. Amended Goal and Logical Name

Within the established Change lineage, provide the smallest deterministic,
fail-closed **Operation Guidance** binding that consumes one committed
PL-V39-06 `ResumeContextV1`/current-authority snapshot, identifies the exact
legal operation from a finite exact mapping, evaluates the selected route's own
authority predicate, and returns exactly one bounded existing guidance bundle
when authorized or one explicit safe non-match/non-authorization result.

`OperationGuidance` is the logical capability name because the selected
operation may be Planning, Readiness, Review, Implementation, or another legal
non-implementation class. The established Change ID remains unchanged, and
this amendment does not require a runtime filename or public-symbol rename.

The result guides an already legal operation. It never grants permission,
advances a lifecycle, executes a next gate, owns current state, or replaces the
approved Definition/Plan, workflow, Execution Envelope, evidence, or owner
decision.

## 6. Preserved Operational Grammar

```text
current authority + explicit request
-> exact legal operation
-> mode / thin skill capability
-> one authoritative workflow
-> route-specific authority predicate
-> applicable policies
-> zero-or-more conditional disciplines/checklists
-> exact task binding + capability envelope
-> verification + result/evidence contract
-> STOP / descriptive next gate
-> derived non-authoritative OperationGuidance / work packet
```

No layer may silently acquire permission owned by another layer. A skill
describes how; a workflow owns procedure and route entry/stop/resume semantics;
policy owns cross-operation invariants; a discipline owns reusable conditional
verification; task binding owns exact IDs, revisions, paths, commands, and
operation-specific bounds; authority remains in current state, approved
artifacts, lifecycle gates, and explicit owner decisions.

## 7. Route-Specific Authority Model

The guidance mechanism must evaluate these facts separately:

```text
operation identity
current lifecycle and next-action facts
workflow entry prerequisites
required owner decision, if any
requested capability class
operation-specific authorization outcome
```

The logical outcome set must be equivalent to:

```text
AUTHORIZED_FOR_THIS_OPERATION
NOT_AUTHORIZED
MISSING_OR_UNUSABLE_CONTEXT
NO_APPLICABLE_OPERATION
AMBIGUOUS_OPERATION
```

Exact runtime spelling remains a Plan/implementation contract. The mechanism is
a finite selector, not a permission database. It may report only the authority
facts and route predicates bound to the current invocation.

The owning workflow validates and owns upstream prerequisites, emits the
canonical lifecycle/stage/next-action projection, and `ACTIVE`/current authority
owns that projection. `ResumeContextV1` carries it; Operation Guidance consumes
it.

```text
ROUTE_PREDICATE_INPUTS: SAME_RESUME_SNAPSHOT_ONLY
```

The selector must not reopen Definition, Plan, or `readiness.md`; rerun
Readiness; infer approval from prose; perform another context build; or perform
additional route-time authority reads. A fact may participate only when it is
observable in the same validated ResumeContext selected-source projection. If a
required predicate fact is not observable there, the route fails closed and
requires a later owner amendment; `ResumeContextV1` is not expanded by this
Change.

`implementation_authorized = true` remains mandatory for implementation and
product-write routes. It is not required for a legal read-only/planning/
readiness/review route unless that selected workflow expressly requires it.
Operation classification must therefore precede evaluation of implementation
authorization.

## 8. Mandatory Capability Envelope

Every selected route must project the bounded capabilities material to the
operation. The logical model must be able to distinguish, without requiring a
universal persistent enum:

```text
READ
GOVERNANCE_WRITE
PRODUCT_WRITE
GIT_STAGE
GIT_COMMIT
NETWORK / EXTERNAL_ACCESS
DISPOSABLE_CONSUMER_MUTATION
LIVE_CONSUMER_MUTATION
```

For each material capability the result must distinguish an allowed capability
from one that is forbidden or requires a separate authority. Absence of a
capability grant is never inferred as permission.

```text
PRODUCT_WRITE authorized != GIT_STAGE or GIT_COMMIT authorized
implementation authorized != NETWORK / EXTERNAL_ACCESS authorized
SESSION_CHECKPOINT requested != GIT_STAGE or GIT_COMMIT authorized
disposable proof authorized != LIVE_CONSUMER_MUTATION authorized
```

The projection may narrow an approved route/task. It may never broaden its
workflow, approved Plan, Execution Envelope, or explicit owner authorization.

Capability states describe the envelope of the selected separately governed
operation under current authority. They never describe capabilities that the
guidance command itself may exercise.

```text
GUIDANCE_COMMAND_MUTATION: READ_ONLY
```

For example, `PRODUCT_WRITE = ALLOWED` means that the separately invoked,
already authorized implementation operation has bounded product-write
authority. `GOVERNANCE_WRITE = ALLOWED` for Formal Readiness describes that
workflow's bounded evidence/state surface. In both cases `planning-lite resume
--guidance` remains mutation-free.

## 9. Git Mutation and Checkpoint Boundary

```text
SESSION_CHECKPOINT != AUTHORIZED_GIT_CHECKPOINT_COMMIT
```

A session or planning checkpoint may record and preserve current durable state
under its workflow. It does not create standing Git staging or commit
permission. `GIT_STAGE` and `GIT_COMMIT` require exact route/task-specific owner
authority, bounded paths, and their own result evidence.

The `planning-checkpoint` skill remains a thin procedure entrypoint. Its
activation cannot authorize Git mutation. A matched implementation route must
explicitly show that Git commit is not granted when only product-write
authorization exists.

## 10. Mandatory Result / Evidence Contract

Each result must expose or reference, where applicable:

```text
selected operation identity
selected route identity
authority-predicate outcome
allowed / forbidden / separately-gated capability projection
success or failure result identity
skill, workflow, policy, and conditional discipline references
task and verification references
evidence destination or evidence limitation
STOP reason
descriptive next gate and next-gate owner
bounded provenance
```

References are preferred over copied bodies. The result is derived,
non-authoritative, non-persistent by default, and reconstructable from the same
current input. It is not a receipt registry or durable permission token.

```text
evidence != authorization
next gate != automatic execution of the next gate
```

Existing task evidence destinations and the cumulative ledger/final review
remain the evidence owners.

## 11. Minimum Pilot Route Families

The amended pilot must include only the smallest route set that discriminates
the corrected architecture:

1. **Formal Readiness** — a legal non-implementation route that may match when
   the canonical lifecycle/action projection produced after Plan approval is
   usable while `implementation_authorized = NO`;
2. **Implementation** — retain the two predecessor exact implementation
   bindings, both of which require `implementation_authorized = YES` and an
   exact authorized task/action.

The mandatory contrasting cases are:

```text
FORMAL_READINESS
+ canonical Readiness lifecycle/action produced after Plan approval
+ implementation_authorized = NO
-> AUTHORIZED_FOR_THIS_OPERATION

IMPLEMENTATION
+ otherwise valid implementation action
+ implementation_authorized = NO
-> NOT_AUTHORIZED

IMPLEMENTATION
+ implementation_authorized = YES
+ no separate Git commit grant
-> authorized implementation guidance
   with GIT_COMMIT not granted
```

No matched Git-checkpoint route is required for the minimum pilot. Independent
Git authority is proven by the capability projection, the checkpoint skill/
workflow boundary, and negative discriminators. Adding another route only to
increase route count would not improve the architectural proof.

The selector does not reopen or independently validate Definition/Plan bodies.
`CHANGE_PLANNING.md` owns the approval-gated transition and exact readiness
action producer; `ResumeContextV1` carries that current lifecycle/action
projection. Missing, contradictory, stale, or otherwise unusable current
projection fails closed through the existing context and route predicates.

The candidate set remains finite, exact, bounded, non-discovering, and free of
semantic/fuzzy/model classification. The Plan must freeze exact candidate
identities and their existing authoritative producers or bounded producer
clarifications.

`RUN_FORMAL_READINESS` is the exact managed consumer lifecycle identity
introduced by the bounded `CHANGE_PLANNING.md` producer clarification. It is not
an alias for the central/self-hosted action
`RUN_PL_V39_07_FORMAL_READINESS` or for any other project-specific string.

```text
ACTION_IDENTITY_NAMESPACE: FINITE_EXACT_MANAGED_IDENTITIES
```

There is no project-ID stripping, normalization, alias, prefix/suffix, or fuzzy
equivalence. Any project-specific current action not separately present in the
finite candidate set returns `NO_APPLICABLE_OPERATION`. The central
self-hosted `CURRENT.md` does not need to match the managed consumer identity.

## 12. Skill, Workflow, Policy, and Discipline Boundary

All eight current canonical skills remain. No skill is added, removed, merged,
split, or deprecated.

Exactly four thin skill contracts may receive bounded clarification:

- `planning-audit`: read-only readiness/review/adjudication uses the selected
  workflow's route-specific authority and does not borrow implementation
  authorization;
- `planning-checkpoint`: session/state checkpointing is distinct from
  separately authorized Git mutation;
- `planning-dialogue`: non-mutating exploration cannot silently promote a
  recommendation or begin governed work;
- `planning-plan`: Definition/Plan/recommendation work uses its planning
  workflow gates and does not authorize production work.

The other four remain unchanged:

```text
planning-execute
planning-git-review
planning-quick-fix
planning-recover
```

A skill remains approximately: identity, trigger, anti-trigger, legal operation
classes, authority-seam and workflow references, capability profile, policy and
conditional-discipline references, evidence expectation, STOP/escalation seam,
and explicit non-ownership of the next gate. This logical contract does not
approve a new machine schema.

Workflow continues to own procedure, entry/preconditions, operation-specific
stop/resume, and transition semantics. Policy continues to own
cross-operation invariants. Workflow/task facts select zero or more
disciplines; zero is legal, and a discipline never authorizes. Stable checks
remain inline until repeated use justifies extraction.

No `PlaybookEngine`, policy registry, permission registry, checklist registry,
or new lifecycle is in scope.

## 13. Amended Scope and Unchanged Boundaries

The current Change owns only:

```text
deterministic bounded Operation Guidance
+ route-specific authority predicates
+ bounded capability projection
+ thin skill/workflow/policy/discipline/task/evidence references
+ explicit result/evidence/STOP/next-gate projection
+ fail-closed deterministic behavior
```

It does not own a recommendation platform, general task compiler, general
preflight platform, evaluation framework, learning system, or orchestration.

The following are explicitly routed out:

| Finding / capability | Destination |
|---|---|
| general preflight-only operation profile | later bounded PL-V39-07 Change |
| local recommendation inbox pilot | `LATER_BOUNDED_PL_V39_07_FIELD_PROOF`; current readiness remains `READY_AFTER_CLARIFICATION` |
| attempt lifecycle | PL-V39-08 |
| task-verifier baseline snapshot | PL-V39-08 |
| quality scoring, learning, PromptOps, adaptive/semantic/model routing | PL-V39-08 |
| Context Compiler and AgentWorkPacket productization | PL-V39-09 |
| multi-agent orchestration, delegation, automatic chaining, release automation | PL-V39-09/later |

Recommendation promotion/runtime automation, live Poker/mood migration,
Campaign generalization, embeddings/RAG, broad skill/checklist corpora, and a
new persistent registry remain excluded.

```text
ROADMAP_MAJOR_CHANGE_REQUIRED: NO
07_08_09_BOUNDARY: PRESERVED
```

The approved Plan Amendment expands the planned implementation/evidence write
surface from 10 predecessor paths to 22 exact paths:

```text
PLANNED_WRITE_SURFACE_CHANGE: 10 -> 22
CLASS: MATERIAL_BUT_BOUNDED_BY_APPROVED_AMENDMENT
JUSTIFICATION: 22/22 paths trace to an amended AC and task
```

The expansion is intentional: it covers route-specific operation semantics,
capability/result projection, four canonical skill clarifications, four thin
adapter alignments, and the exact managed workflow/Git/checkpoint ownership
clarifications. It does not change the nine ACs, nine tasks, three candidate
bindings, two route families, eight-skill corpus, Roadmap structure, or
07/08/09 boundary.

The existing Roadmap item `PL-V39-07 — Execution Contracts, Skills,
Checklists, and Routing` owns the corrected explicit semantics. No Roadmap edit
or additional internal phase is required.

## 14. Acceptance Criteria Reconciliation

```text
AC_COUNT: 9 UNCHANGED
```

### AC-01 — Resume/current-authority compatibility

Preserve the predecessor criterion, replacing execution-only naming with
Operation Guidance where needed. The mechanism still consumes one unchanged
committed `ResumeContextV1` snapshot, performs no history/semantic retrieval or
recursive discovery, and creates no second current-state or persistent handoff
authority.

### AC-02 — Deterministic bounded operation selection

For the same usable explicit input facts and finite canonical candidate set,
the mechanism produces one stable inspectable result. It classifies the exact
operation before authority evaluation, selects exactly one route or fails
closed, and exposes bounded route/provenance identity without semantic, fuzzy,
heuristic, model, conversational-memory, or discovery fallback.

### AC-03 — Route-specific authorization non-elevation

The selected route evaluates only its exact authority predicate. A Formal
Readiness route can be authorized while implementation authorization is false;
an implementation/product-write route cannot. Skill, workflow, discipline,
candidate presence, prior guidance, or one granted capability cannot elevate
or substitute for a missing owner decision or different capability grant.

### AC-04 — Complete subordinate Operation Guidance

A matched result references the applicable mode, skill, workflow, policies,
zero-or-more disciplines, exact task binding, preconditions, capability
envelope, verification, result/evidence contract, STOP/escalation seam, and
descriptive next gate. Allowed, forbidden, and separately gated material
capabilities are explicit. All values remain bounded derived references and may
not widen authority.

### AC-05 — Safe operation no-match, ambiguity, and failure behavior

Controlled nearest-wrong cases prove distinct non-executing results for no
applicable operation, ambiguous operation, missing/unusable current context,
route not authorized, invalid/out-of-bound candidate, and inconsistent
capability contract. The first applicable deterministic failure identity wins;
no fallback invents a route, repairs scope, scans a broader corpus, or executes
a next gate.

### AC-06 — Thin skill and conditional-discipline subordination

All eight canonical skills remain; only the four named contracts receive
bounded trigger/authority/capability clarification. At least one route proves a
discipline reference and one proves an explicit zero-discipline result. Skills
and disciplines never authorize, own current state, duplicate workflow/task
acceptance criteria, or acquire next-gate ownership. Canonical skill bodies own
semantics; host adapters remain aligned thin projections.

### AC-07 — Existing-surface reuse and evidence economy

Preserve the predecessor criterion. Reuse lifecycle/gates, modes, workflows,
policies, Execution Envelope, skills/adapters, conditional disciplines,
`ResumeContextV1`, cumulative Execution Ledger, and final Completion Review.
Create no per-route receipt forest, second router, registry, decision log, or
parallel authority.

### AC-08 — Materially different operation-family discriminators

On one exact committed candidate, disposable fixtures prove at least: (a) a
canonical Plan-approval-to-Readiness projection matches with implementation
authorization false;
(b) an otherwise valid implementation route is not authorized when that flag
is false; and (c) an authorized implementation route can permit bounded product
write while Git commit remains ungranted. Existing Poker-shaped contract
closure and mood-shaped no-active-Change cases may be reduced and reused as
supporting positive/nearest-wrong fixtures, but they are not the sole
architecture discriminators. No live consumer is mutated.

### AC-09 — 07/08/09 boundary preservation

Preserve the predecessor criterion and additionally prove that attempt
lifecycle, task-verifier snapshotting, general preflight productization,
recommendation automation, learning/scoring/PromptOps, production work-packet
compilation, orchestration, and release automation are absent.

## 15. Evidence Strategy Delta

After later Formal Readiness and separate Execution authorization, verification
must cover:

1. exact operation-before-authorization ordering;
2. Formal Readiness match with implementation authorization false;
3. implementation non-authorization with the same false flag;
4. authorized implementation with Git stage/commit explicitly not granted;
5. finite zero/one/multiple and invalid/out-of-bound candidates;
6. missing, stale, blocked, contradictory, or unusable current context;
7. all eight skills preserved, four bounded canonical/adapter clarifications,
   zero-or-more disciplines, and no new registry;
8. same-snapshot, no-extra-read, no-write, exact-output, and plain-resume
   compatibility;
9. disposable cross-route proofs from one clean committed candidate; and
10. full bounded regression, template integrity, adoption/Doctor, scope, and
    07/08/09 exclusion evidence at the existing gates.

Evidence accumulates in one Execution Ledger plus one final Completion Review.
No new receipt subsystem is authorized.

## 16. Internal Sequence

```text
07-A Empirical grammar + authority reconciliation
     EVIDENCE COMPLETE / OWNER AMENDMENT APPROVED

07-B Thin skill/policy normalization
-> 07-C Route-specific deterministic Operation Guidance
-> 07-D Derived binding + empirical proofs
```

The sequence is unchanged. Capability/result clarification belongs within the
existing B/C/D responsibilities and does not create another dependency phase.

## 17. Owner Amendment Decision and Next Gate

```text
PL_V39_07_DEFINITION_AMENDMENT: APPROVED_BY_OWNER
amendment approved: YES / USER EXPLICIT / 2026-09-06
predecessor Definition status: APPROVED_BY_OWNER / UNCHANGED
active Change ID: UNCHANGED
AC count: 9
planned implementation/evidence paths: 22 / JUSTIFIED
Roadmap major change required: NO
07/08/09 boundary: PRESERVED
CURRENT: ALIGN TO NEW PLANNING-AUTHORITY CHECKPOINT GATE
Formal Readiness: NOT RUN / REQUIRED AGAINST NEW COMMITTED AMENDED PLANNING AUTHORITY
implementation_authorized: NO
next owner gate: OWNER_AUTHORIZATION_NEW_PL_V39_07_PLANNING_AUTHORITY_CHECKPOINT
```

This owner approval authorizes only the bounded governance alignment required by
the existing amendment lifecycle. The Plan Amendment has its own explicit
approval record. Neither approval runs Formal Readiness, authorizes
implementation, or authorizes staging/commit.
