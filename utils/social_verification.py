"""Social media post verification utilities."""

from __future__ import annotations

from typing import Optional
import time

from .attribution import AttributionTagManager
from .social_api import PLATFORMS, SocialAPIClient


class SocialMediaVerifier:
    """Verify that social media posts contain valid attribution tags."""

    def __init__(self, tag_manager: AttributionTagManager) -> None:
        self.tag_manager = tag_manager

    def verify_post_text(self, text: str) -> bool:
        """Verify raw post text for a valid attribution tag."""
        return self.tag_manager.validate_tag(text)

    def verify_post(self, post_id: str, platform: str) -> bool:
        """Fetch and verify a post on a specific platform."""
        client_cls: Optional[type[SocialAPIClient]] = PLATFORMS.get(platform)
        if not client_cls:
            return False
        client = client_cls()
        client.authenticate()
        try:
            text = client.get_post_text(post_id)
        except Exception:
            return False
        return self.verify_post_text(text)


class TemporalVerifier:
    """Verify that a post occurred within an allowed time window."""

    def __init__(self, allowed_drift: float = 600.0) -> None:
        self.allowed_drift = allowed_drift

    def verify(self, post_time: float, reference_time: float) -> bool:
        """Check that the time difference does not exceed allowed drift."""
        return abs(post_time - reference_time) <= self.allowed_drift


class ContentAuthenticityVerifier:
    """Check posts for valid attribution and timing."""

    def __init__(self, tag_manager: AttributionTagManager, temporal_verifier: TemporalVerifier) -> None:
        self.tag_manager = tag_manager
        self.temporal_verifier = temporal_verifier

    def verify(self, post_id: str, platform: str, reference_time: float) -> bool:
        client_cls: Optional[type[SocialAPIClient]] = PLATFORMS.get(platform)
        if not client_cls:
            return False
        client = client_cls()
        client.authenticate()
        try:
            text = client.get_post_text(post_id)
            timestamp = client.get_post_time(post_id)
        except Exception:
            return False
        if not self.tag_manager.validate_tag(text):
            return False
        return self.temporal_verifier.verify(timestamp, reference_time)
