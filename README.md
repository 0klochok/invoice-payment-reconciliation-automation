# Invoice Payment Reconciliation Automation

CLI-first Python portfolio project for reconciling invoice and payment exports
with deterministic local rules. It imports synthetic CSV or XLSX files,
validates rows, matches payments to invoices, categorizes exceptions, and writes
Markdown/CSV reports that can be reviewed without a database, deployment,
external API, paid service, or real client data.

## Business Problem

Small finance and operations teams often reconcile invoices and payments in
spreadsheets by hand. Manual reconciliation is slow, inconsistent, and difficult
to audit when exceptions need follow-up. This project demonstrates how a focused
local automation can turn structured exports into repeatable review artifacts
for a portfolio or client-style demo.

## Project Summary

The current version is a local CLI demo, not a production accounting platform.
It is designed to show practical automation engineering: file ingestion,
validation, deterministic matching, exception classification, report generation,
tests, and a minimal CI quality gate.

## Features

- CSV and XLSX invoice/payment input parsing.
- Required-field validation for invoice and payment rows.
- ISO date parsing and decimal money amount parsing.
- Whitespace trimming for text fields and uppercasing for currency values.
- Exact-reference matching between invoice IDs and payment references.
- Exception categories for invoices missing payments, payments missing
  invoices, amount variances, currency conflicts, and duplicate references.
- Markdown reconciliation report with totals, status summary, sorted detail
  sections, and review notes.
- Summary CSV and details CSV outputs for spreadsheet review.
- Synthetic sample data and committed Markdown/CSV demo-output snapshot.

## Demo Workflow

Use PowerShell from the repository root:

1. Install dependencies from the lockfile and run the quality gate.
2. Run the mixed CSV demo and inspect `reports\demo-csv`.
3. Run the equivalent XLSX demo and inspect `reports\demo-xlsx`.
4. Confirm each demo directory contains `reconciliation-report.md`,
   `reconciliation-summary.csv`, and `reconciliation-details.csv`.
5. Compare generated output with the committed reviewer snapshot under
   `docs/demo-output/mixed-demo/`.

## Installation

Prerequisite: install `uv` from the
[official uv installation guide](https://docs.astral.sh/uv/getting-started/installation/)
if it is not already available on `PATH`.

From a fresh clone:

```powershell
uv sync --locked --dev
```

## CLI Usage

Show top-level help:

```powershell
uv run reconcile --help
```

Show report command help:

```powershell
uv run reconcile report --help
```

Run the mixed CSV demo:

```powershell
uv run reconcile report --invoices sample-data/mixed-demo/invoices.csv --payments sample-data/mixed-demo/payments.csv --out-dir reports\demo-csv
```

Run the equivalent XLSX-input demo:

```powershell
uv run reconcile report --invoices sample-data/mixed-demo/invoices.xlsx --payments sample-data/mixed-demo/payments.xlsx --out-dir reports\demo-xlsx
```

Both demo commands write exactly three files inside the selected output
directory:

- `reconciliation-report.md`
- `reconciliation-summary.csv`
- `reconciliation-details.csv`

## Sample Inputs And Outputs

Synthetic inputs live under `sample-data/`:

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

Generated local reports belong under ignored `reports/` paths. The committed
`docs/demo-output/mixed-demo/` snapshot is a small reviewer-facing example
generated from the mixed CSV sample data:

- `docs/demo-output/mixed-demo/reconciliation-report.md`
- `docs/demo-output/mixed-demo/reconciliation-summary.csv`
- `docs/demo-output/mixed-demo/reconciliation-details.csv`

No XLSX report output or large binary report artifact is included.

## Quality Checks

Run the local quality gate before reviewing or changing the project:

```powershell
uv sync --locked --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run reconcile --help
uv run reconcile report --help
```

GitHub Actions mirrors this locked `uv` sync, pytest, Ruff checks, CLI help
smoke checks, and CSV/XLSX demo smoke commands on pull requests and pushes. The
workflow is CI-only; it does not deploy, upload artifacts, or use secrets.

## Limitations And Non-Goals

- No fuzzy matching or probabilistic matching.
- No partial-payment allocation or many-to-one matching.
- No Excel workbook report output.
- No web app, FastAPI service, database, deployment, or hosted runtime
  automation.
- No paid APIs, runtime external services, or real client data.
- Current normalization covers whitespace and currency casing; email
  normalization is not part of the current sample schema.

## Data And Security Posture

- Use fake sample data only.
- Do not use real client data.
- Do not commit secrets, credentials, or production exports.
- Keep generated local report artifacts under ignored `reports/` paths unless
  they are intentional Markdown/CSV examples under `docs/demo-output/`.
