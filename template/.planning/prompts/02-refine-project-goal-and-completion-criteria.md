# Refine project direction and completion target

Use this entry point for whole-project purpose, intended deliverable, Target State, Capability Model, formal Current Capability Assessment, causal Gap Map work, or Project Spine recommendation/history reconciliation.

Planning Lite still uses **one mode and one authoritative workflow per turn**.

Choose exactly one operation from the first unfinished/current stage:

1. If direction authority/current-state consistency is not already current, use **Audit** with `.planning/control/DIRECTION_INVENTORY.md`. Stop the turn after the inventory/gate result; do not continue into Target drafting.
2. If the consistency gate is already current and the Target is missing/materially incomplete, use **Planning** with `.planning/control/TARGET_STATE_EXPLORER.md` to create or revise a `DRAFT` Target.
3. If a Target draft exists and needs question ownership, provisional/accepted baseline status, or Capability Model work, use **Planning** with `.planning/control/TARGET_BASELINE_CALIBRATION.md`.
4. If Target status is `ACCEPTED` and Capability Model status is `CURRENT_BASELINE`, but current capability coverage has not been assessed for that baseline, use **Audit** with `.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md`. Stop after the evidence snapshot/readiness verdict.
5. If the current capability assessment says `Formal-Gap derivation readiness: READY` and the Gap Map is missing/stale, use **Planning** with `.planning/control/CAUSAL_GAP_DERIVATION.md`. Stop after the `DRAFT` Gap Map or explicit acceptance update.
6. If the Gap Map is `CURRENT_BASELINE` and recommendation/history reconciliation is missing or stale for that Spine baseline, use **Planning** with `.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md`. Stop after the `DRAFT` reconciliation assessment or an explicitly authorized acceptance update.

A later turn continues from the durable artifact produced by the previous operation.

Recommendation/history reconciliation is allowed only in step 6 through its authoritative workflow. Do not prioritize or synthesize the current Roadmap, create implementation tasks/Changes, or edit production code through this prompt.
