# REC-PL-CHANGE-COST-001 v1
## Evidence-derived Change Cost profiles for Roadmap bottlenecks and alternative comparison

**Status:** PROVISIONAL / RESEARCH-CORROBORATED / FIELD-CANDIDATE / OPEN
**Date:** 2026-08-20
**Primary motivation:** make Roadmap difficulty decomposable and measurable rather than a subjective "hard/easy" label
**Implementation authority:** none
**Recommended canonical location:** `docs/design/project-spine/REC-PL-CHANGE-COST-001-v1.md`

## 1. Problem

Current Planning Lite Roadmap prioritization intentionally avoids fake weighted
precision. That is correct.

However, Planning Lite can still measure real structural and historical properties of
proposed Changes.

The useful question is:

```text
Where does the expected cost of this Roadmap item come from,
and which design decision creates the bottleneck?
```

This makes alternative search concrete.

## 2. External prior art

### Propagation cost / Design Structure Matrices
SEI describes propagation cost as the percentage of system elements affected when a
change is made and uses dependency/architecture representations to estimate rework
and technical-debt impact.

References:
- https://www.sei.cmu.edu/blog/developing-an-architecture-focused-measurement-framework-for-managing-technical-debt/
- https://insights.sei.cmu.edu/library/managing-technical-debt-in-software-reliant-systems-2/

### Change entropy
Ahmed Hassan's ICSE work models complexity of the change process with
information-theoretic entropy over file modifications.

Reference:
- DOI 10.1109/ICSE.2009.5070510
- https://www.researchgate.net/publication/221554415_Predicting_faults_using_the_complexity_of_code_changes

### Behavioral code analysis
Code Maat mines version-control history for revisions, churn, logical coupling,
ownership, and fragmentation.

Reference:
- https://github.com/adamtornhill/code-maat

CodeScene emphasizes hotspots: problematic code matters most economically when it is
changed often.

Reference:
- https://codescene.com/docs/CodeSceneUseCasesAndRoles.pdf

CodeLore is a newer open-source transparent reference for hotspots and co-change.

Reference:
- https://github.com/emrecdr/codelore

## 3. Recommendation

Planning Lite should evaluate an **evidence-derived Change Cost Profile**.

Initially it should be a vector, not a single synthetic score:

```yaml
change_cost_profile:
  planned_surface:
    files: ...
    modules: ...
    contracts: ...
    data_schemas: ...
  architecture:
    direct_dependents: ...
    reachable_dependents: ...
    propagation_ratio: ...
  history:
    touched_hotspot_percentile: ...
    revision_frequency: ...
    logical_coupling_edges: ...
    change_entropy: ...
  mechanism_delta:
    components: ...
    persistent_artifact_types: ...
    identities: ...
    mutable_states: ...
    state_transitions: ...
    retry_failure_branches: ...
    platform_specific_branches: ...
    config_dimensions: ...
    external_dependencies: ...
  verification_delta:
    named_tests: ...
    scripts: ...
    expensive_runs: ...
  process_actuals:
    planning_loops: ...
    readiness_loops: ...
    tool_calls: ...
    input_tokens: ...
    output_tokens: ...
    human_gates: ...
    test_runtime_seconds: ...
```

## 4. Metric families

### Change Surface
Measure files, modules/packages, contracts, schemas/artifact formats, workflows, tests,
and platform branches. LOC/churn are supporting measures, not the sole measure.

### Propagation / blast radius
From dependency or architecture graphs:

```text
proposed touched nodes
→ direct dependents
→ transitive reachable dependents
→ relevant propagation ratio
```

High propagation is a signal, not automatic proof of bad design.

### Historical change coupling
Use Git history to identify files/modules that repeatedly change together.

### Hotspot exposure
Combine historical touch frequency with a local complexity/code-health signal.

### Change-process entropy
Candidate normalized entropy:

```text
H = -sum(p_i * log(p_i)) / log(n)
```

Use comparatively, not as proof of defects.

### Mechanism Delta
Planning Lite can measure before implementation:

```text
Δ components
Δ artifact types
Δ identities
Δ mutable states
Δ transitions
Δ retry/failure branches
Δ concurrency/lease mechanisms
Δ platform adapters
Δ config dimensions
Δ dependencies
Δ verification seams
```

### Verification burden
Record named executable seams, expensive tests/runs, cross-platform verification,
repeated/recovery runs, and human gates.

### Carry cost
Initial transparent proxy:

```text
carry_exposure
≈ introduced_mechanism_surface × historical_touch_probability
```

Do not turn this into money or a universal score without calibration.

## 5. "Objective" means repeatable evidence, not false certainty

Measured/repeatable:
- files/modules touched;
- dependency reachability;
- Git revision counts;
- co-change frequency;
- declared state/transition counts;
- test count/runtime;
- lifecycle loops/tool calls/tokens after completion.

Estimated/probabilistic:
- future touched surface;
- likely companion modules;
- expected lifecycle effort;
- future carry cost.

No opaque LLM `complexity = 8/10`.

## 6. Roadmap use

A Roadmap candidate should eventually expose:

```text
Outcome: RM-...
Value / Gap impact: HIGH
Change Cost Profile: ...
Primary cost drivers:
  1. recovery/artifact state machine
  2. platform-specific process identity
  3. high-coupling evaluator seam
Alternative search target:
  "simpler immutable research-attempt model"
```

This turns cost analysis into a search lens.

## 7. Alternative comparison

Compare delta profiles for designs serving the same requirement.

Example:

```text
B versus A:
  platform adapters:       -2
  liveness identities:     -4
  mutable transitions:     -6
  retry branches:          -3
  requirements retained:   7/7
```

This is more useful than "B is simpler."

## 8. Keep value and cost separate initially

Do not immediately collapse Roadmap value and Change cost into one number.

Later, after calibration, Planning Lite may experiment with:

```text
expected gap reduction / expected change cost
```

but never let that silently override human Roadmap authority.

## 9. Calibration against actual governed Changes

For completed Changes, capture:
- files changed;
- insertions/deletions;
- implementation commits;
- tests added;
- test runtime;
- Planning loops;
- Readiness loops;
- Verification loops;
- tool calls;
- tokens when available;
- reliable wall-clock time;
- human approval turns;
- failed/repeated attempts.

Then compare:

```text
ROADMAP ESTIMATE
→ PLANNING ESTIMATE
→ ACTUAL COST
```

After enough Changes, fit a small transparent model or calibrated lookup rather than
hand-authoring weights.

## 10. Minimal implementation path

### C0 — profile only
No composite score. Record planned surface, mechanism delta, verification delta, and a
few Git-history measures. Use `CHG-0009` as an initial fixture.

### C1 — deterministic repository extractor
Prototype outside product runtime:
- Git revisions/churn;
- co-change pairs;
- dependency reachability where practical.

### C2 — actual-cost receipts
Capture lifecycle actuals for new completed Changes.

### C3 — bounded backfill
Backfill only historical Changes whose boundaries are reliable.

### C4 — calibration experiment
Test whether profile features predict observed lifecycle burden. Only then consider a
composite expected-cost model.

## 11. Code/reference assets for the code companion

### Code Maat
https://github.com/adamtornhill/code-maat

Useful existing analyses:
```text
revisions
entity-churn
coupling
soc
ownership
fragmentation
```

### CodeLore
https://github.com/emrecdr/codelore

Useful reference ideas:
```text
hotspot ranking
hotspot velocity
significant co-change
centrality over coupling graph
```

### Deterministic seed: normalized entropy

```python
from math import log

def normalized_entropy(counts):
    counts = [c for c in counts if c > 0]
    if len(counts) <= 1:
        return 0.0
    total = sum(counts)
    probs = [c / total for c in counts]
    return -sum(p * log(p) for p in probs) / log(len(probs))
```

### Deterministic seed: propagation ratio

```python
def propagation_ratio(graph, seeds):
    reached = set(seeds)
    stack = list(seeds)
    while stack:
        node = stack.pop()
        for nxt in graph.get(node, ()):
            if nxt not in reached:
                reached.add(nxt)
                stack.append(nxt)
    return len(reached) / max(1, len(graph))
```

These are seed examples, not product contracts.

## 12. Relationship to current Roadmap semantics

Current Project Spine Roadmap intentionally uses qualitative prioritization and rejects
fake weighted precision.

This recommendation does not reverse that decision. It proposes:

```text
qualitative value/prioritization
+
measured structural cost profile
```

until calibration evidence exists.

## 13. Suggested future placement

Do not add a new `PL-V38-*` stage immediately.

- preserve as a Project Spine recommendation now;
- use `CHG-0009` as first retrospective cost-profile fixture;
- inspect existing Lab/code-companion assets before implementation;
- consider deterministic extractor/eval work when `PL-V38-06A/06B` reactivates assets;
- integrate with Roadmap synthesis only after measurement semantics are validated.

## 14. Anti-overreach

Do not invent weights before calibration, use LOC as sole cost measure, treat high
coupling as automatically bad, optimize Roadmap solely for cheapest items, turn
external tools into consumer dependencies, infer individual developer performance
from repository metrics, or let a composite score override explicit human priority.
