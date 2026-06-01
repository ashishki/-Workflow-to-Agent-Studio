# Small E-Commerce Workflow Input

Dataset kind: synthetic demo only. Not customer proof or pilot evidence.

## Business Context

Business: Shopify store selling home accessories.

Approximate volume:

- 500 orders/month;
- frequent order-status, returns, damaged-item, and product-detail questions.

Channels and systems:

- Gmail;
- Instagram DM;
- Shopify;
- Google Sheets;
- Google Doc with canned replies.

Goal: reduce repetitive support work and owner interruptions while keeping refund
and damaged-item decisions under human approval.

## Current Support Workflow

1. Customer asks about order status, return, damaged item, or product details.
2. Support assistant searches Shopify manually.
3. If return/refund is requested, assistant checks policy.
4. Refund requires owner approval.
5. Damaged item requests require a photo.
6. Repetitive responses are copied from a Google Doc.
7. Weekly support reporting is manual.

## Actors

- customer;
- support assistant;
- owner;
- fulfillment partner.

## Pain Points

- too many repetitive order-status questions;
- returns take too long;
- owner is interrupted for easy cases;
- support quality is inconsistent;
- weekly reporting is manual.

## Data Fields

- customer name;
- email;
- shipping address;
- order ID;
- order status;
- return reason;
- damaged-item photo flag;
- refund approval status.

## Sensitive Data Notes

The workflow includes customer PII and payment-adjacent business decisions. It
does not require raw card numbers.

## Boundaries

Do not automate:

- automatic refunds;
- customer compensation decisions;
- final refund approval;
- public product claims without review.
