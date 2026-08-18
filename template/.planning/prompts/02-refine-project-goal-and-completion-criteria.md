# Refine project direction and completion target

Use this entry point for whole-project purpose, intended deliverable, Target State, non-goals, completion meaning, or Capability Model work.

Planning Lite still uses **one mode and one authoritative workflow per turn**.

Choose exactly one operation:

1. If direction authority/current-state consistency is not already current, use **Audit** with `.planning/control/DIRECTION_INVENTORY.md`. Stop the turn after the inventory/gate result; do not continue into Target drafting.
2. If the consistency gate is already current and the Target is missing/materially incomplete, use **Planning** with `.planning/control/TARGET_STATE_EXPLORER.md` to create or revise a `DRAFT` Target.
3. If a Target draft exists and needs question ownership, provisional/accepted baseline status, or Capability Model work, use **Planning** with `.planning/control/TARGET_BASELINE_CALIBRATION.md`.

A later turn continues from the durable artifact produced by the previous operation.

Do not derive Gaps, prioritize the Roadmap, create implementation tasks, or edit production code through this prompt.
