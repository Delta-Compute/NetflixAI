from utils.social_api import (
    PLATFORMS,
    YouTubeAPIClient,
    TikTokAPIClient,
    InstagramAPIClient,
)


def test_platform_registry():
    assert "youtube" in PLATFORMS
    assert issubclass(PLATFORMS["youtube"], YouTubeAPIClient)


def test_get_post_time():
    yt = YouTubeAPIClient()
    tk = TikTokAPIClient()
    ig = InstagramAPIClient()
    assert isinstance(yt.get_post_time("a"), float)
    assert isinstance(tk.get_post_time("a"), float)
    assert isinstance(ig.get_post_time("a"), float)
