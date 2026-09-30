# PL-V39-08 RunReceipt Measurement Correction Route B Pre-Implementation Candidate Disposition v1

Transition: OWNER_DECISION_CHANGE_3_ROUTE_B_PRE_IMPLEMENTATION_CANDIDATE_DISPOSITION  
Change ID: CHG-PL-V39-08-RUNRECEIPT-MEASUREMENT-CORRECTION-001  
Decision date: 2026-09-29

## Owner decision

OWNER_DECISION_SOURCE: EXPLICIT_HUMAN_OWNER  
OWNER_DECISION: ARCHIVE_PRESERVED_CANDIDATE_AND_RESTORE_CANONICAL_HEAD_BASELINE  
SALVAGE_DECISION: M14_LEGACY_COMPATIBILITY_TEST_HUNK / ARCHIVE_EXACT_HUNK / DEFER_REINTRODUCTION_TO_AUTHORIZED_T05 / DO_NOT_KEEP_LIVE_NOW

The owner selected full archival of the preserved candidate, restoration of all six candidate paths to canonical HEAD, and archival-only preservation of the standalone M14 compatibility test hunk. This transition did not implement Route B or perform Formal Readiness.

## Entry state

HEAD: 19217522f3dac695602a8534d7ddb8f9bbee5858  
ENTRY_AUTHORITY_STATE_ID: c1a95c97ffab6f1f892600f0fbfd0fd586c4ca3baaef0319cc2510c4d02fb30d  
ENTRY_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555  
ENTRY_UNRELATED_DIRT_STATE_ID: 2503939f0939840c39e22005260ae02d34621fe682c5c5ed810f2f9271ce348a  
ENTRY_SYNC_STATE_ID: 8479525b960c558379844fe81b0076984e1218ff8e1612b26277621c2f09c43a  
ENTRY_INDEX_EMPTY: YES  
ENTRY_CAPSULE: strict 12-field SYNC_CAPSULE_V1; canonical UTF-8 JSON, sorted keys, compact separators, one final LF; capsule hash excludes `semantic_projection` and `sync_state_id`.

The entry capsule and partition identifiers were reproduced exactly before archive creation. The unrelated-dirt partition remains unchanged.

## Historical candidate archive

ARCHIVE_ROOT: D:\documents\planning-lite-sync\CHANGE_3_ROUTE_B_PRE_IMPLEMENTATION_CANDIDATE_ARCHIVE_V1  
ARCHIVE_MANIFEST_PATH: D:\documents\planning-lite-sync\CHANGE_3_ROUTE_B_PRE_IMPLEMENTATION_CANDIDATE_ARCHIVE_V1\archive_manifest.json  
ARCHIVE_MANIFEST_SHA256: 96fcef0094cb0fb41a73f6d40d49f323f55f1c20ba2a79ce73ec4d9be79f1aff  
FULL_CANDIDATE_PATCH_SHA256: c6649bc64f83bdbaf850fe8f7492f5ed5bc4f5aec9fcfe0907a0f9560e119686  
M14_HUNK_SHA256: 9c1957d2df32557259b8c6195c5ffdd455d1b28a05b141dff3cac556ea442348  
M14_FUNCTION_SHA256: 9a4fc1ee2bc4995e0ae5fd8854b31871613d4fff5e0ffd7060e39714d3501111  
ARCHIVE_ARTIFACT_COUNT: 18

ARCHIVE_CONTAINS_ALL_SIX_RAW_FILES: YES  
ARCHIVE_PATCH_REPRESENTS_ENTRY_CANDIDATE: YES  
ARCHIVE_M14_EXACT_HUNK_CAPTURED: YES  
M14_STANDALONE_PATCH_APPLIES_TO_CANONICAL_HEAD: YES  
HISTORICAL_CANDIDATE_RECONSTRUCTABLE: YES  
ARCHIVE_MANIFEST_VERIFIED: YES

The archive contains the raw worktree bytes and SHA256 for each candidate path, canonical HEAD bytes and Git blob identities for all six paths, the binary-capable HEAD-to-candidate patch, the exact M14 function bytes, a standalone M14 unified patch, and the entry capsule and state record. It is external noncanonical evidence only.

## Canonical baseline restoration

PRESERVED_CANDIDATE_DISPOSITION: ARCHIVED_AND_REMOVED_FROM_ACTIVE_WORKTREE  
HISTORICAL_CANDIDATE_STATE_ID: 37a2f9e23578567528226c714631a4bd057221c041cdc709f948945513be0555  
CANDIDATE_PATH_COUNT_BEFORE: 6  
CANDIDATE_PATH_COUNT_AFTER: 0  
LIVE_CANDIDATE_PATHS: NONE  
PRODUCT_CANDIDATE_BYTES_RETAINED: NO  
ATTEMPT_SPECIFIC_TEST_BYTES_RETAINED: NO

All six paths compare clean to canonical HEAD under `git diff HEAD -- <six paths>`. Their Git-cleaned worktree object identities equal the corresponding HEAD blob IDs. Git's Windows checkout wrote CRLF bytes, so raw worktree SHA256 values are recorded separately from the canonical Git blob IDs:

| Path | WORKTREE_BYTE_SHA256 | HEAD_GIT_BLOB_OID | `git diff HEAD` |
|---|---|---|---|
| `src/planning_lite/telemetry.py` | `482933fedf1785aaedf7f8e89be47a5d70e0150ab909889a7a0eaa3e57e1c57b` | `73f8518522d3531b0a0502df2022d45b41ec76e9` | EMPTY |
| `scripts/capture_codex_run_receipts.py` | `381b3abbefafad26fdd074198832e21b3033ac6b8ef92a3e028c6f56b3d594ce` | `8351ebcf05b93753f1ec650249e1be5694eb475a` | EMPTY |
| `src/planning_lite/operation_lifecycle.py` | `8c70a2560a7052c3cc2b0eaa94b0e079f4371c83bcf4b71633e7ffe761219786` | `a6a71e6087d5e64b3ef1c866cdd6c922e210b1df` | EMPTY |
| `tests/test_run_receipts.py` | `21bb0b0ed2185b74f228a15dfa8f1560b900fc3846a648559608895a7164bae2` | `12c58efd671efe0ba0898dfd3487f89c4663153c` | EMPTY |
| `tests/test_codex_run_receipt_capture.py` | `a3e940ea2428c41a0dd2d269649d91d8fa10ebd7127c87dde7fc3acd1422572d` | `c0cfc3403a215133e68637cccafbfc8feb1840b6` | EMPTY |
| `tests/test_operation_lifecycle.py` | `735cbea47d195c51990941699550dc6d792d1f5ca6da2a062cf1615183809a15` | `405a639d0f6daedfe61657e4cad368e5d563cc92` | EMPTY |

The line-ending representation does not contain candidate hunks. Candidate path count after disposition means paths with a noncanonical Git diff; it is zero. Git status may show a worktree modification marker because the CRLF byte length differs from the LF index stat, while the normalized Git blob and diff are canonical.

ROUTE_B_BASELINE_ISOLATED: YES  
ROUTE_B_BASELINE_SOURCE: HEAD 19217522f3dac695602a8534d7ddb8f9bbee5858  
CANDIDATE_CONTAMINATION_REMAINING: NO  
OLD_CANDIDATE_BYTES_USED_AS_ROUTE_B_BASELINE: NO

## M14 disposition and lifecycle

M14_TEST: ARCHIVED_REUSABLE_HUNK  
M14_LIVE_WORKTREE: NO  
M14_ROUTE_B_STATUS: ELIGIBLE_FOR_REINTRODUCTION_DURING_AUTHORIZED_T05  
M14_AUTO_REINTRODUCTION_AUTHORIZED: NO

FORMAL_READINESS_BLOCKED_PENDING_CANDIDATE_DISPOSITION: NO  
FORMAL_READINESS_FOR_ROUTE_B: NOT YET PERFORMED  
IMPLEMENTATION_AUTHORIZED: NO  
FIELD_PROOF_AUTHORIZED: NO  
T00: PRESERVED / CONSUMED / NO REEXECUTION  
09_G_STARTED: NO  
INDEX_EMPTY: YES  
STAGE: NO  
COMMIT: NO  
PUSH: NO

The next single permitted gate is `RUN_CHANGE_3_PROVIDER_NEUTRAL_COARSE_MEASUREMENT_FORMAL_READINESS`. No Formal Readiness, Route B implementation, T-01..T-06 execution, T00 rerun, Roadmap edit, or 09-G work occurred in this transition.
