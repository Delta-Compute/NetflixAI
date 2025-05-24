"""Pipeline for multi-step social media verification."""

from __future__ import annotations

from typing import Dict
from .social_verification import SocialMediaVerifier
from .attribution import AttributionTagManager
from .account_history import AccountHistoryAnalyzer
from .gaming_detection import GamingDetector


class DeepVerificationPipeline:
    """Run a series of checks to verify social media content."""

    def __init__(self) -> None:
        self.verifier = SocialMediaVerifier(AttributionTagManager())
        self.history_analyzer = AccountHistoryAnalyzer()
        self.gaming_detector = GamingDetector()

    def verify_post(self, post_id: str, platform: str, user_id: str) -> Dict[str, bool]:
        """Return results from multiple verification steps."""
        tag_ok = self.verifier.verify_post(post_id, platform)
        history_stats = self.history_analyzer.analyze_history(user_id, platform)
        metrics = self.verifier.tag_manager._tags.get(post_id, {})  # placeholder
        gaming = self.gaming_detector.detect(metrics)
        return {
            "tag_valid": tag_ok,
            "history_analyzed": bool(history_stats),
            "gaming_detected": gaming,
        }
