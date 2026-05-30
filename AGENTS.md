# AGENTS.md

This file applies to the whole repository.

## Operating Rules

- Work only on the current requested phase.
- Keep changes small, focused, and reviewable.
- Use PowerShell commands on Windows unless the user explicitly approves another
  shell.
- Use `uv` for Python project and dependency management.
- Target Python 3.12 or newer.
- CLI-first and local-demo-first.
- Use fake sample data only.
- Do not use real client data, paid APIs, or AI calls unless explicitly approved.
- Do not add FastAPI, a database, deployment, or GitHub Actions unless a later
  phase explicitly requests them.

## Git Rules

- Codex must never commit.
- Codex must never push.
- Codex must not run `git add`, `git commit`, `git push`, `git reset`,
  destructive checkout, branch deletion, or history rewrite commands.
- Read-only Git inspection commands such as `git status`, `git diff`, `git log`,
  and `git branch` are allowed.
- The user manually validates, stages, commits, and pushes.

## Required Phase Workflow

Before changing files:

1. Read `AGENTS.md`.
2. Read `STATE.md`.
3. Read relevant source-of-truth docs for the requested phase.
4. Confirm the current phase and scope.
5. Avoid future-phase features.

Every phase must update:

- `STATE.md`
- Relevant docs
- Tests when behavior or testable scaffolding changes

## Quality Gate

Required default commands:

```powershell
uv sync --locked --dev
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

When CLI behavior or release readiness is in scope, also run:

```powershell
uv run reconcile --help
uv run reconcile report --help
uv run reconcile report --invoices sample-data/demo-mixed-invoices.csv --payments sample-data/demo-mixed-payments.csv --out-dir reports\demo-csv
uv run reconcile report --invoices sample-data/demo-mixed-invoices.xlsx --payments sample-data/demo-mixed-payments.xlsx --out-dir reports\demo-xlsx
```

If a validation command fails, stop, record the failure in `STATE.md`, and report
the failure clearly.
