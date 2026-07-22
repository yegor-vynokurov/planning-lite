# Planning Lite workflow

Use one entry point for one operation. Numbered prompts are optional shortcuts; control files are authoritative. Active change transitions follow `control/CHANGE_LIFECYCLE.md`.

| Lifecycle stage or operation | Mode | Entry point | Authoritative workflow |
|---|---|---|---|
| Bootstrap an existing repository | Audit | `prompts/00-bootstrap-existing-project.md` | `control/PROJECT_BOOTSTRAP.md` |
| Assess current state | Audit | `prompts/01-assess-current-state-and-recommend-next-steps.md` | prompt itself |
| Discovery / uncertain broad effort | Dialogue / Planning | direct request | `control/WAYFINDING.md` when needed |
| Capture or triage ideas | Dialogue / Planning | `prompts/03-capture-or-triage-recommendations.md` | `control/RECOMMENDATION_LIFECYCLE.md` |
| Definition | Planning | `prompts/04-create-approved-change.md` | `control/CHANGE_DEFINITION.md` + `control/CHANGE_SCAFFOLD.md` |
| Planning | Planning | `prompts/05-plan-approved-change.md` | `control/CHANGE_PLANNING.md` |
| Readiness | Audit | `prompts/06-audit-before-implementation.md` | `control/CHANGE_READINESS.md` |
| Execution | Execution | `prompts/07-implement-approved-change.md` | `control/CHANGE_EXECUTION.md` |
| Verification and closure | Audit | `prompts/08-review-and-close-change.md` | `control/CHANGE_CLOSURE.md` |
| Refresh durable project state | Audit | `prompts/09-refresh-project-state.md` | `control/PROJECT_STATE_REFRESH.md` |
| Quick fix or drift sync | Quick fix / Audit | `prompts/10-quick-fix.md`, `11-drift-sync.md` | `control/DRIFT_POLICY.md` |
| Amend an active change | Planning | `prompts/12-amend-active-change.md` | `control/CHANGE_AMENDMENT.md` |
| Recover from wrong mode | Recovery | `prompts/13-recover-from-wrong-mode.md` | `control/RECOVERY.md` |

A recommendation is not a change. An approved proposal is not an approved plan. A `Ready` verdict is not execution authorization. Completed implementation is not closure. A checkpoint preserves state without advancing the lifecycle.
