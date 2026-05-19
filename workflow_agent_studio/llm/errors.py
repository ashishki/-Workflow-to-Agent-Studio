"""Typed LLM gateway errors."""

from __future__ import annotations


class SchemaValidationError(Exception):
    def __init__(self, *, model_name: str, validation_error_count: int) -> None:
        self.model_name = model_name
        self.validation_error_count = validation_error_count
        super().__init__(
            f"Structured output from {model_name} failed schema validation "
            f"with {validation_error_count} error(s)."
        )
