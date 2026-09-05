# Context policy

Presence on disk does not imply loading.

## Tier 0: always small

Read only:

1. the root `AGENTS.md` bridge;
2. `.planning/ACTIVE.md`;
3. effective configuration through `CONFIG_RESOLUTION.md`;
4. one selected mode.

## Tier 1: one operation

Load at most one authoritative functional workflow for the current operation. A skill or numbered prompt should route to it, not duplicate it.

Load at most one engineering discipline by default. Load a second only when the operation genuinely crosses two distinct concerns and the added context is necessary.

For active work, prefer the active change `context.md`, current `tasks.md` section, exact relevant requirements, and targeted code or tests.

## Tier 2: governing project context

Read only applicable sections of project rules, completion criteria, Definition of Done, architecture, repository map, roadmap, glossary, or named decisions.

## Tier 3: history on demand

Load assessments, completed changes, old recommendations, drift history, raw diffs, usage logs, and archives only for a concrete question.

## Discovery rules

- Use `project/REPOSITORY_MAP.md` before broad exploration, then verify relevant claims.
- A full repository rescan requires a stated reason.
- Prefer exact paths, symbols, tests, and line ranges.
- Read templates only when creating or repairing that artifact.
- Never load all prompts, skills, disciplines, recommendations, adapters, or usage logs by default.
- After a fresh conversation, resume from durable state rather than rescanning automatically.


## Direction-stage context profiles

Whole-project direction work uses stage-dependent depth rather than one broad project scan.

### Direction inventory

Start from `ACTIVE.md`, `CURRENT_STATE.md`, charter/completion criteria, current Roadmap, project instructions/rules where authoritative, `REPOSITORY_MAP.md`, bounded Git state, and only the Change/lifecycle records needed for consistency. Expand recommendations/history only to resolve a concrete authority or freshness conflict.

### Target-State exploration

Start from the current direction inventory plus charter/completion criteria, existing Target State, and targeted evidence for disputed Target claims. Do not reopen broad history merely to brainstorm possibilities.

### Target baseline calibration

Start from the direction inventory, Target draft, and Capability Model template/current model. Read additional evidence only for unresolved `TARGET_BOUNDARY_QUESTION` items. Capability-design and research questions do not justify broad history by default.

### Current Capability Assessment

Start from the accepted Target, current Capability Model, direction inventory, `CURRENT_STATE.md`, and `REPOSITORY_MAP.md`. Inspect repository/code/test/data/documentation evidence capability by capability. Open historical Changes only when a current coverage/provenance claim depends on that exact record. Do not load recommendation or old-Roadmap history by default.

### Causal Gap derivation

Start from the accepted Target/Capability baselines and the current capability assessment. Treat the assessment as the primary evidence boundary. Do not rescan the repository or open recommendation/Roadmap history unless a specific assessment statement is uninterpretable without targeted evidence.

### Recommendation + historical Roadmap reconciliation

Start from the accepted Target/Capability baselines, current capability assessment, and current Gap Map. Then intentionally load the recommendation registry/items and Roadmap/history needed to account for semantic units and lineage. Open completed Change evidence only when exact delivered scope is needed to classify a unit. This is the first direction stage where broad recommendation/Roadmap history is justified; repository rescans and unrelated archives are still not justified. Record missing evidence as uncertainty. Historical order is not current priority.

### Roadmap synthesis + qualitative prioritization

Start from the accepted Target/Capability baselines, current capability assessment, current Gap Map, and current direction-history reconciliation snapshot. Treat the reconciliation snapshot as the normal broad-history boundary. Read the current Roadmap only for current canonical IDs/lineage and baseline context. Do not reopen broad recommendations, historical Roadmaps, completed Changes, or repository code unless one concrete candidate/criterion cannot be resolved from the current artifacts. Historical sequence position is not priority evidence.

After a Roadmap baseline is explicitly accepted, the next turn may load the accepted `NOW` outcome plus exact Gap/recommendation-unit lineage needed by `CHANGE_DEFINITION.md`. Do not carry the whole synthesis matrix into Change planning unless a concrete scope decision depends on it.

These profiles refine Tier 1-3 loading; they do not authorize a Context Compiler or autonomous history search.

## Context packet

The active change `context.md` is the resumable packet. Keep it compact and update it at meaningful checkpoints, decisions, amendments, stage transitions, or before a new session.

The consumer `planning-lite resume` command is a read-only derived view. It
loads only the bounded authority-first inputs named by the command contract;
its output is reconstructable and is never a replacement context store.
