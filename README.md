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
- Generate Markdown, CSV, and future Excel reconciliation reports for review.

## Current Status

Phase 4 improves sample data coverage and client-demo readiness on top of the
ingestion, matching, and reporting foundation:

- Immutable invoice, payment, money amount, and import diagnostic models.
- Dependency-free CSV loading with Python's standard library `csv` module.
- Required-field validation, ISO date parsing, decimal amount parsing,
  whitespace trimming, and currency uppercasing.
- Deterministic exact-reference payment-to-invoice matching.
- Explicit exception classifications for unmatched records, amount mismatches,
  currency mismatches, and ambiguous duplicate references.
- Markdown summary/detail report generation.
- CSV summary and detail report generation for spreadsheet review.
- CLI report command that loads CSV samples, runs matching, and writes local
  reports to an output directory.
- Synthetic CSV files under `sample-data/`, including a mixed-status demo.

Excel report writing, fuzzy matching, and XLSX loading are intentionally not
implemented yet.

## Quickstart

Use PowerShell from the repository root.

```powershell
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run reconcile --help
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo
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

The mixed demo is deterministic and uses fake data only. It produces summary
counts for matched records, unmatched invoices, unmatched payments, amount
mismatches, currency mismatches, and ambiguous duplicate references.

## Sample Data

Synthetic CSV files are available for local demos and tests:

- `sample-data/valid-invoices.csv`
- `sample-data/valid-payments.csv`
- `sample-data/demo-mixed-invoices.csv`
- `sample-data/demo-mixed-payments.csv`
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
| Phase 5 | XLSX input and Excel workbook report support | Planned |

## Safety and Data Policy

- Use fake sample data only.
- Do not use real client data.
- Do not commit secrets or local credentials.
- No paid APIs, AI calls, deployment, database, FastAPI, or GitHub Actions are
  included in the current local-demo scope.
