# PL-V39-09 Minimal Architecture Decision Flow MVP — Implementation Plan Candidate

Status: CANDIDATE / OWNER REVIEW REQUIRED  
Change ID: `CHG-PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-001`  
Prepared: 2026-09-30

This is a candidate Plan for combined owner review. It proposes a bounded
future implementation sequence; it is not an execution authorization. The
present transition performs no product or test mutation.

## Approach

Reuse the existing 09-B owner and 09-E compiler, then prove the smallest
vertical slice in the order: concise guidance and carrier → deterministic
acceptance → one real field proof after authorization → only then consider
refinements. Keep the flow human-led and opt-in. Avoid a runtime schema unless
the reviewed implementation demonstrates that the existing Architecture
Overview carrier cannot safely express the required semantics.

The carrier is the existing consumer-owned
`.planning/project/ARCHITECTURE_OVERVIEW.md`. `ArchitectureDecisionPacketV1`
is not canonized as a new schema. Existing Goal, Critical Flow, Target,
decision, evidence, and semantic Plan records remain their own authorities and
may be referenced from the carrier.

## Proposed product write surface

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

No Python runtime source, CLI, Copier ownership behavior, new top-level
subsystem, canonical architecture pack, or deployable manifest is currently
needed. Reassess only if deterministic acceptance exposes a necessary missing
capability, and return that finding to owner review before widening the write
surface.

## Proposed test write surface

The likely focused test is `tests/test_architecture_decision_flow.py`. It
should inspect the carrier and route semantics and exercise the existing
09-E input contract without asserting prose layout. If the acceptance is
already naturally owned by `tests/test_project_shaping_foundation.py`, extend
that owner instead of duplicating invariants. Do not modify
`tests/test_plan_compilation.py` unless a genuine integration gap in the
existing compiler contract is found. No test path is changed in this
transition.

## Future bounded task sequence

| Task | Work | Evidence / stop condition |
|---|---|---|
| T-01 | Reconfirm reviewed Definition, existing carrier ownership, baseline and exact write boundary. | Stop if ownership or the reusable 09-E contract differs materially. |
| T-02 | Add concise architecture-decision guidance and one ROOT_ROUTER entry. | Demonstrate opt-in routing and unchanged routine-work route. |
| T-03 | Extend the existing Architecture Overview seed with only the compact structured record and references. | Verify no second authority or new packet/schema is introduced. |
| T-04 | Add focused deterministic acceptance at the selected owning test path. | Cover the matrix below; avoid duplicate tests and presentation-only assertions. |
| T-05 | Build one real architecture-sensitive field proof, subject selected by the reviewed Plan/owner gate. | Stop on ungrounded driver, unmeasurable material quality concern, unsupported choice, missing evidence, or incomplete 09-E compilation. |
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
| Decision uncertainty | Accepted choice records rationale/trade-off/nonselection; insufficient evidence yields bounded `SPIKE_REQUIRED` and its unlock decision. |
| Horizons and evolution | Target/MVP/Reference/Transition remain distinct; accepted material decisions carry replacement/scale risk, reopen trigger and next transition; seam remains optional. |
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
choice or a bounded spike. Distinguish the target from the MVP/reference and
next transition, add evolution fields and a practical evidence obligation, and
produce/reference the existing semantic Plan and controlled discoveries.
Compile with:

```text
planning-lite plan-compile TARGET --plan <exact path> --tasks <exact path> --proposal <exact JSON path>
```

The field evidence must show that the existing 09-E compiler consumes the
semantic Plan without changing its dependencies or inventing architecture
decisions.

## Field-proof subject and evidence

The proof is one real architecture-sensitive owner question, not a synthetic
whole-project survey. The subject is not frozen here because discovery did not
identify a uniquely best current case. At the combined review or later owner
gate, select a bounded current Planning Lite question if suitable; otherwise
select another real case and record why. Preserve source evidence and owner
authority, and keep the proof isolated from unrelated live consumers.

Acceptance requires a trace from question → drivers → measurable scenarios →
alternatives including simpler alternative → accepted decision or bounded
spike → target/MVP/transition → evolution mini-fields → evidence obligation →
semantic Plan → existing 09-E compilation. No unresolved architecture fact may
be invented to force a pass.

## Reused contracts and ownership

- 09-B Ideal Scaffold skeleton and frozen Architecture Knowledge topology and
  validation ownership;
- the existing `.planning/project/ARCHITECTURE_OVERVIEW.md` carrier and its
  project-owned status;
- existing Project Spine Goal, Critical Flow, Target, decision and evidence
  authorities;
- 09-E semantic-plan distinction, capability/executor contract, controlled
  discovery fields, tasks/proposal contract, and CLI compiler;
- existing Planning Lite test owners, with one new focused test module only if
  no existing owner fits.

No second architecture packet schema is proposed. If a new schema appears
necessary, stop and return a narrowly evidenced ownership decision instead of
adding it opportunistically.

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

This Plan candidate proposes no present execution. Implementation and tests
remain unauthorized until the Definition and Plan receive the requested
combined owner review and the applicable central execution gate is satisfied.
No 09-G, Roadmap rewrite, stage, commit, push, or release is in scope.

Stop if the existing carrier cannot preserve project ownership, provenance or
decision authority; if the 09-E semantic contract has changed; if acceptance
requires an unreviewed schema/runtime write; or if the selected field case
cannot ground its material claims. Bring the smallest concrete issue back for
owner adjudication without expanding the Change by implication.
