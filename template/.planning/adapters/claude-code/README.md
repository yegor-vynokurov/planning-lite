# Claude Code adapter

This adapter is architectural and is not enabled automatically.

## Instruction bridge

Claude Code reads `CLAUDE.md`, not `AGENTS.md`. When enabling the adapter, copy `templates/CLAUDE.md` to the repository root. It imports `AGENTS.md`, avoiding duplicated core rules.

## Skills

Claude Code discovers project skills under `.claude/skills/<name>/SKILL.md` and invokes them as `/skill-name`. Materialize thin wrappers that point to `.planning/skills/<name>/SKILL.md`, following `templates/SKILL_WRAPPER.md.template`.

Do not copy the complete workflow into `CLAUDE.md`. Keep it short and client-specific. Optional hooks and permission settings may later enforce approval boundaries, but they are outside the neutral core.

Before activation, verify current commands and capabilities in the installed Claude Code version.
