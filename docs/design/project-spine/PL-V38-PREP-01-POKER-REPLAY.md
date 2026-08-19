# PL-V38-PREP-01 — Poker snapshot replay

**Purpose:** verify the corrective updater against the actual post-CHG-0008 Poker Planning Lite snapshot used during Project Spine work, without changing canonical Poker and without requiring Copier/network access.

## Inputs

- user-provided `poker(2).zip` snapshot containing the post-CHG-0008 `.planning` state;
- current Planning Lite template at the PL-V38-PREP-01 candidate;
- current ownership-aware local-only planner/apply implementation.

The current template candidate was rendered deterministically for the two Jinja destinations (`.copier-answers.planning-lite.yml` and `.planning/AGENT_PROFILE.yml`).

## Plan result

```text
ADD_MANAGED        21
UPDATE_MANAGED     26
REMOVE_MANAGED      0
ADD_PROJECT         5
KEEP_PROJECT       21
UNCHANGED_MANAGED  88
UPDATE_METADATA     1
```

The critical comparison with `PREP-FINDING-001` is:

```text
ordinary Copier preview write:
  REMOVED 96

PL-V38-PREP-01 ownership-aware replay:
  REMOVE_MANAGED 0
```

No central managed file is intentionally deleted between the relevant v4.2.0 baseline and this candidate.

## Apply result on disposable snapshot

Key project-owned hashes were preserved:

```text
.planning/ACTIVE.md                         preserved
.planning/project/CURRENT_STATE.md          preserved
.planning/project/ROADMAP.md                preserved
.planning/recommendations/INDEX.md          preserved
```

New Project Spine files appeared:

```text
.planning/control/DIRECTION_INVENTORY.md
.planning/control/ROADMAP_SYNTHESIS_PRIORITIZATION.md
.planning/project/TARGET_STATE.md
.planning/project/CAPABILITY_MODEL.md
.planning/project/GAP_MAP.md
```

A second plan after apply produced:

```text
changed mutations: 0
```

Therefore the replay is idempotent.

## Interpretation

This replay does not replace the required user-local end-to-end Copier smoke, because it bypasses candidate rendering through Copier. It does demonstrate that the ownership-aware planner/apply logic directly resolves the destructive-removal pattern observed during Poker pre-pilot preparation.

The next acceptance gate remains:

```text
central tests
→ local v4.2.0 local-only smoke with real Copier
→ disposable Poker migration preview with exact candidate ref
→ Doctor OK
→ project-owned hash check
→ PILOT_READY
```
