# Pattern Matching Eval

Purpose: verify that opportunities match useful implementation patterns without
forcing every workflow into an AI agent pattern.

## Required Fixtures

- hair salon booking workflow;
- e-commerce support workflow;
- legal consultancy checklist workflow;
- deterministic reminder workflow;
- no-AI-needed reporting workflow;
- high-risk legal decision blocker;
- low-volume workflow where automation is not justified.

## Expected Matches

| Fixture | Expected Pattern | Anti-Match |
|---------|------------------|------------|
| salon reminders | appointment reminder automation | high-autonomy agent |
| salon booking FAQ | booking assistant | autonomous stylist advice |
| e-commerce order status | API lookup | LLM-only answer |
| e-commerce returns | human-in-the-loop returns assistant | automatic refund |
| legal checklist | private checklist assistant | legal advice agent |
| legal status questions | restricted RAG/status assistant | unrestricted cloud bot |

## Automated Checks

- every match includes pattern ID and version;
- every match includes when-not-to-use notes;
- pattern privacy default is not weaker than detected data class;
- deterministic patterns are preferred when LLM is unnecessary;
- high-risk anti-matches are blocked.

## Eval History

| Date | Task | Matcher Version | Metric | Score | Baseline | Delta | Regression? | Eval Source |
|------|------|-----------------|--------|-------|----------|-------|-------------|-------------|
| 2026-06-01 | T75 | pattern-matching-baseline-v1 | Expected SMB pattern matches | 100%; salon reminder, e-commerce returns, legal checklist, reporting automation, privacy anti-match | 100%; salon reminder, e-commerce returns, legal checklist, reporting automation, privacy anti-match | 0% | No | pytest tests/eval/test_pattern_matching_eval.py -q |
| 2026-06-01 | T81 | roadmap-eval-suite-v1 | Roadmap pattern trace pass rate | 100%; 3 demo reports trace expected pattern IDs and versions | 100%; 3 demo reports trace expected pattern IDs and versions | 0% | No | pytest tests/eval/test_pattern_matching_eval.py -q |

## Human Review

Reviewers should confirm:

- the pattern is specific to the pain point;
- the architecture fits the workflow;
- the "when not to use" notes are visible;
- alternatives are considered.
