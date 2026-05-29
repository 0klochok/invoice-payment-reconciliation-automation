# Changelog

All notable project changes are recorded here.

## [Unreleased]

### Added

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
- Placeholder directories for sample data, reports, and screenshots.

### Changed

- README, requirements, design, test strategy, and runbook now describe Phase 3
  Markdown/CSV reporting and the local report CLI command.
- README, requirements, design, test strategy, runbook, and security notes now
  describe Phase 2 matching scope.
- README, requirements, design, test strategy, runbook, and sample-data notes now
  describe Phase 1 CSV ingestion scope.

### Fixed

- Added a visible `sample-data/` placeholder note clarifying that Phase 0 does
  not include CSV or XLSX sample files.

### Security

- Added repository security policy for synthetic data, no secrets, no paid APIs,
  no AI calls, and no deployment in Phase 0.
- Added `.gitignore` coverage for local secrets, caches, virtual environments,
  and generated reports.

### Known Issues

- XLSX loading and Excel workbook report generation are not implemented yet.
- Fuzzy matching and many-to-one payment allocation are intentionally not
  implemented.
