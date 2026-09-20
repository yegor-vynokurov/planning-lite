"""Pure deterministic CriticalJourney traversability contracts.

This module derives observations from caller-supplied facts only. It deliberately
does not read or write files, inspect Git, route work, execute runtime behavior,
or own durable Project Spine state.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass


class TraversabilityError(ValueError):
    """Raised when caller-supplied traversability facts are malformed."""


JOURNEY_STATES = (
    "NOT_DEFINED",
    "DEFINED",
    "WIRED_FAIL",
    "WIRED_TRAVERSABLE",
    "PASSING",
)

GAP_CLASSES = (
    "IMPLEMENTATION_GAP",
    "WIRING_GAP",
    "ORCHESTRATION_GAP",
    "EVIDENCE_GAP",
)

APPLICABILITY_VALUES = ("REQUIRED", "NOT_APPLICABLE")
PLACEHOLDER_VALUES = ("NONE", "NOT_IMPLEMENTED", "FIXTURE_ONLY")
SEAM_DISPOSITIONS = ("PASS", "FAIL", "DOWNSTREAM_UNREACHABLE", "UNOBSERVED")
CHECK_DISPOSITIONS = (
    "PASS",
    "WIRED_FAIL",
    "BLOCKED_BY_ENVIRONMENT",
    "BLOCKED_BY_MISSING_PROBE",
    "NOT_APPLICABLE",
)


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TraversabilityError(f"{field} must be a non-empty string")
    normalized = value.strip()
    if normalized != value:
        raise TraversabilityError(f"{field} must be normalized")
    return normalized


def _optional_text(value: object, field: str) -> str | None:
    if value is None:
        return None
    return _text(value, field)


def _boolean(value: object, field: str) -> bool:
    if not isinstance(value, bool):
        raise TraversabilityError(f"{field} must be boolean")
    return value


def _enum(value: object, allowed: tuple[str, ...], field: str) -> str:
    value = _text(value, field)
    if value not in allowed:
        raise TraversabilityError(f"{field} must be one of {allowed!r}")
    return value


def _tuple(value: object, field: str) -> tuple[object, ...]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise TraversabilityError(f"{field} must be a sequence")
    return tuple(value)


@dataclass(frozen=True, slots=True)
class SeamObservationV1:
    seam_ref: str
    producer_ref: str
    consumer_ref: str
    status: str
    causal_reason: str | None
    reachable: bool
    activated: bool
    identity_continuous: bool
    contract_compatible: bool
    gap_class: str | None
    activation_qualifier: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "seam_ref", _text(self.seam_ref, "seam_ref"))
        object.__setattr__(self, "producer_ref", _text(self.producer_ref, "producer_ref"))
        object.__setattr__(self, "consumer_ref", _text(self.consumer_ref, "consumer_ref"))
        status = _enum(self.status, ("PASS", "FAIL"), "status")
        object.__setattr__(self, "status", status)
        reason = _optional_text(self.causal_reason, "causal_reason")
        object.__setattr__(self, "causal_reason", reason)
        for field in (
            "reachable",
            "activated",
            "identity_continuous",
            "contract_compatible",
            "activation_qualifier",
        ):
            object.__setattr__(self, field, _boolean(getattr(self, field), field))
        gap_class = None if self.gap_class is None else _enum(self.gap_class, GAP_CLASSES, "gap_class")
        object.__setattr__(self, "gap_class", gap_class)

        supports_handoff = (
            self.reachable
            and self.activated
            and self.identity_continuous
            and self.contract_compatible
        )
        if status == "PASS":
            if not supports_handoff or reason is not None or gap_class is not None:
                raise TraversabilityError("PASS seam contains contradictory failure facts")
            if self.activation_qualifier:
                raise TraversabilityError("PASS seam cannot carry Activation")
        elif supports_handoff and gap_class != "IMPLEMENTATION_GAP":
            raise TraversabilityError("FAIL seam contains no failing fact")
        if self.activation_qualifier and gap_class not in (None, "WIRING_GAP"):
            raise TraversabilityError("Activation is only a WIRING_GAP qualifier")
        if self.activation_qualifier and not self.identity_continuous:
            raise TraversabilityError(
                "Activation cannot qualify an orchestration failure"
            )


@dataclass(frozen=True, slots=True)
class CriticalJourneyProjectionV1:
    journey_id: str
    applicability: str
    current_state: str
    ordered_seams: tuple[SeamObservationV1, ...]
    placeholder_policy: str
    real_behavior_present: bool
    traversal_probe_admissible: bool
    evidence_admissible: bool
    observation_block: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "journey_id", _text(self.journey_id, "journey_id"))
        applicability = _enum(self.applicability, APPLICABILITY_VALUES, "applicability")
        object.__setattr__(self, "applicability", applicability)
        current_state = _text(self.current_state, "current_state")
        if applicability == "NOT_APPLICABLE":
            if current_state != "NONE":
                raise TraversabilityError("NOT_APPLICABLE journey must use current_state NONE")
        elif current_state not in JOURNEY_STATES:
            raise TraversabilityError("REQUIRED journey has an invalid current_state")
        object.__setattr__(self, "current_state", current_state)

        raw_seams = _tuple(self.ordered_seams, "ordered_seams")
        seams: tuple[SeamObservationV1, ...] = tuple(
            seam if isinstance(seam, SeamObservationV1) else
            (_raise_type("ordered_seams", seam))
            for seam in raw_seams
        )
        if applicability == "REQUIRED" and not seams:
            raise TraversabilityError("REQUIRED journey must declare ordered_seams")
        seam_refs = [seam.seam_ref for seam in seams]
        if len(seam_refs) != len(set(seam_refs)):
            raise TraversabilityError("ordered_seams must have unique seam_ref values")
        object.__setattr__(self, "ordered_seams", seams)

        object.__setattr__(
            self,
            "placeholder_policy",
            _enum(self.placeholder_policy, PLACEHOLDER_VALUES, "placeholder_policy"),
        )
        object.__setattr__(
            self,
            "real_behavior_present",
            _boolean(self.real_behavior_present, "real_behavior_present"),
        )
        object.__setattr__(
            self,
            "traversal_probe_admissible",
            _boolean(self.traversal_probe_admissible, "traversal_probe_admissible"),
        )
        object.__setattr__(
            self,
            "evidence_admissible",
            _boolean(self.evidence_admissible, "evidence_admissible"),
        )
        object.__setattr__(
            self,
            "observation_block",
            _enum(
                self.observation_block,
                ("NONE", "BLOCKED_BY_ENVIRONMENT", "BLOCKED_BY_MISSING_PROBE"),
                "observation_block",
            ),
        )
        if self.placeholder_policy == "NONE" and not self.real_behavior_present:
            # This is a valid implementation gap, not malformed input.
            pass
        elif self.placeholder_policy != "NONE" and self.real_behavior_present:
            raise TraversabilityError("placeholder cannot claim real behavior")


def _raise_type(field: str, value: object) -> SeamObservationV1:
    raise TraversabilityError(f"{field} contains an invalid value: {value!r}")


@dataclass(frozen=True, slots=True)
class SeamResultV1:
    seam_ref: str
    disposition: str
    causal_reason: str | None

    def __post_init__(self) -> None:
        object.__setattr__(self, "seam_ref", _text(self.seam_ref, "seam_ref"))
        object.__setattr__(
            self,
            "disposition",
            _enum(self.disposition, SEAM_DISPOSITIONS, "disposition"),
        )
        object.__setattr__(
            self,
            "causal_reason",
            _optional_text(self.causal_reason, "causal_reason"),
        )
        if self.disposition in ("PASS", "DOWNSTREAM_UNREACHABLE", "UNOBSERVED") and self.causal_reason is not None:
            raise TraversabilityError("non-causal seam disposition cannot carry a causal reason")
        if self.disposition == "FAIL" and self.causal_reason is None:
            raise TraversabilityError("FAIL seam result requires causal_reason")


@dataclass(frozen=True, slots=True)
class JourneySmokeResultV1:
    journey_id: str
    applicability: str
    observed_traversability_state: str | None
    seams: tuple[SeamResultV1, ...]
    first_broken_seam: str | None
    gap_class: str | None
    activation_qualifier: bool
    check_disposition: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "journey_id", _text(self.journey_id, "journey_id"))
        applicability = _enum(self.applicability, APPLICABILITY_VALUES, "applicability")
        object.__setattr__(self, "applicability", applicability)
        if self.observed_traversability_state is not None:
            state = _enum(
                self.observed_traversability_state,
                JOURNEY_STATES,
                "observed_traversability_state",
            )
        else:
            state = None
        object.__setattr__(self, "observed_traversability_state", state)
        raw_seams = _tuple(self.seams, "seams")
        seams = tuple(
            seam if isinstance(seam, SeamResultV1) else
            (_raise_result_type("seams", seam))
            for seam in raw_seams
        )
        if len({seam.seam_ref for seam in seams}) != len(seams):
            raise TraversabilityError("seams must have unique seam_ref values")
        object.__setattr__(self, "seams", seams)
        first = _optional_text(self.first_broken_seam, "first_broken_seam")
        object.__setattr__(self, "first_broken_seam", first)
        gap_class = None if self.gap_class is None else _enum(self.gap_class, GAP_CLASSES, "gap_class")
        object.__setattr__(self, "gap_class", gap_class)
        object.__setattr__(
            self,
            "activation_qualifier",
            _boolean(self.activation_qualifier, "activation_qualifier"),
        )
        disposition = _enum(self.check_disposition, CHECK_DISPOSITIONS, "check_disposition")
        object.__setattr__(self, "check_disposition", disposition)
        if applicability == "NOT_APPLICABLE":
            if self.observed_traversability_state is not None or first is not None or gap_class is not None:
                raise TraversabilityError("NOT_APPLICABLE result cannot carry durable state or Gap")
            if disposition != "NOT_APPLICABLE" or self.activation_qualifier:
                raise TraversabilityError("NOT_APPLICABLE result is contradictory")
        elif disposition == "NOT_APPLICABLE":
            raise TraversabilityError("REQUIRED result cannot be NOT_APPLICABLE")


def _raise_result_type(field: str, value: object) -> SeamResultV1:
    raise TraversabilityError(f"{field} contains an invalid value: {value!r}")


@dataclass(frozen=True, slots=True)
class SystemTraversabilityResultV1:
    required_journey_ids: tuple[str, ...]
    journey_results: tuple[JourneySmokeResultV1, ...]
    check_disposition: str

    def __post_init__(self) -> None:
        raw_ids = _tuple(self.required_journey_ids, "required_journey_ids")
        ids = tuple(_text(value, "required_journey_ids item") for value in raw_ids)
        if len(ids) != len(set(ids)):
            raise TraversabilityError("required_journey_ids must be unique")
        object.__setattr__(self, "required_journey_ids", ids)
        raw_results = _tuple(self.journey_results, "journey_results")
        results = tuple(
            result if isinstance(result, JourneySmokeResultV1) else
            (_raise_system_type("journey_results", result))
            for result in raw_results
        )
        if len({result.journey_id for result in results}) != len(results):
            raise TraversabilityError("journey_results must have unique journey IDs")
        object.__setattr__(self, "journey_results", results)
        object.__setattr__(
            self,
            "check_disposition",
            _enum(self.check_disposition, CHECK_DISPOSITIONS, "check_disposition"),
        )


def _raise_system_type(field: str, value: object) -> JourneySmokeResultV1:
    raise TraversabilityError(f"{field} contains an invalid value: {value!r}")


def _seam_passes(seam: SeamObservationV1) -> bool:
    return (
        seam.status == "PASS"
        and seam.reachable
        and seam.activated
        and seam.identity_continuous
        and seam.contract_compatible
    )


def _failure_class(seam: SeamObservationV1) -> str:
    if not seam.identity_continuous:
        derived = "ORCHESTRATION_GAP"
    elif (
        seam.activation_qualifier
        or not seam.reachable
        or not seam.activated
        or not seam.contract_compatible
    ):
        derived = "WIRING_GAP"
    else:
        derived = "IMPLEMENTATION_GAP"
    if seam.gap_class is not None and seam.gap_class != derived:
        raise TraversabilityError(
            "supplied gap_class contradicts canonical causal precedence"
        )
    return derived


def _failure_reason(seam: SeamObservationV1, gap_class: str) -> str:
    if seam.causal_reason is not None:
        return seam.causal_reason
    if gap_class == "ORCHESTRATION_GAP":
        return "NO_LEGITIMATE_RUNTIME_LIFETIME_OWNER"
    if gap_class == "WIRING_GAP":
        return "HANDOFF_NOT_TRAVERSABLE"
    if gap_class == "IMPLEMENTATION_GAP":
        return "MISSING_NODE_BEHAVIOR"
    return "EVIDENCE_NOT_ADMISSIBLE"


def check_critical_journey_smoke(
    journey: CriticalJourneyProjectionV1,
) -> JourneySmokeResultV1:
    """Derive one immutable observation from one caller-supplied journey."""
    if not isinstance(journey, CriticalJourneyProjectionV1):
        raise TraversabilityError("journey must be CriticalJourneyProjectionV1")

    if journey.applicability == "NOT_APPLICABLE":
        seams = tuple(
            SeamResultV1(seam.seam_ref, "UNOBSERVED", None)
            for seam in journey.ordered_seams
        )
        return JourneySmokeResultV1(
            journey_id=journey.journey_id,
            applicability="NOT_APPLICABLE",
            observed_traversability_state=None,
            seams=seams,
            first_broken_seam=None,
            gap_class=None,
            activation_qualifier=False,
            check_disposition="NOT_APPLICABLE",
        )

    first_failure: int | None = None
    for index, seam in enumerate(journey.ordered_seams):
        if not _seam_passes(seam):
            first_failure = index
            break

    seam_results: list[SeamResultV1] = []
    if first_failure is not None:
        first = journey.ordered_seams[first_failure]
        gap_class = _failure_class(first)
        reason = _failure_reason(first, gap_class)
        for index, seam in enumerate(journey.ordered_seams):
            if index < first_failure:
                seam_results.append(SeamResultV1(seam.seam_ref, "PASS", None))
            elif index == first_failure:
                seam_results.append(SeamResultV1(seam.seam_ref, "FAIL", reason))
            else:
                seam_results.append(
                    SeamResultV1(seam.seam_ref, "DOWNSTREAM_UNREACHABLE", None)
                )
        return JourneySmokeResultV1(
            journey_id=journey.journey_id,
            applicability="REQUIRED",
            observed_traversability_state="WIRED_FAIL",
            seams=tuple(seam_results),
            first_broken_seam=first.seam_ref,
            gap_class=gap_class,
            activation_qualifier=first.activation_qualifier,
            check_disposition="WIRED_FAIL",
        )

    seam_results = [
        SeamResultV1(seam.seam_ref, "PASS", None)
        for seam in journey.ordered_seams
    ]

    if (
        not journey.real_behavior_present
        and journey.placeholder_policy == "NONE"
    ):
        return JourneySmokeResultV1(
            journey_id=journey.journey_id,
            applicability="REQUIRED",
            observed_traversability_state="WIRED_FAIL",
            seams=tuple(seam_results),
            first_broken_seam=None,
            gap_class="IMPLEMENTATION_GAP",
            activation_qualifier=False,
            check_disposition="WIRED_FAIL",
        )

    if journey.observation_block == "BLOCKED_BY_ENVIRONMENT":
        return JourneySmokeResultV1(
            journey_id=journey.journey_id,
            applicability="REQUIRED",
            observed_traversability_state=journey.current_state,
            seams=tuple(seam_results),
            first_broken_seam=None,
            gap_class=None,
            activation_qualifier=False,
            check_disposition="BLOCKED_BY_ENVIRONMENT",
        )

    if (
        journey.observation_block == "BLOCKED_BY_MISSING_PROBE"
        or not journey.traversal_probe_admissible
        or not journey.evidence_admissible
    ):
        return JourneySmokeResultV1(
            journey_id=journey.journey_id,
            applicability="REQUIRED",
            observed_traversability_state=journey.current_state,
            seams=tuple(seam_results),
            first_broken_seam=None,
            gap_class="EVIDENCE_GAP",
            activation_qualifier=False,
            check_disposition="BLOCKED_BY_MISSING_PROBE",
        )

    if not journey.real_behavior_present:
        return JourneySmokeResultV1(
            journey_id=journey.journey_id,
            applicability="REQUIRED",
            observed_traversability_state="WIRED_TRAVERSABLE",
            seams=tuple(seam_results),
            first_broken_seam=None,
            gap_class=None,
            activation_qualifier=False,
            check_disposition="PASS",
        )

    observed_state = (
        "WIRED_TRAVERSABLE"
        if journey.placeholder_policy != "NONE"
        else "PASSING"
    )
    return JourneySmokeResultV1(
        journey_id=journey.journey_id,
        applicability="REQUIRED",
        observed_traversability_state=observed_state,
        seams=tuple(seam_results),
        first_broken_seam=None,
        gap_class=None,
        activation_qualifier=False,
        check_disposition="PASS",
    )


def check_system_traversability(
    observations: Sequence[JourneySmokeResultV1],
) -> SystemTraversabilityResultV1:
    """Aggregate already-derived journey observations without discovery or writes."""
    if isinstance(observations, (str, bytes)) or not isinstance(observations, Sequence):
        raise TraversabilityError("observations must be a sequence")
    values = tuple(observations)
    if any(not isinstance(value, JourneySmokeResultV1) for value in values):
        raise TraversabilityError("observations contain an invalid result")
    if len({value.journey_id for value in values}) != len(values):
        raise TraversabilityError("observations must have unique journey IDs")

    required = tuple(
        value for value in values if value.applicability == "REQUIRED"
    )
    required_ids = tuple(value.journey_id for value in required)
    if not required:
        disposition = "NOT_APPLICABLE"
    elif all(value.check_disposition == "PASS" for value in required):
        disposition = "PASS"
    elif any(value.check_disposition == "WIRED_FAIL" for value in required):
        disposition = "WIRED_FAIL"
    elif any(
        value.check_disposition == "BLOCKED_BY_ENVIRONMENT"
        for value in required
    ):
        disposition = "BLOCKED_BY_ENVIRONMENT"
    elif any(
        value.check_disposition == "BLOCKED_BY_MISSING_PROBE"
        for value in required
    ):
        disposition = "BLOCKED_BY_MISSING_PROBE"
    else:
        raise TraversabilityError("required observations have no aggregate disposition")

    return SystemTraversabilityResultV1(
        required_journey_ids=required_ids,
        journey_results=values,
        check_disposition=disposition,
    )


__all__ = [
    "APPLICABILITY_VALUES",
    "CHECK_DISPOSITIONS",
    "CriticalJourneyProjectionV1",
    "GAP_CLASSES",
    "JOURNEY_STATES",
    "JourneySmokeResultV1",
    "PLACEHOLDER_VALUES",
    "SEAM_DISPOSITIONS",
    "SeamObservationV1",
    "SeamResultV1",
    "SystemTraversabilityResultV1",
    "TraversabilityError",
    "check_critical_journey_smoke",
    "check_system_traversability",
]
