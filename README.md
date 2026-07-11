README_planning_lite_updated.md


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


## Prerequisites and installing `uv`

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

After installation, close all VS Code terminals, reopen the terminal, and verify:

```powershell
uv --version
```

If the standalone installer completed but PowerShell still cannot find `uv`, temporarily add its default user installation directory to the current session:

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

If the command is still unavailable, add the default installation directory to the current shell:

```bash
export PATH="$HOME/.local/bin:$PATH"
uv --version
```

To make the change persistent for Bash:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

For another shell, add the same directory to that shell's profile file.

### Updating `uv`

When `uv` was installed with the standalone installer:

```text
uv self update
```

When it was installed with WinGet or another package manager, use that package manager's update command instead.

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

## Single-source versioning

Planning Lite uses the Git tag as the only source of a release version. Do not manually synchronize version strings in several files.

- `hatch-vcs` derives Python package metadata from the nearest Git tag;
- `planning_lite.__version__` reads the installed package metadata;
- Copier stores the installed template tag in `.copier-answers.planning-lite.yml`;
- `template/.planning/VERSION` is intentionally absent.

On commits after the latest tag, development builds receive a version such as `3.0.1.dev2+g<commit>`. A tagged commit such as `v3.0.1` produces the release version `3.0.1`.

Prepare release notes under `## Unreleased` in `CHANGELOG.md`, commit the framework changes, and use the release command:

```powershell
uv run planning-lite release patch
```

The positional argument may be `patch`, `minor`, `major`, or an explicit version such as `3.2.0`. The command:

1. requires a clean Git working tree and, by default, the `main` branch;
2. reads the latest stable version tag;
3. validates `CHANGELOG.md` and checks that `uv.lock` does not contain the known environment-specific internal index;
4. runs the test suite and the template update smoke test;
5. moves the `Unreleased` entries into a dated release section;
6. creates a release commit and an annotated Git tag;
7. prints the push commands but does not push automatically.

Preview without changing Git:

```powershell
uv run planning-lite release patch --dry-run
```

After reviewing the local release:

```powershell
git push origin main
git push origin v3.0.1
```

If dependencies or build-system requirements changed, regenerate and commit `uv.lock` before the release command:

```powershell
uv lock --default-index https://pypi.org/simple
uv sync --default-index https://pypi.org/simple
```

## Running the CLI while developing this repository

### Recommended workflow with `uv`

From the repository root:

```text
uv sync
uv run planning-lite --version
```

`uv sync` creates or updates `.venv` and synchronizes it with the dependencies declared by the project. `uv run` executes the command inside that environment, so manual activation is not required.

Configure the template source once.

Windows:

```powershell
uv run planning-lite configure --template-source D:\path\to\planning-lite
```

Linux:

```bash
uv run planning-lite configure --template-source /path/to/planning-lite
```

After the repository is pushed, configure the Git URL instead:

```text
uv run planning-lite configure --template-source git@github.com:YOUR_ACCOUNT/planning-lite.git
```

### Alternative workflow without `uv`

`uv` is recommended but not required. You can use the standard Python `venv` module and `pip` instead. This requires a supported Python installation with `pip` available.

#### Windows PowerShell

```powershell
cd D:\path\to\planning-lite
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e .
planning-lite --version
```

Configure the template source:

```powershell
planning-lite configure --template-source D:\path\to\planning-lite
```

If PowerShell blocks environment activation, either adjust the execution policy for the current process:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

or run the environment's executables directly without activation:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\planning-lite.exe --version
```

#### Linux

```bash
cd /path/to/planning-lite
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
planning-lite --version
```

Configure the template source:

```bash
planning-lite configure --template-source /path/to/planning-lite
```

To leave the environment later:

```text
deactivate
```

The `venv + pip` workflow is fully usable, but it requires manual environment activation and dependency maintenance. `uv` is more convenient for this repository because one command synchronizes the environment, `uv run` avoids activation mistakes, and `uv tool install` provides an isolated global CLI installation.

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


Without `uv`, install the CLI into a dedicated virtual environment rather than into the system Python.

Windows PowerShell:

```powershell
py -m venv $HOME\.venvs\planning-lite
& "$HOME\.venvs\planning-lite\Scripts\python.exe" -m pip install --upgrade pip
& "$HOME\.venvs\planning-lite\Scripts\python.exe" -m pip install "git+ssh://git@github.com/YOUR_ACCOUNT/planning-lite.git@v3.0.0"
& "$HOME\.venvs\planning-lite\Scripts\planning-lite.exe" --version
```

Linux:

```bash
python3 -m venv "$HOME/.venvs/planning-lite"
"$HOME/.venvs/planning-lite/bin/python" -m pip install --upgrade pip
"$HOME/.venvs/planning-lite/bin/python" -m pip install "git+ssh://git@github.com/YOUR_ACCOUNT/planning-lite.git@v3.0.0"
"$HOME/.venvs/planning-lite/bin/planning-lite" --version
```

This fallback keeps Planning Lite isolated, but you must either call the executable by its full path or add that environment's executable directory to `PATH`. For frequent use across many projects, `uv tool install` is simpler.

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

Create a new central release. Add notes to `CHANGELOG.md` under `## Unreleased`, commit the framework changes, then choose the appropriate release increment:

```powershell
# In the Planning Lite repository
git add .
git commit -m "Improve planning checkpoint workflow"
uv run planning-lite release minor

# The release command prints these; push only after review.
git push origin main
git push origin v3.1.0
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
planning-lite release patch|minor|major|MAJOR.MINOR.PATCH
```

See `docs/ARCHITECTURE.ru.md` and `docs/OPERATOR_WORKFLOW.ru.md` for the detailed maintenance procedure.

## Windows bootstrap helper

From the central repository root:

```powershell
.\scripts\bootstrap_repo.ps1 -RemoteUrl git@github.com:YOUR_ACCOUNT/planning-lite.git -Tag v3.0.0
```

The script initializes Git when needed, creates the initial commit and tag, and configures `origin`. It does not push automatically.