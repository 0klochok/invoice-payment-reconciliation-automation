# Invoice Payment Reconciliation Automation

CLI-first Python portfolio project for reconciling invoice files against payment
files. The tool imports synthetic CSV or XLSX invoice/payment exports, validates
rows, matches payments to invoices with deterministic local rules, categorizes
exceptions, and writes review-ready Markdown and CSV reports.

## Project Purpose

Small finance and operations teams often reconcile invoices and payments in
spreadsheets by hand. That workflow is slow, inconsistent, and hard to review.
This project demonstrates a local automation that turns fake invoice and payment
exports into deterministic reconciliation outputs suitable for a portfolio or
client demo.

## Current Features

- CSV and XLSX invoice/payment input parsing.
- Required-field validation for invoice and payment rows.
- ISO date parsing and decimal money amount parsing.
- Whitespace trimming for text fields and uppercasing for currency values.
- Deterministic exact-reference matching between invoice IDs and payment
  references.
- Exception categories for invoices missing payments, payments missing
  invoices, amount differences, currency differences, and duplicate references.
- Markdown reconciliation report with totals, status summary, sorted detail
  sections, and review notes.
- Summary CSV and details CSV outputs for spreadsheet review.
- `reconcile report` CLI command for the full local demo workflow.
- Synthetic sample data only.

## Quickstart

Use PowerShell from the repository root. Install dependencies from the lockfile
and run the local release-readiness gate:

```powershell
uv sync --locked --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run reconcile --help
uv run reconcile report --help
```

## CI Quality Gate

GitHub Actions runs the same locked `uv` sync (`uv sync --locked --dev`),
pytest, Ruff checks, CLI help smoke checks, and CSV/XLSX demo commands on pull
requests and pushes to `main`.

## Demo Commands

Run the mixed CSV demo:

```powershell
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo-csv
```

Run the equivalent XLSX-input demo:

```powershell
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\demo-xlsx
```

Both commands write exactly these report files inside the selected output
directory:

- `reconciliation-report.md`
- `reconciliation-summary.csv`
- `reconciliation-details.csv`

For example, the CSV command writes:

- `reports\demo-csv\reconciliation-report.md`
- `reports\demo-csv\reconciliation-summary.csv`
- `reports\demo-csv\reconciliation-details.csv`

## Sample Data And Reports

Synthetic inputs live under `sample-data/`.

- `valid-invoices.csv` and `valid-payments.csv` demonstrate a clean fully
  matched scenario.
- `invalid-invoices.csv` and `invalid-payments.csv` demonstrate validation
  failures.
- `demo-mixed-invoices.csv` and `demo-mixed-payments.csv` demonstrate the main
  portfolio scenario.
- `demo-mixed-invoices.xlsx` and `demo-mixed-payments.xlsx` contain equivalent
  XLSX inputs for the same mixed scenario.

The mixed demo reviews 8 invoice rows and 8 payment rows. It produces 2 matched
pairs and 6 exception groups: one invoice missing payment, one payment missing
invoice, one amount variance, one currency conflict, and two duplicate-reference
groups.

The generated reports are local artifacts. Files under `reports/` are ignored by
Git.

## Demo Output Snapshot

A small generated snapshot is included under `docs/demo-output/mixed-demo/` for
reviewers who want to inspect the expected Markdown and CSV output without
running the CLI first. It was generated from the mixed CSV sample data and
contains only:

- `docs/demo-output/mixed-demo/reconciliation-report.md`
- `docs/demo-output/mixed-demo/reconciliation-summary.csv`
- `docs/demo-output/mixed-demo/reconciliation-details.csv`

No XLSX report output or large binary report artifact is included.

## Limitations And Non-Goals

- No fuzzy matching or probabilistic matching.
- No partial-payment allocation or many-to-one matching.
- No Excel workbook report output.
- No web app, FastAPI service, database, deployment, or hosted runtime
  automation.
- No paid APIs, AI calls, runtime external services, or real client data.
- Current normalization covers whitespace and currency casing; email
  normalization is not part of the current sample schema.

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
| Phase 7 | Final portfolio/demo readiness documentation pass | Complete |
| Phase 8 | Final local release-readiness review | Complete |
| Phase 9 | Minimal GitHub Actions CI quality gate | Complete |
| Phase 10 | Final portfolio polish and release-readiness review | Complete |

## Safety And Data Policy

- Use fake sample data only.
- Do not use real client data.
- Do not commit secrets or local credentials.
- Do not store production exports in this repository.
- Keep generated local report artifacts under ignored `reports/` paths unless
  they are intentional Markdown/CSV examples under `docs/demo-output/`.
