# REC-PL-MATERIALITY-SIMPLICITY-001 v1
## Evidence-gated materiality, proportionality, and simplicity review

**Status:** PROVISIONAL / FIELD-DERIVED / RESEARCH-CORROBORATED / OPEN
**Date:** 2026-08-20
**Primary field source:** Poker `CHG-0009-bayesian-study-harness` repeated Planning ↔ Readiness loops
**Implementation authority:** none
**Recommended canonical location:** `docs/design/project-spine/REC-PL-MATERIALITY-SIMPLICITY-001-v1.md`

---

## 1. Problem

`CHG-0009` showed that exhaustive Readiness is valuable: it found real scientific,
execution, provenance, recovery, and repository/runtime blockers.

The same adversarial process also creates a symmetric risk:

```text
find plausible failure
→ require mitigation
→ mitigation introduces states / transitions / identities / retries / platform logic
→ new mechanisms create new review surface
→ further mitigations appear
→ the supporting machinery grows faster than the original requirement
```

Planning Lite currently has strong guards against **under-specification**, but a weaker
explicit guard against **specification accretion / over-engineering**.

The desired invariant is:

```text
complete enough to execute safely
+
no more machinery than current evidence requires
```

## 2. External prior art

### Google Engineering Practices

Google code review explicitly asks whether a change is more complex than necessary,
whether it belongs in the system now, and whether it implements speculative future
needs. Google's review standard also says reviewers should favor progress once a
change definitely improves code health rather than demand perfection.

References:
- https://google.github.io/eng-practices/review/reviewer/looking-for.html
- https://github.com/google/eng-practices/blob/master/review/reviewer/standard.md
- https://github.com/google/eng-practices/blob/master/review/reviewer/navigate.md

### Google SRE

Google SRE treats simplicity as an end-to-end reliability property, not only a code
property. It notes that complexity has externalities and that simplification often
consists of removing elements from a system.

References:
- https://sre.google/workbook/simplicity/
- https://sre.google/sre-book/simplicity/

### Google launch/readiness checklists

Google's launch engineering material recommends concrete, practical checklist
questions and continuous checklist curation. It also emphasizes convergence on
existing infrastructure rather than reimplementing common solutions.

Reference:
- https://sre.google/sre-book/reliable-product-launches/

### AWS Operational Readiness Review

AWS operational readiness reviews use reusable question checklists, record residual
risk, and track action items rather than assuming every discovery requires immediate
architecture.

References:
- https://docs.aws.amazon.com/wellarchitected/latest/operational-readiness-reviews/the-orr-tool.html
- https://docs.aws.amazon.com/wellarchitected/2023-04-10/framework/ops_ready_to_support_const_orr.html

### Test Double / Han evidence-based YAGNI

This is the closest reusable agent-oriented precedent found.

Han uses two explicit gates:

```text
Gate 1: evidence test
    Is this item needed now, with concrete evidence?

Gate 2: simpler-version test
    Is there a strictly simpler form satisfying the same evidence?
```

YAGNI findings are intentionally advisory/non-correcting so that a reviewer does not
automatically turn every possible simplification into mandatory work.

References:
- https://github.com/testdouble/han/blob/main/han-coding/references/yagni-rule.md
- https://github.com/testdouble/han/blob/main/han-coding/skills/code-review/references/review-checklist.md
- https://github.com/testdouble/han/blob/main/han-coding/skills/code-review/SKILL.md

## 3. Recommendation

Planning Lite should evaluate a **Materiality & Simplicity Gate** that is paired with,
but distinct from, completeness/readiness checks.

It should answer two questions in order:

```text
1. NECESSITY / MATERIALITY
   Does current evidence show that this mechanism is required?

2. SHAPE / PROPORTIONALITY
   Is this the simplest sufficient mechanism for that requirement?
```

A negative answer to either question should not automatically create another
corrective Change.

## 4. Candidate classification

Every non-trivial proposed mechanism or reviewer-requested mitigation should be
classified as exactly one of:

### MUST_KEEP
Current evidence shows that omission can materially cause wrong result semantics,
execution ambiguity, authorization-boundary violation, evidence corruption,
reproducibility failure, or a confirmed repository/runtime conflict. The chosen
mechanism is also proportionate.

### SIMPLIFY_NOW
The underlying problem is material, but a simpler construction satisfies the same
current evidence.

### DEFER
The problem is real, but it is easily detected later, reversible, does not corrupt
canonical evidence before detection, and adding the solution later is not materially
more expensive. Record a concrete reopen trigger.

### DROP
The mechanism is speculative, redundant, future-flexibility work, or cannot be traced
to a current requirement/failure.

### HUMAN_DECISION
The choice changes scientific, product, policy, or other human-authority semantics.

## 5. Evidence classes

```text
OBSERVED
  directly reproduced in repository/runtime

DIRECT
  logically unavoidable under the current contract

PLAUSIBLE_CURRENT
  reachable under the current bounded workload/environment

SPECULATIVE
  requires a future capability, scale, environment, or consumer
```

Default:

```text
SPECULATIVE → record if useful, but do not build complex current machinery
```

unless explicit authority says otherwise.

## 6. Simpler-alternative ladder

Before accepting a non-trivial mitigation, compare it to at least:

```text
0. do nothing / natural failure
1. fail-fast / refuse
2. manual operator decision for rare research-local operations
3. immutable append / new attempt
4. rerun from scratch for bounded workloads
5. reuse an existing primitive
6. proposed new mechanism
```

The first option satisfying all material requirements wins unless evidence proves a
more complex option has materially lower lifecycle cost.

## 7. Complexity-disproportion signal

A mitigation is a simplification candidate when preventing one bounded failure
introduces a disproportionate number of:

- packages/components;
- persistent artifact types;
- identities/hashes;
- mutable states;
- state transitions;
- retry/recovery paths;
- leases/locks;
- concurrency rules;
- platform-specific adapters;
- configuration surfaces;
- external dependencies;
- verification seams.

Heuristic:

> If the mitigation is materially harder to implement, explain, and verify than the
> failure plus a simple fail-fast/rerun path, the burden of proof belongs to the more
> complex mechanism.

Do not turn this into a hard numeric blocker until field evidence supports thresholds.

## 8. Stop rule

After the current material requirement is satisfied by the simplest proven mechanism:

```text
STOP
```

Do not add optional hardening, speculative flexibility, generic reusable abstractions,
future scale machinery, redundant guards for now-unreachable states, or automation
whose only benefit is avoiding a rare manual research-local action.

"Perfect" is not a Readiness criterion.

## 9. Relationship to exhaustive Readiness

```text
Readiness completeness:
    did we omit something necessary?

Materiality / simplicity:
    did we add something unnecessary or disproportionate?
```

Recommended behavior:
1. Planning produces an executable contract.
2. Readiness performs exhaustive blocker detection.
3. If a blocker requires a non-trivial new mechanism, run materiality/simplicity
   before accepting the mitigation shape.
4. `SIMPLIFY/DEFER/DROP` findings are advisory by default.
5. Human authority remains explicit for semantic/protocol changes.

## 10. CHG-0009 field fixture

Compare the current richer lease/liveness design against:

```text
each invocation
→ new unique immutable attempt directory
→ never overwrite/reclaim old attempt automatically
→ crash leaves incomplete attempt intact
→ retry creates a new attempt
→ publish canonical result only after validation
→ existing completed canonical result = verify/reuse-or-refuse
```

The gate should identify exactly which current requirements the richer design satisfies
that this simple design does not.

## 11. Evaluation plan

Use at least:
1. `CHG-0009` artifact/retry design.
2. A small routine bugfix where the gate should do almost nothing.
3. A real correctness/safety case where the gate must not incorrectly apply YAGNI.

Measure mechanisms kept/simplified/deferred/dropped, later Readiness regressions,
implementation surface, tests added, lifecycle loops, operator corrections, and missed
material failures.

Success:

```text
same material correctness/safety
+
less unnecessary mechanism surface
+
fewer self-created review obligations
```

## 12. Integration candidate

Do not create a new major Roadmap stage solely for this finding.

Candidate destinations:
- `CHANGE_PLANNING.md`: evidence + simpler-version self-check before plan approval;
- `CHANGE_READINESS.md`: materiality tag on proposed corrective mechanisms;
- future reusable checklist layer only after field qualification;
- `PL-V38-06B`: controlled-realistic fixtures;
- `PL-V38-07/08`: automation only after non-inferiority evidence.

## 13. Code/prompt assets to preserve as references

Add reference entries to the Planning Lite code companion / code stash rather than
copying upstream implementations wholesale:

```text
Han evidence-based YAGNI rule
https://github.com/testdouble/han/blob/main/han-coding/references/yagni-rule.md

Han two-pass review checklist
https://github.com/testdouble/han/blob/main/han-coding/skills/code-review/references/review-checklist.md

Microsoft reusable review prompt-file pattern
https://github.com/microsoft/skills/blob/main/.github/prompts/code-review.prompt.md

GitHub prompt-file review example
https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code
```

Candidate local record:

```yaml
finding_id: ...
requirement: ...
evidence_class: OBSERVED | DIRECT | PLAUSIBLE_CURRENT | SPECULATIVE
failure_if_absent: ...
simpler_candidates:
  - do_nothing
  - fail_fast
  - manual
  - immutable_append
  - rerun
  - reuse_existing
  - proposed
classification: MUST_KEEP | SIMPLIFY_NOW | DEFER | DROP | HUMAN_DECISION
reopen_trigger: ...
```

## 14. Anti-overreach

This recommendation does not authorize deleting correctness/security/evidence
safeguards merely because they are complex, overriding explicit user requirements,
hiding deferred items, subjective complexity scores, automatic simplification of
scientific semantics, a new framework dependency, or an always-on heavyweight review
for routine Changes.
