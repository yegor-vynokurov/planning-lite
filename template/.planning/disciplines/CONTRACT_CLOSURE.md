# Contract Closure

Contract Closure is a shared discipline for proving that a material contract is
actually closed rather than merely named, partially checked, or patched around.

It is conditionally loaded. Trivial leaf work must not inherit heavyweight
closure ceremony when the dimensions below are immaterial.

## Four closure dimensions

When material, evaluate all four:

```text
SHAPE
SEMANTICS
ENCODING
OWNERSHIP
```

### SHAPE

Prove the permitted structure, not only the presence of named fields.

Where exact identity is required, unrelated extra fields are not implicitly
allowed.

### SEMANTICS

Prove that accepted values mean what the approved contract says they mean.

A required-field check is not semantic closure if arbitrary or contradictory
meaning can still enter through an open bag.

### ENCODING

Where representation contributes to identity, evidence, hashing, persistence,
or interoperability, require one canonical representation.

Equivalent alternate spellings, nesting, aliases, or type coercions are not
silently accepted when bytes or exact representation are material.

### OWNERSHIP

Prove that responsibility belongs to the approved slice.

Do not pull downstream collection, persistence, environment, Git, filesystem,
or other future responsibility into an earlier task merely because verification
mentions the eventual data.

## Conditional applicability

For each dimension record one of:

```text
CLOSED
BLOCKED
N/A
```

`N/A` is legal only when the dimension is immaterial to the approved task.
It is an explicit result, not an omitted check.

A simple leaf task may legitimately record all heavyweight closure dimensions
as `N/A` when none is material.

## Determinacy

Where exact contract identity or canonical representation is material, test
determinacy:

```text
one approved semantic input
→ one accepted canonical representation
→ one stable identity/evidence result
```

Reject material ambiguity where two accepted representations would produce
different identity, evidence, persistence, or downstream semantics.

Determinacy is conditional. Do not invent identity machinery for work that does
not need it.

## Materiality / Simplicity challenge

Before introducing non-trivial corrective machinery, ask:

```text
Is the mechanism material to the approved contract?
Is there a simpler bounded repair that closes the same contract?
Does the proposed mechanism import future/downstream responsibility?
```

If a simpler bounded repair closes the approved contract, prefer it.

Do not create generic registries, orchestration layers, evaluators, model
routers, repair loops, or future placeholders merely to make Closure look
complete.

## Closed-world / nearest-wrong evidence

Where the contract is exact or security/evidence sensitive, closure should use
both:

```text
canonical-positive
nearest-wrong
```

examples when material.

This evidence may be produced during deterministic verification rather than
during every Readiness pass.

## Relationship to lifecycle

Contract Closure is evidence used by Readiness and Execution.

It does not itself:

- approve a Plan;
- authorize Execution;
- create a Change;
- change Roadmap priority;
- create a new lifecycle stage.

A `Ready` verdict remains distinct from explicit Execution authorization.
