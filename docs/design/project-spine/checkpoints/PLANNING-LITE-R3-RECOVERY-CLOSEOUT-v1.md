# PLANNING LITE — R3 RECOVERY / CLOSEOUT

**Document ID:** `PL-R3-RECOVERY-CLOSEOUT-001`
**Version:** `v1.0`
**Date:** `2026-08-25`
**Status:** `FINAL RECOVERY / CLOSEOUT`
**Recommended canonical placement:**
`docs/design/project-spine/support/checkpoints/PL-R3-RECOVERY-CLOSEOUT-001.md`

**Related campaign:** `routing-policy-calibration-001-r3`
**Candidate:** `status-sufficient-routing-v1`
**Hypothesis:** `HYP-ROUTER-001`
**Related Change:** `CHG-PL-FIELD-CONTROL-PACK-001`

---

## 1. Purpose

This document repairs the Planning Lite design-spine understanding of R3.

The previously carried working assumption was:

> `r3-A02` is authorized but not started; the next action is to start the second independent attempt.

That assumption was derived from an earlier frozen checkpoint and is now known to be stale.

Forensic recovery of the live Campaign journal, current `LAB_STATE`, and surviving A02/A03 receipts shows that R3 progressed substantially beyond that checkpoint:

- `r3-A02` was started and completed;
- A02 passed the hard gate and produced valid suite evidence;
- A02 Candidate Review concluded `continue`;
- the historical A01 suite projection was reconciled into production-compatible evidence;
- `r3-A03` was started and completed;
- A03 also passed the hard gate and produced valid suite evidence;
- the Campaign reached three scientifically reviewed valid independent attempts;
- the Campaign then stopped because the already-authorized A03 caused a token-budget overrun;
- candidate promotion was **not** authorized.

This closeout replaces the stale operational picture without rewriting historical artifacts.

---

# 2. Recovery conclusion

## 2.1 Canonical current interpretation

```text
R3 CAMPAIGN
===========

A01
  valid independent attempt
  historical suite-projection seam later reconciled

A02
  STARTED
  COMPLETED
  hard gate PASS
  improved = true
  verdict = promote-for-fixture
  recommended arm = snapshot

A02 Candidate Review
  decision = continue
  next_action = start_next_independent_attempt

A01 historical evidence reconciliation
  COMPLETE
  production-compatible suite representation added
  historical attempt event preserved

A03
  STARTED
  COMPLETED
  hard gate PASS
  improved = true
  verdict = promote-for-fixture
  recommended arm = snapshot

Campaign scientific state
  3 / 3 scientifically reviewed valid attempts
  scientific_outcome = keep-for-independent-review

Candidate promotion
  NOT AUTHORIZED

Campaign
  STOPPED

Stop cause
  token_budget_overrun_after_authorized_attempt_execution
```

---

# 3. Authoritative recovered evidence

## 3.1 Campaign journal

Current journal:

```text
D:\documents\planning-lite-experiments\
  routing-policy-calibration-001-r3\
  campaign-journal.jsonl
```

Observed Campaign state:

```text
sequence            = 13
events              = 13
attempts started    = 3
attempts completed  = 3
campaign status     = stopped
next_action         = none
```

The recovered event sequence is:

| Seq | Event | Operational meaning |
|---:|---|---|
| 1 | `campaign_initialized` | Campaign created |
| 2 | `hypothesis_registered` | `HYP-ROUTER-001` registered |
| 3 | `candidate_registered` | candidate registered |
| 4 | `attempt_started` | A01 started |
| 5 | `attempt_completed` | A01 completed |
| 6 | `candidate_reviewed` | first review |
| 7 | `attempt_started` | A02 started |
| 8 | `attempt_completed` | A02 completed |
| 9 | `candidate_reviewed` | A02 review |
| 10 | `attempt_evidence_reconciled` | A01 historical suite projection reconciled |
| 11 | `attempt_started` | A03 started |
| 12 | `attempt_completed` | A03 completed |
| 13 | `campaign_stopped` | Campaign stopped after budget overrun |

The old sequence-6 checkpoint remains valid historical evidence, but it is **not current Campaign state**.

---

## 3.2 A02 recovered result

Attempt:

```text
attempt_id = routing-policy-calibration-001-r3-a02
suite_id   = routing-policy-calibration-001-r3-a02
eval_id    = lifecycle-status
adapter    = balanced-suite-v1
```

Completion evidence:

```text
hard_gate_passed = true
improved         = true

suite_status     = completed
verdict_status   = promote-for-fixture
recommended_arm  = snapshot

total_tokens     = 587720
duration_seconds = 2149.393197
```

A02 Candidate Review:

```text
decision            = continue
operational_meaning = collect-or-reconcile-evidence
next_action          = start_next_independent_attempt
promotion_status     = not_requested
```

A02 therefore counts as a completed, valid independent attempt.

---

## 3.3 A01 projection reconciliation

Campaign sequence 10 records:

```text
event_type = attempt_evidence_reconciled

attempt_id = routing-policy-calibration-001-r3-a01
suite_id   = routing-policy-calibration-001-r3-a01
eval_id    = lifecycle-status

reason     = historical_suite_projection_reconciliation
adapter    = balanced-suite-reconciliation-v1

suite_status    = completed
verdict_status  = promote-for-fixture
recommended_arm = snapshot
```

Important interpretation:

- this was a reconciliation of historical evidence representation;
- it did not require rewriting the original A01 completion event;
- the earlier A01 `completion_binding` / production `suite` projection seam is no longer an unresolved blocker for the three-attempt scientific reading;
- historical lineage must remain preserved.

---

## 3.4 A03 recovered result

Attempt:

```text
attempt_id = routing-policy-calibration-001-r3-a03
suite_id   = routing-policy-calibration-001-r3-a03
eval_id    = lifecycle-status
adapter    = balanced-suite-v1
```

Completion evidence:

```text
hard_gate_passed = true
improved         = true

suite_status     = completed
verdict_status   = promote-for-fixture
recommended_arm  = snapshot

total_tokens     = 561943
duration_seconds = 366.345462
```

A03 therefore counts as the third scientifically valid independent attempt.

---

# 4. Campaign stop and budget finding

Sequence 13 records:

```text
event_type = campaign_stopped

reason =
token_budget_overrun_after_authorized_attempt_execution
```

Budget accounting:

```text
max_total_tokens                  = 1500000
tokens_before_a03_completion      = 1164970
remaining_tokens_before_completion = 335030

a03_total_tokens                  = 561943

tokens_after_a03_completion       = 1726913
token_overrun                     = 226913

budget_increase_authorized        = false
```

The accounting rule was:

```text
record_sunk_execution_cost_then_stop;
do_not_hide_or_reauthorize_spend
```

The final Campaign scientific disposition was:

```text
scientifically_reviewed_valid_attempts = 3
scientific_outcome                     = keep-for-independent-review
candidate_promotion_authorized         = false
candidate_review_written               = false
operator_action_required               = new_manifest_new_campaign_decision
```

This distinction is critical:

```text
SCIENTIFIC VALIDITY != PROMOTION AUTHORIZATION
SCIENTIFIC COMPLETION != BUDGET-GOVERNANCE SUCCESS
```

The Campaign obtained enough scientific evidence to support independent review, but it also exposed a governance defect in attempt admission.

---

# 5. Current LAB_STATE

Recovered current state:

```text
state_identity_sha256 =
b06afdb7398fc67eb40516d5ef83c4924b52f1e743d41ea014a4c7799d4a9b0d

updated_by_change =
R3-A03-GOVERNED-BUDGET-OVERRUN-RECONCILIATION-v1.0.0
```

Campaign projection in `LAB_STATE`:

```text
campaign.sequence           = 13
campaign.campaign_status    = stopped
campaign.next_action        = none
campaign.attempts_started   = 3
campaign.attempts_completed = 3

campaign.total_tokens       = 1726913
campaign.wall_clock_seconds = 2878.005659

r3_a02_authorized = true
r3_a02_started    = true

r3_a03_authorized = true
r3_a03_started    = true
```

This state supersedes the earlier operational assumption that A02 had not started.

---

# 6. Scientific interpretation

## 6.1 What R3 demonstrated

Across three scientifically valid independent attempts:

- the candidate repeatedly passed the hard gate;
- A02 and A03 both reported `improved = true`;
- both A02 and A03 produced `verdict_status = promote-for-fixture`;
- both independently recommended `snapshot`.

The proper bounded conclusion is:

> `snapshot` has repeated independent fixture-level support in this Campaign and is suitable for continued controlled evaluation / independent review.

The result does **not** authorize the stronger claim that:

- `snapshot` is universally optimal;
- the candidate should be promoted automatically;
- automatic routing should be shipped;
- the R3 result alone establishes a production-wide policy.

The Campaign itself explicitly stopped short of candidate promotion.

---

# 7. Governance interpretation

R3 produced a second, separate result:

> An attempt can be validly authorized under the current governance flow even when the remaining Campaign token budget is insufficient to absorb a plausible successful completion.

A03 began with:

```text
remaining budget = 335030 tokens
```

but consumed:

```text
561943 tokens
```

The defect is therefore not post-hoc accounting. It is **pre-attempt budget admission**.

Canonical discovery statement:

```text
DISCOVERY:
Authorization did not guarantee affordability.

A governed expensive attempt was allowed to start while the remaining
Campaign budget was lower than the realized attempt cost.

The correct fix class is pre-attempt reservation/admission,
not hiding sunk cost or retroactively increasing the budget.
```

Recommended classification:

```text
Discovery ID:
DISC-PL-R3-BUDGET-ADMISSION-001

Status:
VALIDATED FIELD DISCOVERY

Roadmap treatment:
separate governance recommendation / future work unless explicitly
added to an authorized Change
```

This discovery must **not silently expand**
`CHG-PL-FIELD-CONTROL-PACK-001`.

---

# 8. Relationship to CHG-PL-FIELD-CONTROL-PACK-001

## 8.1 Previous dependency assumption

Before this recovery, the preferred sequencing was:

```text
finish frozen PILOT-PL-DIRECTION-002 / Attempt 002
→ preserve it as clean comparator
→ then implement Field Control Pack
```

That dependency is now satisfied historically.

There is no need to:

- restart A02;
- rerun A02;
- reconstruct a new A02 Campaign event;
- restore an old sequence-6 Campaign journal;
- reopen R3 merely to satisfy the old checkpoint;
- spend more LLM tokens to recreate evidence that already exists.

---

## 8.2 Effect on Change status

`CHG-PL-FIELD-CONTROL-PACK-001` may now move from:

```text
DEFINITION DRAFT
waiting for frozen field-gate completion
```

to:

```text
DEFINITION COMPLETE / IMPLEMENTATION-ELIGIBLE

implementation authorization:
NOT IMPLIED BY THIS CLOSEOUT
```

This is an eligibility transition, not an automatic Change authorization.

---

## 8.3 R3 evidence that should inform the Field Control Pack

R3 supports the following implementation posture.

### A. Keep the first functional candidate bounded

Do **not** use R3 as justification for implementing the full future roadmap.

The Field Control Pack remains a bounded promotion of already field-qualified control rules.

### B. Preserve explicit evidence-bearing gates

R3 showed the value of explicit:

```text
attempt start
→ execution evidence
→ validity
→ outcome review
→ production completion
→ candidate review
→ reconciliation
```

The Field Control Pack should keep evidence-bearing boundaries rather than collapse them into one opaque “agent succeeded” state.

### C. Keep reconciliation distinct from execution

A01 historical projection reconciliation demonstrates that:

```text
historical execution fact
!=
current production evidence representation
```

A representation seam can be repaired without rewriting history.

This supports the Field Control Pack principles of:

- no silent residue;
- explicit reconciliation;
- placement determinacy;
- structured blockers;
- preserving lineage.

### D. Use bounded behavioral control-plane fixtures

R3 provides additional support for the already proposed Field Control Pack pilot strategy:

```text
3–6 bounded behavioral control-plane fixtures
rather than immediate construction of a large generic Eval Core
```

The R3 campaign itself should be treated as field evidence for why small, explicit, evidence-bearing fixtures are useful.

### E. Do not promote automatic routing from R3

Although `snapshot` won repeatedly at fixture level, automatic Execution Pattern / model / context routing remains deferred.

This closeout does not move automatic routing into the current Field Control Pack scope.

---

# 9. Field Control Pack scope after R3 closeout

The current Change should retain its existing promoted-now scope:

1. `Discovery != Recommendation`
2. manual Recommendation Absorption
3. exhaustive-within-scope Readiness
4. conditional four-layer Contract Closure:
   - SHAPE
   - SEMANTICS
   - ENCODING
   - OWNERSHIP
5. determinacy tests
6. Materiality / Simplicity challenge
7. Execution Semantic Choice Guard
8. blocker locality
9. Execution Envelope
10. closed-world / nearest-wrong probes
11. structured blocker representation

Pilot items remain:

- Independent Task Closure Review for selected high-leverage / contract-heavy work;
- manual bounded recommendation CONVERGE;
- 3–6 Poker-derived behavioral control-plane fixtures.

Deferred items remain deferred unless separately authorized.

R3 does not justify scope growth.

---

# 10. Design-spine updates required

This closeout should produce the following bounded spine corrections.

## 10.1 `project-spine/CURRENT.md`

Replace any current statement equivalent to:

```text
r3-A02 authorized / not started
next = R3-A02 governed independent attempt start
```

with:

```text
R3 CAMPAIGN — CLOSED / STOPPED

3/3 scientifically reviewed valid independent attempts completed.

A01 historical suite-projection seam:
RECONCILED

A02:
COMPLETE

A03:
COMPLETE

Scientific disposition:
KEEP FOR INDEPENDENT REVIEW

Repeated fixture-level recommendation:
SNAPSHOT

Candidate promotion:
NOT AUTHORIZED

Campaign stop:
TOKEN BUDGET OVERRUN AFTER AUTHORIZED A03

Further R3 execution:
NOT CURRENTLY AUTHORIZED OR RECOMMENDED

Field Control Pack:
frozen field-gate dependency SATISFIED;
CHG-PL-FIELD-CONTROL-PACK-001 is implementation-eligible.
```

---

## 10.2 Roadmap

Do not create a new roadmap vertebra for the R3 recovery.

Record only the changed dependency state:

```text
R3 frozen comparator / field gate:
SATISFIED

Field Control Pack implementation:
UNBLOCKED BY R3
```

No automatic promotion of Context Router or `snapshot` policy is implied.

---

## 10.3 Discoveries

Add or retain:

```text
DISC-PL-R3-BUDGET-ADMISSION-001
```

with the core observation:

```text
A governed expensive attempt may be authorized while remaining Campaign
budget is insufficient for its plausible completion cost.
```

Possible future recommendation family:

```text
pre-attempt token reservation
budget admission
bounded worst-case / expected-cost check
explicit operator override
```

Do not absorb this into Field Control Pack without explicit scope amendment.

---

## 10.4 Historical checkpoints

Historical sequence-6 records are not invalid.

They should be interpreted as:

```text
VALID HISTORICAL CHECKPOINT
NOT CURRENT STATE
```

No historical file should be rewritten merely to make it look current.

---

# 11. Explicit non-actions

After this closeout, do **not**:

- rerun A02;
- recreate sequence 7;
- restore the sequence-6 Campaign journal over sequence 13;
- reconstruct old A01 reconciliation code merely to repeat an already recorded historical transition;
- claim R3 candidate promotion;
- open a new R3 Campaign solely to make the old checkpoint “finish cleanly”;
- add automatic routing to `CHG-PL-FIELD-CONTROL-PACK-001`;
- hide the A03 token overrun;
- retroactively increase the old Campaign budget.

---

# 12. Supersession statement

This document supersedes the **operational interpretation**:

```text
r3-A02 = AUTHORIZED / NOT STARTED
next_action = start_next_independent_attempt
```

as a statement about the current project state.

It does **not** supersede or invalidate the historical checkpoint in which that statement was true.

Canonical interpretation:

```text
HISTORICAL CHECKPOINT:
A02 not yet started
        ↓
later legal Campaign evolution
        ↓
CURRENT CLOSEOUT:
A02 complete
A01 evidence reconciled
A03 complete
Campaign stopped at sequence 13
```

This is a state-progression correction, not a history rewrite.

---

# 13. Closeout decision

```text
R3 execution status:
COMPLETE

R3 scientific evidence:
SUFFICIENT FOR INDEPENDENT REVIEW

R3 candidate promotion:
NOT AUTHORIZED

R3 further execution:
NOT RECOMMENDED UNDER CURRENT CAMPAIGN

R3 Campaign:
CLOSED / STOPPED

Field-gate dependency for
CHG-PL-FIELD-CONTROL-PACK-001:
SATISFIED

CHG-PL-FIELD-CONTROL-PACK-001:
IMPLEMENTATION-ELIGIBLE
NOT YET IMPLEMENTATION-AUTHORIZED
```

---

# 14. Next permitted Planning Lite action

The next Planning Lite development action should be:

```text
Review the existing
CHG-PL-FIELD-CONTROL-PACK-001-DEFINITION-DRAFT

against this R3 closeout,
confirm that no scope amendment is required,
then explicitly authorize or revise the bounded implementation candidate.
```

R3 itself requires no further execution before that review.

---

# 15. Compact spine capsule

```text
R3 recovered final state
------------------------

Campaign:
routing-policy-calibration-001-r3

Final sequence:
13

Attempts:
3 started / 3 completed / 3 scientifically valid

A01:
valid; historical suite-projection seam reconciled

A02:
complete; hard gate PASS; improved;
promote-for-fixture; recommended snapshot;
587720 tokens

A03:
complete; hard gate PASS; improved;
promote-for-fixture; recommended snapshot;
561943 tokens

Scientific outcome:
keep-for-independent-review

Candidate promotion:
not authorized

Campaign stop:
token_budget_overrun_after_authorized_attempt_execution

Budget:
1,500,000 max
1,726,913 actual
226,913 overrun

Governance discovery:
authorization != affordability;
pre-attempt budget admission/reservation required as separate work

Field Control Pack dependency:
satisfied

CHG-PL-FIELD-CONTROL-PACK-001:
implementation-eligible, not automatically authorized
```

---

## End state

**R3 is closed as a completed field-evidence campaign with a valid scientific result and a separate governance defect.**

The correct Planning Lite move is forward:

```text
R3 closeout
→ reconcile design spine
→ review bounded Field Control Pack definition
→ explicit implementation authorization
```

not backward into A02 reconstruction.
