# Workflow Studio P0 CI and rename-preparation evidence

Date: 2026-07-13
Prepared from: `b21a70a8f3572da5b687d4002807d7d6546a59ba`
Working branch: `agent/workflow-p0-rename-prep`
Remote rename status: blocked; not attempted
Publication boundary: branch, draft-PR, and remote-CI state must be verified on
GitHub; this packet proves the local candidate only

## Scope and evidence boundary

This packet verifies the local P0 repair prepared before renaming
`ashishki/-Workflow-to-Agent-Studio` to
`ashishki/workflow-to-agent-studio`. It does not claim that remote CI is green,
that the repository has been renamed, or that a release is ready.

The exercised inputs are repository fixtures and saved public-source examples.
No external user, observed workflow-owner outcome, production deployment, buyer
validation, or commercial result is represented by these checks.

## Isolation and backup

The original worktree was not used for edits because it contains an unrelated
user change in `templates/SIMPLIFICATION_REPORT.md`. Its patch SHA-256 before
this work was
`5d720e60716c82ab89bc5f86dbab7008f23b7480b9df8924b49f5fa6c9e4c750`.
All prepared edits live in the separate clone at
`.portfolio-audit-worktrees/workflow-to-agent-studio`.

Before editing, the remote was cloned as a protected mirror and bundled:

- mirror: `secure-git-backups/2026-07-13/workflow-to-agent-studio/remote-mirror.git`;
- complete bundle:
  `secure-git-backups/2026-07-13/workflow-to-agent-studio/remote-all-refs.bundle`;
- bundle SHA-256:
  `ee1a4a393b125adad79e457a274c36ccb02e72b4a208a053cdf12c2aa5a2ea68`;
- directory mode: `0700`; bundle mode: `0600`;
- `git fsck --full --strict`: pass;
- `git bundle verify`: complete history, SHA-1 object format, pass.

The remote ref inventory contained only `main` and `HEAD`, both at
`b21a70a8f3572da5b687d4002807d7d6546a59ba`. The public API reported no tags,
releases, open pull requests, or open issues.

## Remote CI diagnosis

The GitHub Actions API reported 43 runs. The latest run was
[`28796113910`](https://github.com/ashishki/-Workflow-to-Agent-Studio/actions/runs/28796113910)
for the source commit above. It completed with `failure` on 2026-07-06 and
created zero jobs.

`actionlint 1.7.12` reproduced the parse failure at
`.github/workflows/ci.yml:32`: an inline YAML scalar contained the unescaped
`PHASE1_AUDIT: PASS` colon. Because the workflow never parsed, its test results
were never authoritative.

A second defect was found after repairing the parser. The trailing-whitespace
command included a missing `prompts` path. GNU `grep` returned an error code,
which `!` inverted to success even while tracked files contained trailing
spaces. The repaired check uses `git grep` across all tracked Markdown and YAML
files; the 12 files it exposed were cleaned mechanically.

## Prepared repair

- make the audit-status command a YAML block scalar;
- restrict the workflow token to `contents: read`;
- cancel superseded branch/PR runs;
- bound the test job to 20 minutes and disable persisted checkout credentials;
- pin `actions/checkout` to `v7.0.0` SHA
  `9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0`;
- pin `actions/setup-python` to `v6.3.0` SHA
  `ece7cb06caefa5fff74198d8649806c4678c61a1`;
- add pip caching and a PyYAML syntax regression test;
- repair and harden the tracked `ci/ci.yml` template, and add regression tests
  that require valid YAML and full-length action SHAs in both workflow files;
- replace stale README test counts with reproducible commands and explicit
  local/demo limitations;
- stop storing scanner-shaped credential literals in tests while preserving the
  runtime credential-redaction cases;
- add a seven-entry, immutable-fingerprint `.gitleaksignore` for the reviewed
  historical synthetic fixtures; it does not suppress new matches;
- make CI fetch full history and run the checksum-verified Gitleaks binary, with
  a regression test that forbids broad allowlist entries;
- update the active session state and demo wording so local fixtures are not
  presented as observed use;
- document that this public repository has no open-source license and grants no
  external reuse permission.

The Actions versions were checked against the official upstream tags and latest
release metadata on 2026-07-13.

## Local verification

Environment:

- Python `3.12.3`;
- Pydantic `2.13.4`;
- pytest `9.1.1`;
- Ruff `0.15.21`;
- PyYAML `6.0.3`;
- actionlint `1.7.12`, release archive SHA-256 verified before use.
- zizmor `1.26.1`;
- Bandit `1.9.4`;
- pip-audit `2.10.1`;
- Gitleaks `8.30.1`, Linux archive SHA-256
  `551f6fc83ea457d62a0d98237cbad105af8d557003051f41f3e7ca7b3f2470eb`
  verified against the official release checksum;
- markdown-link-check `3.14.2`.

Results:

| Check | Result |
|---|---|
| `actionlint .github/workflows/ci.yml ci/ci.yml` | Pass |
| `zizmor --pedantic .github/workflows/ci.yml ci/ci.yml` | Pass; no findings |
| required-document and Phase 1 audit checks | Pass |
| `bash -n hooks/*.sh` | Pass |
| tracked Markdown/YAML trailing-whitespace gate | Pass |
| `ruff check workflow_agent_studio tests/ scripts/` | Pass |
| `ruff format --check workflow_agent_studio tests/ scripts/` | Pass; 150 files |
| `python -m pytest tests/ -q --disable-warnings` | Pass; 372 tests in 40.50 s |
| installed CLI `--help` | Pass |
| `bash scripts/demo_roadmap_ru.sh` | Pass; synthetic salon and public-source HVAC draft paths |
| local Markdown links across 211 Markdown files | Pass; 0 missing targets |
| 41 unique external HTTP locators in active Markdown | 39 returned HTTP 200; 1 returned 404; 1 timed out |
| `bandit -r workflow_agent_studio scripts` | Pass; 10,297 lines, no findings |
| `pip-audit -r requirements.txt` and `-r requirements-dev.txt` | Pass; no known vulnerabilities in the resolved dependency sets |
| Gitleaks current candidate snapshot | Pass; 398 files / 1.99 MB, 0 findings |
| Gitleaks full Git history with reviewed fingerprint allowlist | Pass; 110 commits / 2.33 MB, 0 unaccounted findings |

The historical Mighty Air request-service locator returned HTTP 404; its
source-register row now records that the captured claim cannot currently be
rechecked from that URL. The OpenStack wiki locator timed out from this
environment after two attempts, so this run does not claim it is reachable or
broken. Neither result is presented as a successful browser link.

Gitleaks also scanned all 110 commits (approximately 2.33 MB). The raw scan
before applying the reviewed fingerprint allowlist reported seven
historical matches, all manually traced to explicit redaction/classification
test values: four underscore-form `sk` placeholder occurrences and three
hyphen-form `sk` placeholder occurrences.
Those are synthetic fixtures, not credentials. No history rewrite is proposed:
the current tests construct the same runtime values without scanner-shaped
source literals. `.gitleaksignore` records each accepted match using its exact
commit, path, rule, and line fingerprint, so new or moved matches remain visible.

## Rename-sensitive inventory

The repository contains no badges, submodules, `CITATION.cff`, GitHub repository
URL in package metadata, Docker image name, or published release/tag to migrate.
The Python distribution and CLI are named `workflow-agent-studio`; the evidence
receipt product ID is already `workflow-to-agent-studio`. Those runtime
identities should remain stable during the repository rename.

References requiring action at the rename boundary:

| Surface | Current reference | Required action |
|---|---|---|
| this repository | `docs/COGNITION_MANIFEST.md:6` | change `source_repo` after the remote rename succeeds |
| Telegram project registry | `telegram-research-agent/src/config/projects.yaml:107` | update repository slug in a separate clean worktree |
| Playbook cognition assessment | `AI_workflow_playbook/docs/cognition/current_project_assessment.md:24` | update the display slug in a separate clean worktree |
| cognition-vault registry | `engineering-cognition-vault/00-operating-model/project-registry.tsv:9` | update repository slug and local root after the local directory migration |
| cognition-vault project page | `engineering-cognition-vault/10-projects/workflow-to-agent-studio.md:4-21` | update `source_repo` and `repo://` references, then run the vault verifier |
| generated cognition index | `engineering-cognition-vault/_generated/indexes/workflow-to-agent-studio.index.json` | regenerate from the updated registry; do not hand-edit generated JSON |
| local clones | SSH origin with the leading-hyphen slug | set the new origin and fetch with prune after redirect verification |
| portfolio audit and execution ledger | historical/current audit references | keep historical rows; update only forward-looking execution state |
| protected backup mirror | old SSH origin in the mirror config | retain unchanged as evidence of the pre-rename remote |
| archived orchestrator documents | old absolute local path | retain as historical evidence; do not treat as active automation |

Remote metadata at audit time was public and unarchived, with default branch
`main`, no description, homepage, topics, or detected license. The public branch
API reports `main` as unprotected. Repository admin access is required to rename
it, add protection/rulesets, and verify Actions secrets, webhooks, deploy keys,
Pages, package references, environments, and other settings.

Proposed post-rename metadata (not applied):

- description: `Local-first workflow discovery that turns SOPs and interviews into evidence-linked AI automation blueprints with human approval and evaluation plans.`
- topics: `workflow-discovery`, `ai-automation`, `requirements-engineering`,
  `business-process`, `human-in-the-loop`, `llm-evaluation`,
  `developer-tooling`, `python`.

The repository identity patch must wait until the remote mutation succeeds:

```diff
-source_repo: -Workflow-to-Agent-Studio
+source_repo: workflow-to-agent-studio
```

The Python import (`workflow_agent_studio`), distribution and CLI
(`workflow-agent-studio`), evidence product ID (`workflow-to-agent-studio`), and
human-readable product name do not change at this boundary.

The unauthenticated public API returns HTTP 404 for
`ashishki/workflow-to-agent-studio`; this proves only that no public repository
is visible at that slug. An administrator must still rule out a private-name
collision before renaming.

## Exact remote rename checklist

1. Confirm the clean repair commit/PR is green on the old slug and back up all
   refs again immediately before the admin mutation.
2. Confirm there are no new branches, tags, releases, PRs, issues, packages, or
   environment settings beyond this inventory.
3. In GitHub repository settings, rename only
   `-Workflow-to-Agent-Studio` to `workflow-to-agent-studio`; do not rename the
   Python package or CLI.
4. Verify the new HTTPS and SSH endpoints with `git ls-remote`.
5. Verify the old HTTPS repository URL redirects to the exact new slug. Test an
   old blob URL and the latest old Actions URL as well as the repository root.
6. Update clone origins, `docs/COGNITION_MANIFEST.md`, the Telegram project
   registry, the Playbook assessment, and the cognition-vault registry/project
   page; regenerate the vault index. Re-run the workspace-wide exact-slug `rg`
   audit.
7. Recheck workflow runs, branch protection/rulesets, Actions permissions and
   secrets, environments, webhooks, deploy keys, Pages, packages, and any
   security integrations after the rename.
8. Add the audited description and topics through repository settings, then
   verify them with the repository API.
9. Run the complete CI suite from a fresh clone of the new SSH URL. Record the
   green run URL and commit SHA in this file or a successor evidence packet.
10. Do not publish `v0.1.0` until one consented real workflow owner reviews a
    sanitized before/after blueprint and the evidence limitations remain
    explicit.

Candidate clone migration commands after the API and redirect checks pass:

```bash
git remote set-url origin git@github.com:ashishki/workflow-to-agent-studio.git
git ls-remote --exit-code origin refs/heads/main
git fetch --prune origin
```

If the new endpoints, redirect, settings, or default branch are wrong, stop
before updating cross-repository references. Rename the repository back through
GitHub settings, restore the old origin URL, verify `main` against the protected
bundle, and record the failed migration. No history rewrite or force-push is
needed for this repository rename.

## Blockers

- GitHub CLI is unavailable in this environment; draft-PR publication uses the
  connected GitHub app after an SSH branch push.
- The connected GitHub surface does not expose repository rename/admin settings.
- The public API reports `main` as unprotected; protection/ruleset changes also
  require repository admin settings unavailable to this task.
- Remote CI is an external post-push result and is not represented as green by
  this local evidence packet.
- The observed workflow-owner case required for `v0.1.0` does not exist and must
  not be fabricated.
