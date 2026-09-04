# PLANNING LITE / PL-V39-05-C DEFINITION ACTIVATION v1

- Document ID: `PL-V39-05-C-DEFINITION-ACTIVATION-001`
- Activation date: `2026-09-03`
- Change: `CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001`
- Approved Definition: `docs/design/project-spine/checkpoints/PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-CHANGE-DEFINITION-v1.md`
- Approved Definition SHA256: `98769cceedd226fd602890daa308c9c47682089f89fd99ff2e6748c1a5932751`
- Source draft SHA256: `2b8f6b910cd6079fa0d3a7e86cf919e471ad70d526a57531890452d538296597`
- Approval authority: `USER / EXPLICIT`
- Plan preparation authorization: `YES`
- Implementation authorization: `NO`
- Commit/tag/push/merge/release authorization: `NO`

## 1. Central-source carrier

Planning Lite central development continues to use:

```text
docs/design/project-spine/CURRENT.md
= active semantic state

docs/design/project-spine/checkpoints/
= durable transition evidence
```

No consumer-style root `.planning/changes/active/**` is created, and no
`template/.planning/**` product source is changed by this activation.

## 2. Bounded drift and dirt adjudication

The activation baseline remains:

```text
HEAD: a40019209c133785a4babe06b5e96dfd4673c4f5
branch: reconcile/current-design-spine-2026-08-25
```

The dirty tree contains only the four owner-accepted 05-C design/lifecycle
artifacts and the six incoming files governed by
`PL_V39_05_C_INCOMING_ADJUDICATION.md`. No existing untracked file overlaps this
activation receipt or the Plan path.

The Authority Binding Report, Implementation Start Contract, Incoming
Adjudication, canonical `CURRENT.md`, and canonical Roadmap passed the bounded
hash/existence check. No material drift reopened architecture discovery.

## 3. Transition

```text
DISCOVERY_READY
active_change = NONE
        ↓
explicit owner approval of the current Definition
        ↓
PLANNING_IN_PROGRESS
active_change = CHG-PL-V39-05-C-CONSUMER-CONTROL-TOPOLOGY-001
implementation_authorized = NO
```

## 4. Activated boundary

The approved Definition is the scope authority for the single bounded slice:

```text
PL-V39-05-C
Consumer Control Topology + Project Policy + Telemetry Baseline
```

The detailed `T-01` through `T-09` implementation-start contract remains in
`02_PL_V39_05_C_IMPLEMENTATION_START_CONTRACT.md`. Incoming recommendations and
the non-canonical competing 05-C roadmap snapshot retain the dispositions in the
Incoming Adjudication and do not expand the Change.

## 5. Authorized action and stop boundary

This activation authorizes only:

```text
persist Definition approval
persist this activation receipt
update central CURRENT resume state
prepare one bounded Plan for owner review
```

It does not authorize implementation, product/runtime changes, live Poker or
mood migration, or any Git history/release operation.

## 6. Next lifecycle gate

After Plan preparation:

```text
next_permitted_action: owner_review_pl_v39_05_c_implementation_plan
```

Plan approval is separate. Implementation remains separately gated after Plan
approval and read-only Formal Readiness.
