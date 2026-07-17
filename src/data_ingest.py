"""Ingest Spring AI documentation content into Elasticsearch."""

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from gitsource import GithubRepositoryDataReader
from gitsource import chunk_documents

from embedding import generate_embeddings
from pyfiglet import figlet_format

from config import ELASTICSEARCH_URL, INDEX_NAME


def load_chunks():
    """Load documentation files from the Spring AI GitHub repository and split them into chunks."""
    # Create a reader for the target repository and only include AsciiDoc files under the pages directory.
    reader = GithubRepositoryDataReader(
        repo_owner="spring-projects",
        repo_name="spring-ai",
        commit_id="main",
        allowed_extensions={"adoc"},
        filename_filter=lambda path: "/pages/" in path,
    )

    # Read the matching files from the repository.
    files = reader.read()

    # Parse each file into a document object.
    documents = [file.parse() for file in files]

    # Split the parsed documents into smaller searchable chunks.
    return chunk_documents(
        documents,
        size=2000,
        step=1000,
    )


def index_chunks(chunks):
    """Send the prepared chunks to Elasticsearch for indexing."""
    
    # Generate embeddings in batches
    embeddings = generate_embeddings(
        [chunk["content"] for chunk in chunks]
    )

    # Connect to the configured Elasticsearch instance.
    es = Elasticsearch(ELASTICSEARCH_URL)

    # Build bulk indexing actions for each chunk.
    actions = []

    for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        actions.append(
            {
                "_index": INDEX_NAME,
                "_id": i,
                "_source": {
                    "content": chunk["content"],
                    "filename": chunk["filename"],
                    "start": chunk["start"],
                    "embedding": embedding,
                },
            }
        )

    success, errors = bulk(es, actions, raise_on_error=False)

    print(f"Successfully indexed: {success}")
    print(f"Errors: {len(errors)}")

    if errors:
        print(errors[0])
    else:
        print(figlet_format("STARTUP", font="slant"))
        print("🚀 Spring AI Docs Assistant is Ready!")

def main():
    """Run the ingestion pipeline from loading to indexing."""
    chunks = load_chunks()
    index_chunks(chunks)


if __name__ == "__main__":
    main()