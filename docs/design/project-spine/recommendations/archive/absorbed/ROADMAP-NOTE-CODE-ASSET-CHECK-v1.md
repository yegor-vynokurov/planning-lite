# ROADMAP NOTE — Reusable Code / Research Asset Check

**Date:** 2026-08-20
**Status:** proposed lightweight operating note; not a new Roadmap stage
**Recommended location:** `docs/design/project-spine/ROADMAP-NOTE-CODE-ASSET-CHECK-v1.md`

## Observation

The current Planning Lite Roadmap already preserves and schedules later qualification
of:

```text
planning-lite-lab
planning_lite_tools / step-16.4.1
legacy CODE-PL-ROADMAP / code-companion material
```

However, it does not currently state a small recurring rule such as:

> Before designing a new mechanism, checklist, metric, harness, or workflow helper,
> briefly inspect the current code/research asset stash for an existing reusable seed.

Useful material can therefore be remembered only at a dedicated later reactivation
stage, after a new design has already been invented.

## Proposed lightweight Roadmap rule

Insert near the beginning of the operating principles, before the per-stage sequence:

```text
REUSABLE ASSET CHECK

Before designing a non-trivial new mechanism, checklist, metric, prompt, evaluator,
or harness component:

1. Check the current Planning Lite code companion / code stash.
2. Check relevant active planning-lite-lab recommendations/research assets.
3. Check the currently qualified planning_lite_tools reference candidate when relevant.
4. Classify any match:
   REUSE
   ADAPT
   REFERENCE_ONLY
   NO_MATCH
5. Prefer reuse/adaptation when semantics and provenance are adequate.
6. Do not copy an old asset wholesale merely because it exists.
7. Do not block small routine bugfix/docs work on this check.
8. Record the result only when it materially affects the design.

This is a short read-only discovery step, not a lifecycle gate.
```

## Immediate application

Before productizing the Materiality/Simplicity checklist or Change Cost metrics, inspect
at minimum:

```text
.planning-lab/recommendations/active/CODE-PL-ROADMAP-v3.4.ru.md
.planning-lab/recommendations/active/REC-PL-RULE-PLAYBOOK-CURATION.ru.md
.planning-lab/recommendations/active/REC-PL-CONTROLLED-EVOLUTION.ru.md
planning_lite_tools/step-16.4.1/
```

The purpose is to discover existing prompts, validators, receipts, budget/stop
machinery, or metric patterns that can be adapted instead of rebuilt.

## Why this is separate from PL-V38-06A

`PL-V38-06A` remains the correct stage for formal asset reactivation, lineage
qualification, archival decisions, and provenance receipts.

This note adds only an earlier lightweight question:

```text
"Do we already have a useful seed?"
```

It does not authorize use of an unqualified asset as product truth.

## External examples worth indexing now

Checklist/prompt patterns:
- https://github.com/testdouble/han/blob/main/han-coding/references/yagni-rule.md
- https://github.com/testdouble/han/blob/main/han-coding/skills/code-review/references/review-checklist.md
- https://github.com/microsoft/skills/blob/main/.github/prompts/code-review.prompt.md
- https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code

Cost/history-analysis patterns:
- https://github.com/adamtornhill/code-maat
- https://github.com/emrecdr/codelore

Architecture/cost research:
- https://www.sei.cmu.edu/blog/developing-an-architecture-focused-measurement-framework-for-managing-technical-debt/

These should initially be reference pointers, not vendored dependencies.
