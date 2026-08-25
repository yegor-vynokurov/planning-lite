# REC-PL-WEAK-MODEL-EXECUTION-001 v3
## Four-layer contract closure for weak-model execution:
## shape, semantics, encoding, ownership

**Status:** `PROVISIONAL / FIELD-DERIVED / STRONG CANDIDATE`
**Date:** `2026-08-21`
**Primary field source:** Poker `CHG-0009-bayesian-study-harness`, Planning/Readiness/Execution around `T-01` with Luna 5.6 and Sol High
**Supersedes:** `REC-PL-WEAK-MODEL-EXECUTION-001-v2`
**Implementation authority:** none
**Recommended canonical location:**
`docs/design/project-spine/REC-PL-WEAK-MODEL-EXECUTION-001-v3.md`

**Related recommendations:**
- `REC-PL-CONTEXT-HANDOFF-001-v1`
- `REC-PL-MATERIALITY-SIMPLICITY-001-v1`
- `REC-PL-READINESS-001-v1`
- `REC-PL-CHANGE-COST-001-v1`

---

# 1. Why this recommendation exists

This recommendation exists because the Poker field pilot repeatedly showed that a formally detailed plan can still leave a weaker implementation model with semantic choices that should not belong to Execution.

The observed failure was not simply:

```text
the model ignored instructions
```

and not simply:

```text
the model needed more context
```

The bounded-context experiment actually worked well:

```text
one authorized task
→ current authoritative packet only
→ historical Readiness not needed
→ no extra context needed
→ low execution friction
```

The deeper problem was that some contracts were only **partially closed**.

A weaker model often handled positive requirements correctly:

```text
A must exist
B must exist
C must exist
```

while still leaving:

```text
A + B + C + arbitrary extras
```

representable.

Later iterations exposed three further forms of the same problem:

```text
the allowed shape is closed,
but the meaning is still ambiguous;

the meaning is closed,
but two canonical byte encodings are still legal;

the bytes are closed,
but task/component ownership of runtime derivation is still ambiguous.
```

Therefore Planning Lite needs a stronger notion of **execution-ready contract closure**.

---

# 2. Field evidence from CHG-0009 / T-01

## 2.1 Shape escape

Initial `StudyRecord` contract could carry final/evaluator truth directly or through an open:

```python
Mapping[str, Any]
```

The implementation could therefore satisfy the named type structure while still violating evidence-role isolation.

The eventual Planning repair removed the open extension point entirely:

```text
StudyRecord =
    context
    + action
```

No observable bag.
No features bag.
No metadata bag.

This was better than adding a growing blacklist.

---

## 2.2 Semantic closure gap

`ScientificConfigIdentity` and `ProvenanceIdentity` were initially modeled as identity objects with some required fields, but their complete semantic content was not uniquely fixed.

This allowed:

```text
ScientificConfigIdentity(os_version=...)
```

or:

```text
ProvenanceIdentity(required_fields..., unrelated_extra=...)
```

to remain constructible.

The issue was:

```text
required minimum
!=
complete semantic identity
```

Planning later closed the exact semantic sets.

---

## 2.3 Encoding closure gap

Even after field sets were closed, Formal Readiness found that a single semantic state could still produce multiple legal canonical hashes.

Examples:

```text
flat vs nested JSON
dry-run vs dry_run
-1 vs -1.0
different source manifest inclusion rules
different environment derivation APIs
```

This mattered because:

```text
canonical bytes
→ config_hash / provenance_hash
→ artifact addresses
```

Therefore semantically equivalent but byte-different representations were material.

Planning had to define:

```text
exact JSON shape
exact key names
exact scalar types
exact literals
exact derivation sources
exact canonical bytes
golden hashes
```

This created **encoding closure**.

---

## 2.4 Ownership closure gap

After RD-01/RD-02 were closed, another ambiguity appeared.

T-01 owned:

```text
pure contracts
schemas
canonical serialization
fingerprints
controlled fixtures
```

T-06 owned:

```text
actual Git/filesystem/environment/data/native-absence collection
runtime ProvenanceIdentity assembly
artifact persistence
```

But wording such as "runtime derivation probes" could have caused Luna to implement T-06 responsibilities early inside T-01.

Formal Readiness therefore had to freeze ownership:

```text
T-01:
pure contract + controlled facts

T-06:
actual runtime collection
```

This produced the fourth closure layer:

```text
OWNERSHIP CLOSURE
```

---

# 3. Core model: Four-layer Contract Closure

A contract-heavy task is not execution-ready merely because it has named types and required fields.

Planning Lite should evaluate four distinct closure layers.

```text
1. SHAPE CLOSURE
   What values/fields/states can exist?

2. SEMANTIC CLOSURE
   What exactly do those values mean?

3. ENCODING CLOSURE
   What unique canonical representation corresponds to that meaning?

4. OWNERSHIP CLOSURE
   Which task/component is responsible for constructing/deriving each value?
```

All four matter only where applicable.

A simple local function may need none of them formally.

A scientific identity, persistence schema, evidence boundary or cross-task interface may need all four.

---

# 4. Closure layer 1: Shape Closure

## Question

> Is the complete allowed structural shape defined?

Not:

```text
must contain A/B/C
```

but:

```text
the allowed shape is exactly A/B/C
```

## Checklist

```text
[ ] Complete allowed fields/variants/states are explicit.
[ ] Exact types and cardinality constraints are explicit.
[ ] Unknown semantic fields have an explicit policy.
[ ] Required fields are not merely a minimum subset.
[ ] Open Mapping/dict/metadata bags are absent from protected boundaries
    unless explicitly non-semantic.
[ ] Forbidden states are removed from the representation where practical.
```

## Positive-command pattern

Prefer:

```text
StudyRecord = exactly {context, action}
```

over:

```text
StudyRecord has context/action;
do not put truth/features/metadata/etc. in it.
```

---

# 5. Closure layer 2: Semantic Closure

## Question

> Does every allowed field/state have one current approved meaning?

A closed field set can still be semantically ambiguous.

Example:

```text
true_hypothesis_id
```

may look typed but still require a choice between:

```text
string
integer
card tuple
axis index
opaque ID
```

if ownership/meaning is not specified.

## Checklist

```text
[ ] Each semantic field has one authoritative current meaning.
[ ] Neighboring identities cannot absorb each other's semantics.
[ ] Current scientific/evidence/authorization choices are already fixed.
[ ] No future-generalization field is included merely "for later".
[ ] Remaining semantic choices have an explicit owner:
    Planning / Human / Execution-neutral.
```

## Semantic Choice Guard

Execution asks:

```text
Does this implementation require choosing something that changes:
- valid data,
- scientific meaning,
- evidence visibility,
- identity,
- persistence,
- authorization,
- downstream API semantics?
```

If `NO`:

```text
Execution may choose the simplest local implementation.
```

If `YES`:

```text
Is the choice already uniquely fixed by authoritative artifacts?

YES → implement literally
NO  → BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY
```

Execution must not invent the missing semantic contract.

---

# 6. Closure layer 3: Encoding Closure

## Why this exists

For ordinary internal objects, multiple equivalent encodings may be harmless.

For canonical identities, hashes, manifests, content-addressed paths or persisted evidence, they are not.

If:

```text
same semantic state
→ two valid byte encodings
→ two hashes
```

then the identity contract is underdetermined.

## Checklist

Apply when bytes/hashes/persistence are semantically material.

```text
[ ] Exact object nesting is fixed.
[ ] Exact key names are fixed.
[ ] Exact scalar JSON types are fixed.
[ ] Exact string literals are fixed.
[ ] Mode aliases are forbidden unless explicitly canonicalized.
[ ] Array ordering is fixed.
[ ] Optional/presence rules are fixed.
[ ] Authoritative derivation sources are fixed.
[ ] Path normalization / manifest ordering are fixed where relevant.
[ ] One semantic state produces exactly one canonical byte sequence.
[ ] Golden byte/hash fixtures exist for representative values.
```

## Two-byte test

Attempt:

```text
flat vs nested
dry-run vs dry_run
1 vs 1.0
string seed vs integer seed
alternate file-set rule
alternate environment API
alternate module spelling
```

If two remain valid for the same semantic state:

```text
ENCODING NOT CLOSED
```

---

# 7. Closure layer 4: Ownership Closure

## Why this exists

Even if shape, meaning and encoding are fixed, a weaker model may still implement a future task early if it is not clear who derives the values.

Example from CHG-0009:

```text
T-01:
schema/serialization/fingerprint

T-06:
actual Git/filesystem/environment collection
```

Without explicit ownership, Luna could reasonably implement Git probing inside `contracts.py`.

## Checklist

```text
[ ] Each derived/runtime value has an owning task/component.
[ ] Pure schema ownership is separated from runtime collection ownership.
[ ] A task does not need future modules/files merely to verify its contract.
[ ] Controlled fixtures are distinguished from live derivation.
[ ] Downstream responsibilities are not pulled into an earlier task.
[ ] Verification wording does not accidentally require future ownership.
```

## Ownership determinacy test

Ask:

> Can two task allocations both satisfy the current plan?

Example:

```text
A. T-01 defines provenance schema; T-06 collects environment.
B. T-01 also probes Git/filesystem/environment directly.
```

If both satisfy the text and change blast radius/task dependency semantics:

```text
OWNERSHIP NOT CLOSED
```

---

# 8. Planning Contract Closure Checklist

Use for contract-heavy tasks only.

Typical candidates:

```text
schema
identity
scientific/evidence interface
persistence format
authorization/capability boundary
state machine
shared downstream API
canonical serialization
artifact addressing
```

## Planning pass

```text
SHAPE
[ ] Complete allowed shape defined?
[ ] Unknown semantic fields policy explicit?
[ ] Open extension points challenged for necessity?

SEMANTICS
[ ] Each field/state has one current approved meaning?
[ ] Remaining semantic decisions have an explicit owner?
[ ] No future-generalization semantics added?

ENCODING
[ ] If canonical bytes/hashes matter, is representation unique?
[ ] Exact literals/types/order/derivation sources fixed?
[ ] Golden fixtures supplied where useful?

OWNERSHIP
[ ] Which task/component derives each runtime value?
[ ] Pure contract and live observation responsibilities separated?
[ ] Verification can run without implementing future tasks?
```

---

# 9. Readiness Contract Determinacy Check

Formal Readiness should challenge each relevant closure layer.

The main method:

> Construct two materially different implementations that both satisfy the written contract.

If both are legal and the difference affects current correctness, evidence, identity, persistence, authorization or task ownership:

```text
NEEDS REVISION
```

Examples discovered in CHG-0009:

```text
typed record vs record + arbitrary Mapping
flat vs nested canonical JSON
dry-run vs dry_run
exact source list vs vague "relevant files"
T-01 pure provenance contract vs T-01 runtime collector
```

This is stronger than asking:

```text
"Is the plan detailed enough?"
```

---

# 10. Execution Closure Checklist for weaker models

The implementation prompt should stay constructive and bounded.

## PASS A — Positive shape

```text
[ ] Required types/components exist.
[ ] Allowed constructors work.
[ ] Approved happy path works.
[ ] Named task seam passes.
```

## PASS B — Closed-world check

```text
[ ] Exact allowed set, not minimum subset.
[ ] Unknown semantic field rejected.
[ ] Open Mapping/metadata cannot carry protected semantics.
[ ] Neighboring identity fields rejected.
[ ] Operational data cannot enter canonical identities.
[ ] Forbidden state is absent or rejected.
```

## PASS C — Nearest-wrong probes

For every important boundary, construct one almost-valid wrong case.

Examples:

```text
truth → fit batch
extra identity field
wrong mode literal
output_path inside canonical worker command
alternate nesting
wrong scalar type
forbidden role transition
```

## PASS D — Ownership guard

```text
[ ] Did this task implement only its owned derivation/behavior?
[ ] Did verification accidentally pull a downstream task forward?
[ ] Were controlled fixtures used where live collection belongs later?
```

## PASS E — Dependency stop

If the task owns a contract consumed downstream:

```text
implementation
→ task seam PASS
→ bounded closure review
→ correction if needed
→ freeze
→ authorize dependent task
```

Do not require this for every trivial leaf task.

---

# 11. Blocker locality rule

A local ambiguity should block only its dependency cone.

For a multi-finding corrective call:

```text
for each finding independently:

if current contract is sufficient:
    fix it

if new Planning/Human semantics are required:
    mark that finding BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY

continue independent authorized findings
unless they depend on the blocked finding
```

Example:

```text
R04 BLOCKED
R05 FIXED
R06 FIXED
```

is preferable to abandoning all work merely because R04 is blocked.

Global stop is justified only when the ambiguity contaminates the whole task or shared evidence.

---

# 12. Positive commands over prohibition lists

The central prompt-design recommendation remains:

```text
define what is valid
rather than enumerate everything invalid
```

Preferred hierarchy:

```text
1. invalid state unrepresentable
2. exact closed schema
3. exact canonical encoding
4. explicit ownership
5. deterministic nearest-wrong probes
6. short residual negative prose
7. free-form adversarial reasoning last
```

This is particularly valuable for weaker models because it reduces the burden of remembering a long complement set.

---

# 13. Independent Task Closure Review

CHG-0009 field evidence showed:

```text
implementation model self-test
!=
independent bounded contract review
```

Luna initially passed the named T-01 seam while semantic escapes remained.

Planning Lite should therefore evaluate a lightweight pattern for high-leverage contract tasks:

```text
weak model executes task
        ↓
named seam PASS
        ↓
fresh bounded reviewer sees:
  authoritative task contract
  changed files
  relevant tests
        ↓
PASS or narrow corrective findings
```

This is not another Formal Readiness stage.

Constraints:

```text
no Roadmap replanning
no speculative architecture search
no future-proofing
current reachable escape required
correction stays inside task unless true Planning ambiguity is found
```

---

# 14. Context Handoff interaction

The same T-01 case also produced positive evidence for bounded context.

Execution succeeded without loading historical Readiness.

Therefore:

```text
durable history
!=
active execution context
```

Recommended weak-model packet:

```text
current lifecycle state
current task
current authoritative contract
allowed file surface
verification seam
stop point
```

Historical blockers/rejected designs are retrieval-on-demand only.

---

# 15. Materiality/Simplicity interaction

Closure must not become a new machinery generator.

For every proposed closure mechanism ask:

```text
Can we delete the extension point instead?
Can invalid state be made unrepresentable?
Can an exact small enum/list replace a generalized registry?
Can controlled fixture data replace live collection at this task?
```

CHG-0009 positive examples:

```text
remove observable Mapping entirely
instead of blacklist;

exact ten-file source manifest
instead of generic discovery framework;

canonical empty data manifest
instead of future data registry.
```

---

# 16. Change Cost interaction

Capture actual cost of closure:

```text
Planning closure iterations
Readiness iterations
weak-model corrective calls
independent closure reviews
negative probes added
dependent-task rework avoided
```

The key economic question:

> For which task classes is closure review cheaper than downstream propagation of an open contract?

Likely high-value classes:

```text
identity
schema
evidence boundary
scientific interface
persistence
authorization
shared state machine
canonical artifact addressing
```

Do not make closure review universal before calibration.

---

# 17. Candidate eval fixtures from CHG-0009

CHG-0009 T-01 now provides a useful real regression suite.

## Shape fixture

Bad:

```text
StudyRecord(context, action, observable=Mapping)
```

Expected:

```text
reject / impossible
```

## Semantic fixture

Bad:

```text
ScientificConfigIdentity(os_version=...)
```

Expected:

```text
reject
```

## Encoding fixture

Bad:

```text
mode="dry_run"
```

when canonical is:

```text
mode="dry-run"
```

Expected:

```text
reject / non-canonical
```

## Provenance fixture

Bad:

```text
canonical_worker_command(output_path=...)
```

Expected:

```text
reject
```

## Ownership fixture

Bad:

```text
T-01 implements live Git/filesystem/environment collection
```

Expected:

```text
out-of-scope;
T-06 owns runtime collection
```

These are more valuable than synthetic examples because they come from actual execution failures/ambiguities.

---

# 18. Proposed experimental sequence

Do not productize the full model immediately.

## E1 — corrective T-01 with four-layer checklist

Give Luna the now closed contract.

Measure whether its own nearest-wrong probes catch defects before independent review.

## E2 — independent Task Closure Review

Review only T-01 delta.

Compare:

```text
self-check result
vs
independent review result
```

## E3 — next contract-heavy task

Apply the same four-layer checklist prospectively.

Measure whether Planning/Readiness catch ambiguity before Execution.

## E4 — blocker locality

When a future corrective call contains one blocked and one independent finding, confirm the model continues safe independent work.

## E5 — automation decision

Only after multiple fixtures decide whether to automate:

- exact-schema negative probes;
- golden-byte checks;
- contract mutation tests;
- ownership checks.

---

# 19. Reusable compact checklist

```text
FOUR-LAYER CONTRACT CLOSURE

SHAPE
[ ] Complete allowed fields/variants/states?
[ ] Unknown semantic fields rejected or explicitly non-semantic?
[ ] Open mappings challenged?

SEMANTICS
[ ] One current meaning per field/state?
[ ] Neighboring identities separated?
[ ] Remaining semantic choice owner explicit?

ENCODING
[ ] If bytes/hash matter: one canonical representation?
[ ] Exact literals/types/order/derivation sources?
[ ] Golden fixture where useful?

OWNERSHIP
[ ] Which task/component constructs/derives each value?
[ ] Pure contract vs live collection separated?
[ ] Verification does not pull future work forward?

DETERMINACY
[ ] Can two materially different implementations still satisfy the text?
    If yes and material → revise.

EXECUTION CLOSURE
[ ] Happy path passes.
[ ] Nearest wrong shape rejected.
[ ] Nearest wrong semantic injection rejected.
[ ] Alternate canonical encoding rejected.
[ ] Downstream ownership not implemented early.

STOP
[ ] Local blocker blocks only its dependency cone.
[ ] No speculative hardening.
[ ] No future task implementation.
```

---

# 20. Reusable prompt seed for weak-model execution

```text
Implement the current approved contract literally.

For each task-owned contract:

1. construct only the complete allowed shape;
2. do not generalize the schema;
3. use the exact approved semantic meaning;
4. where canonical bytes matter, use the exact approved encoding;
5. implement only the derivation/behavior owned by this task;
6. run the named happy-path test;
7. run nearest-wrong probes for shape, semantics, encoding and ownership;
8. stop when the current task is closed.

If implementation requires a new material semantic choice not uniquely fixed
by current authoritative artifacts:

BLOCKED_BY_CURRENT_CONTRACT_AMBIGUITY

Block only the dependent slice when independent authorized work can continue.
```

---

# 21. Recommended Roadmap disposition

Do not create a new major Roadmap stage only for this recommendation.

Recommended integration:

```text
Poker field pilot
→ retain real closure fixtures

PL-V38-05
→ bounded current task/context packets

PL-V38-06A
→ inspect/reuse code-companion assets before new machinery

PL-V38-06B
→ evaluate four-layer closure + weak-model Task Closure fixtures

PL-V38-07/08
→ automate deterministic probes only if evidence supports it
```

Likely eventual homes:

```text
Planning checklist:
shape + semantics + encoding + ownership closure

Readiness:
two-implementation / two-byte / ownership determinacy tests

Execution:
semantic-choice guard + nearest-wrong closure probes

Code companion:
reusable prompt/checklist/test seeds
```

---

# 22. Anti-overreach

Do not immediately introduce:

- universal extra lifecycle stages;
- generalized schema compilers;
- fuzzing infrastructure;
- plugin registries;
- provenance frameworks;
- mandatory independent review for trivial tasks;
- enormous negative prompt lists.

Start with prompt/checklist discipline and real Poker fixtures.

Automate only repeated, measurable failure classes.

---

# 23. Provisional conclusion

The Poker T-01 field case suggests a concrete failure mode for weaker models:

```text
they can correctly build the named positive structure
while leaving the surrounding semantic space too open
```

The strongest response is not more prohibition prose.

It is:

```text
Planning closes the shape
→ Planning closes the meaning
→ Planning closes canonical encoding where bytes matter
→ Planning closes task/component ownership
→ Readiness proves determinacy with competing implementations
→ Execution refuses new semantics
→ nearest-wrong probes test the complement
→ dependent tasks wait until the contract is genuinely closed
```

This gives weak models a smaller, more positive, more mechanically verifiable execution problem.
