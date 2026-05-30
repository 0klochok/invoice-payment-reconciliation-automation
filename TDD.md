# Test Strategy

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-30 |
| Status | Active draft |
| Applies to | invoice-payment-reconciliation-automation-new |

## Testing Policy

- Use pytest for automated tests.
- Use Ruff for linting and formatting checks.
- Prefer test-first development for future behavior-heavy phases.
- Keep tests deterministic and local.
- Use synthetic fixtures only.
- Do not use real client data, paid APIs, or live external services in
  tests.

## Current Coverage

Phase 0 includes scaffold tests:

- Package import smoke test.
- CLI help smoke test.

Phase 1 adds ingestion tests:

- Valid invoice CSV loading.
- Valid payment CSV loading.
- Missing required fields.
- Bad date format.
- Bad amount format.
- Whitespace and currency normalization.
- Deterministic validation error output.

These tests prove the package is importable, the `reconcile` command parser can
display help, and the CSV ingestion layer returns validated records plus stable
diagnostics.

Phase 2 adds matching tests:

- Exact successful match.
- Unmatched invoice.
- Unmatched payment.
- Amount mismatch.
- Currency mismatch.
- Duplicate payment reference.
- Duplicate invoice reference.
- Deterministic output ordering.
- No mutation of input record collections.
- Integration with Phase 1 normalized sample CSV records.

Phase 3 adds reporting and CLI workflow tests:

- Markdown report generation with summary and detail sections.
- CSV summary and detail report generation.
- Summary counts for every Phase 2 status.
- Client-readable status labels for all major statuses.
- Deterministic detail CSV status/reference ordering.
- No mutation of input record collections while rendering/writing reports.
- CLI smoke coverage for writing reports under a pytest `tmp_path`.

Phase 5 adds XLSX input and spreadsheet-demo tests:

- Mixed XLSX invoice sample parseability.
- Mixed XLSX payment sample parseability.
- Mixed XLSX demo reconciliation status counts.
- CSV and XLSX mixed-demo status count equivalence.
- CLI smoke coverage for XLSX inputs under a pytest `tmp_path`.
- Output containment coverage for XLSX-generated reports.

Phase 6 adds client-presentable reporting and CLI polish tests:

- Markdown report structure with reconciliation totals, status summary, sorted
  sections, and no placeholder empty sections.
- CSV summary and details labels for client-readable exception categories.
- Details CSV review notes for invoices missing payments, payments missing
  invoices, underpaid/overpaid amount variances, currency conflicts, and
  duplicate references.
- Deterministic report-layer ordering by status category and reference.
- CLI success output wording for the generated Markdown, summary CSV, and
  details CSV files.

Phase 7 adds a documentation and demo-readiness validation pass:

- README, runbook, sample-data notes, requirements, design, test strategy,
  changelog, and state reviewed against current implemented behavior.
- Generated Markdown/CSV example output snapshot under `docs/demo-output/`
  created from existing mixed sample data.
- Manual smoke validation of CSV-input and XLSX-input demo commands.
- Manual equivalence check for generated CSV-input and XLSX-input report files.
- No tests were added because Phase 7 does not change runtime behavior.

Phase 8 adds a final local release-readiness validation pass:

- Source-of-truth docs reviewed as portfolio-facing project documentation.
- Documented CSV and XLSX demo commands rerun from clean local output
  directories.
- Ignored local report artifacts, committed demo-output examples, repository
  hygiene, and no-secrets/no-paid-API assumptions manually reviewed.
- No tests were added because Phase 8 does not change runtime behavior.

Phase 9 adds minimal GitHub Actions CI coverage:

- CI syncs locked dependencies with `uv sync --locked --dev`.
- CI runs pytest, Ruff lint, Ruff format check, top-level CLI help, report CLI
  help, and the CSV/XLSX demo smoke commands.
- No tests were added because Phase 9 adds CI scaffolding only and does not
  change runtime behavior.

## Future Test Layers

| Layer | Purpose | Planned Location |
|---|---|---|
| Unit | Validate pure parsing, normalization, validation, and matching rules. | `tests/` |
| Integration | Load CSV/XLSX fixtures and verify structured results. | `tests/` |
| Smoke | Verify CLI help and end-to-end demo commands. | `tests/` and manual commands |
| Security/safety | Check fake-data-only and no-secrets assumptions. | Manual review and targeted tests |

## Required Quality Gate

Run from the repository root:

```powershell
uv sync --locked --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run reconcile --help
uv run reconcile report --help
```

The GitHub Actions CI workflow mirrors this gate with `uv sync --locked --dev`
on pull requests and pushes to `main`.

When CLI behavior is present, also run:

```powershell
uv run reconcile report --invoices sample-data/mixed-demo/invoices.csv --payments sample-data/mixed-demo/payments.csv --out-dir reports\demo-csv
uv run reconcile report --invoices sample-data/mixed-demo/invoices.xlsx --payments sample-data/mixed-demo/payments.xlsx --out-dir reports\demo-xlsx
Get-ChildItem -Name -LiteralPath reports\demo-csv
Get-ChildItem -Name -LiteralPath reports\demo-xlsx
```

## Acceptance for Future Phases

Future phases should add tests for:

- Mixed currency handling.
- Excel workbook report workflows if a later phase explicitly approves them.
