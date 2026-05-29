# Requirements

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-29 |
| Status | Active draft |
| Project | invoice-payment-reconciliation-automation-new |
| Project type | Portfolio/demo automation |
| Primary users | Accounting and operations teams |

## Product Brief

Build a local Python CLI tool that imports invoice and payment exports, validates
and normalizes the data, matches payments to invoices, detects exceptions, and
generates review-ready reconciliation reports.

The project is a portfolio/demo project. It must use synthetic data only and must
not require deployment, paid services, AI calls, databases, or real client data.

## MVP Requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-001 | Provide a CLI entry point named `reconcile`. | P0 | Phase 0 scaffolded |
| FR-002 | Load invoice and payment inputs from CSV and XLSX files. | P0 | CSV implemented in Phase 1; XLSX planned |
| FR-003 | Validate required fields, dates, amounts, and currency consistency. | P0 | Basic row validation implemented in Phase 1 |
| FR-004 | Normalize customer name and email fields deterministically. | P0 | Customer name whitespace implemented in Phase 1; email planned |
| FR-005 | Capture invalid rows with row number, source, field, error code, and message. | P0 | Implemented in Phase 1 |
| FR-006 | Match payments to invoices using deterministic local rules. | P0 | Implemented in Phase 2 |
| FR-007 | Categorize reconciliation exceptions for review. | P0 | Implemented in Phase 2 |
| FR-008 | Generate Excel and Markdown reconciliation reports. | P0 | Planned |
| FR-009 | Include realistic fake sample data for local demos. | P0 | CSV samples added in Phase 1 |

## Phase 0 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P0-001 | Repository has active source-of-truth docs. | Required docs exist and describe current/future scope accurately. | Implemented |
| P0-002 | Project is managed by uv. | `pyproject.toml` and `uv.lock` exist. | Implemented |
| P0-003 | Minimal package and CLI skeleton exist. | `uv run reconcile --help` succeeds. | Implemented |
| P0-004 | Baseline tests and quality tooling exist. | pytest and Ruff gates pass. | Implemented |

## Phase 1 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P1-001 | Define invoice, payment, money amount, and import diagnostic schemas. | Domain models exist under `src/invoice_reconciliation/`. | Implemented |
| P1-002 | Add synthetic invoice and payment CSV files. | Valid and invalid CSV files exist under `sample-data/`. | Implemented |
| P1-003 | Load invoice and payment CSV files without new runtime dependencies. | CSV loaders use Python standard library `csv`. | Implemented |
| P1-004 | Validate required fields, ISO dates, and decimal amounts. | Invalid rows return structured validation errors. | Implemented |
| P1-005 | Normalize whitespace and currency values. | Tests cover trimmed fields and uppercased currency codes. | Implemented |
| P1-006 | Keep matching and reports out of scope. | No matching engine or report writer is implemented. | Implemented |

## Phase 2 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P2-001 | Match normalized invoice and payment records by exact reference. | Pure matcher accepts Phase 1 `InvoiceRecord` and `PaymentRecord` values. | Implemented |
| P2-002 | Match only one invoice to one payment when reference, currency, and amount agree. | Successful matches return explicit `matched` status values. | Implemented |
| P2-003 | Classify unmatched invoices and payments. | Result structures include stable `unmatched_invoice` and `unmatched_payment` outputs. | Implemented |
| P2-004 | Classify amount and currency mismatches separately. | Result structures include stable `amount_mismatch` and `currency_mismatch` outputs. | Implemented |
| P2-005 | Classify duplicate invoice or payment references as ambiguous. | Duplicate references return `ambiguous_reference` with a client-readable reason. | Implemented |
| P2-006 | Keep fuzzy matching, reports, XLSX, databases, web APIs, and external services out of scope. | No future-phase behavior is added. | Implemented |

## Out of Scope

- Fuzzy matching and probabilistic matching.
- XLSX file readers.
- Excel or Markdown report generation.
- FastAPI or any web service.
- Database or persistence layer.
- GitHub Actions, deployment, or hosted automation.
- Paid APIs, AI calls, or real client data.

## Acceptance Criteria

| ID | Requirement | Given | When | Then | Validation |
|---|---|---|---|---|---|
| AC-001 | P0-002 | A fresh local checkout | `uv sync` is run | Dependencies install from uv config | Manual/local |
| AC-002 | P0-003 | Phase 0 CLI exists | `uv run reconcile --help` is run | Help text is printed and exits successfully | Smoke |
| AC-003 | P0-004 | Phase 0 tests exist | `uv run pytest` is run | Tests pass | Automated |
| AC-004 | P0-004 | Phase 0 tooling exists | Ruff check and format check are run | Both pass | Automated |
| AC-005 | P1-003 | Valid invoice CSV exists | `load_invoice_csv` is called | Valid invoice records and clean diagnostics are returned | Automated |
| AC-006 | P1-003 | Valid payment CSV exists | `load_payment_csv` is called | Valid payment records and clean diagnostics are returned | Automated |
| AC-007 | P1-004 | CSV rows contain missing or malformed values | Loaders are called | Deterministic validation diagnostics are returned | Automated |
| AC-008 | P2-001 | Valid normalized invoices and payments exist | `match_invoices_to_payments` is called | Exact matching and exceptions are returned deterministically | Automated |

## Data Policy

- Only synthetic demo data may be committed.
- Real client files, production exports, secrets, credentials, and private data
  are forbidden.
- Sample files will be added in a later phase.
