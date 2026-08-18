# PL-V38 current operational checkpoint

**Purpose:** compact resumable state for a new chat/agent. Read this file before reopening full roadmap/history.
**Updated:** 2026-08-18

## Central Planning Lite boundary

```text
released baseline: v4.3.0 @ 0e66941
post-release reconciliation: 0d7c923 → 0681b86 → 57eb5bd
design checkpoint: 40ca8cf (v3.8.2)
current product change: PL-V38-01 Direction Foundation (implemented by the commit containing this file)
release: not performed
```

## Priority

```text
PRIMARY: Planning Lite
POKER: FROZEN
```

Poker must remain at the clean post-CHG-0008 `Discovery / Ready`, no-active-Change boundary until PL-V38-04 is complete. Do not manually create the next Poker implementation Change before the field gate.

## Completed

```text
W0 / architecture baseline
PL-V38-00 central working-tree reconciliation
v3.8.2 design/research-asset alignment
PL-V38-01 Direction Foundation
```

PL-V38-01 adds:

```text
PW-DIR-001  DIRECTION_INVENTORY
PW-DIR-002  TARGET_STATE_EXPLORER
PW-DIR-003  TARGET_BASELINE_CALIBRATION
project/TARGET_STATE.md
project/CAPABILITY_MODEL.md
managed pristine copies
direction-stage context profiles
Doctor presence checks
```

It explicitly does **not** add Gap derivation, RecommendationUnit, Roadmap synthesis, Context Compiler, Lab/Harness integration, or autonomous Target acceptance.

## Next

```text
PL-V38-02
Current Capability Assessment + causal Gap Map
```

Then:

```text
PL-V38-03 Recommendation semantic residue + historical reconciliation
PL-V38-04 Roadmap synthesis + qualitative prioritization + bounded-Change handoff
```

After PL-V38-04 stop product expansion and run:

```text
PILOT-PL-DIRECTION-002
Poker continuation / next-Change derivation
```

Expected Poker field state:

```text
CHG-0008 completed
RM-PKR-001 NOW
GAP-PKR-002 open
GAP-PKR-003 open
Bayesian protocol exists
implementation Change absent
```

The test is whether Planning Lite can correctly derive the next bounded Bayesian implementation Change without repeating protocol work, returning to stale API priority, or prematurely integrating/closing research.

## Research assets

Do not delete or activate yet:

```text
planning-lite-lab
→ evidence/governance owner; reactivate at PL-V38-06A

planning_lite_tools/step-16.4.1
→ Context Pilot/Eval Harness reference candidate; qualify at PL-V38-06A
```

Older `planning_lite_tools` versions remain lineage/archive candidates until a receipt proves safe disposition.

## Read next only when needed

```text
full current roadmap:
  PLANNING-LITE-ROADMAP-v3.8.3.ru.md

implementation sequence:
  PL-V38-IMPLEMENTATION-PLAN-v3.8.3.md

workflow semantics:
  DIRECTION-WORKFLOW-PLAYBOOKS-v1.2.md

Poker-derived command source:
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
small deterministic validators only where useful
Poker field evidence before Context Compiler
automation last
```
