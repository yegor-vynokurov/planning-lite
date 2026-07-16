# Agent portability

Before switching the primary agent shell or model:

1. run `SESSION_CHECKPOINT.md`;
2. verify that canonical state is in repository files rather than chat history;
3. read `.planning/AGENT_PROFILE.yml` and the destination adapter;
4. materialize wrappers only when the destination requires them;
5. run a read-only sanity check of mode, active change, authorization, and next action.

Client commands, hooks, permissions, and skill exposure belong in adapters. Project approvals, plans, tests, and state remain neutral.
