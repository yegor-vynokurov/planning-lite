# PL09 Governed Operation Lifecycle — Implementation Plan Amendment v1

```text
CHANGE_ID: CHG-PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-001
AMENDMENT_STATUS: APPROVED_BY_OWNER
OWNER_GATE: OWNER_AUTHORIZATION_PL09_GOVERNED_OPERATION_LIFECYCLE_REPAIR_V6_PLAN_AMENDMENT_MATERIALIZATION
OWNER_DECISION: APPROVE_REPAIR_V6_PLAN_AMENDMENT_MATERIALIZATION
PREDECESSOR_PLAN_PATH: docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-v1.md
PREDECESSOR_PLAN_SHA256: B38B977FD6858597380DD2DB7D7685E7272BC3881776A69370C4E615E671ABEC
SOURCE_REPAIR_V6_CANDIDATE_ORDINARY_SHA256: 08893DAE1303EA83602DECBED1BC5159C22B461FF5F3FDCFFAC8493E58A4FD13
SOURCE_REPAIR_V6_PASS_REVIEW_ORDINARY_SHA256: 894491F4F32DE693B17BF4156E7DAB085B54C1696614887614506EFC96377C80
SOURCE_REPAIR_V6_PASS_REVIEW_VERDICT: PASS_INDEPENDENT_CUMULATIVE_EXECUTABLE_CAPTURE_AND_SEAL_HANDOFF_REPAIR_V6
FORMAL_READINESS_V2: NOT_RUN
IMPLEMENTATION_AUTHORIZED: NO
REPOSITORY_BINDING_REPAIR_V6_1: APPROVED_BY_OWNER
SUPERSEDED_PLANNING_AUTHORITY_COMMIT: e0a7d5c12aa1056cd8ab4f955cf44295b94793be
```

This Amendment is a cumulative bounded delta over the immutable predecessor Plan v1.
It replaces only the entry/evidence contract identified in the reviewed Repair v6;
all predecessor Plan semantics not explicitly replaced by the canonical cumulative
amendment below remain in force. It does not authorize product implementation.

PLAN_AMENDMENT_BINDINGS_BEGIN
PLAN_AMENDMENT_STATUS: APPROVED_BY_OWNER
PREDECESSOR_PLAN_SHA256: B38B977FD6858597380DD2DB7D7685E7272BC3881776A69370C4E615E671ABEC
SOURCE_REPAIR_V6_CANDIDATE_PATH: .local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_ENTRY_BINDING_CUMULATIVE_EXECUTABLE_CAPTURE_AND_SEAL_HANDOFF_REPAIR_V6_CANDIDATE.md
SOURCE_REPAIR_V6_CANDIDATE_ORDINARY_SHA256: 08893DAE1303EA83602DECBED1BC5159C22B461FF5F3FDCFFAC8493E58A4FD13
SOURCE_REPAIR_V6_PASS_REVIEW_PATH: .local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_ENTRY_BINDING_CUMULATIVE_EXECUTABLE_CAPTURE_AND_SEAL_HANDOFF_REPAIR_V6_FRESH_INDEPENDENT_REVIEW.md
SOURCE_REPAIR_V6_PASS_REVIEW_ORDINARY_SHA256: 894491F4F32DE693B17BF4156E7DAB085B54C1696614887614506EFC96377C80
REPOSITORY_BINDING_REPAIR_V6_1: APPROVED_BY_OWNER
SUPERSEDED_PLANNING_AUTHORITY_COMMIT: e0a7d5c12aa1056cd8ab4f955cf44295b94793be
SUPERSEDED_PLANNING_AUTHORITY_PARENT: 407f4daef02227145a0c807ca182925c76888b60
AUTHORITY_IMPORT_PATH_COUNT: 13
CUMULATIVE_AMENDMENT_SHA256: 3FA47ED0208AF6F6F16F0613C2EDF79352258824BE2C46B9F0319FDEA8843485
ENTRY_CHECKER_SHA256: 77318AFF94BC675411D3838B5E3A24ABE49A95C0CA90C2F8B0E61BF1A6F45B61
PLAN_AMENDMENT_BINDINGS_END

CANONICAL_CUMULATIVE_AMENDMENT_BEGIN
## Effective basis

This Amendment is cumulative from the immutable predecessor Plan v1. Failed
repair candidates v1-v5 are lineage only and are not normative dependencies.
Every Plan v1 task, verification row, acceptance row, closure row, product path,
and architecture rule remains unchanged except the exact replacements below.

## Entry authority generation

The first v6 Planning Authority commit `e0a7d5c12aa1056cd8ab4f955cf44295b94793be` is preserved as historical
lineage but is superseded because the real repository revealed that the
predecessor Plan and twelve older authority checkpoint files existed on disk
but were not yet tracked in Git. No product or runtime semantics change.

Superseding Planning Authority commit `A2` is a one-parent commit whose parent
is exactly `e0a7d5c12aa1056cd8ab4f955cf44295b94793be` and which changes exactly these fifteen governance paths:

```text
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-CHANGE-DEFINITION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-ACTIVATION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-v2.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-DEFINITION-AMENDMENT-ACTIVATION-v2.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-CHANGE-DEFINITION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-ACTIVATION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-v2.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-EXECUTOR-CALLABLE-BINDING-DEFINITION-AMENDMENT-ACTIVATION-v2.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-IMPLEMENTATION-PLAN-AMENDMENT-v1.md
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-ENTRY-AUTHORITY-CHECK-v1.py
```

The first thirteen paths are an authority import: their existing worktree bytes
must match the already-approved SHA identities before staging. The final two
paths are this repaired Amendment and its tracked checker.

Renewed Formal Readiness v2 runs at `HEAD=A2`. Readiness commit `R` is a
one-parent commit whose parent is exactly `A2` and whose only changed path is:

```text
docs/design/project-spine/checkpoints/PL-V39-09-GOVERNED-OPERATION-LIFECYCLE-FORMAL-READINESS-VERDICT-v2.md
```

Implementation authorization is an explicit owner decision naming exact `R`.
No latest-history lookup may choose another R.

## Replacement V-01

Before T-01, run the tracked checker in `entry` mode with exact owner-approved
R and current HEAD. V-01 passes only when the R/A chain, predecessor Plan,
old 14 authority records, authority worktree bytes, empty index,
history-sensitive no-touch fence for all twelve planned paths, and clean
planned-path worktree all pass.

## Replacement T-01

T-01 is exactly one checker `capture` invocation. The checker, not PowerShell
or the agent, owns baseline truth construction.

```text
python ENTRY-AUTHORITY-CHECK-v1.py capture --authority-commit <R>
```

`capture` reruns the V-01 entry proof, reads the live Git status and all twelve
planned paths, writes the existing ignored baseline path using deterministic
UTF-8 JSON bytes, rereads those bytes, and returns one compact JSON value:

```text
ENTRY_SEAL_V1 = {
  schema_version: 1,
  implementation_authority_commit: <exact R>,
  entry_head: <exact HEAD>,
  t01_baseline_sha256: <SHA-256 of exact baseline bytes>
}
```

The supervising implementation operation retains this returned JSON value in
operation-local memory and supplies the exact value as `--entry-seal-json` to
V-25, T-12 and V-26. It is not reconstructed from repository files.

If the seal is lost, `capture` may simply be rerun. It will succeed only while
all planned paths are still clean. Once implementation has changed a planned
path, recapture fails closed automatically. No separate phase flag is needed.

The baseline top-level keys are exactly:

```text
schema_version
entry_head
entry_index_empty
implementation_authority_commit
authorized_paths
preexisting_dirty_paths
central_status_porcelain_v1
```

Each path record is exactly:

```text
{path, exists, kind, sha256, git_state, status_code}
```

## Replacement V-25

Run checker `boundary --entry-seal-json <ENTRY_SEAL_V1>`.
The checker verifies the raw baseline digest before parsing, replays the exact R
and sealed entry HEAD, requires empty index, rejects any current dirty path not
in the twelve planned paths or the sealed pre-existing dirty set, and requires
every sealed pre-existing dirty path record to remain byte/state identical.

The returned `mutation_audit` is authoritative V-25 evidence.

## Replacement T-12 schema

T-12 still writes only:

```text
.local/work/experiments/PL09_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION.json
```

Its exact top-level keys are:

```text
schema_version
entry_identity
authority_identity
task_receipts
verification_receipts
acceptance_result
closure_result
mutation_audit
change_boundaries
terminal
```

Exact identities:

```text
entry_identity = {
  head,
  index_empty,
  preexisting_dirty_path_count,
  t01_baseline_sha256
}

authority_identity = {
  predecessor_plan_sha256,
  plan_amendment_sha256,
  entry_checker_sha256,
  planning_authority_commit,
  readiness_sha256,
  implementation_authority_commit
}
```

`task_receipts[]` records are exactly `{task_id, status, evidence_ref}` and contain T-01..T-12 in numeric order. `verification_receipts[]` records are exactly `{verification_id, status, evidence_ref}` and contain V-01..V-26 in numeric order. Every status is `PASS`; each evidence ref is its own JSON pointer. Acceptance remains
52/52/0/0, closure remains 20/20/0/0 with 9 v2 overlays.

`mutation_audit` is copied exactly from checker `boundary` output.
`change_boundaries` remains:

```text
change_2 = BLOCKED / VALID / PAUSED
change_3 = NOT_ABSORBED
major_pl09_next_slice_gate = PRESERVED / UNCONSUMED
```

`terminal` is exactly:

```text
verdict = PASS_GOVERNED_OPERATION_LIFECYCLE_IMPLEMENTATION_EXECUTION
implementation = COMPLETE
formal_readiness_rerun_during_implementation = false
```

## Replacement V-26

Run checker `final --entry-seal-json <ENTRY_SEAL_V1> --execution <T-12 path>`.
`final` first runs the same sealed boundary proof, then validates the complete
T-12 schema and exact 12/26/52/20/9 terminal counts and identities.

## Unchanged remainder

T-02 through T-11 other than V-25 preflight, V-02 through V-24, all product
paths, all test nodes, PL08 carrier mapping, lifecycle order, status projection,
adoption proof, acceptance/closure mappings, Change 2/3 boundaries and the
major PL09 next-slice gate remain exactly as Plan v1 defines them.
CANONICAL_CUMULATIVE_AMENDMENT_END

## Materialization boundary

```text
CANONICAL_PLAN_V1_MUTATED: NO
CURRENT_MUTATED: NO
SOURCE_MUTATED: NO
TEST_MUTATED: NO
TEMPLATE_MUTATED: NO
IMPLEMENTATION_AUTHORIZED: NO
NEXT_GATE_AFTER_PRE_A_PASS: OWNER_AUTHORIZATION_PL09_GOVERNED_OPERATION_LIFECYCLE_PLANNING_AUTHORITY_COMMIT_A
```
