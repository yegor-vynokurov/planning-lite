# PL-V38 current operational checkpoint

**Purpose:** compact resumable state for a new chat/agent. Read this file before reopening full roadmap/history.
**Updated:** 2026-08-20

## Central Planning Lite boundary

```text
released baseline: v4.3.0 @ 0e66941
post-release reconciliation: 0d7c923 → 0681b86 → 57eb5bd
design checkpoint: 40ca8cf (v3.8.2)
PL-V38-01 Direction Foundation: 8d2026d
PL-V38-01 Windows EOL hash-test hotfix: 782c785
PL-V38-02 Current Capability Assessment + causal Gap Map: 3306d7a
PL-V38-03 Recommendation semantic residue + historical reconciliation: 61fe59a
PL-V38-04 Roadmap synthesis/prioritization + Change handoff: fafe133
post-PL-V38-04 Doctor-boundary hotfix: e51320b
PL-V38-PREP-01 Local-only consumer update safety: c7a8cced0020e1e87e17f9567a5037fb44a1279f
remote pilot ref: `pilot/pl-direction-002` → `c7a8cced0020e1e87e17f9567a5037fb44a1279f` (verified by `git ls-remote`)
release: not performed
```

## Verification boundary

Central Planning Lite source-repository verification:

```text
uv sync
uv run pytest
uv run python scripts/test_template_update.py
uv run python scripts/test_local_only_update.py
```

Do **not** run `planning-lite doctor .` at the central repository root. Doctor validates an adopted/installed consumer project. `scripts/test_template_update.py` and `scripts/test_local_only_update.py` create temporary consumers and run Doctor against consumer installations; `Doctor: OK` there is the relevant installation result.

Post-PL-V38-04 docs/test-instructions hotfix: e51320b. No product/template semantics changed in that hotfix.

## Priority / stop gate

```text
PILOT-PL-DIRECTION-002: IN PROGRESS
ATTEMPT-001 ENTRY: COMPLETE / B_VALID_RECONCILIATION_DETOUR
ATTEMPT-001 FOLLOW-UP B: PASS / fact-only PROJECT_STATE_REFRESH
ATTEMPT-001 CHANGE CREATION: 0
ATTEMPT-001 PRODUCTION CHANGES: 0
CURRENT POKER FIXTURE: HEAD 920dad3 / branch planning/continuation-baseline / tracked tree clean
CURRENT DIRECTION: RM-PKR-001 remains NOW / GAP-PKR-002 and GAP-PKR-003 remain open
ATTEMPT-002: NEXT / fresh agent session with unchanged frozen entry prompt after owner-aware readiness PASS
FIELD RECOMMENDATION: recommendations/archive/absorbed/REC-PL-DIRECTION-002-v1.md
PLANNING LITE FEATURE EXPANSION: STOP before PL-V38-05
```

Poker scored fixture is now prepared on local branch `planning/continuation-baseline` at metadata-only migration commit `920dad303f8750b5bc65b38f3bace4f72cb2819c`. The scientific parent remains the clean post-CHG-0008 commit `f88a7fb...`; `.planning/.agents` remain local-only and project-owned Project Spine state has been deterministically materialized. `PILOT_READY: PASS` confirms no active Change, no implementation authorization, `RM-PKR-001` still NOW, and `GAP-PKR-002/003` still open. **Do not manually pre-create the next Poker implementation Change**; deriving that Change through the new Planning Lite direction flow remains the scored field test.

Pre-pilot preparation exposed `PREP-FINDING-001`: ordinary Copier update against Poker's intentionally Git-ignored `.planning/.agents` removed 96 managed/local files in a disposable preview even though the central template had not intentionally deleted them. The scored attempt did not start and canonical Poker was not changed. `PL-V38-PREP-01` adds a fail-closed ownership-aware local-only update path.

## Completed

```text
W0 / architecture baseline
PL-V38-00 central working-tree reconciliation
v3.8.2 design/research-asset alignment
PL-V38-01 Direction Foundation
PL-V38-01 EOL-stable integrity-test hotfix
PL-V38-02 Current Capability Assessment + causal Gap Map
PL-V38-03 Recommendation semantic residue + historical reconciliation
PL-V38-04 Roadmap synthesis + qualitative prioritization + bounded-Change handoff
PL-V38-PREP-01 Local-only consumer update safety
```

The implemented Project Spine workflow chain is now:

```text
PW-DIR-001  DIRECTION_INVENTORY [Audit]
PW-DIR-002  TARGET_STATE_EXPLORER [Planning]
PW-DIR-003  TARGET_BASELINE_CALIBRATION [Planning]
PW-DIR-004  CURRENT_CAPABILITY_ASSESSMENT [Audit]
PW-DIR-005  CAUSAL_GAP_DERIVATION [Planning]
PW-DIR-006  RECOMMENDATION_HISTORY_RECONCILIATION [Planning]
PW-DIR-007  ROADMAP_SYNTHESIS_PRIORITIZATION [Planning]
        ↓
existing CHANGE_DEFINITION on a later turn
```

PL-V38-04 adds:

```text
RoadmapOutcome synthesis from accepted/current Spine artifacts
natural one-outcome → several-Gap bundling with independent Gap closure checks
credible-alternative comparison
qualitative prioritization without fake weighted precision
NOW / NEXT / unordered LATER / FINAL_GATE / DEFERRED sequencing
explicit human acceptance before ROADMAP.md CURRENT_BASELINE mutation
research-heavy protocol-first composition when warranted
exact Roadmap outcome + Gap + RecommendationUnit Change lineage
closure guard: Change completion != RoadmapOutcome completion != Gap closure
```

Hard boundary preserved:

```text
historical Roadmap order != current priority
RoadmapOutcome != Gap != Change
no Roadmap synthesis from stale Project Spine prerequisites
no broad history reload by default after accepted reconciliation
no automatic Change creation from an accepted Roadmap
one mode + one authoritative workflow per turn
no automatic Poker activation
no PL-V38-05 before Poker field findings are reconciled
```

## Next — scored field gate

Attempt 001 is complete and closed at the reconciliation boundary.

Observed:

```text
Entry → B_VALID_RECONCILIATION_DETOUR
Follow-up B → PASS
PROJECT_STATE_REFRESH → provenance-only / no reprioritization
Change creation → none
production change → none
```

The agent correctly enforced the Current-State Consistency Gate, but this means the primary
next-Change handoff hypothesis was not cleanly tested in Attempt 001. Pilot-readiness validation
also exposed a harness weakness: machine checks must follow authoritative ownership and validate
positive current assertions rather than scan long historical documents for forbidden old tokens.

The current reconciled Poker facts are:

```text
fixture branch: planning/continuation-baseline
fixture HEAD: 920dad303f8750b5bc65b38f3bace4f72cb2819c
scientific parent: f88a7fb9aeb5e6baa62cd362a9156fa4a943c063
tracked tree: clean
Planning Lite: v4.3.0-11-gc7a8cce
active Change: none
implementation authorized: No
RM-PKR-001: NOW
GAP-PKR-002: open
GAP-PKR-003: open
```

Primary next:

```text
owner-aware ATTEMPT_002_READY validation
→ fresh agent session
→ unchanged operator/ENTRY_PROMPT.txt
→ preserve first response
→ frozen A–H adjudication
```

Do not continue Attempt 001 into user slice selection. Attempt 002 is the clean test of whether
Planning Lite can form a bounded next-step proposal from the accepted Roadmap while preserving
human approval authority.

Field findings are consolidated in:

```text
REC-PL-DIRECTION-002-v1.md
```

Reconcile Attempt 002 before deciding whether PL-V38-05 proceeds unchanged or needs a bounded
handoff-semantics repair.

## Research assets

Do not delete or activate yet merely because PL-V38-04 is complete:

```text
planning-lite-lab
→ evidence/governance owner; planned reactivation at PL-V38-06A unless field findings change sequencing

planning_lite_tools/step-16.4.1
→ Context Pilot/Eval Harness reference candidate; planned qualification at PL-V38-06A
```

Older `planning_lite_tools` versions remain lineage/archive candidates until a receipt proves safe disposition.

## Read next only when needed

```text
full current roadmap:
  roadmap/archive/PLANNING-LITE-ROADMAP-v3.8.7.ru.md

implementation sequence:
  PL-V38-IMPLEMENTATION-PLAN-v3.8.7.md

workflow design evidence:
  support/playbooks/DIRECTION-WORKFLOW-PLAYBOOKS-v1.2.md

Poker-derived historical command source / comparator:
  POKER-PILOT-OPERATOR-COMMANDS-v1.md

research asset roles:
  support/research/RESEARCH-ASSET-OWNERSHIP-v1.md

consolidated recommendation:
  recommendations/archive/absorbed/REC-PL-DIRECTION-001-v2.md

field-derived consistency/readiness recommendation:
  recommendations/archive/absorbed/REC-PL-DIRECTION-002-v1.md

local-only update corrective change:
  support/field-evidence/PL-V38-PREP-01-LOCAL-ONLY-UPDATE-SAFETY.md

pre-pilot finding:
  support/field-evidence/PILOT-PL-DIRECTION-002-PREP-FINDING-001.md

Poker snapshot replay:
  support/field-evidence/PL-V38-PREP-01-POKER-REPLAY.md
```

## Anti-drift reminder

```text
Project Spine semantics first
existing control/*.md workflow architecture first
project-owned direction truth
assessment evidence separate from durable direction truth
causal Gaps before historical reconciliation
historical reconciliation before current Roadmap priority
current Roadmap before bounded Change definition
Poker field evidence before Context Compiler
field findings before PL-V38-05+
automation last
```
