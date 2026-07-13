# Public n8n Template Source Register

Status: public-source research register; not buyer proof
Captured at: 2026-06-02
Purpose: identify public n8n template corpora that can be mined for workflow
signals and pattern candidates.

## Claim Boundary

These sources can support product mechanics and pattern-library expansion. They
do not prove customer demand, ROI, implementation success, or commercial pilot
readiness.

Raw third-party workflow JSON must not be committed into this repository unless
license review explicitly allows it. The allowed default is to extract metadata:
node types, integrations, triggers, actions, risk signals, data-sensitivity
hints, fingerprints, and normalized pattern candidates.

## Sources

| Source ID | Repository | Source type | Captured at | License status | Allowed use | Limitations | public_demo_only |
|---|---|---|---|---|---|---|---|
| N8N-001 | `enescingoz/awesome-n8n-templates` | public GitHub repository | 2026-06-02 | pending manual review | workflow metadata extraction, dedupe, candidate clustering | template quality and license must be reviewed before copying content | true |
| N8N-002 | `wassupjay/n8n-free-templates` | public GitHub repository | 2026-06-02 | pending manual review | workflow metadata extraction, dedupe, candidate clustering | small repo; may contain duplicated or demo-only workflows | true |
| N8N-003 | `Danitilahun/n8n-workflow-templates` | public GitHub repository | 2026-06-02 | pending manual review | workflow metadata extraction, dedupe, candidate clustering | quality and provenance unknown until review | true |
| N8N-004 | `lucaswalter/n8n-ai-automations` | public GitHub repository | 2026-06-02 | pending manual review | AI workflow signal extraction | AI-heavy templates may overstate autonomy; require safety review | true |
| N8N-005 | `ritik-prog/n8n-automation-templates-5000` | public GitHub repository | 2026-06-02 | pending manual review | large-corpus metadata extraction and dedupe stress test | large volume likely includes duplicates and low-quality templates | true |

## Extracted Fields

The mining pipeline should extract:

- source locator;
- workflow name;
- node types;
- integrations;
- trigger integrations;
- action integrations;
- AI node count;
- human gate signals;
- risky action signals;
- data sensitivity signals;
- stable workflow fingerprint;
- suggested archetype;
- source locator list after dedupe.

## Forbidden Use

- Do not copy raw workflow JSON into committed product artifacts without license
  approval.
- Do not claim these templates are customer proof.
- Do not treat n8n template behavior as safe-by-default implementation guidance.
- Do not import credentials, webhook URLs, private notes, or secrets if they
  appear in a template.
- Do not approve a new SMB pattern without human review.

## Review Path

1. Clone or download public repositories into `.data/` or another ignored local
   workspace.
2. Run the n8n parser against JSON workflows.
3. Dedupe candidates by workflow fingerprint.
4. Cluster candidates by suggested archetype and integration set.
5. Ask a frontier model for missed opportunities and risks only after metadata
   extraction.
6. Convert strong candidates into draft SMB pattern JSON.
7. Human reviewer accepts, rejects, or merges draft patterns.
