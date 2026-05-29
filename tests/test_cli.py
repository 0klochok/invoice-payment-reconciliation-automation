from invoice_reconciliation import __version__
from invoice_reconciliation.cli import main


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
    assert "Phase 2 adds local CSV ingestion and deterministic matching APIs" in (
        normalized_output
    )
    assert "--version" in captured.out
