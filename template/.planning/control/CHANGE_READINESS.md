# Change readiness audit

Use in Audit mode as an independent check before execution. Do not edit production code.

Follow `CHANGE_LIFECYCLE.md`. Verify the complete scaffold through `CHANGE_SCAFFOLD.md`; restore only missing initialized files and preserve populated records.

Require an approved proposal and approved plan.

## Pass 1: specification readiness

Verify:

- scope and non-goals are unambiguous;
- every requirement and acceptance criterion is traceable;
- task outcomes and verification can establish the promised behavior;
- facts are verified and remaining decisions are explicit.

## Pass 2: engineering readiness

Verify:

- tasks are dependency-ordered and blocking edges are explicit;
- architecture, seams, public contracts, data, migration, recovery, security, compatibility, dependencies, tests, documentation, blast radius, and rollback are addressed where applicable;
- no execution detail still requires an unapproved architecture decision.

Record evidence and one verdict in `readiness.md`:

- `Ready`;
- `Needs revision`;
- `Blocked`.

`Ready` sets lifecycle state to `Readiness / Ready` and permits the user to authorize execution. It does not itself authorize execution.

The bounded Operation Guidance route for this procedure is the exact managed
identity `RUN_FORMAL_READINESS` / `FORMAL_READINESS_V1`. It consumes one
current ResumeContext projection, remains read-only, and may report a matched
readiness audit while `implementation_authorized` is `NO`. The derived result
and its evidence pointers never elevate implementation, Git, network, or
consumer authority.

On `Needs revision`, return to `Planning / In progress`. On `Blocked`, keep the narrowest defensible stage and record the blocking decision and next permitted action.

<!-- PL_FCP_EXHAUSTIVE_READINESS_V1:BEGIN -->
## Exhaustive-within-scope Readiness

Readiness audits the **full approved scope** before producing its final verdict.

Do not stop after the first independent blocker.

For every required slice or contract:

1. inspect it;
2. record each material finding;
3. identify the dependency boundary of each blocker;
4. continue across independent slices that remain auditable;
5. record independent legal work that remains permitted;
6. produce the final verdict only after the required bounded pass is complete.

The Readiness result must expose the complete known in-scope blocker set, not
merely the earliest blocker encountered.

### Shared Contract Closure

Where contract dimensions are material, use:

```text
.planning/disciplines/CONTRACT_CLOSURE.md
```

Evaluate conditionally:

```text
SHAPE
SEMANTICS
ENCODING
OWNERSHIP
```

Record each applicable dimension as:

```text
CLOSED
BLOCKED
N/A
```

`N/A` is explicit and legal for immaterial dimensions. Simple leaf work must be
allowed to remain light.

### Determinacy

Where exact identity, bytes, canonical encoding, evidence, persistence, or
interface representation is material, include a determinacy check.

Do not impose determinacy machinery where representation is immaterial.

### Materiality / Simplicity challenge

For non-trivial corrective mechanisms, verify that the mechanism is materially
required and that a simpler bounded repair would not close the same approved
contract.

Do not import future/downstream responsibility merely to satisfy a current
verification sentence.

### Blocker accounting

Readiness must distinguish:

```text
blocked slice
independent legal work
shared contract blocker
```

Two independent blockers must both be reportable in the same Readiness pass.

A shared blocker may block the whole Change only when its dependency boundary
actually makes the approved Change unsafe.

### Authority boundary

```text
Readiness PASS != Execution authorization
```

A Ready verdict never substitutes for explicit implementation authorization.
<!-- PL_FCP_EXHAUSTIVE_READINESS_V1:END -->
