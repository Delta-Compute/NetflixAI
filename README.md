# Subnet 89

A Bittensor subnet template for building decentralized applications.

## Overview

This is a basic template for Subnet 89 on the Bittensor network. It includes the essential components needed to build and deploy miners and validators.

## Structure

```
Subnet89/
├── neurons/          # Miner and validator implementations
├── template/         # Protocol definitions (synapses)
├── config/           # Configuration management
├── utils/            # Utility functions
├── requirements.txt  # Python dependencies
└── setup.py         # Package setup
```

## Quick Start

### Installation

```bash
cd Subnet89
pip install -e .
```

### Running a Miner

```bash
python neurons/miner.py --wallet.name <your-wallet> --wallet.hotkey <your-hotkey>
```

### Running a Validator

```bash
python neurons/validator.py --wallet.name <your-wallet> --wallet.hotkey <your-hotkey>
```

## Development

This template provides the basic structure for a Bittensor subnet. You'll need to:

1. **Define your protocol**: Modify `template/protocol.py` to define the synapses (communication protocol) for your subnet
2. **Implement miner logic**: Update `neurons/miner.py` with your miner's response logic
3. **Implement validator logic**: Update `neurons/validator.py` with your validation and scoring logic
4. **Configure parameters**: Adjust settings in `config/config.py`

## Key Components

### Protocol (Synapses)
- `QuerySynapse`: Basic query/response pattern
- `DataSynapse`: Data exchange pattern

### Miner
- Responds to validator queries
- Implements your subnet's core functionality

### Validator
- Queries miners
- Scores responses
- Sets weights on-chain

## Network Configuration

By default, this subnet uses:
- Network ID: 89
- Network: finney (mainnet)

To use testnet:
```bash
export BT_NETWORK=test
```

## License

MIT License - see LICENSE file for details