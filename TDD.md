# Test Strategy

## Meta

| Field | Value |
|---|---|
| Last updated | 2026-05-29 |
| Status | Active draft |
| Applies to | invoice-payment-reconciliation-automation-new |

## Testing Policy

- Use pytest for automated tests.
- Use Ruff for linting and formatting checks.
- Prefer test-first development for future behavior-heavy phases.
- Keep tests deterministic and local.
- Use synthetic fixtures only.
- Do not use real client data, paid APIs, AI calls, or live external services in
  tests.

## Phase 0 Coverage

Phase 0 includes only scaffold tests:

- Package import smoke test.
- CLI help smoke test.

These tests prove the package is importable and the `reconcile` command parser
can display help. They do not validate reconciliation behavior because that is
out of scope for Phase 0.

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
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

When CLI behavior is present, also run:

```powershell
uv run reconcile --help
```

## Acceptance for Future Phases

Future phases should add tests for:

- Valid invoice CSV loading.
- Valid payment CSV loading.
- Valid XLSX loading.
- Missing required fields.
- Bad amounts.
- Bad dates.
- Mixed currency handling.
- Deterministic normalization.
- Matching and exception categorization.
- Report generation outputs.

