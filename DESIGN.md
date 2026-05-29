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

Phase 0 only establishes the foundation. It does not implement file loading,
validation, matching, exception categorization, or report generation.

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
|   `-- cli.py
|-- tests/
|   |-- conftest.py
|   `-- test_cli.py
|-- sample-data/
|   `-- .gitkeep
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
| CLI | Parse command-line options and orchestrate the workflow. | Scaffolded |
| Readers | Load invoice and payment files from CSV/XLSX. | Planned |
| Schemas/models | Represent validated invoice and payment records. | Planned |
| Validators | Capture structured row-level validation errors. | Planned |
| Normalizers | Normalize names, emails, and comparable fields. | Planned |
| Matching engine | Match payments to invoices and classify exceptions. | Planned |
| Report writers | Write Excel and Markdown outputs. | Planned |

## Data Flow

Planned future flow:

1. User runs `reconcile` with invoice and payment file paths.
2. Readers load CSV/XLSX rows.
3. Validators convert valid rows to internal records and collect invalid rows.
4. Normalizers prepare comparable fields.
5. Matching engine categorizes matches and exceptions.
6. Report writers generate Excel and Markdown outputs.

## Phase 0 Decisions

| ID | Decision | Rationale |
|---|---|---|
| ADR-001 | Use `uv` for dependency and environment management. | Matches project constraint and keeps setup reproducible. |
| ADR-002 | Use `argparse` for the Phase 0 CLI. | Standard library is enough for help/version scaffolding. |
| ADR-003 | Use pytest and Ruff as the baseline quality tools. | Fast local gates with minimal tooling. |
| ADR-004 | Keep generated reports ignored except `reports/.gitkeep`. | Prevents accidental report artifacts from entering Git. |

## Known Limitations

- CLI help and version output are the only implemented runtime behavior.
- No sample data files exist yet.
- No reconciliation, validation, or reporting behavior exists yet.

