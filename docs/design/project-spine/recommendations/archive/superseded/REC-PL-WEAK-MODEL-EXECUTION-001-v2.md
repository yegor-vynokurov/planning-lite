# REC-PL-WEAK-MODEL-EXECUTION-001 v2
## Closed-by-construction contracts, Planning closure checks, and bounded Task Closure Review for weaker implementation models

**Status:** `PROVISIONAL / FIELD-DERIVED / OPEN`
**Date:** `2026-08-21`
**Primary field source:** Poker `CHG-0009-bayesian-study-harness`, Execution `T-01` with Luna 5.6
**Supersedes:** `REC-PL-WEAK-MODEL-EXECUTION-001-v1`
**Implementation authority:** none
**Recommended canonical location:** `docs/design/project-spine/REC-PL-WEAK-MODEL-EXECUTION-001-v2.md`
**Related recommendations:** `REC-PL-CONTEXT-HANDOFF-001-v1`, `REC-PL-MATERIALITY-SIMPLICITY-001-v1`, `REC-PL-READINESS-001-v1`, `REC-PL-CHANGE-COST-001-v1`

---

## 1. Why this recommendation exists

This recommendation is not a generic style preference about schemas or prompts.

It exists because the Poker `CHG-0009` field pilot exposed a repeatable failure pattern when a weaker implementation model executed a formally `READY` contract-heavy task.

The execution strategy itself worked well:

```text
one authorized task
→ bounded current-state packet
→ exact file surface
→ exact verification seam
→ no historical Readiness by default
→ stop before dependent task
```

Luna 5.6 reported:

```text
historical readiness required: NO
extra context required: NO
execution friction: NONE
T-01 named test seam: PASS
```

Yet independent bounded review found multiple semantic escape paths.

### Observed escape pattern A — required minimum mistaken for complete schema

The model correctly implemented required provenance fields, but still allowed arbitrary additional fields to enter `ProvenanceIdentity` and alter its canonical fingerprint.

Likewise, `ScientificConfigIdentity` could accept provenance/environment fields.

The recurring pattern was:

```text
"these fields must exist"
implemented as
"these fields are the minimum required"

instead of

"these fields are the complete allowed semantic set"
```

### Observed escape pattern B — nominal typing defeated by open semantic bags

The model removed explicit hidden/evaluator truth fields from `StudyRecord`, but retained an open:

```python
Mapping[str, Any]
```

observable payload.

Final/evaluator truth could therefore still be smuggled through the model-visible record into development/recovery fitting.

This showed:

```text
typed classes != semantic isolation
if an open payload can carry protected semantics
```

### Observed escape pattern C — execution reached a semantic choice that Planning had not actually defined

After further correction, the implementation model correctly stopped with:

```text
BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY
```

because the approved Planning artifacts said only:

```text
observable hero/flop/context/action data only
```

but did not define an exact closed observable/feature schema.

Creating such a schema would require inventing new evidence semantics during Execution.

The model refused to do so.

This was **good behavior** and exposed a Planning gap that Formal Readiness had missed.

### Observed escape pattern D — local ambiguity caused a global stop

The same corrective invocation also contained independent findings `R05` and `R06`.

Because the prompt said to stop on the R04 ambiguity, the model did not continue those independent corrections.

This indicates that blocker scope also needs governance:

```text
local semantic ambiguity
should block its dependency cone

not automatically every independent authorized correction
```

---

## 2. Core problem

Planning Lite currently distinguishes stages and authority well, but contract-heavy work needs a more explicit answer to three questions:

```text
PLANNING:
Have we defined the complete semantic shape?

READINESS:
Is the written contract unambiguous enough that materially different implementations cannot both satisfy it?

EXECUTION:
Can I implement this without inventing new semantics?
```

For weaker implementation models, a task can pass positive tests while leaving the **semantic complement** unconstrained.

The system therefore needs protection against:

```text
required fields != closed schema
named types != closed semantic boundary
positive test PASS != contract closure
local blocker != global stop
```

---

## 3. Design direction

Planning Lite should evaluate a layered **Contract Closure** discipline.

### Layer A — Planning owns complete semantic definition

Planning must define the exact semantic shape for contract-heavy tasks.

### Layer B — Readiness challenges underdetermination

Readiness should test whether two materially different implementations could both satisfy the text.

### Layer C — Execution refuses new semantics

Execution may choose local semantic-neutral implementation details, but must not invent new schema, evidence, identity, persistence, authorization, or scientific semantics.

### Layer D — Task Closure checks the complement

After task tests pass, a bounded closure review should probe nearest-wrong constructions before dependent tasks are authorized.

---

## 4. Positive-command principle

Prefer defining the complete valid construction:

```text
ScientificConfigIdentity contains exactly:
A
B
C

Unknown semantic fields are invalid.
```

over a long prohibition list:

```text
include A/B/C
do not include OS
do not include NumPy
do not include runtime paths
do not include future fields
...
```

Prefer:

```text
DevelopmentFitBatch accepts only ModelVisibleRecord
FinalEvaluationBatch accepts only EvaluatorOwnedRecord
```

over relying mainly on:

```text
do not leak hidden truth into fit
```

Prefer:

```text
retry creates a new immutable attempt
```

over:

```text
replace=False
force=False
overwrite=False
```

The main instruction should describe the **positive closed shape**.

Negative instructions should be residual checks, not the primary semantic definition.

---

## 5. Planning Contract Closure Checklist

This checklist exists specifically to prevent the `T-01/R04` failure:

> Planning described broad allowed content but did not define the exact allowed semantic shape, forcing Execution either to generalize or to stop.

Apply this checklist to contract-heavy tasks that create schemas, identities, capability boundaries, persistence formats, evidence roles, scientific interfaces, or shared downstream APIs.

### 5.1 Complete shape

For every owned contract:

```text
[ ] What exactly is a valid value?
[ ] What exact fields / variants / states exist?
[ ] What are their types and constraints?
[ ] Is the allowed set complete, not merely a minimum?
[ ] What happens to unknown semantic fields: reject, separate extension boundary, or explicitly non-semantic?
```

### 5.2 Closed-world test

```text
[ ] Does the contract state "exact allowed set" rather than only "must contain"?
[ ] Are arbitrary semantic bags (`Mapping[str, Any]`, open metadata) absent from protected boundaries?
[ ] If open metadata is necessary, is it explicitly non-semantic and excluded from protected identities/evidence?
[ ] Are forbidden states absent from the representation when practical?
```

### 5.3 Two-implementation test

Ask:

> Can two materially different implementations both satisfy the written contract?

Example:

```text
A. typed hero/flop/context/action fields only
B. Mapping[str, Any] called "observable"
```

If both satisfy the text and the difference affects scientific meaning, evidence visibility, identity, persistence, authorization, or downstream interface behavior:

```text
PLANNING CONTRACT IS UNDERDETERMINED
```

Planning must specify further before Execution.

### 5.4 Semantic-owner test

For every remaining implementation choice:

```text
[ ] Is this semantic-neutral implementation detail?
    → Execution may choose simplest local shape.

[ ] Does it change valid data, scientific meaning, evidence visibility,
    identity, persistence semantics, authorization, or downstream API?
    → Planning or human authority must own it.
```

### 5.5 Downstream dependency test

```text
[ ] Will later tasks build on this contract?
```

If yes, unresolved ambiguity is material even if the current task could locally "make something work."

### 5.6 Simplicity check before adding a schema

Before creating a new payload/schema/extension object, ask:

```text
Can the open extension point simply be removed?
```

For `T-01/R04`, a possible simpler resolution may be that `StudyRecord` already owns typed hero/flop/context/action fields and needs no additional open `observable` bag at all.

This must be decided from the current scientific/evidence requirements, not future extensibility.

---

## 6. Readiness Contract Determinacy Check

Readiness should independently verify Planning closure.

Add a bounded question for contract-heavy tasks:

> Construct two materially different implementations that both satisfy the written contract.

If this is possible and the difference is semantically material:

```text
NEEDS REVISION
```

This is stronger and more concrete than asking only:

```text
"Is the plan detailed enough?"
```

### Readiness pass

For each contract-heavy task:

```text
[ ] exact allowed semantic shape identified
[ ] unknown-field policy identified
[ ] semantic owner identified
[ ] two materially different compliant implementations attempted
[ ] no material ambiguity remains
```

Do not use this to demand irrelevant implementation detail.

Apply Materiality/Simplicity:

```text
semantic ambiguity affecting downstream correctness → blocker
local formatting/internal neutral choice → not a blocker
```

---

## 7. Execution Semantic Choice Guard

Before implementing a contract-heavy slice, the execution model asks:

### Question 1

> Do I need to choose anything that changes valid data, scientific meaning, evidence visibility, identity, persistence semantics, authorization, or downstream interface behavior?

If `NO`:

```text
execute using the simplest local implementation
```

If `YES`, continue.

### Question 2

> Is that choice uniquely determined by current authoritative artifacts?

If `YES`:

```text
implement that choice literally
```

If `NO`:

```text
BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY
```

Do not infer the missing semantic contract from historical rejected designs.

Do not invent a "reasonable" schema.

Route the ambiguity to Planning/human authority.

---

## 8. Blocker locality rule

A semantic ambiguity should block the smallest dependency-complete unit.

For a corrective invocation containing several independent findings:

```text
for each finding independently:

if contract is sufficient:
    fix it

if correction requires new Planning/human-owned semantics:
    mark THIS finding:
    BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY

continue independent authorized findings
unless they depend on the blocked finding
```

Final status may be:

```text
R04 BLOCKED
R05 FIXED
R06 FIXED

T-01 overall:
NOT FROZEN / BLOCKED ON R04
```

Global stop is reserved for cases where:

- the ambiguity contaminates the whole task;
- later corrections depend on it;
- continuing could corrupt shared evidence or architecture;
- workflow authority explicitly requires stop.

This avoids wasting an authorized correction pass because of one independent ambiguity.

---

## 9. Execution Closure Checklist

The purpose of this checklist is to catch the exact failure class observed in T-01:

> the implementation satisfies positive requirements and passes its named test, but still accepts semantically invalid neighboring states.

### PASS A — Positive completion

```text
[ ] required types/components exist
[ ] exact required fields exist
[ ] allowed constructors work
[ ] required happy-path examples work
[ ] named task verification seam passes
```

### PASS B — Closed-world review

For each protected contract:

```text
[ ] Is the allowed field set exact, or only a required subset?
[ ] Can unknown semantic fields be accepted?
[ ] Can arbitrary Mapping/dict/metadata carry protected data?
[ ] Can one identity accept another identity's fields?
[ ] Can an unknown extra field change a canonical fingerprint?
[ ] Can a forbidden mode/state be represented through a flag/string/null?
[ ] Can protected data reach a forbidden consumer through another container?
[ ] Can operational paths/runtime details enter canonical identities?
```

### PASS C — nearest-wrong probes

Construct the most plausible almost-valid wrong values.

Examples from `CHG-0009/T-01`:

```text
final truth → DevelopmentFitBatch
final truth inside open observable Mapping
NumPy-only ProvenanceIdentity
ScientificConfigIdentity(os_version=...)
ProvenanceIdentity(unrelated_package_version=...)
canonical_worker_command(output_path=...)
non-flop ConditioningContextIdentity
```

Require rejection for the intended reason.

### PASS D — dependency stop

For a task creating a contract consumed by later tasks:

```text
task implementation
→ named seam PASS
→ bounded Task Closure Review
→ narrow correction if needed
→ task frozen
→ only then authorize dependent task
```

Do not make this universal for trivial leaf tasks.

---

## 10. Prefer deterministic complement checks over longer negative prompts

The preferred hierarchy is:

```text
1. make invalid state unrepresentable
2. exact schema validation
3. deterministic generated negative probes
4. short residual negative instruction
5. only then free-form reviewer reasoning
```

This reduces prompt burden for weaker models.

Candidate generated probes for exact schemas:

```text
remove required field
add unknown field
inject neighboring identity field
replace allowed variant with forbidden variant
add operational path to canonical identity
attempt forbidden role transition
```

---

## 11. Independent Task Closure Review

Field evidence suggests:

```text
implementation model self-test
!=
independent bounded review
```

Luna passed the named T-01 test seam while contract escapes remained.

For high-leverage contract-heavy tasks, test:

```text
weak model executes task
        ↓
task seam PASS
        ↓
fresh independent reviewer gets only:
  authoritative task contract
  changed files
  relevant tests
        ↓
PASS or narrow corrective findings
```

This is not another Formal Readiness cycle.

Constraints:

- no Roadmap replanning;
- no open-ended architecture search;
- no speculative improvements;
- findings must demonstrate a current reachable semantic escape;
- corrections remain inside the already authorized task unless a true Planning ambiguity is found.

---

## 12. Positive reviewer pattern

Instead of:

```text
find anything else wrong
```

use:

```text
For each protected contract:

1. enumerate the complete valid semantic shape;
2. identify direct consumers;
3. verify no wider shape is constructible;
4. attempt the nearest wrong construction;
5. confirm rejection;
6. identify whether any unresolved choice belongs to Planning/human authority;
7. stop.
```

This keeps review bounded and avoids another over-engineering loop.

---

## 13. Interaction with previous recommendations

### `REC-PL-CONTEXT-HANDOFF-001-v1`

Already covered:

- bounded current-state execution packet;
- durable history != active context;
- retrieval-on-demand.

`T-01` now provides positive field evidence:

```text
historical readiness required: NO
extra context required: NO
```

The new recommendation adds **semantic closure**, not more context.

### `REC-PL-MATERIALITY-SIMPLICITY-001-v1`

Already covered:

- evidence-gated necessity;
- simplest sufficient construction;
- stop rule;
- avoid speculative mechanisms.

The new recommendation applies the same principle inside APIs/contracts:

```text
remove representable invalid states
rather than add layers of prohibitions/guards
```

### `REC-PL-READINESS-001-v1`

Already covered executable readiness and the idea that traceability-complete is not execution-ready.

What was missing:

- an explicit **two-materially-different-implementations** determinacy test;
- complete allowed schema versus required minimum;
- Planning ownership of semantic closure.

### `REC-PL-WEAK-MODEL-EXECUTION-001-v1`

Already covered most of:

- positive closed shapes;
- exact schema idea;
- no arbitrary semantic bags;
- Task Closure Review;
- nearest-wrong probes;
- independent review;
- context bounding.

New in v2:

1. explicit explanation of **why** the checklist exists, grounded in T-01 failures;
2. Planning Contract Closure Checklist;
3. Readiness two-implementation determinacy test;
4. Execution Semantic Choice Guard;
5. blocker locality / smallest dependency-complete stop rule;
6. explicit treatment of `T01-R04` as a Planning gap;
7. stronger linkage between positive-command design and removal of open extension points.

---

## 14. Evaluation sequence

Do not productize all of this immediately.

### E1 — current Poker R04

Use Sol High Planning to resolve only the missing current observable schema.

Then return to Luna corrective Execution.

Observe whether the positive closed contract prevents recurrence.

### E2 — finish R05/R06 with blocker-locality behavior

In a future multi-finding correction, test whether an independent blocked finding still allows unrelated authorized corrections to proceed.

### E3 — next contract-heavy task

Add the Execution Closure Checklist to the prompt.

Measure whether Luna catches:

```text
required minimum + arbitrary extras
```

without independent review.

### E4 — independent closure comparison

Compare:

```text
task seam only
vs
task seam + bounded independent closure review
```

Capture Change Cost actuals.

---

## 15. Change Cost interaction

Capture:

```text
task implementation calls
task test attempts
closure-review calls
corrective iterations
Planning returns caused by underdetermined contracts
dependent-task rework avoided
```

The economic question remains:

> Is a small Planning/Task Closure check cheaper than letting an open contract propagate into dependent work?

Calibrate by task class rather than making the check universal.

---

## 16. Reusable checklist seed

```text
CONTRACT-HEAVY TASK

PLANNING CLOSURE
[ ] Complete valid semantic shape is defined
[ ] Allowed set is closed, not merely minimum-required
[ ] Unknown semantic field policy is explicit
[ ] Two materially different implementations cannot both satisfy the contract
[ ] Remaining semantic choices have an explicit owner
[ ] Open extension points were challenged for necessity

EXECUTION GUARD
[ ] No new semantics must be chosen
[ ] If semantics must be chosen, authoritative artifacts already determine them
[ ] Otherwise block only the dependent slice and route to Planning

TASK CLOSURE
[ ] Happy path passes
[ ] Unknown extra rejected
[ ] Neighboring identity field rejected
[ ] Protected value cannot cross role boundary
[ ] Forbidden mode/state is unrepresentable or rejected
[ ] Nearest wrong construction fails for intended reason

STOP
[ ] Independent authorized work continued where safe
[ ] No speculative hardening
[ ] No future task implementation
```

---

## 17. Anti-overreach

Do not immediately introduce:

- a universal lifecycle stage after every task;
- full schema code generation;
- a fuzzing framework;
- mandatory independent review for trivial tasks;
- enormous negative instruction lists;
- new dependencies;
- automatic Planning rewrites.

Start with checklists/prompts and contract-heavy fixtures.

Automate only repeated, well-understood failure patterns.

---

## 18. Recommended Roadmap disposition

Do not add a new major `PL-V38-*` stage solely for this recommendation.

Suggested path:

```text
Poker field work
→ collect contract-closure evidence
→ code-companion checklist/prompt seeds
→ PL-V38-05:
   bounded task/context policy
→ PL-V38-06B:
   weak-model execution + contract determinacy + Task Closure fixtures
→ PL-V38-07/08:
   automation only if measured evidence supports it
```

Before implementing new checklist/probe machinery, run the reusable code/research asset check.

---

## 19. Provisional conclusion

The field problem is not best solved by giving weaker models longer lists of prohibitions.

The stronger direction is:

```text
Planning defines the complete valid semantic shape
→ Readiness proves the contract is determinate
→ Execution refuses to invent missing semantics
→ invalid states are removed by construction where practical
→ nearest-wrong probes test the semantic complement
→ local ambiguities block only their dependency cone
→ dependent tasks wait until the contract is actually closed
```

This keeps prompts more positive and bounded while improving safety for weaker implementation models.
