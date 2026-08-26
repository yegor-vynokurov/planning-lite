# Recommendation Absorption

Recommendation Absorption is the manual accounting workflow used when durable
Recommendation meaning must be reconciled into current project direction
without losing residue or creating a second Recommendation lifecycle.

It is not an automatic prioritizer, Roadmap generator, Change creator, or
Recommendation status machine.

## Applicability

Use Absorption when:

- an existing durable Recommendation contains several semantic obligations;
- implementation evidence closes only part of a Recommendation;
- residue must be placed into a Gap, accepted direction artifact, explicit
  future trigger, or other durable owner;
- a Recommendation has been converted or partly delivered but remaining meaning
  must still be accounted for.

Do not use Absorption merely to capture an observation. Observation-only input
belongs in the Discovery registry.

Do not decompose a simple Recommendation unless unit-level accounting is
material to avoiding residue loss or ownership ambiguity.

## Authorities

Read before absorption:

```text
.planning/control/RECOMMENDATION_LIFECYCLE.md
.planning/control/RECOMMENDATION_HISTORY_RECONCILIATION.md
```

`RECOMMENDATION_LIFECYCLE.md` remains authoritative for lifecycle Status,
RecommendationUnit reconciliation states, primary lineage, and parent
reconciliation state.

Absorption does not define a parallel state vocabulary.

## Canonical RecommendationUnit reconciliation states

Use exactly:

```text
IMPLEMENTED
STILL_OPEN
CARRIED_FORWARD
FUTURE_SEED
DEFERRED
REJECTED
SUPERSEDED
NEEDS_REFRAME
UNCERTAIN
```

Every in-scope durable semantic unit gets exactly one reconciliation state.

## Three distinct state layers

Never collapse:

```text
Recommendation lifecycle Status
RecommendationUnit reconciliation state
parent Recommendation reconciliation state
```

A lifecycle transition requires its existing authority.

Unit accounting does not silently change parent lifecycle Status.

## Manual procedure

### 1. Bound the source

Identify the Recommendation and the exact durable meaning being reconciled.

Preserve source wording or source locators sufficiently to recover lineage.

### 2. Decide whether semantic-unit accounting is material

If the Recommendation is simple and one disposition covers all durable meaning,
do not create artificial units merely for ceremony.

If several independently durable meanings exist, preserve or create stable unit
identities according to the current Recommendation reconciliation contract.

### 3. Account for every in-scope durable unit

For every unit, record:

```text
unit identity
unit reconciliation state
primary lineage classification
evidence or uncertainty
current destination or future trigger when applicable
```

The residue invariant is:

```text
all in-scope durable Recommendation units are accounted for
```

No unit may silently disappear because a linked Change completed.

### 4. Place surviving meaning

A surviving unit may point to an existing durable semantic owner such as a
current Gap, accepted Target/direction artifact, explicit future trigger, or
other governed destination.

Placement must preserve semantic ownership.

### Material placement ambiguity

If two materially different owners are plausible and existing authority does
not resolve the choice:

```text
BLOCK
```

Record the ambiguity for human/authorized adjudication. Do not guess.

### 5. Derive parent reconciliation state separately

Use the existing parent reconciliation vocabulary:

```text
OPEN
COMPLETED
PARTIALLY_REALIZED
CLOSED_WITH_CARRYFORWARD
DEFERRED
SUPERSEDED
REJECTED
UNANCHORED
NEEDS_REFRAME
UNCERTAIN
```

The parent state summarizes the accepted unit ledger. It does not silently
change lifecycle Status.

### 6. Check residue explicitly

Before declaring the absorption complete, ask:

- Is every in-scope durable unit present in the ledger?
- Does every `CARRIED_FORWARD` unit name a durable destination?
- Does every `FUTURE_SEED` have a real future trigger?
- Is uncertainty represented as `UNCERTAIN` rather than guessed?
- Did any unit disappear only because a Change was marked complete?
- Did historical Roadmap order leak in as current priority?

Any unresolved material item keeps Absorption incomplete.

## Roadmap and Change boundary

Absorption MUST NOT automatically:

- create a Roadmap item;
- reorder Roadmap priority;
- create or approve a Change;
- authorize implementation;
- convert a Discovery into executable work;
- treat historical Roadmap order as current priority.

A new Roadmap branch is justified only through the existing Roadmap synthesis
authority and must have a distinct dependency boundary, semantic owner, and
evidence-bearing exit gate.

A new executable Change still requires the normal Change lifecycle and approval
gates.

## Output

The durable output is the existing Recommendation/reconciliation record or
assessment surface already owned by Planning Lite.

Absorption itself does not introduce a new project-owned registry.

## Completion

Absorption is complete only when:

```text
all in-scope durable units have explicit dispositions
+
all surviving residue has an explicit owner/trigger or explicit uncertainty
+
no material semantic placement ambiguity remains
```

Completion of Absorption is accounting evidence, not implementation authority.
