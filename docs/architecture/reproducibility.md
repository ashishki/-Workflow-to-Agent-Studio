# Reproducibility

Purpose: make roadmap generation auditable and reviewable.

## Record With Every Report

- report ID;
- source document IDs;
- source fingerprints/hashes;
- redaction policy version;
- schema versions;
- prompt versions;
- model provider and model name;
- pattern library version;
- scoring model version;
- cost model version;
- privacy model version;
- generation timestamp;
- reviewer status;
- validation findings;
- export path and export timestamp.

## Reproducibility Receipt

The `roadmap_proof_receipt.json` should include:

```json
{
  "report_schema_version": "roadmap_report:v1",
  "source_hashes": [],
  "prompt_versions": {},
  "model_metadata": {},
  "pattern_library_version": "smb_patterns:v1",
  "privacy_model_version": "privacy_model:v1",
  "cost_model_version": "cost_model:v1",
  "scoring_model_version": "priority_model:v1",
  "claim_count": 0,
  "assumption_count": 0,
  "blocking_finding_count": 0,
  "review_status": "draft"
}
```

## Deterministic Demo Mode

For synthetic demos, the product should support deterministic outputs so docs,
evals, and review artifacts can be regenerated without external credentials.

## Pilot Evidence Boundary

Reproducible demo reports still do not prove buyer value. Only reviewed pilot
rows in `docs/pilot_measurement.md` can support commercial claims.
