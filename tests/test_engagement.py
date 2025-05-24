from utils.engagement import (
    EngagementMetricsCollector,
    normalize_metrics,
    is_viral,
)
from utils.social_api import SocialAPIClient, PLATFORMS


class DummyClient(SocialAPIClient):
    def get_post_metrics(self, post_id: str):
        return {"views": 1}

    def get_post_text(self, post_id: str) -> str:
        return ""

    def get_post_time(self, post_id: str) -> float:
        return 0.0


PLATFORMS["metrics_dummy"] = DummyClient


def test_collect_metrics():
    collector = EngagementMetricsCollector()
    data = collector.collect("123", "metrics_dummy")
    assert data == {"views": 1}


def test_normalize_metrics():
    raw = {"views": "10", "likes": 5}
    norm = normalize_metrics(raw)
    assert norm["views"] == 10.0
    assert norm["likes"] == 5.0
    assert norm["comments"] == 0.0


def test_is_viral():
    metrics = {"views": 200000, "likes": 30000, "comments": 2000, "shares": 500}
    assert is_viral(metrics)
    assert not is_viral({"views": 100})
