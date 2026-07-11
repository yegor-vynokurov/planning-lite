---
name: planning-checkpoint
description: Use when the user asks to perform a checkpoint, prepare a durable handoff, compact the current conversation, or start a new session without losing project state.
compatibility: Requires repository file access. Git access is optional but recommended.
metadata:
  planning-lite-version: "2.3.0"
---

Paths in this skill are relative to the skill directory.

Read `../../control/SESSION_CHECKPOINT.md`, `../../ACTIVE.md`, and the effective configuration defined by `../../control/CONFIG_RESOLUTION.md`.

Stop changing production code. Update only the active state files required by the checkpoint workflow. Collect a compact Git summary, not a full raw diff. If a Git review trigger is reached, report it and route to the `planning-git-review` skill rather than silently loading the whole patch.

Prepare durable state and report readiness. Never claim to execute a client-interface action such as context compaction, starting a new session, forking, or clearing a conversation. Those remain operator actions defined by the active agent adapter.
