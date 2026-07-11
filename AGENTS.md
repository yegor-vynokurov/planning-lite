# Planning Lite central repository instructions

This repository is the central source and update mechanism for Planning Lite. It is not an ordinary target project using Planning Lite.

## Source-of-truth boundaries

- `template/` contains files rendered into target projects.
- `src/planning_lite/` contains the distribution CLI.
- `copier.yml` defines update and ownership behavior.
- `docs/` and root `README.md` document central maintenance.
- Never edit a generated target project as the source of a framework change. Port reusable changes back into `template/`.

## Ownership safety

Before moving or renaming a rendered file, check both:

- `copier.yml` `_skip_if_exists` patterns;
- `template/.planning/framework/OWNERSHIP.yml`.

Framework updates must not overwrite project-owned goals, plans, recommendations, decisions, active state, configuration overrides, or completed work records.

`template/AGENTS.md` is a one-time project-owned bridge. The centrally managed routing logic belongs in `template/.planning/control/ROOT_ROUTER.md`.

## Version and release changes

Git tags are the single source of release versions. Do not add hard-coded package or template versions.

- `hatch-vcs` derives Python package metadata from Git tags.
- `planning_lite.__version__` reads installed package metadata.
- target projects read the installed template ref from `.copier-answers.planning-lite.yml`.
- `template/.planning/VERSION` must not exist.

Prepare release notes under `## Unreleased` in `CHANGELOG.md`, commit framework changes, then run:

```text
uv run planning-lite release patch
uv run planning-lite release minor
uv run planning-lite release major
```

The release command runs checks, finalizes the changelog, creates a release commit, and creates an annotated PEP 440-compatible tag. It never pushes automatically.

## Verification

Before declaring a framework change complete:

1. run `uv sync`;
2. run `uv run pytest`;
3. adopt the template into a temporary clean Git repository;
4. run `planning-lite doctor` there;
5. when update behavior changed, test an update between two Git tags and verify project-owned files remain unchanged.

Do not add Copier tasks or migrations without documenting why `--trust` is required and reviewing the security implications.
