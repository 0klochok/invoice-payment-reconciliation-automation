# State

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-06-30 |
| Repository root | `.` |
| Current branch | `main` |
| Current phase | README And Workbook Report Upgrade |
| Overall status | Complete |
| Quality gate status | Green |
| Completion | 100% |
| Main blocker | None |

## Current Objective

Update the public portfolio demo so the README opens with a stronger
client-facing story, the CLI generates an XLSX workbook report, and the
committed synthetic demo snapshot includes workbook and sheet-preview artifacts.

## Confirmed Scope

- In scope: README, source-of-truth docs, report generation code, CLI output
  text, tests, synthetic demo-output artifacts, and workbook sheet previews.
- In scope: local deterministic XLSX workbook report output using existing
  `openpyxl`.
- Out of scope: repository rename, commits, pushes, real accounting/banking/
  Stripe/client data, pandas, fuzzy matching, partial-payment allocation,
  databases, FastAPI, hosted web apps, schedulers, paid APIs, and production
  integrations.

## Completed In This Pass

- Cloned `0klochok/invoice-payment-reconciliation-automation` into
  `work\invoice-payment-reconciliation-automation` because the original working
  directory was not a Git checkout.
- Read `AGENTS.md`, `STATE.md`, and relevant docs before changing files:
  `README.md`, `RUNBOOK.md`, `DESIGN.md`, `REQ.md`, `TDD.md`, `CHANGELOG.md`,
  `SECURITY.md`, `sample-data/README.md`, `docs/demo-output/README.md`, and
  `docs/screenshots/README.md`.
- Confirmed `openpyxl` is already present in `pyproject.toml` and `uv.lock`.
  No dependency or lockfile change was needed.
- Confirmed `pandas` is not a project dependency and should not be claimed.
- Added XLSX workbook report generation to `reconcile report`.
- Updated CLI help and success output to list Markdown, CSV, and XLSX workbook
  reports.
- Updated pytest coverage for workbook creation, expected sheet names, summary
  values, mixed-demo exception values, and four-file output containment.
- Rewrote the README opening with a client-facing 60-second read, manual-vs-
  automated comparison, matching rules table, real-client adaptation notes,
  known limitations, and README-visible About/topics.
- Updated source-of-truth docs to remove stale "no workbook output" wording.
- Regenerated the synthetic mixed-demo output snapshot and added a workbook
  artifact.
- Generated PNG workbook sheet previews for `Summary`, `Exceptions`, and
  `Matched` from the synthetic workbook data.

## Changed In This Pass

| Path | Purpose | Status |
|---|---|---|
| `src/invoice_reconciliation/reporting.py` | Added deterministic workbook writer and workbook output path. | Updated |
| `src/invoice_reconciliation/cli.py` | Updated help and success output for workbook reports. | Updated |
| `tests/test_cli.py` | Checked CLI workbook output behavior. | Updated |
| `tests/test_reporting.py` | Added workbook sheet/value assertions. | Updated |
| `tests/test_sample_data.py` | Updated mixed-demo expectations for four files and workbook values. | Updated |
| `README.md` | Added client-facing opening, matching rules, limitations, screenshots, and About/topics. | Updated |
| `RUNBOOK.md`, `DESIGN.md`, `REQ.md`, `TDD.md`, `CHANGELOG.md`, `SECURITY.md`, `sample-data/README.md`, `docs/demo-output/README.md`, `docs/screenshots/README.md` | Aligned docs with workbook output and synthetic demo artifacts. | Updated |
| `docs/demo-output/mixed-demo/reconciliation-workbook.xlsx` | Added generated synthetic workbook snapshot. | Added |
| `docs/screenshots/workbook-summary.png`, `docs/screenshots/workbook-exceptions.png`, `docs/screenshots/workbook-matched.png` | Added generated workbook sheet previews. | Added |

## Generated Artifacts

- `docs/demo-output/mixed-demo/reconciliation-report.md`
- `docs/demo-output/mixed-demo/reconciliation-summary.csv`
- `docs/demo-output/mixed-demo/reconciliation-details.csv`
- `docs/demo-output/mixed-demo/reconciliation-workbook.xlsx`
- `docs/screenshots/workbook-summary.png`
- `docs/screenshots/workbook-exceptions.png`
- `docs/screenshots/workbook-matched.png`

## Validation And Quality Gates

| Command | Status | Result |
|---|---|---|
| `uv sync --locked --dev` | Pass | `Resolved 10 packages in 1ms`; `Checked 10 packages in 1ms`. |
| `uv run pytest` | Pass | `41 passed in 1.16s` on win32 with Python 3.13.14. |
| `uv run ruff check .` | Pass | `All checks passed!`. |
| `uv run ruff format --check .` | Pass | `12 files already formatted`. |
| `uv run reconcile --help` | Pass | Help text lists Markdown, CSV, and XLSX workbook reports. |
| `uv run reconcile report --help` | Pass | Report help text lists Markdown, CSV, and XLSX workbook reports. |
| `uv run reconcile report --invoices sample-data\mixed-demo\invoices.csv --payments sample-data\mixed-demo\payments.csv --out-dir reports\demo-csv` | Pass | Wrote Markdown, summary CSV, details CSV, and workbook XLSX. |
| `uv run reconcile report --invoices sample-data\mixed-demo\invoices.xlsx --payments sample-data\mixed-demo\payments.xlsx --out-dir reports\demo-xlsx` | Pass | Wrote Markdown, summary CSV, details CSV, and workbook XLSX. |
| `Get-ChildItem -Name -LiteralPath reports\demo-csv` | Pass | Listed `reconciliation-details.csv`, `reconciliation-report.md`, `reconciliation-summary.csv`, and `reconciliation-workbook.xlsx`. |
| `Get-ChildItem -Name -LiteralPath reports\demo-xlsx` | Pass | Listed `reconciliation-details.csv`, `reconciliation-report.md`, `reconciliation-summary.csv`, and `reconciliation-workbook.xlsx`. |
| `gh --version` | Not available | `gh` is not installed in this environment. |

## Known Issues And Deferred Work

- GitHub repository About/topics were not updated because `gh` is unavailable
  in this environment. The README includes the exact manual metadata guidance.
- Workbook sheet preview PNGs are generated table previews, not native Excel UI
  screenshots, because Pillow, matplotlib, LibreOffice, and `gh` were not
  available in the environment.
- Fuzzy matching, probabilistic matching, amount/date tolerance, partial-payment
  allocation, many-to-one matching, production accounting integrations,
  databases, hosted web apps, schedulers, paid APIs, runtime external services,
  and real client data remain out of scope.

## Git Policy

No staging, commit, push, reset, branch deletion, checkout, or history rewrite
operation was performed. The user manually validates, stages, commits, and
pushes when ready.
