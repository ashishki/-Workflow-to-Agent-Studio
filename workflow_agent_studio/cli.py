"""Command line interface for Workflow-to-Agent Studio."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from workflow_agent_studio import __version__
from workflow_agent_studio.domain.blueprint import AutomationBlueprint
from workflow_agent_studio.export import export_draft_blueprint
from workflow_agent_studio.health import get_health_status
from workflow_agent_studio.ingestion import ingest_source_paths
from workflow_agent_studio.pipeline import run_draft_pipeline
from workflow_agent_studio.storage import (
    BlueprintVersionRepository,
    WorkflowRunRepository,
    connect_database,
    initialize_database,
)
from workflow_agent_studio.validators import validate_blueprint_for_approval

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
            result = ingest_source_paths(connection, run_id=args.run_id, paths=args.paths)
            print(json.dumps(result.__dict__, sort_keys=True))
        finally:
            connection.close()
    if args.command == "run":
        connection = connect_database(Path(args.database))
        try:
            initialize_database(connection)
            result = run_draft_pipeline(
                connection,
                run_id=args.run_id,
                source_paths=args.paths,
                index_dir=Path(args.index_dir),
            )
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
