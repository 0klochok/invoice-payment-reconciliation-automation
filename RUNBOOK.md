# Runbook

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-30 |
| Status | Active draft |
| Project | invoice-payment-reconciliation-automation-new |
| Environment | Windows 11, PowerShell, uv, Python 3.12+ |

## Setup

Open PowerShell and enter the repository root:

```powershell
Set-Location -LiteralPath "C:\Users\Санька\Documents\Coding Projects\Portfolio Projects\invoice-payment-reconciliation-automation-new"
git status --short
uv sync
```

## Validate

Run the default quality gate:

```powershell
uv sync
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

CLI smoke checks:

```powershell
uv run reconcile --help
uv run reconcile report --invoices sample-data/valid-invoices.csv --payments sample-data/valid-payments.csv --out-dir reports\clean
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\xlsx-demo
```

Temporary-output smoke check:

```powershell
$DemoOut = Join-Path $env:TEMP "invoice-reconciliation-phase5-csv-demo"
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir $DemoOut
Get-ChildItem -LiteralPath $DemoOut
```

XLSX temporary-output smoke check:

```powershell
$XlsxDemoOut = Join-Path $env:TEMP "invoice-reconciliation-phase5-xlsx-demo"
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir $XlsxDemoOut
Get-ChildItem -LiteralPath $XlsxDemoOut
```

## Current CLI Behavior

The `reconcile` command supports help, version output, and a local report
workflow. The report command loads invoice and payment CSV or XLSX files, runs
deterministic matching, and writes local Markdown and CSV reports.

```powershell
uv run reconcile --help
uv run reconcile --version
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\xlsx-demo
```

The report command writes:

- `reports\demo\reconciliation-report.md`
- `reports\demo\reconciliation-summary.csv`
- `reports\demo\reconciliation-details.csv`

The Markdown report includes reconciliation totals, a status summary, sorted
matched records, and sorted exception sections. Exception rows use
client-readable categories such as invoice missing payment, payment missing
invoice, amount variance, currency conflict, and duplicate reference needing
review. The details CSV uses the same status labels and includes a `reason`
column with review notes such as underpaid/overpaid amount variance details.

## Sample Data

Synthetic CSV and XLSX files live in `sample-data/`:

```powershell
Get-ChildItem -LiteralPath sample-data
```

Phase 1 includes valid and invalid invoice/payment CSV samples. Phase 2 matching
tests and the Phase 3 report command reuse the valid normalized CSV samples.
Phase 4 adds mixed CSV demo samples that produce matched records, unmatched
invoices, unmatched payments, amount mismatches, currency mismatches, and
ambiguous duplicate references. Phase 5 adds XLSX equivalents for the mixed demo
inputs.

## Data Handling

- Use `sample-data/` for synthetic demo inputs only.
- Use `reports/` for generated local outputs.
- Generated report files are ignored by Git.
- Real client data, production exports, and secrets must not be stored in this
  repository.

## Manual Commit Policy

Codex must not commit or push. After manual review, the user may run Git
commands to stage, commit, and push.

Before committing manually, review:

```powershell
git status --short
git diff -- .
```

## Troubleshooting

| Symptom | Likely Cause | Action |
|---|---|---|
| `uv` is not recognized | uv is not installed or not on PATH | Install uv and reopen PowerShell |
| `reconcile` is not found | Environment is not synced | Run `uv sync` from the repository root |
| `reconcile report` returns import errors | The input CSV has invalid rows | Fix the synthetic input or use the valid sample files |
| Ruff format check fails | A Python file needs formatting | Run `uv run ruff format .`, then rerun gates |
| Tests fail | Scaffold or environment issue | Stop, inspect the failure, update `STATE.md` |
