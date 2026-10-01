# PL-V39-09 Minimal Architecture Decision Flow MVP - Implementation Plan Amendment v1

Status: OWNER-ACCEPTED / FORMAL READINESS V2 REVIEWED
Change ID: `CHG-PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-001`
Amends: `PL-V39-09-MINIMAL-ARCHITECTURE-DECISION-FLOW-MVP-IMPLEMENTATION-PLAN-v2.md`
Owner finding: `ARCH-MVP-RF-01_TEMPLATE_INTEGRITY_SURFACE_OMITTED`

This amendment is limited to the implementation write-path budget, template
integrity receipt regeneration, the associated verification obligations, and
the stop condition for any additional template owner. All Definition v2
semantics and all other Plan v2 boundaries remain unchanged. Definition v2 is
byte-identical and remains authoritative. This amendment and its readiness
review do not authorize implementation.

## Effective implementation write surface

The effective semantic/product template surface remains exactly these three
paths:

1. `template/.planning/control/ARCHITECTURE_DECISION_FLOW.md` - new concise
   architecture-decision guidance.
2. `template/.planning/control/ROOT_ROUTER.md` - one bounded routing rule.
3. `template/.planning/project/ARCHITECTURE_OVERVIEW.md` - extend the existing
   consumer-owned carrier seed.

The required integrity-receipt surface adds exactly two paths:

4. `template/.planning/docs/MANIFEST_V4.md` - regenerate the complete path list
   and file count from the final `.planning` template tree.
5. `template/.planning/framework/SHA256SUMS.txt` - regenerate canonical-LF
   SHA-256 receipts for every covered path, excluding the receipt file itself.

Paths 4 and 5 are integrity receipts only; they add no product semantics. No
Python or runtime source path is required. The effective five-path write
surface is the three semantic/template paths plus these two integrity receipts.

## Additional template-owner determination

Do not add
`template/.planning/templates/project/ARCHITECTURE_OVERVIEW.md` to this
Change. Current deterministic evidence does not require changing it:

- `tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree`
  requires exact path-set/count equality and matching canonical-LF receipts; it
  does not require byte equality between the project-owned carrier seed and the
  managed scaffold template.
- `template/.planning/framework/OWNERSHIP.yml` classifies
  `.planning/project/**` as project-owned and `.planning/templates/**` as
  managed. `copier.yml` skips `.planning/project/**` on update.
- The current ownership and integrity contracts therefore distinguish the
  accepted project carrier from the managed scaffold template. Integrity
  receipts cover each path independently.

If a current deterministic contract is found during later authorized work that
requires modifying the additional scaffold template, stop with exactly
`ARCH_MVP_ADDITIONAL_TEMPLATE_OWNER_REQUIRED` and return the contract and path
evidence for owner review. Do not add a sixth semantic/template path by
intuition or implication.

## Integrity regeneration and verification choreography

Preserve T-01 through T-06 and their semantics. Refine only the order between
semantic acceptance, integrity regeneration, verification, and field proof:

| Task | Work | Evidence / stop condition |
|---|---|---|
| T-01 | Reconfirm baseline, authority, ownership, and the exact five-path write boundary. | Stop if ownership or the reusable 09-E contract differs materially. |
| T-02 | Add concise `ARCHITECTURE_DECISION_FLOW.md` guidance and the bounded `ROOT_ROUTER.md` route. | Architecture-sensitive requests are opt-in; routine work retains its ordinary route. |
| T-03 | Extend only the consumer-owned `ARCHITECTURE_OVERVIEW.md` seed. | No second authority or new packet/schema. |
| T-04 | Add or extend the smallest suitable semantic test owner. | Cover the approved one-question flow without prose-layout tests or duplicate invariants. |
| T-04I | After the final template bytes are in place, regenerate `MANIFEST_V4.md` and `SHA256SUMS.txt`. | Manifest listed paths equal the actual `.planning` file set and count; receipt paths equal that set minus `SHA256SUMS.txt`; every receipt matches canonical-LF bytes. |
| T-04V | Run focused semantic acceptance, the required existing integrity detector, and the relevant template/update smoke checks. | All checks pass normally; no weakening, exclusion, xfail, or special case. Smoke checks run from a clean committed central source. |
| T-05 | Perform the frozen real field proof only after the separate implementation authorization. | Preserve the approved real subject and evidence contract; do not start 09-G in this Plan correction. |
| T-06 | Review and close out after the field evidence. | Close only after the end-to-end proof and material findings are adjudicated. |

The minimum focused verification surface is:

- the selected focused Architecture Decision Flow semantic test owner; add
  `tests/test_architecture_decision_flow.py` only if it is clearly the smallest
  suitable owner;
- `uv run --frozen pytest tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree`;
- `uv run --frozen python scripts/test_template_update.py` for temporary
  adoption and consumer Doctor verification; and
- `uv run --frozen python scripts/test_local_only_update.py` for the existing
  local-only consumer update path.

Run both consumer/update smoke scripts from a clean committed central source,
as required for source identity. Do not run `planning-lite doctor .` at the
central source root. Before declaring the framework change complete, retain the
repository verification requirements: `uv sync`, the full `uv run pytest`
suite, and a clean temporary Git consumer adoption followed by Doctor (the
managed-template smoke covers that adoption/Doctor path). Update-between-tags
verification is required only if update behavior changes.

The integrity test is an existing semantic owner for the manifest path set,
header count, receipt set, and canonical-LF digest equality. Do not add prose
layout assertions. The mandatory real field proof remains required after
authorization and cannot be replaced by template-fixture assertions.

## Authority and non-authorization

The effective Plan is:

`IMPLEMENTATION_PLAN_V2 + IMPLEMENTATION_PLAN_AMENDMENT_V1`

The amendment does not alter the approved Definition, architecture, MVP scope,
09-B status, P-05 disposition, or field-proof subject. It does not modify
product source, tests, templates, the Roadmap, or any integrity receipt in this
transition. Implementation, T-05, 09-G, stage, commit, and push remain
unauthorized.
