"""Social platform API client implementations."""

import time
from typing import Dict, Optional, Type


class SocialAPIClient:
    """Base class for social platform clients with simple rate limiting."""

    rate_limit: float = 1.0  # seconds between calls

    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key
        self._last_call = 0.0

    def _wait_rate_limit(self) -> None:
        now = time.time()
        delta = now - self._last_call
        if delta < self.rate_limit:
            time.sleep(self.rate_limit - delta)
        self._last_call = time.time()

    def authenticate(self) -> None:
        """Authenticate with the platform."""
        pass

    def get_post_metrics(self, post_id: str) -> Dict:
        """Retrieve metrics for a post."""
        raise NotImplementedError


PLATFORMS: Dict[str, Type[SocialAPIClient]] = {}


class YouTubeAPIClient(SocialAPIClient):
    """Client for YouTube API."""

    def authenticate(self) -> None:
        # Placeholder for real auth
        pass

    def get_post_metrics(self, post_id: str) -> Dict:
        self._wait_rate_limit()
        # Placeholder response
        return {"views": 0, "likes": 0, "comments": 0, "shares": 0}


class TikTokAPIClient(SocialAPIClient):
    """Client for TikTok API."""

    def authenticate(self) -> None:
        # Placeholder for real auth
        pass

    def get_post_metrics(self, post_id: str) -> Dict:
        self._wait_rate_limit()
        return {"views": 0, "likes": 0, "comments": 0, "shares": 0}


class InstagramAPIClient(SocialAPIClient):
    """Client for Instagram API."""

    def authenticate(self) -> None:
        # Placeholder for real auth
        pass

    def get_post_metrics(self, post_id: str) -> Dict:
        self._wait_rate_limit()
        return {"views": 0, "likes": 0, "comments": 0, "shares": 0}


PLATFORMS["youtube"] = YouTubeAPIClient
PLATFORMS["tiktok"] = TikTokAPIClient
PLATFORMS["instagram"] = InstagramAPIClient
