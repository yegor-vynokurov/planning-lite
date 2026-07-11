# Mode: Interactive planning

## Purpose

Turn a chosen direction into a bounded, testable change through dialogue before implementation.

Planning is not a one-shot document generator. Use two passes.

## Pass A: planning dialogue

1. Read the minimum context from `CONTEXT_POLICY.md`.
2. Inspect relevant existing code, tests, contracts, configuration, and documentation.
3. Produce a short planning brief containing:
   - understood outcome;
   - evidence about current behavior;
   - proposed scope and explicit non-goals;
   - material unknowns and contradictions;
   - 1–3 viable approaches and trade-offs when a real choice exists;
   - decisions requiring the user;
   - provisional assumptions that are safe to make.
4. Challenge weak premises and over-engineering.
5. Pause before freezing the plan when a material product, architecture, migration, data, security, or compatibility decision remains.

Do not ask the user to decide trivial implementation details that can be investigated or safely assumed.

## Pass B: planning artifacts

Proceed when the user confirms the direction, explicitly delegates assumptions, or the remaining unknowns are minor and documented.

- create or update the change folder;
- maintain many-to-many recommendation links;
- fill proposal and specification before implementation details;
- create an executable plan and dependency-ordered tasks;
- map requirements and acceptance criteria to tests and tasks;
- run the pre-implementation audit;
- update the change `context.md` and `.planning/ACTIVE.md`;
- stop before production code unless the same user message directly authorizes implementation and all gates pass.

## Plan updates during execution

- Implementation-detail change: record in `amendments.md`, update plan/tasks/context, then continue.
- Scope or acceptance change: draft the amendment, mark execution blocked, request user approval.
- Unrelated improvement: create a recommendation.
- Accumulated quick fixes: use drift sync rather than rewriting plan history.

## Quality rules

- Prefer the smallest coherent change.
- Follow existing architecture unless evidence justifies changing it.
- Include failure, retry, interruption, repeated execution, rollback, recovery, compatibility, and migration where relevant.
- Name exact files, symbols, state transitions, checks, and stopping conditions.
- Do not hide uncertainty inside an implementation task.
- Do not plan speculative infrastructure for hypothetical future use.
