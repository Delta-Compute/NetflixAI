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

    # IPFS configuration
    IPFS_GATEWAY = os.environ.get("IPFS_GATEWAY", "http://localhost:5001")

    # Video limits
    MAX_VIDEO_SIZE = int(os.environ.get("MAX_VIDEO_SIZE", 1024 * 1024 * 1024))  # 1GB
    SUPPORTED_VIDEO_FORMATS = os.environ.get("SUPPORTED_VIDEO_FORMATS", "mp4,mov,mkv").split(",")

    # Social platform API keys
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
    TIKTOK_API_KEY = os.environ.get("TIKTOK_API_KEY", "")
    INSTAGRAM_API_KEY = os.environ.get("INSTAGRAM_API_KEY", "")

    # AI model paths
    DEEPFAKE_MODEL_PATH = os.environ.get("DEEPFAKE_MODEL_PATH", "./models/deepfake.pt")
    QUALITY_MODEL_PATH = os.environ.get("QUALITY_MODEL_PATH", "./models/quality.pt")
    CLASSIFICATION_MODEL_PATH = os.environ.get("CLASSIFICATION_MODEL_PATH", "./models/classify.pt")

    # Storage configuration
    MAX_STORAGE_SIZE = int(os.environ.get("MAX_STORAGE_SIZE", 500 * 1024 ** 3))

    # Validation thresholds
    VALIDATION_SCORE_THRESHOLD = float(os.environ.get("VALIDATION_SCORE_THRESHOLD", 0.5))

    # Rate limiting
    RATE_LIMIT_REQUESTS = int(os.environ.get("RATE_LIMIT_REQUESTS", 10))
    RATE_LIMIT_PERIOD = int(os.environ.get("RATE_LIMIT_PERIOD", 60))

    # Database configuration
    DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING", "subnet89.db")
    
    # Scoring configuration
    SCORE_DECAY_FACTOR = 0.9
    SCORE_UPDATE_FACTOR = 0.1
    MIN_SCORE_THRESHOLD = 0.01
    
    # Logging configuration
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR"]
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
                "levels": cls.LOG_LEVELS,
            },
            "ipfs": {"gateway": cls.IPFS_GATEWAY},
            "video": {
                "max_size": cls.MAX_VIDEO_SIZE,
                "formats": cls.SUPPORTED_VIDEO_FORMATS,
            },
            "api_keys": {
                "youtube": cls.YOUTUBE_API_KEY,
                "tiktok": cls.TIKTOK_API_KEY,
                "instagram": cls.INSTAGRAM_API_KEY,
            },
            "models": {
                "deepfake": cls.DEEPFAKE_MODEL_PATH,
                "quality": cls.QUALITY_MODEL_PATH,
                "classification": cls.CLASSIFICATION_MODEL_PATH,
            },
            "storage": {"max_size": cls.MAX_STORAGE_SIZE},
            "validation": {"score_threshold": cls.VALIDATION_SCORE_THRESHOLD},
            "rate_limit": {
                "requests": cls.RATE_LIMIT_REQUESTS,
                "period": cls.RATE_LIMIT_PERIOD,
            },
            "database": {"connection": cls.DB_CONNECTION_STRING}
        }