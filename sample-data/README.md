# Sample Data

This directory contains synthetic CSV and XLSX files for local demos and
automated tests. The records are fake and must not be replaced with real client
exports.

## Files

| File | Purpose |
|---|---|
| `valid-invoices.csv` | Clean invoice rows for a fully matched smoke scenario. |
| `valid-payments.csv` | Clean payment rows for a fully matched smoke scenario. |
| `demo-mixed-invoices.csv` | Fake invoice rows for the mixed portfolio demo. |
| `demo-mixed-payments.csv` | Fake payment rows for the mixed portfolio demo. |
| `demo-mixed-invoices.xlsx` | XLSX equivalent of the mixed invoice demo rows. |
| `demo-mixed-payments.xlsx` | XLSX equivalent of the mixed payment demo rows. |
| `invalid-invoices.csv` | Invalid invoice rows for validation checks. |
| `invalid-payments.csv` | Invalid payment rows for validation checks. |

## Demo Scenarios

The clean `valid-*` files demonstrate a fully matched reconciliation.

The `demo-mixed-*` files demonstrate the main portfolio scenario:

- 8 invoice rows reviewed.
- 8 payment rows reviewed.
- 2 matched invoice/payment pairs.
- 1 invoice missing payment.
- 1 payment missing invoice.
- 1 amount variance.
- 1 currency conflict.
- 2 duplicate-reference groups needing review.

The mixed CSV and XLSX inputs are intentionally equivalent. Running the CLI with
the CSV or XLSX mixed inputs should produce equivalent Markdown, summary CSV,
and details CSV report content.

## Generated Reports

Local demo reports should be written under ignored `reports/` paths:

```powershell
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo-csv
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\demo-xlsx
```

Each output directory should contain only:

- `reconciliation-report.md`
- `reconciliation-summary.csv`
- `reconciliation-details.csv`

A committed reviewer snapshot is available under `docs/demo-output/mixed-demo/`.
It was generated from the mixed CSV sample data and intentionally contains only
Markdown/CSV report examples. There is no XLSX report output.

Do not place real client data, production exports, secrets, credentials, or
private information in this directory.
