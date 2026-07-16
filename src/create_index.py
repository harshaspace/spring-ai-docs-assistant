from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_URL, INDEX_NAME


def create_index():
    es = Elasticsearch(ELASTICSEARCH_URL)

    if es.indices.exists(index=INDEX_NAME):
        print(f"Index '{INDEX_NAME}' already exists.")
        return

    es.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {
                "content": {"type": "text"},
                "filename": {"type": "keyword"},
                "start": {"type": "integer"},
            }
        },
    )

    print(f"Created index '{INDEX_NAME}'.")


if __name__ == "__main__":
    create_index()