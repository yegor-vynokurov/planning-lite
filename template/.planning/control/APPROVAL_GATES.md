# Approval gates

Use the narrowest gate that matches the action.

## Gate A: durable recommendation

The agent may create a `Proposed` recommendation when the user asks to record an idea or when durable follow-up is explicitly requested. A recommendation never authorizes code changes.

## Gate B: approved change definition

A change may be drafted after the user accepts a direction or explicitly asks to define it. The change becomes `Approved` only after the user confirms scope, non-goals, acceptance criteria, and material decisions.

## Gate C: implementation readiness

Execution requires a completed plan and a readiness verdict of `Ready`. Missing decisions, traceability, migration, recovery, tests, or compatibility work block readiness.

## Gate D: execution authorization

Production-code edits require both:

1. an approved and ready active change selected in `.planning/ACTIVE.md`; and
2. a direct user command to implement the change or named tasks.

Statements such as `looks good`, `I agree`, `the plan is fine`, or acceptance of a recommendation do not authorize execution.

An explicitly requested quick fix may use the controlled side path in `DRIFT_POLICY.md`.

## Gate E: scope amendment

Any change to approved scope, acceptance criteria, public contract, persisted data, migration, security, compatibility, architecture boundary, or production dependency requires explicit user approval and a renewed readiness audit.

## Gate F: closure

Review authorization is not closure authorization. Closure requires an explicit request to close or user approval of the proposed completion verdict. Accepted limitations require explicit acceptance.

## Destructive actions

Ask before destructive, irreversible, externally billed, security-sensitive, or data-loss-prone actions even when another gate is open.
