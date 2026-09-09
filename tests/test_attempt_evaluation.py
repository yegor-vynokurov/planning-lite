from __future__ import annotations

from pathlib import Path

import pytest

from planning_lite.attempt_evaluation import (
    ABSENT,
    AcceptanceContractV1,
    AttemptEvaluationError,
    AttemptRecordV1,
    CandidateIdentityV1,
    DirtyPathEntryV1,
    EvidenceApplicabilityV1,
    EvidenceSupersessionV1,
    FindingApplicabilityV1,
    FindingV1,
    IdentityRefV1,
    ObservedResultV1,
    TechnicalEvaluationV1,
    VerifierContractV1,
    VerifierEvidenceV1,
    allocate_attempt_ordinal,
    evaluate_technical,
    validate_corrective_attempt,
)


HEAD = "a" * 40
OTHER_HEAD = "b" * 40
CONTENT_A = "1" * 64
CONTENT_B = "2" * 64


def candidate(head: str = HEAD) -> CandidateIdentityV1:
    return CandidateIdentityV1(kind="GIT_COMMIT", head=head)


def versioned_ref(contract_id: str, version_or_ref: str) -> tuple[str, str]:
    if "/" in version_or_ref:
        prefix, version = version_or_ref.split("/", 1)
        assert prefix == contract_id
        return contract_id, version
    return contract_id, version_or_ref


def version_or_ref(value: str) -> str:
    return value.split("/", 1)[1] if "/" in value else value


def attempt(
    *,
    ordinal: int = 1,
    head: str = HEAD,
    contracts: tuple[str, ...] = ("V-A", "V-B"),
    acceptance_contract_ref: str = "ACCEPT-1",
    authorization_ref: str | None = "OWNER-AUTH-1",
    parent_attempt_ref: str | None = None,
    addresses_finding_refs: tuple[str, ...] = (),
    baseline_identity: str = "plan-1",
    normalize_contract_refs: bool = True,
) -> AttemptRecordV1:
    contract_refs = tuple(
        versioned_ref(value, "v1")
        if normalize_contract_refs
        else (versioned_ref(*value.split("/", 1)) if "/" in value else value)
        for value in contracts
    )
    return AttemptRecordV1(
        attempt_id=f"CHG-1/T-01/A{ordinal}",
        change_id="CHG-1",
        task_or_operation_id="T-01",
        attempt_ordinal=ordinal,
        authorization_ref=authorization_ref,
        acceptance_contract_ref=acceptance_contract_ref,
        candidate_identity=candidate(head),
        baseline_refs=(IdentityRefV1("plan", baseline_identity),),
        parent_attempt_ref=parent_attempt_ref,
        addresses_finding_refs=addresses_finding_refs,
        verifier_contract_refs=contract_refs,
    )


def contracts(
    *,
    version_a: str = "v1",
    version_b: str = "v1",
    required_a: bool = True,
    required_b: bool = True,
    required_refs_a: tuple[str, ...] = (),
    required_refs_b: tuple[str, ...] = (),
) -> tuple[VerifierContractV1, VerifierContractV1]:
    return (
        VerifierContractV1("ACCEPT-1", "V-A", version_or_ref(version_a), required_a, "test", "predicate A", required_refs_a, "fail"),
        VerifierContractV1("ACCEPT-1", "V-B", version_or_ref(version_b), required_b, "review", "predicate B", required_refs_b, "fail"),
    )


def acceptance(contract_set: tuple[VerifierContractV1, ...] | None = None, ref: str = "ACCEPT-1") -> AcceptanceContractV1:
    return AcceptanceContractV1(ref, contract_set or contracts())


def evidence(
    attempt_value: AttemptRecordV1,
    contract_id: str,
    outcome: str,
    evidence_id: str,
    *,
    version: str = "v1",
    baseline: str = "plan-1",
    evidence_refs: tuple[str, ...] | None = None,
    claim_refs: tuple[str, ...] | None = None,
    head: str = HEAD,
    acceptance_contract_ref: str | None = None,
) -> VerifierEvidenceV1:
    version_ref = version_or_ref(version)
    evidence_candidate = candidate(head)
    applicability = EvidenceApplicabilityV1(
        attempt_id=attempt_value.attempt_id,
        candidate_identity=evidence_candidate,
        acceptance_contract_ref=(
            attempt_value.acceptance_contract_ref
            if acceptance_contract_ref is None
            else acceptance_contract_ref
        ),
        verifier_contract_ref=contract_id,
        verifier_contract_version_or_ref=version_ref,
        evaluation_scope_ref="EVAL-SCOPE-1",
        input_baseline_refs=(IdentityRefV1("plan", baseline),),
    )
    return VerifierEvidenceV1(
        evidence_id=evidence_id,
        attempt_id=attempt_value.attempt_id,
        candidate_identity=evidence_candidate,
        verifier_contract_ref=contract_id,
        verifier_contract_version_or_ref=version_ref,
        outcome=outcome,
        evidence_refs=evidence_refs or (evidence_id,),
        applicability=applicability,
        claim_refs=claim_refs or (evidence_id,),
    )


def finding(
    attempt_value: AttemptRecordV1,
    impact: str,
    severity: str = "NON_MATERIAL",
    disposition: str = "OPEN",
    finding_id: str | None = None,
    *,
    head: str = HEAD,
    baseline: str = "plan-1",
    acceptance_contract_ref: str | None = None,
    attempt_id: str | None = None,
) -> FindingV1:
    owner = "OWNER-1" if disposition in {"DEFERRED", "CLOSED", "REMEDIATION_REQUIRED"} else None
    finding_candidate = candidate(head)
    applicability = FindingApplicabilityV1(
        attempt_id=attempt_value.attempt_id if attempt_id is None else attempt_id,
        candidate_identity=finding_candidate,
        acceptance_contract_ref=(
            attempt_value.acceptance_contract_ref
            if acceptance_contract_ref is None
            else acceptance_contract_ref
        ),
        evaluation_scope_ref="EVAL-SCOPE-1",
        input_baseline_refs=(IdentityRefV1("plan", baseline),),
    )
    return FindingV1(
        finding_id or f"F-{impact}-{severity}",
        "bounded finding",
        severity,
        ("CONTRACT",),
        impact,
        disposition,
        ("EV-A",),
        owner,
        applicability,
    )


def evaluate(
    attempt_value: AttemptRecordV1,
    values: tuple[VerifierEvidenceV1, ...],
    findings=(),
    *,
    contract_set: tuple[VerifierContractV1, ...] | None = None,
    acceptance_contract: AcceptanceContractV1 | None = None,
    supersession: tuple[EvidenceSupersessionV1, ...] = (),
):
    contract_set = contract_set or contracts()
    acceptance_contract = acceptance_contract or acceptance(contract_set)
    return evaluate_technical(
        attempt_value,
        contract_set,
        values,
        findings,
        acceptance_contract_ref=acceptance_contract.acceptance_contract_ref,
        acceptance_contract=acceptance_contract,
        evaluation_scope_ref="EVAL-SCOPE-1",
        supersession=supersession,
    )


def test_attempt_identity_and_ledger_scoped_allocation() -> None:
    assert attempt().attempt_id == "CHG-1/T-01/A1"
    assert attempt().to_mapping()["acceptance_contract_ref"] == "ACCEPT-1"
    assert allocate_attempt_ordinal([attempt()], change_id="CHG-1", task_or_operation_id="T-01") == 2
    assert allocate_attempt_ordinal([], change_id="CHG-1", task_or_operation_id="T-01") == 1
    with pytest.raises(AttemptEvaluationError):
        allocate_attempt_ordinal([attempt(ordinal=1), attempt(ordinal=3)], change_id="CHG-1", task_or_operation_id="T-01")
    with pytest.raises(AttemptEvaluationError):
        allocate_attempt_ordinal([attempt()], change_id="CHG-2", task_or_operation_id="T-01")
    with pytest.raises(AttemptEvaluationError):
        allocate_attempt_ordinal([{"attempt_id": "CHG-1/T-01/A0", "change_id": "CHG-1", "task_or_operation_id": "T-01", "attempt_ordinal": 0}], change_id="CHG-1", task_or_operation_id="T-01")
    with pytest.raises(AttemptEvaluationError):
        allocate_attempt_ordinal([{"attempt_id": "CHG-1/T-01/A1", "change_id": "CHG-1", "task_or_operation_id": "T-01", "attempt_ordinal": True}], change_id="CHG-1", task_or_operation_id="T-01")
    assert allocate_attempt_ordinal(
        [{"attempt_id": "CHG-1/T-01/A2", "change_id": "CHG-1", "task_or_operation_id": "T-01", "attempt_ordinal": 2},
         {"attempt_id": "CHG-1/T-01/A1", "change_id": "CHG-1", "task_or_operation_id": "T-01", "attempt_ordinal": 1}],
        change_id="CHG-1", task_or_operation_id="T-01"
    ) == 3


def test_attempt_is_not_authority_and_verifier_rerun_is_same_record() -> None:
    value = attempt()
    assert value.authorization_ref == "OWNER-AUTH-1"
    assert not hasattr(value, "authorized")
    assert value.attempt_id == attempt().attempt_id


def test_dirty_manifest_strict_matrix_and_canonical_identity() -> None:
    entries = (
        DirtyPathEntryV1("a.txt", "ADD", ABSENT, CONTENT_A),
        DirtyPathEntryV1("b.txt", "MODIFY", CONTENT_A, CONTENT_B),
        DirtyPathEntryV1("c.txt", "DELETE", CONTENT_A, ABSENT),
        DirtyPathEntryV1("d.txt", "RENAME", CONTENT_A, CONTENT_A, source_path="old.txt"),
        DirtyPathEntryV1("e.txt", "TYPE_CHANGE", CONTENT_A, CONTENT_A),
    )
    dirty = CandidateIdentityV1("DIRTY_SCOPE", HEAD, entries)
    assert [item.change_kind for item in dirty.dirty_manifest] == ["ADD", "MODIFY", "DELETE", "RENAME", "TYPE_CHANGE"]
    assert dirty.dirty_manifest[0].before == ABSENT
    invalid = (
        ("ADD", ABSENT, ABSENT, None),
        ("DELETE", ABSENT, ABSENT, None),
        ("MODIFY", ABSENT, CONTENT_A, None),
        ("MODIFY", CONTENT_A, ABSENT, None),
        ("RENAME", CONTENT_A, ABSENT, "old.txt"),
        ("RENAME", ABSENT, CONTENT_A, "old.txt"),
        ("TYPE_CHANGE", ABSENT, ABSENT, None),
    )
    for kind, before, after, source in invalid:
        with pytest.raises(AttemptEvaluationError):
            DirtyPathEntryV1("invalid.txt", kind, before, after, source_path=source)
    with pytest.raises(AttemptEvaluationError):
        CandidateIdentityV1("DIRTY_SCOPE", HEAD.upper(), ())
    with pytest.raises(AttemptEvaluationError):
        DirtyPathEntryV1("uppercase.txt", "MODIFY", "A" * 64, CONTENT_B)
    with pytest.raises(AttemptEvaluationError):
        CandidateIdentityV1("DIRTY_SCOPE", HEAD, tuple(reversed(entries)))
    with pytest.raises(AttemptEvaluationError):
        CandidateIdentityV1("DIRTY_SCOPE", HEAD, tuple(sorted(entries + (entries[0],), key=lambda item: (item.path, item.source_path or ""))))
    with pytest.raises(AttemptEvaluationError):
        DirtyPathEntryV1("x.txt", "RENAME", CONTENT_A, CONTENT_A)


def test_dirty_manifest_rejects_rename_identity_collisions() -> None:
    rename_a_b = DirtyPathEntryV1("b.txt", "RENAME", CONTENT_A, CONTENT_A, source_path="a.txt")
    rename_a_c = DirtyPathEntryV1("c.txt", "RENAME", CONTENT_A, CONTENT_B, source_path="a.txt")
    with pytest.raises(AttemptEvaluationError):
        CandidateIdentityV1("DIRTY_SCOPE", HEAD, (rename_a_b, rename_a_c))

    rename_b_c = DirtyPathEntryV1("c.txt", "RENAME", CONTENT_A, CONTENT_B, source_path="b.txt")
    rename_a_c = DirtyPathEntryV1("c.txt", "RENAME", CONTENT_A, CONTENT_B, source_path="a.txt")
    with pytest.raises(AttemptEvaluationError):
        CandidateIdentityV1("DIRTY_SCOPE", HEAD, tuple(sorted((rename_a_c, rename_b_c), key=lambda item: (item.path, item.source_path or ""))))

    disjoint = (
        DirtyPathEntryV1("b.txt", "RENAME", CONTENT_A, CONTENT_A, source_path="a.txt"),
        DirtyPathEntryV1("d.txt", "RENAME", CONTENT_B, CONTENT_B, source_path="c.txt"),
    )
    assert CandidateIdentityV1("DIRTY_SCOPE", HEAD, disjoint).dirty_manifest == disjoint

    for kind, before, after in (
        ("ADD", ABSENT, CONTENT_B),
        ("DELETE", CONTENT_B, ABSENT),
        ("MODIFY", CONTENT_A, CONTENT_B),
        ("TYPE_CHANGE", CONTENT_A, CONTENT_B),
    ):
        collision = DirtyPathEntryV1("a.txt", kind, before, after)
        with pytest.raises(AttemptEvaluationError):
            CandidateIdentityV1("DIRTY_SCOPE", HEAD, tuple(sorted((collision, rename_a_b), key=lambda item: (item.path, item.source_path or ""))))


def test_observed_result_is_descriptive_and_separate() -> None:
    result = ObservedResultV1("R-1", "CHG-1/T-01/A1", "COMPLETED", ("out.txt",), ("fact",), ())
    assert result.execution_status == "COMPLETED"
    assert result.to_mapping()["execution_status"] == "COMPLETED"
    with pytest.raises(AttemptEvaluationError):
        ObservedResultV1("R-2", "CHG-1/T-01/A1", "COMPLETED", ("out.txt", "out.txt"))


def test_authoritative_verifier_set_cannot_be_reduced_by_attempt() -> None:
    value = attempt(contracts=("V-A",))
    result = evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"),))
    assert result.outcome == "NOT_EVALUATED"
    assert result.required_verifier_contract_refs == ()
    one_contract = contracts()[:1]
    one_carrier = AcceptanceContractV1("ACCEPT-1", one_contract)
    empty = attempt(contracts=())
    assert evaluate(
        empty,
        (evidence(empty, "V-A", "PASS", "EV-EMPTY"),),
        contract_set=one_contract,
        acceptance_contract=one_carrier,
    ).outcome == "NOT_EVALUATED"
    superset = attempt(contracts=("V-A", "V-B", "V-C"))
    assert evaluate(superset, (), acceptance_contract=acceptance()).outcome == "NOT_EVALUATED"
    reordered = attempt(contracts=("V-B", "V-A"))
    assert evaluate(
        reordered,
        (evidence(reordered, "V-A", "PASS", "EV-REORDER-A"), evidence(reordered, "V-B", "PASS", "EV-REORDER-B")),
    ).outcome == "SATISFIED"
    value = attempt()
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"), evidence(value, "V-B", "PASS", "EV-B"))).outcome == "SATISFIED"
    assert evaluate(value, (evidence(value, "V-A", "FAIL", "EV-A"),)).outcome == "NOT_SATISFIED"
    mismatch = attempt(acceptance_contract_ref="OTHER")
    assert evaluate(mismatch, (), acceptance_contract=acceptance()).outcome == "NOT_EVALUATED"
    with pytest.raises(AttemptEvaluationError):
        AcceptanceContractV1("ACCEPT-1", contracts() + contracts())
    with pytest.raises(AttemptEvaluationError):
        attempt(contracts=("V-A", "V-A"))


def test_attempt_verifier_identity_is_exact_and_versioned() -> None:
    v2 = (VerifierContractV1("ACCEPT-1", "V-A", "v2", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", v2)

    bare = attempt(contracts=("V-A",), normalize_contract_refs=False)
    assert evaluate(
        bare,
        (evidence(bare, "V-A", "PASS", "EV-BARE", version="v2"),),
        contract_set=v2,
        acceptance_contract=carrier,
    ).outcome == "NOT_EVALUATED"

    exact = attempt(contracts=("V-A/v2",), normalize_contract_refs=False)
    assert evaluate(
        exact,
        (evidence(exact, "V-A", "PASS", "EV-EXACT", version="v2"),),
        contract_set=v2,
        acceptance_contract=carrier,
    ).outcome == "SATISFIED"

    old = attempt(contracts=("V-A/v1",), normalize_contract_refs=False)
    assert evaluate(
        old,
        (evidence(old, "V-A", "PASS", "EV-OLD", version="v2"),),
        contract_set=v2,
        acceptance_contract=carrier,
    ).outcome == "NOT_EVALUATED"


def test_attempt_binds_complete_declared_required_and_advisory_set() -> None:
    mixed = (
        VerifierContractV1("ACCEPT-1", "V-A", "v2", True, "test", "predicate A", (), "fail"),
        VerifierContractV1("ACCEPT-1", "V-B", "v1", False, "review", "predicate B", (), "fail"),
    )
    carrier = AcceptanceContractV1("ACCEPT-1", mixed)

    complete = attempt(contracts=("V-A/v2", "V-B/v1"), normalize_contract_refs=False)
    result = evaluate(
        complete,
        (evidence(complete, "V-A", "PASS", "EV-A", version="v2"),),
        contract_set=mixed,
        acceptance_contract=carrier,
    )
    assert result.outcome == "SATISFIED"
    assert result.declared_verifier_contract_refs == (("V-A", "v2"), ("V-B", "v1"))
    assert result.required_verifier_contract_refs == (("V-A", "v2"),)

    omitted = attempt(contracts=("V-A/v2",), normalize_contract_refs=False)
    assert evaluate(
        omitted,
        (evidence(omitted, "V-A", "PASS", "EV-OMITTED", version="v2"),),
        contract_set=mixed,
        acceptance_contract=carrier,
    ).outcome == "NOT_EVALUATED"

    undeclared = attempt(contracts=("V-A/v2", "V-B/v1", "V-C/v1"), normalize_contract_refs=False)
    assert evaluate(undeclared, (), contract_set=mixed, acceptance_contract=carrier).outcome == "NOT_EVALUATED"


def test_verifier_version_is_exactly_bound() -> None:
    value = attempt(contracts=("V-A/v2",), normalize_contract_refs=False)
    v2 = (VerifierContractV1("ACCEPT-1", "V-A", "v2", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", v2)
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A", version="v1"),), contract_set=v2, acceptance_contract=carrier).outcome == "INDETERMINATE"
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A", version="v2"),), contract_set=v2, acceptance_contract=carrier).outcome == "SATISFIED"
    mismatched_applicability = EvidenceApplicabilityV1(
        value.attempt_id, value.candidate_identity, value.acceptance_contract_ref,
        "V-A", "v1", "EVAL-SCOPE-1"
    )
    with pytest.raises(AttemptEvaluationError):
        VerifierEvidenceV1("BAD", value.attempt_id, value.candidate_identity, "V-A", "v2", "PASS", ("BAD",), mismatched_applicability)


def test_acceptance_contract_is_an_exact_applicability_dimension() -> None:
    value = attempt(contracts=("V-A",), acceptance_contract_ref="AC-Y")
    cset = (VerifierContractV1("AC-Y", "V-A", "v1", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("AC-Y", cset)
    foreign_evidence = evidence(
        value,
        "V-A",
        "PASS",
        "EV-X",
        acceptance_contract_ref="AC-X",
    )
    assert evaluate(
        value,
        (foreign_evidence,),
        contract_set=cset,
        acceptance_contract=carrier,
    ).outcome == "INDETERMINATE"

    exact_evidence = evidence(value, "V-A", "PASS", "EV-Y")
    assert evaluate(
        value,
        (exact_evidence,),
        contract_set=cset,
        acceptance_contract=carrier,
    ).outcome == "SATISFIED"

    foreign_finding = finding(
        value,
        "BLOCKING",
        finding_id="FOREIGN-AC",
        acceptance_contract_ref="AC-X",
    )
    result = evaluate(
        value,
        (exact_evidence,),
        (foreign_finding,),
        contract_set=cset,
        acceptance_contract=carrier,
    )
    assert result.outcome == "SATISFIED"
    assert "NON_APPLICABLE_FINDING:FOREIGN-AC" in result.reason_codes

    x_contract = (VerifierContractV1("AC-X", "V-A", "v1", True, "test", "predicate A", (), "fail"),)
    x_attempt = attempt(contracts=("V-A",), acceptance_contract_ref="AC-X")
    x_evidence = evidence(x_attempt, "V-A", "PASS", "EV-SAME-VERSION")
    assert evaluate(
        value,
        (x_evidence,),
        contract_set=cset,
        acceptance_contract=carrier,
    ).outcome == "INDETERMINATE"
    assert evaluate(
        x_attempt,
        (x_evidence,),
        contract_set=x_contract,
        acceptance_contract=AcceptanceContractV1("AC-X", x_contract),
    ).outcome == "SATISFIED"


def test_evaluation_precedence_and_invalid_attempt() -> None:
    value = attempt()
    assert evaluate(value, (evidence(value, "V-A", "FAIL", "EV-A"),)).outcome == "NOT_SATISFIED"
    assert evaluate(value, (evidence(value, "V-A", "FAIL", "EV-A"), evidence(value, "V-A", "PASS", "EV-A2"), evidence(value, "V-B", "PASS", "EV-B"))).outcome == "NOT_SATISFIED"
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"),)).outcome == "INDETERMINATE"
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"),), (finding(value, "BLOCKING"),)).outcome == "NOT_SATISFIED"
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"), evidence(value, "V-A", "INVALID", "EV-A2"), evidence(value, "V-B", "PASS", "EV-B"))).outcome == "INDETERMINATE"
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"), evidence(value, "V-B", "PASS", "EV-B"))).outcome == "SATISFIED"
    invalid = evaluate_technical(object(), (), (), acceptance_contract_ref="ACCEPT-1", evaluation_scope_ref="EVAL-SCOPE-1")
    assert invalid.outcome == "NOT_EVALUATED"


def test_required_evidence_refs_and_candidate_baseline_applicability() -> None:
    value = attempt(contracts=("V-A",))
    cset = (VerifierContractV1("ACCEPT-1", "V-A", "v1", True, "test", "predicate A", ("required-A",), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    missing = evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"),), contract_set=cset, acceptance_contract=carrier)
    assert missing.outcome == "INDETERMINATE"
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A", baseline="other"),), contract_set=cset, acceptance_contract=carrier).outcome == "INDETERMINATE"
    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A", head=OTHER_HEAD),), contract_set=cset, acceptance_contract=carrier).outcome == "INDETERMINATE"


def test_old_fail_remains_applicable_without_supersession() -> None:
    value = attempt()
    result = evaluate(value, (evidence(value, "V-A", "FAIL", "EV-A1"), evidence(value, "V-A", "PASS", "EV-A2"), evidence(value, "V-B", "PASS", "EV-B")))
    assert result.outcome == "NOT_SATISFIED"


def test_claim_scoped_supersession_preserves_residual_fail_and_history() -> None:
    value = attempt(contracts=("V-A",))
    cset = (VerifierContractV1("ACCEPT-1", "V-A", "v1", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    old = evidence(value, "V-A", "FAIL", "OLD", evidence_refs=("old-artifact",), claim_refs=("C1", "C2"))
    new = evidence(value, "V-A", "PASS", "NEW", evidence_refs=("new-artifact",), claim_refs=("C1",))
    partial = EvidenceSupersessionV1("OLD", "NEW", "EVAL-SCOPE-1", ("C1",), "rechecked C1")
    assert evaluate(value, (old, new), contract_set=cset, acceptance_contract=carrier, supersession=(partial,)).outcome == "NOT_SATISFIED"
    assert old.outcome == "FAIL"
    full_new = evidence(value, "V-A", "PASS", "FULL", evidence_refs=("full-artifact",), claim_refs=("C1", "C2"))
    full = EvidenceSupersessionV1("OLD", "FULL", "EVAL-SCOPE-1", ("C1", "C2"), "rechecked all")
    assert evaluate(value, (old, full_new), contract_set=cset, acceptance_contract=carrier, supersession=(full,)).outcome == "SATISFIED"
    with pytest.raises(AttemptEvaluationError):
        EvidenceSupersessionV1("OLD", "NEW", "EVAL-SCOPE-1", (), "empty")


def test_foreign_supersession_and_cycles_fail_closed() -> None:
    value = attempt(contracts=("V-A",))
    cset = (VerifierContractV1("ACCEPT-1", "V-A", "v1", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    old = evidence(value, "V-A", "FAIL", "OLD", claim_refs=("C1",))
    foreign = evidence(value, "V-A", "PASS", "FOREIGN", claim_refs=("C1",), head=OTHER_HEAD)
    relation = EvidenceSupersessionV1("OLD", "FOREIGN", "EVAL-SCOPE-1", ("C1",), "foreign")
    assert evaluate(value, (old, foreign), contract_set=cset, acceptance_contract=carrier, supersession=(relation,)).outcome == "NOT_EVALUATED"
    foreign_version = evidence(value, "V-A", "PASS", "FOREIGN-V", version="v2", claim_refs=("C1",))
    version_relation = EvidenceSupersessionV1("OLD", "FOREIGN-V", "EVAL-SCOPE-1", ("C1",), "foreign version")
    assert evaluate(value, (old, foreign_version), contract_set=cset, acceptance_contract=carrier, supersession=(version_relation,)).outcome == "NOT_EVALUATED"
    e2 = evidence(value, "V-A", "PASS", "E2", claim_refs=("C1",))
    e1 = evidence(value, "V-A", "FAIL", "E1", claim_refs=("C1",))
    e1_to_e2 = EvidenceSupersessionV1("E1", "E2", "EVAL-SCOPE-1", ("C1",), "cycle")
    e2_to_e1 = EvidenceSupersessionV1("E2", "E1", "EVAL-SCOPE-1", ("C1",), "cycle")
    assert evaluate(value, (e1, e2), contract_set=cset, acceptance_contract=carrier, supersession=(e1_to_e2, e2_to_e1)).outcome == "NOT_EVALUATED"


def test_branching_supersession_graph_is_complete_and_order_independent() -> None:
    value = attempt(contracts=("V-A",))
    cset = (VerifierContractV1("ACCEPT-1", "V-A", "v1", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    old = evidence(value, "V-A", "FAIL", "B1", claim_refs=("C1", "C2"))
    c1 = evidence(value, "V-A", "PASS", "B2", claim_refs=("C1",))
    c2 = evidence(value, "V-A", "PASS", "B3", claim_refs=("C2",))
    b1_to_b2 = EvidenceSupersessionV1("B1", "B2", "EVAL-SCOPE-1", ("C1",), "rechecked C1")
    b1_to_b3 = EvidenceSupersessionV1("B1", "B3", "EVAL-SCOPE-1", ("C2",), "rechecked C2")
    for relations in ((b1_to_b2, b1_to_b3), (b1_to_b3, b1_to_b2)):
        result = evaluate(
            value,
            (old, c1, c2),
            contract_set=cset,
            acceptance_contract=carrier,
            supersession=relations,
        )
        assert result.outcome == "SATISFIED"
        assert old.outcome == "FAIL"

    branching_cycle = EvidenceSupersessionV1("B2", "B1", "EVAL-SCOPE-1", ("C1",), "cycle")
    relations = (b1_to_b2, b1_to_b3, branching_cycle)
    for ordered in (relations, tuple(reversed(relations))):
        assert evaluate(
            value,
            (old, c1, c2),
            contract_set=cset,
            acceptance_contract=carrier,
            supersession=ordered,
        ).outcome == "NOT_EVALUATED"


def test_long_supersession_cycle_and_overlapping_superseders_fail_closed() -> None:
    value = attempt(contracts=("V-A",))
    cset = (VerifierContractV1("ACCEPT-1", "V-A", "v1", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    e1 = evidence(value, "V-A", "FAIL", "E1", claim_refs=("C1",))
    e2 = evidence(value, "V-A", "PASS", "E2", claim_refs=("C1",))
    e3 = evidence(value, "V-A", "PASS", "E3", claim_refs=("C1",))
    cycle = (
        EvidenceSupersessionV1("E1", "E2", "EVAL-SCOPE-1", ("C1",), "one"),
        EvidenceSupersessionV1("E2", "E3", "EVAL-SCOPE-1", ("C1",), "two"),
        EvidenceSupersessionV1("E3", "E1", "EVAL-SCOPE-1", ("C1",), "three"),
    )
    assert evaluate(value, (e1, e2, e3), contract_set=cset, acceptance_contract=carrier, supersession=cycle).outcome == "NOT_EVALUATED"
    overlap = (
        EvidenceSupersessionV1("E1", "E2", "EVAL-SCOPE-1", ("C1",), "one"),
        EvidenceSupersessionV1("E1", "E3", "EVAL-SCOPE-1", ("C1",), "two"),
    )
    assert evaluate(value, (e1, e2, e3), contract_set=cset, acceptance_contract=carrier, supersession=overlap).outcome == "NOT_EVALUATED"


@pytest.mark.parametrize(
    ("severity", "impact", "blocks"),
    [("MATERIAL", "NON_BLOCKING", False), ("NON_MATERIAL", "BLOCKING", True), ("MATERIAL", "BLOCKING", True), ("NON_MATERIAL", "NON_BLOCKING", False)],
)
def test_finding_axes_gate_only_on_unresolved_blocking(severity: str, impact: str, blocks: bool) -> None:
    value = attempt()
    result = evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"), evidence(value, "V-B", "PASS", "EV-B")), (finding(value, impact, severity),))
    assert (result.outcome == "NOT_SATISFIED") is blocks


def test_deferred_non_blocking_debt_coexists_with_acceptance() -> None:
    value = attempt()
    debt = finding(value, "NON_BLOCKING", "MATERIAL", "DEFERRED")
    result = evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"), evidence(value, "V-B", "PASS", "EV-B")), (debt,))
    assert result.outcome == "SATISFIED"
    assert debt.owner_adjudication_ref == "OWNER-1"
    with pytest.raises(AttemptEvaluationError):
        FindingV1("F", "x", "MATERIAL", ("CONTRACT",), "NON_BLOCKING", "CLOSED", ("EV",))


def test_finding_carrier_is_fail_closed_and_foreign_findings_are_explicitly_non_applicable() -> None:
    value = attempt()
    passing = (evidence(value, "V-A", "PASS", "EV-A"), evidence(value, "V-B", "PASS", "EV-B"))
    assert evaluate(value, passing, (object(),)).outcome == "NOT_EVALUATED"
    assert evaluate(value, passing, (finding(value, "BLOCKING"), object())).outcome == "NOT_EVALUATED"
    foreign = finding(value, "BLOCKING", head=OTHER_HEAD)
    result = evaluate(value, passing, (foreign,))
    assert result.outcome == "SATISFIED"
    assert "NON_APPLICABLE_FINDING:F-BLOCKING-NON_MATERIAL" in result.reason_codes
    foreign_attempt_finding = finding(attempt(ordinal=2), "BLOCKING", finding_id="FOREIGN-ATTEMPT")
    assert "NON_APPLICABLE_FINDING:FOREIGN-ATTEMPT" in evaluate(value, passing, (foreign_attempt_finding,)).reason_codes


def test_unified_evaluation_boundary_fails_closed_before_aggregation() -> None:
    value = attempt()
    cset = contracts()
    carrier = acceptance(cset)
    passing = (evidence(value, "V-A", "PASS", "EV-A"), evidence(value, "V-B", "PASS", "EV-B"))

    def direct(**overrides):
        kwargs = {
            "acceptance_contract_ref": "ACCEPT-1",
            "acceptance_contract": carrier,
            "evaluation_scope_ref": "EVAL-SCOPE-1",
        }
        kwargs.update(overrides)
        return evaluate_technical(value, cset, passing, (), **kwargs)

    assert direct(acceptance_contract_ref=None).outcome == "NOT_EVALUATED"
    assert direct(acceptance_contract_ref="").outcome == "NOT_EVALUATED"
    assert direct(evaluation_scope_ref=None).outcome == "NOT_EVALUATED"
    assert direct(evaluation_scope_ref=123).outcome == "NOT_EVALUATED"
    assert direct(evaluation_run=1).outcome == "NOT_EVALUATED"

    assert evaluate_technical(
        value,
        cset,
        (object(),),
        (),
        acceptance_contract_ref="ACCEPT-1",
        acceptance_contract=carrier,
        evaluation_scope_ref="EVAL-SCOPE-1",
    ).outcome == "NOT_EVALUATED"

    duplicate_foreign = (
        finding(value, "BLOCKING", finding_id="DUP", head=OTHER_HEAD),
        finding(value, "BLOCKING", finding_id="DUP", head=OTHER_HEAD),
    )
    assert evaluate_technical(
        value,
        cset,
        passing,
        duplicate_foreign,
        acceptance_contract_ref="ACCEPT-1",
        acceptance_contract=carrier,
        evaluation_scope_ref="EVAL-SCOPE-1",
    ).outcome == "NOT_EVALUATED"

    assert evaluate(value, (evidence(value, "V-A", "PASS", "EV-A"),)).outcome == "INDETERMINATE"
    decisive = evaluate(value, (evidence(value, "V-A", "FAIL", "EV-A"),))
    assert decisive.outcome == "NOT_SATISFIED"
    assert decisive.evidence_complete is False


def test_identity_carriers_freeze_mutable_sequences_and_reject_coercion() -> None:
    mutable_contracts = list(contracts())
    carrier = AcceptanceContractV1("ACCEPT-1", mutable_contracts)
    mutable_contracts.clear()
    assert len(carrier.verifier_contracts) == 2
    assert isinstance(carrier.verifier_contracts, tuple)
    with pytest.raises(AttemptEvaluationError):
        VerifierContractV1("ACCEPT-1", "V-A", "v1", 1, "test", "predicate", (), "fail")
    with pytest.raises(AttemptEvaluationError):
        attempt(ordinal=True)
    with pytest.raises(AttemptEvaluationError):
        EvidenceApplicabilityV1(
            attempt().attempt_id,
            attempt().candidate_identity,
            "",
            "V-A",
            "v1",
            "EVAL-SCOPE-1",
        )


def test_evidence_candidate_mismatch_is_non_applicable_not_satisfied() -> None:
    value = attempt()
    result = evaluate(value, (evidence(value, "V-A", "PASS", "EV-A", head=OTHER_HEAD), evidence(value, "V-B", "PASS", "EV-B")))
    assert result.outcome == "INDETERMINATE"
    duplicate = evidence(value, "V-A", "PASS", "DUP")
    assert evaluate(value, (duplicate, duplicate, evidence(value, "V-B", "PASS", "EV-B"))).outcome == "NOT_EVALUATED"


def test_shared_evidence_refs_are_deduplicated_without_collapsing_verifiers() -> None:
    value = attempt()
    cset = contracts(required_refs_a=("shared",), required_refs_b=("shared",))
    result = evaluate(value, (evidence(value, "V-A", "PASS", "EV-A", evidence_refs=("shared",)), evidence(value, "V-B", "PASS", "EV-B", evidence_refs=("shared",))), contract_set=cset)
    assert result.outcome == "SATISFIED"
    assert result.required_evidence_refs == ("shared",)
    result = evaluate(value, (evidence(value, "V-A", "FAIL", "EV-A", evidence_refs=("shared",)), evidence(value, "V-B", "PASS", "EV-B", evidence_refs=("shared",))), contract_set=cset)
    assert result.outcome == "NOT_SATISFIED"


def test_corrective_attempt_lineage_requires_parent_findings_and_new_authorization() -> None:
    parent = attempt(authorization_ref="OWNER-AUTH-1")
    corrective = attempt(ordinal=2, head=OTHER_HEAD, authorization_ref="OWNER-AUTH-2", parent_attempt_ref=parent.attempt_id, addresses_finding_refs=("F-1",))
    prior_finding = finding(parent, "BLOCKING", finding_id="F-1")
    assert validate_corrective_attempt(corrective, parent=parent, prior_lineage=(parent,), prior_findings=(prior_finding,)) is corrective
    with pytest.raises(AttemptEvaluationError):
        validate_corrective_attempt(corrective, parent=attempt(authorization_ref="OTHER"), prior_lineage=(parent,), prior_findings=(prior_finding,))
    with pytest.raises(AttemptEvaluationError):
        validate_corrective_attempt(corrective, parent=parent, prior_lineage=(parent,), prior_findings=(finding(parent, "BLOCKING", finding_id="FOREIGN"),))
    with pytest.raises(AttemptEvaluationError):
        AttemptRecordV1("CHG-1/T-01/A2", "CHG-1", "T-01", 2, "", "ACCEPT-1", candidate(OTHER_HEAD), (IdentityRefV1("plan", "plan-1"),), parent_attempt_ref=parent.attempt_id, addresses_finding_refs=("F-1",), verifier_contract_refs=("V-A", "V-B"))


def test_corrective_attempt_requires_exact_finding_provenance() -> None:
    parent = attempt(authorization_ref="OWNER-AUTH-1")
    corrective = attempt(
        ordinal=2,
        head=OTHER_HEAD,
        authorization_ref="OWNER-AUTH-2",
        parent_attempt_ref=parent.attempt_id,
        addresses_finding_refs=("F-1",),
    )
    valid = finding(parent, "BLOCKING", finding_id="F-1")
    assert validate_corrective_attempt(
        corrective,
        parent=parent,
        prior_lineage=(parent,),
        prior_findings=(valid,),
    ) is corrective

    foreign_values = (
        finding(parent, "BLOCKING", finding_id="F-1", head=OTHER_HEAD),
        finding(parent, "BLOCKING", finding_id="F-1", attempt_id="CHG-1/T-01/A99"),
        finding(parent, "BLOCKING", finding_id="F-1", baseline="other"),
        finding(parent, "BLOCKING", finding_id="F-1", acceptance_contract_ref="OTHER-AC"),
    )
    for foreign in foreign_values:
        with pytest.raises(AttemptEvaluationError):
            validate_corrective_attempt(
                corrective,
                parent=parent,
                prior_lineage=(parent,),
                prior_findings=(foreign,),
            )

    with pytest.raises(AttemptEvaluationError):
        validate_corrective_attempt(
            corrective,
            parent=parent,
            prior_lineage=(parent,),
            prior_findings=(),
        )


def test_corrective_attempt_requires_fresh_authorization_across_full_lineage() -> None:
    a1 = attempt(ordinal=1, authorization_ref="AUTH-1")
    f1 = finding(a1, "BLOCKING", finding_id="F-A1")
    a2 = attempt(
        ordinal=2,
        head=OTHER_HEAD,
        authorization_ref="AUTH-2",
        parent_attempt_ref=a1.attempt_id,
        addresses_finding_refs=("F-A1",),
    )
    assert validate_corrective_attempt(
        a2,
        parent=a1,
        prior_lineage=(a1,),
        prior_findings=(f1,),
    ) is a2

    f2 = finding(a2, "BLOCKING", finding_id="F-A2", head=OTHER_HEAD)
    a3 = attempt(
        ordinal=3,
        authorization_ref="AUTH-3",
        parent_attempt_ref=a2.attempt_id,
        addresses_finding_refs=("F-A2",),
    )
    assert validate_corrective_attempt(
        a3,
        parent=a2,
        prior_lineage=(a2, a1),
        prior_findings=(f2,),
    ) is a3

    for reused, lineage, parent_value, finding_value in (
        (
            attempt(
                ordinal=3,
                authorization_ref="AUTH-1",
                parent_attempt_ref=a2.attempt_id,
                addresses_finding_refs=("F-A2",),
            ),
            (a1, a2),
            a2,
            f2,
        ),
        (
            attempt(
                ordinal=2,
                head=OTHER_HEAD,
                authorization_ref="AUTH-1",
                parent_attempt_ref=a1.attempt_id,
                addresses_finding_refs=("F-A1",),
            ),
            (a1,),
            a1,
            f1,
        ),
        (
            attempt(
                ordinal=4,
                authorization_ref="AUTH-2",
                parent_attempt_ref=a3.attempt_id,
                addresses_finding_refs=("F-A3",),
            ),
            (a1, a2, a3),
            a3,
            finding(a3, "BLOCKING", finding_id="F-A3"),
        ),
    ):
        with pytest.raises(AttemptEvaluationError):
            validate_corrective_attempt(
                reused,
                parent=parent_value,
                prior_lineage=lineage,
                prior_findings=(finding_value,),
            )


def test_prior_lineage_rejects_historical_authorization_reuse() -> None:
    a1 = attempt(ordinal=1, authorization_ref="AUTH-1")
    a2_immediate = attempt(
        ordinal=2,
        authorization_ref="AUTH-1",
        parent_attempt_ref=a1.attempt_id,
        addresses_finding_refs=("F-A2",),
    )
    a3 = attempt(
        ordinal=3,
        authorization_ref="AUTH-3",
        parent_attempt_ref=a2_immediate.attempt_id,
        addresses_finding_refs=("F-A2",),
    )
    with pytest.raises(AttemptEvaluationError):
        validate_corrective_attempt(
            a3,
            parent=a2_immediate,
            prior_lineage=(a1, a2_immediate),
            prior_findings=(finding(a2_immediate, "BLOCKING", finding_id="F-A2"),),
        )

    a2 = attempt(ordinal=2, authorization_ref="AUTH-2", parent_attempt_ref=a1.attempt_id)
    a3_reused = attempt(ordinal=3, authorization_ref="AUTH-1", parent_attempt_ref=a2.attempt_id)
    a4 = attempt(ordinal=4, authorization_ref="AUTH-4", parent_attempt_ref=a3_reused.attempt_id, addresses_finding_refs=("F-A3",))
    with pytest.raises(AttemptEvaluationError):
        validate_corrective_attempt(
            a4,
            parent=a3_reused,
            prior_lineage=(a1, a2, a3_reused),
            prior_findings=(finding(a3_reused, "BLOCKING", finding_id="F-A3"),),
        )


def test_prior_lineage_accepts_unique_history_and_fresh_authorization() -> None:
    a1 = attempt(ordinal=1, authorization_ref="AUTH-1")
    a2 = attempt(ordinal=2, authorization_ref="AUTH-2", parent_attempt_ref=a1.attempt_id)
    a3 = attempt(ordinal=3, authorization_ref="AUTH-3", parent_attempt_ref=a2.attempt_id)
    a4 = attempt(
        ordinal=4,
        authorization_ref="AUTH-4",
        parent_attempt_ref=a3.attempt_id,
        addresses_finding_refs=("F-A3",),
    )
    assert validate_corrective_attempt(
        a4,
        parent=a3,
        prior_lineage=(a1, a2, a3),
        prior_findings=(finding(a3, "BLOCKING", finding_id="F-A3"),),
    ) is a4


def test_failure_cannot_authorize_retry_or_close_finding_and_hook_stays_minimal() -> None:
    value = finding(attempt(), "BLOCKING")
    assert value.disposition == "OPEN"
    assert value.blocks_acceptance
    assert not hasattr(attempt(), "stable_prefix_identity")
    assert not hasattr(attempt(), "recommendation")


def test_composite_identity_distinguishes_contract_ids_with_same_version() -> None:
    cset = (
        VerifierContractV1("ACCEPT-1", "A", "v1", True, "test", "predicate A", (), "fail"),
        VerifierContractV1("ACCEPT-1", "B", "v1", True, "test", "predicate B", (), "fail"),
    )
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    value = attempt(contracts=("A/v1", "B/v1"), normalize_contract_refs=False)
    assert evaluate(
        value,
        (evidence(value, "A", "PASS", "EV-A"), evidence(value, "B", "PASS", "EV-B")),
        contract_set=cset,
        acceptance_contract=carrier,
    ).outcome == "SATISFIED"
    wrong = attempt(contracts=("B/v1",), normalize_contract_refs=False)
    assert evaluate(wrong, (), contract_set=cset, acceptance_contract=carrier).outcome == "NOT_EVALUATED"


def test_composite_identity_distinguishes_versions_for_one_contract_id() -> None:
    cset = (VerifierContractV1("ACCEPT-1", "A", "v2", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    wrong = attempt(contracts=("A/v1",), normalize_contract_refs=False)
    assert evaluate(wrong, (), contract_set=cset, acceptance_contract=carrier).outcome == "NOT_EVALUATED"


def test_bare_version_is_not_a_composite_identity() -> None:
    cset = (VerifierContractV1("ACCEPT-1", "A", "v2", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    bare = attempt(contracts=("v2",), normalize_contract_refs=False)
    assert evaluate(bare, (), contract_set=cset, acceptance_contract=carrier).outcome == "NOT_EVALUATED"


def test_bare_contract_id_is_not_a_composite_identity() -> None:
    cset = (VerifierContractV1("ACCEPT-1", "A", "v2", True, "test", "predicate A", (), "fail"),)
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    bare = attempt(contracts=("A",), normalize_contract_refs=False)
    assert evaluate(bare, (), contract_set=cset, acceptance_contract=carrier).outcome == "NOT_EVALUATED"


def test_progress_template_preserves_declared_and_required_composite_sets() -> None:
    text = (Path(__file__).resolve().parents[1] / "template/.planning/changes/templates/progress.md").read_text(encoding="utf-8")
    assert "Declared verifier contract identities:" in text
    assert "Required verifier contract identities (subset of declared):" in text
    assert "contract_id:" in text
    assert "contract_version_or_ref:" in text


def test_review_template_preserves_declared_and_required_composite_sets() -> None:
    text = (Path(__file__).resolve().parents[1] / "template/.planning/changes/templates/review.md").read_text(encoding="utf-8")
    assert "Complete declared verifier contract identities:" in text
    assert "Required verifier contract identities (subset of declared):" in text
    assert "contract_id:" in text
    assert "contract_version_or_ref:" in text


def test_attempt_requires_exact_complete_declared_composite_set() -> None:
    cset = contracts()
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    reordered = attempt(contracts=("V-B/v1", "V-A/v1"), normalize_contract_refs=False)
    assert evaluate(reordered, (), contract_set=cset, acceptance_contract=carrier).outcome == "INDETERMINATE"
    missing = attempt(contracts=("V-A/v1",), normalize_contract_refs=False)
    assert evaluate(missing, (), contract_set=cset, acceptance_contract=carrier).outcome == "NOT_EVALUATED"
    extra = attempt(contracts=("V-A/v1", "V-B/v1", "V-C/v1"), normalize_contract_refs=False)
    assert evaluate(extra, (), contract_set=cset, acceptance_contract=carrier).outcome == "NOT_EVALUATED"


def test_required_subset_is_evaluated_separately_from_complete_declaration() -> None:
    cset = (
        VerifierContractV1("ACCEPT-1", "A", "v2", True, "test", "predicate A", (), "fail"),
        VerifierContractV1("ACCEPT-1", "B", "v1", False, "review", "predicate B", (), "fail"),
    )
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    value = attempt(contracts=("A/v2", "B/v1"), normalize_contract_refs=False)
    result = evaluate(value, (evidence(value, "A", "PASS", "EV-A", version="v2"),), contract_set=cset, acceptance_contract=carrier)
    assert result.outcome == "SATISFIED"
    assert result.declared_verifier_contract_refs == (("A", "v2"), ("B", "v1"))
    assert result.required_verifier_contract_refs == (("A", "v2"),)


def test_advisory_omission_from_attempt_is_structurally_invalid() -> None:
    cset = (
        VerifierContractV1("ACCEPT-1", "A", "v2", True, "test", "predicate A", (), "fail"),
        VerifierContractV1("ACCEPT-1", "B", "v1", False, "review", "predicate B", (), "fail"),
    )
    carrier = AcceptanceContractV1("ACCEPT-1", cset)
    omitted = attempt(contracts=("A/v2",), normalize_contract_refs=False)
    assert evaluate(omitted, (), contract_set=cset, acceptance_contract=carrier).outcome == "NOT_EVALUATED"


def test_duplicate_composite_identity_fails_before_set_deduplication() -> None:
    with pytest.raises(AttemptEvaluationError):
        attempt(contracts=("V-A/v1", "V-A/v1"), normalize_contract_refs=False)


def test_technical_evaluation_rejects_required_identity_outside_declared_set() -> None:
    with pytest.raises(AttemptEvaluationError):
        TechnicalEvaluationV1(
            "EVAL-1",
            "CHG-1/T-01/A1",
            candidate(),
            "ACCEPT-1",
            (("A", "v1"),),
            (("B", "v1"),),
            "INDETERMINATE",
            False,
            (),
            (),
            ("REQUIRED_EVIDENCE_MISSING",),
        )


def test_technical_evaluation_accepts_declared_required_subset_and_advisory_carrier() -> None:
    value = TechnicalEvaluationV1(
        "EVAL-2",
        "CHG-1/T-01/A1",
        candidate(),
        "ACCEPT-1",
        (("A", "v2"), ("B", "v1")),
        (("A", "v2"),),
        "SATISFIED",
        True,
        (),
        (),
        ("ALL_REQUIRED_PASS",),
    )
    assert value.required_verifier_contract_refs == (("A", "v2"),)


def test_technical_evaluation_accepts_declared_carrier_with_empty_required_subset() -> None:
    value = TechnicalEvaluationV1(
        "EVAL-3",
        "CHG-1/T-01/A1",
        candidate(),
        "ACCEPT-1",
        (("A", "v1"),),
        (),
        "INDETERMINATE",
        False,
        (),
        (),
        ("REQUIRED_EVIDENCE_MISSING",),
    )
    assert value.declared_verifier_contract_refs == (("A", "v1"),)


def test_technical_evaluation_rejects_empty_satisfied_carrier() -> None:
    with pytest.raises(AttemptEvaluationError):
        TechnicalEvaluationV1(
            "EVAL-4",
            "CHG-1/T-01/A1",
            candidate(),
            "ACCEPT-1",
            (),
            (),
            "SATISFIED",
            True,
            (),
            (),
            ("ALL_REQUIRED_PASS",),
        )
