# Project-state refresh

Use in Audit mode after bootstrap, significant implementation, closure, drift synchronization, or an explicit refresh request.

## Procedure

1. Identify which durable facts may be stale.
2. Verify those facts against targeted repository evidence and current decisions.
3. Update only affected documents:
   - `CURRENT_STATE.md`;
   - `ARCHITECTURE_OVERVIEW.md`;
   - `REPOSITORY_MAP.md`;
   - `ROADMAP.md`;
   - project completion criteria and evidence;
   - relevant decisions;
   - `GLOSSARY.md` when canonical domain language or invariants changed.
4. Preserve uncertainty and revision scope.
5. Do not rewrite unrelated documents for stylistic consistency.

A project-state refresh records facts. New opportunities belong in recommendations; implementation belongs in an approved change or qualified quick fix.

`TARGET_STATE.md` and `CAPABILITY_MODEL.md` are not ordinary refresh targets. Do not rewrite accepted direction because implementation facts changed. A material contradiction with an accepted Target should be recorded as a `TARGET_STATE_SIGNAL` and routed to Planning through `TARGET_BASELINE_CALIBRATION.md`; explicit user/durable authority is required for Target acceptance or revision.
