# Cognition Manifest - Workflow-to-Agent Studio

---
artifact_kind: retrieval_manifest
project: workflow-to-agent-studio
source_repo: -Workflow-to-Agent-Studio
status: active
canonical: false
generated: false
tags: [workflow-discovery, rag, planning, cognition]
---

Version: 1.0
Last updated: 2026-05-25

## Purpose

Repo-local map for evidence-linked workflow extraction, blueprint synthesis, retrieval evals, plan evals, public-source experiments, and review continuity.

## Authority Rules

- Canonical repo artifacts win over this manifest.
- Generated notes and Obsidian graph views are convenience only.
- Blueprint quality decisions must cite source evidence, evals, or review artifacts.

## Project Identity

| Field | Value |
|-------|-------|
| Primary shape | Local deterministic workflow with retrieval-supported blueprint synthesis |
| Governance level | Standard |
| Runtime tier | T0/T1 local |
| Active profiles | RAG, Planning/eval, structured LLM extraction |

## Canonical Truth

| Surface | Path | Notes |
|---------|------|-------|
| Architecture | `docs/ARCHITECTURE.md` | System structure and boundaries |
| Contract | `docs/IMPLEMENTATION_CONTRACT.md` | Implementation rules |
| Task graph | `docs/tasks.md` | Execution contract |
| Session state | `docs/CODEX_PROMPT.md` | Current status |
| Decisions | `docs/DECISION_LOG.md` | Decision index |
| Journal | `docs/IMPLEMENTATION_JOURNAL.md` | Handoff continuity |
| Evidence | `docs/EVIDENCE_INDEX.md` | Proof lookup |
| Retrieval eval | `docs/retrieval_eval.md` | Retrieval quality |
| Plan eval | `docs/plan_eval.md`, `docs/evaluation_guide.md` | Blueprint/plan quality |
| Experiments | `docs/experiments/` | Public-source proof |
| Audits | `docs/audit/`, `docs/archive/` | Review history |

## Retrieval Scopes

| Scope | Start here | Include next |
|-------|------------|--------------|
| Blueprint quality | `docs/plan_eval.md` | source register, evidence packs, review workspace |
| Retrieval regression | `docs/retrieval_eval.md` | fixtures, evidence index, prior retrieval review |
| Public demo pack | `docs/experiments/public_demo_pack/` | boundary labels, review results, generated blueprint |
| Pattern reuse | `patterns/README.md`, `patterns/eval_cases.md` | plan eval, decision log |
| Reviewer packet | task ACs and contract | eval artifacts, evidence index, prior audit |

## Local/VPS Agent Context Workflow

Agents do not automatically discover the cognition vault. The operator or orchestrator must pass a repo-local manifest, vault project map, or generated context packet path into the agent task.

Expected sibling layout on any machine that runs agents:

```text
ai-stack/
|-- projects/<repo>/
`-- engineering-cognition-vault/
```

Local project work:

```bash
cd ai-stack/engineering-cognition-vault
./scripts/sync_from_projects.sh --no-pull --commit --push
```

VPS project work:

1. Commit and push code, docs, evals, ADRs, findings, or postmortems in this repo.
2. Refresh the vault on the machine that owns vault sync:

```bash
cd ai-stack/engineering-cognition-vault
git pull --ff-only
./scripts/sync_from_projects.sh --commit --push
```

If an agent runs on the VPS, clone the vault next to `projects/` and pass packet paths explicitly:

```text
../engineering-cognition-vault/10-projects/<project>.md
../engineering-cognition-vault/90-context-packets/<role>-<project>-<scope>.md
```

Do not write canonical decisions, eval results, or findings directly into the vault. Write them into this repo first, then regenerate the vault.

---

## Known Gaps

| Gap | Impact | Migration step |
|-----|--------|----------------|
| Experiment evidence is spread across demo-pack folders | Strategist/reviewer context can be expensive | Generate packets per public demo pack when reviewing |
| Cross-project reuse links are mostly narrative | Pattern graph is not explicit | Link reusable patterns to canonical eval/experiment artifacts |

## Generated Artifacts

| Artifact | Path | Policy |
|----------|------|--------|
| Cognition index | `generated/cognition/index.json` | Optional generated artifact |
| Context packets | `docs/context-packets/` | Commit only major review/regression packets |

