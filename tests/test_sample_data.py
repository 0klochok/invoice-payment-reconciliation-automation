import csv
from pathlib import Path

from invoice_reconciliation.cli import main
from invoice_reconciliation.ingestion import load_invoice_csv, load_payment_csv
from invoice_reconciliation.matching import MatchStatus, match_invoices_to_payments
from invoice_reconciliation.reporting import build_summary_counts

SAMPLE_DATA = Path(__file__).resolve().parents[1] / "sample-data"
MIXED_INVOICES = SAMPLE_DATA / "demo-mixed-invoices.csv"
MIXED_PAYMENTS = SAMPLE_DATA / "demo-mixed-payments.csv"


def test_phase_4_sample_csv_files_are_parseable() -> None:
    invoice_import = load_invoice_csv(MIXED_INVOICES)
    payment_import = load_payment_csv(MIXED_PAYMENTS)

    assert invoice_import.diagnostics.rows_seen == 8
    assert invoice_import.diagnostics.valid_rows == 8
    assert invoice_import.diagnostics.errors == ()
    assert payment_import.diagnostics.rows_seen == 8
    assert payment_import.diagnostics.valid_rows == 8
    assert payment_import.diagnostics.errors == ()


def test_mixed_demo_sample_produces_expected_status_counts() -> None:
    invoice_import = load_invoice_csv(MIXED_INVOICES)
    payment_import = load_payment_csv(MIXED_PAYMENTS)

    result = match_invoices_to_payments(
        invoice_import.records,
        payment_import.records,
    )

    assert build_summary_counts(result) == {
        MatchStatus.MATCHED: 2,
        MatchStatus.UNMATCHED_INVOICE: 1,
        MatchStatus.UNMATCHED_PAYMENT: 1,
        MatchStatus.AMOUNT_MISMATCH: 1,
        MatchStatus.CURRENCY_MISMATCH: 1,
        MatchStatus.AMBIGUOUS_REFERENCE: 2,
    }


def test_cli_report_smoke_with_mixed_demo_sample(tmp_path: Path, capsys) -> None:
    out_dir = tmp_path / "demo-output"

    exit_code = main(
        [
            "report",
            "--invoices",
            str(MIXED_INVOICES),
            "--payments",
            str(MIXED_PAYMENTS),
            "--out-dir",
            str(out_dir),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    assert "Markdown report:" in captured.out

    summary_rows = list(
        csv.DictReader(
            (out_dir / "reconciliation-summary.csv")
            .read_text(encoding="utf-8")
            .splitlines()
        )
    )
    counts_by_status = {row["status"]: row["count"] for row in summary_rows}

    assert counts_by_status == {
        "matched": "2",
        "unmatched_invoice": "1",
        "unmatched_payment": "1",
        "amount_mismatch": "1",
        "currency_mismatch": "1",
        "ambiguous_reference": "2",
    }


def test_cli_report_writes_only_inside_requested_output_directory(
    tmp_path: Path,
    capsys,
) -> None:
    out_dir = tmp_path / "contained-output"

    exit_code = main(
        [
            "report",
            "--invoices",
            str(MIXED_INVOICES),
            "--payments",
            str(MIXED_PAYMENTS),
            "--out-dir",
            str(out_dir),
        ]
    )

    capsys.readouterr()
    assert exit_code == 0
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    ) == [
        "contained-output",
        "contained-output/reconciliation-details.csv",
        "contained-output/reconciliation-report.md",
        "contained-output/reconciliation-summary.csv",
    ]
