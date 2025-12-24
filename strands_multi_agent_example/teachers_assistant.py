#!/usr/bin/env python3
"""
📁 Teacher's Assistant — Strands Multi-Agent (Manual Routing, No Tool-Calling)

Why this version exists:
- Some Bedrock models (e.g., meta.llama3-8b-instruct-v1:0) support system messages
  but do NOT support tool use (and/or tool use in streaming mode).
- The original workshop example uses the "Tool-Agent Pattern" (agents as tools),
  which requires model-side tool calling via Bedrock Converse/ConverseStream.
- This script keeps the multi-agent architecture, but routes in Python
  (manual routing), so it works with models that don't support tool use.

What you still get:
✅ Orchestrator ("Teacher's Assistant") + Specialists
✅ Routing logs ("Routed to X Assistant")
✅ Same CLI experience

Model used:
- meta.llama3-8b-instruct-v1:0
"""

from __future__ import annotations

import re
from strands import Agent
from strands.models import BedrockModel

from computer_science_assistant import computer_science_assistant
from english_assistant import english_assistant
from language_assistant import language_assistant
from math_assistant import math_assistant
from no_expertise import general_assistant


# -----------------------------
# Model configuration (non-streaming)
# -----------------------------
BEDROCK_MODEL_ID = "meta.llama3-8b-instruct-v1:0"

bedrock_model = BedrockModel(
    model_id=BEDROCK_MODEL_ID,
    temperature=0.3,
    streaming=False,
)

# This prompt is used ONLY for classification by the teacher agent.
TEACHER_SYSTEM_PROMPT = """
You are TeachAssist, a query router. Your only job is to classify the user query into ONE label.

Return exactly ONE of these labels (single word, uppercase):
MATH
ENGLISH
LANGUAGE
COMPSCI
GENERAL

Rules:
- MATH: equations, arithmetic, algebra, calculus, geometry, statistics, word problems
- ENGLISH: grammar, writing, comprehension, literature, rewriting, tone, summaries
- LANGUAGE: translation between languages, meaning in another language, bilingual phrasing
- COMPSCI: programming, code, debugging, algorithms, data structures, terminal, software engineering
- GENERAL: anything else

Do NOT answer the user. Only output the label.
""".strip()

teacher_classifier = Agent(
    model=bedrock_model,
    system_prompt=TEACHER_SYSTEM_PROMPT,
    callback_handler=None,
)

VALID_LABELS = {"MATH", "ENGLISH", "LANGUAGE", "COMPSCI", "GENERAL"}


def _normalize_label(text: str) -> str:
    """Extract a routing label from model output robustly."""
    if not text:
        return "GENERAL"
    t = text.strip().upper()
    if t in VALID_LABELS:
        return t
    m = re.search(r"\b(MATH|ENGLISH|LANGUAGE|COMPSCI|GENERAL)\b", t)
    if m:
        return m.group(1)
    return "GENERAL"


def determine_route(query: str) -> str:
    """Ask the classifier agent to output a label, then normalize it."""
    resp = teacher_classifier(query)
    return _normalize_label(str(resp))


def dispatch(label: str, query: str) -> str:
    """
    Call the specialist directly (manual routing).

    Note: Specialist functions already print "Routed to X Assistant".
    """
    if label == "MATH":
        return math_assistant(query)
    if label == "ENGLISH":
        return english_assistant(query)
    if label == "LANGUAGE":
        return language_assistant(query)
    if label == "COMPSCI":
        return computer_science_assistant(query)
    return general_assistant(query)


def main() -> None:
    print("\n📁 Teacher's Assistant Strands Agent 📁\n")
    print("Ask a question in any subject area, and I'll route it to the appropriate specialist.")
    print("Type 'exit' to quit.")

    while True:
        try:
            user_input = input("\n> ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                print("\nGoodbye! 👋")
                break

            label = determine_route(user_input)
            print(f"Routed to: {label}")

            answer = dispatch(label, user_input)
            print(str(answer).strip())

        except KeyboardInterrupt:
            print("\n\nExecution interrupted. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            print("Please try asking a different question.")


if __name__ == "__main__":
    main()
