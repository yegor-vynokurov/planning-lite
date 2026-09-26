# Implementation Plan Amendment v2

## Corrective implementation contract

OPERATION: MATERIALIZE_09_E_CANDIDATE_CORRECTION_CONTRACT_AND_RUN_FORMAL_READINESS_V3
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
AMENDMENT: IMPLEMENTATION_PLAN_AMENDMENT_V2
STATUS: OWNER-REVIEWED / CORRECTIVE CONTRACT BOUND
IMPLEMENTATION_AUTHORIZED: NO

This amendment binds the correction work for the existing implementation
candidate. It is an implementation plan, not an implementation receipt. No
product path is changed or authorized by materializing this document.

## 1. Fixed path budget and correction surface

The effective implementation surface remains exactly these six paths:

src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
src/planning_lite/cli.py
tests/test_cli.py
template/.planning/changes/templates/tasks.md
template/.planning/framework/SHA256SUMS.txt

The correction is expected only in these four product paths:

src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
src/planning_lite/cli.py
tests/test_cli.py

template/.planning/changes/templates/tasks.md and
template/.planning/framework/SHA256SUMS.txt remain byte-identical to the
current candidate unless a fresh readiness evaluation establishes a necessary
template or integrity change. No additional source, test, template,
documentation, migration, generated-project, recommendation/inbox, or
roadmap path may be added to the implementation candidate.

## 2. Required corrective behavior

The implementation must satisfy the Definition Amendment v3 contract while
retaining all previously approved behavior:

- parse and validate the exact DerivedUnitV1 schema;
- validate distinct derived outcomes and own derived capability, tag,
  executor-profile, decision-envelope, assertion, and finding fields;
- prove exact parent capability and tag unions without disallowing legitimate
  duplicate use across derived units;
- compare the complete internal edge set with the complete typed handoff set;
- reject reverse, missing, duplicate, or outside handoffs with the existing
  bounded findings;
- preserve all six S1-S6 assertions exactly once and prevent later PASS values
  from masking earlier failure or duplicate assertions;
- classify malformed proposal schema as PlanCompilationInputError with
  PROPOSAL_SCHEMA_INVALID, exit code 2, and bounded canonical JSON;
- retain structural non-ready plans as exit code 3;
- canonicalize multiple blocking edges by task-table row order for both the
  original task unit and original task graph;
- preserve the pure compiler core, thin CLI seam, path containment, canonical
  JSON, and existing result/exit mappings.

## 3. Required tests C01-C16

The following tests are required in the existing test paths. The names may use
the repository's established naming convention, but each contract must have a
direct owner test and no seventh test path may be introduced.

C01: derived units have distinct outcomes
C02: derived units have distinct capability signatures
C03: derived units have distinct executor profiles and decision envelopes
C04: derived capability union equals the parent capability set exactly
C05: derived tag union equals the parent tag set exactly
C06: an edge A->B with a handoff B->A cannot reach READY
C07: every internal edge has exactly one matching typed handoff
C08: a typed handoff without a matching internal edge is rejected
C09: duplicate contradictory S1 cannot be masked by a later PASS
C10: allowed decisions containing [{}] produce bounded schema error, not TypeError
C11: forbidden decisions containing [{}] produce bounded schema error
C12: unknown capability maps through the CLI to exit code 2
C13: unknown tag maps through the CLI to exit code 2
C14: unknown executor profile maps through the CLI to exit code 2
C15: unknown decision disposition maps through the CLI to exit code 2
C16: reversed textual multi-edge order is canonicalized by task-table row order

All prior Definition, Amendment, regression, controlled-discovery, path,
status, and readiness tests remain in force. Tests must assert the owning
data structure or canonical result, not presentation-only help text or
human-oriented rendering.

## 4. Sequencing and stop conditions

The correction is sequenced as one bounded product change:

1. implement the input schema and bounded error classification in the pure
   compiler;
2. implement derived-unit identity, own-field, union, assertion, and
   handoff/edge validation;
3. canonicalize original dependency ordering and preserve deterministic
   result rendering;
4. keep the CLI adapter thin and map schema errors to exit 2 and structural
   non-readiness to exit 3;
5. add or amend only the required tests in tests/test_plan_compilation.py
   and tests/test_cli.py;
6. verify the six-path boundary and byte identity of the two template/integrity
   paths before any implementation candidate review.

Stop the correction and return to owner review if any additional product path
is required, if a template/integrity change becomes necessary, if compiler
purity or path containment changes, if the exact schema cannot be enforced,
or if an existing material finding is weakened or renamed without a separate
approved amendment.

## 5. Acceptance and authority boundary

Acceptance requires C01-C16, retained regression coverage, exact six-path
accounting, bounded schema/non-ready exit behavior, deterministic canonical
ordering, and a fresh readiness receipt against the effective Definition and
Plan. A passing test run alone does not authorize product execution or owner
approval.

EXPECTED_PRODUCT_CORRECTION_PATH_COUNT: 4
STRICTLY_REQUIRED_ADDITIONAL_PATHS: []
TEMPLATE_PATHS_MUST_REMAIN_BYTE_IDENTICAL: YES
NEW_RUNTIME_OR_AUTHORITY_SUBSYSTEM: NO
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
NEXT_GATE: OWNER_REVIEW_09_E_CORRECTIVE_FORMAL_READINESS_V3
