from src.embedding.embedding import generate_embedding


def test_generate_embedding():
    embedding = generate_embedding("Spring AI")

    assert isinstance(embedding, list)
    assert len(embedding) == 384