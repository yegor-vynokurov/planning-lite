# Миграция на Planning Lite 4.2

## Что меняется

- Жизненный цикл change стал явной state machine: `Discovery → Definition → Planning → Readiness → Execution → Verification → Closure`.
- План теперь требует отдельного подтверждения пользователя перед readiness audit.
- Задачи используют `tracer bullet` или `expand-contract`, blocking edges, verification seams и blast radius.
- Critic разделяет вопросы на проверяемые facts и пользовательские decisions.
- Audit разделён на spec conformance и standards conformance.
- Добавлены условно загружаемые инженерные disciplines.
- Response economy стала строже: нет рутинного рассказа о tool calls и повторения плана.
- Добавлено необязательное prompt-level логирование вызовов skills.

## Установленный проект

Безопасный managed overlay не заменяет `.planning/ACTIVE.md`, `project/*` и живые changes.

После обновления первый planning, readiness, execution, review, closure или checkpoint workflow должен:

1. прочитать `control/CHANGE_LIFECYCLE.md`;
2. добавить отсутствующие lifecycle fields в `ACTIVE.md` targeted merge;
3. сохранить существующий active change и авторизацию;
4. не переписывать заполненные change-файлы новыми templates.

Старые `plan.md`, `tasks.md`, `readiness.md` и `review.md` остаются допустимыми. Новые поля добавляются только когда соответствующий workflow действительно обновляет файл.

## Domain language

Существующий project-owned `GLOSSARY.md` не перезаписывается overlay. При необходимости попросите planning-dialogue привести его к новой таблице, сохранив все термины.

## Skill statistics

По умолчанию выключены. Для эксперимента добавьте в `.planning/CONFIG.yml`:

```yaml
observability:
  skill_usage:
    enabled: true
    path: .planning/observability/SKILL_USAGE.csv
    log_implicit: false
```

Это best-effort статистика, а не точная телеметрия. Логирование может пропускаться клиентами или агентами и создаёт небольшие изменения CSV при каждом вызове skill.
