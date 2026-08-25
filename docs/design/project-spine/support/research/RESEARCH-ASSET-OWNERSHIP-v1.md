# Research Asset Ownership v1

**Status:** current design contract
**Date:** 2026-08-18

This document prevents the three Planning Lite-related repositories/workspaces from drifting into duplicate responsibilities.

---

# 1. Ownership map

| Asset | Role | Product dependency? | Current disposition |
|---|---|---:|---|
| `planning-lite` | product/runtime/template | yes | active central product |
| `planning-lite-lab` | research/evidence/governance | no | preserve; reactivate at PL-V38-06A |
| `planning_lite_tools/step-16.4.1` | Context Pilot/Eval Harness reference | no | preserve; qualify at PL-V38-06A |
| older `planning_lite_tools` versions | provenance/lineage | no | preserve until lineage receipt; then archive where safe |
| Poker | real consumer/fixture source | no | source evidence only |
| Campaign Core | repeated-evidence governor | optional product capability | reuse only when repeated runs are justified |

---

# 2. `planning-lite-lab`

Retain.

It owns research-facing capabilities such as:

```text
artifact/source identity
hash/provenance receipts
fixture qualification
checkpointing
archive/relocation governance
experiment evidence
```

The root `state/CURRENT_STATE.md` in the reviewed archive is stale.
The later checkpoint is authoritative for reactivation:

```text
checkpoints/2026-08-14-r3-closeout-budget-admission-validated/
```

That checkpoint records R3 as complete and terminal at sequence 13 with 3/3 valid production-independent attempts and no new Campaign authorized.

No new v3.8 experiment may resume from the stale sequence-11 root state.

---

# 3. `planning_lite_tools`

Retain for now.

Current reference candidate:

```text
step-16.4.1/planning-lite-context-pilot-0.1.1-step-16.4.1
```

Recorded validation includes:

```text
routing vs resolution vs safe-deferral semantics
36/36 routing success on immutable evidence reclassification
routing-policy-ready verdict
least-privilege targeted fallback
file-access observation
balanced suite/report infrastructure
124 tests in the recorded validation
```

Do not assume every older version remains operationally necessary.
Do not delete them before recursive lineage qualification.

Expected later housekeeping:

```text
old versions
→ manifest/dependency review
→ archive-safe versions moved under governed Lab archive
→ current qualified reference remains easy to find
```

---

# 4. Non-duplication rules

Do not:

```text
rebuild Lab provenance mechanisms inside central Planning Lite
rebuild the entire Eval Harness for PL-V38-07
ship Lab or tools trees into consumer repositories
make central runtime import code from D:\documents\planning-lite-lab
make central runtime import code from D:\documents\planning_lite_tools
use completed R3 as a mutable campaign
preserve all old tools versions as active forever without review
```

Reuse means:

```text
qualified concepts/code/eval machinery at the research boundary
```

not:

```text
filesystem coupling between production and research workspaces
```
