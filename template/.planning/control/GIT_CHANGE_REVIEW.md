# Git change review

Use when requested, before non-trivial closure, or when configured risk triggers fire.

Follow `disciplines/CODE_REVIEW.md` for separate spec-conformance and standards-conformance passes.

## Strategy

Review summary first, then targeted patches:

1. branch, HEAD, status, staged state;
2. bounded commit range;
3. diff stats and changed paths;
4. unexpected, generated, vendored, dependency, schema, migration, security, API, architecture, or test changes;
5. targeted high-risk patches;
6. relevant checks and evidence.

Do not load an unbounded raw repository diff by default.

## Verdict

Record findings, evidence, impact, affected criterion or standard, and one verdict: `Pass`, `Pass with findings`, or `Block`.
