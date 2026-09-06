"""Deterministic, read-only Operation Guidance over one resume snapshot.

This module deliberately contains a small finite contract.  It does not read
the filesystem, inspect Git, discover skills, or persist a result.  Authority
continues to belong to the resume snapshot and the selected lifecycle route.
"""

from __future__ import annotations

from dataclasses import dataclass
import json
from collections.abc import Mapping
from typing import Any, TypedDict


SCHEMA_VERSION = 1
CANDIDATE_SET_ID = "PL_V39_07_OPERATION_GUIDANCE_V1"
MAX_TEST_CANDIDATES = 8
_AMBIGUITY_TEST_ROUTE_SUFFIX = "#AMBIGUOUS_TEST"

OUTCOMES = (
    "MATCHED",
    "NO_APPLICABLE_OPERATION",
    "AMBIGUOUS_OPERATION",
    "NOT_AUTHORIZED",
    "MISSING_OR_UNUSABLE_CONTEXT",
)
CAPABILITY_STATES = (
    "ALLOWED",
    "FORBIDDEN",
    "REQUIRES_SEPARATE_AUTHORIZATION",
    "NOT_APPLICABLE",
)
CAPABILITY_IDS = (
    "READ",
    "GOVERNANCE_WRITE",
    "PRODUCT_WRITE",
    "GIT_STAGE",
    "GIT_COMMIT",
    "NETWORK_EXTERNAL",
    "DISPOSABLE_CONSUMER",
    "LIVE_CONSUMER",
)


class OperationGuidanceV1(TypedDict):
    """JSON-compatible public result shape (the selector returns this mapping)."""

    schema_version: int
    outcome: str
    reason_code: str
    operation: dict[str, str] | None
    authority: dict[str, Any] | None
    capabilities: list[dict[str, Any]]
    guidance: dict[str, Any] | None
    provenance: dict[str, Any]


# Kept as a compatibility name for the predecessor plan's terminology.
ExecutionGuidanceV1 = OperationGuidanceV1

_READINESS_LIFECYCLES = frozenset(
    {
        "Readiness",
        "Formal Readiness",
        "FORMAL_READINESS",
        "Readiness / In progress",
        "Readiness / Ready",
        "FORMAL_READINESS_IN_PROGRESS",
        "FORMAL_READINESS_READY",
    }
)
_IMPLEMENTATION_LIFECYCLES = frozenset(
    {
        "Implementation",
        "Execution",
        "Implementation / In progress",
        "Execution / In progress",
        "EXECUTION_IN_PROGRESS",
    }
)
_READINESS_STATUSES = frozenset(
    {"In progress", "Ready", "IN_PROGRESS", "READY", "FORMAL_READINESS_IN_PROGRESS", "FORMAL_READINESS_READY"}
)
_IMPLEMENTATION_STATUSES = frozenset(
    {"In progress", "Ready", "IN_PROGRESS", "READY", "EXECUTION_IN_PROGRESS"}
)


@dataclass(frozen=True)
class CapabilitySpec:
    """One fixed capability projection in declaration order."""

    capability_id: str
    state: str
    authority_ref: str | None

    def __post_init__(self) -> None:
        if self.capability_id not in CAPABILITY_IDS:
            raise ValueError(f"Unknown capability identity: {self.capability_id!r}")
        if self.state not in CAPABILITY_STATES:
            raise ValueError(f"Unknown capability state: {self.state!r}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "state": self.state,
            "authority_ref": self.authority_ref,
        }


@dataclass(frozen=True)
class OperationBinding:
    """An immutable exact action-to-route binding."""

    action_id: str
    operation_id: str
    operation_class: str
    route_id: str
    predicate_id: str
    skill_ref: str
    procedure_ref: str
    mode_ref: str
    discipline_refs: tuple[str, ...]
    capabilities: tuple[CapabilitySpec, ...]
    implementation_required: bool
    readiness_route: bool
    policy_refs: tuple[str, ...]
    precondition_refs: tuple[str, ...]
    verification_refs: tuple[str, ...]
    result_contract_refs: tuple[str, ...]
    stop_condition_refs: tuple[str, ...]
    escalation_ref: str
    next_gate_ref: str
    next_gate_owner_ref: str
    task_binding_refs: tuple[str, ...]
    fixed_evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        # Keep the private candidate seam constructible for malformed-value
        # tests; _validate_candidates is the structured fail-closed boundary.
        return None

    def operation_dict(self) -> dict[str, str]:
        return {
            "operation_id": self.operation_id,
            "operation_class": self.operation_class,
            "route_id": self.route_id,
        }


# CandidateBinding is the name used by the plan's finite candidate-set seam.
CandidateBinding = OperationBinding


def _capabilities(*states: str, authority_ref: str) -> tuple[CapabilitySpec, ...]:
    if len(states) != len(CAPABILITY_IDS):
        raise ValueError("A route must declare one state for every pilot capability")
    return tuple(
        CapabilitySpec(capability_id, state, authority_ref)
        for capability_id, state in zip(CAPABILITY_IDS, states, strict=True)
    )


_READINESS_CAPABILITIES = _capabilities(
    "ALLOWED",
    "ALLOWED",
    "FORBIDDEN",
    "FORBIDDEN",
    "FORBIDDEN",
    "REQUIRES_SEPARATE_AUTHORIZATION",
    "FORBIDDEN",
    "FORBIDDEN",
    authority_ref=".planning/control/CHANGE_READINESS.md",
)
_IMPLEMENTATION_CAPABILITIES = _capabilities(
    "ALLOWED",
    "ALLOWED",
    "ALLOWED",
    "REQUIRES_SEPARATE_AUTHORIZATION",
    "REQUIRES_SEPARATE_AUTHORIZATION",
    "REQUIRES_SEPARATE_AUTHORIZATION",
    "REQUIRES_SEPARATE_AUTHORIZATION",
    "REQUIRES_SEPARATE_AUTHORIZATION",
    authority_ref=".planning/control/APPROVAL_GATES.md",
)


def _binding(
    *,
    action_id: str,
    operation_id: str,
    operation_class: str,
    route_id: str,
    predicate_id: str,
    skill_ref: str,
    procedure_ref: str,
    mode_ref: str,
    discipline_refs: tuple[str, ...],
    capabilities: tuple[CapabilitySpec, ...],
    implementation_required: bool,
    readiness_route: bool,
    task_binding_refs: tuple[str, ...],
    fixed_evidence_refs: tuple[str, ...],
) -> OperationBinding:
    return OperationBinding(
        action_id=action_id,
        operation_id=operation_id,
        operation_class=operation_class,
        route_id=route_id,
        predicate_id=predicate_id,
        skill_ref=skill_ref,
        procedure_ref=procedure_ref,
        mode_ref=mode_ref,
        discipline_refs=discipline_refs,
        capabilities=capabilities,
        implementation_required=implementation_required,
        readiness_route=readiness_route,
        policy_refs=(
            ".planning/control/APPROVAL_GATES.md",
            ".planning/control/STATE_OWNERSHIP.md",
        ),
        precondition_refs=(
            ".planning/control/CHANGE_PLANNING.md",
            ".planning/control/APPROVAL_GATES.md",
        ),
        verification_refs=(procedure_ref,),
        result_contract_refs=("OperationGuidanceV1",),
        stop_condition_refs=(
            ".planning/control/CHANGE_AMENDMENT.md",
            procedure_ref,
        ),
        escalation_ref=".planning/control/CHANGE_AMENDMENT.md",
        next_gate_ref=".planning/ACTIVE.md#Active change",
        next_gate_owner_ref="change-owner",
        task_binding_refs=task_binding_refs,
        fixed_evidence_refs=fixed_evidence_refs,
    )


PRODUCTION_BINDINGS: tuple[OperationBinding, ...] = (
    _binding(
        action_id="RUN_FORMAL_READINESS",
        operation_id="FORMAL_READINESS_AUDIT",
        operation_class="FORMAL_READINESS_AUDIT",
        route_id="FORMAL_READINESS_V1",
        predicate_id="FORMAL_READINESS_ROUTE_PREDICATE",
        skill_ref=".planning/skills/planning-audit/SKILL.md",
        procedure_ref=".planning/control/CHANGE_READINESS.md",
        mode_ref=".planning/modes/AUDIT.md",
        discipline_refs=(),
        capabilities=_READINESS_CAPABILITIES,
        implementation_required=False,
        readiness_route=True,
        task_binding_refs=(".planning/changes/templates/readiness.md",),
        fixed_evidence_refs=(".planning/changes/templates/readiness.md",),
    ),
    _binding(
        action_id="EXECUTE_AUTHORIZED_TASK",
        operation_id="EXECUTE_CHANGE_TASK",
        operation_class="EXECUTE_CHANGE_TASK",
        route_id="CHANGE_EXECUTION_V1",
        predicate_id="IMPLEMENTATION_ROUTE_PREDICATE",
        skill_ref=".planning/skills/planning-execute/SKILL.md",
        procedure_ref=".planning/control/CHANGE_EXECUTION.md",
        mode_ref=".planning/modes/EXECUTE.md",
        discipline_refs=(),
        capabilities=_IMPLEMENTATION_CAPABILITIES,
        implementation_required=True,
        readiness_route=False,
        task_binding_refs=(".planning/changes/templates/tasks.md",),
        fixed_evidence_refs=(),
    ),
    _binding(
        action_id="EXECUTE_AUTHORIZED_CONTRACT_TASK",
        operation_id="EXECUTE_CONTRACT_CLOSURE_TASK",
        operation_class="EXECUTE_CONTRACT_CLOSURE_TASK",
        route_id="CHANGE_EXECUTION_V1",
        predicate_id="CONTRACT_IMPLEMENTATION_ROUTE_PREDICATE",
        skill_ref=".planning/skills/planning-execute/SKILL.md",
        procedure_ref=".planning/control/CHANGE_EXECUTION.md",
        mode_ref=".planning/modes/EXECUTE.md",
        discipline_refs=(".planning/disciplines/CONTRACT_CLOSURE.md",),
        capabilities=_IMPLEMENTATION_CAPABILITIES,
        implementation_required=True,
        readiness_route=False,
        task_binding_refs=(".planning/changes/templates/tasks.md",),
        fixed_evidence_refs=(),
    ),
)


def _empty_provenance(
    *, outcome: str, reason_code: str, context: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    context = context or {}
    status = context.get("status") if isinstance(context, Mapping) else None
    schema_version = context.get("schema_version") if isinstance(context, Mapping) else None
    source_revision: Any = None
    if isinstance(context, Mapping):
        bootstrap = context.get("bootstrap")
        git_identity = context.get("git_identity")
        if isinstance(bootstrap, Mapping):
            source_revision = bootstrap.get("source_revision")
        if source_revision is None and isinstance(git_identity, Mapping):
            source_revision = git_identity.get("head")
    return {
        "candidate_set_id": CANDIDATE_SET_ID,
        "resume_schema_version": schema_version,
        "resume_status": status,
        "source_revision": source_revision,
        "authority_refs": [],
        "selection_reason": f"{outcome}:{reason_code}",
    }


def _source_refs(context: Mapping[str, Any]) -> list[dict[str, str]]:
    sources = context.get("selected_sources", [])
    if not isinstance(sources, list):
        raise ValueError("selected_sources must be a list")
    refs: list[dict[str, str]] = []
    for source in sources:
        if not isinstance(source, Mapping):
            raise ValueError("selected_sources entries must be objects")
        path = source.get("path")
        digest = source.get("sha256")
        if not isinstance(path, str) or not path or not isinstance(digest, str) or not digest:
            raise ValueError("selected_sources entries require path and sha256")
        refs.append({"path": path, "sha256": digest})
    return refs


def _provenance(context: Mapping[str, Any], *, reason: str) -> dict[str, Any]:
    bootstrap = context["bootstrap"]
    git_identity = context.get("git_identity", {})
    source_revision = bootstrap.get("source_revision")
    if source_revision is None and isinstance(git_identity, Mapping):
        source_revision = git_identity.get("head")
    return {
        "candidate_set_id": CANDIDATE_SET_ID,
        "resume_schema_version": context["schema_version"],
        "resume_status": context["status"],
        "source_revision": source_revision,
        "authority_refs": _source_refs(context),
        "selection_reason": reason,
    }


def _result(
    *,
    context: Mapping[str, Any] | None,
    outcome: str,
    reason_code: str,
    binding: OperationBinding | None = None,
    authorized: bool | None = None,
    capabilities: list[dict[str, Any]] | None = None,
    guidance: dict[str, Any] | None = None,
    reason: str | None = None,
) -> dict[str, Any]:
    operation = binding.operation_dict() if binding else None
    authority = None
    if binding is not None and authorized is not None:
        refs = _source_refs(context) if context is not None else []
        authority = {
            "predicate_id": binding.predicate_id,
            "predicate_result": (
                "AUTHORIZED_FOR_THIS_OPERATION" if authorized else "NOT_AUTHORIZED"
            ),
            "authority_refs": refs,
        }
    if context is not None:
        try:
            provenance = _provenance(context, reason=reason or f"{outcome}:{reason_code}")
        except (KeyError, TypeError, ValueError):
            provenance = _empty_provenance(
                outcome=outcome, reason_code=reason_code, context=context
            )
    else:
        provenance = _empty_provenance(outcome=outcome, reason_code=reason_code)
    return {
        "schema_version": SCHEMA_VERSION,
        "outcome": outcome,
        "reason_code": reason_code,
        "operation": operation,
        "authority": authority,
        "capabilities": capabilities or [],
        "guidance": guidance,
        "provenance": provenance,
    }


def _validate_context(context: object) -> tuple[Mapping[str, Any] | None, str | None]:
    if not isinstance(context, Mapping):
        return None, "INVALID_RESUME_CONTEXT"
    if context.get("schema_version") != SCHEMA_VERSION:
        return context, "INVALID_RESUME_CONTEXT"
    if context.get("status") != "CURRENT":
        return context, "RESUME_NOT_CURRENT"
    bootstrap = context.get("bootstrap")
    if not isinstance(bootstrap, Mapping):
        return context, "INVALID_RESUME_CONTEXT"
    if not isinstance(bootstrap.get("active_change"), str) or not bootstrap.get("active_change"):
        return context, "MISSING_ACTIVE_CHANGE"
    if not isinstance(bootstrap.get("active_context_path"), str) or not bootstrap.get(
        "active_context_path"
    ):
        return context, "MISSING_ACTIVE_CONTEXT"
    required_strings = ("lifecycle_stage", "stage_status", "next_permitted_action")
    if any(not isinstance(bootstrap.get(key), str) or not bootstrap.get(key) for key in required_strings):
        return context, "INVALID_RESUME_CONTEXT"
    if not isinstance(bootstrap.get("implementation_authorized"), bool):
        return context, "INVALID_RESUME_CONTEXT"
    try:
        _source_refs(context)
    except (TypeError, ValueError):
        return context, "INVALID_RESUME_CONTEXT"
    return context, None


def _validate_candidates(candidates: object) -> bool:
    if type(candidates) is not tuple or len(candidates) > MAX_TEST_CANDIDATES:
        return False
    if any(type(item) is not OperationBinding for item in candidates):
        return False
    if any(not _binding_shape_is_valid(item) for item in candidates):
        return False
    # Keep same-action entries intact so the selector can report an
    # ambiguity. Only an exact repeated binding is malformed; collapsing by
    # action ID before lookup would hide the required discriminator. Equality
    # comparison avoids hashing malformed test-only candidates.
    return all(item not in candidates[:index] for index, item in enumerate(candidates))


def _string_tuple_is_valid(value: object) -> bool:
    return type(value) is tuple and all(
        type(item) is str and bool(item) for item in value
    )


def _binding_shape_is_valid(binding: OperationBinding) -> bool:
    """Validate the finite pilot binding shape without reading referenced files."""

    string_fields = (
        "action_id",
        "operation_id",
        "operation_class",
        "route_id",
        "predicate_id",
        "procedure_ref",
        "mode_ref",
        "skill_ref",
        "escalation_ref",
        "next_gate_ref",
        "next_gate_owner_ref",
    )
    if any(type(getattr(binding, field)) is not str or not getattr(binding, field) for field in string_fields):
        return False
    if type(binding.implementation_required) is not bool or type(binding.readiness_route) is not bool:
        return False
    expected = next(
        (item for item in PRODUCTION_BINDINGS if item.action_id == binding.action_id),
        None,
    )
    if expected is None:
        return False
    allowed_route_ids = {
        expected.route_id,
        f"{expected.route_id}{_AMBIGUITY_TEST_ROUTE_SUFFIX}",
    }
    if binding.route_id not in allowed_route_ids:
        return False
    for field in (
        "operation_id",
        "operation_class",
        "predicate_id",
        "skill_ref",
        "procedure_ref",
        "mode_ref",
        "escalation_ref",
        "next_gate_ref",
        "next_gate_owner_ref",
    ):
        if getattr(binding, field) != getattr(expected, field):
            return False
    for field in (
        "discipline_refs",
        "policy_refs",
        "precondition_refs",
        "verification_refs",
        "result_contract_refs",
        "stop_condition_refs",
        "task_binding_refs",
        "fixed_evidence_refs",
    ):
        if getattr(binding, field) != getattr(expected, field):
            return False
        if not _string_tuple_is_valid(getattr(binding, field)):
            return False
    return (
        binding.implementation_required == expected.implementation_required
        and binding.readiness_route == expected.readiness_route
    )


def _implementation_capability_projection(binding: OperationBinding) -> list[dict[str, Any]]:
    if not isinstance(binding.capabilities, tuple):
        raise ValueError("capabilities must be an immutable tuple")
    if any(not isinstance(item, CapabilitySpec) for item in binding.capabilities):
        raise ValueError("capability entries are invalid")
    if any(not isinstance(item.authority_ref, str) or not item.authority_ref for item in binding.capabilities):
        raise ValueError("capability authority references are invalid")
    if tuple(item.capability_id for item in binding.capabilities) != CAPABILITY_IDS:
        raise ValueError("capability identity/order is invalid")
    if len({item.capability_id for item in binding.capabilities}) != len(binding.capabilities):
        raise ValueError("capability identities must be unique")
    expected = _READINESS_CAPABILITIES if binding.readiness_route else _IMPLEMENTATION_CAPABILITIES
    if binding.capabilities != expected:
        raise ValueError("route capability matrix is invalid")
    return [item.to_dict() for item in binding.capabilities]


def _guidance(
    binding: OperationBinding,
    *,
    active_context_path: str,
) -> dict[str, Any]:
    evidence_refs = list(binding.fixed_evidence_refs)
    if not binding.readiness_route:
        context_path = active_context_path.replace("\\", "/")
        if "/" in context_path:
            sibling = f"{context_path.rsplit('/', 1)[0]}/progress.md"
            evidence_refs.append(sibling)
    scope_refs = [active_context_path]
    return {
        "procedure_ref": binding.procedure_ref,
        "mode_ref": binding.mode_ref,
        "skill_ref": binding.skill_ref,
        "policy_refs": list(binding.policy_refs),
        "discipline_refs": list(binding.discipline_refs),
        "task_binding_refs": list(binding.task_binding_refs),
        "precondition_refs": list(binding.precondition_refs),
        "scope_refs": scope_refs,
        "verification_refs": list(binding.verification_refs),
        "result_contract_refs": list(binding.result_contract_refs),
        "evidence_refs": evidence_refs,
        "stop_condition_refs": list(binding.stop_condition_refs),
        "escalation_ref": binding.escalation_ref,
        "next_gate_ref": binding.next_gate_ref,
        "next_gate_owner_ref": binding.next_gate_owner_ref,
    }


def _select_operation_guidance(
    resume_context: object,
    *,
    candidates: tuple[OperationBinding, ...] = PRODUCTION_BINDINGS,
) -> dict[str, Any]:
    context, context_reason = _validate_context(resume_context)
    if context_reason is not None:
        return _result(
            context=context,
            outcome="MISSING_OR_UNUSABLE_CONTEXT",
            reason_code=context_reason,
        )
    assert context is not None
    if not _validate_candidates(candidates):
        return _result(
            context=context,
            outcome="MISSING_OR_UNUSABLE_CONTEXT",
            reason_code="INVALID_CANDIDATE_SET",
        )
    bootstrap = context["bootstrap"]
    action = bootstrap["next_permitted_action"]
    matches = tuple(item for item in candidates if item.action_id == action)
    if not matches:
        return _result(
            context=context,
            outcome="NO_APPLICABLE_OPERATION",
            reason_code="UNMAPPED_OPERATION",
            reason=f"UNMAPPED_OPERATION:{action}",
        )
    if len(matches) > 1:
        return _result(
            context=context,
            outcome="AMBIGUOUS_OPERATION",
            reason_code="MULTIPLE_EXACT_BINDINGS",
        )

    binding = matches[0]
    lifecycle = bootstrap["lifecycle_stage"]
    stage_status = bootstrap["stage_status"]
    implementation_authorized = bootstrap["implementation_authorized"]
    blocker = bootstrap.get("open_blocker")
    if binding.readiness_route:
        if lifecycle not in _READINESS_LIFECYCLES or stage_status not in _READINESS_STATUSES:
            return _result(
                context=context,
                outcome="NOT_AUTHORIZED",
                reason_code="ROUTE_PREREQUISITE_NOT_MET",
                binding=binding,
                authorized=False,
            )
        # Readiness is the audit that can inspect an open blocker.  It does not
        # borrow implementation authorization and therefore intentionally
        # remains legal with implementation_authorized=False.
    else:
        if lifecycle not in _IMPLEMENTATION_LIFECYCLES or stage_status not in _IMPLEMENTATION_STATUSES:
            return _result(
                context=context,
                outcome="NOT_AUTHORIZED",
                reason_code="ROUTE_PREREQUISITE_NOT_MET",
                binding=binding,
                authorized=False,
            )
        if blocker not in (None, "", "None", "none"):
            return _result(
                context=context,
                outcome="NOT_AUTHORIZED",
                reason_code="OPEN_BLOCKER",
                binding=binding,
                authorized=False,
            )
        if implementation_authorized is not True:
            return _result(
                context=context,
                outcome="NOT_AUTHORIZED",
                reason_code="IMPLEMENTATION_NOT_AUTHORIZED",
                binding=binding,
                authorized=False,
            )

    try:
        capabilities = _implementation_capability_projection(binding)
        if len(capabilities) != len(CAPABILITY_IDS):
            raise ValueError
    except (TypeError, ValueError):
        return _result(
            context=context,
            outcome="MISSING_OR_UNUSABLE_CONTEXT",
            reason_code="INVALID_CAPABILITY_CONTRACT",
            binding=binding,
            authorized=False,
        )
    active_context_path = bootstrap["active_context_path"]
    return _result(
        context=context,
        outcome="MATCHED",
        reason_code="EXACT_OPERATION_BINDING",
        binding=binding,
        authorized=True,
        capabilities=capabilities,
        guidance=_guidance(binding, active_context_path=active_context_path),
        reason=f"EXACT_OPERATION_BINDING:{binding.action_id}",
    )


def select_operation_guidance(resume_context: Mapping[str, Any]) -> dict[str, Any]:
    """Select one exact route from a single already-built resume snapshot."""

    return _select_operation_guidance(resume_context)


def operation_guidance(resume_context: Mapping[str, Any]) -> dict[str, Any]:
    """Compatibility alias for the public pure selector."""

    return select_operation_guidance(resume_context)


build_operation_guidance = select_operation_guidance
select_execution_guidance = select_operation_guidance
PRODUCTION_CANDIDATES = PRODUCTION_BINDINGS


def serialize_guidance(result: Mapping[str, Any]) -> str:
    """Serialize a result deterministically for JSON CLI output/tests."""

    return json.dumps(result, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


__all__ = [
    "CAPABILITY_IDS",
    "CAPABILITY_STATES",
    "CANDIDATE_SET_ID",
    "CandidateBinding",
    "CapabilitySpec",
    "ExecutionGuidanceV1",
    "MAX_TEST_CANDIDATES",
    "OperationBinding",
    "OperationGuidanceV1",
    "OUTCOMES",
    "PRODUCTION_BINDINGS",
    "PRODUCTION_CANDIDATES",
    "SCHEMA_VERSION",
    "_select_operation_guidance",
    "operation_guidance",
    "build_operation_guidance",
    "select_execution_guidance",
    "select_operation_guidance",
    "serialize_guidance",
]
