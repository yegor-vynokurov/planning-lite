# Material Code Documentation and Maintainability Binding — Change Definition v1

```text
CHANGE_ID: CHG-PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-001
OWNER_DECISION: ACCEPT_BOUNDED_OPTION_B_PLUS
DEFINITION_STATUS: CANDIDATE / OWNER REVIEW REQUIRED
ENTRY_HEAD: 7bbf5937094484b074d20224aadb370c0d3ae493
ENTRY_GATE: OWNER_ADJUDICATION_BOUNDED_CODEBASE_DESIGN_CORRECTION_BEFORE_FRESH_SESSION_SEQUENTIAL_WHOLE_ORGANISM_PROOF
IMPLEMENTATION_AUTHORIZED: NO
```

## Problem and accepted evidence

The accepted Code Documentation and Maintainability Vitality Challenge found
documentation capability `PARTIAL`, maintainability capability `LIVE_NARROW`,
and the first broken seam `POLICY_TOO_VAGUE`. Its checkpoint is
`docs/design/project-spine/checkpoints/PLANNING-LITE-CODE-DOCUMENTATION-AND-MAINTAINABILITY-VITALITY-CHALLENGE-v1.md`
(SHA-256
`a337a1c7ef947ab423d6c81a57ac61b12f93b6420d084391a92a920d3c5acf18`). The
evaluator-operated, unblinded challenge found that M1 (missing material
documentation) and M2 (tautological documentation) survived. M3 (a false
persistence claim) was caught during manual CODE_REVIEW Pass 2. Execution had
no concrete documentation-standard binding. These results are evidence about
the observed route, not a reliability-rate claim.

The current interfaces and maintainability principles already belong in
`CODEBASE_DESIGN.md`, but no selected policy defines which material source
contracts need adjacent documentation or what that documentation must convey.
The ordinary execution-guidance projection intentionally has no discipline
refs. The approved Plan and Execution workflow provide a smaller deterministic
selector than changing that runtime projection.

## Normative ownership and applicability

`template/.planning/disciplines/CODEBASE_DESIGN.md` is the single normative
owner for both maintainable material code design and the documentation of
material source contracts. It owns the rule body. `CODE_REVIEW.md` remains a
review procedure and will point to that rule; it will not define a competing
standard. Definition of Done keeps its existing broad obligation to update
user, developer, deployment, monitoring, and support documentation where
affected; it does not become the source-code documentation owner.

Use the applicability label `MATERIAL_CODE_CONTRACT` when a task creates or
materially changes a contract whose meaning a reasonable caller or future
maintainer cannot safely infer from a trivial signature and body. The bounded
triggers are:

- a public or externally used callable/class;
- state-transition ownership;
- an authorization or security boundary;
- persistence, serialization, or schema behavior;
- concurrency, locking, or atomicity behavior;
- a parser or validator with non-obvious grammar or failure semantics;
- routing, orchestration, or policy selection;
- a material side effect;
- a non-obvious algorithm or invariant; or
- another concrete hidden contract that would otherwise require inspecting
  implementation details to recover.

The final item is constrained by the same materiality test and must name the
hidden contract. Applicability is prospective: newly created or materially
changed contracts are in scope. Existing undocumented code is
`OBSERVED_EXISTING_DEBT`, not an automatic blocker or retrofit task.

No redundant docstring is required for an obvious tiny private transformation,
a straightforward accessor/property, a trivial forwarding wrapper with no
hidden contract, generated code, or a symbol that does not own the material
contract. These exceptions do not override a concrete trigger.

## Source-document contract

For a `MATERIAL_CODE_CONTRACT`, require nearby source documentation appropriate
to the implementation language. For Python functions and classes, the normal
form is a docstring. Documentation states the material meaning a caller or
maintainer needs, choosing only applicable dimensions: purpose, authoritative
input/source of truth, caller-facing contract, invariant, output or state
transition, failure/rejection semantics, side effects, persistence,
concurrency/locking, authorization assumptions, and non-goals or forbidden
interpretations. Do not require fixed headings, every dimension, a minimum
length, or documentation counts.

`DOCSTRING_PRESENT` and `MATERIAL_CONTRACT_DOCUMENTED` are distinct checks.
A name-restatement, generic phrase such as “Process the data,” or prose that
merely repeats parameter names does not satisfy a material contract. A
reasonable but materially wrong inference caused by omitted meaning is also a
failure. Documentation that contradicts actual behavior or a material
invariant fails standards review. If behavior changes a documented contract,
the same Change updates the source documentation. Passing tests alone does not
make stale prose acceptable.

## Maintainability contract

Preserve and make operational the existing `CODEBASE_DESIGN` principles:
smallest coherent implementation; explicit contracts and ownership; local
reasoning; low unnecessary coupling; thin orchestration; deep/coherent modules
where useful; testable seams; and no generic helper hub, speculative
abstraction, or implementation-time architecture invention without evidence.
“Optimal code” is not an acceptance rule. Performance optimization requires
evidence of a performance need; maintainability work does not imply a
performance target, profiler, or optimization subsystem.

## Workflow bindings

**Planning.** `CHANGE_PLANNING.md` owns selection. In its existing
Documentation and operations part of the semantic Plan, record
`MATERIAL_CODE_CONTRACT: YES` or `NO`. If `YES`, select CODEBASE_DESIGN and name
the material symbol/boundary, the contract meaning that must remain
understandable, expected source-document location/form, and verification
route. If `NO`, give the concrete reason no bounded trigger applies. Do not
draft full docstring prose unless needed to settle semantics.

**Readiness.** `CHANGE_READINESS.md` tests the classification against the
approved scope and affected symbols, checks the symbol-specific documentation
obligation and location/form, confirms the implementation task does not need
to invent contract semantics, and checks that a review/verification route
exists. “Documentation addressed where applicable” by itself is insufficient.
If a trigger is present but Plan says `NO`, or the Plan is indeterminate,
Readiness returns Needs revision or Blocked with evidence.

**Execution.** `CHANGE_EXECUTION.md` reads the approved Plan marker. For
`MATERIAL_CODE_CONTRACT: YES`, it requires loading the applicable
CODEBASE_DESIGN contract before or during code generation and carrying its
obligation in the task envelope. A newly discovered material contract absent
from the approved Plan goes through the existing amendment path before the
dependent code is generated. This is a workflow-level conditional selector;
it adds no runtime schema, discipline-ref field, service, or authority.

**Closure.** `CHANGE_CLOSURE.md` continues to use `CODE_REVIEW.md` for Pass 2.
CODE_REVIEW thinly directs standards review to CODEBASE_DESIGN and checks
applicability, required documentation presence, semantic adequacy,
consistency with behavior/invariants, and maintainability. It does not copy
the normative rule body. DoD remains broad and is not duplicated.

The live selection authorities are `CHANGE_PLANNING.md` (Planning),
`CHANGE_READINESS.md` (Readiness), `CHANGE_EXECUTION.md` (Execution, through
`planning-execute/SKILL.md`), and `CHANGE_CLOSURE.md` with `CODE_REVIEW.md`
(Closure, through `planning-audit/SKILL.md`). The runtime guidance implementation
and its production binding surface require no change.

## Acceptance and boundaries

A later disposable-consumer proof must preserve the following materiality
mutants and outcomes:

| Probe | Case | Expected |
|---|---|---|
| M0 | Concise, semantically sufficient material documentation | PASS |
| M1 | Material public/boundary function has no required source documentation | FAIL |
| M2 | Material function has tautological “Process the data” documentation | FAIL |
| M3 | Documentation materially contradicts behavior or an invariant | FAIL |
| M4 | Tiny obvious private helper has no docstring | PASS |

This Change does not execute that proof or edit existing product modules. It
does not create a separate documentation discipline, documentation counter or
coverage threshold, automatic generator, LLM judge, unconditional pydocstyle
gate, complexity score, quality daemon, database/service, profiler
requirement, or architecture extension. The correction may remain
template/policy/test-only.

The fresh-session sequential whole-organism proof remains `NOT STARTED` and is
not authorized by this Definition. 09-G remains `NOT STARTED`; this Definition
does not authorize it. Formal Readiness does not grant implementation
authority. The Roadmap is outside scope and remains read-only.

## Candidate write boundary

If separately reviewed and authorized, the expected minimum managed template
surface is:

- `template/.planning/disciplines/CODEBASE_DESIGN.md`;
- `template/.planning/control/CHANGE_PLANNING.md`;
- `template/.planning/control/CHANGE_READINESS.md`;
- `template/.planning/control/CHANGE_EXECUTION.md`;
- `template/.planning/control/CHANGE_CLOSURE.md`; and
- `template/.planning/disciplines/CODE_REVIEW.md`.

The expected focused test surface is `tests/test_field_control_pack_foundation.py`.
No Plan template/schema, Python runtime, or `tests/test_execution_guidance.py`
change is needed. The latter retains its current assertion that ordinary
execution guidance has an empty `discipline_refs` list. Live ownership
evidence: `OWNERSHIP.yml` manages `.planning/control/**` and
`.planning/disciplines/**`; `copier.yml` does not skip either tree, and no
project-owned path is in the candidate surface.
