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
| FR-002 | Load invoice and payment inputs from CSV and XLSX files. | P0 | Planned |
| FR-003 | Validate required fields, dates, amounts, and currency consistency. | P0 | Planned |
| FR-004 | Normalize customer name and email fields deterministically. | P0 | Planned |
| FR-005 | Capture invalid rows with row number, source, field, error code, and message. | P0 | Planned |
| FR-006 | Match payments to invoices using deterministic local rules. | P0 | Planned |
| FR-007 | Categorize reconciliation exceptions for review. | P0 | Planned |
| FR-008 | Generate Excel and Markdown reconciliation reports. | P0 | Planned |
| FR-009 | Include realistic fake sample data for local demos. | P0 | Planned |

## Phase 0 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P0-001 | Repository has active source-of-truth docs. | Required docs exist and describe current/future scope accurately. | Implemented |
| P0-002 | Project is managed by uv. | `pyproject.toml` and `uv.lock` exist. | Implemented |
| P0-003 | Minimal package and CLI skeleton exist. | `uv run reconcile --help` succeeds. | Implemented |
| P0-004 | Baseline tests and quality tooling exist. | pytest and Ruff gates pass. | Implemented |

## Out of Scope

- Reconciliation matching logic.
- CSV or XLSX file readers.
- Data validation implementation.
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

## Data Policy

- Only synthetic demo data may be committed.
- Real client files, production exports, secrets, credentials, and private data
  are forbidden.
- Sample files will be added in a later phase.

