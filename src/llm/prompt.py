def build_prompt(question: str, documents: list[dict]) -> list[dict]:
    """
    Build chat messages for the LLM.

    Returns a list of messages compatible with most chat APIs.
    """

    context = "\n\n---\n\n".join(
        f"Source: {doc['filename']}\n\n{doc['content']}"
        for doc in documents
    )

    system_prompt = """You are an expert assistant for the Spring AI documentation.

Answer questions using ONLY the provided documentation.

Rules:
- If the answer is in the documentation, answer clearly and concisely.
- If the documentation does not contain the answer, say:
  "I couldn't find that information in the Spring AI documentation."
- Do not invent or assume information.
- When appropriate, mention which document the information came from.
"""

    user_prompt = f"""Documentation:

{context}

Question:
{question}
"""

    return [
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        },
    ]