# Create a bounded approved change

Mode: Planning.

## Authorization check

Proceed when the user explicitly accepts one or more recommendations, asks to convert them, or directly requests a bounded change. If approval is ambiguous, create a draft proposal only.

## Procedure

1. Read only the relevant project context, source recommendation IDs, and code evidence.
2. Decide whether the direction is best represented by one change or several. Do not force a broad recommendation into one oversized change.
3. Create the next `.planning/changes/active/CHG-NNNN-short-name/` directory and copy all templates.
4. Fill `proposal.md` with outcome, scope, non-goals, constraints, alternatives, source recommendations, coverage intent, and approval record.
5. Fill `specification.md` with requirements, scenarios, acceptance criteria, failure modes, compatibility, assumptions, and open questions.
6. Start `requirements-checklist.md`.
7. Fill `context.md` with the current concise entry point.
8. Leave plan and tasks `Not yet prepared` unless planning was also requested.
9. Update every source recommendation’s `Converted changes` list and status only when the linked change exists.
10. Update `.planning/ACTIVE.md`.
11. Do not implement.

## Many-to-many rule

- Several source recommendations may be listed in one change.
- One recommendation may be linked to several changes.
- Record intended coverage as full or partial.
- Do not mark a source recommendation completed during conversion.

## Output

Summarize scope, source recommendations, coverage, approval state, unresolved decisions, and next permitted action.
