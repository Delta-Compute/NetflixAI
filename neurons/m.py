# The MIT License (MIT)
# Copyright © 2024 Your Organization

import time
import typing
import asyncio
from collections import deque
import bittensor as bt
import argparse
from template.protocol import QuerySynapse, DataSynapse
from utils.ipfs_client import IPFSClient
from utils.video_processor import VideoProcessor
from utils.storage_manager import StorageManager

class Miner:
    """
    Basic miner class for Subnet 369.
    This miner responds to queries from validators.
    """

    def __init__(self, config=None):
        self.config = config or self.get_config()
        self.setup_logging()
        self.setup_bittensor()
        self.setup_axon()

        # IPFS client and helpers
        # print(f"config => {self.config}")
        gateway = getattr(self.config, "ipfs_gateway", "http://localhost:5001")
        # print(f"gateway => {gateway}")
        self.ipfs = IPFSClient(gateway)
        self.video_processor = VideoProcessor()
        self.storage = StorageManager("miner_storage")

        # Submission handling
        self.submission_queue: asyncio.Queue[str] = asyncio.Queue()
        self.submissions: dict[str, dict] = {}
        self.recent_hashes: set[str] = set()
        self.last_submission_time = 0.0
        
    def get_config(self):
        """Setup configuration for the miner."""
        # parser = bt.ArgumentParser()
        parser = argparse.ArgumentParser()
        parser.add_argument('--netuid', type=int, default=369, help='Subnet netuid')
        parser.add_argument('--logging.debug', action='store_true', help='Enable debug logging')
        parser.add_argument('--logging.trace', action='store_true', help='Enable trace logging')
        parser.add_argument('--axon.port', type=int, default=8098, help='Port for the axon server')
        parser.add_argument('--ipfs_gateway', type=str, default='http://localhost:5001', help='IPFS gateway endpoint')
        parser.add_argument('--subtensor.chain_endpoint ', type=str, default='ws://127.0.0.1:9945', help='Subtensor chain endpoint')
        
        bt.subtensor.add_args(parser)
        bt.logging.add_args(parser)
        bt.wallet.add_args(parser)
        bt.axon.add_args(parser)
        
        config = bt.config(parser)
        return config
        
    def setup_logging(self):
        """Initialize logging."""
        bt.logging(config=self.config, logging_dir=self.config.full_path)
        bt.logging.info(f"Running miner on subnet: {self.config.netuid}")

        
    def setup_bittensor(self):
        """Setup wallet, subtensor, and metagraph."""
        self.wallet = bt.wallet(config=self.config)
        self.subtensor = bt.subtensor(config=self.config)
        self.metagraph = self.subtensor.metagraph(self.config.netuid)
        #print(f"metagraph => {self.metagraph.hotkeys}")
        
    def setup_axon(self):
        """Setup the axon server with request handlers."""
        self.axon = bt.axon(wallet=self.wallet, config=self.config)
        
        # Attach handlers for different synapse types
        self.axon.attach(
            forward_fn=self.handle_query,
            blacklist_fn=self.blacklist_query,
            priority_fn=self.priority_query
        ).attach(
            forward_fn=self.handle_data,
            blacklist_fn=self.blacklist_data,
            priority_fn=self.priority_data
        )
        
    async def handle_query(self, synapse: QuerySynapse) -> QuerySynapse:
        """Handle incoming query requests from validators."""
        try:
            # TODO: Implement your query processing logic here
            bt.logging.info(f"Received query: {synapse.query}")
            
            # Example response
            synapse.response = {
                "status": "success",
                "result": f"Processed query: {synapse.query}",
                "timestamp": time.time()
            }
            synapse.successfully_processed = True
            
        except Exception as e:
            bt.logging.error(f"Error handling query: {e}")
            synapse.error_message = str(e)
            synapse.successfully_processed = False
            
        return synapse
        
    async def handle_data(self, synapse: DataSynapse) -> DataSynapse:
        """Handle incoming data requests from validators."""
        try:
            # TODO: Implement your data processing logic here
            bt.logging.info(f"Received data request with {len(synapse.data)} items")
            
            synapse.successfully_processed = True
            
        except Exception as e:
            bt.logging.error(f"Error handling data: {e}")
            synapse.error_message = str(e)
            synapse.successfully_processed = False
            
        return synapse
        
    async def blacklist_query(self, synapse: QuerySynapse) -> typing.Tuple[bool, str]:
        """Determine if a query request should be blacklisted."""
        # TODO: Implement your blacklisting logic
        # For now, accept all requests
        return False, ""
        
    async def blacklist_data(self, synapse: DataSynapse) -> typing.Tuple[bool, str]:
        """Determine if a data request should be blacklisted."""
        # TODO: Implement your blacklisting logic
        # For now, accept all requests
        return False, ""
        
    async def priority_query(self, synapse: QuerySynapse) -> float:
        """Determine the priority of a query request."""
        # TODO: Implement your priority logic
        # For now, all requests have the same priority
        return 0.0
        
    async def priority_data(self, synapse: DataSynapse) -> float:
        """Determine the priority of a data request."""
        # TODO: Implement your priority logic
        # For now, all requests have the same priority
        return 0.0

    async def handle_video_submission(self, file_path: str) -> str:
        """Validate, upload, and track a video submission."""
        if time.time() - self.last_submission_time < 1:
            raise RuntimeError("Rate limit exceeded")

        if not self.video_processor.validate_video_file(
            file_path, 1024 * 1024 * 1024, ["mp4", "mov", "mkv"]
        ):
            raise ValueError("Invalid video")

        file_hash = self.video_processor.calculate_hash(file_path)
        if file_hash in self.recent_hashes:
            raise ValueError("Duplicate submission")

        ipfs_hash = self.ipfs.upload_file(file_path)
        self.recent_hashes.add(file_hash)
        self.submissions[ipfs_hash] = {"status": "uploaded", "time": time.time()}
        self.last_submission_time = time.time()
        return ipfs_hash

    async def handle_validation_request(self, synapse: DataSynapse) -> DataSynapse:
        """Respond to validation status queries."""
        try:
            ipfs_hash = synapse.data.get("ipfs_hash")
            status = self.submissions.get(ipfs_hash, {}).get("status", "unknown")
            synapse.response = {"status": status}
            synapse.successfully_processed = True
        except Exception as e:
            synapse.error_message = str(e)
            synapse.successfully_processed = False
        return synapse

    def cleanup_submissions(self, max_age: float = 3600) -> None:
        """Remove old tracked submissions."""
        cutoff = time.time() - max_age
        for key in list(self.submissions.keys()):
            if self.submissions[key]["time"] < cutoff:
                self.submissions.pop(key, None)
        
    async def run_loop(self):
        """Main loop for the miner."""
        bt.logging.info("Starting miner...")
        print(f"Starting miner...")
        # Start the axon server
        self.axon.start()
        print(f"Starting axon...")

        bt.logging.info(f"Miner running on network: {self.subtensor.chain_endpoint}")
        bt.logging.info(f"Miner serving on: {self.axon.ip}:{self.axon.port}")

        # Main loop
        step = 0
        while True:
            try:
                # Check registration
                if step % 5 == 0:
                    self.metagraph.sync(subtensor=self.subtensor)
                    print(f"metagraph")

                    if self.wallet.hotkey.ss58_address in self.metagraph.hotkeys:
                        my_uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)
                        bt.logging.info(f"Miner running with UID: {my_uid}")
                    else:
                        bt.logging.warning("Miner not registered on network")

                # Process queued submissions
                if not self.submission_queue.empty():
                    file_path = await self.submission_queue.get()
                    try:
                        await self.handle_video_submission(file_path)
                    except Exception as e:
                        bt.logging.error(f"Submission error: {e}")

                # Periodic cleanup
                if step % 100 == 0:
                    self.cleanup_submissions()

                step += 1
                await asyncio.sleep(12)

            except KeyboardInterrupt:
                bt.logging.info("Miner interrupted by user")
                break
            except Exception as e:
                bt.logging.error(f"Error in main loop: {e}")
                
        # Clean up

        self.axon.stop()
        bt.logging.info("Miner stopped")

    def run(self):
        asyncio.run(self.run_loop())   

if __name__ == "__main__":
    miner = Miner()
    miner.run()
