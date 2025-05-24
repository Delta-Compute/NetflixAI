# The MIT License (MIT)
# Copyright © 2024 Your Organization

import os
from typing import Dict, Any

class Config:
    """
    Configuration class for Subnet 89.
    Centralizes all configuration parameters.
    """
    
    # Network configuration
    NETUID = 89
    NETWORK = os.environ.get("BT_NETWORK", "finney")  # finney, test, local
    
    # Timing configuration
    QUERY_INTERVAL = 12  # seconds (1 block)
    WEIGHT_UPDATE_INTERVAL = 100  # blocks
    SYNC_INTERVAL = 5  # blocks
    
    # Miner configuration
    MINER_BLACKLIST_THRESHOLD = 0.1  # Minimum stake to accept requests
    MINER_MAX_CONCURRENT_REQUESTS = 10
    
    # Validator configuration
    VALIDATOR_QUERY_TIMEOUT = 10  # seconds
    VALIDATOR_SAMPLE_SIZE = 10  # Number of miners to query per round
    VALIDATOR_MIN_STAKE = 1000  # Minimum stake to be a validator
    
    # Scoring configuration
    SCORE_DECAY_FACTOR = 0.9
    SCORE_UPDATE_FACTOR = 0.1
    MIN_SCORE_THRESHOLD = 0.01
    
    # Logging configuration
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_DIR = os.environ.get("LOG_DIR", "./logs")
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Return configuration as dictionary."""
        return {
            "netuid": cls.NETUID,
            "network": cls.NETWORK,
            "query_interval": cls.QUERY_INTERVAL,
            "weight_update_interval": cls.WEIGHT_UPDATE_INTERVAL,
            "sync_interval": cls.SYNC_INTERVAL,
            "miner": {
                "blacklist_threshold": cls.MINER_BLACKLIST_THRESHOLD,
                "max_concurrent_requests": cls.MINER_MAX_CONCURRENT_REQUESTS,
            },
            "validator": {
                "query_timeout": cls.VALIDATOR_QUERY_TIMEOUT,
                "sample_size": cls.VALIDATOR_SAMPLE_SIZE,
                "min_stake": cls.VALIDATOR_MIN_STAKE,
            },
            "scoring": {
                "decay_factor": cls.SCORE_DECAY_FACTOR,
                "update_factor": cls.SCORE_UPDATE_FACTOR,
                "min_threshold": cls.MIN_SCORE_THRESHOLD,
            },
            "logging": {
                "level": cls.LOG_LEVEL,
                "dir": cls.LOG_DIR,
            }
        }