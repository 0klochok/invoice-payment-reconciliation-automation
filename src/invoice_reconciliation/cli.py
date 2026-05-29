"""Command line entry point for the reconciliation demo project."""

from __future__ import annotations

import argparse

from invoice_reconciliation import __version__


def build_parser() -> argparse.ArgumentParser:
    """Build the Phase 0 CLI parser."""
    parser = argparse.ArgumentParser(
        prog="reconcile",
        description=(
            "Invoice and payment reconciliation automation. "
            "Phase 0 exposes help and version output only."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line interface."""
    parser = build_parser()
    parser.parse_args(argv)
    return 0
