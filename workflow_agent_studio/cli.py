"""Command line interface for Workflow-to-Agent Studio."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from workflow_agent_studio import __version__
from workflow_agent_studio.blueprint.review import edit_blueprint
from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.export import (
    export_draft_blueprint,
    export_draft_roadmap_report,
    resolve_export_path,
)
from workflow_agent_studio.health import get_health_status
from workflow_agent_studio.ingestion import UnsupportedSourceType, ingest_source_paths
from workflow_agent_studio.pipeline import run_draft_pipeline
from workflow_agent_studio.roadmap.service import generate_roadmap_report
from workflow_agent_studio.storage import (
    AuditEventRepository,
    BlueprintVersionRepository,
    WorkflowRunRepository,
    connect_database,
    initialize_database,
)
from workflow_agent_studio.validators import validate_blueprint_for_approval
from workflow_agent_studio.validators.privacy import validate_model_mode_recommendation

COMMAND_NAME = "workflow-agent-studio"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog=COMMAND_NAME)
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("health", help="Print application health status.")
    ingest_parser = subparsers.add_parser("ingest", help="Ingest local source files.")
    ingest_parser.add_argument("--database", required=True, help="SQLite database path.")
    ingest_parser.add_argument("--run-id", required=True, help="Workflow run ID.")
    ingest_parser.add_argument("paths", nargs="+", help="Source files to ingest.")
    run_parser = subparsers.add_parser("run", help="Generate a draft blueprint.")
    run_parser.add_argument("--database", required=True, help="SQLite database path.")
    run_parser.add_argument("--run-id", required=True, help="Workflow run ID.")
    run_parser.add_argument("--index-dir", required=True, help="Local retrieval index directory.")
    run_parser.add_argument("paths", nargs="+", help="Source files to process.")
    export_parser = subparsers.add_parser("export", help="Export a draft blueprint.")
    export_parser.add_argument("--database", required=True, help="SQLite database path.")
    export_parser.add_argument("--blueprint-version-id", required=True, type=int)
    export_parser.add_argument("--export-dir", required=True, help="Selected export directory.")
    export_parser.add_argument("--output", required=True, help="Output Markdown path.")
    review_parser = subparsers.add_parser("review", help="Export a local review workspace.")
    review_parser.add_argument("--database", required=True, help="SQLite database path.")
    review_parser.add_argument("--run-id", required=True, help="Workflow run ID.")
    review_parser.add_argument("--blueprint-version-id", required=True, type=int)
    review_parser.add_argument("--export-dir", required=True, help="Selected export directory.")
    review_parser.add_argument("--output", required=True, help="Output Markdown path.")
    review_parser.add_argument("--set-rough-effort-band")
    roadmap_parser = subparsers.add_parser("roadmap", help="Generate a draft SMB roadmap.")
    roadmap_parser.add_argument("--database", required=True, help="SQLite database path.")
    roadmap_parser.add_argument("--run-id", required=True, help="Workflow run ID.")
    roadmap_parser.add_argument(
        "--business-profile",
        required=True,
        help="Business profile or demo input Markdown path.",
    )
    roadmap_parser.add_argument(
        "--privacy-mode",
        required=True,
        choices=["lightweight_cloud", "private_analysis", "local_on_prem"],
        help="Requested analysis privacy mode.",
    )
    roadmap_parser.add_argument("--export-dir", required=True, help="Selected export directory.")
    roadmap_parser.add_argument("--output", required=True, help="Output Markdown path.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "health":
        print(json.dumps(get_health_status(), sort_keys=True))
    if args.command == "ingest":
        connection = connect_database(Path(args.database))
        try:
            initialize_database(connection)
            run_repository = WorkflowRunRepository(connection)
            if run_repository.get_run(args.run_id) is None:
                run_repository.create_run(args.run_id)
            try:
                result = ingest_source_paths(connection, run_id=args.run_id, paths=args.paths)
            except UnsupportedSourceType as exc:
                print(json.dumps({"error": str(exc)}, sort_keys=True), file=sys.stderr)
                return 2
            print(json.dumps(result.__dict__, sort_keys=True))
        finally:
            connection.close()
    if args.command == "run":
        connection = connect_database(Path(args.database))
        try:
            initialize_database(connection)
            try:
                result = run_draft_pipeline(
                    connection,
                    run_id=args.run_id,
                    source_paths=args.paths,
                    index_dir=Path(args.index_dir),
                )
            except UnsupportedSourceType as exc:
                print(json.dumps({"error": str(exc)}, sort_keys=True), file=sys.stderr)
                return 2
            print(json.dumps(result.to_json_dict(), sort_keys=True))
            return result.exit_code
        finally:
            connection.close()
    if args.command == "export":
        connection = connect_database(Path(args.database))
        try:
            initialize_database(connection)
            version = BlueprintVersionRepository(connection).get_version(args.blueprint_version_id)
            blueprint = AutomationBlueprint.model_validate_json(version.blueprint_json)
            validation = validate_blueprint_for_approval(blueprint)
            output = export_draft_blueprint(
                blueprint=blueprint,
                findings=validation.findings,
                export_dir=Path(args.export_dir),
                output_path=Path(args.output),
                version=version,
            )
            print(json.dumps({"path": str(output), "status": "draft"}, sort_keys=True))
        finally:
            connection.close()
    if args.command == "review":
        connection = connect_database(Path(args.database))
        try:
            initialize_database(connection)
            versions = BlueprintVersionRepository(connection)
            version = versions.get_version(args.blueprint_version_id)
            blueprint = AutomationBlueprint.model_validate_json(version.blueprint_json)
            if args.set_rough_effort_band:
                blueprint = blueprint.model_copy(
                    update={"rough_effort_band": args.set_rough_effort_band}
                )
                version = edit_blueprint(
                    run_id=args.run_id,
                    blueprint=blueprint,
                    editor_label="review-cli",
                    versions=versions,
                    audit_events=AuditEventRepository(connection),
                )
            validation = validate_blueprint_for_approval(blueprint)
            output = _export_review_workspace(
                blueprint=blueprint,
                version=version,
                findings=validation.findings,
                audit_events=AuditEventRepository(connection).list_events(args.run_id),
                versions=versions.list_versions(args.run_id),
                export_dir=Path(args.export_dir),
                output_path=Path(args.output),
            )
            print(
                json.dumps(
                    {
                        "blueprint_version_id": version.blueprint_version_id,
                        "finding_ids": [finding.rule_id for finding in validation.findings],
                        "path": str(output),
                    },
                    sort_keys=True,
                )
            )
        finally:
            connection.close()
    if args.command == "roadmap":
        connection = connect_database(Path(args.database))
        try:
            initialize_database(connection)
            run_repository = WorkflowRunRepository(connection)
            if run_repository.get_run(args.run_id) is None:
                run_repository.create_run(args.run_id)
            report = generate_roadmap_report(Path(args.business_profile))
            privacy_result = _validate_roadmap_privacy_mode(
                report=report,
                business_profile=Path(args.business_profile),
                privacy_mode=args.privacy_mode,
            )
            if not privacy_result.can_recommend:
                print(
                    json.dumps(
                        {
                            "error": "privacy mode blocked",
                            "finding_ids": [finding.rule_id for finding in privacy_result.findings],
                        },
                        sort_keys=True,
                    ),
                    file=sys.stderr,
                )
                return 2
            output = export_draft_roadmap_report(
                report=report,
                export_dir=Path(args.export_dir),
                output_path=Path(args.output),
            )
            print(
                json.dumps(
                    {
                        "path": str(output),
                        "privacy_mode": args.privacy_mode,
                        "report_id": report.report_id,
                        "run_id": args.run_id,
                        "status": "draft",
                    },
                    sort_keys=True,
                )
            )
        finally:
            connection.close()
    return 0


def _validate_roadmap_privacy_mode(*, report, business_profile: Path, privacy_mode: str):
    source = report.evidence_packet.source_documents[0]
    redaction_status = source.redaction_status
    if (
        source.source_privacy_class == "sensitive"
        and "redact" in report.executive_summary.overall_privacy_mode_recommendation.lower()
    ):
        redaction_status = "required"
    return validate_model_mode_recommendation(
        privacy_class=source.source_privacy_class,
        redaction_status=redaction_status,
        recommended_mode=privacy_mode,
        domain=business_profile.stem.replace("_input", ""),
        source_is_synthetic_or_redacted=source.source_type.startswith("synthetic"),
        report_condition=report.executive_summary.overall_privacy_mode_recommendation,
        human_review_gate=any(card.human_gate.required for card in report.recommendations),
    )


def _export_review_workspace(
    *,
    blueprint: AutomationBlueprint,
    version,
    findings,
    audit_events,
    versions,
    export_dir: Path,
    output_path: Path,
) -> Path:
    target = resolve_export_path(export_dir=export_dir, output_path=output_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    version_lines = [
        f"- v{item.version_number}: blueprint_version_id={item.blueprint_version_id}"
        for item in versions
    ]
    finding_lines = [
        f"- {finding.severity} {finding.rule_id} [{finding.section}]: {finding.message}"
        for finding in findings
    ] or ["- none"]
    evidence_lines = [
        f"- {reference.source_id} / {reference.chunk_id}"
        for reference in _review_evidence(blueprint)
    ] or ["- none"]
    comment_lines = [
        f"- {event['created_at']}: {event['payload_json']}"
        for event in audit_events
        if event["event_type"] == "review_comment_added"
    ] or ["- none"]
    lines = [
        "# Review Workspace",
        "",
        f"Blueprint Version ID: {version.blueprint_version_id}",
        "",
        "## Version History",
        *version_lines,
        "",
        "## Findings",
        *finding_lines,
        "",
        "## Evidence",
        *evidence_lines,
        "",
        "## Comments",
        *comment_lines,
        "",
    ]
    target.write_text("\n".join(lines), encoding="utf-8")
    return target


def _review_evidence(blueprint: AutomationBlueprint):
    references = []
    references.extend(blueprint.workflow_summary.evidence_references)
    for step in blueprint.current_workflow_steps:
        references.extend(step.evidence_references)
    for candidate in blueprint.automation_candidates:
        references.extend(candidate.evidence_references)
    for case in blueprint.eval_cases:
        references.append(case.evidence_reference)
    deduped = {(reference.source_id, reference.chunk_id): reference for reference in references}
    return list(deduped.values())


if __name__ == "__main__":
    raise SystemExit(main())
