---
name: planning-checkpoint
description: Use to prepare durable state before compaction, a new conversation, or an agent switch.
compatibility: Requires repository and Git inspection.
---

Paths are relative to this skill directory.

Read and follow `../../control/SESSION_CHECKPOINT.md`. Stop production-code edits. Do not claim to run client UI actions.

The session checkpoint preserves state and handoff only; it does not grant
Git staging or commit authority. Any checkpoint commit requires its own
explicit gate.
