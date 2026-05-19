import pytest
from pydantic import BaseModel

from workflow_agent_studio.llm import (
    FakeStructuredOutputProvider,
    SchemaValidationError,
    request_structured_output,
)


class ExampleOutput(BaseModel):
    summary: str


def test_fake_provider_returns_valid_structured_output() -> None:
    provider = FakeStructuredOutputProvider(payload={"summary": "ok"})

    result = request_structured_output(
        provider=provider,
        prompt="source text",
        output_model=ExampleOutput,
    )

    assert result.output == ExampleOutput(summary="ok")
    assert result.metrics.provider == "fake"
    assert result.metrics.model == "fake-structured-model"


def test_malformed_response_returns_schema_validation_error() -> None:
    provider = FakeStructuredOutputProvider(payload={"summary": 123}, model_name="bad-model")

    with pytest.raises(SchemaValidationError) as error:
        request_structured_output(
            provider=provider,
            prompt="source text",
            output_model=ExampleOutput,
        )

    assert error.value.model_name == "bad-model"
    assert error.value.validation_error_count == 1


def test_llm_metrics_exclude_prompt_text() -> None:
    provider = FakeStructuredOutputProvider(
        payload={"summary": "ok"},
        input_tokens=10,
        output_tokens=4,
    )

    result = request_structured_output(
        provider=provider,
        prompt="raw confidential workflow source",
        output_model=ExampleOutput,
    )

    assert result.metrics.input_tokens == 10
    assert result.metrics.output_tokens == 4
    assert "raw confidential workflow source" not in repr(result.metrics)
