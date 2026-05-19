# Workflow-to-Agent Studio Orchestrator

Version: 3.0

Use this as the short Codex entrypoint. Do not paste large roadmap or archive content into the prompt. Read only the active task and scoped references needed for the next step.

## Inputs

Read in this order:

1. `docs/CODEX_PROMPT.md` for current state and next task digest.
2. `docs/IMPLEMENTATION_CONTRACT.md` for mandatory rules and stop conditions.
3. The active task entry in `docs/tasks.md`.
4. Only the task's `Context-Refs` and directly affected code/tests/docs.

Archived files under `docs/archive/` are history. Read them only when a task explicitly references them or when investigating a regression.

## Loop

1. Confirm the next task maps to the current phase goal in `docs/tasks.md`.
2. Capture the pre-change baseline with pytest and ruff when the project is configured.
3. Implement within the task file scope.
4. Add or update tests for every acceptance criterion.
5. Update required eval artifacts for tagged tasks:
   - `rag:ingestion` or `rag:query` -> `docs/retrieval_eval.md`
   - `plan:schema` or `plan:validation` -> `docs/plan_eval.md`
6. Run focused tests, full pytest, `ruff check`, and `ruff format --check`.
7. Update `docs/CODEX_PROMPT.md` with baseline, next task, open findings, and profile state.
8. Commit one logical change. Do not add a co-author trailer unless the user asks.
9. Continue to the next eligible task unless a contract stop condition applies.

## Review Rules

Run a light review after each implementation task. Focus on:

- acceptance criteria coverage
- evidence and assumption rules
- source confidentiality
- deterministic validation ownership
- retrieval `insufficient_evidence` behavior
- local export and approval boundaries

Run a deep review at phase boundaries or when the implementation contract requires it. Archive the review under `docs/archive/` and update `docs/audit/AUDIT_INDEX.md`.

## Output Contract

When a task completes, report:

```text
IMPLEMENTATION_RESULT: DONE
Task: T##
Baseline: N passing, 0 skipped, 0 failed
Checks: pytest, ruff check, ruff format --check
Commit: <sha> <message>
Next: T## or phase boundary review
```

When blocked, report:

```text
IMPLEMENTATION_RESULT: BLOCKED
Task: T##
Blocker: <specific stop condition>
Needed: <human decision or missing artifact>
```
