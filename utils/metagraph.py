# The MIT License (MIT)
# Copyright © 2024 Your Organization

import bittensor as bt
from typing import List, Dict, Tuple
import torch

class MetagraphUtils:
    """Utility functions for working with the Bittensor metagraph."""
    
    @staticmethod
    def get_active_miners(metagraph: bt.metagraph) -> List[Tuple[int, bt.axon]]:
        """
        Get list of active miners (non-zero IP addresses).
        
        Args:
            metagraph: Bittensor metagraph instance
            
        Returns:
            List of (uid, axon) tuples for active miners
        """
        active_miners = []
        for uid, axon in enumerate(metagraph.axons):
            if axon.ip != "0.0.0.0":
                active_miners.append((uid, axon))
        return active_miners
    
    @staticmethod
    def get_validators(metagraph: bt.metagraph, min_stake: float = 1000) -> List[int]:
        """
        Get list of validators based on stake threshold.
        
        Args:
            metagraph: Bittensor metagraph instance
            min_stake: Minimum stake to be considered a validator
            
        Returns:
            List of validator UIDs
        """
        validators = []
        for uid in range(metagraph.n):
            if metagraph.S[uid].item() >= min_stake:
                validators.append(uid)
        return validators
    
    @staticmethod
    def normalize_weights(weights: Dict[int, float]) -> Tuple[torch.Tensor, torch.Tensor]:
        """
        Normalize weights dictionary to tensors for chain submission.
        
        Args:
            weights: Dictionary mapping UID to weight
            
        Returns:
            Tuple of (uids_tensor, weights_tensor)
        """
        if not weights:
            return torch.tensor([], dtype=torch.int64), torch.tensor([], dtype=torch.float32)
            
        uids = list(weights.keys())
        raw_weights = list(weights.values())
        
        # Normalize weights to sum to 1
        total_weight = sum(raw_weights)
        if total_weight > 0:
            normalized_weights = [w / total_weight for w in raw_weights]
        else:
            normalized_weights = [1.0 / len(raw_weights) for _ in raw_weights]
            
        return (
            torch.tensor(uids, dtype=torch.int64),
            torch.tensor(normalized_weights, dtype=torch.float32)
        )
    
    @staticmethod
    def check_registration(wallet: bt.wallet, metagraph: bt.metagraph) -> Tuple[bool, int]:
        """
        Check if wallet is registered on the subnet.
        
        Args:
            wallet: Bittensor wallet instance
            metagraph: Bittensor metagraph instance
            
        Returns:
            Tuple of (is_registered, uid)
        """
        if wallet.hotkey.ss58_address in metagraph.hotkeys:
            uid = metagraph.hotkeys.index(wallet.hotkey.ss58_address)
            return True, uid
        return False, -1