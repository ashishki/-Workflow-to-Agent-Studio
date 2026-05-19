# Project Brief: Workflow-to-Agent Studio

Use this document before running `prompts/STRATEGIST.md`. The goal is not to pre-design the system, but to give the Strategist enough context to choose the right solution shape, governance level, runtime tier, and model strategy without guessing.

---

## 1. Project

- **Project name:** Workflow-to-Agent Studio
- **One-sentence summary:** A workflow discovery and automation-spec system that converts messy SOPs, Loom walkthroughs, forms, and operational notes into scoped AI-agent implementation blueprints.
- **Why this project exists:** Companies want AI automation but often cannot describe the workflow clearly enough to build it. Consultants and engineers spend too much time extracting process steps, edge cases, approvals, tools, data sources, risks, and eval requirements before real implementation can start.
- **What success looks like in v1:** An operator uploads or pastes a workflow description, transcript, SOP, or discovery notes and receives a structured automation blueprint: current workflow map, pain points, automation candidates, integration map, human approval boundaries, eval cases, observability needs, rough build effort, and next implementation tasks.

## 1b. Problem Fit and Adoption Reality

Answer these before describing the desired architecture. The Strategist uses
this section to avoid designing a polished AI system around an unproven or
demo-only need.

- **Concrete operational pain:** Discovery for AI automation projects is slow, repetitive, and inconsistent. Stakeholders explain workflows in messy language; engineers must manually translate that into requirements, integration maps, approval boundaries, and eval plans.
- **Current workaround:** Consulting calls, Loom videos, Google Docs, screenshots, manually written specs, Slack follow-ups, and engineer-created implementation plans.
- **Why existing process is insufficient:** Generic notes do not reliably capture edge cases, data contracts, human decisions, failure modes, and measurable acceptance criteria. Ordinary AI summaries produce polished prose but miss implementation boundaries and operational risks.
- **First user / buyer / operator who feels the pain:** AI automation consultants, freelance AI engineers, operations teams, and technical founders who need to turn ambiguous workflows into buildable specs.
- **What would make v1 not worth adopting:** If the generated brief is too generic, misses critical integration details, ignores approval/risk boundaries, lacks eval cases, or still requires the engineer to rewrite the whole spec manually.
- **Adoption proof metric:** The operator can turn a 10-20 minute workflow description into a decision-grade automation brief in under 30 minutes, with at least 80 percent of required implementation sections accepted after human review.
- **Claims that are out of bounds before evidence:** "Automatically builds the agent", "replaces discovery calls", "guarantees implementation accuracy", "fully understands every business process", "production-ready agent builder".
- **Work AI will not replace:** Stakeholder interviews, final scope approval, business accountability, sensitive-process judgment, legal/security review, and final architecture decisions.

## 2. Users and Workflows

- **Primary users / operators:** AI automation engineers, workflow consultants, ops leads, solution architects, and technical founders.
- **Main workflow 1:** Operator imports a workflow source: Loom transcript, SOP, call notes, form payload samples, screenshots described as text, or manually pasted notes.
- **Main workflow 2:** The system extracts actors, systems, steps, triggers, data fields, decisions, exceptions, approvals, current pain points, and candidate automation boundaries.
- **Main workflow 3:** The system produces an implementation-ready blueprint and lets the operator review, edit, approve, and export it into project docs, GitHub issues, or a client-facing proposal.

## 3. Scope

- **In scope for v1:** Text and transcript ingestion, structured workflow extraction, deterministic completeness checks, AI-generated blueprint, risk/approval map, eval-case draft, integration checklist, Markdown export, and evidence-linked source snippets.
- **Out of scope / non-goals:** Full visual process mining, automatic code generation, autonomous deployment, enterprise BPM replacement, high-scale document ingestion, direct production workflow execution, and replacing stakeholder discovery.

## 4. AI Scope

- **Where AI may be needed:** Interpreting messy workflow descriptions, identifying implicit steps, extracting edge cases, drafting automation candidates, generating eval cases, summarizing risks, and turning evidence into a clear implementation brief.
- **Where AI is explicitly not wanted:** Final architecture approval, execution of customer workflows, credential handling, integration testing, estimate arithmetic, security decisions, and audit log writes.
- **Possible retrieval / RAG need:** Yes. The system should retrieve prior workflow briefs, common automation patterns, integration templates, eval templates, guardrail examples, and client-specific SOP context.
- **If retrieval is needed, is text-only likely sufficient or is multimodal evidence truly required:** Text-only is sufficient for v1 if Loom/audio is transcribed before ingestion. Screenshots can be manually described or added later.
- **If multimodal may be needed, which modalities and why:** Later: screenshots of tools/forms, flowcharts, spreadsheet samples, and short screen recordings to capture UI-specific steps that text misses.
- **Possible tool-use need:** Yes. Tools may fetch transcripts, read files, parse docs, write Markdown briefs, create GitHub issues, query prior examples, and optionally generate diagrams.
- **Possible planning / agentic behavior need:** Moderate but bounded. The system can propose missing questions and next discovery steps, but it should not contact stakeholders or mutate production systems automatically.

## 5. Deterministic Candidates

List the parts that probably should stay deterministic unless the Strategist proves otherwise.

- **Validation / policy checks:** Required blueprint sections, evidence links per claim, missing-field checks, sensitive-data flags, forbidden autonomy claims, and minimum eval-case coverage.
- **Routing / decision rules:** Which workflows are ready for implementation, which require more discovery, which need security review, and which automation candidates are too risky for v1.
- **Calculations / transformations:** Completeness score, evidence coverage, integration count, estimated complexity bands, workflow step counts, and field normalization.
- **Retries / idempotency / audit triggers:** Source document fingerprints, run IDs, transcript processing retries, blueprint versioning, review status, and export history.

## 6. Human Approval Boundaries

- **What actions must require human approval:** Final client-facing proposal, implementation scope, cost/timeline estimate, security assumptions, approval boundaries, and creation of execution tickets.
- **What can be automated safely:** Draft extraction, checklist completion, blueprint drafting, missing-question generation, source snippet linking, and initial eval-case generation.
- **Why these boundaries matter:** The system is a discovery accelerator, not a replacement for accountable solution design. Bad automation scope can create real operational risk.

## 7. Risk and Error Cost

- **What is expensive if the system is wrong:** Building the wrong automation, missing a required approval, underestimating integration complexity, or promising unsafe agent behavior.
- **What is expensive if the system is slow:** Discovery remains manual and the product loses its main value. It should be faster than writing the first spec from scratch.
- **What is expensive if the system is inconsistent / variable:** Engineers cannot trust the blueprints, client proposals vary in quality, and reusable patterns do not accumulate.
- **Blast radius if it fails badly:** Medium. It can cause wasted engineering time or incorrect client expectations. It should not directly execute workflows in v1.
- **Audit / explainability needs:** High. Every blueprint assertion should trace back to a source snippet, operator note, or explicit assumption.

## 8. Data

- **Primary data sources:** Loom transcripts, discovery call notes, SOP docs, Google Docs, Notion pages, screenshots described as text, sample forms/webhooks, API docs, client notes, and prior automation briefs.
- **Approximate data volume:** v1 can start with 1-20 source documents per workflow and a library of dozens of prior pattern templates.
- **Does data change frequently:** Yes. Client workflows, tools, fields, and policies can change during discovery.
- **Sensitive / regulated data present:** Potentially yes. Workflow docs may include customer data, internal processes, credentials in screenshots, pricing, or operational details.
- **Retention / deletion expectations:** Keep source snippets and blueprint versions for audit, but support redaction and deletion of sensitive raw inputs.

## 8b. Continuity and Evidence

- **Which decisions are likely to be revisited later:** Scope boundaries, missing questions, architecture choices, eval cases, integration assumptions, risk classification, and stakeholder approvals.
- **What prior evidence or proof will future agents need to find quickly:** Original workflow source snippets, extracted fields, edge cases, assumptions, human edits, rejected automation candidates, and final approved blueprint versions.
- **Will work span multiple sessions / agents / weeks:** Yes. Discovery, strategy, architecture, implementation, and review will often happen across multiple sessions.
- **Any existing docs, ADRs, audits, or notes that should become retrieval anchors:** `AI_workflow_playbook`, `gdev-agent` implementation patterns, `telegram-research-agent` evidence memory, mortgage document-processing workflow notes, and the operator's resume/profile around AI-powered process automation.

## 9. Integrations

- **External APIs / services:** Google Drive/Docs, Notion, Loom transcript export, Slack, GitHub Issues, Airtable/Sheets, optional diagram generation, and LLM provider APIs.
- **Databases / storage:** SQLite for local-first v1; PostgreSQL if multi-user or client workspaces are needed; vector index for prior briefs and pattern retrieval.
- **Auth / identity provider:** Local single-operator access for v1. If client-facing, add authenticated workspaces and role-based access.
- **Webhooks / messaging / queues:** Optional for v1. Later: Slack intake bot, GitHub issue export, webhook for uploaded discovery materials.

## 10. Constraints

- **Preferred stack:** Python, FastAPI or CLI-first, Pydantic schemas, Markdown exports, SQLite/PostgreSQL, structured LLM outputs, deterministic validators, and optionally Mermaid diagrams.
- **Deployment target:** Local/VPS workspace for v1; Docker Compose when adding web UI, database, or background workers.
- **Budget constraints:** Medium. Discovery runs can use stronger reasoning models for final synthesis, but extraction and validation should be routed through cheaper models where possible.
- **Latency / throughput expectations:** A single workflow brief should complete in minutes, not hours. Interactive editing should be fast from stored structured data.
- **Compliance requirements:** No regulated-domain automation claims in v1. Sensitive client data should be redacted from logs and handled through local-first storage by default.
- **Network / security restrictions:** No credential harvesting from screenshots/docs, no production system mutation, secrets in environment/secrets only, and source files treated as confidential by default.

## 11. Runtime and Operations

- **Should runtime stay simple (managed service / container) if possible:** Yes. Start as CLI or local web app. Avoid complex agents until the brief schema and review loop are proven.
- **Any need for shell, package, or toolchain mutation at runtime:** No for v1.
- **Any need for privileged actions or long-lived isolated workers:** No privileged actions. Background jobs may be useful for document parsing/transcription imports later.
- **Recovery / rollback expectations:** Blueprint versions should be immutable or recoverable. Failed runs should keep raw source references and allow regeneration.

## 12. Model and Cost Expectations

Only fill what you know. The Strategist should still make the final recommendation.

- **Cost sensitivity:** medium
- **Latency sensitivity:** medium
- **Expected request / task volume:** Low to medium. A pilot may process a few workflows per week, each with multiple extraction/synthesis calls.
- **If AI is used, should the system prefer smaller / cheaper models by default:** Yes for extraction and checks; stronger models for final blueprint synthesis and ambiguity resolution.
- **Any required capabilities:** Structured output, long-context synthesis, retrieval, function calling/tool use, source-grounded reasoning, and high-quality summarization.
- **Preview-model tolerance:** low for client-facing output; medium for internal draft generation.

## 13. Success Metrics

- **Business success metric:** Number of paid discovery briefs or automation audits completed, and percentage that convert into implementation projects.
- **Quality metric:** Human reviewer acceptance rate of required blueprint sections and number of critical missing questions caught before implementation.
- **Latency metric:** Time from raw workflow input to reviewable blueprint under 30 minutes for v1 workflows.
- **Cost metric:** LLM cost per completed workflow brief stays within a configured ceiling.
- **Operational metric:** Blueprint completeness score, evidence-link coverage, missing-question count, review edit rate, and implementation-ticket conversion rate.

---

## Usage

1. Send this completed brief to the Strategist.
2. Let the Strategist ask one batch of clarifying questions.
3. Use the resulting architecture package as the Phase 1 input to the rest of the playbook.
