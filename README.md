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
- Generate Excel and Markdown reconciliation reports for review.

## Current Status

Phase 2 adds deterministic matching on top of the ingestion foundation:

- Immutable invoice, payment, money amount, and import diagnostic models.
- Dependency-free CSV loading with Python's standard library `csv` module.
- Required-field validation, ISO date parsing, decimal amount parsing,
  whitespace trimming, and currency uppercasing.
- Deterministic exact-reference payment-to-invoice matching.
- Explicit exception classifications for unmatched records, amount mismatches,
  currency mismatches, and ambiguous duplicate references.
- Synthetic CSV files under `sample-data/`.

Report generation, CLI file orchestration, fuzzy matching, and XLSX loading are
intentionally not implemented yet.

## Quickstart

Use PowerShell from the repository root.

```powershell
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run reconcile --help
```

The `reconcile` command currently exposes help and version output only. Phase 2
CSV ingestion and matching are available as package functionality and covered by
tests.

## Sample Data

Synthetic CSV files are available for local demos and tests:

- `sample-data/valid-invoices.csv`
- `sample-data/valid-payments.csv`
- `sample-data/invalid-invoices.csv`
- `sample-data/invalid-payments.csv`

## Roadmap

| Phase | Objective | Status |
|---|---|---|
| Phase 0 | Repository foundation, docs, project skeleton, quality tooling | Complete |
| Phase 1 | Input schemas, sample data, CSV loading, normalization, validation | Complete |
| Phase 2 | Matching engine and exception classification | Complete |
| Phase 3 | Excel and Markdown report generation | Planned |
| Phase 4 | CLI workflow polish and demo runbook | Planned |

## Safety and Data Policy

- Use fake sample data only.
- Do not use real client data.
- Do not commit secrets or local credentials.
- No paid APIs, AI calls, deployment, database, FastAPI, or GitHub Actions are
  included in the current local-demo scope.
