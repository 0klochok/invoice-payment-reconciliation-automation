# Security

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-31 |
| Status | Active |
| Repository visibility | Public portfolio/demo by default |
| Risk level | Low while using synthetic local data only |

## Security Boundaries

- No real client data.
- No secrets, credentials, tokens, private keys, cookies, or production exports.
- No paid APIs.
- No deployment or external runtime automation in the current local-demo scope.
- GitHub Actions is allowed only for the minimal CI quality gate and must not
  use secrets, upload artifacts, or deploy.
- No database or FastAPI service in the current local-demo scope.
- No adult, casino/gambling, crypto-token, shady scraping, spam, bypass, or
  grey/black-hat functionality.

## Data Classification

| Data Type | Allowed? | Notes |
|---|---:|---|
| Synthetic sample data | Yes | May be committed when clearly fake. |
| Generated local reports | Local only | Ignored by Git under `reports/`; intentional fake Markdown/CSV snapshots may be committed under `docs/demo-output/`. |
| Real client data | No | Must never be committed or used for demo tests. |
| Secrets and credentials | No | Must never be committed or logged. |

## Secrets Policy

- `.env` and `.env.*` are ignored.
- `.env.example` may be added later with placeholder values only if needed.
- Tests must not require real secrets.
- Docs and screenshots must not include real credentials or private data.

## Input Safety

The CLI validates imported invoice and payment rows before reconciliation.
Invalid rows are captured as structured diagnostics with source, row, field,
error code, and message details where practical. File processing remains local
to caller-provided paths and synthetic demo inputs.

## Phase 1 Security Review

Phase 1 adds synthetic CSV sample data and local CSV ingestion only. No external
network calls are made by the application, and no real data is included.

## Phase 2 Security Review

Phase 2 adds deterministic in-memory matching over normalized records only. It
does not add external network calls, paid APIs, report generation, file writes,
databases, web services, or real client data.

## Phase 3 Security Review

Phase 3 adds local Markdown and CSV report file writes under a caller-provided
output directory. Generated reports remain local demo artifacts and are ignored
by Git under `reports/`; no external network calls, paid APIs, databases, web
services, or real client data are added.

## Phase 8 Release Readiness Security Review

Phase 8 reviewed the portfolio repository for accidental secrets, paid-service
assumptions, large tracked binaries, generated cache files, unrelated artifacts,
and unintended demo-output contents. No runtime security behavior changed.

## Phase 9 CI Security Review

Phase 9 adds a minimal GitHub Actions CI workflow for pull requests and pushes
without deployment branch filtering. The workflow uses public dependencies from
the lockfile, runs local quality and demo commands, writes only runner-local
report outputs, and does not configure secrets, upload artifacts, deploy, or
call paid APIs.
