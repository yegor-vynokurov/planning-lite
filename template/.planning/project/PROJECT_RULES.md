# Project rules and guardrails

Status: `Template - adapt to repository`
Last reviewed: `YYYY-MM-DD`

These are durable constraints across changes. Keep them testable, concise, and project-specific.

## Data safety and reversibility

- Existing user data and generated artifacts must not be overwritten by default.
- Long-running workflows should be resumable when practical.
- Partial output must not be treated as successful output.
- Destructive operations require explicit approval, backup, and recovery steps.
- Schema or format changes require compatibility or migration planning.

## Scope and interaction discipline

- Implement only approved change scope or a qualifying explicit quick fix.
- New ideas discovered during implementation become recommendations unless necessary for correctness or safety.
- Prefer the smallest coherent change over speculative architecture.
- Do not rewrite working components merely for stylistic preference.
- Questions and planning requests do not authorize production-code edits.

## Code quality

- Follow the repository’s established formatter, linter, type checker, tests, and idioms before generic style advice.
- Prefer readable code with clear responsibilities and unsurprising control flow.
- Apply DRY, KISS, YAGNI, and SOLID where they reduce risk or complexity, not as reasons to create abstractions prematurely.
- For Python, follow PEP 8 and idiomatic Python unless a documented repository convention overrides it.
- Preserve public contracts unless a change explicitly approves modifying them.

## Reliability and errors

- Failures must be observable and actionable.
- Recovery and repeated execution behavior must be defined for stateful workflows.
- Idempotency expectations must be explicit.
- Silent data loss and silent partial success are unacceptable.

## Testing and verification

- Bug fixes should include regression coverage where practical.
- Every task and quick fix must define a verification method.
- Tests, linting, type checks, builds, and sample runs must be reported accurately.
- Network-dependent and slow tests should be identifiable.

## Documentation

- Public functions and non-obvious internal functions should document their role in the end-to-end flow, not merely restate parameters and return values.
- Documentation should explain why a component exists, inputs and outputs, state changes, failure behavior, and relationship to neighboring stages where that context is not obvious.
- README examples must stay runnable or be clearly marked illustrative.
- Architecture and workflow documentation must be updated when responsibilities or data flow change.

## Interfaces and usability

- Core functionality should have an interface appropriate to intended users, such as CLI, API, notebook, library surface, or UI.
- Interface ideas remain recommendations until product need and scope are approved.
- Error messages should help the intended user recover.

## Dependencies and environment

- Prefer existing dependencies unless a new dependency has a clear benefit.
- Pin or constrain versions when reproducibility requires it.
- Record platform assumptions and external tools.
- Do not add online services when a local workflow is a stated constraint.

## Security, privacy, and licensing

- Do not expose credentials, personal data, or restricted datasets.
- New dependencies and datasets require license and provenance review when relevant.
- External side effects require explicit authorization.

## Version-control safety

- Preserve unrelated user edits.
- Avoid destructive commands such as hard resets unless explicitly authorized.
- Keep changes reviewable and logically grouped.

## Project-specific additions

- `Add rules discovered during bootstrap and confirmed by the user.`
