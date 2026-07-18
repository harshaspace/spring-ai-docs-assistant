from src.llm.prompt import build_prompt


def test_build_prompt():
    documents = [
        {
            "filename": "api/advisors-recursive.adoc",
            "content": "Recursive advisors can call the remaining advisor chain multiple times.",
        },
        {
            "filename": "api/tools.adoc",
            "content": "ToolCallingAdvisor implements the tool calling loop.",
        },
    ]

    question = "How do recursive advisors work?"

    messages = build_prompt(question, documents)

    # Two messages: system + user
    assert len(messages) == 2

    assert messages[0]["role"] == "system"
    assert messages[1]["role"] == "user"

    user_prompt = messages[1]["content"]

    # User question is included
    assert question in user_prompt

    # Context from both documents is included
    assert "Recursive advisors can call the remaining advisor chain multiple times." in user_prompt
    assert "ToolCallingAdvisor implements the tool calling loop." in user_prompt

    # Source filenames are included
    assert "api/advisors-recursive.adoc" in user_prompt
    assert "api/tools.adoc" in user_prompt