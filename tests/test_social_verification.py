from utils.attribution import AttributionTagManager
from utils.social_verification import SocialMediaVerifier
from utils.social_api import SocialAPIClient, PLATFORMS


class DummyClient(SocialAPIClient):
    def get_post_metrics(self, post_id: str):
        return {}

    def get_post_text(self, post_id: str) -> str:
        return stored_tag


PLATFORMS["dummy"] = DummyClient

tag_manager = AttributionTagManager()
stored_tag = tag_manager.create_attribution_tag("sub1", "miner1", 0.0)


def test_verify_post_text():
    verifier = SocialMediaVerifier(tag_manager)
    assert verifier.verify_post_text(stored_tag)


def test_verify_post():
    verifier = SocialMediaVerifier(tag_manager)
    assert verifier.verify_post("123", "dummy")
