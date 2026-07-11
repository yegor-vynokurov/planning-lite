# Bootstrap an existing project

Mode: Audit.

## Authorization boundary

Analyze and create planning documentation only. Do not change production code, install dependencies, or create an implementation plan.

## Context discipline

Start with repository root files, primary entry points, tests, configuration, and existing architecture or contributor docs. Expand only when evidence requires it. Do not read all source files or all `.planning/` templates.

## Procedure

1. Inspect repository purpose, entry points, runtime flows, outputs, tests, configuration, dependencies, and existing docs.
2. Fill or adapt:
   - `PROJECT_CHARTER.md`;
   - `PROJECT_COMPLETION_CRITERIA.md`;
   - `PROJECT_RULES.md`;
   - `ARCHITECTURE_OVERVIEW.md`;
   - `REPOSITORY_MAP.md`;
   - `CURRENT_STATE.md`;
   - `ROADMAP.md` only with clearly proposed or approved sequencing.
3. Record the inspected revision in `REPOSITORY_MAP.md`. Build a compact path/symbol/test index so later sessions can use targeted verification instead of repeating repository-wide discovery.
4. Create a dated assessment with evidence and confidence.
5. Create separate recommendations for durable gaps and opportunities.
6. Do not invent readiness percentages when the target or scoring model is unclear.
7. Adapt project overrides in `CONFIG.yml` to repository risk and size only when evidence supports the change.
8. Update `.planning/ACTIVE.md`.
9. Stop before creating change folders or implementation plans.

## Output

Summarize current purpose, evidence, unknowns, completion measurability, top recommendations, and decisions needed from the user.
