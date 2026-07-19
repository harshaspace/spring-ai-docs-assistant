import time

from src.llm.client import chat
from src.llm.prompt import build_prompt
from src.retrieval.hybrid_search import hybrid_search
from src.monitoring.metrics import log_request


def ask(question: str) -> dict:
    start = time.perf_counter()

    # Retrieve documents
    retrieval_start = time.perf_counter()
    documents = hybrid_search(question)
    retrieval_ms = (time.perf_counter() - retrieval_start) * 1000

    prompts = build_prompt(question, documents)

    llm_start = time.perf_counter()
    answer = chat(prompts)
    llm_ms = (time.perf_counter() - llm_start) * 1000

    total_ms = (time.perf_counter() - start) * 1000

    # Persist metrics
    request_id = log_request(
        question=question,
        latency=total_ms,
        retrieval_latency=retrieval_ms,
        llm_latency=llm_ms
    )

    return {
        "answer": answer,
        "sources": [doc["filename"] for doc in documents],
        "request_id": request_id,
    }