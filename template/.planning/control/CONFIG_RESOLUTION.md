# Configuration resolution

Effective configuration is the recursive merge of:

1. `.planning/framework/defaults.yml`;
2. `.planning/CONFIG.yml` project overrides.

Project overrides win. Missing keys inherit defaults.

Do not copy all defaults into `CONFIG.yml`. Keep overrides small so centrally improved defaults remain effective.

Configuration does not override explicit user instructions, hard approval boundaries, or repository safety rules.

## Project policy namespace

The effective `project_policy` block is the only policy namespace for the
topology Change. Defaults remain managed here; project-specific overrides live
in the project-owned `.planning/CONFIG.yml`. It contains topology and safety
values only. It is not copied into lifecycle, Change, task, receipt, memory, or
recommendation artifacts.

## Central local operational root

When Planning Lite runs from the central source repository, persistent
Planning Lite-managed operational data is routed beneath the repository-local
`.local/` root. The central root is explicit via `PLANNING_LITE_CENTRAL_ROOT`
or derived from the central source checkout; there is no implicit
`Path.home()`, `APPDATA`, `USERPROFILE`, `XDG_CONFIG_HOME`, current-directory,
temporary, or sibling-repository fallback.

The canonical local routes are `config.toml`, `registry/`,
`state/projects/<project-id>/`, `inbox/roadmaps/`, `inbox/recommendations/`,
`work/compiled-prompts/`, `work/experiments/`, and `cache/`. Routes are created
lazily by the operation that owns them. An unavailable or unknown route fails
closed with `ARTIFACT_ROUTING_UNRESOLVED`.

Consumer-owned lifecycle, configuration, and project state remain in that
consumer's `.planning/` tree. The local operational root is not a second
consumer policy authority and must not be used to overwrite project-owned
files.
