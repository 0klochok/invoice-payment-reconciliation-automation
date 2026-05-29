import csv
from datetime import date
from decimal import Decimal
from pathlib import Path

from invoice_reconciliation.matching import MatchStatus, match_invoices_to_payments
from invoice_reconciliation.models import InvoiceRecord, MoneyAmount, PaymentRecord
from invoice_reconciliation.reporting import (
    STATUS_LABELS,
    build_summary_counts,
    render_details_csv,
    render_markdown_report,
    render_summary_csv,
    write_reconciliation_reports,
)


def test_summary_counts_include_all_phase_2_statuses() -> None:
    result = _mixed_reconciliation_result()

    assert build_summary_counts(result) == {
        MatchStatus.MATCHED: 1,
        MatchStatus.UNMATCHED_INVOICE: 1,
        MatchStatus.UNMATCHED_PAYMENT: 1,
        MatchStatus.AMOUNT_MISMATCH: 1,
        MatchStatus.CURRENCY_MISMATCH: 1,
        MatchStatus.AMBIGUOUS_REFERENCE: 1,
    }


def test_markdown_report_contains_sections_and_client_readable_labels() -> None:
    markdown = render_markdown_report(_mixed_reconciliation_result())

    assert "# Reconciliation Report" in markdown
    assert "| Matched | 1 |" in markdown
    assert "| Unmatched invoice | 1 |" in markdown
    assert "| Unmatched payment | 1 |" in markdown
    assert "| Amount mismatch | 1 |" in markdown
    assert "| Currency mismatch | 1 |" in markdown
    assert "| Ambiguous duplicate reference | 1 |" in markdown
    assert "## Matched Invoice/Payment Pairs" in markdown
    assert "## Unmatched Invoices" in markdown
    assert "## Unmatched Payments" in markdown
    assert "## Amount Mismatches" in markdown
    assert "## Currency Mismatches" in markdown
    assert "## Ambiguous Duplicate References" in markdown
    assert "Duplicate payment reference" in markdown


def test_csv_reports_include_summary_and_detail_rows() -> None:
    result = _mixed_reconciliation_result()

    summary_rows = list(csv.DictReader(render_summary_csv(result).splitlines()))
    detail_rows = list(csv.DictReader(render_details_csv(result).splitlines()))

    assert summary_rows == [
        {
            "status": status.value,
            "status_label": STATUS_LABELS[status],
            "count": "1",
        }
        for status in (
            MatchStatus.MATCHED,
            MatchStatus.UNMATCHED_INVOICE,
            MatchStatus.UNMATCHED_PAYMENT,
            MatchStatus.AMOUNT_MISMATCH,
            MatchStatus.CURRENCY_MISMATCH,
            MatchStatus.AMBIGUOUS_REFERENCE,
        )
    ]
    assert len(detail_rows) == 6
    assert detail_rows[0]["status"] == "matched"
    assert detail_rows[0]["status_label"] == "Matched"
    assert detail_rows[0]["reference"] == "INV-MATCH"
    assert detail_rows[0]["invoice_id"] == "INV-MATCH"
    assert detail_rows[0]["payment_id"] == "PAY-MATCH"
    assert detail_rows[-1]["status"] == "ambiguous_reference"
    assert detail_rows[-1]["reason"] == "Duplicate payment reference"


def test_detail_csv_ordering_is_deterministic() -> None:
    first = list(
        csv.DictReader(render_details_csv(_mixed_reconciliation_result()).splitlines())
    )
    second = list(
        csv.DictReader(render_details_csv(_mixed_reconciliation_result()).splitlines())
    )

    assert first == second
    assert [row["status"] for row in first] == [
        "matched",
        "unmatched_invoice",
        "unmatched_payment",
        "amount_mismatch",
        "currency_mismatch",
        "ambiguous_reference",
    ]
    assert [row["reference"] for row in first] == [
        "INV-MATCH",
        "INV-ONLY",
        "INV-PAY-ONLY",
        "INV-AMOUNT",
        "INV-CURRENCY",
        "INV-DUP",
    ]


def test_write_reports_uses_output_directory_and_does_not_mutate_inputs(
    tmp_path: Path,
) -> None:
    invoices, payments = _mixed_records()
    original_invoices = tuple(invoices)
    original_payments = tuple(payments)
    result = match_invoices_to_payments(invoices, payments)

    paths = write_reconciliation_reports(result, tmp_path / "report-output")

    assert paths.markdown == tmp_path / "report-output" / "reconciliation-report.md"
    assert paths.summary_csv == (
        tmp_path / "report-output" / "reconciliation-summary.csv"
    )
    assert paths.details_csv == (
        tmp_path / "report-output" / "reconciliation-details.csv"
    )
    assert paths.markdown.read_text(encoding="utf-8").startswith(
        "# Reconciliation Report"
    )
    assert paths.summary_csv.read_text(encoding="utf-8").startswith(
        "status,status_label,count\n"
    )
    assert paths.details_csv.read_text(encoding="utf-8").startswith(
        "status,status_label,reference"
    )
    assert tuple(invoices) == original_invoices
    assert tuple(payments) == original_payments


def _mixed_reconciliation_result():
    invoices, payments = _mixed_records()
    return match_invoices_to_payments(invoices, payments)


def _mixed_records() -> tuple[list[InvoiceRecord], list[PaymentRecord]]:
    invoices = [
        _invoice(invoice_id="INV-MATCH", amount="1200.00", currency="USD", row=2),
        _invoice(invoice_id="INV-ONLY", amount="300.00", currency="USD", row=3),
        _invoice(invoice_id="INV-AMOUNT", amount="875.50", currency="EUR", row=4),
        _invoice(invoice_id="INV-CURRENCY", amount="430.25", currency="USD", row=5),
        _invoice(invoice_id="INV-DUP", amount="99.00", currency="USD", row=6),
    ]
    payments = [
        _payment(
            payment_id="PAY-MATCH",
            payment_reference="INV-MATCH",
            amount="1200.00",
            currency="USD",
            row=2,
        ),
        _payment(
            payment_id="PAY-AMOUNT",
            payment_reference="INV-AMOUNT",
            amount="875.49",
            currency="EUR",
            row=3,
        ),
        _payment(
            payment_id="PAY-CURRENCY",
            payment_reference="INV-CURRENCY",
            amount="430.25",
            currency="EUR",
            row=4,
        ),
        _payment(
            payment_id="PAY-DUP-1",
            payment_reference="INV-DUP",
            amount="99.00",
            currency="USD",
            row=5,
        ),
        _payment(
            payment_id="PAY-DUP-2",
            payment_reference="INV-DUP",
            amount="99.00",
            currency="USD",
            row=6,
        ),
        _payment(
            payment_id="PAY-ONLY",
            payment_reference="INV-PAY-ONLY",
            amount="700.00",
            currency="USD",
            row=7,
        ),
    ]
    return invoices, payments


def _invoice(
    *,
    invoice_id: str,
    amount: str,
    currency: str,
    row: int,
) -> InvoiceRecord:
    return InvoiceRecord(
        invoice_id=invoice_id,
        customer_name=f"{invoice_id} Customer",
        invoice_date=date(2026, 1, 3),
        due_date=date(2026, 2, 2),
        invoice_amount=MoneyAmount(value=Decimal(amount), currency=currency),
        source_row=row,
    )


def _payment(
    *,
    payment_id: str,
    payment_reference: str,
    amount: str,
    currency: str,
    row: int,
) -> PaymentRecord:
    return PaymentRecord(
        payment_id=payment_id,
        customer_name=f"{payment_reference} Customer",
        payment_date=date(2026, 1, 20),
        payment_amount=MoneyAmount(value=Decimal(amount), currency=currency),
        payment_reference=payment_reference,
        source_row=row,
    )
