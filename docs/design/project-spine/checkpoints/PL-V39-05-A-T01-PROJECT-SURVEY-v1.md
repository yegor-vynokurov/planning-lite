# PLANNING LITE / PL-V39-05-A / T-01 PROJECT SURVEY v1

**Document ID:** `PL-V39-05-A-T01-PROJECT-SURVEY-001`
**Date:** `2026-08-27`
**Change:** `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001`
**Task:** `T-01`
**Task verdict:** `COMPLETED`
**Implementation authorization:** `YES`
**Push authorization:** `NO`

## Product increment

Added:

```text
template/.planning/assessments/PROJECT_SURVEY_TEMPLATE.md
```

Modified:

```text
template/.planning/control/CURRENT_CAPABILITY_ASSESSMENT.md
```

## Result

Project Survey is now a bounded optional AS-IS evidence artifact.

Its invocation is owned by `PW-DIR-004 CURRENT_CAPABILITY_ASSESSMENT` and requires
all three conditions:

```text
material brownfield/current-state work
AND
assessment depends on repository/runtime structure
AND
existing current evidence is not sufficiently bounded/fresh
```

Routine/small work may bypass Survey.

Survey explicitly does not become a second owner of Current State, Capability
Assessment, Capability Model, Gap Map, Target State, or Roadmap.

Freshness is bound to:

```text
reflects revision
survey scope
evidence sources
```

and refresh/narrowing occurs only on material drift or scope escape.

## Ownership

No ownership edit was required:

```text
managed:
.planning/assessments/*_TEMPLATE.md

project_owned:
.planning/assessments/current/**
```

## Expected transient integrity state

`MANIFEST_V4.md` and `SHA256SUMS.txt` are intentionally not updated in T-01.

Per the approved Plan, integrity reconciliation belongs to T-03 after T-01 and
T-02 semantics stabilize.

The only expected template-tree delta before T-03 is:

```text
.planning/assessments/PROJECT_SURVEY_TEMPLATE.md
```

## Verification

- exact T-01 product write boundary: PASS
- Survey semantic contract assertions: PASS
- `tests/test_current_capability_gap_foundation.py`: PASS
- central resume contract: PASS
- `git diff --check`: PASS

## Next permitted task

```text
T-02 — bounded Clarification Sweep semantics
```
