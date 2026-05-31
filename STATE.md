# State

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-31 |
| Repository root | `.` |
| Current branch | `main` |
| Current phase | Final public-release readiness audit |
| Overall status | Complete |
| Quality gate status | Green |
| Completion | 100% |
| Main blocker | None |

## Current Objective

Perform a final public-release readiness audit for the portfolio/demo
repository. Keep the project CLI-first, local-demo-first, synthetic-data-only,
and avoid source-code behavior changes, generated committed output
regeneration, paid APIs, external services, secrets, telemetry, deployment,
staging, commits, or pushes.

## Confirmed Scope

- In scope: `README.md`, `REQ.md`, `DESIGN.md`, `TDD.md`, `RUNBOOK.md`,
  `CHANGELOG.md`, `SECURITY.md`, `STATE.md`, `AGENTS.md`,
  `docs/demo-output/README.md`, `docs/screenshots/README.md`,
  `pyproject.toml`, `.gitignore`, public wording, documented commands,
  repository hygiene, tracked generated artifacts, and validation output.
- Out of scope: source-code behavior changes, reconciliation behavior changes,
  test behavior changes, dependency changes, lockfile changes, sample-data
  changes, committed demo-output regeneration, screenshots, paid APIs, runtime
  external services, secrets, telemetry, databases, FastAPI, deployment,
  staging, commits, pushes, resets, branch deletion, and history rewrites.

## Completed In This Pass

- Read `AGENTS.md` and `STATE.md` before changing files.
- Read the public-release source-of-truth docs in scope:
  `README.md`, `REQ.md`, `DESIGN.md`, `TDD.md`, `RUNBOOK.md`,
  `CHANGELOG.md`, `SECURITY.md`, `docs/demo-output/README.md`,
  `docs/screenshots/README.md`, `pyproject.toml`, and `.gitignore`.
- Confirmed the requested phase is a final public-release readiness audit with
  documentation-only, low-risk fixes permitted.
- Audited public-facing docs for inaccurate commands, stale future-scope
  wording, unsupported claims, misleading setup/demo instructions, and
  references to real data, secrets, paid APIs, production systems, telemetry,
  deployment, fabricated screenshots, or runtime external services.
- Verified tracked files include only intentional sample data, source, tests,
  docs, the minimal CI workflow, `reports/.gitkeep`, and the committed
  Markdown/CSV demo-output snapshot.
- Verified generated local report artifacts under `reports/` are ignored and
  not tracked.
- Verified `docs/screenshots/` contains no fabricated screenshots.
- Verified the committed demo-output Markdown/CSV snapshot matches freshly
  generated CSV demo output.
- Verified freshly generated CSV and XLSX demo outputs are equivalent.
- Found and fixed one stale `TDD.md` future-work wording issue that implied
  mixed-currency coverage was still missing even though currency mismatch
  behavior and tests already exist.
- No source code, tests, dependencies, lockfiles, sample data, reconciliation
  behavior, committed demo-output snapshots, screenshots, or Git history were
  changed.

## Changed In This Pass

| Path | Purpose | Status |
|---|---|---|
| `TDD.md` | Replaced stale future-test wording for mixed currency coverage with approved future behavior examples. | Updated |
| `CHANGELOG.md` | Recorded the test-strategy wording fix. | Updated |
| `STATE.md` | Recorded this final public-release readiness audit and validation results. | Updated |

## Validation And Quality Gates

| Command | Status | Result |
|---|---|---|
| `uv sync --locked --dev` | Pass | `Resolved 10 packages in 1ms`; `Checked 10 packages in 3ms`. |
| `uv run pytest` | Pass | `39 passed in 0.54s` on win32 with Python 3.14.4. |
| `uv run ruff check .` | Pass | `All checks passed!`. |
| `uv run ruff format --check .` | Pass | `12 files already formatted`. |
| `uv run reconcile --help` | Pass | Printed top-level usage for `reconcile [-h] [--version] {report} ...`. |
| `uv run reconcile report --help` | Pass | Printed report usage with required `--invoices`, `--payments`, and `--out-dir` options. |
| `uv run reconcile report --invoices sample-data/mixed-demo/invoices.csv --payments sample-data/mixed-demo/payments.csv --out-dir reports\demo-csv` | Pass | Wrote Markdown, summary CSV, and details CSV under ignored `reports\demo-csv`. |
| `uv run reconcile report --invoices sample-data/mixed-demo/invoices.xlsx --payments sample-data/mixed-demo/payments.xlsx --out-dir reports\demo-xlsx` | Pass | Wrote Markdown, summary CSV, and details CSV under ignored `reports\demo-xlsx`. |
| `Get-ChildItem -Name -LiteralPath reports\demo-csv` | Pass | Listed only `reconciliation-details.csv`, `reconciliation-report.md`, and `reconciliation-summary.csv`. |
| `Get-ChildItem -Name -LiteralPath reports\demo-xlsx` | Pass | Listed only `reconciliation-details.csv`, `reconciliation-report.md`, and `reconciliation-summary.csv`. |
| Per-file `git diff --no-index --quiet` comparisons between `docs/demo-output/mixed-demo/` and `reports/demo-csv/` | Pass | Committed snapshot content matches regenerated CSV demo output; Git emitted LF-to-CRLF warnings only. |
| Per-file `git diff --no-index --quiet` comparisons between `reports/demo-csv/` and `reports/demo-xlsx/` | Pass | CSV-input and XLSX-input demo outputs match; Git emitted LF-to-CRLF warnings only. |
| Secret-pattern search with `rg` | Pass | No secret-like tokens, keys, or credential assignments found. |
| `git diff --check` | Pass | No whitespace errors found; Git emitted LF-to-CRLF warnings only. |
| `git status --short` | Pass | Shows only documentation changes: `CHANGELOG.md`, `STATE.md`, and `TDD.md`. |

## Issues Found

- Stale public test-strategy wording in `TDD.md` listed mixed currency handling
  as future test work even though currency mismatch behavior and tests are
  already implemented.

## Known Issues And Deferred Work

- No public-release blocker remains from this audit.
- Screenshots remain intentionally absent. Add real manual screenshots later
  only from synthetic demo data and generated report views.
- Excel workbook report output remains deferred until a later phase explicitly
  approves it.
- Fuzzy matching, partial-payment allocation, overpayment/underpayment policy
  beyond report notes for one-to-one amount mismatches, and many-to-one
  matching remain deferred.
- Ignored local report artifacts already exist under `reports/`; they are not
  tracked and were not promoted into committed demo output.

## Git Policy

No staging, commit, push, reset, branch deletion, checkout, or history rewrite
operation was performed. The user manually validates, stages, commits, and
pushes when ready.
