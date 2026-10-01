# Codebase design discipline

Load for architectural or structural work and for work classified as
`MATERIAL_CODE_CONTRACT`.

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

## Material code contracts

`MATERIAL_CODE_CONTRACT` applies when a task creates or materially changes a
contract whose relevant meaning a reasonable caller or future maintainer
cannot safely infer from a trivial signature and body alone. It is triggered
by any of these bounded cases:

- a public or externally used callable or class;
- ownership of a state transition;
- an authorization or security boundary;
- persistence, serialization, or schema behavior;
- concurrency, locking, or atomicity behavior;
- a parser or validator with non-obvious grammar or failure semantics;
- routing, orchestration, or policy selection;
- a material side effect;
- a non-obvious algorithm or invariant; or
- another specifically named hidden contract whose meaning meets the same materiality test.

The final case must name the hidden contract and pass the same inference test;
it is not an open-ended catch-all.

Redundant source documentation is not required for an obvious tiny private
transformation, a straightforward accessor or property, a trivial forwarding
wrapper with no hidden contract, generated code, or a symbol that does not own
the material contract. These cases do not override a concrete material
trigger. There is no docstring coverage quota or minimum documentation length.

For a material code contract, provide nearby source documentation in the
language's normal form. For Python functions and classes, the normal form is a
docstring. State the material meaning callers and maintainers need. Depending
on the contract, that can include purpose, authoritative input or source of
truth, caller-facing behavior, an invariant, output or state transition,
failure or rejection semantics, side effects, persistence, concurrency or
locking, authorization assumptions, and non-goals or forbidden
interpretations. Include only applicable dimensions; fixed headings and
prose volume are not requirements.

`DOCSTRING_PRESENT` and `MATERIAL_CONTRACT_DOCUMENTED` are separate checks.
Documentation for a material contract is insufficient when it only restates a
name, uses generic wording such as “Process the data,” or repeats parameter
names without material meaning. It is also insufficient when omitted meaning
makes a reasonable but materially wrong inference likely, or when it
contradicts current behavior or an invariant. If a Change alters a documented
material contract, update its source documentation in that same Change.
Passing behavior tests alone does not excuse stale or contradictory
documentation.

Applicability is prospective: it covers newly created or materially changed
contracts. Existing undocumented symbols remain observed debt; this discipline
does not authorize a repository-wide docstring retrofit.

## Maintainability default

Choose the smallest coherent implementation that preserves explicit
contracts and ownership, supports local reasoning, and keeps unnecessary
coupling low. Keep orchestration thin. Prefer deep, coherent modules where
useful and seams that make behavior testable. Do not add a generic helper hub
without evidence, speculative abstractions, or architecture invented during
implementation.

Maintainability and performance optimization are different concerns. Optimize
performance only when evidence shows a performance need; maintainability does
not imply a performance target or optimization work.

## Use

For every material design claim, identify the concrete module, interface,
seam, and blast radius. Classify generic `helper` functions by their actual
role before proposing new abstractions.

Prefer:

- thin orchestrators calling peers at one abstraction level;
- deep modules with explicit contracts;
- policies separated from mechanisms;
- external effects behind seams and adapters;
- local reasoning over cross-cutting hidden state.

Treat high coupling, long call chains, wrapper ladders, generic utility hubs,
and mixed abstraction levels as investigation signals, not automatic defects.

## Completion criterion

A design proposal is ready when callers, interfaces, seams, ownership,
failure behavior, compatibility, and verification are explicit enough to
implement without inventing architecture during execution.
