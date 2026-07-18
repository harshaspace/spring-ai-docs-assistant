from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_client = OpenAI()

def chat(prompts: list) -> str:
    """
    Send the prompts to the LLM and return the generated answer.
    """

    response = _client.responses.create(
        model="gpt-5-mini",
        input=prompts,
    )

    return response.output_text