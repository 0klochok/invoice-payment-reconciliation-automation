# State

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-30 23:11 +03:00 |
| Repository root | `.` |
| Current branch | `main` |
| Current phase | Final public GitHub maintainer pass |
| Overall status | Complete |
| Quality gate status | Green |
| Completion | 100% |
| Main blocker | None |

## Current Objective

Perform a final public GitHub quality and evaluator-clarity pass for the
portfolio version. Review public docs, sample data, tests, demo-output examples,
ignored generated artifacts, and the required local quality gate without
changing reconciliation behavior.

## Confirmed Scope

- In scope: `README.md`, `RUNBOOK.md`, `CHANGELOG.md`, `STATE.md`,
  `AGENTS.md`, `pyproject.toml`, `.gitignore`, `sample-data/`, `tests/`,
  source-of-truth docs, committed demo-output examples, CLI help, documented
  CSV/XLSX demo commands, and repository hygiene.
- Out of scope: reconciliation logic changes, ingestion behavior changes,
  report-generation behavior changes, dependencies, FastAPI, databases,
  deployment, paid APIs, AI calls, real client data, XLSX report output,
  staging, commits, pushes, resets, branch deletion, and history rewrites.

## Completed In This Pass

- Read `AGENTS.md` and `STATE.md` before editing.
- Reviewed `README.md`, `RUNBOOK.md`, `CHANGELOG.md`, `REQ.md`, `DESIGN.md`,
  `TDD.md`, `SECURITY.md`, `sample-data/README.md`, `.gitignore`,
  `pyproject.toml`, `.github/workflows/ci.yml`, sample-data paths, selected
  tests, and committed demo-output files.
- Confirmed the current requested phase is a final public GitHub maintainer pass
  focused on evaluator clarity and repository readiness.
- Confirmed no reconciliation, ingestion, matching, or report-output behavior
  changes were needed.
- Found that the requested evaluator demo commands used
  `sample-data/mixed-demo/...` paths while the repository still used flat
  `sample-data/demo-mixed-*` filenames.
- Moved the existing synthetic mixed demo inputs into `sample-data/mixed-demo/`
  with concise invoice/payment filenames and updated docs/tests/CI references.
- Confirmed the CSV and XLSX demo commands write exactly the expected Markdown,
  summary CSV, and details CSV files under ignored `reports/` paths.
- Scanned project text for absolute local paths and common secret-like patterns;
  none were found.
- Scanned for stale placeholder and forbidden-scope terms. Matches were policy
  statements or explicit non-goals, not implementation claims.
- Confirmed no paid API, AI, deployment, database, FastAPI, real-client-data, or
  XLSX-report-output behavior was added.

## Changed In This Pass

| Path | Purpose | Status |
|---|---|---|
| `.github/workflows/ci.yml` | Updates CI demo smoke commands to the public mixed-demo sample paths. | Updated |
| `AGENTS.md` | Updates release-readiness demo commands to the public mixed-demo sample paths. | Updated |
| `CHANGELOG.md` | Records the mixed-demo sample path clarity change. | Updated |
| `DESIGN.md` | Updates the repository tree to show `sample-data/mixed-demo/`. | Updated |
| `README.md` | Updates evaluator demo commands and expected mixed-demo sample paths. | Updated |
| `RUNBOOK.md` | Updates demo commands and sample-data walkthrough wording. | Updated |
| `TDD.md` | Updates required demo command examples to the public mixed-demo sample paths. | Updated |
| `sample-data/README.md` | Documents the mixed-demo directory and concise input filenames. | Updated |
| `sample-data/mixed-demo/invoices.csv` | Synthetic mixed invoice CSV input moved from the old flat filename. | Moved |
| `sample-data/mixed-demo/payments.csv` | Synthetic mixed payment CSV input moved from the old flat filename. | Moved |
| `sample-data/mixed-demo/invoices.xlsx` | Synthetic mixed invoice XLSX input moved from the old flat filename. | Moved |
| `sample-data/mixed-demo/payments.xlsx` | Synthetic mixed payment XLSX input moved from the old flat filename. | Moved |
| `tests/test_sample_data.py` | Updates sample-data tests to use the public mixed-demo paths. | Updated |
| `STATE.md` | Records this maintainer pass, validations, and remaining known issues. | Updated |

## Validation And Quality Gates

| Command | Status | Result |
|---|---|---|
| `uv sync --locked --dev` | Pass | `Resolved 10 packages in 1ms`; `Checked 10 packages in 1ms`. |
| `uv run pytest` | Pass | `39 passed in 0.76s` on win32 with Python 3.14.4. |
| `uv run ruff check .` | Pass | `All checks passed!`. |
| `uv run ruff format --check .` | Pass | `12 files already formatted`. |
| `uv run reconcile --help` | Pass | Printed top-level usage for `reconcile [-h] [--version] {report} ...`. |
| `uv run reconcile report --help` | Pass | Printed report usage with required `--invoices`, `--payments`, and `--out-dir` options. |
| `uv run reconcile report --invoices sample-data/mixed-demo/invoices.csv --payments sample-data/mixed-demo/payments.csv --out-dir reports/demo-csv` | Pass | Wrote Markdown, summary CSV, and details CSV under `reports\demo-csv`. |
| `uv run reconcile report --invoices sample-data/mixed-demo/invoices.xlsx --payments sample-data/mixed-demo/payments.xlsx --out-dir reports/demo-xlsx` | Pass | Wrote Markdown, summary CSV, and details CSV under `reports\demo-xlsx`. |
| `git diff --check` | Pass | No whitespace errors found; Git reported expected Windows LF/CRLF working-copy warnings for edited text files. |
| `git status --short --ignored` | Pass | Shows the edited files, moved mixed-demo sample inputs, and ignored local caches/generated report artifacts. |

## Output File Checks

| Path | Files Present |
|---|---|
| `reports\demo-csv` | `reconciliation-details.csv`, `reconciliation-report.md`, `reconciliation-summary.csv` |
| `reports\demo-xlsx` | `reconciliation-details.csv`, `reconciliation-report.md`, `reconciliation-summary.csv` |

## Repository Hygiene Findings

- No absolute local paths were found in reviewed project text.
- No common secret-like values were found in reviewed project text.
- No stale placeholder filler was found.
- References to real client data, paid APIs, AI calls, deployment, databases,
  and FastAPI are policy statements or explicit non-goals.
- Generated local report artifacts under `reports/` are ignored by Git.
- The committed `docs/demo-output/mixed-demo/` snapshot remains the only
  intentional generated report example.
- No XLSX report output was added.

## Known Issues And Deferred Work

- No public-repository readiness blockers were found.
- Running the documented demo commands regenerated ignored local report
  artifacts under `reports\demo-csv` and `reports\demo-xlsx`.
- Pre-existing ignored local artifacts remain visible in `git status --ignored`,
  including caches, `.venv/`, and older ignored report directories.
- Excel workbook report output remains deferred until a later phase explicitly
  approves it.
- Fuzzy matching, partial payment allocation, overpayment/underpayment policy
  beyond report notes for one-to-one amount mismatches, and many-to-one matching
  remain deferred.

## Next Step

Manual review of this final maintainer-pass change set. The user manually
validates, stages, commits, and pushes when ready. No commit, push, staging,
reset, branch deletion, or history rewrite has been performed.
