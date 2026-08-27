# PLANNING LITE / PL-V39-05-A DEFINITION ACTIVATION v1

**Document ID:** `PL-V39-05-A-DEFINITION-ACTIVATION-001`
**Activation date:** `2026-08-27`
**Definition:** `CHG-PL-V39-05-A-SHAPING-FOUNDATION-001`
**Approved Definition:** `docs/design/project-spine/checkpoints/PL-V39-05-A-APPROVED-DEFINITION-v1.md`
**Source Definition SHA256:** `5944dcc47b13f59ffcb99f1ee084a2f321ae7ecddb0133a160920162c79c1bda`
**Approval authority:** `USER / EXPLICIT`
**Implementation authorization:** `NO`
**Push authorization:** `NO`

## 1. Central-source topology decision

Planning Lite's own central development repository does not carry this Change as
a consumer-style root:

```text
.planning/changes/active/<change>
```

That path belongs to generated/consumer Planning Lite projects.

For the CENTRAL_SOURCE repository:

```text
CURRENT.md
= authoritative active semantic state

docs/design/project-spine/checkpoints/
= durable transition evidence
```

No root `.planning/` directory is created.

`template/.planning/**` is product template source and is not mutated by this
activation.

## 2. Transition

```text
DISCOVERY_READY
active_change = NONE
        ↓
explicit user approval of CHG-PL-V39-05-A-SHAPING-FOUNDATION-001
        ↓
PLANNING_IN_PROGRESS
active_change = CHG-PL-V39-05-A-SHAPING-FOUNDATION-001
implementation_authorized = NO
```

## 3. Approved scope

```text
entry-contract semantic alignment where current contracts are ambiguous
+
bounded Project Survey / AS-IS evidence
+
bounded Clarification Sweep
```

The approved Definition remains the scope authority.

## 4. Stop boundary

This activation performs only:

```text
persist approved Definition
persist activation receipt
update central CURRENT resume state
commit those central state artifacts
```

It performs no product/template/src/test implementation.

T-01 remains not started.

## 5. Next permitted action

```text
prepare_pl_v39_05_a_implementation_plan
```

The Plan must be reviewed/approved and Formal Readiness must complete before any
separate implementation authorization.
