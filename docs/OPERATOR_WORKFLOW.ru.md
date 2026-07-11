# Операторский workflow

## 1. Изменение центрального Planning Lite

1. Создать ветку в центральном репозитории.
2. Менять файлы в `template/` и при необходимости CLI.
3. Добавлять описание изменений в раздел `## Unreleased` файла `CHANGELOG.md`.
4. Проверить template smoke test и закоммитить изменения.
5. Перейти на чистую ветку `main`.
6. Запустить `uv run planning-lite release patch|minor|major`.
7. Проверить созданный release-коммит и tag.
8. Вручную отправить `main` и tag в remote.

Номера версий в `pyproject.toml`, `__init__.py` и template-файлах вручную не редактируются: единственным источником является Git tag.

## 2. Обновление одного рабочего проекта

1. Завершить или checkpoint текущую агентную работу.
2. Убедиться, что рабочее дерево чистое.
3. Создать отдельную ветку обновления Planning Lite.
4. Выполнить `planning-lite check .`.
5. Выполнить `planning-lite update .`.
6. Разрешить конфликты только в managed-файлах.
7. Выполнить `planning-lite doctor .`.
8. Проверить, что project-owned файлы сохранились.
9. Закоммитить обновление отдельно от продуктового кода.

## 3. Что редактировать где

В центральном репозитории:

- control policies;
- modes and prompts;
- canonical skills and adapters;
- reusable templates;
- framework defaults.

В рабочем проекте:

- project charter and completion criteria;
- repository map and architecture snapshot;
- local rules and configuration overrides;
- recommendations, changes, decisions, progress, and reviews.

## 4. Конфликт при обновлении

Не выбирайте автоматически только ours или theirs.

- Если файл managed, обычно нужно перенести локальную полезную правку в central repo или project-specific instructions.
- Если файл project-owned, Copier не должен был его менять. Сначала проверьте ownership policy и шаблон.
- Если конфликт повторяется в нескольких проектах, это признак неправильной границы владения.
