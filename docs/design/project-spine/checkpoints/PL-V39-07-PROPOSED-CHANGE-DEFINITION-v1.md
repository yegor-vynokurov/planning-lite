# PL-V39-07 Change Definition

## 1. Change Identity

- Change ID: `CHG-PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-001`
- Title: Deterministic Execution Guidance Binding
- Status: `APPROVED_BY_OWNER`
- Proposed on: `2026-09-05`
- Shaping baseline: `e6618cb974991a9e298615af3dec9a2467464ac0`
- Source Roadmap slice: `PL-V39-07`
- Owner approval: `USER / EXPLICIT — 2026-09-05`
- Activation: `ACTIVE / PLANNING_IN_PROGRESS`
- Implementation authorization: `NO`

Definition Gate result:

```text
OWNER_DEFINITION_DECISION: APPROVE
TIGHTENINGS: SEMANTIC_CLARIFICATION (4/4 applied)
scope change: NO
goal change: NO
AC count change: NO
Roadmap change: NO
```

This approved Definition is Change scope authority. It is not current-state or
execution authority and does not authorize implementation.

## 2. Problem

PL-V39-06 can deterministically recover bounded current facts, including the
next permitted action and implementation-authorization state. Planning Lite
also already has lifecycle gates, modes, workflows, an Execution Envelope,
structured blockers, canonical skills, conditional disciplines/checklists,
verification rules, and cumulative evidence surfaces.

The missing seam is the binding between them. Given the same explicit current
facts, agents can still have to infer which execution contract, procedure,
skill, or checklist applies. The current prose routers do not produce an
inspectable deterministic selection, and they do not make no-match,
ambiguity, missing-context, or not-authorized outcomes a testable result. This
creates avoidable re-reading and a risk of guessed procedure or authority.

## 3. Goal

Provide the smallest deterministic, fail-closed execution-guidance binding that
consumes the committed PL-V39-06 resume/current-authority facts and resolves
them to exactly one bounded existing guidance bundle when legal, or to an
explicit safe non-execution result when it cannot.

The result guides how already permitted work is performed. It never grants
permission, owns lifecycle state, or replaces an approved Definition, Plan,
Execution Envelope, checklist evidence, ledger, or review.

## 4. In Scope

- a bounded logical execution-contract representation that references existing
  authority and procedure surfaces rather than copying them;
- a candidate guidance set obtained only from an explicitly bounded existing
  managed set, explicit authoritative pointers, or a finite deterministic
  mapping; inability to establish that bounded set fails closed;
- deterministic selection from explicit structured current facts such as
  lifecycle stage, next permitted action, authorization state, artifact role,
  and explicit contract identity where present; an action class is legal input
  only when explicit in canonical/approved authority or derived by a finite
  exact canonical mapping;
- binding to one existing canonical procedure/workflow and, when applicable,
  an existing canonical skill and evidence-linked checklist;
- a new minimum-pilot skill or checklist only if a later approved
  Implementation Plan proves that no existing canonical surface can satisfy an
  AC, that the artifact is required for the minimum pilot, that it creates no
  new corpus/taxonomy/subsystem, and that it neither authorizes nor owns state;
- explicit precondition, permitted read/write scope, verification, stop,
  evidence, escalation, and next-gate references in the selected guidance;
- bounded inspectable provenance for a match: selected guidance/contract
  identity, source authority/procedure pointers, applicable source
  revision/lineage identity, and a bounded selection reason; this provenance is
  derived, non-authoritative, and non-persistent by default;
- fail-closed outcomes for no applicable contract, ambiguous routes, missing
  required context, and absent execution authorization;
- reuse of `ResumeContextV1`-level output, lifecycle/approval gates, Plan,
  Execution Envelope, current skills/workflows/disciplines, and cumulative
  evidence architecture;
- focused deterministic and nearest-wrong evidence, including mature
  Poker-shaped and early mood-shaped controlled fixtures; and
- only the minimum pilot semantics needed before PL-V39-08 evaluation.

## 5. Out of Scope

- a new lifecycle or current-state authority, execution-authority database,
  permission engine, global blocker registry, or parallel state file;
- changing owner approval, readiness, amendment, execution, checkpoint,
  completion-review, or closure semantics;
- expanding an approved Plan, Execution Envelope, write surface, tool/network
  capability, or verification authority;
- broad new skill/checklist/contract corpora or a parallel taxonomy where an
  existing canonical surface can be extended;
- skill usage analytics, automatic skill discovery, ranking, quality scoring,
  learning, adaptive or semantic routing, PromptOps, and policy optimization;
- embeddings, RAG, semantic memory, recommendation discovery/promotion, or a
  recommendation registry;
- model/vendor selection or an LLM classifier required for routing;
- Campaign Core generalization, multi-agent orchestration, delegation,
  scheduling, release orchestration, or autonomous workflow chaining;
- production Context Compiler work;
- live Poker/mood migration, live consumer mutation, or final external
  control-home placement;
- a task graph, Implementation Plan, Formal Readiness, implementation, or Git
  history/release operations in this Definition step; and
- prematurely fixing exact Python class names, CLI command names, directory
  layout, persisted registry format, or wire schema;
- recursive or implicit contract/skill/checklist discovery, broad repository or
  history scanning to find candidates, and loading all managed guidance merely
  to choose among it; and
- LLM classification, embeddings, semantic/fuzzy similarity, open-ended
  natural-language interpretation, or heuristic best-match routing.

## 6. Authority and Safety Invariants

1. `CURRENT` / consumer `ACTIVE` remains current lifecycle and state authority.
2. Approved Definition/Plan and explicit owner decisions remain scope and
   authorization context. Readiness remains distinct from execution approval.
3. Resume output and any guidance decision are derived views. Neither may
   elevate, revoke, or invent authorization.
4. An execution contract may narrow or reference authorized scope; it may never
   broaden the approved Plan or Execution Envelope.
5. A skill describes how; it does not authorize. A checklist binds procedure or
   evidence; it does not own state or replace acceptance criteria. Routing
   selects guidance; it does not select authority.
6. Candidate guidance comes only from an explicitly bounded managed set,
   explicit authoritative pointers, or a finite deterministic mapping. Failure
   to establish the set is a non-executing result, never a discovery fallback.
7. An action class is accepted only when authority states it explicitly or a
   finite exact canonical mapping derives it. Semantic, fuzzy, heuristic, or
   model-based classification is prohibited.
8. One explicit input state produces one stable result. Uncertainty fails safe;
   semantic/model interpretation is not a hidden fallback.
9. A matched result exposes bounded provenance sufficient to inspect and
   revalidate the selection. Provenance is derived, non-authoritative, and
   non-persistent by default; it is not registry state, execution authority, a
   second `CURRENT`, or a required persistent decision log.
10. Existing workflows, modes, skills, disciplines, gates, state ownership, and
   cumulative evidence surfaces are reused. New parallel limbs require a proven
   gap and are not implied by this Definition.
11. Campaign, recommendation, eval/learning, orchestration, release, and live
   consumer responsibilities retain their existing owners and gates.

## 7. Required Consumer Behaviors

For a mature Poker-shaped project, an agent can use bounded current facts to
identify one applicable procedure, its authorization prerequisite, scope,
verification, stop conditions, and next gate without reopening full execution
history. If those facts do not authorize execution, the result stops rather
than returning executable guidance.

For an early mood-shaped project with no active implementation or applicable
contract, the result explicitly defers. It does not create a Change, infer an
implementation route, or treat absence as permission.

These are fixture shapes, not authorization to read or mutate the live Poker or
mood repositories.

## 8. Failure Behavior

The implementation must distinguish conceptual outcomes equivalent to:

- one deterministic applicable match;
- no applicable contract;
- more than one materially valid route;
- action not authorized; and
- required current context missing, stale, or otherwise unusable.

Exact names are not frozen by this Definition. For every non-match outcome,
the observable behavior must be non-executing, explain the bounded reason, and
point to an existing legal escalation/current-authority seam. It must not guess
a procedure, silently choose among ambiguous routes, or repair scope.

## 9. Acceptance Criteria

### AC-01 — Resume/current-authority compatibility

The guidance mechanism consumes the committed PL-V39-06 schema-version-1
resume/current-authority facts without adding a history scan, semantic-retrieval
dependency, parallel current-state authority, or mandatory new persistent
handoff artifact. Its candidate set is limited to explicit authoritative
pointers, an explicitly bounded existing managed set, or a finite deterministic
mapping; it never scans a broader corpus to discover candidates.

### AC-02 — Deterministic bounded selection

For the same valid explicit input facts and the same canonical contract set, the
mechanism produces one stable, inspectable result. A legal matched result
identifies exactly one bounded execution-guidance bundle; selection does not
depend on conversational memory or LLM/embedding similarity. Action class is
accepted only when explicit in canonical/approved authority or derived through
a finite exact canonical mapping. The match exposes bounded guidance identity,
source pointers, applicable revision/lineage, and selection reason without
persisting a new authority.

### AC-03 — Authorization non-elevation

When implementation authorization is absent, contradictory, stale, or
insufficient for the selected action, the mechanism returns a non-executing
result. Neither route, skill, checklist, nor execution contract can grant or
infer permission or bypass an owner gate.

### AC-04 — Complete subordinate guidance

A matched bundle resolves or references the applicable procedure plus its
preconditions, allowed/forbidden scope, required verification, stop conditions,
evidence destination, escalation seam, and next gate. These values remain
bounded projections/references to approved authority and may not widen it. The
bundle also exposes derived, non-authoritative, non-persistent-by-default
provenance sufficient to inspect and revalidate the route.

### AC-05 — Safe no-match and ambiguity behavior

Controlled nearest-wrong cases prove distinguishable non-executing behavior for
no applicable contract, ambiguous route, and missing required context. No case
falls back to invented procedure, broad repository discovery, semantic routing,
fuzzy or heuristic classification, loading all candidates, or automatic
amendment. An action that has no finite exact classification returns a safe
non-execution result equivalent to no applicable contract or ambiguous route.

### AC-06 — Skill and checklist subordination

At least one minimum pilot route demonstrates precise activation of existing
canonical skill/checklist/workflow/discipline surfaces and evidence-bound
checklist applicability. Tests also demonstrate that skills do not authorize,
checklists do not own state or duplicate task acceptance criteria, and zero
applicable checklist is a legal explicit outcome where the contract does not
require one. A new minimum-pilot skill/checklist is legal only after an approved
Plan proves all five conditions in §4; Definition approval alone does not
authorize creating it.

### AC-07 — Existing-surface reuse and evidence economy

The solution reuses the existing lifecycle/gates, modes, workflows, Execution
Envelope, skills/adapters, conditional disciplines, Plan/task verification, and
cumulative progress/ledger plus final-review evidence model. It creates no
per-task receipt requirement, second router-owned state machine, or parallel
execution authority. Candidate selection is bounded explicitly and cannot use
recursive discovery or load an implicit corpus.

### AC-08 — Mature and early consumer discriminators

Controlled disposable fixtures prove both: (a) a mature authorized
Poker-shaped case selects the intended bounded guidance and preserves its next
gate; and (b) an early mood-shaped case with no active implementation safely
returns a non-execution result. The proofs do not modify live consumers and do
not require final control-home placement.

### AC-09 — 07/08/09 boundary preservation

Focused structural evidence proves the Change does not introduce scoring,
learning, adaptive/semantic/model routing, PromptOps, recommendation automation,
Campaign generalization, multi-agent orchestration, automatic delegation,
release chaining, or production Context Compiler behavior.

## 10. Evidence Strategy

If this Definition is later approved and planned, the smallest sufficient stack
is:

1. focused contract/model tests for determinacy and exact result shape;
2. authorization non-elevation and missing/stale-context discriminators;
3. matched, no-match, ambiguous, and nearest-wrong routing cases;
4. template/ownership tests proving skills, checklists, adapters, and routes stay
   subordinate to existing authority;
5. controlled Poker-shaped and mood-shaped disposable consumer proofs; and
6. a bounded regression/integrity pass selected by the eventual implementation
   blast radius.

Evidence should accumulate in the existing progress/Execution Ledger surface
and final review. Separate artifacts are justified only by an independently
valuable diagnostic result or an existing canonical requirement.

## 11. Deferred / Routed Items

- PL-V39-08: quality scoring, reusable eval extraction, learning, adaptive
  context or contract policy, semantic relevance, model/effort routing,
  PromptOps, optimization, and evidence-backed skill/checklist scale-out.
- PL-V39-09/later: production Context Compiler, multi-agent orchestration,
  delegation, scheduling, autonomous workflow/release chaining.
- Later owner decision: recommendation discovery/promotion/registry, live
  Poker/mood migration, and final external control-home placement.
- Not needed for this Change: embeddings/vector/RAG, semantic memory
  automation, episodic summary trees, utility/forgetting ledgers, graph stores,
  skill usage analytics, and Campaign Core generalization.

## 12. Next Gate After Definition Activation

```text
next gate: PREPARE_PL_V39_07_IMPLEMENTATION_PLAN
Definition status: APPROVED_BY_OWNER
Change activation: ACTIVE / PLANNING_IN_PROGRESS
Implementation Plan: NOT CREATED
Formal Readiness: NOT RUN
implementation_authorized: NO
```

The only next permitted action is preparation of one bounded Implementation
Plan under the existing lifecycle. No Formal Readiness or implementation action
follows automatically.
