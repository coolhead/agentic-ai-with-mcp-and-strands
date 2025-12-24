from __future__ import annotations

from strands import tool
from strands import Agent
from strands.models import BedrockModel


BEDROCK_MODEL_ID = "meta.llama3-8b-instruct-v1:0"
bedrock_model = BedrockModel(model_id=BEDROCK_MODEL_ID, temperature=0.3, streaming=False)

LANG_SYSTEM_PROMPT = """
You are a translation assistant.
Translate accurately. If the user asks for a specific target language, do it.
If formality matters, provide both informal and formal versions briefly.
Do NOT call any tools. Return only text.
""".strip()


@tool
def language_assistant(query: str) -> str:
    print("Routed to Language Assistant")
    try:
        language_agent = Agent(model=bedrock_model, system_prompt=LANG_SYSTEM_PROMPT, callback_handler=None)
        resp = language_agent(query)
        return str(resp).strip()
    except Exception as e:
        return f"Error processing your language query: {str(e)}"
