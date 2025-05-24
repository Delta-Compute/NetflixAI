"""Coordinate social media verification and metrics collection."""

from __future__ import annotations

from typing import Dict

from .attribution import AttributionTagManager
from .social_verification import TemporalVerifier, ContentAuthenticityVerifier
from .engagement import EngagementMetricsCollector, normalize_metrics
from .database import Database


class SocialIntegrationCoordinator:
    """High level helper orchestrating social media interactions."""

    def __init__(self, db: Database, allowed_drift: float = 600.0) -> None:
        self.db = db
        self.tag_manager = AttributionTagManager()
        temporal = TemporalVerifier(allowed_drift=allowed_drift)
        self.verifier = ContentAuthenticityVerifier(self.tag_manager, temporal)
        self.collector = EngagementMetricsCollector()

    def create_tag(self, submission_id: str, miner_id: str, timestamp: float) -> str:
        """Create and store an attribution tag."""
        return self.tag_manager.create_attribution_tag(submission_id, miner_id, timestamp)

    def verify_post(self, post_id: str, platform: str, reference_time: float) -> bool:
        """Verify a social media post."""
        return self.verifier.verify(post_id, platform, reference_time)

    def collect_metrics(self, post_id: str, platform: str) -> Dict[str, float]:
        """Collect and normalize engagement metrics."""
        raw = self.collector.collect(post_id, platform)
        return normalize_metrics(raw)

    def process_post(
        self,
        submission_id: str,
        post_id: str,
        platform: str,
        reference_time: float,
    ) -> Dict[str, float]:
        """Verify a post, collect metrics and persist results."""
        valid = self.verify_post(post_id, platform, reference_time)
        self.db.insert_social_post(submission_id, post_id, platform, valid)

        metrics = self.collect_metrics(post_id, platform)
        self.db.update_social_metrics(
            post_id,
            platform,
            int(metrics.get("views", 0)),
            int(metrics.get("likes", 0)),
            int(metrics.get("comments", 0)),
            int(metrics.get("shares", 0)),
        )
        return metrics
