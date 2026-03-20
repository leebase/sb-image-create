"""
Main entry point for sb-image-create.

Created on 2026-03-20 by Lee Harrington.
"""

import argparse


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="sb-image-create",
        description="sb-image-create - AI-agent project",
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name to greet (default: World)",
    )

    args = parser.parse_args()
    print(f"Hello from sb-image-create, {args.name}!")


if __name__ == "__main__":
    main()
