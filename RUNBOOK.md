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

Run the default Phase 1 quality gate:

```powershell
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

Optional CLI smoke check:

```powershell
uv run reconcile --help
```

## Current CLI Behavior

The `reconcile` command exists, but Phase 1 still supports help and version
output only. CSV ingestion is implemented as package functionality and covered
by tests. Do not expect invoice or payment CLI arguments to work until a later
workflow phase.

```powershell
uv run reconcile --help
uv run reconcile --version
```

## Sample Data

Synthetic CSV files live in `sample-data/`:

```powershell
Get-ChildItem -LiteralPath sample-data
```

Phase 1 includes valid and invalid invoice/payment CSV samples. XLSX sample
inputs are deferred until XLSX support is implemented.

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
| Ruff format check fails | A Python file needs formatting | Run `uv run ruff format .`, then rerun gates |
| Tests fail | Scaffold or environment issue | Stop, inspect the failure, update `STATE.md` |
