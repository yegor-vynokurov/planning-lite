# Ремонт существующих active changes после обновления

После установки managed overlay попросите агента в Planning mode:

```text
Прочитай AGENTS.md, .planning/ACTIVE.md и .planning/control/CHANGE_SCAFFOLD.md.
Проверь все папки .planning/changes/active/CHG-*.
Добавь только отсутствующие файлы из .planning/changes/templates/.
Не перезаписывай заполненные документы.
Удали вложенный .gitkeep только из конкретной папки change.
Покажи итоговую проверку scaffold. Программный код не меняй.
```

Для change, который находится только на стадии definition, заполненными должны быть `proposal.md`, `specification.md` и `requirements-checklist.md`; остальные файлы должны существовать в initialized template state.
