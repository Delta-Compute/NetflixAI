"""Coordinate social media verification workflows."""

from __future__ import annotations

from typing import Dict
from .deep_verification import DeepVerificationPipeline
from .rate_limiter import RateLimiter


class SocialMediaCoordinator:
    """High-level interface for social media integration."""

    def __init__(self, rate: int = 60, per: float = 60.0) -> None:
        self.pipeline = DeepVerificationPipeline()
        self.limiter = RateLimiter(rate, per)

    def process_post(self, post_id: str, platform: str, user_id: str) -> Dict[str, bool]:
        if not self.limiter.check(platform):
            return {"rate_limited": True}
        result = self.pipeline.verify_post(post_id, platform, user_id)
        result["rate_limited"] = False
        return result
