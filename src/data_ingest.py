from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from gitsource import GithubRepositoryDataReader
from gitsource import chunk_documents

from config import ELASTICSEARCH_URL, INDEX_NAME


def load_chunks():
    reader = GithubRepositoryDataReader(
        repo_owner="spring-projects",
        repo_name="spring-ai",
        commit_id="main",
        allowed_extensions={"adoc"},
        filename_filter=lambda path: "/pages/" in path,
    )

    files = reader.read()

    documents = [file.parse() for file in files]

    return chunk_documents(
        documents,
        size=2000,
        step=1000,
    )


def index_chunks(chunks):
    es = Elasticsearch(ELASTICSEARCH_URL)

    actions = [
        {
            "_index": INDEX_NAME,
            "_id": i,
            "_source": {
                "content": chunk["content"],
                "filename": chunk["filename"],
                "start": chunk["start"],
            },
        }
        for i, chunk in enumerate(chunks)
    ]

    bulk(es, actions)

    print(f"Indexed {len(actions)} chunks.")


def main():
    chunks = load_chunks()
    index_chunks(chunks)


if __name__ == "__main__":
    main()