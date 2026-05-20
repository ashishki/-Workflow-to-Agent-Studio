# Pilot Measurement

Status: template only
Date created: 2026-05-19

This artifact records the first adoption proof metric after a real operator pilot. Do
not mark the pilot as passed until the measurement row is filled after human review.

No real pilot has been reviewed yet. Until that evidence exists, this artifact
remains template-only and must not be cited as product validation.

Dataset boundary: demo fixtures, synthetic benchmarks, and unreviewed sanitized
artifacts must not be counted as real pilot rows. Only a human-reviewed real
workflow source can replace the template row below.

## Pilot Intake Checklist

All checklist rows must be complete before replacing the template pilot row with a
real measurement row.

| Requirement | Real Pilot Evidence | Demo/Synthetic Evidence |
|-------------|---------------------|-------------------------|
| workflow source | Real operator-provided SOP, transcript, notes, form, or integration excerpt. | Not accepted. Demo and synthetic fixtures can test mechanics only. |
| source duration | Record minutes of real source material or discovery input. | Not accepted for proof metrics. |
| reviewer action | Human reviewer inspects the generated blueprint and records accepted sections, edits, missing questions, and unsupported claims. | Not accepted unless the reviewer is evaluating a real workflow. |
| thresholds | Record time-to-reviewable blueprint and required-section acceptance after review. | Not accepted for commercial proof. |
| missing-question rule | Any unresolved critical missing question forces `Fail`. | Not accepted for pilot pass/fail. |
| sanitized notes | Summaries may be sanitized, but the reviewer must confirm they came from a real workflow. | Synthetic or demo summaries remain non-pilot data. |

Required source material:

- real workflow source lasting roughly 10-20 minutes or equivalent written detail
- source kind recorded as transcript, notes, form, integration excerpt, SOP, or mixed packet
- sanitization status recorded before any benchmark or public artifact reuse

Required reviewer actions:

- count accepted required blueprint sections
- count substantive reviewer edits
- count critical missing questions
- record unsupported claims, wrong boundaries, weak evals, wrong integrations, and unclear risks when present
- confirm whether every critical missing question is resolved

## Required Fields

| Field | Description | Value |
|-------|-------------|-------|
| workflow_source_duration_minutes | Duration of the raw workflow source material or discovery input. | TBD |
| time_to_reviewable_blueprint_minutes | Minutes from source import to reviewable draft blueprint. | TBD |
| required_section_acceptance_rate_percent | Percent of required blueprint sections accepted after human review without full rewrite. | TBD |
| reviewer_edit_count | Count of substantive reviewer edits before the blueprint is usable. | TBD |
| critical_missing_question_count | Count of critical missing questions found during human review. | TBD |

## Pass/Fail Thresholds

| Metric | Pass Threshold | Result |
|--------|----------------|--------|
| time_to_reviewable_blueprint_minutes | Pass if under 30 minutes. | TBD |
| required_section_acceptance_rate_percent | Pass if at least 80 percent after human review. | TBD |

Overall result is `Pass` only when both threshold rows pass after human review.
Any unresolved critical missing question forces `Fail` even if the timing and
section-acceptance thresholds pass.

## Reviewer Evidence

Record reviewer findings only after a real pilot review:

- reviewer_edit_count: TBD until substantive edits are counted
- critical_missing_question_count: TBD until missing questions are reviewed
- reviewer_edit_summary: TBD until edits are summarized without raw client text
- critical_missing_questions: TBD until questions are summarized without raw client text

## Pilot Rows

| Date | Workflow | Source Duration Min | Time To Reviewable Blueprint Min | Required Section Acceptance Rate % | Reviewer Edit Count | Critical Missing Question Count | Pass? | Notes |
|------|----------|---------------------|----------------------------------|------------------------------------|---------------------|---------------------------------|-------|-------|
| TBD | Template only - no reviewed pilot yet | TBD | TBD | TBD | TBD | TBD | TBD | Fill only after a real pilot and human review. |
