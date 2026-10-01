# Material Code Documentation and Maintainability Binding — Implementation Plan v1

```text
CHANGE_ID: CHG-PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-001
PLAN_STATUS: CANDIDATE / OWNER REVIEW REQUIRED
DEFINITION: docs/design/project-spine/checkpoints/PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-CHANGE-DEFINITION-v1.md
FORMAL_READINESS: READY / IMPLEMENTATION NOT AUTHORIZED
```

## Live discovery answers Q1–Q9

| Question | Evidence-based answer |
|---|---|
| Q1 — selector owners | Planning: `template/.planning/control/CHANGE_PLANNING.md`, invoked by `modes/PLAN.md` and `planning-plan/SKILL.md`. Readiness: `CHANGE_READINESS.md`, invoked by the `RUN_FORMAL_READINESS` / `FORMAL_READINESS_V1` audit route. Execution: `CHANGE_EXECUTION.md`, loaded by `modes/EXECUTE.md` and `planning-execute/SKILL.md`. Closure: `CHANGE_CLOSURE.md` plus its required `disciplines/CODE_REVIEW.md`, selected through `planning-audit/SKILL.md`. `CODEBASE_DESIGN.md` owns the design norm, not stage selection. |
| Q2 — conditional Execution selector | Yes. The approved Plan has a `MATERIAL_CODE_CONTRACT: YES/NO` marker in its existing Documentation and operations section. `CHANGE_EXECUTION.md` requires CODEBASE_DESIGN before/during generation for YES. An approved marker is deterministic; a newly discovered unplanned material contract routes through the existing amendment path. |
| Q3 — runtime change | No. `execution_guidance.py` has a finite operation projection and no materiality facts in its schema. Ordinary execution has `discipline_refs: []` by design. Do not add schema, a new capability, or runtime dispatch for this policy. |
| Q4 — current structural tests | `tests/test_field_control_pack_foundation.py` checks workflow route identity and cross-workflow references, including Execution and Readiness. `tests/test_execution_guidance.py::test_contract_route_projects_contract_closure_and_zero_discipline_is_explicit` locks ordinary execution to an empty discipline-ref list and the separate contract route to `CONTRACT_CLOSURE.md`. Preserve that runtime invariant. |
| Q5 — minimum template/control/discipline surface | The six files listed in Definition: CODEBASE_DESIGN, CHANGE_PLANNING, CHANGE_READINESS, CHANGE_EXECUTION, CHANGE_CLOSURE, CODE_REVIEW. Ownership and Copier manifests already classify these as managed. |
| Q6 — minimum test surface | Add focused policy/selector assertions in `tests/test_field_control_pack_foundation.py`; do not modify runtime tests. Test bounded triggers/exemptions and that Planning, Readiness, Execution, and Closure bind to one CODEBASE_DESIGN rule without duplicating it. |
| Q7 — authority duplication | No. CODEBASE_DESIGN owns the normative source contract. CODE_REVIEW checks it. Definition of Done retains only broad documentation completion. |
| Q8 — M0–M4 field proof | Yes. A later disposable consumer can implement a small material callable and a trivial private helper under the approved workflow, then exercise M0–M4 as reviewer outcomes without central product changes. This Plan does not run the proof. |
| Q9 — runtime-free correction | Yes. The bounded correction remains managed template/policy plus focused tests; no Python runtime or state-schema change is required. |

### Selector determinacy boundary

The marker belongs in the existing semantic Plan, not in a new machine schema.
Planning classifies against the finite Definition triggers and records the
concrete symbols and source-document obligation. Readiness independently checks
that decision against scope and evidence. After approval, Execution follows
that explicit value. If the change in reality exposes another material
contract, do not infer a new approved obligation: amend/re-plan first. This
keeps the workflow selector deterministic while allowing the ordinary
execution projection to retain zero discipline refs.

## Planned tasks and dependency order

| Task | Work and evidence | Dependencies / boundary |
|---|---|---|
| T-01 | Reconfirm live selector owners, ownership manifests, current structural tests, exact paths, and unchanged runtime binding. Record the six-file policy surface and one-file test surface. | First. Read-only discovery. Stop with `CODEBASE_DESIGN_EXECUTION_SELECTOR_ARCHITECTURE_REQUIRED` only if the conditional workflow selector proves non-deterministic in live use. |
| T-02 | Expand CODEBASE_DESIGN into the sole normative maintainability and material source-contract rule. Replace its architecture-only load note with the bounded material-contract applicability. State triggers, legal no-doc cases, semantic adequacy/staleness, prospective debt, and performance boundary. | T-01. No duplicate rule owner. |
| T-03 | Add thin bindings: Plan marker/obligation in CHANGE_PLANNING; applicability and determinacy audit in CHANGE_READINESS; pre-generation conditional load in CHANGE_EXECUTION; CODEBASE_DESIGN reference in CODE_REVIEW and thin use in CHANGE_CLOSURE. | T-02. Keep workflow selectors and authority unchanged outside this contract. No skill/mode/schema changes unless T-01 evidence disproves current direct workflow loading. |
| T-04 | Add focused structural policy assertions in `tests/test_field_control_pack_foundation.py` for all stage bindings, the bounded yes/no materiality test and exemptions, single normative ownership, and no runtime-ref requirement. Preserve the existing execution-guidance empty-ref test. | T-03. Avoid asserting prose layout or a docstring count. |
| T-05 | In a clean disposable consumer only, execute M0–M4 through the Planning, Readiness, Execution, and review route. Record actual files/behavior and each PASS/FAIL disposition. | T-04 and the committed candidate template. No central runtime/product edits. |
| T-06 | Run the focused tests, template adoption/doctor and update checks appropriate to the six managed files, then the broader regression suite and independent candidate review at the integration gate. Check project-owned files stay unchanged. | T-05. Verification scope follows evidence and central repository verification policy. |
| T-07 | After the candidate is complete, independently reviewed, and owner-approved, obtain the separately required implementation/commit/closeout authority; commit the bounded product correction and close the Change with final evidence. | T-06 and explicit authority. This Plan and READY do not supply it. |

These are implementation tasks, not owner micro-gates between routine slices.
The only approval boundaries are the ordinary owner review of this Definition,
Plan, and Readiness, and the separately required implementation/commit
authorization before T-07. No work beyond current authorized checkpoint
preparation is performed here.

## Future implementation write and verification surfaces

Managed template paths:

1. `template/.planning/disciplines/CODEBASE_DESIGN.md` — normative contract.
2. `template/.planning/control/CHANGE_PLANNING.md` — explicit Plan marker and
   symbol-specific obligation.
3. `template/.planning/control/CHANGE_READINESS.md` — applicability,
   obligation, determinacy, and review-route checks.
4. `template/.planning/control/CHANGE_EXECUTION.md` — conditional
   pre-generation CODEBASE_DESIGN load and amendment on newly discovered
   material scope.
5. `template/.planning/disciplines/CODE_REVIEW.md` — thin normative reference
   and Pass 2 checks.
6. `template/.planning/control/CHANGE_CLOSURE.md` — thin closure link to the
   existing code-review procedure.

Focused test path: `tests/test_field_control_pack_foundation.py` only.
`tests/test_execution_guidance.py` remains unchanged and its empty-ref contract
is a regression invariant. No Python source, runtime schemas, Change template,
Copier task, new discipline, or Roadmap path is in the expected write surface.

Verification sequence after implementation authorization: focused structural
tests; disposable consumer M0–M4; required template adoption and doctor/update
checks; then full suite and independent review at the integration gate. The
consumer proof checks M0 concise/sufficient PASS, M1 missing material docs
FAIL, M2 tautology FAIL, M3 contradiction FAIL, and M4 obvious private helper
without docs PASS. No historical code inventory is converted into migration
scope. Existing undocumented symbols remain observed debt unless separately
authorized.

## Non-goals, stops, and authority

No coverage target, universal docstring rule, pydocstyle gate, automatic
generator, LLM judge, complexity or documentation scoring, quality service,
database, profiler, or performance optimization requirement. No old source
retrofit. No new runtime/schema architecture. If the six-file managed-policy
surface cannot express the route, stop and return
`CODEBASE_DESIGN_EXECUTION_SELECTOR_ARCHITECTURE_REQUIRED`; do not expand
architecture under this Plan.

The sequential whole-organism proof remains `NOT STARTED`; 09-G remains `NOT
STARTED`; neither is authorized. Roadmap is read-only. Implementation,
product/template/test changes, staging, commit, and push are not authorized by
this transition.
