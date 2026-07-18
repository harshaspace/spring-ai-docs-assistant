from unittest.mock import MagicMock

from src.retrieval.hybrid_search import hybrid_search


def test_search_calls_elasticsearch(monkeypatch):
    fake_es = MagicMock()

    fake_es.search.return_value = {
        "hits": {
            "hits": []
        }
    }

    monkeypatch.setattr(
        "src.retrieval.hybrid_search.Elasticsearch",
        lambda *_: fake_es,
    )

    hybrid_search("recursive advisor")

    assert fake_es.search.called