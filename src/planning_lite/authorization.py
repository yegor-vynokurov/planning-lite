"""Bounded owner-issued Attempt action authorizations.

This module is deliberately independent from Attempt Runtime, lifecycle, and
executor code.  It owns one immutable, target-local record source and a pure
resolver for the two v1 action/scope contracts.
"""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
import json
import os
from pathlib import Path
import re
import secrets
import threading
import tempfile
from typing import Literal

from .workspace import WorkspaceError, load_effective_policy


class AuthorizationError(RuntimeError):
    """Fail-closed authorization issuance, decoding, or storage error."""


class AuthorizationAction(str, Enum):
    PREPARATION = "OWNER_AUTHORIZED_ATTEMPT_PREPARATION"
    RECOVERY = "OWNER_AUTHORIZED_INTERRUPTED_ATTEMPT_RESOLUTION"


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
]


@dataclass(frozen=True, slots=True)
class PreparationScopeV1:
    change_id: str
    task_or_operation_id: str


@dataclass(frozen=True, slots=True)
class RecoveryScopeV1:
    attempt_id: str


AuthorizationScope = PreparationScopeV1 | RecoveryScopeV1


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
class ResolutionResultV1:
    outcome: ResolutionOutcome
    record: AuthorizationRecordV1 | None = None


AUTHORIZATION_REF_PATTERN = re.compile(r"authz_[0-9a-f]{32}\Z")
MAX_ALLOCATION_ATTEMPTS = 16
PREPARATION_ACTION = AuthorizationAction.PREPARATION
RECOVERY_ACTION = AuthorizationAction.RECOVERY
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


def _scope_mapping(scope: AuthorizationScope) -> dict[str, str]:
    if isinstance(scope, PreparationScopeV1):
        return {
            "change_id": _identifier(scope.change_id, "change_id"),
            "task_or_operation_id": _identifier(
                scope.task_or_operation_id, "task_or_operation_id"
            ),
        }
    if isinstance(scope, RecoveryScopeV1):
        return {"attempt_id": _identifier(scope.attempt_id, "attempt_id")}
    raise AuthorizationError("scope must be a supported typed authorization scope")


def _expected_authority(action: AuthorizationAction) -> str:
    return PREPARATION_AUTHORITY if action is PREPARATION_ACTION else RECOVERY_AUTHORITY


def _record_mapping(record: AuthorizationRecordV1) -> dict[str, object]:
    action = _action(record.action_type)
    ref = _reference(record.authorization_ref)
    if record.schema_version != 1 or isinstance(record.schema_version, bool):
        raise AuthorizationError("schema_version must be exactly 1")
    if record.decision_outcome != "AUTHORIZED":
        raise AuthorizationError("decision_outcome must be AUTHORIZED")
    provenance = _identifier(record.decision_provenance_ref, "decision_provenance_ref")
    authority = _identifier(record.decision_authority_class, "decision_authority_class")
    if authority != _expected_authority(action):
        raise AuthorizationError("decision_authority_class does not match action")
    if action is PREPARATION_ACTION and not isinstance(record.scope, PreparationScopeV1):
        raise AuthorizationError("preparation action requires PreparationScopeV1")
    if action is RECOVERY_ACTION and not isinstance(record.scope, RecoveryScopeV1):
        raise AuthorizationError("recovery action requires RecoveryScopeV1")
    return {
        "schema_version": 1,
        "authorization_ref": ref,
        "action_type": action.value,
        "scope": _scope_mapping(record.scope),
        "decision_authority_class": authority,
        "decision_outcome": "AUTHORIZED",
        "decision_provenance_ref": provenance,
    }


def encode_authorization_record(record: AuthorizationRecordV1) -> bytes:
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


def _mapping_record(value: object) -> AuthorizationRecordV1:
    if not isinstance(value, dict) or set(value) != TOP_LEVEL_KEYS:
        raise AuthorizationError("authorization record has incorrect top-level keys")
    raw_schema = value["schema_version"]
    if raw_schema != 1 or isinstance(raw_schema, bool):
        raise AuthorizationError("schema_version must be exactly 1")
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
    if action is PREPARATION_ACTION:
        if set(raw_scope) != {"change_id", "task_or_operation_id"}:
            raise AuthorizationError("preparation scope has incorrect keys")
        scope: AuthorizationScope = PreparationScopeV1(
            _identifier(raw_scope["change_id"], "change_id"),
            _identifier(raw_scope["task_or_operation_id"], "task_or_operation_id"),
        )
    else:
        if set(raw_scope) != {"attempt_id"}:
            raise AuthorizationError("recovery scope has incorrect keys")
        scope = RecoveryScopeV1(_identifier(raw_scope["attempt_id"], "attempt_id"))
    if authority != _expected_authority(action):
        raise AuthorizationError("decision_authority_class does not match action")
    return AuthorizationRecordV1(1, ref, action, scope, authority, "AUTHORIZED", provenance)


def decode_authorization_record(raw: bytes) -> AuthorizationRecordV1:
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


def issue_authorization(
    target: str | os.PathLike[str] | Path,
    action_type: AuthorizationAction | AuthorizationActionValue | str,
    scope: AuthorizationScope,
    decision_provenance_ref: str,
) -> str:
    """Issue one immutable authorization and return its opaque reference."""

    action = _action(action_type)
    if action is PREPARATION_ACTION and not isinstance(scope, PreparationScopeV1):
        raise AuthorizationError("preparation action requires PreparationScopeV1")
    if action is RECOVERY_ACTION and not isinstance(scope, RecoveryScopeV1):
        raise AuthorizationError("recovery action requires RecoveryScopeV1")
    provenance = _identifier(decision_provenance_ref, "decision_provenance_ref")
    store = authorization_store_path(target)
    with _thread_lock_for(store):
        store.mkdir(parents=True, exist_ok=True)
        for _ in range(MAX_ALLOCATION_ATTEMPTS):
            ref = _reference(_allocate_authorization_ref())
            record = AuthorizationRecordV1(
                1,
                ref,
                action,
                scope,
                _expected_authority(action),
                "AUTHORIZED",
                provenance,
            )
            raw = encode_authorization_record(record)
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
                    if decoded.authorization_ref != ref or verified != raw:
                        raise AuthorizationError("Published authorization failed byte verification")
                    _fsync_directory(store)
                    return ref
            finally:
                if temporary_path is not None:
                    temporary_path.unlink(missing_ok=True)
        raise AuthorizationError("AUTHORIZATION_REF_ALLOCATION_EXHAUSTED")


def issue_preparation_authorization(
    target: str | os.PathLike[str] | Path,
    change_id: str,
    task_or_operation_id: str,
    decision_provenance_ref: str,
) -> str:
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
    return issue_authorization(
        target,
        RECOVERY_ACTION,
        RecoveryScopeV1(attempt_id),
        decision_provenance_ref,
    )


def validate_preparation_applicability(
    record: AuthorizationRecordV1, scope: PreparationScopeV1
) -> ResolutionOutcome:
    if record.action_type is not PREPARATION_ACTION:
        return ResolutionOutcome.WRONG_ACTION
    if not isinstance(scope, PreparationScopeV1) or not isinstance(record.scope, PreparationScopeV1):
        return ResolutionOutcome.WRONG_SCOPE
    if record.scope != scope:
        return ResolutionOutcome.WRONG_SCOPE
    return ResolutionOutcome.AUTHORIZED


def validate_recovery_applicability(
    record: AuthorizationRecordV1, scope: RecoveryScopeV1
) -> ResolutionOutcome:
    if record.action_type is not RECOVERY_ACTION:
        return ResolutionOutcome.WRONG_ACTION
    if not isinstance(scope, RecoveryScopeV1) or not isinstance(record.scope, RecoveryScopeV1):
        return ResolutionOutcome.WRONG_SCOPE
    if record.scope != scope:
        return ResolutionOutcome.WRONG_SCOPE
    return ResolutionOutcome.AUTHORIZED


def _scan_store(store: Path) -> tuple[dict[str, AuthorizationRecordV1], bool]:
    records: dict[str, AuthorizationRecordV1] = {}
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
    """Resolve one exact authorization without mutating the source."""

    if not isinstance(authorization_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(
        authorization_ref
    ):
        return ResolutionResultV1(ResolutionOutcome.INVALID_REFERENCE)
    try:
        action = _action(action_type)
    except AuthorizationError:
        return ResolutionResultV1(ResolutionOutcome.WRONG_ACTION)
    if action is PREPARATION_ACTION and not isinstance(scope, PreparationScopeV1):
        return ResolutionResultV1(ResolutionOutcome.WRONG_SCOPE)
    if action is RECOVERY_ACTION and not isinstance(scope, RecoveryScopeV1):
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
        outcome = validate_preparation_applicability(record, scope)  # type: ignore[arg-type]
    else:
        outcome = validate_recovery_applicability(record, scope)  # type: ignore[arg-type]
    return ResolutionResultV1(outcome, record if outcome is ResolutionOutcome.AUTHORIZED else record)


__all__ = [
    "AuthorizationError",
    "AuthorizationAction",
    "ResolutionOutcome",
    "PreparationScopeV1",
    "RecoveryScopeV1",
    "AuthorizationRecordV1",
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
