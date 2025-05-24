"""Utilities for detecting metric gaming on social platforms."""

from __future__ import annotations

from typing import Dict


class GamingDetector:
    """Detect suspicious engagement patterns."""

    def __init__(self, like_view_ratio_threshold: float = 10.0) -> None:
        self.like_view_ratio_threshold = like_view_ratio_threshold

    def detect(self, metrics: Dict[str, int]) -> bool:
        """Return True if metrics appear to be artificially inflated."""
        views = metrics.get("views", 0)
        likes = metrics.get("likes", 0)
        if views == 0:
            return False
        ratio = likes / views
        return ratio > self.like_view_ratio_threshold
