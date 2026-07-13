# Planning Lite

Planning Lite is a repository-local set of planning prompts, agent instructions, skills, and project-state templates for coding agents.

The normal installation is intentionally small: open a terminal in the project that should receive Planning Lite and run one command.

## Basic installation

### Requirement

The computer needs [`uv`](https://docs.astral.sh/uv/). Check it with:

```text
uv --version
```

If `uv` is missing, install it once:

**Windows PowerShell**

```powershell
winget install --id=astral-sh.uv -e
```

**Linux or macOS**

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Open a new terminal after installing `uv`.

### Install Planning Lite into the current project

Open a terminal in the project root and run:

```powershell
uvx --from "git+https://github.com/yegor-vynokurov/planning-lite.git" planning-lite install .
```

That is the complete basic installation.

The command temporarily downloads and runs the installer, then adds the Planning Lite files to the current project. It does **not** install a permanent `planning-lite` command and does not require `configure`, `doctor`, or an update workflow.

After the command finishes, open or restart the coding agent in this project. The agent should read the bridge in `AGENTS.md` and then load Planning Lite instructions progressively.

Typical result:

```text
my-project/
├── AGENTS.md
├── .agents/
├── .planning/
└── .copier-answers.planning-lite.yml
```

Existing project instructions in `AGENTS.md` are preserved. Planning Lite appends a small marked bridge instead of replacing the file.

### Choose another agent adapter

Codex is the default. To select another prepared adapter:

```powershell
uvx --from "git+https://github.com/yegor-vynokurov/planning-lite.git" planning-lite install . --agent generic
```

Available values:

```text
codex
claude-code
hermes
generic
```

### What the basic installer does not do

The basic installer:

- does not clone the central repository into the project;
- does not add a nested Git repository;
- does not install a global executable;
- does not modify the project's source code;
- does not require the project to be a clean Git repository;
- does not ask the user to maintain Planning Lite versions.

The hidden Copier answers file is retained so that the project can later be moved to the update-enabled workflow without reinstalling all prompts from scratch.

## Update-enabled installation

The basic mode is enough when the goal is simply to add the planning prompts and start the agent.

For centralized updates, version tags, a persistent CLI, previewing changes, and updating many projects, use the advanced workflow:

[Update-enabled installation and maintenance](docs/UPDATABLE_INSTALLATION.ru.md)

## What is installed

### Centrally managed framework files

These files come from the Planning Lite template:

- `.planning/control/`, `.planning/modes/`, and `.planning/prompts/`;
- canonical skills and agent adapters;
- templates for changes, recommendations, assessments, decisions, and drift reviews;
- framework defaults and workflow documentation.

### Project-owned files

These are initialized for the project and then belong to that project:

- goals, rules, architecture notes, roadmap, and repository map;
- active changes, assessments, recommendations, and decisions;
- `.planning/ACTIVE.md`, `.planning/CONFIG.yml`, and `.planning/AGENT_PROFILE.yml`;
- project-specific instructions and the root `AGENTS.md` bridge.

The complete policy is stored in:

```text
.planning/framework/OWNERSHIP.yml
```

## Central repository development

Clone the repository only when you intend to modify Planning Lite itself:

```powershell
git clone https://github.com/yegor-vynokurov/planning-lite.git
cd planning-lite
uv sync
uv run pytest
uv run python scripts/test_template_update.py
```

Development, release automation, and template-update operations are documented separately in:

- `docs/ARCHITECTURE.ru.md`;
- `docs/OPERATOR_WORKFLOW.ru.md`;
- `docs/UPDATABLE_INSTALLATION.ru.md`.

## License

MIT
