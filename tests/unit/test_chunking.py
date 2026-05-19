from workflow_agent_studio.retrieval import chunk_source_document


def test_chunks_preserve_source_metadata() -> None:
    text = "# Intake\n\nFirst paragraph.\n\n## Decisions\n\nSecond paragraph."

    chunks = chunk_source_document(source_id="src-1", text=text)

    assert [chunk.source_id for chunk in chunks] == ["src-1", "src-1"]
    assert chunks[0].chunk_id == "src-1:chunk-1"
    assert chunks[0].heading_path == ("Intake",)
    assert chunks[0].text == "First paragraph."
    assert text[chunks[0].start_char : chunks[0].end_char] == "First paragraph."
    assert chunks[1].heading_path == ("Intake", "Decisions")
    assert chunks[1].text == "Second paragraph."
    assert text[chunks[1].start_char : chunks[1].end_char] == "Second paragraph."
