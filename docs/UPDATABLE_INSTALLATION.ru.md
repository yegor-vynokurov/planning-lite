# Установка Planning Lite с поддержкой обновлений

Этот документ нужен не для обычной разовой установки промптов, а для режима, в котором:

- команда `planning-lite` постоянно доступна на компьютере;
- установленные в проекты управляющие файлы можно обновлять из центрального репозитория;
- версии CLI и шаблона фиксируются Git tags;
- изменения можно предварительно просматривать и коммитить отдельно.

Для простой установки без обслуживания используйте одну команду из корневого README:

```powershell
uvx --from "git+https://github.com/yegor-vynokurov/planning-lite.git" planning-lite install .
```

## 1. Установка `uv`

Проверка:

```powershell
uv --version
```

### Windows

Через WinGet:

```powershell
winget install --id=astral-sh.uv -e
```

Или официальный standalone installer:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Linux и macOS

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Без `curl`:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

## 2. Установка постоянной CLI-команды

Выберите существующий стабильный tag, например `v3.1.0`:

```powershell
uv tool install "git+https://github.com/yegor-vynokurov/planning-lite.git@v3.1.0"
```

Проверка:

```powershell
planning-lite --version
```

### Если PowerShell не находит `planning-lite`

Добавьте каталог инструментов `uv` в конфигурацию оболочки:

```powershell
uv tool update-shell
```

Затем:

1. закройте встроенные терминалы VS Code;
2. откройте новый терминал;
3. если команда всё ещё не видна, закройте **все окна VS Code**;
4. запустите VS Code заново.

Новые терминалы наследуют `PATH` от уже запущенного процесса VS Code, поэтому закрытия одной вкладки иногда недостаточно.

Временно добавить путь в текущую PowerShell-сессию можно так:

```powershell
$env:Path = "$HOME\.local\bin;$env:Path"
planning-lite --version
```

Посмотреть каталог исполняемых файлов:

```powershell
uv tool dir --bin
```

## 3. Первое подключение обновляемого режима

Целевой проект должен находиться под Git. Перед подключением желательно иметь чистое рабочее дерево:

```powershell
cd D:\documents\my-project
git status
```

Подключение:

```powershell
planning-lite adopt . --agent codex --vcs-ref v3.1.0
planning-lite doctor .
```

Затем проверьте и отдельно закоммитьте добавленные файлы:

```powershell
git diff --stat
git add AGENTS.md .agents .planning .copier-answers.planning-lite.yml
git commit -m "Adopt Planning Lite v3.1.0"
```

`adopt` отличается от простой команды `install` тем, что требует Git-дисциплину и сразу ведёт пользователя по обслуживаемому сценарию.

## 4. Обновление CLI и файлов проекта

Это две разные операции.

```text
uv tool install ...
    обновляет исполняемую команду planning-lite на компьютере

planning-lite update .
    обновляет управляющие файлы внутри конкретного проекта
```

### Обновить CLI до нового tag

Если CLI установлена из точного tag, например `@v3.1.0`, она останется на этой версии. Новый tag в GitHub не заменит установленную программу автоматически.

Для перехода на `v3.1.1` повторите установку с новым tag:

```powershell
uv tool install "git+https://github.com/yegor-vynokurov/planning-lite.git@v3.1.1"
planning-lite --version
```

Повторно выполнять `uv tool update-shell` обычно не нужно: путь к executable остаётся тем же. Перезапуск VS Code также обычно не требуется. Сначала достаточно открыть новый терминал.

Проверить установленный источник и ограничения:

```powershell
uv tool list --show-version-specifiers --show-paths
```

### Обновить один проект

Перейдите в проект и убедитесь, что дерево чистое:

```powershell
cd D:\documents\my-project
git status
```

Предварительный просмотр:

```powershell
planning-lite check .
```

Применение в отдельной ветке:

```powershell
git switch -c chore/update-planning-lite
planning-lite update .
planning-lite doctor .
git status
git diff --stat
```

Разрешите конфликты Copier, выполните проверки проекта и закоммитьте обновление framework отдельно от продуктового кода.

`planning-lite update .` читает источник и установленный tag из:

```text
.copier-answers.planning-lite.yml
```

Повторно выполнять `configure` обычно не требуется.

## 5. Необязательное переопределение источника

По умолчанию используется официальный репозиторий:

```text
https://github.com/yegor-vynokurov/planning-lite
```

Для fork:

```powershell
planning-lite configure `
  --template-source https://github.com/OTHER_ACCOUNT/planning-lite
```

Для локальной экспериментальной копии:

```powershell
planning-lite configure `
  --template-source D:\documents\planning-lite
```

Для одной команды без сохранения настройки:

```powershell
planning-lite adopt . `
  --template-source D:\documents\planning-lite `
  --vcs-ref HEAD `
  --agent codex
```

## 6. Разработка центрального репозитория

Центральный репозиторий клонируется только для изменения самого Planning Lite:

```powershell
git clone https://github.com/yegor-vynokurov/planning-lite.git
cd planning-lite
uv sync
uv run planning-lite --version
uv run pytest
uv run python scripts/test_template_update.py
```

Внутри центрального репозитория `configure` не нужен: CLI распознаёт локальные `copier.yml` и `template/`.

Релизный процесс описан в `docs/OPERATOR_WORKFLOW.ru.md`. Planning Lite использует Git tag как единственный источник релизной версии.

## 7. Краткая карта команд

```text
uvx ... planning-lite install .
    простая разовая установка без постоянной CLI

uv tool install ...@vX.Y.Z
    постоянная установка или смена версии CLI

planning-lite adopt .
    первое подключение обслуживаемого режима

planning-lite check .
    предварительный просмотр обновления

planning-lite update .
    обновление файлов в текущем проекте

planning-lite doctor .
    проверка структуры после adopt или update

planning-lite configure ...
    необязательное переопределение источника шаблона
```
