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

## Attempt budget admission (CHG-CAMPAIGN-BUDGET-ADMISSION-001)

Новые Campaign могут включить строгую admission policy в manifest:

```json
"attempt_budget_admission": {
  "required": true
}
```

Для такого Campaign `attempt_started` разрешён только с self-hashed `budget_admission`,
который привязан к текущему `manifest_sha256`, текущему journal head, candidate/attempt
identity и снимку оставшегося token/wall-clock budget.

Balanced-suite adapter принимает явный `AttemptBudgetReservation`:

```python
AttemptBudgetReservation(
    total_tokens=600000,
    wall_clock_seconds=8100.0,
    basis="governed-upper-bound-v1",
)
```

Admission выполняется **до** дорогого attempt. Если reservation превышает оставшийся
frozen Campaign budget, новый `attempt_started` не записывается.

Backward compatibility намеренная:

- historical manifests без `attempt_budget_admission` сохраняют прежний manifest SHA;
- historical journals без `budget_admission` продолжают читаться;
- idempotent replay уже существующего `attempt_started`/`attempt_completed` остаётся доступным;
- strict policy применяется только к новым attempts в Campaign, где она явно включена.

Completion остаётся truthful sunk-cost accounting. Если реальный runtime неожиданно
превысил reservation, `attempt_completed` не скрывает и не отбрасывает фактические
metrics. После такого completion новый attempt всё равно не сможет стартовать, если
фактический Campaign budget уже исчерпан.

## Historical attempt evidence reconciliation

Для legacy Campaign, где исторический `attempt_completed` уже существует, но не содержит
production-compatible balanced-suite projection, Campaign Core поддерживает append-only
`attempt_evidence_reconciled`. Reconciliation привязывает candidate/attempt к точному
историческому completion sequence и event SHA, а также к terminal suite identity и шести
sealed evidence SHA-256.

Исторический `attempt_completed` не переписывается. Reconciliation не меняет attempt/token/
wall-clock accounting и не переинтерпретирует scientific outcome. Candidate Review использует
валидный reconciliation event только как provenance overlay для соответствующего legacy
completion; native completions с уже встроенной suite provenance не reconciliate-ятся.

Production API:

```python
from planning_lite.campaign import reconcile_completed_attempt_suite_evidence
```
