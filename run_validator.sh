#!/bin/bash
# Script to run the validator with common configurations

# Default values
WALLET_NAME="${WALLET_NAME:-default}"
WALLET_HOTKEY="${WALLET_HOTKEY:-default}"
NETUID="${NETUID:-89}"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --wallet.name)
            WALLET_NAME="$2"
            shift 2
            ;;
        --wallet.hotkey)
            WALLET_HOTKEY="$2"
            shift 2
            ;;
        --netuid)
            NETUID="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo "Starting Subnet 89 Validator..."
echo "Wallet: $WALLET_NAME"
echo "Hotkey: $WALLET_HOTKEY"
echo "Netuid: $NETUID"

python neurons/validator.py \
    --wallet.name "$WALLET_NAME" \
    --wallet.hotkey "$WALLET_HOTKEY" \
    --netuid "$NETUID" \
    --logging.debug