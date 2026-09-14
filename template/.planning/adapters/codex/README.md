# Codex adapter

Codex discovers thin wrappers under `.agents/skills/`. Explicit skill invocation uses `$planning-plan`, `$planning-execute`, and the other canonical names. Wrappers must point to `.planning/skills/<name>/SKILL.md` and must not duplicate workflow logic.

Client commands such as context compaction, new conversations, model selection, and permission controls remain operator actions.

## Host binding and bounded execution

The Codex host profile owns provider-specific model and runtime binding. Its
current approved tiers are:

```text
STRONG_PARENT: GPT-5.6 Sol / High
DEFAULT_BOUNDED_MODEL: GPT-5.6 Luna / Extra High
```

The requested binding comes from the operator or dispatch contract.
`REQUESTED_BINDING` is the requested value. The confirmed binding comes from
exact structured host/runtime evidence when confirmation is required;
`CONFIRMED_BINDING` is that structured value. `MODEL_SELF_REPORT` is never
sufficient binding evidence. A current-turn execution must not false-block merely because final
host metadata is available only after completion; the next independent review
binds the completed turn. A later post-turn mismatch is a governance finding
and blocks dependent promotion.

Unavailable confirmation never silently inherits the strong parent or another
model. Record the unavailable-binding finding and stop the dependent route.

## Direct bounded Luna lane

The owner/operator may directly launch the default bounded model for a fully
closed `BOUNDED_MODEL_CAPABLE` contract. Before the turn starts, the contract
must close authority, classification, exact scope, required evidence, STOP
conditions, revision/hash binding, and next gate. The bounded executor is not
its own parent and does not self-authorize.

Direct execution cannot widen scope, adjudicate new material ambiguity, grant
owner acceptance, dispatch a child, or perform nested delegation. Stronger-model
escalation remains STOP. A child/model result is evidence, not owner
acceptance. The parent or authority side independently accepts or rejects the
bounded result.

Binding summary: `MODEL_SELF_REPORT` is never sufficient binding evidence;
direct execution cannot widen scope; direct execution cannot grant owner acceptance;
stronger-model escalation remains STOP; and nested delegation is
forbidden by default.

Model self-report is never binding evidence.

## Result Contract

Any delegated or bounded dispatch records a closed Result Contract with these
fields:

```text
mission
source/scope boundary
questions
required evidence
output contract
escalation rule
```

The contract also identifies the requested binding, exact target, allowed and
forbidden surface, acceptance/evidence boundary, STOP conditions,
revision/hash binding, and next gate. Nested delegation is forbidden by
default. A stronger-than-default bounded tier requires an explicit owner STOP;
there is no silent stronger-child fallback.
