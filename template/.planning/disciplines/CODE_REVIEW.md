# Code review discipline

Use two separate passes. Do not let one pass substitute for the other.

## Pass 1: spec conformance

Check only whether delivered behavior matches:

- approved scope and non-goals;
- requirements and acceptance criteria;
- approved amendments;
- public behavior and observable outcomes.

Record exact evidence and missing evidence. Do not excuse a spec failure because the code is elegant.

## Pass 2: standards conformance

Check engineering quality against:

- project rules and Definition of Done;
- architecture boundaries and interfaces;
- tests and failure handling;
- data, migration, recovery, compatibility, security, and operations;
- maintainability and repository conventions.

For applicable material code contracts, use `CODEBASE_DESIGN.md` as the
single normative standard. Verify material applicability, required nearby
source-document presence and semantic adequacy, consistency with the
implementation and invariants, and maintainability conformance. This review
procedure checks the rule; it does not define a second documentation or
maintainability policy.

Do not assume the specification itself is good merely because it was approved.

## Findings

For each material finding report:

- finding;
- evidence;
- impact;
- affected criterion or standard;
- required action or reason it is non-blocking.

Code smells are hypotheses requiring concrete evidence. Avoid generic claims such as `spaghetti`, `too complex`, or `needs cleanup` without named symbols, paths, dependencies, or failure cases.

## Completion criterion

The review is complete when both passes have explicit verdicts and every blocking finding is linked to evidence and a next action.
