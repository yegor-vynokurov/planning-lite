# Canonical Planning Lite skills

This directory is the source of truth for reusable Planning Lite workflows. Skills follow the open Agent Skills `SKILL.md` format and avoid client-specific invocation syntax.

Agent adapters may expose these skills in different ways:

- Codex: thin wrappers under `.agents/skills/` and explicit invocation such as `$planning-plan`.
- Claude Code: wrappers or copies under `.claude/skills/`, invoked as `/planning-plan`.
- Hermes: this directory can be registered as an external skills directory, or skills can be copied into the Hermes profile.
- Generic agents: read the named canonical `SKILL.md` directly or use the equivalent natural-language trigger.

Do not edit adapter copies as the canonical source. Update files here, then regenerate or refresh the adapter layer.
