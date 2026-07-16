# Planning Lite workflow

Use one entry point for one operation. Numbered prompts are optional human-facing shortcuts; control files are authoritative.

| Stage | Mode | Entry point | Authoritative workflow |
|---|---|---|---|
| Bootstrap an existing repository | Audit | `prompts/00-bootstrap-existing-project.md` | prompt itself |
| Assess current state | Audit | `prompts/01-assess-current-state-and-recommend-next-steps.md` | prompt itself |
| Refine project goal | Planning | `prompts/02-refine-project-goal-and-completion-criteria.md` | prompt itself |
| Capture or triage ideas | Dialogue / Planning | `prompts/03-capture-or-triage-recommendations.md` | `control/RECOMMENDATION_LIFECYCLE.md` |
| Define an approved change | Planning | `prompts/04-create-approved-change.md` | `control/CHANGE_DEFINITION.md` |
| Plan the change | Planning | `prompts/05-plan-approved-change.md` | `control/CHANGE_PLANNING.md` |
| Audit readiness | Audit | `prompts/06-audit-before-implementation.md` | `control/CHANGE_READINESS.md` |
| Implement | Execution | `prompts/07-implement-approved-change.md` | `control/CHANGE_EXECUTION.md` |
| Review and close | Audit | `prompts/08-review-and-close-change.md` | `control/CHANGE_CLOSURE.md` |
| Refresh durable project state | Audit | `prompts/09-refresh-project-state.md` | `control/PROJECT_STATE_REFRESH.md` |
| Quick fix or drift sync | Quick fix / Audit | `prompts/10-quick-fix.md`, `11-drift-sync.md` | `control/DRIFT_POLICY.md` |
| Amend an active change | Planning | `prompts/12-amend-active-change.md` | `control/CHANGE_AMENDMENT.md` |
| Recover from wrong mode | Recovery | `prompts/13-recover-from-wrong-mode.md` | `control/RECOVERY.md` |

A recommendation is not a change. An approved plan is not implementation authorization. Completed implementation is not closure.
