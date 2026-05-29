# Security

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-29 |
| Status | Active draft |
| Repository visibility | Public portfolio/demo by default |
| Risk level | Low while using synthetic local data only |

## Security Boundaries

- No real client data.
- No secrets, credentials, tokens, private keys, cookies, or production exports.
- No paid APIs.
- No AI calls unless explicitly approved.
- No deployment or external automation in Phase 0.
- No database, FastAPI service, or GitHub Actions in Phase 0.
- No adult, casino/gambling, crypto-token, shady scraping, spam, bypass, or
  grey/black-hat functionality.

## Data Classification

| Data Type | Allowed? | Notes |
|---|---:|---|
| Synthetic sample data | Yes | May be committed when clearly fake. |
| Generated local reports | Local only | Ignored by Git except `reports/.gitkeep`. |
| Real client data | No | Must never be committed or used for demo tests. |
| Secrets and credentials | No | Must never be committed or logged. |

## Secrets Policy

- `.env` and `.env.*` are ignored.
- `.env.example` may be added later with placeholder values only if needed.
- Tests must not require real secrets.
- Docs and screenshots must not include real credentials or private data.

## Input Safety

Future phases will validate user-provided file paths and imported row data.
Invalid rows should be captured as structured validation errors instead of
crashing the reconciliation run where practical.

## Phase 0 Security Review

Phase 0 adds project scaffolding only. No external network calls are made by the
application, and no real data is included.

