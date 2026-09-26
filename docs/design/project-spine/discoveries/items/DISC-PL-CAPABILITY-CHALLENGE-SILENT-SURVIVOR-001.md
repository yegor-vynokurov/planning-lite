# DISC-PL-CAPABILITY-CHALLENGE-SILENT-SURVIVOR-001

## First historical SILENT_SURVIVOR case for Capability Challenge

**Discovery ID:** `DISC-PL-CAPABILITY-CHALLENGE-SILENT-SURVIVOR-001`  
**Date:** `2026-09-26`  
**Status:** `EMPIRICAL DISCOVERY / HISTORICAL REGRESSION CASE`  
**Source Change:** `CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001`  
**Class:** verification / epistemic robustness / adversarial review / false-ready resistance

This document records an empirical Planning Lite observation.

It is not a Recommendation, Roadmap item, implementation authorization, new
gate, or new subsystem.

It exists as reusable historical evidence for future work on epistemic
robustness, Capability Challenge, adversarial validation, mutation-style
testing, and false-ready prevention.

## 1. Observed situation

During 09-E productization, the read-only executor plan compiler reached a
state in which conventional validation was strongly green.

Immediately before the independent adversarial owner review, the candidate
reported:

```text
FOCUSED_PLAN_COMPILATION_TESTS:
47 passed

FOCUSED_CLI_TESTS:
30 passed

TEMPLATE_FOUNDATION_TESTS:
83 passed

WHOLE_ORGANISM_TESTS:
30 passed

FULL_SUITE:
704 passed, 2 historical baseline failures

NEW_FULL_SUITE_FAILURES:
0
```

The two full-suite failures were pre-existing central-resume-contract debt and
were not introduced by the 09-E candidate.

The candidate had also passed the bounded S1-S6 micro-correction checks and
whole-organism regression.

A normal green-suite interpretation could therefore have supported the
conclusion:

```text
candidate appears ready for commit
```

Instead, owner review deliberately asked a different question:

```text
What plausible materially broken states can still survive
the current tests and readiness machinery?
```

That adversarial question exposed four additional material seams.

## 2. Surviving material seams

### F7 — DERIVED_DECISION_ENVELOPE_CONTRADICTION_UNCHECKED

A derived unit could place the same executor decision in both:

```text
allowed_executor_decisions
and
forbidden_executor_decisions
```

without the contradiction being rejected.

The candidate could therefore represent an internally contradictory derived
execution envelope.

### F8 — ORIGINAL_ALREADY_DECIDED_SPLIT_ASSERTION_OVERBINDING

The implementation applied the S1-S6 split-assertion validator to
`units[].already_decided` for every original unit rather than only to an
original unit with:

```text
disposition = SPLIT_RECOMMENDED
```

This accidentally narrowed a general semantic decision carrier into a
split-test-only carrier and rejected legitimate non-split `already_decided`
content.

### F9 — C01_C13_NA_AUTHORITY_DRIFT

The frozen 09-E semantics allow C01-C13 criterion values:

```text
PASS
FAIL
N/A
```

A later corrective governance text unintentionally implied that every
non-PASS criterion was non-ready.

The implementation still accepted legitimate `N/A`.

In this case the surviving seam was not simply implementation drift.

It exposed drift in the governing contract itself.

### F10 — CLI_ERROR_RENDERING_AUTHORITY_DRIFT

A later corrective governance text referred to canonical structured JSON error
rendering for schema errors.

The existing CLI contract used:

```text
exit 2
bounded PlanningLiteError on stderr
no result JSON on stdout
```

Independent review found that the later wording had accidentally implied a new
error-response schema that the original product contract had never selected.

Again, the important defect was partly governance drift rather than a simple
code bug.

## 3. Why this is a SILENT_SURVIVOR

For this Discovery, a `SILENT_SURVIVOR` means:

> A materially incorrect or materially under-specified state that survives the
> normal approved verification stack and can appear acceptable until a bounded
> adversarial perturbation, counterexample, contract comparison, or alternative
> interpretation exposes it.

The defining sequence in this case was:

```text
large focused test set PASS
+
whole-organism PASS
+
no new full-suite regression
+
formal readiness previously green
+
bounded corrective work apparently complete

BUT

targeted adversarial review
→ four material surviving seams
```

Therefore:

```text
GREEN TEST COUNT
!=
PROOF THAT NO MATERIAL PLAUSIBLE MUTANT SURVIVES
```

## 4. Important distinction learned

The four survivors were not one homogeneous bug class.

They included:

```text
implementation invariant omission
semantic-carrier overbinding
governance semantic drift
governance/presentation contract drift
```

Therefore a future Capability Challenge should not challenge code alone.

It should be able to challenge:

```text
implementation
contract interpretation
authority consistency
test adequacy
readiness assumptions
presentation/protocol assumptions
```

The challenger must be allowed to conclude either:

```text
implementation is wrong
```

or:

```text
the later governing text is wrong
```

without automatically privileging the newest artifact merely because it is
newest.

## 5. Useful challenge patterns recovered from this case

This historical case suggests at least four reusable adversarial probes:

```text
1. CONTRADICTION INJECTION

Can two fields that should be mutually exclusive coexist and still reach READY?

2. CARRIER SCOPE PERTURBATION

Has a general semantic carrier accidentally been narrowed to one special
decision vocabulary?

3. AUTHORITY DIFFERENTIAL

Does the implementation disagree with a later contract because the
implementation is wrong, or because the later contract drifted from the frozen
semantic authority?

4. PROTOCOL ASSUMPTION CHALLENGE

Did a corrective artifact silently introduce a new presentation or protocol
requirement that was never selected by the product contract?
```

These are candidates for future Capability Challenge / epistemic robustness
experiments.

They are not automatically product requirements.

## 6. Resolution

The four seams were adjudicated together in:

```text
PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-CHANGE-DEFINITION-AMENDMENT-v5.md

PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-IMPLEMENTATION-PLAN-AMENDMENT-v4.md

PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-FORMAL-READINESS-VERDICT-v5.md
```

Formal Readiness v5 reported:

```text
R01-R16:
PASS

F7_BOUND:
YES

F8_BOUND:
YES

F9_BOUND:
YES

F10_BOUND:
YES

MATERIAL_BLOCKER_COUNT:
0

UNBOUND_MATERIAL_CHOICE_COUNT:
0

STRICTLY_REQUIRED_ADDITIONAL_PATHS:
[]
```

Governance commit:

```text
699ed8adc473a3b0d99dec017cbb73d881570a07
```

The product candidate itself was not mutated by the v5 governance gate.

## 7. Relationship to future work

This Discovery is evidence relevant to, but not authority for:

```text
REC-PL-EPISTEMIC-ROBUSTNESS-BLITZ-001

future Capability Challenge work

future adversarial / mutation-style verification experiments

future false-ready / false-done resistance work
```

It should be used as the first historical regression case when such a mechanism
is experimentally evaluated.

A useful future acceptance question is:

```text
Would the candidate Capability Challenge mechanism have surfaced
F7-F10 before owner review did?
```

If the answer is no, this Discovery can be used to improve the challenge
design.

## 8. Non-implications

This Discovery does not imply:

```text
add a new Roadmap vertebra
create a new runtime subsystem
block current 09-E completion
replace normal tests
replace whole-organism validation
require universal mutation testing
require a numeric confidence score
automatically implement REC-PL-EPISTEMIC-ROBUSTNESS-BLITZ-001
```

It records one empirical lesson:

```text
A strong green verification stack can still contain silent survivors.

For material first-of-kind decisions, bounded adversarial attempts to falsify
READY can reveal defects that normal conformance testing misses.
```

## 9. Reuse trigger

Revisit this Discovery when Planning Lite next designs or evaluates:

```text
epistemic robustness
Capability Challenge
defeater search
perturbation testing
mutation-style validation
false-ready resistance
high-impact first-of-kind decision review
```

Until then:

```text
DISPOSITION:
HISTORICAL_EVIDENCE / NO CURRENT ACTION IMPLIED
```
