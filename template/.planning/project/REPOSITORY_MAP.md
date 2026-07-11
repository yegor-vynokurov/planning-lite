# Repository map

This is a compact, durable index of the codebase. It prevents repeated repository-wide discovery in later sessions.

Keep it factual, path-oriented, and concise. Do not copy source code or duplicate the architecture overview.

## Freshness

- Last verified date: `YYYY-MM-DD`
- Last verified revision / commit: `<hash or working-tree state>`
- Verification scope: `Full bootstrap / targeted refresh`
- Known stale areas: `None / paths`

## Repository shape

| Path | Responsibility | Important entry points / symbols | Generated / vendored | Notes |
|---|---|---|---|---|
| | | | `No` | |

## Runtime entry points

| Entry point / command | Path or symbol | Purpose | Main downstream flow |
|---|---|---|---|
| | | | |

## Major flows

| Flow | Start | Main modules / symbols | Persistent state / outputs | Tests |
|---|---|---|---|---|
| | | | | |

## Test and verification map

| Area | Test path / command | What it proves | Typical narrow command |
|---|---|---|---|
| | | | |

## Configuration, data, and generated artifacts

| Path / format | Producer | Consumer | Safe to edit manually | Notes |
|---|---|---|---|---|
| | | | | |

## High-risk or cross-cutting areas

- `Path / symbol :: why changes here require wider verification`

## Targeted refresh rules

Update only the affected rows after ordinary changes. Perform broader rediscovery only when:

- major directories, entry points, or runtime flows changed;
- the map conflicts with observed code;
- the recorded revision is too old for the requested work;
- a current-state audit explicitly requires repository-wide coverage.
