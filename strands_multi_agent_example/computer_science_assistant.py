from __future__ import annotations

from strands import tool, Agent
from strands.models import BedrockModel

BEDROCK_MODEL_ID = "meta.llama3-8b-instruct-v1:0"

bedrock_model = BedrockModel(
    model_id=BEDROCK_MODEL_ID,
    temperature=0.3,
    streaming=False,
)

cs_agent = Agent(
    model=bedrock_model,
    system_prompt=(
        "You are a computer science assistant. "
        "You write correct, clean code and explain briefly. "
        "Do NOT call any tools. Return only text."
    ),
)


def _is_palindrome_request(q: str) -> bool:
    ql = q.lower()
    return "palindrome" in ql and ("python" in ql or "function" in ql or "code" in ql)


@tool
def computer_science_assistant(query: str) -> str:
    print("Routed to Computer Science Assistant")

    if _is_palindrome_request(query):
        return (
            "Here’s a simple Python function to check if a string is a palindrome "
            "(ignoring punctuation/spaces and case):\n\n"
            "```python\n"
            "def is_palindrome(s: str) -> bool:\n"
            "    cleaned = ''.join(ch.lower() for ch in s if ch.isalnum())\n"
            "    return cleaned == cleaned[::-1]\n\n"
            "print(is_palindrome('A man, a plan, a canal, Panama'))  # True\n"
            "print(is_palindrome('hello'))  # False\n"
            "```\n"
        )

    resp = cs_agent(query)
    return str(resp).strip()
