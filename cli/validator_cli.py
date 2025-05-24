"""CLI for validator operations."""

import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validator CLI")
    parser.add_argument(
        "--wallet.name", dest="wallet_name", default="default", help="Wallet name"
    )
    parser.add_argument(
        "--wallet.hotkey", dest="wallet_hotkey", default="default", help="Wallet hotkey"
    )
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("stats", help="Show validator statistics")
    manage = sub.add_parser("manage", help="Manage validator operations")
    manage.add_argument("action", choices=["start", "stop"], help="Action to perform")
    export = sub.add_parser("export", help="Export validator data")
    export.add_argument("path", help="Path to output JSON file")
    return parser


def run_stats(wallet: str, hotkey: str) -> None:
    """Placeholder function to display validator stats."""
    stats = {"uptime": 0, "processed": 0}
    print(f"Stats for {wallet}/{hotkey}: {stats}")


def export_data(path: str) -> None:
    """Export dummy validator data to JSON."""
    import json

    data = {"validators": []}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)
    print(f"Data exported to {path}")


def main(argv: list[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
    if args.command == "stats":
        run_stats(args.wallet_name, args.wallet_hotkey)
    elif args.command == "manage":
        print(f"{args.action.capitalize()}ing validator")
    elif args.command == "export":
        export_data(args.path)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
