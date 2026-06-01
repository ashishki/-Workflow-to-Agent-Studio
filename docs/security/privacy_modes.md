# Privacy Modes

Privacy is a primary product feature, not an appendix.

The product should help customers understand that workflow planning can often be
done from process metadata, field names, rules, synthetic examples, and redacted
snippets without uploading raw private records.

## Safe Workflow Description

Allowed inputs:

- workflow steps;
- roles;
- system names;
- field names;
- SOPs;
- email templates without real names;
- synthetic examples;
- aggregate volumes;
- anonymized transcripts;
- screenshots only after redaction.

Disallowed inputs for default mode:

- production database exports;
- passwords;
- API keys;
- private customer records;
- full medical/legal/financial documents;
- payment card data;
- employee personal files;
- unredacted passports or IDs.

## Mode 1: Lightweight Cloud

Best for:

- hair salon;
- small e-commerce without regulated workflows;
- marketing agency;
- repair service;
- restaurant.

Architecture:

- local or hosted app;
- deterministic redaction before LLM;
- cloud LLM API;
- local or managed database;
- short retention;
- no raw secrets;
- Markdown/JSON report export.

Use when:

- data is low or moderate sensitivity;
- synthetic/redacted examples are enough;
- fast planning matters more than local model control.

Do not use when:

- raw medical, legal, financial, identity, or HR records are required;
- customer cannot approve cloud transfer;
- redaction cannot preserve enough context.

## Mode 2: Private Analysis

Best for:

- accounting firms;
- legal consultancies;
- dental clinics;
- internal teams with sensitive operational data.

Architecture:

- redaction pipeline;
- encryption at rest;
- audit logs;
- project/tenant isolation;
- cloud LLM only after redaction or through a private/enterprise API path;
- retention controls.

Use when:

- data is moderately or highly sensitive;
- cloud model may be acceptable after redaction;
- audit trail matters.

Risk:

- incomplete redaction;
- false sense of compliance;
- reduced context after redaction.

## Mode 3: Local / On-Prem / Sovereign

Best for:

- medical;
- legal;
- finance;
- government-like environments;
- companies that cannot send evidence to external LLM APIs.

Architecture:

- local LLM through vLLM, Ollama, or llama.cpp;
- local embeddings;
- local vector database such as Qdrant, SQLite, or LanceDB;
- encrypted local storage;
- no external model calls;
- local audit logs;
- optional air-gapped export.

Use when:

- data is restricted;
- external model calls are disallowed;
- customer accepts higher infrastructure and quality tradeoffs.

Risk:

- lower model quality on smaller local models;
- hardware and DevOps burden;
- security misconfiguration;
- model update burden.

## Policy Gates

- Restricted data defaults to local/on-prem or private analysis.
- Cloud mode is allowed only when raw sensitive payload is absent or redacted.
- Legal, medical, financial, HR, and identity workflows require human review.
- Disclaimers are not sufficient controls.
- Raw secrets must block export until removed or redacted.
