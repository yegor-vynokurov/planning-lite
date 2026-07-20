# Project bootstrap

Use in Audit mode to materialize durable project documents for an existing repository. This workflow does not authorize production-code edits or creation of an approved change.

## Allowed write scope

Bootstrap may update only:

- `.planning/project/*`;
- `.planning/assessments/current/*`;
- `.planning/ACTIVE.md`.

Repository code, tests, configuration, data, recommendations, decisions, and changes remain read-only unless the user separately authorizes another workflow.

## Canonical pristine copies

Managed pristine copies live under:

```text
.planning/templates/project/
```

Before editing each project-owned document, compare it with the matching canonical copy.

For classification only, normalize:

- an optional UTF-8 BOM;
- `LF` versus `CRLF` line endings;
- trailing spaces;
- the final newline.

Do not classify a file as pristine merely because it looks short, empty, generic, or template-like.

## Write classification

Classify every target document separately as one of:

- `Missing`: the project-owned file does not exist;
- `Pristine template`: normalized content matches the managed canonical copy;
- `Existing project content`: the file contains project-specific information or differs materially from the canonical copy;
- `Ambiguous`: safe classification is not possible.

## Write strategy

### Missing or pristine template

- Materialize the complete intended document directly.
- Do not attempt a line-based patch first.
- Write one file at a time.
- Use UTF-8 without BOM and the repository line-ending convention.
- Re-read the file after writing and verify the expected sections and content.

### Existing project content

- Preserve user-authored facts, decisions, uncertainty, and structure.
- Use a targeted merge or targeted patch.
- Do not replace the complete file unless the user explicitly approves replacement after seeing the preservation risk.

### Ambiguous

- Stop before writing that file.
- Report the conflicting evidence and request a decision.

A failed patch is not evidence that a file is pristine.

## Procedure

1. Confirm the repository root, current Git state, and bootstrap scan scope.
2. Read `.planning/ACTIVE.md`, Audit mode, this workflow, the project-document templates, and targeted repository evidence.
3. Inspect code, tests, configuration, data paths, documentation, and bounded Git summaries broadly enough to establish current facts.
4. Process each project document independently:
   - read the managed canonical copy;
   - read the project-owned target when present;
   - classify it;
   - apply the matching write strategy;
   - re-read and verify it before continuing.
5. Do not send one multi-file line patch across pristine bootstrap documents.
6. Record unknowns rather than inventing facts.
7. Create or refresh one evidence-based assessment under `.planning/assessments/current/`.
8. Update `.planning/ACTIVE.md` with the verified current stage, next permitted action, assessment path, and unresolved blockers.
9. Review the final diff and verify:
   - only the allowed planning paths changed;
   - no project-specific content was lost;
   - no managed canonical template was edited as project state;
   - no production code changed;
   - every written file can be read as UTF-8.
10. Finish with recommendations or questions, not implementation tasks.

## Output contract

Report the scan scope, classification and write strategy used for each project document, assessment path, material unknowns, files changed, and the next permitted action.
