"""LLM provider protocols and fakes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


@dataclass(frozen=True)
class ProviderResponse:
    payload: dict[str, Any]
    input_tokens: int | None = None
    output_tokens: int | None = None


class StructuredOutputProvider(Protocol):
    provider_name: str
    model_name: str

    def request_structured_output(self, *, prompt: str) -> ProviderResponse:
        """Return provider payload for a structured-output request."""


class FakeStructuredOutputProvider:
    provider_name = "fake"

    def __init__(
        self,
        *,
        payload: dict[str, Any],
        model_name: str = "fake-structured-model",
        input_tokens: int | None = None,
        output_tokens: int | None = None,
    ) -> None:
        self.payload = payload
        self.model_name = model_name
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens

    def request_structured_output(self, *, prompt: str) -> ProviderResponse:
        return ProviderResponse(
            payload=self.payload,
            input_tokens=self.input_tokens,
            output_tokens=self.output_tokens,
        )
