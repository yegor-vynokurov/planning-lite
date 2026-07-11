# Changelog

## Unreleased

## 3.0.3 - 2026-07-11

- Use the official GitHub repository as the built-in template source so new computers can run `adopt` immediately after installing the CLI.
- Keep `planning-lite configure` as an optional override for forks and local development copies.
- Add regression tests for template-source precedence and fallback behavior.

## 3.0.2 - 2026-07-11

- Derive package versions from Git tags through `hatch-vcs`.
- Add `planning-lite release` for checked patch, minor, major, and explicit releases.
- Read installed template versions from Copier metadata instead of `.planning/VERSION`.
- Add regression tests for package metadata, version duplication, release numbering, and changelog finalization.

## 3.0.0

- Converted Planning Lite into a centrally versioned Copier template.
- Added an install/update/doctor CLI.
- Split framework defaults from project overrides.
- Added explicit managed and project-owned path policies.
- Moved the full router into a managed control file while preserving project-local `AGENTS.md`.
