# Миграция к архитектуре 4.0

Основное изменение: повторяющиеся инструкции собраны в функциональные workflow под `.planning/control/`. Modes, skills и numbered prompts стали короткими маршрутизаторами.

Добавлены канонические документы:

- `STATE_OWNERSHIP.md`;
- `RECOMMENDATION_LIFECYCLE.md`;
- `CHANGE_DEFINITION.md`;
- `CHANGE_PLANNING.md`;
- `CHANGE_READINESS.md`;
- `CHANGE_EXECUTION.md`;
- `CHANGE_AMENDMENT.md`;
- `CHANGE_CLOSURE.md`;
- `PROJECT_STATE_REFRESH.md`.

В активных change появился `readiness.md`. При переносе существующего проекта не перезаписывайте project-owned данные вслепую. Для центрального шаблона можно заменить всю `template/.planning`; для установленного проекта безопаснее обновлять managed paths и отдельно мигрировать активные change.
