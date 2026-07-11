# Prompt entry points

Do not load this whole folder into context. Select one prompt for the current operation.

Modes are durable behavior contracts under `.planning/modes/`. Prompts are narrower procedures that produce particular artifacts.

| Prompt | Mode | Purpose |
|---|---|---|
| 00 | Audit | Bootstrap existing project |
| 01 | Audit | Current-state assessment and next steps |
| 02 | Dialogue / Planning | Refine goal and project completion criteria |
| 03 | Dialogue / Planning | Capture and triage recommendations |
| 04 | Planning | Convert approved direction into bounded change |
| 05 | Planning | Interactive plan and tasks |
| 06 | Audit | Pre-implementation audit |
| 07 | Execution | Implement approved tasks |
| 08 | Audit | Final review and closure |
| 09 | Audit | Reconcile out-of-band changes |
| 10 | Quick fix | Tiny low-risk edit and ledger entry |
| 11 | Audit | Periodic or immediate drift sync |
| 12 | Planning | Amend active change |
| 13 | Recovery | Recover from wrong mode or missing approval |

Canonical skills live under `.planning/skills/`. Agent adapters may expose them through client-specific skill folders or commands. Generic agents can read the canonical skill, mode, and selected prompt directly.
