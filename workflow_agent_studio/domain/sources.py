"""Source document schemas."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SourceDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    source_id: str = Field(min_length=1)
    source_type: Literal[
        "text", "markdown", "transcript", "notes", "form", "integration", "pattern"
    ]
    title: str = Field(min_length=1)
    fingerprint: str = Field(min_length=1)
    normalized_text: str = Field(min_length=1)
