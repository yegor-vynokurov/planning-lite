# Agent adapter contract

An adapter is valid only if it preserves the neutral Planning Lite semantics.

## Required mappings

Every adapter must document:

1. project instruction entrypoint;
2. canonical skill exposure method;
3. explicit skill invocation syntax, if supported;
4. operator-only context compaction and new-session actions, if supported;
5. how to verify that instructions and skills are loaded;
6. tool limitations that affect Git, tests, file editing, or sandbox behavior.

## Forbidden adapter behavior

An adapter must not:

- weaken approval gates;
- infer code authorization from plan or recommendation approval;
- rewrite canonical skills with agent-specific assumptions;
- store project state only in client memory;
- claim an operator interface action was executed when it was not;
- silently broaden the context packet or load all planning files.

## Canonical skill rule

`.planning/skills/` is the source of truth. Agent-specific skill folders should contain thin wrappers, generated copies, or configured references. Updates flow from canonical skills to adapters, never the reverse without an explicit upstream change.
