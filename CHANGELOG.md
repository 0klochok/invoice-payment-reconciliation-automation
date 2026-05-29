# Changelog

All notable project changes are recorded here.

## [Unreleased]

### Added

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

- Reconciliation logic, matching, XLSX loading, and report generation are not
  implemented yet.
