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
