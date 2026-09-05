# PL-V39-07 Authority and Surface Discovery

## 1. Review Identity

- Review type: bounded discovery and scope shaping
- Review date: `2026-09-05`
- Repository: `D:\documents\planning-lite`
- Baseline HEAD: `e6618cb974991a9e298615af3dec9a2467464ac0`
- Branch: `reconcile/current-design-spine-2026-08-25`
- Preflight status: `CLEAN`
- PL-V39-06: `CLOSED / COMPLETE`
- PL-V39-07: `NOT STARTED / NOT AUTHORIZED`
- Shaping verdict: `READY_FOR_OWNER_DEFINITION_REVIEW`

This review is discovery only. It does not approve or activate a Change, create
an Implementation Plan, run Formal Readiness, or authorize implementation.

## 2. Current Authority Baseline

The central resume authority remains
`docs/design/project-spine/CURRENT.md`. Its current contract says:

```text
active_change: NONE
lifecycle_gate: PLANNING_IN_PROGRESS
implementation_authorized: NO
blockers: NONE
next_permitted_action: PLAN_NEXT_PL_V39_07_SLICE
last_transition_receipt: docs/design/project-spine/checkpoints/PL-V39-06-COMPLETION-REVIEW-v1.md
```

The owning Roadmap section is `PL-V39-07 — Execution Contracts, Skills,
Checklists, and Routing`. Its transition rule is a minimum stable pilot in 07,
qualified evaluation and evidence-backed scale-out in 08, and orchestration only
later. The Roadmap label is broader than the smallest useful Change, but is not
semantically inconsistent with it.

The closed PL-V39-06 contract contributes a deterministic, bounded, read-only
resume view. Its schema-version-1 output already carries project identity,
current Change and lifecycle facts, implementation authorization, blocker,
next permitted action, active context pointer, source revision, freshness, and
bounded authority/lineage references. Handoff validation cannot elevate or
revoke current authorization. PL-V39-07 must consume this view; it must not add
a second discovery scan, memory store, or current-state authority.

## 3. Existing Execution-Control Surfaces

The inventory below groups closely coupled files as one surface. There are 21
materially relevant surface groups.

| ID | Existing surface | Classification | Role | Disposition for 07 |
|---|---|---|---|---|
| S-01 | central `CURRENT.md`; consumer `.planning/ACTIVE.md` | `CANONICAL_AUTHORITY` | defines current state and next legal action | `KEEP_AND_REUSE` |
| S-02 | Project Spine Roadmap §9 / transition rules | `CANONICAL_AUTHORITY` | defines direction and slice boundary | `KEEP_AND_REUSE` |
| S-03 | approved Change Definition, Plan, amendments, and explicit owner authorization | `CANONICAL_AUTHORITY` | defines scope and supplies authorization context | `KEEP_AND_REUSE` |
| S-04 | `CHANGE_LIFECYCLE.md`; `APPROVAL_GATES.md` | `CANONICAL_AUTHORITY`, `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | defines lifecycle and authorization gates | `KEEP_AND_REUSE` |
| S-05 | `tasks.md`, `progress.md`, Execution Ledger practice, and `review.md` / Completion Review | `OPERATOR_GUIDANCE`, `MANAGED_TEMPLATE_POLICY` | records task state and compact evidence; does not authorize | `KEEP_AND_REUSE` |
| S-06 | `ROOT_ROUTER.md` | `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | selects one mode/workflow from explicit current facts | `EXTEND` only at the narrow guidance-binding seam; do not add state |
| S-07 | `MODE_ROUTER.md`; `modes/{PLAN,EXECUTE,AUDIT,...}.md` | `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | distinguishes planning, implementation, review, and recovery behavior | `CLARIFY_ONLY`; no new universal mode |
| S-08 | `CHANGE_EXECUTION.md`; change-local `context.md` Execution Envelope and structured blocker | `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | explains execution; defines bounded read/write/tool scope, verification, stops, and local blockers | `EXTEND` only enough to expose/reuse a selectable execution contract |
| S-09 | `CHANGE_READINESS.md`; `readiness.md` | `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | defines exhaustive preconditions and readiness evidence; does not authorize | `KEEP_AND_REUSE` |
| S-10 | `CHANGE_PLANNING.md`; `plan.md`; `tasks.md`; `requirements-checklist.md` | `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | binds seams, dependencies, verification, and AC traceability | `EXTEND` only if the pilot needs an explicit checklist binding; do not duplicate ACs |
| S-11 | `CHANGE_AMENDMENT.md` | `MANAGED_TEMPLATE_POLICY` | escalates material contradiction or scope drift | `KEEP_AND_REUSE` |
| S-12 | `CHANGE_CLOSURE.md`; `review.md` | `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | completion review, evidence reconciliation, and owner closure | `KEEP_AND_REUSE` |
| S-13 | `SESSION_CHECKPOINT.md`; `progress.md` | `MANAGED_TEMPLATE_POLICY` | preserves resumable state and meaningful cumulative evidence | `KEEP_AND_REUSE` |
| S-14 | `CONTEXT_POLICY.md`; `STATE_OWNERSHIP.md` | `CANONICAL_AUTHORITY`, `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | limits context and prevents derived guidance/evidence from becoming authority | `CLARIFY_ONLY` if the new derived decision needs an explicit ownership statement |
| S-15 | canonical `.planning/skills/*/SKILL.md` including `planning-execute`; skills README | `MANAGED_TEMPLATE_POLICY` | reusable thin routes to modes/workflows; never grants permission | `CLARIFY_ONLY`; reuse existing skill before adding one |
| S-16 | `.agents/skills/*` wrappers and adapter registry/guides | `OPERATOR_GUIDANCE`, `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | client-specific discovery/invocation of canonical skills | `KEEP_AND_REUSE`; no adapter-owned routing logic |
| S-17 | `SKILL_USAGE_LOGGING.md` | `OPERATOR_GUIDANCE` | optional non-authoritative observability | `NOT_RELEVANT_TO_07` |
| S-18 | `CONTRACT_CLOSURE.md`; `DELIVERY_SLICES.md`; `CODE_REVIEW.md` | `MANAGED_TEMPLATE_POLICY`, `TESTED_CONTRACT` | reusable conditional procedure/checklist semantics | `KEEP_AND_REUSE`; load only when applicable |
| S-19 | `src/planning_lite/context.py`; `planning-lite resume` | `RUNTIME_ENFORCEMENT`, `TESTED_CONTRACT` | derives and validates bounded `ResumeContextV1`-level facts without writes | `KEEP_AND_REUSE` as input; no ResumeContext authority expansion |
| S-20 | `test_context_resume.py`, `test_cli.py`, template/foundation tests | `TESTED_CONTRACT` | owns resume determinacy, non-elevation, template topology, and deferred-runtime boundaries | `EXTEND` with focused route discriminators if the Definition is approved |
| S-21 | `src/planning_lite/campaign/**` Campaign Core | `DEFERRED / EXPERIMENTAL` for this slice | opt-in experiment execution/journaling; explicitly does not authorize release | `NOT_RELEVANT_TO_07`; do not generalize it into lifecycle execution |

Runtime enforcement relevant to the 07 seam is currently one integrated surface:
the resume builder/validator exposed by the CLI. It validates current facts,
freshness, bounded paths, and authorization non-elevation. Current routing,
workflow, skills, checklists, and execution-envelope rules are managed template
policy backed by structural tests; no runtime selector binds them to the resume
result.

The current canonical authority groups relevant to selection are five: current
state (`CURRENT`/`ACTIVE`), the Roadmap direction, approved Definition/Plan plus
owner decisions, lifecycle/approval-gate policy, and state/context ownership
policy. Execution ledgers, reviews, resume output, routes, skills, and
checklists remain evidence or derived guidance, not additional authority.

## 4. Capability Matrix

| Capability | Exists? | Where | Authority / enforcement | Real gap? |
|---|---|---|---|---|
| determine next permitted action | Yes | `CURRENT` / `ACTIVE`; resume output | canonical state; runtime-derived view | No |
| determine whether execution is authorized | Yes | owner decision, `APPROVAL_GATES`, `ACTIVE`, resume validation | canonical authority plus runtime non-elevation | No |
| bind action to execution procedure | Partial | `ROOT_ROUTER`, `MODE_ROUTER`, skills, named workflows | deterministic prose policy only | **Yes:** no inspectable deterministic binding result from current facts |
| select relevant execution contract | Partial | approved Plan, Execution Envelope, `CHANGE_EXECUTION` | contract content exists but selection identity is implicit | **Yes:** one bounded contract bundle is not deterministically selected |
| select relevant skill/checklist | Partial | canonical skills, disciplines, AC trace checklist | explicit/manual activation; no applicability decision | **Yes:** no safe deterministic binding, including legal no-match |
| define preconditions | Yes | Plan, Readiness, Approval Gates, Execution Envelope | authority/policy | No new semantics; selected guidance must reference them |
| define stop conditions | Yes | gates, `CHANGE_EXECUTION`, amendments, structured blocker | authority/policy; structurally tested | No new semantics; selected guidance must preserve them |
| define write surfaces | Yes | approved Plan and Execution Envelope | approved scope projected into current context | No |
| define required verification | Yes | Plan, tasks, Readiness, execution and closure workflows | approved scope/policy | No; selector must not broaden or replace it |
| distinguish planning vs implementation vs review | Yes | lifecycle, gates, modes, skills | authority/policy | No |
| escalate ambiguous/out-of-scope work | Yes | amendment workflow, blocker locality, recovery | policy | No new escalation system; routing must fail safe into it |
| preserve evidence without per-task artifact explosion | Yes | cumulative `progress.md` / Execution Ledger plus final review | evidence policy | No |

Only the three adjacent partial rows form the actual 07 capability gap. They are
one seam, not three new subsystems.

## 5. Contract / Skill / Checklist / Routing Boundary

| Concept | Bounded meaning | Must not do |
|---|---|---|
| Execution contract | rule bundle for one class of permitted work: authority prerequisites, scope, procedure references, verification, stops, evidence, and next gate | own lifecycle state or grant permission |
| Skill | reusable procedure/competence for how to perform recurring work | authorize work or duplicate canonical workflow logic |
| Checklist | bounded evidence-linked procedure/verification list | own current state, replace task ACs, or prove approval by self-report |
| Routing | choose applicable subordinate guidance from explicit current facts | invent facts, infer authorization, use semantic similarity, or become a state machine |

Authority topology remains:

```text
CURRENT / consumer ACTIVE
  -> current lifecycle and state authority

approved Definition / Plan + explicit owner decisions
  -> scope and authorization context

Execution Ledger / Review
  -> evidence

PL-V39-06 resume output
  -> derived bounded continuation

PL-V39-07 route / contract / skill / checklist
  -> subordinate execution guidance only
```

## 6. Gap Type and Required Change Class

| Claimed gap | Required class | Reason |
|---|---|---|
| deterministic current-action to guidance binding | `SCHEMA/MODEL` + `RUNTIME` + focused tests | two implementers/agents need the same inspectable outcome from the same explicit facts; prompt-only inference cannot prove ambiguity/no-match behavior |
| selectable execution-contract projection | `TEMPLATE_CONTRACT` + `SCHEMA/MODEL` | existing Plan, envelope, workflow, and gates should be referenced as one bounded logical bundle, not copied into a second authority |
| skill/checklist applicability | `TEMPLATE_CONTRACT` + focused tests | existing skill and discipline bodies can be reused; a minimum pilot needs explicit applicability/evidence binding, including zero applicable checklist |
| safe route failure result | `SCHEMA/MODEL` + focused tests | ambiguity, missing context, no match, and absent authorization must be distinguishable and fail closed |
| lifecycle, approval gates, write-surface ownership, verification authority, evidence ledger | `NO_CHANGE` or at most `DOC_CLARIFICATION` | these contracts already exist and are not the missing capability |
| new CLI command | `NO_CHANGE` at Definition stage | a runtime seam is required, but an additional command is not yet proven necessary; the Plan may bind the smallest existing operator seam |
| skill analytics, semantic discovery/ranking, adaptive routing | `NO_CHANGE` in 07 | these are evaluation/learning concerns for 08 |
| Campaign Core or orchestration runtime | `NO_CHANGE` in 07 | different ownership and later scope |

No exact class name, command name, directory, registry format, or persisted
schema is selected by this shaping result.

## 7. Deferred-Input Applicability

The approved PL-V39-06 Plan §13 contains exactly six routed/deferred items.

| # | Exact 06 item | Adjudication | 07 consequence |
|---|---|---|---|
| 1 | skills, checklists, execution routing/contracts, and complex lifecycle execution refinements | `APPLICABLE_TO_PL_V39_07` | Include only the proven deterministic binding gap and a minimum evidence-bound pilot. Existing gates, readiness, envelope, blocker locality, modes, and skills are already satisfied surfaces; no general lifecycle rewrite. |
| 2 | quality scoring, learning, adaptive context policy, semantic relevance evaluation, and PromptOps | `APPLICABLE_TO_PL_V39_08` | Excluded from 07. |
| 3 | multi-agent orchestration and production Context Compiler experiments | `LATER_OWNER_DECISION` | Preserve for 09/later; no delegation, scheduling, or workflow chaining in 07. |
| 4 | embeddings/vector search/RAG, semantic memory automation, episodic summary trees, utility/forgetting ledgers, graph stores | `NOT_NEEDED` | Not needed to close the explicit-facts guidance seam; no semantic retrieval in 07. |
| 5 | recommendation discovery, automatic promotion/absorption, registry, and routing | `LATER_OWNER_DECISION` | Recommendation intake is a different lifecycle; do not reuse it as contract discovery. |
| 6 | live Poker/mood migration or final external control-home placement | `LATER_OWNER_DECISION` | Use controlled consumer-shaped fixtures only; no live mutation or topology decision. |

Summary:

```text
DEFERRED_06_ITEMS: 6
ROUTED_TO_07: 1
ROUTED_TO_08: 1
ROUTED_LATER: 3
ALREADY_SATISFIED_OR_NOT_NEEDED: 1
```

## 8. PL-V39-06 Integration Boundary

The 07 seam consumes the committed 06 resume contract as a bounded input. It
may also resolve authoritative pointers already named by that input. It must
not rescan completed history, infer current state from conversational memory,
change the resume authority order, or persist a parallel current-state file.

The preferred flow is:

```text
ResumeContextV1-level facts
+ current lifecycle/Plan authority explicitly referenced by those facts
-> deterministic execution-guidance decision
-> one matched bounded guidance bundle, or a fail-closed result
```

Explicit structured facts such as lifecycle stage, authorization, next
permitted action/action class, artifact role, and an explicit contract identity
may drive selection. LLM classification, embeddings, relevance ranking, and
history discovery are boundary pressure for 08, not fallback behavior in 07.

## 9. Consumer Requirements

No live Poker or mood read was needed: PL-V39-06 already produced current,
controlled, disposable evidence for their materially distinct shapes.

For a mature Poker-shaped project, a matched decision must let an agent reach
the authorized procedure, scope, checks, stop conditions, and next gate without
re-reading full procedure history or guessing. It must still stop when owner
authorization is absent or the route is ambiguous.

For an early mood-shaped project with no active implementation or applicable
contract, the result must be a safe no-match/not-authorized defer outcome. It
must not invent a Change, select `planning-execute`, or create a procedure to
fill the absence.

Later evidence should use controlled fixtures representing both shapes.
Live migration, live control-home placement, and consumer mutation remain
separately owner-authorized work.

## 10. 07 / 08 / 09 Boundary

PL-V39-07 may own only a deterministic, inspectable binding from authorized
current facts to a bounded existing guidance bundle, minimum evidence-bound
checklist/skill applicability, and fail-closed route outcomes.

PL-V39-08 owns scoring, eval-system extraction, learning, semantic relevance,
adaptive/model routing, PromptOps, optimization, and evidence-backed scale-out.

PL-V39-09 or later owner decisions own multi-agent orchestration, automatic
delegation/chaining, release orchestration, scheduling, and production Context
Compiler experiments.

`ROADMAP_SEMANTIC_MISMATCH: NO`. The proposed Change is the Roadmap's required
minimum pilot, not the complete future corpus or adaptive router.

## 11. Actual Missing Capability and Scope Recommendation

The actual missing capability is:

> A deterministic, fail-closed, non-authoritative binding from the committed
> PL-V39-06 resume/current-action facts to exactly one applicable bounded
> execution-guidance bundle (or an explicit no-match/ambiguity/authorization/
> missing-context result), reusing existing lifecycle, workflow, skill,
> checklist, scope, verification, and evidence surfaces.

Recommended proposed Change:

```text
CHG-PL-V39-07-DETERMINISTIC-EXECUTION-GUIDANCE-001
```

Scope judgment: `BOUNDED`.

The definition can be reviewed without implementation discovery. Exact runtime
surface, file placement, and representation remain Plan/Readiness questions
after owner approval and activation.
