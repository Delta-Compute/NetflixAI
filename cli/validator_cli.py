"""CLI for validator operations."""

import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validator CLI")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("stats", help="Show validator stats")
    sub.add_parser("manage", help="Manage validator")
    sub.add_parser("export", help="Export data")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = create_parser()
    args = parser.parse_args(argv)
    if args.command == "stats":
        print("Showing validator stats")
    elif args.command == "manage":
        print("Managing validator")
    elif args.command == "export":
        print("Exporting data")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
