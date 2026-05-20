from workflow_agent_studio.patterns import (
    load_vertical_pack,
    load_vertical_packs,
    pack_metadata_for_generation,
)
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


def test_vertical_pack_contract_loads_deterministically() -> None:
    packs = load_vertical_packs("patterns")

    assert [pack.pack_id for pack in packs] == ["support_intake"]
    pack = packs[0]
    assert pack.schema_version == "vertical_pack:v1"
    assert pack.domain == "Support intake"
    assert pack.source_examples
    assert pack.extraction_hints
    assert "automation_candidates" in pack.required_blueprint_sections
    assert pack.risks
    assert pack.eval_fixtures


def test_vertical_pack_metadata_can_attach_to_generation_attempts() -> None:
    pack = load_vertical_pack("patterns/support_intake_pack.json")

    assert pack_metadata_for_generation(pack) == {
        "pack_id": "support_intake",
        "pack_schema_version": "vertical_pack:v1",
        "pack_domain": "Support intake",
    }
