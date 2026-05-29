from datetime import date
from decimal import Decimal
from pathlib import Path

from invoice_reconciliation.ingestion import load_invoice_csv, load_payment_csv

SAMPLE_DATA = Path(__file__).resolve().parents[1] / "sample-data"


def test_valid_invoice_csv_ingestion() -> None:
    result = load_invoice_csv(SAMPLE_DATA / "valid-invoices.csv")

    assert result.diagnostics.rows_seen == 3
    assert result.diagnostics.valid_rows == 3
    assert result.diagnostics.invalid_rows == 0
    assert result.diagnostics.errors == ()

    first = result.records[0]
    assert first.invoice_id == "INV-1001"
    assert first.customer_name == "Acme Supplies"
    assert first.invoice_date == date(2026, 1, 3)
    assert first.due_date == date(2026, 2, 2)
    assert first.invoice_amount.value == Decimal("1200.00")
    assert first.invoice_amount.currency == "USD"
    assert first.source_row == 2

    assert [record.invoice_amount.currency for record in result.records] == [
        "USD",
        "EUR",
        "USD",
    ]


def test_valid_payment_csv_ingestion() -> None:
    result = load_payment_csv(SAMPLE_DATA / "valid-payments.csv")

    assert result.diagnostics.rows_seen == 3
    assert result.diagnostics.valid_rows == 3
    assert result.diagnostics.invalid_rows == 0
    assert result.diagnostics.errors == ()

    first = result.records[0]
    assert first.payment_id == "PAY-5001"
    assert first.customer_name == "Acme Supplies"
    assert first.payment_date == date(2026, 1, 20)
    assert first.payment_amount.value == Decimal("1200.00")
    assert first.payment_amount.currency == "USD"
    assert first.payment_reference == "INV-1001"
    assert first.source_row == 2

    assert [record.payment_amount.currency for record in result.records] == [
        "USD",
        "EUR",
        "USD",
    ]


def test_missing_required_fields_are_reported(tmp_path: Path) -> None:
    csv_path = tmp_path / "payments.csv"
    csv_path.write_text(
        "\n".join(
            [
                "payment_id,customer_name,payment_date,payment_amount,currency,"
                "payment_reference",
                "PAY-9001,Acme Supplies,2026-01-20,1200.00,USD,",
            ]
        ),
        encoding="utf-8",
    )

    result = load_payment_csv(csv_path)

    assert result.records == ()
    assert [error.to_dict() for error in result.diagnostics.errors] == [
        {
            "source": "payments",
            "row_number": 2,
            "field": "payment_reference",
            "error_code": "missing_required",
            "message": "Missing required value.",
        }
    ]


def test_invalid_date_format_is_reported(tmp_path: Path) -> None:
    csv_path = tmp_path / "invoices.csv"
    csv_path.write_text(
        "\n".join(
            [
                "invoice_id,customer_name,invoice_date,due_date,invoice_amount,currency",
                "INV-9001,Acme Supplies,01/03/2026,2026-02-02,1200.00,USD",
            ]
        ),
        encoding="utf-8",
    )

    result = load_invoice_csv(csv_path)

    assert result.records == ()
    assert [error.to_dict() for error in result.diagnostics.errors] == [
        {
            "source": "invoices",
            "row_number": 2,
            "field": "invoice_date",
            "error_code": "invalid_date",
            "message": "Expected ISO date in YYYY-MM-DD format.",
        }
    ]


def test_invalid_amount_format_is_reported(tmp_path: Path) -> None:
    csv_path = tmp_path / "payments.csv"
    csv_path.write_text(
        "\n".join(
            [
                "payment_id,customer_name,payment_date,payment_amount,currency,"
                "payment_reference",
                "PAY-9001,Acme Supplies,2026-01-20,twelve,USD,INV-9001",
            ]
        ),
        encoding="utf-8",
    )

    result = load_payment_csv(csv_path)

    assert result.records == ()
    assert [error.to_dict() for error in result.diagnostics.errors] == [
        {
            "source": "payments",
            "row_number": 2,
            "field": "payment_amount",
            "error_code": "invalid_amount",
            "message": "Expected decimal money amount.",
        }
    ]


def test_whitespace_and_currency_are_normalized(tmp_path: Path) -> None:
    csv_path = tmp_path / "invoices.csv"
    csv_path.write_text(
        "\n".join(
            [
                "invoice_id,customer_name,invoice_date,due_date,invoice_amount,currency",
                " INV-9001 ,  Acme Supplies  , 2026-01-03 , 2026-02-02 , "
                "1200.00 , usd ",
            ]
        ),
        encoding="utf-8",
    )

    result = load_invoice_csv(csv_path)

    assert result.diagnostics.errors == ()
    invoice = result.records[0]
    assert invoice.invoice_id == "INV-9001"
    assert invoice.customer_name == "Acme Supplies"
    assert invoice.invoice_amount.value == Decimal("1200.00")
    assert invoice.invoice_amount.currency == "USD"


def test_validation_error_output_is_deterministic(tmp_path: Path) -> None:
    csv_path = tmp_path / "invoices.csv"
    csv_path.write_text(
        "\n".join(
            [
                "invoice_id,customer_name,invoice_date,due_date,invoice_amount,currency",
                " , ,bad-date,2026-02-30,not-money, ",
            ]
        ),
        encoding="utf-8",
    )

    result = load_invoice_csv(csv_path)

    assert result.records == ()
    assert [error.to_dict() for error in result.diagnostics.errors] == [
        {
            "source": "invoices",
            "row_number": 2,
            "field": "invoice_id",
            "error_code": "missing_required",
            "message": "Missing required value.",
        },
        {
            "source": "invoices",
            "row_number": 2,
            "field": "customer_name",
            "error_code": "missing_required",
            "message": "Missing required value.",
        },
        {
            "source": "invoices",
            "row_number": 2,
            "field": "currency",
            "error_code": "missing_required",
            "message": "Missing required value.",
        },
        {
            "source": "invoices",
            "row_number": 2,
            "field": "invoice_date",
            "error_code": "invalid_date",
            "message": "Expected ISO date in YYYY-MM-DD format.",
        },
        {
            "source": "invoices",
            "row_number": 2,
            "field": "due_date",
            "error_code": "invalid_date",
            "message": "Expected ISO date in YYYY-MM-DD format.",
        },
        {
            "source": "invoices",
            "row_number": 2,
            "field": "invoice_amount",
            "error_code": "invalid_amount",
            "message": "Expected decimal money amount.",
        },
    ]
