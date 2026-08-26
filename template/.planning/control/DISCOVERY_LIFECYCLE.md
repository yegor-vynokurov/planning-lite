# Discovery Lifecycle

Discovery is a durable project observation worth preserving before an action,
Recommendation, Change, or Roadmap decision is justified.

A Discovery records **what was observed**. It does not itself propose or
authorize execution.

## Identity

Use project-local monotonically allocated identifiers:

```text
DISC-NNNN
```

Do not use UUIDs, content hashes, global identifiers, or semantic-unit
decomposition for Discovery v1.

## Required fields

Every Discovery item contains:

```text
id
title
status
observation
evidence / source references
created
recommendation_links
resolution
```

`recommendation_links` may be empty.
`resolution` may be empty while status is `OPEN`.

## Status

The complete Discovery v1 status vocabulary is:

```text
OPEN
RESOLVED
SUPERSEDED
```

- `OPEN`: observation remains current and has no terminal disposition.
- `RESOLVED`: observation remains historically valid and required follow-up or
  disposition is accounted for.
- `SUPERSEDED`: later evidence replaces or corrects the observation.

There is no `ABSORBED` Discovery status.

## Discovery is not Recommendation

```text
Discovery status != Recommendation status
Discovery status != implementation authority
```

An observation-only Discovery may remain useful without becoming a
Recommendation.

If follow-up produces a governed Recommendation or repair, record the
relationship in `recommendation_links` and/or `resolution`. Do not turn
Discovery into a parallel Recommendation lifecycle.

## Execution authority

A Discovery MUST NOT by itself:

- authorize implementation;
- create or approve a Change;
- promote a Recommendation;
- establish Roadmap priority;
- mutate current direction;
- authorize release.

Executable authority continues to come from the existing Planning Lite
approval and Change lifecycle.

## Registry ownership

Framework-managed guidance:

```text
.planning/discoveries/README.md
.planning/discoveries/TEMPLATE.md
```

Project-owned durable state:

```text
.planning/discoveries/INDEX.md
.planning/discoveries/items/**
```

Framework updates may refresh managed guidance. They must preserve an existing
project-owned Discovery index and items.
