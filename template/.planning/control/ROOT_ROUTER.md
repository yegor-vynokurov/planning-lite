# Project agent router

This repository uses `.planning/` for durable project intent, approved work, evidence, and handoff state.

## Route the current turn

1. Read `.planning/ACTIVE.md`.
2. Resolve effective configuration through `.planning/control/CONFIG_RESOLUTION.md`.
3. Select one mode through `.planning/control/MODE_ROUTER.md`.
4. Read only the minimum context allowed by `.planning/control/CONTEXT_POLICY.md`.
5. Load one functional workflow when the selected operation requires it.

Explicit user wording wins. A mode applies to the current turn; do not assume it persists.

## Hard boundaries

Apply `.planning/control/APPROVAL_GATES.md` before creating a change, implementing code, changing approved scope, or closing work.

Use these authoritative workflows when triggered:

- recommendation lifecycle: `RECOMMENDATION_LIFECYCLE.md`;
- change definition, planning, readiness, execution, amendment, and closure: the matching `CHANGE_*.md` file;
- quick fix and drift: `DRIFT_POLICY.md`;
- recovery: `RECOVERY.md`;
- checkpoint: `SESSION_CHECKPOINT.md`;
- Git review: `GIT_CHANGE_REVIEW.md`;
- agent switch: `AGENT_PORTABILITY.md`.

## Response economy

- Default to concise, decision-useful responses.
- Omit greetings, filler, praise, and unnecessary task restatement.
- Do not narrate routine tool calls or obvious intermediate steps.
- Preserve code, commands, paths, identifiers, and errors exactly.
- Never compress away assumptions, uncertainty, failed checks, risks, or reasons for non-obvious decisions.
- Expand when critique, planning, architecture, debugging, safety, or competing alternatives require it.
- Ask before destructive, irreversible, security-sensitive, or scope-expanding actions.
