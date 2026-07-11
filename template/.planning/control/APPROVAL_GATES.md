# Approval gates

## Gate A: idea or recommendation

Allowed:

- discussion, criticism, investigation;
- assessment and recommendation files;
- priority and sequencing proposals.

Not allowed:

- production code;
- executable tasks presented as approved work;
- marking a recommendation `Accepted` without the user’s decision.

## Gate B: accepted direction

The user accepts one or more recommendations or directly requests a bounded change.

Allowed:

- create a draft or approved `CHG-*` folder according to the user’s wording;
- define outcome, scope, non-goals, requirements, and acceptance criteria.

Not allowed:

- implementation merely because the direction was accepted.

## Gate C: approved change and planning

The proposal records approval and material product decisions are resolved or explicitly delegated as assumptions.

Allowed:

- interactive planning;
- plan, tasks, ADRs, and verification design;
- planning-document amendments.

Not allowed:

- production code unless the user directly authorizes implementation.

## Gate D: execution authorization

Required conditions:

- proposal is `Approved`;
- pre-implementation audit has no unresolved critical blocker;
- `.planning/ACTIVE.md` points to the change;
- the user uses a direct implementation instruction.

Allowed:

- approved tasks and verification;
- implementation-detail amendments that do not change scope or acceptance criteria;
- creation of follow-up recommendations.

## Gate Q: quick fix

A full change folder may be skipped only when all Quick fix criteria pass and the user directly requests the edit. The edit must be logged and verified.

## Approval language examples

Direction only:

- “Рекомендацию принимаю.”
- “Этим стоит заняться.”

Planning authorization:

- “Создай change и подготовь спецификацию и план. Код не меняй.”
- “Уточни scope и разбей на задачи.”

Execution authorization:

- “План согласован, выполняй.”
- “Реализуй задачи T003–T006.”
- “Пиши код по утверждённому плану.”

Quick-fix authorization:

- “Это маленькая правка: исправь регистр и проверь тест.”
- “Сделай быструю правку без отдельного change, если она проходит критерии quick fix.”
