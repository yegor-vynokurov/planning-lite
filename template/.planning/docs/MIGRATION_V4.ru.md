# Миграция к архитектуре 4.x

Основное изменение 4.0: повторяющиеся инструкции собраны в функциональные workflow под `.planning/control/`. Modes, skills и numbered prompts стали короткими маршрутизаторами.

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

Следующий совместимый ремонт добавляет:

- `PROJECT_BOOTSTRAP.md`: классификация project-owned документов и безопасная стратегия полной материализации или targeted merge;
- `CHANGE_SCAFFOLD.md`: полный каркас change создаётся сразу, а содержимое созревает по стадиям;
- `.planning/templates/project/`: managed pristine copies для безопасного сравнения без перезаписи живых project-owned документов.

В активных change используется `readiness.md`. При переносе существующего проекта не перезаписывайте project-owned данные вслепую. Для центрального шаблона можно заменить всю `template/.planning`; для установленного проекта обновляйте только managed paths и отдельно запустите scaffold repair для уже существующих active changes.
