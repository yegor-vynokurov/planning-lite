# REC-PL-EXECUTABLE-TARGET-CONTRACT-001 v1
## Executable Target Contract: system claims, target scenarios, and ideal-state evidence

**Status:** `PROVISIONAL / FIELD-DERIVED / STRONG CANDIDATE`
**Date:** `2026-08-21`
**Implementation authority:** none
**Recommended canonical location:**
`docs/design/project-spine/REC-PL-EXECUTABLE-TARGET-CONTRACT-001-v1.md`

**Related recommendations / concepts:**
- `REC-PL-TARGET-SKELETON-001`
- `REC-PL-OUTCOME-LADDER-001`
- `REC-PL-IDEAL-VALIDATION-001`
- `REC-PL-CONTROL-PLANE-EVALS-001`
- `REC-PL-WEAK-MODEL-EXECUTION-001`
- Feedback Channel Matrix
- Implementation Gap / Evidence Gap

---

# 1. Why this recommendation exists

Planning Lite can describe an ideal future state in prose and can verify implementation tasks locally, but this still leaves a structural gap:

```text
target described on paper
        ↓
implementation accumulates
        ↓
many local tests become green
        ↓
but do we know that the WHOLE SYSTEM
actually exhibits the behavior we originally wanted?
```

This problem becomes especially visible in agentic/LLM systems.

A system may have:
- passing unit tests;
- a working retriever;
- a working model call;
- correct serialization;
- a runnable demo;

and still fail its real project claim:

```text
"the assistant answers supported questions correctly
and does not invent answers when evidence is insufficient."
```

The user independently identified a useful direction while reviewing an agent-engineering lecture:

> when creating the project skeleton, also define "general tests" for how the completed system should ideally behave, including what should happen when it cannot behave successfully.

The lecture/repository material supports adjacent pieces:
- early runnable skeleton/smoke validation;
- acceptance criteria;
- verifiable execution signals;
- feedback channels suited to different failure classes.

The stronger synthesis proposed here is Planning Lite-specific:

> **Translate the chosen Outcome Level into a small set of system claims, then make those claims executable as early success and failure scenarios.**

---

# 2. Core distinction: Skeleton Contract vs Target Behavior Contract

A Target Skeleton and an Executable Target Contract answer different questions.

## 2.1 Skeleton Contract

Question:

> Does the intended end-to-end topology exist at all?

For software:

```text
input
→ main layers
→ output
```

may already work with explicit placeholders.

Typical evidence:

```text
build
boot
smoke
wiring
tool availability
migration/test tooling
one end-to-end traversal
```

The Skeleton Contract can become green early.

## 2.2 Target Behavior Contract

Question:

> Does the complete system behave the way the project claims it should?

This can and often should remain red after the skeleton exists.

Example:

```text
Structural contract: PASS
Behavior contract: FAIL / NOT WIRED
```

This is an honest and useful state.

It means:

```text
the whole organism has a skeleton,
but it does not yet have all its muscles and reflexes.
```

---

# 3. System Claims

The Executable Target Contract begins with **System Claims**.

A System Claim is an externally meaningful assertion the project makes about itself.

Bad claims:

```text
retriever class exists
function returns object
database adapter initializes
```

These are implementation facts.

Better claims:

```text
supported chemistry questions receive materially correct answers

answers are grounded in retrieved evidence

unsupported questions do not produce fabricated certainty

ambiguous questions trigger clarification or bounded uncertainty behavior

a documented installation reproduces the demo result
```

## 3.1 Claim source

System Claims should come from:

```text
Outcome Level
+ user/business/scientific value
+ approved target behavior
+ material safety/reliability boundaries
```

not from whatever implementation already happens to exist.

---

# 4. Outcome Ladder → Claims → Executable Target Contract

Each Outcome Level should have its own claim set.

Example:

## L1 — Demonstrable repository

Claims may be:

```text
repository installs from documented instructions
test suite runs
demo starts
one canonical end-to-end example completes
documented result is reproducible
```

This suite may look "boring."

That is correct.

The project is only claiming portfolio/demo-level value.

## L2 — Useful chemistry assistant

Additional claims:

```text
supported questions receive correct grounded answers
unsupported questions produce safe abstention
ambiguous questions trigger clarification
false-premise questions are corrected rather than endorsed
```

## L3 — Trustworthy tutor

Additional claims:

```text
explanation level matches learner target
misconceptions are addressed
multi-turn context remains coherent
Socratic behavior is appropriate where configured
confidence/evidence are calibrated
```

Therefore:

> An Outcome Level is not demonstrated merely because Roadmap says it has been reached.

It is demonstrated when its required System Claims have adequate evidence.

---

# 5. Three claim families

Every Executable Target Contract should consider three families.

## 5.1 Structural claims

Examples:

```text
system can boot
main path is connected
required components are present
data/evidence path is reachable
```

These support the Target Skeleton.

## 5.2 Success behavior claims

Examples:

```text
valid request → useful correct result
supported query → grounded answer
valid poker state → valid analysis
configured pipeline → expected artifact
```

## 5.3 Failure / degradation claims

Examples:

```text
insufficient evidence → abstain / report uncertainty
ambiguous request → clarify
unsupported mode → refuse safely
runtime failure → durable incomplete result, not fake completion
invalid input → deterministic rejection
dependency unavailable → controlled degradation
```

Failure claims are first-class.

A system is often defined as much by **how it fails** as by how it succeeds.

---

# 6. Target Scenarios

Claims become executable through **Target Scenarios**.

A Target Scenario is a canonical case that asks:

```text
Given this starting state/input,
what observable behavior must the whole system exhibit?
```

A Target Scenario should specify:

```text
scenario_id
claim_id
outcome_level
preconditions
input
expected_observable_behavior
forbidden_observable_behavior
evidence_channel
status
```

The preferred focus is external/observable behavior.

Avoid over-specifying internal implementation unless the internal property is itself material.

---

# 7. Status model: DEFINED → WIRED → PASSING

A major benefit of this recommendation is that ideal-state tests do not need to be executable immediately.

Use three independent states.

## DEFINED

The scenario and expected behavior are specified.

No executable harness is required yet.

## WIRED

A real executable probe/eval exists and can exercise the scenario.

The system may still fail.

## PASSING

The current system produces evidence satisfying the scenario.

Example:

```text
TC-CHEM-07 unsupported-question abstention

DEFINED: yes
WIRED: yes
PASSING: no
```

This is much better than pretending the target does not exist until implementation is nearly finished.

---

# 8. Do not force exact-string tests for LLM systems

For non-deterministic systems:

```text
input → exact expected output string
```

is usually the wrong abstraction.

Instead:

```text
input
→ observable criteria
→ grader/evaluator
```

Possible criteria:

```text
must contain concept X
must not claim Y
must cite retrieved source
must abstain below evidence condition
must ask clarification for ambiguity class Z
must preserve numerical quantity Q
must not fabricate source attribution
```

Evidence may be:

```text
deterministic parser
rule-based grader
structured output validation
reference answer comparison
LLM judge
human review
hybrid
```

Prefer deterministic evidence where sufficient.

Use LLM judges only where the behavior genuinely requires semantic judgment.

---

# 9. Feedback Channel Matrix

Do not assume every claim should be proven with a unit test.

For each claim, ask:

> What observable signal could actually falsify our belief that this works?

Suggested mapping:

| Failure / claim class | Primary evidence channel |
|---|---|
| pure deterministic logic | unit/property/contract test |
| integration/wiring | integration / end-to-end |
| UI behavior | browser / DOM / visual / live interaction |
| persistence | reload/restart/recovery |
| performance | benchmark/profiling |
| security/authz | negative/adversarial probe |
| scientific correctness | experiment/holdout |
| reproducibility | rerun + identity comparison |
| operational readiness | smoke/health/observability |
| human usability | task-based human review |
| LLM semantic quality | eval harness / rubric / reference set |

The cheapest adequate channel should be preferred.

---

# 10. Implementation Gap and Evidence Gap

Track two independent deficits.

## Implementation Gap

```text
required target behavior
minus
current implemented behavior
```

## Evidence Gap

```text
evidence required to justify the target claim
minus
current available evidence
```

This prevents:

```text
current tests green
→ target proved
```

A project may have:

```text
Implementation Gap: small
Evidence Gap: large
```

or:

```text
Implementation Gap: large
Evidence Gap: already defined/wired
```

Both are useful states.

---

# 11. Target Skeleton integration

When creating a Target Skeleton:

```text
1. build the end-to-end structural path
2. create Structural Claim probes
3. register Target Behavior Scenarios
4. wire only the cheapest/highest-value behavior probes initially
5. keep missing behavior visibly red / not wired
```

Recommended early state:

```text
STRUCTURAL CONTRACT
mostly PASSING

TARGET BEHAVIOR CONTRACT
mix of:
DEFINED
WIRED+FAIL
PASS
```

This gives a physical ideal-state dashboard without fake completeness.

---

# 12. Vertical-slice planning integration

Roadmap slices should increasingly convert target scenarios:

```text
DEFINED
→ WIRED
→ PASSING
```

A slice should preferably close a meaningful vertical claim rather than merely fill a folder.

Example:

Bad slice:

```text
implement retriever package
```

Better slice:

```text
supported chemistry question
→ retrieval
→ answer
→ evidence citation
→ claim TC-CHEM-01 becomes PASSING
```

Internal tasks may still be necessary, but the Roadmap should know which System Claim they ultimately unlock.

---

# 13. Failure scenarios should be present early

Failure behavior should not be deferred until "hardening."

For agentic/LLM systems, early failure claims are especially valuable.

Examples:

```text
no evidence
→ no fabricated answer

tool unavailable
→ explicit degradation

ambiguous intent
→ clarification

unsupported capability
→ refusal

partial execution
→ no fake success

bad identity/provenance
→ fail closed
```

This complements Planning Lite's authority and evidence governance.

---

# 14. Claim strength must match Outcome Level

Do not over-test a low-value level with high-level behavioral expectations.

Example:

If the Outcome Level is only:

```text
"portfolio-quality repository"
```

then appropriate claims may be:

```text
installs
tests
demo
reproducible example
clean docs
```

It is not a defect that the suite is less behaviorally rich.

Conversely, do not claim:

```text
"trustworthy chemistry tutor"
```

while only proving:

```text
repository boots
```

---

# 15. Claim cardinality: small canonical set first

Do not attempt exhaustive coverage at the beginning.

Start with a **small canonical suite**.

Candidate initial categories:

```text
1–3 core success scenarios
1 unsupported/failure scenario
1 ambiguity scenario
1 major safety/evidence boundary
1 reproducibility/integration scenario
```

Expand only when:
- field failures recur;
- new Outcome Level adds claims;
- new material risk appears;
- eval evidence shows blind spots.

This follows Materiality/Simplicity.

---

# 16. Golden Scenario Registry

Suggested lightweight registry:

```yaml
claims:
  CHEM-CLAIM-01:
    outcome_level: L2
    statement: "Supported chemistry questions receive materially correct grounded answers."

scenarios:
  TC-CHEM-01:
    claim: CHEM-CLAIM-01
    class: success
    status:
      defined: true
      wired: true
      passing: false
    evidence_channel: llm_eval
```

The registry should remain small enough to read and reason about.

Do not build a large test-management system without evidence.

---

# 17. Example: Chemistry assistant

## Claim C1 — Supported questions receive correct grounded answers

Scenario:

```text
Question:
Why does a carbonate release gas when acid is added?

Expected:
- identifies CO2 correctly
- explains the reaction mechanism at target learner level
- uses retrieved source/evidence
- does not fabricate attribution
```

## Claim C2 — Unsupported questions do not produce fabricated certainty

Scenario:

```text
Question:
outside current corpus / unsupported evidence

Expected:
- detects insufficient support
- abstains or clearly bounds uncertainty
- does not invent source/evidence
```

## Claim C3 — Ambiguous question triggers clarification

Scenario:

```text
Question:
materially ambiguous chemistry prompt

Expected:
- identifies ambiguity
- asks a targeted clarification
- does not confidently choose one interpretation silently
```

## Claim C4 — False premise is not endorsed

Scenario:

```text
Question includes a false chemical premise.

Expected:
- corrects or challenges premise
- proceeds only from corrected assumption
```

---

# 18. Example: Poker research harness

System claims may include:

```text
valid fixed-flop state
→ deterministic approved analysis

unsupported/invalid state
→ explicit rejection

insufficient evidence
→ no scientific disposition

runtime interruption
→ durable incomplete evidence

same approved config/provenance
→ same canonical identity
```

This shows that Planning Lite already builds pieces of Executable Target Contracts, but has not yet unified them under one project-level concept.

---

# 19. Relationship to Control-Plane Evals

The same structure can test Planning Lite itself.

Planning Lite makes claims such as:

```text
Readiness is exhaustive
Execution does not invent missing semantics
local blocker does not stop independent authorized work
historical context is not loaded by default
```

These can become System Claims with behavioral regression scenarios.

Thus the Executable Target Contract is not only a product-testing concept.

It can become a **control-plane testing abstraction**.

---

# 20. Planning checklist

When defining a meaningful Outcome Level:

```text
[ ] What claims does this level make about the whole system?
[ ] Which claims are structural?
[ ] Which are success behavior?
[ ] Which are failure/degradation behavior?
[ ] Which 3–7 canonical scenarios best represent them?
[ ] What feedback channel can actually falsify each claim?
[ ] Which scenarios are DEFINED / WIRED / PASSING?
[ ] What Implementation Gap remains?
[ ] What Evidence Gap remains?
```

---

# 21. Readiness checklist

Before a major implementation program:

```text
[ ] Target claims derive from the approved Outcome Level.
[ ] Failure behavior is not omitted.
[ ] Scenarios are observable rather than implementation-mirroring.
[ ] Evidence channels are appropriate to failure class.
[ ] No passing placeholder is counted as real target evidence.
[ ] Skeleton smoke passing is not mistaken for behavior passing.
[ ] At least the highest-risk claims have WIRED probes where feasible.
```

---

# 22. Execution / Verification checklist

For a vertical slice:

```text
[ ] Which System Claim does this slice advance?
[ ] Does it move a scenario DEFINED→WIRED or WIRED→PASSING?
[ ] Is the relevant evidence channel actually exercised?
[ ] Are failure scenarios preserved?
[ ] Did the slice accidentally make a placeholder look passing?
```

At Verification:

```text
[ ] Highest Outcome Level demonstrated by evidence?
[ ] Which claims pass?
[ ] Which claims fail?
[ ] Which claims are not yet wired?
[ ] Remaining Implementation Gap?
[ ] Remaining Evidence Gap?
```

---

# 23. Anti-overreach

Do not immediately create:
- hundreds of end-to-end tests;
- one scenario per requirement;
- a complex eval management platform;
- universal LLM judges;
- expensive full-system runs on every edit.

Start with:
- a small canonical scenario set;
- statuses;
- clear evidence channels;
- targeted execution.

Use cheap deterministic tests where sufficient.

---

# 24. Recommended roadmap disposition

Do not create a new major lifecycle stage.

Integrate as:

```text
Outcome Ladder
→ System Claims

Target Skeleton
→ Structural Contract

Definition/Planning
→ Target Scenarios + Evidence Channels

Execution
→ vertical slices advance scenario states

Verification
→ demonstrated claims / Outcome Level

Controlled Evolution
→ failed field scenarios become new regression candidates
```

Potential later automation belongs near:
- controlled-realistic fixtures;
- Control-Plane Evals;
- Context Compiler / orchestration only after evidence.

---

# 25. Experimental plan

## ETC-E1 — Chemistry assistant mini-suite

Create 5 canonical scenarios:
- 2 supported;
- 1 unsupported;
- 1 ambiguous;
- 1 false premise.

Do not improve the bot first.

Run current system and classify:
- DEFINED;
- WIRED;
- PASS/FAIL.

Observe whether this changes Roadmap priorities.

## ETC-E2 — Skeleton vs behavior

On a partially implemented project:

```text
Skeleton smoke
vs
Target Behavior Contract
```

Verify the system can be structurally green while behavior remains honestly red.

## ETC-E3 — Outcome Ladder

Define L1/L2/L3 claim suites.

Check whether the highest demonstrable level can be determined mechanically/evidentially.

## ETC-E4 — Failure-first value

Compare planning with:
- success scenarios only;
- success + failure/degradation scenarios.

Measure escaped failure semantics later in execution.

---

# 26. Provisional conclusion

Planning Lite should not only ask:

```text
"What should the finished system look like?"
```

It should also ask:

```text
"What observable claims will make us entitled to say that this ideal picture
actually works, including when the world refuses to cooperate?"
```

The recommended chain is:

```text
Outcome Level
→ System Claims
→ Target Scenarios
→ Structural / Success / Failure contracts
→ appropriate evidence channels
→ DEFINED / WIRED / PASSING
→ Implementation Gap + Evidence Gap
→ demonstrated Outcome Level
```

This turns the ideal picture from a document into a progressively executable, falsifiable contract.
