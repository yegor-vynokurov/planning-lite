# CHG-CAMPAIGN-BUDGET-ADMISSION-001

Статус: production capability candidate, без нового Campaign execution.

## Дефект

R3 обнаружил lifecycle gap: `attempt_started` проверял только, что Campaign budget ещё
не исчерпан, но не требовал reservation/projected cost для следующего дорогого attempt.
В результате A03 стартовал при 335030 оставшихся токенах и фактически потратил 561943.

## Исправление

1. В CampaignManifest добавлена backward-compatible optional policy:

   ```json
   "attempt_budget_admission": {"required": true}
   ```

2. Добавлены `AttemptBudgetReservation`, `validate_attempt_budget_reservation()` и
   `prepare_attempt_budget_admission()`.
3. Admission привязан к manifest SHA, journal head, candidate/attempt identity,
   reservation и exact remaining-budget snapshot.
4. `start_campaign_suite_attempt()` для strict Campaign требует reservation и сначала
   проверяет её read-only, до auto-registration writes.
5. Core повторно валидирует admission при append `attempt_started`, поэтому forged или
   stale payload не может обойти gate.
6. Wall-clock значения канонизируются до 6 знаков, чтобы admission identity не зависела
   от IEEE-754 noise.
7. Completion не блокируется из-за post-hoc перерасхода: фактический sunk cost обязан
   быть записан. После исчерпания budget следующий attempt fail-closed не стартует.

## Совместимость

Исторический r3 Campaign не меняется. Existing schema-v1 manifest hash остаётся прежним,
если optional policy отсутствует. Existing started/completed suite attempts остаются
идемпотентно читаемыми даже без admission, потому что admission требуется только перед
созданием нового attempt.

## Governance boundary

Этот change не создаёт новый Campaign, не запускает Harness/LLM, не меняет stopped r3,
не делает candidate promotion и не является post-stop independent-review handoff.
