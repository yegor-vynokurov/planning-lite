from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Mapping


CAMPAIGN_SCHEMA_VERSION = 1
JOURNAL_SCHEMA_VERSION = 1
CAMPAIGN_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
EVENT_TYPES = (
    "campaign_initialized",
    "hypothesis_registered",
    "candidate_registered",
    "attempt_started",
    "attempt_completed",
    "attempt_evidence_reconciled",
    "candidate_reviewed",
    "candidate_kept",
    "candidate_rejected",
    "candidate_quarantined",
    "campaign_stopped",
    "campaign_completed",
)
TERMINAL_EVENT_TYPES = {"campaign_stopped", "campaign_completed"}
ALLOWED_TRANSITIONS = {
    "campaign_initialized": {"hypothesis_registered", "campaign_stopped"},
    "hypothesis_registered": {
        "hypothesis_registered",
        "candidate_registered",
        "campaign_stopped",
    },
    "candidate_registered": {
        "attempt_started",
        "candidate_quarantined",
        "campaign_stopped",
    },
    "attempt_started": {"attempt_completed", "campaign_stopped"},
    "attempt_completed": {
        "attempt_started",
        "candidate_reviewed",
        "candidate_kept",
        "candidate_rejected",
        "candidate_quarantined",
        "campaign_stopped",
    },
    "candidate_reviewed": {
        "attempt_started",
        "attempt_evidence_reconciled",
        "candidate_kept",
        "candidate_rejected",
        "candidate_quarantined",
        "campaign_stopped",
    },
    "attempt_evidence_reconciled": {
        "attempt_started",
        "candidate_quarantined",
        "campaign_stopped",
    },
    "candidate_kept": {"campaign_completed", "campaign_stopped"},
    "candidate_rejected": {
        "hypothesis_registered",
        "candidate_registered",
        "campaign_stopped",
    },
    "candidate_quarantined": {
        "hypothesis_registered",
        "candidate_registered",
        "campaign_stopped",
    },
}


class CampaignError(RuntimeError):
    """Raised when campaign state is invalid, mutable, or internally inconsistent."""


@dataclass(frozen=True)
class FrozenParent:
    repository: str
    commit: str
    tag: str | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "FrozenParent":
        repository = _nonempty_string(payload.get("repository"), "frozen_parent.repository")
        commit = _nonempty_string(payload.get("commit"), "frozen_parent.commit")
        tag = payload.get("tag")
        if tag is not None and not isinstance(tag, str):
            raise CampaignError("frozen_parent.tag must be a string or null")
        return cls(repository=repository, commit=commit, tag=tag)


@dataclass(frozen=True)
class FrozenInput:
    input_id: str
    role: str
    path: str
    sha256: str

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "FrozenInput":
        input_id = _nonempty_string(payload.get("input_id"), "frozen_inputs[].input_id")
        role = _nonempty_string(payload.get("role"), "frozen_inputs[].role")
        path = _nonempty_string(payload.get("path"), "frozen_inputs[].path")
        sha256 = _nonempty_string(payload.get("sha256"), "frozen_inputs[].sha256").lower()
        if not SHA256_RE.fullmatch(sha256):
            raise CampaignError(f"Frozen input {input_id!r} has an invalid sha256")
        return cls(input_id=input_id, role=role, path=path, sha256=sha256)


@dataclass(frozen=True)
class CampaignBudget:
    max_candidates: int
    max_attempts_per_candidate: int
    max_total_attempts: int
    max_total_tokens: int | None = None
    max_wall_clock_seconds: float | None = None

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "CampaignBudget":
        max_candidates = _positive_int(payload.get("max_candidates"), "budget.max_candidates")
        max_attempts_per_candidate = _positive_int(
            payload.get("max_attempts_per_candidate"),
            "budget.max_attempts_per_candidate",
        )
        max_total_attempts = _positive_int(
            payload.get("max_total_attempts"), "budget.max_total_attempts"
        )
        max_total_tokens = _optional_positive_int(
            payload.get("max_total_tokens"), "budget.max_total_tokens"
        )
        max_wall_clock_seconds = _optional_positive_number(
            payload.get("max_wall_clock_seconds"),
            "budget.max_wall_clock_seconds",
        )
        return cls(
            max_candidates=max_candidates,
            max_attempts_per_candidate=max_attempts_per_candidate,
            max_total_attempts=max_total_attempts,
            max_total_tokens=max_total_tokens,
            max_wall_clock_seconds=max_wall_clock_seconds,
        )


@dataclass(frozen=True)
class StopPolicy:
    stop_on_hard_gate_failure: bool
    stop_after_accepted_candidate: bool
    max_consecutive_non_improving: int

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "StopPolicy":
        return cls(
            stop_on_hard_gate_failure=_bool(
                payload.get("stop_on_hard_gate_failure"),
                "stop_policy.stop_on_hard_gate_failure",
            ),
            stop_after_accepted_candidate=_bool(
                payload.get("stop_after_accepted_candidate"),
                "stop_policy.stop_after_accepted_candidate",
            ),
            max_consecutive_non_improving=_positive_int(
                payload.get("max_consecutive_non_improving"),
                "stop_policy.max_consecutive_non_improving",
            ),
        )


@dataclass(frozen=True)
class CampaignManifest:
    schema_version: int
    campaign_id: str
    purpose: str
    frozen_parent: FrozenParent
    frozen_inputs: tuple[FrozenInput, ...]
    mutable_scope: tuple[str, ...]
    off_limits: tuple[str, ...]
    budget: CampaignBudget
    stop_policy: StopPolicy
    manifest_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("manifest_sha256", None)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned_dict(), "manifest_sha256": self.manifest_sha256}

    @classmethod
    def from_dict(
        cls,
        payload: Mapping[str, Any],
        *,
        require_hash: bool,
    ) -> "CampaignManifest":
        if payload.get("schema_version") != CAMPAIGN_SCHEMA_VERSION:
            raise CampaignError(
                f"Unsupported campaign manifest schema: {payload.get('schema_version')!r}"
            )
        campaign_id = _nonempty_string(payload.get("campaign_id"), "campaign_id")
        if not CAMPAIGN_ID_RE.fullmatch(campaign_id):
            raise CampaignError(
                "campaign_id must contain only letters, digits, dot, underscore, or hyphen"
            )
        purpose = _nonempty_string(payload.get("purpose"), "purpose")
        frozen_parent = FrozenParent.from_dict(
            _object(payload.get("frozen_parent"), "frozen_parent")
        )
        frozen_inputs_payload = _list(payload.get("frozen_inputs"), "frozen_inputs")
        frozen_inputs = tuple(
            FrozenInput.from_dict(_object(item, "frozen_inputs[]"))
            for item in frozen_inputs_payload
        )
        if not frozen_inputs:
            raise CampaignError("frozen_inputs must contain at least one pinned input")
        input_ids = [item.input_id for item in frozen_inputs]
        if len(set(input_ids)) != len(input_ids):
            raise CampaignError("frozen_inputs contains duplicate input_id values")
        mutable_scope = _string_tuple(payload.get("mutable_scope"), "mutable_scope")
        off_limits = _string_tuple(payload.get("off_limits"), "off_limits")
        if not mutable_scope:
            raise CampaignError("mutable_scope must not be empty")
        if not off_limits:
            raise CampaignError("off_limits must not be empty")
        overlap = set(mutable_scope) & set(off_limits)
        if overlap:
            raise CampaignError(
                f"mutable_scope and off_limits overlap: {sorted(overlap)!r}"
            )
        budget = CampaignBudget.from_dict(_object(payload.get("budget"), "budget"))
        stop_policy = StopPolicy.from_dict(
            _object(payload.get("stop_policy"), "stop_policy")
        )
        supplied_hash = payload.get("manifest_sha256")
        unsigned = {
            "schema_version": CAMPAIGN_SCHEMA_VERSION,
            "campaign_id": campaign_id,
            "purpose": purpose,
            "frozen_parent": asdict(frozen_parent),
            "frozen_inputs": [asdict(item) for item in frozen_inputs],
            "mutable_scope": list(mutable_scope),
            "off_limits": list(off_limits),
            "budget": asdict(budget),
            "stop_policy": asdict(stop_policy),
        }
        calculated = _sha256_json(unsigned)
        if supplied_hash is None:
            if require_hash:
                raise CampaignError("campaign manifest is missing manifest_sha256")
            supplied_hash = calculated
        if not isinstance(supplied_hash, str) or not SHA256_RE.fullmatch(supplied_hash):
            raise CampaignError("manifest_sha256 must be a lowercase SHA-256 digest")
        if supplied_hash != calculated:
            raise CampaignError("campaign manifest hash does not match its contents")
        return cls(
            schema_version=CAMPAIGN_SCHEMA_VERSION,
            campaign_id=campaign_id,
            purpose=purpose,
            frozen_parent=frozen_parent,
            frozen_inputs=frozen_inputs,
            mutable_scope=mutable_scope,
            off_limits=off_limits,
            budget=budget,
            stop_policy=stop_policy,
            manifest_sha256=calculated,
        )


@dataclass(frozen=True)
class JournalEvent:
    schema_version: int
    sequence: int
    campaign_id: str
    manifest_sha256: str
    event_type: str
    occurred_at_utc: str
    payload: dict[str, Any]
    previous_event_sha256: str | None
    event_sha256: str

    def unsigned_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload.pop("event_sha256", None)
        return payload

    def to_dict(self) -> dict[str, Any]:
        return {**self.unsigned_dict(), "event_sha256": self.event_sha256}


@dataclass(frozen=True)
class ResumeCapsule:
    schema_version: int
    campaign_id: str
    manifest_sha256: str
    journal_head_sha256: str
    last_sequence: int
    last_event_type: str
    campaign_status: str
    current_candidate_id: str | None
    attempts_started: int
    attempts_completed: int
    total_tokens: int
    wall_clock_seconds: float
    hard_gate_failure_seen: bool
    consecutive_non_improving: int
    remaining_budget: dict[str, int | float | None]
    stop_reasons: tuple[str, ...]
    next_action: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_manifest_template(path: Path) -> CampaignManifest:
    return CampaignManifest.from_dict(_read_json_object(path, "campaign manifest"), require_hash=False)


def load_campaign_manifest(campaign_root: Path) -> CampaignManifest:
    path = campaign_root.resolve() / "campaign-manifest.json"
    return CampaignManifest.from_dict(_read_json_object(path, "campaign manifest"), require_hash=True)


def verify_frozen_inputs(
    manifest: CampaignManifest,
    *,
    inputs_root: Path | None = None,
) -> dict[str, str]:
    base = inputs_root.resolve() if inputs_root else None
    verified: dict[str, str] = {}
    for item in manifest.frozen_inputs:
        path = Path(item.path).expanduser()
        if not path.is_absolute():
            if base is None:
                raise CampaignError(
                    f"Frozen input {item.input_id!r} uses a relative path but no inputs_root was supplied"
                )
            path = base / path
        path = path.resolve()
        try:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
        except FileNotFoundError as exc:
            raise CampaignError(
                f"Frozen input {item.input_id!r} was not found: {path}"
            ) from exc
        if digest != item.sha256:
            raise CampaignError(
                f"Frozen input {item.input_id!r} hash mismatch: expected {item.sha256}, got {digest}"
            )
        verified[item.input_id] = str(path)
    return verified


def initialize_campaign(
    *,
    campaign_root: Path,
    manifest: CampaignManifest,
    verify_inputs: bool = True,
    inputs_root: Path | None = None,
) -> ResumeCapsule:
    root = campaign_root.resolve()
    if root.exists() and any(root.iterdir()):
        raise CampaignError(f"Campaign root is not empty: {root}")
    if verify_inputs:
        verify_frozen_inputs(manifest, inputs_root=inputs_root)
    root.mkdir(parents=True, exist_ok=True)
    _atomic_write_json(root / "campaign-manifest.json", manifest.to_dict(), overwrite=False)
    event = _build_event(
        manifest=manifest,
        sequence=1,
        event_type="campaign_initialized",
        payload={"purpose": manifest.purpose},
        previous_event_sha256=None,
    )
    _append_jsonl(root / "campaign-journal.jsonl", event.to_dict(), create_only=True)
    capsule = build_resume_capsule(manifest, (event,))
    _atomic_write_json(root / "resume-capsule.json", capsule.to_dict(), overwrite=True)
    return capsule


def append_campaign_event(
    *,
    campaign_root: Path,
    event_type: str,
    payload: Mapping[str, Any] | None = None,
) -> ResumeCapsule:
    root = campaign_root.resolve()
    manifest = load_campaign_manifest(root)
    if event_type not in EVENT_TYPES or event_type == "campaign_initialized":
        raise CampaignError(f"Unsupported appendable campaign event type: {event_type!r}")
    event_payload = dict(payload or {})
    _validate_event_payload(event_type, event_payload)
    lock = root / ".campaign-journal.lock"
    with _exclusive_lock(lock):
        events = load_campaign_journal(root, manifest=manifest)
        if events[-1].event_type in TERMINAL_EVENT_TYPES:
            raise CampaignError("Cannot append events after a terminal campaign event")
        _validate_transition(
            manifest=manifest,
            events=events,
            event_type=event_type,
            payload=event_payload,
        )
        event = _build_event(
            manifest=manifest,
            sequence=events[-1].sequence + 1,
            event_type=event_type,
            payload=event_payload,
            previous_event_sha256=events[-1].event_sha256,
        )
        _append_jsonl(root / "campaign-journal.jsonl", event.to_dict(), create_only=False)
        events = (*events, event)
        capsule = build_resume_capsule(manifest, events)
        _atomic_write_json(root / "resume-capsule.json", capsule.to_dict(), overwrite=True)
        return capsule


def load_campaign_journal(
    campaign_root: Path,
    *,
    manifest: CampaignManifest | None = None,
) -> tuple[JournalEvent, ...]:
    root = campaign_root.resolve()
    manifest = manifest or load_campaign_manifest(root)
    path = root / "campaign-journal.jsonl"
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError as exc:
        raise CampaignError(f"Campaign journal was not found: {path}") from exc
    if not lines:
        raise CampaignError("Campaign journal is empty")
    result: list[JournalEvent] = []
    previous_hash: str | None = None
    for index, line in enumerate(lines, start=1):
        if not line.strip():
            raise CampaignError(f"Campaign journal contains a blank line at {index}")
        try:
            payload = json.loads(line)
        except json.JSONDecodeError as exc:
            raise CampaignError(f"Campaign journal line {index} is invalid JSON") from exc
        if not isinstance(payload, dict):
            raise CampaignError(f"Campaign journal line {index} must be an object")
        event = _event_from_dict(payload)
        if event.sequence != index:
            raise CampaignError(
                f"Campaign journal sequence mismatch at line {index}: {event.sequence}"
            )
        if event.campaign_id != manifest.campaign_id:
            raise CampaignError("Campaign journal campaign_id does not match manifest")
        if event.manifest_sha256 != manifest.manifest_sha256:
            raise CampaignError("Campaign journal manifest hash does not match manifest")
        if event.previous_event_sha256 != previous_hash:
            raise CampaignError(f"Campaign journal hash chain is broken at sequence {index}")
        if index == 1 and event.event_type != "campaign_initialized":
            raise CampaignError("First campaign journal event must be campaign_initialized")
        if index > 1 and event.event_type == "campaign_initialized":
            raise CampaignError("campaign_initialized may appear only once")
        if result:
            _validate_transition(
                manifest=manifest,
                events=tuple(result),
                event_type=event.event_type,
                payload=event.payload,
            )
        previous_hash = event.event_sha256
        result.append(event)
    return tuple(result)


def inspect_campaign(campaign_root: Path, *, write_capsule: bool = True) -> ResumeCapsule:
    root = campaign_root.resolve()
    manifest = load_campaign_manifest(root)
    events = load_campaign_journal(root, manifest=manifest)
    capsule = build_resume_capsule(manifest, events)
    if write_capsule:
        _atomic_write_json(root / "resume-capsule.json", capsule.to_dict(), overwrite=True)
    return capsule


def build_resume_capsule(
    manifest: CampaignManifest,
    events: Iterable[JournalEvent],
) -> ResumeCapsule:
    event_list = tuple(events)
    if not event_list:
        raise CampaignError("Cannot build a resume capsule without journal events")
    candidates: set[str] = set()
    attempts_started = 0
    attempts_completed = 0
    total_tokens = 0
    wall_clock_seconds = 0.0
    current_candidate_id: str | None = None
    hard_gate_failure_seen = False
    consecutive_non_improving = 0
    attempts_by_candidate: dict[str, int] = {}

    for event in event_list:
        candidate_id = _optional_string(event.payload.get("candidate_id"))
        if event.event_type == "candidate_registered":
            candidate_id = _required_payload_string(event, "candidate_id")
            candidates.add(candidate_id)
            current_candidate_id = candidate_id
        elif candidate_id:
            candidates.add(candidate_id)
            current_candidate_id = candidate_id

        if event.event_type == "attempt_started":
            attempts_started += 1
            candidate = _required_payload_string(event, "candidate_id")
            attempts_by_candidate[candidate] = attempts_by_candidate.get(candidate, 0) + 1
        elif event.event_type == "attempt_completed":
            attempts_completed += 1
            metrics = event.payload.get("metrics")
            if isinstance(metrics, dict):
                total_tokens += _nonnegative_int(metrics.get("total_tokens", 0), "metrics.total_tokens")
                wall_clock_seconds += _nonnegative_number(
                    metrics.get("duration_seconds", 0.0), "metrics.duration_seconds"
                )
            hard_gate_passed = event.payload.get("hard_gate_passed")
            if hard_gate_passed is False:
                hard_gate_failure_seen = True
        elif event.event_type == "candidate_kept":
            consecutive_non_improving = 0
        elif event.event_type in {"candidate_rejected", "candidate_quarantined"}:
            consecutive_non_improving += 1

    current_candidate_attempts = (
        attempts_by_candidate.get(current_candidate_id, 0)
        if current_candidate_id
        else 0
    )
    remaining_budget: dict[str, int | float | None] = {
        "candidates": max(manifest.budget.max_candidates - len(candidates), 0),
        "total_attempts": max(
            manifest.budget.max_total_attempts - attempts_started, 0
        ),
        "current_candidate_attempts": max(
            manifest.budget.max_attempts_per_candidate - current_candidate_attempts,
            0,
        ),
        "tokens": (
            None
            if manifest.budget.max_total_tokens is None
            else max(manifest.budget.max_total_tokens - total_tokens, 0)
        ),
        "wall_clock_seconds": (
            None
            if manifest.budget.max_wall_clock_seconds is None
            else max(manifest.budget.max_wall_clock_seconds - wall_clock_seconds, 0.0)
        ),
    }
    stop_reasons = _stop_reasons(
        manifest=manifest,
        events=event_list,
        remaining_budget=remaining_budget,
        hard_gate_failure_seen=hard_gate_failure_seen,
        consecutive_non_improving=consecutive_non_improving,
    )
    last = event_list[-1]
    status = _campaign_status(last.event_type, stop_reasons)
    next_action = _next_action(
        manifest=manifest,
        last=last,
        stop_reasons=stop_reasons,
        remaining_budget=remaining_budget,
    )
    return ResumeCapsule(
        schema_version=CAMPAIGN_SCHEMA_VERSION,
        campaign_id=manifest.campaign_id,
        manifest_sha256=manifest.manifest_sha256,
        journal_head_sha256=last.event_sha256,
        last_sequence=last.sequence,
        last_event_type=last.event_type,
        campaign_status=status,
        current_candidate_id=current_candidate_id,
        attempts_started=attempts_started,
        attempts_completed=attempts_completed,
        total_tokens=total_tokens,
        wall_clock_seconds=wall_clock_seconds,
        hard_gate_failure_seen=hard_gate_failure_seen,
        consecutive_non_improving=consecutive_non_improving,
        remaining_budget=remaining_budget,
        stop_reasons=stop_reasons,
        next_action=next_action,
    )


def _build_event(
    *,
    manifest: CampaignManifest,
    sequence: int,
    event_type: str,
    payload: dict[str, Any],
    previous_event_sha256: str | None,
) -> JournalEvent:
    unsigned = {
        "schema_version": JOURNAL_SCHEMA_VERSION,
        "sequence": sequence,
        "campaign_id": manifest.campaign_id,
        "manifest_sha256": manifest.manifest_sha256,
        "event_type": event_type,
        "occurred_at_utc": _utc_now(),
        "payload": payload,
        "previous_event_sha256": previous_event_sha256,
    }
    return JournalEvent(event_sha256=_sha256_json(unsigned), **unsigned)


def _event_from_dict(payload: Mapping[str, Any]) -> JournalEvent:
    if payload.get("schema_version") != JOURNAL_SCHEMA_VERSION:
        raise CampaignError(
            f"Unsupported campaign journal schema: {payload.get('schema_version')!r}"
        )
    sequence = _positive_int(payload.get("sequence"), "journal.sequence")
    campaign_id = _nonempty_string(payload.get("campaign_id"), "journal.campaign_id")
    manifest_sha256 = _nonempty_string(
        payload.get("manifest_sha256"), "journal.manifest_sha256"
    )
    event_type = _nonempty_string(payload.get("event_type"), "journal.event_type")
    if event_type not in EVENT_TYPES:
        raise CampaignError(f"Unsupported campaign journal event type: {event_type!r}")
    occurred_at_utc = _nonempty_string(
        payload.get("occurred_at_utc"), "journal.occurred_at_utc"
    )
    event_payload = _object(payload.get("payload"), "journal.payload")
    previous = payload.get("previous_event_sha256")
    if previous is not None and (
        not isinstance(previous, str) or not SHA256_RE.fullmatch(previous)
    ):
        raise CampaignError("journal.previous_event_sha256 must be a SHA-256 or null")
    supplied_hash = _nonempty_string(payload.get("event_sha256"), "journal.event_sha256")
    unsigned = {
        "schema_version": JOURNAL_SCHEMA_VERSION,
        "sequence": sequence,
        "campaign_id": campaign_id,
        "manifest_sha256": manifest_sha256,
        "event_type": event_type,
        "occurred_at_utc": occurred_at_utc,
        "payload": event_payload,
        "previous_event_sha256": previous,
    }
    calculated = _sha256_json(unsigned)
    if supplied_hash != calculated:
        raise CampaignError(f"Campaign journal event hash mismatch at sequence {sequence}")
    _validate_event_payload(event_type, event_payload)
    return JournalEvent(event_sha256=calculated, **unsigned)


def _validate_event_payload(event_type: str, payload: Mapping[str, Any]) -> None:
    if event_type == "hypothesis_registered":
        _nonempty_string(payload.get("hypothesis_id"), "hypothesis_registered.hypothesis_id")
    if event_type == "candidate_registered":
        _nonempty_string(payload.get("hypothesis_id"), "candidate_registered.hypothesis_id")
    if event_type in {
        "candidate_registered",
        "attempt_started",
        "attempt_completed",
        "attempt_evidence_reconciled",
        "candidate_reviewed",
        "candidate_kept",
        "candidate_rejected",
        "candidate_quarantined",
    }:
        _nonempty_string(payload.get("candidate_id"), f"{event_type}.candidate_id")
    if event_type in {"attempt_started", "attempt_completed", "attempt_evidence_reconciled"}:
        _nonempty_string(payload.get("attempt_id"), f"{event_type}.attempt_id")
    if event_type == "attempt_completed":
        hard_gate = payload.get("hard_gate_passed")
        improved = payload.get("improved")
        if not isinstance(hard_gate, bool):
            raise CampaignError("attempt_completed.hard_gate_passed must be boolean")
        if not isinstance(improved, bool):
            raise CampaignError("attempt_completed.improved must be boolean")
        metrics = payload.get("metrics", {})
        if not isinstance(metrics, dict):
            raise CampaignError("attempt_completed.metrics must be an object")
        _nonnegative_int(metrics.get("total_tokens", 0), "metrics.total_tokens")
        _nonnegative_number(metrics.get("duration_seconds", 0.0), "metrics.duration_seconds")
    if event_type == "attempt_evidence_reconciled":
        sequence = _positive_int(
            payload.get("source_attempt_completed_sequence"),
            "attempt_evidence_reconciled.source_attempt_completed_sequence",
        )
        if sequence < 1:
            raise CampaignError("attempt_evidence_reconciled source sequence must be positive")
        source_sha = _nonempty_string(
            payload.get("source_attempt_completed_event_sha256"),
            "attempt_evidence_reconciled.source_attempt_completed_event_sha256",
        )
        if not SHA256_RE.fullmatch(source_sha):
            raise CampaignError(
                "attempt_evidence_reconciled.source_attempt_completed_event_sha256 must be a SHA-256"
            )
        if payload.get("adapter") != "balanced-suite-reconciliation-v1":
            raise CampaignError(
                "attempt_evidence_reconciled.adapter must be balanced-suite-reconciliation-v1"
            )
        if payload.get("reason") != "historical_suite_projection_reconciliation":
            raise CampaignError(
                "attempt_evidence_reconciled.reason must be historical_suite_projection_reconciliation"
            )
        if payload.get("next_action") != "start_next_independent_attempt":
            raise CampaignError(
                "attempt_evidence_reconciled.next_action must remain start_next_independent_attempt"
            )
        suite = _object(payload.get("suite"), "attempt_evidence_reconciled.suite")
        for field in ("suite_id", "suite_root", "eval_id", "source_commit", "plan_sha256", "suite_status", "verdict_status"):
            _nonempty_string(suite.get(field), f"attempt_evidence_reconciled.suite.{field}")
        if not SHA256_RE.fullmatch(str(suite.get("plan_sha256"))):
            raise CampaignError("attempt_evidence_reconciled.suite.plan_sha256 must be a SHA-256")
        for field in ("total_runs", "terminal_runs", "passed_runs", "failed_runs", "error_runs"):
            _nonnegative_int(suite.get(field), f"attempt_evidence_reconciled.suite.{field}")
        evidence = _object(
            suite.get("evidence_sha256"),
            "attempt_evidence_reconciled.suite.evidence_sha256",
        )
        required = {
            "suite-plan.json", "suite-state.json", "suite-result.json",
            "suite-aggregation.json", "suite-report.json", "suite-verdict.json",
        }
        if set(evidence) != required:
            raise CampaignError(
                "attempt_evidence_reconciled.suite.evidence_sha256 must contain the exact six suite evidence files"
            )
        for name, digest in evidence.items():
            if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
                raise CampaignError(
                    f"attempt_evidence_reconciled invalid evidence SHA-256 for {name}"
                )
    if event_type == "candidate_reviewed":
        _nonempty_string(payload.get("hypothesis_id"), "candidate_reviewed.hypothesis_id")
        decision = _nonempty_string(payload.get("decision"), "candidate_reviewed.decision")
        if decision not in {"keep", "reject", "continue"}:
            raise CampaignError("candidate_reviewed.decision must be keep, reject, or continue")
        meanings = {
            "keep": "keep-for-independent-review",
            "reject": "reject-candidate",
            "continue": "collect-or-reconcile-evidence",
        }
        if payload.get("operational_meaning") != meanings[decision]:
            raise CampaignError(
                "candidate_reviewed.operational_meaning does not match decision"
            )
        if payload.get("promotion_status") != "not_requested":
            raise CampaignError(
                "candidate_reviewed.promotion_status must remain not_requested"
            )
        expected_next = {
            "keep": "await_independent_review",
            "reject": "record_candidate_rejected",
            "continue": "start_next_independent_attempt",
        }[decision]
        if payload.get("next_action") != expected_next:
            raise CampaignError("candidate_reviewed.next_action does not match decision")
        for field in (
            "review_path",
            "review_sha256",
            "review_journal_head_sha256",
            "handoff_path",
            "handoff_sha256",
            "receipt_path",
        ):
            _nonempty_string(payload.get(field), f"candidate_reviewed.{field}")
        for field in ("review_sha256", "review_journal_head_sha256", "handoff_sha256"):
            if not SHA256_RE.fullmatch(str(payload.get(field))):
                raise CampaignError(f"candidate_reviewed.{field} must be a SHA-256")
    if event_type == "campaign_completed":
        reason = _nonempty_string(payload.get("reason"), "campaign_completed.reason")
        if reason == "accepted_candidate":
            # Backward-compatible library-level completion for pre-E1.6 campaign chains.
            # The generic CLI no longer exposes campaign_completed; accepted E1.5
            # decisions must use the E1.6 completion seal path below.
            pass
        elif reason == "campaign_completion_seal":
            _nonempty_string(payload.get("candidate_id"), "campaign_completed.candidate_id")
            _nonempty_string(payload.get("hypothesis_id"), "campaign_completed.hypothesis_id")
            for field in (
                "source_decision_artifact_path",
                "completion_seal_path",
                "release_handoff_path",
            ):
                _nonempty_string(payload.get(field), f"campaign_completed.{field}")
            for field in (
                "source_decision_sha256",
                "source_decision_event_sha256",
                "completion_seal_sha256",
                "release_handoff_sha256",
            ):
                value = _nonempty_string(payload.get(field), f"campaign_completed.{field}")
                if not SHA256_RE.fullmatch(value):
                    raise CampaignError(f"campaign_completed.{field} must be a SHA-256")
            if payload.get("release_status") != "not_requested":
                raise CampaignError("campaign_completed.release_status must remain not_requested")
            if payload.get("central_planning_lite_mutated") is not False:
                raise CampaignError(
                    "campaign_completed.central_planning_lite_mutated must be false"
                )
        else:
            raise CampaignError(
                "campaign_completed.reason must be accepted_candidate or campaign_completion_seal"
            )

    if (
        event_type in {"candidate_kept", "candidate_rejected", "candidate_quarantined"}
        and payload.get("reason") == "independent_review_decision"
    ):
        _nonempty_string(payload.get("hypothesis_id"), f"{event_type}.hypothesis_id")
        _nonempty_string(payload.get("reviewer_id"), f"{event_type}.reviewer_id")
        if payload.get("reviewer_role") != "independent_reviewer":
            raise CampaignError(f"{event_type}.reviewer_role must be independent_reviewer")
        _nonempty_string(
            payload.get("decision_artifact_path"), f"{event_type}.decision_artifact_path"
        )
        for field in ("decision_sha256", "source_candidate_reviewed_event_sha256"):
            value = _nonempty_string(payload.get(field), f"{event_type}.{field}")
            if not SHA256_RE.fullmatch(value):
                raise CampaignError(f"{event_type}.{field} must be a SHA-256")
        if payload.get("promotion_status") != "not_requested":
            raise CampaignError(f"{event_type}.promotion_status must remain not_requested")


def _validate_transition(
    *,
    manifest: CampaignManifest,
    events: tuple[JournalEvent, ...],
    event_type: str,
    payload: Mapping[str, Any],
) -> None:
    if not events:
        raise CampaignError("Campaign transition validation requires existing events")
    last = events[-1]
    allowed = ALLOWED_TRANSITIONS.get(last.event_type, set())
    if event_type not in allowed:
        raise CampaignError(
            f"Invalid campaign transition: {last.event_type} -> {event_type}"
        )

    capsule = build_resume_capsule(manifest, events)
    if capsule.campaign_status == "stop-required" and event_type not in TERMINAL_EVENT_TYPES:
        hard_gate_review_path = (
            event_type == "candidate_reviewed"
            and payload.get("decision") == "reject"
            and last.event_type == "attempt_completed"
        )
        explicit_reject_path = (
            event_type == "candidate_rejected"
            and last.event_type == "candidate_reviewed"
            and last.payload.get("decision") == "reject"
        )
        if not hard_gate_review_path and not explicit_reject_path:
            raise CampaignError(
                f"Campaign requires a terminal stop record before {event_type!r}"
            )

    registered_hypotheses = {
        _optional_string(event.payload.get("hypothesis_id"))
        for event in events
        if event.event_type == "hypothesis_registered"
    }
    registered_hypotheses.discard(None)
    registered_candidates = {
        _optional_string(event.payload.get("candidate_id"))
        for event in events
        if event.event_type == "candidate_registered"
    }
    registered_candidates.discard(None)
    started_attempts = {
        _optional_string(event.payload.get("attempt_id"))
        for event in events
        if event.event_type == "attempt_started"
    }
    started_attempts.discard(None)
    completed_attempts = {
        _optional_string(event.payload.get("attempt_id"))
        for event in events
        if event.event_type == "attempt_completed"
    }
    completed_attempts.discard(None)

    if event_type == "hypothesis_registered":
        hypothesis_id = _nonempty_string(
            payload.get("hypothesis_id"), "hypothesis_registered.hypothesis_id"
        )
        if hypothesis_id in registered_hypotheses:
            raise CampaignError(f"Duplicate hypothesis_id: {hypothesis_id}")

    if event_type == "candidate_registered":
        candidate_id = _nonempty_string(
            payload.get("candidate_id"), "candidate_registered.candidate_id"
        )
        hypothesis_id = _nonempty_string(
            payload.get("hypothesis_id"), "candidate_registered.hypothesis_id"
        )
        if candidate_id in registered_candidates:
            raise CampaignError(f"Duplicate candidate_id: {candidate_id}")
        if hypothesis_id not in registered_hypotheses:
            raise CampaignError(
                f"candidate_registered references unknown hypothesis_id: {hypothesis_id}"
            )
        if len(registered_candidates) >= manifest.budget.max_candidates:
            raise CampaignError("Candidate budget is exhausted")

    if event_type == "attempt_started":
        candidate_id = _nonempty_string(
            payload.get("candidate_id"), "attempt_started.candidate_id"
        )
        attempt_id = _nonempty_string(
            payload.get("attempt_id"), "attempt_started.attempt_id"
        )
        current_candidate = _current_candidate(events)
        if candidate_id != current_candidate:
            raise CampaignError(
                f"attempt_started candidate_id {candidate_id!r} does not match current candidate {current_candidate!r}"
            )
        if attempt_id in started_attempts:
            raise CampaignError(f"Duplicate attempt_id: {attempt_id}")
        candidate_attempts = sum(
            1
            for event in events
            if event.event_type == "attempt_started"
            and event.payload.get("candidate_id") == candidate_id
        )
        if len(started_attempts) >= manifest.budget.max_total_attempts:
            raise CampaignError("Total attempt budget is exhausted")
        if candidate_attempts >= manifest.budget.max_attempts_per_candidate:
            raise CampaignError("Current candidate attempt budget is exhausted")
        if (
            manifest.budget.max_total_tokens is not None
            and capsule.total_tokens >= manifest.budget.max_total_tokens
        ):
            raise CampaignError("Token budget is exhausted")
        if (
            manifest.budget.max_wall_clock_seconds is not None
            and capsule.wall_clock_seconds >= manifest.budget.max_wall_clock_seconds
        ):
            raise CampaignError("Wall-clock budget is exhausted")

    if event_type == "attempt_completed":
        candidate_id = _nonempty_string(
            payload.get("candidate_id"), "attempt_completed.candidate_id"
        )
        attempt_id = _nonempty_string(
            payload.get("attempt_id"), "attempt_completed.attempt_id"
        )
        current_candidate = _current_candidate(events)
        if candidate_id != current_candidate:
            raise CampaignError(
                f"attempt_completed candidate_id {candidate_id!r} does not match current candidate {current_candidate!r}"
            )
        open_attempt = _open_attempt(events)
        if open_attempt is None or open_attempt != attempt_id:
            raise CampaignError(
                f"attempt_completed does not match the open attempt: {attempt_id!r}"
            )
        if attempt_id in completed_attempts:
            raise CampaignError(f"Duplicate completed attempt_id: {attempt_id}")

    if event_type == "attempt_evidence_reconciled":
        candidate_id = _nonempty_string(
            payload.get("candidate_id"), "attempt_evidence_reconciled.candidate_id"
        )
        attempt_id = _nonempty_string(
            payload.get("attempt_id"), "attempt_evidence_reconciled.attempt_id"
        )
        current_candidate = _current_candidate(events)
        if candidate_id != current_candidate:
            raise CampaignError(
                f"attempt_evidence_reconciled candidate_id {candidate_id!r} does not match current candidate {current_candidate!r}"
            )
        matches = [
            event for event in events
            if event.event_type == "attempt_completed"
            and event.payload.get("candidate_id") == candidate_id
            and event.payload.get("attempt_id") == attempt_id
        ]
        if len(matches) != 1:
            raise CampaignError(
                f"attempt_evidence_reconciled requires exactly one historical attempt_completed for {attempt_id!r}"
            )
        source = matches[0]
        if source.payload.get("suite") is not None:
            raise CampaignError(
                "attempt_evidence_reconciled is only allowed for historical completions without native suite provenance"
            )
        if payload.get("source_attempt_completed_sequence") != source.sequence:
            raise CampaignError(
                "attempt_evidence_reconciled source sequence does not match historical completion"
            )
        if payload.get("source_attempt_completed_event_sha256") != source.event_sha256:
            raise CampaignError(
                "attempt_evidence_reconciled source event SHA does not match historical completion"
            )
        duplicates = [
            event for event in events
            if event.event_type == "attempt_evidence_reconciled"
            and event.payload.get("candidate_id") == candidate_id
            and event.payload.get("attempt_id") == attempt_id
        ]
        if duplicates:
            raise CampaignError(
                f"Attempt {attempt_id!r} already has reconciled suite evidence"
            )
    if event_type == "candidate_reviewed":
        candidate_id = _nonempty_string(
            payload.get("candidate_id"), "candidate_reviewed.candidate_id"
        )
        current_candidate = _current_candidate(events)
        if candidate_id != current_candidate:
            raise CampaignError(
                f"candidate_reviewed candidate_id {candidate_id!r} does not match current candidate {current_candidate!r}"
            )
        if payload.get("review_journal_head_sha256") != last.event_sha256:
            raise CampaignError(
                "candidate_reviewed review_journal_head_sha256 must match the current journal head"
            )
        duplicate_receipts = [
            event
            for event in events
            if event.event_type == "candidate_reviewed"
            and event.payload.get("candidate_id") == candidate_id
            and event.payload.get("review_sha256") == payload.get("review_sha256")
        ]
        if duplicate_receipts:
            raise CampaignError(
                f"Candidate {candidate_id!r} already has a receipt for this review artifact"
            )

    if last.event_type == "candidate_reviewed":
        decision = last.payload.get("decision")
        permitted = {
            "keep": {
                "candidate_kept",
                "candidate_rejected",
                "candidate_quarantined",
                "campaign_stopped",
            },
            "reject": {"candidate_rejected", "candidate_quarantined", "campaign_stopped"},
            "continue": {"attempt_started", "attempt_evidence_reconciled", "candidate_quarantined", "campaign_stopped"},
        }.get(decision, set())
        if event_type not in permitted:
            raise CampaignError(
                f"Review decision {decision!r} does not permit follow-up event {event_type!r}"
            )
        if (
            decision == "keep"
            and event_type in {"candidate_kept", "candidate_rejected", "candidate_quarantined"}
        ):
            if payload.get("reason") != "independent_review_decision":
                raise CampaignError(
                    "keep-for-independent-review requires the Independent Review Decision Gate "
                    "before a terminal candidate decision"
                )
            if payload.get("source_candidate_reviewed_event_sha256") != last.event_sha256:
                raise CampaignError(
                    "Independent review decision must bind the current candidate_reviewed event"
                )

    if event_type == "campaign_completed":
        if last.event_type != "candidate_kept":
            raise CampaignError("campaign_completed requires candidate_kept as journal head")
        independent_path = last.payload.get("reason") == "independent_review_decision"
        if independent_path:
            if payload.get("reason") != "campaign_completion_seal":
                raise CampaignError(
                    "Independent-review candidate_kept requires the E1.6 Campaign Completion Seal"
                )
            candidate_id = _nonempty_string(
                payload.get("candidate_id"), "campaign_completed.candidate_id"
            )
            current_candidate = _current_candidate(events)
            if candidate_id != current_candidate:
                raise CampaignError(
                    f"campaign_completed candidate_id {candidate_id!r} does not match current candidate {current_candidate!r}"
                )
            if payload.get("source_decision_event_sha256") != last.event_sha256:
                raise CampaignError(
                    "campaign_completed must bind the current candidate_kept journal head"
                )
            if payload.get("source_decision_sha256") != last.payload.get("decision_sha256"):
                raise CampaignError(
                    "campaign_completed source decision hash does not match candidate_kept"
                )
            if Path(
                _nonempty_string(
                    payload.get("source_decision_artifact_path"),
                    "campaign_completed.source_decision_artifact_path",
                )
            ).resolve() != Path(
                _nonempty_string(
                    last.payload.get("decision_artifact_path"),
                    "candidate_kept.decision_artifact_path",
                )
            ).resolve():
                raise CampaignError(
                    "campaign_completed source decision path does not match candidate_kept"
                )
        elif payload.get("reason") != "accepted_candidate":
            raise CampaignError(
                "Legacy candidate_kept completion requires reason='accepted_candidate'"
            )

    if event_type in {"candidate_kept", "candidate_rejected", "candidate_quarantined"}:
        candidate_id = _nonempty_string(
            payload.get("candidate_id"), f"{event_type}.candidate_id"
        )
        current_candidate = _current_candidate(events)
        if candidate_id != current_candidate:
            raise CampaignError(
                f"{event_type} candidate_id {candidate_id!r} does not match current candidate {current_candidate!r}"
            )
        if event_type != "candidate_quarantined":
            completed_for_candidate = any(
                event.event_type == "attempt_completed"
                and event.payload.get("candidate_id") == candidate_id
                for event in events
            )
            if not completed_for_candidate:
                raise CampaignError(
                    f"{event_type} requires at least one completed attempt"
                )


def _current_candidate(events: tuple[JournalEvent, ...]) -> str | None:
    for event in reversed(events):
        candidate_id = _optional_string(event.payload.get("candidate_id"))
        if candidate_id:
            return candidate_id
    return None


def _open_attempt(events: tuple[JournalEvent, ...]) -> str | None:
    completed = {
        _optional_string(event.payload.get("attempt_id"))
        for event in events
        if event.event_type == "attempt_completed"
    }
    for event in reversed(events):
        if event.event_type != "attempt_started":
            continue
        attempt_id = _optional_string(event.payload.get("attempt_id"))
        if attempt_id and attempt_id not in completed:
            return attempt_id
    return None


def _stop_reasons(
    *,
    manifest: CampaignManifest,
    events: tuple[JournalEvent, ...],
    remaining_budget: Mapping[str, int | float | None],
    hard_gate_failure_seen: bool,
    consecutive_non_improving: int,
) -> tuple[str, ...]:
    reasons: list[str] = []
    last = events[-1]
    if last.event_type == "campaign_completed":
        reasons.append("campaign_completed")
    if last.event_type == "campaign_stopped":
        reason = _optional_string(last.payload.get("reason")) or "campaign_stopped"
        reasons.append(reason)
    if manifest.stop_policy.stop_on_hard_gate_failure and hard_gate_failure_seen:
        reasons.append("hard_gate_failure")
    if consecutive_non_improving >= manifest.stop_policy.max_consecutive_non_improving:
        reasons.append("consecutive_non_improving_limit")
    if last.event_type in {"candidate_rejected", "candidate_quarantined"}:
        for key in ("candidates", "total_attempts", "tokens", "wall_clock_seconds"):
            value = remaining_budget.get(key)
            if value == 0 or value == 0.0:
                reasons.append(f"{key}_budget_exhausted")
    if (
        manifest.stop_policy.stop_after_accepted_candidate
        and any(event.event_type == "candidate_kept" for event in events)
    ):
        reasons.append("accepted_candidate")
    return tuple(dict.fromkeys(reasons))


def _campaign_status(last_event_type: str, stop_reasons: tuple[str, ...]) -> str:
    if last_event_type == "campaign_completed":
        return "completed"
    if last_event_type == "campaign_stopped":
        return "stopped"
    if stop_reasons:
        return "stop-required"
    if last_event_type == "campaign_initialized":
        return "initialized"
    return "running"


def _next_action(
    *,
    manifest: CampaignManifest,
    last: JournalEvent,
    stop_reasons: tuple[str, ...],
    remaining_budget: Mapping[str, int | float | None],
) -> str:
    if last.event_type in TERMINAL_EVENT_TYPES:
        return "none"
    if last.event_type == "attempt_evidence_reconciled":
        return "start_next_independent_attempt"
    if last.event_type == "candidate_reviewed":
        return {
            "keep": "await_independent_review",
            "reject": "record_candidate_rejected",
            "continue": "start_next_independent_attempt",
        }.get(last.payload.get("decision"), "inspect_campaign_journal")
    if stop_reasons:
        if "accepted_candidate" in stop_reasons:
            return "record_campaign_completed"
        return "record_campaign_stopped"
    if last.event_type == "campaign_initialized":
        return "register_hypothesis"
    if last.event_type == "hypothesis_registered":
        return "register_candidate"
    if last.event_type == "candidate_registered":
        return "start_attempt"
    if last.event_type == "attempt_started":
        return "recover_or_complete_attempt"
    if last.event_type == "attempt_completed":
        return "review_candidate"
    if last.event_type == "candidate_kept":
        return (
            "record_campaign_completed"
            if manifest.stop_policy.stop_after_accepted_candidate
            else "register_candidate"
        )
    if last.event_type in {"candidate_rejected", "candidate_quarantined"}:
        if remaining_budget.get("candidates") == 0:
            return "record_campaign_stopped"
        return "register_candidate"
    return "inspect_campaign_journal"


class _exclusive_lock:
    def __init__(self, path: Path):
        self.path = path
        self.fd: int | None = None

    def __enter__(self) -> "_exclusive_lock":
        try:
            self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError as exc:
            raise CampaignError(f"Campaign journal is locked: {self.path}") from exc
        os.write(self.fd, f"pid={os.getpid()}\n".encode("utf-8"))
        os.fsync(self.fd)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self.fd is not None:
            os.close(self.fd)
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def _atomic_write_json(path: Path, payload: object, *, overwrite: bool) -> None:
    path = path.resolve()
    if path.exists() and not overwrite:
        raise CampaignError(f"Campaign artifact already exists: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    temporary = path.with_name(f".{path.name}.tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def _append_jsonl(path: Path, payload: object, *, create_only: bool) -> None:
    path = path.resolve()
    if create_only and path.exists():
        raise CampaignError(f"Campaign journal already exists: {path}")
    encoded = (
        json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("utf-8")
    flags = os.O_WRONLY | os.O_APPEND | os.O_CREAT
    if create_only:
        flags |= os.O_EXCL
    fd = os.open(path, flags, 0o644)
    try:
        os.write(fd, encoded)
        os.fsync(fd)
    finally:
        os.close(fd)


def _read_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise CampaignError(f"{label} was not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise CampaignError(f"{label} is invalid JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise CampaignError(f"{label} root must be an object: {path}")
    return payload


def _sha256_json(payload: object) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _nonempty_string(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise CampaignError(f"{label} must be a non-empty string")
    return value.strip()


def _optional_string(value: object) -> str | None:
    return value.strip() if isinstance(value, str) and value.strip() else None


def _required_payload_string(event: JournalEvent, key: str) -> str:
    return _nonempty_string(event.payload.get(key), f"{event.event_type}.{key}")


def _object(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise CampaignError(f"{label} must be an object")
    return dict(value)


def _list(value: object, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise CampaignError(f"{label} must be an array")
    return list(value)


def _string_tuple(value: object, label: str) -> tuple[str, ...]:
    values = _list(value, label)
    result = tuple(_nonempty_string(item, f"{label}[]") for item in values)
    if len(set(result)) != len(result):
        raise CampaignError(f"{label} contains duplicate values")
    return result


def _positive_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise CampaignError(f"{label} must be a positive integer")
    return value


def _optional_positive_int(value: object, label: str) -> int | None:
    if value is None:
        return None
    return _positive_int(value, label)


def _nonnegative_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise CampaignError(f"{label} must be a non-negative integer")
    return value


def _optional_positive_number(value: object, label: str) -> float | None:
    if value is None:
        return None
    number = _number(value, label)
    if number <= 0:
        raise CampaignError(f"{label} must be positive")
    return number


def _nonnegative_number(value: object, label: str) -> float:
    number = _number(value, label)
    if number < 0:
        raise CampaignError(f"{label} must be non-negative")
    return number


def _number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CampaignError(f"{label} must be numeric")
    return float(value)


def _bool(value: object, label: str) -> bool:
    if not isinstance(value, bool):
        raise CampaignError(f"{label} must be boolean")
    return value
