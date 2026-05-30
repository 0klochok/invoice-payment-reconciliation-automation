# Invoice Payment Reconciliation Automation

CLI-first Python portfolio project for reconciling invoice files against payment
files. The tool is intended for accounting and operations teams that receive
separate invoice exports and payment exports, then need a repeatable way to
validate rows, match records, identify exceptions, and produce a clean report.

## Client Problem

Small finance and operations teams often reconcile invoices and payments in
spreadsheets by hand. That workflow is slow, inconsistent, and difficult to
review. This project demonstrates a local automation that will turn synthetic
invoice and payment files into deterministic reconciliation outputs.

## Planned Features

- Import invoice and payment files from CSV and XLSX.
- Validate required fields, dates, amounts, and currency consistency.
- Normalize customer names and email addresses.
- Match payments to invoices using deterministic business rules.
- Categorize exceptions such as missing payments, duplicate payments, and
  overpayments or underpayments.
- Generate Markdown and CSV reconciliation reports for review.

## Current Status

The current implementation supports CSV/XLSX inputs and client-presentable local
reports on top of the existing ingestion, matching, and reporting foundation:

- Immutable invoice, payment, money amount, and import diagnostic models.
- CSV loading with Python's standard library `csv` module.
- XLSX loading with `openpyxl` for local spreadsheet input parsing.
- Required-field validation, ISO date parsing, decimal amount parsing,
  whitespace trimming, and currency uppercasing.
- Deterministic exact-reference payment-to-invoice matching.
- Explicit exception classifications for invoices missing payments, payments
  missing invoices, amount variances, currency conflicts, and duplicate
  references.
- Markdown report generation with concise totals, status counts, sorted detail
  sections, and readable review notes.
- CSV summary and detail report generation with stable ordering and
  client-readable exception labels.
- CLI report command that loads CSV or XLSX samples, runs matching, and writes
  local Markdown and CSV reports to an output directory.
- Synthetic CSV and XLSX files under `sample-data/`, including a mixed-status
  demo.

Fuzzy matching and partial payment allocation are intentionally not implemented
yet.

## Quickstart

Use PowerShell from the repository root.

```powershell
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run reconcile --help
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\xlsx-demo
```

The report command writes these local files:

- `reports\demo\reconciliation-report.md`
- `reports\demo\reconciliation-summary.csv`
- `reports\demo\reconciliation-details.csv`

## Demo Walkthrough

Use the mixed demo sample when presenting the project locally:

```powershell
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo
Get-Content -Raw reports\demo\reconciliation-report.md
```

Use the XLSX equivalent when demonstrating spreadsheet input support:

```powershell
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\xlsx-demo
Get-Content -Raw reports\xlsx-demo\reconciliation-report.md
```

The mixed demo is deterministic and uses fake data only. It produces a Markdown
report with reconciliation totals, status counts, matched records, invoices
missing payments, payments missing invoices, underpaid/overpaid amount
variances, currency conflicts, and duplicate references needing review. The CSV
outputs contain the same status labels and sorted detail rows for spreadsheet
review.

## Sample Data

Synthetic CSV and XLSX files are available for local demos and tests:

- `sample-data/valid-invoices.csv`
- `sample-data/valid-payments.csv`
- `sample-data/demo-mixed-invoices.csv`
- `sample-data/demo-mixed-payments.csv`
- `sample-data/demo-mixed-invoices.xlsx`
- `sample-data/demo-mixed-payments.xlsx`
- `sample-data/invalid-invoices.csv`
- `sample-data/invalid-payments.csv`

## Roadmap

| Phase | Objective | Status |
|---|---|---|
| Phase 0 | Repository foundation, docs, project skeleton, quality tooling | Complete |
| Phase 1 | Input schemas, sample data, CSV loading, normalization, validation | Complete |
| Phase 2 | Matching engine and exception classification | Complete |
| Phase 3 | Markdown and CSV report generation with CLI orchestration | Complete |
| Phase 4 | Demo sample coverage and client-demo readiness | Complete |
| Phase 5 | XLSX invoice/payment input support | Complete |
| Phase 6 | Client-presentable exception reporting and CLI demo polish | Complete |

## Safety and Data Policy

- Use fake sample data only.
- Do not use real client data.
- Do not commit secrets or local credentials.
- No paid APIs, AI calls, deployment, database, FastAPI, or GitHub Actions are
  included in the current local-demo scope.
