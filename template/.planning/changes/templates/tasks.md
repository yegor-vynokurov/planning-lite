# Tasks

This file is authoritative for task status. Prefer end-to-end tracer bullets; use expand-contract for broad migrations.

| ID | Outcome | Slice type | Blocking edge | Verification seam / command | Blast radius | Status |
|---|---|---|---|---|---|---|
| `T-01` | | `Tracer bullet / Expand-contract` | `None` | | | `Pending` |

Allowed status values: `Pending`, `In progress`, `Blocked`, `Done`, `Cancelled`.

The `Blocking edge` cell accepts only `None`, one task ID such as `T-01`, or
comma-separated task IDs such as `T-01, T-02`. Prose, ranges, slash syntax,
and plus syntax are not valid Blocking edge values.
