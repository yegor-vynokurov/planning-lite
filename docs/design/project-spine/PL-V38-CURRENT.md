# PL-V38 current operational checkpoint

**Purpose:** compact resumable state for a new chat/agent. Read this file before reopening full roadmap/history.
**Updated:** 2026-08-18

## Central Planning Lite boundary

```text
released baseline: v4.3.0 @ 0e66941
post-release reconciliation: 0d7c923 → 0681b86 → 57eb5bd
design checkpoint: 40ca8cf (v3.8.2)
PL-V38-01 Direction Foundation: 8d2026d
PL-V38-01 Windows EOL hash-test hotfix: 782c785
PL-V38-02 Current Capability Assessment + causal Gap Map: 3306d7a
PL-V38-03 Recommendation semantic residue + historical reconciliation: 61fe59a
PL-V38-04 Roadmap synthesis/prioritization + Change handoff: implemented by the commit containing this file
release: not performed
```

## Priority / stop gate

```text
PRIMARY NEXT: PILOT-PL-DIRECTION-002 on Poker
PLANNING LITE FEATURE EXPANSION: STOP before PL-V38-05
```

Poker was frozen while PL-V38-01 through PL-V38-04 were implemented. After local PL-V38-04 verification, resume Poker from its clean post-CHG-0008 `Discovery / Ready`, no-active-Change boundary. **Do not manually pre-create the next Poker implementation Change**; deriving that Change through the new Planning Lite direction flow is the field test.

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

## Next — field gate

```text
PILOT-PL-DIRECTION-002
Poker continuation / next-Change derivation
```

Expected Poker field state:

```text
CHG-0008 completed
RM-PKR-001 still NOW
GAP-PKR-002 open
GAP-PKR-003 open
Bayesian study protocol exists
study implementation absent
no active Change
```

Use Planning Lite itself, not the old long operator prompt as the primary procedure, to recover/confirm the accepted Poker direction and derive the next bounded Change through the new Roadmap → `CHANGE_DEFINITION` handoff.

The field test should determine whether Planning Lite can correctly conclude roughly:

```text
completed protocol Change contributed to RM-PKR-001
BUT RM-PKR-001 is not complete
AND GAP-PKR-002 / GAP-PKR-003 remain open
→ next bounded work is implementation/evidence for the approved study protocol
```

Observe especially:

```text
repeating CHG-0008 protocol work
premature Gap/Roadmap/Recommendation closure
return to stale API-first priority
production integration before study evidence
one mega-Change that tries to finish RM-PKR-001 at once
unnecessary broad history reload
loss of exact completed-Change/recommendation-unit lineage
failure to preserve protocol-first scientific boundaries
```

After the field pilot, capture findings before deciding whether PL-V38-05 should proceed unchanged, be amended, or be preceded by a repair change.

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
  PLANNING-LITE-ROADMAP-v3.8.6.ru.md

implementation sequence:
  PL-V38-IMPLEMENTATION-PLAN-v3.8.6.md

workflow design evidence:
  DIRECTION-WORKFLOW-PLAYBOOKS-v1.2.md

Poker-derived historical command source / comparator:
  POKER-PILOT-OPERATOR-COMMANDS-v1.md

research asset roles:
  RESEARCH-ASSET-OWNERSHIP-v1.md

consolidated recommendation:
  REC-PL-DIRECTION-001-v2.md
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
