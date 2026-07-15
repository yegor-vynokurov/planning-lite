# Project agent router

This repository uses `.planning/` for durable project intent, recommendations, approved changes, decisions, execution state, and drift control.

Keep this file short. Do not preload every file under `.planning/`. Select one mode for the current user turn, then read only that mode and its minimum context.

Planning Lite has a neutral core and optional agent adapters. Canonical skills live under `.planning/skills/`. Agent-specific invocation syntax belongs under `.planning/adapters/`, not in the core workflow.

## 1. Select the mode for each user turn

Explicit user wording wins. Natural-language instructions always work, even when the active agent has no native skill integration.

| Mode | Typical user intent | Load |
|---|---|---|
| Dialogue / critic | asks, explains, compares, challenges, brainstorms, requests ideas or analysis | `.planning/modes/DIALOGUE_CRITIC.md` |
| Planning | asks to clarify scope, create or revise a proposal, specification, plan, or tasks | `.planning/modes/PLAN.md` |
| Execution | directly authorizes implementation, code writing, or a named approved task | `.planning/modes/EXECUTE.md` |
| Quick fix | explicitly requests a tiny, low-risk edit outside the full workflow | `.planning/modes/QUICK_FIX.md` |
| Audit | asks to review, assess, check plan drift, verify completeness, or inspect current state | `.planning/modes/AUDIT.md` |
| Recovery | says work started in the wrong mode or without approval | `.planning/control/RECOVERY.md` + prompt `13` |

Logical skill names:

- `planning-dialogue`
- `planning-plan`
- `planning-execute`
- `planning-quick-fix`
- `planning-audit`
- `planning-recover`
- `planning-checkpoint`
- `planning-git-review`

The active adapter may expose these names with different syntax. Read `.planning/AGENT_PROFILE.yml` and the named adapter guide only when translating client-interface commands.

If intent is ambiguous and code changes are possible, default to Dialogue / critic or Planning. Do not infer implementation authorization from enthusiasm, discussion, approval of an idea, or approval of a recommendation.

A question asked during execution switches that turn to Dialogue / critic and pauses further edits unless the user also clearly says to continue implementing.

## 2. Hard approval boundaries

The document classes remain separate:

- Assessment: evidence-based snapshot; no implementation authority.
- Recommendation: candidate improvement; no implementation authority.
- Change: bounded approved work with specification, plan, tasks, progress, and review.

Implementation is allowed only when either:

1. an active change is approved, audited, selected in `.planning/ACTIVE.md`, and the user directly authorizes implementation; or
2. the request qualifies for Quick fix mode under `.planning/control/DRIFT_POLICY.md`.

A recommendation may map to several changes, and a change may originate from several recommendations. Preserve both directions with lists of IDs.

## 3. Context discipline

Before acting, read:

1. `.planning/ACTIVE.md`;
2. `.planning/framework/defaults.yml` and `.planning/CONFIG.yml`;
3. the selected mode file;
4. only the files required by `.planning/control/CONTEXT_POLICY.md`.

Do not read all prompts, all recommendations, old assessments, completed changes, or the whole repository by default. Reuse `.planning/project/REPOSITORY_MAP.md` and the active change `context.md`, then verify only relevant paths, symbols, tests, and stale claims with targeted searches. A repository-wide rescan requires a stated reason.

## 4. Planning and dialogue

Planning is interactive. Surface material unknowns, contradictions, options, and decisions before freezing a plan. Be candid and evidence-based. Do not agree automatically. When criticizing, propose a correction, alternative, or decision path when possible.

Do not edit production code in Dialogue / critic, Planning, or Audit mode.

## 5. Execution

Execute only approved scope and dependency-ordered tasks. Follow repository conventions and configured checks first.

For Python projects, follow PEP 8 and write readable, idiomatic code. Apply DRY, KISS, YAGNI, and SOLID where they improve the design; do not turn them into ritual abstractions.

When reality contradicts the plan:

- implementation-detail change only: record a plan amendment before continuing;
- scope, acceptance criteria, compatibility, data, security, or architectural change: stop the affected work and request approval;
- attractive unrelated idea: create a recommendation, not hidden scope.

## 6. Quick fixes and drift

Tiny out-of-plan edits use Quick fix mode and one compact row in `.planning/drift/QUICK_CHANGES.md`. They do not require a full change folder when all quick-fix criteria pass.

Run a drift sync when a threshold or immediate trigger in `.planning/control/DRIFT_POLICY.md` is reached. Never disguise API, schema, migration, security, architecture, dependency, or acceptance-criterion changes as quick fixes.

## 7. Session checkpoint

When the user requests a session checkpoint in any language, asks to prepare for context compaction, asks to prepare for a new session, or invokes the logical skill `planning-checkpoint`, stop changing production code and follow `.planning/control/SESSION_CHECKPOINT.md`.

The checkpoint updates `tasks.md`, `progress.md`, the active `context.md`, and `.planning/ACTIVE.md`, and records a compact Git summary. It does not load a full raw diff by default.

The agent prepares state and reports readiness. Context compaction, starting a new session, forking, clearing, and similar client-interface actions remain operator actions. Never claim they were executed. Translate them through the active adapter only when needed.

## 8. Git change review

Use `.planning/control/GIT_CHANGE_REVIEW.md` or the logical skill `planning-git-review` when the user requests review, a checkpoint reaches a configured risk trigger, drift or recovery requires inspection, or a non-trivial change is being closed.

Review status, stats, file names, and a bounded commit range before opening targeted patches. Do not read the entire repository diff automatically. Regular atomic commits reduce review size but do not replace plan and acceptance-criteria alignment.

## 9. Agent and model portability

Project state, approvals, plans, tests, and canonical skills are agent-neutral. Client-specific instruction files, skill folders, command syntax, hooks, and permissions belong to `.planning/adapters/`.

Before switching agent shell or model, run a checkpoint and follow `.planning/control/AGENT_PORTABILITY.md`. Do not use a long chat transcript as the primary handoff.

## 10. Recovery

If planning or code started in the wrong mode, stop. Do not silently delete or revert work. Follow `.planning/control/RECOVERY.md`, mark artifacts honestly, show the diff or affected files, and let the user decide whether to adopt, convert, revise, or revert.

## 11. Response economy

- Default to concise, decision-useful responses.
- Omit greetings, filler, praise, and unnecessary task restatement.
- Do not narrate routine tool calls or obvious intermediate steps.
- Preserve code, commands, paths, identifiers, and error messages exactly.
- Prefer structured findings over long prose.
- For routine execution, report only:
  1. result;
  2. files changed;
  3. checks performed;
  4. unresolved issues or next step.
- Never compress away assumptions, uncertainty, failed checks, risks, or reasons for non-obvious decisions.
- Expand when planning, critique, architecture, debugging, safety, or competing alternatives require explanation.
- Ask before destructive, irreversible, security-sensitive, or scope-expanding actions.