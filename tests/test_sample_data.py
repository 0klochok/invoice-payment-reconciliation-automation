import csv
from pathlib import Path

from invoice_reconciliation.cli import main
from invoice_reconciliation.ingestion import (
    load_invoice_csv,
    load_invoice_xlsx,
    load_payment_csv,
    load_payment_xlsx,
)
from invoice_reconciliation.matching import MatchStatus, match_invoices_to_payments
from invoice_reconciliation.reporting import build_summary_counts

SAMPLE_DATA = Path(__file__).resolve().parents[1] / "sample-data"
MIXED_INVOICES = SAMPLE_DATA / "demo-mixed-invoices.csv"
MIXED_PAYMENTS = SAMPLE_DATA / "demo-mixed-payments.csv"
MIXED_INVOICES_XLSX = SAMPLE_DATA / "demo-mixed-invoices.xlsx"
MIXED_PAYMENTS_XLSX = SAMPLE_DATA / "demo-mixed-payments.xlsx"
EXPECTED_MIXED_COUNTS = {
    MatchStatus.MATCHED: 2,
    MatchStatus.UNMATCHED_INVOICE: 1,
    MatchStatus.UNMATCHED_PAYMENT: 1,
    MatchStatus.AMOUNT_MISMATCH: 1,
    MatchStatus.CURRENCY_MISMATCH: 1,
    MatchStatus.AMBIGUOUS_REFERENCE: 2,
}
EXPECTED_MIXED_CSV_COUNTS = {
    status.value: str(count) for status, count in EXPECTED_MIXED_COUNTS.items()
}


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
    assert _summary_counts_for(MIXED_INVOICES, MIXED_PAYMENTS) == EXPECTED_MIXED_COUNTS


def test_phase_5_sample_xlsx_invoice_file_is_parseable() -> None:
    invoice_import = load_invoice_xlsx(MIXED_INVOICES_XLSX)

    assert invoice_import.diagnostics.rows_seen == 8
    assert invoice_import.diagnostics.valid_rows == 8
    assert invoice_import.diagnostics.errors == ()
    assert invoice_import.records[0].invoice_id == "INV-2001"
    assert invoice_import.records[0].source_row == 2


def test_phase_5_sample_xlsx_payment_file_is_parseable() -> None:
    payment_import = load_payment_xlsx(MIXED_PAYMENTS_XLSX)

    assert payment_import.diagnostics.rows_seen == 8
    assert payment_import.diagnostics.valid_rows == 8
    assert payment_import.diagnostics.errors == ()
    assert payment_import.records[0].payment_id == "PAY-7001"
    assert payment_import.records[0].source_row == 2


def test_xlsx_mixed_demo_sample_produces_expected_status_counts() -> None:
    assert (
        _summary_counts_for(MIXED_INVOICES_XLSX, MIXED_PAYMENTS_XLSX)
        == EXPECTED_MIXED_COUNTS
    )


def test_csv_and_xlsx_mixed_demo_inputs_produce_equivalent_status_counts() -> None:
    assert _summary_counts_for(MIXED_INVOICES, MIXED_PAYMENTS) == _summary_counts_for(
        MIXED_INVOICES_XLSX,
        MIXED_PAYMENTS_XLSX,
    )


def test_csv_and_xlsx_mixed_demo_inputs_produce_equivalent_records() -> None:
    assert (
        load_invoice_csv(MIXED_INVOICES).records
        == load_invoice_xlsx(MIXED_INVOICES_XLSX).records
    )
    assert (
        load_payment_csv(MIXED_PAYMENTS).records
        == load_payment_xlsx(MIXED_PAYMENTS_XLSX).records
    )


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
    assert "Report files written:" in captured.out
    assert "- Markdown:" in captured.out

    summary_rows = list(
        csv.DictReader(
            (out_dir / "reconciliation-summary.csv")
            .read_text(encoding="utf-8")
            .splitlines()
        )
    )
    counts_by_status = {row["status"]: row["count"] for row in summary_rows}

    assert counts_by_status == EXPECTED_MIXED_CSV_COUNTS


def test_cli_report_smoke_with_xlsx_mixed_demo_sample(
    tmp_path: Path,
    capsys,
) -> None:
    out_dir = tmp_path / "xlsx-demo-output"

    exit_code = main(
        [
            "report",
            "--invoices",
            str(MIXED_INVOICES_XLSX),
            "--payments",
            str(MIXED_PAYMENTS_XLSX),
            "--out-dir",
            str(out_dir),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    assert "Report files written:" in captured.out
    assert "- Markdown:" in captured.out

    summary_rows = list(
        csv.DictReader(
            (out_dir / "reconciliation-summary.csv")
            .read_text(encoding="utf-8")
            .splitlines()
        )
    )
    counts_by_status = {row["status"]: row["count"] for row in summary_rows}

    assert counts_by_status == EXPECTED_MIXED_CSV_COUNTS


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


def test_cli_report_with_xlsx_inputs_writes_only_inside_requested_output_directory(
    tmp_path: Path,
    capsys,
) -> None:
    out_dir = tmp_path / "contained-xlsx-output"

    exit_code = main(
        [
            "report",
            "--invoices",
            str(MIXED_INVOICES_XLSX),
            "--payments",
            str(MIXED_PAYMENTS_XLSX),
            "--out-dir",
            str(out_dir),
        ]
    )

    capsys.readouterr()
    assert exit_code == 0
    assert sorted(
        path.relative_to(tmp_path).as_posix() for path in tmp_path.rglob("*")
    ) == [
        "contained-xlsx-output",
        "contained-xlsx-output/reconciliation-details.csv",
        "contained-xlsx-output/reconciliation-report.md",
        "contained-xlsx-output/reconciliation-summary.csv",
    ]


def _summary_counts_for(
    invoices_path: Path,
    payments_path: Path,
) -> dict[MatchStatus, int]:
    if invoices_path.suffix == ".xlsx":
        invoice_import = load_invoice_xlsx(invoices_path)
    else:
        invoice_import = load_invoice_csv(invoices_path)

    if payments_path.suffix == ".xlsx":
        payment_import = load_payment_xlsx(payments_path)
    else:
        payment_import = load_payment_csv(payments_path)

    result = match_invoices_to_payments(
        invoice_import.records,
        payment_import.records,
    )
    return build_summary_counts(result)
