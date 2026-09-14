# Execution routing policy

This is the single vendor-neutral policy for routing a material execution
task. It is loaded after the normal project router and before a task is
executed or delegated. It defines durable semantics; host-specific model names
and runtime record formats belong only to the active adapter.

## Authority and classification

Bind the authority/envelope before choosing a route. The envelope identifies the
approved Change/task, exact target, allowed and forbidden surface, required
evidence, STOP conditions, revision or hash binding, and next permitted gate.
Do not infer authority from a task description, a child result, or a model's
self-report.

Classify the task using the strongest material requirement:

```text
DETERMINISTIC_OR_TOOL_PREFERRED
BOUNDED_MODEL_CAPABLE
STRONG_JUDGMENT_REQUIRED
```

The strongest material requirement wins. deterministic subwork remains
tool-first. A bounded model route is allowed only when the closed envelope is
complete and no unresolved strong-judgment responsibility remains. Strong
judgment, unresolved material ambiguity, or a need to widen authority is a
STOP for the appropriate owner.

## Parent responsibility and bounded delegation

The authority owner or parent retains authority binding, classification, scope
control, write accounting, material escalation, and acceptance. A child/model
result is evidence, not owner acceptance. The parent must independently verify
the applicable Result Contract and either accept the evidence for its bounded
task or reject it.

Delegation is permitted only with a closed Result Contract containing every
field below:

```text
mission
source/scope boundary
questions
required evidence
output contract
escalation rule
```

The dispatch envelope must also bind the approved authority, target, allowed
and forbidden surface, STOP conditions, revision/hash, and next gate. A
stronger-than-default bounded tier requires an explicit owner STOP and cannot
be silently inherited or substituted. Nested delegation is forbidden by
default. Any exception requires an explicit owner decision before dispatch.

The child/model result is evidence, not owner acceptance.

## Binding and fail-closed behavior

The operator or dispatch contract supplies the requested binding. The active
adapter supplies exact confirmed host/runtime binding when confirmation is
required. Model self-report is never sufficient evidence. If required binding
or evidence cannot be confirmed, stop the dependent promotion; do not silently
inherit a stronger host, broaden scope, or mark the task complete.

## Direct bounded execution

A fully closed `BOUNDED_MODEL_CAPABLE` task may use a direct bounded executor
when the owner/operator supplies the complete authority envelope before the
turn starts. The direct executor is not its own parent and cannot self-authorize,
widen scope, adjudicate new material ambiguity, grant owner acceptance, dispatch
a child, or perform nested delegation. Stronger-model escalation remains an
owner STOP. Direct execution still produces the required structured evidence and
is subject to the active adapter's binding confirmation.

## Prompt-deduplication boundary

Stable routing boilerplate is canonical here, but prompt-deduplication is not
active under this policy. The steady-state prompt shape may eventually be:

```text
Follow canonical Planning Lite execution routing,
the active host adapter,
and the applicable workflow/checklist/result contract.

TASK-SPECIFIC DELTA:
- authority
- target
- allowed/forbidden surface
- acceptance/evidence
- STOP conditions
- revision/hash binding
- next gate
```

Never deduplicate task-specific authority, mutation boundaries, non-goals,
output/evidence requirements, STOP conditions, revision/hash binding, or the
next gate. Prompt-deduplication remains inactive until the governing slice is
implemented, independently reviewed, owner accepted, and checkpointed.
