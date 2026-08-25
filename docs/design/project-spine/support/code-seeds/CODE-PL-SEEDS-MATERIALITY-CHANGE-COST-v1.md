# CODE-PL-SEEDS-MATERIALITY-CHANGE-COST-v1
## Reference/prompt/code seeds for the Planning Lite code companion

**Status:** research/code-stash candidate; not product semantics
**Date:** 2026-08-20
**Suggested stash location:** `.planning-lab/recommendations/active/CODE-PL-SEEDS-MATERIALITY-CHANGE-COST-v1.md`
(or merge into the next `CODE-PL-ROADMAP` companion revision after reconciliation)

## 1. Materiality / simplicity review seed

External inspiration:
- https://github.com/testdouble/han/blob/main/han-coding/references/yagni-rule.md
- https://github.com/testdouble/han/blob/main/han-coding/skills/code-review/references/review-checklist.md
- https://google.github.io/eng-practices/review/reviewer/looking-for.html

Local prompt seed:

```text
For each newly proposed mechanism:

A. EVIDENCE GATE
   Name current evidence:
   OBSERVED / DIRECT / PLAUSIBLE_CURRENT / SPECULATIVE.
   If only SPECULATIVE:
     recommend DEFER or DROP;
     name the concrete reopen trigger.

B. SIMPLER-VERSION GATE
   Compare:
   do nothing
   fail fast
   manual action
   immutable append/new attempt
   rerun
   reuse existing primitive
   proposed mechanism

   Keep the least complex option satisfying all material current requirements.

C. CLASSIFY
   MUST_KEEP / SIMPLIFY_NOW / DEFER / DROP / HUMAN_DECISION

D. STOP
   Once the material requirement is satisfied, do not add future-proofing.
```

Candidate machine-readable record:

```yaml
finding_id: YAGNI-001
source_requirement: AC-...
evidence_class: OBSERVED
evidence_ref: ...
failure_if_absent: ...
candidate_shapes:
  - name: fail_fast
    satisfies: [...]
    added_states: 0
    added_transitions: 1
  - name: proposed
    satisfies: [...]
    added_states: 4
    added_transitions: 9
classification: SIMPLIFY_NOW
selected_shape: fail_fast
reopen_trigger: ...
```

## 2. Change-cost profile seed

```yaml
change_cost_profile_v1:
  source_change: CHG-...
  estimate_stage: ROADMAP | PLANNING | ACTUAL
  surface:
    files: 0
    modules: 0
    contracts: 0
    schemas: 0
  propagation:
    direct_dependents: 0
    reachable_dependents: 0
    propagation_ratio: 0.0
  history:
    revisions_touched: 0
    logical_coupling_edges: 0
    normalized_change_entropy: 0.0
    hotspot_percentile_max: 0.0
  mechanism_delta:
    components: 0
    artifact_types: 0
    identities: 0
    mutable_states: 0
    state_transitions: 0
    retry_failure_branches: 0
    platform_branches: 0
    config_dimensions: 0
    external_dependencies: 0
  verification_delta:
    tests: 0
    scripts: 0
    expensive_runs: 0
  actuals:
    planning_loops: null
    readiness_loops: null
    verification_loops: null
    tool_calls: null
    input_tokens: null
    output_tokens: null
    test_runtime_seconds: null
```

## 3. Normalized change entropy seed

```python
from math import log

def normalized_change_entropy(counts: list[int]) -> float:
    positive = [c for c in counts if c > 0]
    if len(positive) <= 1:
        return 0.0
    total = sum(positive)
    p = [c / total for c in positive]
    return -sum(x * log(x) for x in p) / log(len(p))
```

Research source:
Ahmed E. Hassan, ICSE 2009, DOI 10.1109/ICSE.2009.5070510.

## 4. Dependency propagation seed

```python
from collections.abc import Iterable, Mapping

def transitive_reach(
    dependents: Mapping[str, Iterable[str]],
    seeds: Iterable[str],
) -> set[str]:
    reached = set(seeds)
    stack = list(reached)
    while stack:
        node = stack.pop()
        for nxt in dependents.get(node, ()):
            if nxt not in reached:
                reached.add(nxt)
                stack.append(nxt)
    return reached

def propagation_ratio(dependents, seeds) -> float:
    universe = set(dependents)
    for items in dependents.values():
        universe.update(items)
    if not universe:
        return 0.0
    return len(transitive_reach(dependents, seeds)) / len(universe)
```

Reference:
https://www.sei.cmu.edu/blog/developing-an-architecture-focused-measurement-framework-for-managing-technical-debt/

## 5. Git-history reuse candidates

Code Maat:
https://github.com/adamtornhill/code-maat

Useful analyses:
```text
revisions
entity-churn
coupling
soc
ownership
fragmentation
```

CodeLore:
https://github.com/emrecdr/codelore

Useful reference ideas:
```text
hotspot ranking
hotspot velocity
significant co-change
centrality over coupling graph
```

## 6. Prompt-file packaging references

Microsoft:
https://github.com/microsoft/skills/blob/main/.github/prompts/code-review.prompt.md

GitHub:
https://docs.github.com/en/copilot/tutorials/customization-library/prompt-files/review-code

Useful packaging pattern:

```text
small named prompt file
+ explicit role
+ bounded review areas
+ structured output
+ optional focus argument
```

Planning Lite should reuse the packaging idea only if it fits existing `control/*.md`
and skill architecture.

## 7. Reuse classification template

```yaml
asset: ...
source: ...
purpose_match: ...
semantic_match: FULL | PARTIAL | NONE
provenance_status: QUALIFIED | REFERENCE_ONLY | UNKNOWN
decision: REUSE | ADAPT | REFERENCE_ONLY | NO_MATCH
reason: ...
```

This keeps "we found some code" separate from "this code is safe to productize".
