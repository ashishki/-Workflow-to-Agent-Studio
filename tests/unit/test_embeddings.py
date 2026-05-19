from workflow_agent_studio.retrieval import FakeEmbeddingProvider


def test_fake_embedding_provider_is_deterministic() -> None:
    provider = FakeEmbeddingProvider(dimensions=4)

    first = provider.embed_texts(["same text"])[0]
    second = provider.embed_texts(["same text"])[0]

    assert first == second
    assert len(first) == 4
