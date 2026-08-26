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

## Official template source

The built-in fallback source is `https://github.com/yegor-vynokurov/planning-lite`. Keep source resolution ordered from explicit overrides to the official fallback, and update the source-precedence tests whenever that behavior changes.

## Cold start / resume

For a fresh chat, coding agent, or maintainer session, do not reconstruct live
state from conversation memory, old Roadmaps, or `.planning-lab/**`.

Start from the Git-backed central checkout:

```powershell
git rev-parse --show-toplevel
uv run --frozen python scripts/maintainer_resume.py
```

Then:

1. treat `docs/design/project-spine/CURRENT.md` as the sole resume/navigation authority;
2. follow its `next_permitted_action`;
3. open `docs/design/project-spine/roadmap/ROADMAP.md` only when current direction sequencing is needed;
4. load the referenced Change/checkpoint/evidence only as required by that action;
5. if Git identity is missing, treat the directory as a snapshot, not an implementation-ready checkout;
6. if the working tree is dirty, report/adjudicate the dirt before writes;
7. do not run `planning-lite doctor .` at the central repository root.

A consumer project uses a different entry path: read that project's `AGENTS.md`,
then `.planning/control/ROOT_ROUTER.md`. Do not use the central
`maintainer_resume.py` workflow inside ordinary consumer projects.

## Verification economy

Use the smallest evidence stack sufficient for the new behavior and blast radius.

Preferred order:

```text
existing owner/product tests
→ one focused acceptance probe for genuinely new behavior
→ Git/write-boundary verification
→ broader/full suite only at meaningful integration, completion, or release gates
```

Rules:

- do not duplicate an invariant already owned by an existing test;
- do not assert on CLI help wording, prose formatting, pytest rendering, or other
  presentation text unless that literal representation is itself contractual;
- derive structural facts directly from Git, filesystem state, manifests, or the
  owning data structure when those are available;
- do not parse a human-oriented failure rendering as machine-readable repository state;
- when a custom verifier fails, adjudicate `product defect` versus `verifier defect`
  before changing product code;
- consumer/update smoke tests whose source identity depends on Git metadata must run
  from a clean committed central source;
- a read-only or documentation-only step should not inherit a full regression suite
  merely because the suite exists.

The goal is evidence quality, not assertion count.

## Verification

Before declaring a framework change complete:

1. run `uv sync`;
2. run `uv run pytest`;
3. adopt the template into a temporary clean Git repository;
4. run `planning-lite doctor` there;
5. when update behavior changed, test an update between two Git tags and verify project-owned files remain unchanged.

Do not add Copier tasks or migrations without documenting why `--trust` is required and reviewing the security implications.
