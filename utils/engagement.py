"""Utilities for collecting engagement metrics from social platforms."""

from __future__ import annotations

from typing import Dict

from .social_api import PLATFORMS, SocialAPIClient


class EngagementMetricsCollector:
    """Collect engagement metrics from configured platform APIs."""

    def collect(self, post_id: str, platform: str) -> Dict:
        client_cls = PLATFORMS.get(platform)
        if not client_cls:
            return {}
        client: SocialAPIClient = client_cls()
        client.authenticate()
        try:
            return client.get_post_metrics(post_id)
        except Exception:
            return {}


def normalize_metrics(metrics: Dict[str, int | float]) -> Dict[str, float]:
    """Normalize raw metric dict to a common schema."""
    fields = ["views", "likes", "comments", "shares"]
    normalized = {}
    for field in fields:
        value = metrics.get(field, 0)
        try:
            normalized[field] = float(value)
        except Exception:
            normalized[field] = 0.0
    return normalized


def is_viral(
    metrics: Dict[str, float],
    view_threshold: int = 100000,
    engagement_rate_threshold: float = 0.1,
) -> bool:
    """Determine if metrics indicate viral content."""
    views = metrics.get("views", 0.0)
    if views < view_threshold:
        return False
    likes = metrics.get("likes", 0.0)
    comments = metrics.get("comments", 0.0)
    shares = metrics.get("shares", 0.0)
    rate = (likes + comments + shares) / views if views else 0.0
    return rate >= engagement_rate_threshold
