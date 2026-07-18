from elasticsearch import Elasticsearch

from src.config import ELASTICSEARCH_URL, INDEX_NAME
from src.ingest.embedding import generate_embedding


def hybrid_search(query: str, k: int = 5):
    es = Elasticsearch(ELASTICSEARCH_URL)

    query_embedding = generate_embedding(query)

    # BM25 search
    bm25 = es.search(
        index=INDEX_NAME,
        query={
            "match": {
                "content": query
            }
        },
        size=20,
        source_excludes=["embedding"],
    )

    # Vector search
    knn = es.search(
        index=INDEX_NAME,
        knn={
            "field": "embedding",
            "query_vector": query_embedding,
            "k": 20,
            "num_candidates": 100,
        },
        source_excludes=["embedding"],
    )

    return reciprocal_rank_fusion(
        bm25["hits"]["hits"],
        knn["hits"]["hits"],
        k,
    )


def reciprocal_rank_fusion(*rankings, k=5, constant=60):
    scores = {}
    docs = {}

    for ranking in rankings:
        for rank, hit in enumerate(ranking):
            doc_id = hit["_id"]

            docs[doc_id] = hit

            scores.setdefault(doc_id, 0.0)
            scores[doc_id] += 1.0 / (constant + rank + 1)

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        docs[doc_id]["_source"]
        for doc_id, _ in ranked[:k]
    ]