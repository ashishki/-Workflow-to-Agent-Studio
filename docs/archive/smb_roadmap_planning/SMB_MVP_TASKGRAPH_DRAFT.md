# SMB AI Roadmap MVP Task Graph

Version: 1.0
Date: 2026-06-01

This task graph implements the SMB roadmap layer described in
`docs/AI_ROADMAP_STUDIO_INDEX.md`. It is separate from the active framework
graph in `docs/tasks.md` so the current kernel can remain stable while this
commercial planning layer is built.

Each acceptance criterion must be verifiable through tests, generated artifacts,
or deterministic docs checks.

---

## Phase A: Product Contract

Goal: freeze the product surface before code expands.

### SMB-A01: Roadmap Product Contract

Owner: strategist
Phase: A
Type: plan:schema
Depends-On: none

Objective: finalize the RoadmapReport product contract, non-goals, and demo
domain boundaries.

Acceptance-Criteria:

- AC-1: `docs/product/report_contract.md` defines required sections for
  `RoadmapReport v1`.
- AC-2: `docs/product/mvp_scope.md` states that production agent building,
  automatic deployment, ROI guarantees, and compliance certification are out of
  scope.
- AC-3: `docs/AI_ROADMAP_STUDIO_INDEX.md` links product, methodology, security,
  architecture, examples, evals, and backlog docs.

Files:

- `docs/product/report_contract.md`
- `docs/product/mvp_scope.md`
- `docs/AI_ROADMAP_STUDIO_INDEX.md`

Context-Refs:

- `docs/product_strategy.md`
- `docs/spec.md`

### SMB-A02: Commercial Offer Boundary

Owner: human
Phase: A
Type: none
Depends-On: SMB-A01

Objective: approve the first commercial wedge and public claim boundary.

Acceptance-Criteria:

- AC-1: `docs/product/commercial_pilot_offer.md` names the first offer and buyer.
- AC-2: offer states that synthetic demos are not pilot evidence.
- AC-3: offer points buyer-proof claims to `docs/pilot_measurement.md`.

Files:

- `docs/product/commercial_pilot_offer.md`
- `docs/pilot_measurement.md`

Context-Refs:

- `docs/product_strategy.md#commercial-pilot-package`

---

## Phase B: Roadmap Domain Schemas

Goal: add typed contracts before generators.

### SMB-B01: Privacy Domain Model

Owner: codex
Phase: B
Type: plan:schema compliance:control
Depends-On: SMB-A01

Objective: implement privacy classes and source/recommendation classification
schemas.

Acceptance-Criteria:

- AC-1: `PrivacyClass` includes public, internal, confidential, sensitive, and
  restricted.
- AC-2: privacy schema rejects unknown classes with Pydantic validation.
- AC-3: unit tests cover valid classes and invalid class rejection.

Files:

- `workflow_agent_studio/domain/privacy.py`
- `tests/unit/test_privacy_schema.py`

Context-Refs:

- `docs/security/data_classification.md`

### SMB-B02: Recommendation Card Schema

Owner: codex
Phase: B
Type: plan:schema
Depends-On: SMB-B01

Objective: implement `RecommendationCard` with required privacy, cost, time,
risks, validation, evidence, assumptions, and fallback fields.

Acceptance-Criteria:

- AC-1: recommendation without target workflow step fails validation.
- AC-2: recommendation without evidence and without assumptions fails
  validation.
- AC-3: recommendation without fallback fails validation.
- AC-4: tests cover happy path and each blocking invalid case.

Files:

- `workflow_agent_studio/domain/recommendation.py`
- `tests/unit/test_recommendation_schema.py`

Context-Refs:

- `docs/product/report_contract.md#6-recommendation-cards`

### SMB-B03: Costing Domain Model

Owner: codex
Phase: B
Type: plan:schema
Depends-On: SMB-B02

Objective: implement cost estimate schemas with one-time/monthly ranges,
assumptions, confidence, and price-card references.

Acceptance-Criteria:

- AC-1: low, medium, high cost ordering is validated.
- AC-2: estimate without assumptions fails validation.
- AC-3: estimate confidence supports low, medium, and high.
- AC-4: tests cover invalid ordering and missing assumptions.

Files:

- `workflow_agent_studio/domain/costing.py`
- `tests/unit/test_costing_schema.py`

Context-Refs:

- `docs/methodology/cost_estimation.md`

### SMB-B04: Scoring Domain Model

Owner: codex
Phase: B
Type: plan:schema
Depends-On: SMB-B02

Objective: implement priority score schemas for business value, delivery
readiness, risk penalty, priority band, confidence, rationale, and uncertainty.

Acceptance-Criteria:

- AC-1: priority band supports quick_win, strategic_pilot, prepare_first,
  do_not_automate_yet, classic_automation, and human_only.
- AC-2: score output requires rationale and uncertainty notes.
- AC-3: tests verify invalid band rejection.

Files:

- `workflow_agent_studio/domain/scoring.py`
- `tests/unit/test_priority_scoring_schema.py`

Context-Refs:

- `docs/methodology/scoring_model.md`

### SMB-B05: Verification Domain Model

Owner: codex
Phase: B
Type: compliance:evidence plan:schema
Depends-On: SMB-B02

Objective: implement claims, assumptions, evidence items, recommendation traces,
and verification receipt schemas.

Acceptance-Criteria:

- AC-1: claim requires claim type, evidence level, confidence, and status.
- AC-2: assumption requires impact, verification method, owner, and status.
- AC-3: recommendation trace records pattern, cost model, scoring model, and
  privacy model versions.
- AC-4: receipt records source hashes and report schema version.

Files:

- `workflow_agent_studio/domain/verification.py`
- `tests/unit/test_verification_receipt.py`

Context-Refs:

- `docs/methodology/verification_model.md`

### SMB-B06: Roadmap Report Schema

Owner: codex
Phase: B
Type: plan:schema
Depends-On: SMB-B01, SMB-B02, SMB-B03, SMB-B04, SMB-B05

Objective: implement the `RoadmapReport` aggregate schema.

Acceptance-Criteria:

- AC-1: report requires executive summary, evidence packet, workflow map,
  process inventory, recommendations, rollout plan, evaluation plan, governance
  plan, and verification appendix.
- AC-2: report fails validation when recommendations list is empty and no
  do-not-automate rationale is provided.
- AC-3: JSON fixture round-trips through Pydantic serialization.

Files:

- `workflow_agent_studio/domain/roadmap.py`
- `tests/unit/test_roadmap_report_schema.py`
- `tests/fixtures/roadmaps/minimal_valid_roadmap.json`

Context-Refs:

- `docs/product/report_contract.md`

---

## Phase C: Privacy And Redaction

Goal: make privacy mode a deterministic planning constraint.

### SMB-C01: Deterministic Privacy Classifier

Owner: codex
Phase: C
Type: compliance:control
Depends-On: SMB-B01

Objective: implement deterministic field/snippet classification for PII,
secrets, legal, health, payment, tax, HR, and identity hints.

Acceptance-Criteria:

- AC-1: classifier marks email, phone, address, passport/ID-like, payment-like,
  and API-key-like examples.
- AC-2: legal/immigration fixture is classified restricted.
- AC-3: salon fixture is classified sensitive, not restricted.
- AC-4: false-positive fixture remains internal or confidential as expected.

Files:

- `workflow_agent_studio/privacy/classifier.py`
- `tests/unit/test_privacy_classifier.py`
- `tests/fixtures/smb/`

Context-Refs:

- `docs/security/data_classification.md`
- `docs/evals/privacy_classification_eval.md`

### SMB-C02: Redaction Preview

Owner: codex
Phase: C
Type: compliance:control
Depends-On: SMB-C01

Objective: implement deterministic redaction preview that masks detected secrets
and personal values while preserving field names and workflow meaning.

Acceptance-Criteria:

- AC-1: preview replaces emails, phones, addresses, IDs, card-like values, and
  API keys with stable placeholders.
- AC-2: preview reports redaction counts by type.
- AC-3: original raw values do not appear in preview output.
- AC-4: tests cover mixed synthetic/real examples.

Files:

- `workflow_agent_studio/privacy/redaction.py`
- `tests/unit/test_redaction_preview.py`

Context-Refs:

- `docs/security/redaction_policy.md`

### SMB-C03: Cloud/Private/Local Policy Gate

Owner: codex
Phase: C
Type: compliance:control plan:validation
Depends-On: SMB-C01, SMB-C02

Objective: block unsafe model-mode recommendations based on privacy class and
redaction status.

Acceptance-Criteria:

- AC-1: restricted data blocks lightweight cloud recommendation unless source is
  synthetic/redacted and report states the condition.
- AC-2: sensitive data requires redaction note for cloud mode.
- AC-3: high-risk legal/medical/financial/HR domains require human review gate.
- AC-4: tests cover legal consultancy, e-commerce, and hair salon fixtures.

Files:

- `workflow_agent_studio/validators/privacy.py`
- `tests/unit/test_privacy_policy_gate.py`

Context-Refs:

- `docs/security/cloud_vs_local_decision.md`

---

## Phase D: Pattern Library

Goal: create versioned SMB implementation patterns.

### SMB-D01: Implementation Pattern Schema

Owner: codex
Phase: D
Type: plan:schema
Depends-On: SMB-B02

Objective: implement schema and loader for SMB implementation patterns.

Acceptance-Criteria:

- AC-1: pattern schema validates pattern ID, version, signals, required data,
  privacy default, architecture, risks, eval metrics, and when-not-to-use.
- AC-2: invalid JSON pattern fails with clear validation error.
- AC-3: loader returns pattern version metadata.

Files:

- `workflow_agent_studio/patterns/smb.py`
- `workflow_agent_studio/patterns/smb/`
- `tests/unit/test_smb_pattern_library.py`

Context-Refs:

- `docs/methodology/implementation_patterns.md`

### SMB-D02: MVP Pattern Pack

Owner: strategist
Phase: D
Type: none
Depends-On: SMB-D01

Objective: add 10-15 versioned SMB pattern JSON files.

Acceptance-Criteria:

- AC-1: pattern pack includes support triage, knowledge assistant, sales email,
  lead qualification, document extraction, invoice processing, appointment
  booking, legal checklist, e-commerce returns, reporting automation, and
  messaging support bot.
- AC-2: every pattern includes when-not-to-use.
- AC-3: pattern library tests validate all JSON files.

Files:

- `workflow_agent_studio/patterns/smb/*.json`
- `tests/unit/test_smb_pattern_library.py`

Context-Refs:

- `docs/methodology/implementation_patterns.md#mvp-pattern-set`

### SMB-D03: Pattern Matching Baseline

Owner: codex
Phase: D
Type: plan:validation
Depends-On: SMB-D01, SMB-D02, SMB-C03

Objective: match opportunities to patterns with anti-matches and privacy checks.

Acceptance-Criteria:

- AC-1: hair salon reminder maps to deterministic reminder/appointment pattern,
  not high-autonomy agent.
- AC-2: e-commerce returns maps to human-in-the-loop returns assistant, not
  automatic refund.
- AC-3: legal checklist maps to private checklist assistant, not legal advice
  automation.
- AC-4: pattern matching eval doc records expected matches.

Files:

- `workflow_agent_studio/roadmap/pattern_matching.py`
- `tests/eval/test_pattern_matching_eval.py`
- `docs/evals/pattern_matching_eval.md`

Context-Refs:

- `docs/evals/pattern_matching_eval.md`

---

## Phase E: Cost And Priority Engines

Goal: produce honest ranges and priority bands.

### SMB-E01: Cost Engine

Owner: codex
Phase: E
Type: plan:validation
Depends-On: SMB-B03, SMB-D01

Objective: implement deterministic cost range generation from pattern, scope,
privacy mode, volume, and assumptions.

Acceptance-Criteria:

- AC-1: engine returns one-time and monthly low/medium/high ranges.
- AC-2: engine requires assumptions and confidence.
- AC-3: local/private mode includes infra and maintenance overhead.
- AC-4: tests cover reminder, support assistant, and private document assistant.

Files:

- `workflow_agent_studio/costing/engine.py`
- `workflow_agent_studio/costing/price_cards.py`
- `tests/unit/test_cost_engine.py`

Context-Refs:

- `docs/methodology/cost_estimation.md`
- `docs/evals/cost_estimation_eval.md`

### SMB-E02: Priority Scoring Engine

Owner: codex
Phase: E
Type: plan:validation
Depends-On: SMB-B04, SMB-C03, SMB-D03

Objective: implement priority banding from business value, delivery readiness,
risk penalty, and confidence.

Acceptance-Criteria:

- AC-1: high value/high readiness/low risk maps to quick_win.
- AC-2: high privacy risk and low evaluation clarity maps to prepare_first or
  do_not_automate_yet.
- AC-3: deterministic reminder can map to classic_automation.
- AC-4: output includes uncertainty notes.

Files:

- `workflow_agent_studio/scoring/priority.py`
- `tests/unit/test_priority_scoring.py`

Context-Refs:

- `docs/methodology/scoring_model.md`

---

## Phase F: Roadmap Generation And Export

Goal: generate a complete RoadmapReport and Markdown export.

### SMB-F01: Roadmap Assembly Service

Owner: codex
Phase: F
Type: plan:schema plan:validation
Depends-On: SMB-B06, SMB-C03, SMB-D03, SMB-E01, SMB-E02

Objective: assemble workflow map, opportunities, privacy results, pattern
matches, costs, scores, and verification data into `RoadmapReport`.

Acceptance-Criteria:

- AC-1: service creates a valid RoadmapReport from each of the three demo inputs.
- AC-2: report includes do-not-automate items.
- AC-3: report includes privacy mode recommendation.
- AC-4: report includes verification appendix.

Files:

- `workflow_agent_studio/roadmap/service.py`
- `tests/integration/test_roadmap_generation.py`

Context-Refs:

- `docs/product/report_contract.md`

### SMB-F02: Roadmap Markdown Export

Owner: codex
Phase: F
Type: none
Depends-On: SMB-F01

Objective: export RoadmapReport to stable Markdown with recommendation cards and
verification appendix.

Acceptance-Criteria:

- AC-1: export includes all required report sections in stable order.
- AC-2: draft export is visibly labeled as draft.
- AC-3: verification appendix includes claims and assumptions.
- AC-4: local export path constraints remain enforced.

Files:

- `workflow_agent_studio/reporting/roadmap_markdown.py`
- `workflow_agent_studio/export/roadmap.py`
- `tests/integration/test_roadmap_markdown_export.py`

Context-Refs:

- `docs/product/report_contract.md`
- `workflow_agent_studio/export/paths.py`

### SMB-F03: Roadmap CLI Command

Owner: codex
Phase: F
Type: none
Depends-On: SMB-F01, SMB-F02

Objective: add a local CLI command that generates a roadmap from a business
profile/input file.

Acceptance-Criteria:

- AC-1: command accepts database, run ID, business profile, privacy mode, and
  output path.
- AC-2: command can generate the hair salon demo report without external
  credentials.
- AC-3: invalid privacy mode exits nonzero with clear error.
- AC-4: integration test covers command success and invalid mode.

Files:

- `workflow_agent_studio/cli.py`
- `tests/integration/test_roadmap_cli.py`
- `docs/operator_guide.md`

Context-Refs:

- `docs/examples/domains/hair_salon_input.md`

---

## Phase G: Demo Reports And Evals

Goal: prove the MVP mechanics on three polished synthetic demos.

### SMB-G01: Demo Fixture Pack

Owner: strategist
Phase: G
Type: none
Depends-On: SMB-F03

Objective: add canonical demo fixtures for hair salon, e-commerce, and legal
consultancy.

Acceptance-Criteria:

- AC-1: each fixture states synthetic demo boundary.
- AC-2: each fixture includes workflow steps, actors, systems, pain points, data
  fields, sensitive-data notes, and do-not-automate boundaries.
- AC-3: fixtures are referenced by README or index.

Files:

- `docs/examples/domains/hair_salon_input.md`
- `docs/examples/domains/ecommerce_input.md`
- `docs/examples/domains/legal_consultancy_input.md`
- `docs/AI_ROADMAP_STUDIO_INDEX.md`

Context-Refs:

- `docs/product/mvp_scope.md`

### SMB-G02: Golden Demo Roadmaps

Owner: strategist
Phase: G
Type: none
Depends-On: SMB-G01

Objective: produce client-readable golden reports for the three demo fixtures.

Acceptance-Criteria:

- AC-1: each report includes recommendation cards, do-not-automate items,
  privacy mode, cost/time ranges, rollout plan, and verification appendix.
- AC-2: legal consultancy report blocks legal advice automation and unrestricted
  cloud analysis.
- AC-3: e-commerce report blocks automatic refunds.
- AC-4: hair salon report recommends deterministic reminders before AI.

Files:

- `docs/examples/roadmaps/hair_salon_roadmap.md`
- `docs/examples/roadmaps/ecommerce_roadmap.md`
- `docs/examples/roadmaps/legal_consultancy_roadmap.md`

Context-Refs:

- `docs/evals/roadmap_quality_eval.md`

### SMB-G03: Roadmap Eval Suite

Owner: codex
Phase: G
Type: plan:validation
Depends-On: SMB-F02, SMB-G02

Objective: implement automated evals for roadmap quality, privacy
classification, cost estimation, pattern matching, and recommendation
verification.

Acceptance-Criteria:

- AC-1: eval tests assert no forbidden claims in demo reports.
- AC-2: eval tests assert every recommendation has evidence or assumptions.
- AC-3: privacy eval blocks unrestricted cloud mode for legal consultancy.
- AC-4: cost eval rejects single-point estimates.

Files:

- `tests/eval/test_roadmap_quality_eval.py`
- `tests/eval/test_privacy_classification_eval.py`
- `tests/eval/test_cost_estimation_eval.py`
- `tests/eval/test_pattern_matching_eval.py`
- `tests/eval/test_recommendation_verification_eval.py`

Context-Refs:

- `docs/evals/`

---

## Phase H: Review And Pilot Packaging

Goal: make output reviewable and commercially testable without overclaiming.

### SMB-H01: Review Checklist And Findings

Owner: codex
Phase: H
Type: plan:validation compliance:evidence
Depends-On: SMB-G03

Objective: add reviewer checklist output for each recommendation.

Acceptance-Criteria:

- AC-1: reviewer output includes accepted, reason, missing evidence, cost
  realism, privacy concern, would-show-to-client, and required changes.
- AC-2: unresolved blocking findings prevent approved export.
- AC-3: tests cover blocked and accepted review states.

Files:

- `workflow_agent_studio/roadmap/review.py`
- `tests/integration/test_roadmap_review.py`

Context-Refs:

- `docs/evals/recommendation_verification_eval.md`

### SMB-H02: Pilot Measurement Extension

Owner: human
Phase: H
Type: compliance:evidence
Depends-On: SMB-H01

Objective: extend pilot measurement fields for roadmap-specific proof.

Acceptance-Criteria:

- AC-1: `docs/pilot_measurement.md` can record roadmap readiness, privacy
  finding count, recommendation acceptance count, and would-show-to-client.
- AC-2: document states synthetic demo reports do not satisfy pilot proof.
- AC-3: docs tests verify the pilot proof boundary.

Files:

- `docs/pilot_measurement.md`
- `tests/unit/test_docs.py`

Context-Refs:

- `docs/product/commercial_pilot_offer.md`

### SMB-H03: Consultant Handoff Export

Owner: codex
Phase: H
Type: none
Depends-On: SMB-H01

Objective: export a scoped implementation handoff from approved roadmap
recommendations.

Acceptance-Criteria:

- AC-1: handoff includes tasks, acceptance criteria, eval cases, risks, owner,
  privacy mode, and human gates.
- AC-2: unapproved or blocked roadmap cannot produce approved handoff.
- AC-3: handoff never claims production deployment has occurred.

Files:

- `workflow_agent_studio/export/roadmap_handoff.py`
- `tests/integration/test_roadmap_handoff_export.py`
- `docs/operator_guide.md`

Context-Refs:

- `docs/backlog/ai_loop_development_plan.md`

---

## V2 Backlog Pointer

After MVP proof, continue with `docs/backlog/v2_backlog.md`.
