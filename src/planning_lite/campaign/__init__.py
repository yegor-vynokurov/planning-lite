"""Bounded Experiment Campaign Core for Planning Lite.

This package is opt-in runtime infrastructure. Importing or installing it does
not create repository-local campaign files and does not authorize release.
"""

from .campaign import (
    CampaignError,
    CampaignManifest,
    append_campaign_event,
    initialize_campaign,
    inspect_campaign,
    load_campaign_journal,
    load_campaign_manifest,
    load_manifest_template,
)

__all__ = [
    "CampaignError",
    "CampaignManifest",
    "append_campaign_event",
    "initialize_campaign",
    "inspect_campaign",
    "load_campaign_journal",
    "load_campaign_manifest",
    "load_manifest_template",
]
