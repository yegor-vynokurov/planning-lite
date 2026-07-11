# Plan an approved change through dialogue

Mode: Planning.

## Authorization check

The change proposal must exist. For a full executable plan, it should be Approved. Planning may proceed without implementation authorization, but production code must not change.

## Pass A: planning brief and dialogue

1. Read the active change `context.md`, proposal, specification, and targeted repository evidence.
2. Produce a concise planning brief:
   - current flow and baseline;
   - proposed scope and non-goals;
   - material unknowns or contradictions;
   - viable approaches and trade-offs;
   - likely files and contracts;
   - migration, recovery, compatibility, and test implications;
   - decisions requiring the user;
   - safe provisional assumptions.
3. Be a candid critic. Flag weak premises, missing criteria, and likely future conflicts.
4. Pause when material product, architecture, data, security, migration, or compatibility decisions remain.

## Pass B: artifacts after alignment

1. Fill `plan.md` as a self-contained executable design.
2. Fill `tasks.md` with dependency-ordered, atomic, verifiable tasks.
3. Map requirements and acceptance criteria to plan sections, tasks, and verification.
4. Create ADRs for durable architectural decisions.
5. Initialize `amendments.md` and update `context.md`.
6. Run prompt `06-audit-before-implementation.md`.
7. Update `.planning/ACTIVE.md` with audit outcome and next permitted action.
8. Stop before code unless the same user message directly authorizes implementation and every gate passes.

## Planning constraints

- Prefer the smallest coherent compatible change.
- Do not hide uncertainty inside tasks.
- Do not add infrastructure for hypothetical future needs.
- Do not remove failure, compatibility, migration, recovery, documentation, or verification work merely because the happy path is easier.
