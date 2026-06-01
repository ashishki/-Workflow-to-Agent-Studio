# Verification Model

Purpose: apply evidence and audit discipline to every roadmap recommendation.

This model follows the same governance spirit as the existing evidence-linked
kernel: claims must be grounded or explicitly marked as assumptions.

## Claim Types

- observation;
- inference;
- recommendation;
- cost estimate;
- risk assessment;
- privacy classification;
- priority score;
- implementation assumption.

## Evidence Levels

- direct evidence;
- inferred from multiple sources;
- pattern-based;
- assumption only;
- unsupported - blocked.

## Claim Registry

```yaml
claim_id: CLM-001
claim_text: Support requests are manually triaged in Gmail.
claim_type: observation
source_refs:
  - source_id: SRC-001
    chunk_id: CH-002
evidence_level: direct
confidence: high
created_by: workflow_decomposer:v1
status: accepted
reviewer_notes: []
```

## Assumptions Registry

```yaml
assumption_id: ASM-001
text: The company receives at least 50 support messages per week.
impact_if_wrong: Automation may not be worth implementing.
verification_method: Ask owner for weekly support volume.
owner: business_owner
expires_at_stage: before implementation
status: unresolved
```

## Recommendation Trace

```yaml
recommendation_id: REC-003
target_step_id: WF-RETURNS-04
matched_pattern_id: customer_support_triage:v1
supporting_claims:
  - CLM-004
  - CLM-009
cost_model_version: cost_model:v1
scoring_model_version: priority_model:v1
privacy_model_version: privacy_model:v1
decision_log_id: DEC-002
review_status: needs_human_review
```

## Deterministic Checks

Block export when:

- a recommendation lacks a workflow step;
- a recommendation lacks evidence and lacks assumptions;
- a cost range lacks assumptions;
- cloud is recommended for restricted data without redaction/private controls;
- high-autonomy is recommended for a high-risk workflow;
- "guaranteed ROI" appears;
- "fully compliant" appears without certification evidence;
- "no human needed" appears for high-risk work;
- high-risk recommendations lack human approval gates;
- recommendations lack fallback options;
- score bands lack uncertainty notes.

## Export Artifacts

Roadmap export should include:

- `roadmap.md`;
- `roadmap_proof_receipt.json`;
- `claims_registry.json`;
- `assumptions_registry.json`;
- `evidence_table.md`;
- `decision_log.md`.
