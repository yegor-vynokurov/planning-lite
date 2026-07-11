# Codex adapter

This adapter is active in the scaffold.

- Codex reads the repository `AGENTS.md`.
- Thin project skill wrappers live in `.agents/skills/`.
- Each wrapper points to the canonical skill under `.planning/skills/`.
- Codex-specific interface commands belong in `OPERATOR_GUIDE.ru.md`, not in the neutral core.

When canonical skills change, refresh the wrappers only if their metadata or routing changes. The workflow body remains centralized.
