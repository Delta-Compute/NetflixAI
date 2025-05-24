"""Account history analysis utilities."""

from __future__ import annotations

from typing import Dict
from .social_api import PLATFORMS


class AccountHistoryAnalyzer:
    """Analyze a user's posting history on a platform."""

    def __init__(self, max_posts: int = 100) -> None:
        self.max_posts = max_posts

    def fetch_post_history(self, user_id: str, platform: str) -> list[str]:
        """Fetch a list of post IDs for a user on a given platform."""
        client_cls = PLATFORMS.get(platform)
        if not client_cls:
            return []
        client = client_cls()
        client.authenticate()
        try:
            # Placeholder: real implementation would use platform APIs
            return [f"{user_id}_{i}" for i in range(self.max_posts)]
        except Exception:
            return []

    def analyze_history(self, user_id: str, platform: str) -> Dict[str, float]:
        """Return simple statistics about a user's history."""
        posts = self.fetch_post_history(user_id, platform)
        return {
            "post_count": float(len(posts)),
        }
