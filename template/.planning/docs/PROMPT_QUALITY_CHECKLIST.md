# Prompt quality checklist

Use when changing Planning Lite instructions, modes, skills, workflows, templates, or routing.

## Operation contract

Every functional workflow must state:

- entry condition;
- required inputs;
- allowed writes;
- authority boundary;
- observable completion criterion;
- next legal transition.

## Single-source test

Each normative rule has one authoritative source. Modes, skills, prompts, and READMEs should link to it rather than restate it. Templates define fields; workflows define when and how fields change.

## No-op test

For every sentence ask: if this sentence were removed, would agent behavior change in an observable way?

- If no, delete it.
- If it only explains a term, move it to a discipline or reference.
- If it repeats another rule, replace it with a link.

## Leading-word test

A specialized term is allowed only when:

- it is defined once;
- it selects a useful engineering pattern;
- it is used consistently;
- it replaces several ambiguous instructions;
- misuse would be detectable.

Do not add jargon for tone.

## Progressive-disclosure test

- Tier 0 remains small.
- One operation loads one workflow.
- A discipline is conditional, not global.
- Rare branches live in dedicated workflows or references.
- Archives, logs, old changes, and all prompts are not loaded by default.

## Lifecycle consistency

For every stage verify:

- required artifacts exist;
- status vocabulary matches templates;
- entry and exit gates agree with `APPROVAL_GATES.md`;
- workflows update `.planning/ACTIVE.md` consistently;
- checkpoint preserves stage;
- closure resets state only after integrity checks.

## Response-economy test

Remove greetings, task restatement, routine tool narration, repeated plans, unchanged facts, full successful logs, and generic summaries. Preserve decisions, evidence, failures, uncertainty, risks, and exact commands or errors.

## Validation

Check internal links, YAML, scaffold completeness, ownership paths, managed-overlay safety, UTF-8, line endings, checksums, tests, and smoke update before release.
