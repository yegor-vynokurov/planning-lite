"""Pure, deterministic Plan/task/proposal compilation for 09-E.

This module deliberately accepts already-read source text and mappings.  It has
no filesystem, Git, network, telemetry, model, CLI, or persistence boundary.
"""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
import hashlib
import json
import re
from typing import Any, Mapping, Sequence


TASK_COLUMNS = (
    "ID",
    "Outcome",
    "Slice type",
    "Blocking edge",
    "Verification seam / command",
    "Blast radius",
    "Status",
)
TASK_STATUSES = ("Pending", "In progress", "Blocked", "Done", "Cancelled")
TASK_ID_RE = re.compile(r"^T-[0-9]{2,}$")
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")

WORK_CAPABILITIES = (
    "INTENT_REQUIREMENTS",
    "DOMAIN_SEMANTICS",
    "REPOSITORY_UNDERSTANDING",
    "ARCHITECTURE_INTERFACES",
    "DEPENDENCY_PLANNING",
    "IMPLEMENTATION",
    "TOOL_RUNTIME_OPERATION",
    "VERIFICATION_TEST_DESIGN",
    "SEMANTIC_REVIEW",
    "EVIDENCE_GOVERNANCE",
)
CROSS_CUTTING_TAGS = (
    "LONG_CONTEXT_SYNTHESIS",
    "ESTIMATION_UNCERTAINTY",
    "RESEARCH_DISCOVERY",
)
EXECUTOR_PROFILES = (
    "STRONG_AUTONOMOUS",
    "BOUNDED_WORKER",
    "JUNIOR_EXECUTOR",
    "MECHANICAL_EDITOR",
)
DISPOSITIONS = ("KEEP_UNIT", "CAPABILITY_COUPLED", "SPLIT_RECOMMENDED")
CRITERIA = tuple(f"C{i:02d}" for i in range(1, 14))
CRITERION_LABELS = {
    "C01": "ATOMICITY / PRIMARY COMPLETION BOUNDARY",
    "C02": "DEPENDENCY COMPLETENESS AND ORDER",
    "C03": "PRECONDITIONS / INPUTS",
    "C04": "AUTHORITY AND SCOPE",
    "C05": "EXECUTOR DECISION BUDGET",
    "C06": "INTERFACE / CONTRACT SUFFICIENCY",
    "C07": "WORK-CAPABILITY SIGNATURE",
    "C08": "CAPABILITY SPLIT / COUPLING DECISION",
    "C09": "TYPED HANDOFF IF REQUIRED",
    "C10": "VERIFICATION",
    "C11": "EVIDENCE UPDATE",
    "C12": "FAILURE / STOP / RECOVERY",
    "C13": "DOWNSTREAM CONSISTENCY",
}
SPLIT_ASSERTIONS = tuple(f"S{i}" for i in range(1, 7))

PROPOSAL_KEYS = frozenset(
    {
        "schema_version",
        "source_binding",
        "units",
        "existing_dependency_handoffs",
        "controlled_discoveries",
        "semantic_assessment_source",
        "semantic_evidence_refs",
    }
)
SOURCE_BINDING_KEYS = frozenset({"plan_ref", "plan_sha256", "tasks_ref", "tasks_sha256"})
UNIT_KEYS = frozenset(
    {
        "original_unit_id",
        "work_capabilities",
        "cross_cutting_tags",
        "target_executor_profile",
        "already_decided",
        "allowed_executor_decisions",
        "forbidden_executor_decisions",
        "disposition",
        "derived_units",
        "new_internal_edges",
        "internal_handoffs",
        "criterion_assertions",
        "material_findings",
    }
)
DERIVED_UNIT_KEYS = frozenset(
    {
        "unit_id",
        "outcome",
        "work_capabilities",
        "cross_cutting_tags",
        "target_executor_profile",
        "already_decided",
        "allowed_executor_decisions",
        "forbidden_executor_decisions",
        "criterion_assertions",
        "material_findings",
    }
)
CRITERION_ASSERTION_KEYS = frozenset({"criterion", "verdict", "reason", "evidence_refs"})
HANDOFF_KEYS = frozenset(
    {
        "source_unit",
        "target_unit",
        "produced_refs",
        "accepted_output_contract",
        "required_downstream_inputs",
        "authority_constraints",
        "allowed_open_questions",
        "forbidden_decisions",
        "verification_evidence",
        "failure_stop_state",
    }
)
DISCOVERY_KEYS = frozenset(
    {
        "unit_ref",
        "question",
        "scope_bound",
        "stop_condition",
        "output_contract",
        "verification_before_dependent_work",
    }
)


class PlanCompilationError(ValueError):
    """Base error for invalid compiler input or compiler invariants."""

    def __init__(self, message: str, code: str = "PROPOSAL_SCHEMA_INVALID") -> None:
        super().__init__(message)
        self.code = code


class PlanCompilationInputError(PlanCompilationError):
    """An input cannot produce a valid structured compilation result."""


class PlanCompilationInvariantError(PlanCompilationError):
    """An unexpected internal contract violation occurred."""


class TaskGraphError(PlanCompilationInputError):
    """The managed task table cannot be parsed under the frozen grammar."""


@dataclass(frozen=True)
class OriginalTaskUnitV1:
    task_id: str
    outcome: str
    slice_type: str
    blocking_edges: tuple[str, ...]
    verification: str
    blast_radius: str
    status: str

    def to_mapping(self) -> dict[str, Any]:
        return {
            "id": self.task_id,
            "outcome": self.outcome,
            "slice_type": self.slice_type,
            "blocking_edges": list(self.blocking_edges),
            "verification": self.verification,
            "blast_radius": self.blast_radius,
            "status": self.status,
        }


@dataclass(frozen=True)
class OriginalTaskGraphV1:
    units: tuple[OriginalTaskUnitV1, ...]
    edges: tuple[tuple[str, str], ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "units": [unit.to_mapping() for unit in self.units],
            "edges": [
                {"source": source, "target": target}
                for source, target in self.edges
            ],
        }


@dataclass(frozen=True)
class CompilationFindingV1:
    finding_code: str
    material: bool = True
    unit_ref: str | None = None
    evidence: tuple[str, ...] = ()
    message: str = ""

    def to_mapping(self) -> dict[str, Any]:
        return {
            "finding_code": self.finding_code,
            "material": self.material,
            "unit_ref": self.unit_ref,
            "evidence": list(self.evidence),
            "message": self.message,
        }


@dataclass(frozen=True)
class TypedHandoffV1:
    source_unit: str
    target_unit: str
    produced_refs: tuple[Any, ...]
    accepted_output_contract: Any
    required_downstream_inputs: tuple[Any, ...]
    authority_constraints: Any
    allowed_open_questions: tuple[Any, ...]
    forbidden_decisions: tuple[Any, ...]
    verification_evidence: tuple[Any, ...]
    failure_stop_state: Any

    def to_mapping(self) -> dict[str, Any]:
        return {
            "source_unit": self.source_unit,
            "target_unit": self.target_unit,
            "produced_refs": list(self.produced_refs),
            "accepted_output_contract": self.accepted_output_contract,
            "required_downstream_inputs": list(self.required_downstream_inputs),
            "authority_constraints": self.authority_constraints,
            "allowed_open_questions": list(self.allowed_open_questions),
            "forbidden_decisions": list(self.forbidden_decisions),
            "verification_evidence": list(self.verification_evidence),
            "failure_stop_state": self.failure_stop_state,
        }


@dataclass(frozen=True)
class CoverageAssertionV1:
    criterion: str
    verdict: str
    reason: str
    evidence_refs: tuple[Any, ...]

    def to_mapping(self) -> dict[str, Any]:
        return {
            "criterion": self.criterion,
            "verdict": self.verdict,
            "reason": self.reason,
            "evidence_refs": list(self.evidence_refs),
        }


@dataclass(frozen=True)
class ControlledDiscoveryV1:
    unit_ref: str
    question: str
    scope_bound: str
    stop_condition: str
    output_contract: str
    verification_before_dependent_work: str

    def to_mapping(self) -> dict[str, str]:
        return {
            "unit_ref": self.unit_ref,
            "question": self.question,
            "scope_bound": self.scope_bound,
            "stop_condition": self.stop_condition,
            "output_contract": self.output_contract,
            "verification_before_dependent_work": self.verification_before_dependent_work,
        }


def canonical_json(value: Any) -> str:
    """Return the frozen canonical JSON representation without a trailing LF."""

    return json.dumps(
        value,
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )


def _clean_cell(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        return value[1:-1].strip()
    return value


def _split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [_clean_cell(cell) for cell in stripped[1:-1].split("|")]


def _is_separator_row(row: Sequence[str]) -> bool:
    return bool(row) and all(bool(re.fullmatch(r":?-{3,}:?", cell.strip())) for cell in row)


def _task_error(code: str, message: str) -> TaskGraphError:
    return TaskGraphError(message, code)


def parse_task_table(markdown: str) -> OriginalTaskGraphV1:
    """Parse exactly one task table using the bounded Markdown table grammar."""

    if not isinstance(markdown, str):
        raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", "tasks input must be text")

    lines = markdown.splitlines()
    candidates: list[int] = []
    for index, line in enumerate(lines[:-1]):
        row = _split_table_row(line)
        if row == list(TASK_COLUMNS):
            separator = _split_table_row(lines[index + 1])
            if separator is not None and _is_separator_row(separator) and len(separator) == len(TASK_COLUMNS):
                candidates.append(index)
    if not candidates:
        raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", "exact task table is missing")
    if len(candidates) != 1:
        raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", "multiple eligible task tables found")

    start = candidates[0] + 2
    rows: list[list[str]] = []
    index = start
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            break
        row = _split_table_row(line)
        if row is None:
            break
        if len(row) != len(TASK_COLUMNS):
            raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", "task table row has wrong column count")
        rows.append(row)
        index += 1
    if not rows:
        raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", "task table has no task rows")

    task_ids: set[str] = set()
    raw_rows: list[tuple[list[str], str]] = []
    for row in rows:
        task_id = row[0]
        if not TASK_ID_RE.fullmatch(task_id):
            raise _task_error("MALFORMED_TASK_ID", f"malformed task ID: {task_id}")
        if task_id in task_ids:
            raise _task_error("DUPLICATE_TASK_ID", f"duplicate task ID: {task_id}")
        task_ids.add(task_id)
        status = row[6]
        if status not in TASK_STATUSES:
            raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", f"unsupported task status: {status}")
        raw_rows.append((row, task_id))

    row_order = {task_id: index for index, (_, task_id) in enumerate(raw_rows)}
    units: list[OriginalTaskUnitV1] = []
    edges: list[tuple[str, str]] = []
    for row, task_id in raw_rows:
        dependency_text = row[3]
        if dependency_text == "None":
            dependencies: list[str] = []
        else:
            if not dependency_text or any(token in dependency_text for token in ("/", "+", "..")):
                raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", f"invalid Blocking edge: {dependency_text}")
            dependencies = [part.strip() for part in dependency_text.split(",")]
            if any(not TASK_ID_RE.fullmatch(part) for part in dependencies):
                raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", f"invalid Blocking edge: {dependency_text}")
            if len(set(dependencies)) != len(dependencies):
                raise _task_error("UNSUPPORTED_TASK_GRAPH_GRAMMAR", f"duplicate dependency: {dependency_text}")
            if task_id in dependencies:
                raise _task_error("SELF_DEPENDENCY", f"self dependency: {task_id}")
            unknown = [dependency for dependency in dependencies if dependency not in task_ids]
            if unknown:
                raise _task_error("UNKNOWN_DEPENDENCY_TASK", f"unknown dependency: {unknown[0]}")
            edges.extend((dependency, task_id) for dependency in dependencies)
            dependencies = sorted(dependencies, key=lambda dependency: row_order[dependency])
            edges[-len(dependencies) :] = [(dependency, task_id) for dependency in dependencies]
        units.append(
            OriginalTaskUnitV1(
                task_id=task_id,
                outcome=row[1],
                slice_type=row[2],
                blocking_edges=tuple(dependencies),
                verification=row[4],
                blast_radius=row[5],
                status=row[6],
            )
        )

    _ensure_acyclic(tuple(task_ids), tuple(edges))
    return OriginalTaskGraphV1(tuple(units), tuple(edges))


def _ensure_acyclic(nodes: Sequence[str], edges: Sequence[tuple[str, str]]) -> None:
    outgoing: dict[str, list[str]] = {node: [] for node in nodes}
    indegree: dict[str, int] = {node: 0 for node in nodes}
    for source, target in edges:
        outgoing[source].append(target)
        indegree[target] += 1
    queue = deque(node for node in nodes if indegree[node] == 0)
    visited = 0
    while queue:
        node = queue.popleft()
        visited += 1
        for target in outgoing[node]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)
    if visited != len(nodes):
        raise _task_error("TASK_GRAPH_CYCLE", "task graph contains a cycle")


def _require_mapping(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise PlanCompilationInputError(f"{label} must be an object")
    return value


def _require_exact_keys(value: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    actual = set(value)
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if extra:
            detail.append("unknown " + ", ".join(extra))
        raise PlanCompilationInputError(f"{label}: " + "; ".join(detail))


def _require_list(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise PlanCompilationInputError(f"{label} must be an array")
    return value


def _require_string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PlanCompilationInputError(f"{label} must be a non-empty string")
    return value


def _validate_sha(value: Any, label: str) -> str:
    if not isinstance(value, str) or not SHA256_RE.fullmatch(value):
        raise PlanCompilationInputError(f"{label} must be a 64-character hexadecimal SHA-256")
    return value.lower()


def _finding(
    code: str,
    *,
    unit_ref: str | None = None,
    evidence: Sequence[str] = (),
    message: str = "",
) -> dict[str, Any]:
    return CompilationFindingV1(
        code,
        True,
        unit_ref,
        tuple(evidence),
        message or code,
    ).to_mapping()


def _normalise_edge(value: Any) -> tuple[str, str] | None:
    if isinstance(value, Mapping):
        source = value.get("source", value.get("source_unit"))
        target = value.get("target", value.get("target_unit"))
        if isinstance(source, str) and isinstance(target, str):
            return source, target
    if isinstance(value, list) and len(value) == 2 and all(isinstance(item, str) for item in value):
        return value[0], value[1]
    return None


def _validate_handoff(value: Any, label: str) -> TypedHandoffV1 | None:
    if not isinstance(value, Mapping) or set(value) != HANDOFF_KEYS:
        return None
    source = value["source_unit"]
    target = value["target_unit"]
    if not isinstance(source, str) or not isinstance(target, str):
        return None
    plural = (
        "produced_refs",
        "required_downstream_inputs",
        "allowed_open_questions",
        "forbidden_decisions",
        "verification_evidence",
    )
    if any(not isinstance(value[field], list) for field in plural):
        return None
    return TypedHandoffV1(
        source,
        target,
        tuple(value["produced_refs"]),
        value["accepted_output_contract"],
        tuple(value["required_downstream_inputs"]),
        value["authority_constraints"],
        tuple(value["allowed_open_questions"]),
        tuple(value["forbidden_decisions"]),
        tuple(value["verification_evidence"]),
        value["failure_stop_state"],
    )


def _extract_derived_id(value: Any) -> str | None:
    if isinstance(value, str):
        return value.strip() or None
    if isinstance(value, Mapping):
        for key in ("unit_id", "id", "unit_ref"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.strip():
                return candidate.strip()
    return None


def _reachable(nodes: Sequence[str], edges: Sequence[tuple[str, str]]) -> set[tuple[str, str]]:
    outgoing: dict[str, list[str]] = defaultdict(list)
    for source, target in edges:
        outgoing[source].append(target)
    result: set[tuple[str, str]] = set()
    for source in nodes:
        pending = list(outgoing[source])
        seen: set[str] = set()
        while pending:
            target = pending.pop()
            if target in seen:
                continue
            seen.add(target)
            result.add((source, target))
            pending.extend(outgoing[target])
    return result


def _canonical_edge_list(edges: Sequence[tuple[str, str]], order: Mapping[str, int]) -> list[dict[str, str]]:
    unique = set(edges)
    return [
        {"source": source, "target": target}
        for source, target in sorted(unique, key=lambda edge: (order.get(edge[0], 10**9), order.get(edge[1], 10**9)))
    ]


def _validate_coverage(
    unit_ref: str,
    assertions: Any,
    findings: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], bool]:
    if not isinstance(assertions, list):
        findings.append(_finding("COVERAGE_INCOMPLETE", unit_ref=unit_ref, message="criterion_assertions must be an array"))
        return [], False
    seen: set[str] = set()
    result: list[dict[str, Any]] = []
    valid = True
    for raw in assertions:
        if not isinstance(raw, Mapping):
            findings.append(_finding("INVALID_CRITERION_VALUE", unit_ref=unit_ref, message="coverage assertion must be an object"))
            valid = False
            continue
        criterion = raw.get("criterion")
        verdict = raw.get("verdict")
        reason = raw.get("reason")
        evidence_refs = raw.get("evidence_refs")
        if criterion not in CRITERIA or criterion in seen:
            findings.append(_finding("INVALID_CRITERION_VALUE", unit_ref=unit_ref, message=f"invalid or duplicate criterion: {criterion}"))
            valid = False
            continue
        seen.add(criterion)
        if verdict not in ("PASS", "FAIL", "N/A") or not isinstance(reason, str) or not reason.strip() or not isinstance(evidence_refs, list):
            findings.append(_finding("INVALID_CRITERION_VALUE", unit_ref=unit_ref, message=f"invalid assertion for {criterion}"))
            valid = False
            continue
        assertion = CoverageAssertionV1(criterion, verdict, reason, tuple(evidence_refs)).to_mapping()
        result.append(assertion)
        if verdict == "FAIL":
            findings.append(_finding("UNRESOLVED_MATERIAL_FINDING", unit_ref=unit_ref, message=f"coverage assertion {criterion} is FAIL"))
            valid = False
    missing = [criterion for criterion in CRITERIA if criterion not in seen]
    if missing:
        findings.append(_finding("COVERAGE_INCOMPLETE", unit_ref=unit_ref, evidence=missing, message="mandatory coverage is incomplete"))
        valid = False
    return result, valid


def _validate_string_array(value: Any, label: str) -> list[str]:
    values = _require_list(value, label)
    if any(not isinstance(item, str) or not item.strip() for item in values):
        raise PlanCompilationInputError(
            f"{label} must contain non-empty strings",
            code="PROPOSAL_SCHEMA_INVALID",
        )
    return [item.strip() for item in values]


def _schema_error(label: str, message: str) -> PlanCompilationInputError:
    return PlanCompilationInputError(f"{label}: {message}", code="PROPOSAL_SCHEMA_INVALID")


def _validated_enum(value: Any, allowed: Sequence[str], label: str) -> str:
    if not isinstance(value, str) or value not in allowed:
        raise _schema_error(label, f"unknown value: {value!r}")
    return value


def _validated_enum_array(value: Any, allowed: Sequence[str], label: str) -> list[str]:
    values = _validate_string_array(value, label)
    unknown = [item for item in values if item not in allowed]
    if unknown:
        raise _schema_error(label, f"unknown value: {unknown[0]!r}")
    return values


def _validate_criterion_assertion_shape(value: Any, label: str) -> list[Mapping[str, Any]]:
    assertions = _require_list(value, label)
    result: list[Mapping[str, Any]] = []
    for index, assertion in enumerate(assertions):
        if not isinstance(assertion, Mapping):
            raise _schema_error(label, f"item {index} must be an object")
        _require_exact_keys(assertion, CRITERION_ASSERTION_KEYS, f"{label}[{index}]")
        if not isinstance(assertion["criterion"], str):
            raise _schema_error(label, f"item {index} criterion must be a string")
        if not isinstance(assertion["verdict"], str):
            raise _schema_error(label, f"item {index} verdict must be a string")
        if not isinstance(assertion["reason"], str) or not assertion["reason"].strip():
            raise _schema_error(label, f"item {index} reason must be a non-empty string")
        if not isinstance(assertion["evidence_refs"], list):
            raise _schema_error(label, f"item {index} evidence_refs must be an array")
        result.append(assertion)
    return result


def _validate_already_decided(
    value: Any,
    label: str,
    *,
    allow_split_assertions: bool,
) -> tuple[list[str], dict[str, str]]:
    assertions = _require_list(value, label)
    notes: list[str] = []
    verdicts: dict[str, str] = {}
    for index, assertion in enumerate(assertions):
        if isinstance(assertion, str):
            if not assertion.strip():
                raise _schema_error(label, f"item {index} must be a non-empty decision note")
            notes.append(assertion)
            continue
        if not allow_split_assertions:
            raise _schema_error(label, f"item {index} must be a decision note string")
        if not isinstance(assertion, Mapping):
            raise _schema_error(label, f"item {index} must be a decision note string or SplitAssertionV1 object")
        _require_exact_keys(assertion, frozenset({"assertion", "verdict"}), f"{label}[{index}]")
        key = assertion["assertion"]
        verdict = assertion["verdict"]
        if key not in SPLIT_ASSERTIONS or verdict not in ("PASS", "FAIL", "N/A"):
            raise _schema_error(label, f"item {index} must be a valid S1-S6 assertion")
        if key in verdicts:
            raise _schema_error(label, f"duplicate assertion: {key}")
        verdicts[key] = verdict
    return notes, verdicts


def _validate_derived_unit(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise _schema_error(label, "must be an object")
    _require_exact_keys(value, DERIVED_UNIT_KEYS, label)
    unit_id = _require_string(value["unit_id"], f"{label}.unit_id")
    outcome = _require_string(value["outcome"], f"{label}.outcome")
    capabilities = _validated_enum_array(value["work_capabilities"], WORK_CAPABILITIES, f"{label}.work_capabilities")
    tags = _validated_enum_array(value["cross_cutting_tags"], CROSS_CUTTING_TAGS, f"{label}.cross_cutting_tags")
    profile = _validated_enum(value["target_executor_profile"], EXECUTOR_PROFILES, f"{label}.target_executor_profile")
    notes, _ = _validate_already_decided(
        value["already_decided"],
        f"{label}.already_decided",
        allow_split_assertions=False,
    )
    allowed = _validate_string_array(value["allowed_executor_decisions"], f"{label}.allowed_executor_decisions")
    forbidden = _validate_string_array(value["forbidden_executor_decisions"], f"{label}.forbidden_executor_decisions")
    _validate_criterion_assertion_shape(value["criterion_assertions"], f"{label}.criterion_assertions")
    _require_list(value["material_findings"], f"{label}.material_findings")
    normalized = dict(value)
    normalized.update(
        {
            "unit_id": unit_id,
            "outcome": outcome,
            "work_capabilities": capabilities,
            "cross_cutting_tags": tags,
            "target_executor_profile": profile,
            "already_decided": notes,
            "allowed_executor_decisions": allowed,
            "forbidden_executor_decisions": forbidden,
        }
    )
    return normalized


def compile_plan(
    tasks_text: str,
    proposal: Mapping[str, Any],
    *,
    source_binding: Mapping[str, Any] | None = None,
    proposal_sha256: str | None = None,
) -> dict[str, Any]:
    """Compile one explicit task graph and proposal into a derived result.

    ``source_binding`` is the adapter's actual binding.  If omitted, the
    proposal binding is used, which keeps the pure core convenient for tests
    while the CLI always supplies the binding computed from exact file bytes.
    """

    graph = parse_task_table(tasks_text)
    proposal_map = _require_mapping(proposal, "proposal")
    _require_exact_keys(proposal_map, PROPOSAL_KEYS, "proposal")
    if proposal_map["schema_version"] != 1:
        raise PlanCompilationInputError("unsupported proposal schema_version")
    findings: list[dict[str, Any]] = []

    source = _require_mapping(proposal_map["source_binding"], "source_binding")
    _require_exact_keys(source, SOURCE_BINDING_KEYS, "source_binding")
    proposal_source = {
        "plan_ref": _require_string(source["plan_ref"], "source_binding.plan_ref"),
        "plan_sha256": _validate_sha(source["plan_sha256"], "source_binding.plan_sha256"),
        "tasks_ref": _require_string(source["tasks_ref"], "source_binding.tasks_ref"),
        "tasks_sha256": _validate_sha(source["tasks_sha256"], "source_binding.tasks_sha256"),
    }
    actual_source = proposal_source if source_binding is None else dict(source_binding)
    if source_binding is not None:
        for field in SOURCE_BINDING_KEYS:
            if field not in actual_source:
                raise PlanCompilationInputError(f"actual source binding is missing {field}")
        actual_source = {
            "plan_ref": _require_string(actual_source["plan_ref"], "actual plan_ref"),
            "plan_sha256": _validate_sha(actual_source["plan_sha256"], "actual plan_sha256"),
            "tasks_ref": _require_string(actual_source["tasks_ref"], "actual tasks_ref"),
            "tasks_sha256": _validate_sha(actual_source["tasks_sha256"], "actual tasks_sha256"),
        }
        if any(actual_source[field] != proposal_source[field] for field in SOURCE_BINDING_KEYS):
            findings.append(
                _finding(
                    "SOURCE_IDENTITY_MISMATCH",
                    message="proposal source binding does not match exact source inputs",
                )
            )

    if not isinstance(proposal_map["units"], list):
        raise PlanCompilationInputError("units must be an array")
    existing_handoff_values = _require_list(proposal_map["existing_dependency_handoffs"], "existing_dependency_handoffs")
    controlled_values = _require_list(proposal_map["controlled_discoveries"], "controlled_discoveries")
    semantic_source = _require_string(proposal_map["semantic_assessment_source"], "semantic_assessment_source")
    semantic_refs = _validate_string_array(proposal_map["semantic_evidence_refs"], "semantic_evidence_refs")

    if proposal_sha256 is None:
        proposal_digest = hashlib.sha256(canonical_json(proposal_map).encode("utf-8")).hexdigest()
    else:
        proposal_digest = _validate_sha(proposal_sha256, "proposal_sha256")

    raw_units: dict[str, Mapping[str, Any]] = {}
    for raw in proposal_map["units"]:
        unit = _require_mapping(raw, "unit proposal")
        _require_exact_keys(unit, UNIT_KEYS, "unit proposal")
        original_id = _require_string(unit["original_unit_id"], "original_unit_id")
        if original_id in raw_units:
            raise PlanCompilationInputError(f"duplicate unit proposal: {original_id}")
        for field in (
            "work_capabilities",
            "cross_cutting_tags",
            "already_decided",
            "allowed_executor_decisions",
            "forbidden_executor_decisions",
            "derived_units",
            "new_internal_edges",
            "internal_handoffs",
            "criterion_assertions",
            "material_findings",
        ):
            if not isinstance(unit[field], list):
                raise PlanCompilationInputError(f"unit {original_id}.{field} must be an array")
        _validated_enum_array(unit["work_capabilities"], WORK_CAPABILITIES, f"unit {original_id}.work_capabilities")
        _validated_enum_array(unit["cross_cutting_tags"], CROSS_CUTTING_TAGS, f"unit {original_id}.cross_cutting_tags")
        _validated_enum(unit["target_executor_profile"], EXECUTOR_PROFILES, f"unit {original_id}.target_executor_profile")
        disposition = _validated_enum(unit["disposition"], DISPOSITIONS, f"unit {original_id}.disposition")
        notes, _ = _validate_already_decided(
            unit["already_decided"],
            f"unit {original_id}.already_decided",
            allow_split_assertions=disposition == "SPLIT_RECOMMENDED",
        )
        _validate_criterion_assertion_shape(unit["criterion_assertions"], f"unit {original_id}.criterion_assertions")
        allowed = set(_validate_string_array(unit["allowed_executor_decisions"], f"unit {original_id}.allowed_executor_decisions"))
        forbidden = set(_validate_string_array(unit["forbidden_executor_decisions"], f"unit {original_id}.forbidden_executor_decisions"))
        normalized_unit = dict(unit)
        normalized_unit["already_decided"] = notes if disposition != "SPLIT_RECOMMENDED" else list(unit["already_decided"])
        raw_units[original_id] = normalized_unit
        if allowed & forbidden:
            findings.append(_finding("EXECUTOR_PROFILE_MISMATCH", unit_ref=original_id, message="executor decision is both allowed and forbidden"))
        if unit["disposition"] in ("KEEP_UNIT", "CAPABILITY_COUPLED") and any(unit[field] for field in ("derived_units", "new_internal_edges", "internal_handoffs")):
            findings.append(_finding("INVALID_SPLIT_STRUCTURE", unit_ref=original_id, message="non-split disposition carries split fields"))

    original_ids = [unit.task_id for unit in graph.units]
    original_id_set = set(original_ids)
    for original_id in raw_units:
        if original_id not in original_id_set:
            findings.append(_finding("UNKNOWN_ORIGINAL_UNIT", unit_ref=original_id, message="proposal names no original task unit"))
    for original_id in original_ids:
        if original_id not in raw_units:
            findings.append(_finding("OMITTED_EXECUTABLE_UNIT", unit_ref=original_id, message="proposal omits an executable task unit"))

    final_ids_by_original: dict[str, list[str]] = {}
    final_raw_by_id: dict[str, Mapping[str, Any]] = {}
    final_order: list[str] = []
    split_edges: list[tuple[str, str]] = []
    internal_handoffs: list[TypedHandoffV1] = []

    for original_id in original_ids:
        unit = raw_units.get(original_id)
        if unit is None:
            continue
        disposition = unit["disposition"]
        if disposition == "SPLIT_RECOMMENDED":
            derived_values = unit["derived_units"]
            derived_ids: list[str] = []
            derived_maps: dict[str, Mapping[str, Any]] = {}
            for index, derived in enumerate(derived_values):
                derived_map = _validate_derived_unit(derived, f"unit {original_id}.derived_units[{index}]")
                derived_id = str(derived_map["unit_id"])
                if derived_id in original_id_set or derived_id in final_raw_by_id or derived_id in derived_ids:
                    findings.append(_finding("INVALID_SPLIT_STRUCTURE", unit_ref=original_id, message="derived unit ID is missing, duplicated, or collides"))
                    continue
                derived_ids.append(derived_id)
                derived_maps[derived_id] = derived_map
            final_ids_by_original[original_id] = derived_ids
            final_order.extend(derived_ids)
            for derived_id in derived_ids:
                final_raw_by_id[derived_id] = derived_maps[derived_id]
                if set(derived_maps[derived_id]["allowed_executor_decisions"]) & set(derived_maps[derived_id]["forbidden_executor_decisions"]):
                    findings.append(
                        _finding(
                            "EXECUTOR_PROFILE_MISMATCH",
                            unit_ref=derived_id,
                            message="executor decision is both allowed and forbidden",
                        )
                    )
            if len(derived_ids) < 2:
                findings.append(_finding("FALSE_CAPABILITY_SPLIT", unit_ref=original_id, message="split must produce at least two derived units"))
            derived_outcomes = [str(derived_maps[derived_id]["outcome"]) for derived_id in derived_ids]
            if len(set(derived_outcomes)) != len(derived_outcomes):
                findings.append(_finding("DUPLICATE_DERIVED_OUTCOME", unit_ref=original_id, message="derived units must have distinct outcomes"))
            capability_signatures = [tuple(sorted(derived_maps[derived_id]["work_capabilities"])) for derived_id in derived_ids]
            if len(set(capability_signatures)) != len(capability_signatures):
                findings.append(_finding("DUPLICATE_DERIVED_CAPABILITY_SIGNATURE", unit_ref=original_id, message="derived units must have distinct capability signatures"))
            profiles = [str(derived_maps[derived_id]["target_executor_profile"]) for derived_id in derived_ids]
            if len(set(profiles)) != len(profiles):
                findings.append(_finding("DUPLICATE_DERIVED_EXECUTOR_PROFILE", unit_ref=original_id, message="derived units must have distinct executor profiles"))
            decision_envelopes = [
                (
                    tuple(sorted(derived_maps[derived_id]["allowed_executor_decisions"])),
                    tuple(sorted(derived_maps[derived_id]["forbidden_executor_decisions"])),
                )
                for derived_id in derived_ids
            ]
            if len(set(decision_envelopes)) != len(decision_envelopes):
                findings.append(_finding("DUPLICATE_DERIVED_DECISION_ENVELOPE", unit_ref=original_id, message="derived units must have distinct decision envelopes"))
            parent_capabilities = set(unit["work_capabilities"])
            derived_capabilities = {
                capability
                for derived_id in derived_ids
                for capability in derived_maps[derived_id]["work_capabilities"]
            }
            if derived_capabilities != parent_capabilities:
                findings.append(
                    _finding(
                        "CAPABILITY_UNION_MISMATCH",
                        unit_ref=original_id,
                        evidence=sorted(parent_capabilities ^ derived_capabilities),
                        message="derived capability union does not equal the parent capability set",
                    )
                )
            parent_tags = set(unit["cross_cutting_tags"])
            derived_tags = {
                tag
                for derived_id in derived_ids
                for tag in derived_maps[derived_id]["cross_cutting_tags"]
            }
            if derived_tags != parent_tags:
                findings.append(
                    _finding(
                        "TAG_UNION_MISMATCH",
                        unit_ref=original_id,
                        evidence=sorted(parent_tags ^ derived_tags),
                        message="derived tag union does not equal the parent tag set",
                    )
                )
            unit_split_edges: list[tuple[str, str]] = []
            for raw_edge in unit["new_internal_edges"]:
                edge = _normalise_edge(raw_edge)
                if edge is None or edge[0] not in derived_ids or edge[1] not in derived_ids or edge[0] == edge[1]:
                    findings.append(_finding("INVALID_SPLIT_STRUCTURE", unit_ref=original_id, message="internal edge is not between derived units"))
                    continue
                if edge in unit_split_edges:
                    findings.append(_finding("INVALID_SPLIT_STRUCTURE", unit_ref=original_id, message="duplicate internal edge"))
                    continue
                unit_split_edges.append(edge)
            split_edges.extend(unit_split_edges)
            if not unit_split_edges:
                findings.append(_finding("FALSE_CAPABILITY_SPLIT", unit_ref=original_id, message="split must add an internal dependency edge"))
            try:
                _ensure_acyclic(derived_ids, unit_split_edges)
            except TaskGraphError:
                findings.append(_finding("INVALID_SPLIT_STRUCTURE", unit_ref=original_id, message="internal split graph contains a cycle"))
            _, verdicts = _validate_already_decided(
                unit["already_decided"],
                f"unit {original_id}.already_decided",
                allow_split_assertions=True,
            )
            if any(verdicts.get(assertion) != "PASS" for assertion in SPLIT_ASSERTIONS):
                findings.append(_finding("INVALID_SPLIT_STRUCTURE", unit_ref=original_id, evidence=SPLIT_ASSERTIONS, message="S1-S6 must all be explicit PASS assertions"))
            local_handoffs: list[TypedHandoffV1] = []
            seen_internal_handoffs: set[tuple[str, str]] = set()
            for raw_handoff in unit["internal_handoffs"]:
                handoff = _validate_handoff(raw_handoff, "internal_handoff")
                if handoff is None or handoff.source_unit not in derived_ids or handoff.target_unit not in derived_ids or handoff.source_unit == handoff.target_unit:
                    findings.append(_finding("INVALID_HANDOFF", unit_ref=original_id, message="invalid internal typed handoff"))
                elif (handoff.source_unit, handoff.target_unit) in seen_internal_handoffs:
                    findings.append(_finding("INVALID_HANDOFF", unit_ref=original_id, message="duplicate internal typed handoff"))
                else:
                    seen_internal_handoffs.add((handoff.source_unit, handoff.target_unit))
                    local_handoffs.append(handoff)
            internal_handoffs.extend(local_handoffs)
            edge_identities = set(unit_split_edges)
            handoff_identities = {(handoff.source_unit, handoff.target_unit) for handoff in local_handoffs}
            for edge in sorted(edge_identities - handoff_identities):
                findings.append(_finding("MISSING_REQUIRED_HANDOFF", unit_ref=original_id, evidence=edge, message="internal edge has no matching typed handoff"))
            for handoff in sorted(handoff_identities - edge_identities):
                findings.append(_finding("HANDOFF_EDGE_MISMATCH", unit_ref=original_id, evidence=handoff, message="typed handoff has no matching internal edge"))
        else:
            final_ids_by_original[original_id] = [original_id]
            final_order.append(original_id)
            final_raw_by_id[original_id] = unit

    final_order_index = {unit_id: index for index, unit_id in enumerate(final_order)}
    final_id_set = set(final_order)

    existing_handoffs: list[TypedHandoffV1] = []
    seen_handoffs: set[tuple[str, str]] = set()
    original_edges = set(graph.edges)
    for raw_handoff in existing_handoff_values:
        handoff = _validate_handoff(raw_handoff, "existing_dependency_handoff")
        if handoff is None:
            findings.append(_finding("INVALID_HANDOFF", message="invalid existing dependency handoff"))
            continue
        identity = (handoff.source_unit, handoff.target_unit)
        if identity in seen_handoffs:
            raise PlanCompilationInputError(f"duplicate existing handoff: {identity}")
        seen_handoffs.add(identity)
        if identity not in original_edges or handoff.source_unit == handoff.target_unit:
            findings.append(_finding("HANDOFF_EDGE_MISMATCH", evidence=identity, message="handoff does not correspond to an original DAG edge"))
        else:
            existing_handoffs.append(handoff)

    valid_discoveries: list[ControlledDiscoveryV1] = []
    seen_discoveries: set[str] = set()
    for raw_discovery in controlled_values:
        if not isinstance(raw_discovery, Mapping) or set(raw_discovery) != DISCOVERY_KEYS:
            findings.append(_finding("INVALID_CONTROLLED_DISCOVERY", message="controlled discovery has invalid exact shape"))
            continue
        values = {key: raw_discovery[key] for key in DISCOVERY_KEYS}
        if any(not isinstance(value, str) or not value.strip() for value in values.values()):
            findings.append(_finding("INVALID_CONTROLLED_DISCOVERY", message="controlled discovery fields must be non-empty strings"))
            continue
        discovery = ControlledDiscoveryV1(
            values["unit_ref"].strip(),
            values["question"].strip(),
            values["scope_bound"].strip(),
            values["stop_condition"].strip(),
            values["output_contract"].strip(),
            values["verification_before_dependent_work"].strip(),
        )
        if discovery.unit_ref not in final_id_set:
            findings.append(_finding("UNKNOWN_CONTROLLED_DISCOVERY_UNIT", unit_ref=discovery.unit_ref, message="discovery must reference a final executable unit"))
            continue
        if discovery.unit_ref in seen_discoveries:
            findings.append(_finding("DUPLICATE_CONTROLLED_DISCOVERY_UNIT", unit_ref=discovery.unit_ref, message="at most one discovery is allowed per final unit"))
            continue
        seen_discoveries.add(discovery.unit_ref)
        valid_discoveries.append(discovery)

    compiled_edges: list[tuple[str, str]] = list(split_edges)
    for source, target in graph.edges:
        sources = final_ids_by_original.get(source, [])
        targets = final_ids_by_original.get(target, [])
        if not sources or not targets:
            continue
        source_internal = [edge for edge in split_edges if edge[0] in sources and edge[1] in sources]
        target_internal = [edge for edge in split_edges if edge[0] in targets and edge[1] in targets]
        source_terminals = [unit_id for unit_id in sources if not any(edge[0] == unit_id for edge in source_internal)] or sources
        target_initials = [unit_id for unit_id in targets if not any(edge[1] == unit_id for edge in target_internal)] or targets
        compiled_edges.extend((compiled_source, compiled_target) for compiled_source in source_terminals for compiled_target in target_initials)

    def _origin_of(unit_id: str) -> str:
        return next((original for original, finals in final_ids_by_original.items() if unit_id in finals), unit_id)

    collapsed_edges = {
        (_origin_of(node), _origin_of(other))
        for node, other in compiled_edges
        if _origin_of(node) != _origin_of(other)
    }
    original_edge_set = set(graph.edges)
    for edge in sorted(collapsed_edges - original_edge_set):
        findings.append(_finding("DEPENDENCY_EDGE_INVENTION", evidence=edge, message="compiled graph introduces an external dependency edge"))
    for edge in sorted(original_edge_set - collapsed_edges):
        findings.append(_finding("DEPENDENCY_EDGE_LOSS", evidence=edge, message="compiled graph loses an original dependency edge"))
    compiled_reachability = _reachable(final_order, compiled_edges)
    collapsed_reachability = {
        (_origin_of(source), _origin_of(target))
        for source, target in compiled_reachability
        if _origin_of(source) != _origin_of(target)
    }
    original_reachability = _reachable(original_ids, graph.edges)
    parallel_loss = collapsed_reachability - original_reachability
    if parallel_loss:
        findings.append(_finding("PARALLELISM_LOSS", evidence=sorted(parallel_loss), message="compiled graph changes original reachability"))

    coverage: list[dict[str, Any]] = []
    all_coverage_ready = True
    compiled_units: list[dict[str, Any]] = []
    for final_id in final_order:
        original_id = next(original for original, finals in final_ids_by_original.items() if final_id in finals)
        parent = raw_units[original_id]
        derived = final_raw_by_id[final_id]
        is_derived = final_id != original_id
        assertions = derived["criterion_assertions"] if is_derived else parent["criterion_assertions"]
        validated_assertions, unit_coverage_ready = _validate_coverage(final_id, assertions, findings)
        all_coverage_ready = all_coverage_ready and unit_coverage_ready
        coverage.append({"unit_ref": final_id, "assertions": validated_assertions})
        task = next(task for task in graph.units if task.task_id == original_id)
        compiled_material_findings = list(parent["material_findings"])
        if is_derived:
            compiled_material_findings.extend(derived["material_findings"])
        compiled_capabilities = derived["work_capabilities"] if is_derived else parent["work_capabilities"]
        compiled_tags = derived["cross_cutting_tags"] if is_derived else parent["cross_cutting_tags"]
        compiled_profile = derived["target_executor_profile"] if is_derived else parent["target_executor_profile"]
        compiled_decisions_allowed = derived["allowed_executor_decisions"] if is_derived else parent["allowed_executor_decisions"]
        compiled_decisions_forbidden = derived["forbidden_executor_decisions"] if is_derived else parent["forbidden_executor_decisions"]
        compiled_already_decided = derived["already_decided"] if is_derived else parent["already_decided"]
        compiled_units.append(
            {
                "unit_ref": final_id,
                "original_unit_id": original_id,
                "outcome": derived["outcome"] if is_derived else task.outcome,
                "slice_type": task.slice_type,
                "status": task.status,
                "disposition": parent["disposition"],
                "work_capabilities": list(compiled_capabilities),
                "cross_cutting_tags": list(compiled_tags),
                "target_executor_profile": compiled_profile,
                "already_decided": list(compiled_already_decided),
                "allowed_executor_decisions": list(compiled_decisions_allowed),
                "forbidden_executor_decisions": list(compiled_decisions_forbidden),
                "criterion_assertions": validated_assertions,
                "material_findings": compiled_material_findings,
            }
        )
        if task.status == "Cancelled":
            findings.append(_finding("UNSUPPORTED_CANCELLED_TASK_STATE", unit_ref=original_id, message="Cancelled tasks cannot be executor-ready"))
        for material in compiled_material_findings:
            if isinstance(material, Mapping):
                code = material.get("finding_code", "UNRESOLVED_MATERIAL_FINDING")
                evidence = material.get("evidence", [])
                message = material.get("message", "proposal supplied a material finding")
            else:
                code = "UNRESOLVED_MATERIAL_FINDING"
                evidence = [str(material)]
                message = "proposal supplied a material finding"
            findings.append(_finding(str(code), unit_ref=final_id, evidence=evidence if isinstance(evidence, list) else (), message=str(message)))

    findings = _deduplicate_findings(findings)
    material_defect = bool(findings) or not all_coverage_ready
    if not controlled_values and not material_defect:
        readiness = "EXECUTOR_READY"
    elif valid_discoveries and not material_defect:
        readiness = "EXECUTOR_READY_WITH_CONTROLLED_DISCOVERY"
    else:
        readiness = "EXECUTOR_NOT_READY"

    compiled_graph = {
        "units": list(final_order),
        "edges": _canonical_edge_list(compiled_edges, final_order_index),
    }
    result = {
        "schema_version": 1,
        "source_binding": {
            "plan_ref": proposal_source["plan_ref"],
            "plan_sha256": proposal_source["plan_sha256"],
            "tasks_ref": proposal_source["tasks_ref"],
            "tasks_sha256": proposal_source["tasks_sha256"],
        },
        "proposal_sha256": proposal_digest,
        "original_graph": graph.to_mapping(),
        "compiled_graph": compiled_graph,
        "compiled_units": compiled_units,
        "existing_edge_handoffs": [handoff.to_mapping() for handoff in existing_handoffs],
        "internal_split_handoffs": [handoff.to_mapping() for handoff in internal_handoffs],
        "controlled_discoveries": [
            discovery.to_mapping()
            for discovery in sorted(valid_discoveries, key=lambda item: final_order_index[item.unit_ref])
        ],
        "coverage": coverage,
        "findings": findings,
        "readiness": readiness,
        "semantic_assertion_provenance": {
            "source": semantic_source,
            "evidence_refs": semantic_refs,
            "cross_cutting_tags": sorted(
                {
                    tag
                    for unit in raw_units.values()
                    for tag in unit["cross_cutting_tags"]
                    if tag in ("ESTIMATION_UNCERTAINTY", "RESEARCH_DISCOVERY")
                }
            ),
        },
    }
    return result


def _deduplicate_findings(findings: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    seen: set[str] = set()
    for finding in findings:
        key = canonical_json(finding)
        if key not in seen:
            seen.add(key)
            result.append(finding)
    return result


def compile_proposal(*args: Any, **kwargs: Any) -> dict[str, Any]:
    """Compatibility spelling for callers that name the operation by proposal."""

    return compile_plan(*args, **kwargs)


def serialize_result(result: Mapping[str, Any]) -> str:
    """Serialize a result using the exact CLI canonical JSON contract."""

    return canonical_json(result) + "\n"
