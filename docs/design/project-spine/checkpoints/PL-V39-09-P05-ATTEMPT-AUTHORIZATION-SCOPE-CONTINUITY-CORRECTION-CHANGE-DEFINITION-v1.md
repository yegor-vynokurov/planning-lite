# P-05 Attempt Authorization Scope Continuity Correction - Definition v1

Status: CANDIDATE / OWNER REVIEW REQUIRED
Change ID: `CHG-PL-V39-09-ATTEMPT-AUTHORIZATION-SCOPE-CONTINUITY-CORRECTION-001`
Entry gate: `OWNER_ADJUDICATION_P05_ATTEMPT_AUTHORIZATION_SCOPE_CONTINUITY_CORRECTION_BEFORE_SEQUENTIAL_TRUNK_PROOF`
Owner decision consumed: `SELECT_P05_ATTEMPT_AUTHORIZATION_SCOPE_CONTINUITY_CORRECTION`
Date: 2026-10-01

## Problem and invariant

The Organism Vitality Audit's material P-05 survivor demonstrates that an Attempt can be prepared under a valid owner authorization, persisted canonically, then have its persisted Change identity consistently replaced while the original authorization reference and document remain. The canonical Attempt store decodes, and current `claim_attempt` transitions that mismatched row from `ACTIVATABLE` to `IN_FLIGHT`.

Preserve this invariant:

> An Attempt may enter a governed claim/execution state only when its current persisted identity is still covered by the exact authorization scope it references.

The problem is continuity across persistence and claim. It is not invalid serialization, an unknown authorization reference by itself, malformed Attempt state, or an absent preparation-time check.

## Exact live contracts and scope

The live `AttemptRecordV1` contract (`src/planning_lite/attempt_evaluation.py`) carries `attempt_id`, `change_id`, `task_or_operation_id`, `attempt_ordinal`, and `authorization_ref` among its fields. Its constructor enforces `attempt_id == f"{change_id}/{task_or_operation_id}/A{attempt_ordinal}"`. The authorization-bearing scope fields are exactly `change_id` and `task_or_operation_id`; the Attempt ID is derived from those plus ordinal, while ordinal is not an Authorization scope field. `authorization_ref` identifies the retained Authorization record and is not itself a scope value.

The live `AuthorizationRecordV1` (`src/planning_lite/authorization.py`) has a `PREPARATION` action and `PreparationScopeV1(change_id, task_or_operation_id)`. That exact pair defines preparation permission. The record also carries schema version, reference, authority class, authorized decision outcome, and provenance; those do not widen the scope. Recovery has a distinct `RecoveryScopeV1(attempt_id)` and is not interchangeable with preparation.

## Read-only seam discovery

| Question | Live answer |
|---|---|
| Q1 - Attempt identity bearing on authorization | `change_id` and `task_or_operation_id`; the derived `attempt_id` must remain internally consistent with them. `attempt_ordinal` is part of identity construction but not the retained preparation scope. |
| Q2 - Authorization scope | `PREPARATION` action and exact `(change_id, task_or_operation_id)` in `PreparationScopeV1`, with decision outcome `AUTHORIZED`. |
| Q3 - Preparation check | `prepare_attempt` calls `_auth_or_raise` with `PREPARATION` and `PreparationScopeV1(change, task)` before materializing the store row. |
| Q4 - Current claim check | `claim_attempt` validates the supplied ID, reads the canonical store under its lock, locates the row, checks `ACTIVATABLE`, then persists `IN_FLIGHT`; it does not resolve `row.authorization_ref` or compare the persisted row's Change/task scope. |
| Q5 - Reusable exact comparison | Yes. `_auth_or_raise` delegates to `resolve_authorization`; the existing `validate_preparation_applicability` compares the exact `PreparationScopeV1` value and yields `WRONG_SCOPE` on mismatch. Reuse this existing resolver/error path. |
| Q6 - Admission path | Yes, `claim_attempt` is the single existing persisted state-transition seam. `execute_governed_operation` calls lookup, activation admissibility, then `claim_attempt`, and stops on `AttemptRuntimeError` before invoking the governed executor. A source search found no other production call to `claim_attempt` and no other production transition that writes `IN_FLIGHT`. `invoke_governed_operation` consumes an Attempt, guidance and already-observed completion facts; it has no callback/worker/persistence path and is not a separate authoritative claim/execution admission route. |
| Q7 - Minimum product surface | `src/planning_lite/attempt_runtime.py`, at `claim_attempt`. |
| Q8 - Minimum test surface | `tests/test_attempt_runtime.py`, which owns preparation, canonical store codec, claim state and authorization behavior. |
| Q9 - Persistence migration | No. Keep `AttemptStoreV1`, `AttemptEnvelopeV1`, and `AttemptRecordV1` unchanged; resolve existing fields at claim. |
| Q10 - Existing persisted mismatch | Fail closed before replacement; raise the existing `AttemptAuthorizationError` path, leave the row and store bytes unchanged, and do not claim or rewrite it. |

The higher-level `execute_governed_operation` implementation resides in a pre-existing dirty worktree path and was read only. That unrelated edit is preserved and its bytes are included in the readiness evidence map. The Attempt Runtime, Authorization, and Attempt contract sources and focused test owner were clean at entry.

## Mandatory current-byte reproduction

Baseline: HEAD `43c7da88e904231da1bd8c5d63447331d6196e80`. The disposable target used normal `issue_preparation_authorization` and `prepare_attempt` for original scope `CHG-P05-ORIGINAL / T-P05-01`, producing `CHG-P05-ORIGINAL/T-P05-01/A1` in `ACTIVATABLE`. It then replaced both persisted `change_id` and `attempt_id` consistently with `CHG-P05-FOREIGN`, retained task `T-P05-01` and the original Authorization reference/document, encoded through `encode_attempt_store`, decoded through `decode_attempt_store`, and verified re-encoding was byte-identical. The foreign canonical store SHA-256 immediately before claim was `5dfa4216b5faff321a9e7316108b298ef07f52eabdf8ae3a384d1c037d4d995f`. The retained reference was the fixture-local `authz_e5fa52ff29b74ae62b3dc38986975394`; the Authorization resolves `AUTHORIZED` for the original scope and `WRONG_SCOPE` for the foreign Change scope.

```text
P05_REPRODUCED: YES
OBSERVED_CURRENT_RESULT: claim_attempt returned IN_FLIGHT; the foreign identity was persisted in IN_FLIGHT.
EXPECTED_SAFE_RESULT: AttemptAuthorizationError; remain ACTIVATABLE; no store-byte mutation.
CANONICAL_CODEC: ENCODE / DECODE / RE-ENCODE BYTE-IDENTICAL
FIXTURE: disposable target outside the repository; removed at context exit
```

This reproduces the audited nearest-wrong persisted state with current HEAD product bytes. It is a real detector-path reproduction, not a malformed-input codec test.

## Required correction semantics

The future implementation will, while holding the Attempt store mutation lock and after resolving the exact stored row, call the existing preparation authorization resolver using that row's retained `authorization_ref`, `change_id`, and `task_or_operation_id`. It must reject any non-`AUTHORIZED` result before constructing/persisting the `IN_FLIGHT` envelope. It must not rely on caller-supplied identity, presence of an authorization file, or preparation-time validation alone. It must not rewrite identity, widen scope, or mutate the store on mismatch. Matching valid attempts retain current claim behavior and error taxonomy. The canonical v1 codec and persisted format remain unchanged.

## Acceptance contract

- **A01_VALID_SCOPE:** normally prepared/persisted matching scope claims successfully.
- **A02_FOREIGN_CHANGE_SCOPE:** canonical foreign-Change row retaining original authorization is rejected.
- **A03_FOREIGN_TASK_SCOPE:** canonical task mismatch is rejected; task is independently in `PreparationScopeV1`.
- **A04_AUTHORIZATION_REF_EXISTS_BUT_SCOPE_MISMATCHES:** an existing retained ref does not imply applicability.
- **A05_CANONICAL_CODEC:** nearest-wrong row round-trips with the canonical store codec and reaches claim detection.
- **A06_NO_SILENT_REPAIR:** rejection leaves serialized row/store unchanged.
- **A07_VALID_STATE_REGRESSION:** existing valid claim/lifecycle behavior stays green.
- **A08_PREPARATION_VALIDATION_PRESERVED:** preparation still rejects wrong Change/task scope.
- **A09_P05_MUTANT_KILLED:** the exact reproduced P-05 mutation is rejected by production `claim_attempt`.
- **A10_NO_NEW_AUTHORITY:** use only the existing Authorization record/store/resolver and Attempt store.

## Ownership, non-goals and boundaries

Product owner: existing Attempt Runtime in `src/planning_lite/attempt_runtime.py`. Test owner: `tests/test_attempt_runtime.py`. Authorization record/storage remains owned by `src/planning_lite/authorization.py`; this Change adds no parallel authority.

Out of scope: implementing now; changing Authorization issuance; schema migration; new store, service, cache, signing, retry model, lifecycle state, or policy engine; changing Roadmap macro structure; the sequential whole-organism proof; and 09-G. This correction only removes the known P-05 blocker after a separately authorized implementation and adversarial rechallenge. The subsequent sequential proof requires owner adjudication; 09-G remains NOT STARTED.

## Evidence references

| Evidence | Path | Canonical-LF SHA-256 |
|---|---|---|
| Accepted P-05 survivor | `docs/design/project-spine/checkpoints/PLANNING-LITE-ORGANISM-VITALITY-AUDIT-v1.md` | `30357ebaa16438ca305dff7e1e373380432b297c92eac922d99135b060859089` |
| Prior Architecture MVP closeout | `docs/design/project-spine/checkpoints/PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-PRODUCT-COMMIT-AND-CLOSEOUT-v1.md` | `4ee775c6d4d5f67d3f142124ec1f04275bca6330d337a777c7f217e970b76960` |
| Attempt contract | `src/planning_lite/attempt_evaluation.py` | `1bffa40ce6a9db27a7ce2e0b39047ca1ae435b9a482da3b9cb25bf5c9cf5cf40` |
| Attempt Runtime and claim | `src/planning_lite/attempt_runtime.py` | `0bd6a209c67327523ae005c31b19c28a530c250c5e4fd508c7dbcceb4a650dfe` |
| Authorization scope/resolver | `src/planning_lite/authorization.py` | `5799e475a58004a45a5816f8a7870e2167beab12adf524756f9ed2e3629499fb` |
