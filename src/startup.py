from ingest.create_index import create_index
from ingest.data_ingest import load_chunks, index_chunks


def main():
    create_index()
    chunks = load_chunks()
    index_chunks(chunks)


if __name__ == "__main__":
    main()