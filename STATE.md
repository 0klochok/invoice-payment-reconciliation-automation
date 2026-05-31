# State

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-31 |
| Repository root | `.` |
| Current branch | `main` |
| Current phase | Demo Output Snapshot Guard |
| Overall status | Complete |
| Quality gate status | Green after rerun |
| Completion | 100% |
| Main blocker | None |

## Current Objective

Add a focused automated regression test that regenerates the mixed CSV demo
report into a pytest temporary directory and compares the generated Markdown and
CSV outputs against the committed reviewer snapshot under
`docs/demo-output/mixed-demo/`.

## Confirmed Scope

- In scope: `tests/test_sample_data.py`, `STATE.md`, `TDD.md`,
  `CHANGELOG.md`, and `docs/demo-output/README.md`.
- In scope: pytest coverage that uses `tmp_path`, invokes the existing
  in-process CLI report flow, asserts the exact generated report file set, and
  compares generated content to the committed mixed-demo snapshot.
- Out of scope: source behavior changes, CLI shape changes, report format
  changes, dependency changes, sample input changes, committed demo-output
  snapshot regeneration, deployment, databases, FastAPI, paid APIs, secrets,
  staging, commits, pushes, resets, checkouts, branch deletion, and history
  rewrites.

## Completed In This Pass

- Read `AGENTS.md`, `STATE.md`, and relevant source-of-truth docs before
  changing files: `README.md`, `RUNBOOK.md`, `REQ.md`, `DESIGN.md`, `TDD.md`,
  `CHANGELOG.md`, `SECURITY.md` from prior context where applicable, and
  `docs/demo-output/README.md`.
- Inspected `pyproject.toml`, `src/`, `tests/`, `sample-data/mixed-demo/`, and
  `docs/demo-output/mixed-demo/`.
- Confirmed the requested phase is Demo Output Snapshot Guard, with test-only
  regression coverage and documentation/state updates in scope.
- Added a focused pytest guard that runs `reconcile report` in process against
  `sample-data/mixed-demo/invoices.csv` and
  `sample-data/mixed-demo/payments.csv`, writing to `tmp_path`.
- The guard asserts the generated file set is exactly
  `reconciliation-report.md`, `reconciliation-summary.csv`, and
  `reconciliation-details.csv`.
- The guard compares generated Markdown and CSV contents against the committed
  `docs/demo-output/mixed-demo/` snapshot without mutating snapshot files.
- Updated test strategy, changelog, and demo-output snapshot docs to describe
  the new regression guard.
- No source behavior, CLI shape, report format, dependencies, sample inputs, or
  committed demo-output snapshot files were changed.

## Changed In This Pass

| Path | Purpose | Status |
|---|---|---|
| `tests/test_sample_data.py` | Added the mixed CSV demo snapshot regression guard. | Updated |
| `TDD.md` | Documented the new snapshot guard in the test strategy. | Updated |
| `CHANGELOG.md` | Recorded the new automated regression guard. | Updated |
| `docs/demo-output/README.md` | Noted that the committed snapshot is regression-tested. | Updated |
| `STATE.md` | Recorded phase scope, changes, validation, and known issues. | Updated |

## Validation And Quality Gates

| Command | Status | Result |
|---|---|---|
| `git status --short --untracked-files=all` | Pass | Initial output was empty; working tree started clean. |
| `uv run pytest tests\test_sample_data.py -q` | Pass | `12 passed in 0.57s`; the new snapshot guard passed, so the committed snapshot is current. |
| `uv sync --locked --dev` | Pass | `Resolved 10 packages in 2ms`; `Checked 10 packages in 1ms`. |
| `uv run pytest` | Pass | `40 passed in 0.54s` on win32 with Python 3.14.4. |
| `uv run ruff check .` | Fail, fixed | First run failed with `E501 Line too long` in `tests/test_sample_data.py`; the constant was wrapped and the command was rerun. |
| `uv run ruff check .` | Pass | Rerun output: `All checks passed!`. |
| `uv run ruff format --check .` | Pass | `12 files already formatted`. |
| `uv run reconcile --help` | Pass | Printed top-level usage for `reconcile [-h] [--version] {report} ...`. |
| `uv run reconcile report --help` | Pass | Printed report usage with required `--invoices`, `--payments`, and `--out-dir` options. |
| `uv run reconcile report --invoices sample-data/mixed-demo/invoices.csv --payments sample-data/mixed-demo/payments.csv --out-dir reports\demo-csv` | Pass | Wrote Markdown, summary CSV, and details CSV under ignored `reports\demo-csv`. |
| `uv run reconcile report --invoices sample-data/mixed-demo/invoices.xlsx --payments sample-data/mixed-demo/payments.xlsx --out-dir reports\demo-xlsx` | Pass | Wrote Markdown, summary CSV, and details CSV under ignored `reports\demo-xlsx`. |
| `Get-ChildItem -Name -LiteralPath reports\demo-csv` | Pass | Listed only `reconciliation-details.csv`, `reconciliation-report.md`, and `reconciliation-summary.csv`. |
| `Get-ChildItem -Name -LiteralPath reports\demo-xlsx` | Pass | Listed only `reconciliation-details.csv`, `reconciliation-report.md`, and `reconciliation-summary.csv`. |
| `git status --short --untracked-files=all` | Pass | Shows only modified `CHANGELOG.md`, `TDD.md`, `docs/demo-output/README.md`, `tests/test_sample_data.py`, and `STATE.md`. |

## Issues Found

- A transient Ruff `E501` failure was introduced by the initial snapshot path
  constant. It was fixed by wrapping the constant, and Ruff passed on rerun.

## Known Issues And Deferred Work

- No known blocker remains for this phase.
- Ignored local report artifacts were regenerated under `reports\demo-csv` and
  `reports\demo-xlsx` by the required validation commands; they remain outside
  the committed demo-output snapshot.
- Screenshots remain intentionally absent. Add real manual screenshots later
  only from synthetic demo data and generated report views.
- Excel workbook report output remains deferred until a later phase explicitly
  approves it.
- Fuzzy matching, partial-payment allocation, overpayment/underpayment policy
  beyond report notes for one-to-one amount mismatches, and many-to-one
  matching remain deferred.

## Git Policy

No staging, commit, push, reset, branch deletion, checkout, or history rewrite
operation was performed. The user manually validates, stages, commits, and
pushes when ready.
