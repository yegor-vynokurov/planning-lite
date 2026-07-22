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
