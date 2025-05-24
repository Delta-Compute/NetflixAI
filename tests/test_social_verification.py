from utils.attribution import AttributionTagManager
from utils.social_verification import (
    SocialMediaVerifier,
    TemporalVerifier,
    ContentAuthenticityVerifier,
)
from utils.social_api import SocialAPIClient, PLATFORMS


class DummyClient(SocialAPIClient):
    def get_post_metrics(self, post_id: str):
        return {}

    def get_post_text(self, post_id: str) -> str:
        return stored_tag

    def get_post_time(self, post_id: str) -> float:
        return 0.0


PLATFORMS["dummy"] = DummyClient

tag_manager = AttributionTagManager()
stored_tag = tag_manager.create_attribution_tag("sub1", "miner1", 0.0)


def test_verify_post_text():
    verifier = SocialMediaVerifier(tag_manager)
    assert verifier.verify_post_text(stored_tag)


def test_verify_post():
    verifier = SocialMediaVerifier(tag_manager)
    assert verifier.verify_post("123", "dummy")


def test_temporal_verifier():
    verifier = TemporalVerifier(allowed_drift=10)
    assert verifier.verify(5.0, 0.0)
    assert not verifier.verify(20.0, 0.0)


def test_content_authenticity_verifier():
    tv = TemporalVerifier(allowed_drift=5)
    cav = ContentAuthenticityVerifier(tag_manager, tv)
    assert cav.verify("123", "dummy", 0.0)
