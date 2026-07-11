---
name: planning-git-review
description: Use to review uncommitted changes, a commit, or a bounded commit range when requested, triggered by risk or drift, or before closing a non-trivial change; inspect summaries before targeted patches to conserve tokens.
compatibility: Requires Git command access and repository file access.
metadata:
  planning-lite-version: "2.3.0"
---

Paths in this skill are relative to the skill directory.

Read `../../control/GIT_CHANGE_REVIEW.md`, `../../ACTIVE.md`, the effective configuration from `../../control/CONFIG_RESOLUTION.md`, and only the active change sections needed for traceability.

Stay read-only for production code. Start with Git status, stats, names, and the narrowest relevant commit range. Do not load a repository-wide raw diff by default. Inspect targeted high-risk paths and record findings, evidence, and a verdict. Route corrections to Quick fix, Planning, Execution, or Recovery as appropriate.
