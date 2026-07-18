from src.ingest.data_ingest import load_chunks


def test_load_chunks():
    chunks = load_chunks()

    assert len(chunks) > 0

    chunk = chunks[0]

    assert "content" in chunk
    assert "filename" in chunk
    assert "start" in chunk