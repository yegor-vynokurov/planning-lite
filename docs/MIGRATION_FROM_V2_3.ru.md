# Переход с распакованного Planning Lite v2.3

Текущую распакованную папку лучше считать прототипом, а не превращать её вручную в template по частям.

## Рекомендуемый путь

1. Сохранить старую папку как резервную копию.
2. Распаковать новый `planning-lite-central-repo` в отдельную папку.
3. Открыть новую папку во VS Code.
4. Инициализировать в ней Git и создать первый tag.
5. Дальнейшие изменения управляющих prompts делать в `template/`, а не в старом корне v2.3.

## Что куда переехало

- старый полный `AGENTS.md` → `template/.planning/control/ROOT_ROUTER.md`;
- новый `template/AGENTS.md` → короткий локальный bridge;
- старый `CONFIG.yml` → `template/.planning/framework/defaults.yml`;
- новый `template/.planning/CONFIG.yml` → только project overrides;
- содержимое v2.3 → в основном внутрь `template/`;
- установка и обновление → `src/planning_lite/cli.py` + `copier.yml`.

## Не копируйте `template/` вручную

После создания центрального Git remote используйте:

```powershell
planning-lite adopt D:\projects\target-project --vcs-ref v3.0.0
```

И затем:

```powershell
planning-lite check D:\projects\target-project
planning-lite update D:\projects\target-project
```
