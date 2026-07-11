# Session checkpoint

Use this workflow when the user says any equivalent of:

- `Выполни чекпоинт.`
- `Выполни чекпоинт перед сжатием контекста.`
- `Выполни чекпоинт перед новой сессией.`
- `Prepare a session checkpoint.`
- invokes the logical skill `planning-checkpoint` through the active adapter.

Client-specific aliases such as `/compact`, `/new`, `/clear`, or similar commands may be accepted, but they are adapter syntax rather than core Planning Lite semantics.

A checkpoint preserves resumable state. It is not an implementation step and it does not execute operator interface commands.

## Hard boundary

1. Stop changing production code before starting the checkpoint.
2. Do not execute context compaction, new-session, clear, fork, or other client-interface actions. The operator runs them.
3. Do not load the entire repository or a full raw diff by default.
4. Summarize evidence; do not paste long logs or patches into planning files.
5. If state cannot be established safely, report `Checkpoint incomplete` and explain why.

## Minimum context

Read only:

- `.planning/ACTIVE.md`;
- `.planning/framework/defaults.yml` and `.planning/CONFIG.yml`;
- the active change `context.md`, `tasks.md`, and `progress.md` when a change is active;
- `.planning/control/GIT_CHANGE_REVIEW.md` only if a review trigger is reached.

Use `REPOSITORY_MAP.md` only when paths or symbols required for the next session are unclear.

## Procedure

### 1. Identify the checkpoint target

Record whether the user is preparing for:

- context compaction: same change and usually the same phase;
- a new session: new conversation, change, phase, agent shell, model, or independent review;
- an ordinary durable checkpoint with no immediate interface action.

When a client-specific command was named, preserve it only as an operator hint. Do not make the core state depend on that command existing.

### 2. Reconcile task state

Update the active `tasks.md` honestly:

- mark complete only tasks whose verification passed;
- leave partially completed tasks unchecked;
- name the exact next permitted task;
- record any task blocked by a user decision, failed verification, or plan conflict.

### 3. Update progress

Append one concise checkpoint entry to `progress.md` with:

- work completed since the previous checkpoint;
- files or components affected;
- tests and commands actually run;
- results, including failures;
- amendments, quick fixes, or recommendations created;
- next permitted action.

Do not copy complete command output or full diffs.

### 4. Collect a token-efficient Git summary

Run the cheapest useful commands first, where Git is available:

```bash
git status --short --branch
git diff --stat
git diff --name-status
git diff --cached --stat
git diff --cached --name-status
```

When a previous checkpoint commit is recorded, also inspect the commit range without opening every patch:

```bash
git log --oneline <previous-checkpoint>..HEAD
git diff --stat <previous-checkpoint>..HEAD
git diff --name-status <previous-checkpoint>..HEAD
```

Do not run or paste a full `git diff`, `git show -p`, or repository-wide patch merely because a checkpoint was requested.

Summarize:

- branch and current `HEAD`;
- previous checkpoint commit, if known;
- commits since that checkpoint;
- clean or dirty working tree;
- staged, unstaged, and untracked files;
- approximate file and line totals when available;
- unexpected files or scope;
- whether a Git change review is required.

### 5. Decide whether Git review is required

Route to the logical skill `planning-git-review` or `.planning/control/GIT_CHANGE_REVIEW.md` when a semantic trigger or configured threshold is reached. Do not perform a full review silently inside the checkpoint.

A required review blocks affected implementation, commit, or change closure until resolved, but it does not by itself block a session handoff. Record it as the mandatory first step after compaction or in the new session. A review is not automatically required for every clean atomic commit.

### 6. Update the active context packet

Update `context.md` with:

- current stage and task;
- last verified checkpoint;
- next permitted action;
- implementation authorization state;
- current blockers and pending user decisions;
- exact files, symbols, tests, and document sections the next session should inspect;
- Git state summary and checkpoint commit range;
- whether Git review is required or completed;
- active adapter or model only when a switch is planned or relevant.

Keep the packet below the configured line limit. Link to detailed artifacts instead of copying them.

### 7. Update `.planning/ACTIVE.md`

Record:

- active change or `None`;
- current phase and mode;
- current or next task;
- last checkpoint commit;
- next permitted action;
- mandatory first action after handoff, when any;
- unresolved blockers and approval state.

### 8. Report readiness

Use one of these neutral outcomes:

```text
Checkpoint завершён.
Состояние записано.
Сессия готова к сжатию контекста.
Команду запускает оператор.
```

```text
Checkpoint завершён.
Состояние записано.
Сессия готова к переходу в новую сессию.
Команду запускает оператор.
```

```text
Checkpoint завершён.
Состояние записано.
Обязательный первый шаг после перехода: planning-git-review.
Сессия готова к переходу.
Команду запускает оператор.
```

If the operator named a supported client command, the response may append it as a parenthetical hint, for example `(/new in the active Codex adapter)`. The neutral outcome must remain understandable without it.

Never claim that an operator interface action was executed.
