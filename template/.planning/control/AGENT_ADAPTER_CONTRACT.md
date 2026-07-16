# Agent adapter contract

Adapters may translate:

- instruction-file locations;
- skill exposure paths and invocation syntax;
- client commands, hooks, permissions, and operator actions.

Adapters must not redefine:

- project state or ownership;
- approval gates;
- modes or functional workflows;
- recommendation or change lifecycle;
- verification evidence.

Canonical skills live under `.planning/skills/`. Adapter copies and wrappers are disposable projections.
