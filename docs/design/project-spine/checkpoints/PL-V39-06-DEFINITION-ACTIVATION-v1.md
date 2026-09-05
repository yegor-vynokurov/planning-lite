# PLANNING LITE / PL-V39-06 DEFINITION ACTIVATION v1

- Document ID: `PL-V39-06-DEFINITION-ACTIVATION-001`
- Activation date: `2026-09-05`
- Change: `CHG-PL-V39-06-CONTEXT-MEMORY-HANDOFF-001`
- Approved Definition: `docs/design/project-spine/checkpoints/PL-V39-06-CONTEXT-MEMORY-HANDOFF-CHANGE-DEFINITION-v1.md`
- Approved Definition SHA256: `015ee1900ab905962eda73c341d30b783375e9795379512e391ac9f56b07d978`
- Approval authority: `USER / EXPLICIT`
- Definition decision: `APPROVE`
- Implementation authorization: `NO`
- Approved Plan: `docs/design/project-spine/checkpoints/PL-V39-06-CONTEXT-MEMORY-HANDOFF-IMPLEMENTATION-PLAN-v1.md`
- Plan decision: `APPROVE / USER EXPLICIT / 2026-09-05`
- Plan / Formal Readiness: `APPROVED BY OWNER / NOT RUN`
- Commit/tag/push/merge/release authorization: `NO`

## 1. Central-source carrier

Planning Lite central development continues to use:

```text
docs/design/project-spine/CURRENT.md
= active semantic state

docs/design/project-spine/checkpoints/
= durable transition evidence
```

No consumer-style `.planning/changes/active/**` is created, and no
`template/.planning/**`, product source, test, Poker, or mood file is changed.

## 2. Bounded transition

```text
DISCOVERY_READY
active_change = NONE
        ↓
explicit owner approval of the tightened Definition
        ↓
PLANNING_IN_PROGRESS
active_change = CHG-PL-V39-06-CONTEXT-MEMORY-HANDOFF-001
implementation_authorized = NO
```

The approved Definition preserves nine acceptance criteria, the 06/07/08
boundary, no second memory authority, no new persistent memory store, and no
live consumer migration. The Authority and Scope Binding remains shaping
evidence and was not materially redesigned.

## 3. Activated boundary

The active slice is:

```text
PL-V39-06 — Context / Memory / Handoffs
```

The Change governs bounded semantics for memory, context, current state, and
handoff; five storage classes; authority-first bounded resume selection; and a
minimal freshness-aware transition contract. Context Bootstrap Capsule,
ContextTrace, and AgentWorkPacket remain reconstructable/derived views or
packets, not a new persistent storage authority. Semantic retrieval,
embeddings, vector search, RAG, and embedding-first selection remain deferred.

## 4. Planning-phase progression and stop boundary

The Definition activation is unchanged. The owner-approved planning progression
now records only:

```text
Definition: APPROVED
Plan: APPROVED BY OWNER
implementation_authorized: NO
planning authority checkpoint: one governance-only commit
next gate after checkpoint: FORMAL_READINESS
```

The planning-authority checkpoint is not the later central implementation
candidate. This governance run does not start Formal Readiness and does not
authorize implementation, live Poker or mood migration, control-Git creation,
source/template/test changes, or any release operation.

## 5. Next lifecycle gate

```text
next_permitted_action: RUN_PL_V39_06_FORMAL_READINESS
```

Formal Readiness is read-only and remains a separate next gate. Implementation
authorization remains a later separate owner decision.
