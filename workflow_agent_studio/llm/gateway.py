"""Provider-neutral structured-output LLM gateway."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from pydantic import BaseModel, ValidationError

from workflow_agent_studio.llm.errors import SchemaValidationError
from workflow_agent_studio.llm.providers import StructuredOutputProvider


@dataclass(frozen=True)
class LLMCallMetrics:
    provider: str
    model: str
    latency_ms: float
    input_tokens: int | None
    output_tokens: int | None


@dataclass(frozen=True)
class StructuredOutputResult[ModelT]:
    output: ModelT
    metrics: LLMCallMetrics


def request_structured_output[ModelT: BaseModel](
    *,
    provider: StructuredOutputProvider,
    prompt: str,
    output_model: type[ModelT],
) -> StructuredOutputResult[ModelT]:
    start = perf_counter()
    response = provider.request_structured_output(prompt=prompt)
    latency_ms = (perf_counter() - start) * 1000
    metrics = LLMCallMetrics(
        provider=provider.provider_name,
        model=provider.model_name,
        latency_ms=latency_ms,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
    )
    try:
        output = output_model.model_validate(response.payload)
    except ValidationError as error:
        raise SchemaValidationError(
            model_name=provider.model_name,
            validation_error_count=error.error_count(),
        ) from error
    return StructuredOutputResult(output=output, metrics=metrics)
