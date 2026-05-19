"""Embedding provider abstraction for retrieval indexing."""

from __future__ import annotations

import hashlib
from typing import Protocol


class EmbeddingProvider(Protocol):
    model_name: str

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Embed text inputs into vector representations."""


class FakeEmbeddingProvider:
    def __init__(self, *, model_name: str = "fake-embedding", dimensions: int = 8) -> None:
        self.model_name = model_name
        self.dimensions = dimensions

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [self._embed_one(text) for text in texts]

    def _embed_one(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        return [digest[index] / 255 for index in range(self.dimensions)]
