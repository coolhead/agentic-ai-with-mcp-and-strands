from __future__ import annotations

from strands import tool
from strands import Agent
from strands.models import BedrockModel


BEDROCK_MODEL_ID = "meta.llama3-8b-instruct-v1:0"
bedrock_model = BedrockModel(model_id=BEDROCK_MODEL_ID, temperature=0.3, streaming=False)

ENGLISH_SYSTEM_PROMPT = """
You are an English assistant.
Fix grammar, improve clarity, and keep the original meaning.
When asked to fix grammar, return:
1) Corrected sentence
2) One-line explanation (short)
Do NOT call any tools. Return only text.
""".strip()


@tool
def english_assistant(query: str) -> str:
    print("Routed to English Assistant")
    try:
        english_agent = Agent(model=bedrock_model, system_prompt=ENGLISH_SYSTEM_PROMPT, callback_handler=None)
        resp = english_agent(query)
        return str(resp).strip()
    except Exception as e:
        return f"Error processing your English language query: {str(e)}"
