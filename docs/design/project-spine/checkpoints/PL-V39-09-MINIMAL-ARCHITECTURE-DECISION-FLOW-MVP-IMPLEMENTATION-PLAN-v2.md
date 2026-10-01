# PL-V39-09 Minimal Architecture Decision Flow MVP — Implementation Plan v2

Status: OWNER-APPROVED / FORMAL READINESS READY  
Change ID: `CHG-PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-001`  
Prepared: 2026-09-30

The owner accepted this v2 Plan under verdict
`PASS_WITH_TWO_BOUNDED_CONTRACT_CORRECTIONS`. It proposes a bounded future
implementation sequence and does not authorize execution. This transition
performs no product or test mutation.

## Approach

Reuse only the frozen/bounded 09-B subset while the 09-B parent remains OPEN /
PARTIALLY DESIGNED, plus the existing 09-E compiler. Prove one human-led,
opt-in vertical slice in this order: concise guidance and carrier →
deterministic acceptance → one real field proof after implementation
authorization → only then consider refinements. Each invocation and carrier
record covers exactly one material architecture question. Do not require the
remaining open 09-B parent work. Avoid a runtime schema unless the reviewed
implementation demonstrates that the existing Architecture Overview carrier
cannot safely express the required semantics.

The carrier is the existing consumer-owned
`.planning/project/ARCHITECTURE_OVERVIEW.md`. `ArchitectureDecisionPacketV1`
is not canonized as a new schema. Existing Goal, Critical Flow, Target,
decision, evidence, and semantic Plan records remain their own authorities and
may be referenced from the carrier.

## Proposed product write surface (exact minimal surface)

The smallest plausible paths are:

1. `template/.planning/control/ARCHITECTURE_DECISION_FLOW.md` — new concise
   user guidance describing entry criteria, the compact record, decision vs
   spike behavior, and 09-E handoff.
2. `template/.planning/control/ROOT_ROUTER.md` — add one routing rule for
   architecture-sensitive requests; route routine work through the existing
   path.
3. `template/.planning/project/ARCHITECTURE_OVERVIEW.md` — extend the existing
   seed with a compact structured decision-flow block and references to
   existing project-owned authorities. This is the established carrier path;
   do not add `.planning/project/IDEAL_SCAFFOLD.*` or a duplicate packet.

No Python runtime source, Context Compiler/runtime implementation, SQLite,
vector index, CLI, Copier ownership behavior, new top-level subsystem,
canonical architecture pack, or deployable manifest is expected in this Change.
The field question may assess those options without implementing or presuming
them. Reassess only if deterministic acceptance exposes a necessary missing
capability, and return that finding to owner review before widening the write
surface.

## Proposed test write surface

Prefer an existing suitable test owner, especially
`tests/test_project_shaping_foundation.py`, when it can own these invariants
without duplication. Add `tests/test_architecture_decision_flow.py` only if it
is clearly the smallest suitable owner. Acceptance must cover exactly one
material question per invocation, one terminal result (`DECISION_ACCEPTED` or
`SPIKE_REQUIRED`), and the other semantic cases below without asserting prose
layout. Do not modify `tests/test_plan_compilation.py` absent a genuine compiler
integration gap. The real field proof is mandatory and cannot be replaced by
template-fixture assertions. No test path is changed in this transition.

## Future bounded task sequence

| Task | Work | Evidence / stop condition |
|---|---|---|
| T-01 | Reconfirm reviewed Definition, existing carrier ownership, baseline and exact write boundary. | Stop if ownership or the reusable 09-E contract differs materially. |
| T-02 | Add concise architecture-decision guidance and one ROOT_ROUTER entry. | Demonstrate opt-in routing and unchanged routine-work route. |
| T-03 | Extend the existing Architecture Overview seed with only the compact structured record and references. | Verify no second authority or new packet/schema is introduced. |
| T-04 | Add focused deterministic acceptance at the selected owning test path. | Cover the matrix below; avoid duplicate tests and presentation-only assertions. |
| T-05 | After implementation authorization, build the frozen real field proof `CONTEXT_MEMORY_ARCHITECTURE_FOR_FIRST_SEQUENTIAL_POST_MVP_TRUNK_FLOW` for exactly one question. | Use actual Organism Vitality Audit evidence; do not assume the answer. Stop on ungrounded facts, unmeasurable material concern, unsupported choice, missing evidence, or incomplete 09-E compilation. Do not start 09-G. |
| T-06 | Review evidence and close or record bounded corrections. | Close only with end-to-end proof and all material findings adjudicated. |

Tasks are a proposed bounded ordering, not authorization to start. There is no
separate architecture methodology rollout, 09-G, or optional framework
expansion task hidden in this sequence. Any required owner review under the
central governance lifecycle should be combined with the appropriate artifact
review rather than creating authorization-only micro-gates.

## Minimal deterministic test matrix

| Case | Required result |
|---|---|
| Opt-in routing | Architecture-sensitive requests reach the flow; routine work does not. |
| Provenance and drivers | Material drivers link to source, capability/seam, significance and uncertainty; ordinary answers are not promoted automatically. |
| Scenario | A material quality concern has a measurable stimulus/context/asset/response/measure scenario; support 1–3 applicable scenarios. |
| Alternatives | Consequential choice has at least two credible alternatives and a simpler credible option unless that option is baseline; no arbitrary score is required. |
| One decision / uncertainty | One material question per flow has exactly one terminal result, `DECISION_ACCEPTED` or `SPIKE_REQUIRED`; accepted result records rationale/trade-off/nonselection, while insufficient evidence yields a bounded spike and its unlock decision. Other questions are separate future records. |
| Horizons and evolution | Target/MVP-Reference/Transition remain distinct; accepted material decisions carry replacement/scale risk, reopen trigger and next transition; seam remains optional. |
| Evidence obligation | At least one practical evidence/fitness route is attached to each material selected claim. |
| Brownfield boundary | Initial Ideal/Target remains independent of observed topology; bounded reconciliation uses the allowed difference labels and provenance. |
| 09-E handoff | Result yields/references ordinary semantic Plan, task and proposal inputs accepted by the existing `plan-compile` path; compiled output does not replace semantic authority. |
| No expansion | No technology follows from a project label; no 09-G behavior, parallel compiler, or full deferred subsystem appears. |

The later field proof must additionally demonstrate one actual end-to-end
architecture-sensitive case and successful existing 09-E compilation. It is
not replaced by a fixture test.

## First end-to-end executable seam

Use one owner question with a material architecture consequence. Route it to the
existing Architecture Overview carrier, cite the goal/tier, critical flow,
constraints and facts, derive traceable drivers and applicable measurable
scenarios, compare credible alternatives, then record either an evidence-backed
choice or a bounded spike. Distinguish Target from MVP-Reference and
Transition, add evolution fields and a practical evidence obligation, and
produce/reference the existing semantic Plan and controlled discoveries.
Compile with:

```text
planning-lite plan-compile TARGET --plan <exact path> --tasks <exact path> --proposal <exact JSON path>
```

The field evidence must show that the existing 09-E compiler consumes the
semantic Plan without changing its dependencies or inventing architecture
decisions.

## Frozen field-proof subject and evidence

The one real field-proof subject is
`CONTEXT_MEMORY_ARCHITECTURE_FOR_FIRST_SEQUENTIAL_POST_MVP_TRUNK_FLOW`: for the
first sequential, pre-09-G whole-organism walking skeleton, determine whether
Planning Lite should (A) reuse the existing bounded ResumeContext / HandoffV1 /
ContextTrace model, (B) introduce a new minimal production Context
Compiler/runtime, or (C) require SQLite / semantic/vector retrieval before
that sequential flow. This is one material architecture question, not a
synthetic whole-project survey. Use the actual Organism Vitality Audit evidence
as facts with provenance, not as a preselected answer:

- The audit records bounded ResumeContext / HandoffV1 / ContextTrace as a live
  current-authority resume path and says it is sufficient for a sequential
  walking skeleton without Context revival.
- It records no production Context Compiler, semantic retrieval, SQLite, or
  vector index as a live dependency; those proposals remain future/deferred.
- It also records limits: no live migration proof, no universal semantic-UNKNOWN
  service, and no delegated-result contraction service. These limits must not
  be generalized into claims beyond the selected sequential case.

The field proof must trace the question against these sourced facts and their
limits, identify any additional evidence needed, and leave the result open to
the evidence. Do not assume the answer.

After separate implementation authorization, preserve source evidence and
owner authority and prove the flow in the existing consumer-owned Architecture
Overview: goal / critical flow / facts → drivers → measurable scenarios →
alternatives including the simpler credible alternative → exactly one
`DECISION_ACCEPTED` or `SPIKE_REQUIRED` result → Target / MVP-Reference /
Transition → `REPLACEMENT_OR_SCALE_RISK` / `REOPEN_TRIGGER` / `NEXT_TRANSITION`
→ practical evidence obligation → ordinary semantic Plan → existing 09-E
`plan-compile`. Keep the proof isolated from unrelated live consumers. The
field proof is mandatory and is not replaced by template fixture assertions.
It exercises the decision flow only; it does not start 09-G.

## Reused contracts and ownership

- the frozen/bounded 09-B subset only: frozen Ideal Scaffold skeleton; frozen
  Architecture Knowledge topology and ownership; accepted Engineering Basis /
  Rationale Lineage semantics; and existing consumer-owned Architecture
  Overview carrier. The live 09-B parent remains OPEN / PARTIALLY DESIGNED;
  full parent closure and remaining 09-B work are not dependencies;
- the existing `.planning/project/ARCHITECTURE_OVERVIEW.md` carrier and its
  project-owned status;
- existing Project Spine Goal, Critical Flow, Target, decision and evidence
  authorities;
- 09-E semantic-plan distinction, capability/executor contract, controlled
  discovery fields, tasks/proposal contract, and CLI compiler;
- existing Planning Lite test owners, with one new focused test module only if
  no existing owner fits.

No second architecture packet/schema authority is proposed. If a new schema
appears necessary, stop and return a narrowly evidenced ownership decision
instead of adding it opportunistically. Preserve the existing Architecture
Overview as the sole project-owned carrier.

## P-05 preservation and pre-09-G obligation

Preserve `ATTEMPT_AUTHORIZATION_SCOPE_CONTINUITY / P-05` as
`OPEN / MATERIAL_PRE_09_G_BLOCKER`. It does not block this MVP because this
flow does not depend on Attempt claim/execution admission. Do not repair P-05
here. Before 09-G relies on Attempt claim/execution admission, correct P-05 and
adversarially recheck it.

## Explicitly deferred

Defer full scale envelope and trigger framework; full evolvability or
replaceability contracts; universal seam-conformance tests; deployable system
manifest; complete review-trigger matrix; universal transition recipes;
Project Doctor; production-readiness evidence gate; full Deployment
Sophistication Ladder; full ADR subsystem; full AI Evaluation Contract;
automatic architecture decisions; whole-project orchestration; multi-agent
scheduler; workflow engine; LangGraph, Temporal or queue substrate selection;
09-G; and 09-H release logic. Also defer exhaustive 09-C reality modeling and
any expansion of the architecture knowledge pack.

## Authorization and stop conditions

This approved Plan proposes no present execution. Implementation and tests
remain unauthorized until the separate next gate
`OWNER_AUTHORIZE_PL_V39_09_MINIMAL_ARCHITECTURE_DECISION_FLOW_MVP_IMPLEMENTATION`
is consumed. No 09-G, Roadmap rewrite, stage, commit, push, or release is in
scope.

Stop if the existing carrier cannot preserve project ownership, provenance or
decision authority; if the 09-E semantic contract has changed; if acceptance
requires an unreviewed schema/runtime write; or if the selected field case
cannot ground its material claims. Bring the smallest concrete issue back for
owner adjudication without expanding the Change by implication.
