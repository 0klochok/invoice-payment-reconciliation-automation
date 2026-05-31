# Requirements

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-31 |
| Status | Active |
| Project | invoice-payment-reconciliation-automation-new |
| Project type | Portfolio/demo automation |
| Primary users | Accounting and operations teams |

## Product Brief

Build a local Python CLI tool that imports invoice and payment exports, validates
and normalizes the data, matches payments to invoices, detects exceptions, and
generates review-ready reconciliation reports.

The project is a portfolio/demo project. It must use synthetic data only and must
not require deployment, paid services, runtime external services, databases, or
real client data.

## MVP Requirements

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR-001 | Provide a CLI entry point named `reconcile`. | P0 | Phase 0 scaffolded |
| FR-002 | Load invoice and payment inputs from CSV and XLSX files. | P0 | Implemented |
| FR-003 | Validate required fields, dates, amounts, and currency consistency. | P0 | Basic row validation implemented in Phase 1 |
| FR-004 | Normalize customer name and email fields deterministically where those fields exist in the sample schema. | P0 | Customer name whitespace implemented in Phase 1; email is not part of the current sample schema |
| FR-005 | Capture invalid rows with row number, source, field, error code, and message. | P0 | Implemented in Phase 1 |
| FR-006 | Match payments to invoices using deterministic local rules. | P0 | Implemented in Phase 2 |
| FR-007 | Categorize reconciliation exceptions for review. | P0 | Implemented in Phase 2; labels polished in Phase 6 |
| FR-008 | Generate Markdown and CSV reconciliation reports. | P0 | Implemented in Phase 3; presentation polished in Phase 6 |
| FR-009 | Include realistic fake sample data for local demos. | P0 | CSV samples added in Phase 1; mixed CSV/XLSX demo samples added in Phases 4 and 5 |

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

## Phase 3 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P3-001 | Generate a deterministic Markdown reconciliation report from Phase 2 results. | Report includes summary counts, matches, unmatched records, mismatches, and ambiguous references. | Implemented |
| P3-002 | Generate deterministic CSV outputs for spreadsheet review. | Summary and detail CSV files include stable columns, client-readable status labels, and all Phase 2 status categories. | Implemented |
| P3-003 | Add a simple local CLI report command for CSV inputs. | `reconcile report --invoices ... --payments ... --out-dir ...` writes local report files. | Implemented |
| P3-004 | Preserve deterministic ordering and avoid mutating input records. | Tests cover stable CSV ordering and unchanged input record collections. | Implemented |
| P3-005 | Keep XLSX, Excel workbook output, fuzzy matching, databases, web APIs, and external services out of scope. | No future-phase behavior is added. | Implemented |

## Phase 4 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P4-001 | Add a deterministic mixed CSV demo scenario for portfolio review. | Mixed sample inputs include matched records and each implemented exception category. | Implemented |
| P4-002 | Keep the mixed demo synthetic and local-demo-first. | Sample rows are fake and report output remains local Markdown/CSV. | Implemented |
| P4-003 | Add smoke coverage for mixed-demo parseability and output containment. | Tests verify mixed sample counts and report files stay inside the requested output directory. | Implemented |

## Phase 5 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P5-001 | Load invoice XLSX files through the same normalization and validation rules as CSV files. | `load_invoice_xlsx` returns validated records and structured diagnostics. | Implemented |
| P5-002 | Load payment XLSX files through the same normalization and validation rules as CSV files. | `load_payment_xlsx` returns validated records and structured diagnostics. | Implemented |
| P5-003 | Preserve existing CSV input behavior and report outputs. | Existing CSV tests and CSV CLI smoke commands continue to pass. | Implemented |
| P5-004 | Add mixed synthetic XLSX sample files equivalent to the deterministic mixed CSV demo. | Mixed CSV and XLSX sample inputs produce equivalent status counts. | Implemented |
| P5-005 | Keep Excel workbook report output, fuzzy matching, databases, web APIs, and external services out of scope. | CLI stays deterministic and local-demo-first with Markdown/CSV report outputs. | Implemented |

## Phase 6 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P6-001 | Improve Markdown report clarity for portfolio/client demos without changing matching semantics. | Markdown includes concise totals, clearer status summary labels, sorted detail sections, and no empty placeholder sections. | Implemented |
| P6-002 | Improve exception detail readability for unmatched, underpaid/overpaid, currency conflict, and duplicate-reference cases. | Markdown and details CSV include client-readable review notes while preserving stable status values. | Implemented |
| P6-003 | Preserve Markdown, summary CSV, and details CSV as the only report outputs. | CLI writes only `reconciliation-report.md`, `reconciliation-summary.csv`, and `reconciliation-details.csv`. | Implemented |
| P6-004 | Keep CSV and XLSX input behavior unchanged. | Existing CSV/XLSX ingestion and equivalence tests continue to pass. | Implemented |
| P6-005 | Keep Excel workbook output, web apps, databases, deployment, runtime external services, and matching changes out of scope. | No future-phase components or dependencies are added. | Implemented |

## Phase 7 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P7-001 | Make source-of-truth docs portfolio-ready for the current implemented CLI behavior. | README, runbook, sample-data notes, requirements, design, test strategy, changelog, and state describe current behavior consistently. | Implemented |
| P7-002 | Document exact local demo commands and expected output files. | Docs show CSV and XLSX-input commands and list the three generated Markdown/CSV files. | Implemented |
| P7-003 | Include a small generated demo-output snapshot only if it helps reviewer clarity. | `docs/demo-output/mixed-demo/` contains only Markdown/CSV report examples generated from existing sample data. | Implemented |
| P7-004 | Preserve current reconciliation, ingestion, and report-generation behavior. | No core logic changes, new dependencies, web app, database, deployment, runtime external service, or XLSX report output are added. | Implemented |

## Phase 8 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P8-001 | Complete a final local release-readiness review for the portfolio version. | Source-of-truth docs, setup steps, demo commands, generated outputs, limitations, sample-data notes, and quality-gate instructions are reviewed against current behavior. | Implemented |
| P8-002 | Verify documented CSV and XLSX demo commands from clean local output directories. | `reports\demo-csv` and `reports\demo-xlsx` are regenerated with exactly the expected Markdown and CSV outputs. | Implemented |
| P8-003 | Verify repository hygiene for a public portfolio demo. | Ignored report artifacts remain ignored, `docs/demo-output/` contains only intentional Markdown/CSV examples, and no accidental secrets, paid API assumptions, large binaries, generated cache files, or unrelated tracked artifacts are found. | Implemented |
| P8-004 | Preserve current runtime behavior. | No reconciliation, ingestion, report-generation, dependency, deployment, web, database, runtime external service, paid API, secret, commit, push, staging, or history changes are made. | Implemented |

## Phase 9 Requirements

| ID | Requirement | Acceptance Signal | Status |
|---|---|---|---|
| P9-001 | Add minimal GitHub Actions CI for the stable local quality gate. | Workflow runs on pull requests and pushes to `main`. | Implemented |
| P9-002 | Use `uv` and the lockfile in CI. | Workflow installs `uv`, runs `uv sync --locked --dev`, then runs pytest, Ruff checks, CLI help smoke checks, and CSV/XLSX demo commands. | Implemented |
| P9-003 | Keep CI non-deploying and local-demo-focused. | Workflow does not upload artifacts, configure secrets, deploy, or add external services beyond GitHub Actions CI. | Implemented |

## Out of Scope

- Fuzzy matching and probabilistic matching.
- Excel workbook report generation unless a later phase explicitly approves it.
- FastAPI or any web service.
- Database or persistence layer.
- Deployment or hosted runtime automation beyond minimal CI.
- Paid APIs, runtime external services, or real client data.

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
| AC-009 | P3-001 | Phase 2 reconciliation results exist | Markdown reporting is called | Summary and detail sections are rendered deterministically | Automated |
| AC-010 | P3-002 | Phase 2 reconciliation results exist | CSV reporting is called | Summary and detail CSV rows include all Phase 2 statuses in stable order | Automated |
| AC-011 | P3-003 | Valid sample CSV inputs exist | `uv run reconcile report --invoices sample-data/valid-invoices.csv --payments sample-data/valid-payments.csv --out-dir reports` is run | Markdown and CSV report files are written locally | Smoke |
| AC-012 | P5-004 | Mixed sample CSV and XLSX inputs exist | Reconciliation is run for both formats | Status counts and Markdown/CSV report outputs are equivalent, and report files stay under the requested output directory | Automated/smoke |
| AC-013 | P6-001 | Mixed sample inputs exist | Reconciliation report generation is run | Markdown and CSV outputs use clear labels, review notes, and deterministic status/reference ordering without XLSX report output | Automated/smoke |
| AC-014 | P7-002 | Source-of-truth docs and mixed sample inputs exist | Required validation and demo commands are run | Docs match current behavior, demo directories contain only the three expected report files, and CSV/XLSX-input outputs are equivalent | Manual/smoke |
| AC-015 | P8-001 | Portfolio-ready docs and mixed sample inputs exist | Full release-readiness validation is run locally | Quality gates pass, documented demo outputs regenerate cleanly, ignored artifacts stay ignored, and no repository hygiene issues are found | Manual/smoke |
| AC-016 | P9-001 | Minimal CI workflow exists | A pull request or push to `main` runs in GitHub Actions | CI syncs locked dependencies and runs the documented quality gate without deployment, secrets, or artifact upload | CI |

## Data Policy

- Only synthetic demo data may be committed.
- Real client files, production exports, secrets, credentials, and private data
  are forbidden.
- Sample files must remain synthetic and demo-only.
