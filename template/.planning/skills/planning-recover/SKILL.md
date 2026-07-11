---
name: planning-recover
description: Use when planning or code started without the correct approval, the agent used the wrong mode, or the user asks to stop and reconcile accidental work without automatic rollback.
compatibility: Requires repository and Git state inspection. Do not require destructive commands.
metadata:
  planning-lite-version: "2.3.0"
---

Paths in this skill are relative to the skill directory.

Read `../../control/RECOVERY.md`, `../../ACTIVE.md`, and `../../prompts/13-recover-from-wrong-mode.md`.

Stop affected work, preserve the diff, inventory side effects, mark premature artifacts honestly, and present adopt, draft, revise, split, or explicit-revert options. Do not edit production code further or perform an automatic rollback.
