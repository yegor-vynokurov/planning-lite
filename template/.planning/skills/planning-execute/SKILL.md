---
name: planning-execute
description: Use only when the user directly commands implementation or named tasks from an approved, audited active change.
compatibility: Requires repository editing and command execution capabilities.
metadata:
  planning-lite-version: "2.3.0"
---

Paths in this skill are relative to the skill directory.

Read `../../modes/EXECUTE.md`, `../../control/APPROVAL_GATES.md`, `../../ACTIVE.md`, and the active change `context.md`.

If authorization is missing, do not edit code. Route to Planning. Execute only approved scope, verify each task, and record amendments before continuing when reality differs. Use the active agent adapter only for interface-specific actions; project behavior remains governed by the neutral Planning Lite core.

## Execution response contract

Keep routine progress updates compact.

After a completed step, report:

- changed;
- checked;
- result;
- blocker, if any.

Do not repeat the approved plan.
Do not explain straightforward edits unless they are surprising,
risky, or differ from the plan.
