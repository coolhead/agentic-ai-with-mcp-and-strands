from typing import Any, Dict
import json

TOOL_SPEC = {
    "name": "count_characters",
    "description": "Counts characters in text. Supports modes: chars, chars_no_spaces, words.",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text to count"},
                "count_mode": {
                    "type": "string",
                    "description": "chars | chars_no_spaces | words (default: chars)",
                },
            },
            "required": [],
        }
    },
}

def _compute(text: str, mode: str) -> int:
    mode = (mode or "chars").strip().lower()
    if mode == "chars":
        return len(text)
    if mode == "chars_no_spaces":
        return sum(1 for ch in text if not ch.isspace())
    if mode == "words":
        # simple whitespace tokenization
        return len(text.split())
    # fallback to default behavior
    return len(text)

def count_characters(tool_use: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    tool_use_id = tool_use.get("toolUseId", "")
    inp = tool_use.get("input", {}) or {}

    # Backward compatible: CLI passes string via input.path
    raw = inp.get("path")

    text = None
    mode = "chars"

    # If caller provided structured json (rare in your CLI, but supported)
    if isinstance(inp.get("json"), dict):
        text = inp["json"].get("text")
        mode = inp["json"].get("count_mode", mode)

    # If path is present, it can be either:
    # - plain text => count chars
    # - JSON string => parse {text, count_mode}
    if raw is not None:
        if isinstance(raw, str):
            s = raw.strip()
            if s.startswith("{") and s.endswith("}"):
                try:
                    payload = json.loads(s)
                    if isinstance(payload, dict):
                        text = payload.get("text", text)
                        mode = payload.get("count_mode", mode)
                except Exception:
                    # Not valid JSON; treat as plain text
                    text = raw
            else:
                text = raw

    if text is None:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": "Character count: 0"}],
        }

    character_count = _compute(str(text), str(mode))
    return {
        "toolUseId": tool_use_id,
        "status": "success",
        "content": [{"text": f"Character count: {character_count}"}],
    }
