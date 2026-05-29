# Sample Data

This directory contains synthetic CSV files for local demos and automated tests.
The records are fake and must not be replaced with real client exports.

## Files

| File | Purpose |
|---|---|
| `valid-invoices.csv` | Valid invoice rows with basic whitespace and currency normalization examples. |
| `valid-payments.csv` | Valid payment rows with payment references for future matching phases. |
| `invalid-invoices.csv` | Invalid invoice rows for manual validation checks. |
| `invalid-payments.csv` | Invalid payment rows for manual validation checks. |

Phase 1 supports CSV ingestion only. XLSX inputs are intentionally deferred until
a later phase so this foundation can stay dependency-free.

Do not place real client data, production exports, secrets, credentials, or
private information in this directory.
