# Agent and model portability

Planning Lite treats the repository as the durable source of project intent and state. The active model or agent shell may change without rewriting the project workflow.

## Portable layer

The following artifacts are agent-neutral:

- goals, completion criteria, project rules, architecture map, and Definition of Done;
- assessments, recommendations, decisions, approved changes, plans, tasks, and reviews;
- checkpoints, active context packets, Git commit ranges, tests, and verification evidence;
- modes, approval gates, drift policy, recovery policy, and canonical skills.

## Adapter layer

Only the following may vary by agent shell:

- persistent instruction filename and discovery rules;
- skill discovery path and explicit invocation syntax;
- operator commands for plan mode, compaction, new sessions, forks, or side conversations;
- optional hooks, permissions, sandboxes, and tool names.

## Switching procedure

Before switching agent shell or model:

1. Run the checkpoint workflow.
2. Record branch, HEAD, working-tree state, current task, blockers, and next permitted action.
3. Ensure the target adapter can read `AGENTS.md` or its bridge file.
4. Expose canonical skills using the target adapter.
5. Start a fresh session and read `ACTIVE.md` plus the active `context.md`.
6. Verify Git state before continuing.
7. Run a narrow cross-agent sanity check before granting implementation authority.

Do not carry a long conversation transcript as the handoff. Carry repository state and evidence.

## Model capability differences

A compatible format does not guarantee equal reliability. Smaller local models may need:

- explicit mode names;
- one bounded task at a time;
- named allowed files and tests;
- shorter context packets;
- stronger human approval and external verification.

Use more capable models for broad brownfield assessment, architectural planning, and final consistency review when needed. Use local models for narrow execution, checkpoints, summaries, and deterministic verification where they perform well.
