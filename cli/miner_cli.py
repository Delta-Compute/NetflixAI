"""CLI for miner operations."""

import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Miner CLI")
    sub = parser.add_subparsers(dest="command")
    submit = sub.add_parser("submit", help="Submit video")
    submit.add_argument("file", help="Path to video file")
    sub.add_parser("status", help="Check miner status")
    sub.add_parser("config", help="Show configuration")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
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

