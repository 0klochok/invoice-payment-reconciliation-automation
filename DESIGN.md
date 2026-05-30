# Design

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-30 |
| Status | Active draft |
| Scope | CLI-first local invoice and payment reconciliation automation |

## Design Objective

Create a local, deterministic Python CLI that helps accounting or operations
users reconcile invoice exports against payment exports. The system should be
easy to run on Windows with PowerShell and `uv`, require no external services,
and produce reviewable outputs from synthetic demo data.

Phase 7 was a final portfolio/demo documentation readiness pass over the current
local CLI behavior. Phase 8 is a final local release-readiness review of that
portfolio version. The workflow remains CLI-first and local-demo-first: CSV and
XLSX inputs are parsed locally, deterministic matching is unchanged, and report
outputs remain Markdown and CSV. It does not implement Excel workbook report
output, fuzzy matching, databases, web APIs, deployment, AI features, or external
services.

## Architecture Summary

The architecture is a small Python package under `src/` with a CLI entry point
named `reconcile`. File readers, schemas, validators, normalizers, matching
logic, and report writers are separate modules so each layer can be tested
independently.

The runtime model is local batch execution: the user runs one CLI command with
invoice and payment input files and receives generated report files. No web
server, database, background job, hosted deployment, paid API, or AI provider is
part of the MVP.

## Current Repository Shape

```text
.
|-- src/invoice_reconciliation/
|   |-- __init__.py
|   |-- cli.py
|   |-- ingestion.py
|   |-- matching.py
|   |-- models.py
|   `-- reporting.py
|-- tests/
|   |-- conftest.py
|   |-- test_cli.py
|   |-- test_ingestion.py
|   |-- test_matching.py
|   |-- test_reporting.py
|   `-- test_sample_data.py
|-- sample-data/
|   |-- README.md
|   |-- invalid-invoices.csv
|   |-- invalid-payments.csv
|   |-- demo-mixed-invoices.csv
|   |-- demo-mixed-invoices.xlsx
|   |-- demo-mixed-payments.csv
|   |-- demo-mixed-payments.xlsx
|   |-- valid-invoices.csv
|   `-- valid-payments.csv
|-- reports/
|   `-- .gitkeep
|-- docs/screenshots/
|   `-- .gitkeep
|-- docs/demo-output/mixed-demo/
|   |-- reconciliation-details.csv
|   |-- reconciliation-report.md
|   `-- reconciliation-summary.csv
|-- pyproject.toml
|-- uv.lock
`-- source-of-truth docs
```

## Planned Components

| Component | Responsibility | Status |
|---|---|---|
| CLI | Parse command-line options and orchestrate the local input-to-report workflow. | CSV/XLSX input report command implemented |
| Readers | Load invoice and payment files from CSV/XLSX. | CSV and XLSX implemented |
| Schemas/models | Represent validated invoice and payment records. | Implemented for Phase 1 inputs |
| Validators | Capture structured row-level validation errors. | Basic row validation implemented |
| Normalizers | Normalize names, emails, and comparable fields. | Whitespace/currency implemented; email planned |
| Matching engine | Match payments to invoices and classify exceptions. | Implemented for deterministic one-to-one Phase 2 rules |
| Report writers | Write local Markdown and CSV outputs from matching results. | Markdown/CSV implemented with polished exception labels and sorted detail rows |

## Data Flow

End-to-end flow, with Phase 1 covering steps 2-4 for CSV, Phase 2 covering step
5 for normalized in-memory records, Phase 3 covering Markdown and CSV outputs in
step 6, Phase 5 extending step 2 to XLSX inputs, and Phase 6 polishing the
report presentation in step 6:

1. User runs `reconcile` with invoice and payment file paths.
2. Readers load CSV or XLSX rows.
3. Validators convert valid rows to internal records and collect invalid rows.
4. Normalizers trim whitespace, uppercase currencies, parse dates, and parse
   decimal amounts.
5. Matching engine categorizes exact matches and deterministic exceptions.
6. Report writers generate deterministic Markdown and CSV files in a local
   output directory with concise totals, status summaries, sorted detail rows,
   and review notes for exception categories.

## Phase 0 Decisions

| ID | Decision | Rationale |
|---|---|---|
| ADR-001 | Use `uv` for dependency and environment management. | Matches project constraint and keeps setup reproducible. |
| ADR-002 | Use `argparse` for the Phase 0 CLI. | Standard library is enough for help/version scaffolding. |
| ADR-003 | Use pytest and Ruff as the baseline quality tools. | Fast local gates with minimal tooling. |
| ADR-004 | Keep generated reports ignored except `reports/.gitkeep`. | Prevents accidental report artifacts from entering Git. |
| ADR-005 | Use Python standard library `csv` for Phase 1 CSV ingestion. | Keeps the ingestion foundation dependency-free and reviewable. |
| ADR-006 | Use dataclasses, `Decimal`, and `date` for normalized input records. | Provides explicit typed records without adding runtime dependencies. |
| ADR-007 | Use a pure in-memory Phase 2 matcher over validated records. | Keeps matching deterministic, testable, and separate from import validation. |
| ADR-008 | Treat duplicate invoice or payment references as ambiguous. | Avoids guessing at many-to-one or many-to-many matches before business rules exist. |
| ADR-009 | Prioritize currency mismatch before amount mismatch. | Prevents comparing amounts as equivalent when currencies differ. |
| ADR-010 | Generate Markdown and CSV reports before Excel workbooks. | Provides useful local review artifacts without adding runtime dependencies in Phase 3. |
| ADR-011 | Keep report content timestamp-free. | Preserves deterministic report snapshots and stable tests. |
| ADR-012 | Use `openpyxl` for XLSX input parsing. | XLSX files are zipped XML workbooks; `openpyxl` is a minimal standard Python dependency for local spreadsheet reading and avoids fragile custom parsing. |
| ADR-013 | Sort report detail rows by status category and reference in the reporting layer. | Improves client-demo readability without changing matching semantics or input parsing behavior. |
| ADR-014 | Omit empty Markdown detail sections. | Keeps clean and mixed demo reports concise without placeholder filler. |
| ADR-015 | Commit a small Markdown/CSV demo-output snapshot under `docs/demo-output/`. | Gives reviewers concrete expected output without storing generated XLSX workbooks or large binary report artifacts. |

## Known Limitations

- Fuzzy matching is not implemented.
- Partial-payment allocation and many-to-one matching are not implemented.
- Excel workbook report output is not implemented.
- Email normalization is not part of the current sample schema.
- No web app, FastAPI service, database, deployment, AI feature, paid API, or
  real client data is part of the current design.
