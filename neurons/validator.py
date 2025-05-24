# The MIT License (MIT)
# Copyright © 2024 Your Organization

import time
import torch
import asyncio
import random
import bittensor as bt
from typing import List, Dict
from template.protocol import QuerySynapse, DataSynapse

class Validator:
    """
    Basic validator class for Subnet 89.
    This validator queries miners and sets weights based on their responses.
    """
    
    def __init__(self, config=None):
        self.config = config or self.get_config()
        self.setup_logging()
        self.setup_bittensor()
        self.scores = {}
        
    def get_config(self):
        """Setup configuration for the validator."""
        parser = bt.ArgumentParser()
        parser.add_argument('--netuid', type=int, default=89, help='Subnet netuid')
        parser.add_argument('--logging.debug', action='store_true', help='Enable debug logging')
        parser.add_argument('--logging.trace', action='store_true', help='Enable trace logging')
        parser.add_argument('--query_timeout', type=int, default=10, help='Query timeout in seconds')
        
        bt.subtensor.add_args(parser)
        bt.logging.add_args(parser)
        bt.wallet.add_args(parser)
        
        config = bt.config(parser)
        return config
        
    def setup_logging(self):
        """Initialize logging."""
        bt.logging(config=self.config, logging_dir=self.config.full_path)
        bt.logging.info(f"Running validator on subnet: {self.config.netuid}")
        
    def setup_bittensor(self):
        """Setup wallet, subtensor, and metagraph."""
        self.wallet = bt.wallet(config=self.config)
        self.subtensor = bt.subtensor(config=self.config)
        self.metagraph = self.subtensor.metagraph(self.config.netuid)
        self.dendrite = bt.dendrite(wallet=self.wallet)
        
        # Initialize scores for all miners
        for uid in range(len(self.metagraph.uids)):
            self.scores[uid] = 0.0
            
    async def query_miners(self, axons: List[bt.axon]) -> List[QuerySynapse]:
        """Query a list of miners with a test query."""
        # Create a sample query
        synapse = QuerySynapse(
            query="test_query_" + str(int(time.time()))
        )
        
        # Query all miners
        responses = await self.dendrite(
            axons=axons,
            synapse=synapse,
            timeout=self.config.query_timeout
        )
        
        return responses
        
    async def send_data_to_miners(self, axons: List[bt.axon]) -> List[DataSynapse]:
        """Send data to miners for processing."""
        # Create sample data
        synapse = DataSynapse(
            data=[
                {"id": i, "value": random.random()} 
                for i in range(10)
            ],
            metadata={"timestamp": time.time()}
        )
        
        # Send to all miners
        responses = await self.dendrite(
            axons=axons,
            synapse=synapse,
            timeout=self.config.query_timeout
        )
        
        return responses
        
    def score_responses(self, responses: List[QuerySynapse], uids: List[int]):
        """Score miner responses and update scores."""
        for response, uid in zip(responses, uids):
            try:
                if response.successfully_processed:
                    # TODO: Implement your scoring logic here
                    # This is a simple example that gives points for successful responses
                    score = 1.0
                    
                    # Update running average
                    self.scores[uid] = 0.9 * self.scores[uid] + 0.1 * score
                    bt.logging.debug(f"UID {uid} scored {score}, avg: {self.scores[uid]}")
                else:
                    # Penalize failed responses
                    self.scores[uid] = 0.9 * self.scores[uid]
                    bt.logging.debug(f"UID {uid} failed, avg: {self.scores[uid]}")
                    
            except Exception as e:
                bt.logging.error(f"Error scoring UID {uid}: {e}")
                self.scores[uid] = 0.9 * self.scores[uid]
                
    def set_weights(self):
        """Set weights on the blockchain based on miner scores."""
        try:
            # Get all UIDs and their scores
            uids = list(self.scores.keys())
            scores = list(self.scores.values())
            
            # Normalize scores
            if sum(scores) > 0:
                weights = [score / sum(scores) for score in scores]
            else:
                weights = [1.0 / len(scores) for _ in scores]
                
            # Convert to tensors
            uids_tensor = torch.tensor(uids, dtype=torch.int64)
            weights_tensor = torch.tensor(weights, dtype=torch.float32)
            
            # Set weights on chain
            success = self.subtensor.set_weights(
                netuid=self.config.netuid,
                wallet=self.wallet,
                uids=uids_tensor,
                weights=weights_tensor,
                wait_for_inclusion=False
            )
            
            if success:
                bt.logging.info("Successfully set weights on chain")
            else:
                bt.logging.error("Failed to set weights on chain")
                
        except Exception as e:
            bt.logging.error(f"Error setting weights: {e}")
            
    async def run_validation_loop(self):
        """Main validation loop."""
        step = 0
        while True:
            try:
                # Sync metagraph periodically
                if step % 5 == 0:
                    self.metagraph.sync(subtensor=self.subtensor)
                    bt.logging.info(f"Metagraph synced, n_miners: {self.metagraph.n}")
                    
                # Get active miners
                active_miners = []
                active_uids = []
                for uid, axon in enumerate(self.metagraph.axons):
                    if axon.ip != "0.0.0.0":
                        active_miners.append(axon)
                        active_uids.append(uid)
                        
                if len(active_miners) > 0:
                    bt.logging.info(f"Querying {len(active_miners)} active miners")
                    
                    # Query miners
                    responses = await self.query_miners(active_miners)
                    
                    # Score responses
                    self.score_responses(responses, active_uids)
                    
                    # Set weights periodically
                    if step % 100 == 0:
                        self.set_weights()
                else:
                    bt.logging.warning("No active miners found")
                    
                step += 1
                await asyncio.sleep(12)  # Sleep for one block
                
            except KeyboardInterrupt:
                bt.logging.info("Validator interrupted by user")
                break
            except Exception as e:
                bt.logging.error(f"Error in validation loop: {e}")
                await asyncio.sleep(12)
                
    def run(self):
        """Main entry point for the validator."""
        bt.logging.info("Starting validator...")
        
        # Check wallet registration
        if self.wallet.hotkey.ss58_address not in self.metagraph.hotkeys:
            bt.logging.error("Validator wallet not registered on subnet")
            return
            
        my_uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)
        bt.logging.info(f"Validator running with UID: {my_uid}")
        
        # Run the async validation loop
        asyncio.run(self.run_validation_loop())

if __name__ == "__main__":
    validator = Validator()
    validator.run()