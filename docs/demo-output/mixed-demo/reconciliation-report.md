# Invoice Payment Reconciliation Report

## Reconciliation Totals

| Metric | Value |
| --- | --- |
| Invoice records reviewed | 8 |
| Payment records reviewed | 8 |
| Matched invoice/payment pairs | 2 |
| Exception groups needing review | 6 |

## Status Summary

| Category | Count |
| --- | --- |
| Matched invoice and payment | 2 |
| Invoice missing payment | 1 |
| Payment missing invoice | 1 |
| Payment amount differs | 1 |
| Payment currency differs | 1 |
| Duplicate reference needs review | 2 |

## Matched Records

| Reference | Invoice ID | Payment ID | Customer | Matched Amount |
| --- | --- | --- | --- | --- |
| INV-2001 | INV-2001 | PAY-7001 | Apex Office Supplies | 100.00 USD |
| INV-2002 | INV-2002 | PAY-7002 | Beacon Field Services | 250.00 EUR |

## Invoices Missing Payments

| Reference | Invoice ID | Customer | Invoice Amount | Review Note |
| --- | --- | --- | --- | --- |
| INV-2003 | INV-2003 | Cascade Design Co | 325.50 USD | No payment found for invoice reference |

## Payments Missing Invoices

| Reference | Payment ID | Customer | Payment Amount | Review Note |
| --- | --- | --- | --- | --- |
| INV-2999 | PAY-ONLY | Lumen Event Rentals | 90.00 USD | No invoice found for payment reference |

## Amount Variances (Underpaid/Overpaid)

| Reference | Invoice ID | Payment ID | Customer | Invoice Amount | Payment Amount | Variance |
| --- | --- | --- | --- | --- | --- | --- |
| INV-2004 | INV-2004 | PAY-7004 | Delta Logistics | 480.00 USD | 475.00 USD | Underpaid by 5.00 USD; possible partial payment |

## Currency Conflicts

| Reference | Invoice ID | Payment ID | Customer | Invoice Amount | Payment Amount | Review Note |
| --- | --- | --- | --- | --- | --- | --- |
| INV-2005 | INV-2005 | PAY-7005 | Evergreen Consulting | 600.00 USD | 600.00 EUR | Invoice currency USD; payment currency EUR |

## Duplicate References Needing Review

| Reference | Invoice IDs | Payment IDs | Invoice Rows | Payment Rows | Review Note |
| --- | --- | --- | --- | --- | --- |
| INV-DUP-INV | INV-DUP-INV | PAY-DUP-INV | 8; 9 | 8 | Duplicate invoice reference; review invoice export duplicates |
| INV-DUP-PAY | INV-DUP-PAY | PAY-DUP-PAY-1; PAY-DUP-PAY-2 | 7 | 6; 7 | Duplicate payment reference; review payment export duplicates |
