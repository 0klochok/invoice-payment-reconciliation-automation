# Invoice Payment Reconciliation Automation

CLI-first Python portfolio project for reconciling invoice files against payment
files. The tool imports synthetic CSV or XLSX invoice/payment exports, validates
rows, matches payments to invoices with deterministic local rules, categorizes
exceptions, and writes review-ready Markdown and CSV reports.

## Project Purpose

Small finance and operations teams often reconcile invoices and payments in
spreadsheets by hand. That workflow is slow, inconsistent, and hard to review.
This project demonstrates a local automation that turns synthetic invoice and
payment exports into deterministic exception reports suitable for a portfolio or
client demo.

## What This Demonstrates

- Business automation for a common back-office reconciliation workflow.
- Input validation and normalization before reconciliation logic runs.
- Deterministic matching with explicit exception categories for human review.
- Review-ready Markdown and CSV outputs that are easy to inspect or share.
- Reproducible local demos using fake CSV/XLSX data and locked dependencies.
- Test coverage and quality gates suitable for a portfolio-ready Python CLI
  demo project.

## Evaluator Walkthrough

1. Run the Quickstart commands to install from the lockfile and verify tests,
   linting, formatting, and CLI help.
2. Run the CSV demo command and inspect `reports\demo-csv`.
3. Run the XLSX demo command and inspect `reports\demo-xlsx`.
4. Confirm both demo directories contain only `reconciliation-report.md`,
   `reconciliation-summary.csv`, and `reconciliation-details.csv`.
5. Compare the generated outputs with the committed snapshot under
   `docs/demo-output/mixed-demo/`.

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

## Supported Inputs And Outputs

The CLI accepts invoice and payment files in these formats:

- CSV files with the sample invoice/payment columns.
- XLSX workbooks with equivalent single-sheet invoice/payment data.

The report workflow writes three local review artifacts to the requested output
directory:

- `reconciliation-report.md` for a human-readable summary and exception review.
- `reconciliation-summary.csv` for status counts by reconciliation category.
- `reconciliation-details.csv` for row-level matched and exception details.

Generated report artifacts belong under ignored `reports/` paths during local
demos. The committed `docs/demo-output/mixed-demo/` snapshot is the only
intentional generated report example.

## Quickstart

Use PowerShell from the repository root. Install dependencies from the lockfile
and run the local quality gate:

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
uv run reconcile report --invoices sample-data/mixed-demo/invoices.csv --payments sample-data/mixed-demo/payments.csv --out-dir reports\demo-csv
```

Run the equivalent XLSX-input demo:

```powershell
uv run reconcile report --invoices sample-data/mixed-demo/invoices.xlsx --payments sample-data/mixed-demo/payments.xlsx --out-dir reports\demo-xlsx
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
- `mixed-demo/invoices.csv` and `mixed-demo/payments.csv` demonstrate the main
  portfolio scenario.
- `mixed-demo/invoices.xlsx` and `mixed-demo/payments.xlsx` contain equivalent
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
- GitHub Actions is CI-only; it does not deploy, upload artifacts, or use
  secrets.
- No paid APIs, AI calls, runtime external services, or real client data.
- Current normalization covers whitespace and currency casing; email
  normalization is not part of the current sample schema.

## Implementation Status

The portfolio version is complete for the local CLI demo scope:

- Local CSV/XLSX invoice and payment imports.
- Deterministic validation, normalization, matching, and exception
  classification.
- Markdown and CSV reconciliation reports.
- Synthetic sample data and committed Markdown/CSV demo-output snapshot.
- Local quality gate and minimal GitHub Actions CI smoke coverage.

Future enhancements such as fuzzy matching, partial-payment allocation, Excel
workbook report output, web APIs, databases, deployment, paid APIs, and AI calls
are intentionally outside the current portfolio scope.

## Safety And Data Policy

- Use fake sample data only.
- Do not use real client data.
- Do not commit secrets or local credentials.
- Do not store production exports in this repository.
- Keep generated local report artifacts under ignored `reports/` paths unless
  they are intentional Markdown/CSV examples under `docs/demo-output/`.
