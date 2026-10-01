# P-05 Attempt Authorization Scope Continuity Correction - Implementation Plan v1

Status: CANDIDATE / OWNER REVIEW REQUIRED
Change ID: `CHG-PL-V39-09-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-001`
Definition: `docs/design/project-spine/checkpoints/PL-V39-09-P05-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-CHANGE-DEFINITION-v1.md`
Definition canonical-LF SHA-256: `faec34cb7f3d9ad103cd16fc7b09e7212f392d35a09053ec371667e04dcf2fa5`

## Outcome

At the existing persisted Attempt claim boundary, re-resolve the retained preparation authorization against the exact stored `(change_id, task_or_operation_id)` before the row can transition from `ACTIVATABLE` to `IN_FLIGHT`. Reuse `_auth_or_raise`, `resolve_authorization`, `PreparationScopeV1` and the existing `AttemptAuthorizationError` taxonomy. A mismatched, absent, corrupt, wrong-action, or otherwise inapplicable authorization fails closed; no Attempt bytes are rewritten on rejection.

## Write and ownership manifest

| Owner | Minimum planned path | Purpose |
|---|---|---|
| Product | `src/planning_lite/attempt_runtime.py` | Add existing-scope authorization validation inside `claim_attempt`, against the authoritative row while the Attempt mutation lock is held and before store replacement. |
| Test | `tests/test_attempt_runtime.py` | Add canonical persisted foreign-scope regression and preserve valid/preparation/codec claims. |

No schema/persistence migration, Authorization store change, second authority, CLI change, lifecycle change, Roadmap edit, or other product/test path is planned. The current `execute_governed_operation` path already reaches `claim_attempt`; no separate equivalent persisted-claim admission owner was found. If implementation evidence contradicts this, stop and return the bypass path before expanding scope.

## Task order

| Task | Work | Evidence / completion condition |
|---|---|---|
| T-01 | Reproduce P-05 and freeze exact live seam. | Already completed in this planning transition: normal preparation, canonical foreign-scope codec round-trip, retained original authorization, real `claim_attempt`, observed `IN_FLIGHT`. |
| T-02 | Add the failing focused regression for the exact canonical P-05 mutant. | Test uses normal preparation, encodes/decodes the consistently changed Change + Attempt ID with the original reference, invokes production claim, expects fail-closed error, unchanged bytes and `ACTIVATABLE`. |
| T-03 | Make the smallest production correction at the existing authorization admission owner. | `claim_attempt` validates stored row scope with existing preparation Authorization helper before transition; no new status or mutation on rejection. |
| T-04 | Run focused lifecycle/authorization regressions. | Attempt Runtime and Authorization focused suites, plus the lifecycle/authorization tests that cover the current caller; valid scope and preparation-time rejection remain passing. |
| T-05 | Rerun the exact P-05 adversarial challenge through production path. | Canonical mismatch is rejected by production detector, the store stays byte-identical, and matching scope still reaches `IN_FLIGHT`. |
| T-06 | Run broader relevant suite and review candidate. | Relevant Attempt, Authorization, lifecycle, governed executor, and system traversal coverage passes; inspect exact product/test write manifest and unrelated dirt. |
| T-07 | Later product commit and Change closeout after owner review. | Requires a separate owner review/decision after implementation and adversarial rechallenge. No stage/commit authority is granted by this candidate Plan. |

No authorization-only micro-gates are inserted between implementation tasks. A failed focused regression remains the ordinary test-first step, not a separate owner gate.

## Planned adversarial acceptance

| ID | Required result |
|---|---|
| A01_VALID_SCOPE | Normal matching persisted Attempt remains claimable and reaches `IN_FLIGHT`. |
| A02_FOREIGN_CHANGE_SCOPE | Canonical persisted foreign Change identity with original authorization fails closed before replacement. |
| A03_FOREIGN_TASK_SCOPE | Canonical persisted task mismatch fails closed because task is independently included in `PreparationScopeV1`. |
| A04_AUTHORIZATION_REF_EXISTS_BUT_SCOPE_MISMATCHES | Existing reference alone is insufficient; exact resolver returns `WRONG_SCOPE`. |
| A05_CANONICAL_CODEC | Mutant is canonically encoded, decoded and re-encoded; no malformed-wire shortcut. |
| A06_NO_SILENT_REPAIR | Mismatch is rejected without identity rewrite or store-byte change. |
| A07_VALID_STATE_REGRESSION | Existing valid claim, no-double-claim, terminalization and lifecycle cases continue passing. |
| A08_PREPARATION_VALIDATION_PRESERVED | Existing wrong-scope preparation cases continue to reject before store creation. |
| A09_P05_MUTANT_KILLED | Exact current survivor from T-01 is killed through real production `claim_attempt`. |
| A10_NO_NEW_AUTHORITY | Only current Authorization/Attempt stores and resolver are used. |

## Verification and stop rules

T-02 and T-05 prove the detector reaches the specific persisted-scope seam. T-04/T-06 use existing owners first and add no duplicate invariant tests beyond the focused regression. Any requirement for new persistence, cryptographic signing, cache, service, retry model, lifecycle state, or generalized policy engine stops with `P05_CORRECTION_ARCHITECTURE_EXPANSION_REQUIRED`. Any claim/execution admission route that materially bypasses `claim_attempt` stops for owner adjudication before product surface expansion.

The Plan does not authorize implementation, sequential whole-organism proof, 09-G, Roadmap macro changes, stage, commit, or push. After successful eventual implementation/rechallenge, the next major action is owner adjudication of the sequential whole-organism proof. 09-G remains NOT STARTED.
