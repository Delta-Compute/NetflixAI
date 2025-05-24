# Subnet 89

An AI-driven video streaming platform built on Bittensor.

This repository contains both the Subnet 89 implementation and the user-facing
application, including miners, validators, and an API server.

## Overview

Subnet 89 includes the miner, validator, and API code needed to run the decentralized video streaming platform. The project is ready for customization and deployment.

## Structure

```
NetflixAI/
├── neurons/          # Miner and validator implementations
├── template/         # Protocol definitions (synapses)
├── config/           # Configuration management
├── utils/            # Helper modules and API server
├── requirements.txt  # Python dependencies
└── setup.py         # Package setup
```

## Quick Start

### Installation

```bash
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

Key files for customization:

- `template/protocol.py` – define the communication protocol
- `neurons/miner.py` – miner logic
- `neurons/validator.py` – validator logic
- `config/config.py` – runtime configuration

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

## Running the API Server

The project includes a lightweight FastAPI server for simple file submissions.
You can start it with `uvicorn`:

```bash
uvicorn utils.api_server:app --reload
```

The server exposes the following endpoints:

- `POST /submit` – upload a video file
- `GET /status` – service status
- `GET /metrics` – basic metrics
- `GET /health` – health check

## License

MIT License - see LICENSE file for details
