from workflow_agent_studio.retrieval import (
    FakeEmbeddingProvider,
    build_evidence_packs,
    build_vector_index,
    chunk_source_document,
)


def _index(tmp_path):
    chunks = chunk_source_document(
        source_id="src-corpus",
        text=(
            "# Support Intake\n\n"
            "The coordinator reviews each support request in the inbox and checks CRM "
            "account_status, customer_name, request_id, and issue_summary fields.\n\n"
            "When engineering review is needed, the coordinator drafts a follow-up task "
            "for the task tracker."
        ),
    )
    return build_vector_index(
        chunks=chunks,
        index_dir=tmp_path,
        embedding_provider=FakeEmbeddingProvider(),
        corpus_version="evidence-pack-fixture-v1",
    )


def test_evidence_packs_group_snippets_by_blueprint_section_and_candidate(tmp_path) -> None:
    index = _index(tmp_path)

    bundle = build_evidence_packs(
        index_path=index.path,
        sections=["current_workflow_steps", "data_fields"],
        candidate_automations=["draft_follow_up_task"],
        embedding_provider=FakeEmbeddingProvider(),
    )

    packs_by_section = {pack.section: pack for pack in bundle.packs}
    assert set(packs_by_section) == {
        "current_workflow_steps",
        "data_fields",
        "automation_candidates:draft_follow_up_task",
    }
    assert all(pack.status == "ok" for pack in bundle.packs)
    assert all(pack.evidence for pack in bundle.packs)
    assert bundle.citation_precision == 1.0


def test_unsupported_evidence_pack_section_returns_insufficient_evidence(tmp_path) -> None:
    index = _index(tmp_path)

    bundle = build_evidence_packs(
        index_path=index.path,
        sections=["budget_forecast"],
        embedding_provider=FakeEmbeddingProvider(),
    )

    assert len(bundle.packs) == 1
    assert bundle.packs[0].section == "budget_forecast"
    assert bundle.packs[0].status == "insufficient_evidence"
    assert bundle.packs[0].evidence == []
