# AI Product Development Phases

Purpose: define how Workflow-to-Agent Studio matures from a local discovery MVP into an evidence-backed automation readiness product.

The product should not compete as another generic agent builder or one-off ChatGPT prompt. Its durable role is the pre-production layer for AI automation: prove what should be automated, what must stay human-approved, what evidence supports the plan, and how success will be evaluated before anyone builds or deploys an agent.

## Product Thesis

Companies are experimenting with AI agents faster than they can standardize discovery, governance, and evaluation. The market does not need more demos that turn a prompt into an automation. It needs repeatable decision artifacts that help teams decide whether an automation is ready, safe, worth building, and testable.

Workflow-to-Agent Studio should become an evidence-first system of record for pre-agent discovery.

Core promise:

- turn messy workflow evidence into a structured automation blueprint
- identify missing questions before implementation starts
- block unsupported or unsafe automation claims
- generate eval cases and implementation tasks
- preserve review, approval, versioning, and audit history

## Phase 0: Local Evidence-Linked MVP

Status: implemented.

Strategic goal:

- Prove that a local CLI can produce a useful draft blueprint from a workflow source without external side effects.

Current capability:

- local source ingestion
- source fingerprinting and duplicate detection
- text-only chunking, fake embeddings, and local retrieval index
- query-time evidence retrieval with `insufficient_evidence`
- workflow extraction
- blueprint synthesis
- deterministic validation gate
- immutable blueprint versions
- local Markdown export
- operator docs and pilot measurement template

AI development scope:

- deterministic scaffolding first
- typed schemas for all generated artifacts
- fake providers in tests
- LLM provider boundary present but not yet the primary production path

Exit criteria:

- CLI can run from sample SOP to draft Markdown export
- unsupported source exits with code 2 and finding IDs
- all important claims require evidence or explicit assumption
- tests, ruff, retrieval eval, and plan eval are green

Market proof:

- one operator can generate a reviewable blueprint from a simple SOP locally

Risks:

- output is still deterministic and generic
- no real interview/transcript corpus yet
- no measured pilot result from a real customer workflow yet

## Phase 1: Evidence Capture And Corpus Expansion

Strategic goal:

- Make the product useful on real discovery inputs, not only clean SOP fixtures.

User value:

- operators can import messy source material from discovery calls, docs, notes, forms, and integration snippets
- the system keeps every claim grounded to the source material

AI development scope:

- transcript ingestion
- pasted notes ingestion
- URL or document snapshot ingestion
- source type labels: `sop`, `transcript`, `interview_notes`, `integration_doc`, `policy`, `prior_blueprint`
- source confidentiality rules
- quote extraction and snippet references
- source quality scoring

Data model changes:

- source provenance fields
- source confidence
- source owner or origin label
- source date and freshness
- source sensitivity findings

Eval requirements:

- messy transcript fixture
- partial notes fixture
- integration-doc fixture
- no-answer fixture for irrelevant sources
- citation precision checks on extracted claims

Exit criteria:

- at least three realistic source types produce grounded workflow facts
- irrelevant source material blocks blueprint generation
- evidence appendix can trace claims back to source chunks

Market proof:

- an AI automation consultant can upload real discovery notes and get a useful first-pass workflow map

Risks:

- transcripts are noisy and may require speaker/section cleanup
- source confidentiality and redaction must be enforced before broader import support

## Phase 2: Retrieval And Evidence Engine

Strategic goal:

- Move from simple RAG to workflow-aware evidence retrieval.

User value:

- the product can answer specific discovery questions from the corpus
- missing evidence is explicit instead of hidden by fluent generation

AI development scope:

- workflow-specific query planner
- retrieval slices for actors, systems, fields, exceptions, approvals, integrations, risks, eval cases
- pattern-library retrieval
- prior-blueprint retrieval
- freshness and corpus version checks
- evidence confidence scoring

Core retrieval questions:

- who participates in the workflow?
- what systems are touched?
- what data fields are required?
- where are approval boundaries?
- what exceptions or edge cases exist?
- what integrations are implied?
- what is unsupported by evidence?

Eval requirements:

- hit@3 and hit@5 by section
- MRR by section
- citation precision by section
- no-answer accuracy for unsupported claims
- regression slices for approval boundaries and data fields

Exit criteria:

- retrieval can support each required blueprint section or return `insufficient_evidence`
- section-level citation precision is tracked
- retrieval eval history records corpus version and exact eval source

Market proof:

- users trust the product because it says "not enough evidence" as often as it drafts

Risks:

- generic vector search can retrieve plausible but wrong chunks
- pattern library can overpower actual customer evidence if weighting is wrong

## Phase 3: Structured LLM Extraction And Synthesis

Strategic goal:

- Use LLMs where they create leverage, while keeping safety-critical judgment deterministic.

User value:

- better extraction from messy language
- richer blueprint drafts
- fewer manual edits before review

AI development scope:

- production LLM provider integration
- model routing by task: extraction, synthesis, missing-question generation, repair suggestions
- structured output only
- schema repair retries
- prompt registry and prompt versioning
- token/cost accounting
- redaction before model calls
- prompt injection checks for source text

Architecture rules:

- LLM drafts; deterministic validators decide approval eligibility
- raw model text must not become authoritative state
- every generated section must parse into versioned schemas
- unsupported evidence cannot be converted into supported claims

Eval requirements:

- extraction accuracy by section
- synthesis required-section coverage
- evidence-link coverage
- hallucinated claim count
- schema repair success rate
- cost per blueprint

Exit criteria:

- real LLM output improves human acceptance rate over deterministic baseline
- unsupported claim rate remains below the threshold defined in `docs/plan_eval.md`
- no generated claim bypasses evidence/assumption validation

Market proof:

- first real users report that the draft saves meaningful discovery/spec writing time

Risks:

- LLM output can become generic
- repair loops can hide prompt quality problems
- cost can spike if extraction is not chunk-scoped

## Phase 4: Automation Readiness And Governance

Strategic goal:

- Turn the blueprint into a decision artifact: ready, not ready, human-in-loop only, or not worth automating.

User value:

- teams can decide whether to build an agent before spending engineering time
- risky automation candidates are blocked or downgraded

AI development scope:

- automation readiness score
- section-level readiness diagnostics
- missing-question engine
- risk classifier
- approval-boundary classifier
- integration readiness checks
- evalability score

Readiness dimensions:

- workflow clarity
- data availability
- system access clarity
- exception complexity
- approval clarity
- evidence coverage
- evalability
- risk level
- implementation effort band

Verdicts:

- `ready_for_automation`
- `ready_for_human_in_loop_copilot`
- `needs_more_discovery`
- `not_safe_to_automate_yet`
- `not_worth_automating`

Eval requirements:

- readiness fixture set with expected verdicts
- false-positive policy for unsafe automation
- missing-question recall checks
- approval-boundary regression tests

Exit criteria:

- every blueprint has a readiness verdict
- every blocking verdict includes repair questions
- unsafe candidates cannot be exported as approved

Market proof:

- consultants can use the verdict to scope or reject automation work with clients

Risks:

- scoring can become arbitrary unless tied to reviewer outcomes
- "readiness" must stay explainable, not a black-box number

## Phase 5: Review Workspace And Human Editing

Strategic goal:

- Make human review a first-class product workflow instead of a manual Markdown step.

User value:

- operators can review, edit, accept, reject, and approve sections with version history

AI development scope:

- review UI or structured CLI review flow
- per-section review state
- reviewer comments
- missing-question answer capture
- section regeneration with evidence constraints
- diff view between blueprint versions
- approval workflow

Data model changes:

- section IDs
- section review status
- reviewer notes
- accepted/rejected generated claims
- missing-question answers
- edit provenance

Eval requirements:

- reviewer edit count
- section acceptance rate
- time to approved draft
- invalid approval blocking
- version mismatch blocking

Exit criteria:

- an operator can complete review without editing raw JSON or Markdown
- approved export always maps to an immutable version
- reviewer edits are measured for pilot proof

Market proof:

- users can use the product in a real client discovery workflow, not just as a developer demo

Risks:

- UI can expand scope too early
- review UX must stay fast enough for consultants and ops teams

## Phase 6: Vertical Blueprint Packs

Strategic goal:

- Stop being generic by shipping opinionated packs for high-value workflows.

User value:

- outputs become more specific, useful, and credible for common automation projects

Initial verticals:

- customer support triage
- sales ops and CRM hygiene
- invoice or back-office processing
- recruiting pipeline
- internal IT helpdesk
- client onboarding

Each vertical pack includes:

- expected source types
- required blueprint sections
- common systems
- common risks
- approval-boundary patterns
- integration checklist
- eval-case templates
- unsafe automation red flags
- implementation task templates

AI development scope:

- vertical classifier
- pack-specific retrieval weighting
- pack-specific validation rules
- pack-specific eval fixtures
- vertical readiness thresholds

Eval requirements:

- per-vertical fixture corpus
- per-vertical readiness verdict checks
- pack-specific missing-question tests
- pack-specific forbidden-claim tests

Exit criteria:

- at least three vertical packs produce better acceptance rate than the generic pack
- each pack has docs, fixtures, evals, and known red flags

Market proof:

- narrow use-case positioning improves conversion: "support triage discovery" sells better than "general AI workflow tool"

Risks:

- too many verticals dilute quality
- packs need real user feedback, not invented templates

## Phase 7: Pilot Proof And Commercial Packaging

Strategic goal:

- Prove that the product saves time and improves blueprint quality in real workflows.

User value:

- buyers can see measurable ROI before adopting it across teams

Pilot measurement fields:

- workflow source duration
- time to reviewable blueprint
- required-section acceptance rate
- reviewer edit count
- critical missing-question count
- automation readiness verdict
- implementation handoff acceptance

Success thresholds:

- under 30 minutes to reviewable blueprint
- at least 80 percent required-section acceptance after human review
- critical missing questions surfaced before implementation
- no approved blueprint with blocking findings

AI development scope:

- measurement collection
- pilot report generation
- anonymized aggregate metrics
- reviewer feedback capture
- improvement backlog from failed pilots

Commercial packaging:

- consultant/agency workflow package
- internal automation team package
- vertical blueprint pack add-ons
- team review/audit package

Exit criteria:

- at least three real pilot rows are filled
- one repeat user runs a second workflow through the product
- a human engineer says the artifact is useful for implementation scoping

Risks:

- users may value the consulting process more than the software unless the workflow is fast and repeatable
- the product must avoid claiming production-readiness from draft-only evidence

## Phase 8: Integrations And Controlled Handoff

Strategic goal:

- Move from local artifact to controlled handoff into execution systems without becoming an unsafe agent builder.

User value:

- teams can move approved implementation tasks into their normal systems

Possible integrations:

- Linear or Jira issue draft export
- GitHub issue draft export
- Notion or Google Docs export
- Slack notification for review request
- code-agent handoff package

Required controls:

- approved version required
- no blocking findings
- explicit human action
- export audit event
- path or destination allowlist
- integration-specific ADR before side effects

AI development scope:

- tool catalog
- export adapters
- human approval gate
- signed handoff package
- integration evals

Exit criteria:

- first external export is draft-only or human-approved
- every external side effect has audit trail and rollback guidance
- no autonomous production mutation

Market proof:

- handoff reduces time from approved blueprint to engineering backlog

Risks:

- adding integrations too early turns the product into another workflow automation tool
- external side effects require stronger governance and permissions

## Phase 9: Learning System And Moat

Strategic goal:

- Build a compounding workflow intelligence dataset from real reviewed blueprints.

User value:

- the product gets better at asking missing questions, identifying risks, and creating useful evals

Data to learn from:

- rejected claims
- reviewer edits
- missing questions answered
- sections accepted without edits
- readiness verdict outcomes
- automation candidates that reached implementation
- eval cases that caught failures
- vertical-specific red flags

AI development scope:

- anonymized learning records
- feedback schema
- reviewer outcome labels
- pack improvement pipeline
- eval fixture generation from accepted/rejected cases

Moat:

- workflow-specific review outcomes
- vertical risk patterns
- missing-question corpus
- eval case library from real projects
- readiness scoring calibrated by human review

Exit criteria:

- each new pilot improves at least one eval or vertical pack
- product can explain how feedback changed templates, rules, or prompts

Risks:

- privacy and confidentiality must be designed before aggregate learning
- learning from weak user edits can degrade quality if not reviewed

## Cross-Phase Engineering Principles

- Prefer evidence over fluent text.
- Prefer structured schemas over markdown-only output.
- Prefer deterministic gates for approval, export, safety, and evaluation.
- Never allow unsupported retrieval to become supported claims.
- Keep local-first behavior until external side effects have ADRs and approval gates.
- Treat review edits as product data, not incidental user changes.
- Make evals mandatory for every new AI behavior.

## AI Development Backlog By Capability

Evidence:

- source provenance
- quote extraction
- evidence confidence
- evidence freshness
- section-level citation precision

Reasoning:

- structured extraction
- blueprint synthesis
- missing-question generation
- readiness explanation
- repair suggestions

Validation:

- evidence coverage
- required sections
- forbidden autonomy claims
- approval boundaries
- eval-case completeness
- version/export integrity

Evaluation:

- retrieval evals
- planning evals
- readiness verdict evals
- pilot proof metrics
- reviewer acceptance metrics

Product:

- operator review workspace
- vertical packs
- pilot reports
- controlled external handoff
- learning loop

## Near-Term Recommended Sequence

1. Run three real workflow pilots with the current CLI.
2. Fill `docs/pilot_measurement.md` after each human review.
3. Identify the first vertical pack from the strongest pilot.
4. Add real LLM extraction/synthesis behind the existing schema gates.
5. Add missing-question engine and readiness verdict.
6. Build review UI only after reviewer edit patterns are clear.
