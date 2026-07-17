from sentence_transformers import SentenceTransformer

_MODEL = None


def get_model():
    global _MODEL

    if _MODEL is None:
        _MODEL = SentenceTransformer("BAAI/bge-small-en-v1.5")

    return _MODEL


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    model = get_model()

    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        show_progress_bar=True,
    )

    return embeddings.tolist()