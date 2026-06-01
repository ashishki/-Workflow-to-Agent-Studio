# Privacy Classifier Prompt Contract

Purpose: provide context notes for deterministic privacy classification. The
final privacy class and gates are deterministic.

## Inputs

- source snippets after secret scan;
- workflow domain;
- data field inventory;
- selected privacy mode.

## Output Schema

- possible_sensitive_contexts;
- regulated_domain_hints;
- fields_needing_review;
- redaction_quality_notes;
- missing_privacy_questions;
- evidence_refs.

## Instructions

- Do not make final policy decisions.
- Do not weaken deterministic classification.
- Flag legal, medical, financial, HR, identity, and child/student hints.
- Suggest questions when context is unclear.
- Do not request raw restricted data.

## Failure Conditions

- claims data is safe because it is common;
- recommends cloud mode directly;
- ignores restricted-domain context.
