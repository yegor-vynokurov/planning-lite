# Design references

Planning Lite uses a neutral core plus thin client adapters.

Primary references used for the portability architecture:

- Agent Skills open specification: canonical `SKILL.md` format and progressive disclosure.
- OpenAI Codex: `AGENTS.md`, Agent Skills, and `.agents/skills/` discovery.
- Claude Code: `CLAUDE.md`, `@AGENTS.md` imports, and project skills under `.claude/skills/`.
- Hermes Agent: Agent Skills compatibility and external skill directories.

The references explain client capabilities; they do not override this repository's approval gates or project rules. Client commands can change across versions, so operator guides should be verified when an adapter is activated.
