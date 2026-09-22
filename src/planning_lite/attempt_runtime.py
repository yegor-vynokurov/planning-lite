"""Authoritative PL09 Attempt Runtime persistence and access boundary.

This module is the sole owner of the target-local Attempt Runtime store.  It
validates the existing PL08 Attempt/ObservedResult contracts, resolves the
closed owner-authorization capability, and performs the bounded
``ACTIVATABLE -> IN_FLIGHT -> TERMINAL`` state transitions.  It deliberately
does not issue authorization, execute work, select guidance, or persist
lifecycle state.

All mutations use the same crash-conscious protocol:
``prepare -> validate -> replace -> verify -> hash``.  Reads never create a
missing store, and every rejected or corrupt input fails closed.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from contextlib import contextmanager
from dataclasses import dataclass, replace
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import threading
from typing import Any, BinaryIO

from .attempt_evaluation import (
    AttemptEvaluationError,
    AttemptRecordV1,
    CandidateIdentityV1,
    DirtyPathEntryV1,
    IdentityRefV1,
    ObservedResultV1,
    VerifierContractIdentity,
    allocate_attempt_ordinal,
    canonical_json_bytes,
)
from .authorization import (
    AuthorizationAction,
    PreparationScopeV1,
    RecoveryScopeV1,
    ResolutionOutcome as AuthorizationResolutionOutcome,
    resolve_authorization,
)
from .workspace import WorkspaceError, load_effective_policy


SCHEMA_VERSION = 1
RUNTIME_STATES = frozenset({"ACTIVATABLE", "IN_FLIGHT", "TERMINAL"})
TERMINAL_STATUSES = frozenset({"COMPLETED", "FAILED", "INTERRUPTED", "INVALID"})
ATTEMPT_ID_PATTERN = re.compile(r"[^/\s]+/[^/\s]+/A[1-9][0-9]*\Z")
AUTHORIZATION_REF_PATTERN = re.compile(r"authz_[0-9a-f]{32}\Z")

STORE_KEYS = frozenset({"schema_version", "attempts"})
ENVELOPE_KEYS = frozenset(
    {"attempt", "runtime_state", "observed_result", "recovery_authorization_ref"}
)
ATTEMPT_KEYS = frozenset(
    {
        "schema_version",
        "attempt_id",
        "change_id",
        "task_or_operation_id",
        "attempt_ordinal",
        "authorization_ref",
        "acceptance_contract_ref",
        "operation_guidance_ref",
        "candidate_identity",
        "baseline_refs",
        "prompt_composition_ref",
        "parent_attempt_ref",
        "addresses_finding_refs",
        "observed_result_ref",
        "verifier_contract_refs",
    }
)
OBSERVED_RESULT_KEYS = frozenset(
    {
        "schema_version",
        "result_id",
        "attempt_id",
        "execution_status",
        "changed_paths",
        "fact_refs",
        "artifact_refs",
    }
)

ReplacementHook = Callable[[str], None]


class AttemptRuntimeError(ValueError):
    """Fail-closed runtime, codec, authorization, or storage error."""


class AttemptStoreCorruptError(AttemptRuntimeError):
    """The authoritative store cannot be decoded as one valid document."""


class AttemptNotFoundError(AttemptRuntimeError):
    """An exact Attempt or required authoritative store was not found."""


class AttemptStateError(AttemptRuntimeError):
    """A requested state transition is not admissible for the exact Attempt."""


class AttemptAuthorizationError(AttemptRuntimeError):
    """The supplied authorization is not applicable to the requested action."""


class LookupOutcome(str, Enum):
    FOUND = "FOUND"
    NOT_FOUND = "NOT_FOUND"
    INVALID_ID = "INVALID_ID"
    CORRUPT_CONFLICT = "CORRUPT_CONFLICT"


class AdmissibilityOutcome(str, Enum):
    ADMISSIBLE = "ADMISSIBLE"
    INVALID_ID = "INVALID_ID"
    NOT_FOUND = "NOT_FOUND"
    CORRUPT_CONFLICT = "CORRUPT_CONFLICT"
    INVALID_RECORD = "INVALID_RECORD"
    IN_FLIGHT = "IN_FLIGHT"
    TERMINAL = "TERMINAL"


@dataclass(frozen=True, slots=True)
class AttemptEnvelopeV1:
    """One persisted Attempt, its runtime state, and its terminal fact.

    ``attempt`` carries immutable materialization provenance.  A terminal
    transition adds the exact same-Attempt ``observed_result`` and updates the
    record's terminal-fact reference; recovery additionally persists the exact
    owner authorization reference beside that fact.
    """

    attempt: AttemptRecordV1
    runtime_state: str
    observed_result: ObservedResultV1 | None = None
    recovery_authorization_ref: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.attempt, AttemptRecordV1):
            raise AttemptRuntimeError("attempt envelope requires AttemptRecordV1")
        if self.runtime_state not in RUNTIME_STATES:
            raise AttemptRuntimeError("runtime_state is unsupported")
        if self.runtime_state == "TERMINAL":
            if not isinstance(self.observed_result, ObservedResultV1):
                raise AttemptRuntimeError("TERMINAL requires an ObservedResultV1")
            if self.observed_result.attempt_id != self.attempt.attempt_id:
                raise AttemptRuntimeError("terminal result belongs to another Attempt")
            if self.observed_result.execution_status not in TERMINAL_STATUSES:
                raise AttemptRuntimeError("terminal result status is unsupported")
            if self.attempt.observed_result_ref != self.observed_result.result_id:
                raise AttemptRuntimeError("terminal result reference is inconsistent")
        else:
            if self.observed_result is not None:
                raise AttemptRuntimeError("non-terminal Attempt cannot carry a result")
            if self.attempt.observed_result_ref is not None:
                raise AttemptRuntimeError("non-terminal Attempt cannot reference a result")
            if self.recovery_authorization_ref is not None:
                raise AttemptRuntimeError("non-terminal Attempt cannot carry recovery authority")
        if self.recovery_authorization_ref is not None and not AUTHORIZATION_REF_PATTERN.fullmatch(
            self.recovery_authorization_ref
        ):
            raise AttemptRuntimeError("recovery_authorization_ref is malformed")

    @property
    def attempt_id(self) -> str:
        return self.attempt.attempt_id

    @property
    def authorization_ref(self) -> str:
        return self.attempt.authorization_ref

    def to_mapping(self) -> dict[str, Any]:
        return {
            "attempt": self.attempt.to_mapping(),
            "runtime_state": self.runtime_state,
            "observed_result": self.observed_result.to_mapping() if self.observed_result else None,
            "recovery_authorization_ref": self.recovery_authorization_ref,
        }


@dataclass(frozen=True, slots=True)
class AttemptStoreV1:
    """The one canonical target-local Attempt Runtime document."""

    attempts: tuple[AttemptEnvelopeV1, ...] = ()
    schema_version: int = SCHEMA_VERSION

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise AttemptRuntimeError("unsupported Attempt Runtime schema_version")
        rows = tuple(self.attempts)
        if any(not isinstance(item, AttemptEnvelopeV1) for item in rows):
            raise AttemptRuntimeError("Attempt store contains an invalid envelope")
        ids = [item.attempt_id for item in rows]
        if len(set(ids)) != len(ids):
            raise AttemptStoreCorruptError("Attempt store contains duplicate Attempt identities")
        if ids != sorted(ids):
            raise AttemptStoreCorruptError("Attempt store records are not canonically ordered")
        object.__setattr__(self, "attempts", rows)

    def to_mapping(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "attempts": [item.to_mapping() for item in self.attempts],
        }

    def by_id(self, attempt_id: str) -> AttemptEnvelopeV1 | None:
        return next((item for item in self.attempts if item.attempt_id == attempt_id), None)


@dataclass(frozen=True, slots=True)
class AttemptLookupResultV1:
    """Exact lookup result; no fallback or reconstructed record is exposed."""

    outcome: LookupOutcome
    envelope: AttemptEnvelopeV1 | None = None

    @property
    def attempt(self) -> AttemptRecordV1 | None:
        return self.envelope.attempt if self.envelope else None

    @property
    def runtime_state(self) -> str | None:
        return self.envelope.runtime_state if self.envelope else None

    def to_mapping(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome.value,
            "attempt": self.envelope.to_mapping() if self.envelope else None,
        }


@dataclass(frozen=True, slots=True)
class AttemptAdmissibilityResultV1:
    """Pure state predicate result for one exact Attempt identity."""

    outcome: AdmissibilityOutcome
    envelope: AttemptEnvelopeV1 | None = None

    @property
    def admissible(self) -> bool:
        return self.outcome is AdmissibilityOutcome.ADMISSIBLE

    def to_mapping(self) -> dict[str, Any]:
        return {
            "outcome": self.outcome.value,
            "attempt": self.envelope.to_mapping() if self.envelope else None,
        }


@dataclass(frozen=True, slots=True)
class MutationEvidenceV1:
    """Non-authoritative evidence returned after a verified store mutation."""

    store_path: str
    store_sha256: str
    attempt_id: str
    runtime_state: str

    def to_mapping(self) -> dict[str, str]:
        return {
            "store_path": self.store_path,
            "store_sha256": self.store_sha256,
            "attempt_id": self.attempt_id,
            "runtime_state": self.runtime_state,
        }


_THREAD_LOCKS: dict[Path, threading.RLock] = {}
_THREAD_LOCKS_GUARD = threading.Lock()


def _thread_lock_for(path: Path) -> threading.RLock:
    key = path.resolve()
    with _THREAD_LOCKS_GUARD:
        return _THREAD_LOCKS.setdefault(key, threading.RLock())


def _canonical_bytes(value: Mapping[str, Any]) -> bytes:
    try:
        return canonical_json_bytes(value) + b"\n"
    except AttemptEvaluationError as exc:
        raise AttemptRuntimeError("Attempt Runtime value is not canonical JSON") from exc


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AttemptStoreCorruptError(f"duplicate JSON member: {key}")
        result[key] = value
    return result


def _strict_json(raw: bytes) -> Mapping[str, Any]:
    if not raw.endswith(b"\n") or raw.endswith(b"\n\n"):
        raise AttemptStoreCorruptError("authoritative store must end with exactly one LF")
    try:
        text = raw[:-1].decode("utf-8")
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                AttemptStoreCorruptError(f"non-finite JSON constant: {value}")
            ),
        )
    except AttemptStoreCorruptError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError, TypeError, ValueError) as exc:
        raise AttemptStoreCorruptError("authoritative store is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("authoritative store must be a JSON object")
    return value


def _keys(value: Mapping[str, Any], expected: frozenset[str], label: str) -> None:
    if set(value) != expected:
        raise AttemptStoreCorruptError(f"{label} has an unexpected key set")


def _version(value: Mapping[str, Any], label: str) -> None:
    if value.get("schema_version") != SCHEMA_VERSION:
        raise AttemptStoreCorruptError(f"{label} has an unsupported schema_version")


def _text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or value != value.strip() or "\r" in value or "\n" in value:
        raise AttemptStoreCorruptError(f"{label} must be a non-empty stripped string")
    return value


def _optional_text(value: object, label: str) -> str | None:
    if value is None:
        return None
    return _text(value, label)


def _dirty_path_from_mapping(value: object) -> DirtyPathEntryV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("dirty manifest entry must be an object")
    _keys(value, frozenset({"path", "change_kind", "content_identity", "source_path"}), "dirty manifest entry")
    identity = value.get("content_identity")
    if not isinstance(identity, Mapping):
        raise AttemptStoreCorruptError("dirty path content_identity must be an object")
    _keys(identity, frozenset({"before", "after"}), "dirty path content_identity")
    try:
        return DirtyPathEntryV1(
            value["path"],
            value["change_kind"],
            identity["before"],
            identity["after"],
            value["source_path"],
        )
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("dirty manifest entry is invalid") from exc


def _candidate_from_mapping(value: object) -> CandidateIdentityV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("candidate_identity must be an object")
    _keys(value, frozenset({"kind", "head", "dirty_manifest"}), "candidate_identity")
    manifest = value.get("dirty_manifest")
    if not isinstance(manifest, list):
        raise AttemptStoreCorruptError("candidate dirty_manifest must be a list")
    try:
        return CandidateIdentityV1(value["kind"], value["head"], tuple(_dirty_path_from_mapping(item) for item in manifest))
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("candidate_identity is invalid") from exc


def _identity_ref_from_mapping(value: object) -> IdentityRefV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("baseline reference must be an object")
    if set(value) != {"ref", "identity"}:
        raise AttemptStoreCorruptError("baseline reference has an unexpected key set")
    try:
        return IdentityRefV1(value["ref"], value["identity"])
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("baseline reference is invalid") from exc


def _attempt_from_mapping(value: object, *, require_authorization_pattern: bool = True) -> AttemptRecordV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("attempt must be an object")
    _keys(value, ATTEMPT_KEYS, "attempt")
    _version(value, "attempt")
    baseline = value.get("baseline_refs")
    findings = value.get("addresses_finding_refs")
    verifier_refs = value.get("verifier_contract_refs")
    if not isinstance(baseline, list) or not isinstance(findings, list) or not isinstance(verifier_refs, list):
        raise AttemptStoreCorruptError("attempt sequence fields are invalid")
    raw_verifier: list[VerifierContractIdentity] = []
    for item in verifier_refs:
        if not isinstance(item, Mapping) or set(item) != {"contract_id", "contract_version_or_ref"}:
            raise AttemptStoreCorruptError("verifier contract identity is invalid")
        raw_verifier.append((_text(item["contract_id"], "contract_id"), _text(item["contract_version_or_ref"], "contract_version_or_ref")))
    authorization_ref = value.get("authorization_ref")
    if require_authorization_pattern and (
        not isinstance(authorization_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(authorization_ref)
    ):
        raise AttemptStoreCorruptError("attempt authorization_ref is malformed")
    try:
        return AttemptRecordV1(
            value["attempt_id"],
            value["change_id"],
            value["task_or_operation_id"],
            value["attempt_ordinal"],
            authorization_ref,
            value["acceptance_contract_ref"],
            _candidate_from_mapping(value["candidate_identity"]),
            tuple(_identity_ref_from_mapping(item) for item in baseline),
            value["operation_guidance_ref"],
            value["prompt_composition_ref"],
            value["parent_attempt_ref"],
            tuple(findings),
            value["observed_result_ref"],
            tuple(raw_verifier),
        )
    except (AttemptEvaluationError, TypeError, KeyError) as exc:
        raise AttemptStoreCorruptError("attempt record is invalid") from exc


def _observed_result_from_mapping(value: object) -> ObservedResultV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("observed_result must be an object")
    _keys(value, OBSERVED_RESULT_KEYS, "observed_result")
    _version(value, "observed_result")
    changed = value.get("changed_paths")
    facts = value.get("fact_refs")
    artifacts = value.get("artifact_refs")
    if not isinstance(changed, list) or not isinstance(facts, list) or not isinstance(artifacts, list):
        raise AttemptStoreCorruptError("observed result sequence fields are invalid")
    try:
        return ObservedResultV1(
            value["result_id"],
            value["attempt_id"],
            value["execution_status"],
            tuple(changed),
            tuple(facts),
            tuple(artifacts),
        )
    except (AttemptEvaluationError, TypeError) as exc:
        raise AttemptStoreCorruptError("observed result is invalid") from exc


def _envelope_from_mapping(value: object) -> AttemptEnvelopeV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("Attempt envelope must be an object")
    _keys(value, ENVELOPE_KEYS, "Attempt envelope")
    attempt = _attempt_from_mapping(value["attempt"])
    raw_result = value["observed_result"]
    result = None if raw_result is None else _observed_result_from_mapping(raw_result)
    recovery_ref = value["recovery_authorization_ref"]
    if recovery_ref is not None and (
        not isinstance(recovery_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(recovery_ref)
    ):
        raise AttemptStoreCorruptError("recovery authorization reference is malformed")
    try:
        return AttemptEnvelopeV1(attempt, value["runtime_state"], result, recovery_ref)
    except AttemptRuntimeError as exc:
        raise AttemptStoreCorruptError("Attempt envelope is inconsistent") from exc


def _store_from_mapping(value: object) -> AttemptStoreV1:
    if not isinstance(value, Mapping):
        raise AttemptStoreCorruptError("Attempt store must be an object")
    _keys(value, STORE_KEYS, "Attempt store")
    _version(value, "Attempt store")
    raw_attempts = value.get("attempts")
    if not isinstance(raw_attempts, list):
        raise AttemptStoreCorruptError("Attempt store attempts must be a list")
    try:
        return AttemptStoreV1(tuple(_envelope_from_mapping(item) for item in raw_attempts))
    except AttemptStoreCorruptError:
        raise
    except AttemptRuntimeError as exc:
        raise AttemptStoreCorruptError("Attempt store is inconsistent") from exc


def encode_attempt_store(store: AttemptStoreV1 | Mapping[str, Any]) -> bytes:
    """Strictly canonical-encode one complete Attempt Runtime document."""

    candidate = store if isinstance(store, AttemptStoreV1) else _store_from_mapping(store)
    raw = _canonical_bytes(candidate.to_mapping())
    # Re-decode the exact bytes so public encoding never produces an invalid
    # authoritative document, even when a future contract field is added.
    decoded = decode_attempt_store(raw)
    if decoded.to_mapping() != candidate.to_mapping():
        raise AttemptRuntimeError("Attempt store canonical round-trip changed the document")
    return raw


def decode_attempt_store(raw: bytes | bytearray | str | os.PathLike[str] | Path) -> AttemptStoreV1:
    """Strictly decode canonical store bytes, rejecting duplicates and drift."""

    if isinstance(raw, (str, os.PathLike, Path)):
        try:
            raw_bytes = Path(raw).read_bytes()
        except OSError as exc:
            raise AttemptStoreCorruptError("cannot read Attempt Runtime store") from exc
    elif isinstance(raw, (bytes, bytearray)):
        raw_bytes = bytes(raw)
    else:
        raise AttemptStoreCorruptError("Attempt Runtime input must be bytes or a path")
    value = _strict_json(raw_bytes)
    store = _store_from_mapping(value)
    if _canonical_bytes(store.to_mapping()) != raw_bytes:
        raise AttemptStoreCorruptError("Attempt Runtime store is not canonical")
    return store


def attempt_store_path(target: str | os.PathLike[str] | Path) -> Path:
    """Resolve the one target-local store through effective project policy."""

    product_root = Path(target).expanduser().resolve()
    try:
        effective = load_effective_policy(product_root)
        policy = effective["project_policy"]
        planning_root = policy["planning_root"]
        if not isinstance(planning_root, str) or not planning_root:
            raise WorkspaceError("effective planning_root is invalid")
        path = (product_root / planning_root / "changes" / "active" / ".planning-lite" / "attempt-runtime.json").resolve()
        if not path.is_relative_to(product_root):
            raise WorkspaceError("Attempt Runtime store escapes product root")
        return path
    except (WorkspaceError, KeyError, TypeError) as exc:
        raise AttemptRuntimeError("cannot resolve effective Attempt Runtime store path") from exc


runtime_store_path = attempt_store_path


def _lock_path(store: Path) -> Path:
    return store.with_name(f"{store.name}.lock")


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


@contextmanager
def _store_lock(store: Path, *, create: bool):
    """Hold the in-process and OS lock for the full mutation sequence.

    The sidecar is intentionally not a runtime state or a second store.  Its
    OS lock is held through replacement and reread so a process loss leaves
    the durable state exactly where the completed atomic replacement left it.
    """

    parent = store.parent
    if create:
        parent.mkdir(parents=True, exist_ok=True)
    elif not parent.is_dir():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    lock_path = _lock_path(store)
    with _thread_lock_for(store):
        handle: BinaryIO | None = None
        acquired = False
        try:
            handle = lock_path.open("a+b")
            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"\0")
                handle.flush()
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            acquired = True
            yield
        except (ImportError, OSError) as exc:
            if not acquired:
                raise AttemptRuntimeError(f"cannot acquire Attempt Runtime lock: {lock_path}") from exc
            raise AttemptRuntimeError("Attempt Runtime lock or mutation failed") from exc
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


def _run_hook(hook: ReplacementHook | None, phase: str) -> None:
    if hook is not None:
        hook(phase)


def _safe_replace(
    store: Path,
    proposed: AttemptStoreV1,
    *,
    hook: ReplacementHook | None = None,
) -> MutationEvidenceV1:
    """Publish one complete validated document without destructive truncation."""

    raw = encode_attempt_store(proposed)
    temporary: Path | None = None
    try:
        _run_hook(hook, "prepare")
        with tempfile.NamedTemporaryFile(mode="wb", dir=store.parent, prefix=".attempt-runtime-", suffix=".tmp", delete=False) as handle:
            temporary = Path(handle.name)
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        _run_hook(hook, "validate")
        validated = decode_attempt_store(raw)
        if validated.to_mapping() != proposed.to_mapping():
            raise AttemptRuntimeError("prepared Attempt Runtime bytes changed during validation")
        _run_hook(hook, "replace")
        os.replace(temporary, store)
        temporary = None
        _fsync_directory(store.parent)
        _run_hook(hook, "verify")
        verified_raw = store.read_bytes()
        verified = decode_attempt_store(verified_raw)
        if verified.to_mapping() != proposed.to_mapping() or verified_raw != raw:
            raise AttemptRuntimeError("verified Attempt Runtime bytes do not match the intended document")
        digest = hashlib.sha256(verified_raw).hexdigest()
        _run_hook(hook, "hash")
        changed = proposed.attempts[-1] if proposed.attempts else None
        if changed is None:
            raise AttemptRuntimeError("Attempt Runtime mutation has no resulting Attempt")
        return MutationEvidenceV1(str(store), digest, changed.attempt_id, changed.runtime_state)
    except AttemptRuntimeError:
        raise
    except (OSError, ValueError, TypeError) as exc:
        raise AttemptRuntimeError("Attempt Runtime safe replacement failed") from exc
    except Exception as exc:
        raise AttemptRuntimeError("Attempt Runtime safe replacement failed") from exc
    finally:
        if temporary is not None:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass


def _read_store(store: Path) -> AttemptStoreV1:
    if not store.exists():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    try:
        raw = store.read_bytes()
    except OSError as exc:
        raise AttemptStoreCorruptError("cannot read Attempt Runtime store") from exc
    return decode_attempt_store(raw)


def _read_store_or_empty(store: Path) -> AttemptStoreV1:
    if not store.exists():
        return AttemptStoreV1()
    return _read_store(store)


def _exact_id(attempt_id: object) -> str:
    if not isinstance(attempt_id, str) or not ATTEMPT_ID_PATTERN.fullmatch(attempt_id):
        raise AttemptRuntimeError("INVALID_ID")
    return attempt_id


def _auth_or_raise(target: Path, authorization_ref: str, action: AuthorizationAction, scope: object) -> None:
    result = resolve_authorization(target, authorization_ref, action, scope)  # type: ignore[arg-type]
    if result.outcome is not AuthorizationResolutionOutcome.AUTHORIZED or result.record is None:
        raise AttemptAuthorizationError(f"authorization rejected: {result.outcome.value}")
    if result.record.decision_outcome != "AUTHORIZED":
        raise AttemptAuthorizationError("authorization decision is not AUTHORIZED")


def _payload_mapping(preparation: Mapping[str, Any] | bytes | str | os.PathLike[str] | Path | None) -> dict[str, Any]:
    if preparation is None:
        return {}
    if isinstance(preparation, Mapping):
        return dict(preparation)
    if isinstance(preparation, (str, os.PathLike, Path)):
        try:
            raw = Path(preparation).read_bytes()
        except OSError as exc:
            raise AttemptRuntimeError("cannot read preparation input") from exc
    elif isinstance(preparation, bytes):
        raw = preparation
    else:
        raise AttemptRuntimeError("preparation input must be a mapping, JSON bytes, or a path")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_reject_duplicate_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as exc:
        raise AttemptRuntimeError("preparation input is not valid JSON") from exc
    if not isinstance(value, Mapping):
        raise AttemptRuntimeError("preparation input must be a JSON object")
    return dict(value)


def _merge_preparation_fields(
    preparation: Mapping[str, Any] | bytes | str | os.PathLike[str] | Path | None,
    overrides: Mapping[str, Any],
) -> dict[str, Any]:
    data = _payload_mapping(preparation)
    nested = data.get("attempt") or data.get("attempt_record")
    if nested is not None:
        if not isinstance(nested, Mapping):
            raise AttemptRuntimeError("preparation attempt payload must be an object")
        merged = dict(nested)
        merged.update({key: value for key, value in data.items() if key not in {"attempt", "attempt_record"}})
        data = merged
    for key, value in overrides.items():
        if value is not None:
            data[key] = value
    return data


def _candidate_from_payload(value: object) -> CandidateIdentityV1:
    return _candidate_from_mapping(value)


def _baseline_from_payload(value: object) -> tuple[IdentityRefV1, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)) or not value:
        raise AttemptRuntimeError("baseline_refs must be a non-empty list")
    try:
        return tuple(_identity_ref_from_mapping(item) for item in value)
    except AttemptStoreCorruptError as exc:
        raise AttemptRuntimeError("baseline_refs are invalid") from exc


def _build_attempt(
    data: Mapping[str, Any],
    *,
    ordinal: int,
    existing: Sequence[AttemptEnvelopeV1],
) -> AttemptRecordV1:
    required = ("change_id", "task_or_operation_id", "authorization_ref", "acceptance_contract_ref", "candidate_identity", "baseline_refs")
    missing = [key for key in required if key not in data]
    if missing:
        raise AttemptRuntimeError(f"preparation input is missing: {', '.join(missing)}")
    change_id = _text(data["change_id"], "change_id")
    task_id = _text(data["task_or_operation_id"], "task_or_operation_id")
    auth_ref = data["authorization_ref"]
    if not isinstance(auth_ref, str) or not AUTHORIZATION_REF_PATTERN.fullmatch(auth_ref):
        raise AttemptRuntimeError("authorization_ref is malformed")
    candidate = _candidate_from_payload(data["candidate_identity"])
    baseline = _baseline_from_payload(data["baseline_refs"])
    findings = data.get("addresses_finding_refs", [])
    verifier_values = data.get("verifier_contract_refs", [])
    if not isinstance(findings, Sequence) or isinstance(findings, (str, bytes)):
        raise AttemptRuntimeError("addresses_finding_refs must be a list")
    if not isinstance(verifier_values, Sequence) or isinstance(verifier_values, (str, bytes)):
        raise AttemptRuntimeError("verifier_contract_refs must be a list")
    verifier_contracts: list[VerifierContractIdentity] = []
    for item in verifier_values:
        if not isinstance(item, Mapping) or set(item) != {"contract_id", "contract_version_or_ref"}:
            raise AttemptRuntimeError("verifier_contract_refs contains an invalid identity")
        verifier_contracts.append(
            (_text(item["contract_id"], "contract_id"), _text(item["contract_version_or_ref"], "contract_version_or_ref"))
        )
    try:
        attempt = AttemptRecordV1(
            f"{change_id}/{task_id}/A{ordinal}",
            change_id,
            task_id,
            ordinal,
            auth_ref,
            _text(data["acceptance_contract_ref"], "acceptance_contract_ref"),
            candidate,
            baseline,
            _optional_text(data.get("operation_guidance_ref"), "operation_guidance_ref"),
            _optional_text(data.get("prompt_composition_ref"), "prompt_composition_ref"),
            _optional_text(data.get("parent_attempt_ref"), "parent_attempt_ref"),
            tuple(findings),
            None,
            tuple(verifier_contracts),
        )
    except (AttemptEvaluationError, TypeError, KeyError) as exc:
        raise AttemptRuntimeError("preparation Attempt input is invalid") from exc
    parent_id = attempt.parent_attempt_ref
    if parent_id is not None:
        parent = next((row.attempt for row in existing if row.attempt_id == parent_id), None)
        if parent is None or (parent.change_id, parent.task_or_operation_id) != (change_id, task_id):
            raise AttemptRuntimeError("parent Attempt is absent or crosses Change/task scope")
    return attempt


def prepare_attempt(
    target: str | os.PathLike[str] | Path,
    preparation: Mapping[str, Any] | bytes | str | os.PathLike[str] | Path | None = None,
    *,
    authorization_ref: str | None = None,
    change_id: str | None = None,
    task_or_operation_id: str | None = None,
    acceptance_contract_ref: str | None = None,
    candidate_identity: Mapping[str, Any] | None = None,
    baseline_refs: Sequence[Mapping[str, Any]] | None = None,
    operation_guidance_ref: str | None = None,
    prompt_composition_ref: str | None = None,
    parent_attempt_ref: str | None = None,
    addresses_finding_refs: Sequence[str] | None = None,
    verifier_contract_refs: Sequence[Mapping[str, str]] | None = None,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1:
    """Materialize exactly one authorized ``ACTIVATABLE`` Attempt.

    Authorization is resolved before creating runtime state.  Lineage and
    ordinal allocation happen under the Attempt-store lock, so a reused
    preparation reference or concurrent same-scope preparation cannot create a
    second occurrence.
    """

    overrides = {
        "authorization_ref": authorization_ref,
        "change_id": change_id,
        "task_or_operation_id": task_or_operation_id,
        "acceptance_contract_ref": acceptance_contract_ref,
        "candidate_identity": candidate_identity,
        "baseline_refs": baseline_refs,
        "operation_guidance_ref": operation_guidance_ref,
        "prompt_composition_ref": prompt_composition_ref,
        "parent_attempt_ref": parent_attempt_ref,
        "addresses_finding_refs": addresses_finding_refs,
        "verifier_contract_refs": verifier_contract_refs,
    }
    data = _merge_preparation_fields(preparation, overrides)
    required = ("authorization_ref", "change_id", "task_or_operation_id")
    if any(key not in data for key in required):
        raise AttemptRuntimeError("preparation input lacks authorization and exact Change/task scope")
    change = _text(data["change_id"], "change_id")
    task = _text(data["task_or_operation_id"], "task_or_operation_id")
    auth_ref = data["authorization_ref"]
    if not isinstance(auth_ref, str):
        raise AttemptRuntimeError("authorization_ref is malformed")
    product_root = Path(target).expanduser().resolve()
    _auth_or_raise(
        product_root,
        auth_ref,
        AuthorizationAction.PREPARATION,
        PreparationScopeV1(change, task),
    )
    store = attempt_store_path(product_root)
    with _store_lock(store, create=True):
        current = _read_store_or_empty(store)
        if any(row.authorization_ref == auth_ref for row in current.attempts):
            raise AttemptAuthorizationError("preparation authorization has already materialized an Attempt")
        lineage = sorted(
            (row.attempt for row in current.attempts if row.attempt.change_id == change and row.attempt.task_or_operation_id == task),
            key=lambda row: row.attempt_ordinal,
        )
        try:
            ordinal = allocate_attempt_ordinal(lineage, change_id=change, task_or_operation_id=task)
        except AttemptEvaluationError as exc:
            raise AttemptRuntimeError("authoritative Attempt lineage is invalid") from exc
        attempt = _build_attempt(data, ordinal=ordinal, existing=current.attempts)
        envelope = AttemptEnvelopeV1(attempt, "ACTIVATABLE")
        proposed = AttemptStoreV1(tuple(sorted((*current.attempts, envelope), key=lambda row: row.attempt_id)))
        _safe_replace(store, proposed, hook=fault_hook)
        verified = _read_store(store).by_id(attempt.attempt_id)
        if verified is None:
            raise AttemptRuntimeError("materialized Attempt disappeared during verification")
        return verified


materialize_attempt = prepare_attempt


def lookup_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
) -> AttemptLookupResultV1:
    """Return one exact authoritative lookup outcome without creating state."""

    if not isinstance(attempt_id, str) or not ATTEMPT_ID_PATTERN.fullmatch(attempt_id):
        return AttemptLookupResultV1(LookupOutcome.INVALID_ID)
    store = attempt_store_path(target)
    if not store.exists():
        return AttemptLookupResultV1(LookupOutcome.NOT_FOUND)
    try:
        record = _read_store(store).by_id(attempt_id)
    except AttemptRuntimeError:
        return AttemptLookupResultV1(LookupOutcome.CORRUPT_CONFLICT)
    return AttemptLookupResultV1(
        LookupOutcome.FOUND if record is not None else LookupOutcome.NOT_FOUND,
        record,
    )


def exact_lookup(target: str | os.PathLike[str] | Path, attempt_id: str) -> AttemptLookupResultV1:
    """Alias for the exact lookup application seam."""

    return lookup_attempt(target, attempt_id)


def check_activation_admissibility(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
) -> AttemptAdmissibilityResultV1:
    """Purely report whether one authoritative Attempt is ``ACTIVATABLE``."""

    if not isinstance(attempt_id, str) or not ATTEMPT_ID_PATTERN.fullmatch(attempt_id):
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.INVALID_ID)
    store = attempt_store_path(target)
    if not store.exists():
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.NOT_FOUND)
    try:
        envelope = _read_store(store).by_id(attempt_id)
    except AttemptRuntimeError:
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.CORRUPT_CONFLICT)
    if envelope is None:
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.NOT_FOUND)
    if envelope.runtime_state == "ACTIVATABLE":
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.ADMISSIBLE, envelope)
    if envelope.runtime_state == "IN_FLIGHT":
        return AttemptAdmissibilityResultV1(AdmissibilityOutcome.IN_FLIGHT, envelope)
    return AttemptAdmissibilityResultV1(AdmissibilityOutcome.TERMINAL, envelope)


def _required_store_for_mutation(target: str | os.PathLike[str] | Path) -> tuple[Path, AttemptStoreV1]:
    store = attempt_store_path(target)
    if not store.exists():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    return store, _read_store(store)


def claim_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
    *,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1:
    """Atomically claim one exact ``ACTIVATABLE`` Attempt as ``IN_FLIGHT``."""

    _exact_id(attempt_id)
    store = attempt_store_path(target)
    if not store.exists():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    with _store_lock(store, create=False):
        current = _read_store(store)
        row = current.by_id(attempt_id)
        if row is None:
            raise AttemptNotFoundError("Attempt is not found")
        if row.runtime_state != "ACTIVATABLE":
            raise AttemptStateError(f"Attempt cannot be claimed from {row.runtime_state}")
        claimed = replace(row, runtime_state="IN_FLIGHT")
        proposed = AttemptStoreV1(tuple(sorted((claimed if item.attempt_id == attempt_id else item for item in current.attempts), key=lambda item: item.attempt_id)))
        _safe_replace(store, proposed, hook=fault_hook)
        verified = _read_store(store).by_id(attempt_id)
        if verified is None or verified.runtime_state != "IN_FLIGHT":
            raise AttemptRuntimeError("claimed Attempt failed authoritative verification")
        return verified


def _result_from_input(value: ObservedResultV1 | Mapping[str, Any]) -> ObservedResultV1:
    if isinstance(value, ObservedResultV1):
        return value
    return _observed_result_from_mapping(value)


def terminalize_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
    observed_result: ObservedResultV1 | Mapping[str, Any],
    *,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1:
    """Persist one normal irreversible same-Attempt terminal fact.

    Normal terminalization accepts all supported executor statuses and always
    persists null recovery provenance.  In particular, ``INTERRUPTED``
    describes what happened during execution; it is not owner recovery
    authority.  Explicit owner recovery is available only through
    ``resolve_interrupted_attempt``.

    Only ``IN_FLIGHT`` can terminalize.  This performs an authoritative
    prepare, validate, replace, verify, and hash-preserving write; there is no
    reset, retry, rollback, lease, or automatic repair after process loss.
    """

    # INTERRUPTED execution status != owner recovery authority.
    return _terminalize_attempt(
        Path(target).expanduser().resolve(),
        attempt_id,
        observed_result,
        terminal_authorization_ref=None,
        fault_hook=fault_hook,
    )


def _terminalize_attempt(
    target: Path,
    attempt_id: str,
    observed_result: ObservedResultV1 | Mapping[str, Any],
    *,
    terminal_authorization_ref: str | None,
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1:
    """Persist terminal facts after provenance has been selected internally.

    ``terminal_authorization_ref`` may be non-null only for the private owner
    recovery caller, after exact CLOSED Authorization resolution.  Keeping
    this capability out of the public normal-terminalization signature makes
    fabricated recovery provenance fail closed at the public contract.
    """

    _exact_id(attempt_id)
    result = _result_from_input(observed_result)
    if result.attempt_id != attempt_id or result.execution_status not in TERMINAL_STATUSES:
        raise AttemptStateError("terminal fact is wrong-Attempt or unsupported")
    if terminal_authorization_ref is not None and not AUTHORIZATION_REF_PATTERN.fullmatch(terminal_authorization_ref):
        raise AttemptAuthorizationError("recovery authorization reference is malformed")
    store = attempt_store_path(target)
    if not store.exists():
        raise AttemptNotFoundError("Attempt Runtime store is absent")
    with _store_lock(store, create=False):
        current = _read_store(store)
        row = current.by_id(attempt_id)
        if row is None:
            raise AttemptNotFoundError("Attempt is not found")
        if row.runtime_state != "IN_FLIGHT":
            raise AttemptStateError(f"Attempt cannot terminalize from {row.runtime_state}")
        if any(item.observed_result and item.observed_result.result_id == result.result_id for item in current.attempts):
            raise AttemptStateError("terminal result identity is already persisted")
        updated_attempt = replace(row.attempt, observed_result_ref=result.result_id)
        terminal = AttemptEnvelopeV1(
            updated_attempt,
            "TERMINAL",
            result,
            terminal_authorization_ref,
        )
        proposed = AttemptStoreV1(tuple(sorted((terminal if item.attempt_id == attempt_id else item for item in current.attempts), key=lambda item: item.attempt_id)))
        _safe_replace(store, proposed, hook=fault_hook)
        verified = _read_store(store).by_id(attempt_id)
        if verified is None or verified.runtime_state != "TERMINAL":
            raise AttemptRuntimeError("terminal Attempt failed authoritative verification")
        return verified


def resolve_interrupted_attempt(
    target: str | os.PathLike[str] | Path,
    attempt_id: str,
    authorization_ref: str,
    *,
    result_id: str | None = None,
    fact_refs: Sequence[str] = (),
    artifact_refs: Sequence[str] = (),
    fault_hook: ReplacementHook | None = None,
) -> AttemptEnvelopeV1:
    """Resolve one exact in-flight Attempt through owner recovery authority.

    The CLOSED Authorization capability must authorize the exact recovery
    action and Attempt scope before the private terminalization helper may
    persist its verified provenance reference.
    """

    _exact_id(attempt_id)
    if not isinstance(authorization_ref, str):
        raise AttemptAuthorizationError("recovery authorization reference is malformed")
    product_root = Path(target).expanduser().resolve()
    _auth_or_raise(
        product_root,
        authorization_ref,
        AuthorizationAction.RECOVERY,
        RecoveryScopeV1(attempt_id),
    )
    return _terminalize_with_recovery(
        product_root,
        attempt_id,
        authorization_ref,
        result_id=result_id,
        fact_refs=fact_refs,
        artifact_refs=artifact_refs,
        fault_hook=fault_hook,
    )


def _terminalize_with_recovery(
    target: Path,
    attempt_id: str,
    authorization_ref: str,
    *,
    result_id: str | None,
    fact_refs: Sequence[str],
    artifact_refs: Sequence[str],
    fault_hook: ReplacementHook | None,
) -> AttemptEnvelopeV1:
    result = ObservedResultV1(
        result_id or f"recovery:{attempt_id}",
        attempt_id,
        "INTERRUPTED",
        (),
        tuple(fact_refs),
        tuple(artifact_refs),
    )
    return _terminalize_attempt(
        target,
        attempt_id,
        result,
        terminal_authorization_ref=authorization_ref,
        fault_hook=fault_hook,
    )


recover_interrupted_attempt = resolve_interrupted_attempt


def load_attempt_store(target: str | os.PathLike[str] | Path) -> AttemptStoreV1:
    """Read the authoritative store without creating or mutating it."""

    return _read_store(attempt_store_path(target))


def store_sha256(target: str | os.PathLike[str] | Path) -> str:
    """Return evidence hash of the verified canonical store bytes."""

    path = attempt_store_path(target)
    raw = path.read_bytes()
    decode_attempt_store(raw)
    return hashlib.sha256(raw).hexdigest()


__all__ = [
    "AdmissibilityOutcome",
    "AttemptAdmissibilityResultV1",
    "AttemptAuthorizationError",
    "AttemptEnvelopeV1",
    "AttemptLookupResultV1",
    "AttemptNotFoundError",
    "AttemptRuntimeError",
    "AttemptStateError",
    "AttemptStoreCorruptError",
    "AttemptStoreV1",
    "LookupOutcome",
    "MutationEvidenceV1",
    "RUNTIME_STATES",
    "TERMINAL_STATUSES",
    "attempt_store_path",
    "check_activation_admissibility",
    "claim_attempt",
    "decode_attempt_store",
    "encode_attempt_store",
    "exact_lookup",
    "load_attempt_store",
    "lookup_attempt",
    "materialize_attempt",
    "prepare_attempt",
    "recover_interrupted_attempt",
    "resolve_interrupted_attempt",
    "runtime_store_path",
    "store_sha256",
    "terminalize_attempt",
]
