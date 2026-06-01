# Implementation Patterns

Purpose: define the first SMB pattern library for matching workflow pains to
implementation options.

## Pattern Contract

```yaml
pattern_id: customer_support_triage:v1
pattern_name: Customer support triage
business_problem: Manual classification and routing of inbound requests
suitable_company_type:
  - e-commerce
  - SaaS
  - local service business
workflow_signals:
  - repeated inbound messages
  - manual routing
  - FAQ or policy exists
required_data:
  - support messages
  - FAQ
  - policy docs
  - order/customer lookup metadata
privacy_class: moderate
architecture:
  recommended_solution_type: LLM assistant plus deterministic routing
  llm_owned_steps:
    - summarize message
    - suggest intent
  deterministic_steps:
    - policy lookup
    - escalation routing
    - refund approval gate
estimated_implementation_time: 2-6 weeks
cost_range: implementation range plus monthly run cost
required_roles:
  - AI automation engineer
  - process owner
  - reviewer
risks:
  - hallucinated policy answer
  - wrong escalation
  - sensitive customer data exposure
evaluation_metrics:
  - classification accuracy
  - first response time
  - escalation precision
when_not_to_use:
  - low message volume
  - no stable policy
  - high-risk decision without human review
```

## MVP Pattern Set

| Pattern | Best Fit | Solution Type | Privacy Default | When Not To Use |
|---------|----------|---------------|-----------------|-----------------|
| Customer support triage | e-commerce, local services | LLM assistant + routing | moderate | unstable policy, high-stakes support |
| Internal knowledge assistant | agencies, ops teams | RAG assistant | low-moderate | outdated docs |
| Sales email assistant | B2B services | draft assistant | moderate | no human review |
| Lead qualification | clinics, real estate, services | rules + LLM summary | moderate | discriminatory scoring risk |
| Document extraction | accounting, legal, logistics | extraction + review | high | no validation samples |
| Invoice processing | accounting, ops | extraction + accounting rules | moderate-high | no accounting review |
| Meeting summarization | agencies, sales | transcription + summary | moderate | consent unclear |
| CRM enrichment | sales teams | API integration + cleanup | moderate | no CRM owner |
| HR screening support | recruiters | assistant, not decision-maker | high | automated rejection |
| Legal checklist assistant | legal consultancy | private assistant + review | high | legal advice automation |
| Inventory forecasting | retail/e-commerce | statistical model first | low-moderate | insufficient history |
| Reporting automation | ops/accounting | scripts + LLM explanation | low-moderate | metrics undefined |
| Operations copilot | internal teams | RAG + workflow assistant | moderate | no SOPs |
| QA assistant | support/engineering | checklist + LLM review | moderate | ambiguous quality criteria |
| Onboarding assistant | HR/customer success | RAG assistant | moderate | docs outdated |
| Content generation workflow | marketing | LLM drafting + approvals | low-moderate | regulated claims |
| Research assistant | consultants | RAG/search + citations | low-moderate | citation quality unverified |
| Compliance checklist assistant | regulated ops | checklist + review | high | treated as compliance guarantee |
| Messaging support bot | local services | chat assistant + escalation | moderate | payments/medical/legal advice |
| Voice transcription summary | clinics, sales, ops | transcription + summary | high if sensitive | consent unclear |

## Matching Rules

Pattern matching should use:

- workflow signals;
- pain points;
- systems involved;
- data classes;
- volume/frequency;
- integration feasibility;
- evaluation clarity;
- privacy mode.

The matched pattern is only a recommendation input. Final recommendation still
requires scoring, cost assumptions, privacy gates, and human review.
