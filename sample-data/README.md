# Sample Data

This directory contains synthetic CSV and XLSX files for local demos and
automated tests. The records are fake and must not be replaced with real client
exports.

## Files

| File | Purpose |
|---|---|
| `valid-invoices.csv` | Valid invoice rows with basic whitespace and currency normalization examples. |
| `valid-payments.csv` | Valid payment rows with references used by matching and report demos. |
| `demo-mixed-invoices.csv` | Fake invoice rows for the mixed portfolio demo scenario. |
| `demo-mixed-payments.csv` | Fake payment rows for the mixed portfolio demo scenario. |
| `demo-mixed-invoices.xlsx` | XLSX equivalent of the mixed invoice demo rows. |
| `demo-mixed-payments.xlsx` | XLSX equivalent of the mixed payment demo rows. |
| `invalid-invoices.csv` | Invalid invoice rows for manual validation checks. |
| `invalid-payments.csv` | Invalid payment rows for manual validation checks. |

Current local workflows support CSV/XLSX ingestion, deterministic matching, and
Markdown/CSV report generation.

The clean `valid-*` files demonstrate fully matched records. The `demo-mixed-*`
files demonstrate matched records, invoices missing payments, payments missing
invoices, underpaid amount variances, currency conflicts, duplicate payment
references, and duplicate invoice references in one deterministic local
scenario. The generated reports sort rows by status and reference and use
review notes for exception rows. The mixed CSV and XLSX inputs are intentionally
equivalent.

Do not place real client data, production exports, secrets, credentials, or
private information in this directory.
