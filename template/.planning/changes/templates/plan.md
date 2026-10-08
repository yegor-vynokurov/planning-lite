# Implementation plan

- Status: `Draft / Approved`
- Approved by:
- Approval evidence:
- Approval date:
- Approved plan digest: `<64 lowercase hex>`
- Dependency semantic digest: `<64 lowercase hex>`

## Approved outcome and exclusions

## Design summary

## Modules, interfaces, seams, and adapters

## Affected paths and symbols

## Contracts and state transitions

## Delivery strategy

- Default slice type: `Tracer bullet / Expand-contract / Mixed`
- Blocking edges:
- Blast radius:

## Data, migration, recovery, and repeated execution

## Verification strategy and seams

## Documentation and operations

## Risks and rollback

## Dependency order

## Dependency contracts

For a dependency-aware approved Plan, keep exactly one canonical JSON
`PlanDependencyContractV2` object in this section. Replace the example refs
with the approved producer/consumer transfer, acceptance, scope, and verifier
identities. Keep the verifier pairs unique and sorted by `contract_id`, then
`contract_version_or_ref`.

```json
{"accepted_output_contract_ref":"acceptance:output-v1","acceptance_contract_ref":"acceptance:successor-v1","evaluation_scope_ref":"scope:successor-v1","produced_artifact_logical_ref":"artifact:producer-output","required_input_logical_ref":"artifact:successor-input","required_verifier_contract_refs":[{"contract_id":"build","contract_version_or_ref":"v1"}],"schema_version":2,"source_task_id":"T-01","target_task_id":"T-02"}
```

At the existing Plan approval or authorized reconciliation transition,
compute `plan_semantics_sha256` from canonical-LF UTF-8 bytes beginning at the
exact `## Approved outcome and exclusions` heading, `task_semantics_sha256`
from the ordered six-field task rows, `amendments_semantics_sha256` from the
amendments document before its final generated receipt, and the fixed
T-01 -> T-02 `dependency_semantic_digest`. Put the resulting
`approved_plan_digest` and fixed-edge `dependency_semantic_digest` in the two
metadata fields above this semantic boundary. These digests record approved
meaning; they do not create or refresh approval.
