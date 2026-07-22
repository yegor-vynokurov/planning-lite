# Changelog

## Unreleased

- state machine:

Discovery
→ Definition
→ Planning
→ Readiness
→ Execution
→ Verification
→ Closure

- every stage has:

Lifecycle stage
Stage status
Next gate
Next permitted action

- new chain of aproving:

proposal approved
→ plan drafted
→ plan approved
→ readiness audit
→ direct execution authorization

- also added 
Facts vs Decisions в critic mode;
WAYFINDING.md for big tasks;
CODEBASE_DESIGN.md;
DELIVERY_SLICES.md;
DOMAIN_MODELING.md;
CODE_REVIEW.md;
tracer bullet, expand-contract, blocking edge, verification seam, blast radius;
separate runnings spec conformance and standards conformance;
prompt-quality checklist с completion criterion и no-op test;
new version of project glossary for canonical terms of the project (autho filling).

## 4.1.0 - 2026-07-20

- ready templates for all main actions.
- now agents may do not overwrite task.md or like document but go to templates and fill the template

## 4.0.0 - 2026-07-16

- big update to avoide duplications in the control prompts 
- to clarify functional procedures for agents such as closure.

## 3.1.2 - 2026-07-15

- change cirillic symbols to eng descriptions

## 3.1.1 - 2026-07-14

- Add a caveman prompt parts to the control root_router.md as soft rules
- Add a caveman prompt parts to the skills depend role of the agent in the skill

## 3.1.0 - 2026-07-13

- Add a simple one-command installation mode using `uvx`.
- Add `planning-lite install` for users who only need repository-local agent prompts.
- Move persistent CLI installation and template updates to `docs/UPDATABLE_INSTALLATION.ru.md`.

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
