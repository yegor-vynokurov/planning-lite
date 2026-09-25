# PL-V39-09 Compact Semantic Operation Trace
## Implementation Plan Amendment v3

**Amendment purpose:** `MANAGED TEMPLATE INTEGRITY PATH-BUDGET CORRECTION`

This Amendment is cumulative over:

```text
Implementation Plan v1
+ Implementation Plan Amendment v1
+ Implementation Plan Amendment v2
+ Implementation Plan Amendment v3
```

Amendment v3 resolves the managed-template integrity path-budget finding from
the previous fresh Formal Readiness review. It introduces no new semantic or
integration decision.

## 2. Readiness finding adjudication

Materialize the blocked readiness result:

```text
PREVIOUS_FRESH_FORMAL_READINESS:
BLOCKED

ARCHITECTURE_BLOCKER_COUNT:
0

MATERIAL_FINDING_COUNT:
1

UNBOUND_MATERIAL_CHOICE_COUNT:
0

MATERIAL_FINDING:
Managed template integrity requires updating
template/.planning/framework/SHA256SUMS.txt
when template/.planning/changes/templates/progress.md changes.

FINDING_CLASS:
MANAGED_TEMPLATE_INTEGRITY_PATH_BUDGET

ARCHITECTURE_CHANGE_REQUIRED:
NO

DEFINITION_AMENDMENT_REQUIRED:
NO

NEW_AUTHORITY:
NO

NEW_STORE:
NO

NEW_OPERATION_IDENTITY:
NO
```

## 3. Supersede five-path surface

Amendment v2's five-path implementation surface is superseded only for
integrity maintenance.

The exact implementation surface becomes six paths:

```text
ADD:
src/planning_lite/operation_trace.py
tests/test_operation_trace.py

MODIFY:
src/planning_lite/operation_lifecycle.py
tests/test_operation_lifecycle.py
template/.planning/changes/templates/progress.md
template/.planning/framework/SHA256SUMS.txt
```

Record:

```text
FUTURE_IMPLEMENTATION_WRITE_PATH_COUNT:
6
```

No other path is added.

## 4. SHA256SUMS role

`template/.planning/framework/SHA256SUMS.txt` is:

```text
INTEGRITY_COMPANION_ONLY
```

It does not:

```text
own trace semantics
own persistence
own routing
own PL08 evidence
own Project Spine
own lifecycle
change Change 2 architecture
```

It is changed solely because the managed template:

`template/.planning/changes/templates/progress.md`

changes.

## 5. Exact checksum rule

During future implementation:

1. finalize the intended bytes of
   `template/.planning/changes/templates/progress.md`;

2. compute SHA-256 over the exact final template file bytes using the repository's
   existing SHA256SUMS convention;

3. replace only the existing checksum entry corresponding to:

```text
.planning/changes/templates/progress.md
```

inside:

`template/.planning/framework/SHA256SUMS.txt`;

4. preserve all unrelated checksum entries byte-semantically;

5. do not reorder unrelated entries;

6. verify the recorded checksum reproduces from the final progress template bytes.

Do not create a second checksum file.

Do not modify MANIFEST_V4.md because Formal Readiness verified:

```text
MANIFEST_UPDATE_REQUIRED:
NO
```

## 6. No semantic change

Everything approved in Amendment v2 remains unchanged:

```text
F01_LIVE_BINDING:
PRESERVED

F02_LIVE_BINDING:
PRESERVED

F03_POST_S6_BINDING:
PRESERVED

OPTIONAL_DURING_BINDING:
PRESERVED

PROGRESS_PATH_BINDING:
PRESERVED

MISSING_PROGRESS_POLICY:
PRESERVED

MARKER_GRAMMAR:
PRESERVED

PRE_PERSISTENCE:
PRESERVED

POST_ENRICHMENT:
PRESERVED

STALE_WRITE_PROTECTION:
PRESERVED

TRACE_NONAUTHORITY:
PRESERVED

OPERATION_TRACE_PURITY:
PRESERVED

LIFECYCLE_TRANSPORT_BOUNDARY:
PRESERVED

WALKING_SKELETON_A:
PRESERVED

WALKING_SKELETON_B:
PRESERVED

CHANGE3_SEPARATION:
PRESERVED
```

No new semantic or integration decision is introduced.

## 7. Revised exact read/write boundaries

Future Change 2 writable paths exactly:

```text
src/planning_lite/operation_trace.py
src/planning_lite/operation_lifecycle.py
tests/test_operation_trace.py
tests/test_operation_lifecycle.py
template/.planning/changes/templates/progress.md
template/.planning/framework/SHA256SUMS.txt
```

Remain read-only:

```text
src/planning_lite/cli.py
src/planning_lite/context.py
src/planning_lite/telemetry.py
src/planning_lite/attempt_evaluation.py
src/planning_lite/project_spine.py
src/planning_lite/traversability.py
```

No Change 3 path.

## 8. Verification addition

Future implementation verification must additionally prove:

```text
PROGRESS_TEMPLATE_SHA256:
exactly matches the corresponding SHA256SUMS entry

UNRELATED_SHA256SUMS_ENTRIES_CHANGED:
NO
```

A stale or incorrect managed-template checksum is implementation failure.

## 9. Change state

Preserve:

```text
CHANGE_2:
VALID / PAUSED_PENDING_FRESH_FORMAL_READINESS

IMPLEMENTATION_AUTHORIZED:
NO

LIFECYCLE_PREREQUISITE:
CLOSED / COMPLETE

CRITICAL_JOURNEY:
PASSING

CHANGE_3:
NOT_ABSORBED

MAJOR_PL09_NEXT_SLICE_GATE:
PRESERVED / UNCONSUMED
```

## 10. Next gate

After materialization:

```text
NEXT_SINGLE_GATE:
FRESH_FORMAL_READINESS_CHANGE_2_AFTER_AMENDMENT_V3
```

No implementation authorization is granted by this Amendment.

## 11. Materialization boundary

Allowed governance writes exactly:

```text
docs/design/project-spine/checkpoints/PL-V39-09-COMPACT-SEMANTIC-OPERATION-TRACE-IMPLEMENTATION-PLAN-AMENDMENT-v3.md
docs/design/project-spine/CURRENT.md
```

CURRENT receives only a bounded Change 2 projection:

```text
CHANGE_2:
VALID / PAUSED_PENDING_FRESH_FORMAL_READINESS

IMPLEMENTATION_AUTHORIZED:
NO

NEXT_PERMITTED_ACTION:
FRESH_FORMAL_READINESS_CHANGE_2_AFTER_AMENDMENT_V3
```

Do not clean unrelated CURRENT content.
