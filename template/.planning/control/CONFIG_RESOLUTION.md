# Effective configuration

Planning Lite configuration has two layers:

1. `.planning/framework/defaults.yml` is centrally managed and updated with the framework.
2. `.planning/CONFIG.yml` belongs to the project and contains only local overrides.

Resolve configuration as a recursive mapping merge:

```text
effective configuration = framework defaults + project overrides
```

A value from `CONFIG.yml` replaces the matching default. Unmentioned defaults remain active.
Do not copy all defaults into `CONFIG.yml`; that would freeze the project on old framework values.

When a workflow says “read the effective configuration”, read `defaults.yml` first and then the relevant override keys from `CONFIG.yml`.
