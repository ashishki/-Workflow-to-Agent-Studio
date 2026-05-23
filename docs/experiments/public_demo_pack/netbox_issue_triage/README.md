# NetBox Issue Triage Public Demo Pack

Status: public-source demo material; not customer proof.

Source fixture:
`tests/fixtures/public_sources/netbox_issue_triage.notes.md`

Source URL:
https://github.com/netbox-community/netbox/wiki/Issue-Triage-Workflow

This pack demonstrates the local Workflow-to-Agent Studio flow on a public
workflow source. It is suitable for product demo review and regression checks,
but it does not satisfy real-pilot evidence gates, T34, T40, or commercial proof
claims.

## Contents

- `command_transcript.md`: reproducible commands and observed CLI outputs.
- `source_register.md`: source-register row for the public source fixture.
- `generated_blueprint.md`: draft blueprint exported from the committed source fixture.
- `review_workspace.md`: local review workspace exported for the generated blueprint.
- `gap_summary.md`: remaining gaps and public-source boundary notes.
- `boundary_label.md`: public-demo-only label for the pack.

## Reproduction

Run the commands in `command_transcript.md` from the repository root. Temporary
database and index files are written under `.data/public_demo_pack/`, which is
ignored by git. The committed Markdown outputs can be regenerated from the
fixture with the same run ID and output paths.
