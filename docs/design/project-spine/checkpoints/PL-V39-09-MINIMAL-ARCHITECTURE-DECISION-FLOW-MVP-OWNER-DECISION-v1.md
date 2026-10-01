# PL-V39-09 Minimal Architecture Decision Flow MVP — Owner Decision

Date: 2026-09-30

## Decision

```text
OWNER_DECISION: SELECT_PL_V39_09_MINIMAL_ARCHITECTURE_DECISION_FLOW_MVP
DECISION_SOURCE: EXPLICIT_HUMAN_OWNER / USER REQUEST
PREVIOUS_GATE: OWNER_ADJUDICATION_NEXT_IMPLEMENTATION_CHANGE_AFTER_ROADMAP_RECONCILIATION
SELECTED_CHANGE_ID: CHG-PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-001
ROADMAP_MACRO_STRUCTURE_CHANGED: NO
09_G_STARTED: NO
IMPLEMENTATION_AUTHORIZED: NO
NEXT_PHASE: COMBINED_DEFINITION_AND_PLAN_OWNER_REVIEW
NEXT_SINGLE_GATE: OWNER_REVIEW_PL_V39_09_MINIMAL_ARCHITECTURE_DECISION_FLOW_MVP_DEFINITION_AND_PLAN
```

This consumes the current owner-adjudication gate by selecting the bounded
Minimal Architecture Decision Flow MVP. It does not start 09-G, alter the live
Roadmap, approve either candidate, or authorize product implementation.

## Entry state and bounded evidence

The central checkout was `D:/documents/planning-lite`, at HEAD
`f16fd50f93452f9f38a892d58fdad7c67f3bbcd8`. The strict resume entry reported
the previous gate above, no active Change, no implementation authority, and a
dirty working tree. The index was empty. The pre-existing dirt consists of
unrelated PL-V39-09 checkpoint drafts plus edits to
`src/planning_lite/operation_lifecycle.py` and
`tests/test_operation_lifecycle.py`; it is preserved and excluded from this
Change's write set.

The entry authority evidence covered CURRENT, the live Roadmap, the PL08
closeout, the 09-B Ideal Scaffold and architecture-knowledge ownership
contracts, the Engineering Basis contract, the 09-E semantic-plan/compiler
contracts and implementation/tests, and the relevant consumer templates,
decision template, Root Router, and Plan template. Its canonical state ID was
`8e97c8254a99dae41f0ced32aecb555a6bdef6237ea2071cd6bc49d555263424`.
The unrelated-dirt baseline ID was
`2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821`.

## Bounded read-only discovery

1. **Carrier owner.** Reuse the consumer-owned
   `.planning/project/ARCHITECTURE_OVERVIEW.md` as the compact structured
   architecture model and decision-flow carrier. It is the existing accepted
   09-B scaffold location, protected as project-owned by
   `copier.yml` (`.planning/project/**`) and the ownership manifest. Keep
   `ArchitectureDecisionPacketV1` as a conceptual label only; do not create a
   parallel canonical packet path or runtime schema.
2. **Existing 09-B/C/D owners.** Reuse the frozen Ideal Scaffold semantics and
   the Architecture Knowledge topology/validation boundaries from 09-B. 09-C
   Observed Reality and reconciliation is merged into 09-B, so this Change
   needs only bounded provenance-aware reconciliation labels. 09-D progressive
   estimation/uncertainty is merged into 09-E; reuse its bounded uncertainty
   and spike semantics rather than creating another subsystem. Do not expand
   the framework knowledge pack.
3. **09-E handoff.** Produce/reference the existing semantic Plan and ordinary
   task/proposal inputs. Preserve the contract
   `SEMANTIC_PLAN != EXECUTOR_COMPILED_PLAN != TASK_OR_OPERATION_CAPSULE` and
   use the existing `planning-lite plan-compile TARGET --plan <path> --tasks
   <path> --proposal <path>` path. 09-E remains the compiler and acquires no
   architecture-decision authority.
4. **Implementation class.** The smallest MVP is guidance/template-first:
   one bounded control guide, one Root Router route, and one compact structured
   block in the existing Architecture Overview seed. A new product runtime
   schema or Python implementation is not presently justified.
5. **Smallest plausible write surface.** Candidate paths are
   `template/.planning/control/ARCHITECTURE_DECISION_FLOW.md`,
   `template/.planning/control/ROOT_ROUTER.md`, and
   `template/.planning/project/ARCHITECTURE_OVERVIEW.md`. The consumer
   Architecture Overview remains project-owned after adoption.
6. **First end-to-end executable seam.** One architecture-sensitive request
   traverses the control guide into the Architecture Overview record, yields an
   ordinary semantic Plan/tasks/proposal, then compiles through the existing
   09-E CLI into its canonical executor-aware plan, including a bounded
   controlled discovery when required.
7. **Semantics already present.** The 09-B owner artifacts already establish
   goal/critical-flow-first reasoning, progressive questions, drivers before
   technology, a single structured semantic model, justified alternatives,
   reversible low-risk defaults, and reuse of existing decision/evidence
   authorities. 09-E already provides capability-aware semantic plans,
   executor readiness, controlled discoveries, and authority boundaries. The
   Change integrates these into one end-to-end flow; it does not reimplement
   them.

## State receipt

The candidates prepared for combined owner review are:

- `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-CHANGE-DEFINITION-v1.md`
- `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-IMPLEMENTATION-PLAN-v1.md`

The Definition SHA-256 is
`6f2b9fbe88a5cbd8b570b027f5ed3108390f045c2c9d3e5d826757500b1b8a1a`; the
Plan SHA-256 is
`118ae569d2dc7eea1b5342589e2b8d25feaddcfdb4b55535bcd24a96a6f85cb2`. Their
canonical candidate-state ID is recorded below. The exit authority-state
digest includes the entry authority set, the changed CURRENT, and these two
candidates. This decision checkpoint is excluded from that digest to avoid a
self-reference; its path is recorded by CURRENT. The pre-existing
unrelated-dirt set remains preserved and is independently fingerprinted at
exit.

```text
EXIT_HEAD: f16fd50f93452f9f38a892d58fdad7c67f3bbcd8
EXIT_AUTHORITY_STATE_ID: b603819ec1372a2a55852c1bfff3eaa69b9078b39ca1d9552ca6e3e4fd95a453
EXIT_CANDIDATE_STATE_ID: 5730f9d7a2b4211f38b8b8bc05ce398e243af85730208398f2d4a6bf67cae6c1
EXIT_UNRELATED_DIRT_STATE_ID: 2153d2ac08da5f6f91d2cf783af37a29dca34f340dad3d132e7bf8e844a43821
EXIT_SYNC_STATE_ID: NOT_REPRODUCIBLE_BY_CURRENT_TOOLING
ROADMAP_CHANGED: NO
PRODUCT_SOURCE_CHANGED: NO
TESTS_CHANGED: NO
STAGE: NO
COMMIT: NO
PUSH: NO
RELEASE: NO
```
