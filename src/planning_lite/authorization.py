"""Bounded owner-issued Attempt action authorizations.

This module owns immutable target-local Authorization records. New Preparation
ingress derives its nine-field V2 binding from the canonical dependency
resolver, then asks Runtime's public cancellation owner before immutable
publication. Runtime never calls this issuer. V1 Recovery remains
Plan-independent and byte-compatible; invalidation V2 records require the
same exact ADR bytes at issuance and every later resolution.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
import json
import hashlib
import os
from pathlib import Path
import re
import secrets
import threading
import tempfile
from typing import Any, Literal, Mapping

from .dependency_admission import (
    DependencyAdmissionError,
    DependencyResolution,
    historical_use_is_valid,
    resolve_dependency,
)
from .workspace import WorkspaceError, load_effective_policy


class AuthorizationError(RuntimeError):
    """Fail-closed authorization issuance, decoding, or storage error."""


class AuthorizationAction(str, Enum):
    PREPARATION = "OWNER_AUTHORIZED_ATTEMPT_PREPARATION"
    RECOVERY = "OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION"
    DEPENDENCY_PROOF_INVALIDATION = "OWNER_AUTHORIZED_DEPENDENCY_PROOF_INVALIDATION"


class ResolutionOutcome(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    INVALID_REFERENCE = "INVALID_REFERENCE"
    NOT_FOUND = "NOT_FOUND"
    CORRUPT_CONFLICT = "CORRUPT_CONFLICT"
    WRONG_ACTION = "WRONG_ACTION"
    WRONG_SCOPE = "WRONG_SCOPE"


AuthorizationActionValue = Literal[
    "OWNER_AUTHORIZED_ATTEMPT_PREPARATION",
    "OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION",
    "OWNER_AUTHORIZED_DEPENDENCY_PROOF_INVALIDATION",
]


@dataclass(frozen=True, slots=True)
class PreparationScopeV1:
    change_id: str
    task_or_operation_id: str


@dataclass(frozen=True, slots=True)
class PreparationScopeV2:
    """Resolver-owned exact nine-field current Preparation binding.

    Callers submit only the two request identities in PreparationScopeV1;
    this scope is constructed from approved current governance and never
    accepted as a trusted issuer input.
    """

    change_id: str
    task_or_operation_id: str
    plan_ref: str
    tasks_ref: str
    approved_plan_digest: str
    dependency_semantic_digest: str
    requirement_id: str
    dependency_classification: str
    expected_attempt_id: str | None


@dataclass(frozen=True, slots=True)
class DependencyProofInvalidationScopeV1:
    """Exact fixed T-01/A1 -> T-02/A1 proof invalidation tuple."""

    change_id: str
    source_attempt_id: str
    successor_attempt_id: str
    proof_id: str


@dataclass(frozen=True, slots=True)
class RecoveryScopeV1:
    attempt_id: str


AuthorizationScope = PreparationScopeV1 | PreparationScopeV2 | RecoveryScopeV1 | DependencyProofInvalidationScopeV1


@dataclass(frozen=True, slots=True)
class AuthorizationRecordV1:
    schema_version: int
    authorization_ref: str
    action_type: AuthorizationAction
    scope: AuthorizationScope
    decision_authority_class: str
    decision_outcome: Literal["AUTHORIZED"]
    decision_provenance_ref: str


@dataclass(frozen=True, slots=True)
class AuthorizationRecordV2:
    """Exact seven-key immutable V2 Preparation or invalidation authority."""

    schema_version: int
    authorization_ref: str
    action_type: AuthorizationAction
    scope: PreparationScopeV2 | DependencyProofInvalidationScopeV1
    decision_authority_class: str
    decision_outcome: Literal["AUTHORIZED"]
    decision_provenance_ref: str


AuthorizationRecord = AuthorizationRecordV1 | AuthorizationRecordV2


@dataclass(frozen=True, slots=True)
class ResolutionResultV1:
    outcome: ResolutionOutcome
    record: AuthorizationRecord | None = None


AUTHORIZATION_REF_PATTERN = re.compile(r"authz_[0-9a-f]{32}\Z")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}\Z")
REQUIREMENT_PATTERN = re.compile(r"dreq_[0-9a-f]{64}\Z")
PROOF_PATTERN = re.compile(r"dproof_[0-9a-f]{64}\Z")
DECISION_PATH_PATTERN = re.compile(
    r"\.planning/decisions/(ADR-([0-9]{4})-([a-z0-9]+(?:-[a-z0-9]+)*)\.md)\Z"
)
DECISION_REF_PATTERN = re.compile(
    r"decision:(\.planning/decisions/[^@]+\.md)@sha256:([0-9a-f]{64})\Z"
)
MAX_ALLOCATION_ATTEMPTS = 16
PREPARATION_ACTION = AuthorizationAction.PREPARATION
RECOVERY_ACTION = AuthorizationAction.RECOVERY
INVALIDATION_ACTION = AuthorizationAction.DEPENDENCY_PROOF_INVALIDATION
PREPARATION_AUTHORITY = "EXISTING_OWNER/GATE_GOVERNANCE_AUTHORITY"
RECOVERY_AUTHORITY = "EXISTING_OWNER/LIFECYCLE_CONTROL_AUTHORITY"
TOP_LEVEL_KEYS = frozenset(
    {
        "schema_version",
        "authorization_ref",
        "action_type",
        "scope",
        "decision_authority_class",
        "decision_outcome",
        "decision_provenance_ref",
    }
)

_THREAD_LOCKS: dict[Path, threading.RLock] = {}
_THREAD_LOCKS_GUARD = threading.Lock()


def _thread_lock_for(path: Path) -> threading.RLock:
    key = path.resolve()
    with _THREAD_LOCKS_GUARD:
        return _THREAD_LOCKS.setdefault(key, threading.RLock())


@contextmanager
def _store_lock(store: Path):
    """Hold one process and cross-process lock for the target store."""

    lock_path = store / ".authorization.lock"
    handle = None
    acquired = False
    try:
        store.mkdir(parents=True, exist_ok=True)
        handle = lock_path.open("a+b")
        if os.name == "nt":
            import msvcrt

            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            acquired = True
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            acquired = True
        yield
    except (ImportError, OSError) as exc:
        if not acquired:
            raise AuthorizationError(f"Cannot acquire authorization store lock: {lock_path}") from exc
        raise
    finally:
        if handle is not None:
            try:
                if acquired:
                    if os.name == "nt":
                        import msvcrt

                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                    else:
                        import fcntl

                        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            finally:
                handle.close()


def _identifier(value: object, field: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip():
        raise AuthorizationError(f"{field} must be a non-empty already-stripped string")
    if "\r" in value or "\n" in value:
        raise AuthorizationError(f"{field} must not contain CR/LF")
    return value


def _action(value: object) -> AuthorizationAction:
    try:
        return value if isinstance(value, AuthorizationAction) else AuthorizationAction(value)
    except (TypeError, ValueError) as exc:
        raise AuthorizationError(f"Unsupported authorization action: {value!r}") from exc


def _reference(value: object) -> str:
    if not isinstance(value, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(value):
        raise AuthorizationError("authorization_ref must match authz_[0-9a-f]{32}")
    return value


def _normalized_target_ref(value: object, field: str) -> str:
    ref = _identifier(value, field)
    if "\\" in ref or ref.startswith("/") or ref.endswith("/"):
        raise AuthorizationError(f"{field} must be a normalized target-relative POSIX path")
    parts = ref.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise AuthorizationError(f"{field} must be a normalized target-relative POSIX path")
    return ref


def _scope_mapping(scope: AuthorizationScope) -> dict[str, object]:
    if isinstance(scope, PreparationScopeV1):
        return {
            "change_id": _identifier(scope.change_id, "change_id"),
            "task_or_operation_id": _identifier(
                scope.task_or_operation_id, "task_or_operation_id"
            ),
        }
    if isinstance(scope, PreparationScopeV2):
        change_id = _identifier(scope.change_id, "change_id")
        task_id = _identifier(scope.task_or_operation_id, "task_or_operation_id")
        plan_ref = _normalized_target_ref(scope.plan_ref, "plan_ref")
        tasks_ref = _normalized_target_ref(scope.tasks_ref, "tasks_ref")
        if not isinstance(scope.approved_plan_digest, str) or not SHA256_PATTERN.fullmatch(scope.approved_plan_digest):
            raise AuthorizationError("approved_plan_digest must be lowercase SHA-256")
        if not isinstance(scope.dependency_semantic_digest, str) or not SHA256_PATTERN.fullmatch(scope.dependency_semantic_digest):
            raise AuthorizationError("dependency_semantic_digest must be lowercase SHA-256")
        if not isinstance(scope.requirement_id, str) or not REQUIREMENT_PATTERN.fullmatch(scope.requirement_id):
            raise AuthorizationError("requirement_id must match dreq_<sha256>")
        if scope.dependency_classification == "DEPENDENCY_EDGE_MEMBER":
            if task_id not in {"T-01", "T-02"} or scope.expected_attempt_id != f"{change_id}/{task_id}/A1":
                raise AuthorizationError("dependent Preparation must bind its exact supported endpoint A1")
        elif scope.dependency_classification == "NOT_APPLICABLE":
            if scope.expected_attempt_id is not None:
                raise AuthorizationError("independent Preparation must have a null expected_attempt_id")
        else:
            raise AuthorizationError("dependency_classification is unsupported")
        return {
            "change_id": change_id,
            "task_or_operation_id": task_id,
            "plan_ref": plan_ref,
            "tasks_ref": tasks_ref,
            "approved_plan_digest": scope.approved_plan_digest,
            "dependency_semantic_digest": scope.dependency_semantic_digest,
            "requirement_id": scope.requirement_id,
            "dependency_classification": scope.dependency_classification,
            "expected_attempt_id": scope.expected_attempt_id,
        }
    if isinstance(scope, RecoveryScopeV1):
        return {"attempt_id": _identifier(scope.attempt_id, "attempt_id")}
    if isinstance(scope, DependencyProofInvalidationScopeV1):
        change_id = _identifier(scope.change_id, "change_id")
        source = _identifier(scope.source_attempt_id, "source_attempt_id")
        successor = _identifier(scope.successor_attempt_id, "successor_attempt_id")
        if source != f"{change_id}/T-01/A1" or successor != f"{change_id}/T-02/A1":
            raise AuthorizationError("invalidation scope must bind the exact fixed edge A1 pair")
        if not PROOF_PATTERN.fullmatch(scope.proof_id):
            raise AuthorizationError("proof_id must match dproof_<sha256>")
        return {
            "change_id": change_id,
            "source_attempt_id": source,
            "successor_attempt_id": successor,
            "proof_id": scope.proof_id,
        }
    raise AuthorizationError("scope must be a supported typed authorization scope")


def _expected_authority(action: AuthorizationAction) -> str:
    return RECOVERY_AUTHORITY if action is RECOVERY_ACTION else PREPARATION_AUTHORITY


def _record_mapping(record: AuthorizationRecord) -> dict[str, object]:
    action = _action(record.action_type)
    ref = _reference(record.authorization_ref)
    if isinstance(record, AuthorizationRecordV1):
        if type(record.schema_version) is not int or record.schema_version != 1:
            raise AuthorizationError("schema_version must be exactly 1")
        if action is INVALIDATION_ACTION:
            raise AuthorizationError("V1 does not support dependency-proof invalidation")
        if action is PREPARATION_ACTION and not isinstance(record.scope, PreparationScopeV1):
            raise AuthorizationError("V1 preparation action requires PreparationScopeV1")
        if action is RECOVERY_ACTION and not isinstance(record.scope, RecoveryScopeV1):
            raise AuthorizationError("recovery action requires RecoveryScopeV1")
    elif isinstance(record, AuthorizationRecordV2):
        if type(record.schema_version) is not int or record.schema_version != 2:
            raise AuthorizationError("schema_version must be exactly 2")
        if action not in {PREPARATION_ACTION, INVALIDATION_ACTION}:
            raise AuthorizationError("V2 supports Preparation and dependency-proof invalidation only")
        if action is PREPARATION_ACTION and not isinstance(record.scope, PreparationScopeV2):
            raise AuthorizationError("V2 preparation action requires PreparationScopeV2")
        if action is INVALIDATION_ACTION and not isinstance(record.scope, DependencyProofInvalidationScopeV1):
            raise AuthorizationError("V2 invalidation action requires DependencyProofInvalidationScopeV1")
    else:
        raise AuthorizationError("unsupported Authorization record type")
    if record.decision_outcome != "AUTHORIZED":
        raise AuthorizationError("decision_outcome must be AUTHORIZED")
    provenance = _identifier(record.decision_provenance_ref, "decision_provenance_ref")
    authority = _identifier(record.decision_authority_class, "decision_authority_class")
    if authority != _expected_authority(action):
        raise AuthorizationError("decision_authority_class does not match action")
    _scope_mapping(record.scope)
    return {
        "schema_version": record.schema_version,
        "authorization_ref": ref,
        "action_type": action.value,
        "scope": _scope_mapping(record.scope),
        "decision_authority_class": authority,
        "decision_outcome": "AUTHORIZED",
        "decision_provenance_ref": provenance,
    }


def encode_authorization_record(record: AuthorizationRecord) -> bytes:
    """Return one exact canonical record byte sequence."""

    try:
        return (
            json.dumps(
                _record_mapping(record),
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
            ).encode("utf-8")
            + b"\n"
        )
    except (TypeError, ValueError, UnicodeError) as exc:
        raise AuthorizationError(f"Cannot encode authorization record: {exc}") from exc


def _reject_duplicate_members(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise AuthorizationError(f"Duplicate JSON member: {key}")
        result[key] = value
    return result


def _mapping_record(value: object) -> AuthorizationRecord:
    if not isinstance(value, dict) or set(value) != TOP_LEVEL_KEYS:
        raise AuthorizationError("authorization record has incorrect top-level keys")
    raw_schema = value["schema_version"]
    if type(raw_schema) is not int or raw_schema not in {1, 2}:
        raise AuthorizationError("schema_version must be integer 1 or 2")
    action = _action(value["action_type"])
    ref = _reference(value["authorization_ref"])
    authority = _identifier(value["decision_authority_class"], "decision_authority_class")
    outcome = value["decision_outcome"]
    if outcome != "AUTHORIZED":
        raise AuthorizationError("decision_outcome must be AUTHORIZED")
    provenance = _identifier(value["decision_provenance_ref"], "decision_provenance_ref")
    raw_scope = value["scope"]
    if not isinstance(raw_scope, dict):
        raise AuthorizationError("scope must be an object")
    if authority != _expected_authority(action):
        raise AuthorizationError("decision_authority_class does not match action")
    if raw_schema == 1:
        if action is INVALIDATION_ACTION:
            raise AuthorizationError("V1 does not support dependency-proof invalidation")
        if action is PREPARATION_ACTION:
            if set(raw_scope) != {"change_id", "task_or_operation_id"}:
                raise AuthorizationError("V1 preparation scope has incorrect keys")
            scope: AuthorizationScope = PreparationScopeV1(
                _identifier(raw_scope["change_id"], "change_id"),
                _identifier(raw_scope["task_or_operation_id"], "task_or_operation_id"),
            )
        else:
            if action is not RECOVERY_ACTION or set(raw_scope) != {"attempt_id"}:
                raise AuthorizationError("V1 recovery scope has incorrect keys")
            scope = RecoveryScopeV1(_identifier(raw_scope["attempt_id"], "attempt_id"))
        return AuthorizationRecordV1(1, ref, action, scope, authority, "AUTHORIZED", provenance)

    if action is PREPARATION_ACTION:
        expected_keys = {
            "change_id",
            "task_or_operation_id",
            "plan_ref",
            "tasks_ref",
            "approved_plan_digest",
            "dependency_semantic_digest",
            "requirement_id",
            "dependency_classification",
            "expected_attempt_id",
        }
        if set(raw_scope) != expected_keys:
            raise AuthorizationError("V2 preparation scope has incorrect keys")
        expected_attempt_id = raw_scope["expected_attempt_id"]
        if expected_attempt_id is not None:
            expected_attempt_id = _identifier(expected_attempt_id, "expected_attempt_id")
        scope_v2: PreparationScopeV2 | DependencyProofInvalidationScopeV1 = PreparationScopeV2(
            _identifier(raw_scope["change_id"], "change_id"),
            _identifier(raw_scope["task_or_operation_id"], "task_or_operation_id"),
            _normalized_target_ref(raw_scope["plan_ref"], "plan_ref"),
            _normalized_target_ref(raw_scope["tasks_ref"], "tasks_ref"),
            _identifier(raw_scope["approved_plan_digest"], "approved_plan_digest"),
            _identifier(raw_scope["dependency_semantic_digest"], "dependency_semantic_digest"),
            _identifier(raw_scope["requirement_id"], "requirement_id"),
            _identifier(raw_scope["dependency_classification"], "dependency_classification"),
            expected_attempt_id,
        )
    elif action is INVALIDATION_ACTION:
        if set(raw_scope) != {"change_id", "source_attempt_id", "successor_attempt_id", "proof_id"}:
            raise AuthorizationError("V2 invalidation scope has incorrect keys")
        scope_v2 = DependencyProofInvalidationScopeV1(
            _identifier(raw_scope["change_id"], "change_id"),
            _identifier(raw_scope["source_attempt_id"], "source_attempt_id"),
            _identifier(raw_scope["successor_attempt_id"], "successor_attempt_id"),
            _identifier(raw_scope["proof_id"], "proof_id"),
        )
    else:
        raise AuthorizationError("V2 does not support Recovery")
    _scope_mapping(scope_v2)
    return AuthorizationRecordV2(2, ref, action, scope_v2, authority, "AUTHORIZED", provenance)


def decode_authorization_record(raw: bytes) -> AuthorizationRecord:
    """Strictly decode and byte-validate one authoritative record."""

    if not isinstance(raw, bytes):
        raise AuthorizationError("authorization record bytes are required")
    try:
        decoded = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_members)
    except (UnicodeDecodeError, json.JSONDecodeError, AuthorizationError) as exc:
        raise AuthorizationError(f"Invalid authorization JSON: {exc}") from exc
    record = _mapping_record(decoded)
    if encode_authorization_record(record) != raw:
        raise AuthorizationError("Authorization record is not canonical bytes")
    return record


def authorization_store_path(target: str | os.PathLike[str] | Path) -> Path:
    """Return the one target-scoped store selected by effective policy."""

    product_root = Path(target).expanduser().resolve()
    try:
        policy = load_effective_policy(product_root)["project_policy"]
    except (WorkspaceError, KeyError, TypeError) as exc:
        raise AuthorizationError(f"Cannot load effective authorization root: {exc}") from exc
    planning_root = policy.get("planning_root")
    if not isinstance(planning_root, str) or not planning_root:
        raise AuthorizationError("effective planning_root is invalid")
    return product_root / Path(planning_root) / "project" / "authorizations"


def _allocate_authorization_ref() -> str:
    return f"authz_{secrets.token_hex(16)}"


def _dependency_root(target: str | os.PathLike[str] | Path) -> Path:
    """Return the consumer root consumed by the one existing T-01 resolver."""
    return Path(target).expanduser().resolve()


def _preparation_scope(resolution: DependencyResolution) -> PreparationScopeV2:
    """Derive own-endpoint Preparation scope from the current edge resolution.

    T-01 and T-02 share one dependent requirement and digest, while each
    immutable Authorization binds its own exact A1. Issuance checks that both
    edge A1 identities are free but occupies neither; later use revalidates
    the Authorization's own binding and own A1 availability.
    """
    requirement = resolution.requirement
    return PreparationScopeV2(
        change_id=resolution.change_id,
        task_or_operation_id=resolution.task_id,
        plan_ref=resolution.plan_ref,
        tasks_ref=resolution.tasks_ref,
        approved_plan_digest=resolution.approved_plan_digest,
        dependency_semantic_digest=resolution.dependency_semantic_digest,
        requirement_id=requirement["requirement_id"],
        dependency_classification=resolution.dependency_classification,
        expected_attempt_id=(
            f"{resolution.change_id}/{resolution.task_id}/A1"
            if resolution.dependency_classification == "DEPENDENCY_EDGE_MEMBER"
            else None
        ),
    )


def _prepare_scope_matches_current(
    stored: PreparationScopeV2, current: DependencyResolution, target: Path
) -> bool:
    current_scope = _preparation_scope(current)
    if (
        stored.change_id != current_scope.change_id
        or stored.task_or_operation_id != current_scope.task_or_operation_id
        or stored.plan_ref != current_scope.plan_ref
        or stored.tasks_ref != current_scope.tasks_ref
        or stored.dependency_semantic_digest != current_scope.dependency_semantic_digest
        or stored.requirement_id != current_scope.requirement_id
        or stored.dependency_classification != current_scope.dependency_classification
        or stored.expected_attempt_id != current_scope.expected_attempt_id
    ):
        return False
    # approved_plan_digest is immutable issuance provenance. The shared T-01
    # predicate validates projection-relative history and deliberately permits
    # unrelated governance changes to alter current general provenance.
    try:
        return historical_use_is_valid(
        _dependency_root(target),
        stored.task_or_operation_id,
        current.requirement,
            stored.approved_plan_digest,
        )
    except DependencyAdmissionError:
        return False


def _decision_provenance_parts(value: object) -> tuple[str, str, str]:
    reference = _identifier(value, "decision_provenance_ref")
    match = DECISION_REF_PATTERN.fullmatch(reference)
    if match is None:
        raise AuthorizationError("invalidation provenance must be an exact decision:<path>@sha256:<digest> ref")
    path, digest = match.groups()
    path_match = DECISION_PATH_PATTERN.fullmatch(path)
    if path_match is None or int(path_match.group(2)) == 0 or len(path_match.group(3)) > 64:
        raise AuthorizationError("decision path must match the exact ADR-NNNN-slug grammar")
    if _normalized_target_ref(path, "decision path") != path:
        raise AuthorizationError("decision path is not normalized")
    return path, f"ADR-{path_match.group(2)}", digest


def _canonical_decision_bytes(raw: bytes) -> bytes:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AuthorizationError("decision item UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise AuthorizationError("decision item must be strict UTF-8") from exc
    normalized = text.replace("\r\n", "\n")
    if "\r" in normalized:
        raise AuthorizationError("decision item contains a bare carriage return")
    if not normalized.endswith("\n") or normalized.endswith("\n\n"):
        raise AuthorizationError("decision item must have exactly one terminal LF")
    return normalized.encode("utf-8", errors="strict")


def _decision_json_object(body: str) -> dict[str, Any]:
    def reject_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in pairs:
            if key in result:
                raise AuthorizationError(f"decision block has duplicate JSON member: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(body, object_pairs_hook=reject_duplicates)
    except (json.JSONDecodeError, AuthorizationError) as exc:
        raise AuthorizationError(f"decision block JSON is invalid: {exc}") from exc
    if not isinstance(value, dict):
        raise AuthorizationError("decision block must contain one JSON object")
    return value


def _verify_decision_provenance(
    target: str | os.PathLike[str] | Path,
    provenance_ref: str,
    scope: DependencyProofInvalidationScopeV1,
) -> None:
    """Verify the exact ADR path, whole-item bytes, typed block, and proof tuple.

    The immutable Authorization stores this exact provenance string. Both
    issuance and later invalidation resolution call this same verifier, so a
    changed rationale, moved item, duplicate ordinal, or plausible substitute
    cannot replace the original decision.
    """
    relative_ref, decision_id, expected_digest = _decision_provenance_parts(provenance_ref)
    root = Path(target).expanduser().resolve()
    try:
        item = (root / Path(*relative_ref.split("/"))).resolve(strict=True)
    except OSError as exc:
        raise AuthorizationError("exact decision item is missing or cannot be resolved") from exc
    if not item.is_relative_to(root) or not item.is_file():
        raise AuthorizationError("decision item must resolve within the target root")
    try:
        raw = item.read_bytes()
    except OSError as exc:
        raise AuthorizationError("cannot read exact decision item") from exc
    canonical_bytes = _canonical_decision_bytes(raw)
    if hashlib.sha256(canonical_bytes).hexdigest() != expected_digest:
        raise AuthorizationError("decision provenance digest does not match whole-item canonical-LF bytes")

    ordinal = int(decision_id[-4:])
    if not 1 <= ordinal <= 9999:
        raise AuthorizationError("ADR ordinal must be between 0001 and 9999")
    decisions_dir = root / ".planning" / "decisions"
    seen: list[str] = []
    try:
        candidates = decisions_dir.glob("ADR-*.md")
        for candidate in candidates:
            match = DECISION_PATH_PATTERN.fullmatch(candidate.relative_to(root).as_posix())
            if match is not None and int(match.group(2)) == ordinal:
                seen.append(candidate.name)
    except OSError as exc:
        raise AuthorizationError("cannot verify unique ADR ordinal") from exc
    if seen != [item.name]:
        raise AuthorizationError("ADR ordinal is duplicated or exact decision item is not discoverable")

    text = canonical_bytes.decode("utf-8")
    heading = f"# {decision_id}:"
    if not text.startswith(heading):
        raise AuthorizationError("decision heading does not match its ADR identity")
    statuses = re.findall(r"^- Status:.*$", text, re.MULTILINE)
    if statuses != ["- Status: `Accepted`"]:
        raise AuthorizationError("decision item must contain exactly one Accepted status line")

    info_line = "```dependency-proof-invalidation-decision-v1"
    lines = text.splitlines()
    openings = [index for index, line in enumerate(lines) if line == info_line]
    if len(openings) != 1:
        raise AuthorizationError("decision item must contain exactly one typed invalidation block")
    opening = openings[0]
    closings = [index for index in range(opening + 1, len(lines)) if lines[index] == "```"]
    if not closings:
        raise AuthorizationError("decision invalidation block is not closed")
    closing = closings[0]
    block = _decision_json_object("\n".join(lines[opening + 1 : closing]))
    expected_keys = {
        "schema_version",
        "decision_id",
        "decision_kind",
        "decision_status",
        "change_id",
        "source_attempt_id",
        "successor_attempt_id",
        "proof_id",
        "decision_outcome",
    }
    if set(block) != expected_keys:
        raise AuthorizationError("decision invalidation block has an incorrect nine-key shape")
    if type(block["schema_version"]) is not int or block["schema_version"] != 1:
        raise AuthorizationError("decision schema_version must be integer 1")
    try:
        current = resolve_dependency(_dependency_root(root), "T-02")
    except DependencyAdmissionError as exc:
        raise AuthorizationError("decision Change has no current approved dependency governance") from exc
    expected = {
        "decision_id": decision_id,
        "decision_kind": "DEPENDENCY_PROOF_INVALIDATION",
        "decision_status": "APPROVED",
        "change_id": current.change_id,
        "source_attempt_id": f"{current.change_id}/T-01/A1",
        "successor_attempt_id": f"{current.change_id}/T-02/A1",
        "proof_id": scope.proof_id,
        "decision_outcome": "INVALIDATE_EXACT_DEPENDENCY_PROOF",
    }
    if any(block.get(key) != value for key, value in expected.items()):
        raise AuthorizationError("decision block does not bind the exact current Change/proof tuple")
    if scope.change_id != current.change_id:
        raise AuthorizationError("invalidation scope Change is not the exact active governed Change")


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    try:
        fd = os.open(path, os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        pass
    finally:
        os.close(fd)


def _publish_authorization(target: str | os.PathLike[str] | Path, record: AuthorizationRecord) -> str:
    """Publish one fully validated immutable record with exact reread evidence."""
    store = authorization_store_path(target)
    with _thread_lock_for(store):
        store.mkdir(parents=True, exist_ok=True)
        for _ in range(MAX_ALLOCATION_ATTEMPTS):
            ref = _reference(_allocate_authorization_ref())
            if isinstance(record, AuthorizationRecordV1):
                candidate: AuthorizationRecord = AuthorizationRecordV1(
                    1,
                    ref,
                    record.action_type,
                    record.scope,
                    record.decision_authority_class,
                    "AUTHORIZED",
                    record.decision_provenance_ref,
                )
            else:
                candidate = AuthorizationRecordV2(
                    2,
                    ref,
                    record.action_type,
                    record.scope,
                    record.decision_authority_class,
                    "AUTHORIZED",
                    record.decision_provenance_ref,
                )
            raw = encode_authorization_record(candidate)
            final = store / f"{ref}.json"
            temporary_path: Path | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="wb", dir=store, prefix=".authorization-", suffix=".tmp", delete=False
                ) as handle:
                    temporary_path = Path(handle.name)
                    handle.write(raw)
                    handle.flush()
                    os.fsync(handle.fileno())
                with _store_lock(store):
                    if final.exists():
                        continue
                    try:
                        os.link(temporary_path, final)
                    except FileExistsError:
                        continue
                    temporary_path.unlink(missing_ok=True)
                    temporary_path = None
                    verified = final.read_bytes()
                    decoded = decode_authorization_record(verified)
                    if decoded != candidate or decoded.authorization_ref != ref or verified != raw:
                        raise AuthorizationError("Published authorization failed byte verification")
                    _fsync_directory(store)
                    return ref
            finally:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)
        raise AuthorizationError("AUTHORIZATION_REF_ALLOCATION_EXHAUSTED")


def issue_authorization(
    target: str | os.PathLike[str] | Path,
    action_type: AuthorizationAction | AuthorizationActionValue | str,
    scope: AuthorizationScope,
    decision_provenance_ref: str,
) -> str:
    """Resolve Preparation authority and exact A1 availability before publish.

    Preparation accepts only a two-field request scope, resolves current
    approved governance beneath the validated effective planning root, and
    invokes Runtime's locked cancellation owner before it can create the
    Authorization store. For the dependent edge, Attempt Runtime must report
    exact T-01/A1 and T-02/A1 as NOT_FOUND; occupancy, invalid IDs, corrupt
    stores, and lookup errors fail closed before immutable publication. These
    checks read Runtime's authority and never parse its store here. Recovery
    remains the exact V1 Plan-independent route. Invalidation V2 requires the
    exact D8 product-root decision item and typed proof tuple. No
    caller-supplied V2 binding reaches publication.
    """
    action = _action(action_type)
    provenance = _identifier(decision_provenance_ref, "decision_provenance_ref")
    if action is PREPARATION_ACTION:
        if type(scope) is not PreparationScopeV1:
            raise AuthorizationError("Preparation ingress requires only PreparationScopeV1 request identities")
        request_mapping = _scope_mapping(scope)
        try:
            governed_root = _dependency_root(target)
            resolution = resolve_dependency(governed_root, scope.task_or_operation_id)
        except (DependencyAdmissionError, AuthorizationError) as exc:
            raise AuthorizationError(f"Preparation requires canonical approved governance: {exc}") from exc
        if resolution.change_id != scope.change_id:
            raise AuthorizationError("requested Change does not match the active governed Change")
        expected_scope = _preparation_scope(resolution)

        # Local import is the approved Runtime -> Authorization cycle break.
        # Cancellation is owned and durably re-resolved by Runtime; an
        # Authorization rejection cannot substitute for its lock/tombstone.
        from .attempt_runtime import (
            AttemptRuntimeError,
            CancellationOutcome,
            observe_dependency_cancellation,
        )

        try:
            observation = observe_dependency_cancellation(
                target,
                str(request_mapping["change_id"]),
                str(request_mapping["task_or_operation_id"]),
            )
        except AttemptRuntimeError as exc:
            raise AuthorizationError(f"Runtime cancellation observation failed closed: {exc}") from exc
        if observation.outcome is not CancellationOutcome.CLEAR:
            raise AuthorizationError("Preparation is blocked by the durable dependency cancellation tombstone")
        if observation.change_id != expected_scope.change_id or observation.requested_task_id != expected_scope.task_or_operation_id:
            raise AuthorizationError("Runtime cancellation observation does not match the resolved Preparation request")
        if expected_scope.dependency_classification == "DEPENDENCY_EDGE_MEMBER":
            from .attempt_runtime import LookupOutcome, lookup_attempt

            for attempt_id in (
                f"{expected_scope.change_id}/T-01/A1",
                f"{expected_scope.change_id}/T-02/A1",
            ):
                try:
                    lookup = lookup_attempt(target, attempt_id)
                except AttemptRuntimeError as exc:
                    raise AuthorizationError(
                        f"Runtime exact Attempt lookup failed closed for {attempt_id}: {exc}"
                    ) from exc
                if lookup.outcome is not LookupOutcome.NOT_FOUND:
                    raise AuthorizationError(
                        f"dependent Preparation requires unoccupied exact A1 {attempt_id}; "
                        f"Runtime returned {lookup.outcome.value}"
                    )
        record_v2 = AuthorizationRecordV2(
            2,
            "authz_" + "0" * 32,
            action,
            expected_scope,
            PREPARATION_AUTHORITY,
            "AUTHORIZED",
            provenance,
        )
        return _publish_authorization(target, record_v2)
    if action is RECOVERY_ACTION:
        if type(scope) is not RecoveryScopeV1:
            raise AuthorizationError("recovery action requires RecoveryScopeV1")
        _scope_mapping(scope)
        record_v1 = AuthorizationRecordV1(
            1,
            "authz_" + "0" * 32,
            action,
            scope,
            RECOVERY_AUTHORITY,
            "AUTHORIZED",
            provenance,
        )
        return _publish_authorization(target, record_v1)
    if action is INVALIDATION_ACTION:
        if type(scope) is not DependencyProofInvalidationScopeV1:
            raise AuthorizationError("invalidation action requires DependencyProofInvalidationScopeV1")
        _scope_mapping(scope)
        try:
            governed = resolve_dependency(_dependency_root(target), "T-02")
        except DependencyAdmissionError as exc:
            raise AuthorizationError("invalidation requires current approved dependency governance") from exc
        if governed.change_id != scope.change_id:
            raise AuthorizationError("invalidation scope does not name the active governed Change")
        _verify_decision_provenance(target, provenance, scope)
        record_v2 = AuthorizationRecordV2(
            2,
            "authz_" + "0" * 32,
            action,
            scope,
            PREPARATION_AUTHORITY,
            "AUTHORIZED",
            provenance,
        )
        return _publish_authorization(target, record_v2)
    raise AuthorizationError("unsupported Authorization ingress")


def issue_preparation_authorization(
    target: str | os.PathLike[str] | Path,
    change_id: str,
    task_or_operation_id: str,
    decision_provenance_ref: str,
) -> str:
    """Issue V2 Preparation through the same request-only generic ingress."""
    return issue_authorization(
        target,
        PREPARATION_ACTION,
        PreparationScopeV1(change_id, task_or_operation_id),
        decision_provenance_ref,
    )


def issue_recovery_authorization(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
    decision_provenance_ref: str,
) -> str:
    """Issue the unchanged Plan-independent V1 Recovery record."""
    return issue_authorization(
        target,
        RECOVERY_ACTION,
        RecoveryScopeV1(attempt_id),
        decision_provenance_ref,
    )


def validate_preparation_applicability(
    record: AuthorizationRecord,
    scope: PreparationScopeV1 | PreparationScopeV2,
    target: str | os.PathLike[str] | Path | None = None,
) -> ResolutionOutcome:
    """Check exact V1 legacy or current V2 Preparation applicability.

    A V1 record is usable only for a resolver-derived independent task. A V2
    record must still match the current own projection and complete amendment
    chain; current general approval digest equality is not a freshness test.
    """
    if record.action_type is not PREPARATION_ACTION:
        return ResolutionOutcome.WRONG_ACTION
    if isinstance(record, AuthorizationRecordV1):
        if not isinstance(scope, PreparationScopeV1) or not isinstance(record.scope, PreparationScopeV1):
            return ResolutionOutcome.WRONG_SCOPE
        if record.scope != scope or target is None:
            return ResolutionOutcome.WRONG_SCOPE
        try:
            current = resolve_dependency(_dependency_root(target), scope.task_or_operation_id)
        except (DependencyAdmissionError, AuthorizationError):
            return ResolutionOutcome.CORRUPT_CONFLICT
        if current.change_id != scope.change_id or current.dependency_classification != "NOT_APPLICABLE":
            return ResolutionOutcome.WRONG_SCOPE
        return ResolutionOutcome.AUTHORIZED
    if not isinstance(record.scope, PreparationScopeV2):
        return ResolutionOutcome.WRONG_SCOPE
    if type(scope) is not PreparationScopeV2 or record.scope != scope:
        # The pre-T-03 V1 materializer supplies only PreparationScopeV1. Do not
        # let it consume a new V2 record without copying the resolver binding;
        # T-03 owns that V2 persistence transition.
        return ResolutionOutcome.WRONG_SCOPE
    if target is None:
        return ResolutionOutcome.WRONG_SCOPE
    try:
        current = resolve_dependency(_dependency_root(target), record.scope.task_or_operation_id)
    except (DependencyAdmissionError, AuthorizationError):
        return ResolutionOutcome.CORRUPT_CONFLICT
    if current.change_id != record.scope.change_id:
        return ResolutionOutcome.WRONG_SCOPE
    return (
        ResolutionOutcome.AUTHORIZED
        if _prepare_scope_matches_current(record.scope, current, Path(target))
        else ResolutionOutcome.WRONG_SCOPE
    )


def validate_recovery_applicability(
    record: AuthorizationRecord, scope: RecoveryScopeV1
) -> ResolutionOutcome:
    if record.action_type is not RECOVERY_ACTION:
        return ResolutionOutcome.WRONG_ACTION
    if not isinstance(scope, RecoveryScopeV1) or not isinstance(record.scope, RecoveryScopeV1):
        return ResolutionOutcome.WRONG_SCOPE
    if record.scope != scope:
        return ResolutionOutcome.WRONG_SCOPE
    return ResolutionOutcome.AUTHORIZED


def _scan_store(store: Path) -> tuple[dict[str, AuthorizationRecord], bool]:
    records: dict[str, AuthorizationRecord] = {}
    if not store.is_dir():
        return records, False
    for path in sorted(store.glob("*.json"), key=lambda item: item.name):
        try:
            record = decode_authorization_record(path.read_bytes())
        except (OSError, AuthorizationError):
            return {}, True
        if path.stem != record.authorization_ref:
            return {}, True
        if record.authorization_ref in records:
            return {}, True
        records[record.authorization_ref] = record
    return records, False


def resolve_authorization(
    target: str | os.PathLike[str] | Path,
    authorization_ref: str,
    action_type: AuthorizationAction | AuthorizationActionValue | str,
    scope: AuthorizationScope,
) -> ResolutionResultV1:
    """Resolve immutable V1/V2 records without writing or hiding transitions.

    Preparation resolution re-derives current governed scope and historical
    projection validity. V1 Recovery stays independent of Plan state. V2
    invalidation reopens only the exact stored decision path and rechecks its
    whole-item digest and typed tuple; it never searches for a replacement.
    """

    if not isinstance(authorization_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(
        authorization_ref
    ):
        return ResolutionResultV1(ResolutionOutcome.INVALID_REFERENCE)
    try:
        action = _action(action_type)
    except AuthorizationError:
        return ResolutionResultV1(ResolutionOutcome.WRONG_ACTION)
    if action is PREPARATION_ACTION and not isinstance(scope, (PreparationScopeV1, PreparationScopeV2)):
        return ResolutionResultV1(ResolutionOutcome.WRONG_SCOPE)
    if action is RECOVERY_ACTION and type(scope) is not RecoveryScopeV1:
        return ResolutionResultV1(ResolutionOutcome.WRONG_SCOPE)
    if action is INVALIDATION_ACTION and type(scope) is not DependencyProofInvalidationScopeV1:
        return ResolutionResultV1(ResolutionOutcome.WRONG_SCOPE)
    try:
        _scope_mapping(scope)
    except AuthorizationError:
        return ResolutionResultV1(ResolutionOutcome.WRONG_SCOPE)
    try:
        store = authorization_store_path(target)
    except AuthorizationError:
        return ResolutionResultV1(ResolutionOutcome.CORRUPT_CONFLICT)
    records, corrupt = _scan_store(store)
    if corrupt:
        return ResolutionResultV1(ResolutionOutcome.CORRUPT_CONFLICT)
    record = records.get(authorization_ref)
    if record is None:
        return ResolutionResultV1(ResolutionOutcome.NOT_FOUND)
    if record.action_type is not action:
        return ResolutionResultV1(ResolutionOutcome.WRONG_ACTION, record)
    if action is PREPARATION_ACTION:
        outcome = validate_preparation_applicability(record, scope, target)  # type: ignore[arg-type]
    elif action is RECOVERY_ACTION:
        outcome = validate_recovery_applicability(record, scope)  # type: ignore[arg-type]
    else:
        if not isinstance(record, AuthorizationRecordV2) or not isinstance(
            record.scope, DependencyProofInvalidationScopeV1
        ):
            outcome = ResolutionOutcome.WRONG_SCOPE
        elif record.scope != scope:
            outcome = ResolutionOutcome.WRONG_SCOPE
        else:
            try:
                _verify_decision_provenance(target, record.decision_provenance_ref, record.scope)
            except AuthorizationError:
                outcome = ResolutionOutcome.CORRUPT_CONFLICT
            else:
                outcome = ResolutionOutcome.AUTHORIZED
    return ResolutionResultV1(outcome, record)


__all__ = [
    "AuthorizationError",
    "AuthorizationAction",
    "ResolutionOutcome",
    "AuthorizationScope",
    "PreparationScopeV1",
    "PreparationScopeV2",
    "RecoveryScopeV1",
    "DependencyProofInvalidationScopeV1",
    "AuthorizationRecordV1",
    "AuthorizationRecordV2",
    "ResolutionResultV1",
    "authorization_store_path",
    "issue_authorization",
    "issue_preparation_authorization",
    "issue_recovery_authorization",
    "resolve_authorization",
    "validate_preparation_applicability",
    "validate_recovery_applicability",
    "encode_authorization_record",
    "decode_authorization_record",
]
