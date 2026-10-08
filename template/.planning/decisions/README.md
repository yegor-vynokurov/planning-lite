# Decisions

Use decision records for choices with durable architectural, product, data, compatibility, security, or operational consequences. Do not use them as task logs.

## Identity, ownership, and discovery

An individual decision item is named `.planning/decisions/ADR-NNNN-<slug>.md`. `NNNN` is exactly four ASCII digits from `0001` through `9999`; the ordinal is unique and is never reused. The slug is 1-64 lowercase ASCII letters or digits in non-empty hyphen-separated groups, beginning and ending with a letter or digit. The `decision_id` is exactly `ADR-NNNN`, matching the filename prefix, and the Markdown heading begins exactly `# ADR-NNNN:`.

Individual ADR files are project-owned. Framework updates preserve existing ADR bytes and do not require existing items to be rewritten. `README.md` and `TEMPLATE.md` remain centrally managed. `INDEX.md` is for discovery and summary only; it is not authorization evidence.

## Dependency-proof invalidation decisions

Only an invalidation item that is ready for owner approval uses the typed invalidation contract. It has exactly one ordinary status line, `` `- Status: `Accepted` ``, and exactly one `dependency-proof-invalidation-decision-v1` fenced block. The JSON object has exactly the nine keys shown in `TEMPLATE.md`, with no duplicate keys or extras. `schema_version` is integer `1`; the remaining values bind the exact ADR ID, active Change, T-01/A1 and T-02/A1 attempt IDs, proof ID, and `INVALIDATE_EXACT_DEPENDENCY_PROOF` outcome.

`decision_provenance_ref` identifies the exact target-root-relative POSIX path and SHA-256 of the whole decision item, including rationale and its final newline. The digest is computed from strict UTF-8 canonical-LF bytes: CRLF pairs become LF; a BOM, bare CR, malformed UTF-8, or missing/multiple terminal LF is rejected. Whitespace and all other bytes remain significant. Do not edit, move, rename, or reformat an item after issuing provenance; issuance and later use both revalidate the same item and proof tuple.

A decision item records an owner decision; it does not issue Authorization. Copier and local-only updates only preserve or refresh files according to ownership rules. They grant no authority. Only the existing Authorization issuer and resolver can publish and verify an Authorization record.
