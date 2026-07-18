from src.llm.client import chat
from src.llm.prompt import build_prompt
from src.retrieval.hybrid_search import hybrid_search


def ask(question: str) -> dict:
    documents = hybrid_search(question)

    prompts = build_prompt(question, documents)

    answer = chat(prompts)

    return {
        "answer": answer,
        "sources": [doc["filename"] for doc in documents],
    }