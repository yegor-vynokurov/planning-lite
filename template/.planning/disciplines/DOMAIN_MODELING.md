# Domain modeling discipline

Load when terminology, entity boundaries, states, or invariants are causing ambiguity.

Use `.planning/project/GLOSSARY.md` as the project-owned domain-language record.

## Canonical term

A useful term has:

- one project-specific definition;
- explicit invariants or state rules;
- aliases that should be avoided;
- code or document anchors;
- an owner or source.

Prefer canonical project terms in specifications, code names, tests, logs, and user-facing language. Do not introduce domain jargon merely because it sounds precise.

## Investigation

Look for:

- one word used for several concepts;
- several words used for one concept;
- state transitions hidden in booleans or strings;
- code names that disagree with user language;
- entities that own no clear invariants;
- invariants duplicated across unrelated functions.

Repository facts must be inspected. Naming, product meaning, and scope choices remain user decisions.

## Completion criterion

A terminology change is ready when the canonical term, definition, invariants, aliases, migration impact, and code anchors are explicit. Update the glossary only for durable language, not temporary implementation labels.
