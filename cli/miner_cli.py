"""CLI for miner operations."""

import argparse

try:
    import bittensor as bt
except Exception:  # pragma: no cover - optional dependency
    bt = None


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Miner CLI")
    parser.add_argument("--wallet.name", dest="wallet_name", default="default", help="Wallet name")
    parser.add_argument("--wallet.hotkey", dest="wallet_hotkey", default="default", help="Wallet hotkey")
    sub = parser.add_subparsers(dest="command")
    submit = sub.add_parser("submit", help="Submit video")
    submit.add_argument("file", help="Path to video file")
    sub.add_parser("status", help="Check miner status")
    sub.add_parser("config", help="Show configuration")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
    if bt:
        wallet = bt.wallet(name=args.wallet_name, hotkey=args.wallet_hotkey)
        print(f"Using wallet {wallet.name} with hotkey {wallet.hotkey.ss58_address}")
    else:
        print(f"Wallet: {args.wallet_name}/{args.wallet_hotkey}")
    if args.command == "submit":
        print(f"Submitting {args.file}")
    elif args.command == "status":
        print("Miner running")
    elif args.command == "config":
        print("Showing config")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

