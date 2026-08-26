# Authoritative references

| Concern | Source of truth |
|---|---|
| Turn routing | `.planning/control/MODE_ROUTER.md` |
| Context limits | `.planning/control/CONTEXT_POLICY.md` |
| Configuration | `.planning/control/CONFIG_RESOLUTION.md` |
| Approval | `.planning/control/APPROVAL_GATES.md` |
| State ownership | `.planning/control/STATE_OWNERSHIP.md` |
| Recommendation lifecycle | `.planning/control/RECOMMENDATION_LIFECYCLE.md` |
| Change definition | `.planning/control/CHANGE_DEFINITION.md` |
| Change planning | `.planning/control/CHANGE_PLANNING.md` |
| Readiness audit | `.planning/control/CHANGE_READINESS.md` |
| Execution | `.planning/control/CHANGE_EXECUTION.md` |
| Amendment | `.planning/control/CHANGE_AMENDMENT.md` |
| Closure | `.planning/control/CHANGE_CLOSURE.md` |
| Quick fixes and drift | `.planning/control/DRIFT_POLICY.md` |
| Recovery | `.planning/control/RECOVERY.md` |
| Git review | `.planning/control/GIT_CHANGE_REVIEW.md` |
| Checkpoint | `.planning/control/SESSION_CHECKPOINT.md` |
| Project-state refresh | `.planning/control/PROJECT_STATE_REFRESH.md` |
| Agent portability | `.planning/control/AGENT_PORTABILITY.md` |

<!-- PL_FCP_RECOMMENDATION_REFERENCES_V1:BEGIN -->
## Recommendation accounting references

For observation-only durable evidence:

```text
.planning/control/DISCOVERY_LIFECYCLE.md
.planning/discoveries/README.md
```

For Recommendation lifecycle and semantic residue:

```text
.planning/control/RECOMMENDATION_LIFECYCLE.md
.planning/control/RECOMMENDATION_ABSORPTION.md
.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md
```

Absorption is subordinate to the existing Recommendation lifecycle and does not
create a parallel state machine.
<!-- PL_FCP_RECOMMENDATION_REFERENCES_V1:END -->
