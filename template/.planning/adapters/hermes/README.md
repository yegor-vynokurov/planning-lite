# Hermes adapter

This adapter is architectural and is not enabled automatically.

Hermes can use the repository `AGENTS.md` directly. Its skills follow the Agent Skills format and may be invoked with `/skill-name`.

The preferred future setup is to register the repository's `.planning/skills/` directory as an external Hermes skills directory. This avoids duplicate skill copies and keeps Planning Lite updates centralized. A profile-local copy is a fallback when external directories are unavailable or should be immutable.

Security note: an external directory is not automatically read-only. If Hermes may edit skills, protect shared canonical files with filesystem permissions or a profile policy.

Before activation, verify the external-directory configuration against the installed Hermes version and update the project `AGENT_PROFILE.yml`.
