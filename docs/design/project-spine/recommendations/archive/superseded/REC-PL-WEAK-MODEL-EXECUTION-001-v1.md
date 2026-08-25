# REC-PL-WEAK-MODEL-EXECUTION-001 v1
## Closed-by-construction execution contracts, positive task packets, and bounded post-task review for weaker implementation models

**Status:** `PROVISIONAL / FIELD-DERIVED / OPEN`
**Date:** `2026-08-21`
**Primary field source:** Poker `CHG-0009-bayesian-study-harness`, Execution `T-01` with Luna 5.6
**Implementation authority:** none
**Recommended canonical location:** `docs/design/project-spine/REC-PL-WEAK-MODEL-EXECUTION-001-v1.md`
**Related recommendations:** `REC-PL-CONTEXT-HANDOFF-001-v1`, `REC-PL-MATERIALITY-SIMPLICITY-001-v1`, `REC-PL-READINESS-001-v1`, `REC-PL-CHANGE-COST-001-v1`

---

## 1. Field observation

`CHG-0009` reached formal `READY` after exhaustive Readiness and a Materiality/Simplicity simplification pass.

The first authorized execution slice, `T-01`, was deliberately bounded for Luna 5.6:

```text
one task
→ small current-context packet
→ exact allowed files
→ exact verification seam
→ no historical Readiness by default
→ stop before T-02
```

This part worked well.

The model reported:

```text
historical readiness needed: NO
extra context required: NO
execution friction: NONE
T-01 contract test: PASS
```

An independent bounded source review nevertheless found contract escapes.

### First corrective review

The initial implementation allowed:

1. final/evaluator truth to remain structurally reachable from model-visible records;
2. `ProvenanceIdentity` to be instantiated with materially incomplete provenance;
3. a generic `ConditioningContextIdentity` that accepted non-flop/incomplete-flop contexts despite the current protocol being fixed-flop.

These were corrected.

### Second corrective review

The corrected implementation still allowed:

1. hidden/final truth to be smuggled through an arbitrary `Mapping[str, Any]` observable payload;
2. provenance/environment fields to be placed inside `ScientificConfigIdentity`;
3. arbitrary extra fields to enter `ProvenanceIdentity` and therefore alter its fingerprint;
4. operational output paths to enter `canonical_worker_command`, reopening a previously eliminated provenance/hash/path cycle.

The recurring implementation pattern was:

```text
"these fields must exist"
implemented as
"these fields are the required minimum"

instead of

"these are the complete allowed semantics;
no other semantically meaningful fields/states are representable"
```

This is a materially different problem from missing context or failed planning.

---

## 2. Core diagnosis

For weaker implementation models, positive requirements are often handled better than **closed-world constraints**.

The model can follow:

```text
include A
include B
include C
```

while still implementing:

```text
A + B + C + arbitrary extras
```

Likewise, a nominal type boundary is not sufficient if an open payload reintroduces the forbidden information:

```text
typed StudyRecord
    ↓
observable: Mapping[str, Any]
    ↓
hidden truth can still be encoded
```

Therefore:

```text
typed classes != structural isolation
required fields != closed schema
a test seam PASS != task contract closure
```

The important weakness is not merely "the model ignores negative instructions."

The deeper issue is:

> **The implementation may preserve the named positive structure while leaving the semantic complement unconstrained.**

---

## 3. Recommendation

Planning Lite should evaluate a **Weak-Model Execution Contract** built around three complementary ideas:

```text
A. POSITIVE CLOSED SHAPE
   describe exactly what valid structure is

B. DENY BY CONSTRUCTION
   make invalid semantic states difficult or impossible to represent

C. BOUNDED POST-TASK ADVERSARIAL CHECK
   after the task test passes, explicitly probe the complement of the contract
```

The goal is not to make execution prompts longer.

The goal is to replace long negative prose with smaller constructive contracts plus cheap mechanical/adversarial checks.

---

## 4. Positive-command principle

Prefer:

```text
The only accepted fields are:
A
B
C

Construct the value from this exact closed schema.
Unknown fields are invalid.
```

over:

```text
Include A/B/C.
Do not include X.
Do not include Y.
Do not include Z.
Do not include future fields.
Do not include operational fields.
...
```

Prefer:

```text
ExecutableEnvelope can be constructed only from:
RecoveryConfig | DryRunConfig
```

over:

```text
OfficialStudyHandoffConfig must not execute.
Do not accidentally treat handoff as executable.
Do not expose it through generic config.
...
```

Prefer:

```text
DevelopmentFitBatch accepts only ModelVisibleRecord
FinalEvaluationBatch accepts only EvaluatorOwnedRecord
```

over:

```text
Do not leak evaluator truth into fit.
Do not put hidden truth into observable.
Do not convert final batches to development batches.
...
```

This is a **positive closure** pattern:

> state the complete allowed shape first; use negative statements only for the small set of residual failure modes that cannot be eliminated structurally.

---

## 5. Closed-by-construction patterns

### 5.1 Exact schemas, not minimum schemas

For identity/config payloads:

```text
set(actual_keys) == set(approved_keys)
```

not:

```text
approved_keys <= actual_keys
```

Unknown semantically significant fields must fail closed.

Candidate implementation patterns include:

- frozen dataclasses with explicit fields;
- TypedDict / schema objects with exact-extra rejection;
- Pydantic models configured to forbid extras;
- explicit parser/constructor functions that reject unknown keys;
- canonical serialization derived only from declared fields.

Planning Lite should not mandate a library; it should mandate the semantic property.

### 5.2 No arbitrary semantic bags at protected boundaries

Avoid:

```python
Mapping[str, Any]
dict[str, Any]
metadata: dict
extras: dict
```

inside boundaries whose purpose is semantic isolation.

If an open metadata field is truly required:

- it must be explicitly non-semantic;
- it must not participate in scientific/config/provenance fingerprints unless specified;
- it must not carry protected truth;
- it should be isolated from model-visible or fit-visible payloads.

### 5.3 Capabilities instead of mode flags

Prefer sealed capability types:

```text
RecoveryConfig
DryRunConfig
OfficialStudyHandoffConfig
```

with executable constructors accepting only executable capability types.

Avoid generic:

```text
mode="recovery" | "dry-run" | "official"
count=...
seed=...
```

where forbidden combinations remain representable.

### 5.4 Mode-specific identities

If a mode does not have a semantic value, do not encode absence as:

```text
null
""
fake hash
sentinel pretending to be a hash
```

Prefer an explicit mode-specific variant:

```text
RecoveryNoDevelopmentState
DevelopmentStateHash(...)
```

### 5.5 Make invalid transitions absent

Prefer:

```text
retry → create_new_attempt()
```

when replacement is forbidden.

Do not implement:

```text
replace=False
force=False
allow_overwrite=False
```

if the simpler API can omit replacement entirely.

This applies the Materiality/Simplicity recommendation at the API-contract level.

---

## 6. Execution task packet for weaker models

A task packet should be **small, constructive, and exact**.

Candidate order:

```text
1. exact authorization
2. task outcome
3. allowed files/surface
4. current authoritative context only
5. exact positive contract shapes
6. exact verification seam
7. bounded stop point
8. small residual negative list
```

Avoid giving the implementation model:

- historical Readiness by default;
- obsolete rejected designs;
- full change archaeology;
- large lists of old blockers after the current contract already resolves them.

This preserves the successful field result from `T-01`:

```text
bounded current-state packet sufficient: YES
historical readiness required: NO
```

---

## 7. Negative constraints: minimize prose, maximize executable complement checks

Negative constraints still matter.

The recommendation is **not** to delete them.

Instead, move as many as possible from prose into one of:

```text
closed schema
type boundary
constructor boundary
sealed capability
exact-key validation
state-transition shape
negative executable test
direct adversarial probe
```

Example:

Instead of relying mainly on:

```text
Do not place provenance fields in ScientificConfigIdentity.
```

define:

```text
ScientificConfigIdentity = exact approved scientific field set
ProvenanceIdentity = exact approved provenance field set
```

and add a test:

```text
ScientificConfigIdentity(os_version="Windows") → reject
```

The positive contract determines the implementation.
The negative probe verifies closure.

---

## 8. Proposed Execution Closure Checklist

Do not immediately add this as a new Planning Lite architecture layer.

First simulate it in prompts/fixtures.

### PASS A — Positive completion

After implementation, verify:

```text
[ ] required types/components exist
[ ] exact required fields exist
[ ] allowed constructors work
[ ] required happy-path examples work
[ ] named task verification seam passes
```

### PASS B — Closed-world review

For every protected contract boundary ask:

```text
[ ] Is the allowed field set exact, or merely a required subset?
[ ] Can arbitrary Mapping/dict/metadata carry semantically protected data?
[ ] Can an unknown extra field change a canonical fingerprint?
[ ] Can one semantic identity accept another identity's fields?
[ ] Can a forbidden mode/state still be represented by a flag/string/null?
[ ] Can a protected value reach a forbidden consumer through another container?
[ ] Can an operational path/runtime detail enter a scientific/provenance identity?
[ ] Can a forbidden state transition still be requested even if default=False?
```

### PASS C — Nearest-wrong direct probes

For each contract, construct at least one implementation that is **almost valid but wrong**.

Examples from T-01:

```text
final truth → DevelopmentFitBatch
NumPy-only ProvenanceIdentity
ScientificConfigIdentity(os_version=...)
ProvenanceIdentity(unrelated_package_version=...)
canonical_worker_command(output_path=...)
non-flop ConditioningContextIdentity
```

The check is not complete until the nearest wrong implementation is rejected for the intended reason.

### PASS D — Dependency stop

If the current task owns a contract used by later tasks:

```text
task PASS
→ bounded independent contract review
→ correction if needed
→ freeze task
→ only then authorize dependent task
```

Do not require this for every trivial task.

Use it when the task creates:

- schemas;
- identities;
- permission/capability boundaries;
- persistence formats;
- public/internal interfaces;
- scientific/evidence contracts;
- state machines consumed by downstream tasks.

---

## 9. Independent review versus self-review

The T-01 field evidence suggests:

```text
implementation model self-test
≠
independent bounded review
```

The implementation model passed its own named test seam while leaving contract escapes.

Therefore Planning Lite should test a lightweight pattern:

```text
weak model executes task
        ↓
task seam PASS
        ↓
fresh/independent bounded reviewer sees only:
  task contract
  changed files
  relevant tests
        ↓
PASS or narrow corrective findings
```

This is not another full Readiness cycle.

It is a **Task Closure Review**.

Candidate constraints:

- no Roadmap replanning;
- no open-ended architecture search;
- no speculative improvements;
- review only the task-owned contract surface;
- findings must point to a concrete reachable escape;
- corrections remain inside the already authorized task.

---

## 10. Positive reviewer prompt pattern

Instead of telling the reviewer to search arbitrarily for mistakes:

```text
For each protected contract:
1. enumerate the complete valid semantic shape;
2. enumerate the direct consumers;
3. verify no other shape can be constructed;
4. attempt the nearest wrong construction;
5. confirm rejection;
6. stop.
```

This keeps the reviewer bounded and constructive.

---

## 11. Potential implementation strategies to evaluate

Planning Lite should test several alternatives rather than immediately choosing one.

### Strategy A — Prompt-only execution checklist

Cheapest first experiment.

Add the four execution passes to weak-model task prompts.

Pros:
- no product code;
- easy to test.

Risk:
- the same model may still confirm its own mistake.

### Strategy B — Generated negative probes from exact schemas

If a contract declares exact fields/types, deterministically generate tests for:

- missing fields;
- extra fields;
- cross-identity field injection;
- wrong variants;
- forbidden transitions.

Pros:
- reduces dependence on model creativity;
- cheap once schema is explicit.

Risk:
- only catches violations expressible from the schema.

### Strategy C — Fresh independent Task Closure Review

A new model call/reviewer gets only:

- authoritative task contract;
- changed files;
- task tests.

Pros:
- field evidence already supports value;
- avoids author self-review bias.

Risk:
- additional tokens/latency.

This cost should be measured against the downstream cost of letting a bad contract reach dependent tasks.

### Strategy D — Contract mutation probes

For contract-heavy tasks, automatically mutate valid payloads:

```text
add unknown field
remove required field
swap identity field
replace variant
inject protected value
alter mode
add output path
```

and require rejection.

Pros:
- directly targets the T-01 failure pattern.

Risk:
- should remain bounded; not full fuzzing by default.

### Strategy E — Schema ownership + code generation

Where suitable, define a canonical schema once and generate:

- validation;
- serialization;
- negative field checks;
- maybe typed structures.

Pros:
- fewer opportunities for model-written drift.

Risk:
- could become new framework complexity; use only if repeated evidence justifies it.

---

## 12. Recommended experimental sequence

Do not productize all strategies at once.

### E1 — prompt-only checklist

Use the next contract-heavy Poker task or a synthetic fixture.

Measure whether the implementation model catches its own extra-field/open-mapping errors.

### E2 — independent closure review

Compare:

```text
task seam only
vs
task seam + independent bounded review
```

Measure:
- additional tokens/tool calls;
- defects caught before next task;
- false-positive corrections;
- downstream rework avoided.

### E3 — deterministic mutation probes

Apply only to exact-schema/capability tasks.

Measure whether direct probes catch the recurring "required minimum + arbitrary extras" pattern.

### E4 — decide architecture

Only after several fixtures decide whether Planning Lite needs:

- a reusable execution checklist;
- a Task Closure workflow;
- generated contract probes;
- or only prompt templates/code-companion seeds.

---

## 13. Change Cost interaction

This recommendation should connect to `REC-PL-CHANGE-COST-001-v1`.

Capture actuals:

```text
task implementation calls
task test attempts
closure-review calls
corrective iterations
files changed
negative probes added
dependent-task rework avoided
```

The key economic question:

> Is one small closure review cheaper than allowing a contract defect to propagate into T-02/T-03/...?

Do not assume yes universally.

Calibrate by task type.

Likely high-value task classes:

```text
schema/contract
identity
authorization
scientific boundary
persistence format
state machine
shared interface
```

Likely low-value classes:

```text
small docs
isolated formatting
simple local refactor
leaf implementation with no downstream contract
```

---

## 14. Context Handoff interaction

This recommendation reinforces `REC-PL-CONTEXT-HANDOFF-001-v1`.

The T-01 field result supports:

```text
current authoritative packet
+ exact task
+ relevant sections
```

over:

```text
entire Planning/Readiness history
```

The independent Task Closure reviewer should also receive a fresh bounded packet:

```text
task contract
changed files
task test
current invariants
```

Historical reviews are retrieval-on-demand only.

---

## 15. Materiality/Simplicity interaction

Do not let Task Closure Review become a new over-engineering generator.

Every corrective finding must be:

```text
CURRENT
REACHABLE
MATERIAL TO THE TASK CONTRACT
BOUNDED TO THE AUTHORIZED TASK
```

No future-proofing.

Prefer removing representable invalid states over adding guards around them.

Example:

```text
bad:
generic config + many "official=false" checks

better:
OfficialStudyHandoffConfig is not executable by type
```

This is simultaneously:

- safer for weak models;
- easier to review;
- lower Change Cost.

---

## 16. Candidate semantic units

| Unit | Recommendation | State | Candidate destination |
|---|---|---|---|
| `REC-PL-WEAK-MODEL-EXECUTION-001/U1` | Distinguish **required-field presence** from **closed-schema exactness**. Contract-heavy execution should prefer exact allowed schemas. | `FIELD_CONFIRMED` | execution checklist / contract guidance |
| `.../U2` | Protected semantic boundaries should not contain arbitrary semantic bags (`Mapping[str, Any]`, open metadata) unless explicitly non-semantic. | `FIELD_CONFIRMED` | contract guidance |
| `.../U3` | Prefer positive, closed constructions over long negative prohibition lists. | `STRONG CANDIDATE` | task prompt template |
| `.../U4` | Move negative semantics into constructors/types/exact-key validation/tests where possible. | `STRONG CANDIDATE` | execution template / code seeds |
| `.../U5` | A task verification seam passing does not prove closure of a contract consumed by downstream tasks. | `FIELD_CONFIRMED` | task closure policy |
| `.../U6` | Contract-heavy tasks should receive bounded independent review before authorizing dependency-linked tasks. | `TO TEST / FIELD-SUPPORTED` | execution experiment |
| `.../U7` | Use nearest-wrong constructions as explicit negative probes. | `FIELD-SUPPORTED` | test/checklist seed |
| `.../U8` | Fresh reviewers should receive a bounded task packet, not historical lifecycle archaeology. | `FIELD-CONFIRMED FOR T-01 / TO GENERALIZE` | context handoff |
| `.../U9` | Corrections found by Task Closure Review stay inside the authorized task; they do not automatically return to Planning. | `STRONG CANDIDATE` | lifecycle semantics |
| `.../U10` | Measure closure-review cost versus downstream rework before making it universal. | `STRONG CANDIDATE` | Change Cost / eval |

---

## 17. Reusable checklist seed

Candidate for the Planning Lite code companion:

```text
EXECUTION CONTRACT CLOSURE

For every contract owned by this task:

POSITIVE SHAPE
[ ] What exact valid values/types/fields exist?
[ ] Are constructors limited to those values?
[ ] Does the happy path pass?

CLOSED WORLD
[ ] Are unknown fields rejected?
[ ] Are protected semantics impossible to smuggle through open maps/metadata?
[ ] Are identity schemas mutually exclusive?
[ ] Are forbidden states absent rather than represented by flags/nulls?
[ ] Can operational details enter canonical identities unexpectedly?

NEAREST WRONG
[ ] Add one unknown field → reject
[ ] Remove one required field → reject
[ ] Inject a neighboring identity's field → reject
[ ] Attempt a forbidden role transition → reject
[ ] Attempt the most plausible wrong mode/state → reject

STOP
[ ] No speculative hardening
[ ] No future task implementation
[ ] No new architecture unless the current task contract is impossible
```

---

## 18. Reusable prompt seed for weaker models

```text
Implement exactly the allowed semantic shape below.

Do not generalize the schema.

For each contract:
1. define the complete allowed fields/types;
2. reject unknown fields;
3. make forbidden states unrepresentable when practical;
4. add the happy-path test;
5. add nearest-wrong rejection tests;
6. stop when the current task contract is satisfied.

If the authoritative task does not define the complete allowed semantic shape,
do not invent it. Return BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY.
```

This intentionally uses positive construction as the main instruction and keeps the negative language compact.

---

## 19. What not to do

Do not immediately introduce:

- a universal extra lifecycle stage after every task;
- a general fuzzing framework;
- a schema compiler;
- a new dependency;
- a second Readiness system;
- mandatory independent review for trivial leaf tasks;
- enormous negative prompt lists.

The field problem should first be addressed with the cheapest mechanisms that can be evaluated.

---

## 20. Recommended Roadmap disposition

Do not add a new major `PL-V38-*` stage solely for this recommendation.

Recommended path:

```text
current Poker field work
→ collect T-01/T-02/... closure evidence
→ store prompt/checklist seeds in code companion
→ PL-V38-05:
   context/task packet policy
→ PL-V38-06B:
   weak-model execution + task-closure fixtures
→ PL-V38-07/08:
   automate only if evidence supports it
```

Also apply the existing reusable-asset check before implementation: inspect the Planning Lite code companion / lab for already existing checklist, validation, or negative-probe machinery.

---

## 21. Provisional conclusion

The T-01 experiment suggests that weaker models can execute a well-frozen task with a compact context packet, but contract-heavy tasks need an additional notion of **semantic closure**.

The preferred direction is not:

```text
write more prohibitions
```

but:

```text
define the complete valid shape
→ make invalid states hard to represent
→ mechanically probe the nearest invalid shapes
→ independently review only the task-owned contract
→ then authorize dependent work
```

This may improve correctness while keeping prompts and downstream context smaller.
