# PILOT-PL-DIRECTION-002 — PREP-FINDING-001

**Class:** consumer-update compatibility defect  
**Stage:** non-scored preparation  
**Scored attempt started:** NO

## Condition

Poker uses Planning Lite as local operational state:

```text
.planning/
.agents/
```

Both are intentionally Git-ignored and absent from the public Poker history.

## Observation

A disposable v4.2.0 Poker preview was updated with ordinary Copier semantics to Planning Lite `e51320b`.

```text
before snapshot: 254 files
after snapshot:  174 files

REMOVED   96
CHANGED   26
ADDED     16
UNCHANGED 132
```

Many removed paths were still present in the new central template and were centrally managed. Therefore the removals were unintended.

`planning-lite check` and `update --dry-run` also failed to expose this file-level mutation plan before the disposable write.

## Interpretation

The current updater assumed the update-enabled installation model where generated managed files are tracked by Git/Copier history. That assumption does not hold for Poker's deliberate local-only Planning Lite state.

## Disposition

```text
PILOT-PL-DIRECTION-002 Attempt 001: NOT STARTED
Poker canonical state: UNCHANGED / FROZEN
PL-V38-05: DO NOT START
corrective change: PL-V38-PREP-01
```

After the corrective change, repeat the non-scored migration preview before creating `PILOT_READY`.
