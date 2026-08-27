# Project Survey

- Status: `DRAFT`
- Reflects revision:
- Survey scope:
- Evidence sources:
- Refresh condition:

`SURVEY = AS-IS EVIDENCE`.

`TARGET = TO-BE ACCEPTED INTENT`.

This assessment is a bounded evidence snapshot. It does not own or replace
`CURRENT_STATE`, `CURRENT_CAPABILITY_ASSESSMENT`, `CAPABILITY_MODEL`, `GAP_MAP`,
`TARGET_STATE`, or `ROADMAP`.

Use it only when the current capability assessment needs a bounded, fresh view of
repository/runtime structure. Routine or small work does not require a Project
Survey.

## Evidence notation

Use the lightest evidence label that keeps claims honest:

```text
OBSERVED
INFERRED
UNKNOWN
```

- `OBSERVED`: supported by cited current repository/runtime evidence.
- `INFERRED`: a bounded interpretation of observed evidence; state the basis.
- `UNKNOWN`: evidence is absent, contradictory, outside scope, or not yet inspected.

Do not convert observed implementation into claims about historical intent.

## System boundaries

## Components / modules

## Datastores / durable state

## External integrations

## Main execution paths

## Build / test / run commands

## Important conventions and source evidence

## Material constraints

## Relevant debt

## Reusable assets

## Unknown / not yet observed

## Freshness / reuse decision

A Survey is reusable only while its `Reflects revision`, `Survey scope`, and
`Evidence sources` remain adequate for the active assessment.

Refresh or narrow it when:

```text
material repository/runtime drift occurs
OR
the active work leaves the surveyed scope
```

Unrelated minor drift does not automatically invalidate the whole Survey.

Survey completion does not imply capability completeness, formal Gap readiness,
or Target acceptance.
