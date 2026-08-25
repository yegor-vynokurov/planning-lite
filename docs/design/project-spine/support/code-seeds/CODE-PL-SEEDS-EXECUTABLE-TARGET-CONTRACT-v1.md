# CODE-PL-SEEDS-EXECUTABLE-TARGET-CONTRACT-v1
## Reusable prompts, schemas, and small code seeds

**Status:** `DRAFT / REUSABLE ASSET`
**Date:** `2026-08-21`

**Suggested code-companion location:**
`.planning-lab/recommendations/active/CODE-PL-SEEDS-EXECUTABLE-TARGET-CONTRACT-v1.md`

---

# 1. Prompt seed — derive System Claims from an Outcome Level

```text
You are defining an Executable Target Contract.

Input:
- approved Outcome Level;
- target users/value;
- current specification;
- known safety/evidence boundaries.

Task:

1. State 3–7 externally meaningful System Claims for this Outcome Level.
2. Do not mirror implementation structure.
3. Separate claims into:
   - STRUCTURAL
   - SUCCESS_BEHAVIOR
   - FAILURE_OR_DEGRADATION
4. For each claim state:
   - who receives value;
   - what observable behavior proves it;
   - what observable behavior would falsify it;
   - the cheapest adequate evidence channel.
5. Do not invent implementation details.
6. Do not require claims belonging only to a higher Outcome Level.

Output table:
Claim ID | Class | Claim | Observable proof | Falsifier | Evidence channel
```

---

# 2. Prompt seed — turn claims into canonical Target Scenarios

```text
Given the approved System Claims, create the smallest useful canonical
Target Scenario suite.

Prefer 3–7 scenarios total for the first pass.

Include:
- at least one core success path;
- at least one material failure/degradation path;
- ambiguity/unsupported behavior if relevant;
- reproducibility/integration scenario if material.

For each scenario return:

scenario_id
claim_id
preconditions
input
expected_observable_behavior
forbidden_observable_behavior
evidence_channel
initial_status:
  DEFINED

Do not write implementation code.
Do not create duplicate scenarios for stylistic variants.
Choose scenarios that would materially change our belief that the target works.
```

---

# 3. Prompt seed — failure/degradation scenario extraction

```text
For each approved System Claim ask:

"If the system cannot honestly satisfy this claim in the current situation,
what must it do instead?"

Generate only material failure/degradation behaviors.

Look for:
- insufficient evidence;
- ambiguity;
- invalid input;
- unavailable dependency/tool;
- partial execution;
- unsupported capability;
- timeout/resource failure;
- provenance/reproducibility failure.

Prefer explicit fail-closed / abstain / clarify / durable-incomplete behavior
over plausible fake success.

Return:
Claim | Failure condition | Required observable degradation | Forbidden behavior
```

---

# 4. Prompt seed — choose evidence channel

```text
For each Target Scenario, choose the cheapest evidence channel that could
actually falsify the belief that the behavior works.

Candidate channels:
- unit/property/contract test
- integration/end-to-end
- browser/DOM/visual/live interaction
- reload/restart/recovery
- benchmark/profiling
- negative/adversarial probe
- controlled experiment/holdout
- rerun/identity comparison
- smoke/health/observability
- human task review
- deterministic grader
- LLM rubric judge

Do not choose "unit test" by default.
Explain in one sentence why the chosen channel observes the actual failure class.
```

---

# 5. YAML seed — claims/scenarios registry

```yaml
version: executable-target-contract-v1

outcome_levels:
  L2:
    name: useful
    claims:
      - CHEM-CLAIM-01
      - CHEM-CLAIM-02

claims:
  CHEM-CLAIM-01:
    class: success_behavior
    statement: >
      Supported chemistry questions receive materially correct grounded answers.
    evidence_channel: llm_eval

  CHEM-CLAIM-02:
    class: failure_or_degradation
    statement: >
      Unsupported questions do not receive fabricated confident answers.
    evidence_channel: llm_eval

scenarios:
  TC-CHEM-01:
    claim_id: CHEM-CLAIM-01
    status:
      defined: true
      wired: false
      passing: false
    input:
      question: "Why does carbonate release gas when acid is added?"
    expected:
      - identifies carbon dioxide
      - explains reaction mechanism
      - uses retrieved evidence
    forbidden:
      - fabricated source attribution

  TC-CHEM-02:
    claim_id: CHEM-CLAIM-02
    status:
      defined: true
      wired: false
      passing: false
    input:
      question: "<unsupported question fixture>"
    expected:
      - reports insufficient support or abstains
    forbidden:
      - confident unsupported answer
```

---

# 6. Python seed — scenario state

```python
from dataclasses import dataclass
from enum import Enum


class ScenarioState(str, Enum):
    DEFINED = "defined"
    WIRED = "wired"
    PASSING = "passing"


@dataclass(frozen=True)
class ScenarioStatus:
    defined: bool
    wired: bool
    passing: bool

    def state(self) -> ScenarioState:
        if self.passing:
            if not self.wired or not self.defined:
                raise ValueError("passing requires wired and defined")
            return ScenarioState.PASSING
        if self.wired:
            if not self.defined:
                raise ValueError("wired requires defined")
            return ScenarioState.WIRED
        if self.defined:
            return ScenarioState.DEFINED
        raise ValueError("scenario must at least be defined")
```

Purpose:
- preserve the distinction between a specified target,
  an executable probe,
  and a demonstrated behavior.

---

# 7. Python seed — simple deterministic criteria grader

```python
from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class Criterion:
    name: str
    check: Callable[[dict], bool]


@dataclass(frozen=True)
class CriterionResult:
    name: str
    passed: bool


def grade_observation(
    observation: dict,
    criteria: list[Criterion],
) -> list[CriterionResult]:
    return [
        CriterionResult(name=c.name, passed=bool(c.check(observation)))
        for c in criteria
    ]
```

Use only when scenario criteria can genuinely be checked deterministically.

Do not force semantic behavior into brittle keyword checks.

---

# 8. Python seed — claim result aggregation

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class ScenarioResult:
    scenario_id: str
    claim_id: str
    passing: bool


def claim_is_demonstrated(
    claim_id: str,
    results: list[ScenarioResult],
    required_scenario_ids: set[str],
) -> bool:
    by_id = {
        r.scenario_id: r
        for r in results
        if r.claim_id == claim_id
    }
    return all(
        sid in by_id and by_id[sid].passing
        for sid in required_scenario_ids
    )
```

The mapping from claim → required scenarios should be explicit in the registry.

---

# 9. Python seed — highest demonstrated Outcome Level

```python
def highest_demonstrated_level(
    ordered_levels: list[str],
    level_required_claims: dict[str, set[str]],
    demonstrated_claims: set[str],
) -> str | None:
    highest = None
    for level in ordered_levels:
        required = level_required_claims[level]
        if required.issubset(demonstrated_claims):
            highest = level
        else:
            break
    return highest
```

Assumption:
- levels are cumulative.

If a project uses non-cumulative Outcome Levels, do not use this helper.

---

# 10. Prompt seed — assess current system against target scenarios

```text
Do NOT improve the system in this pass.

Run/inspect the current system against the approved Target Scenarios.

For every scenario classify:

DEFINED_ONLY
WIRED_FAIL
WIRED_PASS
BLOCKED_BY_MISSING_PROBE
BLOCKED_BY_ENVIRONMENT

Report separately:

Implementation Gap:
what target behavior is absent.

Evidence Gap:
what required proof is missing or not wired.

Do not infer PASS from local unit tests unless the scenario's approved
evidence channel is actually exercised.
```

---

# 11. Prompt seed — target-skeleton integration

```text
Given:
- Target Skeleton;
- System Claims;
- Target Scenarios;

reconcile them.

For every main skeleton path identify:
- which structural claim it supports;
- which behavior scenarios traverse it;
- which missing capability remains an explicit placeholder.

Expected early state:

Structural claims:
mostly WIRED/PASSING

Behavior claims:
mixed DEFINED / WIRED_FAIL / PASSING

Do not replace missing behavior with fake success merely to make the skeleton green.
```

---

# 12. Prompt seed — derive vertical slices from scenarios

```text
Generate candidate vertical slices from the current Target Scenario states.

Prefer slices that move a meaningful scenario:

DEFINED → WIRED
or
WIRED_FAIL → PASSING

Each slice must state:

- System Claim advanced;
- Target Scenario advanced;
- current failure/missing behavior;
- implementation surfaces likely touched;
- evidence channel that will prove completion;
- failure scenario that must remain correct.

Do not prefer a slice merely because it fills one architectural layer.
```

---

# 13. Example chemistry eval case format

```yaml
scenario_id: TC-CHEM-UNSUPPORTED-01
claim_id: CHEM-CLAIM-ABSTAIN
class: failure_or_degradation

input:
  question: "<question unsupported by current corpus>"

expected_behavior:
  must:
    - recognize insufficient support
    - abstain or explicitly bound uncertainty
  must_not:
    - fabricate a source
    - present unsupported answer as certain

evidence_channel:
  type: hybrid_eval
  deterministic_checks:
    - structured certainty field below threshold
    - no unknown citation ids
  semantic_judge:
    rubric: >
      Does the response clearly avoid asserting unsupported chemistry content
      as established fact?
```

---

# 14. Example portfolio-level claim suite

```yaml
outcome_level: L1
name: portfolio_quality_repository

claims:
  - id: PORT-01
    statement: repository installs from documented instructions
    evidence_channel: clean_install_smoke

  - id: PORT-02
    statement: automated tests execute successfully
    evidence_channel: test_runner

  - id: PORT-03
    statement: documented demo completes end-to-end
    evidence_channel: demo_smoke

  - id: PORT-04
    statement: documented result is reproducible
    evidence_channel: clean_rerun
```

This is intentionally simpler than a useful/trustworthy production system suite.

---

# 15. Prompt seed — challenge claims for overreach

```text
Review the proposed System Claims against the selected Outcome Level.

For each claim classify:

REQUIRED_FOR_LEVEL
BELONGS_TO_HIGHER_LEVEL
IMPLEMENTATION_DETAIL
TOO_VAGUE_TO_TEST
DUPLICATE

Remove or rewrite anything that exceeds the current Outcome Level.

A lower Outcome Level may claim fewer capabilities,
but any claimed capability must still meet its correctness/safety floor.
```

---

# 16. Suggested first Planning Lite fixture

Use the chemistry assistant because success and failure behavior are both natural.

Start with exactly five scenarios:

```text
2 supported questions
1 unsupported question
1 ambiguous question
1 false-premise question
```

Record before changing the bot:

```text
DEFINED?
WIRED?
PASSING?
Implementation Gap?
Evidence Gap?
```

This provides a clean first field test of the recommendation.
