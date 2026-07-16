# Configuration resolution

Effective configuration is the recursive merge of:

1. `.planning/framework/defaults.yml`;
2. `.planning/CONFIG.yml` project overrides.

Project overrides win. Missing keys inherit defaults.

Do not copy all defaults into `CONFIG.yml`. Keep overrides small so centrally improved defaults remain effective.

Configuration does not override explicit user instructions, hard approval boundaries, or repository safety rules.
