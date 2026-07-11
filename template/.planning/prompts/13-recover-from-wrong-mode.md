# Recover from wrong mode or missing approval

Mode: Audit followed by Dialogue / critic.

Follow `control/RECOVERY.md`.

## Procedure

1. Stop affected work.
2. Inventory created and changed files, commands, side effects, tests, and data impact.
3. Identify the intended authorization and the point where the boundary was crossed.
4. Mark premature artifacts as drafts; do not forge approvals.
5. Preserve the diff. Do not revert without explicit permission.
6. Create a drift report if production code or durable state changed.
7. Present adopt, keep-draft, revise, split, and revert options with risks.
8. Update `.planning/ACTIVE.md` to a safe next action.

## Output

A concise incident summary, current safety state, available recovery paths, and the exact user decision required.
