from utils.social_api import PLATFORMS, YouTubeAPIClient


def test_platform_registry():
    assert "youtube" in PLATFORMS
    assert issubclass(PLATFORMS["youtube"], YouTubeAPIClient)
