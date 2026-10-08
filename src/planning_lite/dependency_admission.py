"""Resolve Planning Lite dependency governance without granting runtime authority.

Bootstrap defaults and project policy are read from the product's managed
``.planning`` files. The validated effective ``planning_root`` then owns
``ACTIVE.md`` and the active Change's proposal, approved Plan, task table, and
amendments ledger. Governance is never merged with or recovered from another
root. The resolver derives one fixed T-01 -> T-02 edge projection and, for a task with no
incoming edge, a separate task-local independent projection.  Each digest is
SHA-256 over the exact canonical JSON mapping described by the Change
Definition; it identifies semantics and provenance, never approval or an
execution right.

Returned governance refs are product-root-relative POSIX paths. D8 decision
items are deliberately outside this resolver and remain product-root scoped
under ``.planning/decisions``.

Amendment rows carry stable IDs and complete values at exact projection keys.
Rows are checked in governance order for continuous before/after values and
against the current parsed Plan/task state.  Applicable effects remain in the
projection preimage, including material reversions; effects outside a
requested task's projection are omitted only after their full values prove
that relation.  Missing, malformed, discontinuous, or unreconciled history
fails closed. This module owns the pure dependency resolver, the narrowly
scoped CancellationTombstoneV1 codec/carrier used by the Attempt Runtime, and
the T-04 inert dependency-proof snapshot/codec, immutable exact-byte
EvidenceContentCarrierV1 with deterministic target-local resolution, plus the
private artifact-identity carrier. Workspace remains the only artifact-route
derivation owner; the evidence-content route is derived here from the
effective planning root and opaque evidence ref. Neither route grants
lifecycle authority. This module owns immutable target-local proof and
cancellation carriers, and validates/builds a complete admission mapping but
never stores or attaches one. Attempt Runtime alone owns CURRENT/invalidation,
admission attachment, and lifecycle transitions. The cancellation carrier is
called only while Runtime holds its effective-policy V2 mutation lock;
carrier directories are lookup metadata, not authorities or backends.
"""

from __future__ import annotations

import base64
import binascii
from dataclasses import dataclass
import hashlib
import json
import math
import os
from pathlib import Path
import re
import stat
import tempfile
from typing import Any, Mapping

from . import attempt_evaluation as _pl08
from .plan_compilation import OriginalTaskUnitV1, canonical_json, parse_task_table
from .workspace import WorkspaceError, load_effective_policy


class DependencyAdmissionError(ValueError):
    """A current governance artifact cannot support an unambiguous requirement."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class DependencyResolution:
    """Derived, non-authorizing view of the current approved dependency state.

    ``projection`` and ``dependency_semantic_digest`` are task-local: the
    dependent mapping for T-02, otherwise an independent mapping for a task
    whose parsed incoming-edge set is empty. ``dependent_projection`` and
    ``dependent_dependency_semantic_digest`` always describe the Plan's fixed
    T-01 -> T-02 approval edge, which is the digest stored in Plan metadata and
    the reconciliation receipt. The distinction prevents an independent
    task's NOT_APPLICABLE identity from replacing Plan-level edge approval.
    """

    change_id: str
    task_id: str
    dependency_classification: str
    plan_ref: str
    tasks_ref: str
    amendments_ref: str
    plan_semantics_sha256: str
    task_semantics_sha256: str
    amendments_semantics_sha256: str
    approved_plan_digest: str
    dependent_projection: dict[str, Any]
    dependent_dependency_semantic_digest: str
    projection: dict[str, Any]
    dependency_semantic_digest: str
    requirement: dict[str, Any]
    reconciliation_receipt: dict[str, Any]
    history_complete: bool
    task_status: str


@dataclass(frozen=True)
class CancellationTombstoneV1:
    """Exact durable observation that either member of the fixed edge cancelled.

    The record is edge-scoped so T-01 and T-02 cancellation converge on one
    identity. It excludes mutable governance status from the stable semantic
    digest; Runtime couples this terminal tombstone with live status checks.
    """

    change_id: str
    source_task_id: str = "T-01"
    target_task_id: str = "T-02"
    observed_status: str = "Cancelled"

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "change_id": self.change_id,
            "source_task_id": self.source_task_id,
            "target_task_id": self.target_task_id,
            "observed_status": self.observed_status,
        }


class CancellationCarrierError(ValueError):
    """A cancellation record is malformed, conflicting, or not durable."""


_CONTRACT_KEYS = {
    "schema_version",
    "source_task_id",
    "target_task_id",
    "accepted_output_contract_ref",
    "produced_artifact_logical_ref",
    "required_input_logical_ref",
    "acceptance_contract_ref",
    "evaluation_scope_ref",
    "required_verifier_contract_refs",
}
_REQUIREMENT_KEYS = {
    "schema_version",
    "requirement_id",
    "change_id",
    "plan_ref",
    "tasks_ref",
    "dependency_semantic_digest",
    "dependency_classification",
    "source_task_or_operation_id",
    "source_attempt_id",
    "successor_task_or_operation_id",
    "successor_attempt_id",
    "accepted_output_contract_ref",
    "produced_artifact_logical_ref",
    "required_successor_input_logical_ref",
    "acceptance_contract_ref",
    "evaluation_scope_ref",
    "required_verifier_contract_refs",
}
_RECEIPT_KEYS = {
    "schema_version",
    "change_id",
    "status",
    "approved_plan_digest",
    "dependency_semantic_digest",
    "amendments_semantics_sha256",
    "applicable_dependency_material_amendment_ids",
}
_TASK_KEYS = ("id", "outcome", "slice_type", "blocking_edges", "verification", "blast_radius")
_AMENDMENT_COLUMNS = (
    "Date",
    "Amendment ID",
    "Type",
    "Trigger and evidence",
    "Old approach",
    "New approach",
    "Approval",
    "Readiness impact",
    "Changed dependency fields",
    "Before values",
    "After values",
)
_MUTABLE_FIELDS = {
    "accepted_output_contract_ref",
    "produced_artifact_logical_ref",
    "required_input_logical_ref",
    "acceptance_contract_ref",
    "evaluation_scope_ref",
    "required_verifier_contract_refs",
    "source_task_semantics",
    "target_task_semantics",
    "task_semantics",
    "incoming_dependency_edges",
}
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_CHANGE_ID_RE = re.compile(r"^CHG-[A-Z0-9][A-Z0-9-]*$")
_TASK_ID_RE = re.compile(r"^T-[0-9]{2,}$")


def _fail(code: str, message: str) -> DependencyAdmissionError:
    return DependencyAdmissionError(code, message)


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_json(value: Any) -> str:
    """Hash canonical UTF-8 JSON without LF for governed semantic identities."""
    try:
        encoded = canonical_json(value).encode("utf-8", errors="strict")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise _fail("CANONICAL_JSON_INVALID", "semantic value is not finite strict UTF-8 JSON") from exc
    return _sha256(encoded)


def _canonical_lf(data: bytes, ref: str) -> bytes:
    if data.startswith(b"\xef\xbb\xbf"):
        raise _fail("UTF8_BOM_FORBIDDEN", f"{ref} must be UTF-8 without a BOM")
    try:
        text = data.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise _fail("INVALID_UTF8", f"{ref} is not strict UTF-8") from exc
    normalized = text.replace("\r\n", "\n")
    if "\r" in normalized:
        raise _fail("NON_CANONICAL_LINE_ENDING", f"{ref} contains a bare carriage return")
    return normalized.encode("utf-8", errors="strict")


def _read_text(root: Path, relative: str) -> tuple[str, bytes]:
    path = root / Path(*relative.split("/"))
    try:
        data = path.read_bytes()
    except OSError as exc:
        raise _fail("GOVERNANCE_FILE_MISSING", f"cannot read {relative}") from exc
    canonical = _canonical_lf(data, relative)
    return canonical.decode("utf-8"), canonical


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number: {value}")


def _parse_finite_float(value: str) -> float:
    parsed = float(value)
    if not math.isfinite(parsed):
        raise ValueError(f"non-finite JSON number: {value}")
    return parsed


def _parse_json(text: str, where: str) -> Any:
    try:
        return json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
            parse_float=_parse_finite_float,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        raise _fail("MALFORMED_CANONICAL_JSON", f"{where}: {exc}") from exc


def _one_field(text: str, name: str, *, required: bool = True) -> str | None:
    matches = re.findall(rf"^-[ \t]+{re.escape(name)}:[ \t]*(.*?)[ \t]*$", text, re.MULTILINE)
    if len(matches) > 1 or (required and len(matches) != 1):
        raise _fail("AMBIGUOUS_APPROVAL_METADATA", f"expected one {name} field")
    if not matches:
        return None
    value = matches[0]
    if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
        value = value[1:-1]
    return value.strip()


def _required_nonempty(text: str, name: str) -> str:
    value = _one_field(text, name)
    assert value is not None
    if not value or value in {"None", "TBD", "TODO"}:
        raise _fail("APPROVAL_METADATA_INCOMPLETE", f"{name} must be explicit")
    return value


def _section(text: str, heading: str) -> tuple[int, int, str]:
    lines = text.splitlines(keepends=True)
    starts: list[int] = []
    offset = 0
    for line in lines:
        if line.rstrip("\n") == heading:
            starts.append(offset)
        offset += len(line)
    if len(starts) != 1:
        raise _fail("AMBIGUOUS_GOVERNANCE_SECTION", f"expected exactly one {heading}")
    start = starts[0]
    body_start = start + len(heading) + (1 if text[start + len(heading):].startswith("\n") else 0)
    next_heading = re.search(r"^##\s+", text[body_start:], re.MULTILINE)
    end = body_start + next_heading.start() if next_heading else len(text)
    return start, end, text[body_start:end]


def _fenced_json_blocks(section: str, where: str) -> list[Any]:
    matches = re.findall(r"(?ms)^```json\n(.*?)\n```(?=\n|$)", section)
    blocks: list[Any] = []
    for payload in matches:
        value = _parse_json(payload, where)
        if canonical_json(value) != payload:
            raise _fail("NONCANONICAL_GOVERNED_JSON", f"{where} must use sorted compact canonical JSON")
        blocks.append(value)
    return blocks


def _effective_planning_root(root: str | Path) -> tuple[Path, str, Path]:
    """Resolve the validated policy root while keeping refs product-relative.

    Policy discovery remains product-root ``.planning``. Only the resulting
    validated ``project_policy.planning_root`` selects canonical lifecycle and
    Change governance; this seam does not search, merge, or fall back to a
    second governance tree. D8 decision items retain their separate
    product-root ``.planning/decisions`` authority.
    """
    product_root = Path(root).expanduser().resolve()
    try:
        policy = load_effective_policy(product_root)["project_policy"]
        planning_root_ref = policy["planning_root"]
        if not isinstance(planning_root_ref, str) or not planning_root_ref:
            raise WorkspaceError("effective planning_root is invalid")
        planning_root = (product_root / Path(*planning_root_ref.split("/"))).resolve()
        if not planning_root.is_relative_to(product_root):
            raise WorkspaceError("effective planning_root escapes the product root")
    except (WorkspaceError, KeyError, TypeError, OSError) as exc:
        raise _fail("EFFECTIVE_PLANNING_ROOT_INVALID", f"cannot resolve validated planning_root: {exc}") from exc
    return product_root, planning_root_ref, planning_root


def _active_change(product_root: Path, planning_root_ref: str) -> str:
    """Read the sole ACTIVE pointer below the validated effective root."""
    active_ref = f"{planning_root_ref}/ACTIVE.md" if planning_root_ref != "." else "ACTIVE.md"
    active, _ = _read_text(product_root, active_ref)
    _, _, active_section = _section(active, "## Active change")
    value = _one_field(active_section, "Change")
    assert value is not None
    if not _CHANGE_ID_RE.fullmatch(value):
        raise _fail("ACTIVE_CHANGE_INVALID", "ACTIVE.md must name one exact Change ID")
    return value


def _change_refs(change_id: str, planning_root_ref: str) -> tuple[str, str, str, str]:
    if not _CHANGE_ID_RE.fullmatch(change_id):
        raise _fail("ACTIVE_CHANGE_INVALID", "Change ID has an unsupported form")
    prefix = "" if planning_root_ref == "." else planning_root_ref
    folder = "/".join(part for part in (prefix, "changes/active", change_id) if part)
    return (
        folder,
        f"{folder}/plan.md",
        f"{folder}/tasks.md",
        f"{folder}/amendments.md",
    )


def _validate_change_identity(root: Path, folder: str, change_id: str) -> None:
    proposal, _ = _read_text(root, f"{folder}/proposal.md")
    headings = re.findall(r"^#\s+(CHG-[A-Z0-9][A-Z0-9-]*):\s+.+$", proposal, re.MULTILINE)
    if headings != [change_id]:
        raise _fail("ACTIVE_CHANGE_IDENTITY_MISMATCH", "active folder, pointer, and proposal ID must agree")


def _parse_contract(plan: str) -> dict[str, Any]:
    """Read the one duplicate-safe exact V2 contract from the approved Plan.

    The contract is source governance under ``## Dependency contracts``; it
    is never taken from compiled output or caller input. Unsupported members,
    verifier ordering, versions, or values fail before any projection exists.
    Non-empty refs retain their exact identity here; this T-01 resolver does
    not claim that a referenced policy or resource has been operationally
    resolved, which remains with the later owner of that route/evaluation.
    """
    _, _, section = _section(plan, "## Dependency contracts")
    blocks = _fenced_json_blocks(section, "PlanDependencyContractV2")
    if len(blocks) != 1 or not isinstance(blocks[0], dict):
        raise _fail("DEPENDENCY_CONTRACT_AMBIGUOUS", "exactly one JSON object is required")
    contract = blocks[0]
    if set(contract) != _CONTRACT_KEYS:
        raise _fail("DEPENDENCY_CONTRACT_KEYS_INVALID", "PlanDependencyContractV2 has missing or extra keys")
    if type(contract["schema_version"]) is not int or contract["schema_version"] != 2:
        raise _fail("DEPENDENCY_CONTRACT_VERSION_INVALID", "schema_version must be integer 2")
    if contract["source_task_id"] != "T-01" or contract["target_task_id"] != "T-02":
        raise _fail("DEPENDENCY_CONTRACT_EDGE_INVALID", "the approved contract must select T-01 -> T-02")
    for name in (
        "accepted_output_contract_ref",
        "produced_artifact_logical_ref",
        "required_input_logical_ref",
        "acceptance_contract_ref",
        "evaluation_scope_ref",
    ):
        value = contract[name]
        if not isinstance(value, str) or not value or value != value.strip():
            raise _fail("DEPENDENCY_CONTRACT_VALUE_INVALID", f"{name} must be a non-empty trimmed string")
    refs = contract["required_verifier_contract_refs"]
    if not isinstance(refs, list) or not refs:
        raise _fail("DEPENDENCY_CONTRACT_VERIFIERS_INVALID", "at least one verifier pair is required")
    identities: list[tuple[str, str]] = []
    for pair in refs:
        if not isinstance(pair, dict) or set(pair) != {"contract_id", "contract_version_or_ref"}:
            raise _fail("DEPENDENCY_CONTRACT_VERIFIERS_INVALID", "each verifier must be an exact identity pair")
        identity = (pair["contract_id"], pair["contract_version_or_ref"])
        if any(not isinstance(part, str) or not part or part != part.strip() for part in identity):
            raise _fail("DEPENDENCY_CONTRACT_VERIFIERS_INVALID", "verifier identity values must be trimmed strings")
        identities.append(identity)
    if identities != sorted(set(identities)):
        raise _fail("DEPENDENCY_CONTRACT_VERIFIERS_INVALID", "verifier pairs must be unique and lexically sorted")
    return contract


def _task_map(unit: OriginalTaskUnitV1) -> dict[str, Any]:
    return {
        "id": unit.task_id,
        "outcome": unit.outcome,
        "slice_type": unit.slice_type,
        "blocking_edges": list(unit.blocking_edges),
        "verification": unit.verification,
        "blast_radius": unit.blast_radius,
    }


def _parse_task_governance(tasks_text: str) -> tuple[dict[str, OriginalTaskUnitV1], tuple[tuple[str, str], ...], str]:
    """Parse existing task governance and enforce this resolver's fixed topology.

    The existing task-table parser owns row grammar and status validation. This
    boundary adds the supported T-01 -> T-02 edge restriction and hashes the
    ordered six-field task semantics, excluding mutable status. Parser failures
    become TASK_GOVERNANCE_INVALID; missing or extra edges fail closed as
    UNSUPPORTED_TASK_TOPOLOGY.
    """
    try:
        parsed = parse_task_table(tasks_text)
    except ValueError as exc:
        raise _fail("TASK_GOVERNANCE_INVALID", str(exc)) from exc
    units = {unit.task_id: unit for unit in parsed.units}
    required = {"T-01", "T-02"}
    if not required <= units.keys() or ("T-01", "T-02") not in parsed.edges:
        raise _fail("UNSUPPORTED_TASK_TOPOLOGY", "task table must contain the fixed T-01 -> T-02 edge")
    if any(edge != ("T-01", "T-02") for edge in parsed.edges):
        raise _fail("UNSUPPORTED_TASK_TOPOLOGY", "only the fixed T-01 -> T-02 edge is supported")
    semantics = [_task_map(unit) for unit in parsed.units]
    return units, parsed.edges, _sha256_json(semantics)


def _field_mapping(path: str, contract: Mapping[str, Any], tasks: Mapping[str, OriginalTaskUnitV1]) -> Any:
    if path in {
        "accepted_output_contract_ref",
        "produced_artifact_logical_ref",
        "required_input_logical_ref",
        "acceptance_contract_ref",
        "evaluation_scope_ref",
        "required_verifier_contract_refs",
    }:
        return contract[path]
    if path == "source_task_semantics":
        return _task_map(tasks["T-01"])
    if path == "target_task_semantics":
        return _task_map(tasks["T-02"])
    if path == "task_semantics":
        raise _fail("EFFECT_SCOPE_UNRESOLVED", "task_semantics requires a task-scoped amendment value")
    if path == "incoming_dependency_edges":
        raise _fail("EFFECT_SCOPE_UNRESOLVED", "incoming_dependency_edges requires a task-scoped amendment value")
    raise _fail("AMENDMENT_EFFECT_FIELD_INVALID", f"unsupported dependency projection field: {path}")


def _validate_effect_value(path: str, value: Any) -> str | None:
    """Validate one complete amendment value and return its task projection scope.

    Task effects carry the exact six governed fields and retain task identity;
    incoming-edge effects carry sorted exact edge identities for one target;
    contract effects use their complete typed values. Returning the task ID lets
    the amendment parser reject effects that change projection scope. Malformed
    values, mixed task scopes, and unsupported fields fail closed.
    """
    if path in {"source_task_semantics", "target_task_semantics", "task_semantics"}:
        if not isinstance(value, dict) or set(value) != set(_TASK_KEYS):
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", f"{path} must carry the complete six-field task projection")
        if not isinstance(value["id"], str) or not _TASK_ID_RE.fullmatch(value["id"]):
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", f"{path}.id must be a task ID")
        for key in ("outcome", "slice_type", "verification", "blast_radius"):
            if not isinstance(value[key], str):
                raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", f"{path}.{key} must be text")
        blocking_edges = value["blocking_edges"]
        if (
            not isinstance(blocking_edges, list)
            or any(not isinstance(item, str) or not _TASK_ID_RE.fullmatch(item) or item == value["id"] for item in blocking_edges)
            or len(blocking_edges) != len(set(blocking_edges))
        ):
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", f"{path}.blocking_edges must be a string array")
        if path == "source_task_semantics" and value["id"] != "T-01":
            raise _fail("AMENDMENT_EFFECT_SCOPE_INVALID", "source task effects must identify T-01")
        if path == "target_task_semantics" and value["id"] != "T-02":
            raise _fail("AMENDMENT_EFFECT_SCOPE_INVALID", "target task effects must identify T-02")
        return value["id"]
    if path == "incoming_dependency_edges":
        if not isinstance(value, list):
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "incoming_dependency_edges must be an array")
        targets: set[str] = set()
        normalized: list[tuple[str, str]] = []
        for edge in value:
            if not isinstance(edge, dict) or set(edge) != {"source_task_id", "target_task_id"}:
                raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "each incoming edge must contain exact source/target IDs")
            source, target = edge["source_task_id"], edge["target_task_id"]
            if not isinstance(source, str) or not _TASK_ID_RE.fullmatch(source) or not isinstance(target, str) or not _TASK_ID_RE.fullmatch(target):
                raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "incoming edge IDs must be task IDs")
            targets.add(target)
            normalized.append((source, target))
        if len(targets) > 1 or normalized != sorted(set(normalized)):
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "incoming edges must be sorted and belong to one target task")
        return next(iter(targets), None)
    if path in {"accepted_output_contract_ref", "produced_artifact_logical_ref", "required_input_logical_ref", "acceptance_contract_ref", "evaluation_scope_ref"}:
        if not isinstance(value, str) or not value or value != value.strip():
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", f"{path} must be non-empty trimmed text")
    if path == "required_verifier_contract_refs":
        if not isinstance(value, list) or not value:
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "required verifier refs must be a non-empty array")
        pairs: list[tuple[str, str]] = []
        for item in value:
            if not isinstance(item, dict) or set(item) != {"contract_id", "contract_version_or_ref"}:
                raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "verifier refs must be exact identity pairs")
            left, right = item["contract_id"], item["contract_version_or_ref"]
            if not isinstance(left, str) or not left or left != left.strip() or not isinstance(right, str) or not right or right != right.strip():
                raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "verifier identities must be trimmed strings")
            pairs.append((left, right))
        if pairs != sorted(set(pairs)):
            raise _fail("AMENDMENT_EFFECT_VALUE_INVALID", "verifier refs must be unique and sorted")
    return None


def _split_table_row(line: str) -> list[str] | None:
    stripped = line.strip()
    if not stripped.startswith("|") or not stripped.endswith("|"):
        return None
    return [cell.strip() for cell in stripped[1:-1].split("|")]


def _parse_amendments(amendments: str) -> tuple[list[dict[str, Any]], dict[str, Any], str]:
    """Parse governed amendment rows and the final generated receipt.

    This parser owns the exact eleven-column contiguous table, stable unique IDs,
    supported amendment types, canonical effect JSON, complete before/after
    maps, and the final canonical reconciliation receipt. It hashes canonical-LF
    amendment text only up to that receipt, so the receipt cannot create a
    digest cycle. Malformed, duplicate, noncanonical, or incomplete records fail
    closed before their effects can enter a projection.
    """
    receipt_start, _, receipt_section = _section(amendments, "## Dependency reconciliation receipt")
    receipt_tail = amendments[receipt_start:]
    blocks = _fenced_json_blocks(receipt_section, "DependencyReconciliationReceiptV1")
    if len(blocks) != 1 or not isinstance(blocks[0], dict):
        raise _fail("RECONCILIATION_RECEIPT_INVALID", "one exact JSON receipt is required")
    # The receipt is the final section and contains only its one JSON block.
    stripped_tail = receipt_tail.strip()
    block_match = re.fullmatch(r"(?s)## Dependency reconciliation receipt\n\n```json\n(.*?)\n```", stripped_tail)
    if block_match is None:
        raise _fail("RECONCILIATION_RECEIPT_INVALID", "receipt section must be final and contain only its JSON block")
    if canonical_json(blocks[0]) != block_match.group(1):
        raise _fail("RECONCILIATION_RECEIPT_INVALID", "receipt JSON must use sorted compact canonical encoding")
    lines = amendments.splitlines()
    header_rows = [(index, _split_table_row(line)) for index, line in enumerate(lines) if _split_table_row(line) == list(_AMENDMENT_COLUMNS)]
    if len(header_rows) != 1:
        raise _fail("AMENDMENTS_TABLE_INVALID", "one exact structured amendment table is required")
    header_index = header_rows[0][0]
    separator = _split_table_row(lines[header_index + 1]) if header_index + 1 < len(lines) else None
    if separator is None or len(separator) != len(_AMENDMENT_COLUMNS) or not all(re.fullmatch(r":?-{3,}:?", part) for part in separator):
        raise _fail("AMENDMENTS_TABLE_INVALID", "structured amendment table separator is invalid")
    rows: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    index = header_index + 2
    while index < len(lines) and lines[index].strip() and not lines[index].startswith("## "):
        row = _split_table_row(lines[index])
        if row is None:
            break
        if len(row) != len(_AMENDMENT_COLUMNS):
            raise _fail("AMENDMENTS_TABLE_INVALID", "amendment row has an incorrect number of cells")
        record = dict(zip(_AMENDMENT_COLUMNS, row, strict=True))
        amendment_id = record["Amendment ID"]
        if not amendment_id or amendment_id != amendment_id.strip() or amendment_id in seen_ids:
            raise _fail("AMENDMENT_ID_INVALID", "every amendment needs one stable unique non-empty ID")
        seen_ids.add(amendment_id)
        if record["Type"] not in {"Implementation detail", "Scope"}:
            raise _fail("AMENDMENT_CLASSIFICATION_UNRESOLVED", f"unsupported amendment type for {amendment_id}")
        for label in ("Date", "Trigger and evidence", "Old approach", "New approach", "Approval", "Readiness impact"):
            if not record[label] or record[label] in {"None", "TBD", "TODO"}:
                raise _fail("AMENDMENT_RECORD_INCOMPLETE", f"{amendment_id} needs explicit {label}")
        changed = _parse_json(record["Changed dependency fields"], f"{amendment_id} changed_dependency_fields")
        before = _parse_json(record["Before values"], f"{amendment_id} before_values")
        after = _parse_json(record["After values"], f"{amendment_id} after_values")
        if not isinstance(changed, list) or any(not isinstance(path, str) for path in changed):
            raise _fail("AMENDMENT_EFFECT_INVALID", f"{amendment_id} changed fields must be a string array")
        if changed != sorted(set(changed)) or not isinstance(before, dict) or not isinstance(after, dict) or set(before) != set(changed) or set(after) != set(changed):
            raise _fail("AMENDMENT_EFFECT_INVALID", f"{amendment_id} effects need sorted unique paths and exact complete maps")
        if record["Changed dependency fields"] != canonical_json(changed) or record["Before values"] != canonical_json(before) or record["After values"] != canonical_json(after):
            raise _fail("AMENDMENT_EFFECT_NONCANONICAL", f"{amendment_id} effect JSON must use canonical compact encoding")
        if any(path not in _MUTABLE_FIELDS for path in changed):
            raise _fail("AMENDMENT_EFFECT_FIELD_INVALID", f"{amendment_id} names an unsupported projection field")
        if not changed and (before or after):
            raise _fail("AMENDMENT_EFFECT_INVALID", f"{amendment_id} empty effects must use empty value maps")
        scopes: dict[str, str | None] = {}
        for path in changed:
            before_scope = _validate_effect_value(path, before[path])
            after_scope = _validate_effect_value(path, after[path])
            if path == "incoming_dependency_edges":
                if before_scope is not None and after_scope is not None and before_scope != after_scope:
                    raise _fail("AMENDMENT_EFFECT_SCOPE_INVALID", f"{amendment_id} changes the identity of {path}")
                scope = before_scope or after_scope
                if scope is None:
                    raise _fail("AMENDMENT_EFFECT_SCOPE_INVALID", f"{amendment_id} does not identify an incoming-edge target")
            elif before_scope != after_scope:
                raise _fail("AMENDMENT_EFFECT_SCOPE_INVALID", f"{amendment_id} changes the identity of {path}")
            else:
                scope = before_scope
            if before[path] == after[path]:
                raise _fail("AMENDMENT_EFFECT_INVALID", f"{amendment_id} marks unchanged values as changed")
            scopes[path] = scope
        rows.append({
            "amendment_id": amendment_id,
            "changed_dependency_fields": changed,
            "before_values": before,
            "after_values": after,
            "scopes": scopes,
        })
        index += 1
    receipt_line = next(
        position for position, line in enumerate(lines)
        if line == "## Dependency reconciliation receipt"
    )
    if any(_split_table_row(line) is not None for line in lines[index:receipt_line]):
        raise _fail("AMENDMENTS_TABLE_INVALID", "an amendment table row appears outside the contiguous governed record table")
    amendments_semantics_sha256 = _sha256(amendments[:receipt_start].encode("utf-8"))
    return rows, blocks[0], amendments_semantics_sha256


def _effect_scope_key(path: str, scope: str | None) -> str:
    if path in {"task_semantics", "incoming_dependency_edges"}:
        if scope is None:
            raise _fail("AMENDMENT_EFFECT_SCOPE_INVALID", f"{path} effect must identify a task")
        return f"{path}[{scope}]"
    return path


def _current_effect_value(scope_key: str, contract: Mapping[str, Any], tasks: Mapping[str, OriginalTaskUnitV1], edges: tuple[tuple[str, str], ...]) -> Any:
    if scope_key.startswith("task_semantics["):
        task_id = scope_key[len("task_semantics["):-1]
        if task_id not in tasks:
            raise _fail("EFFECT_SCOPE_UNRESOLVED", f"amendment refers to unknown task {task_id}")
        return _task_map(tasks[task_id])
    if scope_key.startswith("incoming_dependency_edges["):
        task_id = scope_key[len("incoming_dependency_edges["):-1]
        if task_id not in tasks:
            raise _fail("EFFECT_SCOPE_UNRESOLVED", f"amendment refers to incoming edges for unknown task {task_id}")
        return [
            {"source_task_id": source, "target_task_id": target}
            for source, target in sorted(edges)
            if target == task_id
        ]
    return _field_mapping(scope_key, contract, tasks)


def _validate_effect_chain(rows: list[dict[str, Any]], contract: Mapping[str, Any], tasks: Mapping[str, OriginalTaskUnitV1], edges: tuple[tuple[str, str], ...]) -> None:
    """Prove each structured amendment transition joins and ends at current state.

    Amendment row order is authoritative. For each task-scoped projection key,
    every later ``before_values`` must equal the preceding ``after_values``;
    each last value must equal the current approved contract/task graph. Any
    missing join or unresolved final value blocks all requirement resolution.
    """
    previous: dict[str, Any] = {}
    final: dict[str, Any] = {}
    for row in rows:
        for path in row["changed_dependency_fields"]:
            key = _effect_scope_key(path, row["scopes"][path])
            before = row["before_values"][path]
            after = row["after_values"][path]
            if key in previous and previous[key] != before:
                raise _fail("AMENDMENT_EFFECT_CHAIN_INCOMPLETE", f"discontinuous before/after chain for {key}")
            previous[key] = after
            final[key] = after
    for key, after in final.items():
        if after != _current_effect_value(key, contract, tasks, edges):
            raise _fail("AMENDMENT_EFFECT_CHAIN_UNRESOLVED", f"last governed value for {key} differs from current authority")


def _effect_applies_to_dependent(path: str) -> bool:
    return path in {
        "accepted_output_contract_ref",
        "produced_artifact_logical_ref",
        "required_input_logical_ref",
        "acceptance_contract_ref",
        "evaluation_scope_ref",
        "required_verifier_contract_refs",
        "source_task_semantics",
        "target_task_semantics",
    }


def _effect_applies_to_independent(path: str, scope: str | None, task_id: str) -> bool:
    if path == "task_semantics":
        return scope == task_id
    if path == "incoming_dependency_edges":
        return scope == task_id
    return False


def _project_effects(rows: list[dict[str, Any]], *, dependent: bool, task_id: str | None = None) -> list[dict[str, Any]]:
    effects: list[dict[str, Any]] = []
    for row in rows:
        applicable = [
            path for path in row["changed_dependency_fields"]
            if (_effect_applies_to_dependent(path) if dependent else _effect_applies_to_independent(path, row["scopes"][path], task_id or ""))
        ]
        if not applicable:
            continue
        effects.append({
            "amendment_id": row["amendment_id"],
            "changed_dependency_fields": applicable,
            "before_values": {path: row["before_values"][path] for path in applicable},
            "after_values": {path: row["after_values"][path] for path in applicable},
        })
    return effects


def _dependent_projection(change_id: str, contract: Mapping[str, Any], tasks: Mapping[str, OriginalTaskUnitV1], effects: list[dict[str, Any]]) -> dict[str, Any]:
    """Build the exact fixed T-01 -> T-02 projection and its scoped history.

    Only contract refs, the two six-field task meanings, and complete effects
    relevant to this edge enter the mapping. General Plan provenance, task
    status, and unrelated independent-task effects do not enter its digest.
    """
    return {
        "schema_version": 1,
        "change_id": change_id,
        "source_task_id": "T-01",
        "target_task_id": "T-02",
        "edge": {"source_task_id": "T-01", "target_task_id": "T-02"},
        "plan_dependency_contract_version": 2,
        "accepted_output_contract_ref": contract["accepted_output_contract_ref"],
        "produced_artifact_logical_ref": contract["produced_artifact_logical_ref"],
        "required_input_logical_ref": contract["required_input_logical_ref"],
        "acceptance_contract_ref": contract["acceptance_contract_ref"],
        "evaluation_scope_ref": contract["evaluation_scope_ref"],
        "required_verifier_contract_refs": contract["required_verifier_contract_refs"],
        "source_task_semantics": _task_map(tasks["T-01"]),
        "target_task_semantics": _task_map(tasks["T-02"]),
        "dependency_material_amendments": effects,
    }


def _independent_projection(change_id: str, unit: OriginalTaskUnitV1, incoming: list[dict[str, str]], effects: list[dict[str, Any]]) -> dict[str, Any]:
    """Build one task-local NOT_APPLICABLE mapping from a proven empty edge set.

    A caller cannot assert independence: the resolver supplies parsed incoming
    edges and only an empty list is accepted. The own six-field task meaning
    and effects scoped to that task distinguish its digest from other tasks
    and from the Plan's fixed dependent-edge digest.
    """
    if incoming:
        raise _fail("TASK_IS_NOT_INDEPENDENT", f"{unit.task_id} has current incoming dependency edges")
    return {
        "schema_version": 1,
        "dependency_classification": "NOT_APPLICABLE",
        "change_id": change_id,
        "task_or_operation_id": unit.task_id,
        "task_semantics": _task_map(unit),
        "incoming_dependency_edges": incoming,
        "applicable_dependency_material_amendments": effects,
    }


def _requirement(change_id: str, plan_ref: str, tasks_ref: str, digest: str, contract: Mapping[str, Any], dependent: bool) -> dict[str, Any]:
    """Derive the exact resolver-only V2 requirement and its content ID.

    Dependent fields bind T-01/A1 -> T-02/A1 and the exact contract values;
    independent fields are explicit nulls/empty array. The ``dreq_`` ID hashes
    every other field in canonical JSON with no trailing LF. This value names
    a requirement; only a later existing Authorization owner may grant action.
    """
    if dependent:
        fields: dict[str, Any] = {
            "dependency_classification": "DEPENDENCY_EDGE_MEMBER",
            "source_task_or_operation_id": "T-01",
            "source_attempt_id": f"{change_id}/T-01/A1",
            "successor_task_or_operation_id": "T-02",
            "successor_attempt_id": f"{change_id}/T-02/A1",
            "accepted_output_contract_ref": contract["accepted_output_contract_ref"],
            "produced_artifact_logical_ref": contract["produced_artifact_logical_ref"],
            "required_successor_input_logical_ref": contract["required_input_logical_ref"],
            "acceptance_contract_ref": contract["acceptance_contract_ref"],
            "evaluation_scope_ref": contract["evaluation_scope_ref"],
            "required_verifier_contract_refs": contract["required_verifier_contract_refs"],
        }
    else:
        fields = {
            "dependency_classification": "NOT_APPLICABLE",
            "source_task_or_operation_id": None,
            "source_attempt_id": None,
            "successor_task_or_operation_id": None,
            "successor_attempt_id": None,
            "accepted_output_contract_ref": None,
            "produced_artifact_logical_ref": None,
            "required_successor_input_logical_ref": None,
            "acceptance_contract_ref": None,
            "evaluation_scope_ref": None,
            "required_verifier_contract_refs": [],
        }
    without_id = {
        "schema_version": 2,
        "change_id": change_id,
        "plan_ref": plan_ref,
        "tasks_ref": tasks_ref,
        "dependency_semantic_digest": digest,
        **fields,
    }
    result = {"schema_version": 2, "requirement_id": "dreq_" + _sha256_json(without_id), **{key: value for key, value in without_id.items() if key != "schema_version"}}
    if set(result) != _REQUIREMENT_KEYS:
        raise _fail("INTERNAL_REQUIREMENT_SCHEMA_INVALID", "derived requirement does not match DependencyRequirementV2")
    return result


def _validate_requirement(requirement: Mapping[str, Any], root: str | Path) -> None:
    """Reject non-exact V2 requirement objects and forged content IDs."""
    if not isinstance(requirement, Mapping) or set(requirement) != _REQUIREMENT_KEYS:
        raise _fail("BOUND_REQUIREMENT_INVALID", "bound requirement has an incorrect key set")
    if type(requirement["schema_version"]) is not int or requirement["schema_version"] != 2:
        raise _fail("BOUND_REQUIREMENT_INVALID", "bound requirement version must be integer 2")
    change_id = requirement["change_id"]
    if not isinstance(change_id, str) or not _CHANGE_ID_RE.fullmatch(change_id):
        raise _fail("BOUND_REQUIREMENT_INVALID", "bound requirement Change ID is malformed")
    _, planning_root_ref, _ = _effective_planning_root(root)
    _, expected_plan_ref, expected_tasks_ref, _ = _change_refs(change_id, planning_root_ref)
    if requirement["plan_ref"] != expected_plan_ref or requirement["tasks_ref"] != expected_tasks_ref:
        raise _fail("BOUND_REQUIREMENT_INVALID", "bound requirement refs are not normalized active-Change refs")
    if not isinstance(requirement["dependency_semantic_digest"], str) or not _SHA256_RE.fullmatch(requirement["dependency_semantic_digest"]):
        raise _fail("BOUND_REQUIREMENT_INVALID", "bound dependency digest must be lowercase SHA-256")
    classification = requirement["dependency_classification"]
    if classification == "DEPENDENCY_EDGE_MEMBER":
        expected = {
            "source_task_or_operation_id": "T-01",
            "source_attempt_id": f"{change_id}/T-01/A1",
            "successor_task_or_operation_id": "T-02",
            "successor_attempt_id": f"{change_id}/T-02/A1",
        }
        if any(requirement[name] != value for name, value in expected.items()):
            raise _fail("BOUND_REQUIREMENT_INVALID", "dependent requirement must bind the fixed T-01/A1 -> T-02/A1 edge")
        for name in (
            "accepted_output_contract_ref",
            "produced_artifact_logical_ref",
            "required_successor_input_logical_ref",
            "acceptance_contract_ref",
            "evaluation_scope_ref",
        ):
            value = requirement[name]
            if not isinstance(value, str) or not value or value != value.strip():
                raise _fail("BOUND_REQUIREMENT_INVALID", f"dependent requirement {name} is invalid")
        verifier_refs = requirement["required_verifier_contract_refs"]
        if not isinstance(verifier_refs, list) or not verifier_refs:
            raise _fail("BOUND_REQUIREMENT_INVALID", "dependent requirement needs verifier identities")
        verifier_pairs: list[tuple[str, str]] = []
        for pair in verifier_refs:
            if not isinstance(pair, dict) or set(pair) != {"contract_id", "contract_version_or_ref"}:
                raise _fail("BOUND_REQUIREMENT_INVALID", "dependent verifier identity has an incorrect shape")
            left, right = pair["contract_id"], pair["contract_version_or_ref"]
            if not isinstance(left, str) or not left or left != left.strip() or not isinstance(right, str) or not right or right != right.strip():
                raise _fail("BOUND_REQUIREMENT_INVALID", "dependent verifier identities must be trimmed strings")
            verifier_pairs.append((left, right))
        if verifier_pairs != sorted(set(verifier_pairs)):
            raise _fail("BOUND_REQUIREMENT_INVALID", "dependent verifier identities must be sorted and unique")
    elif classification == "NOT_APPLICABLE":
        nullable = (
            "source_task_or_operation_id",
            "source_attempt_id",
            "successor_task_or_operation_id",
            "successor_attempt_id",
            "accepted_output_contract_ref",
            "produced_artifact_logical_ref",
            "required_successor_input_logical_ref",
            "acceptance_contract_ref",
            "evaluation_scope_ref",
        )
        if any(requirement[name] is not None for name in nullable) or requirement["required_verifier_contract_refs"] != []:
            raise _fail("BOUND_REQUIREMENT_INVALID", "independent requirement must use explicit nulls and an empty verifier array")
    else:
        raise _fail("BOUND_REQUIREMENT_INVALID", "dependency classification is unsupported")
    value = dict(requirement)
    requirement_id = value.pop("requirement_id")
    if not isinstance(requirement_id, str) or not re.fullmatch(r"dreq_[0-9a-f]{64}", requirement_id):
        raise _fail("BOUND_REQUIREMENT_INVALID", "bound requirement ID is malformed")
    expected = "dreq_" + _sha256_json(value)
    if requirement_id != expected:
        raise _fail("BOUND_REQUIREMENT_ID_MISMATCH", "bound requirement ID does not match its canonical preimage")


def resolve_dependency(root: str | Path, task_id: str) -> DependencyResolution:
    """Resolve exact current governance and derive the requested task requirement.

    The effective-policy root owns the only active pointer. Paths are derived
    from that ID and returned relative to the product root; no fallback, merge,
    caller path, or ref search is accepted. Plan approval metadata and the final
    amendments receipt must match recomputed hashes. Requests for either
    endpoint of the fixed T-01 -> T-02 edge receive the same dependent edge
    projection and requirement identity. The Preparation scope remains
    endpoint-specific through ``task_id``. Other supported tasks receive their
    own independent projection only when the parsed graph proves no incoming
    edge. The returned result is transient semantic data, never runtime authority.
    """
    if not isinstance(task_id, str) or not _TASK_ID_RE.fullmatch(task_id):
        raise _fail("TASK_ID_INVALID", "requested task ID is invalid")
    root_path, planning_root_ref, _ = _effective_planning_root(root)
    change_id = _active_change(root_path, planning_root_ref)
    folder, plan_ref, tasks_ref, amendments_ref = _change_refs(change_id, planning_root_ref)
    _validate_change_identity(root_path, folder, change_id)
    plan, _ = _read_text(root_path, plan_ref)
    tasks_text, _ = _read_text(root_path, tasks_ref)
    amendments, _ = _read_text(root_path, amendments_ref)

    status = _one_field(plan, "Status")
    if status != "Approved":
        raise _fail("PLAN_NOT_APPROVED", "Plan Status must be exactly Approved")
    _required_nonempty(plan, "Approved by")
    _required_nonempty(plan, "Approval evidence")
    _required_nonempty(plan, "Approval date")
    approved_digest_metadata = _required_nonempty(plan, "Approved plan digest")
    dependent_digest_metadata = _required_nonempty(plan, "Dependency semantic digest")
    if not _SHA256_RE.fullmatch(approved_digest_metadata) or not _SHA256_RE.fullmatch(dependent_digest_metadata):
        raise _fail("APPROVAL_DIGEST_INVALID", "approved digest fields must be lowercase SHA-256")

    plan_semantics_start, _, _ = _section(plan, "## Approved outcome and exclusions")
    plan_semantics_sha256 = _sha256(plan[plan_semantics_start:].encode("utf-8"))
    contract = _parse_contract(plan)
    units, edges, task_semantics_sha256 = _parse_task_governance(tasks_text)
    if task_id not in units:
        raise _fail("REQUESTED_TASK_MISSING", f"task table has no {task_id}")

    amendment_rows, receipt, amendments_semantics_sha256 = _parse_amendments(amendments)
    _validate_effect_chain(amendment_rows, contract, units, edges)
    dependent_effects = _project_effects(amendment_rows, dependent=True)
    dependent_projection = _dependent_projection(change_id, contract, units, dependent_effects)
    dependent_digest = _sha256_json(dependent_projection)
    expected_material_ids = [effect["amendment_id"] for effect in dependent_effects]
    approval_mapping = {
        "schema_version": 1,
        "change_id": change_id,
        "plan_ref": plan_ref,
        "tasks_ref": tasks_ref,
        "amendments_ref": amendments_ref,
        "plan_semantics_sha256": plan_semantics_sha256,
        "task_semantics_sha256": task_semantics_sha256,
        "amendments_semantics_sha256": amendments_semantics_sha256,
        "dependency_semantic_digest": dependent_digest,
    }
    approved_plan_digest = _sha256_json(approval_mapping)
    if dependent_digest_metadata != dependent_digest or approved_digest_metadata != approved_plan_digest:
        raise _fail("APPROVED_PLAN_DIGEST_STALE", "Plan approval digest metadata does not match current semantics")
    expected_receipt = {
        "schema_version": 1,
        "change_id": change_id,
        "status": "RECONCILED",
        "approved_plan_digest": approved_plan_digest,
        "dependency_semantic_digest": dependent_digest,
        "amendments_semantics_sha256": amendments_semantics_sha256,
        "applicable_dependency_material_amendment_ids": expected_material_ids,
    }
    if set(receipt) != _RECEIPT_KEYS or canonical_json(receipt) != canonical_json(expected_receipt):
        raise _fail("RECONCILIATION_RECEIPT_STALE", "amendments reconciliation receipt does not match current governance")

    incoming = [
        {"source_task_id": source, "target_task_id": target}
        for source, target in sorted(edges)
        if target == task_id
    ]
    if task_id in {"T-01", "T-02"}:
        projection = dependent_projection
        digest = dependent_digest
        dependent = True
        classification = "DEPENDENCY_EDGE_MEMBER"
    else:
        independent_effects = _project_effects(amendment_rows, dependent=False, task_id=task_id)
        projection = _independent_projection(change_id, units[task_id], incoming, independent_effects)
        digest = _sha256_json(projection)
        dependent = False
        classification = "NOT_APPLICABLE"
    requirement = _requirement(change_id, plan_ref, tasks_ref, digest, contract, dependent)
    return DependencyResolution(
        change_id=change_id,
        task_id=task_id,
        dependency_classification=classification,
        plan_ref=plan_ref,
        tasks_ref=tasks_ref,
        amendments_ref=amendments_ref,
        plan_semantics_sha256=plan_semantics_sha256,
        task_semantics_sha256=task_semantics_sha256,
        amendments_semantics_sha256=amendments_semantics_sha256,
        approved_plan_digest=approved_plan_digest,
        dependent_projection=dependent_projection,
        dependent_dependency_semantic_digest=dependent_digest,
        projection=projection,
        dependency_semantic_digest=digest,
        requirement=requirement,
        reconciliation_receipt=receipt,
        history_complete=True,
        task_status=units[task_id].status,
    )


class DependencyProofError(ValueError):
    """A dependency proof/capture value is incomplete, conflicting, or unsafe."""

    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


def _proof_fail(code: str, message: str) -> DependencyProofError:
    return DependencyProofError(code, message)


def _proof_json_bytes(value: Any) -> bytes:
    try:
        return canonical_json(value).encode("utf-8", errors="strict")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise _proof_fail("PROOF_JSON_INVALID", "proof value is not finite canonical UTF-8 JSON") from exc


def _proof_mapping(value: Any, keys: frozenset[str] | set[str], where: str) -> dict[str, Any]:
    if not isinstance(value, Mapping) or set(value) != set(keys):
        raise _proof_fail("PROOF_SCHEMA_INVALID", f"{where} has an incorrect key set")
    return dict(value)


def _proof_string(value: Any, where: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise _proof_fail("PROOF_JOIN_INVALID", f"{where} must be a non-empty trimmed string")
    return value


def _proof_digest(value: Any, where: str) -> str:
    if not isinstance(value, str) or not _SHA256_RE.fullmatch(value):
        raise _proof_fail("PROOF_DIGEST_INVALID", f"{where} must be lowercase SHA-256")
    return value


@dataclass(frozen=True, slots=True, init=False)
class CapturedJsonValueV1:
    """Immutable exact two-key capture of one complete PL08 owner mapping.

    The value is held as canonical bytes, so freezing this record also freezes
    nested arrays and mappings. Its digest covers canonical JSON(value) without
    LF; the wrapper has no tag or type-specific alternate field.
    """

    content_digest: str
    _value_json: bytes

    def __init__(self, content_digest: str, value_json: bytes) -> None:
        _proof_digest(content_digest, "CapturedJsonValueV1.content_digest")
        try:
            decoded = json.loads(value_json.decode("utf-8", errors="strict"), object_pairs_hook=_unique_object, parse_constant=_reject_constant)
        except (AttributeError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
            raise _proof_fail("CAPTURE_WRAPPER_INVALID", "CapturedJsonValueV1 value bytes are invalid") from exc
        if not isinstance(decoded, Mapping) or _sha256(_proof_json_bytes(decoded)) != content_digest:
            raise _proof_fail("CAPTURE_WRAPPER_DIGEST_MISMATCH", "CapturedJsonValueV1 content digest does not match value")
        if _proof_json_bytes(decoded) != value_json:
            raise _proof_fail("CAPTURE_WRAPPER_INVALID", "CapturedJsonValueV1 value bytes are not canonical")
        object.__setattr__(self, "content_digest", content_digest)
        object.__setattr__(self, "_value_json", value_json)

    @classmethod
    def from_value(cls, value: Any) -> "CapturedJsonValueV1":
        if hasattr(value, "to_mapping") and callable(value.to_mapping):
            value = value.to_mapping()
        if not isinstance(value, Mapping):
            raise _proof_fail("CAPTURE_WRAPPER_INVALID", "CapturedJsonValueV1.value must be a complete mapping")
        encoded = _proof_json_bytes(value)
        return cls(_sha256(encoded), encoded)

    @classmethod
    def from_mapping(cls, value: Any) -> "CapturedJsonValueV1":
        mapping = _proof_mapping(value, {"content_digest", "value"}, "CapturedJsonValueV1")
        wrapped = cls.from_value(mapping["value"])
        if mapping["content_digest"] != wrapped.content_digest:
            raise _proof_fail("CAPTURE_WRAPPER_DIGEST_MISMATCH", "CapturedJsonValueV1 content digest does not match value")
        return wrapped

    @property
    def value(self) -> dict[str, Any]:
        return json.loads(self._value_json.decode("utf-8"), object_pairs_hook=_unique_object)

    def to_mapping(self) -> dict[str, Any]:
        return {"content_digest": self.content_digest, "value": self.value}


@dataclass(frozen=True, slots=True, init=False)
class DependencyAcceptanceProofV1:
    """Immutable inert D6 snapshot; proof identity covers the complete mapping.

    ``proof_id`` is ``dproof_`` plus SHA-256 of canonical JSON for every proof
    field except ``proof_id`` and ``proof_digest`` themselves, including the
    three exact ordered PL08 wrapper arrays and evidence-content coverage.
    Stored canonical bytes are immutable; their existence does not install a
    proof head, create admission, establish currentness, or authorize execution.
    """

    _canonical_json: bytes

    def __init__(self, canonical_json_bytes: bytes) -> None:
        object.__setattr__(self, "_canonical_json", canonical_json_bytes)

    @classmethod
    def from_mapping(
        cls, value: Any, *, current_requirement: Mapping[str, Any] | None = None
    ) -> "DependencyAcceptanceProofV1":
        mapping = _validate_dependency_acceptance_proof(value, current_requirement=current_requirement)
        return cls(_proof_json_bytes(mapping))

    @property
    def proof_id(self) -> str:
        return self.to_mapping()["proof_id"]

    @property
    def proof_digest(self) -> str:
        return self.to_mapping()["proof_digest"]

    def to_mapping(self) -> dict[str, Any]:
        return json.loads(self._canonical_json.decode("utf-8"), object_pairs_hook=_unique_object)


_PROOF_KEYS = frozenset({
    "schema_version", "proof_id", "proof_digest", "change_id",
    "source_task_or_operation_id", "source_attempt_id",
    "successor_task_or_operation_id", "successor_attempt_id",
    "dependency_semantic_digest", "observed_result_id",
    "observed_result_content_digest", "observed_result",
    "attempt_evaluation_input", "acceptance_contract_ref", "acceptance_contract",
    "evaluation_scope_ref", "required_verifier_contract_refs",
    "verifier_evidence_inputs", "evidence_ref_contents",
    "evidence_supersession_inputs", "finding_inputs", "technical_evaluation_id",
    "technical_evaluation_outcome", "technical_evaluation", "artifact_logical_ref",
    "artifact_digest",
})
_WRAPPER_KEYS = frozenset({"content_digest", "value"})
_IDENTITY_KEYS = frozenset({"contract_id", "contract_version_or_ref"})


def _strict_pl08_mapping(value: Any, expected: type, decoder: Any, where: str) -> dict[str, Any]:
    if isinstance(value, expected):
        mapping = value.to_mapping()
    else:
        mapping = decoder(value).to_mapping()
    if not isinstance(mapping, dict):
        raise _proof_fail("PROOF_SCHEMA_INVALID", f"{where} did not produce a mapping")
    return mapping


def _decode_identity_ref(value: Any) -> _pl08.IdentityRefV1:
    item = _proof_mapping(value, {"ref", "identity"}, "IdentityRefV1")
    return _pl08.IdentityRefV1(item["ref"], item["identity"])


def _decode_candidate(value: Any) -> _pl08.CandidateIdentityV1:
    item = _proof_mapping(value, {"kind", "head", "dirty_manifest"}, "CandidateIdentityV1")
    if not isinstance(item["dirty_manifest"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "CandidateIdentityV1 dirty_manifest must be an array")
    entries = []
    for row in item["dirty_manifest"]:
        entry = _proof_mapping(row, {"path", "change_kind", "content_identity", "source_path"}, "DirtyPathEntryV1")
        content = _proof_mapping(entry["content_identity"], {"before", "after"}, "DirtyPathEntryV1.content_identity")
        entries.append(_pl08.DirtyPathEntryV1(entry["path"], entry["change_kind"], content["before"], content["after"], entry["source_path"]))
    return _pl08.CandidateIdentityV1(item["kind"], item["head"], tuple(entries))


def _decode_verifier_contract(value: Any) -> _pl08.VerifierContractV1:
    item = _proof_mapping(value, {
        "schema_version", "acceptance_contract_ref", "contract_id",
        "contract_version_or_ref", "required", "evidence_class", "predicate",
        "required_evidence_refs", "failure_semantics",
    }, "VerifierContractV1")
    if type(item["schema_version"]) is not int or item["schema_version"] != 1:
        raise _proof_fail("PROOF_SCHEMA_INVALID", "VerifierContractV1 schema_version must be integer 1")
    if not isinstance(item["required_evidence_refs"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "VerifierContractV1 required_evidence_refs must be an array")
    return _pl08.VerifierContractV1(
        item["acceptance_contract_ref"], item["contract_id"],
        item["contract_version_or_ref"], item["required"], item["evidence_class"],
        item["predicate"], tuple(item["required_evidence_refs"]), item["failure_semantics"],
    )


def _decode_acceptance_contract(value: Any) -> _pl08.AcceptanceContractV1:
    item = _proof_mapping(value, {"schema_version", "acceptance_contract_ref", "verifier_contracts"}, "AcceptanceContractV1")
    if type(item["schema_version"]) is not int or item["schema_version"] != 1 or not isinstance(item["verifier_contracts"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "AcceptanceContractV1 schema or verifier array is invalid")
    return _pl08.AcceptanceContractV1(
        item["acceptance_contract_ref"], tuple(_decode_verifier_contract(row) for row in item["verifier_contracts"])
    )


def _decode_evidence_applicability(value: Any) -> _pl08.EvidenceApplicabilityV1:
    item = _proof_mapping(value, {
        "attempt_id", "candidate_identity", "acceptance_contract_ref",
        "verifier_contract_ref", "verifier_contract_version_or_ref",
        "evaluation_scope_ref", "finding_refs", "input_baseline_refs",
    }, "EvidenceApplicabilityV1")
    if not isinstance(item["finding_refs"], list) or not isinstance(item["input_baseline_refs"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "evidence applicability arrays are invalid")
    return _pl08.EvidenceApplicabilityV1(
        item["attempt_id"], _decode_candidate(item["candidate_identity"]),
        item["acceptance_contract_ref"], item["verifier_contract_ref"],
        item["verifier_contract_version_or_ref"], item["evaluation_scope_ref"],
        tuple(item["finding_refs"]), tuple(_decode_identity_ref(ref) for ref in item["input_baseline_refs"]),
    )


def _decode_verifier_evidence(value: Any) -> _pl08.VerifierEvidenceV1:
    item = _proof_mapping(value, {
        "evidence_id", "attempt_id", "candidate_identity", "verifier_contract_ref",
        "verifier_contract_version_or_ref", "outcome", "evidence_refs", "claim_refs", "applicability",
    }, "VerifierEvidenceV1")
    if not isinstance(item["evidence_refs"], list) or not isinstance(item["claim_refs"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "VerifierEvidenceV1 refs must be arrays")
    return _pl08.VerifierEvidenceV1(
        item["evidence_id"], item["attempt_id"], _decode_candidate(item["candidate_identity"]),
        item["verifier_contract_ref"], item["verifier_contract_version_or_ref"], item["outcome"],
        tuple(item["evidence_refs"]), _decode_evidence_applicability(item["applicability"]),
        tuple(item["claim_refs"]),
    )


def _decode_supersession(value: Any) -> _pl08.EvidenceSupersessionV1:
    item = _proof_mapping(value, {
        "schema_version", "prior_evidence_ref", "successor_evidence_ref",
        "current_acceptance_scope_ref", "rechecked_claim_refs", "reason",
    }, "EvidenceSupersessionV1")
    if type(item["schema_version"]) is not int or item["schema_version"] != 1 or not isinstance(item["rechecked_claim_refs"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "EvidenceSupersessionV1 schema or rechecked refs are invalid")
    return _pl08.EvidenceSupersessionV1(
        item["prior_evidence_ref"], item["successor_evidence_ref"],
        item["current_acceptance_scope_ref"], tuple(item["rechecked_claim_refs"]), item["reason"],
    )


def _decode_finding(value: Any) -> _pl08.FindingV1:
    item = _proof_mapping(value, {
        "finding_id", "statement", "severity", "responsibility_domains", "acceptance_impact",
        "disposition", "owner_adjudication_ref", "evidence_refs", "applicability",
    }, "FindingV1")
    if not isinstance(item["responsibility_domains"], list) or not isinstance(item["evidence_refs"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "FindingV1 arrays are invalid")
    app_raw = item["applicability"]
    app = None
    if app_raw is not None:
        app_value = _proof_mapping(app_raw, {
            "attempt_id", "candidate_identity", "acceptance_contract_ref",
            "evaluation_scope_ref", "input_baseline_refs",
        }, "FindingApplicabilityV1")
        if not isinstance(app_value["input_baseline_refs"], list):
            raise _proof_fail("PROOF_SCHEMA_INVALID", "finding baseline refs must be an array")
        app = _pl08.FindingApplicabilityV1(
            app_value["attempt_id"], _decode_candidate(app_value["candidate_identity"]),
            app_value["acceptance_contract_ref"], app_value["evaluation_scope_ref"],
            tuple(_decode_identity_ref(ref) for ref in app_value["input_baseline_refs"]),
        )
    return _pl08.FindingV1(
        item["finding_id"], item["statement"], item["severity"],
        tuple(item["responsibility_domains"]), item["acceptance_impact"],
        item["disposition"], tuple(item["evidence_refs"]),
        item["owner_adjudication_ref"], app,
    )


def _decode_technical_evaluation(value: Any) -> _pl08.TechnicalEvaluationV1:
    item = _proof_mapping(value, {
        "schema_version", "evaluation_id", "attempt_id", "candidate_identity",
        "acceptance_contract_ref", "declared_verifier_contract_refs",
        "required_verifier_contract_refs", "outcome", "evidence_complete",
        "required_evidence_refs", "applicable_finding_refs", "reason_codes",
    }, "TechnicalEvaluationV1")
    if type(item["schema_version"]) is not int or item["schema_version"] != 1:
        raise _proof_fail("PROOF_SCHEMA_INVALID", "TechnicalEvaluationV1 schema_version must be integer 1")
    array_fields = ("declared_verifier_contract_refs", "required_verifier_contract_refs", "required_evidence_refs", "applicable_finding_refs", "reason_codes")
    if any(not isinstance(item[name], list) for name in array_fields):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "TechnicalEvaluationV1 arrays are invalid")
    def pairs(rows: list[Any], where: str) -> tuple[tuple[str, str], ...]:
        out = []
        for row in rows:
            pair = _proof_mapping(row, _IDENTITY_KEYS, where)
            out.append((pair["contract_id"], pair["contract_version_or_ref"]))
        return tuple(out)
    candidate = None if item["candidate_identity"] is None else _decode_candidate(item["candidate_identity"])
    return _pl08.TechnicalEvaluationV1(
        item["evaluation_id"], item["attempt_id"], candidate,
        item["acceptance_contract_ref"], pairs(item["declared_verifier_contract_refs"], "declared verifier identity"),
        pairs(item["required_verifier_contract_refs"], "required verifier identity"), item["outcome"],
        item["evidence_complete"], tuple(item["required_evidence_refs"]),
        tuple(item["applicable_finding_refs"]), tuple(item["reason_codes"]),
    )


def _decode_observed_result(value: Any) -> _pl08.ObservedResultV1:
    item = _proof_mapping(value, {
        "schema_version", "result_id", "attempt_id", "execution_status",
        "changed_paths", "fact_refs", "artifact_refs",
    }, "ObservedResultV1")
    if type(item["schema_version"]) is not int or item["schema_version"] != 1:
        raise _proof_fail("PROOF_SCHEMA_INVALID", "ObservedResultV1 schema_version must be integer 1")
    if any(not isinstance(item[name], list) for name in ("changed_paths", "fact_refs", "artifact_refs")):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "ObservedResultV1 arrays are invalid")
    return _pl08.ObservedResultV1(
        item["result_id"], item["attempt_id"], item["execution_status"],
        tuple(item["changed_paths"]), tuple(item["fact_refs"]), tuple(item["artifact_refs"]),
    )


def _owner_mapping(value: Any, expected: type, decoder: Any, where: str) -> dict[str, Any]:
    try:
        return _strict_pl08_mapping(value, expected, decoder, where)
    except DependencyProofError:
        raise
    except Exception as exc:
        raise _proof_fail("PROOF_INPUT_INVALID", f"{where} is not a valid complete owner mapping") from exc


def _capture_wrapper(value: Any, expected: type, decoder: Any, where: str) -> dict[str, Any]:
    mapping = _owner_mapping(value, expected, decoder, where)
    return CapturedJsonValueV1.from_value(mapping).to_mapping()


def _wrapper_value(value: Any, decoder: Any, where: str) -> tuple[dict[str, Any], CapturedJsonValueV1]:
    wrapper = CapturedJsonValueV1.from_mapping(value)
    try:
        typed = decoder(wrapper.value)
    except DependencyProofError:
        raise
    except Exception as exc:
        raise _proof_fail("PROOF_INPUT_INVALID", f"{where} is not a valid complete owner value") from exc
    if canonical_json(typed.to_mapping()) != canonical_json(wrapper.value):
        raise _proof_fail("PROOF_SCHEMA_INVALID", f"{where} does not preserve its exact typed mapping")
    return typed.to_mapping(), wrapper


def _identity_pairs(value: Any, where: str) -> tuple[tuple[str, str], ...]:
    if not isinstance(value, list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", f"{where} must be an array")
    pairs = []
    for row in value:
        pair = _proof_mapping(row, _IDENTITY_KEYS, where)
        pairs.append((_proof_string(pair["contract_id"], where), _proof_string(pair["contract_version_or_ref"], where)))
    if len(set(pairs)) != len(pairs):
        raise _proof_fail("PROOF_JOIN_INVALID", f"{where} contains duplicate verifier identities")
    return tuple(pairs)


def _validate_dependency_acceptance_proof(
    value: Any, *, current_requirement: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    """Strictly validate D6's exact schema, typed values, content joins and ID.

    This validates but never runs PL08: the supplied TechnicalEvaluationV1 is
    captured as the live owner's result. Structurally valid inapplicable inputs
    remain in their original order. Required evidence and Finding/supersession
    content refs require exactly one identity/digest entry; semantic refs are
    never converted to filesystem locations.
    """
    proof = _proof_mapping(value, _PROOF_KEYS, "DependencyAcceptanceProofV1")
    if type(proof["schema_version"]) is not int or proof["schema_version"] != 1:
        raise _proof_fail("PROOF_SCHEMA_INVALID", "DependencyAcceptanceProofV1 schema_version must be integer 1")
    change_id = _proof_string(proof["change_id"], "change_id")
    source_id = f"{change_id}/T-01/A1"
    successor_id = f"{change_id}/T-02/A1"
    exact_strings = (
        "source_task_or_operation_id", "source_attempt_id", "successor_task_or_operation_id",
        "successor_attempt_id", "observed_result_id", "acceptance_contract_ref",
        "evaluation_scope_ref", "technical_evaluation_id", "technical_evaluation_outcome",
        "artifact_logical_ref",
    )
    for field in exact_strings:
        _proof_string(proof[field], field)
    if (
        proof["source_task_or_operation_id"] != "T-01"
        or proof["source_attempt_id"] != source_id
        or proof["successor_task_or_operation_id"] != "T-02"
        or proof["successor_attempt_id"] != successor_id
    ):
        raise _proof_fail("PROOF_JOIN_INVALID", "proof must bind exact current T-01/A1 -> T-02/A1")
    dependency_digest = _proof_digest(proof["dependency_semantic_digest"], "dependency_semantic_digest")
    _proof_digest(proof["artifact_digest"], "artifact_digest")

    observed, observed_wrapper = _wrapper_value(proof["observed_result"], _decode_observed_result, "ObservedResultV1")
    contract, _ = _wrapper_value(proof["acceptance_contract"], _decode_acceptance_contract, "AcceptanceContractV1")
    evaluation, _ = _wrapper_value(proof["technical_evaluation"], _decode_technical_evaluation, "TechnicalEvaluationV1")
    if proof["observed_result_id"] != observed["result_id"] or proof["observed_result_content_digest"] != observed_wrapper.content_digest:
        raise _proof_fail("PROOF_JOIN_INVALID", "ObservedResultV1 identity/content digest does not join")
    if observed["attempt_id"] != source_id or observed["execution_status"] != "COMPLETED":
        raise _proof_fail("PROOF_JOIN_INVALID", "ObservedResultV1 must be completed for exact T-01/A1")
    if proof["artifact_logical_ref"] not in observed["artifact_refs"]:
        raise _proof_fail("PROOF_JOIN_INVALID", "ObservedResultV1 does not name the exact artifact logical ref")
    if proof["acceptance_contract_ref"] != contract["acceptance_contract_ref"]:
        raise _proof_fail("PROOF_JOIN_INVALID", "AcceptanceContractV1 ref does not join")
    if proof["technical_evaluation_id"] != evaluation["evaluation_id"] or proof["technical_evaluation_outcome"] != "SATISFIED":
        raise _proof_fail("PROOF_JOIN_INVALID", "TechnicalEvaluationV1 identity/outcome does not join")
    if evaluation["outcome"] != "SATISFIED" or evaluation["evidence_complete"] is not True or evaluation["candidate_identity"] is None:
        raise _proof_fail("PROOF_NOT_SATISFIED", "only a complete SATISFIED PL08 result can be captured")

    attempt = _proof_mapping(proof["attempt_evaluation_input"], {
        "attempt_id", "candidate_identity", "baseline_refs", "acceptance_contract_ref",
        "verifier_contract_refs", "evaluation_id", "evaluation_scope_ref", "evaluation_run", "candidate_quality",
    }, "AttemptEvaluationInputV1")
    candidate = _decode_candidate(attempt["candidate_identity"]).to_mapping()
    if not isinstance(attempt["baseline_refs"], list) or not attempt["baseline_refs"]:
        raise _proof_fail("PROOF_JOIN_INVALID", "AttemptEvaluationInputV1 baseline_refs must be non-empty")
    baselines = [_decode_identity_ref(ref).to_mapping() for ref in attempt["baseline_refs"]]
    attempt_verifiers = _identity_pairs(attempt["verifier_contract_refs"], "attempt verifier refs")
    if type(attempt["evaluation_run"]) is not bool or type(attempt["candidate_quality"]) is not bool:
        raise _proof_fail("PROOF_SCHEMA_INVALID", "AttemptEvaluationInputV1 state flags must be booleans")
    if attempt["evaluation_run"] is not True or attempt["candidate_quality"] is not True:
        raise _proof_fail("PROOF_NOT_SATISFIED", "captured PL08 input flags must both be true for a SATISFIED proof")
    if attempt["attempt_id"] != source_id or attempt["acceptance_contract_ref"] != proof["acceptance_contract_ref"]:
        raise _proof_fail("PROOF_JOIN_INVALID", "AttemptEvaluationInputV1 does not bind exact source/contract")
    if attempt["evaluation_id"] != evaluation["evaluation_id"] or attempt["evaluation_scope_ref"] != proof["evaluation_scope_ref"]:
        raise _proof_fail("PROOF_JOIN_INVALID", "AttemptEvaluationInputV1 does not bind exact evaluation/scope")
    if canonical_json(candidate) != canonical_json(evaluation["candidate_identity"]):
        raise _proof_fail("PROOF_JOIN_INVALID", "TechnicalEvaluationV1 candidate does not match captured input")
    if evaluation["attempt_id"] != source_id or evaluation["acceptance_contract_ref"] != proof["acceptance_contract_ref"]:
        raise _proof_fail("PROOF_JOIN_INVALID", "TechnicalEvaluationV1 does not bind exact source/contract")

    if not isinstance(proof["required_verifier_contract_refs"], list):
        raise _proof_fail("PROOF_SCHEMA_INVALID", "required_verifier_contract_refs must be an array")
    if not proof["required_verifier_contract_refs"]:
        raise _proof_fail("EMPTY_REQUIRED_VERIFIER_SET", "M14: required_verifier_contract_refs must be non-empty")
    required_pairs = _identity_pairs(proof["required_verifier_contract_refs"], "required verifier refs")
    contract_rows = contract["verifier_contracts"]
    if any(row["required"] is not True for row in contract_rows):
        raise _proof_fail("PROOF_JOIN_INVALID", "dependency AcceptanceContract requires every approved verifier")
    contract_pairs = tuple((row["contract_id"], row["contract_version_or_ref"]) for row in contract_rows)
    if len(set(contract_pairs)) != len(contract_pairs) or set(required_pairs) != set(contract_pairs):
        raise _proof_fail("PROOF_JOIN_INVALID", "required verifiers do not exactly match AcceptanceContract")
    declared_pairs = _identity_pairs(evaluation["declared_verifier_contract_refs"], "PL08 declared verifier refs")
    evaluation_required_pairs = _identity_pairs(evaluation["required_verifier_contract_refs"], "PL08 required verifier refs")
    if any(set(values) != set(required_pairs) for values in (attempt_verifiers, declared_pairs, evaluation_required_pairs)):
        raise _proof_fail("PROOF_JOIN_INVALID", "Plan, AcceptanceContract, Attempt, and PL08 verifier sets differ")
    if current_requirement is not None:
        if (
            current_requirement.get("dependency_classification") != "DEPENDENCY_EDGE_MEMBER"
            or current_requirement.get("change_id") != change_id
            or current_requirement.get("requirement_id") is None
            or current_requirement.get("dependency_semantic_digest") != dependency_digest
            or current_requirement.get("accepted_output_contract_ref") is None
            or current_requirement.get("produced_artifact_logical_ref") != proof["artifact_logical_ref"]
            or current_requirement.get("acceptance_contract_ref") != proof["acceptance_contract_ref"]
            or current_requirement.get("evaluation_scope_ref") != proof["evaluation_scope_ref"]
            or set(tuple((row["contract_id"], row["contract_version_or_ref"])) for row in current_requirement.get("required_verifier_contract_refs", [])) != set(required_pairs)
        ):
            raise _proof_fail("PROOF_REQUIREMENT_MISMATCH", "proof does not match the freshly resolved current requirement")

    def capture_wrappers(field: str, decoder: Any) -> list[tuple[dict[str, Any], CapturedJsonValueV1]]:
        if not isinstance(proof[field], list):
            raise _proof_fail("PROOF_SCHEMA_INVALID", f"{field} must be an ordered array")
        destination: list[tuple[dict[str, Any], CapturedJsonValueV1]] = []
        for row in proof[field]:
            mapping, wrapper = _wrapper_value(row, decoder, field)
            destination.append((mapping, wrapper))
        return destination

    # Keep the same structural owner order as PL08: evidence values and IDs,
    # then Finding values/applicability/IDs, then supersession values.
    evidence_wrappers = capture_wrappers("verifier_evidence_inputs", _decode_verifier_evidence)
    evidence_by_id: dict[str, tuple[dict[str, Any], CapturedJsonValueV1]] = {}
    applicable_evidence: list[dict[str, Any]] = []
    for evidence, wrapper in evidence_wrappers:
        if evidence["evidence_id"] in evidence_by_id:
            raise _proof_fail("PROOF_INPUT_INVALID", "duplicate VerifierEvidenceV1 evidence_id")
        evidence_by_id[evidence["evidence_id"]] = (evidence, wrapper)
        app = evidence["applicability"]
        # PL08 captures structurally valid but inapplicable inputs too. Keep
        # them in exact caller order; only the owner-defined applicability
        # predicate selects evidence that can support this proof.
        if (
            evidence["attempt_id"] == source_id
            and canonical_json(evidence["candidate_identity"]) == canonical_json(candidate)
            and app["attempt_id"] == source_id
            and canonical_json(app["candidate_identity"]) == canonical_json(candidate)
            and app["acceptance_contract_ref"] == proof["acceptance_contract_ref"]
            and app["evaluation_scope_ref"] == proof["evaluation_scope_ref"]
            and canonical_json(app["input_baseline_refs"]) == canonical_json(baselines)
        ):
            applicable_evidence.append(evidence)

    finding_wrappers = capture_wrappers("finding_inputs", _decode_finding)
    if any(finding["applicability"] is None for finding, _ in finding_wrappers):
        raise _proof_fail("PROOF_JOIN_INVALID", "captured FindingV1 applicability is required")
    finding_ids = [finding["finding_id"] for finding, _ in finding_wrappers]
    if len(set(finding_ids)) != len(finding_ids):
        raise _proof_fail("PROOF_INPUT_INVALID", "duplicate FindingV1 finding_id")

    supersession_wrappers = capture_wrappers("evidence_supersession_inputs", _decode_supersession)

    for pair in required_pairs:
        contract_row = next(row for row in contract_rows if (row["contract_id"], row["contract_version_or_ref"]) == pair)
        qualifying = [item for item in applicable_evidence if
            (item["verifier_contract_ref"], item["verifier_contract_version_or_ref"]) == pair and item["outcome"] == "PASS"]
        refs = {ref for item in qualifying for ref in item["evidence_refs"]}
        if not qualifying or not set(contract_row["required_evidence_refs"]).issubset(refs):
            raise _proof_fail("PROOF_JOIN_INVALID", "required verifier lacks exact PASS evidence/content refs")
    applicable_evidence_refs = {ref for item in applicable_evidence for ref in item["evidence_refs"]}
    if not set(evaluation["required_evidence_refs"]).issubset(applicable_evidence_refs):
        raise _proof_fail("PROOF_JOIN_INVALID", "TechnicalEvaluationV1 required evidence is absent from captured inputs")

    applicable_finding_ids: list[str] = []
    for finding, _ in finding_wrappers:
        app = finding["applicability"]
        if (
            app["attempt_id"] != source_id
            or canonical_json(app["candidate_identity"]) != canonical_json(candidate)
            or app["acceptance_contract_ref"] != proof["acceptance_contract_ref"]
            or app["evaluation_scope_ref"] != proof["evaluation_scope_ref"]
            or canonical_json(app["input_baseline_refs"]) != canonical_json(baselines)
        ):
            # Non-applicable findings are still captured. They may carry a
            # distinct applicability scope; only structurally valid refs are
            # needed here, matching the frozen PL08 list boundary.
            _decode_finding(finding)
        else:
            applicable_finding_ids.append(finding["finding_id"])
            if finding["acceptance_impact"] == "BLOCKING" and finding["disposition"] in {"OPEN", "REMEDIATION_REQUIRED"}:
                raise _proof_fail("PROOF_NOT_SATISFIED", "SATISFIED PL08 output conflicts with an applicable blocking Finding")
    if tuple(applicable_finding_ids) != tuple(evaluation["applicable_finding_refs"]):
        raise _proof_fail("PROOF_JOIN_INVALID", "TechnicalEvaluationV1 applicable Finding order does not match captured inputs")
    for relation, _ in supersession_wrappers:
        if relation["prior_evidence_ref"] == relation["successor_evidence_ref"]:
            raise _proof_fail("PROOF_JOIN_INVALID", "supersession self-reference is invalid")

    required_content_refs: list[str] = []
    for mapping, _ in evidence_wrappers:
        required_content_refs.extend(mapping["evidence_refs"])
    for mapping, _ in finding_wrappers:
        required_content_refs.extend(mapping["evidence_refs"])
    for mapping, _ in supersession_wrappers:
        required_content_refs.extend((mapping["prior_evidence_ref"], mapping["successor_evidence_ref"]))
    unique_refs = set(required_content_refs)
    if not isinstance(proof["evidence_ref_contents"], list):
        raise _proof_fail("EVIDENCE_CONTENT_COVERAGE_GAP", "evidence_ref_contents must be an array")
    content_by_ref: dict[str, dict[str, Any]] = {}
    content_refs_in_order: list[str] = []
    for raw_entry in proof["evidence_ref_contents"]:
        entry = _proof_mapping(raw_entry, {"evidence_ref", "content_identity", "content_digest"}, "evidence content entry")
        ref = _proof_string(entry["evidence_ref"], "evidence_ref")
        digest = _proof_digest(entry["content_digest"], "evidence content digest")
        if ref in content_by_ref:
            raise _proof_fail("EVIDENCE_CONTENT_CONFLICT", "each exact evidence ref must have one content entry")
        if entry["content_identity"] != "econtent_" + digest:
            raise _proof_fail("EVIDENCE_CONTENT_IDENTITY_MISMATCH", "evidence content identity must derive from its digest")
        content_by_ref[ref] = {"evidence_ref": ref, "content_identity": entry["content_identity"], "content_digest": digest}
        content_refs_in_order.append(ref)
    if set(content_by_ref) != unique_refs:
        raise _proof_fail("EVIDENCE_CONTENT_COVERAGE_GAP", "evidence content entries must exactly cover referenced content")
    if content_refs_in_order != sorted(unique_refs):
        raise _proof_fail("EVIDENCE_CONTENT_ORDER_INVALID", "evidence content entries must use exact-ref lexical order")
    class_a_refs = {
        ref
        for relation, _ in supersession_wrappers
        for ref in (relation["prior_evidence_ref"], relation["successor_evidence_ref"])
        if ref in evidence_by_id
    }
    for ref in class_a_refs:
        evidence_mapping, wrapper = evidence_by_id[ref]
        class_a_digest = _sha256(_proof_json_bytes(evidence_mapping))
        if (
            content_by_ref[ref]["content_digest"] != class_a_digest
            or content_by_ref[ref]["content_identity"] != "econtent_" + class_a_digest
            or wrapper.content_digest != class_a_digest
        ):
            raise _proof_fail("EVIDENCE_CONTENT_DIGEST_MISMATCH", "Class-A content does not bind the complete captured verifier mapping")

    if current_requirement is not None:
        for field in ("change_id", "dependency_semantic_digest"):
            if proof[field] != current_requirement[field]:
                raise _proof_fail("PROOF_REQUIREMENT_MISMATCH", f"proof {field} differs from current requirement")
        if proof["required_verifier_contract_refs"] != current_requirement["required_verifier_contract_refs"]:
            raise _proof_fail("PROOF_REQUIREMENT_MISMATCH", "proof required verifiers differ from current requirement order")

    preimage = {key: item for key, item in proof.items() if key not in {"proof_id", "proof_digest"}}
    digest = _sha256(_proof_json_bytes(preimage))
    _proof_digest(proof["proof_digest"], "proof_digest")
    if proof["proof_digest"] != digest or proof["proof_id"] != "dproof_" + digest:
        raise _proof_fail("PROOF_IDENTITY_MISMATCH", "proof ID/digest do not match the complete canonical preimage")
    # Make the order-stable normalized result explicit and prevent unknown
    # mappings from reaching persistence through an accepted partial object.
    return proof


def encode_dependency_acceptance_proof(proof: DependencyAcceptanceProofV1) -> bytes:
    """Encode one inert proof mapping as canonical JSON plus exactly one LF."""
    if not isinstance(proof, DependencyAcceptanceProofV1):
        raise _proof_fail("PROOF_INPUT_INVALID", "DependencyAcceptanceProofV1 is required")
    mapping = _validate_dependency_acceptance_proof(proof.to_mapping())
    return _proof_json_bytes(mapping) + b"\n"


def decode_dependency_acceptance_proof(raw: bytes) -> DependencyAcceptanceProofV1:
    """Strictly decode a canonical inert proof blob; existence grants no state."""
    if not isinstance(raw, bytes) or raw.startswith(b"\xef\xbb\xbf"):
        raise _proof_fail("PROOF_ENCODING_INVALID", "proof bytes require UTF-8 without BOM")
    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(
            text, object_pairs_hook=_unique_object,
            parse_constant=_reject_constant, parse_float=_parse_finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise _proof_fail("PROOF_ENCODING_INVALID", "proof JSON is malformed or has duplicate keys") from exc
    proof = DependencyAcceptanceProofV1.from_mapping(value)
    if encode_dependency_acceptance_proof(proof) != raw:
        raise _proof_fail("PROOF_ENCODING_NONCANONICAL", "proof bytes must be canonical JSON plus one LF")
    return proof


class DependencyProofCarrierError(ValueError):
    """A proof blob is malformed, conflicting, or not durably resolvable."""


def dependency_acceptance_proof_path(carrier_root: str | Path, proof: DependencyAcceptanceProofV1) -> Path:
    """Locate one proof by digest beneath Runtime's target-local carrier.

    The filename is retrieval metadata only. A Runtime CURRENT head remains
    the sole authority and must be installed under its V2 mutation lock.
    """
    if not isinstance(proof, DependencyAcceptanceProofV1):
        raise DependencyProofCarrierError("DependencyAcceptanceProofV1 is required")
    validated = DependencyAcceptanceProofV1.from_mapping(proof.to_mapping())
    return Path(carrier_root) / "dependency-admission" / "proofs" / f"{validated.proof_digest}.json"


def resolve_dependency_acceptance_proof_blob(
    carrier_root: str | Path, proof_id: str
) -> DependencyAcceptanceProofV1 | None:
    """Strictly resolve one immutable proof blob; existence remains inert."""
    if not isinstance(proof_id, str) or not re.fullmatch(r"dproof_[0-9a-f]{64}", proof_id):
        raise DependencyProofCarrierError("proof_id is malformed")
    base = Path(carrier_root)
    path = base / "dependency-admission" / "proofs" / f"{proof_id.removeprefix('dproof_')}.json"
    try:
        _guard_artifact_carrier_path(base, path)
    except DependencyProofError as exc:
        raise DependencyProofCarrierError(f"proof carrier path is unsafe: {exc}") from exc
    try:
        raw = _read_contained_regular_file(path, "dependency proof blob")
    except DependencyProofError as exc:
        if exc.code == "ARTIFACT_ROUTE_MISSING":
            return None
        raise DependencyProofCarrierError(f"proof carrier cannot be resolved: {exc}") from exc
    try:
        proof = decode_dependency_acceptance_proof(raw)
    except DependencyProofError as exc:
        raise DependencyProofCarrierError(f"proof carrier is corrupt: {exc}") from exc
    if proof.proof_id != proof_id:
        raise DependencyProofCarrierError("proof locator resolved to conflicting content")
    return proof


def publish_dependency_acceptance_proof_blob(
    carrier_root: str | Path, proof: DependencyAcceptanceProofV1
) -> tuple[str, DependencyAcceptanceProofV1]:
    """Durably publish one canonical proof without installing authority.

    Publication is target-local, immutable, no-clobber, and strictly reread.
    Identical bytes may be reused; conflicting content fails closed. Runtime
    must separately install the matching CURRENT head under its lock.
    """
    try:
        raw = encode_dependency_acceptance_proof(proof)
    except DependencyProofError as exc:
        raise DependencyProofCarrierError(f"proof is invalid: {exc}") from exc
    final = dependency_acceptance_proof_path(carrier_root, proof)
    base = Path(carrier_root)
    _guard_artifact_carrier_path(base, final)
    try:
        final.parent.mkdir(parents=True, exist_ok=True)
        if final.exists() or final.is_symlink():
            existing = _read_contained_regular_file(final, "dependency proof blob")
            if existing != raw:
                raise DependencyProofCarrierError("conflicting immutable proof bytes")
        else:
            staged: Path | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="wb", dir=final.parent, prefix=".dependency-proof-", suffix=".tmp", delete=False
                ) as handle:
                    staged = Path(handle.name)
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
                try:
                    os.link(staged, final)
                except FileExistsError:
                    pass
                staged.unlink(missing_ok=True)
                staged = None
            finally:
                if staged is not None:
                    staged.unlink(missing_ok=True)
        verified_raw = _read_contained_regular_file(final, "published dependency proof blob")
        verified = decode_dependency_acceptance_proof(verified_raw)
        if verified_raw != raw or verified.proof_id != proof.proof_id:
            raise DependencyProofCarrierError("published proof failed strict byte readback")
        _fsync_directory(final.parent)
        return verified.proof_id, verified
    except DependencyProofCarrierError:
        raise
    except (OSError, DependencyProofError) as exc:
        raise DependencyProofCarrierError("proof publication or strict readback failed") from exc


def build_dependency_admission(
    proof: DependencyAcceptanceProofV1,
    requirement: Mapping[str, Any],
    *,
    artifact_digest: str,
) -> dict[str, Any]:
    """Build the complete non-authorizing admission from freshly joined inputs.

    Runtime supplies the current requirement, proof, and exact artifact-byte
    digest while holding its one mutation lock. This pure constructor accepts
    no Attempt, caller ID, store, or lifecycle assertion; Runtime owns atomic
    attachment and strict readback of the resulting complete object.
    """
    try:
        current = DependencyAcceptanceProofV1.from_mapping(
            proof.to_mapping(), current_requirement=requirement
        ).to_mapping()
        contract = CapturedJsonValueV1.from_mapping(current["acceptance_contract"])
        _proof_digest(artifact_digest, "artifact_digest")
        semantic = {
            "schema_version": 2,
            "requirement_id": requirement["requirement_id"],
            "change_id": current["change_id"],
            "source_task_or_operation_id": "T-01",
            "source_attempt_id": f"{current['change_id']}/T-01/A1",
            "successor_task_or_operation_id": "T-02",
            "successor_attempt_id": f"{current['change_id']}/T-02/A1",
            "dependency_semantic_digest": requirement["dependency_semantic_digest"],
            "observed_result_id": current["observed_result_id"],
            "acceptance_proof_id": current["proof_id"],
            "acceptance_proof_digest": current["proof_digest"],
            "technical_evaluation_id": current["technical_evaluation_id"],
            "technical_evaluation_outcome": current["technical_evaluation_outcome"],
            "acceptance_contract_ref": current["acceptance_contract_ref"],
            "acceptance_contract_digest": contract.content_digest,
            "evaluation_scope_ref": current["evaluation_scope_ref"],
            "required_verifier_contract_refs": current["required_verifier_contract_refs"],
            "artifact_logical_ref": current["artifact_logical_ref"],
            "artifact_digest": artifact_digest,
            "required_successor_input_logical_ref": requirement["required_successor_input_logical_ref"],
            "eligible_outcome": "ELIGIBLE_FOR_CLAIM_CHECK",
        }
        admission_id = "dadm_" + _sha256(_proof_json_bytes(semantic))
        return {"schema_version": 2, "admission_id": admission_id, **{k: v for k, v in semantic.items() if k != "schema_version"}}
    except (KeyError, TypeError, DependencyProofError) as exc:
        raise _proof_fail("ADMISSION_JOIN_INVALID", "current proof and requirement cannot form an exact admission") from exc


def validate_dependency_admission(
    value: object,
    proof: DependencyAcceptanceProofV1,
    requirement: Mapping[str, Any],
    *,
    artifact_digest: str,
) -> None:
    """Validate an already-persisted admission against all current T-06 joins.

    This pure validator derives the only acceptable 22-field mapping from the
    strict proof, current requirement, and independently hashed artifact
    bytes. It grants no authority and does not create, attach, repair, or
    persist an admission; Runtime remains the sole lifecycle mutation owner.
    """
    if not isinstance(proof, DependencyAcceptanceProofV1):
        raise _proof_fail("ADMISSION_JOIN_INVALID", "a strict DependencyAcceptanceProofV1 is required")
    if not isinstance(value, Mapping):
        raise _proof_fail("ADMISSION_JOIN_INVALID", "an existing complete admission mapping is required")
    try:
        expected = build_dependency_admission(proof, requirement, artifact_digest=artifact_digest)
        def plain_json(item: Any) -> Any:
            if isinstance(item, Mapping):
                return {key: plain_json(child) for key, child in item.items()}
            if isinstance(item, (list, tuple)):
                return [plain_json(child) for child in item]
            return item

        normalized = plain_json(value)
        if (
            set(value) != set(expected)
            or normalized != expected
            or _proof_json_bytes(normalized) != _proof_json_bytes(expected)
        ):
            raise _proof_fail(
                "ADMISSION_JOIN_INVALID",
                "existing admission does not exactly join the current requirement, proof, and artifact bytes",
            )
    except DependencyProofError:
        raise
    except (KeyError, TypeError, ValueError) as exc:
        raise _proof_fail("ADMISSION_JOIN_INVALID", "existing admission cannot be joined to current inputs") from exc


@dataclass(frozen=True, slots=True)
class _DependencyArtifactCarrierV1:
    """Immutable inert binding of the semantic artifact pair to its digest."""

    artifact_logical_ref: str
    artifact_digest: str

    def to_mapping(self) -> dict[str, str]:
        return {"artifact_logical_ref": self.artifact_logical_ref, "artifact_digest": self.artifact_digest}


_EVIDENCE_CONTENT_KEYS = frozenset({
    "schema_version", "evidence_ref", "content_identity", "content_digest", "content_base64",
})


@dataclass(frozen=True, slots=True)
class EvidenceContentCarrierV1:
    """Immutable target-local binding of one opaque evidence ref to exact bytes.

    The persisted mapping has exactly five fields. Its semantic content identity
    and digest are derived from the decoded raw bytes; the ref-derived filename
    is only a retrieval locator. Publication is no-clobber and verified by a
    strict reread, and carrier existence grants no lifecycle authority.
    """

    schema_version: int
    evidence_ref: str
    content_identity: str
    content_digest: str
    content_base64: str

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "evidence_ref": self.evidence_ref,
            "content_identity": self.content_identity,
            "content_digest": self.content_digest,
            "content_base64": self.content_base64,
        }

    @property
    def exact_raw_bytes(self) -> bytes:
        return _evidence_content_raw_bytes(self)


def _evidence_content_raw_bytes(carrier: EvidenceContentCarrierV1) -> bytes:
    if not isinstance(carrier, EvidenceContentCarrierV1):
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "EvidenceContentCarrierV1 is required")
    value = carrier.to_mapping()
    if set(value) != _EVIDENCE_CONTENT_KEYS:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence content carrier must have exactly five fields")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence content schema_version must be integer 1")
    ref = value["evidence_ref"]
    if not isinstance(ref, str) or not ref or ref != ref.strip():
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence_ref must be a non-empty exact string")
    try:
        ref.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence_ref must be valid UTF-8 text") from exc
    digest = value["content_digest"]
    if not isinstance(digest, str) or not _SHA256_RE.fullmatch(digest):
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "content_digest must be lowercase SHA-256")
    identity = value["content_identity"]
    if not isinstance(identity, str) or identity != "econtent_" + digest:
        raise _proof_fail("EVIDENCE_CONTENT_IDENTITY_MISMATCH", "content_identity must derive from content_digest")
    encoded = value["content_base64"]
    if not isinstance(encoded, str):
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "content_base64 must be a string")
    try:
        encoded_bytes = encoded.encode("ascii", errors="strict")
        decoded = base64.b64decode(encoded_bytes, validate=True)
    except (UnicodeEncodeError, binascii.Error, ValueError) as exc:
        raise _proof_fail("EVIDENCE_CONTENT_BASE64_INVALID", "content_base64 must use canonical standard Base64") from exc
    if base64.b64encode(decoded) != encoded_bytes:
        raise _proof_fail("EVIDENCE_CONTENT_BASE64_INVALID", "content_base64 is not canonical standard Base64")
    if _sha256(decoded) != digest:
        raise _proof_fail("EVIDENCE_CONTENT_DIGEST_MISMATCH", "content_digest does not hash the exact decoded bytes")
    return decoded


def _encode_evidence_content_carrier(carrier: EvidenceContentCarrierV1) -> bytes:
    _evidence_content_raw_bytes(carrier)
    return _proof_json_bytes(carrier.to_mapping()) + b"\n"


def _decode_evidence_content_carrier(raw: bytes) -> EvidenceContentCarrierV1:
    """Strictly decode the exact five-key canonical carrier and raw-byte joins.

    Duplicate members, wrong primitive types, noncanonical Base64 or JSON,
    digest/identity mismatches, and any encoding other than compact sorted
    UTF-8 JSON plus one LF are rejected without repair.
    """
    if not isinstance(raw, bytes) or raw.startswith(b"\xef\xbb\xbf"):
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "carrier requires UTF-8 without BOM")
    try:
        value = json.loads(
            raw.decode("utf-8", errors="strict"),
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
            parse_float=_parse_finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "carrier JSON is malformed or has duplicate members") from exc
    if not isinstance(value, Mapping) or set(value) != _EVIDENCE_CONTENT_KEYS:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "carrier must have exactly the five required fields")
    carrier = EvidenceContentCarrierV1(
        value["schema_version"], value["evidence_ref"], value["content_identity"],
        value["content_digest"], value["content_base64"],
    )
    _evidence_content_raw_bytes(carrier)
    if _encode_evidence_content_carrier(carrier) != raw:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "carrier bytes are not canonical compact JSON plus one LF")
    return carrier


def _evidence_content_carrier_from_bytes(evidence_ref: str, exact_raw_bytes: bytes) -> EvidenceContentCarrierV1:
    if not isinstance(evidence_ref, str) or not evidence_ref or evidence_ref != evidence_ref.strip():
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence_ref must be a non-empty exact string")
    try:
        evidence_ref.encode("utf-8", errors="strict")
    except UnicodeEncodeError as exc:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence_ref must be valid UTF-8 text") from exc
    if not isinstance(exact_raw_bytes, bytes):
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "exact_raw_bytes must be bytes")
    digest = _sha256(exact_raw_bytes)
    return EvidenceContentCarrierV1(
        1, evidence_ref, "econtent_" + digest, digest,
        base64.b64encode(exact_raw_bytes).decode("ascii"),
    )


def _evidence_content_carrier_path(planning_root: str | Path, evidence_ref: str) -> Path:
    """Return the sole retrieval path for the exact opaque UTF-8 evidence ref.

    The locator is SHA-256 of the unnormalized exact ref bytes. The resulting
    path is effective_planning_root/changes/active/.planning-lite/
    dependency-admission/evidence-content-v1/<locator>.json; it is not content
    identity and the ref is never joined to or interpreted as a filesystem path.
    """
    if not isinstance(evidence_ref, str) or not evidence_ref or evidence_ref != evidence_ref.strip():
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence_ref must be a non-empty exact string")
    try:
        locator = _sha256(evidence_ref.encode("utf-8", errors="strict"))
    except UnicodeEncodeError as exc:
        raise _proof_fail("EVIDENCE_CONTENT_INVALID", "evidence_ref must be valid UTF-8 text") from exc
    return (
        Path(planning_root) / "changes" / "active" / ".planning-lite"
        / "dependency-admission" / "evidence-content-v1" / f"{locator}.json"
    )


def _guard_contained_carrier_path(
    carrier_root: str | Path, path: Path, *, error_code: str, where: str
) -> None:
    """Reject symlink aliases and non-directory parents below one carrier root."""
    root = Path(carrier_root)
    try:
        root_info = root.lstat()
    except FileNotFoundError:
        root_info = None
    except OSError as exc:
        raise _proof_fail(error_code, f"cannot inspect {where} root") from exc
    if root_info is not None and (stat.S_ISLNK(root_info.st_mode) or not stat.S_ISDIR(root_info.st_mode)):
        raise _proof_fail(error_code, f"{where} root must be a real directory")
    try:
        relative = path.relative_to(root)
    except ValueError as exc:
        raise _proof_fail(error_code, f"{where} escapes its selected root") from exc
    cursor = root
    for index, part in enumerate(relative.parts):
        cursor = cursor / part
        try:
            info = cursor.lstat()
        except FileNotFoundError:
            return
        except OSError as exc:
            raise _proof_fail(error_code, f"cannot inspect {where} path") from exc
        last = index == len(relative.parts) - 1
        if stat.S_ISLNK(info.st_mode):
            raise _proof_fail(error_code, f"{where} path contains a symlink alias")
        if last:
            if not stat.S_ISREG(info.st_mode):
                raise _proof_fail(error_code, f"{where} terminal object is not a regular file")
        elif not stat.S_ISDIR(info.st_mode):
            raise _proof_fail(error_code, f"{where} parent is not a directory")


def _guard_artifact_carrier_path(carrier_root: str | Path, path: Path) -> None:
    _guard_contained_carrier_path(
        carrier_root, path, error_code="ARTIFACT_CARRIER_UNSAFE", where="artifact carrier"
    )


def _dependency_artifact_carrier_ref(carrier: _DependencyArtifactCarrierV1) -> str:
    """Return a private content-derived locator for the immutable pair carrier."""
    if not isinstance(carrier, _DependencyArtifactCarrierV1):
        raise _proof_fail("ARTIFACT_CARRIER_INVALID", "artifact identity carrier is required")
    mapping = carrier.to_mapping()
    _proof_string(mapping["artifact_logical_ref"], "artifact_logical_ref")
    _proof_digest(mapping["artifact_digest"], "artifact_digest")
    return "artifact-carrier:" + _sha256(_proof_json_bytes(mapping))


def _encode_artifact_carrier(carrier: _DependencyArtifactCarrierV1) -> bytes:
    return _proof_json_bytes(carrier.to_mapping()) + b"\n"


def _decode_artifact_carrier(raw: bytes) -> _DependencyArtifactCarrierV1:
    if not isinstance(raw, bytes) or raw.startswith(b"\xef\xbb\xbf"):
        raise _proof_fail("ARTIFACT_CARRIER_INVALID", "artifact carrier requires UTF-8 without BOM")
    try:
        value = json.loads(raw.decode("utf-8", errors="strict"), object_pairs_hook=_unique_object, parse_constant=_reject_constant)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise _proof_fail("ARTIFACT_CARRIER_INVALID", "artifact carrier JSON is invalid") from exc
    item = _proof_mapping(value, {"artifact_logical_ref", "artifact_digest"}, "artifact identity carrier")
    carrier = _DependencyArtifactCarrierV1(
        _proof_string(item["artifact_logical_ref"], "artifact_logical_ref"),
        _proof_digest(item["artifact_digest"], "artifact_digest"),
    )
    if _encode_artifact_carrier(carrier) != raw:
        raise _proof_fail("ARTIFACT_CARRIER_INVALID", "artifact carrier bytes are not canonical")
    return carrier


def _read_contained_regular_file(path: Path, where: str) -> bytes:
    try:
        info = path.lstat()
    except FileNotFoundError as exc:
        raise _proof_fail("ARTIFACT_ROUTE_MISSING", f"{where} does not exist") from exc
    except OSError as exc:
        raise _proof_fail("ARTIFACT_ROUTE_UNSAFE", f"cannot inspect {where}") from exc
    if not stat.S_ISREG(info.st_mode):
        raise _proof_fail("ARTIFACT_ROUTE_UNSAFE", f"{where} is not a regular file")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        fd = os.open(path, flags)
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            if not stat.S_ISREG(opened.st_mode):
                raise _proof_fail("ARTIFACT_ROUTE_UNSAFE", f"{where} changed to a non-regular object")
            data = handle.read()
    except DependencyProofError:
        raise
    except OSError as exc:
        raise _proof_fail("ARTIFACT_ROUTE_READ_FAILED", f"cannot read exact bytes from {where}") from exc
    return data


def _artifact_carrier_path(carrier_root: str | Path, carrier: _DependencyArtifactCarrierV1) -> Path:
    ref = _dependency_artifact_carrier_ref(carrier).removeprefix("artifact-carrier:")
    return Path(carrier_root) / "dependency-admission" / "artifacts" / f"{ref}.json"


def _resolve_dependency_artifact_carrier(
    carrier_root: str | Path, carrier: _DependencyArtifactCarrierV1
) -> tuple[str, _DependencyArtifactCarrierV1] | None:
    """Strictly reread the exact immutable semantic artifact carrier."""
    path = _artifact_carrier_path(carrier_root, carrier)
    _guard_artifact_carrier_path(carrier_root, path)
    try:
        raw = _read_contained_regular_file(path, "artifact carrier")
    except DependencyProofError as exc:
        if exc.code == "ARTIFACT_ROUTE_MISSING":
            return None
        raise
    stored = _decode_artifact_carrier(raw)
    if stored != carrier:
        raise _proof_fail("ARTIFACT_CARRIER_CONFLICT", "artifact carrier locator resolved to conflicting content")
    return _dependency_artifact_carrier_ref(stored), stored


def _publish_dependency_artifact_carrier(
    carrier_root: str | Path, carrier: _DependencyArtifactCarrierV1
) -> tuple[str, _DependencyArtifactCarrierV1]:
    """No-clobber publish and strict reread under the existing private carrier protocol.

    Staging is same-directory beneath the validated effective planning root;
    an existing object is accepted only after byte-exact decoding. There is no
    overwrite, repair, registry lookup, or authority inferred from existence.
    """
    raw = _encode_artifact_carrier(carrier)
    final = _artifact_carrier_path(carrier_root, carrier)
    parent = final.parent
    base = Path(carrier_root)
    _guard_artifact_carrier_path(base, final)
    try:
        relative = parent.relative_to(base)
    except ValueError as exc:
        raise _proof_fail("ARTIFACT_CARRIER_UNSAFE", "carrier path escapes its effective-root boundary") from exc
    cursor = base
    if cursor.exists():
        info = cursor.lstat()
        if not stat.S_ISDIR(info.st_mode):
            raise _proof_fail("ARTIFACT_CARRIER_UNSAFE", "carrier root is not a regular directory")
    for part in relative.parts:
        cursor = cursor / part
        try:
            info = cursor.lstat()
        except FileNotFoundError:
            continue
        if not stat.S_ISDIR(info.st_mode):
            raise _proof_fail("ARTIFACT_CARRIER_UNSAFE", "carrier parent contains a symlink or non-directory")
    try:
        parent.mkdir(parents=True, exist_ok=True)
        if final.exists() or final.is_symlink():
            existing = _read_contained_regular_file(final, "artifact carrier")
            if existing != raw or _decode_artifact_carrier(existing) != carrier:
                raise _proof_fail("ARTIFACT_CARRIER_CONFLICT", "conflicting immutable artifact carrier")
        else:
            staged: Path | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="wb", dir=parent, prefix=".artifact-carrier-", suffix=".tmp", delete=False
                ) as handle:
                    staged = Path(handle.name)
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
                try:
                    os.link(staged, final)
                except FileExistsError:
                    pass
                staged.unlink(missing_ok=True)
                staged = None
            finally:
                if staged is not None:
                    staged.unlink(missing_ok=True)
        verified = _read_contained_regular_file(final, "published artifact carrier")
        stored = _decode_artifact_carrier(verified)
        if verified != raw or stored != carrier:
            raise _proof_fail("ARTIFACT_CARRIER_CONFLICT", "published artifact carrier failed byte verification")
        _fsync_directory(parent)
        return _dependency_artifact_carrier_ref(stored), stored
    except DependencyProofError:
        raise
    except OSError as exc:
        raise _proof_fail("ARTIFACT_CARRIER_WRITE_FAILED", "immutable artifact carrier publication failed") from exc


def _evidence_content_location(product_root: str | Path, evidence_ref: str) -> tuple[Path, Path]:
    try:
        _, _, planning_root = _effective_planning_root(product_root)
    except DependencyAdmissionError as exc:
        raise _proof_fail("EVIDENCE_CONTENT_ROOT_INVALID", "cannot resolve the effective planning root") from exc
    return planning_root, _evidence_content_carrier_path(planning_root, evidence_ref)


def _read_evidence_content_carrier_file(path: Path) -> bytes:
    try:
        return _read_contained_regular_file(path, "evidence-content carrier")
    except DependencyProofError as exc:
        code = {
            "ARTIFACT_ROUTE_MISSING": "EVIDENCE_CONTENT_MISSING",
            "ARTIFACT_ROUTE_UNSAFE": "EVIDENCE_CONTENT_UNSAFE",
            "ARTIFACT_ROUTE_READ_FAILED": "EVIDENCE_CONTENT_READ_FAILED",
        }.get(exc.code, "EVIDENCE_CONTENT_READ_FAILED")
        raise _proof_fail(code, str(exc)) from exc


def resolve_evidence_content(product_root: str | Path, evidence_ref: str) -> EvidenceContentCarrierV1:
    """Resolve one opaque ref from its sole effective-root durable carrier.

    The exact UTF-8 ref determines only the filename; it is never interpreted
    as a path or content identity. Resolution performs path containment and
    symlink checks, strict canonical decoding, and independent ref, raw-byte,
    digest, and identity verification on every call, so a fresh process needs
    no cache or registry. A carrier is inert and grants no lifecycle authority.
    """
    planning_root, path = _evidence_content_location(product_root, evidence_ref)
    _guard_contained_carrier_path(
        planning_root, path, error_code="EVIDENCE_CONTENT_UNSAFE", where="evidence-content carrier"
    )
    carrier = _decode_evidence_content_carrier(_read_evidence_content_carrier_file(path))
    if carrier.evidence_ref != evidence_ref:
        raise _proof_fail("EVIDENCE_CONTENT_REF_MISMATCH", "carrier ref does not match its exact requested locator")
    return carrier


def _ensure_evidence_content_parent(planning_root: Path, parent: Path) -> None:
    """Create only the derived carrier parents after checking each path owner."""
    try:
        relative = parent.relative_to(planning_root)
    except ValueError as exc:
        raise _proof_fail("EVIDENCE_CONTENT_UNSAFE", "carrier parent escapes the effective planning root") from exc
    try:
        root_info = planning_root.lstat()
    except OSError as exc:
        raise _proof_fail("EVIDENCE_CONTENT_UNSAFE", "cannot inspect effective planning root") from exc
    if stat.S_ISLNK(root_info.st_mode) or not stat.S_ISDIR(root_info.st_mode):
        raise _proof_fail("EVIDENCE_CONTENT_UNSAFE", "effective planning root is not a real directory")
    cursor = planning_root
    for part in relative.parts:
        cursor = cursor / part
        try:
            info = cursor.lstat()
        except FileNotFoundError:
            try:
                cursor.mkdir()
            except FileExistsError:
                pass
            except OSError as exc:
                raise _proof_fail("EVIDENCE_CONTENT_WRITE_FAILED", "cannot create canonical carrier parent") from exc
            try:
                info = cursor.lstat()
            except OSError as exc:
                raise _proof_fail("EVIDENCE_CONTENT_UNSAFE", "cannot verify created carrier parent") from exc
        except OSError as exc:
            raise _proof_fail("EVIDENCE_CONTENT_UNSAFE", "cannot inspect carrier parent") from exc
        if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
            raise _proof_fail("EVIDENCE_CONTENT_UNSAFE", "carrier parent contains a symlink or non-directory")


def publish_evidence_content(
    product_root: str | Path, evidence_ref: str, exact_raw_bytes: bytes
) -> EvidenceContentCarrierV1:
    """Publish exact evidence bytes at the one immutable effective-root route.

    The caller supplies only product_root, the opaque exact evidence_ref, and
    raw bytes. This owner derives the target-local locator, SHA-256 digest,
    econtent identity, and canonical Base64 carrier. Same-ref/same-byte
    publication is verified idempotent reuse; different bytes or malformed
    existing state fail closed without overwrite or repair. Staging is flushed
    in the destination directory, linked without clobbering, and followed by a
    strict reread. No alternate route, registry, OS Temp, or lifecycle
    authority is introduced; the returned carrier is an inert verified value.
    """
    carrier = _evidence_content_carrier_from_bytes(evidence_ref, exact_raw_bytes)
    raw = _encode_evidence_content_carrier(carrier)
    planning_root, final = _evidence_content_location(product_root, evidence_ref)
    parent = final.parent
    _ensure_evidence_content_parent(planning_root, parent)
    _guard_contained_carrier_path(
        planning_root, final, error_code="EVIDENCE_CONTENT_UNSAFE", where="evidence-content carrier"
    )
    try:
        if final.exists():
            existing_raw = _read_evidence_content_carrier_file(final)
            existing = _decode_evidence_content_carrier(existing_raw)
            if existing.evidence_ref != evidence_ref or existing_raw != raw or existing != carrier:
                raise _proof_fail("EVIDENCE_CONTENT_CONFLICT", "same evidence ref already has different immutable bytes")
        else:
            staged: Path | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="wb", dir=parent, prefix=".evidence-content-", suffix=".tmp", delete=False
                ) as handle:
                    staged = Path(handle.name)
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
                try:
                    os.link(staged, final)
                except FileExistsError:
                    pass
                staged.unlink(missing_ok=True)
                staged = None
            finally:
                if staged is not None:
                    staged.unlink(missing_ok=True)
        _guard_contained_carrier_path(
            planning_root, final, error_code="EVIDENCE_CONTENT_UNSAFE", where="evidence-content carrier"
        )
        verified_raw = _read_evidence_content_carrier_file(final)
        verified = _decode_evidence_content_carrier(verified_raw)
        if verified_raw != raw or verified != carrier or verified.evidence_ref != evidence_ref:
            raise _proof_fail("EVIDENCE_CONTENT_CONFLICT", "published carrier failed exact reread verification")
        _fsync_directory(parent)
        return verified
    except DependencyProofError:
        raise
    except OSError as exc:
        raise _proof_fail("EVIDENCE_CONTENT_WRITE_FAILED", "immutable evidence-content publication failed") from exc


def capture_dependency_acceptance_proof(
    product_root: str | Path,
    *,
    observed_result: Any,
    attempt_evaluation_input: Mapping[str, Any],
    acceptance_contract: Any,
    verifier_evidence_inputs: Any,
    evidence_supersession_inputs: Any,
    finding_inputs: Any,
    technical_evaluation: Any,
) -> DependencyAcceptanceProofV1:
    """Capture exact current T-01/A1 PL08 evidence and route bytes into an inert proof.

    The sole product argument is ``product_root``. Current requirement and
    route are freshly derived by workspace; this API accepts neither a path,
    requirement, route key, artifact bytes, nor caller evidence-content rows.
    It snapshots complete typed PL08 owner mappings without reevaluating them
    and preserves all three invocation orders. This owner derives Class-A
    captured-mapping bytes and resolves every Class-B ref through the durable
    target-local EvidenceContentCarrierV1, compares overlap bytes, then sorts
    only the exact-ref evidence-content rows. Artifact bytes are read raw from
    the contained current route and independently hashed; its private carrier
    remains separate. Missing, changed, conflicting or unsafe route/carrier
    state fails closed. The returned proof blob is inert: it installs no head,
    admission, Attempt state, or claim authority, and physical locators are not
    proof identity.
    """
    from .workspace import DependencyArtifactOutputRouteV1, resolve_dependency_artifact_output_route

    try:
        route = resolve_dependency_artifact_output_route(product_root)
    except Exception as exc:
        raise _proof_fail("ARTIFACT_ROUTE_UNRESOLVED", "fresh current workspace route resolution failed") from exc
    if not isinstance(route, DependencyArtifactOutputRouteV1):
        raise _proof_fail("ARTIFACT_ROUTE_UNRESOLVED", "workspace did not return its canonical route owner value")
    requirement_resolution = resolve_dependency(route.product_root, "T-02")
    requirement = requirement_resolution.requirement
    _validate_requirement(requirement, route.product_root)
    if (
        requirement_resolution.change_id != route.key.change_id
        or requirement["source_attempt_id"] != route.key.source_attempt_id
        or requirement["requirement_id"] != route.key.requirement_id
        or requirement["dependency_semantic_digest"] != route.key.dependency_semantic_digest
        or requirement["accepted_output_contract_ref"] != route.key.accepted_output_contract_ref
        or requirement["produced_artifact_logical_ref"] != route.key.artifact_logical_ref
    ):
        raise _proof_fail("PROOF_REQUIREMENT_MISMATCH", "route and fresh requirement derivations disagree")
    artifact_bytes = _read_contained_regular_file(route.path, "canonical artifact route")
    artifact_digest = _sha256(artifact_bytes)
    artifact_ref = route.key.artifact_logical_ref

    observed_mapping = _owner_mapping(observed_result, _pl08.ObservedResultV1, _decode_observed_result, "ObservedResultV1")
    contract_mapping = _owner_mapping(acceptance_contract, _pl08.AcceptanceContractV1, _decode_acceptance_contract, "AcceptanceContractV1")
    evaluation_mapping = _owner_mapping(technical_evaluation, _pl08.TechnicalEvaluationV1, _decode_technical_evaluation, "TechnicalEvaluationV1")
    if not isinstance(attempt_evaluation_input, Mapping):
        raise _proof_fail("PROOF_INPUT_INVALID", "attempt_evaluation_input must be the exact PL08 mapping")
    input_mapping = dict(attempt_evaluation_input)

    def ordered_wrappers(values: Any, expected: type, decoder: Any, where: str) -> list[dict[str, Any]]:
        if not isinstance(values, (tuple, list)):
            raise _proof_fail("PROOF_INPUT_INVALID", f"{where} must preserve the PL08 invocation array")
        return [_capture_wrapper(value, expected, decoder, where) for value in values]

    verifier_wrappers = ordered_wrappers(verifier_evidence_inputs, _pl08.VerifierEvidenceV1, _decode_verifier_evidence, "VerifierEvidenceV1")
    supersession_wrappers = ordered_wrappers(evidence_supersession_inputs, _pl08.EvidenceSupersessionV1, _decode_supersession, "EvidenceSupersessionV1")
    finding_wrappers = ordered_wrappers(finding_inputs, _pl08.FindingV1, _decode_finding, "FindingV1")

    verifier_values = [wrapper["value"] for wrapper in verifier_wrappers]
    finding_values = [wrapper["value"] for wrapper in finding_wrappers]
    supersession_values = [wrapper["value"] for wrapper in supersession_wrappers]
    evidence_by_id: dict[str, dict[str, Any]] = {}
    for evidence in verifier_values:
        evidence_id = _proof_string(evidence["evidence_id"], "VerifierEvidenceV1.evidence_id")
        if evidence_id in evidence_by_id:
            raise _proof_fail("PROOF_INPUT_INVALID", "duplicate VerifierEvidenceV1 evidence_id")
        evidence_by_id[evidence_id] = evidence

    required_content_refs: set[str] = set()
    class_b_refs: set[str] = set()
    for evidence in verifier_values:
        for ref in evidence["evidence_refs"]:
            exact_ref = _proof_string(ref, "VerifierEvidenceV1.evidence_refs member")
            required_content_refs.add(exact_ref)
            class_b_refs.add(exact_ref)
    for finding in finding_values:
        for ref in finding["evidence_refs"]:
            exact_ref = _proof_string(ref, "FindingV1.evidence_refs member")
            required_content_refs.add(exact_ref)
            class_b_refs.add(exact_ref)

    class_a_bytes: dict[str, bytes] = {}
    for relation in supersession_values:
        for ref in (relation["prior_evidence_ref"], relation["successor_evidence_ref"]):
            exact_ref = _proof_string(ref, "EvidenceSupersessionV1 endpoint")
            required_content_refs.add(exact_ref)
            if exact_ref in evidence_by_id:
                class_a_bytes[exact_ref] = _proof_json_bytes(evidence_by_id[exact_ref])
            else:
                class_b_refs.add(exact_ref)

    content_entries: list[dict[str, str]] = []
    for exact_ref in sorted(required_content_refs):
        class_a_content = class_a_bytes.get(exact_ref)
        if class_a_content is not None and exact_ref not in class_b_refs:
            content_bytes = class_a_content
        else:
            carrier = resolve_evidence_content(product_root, exact_ref)
            content_bytes = carrier.exact_raw_bytes
            if exact_ref in class_a_bytes and content_bytes != class_a_bytes[exact_ref]:
                raise _proof_fail("EVIDENCE_CONTENT_OVERLAP_MISMATCH", "Class-A and Class-B bytes differ for the same exact ref")
            if carrier.content_digest != _sha256(content_bytes):
                raise _proof_fail("EVIDENCE_CONTENT_DIGEST_MISMATCH", "resolved carrier digest does not match its exact bytes")
        digest = _sha256(content_bytes)
        content_entries.append({
            "evidence_ref": exact_ref,
            "content_identity": "econtent_" + digest,
            "content_digest": digest,
        })

    # Verify every identity and wrapper before writing the inert carrier.
    shell = {
        "schema_version": 1,
        "proof_id": "dproof_" + "0" * 64,
        "proof_digest": "0" * 64,
        "change_id": requirement["change_id"],
        "source_task_or_operation_id": "T-01",
        "source_attempt_id": requirement["source_attempt_id"],
        "successor_task_or_operation_id": "T-02",
        "successor_attempt_id": requirement["successor_attempt_id"],
        "dependency_semantic_digest": requirement["dependency_semantic_digest"],
        "observed_result_id": observed_mapping["result_id"],
        "observed_result_content_digest": _sha256(_proof_json_bytes(observed_mapping)),
        "observed_result": CapturedJsonValueV1.from_value(observed_mapping).to_mapping(),
        "attempt_evaluation_input": input_mapping,
        "acceptance_contract_ref": requirement["acceptance_contract_ref"],
        "acceptance_contract": CapturedJsonValueV1.from_value(contract_mapping).to_mapping(),
        "evaluation_scope_ref": requirement["evaluation_scope_ref"],
        "required_verifier_contract_refs": requirement["required_verifier_contract_refs"],
        "verifier_evidence_inputs": verifier_wrappers,
        "evidence_ref_contents": content_entries,
        "evidence_supersession_inputs": supersession_wrappers,
        "finding_inputs": finding_wrappers,
        "technical_evaluation_id": evaluation_mapping["evaluation_id"],
        "technical_evaluation_outcome": evaluation_mapping["outcome"],
        "technical_evaluation": CapturedJsonValueV1.from_value(evaluation_mapping).to_mapping(),
        "artifact_logical_ref": artifact_ref,
        "artifact_digest": artifact_digest,
    }
    # Preflight joins using the derived artifact identity; placeholder proof
    # identity is replaced after all fields pass structural validation.
    preimage = {key: value for key, value in shell.items() if key not in {"proof_id", "proof_digest"}}
    proof_digest = _sha256(_proof_json_bytes(preimage))
    shell["proof_digest"] = proof_digest
    shell["proof_id"] = "dproof_" + proof_digest
    validated = _validate_dependency_acceptance_proof(shell, current_requirement=requirement)

    carrier = _DependencyArtifactCarrierV1(artifact_ref, artifact_digest)
    carrier_root = route.effective_planning_root / "changes" / "active" / ".planning-lite"
    carrier_ref, stored_carrier = _publish_dependency_artifact_carrier(carrier_root, carrier)
    if _resolve_dependency_artifact_carrier(carrier_root, carrier) != (carrier_ref, stored_carrier):
        raise _proof_fail("ARTIFACT_CARRIER_READBACK_FAILED", "immutable artifact carrier strict reread failed")
    # Re-derive after carrier publication and rehash route bytes. A changed
    # requirement/root or artifact cannot be bound by stale pre-carrier state.
    current_route = resolve_dependency_artifact_output_route(route.product_root)
    if current_route.key != route.key or current_route.path != route.path:
        raise _proof_fail("PROOF_REQUIREMENT_MISMATCH", "current requirement or route changed during capture")
    if _sha256(_read_contained_regular_file(current_route.path, "canonical artifact route")) != artifact_digest:
        raise _proof_fail("ARTIFACT_BYTES_CHANGED", "canonical artifact bytes changed during capture")
    return DependencyAcceptanceProofV1.from_mapping(validated, current_requirement=requirement)
_CANCELLATION_KEYS = frozenset(
    {"schema_version", "change_id", "source_task_id", "target_task_id", "observed_status"}
)


def _validate_cancellation_tombstone(value: Any) -> CancellationTombstoneV1:
    if not isinstance(value, dict) or set(value) != _CANCELLATION_KEYS:
        raise CancellationCarrierError("CancellationTombstoneV1 has an incorrect key set")
    version = value["schema_version"]
    if type(version) is not int or version != 1:
        raise CancellationCarrierError("CancellationTombstoneV1 schema_version must be integer 1")
    change_id = value["change_id"]
    if not isinstance(change_id, str) or not _CHANGE_ID_RE.fullmatch(change_id):
        raise CancellationCarrierError("CancellationTombstoneV1 change_id is invalid")
    if value["source_task_id"] != "T-01" or value["target_task_id"] != "T-02":
        raise CancellationCarrierError("CancellationTombstoneV1 must bind the fixed T-01 -> T-02 edge")
    if value["observed_status"] != "Cancelled":
        raise CancellationCarrierError("CancellationTombstoneV1 observed_status must be Cancelled")
    return CancellationTombstoneV1(change_id)


def encode_cancellation_tombstone(record: CancellationTombstoneV1) -> bytes:
    """Encode the exact D5 tombstone as canonical UTF-8 JSON with one LF."""
    if not isinstance(record, CancellationTombstoneV1):
        raise CancellationCarrierError("CancellationTombstoneV1 is required")
    validated = _validate_cancellation_tombstone(record.to_mapping())
    return (canonical_json(validated.to_mapping()) + "\n").encode("utf-8", errors="strict")


def decode_cancellation_tombstone(raw: bytes) -> CancellationTombstoneV1:
    """Strictly decode exact canonical D5 bytes, rejecting duplicates and drift."""
    if not isinstance(raw, bytes) or raw.startswith(b"\xef\xbb\xbf"):
        raise CancellationCarrierError("CancellationTombstoneV1 requires UTF-8 bytes without a BOM")
    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
            parse_float=_parse_finite_float,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise CancellationCarrierError(f"CancellationTombstoneV1 JSON is invalid: {exc}") from exc
    record = _validate_cancellation_tombstone(value)
    if encode_cancellation_tombstone(record) != raw:
        raise CancellationCarrierError("CancellationTombstoneV1 bytes are not canonical with one LF")
    return record


def cancellation_tombstone_ref(record: CancellationTombstoneV1) -> str:
    """Return the stable cancellation identity from canonical JSON without LF."""
    if not isinstance(record, CancellationTombstoneV1):
        raise CancellationCarrierError("CancellationTombstoneV1 is required")
    validated = _validate_cancellation_tombstone(record.to_mapping())
    digest = _sha256(canonical_json(validated.to_mapping()).encode("utf-8", errors="strict"))
    return f"cancellation:{digest}"


def cancellation_tombstone_path(carrier_root: str | Path, record: CancellationTombstoneV1) -> Path:
    """Map one deterministic ref into Runtime's bounded target-local carrier.

    Runtime supplies the effective-policy ``.planning-lite`` directory.  The
    nested path is private carrier layout selected for this implementation;
    the public ref remains content-derived and independent of that layout.
    """
    ref = cancellation_tombstone_ref(record)
    return Path(carrier_root) / "dependency-admission" / "cancellations" / f"{ref.removeprefix('cancellation:')}.json"


def resolve_cancellation_tombstone(
    carrier_root: str | Path, record: CancellationTombstoneV1
) -> tuple[str, CancellationTombstoneV1] | None:
    """Strictly reread the exact immutable object for the requested edge."""
    path = cancellation_tombstone_path(carrier_root, record)
    try:
        raw = path.read_bytes()
    except FileNotFoundError:
        return None
    except OSError as exc:
        raise CancellationCarrierError("cannot read cancellation tombstone") from exc
    stored = decode_cancellation_tombstone(raw)
    if stored != record:
        raise CancellationCarrierError("cancellation identity resolved to conflicting tombstone content")
    return cancellation_tombstone_ref(stored), stored


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    try:
        descriptor = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(descriptor)
    except OSError:
        pass
    finally:
        os.close(descriptor)


def _publish_cancellation_tombstone_locked(
    carrier_root: str | Path, record: CancellationTombstoneV1
) -> tuple[str, CancellationTombstoneV1]:
    """Publish once by same-directory link, then verify the durable bytes.

    The caller must already hold Runtime's effective-policy V2 mutation lock.
    Staging is flushed and fsynced; immutable publication never replaces an
    object with the deterministic name. Existing equal bytes are accepted only
    after strict reread, while conflicts and I/O failures fail closed.
    """
    raw = encode_cancellation_tombstone(record)
    final = cancellation_tombstone_path(carrier_root, record)
    try:
        final.parent.mkdir(parents=True, exist_ok=True)
        if final.exists():
            verified = final.read_bytes()
            stored = decode_cancellation_tombstone(verified)
            if verified != raw or stored != record:
                raise CancellationCarrierError("conflicting immutable cancellation tombstone")
            return cancellation_tombstone_ref(stored), stored
        staged: Path | None = None
        try:
            with tempfile.NamedTemporaryFile(
                mode="wb", dir=final.parent, prefix=".cancellation-", suffix=".tmp", delete=False
            ) as handle:
                staged = Path(handle.name)
                handle.write(raw)
                handle.flush()
                os.fsync(handle.fileno())
            try:
                os.link(staged, final)
            except FileExistsError:
                pass
            staged.unlink(missing_ok=True)
            staged = None
        finally:
            if staged is not None:
                staged.unlink(missing_ok=True)
        verified = final.read_bytes()
        stored = decode_cancellation_tombstone(verified)
        if verified != raw or stored != record:
            raise CancellationCarrierError("published cancellation tombstone failed byte verification")
        _fsync_directory(final.parent)
        return cancellation_tombstone_ref(stored), stored
    except CancellationCarrierError:
        raise
    except OSError as exc:
        raise CancellationCarrierError("cancellation tombstone publication or reread failed") from exc


def historical_use_is_valid(
    root: str | Path,
    task_id: str,
    bound_requirement: Mapping[str, Any],
    bound_approved_plan_digest: str,
) -> bool:
    """Re-resolve current governance and validate an immutable task requirement.

    The predicate validates the bound requirement's exact V2 key set and
    content-derived ID, then requires the current resolver to verify the
    structured amendment table, continuous effect values, current approval
    digests, and reconciliation receipt. The caller-carried approved Plan digest
    is issuance-time general provenance: T-01 validates only its lowercase
    SHA-256 marker shape and does not authenticate it against the immutable
    Authorization/Preparation record. That owner authenticates the exact value
    stored at issuance. The value may differ from the current general digest;
    neither equality nor difference alone determines dependency freshness.
    Current-use validity is projection-relative: unrelated governed amendments
    may change general provenance while an unchanged own projection remains
    usable, whereas material edits and reversions remain in that projection's
    effect history. This result informs a later authority owner and grants no
    execution, rebinding, or runtime transition authority. Current projections
    and classifications are re-derived from the active pointer and owned files;
    invalid or incomplete current governance returns false.
    """
    _validate_requirement(bound_requirement, root)
    if not isinstance(bound_approved_plan_digest, str) or not _SHA256_RE.fullmatch(bound_approved_plan_digest):
        raise _fail("BOUND_APPROVED_DIGEST_INVALID", "bound approval provenance must be lowercase SHA-256")
    try:
        current = resolve_dependency(root, task_id)
    except DependencyAdmissionError:
        return False
    if not current.history_complete:
        return False
    same_requirement = dict(bound_requirement) == current.requirement
    if bound_approved_plan_digest == current.approved_plan_digest:
        return same_requirement
    return current.history_complete and same_requirement
