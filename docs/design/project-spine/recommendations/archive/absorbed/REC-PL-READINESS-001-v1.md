# REC-PL-READINESS-001 v1 — Executable readiness, evidence identity, and governed residual findings

**Status:** `PROVISIONAL / FIELD-DERIVED / OPEN`
**Date:** `2026-08-20`
**Source:** `PILOT-PL-DIRECTION-002` and Poker `CHG-0009-bayesian-study-harness` readiness review
**Visibility:** `ACTIVE_DIRECTION` for Planning Lite design; individual residual findings may enter `UNANCHORED_BACKLOG`
**Implementation authority:** none; this recommendation records field evidence and design constraints

---

## 1. Problem observed in field use

Poker `CHG-0009-bayesian-study-harness` reached a detailed, fully traced Planning state:

- one bounded Roadmap contribution;
- ten dependency-ordered implementation slices;
- sixteen acceptance criteria mapped to tasks;
- explicit scientific exclusions;
- no implementation authorization.

A formal Readiness review nevertheless returned `Needs revision`.

The reason was not missing scope or missing task ownership. The problem was that several safety and scientific guarantees existed only as prose or positive-path intent and were not yet enforceable at executable seams.

This exposes a Planning Lite design distinction:

```text
traceability-complete
!=
execution-ready
```

A Change can have complete AC-to-task mapping and still be unsafe to execute.

---

## 2. Recommendation

Planning Lite Readiness should evaluate whether approved planning constraints are **constructively enforceable and evidence-producing**, not merely present in prose.

The readiness model should distinguish at least:

```text
SEMANTIC_READY
  scope, target, lineage, exclusions are coherent

DELIVERY_READY
  dependency-ordered bounded tasks exist

CONTRACT_READY
  important identities, roles, invalid states, and forbidden flows are enforceable

EVIDENCE_READY
  each critical AC has an executable evidence seam

RUNTIME_READY
  exact required workloads have bounded preflight / stop behavior when material

PROVENANCE_READY
  final evidence can be bound to one reviewed source/config/data/environment identity

EXECUTION_READY
  all required dimensions pass
```

A single `Ready` verdict should be the conjunction of the required dimensions for that Change type.

---

## 3. Field-derived recommendation units

| Unit | Recommendation | State | Intended destination |
|---|---|---|---|
| `REC-PL-READINESS-001/U1` | Treat **traceability completeness and executable readiness as separate properties**. AC mapped to a task is not enough; critical ACs need an executable test, audit, typed contract, runtime gate, or other verifiable seam. | `FIELD_CONFIRMED` | Readiness workflow + PL-V38-06B eval fixtures |
| `REC-PL-READINESS-001/U2` | Readiness may legitimately return an approved Plan to `Planning / In progress` with a **minimal bounded patch proposal**, preserving approved scope, AC identities, lineage, and task decomposition unless the evidence requires broader change. | `FIELD_CONFIRMED` | Change lifecycle / approval gates |
| `REC-PL-READINESS-001/U3` | Safety boundaries should be **constructively unavailable**, not merely undocumented or hidden from CLI. If a mode/action is forbidden in the current Change, internal APIs must not offer an accidental execution path. Negative/direct-import tests should prove the boundary where risk is material. | `FIELD_CONFIRMED` | Readiness disciplines / verification patterns |
| `REC-PL-READINESS-001/U4` | Evidence-role and information-flow constraints should use **typed or otherwise mechanically enforceable boundaries plus negative tests** when leakage would invalidate evidence. Prose separation is insufficient for high-consequence research workflows. | `FIELD_CONFIRMED` | Research-heavy readiness playbook / eval fixtures |
| `REC-PL-READINESS-001/U5` | Separate **portable scientific/config identity**, **source/data/environment provenance**, and **raw numerical-result identity**. Do not make floating-point byte identity stand in for scientific sameness. Cross-environment numerical comparison should be versioned and explicitly scoped, not silently folded into config hashes. | `FIELD_CONFIRMED / POLICY_DETAIL TO CALIBRATE` | Evidence/provenance guidance |
| `REC-PL-READINESS-001/U6` | Exact protocol workloads that may be expensive need a **bounded representative preflight + explicit runtime/memory stop rule**. Execution must never silently reduce counts, seeds, formulas, evidence roles, or scientific semantics to satisfy runtime. | `FIELD_CONFIRMED` | Readiness + execution stop rules |
| `REC-PL-READINESS-001/U7` | Final evidence must be bound to **one reviewed source revision and explicit config/data/environment identities**. Where tracked code/docs are part of the evidence-producing implementation, final authoritative evidence should be rerun on the reviewed clean revision; no tracked mutation may occur afterward without invalidating/repeating the freeze step. | `FIELD_CONFIRMED` | Verification/closure/provenance workflow |
| `REC-PL-READINESS-001/U8` | Existing acceleration/backends may be reused only through a **semantic-parity gate against the current authoritative implementation/data semantics**. Performance is subordinate to correctness. If parity fails, the active Change must not repair an out-of-scope backend merely to gain speed. | `NEW FIELD REQUIREMENT / TO TEST` | Readiness performance discipline |
| `REC-PL-READINESS-001/U9` | A material defect discovered incidentally during an unrelated governed Change should be recorded as **Discovery fact first**, then converted to an anchored Recommendation only when a legitimate current Roadmap/Gap owner exists. Otherwise preserve it as `UNANCHORED_BACKLOG` or `DEFERRED_VISIBLE`; never force-fit lineage into the active Change. | `NEW FIELD REQUIREMENT / TO TEST` | Recommendation residue/history reconciliation + eval |
| `REC-PL-READINESS-001/U10` | Readiness should distinguish **"cannot execute safely"** from **"scope is wrong"**. A `Needs revision` verdict caused by enforceability/provenance/runtime gaps should not automatically reopen Target, Gap, Roadmap priority, or Change Definition. | `FIELD_CONFIRMED` | Router / wayfinding / lifecycle evaluation |

---

## 4. Native/backend parity scenario as an explicit field test

Poker provides a concrete upcoming test for U8 and U9.

The active Bayesian research Change may benefit from an existing native/Cython/C/C++ evaluator/acceleration path.

However, the project previously corrected a hand-strength ordering defect in the Python/evaluator path. Before the native backend can be used for CHG-0009 evidence, the agent must inspect whether the native path implements or consumes the same corrected semantics.

Required governed behavior:

```text
inspect existing native backend
        ↓
run semantic parity checks against current authoritative evaluator semantics
        ↓
PASS and materially faster
    → native backend may be used
    → record backend/source/environment identity in evidence

PASS but irrelevant/not faster
    → keep simpler authoritative path

FAIL
    → do NOT use native backend in CHG-0009
    → do NOT repair it inside CHG-0009
    → record a Discovery with exact mismatch evidence
    → create a follow-up Recommendation
         if legitimate Roadmap/Gap owner exists → anchor it
         otherwise → UNANCHORED_BACKLOG / DEFERRED_VISIBLE
    → continue with correct fallback if runtime gate passes,
      otherwise stop CHG-0009 at a blocker requiring separate governance
```

This scenario is valuable because it tests Recommendation residue handling on a real incidental defect rather than a synthetic fixture.

---

## 5. Anti-overreach constraints

This recommendation does not imply that every Change needs:

- typed wrapper classes for every value;
- negative tests for every internal function;
- a performance benchmark;
- a Git freeze commit;
- cross-platform numerical comparison;
- a new Recommendation for every small defect.

Apply these mechanisms only when the Change's failure modes make them material.

Readiness should scale controls to evidence risk, irreversibility, scientific validity, and blast radius.

---

## 6. Suggested Planning Lite placement and follow-through

Canonical location:

```text
docs/design/project-spine/REC-PL-READINESS-001-v1.md
```

Recommended references after the current Poker readiness loop is complete:

- `docs/design/project-spine/PL-V38-CURRENT.md`
- `docs/design/project-spine/PLANNING-LITE-ROADMAP-v3.8.7.ru.md`
- `docs/design/project-spine/README.md`

Do not insert a new PL-V38 stage solely for this recommendation before Poker Field Pilot 2 finishes.

After the CHG-0009 readiness/execution evidence:

```text
if U1-U7 remain confirmed
→ carry them into PL-V38-06B readiness/eval fixtures
→ consider their implications for PL-V38-05 visibility/context

if U8/U9 are exercised by an actual native mismatch
→ add a dedicated eval fixture for incidental discovery → unanchored recommendation routing

if Readiness repeatedly cannot express these guarantees without ad-hoc prose
→ consider a bounded workflow/schema improvement before later orchestration work
```

---

## 7. Evidence status

Already observed:

- detailed Planning with 10 tasks and 16 mapped ACs;
- formal Readiness `Needs revision`;
- missing hypothesis-axis identity;
- config/provenance/result identity conflation;
- no exact-workload runtime gate;
- forbidden official execution hidden but programmatically reachable in the planned design;
- evidence-role isolation not mechanically negative-tested;
- final evidence not yet bound to one reviewed source revision;
- Planning returned to Draft/In progress without expanding Roadmap scope.

Still to test:

- corrected native-vs-authoritative evaluator parity routing;
- creation of a genuine incidental unanchored/deferred Recommendation if parity fails;
- repeated Readiness after minimal patch;
- whether the same readiness semantics generalize outside research-heavy Poker work.
