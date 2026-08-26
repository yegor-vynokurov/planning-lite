# Change execution

Use in Execution mode only after Gate D is satisfied.

Follow `CHANGE_LIFECYCLE.md`. On valid direct authorization, set lifecycle state to `Execution / In progress` and record the authorized task scope.

## Procedure

1. Verify scaffold integrity and stop on ambiguous or conflicting records.
2. Read `.planning/ACTIVE.md`, active `context.md`, current task, exact relevant plan and specification sections, and targeted code or tests.
3. Execute approved tasks in dependency order, one coherent slice at a time.
4. Keep edits inside approved scope and respect named seams, interfaces, blocking edges, and blast radius.
5. Run the narrowest meaningful check after each slice and configured broader checks at milestones.
6. Update `tasks.md`, append evidence to `progress.md`, and refresh `context.md` at meaningful checkpoints.
7. Do not narrate routine reads, edits, or checks. Report only a blocker, decision, risk, or completed milestone that changes the next action.

## Divergence

When reality differs from the plan, follow `CHANGE_AMENDMENT.md` before continuing the affected work. Do not hide attractive unrelated work inside implementation.

## Completion

When all approved tasks are complete and required implementation checks have run, transition to `Verification / Ready`. Finishing tasks prepares completion review; it does not authorize closure.

<!-- PL_FCP_EXECUTION_CONTROL_V1:BEGIN -->
## Field Control Pack execution controls

Execution remains bounded by the approved Plan and the active Change.

The active consumer Change context packet carries the current **Execution
Envelope**. It is a projection of approved authority, not a replacement for the
Plan.

### Execution Semantic Choice Guard

Execution MUST NOT invent an unresolved material choice that changes any of:

```text
science
evidence
identity
persistence
authorization
cross-task ownership
downstream interface semantics
```

If the approved contract and current evidence do not determine such a material
choice, stop only the dependent slice and record a structured blocked outcome.

Do not guess merely because one option is convenient, locally attractive, or
easy to implement.

### Blocker locality

A blocker stops only the work that depends on it unless a shared contract makes
the whole approved Change unsafe.

For each blocker distinguish:

```text
blocked slice
independent work still allowed
shared dependency, if any
decision owner needed to proceed
```

An independently closed task remains permitted when its contract does not
depend on the blocked semantic choice.

### Execution Envelope

The active consumer Change `context.md` records:

```text
Authorized task(s)
Allowed write surface
Relevant read-only surface
Forbidden/downstream surface
Tool/network constraints when material
Owned responsibility
Next permitted action
```

The Envelope may narrow work to the current bounded task. It may not expand the
approved Plan.

Writes outside the allowed surface, ownership transfers, or downstream
responsibility require the existing Change amendment/approval path.

### Structured blocked outcome

When a material execution blocker is encountered, record:

```text
failure_class
evidence
blocked_slice
independent_work_still_allowed
missing_decision_owner
next_permitted_action
```

There is no global blocker registry.

A blocked outcome is evidence and routing information. It is not permission for
an autonomous repair loop.

### Conditional closed-world completion

Where Contract Closure says exactness is material, completion should include
closed-world evidence:

```text
canonical-positive
nearest-wrong
```

Use these probes only where material to SHAPE, SEMANTICS, ENCODING, OWNERSHIP,
identity, evidence, persistence, or an interface contract.

Do not add heavyweight probes to trivial leaf work whose closure dimensions are
legitimately `N/A`.

### Ownership guard

Execution owns only the responsibility assigned to the authorized task.

Do not silently absorb:

```text
downstream persistence
future orchestration
unapproved registries
cross-task ownership
automatic routing
future Roadmap work
```

If completion would require one of these, stop the dependent slice and use the
normal amendment/decision authority.

### Completion boundary

Before declaring the authorized task complete:

1. verify the task stayed inside the Execution Envelope;
2. verify material semantic choices were determined rather than invented;
3. verify blockers were local unless a shared contract required broader stop;
4. verify independent legal work was not unnecessarily suppressed;
5. run conditional canonical-positive / nearest-wrong evidence where material;
6. preserve the distinction between task completion and broader Change
   completion.
<!-- PL_FCP_EXECUTION_CONTROL_V1:END -->
