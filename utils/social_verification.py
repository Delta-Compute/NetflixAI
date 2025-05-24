"""Social media post verification utilities."""

from __future__ import annotations

from typing import Optional

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
