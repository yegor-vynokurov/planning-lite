# Experiment Campaign Core: Release Integration Candidate 0.1

Статус: **integration candidate, не релиз**.

Этот слой переносит validated цепочку CHG-E1.1–E1.6 из Context Eval Harness в основной Python-дистрибутив Planning Lite как opt-in runtime.

## Граница интеграции

В продукт входят:

- immutable/self-hashed CampaignManifest;
- проверка frozen inputs;
- append-only hash-linked journal;
- budget/stop policy и deterministic ResumeCapsule;
- suite-attempt adapter contract;
- Candidate Review Gate;
- Review Receipt + independent-review handoff;
- Independent Review Decision Gate;
- Campaign Completion Seal + release handoff;
- отдельный CLI `planning-lite-campaign`.

В integration candidate **не входят**:

- Context Pilot;
- `evals/` и lifecycle-status fixture;
- Codex runner и routing-experiment scripts;
- CHG validation reports и smoke evidence;
- `.planning-lab/`;
- изменения `template/`, `copier.yml`, `AGENTS.md`;
- release promotion controller.

## Почему отдельный CLI

`planning-lite-campaign` не подключается к обычному `planning-lite` CLI и ничего не записывает в пользовательский проект при установке. Campaign artifacts появляются только когда оператор явно вызывает campaign command и передаёт `--campaign-root`.

Это сохраняет существующую установку Planning Lite и не добавляет `.campaign`, `.planning-lab` или другие experiment-файлы в Poker/обычные проекты.

## Release boundary

Даже после `candidate_kept` и `campaign_completed`:

```text
release_status = not_requested
central_planning_lite_mutated = false
next_release_action = await_release_gate
```

Release Integration Candidate 0.1 не меняет версию, не создаёт tag и не авторизует promotion.
