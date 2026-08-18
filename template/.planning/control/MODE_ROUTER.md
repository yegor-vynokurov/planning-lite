# Mode router

Select a mode for every user turn. Modes do not persist automatically.

| Mode | Use when the user asks to | Load |
|---|---|---|
| Dialogue / critic | explain, compare, challenge, brainstorm, inspect an idea | `.planning/modes/DIALOGUE_CRITIC.md` |
| Planning | define scope, requirements, decisions, plans, tasks, or amendments | `.planning/modes/PLAN.md` |
| Execution | implement named approved work | `.planning/modes/EXECUTE.md` |
| Quick fix | make an explicitly requested tiny low-risk edit | `.planning/modes/QUICK_FIX.md` |
| Audit | assess evidence, readiness, drift, Git changes, completion, or project state | `.planning/modes/AUDIT.md` |
| Recovery | work started in the wrong mode or without authority | `.planning/control/RECOVERY.md` |

## Routing rules

- Explicit wording and explicit skill invocation win.
- When code changes are possible but authorization is ambiguous, choose Dialogue or Planning.
- For a broad effort that cannot yet support a bounded specification, use Dialogue or Planning with `WAYFINDING.md` when the uncertainty is local to one effort.
- For whole-project direction, intended deliverable, or "what should this project become?" questions, establish direction authority/current-state consistency in Audit with `DIRECTION_INVENTORY.md`, then use Planning with `TARGET_STATE_EXPLORER.md` or `TARGET_BASELINE_CALIBRATION.md`.
- Approval of an idea or recommendation is not approval of a change or plan.
- A question during execution pauses further edits for that turn unless the user also clearly says to continue.
- Mixed requests must be split at the approval boundary. Complete read-only analysis first; do not silently cross into editing.
- Special workflows and disciplines may be invoked from their normal mode without creating another mode.
