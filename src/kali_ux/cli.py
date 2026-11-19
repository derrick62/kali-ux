"""Minimal CLI for the Kali UX foundation."""

from __future__ import annotations

import argparse

from kali_ux import __version__


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="kali-ux",
        description="Kali UX desktop enhancement suite.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    build_parser().parse_args(argv)
    print("Kali UX foundation is installed; desktop features are not yet wired.")
    return 0
