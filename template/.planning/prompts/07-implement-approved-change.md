# Implement approved work

Mode: Execution.

## Authorization check

Proceed only when:

- proposal status is Approved;
- pre-implementation audit has no unresolved critical blocker;
- `.planning/ACTIVE.md` points to this change;
- the user directly authorizes implementation or named tasks.

## Procedure

1. Read the active context packet, current tasks, relevant plan/spec sections, code, tests, and applicable project rules.
2. Record or reproduce the baseline.
3. Work through tasks in dependency order.
4. For each task:
   - make the smallest in-scope change;
   - follow established repository conventions;
   - verify it;
   - mark it complete only after verification;
   - update progress at a meaningful checkpoint.
5. For Python, follow PEP 8 and write readable idiomatic code. Apply DRY, KISS, YAGNI, and SOLID pragmatically.
6. When reality differs:
   - record a plan amendment before continuing if scope is unchanged;
   - stop and request approval for scope or acceptance amendments;
   - create recommendations for unrelated follow-ups.
7. A tiny user-requested unrelated correction may switch to Quick fix mode and must be logged.
8. Run the full relevant verification set.
9. Update `context.md` and `.planning/ACTIVE.md` to `In review`.
10. Do not declare completion before final review.

## Communication

Surface failures, risk, plan mismatch, and skipped checks immediately. Do not conceal partial success.
