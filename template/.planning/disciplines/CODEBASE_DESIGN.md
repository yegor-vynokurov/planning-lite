# Codebase design discipline

Load only for architectural or structural work.

## Leading terms

- **Module**: a unit with an interface and hidden implementation. It may be a function, class, package, pipeline stage, or subsystem.
- **Interface**: everything callers must know, including inputs, outputs, invariants, errors, ordering, and configuration.
- **Implementation**: behavior hidden behind the interface.
- **Seam**: a boundary where behavior can be substituted or tested without rewriting callers.
- **Adapter**: a concrete integration attached through a seam.
- **Orchestrator**: coordinates peers at one abstraction level; it should not absorb their implementation details.
- **Policy**: an explicit rule for choosing behavior.
- **Gateway / repository**: a boundary for external systems or persistence.
- **Parser / validator / normalizer / serializer**: transformations with distinct contracts; do not collapse them into the word `helper`.
- **Registry**: named discovery or selection data, not hidden control flow.
- **Stage runner**: executes a declarative stage contract.
- **Deep module**: a simple interface hiding substantial coherent behavior.
- **Locality**: knowledge and changes for one responsibility remain close together.
- **Leverage**: one stable abstraction removes repeated complexity from many callers.
- **Blast radius**: the code, data, users, and operations potentially affected by a change.

## Use

For every material design claim, identify the concrete module, interface, seam, and blast radius. Classify generic `helper` functions by their actual role before proposing new abstractions.

Prefer:

- thin orchestrators calling peers at one abstraction level;
- deep modules with explicit contracts;
- policies separated from mechanisms;
- external effects behind seams and adapters;
- local reasoning over cross-cutting hidden state.

Treat high coupling, long call chains, wrapper ladders, generic utility hubs, and mixed abstraction levels as investigation signals, not automatic defects.

## Completion criterion

A design proposal is ready when callers, interfaces, seams, ownership, failure behavior, compatibility, and verification are explicit enough to implement without inventing architecture during execution.
