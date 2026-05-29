"""Command line entry point for the reconciliation demo project."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from invoice_reconciliation import __version__
from invoice_reconciliation.ingestion import load_invoice_csv, load_payment_csv
from invoice_reconciliation.matching import match_invoices_to_payments
from invoice_reconciliation.models import ImportDiagnostics
from invoice_reconciliation.reporting import write_reconciliation_reports


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI parser."""
    parser = argparse.ArgumentParser(
        prog="reconcile",
        description=(
            "Invoice and payment reconciliation automation. "
            "Phase 3 generates local Markdown and CSV reconciliation reports "
            "from validated CSV inputs."
        ),
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    subparsers = parser.add_subparsers(dest="command")

    report_parser = subparsers.add_parser(
        "report",
        help="generate local Markdown and CSV reconciliation reports",
        description=(
            "Load invoice and payment CSV files, run deterministic matching, "
            "and write local Markdown and CSV reports."
        ),
    )
    report_parser.add_argument(
        "--invoices",
        required=True,
        type=Path,
        help="path to the invoice CSV input",
    )
    report_parser.add_argument(
        "--payments",
        required=True,
        type=Path,
        help="path to the payment CSV input",
    )
    report_parser.add_argument(
        "--out-dir",
        required=True,
        type=Path,
        help="directory for generated local report files",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line interface."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "report":
        return _run_report_command(args.invoices, args.payments, args.out_dir)
    return 0


def _run_report_command(invoices_path: Path, payments_path: Path, out_dir: Path) -> int:
    invoice_import = load_invoice_csv(invoices_path)
    payment_import = load_payment_csv(payments_path)

    if invoice_import.diagnostics.errors or payment_import.diagnostics.errors:
        _print_import_errors(invoice_import.diagnostics)
        _print_import_errors(payment_import.diagnostics)
        return 1

    result = match_invoices_to_payments(invoice_import.records, payment_import.records)
    paths = write_reconciliation_reports(result, out_dir)
    print(f"Markdown report: {paths.markdown}")
    print(f"Summary CSV: {paths.summary_csv}")
    print(f"Details CSV: {paths.details_csv}")
    return 0


def _print_import_errors(diagnostics: ImportDiagnostics) -> None:
    for error in diagnostics.errors:
        print(
            (
                f"{error.source} row {error.row_number} "
                f"{error.field} {error.error_code}: {error.message}"
            ),
            file=sys.stderr,
        )
