# Project agent router

This repository uses `.planning/` for durable intent, approved work, evidence, and handoff state.

## Route the turn

1. Read `.planning/ACTIVE.md`.
2. Resolve effective configuration through `CONFIG_RESOLUTION.md`.
3. Select one mode through `MODE_ROUTER.md`.
4. Apply `CONTEXT_POLICY.md`.
5. Load one functional workflow and, only when needed, one engineering discipline.

Explicit user wording wins. Modes apply to the current turn only.

## Boundaries and routes

Apply `APPROVAL_GATES.md` before approving plans, editing production code, changing approved scope, or closing work.

Use the matching authoritative workflow for bootstrap, direction inventory, Target-State exploration/calibration, Current Capability Assessment, causal Gap derivation, recommendation/history reconciliation, Roadmap synthesis/prioritization, wayfinding, recommendations, lifecycle, scaffold, definition, planning, readiness, execution, amendment, closure, drift, recovery, checkpoint, Git review, or agent portability. Do not duplicate those rules in the current prompt.

For whole-project direction work, establish authority/current-state consistency through `DIRECTION_INVENTORY.md` before Target exploration when that evidence is not already current. Use `TARGET_STATE_EXPLORER.md` for a Target draft and `TARGET_BASELINE_CALIBRATION.md` for question ownership, Target acceptance, and Capability Model foundation. After an `ACCEPTED` Target and `CURRENT_BASELINE` Capability Model exist, use `CURRENT_CAPABILITY_ASSESSMENT.md` before `CAUSAL_GAP_DERIVATION.md`. Do not infer formal Gaps directly from general assessment prose. After an accepted/current Gap baseline exists, use `RECOMMENDATION_HISTORY_RECONCILIATION.md` for broad recommendation + historical Roadmap reconciliation; do not inherit historical priority or continue into Roadmap synthesis in that turn. After that reconciliation is `CURRENT` and `READY_FOR_ROADMAP_SYNTHESIS`, use `ROADMAP_SYNTHESIS_PRIORITIZATION.md` to synthesize/compare Roadmap outcomes and, only on a later explicitly authorized turn, accept the current Roadmap baseline. Do not create a Change in the Roadmap-synthesis turn.

If a repository skill is selected and effective configuration enables usage logging, follow `SKILL_USAGE_LOGGING.md` once for the turn. Logging is non-blocking.

## Response economy

- Lead with the result, decision, blocker, or question. Omit greetings, praise, filler, and task restatement.
- Do not narrate routine reads, edits, searches, commands, or successful logs. Send interim updates only for blockers, decisions, material risks, or useful milestones.
- For routine work report only: result, changed, checked, unresolved.
- Do not repeat approved plans, unchanged facts, full diffs, or obvious next steps.
- Preserve exact paths, commands, errors, evidence, assumptions, uncertainty, failed checks, and non-obvious rationale. Expand only when they affect a decision.
- Ask before destructive, irreversible, security-sensitive, externally billed, or scope-expanding actions.
