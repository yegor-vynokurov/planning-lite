# Recommendation lifecycle

Recommendations hold durable hypotheses or opportunities. They do not contain executable tasks and do not authorize implementation.

## Capture

Create a recommendation only when the idea is durable enough to revisit. Search the index and relevant items for overlap first. Record evidence separately from interpretation and preserve user wording when it matters.

## Statuses

- `Proposed`: recorded for discussion; no direction approved.
- `Accepted`: direction approved; no approved change yet.
- `Converted`: one or more linked changes exist; outcome may still be partial.
- `Deferred`: intentionally postponed by user decision.
- `Rejected`: intentionally declined with rationale.
- `Completed`: intended outcome is fulfilled and no incomplete linked change remains.

The agent may create `Proposed`, recommend transitions, and set `Converted` as bookkeeping when an approved linked change is created. Acceptance, deferral, rejection, and abandonment require user decisions. `Completed` is set only during authorized closure with full coverage.

## Conversion to change

A recommendation may map to several changes, and a change may originate from several recommendations. Update both directions:

- recommendation `Converted changes`;
- change `Source recommendations`;
- recommendation item and `INDEX.md`.

## Coverage at closure

Use `Full`, `Partial`, or `None`.

| Coverage and remaining work | Result |
|---|---|
| Full and no incomplete linked changes | `Completed` |
| Full but other incomplete linked changes remain | `Converted` |
| Partial | `Converted` |
| None | preserve status and explain |

A completed change does not automatically complete its source recommendation.

## Integrity

The individual item is authoritative. Keep the index synchronized. Resolve missing items, duplicate IDs, invalid transitions, and item/index disagreements before conversion or closure.
