from __future__ import annotations

import hashlib
import json
import base64
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Mapping

import pytest

import planning_lite.dependency_admission as dependency_admission_module
from planning_lite.attempt_evaluation import (
    AcceptanceContractV1,
    AttemptRecordV1,
    CandidateIdentityV1,
    EvidenceApplicabilityV1,
    EvidenceSupersessionV1,
    FindingApplicabilityV1,
    FindingV1,
    IdentityRefV1,
    ObservedResultV1,
    VerifierContractV1,
    VerifierEvidenceV1,
    evaluate_technical,
)
from planning_lite.dependency_admission import (
    CancellationCarrierError,
    CancellationTombstoneV1,
    CapturedJsonValueV1,
    EvidenceContentCarrierV1,
    _DependencyArtifactCarrierV1,
    DependencyAdmissionError,
    DependencyAcceptanceProofV1,
    DependencyProofCarrierError,
    DependencyProofError,
    _artifact_carrier_path,
    cancellation_tombstone_path,
    cancellation_tombstone_ref,
    capture_dependency_acceptance_proof,
    decode_dependency_acceptance_proof,
    decode_cancellation_tombstone,
    encode_dependency_acceptance_proof,
    build_dependency_admission,
    validate_dependency_admission,
    dependency_acceptance_proof_path,
    publish_dependency_acceptance_proof_blob,
    resolve_dependency_acceptance_proof_blob,
    encode_cancellation_tombstone,
    historical_use_is_valid,
    _publish_cancellation_tombstone_locked,
    publish_evidence_content,
    resolve_evidence_content,
    _dependency_artifact_carrier_ref,
    _resolve_dependency_artifact_carrier,
    resolve_cancellation_tombstone,
    resolve_dependency,
)
from planning_lite.plan_compilation import canonical_json
from planning_lite.workspace import resolve_dependency_artifact_output_route


CHANGE_ID = "CHG-TEST-DEPENDENCY-001"
REPO_ROOT = Path(__file__).parents[1]
CONTRACT = {
    "schema_version": 2,
    "source_task_id": "T-01",
    "target_task_id": "T-02",
    "accepted_output_contract_ref": "acceptance:output-v1",
    "produced_artifact_logical_ref": "artifact:build",
    "required_input_logical_ref": "artifact:build-input",
    "acceptance_contract_ref": "acceptance:build-v1",
    "evaluation_scope_ref": "scope:build-v1",
    "required_verifier_contract_refs": [
        {"contract_id": "build", "contract_version_or_ref": "v1"}
    ],
}


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _task_rows(*, t03_outcome: str = "Inspect independent path", edge_to_t03: bool = False) -> list[dict[str, str]]:
    return [
        {
            "id": "T-01",
            "outcome": "Produce governed artifact",
            "slice": "Tracer bullet",
            "edge": "None",
            "verification": "focused producer test",
            "blast": "source task",
            "status": "Pending",
        },
        {
            "id": "T-02",
            "outcome": "Consume governed artifact",
            "slice": "Tracer bullet",
            "edge": "T-01",
            "verification": "focused consumer test",
            "blast": "successor task",
            "status": "Pending",
        },
        {
            "id": "T-03",
            "outcome": t03_outcome,
            "slice": "Expand-contract",
            "edge": "T-01" if edge_to_t03 else "None",
            "verification": "independent test",
            "blast": "independent task",
            "status": "Pending",
        },
        {
            "id": "T-04",
            "outcome": "A second independent task",
            "slice": "Tracer bullet",
            "edge": "None",
            "verification": "second independent test",
            "blast": "independent task",
            "status": "Pending",
        },
    ]


def _task_semantics(row: dict[str, str]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "outcome": row["outcome"],
        "slice_type": row["slice"],
        "blocking_edges": [] if row["edge"] == "None" else [row["edge"]],
        "verification": row["verification"],
        "blast_radius": row["blast"],
    }


def _task_table(rows: list[dict[str, str]]) -> str:
    template = (REPO_ROOT / "template/.planning/changes/templates/tasks.md").read_text(encoding="utf-8")
    lines = template.splitlines()
    header_index = lines.index("| ID | Outcome | Slice type | Blocking edge | Verification seam / command | Blast radius | Status |")
    prefix = lines[:header_index + 2]
    postamble_start = next(index for index in range(header_index + 2, len(lines)) if lines[index].startswith("Allowed status values:"))
    lines = prefix
    lines.extend(
        f"| `{row['id']}` | {row['outcome']} | `{row['slice']}` | `{row['edge']}` | {row['verification']} | {row['blast']} | `{row['status']}` |"
        for row in rows
    )
    lines.extend(["", *template.splitlines()[postamble_start:]])
    return "\n".join(lines) + "\n"


def _effect(amendment_id: str, changed: dict[str, tuple[Any, Any]], *, kind: str = "Scope") -> dict[str, Any]:
    paths = sorted(changed)
    return {
        "id": amendment_id,
        "kind": kind,
        "changed": paths,
        "before": {path: changed[path][0] for path in paths},
        "after": {path: changed[path][1] for path in paths},
    }


def _amendment_text(
    rows: list[dict[str, Any]], receipt: dict[str, Any], *, change_id: str = CHANGE_ID
) -> str:
    text = (REPO_ROOT / "template/.planning/changes/templates/amendments.md").read_text(encoding="utf-8")
    lines = text.splitlines()
    header_index = lines.index("| Date | Amendment ID | Type | Trigger and evidence | Old approach | New approach | Approval | Readiness impact | Changed dependency fields | Before values | After values |")
    separator_index = header_index + 1
    if not lines[separator_index].startswith("|---"):
        raise AssertionError("managed amendments template has no table separator")
    rendered_rows: list[str] = []
    for row in rows:
        if row["changed"]:
            before = {path: row["before"][path] for path in row["changed"]}
            after = {path: row["after"][path] for path in row["changed"]}
        else:
            before = {}
            after = {}
        cells = [
            "2026-10-04",
            row["id"],
            row["kind"],
            f"Evidence for {row['id']}",
            "Prior governed value",
            "Authorized current value",
            "Owner approval ref",
            "Readiness reviewed",
            canonical_json(row["changed"]),
            canonical_json(before),
            canonical_json(after),
        ]
        rendered_rows.append("| " + " | ".join(cells) + " |")
    lines[separator_index + 1:separator_index + 1] = rendered_rows + [""]
    text = "\n".join(lines) + "\n"
    text = text.replace("CHG-NNNN", change_id)
    text, count = re.subn(
        r"(?s)(## Dependency reconciliation receipt\n\n```json\n)(.*?)(\n```)",
        lambda match: match.group(1) + canonical_json(receipt) + match.group(3),
        text,
    )
    if count != 1:
        raise AssertionError("managed amendments template must contain one final receipt")
    return text


def _expected_dependent(change_id: str, contract: dict[str, Any], semantics: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[str, Any]:
    effects = []
    dependent_fields = {
        "accepted_output_contract_ref",
        "produced_artifact_logical_ref",
        "required_input_logical_ref",
        "acceptance_contract_ref",
        "evaluation_scope_ref",
        "required_verifier_contract_refs",
        "source_task_semantics",
        "target_task_semantics",
    }
    for row in rows:
        paths = [path for path in row["changed"] if path in dependent_fields]
        if paths:
            effects.append(
                {
                    "amendment_id": row["id"],
                    "changed_dependency_fields": paths,
                    "before_values": {path: row["before"][path] for path in paths},
                    "after_values": {path: row["after"][path] for path in paths},
                }
            )
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
        "source_task_semantics": semantics[0],
        "target_task_semantics": semantics[1],
        "dependency_material_amendments": effects,
    }


def _write_fixture(
    root: Path,
    *,
    planning_root: str = ".planning",
    change_id: str = CHANGE_ID,
    contract: dict[str, Any] | None = None,
    task_rows: list[dict[str, str]] | None = None,
    amendments: list[dict[str, Any]] | None = None,
) -> Path:
    """Build complete governed inputs below the selected effective root.

    This fixture constructor supplies explicit approval metadata, derives the
    semantic hashes, renders governed amendment records, and closes their final
    reconciliation receipt. ``planning_root`` controls both the canonical
    ACTIVE pointer and product-root-relative Change refs so custom-root tests
    exercise the same authority location as production. It is evidence
    construction, not an alternate governance authority or resolver shortcut.
    """
    contract = json.loads(json.dumps(contract if contract is not None else CONTRACT))
    task_rows = task_rows if task_rows is not None else _task_rows()
    amendments = amendments if amendments is not None else []
    governance_root = root / planning_root
    folder = governance_root / "changes" / "active" / change_id
    folder.mkdir(parents=True)
    (governance_root / "ACTIVE.md").write_text(
        "# Active state\n\n## Active change\n\n"
        f"- Change: `{change_id}`\n- Change status: `In progress`\n",
        encoding="utf-8",
        newline="\n",
    )
    proposal = (REPO_ROOT / "template/.planning/changes/templates/proposal.md").read_text(encoding="utf-8")
    proposal = proposal.replace("CHG-NNNN: Change title", f"{change_id}: Dependency test", 1)
    proposal = proposal.replace("- Status: `Draft / Approved / Deferred / Rejected`", "- Status: `Approved`", 1)
    (folder / "proposal.md").write_text(proposal, encoding="utf-8", newline="\n")
    plan = (REPO_ROOT / "template/.planning/changes/templates/plan.md").read_text(encoding="utf-8")
    plan = plan.replace("- Status: `Draft / Approved`", "- Status: `Approved`", 1)
    plan = plan.replace("- Approved by:", "- Approved by: Test owner", 1)
    plan = plan.replace("- Approval evidence:", "- Approval evidence: decision:test-owner", 1)
    plan = plan.replace("- Approval date:", "- Approval date: 2026-10-04", 1)
    plan = plan.replace("## Approved outcome and exclusions\n", "## Approved outcome and exclusions\n\nA bounded dependency test fixture.\n", 1)
    contract_match = re.search(r"(?s)(```json\n)(.*?)(\n```)", plan)
    if contract_match is None:
        raise AssertionError("managed Plan template has no dependency contract example")
    plan = plan[:contract_match.start(2)] + canonical_json(contract) + plan[contract_match.end(2):]
    tasks_text = _task_table(task_rows)
    semantics = [_task_semantics(row) for row in task_rows]
    dependent = _expected_dependent(change_id, contract, semantics, amendments)
    dependent_digest = _sha(canonical_json(dependent).encode("utf-8"))
    plan_sem_start = plan.index("## Approved outcome and exclusions")
    plan_semantics_sha256 = _sha(plan[plan_sem_start:].encode("utf-8"))
    task_semantics_sha256 = _sha(canonical_json(semantics).encode("utf-8"))
    amendments_placeholder = {
        "schema_version": 1,
        "change_id": change_id,
        "status": "RECONCILED",
        "approved_plan_digest": "0" * 64,
        "dependency_semantic_digest": dependent_digest,
        "amendments_semantics_sha256": "0" * 64,
        "applicable_dependency_material_amendment_ids": [effect["id"] for effect in amendments if any(path in {
            "accepted_output_contract_ref", "produced_artifact_logical_ref", "required_input_logical_ref",
            "acceptance_contract_ref", "evaluation_scope_ref", "required_verifier_contract_refs",
            "source_task_semantics", "target_task_semantics",
        } for path in effect["changed"])],
    }
    amendment_text = _amendment_text(amendments, amendments_placeholder, change_id=change_id)
    receipt_heading = amendment_text.index("## Dependency reconciliation receipt")
    amendments_semantics_sha256 = _sha(amendment_text[:receipt_heading].encode("utf-8"))
    root_ref = "" if planning_root == "." else planning_root.rstrip("/")
    change_ref = f"{root_ref}/changes/active/{change_id}" if root_ref else f"changes/active/{change_id}"
    approval = {
        "schema_version": 1,
        "change_id": change_id,
        "plan_ref": f"{change_ref}/plan.md",
        "tasks_ref": f"{change_ref}/tasks.md",
        "amendments_ref": f"{change_ref}/amendments.md",
        "plan_semantics_sha256": plan_semantics_sha256,
        "task_semantics_sha256": task_semantics_sha256,
        "amendments_semantics_sha256": amendments_semantics_sha256,
        "dependency_semantic_digest": dependent_digest,
    }
    approved_digest = _sha(canonical_json(approval).encode("utf-8"))
    plan = plan.replace("<64 lowercase hex>", approved_digest, 1).replace("<64 lowercase hex>", dependent_digest, 1)
    final_receipt = {
        "schema_version": 1,
        "change_id": change_id,
        "status": "RECONCILED",
        "approved_plan_digest": approved_digest,
        "dependency_semantic_digest": dependent_digest,
        "amendments_semantics_sha256": amendments_semantics_sha256,
        "applicable_dependency_material_amendment_ids": amendments_placeholder["applicable_dependency_material_amendment_ids"],
    }
    amendment_text = _amendment_text(amendments, final_receipt, change_id=change_id)
    (folder / "plan.md").write_text(plan, encoding="utf-8", newline="\n")
    (folder / "tasks.md").write_text(tasks_text, encoding="utf-8", newline="\n")
    (folder / "amendments.md").write_text(amendment_text, encoding="utf-8", newline="\n")
    return root


def _expect_error(code: str, action: Any) -> None:
    with pytest.raises(DependencyAdmissionError) as exc:
        action()
    assert exc.value.code == code


def _capture_inputs() -> dict[str, Any]:
    """Create exact live-owner PL08 values, including inapplicable ordered inputs."""
    attempt_id = f"{CHANGE_ID}/T-01/A1"
    candidate = CandidateIdentityV1("GIT_COMMIT", "1" * 40)
    baselines = (IdentityRefV1("baseline:main", "baseline-main"),)
    contract_ref = "acceptance:build-v1"
    scope_ref = "scope:build-v1"
    contract = VerifierContractV1(
        contract_ref, "build", "v1", True, "AUTOMATED_TEST",
        "All required checks pass", ("evidence-content:build",), "Block on missing or non-pass evidence",
    )
    acceptance = AcceptanceContractV1(contract_ref, (contract,))
    attempt = AttemptRecordV1(
        attempt_id, CHANGE_ID, "T-01", 1, "authz:test", contract_ref,
        candidate, baselines, verifier_contract_refs=(("build", "v1"),),
    )
    applicable = EvidenceApplicabilityV1(
        attempt_id, candidate, contract_ref, "build", "v1", scope_ref,
        input_baseline_refs=baselines,
    )
    inapplicable = EvidenceApplicabilityV1(
        attempt_id, candidate, contract_ref, "build", "v1", "scope:other",
        input_baseline_refs=baselines,
    )
    effective_evidence = VerifierEvidenceV1(
        "evidence:build:pass", attempt_id, candidate, "build", "v1", "PASS",
        ("evidence-content:build",), applicable, ("claim:build",),
    )
    other_evidence = VerifierEvidenceV1(
        "evidence:build:other-scope", attempt_id, candidate, "build", "v1", "NOT_RUN",
        ("evidence-content:other-scope",), inapplicable, (),
    )
    relation = EvidenceSupersessionV1(
        "evidence:historical:prior", "evidence:historical:successor",
        "scope:other", ("claim:historical",), "Captured but not applicable to this scope.",
    )
    finding = FindingV1(
        "finding:other-scope", "A non-applicable observation.", "NON_MATERIAL",
        ("VERIFICATION_TEST_COVERAGE",), "NON_BLOCKING", "OPEN",
        ("evidence-content:finding",), None,
        FindingApplicabilityV1(attempt_id, candidate, contract_ref, "scope:other", baselines),
    )
    technical = evaluate_technical(
        attempt, (contract,), (other_evidence, effective_evidence), (finding,),
        acceptance_contract_ref=contract_ref, evaluation_scope_ref=scope_ref,
        acceptance_contract=acceptance, supersession=(relation,), evaluation_id="evaluation:build:1",
    )
    assert technical.outcome == "SATISFIED"
    result = ObservedResultV1(
        "result:build:1", attempt_id, "COMPLETED", artifact_refs=(CONTRACT["produced_artifact_logical_ref"],)
    )
    evaluation_input = {
        "attempt_id": attempt_id,
        "candidate_identity": candidate.to_mapping(),
        "baseline_refs": [item.to_mapping() for item in baselines],
        "acceptance_contract_ref": contract_ref,
        "verifier_contract_refs": [{"contract_id": "build", "contract_version_or_ref": "v1"}],
        "evaluation_id": "evaluation:build:1",
        "evaluation_scope_ref": scope_ref,
        "evaluation_run": True,
        "candidate_quality": True,
    }
    return {
        "observed_result": result,
        "attempt_evaluation_input": evaluation_input,
        "acceptance_contract": acceptance,
        "verifier_evidence_inputs": (other_evidence, effective_evidence),
        "evidence_supersession_inputs": (relation,),
        "finding_inputs": (finding,),
        "technical_evaluation": technical,
    }


def _publish_fixture_evidence_content(
    root: Path,
    inputs: Mapping[str, Any],
    *,
    carrier_payloads: Mapping[str, bytes] | None = None,
    skip_carrier_refs: tuple[str, ...] = (),
) -> None:
    """Publish test-only Class-B fixtures from the exact supplied PL08 values."""
    def owner_mapping(value: Any) -> dict[str, Any]:
        return value.to_mapping() if hasattr(value, "to_mapping") else dict(value)

    verifier_values = [owner_mapping(value) for value in inputs["verifier_evidence_inputs"]]
    finding_values = [owner_mapping(value) for value in inputs["finding_inputs"]]
    supersession_values = [owner_mapping(value) for value in inputs["evidence_supersession_inputs"]]
    evidence_by_id = {value["evidence_id"]: value for value in verifier_values}
    refs: set[str] = {
        ref for value in verifier_values for ref in value["evidence_refs"]
    } | {
        ref for value in finding_values for ref in value["evidence_refs"]
    }
    for relation in supersession_values:
        for ref in (relation["prior_evidence_ref"], relation["successor_evidence_ref"]):
            if ref not in evidence_by_id:
                refs.add(ref)
    supplied = dict(carrier_payloads or {})
    for ref in sorted(refs):
        if ref in skip_carrier_refs:
            continue
        if ref in supplied:
            exact_bytes = supplied[ref]
        elif ref in evidence_by_id:
            exact_bytes = canonical_json(evidence_by_id[ref]).encode("utf-8")
        else:
            exact_bytes = ("fixture evidence bytes:" + ref).encode("utf-8")
        publish_evidence_content(root, ref, exact_bytes)


def _evidence_content_path_for_test(root: Path, evidence_ref: str) -> Path:
    route = resolve_dependency_artifact_output_route(root)
    locator = hashlib.sha256(evidence_ref.encode("utf-8")).hexdigest()
    return (
        route.effective_planning_root / "changes" / "active" / ".planning-lite"
        / "dependency-admission" / "evidence-content-v1" / f"{locator}.json"
    )


def _carrier_mapping_for_test(evidence_ref: str, exact_raw_bytes: bytes) -> dict[str, Any]:
    digest = hashlib.sha256(exact_raw_bytes).hexdigest()
    return {
        "schema_version": 1,
        "evidence_ref": evidence_ref,
        "content_identity": "econtent_" + digest,
        "content_digest": digest,
        "content_base64": base64.b64encode(exact_raw_bytes).decode("ascii"),
    }


def _write_carrier_bytes(root: Path, evidence_ref: str, raw: bytes) -> Path:
    path = _evidence_content_path_for_test(root, evidence_ref)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(raw)
    return path


def _capture_proof(
    root: Path,
    *,
    publish_carriers: bool = True,
    carrier_payloads: Mapping[str, bytes] | None = None,
    skip_carrier_refs: tuple[str, ...] = (),
    **overrides: Any,
):
    route = resolve_dependency_artifact_output_route(root)
    route.path.parent.mkdir(parents=True, exist_ok=True)
    route.path.write_bytes(b"\x00artifact\r\nbytes\xff")
    inputs = _capture_inputs()
    inputs.update(overrides)
    if publish_carriers:
        _publish_fixture_evidence_content(
            root, inputs, carrier_payloads=carrier_payloads, skip_carrier_refs=skip_carrier_refs
        )
    return capture_dependency_acceptance_proof(root, **inputs)


def test_cancellation_tombstone_codec_and_carrier_are_exact_and_immutable(tmp_path: Path) -> None:
    record = CancellationTombstoneV1(CHANGE_ID)
    raw = encode_cancellation_tombstone(record)
    expected_mapping = {
        "schema_version": 1,
        "change_id": CHANGE_ID,
        "source_task_id": "T-01",
        "target_task_id": "T-02",
        "observed_status": "Cancelled",
    }
    assert raw == (canonical_json(expected_mapping) + "\n").encode("utf-8")
    assert decode_cancellation_tombstone(raw) == record
    ref = cancellation_tombstone_ref(record)
    assert ref == "cancellation:" + hashlib.sha256(canonical_json(expected_mapping).encode("utf-8")).hexdigest()
    assert cancellation_tombstone_ref(CancellationTombstoneV1(CHANGE_ID)) == ref

    carrier_root = tmp_path / "managed[1]-planning" / "changes" / "active" / ".planning-lite"
    expected_path = carrier_root / "dependency-admission" / "cancellations" / f"{ref.removeprefix('cancellation:')}.json"
    assert cancellation_tombstone_path(carrier_root, record) == expected_path
    published_ref, published = _publish_cancellation_tombstone_locked(carrier_root, record)
    assert (published_ref, published) == (ref, record)
    assert expected_path.read_bytes() == raw
    assert resolve_cancellation_tombstone(carrier_root, record) == (ref, record)
    assert list(expected_path.parent.glob("*.tmp")) == []

    with pytest.raises(CancellationCarrierError):
        decode_cancellation_tombstone(raw[:-1])
    with pytest.raises(CancellationCarrierError):
        decode_cancellation_tombstone(b"\xef\xbb\xbf" + raw)
    with pytest.raises(CancellationCarrierError):
        decode_cancellation_tombstone(raw.replace(b'"schema_version":1', b'"schema_version":true'))
    with pytest.raises(CancellationCarrierError):
        decode_cancellation_tombstone(raw.replace(b'"change_id":', b'"change_id":"duplicate","change_id":', 1))

    expected_path.write_bytes(b"conflicting immutable bytes\n")
    with pytest.raises(CancellationCarrierError):
        _publish_cancellation_tombstone_locked(carrier_root, record)
    assert expected_path.read_bytes() == b"conflicting immutable bytes\n"


def test_dependent_projection_hashes_requirement_and_reconciliation_are_exact(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    result = resolve_dependency(root, "T-02")
    source = resolve_dependency(root, "T-01")
    semantics = [_task_semantics(row) for row in _task_rows()]
    expected_projection = _expected_dependent(CHANGE_ID, CONTRACT, semantics, [])
    assert result.dependency_classification == "DEPENDENCY_EDGE_MEMBER"
    assert source.dependency_classification == "DEPENDENCY_EDGE_MEMBER"
    assert source.dependent_projection == result.dependent_projection
    assert source.dependency_semantic_digest == result.dependency_semantic_digest
    assert source.requirement == result.requirement
    assert source.requirement["requirement_id"] == result.requirement["requirement_id"]
    assert source.task_id == "T-01" and result.task_id == "T-02"
    assert set(result.dependent_projection) == {
        "schema_version", "change_id", "source_task_id", "target_task_id", "edge",
        "plan_dependency_contract_version", "accepted_output_contract_ref",
        "produced_artifact_logical_ref", "required_input_logical_ref", "acceptance_contract_ref",
        "evaluation_scope_ref", "required_verifier_contract_refs", "source_task_semantics",
        "target_task_semantics", "dependency_material_amendments",
    }
    assert result.dependent_projection == expected_projection
    expected_dep_digest = _sha(canonical_json(expected_projection).encode("utf-8"))
    assert result.dependent_dependency_semantic_digest == expected_dep_digest
    assert result.dependency_semantic_digest == expected_dep_digest
    assert "\n" not in canonical_json(expected_projection)

    plan = (root / result.plan_ref).read_text(encoding="utf-8")
    plan_start = plan.index("## Approved outcome and exclusions")
    assert result.plan_semantics_sha256 == _sha(plan[plan_start:].encode("utf-8"))
    assert result.task_semantics_sha256 == _sha(canonical_json(semantics).encode("utf-8"))
    amendment_text = (root / result.amendments_ref).read_text(encoding="utf-8")
    receipt_start = amendment_text.index("## Dependency reconciliation receipt")
    assert result.amendments_semantics_sha256 == _sha(amendment_text[:receipt_start].encode("utf-8"))
    approval_mapping = {
        "schema_version": 1,
        "change_id": CHANGE_ID,
        "plan_ref": result.plan_ref,
        "tasks_ref": result.tasks_ref,
        "amendments_ref": result.amendments_ref,
        "plan_semantics_sha256": result.plan_semantics_sha256,
        "task_semantics_sha256": result.task_semantics_sha256,
        "amendments_semantics_sha256": result.amendments_semantics_sha256,
        "dependency_semantic_digest": expected_dep_digest,
    }
    expected_approved_digest = _sha(canonical_json(approval_mapping).encode("utf-8"))
    assert result.approved_plan_digest == expected_approved_digest
    assert result.reconciliation_receipt == {
        "schema_version": 1,
        "change_id": CHANGE_ID,
        "status": "RECONCILED",
        "approved_plan_digest": expected_approved_digest,
        "dependency_semantic_digest": expected_dep_digest,
        "amendments_semantics_sha256": result.amendments_semantics_sha256,
        "applicable_dependency_material_amendment_ids": [],
    }
    requirement_without_id = dict(result.requirement)
    requirement_id = requirement_without_id.pop("requirement_id")
    assert requirement_id == "dreq_" + _sha(canonical_json(requirement_without_id).encode("utf-8"))
    assert historical_use_is_valid(root, "T-02", result.requirement, result.approved_plan_digest)


def test_independent_projection_has_own_digest_and_explicit_null_requirement_fields(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    result = resolve_dependency(root, "T-03")
    expected = {
        "schema_version": 1,
        "dependency_classification": "NOT_APPLICABLE",
        "change_id": CHANGE_ID,
        "task_or_operation_id": "T-03",
        "task_semantics": _task_semantics(_task_rows()[2]),
        "incoming_dependency_edges": [],
        "applicable_dependency_material_amendments": [],
    }
    assert result.projection == expected
    assert result.dependency_classification == "NOT_APPLICABLE"
    assert result.dependency_semantic_digest == _sha(canonical_json(expected).encode("utf-8"))
    assert result.dependency_semantic_digest != result.dependent_dependency_semantic_digest
    assert result.dependency_semantic_digest != "0" * 64
    for field in (
        "source_task_or_operation_id", "source_attempt_id", "successor_task_or_operation_id",
        "successor_attempt_id", "accepted_output_contract_ref", "produced_artifact_logical_ref",
        "required_successor_input_logical_ref", "acceptance_contract_ref", "evaluation_scope_ref",
    ):
        assert result.requirement[field] is None
    assert result.requirement["required_verifier_contract_refs"] == []
    assert set(result.projection) == {
        "schema_version", "dependency_classification", "change_id", "task_or_operation_id",
        "task_semantics", "incoming_dependency_edges", "applicable_dependency_material_amendments",
    }


def test_task_status_is_excluded_but_plan_body_changes_stale_approval(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    original = resolve_dependency(root, "T-02")
    tasks_path = root / original.tasks_ref
    tasks_path.write_text(tasks_path.read_text(encoding="utf-8").replace("`Pending`", "`In progress`", 1), encoding="utf-8", newline="\n")
    after_status = resolve_dependency(root, "T-02")
    assert after_status.task_semantics_sha256 == original.task_semantics_sha256
    assert after_status.dependency_semantic_digest == original.dependency_semantic_digest
    assert historical_use_is_valid(root, "T-02", original.requirement, original.approved_plan_digest)

    plan_path = root / original.plan_ref
    plan_path.write_text(plan_path.read_text(encoding="utf-8").replace("bounded dependency test fixture", "changed approved outcome"), encoding="utf-8", newline="\n")
    _expect_error("APPROVED_PLAN_DIGEST_STALE", lambda: resolve_dependency(root, "T-02"))


def test_unicode_approval_metadata_before_semantic_boundary_hashes_exact_utf8(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    plan_path = root / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = plan_path.read_text(encoding="utf-8")
    original = "- Approved by: Test owner"
    replacement = "- Approved by: Nad\u00edya \u0411\u0430\u0445\u0443\u0440\u0438\u043d\u0441\u044c\u043a\u0430"
    assert original in plan
    plan = plan.replace(original, replacement, 1)
    plan_path.write_text(plan, encoding="utf-8", newline="\n")

    heading = "## Approved outcome and exclusions"
    canonical_lf_plan = plan.replace("\r\n", "\n")
    start = canonical_lf_plan.index(heading)
    assert len(canonical_lf_plan[:start].encode("utf-8")) != start
    expected = _sha(canonical_lf_plan[start:].encode("utf-8"))

    result = resolve_dependency(root, "T-02")
    assert result.plan_semantics_sha256 == expected


def test_plan_status_must_be_exactly_approved(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    path = root / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = path.read_text(encoding="utf-8")
    assert "- Status: `Approved`" in plan
    path.write_text(plan.replace("- Status: `Approved`", "- Status: `Draft`", 1), encoding="utf-8", newline="\n")
    _expect_error("PLAN_NOT_APPROVED", lambda: resolve_dependency(root, "T-02"))


@pytest.mark.parametrize(
    ("field", "form", "code"),
    [
        ("Approved by", "missing", "AMBIGUOUS_APPROVAL_METADATA"),
        ("Approved by", "empty", "APPROVAL_METADATA_INCOMPLETE"),
        ("Approval evidence", "missing", "AMBIGUOUS_APPROVAL_METADATA"),
        ("Approval evidence", "empty", "APPROVAL_METADATA_INCOMPLETE"),
        ("Approval date", "missing", "AMBIGUOUS_APPROVAL_METADATA"),
        ("Approval date", "empty", "APPROVAL_METADATA_INCOMPLETE"),
    ],
    ids=[
        "approved-by-missing", "approved-by-empty",
        "approval-evidence-missing", "approval-evidence-empty",
        "approval-date-missing", "approval-date-empty",
    ],
)
def test_required_approval_metadata_must_be_present_and_complete(
    tmp_path: Path, field: str, form: str, code: str
) -> None:
    root = _write_fixture(tmp_path)
    path = root / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = path.read_text(encoding="utf-8")
    line = next(line for line in plan.splitlines() if line.startswith(f"- {field}:"))
    if form == "missing":
        plan = plan.replace(line + "\n", "", 1)
    else:
        plan = plan.replace(line, f"- {field}:", 1)
    path.write_text(plan, encoding="utf-8", newline="\n")
    _expect_error(code, lambda: resolve_dependency(root, "T-02"))


def test_duplicate_approval_metadata_is_rejected(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    path = root / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = path.read_text(encoding="utf-8")
    line = "- Approved by: Test owner"
    assert line in plan
    path.write_text(plan.replace(line, line + "\n" + line, 1), encoding="utf-8", newline="\n")
    _expect_error("AMBIGUOUS_APPROVAL_METADATA", lambda: resolve_dependency(root, "T-02"))


def test_duplicate_amendment_ids_are_rejected(tmp_path: Path) -> None:
    amendments = [_effect("AMD-DUPLICATE", {}), _effect("AMD-DUPLICATE", {})]
    root = _write_fixture(tmp_path, amendments=amendments)
    _expect_error("AMENDMENT_ID_INVALID", lambda: resolve_dependency(root, "T-02"))


def test_unsupported_amendment_type_is_rejected(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path, amendments=[_effect("AMD-UNSUPPORTED", {}, kind="Experimental")])
    _expect_error("AMENDMENT_CLASSIFICATION_UNRESOLVED", lambda: resolve_dependency(root, "T-02"))


def test_noncanonical_amendment_effect_json_is_rejected(tmp_path: Path) -> None:
    effect = _effect(
        "AMD-NONCANONICAL",
        {"accepted_output_contract_ref": (CONTRACT["accepted_output_contract_ref"], "acceptance:output-v2")},
    )
    root = _write_fixture(tmp_path, amendments=[effect])
    path = root / ".planning" / "changes" / "active" / CHANGE_ID / "amendments.md"
    text = path.read_text(encoding="utf-8")
    canonical = '["accepted_output_contract_ref"]'
    assert canonical in text
    path.write_text(text.replace(canonical, '[ "accepted_output_contract_ref" ]', 1), encoding="utf-8", newline="\n")
    _expect_error("AMENDMENT_EFFECT_NONCANONICAL", lambda: resolve_dependency(root, "T-02"))


def test_incoming_edge_effect_cannot_change_task_scope(tmp_path: Path) -> None:
    before = [{"source_task_id": "T-01", "target_task_id": "T-03"}]
    after = [{"source_task_id": "T-01", "target_task_id": "T-04"}]
    effect = _effect("AMD-MIXED-TASK-SCOPE", {"incoming_dependency_edges": (before, after)})
    root = _write_fixture(tmp_path, amendments=[effect])
    _expect_error("AMENDMENT_EFFECT_SCOPE_INVALID", lambda: resolve_dependency(root, "T-03"))


def test_complete_unrelated_amendment_changes_general_provenance_not_own_projection(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    bound = resolve_dependency(root, "T-03")
    row = _effect("AMD-001", {})
    changed = _write_fixture(tmp_path / "updated", amendments=[row])
    current = resolve_dependency(changed, "T-03")
    assert current.approved_plan_digest != bound.approved_plan_digest
    assert current.amendments_semantics_sha256 != bound.amendments_semantics_sha256
    assert current.dependency_semantic_digest == bound.dependency_semantic_digest
    assert historical_use_is_valid(changed, "T-03", bound.requirement, bound.approved_plan_digest)


def test_dependent_edge_only_amendment_preserves_independent_task_binding(tmp_path: Path) -> None:
    original = _write_fixture(tmp_path / "original")
    bound = resolve_dependency(original, "T-03")
    revised_contract = dict(CONTRACT, acceptance_contract_ref="acceptance:successor-v2")
    edge_only_amendment = _effect(
        "AMD-EDGE-ONLY",
        {"acceptance_contract_ref": (CONTRACT["acceptance_contract_ref"], revised_contract["acceptance_contract_ref"])},
    )
    revised = _write_fixture(tmp_path / "revised", contract=revised_contract, amendments=[edge_only_amendment])
    current = resolve_dependency(revised, "T-03")
    assert current.dependent_dependency_semantic_digest != bound.dependent_dependency_semantic_digest
    assert current.dependency_semantic_digest == bound.dependency_semantic_digest
    assert current.approved_plan_digest != bound.approved_plan_digest
    assert historical_use_is_valid(revised, "T-03", bound.requirement, bound.approved_plan_digest)


def test_material_edit_and_reversion_remain_in_projection_history(tmp_path: Path) -> None:
    original_contract = dict(CONTRACT)
    changed_contract = dict(CONTRACT, accepted_output_contract_ref="acceptance:output-v2")
    amendment = _effect(
        "AMD-001",
        {"accepted_output_contract_ref": (CONTRACT["accepted_output_contract_ref"], changed_contract["accepted_output_contract_ref"])},
    )
    edited = _write_fixture(tmp_path / "edited", contract=changed_contract, amendments=[amendment])
    original = _write_fixture(tmp_path / "original")
    bound = resolve_dependency(original, "T-02")
    assert not historical_use_is_valid(edited, "T-02", bound.requirement, bound.approved_plan_digest)
    current_edit = resolve_dependency(edited, "T-02")
    assert current_edit.dependent_projection["dependency_material_amendments"] == [
        {
            "amendment_id": "AMD-001",
            "changed_dependency_fields": ["accepted_output_contract_ref"],
            "before_values": {"accepted_output_contract_ref": CONTRACT["accepted_output_contract_ref"]},
            "after_values": {"accepted_output_contract_ref": changed_contract["accepted_output_contract_ref"]},
        }
    ]

    first = amendment
    second = _effect(
        "AMD-002",
        {"accepted_output_contract_ref": (changed_contract["accepted_output_contract_ref"], original_contract["accepted_output_contract_ref"])},
    )
    reverted = _write_fixture(tmp_path / "reverted", contract=original_contract, amendments=[first, second])
    current_reversion = resolve_dependency(reverted, "T-02")
    assert current_reversion.dependent_projection["accepted_output_contract_ref"] == original_contract["accepted_output_contract_ref"]
    assert len(current_reversion.dependent_projection["dependency_material_amendments"]) == 2
    assert not historical_use_is_valid(reverted, "T-02", bound.requirement, bound.approved_plan_digest)


def test_incomplete_or_unresolved_effect_chains_fail_closed(tmp_path: Path) -> None:
    good = {"accepted_output_contract_ref": ("acceptance:output-v1", "acceptance:output-v2")}
    broken = {"accepted_output_contract_ref": ("acceptance:unrelated", "acceptance:output-v3")}
    _write_fixture(tmp_path / "broken", contract=dict(CONTRACT, accepted_output_contract_ref="acceptance:output-v3"), amendments=[
        _effect("AMD-001", good),
        _effect("AMD-002", broken),
    ])
    _expect_error("AMENDMENT_EFFECT_CHAIN_INCOMPLETE", lambda: resolve_dependency(tmp_path / "broken", "T-02"))

    unresolved = _write_fixture(
        tmp_path / "unresolved",
        contract=dict(CONTRACT, accepted_output_contract_ref="acceptance:output-v3"),
        amendments=[_effect("AMD-001", good)],
    )
    _expect_error("AMENDMENT_EFFECT_CHAIN_UNRESOLVED", lambda: resolve_dependency(unresolved, "T-02"))


def test_independent_task_edit_is_scoped_to_that_task_and_edge_change_is_rejected(tmp_path: Path) -> None:
    original_rows = _task_rows()
    original_root = _write_fixture(tmp_path / "original")
    bound_t03 = resolve_dependency(original_root, "T-03")
    bound_t04 = resolve_dependency(original_root, "T-04")
    updated_rows = _task_rows(t03_outcome="Updated independent outcome")
    effect = _effect(
        "AMD-001",
        {"task_semantics": (_task_semantics(original_rows[2]), _task_semantics(updated_rows[2]))},
    )
    changed_root = _write_fixture(tmp_path / "changed", task_rows=updated_rows, amendments=[effect])
    changed_t03 = resolve_dependency(changed_root, "T-03")
    assert not historical_use_is_valid(changed_root, "T-03", bound_t03.requirement, bound_t03.approved_plan_digest)
    assert changed_t03.projection["applicable_dependency_material_amendments"][0]["amendment_id"] == "AMD-001"
    assert historical_use_is_valid(changed_root, "T-04", bound_t04.requirement, bound_t04.approved_plan_digest)

    incoming = [{"source_task_id": "T-01", "target_task_id": "T-03"}]
    edge_history = [
        _effect("AMD-EDGE-ADD", {"incoming_dependency_edges": ([], incoming)}),
        _effect("AMD-EDGE-REMOVE", {"incoming_dependency_edges": (incoming, [])}),
    ]
    edge_root = _write_fixture(tmp_path / "edge-history", amendments=edge_history)
    after_edge_reversion = resolve_dependency(edge_root, "T-03")
    assert after_edge_reversion.projection["incoming_dependency_edges"] == []
    assert len(after_edge_reversion.projection["applicable_dependency_material_amendments"]) == 2
    assert not historical_use_is_valid(edge_root, "T-03", bound_t03.requirement, bound_t03.approved_plan_digest)

    unresolved_edge_root = _write_fixture(tmp_path / "unresolved-edge", task_rows=_task_rows(edge_to_t03=True), amendments=[edge_history[0]])
    _expect_error("UNSUPPORTED_TASK_TOPOLOGY", lambda: resolve_dependency(unresolved_edge_root, "T-03"))


@pytest.mark.parametrize(
    ("contract", "code"),
    [
        (dict(CONTRACT, schema_version=True), "DEPENDENCY_CONTRACT_VERSION_INVALID"),
        (dict(CONTRACT, unexpected="alias"), "DEPENDENCY_CONTRACT_KEYS_INVALID"),
        (dict(CONTRACT, source_task_id="T-03"), "DEPENDENCY_CONTRACT_EDGE_INVALID"),
        (dict(CONTRACT, accepted_output_contract_ref=" padded "), "DEPENDENCY_CONTRACT_VALUE_INVALID"),
        (dict(CONTRACT, acceptance_contract_ref=""), "DEPENDENCY_CONTRACT_VALUE_INVALID"),
        (dict(CONTRACT, evaluation_scope_ref=" "), "DEPENDENCY_CONTRACT_VALUE_INVALID"),
        (dict(CONTRACT, required_verifier_contract_refs=[]), "DEPENDENCY_CONTRACT_VERIFIERS_INVALID"),
    ],
)
def test_nearest_wrong_contract_values_are_rejected(tmp_path: Path, contract: dict[str, Any], code: str) -> None:
    root = _write_fixture(tmp_path, contract=contract)
    _expect_error(code, lambda: resolve_dependency(root, "T-02"))


def test_missing_contract_member_is_rejected(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    path = root / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = path.read_text(encoding="utf-8")
    incomplete = {key: value for key, value in CONTRACT.items() if key != "acceptance_contract_ref"}
    path.write_text(plan.replace(canonical_json(CONTRACT), canonical_json(incomplete)), encoding="utf-8", newline="\n")
    _expect_error("DEPENDENCY_CONTRACT_KEYS_INVALID", lambda: resolve_dependency(root, "T-02"))


def test_duplicate_contract_members_and_noncanonical_contract_json_are_rejected(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    plan_path = root / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = plan_path.read_text(encoding="utf-8")
    plan = plan.replace('"schema_version":2,', '"schema_version":2,"schema_version":2,', 1)
    plan_path.write_text(plan, encoding="utf-8", newline="\n")
    _expect_error("MALFORMED_CANONICAL_JSON", lambda: resolve_dependency(root, "T-02"))

    root2 = _write_fixture(tmp_path / "pretty")
    plan_path = root2 / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = plan_path.read_text(encoding="utf-8")
    plan = plan.replace(canonical_json(CONTRACT), json.dumps(CONTRACT, indent=2, ensure_ascii=False), 1)
    plan_path.write_text(plan, encoding="utf-8", newline="\n")
    _expect_error("NONCANONICAL_GOVERNED_JSON", lambda: resolve_dependency(root2, "T-02"))

    root3 = _write_fixture(tmp_path / "multiple")
    plan_path = root3 / ".planning" / "changes" / "active" / CHANGE_ID / "plan.md"
    plan = plan_path.read_text(encoding="utf-8")
    plan_path.write_text(plan + "\n```json\n" + canonical_json(CONTRACT) + "\n```\n", encoding="utf-8", newline="\n")
    _expect_error("DEPENDENCY_CONTRACT_AMBIGUOUS", lambda: resolve_dependency(root3, "T-02"))


def test_semantic_json_uses_utf8_compact_sorted_bytes_without_lf(tmp_path: Path) -> None:
    unicode_contract = dict(CONTRACT, accepted_output_contract_ref="acceptance:résultat-v1")
    root = _write_fixture(tmp_path, contract=unicode_contract)
    result = resolve_dependency(root, "T-02")
    encoded = canonical_json(result.dependent_projection).encode("utf-8")
    assert "résultat" in canonical_json(result.dependent_projection)
    assert b"\\u00e9" not in encoded
    assert not encoded.endswith(b"\n")
    assert result.dependent_dependency_semantic_digest == _sha(encoded)


def test_stale_or_wrong_reconciliation_receipt_blocks(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    path = root / ".planning" / "changes" / "active" / CHANGE_ID / "amendments.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace('"status":"RECONCILED"', '"status":"PENDING"')
    path.write_text(text, encoding="utf-8", newline="\n")
    _expect_error("RECONCILIATION_RECEIPT_STALE", lambda: resolve_dependency(root, "T-02"))


def test_pointer_identity_utf8_and_line_ending_boundaries(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "valid")
    baseline = resolve_dependency(root, "T-02")
    for relative in (baseline.plan_ref, baseline.tasks_ref, baseline.amendments_ref):
        path = root / relative
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
    normalized = resolve_dependency(root, "T-02")
    assert normalized.plan_semantics_sha256 == baseline.plan_semantics_sha256
    assert normalized.dependency_semantic_digest == baseline.dependency_semantic_digest

    proposal = root / ".planning" / "changes" / "active" / CHANGE_ID / "proposal.md"
    proposal.write_text("# CHG-WRONG-001: Wrong identity\n", encoding="utf-8", newline="\n")
    _expect_error("ACTIVE_CHANGE_IDENTITY_MISMATCH", lambda: resolve_dependency(root, "T-02"))

    root2 = _write_fixture(tmp_path / "bom")
    active = root2 / ".planning" / "ACTIVE.md"
    active.write_bytes(b"\xef\xbb\xbf" + active.read_bytes())
    _expect_error("UTF8_BOM_FORBIDDEN", lambda: resolve_dependency(root2, "T-02"))


def test_unknown_task_and_requested_independence_are_derived(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    _expect_error("REQUESTED_TASK_MISSING", lambda: resolve_dependency(root, "T-99"))
    _expect_error("TASK_ID_INVALID", lambda: resolve_dependency(root, "T/03"))


def test_active_pointer_is_the_live_change_selector_even_with_a_decoy_folder(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path)
    decoy = root / ".planning" / "changes" / "active" / "CHG-DECOY-999"
    decoy.mkdir()
    (decoy / "proposal.md").write_text("# CHG-DECOY-999: Stale context\n", encoding="utf-8")
    (decoy / "plan.md").write_text("not an approved Plan\n", encoding="utf-8")
    result = resolve_dependency(root, "T-02")
    assert result.change_id == CHANGE_ID


def test_effective_planning_root_beats_default_root_decoy_and_fails_closed(tmp_path: Path) -> None:
    """Select only complete governance under validated policy and never fall back."""
    root = tmp_path / "consumer"
    custom_root = "managed-planning"
    (root / ".planning").mkdir(parents=True)
    (root / ".planning/CONFIG.yml").write_text(
        "project_policy:\n  planning_root: managed-planning\n",
        encoding="utf-8",
        newline="\n",
    )

    # Build complete, distinct A and B Changes. The default-root B is a valid
    # conflicting decoy; only A under the validated effective root may win.
    a_id = CHANGE_ID
    _write_fixture(root, planning_root=custom_root, change_id=a_id)
    _write_fixture(
        root,
        planning_root=".planning",
        change_id="CHG-DEFAULT-DECOY-002",
    )

    a_active = root / custom_root / "ACTIVE.md"
    b_active = root / ".planning/ACTIVE.md"
    assert f"Change: `{a_id}`" in a_active.read_text(encoding="utf-8")
    assert "Change: `CHG-DEFAULT-DECOY-002`" in b_active.read_text(encoding="utf-8")
    assert a_active.read_bytes() != b_active.read_bytes()
    selected = resolve_dependency(root, "T-02")
    assert selected.change_id == a_id
    assert selected.plan_ref == f"{custom_root}/changes/active/{a_id}/plan.md"
    assert selected.tasks_ref == f"{custom_root}/changes/active/{a_id}/tasks.md"
    assert selected.amendments_ref == f"{custom_root}/changes/active/{a_id}/amendments.md"
    (root / ".planning/CONFIG.yml").write_text(
        "project_policy:\n  planning_root: .planning\n",
        encoding="utf-8",
        newline="\n",
    )
    valid_b = resolve_dependency(root, "T-02")
    assert valid_b.change_id == "CHG-DEFAULT-DECOY-002"
    assert valid_b.plan_ref == ".planning/changes/active/CHG-DEFAULT-DECOY-002/plan.md"
    (root / ".planning/CONFIG.yml").write_text(
        "project_policy:\n  planning_root: managed-planning\n",
        encoding="utf-8",
        newline="\n",
    )

    default = _write_fixture(tmp_path / "default-root")
    default_result = resolve_dependency(default, "T-02")
    assert default_result.plan_ref == f".planning/changes/active/{CHANGE_ID}/plan.md"

    valid_a = a_active.read_bytes()
    a_active.unlink()
    _expect_error("GOVERNANCE_FILE_MISSING", lambda: resolve_dependency(root, "T-02"))
    a_active.write_bytes(b"\xef\xbb\xbf" + valid_a)
    _expect_error("UTF8_BOM_FORBIDDEN", lambda: resolve_dependency(root, "T-02"))

def test_literal_effective_planning_root_is_not_pattern_syntax(tmp_path: Path) -> None:
    root = tmp_path / "consumer"
    planning_root = "managed[1]-planning"
    change_id = "CHG-LITERAL-ROOT-003"
    lookalike_change_id = "CHG-PATTERN-DECOY-004"
    (root / ".planning").mkdir(parents=True)
    (root / ".planning" / "CONFIG.yml").write_text(
        "project_policy:\n  planning_root: managed[1]-planning\n",
        encoding="utf-8",
        newline="\n",
    )
    _write_fixture(root, planning_root=planning_root, change_id=change_id)

    # This incomplete glob lookalike must never substitute for the exact root.
    literal_active = root / planning_root / "ACTIVE.md"
    lookalike_active = root / "managed1-planning" / "ACTIVE.md"
    lookalike_active.parent.mkdir(parents=True)
    lookalike_active.write_text(
        literal_active.read_text(encoding="utf-8").replace(change_id, lookalike_change_id),
        encoding="utf-8",
        newline="\n",
    )

    selected = resolve_dependency(root, "T-02")
    change_ref = f"{planning_root}/changes/active/{change_id}"
    assert selected.change_id == change_id
    assert selected.plan_ref == f"{change_ref}/plan.md"
    assert selected.tasks_ref == f"{change_ref}/tasks.md"
    assert selected.amendments_ref == f"{change_ref}/amendments.md"

    # With the literal ACTIVE removed, the lookalike cannot become a fallback.
    literal_active.unlink()
    with pytest.raises(DependencyAdmissionError) as exc:
        resolve_dependency(root, "T-02")
    assert exc.value.code == "GOVERNANCE_FILE_MISSING"
    assert f"cannot read {planning_root}/ACTIVE.md" in str(exc.value)


def test_captured_json_wrapper_is_exact_immutable_and_digest_bound() -> None:
    wrapper = CapturedJsonValueV1.from_value({"z": [1, 2], "a": "λ"})
    mapping = wrapper.to_mapping()
    assert set(mapping) == {"content_digest", "value"}
    assert mapping["content_digest"] == _sha(canonical_json(mapping["value"]).encode("utf-8"))
    assert CapturedJsonValueV1.from_mapping(mapping).to_mapping() == mapping
    with pytest.raises(DependencyProofError):
        CapturedJsonValueV1.from_mapping({**mapping, "type": "VerifierEvidenceV1"})
    with pytest.raises(DependencyProofError):
        CapturedJsonValueV1.from_mapping({"content_digest": "0" * 64, "value": mapping["value"]})


def test_t04_capture_uses_exact_raw_route_bytes_and_publishes_only_inert_carrier(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    route = resolve_dependency_artifact_output_route(root)
    raw_artifact = b"\x00artifact\r\nbytes\xff"
    route.path.parent.mkdir(parents=True, exist_ok=True)
    route.path.write_bytes(raw_artifact)

    inputs = _capture_inputs()
    _publish_fixture_evidence_content(root, inputs)
    proof = capture_dependency_acceptance_proof(root, **inputs)
    mapping = proof.to_mapping()
    assert len(mapping) == 26
    assert set(mapping) == {
        "schema_version", "proof_id", "proof_digest", "change_id",
        "source_task_or_operation_id", "source_attempt_id", "successor_task_or_operation_id",
        "successor_attempt_id", "dependency_semantic_digest", "observed_result_id",
        "observed_result_content_digest", "observed_result", "attempt_evaluation_input",
        "acceptance_contract_ref", "acceptance_contract", "evaluation_scope_ref",
        "required_verifier_contract_refs", "verifier_evidence_inputs", "evidence_ref_contents",
        "evidence_supersession_inputs", "finding_inputs", "technical_evaluation_id",
        "technical_evaluation_outcome", "technical_evaluation", "artifact_logical_ref", "artifact_digest",
    }
    assert mapping["artifact_logical_ref"] == "artifact:build"
    assert mapping["artifact_digest"] == hashlib.sha256(raw_artifact).hexdigest()
    assert mapping["verifier_evidence_inputs"][0]["value"]["evidence_id"] == "evidence:build:other-scope"
    assert mapping["verifier_evidence_inputs"][1]["value"]["evidence_id"] == "evidence:build:pass"
    assert mapping["evidence_supersession_inputs"][0]["value"]["prior_evidence_ref"] == "evidence:historical:prior"
    assert mapping["finding_inputs"][0]["value"]["finding_id"] == "finding:other-scope"
    content_refs = [row["evidence_ref"] for row in mapping["evidence_ref_contents"]]
    assert content_refs == sorted(content_refs)
    for entry in mapping["evidence_ref_contents"]:
        carrier = resolve_evidence_content(root, entry["evidence_ref"])
        independent_digest = hashlib.sha256(carrier.exact_raw_bytes).hexdigest()
        assert entry["content_digest"] == independent_digest
        assert entry["content_identity"] == "econtent_" + independent_digest
    preimage = {key: value for key, value in mapping.items() if key not in {"proof_id", "proof_digest"}}
    expected_digest = hashlib.sha256(canonical_json(preimage).encode("utf-8")).hexdigest()
    assert mapping["proof_digest"] == expected_digest
    assert mapping["proof_id"] == "dproof_" + expected_digest
    encoded = encode_dependency_acceptance_proof(proof)
    assert encoded.endswith(b"\n") and not encoded.endswith(b"\n\n")
    assert decode_dependency_acceptance_proof(encoded).to_mapping() == mapping
    assert "artifact_route_digest" not in mapping and "route_path" not in mapping

    carrier = _DependencyArtifactCarrierV1("artifact:build", hashlib.sha256(raw_artifact).hexdigest())
    carrier_root = route.effective_planning_root / "changes" / "active" / ".planning-lite"
    carrier_path = _artifact_carrier_path(carrier_root, carrier)
    assert carrier_path.read_bytes().endswith(b"\n")
    assert _resolve_dependency_artifact_carrier(carrier_root, carrier) == (_dependency_artifact_carrier_ref(carrier), carrier)
    assert _evidence_content_path_for_test(root, "evidence-content:build").is_file()
    assert not (carrier_root / "CURRENT").exists()
    assert not (carrier_root / "attempt-runtime-v2.json").exists()


def test_t04_capture_rejects_missing_route_and_caller_bytes_only_provenance(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    with pytest.raises(DependencyProofError) as missing:
        capture_dependency_acceptance_proof(root, **_capture_inputs())
    assert missing.value.code == "ARTIFACT_ROUTE_MISSING"
    with pytest.raises(TypeError, match="artifact_bytes"):
        capture_dependency_acceptance_proof(root, **_capture_inputs(), artifact_bytes=b"not provenance")


def test_t04_capture_rejects_wrong_requirement_joins_and_m14(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    inputs = _capture_inputs()
    bad_input = dict(inputs["attempt_evaluation_input"])
    bad_input["acceptance_contract_ref"] = "acceptance:wrong"
    inputs["attempt_evaluation_input"] = bad_input
    with pytest.raises(DependencyProofError) as mismatch:
        _capture_proof(root, **inputs)
    assert mismatch.value.code == "PROOF_JOIN_INVALID"

    proof = _capture_proof(root)
    mapping = proof.to_mapping()
    mapping["required_verifier_contract_refs"] = []
    preimage = {key: value for key, value in mapping.items() if key not in {"proof_id", "proof_digest"}}
    digest = hashlib.sha256(canonical_json(preimage).encode("utf-8")).hexdigest()
    mapping["proof_digest"] = digest
    mapping["proof_id"] = "dproof_" + digest
    with pytest.raises(DependencyProofError) as m14:
        DependencyAcceptanceProofV1.from_mapping(mapping)
    assert m14.value.code == "EMPTY_REQUIRED_VERIFIER_SET"


def test_t04_proof_codec_rejects_extra_wrapper_keys_and_wrong_digest(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    proof = _capture_proof(root)
    mapping = proof.to_mapping()
    mapping["verifier_evidence_inputs"][0]["verifier_evidence"] = mapping["verifier_evidence_inputs"][0].pop("value")
    with pytest.raises(DependencyProofError):
        DependencyAcceptanceProofV1.from_mapping(mapping)

    mapping = proof.to_mapping()
    mapping["schema_version"] = True
    with pytest.raises(DependencyProofError) as bool_version:
        DependencyAcceptanceProofV1.from_mapping(mapping)
    assert bool_version.value.code == "PROOF_SCHEMA_INVALID"

    mapping = proof.to_mapping()
    mapping["artifact_digest"] = "0" * 64
    with pytest.raises(DependencyProofError) as bad_digest:
        DependencyAcceptanceProofV1.from_mapping(mapping)
    assert bad_digest.value.code == "PROOF_IDENTITY_MISMATCH"


def test_rf01_capture_rejects_fabricated_caller_content_rows(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    with pytest.raises(TypeError, match="evidence_ref_contents"):
        _capture_proof(
            root,
            evidence_ref_contents=[{
                "evidence_ref": "evidence-content:build",
                "content_identity": "content-id:evidence-content:build",
                "content_digest": hashlib.sha256(b"evidence-content:build").hexdigest(),
            }],
        )


@pytest.mark.parametrize(
    "missing_ref",
    [
        "evidence-content:build",
        "evidence-content:finding",
        "evidence:historical:prior",
        "evidence-content:other-scope",
    ],
)
def test_rf01_every_class_b_reference_requires_a_durable_carrier(tmp_path: Path, missing_ref: str) -> None:
    root = _write_fixture(tmp_path / "consumer")
    with pytest.raises(DependencyProofError) as missing:
        _capture_proof(root, skip_carrier_refs=(missing_ref,))
    assert missing.value.code == "EVIDENCE_CONTENT_MISSING"


def test_rf01_class_a_supersession_mapping_needs_no_external_carrier(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    inputs = _capture_inputs()
    captured = inputs["verifier_evidence_inputs"][0]
    inputs["evidence_supersession_inputs"] = (
        EvidenceSupersessionV1(
            captured.evidence_id, "evidence:historical:successor", "scope:other",
            ("claim:historical",), "Captured but not applicable to this scope.",
        ),
    )
    proof = _capture_proof(root, skip_carrier_refs=(captured.evidence_id,), **inputs)
    entry = next(row for row in proof.to_mapping()["evidence_ref_contents"] if row["evidence_ref"] == captured.evidence_id)
    canonical_mapping_bytes = canonical_json(captured.to_mapping()).encode("utf-8")
    expected_digest = hashlib.sha256(canonical_mapping_bytes).hexdigest()
    assert not _evidence_content_path_for_test(root, captured.evidence_id).exists()
    assert entry == {
        "evidence_ref": captured.evidence_id,
        "content_identity": "econtent_" + expected_digest,
        "content_digest": expected_digest,
    }


@pytest.mark.parametrize("overlap_matches", [True, False])
def test_rf01_class_a_class_b_overlap_requires_identical_bytes(tmp_path: Path, overlap_matches: bool) -> None:
    root = _write_fixture(tmp_path / "consumer")
    inputs = _capture_inputs()
    captured = inputs["verifier_evidence_inputs"][0]
    finding = inputs["finding_inputs"][0]
    inputs["finding_inputs"] = (
        finding,
        FindingV1(
            "finding:overlap", "An inapplicable overlap observation.", "NON_MATERIAL",
            ("VERIFICATION_TEST_COVERAGE",), "NON_BLOCKING", "OPEN",
            (captured.evidence_id,), None, finding.applicability,
        ),
    )
    inputs["evidence_supersession_inputs"] = (
        EvidenceSupersessionV1(
            captured.evidence_id, "evidence:historical:successor", "scope:other",
            ("claim:historical",), "Captured but not applicable to this scope.",
        ),
    )
    payload = canonical_json(captured.to_mapping()).encode("utf-8")
    if overlap_matches:
        proof = _capture_proof(root, **inputs)
        entries = proof.to_mapping()["evidence_ref_contents"]
        matching = [row for row in entries if row["evidence_ref"] == captured.evidence_id]
        assert len(matching) == 1
        assert matching[0]["content_digest"] == hashlib.sha256(payload).hexdigest()
    else:
        with pytest.raises(DependencyProofError) as conflict:
            _capture_proof(root, carrier_payloads={captured.evidence_id: b"different Class-B bytes"}, **inputs)
        assert conflict.value.code == "EVIDENCE_CONTENT_OVERLAP_MISMATCH"


def test_rf01_inapplicable_refs_and_all_pl08_array_orders_are_preserved(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    inputs = _capture_inputs()
    second_relation = EvidenceSupersessionV1(
        "evidence:second:prior", "evidence:second:successor", "scope:other",
        ("claim:second",), "Second inapplicable relation.",
    )
    inputs["evidence_supersession_inputs"] = (second_relation, *inputs["evidence_supersession_inputs"])
    finding = inputs["finding_inputs"][0]
    inputs["finding_inputs"] = (
        FindingV1(
            "finding:second", "Second inapplicable finding.", "NON_MATERIAL",
            ("VERIFICATION_TEST_COVERAGE",), "NON_BLOCKING", "OPEN",
            ("evidence-content:second-finding",), None, finding.applicability,
        ),
        finding,
    )
    proof = _capture_proof(root, **inputs).to_mapping()
    assert [row["value"]["evidence_id"] for row in proof["verifier_evidence_inputs"]] == [
        "evidence:build:other-scope", "evidence:build:pass",
    ]
    assert [row["value"]["prior_evidence_ref"] for row in proof["evidence_supersession_inputs"]] == [
        "evidence:second:prior", "evidence:historical:prior",
    ]
    assert [row["value"]["finding_id"] for row in proof["finding_inputs"]] == [
        "finding:second", "finding:other-scope",
    ]
    refs = {row["evidence_ref"] for row in proof["evidence_ref_contents"]}
    assert {"evidence-content:other-scope", "evidence-content:finding", "evidence-content:second-finding"} <= refs
    assert {"evidence:second:prior", "evidence:second:successor"} <= refs


def test_rf01_proof_validator_rechecks_class_a_mapping_digest_and_identity(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    inputs = _capture_inputs()
    captured = inputs["verifier_evidence_inputs"][0]
    inputs["evidence_supersession_inputs"] = (
        EvidenceSupersessionV1(
            captured.evidence_id, "evidence:historical:successor", "scope:other",
            ("claim:historical",), "Captured but not applicable to this scope.",
        ),
    )
    mapping = _capture_proof(root, **inputs).to_mapping()
    entry = next(row for row in mapping["evidence_ref_contents"] if row["evidence_ref"] == captured.evidence_id)
    entry["content_digest"] = "0" * 64
    entry["content_identity"] = "econtent_" + "0" * 64
    preimage = {key: item for key, item in mapping.items() if key not in {"proof_id", "proof_digest"}}
    digest = hashlib.sha256(canonical_json(preimage).encode("utf-8")).hexdigest()
    mapping["proof_digest"] = digest
    mapping["proof_id"] = "dproof_" + digest
    with pytest.raises(DependencyProofError) as mismatch:
        DependencyAcceptanceProofV1.from_mapping(mapping)
    assert mismatch.value.code == "EVIDENCE_CONTENT_DIGEST_MISMATCH"


@pytest.mark.parametrize("planning_root", [".planning", "managed-planning", "managed[1]-planning"])
def test_rf01_carrier_route_uses_default_custom_and_literal_effective_roots(
    tmp_path: Path, planning_root: str
) -> None:
    root = tmp_path / "consumer"
    if planning_root != ".planning":
        (root / ".planning").mkdir(parents=True)
        (root / ".planning" / "CONFIG.yml").write_text(
            f"project_policy:\n  planning_root: {planning_root}\n", encoding="utf-8", newline="\n"
        )
    root = _write_fixture(root, planning_root=planning_root)
    ref = "evidence:route:opaque"
    payload = b"route bytes\x00\xff"
    carrier = publish_evidence_content(root, ref, payload)
    path = _evidence_content_path_for_test(root, ref)
    expected = _carrier_mapping_for_test(ref, payload)
    assert path == resolve_dependency_artifact_output_route(root).effective_planning_root / (
        "changes/active/.planning-lite/dependency-admission/evidence-content-v1/"
        + hashlib.sha256(ref.encode("utf-8")).hexdigest() + ".json"
    )
    assert carrier.to_mapping() == expected
    assert path.is_file() and path.is_relative_to(resolve_dependency_artifact_output_route(root).effective_planning_root)


def test_rf01_evidence_ref_is_opaque_and_fresh_process_resolves_same_binding(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    ref = "../../outside/managed[1]-planning/evidence"
    payload = b"fresh process exact bytes"
    published = publish_evidence_content(root, ref, payload)
    expected_path = _evidence_content_path_for_test(root, ref)
    assert expected_path.name == hashlib.sha256(ref.encode("utf-8")).hexdigest() + ".json"
    assert expected_path.parent.name == "evidence-content-v1"
    code = (
        "import json,sys; from planning_lite.dependency_admission import resolve_evidence_content; "
        "print(json.dumps(resolve_evidence_content(sys.argv[1],sys.argv[2]).to_mapping(),sort_keys=True))"
    )
    result = subprocess.run(
        [sys.executable, "-c", code, str(root), ref], cwd=REPO_ROOT,
        check=True, capture_output=True, text=True,
    )
    assert json.loads(result.stdout) == published.to_mapping()
    assert resolve_evidence_content(root, ref) == published


@pytest.mark.parametrize(
    ("variant", "expected_code"),
    [
        ("unknown", "EVIDENCE_CONTENT_INVALID"),
        ("missing", "EVIDENCE_CONTENT_INVALID"),
        ("bool-version", "EVIDENCE_CONTENT_INVALID"),
        ("ref-type", "EVIDENCE_CONTENT_INVALID"),
        ("digest-type", "EVIDENCE_CONTENT_INVALID"),
        ("embedded-ref", "EVIDENCE_CONTENT_REF_MISMATCH"),
        ("raw-digest", "EVIDENCE_CONTENT_DIGEST_MISMATCH"),
        ("identity", "EVIDENCE_CONTENT_IDENTITY_MISMATCH"),
        ("malformed-base64", "EVIDENCE_CONTENT_BASE64_INVALID"),
        ("whitespace-base64", "EVIDENCE_CONTENT_BASE64_INVALID"),
        ("noncanonical-base64", "EVIDENCE_CONTENT_BASE64_INVALID"),
        ("duplicate-member", "EVIDENCE_CONTENT_INVALID"),
        ("extra-lf", "EVIDENCE_CONTENT_INVALID"),
        ("missing-lf", "EVIDENCE_CONTENT_INVALID"),
        ("pretty-json", "EVIDENCE_CONTENT_INVALID"),
    ],
)
def test_rf01_carrier_codec_rejects_malformed_or_noncanonical_records(
    tmp_path: Path, variant: str, expected_code: str
) -> None:
    root = _write_fixture(tmp_path / "consumer")
    requested_ref = "evidence:requested"
    payload = b"exact raw evidence"
    mapping = _carrier_mapping_for_test(requested_ref, payload)
    encoded: bytes
    if variant == "unknown":
        encoded = (canonical_json({**mapping, "extra": True}) + "\n").encode("utf-8")
    elif variant == "missing":
        encoded = (canonical_json({key: value for key, value in mapping.items() if key != "content_base64"}) + "\n").encode("utf-8")
    elif variant == "bool-version":
        encoded = (canonical_json({**mapping, "schema_version": True}) + "\n").encode("utf-8")
    elif variant == "ref-type":
        encoded = (canonical_json(dict(mapping, evidence_ref=17)) + "\n").encode("utf-8")
    elif variant == "digest-type":
        encoded = (canonical_json(dict(mapping, content_digest=17)) + "\n").encode("utf-8")
    elif variant == "embedded-ref":
        encoded = (canonical_json(_carrier_mapping_for_test("evidence:other", payload)) + "\n").encode("utf-8")
    elif variant == "raw-digest":
        wrong = dict(mapping, content_digest="0" * 64, content_identity="econtent_" + "0" * 64)
        encoded = (canonical_json(wrong) + "\n").encode("utf-8")
    elif variant == "identity":
        encoded = (canonical_json(dict(mapping, content_identity="econtent_wrong")) + "\n").encode("utf-8")
    elif variant == "malformed-base64":
        encoded = (canonical_json(dict(mapping, content_base64="%%%")) + "\n").encode("utf-8")
    elif variant == "whitespace-base64":
        encoded = (canonical_json(dict(mapping, content_base64=mapping["content_base64"] + "\n")) + "\n").encode("utf-8")
    elif variant == "noncanonical-base64":
        one_byte = _carrier_mapping_for_test(requested_ref, b"a")
        encoded = (canonical_json(dict(one_byte, content_base64="YQ")) + "\n").encode("utf-8")
    elif variant == "duplicate-member":
        encoded = (canonical_json(mapping).replace('"schema_version":1', '"schema_version":1,"schema_version":1') + "\n").encode("utf-8")
    elif variant == "extra-lf":
        encoded = (canonical_json(mapping) + "\n\n").encode("utf-8")
    elif variant == "missing-lf":
        encoded = canonical_json(mapping).encode("utf-8")
    else:
        encoded = (json.dumps(mapping, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    _write_carrier_bytes(root, requested_ref, encoded)
    with pytest.raises(DependencyProofError) as malformed:
        resolve_evidence_content(root, requested_ref)
    assert malformed.value.code == expected_code


def test_rf01_publication_reuses_identical_bytes_and_conflicts_without_overwrite(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    ref = "evidence:immutable"
    payload = b"first raw value"
    first = publish_evidence_content(root, ref, payload)
    path = _evidence_content_path_for_test(root, ref)
    first_bytes = path.read_bytes()
    first_stat = path.stat()
    second = publish_evidence_content(root, ref, payload)
    second_stat = path.stat()
    assert second == first
    assert path.read_bytes() == first_bytes
    assert (second_stat.st_size, second_stat.st_mtime_ns) == (first_stat.st_size, first_stat.st_mtime_ns)
    with pytest.raises(DependencyProofError) as conflict:
        publish_evidence_content(root, ref, b"different raw value")
    assert conflict.value.code == "EVIDENCE_CONTENT_CONFLICT"
    assert path.read_bytes() == first_bytes


def test_rf01_malformed_authoritative_carrier_is_not_repaired(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    ref = "evidence:corrupt-authority"
    corrupt = b"not canonical carrier bytes\n"
    path = _write_carrier_bytes(root, ref, corrupt)
    with pytest.raises(DependencyProofError):
        publish_evidence_content(root, ref, b"replacement is forbidden")
    assert path.read_bytes() == corrupt


def test_rf01_symlinked_carrier_directory_fails_closed(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    ref = "evidence:symlink"
    path = _evidence_content_path_for_test(root, ref)
    carrier_parent = path.parent.parent
    carrier_parent.mkdir(parents=True, exist_ok=True)
    external = tmp_path / "external"
    external.mkdir()
    link = carrier_parent / "evidence-content-v1"
    try:
        link.symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("directory symlink creation is unavailable in this environment")
    with pytest.raises(DependencyProofError) as unsafe:
        publish_evidence_content(root, ref, b"must not escape")
    assert unsafe.value.code == "EVIDENCE_CONTENT_UNSAFE"
    assert list(external.iterdir()) == []


def test_t04_capture_rejects_duplicate_finding_ids_and_wrong_observed_artifact_join(
    tmp_path: Path,
) -> None:
    root = _write_fixture(tmp_path / "consumer")
    inputs = _capture_inputs()
    inputs["finding_inputs"] = inputs["finding_inputs"] * 2
    with pytest.raises(DependencyProofError) as duplicate:
        _capture_proof(root, **inputs)
    assert duplicate.value.code == "PROOF_INPUT_INVALID"

    inputs = _capture_inputs()
    observed = inputs["observed_result"]
    inputs["observed_result"] = ObservedResultV1(
        observed.result_id, observed.attempt_id, observed.execution_status,
        observed.changed_paths, observed.fact_refs, ("artifact:caller-substitute",),
    )
    with pytest.raises(DependencyProofError) as wrong_artifact:
        _capture_proof(root, **inputs)
    assert wrong_artifact.value.code == "PROOF_JOIN_INVALID"


def test_t04_carrier_is_idempotent_and_conflicts_fail_closed(tmp_path: Path) -> None:
    root = _write_fixture(tmp_path / "consumer")
    first = _capture_proof(root)
    second = _capture_proof(root)
    assert first.to_mapping() == second.to_mapping()
    route = resolve_dependency_artifact_output_route(root)
    carrier = _DependencyArtifactCarrierV1(first.to_mapping()["artifact_logical_ref"], first.to_mapping()["artifact_digest"])
    carrier_root = route.effective_planning_root / "changes" / "active" / ".planning-lite"
    path = _artifact_carrier_path(carrier_root, carrier)
    path.write_bytes(b"conflicting immutable bytes\n")
    with pytest.raises(DependencyProofError) as conflict:
        _capture_proof(root)
    assert conflict.value.code == "ARTIFACT_CARRIER_CONFLICT"


def test_t04_capture_detects_artifact_mutation_during_carrier_publication(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = _write_fixture(tmp_path / "consumer")
    route = resolve_dependency_artifact_output_route(root)
    route.path.parent.mkdir(parents=True, exist_ok=True)
    route.path.write_bytes(b"before")
    inputs = _capture_inputs()
    _publish_fixture_evidence_content(root, inputs)
    publish = dependency_admission_module._publish_dependency_artifact_carrier

    def mutate_after_publish(carrier_root: Path, carrier: _DependencyArtifactCarrierV1):
        result = publish(carrier_root, carrier)
        route.path.write_bytes(b"changed while capturing")
        return result

    monkeypatch.setattr(dependency_admission_module, "_publish_dependency_artifact_carrier", mutate_after_publish)
    with pytest.raises(DependencyProofError) as changed:
        capture_dependency_acceptance_proof(root, **inputs)
    assert changed.value.code == "ARTIFACT_BYTES_CHANGED"


def test_t05_proof_blob_is_immutable_inert_and_admission_builder_is_exact(tmp_path: Path) -> None:
    from planning_lite.attempt_runtime import attempt_store_v2_path

    root = _write_fixture(tmp_path)
    proof = _capture_proof(root)
    route = resolve_dependency_artifact_output_route(root)
    requirement = resolve_dependency(root, "T-02").requirement
    exact_artifact_digest = hashlib.sha256(route.path.read_bytes()).hexdigest()
    admission = build_dependency_admission(proof, requirement, artifact_digest=exact_artifact_digest)
    expected_keys = {
        "schema_version", "admission_id", "requirement_id", "change_id",
        "source_task_or_operation_id", "source_attempt_id", "successor_task_or_operation_id",
        "successor_attempt_id", "dependency_semantic_digest", "observed_result_id",
        "acceptance_proof_id", "acceptance_proof_digest", "technical_evaluation_id",
        "technical_evaluation_outcome", "acceptance_contract_ref", "acceptance_contract_digest",
        "evaluation_scope_ref", "required_verifier_contract_refs", "artifact_logical_ref",
        "artifact_digest", "required_successor_input_logical_ref", "eligible_outcome",
    }
    assert set(admission) == expected_keys and len(admission) == 22
    semantic = dict(admission)
    admission_id = semantic.pop("admission_id")
    assert admission_id == "dadm_" + hashlib.sha256(canonical_json(semantic).encode("utf-8")).hexdigest()
    assert not attempt_store_v2_path(root).exists()

    carrier_root = route.effective_planning_root / "changes/active/.planning-lite"
    path = dependency_acceptance_proof_path(carrier_root, proof)
    first = publish_dependency_acceptance_proof_blob(carrier_root, proof)
    second = publish_dependency_acceptance_proof_blob(carrier_root, proof)
    assert first == second
    assert first[0] == proof.proof_id
    assert path.read_bytes() == encode_dependency_acceptance_proof(proof)
    assert resolve_dependency_acceptance_proof_blob(carrier_root, proof.proof_id) == proof
    assert not attempt_store_v2_path(root).exists()

    original = path.read_bytes()
    path.write_bytes(b"conflicting immutable proof bytes")
    with pytest.raises(DependencyProofCarrierError):
        publish_dependency_acceptance_proof_blob(carrier_root, proof)
    assert path.read_bytes() == b"conflicting immutable proof bytes"
    assert original == encode_dependency_acceptance_proof(proof)


def test_t06_pure_admission_validator_accepts_only_exact_current_joins(tmp_path: Path) -> None:
    _write_fixture(tmp_path)
    proof = _capture_proof(tmp_path)
    requirement = resolve_dependency(tmp_path, "T-02").requirement
    route = resolve_dependency_artifact_output_route(tmp_path)
    digest = hashlib.sha256(route.path.read_bytes()).hexdigest()
    admission = build_dependency_admission(proof, requirement, artifact_digest=digest)

    assert validate_dependency_admission(admission, proof, requirement, artifact_digest=digest) is None
    for field, replacement in (
        ("schema_version", 2.0),
        ("admission_id", "dadm_" + "0" * 64),
        ("requirement_id", "dreq_" + "0" * 64),
        ("change_id", "CHG-FORGED"),
        ("source_attempt_id", "CHG-FORGED/T-01/A1"),
        ("successor_attempt_id", "CHG-FORGED/T-02/A1"),
        ("acceptance_proof_id", "dproof_" + "0" * 64),
        ("acceptance_proof_digest", "0" * 64),
        ("artifact_logical_ref", "artifact:wrong"),
        ("artifact_digest", "f" * 64),
        ("required_successor_input_logical_ref", "artifact:wrong-input"),
        ("eligible_outcome", "SATISFIED"),
    ):
        forged = dict(admission)
        forged[field] = replacement
        if field != "admission_id":
            semantic = dict(forged)
            semantic.pop("admission_id")
            forged["admission_id"] = "dadm_" + hashlib.sha256(canonical_json(semantic).encode("utf-8")).hexdigest()
        with pytest.raises(DependencyProofError):
            validate_dependency_admission(forged, proof, requirement, artifact_digest=digest)

    with pytest.raises(DependencyProofError):
        validate_dependency_admission(None, proof, requirement, artifact_digest=digest)
    with pytest.raises(DependencyProofError):
        validate_dependency_admission({**admission, "unapproved": True}, proof, requirement, artifact_digest=digest)
