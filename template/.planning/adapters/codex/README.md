# Codex adapter

Codex discovers thin wrappers under `.agents/skills/`. Explicit skill invocation uses `$planning-plan`, `$planning-execute`, and the other canonical names. Wrappers must point to `.planning/skills/<name>/SKILL.md` and must not duplicate workflow logic.

Client commands such as context compaction, new conversations, model selection, and permission controls remain operator actions.
