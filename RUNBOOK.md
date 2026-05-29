# Runbook

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-29 |
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

Run the default Phase 3 quality gate:

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Optional CLI smoke check:

```powershell
uv run reconcile --help
uv run reconcile report --invoices sample-data/valid-invoices.csv --payments sample-data/valid-payments.csv --out-dir reports
```

## Current CLI Behavior

The `reconcile` command supports help, version output, and a local CSV report
workflow. The report command loads invoice and payment CSV files, runs
deterministic matching, and writes local Markdown and CSV reports.

```powershell
uv run reconcile --help
uv run reconcile --version
uv run reconcile report --invoices sample-data/valid-invoices.csv --payments sample-data/valid-payments.csv --out-dir reports
```

The report command writes:

- `reports/reconciliation-report.md`
- `reports/reconciliation-summary.csv`
- `reports/reconciliation-details.csv`

## Sample Data

Synthetic CSV files live in `sample-data/`:

```powershell
Get-ChildItem -LiteralPath sample-data
```

Phase 1 includes valid and invalid invoice/payment CSV samples. Phase 2 matching
tests and the Phase 3 report command reuse the valid normalized CSV samples.
XLSX sample inputs are deferred until XLSX support is implemented.

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
