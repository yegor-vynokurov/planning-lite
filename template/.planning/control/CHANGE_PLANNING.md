# Change planning

Use in Planning mode for an approved change. Do not edit production code.

Follow `CHANGE_LIFECYCLE.md` and `CHANGE_SCAFFOLD.md`. Load `disciplines/CODEBASE_DESIGN.md` for architectural work or `disciplines/DELIVERY_SLICES.md` for task decomposition. Load both only when necessary.

## Minimum context

Read `.planning/ACTIVE.md`, proposal, specification, requirements checklist, relevant project rules, repository map, and only the code or tests needed to resolve planning facts.

Verify and, when safe, repair the complete scaffold before reading or updating `context.md`. Missing initialized files may be restored from canonical templates. Populated records must be preserved.

For a traversability-aware Change, also read the durable
`.planning/project/CRITICAL_JOURNEYS.md`, the Definition's journey block, the
Specification's ordered seams, and any evidence-backed bypass record.

## Procedure

1. Verify that the proposal is `Approved` and lifecycle state is `Planning`.
2. Resolve repository facts; surface unresolved product, scope, and architecture decisions to the user.
3. Fill `plan.md` with exact paths, symbols, module interfaces, seams, adapters, state transitions, data, migration, recovery, compatibility, tests, documentation, verification commands, blast radius, and rollback.
4. Prefer the smallest coherent design compatible with the existing architecture. Classify generic `helper` roles precisely.
4a. Bind every affected journey ID, ordered seam, expected state delta, task/proof IDs, and the early System Walking Skeleton handoff. Missing carrier data or an unbound applicability choice is an architecture STOP, not an invitation to invent a second authority or reinterpret the Definition.
5. Choose a delivery strategy:
   - `Tracer bullet` for the smallest end-to-end behavioral slice;
   - `Expand-contract` for migrations or broad compatibility transitions.
6. Fill `tasks.md` with dependency-ordered outcomes, slice type, blocking edge, verification seam, blast radius, and status.
7. Map every requirement and acceptance criterion to plan sections and tasks.
8. Record durable architectural decisions separately when needed.
9. Initialize or update `context.md`.
10. Mark `plan.md` as `Draft`, set `Planning / Awaiting approval`, and ask the user to approve or revise the plan.

## Plan approval

Only explicit user approval changes `plan.md` to `Approved`. After approval, transition to `Readiness / In progress` and set the next gate to readiness audit.

Do not hide uncertainty, compatibility work, blocking edges, or recovery behavior inside generic implementation tasks.

## Deterministic Operation Guidance binding

At the existing legal Plan-approval transition, the managed current-action
projection may emit the exact identity `RUN_FORMAL_READINESS`. This is a finite
consumer guidance identity for the Readiness route; it is not an alias for a
central project-specific action, does not create state, and does not authorize
implementation. `.planning/ACTIVE.md` remains the authority for the actual
`Next permitted action` value.
