"""Local deterministic reconciliation report generation."""

from __future__ import annotations

import csv
from collections.abc import Iterable
from dataclasses import dataclass
from decimal import Decimal
from io import StringIO
from pathlib import Path

from .matching import (
    AmbiguousReference,
    AmbiguousReferenceReason,
    AmountMismatch,
    CurrencyMismatch,
    MatchedPair,
    MatchStatus,
    ReconciliationResult,
    UnmatchedInvoice,
    UnmatchedPayment,
)
from .models import InvoiceRecord, MoneyAmount, PaymentRecord

STATUS_ORDER = (
    MatchStatus.MATCHED,
    MatchStatus.UNMATCHED_INVOICE,
    MatchStatus.UNMATCHED_PAYMENT,
    MatchStatus.AMOUNT_MISMATCH,
    MatchStatus.CURRENCY_MISMATCH,
    MatchStatus.AMBIGUOUS_REFERENCE,
)

STATUS_LABELS = {
    MatchStatus.MATCHED: "Matched",
    MatchStatus.UNMATCHED_INVOICE: "Unmatched invoice",
    MatchStatus.UNMATCHED_PAYMENT: "Unmatched payment",
    MatchStatus.AMOUNT_MISMATCH: "Amount mismatch",
    MatchStatus.CURRENCY_MISMATCH: "Currency mismatch",
    MatchStatus.AMBIGUOUS_REFERENCE: "Ambiguous duplicate reference",
}

AMBIGUOUS_REASON_LABELS = {
    AmbiguousReferenceReason.DUPLICATE_INVOICE_REFERENCE: (
        "Duplicate invoice reference"
    ),
    AmbiguousReferenceReason.DUPLICATE_PAYMENT_REFERENCE: (
        "Duplicate payment reference"
    ),
    AmbiguousReferenceReason.DUPLICATE_INVOICE_AND_PAYMENT_REFERENCE: (
        "Duplicate invoice and payment reference"
    ),
}

SUMMARY_COLUMNS = ("status", "status_label", "count")
DETAIL_COLUMNS = (
    "status",
    "status_label",
    "reference",
    "invoice_id",
    "payment_id",
    "customer_name",
    "invoice_amount",
    "payment_amount",
    "invoice_source_row",
    "payment_source_row",
    "reason",
)


@dataclass(frozen=True, slots=True)
class ReportOutputPaths:
    """Paths written by the local report writer."""

    markdown: Path
    summary_csv: Path
    details_csv: Path


def build_summary_counts(result: ReconciliationResult) -> dict[MatchStatus, int]:
    """Return deterministic counts by reconciliation status."""
    counts_by_status = {
        MatchStatus.MATCHED: len(result.matched_pairs),
        MatchStatus.UNMATCHED_INVOICE: len(result.unmatched_invoices),
        MatchStatus.UNMATCHED_PAYMENT: len(result.unmatched_payments),
        MatchStatus.AMOUNT_MISMATCH: len(result.amount_mismatches),
        MatchStatus.CURRENCY_MISMATCH: len(result.currency_mismatches),
        MatchStatus.AMBIGUOUS_REFERENCE: len(result.ambiguous_references),
    }
    return {status: counts_by_status[status] for status in STATUS_ORDER}


def render_markdown_report(result: ReconciliationResult) -> str:
    """Render a deterministic client-readable Markdown report."""
    lines = [
        "# Reconciliation Report",
        "",
        "## Summary",
        "",
    ]
    lines.extend(
        _markdown_table(
            ("Status", "Count"),
            [
                (STATUS_LABELS[status], str(count))
                for status, count in build_summary_counts(result).items()
            ],
        )
    )

    lines.extend(
        _markdown_section(
            "Matched Invoice/Payment Pairs",
            ("Reference", "Invoice ID", "Payment ID", "Customer", "Amount"),
            (
                (
                    pair.reference,
                    pair.invoice.invoice_id,
                    pair.payment.payment_id,
                    pair.invoice.customer_name,
                    _format_money(pair.invoice.invoice_amount),
                )
                for pair in result.matched_pairs
            ),
        )
    )
    lines.extend(
        _markdown_section(
            "Unmatched Invoices",
            ("Reference", "Invoice ID", "Customer", "Invoice Amount"),
            (
                (
                    item.reference,
                    item.invoice.invoice_id,
                    item.invoice.customer_name,
                    _format_money(item.invoice.invoice_amount),
                )
                for item in result.unmatched_invoices
            ),
        )
    )
    lines.extend(
        _markdown_section(
            "Unmatched Payments",
            ("Reference", "Payment ID", "Customer", "Payment Amount"),
            (
                (
                    item.reference,
                    item.payment.payment_id,
                    item.payment.customer_name,
                    _format_money(item.payment.payment_amount),
                )
                for item in result.unmatched_payments
            ),
        )
    )
    lines.extend(
        _markdown_section(
            "Amount Mismatches",
            (
                "Reference",
                "Invoice ID",
                "Payment ID",
                "Invoice Amount",
                "Payment Amount",
            ),
            (
                (
                    item.reference,
                    item.invoice.invoice_id,
                    item.payment.payment_id,
                    _format_money(item.invoice.invoice_amount),
                    _format_money(item.payment.payment_amount),
                )
                for item in result.amount_mismatches
            ),
        )
    )
    lines.extend(
        _markdown_section(
            "Currency Mismatches",
            (
                "Reference",
                "Invoice ID",
                "Payment ID",
                "Invoice Amount",
                "Payment Amount",
            ),
            (
                (
                    item.reference,
                    item.invoice.invoice_id,
                    item.payment.payment_id,
                    _format_money(item.invoice.invoice_amount),
                    _format_money(item.payment.payment_amount),
                )
                for item in result.currency_mismatches
            ),
        )
    )
    lines.extend(
        _markdown_section(
            "Ambiguous Duplicate References",
            ("Reference", "Invoice IDs", "Payment IDs", "Reason"),
            (
                (
                    item.reference,
                    _join_values(invoice.invoice_id for invoice in item.invoices),
                    _join_values(payment.payment_id for payment in item.payments),
                    AMBIGUOUS_REASON_LABELS[item.reason],
                )
                for item in result.ambiguous_references
            ),
        )
    )

    return "\n".join(lines).rstrip() + "\n"


def render_summary_csv(result: ReconciliationResult) -> str:
    """Render status counts as deterministic CSV text."""
    rows = [
        {
            "status": status.value,
            "status_label": STATUS_LABELS[status],
            "count": str(count),
        }
        for status, count in build_summary_counts(result).items()
    ]
    return _render_csv(SUMMARY_COLUMNS, rows)


def render_details_csv(result: ReconciliationResult) -> str:
    """Render reconciliation detail rows as deterministic CSV text."""
    return _render_csv(DETAIL_COLUMNS, _detail_rows(result))


def write_reconciliation_reports(
    result: ReconciliationResult,
    output_dir: str | Path,
) -> ReportOutputPaths:
    """Write Markdown and CSV reconciliation reports to a local directory."""
    directory = Path(output_dir)
    directory.mkdir(parents=True, exist_ok=True)

    paths = ReportOutputPaths(
        markdown=directory / "reconciliation-report.md",
        summary_csv=directory / "reconciliation-summary.csv",
        details_csv=directory / "reconciliation-details.csv",
    )
    _write_text(paths.markdown, render_markdown_report(result))
    _write_text(paths.summary_csv, render_summary_csv(result))
    _write_text(paths.details_csv, render_details_csv(result))
    return paths


def _detail_rows(result: ReconciliationResult) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    rows.extend(_matched_row(pair) for pair in result.matched_pairs)
    rows.extend(_unmatched_invoice_row(item) for item in result.unmatched_invoices)
    rows.extend(_unmatched_payment_row(item) for item in result.unmatched_payments)
    rows.extend(_amount_mismatch_row(item) for item in result.amount_mismatches)
    rows.extend(_currency_mismatch_row(item) for item in result.currency_mismatches)
    rows.extend(_ambiguous_reference_row(item) for item in result.ambiguous_references)
    return rows


def _matched_row(item: MatchedPair) -> dict[str, str]:
    row = _base_detail_row(item.status, item.reference)
    _add_invoice(row, item.invoice)
    _add_payment(row, item.payment)
    return row


def _unmatched_invoice_row(item: UnmatchedInvoice) -> dict[str, str]:
    row = _base_detail_row(item.status, item.reference)
    _add_invoice(row, item.invoice)
    return row


def _unmatched_payment_row(item: UnmatchedPayment) -> dict[str, str]:
    row = _base_detail_row(item.status, item.reference)
    _add_payment(row, item.payment)
    return row


def _amount_mismatch_row(item: AmountMismatch) -> dict[str, str]:
    row = _base_detail_row(item.status, item.reference)
    _add_invoice(row, item.invoice)
    _add_payment(row, item.payment)
    row["reason"] = "Invoice and payment amounts differ"
    return row


def _currency_mismatch_row(item: CurrencyMismatch) -> dict[str, str]:
    row = _base_detail_row(item.status, item.reference)
    _add_invoice(row, item.invoice)
    _add_payment(row, item.payment)
    row["reason"] = "Invoice and payment currencies differ"
    return row


def _ambiguous_reference_row(item: AmbiguousReference) -> dict[str, str]:
    row = _base_detail_row(item.status, item.reference)
    row["invoice_id"] = _join_values(invoice.invoice_id for invoice in item.invoices)
    row["payment_id"] = _join_values(payment.payment_id for payment in item.payments)
    row["customer_name"] = _join_values(
        record.customer_name for record in (*item.invoices, *item.payments)
    )
    row["invoice_amount"] = _join_values(
        _format_money(invoice.invoice_amount) for invoice in item.invoices
    )
    row["payment_amount"] = _join_values(
        _format_money(payment.payment_amount) for payment in item.payments
    )
    row["invoice_source_row"] = _join_values(
        str(invoice.source_row) for invoice in item.invoices
    )
    row["payment_source_row"] = _join_values(
        str(payment.source_row) for payment in item.payments
    )
    row["reason"] = AMBIGUOUS_REASON_LABELS[item.reason]
    return row


def _base_detail_row(status: MatchStatus, reference: str) -> dict[str, str]:
    return {
        "status": status.value,
        "status_label": STATUS_LABELS[status],
        "reference": reference,
        "invoice_id": "",
        "payment_id": "",
        "customer_name": "",
        "invoice_amount": "",
        "payment_amount": "",
        "invoice_source_row": "",
        "payment_source_row": "",
        "reason": "",
    }


def _add_invoice(row: dict[str, str], invoice: InvoiceRecord) -> None:
    row["invoice_id"] = invoice.invoice_id
    row["customer_name"] = invoice.customer_name
    row["invoice_amount"] = _format_money(invoice.invoice_amount)
    row["invoice_source_row"] = str(invoice.source_row)


def _add_payment(row: dict[str, str], payment: PaymentRecord) -> None:
    row["payment_id"] = payment.payment_id
    row["customer_name"] = row["customer_name"] or payment.customer_name
    row["payment_amount"] = _format_money(payment.payment_amount)
    row["payment_source_row"] = str(payment.source_row)


def _markdown_section(
    title: str,
    headers: tuple[str, ...],
    rows: Iterable[tuple[str, ...]],
) -> list[str]:
    section = ["", f"## {title}", ""]
    row_list = list(rows)
    if not row_list:
        section.append("No records.")
        return section
    section.extend(_markdown_table(headers, row_list))
    return section


def _markdown_table(
    headers: tuple[str, ...],
    rows: Iterable[tuple[str, ...]],
) -> list[str]:
    table = [
        "| " + " | ".join(_markdown_cell(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    table.extend(
        "| " + " | ".join(_markdown_cell(value) for value in row) + " |" for row in rows
    )
    return table


def _markdown_cell(value: str) -> str:
    return value.replace("|", "\\|")


def _render_csv(columns: tuple[str, ...], rows: Iterable[dict[str, str]]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=columns, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def _write_text(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as file:
        file.write(content)


def _format_money(money: MoneyAmount) -> str:
    return f"{_format_decimal(money.value)} {money.currency}"


def _format_decimal(value: Decimal) -> str:
    return format(value, "f")


def _join_values(values: Iterable[str]) -> str:
    unique_values: list[str] = []
    for value in values:
        if value and value not in unique_values:
            unique_values.append(value)
    return "; ".join(unique_values)
