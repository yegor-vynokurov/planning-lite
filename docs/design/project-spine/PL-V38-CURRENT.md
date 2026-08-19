# PL-V38 current operational checkpoint

**Purpose:** compact resumable state for a new chat/agent. Read this file before reopening full roadmap/history.
**Updated:** 2026-08-19

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
PRIMARY NEXT: start PILOT-PL-DIRECTION-002 scored Attempt 001 with the frozen `operator/ENTRY_PROMPT.txt`
PRE_UPDATE_BASELINE: PASS / captured at Poker `f88a7fb9aeb5e6baa62cd362a9156fa4a943c063`
PILOT PREPARATION: 1.1.2 / validation PASS
REPAIRED DISPOSABLE PREVIEW: PASS / REMOVE_MANAGED=0 / Doctor OK / second plan zero mutations
CANONICAL POKER MIGRATION: PASS / metadata-only commit `920dad303f8750b5bc65b38f3bace4f72cb2819c` on local branch `planning/continuation-baseline`
PROJECT SPINE MATERIALIZATION: PASS
PILOT_READY: PASS / receipt `runs/preflight/pilot-ready/PILOT_READY.json`
REMOTE PILOT CANDIDATE: `pilot/pl-direction-002` → `c7a8cce...`
SCORED ATTEMPT-001: NOT STARTED / attempts executed = 0
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

All non-scored migration/materialization gates are complete. The repaired local-only updater has passed synthetic regression, disposable real-Poker replay, canonical read-only check, canonical atomic update, Doctor, and idempotence. The canonical scored fixture is clean and `PILOT_READY: PASS`.

Start exactly one scored Attempt 001 with the frozen entry prompt from the Lab package:

```text
operator/ENTRY_PROMPT.txt
```

Do not add coaching before the entry turn. After the response, classify it using the frozen `operator/BRANCH_POLICY.md` (A–H). Only branch A permits the later frozen Follow-up A; genuine inconsistency follows branch B; premature write or historical-priority regression are hard failures.

Expected Poker field state remains:

```text
fixture branch: planning/continuation-baseline
fixture HEAD: 920dad303f8750b5bc65b38f3bace4f72cb2819c
scientific parent: f88a7fb9aeb5e6baa62cd362a9156fa4a943c063
CHG-0008 completed
RM-PKR-001 still NOW
GAP-PKR-002 open
GAP-PKR-003 open
Bayesian study protocol exists
study implementation absent
no active Change
implementation authorized: No
```

The field test should determine whether Planning Lite can correctly conclude roughly:

```text
completed protocol Change contributed to RM-PKR-001
BUT RM-PKR-001 is not complete
AND GAP-PKR-002 / GAP-PKR-003 remain open
→ next governed step is bounded Change definition for implementation/evidence of the approved study protocol
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

After Attempt 001, preserve the full agent response and branch classification before any recovery/diagnostic turn. Reconcile field findings before deciding whether PL-V38-05 should proceed unchanged, be amended, or be preceded by another repair change.

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
  PLANNING-LITE-ROADMAP-v3.8.7.ru.md

implementation sequence:
  PL-V38-IMPLEMENTATION-PLAN-v3.8.7.md

workflow design evidence:
  DIRECTION-WORKFLOW-PLAYBOOKS-v1.2.md

Poker-derived historical command source / comparator:
  POKER-PILOT-OPERATOR-COMMANDS-v1.md

research asset roles:
  RESEARCH-ASSET-OWNERSHIP-v1.md

consolidated recommendation:
  REC-PL-DIRECTION-001-v2.md

local-only update corrective change:
  PL-V38-PREP-01-LOCAL-ONLY-UPDATE-SAFETY.md

pre-pilot finding:
  PILOT-PL-DIRECTION-002-PREP-FINDING-001.md

Poker snapshot replay:
  PL-V38-PREP-01-POKER-REPLAY.md
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
