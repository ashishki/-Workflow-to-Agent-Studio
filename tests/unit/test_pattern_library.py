from workflow_agent_studio.retrieval import load_pattern_library


def test_pattern_library_loads_markdown_templates() -> None:
    patterns = load_pattern_library("patterns")

    assert {pattern.source_id for pattern in patterns} == {
        "pattern-automation_blueprint",
        "pattern-eval_cases",
    }
    assert {pattern.corpus_type for pattern in patterns} == {"pattern"}
    assert {pattern.title for pattern in patterns} == {
        "Automation Blueprint Pattern",
        "Evaluation Case Pattern",
    }
