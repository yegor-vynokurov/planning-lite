# Planning Lite

Planning Lite is a centrally versioned planning and control framework for coding agents.
It is maintained in one Git repository and installed into many existing projects without nested Git repositories.

The central repository contains:

- the canonical prompts, modes, controls, templates, and agent skills;
- a Copier template used for safe project updates;
- a small `planning-lite` CLI that wraps adoption, updates, and validation.

Each target project receives ordinary tracked files. Copier records the source repository and installed Git tag in `.copier-answers.planning-lite.yml`, then performs smart updates from newer tags. Copier recommends a Git-versioned template, a tracked answers file, and a Git-versioned target project for reliable updates.

## Ownership model

### Centrally managed

These files evolve in this repository and are updated into target projects:

- `.planning/control/`, `.planning/modes/`, `.planning/prompts/`;
- canonical skills and agent adapters;
- templates for changes, recommendations, assessments, decisions, and drift reviews;
- framework defaults, workflow documentation, and the managed root router.

### Project-owned

These files are created on first adoption and then preserved:

- project goals, rules, completion criteria, architecture, roadmap, and repository map;
- active and completed changes;
- assessments, recommendations, decisions, and quick-change records;
- `.planning/ACTIVE.md`, `.planning/CONFIG.yml`, and `.planning/AGENT_PROFILE.yml`;
- the root `AGENTS.md` bridge and project-specific instructions.

The complete policy is rendered to `.planning/framework/OWNERSHIP.yml`.

## Repository layout

```text
planning-lite/
├── copier.yml                 # template update policy
├── template/                  # files rendered into target projects
├── src/planning_lite/         # CLI wrapper
├── tests/
├── docs/
└── pyproject.toml
```

## First-time setup of this central repository

```powershell
cd D:\path\to\planning-lite
git init
git add .
git commit -m "Create Planning Lite template repository"
git branch -M main
git tag v3.0.0
```

Create a remote repository and add it:

```powershell
git remote add origin git@github.com:YOUR_ACCOUNT/planning-lite.git
git push -u origin main
git push origin v3.0.0
```

Copier chooses released Git tags for updates, so framework releases should be tagged with PEP 440-compatible versions such as `v3.0.0` and `v3.1.0`.

## Running the CLI while developing this repository

```powershell
uv sync
uv run planning-lite --version
```

Configure the template source once:

```powershell
uv run planning-lite configure --template-source D:\path\to\planning-lite
```

After the repository is pushed, configure the Git URL instead:

```powershell
uv run planning-lite configure --template-source git@github.com:YOUR_ACCOUNT/planning-lite.git
```

## Installing the CLI globally

From a Git remote:

```powershell
uv tool install git+ssh://git@github.com/YOUR_ACCOUNT/planning-lite.git@v3.0.0
planning-lite configure --template-source git@github.com:YOUR_ACCOUNT/planning-lite.git
```

For a public HTTPS repository:

```powershell
uv tool install git+https://github.com/YOUR_ACCOUNT/planning-lite.git@v3.0.0
```

`uv tool install` installs the CLI in an isolated tool environment, so it does not become a dependency of the target Python, R, or mixed-language project.

## Adopting Planning Lite in an existing project

Start with a clean Git working tree:

```powershell
cd D:\projects\my-project
git status
planning-lite adopt . --agent codex --vcs-ref v3.0.0
planning-lite doctor .
git diff --stat
git add AGENTS.md .agents .planning .copier-answers.planning-lite.yml
git commit -m "Adopt Planning Lite v3.0.0"
```

The `adopt` command appends a small marked bridge to an existing `AGENTS.md` instead of replacing the file.

## Updating target projects

Create a new central release:

```powershell
# In the Planning Lite repository
git add .
git commit -m "Improve planning checkpoint workflow"
git tag v3.1.0
git push origin main v3.1.0
```

Preview the update in a target project:

```powershell
planning-lite check .
```

Apply it in a dedicated branch:

```powershell
git switch -c chore/update-planning-lite-3.1
planning-lite update .
planning-lite doctor .
git status
git diff --stat
```

Resolve any Copier conflict markers, run project checks, and commit the framework update separately.

## Local configuration

Centrally managed defaults live in:

```text
.planning/framework/defaults.yml
```

Project-specific overrides live in:

```text
.planning/CONFIG.yml
```

Keep the override file small. Do not copy all defaults into it, or the project will stop receiving improved defaults from future framework versions.

## Commands

```text
planning-lite configure --template-source SOURCE
planning-lite adopt [TARGET]
planning-lite check [TARGET]
planning-lite update [TARGET]
planning-lite doctor [TARGET]
planning-lite ownership [TARGET]
```

See `docs/ARCHITECTURE.ru.md` and `docs/OPERATOR_WORKFLOW.ru.md` for the detailed maintenance procedure.

## Windows bootstrap helper

From the central repository root:

```powershell
.\scripts\bootstrap_repo.ps1 -RemoteUrl git@github.com:YOUR_ACCOUNT/planning-lite.git -Tag v3.0.0
```

The script initializes Git when needed, creates the initial commit and tag, and configures `origin`. It does not push automatically.
