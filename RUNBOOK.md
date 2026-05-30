# Runbook

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-30 |
| Status | Active |
| Project | invoice-payment-reconciliation-automation-new |
| Environment | Windows 11, PowerShell, uv, Python 3.12+ |

## Setup

Open PowerShell and enter the repository root:

```powershell
Set-Location -LiteralPath "C:\Users\Санька\Documents\Coding Projects\Portfolio Projects\invoice-payment-reconciliation-automation-new"
uv sync
```

## Quality Gate

Run the default validation commands:

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run reconcile --help
uv run reconcile report --help
```

## Demo Commands

Run the CSV-input portfolio demo:

```powershell
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo-csv
```

Run the XLSX-input portfolio demo:

```powershell
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\demo-xlsx
```

Each command prints a `Report files written:` message and writes exactly three
files in the selected output directory:

- `reconciliation-report.md`
- `reconciliation-summary.csv`
- `reconciliation-details.csv`

Verify the output file list:

```powershell
Get-ChildItem -Name -LiteralPath reports\demo-csv
Get-ChildItem -Name -LiteralPath reports\demo-xlsx
```

Inspect the Markdown report:

```powershell
Get-Content -Raw -LiteralPath reports\demo-csv\reconciliation-report.md
```

Confirm CSV-input and XLSX-input report content equivalence:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath reports\demo-csv\reconciliation-report.md, reports\demo-xlsx\reconciliation-report.md
Get-FileHash -Algorithm SHA256 -LiteralPath reports\demo-csv\reconciliation-summary.csv, reports\demo-xlsx\reconciliation-summary.csv
Get-FileHash -Algorithm SHA256 -LiteralPath reports\demo-csv\reconciliation-details.csv, reports\demo-xlsx\reconciliation-details.csv
```

The matching hashes should be identical for each corresponding file.

## Current CLI Behavior

The `reconcile` command supports help, version output, and a local report
workflow. The report command loads invoice and payment CSV or XLSX files, runs
deterministic exact-reference matching, and writes local Markdown and CSV
reports.

```powershell
uv run reconcile --version
uv run reconcile report --invoices sample-data/valid-invoices.csv --payments sample-data/valid-payments.csv --out-dir reports\clean
```

The Markdown report includes:

- Reconciliation totals.
- Status summary counts.
- Matched records.
- Invoices missing payments.
- Payments missing invoices.
- Amount variances with underpaid/overpaid notes.
- Currency conflicts.
- Duplicate references needing review.

The summary CSV contains one row per status. The details CSV contains sorted
detail rows with stable status values, readable status labels, source row
numbers, and exception review notes.

## Example Output Snapshot

The repository includes a small generated example under
`docs/demo-output/mixed-demo/`. It was generated from the mixed CSV sample data
and contains only Markdown and CSV report examples:

- `docs/demo-output/mixed-demo/reconciliation-report.md`
- `docs/demo-output/mixed-demo/reconciliation-summary.csv`
- `docs/demo-output/mixed-demo/reconciliation-details.csv`

Use this snapshot for quick reviewer inspection. Use the `reports/` directory
for local generated output during demos.

## Sample Data

Synthetic CSV and XLSX files live in `sample-data/`:

```powershell
Get-ChildItem -LiteralPath sample-data
```

The clean `valid-*` files produce only matched records. The `demo-mixed-*`
files produce the main portfolio scenario with matched records, unmatched
records, amount variance, currency conflict, and duplicate-reference exceptions.
The mixed CSV and XLSX inputs are intentionally equivalent.

## Data Handling

- Use `sample-data/` for synthetic demo inputs only.
- Use `reports/` for generated local outputs.
- Generated report files under `reports/` are ignored by Git.
- Only intentional Markdown/CSV examples belong under `docs/demo-output/`.
- Real client data, production exports, secrets, credentials, and private
  information must not be stored in this repository.

## Manual Commit Policy

Codex must not stage, unstage, commit, push, reset, or rewrite Git history. After
manual review, the user may run Git commands to stage, commit, and push.

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
| `reconcile report` returns import errors | Input rows are invalid | Use the synthetic samples or fix the demo input |
| Ruff format check fails | A Python file needs formatting | Run `uv run ruff format .`, then rerun gates |
| Tests fail | Behavior or environment issue | Stop, inspect the failure, update `STATE.md` |
