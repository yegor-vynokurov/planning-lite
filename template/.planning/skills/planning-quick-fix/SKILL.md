---
name: planning-quick-fix
description: Use for an explicit tiny low-risk edit such as a typo, capitalization correction, narrow message change, or local regression assertion; do not use for API, schema, architecture, dependency, migration, security, or scope changes.
compatibility: Requires repository editing and narrow verification capabilities.
metadata:
  planning-lite-version: "2.3.0"
---

Paths in this skill are relative to the skill directory.

Read `../../modes/QUICK_FIX.md`, `../../control/DRIFT_POLICY.md`, and the effective configuration defined by `../../control/CONFIG_RESOLUTION.md`.

If every criterion passes, make the minimum edit, verify it, and add one row to `../../drift/QUICK_CHANGES.md`. Otherwise stop and switch to Planning.
