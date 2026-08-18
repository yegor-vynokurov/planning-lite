"""Bounded Experiment Campaign Core for Planning Lite.

This package is opt-in runtime infrastructure. Importing or installing it does
not create repository-local campaign files and does not authorize release.
"""

from .attempt_reconciliation import (
    AttemptEvidenceReconciliationError,
    build_reconciled_suite_payload,
    reconcile_completed_attempt_suite_evidence,
)

from .campaign import (
    AttemptBudgetAdmissionPolicy,
    AttemptBudgetReservation,
    CampaignError,
    CampaignManifest,
    append_campaign_event,
    initialize_campaign,
    inspect_campaign,
    load_campaign_journal,
    load_campaign_manifest,
    load_manifest_template,
    prepare_attempt_budget_admission,
    validate_attempt_budget_reservation,
)

__all__ = [
    "AttemptEvidenceReconciliationError",
    "build_reconciled_suite_payload",
    "reconcile_completed_attempt_suite_evidence",
    "AttemptBudgetAdmissionPolicy",
    "AttemptBudgetReservation",
    "CampaignError",
    "CampaignManifest",
    "append_campaign_event",
    "initialize_campaign",
    "inspect_campaign",
    "load_campaign_journal",
    "load_campaign_manifest",
    "load_manifest_template",
    "prepare_attempt_budget_admission",
    "validate_attempt_budget_reservation",
]
