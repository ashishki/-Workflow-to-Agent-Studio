"""End-to-end draft blueprint pipeline."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from workflow_agent_studio.blueprint import synthesize_blueprint
from workflow_agent_studio.blueprint.review import edit_blueprint
from workflow_agent_studio.domain.sources import SourceDocument
from workflow_agent_studio.extraction import extract_workflow_map
from workflow_agent_studio.ingestion import ingest_source_paths
from workflow_agent_studio.retrieval import (
    FakeEmbeddingProvider,
    SourceChunk,
    build_vector_index,
    chunk_source_document,
    retrieve_evidence,
)
from workflow_agent_studio.storage import (
    AuditEventRepository,
    BlueprintVersionRepository,
    SourceDocumentRepository,
    WorkflowRunRepository,
)
from workflow_agent_studio.validators import (
    BlueprintValidationFinding,
    validate_blueprint_for_approval,
)

DEFAULT_RETRIEVAL_QUERY = (
    "workflow triage review support request follow-up task engineering bug issue incident"
)


@dataclass(frozen=True)
class DraftPipelineResult:
    run_id: str
    exit_code: int
    source_count: int
    chunk_count: int
    index_namespace: str | None
    blueprint_version_id: int | None
    finding_ids: list[str] = field(default_factory=list)

    def to_json_dict(self) -> dict[str, object]:
        return {
            "run_id": self.run_id,
            "exit_code": self.exit_code,
            "source_count": self.source_count,
            "chunk_count": self.chunk_count,
            "index_namespace": self.index_namespace,
            "blueprint_version_id": self.blueprint_version_id,
            "finding_ids": self.finding_ids,
        }


def run_draft_pipeline(
    connection: sqlite3.Connection,
    *,
    run_id: str,
    source_paths: list[str | Path],
    index_dir: str | Path,
) -> DraftPipelineResult:
    run_repository = WorkflowRunRepository(connection)
    if run_repository.get_run(run_id) is None:
        run_repository.create_run(run_id)

    ingestion = ingest_source_paths(connection, run_id=run_id, paths=source_paths)
    sources = [
        SourceDocument(
            source_id=record.source_id,
            source_type=record.source_type,
            title=record.title,
            fingerprint=record.fingerprint,
            normalized_text=record.normalized_text,
        )
        for record in SourceDocumentRepository(connection).list_by_run(run_id)
    ]
    chunks = _chunk_sources(sources)
    index = build_vector_index(
        chunks=chunks,
        index_dir=index_dir,
        embedding_provider=FakeEmbeddingProvider(),
        corpus_version=f"{run_id}-e2e",
    )
    retrieval = retrieve_evidence(
        index_path=index.path,
        query=DEFAULT_RETRIEVAL_QUERY,
        embedding_provider=FakeEmbeddingProvider(),
    )
    if retrieval.status == "insufficient_evidence":
        finding = BlueprintValidationFinding(
            rule_id="RAG-INSUFFICIENT-EVIDENCE",
            severity="blocking",
            section="retrieval",
            message="No source evidence supports the draft blueprint.",
            repair_hint="Add workflow source material that describes support request handling.",
        )
        return DraftPipelineResult(
            run_id=run_id,
            exit_code=2,
            source_count=ingestion.source_count,
            chunk_count=len(chunks),
            index_namespace=index.namespace,
            blueprint_version_id=None,
            finding_ids=[finding.rule_id],
        )

    workflow = extract_workflow_map(source=sources[0], evidence=retrieval.evidence)
    blueprint = synthesize_blueprint(workflow=workflow, evidence=retrieval.evidence)
    validation = validate_blueprint_for_approval(blueprint)
    version = edit_blueprint(
        run_id=run_id,
        blueprint=blueprint,
        editor_label="pipeline",
        versions=BlueprintVersionRepository(connection),
        audit_events=AuditEventRepository(connection),
    )
    finding_ids = [finding.rule_id for finding in validation.findings]
    return DraftPipelineResult(
        run_id=run_id,
        exit_code=2 if validation.blocking_count else 0,
        source_count=ingestion.source_count,
        chunk_count=len(chunks),
        index_namespace=index.namespace,
        blueprint_version_id=version.blueprint_version_id,
        finding_ids=finding_ids,
    )


def _chunk_sources(sources: list[SourceDocument]) -> list[SourceChunk]:
    chunks: list[SourceChunk] = []
    for source in sources:
        chunks.extend(
            chunk_source_document(
                source_id=source.source_id,
                text=source.normalized_text,
            )
        )
    return chunks
