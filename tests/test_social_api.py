import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.social_api import PLATFORMS, SocialAPIClient


def test_platform_registry():
    assert "youtube" in PLATFORMS
    assert issubclass(PLATFORMS["youtube"], SocialAPIClient)
