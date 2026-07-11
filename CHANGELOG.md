# Changelog

## Unreleased

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
