# Material Code Documentation and Maintainability Binding — Plan Amendment v1

```text
CHANGE_ID: CHG-PL-V39-09-MATERIAL-CODE-DOCUMENTATION-AND-MAINTAINABILITY-BINDING-001
OWNER_REVIEW_VERDICT: SEMANTIC_CONTRACT_PASS / FORMAL_READINESS_HOLD_FOR_ONE_TEMPLATE_INTEGRITY_PLAN_CORRECTION
OWNER_FINDING: DOC-MAINT-RF-01_TEMPLATE_INTEGRITY_SURFACE_OMITTED
AMENDMENT_STATUS: CANDIDATE / OWNER REVIEWED CORRECTION
DEFINITION_V1_SHA256: 4eba43b069348750bd860441866b8c6f09ac7a17d36d547e1895b6110eaf89a6
PLAN_V1_SHA256: a1e0f00e2b48333ba01ec526a06fce20c472a887c61999dfc9ede21acf1db204
```

## Decision and precedence

The owner accepted the semantic contract in Definition v1 and the semantic
implementation surface in Plan v1. This amendment does not reopen either
decision. Definition v1 remains byte-identical and semantically accepted. Plan
v1 remains byte-identical; this amendment only completes its effective path
budget, receipt choreography, mandatory verification, and proof-source
binding. Where this amendment is more specific, it amends Plan v1 for those
execution details. The effective planning authority is:

1. Definition v1 — accepted semantics and scope;
2. Plan v1 — accepted T-01 through T-07 semantic task order; and
3. Plan Amendment v1 — integrity receipts, verification order, consumer proof,
   and exact effective implementation surfaces.

Implementation remains `NOT AUTHORIZED`.

## Effective write surface

The candidate implementation may write only these paths:

| Class | Path | Purpose |
|---|---|---|
| Semantic template | `template/.planning/disciplines/CODEBASE_DESIGN.md` | Single normative design and material source-contract rule. |
| Semantic template | `template/.planning/control/CHANGE_PLANNING.md` | Plan applicability marker and symbol-specific obligation. |
| Semantic template | `template/.planning/control/CHANGE_READINESS.md` | Applicability, determinacy, and verification-route checks. |
| Semantic template | `template/.planning/control/CHANGE_EXECUTION.md` | Conditional CODEBASE_DESIGN load before/during applicable generation. |
| Semantic template | `template/.planning/control/CHANGE_CLOSURE.md` | Thin closure route to the code-review standard. |
| Semantic template | `template/.planning/disciplines/CODE_REVIEW.md` | Thin verification reference to CODEBASE_DESIGN. |
| Focused test | `tests/test_field_control_pack_foundation.py` | Focused workflow/policy assertions. |
| Integrity receipt | `template/.planning/docs/MANIFEST_V4.md` | Allowed regeneration/verification surface; expected byte-identical because no template paths are added or removed. |
| Integrity receipt | `template/.planning/framework/SHA256SUMS.txt` | Regenerated canonical-LF hashes for the final managed template tree. |

The six semantic paths and one focused test path remain unchanged from Plan
v1. The two integrity paths add no product or policy semantics. No Python
runtime, `execution_guidance.py`, `tests/test_execution_guidance.py`, Plan
template/schema, skill, mode, `OWNERSHIP.yml`, `copier.yml`, Roadmap, or other
path is in scope. If deterministic evidence shows another path is required,
stop and return `DOC_MAINT_ADDITIONAL_TEMPLATE_OWNER_REQUIRED` with the exact
path and owning contract; do not expand the surface here.

## Integrity expectations and T-04I

This Change adds or removes no template path. Therefore:

```text
MANIFEST_V4.md: expected to remain byte-identical after deterministic regeneration/verification
SHA256SUMS.txt: expected to change for the six modified semantic template files
```

Do not force a manifest diff to show activity. Once the six semantic template
files have their final bytes, perform T-04I:

1. Enumerate every file below `template/.planning/` using its `.planning/`
   relative POSIX path. Compare this exact set with the manifest's listed set.
2. Reconcile the manifest file count to that actual set. With the approved
   no-path-add/no-path-remove scope, the expected count and listed paths remain
   unchanged; deterministic regeneration should reproduce the existing
   manifest bytes exactly.
3. If deterministic manifest regeneration changes `MANIFEST_V4.md` despite
   an unchanged path set/count, inspect the byte difference and its cause. If
   the difference is not fully explained by canonical regeneration, stop as
   `DOC_MAINT_MANIFEST_UNEXPECTED_DRIFT`.
4. Regenerate the complete `SHA256SUMS.txt` using the existing repository
   canonical-LF contract: one entry for every actual `.planning/` file except
   `framework/SHA256SUMS.txt` itself; each digest is SHA-256 of final file
   bytes after CRLF-to-LF normalization. Preserve the repository's established
   deterministic receipt ordering and line format.
5. Verify manifest path set equals the actual tree, manifest count equals the
   covered path count, checksum path set equals actual paths excluding the
   receipt itself, and every digest matches the corresponding final canonical-
   LF file bytes. The existing integrity detector is mandatory and may not be
   weakened, excluded, or xfailed.

The current detector is
`tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree`.
It compares manifest set/count, checksum set excluding the checksum receipt,
and every canonical-LF SHA-256. Existing prior template changes use this same
manifest-aligned tree and canonical-LF receipt contract; no new generator or
receipt taxonomy is proposed.

## Preserved task order with integrity verification

Keep T-01 through T-07 semantics. Refine the sequence as follows; T-04I and
T-04V are ordinary implementation tasks, not added owner micro-gates.

| Task | Required work and evidence |
|---|---|
| T-01 | Reconfirm live ownership, selectors, six semantic template paths, focused test path, and the current integrity detector. Record the exact nine-path effective surface and expected manifest/checksum behavior. |
| T-02 | Update the single normative CODEBASE_DESIGN contract. |
| T-03 | Add thin Planning, Readiness, Execution, Closure, and CODE_REVIEW bindings. |
| T-04 | Add focused structural/semantic tests in `tests/test_field_control_pack_foundation.py`. Do not change the execution-guidance runtime test. |
| T-04I | After all semantic template bytes are final, reconcile/regenerate MANIFEST_V4 and SHA256SUMS by the procedure above. Verify exact sets, counts, canonical-LF hashes, and expected manifest identity. |
| T-04V | Run the focused semantic tests and mandatory existing integrity detector below; run the relevant execution-guidance regression read-only. T-05 is blocked until all pass. |
| T-05 | After T-04V passes, run the disposable-consumer M0–M4 proof against the exact candidate bytes in the clean proof checkout described below. Exercise the ordinary Definition → Planning → Readiness → Execution → Review/Closure-preparation route and separately record selector evidence and review-outcome evidence. |
| T-06 | Run template adoption/update/Doctor smokes, full regression, and candidate review using the exact reviewed candidate source identity described below. |
| T-07 | Later commit and closeout only after separate owner review/authorization. |

Mandatory T-04V commands:

```text
uv run --frozen pytest -q tests/test_field_control_pack_foundation.py
uv run --frozen pytest -q tests/test_direction_foundation.py::test_planning_manifest_and_sha_receipt_match_template_tree
uv run --frozen pytest -q tests/test_execution_guidance.py::test_contract_route_projects_contract_closure_and_zero_discipline_is_explicit
```

The third command is read-only regression evidence. Preserve the ordinary
execution `discipline_refs == []` contract and the test; do not change it to
represent the workflow-level conditional selector.

## M0–M4 selector field proof

The proof must demonstrate that the approved Plan selector actually routes the
ordinary consumer workflow, not merely that a reviewer remembers a rule. Use
a disposable consumer and traverse Definition → Planning → Readiness →
Execution → Review/Closure preparation. Do not inject an extra hidden
instruction such as “remember to add a docstring” into the task.

Bind this field proof to the exact reviewed candidate byte manifest. Use the
same clean disposable proof checkout/source identity described below whenever
the consumer workflow relies on Git source identity. The proof is invalidated
if a bound candidate path changes afterward; rerun against the final bytes.

Record separate observable evidence that:

- Planning records `MATERIAL_CODE_CONTRACT: YES` and names the concrete
  material symbol/boundary obligation;
- Readiness checks the YES marker against the actual approved scope;
- before or during generation, Execution receives/loads CODEBASE_DESIGN
  because of that approved YES marker (preserve the relevant task context,
  workflow-read trace, or equivalent direct evidence);
- Closure preparation selects CODE_REVIEW and checks the same CODEBASE_DESIGN
  contract; and
- the review outcome evidence for each mutant is independent of the selector
  evidence.

Then exercise M0 concise sufficient documentation → PASS; M1 missing required
material documentation → FAIL; M2 tautological documentation → FAIL; M3
contradictory documentation → FAIL; and M4 tiny obvious private helper without
a docstring → PASS. This evaluator-operated field proof is not an automated
reliability-rate claim.

## Clean-source consumer and update proof

Require these existing scripts from a clean Git-versioned source containing
the exact reviewed candidate bytes:

```text
uv run --frozen python scripts/test_template_update.py
uv run --frozen python scripts/test_local_only_update.py
```

Also require clean temporary Git consumer adoption followed by
`planning-lite doctor` where the central repository verification contract
requires it. Do not run adoption/update smoke from the dirty central source and
claim it proves candidate identity. Use the same isolated clean proof
checkout/source identity for T-05 when Git identity is required and these T-06
smokes. Before a central product commit is authorized, the disposable proof
checkout/worktree may contain an isolated temporary synthetic local commit made
solely to give the exact reviewed candidate bytes a Git source identity. Bind
every effective candidate path to its exact hash and record the synthetic
commit identity in the later implementation checkpoint. That temporary commit
does not alter central HEAD, stage central files, grant product commit
authority, or grant release authority. Any use of it remains confined to
temporary proof sources.

At the T-06 integration gate, run `uv sync`, `uv run pytest`, both smoke
scripts above, the clean temporary consumer adoption/Doctor check, and
independent candidate review. Update-between-tags verification remains
conditional on changing update behavior; this Change does not change updater
behavior. Keep project-owned consumer files unchanged.

## Authority and stop conditions

This amendment closes only the template-integrity omission in
`DOC-MAINT-RF-01`. It does not authorize implementation, field proof, staging,
central commit, push, or release. The whole-organism proof remains
`NOT STARTED`; 09-G remains `NOT STARTED`; Roadmap remains read-only. If the
existing manifest changes without a fully explained deterministic reason,
stop with `DOC_MAINT_MANIFEST_UNEXPECTED_DRIFT`. If any additional template
owner/path is required, stop with `DOC_MAINT_ADDITIONAL_TEMPLATE_OWNER_REQUIRED`.
