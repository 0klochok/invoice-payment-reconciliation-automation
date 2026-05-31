# Demo Output Snapshot

This directory contains the committed reviewer snapshot for the mixed
reconciliation demo. The files under `mixed-demo/` were generated from the
synthetic CSV inputs in `sample-data/mixed-demo/` and are included so reviewers
can inspect expected output without running the CLI first.

The mixed-demo snapshot is covered by an automated pytest regression guard that
regenerates the CSV demo output in a temporary directory and compares the
generated Markdown and CSV contents with these committed files.

## Contents

- `mixed-demo/reconciliation-report.md`: human-readable reconciliation summary
  with matched records and exception sections.
- `mixed-demo/reconciliation-summary.csv`: status counts by reconciliation
  category.
- `mixed-demo/reconciliation-details.csv`: row-level matched and exception
  details for spreadsheet review.

## What To Notice

- The snapshot uses fake demo data only.
- The report covers matched records, missing invoices/payments, amount
  variance, currency conflict, and duplicate-reference review cases.
- The outputs are Markdown and CSV only; no generated XLSX report artifact is
  committed.
- Local demo runs should write new artifacts under ignored `reports/` paths
  rather than replacing this snapshot.
