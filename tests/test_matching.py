from datetime import date
from decimal import Decimal
from pathlib import Path

from invoice_reconciliation.ingestion import load_invoice_csv, load_payment_csv
from invoice_reconciliation.matching import (
    AmbiguousReferenceReason,
    MatchStatus,
    match_invoices_to_payments,
)
from invoice_reconciliation.models import InvoiceRecord, MoneyAmount, PaymentRecord

SAMPLE_DATA = Path(__file__).resolve().parents[1] / "sample-data"


def test_exact_successful_match() -> None:
    invoice = _invoice(invoice_id="INV-1001", amount="1200.00", currency="USD")
    payment = _payment(
        payment_id="PAY-5001",
        payment_reference="INV-1001",
        amount="1200.00",
        currency="USD",
    )

    result = match_invoices_to_payments([invoice], [payment])

    assert result.matched_pairs[0].reference == "INV-1001"
    assert result.matched_pairs[0].invoice is invoice
    assert result.matched_pairs[0].payment is payment
    assert result.matched_pairs[0].status == MatchStatus.MATCHED
    assert result.unmatched_invoices == ()
    assert result.unmatched_payments == ()
    assert result.amount_mismatches == ()
    assert result.currency_mismatches == ()
    assert result.ambiguous_references == ()


def test_unmatched_invoice() -> None:
    invoice = _invoice(invoice_id="INV-1001")

    result = match_invoices_to_payments([invoice], [])

    assert result.matched_pairs == ()
    assert result.unmatched_invoices[0].reference == "INV-1001"
    assert result.unmatched_invoices[0].invoice is invoice
    assert result.unmatched_invoices[0].status == MatchStatus.UNMATCHED_INVOICE


def test_unmatched_payment() -> None:
    payment = _payment(payment_id="PAY-5001", payment_reference="INV-9999")

    result = match_invoices_to_payments([], [payment])

    assert result.matched_pairs == ()
    assert result.unmatched_payments[0].reference == "INV-9999"
    assert result.unmatched_payments[0].payment is payment
    assert result.unmatched_payments[0].status == MatchStatus.UNMATCHED_PAYMENT


def test_amount_mismatch_when_reference_and_currency_match() -> None:
    invoice = _invoice(invoice_id="INV-1001", amount="1200.00", currency="USD")
    payment = _payment(
        payment_id="PAY-5001",
        payment_reference="INV-1001",
        amount="1199.99",
        currency="USD",
    )

    result = match_invoices_to_payments([invoice], [payment])

    assert result.matched_pairs == ()
    assert result.amount_mismatches[0].reference == "INV-1001"
    assert result.amount_mismatches[0].invoice is invoice
    assert result.amount_mismatches[0].payment is payment
    assert result.amount_mismatches[0].status == MatchStatus.AMOUNT_MISMATCH


def test_currency_mismatch_takes_precedence_over_amount_comparison() -> None:
    invoice = _invoice(invoice_id="INV-1001", amount="1200.00", currency="USD")
    payment = _payment(
        payment_id="PAY-5001",
        payment_reference="INV-1001",
        amount="1100.00",
        currency="EUR",
    )

    result = match_invoices_to_payments([invoice], [payment])

    assert result.matched_pairs == ()
    assert result.amount_mismatches == ()
    assert result.currency_mismatches[0].reference == "INV-1001"
    assert result.currency_mismatches[0].invoice is invoice
    assert result.currency_mismatches[0].payment is payment
    assert result.currency_mismatches[0].status == MatchStatus.CURRENCY_MISMATCH


def test_duplicate_payment_reference_is_ambiguous() -> None:
    invoice = _invoice(invoice_id="INV-1001")
    first_payment = _payment(
        payment_id="PAY-5001",
        payment_reference="INV-1001",
        row=5,
    )
    second_payment = _payment(
        payment_id="PAY-5002",
        payment_reference="INV-1001",
        row=6,
    )

    result = match_invoices_to_payments([invoice], [first_payment, second_payment])

    ambiguous = result.ambiguous_references[0]
    assert ambiguous.reference == "INV-1001"
    assert ambiguous.invoices == (invoice,)
    assert ambiguous.payments == (first_payment, second_payment)
    assert ambiguous.reason == AmbiguousReferenceReason.DUPLICATE_PAYMENT_REFERENCE
    assert ambiguous.status == MatchStatus.AMBIGUOUS_REFERENCE
    assert result.matched_pairs == ()


def test_duplicate_invoice_reference_is_ambiguous() -> None:
    first_invoice = _invoice(invoice_id="INV-1001", row=2)
    second_invoice = _invoice(invoice_id="INV-1001", row=3)
    payment = _payment(payment_id="PAY-5001", payment_reference="INV-1001")

    result = match_invoices_to_payments([first_invoice, second_invoice], [payment])

    ambiguous = result.ambiguous_references[0]
    assert ambiguous.reference == "INV-1001"
    assert ambiguous.invoices == (first_invoice, second_invoice)
    assert ambiguous.payments == (payment,)
    assert ambiguous.reason == AmbiguousReferenceReason.DUPLICATE_INVOICE_REFERENCE
    assert ambiguous.status == MatchStatus.AMBIGUOUS_REFERENCE
    assert result.matched_pairs == ()


def test_output_ordering_is_deterministic() -> None:
    invoices = [
        _invoice(invoice_id="INV-3003", row=4),
        _invoice(invoice_id="INV-1001", row=2),
        _invoice(invoice_id="INV-2002", row=3),
    ]
    payments = [
        _payment(payment_id="PAY-7001", payment_reference="INV-2002", row=7),
        _payment(payment_id="PAY-5001", payment_reference="INV-9999", row=5),
        _payment(payment_id="PAY-6001", payment_reference="INV-3003", row=6),
    ]

    first_result = match_invoices_to_payments(invoices, payments)
    second_result = match_invoices_to_payments(invoices, payments)

    assert first_result == second_result
    assert [pair.reference for pair in first_result.matched_pairs] == [
        "INV-3003",
        "INV-2002",
    ]
    assert [item.reference for item in first_result.unmatched_invoices] == ["INV-1001"]
    assert [item.reference for item in first_result.unmatched_payments] == ["INV-9999"]


def test_matcher_does_not_mutate_input_records() -> None:
    invoices = [_invoice(invoice_id="INV-1001")]
    payments = [_payment(payment_id="PAY-5001", payment_reference="INV-1001")]
    original_invoices = tuple(invoices)
    original_payments = tuple(payments)

    match_invoices_to_payments(invoices, payments)

    assert tuple(invoices) == original_invoices
    assert tuple(payments) == original_payments


def test_matches_phase_1_normalized_csv_records() -> None:
    invoices = load_invoice_csv(SAMPLE_DATA / "valid-invoices.csv").records
    payments = load_payment_csv(SAMPLE_DATA / "valid-payments.csv").records

    result = match_invoices_to_payments(invoices, payments)

    assert [pair.reference for pair in result.matched_pairs] == [
        "INV-1001",
        "INV-1002",
        "INV-1003",
    ]
    assert {pair.status for pair in result.matched_pairs} == {MatchStatus.MATCHED}
    assert result.unmatched_invoices == ()
    assert result.unmatched_payments == ()
    assert result.amount_mismatches == ()
    assert result.currency_mismatches == ()
    assert result.ambiguous_references == ()


def _invoice(
    *,
    invoice_id: str,
    amount: str = "1200.00",
    currency: str = "USD",
    row: int = 2,
) -> InvoiceRecord:
    return InvoiceRecord(
        invoice_id=invoice_id,
        customer_name="Acme Supplies",
        invoice_date=date(2026, 1, 3),
        due_date=date(2026, 2, 2),
        invoice_amount=MoneyAmount(value=Decimal(amount), currency=currency),
        source_row=row,
    )


def _payment(
    *,
    payment_id: str,
    payment_reference: str,
    amount: str = "1200.00",
    currency: str = "USD",
    row: int = 2,
) -> PaymentRecord:
    return PaymentRecord(
        payment_id=payment_id,
        customer_name="Acme Supplies",
        payment_date=date(2026, 1, 20),
        payment_amount=MoneyAmount(value=Decimal(amount), currency=currency),
        payment_reference=payment_reference,
        source_row=row,
    )
