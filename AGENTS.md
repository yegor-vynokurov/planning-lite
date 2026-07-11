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

## Version changes

For every release, update together:

- `pyproject.toml` project version;
- `src/planning_lite/__init__.py`;
- `template/.planning/VERSION`;
- `CHANGELOG.md`.

Use PEP 440-compatible Git tags such as `v3.0.0` or `v3.1.0`.

## Verification

Before declaring a framework change complete:

1. run `uv sync`;
2. run `uv run pytest`;
3. adopt the template into a temporary clean Git repository;
4. run `planning-lite doctor` there;
5. when update behavior changed, test an update between two Git tags and verify project-owned files remain unchanged.

Do not add Copier tasks or migrations without documenting why `--trust` is required and reviewing the security implications.
