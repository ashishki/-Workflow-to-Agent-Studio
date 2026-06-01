# AI Roadmap Studio Documentation Index

Status: planning layer for the SMB AI implementation roadmap product.

This documentation set translates the strategic review into a concrete product
contract and development loop. It does not replace the existing local
evidence-linked blueprint kernel. It adds the commercial roadmap layer needed to
position Workflow-to-Agent Studio as an AI implementation planning tool for
small and medium businesses.

## Core Decision

Workflow-to-Agent Studio should be sold as a pre-implementation AI roadmap
studio, not as an agent builder.

The product promise:

> Convert company workflow evidence into a verified AI implementation roadmap:
> what to automate, what not to automate, which solution type fits, which data is
> needed, which privacy mode is safe, what it may cost, who must review it, and
> how implementation should be staged.

## Reading Order

1. `docs/product/vision.md`
2. `docs/product/report_contract.md`
3. `docs/product/mvp_scope.md`
4. `docs/security/privacy_modes.md`
5. `docs/methodology/workflow_analysis.md`
6. `docs/methodology/implementation_patterns.md`
7. `docs/methodology/cost_estimation.md`
8. `docs/methodology/scoring_model.md`
9. `docs/methodology/verification_model.md`
10. `docs/architecture/smb_roadmap_architecture.md`
11. `docs/prompts/roadmap_prompt_contracts.md`
12. `docs/tasks.md#phase-14-smb-ai-roadmap-product-layer`
13. `docs/CODEX_PROMPT.md`

## Demo Packs

The first three demo packs are deliberately synthetic and must not be presented
as pilot proof:

- `docs/examples/domains/hair_salon_input.md`
- `docs/examples/roadmaps/hair_salon_roadmap.md`
- `docs/examples/domains/ecommerce_input.md`
- `docs/examples/roadmaps/ecommerce_roadmap.md`
- `docs/examples/domains/legal_consultancy_input.md`
- `docs/examples/roadmaps/legal_consultancy_roadmap.md`

## Development Boundaries

- Keep the current local-first architecture.
- Keep typed Pydantic schemas and deterministic validators.
- Keep the evidence-or-assumption rule.
- Keep immutable versions, audit events, review workspace, and Markdown export.
- Do not build production agents in this phase.
- Do not claim ROI, compliance certification, or buyer validation from demo
  fixtures.
- Do not recommend high-autonomy automation for high-risk legal, medical,
  financial, or HR decisions.

## Required Proof Before Commercial Claims

Commercial claims require real pilot evidence recorded in
`docs/pilot_measurement.md`. Synthetic reports, public-source demos, and
sanitized fixtures can show mechanics only.

## Archived Drafts

The original separate SMB-loop draft taskgraph was folded into active Phase 14 in
`docs/tasks.md`. Historical copies live under:

- `docs/archive/smb_roadmap_planning/`
- `docs/archive/roadmap_prompt_contracts/`
