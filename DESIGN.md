# Design

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-29 |
| Status | Active draft |
| Scope | CLI-first local invoice and payment reconciliation automation |

## Design Objective

Create a local, deterministic Python CLI that helps accounting or operations
users reconcile invoice exports against payment exports. The system should be
easy to run on Windows with PowerShell and `uv`, require no external services,
and produce reviewable outputs from synthetic demo data.

Phase 1 establishes the first ingestion layer. It implements CSV loading,
required-field validation, normalization, and structured import diagnostics. It
does not implement matching, exception categorization, report generation, or
XLSX loading.

## Architecture Summary

The intended architecture is a small Python package under `src/` with a CLI entry
point named `reconcile`. Future phases will add file readers, schemas,
validators, normalizers, matching logic, and report writers as separate modules
so each layer can be tested independently.

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
|   `-- models.py
|-- tests/
|   |-- conftest.py
|   |-- test_cli.py
|   `-- test_ingestion.py
|-- sample-data/
|   |-- README.md
|   |-- invalid-invoices.csv
|   |-- invalid-payments.csv
|   |-- valid-invoices.csv
|   `-- valid-payments.csv
|-- reports/
|   `-- .gitkeep
|-- docs/screenshots/
|   `-- .gitkeep
|-- pyproject.toml
|-- uv.lock
`-- source-of-truth docs
```

## Planned Components

| Component | Responsibility | Status |
|---|---|---|
| CLI | Parse command-line options and orchestrate the workflow. | Help/version scaffolded |
| Readers | Load invoice and payment files from CSV/XLSX. | CSV implemented; XLSX planned |
| Schemas/models | Represent validated invoice and payment records. | Implemented for Phase 1 inputs |
| Validators | Capture structured row-level validation errors. | Basic row validation implemented |
| Normalizers | Normalize names, emails, and comparable fields. | Whitespace/currency implemented; email planned |
| Matching engine | Match payments to invoices and classify exceptions. | Planned |
| Report writers | Write Excel and Markdown outputs. | Planned |

## Data Flow

End-to-end planned flow, with Phase 1 covering steps 2-4 for CSV only:

1. User runs `reconcile` with invoice and payment file paths.
2. Readers load CSV rows. XLSX loading is deferred.
3. Validators convert valid rows to internal records and collect invalid rows.
4. Normalizers trim whitespace, uppercase currencies, parse dates, and parse
   decimal amounts.
5. Matching engine categorizes matches and exceptions in a later phase.
6. Report writers generate Excel and Markdown outputs in a later phase.

## Phase 0 Decisions

| ID | Decision | Rationale |
|---|---|---|
| ADR-001 | Use `uv` for dependency and environment management. | Matches project constraint and keeps setup reproducible. |
| ADR-002 | Use `argparse` for the Phase 0 CLI. | Standard library is enough for help/version scaffolding. |
| ADR-003 | Use pytest and Ruff as the baseline quality tools. | Fast local gates with minimal tooling. |
| ADR-004 | Keep generated reports ignored except `reports/.gitkeep`. | Prevents accidental report artifacts from entering Git. |
| ADR-005 | Use Python standard library `csv` for Phase 1 CSV ingestion. | Keeps the ingestion foundation dependency-free and reviewable. |
| ADR-006 | Use dataclasses, `Decimal`, and `date` for normalized input records. | Provides explicit typed records without adding runtime dependencies. |

## Known Limitations

- CLI help and version output are the only implemented command-line behavior.
- CSV ingestion is exposed through package functions, not a full CLI workflow.
- XLSX loading is not implemented yet.
- No reconciliation matching or reporting behavior exists yet.
