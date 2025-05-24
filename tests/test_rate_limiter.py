from utils.rate_limiter import RateLimiter
import time


def test_rate_limiter_basic():
    rl = RateLimiter(2, 1)
    assert rl.check("x")
    assert rl.check("x")
    assert not rl.check("x")
    time.sleep(1)
    assert rl.check("x")
