from sentence_transformers import SentenceTransformer

_MODEL = None


def get_model():
    global _MODEL

    if _MODEL is None:
        _MODEL = SentenceTransformer("BAAI/bge-small-en-v1.5")

    return _MODEL

def generate_embedding(text: str) -> list[float]:
    """Generate an embedding for a single piece of text."""

    model = get_model()

    embedding = model.encode(
        text,
        normalize_embeddings=True,
        show_progress_bar=False,
    )

    return embedding.tolist()

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    model = get_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    return embeddings.tolist()