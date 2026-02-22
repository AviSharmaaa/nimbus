#!/usr/bin/env python3
"""
╔══════════════════════════════════════╗
║   Nimbus — ASCII Weather App         ║
║   Animated terminal weather viewer   ║
╚══════════════════════════════════════╝

Usage:
    python -m nimbus                      # auto-detect location
    python -m nimbus "London"             # specific city
    python -m nimbus "New York"
    python -m nimbus --demo rain          # offline demo
    python -m nimbus --demo snow/sun/cloud/thunder/fog
"""

import curses
import sys
import time
import argparse

from app import run
from weather import REQUESTS_OK


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="python -m nimbus",
        description="Nimbus — Animated ASCII weather in your terminal",
    )
    parser.add_argument(
        "city", nargs="?", default=None,
        help="City name (e.g. 'London', 'Bengaluru'). Omit to auto-detect.",
    )
    parser.add_argument(
        "--demo",
        choices=["sun", "rain", "snow", "cloud", "thunder", "fog"],
        default=None,
        help="Run in demo mode (no internet needed)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    # Prompt the user if requests isn't installed and no demo mode was chosen
    if not REQUESTS_OK and not args.demo:
        print("Note: the 'requests' library is not installed.")
        print("      Install it with:  pip install requests")
        print("      Or run offline:   python -m nimbus --demo rain")
        print()
        choice = input("Run in demo (sun) mode instead? [Y/n]: ").strip().lower()
        if choice in ("", "y", "yes"):
            args.demo = "sun"
        else:
            sys.exit(1)

    print("Starting Nimbus…")
    print("Controls:  R = refresh weather   Q = quit")
    print()
    time.sleep(0.4)

    try:
        curses.wrapper(run, args.city, args.demo)
    except KeyboardInterrupt:
        pass

    print("\nThanks for using Nimbus! 🌤")


if __name__ == "__main__":
    main()
