# Skill usage logging

This is optional prompt-level observability, not authoritative telemetry.

## Configuration

Effective configuration:

```yaml
observability:
  skill_usage:
    enabled: false
    path: .planning/observability/SKILL_USAGE.csv
    log_implicit: false
```

When disabled, perform no logging work.

## Logging rule

When enabled, append at most one row per selected skill per user turn:

```text
timestamp_utc,skill,invocation,lifecycle_stage,change_id
```

- `timestamp_utc`: ISO 8601 UTC timestamp;
- `skill`: canonical skill name;
- `invocation`: `explicit`, `implicit`, or `unknown`;
- `lifecycle_stage`: current stage or `Unknown`;
- `change_id`: active change ID or `None`.

If the file is missing, initialize it from `.planning/templates/observability/SKILL_USAGE.csv`.

Do not read the existing log merely to append a row. Do not narrate logging. Logging failure is non-blocking and must not alter the operation verdict.

## Limits

Prompt-level logging can miss invocations when a client bypasses repository skills, an agent does not follow the logging instruction, or implicit routing is not observable. Use it for rough frequency counts, not billing, compliance, security, or exact performance measurement.
