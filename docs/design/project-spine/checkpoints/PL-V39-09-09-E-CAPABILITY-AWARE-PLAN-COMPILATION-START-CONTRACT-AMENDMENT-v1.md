# PL-V39-09 09-E Capability-Aware Plan Compilation Start Contract Amendment v1

## Amendment identity and authority

```text
AMENDMENT_ID: PL-V39-09-09-E-SPLIT-HANDOFF-CORRECTION-001
AMENDMENT_KIND: START_CONTRACT_SEMANTIC_CORRECTION
AMENDMENT_STATUS: MATERIALIZED / OWNER_AUTHORED
PREDECESSOR:
docs/design/project-spine/checkpoints/PL-V39-09-09-E-CAPABILITY-AWARE-PLAN-COMPILATION-START-CONTRACT-v1.md
PREDECESSOR_SHA256: CE499ADAB98A6E0C416AB85BC6411DFD8B77C272242138B42D43415C677514E5
OWNER_DECISION: ACCEPT_E0_B2_SPLIT_HANDOFF_CORRECTION
```

This Amendment records the one material semantic correction identified by the
owner after `RUN_PL09_09_E_CAPABILITY_AWARE_PLAN_COMPILATION_FIELD_EXPERIMENT_E0`:

```text
09_E_FIELD_E0:
PASS_WITH_ONE_MATERIAL_SEMANTIC_CORRECTION_REQUIRED

09_E_OPEN_FINDING:
SPLIT_VS_EXISTING_HANDOFF_CONFLATION
```

The predecessor start contract remains in force except for the correction
below. The correction applies to the derived E0 experiment candidate only. It
does not edit, rewrite, or reinterpret the historical PL07 Plan.

## Corrected PL07 dependency and handoff semantics

The effective accepted PL07 Plan preserves this dependency graph:

```text
T-03 depends on T-02
T-04 depends on T-02
T-03 and T-04 may remain independent
T-05 depends on both T-03 and T-04
```

The E0 result must not create an artificial dependency or handoff:

```text
FORBIDDEN:
T-03 -> T-04
T-04 -> T-03
```

Typed handoffs are evaluated only on actual dependency edges:

```text
T-03 -> T-05
T-04 -> T-05
```

The distinction is mandatory:

```text
dependency edge != capability boundary
capability boundary != typed handoff
existing downstream input != new upstream/downstream dependency
```

An existing typed or structurally sufficient downstream input must not be
represented as a new dependency between two sibling tasks. Parallelism is part
of the accepted Plan semantics and must be preserved by compilation.

## E0-B2 correction method

The next read-only delta must:

1. re-evaluate the effective PL07 Plan around T-03, T-04, and T-05;
2. prove the exact dependency graph and preserved parallelism;
3. evaluate handoffs only on `T-03 -> T-05` and `T-04 -> T-05`;
4. evaluate a separate true split candidate using PL05-C T-02;
5. reject a split if any S1-S6 condition fails; and
6. verify that no goal, authority, write scope, dependency graph, owner gate,
   or runtime authority is invented.

The PL05-C candidate is:

```text
ORIGINAL_UNIT:
T-02 Home, effective policy, registry, and inspection

CANDIDATE_T-02A:
home / effective policy / registry core

CANDIDATE_T-02B:
read-only projects / inspect CLI adapter
```

This is an experiment candidate only. It does not amend the PL05-C Plan or
authorize implementation.

## Preserved authority boundary

```text
ORIGINAL_PLAN_GOAL_UNCHANGED: YES
AUTHORITY_UNCHANGED: YES
WRITE_SCOPE_NOT_BROADENED: YES
DEPENDENCY_GRAPH_EXTERNAL_TO_ORIGINAL_UNIT_UNCHANGED: YES
NEW_OWNER_GATE: NO
NEW_RUNTIME_AUTHORITY: NO
```

No product source, test, template, Roadmap, recommendation, consumer, or
historical Plan mutation is authorized by this Amendment. No 09-F AgentWorkPack
or 09-G orchestration work is authorized.

## Bounded current-state projection

```text
09_E_FIELD_E0:
PASS_WITH_ONE_MATERIAL_SEMANTIC_CORRECTION_REQUIRED

09_E_OPEN_FINDING:
SPLIT_VS_EXISTING_HANDOFF_CONFLATION

NEXT_PERMITTED_ACTION:
RUN_09_E_FIELD_EXPERIMENT_E0_B2_SPLIT_HANDOFF_CORRECTION
```

The single next gate after this materialization is:

```text
OWNER_REVIEW_09_E_E0_B2_AND_V1_FREEZE_DECISION
```
