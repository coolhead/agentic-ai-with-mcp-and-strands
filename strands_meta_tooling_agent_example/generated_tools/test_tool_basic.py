import json
import importlib
from typing import Any, Dict

TOOL_SPEC = {
    "name": "test_tool_basic",
    "description": "Tests another tool using sample inputs and expected integer outputs.",
    "inputSchema": {
        "json": {
            "type": "object",
            "properties": {
                "tool_name": {"type": "string"},
                "cases": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "input_text": {"type": "string"},
                            "expected_int": {"type": "integer"}
                        },
                        "required": ["input_text", "expected_int"]
                    }
                }
            },
            "required": ["tool_name", "cases"]
        }
    }
}

def test_tool_basic(tool_use: Dict[str, Any], **kwargs: Any) -> Dict[str, Any]:
    tool_use_id = tool_use.get("toolUseId", "")
    inp = tool_use.get("input", {}) or {}

    raw = inp.get("path")  # CLI passes the whole arg here as a string
    if not raw:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": "Missing input. Provide JSON string via use test_tool_basic '<json>'"}],
        }

    try:
        payload = json.loads(raw)
    except Exception as e:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Failed to parse JSON input: {e}. Got: {raw!r}"}],
        }

    tool_name = payload.get("tool_name")
    cases = payload.get("cases")

    if not tool_name or not isinstance(cases, list):
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": "Invalid payload. Need tool_name (string) and cases (list)."}],
        }

    try:
        mod = importlib.import_module(tool_name)
        tool_fn = getattr(mod, tool_name)
    except Exception as e:
        return {
            "toolUseId": tool_use_id,
            "status": "error",
            "content": [{"text": f"Failed to import tool '{tool_name}': {e}"}],
        }

    passed = 0
    results = []

    for i, case in enumerate(cases, 1):
        input_text = case.get("input_text", "")
        expected = case.get("expected_int", None)

        try:
            res = tool_fn({"toolUseId": f"case-{i}", "input": {"path": input_text}})
            text = res.get("content", [{}])[0].get("text", "")
            got_digits = "".join(c for c in text if c.isdigit())
            got = int(got_digits) if got_digits else None
        except Exception as e:
            results.append(f"❌ Case {i}: exception {type(e).__name__}: {e}")
            continue

        if got == expected:
            passed += 1
            results.append(f"✅ Case {i} passed (got {got})")
        else:
            results.append(f"❌ Case {i} failed (expected {expected}, got {got})")

    status = "success" if passed == len(cases) else "error"
    return {
        "toolUseId": tool_use_id,
        "status": status,
        "content": [{"text": f"Passed {passed}/{len(cases)} cases\n" + "\n".join(results)}],
    }

