# ADR-NNNN: Decision title

- Status: `Proposed / Accepted / Superseded / Rejected`
- Date:
- Deciders:
- Related changes:

## Context

## Decision

## Alternatives

## Consequences

## Follow-up

## Dependency-proof invalidation provenance (only for this decision kind)

For an ordinary ADR, omit this entire section. For a dependency-proof invalidation item, use a unique ordinal from `0001` through `9999`, never reuse an ordinal, and use a 1-64 character lowercase ASCII alphanumeric slug in non-empty hyphen-separated groups. The basename must be `ADR-NNNN-<slug>.md`; `decision_id` must equal its four-digit `ADR-NNNN` prefix; the heading must begin exactly `# ADR-NNNN:`. The ordinal must be unique across supported ADR items.

The invalidation item must have exactly one status line, `` `- Status: `Accepted` ``. Include exactly one block with the opening line below and a closing line containing only three backticks. Replace every placeholder with the exact current owner-approved value. The block itself does not issue authority; the existing Authorization API validates it and the whole item at issuance and every later use.

```dependency-proof-invalidation-decision-v1
{
  "schema_version": 1,
  "decision_id": "ADR-NNNN",
  "decision_kind": "DEPENDENCY_PROOF_INVALIDATION",
  "decision_status": "APPROVED",
  "change_id": "<exact active Change ID>",
  "source_attempt_id": "<exact Change/T-01/A1>",
  "successor_attempt_id": "<exact Change/T-02/A1>",
  "proof_id": "<exact immutable proof ID>",
  "decision_outcome": "INVALIDATE_EXACT_DEPENDENCY_PROOF"
}
```

There are exactly nine keys: `schema_version`, `decision_id`, `decision_kind`, `decision_status`, `change_id`, `source_attempt_id`, `successor_attempt_id`, `proof_id`, and `decision_outcome`. `schema_version` is integer `1`, not a boolean. No duplicate JSON members or additional keys are valid.

The provenance reference has the form `decision:.planning/decisions/ADR-NNNN-<slug>.md@sha256:<64 lowercase hex digits>`. Its digest covers the whole item, including rationale, metadata, block, and final newline, using strict UTF-8 canonical-LF bytes. CRLF pairs convert to LF; BOM, bare CR, malformed UTF-8, or a non-exact terminal LF fails closed. All other whitespace and bytes remain significant. Do not change or move the item after provenance is issued.

`INDEX.md` is discovery material, never authorization authority. Individual ADR files are project-owned and existing ADRs need no rewrite during framework updates. README/TEMPLATE remain managed. Neither normal Copier nor local-only update issues Authorization; only the existing Authorization issuer and resolver do that.
