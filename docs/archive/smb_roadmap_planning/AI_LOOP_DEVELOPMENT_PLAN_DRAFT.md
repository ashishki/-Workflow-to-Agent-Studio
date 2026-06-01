# AI Loop Development Plan

Purpose: define how Codex, strategist, reviewer, and human roles should execute
the SMB roadmap layer without collapsing design, implementation, and review into
one unchecked loop.

## Operating Model

The loop uses role separation:

- Orchestrator: selects the next task, checks dependencies, and keeps scope
  narrow.
- Strategist: writes product/methodology docs, report examples, and review
  criteria.
- Codex implementer: changes code, schemas, tests, and deterministic exporters.
- Verification reviewer: reviews output for unsupported claims, privacy issues,
  missing tests, and over-automation.
- Human owner: approves product boundaries, pilot claims, privacy language, and
  cost assumptions.

The implementer should not approve its own output. The reviewer should not
silently rewrite implementation scope.

## Loop Per Task

1. Select one task from `docs/backlog/smb_mvp_taskgraph.md`.
2. Read only the listed context refs.
3. Confirm dependencies are complete.
4. Implement the smallest code/docs change that satisfies acceptance criteria.
5. Add or update tests named in acceptance criteria.
6. Run targeted tests.
7. Update eval docs when behavior changes.
8. Produce a short handoff:
   - files changed;
   - tests run;
   - residual risk;
   - reviewer focus.
9. Reviewer checks against acceptance criteria and forbidden claims.
10. Human owner approves only when product/pilot/privacy claims are involved.

## Gates

### Product Gate

Required before implementation:

- report contract accepted;
- MVP non-goals explicit;
- privacy modes documented;
- demo domains selected.

### Schema Gate

Required before generator work:

- `RoadmapReport`;
- `RecommendationCard`;
- `PrivacyClassification`;
- `CostEstimate`;
- `PriorityScore`;
- `VerificationReceipt`.

### Privacy Gate

Required before cloud/private/local recommendations:

- deterministic privacy classifier;
- redaction preview;
- restricted-data blocking tests;
- human review rule for high-risk domains.

### Report Gate

Required before demo export is called client-ready:

- roadmap quality eval passes;
- verification appendix exists;
- no forbidden claims;
- do-not-automate section exists.

### Commercial Gate

Required before public buyer proof claims:

- real pilot row in `docs/pilot_measurement.md`;
- named reviewer;
- time-to-roadmap metric;
- required-section acceptance rate;
- critical missing questions resolved.

## Cadence

Recommended 30-day implementation cadence:

- Week 1: product contract and roadmap schema docs.
- Week 2: core domain schemas and validators.
- Week 3: privacy classifier, pattern library, cost/scoring engines.
- Week 4: demo reports, evals, CLI command, verification receipt.

## Stop Conditions

Stop and ask for human decision when:

- product scope shifts toward production agent building;
- legal/compliance claims are requested;
- cost assumptions are being marketed as quotes;
- real sensitive customer data appears in fixtures;
- a task requires external credentials or customer access;
- an implementation would weaken local-first boundaries.
