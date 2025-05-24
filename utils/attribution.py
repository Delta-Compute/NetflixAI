"""Attribution tag generation and management utilities."""

from __future__ import annotations

import hashlib
import os
import re
import time
from typing import Dict, Optional


class AttributionTagManager:
    """Create and validate attribution tags for submissions."""

    TAG_PATTERN = re.compile(
        r"Built with Bittensor and TensorFlix - hash ([a-f0-9]{64})",
        re.IGNORECASE,
    )

    def __init__(self) -> None:
        self._tags: Dict[str, Dict[str, str | float]] = {}

    def generate_unique_hash(self, miner_id: str, submission_timestamp: float) -> str:
        """Generate a unique hash from miner id, timestamp and random salt."""
        while True:
            salt = os.urandom(16).hex()
            data = f"{miner_id}{submission_timestamp}{salt}".encode()
            tag_hash = hashlib.sha256(data).hexdigest()
            if not any(t["hash"] == tag_hash for t in self._tags.values()):
                return tag_hash

    def create_attribution_tag(
        self, submission_id: str, miner_id: str, submission_timestamp: float
    ) -> str:
        """Create and store a new attribution tag."""
        tag_hash = self.generate_unique_hash(miner_id, submission_timestamp)
        tag = f"Built with Bittensor and TensorFlix - hash {tag_hash}"
        self._tags[submission_id] = {
            "tag": tag,
            "hash": tag_hash,
            "timestamp": time.time(),
        }
        return tag

    def get_tag(self, submission_id: str) -> Optional[str]:
        """Retrieve a stored tag if not expired."""
        record = self._tags.get(submission_id)
        if not record:
            return None
        if time.time() - record["timestamp"] > 86400:
            self._tags.pop(submission_id, None)
            return None
        return record["tag"]

    def validate_tag(self, tag: str) -> bool:
        """Check if a tag matches stored hashes and pattern."""
        match = self.TAG_PATTERN.fullmatch(tag.strip())
        if not match:
            return False
        tag_hash = match.group(1)
        for record in list(self._tags.values()):
            if time.time() - record["timestamp"] > 86400:
                self._tags.pop(next(k for k, v in self._tags.items() if v == record), None)
                continue
            if record["hash"] == tag_hash:
                return True
        return False
