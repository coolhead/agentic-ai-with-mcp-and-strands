from __future__ import annotations

from strands import tool
from strands import Agent
from strands.models import BedrockModel


BEDROCK_MODEL_ID = "meta.llama3-8b-instruct-v1:0"
bedrock_model = BedrockModel(model_id=BEDROCK_MODEL_ID, temperature=0.3, streaming=False)

GENERAL_SYSTEM_PROMPT = """
You are a helpful general assistant.
Answer clearly and concisely.
Do NOT call any tools. Return only text.
""".strip()


@tool
def general_assistant(query: str) -> str:
    print("Routed to General Assistant")
    try:
        general_agent = Agent(model=bedrock_model, system_prompt=GENERAL_SYSTEM_PROMPT, callback_handler=None)
        resp = general_agent(query)
        return str(resp).strip()
    except Exception as e:
        return f"Error processing your general query: {str(e)}"
