# Planning Lite

Planning Lite is a centrally versioned planning and control framework for coding agents.
It is maintained in one Git repository and installed into many existing projects without nested Git repositories.

The central repository contains:

- canonical prompts, modes, controls, templates, and agent skills;
- a Copier template used for safe project updates;
- a small `planning-lite` CLI that wraps adoption, updates, validation, and releases.

Each target project receives ordinary tracked files. Copier records the source repository and installed Git tag in `.copier-answers.planning-lite.yml`, then performs smart updates from newer tags.

## Quick start on a new computer

The central repository does not need to be cloned to use Planning Lite in other projects.
The normal workflow is:

```text
install uv
    ↓
install the planning-lite CLI once
    ↓
adopt Planning Lite in any Git project
    ↓
update that project when a newer template tag is released
```

### 1. Install `uv`

Check whether `uv` is already available:

```text
uv --version
```

If it is missing, see [Installing `uv`](#installing-uv) below.

### 2. Install the Planning Lite CLI

Install a released version as a user-wide isolated tool:

```powershell
uv tool install "git+https://github.com/yegor-vynokurov/planning-lite.git@v3.0.2"
```

Verify the command:

```powershell
planning-lite --version
```

If `uv` reports that the tool directory is not on `PATH`, run:

```powershell
uv tool update-shell
```

Then reopen the terminal.

This installs the CLI and its Python dependencies in an isolated `uv` tool environment. It does not clone the central repository into your documents and does not add Planning Lite as a dependency of the target project.

### 3. Adopt Planning Lite in a project

The target must already be a Git repository. Start with a clean working tree:

```powershell
cd D:\documents\my-project
git status

planning-lite adopt . --agent codex --vcs-ref v3.0.2
planning-lite doctor .

git diff --stat
git add AGENTS.md .agents .planning .copier-answers.planning-lite.yml
git commit -m "Adopt Planning Lite v3.0.2"
```

The `adopt` command creates ordinary project files such as:

```text
my-project/
├── AGENTS.md
├── .agents/
├── .planning/
└── .copier-answers.planning-lite.yml
```

The root `AGENTS.md` remains project-owned. Planning Lite appends a small marked bridge instead of replacing existing project instructions.

### Why `configure` is not required

The CLI contains this official template source as its built-in default:

```text
https://github.com/yegor-vynokurov/planning-lite
```

Therefore, after `uv tool install`, this works immediately from any target project:

```powershell
planning-lite adopt . --agent codex --vcs-ref v3.0.2
```

`planning-lite configure` is now optional. Use it only to override the official source with a fork, another repository, or a local development copy.

## Template source selection

Planning Lite resolves the template source in this order:

1. `--template-source` passed to the current command;
2. the `PLANNING_LITE_TEMPLATE` environment variable;
3. a local central repository found from the current directory or one of its parents;
4. a user override saved by `planning-lite configure`;
5. the built-in official repository: `https://github.com/yegor-vynokurov/planning-lite`.

### Override the source for all future adoptions

For a fork:

```powershell
planning-lite configure `
  --template-source https://github.com/OTHER_ACCOUNT/planning-lite
```

For a local development copy:

```powershell
planning-lite configure `
  --template-source D:\documents\planning-lite
```

The override is stored in the current user's Planning Lite configuration. Existing adopted projects keep their own source metadata in `.copier-answers.planning-lite.yml`.

### Override the source for one command only

```powershell
planning-lite adopt . `
  --template-source D:\documents\planning-lite `
  --vcs-ref HEAD `
  --agent codex
```

This is useful for testing an unreleased local template without changing the user-wide default.

## Updating an adopted project

After a newer template tag is released, enter the target project and preview the update:

```powershell
cd D:\documents\my-project
planning-lite check .
```

Apply it in a dedicated branch:

```powershell
git switch -c chore/update-planning-lite
planning-lite update .
planning-lite doctor .
git status
git diff --stat
```

Resolve any Copier conflicts, run the project's checks, and commit the framework update separately from product code.

The update command reads the source and currently installed tag from:

```text
.copier-answers.planning-lite.yml
```

It normally does not need `configure` or `--template-source` again.

## Updating the globally installed CLI

The installed CLI and the template files inside a target project are related but separate:

```text
uv tool install ...
    updates the executable used on the computer

planning-lite update .
    updates managed Planning Lite files in one target project
```

To install a newer released CLI, repeat `uv tool install` with the new tag:

```powershell
uv tool install "git+https://github.com/yegor-vynokurov/planning-lite.git@v3.0.3"
planning-lite --version
```

Then update each adopted project separately:

```powershell
planning-lite check .
planning-lite update .
planning-lite doctor .
```

## Ownership model

### Centrally managed

These files evolve in the central repository and are updated into target projects:

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

## Installing `uv`

Planning Lite uses [`uv`](https://docs.astral.sh/uv/) for the recommended workflow. It can create and synchronize virtual environments, run project commands without manual activation, and install CLI tools in isolated user-wide environments.
Planning Lite is a Python CLI project. The recommended development workflow uses [`uv`](https://docs.astral.sh/uv/), a fast Python project and package manager that can:

- create and synchronize the local `.venv` environment;
- install the versions declared by `pyproject.toml` and `uv.lock`;
- run project commands without manually activating the environment;
- install `planning-lite` globally as an isolated CLI tool without adding it to another project's dependencies.

Check whether `uv` is already available:

```text
uv --version
```

If the command is not recognized, install `uv` using one of the methods below.
### Windows

The simplest option on current Windows systems is WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

Alternatively, use the official standalone installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Close all VS Code terminals, reopen the terminal, and verify:

```powershell
uv --version
```

If the standalone installer completed but PowerShell still cannot find `uv`, temporarily add its default user installation directory:

```powershell
$env:Path = "$HOME\.local\bin;$env:Path"
Get-Command uv
uv --version
```

Then restart VS Code. If necessary, add `$HOME\.local\bin` permanently to the user `PATH`.

### Linux

Install `uv` with the official standalone installer:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

If `curl` is unavailable:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

Open a new shell and verify:

```bash
uv --version
```

If the command is still unavailable:

```bash
export PATH="$HOME/.local/bin:$PATH"
uv --version
```

For Bash, make the path persistent:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

### Updating `uv`

When installed with the standalone installer:

```text
uv self update
```

When installed with WinGet or another package manager, use that package manager's update command.

## Alternative installation without `uv`

`uv` is recommended but not required. A standard Python virtual environment and `pip` can also install the CLI.

### Windows PowerShell

```powershell
py -m venv $HOME\.venvs\planning-lite
& "$HOME\.venvs\planning-lite\Scripts\python.exe" -m pip install --upgrade pip
& "$HOME\.venvs\planning-lite\Scripts\python.exe" -m pip install `
  "git+https://github.com/yegor-vynokurov/planning-lite.git@v3.0.2"
& "$HOME\.venvs\planning-lite\Scripts\planning-lite.exe" --version
```

Run it by full path, or add the environment's `Scripts` directory to `PATH`:

```powershell
& "$HOME\.venvs\planning-lite\Scripts\planning-lite.exe" adopt . `
  --agent codex `
  --vcs-ref v3.0.2
```

### Linux

```bash
python3 -m venv "$HOME/.venvs/planning-lite"
"$HOME/.venvs/planning-lite/bin/python" -m pip install --upgrade pip
"$HOME/.venvs/planning-lite/bin/python" -m pip install \
  "git+https://github.com/yegor-vynokurov/planning-lite.git@v3.0.2"
"$HOME/.venvs/planning-lite/bin/planning-lite" --version
```

The `venv + pip` workflow is fully usable. `uv` is more convenient because it installs the command user-wide, keeps it isolated, manages its environment, and avoids calling the executable by a long path.

## Developing the central repository

Clone the central repository only when you intend to modify Planning Lite itself:

```powershell
git clone https://github.com/yegor-vynokurov/planning-lite.git
cd planning-lite
uv sync
uv run planning-lite --version
uv run pytest
uv run python scripts/test_template_update.py
```

No `planning-lite configure` command is needed for central development. When commands run inside the central repository, the CLI recognizes the local `copier.yml` and `template/` directory.

To test the local unreleased template against another repository:

```powershell
uv run planning-lite adopt D:\documents\test-project `
  --template-source D:\documents\planning-lite `
  --vcs-ref HEAD `
  --agent codex
```

## Single-source versioning and releases

Planning Lite uses the Git tag as the only source of a release version. Do not manually synchronize version strings in several files.

- `hatch-vcs` derives Python package metadata from the nearest Git tag;
- `planning_lite.__version__` reads installed package metadata;
- Copier stores the installed template tag in `.copier-answers.planning-lite.yml`;
- `template/.planning/VERSION` is intentionally absent.

On commits after the latest tag, development builds receive a version such as `3.0.3.dev2+g<commit>`. A tagged commit such as `v3.0.3` produces the release version `3.0.3`.

Prepare notes under `## Unreleased` in `CHANGELOG.md`, commit the framework changes, and preview the next release:

```powershell
uv run planning-lite release patch --dry-run
```

Create the release:

```powershell
uv run planning-lite release patch
```

The positional argument may be `patch`, `minor`, `major`, or an explicit version such as `3.2.0`. The command:

1. requires a clean Git working tree and, by default, the `main` branch;
2. reads the latest stable version tag;
3. validates `CHANGELOG.md` and `uv.lock`;
4. runs the test suite and template smoke test;
5. moves `Unreleased` entries into a dated release section;
6. creates a release commit and annotated Git tag;
7. prints push commands but does not push automatically.

After reviewing the local release:

```powershell
git push origin main
git push origin v3.0.3
```

If dependencies or build-system requirements changed, regenerate and commit `uv.lock` first:

```powershell
uv lock --default-index https://pypi.org/simple
uv sync --default-index https://pypi.org/simple
```

## Local project configuration

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
planning-lite adopt [TARGET]
planning-lite check [TARGET]
planning-lite update [TARGET]
planning-lite doctor [TARGET]
planning-lite ownership [TARGET]
planning-lite release patch|minor|major|MAJOR.MINOR.PATCH
planning-lite configure --template-source SOURCE   # optional override
```

See `docs/ARCHITECTURE.ru.md` and `docs/OPERATOR_WORKFLOW.ru.md` for the detailed maintenance procedure.

## Windows bootstrap helper

For a new central repository checkout that has not yet been initialized with Git:

```powershell
.\scripts\bootstrap_repo.ps1 `
  -RemoteUrl https://github.com/yegor-vynokurov/planning-lite.git `
  -Tag v3.0.0
```

The script initializes Git when needed, creates the initial commit and tag, and configures `origin`. It does not push automatically.
