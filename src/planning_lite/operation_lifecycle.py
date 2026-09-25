"""Pattern-B coordinator for one bounded governed operation.

The lifecycle owns ordering only.  Attempt Runtime owns occurrence/state,
Telemetry owns receipt validation/storage/readback, and PL08 owns evaluation.
There is no lifecycle store, queue, worker, retry, callback, or next-gate
authority here.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Any

from .attempt_evaluation import (
    AcceptanceContractV1,
    EvidenceSupersessionV1,
    FindingV1,
    FindingApplicabilityV1,
    CandidateIdentityV1,
    DirtyPathEntryV1,
    EvidenceApplicabilityV1,
    ObservedResultV1,
    IdentityRefV1,
    VerifierContractV1,
    VerifierEvidenceV1,
    evaluate_technical,
)
from .context import OperationDepthObservationV1, build_compact_status
from .attempt_runtime import (
    AdmissibilityOutcome,
    AttemptRuntimeError,
    LookupOutcome,
    check_activation_admissibility,
    claim_attempt,
    lookup_attempt,
    terminalize_attempt,
)
from .governed_executor import (
    GovernedExecutionCompletionV1,
    GovernedExecutionEnvelopeV1,
    GovernedExecutionResultV1,
    GovernedExecutorError,
    invoke_governed_operation,
    prepare_governed_operation,
)
from .project_spine import (
    PostEvaluationCheckpointV1,
    ProjectSpineHandoffError,
    ProjectSpineSnapshotV1,
    capture_project_spine_snapshot,
    record_post_evaluation_checkpoint,
)
from .operation_trace import (
    OperationTraceError,
    OperationTraceView,
    read_operation_trace_evidence,
    record_governed_attempt_evidence,
)
from .telemetry import ReceiptError, collect_governed_receipt
from .workspace import WorkspaceError, inspect_project


class OperationLifecycleError(RuntimeError):
    """The lifecycle stopped at its first broken governed seam."""


OperationGuidanceV1 = Mapping[str, Any]


def _attribute(value: object, name: str, default: object = None) -> object:
    try:
        return object.__getattribute__(value, name)
    except AttributeError:
        return default


@dataclass(frozen=True, slots=True)
class GovernedLifecycleResultV1:
    """Detached result of one lifecycle call, with no authority fields."""

    disposition: str
    attempt_id: str
    first_broken_seam: str | None = None
    reason_code: str | None = None
    guidance: OperationGuidanceV1 | None = None
    envelope: GovernedExecutionEnvelopeV1 | None = None
    execution: GovernedExecutionResultV1 | None = None
    receipt: dict[str, Any] | None = None
    observed_result: ObservedResultV1 | None = None
    technical_evaluation: Any = None
    terminal_attempt: Any = None
    downstream: dict[str, Any] | None = None

    @property
    def completed(self) -> bool:
        return self.disposition == "COMPLETED_WITH_FACTS"

    def to_mapping(self) -> dict[str, Any]:
        def detached(value: object) -> object:
            if value is None:
                return None
            method = _attribute(value, "to_mapping")
            if callable(method):
                return method()
            if isinstance(value, Mapping):
                return dict(value)
            return value

        return {
            "disposition": self.disposition,
            "attempt_id": self.attempt_id,
            "first_broken_seam": self.first_broken_seam,
            "reason_code": self.reason_code,
            "guidance": detached(self.guidance),
            "envelope": detached(self.envelope),
            "execution": detached(self.execution),
            "receipt": dict(self.receipt) if self.receipt is not None else None,
            "observed_result": detached(self.observed_result),
            "technical_evaluation": detached(self.technical_evaluation),
            "terminal_attempt": detached(self.terminal_attempt),
            "downstream": dict(self.downstream) if self.downstream is not None else None,
        }


def _stopped(
    attempt_id: str,
    seam: str,
    reason: str,
    *,
    guidance: OperationGuidanceV1 | None = None,
    envelope: GovernedExecutionEnvelopeV1 | None = None,
    execution: GovernedExecutionResultV1 | None = None,
    receipt: dict[str, Any] | None = None,
    observed_result: ObservedResultV1 | None = None,
    technical_evaluation: Any = None,
    terminal_attempt: Any = None,
    downstream: dict[str, Any] | None = None,
) -> GovernedLifecycleResultV1:
    return GovernedLifecycleResultV1(
        disposition="STOPPED_FAIL_CLOSED",
        attempt_id=attempt_id,
        first_broken_seam=seam,
        reason_code=reason,
        guidance=guidance,
        envelope=envelope,
        execution=execution,
        receipt=receipt,
        observed_result=observed_result,
        technical_evaluation=technical_evaluation,
        terminal_attempt=terminal_attempt,
        downstream=downstream,
    )


def _typed_completion(value: object) -> GovernedExecutionCompletionV1 | None:
    if isinstance(value, GovernedExecutionCompletionV1):
        source = {name: object.__getattribute__(value, name) for name in GovernedExecutionCompletionV1.__dataclass_fields__}
    elif isinstance(value, Mapping):
        source = dict(value)
    else:
        return None
    try:
        source["acceptance_contract"] = _acceptance_contract(source.get("acceptance_contract"))
        source["verifier_contracts"] = tuple(
            _verifier_contract(item) for item in source.get("verifier_contracts", ())
        )
        source["verifier_evidence"] = tuple(
            _verifier_evidence(item) for item in source.get("verifier_evidence", ())
        )
        source["findings"] = tuple(_finding(item) for item in source.get("findings", ()))
        source["supersession"] = tuple(_supersession(item) for item in source.get("supersession", ()))
        fields = {field.name for field in GovernedExecutionCompletionV1.__dataclass_fields__.values()}
        return GovernedExecutionCompletionV1(**{key: source[key] for key in fields if key in source})
    except (TypeError, ValueError, GovernedExecutorError):
        return None


def _identity_ref(value: object) -> IdentityRefV1:
    if isinstance(value, IdentityRefV1):
        return value
    if isinstance(value, Mapping):
        return IdentityRefV1(ref=value.get("ref"), identity=value.get("identity"))
    raise ValueError("identity reference is invalid")


def _candidate(value: object) -> CandidateIdentityV1:
    if isinstance(value, CandidateIdentityV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("candidate identity is invalid")
    dirty: list[DirtyPathEntryV1] = []
    for item in value.get("dirty_manifest", ()):
        if isinstance(item, DirtyPathEntryV1):
            dirty.append(item)
            continue
        if not isinstance(item, Mapping):
            raise ValueError("dirty candidate entry is invalid")
        identity = item.get("content_identity", {})
        if not isinstance(identity, Mapping):
            raise ValueError("dirty candidate identity is invalid")
        dirty.append(
            DirtyPathEntryV1(
                path=item.get("path"),
                change_kind=item.get("change_kind"),
                before=identity.get("before"),
                after=identity.get("after"),
                source_path=item.get("source_path"),
            )
        )
    return CandidateIdentityV1(kind=value.get("kind"), head=value.get("head"), dirty_manifest=tuple(dirty))


def _verifier_contract(value: object) -> VerifierContractV1:
    if isinstance(value, VerifierContractV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("verifier contract is invalid")
    return VerifierContractV1(
        acceptance_contract_ref=value.get("acceptance_contract_ref"),
        contract_id=value.get("contract_id"),
        contract_version_or_ref=value.get("contract_version_or_ref"),
        required=value.get("required"),
        evidence_class=value.get("evidence_class"),
        predicate=value.get("predicate"),
        required_evidence_refs=tuple(value.get("required_evidence_refs", ())),
        failure_semantics=value.get("failure_semantics"),
    )


def _acceptance_contract(value: object) -> AcceptanceContractV1 | None:
    if value is None or isinstance(value, AcceptanceContractV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("acceptance contract is invalid")
    return AcceptanceContractV1(
        value.get("acceptance_contract_ref"),
        tuple(_verifier_contract(item) for item in value.get("verifier_contracts", ())),
    )


def _evidence_applicability(value: object) -> EvidenceApplicabilityV1:
    if isinstance(value, EvidenceApplicabilityV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("evidence applicability is invalid")
    return EvidenceApplicabilityV1(
        attempt_id=value.get("attempt_id"),
        candidate_identity=_candidate(value.get("candidate_identity")),
        acceptance_contract_ref=value.get("acceptance_contract_ref"),
        verifier_contract_ref=value.get("verifier_contract_ref"),
        verifier_contract_version_or_ref=value.get("verifier_contract_version_or_ref"),
        evaluation_scope_ref=value.get("evaluation_scope_ref"),
        finding_refs=tuple(value.get("finding_refs", ())),
        input_baseline_refs=tuple(_identity_ref(item) for item in value.get("input_baseline_refs", ())),
    )


def _verifier_evidence(value: object) -> VerifierEvidenceV1:
    if isinstance(value, VerifierEvidenceV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("verifier evidence is invalid")
    return VerifierEvidenceV1(
        evidence_id=value.get("evidence_id"),
        attempt_id=value.get("attempt_id"),
        candidate_identity=_candidate(value.get("candidate_identity")),
        verifier_contract_ref=value.get("verifier_contract_ref"),
        verifier_contract_version_or_ref=value.get("verifier_contract_version_or_ref"),
        outcome=value.get("outcome"),
        evidence_refs=tuple(value.get("evidence_refs", ())),
        applicability=_evidence_applicability(value.get("applicability")),
        claim_refs=tuple(value.get("claim_refs", ())),
    )


def _finding(value: object) -> FindingV1:
    if isinstance(value, FindingV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("finding is invalid")
    raw_applicability = value.get("applicability")
    applicability = raw_applicability
    if isinstance(raw_applicability, Mapping):
        applicability = FindingApplicabilityV1(
            attempt_id=raw_applicability.get("attempt_id"),
            candidate_identity=_candidate(raw_applicability.get("candidate_identity")),
            acceptance_contract_ref=raw_applicability.get("acceptance_contract_ref"),
            evaluation_scope_ref=raw_applicability.get("evaluation_scope_ref"),
            input_baseline_refs=tuple(_identity_ref(item) for item in raw_applicability.get("input_baseline_refs", ())),
        )
    return FindingV1(
        finding_id=value.get("finding_id"),
        statement=value.get("statement"),
        severity=value.get("severity"),
        responsibility_domains=tuple(value.get("responsibility_domains", ())),
        acceptance_impact=value.get("acceptance_impact"),
        disposition=value.get("disposition"),
        evidence_refs=tuple(value.get("evidence_refs", ())),
        owner_adjudication_ref=value.get("owner_adjudication_ref"),
        applicability=applicability,
    )


def _supersession(value: object) -> EvidenceSupersessionV1:
    if isinstance(value, EvidenceSupersessionV1):
        return value
    if not isinstance(value, Mapping):
        raise ValueError("supersession is invalid")
    return EvidenceSupersessionV1(
        prior_evidence_ref=value.get("prior_evidence_ref"),
        successor_evidence_ref=value.get("successor_evidence_ref"),
        current_acceptance_scope_ref=value.get("current_acceptance_scope_ref"),
        rechecked_claim_refs=tuple(value.get("rechecked_claim_refs", ())),
        reason=value.get("reason"),
    )


def _evaluation_carriers_valid(completion: GovernedExecutionCompletionV1) -> bool:
    """Check the live typed carrier boundary before irreversible terminalization."""

    return (
        isinstance(completion.acceptance_contract, AcceptanceContractV1)
        and isinstance(completion.evaluation_scope_ref, str)
        and bool(completion.evaluation_scope_ref)
        and all(isinstance(item, VerifierContractV1) for item in completion.verifier_contracts)
        and all(isinstance(item, VerifierEvidenceV1) for item in completion.verifier_evidence)
        and all(isinstance(item, FindingV1) for item in completion.findings)
        and all(isinstance(item, EvidenceSupersessionV1) for item in completion.supersession)
    )


def _receipt_context(
    target: Path,
    *,
    registered_project_id: str | None,
    receipt_path: str | Path | None,
    home: str | Path | None,
) -> tuple[str, Path, bool]:
    if registered_project_id is not None and receipt_path is not None:
        return registered_project_id, Path(receipt_path).expanduser().resolve(), True
    info = inspect_project(target, home=home)
    entry = info.get("entry", info)
    project_id = registered_project_id or entry.get("project_id")
    telemetry = entry.get("telemetry") if isinstance(entry, Mapping) else None
    path = receipt_path or (telemetry.get("receipt_path") if isinstance(telemetry, Mapping) else None)
    enabled = bool(telemetry.get("enabled")) if isinstance(telemetry, Mapping) else False
    if not isinstance(project_id, str) or not project_id or path is None:
        raise WorkspaceError("registered telemetry receipt context is unavailable")
    return project_id, Path(path).expanduser().resolve(), enabled


class _TracePersistenceError(RuntimeError):
    """A non-authoritative progress trace transport failure."""


_TRACE_OWNER_HEADING = "## Governed Attempt / Evaluation evidence"
_TRACE_CONTAINER_BEGIN = "<!-- PL_OPERATION_TRACE_ENTRIES_BEGIN -->"
_TRACE_CONTAINER_END = "<!-- PL_OPERATION_TRACE_ENTRIES_END -->"
_TRACE_ENTRY_BEGIN = "<!-- PL_OPERATION_TRACE_ENTRY_BEGIN -->"
_TRACE_ENTRY_END = "<!-- PL_OPERATION_TRACE_ENTRY_END -->"
_TRACE_OWNER_RE = re.compile(r"(?m)^## Governed Attempt / Evaluation evidence[ \t]*(?:\r?\n|\Z)")
_TRACE_H2_RE = re.compile(r"(?m)^##(?!#)[ \t]+")
_TRACE_ENTRY_FIELDS = {
    "operation_guidance_ref",
    "expected_route_operation_id",
    "expected_route_operation_class",
    "expected_route_id",
    "expected_route_outcome",
    "expected_route_reason_code",
    "expected_route_source_revision",
    "expected_route_authority_refs",
    "expected_route_selection_reason",
    "during_operation_ref",
    "during_completeness",
    "during_expansion_count",
    "actual_executor_receipt_ref",
    "actual_executor_receipt_id",
    "actual_executor_planning_lite_ref",
    "next_" + "gate_ref",
    "next_" + "gate_source_ref",
    "next_" + "gate_source_sha256",
}


@dataclass(frozen=True, slots=True)
class _PreTraceHandle:
    path: Path
    raw_sha256: str
    attempt_id: str


def _trace_newline(text: str) -> str:
    if "\r\n" in text:
        return "\r\n"
    if "\n" in text:
        return "\n"
    return "\n"


def _trace_progress_path(target_root: str | Path) -> Path:
    root = Path(target_root).expanduser().resolve()
    snapshot = capture_project_spine_snapshot(root)
    context_ref = snapshot.active_context_path.replace("\\", "/")
    expected = (".planning", "changes", "active", snapshot.active_change, "context.md")
    if tuple(context_ref.split("/")) != expected:
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD")
    context_path = root.joinpath(*expected)
    if not context_path.is_file():
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD")
    try:
        context_path.resolve().relative_to(root)
    except ValueError as exc:
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD") from exc
    progress_path = context_path.with_name("progress.md").resolve()
    try:
        progress_path.relative_to(root)
    except ValueError as exc:
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD") from exc
    if not progress_path.is_file():
        raise _TracePersistenceError("INVALID_CHANGE_SCAFFOLD")
    return progress_path


def _trace_owner_span(text: str) -> tuple[int, int]:
    owners = list(_TRACE_OWNER_RE.finditer(text))
    if len(owners) != 1:
        raise _TracePersistenceError("INVALID_TRACE_OWNER_SECTION")
    owner = owners[0]
    next_heading = _TRACE_H2_RE.search(text, owner.end())
    return owner.start(), next_heading.start() if next_heading is not None else len(text)


def _trace_initialize_container(text: str, section_end: int) -> str:
    section = text[:section_end]
    if section.count(_TRACE_CONTAINER_BEGIN) or section.count(_TRACE_CONTAINER_END):
        return text
    newline = _trace_newline(section)
    insertion = f"{_TRACE_CONTAINER_BEGIN}{newline}{_TRACE_CONTAINER_END}"
    if not section.endswith(("\r\n", "\n")):
        insertion = newline + insertion
    insertion += newline
    return text[:section_end] + insertion + text[section_end:]


def _trace_container_span(text: str) -> tuple[int, int, int, int]:
    section_start, section_end = _trace_owner_span(text)
    section = text[section_start:section_end]
    begins = [match.start() + section_start for match in re.finditer(re.escape(_TRACE_CONTAINER_BEGIN), section)]
    ends = [match.start() + section_start for match in re.finditer(re.escape(_TRACE_CONTAINER_END), section)]
    if len(begins) != 1 or len(ends) != 1 or begins[0] > ends[0]:
        raise _TracePersistenceError("MALFORMED_TRACE_CONTAINER")
    container_begin_end = begins[0] + len(_TRACE_CONTAINER_BEGIN)
    if _TRACE_CONTAINER_BEGIN in text[container_begin_end:ends[0]] or _TRACE_CONTAINER_END in text[container_begin_end:ends[0]]:
        raise _TracePersistenceError("MALFORMED_TRACE_CONTAINER")
    for marker in (_TRACE_ENTRY_BEGIN, _TRACE_ENTRY_END):
        if marker in text[section_start:begins[0]] or marker in text[ends[0] + len(_TRACE_CONTAINER_END):section_end]:
            raise _TracePersistenceError("MALFORMED_TRACE_MARKERS")
    return begins[0], container_begin_end, ends[0], ends[0] + len(_TRACE_CONTAINER_END)


def _trace_entries(text: str) -> list[tuple[int, int, dict[str, Any]]]:
    begin, begin_end, end, _ = _trace_container_span(text)
    content = text[begin_end:end]
    markers = list(re.finditer(re.escape(_TRACE_ENTRY_BEGIN) + "|" + re.escape(_TRACE_ENTRY_END), content))
    if len(markers) % 2:
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY_MARKERS")
    entries: list[tuple[int, int, dict[str, Any]]] = []
    for index in range(0, len(markers), 2):
        opening, closing = markers[index], markers[index + 1]
        if opening.group(0) != _TRACE_ENTRY_BEGIN or closing.group(0) != _TRACE_ENTRY_END:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY_MARKERS")
        raw_start = begin_end + opening.start()
        raw_end = begin_end + closing.end()
        body = content[opening.end():closing.start()]
        entry = _trace_parse_entry(body)
        entries.append((raw_start, raw_end, entry))
    attempt_ids = [entry.get("attempt_id") for _, _, entry in entries]
    if len(attempt_ids) != len(set(attempt_ids)):
        raise _TracePersistenceError("DUPLICATE_TRACE_ATTEMPT")
    return entries


def _trace_parse_entry(body: str) -> dict[str, Any]:
    result: dict[str, Any] = {}
    attempt_count = 0
    attempt_pattern = re.compile(r"^[ \t]*- Attempt ref: `([^`\r\n]+)`[ \t]*(?:\r)?$", re.MULTILINE)
    for match in attempt_pattern.finditer(body):
        attempt_count += 1
        result["attempt_id"] = match.group(1)
    for line in body.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("- Attempt ref:"):
            continue
        field_match = re.fullmatch(r"- ([a-z][a-z0-9_]*)[ \t]*:[ \t]*(.*)", stripped)
        if field_match is None:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
        key, raw_value = field_match.groups()
        if key not in _TRACE_ENTRY_FIELDS or key in result:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
        try:
            result[key] = json.loads(raw_value)
        except (TypeError, ValueError, json.JSONDecodeError) as exc:
            raise _TracePersistenceError("MALFORMED_TRACE_ENTRY") from exc
    if attempt_count != 1 or "attempt_id" not in result:
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
    return result


def _trace_format_entry(entry: Mapping[str, Any], newline: str) -> str:
    attempt_id = entry.get("attempt_id")
    if not isinstance(attempt_id, str) or not attempt_id:
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
    lines = [f"{_TRACE_ENTRY_BEGIN}", f"- Attempt ref: `{attempt_id}`"]
    order = (
        "operation_guidance_ref",
        "expected_route_operation_id",
        "expected_route_operation_class",
        "expected_route_id",
        "expected_route_outcome",
        "expected_route_reason_code",
        "expected_route_source_revision",
        "expected_route_authority_refs",
        "expected_route_selection_reason",
        "during_operation_ref",
        "during_completeness",
        "during_expansion_count",
        "actual_executor_receipt_ref",
        "actual_executor_receipt_id",
        "actual_executor_planning_lite_ref",
        "next_" + "gate_ref",
        "next_" + "gate_source_ref",
        "next_" + "gate_source_sha256",
    )
    for key in order:
        if key in entry:
            try:
                value = json.dumps(entry[key], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            except (TypeError, ValueError) as exc:
                raise _TracePersistenceError("MALFORMED_TRACE_ENTRY") from exc
            lines.append(f"- {key}: {value}")
    if set(entry) - ({"attempt_id"} | _TRACE_ENTRY_FIELDS):
        raise _TracePersistenceError("MALFORMED_TRACE_ENTRY")
    lines.append(_TRACE_ENTRY_END)
    return newline.join(lines)


def _trace_replace_entry(text: str, entry: Mapping[str, Any], *, existing: tuple[int, int, dict[str, Any]] | None) -> str:
    newline = _trace_newline(text)
    serialized = _trace_format_entry(entry, newline)
    if existing is not None:
        start, end, _ = existing
        return text[:start] + serialized + text[end:]
    _, _, container_end, _ = _trace_container_span(text)
    prefix = text[:container_end]
    if not prefix.endswith(("\r\n", "\n")):
        prefix += newline
    return prefix + serialized + newline + text[container_end:]


def _trace_read(path: Path, *, initialize_legacy: bool) -> tuple[bytes, str, list[tuple[int, int, dict[str, Any]]]]:
    try:
        raw = path.read_bytes()
        text = raw.decode("utf-8")
        section_start, section_end = _trace_owner_span(text)
        section = text[section_start:section_end]
        if section.count(_TRACE_CONTAINER_BEGIN) == 0 and section.count(_TRACE_CONTAINER_END) == 0:
            if not initialize_legacy:
                raise _TracePersistenceError("MISSING_TRACE_CONTAINER")
            text = _trace_initialize_container(text, section_end)
        elif section.count(_TRACE_CONTAINER_BEGIN) != 1 or section.count(_TRACE_CONTAINER_END) != 1:
            raise _TracePersistenceError("MALFORMED_TRACE_CONTAINER")
        entries = _trace_entries(text)
        return raw, text, entries
    except _TracePersistenceError:
        raise
    except (OSError, UnicodeError) as exc:
        raise _TracePersistenceError("TRACE_PROGRESS_READ_FAILED") from exc


def _trace_atomic_replace(path: Path, raw: bytes) -> None:
    temporary: str | None = None
    try:
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=str(path.parent))
        with os.fdopen(fd, "wb") as handle:
            handle.write(raw)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        temporary = None
    except OSError as exc:
        raise _TracePersistenceError("TRACE_PROGRESS_ATOMIC_WRITE_FAILED") from exc
    finally:
        if temporary is not None:
            try:
                os.unlink(temporary)
            except OSError:
                pass


def _trace_persist_pre(
    target_root: str | Path,
    attempt_id: str,
    guidance: OperationGuidanceV1,
    operation_guidance_ref: str | None,
    operation_depth_observation: OperationDepthObservationV1 | None,
) -> _PreTraceHandle:
    path = _trace_progress_path(target_root)
    raw, text, entries = _trace_read(path, initialize_legacy=True)
    existing = next((item for item in entries if item[2].get("attempt_id") == attempt_id), None)
    if existing is not None:
        raise _TracePersistenceError("DUPLICATE_TRACE_ATTEMPT")
    entry = record_governed_attempt_evidence(
        "PRE",
        attempt_id,
        operation_guidance_ref=operation_guidance_ref,
        guidance=guidance,
        operation_depth_observation=operation_depth_observation,
    )
    new_text = _trace_replace_entry(text, entry, existing=None)
    new_raw = new_text.encode("utf-8")
    _trace_atomic_replace(path, new_raw)
    try:
        reread = path.read_bytes()
        _, reread_text, reread_entries = _trace_read(path, initialize_legacy=False)
    except (OSError, UnicodeError, _TracePersistenceError) as exc:
        raise _TracePersistenceError("TRACE_PROGRESS_READBACK_FAILED") from exc
    matching = [item for item in reread_entries if item[2].get("attempt_id") == attempt_id]
    if len(matching) != 1 or matching[0][2] != dict(entry):
        raise _TracePersistenceError("TRACE_PRE_READBACK_MISMATCH")
    _ = reread_text
    return _PreTraceHandle(path, hashlib.sha256(reread).hexdigest(), attempt_id)


def _trace_persist_post(
    handle: _PreTraceHandle,
    persisted_receipt: Mapping[str, Any],
    post_spine_snapshot: ProjectSpineSnapshotV1,
) -> OperationTraceView:
    current_raw = handle.path.read_bytes()
    if hashlib.sha256(current_raw).hexdigest() != handle.raw_sha256:
        raise _TracePersistenceError("STALE_PROGRESS")
    _, text, entries = _trace_read(handle.path, initialize_legacy=False)
    matching = [item for item in entries if item[2].get("attempt_id") == handle.attempt_id]
    if len(matching) != 1:
        raise _TracePersistenceError("MISSING_PRE_TRACE")
    receipt_id = persisted_receipt.get("receipt_id")
    if not isinstance(receipt_id, str) or not receipt_id:
        raise _TracePersistenceError("INCOMPLETE_EXECUTOR_RECEIPT")
    receipt_ref = f"{handle.path.as_posix()}#receipt_id={receipt_id}"
    entry = record_governed_attempt_evidence(
        "POST",
        handle.attempt_id,
        matching[0][2],
        receipt_ref=receipt_ref,
        validated_receipt=persisted_receipt,
        **{
            "next_" + "gate_ref": post_spine_snapshot.next_permitted_action,
            "next_" + "gate_source_ref": ".planning/ACTIVE.md#Active change/Next permitted action",
            "next_" + "gate_source_sha256": post_spine_snapshot.active_sha256.lower(),
        },
    )
    new_text = _trace_replace_entry(text, entry, existing=matching[0])
    _trace_atomic_replace(handle.path, new_text.encode("utf-8"))
    _, reread_text, reread_entries = _trace_read(handle.path, initialize_legacy=False)
    _ = reread_text
    final = [item[2] for item in reread_entries if item[2].get("attempt_id") == handle.attempt_id]
    if len(final) != 1 or final[0] != dict(entry):
        raise _TracePersistenceError("TRACE_POST_READBACK_MISMATCH")
    expected_ref = receipt_ref
    return read_operation_trace_evidence(
        final[0], lambda ref: dict(persisted_receipt) if ref == expected_ref else None
    )


def execute_governed_operation(
    target: str | Path,
    attempt_id: str,
    *,
    target_root: str | Path,
    pre_execution_project_spine_snapshot: ProjectSpineSnapshotV1,
    guidance: OperationGuidanceV1 | Mapping[str, Any] | None = None,
    bounded_payload: object = None,
    completion: GovernedExecutionCompletionV1 | Mapping[str, Any] | None = None,
    receipt: Mapping[str, Any] | None = None,
    receipt_path: str | Path | None = None,
    registered_project_id: str | None = None,
    home: str | Path | None = None,
    telemetry_enabled: bool | None = None,
    payload_schema_ref: str = "payload.v1",
    authority_refs: Sequence[str] | None = None,
    guidance_ref: str | None = None,
    operation_depth_observation: OperationDepthObservationV1 | None = None,
) -> GovernedLifecycleResultV1:
    """Run the exact lookup→claim→execute→receipt→terminal→PL08 order."""

    root = Path(target).expanduser().resolve()
    lookup = lookup_attempt(root, attempt_id)
    if lookup.outcome is not LookupOutcome.FOUND or lookup.attempt is None:
        return _stopped(attempt_id, "AUTHORITATIVE_ATTEMPT_LOOKUP", lookup.outcome.value)
    admissibility = check_activation_admissibility(root, attempt_id)
    if admissibility.outcome is not AdmissibilityOutcome.ADMISSIBLE:
        return _stopped(attempt_id, "ATTEMPT_ADMISSIBILITY", admissibility.outcome.value)
    try:
        claimed = claim_attempt(root, attempt_id)
    except AttemptRuntimeError as exc:
        return _stopped(attempt_id, "ATTEMPT_CLAIM", type(exc).__name__)
    attempt = claimed.attempt

    selected_guidance: OperationGuidanceV1 | None
    if guidance is None:
        return _stopped(attempt_id, "OPERATION_GUIDANCE", "GUIDANCE_REQUIRED")
    selected_guidance = guidance  # exact supplied PL07 projection; no reselection
    if not isinstance(selected_guidance, Mapping) or selected_guidance.get("outcome") != "MATCHED":
        return _stopped(attempt_id, "OPERATION_GUIDANCE", "GUIDANCE_NOT_MATCHED")

    pre_trace: _PreTraceHandle | None = None
    try:
        pre_trace = _trace_persist_pre(
            target_root,
            attempt.attempt_id,
            selected_guidance,
            attempt.operation_guidance_ref,
            operation_depth_observation,
        )
    except Exception:
        # Progress evidence is derived and non-authoritative.  Its absence or
        # failure must not alter the governed execution decision.
        pre_trace = None

    execution = invoke_governed_operation(
        attempt,
        selected_guidance,
        bounded_payload,
        completion,
        payload_schema_ref,
        authority_refs,
        guidance_ref,
    )
    envelope: GovernedExecutionEnvelopeV1 | None = None
    if execution.envelope_digest is not None:
        try:
            envelope = prepare_governed_operation(
                attempt,
                selected_guidance,
                bounded_payload,
                payload_schema_ref,
                authority_refs,
                guidance_ref,
            )
        except GovernedExecutorError:
            envelope = None
    if not execution.accepted or execution.completion is None:
        return _stopped(
            attempt_id,
            "GOVERNED_EXECUTOR_COMPLETION",
            execution.failure_category or "EXECUTION_REJECTED",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    typed = _typed_completion(execution.completion)
    if typed is None or not _evaluation_carriers_valid(typed):
        return _stopped(
            attempt_id,
            "TYPED_EVALUATION_CARRIERS",
            "INVALID_CONTRACT_OR_FIXTURE",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    if receipt is None:
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_COLLECTION",
            "RECEIPT_MISSING",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    if receipt.get("receipt_id") != typed.receipt_id if typed.receipt_id is not None else False:
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_IDENTITY",
            "RECEIPT_ID_MISMATCH",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    try:
        project_id, path, registered_enabled = _receipt_context(
            root,
            registered_project_id=registered_project_id,
            receipt_path=receipt_path,
            home=home,
        )
        enabled = registered_enabled if telemetry_enabled is None else telemetry_enabled
        persisted = collect_governed_receipt(
            receipt,
            project_root=root,
            receipt_path=path,
            registered_project_id=project_id,
            attempt_id=attempt.attempt_id,
            execution_invocation_id=execution.execution_invocation_id or "",
            enabled=enabled,
        )
    except (ReceiptError, WorkspaceError, OSError, ValueError) as exc:
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_COLLECTION",
            type(exc).__name__,
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
        )
    if (
        persisted.get("schema_version") != 2
        or persisted.get("receipt_id") != receipt.get("receipt_id")
        or persisted.get("attempt_id") != attempt.attempt_id
        or persisted.get("execution_invocation_id") != execution.execution_invocation_id
        or typed.receipt_id is not None and persisted.get("receipt_id") != typed.receipt_id
    ):
        return _stopped(
            attempt_id,
            "GOVERNED_RECEIPT_IDENTITY",
            "IDENTITY_TRIANGLE_MISMATCH",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
            receipt=persisted,
        )

    observed = ObservedResultV1(
        result_id=typed.result_id,
        attempt_id=attempt.attempt_id,
        execution_status=typed.execution_status,
        changed_paths=typed.changed_paths,
        fact_refs=typed.fact_refs,
        artifact_refs=typed.artifact_refs,
    )
    try:
        terminal = terminalize_attempt(root, attempt.attempt_id, observed)
    except AttemptRuntimeError as exc:
        return _stopped(
            attempt_id,
            "ATTEMPT_TERMINALIZATION",
            type(exc).__name__,
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
            receipt=persisted,
        )
    technical = evaluate_technical(
        attempt=attempt,
        contracts=typed.verifier_contracts,
        evidence=typed.verifier_evidence,
        findings=typed.findings,
        acceptance_contract_ref=attempt.acceptance_contract_ref,
        evaluation_scope_ref=typed.evaluation_scope_ref,
        acceptance_contract=typed.acceptance_contract,
        supersession=typed.supersession,
        evaluation_id=typed.evaluation_id,
        evaluation_run=typed.evaluation_run,
        candidate_quality=typed.candidate_quality,
    )
    checkpoint = PostEvaluationCheckpointV1(
        attempt_id=attempt.attempt_id,
        result_id=observed.result_id,
        evaluation_id=technical.evaluation_id,
        evaluation_outcome=technical.outcome,
        evaluation_reason_codes=technical.reason_codes,
    )
    post_spine_snapshot: ProjectSpineSnapshotV1
    try:
        post_spine_snapshot = record_post_evaluation_checkpoint(
            target_root,
            pre_execution_snapshot=pre_execution_project_spine_snapshot,
            checkpoint=checkpoint,
            operation_guidance=selected_guidance,
        )
        downstream = build_compact_status(target_root, attempt_id=attempt.attempt_id)
        if downstream.get("what_next") != pre_execution_project_spine_snapshot.next_permitted_action:
            raise ProjectSpineHandoffError("post-PL08 compact status is not authoritative")
    except (ProjectSpineHandoffError, OSError, ValueError, KeyError, TypeError) as exc:
        return _stopped(
            attempt_id,
            "PL08 Result/Evidence -> authoritative Next Gate",
            "PROJECT_SPINE_HANDOFF",
            guidance=selected_guidance,
            envelope=envelope,
            execution=execution,
            receipt=persisted,
            observed_result=observed,
            technical_evaluation=technical,
            terminal_attempt=terminal,
        )
    if pre_trace is not None:
        try:
            _trace_persist_post(pre_trace, persisted, post_spine_snapshot)
        except Exception:
            # A stale or malformed trace cannot roll back facts already owned
            # by receipt, Attempt Runtime, PL08, or Project Spine.
            pass
    return GovernedLifecycleResultV1(
        disposition="COMPLETED_WITH_FACTS",
        attempt_id=attempt.attempt_id,
        guidance=selected_guidance,
        envelope=envelope,
        execution=execution,
        receipt=dict(persisted),
        observed_result=observed,
        technical_evaluation=technical,
        terminal_attempt=terminal,
        downstream=downstream,
    )


run_governed_operation = execute_governed_operation
execute_operation_lifecycle = execute_governed_operation


__all__ = [
    "GovernedLifecycleResultV1",
    "OperationLifecycleError",
    "execute_governed_operation",
    "execute_operation_lifecycle",
    "run_governed_operation",
]
