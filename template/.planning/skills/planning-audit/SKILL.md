---
name: planning-audit
description: Use for current-state assessment, plan review, requirements completeness, implementation review, Git or plan-drift analysis without production-code edits.
compatibility: Requires repository file access. Git and test command access are optional but recommended.
metadata:
  planning-lite-version: "2.3.0"
---

Paths in this skill are relative to the skill directory.

Read `../../modes/AUDIT.md`, `../../ACTIVE.md`, and the single audit prompt or control workflow relevant to the request.

Write assessments, reviews, drift reports, or recommendations, but do not implement fixes. Use evidence from the smallest relevant set of files, commands, and commit ranges. Distinguish verified fact, inference, assumption, and recommendation.

## Planning response contract

Prefer compact plans with explicit:

- goal;
- scope;
- non-goals;
- decisions;
- tasks;
- acceptance criteria;
- risks and open questions.

Do not pad plans with generic engineering advice.
Do not omit dependencies or decision rationale merely to stay brief.
