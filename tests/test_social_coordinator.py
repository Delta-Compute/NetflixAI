from utils.social_coordinator import SocialMediaCoordinator


def test_process_post_rate_limit():
    coord = SocialMediaCoordinator(rate=1, per=1)
    assert coord.process_post("p", "youtube", "u")["rate_limited"] is False
    assert coord.process_post("p", "youtube", "u")["rate_limited"] is True
