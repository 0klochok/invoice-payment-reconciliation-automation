# Changelog

All notable project changes are recorded here.

## [Unreleased]

### Added

- Final public-repository readiness audit record.
- Public-repo presentation polish pass for README, RUNBOOK, STATE, sample-data,
  and demo-output review.
- Phase 12 final release-readiness audit record.
- Phase 11 final portfolio release hardening and evaluator walkthrough record.
- README evaluator walkthrough and concise business automation value summary for
  portfolio reviewers.
- Runbook cleanup command for removing ignored local demo report outputs before
  rerunning the CSV/XLSX walkthrough.
- Phase 10 final portfolio polish and release-readiness review record.
- Phase 9 minimal GitHub Actions CI workflow for pull requests and pushes to
  `main`, using `uv sync --locked --dev` and the documented local quality gate.
- Phase 7 generated Markdown/CSV demo-output snapshot under
  `docs/demo-output/mixed-demo/`, generated from existing mixed sample data for
  reviewer clarity.
- Phase 6 report polish tests for Markdown structure, omitted empty sections,
  deterministic status/reference ordering, underpaid/overpaid amount variance
  notes, and CLI success output.
- Phase 5 XLSX input support for invoice and payment files using `openpyxl`.
- Phase 5 mixed synthetic XLSX demo files equivalent to the deterministic mixed
  CSV demo scenario.
- Phase 5 XLSX sample-data and CLI smoke tests for parseability, expected
  mixed-demo status counts, CSV/XLSX record and count equivalence, and output
  containment.
- Phase 4 mixed synthetic demo CSV files covering matched records, unmatched
  invoices, unmatched payments, amount mismatches, currency mismatches, and
  ambiguous duplicate references.
- Phase 4 sample-data and CLI smoke tests for parseability, expected mixed-demo
  status counts, and output containment under the requested report directory.
- Phase 3 deterministic Markdown reconciliation report generation.
- Phase 3 summary and detail CSV report generation for spreadsheet review.
- `reconcile report` CLI command for loading CSV inputs, running deterministic
  matching, and writing local report files.
- Reporting test coverage for Markdown, CSV, summary counts, status labels,
  deterministic ordering, input immutability, and CLI output path behavior.
- Phase 2 deterministic matching engine for normalized invoice and payment
  records.
- Matching result structures for exact matches, unmatched invoices, unmatched
  payments, amount mismatches, currency mismatches, and ambiguous references.
- Explicit matching status values and duplicate-reference ambiguity reasons.
- Phase 2 matching test coverage for successful matches, exceptions,
  deterministic ordering, input immutability, and Phase 1 CSV integration.
- Phase 1 invoice/payment domain models and import diagnostics.
- Dependency-free CSV ingestion for invoices and payments.
- Required-field, ISO date, decimal amount, whitespace, and currency
  normalization validation.
- Synthetic valid and invalid invoice/payment CSV sample files.
- Phase 1 ingestion test coverage for valid rows, invalid rows, normalization,
  and deterministic validation errors.
- Phase 0 repository foundation.
- uv-managed Python project configuration.
- Minimal `invoice_reconciliation` package and `reconcile` CLI entry point.
- Baseline pytest and Ruff configuration.
- Package import and CLI help smoke tests.
- Source-of-truth project docs.
- Initial directories for sample data, reports, and screenshots.

### Changed

- Mixed demo sample inputs now live under `sample-data/mixed-demo/` with concise
  `invoices` and `payments` filenames for the public evaluator walkthrough.
- README now presents a concise implementation status section instead of a long
  internal phase roadmap.
- README now includes a dedicated supported inputs/outputs section and states
  that GitHub Actions is CI-only, with no deployment, artifacts, or secrets.
- RUNBOOK now includes fresh-clone prerequisites and uses the locked sync command
  in troubleshooting.
- STATE now avoids recording a machine-specific absolute clone path.
- RUNBOOK setup instructions now describe entering the repository root without a
  machine-specific absolute clone path.
- Removed redundant tracked `.manual-validation` report snapshots; the committed
  `docs/demo-output/mixed-demo/` snapshot remains the canonical reviewer sample.
- AGENTS quality-gate commands now match the current locked setup step,
  `reconcile report` CLI shape, and mixed CSV/XLSX demo sample paths.
- README, runbook, and test strategy now document
  `uv sync --locked --dev` as the local release-readiness sync step.
- Phase 8 records the final local release-readiness review, including clean demo
  output regeneration, ignored-artifact verification, repository hygiene review,
  and current quality-gate results.
- README, runbook, sample-data notes, requirements, design, and test strategy now
  present the current local CLI demo behavior with exact demo commands, expected
  output files, limitations, and non-goals.
- Markdown reports now include reconciliation totals, clearer status labels,
  sorted detail sections, and exception review notes.
- Summary and details CSV reports now use clearer exception labels and detail
  reasons for unmatched, amount variance, currency conflict, and duplicate
  reference rows.
- `reconcile report` success output now groups the generated Markdown and CSV
  file paths under a concise `Report files written:` heading.
- CLI report input help now accepts CSV or XLSX invoice and payment files while
  preserving Markdown/CSV report output behavior.
- README, runbook, and sample-data notes now include concise Phase 5 XLSX demo
  commands.
- README, runbook, and sample-data notes now include a concise Phase 4 mixed
  demo walkthrough.
- CLI help text no longer names a completed phase in the top-level description.
- README, requirements, design, test strategy, and runbook now describe Phase 3
  Markdown/CSV reporting and the local report CLI command.
- README, requirements, design, test strategy, runbook, and security notes now
  describe Phase 2 matching scope.
- README, requirements, design, test strategy, runbook, and sample-data notes now
  describe Phase 1 CSV ingestion scope.

### Fixed

- Added the initial `sample-data/` note clarifying that sample files were not
  part of the Phase 0 scaffold.

### Security

- Added repository security policy for synthetic data, no secrets, no paid APIs,
  no AI calls, and no deployment in Phase 0.
- Added `.gitignore` coverage for local secrets, caches, virtual environments,
  and generated reports.

### Known Issues

- Fuzzy matching and many-to-one payment allocation are intentionally not
  implemented.
