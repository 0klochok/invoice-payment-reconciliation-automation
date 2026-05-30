from pathlib import Path

from invoice_reconciliation import __version__
from invoice_reconciliation.cli import main

SAMPLE_DATA = Path(__file__).resolve().parents[1] / "sample-data"


def test_package_import_exposes_version() -> None:
    assert __version__ == "0.1.0"


def test_cli_help_smoke(capsys) -> None:
    try:
        main(["--help"])
    except SystemExit as exc:
        assert exc.code == 0

    captured = capsys.readouterr()
    normalized_output = " ".join(captured.out.split())
    assert "Invoice and payment reconciliation automation" in captured.out
    assert (
        "Generates local Markdown and CSV reconciliation reports" in normalized_output
    )
    assert "--version" in captured.out
    assert "report" in captured.out


def test_cli_report_smoke_writes_reports(tmp_path: Path, capsys) -> None:
    out_dir = tmp_path / "reports"

    exit_code = main(
        [
            "report",
            "--invoices",
            str(SAMPLE_DATA / "valid-invoices.csv"),
            "--payments",
            str(SAMPLE_DATA / "valid-payments.csv"),
            "--out-dir",
            str(out_dir),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.err == ""
    assert "Markdown report:" in captured.out
    assert (out_dir / "reconciliation-report.md").exists()
    assert (out_dir / "reconciliation-summary.csv").exists()
    assert (out_dir / "reconciliation-details.csv").exists()
    assert "| Matched | 3 |" in (out_dir / "reconciliation-report.md").read_text(
        encoding="utf-8"
    )
