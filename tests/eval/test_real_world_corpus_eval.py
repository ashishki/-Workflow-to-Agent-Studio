from pathlib import Path

from workflow_agent_studio.ingestion import normalize_text, normalize_transcript_text
from workflow_agent_studio.ingestion.readers import read_source_path
from workflow_agent_studio.retrieval import (
    build_evidence_anchor_map,
    build_evidence_gap_report,
    chunk_source_document,
)

CORPUS_FILES = [
    Path("tests/fixtures/sources/discovery_call.transcript.txt"),
    Path("tests/fixtures/sources/discovery_notes.notes.txt"),
    Path("tests/fixtures/sources/intake_form.form.md"),
    Path("tests/fixtures/sources/crm_integration.integration.txt"),
]


def _normalized_text(path: Path) -> tuple[str, str]:
    raw = read_source_path(path)
    if raw.source_type == "transcript":
        return raw.source_type, normalize_transcript_text(raw.text)
    return raw.source_type, normalize_text(raw.text)


def _corpus_chunks():
    chunks = []
    source_types = []
    for path in CORPUS_FILES:
        source_type, normalized = _normalized_text(path)
        source_types.append(source_type)
        chunks.extend(
            chunk_source_document(
                source_id=f"src-{path.stem}",
                text=normalized,
            )
        )
    return source_types, chunks


def test_real_world_corpus_contains_required_source_kinds() -> None:
    source_types, _chunks = _corpus_chunks()

    assert len(CORPUS_FILES) == 4
    assert set(source_types) == {"transcript", "notes", "form", "integration"}


def test_real_world_corpus_retrieval_baseline_metrics() -> None:
    _source_types, chunks = _corpus_chunks()
    anchors = build_evidence_anchor_map(chunks)
    supported_anchors = [
        anchor
        for anchor in anchors
        if anchor.source_id and anchor.chunk_id and anchor.normalized_snippet
    ]

    assert len(chunks) == 10
    assert len(supported_anchors) / len(chunks) == 1.0


def test_real_world_corpus_plan_baseline_metrics() -> None:
    _source_types, chunks = _corpus_chunks()
    report = build_evidence_gap_report(anchors=build_evidence_anchor_map(chunks))
    covered_sections = 6 - report.gap_count

    assert covered_sections / 6 == 4 / 6
    assert {gap.section for gap in report.gaps} == {"exceptions", "approval_boundaries"}


def test_real_world_corpus_eval_artifacts_are_recorded() -> None:
    retrieval_eval = Path("docs/retrieval_eval.md").read_text(encoding="utf-8")
    plan_eval = Path("docs/plan_eval.md").read_text(encoding="utf-8")

    assert "T24 established the real-world-style corpus fixture baseline" in retrieval_eval
    assert "Corpus count: 4" in retrieval_eval
    assert "Chunk count: 10" in retrieval_eval
    assert "Citation support: 1.00" in retrieval_eval
    assert "T24 established the real-world-style corpus planning baseline" in plan_eval
    assert "Required-section coverage: 0.67" in plan_eval
    assert "Evidence gaps: 2" in plan_eval


def test_readme_points_to_real_world_corpus_and_eval_commands() -> None:
    readme = Path("README.md").read_text(encoding="utf-8")

    assert "tests/fixtures/sources/discovery_call.transcript.txt" in readme
    assert "tests/fixtures/sources/discovery_notes.notes.txt" in readme
    assert "tests/fixtures/sources/intake_form.form.md" in readme
    assert "tests/fixtures/sources/crm_integration.integration.txt" in readme
    assert "tests/eval/test_real_world_corpus_eval.py" in readme
