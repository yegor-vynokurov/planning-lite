# Change Definition Amendment v3

## Derived Unit and Candidate-Correction Contract

OPERATION: MATERIALIZE_09_E_CANDIDATE_CORRECTION_CONTRACT_AND_RUN_FORMAL_READINESS_V3
CHANGE: CHG-PL-V39-09-E-READONLY-EXECUTOR-PLAN-COMPILER-001
AMENDMENT: DEFINITION_AMENDMENT_V3
STATUS: OWNER-REVIEWED / CORRECTIVE CONTRACT BOUND
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO
PRODUCT_IMPLEMENTATION_PERFORMED: NO

This amendment is a bounded corrective contract for the implementation
candidate. It binds the candidate corrections identified by the fresh v3
readiness evaluation without changing the approved product scope, compiler
architecture, task-table grammar, ownership boundary, or implementation
authorization. It is governance authority only; it does not claim that the
candidate has already been corrected.

### Scope, architecture, and path boundary

SCOPE_CHANGE: NO
ARCHITECTURE_CHANGE: NO
TASK_GRAMMAR_CHANGE: NO
READINESS_STATE_CHANGE: NO
OWNERSHIP_BOUNDARY_CHANGE: NO
IMPLEMENTATION_PATH_BUDGET_CHANGE: NO
PRODUCT_IMPLEMENTATION_AUTHORIZED: NO

The implementation candidate remains bounded to these six paths:

src/planning_lite/plan_compilation.py
tests/test_plan_compilation.py
src/planning_lite/cli.py
tests/test_cli.py
template/.planning/changes/templates/tasks.md
template/.planning/framework/SHA256SUMS.txt

The corrective product work is expected only in the four product paths:
src/planning_lite/plan_compilation.py, tests/test_plan_compilation.py,
src/planning_lite/cli.py, and tests/test_cli.py. The two template and
integrity paths remain byte-identical unless a fresh readiness evaluation
proves a necessary, separately bounded change. No seventh product path,
helper package, migration, generated target, recommendation/inbox file, or
roadmap file is authorized by this amendment.

## A. DerivedUnitV1 exact schema

Every derived unit must be a DerivedUnitV1 object with exactly these object
keys, with no missing key and no extra key, in the canonical semantic order
shown here:

unit_id
outcome
work_capabilities
cross_cutting_tags
target_executor_profile
already_decided
allowed_executor_decisions
forbidden_executor_decisions
criterion_assertions
material_findings

The schema and compiler validation requirements are:

1. unit_id is a nonempty string, unique within the proposal, and does not
   collide with any original task ID, parent unit ID, or other derived unit ID.
2. outcome is a nonempty string describing the distinct bounded outcome of
   this derived unit.
3. work_capabilities, cross_cutting_tags, already_decided,
   allowed_executor_decisions, forbidden_executor_decisions,
   criterion_assertions, and material_findings are arrays of the exact
   expected element shape. They are never silently coerced from scalars,
   objects, null, or other types.
4. Every capability and tag is a valid value from the existing authoritative
   capability and cross-cutting-tag vocabularies. Every
   target_executor_profile is a valid existing executor profile.
5. allowed_executor_decisions and forbidden_executor_decisions contain
   valid decision objects from the existing decision vocabulary. Their
   intersection must be empty after canonical identity comparison.
6. criterion_assertions must contain the complete C01-C13 assertion set,
   with the existing criterion identity, disposition, and assertion shape.
   Missing, duplicated, unknown, malformed, or non-PASS assertions are
   structural non-readiness conditions according to the effective contract.
7. material_findings preserves all material findings attached to the parent
   and adds findings local to the derived unit. Parent material findings are
   never discarded when a parent is split.
8. A derived compiled unit uses its own outcome, capabilities, tags,
   executor profile, decisions, assertions, and findings. It does not inherit
   the parent object wholesale, and the compiler must not replace its own
   fields with the parent's fields by default.
9. The parent capability union across all derived units must equal the exact
   parent capability set. The parent tag union across all derived units must
   equal the exact parent tag set. A capability or tag may occur in more than
   one derived unit when the bounded work requires it; duplicates across
   derived units are permitted and are not deduplicated into a different
   semantic unit.
10. Each derived unit must have a distinct outcome and a distinct bounded
    responsibility. An implementation may not create multiple IDs that are
    merely aliases for one parent outcome.

## B. Internal typed edge and handoff contract

The internal typed handoff set is an exact representation of the new internal
dependency edges introduced by the split:

INTERNAL_TYPED_HANDOFF_IDENTITIES == NEW_INTERNAL_EDGE_IDENTITIES

For every new internal edge there is exactly one matching typed handoff with
the same source and target unit identities and the required handoff type.
For every internal typed handoff there is exactly one matching new internal
edge. Opposite-direction handoffs, source or target identities outside the
derived-unit set, duplicate handoff identities, and handoffs without an edge
are invalid. An edge without its matching handoff is invalid.

The existing material findings remain the canonical failure vocabulary:

HANDOFF_EDGE_MISMATCH
MISSING_REQUIRED_HANDOFF
INVALID_HANDOFF

These checks are applied to the complete internal edge/handoff relation, not
only to the first edge or first handoff encountered. A plan cannot become
ready by retaining a reverse handoff, by omitting an edge, or by placing a
handoff outside the derived-unit list.

## C. S1-S6 decision assertions

Each derived unit must contain exactly one assertion for each of S1, S2, S3,
S4, S5, and S6 in already_decided:

S1: exactly one
S2: exactly one
S3: exactly one
S4: exactly one
S5: exactly one
S6: exactly one

Duplicate assertions for one S identity are invalid schema, including
contradictory duplicates. Missing assertions are invalid. N/A is not a
valid substitute for a required S1-S6 assertion. A verdict other than PASS
is structurally not ready. A later PASS assertion cannot mask an earlier
FAIL, duplicate, or otherwise invalid assertion; evaluation preserves the
first broken assertion and does not collapse assertions through a last-write-
wins map.

## D. Proposal schema error classification

The proposal validator must classify malformed proposal data as a bounded
PlanCompilationInputError with code PROPOSAL_SCHEMA_INVALID. It must not
leak TypeError, KeyError, an unhandled enum conversion error, or a
traceback for malformed input. This classification applies to all of the
following:

- any non-string element in capabilities, tags, allowed decisions, or
  forbidden decisions;
- any unknown capability, unknown tag, unknown executor profile, or unknown
  decision disposition;
- any invalid DerivedUnitV1 exact object shape, including missing or extra
  keys, invalid field types, invalid nested element shape, or invalid
  criterion assertion shape;
- any duplicate S1-S6 assertion, including a contradictory duplicate.

The CLI maps PROPOSAL_SCHEMA_INVALID to exit code 2 with the existing
canonical structured JSON error rendering. The compiler remains pure and the
JSON loader remains responsible only for duplicate-key rejection and input
decoding. Schema classification does not add a new runtime, persistence, or
authority subsystem.

## E. Structural non-readiness and exit behavior

Structurally unacceptable plans remain normal non-ready results. They are not
input-schema errors merely because they fail graph, split, handoff, coverage,
or readiness invariants. The existing structured non-ready result and CLI exit
code 3 remain authoritative for those cases. Only malformed proposal data
covered by section D uses PlanCompilationInputError and exit code 2.

The readiness projection continues to distinguish READY,
READY_WITH_CONTROLLED_DISCOVERY, and NOT_READY according to the effective
base Definition and prior amendments. A proposal cannot override a material
finding by supplying a later PASS or a second decision envelope.

## F. Canonical dependency ordering

When a task table contains multiple blocking edges, the compiler canonicalizes
the edge order by task-table row order. This applies to both:

OriginalTaskUnitV1.blocking_edges
OriginalTaskGraphV1.edges

Reversing the textual order of otherwise identical dependency declarations
must produce the same canonical edge sequence, graph identity, findings, and
result JSON. The row-order key is derived from the canonical task table, not
from input dictionary insertion order or incidental JSON serialization order.

## Corrective acceptance boundary

The implementation is correct only when the effective Definition base plus
Amendments v1, v2, and this v3 contract is reflected in the four permitted
product paths and the required C01-C16 tests in the existing test paths. The
template and checksum paths must remain byte-identical for this correction
unless a fresh readiness receipt proves a necessary change. This amendment
does not authorize implementation, staging, commit, push, or owner approval.

MATERIAL_IMPLEMENTATION_FINDINGS: 6
CORRECTIVE_CONTRACT: BOUND
NEXT_GATE: OWNER_REVIEW_09_E_CORRECTIVE_FORMAL_READINESS_V3
