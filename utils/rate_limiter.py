"""Token bucket rate limiter for API usage."""

from __future__ import annotations

import time
from typing import Dict


class RateLimiter:
    """Manage API call rates and track costs."""

    def __init__(self, rate: int, per: float) -> None:
        self.rate = rate
        self.per = per
        self.allowance: Dict[str, float] = {}
        self.last_check: Dict[str, float] = {}
        self.costs: Dict[str, float] = {}

    def check(self, key: str, cost: float = 0.0) -> bool:
        """Return True if a call is allowed for the given key."""
        now = time.time()
        allowance = self.allowance.get(key, self.rate)
        last = self.last_check.get(key, now)
        allowance += (now - last) * (self.rate / self.per)
        if allowance > self.rate:
            allowance = self.rate
        if allowance < 1:
            self.allowance[key] = allowance
            self.last_check[key] = now
            return False
        else:
            allowance -= 1
            self.allowance[key] = allowance
            self.last_check[key] = now
            self.costs[key] = self.costs.get(key, 0.0) + cost
            return True

    def get_cost(self, key: str) -> float:
        """Return accumulated API cost for a key."""
        return self.costs.get(key, 0.0)
