# Small E-Commerce AI Implementation Roadmap

Dataset kind: synthetic demo only. Not customer proof or pilot evidence.

## Executive Summary

Recommended privacy mode: private analysis for real customer data; lightweight
cloud is acceptable only for redacted process analysis and synthetic examples.

Top recommendations:

1. Support triage assistant.
2. Order-status lookup integration.
3. Human-in-the-loop returns assistant.

Do not automate yet:

- automatic refunds;
- customer compensation decisions;
- public product claims without review.

30/60/90 day plan:

- 30 days: clean FAQ, returns policy, canned replies, and support categories.
- 60 days: pilot support triage and order-status lookup in shadow mode.
- 90 days: add returns workflow assistant with owner approval gate.

Overall confidence: medium. Order volume is known, but ticket categories and
historical labels need verification.

## Evidence Packet

Primary source: `docs/examples/domains/ecommerce_input.md`

Evidence snippets:

- store receives order-status, return, damaged-item, and product-detail
  questions;
- support assistant manually searches Shopify;
- refunds require owner approval;
- repetitive replies are copied from a Google Doc.

Missing evidence:

- monthly support ticket volume;
- historical ticket labels;
- final refund and damaged-item policies;
- identity verification rules for order status.

## Process Inventory

| Process | Recommended Type | Impact | Readiness | Privacy | Priority |
|---------|------------------|--------|-----------|---------|----------|
| Support triage | LLM assistant | high | medium | sensitive | strategic pilot |
| Order status lookup | API integration + canned reply | high | high | sensitive | quick win |
| Returns workflow | Human-in-the-loop workflow | high | medium | sensitive/payment-adjacent | strategic pilot |
| Automatic refunds | Do not automate yet | high | low | sensitive/payment-adjacent | human-only |

## Recommendation REC-001: Support Triage Assistant

Solution type: LLM assistant.

Why: repeated inbound questions have clear categories, but the assistant should
suggest triage and draft replies rather than make final financial decisions.

Required data:

- FAQ;
- return policy;
- historical support messages after redaction;
- Shopify order metadata;
- canned reply library.

Privacy class: sensitive.

Estimated cost:

- one-time: 3000-15000 USD;
- monthly: 50-1000 USD depending on volume, model, and context size.

Estimated time: 3-6 weeks.

Required people:

- AI automation engineer;
- support assistant;
- owner.

Risks:

- hallucinated policy answer;
- wrong intent label;
- exposure of address/order data;
- inconsistent escalation.

Human gate:

- all refund, damaged-item, and compensation cases stay human-approved.

Validation:

- label 100 historical tickets;
- compare assistant intent against human labels;
- review first 100 live classifications.

Success metrics:

- first response time;
- escalation accuracy;
- manual handling time;
- owner interruption count.

Confidence: medium until historical support labels exist.

Fallback: deterministic category tags and canned replies.

## Recommendation REC-002: Order Status Lookup

Solution type: API integration plus canned response.

Why: order status is factual lookup. LLM is not required for the core answer.

Required data:

- order ID;
- customer email;
- Shopify order status;
- fulfillment tracking link.

Privacy class: sensitive.

Estimated cost:

- one-time: 2000-10000 USD;
- monthly: 0-300 USD plus integration platform cost if used.

Estimated time: 1-3 weeks.

Risks:

- leaking order details to wrong person;
- stale Shopify data;
- overexposing address details.

Controls:

- identity verification before status details;
- no full address in reply unless necessary;
- audit of lookup events.

Validation:

- test 30 synthetic orders and edge cases;
- verify no wrong-recipient responses.

Confidence: high if Shopify access and identity rules are clear.

Fallback: support assistant manually searches Shopify.

## Recommendation REC-003: Returns Workflow Assistant

Solution type: human-in-the-loop workflow.

Why: policy can be standardized, but refunds affect money and require owner
approval.

Required data:

- return policy;
- order date;
- product condition;
- damaged-item photo flag;
- owner approval status.

Privacy class: sensitive/payment-adjacent.

Estimated cost:

- one-time: 4000-20000 USD;
- monthly: 100-1000 USD.

Estimated time: 4-8 weeks.

Risks:

- wrong refund recommendation;
- inconsistent application of policy;
- customer dissatisfaction.

Human gate:

- owner approves refund or compensation.

Validation:

- review 50 past return cases;
- compare assistant recommendation with owner decision;
- require shadow mode before live use.

Confidence: medium-low until past return decisions are reviewed.

Fallback: structured checklist in a shared spreadsheet.

## Verification Appendix

Claims:

- CLM-001: Shopify is searched manually. Evidence: domain input workflow step 2.
- CLM-002: refund requires owner approval. Evidence: domain input workflow step
  4.
- CLM-003: data includes name, email, address, and order ID. Evidence: domain
  input data fields.

Assumptions:

- ASM-001: 500 orders/month creates enough support volume to justify automation.
- ASM-002: Shopify API access can be granted read-only for pilot.
- ASM-003: return policy is stable enough to encode.

Blocking findings:

- automatic refunds blocked;
- real customer records require redaction/private mode before analysis.
