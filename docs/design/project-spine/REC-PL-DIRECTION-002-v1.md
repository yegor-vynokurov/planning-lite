# REC-PL-DIRECTION-002 v1 — Authority-owned consistency and evidence-safe readiness

**Status:** `PROVISIONAL / FIELD-DERIVED / OPEN`  
**Date:** 2026-08-20  
**Source:** `PILOT-PL-DIRECTION-002`, non-scored preparation + scored Attempt 001  
**Visibility:** `ACTIVE_DIRECTION` until the Poker field findings are reconciled  
**Implementation authority:** none; this recommendation records field evidence and constraints

---

## 1. Why this recommendation exists

Poker Field Pilot 2 produced three connected observations.

First, non-scored preparation showed that a consumer can be Git-clean while its intentionally
local-only `.planning/.agents` state still needs framework migration or semantic reconciliation.
That produced `PL-V38-PREP-01`.

Second, scored Attempt 001 correctly stopped before Change creation when durable current-state
provenance lagged behind the actual fixture. The agent used the owning
`PROJECT_STATE_REFRESH` workflow, changed only factual/local planning state, preserved
`RM-PKR-001`, created no Change, and left production untouched.

Third, the pilot-readiness harness itself produced false positives when it tried to validate
consistency by scanning long narrative documents for forbidden historical tokens. In the
reconciled Poker `CURRENT_STATE.md`:

- the authoritative current block correctly identifies fixture HEAD `920dad3...`, branch
  `planning/continuation-baseline`, parent `f88a7fb...`, production baseline `379920a`, and
  Planning Lite `c7a8cce`;
- `f88a7fb` remains legitimate historical/scientific parent provenance;
- the word `uncommitted` remains legitimate history describing already-completed CHG-0004-2 /
  CHG-0005 work;
- CHG-0008 appears elsewhere as a closed protocol-only planning packet.

Therefore whole-document negative regexes confuse historical provenance with current truth.

---

## 2. Recommendation

Planning Lite direction consistency, readiness, context selection, and later automation should
validate **authoritative current assertions**, not require all artifacts to duplicate all facts and
not infer staleness from the mere presence of historical tokens.

The governing model should be:

```text
fact
  ↓
authoritative owner
  ↓
current assertion / receipt
  ↓
cross-owner consistency check
```

not:

```text
search every durable document
  ↓
forbid old commit IDs / words globally
  ↓
treat any historical occurrence as current drift
```

---

## 3. Semantic units

| Unit | Recommendation unit | Current field state | Destination / trigger |
|---|---|---|---|
| `REC-PL-DIRECTION-002/U1` | Define an **authority-owned consistency graph**: Git owns actual branch/HEAD/clean state; `ACTIVE` owns lifecycle/gate/authorization; `CURRENT_STATE` owns durable factual provenance; `ROADMAP` owns accepted direction + bounded provenance; other Project Spine artifacts own their explicit semantics. | `CARRIED_FORWARD` | Cross-cutting requirement for deterministic validators, PL-V38-05 context policy, PL-V38-06B fixtures, PL-V38-07 compiler, PL-V38-08 orchestration. |
| `REC-PL-DIRECTION-002/U2` | Validate current truth through **positive current assertions** or stable machine-readable fields/receipts. Historical references are allowed outside the current-authority seam. Avoid whole-document negative-token scans for `old SHA`, `uncommitted`, etc. | `CARRIED_FORWARD` | Immediate pilot-harness correction; product promotion only after field reconciliation. |
| `REC-PL-DIRECTION-002/U3` | Make readiness multidimensional: distinguish at least `SEMANTIC_DIRECTION_READY`, `PROVENANCE_READY`, `LIFECYCLE_READY`, and `FRAMEWORK_READY`; `PILOT_READY`/future eval receipts compose these dimensions instead of collapsing them into one boolean intuition. | `CARRIED_FORWARD` | Strong input to PL-V38-06B fixture qualification and later deterministic orchestration. |
| `REC-PL-DIRECTION-002/U4` | Preserve the principle `repository clean != planning consistent`. Git cleanliness is evidence for one owner only; local-only project planning state needs its own freshness/consistency evidence. | `PARTIALLY_REALIZED` | Already exercised by PW-DIR consistency routing and Attempt 001; add explicit regression/eval coverage in PL-V38-06B. |
| `REC-PL-DIRECTION-002/U5` | Treat a valid reconciliation as a **bounded detour**. After fact-only reconciliation, resume the original governed planning question without reprioritizing the accepted Roadmap or forcing a broad re-audit. | `PARTIALLY_REALIZED` | Attempt 001 Branch B passed. Verify resume behavior in Attempt 002 and encode as workflow/eval invariant if repeated. |
| `REC-PL-DIRECTION-002/U6` | Human direction authority must not silently become an obligation for the user to invent the next option. Where the accepted Roadmap supplies enough evidence, Planning Lite should be able to propose bounded candidate slice(s) and a preferred handoff while reserving approval/selection to the human. | `UNCERTAIN / TO_TEST` | Attempt 002 is the direct test. Amend PL-V38-04/CHANGE_DEFINITION handoff semantics only if field evidence confirms the agent is over-delegating candidate formation. |
| `REC-PL-DIRECTION-002/U7` | Prefer a small stable **provenance seam** (explicit fields or deterministic receipt) over parsing an entire evolving narrative `CURRENT_STATE.md` when machine validation is required. Keep human-readable history, but separate it from machine-critical current facts. | `FUTURE_SEED / STRONG CANDIDATE` | Evaluate during PL-V38-05/06B before Context Compiler or orchestration; do not introduce a parallel domain-model subsystem prematurely. |

---

## 4. Field evidence already supporting the recommendation

### Local-only update boundary

Observed ordinary Copier preview:

```text
REMOVED 96
```

After `PL-V38-PREP-01`:

```text
REMOVE_MANAGED = 0
atomic local-only update = PASS
Doctor = OK
second plan = zero mutations
```

### Attempt 001

```text
Entry classification:
B_VALID_RECONCILIATION_DETOUR

Follow-up B:
PASS

Change created:
NO

production code changed:
NO

Roadmap reprioritized:
NO
```

The reconciliation refreshed current provenance only and stopped at the next authority gate.

### Readiness-harness false positives

False check 1:

```text
ACTIVE must contain current Git branch
```

Rejected because branch is owned by Git/current factual provenance, while `ACTIVE` owns
lifecycle/gate/authorization.

False check 2:

```text
CURRENT_STATE must not contain "uncommitted" near any CHG-0008 occurrence
```

Rejected because long durable history legitimately contains both tokens in independent historical
statements. Machine validation must target the current-authority seam.

---

## 5. Roadmap effect

This recommendation does **not** justify a new feature stage before Poker Field Pilot 2.

Current sequence remains:

```text
PL-V38-01..04        COMPLETE
PL-V38-PREP-01       COMPLETE
Poker Field Pilot 2 IN PROGRESS
  Attempt 001        CLOSED / Branch B reconciliation PASS
  Attempt 002        NEXT
PL-V38-05            STOPPED pending field reconciliation
```

Recommended reconciliation rule after Attempt 002:

```text
if U6 confirmed
→ amend bounded-Change handoff semantics before PL-V38-05

if only U1-U5/U7 confirmed
→ carry them as explicit requirements/eval cases into PL-V38-05 and PL-V38-06B
   without inserting another product stage

if new safety failure appears
→ consider a bounded corrective change before PL-V38-05
```

---

## 6. Acceptance / evidence plan

Before this recommendation is promoted from `PROVISIONAL`:

1. run Attempt 002 from the reconciled fixture with the unchanged frozen entry prompt;
2. adjudicate whether the agent proposes a bounded next slice or incorrectly delegates candidate
   formation to the user;
3. qualify at least one positive and one stale-provenance fixture in PL-V38-06B;
4. verify historical SHA/text can remain in durable documents without false staleness;
5. verify true stale current assertions still fail closed;
6. preserve exact owner/source evidence in the readiness receipt or ContextTrace.

---

## 7. Anti-overengineering guard

Do not respond to this finding by immediately creating:

- a Python ProjectSpine domain model;
- a general graph database of authority;
- a schema migration of every planning document;
- a Context Compiler;
- an orchestration engine.

First stabilize the owner/seam semantics in workflow docs + deterministic pilot/eval checks.
Structured fields/receipts should be the smallest mechanism that removes ambiguity.
