# The MIT License (MIT)
# Copyright © 2024 Your Organization

import time
import typing
import bittensor as bt
from template.protocol import QuerySynapse, DataSynapse

class Miner:
    """
    Basic miner class for Subnet 89.
    This miner responds to queries from validators.
    """
    
    def __init__(self, config=None):
        self.config = config or self.get_config()
        self.setup_logging()
        self.setup_bittensor()
        self.setup_axon()
        
    def get_config(self):
        """Setup configuration for the miner."""
        parser = bt.ArgumentParser()
        parser.add_argument('--netuid', type=int, default=89, help='Subnet netuid')
        parser.add_argument('--logging.debug', action='store_true', help='Enable debug logging')
        parser.add_argument('--logging.trace', action='store_true', help='Enable trace logging')
        parser.add_argument('--axon.port', type=int, default=None, help='Port for the axon server')
        
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
        
    def run(self):
        """Main loop for the miner."""
        bt.logging.info("Starting miner...")
        
        # Start the axon server
        self.axon.start()
        
        bt.logging.info(f"Miner running on network: {self.subtensor.chain_endpoint}")
        bt.logging.info(f"Miner serving on: {self.axon.ip}:{self.axon.port}")
        
        # Main loop
        step = 0
        while True:
            try:
                # Check registration
                if step % 5 == 0:
                    self.metagraph.sync(subtensor=self.subtensor)
                    
                    if self.wallet.hotkey.ss58_address in self.metagraph.hotkeys:
                        my_uid = self.metagraph.hotkeys.index(self.wallet.hotkey.ss58_address)
                        bt.logging.info(f"Miner running with UID: {my_uid}")
                    else:
                        bt.logging.warning("Miner not registered on network")
                        
                # TODO: Add any periodic tasks here
                
                step += 1
                time.sleep(12)  # Sleep for one block
                
            except KeyboardInterrupt:
                bt.logging.info("Miner interrupted by user")
                break
            except Exception as e:
                bt.logging.error(f"Error in main loop: {e}")
                
        # Clean up
        self.axon.stop()
        bt.logging.info("Miner stopped")

if __name__ == "__main__":
    miner = Miner()
    miner.run()