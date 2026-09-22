# PL09 Authoritative Attempt Runtime Access — Formal Readiness Verdict

Status: `CANONICAL / FORMAL READINESS VERDICT`

Change: `CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001`

Gate: `FORMAL_READINESS_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS`

Executor: `GPT-5.6 Luna / Extra High`

## Verdict

`READY`

This is a formal implementation-readiness result only. It does not authorize implementation, source or test mutation, staging, commit, push, or downstream work. The next permitted gate is `OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_IMPLEMENTATION`.

## Authority and entry state

The reviewed authority chain is closed and internally bound:

| Authority | Path | SHA-256 |
| --- | --- | --- |
| Definition | `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-CHANGE-DEFINITION-v1.md` | `81514C1519BBDF97D2908B1F0EF2A73CAE19A76535D22923ED726C82A5C63DB1` |
| Definition activation | `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-DEFINITION-ACTIVATION-v1.md` | `0DE397A60FCE5E1ABB3257BD0F7DC3C66F5DEF851274033D2A1C14B8A5A7BB3D` |
| Canonical implementation plan | `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-IMPLEMENTATION-PLAN-v1.md` | `3347577BEB68AB907253C19706436B72D5EC1293F997F9D828990AF5F4CE42C6` |
| Plan approval/readiness entry | `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-PLAN-APPROVAL-READINESS-ENTRY-v1.md` | `5E37D074D82B593A3075F518F58DA90FD41D781A15A078720038840A8373A7DC` |
| Authorization closure | `docs/design/project-spine/checkpoints/PL-V39-09-AUTHORITATIVE-ATTEMPT-ACTION-AUTHORIZATION-CLOSURE-v1.md` | `B16025A7170BC7F14430989C3A203449B95A3432ABAEB7231831B59BD76E1E44` |

Entry checks:

- `HEAD`: `96b03dfce442d0ddfbc9329f7d8d4ead9e2cf600` — expected and unchanged.
- Index: empty; no staged paths.
- Existing working-tree dirt: preserved and not adjudicated as implementation work.
- Authorization prerequisite: `CLOSED`.
- Source mutations during this gate: `0`.
- Test mutations during this gate: `0`.

## Formal feasibility checks

| Check | Result | Evidence / conclusion |
| --- | --- | --- |
| Authorization capability compatibility | `PASS` | `authorization.py` already provides exact authorization-reference resolution, preparation applicability, recovery applicability, immutable target-local records, exact action and typed-scope validation, and explicit failure outcomes. |
| Authorization module mutation required | `NO` | The planned runtime can consume the existing resolver and applicability contracts without modifying `src/planning_lite/authorization.py`. |
| Attempt contract compatibility | `PASS` | Existing `AttemptRecordV1`, candidate/identity references, dirty-path entries, observed results, execution statuses, ordinal allocation, and corrective-attempt validation are reusable. |
| Attempt identity feasibility | `PASS` | The plan binds attempts to the existing typed candidate identity and lineage/corrective validation model. |
| Ordinal allocation feasibility | `PASS` | Existing `allocate_attempt_ordinal` supplies the planned monotonic allocation seam. |
| Preparation authorization binding | `PASS` | Preparation can resolve the supplied authorization reference against the exact preparation action and typed change/task scope. |
| Preparation single-use | `PASS` | The immutable target-local store and atomic claim design provide a feasible one-time preparation claim. |
| Recovery authorization binding | `PASS` | Recovery can resolve the supplied reference against the exact recovery action and typed attempt scope. |
| Recovery single-use | `PASS` | The same immutable authorization and atomic-claim boundary supports one-time interrupted-attempt resolution. |
| Store path feasibility | `PASS` | The effective policy resolves the target-local store under `<target>/<effective planning_root>/changes/active/.planning-lite/attempt-runtime.json`. |
| Store ownership/update safety | `PASS` | The path is under project-owned `.planning/changes/active/**`, which is protected by the ownership manifest and Copier skip rules; framework updates do not replace runtime records. |
| Canonical JSON feasibility | `PASS` | Existing canonical JSON and immutable publication conventions are sufficient for the planned runtime records. |
| Locking feasibility | `PASS` | Existing per-path locking supports thread/process coordination on Windows and POSIX. |
| Safe replacement feasibility | `PASS` | Same-directory temporary materialization, flush/fsync, validation, replacement, reread, and hash verification are implementable with current standard-library primitives. |
| Windows safe replacement | `PASS` | The existing Windows locking path and same-directory replacement approach are compatible with the planned protocol. |
| POSIX safe replacement | `PASS` | The existing POSIX locking path and directory-fsync helper are compatible with the planned protocol. |
| Atomic-claim test feasibility | `PASS` | Existing multiprocessing spawn/process/queue test infrastructure can exercise concurrent claim races. |
| Abrupt-loss test feasibility | `PASS` | Existing multiprocessing and subprocess patterns can exercise process loss and recovery without new infrastructure. |
| Preparation CLI adapter | `PASS` | `cli.py` already has the authorization command-adapter shape and argparse subparser surface; a thin preparation adapter can delegate to runtime logic. |
| Recovery CLI adapter | `PASS` | The existing CLI structure supports a thin interrupted-attempt recovery adapter without a parser or command architecture rewrite. |
| VS Code/chat/agent operator model | `PASS` | The planned adapters accept authorization references and runtime inputs as bounded command arguments; no owner manual JSON editing or manual command choreography is required. |
| Manual CLI typing required from owner | `NO` | Owner authorization is a prerequisite artifact; implementation runtime invocation is the executor's bounded adapter responsibility. |
| Owner manual JSON required | `NO` | Runtime state is produced and updated by the implementation through the target-local store protocol. |
| CLI thinness | `PASS` | State, authorization, locking, replacement, and recovery logic can remain in the runtime module while `cli.py` delegates. |
| Bounded traversability test | `PASS` | The existing system-traversability seam and next-broken-seam assertions can be extended at the planned adapter/runtime boundary. |
| Next broken seam preservable | `PASS` | The plan requires the first bounded failure to remain observable and does not require executor, lifecycle, or Change-2 behavior. |
| Executor dependency | `NO` | No executor implementation or registration is required by the plan. |
| Run-receipt dependency | `NO` | Run-receipt infrastructure is not required for the runtime access seam. |
| Lifecycle dependency | `NO` | Governed operation lifecycle changes are outside this change boundary. |
| Change-2 dependency | `NO` | No downstream Change-2 artifact or behavior is required. |
| PL08 boundary feasibility | `PASS` | The planned runtime consumes the closed authorization boundary and does not broaden it. |
| Package discovery | `PASS` | `pyproject.toml` discovers `src/planning_lite` through Hatch's configured wheel package path. |
| Test discovery | `PASS` | `pyproject.toml` uses `tests` as pytest's test path; the planned `tests/test_attempt_runtime.py` is auto-discoverable. |
| Hidden required tracked paths | `0` | No additional source, test, package, template, ownership, fixture, registry, or metadata path is required by the plan. |
| Planned-path worktree conflicts | `0` | The planned add/modify paths are currently absent or clean: `src/planning_lite/attempt_runtime.py` ADD, `src/planning_lite/cli.py` MODIFY, `tests/test_attempt_runtime.py` ADD, `tests/test_cli.py` MODIFY, `tests/test_system_traversability.py` MODIFY. |
| Uncommitted canonical governance compatibility | `YES` | The existing uncommitted governance artifacts are preserved; none is a source/test implementation conflict. |
| Unbound architecture choices | `0` | No unbound architecture choice blocks implementation. |
| Unbound material implementation choices | `0` | Remaining choices are private naming/mechanical details within the frozen plan. |
| False-readiness resistance | `PASS` | No sixth path, authorization mutation, new dependency, ownership change, registry/UI change, executor/lifecycle dependency, or manual owner JSON step is hidden behind the readiness claim. |

## Frozen-plan coverage

- Verification obligations: `24/24` feasible (`V1`–`V24`).
- Acceptance criteria: `22/22` implementable (`AC1`–`AC22`).
- Closure criteria: `11/11` closable if implementation satisfies the plan (`CC1`–`CC11`).
- Implementation tasks: `9/9` executable as bounded tasks.
- Acceptance/closure traceability: present in the canonical plan and consistent with the reviewed contracts.
- Verification execution: executable after implementation; this readiness gate does not claim implementation tests passed.
- Central completion checks: feasible, including `uv sync`, `uv run pytest`, clean temporary adoption, and `planning-lite doctor` in the adopted project.
- Clean adoption: feasible with current package/template structure.
- Doctor: feasible with current CLI and project-policy architecture.
- Coding-quality guidance: feasible without a new tooling or dependency path.

## Path and mutation boundary

The only artifact created by this gate is this verdict. No source file, test file, Definition, Activation, canonical Plan, approval entry, authorization record, or `CURRENT.md` was modified by this gate. No path was staged, committed, pushed, or handed to downstream execution.

The expected implementation boundary remains exactly five paths:

| Path | Planned state |
| --- | --- |
| `src/planning_lite/attempt_runtime.py` | `ADD` |
| `src/planning_lite/cli.py` | `MODIFY` |
| `tests/test_attempt_runtime.py` | `ADD` |
| `tests/test_cli.py` | `MODIFY` |
| `tests/test_system_traversability.py` | `MODIFY` |

No sixth path is required for package discovery, pytest discovery, ownership metadata, Copier behavior, project policy, fixtures, registries, UI integration, or release metadata.

## State transition and next gate

`DEFINITION_APPROVED / PLAN_APPROVED / FORMAL_READINESS_READY / IMPLEMENTATION_NOT_AUTHORIZED`

The next permitted action is owner authorization for implementation. Until that gate is separately passed, implementation remains prohibited.

## Terminal receipt

```text
FORMAL_READINESS_VERDICT: READY
CHANGE_ID: CHG-PL-V39-09-AUTHORITATIVE-ATTEMPT-RUNTIME-ACCESS-001
GATE: FORMAL_READINESS_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS
HEAD: 96b03dfce442d0ddfbc9329f7d8d4ead9e2cf600
DEFINITION_SHA256: 81514C1519BBDF97D2908B1F0EF2A73CAE19A76535D22923ED726C82A5C63DB1
ACTIVATION_SHA256: 0DE397A60FCE5E1ABB3257BD0F7DC3C66F5DEF851274033D2A1C14B8A5A7BB3D
PLAN_SHA256: 3347577BEB68AB907253C19706436B72D5EC1293F997F9D828990AF5F4CE42C6
PLAN_APPROVAL_READINESS_ENTRY_SHA256: 5E37D074D82B593A3075F518F58DA90FD41D781A15A078720038840A8373A7DC
AUTHORIZATION_CLOSURE_SHA256: B16025A7170BC7F14430989C3A203449B95A3432ABAEB7231831B59BD76E1E44
FORMAL_READINESS_ARTIFACT_SHA256: REPORTED_EXTERNALLY_AFTER_FINAL_BYTE_VERIFICATION
SOURCE_MUTATIONS: 0
TEST_MUTATIONS: 0
HIDDEN_REQUIRED_PATH_COUNT: 0
PLANNED_PATH_WORKTREE_CONFLICT_COUNT: 0
STAGED_PATHS: 0
COMMIT: NO
PUSH: NO
NEXT_GATE: OWNER_AUTHORIZATION_PL09_AUTHORITATIVE_ATTEMPT_RUNTIME_ACCESS_IMPLEMENTATION
```

## Result digest

The implementation boundary is feasible against the current committed architecture. The existing authorization resolver already provides the exact action, typed scope, target-local store, and immutable-record capabilities required by the plan. The existing attempt-evaluation contracts provide identity, ordinals, lineage validation, and observed-result compatibility. The target-local runtime store is project-owned and update-safe under the current Copier and ownership rules. Standard-library locking and safe-replacement primitives support the Windows and POSIX protocol. The five planned paths are discoverable and have zero current worktree conflicts. Atomic-claim and abrupt-loss tests can use existing multiprocessing infrastructure. The CLI can remain a thin adapter over a new runtime module. No executor, run-receipt, lifecycle, Change-2, dependency, registry, UI, or owner-manual-JSON work is required. Therefore the change is formally ready for a separate owner-authorization gate, while implementation remains unauthorized.
