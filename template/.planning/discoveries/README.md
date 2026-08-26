# Discoveries

This registry preserves durable observations before an action or Recommendation
is justified.

Use a Discovery when evidence is worth keeping but the correct response is not
yet an approved executable decision.

## Ownership

Framework-managed:

```text
.planning/discoveries/README.md
.planning/discoveries/TEMPLATE.md
```

Project-owned:

```text
.planning/discoveries/INDEX.md
.planning/discoveries/items/**
```

Existing project-owned Discovery history must survive Planning Lite updates.

## Capture workflow

1. Read `INDEX.md`.
2. Allocate the next project-local `DISC-NNNN` identifier.
3. Copy `TEMPLATE.md` to `items/DISC-NNNN-<short-name>.md`.
4. Record the item in `INDEX.md`.
5. Keep status within `OPEN | RESOLVED | SUPERSEDED`.
6. Link Recommendations only when a governed Recommendation exists.
7. Record terminal accounting in `resolution`.

Observation-only capture has no executable authority.

For lifecycle semantics, read:

```text
.planning/control/DISCOVERY_LIFECYCLE.md
```
