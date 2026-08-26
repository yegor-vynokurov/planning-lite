# Active context packet

Keep this concise and resumable.

- Approved outcome:
- Exclusions:
- Lifecycle stage:
- Stage status:
- Current task:
- Next gate:
- Key decisions and constraints:
- Relevant modules, seams, files, and symbols:
- Verification commands:
- Git reference:
- Blockers or user decisions:
- Exact documents to read next:
- Next permitted action:

<!-- PL_FCP_EXECUTION_CONTEXT_V1:BEGIN -->
## Execution Envelope

- Authorized task(s): `<approved current task(s)>`
- Allowed write surface: `<paths / NONE>`
- Relevant read-only surface: `<paths / references / NONE>`
- Forbidden/downstream surface: `<paths / responsibilities / NONE>`
- Tool/network constraints when material: `<constraints / N/A>`
- Owned responsibility: `<bounded responsibility>`
- Next permitted action: `<single next legal action>`

The Execution Envelope is a bounded projection of the approved Plan. It cannot
expand implementation authority.

## Structured blocked outcome

Use only when the current execution slice is blocked.

- failure_class: `<class>`
- evidence: `<direct evidence>`
- blocked_slice: `<dependent slice>`
- independent_work_still_allowed: `<work / NONE>`
- missing_decision_owner: `<owner / NONE>`
- next_permitted_action: `<single next legal action>`

A blocker is local unless a shared contract makes broader execution unsafe.
Do not create an autonomous repair loop or a global blocker registry.
<!-- PL_FCP_EXECUTION_CONTEXT_V1:END -->
